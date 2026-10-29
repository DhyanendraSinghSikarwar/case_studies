### Q1 ⭐⭐⭐ 🟢 Hit counter for the last 5 minutes. Implement class `HitCounter(clock)` with `hit()` (records one hit at the current time, returns None) and `getHits()` (returns the number of hits recorded at times t' with now - 300 < t' <= now, so a hit exactly 300 seconds old is NOT counted). Several hits can share one timestamp. Keep a deque of [timestamp, count] pairs and a running total so that memory is bounded by the 300 distinct seconds in the window, and say how the design changes when one second can see a million hits (buckets, which this design already uses) and when you need the last N minutes for large N (a circular array of 300 buckets keyed by second modulo 300, with the stale-bucket check). The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[], ops=[[1, 'hit', []], [2, 'hit', []], [3, 'hit', []], [4, 'getHits', []], [300, 'getHits', []], [301, 'getHits', []], [301, 'hit', []], [302, 'getHits', []], [310, 'getHits', []]] -> [null, null, null, 3, 3, 2, null, 2, 1].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Design problem with a sliding time window. Buckets of [second, count] in a deque, plus a running total. The clock is injected, so tests control time.

**Say this first (1 line):** "A hit at time t counts while now - 300 < t, so age exactly 300 is out. I keep a deque of [second, count] pairs and a running total, and I expire from the left."

**Brute force:**
- Append every timestamp to a list. `getHits` scans the list and counts `now - 300 < t <= now`.
- Time O(total hits) per query. Memory grows forever. A million hits in one second means a million list entries.

**Optimal:**
- Deque of `[second, count]`, oldest on the left, plus `total` (hits currently inside the window).
- `hit`: expire, then add to the last bucket if it has the same second, else append a new bucket. `total += 1`.
- `getHits`: expire, return `total`.
- Expire rule: pop from the left while `bucket_second <= now - 300`, and subtract its count from `total`. That is the exact boundary: age 300 is gone.
- Why expire inside `hit` too: with hits only and no queries, the deque would otherwise grow without bound. Expiring in both keeps it at most 300 buckets.
- Invariant: `total` equals the sum of the counts in the deque, and every bucket second is greater than `now - 300` (after expiring).
- Variant (large N or fixed memory): a circular array of 300 buckets. Index `second % 300`, and store the second stamp in each bucket. On `hit`, if the stamp differs from `now`, the bucket is stale: reset its count to 0 and re-stamp it. On `getHits`, sum only buckets whose stamp is in `(now - 300, now]`. Memory is fixed, but `getHits` is O(300), not O(1).
- A million hits in one second: still ONE bucket. That is why buckets beat one-entry-per-hit.

| Operation | Deque of buckets | Ring of 300 |
|---|---|---|
| `hit` | O(1) amortised | O(1) |
| `getHits` | O(1) amortised | O(300) = O(1) in n, but a bigger constant |
| Memory | at most 300 buckets | exactly 300 buckets |

**Complexity:**
- Each bucket is appended once and popped once, so `hit` and `getHits` are O(1) amortised.
- Memory is O(300) = O(1) in the number of hits.
- Eviction rule: expire when `bucket_second <= now - 300`. No ties: expiry depends only on age.
- Thread safety (concept only): `hit` and `getHits` both mutate the deque and `total`. A lock would have to cover the expire step and the update together, or one reader could see `total` out of step with the deque.

**Dry run:** the first example. `now - 300` is the cutoff; a bucket dies when its second is `<=` the cutoff.

| time | call | cutoff | deque after | returns |
|---|---|---|---|---|
| 1, 2, 3 | hit | negative | [[1,1],[2,1],[3,1]], total 3 | None |
| 4 | getHits | -296 | unchanged | 3 |
| 300 | getHits | 0 | 1 <= 0? no | 3 |
| 301 | getHits | 1 | pop [1,1], total 2 | 2 |
| 301 | hit | 1 | append [301,1], total 3 | None |
| 302 | getHits | 2 | pop [2,1], total 2 | 2 |
| 310 | getHits | 10 | pop [3,1], total 1 | 1 |

**Code:**
```python
import random
from collections import deque

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class HitCounter:                      # optimal: deque of [second, count] + running total
    def __init__(self, clock):
        self.clock = clock; self.q = deque(); self.total = 0
    def _expire(self, now):
        while self.q and self.q[0][0] <= now - 300:   # exactly 300 old is expired
            self.total -= self.q.popleft()[1]
    def hit(self):
        now = self.clock(); self._expire(now)         # expire here too, so hit-only traffic stays bounded
        if self.q and self.q[-1][0] == now: self.q[-1][1] += 1
        else: self.q.append([now, 1])
        self.total += 1
    def getHits(self):
        self._expire(self.clock())
        return self.total

class RingHitCounter:                  # variant: 300 buckets keyed by second % 300, stale check by stamp
    def __init__(self, clock):
        self.clock = clock; self.stamp = [None] * 300; self.cnt = [0] * 300
    def hit(self):
        now = self.clock(); i = now % 300
        if self.stamp[i] != now: self.stamp[i] = now; self.cnt[i] = 0   # stale bucket: reuse it
        self.cnt[i] += 1
    def getHits(self):
        now = self.clock()
        return sum(c for s, c in zip(self.stamp, self.cnt) if s is not None and now - 300 < s <= now)

class NaiveHits:                       # brute force: keep every timestamp, rescan
    def __init__(self, clock): self.clock = clock; self.ts = []
    def hit(self): self.ts.append(self.clock())
    def getHits(self):
        now = self.clock()
        return sum(1 for t in self.ts if now - 300 < t <= now)

def run(cls, ops):
    clk = Clock(); obj = cls(clk); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(obj, m)(*a))
    return out

ex = [[1,'hit',[]],[2,'hit',[]],[3,'hit',[]],[4,'getHits',[]],[300,'getHits',[]],[301,'getHits',[]],
      [301,'hit',[]],[302,'getHits',[]],[310,'getHits',[]]]
want = [None, None, None, 3, 3, 2, None, 2, 1]
for cls in (HitCounter, RingHitCounter, NaiveHits):
    assert run(cls, ex) == want, cls.__name__
print("example ok for all three classes:", run(HitCounter, ex))

random.seed(14)
for case in range(600):
    t = 0; ops = []
    step = random.choice([2, 20, 150])          # small steps: dense; large steps: expiry at 300
    for _ in range(random.randint(0, 60)):
        t += random.randint(0, step)
        ops.append([t, random.choice(['hit', 'hit', 'getHits']), []])
    a = run(HitCounter, ops); assert a == run(NaiveHits, ops) == run(RingHitCounter, ops), ops
print("600 random operation sequences: deque == ring == naive")

# edge cases
assert run(HitCounter, [[5, 'getHits', []]]) == [0]                       # nothing yet
assert run(HitCounter, [[0, 'hit', []], [299, 'getHits', []], [300, 'getHits', []]]) == [None, 1, 0]
assert run(HitCounter, [[7,'hit',[]],[7,'hit',[]],[7,'hit',[]],[7,'getHits',[]]]) == [None]*3 + [3]
clk = Clock(); h = HitCounter(clk); clk.t = 9
for _ in range(10**6): h.hit()                                            # a million hits in one second
assert h.getHits() == 10**6 and len(h.q) == 1
clk.t = 9 + 1000
for s in range(9 + 1000, 9 + 1000 + 5000): clk.t = s; h.hit()       # hits only, never getHits
assert len(h.q) <= 300 and h.total <= 300
print("1,000,000 hits in one second -> 1 deque entry; after 5000 hit-only seconds the deque holds", len(h.q), "entries")
```

**Output (my run):**
```
example ok for all three classes: [None, None, None, 3, 3, 2, None, 2, 1]
600 random operation sequences: deque == ring == naive
1,000,000 hits in one second -> 1 deque entry; after 5000 hit-only seconds the deque holds 300 entries
```

**Edge cases:**
- A hit exactly 300 seconds old is NOT counted (checked: hit at 0, query at 299 gives 1, at 300 gives 0).
- No hits yet: 0.
- Many hits in one second share a bucket (a million hits give a deque of length 1).
- Hit-only traffic: expiring inside `hit` keeps memory bounded.
- Clock never goes backwards (the prompt guarantees it). If it could, expiry would need care.

**Follow-ups:**
- "A million hits per second?" Buckets already handle it: still one entry per second. If one process cannot take the write rate, shard the counters and add them at read time.
- "Last N minutes for large N?" Circular array of N*60 buckets keyed by `second % size`, with the stamp check for stale buckets. Or keep one coarser bucket per minute if second precision is not needed.
- "Multiple threads?" A lock around each method, since both mutate shared state. Concept only here.

**Common mistakes:**
- Using `<` instead of `<=` in the expire test, which keeps age-300 hits.
- Forgetting to subtract the popped bucket's count from `total`.
- One entry per hit instead of per second.
- Expiring only in `getHits`, so hit-only traffic leaks memory.
- Ring buffer without the stamp check: an old bucket from 300 seconds ago is counted as fresh.

### Q2 ⭐⭐⭐ 🟢 [Set A, Q1 of 5, 5 min, 10 pts] Moving average from a data stream. Implement class `MovingAverage(size)` (1 <= size <= 1000) with `next(val)` (|val| <= 10^4) that adds `val` to the stream and returns the average (a float, total / count) of the last `size` values, or of all values so far when fewer than `size` have arrived. Keep a deque and a running total (add the new value, subtract the value that falls out), O(1) per call and O(size) memory; say why recomputing sum(last size values) is O(size) per call and why floats are only formed at the end (the integer total is exact). This is a ring-buffer idea (compare the circular queue of Part 4 Q22) and the fixed-window average of Part 2 Q3, but online. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[3], ops=[['next', [1]], ['next', [10]], ['next', [3]], ['next', [5]], ['next', [-4]]] -> [1.0, 5.5, 4.666666666666667, 6.0, 1.3333333333333333].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Online sliding window (fixed size, stream). Deque plus a running total. It is the streaming form of the fixed-window average (Part 2 Q3) and a ring-buffer idea (compare the circular queue of Part 4 Q22).

**Say this first (1 line):** "I keep a deque of the last `size` values and an exact integer total. Add the new value, subtract the one that falls out, divide at the end."

**Brute force:**
- Keep every value in a list. On each call, `sum(a[-size:]) / len(a[-size:])`.
- O(size) per call and O(total calls) memory.

**Optimal:**
- `next(val)`: append `val`, `total += val`. If the deque now holds more than `size` values, `total -= popleft()`.
- Return `total / len(deque)`. Before `size` values have arrived, `len` is the count so far, so the first call returns the value itself.
- The float is formed only at the end. The total is an integer, so it is exact and never drifts. Adding floats one by one would accumulate rounding error.
- Invariant: `total == sum(deque)` and `len(deque) <= size`.

**Complexity:**
- `next` is O(1): one append, at most one pop, one division.
- Memory O(size), at most 1000 values.
- Rule on ties/eviction: strictly FIFO. The oldest value leaves first.
- Thread safety (concept only): `next` changes the deque and `total` together, so concurrent callers would need a lock around the whole method.

**Dry run:** `size = 3`.

| call | deque after | total | returns |
|---|---|---|---|
| next(1) | [1] | 1 | 1/1 = 1.0 |
| next(10) | [1,10] | 11 | 11/2 = 5.5 |
| next(3) | [1,10,3] | 14 | 14/3 = 4.666... |
| next(5) | [10,3,5] (1 left) | 14 + 5 - 1 = 18 | 18/3 = 6.0 |
| next(-4) | [3,5,-4] (10 left) | 18 - 4 - 10 = 4 | 4/3 = 1.333... |

**Code:**
```python
import random
from collections import deque

class MovingAverage:                   # optimal: deque + exact integer running total
    def __init__(self, size):
        self.size = size; self.q = deque(); self.total = 0
    def next(self, val):
        self.q.append(val); self.total += val
        if len(self.q) > self.size:
            self.total -= self.q.popleft()      # the value that fell out of the window
        return self.total / len(self.q)         # the only float, formed at the end

class NaiveMA:                         # brute force: keep everything, re-sum the last `size` each call
    def __init__(self, size): self.size = size; self.a = []
    def next(self, val):
        self.a.append(val); w = self.a[-self.size:]
        return sum(w) / len(w)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

ex = [['next',[1]],['next',[10]],['next',[3]],['next',[5]],['next',[-4]]]
want = [1.0, 5.5, 4.666666666666667, 6.0, 1.3333333333333333]
assert run(MovingAverage, [3], ex) == want == run(NaiveMA, [3], ex)
print("example:", run(MovingAverage, [3], ex))

random.seed(14)
for _ in range(500):
    size = random.randint(1, 6)
    ops = [['next', [random.randint(-10**4, 10**4)]] for _ in range(random.randint(0, 40))]
    assert run(MovingAverage, [size], ops) == run(NaiveMA, [size], ops)
print("500 random sequences: deque version == naive version (exact float equality)")

# edge cases
assert run(MovingAverage, [1], [['next',[7]],['next',[-3]]]) == [7.0, -3.0]        # size 1
m = MovingAverage(1000)
for _ in range(5000): r = m.next(10**4)
assert r == 10**4 and m.total == 1000 * 10**4 and len(m.q) == 1000                  # max size, max value
m = MovingAverage(3); assert [m.next(0) for _ in range(4)] == [0.0]*4              # all zeros
m = MovingAverage(2)
assert [m.next(v) for v in (-10**4, -10**4, 10**4)] == [-10000.0, -10000.0, 0.0]   # negatives
# floats would drift: sum of 0.1s vs the exact integer total
f = 0.0
for _ in range(10): f += 0.1
print("float total after ten +0.1:", f, "(integer totals never drift)")
print("edge asserts ok")
```

**Output (my run):**
```
example: [1.0, 5.5, 4.666666666666667, 6.0, 1.3333333333333333]
500 random sequences: deque version == naive version (exact float equality)
float total after ten +0.1: 0.9999999999999999 (integer totals never drift)
edge asserts ok
```

**Edge cases:**
- `size = 1`: the average is the latest value.
- Fewer than `size` values so far: divide by the count, not by `size`.
- Negatives and all zeros work with the exact integer total.
- Maximum `size` 1000 and value 10^4: total stays tiny, no overflow in Python anyway.

**Follow-ups:**
- Scoring note (Set A, Q1 of 5, 5 min, 10 pts). Full 3/3 on rules: say out loud that the window is the last `size` values, that the early calls divide by the count, and that the return is a float. Partial: only "sliding window". Full 3/3 on code: correct and it passes the example plus the random check against the naive version. Full 2/2 on complexity: O(1) per call because each value is added once and removed once, O(size) memory; partial for the claim without the reason. 1/1 for edge cases (size 1, fewer than size values). 1/1 for a spoken summary under 60 seconds. How I would pace this: 1 minute stating rules, 2 minutes coding, 1 minute on the dry run and random check, 1 minute on complexity and the summary.
- "Why not float totals?" Rounding errors accumulate over millions of calls. An integer total plus one final division is exact.
- "Could it be a fixed array?" Yes: a ring buffer with an index. Same O(1), no allocation.

**Common mistakes:**
- Dividing by `size` before the window is full.
- Recomputing `sum` of the window every call (O(size)).
- Subtracting before appending, which pops the wrong value when `size = 1`.
- Keeping a float running sum.

### Q3 ⭐⭐⭐ 🟢 [Set B, Q1 of 5, 5 min, 10 pts] Is this graph a tree? `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges`, a list of undirected [u, v] pairs (0 <= len <= 2*10^5; repeats and self loops may occur). Return True exactly when the graph is a tree: connected with no cycle. A parallel edge and a self loop are cycles. Union-find (Part 9 Q13): a tree on n nodes has exactly n - 1 edges, so return False at once for any other count, then union the endpoints and return False when an edge joins two nodes that already share a root. Say why n - 1 edges plus 'no cycle' implies connectedness, and how it differs from Part 9 Q14 (which finds the extra edge in an otherwise tree-like graph). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a BFS connectivity check combined with the edge-count identity on small inputs. Example: n=5, edges=[[0, 1], [0, 2], [0, 3], [1, 4]] -> True; n=5, edges=[[0, 1], [1, 2], [2, 3], [1, 3]] -> False; n=1, edges=[] -> True; n=2, edges=[[0, 1], [0, 1]] -> False.
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Union-find (Part 9 Q13) for cycle detection, plus the tree edge-count identity. A graph on n nodes is a tree if and only if it has exactly n - 1 edges and no cycle.

**Say this first (1 line):** "A tree has exactly n - 1 edges, so any other count is False at once. Then I union the endpoints, and an edge whose ends already share a root is a cycle."

**Brute force:**
- BFS from node 0, check that all n nodes are reached (connected), and check that the edge count is n - 1 (the identity that rules out a cycle).
- O(n + m) time with an adjacency list. It is correct, and also a fine oracle.

**Optimal:**
- If `len(edges) != n - 1`, return False. Too few edges cannot connect n nodes. Too many must contain a cycle.
- Otherwise union each edge. If `find(u) == find(v)` the edge closes a cycle: return False. A self loop `[u, u]` has equal roots, so it is caught. A repeated edge `[u, v]` twice is caught on the second copy.
- If no edge fails, return True.
- Why connected follows: n nodes start as n components. Each successful union merges two, so n - 1 successful unions leave 1 component. Since every one of the n - 1 edges succeeded (no cycle), the graph is connected.
- Difference from Part 9 Q14: there the graph already has one extra edge, and you must FIND it (the last edge that closes a cycle). Here you only decide yes or no.
- Path halving inside `find` keeps trees flat without recursion.

**Complexity:**
- Edge count check O(1). Unions: m = n - 1 calls, each nearly O(1) (inverse Ackermann). Total about O(n).
- Space O(n) for `parent`.
- No tie rules apply. Thread safety (concept only): not relevant for a one-shot function.

**Dry run:** `n = 5, edges = [[0,1],[1,2],[2,3],[1,3]]`. Edge count is 4 = n - 1, so continue.

| edge | find(u), find(v) | action |
|---|---|---|
| [0,1] | 0, 1 | union, ok |
| [1,2] | root(1), 2 | union, ok |
| [2,3] | root(2), 3 | union, ok |
| [1,3] | same root (0..3 are one set) | cycle, return False |

Node 4 was never reached either, which is the "cycle implies disconnected" side of the identity.

**Code:**
```python
import random
from collections import deque

def is_tree(n, edges):                 # optimal: edge count, then union-find with path halving
    if len(edges) != n - 1: return False
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv: return False      # self loop, parallel edge or a longer cycle
        parent[ru] = rv
    return True

def is_tree_brute(n, edges):           # brute force: BFS connectivity + "no cycle" by edge count identity
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)   # a self loop adds u to its own list
    seen = {0}; q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen: seen.add(v); q.append(v)
    return len(seen) == n and len(edges) == n - 1           # connected and exactly n-1 edges

examples = [(5, [[0,1],[0,2],[0,3],[1,4]], True), (5, [[0,1],[1,2],[2,3],[1,3]], False),
            (1, [], True), (2, [[0,1],[0,1]], False)]
for n, e, w in examples:
    assert is_tree(n, e) == is_tree_brute(n, e) == w
print("examples:", [is_tree(n, e) for n, e, _ in examples])

random.seed(14); trues = 0
for _ in range(2000):
    n = random.randint(1, 7); m = random.choice([n - 1, n - 1, random.randint(0, 9)])
    if random.random() < .5 and n > 1:      # build a real tree half the time, then maybe perturb
        e = [[random.randrange(i), i] for i in range(1, n)]
        if random.random() < .3: e[random.randrange(len(e))] = [random.randrange(n), random.randrange(n)]
    else:
        e = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    random.shuffle(e); a = is_tree(n, e); assert a == is_tree_brute(n, e), (n, e); trues += a
print("2000 random small graphs agree with BFS + edge-count check;", trues, "were trees")

# edge cases
assert is_tree(1, []) and not is_tree(1, [[0, 0]])         # lone node ok, self loop is a cycle
assert not is_tree(3, [[0, 1]])                            # too few edges: disconnected
assert not is_tree(4, [[0, 1], [0, 1], [2, 3]])            # n-1 edges but a cycle, so also disconnected
assert not is_tree(3, [])                                  # no edges, n > 1
n = 10**5; path = [[i, i + 1] for i in range(n - 1)]
assert is_tree(n, path)                                    # deep path: no recursion used
assert not is_tree(n, path[:-1] + [[0, n - 2]])            # long path closed into a cycle
assert not is_tree(n, path + [[0, n - 1]])                 # n edges
print("edge asserts ok, including a 10^5-node path")
```

**Output (my run):**
```
examples: [True, False, True, False]
2000 random small graphs agree with BFS + edge-count check; 1063 were trees
edge asserts ok, including a 10^5-node path
```

**Edge cases:**
- `n = 1, edges = []` is a tree. `n = 1, edges = [[0,0]]` is not (self loop, and the count is wrong).
- `n = 2` with `[[0,1],[0,1]]`: two edges, not n - 1, so False.
- n - 1 edges but a cycle plus an isolated node: False from the union step.
- 10^5-node path: union-find uses no recursion, so no recursion limit issue.

**Follow-ups:**
- Scoring note (Set B, Q1 of 5, 5 min, 10 pts). Full 3/3 on rules: say that a parallel edge and a self loop are cycles, that n - 1 edges is required, and that n = 1 with no edges is a tree. Partial: "connected and acyclic" only. 3/3 on code: passes the examples and the random check against BFS. 2/2 on complexity: about O(n) with the reason (n - 1 near-constant unions); partial without the reason. 1/1 for edge cases. 1/1 for a crisp summary under 60 seconds. How I would pace this: 1 minute on rules and the edge-count shortcut, 2 minutes coding, 1 minute testing, 1 minute on complexity and the summary.
- "Directed version?" That is a rooted-tree check: exactly one node of in-degree 0, all others in-degree 1, and everything reachable from the root.
- "Why not DFS?" It works, but needs an iterative stack at 10^5 nodes and a parent check for parallel edges. Union-find avoids both.

**Common mistakes:**
- Skipping the edge-count check. Then a forest such as `n = 4`, edges `[[0,1],[2,3]]` (no cycle, but disconnected) wrongly returns True.
- Treating a self loop or a repeated edge as fine.
- Recursive `find` without path compression on a long chain.
- Testing only connectivity (BFS) and forgetting the cycle side.

### Q4 ⭐⭐⭐ 🟡 LRU cache with collections.OrderedDict. Implement class `LRUCache(capacity)` (1 <= capacity <= 3000) with `get(key)` and `put(key, value)`, both O(1) on average. `get` returns the value, or -1 when the key is absent, and a successful `get` makes the key the most recently used. `put` on a new key inserts it as most recently used; `put` on an existing key replaces the value and also makes it most recently used; after an insert that leaves more than `capacity` keys, evict the least recently used key (a failed `get` changes nothing). `put` returns None. Use `move_to_end` and `popitem(last=False)` and say why a plain dict (insertion order only) is not enough. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). The hand-built doubly linked list version is Q5 (the linked-list idea is Part 6 Q30; sentinel pointer practice is Part 6 Q29). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[2], ops=[['put', [1, 1]], ['put', [2, 2]], ['get', [1]], ['put', [3, 3]], ['get', [2]], ['put', [4, 4]], ['get', [1]], ['get', [3]], ['get', [4]]] -> [null, null, 1, null, -1, null, -1, 3, 4]; init=[1], ops=[['put', [5, 10]], ['put', [5, 20]], ['get', [5]], ['put', [6, 1]], ['get', [5]], ['get', [6]]] -> [null, null, 20, null, -1, 1].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Design problem, hash map plus recency order. `OrderedDict` is exactly that pair: O(1) lookup and a movable order.

**Say this first (1 line):** "I keep the most recent key at the END of an OrderedDict. A hit does `move_to_end`, and an overflow does `popitem(last=False)` to drop the front."

**Brute force:**
- A plain dict for values plus a list of keys in recency order.
- Each `get` and `put` does `list.remove(key)` (O(n)), and eviction does `pop(0)` (O(n)).
- O(capacity) per operation. It is also the oracle in the code.

**Optimal:**
- `get(key)`: if absent return -1 and change nothing. Else `move_to_end(key)` and return the value.
- `put(key, value)`: if the key exists, `move_to_end` first (an update is a use). Set the value. If `len > capacity`, `popitem(last=False)` removes the least recently used key.
- Eviction rule: exactly one key is evicted, only after an insert of a NEW key pushes the size over capacity. Updating an existing key never evicts. A failed `get` is not a use.
- Why a plain dict is not enough, stated carefully: a dict remembers insertion order but has no O(1) "move this key to the end" operation. You can fake it with `pop` and re-insert, and `next(iter(d))` finds the oldest key. But I measured the catch: after many deletions at the front, CPython's dict keeps dead slots, and `next(iter(d))` has to scan past them, so it can be far slower than O(1) (see the last line of the output; sandbox timing only). `OrderedDict` has a linked list inside and does both moves in O(1).
- Invariant: keys are ordered least recent to most recent, and `len <= capacity` after every `put`.

**Complexity:**
- `get` and `put`: O(1) average (hash lookup plus a linked-list move).
- Space O(capacity).
- Thread safety (concept only): `get` mutates the order, so even reads need exclusion. A lock around each method, or striped locks per shard, would protect the dict and its order together.

**Dry run:** first example, capacity 2.

| call | cache (LRU -> MRU) | returns |
|---|---|---|
| put(1,1) | [1] | None |
| put(2,2) | [1,2] | None |
| get(1) | [2,1] | 1 |
| put(3,3) | [2,1,3] too big, evict 2 -> [1,3] | None |
| get(2) | [1,3] | -1 |
| put(4,4) | [1,3,4] evict 1 -> [3,4] | None |
| get(1) | [3,4] | -1 |
| get(3) | [4,3] | 3 |
| get(4) | [3,4] | 4 |

**Code:**
```python
import random, time
from collections import OrderedDict

class LRUCache:                        # optimal: OrderedDict, most recent at the END
    def __init__(self, capacity):
        self.cap = capacity; self.d = OrderedDict()
    def get(self, key):
        if key not in self.d: return -1         # a miss changes nothing
        self.d.move_to_end(key)                 # O(1): a hit makes it most recent
        return self.d[key]
    def put(self, key, value):
        if key in self.d: self.d.move_to_end(key)   # update also refreshes recency
        self.d[key] = value
        if len(self.d) > self.cap:
            self.d.popitem(last=False)          # evict the least recent (front)

class NaiveLRU:                        # brute force: plain dict + a list of keys, O(n) remove
    def __init__(self, capacity): self.cap = capacity; self.val = {}; self.order = []   # oldest first
    def get(self, key):
        if key not in self.val: return -1
        self.order.remove(key); self.order.append(key); return self.val[key]
    def put(self, key, value):
        if key in self.val: self.order.remove(key)
        elif len(self.val) == self.cap:
            old = self.order.pop(0); del self.val[old]
        self.val[key] = value; self.order.append(key)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([2], [['put',[1,1]],['put',[2,2]],['get',[1]],['put',[3,3]],['get',[2]],['put',[4,4]],['get',[1]],['get',[3]],['get',[4]]],
      [None,None,1,None,-1,None,-1,3,4])
e2 = ([1], [['put',[5,10]],['put',[5,20]],['get',[5]],['put',[6,1]],['get',[5]],['get',[6]]], [None,None,20,None,-1,1])
for init, ops, want in (e1, e2):
    assert run(LRUCache, init, ops) == want == run(NaiveLRU, init, ops)
print("examples:", run(LRUCache, *e1[:2]), run(LRUCache, *e2[:2]))

random.seed(14)
for _ in range(1000):
    cap = random.randint(1, 4)
    ops = [random.choice([['get', [random.randint(0, 5)]], ['put', [random.randint(0, 5), random.randint(0, 99)]]])
           for _ in range(random.randint(0, 50))]
    assert run(LRUCache, [cap], ops) == run(NaiveLRU, [cap], ops), (cap, ops)
print("1000 random operation sequences: OrderedDict == naive")

# edge cases
c = LRUCache(1); c.put(1, 1); c.put(1, 2); assert c.get(1) == 2 and len(c.d) == 1   # update at capacity does not evict
c.put(2, 3); assert c.get(1) == -1 and c.get(2) == 3
assert LRUCache(2).get(9) == -1                                                    # empty cache
c = LRUCache(2); c.put(1, 1); c.put(2, 2); c.get(9); c.put(3, 3)                  # failed get must not refresh
assert c.get(1) == -1 and c.get(2) == 2
c = LRUCache(3000)
for k in range(10**5): c.put(k, k)
assert len(c.d) == 3000 and list(c.d)[0] == 10**5 - 3000
print("edge asserts ok (capacity 1, update at capacity, failed get, 10^5 puts at capacity 3000)")

# Claim check: can a PLAIN dict do it? Yes by pop + re-insert, and next(iter(d)) finds the oldest key,
# but after many deletions at the front the dict keeps dead slots and next(iter(d)) scans them.
d = {k: k for k in range(200000)}
for k in range(199990): del d[k]
t = time.perf_counter()
for _ in range(200): next(iter(d))
slow = time.perf_counter() - t
d2 = {k: k for k in range(10)}
t = time.perf_counter()
for _ in range(200): next(iter(d2))
fast = time.perf_counter() - t
print("sandbox timing: dict with a dead front, oldest-key lookup more than 10x slower than fresh dict:", slow > 10 * fast)
```

**Output (my run):**
```
examples: [None, None, 1, None, -1, None, -1, 3, 4] [None, None, 20, None, -1, 1]
1000 random operation sequences: OrderedDict == naive
edge asserts ok (capacity 1, update at capacity, failed get, 10^5 puts at capacity 3000)
sandbox timing: dict with a dead front, oldest-key lookup more than 10x slower than fresh dict: True
```

**Edge cases:**
- Capacity 1: every new key evicts the previous one; updating the same key must not evict it.
- `put` on an existing key at full capacity: no eviction.
- `get` miss on an empty cache returns -1.
- A failed `get` must not change the order.
- Values may be 0 or falsy: test `key in d`, not `if d.get(key)`.

**Follow-ups:**
- "Build it without OrderedDict?" That is Q5: dict plus doubly linked list with sentinels.
- "Add expiry or a frequency policy?" Those need a clock or per-frequency lists; different designs, not a small tweak.
- "Why `popitem(last=False)`?" `last=True` (the default) pops the NEWEST key, which is MRU eviction, a bug here.

**Common mistakes:**
- Forgetting `move_to_end` on `get` or on an update `put`.
- Evicting before checking whether the key already exists.
- Using `popitem()` with the default, which removes the most recent key.
- Treating `get` returning 0 as a miss.

### Q5 ⭐⭐⭐ 🟡 LRU cache from scratch: a doubly linked list with sentinels plus a dict. Implement class `LRUCache(capacity)` (1 <= capacity <= 3000) with `get(key)`, `put(key, value)`, `order()` and `size()`; do NOT use OrderedDict, and write the node class and the two helpers `_unlink(node)` and `_push_front(node)` yourself, with a dummy head and a dummy tail so no pointer move needs an `if node is None` case. Rules: `get` returns the value or -1 and makes a found key the most recently used; `put` inserts or updates a key as most recently used and, when an insert would exceed `capacity`, first evicts the least recently used key (store the key inside the node so the evicted node can be deleted from the dict). `order()` returns the keys from most recently used to least recently used, `size()` the number of stored keys; `put` returns None. State why each of the four pointer assignments of an unlink matters, why a singly linked list cannot unlink in O(1), and say as a stated concept only (not code) what a lock around `get` and `put` would protect: both methods mutate the list, so even `get` is a write. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[3], ops=[['put', [1, 'a']], ['put', [2, 'b']], ['put', [3, 'c']], ['order', []], ['get', [1]], ['order', []], ['put', [4, 'd']], ['order', []], ['get', [2]], ['size', []]] -> [null, null, null, [3, 2, 1], 'a', [1, 3, 2], null, [4, 1, 3], -1, 3]; init=[1], ops=[['put', [1, 1]], ['put', [2, 2]], ['get', [1]], ['get', [2]], ['order', []]] -> [null, null, -1, 2, [2]].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Design problem, dict plus a hand-built doubly linked list with dummy head and dummy tail. The dict gives O(1) find, the list gives O(1) reorder.

**Say this first (1 line):** "Dict maps key to node. A doubly linked list keeps recency, head side most recent, tail side least recent, and two sentinels remove every null check."

**Brute force:**
- A list of `[key, value]` pairs in recency order. Scan to find, `pop(i)` to move, `pop(0)` to evict.
- O(capacity) per call. It is the oracle in the code.

**Optimal:**
- Nodes hold `key`, `val`, `prev`, `next`. Dummy `head` and dummy `tail` always exist, so a real node always has two neighbours and no `if node is None` appears in the pointer code.
- `_unlink(node)`: two assignments, `node.prev.next = node.next` and `node.next.prev = node.prev`. Skip either one and a neighbour still points at the removed node (a dangling link, then wrong `order()`, or an infinite loop).
- `_push_front(node)`: four assignments. `node.prev = head`, `node.next = head.next`, `head.next.prev = node`, `head.next = node`. Do them in that order. If you set `head.next = node` first, you lose the old first node.
- A move to front is unlink (2) plus push (4).
- Why a singly linked list cannot unlink in O(1): to unlink a node you must change the PREVIOUS node's `next`, and a singly linked node has no pointer to its previous node. You would walk from the head, O(n).
- `get`: miss returns -1. Hit unlinks and pushes front, returns the value.
- `put`: existing key updates value and moves to front. New key: if the dict already holds `capacity` keys, evict `tail.prev` first (unlink and `del map[lru.key]`, which is why the node stores its key), then create the node and push front.
- Eviction rule: evict before inserting a NEW key at full capacity; an update never evicts; the victim is always `tail.prev`. No ties exist because recency is a strict total order.
- Invariant: following `next` from head visits exactly the keys in the dict, most recent first, and `prev` pointers mirror them.

**Complexity:**
- `get`, `put`, `size`: O(1). `order()`: O(n), it walks the list.
- Space O(capacity).
- Thread safety (concept only): both methods mutate the list and the dict. Even `get` is a write, because it re-links the node. One lock would have to cover the dict lookup AND the unlink/push together; a read-write lock does not help because there are no pure reads.

**Dry run:** first example, capacity 3. `order()` lists most recent first.

| call | list after (MRU -> LRU) | returns |
|---|---|---|
| put 1,2,3 | 3,2,1 | None |
| order | 3,2,1 | [3,2,1] |
| get(1) | 1,3,2 | 'a' |
| order | 1,3,2 | [1,3,2] |
| put(4,'d') | full: evict tail.prev = 2, then 4,1,3 | None |
| order | 4,1,3 | [4,1,3] |
| get(2) | 4,1,3 | -1 |
| size | 3 keys | 3 |

**Code:**
```python
import random

class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key = key; self.val = val; self.prev = None; self.next = None

class LRUCache:                        # dict + doubly linked list, dummy head (MRU side) and dummy tail (LRU side)
    def __init__(self, capacity):
        self.cap = capacity; self.map = {}
        self.head = Node(); self.tail = Node()
        self.head.next = self.tail; self.tail.prev = self.head
    def _unlink(self, node):
        node.prev.next = node.next          # unlink 1: left neighbour skips node
        node.next.prev = node.prev          # unlink 2: right neighbour skips node
        # node.prev / node.next are stale now; _push_front overwrites both
    def _push_front(self, node):
        node.prev = self.head               # push 1
        node.next = self.head.next          # push 2
        self.head.next.prev = node          # push 3: old first node points back at us
        self.head.next = node               # push 4: head points forward at us
    def get(self, key):
        node = self.map.get(key)
        if node is None: return -1
        self._unlink(node); self._push_front(node)      # even a read mutates the list
        return node.val
    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.val = value; self._unlink(node); self._push_front(node); return
        if len(self.map) == self.cap:
            lru = self.tail.prev            # never the head dummy because cap >= 1
            self._unlink(lru); del self.map[lru.key]    # node stores its key for exactly this delete
        node = Node(key, value); self.map[key] = node; self._push_front(node)
    def order(self):
        out = []; n = self.head.next
        while n is not self.tail: out.append(n.key); n = n.next
        return out
    def size(self): return len(self.map)

class NaiveLRU:                        # brute force: list of [key, value], least recent first, O(n) scans
    def __init__(self, capacity): self.cap = capacity; self.items = []
    def _find(self, key):
        for i, (k, _) in enumerate(self.items):
            if k == key: return i
        return -1
    def get(self, key):
        i = self._find(key)
        if i < 0: return -1
        kv = self.items.pop(i); self.items.append(kv); return kv[1]
    def put(self, key, value):
        i = self._find(key)
        if i >= 0: self.items.pop(i)
        elif len(self.items) == self.cap: self.items.pop(0)
        self.items.append([key, value])
    def order(self): return [k for k, _ in reversed(self.items)]
    def size(self): return len(self.items)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([3], [['put',[1,'a']],['put',[2,'b']],['put',[3,'c']],['order',[]],['get',[1]],['order',[]],['put',[4,'d']],
            ['order',[]],['get',[2]],['size',[]]], [None,None,None,[3,2,1],'a',[1,3,2],None,[4,1,3],-1,3])
e2 = ([1], [['put',[1,1]],['put',[2,2]],['get',[1]],['get',[2]],['order',[]]], [None,None,-1,2,[2]])
for init, ops, want in (e1, e2):
    assert run(LRUCache, init, ops) == want == run(NaiveLRU, init, ops)
print("examples:", run(LRUCache, *e1[:2]), run(LRUCache, *e2[:2]))

def check_links(c):                    # structural invariant: forward and backward walks agree with the dict
    fwd = []; n = c.head.next
    while n is not c.tail: assert n.prev.next is n and n.next.prev is n; fwd.append(n.key); n = n.next
    assert len(fwd) == len(c.map) <= c.cap and set(fwd) == set(c.map)

random.seed(14)
for _ in range(1000):
    cap = random.randint(1, 4)
    ops = [random.choice([['get', [random.randint(0, 5)]], ['put', [random.randint(0, 5), random.randint(0, 99)]],
                          ['order', []], ['size', []]]) for _ in range(random.randint(0, 50))]
    assert run(LRUCache, [cap], ops) == run(NaiveLRU, [cap], ops), (cap, ops)
    c = LRUCache(cap)
    for m, a in ops: getattr(c, m)(*a); check_links(c)
print("1000 random operation sequences: linked list == naive, links consistent after every call")

# edge cases
c = LRUCache(1); c.put(1, 1); c.put(1, 2); assert c.order() == [1] and c.get(1) == 2   # update at capacity: no eviction
c.put(2, 3); assert c.get(1) == -1 and c.order() == [2]
c = LRUCache(2); assert c.get(0) == -1 and c.order() == [] and c.size() == 0           # empty
c.put(1, 1); c.put(2, 2); c.get(1); c.put(3, 3); assert c.order() == [3, 1]            # 2 was least recent
c = LRUCache(3000)
for k in range(10**5): c.put(k, k)
assert c.size() == 3000 and c.order()[0] == 10**5 - 1 and c.order()[-1] == 10**5 - 3000
print("edge asserts ok (capacity 1, empty, 10^5 puts at capacity 3000)")
```

**Output (my run):**
```
examples: [None, None, None, [3, 2, 1], 'a', [1, 3, 2], None, [4, 1, 3], -1, 3] [None, None, -1, 2, [2]]
1000 random operation sequences: linked list == naive, links consistent after every call
edge asserts ok (capacity 1, empty, 10^5 puts at capacity 3000)
```

**Edge cases:**
- Capacity 1: second put evicts the first (second example: after `put 2`, key 1 is gone, `get(1)` returns -1).
- Update at capacity: no eviction.
- Empty cache: `order()` is `[]`, `get` is -1.
- Node must store its key, otherwise the evicted node cannot be removed from the dict.
- The checker runs the structural check after every call in my cross-test: forward and backward links agree.

**Follow-ups:**
- "Why dummy nodes?" With sentinels, insert and remove at the ends are the same code as in the middle. Without them you branch on empty list, first node, last node.
- "Why not OrderedDict?" It is the Q4 answer and fine in practice. Interviewers ask for this version to see the pointer work.
- "Make it thread-safe?" State the lock scope as above; no code needed.

**Common mistakes:**
- Wrong order of the four push assignments, losing the old first node.
- Moving a node on `get` but forgetting it on an update `put`.
- Evicting `head.next` instead of `tail.prev`.
- Not storing the key in the node.
- Evicting when merely updating an existing key.
- Prompt wording note: the prompt says "four pointer assignments of an unlink". An unlink itself is two assignments; four is the push-front. I explain both above.

### Q6 ⭐⭐⭐ 🟡 Time-based key-value store with bisect. Implement class `TimeMap()` with `set(key, value, timestamp)` (returns None) and `get(key, timestamp)`. `get` returns the value stored for `key` with the LARGEST stored timestamp that is <= `timestamp`, or the empty string '' when the key is unknown or every stored timestamp is greater. For one key the `set` timestamps are strictly increasing (1 <= timestamp <= 10^7), so each key keeps two parallel lists that stay sorted; `get` must use `bisect_right` (explain why bisect_left would be wrong when the timestamp equals a stored one: compare Part 5 Q11) and cost O(log m) for m values under that key, `set` O(1). Up to 2*10^5 operations. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[], ops=[['set', ['love', 'high', 10]], ['get', ['love', 10]], ['get', ['love', 15]], ['set', ['love', 'low', 20]], ['get', ['love', 5]], ['get', ['love', 19]], ['get', ['love', 20]], ['get', ['hate', 10]]] -> [null, 'high', 'high', null, '', 'high', 'low', ''].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Design problem plus binary search on sorted history. Per key, two parallel lists (timestamps, values) that stay sorted because timestamps only grow.

**Say this first (1 line):** "`get` wants the last stored timestamp that is <= the query. `bisect_right` returns the first index with a timestamp greater than the query, so the answer is the value just before it."

**Brute force:**
- Store every `(key, value, timestamp)` row in one list. On `get`, scan all rows for the key and keep the one with the largest timestamp <= query.
- O(total rows) per `get`. With 2*10^5 operations this is too slow.

**Optimal:**
- `set`: append the timestamp to `ts[key]` and the value to `vs[key]`. Timestamps are strictly increasing per key, so both lists stay sorted for free. O(1).
- `get`: `i = bisect_right(ts[key], timestamp)`. If `i == 0`, every stored timestamp is larger (or none exist): return ''. Else return `vs[key][i - 1]`.
- Why `bisect_right` and not `bisect_left`: for a stored timestamp EQUAL to the query, `bisect_left` returns that equal element's own index, so `i - 1` steps back one entry too far and returns the previous value (or '' when it is the first). `bisect_right` goes past equal elements, so `i - 1` lands on the equal element itself. The output below shows the wrong version failing the prompt's own example (compare Part 5 Q11).
- Tie rule: a query at exactly a stored timestamp returns THAT entry's value. Timestamps for one key never repeat, so there is no tie between two values.
- Unknown key: return ''. Different keys never interact.
- Invariant: each `ts[key]` is strictly increasing and the same length as `vs[key]`.

**Complexity:**
- `set` O(1) amortised (list append).
- `get` O(log m) for m values under that key, plus an O(1) dict lookup.
- Space O(total sets).
- Thread safety (concept only): appends and binary searches on the same key would need a lock (or an append-only structure with a published length) so a reader never sees timestamps and values out of step.

**Dry run:** first example.

| call | state for 'love' | result |
|---|---|---|
| set(love, high, 10) | ts [10], vs [high] | None |
| get(love, 10) | bisect_right([10], 10) = 1, take index 0 | high |
| get(love, 15) | bisect_right = 1, index 0 | high |
| set(love, low, 20) | ts [10,20] | None |
| get(love, 5) | bisect_right([10,20], 5) = 0 | '' |
| get(love, 19) | bisect_right = 1, index 0 | high |
| get(love, 20) | bisect_right = 2, index 1 | low |
| get(hate, 10) | unknown key | '' |

**Code:**
```python
import random
from bisect import bisect_right, bisect_left

class TimeMap:                         # optimal: per key two parallel sorted lists
    def __init__(self): self.ts = {}; self.vs = {}
    def set(self, key, value, timestamp):
        self.ts.setdefault(key, []).append(timestamp)     # timestamps arrive strictly increasing per key
        self.vs.setdefault(key, []).append(value)
    def get(self, key, timestamp):
        ts = self.ts.get(key)
        if not ts: return ''
        i = bisect_right(ts, timestamp)                   # first index with ts > timestamp
        return self.vs[key][i - 1] if i else ''           # i - 1 is the last ts <= timestamp

class WrongTimeMap(TimeMap):           # the classic bug, kept only to show it fails
    def get(self, key, timestamp):
        ts = self.ts.get(key)
        if not ts: return ''
        i = bisect_left(ts, timestamp)                    # first index with ts >= timestamp
        return self.vs[key][i - 1] if i else ''

class NaiveTimeMap:                    # brute force: one flat list of rows, scan all of them
    def __init__(self): self.rows = []
    def set(self, key, value, timestamp): self.rows.append((key, value, timestamp))
    def get(self, key, timestamp):
        best = None
        for k, v, t in self.rows:
            if k == key and t <= timestamp and (best is None or t > best[0]): best = (t, v)
        return best[1] if best else ''

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

ex = [['set',['love','high',10]],['get',['love',10]],['get',['love',15]],['set',['love','low',20]],['get',['love',5]],
      ['get',['love',19]],['get',['love',20]],['get',['hate',10]]]
want = [None,'high','high',None,'','high','low','']
assert run(TimeMap, [], ex) == want == run(NaiveTimeMap, [], ex)
print("example:", run(TimeMap, [], ex))
print("bisect_left version on the same example:", run(WrongTimeMap, [], ex))
assert run(WrongTimeMap, [], ex) != want

random.seed(14)
for _ in range(1000):
    last = {}; ops = []
    for _ in range(random.randint(0, 40)):
        k = random.choice('abc')
        if random.random() < .5:
            last[k] = last.get(k, 0) + random.randint(1, 4)
            ops.append(['set', [k, 'v%d' % random.randint(0, 99), last[k]]])
        else: ops.append(['get', [k, random.randint(0, 30)]])
    assert run(TimeMap, [], ops) == run(NaiveTimeMap, [], ops), ops
print("1000 random operation sequences: bisect_right version == naive")

# edge cases
m = TimeMap(); assert m.get('x', 5) == ''                          # unknown key
m.set('x', 'a', 3); assert m.get('x', 2) == '' and m.get('x', 3) == 'a' and m.get('x', 10**7) == 'a'   # before first, exact, far after
m = TimeMap()
for t in range(1, 2 * 10**5 + 1): m.set('k', t, t)
assert m.get('k', 10**7) == 2 * 10**5 and m.get('k', 77777) == 77777 and m.get('k', 0) == ''
print("edge asserts ok (unknown key, before first, exact hit, 2*10^5 sets)")
```

**Output (my run):**
```
example: [None, 'high', 'high', None, '', 'high', 'low', '']
bisect_left version on the same example: [None, '', 'high', None, '', 'high', 'high', '']
1000 random operation sequences: bisect_right version == naive
edge asserts ok (unknown key, before first, exact hit, 2*10^5 sets)
```

**Edge cases:**
- Unknown key: ''.
- Query before the first timestamp: ''.
- Query exactly equal to a stored timestamp: that value.
- Query far after the last timestamp: the last value.
- 2*10^5 sets on one key, then queries: still O(log m) each.

**Follow-ups:**
- "What if timestamps could arrive out of order?" Use `bisect.insort` on the timestamp list (O(m) shift) or a balanced tree; the append-only trick no longer holds.
- "Delete old data?" Binary search for the cutoff and slice, or keep a deque if only the oldest entries go.
- "Why two parallel lists?" `bisect` needs a plain sorted list of keys; a list of tuples works too with a `key=` argument (Python 3.10+) but the parallel lists are simpler and faster.

**Common mistakes:**
- `bisect_left`, which fails exactly on equal timestamps.
- Forgetting the `i == 0` case, so `vs[-1]` silently returns the LAST value.
- Returning `None` instead of '' for a miss.
- Re-sorting on every `set`.

### Q7 ⭐⭐⭐ 🟡 Sliding-window-log rate limiter with an injected clock. Implement class `SlidingWindowLimiter(clock, limit, window)` with `allow(user)` returning True when the request is accepted. A request at time t is accepted when fewer than `limit` ACCEPTED requests of the same user have a timestamp in the half-open window (t - window, t], that is timestamp > t - window and timestamp <= t; so a request made exactly `window` seconds ago has already expired. Rejected requests are not recorded and do not count. Keep one deque of accepted timestamps per user and pop expired timestamps from the left; each request is O(1) amortised and memory is O(limit) per user. 1 <= limit <= 100, 1 <= window <= 3600. State what the boundary rule means with limit 2, window 10: accepted at t = 0 and t = 5, rejected at t = 9, accepted again at t = 10. Say, as a stated concept only, that several worker threads sharing the limiter would need a lock (or one limiter per thread plus a shared store) because the check and the append must happen together. The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[2, 10], ops=[[0, 'allow', ['u']], [5, 'allow', ['u']], [9, 'allow', ['u']], [10, 'allow', ['u']], [10, 'allow', ['v']], [15, 'allow', ['u']], [16, 'allow', ['u']]] -> [True, True, False, True, True, True, False].
**Asked at:** Rate-limiter guides (techinterview.org 'Implement a Rate Limiter' covering token bucket, leaky bucket, fixed and sliding window; a Redis rate-limiter interview post on oneuptime.com; search snippets only, not opened)

**Pattern:** Design problem, sliding-window log with an injected clock. Per user, a deque of accepted timestamps, expired from the left.

**Say this first (1 line):** "The window is the half-open (t - window, t]. I pop timestamps `<= t - window` from the left, then accept only if fewer than `limit` accepted timestamps remain. Rejected requests are not recorded."

**Brute force:**
- Keep one list of all accepted `(user, time)` pairs. On each request, count entries for that user with `t - window < time <= t`.
- O(accepted so far) per request; memory grows forever.

**Optimal:**
- `log[user]` is a deque of ACCEPTED timestamps, oldest first.
- `allow(user)`: `now = clock()`. While `q[0] <= now - window`, pop left. If `len(q) < limit`: append `now`, return True. Else return False and record nothing.
- Boundary rule, concretely: limit 2, window 10. Accepted at 0 and 5. At 9 the window is (-1, 9]: both count, 2 is not below 2, so rejected. At 10 the window is (0, 10]: the request at 0 is exactly 10 old, so it has expired. Only 5 counts, 1 < 2, accepted.
- Why only accepted requests are stored: rejected ones must not push the user further into the penalty. It also bounds memory by `limit`.
- Times are non-decreasing, so the deque is sorted and popping from the left is enough.
- Invariant: after expiry, the deque holds only accepted timestamps in (now - window, now], at most `limit` of them.

**Complexity:**
- `allow` is O(1) amortised: each timestamp is appended once and popped once.
- Memory O(limit) per user, O(users * limit) overall. (Idle users still hold a deque; a real system would also drop empty deques.)
- Tie rule: requests at the same second are separate entries; each is judged in call order.
- Thread safety (concept only): the check (`len < limit`) and the append must happen as one step. Otherwise two threads could both see `limit - 1` entries and both accept. One lock per user (or per limiter) around `allow` is the stated concept.

**Dry run:** `limit = 2, window = 10`.

| time | user | expired (<= t - 10) | count left | result |
|---|---|---|---|---|
| 0 | u | none | 0 | True, log [0] |
| 5 | u | none | 1 | True, log [0,5] |
| 9 | u | <= -1: none | 2 | False |
| 10 | u | <= 0: pop 0 | 1 | True, log [5,10] |
| 10 | v | n/a (new user) | 0 | True |
| 15 | u | <= 5: pop 5 | 1 | True, log [10,15] |
| 16 | u | <= 6: none | 2 | False |

**Code:**
```python
import random
from collections import deque

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class SlidingWindowLimiter:            # optimal: per-user deque of ACCEPTED timestamps
    def __init__(self, clock, limit, window):
        self.clock = clock; self.limit = limit; self.window = window; self.log = {}
    def allow(self, user):
        now = self.clock()
        q = self.log.setdefault(user, deque())
        while q and q[0] <= now - self.window:      # window is (now - window, now]: age == window is expired
            q.popleft()
        if len(q) < self.limit:
            q.append(now); return True              # only accepted requests are recorded
        return False

class NaiveLimiter:                    # brute force: one flat list of accepted (user, t), rescanned
    def __init__(self, clock, limit, window): self.clock = clock; self.limit = limit; self.window = window; self.acc = []
    def allow(self, user):
        now = self.clock()
        n = sum(1 for u, t in self.acc if u == user and now - self.window < t <= now)
        if n < self.limit: self.acc.append((user, now)); return True
        return False

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = [[0,'allow',['u']],[5,'allow',['u']],[9,'allow',['u']],[10,'allow',['u']],[10,'allow',['v']],[15,'allow',['u']],[16,'allow',['u']]]
want = [True, True, False, True, True, True, False]
assert run(SlidingWindowLimiter, [2, 10], ex) == want == run(NaiveLimiter, [2, 10], ex)
print("example:", run(SlidingWindowLimiter, [2, 10], ex))

random.seed(14)
for _ in range(1500):
    limit = random.randint(1, 4); window = random.randint(1, 8); t = 0; ops = []
    for _ in range(random.randint(0, 50)):
        t += random.randint(0, 4); ops.append([t, 'allow', [random.choice('uvw')]])
    assert run(SlidingWindowLimiter, [limit, window], ops) == run(NaiveLimiter, [limit, window], ops), (limit, window, ops)
print("1500 random clocked sequences: deque limiter == naive")

# boundary and edge cases
def seq(limit, window, times, user='u'): return run(SlidingWindowLimiter, [limit, window], [[t, 'allow', [user]] for t in times])
assert seq(2, 10, [0, 5, 9, 10]) == [True, True, False, True]       # age exactly 10 has expired
assert seq(1, 3, [0, 2, 3]) == [True, False, True]                  # window 3: t=3 sees (0,3], t=0 is out
assert seq(2, 5, [7, 7, 7, 7]) == [True, True, False, False]        # same second
assert seq(1, 5, [0, 1, 2, 3, 4, 5]) == [True, False, False, False, False, True]   # rejected calls are NOT recorded
assert run(SlidingWindowLimiter, [1, 1], []) == []                  # no calls
q = SlidingWindowLimiter(Clock(), 100, 3600)
for i in range(10**5): q.clock.t = i // 10; q.allow('u')
assert len(q.log['u']) <= 100                                       # memory O(limit)
print("edge asserts ok (boundary at age == window, same second, rejected not recorded, memory <= limit)")
```

**Output (my run):**
```
example: [True, True, False, True, True, True, False]
1500 random clocked sequences: deque limiter == naive
edge asserts ok (boundary at age == window, same second, rejected not recorded, memory <= limit)
```

**Edge cases:**
- A request exactly `window` seconds old is expired (checked with limit 2, window 10 and with limit 1, window 3).
- Many requests in one second: the first `limit` pass, the rest fail.
- Rejected requests do not extend the penalty (checked: limit 1, window 5, requests at 0 to 5: only 0 and 5 pass).
- Different users are independent.
- No requests: nothing happens.

**Follow-ups:**
- "Memory for millions of users?" O(limit) each is large in total. A fixed-window counter uses O(1) per user but allows a 2x burst at window edges; a sliding-window counter blends two windows to approximate.
- "Distributed?" The log lives in a shared store and the check and append must be atomic there (a script or transaction). Concept only.
- "Compare with token bucket?" See Q8: the log is exact but stores timestamps; the bucket stores two numbers and allows bursts.

**Common mistakes:**
- Closed window `[t - window, t]`, which keeps age-`window` requests and rejects too early.
- Recording rejected requests.
- Using `len(q) <= limit`, which allows `limit + 1` requests.
- Reading `time.time()` instead of `clock()`, so tests cannot control time.
- Forgetting that a new user has no deque yet.

### Q8 ⭐⭐⭐ 🟡 Token bucket rate limiter with an injected clock. Implement class `TokenBucket(clock, capacity, rate)`: the bucket holds at most `capacity` tokens (integer, 1 <= capacity <= 10^6), starts FULL when it is created (the clock reads 0 then) and gains `rate` tokens per elapsed second (integer, 0 <= rate <= 10^6) without ever exceeding `capacity`. `allow(cost=1)` first refills for the time since the previous call (the previous call time is updated on EVERY call, accepted or rejected), then returns True and removes `cost` tokens when at least `cost` tokens are available, otherwise returns False and removes nothing. Refill lazily inside `allow`: store `tokens` and `last`, no background timer. Because times and tokens are integers the arithmetic is exact; say why a float rate would make boundary tests fragile (use integers or Fraction). Explain how it differs from a sliding window (it allows a burst of `capacity` and then a steady `rate`). A call with cost greater than `capacity` can never succeed. The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[3, 1], ops=[[0, 'allow', []], [0, 'allow', []], [0, 'allow', []], [0, 'allow', []], [1, 'allow', []], [1, 'allow', []], [10, 'allow', [3]], [10, 'allow', [1]], [11, 'allow', [2]]] -> [True, True, True, False, True, False, True, False, False].
**Asked at:** Rate-limiter guides (techinterview.org 'Implement a Rate Limiter' covering token bucket, leaky bucket, fixed and sliding window; a Redis rate-limiter interview post on oneuptime.com; search snippets only, not opened)

**Pattern:** Design problem, token bucket with lazy refill and an injected clock. Two numbers (`tokens`, `last`), no timer thread.

**Say this first (1 line):** "On every call I first add `elapsed * rate` tokens, capped at `capacity`, and set `last = now`. Then I take `cost` tokens if there are enough, else I reject and take nothing."

**Brute force:**
- Simulate the refill one second at a time: loop from `last` to `now`, add `rate` each step, cap at `capacity`.
- O(elapsed seconds) per call. A call after a gap of 10^9 seconds loops 10^9 times. It is the oracle in the code.

**Optimal:**
- State: `tokens` (starts at `capacity`, bucket is full), `last` (the clock at creation).
- `allow(cost=1)`: `now = clock()`; `tokens = min(capacity, tokens + (now - last) * rate)`; `last = now`; if `cost <= tokens`: `tokens -= cost`, return True; else return False.
- `last` is updated on EVERY call, accepted or rejected. If you updated it only on success, the same elapsed time would be refilled again on the next call and you would hand out extra tokens.
- A rejected call removes nothing.
- A cost above `capacity` can never succeed, because `tokens <= capacity` always.
- Integers make the arithmetic exact. With a float rate, `0.1 * 10` style sums land at 0.9999999999999999, so a request exactly at the boundary could flip between pass and fail. Use integers (as here) or `Fraction`.
- Versus a sliding window: the bucket allows a burst of up to `capacity` at once and then a steady `rate` per second. A sliding window caps every window equally and has no burst credit.
- Invariant: `0 <= tokens <= capacity` after every call.

**Complexity:**
- `allow` is O(1) time, O(1) space.
- Rule: no tie-breaking; calls are judged in order.
- Thread safety (concept only): refill, compare and subtract must be one critical section, or two threads can both spend the same tokens.

**Dry run:** `capacity = 3, rate = 1`, starts full (3 tokens, last = 0).

| time | cost | tokens before (after refill) | result | tokens after |
|---|---|---|---|---|
| 0 | 1 | 3 | True | 2 |
| 0 | 1 | 2 | True | 1 |
| 0 | 1 | 1 | True | 0 |
| 0 | 1 | 0 | False | 0 |
| 1 | 1 | 0 + 1 = 1 | True | 0 |
| 1 | 1 | 0 | False | 0 |
| 10 | 3 | 0 + 9 = 9, capped at 3 | True | 0 |
| 10 | 1 | 0 | False | 0 |
| 11 | 2 | 0 + 1 = 1 | False | 1 |

**Code:**
```python
import random
from fractions import Fraction

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class TokenBucket:                     # optimal: lazy refill, integer arithmetic
    def __init__(self, clock, capacity, rate):
        self.clock = clock; self.cap = capacity; self.rate = rate
        self.tokens = capacity; self.last = clock()          # starts full; clock reads 0 here
    def allow(self, cost=1):
        now = self.clock()
        self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate)   # refill for elapsed time
        self.last = now                                      # updated on EVERY call, accepted or not
        if cost <= self.tokens:
            self.tokens -= cost; return True
        return False                                         # a rejection removes nothing

class NaiveBucket:                     # brute force: simulate one second at a time
    def __init__(self, clock, capacity, rate):
        self.clock = clock; self.cap = capacity; self.rate = rate; self.tokens = capacity; self.last = clock()
    def allow(self, cost=1):
        now = self.clock()
        while self.last < now:
            self.tokens = min(self.cap, self.tokens + self.rate); self.last += 1
        if cost <= self.tokens: self.tokens -= cost; return True
        return False

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = [[0,'allow',[]],[0,'allow',[]],[0,'allow',[]],[0,'allow',[]],[1,'allow',[]],[1,'allow',[]],[10,'allow',[3]],[10,'allow',[1]],[11,'allow',[2]]]
want = [True, True, True, False, True, False, True, False, False]
assert run(TokenBucket, [3, 1], ex) == want == run(NaiveBucket, [3, 1], ex)
print("example:", run(TokenBucket, [3, 1], ex))

random.seed(14)
for _ in range(1500):
    cap = random.randint(1, 6); rate = random.randint(0, 3); t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 5); ops.append([t, 'allow', random.choice([[], [], [random.randint(1, 8)]])])
    assert run(TokenBucket, [cap, rate], ops) == run(NaiveBucket, [cap, rate], ops), (cap, rate, ops)
print("1500 random clocked sequences: lazy-refill bucket == one-second-at-a-time naive")

# edge cases
assert run(TokenBucket, [3, 0], [[0,'allow',[3]],[100,'allow',[]]]) == [True, False]     # rate 0: never refills
assert run(TokenBucket, [5, 1], [[0,'allow',[6]],[50,'allow',[6]]]) == [False, False]    # cost > capacity never succeeds
assert run(TokenBucket, [5, 2], [[0,'allow',[5]],[1,'allow',[3]],[1,'allow',[2]]]) == [True, False, True]  # 2 tokens at t=1: cost 3 fails, cost 2 passes
# rejection still moves `last`: refilling must not be counted twice
assert run(TokenBucket, [2, 1], [[0,'allow',[2]],[1,'allow',[2]],[2,'allow',[2]]]) == [True, False, True]
b = TokenBucket(Clock(), 10**6, 10**6); b.clock.t = 10**9
assert b.allow(10**6) and b.tokens == 0                    # huge elapsed time is capped at capacity
# why floats are fragile: ten 0.1-second ticks do not add up to one second
f = 0.0
for _ in range(10): f += 0.1
print("ten additions of 0.1 equal 1.0?", f == 1.0, "; Fraction version:", sum([Fraction(1, 10)] * 10) == 1)
print("edge asserts ok (rate 0, cost > capacity, rejection updates last, capacity cap, 10^6 values)")
```

**Output (my run):**
```
example: [True, True, True, False, True, False, True, False, False]
1500 random clocked sequences: lazy-refill bucket == one-second-at-a-time naive
ten additions of 0.1 equal 1.0? False ; Fraction version: True
edge asserts ok (rate 0, cost > capacity, rejection updates last, capacity cap, 10^6 values)
```

**Edge cases:**
- `rate = 0`: never refills (checked).
- `cost > capacity`: always False (checked).
- Rejection still updates `last` (checked: capacity 2, rate 1, costs 2, 2, 2 at times 0, 1, 2 gives True, False, True).
- A huge elapsed gap is capped at `capacity`.
- Same-second calls: elapsed is 0, no refill.

**Follow-ups:**
- "Leaky bucket?" Same two numbers, but it drains at a constant rate and smooths output instead of allowing bursts.
- "Fractional rates?" Store tokens in micro-units, or use `Fraction`, so nothing is rounded.
- "Distributed?" Keep `(tokens, last)` in a shared store and update it atomically. Concept only.

**Common mistakes:**
- Not capping tokens at `capacity`.
- Updating `last` only on success (double refill).
- Subtracting tokens on a rejected call.
- Starting empty instead of full.
- Float arithmetic at boundaries.

### Q9 ⭐⭐⭐ 🟡 Flatten a nested list with an iterator. Implement class `NestedIterator(nested)` where `nested` is a list whose items are integers or (recursively) lists of the same kind; `next()` returns the next integer in left-to-right order and `hasNext()` says whether one remains. Empty lists, lists of empty lists and nesting such as [[], [[]], 3] must be skipped correctly: `hasNext()` must be right even before the first `next()`, so you must advance to the next integer eagerly (in the constructor and after every `next`), not lazily inside `next`. Use a stack of Python iterators (one per open list) instead of recursion or of flattening everything up front: memory O(depth), and a nesting depth of 5000 must not hit CPython's recursion limit of 1000 (a recursive flatten would). The checker never calls `next()` when `hasNext()` is False. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). Here `init` is a one-element list holding the nested list. BST iterator practice is Part 7 Q30. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[[1, 1], 2, [1, 1]]], ops=[['hasNext', []], ['next', []], ['next', []], ['next', []], ['hasNext', []], ['next', []], ['next', []], ['hasNext', []]] -> [True, 1, 1, 2, True, 1, 1, False]; init=[[[], [[]], 3, [[], []]]], ops=[['hasNext', []], ['next', []], ['hasNext', []]] -> [True, 3, False].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Iterator design with an explicit stack (iterative DFS). One Python iterator per open list, advance eagerly.

**Say this first (1 line):** "A stack of iterators, one per open list. After the constructor and after every `next`, I advance until I hold the next integer or the stack is empty, so `hasNext` is just 'do I hold one'."

**Brute force:**
- Recursively flatten the whole structure into a list in the constructor, then index through it.
- Simple, but O(total elements) extra memory up front, and recursion fails on deep nesting: a depth of 5000 exceeds CPython's recursion limit of 1000 (my run shows the recursive version raising `RecursionError`).

**Optimal:**
- `stack = [iter(nested)]` and `ready = None` (or a one-element tuple holding the next integer).
- `_advance()`: loop while the stack is not empty. Take `next(stack[-1])`. On `StopIteration` pop and continue (back to the parent list). If the item is an int, store it in `ready` and stop. Otherwise it is a list: push `iter(item)` and continue.
- `next()`: save `ready`, call `_advance()`, return the saved value.
- `hasNext()`: `ready is not None`.
- Why eager: `[[], [[]], 3]` starts with empty lists. `hasNext()` before the first `next()` must already know that 3 exists, so the advance has to happen in the constructor, not lazily inside `next`.
- The 1-tuple matters: store `(x,)` so that the integer 0 (falsy) is not mistaken for "nothing ready".
- Invariant: `ready` is the next integer in left-to-right order, or None exactly when everything is consumed.

**Complexity:**
- Each element of the structure is visited once, so total work over all calls is O(total ints + total lists).
- A single `next` can be longer (skipping many empty lists) but the total is linear: amortised O(1) per integer.
- Memory O(depth) for the stack, not O(total).
- Eviction/tie rules: none, order is fixed left to right.
- Thread safety (concept only): an iterator is stateful, so two threads calling `next` on one iterator would need a lock around `hasNext`/`next`, or each thread gets its own iterator.

**Dry run:** `[[1, 1], 2, [1, 1]]`.

| step | stack (open lists) | ready |
|---|---|---|
| constructor: next(outer) is a list, push; next is 1 | outer, [1,1] | 1 |
| hasNext | | True |
| next() returns 1, advance: gets 1 | outer, [1,1] | 1 |
| next() returns 1, advance: inner exhausted, pop; outer gives 2 | outer | 2 |
| next() returns 2, advance: outer gives list, push; gets 1 | outer, [1,1] | 1 |
| next() returns 1, advance: gets 1 | same | 1 |
| next() returns 1, advance: inner done, outer done, empty | empty | None |
| hasNext | | False |

**Code:**
```python
import random

class NestedIterator:                  # optimal: stack of Python iterators, eager advance
    def __init__(self, nested):
        self.stack = [iter(nested)]; self.ready = None   # ready: None or a 1-tuple holding the next int
        self._advance()
    def _advance(self):
        self.ready = None
        while self.stack:
            try: x = next(self.stack[-1])
            except StopIteration:
                self.stack.pop(); continue               # this list is exhausted: go back to its parent
            if isinstance(x, int):
                self.ready = (x,); return                # found the next integer
            self.stack.append(iter(x))                   # a sub-list: descend into it
    def next(self):
        v = self.ready[0]; self._advance(); return v     # advance NOW so hasNext is always right
    def hasNext(self): return self.ready is not None

class NaiveNested:                     # brute force: recursive flatten up front (fails on depth 5000)
    def __init__(self, nested):
        self.flat = []
        def go(x):
            for y in x:
                if isinstance(y, int): self.flat.append(y)
                else: go(y)
        go(nested); self.i = 0
    def next(self): self.i += 1; return self.flat[self.i - 1]
    def hasNext(self): return self.i < len(self.flat)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([[[1,1],2,[1,1]]], [['hasNext',[]],['next',[]],['next',[]],['next',[]],['hasNext',[]],['next',[]],['next',[]],['hasNext',[]]],
      [True,1,1,2,True,1,1,False])
e2 = ([[[],[[]],3,[[],[]]]], [['hasNext',[]],['next',[]],['hasNext',[]]], [True,3,False])
for init, ops, want in (e1, e2):
    assert run(NestedIterator, init, ops) == want == run(NaiveNested, init, ops)
print("examples:", run(NestedIterator, *e1[:2]), run(NestedIterator, *e2[:2]))

random.seed(14)
def mk(d): return [random.randint(-5, 9) if d == 0 or random.random() < .6 else mk(d - 1) for _ in range(random.randint(0, 4))]
def count(x): return sum(1 if isinstance(y, int) else count(y) for y in x)
for _ in range(1500):
    nested = mk(4); left = count(nested); ops = [['hasNext', []]]
    for _ in range(random.randint(0, 14)):
        if left and random.random() < .6: ops.append(['next', []]); left -= 1    # never next() when empty
        else: ops.append(['hasNext', []])
    assert run(NestedIterator, [nested], ops) == run(NaiveNested, [nested], ops), (nested, ops)
print("1500 random nested lists with random hasNext/next sequences: iterator == naive")

# edge cases
assert run(NestedIterator, [[]], [['hasNext', []]]) == [False]                    # empty list
assert run(NestedIterator, [[[], [[]], [[], []]]], [['hasNext', []]]) == [False]  # only empty lists
assert run(NestedIterator, [[[[[7]]]]], [['hasNext',[]],['next',[]],['hasNext',[]]]) == [True, 7, False]
it = NestedIterator([0, [], -3]); assert [it.next(), it.hasNext(), it.next(), it.hasNext()] == [0, True, -3, False]  # 0 is a value
deep = 7
for _ in range(5000): deep = [deep]                      # nesting depth 5000
it = NestedIterator(deep); assert it.hasNext() and it.next() == 7 and not it.hasNext()
try: NaiveNested(deep); recursive_ok = True
except RecursionError: recursive_ok = False
print("depth 5000: iterator ok; recursive flatten survived?", recursive_ok)
big = [[i, [i + 1]] for i in range(0, 2 * 10**5, 2)]
it = NestedIterator(big); out = []
while it.hasNext(): out.append(it.next())
assert out == list(range(2 * 10**5))
print("edge asserts ok (empty, only-empty lists, value 0, depth 5000, 2*10^5 ints)")
```

**Output (my run):**
```
examples: [True, 1, 1, 2, True, 1, 1, False] [True, 3, False]
1500 random nested lists with random hasNext/next sequences: iterator == naive
depth 5000: iterator ok; recursive flatten survived? False
edge asserts ok (empty, only-empty lists, value 0, depth 5000, 2*10^5 ints)
```

**Edge cases:**
- Empty list, only empty lists (`[[], [[]]]`): `hasNext()` is False from the start.
- The value 0 or a negative number is a real element.
- Depth 5000: fine with the iterator stack, `RecursionError` with a recursive flatten.
- 2*10^5 integers: linear.
- The checker never calls `next()` when `hasNext()` is False, so no error handling is needed.
- Harness note: deep-copying a depth-5000 list (as a test harness that copies its inputs would) itself raises `RecursionError` in CPython; the iterator is fine when called directly, as in my test.

**Follow-ups:**
- "Peeking?" `ready` already is the peek: return it without advancing.
- "Lists of lists lazily from a generator?" The same stack works, since it only calls `next` on iterators.
- "Why not `chain.from_iterable`?" It flattens exactly one level.

**Common mistakes:**
- Advancing lazily in `next`, so `hasNext` is wrong on inputs starting with empty lists.
- Using truthiness (`if ready`), which treats 0 as empty.
- Recursing, which breaks at depth about 1000.
- Flattening everything up front when the interviewer asks for O(depth) memory.

### Q10 ⭐⭐⭐ 🟡 Fenwick tree (BIT): point update and range sum. Implement class `NumArray(nums)` (1 <= len <= 10^5, |value| <= 10^9) with `update(i, val)` (SET nums[i] = val, returns None) and `sumRange(l, r)` (the sum of nums[l..r], both ends included). Keep a Fenwick array `t` of size n + 1 (1-based): `t[i]` stores the sum of the block of length `i & -i` ending at index i. `update` adds the DELTA (new value minus the old value you keep in a separate list) with `while i <= n: t[i] += d; i += i & -i`; a prefix sum uses `while i > 0: s += t[i]; i -= i & -i`; `sumRange(l, r)` = prefix(r + 1) - prefix(l). Both O(log n); the build can be O(n) by pushing each t[i] to its parent i + (i & -i). Explain why the lowest set bit `i & -i` defines the block, why index 0 cannot be used, and why the common bug 'add val instead of val - old' double counts. Compare with the static prefix array of Part 13 Q1 (O(1) query, O(n) update) and with a segment tree (Q23). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[1, 3, 5]], ops=[['sumRange', [0, 2]], ['update', [1, 2]], ['sumRange', [0, 2]], ['sumRange', [2, 2]]] -> [9, null, 8, 5]; init=[[-4, 7]], ops=[['sumRange', [0, 1]], ['update', [0, 10]], ['sumRange', [0, 0]], ['sumRange', [0, 1]]] -> [3, null, 10, 17].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Fenwick tree (binary indexed tree). Point update and prefix sum in O(log n), using the lowest set bit to define blocks.

**Say this first (1 line):** "`t[i]` stores the sum of a block of length `i & -i` ending at index i, so update climbs with `i += i & -i`, prefix sum descends with `i -= i & -i`, and a range sum is a difference of two prefixes."

**Brute force:**
- Plain list: update is O(1), `sum(a[l:r+1])` is O(n) per query.
- Or a prefix array (Part 13 Q1): query O(1) but each update rebuilds up to O(n).

**Optimal:**
- Array `t` of size n + 1, 1-based. Index 0 is unusable: `0 & -0 == 0`, so `i += i & -i` would never move and the loop would spin forever.
- Block rule: `t[i]` = sum of `nums` over the `i & -i` positions ending at i (1-based). Example: `t[6]` has lowest bit 2, so it covers positions 5 and 6; `t[8]` covers 1 to 8. The output checks this for every i.
- `update(i, val)`: `d = val - old` (keep `old` in a separate list), then `i += 1` and `while i <= n: t[i] += d; i += i & -i`. The index jumps to the next block that contains i.
- Why delta and not `val`: the tree stores sums, which already include the old value. Adding `val` counts old and new together. Output shows the bug turning 8 into 11 on example 1.
- `prefix(i)` (sum of the first i items): `while i > 0: s += t[i]; i -= i & -i`. Stripping the lowest bit hops to the end of the previous block.
- `sumRange(l, r) = prefix(r + 1) - prefix(l)`.
- O(n) build: set `t[i] = nums[i-1]`, then push each `t[i]` into its parent `j = i + (i & -i)` if `j <= n`. Going in increasing i guarantees `t[i]` is complete before it is pushed.
- Invariant: each `t[i]` equals the sum of its block of the CURRENT array.
- Versus a segment tree (Q23): the Fenwick tree is shorter and lighter, but only for invertible operations like sum; min with set-to-larger needs the segment tree.

**Complexity:**
- `update`, `sumRange`: O(log n) each (at most log2(n) bits to climb or strip).
- Build O(n), space O(n).
- Rule: `update` SETS the value (delta against the stored copy), it does not add.
- Thread safety (concept only): an update touches up to log n cells, so a concurrent query could see a half-applied delta. A lock around both operations, or a read-write lock, is the stated concept.

**Dry run:** `nums = [1, 3, 5]`, n = 3. Build: `t[1]=1`, `t[2]=1+3=4` (block 1..2), `t[3]=5`.

| call | work | result |
|---|---|---|
| sumRange(0,2) | prefix(3) = t[3]+t[2] = 5+4 = 9, prefix(0) = 0 | 9 |
| update(1,2) | d = 2-3 = -1; i = 2: t[2]=3; i = 4 > 3 stop | None |
| sumRange(0,2) | prefix(3) = 5 + 3 = 8 | 8 |
| sumRange(2,2) | prefix(3) - prefix(2) = 8 - 3 | 5 |

**Code:**
```python
import random

class NumArray:                        # optimal: Fenwick tree (1-based) + a copy of the values
    def __init__(self, nums):
        n = self.n = len(nums); self.a = list(nums); self.t = [0] * (n + 1)
        for i in range(1, n + 1):                     # O(n) build: push each node into its parent
            self.t[i] += nums[i - 1]
            j = i + (i & -i)
            if j <= n: self.t[j] += self.t[i]
    def update(self, i, val):
        d = val - self.a[i]; self.a[i] = val          # DELTA, not val
        i += 1                                        # shift to 1-based
        while i <= self.n:
            self.t[i] += d; i += i & -i               # climb to the next block that covers i
    def _prefix(self, i):                             # sum of nums[0 .. i-1]
        s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i               # strip the lowest set bit
        return s
    def sumRange(self, l, r): return self._prefix(r + 1) - self._prefix(l)

class NaiveArray:                      # brute force: plain list, O(n) query
    def __init__(self, nums): self.a = list(nums)
    def update(self, i, val): self.a[i] = val
    def sumRange(self, l, r): return sum(self.a[l:r + 1])

class WrongArray(NumArray):            # the classic bug: adds val instead of val - old
    def update(self, i, val):
        self.a[i] = val; i += 1
        while i <= self.n: self.t[i] += val; i += i & -i

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([[1,3,5]], [['sumRange',[0,2]],['update',[1,2]],['sumRange',[0,2]],['sumRange',[2,2]]], [9,None,8,5])
e2 = ([[-4,7]], [['sumRange',[0,1]],['update',[0,10]],['sumRange',[0,0]],['sumRange',[0,1]]], [3,None,10,17])
for init, ops, want in (e1, e2):
    assert run(NumArray, init, ops) == want == run(NaiveArray, init, ops)
print("examples:", run(NumArray, *e1[:2]), run(NumArray, *e2[:2]))
print("'add val' bug on example 1:", run(WrongArray, *e1[:2]), "(wanted [9, None, 8, 5])")
assert run(WrongArray, *e1[:2]) != e1[2]

random.seed(14)
for _ in range(1500):
    n = random.randint(1, 12); nums = [random.randint(-9, 9) for _ in range(n)]; ops = []
    for _ in range(random.randint(0, 40)):
        if random.random() < .5: ops.append(['update', [random.randrange(n), random.randint(-9, 9)]])
        else:
            l = random.randrange(n); ops.append(['sumRange', [l, random.randrange(l, n)]])
    assert run(NumArray, [nums], ops) == run(NaiveArray, [nums], ops), (nums, ops)
print("1500 random operation sequences: Fenwick == naive")

# the block rule: t[i] covers length i & -i ending at i, checked against direct sums
nums = [random.randint(-50, 50) for _ in range(37)]; f = NumArray(nums)
for i in range(1, 38): assert f.t[i] == sum(nums[i - (i & -i):i])
print("t[i] == sum of the block of length i & -i ending at i, for every i in 1..37")

# edge cases
assert run(NumArray, [[5]], [['sumRange',[0,0]],['update',[0,-5]],['sumRange',[0,0]]]) == [5, None, -5]   # n = 1
f = NumArray([0] * 8); f.update(7, 3); assert f.sumRange(0, 7) == 3 and f.sumRange(0, 6) == 0              # last index
n = 10**5; f = NumArray([10**9] * n); assert f.sumRange(0, n - 1) == 10**9 * n                           # big sums
f.update(0, -10**9); assert f.sumRange(0, n - 1) == 10**9 * (n - 2) and f.sumRange(0, 0) == -10**9
print("edge asserts ok (n=1, last index, 10^5 values of 10^9, negative set)")
```

**Output (my run):**
```
examples: [9, None, 8, 5] [3, None, 10, 17]
'add val' bug on example 1: [9, None, 11, 5] (wanted [9, None, 8, 5])
1500 random operation sequences: Fenwick == naive
t[i] == sum of the block of length i & -i ending at i, for every i in 1..37
edge asserts ok (n=1, last index, 10^5 values of 10^9, negative set)
```

**Edge cases:**
- n = 1.
- Updating the last index: the climb ends immediately.
- Negative values and a set to a negative number (delta handles it).
- Large sums: 10^5 values of 10^9 sum to 10^14, no overflow in Python.
- `l == r`: `prefix(l+1) - prefix(l)`.

**Follow-ups:**
- "Why does `i & -i` work?" Two's complement flips bits above the lowest set bit, so the AND isolates that bit.
- "Range add, range sum?" Two Fenwick trees, or a lazy segment tree.
- "Range minimum?" Fenwick does not give it with arbitrary sets (a prefix minimum cannot be undone), so use a segment tree.

**Common mistakes:**
- Adding `val` instead of `val - old`.
- Using index 0 (infinite loop).
- Forgetting the +1 shift between 0-based input and 1-based tree.
- `sumRange(l, r)` as `prefix(r) - prefix(l)`, an off-by-one that drops `nums[r]`.
- Starting the O(n) build push from the wrong order.
