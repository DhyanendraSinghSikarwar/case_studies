### Q1 ⭐⭐⭐ 🟡 Prefill vs decode at the serving level: how do the two phases map to TTFT and per-token latency, why are they bottlenecked differently, and what does that change about what you optimise first? (Part 1 Q7 has the mechanism; go to the serving consequences.)
**Asked at:** all types; inference-platform teams, GenAI-engineer and MLE rounds; interview-prep guide, not a candidate report
**Say this first (1 line):** Prefill is one big parallel pass over the prompt that is compute-bound and sets TTFT; decode is one token per step that is memory-bandwidth-bound and sets per-token latency, so you optimise the phase that dominates your product's latency (decode for chat with long answers, prefill for long prompts).

**Then explain:**
- **Prefill and TTFT:** all prompt tokens go through the model at once, about `2 x params x tokens` FLOPs, so a long prompt is compute-bound. TTFT is queue wait + prefill + network (the NVIDIA NIM metrics page counts queueing and network inside TTFT, vendor docs).
- **Decode and TPOT/ITL:** each step produces one token per sequence and must read all weights plus that sequence's KV cache from HBM, so it is memory-bandwidth-bound. Total latency = TTFT + (output tokens - 1) x TPOT. Mechanism is in Part 1 Q7; the roofline view is Part 1 Q32 and Part 10 Q33.
- **The crossover:** with the assumed numbers in the code, weight reading costs 7.0 ms per step, and prefill compute passes that at about `7 ms x 312e12 / (2 x 7e9) = 156` tokens. Below that even prefill is memory-bound; above it, compute-bound.
- **What to optimise first:** measure the split. Decode-heavy (chat, long outputs): batch more (needs KV memory, Q3/Q4), quantize weights or KV (Q8, Q22), speculative decoding (Q11). Prefill-heavy (RAG, long documents): prefix caching (Q14), chunked prefill (Q20), more compute via tensor parallelism (Q17).
- **They interfere:** if both share one batch, a long prefill stalls everyone's decode steps. That is why chunked prefill (Q20) and prefill/decode disaggregation (Q32) exist.

**Example:** (assumed A100-class numbers, a roofline lower bound, not measured) a 7B fp16 model. Request A: 1,024-token prompt, 200 output tokens, 20 ms assumed queue wait. TTFT = 65.9 ms, TPOT = 7.0 ms, E2E = 1,458.9 ms, and 95.5% of E2E is decode. Make the prompt 4x longer (4,096): TTFT rises to 203.8 ms but E2E only to 1,596.8 ms. Make the output 4x longer (800 tokens): E2E becomes 5,658.9 ms, 3.9x. So for this chat shape, shaving decode time matters most; a prompt-heavy product would look the other way round.

**Code:** (toy roofline; hardware numbers are assumptions)
```python
# Toy roofline for one request: prefill vs decode. ASSUMED hardware (not measured):
# bf16 peak 312e12 FLOP/s, HBM 2.0e12 B/s (A100-80GB-class numbers from memory, check spec sheet).
PEAK, BW = 312e12, 2.0e12
P, W_BYTES = 7e9, 7e9 * 2          # 7B params, fp16 weights
def step_time(tokens_in_step):
    flops = 2 * P * tokens_in_step          # ~2 FLOPs per parameter per token
    t_compute = flops / PEAK
    t_memory = W_BYTES / BW                 # weights read once per step (KV read ignored)
    return max(t_compute, t_memory), ("compute" if t_compute > t_memory else "memory")

for prompt in (128, 1024, 4096):
    t, bound = step_time(prompt)
    print(f"prefill prompt={prompt:5d}: {t*1e3:7.1f} ms ({bound}-bound)")
t, bound = step_time(1)
print(f"decode  1 token/step    : {t*1e3:7.1f} ms ({bound}-bound)")

queue_ms = 20.0                              # assumed queueing delay
for prompt, out in ((1024, 200), (4096, 200), (1024, 800)):
    ttft = queue_ms + step_time(prompt)[0] * 1e3
    tpot = step_time(1)[0] * 1e3
    e2e = ttft + (out - 1) * tpot
    print(f"prompt={prompt:5d} out={out:4d}: TTFT={ttft:6.1f} ms  TPOT={tpot:5.2f} ms  E2E={e2e:7.1f} ms  decode share={100*(e2e-ttft)/e2e:4.1f}%")
```
**Output (my run):**
```
prefill prompt=  128:     7.0 ms (memory-bound)
prefill prompt= 1024:    45.9 ms (compute-bound)
prefill prompt= 4096:   183.8 ms (compute-bound)
decode  1 token/step    :     7.0 ms (memory-bound)
prompt= 1024 out= 200: TTFT=  65.9 ms  TPOT= 7.00 ms  E2E= 1458.9 ms  decode share=95.5%
prompt= 4096 out= 200: TTFT= 203.8 ms  TPOT= 7.00 ms  E2E= 1596.8 ms  decode share=87.2%
prompt= 1024 out= 800: TTFT=  65.9 ms  TPOT= 7.00 ms  E2E= 5658.9 ms  decode share=98.8%
```

**Follow-ups:**
- *Why does decode not use the GPU's compute well at batch 1?* One token per weight read gives very low arithmetic intensity; batching several sequences reuses the same weight read (Q7).
- *Does TTFT include queueing?* In the NIM definition, yes. Under load, queue wait is often the biggest part of p99 TTFT (Q46).
- *What did the toy ignore?* KV-cache reads (they grow with context), kernel overheads, communication in TP, and real efficiency below peak.

**Common mistakes:** calling prefill memory-bound for normal prompts; leaving queue time out of TTFT; optimising prefill for a decode-dominated workload; quoting the toy milliseconds as GPU measurements.


### Q2 ⭐⭐⭐ 🟡 Latency and throughput metrics for LLM serving: define TTFT, TPOT/ITL, end-to-end latency, tokens per second (system vs per user), requests per second and goodput. How do percentiles and SLOs apply, and why is the mean misleading?
**Asked at:** all types; inference-platform teams, product companies, GCCs; interview-prep guide, not a candidate report
**Say this first (1 line):** TTFT is time to first token, TPOT/ITL is the time between later tokens, E2E is the whole request, throughput is tokens or requests per second, and goodput counts only requests that met their SLOs; always report percentiles (p50, p95, p99) because the mean hides the tail users actually feel.

**Then explain:**
- **TTFT:** request arrival to first token, including queue and network (NVIDIA NIM metrics page, vendor docs).
- **TPOT / ITL:** the same page defines ITL as `(E2E - TTFT) / (output tokens - 1)`. Tools differ in names: some report TPOT as that per-request average and ITL as every individual gap, so state your definition (vLLM's benchmark CLI reports TTFT, ITL and TPOT with mean, median and P99; check live docs).
- **E2E latency:** `TTFT + (n - 1) x TPOT`. Long answers make E2E dominated by decode.
- **Throughput:** system tokens/s (all users, what the GPU bill sees) vs per-user tokens/s (what one reader feels, roughly 1/TPOT). Raising batch size raises the first and lowers the second (Q7). Requests/s (RPS) depends on output lengths, so quote the length mix.
- **Goodput:** requests per second that meet all stated SLOs, for example TTFT <= X and TPOT <= Y. DistServe frames serving this way (goodput under TTFT and TPOT SLOs, from the paper abstract). A server can show high throughput and low goodput.
- **Percentiles and the mean:** SLOs are set on a percentile per metric (for example p99 TTFT), measured on a realistic arrival process (Q30). Latency is heavy-tailed, so the mean sits near the typical request while the p99 is several times larger.

**Example:** a 4-request log (synthetic, below). TTFTs are 0.4, 0.4, 1.0 and 0.3 s; ITL is 0.1 s for each (10 tokens/s per user). The four requests overlap in time, so system throughput is 94 tokens / 4.5 s = 20.9 tok/s, while the mean per-user rate is 8.4 tok/s. For the heavy-tail point I drew 10,000 synthetic TTFTs from a lognormal (an assumed shape): mean 0.449 s but p99 2.402 s, and 91.0% meet a 1.0 s target, so 9% of users miss it while the mean looks comfortable.

**Code:** (synthetic data; the full log-processing code is Q16)
```python
import numpy as np
# Hand-checkable log: (arrival, first_token, finish, output_tokens), seconds. Synthetic.
log = [(0.0, 0.4, 2.4, 21), (0.1, 0.5, 4.5, 41), (0.2, 1.2, 3.2, 21), (1.0, 1.3, 2.3, 11)]
ttft = [f - a for a, f, e, n in log]
e2e = [e - a for a, f, e, n in log]
itl = [(e - f) / (n - 1) for a, f, e, n in log]      # (E2E - TTFT)/(n-1), the NIM-style definition
print("TTFT:", [round(x, 2) for x in ttft])
print("E2E :", [round(x, 2) for x in e2e])
print("ITL :", [round(x, 3) for x in itl])
span = max(e for _, _, e, _ in log) - min(a for a, _, _, _ in log)
toks = sum(n for *_, n in log)
print(f"system tok/s = {toks}/{span:.1f} = {toks/span:.1f}; req/s = {len(log)/span:.2f}")
print(f"per-user tok/s (mean of n/E2E) = {np.mean([n/x for (*_, n), x in zip(log, e2e)]):.1f}")

# Mean vs tail on a synthetic heavy-tailed TTFT sample (lognormal, assumed shape)
rng = np.random.default_rng(0)
s = rng.lognormal(mean=np.log(0.3), sigma=0.9, size=10000)
print(f"synthetic TTFT: mean={s.mean():.3f}s p50={np.percentile(s,50):.3f}s p95={np.percentile(s,95):.3f}s p99={np.percentile(s,99):.3f}s")
slo = 1.0
print(f"share meeting TTFT<=1.0s: {100*(s<=slo).mean():.1f}%  (mean {s.mean():.2f}s looks fine)")
```
**Output (my run):**
```
TTFT: [0.4, 0.4, 1.0, 0.3]
E2E : [2.4, 4.4, 3.0, 1.3]
ITL : [0.1, 0.1, 0.1, 0.1]
system tok/s = 94/4.5 = 20.9; req/s = 0.89
per-user tok/s (mean of n/E2E) = 8.4
synthetic TTFT: mean=0.449s p50=0.298s p95=1.312s p99=2.402s
share meeting TTFT<=1.0s: 91.0%  (mean 0.45s looks fine)
```

**Follow-ups:**
- *Why not just report p50?* Half the users are slower than p50; p99 decides complaints and timeouts. At low traffic p99 needs many samples to be stable.
- *Do you average percentiles across replicas?* No; merge the raw samples or histograms (Part 11 for monitoring).
- *What is a good SLO?* Product-driven (typing speed for chat, time-to-answer for agents); I would not quote universal numbers.

**Common mistakes:** reporting only mean latency; mixing system and per-user tokens/s; computing ITL with n instead of n - 1; measuring TTFT from first-byte at the server and ignoring queue wait; calling throughput "goodput".


### Q3 ⭐⭐⭐ 🟡 Budget GPU memory for serving: weights, KV cache, activations and runtime overhead. For a 7B and a 70B model on an 80 GB GPU, what fits, what does gpu_memory_utilization control, and how do tensor-parallel shards change the maths? (Part 1 Q15 has the KV formula.)
**Asked at:** all types; inference-platform teams, MLE rounds; interview-prep guide, not a candidate report
**Say this first (1 line):** Per GPU, the KV pool is what is left of `gpu_memory_utilization x GPU memory` after weights and runtime overhead; weights are `params x bytes / TP`, so a 7B fits easily on one 80 GB GPU while a 70B in fp16 does not fit on one and leaves little cache at TP=2.

**Then explain:**
- **Four buckets:** weights, KV cache, activations/workspace (grows with tokens per step; prefill workspace scales with tokens per step, and vLLM's max_num_batched_tokens knob caps it; from memory, check, Q20), and runtime overhead (CUDA context, graphs, fragmentation).
- **`gpu_memory_utilization`:** in vLLM docs it is the fraction of GPU memory the engine instance may use; whatever remains after weights and profiling becomes KV blocks. Higher means more cache but less headroom for spikes or other processes (semantics as of the docs read on 2026-10-24, check live docs).
- **Tensor parallel:** weights are sharded across the TP ranks, and so are KV heads, so KV bytes per token per GPU also fall by the TP factor. Total cluster KV is not magically bigger; you freed per-GPU space by splitting the weights.
- **KV per token:** `2 x layers x kv_heads x head_dim x bytes` (Part 1 Q15). Llama-2-7B-style (MHA): 512 KiB. A 70B-class GQA with 80 layers and 8 KV heads: 320 KiB (from memory, check the config).
- **Assumptions in the run:** 80 GiB per GPU, utilisation 0.90, 3 GiB overhead per GPU (a guess), 70e9 parameters, fp16 weights and KV.

**Example:** from the run. 7B MHA on one GPU: weights 12.6 GiB, KV pool 56.4 GiB, 115,601 tokens, about 28 sequences of 4,096 tokens. 70B fp16 on one GPU: 130.4 GiB of weights, does not fit. TP=2: 65.2 GiB per GPU, pool only 3.8 GiB, 24,952 tokens (about 6 sequences at 4k). TP=4: 32.6 GiB per GPU, pool 36.4 GiB, 477,151 tokens (about 116). Going from TP=2 to TP=4 gave 19x more cache tokens, because weights per GPU halve and KV per token per GPU halves at the same time. One-byte weights on a single GPU also fit, but then leave only 12,476 tokens of fp16 KV.

**Code:** (assumed GPU and overhead; matches the hand maths above)
```python
# GPU memory budget. ASSUMED: 80 GiB per GPU, activation/runtime overhead 3 GiB per GPU (guess), fp16 = 2 B.
GiB = 2**30
def kv_per_token(L, n_kv, dh, b=2): return 2 * L * n_kv * dh * b
def plan(name, params, L, n_kv, dh, tp, util=0.90, wbytes=2, overhead_gib=3, gpu_gib=80):
    budget = util * gpu_gib * GiB                          # what the engine may use per GPU
    weights = params * wbytes / tp
    kv_tok = kv_per_token(L, n_kv, dh) / tp                # KV heads are sharded across TP ranks
    kv_pool = budget - weights - overhead_gib * GiB
    if kv_pool <= 0:
        print(f"{name:34s} weights/GPU {weights/GiB:6.1f} GiB  -> DOES NOT FIT"); return
    toks = kv_pool / kv_tok                                # tokens per GPU; same on every rank
    print(f"{name:34s} weights/GPU {weights/GiB:6.1f}  KV pool/GPU {kv_pool/GiB:6.1f} GiB  KV/token/GPU {kv_tok/1024:6.1f} KiB  tokens {toks:10,.0f}  ~seqs@4k {toks/4096:7.0f}")
plan("7B MHA (L32,kv32) fp16 TP1", 6.74e9, 32, 32, 128, 1)
plan("7B MHA fp16 TP1 util=0.95", 6.74e9, 32, 32, 128, 1, util=0.95)
plan("70B GQA (L80,kv8) fp16 TP1", 70e9, 80, 8, 128, 1)
plan("70B GQA fp16 TP2", 70e9, 80, 8, 128, 2)
plan("70B GQA fp16 TP4", 70e9, 80, 8, 128, 4)
plan("70B GQA 1-byte weights TP1", 70e9, 80, 8, 128, 1, wbytes=1)
```
**Output (my run):**
```
7B MHA (L32,kv32) fp16 TP1         weights/GPU   12.6  KV pool/GPU   56.4 GiB  KV/token/GPU  512.0 KiB  tokens    115,601  ~seqs@4k      28
7B MHA fp16 TP1 util=0.95          weights/GPU   12.6  KV pool/GPU   60.4 GiB  KV/token/GPU  512.0 KiB  tokens    123,793  ~seqs@4k      30
70B GQA (L80,kv8) fp16 TP1         weights/GPU  130.4 GiB  -> DOES NOT FIT
70B GQA fp16 TP2                   weights/GPU   65.2  KV pool/GPU    3.8 GiB  KV/token/GPU  160.0 KiB  tokens     24,952  ~seqs@4k       6
70B GQA fp16 TP4                   weights/GPU   32.6  KV pool/GPU   36.4 GiB  KV/token/GPU   80.0 KiB  tokens    477,151  ~seqs@4k     116
70B GQA 1-byte weights TP1         weights/GPU   65.2  KV pool/GPU    3.8 GiB  KV/token/GPU  320.0 KiB  tokens     12,476  ~seqs@4k       3
```

**Follow-ups:**
- *Raise utilisation to 0.95?* For the 7B case the pool goes from 56.4 to 60.4 GiB (+7%), in exchange for less safety margin against OOM (Q47).
- *Is TP=4 always better than TP=2?* It buys cache and per-token speed but costs communication and half the replicas per node (Q17).
- *What if TP exceeds the number of KV heads?* Then KV heads must be replicated across ranks (from memory, check the engine docs).

**Common mistakes:** forgetting that KV is the bulk of the budget at long context or high batch; using attention heads instead of KV heads; mixing GB and GiB; assuming TP gives free total capacity; treating the 3 GiB overhead as a constant (it is an assumption here).


### Q4 ⭐⭐⭐ 🟡 Capacity planning from the KV cache: how many concurrent sequences fit after loading the weights, how do context length, GQA/MQA and cache dtype change that number, and how do you turn it into a replica count using Little's law?
**Asked at:** product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report
**Say this first (1 line):** Concurrent sequences = KV pool / KV bytes per sequence; GQA and a smaller cache dtype raise it, longer context lowers it, and Little's law (in flight = arrival rate x time in system) turns the concurrency you need into replicas.

**Then explain:**
- **Per-sequence cache:** `tokens x 2 x layers x kv_heads x head_dim x bytes`, rounded up to whole blocks (16 tokens in this toy; PagedAttention allocates by block, Q5).
- **Levers:** fewer KV heads (GQA/MQA, Part 1 Q10), smaller dtype (FP8 KV, Q22), shorter context, sliding-window or other cache reductions (Part 1 Q23).
- **Little's law:** `L = lambda x W`. L is average requests in the system, lambda the arrival rate, W the average time a request holds KV (queue is not holding KV, but running time is). Required replicas = `L / (per-replica capacity x target fill)`.
- **KV capacity is only one constraint.** Throughput and TPOT limit how many sequences you can actually run per step (Q7), and W itself grows when the system is loaded, so I would re-check after a load test (Q30).
- **Assumptions in the run:** 80 GiB GPU, util 0.9, 3 GiB overhead, 13.5e9-byte weights, every sequence at full context (conservative; real sequences are shorter on average), plus hypothetical traffic.

**Example:** from the run, per-replica concurrency on one GPU: MHA fp16 at 2,048 tokens: 1.00 GiB per sequence, 56 sequences; at 8,192: 14. GQA (8 KV heads) fp16: 225 at 2,048 and 56 at 8,192. GQA with 1-byte KV: 451 and 112 (scale metadata ignored). Hypothetical traffic: 20 req/s, each request in the system for 8 s, so L = 160. With the 225 cap and a planned 70% fill, `ceil(160 / (225 x 0.7)) = 2` replicas. If time in system doubles to 16 s (slower decode under load), L = 320 and the answer becomes 3. The 2 is sensitive: 160/157.5 is just over 1.

**Code:** (hypothetical traffic; assumed hardware)
```python
import math
GiB = 2**30
# ASSUMED: 80 GiB GPU, util 0.9, 3 GiB overhead, 16-token blocks, 7B-class weights 13.5e9 B per replica.
def cap(kv_tok_bytes, ctx, weights=13.5e9, block=16, util=0.9, gpu=80*GiB, over=3*GiB):
    pool = util*gpu - weights - over
    per_seq = math.ceil(ctx/block)*block*kv_tok_bytes     # block rounding
    return int(pool // per_seq), per_seq/GiB
cases = {"MHA n_kv=32 fp16": 2*32*32*128*2, "GQA n_kv=8 fp16": 2*32*8*128*2, "GQA n_kv=8 fp8 KV": 2*32*8*128*1}
for name, b in cases.items():
    for ctx in (2048, 8192):
        c, g = cap(b, ctx)
        print(f"{name:18s} ctx={ctx:5d}: {b/1024:5.0f} KiB/token, {g:5.2f} GiB/seq, max concurrent seqs = {c}")

# Little's law: L = lambda * W. HYPOTHETICAL traffic.
lam, W = 20.0, 8.0                      # req/s, mean seconds a request occupies KV
L = lam * W
c, _ = cap(cases["GQA n_kv=8 fp16"], 2048)
headroom = 0.7                          # assumed: plan to run KV at 70% so bursts do not preempt
print(f"in flight = {lam}*{W} = {L:.0f}; per-replica cap {c}; replicas (KV only) = {math.ceil(L/(c*headroom))}")
print("same load, sequences twice as long in system (W=16):", math.ceil(lam*16/(c*headroom)))
```
**Output (my run):**
```
MHA n_kv=32 fp16   ctx= 2048:   512 KiB/token,  1.00 GiB/seq, max concurrent seqs = 56
MHA n_kv=32 fp16   ctx= 8192:   512 KiB/token,  4.00 GiB/seq, max concurrent seqs = 14
GQA n_kv=8 fp16    ctx= 2048:   128 KiB/token,  0.25 GiB/seq, max concurrent seqs = 225
GQA n_kv=8 fp16    ctx= 8192:   128 KiB/token,  1.00 GiB/seq, max concurrent seqs = 56
GQA n_kv=8 fp8 KV  ctx= 2048:    64 KiB/token,  0.12 GiB/seq, max concurrent seqs = 451
GQA n_kv=8 fp8 KV  ctx= 8192:    64 KiB/token,  0.50 GiB/seq, max concurrent seqs = 112
in flight = 20.0*8.0 = 160; per-replica cap 225; replicas (KV only) = 2
same load, sequences twice as long in system (W=16): 3
```

**Follow-ups:**
- *Why plan at 70% fill?* Bursts and length variance cause preemption (Q21); the 70% is my assumption, tune it from load tests.
- *Does a bigger cap mean more throughput?* Not automatically; it allows a bigger batch, but TPOT rises with batch (Q7).
- *Does prefix sharing change it?* Yes, shared blocks count once (Q5, Q14).

**Common mistakes:** sizing from average length when the tail dominates; forgetting block rounding; counting queued requests as holding KV; treating KV concurrency as the throughput limit; not stating that traffic numbers are assumptions.


### Q5 ⭐⭐⭐ 🟡 What is PagedAttention and how does vLLM's block manager work (fixed-size blocks, block tables, near-zero fragmentation, sharing and copy-on-write)? What problem in earlier systems did it fix?
**Asked at:** all types; inference-platform teams, AI labs and GenAI startups; interview-prep guide, not a candidate report lists it as a core topic
**Say this first (1 line):** PagedAttention stores each sequence's KV cache in fixed-size blocks that need not be contiguous, tracked by a per-sequence block table, so memory is allocated on demand with near-zero waste and blocks can be shared with copy-on-write; it fixed the fragmentation and duplication that capped batch size in earlier systems.

**Then explain:**
- **The problem (vLLM paper abstract, arXiv 2309.06180):** KV memory per request is large and grows and shrinks; with contiguous max-length reservations, fragmentation and duplication limit the batch size. Reserved-but-unused space is internal fragmentation, gaps between slabs are external.
- **The idea:** modelled on OS virtual memory paging. Logical blocks of a sequence map through a block table to physical blocks anywhere in a pool. The attention kernel reads K and V through the table.
- **Block manager:** a free list of physical blocks, a table per sequence, a new block only when the last one fills. Waste is at most the unfilled part of one block per sequence.
- **Sharing:** parallel sampling, beam search and shared prompts point to the same physical blocks with reference counts. A write into a shared block triggers copy-on-write: allocate a new block, copy, then write.
- **Claim, labelled:** the authors report 2-4x throughput vs FasterTransformer and Orca at the same latency, larger for longer sequences (authors' claim, their setup). vLLM's own design page for the kernel is flagged as historical and says it no longer describes today's code, so treat details such as block size as version-specific (check live docs).

**Example:** run below (block = 16 tokens). A sequence of 40 tokens uses 3 blocks. Fork it (a second sample from the same prompt): still 3 physical blocks, each with refcount 2. The fork appends a token into the half-full last block, so copy-on-write fires and the pool uses 4 blocks. Free both: all 64 blocks are free again. Waste on 100 synthetic sequences of 20-600 tokens: a contiguous 2,048-token reservation wastes 171,528 token slots; paging wastes 744 (under 16 per sequence).

**Code:** (toy; the fuller allocator with free-list tests is Q39)
```python
# Minimal block-table demo (the fuller allocator is Part 10 Q39). Block = 16 tokens.
BLOCK = 16
class Pool:
    def __init__(self, n): self.free = list(range(n)); self.ref = {}
    def alloc(self):
        b = self.free.pop(); self.ref[b] = 1; return b
    def release(self, b):
        self.ref[b] -= 1
        if self.ref[b] == 0: del self.ref[b]; self.free.append(b)
class Seq:
    def __init__(self, pool): self.pool, self.table, self.n = pool, [], 0
    def append(self):                       # add one token
        if self.n % BLOCK == 0: self.table.append(self.pool.alloc())
        else:
            last = self.table[-1]
            if self.pool.ref[last] > 1:     # shared and about to be written: copy-on-write
                self.pool.release(last); self.table[-1] = self.pool.alloc(); print("  CoW on logical block", len(self.table)-1)
        self.n += 1
    def fork(self):
        c = Seq(self.pool); c.table = list(self.table); c.n = self.n
        for b in c.table: self.pool.ref[b] += 1
        return c
    def free(self):
        for b in self.table: self.pool.release(b)
        self.table = []

pool = Pool(64)
a = Seq(pool)
for _ in range(40): a.append()                       # 40 tokens -> 3 blocks (last one 8/16 full)
print("a.table", a.table, "used blocks", len(pool.ref))
b = a.fork()                                         # e.g. a second sample from the same prompt
print("after fork: used blocks", len(pool.ref), "refcounts", [pool.ref[x] for x in a.table])
b.append()                                           # writes into the shared partial block
print("b.table", b.table, "a.table", a.table, "used blocks", len(pool.ref))
a.free(); b.free()
print("after freeing both: used", len(pool.ref), "free", len(pool.free))

# Waste: contiguous reservation at max length vs paged blocks (synthetic lengths, assumed)
import random
random.seed(1)
lens = [random.randint(20, 600) for _ in range(100)]; MAX = 2048
contig = sum(MAX - l for l in lens)
paged = sum(-(-l // BLOCK) * BLOCK - l for l in lens)
print(f"tokens reserved but unused: contiguous@{MAX} = {contig}, paged = {paged} (limit < {BLOCK} per sequence)")
```
**Output (my run):**
```
a.table [63, 62, 61] used blocks 3
after fork: used blocks 3 refcounts [2, 2, 2]
  CoW on logical block 2
b.table [63, 62, 60] a.table [63, 62, 61] used blocks 4
after freeing both: used 0 free 64
tokens reserved but unused: contiguous@2048 = 171528, paged = 744 (limit < 16 per sequence)
```

**Follow-ups:**
- *Does it change model outputs?* No, only where the same numbers are stored.
- *What happens when blocks run out?* The scheduler preempts (recompute or swap), Q21.
- *Relation to prefix caching?* Hashing full blocks lets later requests reuse them (Q14).

**Common mistakes:** saying PagedAttention speeds up the attention maths (it fixes memory management and so allows bigger batches); confusing it with FlashAttention (Part 1 Q11); claiming zero waste (the last block is partly empty); forgetting reference counts and copy-on-write.


### Q6 ⭐⭐⭐ 🟡 Static vs dynamic vs continuous (in-flight, iteration-level) batching: how does each work, why does continuous batching raise throughput when output lengths vary, and what does it cost (scheduling, memory pressure)?
**Asked at:** all types; inference-platform teams, GenAI startups; interview-prep guide, not a candidate report
**Say this first (1 line):** Static batching runs a fixed batch until its longest request ends, dynamic batching just forms that batch from a time window, and continuous (iteration-level) batching re-forms the batch every decoding step so finished requests leave and waiting ones join immediately, which raises throughput when output lengths vary.

**Then explain:**
- **Static:** pick N requests, run until all finish. Short requests wait (padding or idle slots) for the longest one.
- **Dynamic:** wait up to a timeout or batch size, then run as static. Better than one-by-one, same tail problem (from memory: this is how generic model servers batch, check your server).
- **Continuous:** Orca introduced iteration-level scheduling and selective batching; the authors report 36.9x throughput vs FasterTransformer on GPT-3 175B at the same latency (authors' claim, their setup). vLLM and others use the same idea, and vLLM pairs it with PagedAttention (Q5).
- **Why it helps:** decode cost per step is roughly flat in the number of active rows (Q7), so empty slots are wasted capacity. Refilling slots uses them.
- **What it costs:** a scheduler running every step; KV memory must be allocated and freed dynamically (hence PagedAttention, Q5); prefill of newcomers interferes with others' decode (Q20); when memory runs out it must preempt (Q21).

**Example:** run below (synthetic): 64 requests with output lengths 5-200 tokens (mean 107.3), 8 slots, all arrive together, and an assumed step cost of `1 + 0.02 x active`. Static: makespan 1,665.8 units, 4.12 tokens per unit, mean finish 857.6. Continuous: 1,106.3 units, 6.21 tokens per unit, mean finish 541.9. That is 1.51x throughput here. The ratio comes entirely from my length spread and the toy cost model; it says nothing about the papers' numbers. With one length for every request the gap would vanish.

**Code:** (toy; the fuller scheduler comparison with arrivals is Q38)
```python
import random
# Synthetic: 64 requests, output lengths 5..200 tokens (assumed), 8 batch slots, all arrive at t=0.
random.seed(0)
lens = [random.randint(5, 200) for _ in range(64)]; SLOTS = 8
def step_cost(active): return 1.0 + 0.02 * active     # ASSUMED: one step costs a bit more with more active seqs

def static():
    t = 0.0; done = []
    for i in range(0, len(lens), SLOTS):
        grp = lens[i:i+SLOTS]
        for s in range(max(grp)):                       # batch runs until its LONGEST request finishes
            t += step_cost(len(grp))
            for l in grp:
                if l == s + 1: done.append(t)
    return t, done
def continuous():
    t = 0.0; q = list(lens); slots = []; done = []
    while q or slots:
        while q and len(slots) < SLOTS: slots.append(q.pop(0))   # refill the moment a slot frees
        t += step_cost(len(slots))
        slots = [l - 1 for l in slots]
        done += [t] * sum(1 for l in slots if l == 0)
        slots = [l for l in slots if l > 0]
    return t, done
for name, fn in (("static", static), ("continuous", continuous)):
    T, d = fn()
    print(f"{name:10s} makespan={T:8.1f} steps-units  tokens/unit={sum(lens)/T:5.2f}  mean finish={sum(d)/len(d):7.1f}")
print("total tokens", sum(lens), "| mean len", round(sum(lens)/len(lens), 1), "| sum of per-batch max", sum(max(lens[i:i+SLOTS]) for i in range(0, 64, SLOTS)))
```
**Output (my run):**
```
static     makespan=  1665.8 steps-units  tokens/unit= 4.12  mean finish=  857.6
continuous makespan=  1106.3 steps-units  tokens/unit= 6.21  mean finish=  541.9
total tokens 6866 | mean len 107.3 | sum of per-batch max 1436
```

**Follow-ups:**
- *When is static fine?* Same-length offline jobs.
- *Does continuous batching change outputs?* No (apart from floating-point batch effects).
- *What limits batch growth?* KV memory and TPOT SLOs (Q4, Q7).

**Common mistakes:** quoting 36.9x as a general speedup; ignoring that gains depend on length variance; forgetting the memory-management side; calling dynamic batching "continuous".


### Q7 ⭐⭐⭐ 🟡 Throughput vs latency: how do batch size and concurrency move TTFT, TPOT and tokens per second, where is the knee of the curve, and how do you pick an operating point for a chat product vs an offline job?
**Asked at:** product companies, inference-platform teams, GCCs; interview-prep guide, not a candidate report frames chat vs offline objectives
**Say this first (1 line):** Raising batch size or concurrency raises system tokens/s with diminishing returns while TPOT and TTFT worsen; the knee is where the extra throughput stops being worth the latency, so chat runs below the knee under a TPOT SLO and offline jobs run near the KV-memory limit.

**Then explain:**
- **Why throughput rises:** the weight read is shared by every sequence in the step (Q1, Part 1 Q32).
- **Why it flattens:** each added sequence adds its own KV read, and eventually compute; step time grows, so tokens/s gains shrink.
- **What gets worse:** TPOT rises with batch; TTFT rises with queueing and with prefill interference (Q20); beyond the KV cap requests queue or are preempted (Q21).
- **Concurrency vs batch:** concurrency is requests in flight; the engine batches those that fit. If concurrency exceeds what fits, TTFT grows through queueing (Little's law, Q4).
- **Operating point:** chat: set a p99 TPOT and TTFT SLO, load-test open-loop (Q30), pick the highest load that holds them. Offline: maximise tokens/s subject to memory, ignore per-token latency (Q34).

**Example:** run below, step time `max(compute, (weights + b x KV read)/BW)`, assumed A100-class numbers, 7B fp16, MHA KV 0.5 MiB per token, 1,000-token contexts. Batch 1: 7.26 ms, 138 tok/s. Batch 16: 11.19 ms, 1,429 tok/s. Batch 64: 23.78 ms, 2,692 tok/s. Batch 96: 32.17 ms, 2,985 tok/s, only 10.9% more than the previous row for a 1.5x larger batch. KV memory caps the batch at 114. With a hypothetical 20 ms TPOT target: largest batch 49, 2,469 tok/s. Offline at batch 114: 3,091 tok/s (+25%) at 36.9 ms per token. The toy's asymptote is 3,815 tok/s because per-sequence KV reads dominate. TTFT is not modelled.

**Code:** (assumed hardware; hypothetical SLO)
```python
# Decode-step model, ASSUMED A100-class: BW 2.0e12 B/s, peak 312e12 FLOP/s, 7B fp16 (14e9 B), KV 0.5 MiB/token (MHA), avg ctx 1000.
BW, PEAK = 2.0e12, 312e12
W = 14e9; kv_read = 0.5 * 2**20 * 1000     # bytes of KV each sequence reads per step
comp = 2 * 7e9 / PEAK                      # compute seconds per token
GiB = 2**30
kv_cap = int((0.9*80*GiB - W - 3*GiB) // (0.5 * 2**20 * 1000))   # KV memory limit on batch (1000-token seqs)
def t_step(b): return max(b * comp, (W + b * kv_read) / BW)
print("KV memory caps batch at", kv_cap)
print(" b   TPOT(ms)  tok/s   gain vs prev")
prev = None
for b in (1, 2, 4, 8, 16, 32, 64, 96):
    t = t_step(b); thr = b / t
    print(f"{b:3d}  {t*1e3:7.2f}  {thr:7.0f}  {'' if prev is None else f'{100*(thr/prev-1):5.1f}%'}")
    prev = thr
SLO_MS = 20.0                              # hypothetical chat TPOT target
best = max(b for b in range(1, kv_cap + 1) if t_step(b) * 1e3 <= SLO_MS)
print(f"chat (TPOT<= {SLO_MS} ms): largest batch = {best} -> {best/t_step(best):.0f} tok/s; offline: batch {kv_cap} -> {kv_cap/t_step(kv_cap):.0f} tok/s at TPOT {t_step(kv_cap)*1e3:.1f} ms")
print("asymptote 1/(kv_read/BW) =", round(BW / kv_read), "tok/s")
```
**Output (my run):**
```
KV memory caps batch at 114
 b   TPOT(ms)  tok/s   gain vs prev
  1     7.26      138  
  2     7.52      266   93.0%
  4     8.05      497   87.0%
  8     9.10      879   76.9%
 16    11.19     1429   62.5%
 32    15.39     2079   45.5%
 64    23.78     2692   29.4%
 96    32.17     2985   10.9%
chat (TPOT<= 20.0 ms): largest batch = 49 -> 2469 tok/s; offline: batch 114 -> 3091 tok/s at TPOT 36.9 ms
asymptote 1/(kv_read/BW) = 3815 tok/s
```

**Follow-ups:**
- *Where is the knee in practice?* It depends on model, context length, hardware and kernels; find it by load test, not formula.
- *How do you push the knee out?* GQA, KV quantization, weight quantization (Q8), faster attention kernels.
- *Why not always run at the knee?* Headroom for bursts and p99.

**Common mistakes:** reading the knee from mean latency; benchmarking closed-loop only; forgetting KV capacity as the hard cap; using one number for chat and batch jobs.


### Q8 ⭐⭐⭐ 🟡 Quantization for inference: what do INT8, INT4 and FP8 change (weight-only vs weight-and-activation, memory vs compute), which phase does each speed up, and why is the speedup not simply 'bits halved, speed doubled'?
**Asked at:** all types; inference-platform teams, GenAI startups, GCCs; interview-prep guide, not a candidate report
**Say this first (1 line):** Quantization shrinks bytes (weights, sometimes KV and activations) and, when activations are quantized too, can use faster low-precision math; weight-only INT4/INT8 mainly speeds up memory-bound decode, W8A8 and FP8 also help compute-bound prefill, and speedup is below the bit ratio because KV reads, dequantisation and unquantized parts remain.

**Then explain:**
- **Weight-only (W4A16, W8A16, the GPTQ/AWQ style):** weights are stored in few bits and dequantised to 16-bit inside the kernel. Fewer bytes read per decode step; prefill is compute-bound, so little gain.
- **Weight-and-activation (W8A8, FP8):** both operands in low precision on matching tensor-core hardware. SmoothQuant moves activation outliers into the weights offline and reports up to 1.56x speed and 2x memory (authors' "up to"). FP8 defines E4M3 and E5M2 (arXiv 2209.05433, Q23).
- **Why activations are harder:** a few channels have huge outliers (LLM.int8() handles them with 16-bit outlier decomposition); one outlier stretches a per-tensor scale (code below). NVIDIA's blog also notes weights are easier to quantize than activations (vendor blog).
- **Why not "bits halved, speed doubled":** Amdahl. Weights are only part of decode traffic; the KV cache, attention, norms and logits remain, and dequantisation costs work. Hardware support is by kernel and GPU generation (vLLM's quantization docs list a support table; check live docs).
- **Quality risk:** lower bits add error; INT4 needs calibration-aware methods (Q9) and validation (Q10). Details of INT8 code: Q40; KV quantization: Q22.

**Example:** run below. On my synthetic layer with one 20x outlier input channel, INT8 per-row has 3.05% relative output error and per-tensor 10.17%; plain INT4 round-to-nearest per-row is 42.29% (that is why real INT4 uses groups and GPTQ/AWQ-style methods). An INT8 per-tensor activation with one outlier at 60 gets a step of 0.472, so ordinary channels (std 1) see an error std of 0.1365. Time model (assumed A100-class, 7B, 1,000-token contexts): batch 1 decode fp16 7.26 ms vs W4 2.01 ms (3.61x, not 4x); batch 64 fp16 23.78 ms vs W4 18.53 ms (1.28x), because KV reads dominate. A 4,096-token prefill is 183.8 ms of compute vs 7.0 ms of weight reading, so weight-only bits barely matter there (dequantisation overhead not modelled).

**Code:** (synthetic weights; roofline numbers assumed)
```python
import numpy as np
rng = np.random.default_rng(0)
# (a) quantization error, synthetic weights: 256x256 gaussian, one outlier input channel x20 (assumed).
W = rng.normal(0, 0.02, (256, 256)); W[:, 7] *= 20
X = rng.normal(0, 1, (64, 256))
def q(W, bits, axis):                                 # symmetric round-to-nearest; axis=None per-tensor, 0 per-output-row
    qmax = 2**(bits-1) - 1
    s = (np.abs(W).max() if axis is None else np.abs(W).max(axis=1, keepdims=True)) / qmax
    return np.clip(np.round(W / s), -qmax-1, qmax) * s
for bits in (8, 4):
    for name, ax in (("per-tensor", None), ("per-row", 0)):
        Wq = q(W, bits, ax)
        print(f"INT{bits} {name:10s}: weight MSE={np.mean((W-Wq)**2):.2e}  output rel err={np.linalg.norm(X@W.T-X@Wq.T)/np.linalg.norm(X@W.T):.4f}")
# (b) activations: one token with an outlier channel, per-tensor INT8
x = rng.normal(0, 1, (1, 256)); x[0, 7] = 60.0
xq = q(x, 8, None)
print(f"INT8 activation per-tensor, outlier 60: rel err on x = {np.linalg.norm(x-xq)/np.linalg.norm(x):.4f}; non-outlier channels error std = {np.std(np.delete(x-xq,7)):.4f} (step = {60/127:.3f})")
# (c) why not 'bits halved, speed doubled': time model, ASSUMED A100-class, 7B, KV 0.5 MiB/token, ctx 1000
BW, PEAK = 2.0e12, 312e12
kv = 0.5 * 2**20 * 1000
def decode_ms(b, wbytes): return 1e3 * max(b * 2 * 7e9 / PEAK, (7e9 * wbytes + b * kv) / BW)
for b in (1, 16, 64):
    print(f"decode batch {b:2d}: fp16 {decode_ms(b,2):6.2f} ms, W8 {decode_ms(b,1):6.2f} ms ({decode_ms(b,2)/decode_ms(b,1):.2f}x), W4 {decode_ms(b,0.5):6.2f} ms ({decode_ms(b,2)/decode_ms(b,0.5):.2f}x)")
T = 4096; t_pref = 2 * 7e9 * T / PEAK
print(f"prefill {T} tokens: compute {t_pref*1e3:.1f} ms vs weight read {7e9*2/BW*1e3:.1f} ms -> weight-only bits barely change it (dequant not modelled)")
```
**Output (my run):**
```
INT8 per-tensor: weight MSE=8.22e-06  output rel err=0.1017
INT8 per-row   : weight MSE=7.42e-07  output rel err=0.0305
INT4 per-tensor: weight MSE=4.09e-04  output rel err=0.7123
INT4 per-row   : weight MSE=1.47e-04  output rel err=0.4229
INT8 activation per-tensor, outlier 60: rel err on x = 0.0352; non-outlier channels error std = 0.1365 (step = 0.472)
decode batch  1: fp16   7.26 ms, W8   3.76 ms (1.93x), W4   2.01 ms (3.61x)
decode batch 16: fp16  11.19 ms, W8   7.69 ms (1.45x), W4   5.94 ms (1.88x)
decode batch 64: fp16  23.78 ms, W8  20.28 ms (1.17x), W4  18.53 ms (1.28x)
prefill 4096 tokens: compute 183.8 ms vs weight read 7.0 ms -> weight-only bits barely change it (dequant not modelled)
```

**Follow-ups:**
- *Which phase does W4A16 speed up?* Decode, at small and moderate batch.
- *Why does the benefit shrink with batch?* The weight read is amortised and KV reads grow (Q7).
- *Do all GPUs support FP8?* Native support is by generation (Q23); check the engine's table.

**Common mistakes:** promising 4x from INT4; ignoring KV cache and long contexts; quoting paper speedups as general (they are the authors' results in their setups); calling INT4 lossless without evals.


### Q9 ⭐⭐⭐ 🟡 GPTQ vs AWQ vs bitsandbytes (LLM.int8 and NF4): how does each work, what hardware and kernels support them, and how would you choose for serving vs for QLoRA-style fine-tuning? (Part 4 Q6 covers NF4 for training.)
**Asked at:** all types; GenAI startups, inference-platform teams; interview-prep guide, not a candidate report lists GPTQ and AWQ
**Say this first (1 line):** GPTQ and AWQ are post-training weight-only methods that use calibration data (GPTQ with second-order error compensation, AWQ by protecting salient channels), while bitsandbytes is easy load-time quantization (LLM.int8() and NF4); I would serve with AWQ/GPTQ or FP8 where my engine has fast kernels, and use NF4 with QLoRA for fine-tuning (Part 4 Q6).

**Then explain:**
- **GPTQ (arXiv 2210.17323 abstract):** one-shot, layer-wise, uses approximate second-order information; quantizes weights column by column and corrects the remaining ones for the error. The authors report a 175B model in about 4 GPU hours at 3-4 bits and inference speedups of about 3.25x on A100 and 4.5x on A6000 (authors' claims, their setups).
- **AWQ (arXiv 2306.00978 abstract):** weight-only; observes that about 1% of channels, chosen by activation magnitude, are salient, and scales them to protect them; no backpropagation. The authors report TinyChat over 3x vs HF FP16 on desktop and mobile GPUs (authors' claim).
- **bitsandbytes:** LLM.int8() (vector-wise quantization plus 16-bit outlier decomposition; memory roughly halved) and NF4 (quantile-based 4-bit, Part 4 Q6). No calibration step; convenient. I recall it is often not the fastest serving path, check your engine.
- **Hardware/kernels:** in the vLLM quantization docs I read on 2026-10-24, AWQ was listed for Turing to Hopper, GPTQ for Volta to Hopper, and Marlin kernels for Ampere and newer (tables change by release, check live docs).
- **Choosing:** serving, throughput matters: AWQ/GPTQ (or FP8 on supported GPUs, Q23) with a kernel your engine supports; fine-tuning on a small GPU: NF4 + QLoRA; quick experiments: bitsandbytes. Calibration data should look like production; then validate (Q10).

**Example:** run below on one synthetic layer (out 64, in 128, four high-magnitude input channels, 4-bit signed): round-to-nearest relative output error 0.1141; AWQ-style scaling (scale exponent 0.3, chosen on calibration data) 0.0935; GPTQ-style error feedback 0.0815. On gaussian weights with block-64 scales, a quantile 4-bit grid (my simplified NF4-like grid, not the exact bitsandbytes table) has MSE 0.00844 vs 0.01153 for uniform INT4.

**Code:** (toy re-implementations; one seed, one layer, so the ordering is suggestive only and not a ranking of the real libraries)
```python
import numpy as np
rng = np.random.default_rng(0)
# Toy linear layer y = x W^T, out=64, in=128. Calibration inputs X: correlated, with 4 "salient" high-magnitude channels (assumed).
out_f, in_f, n = 64, 128, 1024
mix = rng.normal(0, 1, (in_f, in_f)) * 0.15 + np.eye(in_f)
X = rng.normal(0, 1, (n, in_f)) @ mix
sal = [3, 40, 77, 101]; X[:, sal] *= 8
W = rng.normal(0, 0.05, (out_f, in_f))
Xte = rng.normal(0, 1, (n, in_f)) @ mix; Xte[:, sal] *= 8          # held-out inputs, same distribution
ref = Xte @ W.T
def err(Wq): return np.linalg.norm(Xte @ Wq.T - ref) / np.linalg.norm(ref)
QMAX = 7                                                            # signed INT4: -8..7
def rtn(W, scale=None):
    s = np.abs(W).max(axis=1, keepdims=True) / QMAX if scale is None else scale
    return np.clip(np.round(W / s), -8, QMAX) * s
# --- RTN baseline
print(f"RTN INT4 per-row           : rel output err {err(rtn(W)):.4f}")
# --- AWQ-style: scale salient input channels up before quantizing, fold 1/s into the activation (here: back into W after dequant)
act = np.abs(X).mean(axis=0)
best = None
for a in np.linspace(0, 1, 11):
    s = act**a; s = s / np.sqrt(s.max() * s.min())
    Wq = rtn(W * s) / s                                             # quantize W*s, undo with 1/s (equivalent to X/s)
    e = np.linalg.norm(X @ Wq.T - X @ W.T) / np.linalg.norm(X @ W.T)   # alpha chosen on CALIBRATION data
    if best is None or e < best[0]: best = (e, a, Wq)
print(f"AWQ-style (alpha={best[1]:.1f})     : rel output err {err(best[2]):.4f}  (alpha picked on calibration data)")
# --- GPTQ-style: sequential column quantization with Hessian-based error compensation
H = X.T @ X / n + 1e-2 * np.eye(in_f) * np.mean(np.diag(X.T @ X / n))
U = np.linalg.cholesky(np.linalg.inv(H)).T                          # upper Cholesky factor of H^-1
Wg = W.copy(); scale = np.abs(W).max(axis=1, keepdims=True) / QMAX
Wq = np.zeros_like(W)
for i in range(in_f):
    q = np.clip(np.round(Wg[:, i:i+1] / scale), -8, QMAX) * scale
    Wq[:, i:i+1] = q
    e = (Wg[:, i:i+1] - q) / U[i, i]
    Wg[:, i:] -= e @ U[i:i+1, i:]                                   # push the error onto not-yet-quantized columns
print(f"GPTQ-style (error feedback): rel output err {err(Wq):.4f}")
# --- NF4 vs uniform INT4 levels on gaussian weights (block of 64 per scale), as in QLoRA-style storage
from statistics import NormalDist
nd = NormalDist(); ps = (np.arange(16) + 0.5) / 16
lv = np.array([nd.inv_cdf(p) for p in ps]); lv = lv / np.abs(lv).max()     # quantile levels (simplified NF4-like, NOT the exact bnb table)
w = rng.normal(0, 1, 64 * 2000).reshape(-1, 64); s = np.abs(w).max(axis=1, keepdims=True)
nf = lv[np.abs(w[..., None] / s[..., None] - lv).argmin(-1)] * s
un = np.clip(np.round(w / s * 7), -8, 7) / 7 * s
print(f"gaussian weights, block-64: MSE uniform-INT4 {np.mean((w-un)**2):.5f} vs quantile-4bit {np.mean((w-nf)**2):.5f}")
```
**Output (my run):**
```
RTN INT4 per-row           : rel output err 0.1141
AWQ-style (alpha=0.3)     : rel output err 0.0935  (alpha picked on calibration data)
GPTQ-style (error feedback): rel output err 0.0815
gaussian weights, block-64: MSE uniform-INT4 0.01153 vs quantile-4bit 0.00844
```

**Follow-ups:**
- *Why does GPTQ need a Hessian?* It tells which weight errors matter for the layer's outputs on the calibration inputs.
- *What if calibration data is off-distribution?* The scales and compensations fit the wrong inputs; quality can drop on your real traffic.
- *Is group size important?* Smaller groups track weight ranges better at a small size cost (from memory, check the method docs).

**Common mistakes:** treating the three as the same thing; ignoring kernel/hardware support (a quantized checkpoint without a fast kernel can be slower); calibrating on irrelevant text; assuming NF4 is a serving format; quoting the papers' speedups as universal.


### Q10 ⭐⭐⭐ 🟡 How do you validate a quantized model before shipping (task evals, long-context and retrieval checks, calibration data choice, latency re-measurement, rollback plan), and what silently degrades?
**Asked at:** product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report
**Say this first (1 line):** I compare the quantized model with the full-precision model on the same prompts, paired, overall and per slice (long context, retrieval, code, languages, structured output), re-measure latency on the target hardware, ship behind a canary with a rollback threshold, because the average can hide a large drop in one slice.

**Then explain:**
- **Task evals, paired:** run both models on the same golden set (Part 9 Q2) and analyse the difference per item with a paired bootstrap or exact sign test (Part 9 Q28, Q38), with the set size in mind (Part 9 Q26). Regression gates are Part 9 Q14.
- **Slices:** one prep guide (PracHub, a scenario, not a candidate report) describes a quantized model failing long-context retrieval; quantization error can show up in long contexts and in rare languages (from memory, check), code, math, tool-call formatting and refusals. Include these slices explicitly.
- **Calibration data:** should resemble production inputs; calibrating on the wrong text is a silent failure.
- **Performance:** re-measure TTFT, TPOT and throughput with the real kernels on the real GPU (Q30); a smaller checkpoint without a good kernel may not be faster.
- **Rollout:** shadow or canary with pre-agreed thresholds and a one-command rollback to the previous precision (Q46).
- **What silently degrades:** long-context recall, calibration mismatch, structured-output validity, safety behaviour, low-resource languages, and sampling-sensitive tasks.

**Example:** synthetic eval (400 short items, 60 long-context items). I wrote in the degradation myself: assumed true accuracy 0.85 to 0.84 on short, 0.80 to 0.66 on long. Measured: short 0.860 to 0.853 (diff -0.007, paired bootstrap 95% CI [-0.018, +0.000], 3 items lost, 0 gained, exact p = 0.250); long-context 0.817 to 0.633 (diff -0.183, CI [-0.283, -0.100], 11 lost, 0 gained, p = 0.001); overall -0.030 (CI [-0.046, -0.015]). A hypothetical gate of overall >= -1 pt and every slice >= -3 pt blocks the ship. The n = 60 slice is small, so its CI is wide; I would add more long-context items before trusting the size of the drop. This only shows the method detects a planted effect.

**Code:** (mock paired outcomes; exact sign test verified against brute-force enumeration inside the script)
```python
import numpy as np, math, itertools
rng = np.random.default_rng(3)
# Synthetic eval: 400 short-task items + 60 long-context items. Quantization only flips correct -> wrong here (a simplification).
# ASSUMED true accuracies: FP16 0.85 / 0.80 ; quantized 0.84 / 0.66 (long context degrades more).
def paired(n, p_fp, p_q):
    fp = rng.random(n) < p_fp
    keep = rng.random(n) < min(1, p_q / p_fp)              # a correct item stays correct w.p. p_q/p_fp
    q = fp & keep
    extra = ~fp & (rng.random(n) < max(0, (p_q - p_fp * min(1, p_q / p_fp)) / (1 - p_fp)))
    return fp, q | extra
fp_s, q_s = paired(400, 0.85, 0.84)
fp_l, q_l = paired(60, 0.80, 0.66)
def exact_sign_p(b, c):                                    # two-sided exact McNemar on discordant counts
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n)
def brute_sign_p(b, c):                                    # enumerate all 2^n sign patterns
    n = b + c; k = min(b, c); cnt = 0
    for pat in itertools.product((0, 1), repeat=n):
        s = sum(pat)
        if s <= k or n - s <= k: cnt += 1
    return cnt / 2**n
assert abs(exact_sign_p(2, 9) - brute_sign_p(2, 9)) < 1e-12 and abs(exact_sign_p(5, 5) - brute_sign_p(5, 5)) < 1e-12
def report(name, fp, q):
    b = int((fp & ~q).sum()); c = int((~fp & q).sum())
    d = (q.astype(float) - fp.astype(float))
    boots = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(4000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    print(f"{name:11s} n={len(fp):3d} fp={fp.mean():.3f} q={q.mean():.3f} diff={d.mean():+.3f}  95% paired-boot CI [{lo:+.3f},{hi:+.3f}]  lost={b} gained={c} exact p={exact_sign_p(b,c):.3f}")
report("short", fp_s, q_s)
report("long-ctx", fp_l, q_l)
report("overall", np.r_[fp_s, fp_l], np.r_[q_s, q_l])
print("sign-test code checked against brute-force enumeration (n=11, n=10): OK")
GATE_SLICE, GATE_ALL = -0.03, -0.01                          # hypothetical ship gates
print("gate: overall >= -1pt and every slice >= -3pt ->", "SHIP" if (np.r_[q_s,q_l].mean()-np.r_[fp_s,fp_l].mean() >= GATE_ALL and (q_l.mean()-fp_l.mean()) >= GATE_SLICE) else "BLOCK (long-context slice fails)")
```
**Output (my run):**
```
short       n=400 fp=0.860 q=0.853 diff=-0.007  95% paired-boot CI [-0.018,+0.000]  lost=3 gained=0 exact p=0.250
long-ctx    n= 60 fp=0.817 q=0.633 diff=-0.183  95% paired-boot CI [-0.283,-0.100]  lost=11 gained=0 exact p=0.001
overall     n=460 fp=0.854 q=0.824 diff=-0.030  95% paired-boot CI [-0.046,-0.015]  lost=14 gained=0 exact p=0.000
sign-test code checked against brute-force enumeration (n=11, n=10): OK
gate: overall >= -1pt and every slice >= -3pt -> BLOCK (long-context slice fails)
```

**Follow-ups:**
- *Is a 1-point average drop acceptable?* Depends on the product and on which slice; set it per slice before testing.
- *Do you need a judge model?* For open-ended outputs, yes, calibrated against humans (Part 9 Q6); for exact-match tasks, no.
- *How do you roll back?* Keep the previous precision's deployment warm during the canary.

**Common mistakes:** one average benchmark score; unpaired comparisons that waste statistical power; no long-context slice; calibrating on generic text; skipping the latency re-measurement; no rollback plan.


### Q11 ⭐⭐⭐ 🟡 Speculative decoding: how does a draft model propose and the target verify, why is the output distribution unchanged, how does acceptance rate set the speedup, and when does it not help?
**Asked at:** all types; inference-platform teams, AI labs; interview-prep guide, not a candidate report lists it with its limits
**Say this first (1 line):** A cheap draft model proposes several tokens, the target model scores them all in one forward pass, and a rejection rule accepts a prefix and resamples at the first miss so the output distribution is exactly the target's; the speedup comes from the acceptance rate and draft cost, and it can be a slowdown.

**Then explain:**
- **Procedure:** draft samples `gamma` tokens from `q`; target computes `p` at every position in one pass; accept token x with probability `min(1, p(x)/q(x))`; on the first rejection sample from the normalised `max(p - q, 0)`; if all are accepted, take one extra token from the target. This is the modified rejection sampling of Leviathan et al. (arXiv 2211.17192) and Chen et al. (arXiv 2302.01318).
- **Why the distribution is unchanged:** for token x the chance of emitting it is `min(p,q)(x)` plus the rejected mass times `max(p-q,0)(x)/sum(...)`, which equals `p(x)`. The code checks this empirically.
- **Acceptance rate:** `alpha = sum_x min(p(x), q(x))`. With i.i.d. acceptance, expected tokens per round are `(1 - alpha^(gamma+1)) / (1 - alpha)`; cost per round is `gamma x c + 1` target-pass units, with `c` the draft/target cost ratio. Derivation is Q42; simulation Q41; variants Q24.
- **Authors' reported results (their setups):** 2-3x on T5-XXL (Leviathan), 2-2.5x on Chinchilla 70B in a distributed setup (Chen).
- **When it does not help:** low acceptance, a draft that is not cheap enough, or a server already running large batches where the verification pass is no longer free (an explainer, system-design.space, notes that low acceptance can cancel the gain; the batch-size caveat is from memory, check).

**Example:** run below with a 6-token vocabulary, synthetic `p` and `q`. Closed-form acceptance 0.8500, simulated 0.8497. Output frequencies match the target (max difference 0.0004 over 200,000 draws, noise about 0.0011). Expected tokens per round at alpha = 0.7, gamma = 4: formula 2.773, simulated 2.770. Speedup at c = 0.05: alpha 0.7 gives 2.31x at gamma 4; alpha 0.5 gives 1.61x at gamma 4 and falls to 1.43x at gamma 8 (drafting too far wastes work). With an expensive draft (c = 0.3) at gamma 4, alpha 0.5 gives 0.88x, a slowdown.

**Code:** (toy distributions; i.i.d. acceptance assumed in the speedup table)
```python
import numpy as np
rng = np.random.default_rng(0)
V = 6
p = np.array([0.40, 0.25, 0.15, 0.10, 0.07, 0.03])        # target distribution (synthetic)
q = np.array([0.30, 0.30, 0.20, 0.05, 0.10, 0.05])        # draft distribution (synthetic)
alpha = np.minimum(p, q).sum()                              # closed-form acceptance prob for one token
resid = np.maximum(p - q, 0); resid /= resid.sum()          # resample distribution on rejection
def one_token():
    x = rng.choice(V, p=q)                                  # draft proposes
    if rng.random() < min(1, p[x] / q[x]): return x, True   # accept w.p. min(1, p/q)
    return rng.choice(V, p=resid), False                    # else sample from (p-q)+ normalised
N = 200000; out = np.zeros(V); acc = 0
for _ in range(N):
    t, a = one_token(); out[t] += 1; acc += a
print("target p       :", p)
print("empirical out  :", np.round(out / N, 4))
print(f"max |diff| = {np.abs(out/N - p).max():.4f} (sampling noise ~ {np.sqrt(0.25/N):.4f})")
print(f"acceptance: simulated {acc/N:.4f} vs closed form sum(min(p,q)) = {alpha:.4f}")
# Speedup: expected tokens per target pass with gamma drafts, i.i.d. acceptance alpha: (1-alpha^(g+1))/(1-alpha).
# Cost per round = gamma*c + 1 target-pass units, c = draft cost / target cost (assumed).
def speedup(a, g, c): return (1 - a**(g + 1)) / (1 - a) / (g * c + 1)
def sim_tokens(a, g, rounds=200000):
    tot = 0
    for _ in range(rounds):
        k = 0
        while k < g and rng.random() < a: k += 1
        tot += k + 1                                        # accepted drafts + 1 token from the target
    return tot / rounds
print(f"expected tokens/round alpha=0.7 gamma=4: formula {(1-0.7**5)/0.3:.3f}, simulated {sim_tokens(0.7,4):.3f}")
print("speedup = tokens/round / (gamma*c+1)")
for a in (0.5, 0.7, 0.9):
    print(f"alpha={a}: " + "  ".join(f"g={g},c=0.05:{speedup(a,g,0.05):.2f}x" for g in (2, 4, 8)) + f"  | g=4,c=0.3:{speedup(a,4,0.3):.2f}x")
```
**Output (my run):**
```
target p       : [0.4  0.25 0.15 0.1  0.07 0.03]
empirical out  : [0.4    0.25   0.1496 0.1004 0.07   0.0299]
max |diff| = 0.0004 (sampling noise ~ 0.0011)
acceptance: simulated 0.8497 vs closed form sum(min(p,q)) = 0.8500
expected tokens/round alpha=0.7 gamma=4: formula 2.773, simulated 2.770
speedup = tokens/round / (gamma*c+1)
alpha=0.5: g=2,c=0.05:1.59x  g=4,c=0.05:1.61x  g=8,c=0.05:1.43x  | g=4,c=0.3:0.88x
alpha=0.7: g=2,c=0.05:1.99x  g=4,c=0.05:2.31x  g=8,c=0.05:2.28x  | g=4,c=0.3:1.26x
alpha=0.9: g=2,c=0.05:2.46x  g=4,c=0.05:3.41x  g=8,c=0.05:4.38x  | g=4,c=0.3:1.86x
```

**Follow-ups:**
- *Is greedy decoding special?* Acceptance becomes "does the draft's argmax equal the target's argmax".
- *Where does the draft come from?* A small model of the same family, n-gram lookup, or trained heads (Medusa, EAGLE; Q24).
- *Does it save compute?* No; it spends extra compute to save latency, so check the cost at load.

**Common mistakes:** saying it is approximate or changes outputs; quoting 2-3x as universal; ignoring draft cost; assuming it helps at high batch; forgetting the bonus token and the resample step.


### Q12 ⭐⭐⭐ 🟡 Choose a serving stack: compare vLLM, TGI, TensorRT-LLM, SGLang and llama.cpp/Ollama (hardware, features, ops effort, maturity), and say how you decide for a given workload.
**Asked at:** all types; product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report lists these frameworks
**Say this first (1 line):** I filter on hardware and required features first, then benchmark the survivors on my own workload; vLLM and SGLang are the usual general-purpose open choices on GPUs, TensorRT-LLM if I am NVIDIA-only and will pay build effort for vendor kernels, llama.cpp for CPU, Apple and edge, and TGI only if I already run it (its docs banner says maintenance mode).

**Then explain:**
- **vLLM (docs read 2026-10-24):** prefix caching, chunked prefill (on by default in V1 per the tuning docs), multi-LoRA, structured outputs (xgrammar, guidance), a broad quantization list, disaggregated prefilling.
- **SGLang (paper arXiv 2312.07104):** RadixAttention KV reuse and compressed finite-state machines for structured output; the authors report up to 6.4x throughput (their benchmarks, their setup).
- **TensorRT-LLM (NVIDIA docs):** in-flight batching, paged KV cache, FP8 on H100+, speculative decoding, LoRA, chunked prefill, guided decoding; NVIDIA GPUs only, vendor-optimised.
- **TGI (HF docs):** continuous batching, Flash and Paged Attention, tensor parallel, SSE streaming, bitsandbytes and GPTQ; the banner says maintenance mode and points to vLLM, SGLang, llama.cpp and MLX. TGI v3's 13x vs vLLM on 200k-token prompts is a vendor-reported number on one benchmark; do not generalise it.
- **llama.cpp / Ollama:** C/C++ with GGUF, 1.5-8 bit quantization, CPU+GPU hybrid, many backends, OpenAI-compatible server; for local, edge and single-user use (Q36).
- **How I decide:** (1) hardware, (2) must-have features (LoRA, structured output, prefix reuse, your quant format), (3) team and ops effort, (4) project health, (5) an open-loop benchmark on my traffic (Q30). I quote no cross-engine speed numbers because I did not verify any.

**Example:** a product company with NVIDIA GPUs, many users and heavy shared system prompts: shortlist vLLM, SGLang, TensorRT-LLM and benchmark them with prefix caching on and a realistic prompt mix. A laptop assistant on Apple Silicon: llama.cpp (or Ollama on top). An existing TGI deployment that works: keep it, and plan a migration path rather than a rewrite.

**Code:** (a hard-constraint filter built from the sources above; it does not rank engines)
```python
# A hard-constraint filter, NOT a ranking and NOT a benchmark. Entries encode what the sources note says
# (docs read 2026-10-24; check live docs). Which survivor wins is decided by YOUR benchmark (Q30).
STACKS = {
    "vLLM":         {"hw": {"nvidia", "amd", "other_gpu"}, "note": "general-purpose engine; prefix caching, chunked prefill, multi-LoRA, structured output in docs"},
    "SGLang":       {"hw": {"nvidia", "amd"},               "note": "RadixAttention prefix reuse and structured-output focus (paper)"},
    "TensorRT-LLM": {"hw": {"nvidia"},                      "note": "NVIDIA-only; vendor-optimised kernels, FP8 on H100+; more build/ops steps"},
    "TGI":          {"hw": {"nvidia", "amd", "other_gpu"}, "note": "docs banner says maintenance mode: avoid for new builds"},
    "llama.cpp":    {"hw": {"cpu", "apple", "nvidia", "amd", "other_gpu"}, "note": "GGUF, CPU+GPU hybrid, edge/local; not a multi-tenant GPU server by design"},
}
def filter_stacks(hw, need_many_users, allow_maintenance=False):
    keep, drop = [], []
    for n, f in STACKS.items():
        if hw not in f["hw"]: drop.append((n, f"{hw} not in my encoded list (verify live docs)"))
        elif n == "TGI" and not allow_maintenance: drop.append((n, "maintenance mode"))
        elif n == "llama.cpp" and need_many_users and hw in {"nvidia", "amd", "other_gpu"}: keep.append((n, "possible, but check batching throughput vs the GPU engines"))
        else: keep.append((n, "ok"))
    return keep, drop
for scen in [("nvidia", True), ("apple", False), ("cpu", False)]:
    k, d = filter_stacks(*scen)
    print(scen, "benchmark:", [n for n, _ in k], "| dropped:", d)
```
**Output (my run):**
```
('nvidia', True) benchmark: ['vLLM', 'SGLang', 'TensorRT-LLM', 'llama.cpp'] | dropped: [('TGI', 'maintenance mode')]
('apple', False) benchmark: ['llama.cpp'] | dropped: [('vLLM', 'apple not in my encoded list (verify live docs)'), ('SGLang', 'apple not in my encoded list (verify live docs)'), ('TensorRT-LLM', 'apple not in my encoded list (verify live docs)'), ('TGI', 'apple not in my encoded list (verify live docs)')]
('cpu', False) benchmark: ['llama.cpp'] | dropped: [('vLLM', 'cpu not in my encoded list (verify live docs)'), ('SGLang', 'cpu not in my encoded list (verify live docs)'), ('TensorRT-LLM', 'cpu not in my encoded list (verify live docs)'), ('TGI', 'cpu not in my encoded list (verify live docs)')]
```

**Follow-ups:**
- *Does vLLM support CPU or Apple hardware?* I did not verify that in the docs I read; the filter says "not in my encoded list". Check live docs.
- *Why not just pick the fastest on a leaderboard?* Results depend on model, prompt mix, hardware and version; run your own.
- *What about managed APIs?* That is the self-host vs API question (Q18).

**Common mistakes:** choosing by one vendor benchmark; ignoring maintenance status and hardware lock-in; comparing engines with a single repeated prompt (prefix cache inflates it); assuming a framework's feature list is current without reading its docs.

