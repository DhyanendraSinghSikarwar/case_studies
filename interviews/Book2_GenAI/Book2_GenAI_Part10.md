# Book 2 — Part 10: Deployment (vLLM, TGI, quantization, batching, speculative decoding, latency and cost)

**Topic:** serving LLMs in production: prefill vs decode, KV-cache memory and capacity planning, PagedAttention and the vLLM block manager, continuous batching, chunked prefill, prefix caching, latency metrics and SLOs, quantization (INT8, INT4, FP8, GPTQ, AWQ, bitsandbytes, KV-cache quantization), speculative decoding, parallelism, serving frameworks (vLLM, TGI, TensorRT-LLM, SGLang, llama.cpp), multi-LoRA, constrained decoding cost, streaming, autoscaling, cost per million tokens, benchmarking, long context, disaggregation, and design and diagnosis questions
**Target:** 45  |  **Actual:** 49 (⭐⭐⭐ 16, ⭐⭐ 21, ⭐ 12)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: earlier parts introduced these ideas and deferred depth to this part; answers here go deeper and cross-reference, not repeat. Part 1 covers the KV cache and its growth (Q6), prefill vs decode mechanism (Q7), MQA/GQA (Q10), FlashAttention (Q11), KV and parameter maths (Q15), KV-reduction levers (Q23), API prompt caching (Q24), long-context breakage (Q30), arithmetic intensity and batching (Q32), MLA (Q33), MoE serving trade-offs (Q34), a KV-cache decoding loop (Q35), FlashAttention's online softmax (Q43) and multi-token prediction (Q45). Part 2 covers token costs (Q5), training parallelism (Q34) and test-time compute (Q43). Part 3 covers constrained decoding at the logit level (Q22), prompt-level cost cuts (Q36) and slow grammar compilation (Q40). Part 4 covers NF4 and QLoRA (Q6), merging adapters (Q13), the fine-tuned-small-model break-even (Q25) and merged vs multi-LoRA serving (Q32). Part 6 covers the RAG latency budget (Q31) and cost estimate (Q32); Part 7 covers reranker serving (Q21); Part 8 covers agent cost and latency (Q37); Part 9 covers evaluation cost (Q33) and is where quantized-model quality checks get their eval method. Part 10 owns engine internals, serving-side capacity and cost maths, quantization for inference, speculative decoding, framework choice and production diagnosis. Book 4 owns generic MLOps, Docker and Kubernetes, so autoscaling and rollout questions here stay LLM-specific (signals, KV memory, cold starts); monitoring and tracing depth goes to Part 11. Engines, flags, supported hardware, framework status (TGI's docs now say maintenance mode) and benchmark numbers change quickly: answers must hedge current-state claims and tell the reader to check live docs. Headline numbers (vLLM 2-4x, Orca 36.9x, speculative 2-3x, Medusa and EAGLE speedups, DistServe 7.4x, Sarathi-Serve gains, GPTQ and AWQ speedups) are the authors' reported results in their stated setups and must be labelled as such. No GPU prices appear; cost questions use symbolic or clearly hypothetical numbers.

Evidence limits: no candidate-reported deployment questions were found (searches for Glassdoor, Blind and Reddit reports returned only job postings and prep guides); the "Asked at" tags are company types, and where an interview-prep guide describes a prompt this is marked as a guide, not a candidate report. The guides are commercial or institute pages that say their numbers are illustrative. Star ratings blend topic frequency across guides with judgement. See research_notes/Book2_Part10_sources.md for which pages were opened.

---

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

### Q13 ⭐⭐⭐ 🟡 Cost per million tokens: derive it from GPU price per hour, throughput and utilisation, separate input from output tokens, and explain why low utilisation is the usual reason self-hosting loses.
**Asked at:** product companies, GCCs, GenAI startups; interview-prep guide, not a candidate report includes cost-per-million-token maths
**Say this first (1 line):** Cost per million tokens is GPU price per hour divided by the tokens the GPU actually serves per hour, so it falls as throughput rises and balloons as utilisation falls; self-hosting usually loses because the GPU is paid for while idle.

**Then explain:**
- **The formula:** cost per M tokens = (price per GPU-hour) / (tokens per second x 3600 x utilisation) x 1,000,000. Utilisation here means the fraction of paid time the GPU is doing useful, SLO-meeting work, not the nvidia-smi number (see Q33).
- **Input and output are different jobs.** Prefill processes the whole prompt in parallel and is compute-bound, so input tokens are served much faster per GPU-second than output tokens, which are generated one step at a time and are memory-bound (Part 1 Q7). So compute the two rates separately and add GPU-seconds per request: in / prefill rate + out / decode rate. Providers commonly price output above input for this reason (check each provider's page).
- **Use the throughput you can hold under your SLO**, not the peak from a benchmark with giant batches. Throughput at the batch size where TPOT still meets the SLO is the honest denominator (Q7).
- **Why self-hosting loses:** you pay per hour, an API charges per token. If traffic is spiky or small, the GPU sits idle and every served token carries the idle cost. At 25% utilisation the cost is 4x the full-utilisation cost, by construction. You also pay for a redundancy floor (at least two replicas for an always-on service) and for the engineers.
- **What to do about it:** raise utilisation (batch offline work into the troughs, share one fleet across products, autoscale on queue depth, see Q27), cut GPU-seconds per request (prefix caching Q14, quantization Q8), or buy tokens instead (Q18).

**Example:** every number is hypothetical: 1 unit = one GPU-hour, assumed 20,000 input tokens/s and 2,000 output tokens/s when busy. One request with 1,000 input and 200 output tokens needs 0.05 s + 0.10 s = 0.15 GPU-seconds, so output is 67% of the busy time even though it is only 17% of the tokens. At 100% utilisation that is 4.17e-5 units per request; at 25% it is 1.67e-4. Against a hypothetical API price of 0.10 units per million blended tokens, self-hosting at full utilisation costs 0.035, so it wins only above about 35% utilisation.

**Code:** (all inputs hypothetical, symbolic units; the formula is checked against a brute-force loop)
```python
# Cost per million tokens from GPU price, throughput and utilisation.
# ALL numbers are HYPOTHETICAL: GPU price is 1.0 "unit" per hour (symbolic), throughputs are assumed.
GPU_UNIT_PER_HOUR = 1.0          # symbolic price: 1 unit = one GPU-hour
PREFILL_TPS = 20000.0            # assumed: input tokens/s the GPU can prefill when busy
DECODE_TPS = 2000.0              # assumed: output tokens/s aggregate across the batch when busy

def cost_per_million(tps, util, price=GPU_UNIT_PER_HOUR):
    # price per hour / (tokens per hour actually served)
    return price / (tps * 3600 * util) * 1e6

print("util  cost/M output tokens (units)   cost/M input tokens (units)")
for u in (1.0, 0.5, 0.25, 0.10):
    print(f"{u:4.2f}  {cost_per_million(DECODE_TPS, u):10.4f}                    {cost_per_million(PREFILL_TPS, u):10.4f}")

# Per-request cost with one input/output mix: GPU-seconds = in/prefill_tps + out/decode_tps
def per_request(n_in, n_out, util):
    busy_s = n_in / PREFILL_TPS + n_out / DECODE_TPS
    return GPU_UNIT_PER_HOUR / 3600 * busy_s / util, busy_s

n_in, n_out = 1000, 200
c, busy = per_request(n_in, n_out, 1.0)
print(f"\nrequest {n_in} in / {n_out} out: busy {busy:.3f} GPU-s, "
      f"decode share of busy time {n_out/DECODE_TPS/busy:.0%}")

# Brute-force check: serve 10,000 identical requests, wall time = busy / util
for u in (1.0, 0.25):
    N = 10000
    busy_total = sum(n_in / PREFILL_TPS + n_out / DECODE_TPS for _ in range(N))
    wall_h = busy_total / u / 3600
    brute = GPU_UNIT_PER_HOUR * wall_h / N
    formula = per_request(n_in, n_out, u)[0]
    assert abs(brute - formula) < 1e-12
    print(f"util {u:.2f}: cost per request {formula:.3e} units (brute force matches)")

# Blended cost per million total tokens, and break-even utilisation vs a hypothetical API price
blend = lambda u: per_request(n_in, n_out, u)[0] / (n_in + n_out) * 1e6
API_BLENDED = 0.10               # hypothetical API price, units per million blended tokens
print(f"\nself-host blended cost/M tokens at util 1.00: {blend(1.0):.3f} units")
u_star = blend(1.0) / API_BLENDED
print(f"hypothetical API price {API_BLENDED} units/M -> self-host wins only if util > {u_star:.2f}")
for u in (0.9, 0.5, 0.25, 0.1):
    print(f"  util {u:.2f}: self {blend(u):.3f} vs API {API_BLENDED} -> {'self' if blend(u) < API_BLENDED else 'API'} cheaper")
```

**Output (my run):**
```
util  cost/M output tokens (units)   cost/M input tokens (units)
1.00      0.1389                        0.0139
0.50      0.2778                        0.0278
0.25      0.5556                        0.0556
0.10      1.3889                        0.1389

request 1000 in / 200 out: busy 0.150 GPU-s, decode share of busy time 67%
util 1.00: cost per request 4.167e-05 units (brute force matches)
util 0.25: cost per request 1.667e-04 units (brute force matches)

self-host blended cost/M tokens at util 1.00: 0.035 units
hypothetical API price 0.1 units/M -> self-host wins only if util > 0.35
  util 0.90: self 0.039 vs API 0.1 -> self cheaper
  util 0.50: self 0.069 vs API 0.1 -> self cheaper
  util 0.25: self 0.139 vs API 0.1 -> API cheaper
  util 0.10: self 0.347 vs API 0.1 -> API cheaper
```

**Follow-ups:**
- *Why is output more expensive than input?* Decode reads all weights (and the KV cache) for each step and is memory-bound, so each output token uses more GPU time than an input token.
- *What does 50% utilisation mean in practice?* Half the paid hours produce no SLO-meeting tokens. The fix is a traffic shape or fleet-sharing fix, not a faster kernel.
- *How do you handle a request mix that changes?* Track GPU-seconds per request by bucket of (input, output) length and recompute; the mix, not the average, sets the cost.

**Common mistakes:** dividing price by benchmark peak throughput; using one blended rate for input and output; counting only GPU rent and forgetting the redundancy floor and on-call; quoting a dollar figure from memory instead of showing the formula and the assumptions.

### Q14 ⭐⭐⭐ 🟡 Prefix caching inside an engine (vLLM-style block hashing, LRU eviction) vs a provider's prompt caching: how does each work, what does it save (prefill, not decode), and how do you structure prompts and routing to get hits? (Part 1 Q24 covers API prompt caching.)
**Asked at:** product companies, inference-platform teams; interview-prep guide, not a candidate report
**Say this first (1 line):** Both reuse the KV cache of an identical prompt prefix so the model skips prefill for it; they save prefill compute and time to first token, not decode, and you only get hits if the shared text comes first and is byte-identical.

**Then explain:**
- **Engine-side (vLLM-style) automatic prefix caching.** Per the vLLM design docs read on 2026-10-24 (check live docs): only full blocks are cached; each block's hash covers the parent block's hash, the block's tokens, and extras such as a LoRA id; blocks are reference-counted and unused cached blocks are evicted LRU. Because the hash is chained, a change at token 5 changes every later block's hash, so nothing after it can match. The docs also describe a cache salt so tenants do not share cache, and the hash function default has changed across versions, so check what your version uses.
- **Provider prompt caching** is the same idea behind an API: the provider keeps KV state for a prefix and bills or processes it differently. Minimum prefix length, lifetime, explicit markers and discounts differ by provider, so read their docs (Part 1 Q24 has the API view).
- **What it saves:** prefill FLOPs and TTFT for the cached part. Decode is untouched: every output token still needs a forward pass that reads the whole KV cache. So the win is large for long shared prompts with short outputs (RAG with a fixed instruction block, agents with long tool schemas) and small for short prompts with long outputs.
- **Prompt structure:** stable content first (system prompt, tool definitions, few-shot examples, documents), variable content last (user turn); no timestamps, request ids or reordered JSON keys near the top; deterministic serialisation of the prefix.
- **Routing:** the cache lives in one replica's GPU memory, so a hit needs the request to land on a replica that has the prefix: sticky routing by tenant or prefix hash, or a cache-aware router (Q37). The cost is hot spots.

**Example:** a toy engine with 4-token blocks and a 12-token shared system prompt (3 full blocks), 20 requests of 18 tokens. Shared prefix first: 228 of 360 prompt tokens skipped (63%, the first request is a cold miss). Same text but a per-request value placed first: 0 hits. Shared text placed after the user text: 0 hits. The 18-token prompt repeated exactly gets 16 hits: the 2-token tail is a partial block and is never cached.

**Code:** (toy block-hash cache with LRU; synthetic token ids)
```python
# Toy engine prefix cache: block hashing (chained) + LRU, full blocks only. Token ids are synthetic.
from collections import OrderedDict
BLOCK = 4   # toy block size (real engines commonly use 16; check live docs)

class PrefixCache:
    def __init__(self, capacity_blocks):
        self.cap, self.lru = capacity_blocks, OrderedDict()
        self.hit_tokens = self.total_tokens = 0
    def prefill(self, tokens):
        """Return number of prompt tokens served from cache; cache every full block."""
        parent, hits, missed = 0, 0, False
        full = len(tokens) // BLOCK * BLOCK          # a partial last block is never cached
        for i in range(0, full, BLOCK):
            h = hash((parent, tuple(tokens[i:i + BLOCK])))   # chained: depends on ALL earlier tokens
            if h in self.lru and not missed:
                hits += BLOCK; self.lru.move_to_end(h)
            else:
                missed = True                         # after the first miss the rest cannot match
                self.lru[h] = True; self.lru.move_to_end(h)
                while len(self.lru) > self.cap:
                    self.lru.popitem(last=False)      # evict least recently used
            parent = h
        self.hit_tokens += hits; self.total_tokens += len(tokens)
        return hits

SYS = list(range(100, 112))                           # 12-token shared system prompt
def req(i, sys_first=True, ts=False):
    user = [1000 + i * 7 + j for j in range(6)]       # unique per request
    stamp = [9000 + i] if ts else []                  # per-request value (like a timestamp)
    return (stamp + SYS + user) if sys_first else (user + SYS)

for name, mk in [("shared prefix first        ", lambda i: req(i)),
                 ("timestamp before the prefix", lambda i: req(i, ts=True)),
                 ("shared text AFTER user text", lambda i: req(i, sys_first=False))]:
    c = PrefixCache(64)
    for i in range(20): c.prefill(mk(i))
    print(f"{name}: prefill tokens saved {c.hit_tokens}/{c.total_tokens} = {c.hit_tokens/c.total_tokens:.0%}")

# Block-boundary effect: first request is 18 tokens -> 4 full blocks cached (16 tokens), tail 2 never cached
c = PrefixCache(64); a = req(0); c.prefill(a)
print("repeat the exact same 18-token prompt: hit tokens =", c.prefill(a), "of", len(a))

# LRU eviction: tiny cache, two alternating tenants with different system prompts
def run(cap):
    c = PrefixCache(cap)
    for i in range(30):
        base = 100 if i % 2 == 0 else 500
        c.prefill(list(range(base, base + 12)) + [2000 + i])
    return c.hit_tokens / c.total_tokens
print("alternating 2 prompts, capacity 3 blocks :", f"{run(3):.0%}", "(thrashes)")
print("alternating 2 prompts, capacity 6 blocks :", f"{run(6):.0%}")

# Routing: 2 replicas, 3 tenants (own 12-token system prompt), 60 requests; tenant 0 sends 3x the traffic
def routing(policy):
    reps = [PrefixCache(64), PrefixCache(64)]
    load = [0, 0]
    tenants = [0, 0, 0, 1, 2] * 12                    # skewed: tenant 0 is 60% of traffic
    for i, t in enumerate(tenants):
        prompt = list(range(300 + t * 50, 312 + t * 50)) + [7000 + i] * 2
        k = i % 2 if policy == "round-robin" else t % 2
        load[k] += 1
        reps[k].prefill(prompt)
    h = sum(r.hit_tokens for r in reps); n = sum(r.total_tokens for r in reps)
    return h / n, load
for p in ("round-robin", "sticky"):
    hr, load = routing(p)
    print(f"{p:12s}: hit rate {hr:.0%}, requests per replica {load}")
```

**Output (my run):**
```
shared prefix first        : prefill tokens saved 228/360 = 63%
timestamp before the prefix: prefill tokens saved 0/380 = 0%
shared text AFTER user text: prefill tokens saved 0/360 = 0%
repeat the exact same 18-token prompt: hit tokens = 16 of 18
alternating 2 prompts, capacity 3 blocks : 0% (thrashes)
alternating 2 prompts, capacity 6 blocks : 86%
round-robin : hit rate 77%, requests per replica [30, 30]
sticky      : hit rate 81%, requests per replica [48, 12]
```

**Follow-ups:**
- *Why does hit rate fall when cache memory is small?* Cached blocks compete with live sequences for the same KV pool, and LRU evicts prefixes that alternate (the 3-block cache above thrashes to 0%, the 6-block cache reaches 86%).
- *How do you stop one tenant reading another's cache timing?* Per-tenant salt or isolation; the vLLM docs describe a cache salt (check live docs).
- *Round-robin vs sticky?* In my toy run sticky raised the hit rate only from 77% to 81% (every replica warms each prefix once), but put 48 of 60 requests on one replica. Hit rate gains must be weighed against load balance (Q37).

**Common mistakes:** thinking prefix caching speeds up decode; putting dynamic text (dates, user names, ids) at the top; expecting a hit on a partial block; assuming a cache hit rate someone quoted in a guide applies to your traffic; forgetting that cached blocks occupy KV memory.

### Q15 ⭐⭐⭐ 🟡 Code: write a KV-cache size and concurrency calculator (layers, KV heads, head dim, dtype, context, batch, weights, GPU memory) and check it against a hand-worked Llama-style example, including the GQA vs MHA difference.
**Asked at:** product companies, inference-platform teams, live-coding or take-home rounds; interview-prep guide, not a candidate report lists KV memory estimation
**Say this first (1 line):** KV bytes per token = 2 x layers x KV heads x head dim x bytes per element; subtract weights and overhead from the usable GPU memory, divide the remainder by the per-sequence size, and you get how many sequences fit.

**Then explain:**
- **Use KV heads, not attention heads.** GQA shares each K/V head across several query heads, so the cache shrinks by (attention heads / KV heads). Using attention heads overstates a GQA model's cache (the bug planted in Q43).
- **Pool size:** gpu_memory_utilization x GPU memory x number of GPUs, minus weights, minus an overhead term for activations and CUDA graphs. The overhead I use (2 GiB per GPU) is an assumption; real engines measure it at startup.
- **Per sequence:** per-token bytes x context, rounded up to whole blocks. Concurrency is the pool divided by that, and it is a ceiling for sequences at that full context; shorter sequences pack more.
- **Levers:** dtype (FP8 KV halves it, Q22), context length (linear), GQA/MQA/MLA (Part 1 Q10, Q33), tensor parallelism (weights split across GPUs leave more pool, Q17).
- Model configurations and parameter counts below are from memory, check against the model cards. The A100-class 80 GiB capacity is an assumption.

**Example (hand-worked first):** Llama-2-7B style, 32 layers, 32 KV heads, head dim 128, FP16: 2 x 32 x 32 x 128 x 2 = 524,288 bytes = 0.5 MiB per token, so 4,096 tokens = 2 GiB per sequence. That matches the roughly 2 GB the NVIDIA engineering blog gives for Llama 2 7B at 4,096 tokens (as summarised when read). A GQA model with 8 KV heads, same shape: 128 KiB per token, 4x smaller. A 70B-class model (80 layers, 8 KV heads): 320 KiB per token.

**Code:** (hand-checked asserts, then a sweep; assumed 80 GiB GPU, utilisation 0.90)
```python
# KV-cache size and concurrency calculator. GPU specs and overheads are ASSUMED (not measured).
from dataclasses import dataclass
GIB = 1024 ** 3

@dataclass
class Model:
    name: str; layers: int; kv_heads: int; head_dim: int; params_b: float

def kv_bytes_per_token(m, dtype_bytes):
    # K and V (the 2) x layers x kv_heads x head_dim x bytes. Uses KV heads, not attention heads.
    return 2 * m.layers * m.kv_heads * m.head_dim * dtype_bytes

def plan(m, gpu_gib, util, n_gpus, weight_bytes, kv_bytes, ctx, overhead_gib=2.0, block=16):
    total = gpu_gib * GIB * util * n_gpus                 # memory the engine may use (gpu_memory_utilization)
    weights = m.params_b * 1e9 * weight_bytes
    left = total - weights - overhead_gib * GIB * n_gpus  # overhead (activations, graphs) is an assumption
    per_tok = kv_bytes_per_token(m, kv_bytes)
    blocks_per_seq = -(-ctx // block)                     # round up to whole blocks
    per_seq = blocks_per_seq * block * per_tok
    return dict(weights_gib=weights / GIB, kv_pool_gib=left / GIB, per_tok_kib=per_tok / 1024,
                per_seq_gib=per_seq / GIB, max_seqs=max(0, int(left // per_seq)))

llama2_7b = Model("Llama-2-7B (MHA, 32 KV heads)", 32, 32, 128, 6.74)
llama3_8b = Model("Llama-3-8B (GQA, 8 KV heads)", 32, 8, 128, 8.03)
llama3_70b = Model("Llama-3-70B (GQA, 8 KV heads)", 80, 8, 128, 70.6)
llama3_70b_mha = Model("70B if it were MHA (64 KV heads)", 80, 64, 128, 70.6)

# Hand-worked checks (done on paper first)
assert kv_bytes_per_token(llama2_7b, 2) == 2 * 32 * 32 * 128 * 2 == 524288      # 0.5 MiB per token
assert kv_bytes_per_token(llama2_7b, 2) * 4096 == 2 * GIB                       # 2 GiB at 4096 tokens, batch 1
assert kv_bytes_per_token(llama3_8b, 2) == 131072                              # 128 KiB per token (4x smaller)
assert kv_bytes_per_token(llama3_70b, 2) == 327680                             # 320 KiB per token
print("hand checks passed: 7B MHA 0.5 MiB/token, 8B GQA 128 KiB/token, 70B GQA 320 KiB/token")

print("\nassumed GPU: 80 GiB, gpu_memory_utilization 0.90, overhead 2 GiB per GPU, FP16 weights, context 4096")
for m, n in [(llama2_7b, 1), (llama3_8b, 1), (llama3_70b, 2), (llama3_70b, 4), (llama3_70b_mha, 4)]:
    for kvb, tag in [(2, "FP16 KV"), (1, "FP8 KV ")]:
        r = plan(m, 80, 0.90, n, 2, kvb, 4096)
        print(f"{m.name:34s} TP={n} {tag}: weights {r['weights_gib']:6.1f} GiB, KV pool {r['kv_pool_gib']:6.1f} GiB, "
              f"{r['per_tok_kib']:6.0f} KiB/tok, seq {r['per_seq_gib']:.2f} GiB -> {r['max_seqs']} seqs")

r = plan(llama3_8b, 80, 0.90, 1, 2, 2, 32768)
print(f"\n8B GQA at 32k context: {r['per_seq_gib']:.2f} GiB per sequence -> {r['max_seqs']} concurrent seqs")
```

**Output (my run):**
```
hand checks passed: 7B MHA 0.5 MiB/token, 8B GQA 128 KiB/token, 70B GQA 320 KiB/token

assumed GPU: 80 GiB, gpu_memory_utilization 0.90, overhead 2 GiB per GPU, FP16 weights, context 4096
Llama-2-7B (MHA, 32 KV heads)      TP=1 FP16 KV: weights   12.6 GiB, KV pool   57.4 GiB,    512 KiB/tok, seq 2.00 GiB -> 28 seqs
Llama-2-7B (MHA, 32 KV heads)      TP=1 FP8 KV : weights   12.6 GiB, KV pool   57.4 GiB,    256 KiB/tok, seq 1.00 GiB -> 57 seqs
Llama-3-8B (GQA, 8 KV heads)       TP=1 FP16 KV: weights   15.0 GiB, KV pool   55.0 GiB,    128 KiB/tok, seq 0.50 GiB -> 110 seqs
Llama-3-8B (GQA, 8 KV heads)       TP=1 FP8 KV : weights   15.0 GiB, KV pool   55.0 GiB,     64 KiB/tok, seq 0.25 GiB -> 220 seqs
Llama-3-70B (GQA, 8 KV heads)      TP=2 FP16 KV: weights  131.5 GiB, KV pool    8.5 GiB,    320 KiB/tok, seq 1.25 GiB -> 6 seqs
Llama-3-70B (GQA, 8 KV heads)      TP=2 FP8 KV : weights  131.5 GiB, KV pool    8.5 GiB,    160 KiB/tok, seq 0.62 GiB -> 13 seqs
Llama-3-70B (GQA, 8 KV heads)      TP=4 FP16 KV: weights  131.5 GiB, KV pool  148.5 GiB,    320 KiB/tok, seq 1.25 GiB -> 118 seqs
Llama-3-70B (GQA, 8 KV heads)      TP=4 FP8 KV : weights  131.5 GiB, KV pool  148.5 GiB,    160 KiB/tok, seq 0.62 GiB -> 237 seqs
70B if it were MHA (64 KV heads)   TP=4 FP16 KV: weights  131.5 GiB, KV pool  148.5 GiB,   2560 KiB/tok, seq 10.00 GiB -> 14 seqs
70B if it were MHA (64 KV heads)   TP=4 FP8 KV : weights  131.5 GiB, KV pool  148.5 GiB,   1280 KiB/tok, seq 5.00 GiB -> 29 seqs

8B GQA at 32k context: 4.00 GiB per sequence -> 13 concurrent seqs
```

**Follow-ups:**
- *Why does TP=2 give only 8.5 GiB of pool for 70B?* Two GPUs offer 144 GiB usable (before overhead); FP16 weights are about 131.5 GiB, so almost nothing is left. TP=4 leaves 148.5 GiB, which is why a 70B FP16 deployment on 80 GiB cards is normally TP=4 or quantized.
- *What does GQA buy here?* If the 70B model had 64 KV heads (MHA), the same TP=4 pool would hold 14 sequences instead of 118.
- *Is the calculator exact?* No: it ignores fragmentation, cross-block overhead beyond rounding, the CUDA context and activation peaks (Q47). Treat it as a planning ceiling and confirm with the engine's startup log.

**Common mistakes:** using attention heads instead of KV heads; forgetting that bytes per element depends on dtype; forgetting K and V (the factor 2); dividing total GPU memory without subtracting weights; ignoring that gpu_memory_utilization is a cap on what the engine takes, not a measure of use.

### Q16 ⭐⭐⭐ 🟡 Code: given a log of requests (arrival, first-token and finish times, output tokens), compute TTFT, TPOT and E2E percentiles, throughput and goodput against an SLO.
**Asked at:** product companies, inference-platform teams, live-coding rounds
**Say this first (1 line):** From each request's arrival, first-token and finish times, TTFT = first - arrival, TPOT = (finish - first) / (tokens - 1), E2E = finish - arrival; report percentiles, and compute goodput as requests that meet every SLO per second.

**Then explain:**
- **Definitions** follow NVIDIA's NIM benchmarking docs as read: TTFT includes queueing and network; inter-token latency is (E2E - TTFT) / (output tokens - 1). A one-token output has no TPOT, so exclude it from TPOT rather than dividing by zero.
- **Percentiles:** state the method. Nearest-rank (used here) returns an actual observation; numpy's default interpolates. With few samples p99 is just the maximum, so say how many requests back it.
- **Throughput has two readings:** system tokens per second (total output tokens over the wall span) and per-user tokens per second (about 1 / TPOT). Requests per second is a third number. Failed requests count against goodput and must not silently vanish.
- **Goodput** is the rate of requests that met all SLOs (here TTFT and TPOT together). It can be far below raw throughput, and it is the number that DistServe-style work optimises (Q32).
- **Mean hides the tail** because a few queued requests add seconds to a few requests and barely move the average.

**Example:** a 3-request hand-checkable log: (arrival 0.0, first token 0.5, finish 2.5, 21 tokens) gives TTFT 0.5, E2E 2.5, TPOT (2.5 - 0.5) / 20 = 0.100 s. The code asserts those hand values before running a larger synthetic log (seeded, not a real trace) with an assumed SLO of TTFT at most 0.5 s and TPOT at most 45 ms.

**Code:** (synthetic log, nearest-rank percentiles, brute-force percentile check)
```python
# Request-log metrics. The log is SYNTHETIC (seeded random), not a real trace. Times in seconds.
import random, math
random.seed(7)

def pct(xs, p):
    """Nearest-rank percentile (p in 0..100): smallest value with at least p% of data at or below it."""
    s = sorted(xs); k = max(1, math.ceil(p / 100 * len(s))); return s[k - 1]

# ---- tiny hand-checkable log first -------------------------------------------------------------
tiny = [  # (arrival, first_token, finish, out_tokens, ok)
    (0.0, 0.5, 2.5, 21, True),    # TTFT 0.5, E2E 2.5, TPOT (2.5-0.5)/20 = 0.100
    (1.0, 1.2, 1.6, 5,  True),    # TTFT 0.2, E2E 0.6, TPOT 0.4/4 = 0.100
    (2.0, 4.0, 6.0, 11, True),    # TTFT 2.0, E2E 4.0, TPOT 2.0/10 = 0.200
]
def metrics(log):
    rows = []
    for a, f, e, n, ok in log:
        if not ok or n < 1: continue                      # failed requests handled separately
        tpot = (e - f) / (n - 1) if n > 1 else None       # undefined for 1-token outputs
        rows.append((f - a, tpot, e - a, n))
    return rows
m = metrics(tiny)
assert [round(r[0], 3) for r in m] == [0.5, 0.2, 2.0]
assert [round(r[1], 3) for r in m] == [0.1, 0.1, 0.2]
assert [round(r[2], 3) for r in m] == [2.5, 0.6, 4.0]
print("tiny-log hand checks passed")

# ---- synthetic log: 400 requests, Poisson arrivals, a few slow outliers ----------------------------
log, t = [], 0.0
for _ in range(400):
    t += random.expovariate(8.0)                          # about 8 requests/s
    n = max(1, int(random.lognormvariate(4.6, 0.7)))      # output tokens, long-tailed
    ttft = 0.15 + random.expovariate(1 / 0.25) + (3.0 if random.random() < 0.03 else 0)   # 3% queued badly
    tpot = 0.030 + random.random() * 0.02
    log.append((t, t + ttft, t + ttft + tpot * (n - 1), n, random.random() > 0.01))       # 1% failed
rows = metrics(log)
ttft = [r[0] for r in rows]; tpots = [r[1] for r in rows if r[1] is not None]; e2e = [r[2] for r in rows]
span = max(l[2] for l in log) - min(l[0] for l in log)
print(f"requests {len(log)}, completed {len(rows)}, failed {len(log) - len(rows)}, wall span {span:.1f}s")
for name, xs in [("TTFT", ttft), ("TPOT", tpots), ("E2E ", e2e)]:
    print(f"{name}: mean {sum(xs)/len(xs):.3f}  p50 {pct(xs,50):.3f}  p95 {pct(xs,95):.3f}  p99 {pct(xs,99):.3f}")

# percentile check against brute force: count of values <= result must be >= p% and the previous value must be below it
for xs in (ttft, e2e):
    for p in (50, 95, 99):
        v = pct(xs, p)
        assert sum(1 for x in xs if x <= v) >= p / 100 * len(xs)
        assert sum(1 for x in xs if x < v) < p / 100 * len(xs)
print("percentile brute-force check passed")

tokens = sum(r[3] for r in rows)
print(f"system throughput: {tokens/span:.0f} output tokens/s, {len(rows)/span:.2f} req/s")

SLO_TTFT, SLO_TPOT = 0.5, 0.045                           # assumed SLO: TTFT <= 0.5 s AND TPOT <= 45 ms
good = [r for r in rows if r[0] <= SLO_TTFT and (r[1] is None or r[1] <= SLO_TPOT)]
print(f"goodput under SLO (TTFT<={SLO_TTFT}s and TPOT<={SLO_TPOT*1000:.0f}ms): {len(good)}/{len(rows)} requests "
      f"= {len(good)/span:.2f} req/s ({len(good)/len(rows):.0%} of completed)")
print(f"mean TTFT {sum(ttft)/len(ttft):.3f}s hides a p99 of {pct(ttft,99):.3f}s (queued tail)")
```

**Output (my run):**
```
tiny-log hand checks passed
requests 400, completed 393, failed 7, wall span 65.5s
TTFT: mean 0.455  p50 0.308  p95 1.064  p99 3.343
TPOT: mean 0.040  p50 0.040  p95 0.049  p99 0.050
E2E : mean 5.565  p50 4.505  p95 13.323  p99 25.424
percentile brute-force check passed
system throughput: 774 output tokens/s, 6.00 req/s
goodput under SLO (TTFT<=0.5s and TPOT<=45ms): 220/393 requests = 3.36 req/s (56% of completed)
mean TTFT 0.455s hides a p99 of 3.343s (queued tail)
```

**Follow-ups:**
- *Why is goodput only 56% of completed requests here?* Both SLOs must hold at once: in this synthetic log TPOT is uniform from 30 to 50 ms, so about a quarter of requests miss 45 ms on their own, and the queued tail misses TTFT. The synthetic distribution is mine, not a measurement.
- *Which clock do you trust?* Timestamp at the client or load balancer for user-visible TTFT; engine-side clocks miss network and gateway queueing.
- *How do you treat streaming stalls?* Use the full inter-token gap distribution, not just the mean TPOT, since a request can average 40 ms and still freeze for a second.

**Common mistakes:** dividing by output tokens instead of tokens - 1; reporting only the mean; mixing arrival time with engine-admission time; ignoring failed or cancelled requests; computing goodput with one SLO when the product has two.

### Q17 ⭐⭐ 🟡 Tensor vs pipeline vs data parallelism for inference: when must you shard, how do they affect latency and throughput, and when are two replicas better than one TP=2 deployment? (Part 2 Q34 covers training parallelism.)
**Asked at:** inference-platform teams, GCCs; interview-prep guide, not a candidate report lists TP=2 vs TP=4 and TP vs replicas
**Say this first (1 line):** Shard (tensor parallel) only when the model or its KV pool does not fit on one GPU or when you need lower per-token latency; otherwise replicas (data parallel) give more throughput with less communication and better isolation.

**Then explain:**
- **Tensor parallelism (TP)** splits each layer's matrices across GPUs, so every decode step reads only a shard of the weights (lower per-token latency) but needs allreduces every layer, so it wants a fast interconnect inside one node. vLLM's docs describe TP as sharding the parameters; check live docs for how it interacts with KV memory.
- **Pipeline parallelism (PP)** puts different layers on different GPUs. It needs little bandwidth between stages (so it can span nodes), does not cut single-request latency, and needs several requests in flight to keep stages busy.
- **Data parallelism / replicas** run independent copies. Throughput scales nearly linearly, a replica failure costs only that replica, and there is no per-layer communication. Each copy pays for its own weights.
- **When you must shard:** weights plus a useful KV pool do not fit. TP also helps indirectly: weights are split, so more of each GPU is left for KV, which raises concurrency.
- **TP=2 vs two replicas** for a model that fits on one GPU: TP=2 gives lower latency per stream (less than 2x because of communication) and a bigger shared pool; two replicas give more total streams at the baseline latency and fewer failure modes. Pick by the SLO: tight TPOT at low load favours TP, throughput per dollar and resilience favour replicas.

**Example:** assumed hardware (80 GiB, 2.0 TB/s per GPU, 15 microseconds per allreduce, two allreduces per layer; all assumed): an 8B-class model with 16 GiB of weights decodes batch-1 at 8.59 ms per token on one GPU and 5.25 ms with TP=2, a speedup of 1.64x rather than 2x. Two replicas keep 8.59 ms per stream but serve two independent streams. A 70B-class FP16 model (140 GiB) leaves 0.0 GiB of KV pool at TP=2 in this arithmetic, so TP=2 is unusable and TP=4 is the first workable size.

**Code:** (toy roofline with assumed constants; communication cost is held constant, which is a weak assumption)
```python
# TP vs replicas, toy roofline. EVERYTHING here is ASSUMED: 80 GiB GPUs, 2.0 TB/s per GPU, allreduce cost per layer.
GIB = 1024 ** 3
HBM_GIB, UTIL, OVERHEAD_GIB = 80, 0.90, 2.0
BW = 2.0e12                  # assumed bytes/s per GPU
AR_US = 15e-6                # assumed latency of one allreduce (small message, NVLink-class); 2 per layer
def step_time(weight_gib, layers, tp):
    # batch-1 decode step: read the weight shard from HBM + 2 allreduces per layer (attention out, MLP out)
    read = weight_gib * GIB / tp / BW
    comm = 0 if tp == 1 else 2 * layers * AR_US
    return read + comm

def kv_room(weight_gib, tp):                      # KV pool across the group, GiB (negative = does not fit)
    return tp * HBM_GIB * UTIL - weight_gib - tp * OVERHEAD_GIB

print("--- 8B-class model (16 GiB FP16 weights, 32 layers): 2 GPUs as TP=2 vs 2 independent replicas")
for label, tp, copies in [("TP=1 x1", 1, 1), ("TP=2 x1", 2, 1), ("2 replicas", 1, 2)]:
    t = step_time(16, 32, tp)
    print(f"{label:10s}: batch-1 step {t*1e3:5.2f} ms -> {1/t:6.1f} tok/s per stream; "
          f"KV pool total {copies*kv_room(16, tp):6.1f} GiB")
print("TP=2 cuts per-stream latency less than 2x (comm overhead); two replicas double independent streams.")

print("\n--- 70B-class model (140 GiB FP16 weights, 80 layers)")
for tp in (1, 2, 4, 8):
    room = kv_room(140, tp)
    if room <= 0:
        print(f"TP={tp}: no usable KV room ({room:.1f} GiB left after weights)"); continue
    t = step_time(140, 80, tp)
    print(f"TP={tp}: batch-1 step {t*1e3:5.1f} ms ({1/t:5.1f} tok/s), KV pool {room:6.1f} GiB")

print("\n--- same hardware budget of 8 GPUs, 70B model: TP=4 x 2 replicas vs TP=8 x 1")
for tp, copies in [(4, 2), (8, 1)]:
    t = step_time(140, 80, tp)
    print(f"TP={tp} x{copies}: per-stream {1/t:5.1f} tok/s, total KV pool {copies*kv_room(140, tp):6.1f} GiB")
```

**Output (my run):**
```
--- 8B-class model (16 GiB FP16 weights, 32 layers): 2 GPUs as TP=2 vs 2 independent replicas
TP=1 x1   : batch-1 step  8.59 ms ->  116.4 tok/s per stream; KV pool total   54.0 GiB
TP=2 x1   : batch-1 step  5.25 ms ->  190.3 tok/s per stream; KV pool total  124.0 GiB
2 replicas: batch-1 step  8.59 ms ->  116.4 tok/s per stream; KV pool total  108.0 GiB
TP=2 cuts per-stream latency less than 2x (comm overhead); two replicas double independent streams.

--- 70B-class model (140 GiB FP16 weights, 80 layers)
TP=1: no usable KV room (-70.0 GiB left after weights)
TP=2: no usable KV room (0.0 GiB left after weights)
TP=4: batch-1 step  21.2 ms ( 47.2 tok/s), KV pool  140.0 GiB
TP=8: batch-1 step  11.8 ms ( 84.8 tok/s), KV pool  420.0 GiB

--- same hardware budget of 8 GPUs, 70B model: TP=4 x 2 replicas vs TP=8 x 1
TP=4 x2: per-stream  47.2 tok/s, total KV pool  280.0 GiB
TP=8 x1: per-stream  84.8 tok/s, total KV pool  420.0 GiB
```

**Follow-ups:**
- *Why not always use the biggest TP?* Communication per layer does not shrink as you add GPUs, kernels get small, and one GPU failure takes down the group. My toy holds allreduce cost flat, so it overstates TP=8's gain.
- *When is pipeline parallelism preferred?* Across nodes without fast interconnect, or when throughput matters more than latency.
- *Does TP raise throughput?* It can, by freeing KV memory for larger batches, but compare against replicas at equal GPU count, as in the 8-GPU comparison above (TP=4 x2 vs TP=8).

**Common mistakes:** assuming TP=2 halves latency; sharding a model that fits, paying for communication with no memory need; ignoring that a TP group fails together; forgetting that TP needs fast intra-node links; comparing TP and replicas at different GPU counts.

### Q18 ⭐⭐ 🟡 Self-host vs call an API: build the break-even (token volume, utilisation, engineering and on-call cost, privacy, quality, latency, lock-in) and say what would change your answer. (Part 4 Q25 covers the fine-tuned-small-model case.)
**Asked at:** product companies, GCCs, GenAI startups; interview-prep guide, not a candidate report lists managed API vs self-hosting
**Say this first (1 line):** Self-hosting wins only when sustained token volume keeps enough GPUs busy that cost per token, plus the fixed cost of engineers and redundancy, drops below the API price; below that volume the API is cheaper, and privacy or latency needs can override cost.

**Then explain:**
- **Cost model:** self cost per month = GPUs x hours x GPU price + fixed engineering, on-call, monitoring and evaluation cost. API cost = volume x price per token. Break-even volume is where they cross.
- **Utilisation sets the slope.** GPUs must cover peak demand, so average utilisation is roughly 1 / (peak to average ratio) unless you can autoscale or fill troughs with offline work (Q13, Q34).
- **There is a floor:** at least two GPUs for redundancy, so small volume is dominated by fixed cost. Costs also come in steps as you add GPUs.
- **Non-cost factors:** data residency and privacy (self-hosting can be required), latency control, ability to fine-tune or serve custom adapters (Part 4 Q25 has the small-model case), quality gap versus frontier APIs, lock-in and rate-limit risk, and vendor price changes (the API price is not a constant).
- **What changes the answer:** volume growth, a smaller or distilled model that is good enough, prices moving, utilisation improving (batching, quantization), or a compliance requirement.

**Example:** hypothetical units only (1 unit = one GPU-hour; assumed 4M blended tokens per GPU-hour at SLO; API 0.80 units per M tokens; fixed engineering 300 units/month; a 2-GPU floor; 730 hours per month). With peak-to-average ratio 2 the API is cheaper through 2,000M tokens per month (1,600 vs 1,760 units) and self-hosting is cheaper from 5,000M (4,000 vs 3,220). The scan puts the first break-even at 2,210M tokens/month. Quadrupling the fixed cost moves it to 4,240M; with a peak-to-average ratio of 4 self-hosting never wins in the scanned range because the effective cost per M tokens (1.0 unit) exceeds the API price.

**Code:** (hypothetical symbolic numbers; change the constants to your own)
```python
# Self-host vs API break-even. All numbers HYPOTHETICAL in symbolic units (1 unit = one GPU-hour).
import math
GPU_HR = 1.0                     # unit
HOURS = 730                      # hours per month
CAPACITY_M_PER_GPU_HR = 4.0      # assumed: millions of blended tokens one GPU serves per busy hour at SLO
API_PER_M = 0.80                 # assumed API price, units per million blended tokens
FIXED_ENG = 300.0                # assumed monthly engineering/on-call/monitoring cost in units
MIN_GPUS = 2                     # redundancy floor for an always-on service

def self_cost(vol_m, peak_to_avg=2.0, target_util=None):
    # GPUs must cover PEAK demand, so average utilisation = 1/peak_to_avg unless you autoscale perfectly
    need = vol_m / HOURS / CAPACITY_M_PER_GPU_HR * peak_to_avg          # GPUs needed at peak
    gpus = max(MIN_GPUS, math.ceil(need))
    return gpus * GPU_HR * HOURS + FIXED_ENG, gpus, vol_m / HOURS / (gpus * CAPACITY_M_PER_GPU_HR)

print("monthly volume (M tokens) | API cost | self cost | GPUs | avg util | cheaper")
for vol in (100, 500, 1000, 2000, 5000, 20000, 100000):
    s, g, u = self_cost(vol)
    a = vol * API_PER_M
    print(f"{vol:12d}              | {a:8.0f} | {s:9.0f} | {g:4d} | {u:7.0%}  | {'self' if s < a else 'API'}")

def breakeven(**kw):
    for vol in range(10, 400000, 10):
        if self_cost(vol, **kw)[0] < vol * API_PER_M: return vol
    return 'never (scanned to 400,000)'
print("\nbreak-even volume (M tokens/month, first scanned volume where self is cheaper):")
print("  peak/avg 2.0 :", breakeven(peak_to_avg=2.0))
print("  peak/avg 4.0 :", breakeven(peak_to_avg=4.0))
print("  peak/avg 1.0 :", breakeven(peak_to_avg=1.0))
FIXED_ENG = 1200.0
print("  fixed eng cost x4 (peak/avg 2.0):", breakeven(peak_to_avg=2.0))
API_PER_M = 0.40
print("  API price halved (eng x4 kept)  :", breakeven(peak_to_avg=2.0))
```

**Output (my run):**
```
monthly volume (M tokens) | API cost | self cost | GPUs | avg util | cheaper
         100              |       80 |      1760 |    2 |      2%  | API
         500              |      400 |      1760 |    2 |      9%  | API
        1000              |      800 |      1760 |    2 |     17%  | API
        2000              |     1600 |      1760 |    2 |     34%  | API
        5000              |     4000 |      3220 |    4 |     43%  | self
       20000              |    16000 |     10520 |   14 |     49%  | self
      100000              |    80000 |     50670 |   69 |     50%  | self

break-even volume (M tokens/month, first scanned volume where self is cheaper):
  peak/avg 2.0 : 2210
  peak/avg 4.0 : never (scanned to 400,000)
  peak/avg 1.0 : 2210
  fixed eng cost x4 (peak/avg 2.0): 4240
  API price halved (eng x4 kept)  : never (scanned to 400,000)
```

**Follow-ups:**
- *What if the API price halves?* In my toy, with the engineering cost kept at 4x, self-hosting never wins in the scanned range; vendor price moves can erase the case.
- *What about reserved or spot GPUs?* They change the GPU price term only; the utilisation and fixed-cost logic stays.
- *What is the hidden cost?* Evaluation and regression testing for each model or engine upgrade, security patching, and incident response.

**Common mistakes:** comparing GPU price per hour with API price per token without a utilisation term; leaving out engineers and on-call; sizing for average rather than peak load; treating quality as equal; deciding once and never re-running the numbers.

### Q19 ⭐⭐ 🟡 Streaming tokens with SSE: how does the path from engine to browser work, what is backpressure for a slow client, how do you handle cancellation and disconnects so GPU work stops, and how do proxies break streaming?
**Asked at:** product companies, inference-platform teams; interview-prep guide, not a candidate report poses streaming with backpressure as a design prompt
**Say this first (1 line):** The engine emits tokens as it decodes, a server wraps them as Server-Sent Events over a long-lived HTTP response, and the key production work is propagating a client disconnect back to the engine so the GPU stops, bounding per-client buffers, and stopping proxies from buffering the stream.

**Then explain:**
- **Path:** engine step produces a token, detokeniser turns token ids into text (watch partial UTF-8 and merged tokens), the API server writes an SSE frame (`data: ...` followed by a blank line), a gateway or proxy forwards it, and the browser reads it with EventSource or fetch streaming. TGI's docs list SSE token streaming as a feature.
- **Backpressure:** the engine produces at its own pace; a slow client or network does not slow it. If the server buffers unboundedly, memory grows per slow client. Use a bounded per-request buffer and a policy: drop the connection after a stall timeout, or coalesce tokens into bigger frames. Do not stall the whole batch for one reader.
- **Cancellation:** a closed connection must trigger an abort in the engine (free the slot and KV blocks). Detect it in the server (disconnect event or failed write), then call the engine's abort. Without it, decoding continues to max_tokens for nobody.
- **Proxies:** response buffering, gzip and idle timeouts break streaming; the token arrives all at once or the connection is cut during a long prefill. Turn off buffering for the route, send periodic comment frames as keep-alives, and set idle timeouts above worst-case TTFT. Specific header and setting names vary by proxy, from memory, check yours.
- **Measure TTFT at the client**, where buffering shows up.

**Example:** a toy tick simulation: the engine makes 1 token per tick, a slow client reads 1 every 3 ticks. Unbounded buffering reaches a peak of 80 queued tokens in 120 ticks. A 16-token limit closes the slow stream after 25 tokens. If a client disconnects at tick 20 and abort is not propagated, the engine decodes 100 more ticks for nobody; with abort propagated, it stops at 20.

**Code:** (deterministic tick simulation, no sockets; shows the SSE frame format)
```python
# Streaming toy: deterministic tick simulation (no network). 1 tick = one decode step of the engine.
def sse(token):                                   # one Server-Sent Event frame; the blank line ends the event
    return f"data: {token}\n\n"
print(repr(sse("Hel")), repr(sse("lo")), repr("data: [DONE]\n\n"))

def run(client_every, buffer_limit, disconnect_at, abort_on_disconnect, max_tokens=200, ticks=120):
    """Engine makes 1 token per tick. The client reads 1 token every `client_every` ticks.
    buffer_limit=None -> unbounded server-side buffer. Otherwise: if the buffer is full the stream is closed (slow-client policy)."""
    buf, engine_tokens, delivered, peak, closed = 0, 0, 0, 0, False
    gpu_ticks_after_gone = 0
    for t in range(ticks):
        gone = disconnect_at is not None and t >= disconnect_at
        if gone and abort_on_disconnect: break    # abort propagates to the engine: slot and KV freed
        if engine_tokens < max_tokens and not closed:
            engine_tokens += 1; buf += 1; peak = max(peak, buf)
            if gone: gpu_ticks_after_gone += 1    # decoding for nobody
            if buffer_limit is not None and buf > buffer_limit:
                closed = True                     # shed the slow consumer instead of buffering forever
        if not gone and t % client_every == 0 and buf > 0:
            buf -= 1; delivered += 1
    return dict(engine_tokens=engine_tokens, delivered=delivered, peak_buffer=peak,
                wasted_ticks=gpu_ticks_after_gone, closed=closed)

print("\nslow client (reads 1 token per 3 ticks, engine makes 1 per tick):")
print("  unbounded buffer :", run(3, None, None, False))
print("  buffer limit 16  :", run(3, 16, None, False))
print("\nclient disconnects at tick 20:")
print("  no abort propagation:", run(1, None, 20, False))
print("  abort propagated    :", run(1, None, 20, True))
print("(max_tokens=200: without abort the engine keeps decoding to the cap for nobody)")
```

**Output (my run):**
```
'data: Hel\n\n' 'data: lo\n\n' 'data: [DONE]\n\n'

slow client (reads 1 token per 3 ticks, engine makes 1 per tick):
  unbounded buffer : {'engine_tokens': 120, 'delivered': 40, 'peak_buffer': 80, 'wasted_ticks': 0, 'closed': False}
  buffer limit 16  : {'engine_tokens': 25, 'delivered': 25, 'peak_buffer': 17, 'wasted_ticks': 0, 'closed': True}

client disconnects at tick 20:
  no abort propagation: {'engine_tokens': 120, 'delivered': 20, 'peak_buffer': 100, 'wasted_ticks': 100, 'closed': False}
  abort propagated    : {'engine_tokens': 20, 'delivered': 20, 'peak_buffer': 1, 'wasted_ticks': 0, 'closed': False}
(max_tokens=200: without abort the engine keeps decoding to the cap for nobody)
```

**Follow-ups:**
- *SSE or WebSocket?* SSE is one-way text over plain HTTP and fits token streams; WebSocket helps when the client also sends mid-stream messages.
- *What about retries after a drop?* Send event ids and let the client resume, or accept restarting; resuming requires keeping generated text server-side.
- *How do you make cancellation reliable?* Test it: count live sequences in the engine after a client kills the connection, and alert if they stay.

**Common mistakes:** assuming a closed socket stops GPU work; buffering whole responses in a proxy; unbounded queues per client; measuring TTFT at the server; forgetting max_tokens as a backstop.

### Q20 ⭐⭐ 🟡 Chunked prefill and scheduling: how does the scheduler mix prefill and decode under a token budget, why does a long prompt stall other users' decoding without chunking, and how do max_num_batched_tokens and max_num_seqs trade TTFT against inter-token latency?
**Asked at:** inference-platform teams, AI labs; interview-prep guide, not a candidate report lists chunked prefill; vLLM docs describe the token-budget knobs
**Say this first (1 line):** The scheduler gives each step a token budget; decodes go first, and leftover budget is spent on prefill chunks, so a long prompt is spread across many steps instead of freezing everyone else's decoding for one big step.

**Then explain:**
- **Without chunking** a step processing an 8,000-token prompt takes far longer than a decode step, and every active user's next token waits for it, so inter-token latency (ITL) spikes for all.
- **With chunking** the prompt is cut into pieces that fit the leftover budget. As of the vLLM docs read on 2026-10-24 (check live docs), chunked prefill is on by default in V1, decodes are scheduled first, and the remaining max_num_batched_tokens go to prefill.
- **The knob:** smaller max_num_batched_tokens favours ITL (short steps) but slows the long prompt's TTFT; larger favours TTFT and throughput but allows bigger stalls (the vLLM tuning docs say the same). max_num_seqs caps concurrent sequences: more sequences raise throughput and lower queueing TTFT, but each step has more work, so ITL rises.
- **Authors' claim:** Sarathi-Serve reports stall-free scheduling with chunked prefills; for example 2.6x serving capacity versus vLLM on Mistral-7B with A100 (reported by the authors in their setup, I read the abstract only).

**Example:** assumed step-time model (5 ms + 0.02 ms per prefill token + 0.15 ms per decoding sequence), 8 users decoding, an 8,000-token prompt arrives. With a 8,192 budget the prompt goes in one step: decoders see a 166.2 ms step and the long prompt's first token arrives at 166.2 ms. With a 512 budget, the worst decoder step is 16.3 ms and the long prompt's TTFT is 259.2 ms. With a 256 budget, the worst step is 11.2 ms but TTFT is 364.6 ms.

**Code:** (toy scheduler, assumed linear step-time model; not a measurement of any engine)
```python
# Chunked prefill with a per-step token budget. Step-time model is ASSUMED (not measured):
# step_ms = 5 + 0.02 * prefill_tokens + 0.15 * decoding_seqs
def step_ms(prefill_tokens, n_decode):
    return 5 + 0.02 * prefill_tokens + 0.15 * n_decode

def pct(xs, p):
    s = sorted(xs); import math; return s[max(1, math.ceil(p / 100 * len(s))) - 1]

def sim_long_prompt(budget, n_decoders=8, long_prompt=8000, arrive_step=10, steps=400):
    """n_decoders users are mid-generation. At arrive_step an 8000-token prompt arrives.
    Each step: all decodes run first (1 token each), leftover budget goes to prefill chunks."""
    t, itls, remaining, ttft = 0.0, [], None, None
    for s in range(steps):
        if s == arrive_step: remaining, t_arr = long_prompt, t
        chunk = 0
        if remaining:
            chunk = min(remaining, max(0, budget - n_decoders))
            remaining -= chunk
        dt = step_ms(chunk, n_decoders)
        t += dt
        itls.append(dt)                               # every decoder emits one token per step
        if remaining == 0 and ttft is None and chunk > 0:
            ttft = t - t_arr                          # long prompt's first token comes after its last chunk step
        if ttft is not None and s > arrive_step + 40: break
    return itls, ttft

print("budget(max_num_batched_tokens) | decoders' ITL p50 / p99 / max (ms) | long prompt TTFT (ms)")
for b in (256, 512, 2048, 8192):
    itls, ttft = sim_long_prompt(b)
    print(f"{b:6d}                         | {pct(itls,50):6.1f} / {pct(itls,99):6.1f} / {max(itls):6.1f}      | {ttft:7.1f}")
print("8192 budget = whole 8000-token prompt in one step (behaves like no chunking).")

# max_num_seqs: 40 requests (100-token prompt, 20 output tokens) arrive at once; cap concurrent sequences
def sim_cap(max_seqs, n=40, prompt=100, out=20, budget=2048):
    waiting, running, t = list(range(n)), {}, 0.0
    ttft, itls, tokens = {}, [], 0
    while waiting or running:
        prefill = 0
        while waiting and len(running) < max_seqs and prefill + prompt <= budget - len(running):
            r = waiting.pop(0); running[r] = out; prefill += prompt; ttft[r] = None
        dec = [r for r in running if ttft[r] is not None]
        dt = step_ms(prefill, len(dec)); t += dt
        for r in list(dec):
            running[r] -= 1; tokens += 1; itls.append(dt)
            if running[r] == 0: del running[r]
        for r in running:
            if ttft[r] is None: ttft[r] = t            # first token appears at the end of its prefill step (toy)
    return sum(ttft.values()) / n, pct(list(ttft.values()), 99), sum(itls) / len(itls), tokens / t * 1000
print("\nmax_num_seqs | mean TTFT | p99 TTFT | mean ITL (ms) | tokens/s (toy)")
for cap in (4, 8, 16, 40):
    a, b99, itl, tps = sim_cap(cap)
    print(f"{cap:6d}       | {a:7.1f}   | {b99:7.1f}  | {itl:6.2f}        | {tps:7.0f}")
```

**Output (my run):**
```
budget(max_num_batched_tokens) | decoders' ITL p50 / p99 / max (ms) | long prompt TTFT (ms)
   256                         |   11.2 /   11.2 /   11.2      |   364.6
   512                         |    6.2 /   16.3 /   16.3      |   259.2
  2048                         |    6.2 /   47.0 /   47.0      |   184.8
  8192                         |    6.2 /  166.2 /  166.2      |   166.2
8192 budget = whole 8000-token prompt in one step (behaves like no chunking).

max_num_seqs | mean TTFT | p99 TTFT | mean ITL (ms) | tokens/s (toy)
     4       |   575.5   |  1138.0  |   5.60        |     640
     8       |   311.0   |   601.0  |   6.20        |    1103
    16       |   181.8   |   391.0  |   7.16        |    1553
    40       |    69.0   |    93.0  |  11.85        |    2581
```

**Follow-ups:**
- *Why are p50 ITLs identical for 512 to 8192?* Most steps in the window are plain decode steps; the budget only changes the few chunk steps, which is why you must look at p99 and max, not the median. At budget 256 the p50 itself is 11.2 ms because most steps in this short window are chunk steps.
- *Is there a best budget?* It depends on the SLO: choose the largest budget whose worst step still meets TPOT, because larger budgets help TTFT and throughput.
- *Does chunking change outputs?* It splits an exact computation, so the result is mathematically the same (up to floating-point differences).

**Common mistakes:** thinking chunked prefill speeds up the prompt (it slows that prompt slightly, to protect others); tuning only the median ITL; leaving max_num_seqs untouched for long-context traffic; copying the default budget from another workload.

### Q21 ⭐⭐ 🟡 Preemption and admission control in an engine: what happens when KV blocks run out (recompute vs swap), what does it do to tail latency, and what do you tune or monitor to avoid it?
**Asked at:** inference-platform teams; interview-prep guide, not a candidate report lists preemption
**Say this first (1 line):** When the KV block pool runs out, the engine must evict a running sequence (preempt) and later restart it by recomputing its context or swapping its blocks to CPU, which wastes work and adds latency to the victim, so you size the pool and admission to avoid it.

**Then explain:**
- **Why it happens:** admission looks at prompts, but sequences keep growing during decode, so a pool that fit every prompt can still run out later. Block allocation happens at block boundaries, so pressure shows up suddenly.
- **Two recovery styles:** recompute (drop the victim's blocks, re-prefill prompt plus generated tokens later) or swap (copy blocks to host memory and back). As of the vLLM docs read on 2026-10-24, preemption by recompute is the V1 default; check live docs and your version.
- **Cost to tail latency:** the victim loses its progress and waits in the queue again, and recompute competes with new prefill. Preemption raises p99 more than p50; many preemptions mean the pool is undersized for the workload.
- **What to tune and watch:** lower max_num_seqs or max_num_batched_tokens, keep gpu_memory_utilization high enough for the pool, quantize the KV cache (Q22), add an admission watermark (admit only if free blocks exceed the prompt need plus a reserve), and alert on KV-cache usage and preemption counts. I did not see a preemption counter on the vLLM metrics design page I read; check what your version exports.
- **Victim choice:** the newest request is typically preempted so older ones can finish; this is a policy choice you should state.

**Example:** a synthetic seeded workload (120 requests, prompts of 60 to 300 tokens, outputs of 40 to 260, 16-token blocks). With a 400-block pool and no reserve there are 66 preemptions and 11,478 recomputed tokens; a 12-block admission reserve cuts that to 19 preemptions and 3,655 recomputed tokens. But p99 latency barely moves (625 vs 618 ticks at 400 blocks, and 1,735 vs 1,817 ticks at 160 blocks): in this toy, total capacity drives latency, and the reserve mainly trades fewer preemptions for slower admission.

**Code:** (toy block pool with recompute preemption; assumed 256 tokens per tick re-prefill; synthetic workload)
```python
# Toy KV block pool with preemption by recompute. Workload is SYNTHETIC (seeded). 1 tick = 1 decode step.
import random, math
BLOCK = 16
def pct(xs, p):
    s = sorted(xs); return s[max(1, math.ceil(p / 100 * len(s))) - 1]

def simulate(pool_blocks, reserve=0, n=120, seed=3, rate=0.35):
    rnd = random.Random(seed)
    reqs, t = [], 0.0
    for i in range(n):
        t += rnd.expovariate(rate)
        reqs.append(dict(id=i, arrive=int(t), prompt=rnd.randint(60, 300), out=rnd.randint(40, 260)))
    waiting, running, free = [], [], pool_blocks
    done, preempts, wasted, tick, nxt = {}, 0, 0, 0, 0
    need = lambda tokens: -(-tokens // BLOCK)
    while len(done) < n and tick < 200000:
        while nxt < n and reqs[nxt]['arrive'] <= tick:
            r = reqs[nxt]; r.update(gen=0, blocks=0, first=None); waiting.append(r); nxt += 1
        # admit FCFS if the prompt (plus any generated tokens, for preempted requests) fits plus a reserve
        while waiting:
            r = waiting[0]; b = need(r['prompt'] + r['gen'])
            if free - b >= reserve and b <= pool_blocks:
                waiting.pop(0); free -= b; r['blocks'] = b; running.append(r)
                if r['gen'] > 0:
                    wasted += r['prompt'] + r['gen']                   # recompute: whole context prefilled again
                    r['stall'] = -(-(r['prompt'] + r['gen']) // 256)
            else: break
        # decode one token for each running request; allocate a block at each boundary
        for r in list(running):
            if r not in running: continue
            total = r['prompt'] + r['gen']
            if r.get('stall', 0) > 0:                                  # re-prefilling after preemption (assumed 256 tokens/tick)
                r['stall'] -= 1; continue
            if r['blocks'] * BLOCK < total + 1:                           # next token needs a new block
                while free < 1 and len(running) > 1:                  # out of blocks: preempt the newest request
                    victim = max((x for x in running if x is not r), key=lambda x: x['arrive'])
                    running.remove(victim); free += victim['blocks']; victim['blocks'] = 0
                    waiting.insert(0, victim); preempts += 1
                if free < 1: continue                                  # cannot grow, stall this tick
                free -= 1; r['blocks'] += 1
            r['gen'] += 1
            if r['first'] is None: r['first'] = tick
            if r['gen'] >= r['out']:
                running.remove(r); free += r['blocks']; done[r['id']] = tick - r['arrive']
        tick += 1
    lat = list(done.values())
    return preempts, wasted, pct(lat, 50), pct(lat, 99), tick

print("pool blocks | reserve | preemptions | recomputed tokens | latency p50 / p99 (ticks)")
for pool in (400, 300, 220, 160):
    for reserve in (0, 12):
        p, w, a, b, _ = simulate(pool, reserve)
        print(f"{pool:8d}    | {reserve:5d}   | {p:8d}    | {w:10d}        | {a:6d} / {b:6d}")
```

**Output (my run):**
```
pool blocks | reserve | preemptions | recomputed tokens | latency p50 / p99 (ticks)
     400    |     0   |       66    |      11478        |    313 /    625
     400    |    12   |       19    |       3655        |    316 /    618
     300    |     0   |       74    |      13472        |    447 /    811
     300    |    12   |       24    |       4732        |    451 /    824
     220    |     0   |       84    |      14972        |    647 /   1212
     220    |    12   |       24    |       4637        |    661 /   1264
     160    |     0   |       81    |      15187        |    924 /   1735
     160    |    12   |       23    |       4476        |    944 /   1817
```

**Follow-ups:**
- *Recompute or swap?* Recompute costs compute and no PCIe bandwidth; swap costs host memory and transfer time. Which wins depends on the interconnect and context length, so measure.
- *Why did the reserve not help p99 here?* Honest toy result: it reduces wasted work but also delays admissions; real gains depend on how expensive recompute is relative to waiting.
- *How is this different from OOM?* Preemption is the engine managing a full pool gracefully; OOM is memory outside the pool (Q47).

**Common mistakes:** sizing the pool for prompts only; treating preemption as free; not exporting or alerting on preemption; raising max_num_seqs to chase throughput without extra KV room.

### Q22 ⭐⭐ 🟡 KV-cache quantization (for example FP8): how much capacity does it add, what does it do to quality and speed, why do scales and calibration matter, and when is it risky? (Part 1 Q23 compares KV levers.)
**Asked at:** inference-platform teams, GenAI startups; interview-prep guide, not a candidate report lists KV-cache quantization trade-offs
**Say this first (1 line):** Storing K and V in FP8 halves bytes per token versus FP16, roughly doubling the number of cached tokens, at a small accuracy cost that depends on getting the scales right; the risk is clipping and underflow when scales are wrong or uncalibrated.

**Then explain:**
- **Capacity:** per-token KV bytes scale with the element size (Q15). FP16 to FP8 gives about 2x tokens in the same pool, so more concurrent sequences or longer context. The scales themselves are tiny.
- **Speed:** decode attention reads the whole KV cache each step, so smaller KV means less memory traffic; the gain depends on whether the attention kernel handles FP8 natively or converts on the fly, so measure on your hardware (check live docs for kernel and hardware support).
- **Scales matter:** FP8 E4M3 only spans up to 448 (Q23), so values are divided by a scale first. As read in the vLLM quantized-KV docs (check live docs), scales can be per tensor or per attention head and are calibrated, for example with llm-compressor; without calibration the default scale is 1.0.
- **Quality:** FP8 keeps 3 mantissa bits so each value has about a few percent relative error even when scaled well; softmax over many keys averages some of this out, but outlier heads and long contexts (where errors accumulate over many tokens) are where it hurts. The docs suggest skipping sensitive layers.
- **When risky:** long-context retrieval, models with outlier K channels, no calibration data matching your traffic, and safety-critical output. Validate with long-context evals (Q10).

**Example:** for an 8B-class GQA model (32 layers, 8 KV heads, head dim 128, from memory) FP16 uses 131,072 bytes per token and FP8 65,536; a 55 GiB pool (taken from Q15's calculator) holds 450,560 versus 901,120 tokens. In my synthetic toy with 8 heads of very different magnitude (assumed), the uncalibrated scale of 1.0 clips 1.67% of K values and gives a relative attention-output error of 1.451 on the largest head; per-tensor and per-head scales bring that head to 0.026.

**Code:** (torch float8_e4m3fn cast on CPU; synthetic K and V, assumed head magnitudes)
```python
# FP8 (E4M3) KV-cache toy: capacity gain + effect of scale choice. K/V are SYNTHETIC, head magnitudes are assumed.
import torch
torch.manual_seed(0)
E4M3_MAX = 448.0

def fp8_roundtrip(x, scale):
    """Store x/scale as float8_e4m3fn, read back and multiply by scale. Clamp first: the cast is not saturating."""
    q = (x / scale).clamp(-E4M3_MAX, E4M3_MAX).to(torch.float8_e4m3fn)
    return q.to(torch.float32) * scale

# ---- capacity: bytes per token halves (scales add a tiny overhead) ------------------------------
layers, kv_heads, hd = 32, 8, 128                        # Llama-3-8B-like config (from memory, check)
fp16 = 2 * layers * kv_heads * hd * 2
fp8 = 2 * layers * kv_heads * hd * 1
scale_bytes = 2 * layers * kv_heads * 4                  # one fp32 scale per head per layer for K and V (static, per-head)
print(f"bytes/token: FP16 {fp16}, FP8 {fp8}; per-head fp32 scales cost {scale_bytes} bytes in total (not per token)")
pool_gib = 55.0                                          # KV pool assumed from the Q15 calculator (8B on one 80 GiB GPU)
for name, b in (("FP16", fp16), ("FP8 ", fp8)):
    print(f"{name}: {int(pool_gib * 1024**3 // b):>9,d} cached tokens in a {pool_gib} GiB pool")

# ---- quality: attention output error under three scale policies ----------------------------------
T, H, D = 512, 8, 64
head_std = torch.tensor([0.002, 0.05, 0.5, 1.0, 2.0, 5.0, 20.0, 300.0])   # assumed, deliberately wide range
K = torch.randn(H, T, D) * head_std[:, None, None]
V = torch.randn(H, T, D) * head_std[:, None, None].sqrt()
q = torch.randn(H, 1, D)

def attn(K, V):
    p = torch.softmax(q @ K.transpose(1, 2) / D ** 0.5, dim=-1)
    return p @ V
ref = attn(K, V)

def policy(name, kscale, vscale):
    out = attn(fp8_roundtrip(K, kscale), fp8_roundtrip(V, vscale))
    rel = ((out - ref).flatten(1).norm(dim=1) / ref.flatten(1).norm(dim=1))
    return name, rel
one = torch.tensor(1.0)
pt_k = K.abs().max() / E4M3_MAX; pt_v = V.abs().max() / E4M3_MAX
ph_k = K.abs().amax(dim=(1, 2), keepdim=True) / E4M3_MAX; ph_v = V.abs().amax(dim=(1, 2), keepdim=True) / E4M3_MAX
print("\nrelative attention-output error per head (head std 0.002 ... 300):")
for name, rel in (policy("scale 1.0 (uncalibrated default)", one, one),
                  policy("one per-tensor scale           ", pt_k, pt_v),
                  policy("per-head scale                 ", ph_k, ph_v)):
    print(f"{name}: " + " ".join(f"{x:.3f}" for x in rel.tolist()) + f" | mean {rel.mean():.3f}")
print("K clipped fraction with scale 1.0:", f"{(K.abs() > E4M3_MAX).float().mean():.4f}")
```

**Output (my run):**
```
bytes/token: FP16 131072, FP8 65536; per-head fp32 scales cost 2048 bytes in total (not per token)
FP16:   450,560 cached tokens in a 55.0 GiB pool
FP8 :   901,120 cached tokens in a 55.0 GiB pool

relative attention-output error per head (head std 0.002 ... 300):
scale 1.0 (uncalibrated default): 0.020 0.022 0.030 0.039 0.061 0.134 0.076 1.451 | mean 0.229
one per-tensor scale           : 0.023 0.023 0.030 0.038 0.069 0.239 0.103 0.026 | mean 0.069
per-head scale                 : 0.027 0.024 0.042 0.033 0.073 0.058 0.129 0.026 | mean 0.051
K clipped fraction with scale 1.0: 0.0167
```

**Follow-ups:**
- *Is per-head always better than per-tensor?* Not in this toy: mean error 0.051 vs 0.069, but individual middle heads (for example the 20-std head, 0.129 vs 0.103) came out worse; those gaps are noise from one random draw. The robust finding is clipping with an uncalibrated scale.
- *Why not INT4 KV?* Fewer bits means more error and more kernel complexity; it is an option some stacks offer, but validate harder.
- *Does it combine with weight quantization?* Yes, they act on different memory (weights vs cache), so you validate the combination, not each alone.

**Common mistakes:** assuming FP8 KV is free; shipping with default scale 1.0; calibrating on data that does not look like production; measuring only short-context quality; forgetting to re-measure speed.

### Q23 ⭐⭐ 🟡 FP8 and W8A8 serving: what are the E4M3 and E5M2 formats, which GPUs support them natively, how do static vs dynamic scaling and SmoothQuant-style outlier handling work, and when do you prefer FP8 over INT4 weight-only?
**Asked at:** inference-platform teams, AI labs; interview-prep guide, not a candidate report lists FP8, INT8 and INT4 formats
**Say this first (1 line):** FP8 is an 8-bit floating-point format with two flavours, E4M3 (more precision, max 448) for weights and activations and E5M2 (more range, max 57,344) for gradients, and W8A8 means both weights and activations are 8-bit so the matmul itself runs in low precision on hardware with FP8 tensor cores.

**Then explain:**
- **Formats** (defined in the FP8 formats paper, arXiv 2209.05433, abstract read): E4M3 has 4 exponent and 3 mantissa bits; E5M2 has 5 and 2. I decoded all 256 codes in code: E4M3 has 254 finite codes, max 448, smallest subnormal 0.00195; E5M2 has 248 finite codes, max 57,344, smallest subnormal 1.5e-5. The E4M3 variant used in practice has one NaN pattern and no infinity (the OCP convention, from memory, check).
- **Hardware:** native FP8 matmul needs recent GPUs; the vLLM quantization docs read on 2026-10-24 list FP8 W8A8 for Ada, Hopper and AMD parts (tables change by release, check live docs). On older GPUs, FP8 may run as weight-only with dequantization, saving memory but not compute.
- **Static vs dynamic scaling:** static uses a fixed activation scale from calibration, so it is fast but wrong if live activations drift; dynamic computes the scale from each batch or token, which costs a little compute but adapts.
- **SmoothQuant-style smoothing:** a few activation channels have huge outliers that waste the 8-bit range; SmoothQuant divides those channels by a per-channel factor and multiplies the matching weight rows, an exact rewrite that moves the difficulty into the weights. The authors report up to 1.56x speed and 2x memory (their stated setups, abstract read).
- **FP8 vs INT4 weight-only:** FP8 W8A8 speeds compute-bound work (prefill, big batches) and halves memory; INT4 weight-only quarters weight memory and helps memory-bound decode at small batch, but does not accelerate compute-bound prefill and needs dequantization kernels (Q8). Prefer FP8 when you have native hardware and a throughput-heavy workload; prefer INT4 when memory is the constraint or the hardware lacks FP8.

**Example:** in my toy (synthetic activations), a static FP8 scale calibrated at activation scale 1 gives 0.0370 relative output error on a matching batch, 0.7012 when live activations are 10x larger and 0.9837 at 200x (values saturate at 448), while dynamic scaling stays near 0.037. For INT8 W8A8 with one channel 80x larger, smoothing with alpha 0.5 cuts relative error from 0.0524 to 0.0132.

**Code:** (E4M3 and E5M2 decoded by brute force; synthetic activations)
```python
# FP8 formats decoded by brute force, static vs dynamic scaling, and SmoothQuant-style smoothing. Data are SYNTHETIC.
import numpy as np
rng = np.random.default_rng(0)

def decode(code, ebits, mbits, bias, has_inf):
    s = -1.0 if code >> (ebits + mbits) else 1.0
    e = (code >> mbits) & ((1 << ebits) - 1); m = code & ((1 << mbits) - 1)
    if has_inf and e == (1 << ebits) - 1: return s * np.inf if m == 0 else np.nan      # E5M2: IEEE-style inf/NaN
    if not has_inf and e == (1 << ebits) - 1 and m == (1 << mbits) - 1: return np.nan   # E4M3: one NaN pattern, no inf
    if e == 0: return s * (m / (1 << mbits)) * 2.0 ** (1 - bias)                         # subnormal
    return s * (1 + m / (1 << mbits)) * 2.0 ** (e - bias)

for name, eb, mb, bias, inf in (("E4M3", 4, 3, 7, False), ("E5M2", 5, 2, 15, True)):
    vals = np.array([decode(c, eb, mb, bias, inf) for c in range(256)])
    fin = vals[np.isfinite(vals)]; pos = np.sort(fin[fin > 0])
    print(f"{name}: finite codes {len(fin)}, max {pos.max():g}, min subnormal {pos.min():g}, min normal {2.0**(1-bias):g}")

E4M3 = np.array(sorted({decode(c, 4, 3, 7, False) for c in range(256)} - {np.nan}))
E4M3 = E4M3[np.isfinite(E4M3)]
def fp8(x):                                           # round to nearest representable E4M3 value, saturate at 448
    x = np.clip(x, -448, 448)
    i = np.clip(np.searchsorted(E4M3, x), 1, len(E4M3) - 1)
    lo, hi = E4M3[i - 1], E4M3[i]
    return np.where(np.abs(x - lo) <= np.abs(hi - x), lo, hi)

# ---- static vs dynamic activation scaling (per-tensor), activations with a distribution shift ------
W = rng.normal(0, 0.02, (256, 256))
def batch(scale): return rng.normal(0, 1, (64, 256)) * scale
calib = batch(1.0)                                     # calibration data
static_scale = np.abs(calib).max() / 448
def run(X, scale):
    Xq = fp8(X / scale) * scale; Wq = fp8(W / (np.abs(W).max() / 448)) * (np.abs(W).max() / 448)
    return np.linalg.norm(Xq @ Wq - X @ W) / np.linalg.norm(X @ W)
print("\nactivation scale of live batch vs calibration (FP8 W8A8 relative output error):")
for mult in (1.0, 10.0, 200.0):
    X = batch(mult)
    dyn = np.abs(X).max() / 448
    print(f"live batch x{mult:5.0f}: static scale {run(X, static_scale):.4f} | dynamic scale {run(X, dyn):.4f}")

# ---- SmoothQuant-style smoothing with INT8 W8A8 (per-tensor), where one activation channel is an outlier ----
X = rng.normal(0, 1, (128, 64)); X[:, 5] *= 80                 # outlier channel
W2 = rng.normal(0, 0.05, (64, 64))
def int8_q(a):
    s = np.abs(a).max() / 127; return np.round(a / s).clip(-127, 127) * s
def err(X, W2): return np.linalg.norm(int8_q(X) @ int8_q(W2) - X @ W2) / np.linalg.norm(X @ W2)
alpha = 0.5
s = np.abs(X).max(axis=0) ** alpha / np.abs(W2).max(axis=1) ** (1 - alpha)    # per input channel
Xs, Ws = X / s, W2 * s[:, None]
assert np.allclose(Xs @ Ws, X @ W2)                                           # smoothing is mathematically exact
print(f"\nINT8 W8A8 per-tensor error, outlier channel x80: plain {err(X, W2):.4f} -> smoothed (alpha 0.5) {err(Xs, Ws):.4f}")
print(f"max|X| per channel before: {np.abs(X).max(0).max():.1f} vs median channel {np.median(np.abs(X).max(0)):.1f};"
      f" after: {np.abs(Xs).max(0).max():.1f} vs {np.median(np.abs(Xs).max(0)):.1f}")
```

**Output (my run):**
```
E4M3: finite codes 254, max 448, min subnormal 0.00195312, min normal 0.015625
E5M2: finite codes 248, max 57344, min subnormal 1.52588e-05, min normal 6.10352e-05

activation scale of live batch vs calibration (FP8 W8A8 relative output error):
live batch x    1: static scale 0.0370 | dynamic scale 0.0377
live batch x   10: static scale 0.7012 | dynamic scale 0.0375
live batch x  200: static scale 0.9837 | dynamic scale 0.0366

INT8 W8A8 per-tensor error, outlier channel x80: plain 0.0524 -> smoothed (alpha 0.5) 0.0132
max|X| per channel before: 244.7 vs median channel 2.8; after: 6.4 vs 0.6
```

**Follow-ups:**
- *Why not E5M2 for activations?* Two mantissa bits give coarser steps; E4M3's finer precision matters more once scaling handles range.
- *What is alpha in SmoothQuant?* It balances how much of the difficulty moves to the weights (0.5 splits evenly; the paper tunes it per model, from memory, check).
- *What must you validate?* Task quality, long-context retrieval and the speedup on your GPU (Q10).

**Common mistakes:** assuming FP8 speeds up every GPU; using a static scale without a drift check; confusing E4M3 with E5M2 roles; treating SmoothQuant as lossy (the rewrite is exact, the later rounding is not); expecting FP8 to help decode as much as it helps prefill.

### Q24 ⭐⭐ 🟡 Speculative decoding variants: draft model vs n-gram or prompt lookup vs Medusa heads vs EAGLE feature-level drafting. What does each need (training, memory), and why does speedup fall at high batch sizes? (Part 1 Q45 links multi-token prediction.)
**Asked at:** inference-platform teams, AI labs; interview-prep guide, not a candidate report lists Medusa, EAGLE and lookahead
**Say this first (1 line):** All variants propose several next tokens cheaply and let the target verify them in one pass; they differ in who drafts (a small model, the prompt itself, extra heads, or a feature-level head) and what that costs in training and memory, and the gain shrinks at high batch size because verification stops being free.

**Then explain:**
- **Draft model** (Leviathan et al., Chen et al.): a smaller model of the same vocabulary proposes k tokens, the target verifies in parallel; the output distribution is unchanged (Q11). Needs a second model's weights and KV cache, and a draft that agrees often with the target.
- **N-gram / prompt lookup:** proposes tokens by finding the recent n-gram earlier in the prompt or output and copying what followed. No training and almost no memory; works when outputs quote the prompt (editing, RAG, code), useless on novel text.
- **Medusa:** extra decoding heads on the target predict several future tokens, verified using tree attention. The Medusa authors report over 2.2x for Medusa-1 and 2.3-3.6x for Medusa-2 (their setups; heads need training, and Medusa-2 also fine-tunes the backbone, from memory, check).
- **EAGLE:** drafts at the feature level (the target's hidden states) with a small trained head; the authors report 2.7-3.5x latency speedup on LLaMA2-Chat 70B (their setup, abstract read).
- **Why speedup falls at high batch:** at small batch decode is memory-bound, so verifying k+1 tokens per sequence costs about the same as one token; at large batch the step becomes compute-bound, so verification does k+1 times the work and rejected tokens are wasted compute. Expected tokens per step is (1 - alpha^(k+1)) / (1 - alpha) for acceptance alpha (iid assumption).
- Real acceptance varies per token and per domain, so measure it on your traffic.

**Example:** n-gram drafting (k = 4) on a synthetic copy-heavy stream emits 3.38 tokens per target step; on novel random tokens 1.00. In the roofline toy (assumed 1.0 ms weight-read, 0.02 ms per token, draft step at 5% of a target step, k = 4), acceptance 0.8 gives a 2.80x speedup at batch 1 and 8, 1.87x at 16, 0.99x at 32, and 0.65x at 64 and beyond, i.e. slower than plain decoding.

**Code:** (n-gram drafter on synthetic token streams; roofline toy with assumed constants; closed form checked by Monte Carlo)
```python
# (1) n-gram / prompt-lookup drafting on toy token streams; (2) why speedup falls with batch size (roofline toy).
# Token streams are SYNTHETIC; hardware numbers in part 2 are ASSUMED.
import random
random.seed(1)

def ngram_draft(context, k, n=2):
    """Prompt lookup: find the last n tokens earlier in the context and propose the k tokens that followed."""
    key = tuple(context[-n:])
    for i in range(len(context) - n - 1, -1, -1):
        if tuple(context[i:i + n]) == key:
            return context[i + n:i + n + k]
    return []

def run(stream, prompt_len, k=4):
    """'Target' = the stream itself (greedy). Count tokens emitted per verification step."""
    pos, steps = prompt_len, 0
    while pos < len(stream):
        draft = ngram_draft(stream[:pos], k)
        acc = 0
        while acc < len(draft) and pos + acc < len(stream) and draft[acc] == stream[pos + acc]: acc += 1
        pos += acc + 1                        # accepted tokens plus one token from the target itself
        steps += 1
    return (len(stream) - prompt_len) / steps

base = [random.randrange(50) for _ in range(40)]
copy_heavy = base + base[5:35] + base[10:38] + base[0:30]                   # output re-uses prompt text (like editing/RAG quoting)
random_text = base + [random.randrange(50) for _ in range(90)]               # no reuse
print("n-gram drafting, k=4, tokens emitted per target step (1.0 = no gain):")
print(f"  copy-heavy output : {run(copy_heavy, 40):.2f}")
print(f"  novel output      : {run(random_text, 40):.2f}")

# ---- speedup vs batch size: verification of (k+1) tokens per sequence costs more as the batch becomes compute-bound
def step_time(tokens_in_step, t_mem=1.0, t_per_token=0.02):
    # roofline toy (units: ms): max(memory time to read weights, compute time proportional to tokens processed)
    return max(t_mem, t_per_token * tokens_in_step)

def speedup(alpha, k, batch, draft_cost=0.05):
    e_tokens = (1 - alpha ** (k + 1)) / (1 - alpha)            # expected tokens per step per sequence (i.i.d. acceptance)
    t_plain = step_time(batch)                                  # one token per sequence
    t_spec = k * draft_cost * step_time(batch) + step_time(batch * (k + 1))   # k cheap draft steps + one verify of k+1 tokens
    return e_tokens * t_plain / t_spec

# check the closed form E = (1 - a^(k+1)) / (1 - a) against Monte Carlo (iid acceptance per draft token)
def mc(alpha, k, n=200000):
    tot = 0
    for _ in range(n):
        a = 0
        while a < k and random.random() < alpha: a += 1
        tot += a + 1
    return tot / n
print(f"\nexpected tokens/step, alpha=0.8 k=4: formula {(1-0.8**5)/(1-0.8):.3f}, Monte Carlo {mc(0.8, 4):.3f}")
print("assumed: weight-read time 1.0 ms, compute 0.02 ms per token, draft step = 5% of a target step, k=4")
print("batch | speedup at acceptance 0.8 | at 0.5")
for b in (1, 8, 16, 32, 64, 512):
    print(f"{b:5d} | {speedup(0.8, 4, b):10.2f}                | {speedup(0.5, 4, b):.2f}")
```

**Output (my run):**
```
n-gram drafting, k=4, tokens emitted per target step (1.0 = no gain):
  copy-heavy output : 3.38
  novel output      : 1.00

expected tokens/step, alpha=0.8 k=4: formula 3.362, Monte Carlo 3.361
assumed: weight-read time 1.0 ms, compute 0.02 ms per token, draft step = 5% of a target step, k=4
batch | speedup at acceptance 0.8 | at 0.5
    1 |       2.80                | 1.61
    8 |       2.80                | 1.61
   16 |       1.87                | 1.08
   32 |       0.99                | 0.57
   64 |       0.65                | 0.37
  512 |       0.65                | 0.37
```

**Follow-ups:**
- *Does it change quality?* The draft-model and sampling variants with correct verification keep the target distribution (Q41 checks this); lossy "typical acceptance" variants exist, so read the docs.
- *Which variant first?* N-gram if outputs quote inputs (free to try); a draft model if one exists with matching vocabulary; Medusa or EAGLE when you can afford training heads and run mostly small batches. All must be benchmarked against your traffic.
- *Link to multi-token prediction?* Part 1 Q45 explains how MTP heads can serve as drafters.

**Common mistakes:** quoting 2-3x as universal; benchmarking at batch 1 and deploying at batch 64; forgetting the draft model's memory and KV; assuming acceptance rates transfer between domains; ignoring that verification cost grows in the compute-bound regime.

### Q25 ⭐⭐ 🟡 Multi-LoRA serving: how do engines keep one base model and many adapters (batched adapter kernels, adapter paging as in S-LoRA and Punica, max loaded adapters, dynamic loading), and what limits latency and adapter count? (Part 4 Q32 covers merged vs unmerged.)
**Asked at:** GenAI startups, platform teams, multi-tenant SaaS; interview-prep guide, not a candidate report lists multi-LoRA serving
**Say this first (1 line):** Keep one copy of the base model in GPU memory and many small LoRA adapters beside it. In each batch the base matmul runs once for everyone and a small per-request low-rank delta is added, picked by adapter id. The limit is adapter memory, swap-in latency and kernel efficiency, not the base model.

**Then explain:**
- **The maths of one batch:** for a layer, y = x W + (x A_i) B_i, where request i uses adapter i. W is shared, so it is one big GEMM. The deltas are small, so engines gather each request's A and B by adapter id and run batched low-rank kernels (the idea in Punica). In the toy below the batched result matches "merge the adapter for each request separately" to about 1.8e-14 in float64.
- **Paging adapters:** S-LoRA keeps adapters in host memory and pulls the ones needed into GPU memory, with unified paging for adapter weights and KV cache. Reported by the authors in the abstracts I opened (their setups): Punica about 12x throughput and about 2 ms extra per token; S-LoRA thousands of adapters and up to 4x over naive baselines. Treat these as the authors' numbers, not what you will see.
- **Engine knobs (vLLM docs as read on 2026-10-24, check live docs):** `--enable-lora`, `--max-lora-rank`, and a max-loaded-adapters setting (`max_loras`); runtime load and unload endpoints exist but are gated behind an environment variable with a security warning. The prefix-cache hash includes the LoRA id, so adapters do not share cached prefixes.
- **What limits adapter count:** memory for loaded adapters, reserved up front from the max rank and max loaded settings (check how your engine pads), plus KV cache competing for the same GPU memory. In the toy a rank-16 adapter on four 4096x4096 projections in 32 layers is 16.78M parameters, 33.6 MB in fp16, 0.24% of a 7B base. About 298 such adapters fit in 10 GB; rank 64 gives only about 74.
- **What limits latency:** the extra low-rank kernels (small, memory-gather heavy, so efficiency is worse than a big GEMM), many distinct adapters in one batch, and misses. A miss means loading from host memory or disk before the request can run.
- **Traffic shape decides the cache:** with synthetic Zipf traffic (s=1.1) over 1000 adapters, an LRU of 64 slots hit 60.5% and 256 slots 80.2%; with uniform traffic 64 slots hit only 6.5%.
- **Versus merged weights:** a merged adapter has zero extra latency but needs a model copy per replica. Part 4 Q32 has the decision; this answer is the engine side.

**Example:** A SaaS product has 1000 customers, each with a rank-16 adapter on the 7B-like shape. In fp16 that is 1000 x 33.6 MB, about 33.6 GB: keep all of it in host memory and 64 hot adapters in GPU memory (about 2.1 GB). In the toy with Zipf traffic that gives a 60.5% hit rate, so about 4 in 10 requests wait for an adapter load unless you raise slots, pre-load known hot tenants or route a tenant's requests to the replica that already holds its adapter. Traffic shape and numbers here are synthetic.

**Code:** (run with `python3 -I`; numpy only, toy shapes (the 7B-like sizes in section 2 are assumed). Not a GPU measurement.)
```python
# TOY multi-LoRA serving maths (numpy only). Shapes are ASSUMED Llama-7B-like; nothing here is a GPU measurement.
import numpy as np
rng = np.random.default_rng(0)

# 1) One batch, many adapters: base GEMM for everyone + per-request low-rank delta gathered by adapter id.
d_in, d_out, r, n_adapters, batch = 64, 64, 4, 6, 10
W = rng.normal(size=(d_in, d_out))
A = rng.normal(size=(n_adapters, d_in, r)) * 0.1      # per-adapter down-projection
B = rng.normal(size=(n_adapters, r, d_out)) * 0.1     # per-adapter up-projection
x = rng.normal(size=(batch, d_in))
aid = rng.integers(0, n_adapters, size=batch)         # which adapter each request uses

y_loop = np.stack([x[i] @ (W + A[aid[i]] @ B[aid[i]]) for i in range(batch)])   # reference: merge per request
base = x @ W                                                                     # shared base matmul, one GEMM
delta = np.einsum('bi,bir->br', x, A[aid])                                       # gather A by id, (batch, r)
delta = np.einsum('br,bro->bo', delta, B[aid])                                   # gather B by id, (batch, d_out)
y_batched = base + delta
print("batched == per-request merged:", np.allclose(y_loop, y_batched), " max abs diff %.2e" % np.abs(y_loop - y_batched).max())

# 2) Adapter size and how many fit in a memory budget (ASSUMED 7B-like: hidden 4096, 32 layers, 4 square projections q,k,v,o).
hidden, layers, mods = 4096, 32, 4
for rank in (8, 16, 64):
    params = layers * mods * rank * (hidden + hidden)
    mb = params * 2 / 1e6                              # fp16 = 2 bytes
    print(f"rank {rank:2d}: {params/1e6:6.2f}M params = {mb:7.1f} MB fp16; per 10 GB of adapter memory: {int(10e9 // (params*2))} adapters")
base_params = 7e9
print("rank 16 adapter / 7B base params = %.3f%%" % (100 * layers*mods*16*2*hidden / base_params))

# 3) Adapter cache with LRU and Zipf popularity (max loaded adapters = slots). Hit rate decides how often a request waits for a load.
def lru_hit_rate(n_adapters, slots, n_req=20000, s=1.1, seed=1):
    g = np.random.default_rng(seed)
    p = 1.0 / np.arange(1, n_adapters + 1) ** s; p /= p.sum()
    reqs = g.choice(n_adapters, size=n_req, p=p)
    cache, hits = [], 0
    for a in reqs:
        if a in cache: hits += 1; cache.remove(a)
        elif len(cache) >= slots: cache.pop(0)          # evict least recently used (front)
        cache.append(a)
    return hits / n_req
print("LRU hit rate, 1000 adapters, Zipf s=1.1 (SYNTHETIC traffic):")
for slots in (4, 16, 64, 256):
    print(f"  slots {slots:3d}: hit rate {lru_hit_rate(1000, slots):.3f}")
print("  uniform traffic, 64 slots:", end=" ")
g = np.random.default_rng(2); reqs = g.integers(0, 1000, 20000); cache, hits = [], 0
for a in reqs:
    if a in cache: hits += 1; cache.remove(a)
    elif len(cache) >= 64: cache.pop(0)
    cache.append(a)
print(f"hit rate {hits/20000:.3f}")
```
**Output (my run):**
```
batched == per-request merged: True  max abs diff 1.78e-14
rank  8:   8.39M params =    16.8 MB fp16; per 10 GB of adapter memory: 596 adapters
rank 16:  16.78M params =    33.6 MB fp16; per 10 GB of adapter memory: 298 adapters
rank 64:  67.11M params =   134.2 MB fp16; per 10 GB of adapter memory: 74 adapters
rank 16 adapter / 7B base params = 0.240%
LRU hit rate, 1000 adapters, Zipf s=1.1 (SYNTHETIC traffic):
  slots   4: hit rate 0.166
  slots  16: hit rate 0.387
  slots  64: hit rate 0.605
  slots 256: hit rate 0.802
  uniform traffic, 64 slots: hit rate 0.065
```

**Follow-ups:**
- *Different ranks in one batch?* Engines usually cap the rank and may pad to it, so a single large-rank adapter can tax everyone; check your engine's behaviour.
- *Can adapters share the prefix cache?* Not in vLLM-style hashing, because the LoRA id is part of the block hash.
- *Is dynamic loading safe?* Only from trusted storage. The vLLM docs attach a security warning and an environment-variable gate to the endpoints.

**Common mistakes:** Saying the delta is free because it is small; ignoring that adapter memory competes with KV cache; promising thousands of adapters with no hit-rate or load-latency analysis; assuming adapters share prefix-cache hits; treating Punica and S-LoRA headline speedups as expected results.

### Q26 ⭐⭐ 🟡 What does structured or constrained decoding cost at serving time (grammar compilation, per-token masking, batch interaction, first-request latency), and how do engines such as vLLM and SGLang reduce it? (Part 3 Q22 covers the mechanism; Q40 the p99 problem.)
**Asked at:** product companies, GenAI startups; interview-prep guide, not a candidate report lists guided decoding and slow first requests
**Say this first (1 line):** Constrained decoding costs three things: a one-off grammar-to-automaton compile, a mask over the vocabulary at every token, and a batch where every request has its own mask. Engines cut it by caching compiled grammars, building masks per automaton state and doing the work off the critical path, but a new schema still makes its first request slow.

**Then explain:**
- **Compile cost:** a schema becomes a regex or grammar and then an automaton, and the work grows with schema size. In the toy a word-list grammar has 22, 34 and 82 states for at most 2, 8 and 32 words, and filling the full per-state token-mask table costs 73,717, 116,347 and 286,867 character-steps.
- **Per-token masking:** the naive way rescans the whole vocabulary at every step (about 3,145 character-steps at the start state, 3,000-token toy vocabulary). Precomputing a table per state turns that into a lookup. Real engines use bitmask-based backends; the vLLM docs I read list xgrammar and guidance as backends and choice, regex, JSON, grammar and structural-tag modes.
- **Batch interaction:** each request sits in a different automaton state, so the logits mask is a (batch, vocab) array gathered per row. If it is built on the CPU every step it can serialise with the GPU forward pass unless it is overlapped. In the toy, 8 requests had 1 to 16 allowed tokens each out of 3,001.
- **First-request latency:** compile happens when a new schema first appears. With the same schema the table is built once; with a new schema per request you pay it every time. Toy: 116,347 vs 11,634,700 character-steps for 100 requests. Part 3 Q40 covers the p99 fixes (cache by schema hash, pre-warm common schemas, simplify schemas, compile off the request path).
- **How engines reduce it:** cache compiled grammars, lazy or per-state mask construction, token tries or bitmasks, and jump-forward (when the grammar forces the next characters, emit them without a model step per token; SGLang's paper describes compressed finite state machines for this, from memory of the paper, check). The SGLang abstract's 6.4x is for its whole system across tasks, not structured output alone.
- **Guarantees:** the output is valid only if generation finishes; hitting `max_tokens` mid-object still gives invalid JSON. Constraints do not make the content correct. Part 3 Q22 has the mechanism.
- **API drift, hedged:** as of the vLLM docs read on 2026-10-24 the older `guided_*` request fields were removed in v0.12.0 in favour of the structured-outputs interface; check live docs.

**Example:** Eight requests are mid-generation at different positions in the same JSON grammar. One is inside a digit run (10 digits plus a comma allowed), one is forced to emit a literal quote (1 token allowed). The engine gathers each row's mask from the per-state table, applies one batched masked softmax, and the cost per step is a lookup, not a rescan of 3,000 tokens. A ninth request with a never-seen schema waits for its own compile first.

**Code:** (run with `python3 -I`; stdlib and numpy; toy character-level automaton with a synthetic vocabulary, costs counted in character-steps (deterministic, not seconds). When I first ran it, five automaton states had an empty mask because my synthetic vocabulary lacked the single characters i, d, t, g, s; I added them. Real tokenisers have byte fallback, but token boundaries that do not line up with the grammar are a classic source of constrained-decoding bugs.)
```python
# TOY constrained-decoding cost model: hand-built DFA for {"id":<digits>,"tags":[w(,w)*]} with at most m words, w = [abc]+.
# Synthetic vocabulary, random "logits", no LLM. Costs are counted in character-steps (deterministic), not seconds.
import re, random
import numpy as np
random.seed(0); rng = np.random.default_rng(0)

def build_dfa(m):
    T = [{}]                                   # T[state] = {char: next_state}; state 0 is the start
    def new(): T.append({}); return len(T) - 1
    def lit(cur, text):
        for ch in text: nxt = new(); T[cur][ch] = nxt; cur = nxt
        return cur
    cur = lit(0, '{"id":')
    d1 = new()
    for c in "0123456789": T[cur][c] = d1; T[d1][c] = d1
    cur = lit(d1, ',"tags":[')
    end = new(); close = new(); T[close]['}'] = end
    for k in range(m):
        b = new()
        for c in "abc": T[cur][c] = b; T[b][c] = b
        T[b][']'] = close
        if k < m - 1: nxt = new(); T[b][','] = nxt; cur = nxt
    return T, end

chars = list('{}[]":,0123456789abcidtgs')
vocab = set(chars)
while len(vocab) < 3000: vocab.add(''.join(random.choice(chars) for _ in range(random.randint(2, 6))))
V = sorted(vocab) + ["<eos>"]; EOS = len(V) - 1

def walk(T, s, tok):                           # returns (end_state or None, chars_examined)
    n = 0
    for ch in tok:
        n += 1
        s = T[s].get(ch)
        if s is None: return None, n
    return s, n

def token_mask(T, end, s):                     # (bool mask over vocab, character-steps spent building it)
    mask = np.zeros(len(V), dtype=bool); ops = 0
    for i, tok in enumerate(V[:-1]):
        e, n = walk(T, s, tok); ops += n; mask[i] = e is not None
    mask[EOS] = (s == end)
    return mask, ops

def generate(T, end, masks, rng, cap=300):     # sample under the mask; masks[s] is the precomputed table row
    s, out = 0, []
    for _ in range(cap):
        logits = rng.normal(size=len(V)); logits[~masks[s]] = -np.inf
        i = int(np.argmax(logits + rng.gumbel(size=len(V))))   # Gumbel-max = sampling from softmax(masked logits)
        if i == EOS: return ''.join(out), True
        out.append(V[i]); s, _ = walk(T, s, V[i])
    return ''.join(out), False

print("Grammar compilation (state count and one-off mask-table cost grow with schema size):")
for m in (2, 8, 32):
    T, end = build_dfa(m)
    total = sum(token_mask(T, end, s)[1] for s in range(len(T)))
    print(f"  max words {m:2d}: DFA states {len(T):3d}, full table build = {total:9,d} character-steps")

m = 8; T, end = build_dfa(m)
tables = {s: token_mask(T, end, s) for s in range(len(T))}
masks = {s: v[0] for s, v in tables.items()}; table_cost = sum(v[1] for v in tables.values())
one_step = tables[0][1]
print(f"\nNaive per-step masking (rescan vocab of {len(V)-1} tokens every step): about {one_step:,d} character-steps per token per request")
print(f"Precomputed table (m={m}): {table_cost:,d} one-off, then a lookup per token")

pat = re.compile(r'\{"id":[0-9]+,"tags":\[[abc]+(,[abc]+){0,%d}\]\}' % (m - 1))
done = ok = steps = 0
for _ in range(300):
    text, fin = generate(T, end, masks, rng)
    done += fin; ok += fin and bool(pat.fullmatch(text))
print(f"\n300 constrained samples: finished {done}, fully match the regex {ok}  (validity guaranteed whenever generation finishes)")

# Unconstrained random tokens for contrast
bad = sum(not pat.fullmatch(''.join(V[j] for j in rng.integers(0, len(V) - 1, size=6))) for _ in range(300))
print(f"Unconstrained random 6-token strings that fail the pattern: {bad}/300")

# Batch interaction: each request is in a different DFA state, so the batch needs a (batch, vocab) mask gathered per row.
states = rng.integers(0, len(T), size=8)
M = np.stack([masks[s] for s in states]); print("batch mask shape:", M.shape, " allowed tokens per row:", M.sum(axis=1).tolist())

# Amortisation: a cached grammar is compiled once; per-request-new schema pays every time.
N = 100
print(f"\nCharacter-steps for {N} requests: shared schema, table built once = {table_cost:,d}; new schema per request = {N*table_cost:,d}")
print(f"Naive per-step rescan for {N} requests x 40 tokens = {N*40*one_step:,d}")
```
**Output (my run):**
```
Grammar compilation (state count and one-off mask-table cost grow with schema size):
  max words  2: DFA states  22, full table build =    73,717 character-steps
  max words  8: DFA states  34, full table build =   116,347 character-steps
  max words 32: DFA states  82, full table build =   286,867 character-steps

Naive per-step masking (rescan vocab of 3000 tokens every step): about 3,145 character-steps per token per request
Precomputed table (m=8): 116,347 one-off, then a lookup per token

300 constrained samples: finished 300, fully match the regex 300  (validity guaranteed whenever generation finishes)
Unconstrained random 6-token strings that fail the pattern: 300/300
batch mask shape: (8, 3001)  allowed tokens per row: [1, 2, 1, 2, 16, 14, 4, 1]

Character-steps for 100 requests: shared schema, table built once = 116,347; new schema per request = 11,634,700
Naive per-step rescan for 100 requests x 40 tokens = 12,580,000
```

**Follow-ups:**
- *How do you keep p99 under a per-request schema?* See Part 3 Q40: cache, pre-warm, simplify, and compile asynchronously.
- *Does masking change quality?* It can: forcing a format can push probability mass toward a worse but legal token. Evaluate with and without the constraint.
- *Why not just validate and retry?* That costs extra full generations and retries can repeat the same failure; constraints trade a fixed overhead for a guarantee.

**Common mistakes:** Blaming the model for slow first requests when it is grammar compilation; compiling a schema per request; assuming constraints guarantee valid output when generation is truncated; forgetting the batch mask must be per row; quoting a framework's headline speedup as the cost of constraints.

### Q27 ⭐⭐ 🟡 Autoscaling and cold starts for GPU-backed LLM replicas: which signals scale well (queue depth, KV-cache usage, running requests) vs which mislead (GPU utilisation), what dominates cold start (weight download and load), and how do you hedge? (Book 4 owns generic Kubernetes autoscaling.)
**Asked at:** product companies, GCCs, platform teams; interview-prep guide, not a candidate report lists autoscaling signals and cold starts
**Say this first (1 line):** Scale on signals that see work waiting (queue depth, running requests per replica, KV-cache usage), not GPU utilisation, because with continuous batching a replica looks busy at modest load. Plan for cold starts that last minutes at large model sizes, keep headroom, and scale in slowly.

**Then explain:**
- **Why GPU utilisation misleads:** it mostly says some kernel was running. A replica can read near 100% at a fraction of its real capacity, so a util-based policy either scales to the maximum and never scales in, or has no idea how close you are to queueing. In the toy it did exactly that.
- **Better signals:** waiting-queue length and queue time, running requests per replica, `kv_cache_usage_perc`-style KV usage, and TTFT percentiles. The vLLM metrics page I read lists queue time, running and waiting request counts and KV-cache usage (check live docs for names).
- **Cold start is dominated by weights:** seconds = bytes / read bandwidth, plus engine start-up, graph capture and warm-up that I did not model. Assumed round bandwidths: a 14 GB 7B fp16 model takes 70 s at 0.2 GB/s, 14 s at 1 GB/s, 2.8 s at 5 GB/s; a 140 GB 70B fp16 model 700 s, 140 s and 28 s; 35 GB at 4-bit 175 s, 35 s and 7 s.
- **Cold start is longer than your ramp:** if a new replica takes longer than demand takes to rise, every reactive policy queues. In the toy (assumed 120 s cold start, 60 s ramp) the best reactive policy still built a queue.
- **Hedges:** a minimum replica floor with headroom, scheduled or predictive scaling for known peaks, weights cached on local disk or a shared fast volume, smaller or quantized weights, a warm pool, slow scale-in with a stabilisation window, load shedding (Q29) while new replicas start, and an API or smaller-model fallback. Book 4 owns the Kubernetes mechanics.

**Example:** From the run (all inputs assumed: 10 req/s per replica, demand 40 -> 160 req/s over 60 s, 120 s cold start, 16 replicas needed at peak):

| policy | peak queue | seconds with queue > 100 | replica-hours | max replicas |
|---|---|---|---|---|
| GPU util > 0.8 | 0 | 0 | 18.79 | 40 |
| queue depth | 10,400 | 177 | 7.43 | 40 |
| target load 70% of capacity | 11,630 | 345 | 6.08 | 22 |
| target load with headroom (35%) | 3,840 | 120 | 11.52 | 40 |

The util policy shows no queue only because it sat at the 40-replica cap, 3.1x the replica-hours of the 70% policy, and never scaled in. Headroom cut the peak queue from 11,630 to 3,840 for about 1.9x the replica-hours. Both effects come from my assumed numbers, not a real fleet.

**Code:** (run with `python3 -I`; stdlib only; one-second fluid simulation. Capacities, cold-start times, thresholds and bandwidths are assumed; the policy rules are my choices, so the table shows the shape, not a recommendation.)
```python
# TOY autoscaling simulation (stdlib only). All capacities, times and thresholds are ASSUMED, not measured.
# Fluid model, 1-second steps. Each replica serves CAP requests/s. A new replica takes COLD seconds before it serves.
CAP, COLD, T = 10.0, 120, 1800
def demand(t):                       # requests/s: calm 40, ramp to 160 at t=300..360, back down at t=1200
    if t < 300: return 40.0
    if t < 360: return 40.0 + (160 - 40) * (t - 300) / 60
    if t < 1200: return 160.0
    return 40.0

def util_signal(load_per_replica):   # "GPU utilisation": with continuous batching one replica looks ~busy even at modest load.
    return min(1.0, load_per_replica / (0.25 * CAP))   # ASSUMPTION: saturates at 25% of real capacity

def run(policy):
    ready = 6.0; pending = []       # ready replicas, list of (ready_at time, count)
    queue = 0.0; peak_q = 0.0; q_over = 0; rep_seconds = 0.0; max_rep = 0
    for t in range(T):
        for p in list(pending):
            if p[0] <= t: ready += p[1]; pending.remove(p)
        total = ready + sum(c for _, c in pending)
        arrivals = demand(t); served = min(ready * CAP, queue + arrivals)
        queue += arrivals - served; peak_q = max(peak_q, queue); q_over += queue > 100
        load = arrivals / max(ready, 1)
        want = total
        if policy == "gpu_util>0.8":
            if util_signal(load) > 0.8: want = total + 2       # keeps adding while util reads 'hot'
            elif util_signal(load) < 0.3: want = total - 1
        elif policy == "queue-depth":
            if queue > 20: want = total + max(1, int(queue / (CAP * COLD / 4)))   # backlog that would take a while to drain
            elif queue < 1 and arrivals < 0.6 * ready * CAP: want = total - 1
        elif policy == "target-load (req/s per replica = 70% cap)":
            want = max(1, -(-int(arrivals / (0.7 * CAP)) // 1))   # reacts to demand directly (still lags by COLD)
        elif policy == "target-load with headroom (35% cap)":
            want = max(1, -(-int(arrivals / (0.35 * CAP)) // 1))
        want = max(1, min(40, int(want)))
        if want > total: pending.append((t + COLD, want - total))
        elif want < total and ready > want: ready -= min(ready - want, 1)
        rep_seconds += ready; max_rep = max(max_rep, ready + sum(c for _, c in pending))
    return peak_q, q_over, rep_seconds / 3600, max_rep

print(f"ASSUMED: CAP={CAP}/s per replica, cold start {COLD}s, demand 40 -> 160 req/s ramp then back to 40. Needed at peak: {160/CAP:.0f} replicas.")
print(f"{'policy':44} peak queue  secs queue>100  replica-hours  max replicas")
for pol in ("gpu_util>0.8", "queue-depth", "target-load (req/s per replica = 70% cap)", "target-load with headroom (35% cap)"):
    pq, qo, rh, mr = run(pol)
    print(f"{pol:44} {pq:10.0f} {qo:15d} {rh:14.2f} {mr:13.0f}")

# What a cold start is made of: weight bytes / effective read bandwidth. Bandwidths are ASSUMED round numbers.
print("\nCold start, weights only (ASSUMED sizes and bandwidths): seconds = bytes / bandwidth")
for name, gb in (("7B fp16 (14 GB)", 14), ("70B fp16 (140 GB)", 140), ("70B 4-bit (35 GB)", 35)):
    print(f"  {name:20}", "  ".join(f"{bw:>4} GB/s: {gb/bw:6.1f}s" for bw in (0.2, 1, 5)))
```
**Output (my run):**
```
ASSUMED: CAP=10.0/s per replica, cold start 120s, demand 40 -> 160 req/s ramp then back to 40. Needed at peak: 16 replicas.
policy                                       peak queue  secs queue>100  replica-hours  max replicas
gpu_util>0.8                                          0               0          18.79            40
queue-depth                                       10400             177           7.43            40
target-load (req/s per replica = 70% cap)         11630             345           6.08            22
target-load with headroom (35% cap)                3840             120          11.52            40

Cold start, weights only (ASSUMED sizes and bandwidths): seconds = bytes / bandwidth
  7B fp16 (14 GB)       0.2 GB/s:   70.0s     1 GB/s:   14.0s     5 GB/s:    2.8s
  70B fp16 (140 GB)     0.2 GB/s:  700.0s     1 GB/s:  140.0s     5 GB/s:   28.0s
  70B 4-bit (35 GB)     0.2 GB/s:  175.0s     1 GB/s:   35.0s     5 GB/s:    7.0s
```

**Follow-ups:**
- *What is the scale-in rule?* Slow and conditional on empty queue and low running requests, because re-adding capacity costs a cold start.
- *Scale to zero?* Only for tolerant workloads; a multi-minute cold start is a failed request for chat.
- *Why not scale on tokens per second?* It is a fine output metric but lags and saturates; queue and KV usage lead it.

**Common mistakes:** Scaling on GPU utilisation or CPU; ignoring cold start when sizing the ramp; scaling in aggressively then paying a cold start; counting only weight download and forgetting engine start-up and warm-up; autoscaling with no cap or no floor.

### Q28 ⭐⭐ 🟡 Model routing and caching to cut cost: explicit routing, classifier routing and cascades, exact-match and semantic response caches, and the quality and safety risks of each. (Part 8 Q37 covers agent cost levers; Part 3 Q36 prompt-level cuts.)
**Asked at:** product companies, GenAI startups, GCCs; interview-prep guide, not a candidate report lists routing, cascades and caching
**Say this first (1 line):** Routing and caching cut cost by not sending every request to the biggest model or to any model at all, but each one trades quality or safety: a router can misroute hard queries, a cascade adds latency and depends on a good confidence signal, and a semantic cache can return a plausible wrong answer.

**Then explain:**
- **Explicit routing:** the product decides by feature or tenant (summaries to a small model, code to a large one). Cheap, predictable, no classifier error, but static.
- **Classifier routing:** a small model or rules estimate difficulty up front and pick one model. It adds a hop and fails silently on misroutes. Evaluate per slice (Part 9 has the eval method).
- **Cascades:** try the small model, escalate when a confidence or verifier score is low. Escalated requests pay both calls and extra latency, and everything depends on the scorer: a scorer that cannot tell right from wrong keeps wrong answers.
- **Exact-match cache:** key on the full prompt plus model, template, parameters and tenant; safe for deterministic requests. Risks: cross-tenant leaks if the key omits the tenant, stale answers, and caching non-deterministic or personalised outputs.
- **Semantic cache:** returns a stored answer for a similar query. Risks: false hits (one changed number or negation flips the correct answer), cross-tenant leakage, poisoning by a stored bad answer, bypassing newer guardrails, and stale facts. Use per-tenant namespaces, TTLs, a high threshold, and restrict it to low-stakes FAQ-like traffic.
- **Related levers:** provider prompt caching saves input cost on repeated prefixes and is not a response cache (Part 1 Q24; engine side in Q14). Agent cost levers are Part 8 Q37 and prompt-level cuts Part 3 Q36.

**Example:** Synthetic toy (cost units hypothetical: small = 1, large = 10; accuracies assumed): always small 0.620 at 1.00; always large 0.852 at 10.00; a classifier router 0.755 at 4.61 (estimate noise 0.1). A cascade with a decent scorer reaches 0.871 at 5.17, but that scorer is simulated from true correctness, so it is optimistic and its accuracy beating always-large is an artifact of the toy. A weak scorer kept wrong small answers on 12.9% of requests at 0.798 accuracy and 5.65 cost. For the semantic cache, "refund policy within 30 days" and "within 90 days" scored the same cosine (0.875) against a stored 30-day query as the true paraphrase "return policy within 30 days", so no threshold separates them.

**Code:** (run with `python3 -I`; numpy only; every input synthetic or assumed (difficulty, accuracies, scorer quality, costs, and a bag-of-words stand-in for embeddings).)
```python
# TOY routing, cascade and semantic-cache simulation (numpy only). Everything is SYNTHETIC: difficulty, accuracies,
# scorer noise and costs are assumed numbers; "cost" is in hypothetical units (small model = 1, large model = 10).
import numpy as np
rng = np.random.default_rng(0)
N = 20000
difficulty = rng.beta(2, 3, size=N)                    # 0 easy .. 1 hard (synthetic)
p_small = np.clip(0.98 - 0.9 * difficulty, 0.02, 1)    # ASSUMED chance the small model is right
p_large = np.clip(0.99 - 0.35 * difficulty, 0.02, 1)  # ASSUMED chance the large model is right
small_ok = rng.random(N) < p_small; large_ok = rng.random(N) < p_large
C_S, C_L = 1.0, 10.0
def report(name, ok, cost): print(f"{name:42} accuracy {ok.mean():.3f}   mean cost {cost.mean():5.2f}")
report("always small", small_ok, np.full(N, C_S))
report("always large", large_ok, np.full(N, C_L))

# Classifier router: noisy estimate of difficulty decides the model up front.
for noise in (0.1, 0.3):
    est = difficulty + rng.normal(0, noise, N)
    to_large = est > 0.45
    ok = np.where(to_large, large_ok, small_ok); cost = np.where(to_large, C_L, C_S)
    report(f"router (est noise {noise}, threshold 0.45)", ok, cost)

# Cascade: small answers first, a confidence scorer decides whether to escalate. Cost of escalated = small + large.
# The scorer is simulated from the true correctness plus noise, so even the "decent" one is optimistic (a real scorer has no oracle).
for name, quality in (("decent scorer (q=2.0)", 2.0), ("weak scorer (q=0.8)", 0.8)):
    conf = rng.normal(0, 1, N) + quality * (small_ok - 0.5)
    for th in (0.0, 1.0):
        esc = conf < th
        ok = np.where(esc, large_ok, small_ok); cost = C_S + esc * C_L
        wrong_kept = ((~esc) & (~small_ok)).mean()
        report(f"cascade, {name}, escalate if conf<{th}", ok, cost)
        print(f"{'':44} escalated {esc.mean():.2f}, wrong small answers kept {wrong_kept:.3f}")

# Semantic cache: bag-of-words vectors, cosine similarity against stored queries. Hit = similarity above threshold.
vocab = ["refund", "within", "days", "policy", "return", "item", "order", "shipping", "cost", "to", "india", "30", "90", "what", "is", "the"]
def emb(s):
    v = np.zeros(len(vocab)); 
    for w in s.lower().split():
        if w in vocab: v[vocab.index(w)] += 1
    return v / (np.linalg.norm(v) + 1e-9)
cached_q = "what is the refund policy within 30 days"; cached_ans = "30-day refund policy answer"
tests = [("what is the refund policy within 30 days", True),    # exact repeat: safe
         ("what is the refund policy within 90 days", False),   # differs in one critical token: answer differs
         ("what is the return policy within 30 days", True),     # paraphrase: same answer
         ("what is the shipping cost to india", False)]          # unrelated
print("\nSemantic cache, one stored query:", repr(cached_q))
e0 = emb(cached_q)
for q, same in tests:
    print(f"  cos={float(e0 @ emb(q)):.3f}  same correct answer={same!s:5}  {q}")
sims = {q: float(e0 @ emb(q)) for q, _ in tests}
print("  paraphrase and '90 days' have the same score:", abs(sims[tests[1][0]] - sims[tests[2][0]]) < 1e-9, "-> no threshold serves one and blocks the other")
```
**Output (my run):**
```
always small                               accuracy 0.620   mean cost  1.00
always large                               accuracy 0.852   mean cost 10.00
router (est noise 0.1, threshold 0.45)     accuracy 0.755   mean cost  4.61
router (est noise 0.3, threshold 0.45)     accuracy 0.751   mean cost  5.05
cascade, decent scorer (q=2.0), escalate if conf<0.0 accuracy 0.871   mean cost  5.17
                                             escalated 0.42, wrong small answers kept 0.059
cascade, decent scorer (q=2.0), escalate if conf<1.0 accuracy 0.885   mean cost  7.77
                                             escalated 0.68, wrong small answers kept 0.009
cascade, weak scorer (q=0.8), escalate if conf<0.0 accuracy 0.798   mean cost  5.65
                                             escalated 0.47, wrong small answers kept 0.129
cascade, weak scorer (q=0.8), escalate if conf<1.0 accuracy 0.850   mean cost  9.01
                                             escalated 0.80, wrong small answers kept 0.030

Semantic cache, one stored query: 'what is the refund policy within 30 days'
  cos=1.000  same correct answer=True   what is the refund policy within 30 days
  cos=0.875  same correct answer=False  what is the refund policy within 90 days
  cos=0.875  same correct answer=True   what is the return policy within 30 days
  cos=0.401  same correct answer=False  what is the shipping cost to india
  paraphrase and '90 days' have the same score: True -> no threshold serves one and blocks the other
```

**Follow-ups:**
- *How do you prove a router is safe?* Hold out a labelled set, compare per slice against always-large, and monitor escalation rate and complaint signals.
- *Where would a semantic cache be fine?* Public, low-stakes, high-repeat questions with short TTLs.
- *Cascade vs router?* Router saves latency but guesses; cascade checks the real answer but pays twice on hard cases.

**Common mistakes:** Reporting average accuracy and hiding slice regressions; trusting a confidence score without checking its calibration; a semantic cache shared across tenants; a cache key that leaves out model version or system prompt; forgetting that cache hits skip safety filters unless you re-apply them.

### Q29 ⭐⭐ 🟡 Rate limiting and overload protection for an LLM API: why requests-per-minute is a poor limit, token-based limits, queue length and timeouts, 429 and retry-after, load shedding, and priority tiers.
**Asked at:** product companies, platform teams; interview-prep guide, not a candidate report lists token-based limits and overload protection
**Say this first (1 line):** Requests per minute ignores how much work each request is, so limit tokens (input plus reserved output) per tenant, bound the queue by how long you can afford to wait, shed load early with a clear 429 or 503 and Retry-After, and protect priority traffic with reserved capacity.

**Then explain:**
- **Why RPM is poor:** one request can be 200 tokens or 8,000. In the toy two tenants each send 60 requests a minute under an RPM cap of 60. Tenant A (200 tokens) used 120,000 tokens and tenant B (8,000 tokens) 4,800,000 over 10 minutes, so the server saw 8,200 tokens/s against an assumed capacity of 3,000.
- **Token limits:** a token bucket per tenant, charged at admission with input tokens plus the requested `max_tokens` (a reservation), refunded for the unused part when the response ends. The same toy with a 250 tokens/s bucket admitted 120,000 (A) and 160,000 (B) tokens, about 467 tokens/s total. The burst size must be at least the largest legal request or it can never be admitted (my first run had that bug).
- **Also limit concurrency:** in-flight requests or running tokens per tenant, since long generations hold KV memory.
- **Queue and timeouts:** bound the wait queue (Little's law: queue length = arrival rate x tolerable wait) and drop requests that cannot meet their deadline or whose client has gone (Q19). An unbounded queue turns overload into universal timeouts.
- **Signals to clients:** 429 for "you are over your limit", 503 for "the service is overloaded", with Retry-After and client-side exponential backoff with jitter. Retries without jitter synchronise into storms.
- **Priority tiers:** reserve a share of capacity for the high tier and shed the low tier first. Multi-tenant fairness and noisy-neighbour isolation are Q49.

**Example:** Overload run (arrival about 1.3x the assumed capacity for 60 s; SLO 5 s end to end; 20% priority requests): 1,252 arrivals. Unbounded FIFO served all of them but only 297 (24%) met the SLO, p99 was 17.3 s and only 44 of 232 priority requests were in SLO. With a bounded wait and shedding (priority gets a longer wait budget), 1,012 were served, all within SLO (81% of arrivals), 240 were shed, p99 was 3.5 s and 232 of 232 priority requests were in SLO. Shedding looks like failure but raised the number of requests that were actually useful.

**Code:** (run with `python3 -I`; stdlib only; arrival rates, token sizes, service time (2 ms per token) and the SLO are assumed. The shed policy uses an estimated wait at arrival.)
```python
# TOY rate limiting and overload protection (stdlib + random). Capacities, token counts and SLOs are ASSUMED.
import random, heapq, statistics
random.seed(0)

# ---- Part 1: RPM limit vs token-bucket limit, two tenants sharing a server --------------------------------------
# Tenant A: short chat (200 tokens/request). Tenant B: long documents (8000 tokens/request). Both send 60 req/min.
# Server capacity ASSUMED: 3,000 tokens/s total.
class TokenBucket:
    def __init__(self, rate, burst): self.rate, self.burst, self.tokens, self.t = rate, burst, burst, 0.0
    def allow(self, now, cost):
        self.tokens = min(self.burst, self.tokens + (now - self.t) * self.rate); self.t = now
        if self.tokens >= cost: self.tokens -= cost; return True
        return False
def admitted_tokens(limiter_kind):
    used = {"A": 0, "B": 0}; rpm = {"A": {}, "B": {}}
    buckets = {k: TokenBucket(rate=250, burst=16000) for k in "AB"}  # 250 tokens/s per tenant, burst must exceed the largest request
    for sec in range(600):                                           # 10 minutes
        for who, toks in (("A", 200), ("B", 8000)):
            if True:                                                  # 1 request/s each
                if limiter_kind == "rpm":
                    m = sec // 60; rpm[who][m] = rpm[who].get(m, 0)
                    if rpm[who][m] < 60: rpm[who][m] += 1; used[who] += toks
                else:
                    if buckets[who].allow(sec, toks): used[who] += toks
    return used
for kind in ("rpm", "token bucket"):
    u = admitted_tokens(kind); tot = u["A"] + u["B"]
    print(f"{kind:13}: admitted tokens A={u['A']:>9,d}  B={u['B']:>9,d}  demand on server = {tot/600:7.0f} tokens/s (capacity 3000)")

# ---- Part 2: overload with and without bounded queue + deadline shedding ---------------------------------------
# Single server pool, service time ~ tokens (ASSUMED 2 ms/token), 8 parallel slots; arrivals 1.3x capacity for 60 s.
def simulate(policy, seed=1):
    g = random.Random(seed); slots, SLO = 8, 5.0
    t, free_at = 0.0, [0.0] * slots; arrivals = []
    while t < 60:
        t += g.expovariate(21.6); arrivals.append((t, int(g.lognormvariate(5.3, 0.6)), g.random() < 0.2))   # (time, tokens, is_priority)
    per_req = [0.002 * tok for _, tok, _ in arrivals]; capacity = slots / (sum(per_req) / len(per_req))
    queue, done, shed, pending = [], [], 0, list(enumerate(arrivals))
    heap = [(0.0, i) for i in range(slots)]; heapq.heapify(heap); lat = []
    for idx, (ta, tok, prio) in pending:
        # admission control: bound the queue by estimated wait
        free = heap[0][0]; est_wait = max(0.0, free - ta)
        if policy == "bounded+shed" and est_wait > (SLO * (0.9 if prio else 0.4)): shed += 1; continue   # priority gets a longer wait budget
        start_free, slot = heapq.heappop(heap); start = max(ta, start_free)
        if policy == "bounded+shed" and start - ta > SLO: shed += 1; heapq.heappush(heap, (start_free, slot)); continue
        finish = start + 0.002 * tok; heapq.heappush(heap, (finish, slot)); lat.append((finish - ta, prio))
    ok = [l for l, _ in lat if l <= SLO]
    pr = [l for l, p in lat if p]; pr_ok = [l for l in pr if l <= SLO]
    return len(arrivals), capacity, len(lat), len(ok), shed, (statistics.quantiles([l for l, _ in lat], n=100)[98] if lat else 0), len(pr), len(pr_ok)
print("\nOverload for 60 s (arrival rate set to about 1.3x the ASSUMED service capacity; SLO = 5 s end to end):")
for pol in ("unbounded FIFO", "bounded+shed"):
    n, cap, served, ok, shed, p99, npr, npr_ok = simulate(pol)
    print(f"{pol:15}: arrivals {n}  capacity ~{cap:.0f} req/s vs arrival {n/60:.0f} req/s | served {served}, within SLO {ok} ({100*ok/n:.0f}% of arrivals), shed {shed}, p99 latency of served {p99:.1f}s | priority within SLO {npr_ok}/{npr}")
```
**Output (my run):**
```
rpm          : admitted tokens A=  120,000  B=4,800,000  demand on server =    8200 tokens/s (capacity 3000)
token bucket : admitted tokens A=  120,000  B=  160,000  demand on server =     467 tokens/s (capacity 3000)

Overload for 60 s (arrival rate set to about 1.3x the ASSUMED service capacity; SLO = 5 s end to end):
unbounded FIFO : arrivals 1252  capacity ~16 req/s vs arrival 21 req/s | served 1252, within SLO 297 (24% of arrivals), shed 0, p99 latency of served 17.3s | priority within SLO 44/232
bounded+shed   : arrivals 1252  capacity ~16 req/s vs arrival 21 req/s | served 1012, within SLO 1012 (81% of arrivals), shed 240, p99 latency of served 3.5s | priority within SLO 232/232
```

**Follow-ups:**
- *Token-based limit when output length is unknown?* Reserve `max_tokens` and refund; require a max_tokens cap (the code-review question Q43 flags its absence).
- *What do you do with a shed request?* Return 429/503 with Retry-After, or degrade (smaller model, shorter output) for lower tiers.
- *How is this different from Kubernetes rate limiting?* Cost per request varies by orders of magnitude here, so the limiter must be token-aware.

**Common mistakes:** Limiting RPM only; counting input tokens and forgetting output; an unbounded queue; retrying without jitter; shedding by random drop instead of by tier and deadline; setting the bucket burst below the largest allowed request.

### Q30 ⭐⭐ 🟡 Benchmarking an LLM server properly: open-loop (fixed arrival rate, Poisson or bursty) vs closed-loop (fixed concurrency), realistic prompt and output length distributions, warm-up, prefix-cache effects, and which numbers to report.
**Asked at:** inference-platform teams, senior MLE rounds; interview-prep guide, not a candidate report; the vLLM benchmark docs and the TGI v3 post describe methodology
**Say this first (1 line):** Benchmark with open-loop arrivals at a fixed rate (Poisson, plus bursts) and realistic prompt and output length distributions, to see queueing and tail latency; use closed-loop fixed concurrency only to find capacity. Warm up, control prefix-cache effects, and report percentiles with the load level, lengths, hardware and engine settings.

**Then explain:**
- **Closed loop** (N clients, each sends the next request after the last returns) cannot overload the server: it slows its own offer. It finds capacity and shows Little's-law latency for that N, but hides queueing. **Open loop** (arrivals on a schedule regardless of responses) shows the knee and what an unlucky user sees.
- **From the toy:** capacity 2.8 req/s with 8 slots. Closed loop at concurrency 8 reached 2.8 req/s with p99 13.10 s; at 64 the same throughput but p50 22.23 s, which is just queueing in the client. Open loop at 0.50, 0.80, 0.95 and 1.10 x capacity had p99 of 13.11, 13.90, 23.18 and 211.16 s.
- **Workload realism:** use real prompt and output length distributions (the vLLM benchmark docs list ShareGPT, random and prefix-repetition datasets; check what your traffic looks like instead). Fixed lengths hide long-tail effects.
- **Prefix-cache effects:** one repeated prompt hits the cache almost always. In the toy (synthetic prompts, 16-token blocks) the repeated prompt hit 0.995 of blocks and a realistic mix 0.538 (0.554 after discarding 20 warm-up requests). Decide whether you are measuring cold or warm, and say so. The TGI v3 docs describe a second run for the prefix-cache case; its 13x claim is vendor-reported on one benchmark and I do not rely on it.
- **Warm-up and steady state:** discard start-up (compilation, graph capture, empty caches) and run long enough for the queue to reach steady state.
- **Report:** TTFT, TPOT or ITL and E2E at p50/p95/p99 (the vLLM benchmark docs report mean, median and P99), request rate and achieved throughput, goodput against stated SLOs, error and timeout counts, length distributions, engine version and flags, hardware, whether the cache was warm. The page I read did not mention goodput, so compute it yourself (Q16).

**Example:** Your "benchmark" runs 64 concurrent clients with one 2,000-token prompt and reports median latency 22 s and 2.8 req/s. In the toy that setup measures nothing about the user experience at 0.8 x capacity (p99 13.90 s) or at overload (p99 211 s), and the repeated prompt inflates cache hits to 99.5%. A proper run sweeps open-loop rates, uses sampled lengths and prints a table of p50/p99 against rate.

**Code:** (run with `python3 -I`; stdlib and numpy; the server is a toy queue with 8 slots and assumed service times (0.1 s plus 0.02 s per lognormal-distributed output token), not an LLM engine. Prompts are synthetic.)
```python
# TOY benchmark-methodology demo (stdlib + numpy). The "server" is a queue with S parallel slots and random service times
# (ASSUMED: 0.1 s prefill + 0.02 s per output token, output tokens lognormal). It is not an LLM engine.
import heapq, random, hashlib
import numpy as np
S = 8
def service_times(n, seed):
    g = np.random.default_rng(seed); toks = np.minimum(g.lognormal(4.6, 0.8, n), 1500)   # median ~100 tokens, long tail
    return 0.1 + 0.02 * toks
mean_service = service_times(200000, 0).mean(); capacity = S / mean_service
print(f"mean service {mean_service:.2f}s  ->  capacity {capacity:.1f} req/s with {S} slots (assumed toy server)\n")

def pct(x, q): return float(np.percentile(x, q))
def open_loop(rate, n=6000, seed=1):                     # arrivals do NOT wait for responses
    g = np.random.default_rng(seed); arr = np.cumsum(g.exponential(1 / rate, n)); svc = service_times(n, seed + 7)
    free = [0.0] * S; heapq.heapify(free); lat = []
    for a, s in zip(arr, svc):
        f = heapq.heappop(free); st = max(a, f); heapq.heappush(free, st + s); lat.append(st + s - a)
    return np.array(lat), n / (arr[-1] if arr[-1] else 1)
def closed_loop(conc, n=6000, seed=1):                   # each of `conc` clients sends the next request when the last returns
    svc = service_times(n, seed + 7); free = [0.0] * S; heapq.heapify(free)
    clients = [0.0] * conc; heapq.heapify(clients); lat = []; end = 0.0
    for s in svc:
        a = heapq.heappop(clients); f = heapq.heappop(free); st = max(a, f); fin = st + s
        heapq.heappush(free, fin); heapq.heappush(clients, fin); lat.append(fin - a); end = max(end, fin)
    return np.array(lat), n / end
print("Closed loop (fixed concurrency): measures capacity, but latency only reflects how many clients you chose")
for c in (4, 8, 16, 64):
    lat, thr = closed_loop(c); print(f"  concurrency {c:3d}: throughput {thr:5.1f} req/s   p50 {pct(lat,50):6.2f}s   p99 {pct(lat,99):6.2f}s")
print("Open loop (Poisson arrivals at a fraction of capacity): shows the knee")
for f in (0.5, 0.8, 0.95, 1.1):
    lat, thr = open_loop(f * capacity); print(f"  load {f:4.2f} x capacity: p50 {pct(lat,50):7.2f}s   p99 {pct(lat,99):8.2f}s   (arrival rate {f*capacity:5.1f} req/s)")

# Prefix-cache effect: block-hash cache, 16-token blocks. Count how much of each prompt is a cache hit.
B = 16
def block_hashes(tokens):
    h, out = b"", []
    for i in range(0, len(tokens) - len(tokens) % B, B):   # only FULL blocks are cached
        h = hashlib.sha256(h + bytes(str(tokens[i:i + B]), "ascii")).digest(); out.append(h)
    return out
def hit_rate(prompts, warmup=0):
    cache, hit, tot = set(), 0, 0
    for k, p in enumerate(prompts):
        hs = block_hashes(p); h_here = 0
        for x in hs:
            if x in cache: h_here += 1
            else: break                                      # prefix match stops at first miss
        if k >= warmup: hit += h_here; tot += len(hs)
        cache.update(hs)
    return hit / tot
g = random.Random(0)
system = [[g.randrange(50000) for _ in range(1000)] for _ in range(3)]       # 3 distinct 1000-token system prompts
same = [system[0] + [7] * 1000] * 200                                          # benchmark that repeats ONE prompt
real = [system[g.randrange(3)] + [g.randrange(50000) for _ in range(g.randint(100, 1500))] for _ in range(200)]
print("\nPrefix-cache hit rate on full blocks (SYNTHETIC prompts, 200 requests):")
print(f"  one repeated prompt, counting all requests : {hit_rate(same):.3f}")
print(f"  realistic mix (3 system prompts + unique text), counting all : {hit_rate(real):.3f}")
print(f"  realistic mix, after discarding 20 warm-up requests          : {hit_rate(real, 20):.3f}")
```
**Output (my run):**
```
mean service 2.84s  ->  capacity 2.8 req/s with 8 slots (assumed toy server)

Closed loop (fixed concurrency): measures capacity, but latency only reflects how many clients you chose
  concurrency   4: throughput   1.4 req/s   p50   2.08s   p99  13.10s
  concurrency   8: throughput   2.8 req/s   p50   2.08s   p99  13.10s
  concurrency  16: throughput   2.8 req/s   p50   5.02s   p99  16.14s
  concurrency  64: throughput   2.8 req/s   p50  22.23s   p99  34.27s
Open loop (Poisson arrivals at a fraction of capacity): shows the knee
  load 0.50 x capacity: p50    2.11s   p99    13.11s   (arrival rate   1.4 req/s)
  load 0.80 x capacity: p50    2.64s   p99    13.90s   (arrival rate   2.3 req/s)
  load 0.95 x capacity: p50    7.15s   p99    23.18s   (arrival rate   2.7 req/s)
  load 1.10 x capacity: p50  121.10s   p99   211.16s   (arrival rate   3.1 req/s)

Prefix-cache hit rate on full blocks (SYNTHETIC prompts, 200 requests):
  one repeated prompt, counting all requests : 0.995
  realistic mix (3 system prompts + unique text), counting all : 0.538
  realistic mix, after discarding 20 warm-up requests          : 0.554
```

**Follow-ups:**
- *Why Poisson?* It models independent users; add bursty arrivals to test spikes (the vLLM CLI has a burstiness option).
- *How long to run?* Until percentiles stop moving; tails need many samples (p99 from 100 requests is a guess).
- *How do you compare two engines?* Same hardware, same dataset and rate sweep, warm and cold cache variants, same output-length handling, repeated runs.

**Common mistakes:** Closed loop only; one repeated prompt; fixed lengths; reporting the mean; no warm-up; mixing cache-warm and cache-cold runs; comparing engines with different max_tokens or sampling settings; quoting a vendor benchmark as universal.

### Q31 ⭐⭐ 🟡 Long-context serving: how do prefill time, KV memory and attention cost grow at 32k to 200k+ tokens, and what helps (chunked prefill, prefix reuse, KV quantization, sliding window or GQA/MLA models, offload, sequence parallelism)? (Part 1 Q30 covers why quality and cost break.)
**Asked at:** product companies, AI labs, inference-platform teams; interview-prep guide, not a candidate report poses a 200K-token serving design
**Say this first (1 line):** At long context, KV memory grows linearly with tokens, prefill compute grows roughly quadratically in the attention part, and every decode step re-reads the whole KV. You help with chunked prefill, prefix reuse, KV quantization, GQA or MLA models, sliding windows, offload and sequence parallelism, each with a quality or complexity cost.

**Then explain:**
- **KV memory is linear:** with assumed Llama-3-8B-like shapes (32 layers, 8 KV heads, head dim 128, fp16) one sequence takes 1.07 GB at 8,192 tokens, 4.29 GB at 32,768, 17.18 GB at 131,072 and 26.21 GB at 200,000. The same layers with 32 KV heads (MHA) would take 4x that. A 70B-like shape (80 layers) takes 65.54 GB at 200,000. Shapes are assumed; Part 1 Q15 has the formula.
- **Capacity collapses:** on an 80 GB card with 16 GB weights and 10% reserve, the 8B-like model fits 52 sequences at 8,192 tokens, 13 at 32,768, 3 at 131,072 and 2 at 200,000 (fp8 KV doubles those to 104, 26, 6 and 4).
- **Prefill grows quadratically in attention:** FLOPs are about 2 x params x L for the linear layers plus about 2 x layers x hidden x L^2 for causal attention. I checked the closed form against a brute-force sum. Attention equals the linear part at L = params / (layers x hidden), about 61,000 tokens here, and is 35% of FLOPs at 32,768 and 77% at 200,000. At an assumed sustained 200 TFLOP/s that is 4.0 s at 32k and 68.4 s at 200k of prefill: a TTFT problem.
- **Decode gets heavier too:** one sequence at 131,072 tokens reads 17.18 GB of KV per step on top of 16 GB of weights, so the memory-bound floor goes from 8.5 ms (8k) to 16.6 ms at an assumed 2 TB/s.
- **What helps:** chunked prefill (Q20) so long prompts do not stall others; prefix reuse (Q14) when prompts share a long document; KV quantization (Q22); GQA and MLA models (Part 1 Q33); sliding-window layers (a 4,096-token window caps KV at 0.54 GB per sequence in the toy, at a quality cost); offloading KV to host memory or SSD (Mooncake describes a CPU/DRAM/SSD cache pool, authors' claims); sequence or context parallelism to split one long prompt across GPUs. Why quality breaks is Part 1 Q30.

**Example:** A 200k-token legal document question on an 8B-like model: KV is 26.21 GB (fp16) or about 13 GB (fp8), so one 80 GB card holds 2 such sequences in fp16 (4 in fp8) with nothing left for short chats. Prefill takes about 68 s at the assumed 200 TFLOP/s unless split across GPUs. If many users ask about the same document, caching its prefix turns most of that into a one-time cost. A mixed fleet usually routes long-context traffic to its own pool so it does not starve short requests.

**Code:** (run with `python3 -I`; stdlib only. Model shapes, the 200 TFLOP/s sustained rate and the 2 TB/s bandwidth are assumptions, and the 8B-like shape is used for arithmetic even though a given model may not support 200k.)
```python
# Long-context serving arithmetic (stdlib only). Model shapes are ASSUMED Llama-3-8B-like and Llama-3-70B-like
# (32 layers/8 KV heads/head dim 128/hidden 4096; 80 layers/8 KV heads/head dim 128/hidden 8192). GPU numbers ASSUMED.
GB = 1e9
def kv_bytes_per_token(layers, kv_heads, hd, dtype_bytes): return 2 * layers * kv_heads * hd * dtype_bytes
models = {"8B-like GQA": dict(P=8.0e9, L=32, kvh=8, hd=128, d=4096), "70B-like GQA": dict(P=70e9, L=80, kvh=8, hd=128, d=8192)}
print("KV cache per sequence (fp16, assumed shapes), and the same 8B-like shape if it had MHA (32 KV heads):")
print(f"{'context':>8} {'8B GQA':>9} {'8B MHA':>9} {'70B GQA':>9}   (GB)")
for ctx in (8192, 32768, 131072, 200000):
    a = kv_bytes_per_token(32, 8, 128, 2) * ctx / GB; m = kv_bytes_per_token(32, 32, 128, 2) * ctx / GB; b = kv_bytes_per_token(80, 8, 128, 2) * ctx / GB
    print(f"{ctx:8d} {a:9.2f} {m:9.2f} {b:9.2f}")
print("fp8 KV halves the GQA numbers (1 byte instead of 2).")

# Prefill FLOPs: linear part 2*P*L, causal attention part sum_{i=1..L} 4*layers*d*i  ~= 2*layers*d*L^2.
def attn_flops_exact(L, layers, d): return sum(4 * layers * d * i for i in range(1, L + 1))
def attn_flops_closed(L, layers, d): return 2 * layers * d * L * (L + 1)
chk = attn_flops_exact(3000, 32, 4096) == attn_flops_closed(3000, 32, 4096)
print("\nclosed form for causal attention FLOPs matches brute-force sum (L=3000):", chk)
m = models["8B-like GQA"]
print("Prefill FLOPs, 8B-like model, and time at an ASSUMED sustained 200 TFLOP/s (guess, not measured):")
print(f"{'context':>8} {'linear TFLOP':>13} {'attention TFLOP':>16} {'attn share':>11} {'prefill s':>10}")
for ctx in (4096, 32768, 131072, 200000):
    lin = 2 * m["P"] * ctx; att = attn_flops_closed(ctx, m["L"], m["d"]); tot = lin + att
    print(f"{ctx:8d} {lin/1e12:13.1f} {att/1e12:16.1f} {att/tot:10.0%} {tot/200e12:10.1f}")
print("attention term equals the linear term at L = P/(layers*d) = %d tokens" % (m["P"] / (m["L"] * m["d"])))

# How many sequences fit? 80 GB card (ASSUMED), 8B weights fp16 = 16 GB, keep 10% for activations/overhead.
free = 80 * 0.9 * GB - 16 * GB
print("\nConcurrent sequences on one 80 GB card after 16 GB weights (8B-like, fp16 KV vs fp8 KV):")
for ctx in (8192, 32768, 131072, 200000):
    f16 = int(free // (kv_bytes_per_token(32, 8, 128, 2) * ctx)); f8 = int(free // (kv_bytes_per_token(32, 8, 128, 1) * ctx))
    print(f"  ctx {ctx:6d}: fp16 KV {f16:3d} seqs, fp8 KV {f8:3d} seqs")

# Sliding window: KV capped at W tokens per layer that uses it.
W = 4096
print("\nIf every layer used a %d-token sliding window, KV per sequence would be capped at %.2f GB regardless of context (quality trade-off)." % (W, kv_bytes_per_token(32, 8, 128, 2) * W / GB))

# Decode: every step re-reads the whole KV of every running sequence.
bw = 2.0e12   # ASSUMED 2 TB/s
for ctx in (8192, 131072):
    kv = kv_bytes_per_token(32, 8, 128, 2) * ctx
    print(f"decode step, one sequence, ctx {ctx}: reads weights 16 GB + KV {kv/GB:.2f} GB -> memory-bound floor {1000*(16*GB+kv)/bw:.1f} ms")
```
**Output (my run):**
```
KV cache per sequence (fp16, assumed shapes), and the same 8B-like shape if it had MHA (32 KV heads):
 context    8B GQA    8B MHA   70B GQA   (GB)
    8192      1.07      4.29      2.68
   32768      4.29     17.18     10.74
  131072     17.18     68.72     42.95
  200000     26.21    104.86     65.54
fp8 KV halves the GQA numbers (1 byte instead of 2).

closed form for causal attention FLOPs matches brute-force sum (L=3000): True
Prefill FLOPs, 8B-like model, and time at an ASSUMED sustained 200 TFLOP/s (guess, not measured):
 context  linear TFLOP  attention TFLOP  attn share  prefill s
    4096          65.5              4.4         6%        0.3
   32768         524.3            281.5        35%        4.0
  131072        2097.2           4503.6        68%       33.0
  200000        3200.0          10485.8        77%       68.4
attention term equals the linear term at L = P/(layers*d) = 61035 tokens

Concurrent sequences on one 80 GB card after 16 GB weights (8B-like, fp16 KV vs fp8 KV):
  ctx   8192: fp16 KV  52 seqs, fp8 KV 104 seqs
  ctx  32768: fp16 KV  13 seqs, fp8 KV  26 seqs
  ctx 131072: fp16 KV   3 seqs, fp8 KV   6 seqs
  ctx 200000: fp16 KV   2 seqs, fp8 KV   4 seqs

If every layer used a 4096-token sliding window, KV per sequence would be capped at 0.54 GB regardless of context (quality trade-off).
decode step, one sequence, ctx 8192: reads weights 16 GB + KV 1.07 GB -> memory-bound floor 8.5 ms
decode step, one sequence, ctx 131072: reads weights 16 GB + KV 17.18 GB -> memory-bound floor 16.6 ms
```

**Follow-ups:**
- *Is 200 TFLOP/s realistic for attention?* Attention kernels often run below the linear layers' efficiency, so real prefill is likely slower; the point is the scaling.
- *Why not just add more GPUs?* TP shards weights and KV but each long request still needs its prefill done; sequence parallelism splits the prompt itself.
- *When is a sliding window acceptable?* When the task only needs local context; test retrieval at depth first.

**Common mistakes:** Computing KV with attention heads instead of KV heads; forgetting the quadratic prefill term; sizing for average context when the long tail decides capacity; assuming a model supports a context because the shape arithmetic fits; mixing long and short requests in one pool without chunking.

### Q32 ⭐⭐ 🔴 Disaggregated prefill and decode (DistServe, Mooncake, vLLM's disaggregated prefilling): why separate the phases, what does it improve (goodput under TTFT and TPOT SLOs, tail ITL), what does it not improve, and what does the KV transfer cost?
**Asked at:** inference-platform teams, AI labs, large-scale serving teams; interview-prep guide, not a candidate report lists disaggregation
**Say this first (1 line):** Disaggregation runs prefill and decode on separate GPU pools so each phase can be tuned to its own SLO: it protects decode token gaps and lets you size TTFT and TPOT independently. It does not make the same GPUs generate more tokens per second, and it adds a KV transfer and two pools to run.

**Then explain:**
- **Why separate:** prefill is compute-heavy bursts, decode is memory-bound steady steps (Part 1 Q7). On one engine a long prefill stalls everyone's decoding unless chunked (Q20).
- **What it improves:** goodput under both TTFT and TPOT SLOs, and tail inter-token latency. Authors' claims, in their setups: DistServe reports up to 7.4x more requests or 12.6x tighter SLOs; Mooncake reports up to 525% throughput in simulation and 75% more requests on its production Kimi workload. Do not expect those on yours.
- **What it does not improve:** the vLLM docs I read say disaggregated prefilling does not improve throughput; it tunes TTFT and ITL independently (check live docs). My toy agrees: output tokens/s were equal at light loads (786 vs 787, 1,293 vs 1,295 at 6 and 10 req/s, 1,787 vs 1,787 at 14) and slightly lower at 17 req/s (2,002 vs 2,027).
- **KV transfer cost:** bytes = tokens x KV bytes per token. A 2,048-token prompt on the assumed 8B-like GQA shape is 268 MB, or 10.7 ms over an assumed 25 GB/s link. It needs a fast interconnect and a KV connector, and long prompts make it worse.
- **Costs:** two pools to size and balance (when the prefill pool saturates, TTFT blows up), more failure modes, and TTFT can rise (toy p50 0.06 s to 0.10 s at 10 req/s).
- **Alternatives:** chunked prefill with a token budget (Q20) fixes much of the interference on one pool at lower complexity.

**Example:** Toy at 10 req/s (synthetic lengths, assumed step times): two colocated GPUs had p99 inter-token gap 151.2 ms, so only 1.06 req/s met "TTFT <= 1 s and no gap > 100 ms"; one prefill plus one decode GPU had p99 gap 15.0 ms and 9.56 req/s met it. With the looser "mean TPOT <= 50 ms" criterion both were about 9.55 req/s: the gain depends on which SLO you write down. At 14 req/s the colocated pair actually scored higher on mean TPOT goodput (12.82 vs 12.10) because the single prefill GPU became the bottleneck.

**Code:** (run with `python3 -I`; stdlib and numpy; step times (prefill 5 ms + 0.05 ms per token, decode step 12 ms + 0.1 ms per running sequence), lengths, slot cap and link speed are all assumed. Colocated engines prefill the whole prompt before the next decode step (no chunking).)
```python
# TOY comparison: 2 colocated GPUs vs 1 prefill GPU + 1 decode GPU (stdlib + numpy). Step-time model and all constants are
# ASSUMED (prefill 5 ms + 0.05 ms/token; decode step 12 ms + 0.1 ms per running sequence). No real engine, no GPU measurement.
import numpy as np
P0, P1, D0, D1, CAP = 0.005, 0.00005, 0.012, 0.0001, 32
KV_BYTES_PER_TOKEN = 131072          # 8B-like GQA fp16: 2*32 layers*8 heads*128*2 bytes (assumed shape)
LINK = 25e9                          # ASSUMED 25 GB/s usable link for the KV transfer

def make_requests(rate, n, seed):
    g = np.random.default_rng(seed); arr = np.cumsum(g.exponential(1 / rate, n))
    plen = np.clip(g.lognormal(6.8, 0.7, n), 128, 8192).astype(int); olen = np.clip(g.lognormal(4.8, 0.5, n), 16, 600).astype(int)
    return [dict(a=arr[i], p=int(plen[i]), o=int(olen[i])) for i in range(n)]

def colocated(reqs):
    """One engine: if a prompt is waiting (and a slot is free) run its whole prefill (decode stalls); else one decode step."""
    t, nxt, wait, run = 0.0, 0, [], []
    out = []
    while nxt < len(reqs) or wait or run:
        while nxt < len(reqs) and reqs[nxt]['a'] <= t: wait.append(reqs[nxt]); nxt += 1
        if wait and len(run) < CAP:
            r = wait.pop(0); t += P0 + P1 * r['p']; r['first'] = t; r['times'] = [t]; r['left'] = r['o'] - 1
            if r['left'] > 0: run.append(r)
            else: r['end'] = t; out.append(r)
        elif run:
            t += D0 + D1 * len(run)
            for r in list(run):
                r['times'].append(t); r['left'] -= 1
                if r['left'] == 0: r['end'] = t; run.remove(r); out.append(r)
        else: t = reqs[nxt]['a']
    return out

def prefill_only(reqs):
    t = 0.0
    for r in reqs:
        t = max(t, r['a']) + P0 + P1 * r['p']; r['first'] = t; r['ready'] = t + r['p'] * KV_BYTES_PER_TOKEN / LINK
    return reqs
def decode_only(reqs):
    reqs = sorted(reqs, key=lambda r: r['ready']); t, nxt, wait, run, out = 0.0, 0, [], [], []
    while nxt < len(reqs) or wait or run:
        while nxt < len(reqs) and reqs[nxt]['ready'] <= t: wait.append(reqs[nxt]); nxt += 1
        while wait and len(run) < CAP:
            r = wait.pop(0); r['times'] = [r['first']]; r['left'] = r['o'] - 1
            if r['left'] > 0: run.append(r)
            else: r['end'] = r['first']; out.append(r)
        if run:
            t += D0 + D1 * len(run)
            for r in list(run):
                r['times'].append(t); r['left'] -= 1
                if r['left'] == 0: r['end'] = t; run.remove(r); out.append(r)
        elif nxt < len(reqs): t = max(t, reqs[nxt]['ready'])
        else: break
    return out

def metrics(done, label, T_SLO=1.0, GAP_SLO=0.1):
    ttft = np.array([r['first'] - r['a'] for r in done])
    gaps = np.concatenate([np.diff(r['times']) for r in done if len(r['times']) > 1])
    ok = sum(1 for r in done if r['first'] - r['a'] <= T_SLO and (len(r['times']) < 2 or np.diff(r['times']).max() <= GAP_SLO))
    ok2 = sum(1 for r in done if r['first'] - r['a'] <= T_SLO and (r['o'] < 2 or (r['end'] - r['first']) / (r['o'] - 1) <= 0.05))
    span = max(r['end'] for r in done) - min(r['a'] for r in done)
    toks = sum(r['o'] for r in done)
    print(f"  {label:20} TTFT p50 {np.percentile(ttft,50):5.2f}s p99 {np.percentile(ttft,99):6.2f}s | ITL p99 {np.percentile(gaps,99)*1000:6.1f} ms | goodput(max gap) {ok/span:5.2f} goodput(mean TPOT) {ok2/span:5.2f} req/s | out tok/s {toks/span:6.0f}")

print(f"KV for a 2048-token prompt: {2048*KV_BYTES_PER_TOKEN/1e6:.0f} MB -> {2048*KV_BYTES_PER_TOKEN/LINK*1000:.1f} ms at an ASSUMED {LINK/1e9:.0f} GB/s link\n")
for rate in (6, 10, 14, 17):
    n = 1500; reqs = make_requests(rate, n, 3)
    # colocated: 2 engines, round-robin dispatch
    ca = colocated([dict(r) for r in reqs[0::2]]); cb = colocated([dict(r) for r in reqs[1::2]])
    # disaggregated: 1 prefill engine + 1 decode engine (same 2 GPUs)
    dd = decode_only(prefill_only([dict(r) for r in reqs]))
    print(f"arrival rate {rate} req/s (SYNTHETIC lengths; goodput = TTFT<=1 s AND [max token gap <=100 ms | mean TPOT <=50 ms])")
    metrics(ca + cb, "2 colocated"); metrics(dd, "1 prefill + 1 decode")
```
**Output (my run):**
```
KV for a 2048-token prompt: 268 MB -> 10.7 ms at an ASSUMED 25 GB/s link

arrival rate 6 req/s (SYNTHETIC lengths; goodput = TTFT<=1 s AND [max token gap <=100 ms | mean TPOT <=50 ms])
  2 colocated          TTFT p50  0.06s p99   0.25s | ITL p99   97.1 ms | goodput(max gap)  1.85 goodput(mean TPOT)  5.80 req/s | out tok/s    786
  1 prefill + 1 decode TTFT p50  0.07s p99   0.43s | ITL p99   14.0 ms | goodput(max gap)  5.81 goodput(mean TPOT)  5.81 req/s | out tok/s    787
arrival rate 10 req/s (SYNTHETIC lengths; goodput = TTFT<=1 s AND [max token gap <=100 ms | mean TPOT <=50 ms])
  2 colocated          TTFT p50  0.06s p99   0.29s | ITL p99  151.2 ms | goodput(max gap)  1.06 goodput(mean TPOT)  9.55 req/s | out tok/s   1293
  1 prefill + 1 decode TTFT p50  0.10s p99   0.60s | ITL p99   15.0 ms | goodput(max gap)  9.56 goodput(mean TPOT)  9.56 req/s | out tok/s   1295
arrival rate 14 req/s (SYNTHETIC lengths; goodput = TTFT<=1 s AND [max token gap <=100 ms | mean TPOT <=50 ms])
  2 colocated          TTFT p50  0.08s p99   1.21s | ITL p99  215.4 ms | goodput(max gap)  0.37 goodput(mean TPOT) 12.82 req/s | out tok/s   1787
  1 prefill + 1 decode TTFT p50  0.23s p99   1.85s | ITL p99   15.2 ms | goodput(max gap)  9.67 goodput(mean TPOT) 12.10 req/s | out tok/s   1787
arrival rate 17 req/s (SYNTHETIC lengths; goodput = TTFT<=1 s AND [max token gap <=100 ms | mean TPOT <=50 ms])
  2 colocated          TTFT p50  3.67s p99   7.17s | ITL p99  199.5 ms | goodput(max gap)  0.09 goodput(mean TPOT)  4.56 req/s | out tok/s   2027
  1 prefill + 1 decode TTFT p50  4.40s p99   5.71s | ITL p99   15.2 ms | goodput(max gap)  2.00 goodput(mean TPOT)  3.73 req/s | out tok/s   2002
```

**Follow-ups:**
- *Why does ITL tail fall?* Decode GPUs never run a long prefill, so no token waits behind one.
- *When is it not worth it?* Short prompts, small clusters, or when chunked prefill already meets the SLO.
- *How do you size the pools?* From prompt and output length mix: prefill GPUs by prompt tokens per second, decode GPUs by running sequences and KV memory.

**Common mistakes:** Selling it as a throughput win; ignoring KV transfer time and the interconnect; sizing the prefill pool too small; not saying which SLO defines goodput; comparing against an unchunked baseline and calling it a fair test.

### Q33 ⭐⭐ 🟡 Estimate the ceiling for decode speed: using memory bandwidth and bytes read per token, estimate tokens per second at batch 1 for a 7B and a 70B model, then explain MFU/MBU and why nvidia-smi 'GPU utilisation 100%' says little.
**Asked at:** inference-platform teams, MLE rounds; interview-prep guide, not a candidate report lists throughput estimation and misleading GPU utilisation
**Say this first (1 line):** At batch 1 decode reads every weight once per token, so tokens per second is at most memory bandwidth divided by bytes read per token. On an assumed 2 TB/s card that is about 143 tokens/s for a 7B fp16 model and about 14 for 70B fp16 on one card's bandwidth. MFU and MBU measure how close you get; nvidia-smi utilisation only says a kernel was running.

**Then explain:**
- **Formula:** tokens/s <= bandwidth / (weight bytes + KV bytes read per token). Weights only gives a ceiling. Specs here are assumed A100-80GB-class values (about 2.0 TB/s, about 312 TFLOP/s dense fp16), from memory; check the vendor sheet.
- **From the run:** 7B fp16 (14 GB): 142.9 tokens/s. 7B at 4-bit (3.5 GB): 571.4. 70B fp16 is 140 GB, so it needs at least 2 x 80 GB cards; one card's bandwidth gives 14.3 and two cards in tensor parallel at best 28.6, before all-reduce cost. 70B at 4-bit (35 GB): 57.1.
- **Why it is memory-bound:** the ridge point (peak FLOPs / bandwidth) is 156 FLOPs per byte, and batch-1 decode does about 1 FLOP per byte. MFU (achieved FLOPs / peak) at the 7B ceiling is 0.64%. Part 1 Q32 has the roofline argument.
- **MBU:** achieved bytes per second (weights plus KV per step, divided by step time) divided by peak bandwidth. It is the useful efficiency number for decode; MFU is the right one for prefill.
- **Batching:** a batch reads the weights once, so tokens per second rises almost linearly with batch until compute or KV reads take over. The weights-only table is an upper bound because KV reads grow with batch and context (Q4, Q31).
- **nvidia-smi "GPU util":** from memory (check NVIDIA's docs) it is the fraction of the sample period in which at least one kernel was running, so one tiny kernel keeps it near 100% while most SMs and bandwidth sit idle. Use MBU/MFU, queue metrics and tokens per second.
- **CPU toy shape (noisy, this machine):** a 268 MB matrix times 1 to 64 vectors went from 8.30 ms to 37.10 ms, 120 to 1,725 results/s, about 14x more results for about 4.5x the time: the memory stream is shared.

**Example:** You are told a 70B fp16 model must answer at 40 tokens/s per user at batch 1. Weights are 140 GB. On an assumed 2 TB/s card with TP=2 the best case is about 28.6 tokens/s before communication and KV reads, so you need a faster card, more TP, a 4-bit model (ceiling 57.1 on one card) or speculative decoding (Q11), and you have only calculated, not measured. The answer in an interview is the arithmetic plus "then I would measure MBU".

**Code:** (run with `python3 -I`; stdlib and numpy. Part A is arithmetic on assumed A100-class specs (no GPU was used). Part B times a float32 matrix-vector product on whatever CPU runs it; timings are noisy and machine-specific, so only the shape matters.)
```python
# Decode-speed ceiling. Part A: arithmetic with ASSUMED A100-80GB-class specs (check vendor sheets).
# Part B: a CPU toy with numpy showing the same memory-bound shape; numbers are about THIS machine, not any GPU.
import time, numpy as np
BW, PEAK = 2.0e12, 312e12            # ASSUMED A100-80GB-class: ~2.0 TB/s HBM, ~312 TFLOP/s dense fp16/bf16
print("A) batch-1 ceiling = bandwidth / bytes read per token (weights only; KV and overheads ignored, so a ceiling)")
for name, params, bytes_pw in (("7B fp16", 7e9, 2), ("7B 4-bit", 7e9, 0.5), ("70B fp16", 70e9, 2), ("70B 4-bit", 70e9, 0.5)):
    wb = params * bytes_pw; gpus_min = -(-wb // 80e9)
    print(f"  {name:9}: weights {wb/1e9:6.1f} GB, needs >= {int(gpus_min)} x 80 GB card(s); ceiling on ONE card's bandwidth {BW/wb:6.1f} tok/s; "
          f"with TP over {int(max(gpus_min,1))} card(s), best case {BW*max(gpus_min,1)/wb:6.1f} tok/s (ignores all-reduce)")
print(f"  FLOPs/byte ridge point = PEAK/BW = {PEAK/BW:.0f}; batch-1 decode does ~1 FLOP per byte read (2 FLOPs per fp16 weight, 2 bytes)")
print("  MFU at the 7B fp16 ceiling = %.2f%%  (14 GFLOP per token x %.0f tok/s / peak)" % (100 * 14e9 * (BW / 14e9) / PEAK, BW / 14e9))
print("  batch b reads the weights once: ceiling in total tokens/s grows ~linearly until compute or KV reads bite:")
for b in (1, 8, 32, 128):
    t_mem = 14e9 / BW; t_cmp = b * 14e9 / PEAK
    print(f"    b={b:3d}: memory time {t_mem*1e3:5.2f} ms, compute time {t_cmp*1e3:5.2f} ms -> step ~ {max(t_mem,t_cmp)*1e3:5.2f} ms, {b/max(t_mem,t_cmp):8.0f} tok/s total (KV reads ignored)")

print("\nB) CPU toy: y = W @ x for W of 4096 x 16384 float32 (268 MB), batch of 1..64 vectors (this machine, numpy; timings are noisy and machine-specific, look at the shape)")
rng = np.random.default_rng(0); W = rng.standard_normal((4096, 16384), dtype=np.float32)
def best(fn, reps=9): return min((lambda t0: (fn(), time.perf_counter() - t0)[1])(time.perf_counter()) for _ in range(reps))
for b in (1, 4, 16, 64):
    X = rng.standard_normal((16384, b), dtype=np.float32); t = best(lambda: W @ X)
    print(f"  batch {b:2d}: {t*1e3:7.2f} ms, weight bytes streamed per result {W.nbytes/b/1e6:6.1f} MB, results/s {b/t:8.0f}, ms per vector {t/b*1e3:6.3f}")
```
**Output (my run):**
```
A) batch-1 ceiling = bandwidth / bytes read per token (weights only; KV and overheads ignored, so a ceiling)
  7B fp16  : weights   14.0 GB, needs >= 1 x 80 GB card(s); ceiling on ONE card's bandwidth  142.9 tok/s; with TP over 1 card(s), best case  142.9 tok/s (ignores all-reduce)
  7B 4-bit : weights    3.5 GB, needs >= 1 x 80 GB card(s); ceiling on ONE card's bandwidth  571.4 tok/s; with TP over 1 card(s), best case  571.4 tok/s (ignores all-reduce)
  70B fp16 : weights  140.0 GB, needs >= 2 x 80 GB card(s); ceiling on ONE card's bandwidth   14.3 tok/s; with TP over 2 card(s), best case   28.6 tok/s (ignores all-reduce)
  70B 4-bit: weights   35.0 GB, needs >= 1 x 80 GB card(s); ceiling on ONE card's bandwidth   57.1 tok/s; with TP over 1 card(s), best case   57.1 tok/s (ignores all-reduce)
  FLOPs/byte ridge point = PEAK/BW = 156; batch-1 decode does ~1 FLOP per byte read (2 FLOPs per fp16 weight, 2 bytes)
  MFU at the 7B fp16 ceiling = 0.64%  (14 GFLOP per token x 143 tok/s / peak)
  batch b reads the weights once: ceiling in total tokens/s grows ~linearly until compute or KV reads bite:
    b=  1: memory time  7.00 ms, compute time  0.04 ms -> step ~  7.00 ms,      143 tok/s total (KV reads ignored)
    b=  8: memory time  7.00 ms, compute time  0.36 ms -> step ~  7.00 ms,     1143 tok/s total (KV reads ignored)
    b= 32: memory time  7.00 ms, compute time  1.44 ms -> step ~  7.00 ms,     4571 tok/s total (KV reads ignored)
    b=128: memory time  7.00 ms, compute time  5.74 ms -> step ~  7.00 ms,    18286 tok/s total (KV reads ignored)

B) CPU toy: y = W @ x for W of 4096 x 16384 float32 (268 MB), batch of 1..64 vectors (this machine, numpy; timings are noisy and machine-specific, look at the shape)
  batch  1:    8.30 ms, weight bytes streamed per result  268.4 MB, results/s      120, ms per vector  8.302
  batch  4:   16.78 ms, weight bytes streamed per result   67.1 MB, results/s      238, ms per vector  4.196
  batch 16:   19.49 ms, weight bytes streamed per result   16.8 MB, results/s      821, ms per vector  1.218
  batch 64:   37.10 ms, weight bytes streamed per result    4.2 MB, results/s     1725, ms per vector  0.580
```

**Follow-ups:**
- *Why does the ceiling overestimate?* It ignores KV reads, kernel launch gaps, all-reduce, dequantisation work and attention overheads.
- *Does a faster GPU always help decode?* Only if bandwidth rises; compare bandwidth, not FLOPs.
- *Does 4-bit give 4x?* Not exactly: dequantisation and non-weight traffic eat part of it (Q8).

**Common mistakes:** Using FLOPs to estimate batch-1 decode; forgetting a 70B fp16 model does not fit one 80 GB card; quoting nvidia-smi utilisation as efficiency; treating a weights-only ceiling as a prediction; mixing GB and GiB or bits and bytes.

### Q34 ⭐⭐ 🟡 Offline batch inference vs online serving: how do the objectives, batching, scheduling, cost and failure handling differ (throughput-optimised jobs, spot capacity, checkpointing, length sorting)?
**Asked at:** product companies, data and GenAI platform teams; interview-prep guide, not a candidate report contrasts chat with offline summarisation
**Say this first (1 line):** Online serving optimises latency percentiles under an SLO; offline batch optimises total throughput and cost per token, so it uses big batches, length sorting, spot capacity and checkpointing, and tolerates retries and long queues.

**Then explain:**
- **Objective:** online: TTFT/TPOT percentiles and goodput (Q2). Offline: tokens per GPU-hour and finishing the job; no one waits on a single request.
- **Batching and scheduling:** offline can run at the maximum batch and token budget the KV memory allows (the vLLM tuning docs note larger `max_num_batched_tokens` favours throughput and TTFT, smaller favours ITL; check live docs) and queue everything. Sort or bucket by length so long and short prompts are not mixed: in the toy, static padded batches of 32 were 23% useful in random order (26,361,920 padded vs 5,983,372 real tokens) and 98% useful when sorted by length (6,109,536). Continuous-batching engines pad much less, so sorting matters most for static or fixed-shape pipelines; it can still help scheduling and tail management.
- **Cost:** offline can run GPUs near full utilisation (Q13), use cheaper spot capacity, or use a provider's batch endpoint where offered (from memory, check current terms).
- **Failure handling:** make work idempotent: give each item an ID, write outputs in shards, track completed IDs, retry failed items, and checkpoint so a preemption loses little.
- **Spot and checkpoint interval:** for preemptions at rate lambda, checkpoint interval c and checkpoint cost d, a segment must finish uninterrupted; expected time is (T/c) x (e^(lambda(c+d)) - 1)/lambda. The simulation matched that closed form.

**Example:** A 20-hour job on spot GPUs with one preemption per 2 hours on average (assumed rate) and a 1.2-minute checkpoint: checkpointing every 0.1 h gives an expected 24.7 h, every 0.5 h 23.8 h, every 2.0 h 34.9 h, and with no checkpoint until the end (20 h) about 44,494 h in the formula (the simulation gave 44,080 h from 4,000 trials, noisy because the true value is dominated by rare long runs). The best interval on a grid was 0.25 h at 23.1 h. Too-rare checkpoints are catastrophic; too-frequent ones cost a little.

**Code:** (run with `python3 -I`; stdlib and numpy; synthetic prompt lengths; preemption rate and checkpoint cost are assumed. The closed form is checked against a Monte Carlo simulation.)
```python
# Offline batch inference toys (numpy + stdlib). Distributions and rates are SYNTHETIC/ASSUMED.
import math, random
import numpy as np
rng = np.random.default_rng(0)

# 1) Length sorting: a static (padded) batch costs batch_size * max_len in the batch. 10,000 prompts, lognormal lengths.
lens = np.clip(rng.lognormal(6.0, 0.9, 10000), 20, 4000).astype(int); B = 32
def padded_tokens(order):
    return sum(B * int(lens[order[i:i + B]].max()) for i in range(0, len(order), B))
real = int(lens.sum())
rand = padded_tokens(rng.permutation(len(lens))); srt = padded_tokens(np.argsort(lens))
print(f"real tokens {real:,d}; padded cost random order {rand:,d} ({real/rand:.0%} useful); sorted by length {srt:,d} ({real/srt:.0%} useful)")

# 2) Spot preemption with checkpoints. Job needs T hours of work; preemptions are Poisson with rate lam per hour;
#    a checkpoint every c hours costs d hours; after a preemption you resume from the last checkpoint (restart cost 0).
def closed_form(T, lam, c, d):
    seg = c + d                                   # one segment = work + checkpoint write; must finish uninterrupted
    return (T / c) * (math.exp(lam * seg) - 1) / lam
def simulate(T, lam, c, d, trials=4000, seed=1):
    g = random.Random(seed); tot = 0.0
    for _ in range(trials):
        done, t = 0.0, 0.0
        while done < T - 1e-12:
            seg = min(c, T - done) + d
            x = g.expovariate(lam)                 # time to next preemption
            if x >= seg: t += seg; done += min(c, T - done)
            else: t += x                           # lost the in-flight segment
        tot += t
    return tot / trials
T, lam, d = 20.0, 0.5, 0.02       # 20 h of work, one preemption per 2 h on average (ASSUMED), 1.2 min checkpoint cost
print("\nExpected wall time for 20 h of work, preemption rate 0.5/h (ASSUMED), checkpoint cost 0.02 h:")
print(f"{'checkpoint every':>17} {'closed form':>12} {'simulation':>11}")
for c in (0.1, 0.5, 2.0, 20.0):
    print(f"{c:15.1f} h {closed_form(T, lam, c, d):11.1f}h {simulate(T, lam, c, d):10.1f}h")
best = min((closed_form(T, lam, c, d), c) for c in np.arange(0.05, 5, 0.05))
print(f"best interval on a grid: {best[1]:.2f} h -> {best[0]:.1f} h expected (no checkpoints at all would be c=20)")
```
**Output (my run):**
```
real tokens 5,983,372; padded cost random order 26,361,920 (23% useful); sorted by length 6,109,536 (98% useful)

Expected wall time for 20 h of work, preemption rate 0.5/h (ASSUMED), checkpoint cost 0.02 h:
 checkpoint every  closed form  simulation
            0.1 h        24.7h       24.7h
            0.5 h        23.8h       23.8h
            2.0 h        34.9h       35.0h
           20.0 h     44493.7h    44080.2h
best interval on a grid: 0.25 h -> 23.1 h expected (no checkpoints at all would be c=20)
```

**Follow-ups:**
- *Why not run offline jobs on the online fleet?* They can starve interactive traffic; use a separate pool or low priority.
- *How do you resume?* From a manifest of completed item IDs, not a byte offset.
- *Does offline need TTFT?* No, but watch throughput per dollar and tail items that delay the last batch.

**Common mistakes:** Running offline jobs with online-style small batches; no idempotency so retries duplicate work; checkpointing never or too often; mixing very different lengths in one static batch; ignoring the final long-tail items that decide job completion time.

### Q35 ⭐⭐ 🟡 Hardware choice for serving: how do GPU memory capacity, memory bandwidth, FP8 support and interconnect decide between options such as L4, A100, H100 and H200-class cards, and when does a smaller or older card win on cost per token?
**Asked at:** product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report lists GPU selection (no prices quoted here)
**Say this first (1 line):** Memory capacity decides what fits and how many sequences you can batch, memory bandwidth decides decode speed, FP8 support and kernels decide how cheaply you can shrink the model, and interconnect decides whether tensor parallelism across cards is practical. A cheaper or older card wins when the model fits and the card stays busy.

**Then explain:**
- **Specs used (assumed, from memory, check vendor sheets):** L4 24 GB at about 300 GB/s; A100 80 GB at about 2,000 GB/s; H100 80 GB at about 3,350 GB/s; H200 141 GB at about 4,800 GB/s. Native FP8: L4 yes, A100 no, H100 and H200 yes (consistent with the vLLM quantization table I read listing FP8 W8A8 for Ada and Hopper, check live docs).
- **Toy (8B-like GQA, 4,096-token sequences, memory-bound step model):** in fp16, free KV room is 5.6 GB on L4 (10 sequences), 56.0 GB on A100 and H100 (104 sequences) and 110.9 GB on H200 (206). Relative to A100, estimated throughput at max batch is 0.05 (L4), 1.68 (H100) and 2.70 (H200). With 8-bit weights and KV: 0.11, 1.68 and 2.53.
- **Break-even rule:** a card wins on tokens per unit price when its price ratio to A100 is below its throughput ratio. With my toy numbers H100 must cost less than 1.68x an A100 per hour. I use no prices.
- **When the small or old card wins:** the model fits with KV room, traffic is low or spiky so a big card would idle (Q13), latency targets are loose, or the model is small enough that an L4-class card is the right size. In the toy L4 loses badly for an 8B model at this context because KV room is small and bandwidth is low.
- **Interconnect:** a 70B fp16 model has 140 GB of weights, so at least 2 x 80 GB cards (7 L4 cards), and tensor parallel needs fast links because each layer does an all-reduce (Q17). I did not model interconnect.
- **Quantization changes the choice:** 8-bit or 4-bit weights let a model fit on fewer or smaller cards (Q8, Q23), but FP8 speed needs native FP8 hardware and kernels.

**Example:** From the run, 8B-like model, 4,096-token context, fp16: A100 fits 104 sequences with an estimated 2,896 tokens/s at max batch; H100 the same 104 but 4,850 tokens/s because of bandwidth; H200 fits 206 and 7,811 tokens/s. If an H200-class card costs less than 2.7x an A100 in your contract, it wins on this memory-bound estimate; if your traffic only needs 300 tokens/s, neither is busy and the cheapest card that fits wins. Estimates, not measurements.

**Code:** (run with `python3 -I`; stdlib only; hardware numbers are assumed from memory and shapes are assumed. The throughput model is memory-bound only (weights read once per step plus each sequence's KV), ignoring compute limits, kernel quality and interconnect.)
```python
# Hardware comparison from ASSUMED, from-memory spec numbers (memory GB, bandwidth GB/s). CHECK VENDOR SHEETS before use.
# No prices appear; the output is the price ratio at which a card breaks even on tokens per unit price.
GB = 1e9
cards = {  # name: (HBM/GDDR GB, bandwidth GB/s, native FP8 tensor cores?)  ASSUMED values
    "L4":   (24, 300, True),
    "A100": (80, 2000, False),
    "H100": (80, 3350, True),
    "H200": (141, 4800, True),
}
# Workload: 8B-like GQA model (ASSUMED shapes), context 4096 per sequence. Throughput = memory-bound estimate only
# (each step reads weights once plus every running sequence's KV); compute limits and kernel quality are ignored.
def table(label, w_gb, kv_bytes):
    W = w_gb * GB; kv_seq = 2 * 32 * 8 * 128 * kv_bytes * 4096
    print(f"{label}: weights {w_gb} GB, KV per 4096-token sequence {kv_seq/GB:.2f} GB")
    print(f"  {'card':5} {'free for KV GB':>14} {'max seqs':>9} {'tok/s at max batch':>19} {'rel. to A100':>13}")
    out = {}
    for n, (mem, bw, fp8) in cards.items():
        free = mem * 0.9 * GB - W; seqs = max(int(free // kv_seq), 0)
        out[n] = seqs * (bw * GB) / (W + seqs * kv_seq) if seqs else 0.0
    for n, (mem, bw, fp8) in cards.items():
        seqs = max(int((mem * 0.9 * GB - W) // kv_seq), 0)
        print(f"  {n:5} {mem*0.9-w_gb:14.1f} {seqs:9d} {out[n]:19.0f} {out[n]/out['A100']:13.2f}")
    return out
fp16 = table("fp16 weights and fp16 KV", 16, 2)
print()
q8 = table("8-bit weights and 8-bit KV (assumes working kernels on every card)", 8, 1)
print("\nBreak-even rule: a card wins on tokens per unit price when (its price / A100 price) < (its throughput / A100 throughput).")
print("Break-even price ratios vs A100, fp16 case: " + ", ".join(f"{n} {fp16[n]/fp16['A100']:.2f}" for n in ("L4", "H100", "H200")))
print("Break-even price ratios vs A100, 8-bit case: " + ", ".join(f"{n} {q8[n]/q8['A100']:.2f}" for n in ("L4", "H100", "H200")))
print("\nFits-in-memory check for a 70B-like model, fp16 weights = 140 GB (ASSUMED), before any KV:")
for n, (mem, bw, fp8) in cards.items():
    print(f"  {n}: needs >= {int(-(-140 // (mem * 0.9)))} cards just to hold fp16 weights (more once KV and overhead are counted)")
print("\nNative FP8 in these ASSUMED specs:", ", ".join(f"{n}={'yes' if v[2] else 'no'}" for n, v in cards.items()))
```
**Output (my run):**
```
fp16 weights and fp16 KV: weights 16 GB, KV per 4096-token sequence 0.54 GB
  card  free for KV GB  max seqs  tok/s at max batch  rel. to A100
  L4               5.6        10                 140          0.05
  A100            56.0       104                2896          1.00
  H100            56.0       104                4850          1.68
  H200           110.9       206                7811          2.70

8-bit weights and 8-bit KV (assumes working kernels on every card): weights 8 GB, KV per 4096-token sequence 0.27 GB
  card  free for KV GB  max seqs  tok/s at max batch  rel. to A100
  L4              13.6        50                 700          0.11
  A100            64.0       238                6621          1.00
  H100            64.0       238               11091          1.68
  H200           118.9       442               16752          2.53

Break-even rule: a card wins on tokens per unit price when (its price / A100 price) < (its throughput / A100 throughput).
Break-even price ratios vs A100, fp16 case: L4 0.05, H100 1.68, H200 2.70
Break-even price ratios vs A100, 8-bit case: L4 0.11, H100 1.68, H200 2.53

Fits-in-memory check for a 70B-like model, fp16 weights = 140 GB (ASSUMED), before any KV:
  L4: needs >= 7 cards just to hold fp16 weights (more once KV and overhead are counted)
  A100: needs >= 2 cards just to hold fp16 weights (more once KV and overhead are counted)
  H100: needs >= 2 cards just to hold fp16 weights (more once KV and overhead are counted)
  H200: needs >= 2 cards just to hold fp16 weights (more once KV and overhead are counted)

Native FP8 in these ASSUMED specs: L4=yes, A100=no, H100=yes, H200=yes
```

**Follow-ups:**
- *Why can H200 help beyond bandwidth?* More memory per card means more KV room, hence a bigger batch and fewer TP shards.
- *PCIe vs NVLink?* For TP the all-reduce traffic makes link speed matter; for replicas it does not.
- *Is FP8 on Hopper a free win?* It needs supported kernels and a quality check (Q10, Q23).

**Common mistakes:** Comparing FLOPs instead of bandwidth and memory for decode; forgetting KV room; assuming an old card is cheaper per token without utilisation; ignoring interconnect for sharded models; trusting spec numbers from memory without checking.

### Q36 ⭐⭐ 🟡 llama.cpp, GGUF and Ollama: what are they for (CPU or Apple Silicon, edge, local development, hybrid CPU-GPU offload), how do GGUF quantization levels differ from GPTQ/AWQ, and where do they stop being the right tool for a server?
**Asked at:** product companies, startups, edge and on-device teams; interview-prep guide, not a candidate report
**Say this first (1 line):** llama.cpp is a C/C++ inference engine, GGUF is its single-file model format with block quantization, and Ollama is a local runner built around that stack. They are great for CPU, Apple Silicon, edge and hybrid CPU-GPU offload, and they stop being the right tool when you need high-concurrency batching, multi-GPU scaling and fleet operations.

**Then explain:**
- **What they are:** the llama.cpp repo describes a C/C++ library with GGUF conversion, 1.5 to 8-bit quantization, many hardware backends, CPU plus GPU hybrid inference and an OpenAI-compatible server. Ollama (from memory, check) wraps this for easy local use.
- **GGUF quantization:** weights are stored in blocks with a per-block scale. From memory of ggml, Q4_0 is blocks of 32 with an fp16 scale, so (32 x 4 + 16)/32 = 4.5 bits per weight, and Q8_0 is 8.5. A 7B model is then about 3.94 GB at Q4_0, 7.44 GB at Q8_0 and 14 GB in fp16. K-quants and importance-matrix variants exist (from memory, check the repo).
- **Block size matters:** in the toy, 4-bit absmax with one scale for a whole tensor had MSE 1.522e-05 on Gaussian weights; blocks of 1024, 128 and 32 gave 8.280e-06, 5.574e-06 and 3.827e-06. With 64 synthetic outliers (x30) the whole-tensor error was 4.036e-04 against 1.055e-05 for blocks of 32. Small blocks cost extra scale bits (4.50 vs 4.00 bits per weight).
- **Versus GPTQ and AWQ:** GGUF levels are a storage and runtime format with simple block scales; GPTQ and AWQ are calibration-based methods (second-order and activation-aware, per the abstracts I opened) packaged for GPU kernels in engines such as vLLM (Q9).
- **Hybrid offload:** layers that do not fit on the GPU run on the CPU and the token pays both. With assumed 300 GB/s GPU and 50 GB/s CPU bandwidth and a 3.9 GB model, the weights-only ceiling is 76.9 tokens/s with all 32 layers on GPU, 34.2 with 24, 22.0 with 16 and 12.8 with none.
- **Where they stop:** many concurrent users with tight SLOs, large-scale batching and paged KV, multi-node tensor parallelism, autoscaling and observability. The llama.cpp server has parallel slots and continuous batching (from memory, check) but is not designed as a fleet engine; the TGI docs banner (read 2026-10-24) lists vLLM, SGLang, llama.cpp and MLX as the engines it recommends instead.

**Example:** A laptop demo for a 7B model: Q4_0 is about 3.94 GB, which fits in 8 GB of memory. At an assumed 50 GB/s of memory bandwidth the weights-only ceiling is 50/3.94, roughly 13 tokens per second, close to the 0-layers-on-GPU line in the run (12.8, which used a rounded 3.9 GB). For 200 concurrent web users with a latency SLO you would move to a GPU engine with continuous batching and paged KV (Q5, Q6, Q12).

**Code:** (run with `python3 -I`; numpy only; a simplified absmax block quantizer in the style of Q4_0 and Q8_0 (not the real ggml code), synthetic Gaussian weights with synthetic outliers, assumed bandwidths.)
```python
# GGUF-style block quantization toy (numpy). Block layouts for Q4_0 and Q8_0 are from memory of ggml (check the repo):
# blocks of 32 weights, one fp16 scale per block; Q4_0 = 4-bit values, Q8_0 = 8-bit values. This is a simplified re-implementation.
import numpy as np
rng = np.random.default_rng(0)
print("bits per weight incl. the fp16 scale (block of 32):  Q4_0 = (32*4+16)/32 = %.2f   Q8_0 = (32*8+16)/32 = %.2f" % ((32*4+16)/32, (32*8+16)/32))
for name, bpw in (("Q4_0", 4.5), ("Q8_0", 8.5), ("fp16", 16)):
    print(f"  7B model at {name}: {7e9*bpw/8/1e9:5.2f} GB")

def quant_block(w, bits, block):                      # symmetric absmax per block, round to nearest
    x = w.reshape(-1, block); qmax = 2 ** (bits - 1) - 1
    scale = np.abs(x).max(axis=1, keepdims=True) / qmax; scale[scale == 0] = 1
    q = np.clip(np.round(x / scale), -qmax - 1, qmax)
    return (q * scale).reshape(w.shape)
n = 1 << 16
w = rng.standard_normal(n) * 0.02
w_out = w.copy(); idx = rng.choice(n, 64, replace=False); w_out[idx] *= 30         # a few large outlier weights (synthetic)
for label, arr in (("gaussian weights", w), ("with 64 outliers x30", w_out)):
    print(f"\n{label}: mean squared error of 4-bit absmax quantisation")
    for block in (n, 1024, 128, 32):
        err = np.mean((arr - quant_block(arr, 4, block)) ** 2)
        bits = 4 + 16 / block
        print(f"  block size {block:6d}{' (whole tensor)' if block == n else '':16}: MSE {err:.3e}   bits/weight {bits:5.2f}")
print("\n8-bit, block 32, outlier tensor: MSE %.3e (vs 4-bit block 32 %.3e)" % (np.mean((w_out - quant_block(w_out, 8, 32)) ** 2), np.mean((w_out - quant_block(w_out, 4, 32)) ** 2)))

# Hybrid CPU-GPU offload: layers that do not fit in GPU memory run on the CPU; each token pays both parts (sequentially).
layers, model_gb = 32, 3.9                           # ~7B at Q4_0 (from the calculation above, rounded)
gpu_bw, cpu_bw = 300.0, 50.0                         # ASSUMED GB/s: small GPU (L4-class) and desktop DDR
print("\nHybrid offload ceiling (ASSUMED bandwidths: GPU 300 GB/s, CPU 50 GB/s; weights-only memory-bound model):")
for on_gpu in (32, 24, 16, 0):
    t = model_gb * (on_gpu / layers) / gpu_bw + model_gb * ((layers - on_gpu) / layers) / cpu_bw
    print(f"  {on_gpu:2d}/{layers} layers on GPU: ceiling {1/t:6.1f} tokens/s")
```
**Output (my run):**
```
bits per weight incl. the fp16 scale (block of 32):  Q4_0 = (32*4+16)/32 = 4.50   Q8_0 = (32*8+16)/32 = 8.50
  7B model at Q4_0:  3.94 GB
  7B model at Q8_0:  7.44 GB
  7B model at fp16: 14.00 GB

gaussian weights: mean squared error of 4-bit absmax quantisation
  block size  65536 (whole tensor) : MSE 1.522e-05   bits/weight  4.00
  block size   1024                : MSE 8.280e-06   bits/weight  4.02
  block size    128                : MSE 5.574e-06   bits/weight  4.12
  block size     32                : MSE 3.827e-06   bits/weight  4.50

with 64 outliers x30: mean squared error of 4-bit absmax quantisation
  block size  65536 (whole tensor) : MSE 4.036e-04   bits/weight  4.00
  block size   1024                : MSE 1.893e-04   bits/weight  4.02
  block size    128                : MSE 3.257e-05   bits/weight  4.12
  block size     32                : MSE 1.055e-05   bits/weight  4.50

8-bit, block 32, outlier tensor: MSE 6.877e-08 (vs 4-bit block 32 1.055e-05)

Hybrid offload ceiling (ASSUMED bandwidths: GPU 300 GB/s, CPU 50 GB/s; weights-only memory-bound model):
  32/32 layers on GPU: ceiling   76.9 tokens/s
  24/32 layers on GPU: ceiling   34.2 tokens/s
  16/32 layers on GPU: ceiling   22.0 tokens/s
   0/32 layers on GPU: ceiling   12.8 tokens/s
```

**Follow-ups:**
- *Should you serve GGUF through vLLM?* Support exists for some GGUF models in some engines but varies; check live docs, and prefer GPTQ, AWQ or FP8 for GPU serving.
- *Why is Q4 not 4 bits?* Scales add overhead: 4.5 bits per weight at block size 32.
- *When is Ollama enough?* Local development, demos and single-user tools.

**Common mistakes:** Treating a laptop tokens-per-second figure as server capacity; thinking GGUF Q4 equals GPTQ or AWQ 4-bit; ignoring offload cost when part of the model sits on CPU; using it for multi-tenant production traffic; forgetting that quantization quality needs an eval (Q10).

### Q37 ⭐⭐ 🟡 Replicas behind a load balancer: why does prefix caching and KV reuse need cache-aware routing or sticky sessions, what are the risks (hot spots, uneven load), and what do round-robin and least-loaded routing get wrong for LLMs?
**Asked at:** inference-platform teams, platform teams; TGI's docs note the replica cache problem; interview-prep guide, not a candidate report lists KV-cache-aware routing
**Say this first (1 line):** Prefix caching lives inside each replica, so a router that scatters requests sharing a prefix across replicas throws the cache away; route by prefix affinity, but cap the load, because pure stickiness creates hot spots.

**Then explain:**
- **Why routing matters:** every replica keeps its own KV blocks and prefix cache in its own GPU memory (how an engine hashes and evicts blocks is Part 10 Q14). A hit needs the request to land on a replica that already holds those blocks. The TGI docs (opened for this book, as summarised) note this replica caveat and suggest sticky sessions.
- **Round-robin gets wrong:** it ignores the cache (each replica sees all prefixes, so its small cache thrashes) and ignores request size (a 30k-token prompt costs far more than a 300-token one but counts as "one request").
- **Least-loaded gets wrong:** better tails than round-robin, but still cache-blind. Count load in work (queued tokens or KV blocks), not connections or request counts.
- **Sticky or hash routing:** best hit rate, but traffic is skewed (a few system prompts or tenants dominate), so one replica gets the hot prefix and saturates.
- **Middle path (bounded-load affinity):** send to a replica that holds the prefix unless its backlog is more than a slack above the least-loaded replica; then spill to the least-loaded one, which warms its own copy. Hot prefixes end up replicated on a few replicas.
- **Other risks:** the router needs a view of replica cache state (hash of the first N tokens, or replicas report cached blocks); scale-out or a restart reshuffles a hash ring and every cache goes cold; a cache shared across tenants can leak timing information (the vLLM docs read on 2026-10-24 describe a cache salt for isolation; check live docs). Cache-aware routers exist in some stacks (from memory, check); Mooncake's paper describes KVCache-centric scheduling (authors' design).
- **Toy demo (synthetic, assumed constants, no real engine):** 4 replicas, 12 shared prefixes with Zipf-skewed popularity, each replica's LRU cache holds 3 prefixes, service time = 0.05 ms per uncached prompt token + 20 ms.

**Example:** from the run, at 80 req/s the hottest prefix is 36% of traffic. Round-robin and least-loaded get a 0.46 prefix hit rate and the queue grows for the whole run (p50 84,900 ms and 81,354 ms; that is an overloaded queue, not a steady state). Sticky gets hit rate 1.00 but one replica carries 1.79x the mean load, p99 18,952 ms. Cache-aware with a load bound gets 0.95 hit, load 1.03x, p50 52 ms, p99 226 ms. At 32 req/s sticky was actually the best p99 (94 ms vs 122 ms), so skew only hurts when load is high. At 110 req/s everything is saturated and the bounded router still queues (p50 9,505 ms): routing cannot create capacity.

**Code:** (run with `python3 -I`; stdlib only; toy simulation, not a benchmark)
```python
# TOY routing simulation (synthetic workload, assumed constants; no real engine, no GPU timing).
# 4 replicas, each a FIFO server with an LRU prefix cache. 12 shared prefixes (system prompts), Zipf-skewed popularity.
import random, bisect, collections

N_REP, N_PREFIX, CACHE_SLOTS = 4, 12, 3        # assumed: each replica can keep 3 prefixes of KV
PREFIX_TOK, SUFFIX_TOK = 2000, 200             # assumed prompt shape
MS_PER_PREFILL_TOK, DECODE_MS = 0.05, 20.0     # assumed service-time model: service = uncached*0.05 ms + 20 ms
RATE_PER_S, N_REQ = 32.0, 20000                # assumed arrival rate (Poisson) and run length

def make_workload(seed, rate=RATE_PER_S):
    rnd = random.Random(seed)
    w = [1.0 / (i + 1) ** 1.1 for i in range(N_PREFIX)]          # Zipf-like popularity
    cum = [sum(w[:i + 1]) for i in range(N_PREFIX)]
    t, reqs = 0.0, []
    for _ in range(N_REQ):
        t += rnd.expovariate(rate) * 1000.0                # ms
        reqs.append((t, bisect.bisect_left(cum, rnd.random() * cum[-1])))
    return reqs

class Replica:
    def __init__(self):
        self.free_at = 0.0
        self.cache = collections.OrderedDict()                    # LRU of prefix ids
    def backlog(self, t): return max(0.0, self.free_at - t)
    def serve(self, t, pid):
        hit = pid in self.cache
        if hit: self.cache.move_to_end(pid)
        else:
            self.cache[pid] = True
            if len(self.cache) > CACHE_SLOTS: self.cache.popitem(last=False)
        uncached = SUFFIX_TOK + (0 if hit else PREFIX_TOK)
        start = max(t, self.free_at)
        self.free_at = start + uncached * MS_PER_PREFILL_TOK + DECODE_MS
        return hit, self.free_at - t                               # latency = wait + service

def route_rr(reps, t, pid, i):          return i % N_REP
def route_least(reps, t, pid, i):       return min(range(N_REP), key=lambda r: reps[r].backlog(t))
def route_sticky(reps, t, pid, i):      return pid % N_REP         # prefix -> fixed replica
def route_aware(reps, t, pid, i, slack_ms=150.0):
    ll = route_least(reps, t, pid, i)
    holders = [r for r in range(N_REP) if pid in reps[r].cache]
    if holders:
        best = min(holders, key=lambda r: reps[r].backlog(t))
        if reps[best].backlog(t) <= reps[ll].backlog(t) + slack_ms: return best   # bounded-load affinity
    return ll

def run(router, reqs):
    reps = [Replica() for _ in range(N_REP)]
    lat, hits, per = [], 0, [0] * N_REP
    for i, (t, pid) in enumerate(reqs):
        r = router(reps, t, pid, i)
        hit, l = reps[r].serve(t, pid)
        lat.append(l); hits += hit; per[r] += 1
    lat.sort()
    pct = lambda p: lat[min(len(lat) - 1, int(p * len(lat)))]
    return hits / len(reqs), pct(0.50), pct(0.99), max(per) / (len(reqs) / N_REP)

for rate in (32.0, 80.0, 110.0):                  # offered load in requests/s (assumed sweep)
    reqs = make_workload(7, rate)
    share = collections.Counter(p for _, p in reqs)
    print(f"\noffered {rate:.0f} req/s over {N_REP} replicas; hottest prefix = {share.most_common(1)[0][1] / N_REQ:.2f} of traffic (synthetic)")
    print(f"{'router':24}{'prefix hit':>11}{'p50 ms':>9}{'p99 ms':>9}{'max/mean load':>15}")
    for name, fn in [("round-robin", route_rr), ("least-loaded", route_least),
                     ("sticky (hash prefix)", route_sticky), ("cache-aware+load bound", route_aware)]:
        h, p50, p99, imb = run(fn, reqs)
        print(f"{name:24}{h:11.2f}{p50:9.0f}{p99:9.0f}{imb:15.2f}")
```
**Output (my run):**
```

offered 32 req/s over 4 replicas; hottest prefix = 0.36 of traffic (synthetic)
router                   prefix hit   p50 ms   p99 ms  max/mean load
round-robin                    0.46      130      400           1.00
least-loaded                   0.46      130      265           1.19
sticky (hash prefix)           1.00       30       94           1.79
cache-aware+load bound         1.00       30      122           2.04

offered 80 req/s over 4 replicas; hottest prefix = 0.36 of traffic (synthetic)
router                   prefix hit   p50 ms   p99 ms  max/mean load
round-robin                    0.46    84900   171199           1.00
least-loaded                   0.47    81354   164432           1.00
sticky (hash prefix)           1.00       79    18952           1.79
cache-aware+load bound         0.95       52      226           1.03

offered 110 req/s over 4 replicas; hottest prefix = 0.36 of traffic (synthetic)
router                   prefix hit   p50 ms   p99 ms  max/mean load
round-robin                    0.46   118700   238253           1.00
least-loaded                   0.46   118411   236029           1.01
sticky (hash prefix)           1.00      146    85187           1.79
cache-aware+load bound         0.90     9505    17260           1.02
```

**Follow-ups:**
- *What do you hash on?* The shared prefix (system-prompt id or hash of the first block or two of tokens) for stateless traffic; the conversation id for multi-turn chat, so each turn finds its own history.
- *What if one prefix is hotter than a replica can serve?* Allow it on several replicas (bounded-load spill, or hash to 2 candidates and pick the less loaded).
- *How do you know routing is working?* Per-replica prefix hit rate, uncached tokens per replica, queue depth in tokens, and the spread between replicas.

**Common mistakes:** equating "least connections" with balanced work; sticky sessions with no load bound; forgetting that a rollout or scale event empties the caches; benchmarking routing with a single repeated prompt; ignoring that overload cannot be fixed by smarter routing.

### Q38 ⭐ 🟡 Code: write a toy continuous-batching scheduler simulation (arrivals, per-request output lengths, a batch-slot limit) and compare it with static batching on throughput and latency percentiles.
**Asked at:** inference-platform teams, AI labs, live-coding rounds; interview-prep guide, not a candidate report lists a request scheduler with priority and preemption as a coding round
**Say this first (1 line):** In a toy simulation, continuous batching refills a freed slot on the very next step, so the server stays full and short requests leave early, while static batching holds every slot until the longest request in the batch finishes.

**Then explain:**
- **Static batching:** take up to B waiting requests, run until the longest finishes, return them together. A request with 5 tokens waits for its batch-mate with 200. Slots sit idle after their request is done.
- **Continuous (iteration-level) batching:** at every decode step, admit waiting requests into free slots and retire finished ones. This is the idea in Orca (OSDI 2022; the authors report up to 36.9x throughput vs FasterTransformer on GPT-3 175B at the same latency, in their setup) and is the default in modern engines (details in Part 10 Q6).
- **Toy assumptions (synthetic):** one step emits one token per active request; step time does not depend on batch size (real engines are not exactly flat, Part 10 Q7); no prefill; no KV limit; lognormal output lengths with mean about 40 tokens; 8 slots; Poisson arrivals.
- **Check built in:** with equal output lengths arriving together both schedulers must finish 16 requests x 10 tokens on 8 slots in 20 steps; the code asserts that.
- **Reading the result:** with 8 slots and skewed lengths, static batching tops out near 3 tokens per step (about 37% of the 8-slot peak) because slots idle waiting for the longest request.

**Example:** at 0.05 req/step (about 2 tokens per step offered) both schedulers deliver the same throughput, 2.03 tokens per step, but latency differs: static p50 139.7 / p99 582.5 steps, continuous p50 28.9 / p99 190.0 steps. At 0.10 req/step offered load is about 4 tokens per step, above static's roughly 3 per step ceiling: static's backlog grows (p50 5,741 steps; that number grows with run length, it is not a steady state) while continuous delivers 4.06 tokens per step at p50 29.5, p99 190.6. At 0.17 it reaches 6.87 of 8 with p99 217.6 steps.

**Code:** (run with `python3 -I`; stdlib only; synthetic arrivals)
```python
# TOY scheduler simulation in units of decode steps. One step emits one token for every active request.
# Assumption: step time is the same for any batch size up to the slot limit (decode is memory-bound; real engines are not exactly flat).
import random, math

def make_requests(n, rate_per_step, seed, mean_out=40):
    rnd = random.Random(seed)
    t, reqs = 0.0, []
    for i in range(n):
        t += rnd.expovariate(rate_per_step)
        out = max(1, int(rnd.lognormvariate(math.log(mean_out) - 0.5 * 0.8 ** 2, 0.8)))   # skewed output lengths (assumed lognormal)
        reqs.append([i, t, out])                      # id, arrival step (float), output tokens
    return reqs

def sim_static(reqs, slots):
    """Static batching: take up to `slots` waiting requests, run until the LONGEST finishes, then take the next batch."""
    t, i, done = 0.0, 0, {}
    while i < len(reqs):
        t = max(t, reqs[i][1])                        # idle until the next arrival
        batch = [r for r in reqs[i:i + slots] if r[1] <= t] or [reqs[i]]
        i += len(batch)
        t += max(r[2] for r in batch)                 # the batch holds the GPU until its LONGEST request finishes
        for r in batch: done[r[0]] = t                # classic static batching returns the whole batch together
    return done, t

def sim_continuous(reqs, slots):
    """Continuous batching: each step, fill free slots from the queue, emit one token per active request, free slots at EOS."""
    t, i, active, done, waiting = 0.0, 0, [], {}, []
    n = len(reqs)
    while len(done) < n:
        while i < n and reqs[i][1] <= t: waiting.append(reqs[i]); i += 1
        while waiting and len(active) < slots:
            r = waiting.pop(0); active.append([r[0], r[2]])
        if not active:
            t = reqs[i][1]; continue
        t += 1.0
        for a in active: a[1] -= 1
        for a in [a for a in active if a[1] == 0]: done[a[0]] = t
        active = [a for a in active if a[1] > 0]
    return done, t

def report(name, reqs, done, end, slots):
    lat = sorted(done[r[0]] - r[1] for r in reqs)
    tokens = sum(r[2] for r in reqs)
    p = lambda q: lat[min(len(lat) - 1, int(q * len(lat)))]
    print(f"{name:11} tokens/step {tokens / end:6.2f} (max {slots})  latency p50 {p(.5):7.1f}  p95 {p(.95):7.1f}  p99 {p(.99):7.1f}  (steps)")

SLOTS = 8
# Check 1: equal output lengths, all arrive at t=0 -> both schedulers must give identical results (known closed form: 16 requests x 10 steps / 8 slots = 20 steps).
eq = [[i, 0.0, 10] for i in range(16)]
ds, es = sim_static(eq, SLOTS); dc, ec = sim_continuous(eq, SLOTS)
assert es == ec == 20.0, (es, ec)
print("check: equal lengths, simultaneous arrival -> both finish in", es, "steps (closed form 20)")
for rate in (0.05, 0.10, 0.17):                             # requests per step; capacity is roughly SLOTS/mean_out = 0.2 req/step
    reqs = make_requests(3000, rate, seed=1)
    print(f"\narrival rate {rate} req/step, mean output 40 tokens, {SLOTS} slots (synthetic)")
    d, e = sim_static(reqs, SLOTS);     report("static", reqs, d, e, SLOTS)
    d, e = sim_continuous(reqs, SLOTS); report("continuous", reqs, d, e, SLOTS)
```
**Output (my run):**
```
check: equal lengths, simultaneous arrival -> both finish in 20.0 steps (closed form 20)

arrival rate 0.05 req/step, mean output 40 tokens, 8 slots (synthetic)
static      tokens/step   2.03 (max 8)  latency p50   139.7  p95   455.1  p99   582.5  (steps)
continuous  tokens/step   2.03 (max 8)  latency p50    28.9  p95   110.8  p99   190.0  (steps)

arrival rate 0.1 req/step, mean output 40 tokens, 8 slots (synthetic)
static      tokens/step   2.98 (max 8)  latency p50  5741.2  p95 10269.0  p99 10714.6  (steps)
continuous  tokens/step   4.06 (max 8)  latency p50    29.5  p95   112.4  p99   190.6  (steps)

arrival rate 0.17 req/step, mean output 40 tokens, 8 slots (synthetic)
static      tokens/step   2.99 (max 8)  latency p50 11574.8  p95 21345.4  p99 22505.6  (steps)
continuous  tokens/step   6.87 (max 8)  latency p50    44.7  p95   137.0  p99   217.6  (steps)
```

**Follow-ups:**
- *Why is p99 still 190 steps at low load for continuous batching?* That is the output-length tail itself (long generations take that many steps), not queueing.
- *What does the toy leave out?* Prefill cost and chunking (Part 10 Q20), KV-memory limits and preemption (Q21), and step time rising with batch size.
- *How would you add priorities?* Replace the FIFO `waiting` list with a priority queue and decide who may preempt a running request.

**Common mistakes:** comparing the schedulers only at light load (they look equal); quoting the toy's ratios as engine speed-ups; measuring static latency per request instead of per batch return; forgetting that real step time grows with batch size.

### Q39 ⭐ 🔴 Code: write a toy paged KV-block allocator (fixed-size blocks, block tables, reference counts, shared prefixes with copy-on-write, free list) and show fragmentation compared with contiguous allocation.
**Asked at:** inference-platform teams, AI labs, live-coding rounds; interview-prep guide, not a candidate report lists a KV-cache memory allocator as a coding round
**Say this first (1 line):** A paged KV allocator hands out fixed-size blocks from a free list, each sequence keeps a block table, shared prefixes just bump reference counts, and a write to a shared block first copies it (copy-on-write); that removes the waste of reserving a max-length contiguous slot per request.

**Then explain:**
- **Structure:** free list of physical block ids, a refcount per block, and per sequence a block table (logical block index to physical id). Lookup is one indirection per block. PagedAttention's analogy is OS virtual memory paging (arXiv 2309.06180, abstract; the authors report near-zero waste and 2-4x throughput vs FasterTransformer and Orca at the same latency, in their setup). Engine-level detail is Part 10 Q5.
- **Fork and share:** forking a sequence copies only the table and increments refcounts. Used for parallel sampling, beam search and shared system prompts.
- **Copy-on-write:** appending to a block with refcount above 1 allocates a new block, copies its contents, decrements the old refcount and writes to the copy. Full shared blocks are never written, so only the partial last block is ever copied.
- **Fragmentation:** contiguous max-length slots waste the unused tail (internal fragmentation) and leave holes (external). Paged blocks waste at most part of the last block per sequence, and any free block is usable, so external fragmentation disappears by construction.
- **Block size trade:** small blocks waste less but make tables longer and gathers less efficient; the 16 tokens used here is a toy constant (the vLLM kernel doc, flagged historical, uses a 16-token block in its example; check current docs).
- **Not modelled:** the actual tensors, the attention kernel, eviction and prefix hashing (Part 10 Q14), swapping.

**Example:** from the run: one 40-token parent plus 3 forks use 3 blocks instead of 12. After each child appends 20 divergent tokens the total is 9 blocks, parent data unchanged, and shared full blocks show refcount 4. With 200 synthetic sequences (72,272 actual tokens), max-length slots of 2048 tokens reserve 409,600 token slots (82.4% wasted) vs 73,664 (1.9% wasted) for 16-token blocks. In an alloc/free churn test, contiguous first-fit failed 12 times although total free space was enough, paged 0.

**Code:** (run with `python3 -I`; stdlib only; no tensors, content is a list of token ids so copy-on-write can be tested)
```python
# TOY paged KV-block allocator: block table per sequence, refcounts, shared prefix, copy-on-write, free list.
# Units are tokens/blocks; no tensors. Block size 16 tokens (vLLM's historical default example; just an assumed constant here).
import random

class PagedAllocator:
    def __init__(self, n_blocks, block_size=16):
        self.bs, self.n = block_size, n_blocks
        self.free = list(range(n_blocks))             # free list (stack)
        self.ref = [0] * n_blocks                     # reference counts
        self.tables = {}                              # seq id -> list of physical block ids
        self.lens = {}                                # seq id -> tokens stored
        self.content = {}                             # block id -> list of token ids (stands in for the KV data, so we can test CoW)
    def _alloc(self):
        if not self.free: raise MemoryError("out of KV blocks")
        b = self.free.pop(); self.ref[b] = 1; self.content[b] = []; return b
    def _release(self, b):
        self.ref[b] -= 1
        if self.ref[b] == 0: self.free.append(b); self.content.pop(b, None)
    def add_seq(self, sid, tokens):
        self.tables[sid], self.lens[sid] = [], 0
        for t in tokens: self.append(sid, t)
    def append(self, sid, tok):
        tab = self.tables[sid]
        if self.lens[sid] % self.bs == 0:             # last block full (or none): take a fresh block
            tab.append(self._alloc())
        elif self.ref[tab[-1]] > 1:                   # last block is shared: copy-on-write before writing
            old = tab[-1]; new = self._alloc()
            self.content[new] = list(self.content[old]); self.ref[old] -= 1; tab[-1] = new
        self.content[tab[-1]].append(tok); self.lens[sid] += 1
    def fork(self, parent, child):                    # share every block, just bump refcounts
        self.tables[child] = list(self.tables[parent]); self.lens[child] = self.lens[parent]
        for b in self.tables[child]: self.ref[b] += 1
    def free_seq(self, sid):
        for b in self.tables.pop(sid): self._release(b)
        self.lens.pop(sid)
    def read(self, sid): return [t for b in self.tables[sid] for t in self.content[b]]
    def check(self):                                  # invariants
        used = {b for tab in self.tables.values() for b in tab}
        assert len(used) + len(self.free) == self.n and not used & set(self.free)
        for b in used: assert self.ref[b] == sum(t.count(b) for t in self.tables.values())

# --- 1. correctness: shared prefix + copy-on-write
A = PagedAllocator(n_blocks=64)
prefix = list(range(40))                              # 40 tokens = 2 full blocks + 8 tokens in block 3
A.add_seq("p", prefix)
for k in range(3): A.fork("p", f"c{k}")
print("blocks used by 1 parent + 3 forks sharing a 40-token prefix:", 64 - len(A.free), "(no sharing would need", 4 * 3, ")")
for k in range(3):
    for j in range(20): A.append(f"c{k}", 1000 * (k + 1) + j)     # each child diverges for 20 tokens -> CoW on the partial block
A.check()
assert A.read("p") == prefix                          # parent's data untouched by children's writes
assert A.read("c1") == prefix + [2000 + j for j in range(20)]
print("after 20 divergent tokens per child: blocks used", 64 - len(A.free), "; parent unchanged: True; refcounts of shared full blocks:", [A.ref[b] for b in A.tables["p"][:2]])
for s in ["c0", "c1", "c2", "p"]: A.free_seq(s)
A.check(); assert len(A.free) == 64
print("all freed -> free list back to 64 blocks")

# --- 2. fragmentation: contiguous reservation at max length vs paged, same sequences
rnd = random.Random(0)
MAX_LEN, N_SEQ, BS = 2048, 200, 16
lens = [min(MAX_LEN, max(1, int(rnd.lognormvariate(5.5, 0.9)))) for _ in range(N_SEQ)]   # synthetic actual lengths (mean around 300 tokens)
actual = sum(lens)
contig_reserved = N_SEQ * MAX_LEN                     # slot sized for the max length (what a pre-allocating system does)
paged_reserved = sum(-(-l // BS) * BS for l in lens)  # ceil to whole blocks
print(f"\n{N_SEQ} synthetic sequences, actual tokens {actual}")
print(f"contiguous max-length slots: reserved {contig_reserved}, wasted {1 - actual / contig_reserved:.1%}")
print(f"paged 16-token blocks:       reserved {paged_reserved}, wasted {1 - actual / paged_reserved:.1%}")

# --- 3. external fragmentation: contiguous first-fit arena vs paged, random alloc/free churn
def churn_contiguous(arena, steps, seed):
    r = random.Random(seed); live = {}                # start -> size
    def first_fit(sz):
        pos = 0
        for s in sorted(live):
            if s - pos >= sz: return pos
            pos = s + live[s]
        return pos if arena - pos >= sz else None
    fails_with_space = 0
    for i in range(steps):
        if live and r.random() < 0.5:
            del live[r.choice(list(live))]
        else:
            sz = r.randint(20, 400)
            pos = first_fit(sz)
            if pos is None:
                if arena - sum(live.values()) >= sz: fails_with_space += 1   # enough TOTAL space, no contiguous hole
            else: live[pos] = sz
    return fails_with_space
def churn_paged(n_blocks, steps, seed):
    r = random.Random(seed); P = PagedAllocator(n_blocks); live = []; fails_with_space = 0; sid = 0
    for i in range(steps):
        if live and r.random() < 0.5:
            P.free_seq(live.pop(r.randrange(len(live))))
        else:
            sz = r.randint(20, 400); need = -(-sz // P.bs)
            if need > len(P.free):
                if len(P.free) * P.bs >= sz: fails_with_space += 1            # cannot happen by construction
            else:
                sid += 1; P.add_seq(sid, list(range(sz))); live.append(sid)
    return fails_with_space
print("\nallocation failures although total free space was enough (4000 alloc/free events, arena of 8000 tokens):")
print("  contiguous first-fit:", churn_contiguous(8000, 4000, 1), "   paged:", churn_paged(8000 // 16, 4000, 1))
```
**Output (my run):**
```
blocks used by 1 parent + 3 forks sharing a 40-token prefix: 3 (no sharing would need 12 )
after 20 divergent tokens per child: blocks used 9 ; parent unchanged: True; refcounts of shared full blocks: [4, 4]
all freed -> free list back to 64 blocks

200 synthetic sequences, actual tokens 72272
contiguous max-length slots: reserved 409600, wasted 82.4%
paged 16-token blocks:       reserved 73664, wasted 1.9%

allocation failures although total free space was enough (4000 alloc/free events, arena of 8000 tokens):
  contiguous first-fit: 12    paged: 0
```

**Follow-ups:**
- *Why is "0 failures" for paged not a surprise?* It is by construction: any free block fits any request block, so a failure means the pool is truly short. The test mainly shows what contiguous allocation costs.
- *What happens when the pool runs out?* The engine must preempt (recompute or swap) or reject; Part 10 Q21.
- *Where does prefix caching differ?* It keeps freed blocks hashed for reuse instead of returning them immediately (Part 10 Q14).

**Common mistakes:** forgetting copy-on-write on the partial last block (children then corrupt each other); freeing a shared block when one owner finishes; counting reserved rather than used tokens; claiming paging reduces compute (it reduces memory waste and so allows bigger batches).

### Q40 ⭐ 🟡 Code: implement INT8 per-tensor and per-channel weight quantize and dequantize in NumPy, measure the error (MSE, max error, output error on a matmul), and show what an outlier channel does.
**Asked at:** product companies, GenAI startups, live-coding rounds
**Say this first (1 line):** Symmetric INT8 maps each weight to round(w / scale) with scale = absmax / 127; per-tensor uses one scale for the whole matrix, per-channel uses one per output row, and one large-magnitude channel wrecks per-tensor accuracy because it inflates the shared step size.

**Then explain:**
- **Quantize and dequantize:** `q = clip(round(W / s), -127, 127)` as int8, `W_hat = q * s`. Rounding error per element is at most s/2; the code asserts that.
- **Per-tensor:** one `s`. Simple, but every weight gets the same step size, so small-magnitude rows are coarsely represented if any single weight is large.
- **Per-channel (per output row):** one `s` per row, applied after the integer matmul. Cost is a vector of scales; accuracy is usually clearly better.
- **What I measure:** MSE, max abs error, and relative error of `X @ W.T` against the float result on synthetic activations (weight-only quantization: X stays float).
- **Honest scoping:** my outlier is a whole output row scaled 40x (assumed). Outliers that matter most in LLMs are activation channels (input features), which per-output-channel weight scales do not fix; LLM.int8() (separate 16-bit outlier path) and SmoothQuant (migrate activation outliers into weights offline) address that, per their abstracts. See Part 10 Q8, Q9, Q23.

**Example:** from the run. Well-behaved Gaussian weights: per-tensor MSE 4.357e-08, relative matmul error 0.01042; per-channel MSE 2.232e-08, relative error 0.00743. That is a modest gain. With one row scaled 40x, the per-tensor step grows from 0.000723 to 0.0184 (25x), MSE rises to 2.823e-05 (about 650x) and relative matmul error to 0.09644, while per-channel stays at 0.00679. On the 255 normal rows, per-tensor MSE is 2.823e-05 vs 2.234e-08 per-channel (about 1,260x). The max abs error is identical (0.00920) for both, because it comes from the outlier row itself: max error hides the damage, MSE on the normal rows shows it.

**Code:** (run with `python3 -I`; NumPy only; synthetic weights and activations)
```python
# INT8 weight quantization in NumPy: per-tensor vs per-channel (one scale per output row), symmetric, round-to-nearest.
import numpy as np

def quant_per_tensor(W):
    s = np.abs(W).max() / 127.0
    q = np.clip(np.round(W / s), -127, 127).astype(np.int8)
    return q, s
def quant_per_channel(W):                              # W is (out, in); one scale per output row
    s = np.abs(W).max(axis=1, keepdims=True) / 127.0
    q = np.clip(np.round(W / s), -127, 127).astype(np.int8)
    return q, s
def dequant(q, s): return q.astype(np.float32) * s

def metrics(W, What, X):
    err = W - What
    y, yh = X @ W.T, X @ What.T
    rel = np.linalg.norm(y - yh) / np.linalg.norm(y)
    return float((err ** 2).mean()), float(np.abs(err).max()), float(rel)

rng = np.random.default_rng(0)
out_f, in_f = 256, 512
X = rng.standard_normal((128, in_f)).astype(np.float32)          # synthetic activations

def run(tag, W):
    print(f"\n{tag}")
    print(f"{'scheme':12}{'MSE':>12}{'max abs err':>14}{'rel matmul err':>16}")
    for name, fn in [("per-tensor", quant_per_tensor), ("per-channel", quant_per_channel)]:
        q, s = fn(W); What = dequant(q, s)
        # verification: rounding error is at most half a step per element
        assert (np.abs(W - What) <= (s / 2 + 1e-6)).all()
        m = metrics(W, What, X)
        print(f"{name:12}{m[0]:12.3e}{m[1]:14.5f}{m[2]:16.5f}")

W = (rng.standard_normal((out_f, in_f)) * 0.02).astype(np.float32)   # synthetic Gaussian weights
run("A. well-behaved weights (all rows std 0.02)", W)
W2 = W.copy(); W2[7] *= 40.0                                          # one outlier output channel, 40x larger (assumed)
run("B. same weights, row 7 scaled 40x", W2)
# where does the damage land? error on the NON-outlier rows only
for name, fn in [("per-tensor", quant_per_tensor), ("per-channel", quant_per_channel)]:
    q, s = fn(W2); What = dequant(q, s)
    mask = np.arange(out_f) != 7
    print(f"{name:12} MSE on the 255 normal rows: {((W2[mask] - What[mask]) ** 2).mean():.3e}")
print("per-tensor step size A vs B:", np.abs(W).max() / 127, np.abs(W2).max() / 127)
```
**Output (my run):**
```

A. well-behaved weights (all rows std 0.02)
scheme               MSE   max abs err  rel matmul err
per-tensor     4.357e-08       0.00036         0.01042
per-channel    2.232e-08       0.00036         0.00743

B. same weights, row 7 scaled 40x
scheme               MSE   max abs err  rel matmul err
per-tensor     2.823e-05       0.00920         0.09644
per-channel    1.350e-07       0.00920         0.00679
per-tensor   MSE on the 255 normal rows: 2.823e-05
per-channel  MSE on the 255 normal rows: 2.234e-08
per-tensor step size A vs B: 0.0007234631 0.018402208
```

**Follow-ups:**
- *Why not always per-channel?* It is usually the right default for weights; per-tensor is simpler for activations where per-token or per-channel scales are harder to fuse.
- *What about INT4?* Same idea with 15 levels, so group-wise scales (for example one per 128 weights) and calibration matter much more (Part 10 Q9).
- *Asymmetric quantization?* Adds a zero point; useful for skewed ranges, costs extra arithmetic.

**Common mistakes:** judging quality by max error only; quantizing along the wrong axis; reporting weight MSE without checking the layer's output error; assuming the toy Gaussian result transfers to real LLM weights and activations.

### Q41 ⭐ 🟡 Code: simulate speculative decoding acceptance (draft and target token distributions, the accept-or-resample rule), check that the output distribution matches the target, and compare measured tokens per step with the closed-form formula.
**Asked at:** inference-platform teams, AI labs, live-coding rounds
**Say this first (1 line):** The draft proposes a token x from q, the target accepts it with probability min(1, p(x)/q(x)), and on rejection resamples from the normalised residual max(p - q, 0); this makes every emitted token exactly target-distributed, and the expected tokens per step follow (1 - a^(g+1)) / (1 - a) where a = sum of min(p, q).

**Then explain:**
- **Why the distribution is exact:** a token x is emitted either by acceptance, with probability q(x) * min(1, p(x)/q(x)) = min(p(x), q(x)), or after rejection, with probability (1 - a) * max(p(x) - q(x), 0) / (1 - a) = max(p(x) - q(x), 0). The sum is p(x). This is the modified rejection sampling in Leviathan et al. (arXiv 2211.17192) and Chen et al. (arXiv 2302.01318); both report 2-3x and 2-2.5x speedups in their own setups (T5-XXL; Chinchilla 70B in a distributed setup), which are not what this toy measures.
- **Acceptance rate:** per-token acceptance is a = sum_x min(p(x), q(x)) = 1 - TV(p, q). The code checks both forms agree (0.78).
- **Tokens per step with draft length g:** the target verifies all g drafted tokens in one pass; you keep the accepted prefix plus one more token (the resampled one on a rejection, or a bonus token if all g were accepted). With independent acceptance that is `sum_{i=0..g} a^i`.
- **What the toy simplifies:** the same p and q at every position (real acceptance varies by token and context, so the formula uses an average a); no draft cost (that is Q42); no KV cache.
- **Related:** the mechanism and variants are Part 10 Q11 and Q24.

**Example:** from the run, a = 0.78. Emitted-token frequencies over 400,000 samples match the target to within 0.0009 per token (a 5-sigma noise band for the worst bin is about 0.0039), while the draft q differs from p by up to 0.15. Tokens per step: g=1 measured 1.777 vs formula 1.780; g=4 measured 3.233 vs 3.233; g=8 measured 4.051 vs 4.060.

**Code:** (run with `python3 -I`; NumPy only; synthetic distributions)
```python
# Speculative sampling toy: vocab of 6 tokens, draft q and target p. Accept token x ~ q with prob min(1, p/q), else resample from norm(max(p-q, 0)).
import numpy as np
rng = np.random.default_rng(0)
V = 6
p = np.array([0.40, 0.25, 0.15, 0.10, 0.07, 0.03])     # target distribution (synthetic)
q = np.array([0.25, 0.30, 0.10, 0.20, 0.05, 0.10])     # draft distribution (synthetic)
alpha = np.minimum(p, q).sum()                         # per-token acceptance probability = 1 - TV(p, q)
print("alpha = sum min(p,q) =", round(float(alpha), 4), " 1 - TV =", round(1 - 0.5 * float(np.abs(p - q).sum()), 4))
resid = np.maximum(p - q, 0); resid /= resid.sum()

def one_token():
    x = rng.choice(V, p=q)
    if rng.random() < min(1.0, p[x] / q[x]): return x, True
    return rng.choice(V, p=resid), False

# 1. distribution check: single emitted token must follow p exactly (up to sampling noise)
N = 400_000
emit = np.array([one_token()[0] for _ in range(N)])
freq = np.bincount(emit, minlength=V) / N
print("target p      :", np.round(p, 4))
print("emitted freq  :", np.round(freq, 4), " max |diff| =", round(float(np.abs(freq - p).max()), 4),
      "(5 sigma of the worst bin ~", round(float(5 * np.sqrt(p * (1 - p) / N).max()), 4), ")")
print("draft-only q  :", np.round(q, 4), " <- sampling q directly would be visibly wrong")

# 2. tokens per verification step with draft length g: accepted prefix + one bonus/resampled token
def step_tokens(g):
    n = 0
    for _ in range(g):
        x, ok = one_token()
        if not ok: return n + 1                         # rejected: the resampled token is still a valid output token
        n += 1
    return n + 1                                        # all g accepted: bonus token from the target (the g+1-th)
for g in (1, 2, 4, 8):
    meas = np.mean([step_tokens(g) for _ in range(100_000)])
    formula = (1 - alpha ** (g + 1)) / (1 - alpha)
    print(f"draft length {g}: measured tokens/step {meas:.3f}   formula (1-a^(g+1))/(1-a) = {formula:.3f}")
```
**Output (my run):**
```
alpha = sum min(p,q) = 0.78  1 - TV = 0.78
target p      : [0.4  0.25 0.15 0.1  0.07 0.03]
emitted freq  : [0.4009 0.2503 0.1495 0.1001 0.0697 0.0296]  max |diff| = 0.0009 (5 sigma of the worst bin ~ 0.0039 )
draft-only q  : [0.25 0.3  0.1  0.2  0.05 0.1 ]  <- sampling q directly would be visibly wrong
draft length 1: measured tokens/step 1.777   formula (1-a^(g+1))/(1-a) = 1.780
draft length 2: measured tokens/step 2.391   formula (1-a^(g+1))/(1-a) = 2.388
draft length 4: measured tokens/step 3.233   formula (1-a^(g+1))/(1-a) = 3.233
draft length 8: measured tokens/step 4.051   formula (1-a^(g+1))/(1-a) = 4.060
```

**Follow-ups:**
- *Does speculative decoding change quality?* Not in distribution, for sampling at the same temperature; greedy decoding stays identical to the target's greedy output except for floating-point differences in batched verification (from memory, check).
- *Why does the formula plateau as g grows?* It tends to 1 / (1 - a) (here 4.55), so extra draft tokens stop paying; Q42 adds the draft cost.
- *Why can acceptance be low?* Draft and target disagree (different sizes, domains, or sampling temperature).

**Common mistakes:** sampling the residual from p instead of max(p - q, 0); forgetting the bonus token; using the same random number for acceptance and resampling; checking only the first token's distribution; assuming acceptance is a constant in real text.

### Q42 ⭐ 🔴 Derive the expected speedup of speculative decoding: expected accepted tokens per verification step as a function of acceptance rate and draft length, then include draft cost to find the best draft length.
**Asked at:** AI labs, inference-platform teams, research-leaning rounds
**Say this first (1 line):** If each drafted token is accepted independently with probability a, a step yields on average (1 - a^(g+1)) / (1 - a) tokens, a step costs g*c + 1 target-step units (c = draft step time / target step time), so speedup = E[tokens] / (g*c + 1), and the best g is where an extra draft token stops adding more expected tokens than it costs.

**Then explain:**
- **Derivation:** let N be the number of leading accepted tokens among g drafts. P(N >= i) = a^i, so E[N] = a + a^2 + ... + a^g. You always get one extra token (the resampled or bonus one), so E[tokens] = 1 + E[N] = sum_{i=0..g} a^i = (1 - a^(g+1)) / (1 - a). As g grows it tends to 1 / (1 - a).
- **Cost:** g sequential draft forwards at c each, plus one target verification of g+1 positions. Assume verification costs about 1 target step because decode is memory-bound (Part 10 Q1, Q33). That assumption weakens at large batch sizes where the verifier becomes compute-bound.
- **Speedup:** S(g) = (1 - a^(g+1)) / ((1 - a)(g*c + 1)). This matches the improvement factor I remember from Leviathan et al. (from memory, check the paper); the derivation here stands on its own.
- **Best g:** maximise S over integer g; there is no neat closed form, so scan g. Higher a and cheaper drafts push the best g up.
- **Checks in the code:** brute-force enumeration of all accept/reject patterns equals the closed form, and Monte Carlo agrees to three decimals.
- **Caveats:** a is not constant in real text; real systems have scheduling overhead and batching effects. Table values below are outputs of this model, not measurements. The authors' measured gains are 2-3x (T5-XXL, Leviathan et al.) and 2-2.5x (Chinchilla 70B, Chen et al.), in their setups.

**Example:** a = 0.8, c = 0.05: speedup by g for g = 1, 2, 3, 4, 6, 8, 12 is 1.71, 2.22, 2.57, 2.80, 3.04, 3.09, 2.95, so the best g is 8 at 3.09x, and drafting more than that loses. With a = 0.3, c = 0.3 and g = 4 the model gives 0.648x: slower than not speculating. In the table, a = 0.8 with c = 0.02 / 0.05 / 0.10 / 0.30 gives best g = 11 / 8 / 6 / 3.

**Code:** (run with `python3 -I`; stdlib only)
```python
# Speculative decoding speedup: closed form, brute-force check, and best draft length.
# Model (assumptions): each draft token is accepted independently with prob a; one target verification pass costs 1 unit
# (memory-bound, so checking g+1 positions costs about the same as 1); one draft forward costs c units (c = draft/target step-time ratio).
import itertools, random

def exp_tokens(a, g):                 # E[tokens per step] = sum_{i=0..g} a^i = (1-a^(g+1))/(1-a)
    return (1 - a ** (g + 1)) / (1 - a) if a < 1 else g + 1
def speedup(a, g, c):                 # tokens per unit time vs 1 token per unit time for plain decoding
    return exp_tokens(a, g) / (g * c + 1)

# brute force: enumerate every accept/reject pattern of g independent draft tokens; tokens emitted = leading accepts + 1
def exp_tokens_bruteforce(a, g):
    total = 0.0
    for pattern in itertools.product([1, 0], repeat=g):
        pr = 1.0
        for bit in pattern: pr *= a if bit else (1 - a)
        lead = 0
        for bit in pattern:
            if not bit: break
            lead += 1
        total += pr * (lead + 1)
    return total
for a, g in [(0.5, 3), (0.8, 4), (0.9, 7)]:
    assert abs(exp_tokens(a, g) - exp_tokens_bruteforce(a, g)) < 1e-12
print('brute-force enumeration matches the closed form for (a,g) = (0.5,3), (0.8,4), (0.9,7)')
# Monte Carlo check of the same quantity
rnd = random.Random(1)
def mc(a, g, n=200000):
    tot = 0
    for _ in range(n):
        k = 0
        while k < g and rnd.random() < a: k += 1
        tot += k + 1
    return tot / n
print("check a=0.8 g=4: formula", round(exp_tokens(0.8, 4), 4), " Monte Carlo", round(mc(0.8, 4), 4))

print("\nspeedup table (rows: acceptance a, cols: draft cost ratio c); entry = best g (speedup)  [g searched 1..16]")
cs = [0.02, 0.05, 0.10, 0.30]
print(f"{'a':>5}" + "".join(f"{'c=' + str(c):>16}" for c in cs))
for a in (0.5, 0.7, 0.8, 0.9, 0.95):
    row = f"{a:5.2f}"
    for c in cs:
        g = max(range(1, 17), key=lambda g: speedup(a, g, c))
        row += f"{'g=' + str(g) + ' (' + format(speedup(a, g, c), '.2f') + 'x)':>16}"
    print(row)
print("\nbreak-even: a low acceptance can lose. a=0.3, c=0.3, g=4 ->", round(speedup(0.3, 4, 0.3), 3), "x (below 1 means slower than plain decoding)")
print("a=0.8 c=0.05 by g:", [round(speedup(0.8, g, 0.05), 2) for g in (1, 2, 3, 4, 6, 8, 12)])
```
**Output (my run):**
```
brute-force enumeration matches the closed form for (a,g) = (0.5,3), (0.8,4), (0.9,7)
check a=0.8 g=4: formula 3.3616  Monte Carlo 3.3614

speedup table (rows: acceptance a, cols: draft cost ratio c); entry = best g (speedup)  [g searched 1..16]
    a          c=0.02          c=0.05           c=0.1           c=0.3
 0.50     g=4 (1.79x)     g=3 (1.63x)     g=2 (1.46x)     g=1 (1.15x)
 0.70     g=8 (2.76x)     g=6 (2.35x)     g=4 (1.98x)     g=2 (1.37x)
 0.80    g=11 (3.82x)     g=8 (3.09x)     g=6 (2.47x)     g=3 (1.55x)
 0.90    g=16 (6.31x)    g=13 (4.67x)    g=10 (3.43x)     g=5 (1.87x)
 0.95    g=16 (8.82x)    g=16 (6.47x)    g=15 (4.48x)     g=8 (2.18x)

break-even: a low acceptance can lose. a=0.3, c=0.3, g=4 -> 0.648 x (below 1 means slower than plain decoding)
a=0.8 c=0.05 by g: [1.71, 2.22, 2.57, 2.8, 3.04, 3.09, 2.95]
```

**Follow-ups:**
- *What if verification is not free?* Replace the 1 with t_verify(g+1) / t_target(1); once the batch is compute-bound, the gain shrinks or vanishes.
- *How do you raise a?* A better or fine-tuned draft model, lower temperature, drafting from the target's own features (EAGLE) or extra heads (Medusa); Part 10 Q24.
- *What is c for Medusa-style heads?* Much smaller than a separate draft model, but they need training.

**Common mistakes:** forgetting the +1 token; ignoring draft cost; assuming larger g is always better; treating the table's 6x as an achievable number; applying the formula when acceptances are strongly correlated.

### Q43 ⭐ 🟡 AI code review: this LLM-written serving and benchmark script has bugs (KV size uses attention heads instead of KV heads, ignores dtype bytes, closed-loop benchmark with one repeated prompt, reports only mean latency, model loaded per request, blocking call in an async handler, no max_tokens, gpu memory fraction set to 1.0). Find and fix them.
**Asked at:** product companies, big tech, AI-era code-review rounds
**Say this first (1 line):** I would reject this script on eight counts: the KV estimate is off by 4x in the wrong direction, the benchmark is not measuring what real traffic does, it reports the wrong statistic, and the server code has three operational bugs (per-request model load, blocking call in async, no output cap) plus a memory setting with no headroom.

**Then explain:** (each with the fix and a number from the toy run; shape and constants are assumed)
- **1. KV size uses attention heads (64) instead of KV heads (8):** with grouped-query attention only KV heads are cached (Part 1 Q10, Q15). 8x too big.
- **2. Ignores dtype bytes:** elements are not bytes. fp16 is 2 bytes, fp8 cache 1. Together with bug 1 the buggy figure is 1,310,720 vs the correct 327,680 bytes per token: 4.0x too big (8x from heads, 0.5x from the missing dtype). A wrong estimate here either wastes capacity or, if the errors go the other way, causes OOM.
- **3. Closed-loop benchmark with one repeated prompt:** the prefix cache hits 100% so prefill looks free; real traffic has different prompts. Use a realistic length and prefix distribution, open-loop arrivals (Part 10 Q30).
- **4. Mean latency only:** report p50/p95/p99 TTFT and TPOT per percentile and SLO (Part 10 Q2, Q16).
- **5. Model loaded per request:** load once at startup, share across requests; a real load reads tens of GB.
- **6. Blocking call in an async handler:** it stalls the event loop, so concurrent requests serialise. Await the engine call or push blocking work to an executor.
- **7. No `max_tokens`:** one runaway generation holds KV blocks and a slot. Cap per request and per tenant.
- **8. GPU memory fraction 1.0:** leaves nothing for CUDA context and other non-pool memory; use a fraction below 1 and leave headroom (Part 10 Q3, Q47). Engine semantics of `gpu_memory_utilization` as of the docs read on 2026-10-24: check live docs.

**Example:** the buggy script (illustrative, not run) looked like this; the Code block demonstrates each bug with a toy number.
```
kv_per_token = 2 * layers * num_attention_heads * head_dim          # bugs 1 and 2
def handle(req):
    model = load_model("big-model")                                  # bug 5
    time.sleep(0.05)   # inside an async def                         # bug 6
    return model.generate(req.prompt)                                # bug 7: no max_tokens
for _ in range(100): bench(prompt="same prompt every time")          # bug 3
print("avg latency:", mean(latencies))                               # bug 4
engine = Engine(gpu_memory_utilization=1.0)                          # bug 8
```
From the run: 8k tokens of KV is 2.50 GiB fixed vs 10.00 GiB buggy; repeated-prompt mean prefill 1.0 ms vs 100.0 ms for distinct prompts; synthetic heavy-tail latencies have mean 300 ms but p99 1639 ms; 100 requests cause 100 model loads buggy vs 0 per request fixed; 10 concurrent 50 ms requests take about 0.5 s blocking vs about 0.05 s non-blocking (real timing, small sleeps, so approximate; this run printed 0.50 s vs 0.05 s); uncapped mock generation reached 3,878 tokens (cap 512 stops at 512); at memory fraction 1.0 the non-pool headroom is 0.0 GB vs an assumed 2.5 GB need.

**Code:** (run with `python3 -I`; stdlib only; mock LLM, assumed constants: Llama-2-70B-like shape, 80 GB card, 7B fp16 weights)
```python
# Review of an LLM-written serving/benchmark script: each bug shown as buggy vs fixed, with a number. Mock LLM only; constants are assumed.
import asyncio, random, time, math

# ---- Bug 1+2: KV size uses attention heads and ignores dtype bytes ---------------------------------
L, HEADS, KV_HEADS, HD = 80, 64, 8, 128            # assumed Llama-2-70B-like shape (GQA: 8 KV heads), fp16
def kv_bytes_per_token_buggy(): return 2 * L * HEADS * HD                  # elements of an MHA cache, labelled "bytes"
def kv_bytes_per_token_fixed(dtype_bytes=2): return 2 * L * KV_HEADS * HD * dtype_bytes
b, f = kv_bytes_per_token_buggy(), kv_bytes_per_token_fixed()
print(f"1-2. KV per token: buggy {b:,} vs fixed {f:,} bytes -> buggy is {b / f:.1f}x too big (8x from heads, 0.5x from missing dtype)")
print(f"     fp8 cache would be {kv_bytes_per_token_fixed(1):,} bytes; 8k-token sequence = {8192 * f / 2**30:.2f} GiB fixed vs {8192 * b / 2**30:.2f} GiB buggy")

# ---- Bug 3: closed loop with ONE repeated prompt (prefix cache hits everything) --------------------
def prefill_ms(tokens, cached): return 0.05 * (tokens - cached)            # assumed 0.05 ms per uncached prompt token
same = [prefill_ms(2000, 2000 if i else 0) for i in range(100)]            # 1st request fills the cache, then 100% hits
distinct = [prefill_ms(2000, 0) for _ in range(100)]                       # real traffic: mostly different prompts
print(f"3. mean prefill: repeated prompt {sum(same) / 100:.1f} ms vs distinct prompts {sum(distinct) / 100:.1f} ms (the benchmark flatters the server)")

# ---- Bug 4: only mean latency ------------------------------------------------------------------------
rnd = random.Random(0)
lat = sorted(rnd.lognormvariate(math.log(200), 0.9) for _ in range(5000))   # synthetic heavy-tailed latencies in ms
pct = lambda p: lat[int(p * len(lat))]
print(f"4. synthetic latencies: mean {sum(lat) / len(lat):.0f} ms, p50 {pct(.5):.0f}, p95 {pct(.95):.0f}, p99 {pct(.99):.0f} -> the mean hides the tail")

# ---- Bug 5: model loaded per request ------------------------------------------------------------------
loads = {"n": 0}
def load_model(): loads["n"] += 1; return object()
def handler_buggy(): m = load_model(); return m
_MODEL = load_model()                                                     # fixed: load once at startup
def handler_fixed(): return _MODEL
loads["n"] = 0; [handler_buggy() for _ in range(100)]; n_buggy = loads["n"]
loads["n"] = 0; [handler_fixed() for _ in range(100)]; n_fixed = loads["n"]
print(f"5. model loads for 100 requests: buggy {n_buggy}, fixed {n_fixed} per request plus 1 at startup (a real load reads tens of GB; here only counted)")

# ---- Bug 6: blocking call in an async handler (real timing, small sleeps) ----------------------------------
async def handler_blocking(): time.sleep(0.05); return 1                   # blocks the event loop
async def handler_ok():       await asyncio.sleep(0.05); return 1          # yields; stands in for awaiting an engine/HTTP call
async def bench(h, n=10):
    t = time.perf_counter(); await asyncio.gather(*[h() for _ in range(n)]); return time.perf_counter() - t
print(f"6. 10 concurrent requests of 50 ms: blocking {asyncio.run(bench(handler_blocking)):.2f} s vs non-blocking {asyncio.run(bench(handler_ok)):.2f} s")

# ---- Bug 7: no max_tokens ----------------------------------------------------------------------------------------
def mock_generate(rnd, max_tokens=None, p_eos=0.002):                      # mock LLM: stops with prob p_eos per token
    n = 0
    while rnd.random() > p_eos and (max_tokens is None or n < max_tokens): n += 1
    return n
r1, r2 = random.Random(5), random.Random(5)
unc = [mock_generate(r1) for _ in range(2000)]; cap = [mock_generate(r2, 512) for _ in range(2000)]
print(f"7. output lengths over 2000 mock requests: no cap max {max(unc)} tokens (mean {sum(unc) / 2000:.0f}); cap 512 max {max(cap)} (mean {sum(cap) / 2000:.0f})")

# ---- Bug 8: gpu memory fraction 1.0 ----------------------------------------------------------------------------------
TOTAL, WEIGHTS, ACT_PEAK, OTHER = 80.0, 14.0, 3.0, 2.5      # GB, assumed: 80 GB card, 7B fp16 weights, activation peak, CUDA context + other non-pool memory
for util in (1.0, 0.9):
    pool = util * TOTAL - WEIGHTS - ACT_PEAK
    headroom = TOTAL - util * TOTAL
    print(f"8. util {util}: KV pool {pool:.1f} GB, headroom left for non-pool memory {headroom:.1f} GB vs need ~{OTHER} GB -> {'OOM risk' if headroom < OTHER else 'ok'}")
```
**Output (my run):**
```
1-2. KV per token: buggy 1,310,720 vs fixed 327,680 bytes -> buggy is 4.0x too big (8x from heads, 0.5x from missing dtype)
     fp8 cache would be 163,840 bytes; 8k-token sequence = 2.50 GiB fixed vs 10.00 GiB buggy
3. mean prefill: repeated prompt 1.0 ms vs distinct prompts 100.0 ms (the benchmark flatters the server)
4. synthetic latencies: mean 300 ms, p50 201, p95 897, p99 1639 -> the mean hides the tail
5. model loads for 100 requests: buggy 100, fixed 0 per request plus 1 at startup (a real load reads tens of GB; here only counted)
6. 10 concurrent requests of 50 ms: blocking 0.50 s vs non-blocking 0.05 s
7. output lengths over 2000 mock requests: no cap max 3878 tokens (mean 498); cap 512 max 512 (mean 315)
8. util 1.0: KV pool 63.0 GB, headroom left for non-pool memory 0.0 GB vs need ~2.5 GB -> OOM risk
8. util 0.9: KV pool 55.0 GB, headroom left for non-pool memory 8.0 GB vs need ~2.5 GB -> ok
```

**Follow-ups:**
- *Which bug is most dangerous?* In production, the missing cap and the 1.0 memory fraction (crashes under load); in a benchmark, the repeated prompt (a wrong decision made on flattering numbers).
- *How would you catch these automatically?* A KV calculator with unit tests against a known model config, a benchmark harness that refuses fewer than N distinct prompts, a lint for blocking calls in async code.
- *Is the LLM's code wrong in a pattern?* Yes: plausible-looking formulas with unit slips; ask for the units of every quantity.

**Common mistakes:** only listing symptoms without fixes; fixing KV heads but not dtype; "async" without checking what is awaited; trusting a benchmark with a single prompt; reviewing for style while missing the memory arithmetic.

### Q44 ⭐ 🔴 Design question: an LLM serving platform for N requests per second with TTFT and TPOT SLOs (workload assumptions, capacity maths, engine choice, batching and scheduling, caching, autoscaling, routing, observability, failure modes).
**Asked at:** senior roles; interview-prep guide, not a candidate report poses '100K req/s of an 8B model' and 'design an LLM inference API'
**Say this first (1 line):** I would turn the SLOs into a per-replica concurrency limit, size replicas from Little's law and a target utilisation below 100%, run a continuous-batching engine behind a token-aware router, scale on queue and KV signals, and prove the plan with an open-loop test before any traffic.

**Then explain:**
- **Clarify first:** requests per second N, prompt and output length distributions (not means), shared prefixes, streaming or not, TTFT and TPOT targets at which percentile, model and quality bar, burstiness, regions. Without these, the plan is a guess.
- **Capacity maths:** (1) the TPOT SLO bounds step time, which bounds the batch size; the KV pool bounds concurrent sequences (Part 10 Q4, Q15); take the smaller. (2) Replica-seconds per request at that batch = decode share + prefill. (3) Replicas = N / (replica capacity x target utilisation); keep headroom for bursts, failures and deploys. (4) Check with Little's law, L = lambda x W, that in-flight sequences per replica stay under the KV cap.
- **Engine and scheduling:** an engine with continuous batching, paged KV and chunked prefill (vLLM, SGLang, TensorRT-LLM, check current docs; framework choice is Part 10 Q12). Tune the batched-token budget: small favours inter-token latency, large favours TTFT and throughput (vLLM optimisation docs, as of 2026-10-24, check live). Separate pools for long-context or batch traffic (Q20, Q32).
- **Caching and routing:** prefix caching with cache-aware, load-bounded routing (Q14, Q37); response and semantic caches only where acceptable (Q28).
- **Autoscaling:** scale on queue depth, running and waiting requests and KV usage, not GPU utilisation; account for cold start (weights load) with warm spares (Q27). Admission control and token-based limits protect the SLO under overload (Q29).
- **Observability and failure modes:** TTFT, TPOT, queue time, KV usage, preemptions, cache hit rate, per percentile and per tenant (depth in Part 11); failure modes are replica OOM (Q47), a stuck long request, a bad deploy, a noisy tenant (Q49), and overload. Use canary plus rollback thresholds.
- **Toy check (all constants assumed, no real GPU):** step time = 25 ms + 0.4 ms x decoding sequences + 0.02 ms per prefill token; KV cap 64 sequences; mean prompt 1000, output 200; SLOs p99 TTFT 1500 ms, p99 TPOT 60 ms.

**Example:** from the run, the TPOT SLO allows 87 sequences but the KV cap is 64, so the limit is 64 and one replica does 5.61 req/s. For N = 20 req/s at 70% target utilisation that is 6 replicas, 3.33 req/s each, about 33.7 sequences in flight per replica (cap 64). The single-replica simulation meets both SLOs at 2.0, 3.0 and 4.6 req/s (p99 TTFT 399, 498, 819 ms; p99 TPOT 36.5, 42.7, 54.9 ms), and at 4.6 req/s the time-average number of requests in the system is 42.6 vs lambda x W = 42.7, confirming Little's law. With 2% of prompts at 20k tokens, whole-prompt prefill gives p99 TTFT 466 ms and TPOT 47.4 ms; chunked prefill (512 tokens per step, served FIFO in this toy) gives TPOT 45.6 ms but TTFT 2076 ms, missing the SLO. That is a weak and honest result: chunking here buys a little TPOT and costs a lot of TTFT because short prompts queue behind long chunked ones; real schedulers order work differently, so tune on your own traffic.

**Code:** (run with `python3 -I`; stdlib only; toy model, assumed constants)
```python
# TOY capacity model + single-replica simulation for a TTFT/TPOT SLO design. Every constant is ASSUMED (not measured on any GPU).
import random, math

A_MS, C_MS, PT_MS = 25.0, 0.4, 0.02       # step time = A + C*decoding_seqs + PT*prefill_tokens_in_step   (ms, assumed)
MAX_SEQS = 64                              # assumed KV-memory cap on in-flight sequences per replica
PROMPT, OUT = 1000, 200                    # assumed mean prompt / output tokens
SLO_TPOT_MS, SLO_TTFT_MS = 60.0, 1500.0    # assumed SLOs (p99)

# ---- 1. back-of-envelope capacity (the part you say out loud) ----
step = lambda b: A_MS + C_MS * b
b_slo = int((SLO_TPOT_MS - A_MS) / C_MS)                    # largest batch whose pure-decode step meets TPOT
b = min(b_slo, MAX_SEQS)
ms_per_req = OUT * step(b) / b + PROMPT * PT_MS             # replica-milliseconds per request at batch b
cap = 1000.0 / ms_per_req                                   # requests/s one replica can do
N, TARGET_UTIL = 20.0, 0.7
replicas = math.ceil(N / (cap * TARGET_UTIL))
print(f"batch limit from TPOT SLO {b_slo}, from KV {MAX_SEQS} -> use {b}; replica capacity {cap:.2f} req/s")
print(f"N={N}/s at {TARGET_UTIL:.0%} target utilisation -> {replicas} replicas; per-replica load {N / replicas:.2f} req/s")
print(f"Little's law at that load: L = lambda*W ~ {N / replicas:.2f} * ({OUT * step(b) / 1000:.1f} s decode) = {N / replicas * OUT * step(b) / 1000:.1f} in flight per replica (cap {MAX_SEQS})")

# ---- 2. simulate one replica: continuous batching, optional chunked prefill ----
def simulate(lam_per_s, chunk, tail=0.0, n_req=6000, seed=3):
    rnd = random.Random(seed); t_arr, reqs = 0.0, []
    for _ in range(n_req):
        t_arr += rnd.expovariate(lam_per_s / 1000.0)
        prompt = max(50, int(rnd.lognormvariate(math.log(PROMPT) - 0.5 * 0.7 ** 2, 0.7)))
        if rnd.random() < tail: prompt = 20000                   # assumed rare very long prompts
        out = max(2, int(rnd.lognormvariate(math.log(OUT) - 0.5 * 0.7 ** 2, 0.7)))
        reqs.append((t_arr, prompt, out))
    t, i = 0.0, 0; waiting, pre, dec = [], [], []            # pre: [arrival, remaining_prompt, out]; dec: [arrival, out_left, first_t]
    ttft, tpot, area, busy, wsum, nd = [], [], 0.0, 0.0, 0.0, 0
    while i < n_req or waiting or pre or dec:
        if not (waiting or pre or dec) and i < n_req: t = max(t, reqs[i][0])
        while i < n_req and reqs[i][0] <= t: waiting.append(reqs[i]); i += 1
        while waiting and len(pre) + len(dec) < MAX_SEQS:
            a, p, o = waiting.pop(0); pre.append([a, p, o])
        budget, pf, newly = (chunk if chunk else 10 ** 9), 0, []
        for r in pre:
            take = min(r[1], budget); r[1] -= take; budget -= take; pf += take
            if r[1] == 0: newly.append(r)
        dt = A_MS + C_MS * len(dec) + PT_MS * pf
        area += dt * (len(waiting) + len(pre) + len(dec)); busy += dt
        t += dt
        for r in dec: r[1] -= 1
        for r in [r for r in dec if r[1] == 0]:
            tpot.append((t - r[2]) / max(1, r[3] - 1)); wsum += t - r[0]; nd += 1
        dec = [r for r in dec if r[1] > 0]
        for r in newly:
            pre.remove(r); ttft.append(t - r[0])
            if r[2] > 1: dec.append([r[0], r[2] - 1, t, r[2]])
    pct = lambda xs, q: sorted(xs)[int(q * len(xs))]
    return pct(ttft, .99), pct(tpot, .99), area / busy, (nd / t) * (wsum / nd)    # last = lambda_eff * W (Little)

print(f"\n{'load req/s':>10}{'prompts':>13}{'prefill':>11}{'p99 TTFT ms':>13}{'p99 TPOT ms':>13}{'time-avg in sys':>17}{'lambda*W':>10}  SLO met?")
for lam, chunk, tail in [(2.0, 512, 0), (3.0, 512, 0), (3.0, None, 0), (4.6, 512, 0), (3.0, None, 0.02), (3.0, 512, 0.02)]:
    f, p, avg_in_sys, lw = simulate(lam, chunk, tail)
    ok = "yes" if f <= SLO_TTFT_MS and p <= SLO_TPOT_MS else "NO"
    print(f"{lam:10.1f}{'2% x 20k' if tail else 'normal':>13}{'chunk 512' if chunk else 'whole':>11}{f:13.0f}{p:13.1f}{avg_in_sys:17.1f}{lw:10.1f}  {ok}")
```
**Output (my run):**
```
batch limit from TPOT SLO 87, from KV 64 -> use 64; replica capacity 5.61 req/s
N=20.0/s at 70% target utilisation -> 6 replicas; per-replica load 3.33 req/s
Little's law at that load: L = lambda*W ~ 3.33 * (10.1 s decode) = 33.7 in flight per replica (cap 64)

load req/s      prompts    prefill  p99 TTFT ms  p99 TPOT ms  time-avg in sys  lambda*W  SLO met?
       2.0       normal  chunk 512          399         36.5             12.7      12.7  yes
       3.0       normal  chunk 512          498         42.7             21.6      21.7  yes
       3.0       normal      whole          154         42.8             21.4      21.5  yes
       4.6       normal  chunk 512          819         54.9             42.6      42.7  yes
       3.0     2% x 20k      whole          466         47.4             22.2      22.3  yes
       3.0     2% x 20k  chunk 512         2076         45.6             22.8      22.9  NO
```

**Follow-ups:**
- *What changes at 100x the traffic?* More replicas behind a hierarchy of routers, regional pools, disaggregated prefill and decode if TTFT and TPOT conflict (Q32), and a capacity plan per model.
- *What if the SLO is tighter?* Lower the batch limit (lower utilisation), use smaller or quantized models, speculative decoding (Q11), or more tensor-parallel shards.
- *How do you validate before launch?* Open-loop load test with realistic prompt and prefix distributions, find the knee, set the autoscaling target below it (Q30).

**Common mistakes:** sizing from average tokens per second only; using the KV cap or the SLO bound but not both; planning for 100% utilisation; scaling on GPU utilisation; no admission control; a design with no observability or rollback.

### Q45 ⭐ 🔴 Design question: cut LLM serving cost by 50% without hurting quality (where to measure first, then quantization, batching and utilisation, caching, routing, smaller or distilled models, spot capacity, and how you prove quality held).
**Asked at:** senior roles at product companies, GCCs, platform teams
**Say this first (1 line):** First measure where the money goes (utilisation, prefill vs decode share, token mix), then pull the levers that do not change the model output (batching and utilisation, prefix caching) before the ones that might (quantization, routing, smaller models), and prove quality held with a paired non-inferiority test on a fixed eval set.

**Then explain:**
- **Measure first:** GPU-hours per million tokens split into input and output (Part 10 Q13), utilisation and queue headroom, prefill vs decode time, cache hit rate, idle replicas, requests that hit max length. Cost per token is mostly decided by utilisation, so find idle capacity before touching quality.
- **Lever order (safest first):** batching and utilisation (continuous batching, right-sized replicas, autoscale on queue signals, Q7, Q27); prefix caching (Q14); quantization with a validation protocol (Q8, Q10); routing easy traffic to a cheaper model (Q28); distilled or smaller models (Part 4 Q25 break-even); spot or preemptible capacity for offline traffic (Q34).
- **Do not trust stacked estimates:** factors overlap (a higher-utilisation fleet makes quantization's gain smaller in cost terms). Measure each lever in isolation, then combined.
- **How to prove quality held:** a fixed eval set that mirrors production, same prompts for baseline and candidate (paired), a pre-agreed non-inferiority margin, a one-sided confidence bound, plus slice checks (long context, languages, tool calls) and a shadow or canary in production (eval method in Part 9; quantized-model checks in Part 10 Q10).
- **Toy demo (hypothetical factors, synthetic judge data, no prices):** a four-lever cost stack, then two candidates scored on 1000 prompts with a mock pass/fail judge.

**Example:** hypothetical lever factors on a baseline cost of 1.00: utilisation 35% to 55% gives 0.636, prefix cache (30% of prefill saved, prefill 40% of GPU time) 0.880, routing 30% of traffic to a 0.25x-cost model 0.775, a 1.25x decode speed-up from lower precision 0.800; cumulative 0.347, a 65% saving on paper, which is why a 50% target is plausible but only if the factors survive measurement. Quality gate with margin -2 points: candidate A (4% of baseline passes break, 4% of fails fix) has pass rate 0.809 to 0.776, paired diff -0.0330, lower bound -0.0449, so I cannot claim quality held. Candidate B (1.5% break, 6.8% fix) goes 0.809 to 0.805, diff -0.0040, SE 0.0058 (bootstrap 0.0057), lower bound -0.0136, so non-inferior. Pairing matters: the unpaired SE would be 0.0177 vs 0.0058 on the same data.

**Code:** (run with `python3 -I`; NumPy only; hypothetical cost factors, mock judge on synthetic data)
```python
# (1) Stack cost levers multiplicatively with HYPOTHETICAL factors; (2) prove "quality held" with a paired non-inferiority test on a mock judge.
import numpy as np
# ---- 1. cost lever stack. Baseline cost = 1.00 per unit of work (symbolic; no prices). All factors are hypothetical assumptions.
levers = [
    ("raise utilisation 35% -> 55% (tune batch, fewer idle replicas)", 0.35 / 0.55),   # same GPUs do 55/35 more work
    ("prefix cache saves 30% of prefill, prefill is 40% of GPU time", 1 - 0.30 * 0.40),
    ("route 30% of traffic to a model costing 0.25x per request",     0.70 + 0.30 * 0.25),
    ("INT8/FP8 weights: 1.25x decode speed-up on the rest (assumed)",  1 / 1.25),
]
cost = 1.0
print(f"{'lever (all factors hypothetical)':66}{'factor':>8}{'cumulative cost':>17}")
for name, f in levers:
    cost *= f; print(f"{name:66}{f:8.3f}{cost:17.3f}")
print(f"stacked cost {cost:.3f} of baseline -> saving {1 - cost:.0%} IF the factors hold and do not overlap (they usually overlap: measure each in isolation)")

# ---- 2. quality gate: same 1000 prompts, mock judge pass/fail for baseline and candidate (paired). Synthetic data.
rng = np.random.default_rng(0)
n, MARGIN = 1000, -0.02
base_pass = rng.random(n) < 0.82                        # synthetic: baseline passes about 82%
flip = rng.random(n)
def gate(name, down, up):
    cand = base_pass.copy()
    cand[base_pass & (flip < down)] = False             # baseline passes that the candidate now fails
    cand[~base_pass & (flip < up)] = True               # baseline fails that the candidate now passes
    d = cand.astype(float) - base_pass.astype(float)    # paired difference per prompt in {-1, 0, +1}
    m, se = d.mean(), d.std(ddof=1) / np.sqrt(n)
    boot = np.array([d[rng.integers(0, n, n)].mean() for _ in range(4000)]).std()
    se_unp = np.sqrt(base_pass.var(ddof=1) / n + cand.var(ddof=1) / n)
    lo = m - 1.645 * se
    print(f"{name}: pass {base_pass.mean():.3f} -> {cand.mean():.3f}, paired diff {m:+.4f}, SE formula {se:.4f} vs bootstrap {boot:.4f} (unpaired SE would be {se_unp:.4f})")
    print(f"   one-sided 95% lower bound {lo:+.4f} vs margin {MARGIN:+.2f} -> {'non-inferior, ship' if lo > MARGIN else 'cannot claim quality held'}")
print()
gate("candidate A (4% break, 4% fix)    ", 0.04, 0.04)
gate("candidate B (1.5% break, 6.8% fix)", 0.015, 0.068)
```
**Output (my run):**
```
lever (all factors hypothetical)                                    factor  cumulative cost
raise utilisation 35% -> 55% (tune batch, fewer idle replicas)       0.636            0.636
prefix cache saves 30% of prefill, prefill is 40% of GPU time        0.880            0.560
route 30% of traffic to a model costing 0.25x per request            0.775            0.434
INT8/FP8 weights: 1.25x decode speed-up on the rest (assumed)        0.800            0.347
stacked cost 0.347 of baseline -> saving 65% IF the factors hold and do not overlap (they usually overlap: measure each in isolation)

candidate A (4% break, 4% fix)    : pass 0.809 -> 0.776, paired diff -0.0330, SE formula 0.0072 vs bootstrap 0.0072 (unpaired SE would be 0.0181)
   one-sided 95% lower bound -0.0449 vs margin -0.02 -> cannot claim quality held
candidate B (1.5% break, 6.8% fix): pass 0.809 -> 0.805, paired diff -0.0040, SE formula 0.0058 vs bootstrap 0.0057 (unpaired SE would be 0.0177)
   one-sided 95% lower bound -0.0136 vs margin -0.02 -> non-inferior, ship
```

**Follow-ups:**
- *What if quality drops on one slice only?* Gate on slices, not only the average; route that slice to the old model.
- *How big must the eval set be?* It depends on the discordance rate and the margin; a tighter margin or noisier judge needs more prompts, and the judge's own noise must be audited (Part 9).
- *What if 50% is not reachable safely?* Report the safe saving and the next lever's measured quality cost.

**Common mistakes:** starting with INT4 before looking at utilisation; multiplying lever savings as if independent; comparing average scores with no confidence bound; an eval set that does not match production traffic; counting a saving that came from lower quality or higher latency.

### Q46 ⭐ 🔴 Production diagnosis: p99 TTFT doubled after a traffic increase and a deploy while GPU 'utilisation' looks fine. Walk through how you localise the cause (queueing, preemptions, prefix-cache hit rate, prompt template change, long-tail prompts, a noisy tenant) and fix it.
**Asked at:** senior roles, inference-platform teams; interview-prep guide, not a candidate report lists tail latency, prefix-cache and prompt-template scenarios
**Say this first (1 line):** Split TTFT into queue wait plus prefill compute first; then ask which input changed (traffic, prefix-cache hit rate, prompt lengths, one tenant), because each cause moves a different signal even though "GPU utilisation" looks fine in all of them.

**Then explain:**
- **Why utilisation is useless here:** a GPU that is busy is not necessarily doing useful work; it can be recomputing prefixes or prefilling a giant prompt while others wait (Part 10 Q2 on metrics, Q1 on phases).
- **Step 1, queue vs compute:** TTFT = queue time + prefill time (+ network). If queue time carries p99, you are over capacity or blocked behind something big; if prefill time carries it, requests got more expensive (cache hit dropped, longer prompts).
- **Step 2, what changed:** compare the before and after of (a) arrival rate and token rate, (b) prefix-cache hit rate (a template change that puts a timestamp or user id early in the prompt breaks prefix reuse, Part 10 Q14), (c) prompt-length percentiles (a long tail), (d) per-tenant uncached-token share (a noisy tenant), (e) preemptions and KV usage (Q21), (f) the deploy diff (flags such as the batched-token budget, chunked prefill, memory fraction).
- **Metrics to read:** the vLLM metrics doc lists queue time, running and waiting requests, KV-cache usage and TTFT histograms; it did not list a preemption counter on the page I read, so check whether your version exports one.
- **Fix by cause:** capacity (add replicas, scale on queue signals, Q27); cache (fix the template so shared text comes first; route by prefix, Q37); long tail (separate pool, chunked prefill, input-length limits); noisy tenant (per-tenant budgets and fair scheduling, Q29, Q49); preemptions (lower max concurrency, more KV, quantize KV, Q22).
- **Toy triage (synthetic, assumed constants, one FCFS prefill queue; shows which signal moves, not a real engine):** 20 tenants, prefill = 0.05 ms per uncached token + 10 ms.

**Example:** from the run (baseline at 14 req/s, p99 TTFT 221 ms). Traffic up to 22 req/s: p99 413 ms (about 1.9x), hit rate unchanged at 75%, p99 prompt unchanged. Template change (prefix hit 90% to 50% of requests): p99 1,469 ms, token hit rate down from 75% to 42%, prompt lengths unchanged. 1% giant prompts: p99 3,370 ms, p99 prompt length 6,851 vs 2,881. Noisy tenant: p99 10,824 ms, one tenant is 37% of uncached prefill work vs about 6% baseline. The queue share of p99 TTFT is 78 to 99% in every case, so "it's queueing" is true but does not localise the cause; the hit rate, prompt percentile and per-tenant share do.

**Code:** (run with `python3 -I`; stdlib only; toy queue)
```python
# TOY triage of "p99 TTFT doubled". One FCFS prefill queue per replica (Lindley recursion); synthetic traffic; all constants assumed.
# The point is the DIAGNOSTIC SIGNALS: queue wait vs compute, cache hit rate, prompt-length tail, per-tenant share. Not a model of any real engine.
import random, math, collections

MS_PER_TOK, FIXED_MS, SYS_TOK = 0.05, 10.0, 1500        # assumed: prefill ms per uncached token, fixed overhead, shared system-prompt tokens

def gen(seed, rate_per_s, n=30000, hit=0.90, tail=0.0, burst=False):
    rnd = random.Random(seed); t, reqs = 0.0, []
    for _ in range(n):
        t += rnd.expovariate(rate_per_s / 1000.0)
        tenant = rnd.randrange(20)
        if burst and 120_000 < t % 600_000 < 150_000 and rnd.random() < 0.5: tenant = 0   # tenant 0 floods 30 s out of every 600 s
        user = max(20, int(rnd.lognormvariate(math.log(300) - 0.32, 0.8)))
        if tenant == 0 and burst: user = 3000                                              # ...with long prompts
        if rnd.random() < tail: user = 30000                                               # rare giant prompt
        cached = SYS_TOK if rnd.random() < hit else 0
        reqs.append((t, tenant, SYS_TOK + user, cached))
    return reqs

def serve(reqs):
    free, rows, busy = 0.0, [], 0.0
    for t, ten, tok, cached in reqs:
        svc = FIXED_MS + (tok - cached) * MS_PER_TOK
        start = max(t, free); free = start + svc; busy += svc
        rows.append((start - t, svc, ten, tok, cached))                 # wait, service, tenant, prompt tokens, cached tokens
    return rows, busy / free

def triage(name, reqs):
    rows, util = serve(reqs)
    ttft = sorted(w + s for w, s, *_ in rows); p99 = ttft[int(.99 * len(ttft))]
    tail = [r for r in rows if r[0] + r[1] >= p99]                      # the requests that define p99
    qshare = sum(r[0] for r in tail) / sum(r[0] + r[1] for r in tail)
    hit = sum(r[4] for r in rows) / sum(r[3] for r in rows)
    ptok = sorted(r[3] for r in rows)
    cost = collections.Counter()
    for w, s, ten, tok, cached in rows: cost[ten] += tok - cached
    top, topv = cost.most_common(1)[0]
    print(f"{name:34}{p99:9.0f}{qshare:8.0%}{hit:8.0%}{ptok[int(.99 * len(ptok))]:10d}{topv / sum(cost.values()):9.0%}{util:8.0%}")

print(f"{'scenario':34}{'p99 TTFT':>9}{'queue%':>8}{'hit%':>8}{'p99 ptok':>10}{'top-ten%':>9}{'busy':>8}")
triage("baseline (14 req/s)",               gen(1, 14))
triage("traffic up to 22 req/s",            gen(1, 22))
triage("template change: hit 90% -> 50%",   gen(1, 14, hit=0.50))
triage("1% giant prompts (30k tokens)",     gen(1, 14, tail=0.01))
triage("noisy tenant bursts",               gen(1, 14, burst=True))
print("legend: queue% = share of TTFT that is waiting in the queue for the requests at or above p99; hit% = prefix tokens served from cache;")
print("        p99 ptok = p99 prompt length; top-ten% = largest tenant's share of uncached prefill work; busy = fraction of time the prefill server worked")
```
**Output (my run):**
```
scenario                           p99 TTFT  queue%    hit%  p99 ptok top-ten%    busy
baseline (14 req/s)                     221     78%     75%      2881       6%     45%
traffic up to 22 req/s                  413     92%     75%      2881       6%     71%
template change: hit 90% -> 50%        1469     96%     42%      2881       5%     87%
1% giant prompts (30k tokens)          3370     97%     65%      6851       6%     65%
noisy tenant bursts                   10824     99%     67%      4500      37%     59%
legend: queue% = share of TTFT that is waiting in the queue for the requests at or above p99; hit% = prefix tokens served from cache;
        p99 ptok = p99 prompt length; top-ten% = largest tenant's share of uncached prefill work; busy = fraction of time the prefill server worked
```

**Follow-ups:**
- *Traffic and a deploy changed together; how do you separate them?* Replay the old traffic on the new build and the new traffic on the old build (or compare canary vs stable on the same traffic).
- *How do you stop it recurring?* Alerts on hit rate, p99 prompt length, per-tenant share and queue time, and a prompt-template test that checks prefix stability.
- *What if the cause is preemption?* Look at KV usage near 100% and requests restarting; reduce concurrency or add KV capacity.

**Common mistakes:** checking GPU utilisation or mean latency; fixing capacity when the real cause is a cache break; ignoring tenant breakdowns; assuming a deploy is innocent because it "only changed the prompt"; no before and after comparison on the same signals.

### Q47 ⭐ 🔴 Production diagnosis: a replica crashes with CUDA out-of-memory after hours of stable traffic, or fails to start at long context. Explain the causes (KV growth, activation peaks, fragmentation, logits for long prompts, memory settings) and the fixes.
**Asked at:** senior roles, inference-platform teams; interview-prep guide, not a candidate report lists long-context startup failures and OOM from batch size; TGI's v3 post notes prompt-logits memory
**Say this first (1 line):** Crashes after hours of stable traffic point to something that grows (leaked or never-freed KV blocks, fragmentation, caches, logprob or adapter state), while failing to start at long context is arithmetic: weights plus activation peak plus one max-length sequence of KV must fit in the budget.

**Then explain:**
- **Memory pieces:** weights, a KV pool sized at startup from what is left, an activation peak for the largest prefill chunk, and non-pool overhead such as the CUDA context. The engine's memory-fraction setting decides how much of the card the engine may plan for (Part 10 Q3; semantics as of the docs read on 2026-10-24, check live docs).
- **Fails at long context:** the KV pool must hold at least one maximum-length sequence. In the toy: KV per token is 131,072 bytes; a 131,072-token sequence needs 16.0 GiB; an assumed 24 GiB card has only 1.6 GiB of pool at 0.90 and cannot do 32k (4.0 GiB) but can do 8k (1.0 GiB). Fixes: lower the maximum model length, quantize the KV cache (Q22), shard across GPUs (Q17), or use a bigger card. Engines normally fail with a clear message about KV capacity vs max length (from memory, check).
- **Logits for long prompts:** materialising logits for every prompt position costs tokens x vocab x bytes. The TGI v3 docs (opened) give 100k tokens x 128k vocab x 2 bytes = 25.6 GB; my run with a 128,256 vocab gives 25.7 GB fp16 and 51.3 GB fp32, vs 0.51 MB for the last position only. Engines avoid this by computing only what they need (from memory, check), and chunked prefill bounds the activation peak (Q20).
- **After hours of stable load:** (a) cancelled or disconnected streams whose blocks are never released; (b) prefix-cache or adapter caches growing past their budget; (c) fragmentation outside the paged pool (allocator caching, variable-size activations); (d) a rare large request (long prompt, huge `n` or logprobs) arriving after hours; (e) memory fraction set so high there is no headroom (Q43, bug 8).
- **Diagnose:** plot KV blocks in use against running requests (they should track each other; a leak makes the gap grow), GPU memory by process, request-length percentiles, and the crash's last requests.
- **Fixes:** release on cancel and timeout, cap `max_tokens`, `n` and logprobs, limit concurrency by KV not by request count, keep memory headroom, restart replicas on a schedule as a stopgap only, and canary new builds.
- **Toy (assumed shapes):** a Llama-3-8B-like model (32 layers, 8 KV heads, head dim 128, vocab 128256, fp16).

**Example:** from the run, a leak simulation: 40 GiB pool = 20,480 blocks of 2 MiB, working set 60% of the pool leaves 8,192 blocks of headroom; if 0.1% of requests at 5 req/s (mean 1500 tokens) never free their blocks, closed form says exhaustion in 4.9 h and the simulation gave a mean of 4.9 h (range 3.2 to 6.7 h over 200 runs). Traffic was "stable" the whole time; only the used-blocks to running-requests gap shows it.

**Code:** (run with `python3 -I`; stdlib only; assumed model shape and sizes)
```python
# OOM diagnosis calculators + a leak simulation. Model shape and GPU sizes are ASSUMED (Llama-3-8B-like: 32 layers, 8 KV heads, head dim 128, vocab 128256, fp16).
import random
GiB = 2 ** 30
L, KVH, HD, VOCAB, BYTES = 32, 8, 128, 128256, 2
KV_TOK = 2 * L * KVH * HD * BYTES                         # bytes of KV per token
WEIGHTS = 8.03e9 * BYTES                                  # assumed parameter count x 2 bytes
print(f"KV per token {KV_TOK:,} B ({KV_TOK / 1024:.0f} KiB); weights ~{WEIGHTS / GiB:.1f} GiB")

# ---- A. does one max-length sequence fit in the KV pool? (fail-at-start check) ----
ACT_PEAK, OTHER = 3 * GiB, 2 * GiB                        # assumed activation peak for the largest prefill chunk + CUDA context/other
print("\nA. startup check: pool = util*GPU - weights - activation peak - other; need pool >= max_model_len * KV per token")
print(f"{'GPU GiB':>8}{'util':>6}{'pool GiB':>10}{'max_model_len':>15}{'needs GiB':>11}{'full-length seqs':>18}  verdict")
for gpu_gib, util, mml in [(80, 0.90, 131072), (40, 0.90, 131072), (24, 0.90, 32768), (24, 0.90, 8192)]:
    pool = util * gpu_gib * GiB - WEIGHTS - ACT_PEAK - OTHER
    need = mml * KV_TOK
    print(f"{gpu_gib:8d}{util:6.2f}{pool / GiB:10.1f}{mml:15d}{need / GiB:11.1f}{max(0, int(pool // need)):18d}  {'fits' if pool >= need else 'FAILS: lower max_model_len, quantize KV, or shard'}")

# ---- B. logits for a long prompt: tokens x vocab x bytes if logits are materialised for every position ----
print("\nB. full-prompt logits if materialised for every position:")
for tok in (8_000, 32_000, 100_000):
    print(f"   {tok:>7} tokens: fp16 {tok * VOCAB * 2 / 1e9:6.1f} GB, fp32 {tok * VOCAB * 4 / 1e9:6.1f} GB   (last position only: {VOCAB * 4 / 1e6:.2f} MB)")

# ---- C. 'OOM after hours': leaked blocks from cancelled streams, with closed-form check ----
BLOCK_TOK = 16
BLOCK_B = BLOCK_TOK * KV_TOK
POOL_BLOCKS = int(40 * GiB / BLOCK_B)                      # assumed 40 GiB KV pool
WORKING = 0.60                                             # assumed steady working set = 60% of the pool
LAM, P_LEAK, MEAN_TOK = 5.0, 0.001, 1500                   # assumed req/s, fraction of requests whose blocks are never freed, mean tokens held
headroom = POOL_BLOCKS * (1 - WORKING)
blocks_per_req = MEAN_TOK / BLOCK_TOK
closed = headroom / (LAM * P_LEAK * blocks_per_req)
rnd = random.Random(0); runs = []
for _ in range(200):
    leaked, n = 0.0, 0
    while leaked < headroom:
        n += 1
        if rnd.random() < P_LEAK: leaked += rnd.expovariate(1 / blocks_per_req)   # random size around the mean
    runs.append(n / LAM)
print(f"\nC. pool {POOL_BLOCKS} blocks of {BLOCK_B / 2**20:.0f} MiB; headroom {headroom:.0f} blocks; leak {P_LEAK:.1%} of requests at {LAM} req/s")
print(f"   closed form time to exhaustion {closed / 3600:.1f} h; simulated mean {sum(runs) / len(runs) / 3600:.1f} h (min {min(runs) / 3600:.1f}, max {max(runs) / 3600:.1f})")
print("   -> 'stable traffic' for hours then OOM is the signature of a slow leak or growth, not of a bad batch size; a metrics line of used blocks vs running requests shows it")
```
**Output (my run):**
```
KV per token 131,072 B (128 KiB); weights ~15.0 GiB

A. startup check: pool = util*GPU - weights - activation peak - other; need pool >= max_model_len * KV per token
 GPU GiB  util  pool GiB  max_model_len  needs GiB  full-length seqs  verdict
      80  0.90      52.0         131072       16.0                 3  fits
      40  0.90      16.0         131072       16.0                 1  fits
      24  0.90       1.6          32768        4.0                 0  FAILS: lower max_model_len, quantize KV, or shard
      24  0.90       1.6           8192        1.0                 1  fits

B. full-prompt logits if materialised for every position:
      8000 tokens: fp16    2.1 GB, fp32    4.1 GB   (last position only: 0.51 MB)
     32000 tokens: fp16    8.2 GB, fp32   16.4 GB   (last position only: 0.51 MB)
    100000 tokens: fp16   25.7 GB, fp32   51.3 GB   (last position only: 0.51 MB)

C. pool 20480 blocks of 2 MiB; headroom 8192 blocks; leak 0.1% of requests at 5.0 req/s
   closed form time to exhaustion 4.9 h; simulated mean 4.9 h (min 3.2, max 6.7)
   -> 'stable traffic' for hours then OOM is the signature of a slow leak or growth, not of a bad batch size; a metrics line of used blocks vs running requests shows it
```

**Follow-ups:**
- *OOM at startup vs at runtime?* Startup failures are deterministic arithmetic or profiling problems; runtime failures come from growth, rare large requests or fragmentation.
- *Does lowering batch size help?* It reduces the KV in use and activation peaks, but a leak still ends in OOM, just later.
- *What changes with tensor parallelism?* Weights and KV shard across GPUs, so per-GPU weights shrink; the per-GPU pool grows (Q3, Q17).

**Common mistakes:** raising the batch size without a KV estimate; setting the memory fraction to 1.0; assuming OOM means too many requests when it is a leak; testing only with short prompts; forgetting logits and activation peaks; restarting nightly and calling it fixed.

### Q48 ⭐ 🔴 Design question: scale a chat product from 8k to 200k-token contexts (memory, prefill latency, cost, caching, model choice, degradation and limits, evaluation of quality at length).
**Asked at:** senior roles; interview-prep guide, not a candidate report poses a 200K-token serving design
**Say this first (1 line):** Going from 8k to 200k context multiplies KV memory by about 24x, prefill compute by far more (attention grows quadratically), and shrinks how many users fit per node, so the design must separate long requests into their own pool, reuse prefixes, cap and degrade deliberately, and measure quality at length before promising it.

**Then explain:**
- **Memory:** KV grows linearly with tokens (Part 1 Q15, Q23). Concurrency per node falls in proportion, so long sessions pin lots of HBM.
- **Prefill compute:** linear layers cost about 2 x parameters x tokens; causal attention adds about 2 x layers x d_model x tokens^2, which overtakes the linear part at about params / (layers x d_model) tokens (about 107k in the toy). TTFT therefore grows faster than linearly (Part 1 Q30; Part 10 Q31).
- **Cost and caching:** reuse the conversation prefix across turns (prefix caching, Q14) or you re-pay prefill on every turn; but a cached session pins its KV, so only a limited number of sessions fit in HBM and the rest need offload or recompute.
- **Model and system levers:** a model with GQA/MLA or sliding-window layers (Part 1 Q10, Q33), KV quantization (Q22), chunked prefill (Q20), disaggregated prefill/decode (Q32), sequence parallelism, a separate long-context pool so a few giants do not hurt short chat (Q46).
- **Degradation and limits:** per-plan context caps, summarise or drop old turns, retrieval instead of stuffing (Part 6), token-based rate limits (Q29), queue and warn for long requests rather than time out silently.
- **Quality at length:** models can degrade with position and length (Part 1 Q30). Evaluate on your tasks with the answer position varied and distractors present, per length bucket; a simple needle test is necessary but not sufficient; re-run after quantizing KV or changing the model.
- **Toy (all hardware numbers assumed, not measured):** a 70B-class GQA model (80 layers, d_model 8192, 8 KV heads, head dim 128), an 8-GPU node of 80 GiB each, 300 TFLOP/s effective per GPU, 2.0 TB/s HBM per GPU.

**Example:** from the run: KV per token is 320 KiB (fp16). At 8,192 tokens one sequence is 2.5 GiB; at 200,000 it is 61.0 GiB (30.5 GiB with an fp8 cache). On the assumed node the pool is about 407 GiB, so 162 sequences fit at 8k but 6 at 200k. Attention FLOPs grow from 0.09 to 52.43 PFLOP (about 580x) and modelled prefill time from 0.5 s to 33.5 s, because attention passes the linear cost at about 106,812 tokens. For a 10-turn chat on a 100k-token history adding 500 tokens a turn, prefill tokens without reuse are 1,027,500 vs 5,000 with prefix reuse (206x fewer), but each live session pins about 32 GiB, so only 12 such sessions fit in HBM.

**Code:** (run with `python3 -I`; stdlib only; assumed model and hardware numbers)
```python
# 8k -> 200k context: what grows how. ASSUMED 70B-class GQA model and an 8-GPU node; every hardware number is an assumption, not a measurement.
GiB = 2 ** 30
P, L, D, KVH, HD = 70e9, 80, 8192, 8, 128           # assumed: params, layers, d_model, KV heads, head dim
BYTES_W = 2                                          # fp16 weights
GPUS, GPU_GIB, EFF_TFLOPS, BW_TBS = 8, 80, 300.0, 2.0   # assumed node: 8 x 80 GiB, 300 effective TFLOP/s per GPU for prefill, 2.0 TB/s per GPU HBM
kv_tok = lambda b: 2 * L * KVH * HD * b             # KV bytes per token at b bytes/element
weights = P * BYTES_W
pool = 0.9 * GPUS * GPU_GIB * GiB - weights - 0.06 * GPUS * GPU_GIB * GiB   # assumed 6% extra for activations/other
print(f"KV per token fp16 {kv_tok(2) / 1024:.0f} KiB; weights {weights / GiB:.0f} GiB; KV pool on the node ~{pool / GiB:.0f} GiB (assumed)")
print(f"\n{'ctx':>8}{'KV fp16 GiB':>13}{'KV fp8 GiB':>12}{'prefill PFLOP lin':>19}{'attn':>7}{'prefill s':>11}{'seqs fit fp16':>15}{'step floor ms':>15}")
for n in (8_192, 32_768, 131_072, 200_000):
    lin = 2 * P * n; attn = 2 * L * D * n * n          # causal attention FLOPs ~ 2*n^2*d per layer (QK^T and AV, half masked)
    t = (lin + attn) / (GPUS * EFF_TFLOPS * 1e12)
    kv16 = n * kv_tok(2)
    step = (weights + kv16) / (GPUS * BW_TBS * 1e12) * 1000      # one sequence alone: bytes read per decode step / aggregate bandwidth
    print(f"{n:8d}{kv16 / GiB:13.1f}{n * kv_tok(1) / GiB:12.1f}{lin / 1e15:19.2f}{attn / 1e15:7.2f}{t:11.1f}{int(pool // kv16):15d}{step:15.1f}")
print(f"attention FLOPs pass the linear-layer FLOPs at n = P/(L*D) = {P / (L * D):,.0f} tokens (same formulas)")

# multi-turn chat: each turn adds 500 tokens on top of a 100k-token history. Prefill tokens per turn with and without a reused prefix.
hist, turn, turns = 100_000, 500, 10
no_cache = sum(hist + k * turn + turn for k in range(turns))
cached = turns * turn
print(f"\n10 turns on a 100k-token history: prefill tokens with no reuse {no_cache:,} vs with prefix reuse {cached:,} ({no_cache / cached:.0f}x fewer)")
sess = (hist + turns * turn) * kv_tok(2) / GiB
print(f"but each live session pins ~{sess:.0f} GiB of KV (fp16): {int(pool // (sess * GiB))} such sessions fit in HBM; the rest need offload or recompute")
```
**Output (my run):**
```
KV per token fp16 320 KiB; weights 130 GiB; KV pool on the node ~407 GiB (assumed)

     ctx  KV fp16 GiB  KV fp8 GiB  prefill PFLOP lin   attn  prefill s  seqs fit fp16  step floor ms
    8192          2.5         1.2               1.15   0.09        0.5            162            8.9
   32768         10.0         5.0               4.59   1.41        2.5             40            9.4
  131072         40.0        20.0              18.35  22.52       17.0             10           11.4
  200000         61.0        30.5              28.00  52.43       33.5              6           12.8
attention FLOPs pass the linear-layer FLOPs at n = P/(L*D) = 106,812 tokens (same formulas)

10 turns on a 100k-token history: prefill tokens with no reuse 1,027,500 vs with prefix reuse 5,000 (206x fewer)
but each live session pins ~32 GiB of KV (fp16): 12 such sessions fit in HBM; the rest need offload or recompute
```

**Follow-ups:**
- *Why not just route everything to a long-context pool?* Over-provisioned memory for short requests; keep chat on a short-context pool and send only long requests to the expensive one.
- *Is 200k worth it vs retrieval?* Often not for every turn; retrieval or summarisation cuts cost, long context fits when the task needs the whole document.
- *What do you tell users?* Limits, expected wait for long inputs, and a streaming progress or queue indicator.

**Common mistakes:** extrapolating latency linearly from 8k; ignoring that cached sessions pin HBM; sizing for average context; offering 200k to every request on one pool; assuming quality holds at length without testing; forgetting decode reads the whole KV every step.

### Q49 ⭐ 🔴 Design question: a multi-tenant inference service with priority tiers, per-tenant token budgets, fairness, per-tenant LoRA adapters, noisy-neighbour isolation and SLO reporting.
**Asked at:** senior roles at platform teams and SaaS companies; interview-prep guide, not a candidate report poses a multi-tenant service with priority queues and rate limits
**Say this first (1 line):** Admit work through per-tenant token budgets (token buckets), schedule what is admitted by priority tier with fair sharing between tenants in a tier, give high tiers capacity reservations rather than only priority, isolate heavy tenants by limits (or separate pools), and report SLOs per tenant and tier.

**Then explain:**
- **Budgets:** limit tokens, not requests (Part 10 Q29): input plus expected output tokens per minute, with burst allowance, and a max concurrent sequences or KV share per tenant. Over budget gives 429 with retry-after, or a lower-priority queue.
- **Priority tiers:** premium work is scheduled first; but strict priority starves the lowest tier, so combine it with budgets or reserved shares, or use weighted fair queueing.
- **Fairness within a tier:** round-robin or deficit-style scheduling over tenants so one tenant's backlog cannot delay everyone's.
- **Noisy-neighbour isolation:** budgets and KV-share caps first; dedicated pools or replicas for tenants with strict contracts; long-prompt tenants separated (Q46); preemption policy that evicts low-priority work first (Q21).
- **Per-tenant LoRA adapters:** one base model, many adapters (Part 4 Q32; Part 10 Q25). The vLLM LoRA docs describe settings such as `--enable-lora`, a max LoRA rank and the max number of adapters loaded at once, and dynamic load and unload endpoints gated by an environment variable with a security warning (as of the docs read on 2026-10-24, check live docs). Adapters affect cache keys (the prefix-cache hash includes the LoRA id per the vLLM docs read), routing (send a tenant to replicas with its adapter hot) and batch diversity. The toy below does not model adapters.
- **SLO reporting:** per tenant and tier: TTFT and TPOT percentiles, queue time, rejection rate, token budget used vs allowed, so a tenant's bad day is attributable to them or to you.
- **Toy (synthetic, assumed rates and budgets):** server capacity 30,000 work units per second (a unit is about one token of work); five tenants plus a free tier; the "noisy" standard-tier tenant sends 8x its normal rate for 20 of 60 s.

**Example:** from the run (p99 completion latency in seconds; noisy tenant rejection in brackets). FIFO with no limits: every tenant sees about 13 s (premium 13.00, std 12.9 to 13.0, noisy 13.00, free 12.70). FIFO plus token buckets: premium 0.70, std 0.70 to 0.80, noisy 0.90 with 49% of its requests rejected, free 0.80. Tiered fair scheduling with no limits: premium 0.20, std 0.30 to 0.60, but noisy 22.50 and free 45.00 (the free tier starves behind higher tiers). Tiered fair plus buckets: premium 0.20, std 0.30 to 0.60, noisy 1.50 (49% rejected), free 3.70. In this toy the budgets did most of the isolating; the tiers then give premium its extra margin; and strict priority alone starves the free tier.

**Code:** (run with `python3 -I`; stdlib only; toy scheduler, no adapters)
```python
# TOY multi-tenant scheduler. A "work unit" ~ one token of prefill/decode work; the server does CAP units per 100 ms step.
# Synthetic tenants, assumed rates and budgets. Compares FIFO, FIFO + token buckets, and tiered fair scheduling (+ buckets).
import random, math, collections

STEP, STEPS, CAP = 0.1, 600, 3000                      # 100 ms steps, 60 s run, 30k units/s capacity (assumed)
TENANTS = {                                            # name: (tier 0=best, offered req/s, budget units/s)
    "premium": (0, 8, 6000), "std-A": (1, 8, 6000), "std-B": (1, 8, 6000), "std-C": (1, 8, 6000),
    "noisy":   (1, 8, 6000), "free": (2, 4, 3000)}
MEAN_COST = 500                                        # mean units per request (assumed, lognormal)

def make_arrivals(seed):
    rnd = random.Random(seed); arr = []
    for step in range(STEPS):
        t = step * STEP
        for name, (tier, rate, _) in TENANTS.items():
            r = rate * (8 if name == "noisy" and 20 <= t < 40 else 1)            # noisy tenant sends 8x for 20 s
            n = 0; x = rnd.random(); p = math.exp(-r * STEP)                      # Poisson count per step by inversion
            c = p
            while x > c: n += 1; p *= r * STEP / n; c += p
            for _ in range(n):
                cost = max(20, int(rnd.lognormvariate(math.log(MEAN_COST) - 0.32, 0.8)))
                arr.append((t, name, cost))
    return arr

def run(arrivals, policy, buckets):
    by_step = collections.defaultdict(list)
    for a in arrivals: by_step[int(a[0] / STEP + 1e-9)].append(a)
    bucket = {n: TENANTS[n][2] * 5.0 for n in TENANTS}                             # burst allowance = 5 s of budget
    queues = {n: collections.deque() for n in TENANTS}; fifo = collections.deque()
    lat, rejected, offered = collections.defaultdict(list), collections.Counter(), collections.Counter()
    for step in range(STEPS + 4000):
        t = step * STEP
        for n in bucket: bucket[n] = min(TENANTS[n][2] * 5.0, bucket[n] + TENANTS[n][2] * STEP)
        for (ta, name, cost) in by_step.get(step, []):
            offered[name] += 1
            if buckets:
                if bucket[name] < cost: rejected[name] += 1; continue              # 429: over budget
                bucket[name] -= cost
            item = [ta, name, cost]
            (fifo if policy == "fifo" else queues[name]).append(item)
        cap = CAP
        def serve(item):
            nonlocal cap
            take = min(cap, item[2]); item[2] -= take; cap -= take
            if item[2] == 0: lat[item[1]].append(t + STEP - item[0]); return True
            return False
        if policy == "fifo":
            while cap > 0 and fifo:
                if serve(fifo[0]): fifo.popleft()
        else:                                                                       # strict tier priority; round-robin quantum inside a tier
            for tier in (0, 1, 2):
                names = [n for n in TENANTS if TENANTS[n][0] == tier]
                while cap > 0 and any(queues[n] for n in names):
                    for n in names:
                        quantum = 200                                               # units this tenant may take per round
                        while cap > 0 and queues[n] and quantum > 0:
                            before = cap
                            if serve(queues[n][0]): queues[n].popleft()
                            quantum -= before - cap
        if step > STEPS and not fifo and not any(queues.values()): break
    return lat, rejected, offered

arr = make_arrivals(4)
tot = sum(c for _, _, c in arr)
print(f"offered work {tot / (STEPS * STEP):,.0f} units/s on average vs capacity {CAP / STEP:,.0f}; the noisy tenant sends 8x for 20 of 60 s")
policies = [("FIFO, no limits", "fifo", False), ("FIFO + token buckets", "fifo", True), ("tiered fair, no limits", "fair", False), ("tiered fair + buckets", "fair", True)]
results = [(name, *run(arr, pol, bk)) for name, pol, bk in policies]
pct = lambda xs, q: sorted(xs)[min(len(xs) - 1, int(q * len(xs)))] if xs else float("nan")
print("\np99 completion latency in seconds (rejected % in brackets)")
print(f"{'tenant':9}" + "".join(f"{n:>26}" for n, *_ in results))
for t in TENANTS:
    row = f"{t:9}"
    for _, lat, rej, off in results:
        row += f"{pct(lat[t], .99):>17.2f} ({rej[t] / off[t]:4.0%})   "
    print(row)
```
**Output (my run):**
```
offered work 30,821 units/s on average vs capacity 30,000; the noisy tenant sends 8x for 20 of 60 s

p99 completion latency in seconds (rejected % in brackets)
tenant              FIFO, no limits      FIFO + token buckets    tiered fair, no limits     tiered fair + buckets
premium              13.00 (  0%)                0.70 (  0%)                0.20 (  0%)                0.20 (  0%)   
std-A                12.90 (  0%)                0.70 (  0%)                0.30 (  0%)                0.30 (  0%)   
std-B                13.00 (  0%)                0.70 (  0%)                0.30 (  0%)                0.30 (  0%)   
std-C                12.90 (  0%)                0.80 (  0%)                0.60 (  0%)                0.60 (  0%)   
noisy                13.00 (  0%)                0.90 ( 49%)               22.50 (  0%)                1.50 ( 49%)   
free                 12.70 (  0%)                0.80 (  0%)               45.00 (  0%)                3.70 (  0%)   
```

**Follow-ups:**
- *Should budgets sum to capacity?* Not necessarily (statistical multiplexing), but premium reservations should be satisfiable together, and you need overload shedding for when the sum is exceeded.
- *How do you price or enforce fairness for long outputs?* Charge by tokens actually processed and cap output tokens per request.
- *What about a tenant that needs guaranteed latency?* A dedicated replica pool with its own autoscaling, billed as such.

**Common mistakes:** request-count limits; strict priority with no budgets (starvation); one shared FIFO; ignoring per-tenant adapters in cache and routing; averaging SLOs across tenants so one tenant's pain disappears.

