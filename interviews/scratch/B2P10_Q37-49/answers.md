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
