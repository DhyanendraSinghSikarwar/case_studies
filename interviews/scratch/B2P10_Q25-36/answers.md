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
