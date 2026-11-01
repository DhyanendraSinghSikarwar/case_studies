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
