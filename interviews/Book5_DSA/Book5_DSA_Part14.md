# Book 5 — Part 14: Extra II (Design Problems, Advanced Graphs, Segment and Fenwick Trees, Mixed Mock Sets)

**Topic:** Python DSA for product-company interviews, the 'Extra II' part and the LAST part of Book 5: design problems with exact API and tie rules (LRU cache with OrderedDict and with a hand-built doubly linked list, LFU cache in O(1), rate limiters (fixed window, sliding window log, token bucket) and the logger and hit counter, all with an injected clock; iterator design (nested list, peeking, zigzag), time-based key-value store with bisect, snapshot array, news feed with heaps, the all-O(1) data structure), advanced graphs (strongly connected components with Kosaraju and with Tarjan, bridges and articulation points, Hierholzer's Eulerian path for the itinerary problem, lexicographically smallest topological order, parallel courses with durations, shortest path with a coupon, maximum bipartite matching), segment trees and Fenwick (BIT) trees (point update and range query, range minimum, lazy propagation for range add and range sum, sparse table, coordinate compression, inversions and smaller-after-self with a BIT, a 2D BIT), and four timed company-style mock sets that integrate Parts 1 to 14.

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 13, ⭐⭐ 24, ⭐ 13)  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Split:** 32 standalone questions and 18 mock-set questions (Set A has 5; Set B has 5; Set C has 4; Set D has 4). The set questions are real problems of their own (not repeats of the standalone ones) and are listed by star rating like every other question, so a set is scattered through the file; to run a set as a mock, collect its tag. Where the sets sit in this file: Set A: Q2, Q26, Q27, Q12, Q47; Set B: Q3, Q28, Q29, Q35, Q48; Set C: Q30, Q49, Q36, Q50; Set D: Q11, Q31, Q13, Q37.

How the sets work: there are 4 sets (A and B with 5 questions, C and D with 4), each 45 minutes and 100 points. Each set question is tagged `[Set A, Q1 of 5, 5 min, 10 pts]`. Inside a set the questions run from warm-up to hardest and the points never decrease: sets of 5 use 10, 15, 20, 25 and 30 points, sets of 4 use 15, 25, 30 and 30 points; the minutes add up to 45. Suggested scoring per question: 30 percent for stating the rules, tie-breaks and boundaries out loud before coding (inclusive or exclusive windows, tie rules, what an empty input returns), 30 percent for a correct solution that passes the example and a random operation-sequence or brute-force check, 20 percent for the stated complexity and the reason it holds, 10 percent for the edge cases the prompt seeds, 10 percent for a crisp spoken summary in under 60 seconds. Bands per set: 85 to 100 strong, 70 to 84 solid with gaps, 50 to 69 review the linked parts, below 50 redo the linked earlier parts first. Time budgets and bands are practice targets set by this book, not any company's published rules.

| Set | What it covers | Questions | Time | Points | Earlier questions it builds on |
|---|---|---|---|---|---|
| A | Backend design round: streams, trips, scores, expiring caches and delayed jobs | 5 | 45 min | 100 | Part 1 Q39, Part 2 Q3, Part 4 Q22, Part 8 Q1, Part 8 Q4, Part 8 Q29, Part 8 Q31; this part: Q5 |
| B | Graph round: union-find, Kruskal with pre-built edges, directed tree repair and strongly connected components | 5 | 45 min | 100 | Part 9 Q3, Part 9 Q13, Part 9 Q14, Part 9 Q29, Part 9 Q43; this part: Q20 |
| C | Range-query round: positions with bisect, Fenwick order statistics, reverse pairs and a lazy segment tree | 4 | 45 min | 100 | Part 5 Q4, Part 5 Q11, Part 8 Q7, Part 8 Q17, Part 13 Q4, Part 13 Q17, Part 13 Q47; this part: Q10, Q17, Q25, Q44 |
| D | Online-assessment mix: heaps with lazy deletion, bisect, frequency stacks and an event sweep | 4 | 45 min | 100 | Part 1 Q10, Part 4 Q2, Part 4 Q38, Part 5 Q11, Part 8 Q5, Part 8 Q7, Part 8 Q31, Part 8 Q38 |

Scope note: this part owns design problems with an API, advanced graph algorithms, segment and Fenwick trees and the mixed mock sets. It does not repeat: the min stack ('Part 4 Q2') and max stack ('Part 4 Q38'), the randomised set ('Part 1 Q35'), the BST iterator ('Part 7 Q30'), the linked-list pieces of an LRU cache ('Part 6 Q29' and 'Part 6 Q30'; Q5 here builds the full class), minimum spanning trees ('Part 9 Q29' Kruskal and 'Part 9 Q37' Prim; Set B reuses Kruskal with pre-built edges), basic bipartite colouring ('Part 9 Q21'; Q43 is the matching variant), the Eulerian existence test ('Part 9 Q36'; Q34 constructs the trail), unit-time parallel courses ('Part 9 Q24'; Q39 adds durations), cheapest flights with at most k stops ('Part 9 Q34'; Q22 is a different constraint), the merge-sort inversion count and range-sum counting ('Part 13 Q17' and 'Part 13 Q47'; Q25, Q46 and Q36 use a Fenwick tree) and the row-prefix 2D point-update version ('Part 13 Q40'; Q45 is the Fenwick answer it promises). Every 'Part N Qn' reference in this file was checked by script against the headings of Book5_DSA_Part01 to Part13.

API-shaped questions: every design prompt names the class, the methods and their signatures and states the exact call format used in its examples: the checker builds the object with `init` (the constructor arguments) and runs `ops`, a list of [method, [args]] calls, collecting one return value per call (None when a method returns nothing); an example is written `init=..., ops=... -> list of return values`. Time-dependent designs (Q7, Q8, Q14, Q1, Q16 and the set questions with a clock) take an INJECTED clock: the first constructor argument is a zero-argument callable returning integer seconds, the checker sets it before each call, ops are [time, method, [args]] with non-decreasing times, and every prompt states the window boundary exactly (half-open windows, expiry at the exact second, the second a message may print again). Tie and eviction rules are explicit (LRU and LFU eviction, the all-O(1) tie rule, the Twitter feed recency rule, the frequency-stack tie rule, the voting tie rule). Thread safety appears only as a stated concept (what a lock would have to cover), never as code. Every design answer must include an operation-sequence oracle: random operation sequences replayed against a simple reference implementation, with the two outputs compared.

Recursion and size notes: every graph question that walks deep paths (Q20, Q33, Q41, Q42, Q48 as the SCC step) requires an iterative implementation because a path of 10^5 nodes exceeds CPython's default recursion limit of 1000; the checker confirmed that a recursive flatten or DFS fails at depth 1500 and that the iterative references handle 10^5 nodes. Segment-tree recursion depth is about log2(n) (under 20) and the matching recursion depth is at most L <= 300, so recursion is fine there; the prompts say so. Examples in every prompt are rendered from the same data the checker runs.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for en.wikipedia.org), so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part14_sources.md). Searches returned design-problem lists (a LeetCode Discuss post, talentd.in, walkccc, designgurus), rate-limiter and LRU guides (techinterview.org, InterviewBit, a Redis rate-limiter post), segment-tree, Fenwick and sparse-table guides (techinterview.org, mintlify, cp-algorithms, designgurus) and advanced-graph guides (techinterview.org, algocademy, Naukri Code360). The searches did not cover the zigzag iterator, the skyline problem or a worked LFU solution, so those come from editor knowledge of standard lists. Nothing was found tying any single item to a named company, so 'Asked at' lines name source types only; the mock sets are editor designs in the style of timed rounds. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 Hit counter for the last 5 minutes. Implement class `HitCounter(clock)` with `hit()` (records one hit at the current time, returns None) and `getHits()` (returns the number of hits recorded at times t' with now - 300 < t' <= now, so a hit exactly 300 seconds old is NOT counted). Several hits can share one timestamp. Keep a deque of [timestamp, count] pairs and a running total so that, provided both `hit` and `getHits` drop expired buckets, memory is bounded by the 300 distinct seconds in the window, and say how the design changes when one second can see a million hits (buckets, which this design already uses) and when you need the last N minutes for large N (a circular array of 300 buckets keyed by second modulo 300, with the stale-bucket check). The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[], ops=[[1, 'hit', []], [2, 'hit', []], [3, 'hit', []], [4, 'getHits', []], [300, 'getHits', []], [301, 'getHits', []], [301, 'hit', []], [302, 'getHits', []], [310, 'getHits', []]] -> [null, null, null, 3, 3, 2, null, 2, 1].
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

### Q4 ⭐⭐⭐ 🟡 LRU cache with collections.OrderedDict. Implement class `LRUCache(capacity)` (1 <= capacity <= 3000) with `get(key)` and `put(key, value)`, both O(1) on average. `get` returns the value, or -1 when the key is absent, and a successful `get` makes the key the most recently used. `put` on a new key inserts it as most recently used; `put` on an existing key replaces the value and also makes it most recently used; after an insert that leaves more than `capacity` keys, evict the least recently used key (a failed `get` changes nothing). `put` returns None. Use `move_to_end` and `popitem(last=False)` and say why a plain dict (insertion order only) is a poor fit. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). The hand-built doubly linked list version is Q5 (the linked-list idea is Part 6 Q30; sentinel pointer practice is Part 6 Q29). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[2], ops=[['put', [1, 1]], ['put', [2, 2]], ['get', [1]], ['put', [3, 3]], ['get', [2]], ['put', [4, 4]], ['get', [1]], ['get', [3]], ['get', [4]]] -> [null, null, 1, null, -1, null, -1, 3, 4]; init=[1], ops=[['put', [5, 10]], ['put', [5, 20]], ['get', [5]], ['put', [6, 1]], ['get', [5]], ['get', [6]]] -> [null, null, 20, null, -1, 1].
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

### Q5 ⭐⭐⭐ 🟡 LRU cache from scratch: a doubly linked list with sentinels plus a dict. Implement class `LRUCache(capacity)` (1 <= capacity <= 3000) with `get(key)`, `put(key, value)`, `order()` and `size()`; do NOT use OrderedDict, and write the node class and the two helpers `_unlink(node)` and `_push_front(node)` yourself, with a dummy head and a dummy tail so no pointer move needs an `if node is None` case. Rules: `get` returns the value or -1 and makes a found key the most recently used; `put` inserts or updates a key as most recently used and, when an insert would exceed `capacity`, first evicts the least recently used key (store the key inside the node so the evicted node can be deleted from the dict). `order()` returns the keys from most recently used to least recently used, `size()` the number of stored keys; `put` returns None. State why each pointer assignment of an unlink (two) and of a push-front (four) matters, why a singly linked list cannot unlink in O(1), and say as a stated concept only (not code) what a lock around `get` and `put` would protect: both methods mutate the list, so even `get` is a write. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[3], ops=[['put', [1, 'a']], ['put', [2, 'b']], ['put', [3, 'c']], ['order', []], ['get', [1]], ['order', []], ['put', [4, 'd']], ['order', []], ['get', [2]], ['size', []]] -> [null, null, null, [3, 2, 1], 'a', [1, 3, 2], null, [4, 1, 3], -1, 3]; init=[1], ops=[['put', [1, 1]], ['put', [2, 2]], ['get', [1]], ['get', [2]], ['order', []]] -> [null, null, -1, 2, [2]].
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

### Q11 ⭐⭐⭐ 🟡 [Set D, Q1 of 4, 8 min, 15 pts] Stock price fluctuation. Implement class `StockPrice()` receiving a stream of (timestamp, price) records that can arrive out of order and can CORRECT an earlier record: `update(timestamp, price)` (returns None) sets the price for that timestamp, replacing any earlier price for the same timestamp. `current()` returns the price at the LATEST timestamp seen so far, `maximum()` and `minimum()` the highest and lowest price over all timestamps using each timestamp's latest price. They are only called after at least one update. Keep a dict timestamp -> price and two heaps of (price, timestamp) (negate for the max); on `maximum` and `minimum` discard heap tops whose price no longer equals the dict value (lazy deletion, Part 8 Q31; the changing-priority idea of Part 8 Q38). Amortised O(log n) per call; say why every pushed entry is discarded at most once. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[], ops=[['update', [1, 10]], ['update', [2, 5]], ['current', []], ['maximum', []], ['update', [1, 3]], ['maximum', []], ['update', [4, 2]], ['minimum', []], ['current', []], ['update', [4, 20]], ['maximum', []], ['minimum', []]] -> [null, null, 5, 10, null, 5, null, 2, 2, null, 20, 3].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Hash map plus two heaps with lazy deletion. The data changes (a correction replaces an old price), and a heap cannot delete from the middle. So I leave stale entries in the heap and throw them away only when they reach the top (Part 8 Q31; the changing-priority idea is Part 8 Q38).

**Say this first (1 line):** "A dict holds each timestamp's latest price; a min-heap and a max-heap hold every (price, timestamp) ever pushed, and I discard a top entry only when the dict says it is stale."

**Brute force:**
- Keep the dict. `current` = price at `max(dict)`, `maximum` = `max(dict.values())`, `minimum` = `min(dict.values())`.
- Every query rescans, so O(n) per call. With 10^5 queries on 10^5 records that is about 10^10 steps.

**Optimal:**
- `price`: timestamp -> latest price. `latest`: the largest timestamp seen (one integer, updated in `update`). `current()` is `price[latest]`, O(1).
- `update(ts, p)`: set `price[ts] = p`, push `(p, ts)` on the min-heap and `(-p, ts)` on the max-heap. O(log n).
- `maximum()`: look at the max-heap top. If `price[ts]` differs from that entry's price, the record was corrected after it was pushed, so pop it and look again. The first top that matches is the answer.
- `minimum()` is the same on the min-heap.
- Tie rule: equal prices on different timestamps give equal heap keys, and that is fine, because only the price is returned. If the same price is re-sent for a timestamp, two identical entries exist and both are valid; the later one is simply a duplicate.
- Invariant: for every timestamp, the entry holding its current price is in both heaps, so a matching top is always the true extreme.

**Complexity:**
- `update`: O(log n) (two pushes). `current`: O(1).
- `maximum` / `minimum`: O(log n) amortised. Every call does one comparison that succeeds, plus some pops.
- Why amortised: each entry is pushed once and popped at most once, and an entry is popped only when it is stale. Total pops <= total pushes = 2 * updates. So the pop work over any sequence of m calls is O(m log m) in total, which averages to O(log n) per call.
- Space: O(updates), not O(distinct timestamps), because stale entries wait in the heaps until they reach the top.

**Dry run:** the first example.

| call | dict (ts: price) | what happens | returns |
|---|---|---|---|
| update(1, 10) | {1:10} | latest = 1 | None |
| update(2, 5) | {1:10, 2:5} | latest = 2 | None |
| current() | | price[2] | 5 |
| maximum() | | max-heap top (-10, 1): price[1] = 10 matches | 10 |
| update(1, 3) | {1:3, 2:5} | push (3,1) and (-3,1); latest stays 2 | None |
| maximum() | | top (-10, 1) is stale (price[1] = 3): pop; next top (-5, 2) matches | 5 |
| update(4, 2) | {1:3, 2:5, 4:2} | latest = 4 | None |
| minimum() | | min-heap top (2, 4) matches | 2 |
| current() | | price[4] | 2 |
| update(4, 20) | {1:3, 2:5, 4:20} | corrects ts 4 | None |
| maximum() | | top (-20, 4) matches | 20 |
| minimum() | | top (2, 4) is stale: pop; next (3, 1) matches | 3 |

**Code:**
```python
import heapq, random

class NaiveStock:                       # brute force: rescan the dict every call
    def __init__(self): self.p = {}
    def update(self, timestamp, price): self.p[timestamp] = price
    def current(self): return self.p[max(self.p)]
    def maximum(self): return max(self.p.values())
    def minimum(self): return min(self.p.values())

class StockPrice:                       # optimal: dict + two heaps with lazy deletion
    def __init__(self):
        self.price = {}                 # timestamp -> latest price
        self.latest = -1                # largest timestamp seen
        self.lo = []                    # (price, ts)
        self.hi = []                    # (-price, ts)
        self.pushed = 0; self.popped = 0   # counters only for the amortised claim
    def update(self, timestamp, price):
        self.price[timestamp] = price
        if timestamp > self.latest: self.latest = timestamp
        heapq.heappush(self.lo, (price, timestamp))
        heapq.heappush(self.hi, (-price, timestamp))
        self.pushed += 2
    def current(self): return self.price[self.latest]
    def maximum(self):
        while self.price[self.hi[0][1]] != -self.hi[0][0]:   # stale: that ts now has another price
            heapq.heappop(self.hi); self.popped += 1
        return -self.hi[0][0]
    def minimum(self):
        while self.price[self.lo[0][1]] != self.lo[0][0]:
            heapq.heappop(self.lo); self.popped += 1
        return self.lo[0][0]

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[], ops=[['update', [1, 10]], ['update', [2, 5]], ['current', []], ['maximum', []], ['update', [1, 3]],
          ['maximum', []], ['update', [4, 2]], ['minimum', []], ['current', []], ['update', [4, 20]], ['maximum', []], ['minimum', []]])
want = [None, None, 5, 10, None, 5, None, 2, 2, None, 20, 3]
assert run(StockPrice, **ex) == want == run(NaiveStock, **ex)
print('example ->', run(StockPrice, **ex))

random.seed(11)
for case in range(500):
    ops = [['update', [random.randint(1, 8), random.randint(1, 6)]]]   # first call must be update
    for _ in range(random.randint(0, 40)):
        if random.random() < 0.5: ops.append(['update', [random.randint(1, 8), random.randint(1, 6)]])
        else: ops.append([random.choice(['current', 'maximum', 'minimum']), []])
    assert run(StockPrice, [], ops) == run(NaiveStock, [], ops), ops
print('500 random sequences match the naive reference')

# amortised claim: every entry is popped at most once, so pops <= pushes
s = StockPrice()
for i in range(20000):
    s.update(random.randint(1, 50), random.randint(1, 10**6))
    if i % 7 == 0: s.maximum(); s.minimum()
assert s.popped <= s.pushed
print('pushed', s.pushed, 'popped', s.popped, '(popped <= pushed)')

# edge cases
s = StockPrice(); s.update(5, 9)
assert (s.current(), s.maximum(), s.minimum()) == (9, 9, 9)
s.update(5, 4); assert (s.current(), s.maximum(), s.minimum()) == (4, 4, 4)   # correction of the only record
s.update(2, 4); assert s.current() == 4 and s.maximum() == 4                  # older timestamp, same price
s.update(5, 4); assert s.minimum() == 4                                        # same value re-sent: duplicate heap entry is fine
s.update(1, 100); assert s.current() == 4 and s.maximum() == 100               # late record does not change current
s.update(1, 1); assert s.maximum() == 4 and s.minimum() == 1
print('edge asserts ok')
```

**Output (my run):**
```
example -> [None, None, 5, 10, None, 5, None, 2, 2, None, 20, 3]
500 random sequences match the naive reference
pushed 40000 popped 5425 (popped <= pushed)
edge asserts ok
```

**Edge cases:**
- One record: all three queries return that price.
- Correcting the only record (or the current latest timestamp): `current` follows the new price.
- A late (older) timestamp never changes `current`, but it can change `maximum` and `minimum`.
- The same price re-sent for a timestamp: duplicate heap entry, both valid, no bug.
- Correcting a record down and then back to its old price makes the old stale entry valid again. That is correct: validity is checked against the dict, not stored on the entry.
- Heap entries are tuples `(price, ts)`, so equal prices fall back to comparing timestamps (ints, always comparable).

**Follow-ups:**
- *Why not a `SortedList` of prices?* It also works (remove the old price, add the new one, O(log n) with a real balanced structure), but it is not in the standard library; lazy deletion needs only `heapq`.
- *Can the heaps grow without bound?* Yes, if nobody calls `maximum` or `minimum`, stale entries sit there. Rebuild a heap from the dict when it exceeds twice the number of live timestamps (O(n) per rebuild, amortised O(1) per update).
- *Thread-safety (stated concept only):* the dict write and the two pushes must look atomic to readers, so one lock around each method body; the heaps' lazy pops mutate state even inside a "read".
- *Scoring note [Set D, Q1 of 4, 8 min, 15 pts]:* about 4.5 points for stating the rules first (correction replaces, current = latest timestamp not latest call, stale means price differs from the dict), 4.5 for a correct solution that passes the example and a random check, 3 for O(log n) amortised with the "each entry popped once" reason, 1.5 for the edge cases above, 1.5 for a crisp under-60-second summary. Partial credit: a working O(n)-per-query version with correct rules earns most of the first two parts (about 6 of 15), but nothing for the complexity part. How I would pace this: 1.5 minutes to restate rules and pick dict plus two heaps, 4 minutes to code, 1.5 minutes to run the example, 1 minute for complexity and the stale-entry argument.

**Common mistakes:**
- Taking `current` from the last call instead of the largest timestamp.
- Forgetting that a correction leaves the old entry in the heap, then returning a stale maximum.
- Deleting by value when a different timestamp has the same price (check the timestamp's own latest price, not "does this price exist").
- Using `heapq` for the max without negating.
- Popping a valid top entry "to be safe" and so losing a live record.

---

### Q12 ⭐⭐⭐ 🔴 [Set A, Q4 of 5, 12 min, 25 pts] LRU cache with expiry (TTL) and an injected clock. Implement class `TTLCache(clock, capacity)` (1 <= capacity <= 1000) with `put(key, value, ttl)` (ttl >= 1 seconds), `get(key)` and `size()`. An entry put at time T with ttl is alive while now < T + ttl and expired from time T + ttl on (exactly at T + ttl it is already gone). `get` returns the value of a live key, or -1 when the key is absent or expired; a successful `get` makes the key the most recently used but does NOT extend its life. `put` first removes every expired entry; then, if the key is already present, replaces its value, ttl and expiry (new life measured from now) and makes it most recently used; otherwise, if the cache already holds `capacity` live keys, evicts the least recently used LIVE key; then inserts. `put` returns None; `size()` returns the number of live entries (after removing expired ones). Combine an OrderedDict (or the list of Q5) for recency with a min-heap of (expiry, key, version) and lazy deletion of stale heap entries (Part 8 Q31): each operation is O(log n) amortised. Say why expired entries must be purged before choosing an LRU victim (an expired entry must never survive while a live one is evicted) and, as a stated concept only, what a lock around the whole method body would protect. The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[2], ops=[[0, 'put', ['a', 1, 10]], [1, 'put', ['b', 2, 3]], [2, 'get', ['a']], [3, 'put', ['c', 3, 10]], [3, 'get', ['b']], [4, 'size', []], [10, 'get', ['a']], [10, 'size', []], [11, 'put', ['c', 9, 5]], [15, 'get', ['c']], [16, 'get', ['c']]] -> [null, null, 1, null, -1, 2, -1, 1, null, 9, -1].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** LRU recency (OrderedDict) plus expiry (min-heap of expiry times with lazy deletion, Part 8 Q31). Two different orders on the same keys: "least recently used" and "expires soonest". One structure each.

**Say this first (1 line):** "Rules first: alive while now < T + ttl, so expiry at exactly T + ttl; purge every expired entry before I look at capacity; a get refreshes recency but never life."

**Brute force:**
- A list of `[key, value, expiry]` in recency order. On every call filter out expired entries (O(n)), then find or insert (O(n)).
- O(n) per operation, n <= 1000 here so it passes, but it is the oracle, not the answer.

**Optimal:**
- `od`: OrderedDict key -> (value, version), oldest first, so the left end is the LRU key.
- `heap`: entries `(expiry, key, version)`. `version` increases on every `put`, so an entry for an overwritten key is recognised as stale (the stored version no longer matches).
- `_purge()`: while the heap top has `expiry <= now`, pop it. If that key is still in `od` with the same version, delete it. Otherwise the entry was stale (key replaced or already evicted): ignore it. "`<=`" is the exactly-at-expiry rule.
- `put(key, value, ttl)`: purge; then if the key exists, remove it (it will be reinserted fresh, so new value, new ttl, new expiry, most recent); else if `len(od) == capacity`, `popitem(last=False)` evicts the LRU live key; then insert at the right end and push `(now + ttl, key, version)`.
- `get(key)`: purge; if absent return -1; else `move_to_end` and return the value. The heap is untouched, so life is not extended.
- `size()`: purge, then `len(od)`.
- Tie rules: LRU order is the only tie-break for eviction (an entry is never evicted because it is "nearly expired"; only expired entries disappear for that reason). Two entries with the same expiry are both purged in one pass; the heap's secondary comparison on `key` only matters for ordering inside the heap, and the unique `version` stops comparisons ever reaching the value (keys must be comparable with each other, true for the strings and ints used here).
- Why purge first: if an expired entry is still in `od` while the cache is at capacity, the LRU victim could be a live key even though a dead entry was holding the slot. The cache would shrink its live content for nothing.

**Complexity:**
- Each call: O(log n) amortised. Every heap entry is pushed once and popped at most once, so total purge pops <= total puts.
- OrderedDict `move_to_end`, `popitem`, delete and insert are O(1).
- Space: O(capacity) live keys, plus stale heap entries that wait until their expiry time passes; at most one per `put`, so O(puts in the last max-ttl seconds).

**Dry run:** the first example, capacity 2. Notation: `od` is listed LRU first.

| time | call | purge | od after | returns |
|---|---|---|---|---|
| 0 | put a=1 ttl 10 | nothing | a (exp 10) | None |
| 1 | put b=2 ttl 3 | nothing | a, b (exp 4) | None |
| 2 | get a | nothing | b, a | 1 |
| 3 | put c=3 ttl 10 | nothing (b expires at 4) | full, evict LRU b: a, c (exp 13) | None |
| 3 | get b | nothing | a, c | -1 |
| 4 | size | pop (4, b): b not in od, ignore | a, c | 2 |
| 10 | get a | pop (10, a): delete a | c | -1 |
| 10 | size | | c | 1 |
| 11 | put c=9 ttl 5 | nothing | c replaced, exp 16 | None |
| 15 | get c | nothing (16 > 15) | c | 9 |
| 16 | get c | pop (16, c): delete | empty | -1 |

**Code:**
```python
import heapq, random
from collections import OrderedDict

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class NaiveTTL:                          # brute force: list of [key, value, expiry], least recent first, O(n) per call
    def __init__(self, clock, capacity): self.clock = clock; self.cap = capacity; self.items = []
    def _live(self):
        now = self.clock(); self.items = [e for e in self.items if e[2] > now]
    def put(self, key, value, ttl):
        self._live(); now = self.clock()
        for i, e in enumerate(self.items):
            if e[0] == key: del self.items[i]; break
        else:
            if len(self.items) >= self.cap: self.items.pop(0)     # least recently used LIVE key
        self.items.append([key, value, now + ttl])
    def get(self, key):
        self._live()
        for i, e in enumerate(self.items):
            if e[0] == key: self.items.append(self.items.pop(i)); return e[1]
        return -1
    def size(self): self._live(); return len(self.items)

class TTLCache:
    def __init__(self, clock, capacity):
        self.clock = clock; self.cap = capacity
        self.od = OrderedDict()          # key -> (value, version); order = recency, LRU first
        self.heap = []                   # (expiry, key, version); stale versions skipped lazily
        self.version = 0
    def _purge(self):
        now = self.clock()
        while self.heap and self.heap[0][0] <= now:          # expiry <= now means already gone
            _, key, ver = heapq.heappop(self.heap)
            if key in self.od and self.od[key][1] == ver: del self.od[key]
    def put(self, key, value, ttl):
        self._purge()                                         # 1. drop every expired entry first
        now = self.clock()
        if key in self.od: del self.od[key]                   # 2. replace: new value, new life, most recent
        elif len(self.od) >= self.cap: self.od.popitem(last=False)   # 3. evict LRU live key
        self.version += 1
        self.od[key] = (value, self.version)
        heapq.heappush(self.heap, (now + ttl, key, self.version))
    def get(self, key):
        self._purge()
        if key not in self.od: return -1
        self.od.move_to_end(key)                              # refresh recency, not life
        return self.od[key][0]
    def size(self): self._purge(); return len(self.od)

class NoPurgeBug(TTLCache):              # deliberately wrong: evicts by recency without purging first
    def put(self, key, value, ttl):
        now = self.clock()
        if key in self.od: del self.od[key]
        elif len(self.od) >= self.cap: self.od.popitem(last=False)
        self.version += 1; self.od[key] = (value, self.version)
        heapq.heappush(self.heap, (now + ttl, key, self.version))

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = dict(init=[2], ops=[[0, 'put', ['a', 1, 10]], [1, 'put', ['b', 2, 3]], [2, 'get', ['a']], [3, 'put', ['c', 3, 10]],
    [3, 'get', ['b']], [4, 'size', []], [10, 'get', ['a']], [10, 'size', []], [11, 'put', ['c', 9, 5]], [15, 'get', ['c']], [16, 'get', ['c']]])
want = [None, None, 1, None, -1, 2, -1, 1, None, 9, -1]
assert run(TTLCache, **ex) == want == run(NaiveTTL, **ex)
print('example ->', run(TTLCache, **ex))

random.seed(12)
for case in range(600):
    cap = random.randint(1, 4); t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 3)
        r = random.random()
        if r < 0.45: ops.append([t, 'put', [random.choice('abcde'), random.randint(0, 99), random.randint(1, 6)]])
        elif r < 0.9: ops.append([t, 'get', [random.choice('abcde')]])
        else: ops.append([t, 'size', []])
    assert run(TTLCache, [cap], ops) == run(NaiveTTL, [cap], ops), (cap, ops)
print('600 random timed sequences match the naive reference')

# why purge first: capacity 2, a expires at 5, b lives long. At t=5 put c.
seq = [[0, 'put', ['a', 1, 5]], [1, 'put', ['b', 2, 100]], [2, 'get', ['a']], [5, 'put', ['c', 3, 100]], [5, 'get', ['b']]]
good = run(TTLCache, [2], seq); bad = run(NoPurgeBug, [2], seq)
assert good[-1] == 2 and bad[-1] == -1
print('with purge b ->', good[-1], '| without purge b ->', bad[-1], '(a is dead but b, live, gets evicted)')

# boundary and get-does-not-extend-life
seq = [[0, 'put', ['k', 7, 4]], [3, 'get', ['k']], [3, 'size', []], [4, 'get', ['k']], [4, 'size', []]]
assert run(TTLCache, [1], seq) == [None, 7, 1, -1, 0]
seq = [[0, 'put', ['k', 7, 4]], [3, 'put', ['k', 8, 4]], [6, 'get', ['k']], [7, 'get', ['k']]]   # re-put restarts the life
assert run(TTLCache, [1], seq) == [None, None, 8, -1]
seq = [[0, 'put', ['a', 1, 9]], [0, 'put', ['b', 2, 9]], [0, 'get', ['a']], [0, 'put', ['c', 3, 9]], [0, 'get', ['b']], [0, 'get', ['a']]]
assert run(TTLCache, [2], seq) == [None, None, 1, None, -1, 1]       # capacity 2: get(a) saved a, b was LRU
assert run(TTLCache, [1], []) == []
print('edge asserts ok')
```

**Output (my run):**
```
example -> [None, None, 1, None, -1, 2, -1, 1, None, 9, -1]
600 random timed sequences match the naive reference
with purge b -> 2 | without purge b -> -1 (a is dead but b, live, gets evicted)
edge asserts ok
```

**Edge cases:**
- A key is alive at T + ttl - 1 and gone at T + ttl (tested).
- `get` right before expiry does not extend life (tested).
- Re-`put` of a key restarts life from now and replaces value and ttl (tested).
- Capacity 1: every new key evicts the previous one.
- A put when every entry is expired: purge empties the cache first, nothing is evicted.
- Stale heap entries (replaced or evicted keys) must be ignored on pop, otherwise the new entry for the same key would be deleted early. That is why `version` exists.
- Same timestamp for many calls (non-decreasing, not strictly increasing) works because nothing depends on distinct times.

**Follow-ups:**
- *Why `version` and not just the key?* After `put(k)` twice, the heap holds two entries for `k`. The old one fires first (if its ttl was shorter) and must not delete the new value.
- *Thread-safety (stated concept only):* a single lock around the whole body of `put`, `get` and `size`. The purge, the capacity check and the insert must happen as one step, and even `get` mutates recency order and the heap, so there are no read-only methods.
- *Could a background thread do the purging?* It could free memory sooner, but correctness must not depend on it: every call still purges lazily, so results are identical with or without the thread.
- *Scoring note [Set A, Q4 of 5, 12 min, 25 pts]:* 7.5 points for stating the rules (expiry boundary, purge before evict, get does not extend life, put-replace restarts life), 7.5 for a correct solution that passes the example and a random timed check against the naive version, 5 for O(log n) amortised and why each entry is popped once, 2.5 for edge cases, 2.5 for a crisp spoken summary. Partial credit: a correct list-based O(n) version gets about 12 of 25; a correct LRU with no expiry handled gets about 8. How I would pace this: 2 minutes for rules, 3 minutes to sketch OrderedDict plus heap and the version trick, 5 minutes to code, 2 minutes to run the example and test.

**Common mistakes:**
- Evicting the LRU key before purging expired ones.
- Treating the expiry as inclusive (`now <= T + ttl`) instead of `now < T + ttl`.
- Letting `get` refresh the expiry.
- Deleting by key alone from stale heap entries, killing a freshly replaced value.
- Reading `time.time()` inside the class instead of `clock()`.
- `size()` returning `len(od)` without purging.

---

### Q13 ⭐⭐⭐ 🔴 [Set D, Q3 of 4, 13 min, 30 pts] Maximum frequency stack. Implement class `FreqStack()` with `push(x)` (returns None) and `pop()`, which removes and returns the most frequent element currently in the stack; if several elements share the highest frequency, remove the one whose TOP-most occurrence is closest to the top of the stack (the most recently pushed among them). `pop` is never called on an empty stack. O(1) per operation: a dict value -> count, a dict count -> stack of values (the value is pushed on stack f when its count becomes f), and `max_freq`; `pop` takes the top of stack[max_freq], decrements that value's count and lowers `max_freq` when its stack empties. Explain why one value can sit on several frequency stacks at once and why this gives exactly the tie rule. The related designs are the min stack of Part 4 Q2 and the max stack of Part 4 Q38; top-k frequencies are Part 1 Q10. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference that scans the whole stack for the highest frequency and its topmost occurrence on small inputs. Example: init=[], ops=[['push', [5]], ['push', [7]], ['push', [5]], ['push', [7]], ['push', [4]], ['push', [5]], ['pop', []], ['pop', []], ['pop', []], ['pop', []]] -> [null, null, null, null, null, null, 5, 7, 5, 4].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Frequency buckets as stacks (O(1) design). Instead of searching for the most frequent element, keep one stack per frequency level, in push order.

**Say this first (1 line):** "A value with count f sits on stacks 1 to f, one entry each; `pop` takes the top of the highest non-empty stack, and that top is exactly the most frequent, most recently pushed value."

**Brute force:**
- Keep the stack as a list. On `pop`, count every value, find the highest count, then scan from the top for the first element with that count and remove it. O(n) per pop.

**Optimal:**
- `count[x]`: how many copies of x are in the stack now.
- `stacks[f]`: values in the order their count REACHED f. `push(x)`: `count[x] += 1`, append x to `stacks[count[x]]`, raise `max_freq` if needed.
- `pop()`: take `x = stacks[max_freq].pop()`, `count[x] -= 1`, and if `stacks[max_freq]` is now empty then `max_freq -= 1`.
- Why one value sits on several stacks: pushing 5 three times puts 5 on stack 1, stack 2 and stack 3. Popping 5 removes it from stack 3 only, so it correctly remains on stacks 1 and 2 as a 2-copy value. The levels peel off from the top, mirroring the order in which the copies were pushed.
- Why this gives exactly the tie rule: the highest non-empty level is the highest frequency. Within that level, the stack order is the order in which values reached that level, and the last one to reach it is the one whose latest push is most recent. That is the topmost occurrence among the tied values (the entry on stack f was placed at the time of the push that made the count f, and a later push of another tied value would have placed that value later on the same stack).
- Invariant: `stacks[f]` is non-empty for every f <= `max_freq`, which is why decreasing `max_freq` by one after a pop is enough.

**Complexity:**
- `push` and `pop`: O(1) average (dict operations and list append/pop).
- Space: O(n), one stack entry per element in the stack (a value with count f has exactly f entries across the stacks).

**Dry run:** the first example.

| push | count | stacks (level: contents) | max_freq |
|---|---|---|---|
| 5 | 5:1 | 1:[5] | 1 |
| 7 | 7:1 | 1:[5,7] | 1 |
| 5 | 5:2 | 1:[5,7] 2:[5] | 2 |
| 7 | 7:2 | 1:[5,7] 2:[5,7] | 2 |
| 4 | 4:1 | 1:[5,7,4] 2:[5,7] | 2 |
| 5 | 5:3 | 1:[5,7,4] 2:[5,7] 3:[5] | 3 |

| pop | step | result |
|---|---|---|
| 1 | top of level 3 is 5; level 3 empties, max_freq = 2; count 5 = 2 | 5 |
| 2 | level 2 is [5,7]: top is 7 (7 reached count 2 after 5 did); count 7 = 1 | 7 |
| 3 | level 2 is [5]: top is 5; level 2 empties, max_freq = 1; count 5 = 1 | 5 |
| 4 | level 1 is [5,7,4]: top is 4 | 4 |

Outputs: 5, 7, 5, 4.

**Code:**
```python
import random
from collections import defaultdict

class NaiveFreqStack:                    # brute force: scan the whole stack on every pop, O(n)
    def __init__(self): self.s = []
    def push(self, x): self.s.append(x)
    def pop(self):
        cnt = {}
        for v in self.s: cnt[v] = cnt.get(v, 0) + 1
        best = max(cnt.values())
        for i in range(len(self.s) - 1, -1, -1):      # topmost occurrence among the most frequent values
            if cnt[self.s[i]] == best: return self.s.pop(i)

class FreqStack:
    def __init__(self):
        self.count = defaultdict(int)    # value -> current count
        self.stacks = defaultdict(list)  # f -> values in the order their count reached f
        self.max_freq = 0
    def push(self, x):
        self.count[x] += 1
        f = self.count[x]
        self.stacks[f].append(x)         # x now sits on stack 1..f (one entry per level)
        if f > self.max_freq: self.max_freq = f
    def pop(self):
        x = self.stacks[self.max_freq].pop()
        self.count[x] -= 1
        if not self.stacks[self.max_freq]: self.max_freq -= 1
        return x

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[], ops=[['push', [5]], ['push', [7]], ['push', [5]], ['push', [7]], ['push', [4]], ['push', [5]],
                        ['pop', []], ['pop', []], ['pop', []], ['pop', []]])
want = [None, None, None, None, None, None, 5, 7, 5, 4]
assert run(FreqStack, **ex) == want == run(NaiveFreqStack, **ex)
print('example ->', run(FreqStack, **ex))

random.seed(13)
for case in range(800):
    ops = []; size = 0
    for _ in range(random.randint(0, 50)):
        if size and random.random() < 0.4: ops.append(['pop', []]); size -= 1
        else: ops.append(['push', [random.randint(0, 4)]]); size += 1
    assert run(FreqStack, [], ops) == run(NaiveFreqStack, [], ops), ops
print('800 random sequences match the naive reference')

# one value on several stacks
f = FreqStack()
for x in [5, 5, 5, 7]: f.push(x)
assert [i for i in (1, 2, 3) if 5 in f.stacks[i]] == [1, 2, 3] and f.stacks[1] == [5, 7]
print('stacks after 5,5,5,7:', {k: v for k, v in sorted(f.stacks.items())})

# edge cases
f = FreqStack(); f.push(9); assert f.pop() == 9 and f.max_freq == 0
f = FreqStack()
for x in [1, 2, 3]: f.push(x)
assert [f.pop(), f.pop(), f.pop()] == [3, 2, 1]               # all frequency 1: plain LIFO
f = FreqStack()
for x in [2, 2, 2]: f.push(x)
assert [f.pop(), f.pop(), f.pop()] == [2, 2, 2]
f = FreqStack()
for x in [1, 1, 2, 2]: f.push(x)
assert f.pop() == 2 and f.pop() == 1 and f.pop() == 2 and f.pop() == 1   # tie at freq 2: 2 was pushed last
assert run(FreqStack, [], []) == []
print('edge asserts ok')
```

**Output (my run):**
```
example -> [None, None, None, None, None, None, 5, 7, 5, 4]
800 random sequences match the naive reference
stacks after 5,5,5,7: {1: [5, 7], 2: [5], 3: [5]}
edge asserts ok
```

**Edge cases:**
- All values distinct: every element has frequency 1, so it behaves as a normal LIFO stack.
- One value repeated: pops return it every time and `max_freq` drops 3, 2, 1, 0.
- Tie at the top frequency (1,1,2,2): the value pushed last pops first (2), then the other (1), then the same again.
- Pushing, popping to empty, then pushing again: `max_freq` returns to 0 and then grows again correctly.
- `pop` is never called on an empty stack (stated by the prompt), so no error handling is needed.

**Follow-ups:**
- *Relation to earlier designs:* the min stack (Part 4 Q2) keeps a parallel stack of minimums and the max stack (Part 4 Q38) needs lazy deletion or a linked list for `popMax`; here the bucket-per-frequency idea gives O(1) with no heap. Top-k frequencies by counting is Part 1 Q10.
- *What if `pop` had to remove the least frequent element?* Keep a `min_freq` too; but then raising it after a pop is harder (levels can become empty in the middle), so a doubly linked list of levels is needed (the same idea as the all-O(1) data structure).
- *Thread-safety (stated concept only):* `push` and `pop` each touch `count`, a stack and `max_freq`, so a lock around each method makes them atomic; without it a pop could see a `max_freq` that no longer matches the stacks.
- *Scoring note [Set D, Q3 of 4, 13 min, 30 pts]:* 9 points for stating the tie rule and an example before coding, 9 for a correct O(1) solution that passes the example and a random check, 6 for the complexity and the "value on several stacks" explanation, 3 for edge cases, 3 for a crisp summary. Partial credit: a correct O(n)-per-pop scan solution earns about 12 of 30; a heap of (-freq, -time, value) with lazy deletion gets about 20 (it is O(log n) and correct, only not O(1)). How I would pace this: 2 minutes for rules and an example, 3 minutes to find the per-frequency stacks, 5 minutes to code, 3 minutes to test and explain.

**Common mistakes:**
- Using one stack per VALUE instead of per frequency, losing the global push order.
- Removing the value from every level on pop instead of only the top level.
- Forgetting to lower `max_freq` when its stack empties (the next pop hits an empty list).
- Pushing the value only on stack `count` but pulling `count` from the stale value after a pop (update `count` on every pop).
- Breaking ties by smallest value or by insertion order of first appearance instead of the most recent push.

---

### Q14 ⭐⭐ 🟢 Fixed-window counter rate limiter and its boundary burst. Implement class `FixedWindowLimiter(clock, limit, window)` with `allow(user)`: time is cut into windows [k*window, (k+1)*window) for k = t // window; a request is accepted when fewer than `limit` requests were ACCEPTED for that user in the current window (the count resets when the window index changes); rejected requests do not count. O(1) time and memory per user. Show the weakness with limit 2, window 10: accepted at t = 8, 9, 10 and 11 (four requests inside 4 seconds, double the intended rate), which a sliding window would reject; compare with the sliding window log of Q7 and the token bucket of Q8. Say as a stated concept that a distributed version uses an atomic increment with an expiry in a shared store. The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[2, 10], ops=[[8, 'allow', ['u']], [9, 'allow', ['u']], [9, 'allow', ['u']], [10, 'allow', ['u']], [11, 'allow', ['u']], [11, 'allow', ['u']], [20, 'allow', ['u']], [20, 'allow', ['v']]] -> [True, True, False, True, True, False, True, True].
**Asked at:** Rate-limiter guides (techinterview.org 'Implement a Rate Limiter' covering token bucket, leaky bucket, fixed and sliding window; a Redis rate-limiter interview post on oneuptime.com; search snippets only, not opened)

**Pattern:** Fixed-window counter. Cut time into equal windows, count accepted requests per user per window, reset when the window index changes. The simplest limiter, and the one with a known boundary weakness.

**Say this first (1 line):** "Window index is `t // window`; I store one pair `[index, accepted]` per user, reset it when the index changes, and only count accepted requests."

**Brute force:**
- Remember every accepted timestamp per user. On each request, count those with the same `t // window`. O(history) per call and unbounded memory.

**Optimal:**
- `state[user] = [k, count]` where `k = t // window`.
- On `allow`: compute `k` from `clock()`. If the user has no state or the stored index differs, reset to `[k, 0]`. If `count < limit`, increment and return True. Else return False without incrementing (rejected requests do not count).
- Boundary rule: window `k` is `[k*window, (k+1)*window)`, so `t = 10` with window 10 is the FIRST second of window 1.
- Tie rule: two requests in the same second are just two requests in the same window; the first ones accepted take the quota.

**Complexity:**
- Time O(1) per call (one dict lookup and integer arithmetic).
- Memory O(1) per user (two integers), O(users) in total. Old users' entries can be dropped when their window index is behind the current one (a sweep every so often).

**Dry run:** limit 2, window 10 (the example).

| t | user | window k | count before | decision |
|---|---|---|---|---|
| 8 | u | 0 | 0 | True (count 1) |
| 9 | u | 0 | 1 | True (count 2) |
| 9 | u | 0 | 2 | False (not counted) |
| 10 | u | 1 | reset to 0 | True (count 1) |
| 11 | u | 1 | 1 | True (count 2) |
| 11 | u | 1 | 2 | False |
| 20 | u | 2 | reset | True |
| 20 | v | 2 | no state | True |

The weakness is visible in rows 1, 2, 4, 5: accepted at t = 8, 9, 10, 11. That is four requests inside four seconds with a limit of 2 per 10 seconds, double the intended rate, because the window boundary at 10 resets the count. The sliding window log of Q7 would accept 8 and 9, and refuse 10 and 11 (the code below shows both). In the worst case a client can send `limit` requests at the end of one window and `limit` at the start of the next, so up to `2 * limit` in a span of two seconds. The token bucket of Q8 smooths this with a burst allowance plus a steady refill.

**Code:**
```python
import random

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class NaiveFixed:                        # brute force: keep every accepted timestamp, count those in the same window
    def __init__(self, clock, limit, window): self.clock = clock; self.limit = limit; self.w = window; self.acc = {}
    def allow(self, user):
        now = self.clock(); k = now // self.w
        n = sum(1 for t in self.acc.get(user, []) if t // self.w == k)
        if n < self.limit:
            self.acc.setdefault(user, []).append(now); return True
        return False

class FixedWindowLimiter:
    def __init__(self, clock, limit, window):
        self.clock = clock; self.limit = limit; self.window = window
        self.state = {}                  # user -> [window index, accepted count]
    def allow(self, user):
        k = self.clock() // self.window
        st = self.state.get(user)
        if st is None or st[0] != k: st = self.state[user] = [k, 0]    # new window: reset
        if st[1] < self.limit:
            st[1] += 1; return True
        return False                     # rejected requests are not counted

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = dict(init=[2, 10], ops=[[8, 'allow', ['u']], [9, 'allow', ['u']], [9, 'allow', ['u']], [10, 'allow', ['u']],
    [11, 'allow', ['u']], [11, 'allow', ['u']], [20, 'allow', ['u']], [20, 'allow', ['v']]])
want = [True, True, False, True, True, False, True, True]
assert run(FixedWindowLimiter, **ex) == want == run(NaiveFixed, **ex)
print('example ->', run(FixedWindowLimiter, **ex))

random.seed(14)
for case in range(600):
    limit = random.randint(1, 3); w = random.randint(1, 6); t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 4)
        ops.append([t, 'allow', [random.choice('uvw')]])
    assert run(FixedWindowLimiter, [limit, w], ops) == run(NaiveFixed, [limit, w], ops)
print('600 random timed sequences match the naive reference')

# the boundary burst: 4 accepted in 4 seconds (t = 8..11) with limit 2 per 10 s
res = run(FixedWindowLimiter, [2, 10], [[t, 'allow', ['u']] for t in (8, 9, 10, 11)])
assert res == [True] * 4
# a sliding window log (accept if < limit accepted in (now-window, now]) would refuse t=10 and t=11
def sliding(limit, window, times):
    acc = []; out = []
    for t in times:
        n = sum(1 for a in acc if a > t - window)
        if n < limit: acc.append(t); out.append(True)
        else: out.append(False)
    return out
assert sliding(2, 10, (8, 9, 10, 11)) == [True, True, False, False]
print('fixed window', res, '| sliding window', sliding(2, 10, (8, 9, 10, 11)))

# edge cases
assert run(FixedWindowLimiter, [1, 5], [[0, 'allow', ['a']], [4, 'allow', ['a']], [5, 'allow', ['a']]]) == [True, False, True]  # t=5 is a new window
assert run(FixedWindowLimiter, [3, 1], [[7, 'allow', ['a']]] * 4) == [True, True, True, False]
assert run(FixedWindowLimiter, [1, 1], [[t, 'allow', ['a']] for t in range(5)]) == [True] * 5     # window 1: every second is new
assert run(FixedWindowLimiter, [1, 10], []) == []
assert run(FixedWindowLimiter, [1, 10], [[0, 'allow', ['a']], [0, 'allow', ['b']], [0, 'allow', ['a']]]) == [True, True, False]  # users independent
print('edge asserts ok')
```

**Output (my run):**
```
example -> [True, True, False, True, True, False, True, True]
600 random timed sequences match the naive reference
fixed window [True, True, True, True] | sliding window [True, True, False, False]
edge asserts ok
```

**Edge cases:**
- First request of a user: no state, treat as a fresh window.
- Window 1: every second is its own window, so each request is a new window and always accepted when limit >= 1.
- Skipping whole windows (t jumps from 3 to 57): the stored index is stale, so reset; no need to "tick" the empty windows.
- Different users are independent.
- Rejected requests do not consume quota, so a client hammering the limiter in one window cannot lock itself out of the next.
- Same second repeated: windows depend on the integer time only.

**Follow-ups:**
- *Distributed version (stated concept only):* store the count under a key like `user:window_index` in a shared store, use an atomic increment, and set an expiry of one window so old keys vanish. Any server that sees the same key sees the same count. Note that this version counts every attempt, including rejected ones, unless you decrement.
- *How do I fix the boundary burst?* Sliding window log (exact, O(limit) memory per user, Q7), sliding window counter (weighted blend of two adjacent windows, approximate, O(1)), or token bucket (Q8).
- *Thread-safety (stated concept only):* the read-compare-increment must be one atomic step, so a lock per user or around the method.

**Common mistakes:**
- Counting rejected requests (a client over the limit stays blocked for no reason).
- Using `t % window` as the window id (that is the offset inside the window).
- Forgetting to reset when the index changes.
- Claiming fixed window is "accurate": it is exact per window but allows up to `2 * limit` across a boundary.

---

### Q15 ⭐⭐ 🟢 Peeking iterator. Implement class `PeekingIterator(it)` where `it` is a Python iterator (the checker passes `iter(list)`): you may only call `next(it)`, never index or copy it, and `list(it)` is not allowed. Methods: `peek()` returns the next element WITHOUT consuming it (calling it twice returns the same value), `next()` returns and consumes it, `hasNext()` says whether an element remains. Keep one buffered element and refill it after each `next`. The checker never calls `peek` or `next` when `hasNext()` is False. Say why the buffer must be filled eagerly (so `hasNext` is a plain flag) and the cost of one extra element of memory. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). Here `init` is a one-element list holding the list that the checker wraps with `iter()`. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[1, 2, 3]], ops=[['next', []], ['peek', []], ['next', []], ['next', []], ['hasNext', []]] -> [1, 2, 2, 3, False]; init=[[7]], ops=[['peek', []], ['peek', []], ['hasNext', []], ['next', []], ['hasNext', []]] -> [7, 7, True, 7, False].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Iterator adapter with a one-element look-ahead buffer. An iterator only goes forward, so to answer "what comes next?" without consuming it, I pull one element early and hold it.

**Say this first (1 line):** "I keep one buffered element, filled eagerly in the constructor and refilled after every `next`, so `peek` returns the buffer and `hasNext` is a plain sentinel check."

**Brute force:**
- `list(it)` once and keep an index. That breaks the rules (not allowed), uses O(n) memory, and cannot work on an infinite or lazy stream.

**Optimal:**
- A private sentinel object `_DONE` marks exhaustion. A sentinel, not `None`, because `None` can be a real element.
- `__init__`: `buf = next(it, _DONE)`.
- `peek()`: return `buf`. Calling it twice returns the same value.
- `next()`: save `v = buf`, refill `buf = next(it, _DONE)`, return `v`.
- `hasNext()`: `buf is not _DONE`.
- Why eager: the buffer always holds the next value or the sentinel, so `hasNext` needs no call into the underlying iterator and cannot raise or have side effects.
- The cost is one extra element of memory. The trade-off: the underlying iterator is advanced one step earlier than the caller's `next`, which matters if pulling an element has a side effect or is slow (a lazy variant fills the buffer on the first `peek` or `hasNext`; the code below shows the eager one, and the test confirms the constructor pulled exactly one element).

**Complexity:**
- Every method O(1) apart from the cost of the underlying `next(it)`.
- Space O(1) extra (one buffered element).

**Dry run:** first example, `[1, 2, 3]`.

| call | buf after | returns |
|---|---|---|
| constructor | 1 | |
| next() | v = 1, buf = 2 | 1 |
| peek() | 2 | 2 |
| next() | v = 2, buf = 3 | 2 |
| next() | v = 3, buf = _DONE | 3 |
| hasNext() | | False |

Second example `[7]`: peek 7, peek 7, hasNext True, next 7 (buf becomes `_DONE`), hasNext False.

**Code:**
```python
import random

class NaivePeeking:                      # brute force: copies everything into a list (not allowed by the prompt, fine as an oracle)
    def __init__(self, it): self.a = list(it); self.i = 0
    def peek(self): return self.a[self.i]
    def next(self): self.i += 1; return self.a[self.i - 1]
    def hasNext(self): return self.i < len(self.a)

_DONE = object()

class PeekingIterator:
    def __init__(self, it):
        self.it = it
        self.buf = next(it, _DONE)       # buffer is filled eagerly, one element ahead
    def peek(self): return self.buf
    def next(self):
        v = self.buf
        self.buf = next(self.it, _DONE)  # refill right after consuming
        return v
    def hasNext(self): return self.buf is not _DONE

def run(cls, init, ops):
    o = cls(iter(init[0]))
    return [getattr(o, m)(*a) for m, a in ops]

e1 = dict(init=[[1, 2, 3]], ops=[['next', []], ['peek', []], ['next', []], ['next', []], ['hasNext', []]])
e2 = dict(init=[[7]], ops=[['peek', []], ['peek', []], ['hasNext', []], ['next', []], ['hasNext', []]])
assert run(PeekingIterator, **e1) == [1, 2, 2, 3, False] == run(NaivePeeking, **e1)
assert run(PeekingIterator, **e2) == [7, 7, True, 7, False] == run(NaivePeeking, **e2)
print('examples ->', run(PeekingIterator, **e1), run(PeekingIterator, **e2))

random.seed(15)
for case in range(600):
    data = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    ops = []; left = len(data)
    for _ in range(random.randint(0, 20)):
        r = random.random()
        if left and r < 0.35: ops.append(['next', []]); left -= 1
        elif left and r < 0.7: ops.append(['peek', []])
        else: ops.append(['hasNext', []])
    assert run(PeekingIterator, [data], ops) == run(NaivePeeking, [data], ops)
print('600 random sequences match the naive reference')

# it works on a one-shot generator and never reads more than one element ahead
pulled = []
def gen():
    for i in range(5): pulled.append(i); yield i
p = PeekingIterator(gen())
assert pulled == [0]                     # constructor pulled exactly one element
p.peek(); p.peek(); assert pulled == [0]  # peeking never advances
p.next(); assert pulled == [0, 1]
print('elements pulled so far:', pulled)

# edge cases: None and falsy values are legitimate elements (sentinel is a private object)
p = PeekingIterator(iter([None, 0, '']))
assert p.hasNext() and p.next() is None and p.next() == 0 and p.next() == '' and not p.hasNext()
p = PeekingIterator(iter([]))
assert not p.hasNext()
p = PeekingIterator(iter([4])); assert p.next() == 4 and not p.hasNext()
print('edge asserts ok')
```

**Output (my run):**
```
examples -> [1, 2, 2, 3, False] [7, 7, True, 7, False]
600 random sequences match the naive reference
elements pulled so far: [0, 1]
edge asserts ok
```

**Edge cases:**
- Empty iterator: constructor leaves `buf = _DONE`, `hasNext` is False immediately.
- Elements that are `None`, 0 or `''` are real data (tested). This is the reason for a private sentinel.
- `peek` twice, `next` once: both peeks return the same value.
- A generator that can be iterated only once works, since nothing is copied and nothing is rewound (tested).
- The checker never calls `peek` or `next` when `hasNext` is False. In a real API I would raise `StopIteration` there.

**Follow-ups:**
- *Why not call `next` inside `hasNext`?* It would consume an element that `peek` or `next` later needs, or force a second buffer; eager fill keeps one rule: the buffer is always current.
- *Lazy buffering:* fill on first demand, with a `filled` flag. Useful when constructing the iterator must not touch the source. Costs a branch in every method.
- *Thread-safety (stated concept only):* `next` reads the buffer and refills it in two steps, so concurrent callers need a lock around the method body or they may receive the same element twice.

**Common mistakes:**
- Using `None` as the "done" marker and mishandling real `None` elements.
- Refilling the buffer in `peek`, which consumes data.
- Calling `list(it)` (explicitly disallowed).
- Forgetting to refill after `next`, so `peek` returns the element just consumed.

---

### Q16 ⭐⭐ 🟢 Logger rate limiter for repeated messages. Implement class `Logger(clock)` with `shouldPrint(message)`: return True (and remember the time) when `message` was never printed before or was last printed at time p with now - p >= 10 (so exactly 10 seconds later it is allowed again); otherwise return False WITHOUT updating the remembered time. A message that was refused keeps its old print time, so a steady stream of the same message every 3 seconds prints at t = 0, 12 (the first arrival at or after 10), 24 and so on. One dict message -> last printed time gives O(1) per call; say, as a stated concept, how to bound memory for an unbounded stream of distinct messages (periodically drop entries older than 10 seconds, or keep a deque of (time, message) in arrival order). Compare the boundary with the hit counter of Q1. The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[], ops=[[1, 'shouldPrint', ['foo']], [2, 'shouldPrint', ['bar']], [3, 'shouldPrint', ['foo']], [8, 'shouldPrint', ['bar']], [10, 'shouldPrint', ['foo']], [11, 'shouldPrint', ['foo']], [12, 'shouldPrint', ['bar']], [21, 'shouldPrint', ['foo']]] -> [True, True, False, False, False, True, True, True].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Hash map of last PRINT time. The only subtle point is what gets stored when a message is refused: nothing.

**Say this first (1 line):** "I store the time a message was last printed; print again when now minus that is at least 10; a refusal does not touch the stored time."

**Brute force:**
- Keep every print time of every message and compare against the last one. Same answers, unbounded memory. (It is the oracle in the code.)

**Optimal:**
- `last[message]`: time of the last successful print.
- `shouldPrint(m)`: if `m` is unseen, or `now - last[m] >= 10`, set `last[m] = now` and return True. Otherwise return False and leave `last` alone.
- Boundary rule: exactly 10 seconds later is allowed again. This is the same family as the hit counter of Q1, where an item exactly 300 seconds old has already expired: an interval of length L is half-open, so age L means "over".
- Tie rule: two identical messages at the same second: first prints, second is refused (age 0).

**Complexity:**
- O(1) per call (one dict lookup and one compare).
- Memory O(distinct messages seen). For an unbounded stream of distinct messages (stated concept): periodically drop entries older than 10 seconds, or keep a deque of `(time, message)` in arrival order and pop from the left while the head is older than 10 (each entry is dropped once, so O(1) amortised). Dropping an entry older than 10 is safe because the message would be allowed anyway.

**Dry run:** the example.

| t | message | last | now - last | result |
|---|---|---|---|---|
| 1 | foo | none | | True (last = 1) |
| 2 | bar | none | | True (last = 2) |
| 3 | foo | 1 | 2 | False |
| 8 | bar | 2 | 6 | False |
| 10 | foo | 1 | 9 | False |
| 11 | foo | 1 | 10 | True (last = 11) |
| 12 | bar | 2 | 10 | True (last = 12) |
| 21 | foo | 11 | 10 | True |

The "steady stream every 3 seconds" claim: arrivals at 0, 3, 6, 9 are refused after the print at 0; 12 is the first arrival with age >= 10, so it prints; then 15, 18, 21 are refused (ages 3, 6, 9) and 24 prints. Prints at 0, 12, 24 (and 36), as the code confirms.

**Code:**
```python
import random

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class NaiveLogger:                       # brute force: remember every print time
    def __init__(self, clock): self.clock = clock; self.times = {}
    def shouldPrint(self, message):
        now = self.clock(); ts = self.times.setdefault(message, [])
        if not ts or now - ts[-1] >= 10: ts.append(now); return True
        return False

class Logger:
    def __init__(self, clock): self.clock = clock; self.last = {}     # message -> time it was last PRINTED
    def shouldPrint(self, message):
        now = self.clock(); p = self.last.get(message)
        if p is None or now - p >= 10:   # exactly 10 later is allowed
            self.last[message] = now; return True
        return False                     # refused: do NOT touch the stored time

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = dict(init=[], ops=[[1, 'shouldPrint', ['foo']], [2, 'shouldPrint', ['bar']], [3, 'shouldPrint', ['foo']], [8, 'shouldPrint', ['bar']],
    [10, 'shouldPrint', ['foo']], [11, 'shouldPrint', ['foo']], [12, 'shouldPrint', ['bar']], [21, 'shouldPrint', ['foo']]])
want = [True, True, False, False, False, True, True, True]
assert run(Logger, **ex) == want == run(NaiveLogger, **ex)
print('example ->', run(Logger, **ex))

random.seed(16)
for case in range(600):
    t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.choice([0, 1, 3, 9, 10, 11])      # boundary-biased gaps around 10
        ops.append([t, 'shouldPrint', [random.choice('ab')]])
    assert run(Logger, [], ops) == run(NaiveLogger, [], ops)
print('600 random timed sequences match the naive reference')

# steady stream every 3 seconds prints at 0, 12, 24 ...
ops = [[t, 'shouldPrint', ['m']] for t in range(0, 40, 3)]
printed = [t for (t, _, _), ok in zip(ops, run(Logger, [], ops)) if ok]
assert printed[:3] == [0, 12, 24]
print('stream every 3 s prints at', printed)

# if a refusal wrongly refreshed the time, the message would never print again
class RefreshBug(Logger):
    def shouldPrint(self, message):
        now = self.clock(); p = self.last.get(message)
        ok = p is None or now - p >= 10
        self.last[message] = now
        return ok
bad = [t for (t, _, _), ok in zip(ops, run(RefreshBug, [], ops)) if ok]
assert bad == [0]
print('buggy refresh-on-refuse prints at', bad)

# same boundary family as the hit counter of Q1: an item of age exactly 10 (here) or 300 (there) is already expired, so the new print is allowed at age >= 10
assert run(Logger, [], [[0, 'shouldPrint', ['x']], [9, 'shouldPrint', ['x']], [10, 'shouldPrint', ['x']]]) == [True, False, True]
assert run(Logger, [], [[5, 'shouldPrint', ['x']], [5, 'shouldPrint', ['x']]]) == [True, False]      # same second
assert run(Logger, [], []) == []
assert run(Logger, [], [[0, 'shouldPrint', ['']]]) == [True]                                            # empty message is a message
print('edge asserts ok')
```

**Output (my run):**
```
example -> [True, True, False, False, False, True, True, True]
600 random timed sequences match the naive reference
stream every 3 s prints at [0, 12, 24, 36]
buggy refresh-on-refuse prints at [0]
edge asserts ok
```

**Edge cases:**
- Exactly 10 seconds apart: allowed (tested).
- 9 seconds apart: refused.
- Same message twice in one second: second refused.
- First message ever, at time 0: allowed (the unseen check is `is None`, not falsy on the time, because 0 is a legal time).
- An empty-string message is still a message.
- A refused message must NOT refresh its time; the buggy version prints once at time 0 and then never again on a steady stream (tested).

**Follow-ups:**
- *Memory bound (stated concept only):* see the complexity section; a deque in arrival order plus the dict, popping while `now - head_time >= 10` and deleting from the dict only if the dict still holds that same time.
- *Compare with the hit counter of Q1:* the same half-open boundary, but the logger keeps one timestamp per message, while the hit counter keeps counts per second in a window.
- *Thread-safety (stated concept only):* check-then-set on `last[m]` must be atomic, or two threads could both print the same message; a lock, or an atomic "set if absent or older" in a shared store.

**Common mistakes:**
- Updating the stored time on a refusal.
- Using `> 10` instead of `>= 10`.
- Using `if not last.get(m)` and mishandling a last time of 0.
- Reading `time.time()` instead of `clock()`.

---

### Q17 ⭐⭐ 🟢 Coordinate compression (dense ranks). `values` is a list of 0 <= len <= 10^5 integers with |value| <= 10^18 (duplicates and negatives allowed). Return `[ranks, distinct]`: `ranks[i]` is the 1-based DENSE rank of values[i] (equal values share one rank, the smallest value gets 1, and ranks have no gaps) and `distinct` the number of distinct values. Sort the distinct values once and look each element up (a dict from value to rank, or `bisect_left` on the sorted unique list); O(n log n). Explain why Fenwick trees and counting arrays need ranks (they index by position, and 10^18 cannot index an array), why ranks must start at 1 for a Fenwick tree (index 0 is unused), and the difference from the 'rank transform' with ties that skips numbers (competition ranking). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) oracle that counts, for each value, the distinct smaller values on small inputs. Example: values=[40, -5, 40, 7] -> [[3, 1, 3, 2], 3]; values=[] -> [[], 0]; values=[1000000000000000000, -1000000000000000000, 0] -> [[3, 1, 2], 3].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Coordinate compression. Replace big or sparse values by their order-preserving small ranks, so array-indexed structures (Fenwick tree, counting array) can be used.

**Say this first (1 line):** "Sort the distinct values once, give them ranks 1, 2, 3, and look each element up: O(n log n)."

**Brute force:**
- For each value, count how many distinct values are smaller and add 1. O(n^2). It is the oracle in the code.

**Optimal:**
- `uniq = sorted(set(values))`: O(n log n).
- `rank = {v: i + 1}`: the dict maps each value to its 1-based dense rank. Or use `bisect_left(uniq, v) + 1` (no dict, O(log n) per lookup; same answer).
- Return `[[rank[v] for v in values], len(uniq)]`.
- Dense rank means equal values share a rank, the smallest is 1 and there are no gaps; the largest rank equals `distinct`.
- Why Fenwick trees and counting arrays need this: they index by position, and a value like 10^18 cannot be an array index. Ranks keep the index range at most n.
- Why start at 1: a Fenwick tree is 1-indexed. Index 0 is unused (the update loop `i += i & -i` would never leave 0 and the query loop would not stop correctly).
- Difference from competition ranking ("1224"): there, ties share the first position and the next rank skips numbers, so the largest rank can exceed `distinct`. Dense ranking gives "1223".

**Complexity:**
- Time O(n log n) for the sort; building the dict and mapping is O(n). `bisect_left` version: O(n log n) for lookups too.
- Space O(n).
- Python integers have no overflow, so 10^18 is no problem, and sorting compares them exactly.

**Dry run:** `values = [40, -5, 40, 7]`.
- `set` gives {40, -5, 7}; sorted: `[-5, 7, 40]`.
- Ranks: -5 -> 1, 7 -> 2, 40 -> 3.
- Map the input: 40 -> 3, -5 -> 1, 40 -> 3, 7 -> 2. Result `[[3, 1, 3, 2], 3]`.

**Code:**
```python
import random
from bisect import bisect_left

def brute(values):                       # oracle: for each value count the distinct smaller values, O(n^2)
    ranks = [1 + len({u for u in values if u < v}) for v in values]
    return [ranks, len(set(values))]

def compress(values):
    uniq = sorted(set(values))           # sort the distinct values once
    rank = {v: i + 1 for i, v in enumerate(uniq)}     # 1-based dense rank
    return [[rank[v] for v in values], len(uniq)]

def compress_bisect(values):             # same with bisect_left on the sorted unique list
    uniq = sorted(set(values))
    return [[bisect_left(uniq, v) + 1 for v in values], len(uniq)]

for vals, want in [([40, -5, 40, 7], [[3, 1, 3, 2], 3]), ([], [[], 0]),
                   ([10**18, -10**18, 0], [[3, 1, 2], 3])]:
    assert compress(vals) == compress_bisect(vals) == brute(vals) == want
    print(vals, '->', compress(vals))

random.seed(17)
for case in range(800):
    vals = [random.randint(-6, 6) for _ in range(random.randint(0, 12))]
    assert compress(vals) == compress_bisect(vals) == brute(vals)
print('800 random cases match the O(n^2) oracle')

# competition ranking ("1224") differs: ties share a rank and the next rank skips
def competition(values):
    s = sorted(values); first = {}
    for i, v in enumerate(s): first.setdefault(v, i + 1)
    return [first[v] for v in values]
assert competition([40, 40, 7, 90]) == [2, 2, 1, 4] and compress([40, 40, 7, 90])[0] == [2, 2, 1, 3]
print('dense', compress([40, 40, 7, 90])[0], 'competition', competition([40, 40, 7, 90]))

# edge cases and size
assert compress([5]) == [[1], 1]
assert compress([2, 2, 2]) == [[1, 1, 1], 1]
assert compress([-1, -2, -3]) == [[3, 2, 1], 3]
big = [random.randint(-10**18, 10**18) for _ in range(10**5)]
r, d = compress(big)
assert d == len(set(big)) and min(r) == 1 and max(r) == d       # ranks fill 1..d with no gaps
print('n = 100000: distinct', d, 'ranks span 1..', max(r))
print('edge asserts ok')
```

**Output (my run):**
```
[40, -5, 40, 7] -> [[3, 1, 3, 2], 3]
[] -> [[], 0]
[1000000000000000000, -1000000000000000000, 0] -> [[3, 1, 2], 3]
800 random cases match the O(n^2) oracle
dense [2, 2, 1, 3] competition [2, 2, 1, 4]
n = 100000: distinct 100000 ranks span 1.. 100000
edge asserts ok
```

**Edge cases:**
- Empty list: `[[], 0]`.
- Single element: `[[1], 1]`.
- All equal: all ranks 1, distinct 1.
- Negatives and +-10^18: handled by sort (tested).
- Strictly decreasing input: ranks decreasing from n to 1.
- n = 10^5 with random huge values: ranks span exactly 1 to `distinct` (tested).

**Follow-ups:**
- *Where do I use it?* Counting smaller numbers after self and inversions with a Fenwick tree (inversions with a BIT is Q25 in this part; the merge sort version is Part 13 Q17), and any sweep over coordinates.
- *Why `sorted(set(...))` and not `sorted(values)`?* The set removes duplicates first, so the rank table has no gaps. Sorting with duplicates and enumerating would give gaps.
- *Do I need the dict?* No; `bisect_left` on `uniq` avoids it and keeps memory at one list, at O(log n) per lookup instead of O(1).

**Common mistakes:**
- 0-based ranks passed to a Fenwick tree.
- Enumerating the sorted list WITH duplicates, producing gaps.
- Mixing up dense ranking with competition ranking.
- Compressing the queries and the data separately, so the same value gets different ranks (compress them together).

---

### Q18 ⭐⭐ 🟡 Snapshot array. Implement class `SnapshotArray(length)` (1 <= length <= 5*10^4): every index starts at 0. `set(index, val)` changes the current array (returns None), `snap()` freezes the current contents and returns the snapshot id, with ids 0, 1, 2, ... in order, and `get(index, snap_id)` returns the value index had when snapshot `snap_id` was taken (snap_id is always an id already returned). Do not copy the array on `snap`: for each index keep a list of (snap_id, value) pairs recorded only when it is set, overwrite the last pair when the same index is set twice before a snapshot, and answer `get` with `bisect_right` on the snap ids (the answer is the last pair with id <= snap_id; the initial pair (0, 0) guarantees one exists). `snap` is O(1), `set` O(1), `get` O(log k). Up to 5*10^4 operations. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[3], ops=[['set', [0, 5]], ['snap', []], ['set', [0, 6]], ['get', [0, 0]], ['set', [1, 9]], ['set', [1, 8]], ['snap', []], ['get', [1, 0]], ['get', [1, 1]], ['get', [0, 1]], ['get', [2, 1]]] -> [null, 0, null, 5, null, null, 1, 0, 8, 6, 0].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Persistent per-index history plus binary search. Do not copy the array on `snap`; record only the changes, tagged with the epoch, and binary search the epoch at query time.

**Say this first (1 line):** "For each index I keep a sorted list of (snap id, value) pairs written only when it is set, and `get` is a `bisect_right` on the snap ids."

**Brute force:**
- `snap` copies the whole array, `get` reads `snaps[snap_id][index]`. `snap` costs O(length), so 5*10^4 snaps on a 5*10^4 array is 2.5*10^9 stored integers. Too much memory and time.

**Optimal:**
- `sid`: the id the NEXT `snap()` will return (the current epoch, starting at 0).
- Per index two parallel lists, `ids[i]` (epochs) and `vals[i]` (values), starting with the pair `(0, 0)`.
- `set(i, v)`: if the last epoch recorded for `i` equals `sid`, overwrite the last value (set twice before a snapshot); otherwise append `(sid, v)`.
- `snap()`: `sid += 1`, return the old `sid`. O(1), nothing copied.
- `get(i, s)`: `bisect_right(ids[i], s) - 1` is the last pair with epoch <= `s`; return its value. The initial pair guarantees the position is >= 0.
- Why that pair is right: a pair stamped epoch e means "set during epoch e", i.e. before snapshot e was taken (snapshot e freezes everything written in epochs 0..e). So the value at snapshot s is the newest write with epoch <= s.

**Complexity:**
- `set` O(1), `snap` O(1), `get` O(log k) where k is the number of recorded epochs for that index.
- Space O(length + number of sets), not O(length * snaps).

**Dry run:** first example, `length = 3`. `sid` starts 0; `ids[0] = [0]`, `vals[0] = [0]` etc.

| call | action | returns |
|---|---|---|
| set(0, 5) | last epoch of index 0 is 0 = sid: overwrite: vals[0] = [5] | None |
| snap() | sid becomes 1 | 0 |
| set(0, 6) | last epoch 0 != 1: append: ids [0,1], vals [5,6] | None |
| get(0, 0) | bisect_right([0,1], 0) = 1, pair 0: 5 | 5 |
| set(1, 9) | append (1, 9): ids[1] = [0,1], vals [0,9] | None |
| set(1, 8) | same epoch: overwrite: vals [0,8] | None |
| snap() | sid becomes 2 | 1 |
| get(1, 0) | bisect_right([0,1], 0) = 1, pair 0: 0 | 0 |
| get(1, 1) | bisect_right([0,1], 1) = 2, pair 1: 8 | 8 |
| get(0, 1) | bisect_right([0,1], 1) = 2, pair 1: 6 | 6 |
| get(2, 1) | ids[2] = [0], bisect_right = 1, pair 0: 0 | 0 |

**Code:**
```python
import random
from bisect import bisect_right

class NaiveSnapshot:                     # brute force: copy the whole array on snap, O(length) per snap
    def __init__(self, length): self.cur = [0] * length; self.snaps = []
    def set(self, index, val): self.cur[index] = val
    def snap(self): self.snaps.append(list(self.cur)); return len(self.snaps) - 1
    def get(self, index, snap_id): return self.snaps[snap_id][index]

class SnapshotArray:
    def __init__(self, length):
        self.ids = [[0] for _ in range(length)]     # per index: snap ids at which it was set (initial 0)
        self.vals = [[0] for _ in range(length)]    # parallel values; initial pair (0, 0)
        self.sid = 0                                # id the NEXT snap() will return = current epoch
    def set(self, index, val):
        ids, vals = self.ids[index], self.vals[index]
        if ids[-1] == self.sid: vals[-1] = val      # same epoch: overwrite, no new pair
        else: ids.append(self.sid); vals.append(val)
    def snap(self):
        self.sid += 1; return self.sid - 1          # O(1): nothing is copied
    def get(self, index, snap_id):
        ids = self.ids[index]
        return self.vals[index][bisect_right(ids, snap_id) - 1]   # last pair with id <= snap_id

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[3], ops=[['set', [0, 5]], ['snap', []], ['set', [0, 6]], ['get', [0, 0]], ['set', [1, 9]], ['set', [1, 8]],
    ['snap', []], ['get', [1, 0]], ['get', [1, 1]], ['get', [0, 1]], ['get', [2, 1]]])
want = [None, 0, None, 5, None, None, 1, 0, 8, 6, 0]
assert run(SnapshotArray, **ex) == want == run(NaiveSnapshot, **ex)
print('example ->', run(SnapshotArray, **ex))

random.seed(18)
for case in range(600):
    n = random.randint(1, 4); ops = []; snaps = 0
    for _ in range(random.randint(0, 40)):
        r = random.random()
        if r < 0.4: ops.append(['set', [random.randrange(n), random.randint(0, 9)]])
        elif r < 0.6: ops.append(['snap', []]); snaps += 1
        elif snaps: ops.append(['get', [random.randrange(n), random.randrange(snaps)]])
    assert run(SnapshotArray, [n], ops) == run(NaiveSnapshot, [n], ops)
print('600 random sequences match the naive reference')

# memory: pairs stored = number of distinct (index, epoch) sets, not length * snaps
s = SnapshotArray(50000)
for i in range(1000): s.set(i % 7, i); s.snap()
pairs = sum(len(x) for x in s.ids)
assert pairs == 50000 + 999                 # 1000 sets, but the very first one overwrote its index's initial (0, 0) pair
print('pairs stored', pairs, 'versus a full copy per snap', 50000 * 1000)

# edge cases
s = SnapshotArray(1); assert s.snap() == 0 and s.get(0, 0) == 0           # snapshot of untouched array
s.set(0, 0); s.set(0, 0); assert s.snap() == 1 and s.get(0, 1) == 0
s.set(0, 4); s.set(0, 5); assert s.get(0, 1) == 0 and s.snap() == 2 and s.get(0, 2) == 5   # double set in one epoch
assert s.get(0, 0) == 0 and len(s.ids[0]) == 3                              # pairs for epochs 0, 1 and 2
print('pairs for index 0:', list(zip(s.ids[0], s.vals[0])))
print('edge asserts ok')
```

**Output (my run):**
```
example -> [None, 0, None, 5, None, None, 1, 0, 8, 6, 0]
600 random sequences match the naive reference
pairs stored 50999 versus a full copy per snap 50000000
pairs for index 0: [(0, 0), (1, 0), (2, 5)]
edge asserts ok
```

**Edge cases:**
- `get` on an index never set: the initial `(0, 0)` pair answers 0.
- Snapshot of an untouched array: id 0, every get returns 0 (tested).
- Setting the same value again in a new epoch still appends a pair; it is harmless (tested), and skipping it when the value equals the last one is an optional saving.
- Two sets of one index before a snapshot keep only the last (tested; pair count printed).
- `bisect_right` (not `bisect_left`): the pair stamped exactly `snap_id` must be included.
- `length = 1` and up to 5*10^4 operations: fine.

**Follow-ups:**
- *Could I store the full array only every k snaps?* Yes, but per-index change lists are simpler and already optimal for sparse updates.
- *Worst case:* every index changes every epoch, so memory is O(length * snaps) anyway; that is inherent to storing the history.
- *Thread-safety (stated concept only):* `set` and `snap` must not interleave in a way that lets a set land in the wrong epoch; a lock around both, or a copy-on-write structure.

**Common mistakes:**
- Copying the array on every `snap`.
- Using `bisect_left` and missing the pair equal to `snap_id`.
- Appending a duplicate pair for the same epoch, so `bisect` finds the older value.
- Returning `snap_id` as `len(snaps)` after incrementing (off by one).

---

### Q19 ⭐⭐ 🟡 News feed with heaps (design Twitter). Implement class `Twitter(feed_size)` with `postTweet(user, tweet_id)`, `follow(a, b)`, `unfollow(a, b)` and `getNewsFeed(user)`. A user always sees their own tweets. `getNewsFeed` returns the ids of the at most `feed_size` most recent tweets posted by the user or anyone the user follows, newest first, where recency is the global order of the `postTweet` calls (tweet ids are arbitrary labels, not an ordering). `follow(a, b)` with a == b and `unfollow` of someone not followed do nothing; following twice is the same as once; `unfollow` stops that person's tweets (past and future) from appearing. The mutators return None. Keep each user's tweets as a list in posting order and merge the newest-first lists of the user and followees with a heap (`heapq.merge` or a heap of (negative post number, user, index)); a feed costs O(f + k log f) for f followees and k = feed_size, not a sort of all tweets. 1 <= feed_size <= 20 and up to 3*10^4 operations. Say as a stated concept how a real service would pre-compute feeds (fan-out on write versus on read). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[3], ops=[['postTweet', [1, 5]], ['getNewsFeed', [1]], ['follow', [1, 2]], ['postTweet', [2, 6]], ['getNewsFeed', [1]], ['postTweet', [2, 7]], ['postTweet', [1, 8]], ['getNewsFeed', [1]], ['unfollow', [1, 2]], ['getNewsFeed', [1]]] -> [null, [5], null, null, [6, 5], null, null, [8, 7, 6], null, [8, 5]].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** K-way merge with a heap (Part 8 Q10 style). Each user's tweets are already in posting order, so the feed is a merge of newest-first lists that stops after `k` items.

**Say this first (1 line):** "Recency is one global post counter; each user keeps a list in posting order, and the feed is a heap merge of the newest-first lists of the user and followees, stopped after feed_size pops."

**Brute force:**
- One global list of all tweets. For a feed, scan from newest to oldest, keep tweets whose author is the user or a followee, stop after `k`. O(total tweets) per feed in the worst case (it is the oracle).

**Optimal:**
- `clock`: global post number, +1 per `postTweet`. Tweet ids are labels (the example posts 5, 6, 7, 8 but another run could post 9, 2, 5), so recency comes only from the counter.
- `tweets[user]`: list of `(post number, tweet id)`, oldest first. `following[user]`: set of followees, never containing the user.
- `follow(a, b)`: ignore when `a == b`; set add (twice is the same as once). `unfollow(a, b)`: `discard` (a no-op when not followed). Past and future tweets of `b` leave and re-enter the feed at once, because the feed is computed from the current follow set.
- `getNewsFeed(u)`: sources = followees plus `u`. Push `(-newest post number, user, index of newest)` for every source that has tweets, heapify. Pop up to `k` times: take the tweet, then push that user's next-older tweet. Ties cannot occur because post numbers are unique.

**Complexity:**
- `postTweet`, `follow`, `unfollow`: O(1) average.
- `getNewsFeed`: O(f) to build and heapify, plus up to k pops and pushes at O(log f) each: O(f + k log f), independent of how many tweets exist. With k <= 20 this is tiny.
- Space O(tweets + follow edges).
- Stated concept: a real service pre-computes feeds. Fan-out on write pushes each new tweet into every follower's stored feed (fast reads, slow posts for users with millions of followers); fan-out on read merges at request time as here (cheap writes, costly reads); large systems mix the two, using fan-out on write for ordinary users and fan-out on read for celebrity accounts.

**Dry run:** first example, `feed_size = 3`.

| call | state | returns |
|---|---|---|
| postTweet(1, 5) | tweet 5 gets post number 1 | None |
| getNewsFeed(1) | sources {1}: [5] | [5] |
| follow(1, 2) | following[1] = {2} | None |
| postTweet(2, 6) | post number 2 | None |
| getNewsFeed(1) | heap (-1, user 1), (-2, user 2): pop 6, pop 5 | [6, 5] |
| postTweet(2, 7) | post number 3 | None |
| postTweet(1, 8) | post number 4 | None |
| getNewsFeed(1) | newest per source: user 1 -> 8 (4), user 2 -> 7 (3). pop 8, pop 7, push user 2's 6 (2) vs user 1's 5 (1): pop 6 | [8, 7, 6] |
| unfollow(1, 2) | following[1] = {} | None |
| getNewsFeed(1) | only user 1: 8, 5 | [8, 5] |

**Code:**
```python
import heapq, random
from collections import defaultdict

class NaiveTwitter:                      # brute force: one global list, scan newest to oldest, filter by author
    def __init__(self, feed_size): self.k = feed_size; self.all = []; self.f = defaultdict(set)
    def postTweet(self, user, tweet_id): self.all.append((user, tweet_id))
    def follow(self, a, b):
        if a != b: self.f[a].add(b)
    def unfollow(self, a, b): self.f[a].discard(b)
    def getNewsFeed(self, user):
        seen = self.f[user] | {user}
        return [t for u, t in reversed(self.all) if u in seen][:self.k]

class Twitter:
    def __init__(self, feed_size):
        self.k = feed_size
        self.clock = 0                              # global post number: the ONLY recency order
        self.tweets = defaultdict(list)             # user -> [(post number, tweet id)] oldest first
        self.following = defaultdict(set)           # user -> set of followees (never contains self)
    def postTweet(self, user, tweet_id):
        self.clock += 1
        self.tweets[user].append((self.clock, tweet_id))
    def follow(self, a, b):
        if a != b: self.following[a].add(b)         # set makes a double follow a no-op
    def unfollow(self, a, b):
        self.following[a].discard(b)                # not followed: no-op
    def getNewsFeed(self, user):
        heap = []
        for u in self.following[user] | {user}:     # f + 1 sources
            lst = self.tweets.get(u)
            if lst: heap.append((-lst[-1][0], u, len(lst) - 1))   # newest tweet of u; negative so the min-heap pops newest
        heapq.heapify(heap)
        out = []
        while heap and len(out) < self.k:           # k pops, each O(log f)
            negn, u, i = heapq.heappop(heap)
            out.append(self.tweets[u][i][1])
            if i:                                    # push u's next-older tweet
                heapq.heappush(heap, (-self.tweets[u][i - 1][0], u, i - 1))
        return out

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[3], ops=[['postTweet', [1, 5]], ['getNewsFeed', [1]], ['follow', [1, 2]], ['postTweet', [2, 6]], ['getNewsFeed', [1]],
    ['postTweet', [2, 7]], ['postTweet', [1, 8]], ['getNewsFeed', [1]], ['unfollow', [1, 2]], ['getNewsFeed', [1]]])
want = [None, [5], None, None, [6, 5], None, None, [8, 7, 6], None, [8, 5]]
assert run(Twitter, **ex) == want == run(NaiveTwitter, **ex)
print('example ->', run(Twitter, **ex))

random.seed(19)
for case in range(800):
    k = random.randint(1, 5); ops = []; nxt = 100
    for _ in range(random.randint(0, 50)):
        r = random.random(); u = random.randint(1, 4); v = random.randint(1, 4)
        if r < 0.3: ops.append(['postTweet', [u, random.randint(0, 9)]])      # tweet ids repeat: they are labels, not an order
        elif r < 0.45: ops.append(['follow', [u, v]])
        elif r < 0.6: ops.append(['unfollow', [u, v]])
        else: ops.append(['getNewsFeed', [u]])
    assert run(Twitter, [k], ops) == run(NaiveTwitter, [k], ops), ops
print('800 random sequences match the naive reference')

# edge cases
t = Twitter(2)
assert t.getNewsFeed(1) == []                                  # nothing posted
t.follow(1, 1); t.postTweet(1, 9); assert t.getNewsFeed(1) == [9]   # self-follow does nothing: no duplicates
t.follow(1, 2); t.follow(1, 2); t.postTweet(2, 3); assert t.getNewsFeed(1) == [3, 9]
t.unfollow(1, 2); t.unfollow(1, 2); t.unfollow(1, 5); assert t.getNewsFeed(1) == [9]   # repeated / unknown unfollow is a no-op
t.follow(1, 2); assert t.getNewsFeed(1) == [3, 9]               # old tweets reappear on re-follow
t.postTweet(2, 1); t.postTweet(2, 0); assert t.getNewsFeed(1) == [0, 1]   # feed_size cap, ids 0 and 1 are not an order
# many tweets by one user: only k heap pops are needed
t = Twitter(3)
for i in range(10000): t.postTweet(1, i)
assert t.getNewsFeed(1) == [9999, 9998, 9997]
print('edge asserts ok')
```

**Output (my run):**
```
example -> [None, [5], None, None, [6, 5], None, None, [8, 7, 6], None, [8, 5]]
800 random sequences match the naive reference
edge asserts ok
```

**Edge cases:**
- A user with no tweets and no followees: empty feed.
- `follow(a, a)`: ignored; own tweets still appear exactly once (tested).
- Follow twice, unfollow twice, unfollow a stranger: all harmless (tested).
- Re-following brings the old tweets back (tested).
- Fewer than `feed_size` tweets exist: return what there is.
- Tweet ids 0 and 1 posted after 3 and 9 must come first: ids are not an ordering (tested with random repeated ids too).
- A user with 10,000 tweets: only the last k are touched (tested).

**Follow-ups:**
- *Why not sort all tweets?* O(T log T) per feed. The merge touches only f + k entries.
- *`heapq.merge`:* `heapq.merge(*[reversed(lst) for lst in lists], key=..., reverse=...)` can do the same lazily; the explicit heap makes the "stop after k" and the index bookkeeping visible.
- *Thread-safety (stated concept only):* the global counter increment and the list append in `postTweet` must be one atomic step so post numbers match list order; a lock around each mutator, and readers need a consistent snapshot of the follow set.

**Common mistakes:**
- Using the tweet id as the recency order.
- Letting a user follow themselves and then showing their tweets twice.
- Pushing all tweets of all followees onto the heap (O(T log T)).
- Forgetting to include the user's own tweets.
- Keeping an unfollowed user's old tweets in the feed.

---

### Q20 ⭐⭐ 🟡 Strongly connected components with Kosaraju. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges`, a list of directed [u, v] pairs (0 <= len <= 2*10^5; repeats and self loops allowed). Return the list of strongly connected components (maximal sets of nodes that can all reach each other), each component sorted ascending and the list of components sorted by smallest member. Run an iterative DFS to get the finish order, then an iterative DFS on the reversed graph in decreasing finish order; recursion is NOT allowed because a path graph of 10^5 nodes would exceed CPython's default recursion limit of 1000 (see Part 9 Q6 for the explicit-stack DFS). Say why the first pass order works (the component finishing last in the first pass is a source of the condensation DAG), and what the condensation is. The Tarjan one-pass version is Q41. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a closure-based oracle (Floyd-Warshall reachability: u and v are together exactly when each reaches the other) on small inputs. Example: n=5, edges=[[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [[0, 1, 2], [3], [4]]; n=3, edges=[[0, 0]] -> [[0], [1], [2]]; n=4, edges=[[0, 1], [1, 0], [2, 3], [3, 2], [1, 2]] -> [[0, 1], [2, 3]].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** Strongly connected components with Kosaraju: two DFS passes, both written with an explicit stack because recursion would break on a 10^5-node path (Part 9 Q6 shows the explicit-stack DFS).

**Say this first (1 line):** "Pass 1: DFS on the graph recording finish order. Pass 2: DFS on the reversed graph in decreasing finish order; each tree of pass 2 is one component."

**Brute force:**
- Compute reachability from every node (Floyd-Warshall or a BFS per node), then group u and v when each reaches the other. O(n^3) or O(n (n + m)); far too slow at 10^5 nodes. It is the oracle in the code.

**Optimal:**
- Build `g` and the reversed graph `rg`.
- Pass 1: for each unvisited start, run an iterative DFS with a stack of `(node, next neighbour index)`. When a node has no neighbours left, append it to `order` (it finishes).
- Pass 2: go through `order` backwards. For each node not yet assigned, run a DFS (a plain stack is fine, only reachability matters) over `rg` through unassigned nodes. Everything reached forms one component.
- Finally sort each component, then sort components by their smallest member.
- Why it works: take the component whose node finished LAST in pass 1. It is a source of the condensation, so nothing outside reaches it; in the reversed graph it has no way out to other components. So the reversed DFS from that node collects exactly this component. Remove it, and the next-latest remaining finisher is a source of what is left, and so on.
- The condensation is the graph obtained by shrinking every SCC to one node. It is always a DAG (a cycle between components would merge them), which is what makes the finish-order argument work.
- Self loops and repeated edges change nothing: a self loop leaves a node in its own component; duplicates are ignored by the visited marks.

**Complexity:**
- Time O(n + m): each node and edge is processed a constant number of times in each pass, plus the final sort O(n log n).
- Space O(n + m) for the two adjacency lists, the stacks and the order.
- The stack lives in a Python list on the heap, so depth is not limited by the recursion limit (1000 by default).

**Dry run:** `n = 5`, edges 0->1, 1->2, 2->0, 1->3, 3->4.
- Pass 1 from 0: go to 1, go to 2; 2's only neighbour 0 is seen, so 2 finishes. Back at 1: next neighbour 3, then 4; 4 finishes, 3 finishes, 1 finishes, 0 finishes. `order = [2, 4, 3, 1, 0]`.
- Reversed edges: 1->0, 2->1, 0->2, 3->1, 4->3.
- Pass 2 in reverse order: start 0. `rg[0] = [2]`, `rg[2] = [1]`, `rg[1] = [0]` (seen). Component {0, 2, 1}. Next unassigned in order: 3. `rg[3] = [1]` is assigned, so {3}. Then 4: `rg[4] = [3]` assigned, so {4}.
- Sorted result `[[0, 1, 2], [3], [4]]`.

**Code:**
```python
import random

def brute(n, edges):                     # oracle: Floyd-Warshall reachability, u ~ v iff each reaches the other
    reach = [[i == j for j in range(n)] for i in range(n)]
    for u, v in edges: reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]: reach[i][j] = True
    seen = [False] * n; out = []
    for i in range(n):
        if not seen[i]:
            comp = [j for j in range(n) if reach[i][j] and reach[j][i]]
            for j in comp: seen[j] = True
            out.append(comp)
    return out

def kosaraju(n, edges):
    g = [[] for _ in range(n)]; rg = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v); rg[v].append(u)
    # pass 1: iterative DFS on g, record nodes in order of FINISH
    seen = [False] * n; order = []
    for s in range(n):
        if seen[s]: continue
        seen[s] = True
        stack = [(s, 0)]                        # (node, index of next neighbour to try)
        while stack:
            u, i = stack.pop()
            if i < len(g[u]):
                stack.append((u, i + 1))        # come back to u for its next neighbour
                v = g[u][i]
                if not seen[v]:
                    seen[v] = True; stack.append((v, 0))
            else:
                order.append(u)                 # all neighbours done: u finishes now
    # pass 2: iterative DFS on the reversed graph in decreasing finish order; each tree = one SCC
    comp_of = [-1] * n; comps = []
    for s in reversed(order):
        if comp_of[s] != -1: continue
        comp_of[s] = len(comps); members = [s]; stack = [s]
        while stack:
            u = stack.pop()
            for v in rg[u]:
                if comp_of[v] == -1:
                    comp_of[v] = len(comps); members.append(v); stack.append(v)
        comps.append(sorted(members))
    return sorted(comps, key=lambda c: c[0])

cases = [(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]], [[0, 1, 2], [3], [4]]),
         (3, [[0, 0]], [[0], [1], [2]]),
         (4, [[0, 1], [1, 0], [2, 3], [3, 2], [1, 2]], [[0, 1], [2, 3]])]
for n, e, want in cases:
    assert kosaraju(n, e) == brute(n, e) == want
    print(n, e, '->', kosaraju(n, e))

random.seed(20)
for case in range(600):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 14))]   # repeats and self loops allowed
    assert kosaraju(n, edges) == brute(n, edges), (n, edges)
print('600 random graphs match the Floyd-Warshall oracle')

# deep graphs: a path of 10^5 nodes would blow the recursion limit, the explicit stack does not
N = 10**5
path = [[i, i + 1] for i in range(N - 1)]
res = kosaraju(N, path); assert len(res) == N and res[0] == [0] and res[-1] == [N - 1]
cyc = path + [[N - 1, 0]]
res = kosaraju(N, cyc); assert res == [list(range(N))]
print('path of', N, '->', len(kosaraju(N, path)), 'components; same path closed into one cycle ->', len(res), 'component')

# edge cases
assert kosaraju(1, []) == [[0]]
assert kosaraju(2, []) == [[0], [1]]
assert kosaraju(3, [[0, 1], [0, 1], [1, 0]]) == [[0, 1], [2]]          # repeated edges
assert kosaraju(3, [[2, 1], [1, 0]]) == [[0], [1], [2]]                 # DAG: every node alone
assert kosaraju(4, [[3, 2], [2, 1], [1, 0], [0, 3]]) == [[0, 1, 2, 3]] # unsorted labels in one cycle
print('edge asserts ok')
```

**Output (my run):**
```
5 [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [[0, 1, 2], [3], [4]]
3 [[0, 0]] -> [[0], [1], [2]]
4 [[0, 1], [1, 0], [2, 3], [3, 2], [1, 2]] -> [[0, 1], [2, 3]]
600 random graphs match the Floyd-Warshall oracle
path of 100000 -> 100000 components; same path closed into one cycle -> 1 component
edge asserts ok
```

**Edge cases:**
- No edges: every node is its own component.
- Single node; a self loop only (`[[0, 0]]`).
- Repeated edges (tested).
- A DAG: n components (tested).
- One big cycle with unsorted labels (tested); the output is sorted inside and across components.
- Path of 10^5 nodes and the same path closed into a cycle (tested, the explicit stack never hits the recursion limit).
- Disconnected graph: both loops start from every unvisited node.

**Follow-ups:**
- *Why reversed graph?* In the reversed graph the component of the last finisher cannot leak into other components, so one DFS stays inside it. A forward DFS from it would escape into everything it can reach.
- *Tarjan's version (Q41):* one DFS with `low` values and a component stack; same O(n + m), no reversed graph.
- *Use of SCCs:* condense to a DAG and run topological DP (2-SAT, minimum number of nodes to reach everything is the number of source components).

**Common mistakes:**
- Using recursion and crashing on a deep path (CPython's limit is 1000).
- Running pass 2 on the original graph instead of the reversed graph.
- Processing pass 2 in finish order instead of decreasing finish order.
- Appending to `order` at discovery instead of at finish.
- Forgetting to sort members and components for the required output.

---

### Q21 ⭐⭐ 🟡 Lexicographically smallest topological order. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` a list of [a, b] meaning a must come before b (0 <= len <= 2*10^5; repeats allowed). Return the topological order that is smallest when compared as a list (the first node as small as possible, then the second, and so on), or [] when a cycle makes any order impossible. Kahn's algorithm with a min-heap of the nodes whose in-degree is 0 (a plain FIFO queue gives a valid order but not the smallest); O((n + m) log n). Explain why taking the smallest available node at each step is optimal here (the choice set is exactly the available nodes) and why it is NOT the right rule for 'put label 0 as early as possible, then label 1, and so on' (for that goal reverse the graph, take the LARGEST available node each time, and reverse the result). Part 9 Q9 gives any valid order and Part 9 Q33 builds the order from word constraints; this question fixes the tie rule. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that tries all permutations in lexicographic order for n <= 6 and keeps the first valid one on small inputs. Example: n=4, edges=[[3, 0], [3, 1], [1, 2]] -> [3, 0, 1, 2]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> []; n=3, edges=[] -> [0, 1, 2].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** Topological sort (Kahn) with a min-heap as the ready set. The tie rule is the whole question.

**Say this first (1 line):** "Kahn's algorithm, but the ready set is a min-heap, so each step takes the smallest node with in-degree 0; a cycle shows up as fewer than n nodes output."

**Brute force:**
- Try all n! permutations in lexicographic order and keep the first that respects every edge. O(n! * (n + m)). It is my oracle for n <= 6.

**Optimal:**
- Count in-degrees (repeated edges count twice and are decremented twice, so it stays consistent).
- Put every in-degree-0 node in a min-heap. Pop the smallest, append it, decrement its neighbours, push any that reach 0.
- If the output has fewer than n nodes, a cycle blocks the rest: return [].
- Why smallest-first is optimal: the first element of any valid order must be an available node (in-degree 0). So the smallest possible first element is the smallest available node. After removing it the rest is the same problem on the residual graph, and its choice set is again exactly its available nodes. A FIFO queue is valid but not smallest.
- Why it is NOT the rule for "label 0 as early as possible, then label 1, ...": that goal compares the position vector (pos[0], pos[1], ...), not the order list. Example n=3, edge 2 -> 0: smallest-first gives [1, 2, 0] (label 0 at position 2) but [2, 0, 1] puts label 0 at position 1. The fix: reverse the graph, take the LARGEST available node each time, reverse the result. The code checks both rules against brute force.

**Complexity:**
- Time O((n + m) log n): each node is pushed and popped once (log n each), each edge decrements once.
- Space O(n + m) for adjacency lists, in-degrees and heap.
- Iterative, so n = 10^5 is no recursion problem.

**Dry run:** n=4, edges 3->0, 3->1, 1->2.
- in-degrees: 0:1, 1:1, 2:1, 3:0. Heap [3].
- Pop 3, order [3]. 0 and 1 drop to 0, heap [0, 1].
- Pop 0, order [3, 0]. No out-edges.
- Pop 1, order [3, 0, 1]. Node 2 drops to 0, push.
- Pop 2. Order [3, 0, 1, 2], length 4 = n, so return it.
- Cycle example 0->1->2->0: no node has in-degree 0, heap empty at the start, output length 0 != 3, return [].

**Code:**
```python
import heapq, random
from itertools import permutations

def optimal(n, edges):
    """Kahn's algorithm with a min-heap: lexicographically smallest topological order, or [] on a cycle."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in edges:                      # repeated edges are counted twice in indeg and twice in adj: consistent
        adj[a].append(b)
        indeg[b] += 1
    heap = [v for v in range(n) if indeg[v] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        v = heapq.heappop(heap)             # smallest available node
        order.append(v)
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                heapq.heappush(heap, w)
    return order if len(order) == n else []

def brute(n, edges):
    """Try permutations in lexicographic order, keep the first that respects every edge."""
    for p in permutations(range(n)):        # itertools yields lexicographic order for a sorted input
        pos = {v: i for i, v in enumerate(p)}
        if all(pos[a] < pos[b] for a, b in edges):
            return list(p)
    return []

def labels_early(n, edges):
    """'label 0 as early as possible, then label 1, ...': reverse the graph, take the LARGEST available, reverse."""
    adj = [[] for _ in range(n)]
    outdeg = [0] * n
    for a, b in edges:
        adj[b].append(a)                    # reversed edge
        outdeg[a] += 1
    heap = [-v for v in range(n) if outdeg[v] == 0]
    heapq.heapify(heap)
    rev = []
    while heap:
        v = -heapq.heappop(heap)            # largest available in the reversed graph
        rev.append(v)
        for w in adj[v]:
            outdeg[w] -= 1
            if outdeg[w] == 0:
                heapq.heappush(heap, -w)
    return rev[::-1] if len(rev) == n else []

def labels_brute(n, edges):
    """Minimise the vector (position of 0, position of 1, ...) over all valid orders."""
    best = None
    for p in permutations(range(n)):
        pos = [0] * n
        for i, v in enumerate(p):
            pos[v] = i
        if all(pos[a] < pos[b] for a, b in edges):
            if best is None or pos < best[0]:
                best = (pos, list(p))
    return best[1] if best else []

# examples from the prompt
assert optimal(4, [[3, 0], [3, 1], [1, 2]]) == [3, 0, 1, 2]
assert optimal(3, [[0, 1], [1, 2], [2, 0]]) == []
assert optimal(3, []) == [0, 1, 2]
print('examples:', optimal(4, [[3, 0], [3, 1], [1, 2]]), optimal(3, [[0, 1], [1, 2], [2, 0]]), optimal(3, []))

# why the other goal needs the reverse trick: smallest-first is NOT optimal for 'label 0 early'
n, e = 3, [[2, 0]]
print('smallest-first:', optimal(n, e), ' label-0-early (brute):', labels_brute(n, e), ' reverse+largest:', labels_early(n, e))
assert optimal(n, e) == [1, 2, 0] and labels_brute(n, e) == [2, 0, 1] == labels_early(n, e)

# edge cases
assert optimal(1, []) == [0]
assert optimal(1, [[0, 0]]) == []                       # self loop is a cycle
assert optimal(3, [[0, 1], [0, 1], [1, 2]]) == [0, 1, 2]  # repeated edges
assert optimal(2, [[1, 0]]) == [1, 0]

random.seed(21)
cases = 0
for _ in range(600):
    n = random.randint(1, 6)
    m = random.randint(0, 9)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    if random.random() < 0.7:                           # mostly acyclic: orient along a hidden permutation
        perm = list(range(n)); random.shuffle(perm)
        rank = {v: i for i, v in enumerate(perm)}
        edges = [[a, b] if rank[a] < rank[b] else [b, a] for a, b in edges if a != b]
    assert optimal(n, edges) == brute(n, edges), (n, edges)
    assert labels_early(n, edges) == labels_brute(n, edges), (n, edges)
    cases += 1
print('random cross-check ok:', cases, 'cases (n <= 6), both rules')

# size: a path 0 <- 1 <- ... (reverse chain) and a wide fan; iterative so no recursion issue
N = 10**5
chain = [[i + 1, i] for i in range(N - 1)]
assert optimal(N, chain) == list(range(N - 1, -1, -1))
fan = [[0, i] for i in range(1, N)]
assert optimal(N, fan) == list(range(N))
print('n = 10^5 chain and fan ok')
```

**Output (my run):**
```
examples: [3, 0, 1, 2] [] [0, 1, 2]
smallest-first: [1, 2, 0]  label-0-early (brute): [2, 0, 1]  reverse+largest: [2, 0, 1]
random cross-check ok: 600 cases (n <= 6), both rules
n = 10^5 chain and fan ok
```

**Edge cases:**
- No edges: [0, 1, ..., n-1]. n = 1: [0].
- A self loop (a, a) is a cycle: [].
- Repeated edges: harmless as shown. A cycle in only part of the graph still returns [] (the whole answer is empty, not a partial order).
- Edge endpoints are within 0..n-1; isolated nodes are just ready from the start.

**Follow-ups:**
- Lexicographically smallest for a different tie rule, say the largest label first? Use a max-heap (push negatives in Python).
- Why not DFS? A DFS finish-time order gives a valid order but not the smallest one without extra work; Kahn with a heap is the natural fit. Part 9 Q9 has the any-order version and Part 9 Q33 builds the order from word constraints.
- Is the order unique? Only when the graph has a Hamiltonian path in the DAG: every step has exactly one ready node.

**Common mistakes:**
- Using a deque and calling it "smallest".
- Applying smallest-first to the "label 0 earliest" goal.
- Forgetting the cycle check (output shorter than n).
- Using `heapq` on a list that is not heapified after building it from a comprehension.

---

### Q22 ⭐⭐ 🟡 Cheapest path with one half-price edge. `n` nodes 0..n-1 (2 <= n <= 10^4) and `edges`, a list of directed [u, v, w] with integer cost 1 <= w <= 10^6 (0 <= len <= 5*10^4). Travel from node 0 to node n-1. You hold ONE coupon that you may use on at most one edge of your path, making that edge cost w // 2 (integer floor division). Return the minimum total cost, or -1 when n-1 is unreachable. Run Dijkstra on the layered state (node, coupon_used in {0, 1}) with a heap and lazy stale-entry skipping: the answer is min(dist[n-1][0], dist[n-1][1]). Say why a plain Dijkstra on the original graph cannot answer it, why positive weights keep the best walk simple, and why the same state-expansion idea handles 'at most k coupons' with k + 1 layers. The 'at most k stops' flight question is Part 9 Q34 and is not repeated. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a brute-force oracle that enumerates every simple path and subtracts the best single saving w - w // 2 on small inputs. Example: n=3, edges=[[0, 1, 10], [1, 2, 10], [0, 2, 25]] -> 12; n=3, edges=[[0, 1, 4]] -> -1; n=4, edges=[[0, 1, 1], [1, 3, 1], [0, 2, 3], [2, 3, 3]] -> 1.
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** Dijkstra on a layered state graph (node, coupons used). Positive weights, so a heap with lazy stale-entry skipping works.

**Say this first (1 line):** "State is (node, coupon_used); each edge can be taken at full price within a layer or at w // 2 moving from layer 0 to layer 1; the answer is the min of the two layers at n-1."

**Brute force:**
- Enumerate every simple path from 0 to n-1, sum its weights and subtract the best single saving w - w // 2 on that path. Exponential, my oracle for n <= 6.

**Optimal:**
- dist[v][c] = cheapest cost to reach v having used c coupons (c is 0 or 1). Start at (0, 0) with cost 0.
- From (u, c) with edge (v, w): go to (v, c) for cost w; if c == 0 also go to (v, 1) for cost w // 2.
- Pop from a heap of (cost, node, c); skip an entry if its cost is larger than the stored dist (stale).
- Answer min(dist[n-1][0], dist[n-1][1]), or -1 if both are infinite.
- Why plain Dijkstra on the original graph is not enough: the cheapest plain path is not always the cheapest with a coupon. In example 1 the plain best is 20 (via node 1), minus one saving of 5 gives 15, but the direct edge 25 with the coupon costs 12. The coupon changes which path wins, so the state has to remember it.
- Why a simple path is enough: weights are positive, and w // 2 >= 0, so deleting a cycle from a walk never raises the cost (if the coupon was inside the cycle the shortened walk can still use it, or not, at most the same cost). That is also why the brute-force oracle over simple paths is valid.
- "At most k coupons": the same idea with k + 1 layers; the code has `k_coupons` and checks it equals the one-coupon answer for k = 1 and plain Dijkstra for k = 0.

**Complexity:**
- 2n states and at most 2 * (edges) * 2 transitions. Each push is O(log) of the heap size.
- Time O((n + m) log(n + m)) (heap size is bounded by pushes, which is O(m)). Space O(n + m).
- For k coupons: states (k + 1) n, time O(k (n + m) log(...)).

**Dry run:** example 1, edges 0->1 (10), 1->2 (10), 0->2 (25), n=3.
- Start (0,0)=0. Edge 0->1: (1,0)=10 and with the coupon (1,1)=5. Edge 0->2: (2,0)=25, (2,1)=12.
- Pop (1,1)=5: edge 1->2 at full price gives 15, worse than (2,1)=12.
- Pop (1,0)=10: edge 1->2 gives (2,0)=20; the coupon gives (2,1)=10+5=15, no improvement.
- Answer min(20, 12) = 12.

**Code:**
```python
import heapq, random

def optimal(n, edges):
    """Dijkstra on states (node, coupon_used). Returns min cost 0 -> n-1 or -1."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [[INF, INF] for _ in range(n)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]                                  # (cost, node, used)
    while heap:
        d, u, c = heapq.heappop(heap)
        if d > dist[u][c]:
            continue                                    # stale entry
        for v, w in adj[u]:
            if d + w < dist[v][c]:
                dist[v][c] = d + w
                heapq.heappush(heap, (d + w, v, c))
            if c == 0 and d + w // 2 < dist[v][1]:      # spend the coupon on this edge
                dist[v][1] = d + w // 2
                heapq.heappush(heap, (d + w // 2, v, 1))
    ans = min(dist[n - 1])
    return -1 if ans == INF else ans

def brute(n, edges):
    """Enumerate every simple path 0 -> n-1; cost = sum - best single saving (w - w//2)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [float('inf')]
    seen = [False] * n
    def go(u, total, saving):
        if u == n - 1:
            best[0] = min(best[0], total - saving)
            return
        seen[u] = True
        for v, w in adj[u]:
            if not seen[v]:
                go(v, total + w, max(saving, w - w // 2))
        seen[u] = False
    go(0, 0, 0)
    return -1 if best[0] == float('inf') else best[0]

def k_coupons(n, edges, k):
    """Same idea with k + 1 layers: at most k half-price edges."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [[INF] * (k + 1) for _ in range(n)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        d, u, c = heapq.heappop(heap)
        if d > dist[u][c]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v][c]:
                dist[v][c] = d + w; heapq.heappush(heap, (d + w, v, c))
            if c < k and d + w // 2 < dist[v][c + 1]:
                dist[v][c + 1] = d + w // 2; heapq.heappush(heap, (d + w // 2, v, c + 1))
    ans = min(dist[n - 1])
    return -1 if ans == INF else ans

assert optimal(3, [[0, 1, 10], [1, 2, 10], [0, 2, 25]]) == 12
assert optimal(3, [[0, 1, 4]]) == -1
assert optimal(4, [[0, 1, 1], [1, 3, 1], [0, 2, 3], [2, 3, 3]]) == 1
print('examples:', optimal(3, [[0, 1, 10], [1, 2, 10], [0, 2, 25]]), optimal(3, [[0, 1, 4]]), optimal(4, [[0, 1, 1], [1, 3, 1], [0, 2, 3], [2, 3, 3]]))

# plain Dijkstra + 'best saving on that path' is wrong: the cheapest plain path is not always the cheapest with a coupon
n, e = 3, [[0, 1, 10], [1, 2, 10], [0, 2, 25]]          # plain best = 20 (via 1), with coupon 15 (via 1) vs 12 (direct)
plain = k_coupons(n, e, 0)                              # k = 0 layers is plain Dijkstra
assert plain == 20
print('plain shortest =', plain, ' with coupon =', optimal(n, e), '(direct edge 25 -> 12 beats 20 - 5 = 15)')
assert optimal(n, e) == 12 < plain - 5

# edge cases
assert optimal(2, [[0, 1, 1]]) == 0                     # coupon makes a weight-1 edge free (1 // 2 = 0)
assert optimal(2, [[1, 0, 5]]) == -1                    # wrong direction
assert optimal(2, [[0, 1, 7], [0, 1, 3]]) == 1          # parallel edges: 3 // 2 = 1

random.seed(22)
cases = 0
for _ in range(500):
    n = random.randint(2, 6)
    m = random.randint(0, 12)
    edges = [[random.randrange(n), random.randrange(n), random.randint(1, 20)] for _ in range(m)]
    assert optimal(n, edges) == brute(n, edges), (n, edges)
    assert k_coupons(n, edges, 1) == optimal(n, edges)
    assert k_coupons(n, edges, 3) == k_coupons(n, edges, 1) or k_coupons(n, edges, 3) < k_coupons(n, edges, 1)   # more coupons never hurt
    cases += 1
print('random cross-check ok:', cases, 'cases (n <= 6, w <= 20)')

# larger, just to be sure it runs: a 10^4 node chain with shortcuts
N = 10**4
big = [[i, i + 1, 10**6] for i in range(N - 1)] + [[i, i + 7, 5 * 10**6] for i in range(0, N - 7, 3)]
print('large run cost =', optimal(N, big))
```

**Output (my run):**
```
examples: 12 -1 1
plain shortest = 20  with coupon = 12 (direct edge 25 -> 12 beats 20 - 5 = 15)
random cross-check ok: 500 cases (n <= 6, w <= 20)
large run cost = 7774500000
```

**Edge cases:**
- Unreachable n-1: -1 (example 2). A weight-1 edge with the coupon is free (1 // 2 = 0).
- Parallel edges, edges into node 0 or out of n-1: harmless.
- Floor division, not a float: an odd 25 costs 12, not 12.5.
- The coupon is optional: min over both layers covers "do not use it".

**Follow-ups:**
- Can the coupon be used on a node instead of an edge? Same layering, different transition.
- What if weights can be 0? Still fine, stale-skipping handles ties; negative weights would break Dijkstra.
- Cheapest flights with at most k stops is Part 9 Q34: that constrains the number of edges, not a discount.

**Common mistakes:**
- Running plain Dijkstra and subtracting the largest saving on the plain shortest path (wrong, see example 1).
- Marking the coupon layer visited too early, so a cheaper path using the coupon later is missed.
- Using `w / 2` (float) instead of `w // 2`.
- Taking the coupon twice because the layer check was missing (`c == 0`).

---

### Q23 ⭐⭐ 🟡 Segment tree for range minimum with point updates. Implement class `MinSegTree(nums)` (1 <= len <= 10^5) with `update(i, v)` (set nums[i] = v, returns None) and `query(l, r)` (the minimum of nums[l..r], both ends included, 0 <= l <= r < len). Build a bottom-up array tree of size 2n: leaves at positions n..2n-1, node i holds min(tree[2i], tree[2i+1]); `update` walks up from the leaf, `query` shrinks the half-open range [l + n, r + n + 1) and takes a node whenever l is odd or r is odd. Both operations are O(log n), the build O(n) and the memory 2n. Explain why this bottom-up form works for any n (not only powers of two) for a commutative, associative operation such as min, sum or gcd, and when you need the recursive top-down form instead (lazy propagation: Q44, or a non-commutative merge). A plain Fenwick tree cannot answer min when values can be set to larger numbers (a prefix minimum cannot be undone, so there is no delta to add: explain in one line). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[5, 3, 8, 1, 9, 2]], ops=[['query', [0, 5]], ['query', [2, 4]], ['update', [3, 10]], ['query', [0, 5]], ['query', [2, 4]], ['update', [0, 0]], ['query', [0, 1]]] -> [1, 1, null, 2, 8, null, 0]; init=[[4]], ops=[['query', [0, 0]], ['update', [0, -2]], ['query', [0, 0]]] -> [4, null, -2].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Bottom-up segment tree (array of size 2n) for a commutative, associative merge, here min.

**Say this first (1 line):** "Leaves live at positions n..2n-1, each inner node is the min of its two children, an update walks up from the leaf and a query takes whole nodes on the borders of a half-open range."

**Brute force:**
- Keep the plain list. `update` is O(1), `query` is min over a slice, O(n). My oracle (rescans the list on every query).

**Optimal:**
- Build: copy values into tree[n:], then for i from n-1 down to 1 set tree[i] = min(tree[2i], tree[2i+1]). O(n).
- Update: set the leaf, then i >>= 1 and recompute until the root. O(log n).
- Query [l, r] inclusive: use the half-open range [l + n, r + n + 1). While l < r: if l is odd (a right child) take tree[l] and move l right by one; if r is odd take tree[r - 1]; then halve both. O(log n).
- Why it works for any n, not only powers of two: the tree is not one balanced tree but a forest of perfect subtrees glued by the index arithmetic. Every node i >= 1 covers the leaves below it, and the loop only ever reads nodes that lie completely inside the range. Because min is commutative and associative, the order in which borders are collected does not matter, and a node that "wraps" (mixes the end and the start of the array) is never read by a query that stays inside [0, n). I verified it exhaustively for every (l, r) for n = 1..20.
- When you need the recursive top-down form: lazy propagation (Q44, pending updates need a place to sit on a node) or a non-commutative merge (e.g. string concatenation or matrix product), where the left-to-right order of the pieces matters. The bottom-up loop can be extended with a left and a right accumulator, but top-down is the safer interview answer.
- Why a Fenwick tree cannot do min with values that can grow: a BIT cell stores an aggregate that you update by adding a delta. For min there is no inverse: once a cell holds 1 you cannot "undo" it when that 1 is raised to 10. The code shows the prefix-min BIT staying at 1.

**Complexity:**
- Build O(n), `update` O(log n), `query` O(log n), memory 2n integers.
- Per operation: update walks at most log2(n) + 1 levels; query touches at most about 2 log2(n) nodes.
- Thread safety (concept only): a query reads several nodes and an update writes a whole root path, so a reader could see a half-updated path. One lock around update and query keeps it correct (or a readers-writer lock); a lock-free version needs versioned nodes.

**Dry run:** nums = [5, 3, 8, 1, 9, 2], n = 6, so leaves are tree[6..11] = 5, 3, 8, 1, 9, 2.
- Build: tree[5] = min(9, 2) = 2, tree[4] = min(8, 1) = 1, tree[3] = min(5, 3) = 3, tree[2] = min(1, 2) = 1, tree[1] = 1.
- query(2, 4): half-open [8, 11). l = 8 even; r = 11 odd so r = 10 and take tree[10] = 9. Halve: l = 4, r = 5. l even; r odd so r = 4 and take tree[4] = 1. Halve: l = 2, r = 2, stop. Answer min(9, 1) = 1.
- update(3, 10): leaf 9 becomes 10, tree[4] = min(8, 10) = 8, tree[2] = min(8, 2) = 2, tree[1] = min(2, 3) = 2. Then query(0, 5) = 2 and query(2, 4) = 8, as in the example.

**Code:**
```python
import random

class MinSegTree:
    """Bottom-up segment tree for range minimum with point assignment. tree[1] is the root, leaves at n..2n-1."""
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1):                 # O(n) build
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, v):                                # set nums[i] = v, O(log n)
        i += self.n
        self.tree[i] = v
        while i > 1:
            i >>= 1
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, l, r):                                 # min of nums[l..r] inclusive, O(log n)
        res = float('inf')
        l += self.n
        r += self.n + 1                                    # half-open [l, r)
        while l < r:
            if l & 1:                                      # l is a right child: take it, move right
                res = min(res, self.tree[l]); l += 1
            if r & 1:                                      # r is a right child: its left sibling r-1 is inside
                r -= 1; res = min(res, self.tree[r])
            l >>= 1; r >>= 1
        return res

class Naive:
    def __init__(self, nums): self.a = list(nums)
    def update(self, i, v): self.a[i] = v
    def query(self, l, r): return min(self.a[l:r + 1])

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ex1 = ([[5, 3, 8, 1, 9, 2]], [['query', [0, 5]], ['query', [2, 4]], ['update', [3, 10]], ['query', [0, 5]],
       ['query', [2, 4]], ['update', [0, 0]], ['query', [0, 1]]])
ex2 = ([[4]], [['query', [0, 0]], ['update', [0, -2]], ['query', [0, 0]]])
assert run(MinSegTree, *ex1) == [1, 1, None, 2, 8, None, 0]
assert run(MinSegTree, *ex2) == [4, None, -2]
print('example 1:', run(MinSegTree, *ex1))
print('example 2:', run(MinSegTree, *ex2))

# exhaustive check of every (l, r) for every length 1..20 (non powers of two included)
random.seed(23)
for n in range(1, 21):
    a = [random.randint(-9, 9) for _ in range(n)]
    t = MinSegTree(a)
    for l in range(n):
        for r in range(l, n):
            assert t.query(l, r) == min(a[l:r + 1]), (n, l, r)
print('exhaustive all (l, r), n = 1..20 ok (includes n = 3, 5, 6, 7 ... not powers of two)')

# the same bottom-up code with a different commutative, associative op (sum) also works for any n
class SumSeg(MinSegTree):
    def __init__(self, nums):
        self.n = len(nums); self.tree = [0] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1): self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    def update(self, i, v):
        i += self.n; self.tree[i] = v
        while i > 1: i >>= 1; self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    def query(self, l, r):
        res = 0; l += self.n; r += self.n + 1
        while l < r:
            if l & 1: res += self.tree[l]; l += 1
            if r & 1: r -= 1; res += self.tree[r]
            l >>= 1; r >>= 1
        return res
a = [random.randint(-9, 9) for _ in range(13)]
s = SumSeg(a)
assert all(s.query(l, r) == sum(a[l:r + 1]) for l in range(13) for r in range(l, 13))
print('same loop with + instead of min ok for n = 13')

# why a Fenwick tree cannot do min with raises: a 'prefix min' BIT only ever keeps the smaller value
class BadMinBIT:
    def __init__(self, n): self.t = [float('inf')] * (n + 1); self.n = n
    def set(self, i, v):                                   # i is 1-based
        while i <= self.n: self.t[i] = min(self.t[i], v); i += i & -i
    def prefix_min(self, i):
        res = float('inf')
        while i > 0: res = min(res, self.t[i]); i -= i & -i
        return res
b = BadMinBIT(4)
for i, v in enumerate([5, 3, 8, 1], 1): b.set(i, v)
b.set(4, 10)                                              # raise the 1 to 10: the stored 1 cannot be undone
print('BIT prefix_min after raising 1 -> 10:', b.prefix_min(4), '(true answer 3)')
assert b.prefix_min(4) == 1 != 3

# operation-sequence oracle against the naive version
cases = ops_total = 0
for _ in range(400):
    n = random.randint(1, 12)
    init = [[random.randint(-20, 20) for _ in range(n)]]
    ops = []
    for _ in range(random.randint(1, 40)):
        if random.random() < 0.4:
            ops.append(['update', [random.randrange(n), random.randint(-30, 30)]])
        else:
            l = random.randrange(n); r = random.randint(l, n - 1)
            ops.append(['query', [l, r]])
    assert run(MinSegTree, init, ops) == run(Naive, init, ops), (init, ops)
    cases += 1; ops_total += len(ops)
print('operation-sequence oracle ok:', cases, 'sequences,', ops_total, 'operations')
```

**Output (my run):**
```
example 1: [1, 1, None, 2, 8, None, 0]
example 2: [4, None, -2]
exhaustive all (l, r), n = 1..20 ok (includes n = 3, 5, 6, 7 ... not powers of two)
same loop with + instead of min ok for n = 13
BIT prefix_min after raising 1 -> 10: 1 (true answer 3)
operation-sequence oracle ok: 400 sequences, 7971 operations
```

**Edge cases:**
- n = 1: the tree is `[0, x]`, loop `while i > 1` does nothing, a query takes the leaf.
- Negative values and an update that makes a leaf larger (min must be recomputed, not min-ed in place).
- l == r, the full range, and n not a power of two (all in the exhaustive test).
- `query` is inclusive on both ends (the +1 builds the half-open range).

**Follow-ups:**
- Range sum instead? Same loop with `+` (the code does it); a BIT is shorter if there are no min/max queries (Q10, Q17).
- Static array, no updates? A sparse table answers min in O(1) (Q24).
- Range add? You need lazy propagation (Q44).

**Common mistakes:**
- Forgetting `r + n + 1` (querying [l, r) by accident).
- Mixing 0-based user indices with the 1-based heap layout of a recursive tree.
- Update that does `tree[i] = min(tree[i], v)`: only works for decreases.
- Starting the update loop at the root instead of the leaf.

---

### Q24 ⭐⭐ 🟡 Sparse table for static range minimum queries. `nums` has 1 <= len <= 10^5 integers (static, never updated) and `queries` is a list of up to 10^5 pairs [l, r] with 0 <= l <= r < len(nums). Return `[answers, entries]`: `answers` holds, for each query, `[minimum, index of its LEFTMOST occurrence inside l..r]`, and `entries` is the total number of cells stored in your table (level j stores one cell for every start i with i + 2^j <= n, for every level with 2^j <= n). Build `table[j][i]` = the best (value, index) pair for the block [i, i + 2^j) from two blocks of level j - 1 (compare (value, index) tuples so the leftmost index wins ties), and answer a query with k = floor(log2(r - l + 1)) from `table[k][l]` and `table[k][r - 2^k + 1]`: the two blocks overlap, which is harmless because min is idempotent (a sum would double count). Build O(n log n), query O(1); compare with the segment tree of Q23 (O(log n) query but supports updates) and say why Part 2 Q45 can also use a deque. In the answer include a dry run on the first example and a seeded random cross-check of your solution against slicing with min() and list.index on each query on small inputs. Example: nums=[5, 2, 4, 2, 7], queries=[[0, 4], [2, 4], [0, 0]] -> [[[2, 1], [2, 3], [5, 0]], 11]; nums=[3], queries=[[0, 0]] -> [[[3, 0]], 1].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Sparse table (binary lifting on blocks) for an idempotent operation on a static array.

**Say this first (1 line):** "Block j covers 2^j elements; I cover [l, r] with two possibly overlapping blocks of size 2^k, k = floor(log2(length)), which is fine for min because min(x, x) = x."

**Brute force:**
- For each query slice `nums[l:r+1]`, take `min` and `list.index`. O(n) per query, O(n * q) total. The oracle.

**Optimal:**
- Level 0 holds the pairs (value, index). Level j at start i holds min of the two level j-1 blocks at i and i + 2^(j-1).
- Compare (value, index) tuples: the smaller value wins, and on equal values the smaller index wins, so the leftmost occurrence survives every merge.
- Query: k = (r - l + 1).bit_length() - 1 (an exact floor of log2 without floats). Take min(table[k][l], table[k][r - 2^k + 1]).
- Overlap is harmless for min because it is idempotent. The code shows a sum would double count the middle.
- Entries: level j has n - 2^j + 1 cells, for every level with 2^j <= n. For the first example n = 5: 5 + 4 + 2 = 11. For n = 10^5 it is 1,568,946 cells (about n log2 n).
- Vs the segment tree of Q23: sparse table has O(1) query but O(n log n) build and memory and no updates. Segment tree has O(log n) query, O(n) build, supports updates.
- Part 2 Q45 can also use a monotonic deque: for sliding windows of a fixed size the deque gives all answers in O(n) total, without the n log n table.

**Complexity:**
- Build O(n log n) time and cells. Query O(1): two lookups and one comparison.
- Memory is the cost: about n log n tuples, so for large n it is heavy in Python; storing indices only (compare by nums[i], i) halves it.

**Dry run:** nums = [5, 2, 4, 2, 7].
- Level 0: (5,0) (2,1) (4,2) (2,3) (7,4).
- Level 1 (blocks of 2): (2,1) (2,1) (2,3) (2,3). Level 2 (blocks of 4): (2,1) (2,1). Total 5 + 4 + 2 = 11 cells.
- Query [2, 4]: length 3, k = 1. table[1][2] = (2,3) and table[1][4 - 2 + 1 = 3] = (2,3). Answer [2, 3].
- Query [0, 4]: length 5, k = 2. table[2][0] = (2,1), table[2][1] = (2,1). Answer [2, 1], the leftmost 2.

**Code:**
```python
import random

def build(nums):
    """table[j][i] = best (value, index) of block [i, i + 2^j). Tuples compare value first, then index: leftmost wins ties."""
    n = len(nums)
    table = [[(v, i) for i, v in enumerate(nums)]]
    j = 1
    while (1 << j) <= n:
        prev, half = table[-1], 1 << (j - 1)
        table.append([min(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)])
        j += 1
    return table

def optimal(nums, queries):
    table = build(nums)
    entries = sum(len(row) for row in table)
    answers = []
    for l, r in queries:
        k = (r - l + 1).bit_length() - 1                  # floor(log2(length)), no float log
        v, i = min(table[k][l], table[k][r - (1 << k) + 1])   # two overlapping blocks
        answers.append([v, i])
    return [answers, entries]

def brute(nums, queries):
    answers = []
    for l, r in queries:
        seg = nums[l:r + 1]
        m = min(seg)
        answers.append([m, l + seg.index(m)])             # list.index returns the leftmost
    n = len(nums)
    entries = sum(n - (1 << j) + 1 for j in range(n.bit_length()) if (1 << j) <= n)
    return [answers, entries]

assert optimal([5, 2, 4, 2, 7], [[0, 4], [2, 4], [0, 0]]) == [[[2, 1], [2, 3], [5, 0]], 11]
assert optimal([3], [[0, 0]]) == [[[3, 0]], 1]
print('examples:', optimal([5, 2, 4, 2, 7], [[0, 4], [2, 4], [0, 0]]), optimal([3], [[0, 0]]))

# the overlap is harmless for min (idempotent) but breaks a sum
nums = [1, 2, 3, 4, 5]
l, r = 0, 4; k = 2                                        # blocks [0,4) and [1,5) overlap on 1..3
wrong = sum(nums[0:4]) + sum(nums[1:5])
print('overlapping blocks: sum would be', wrong, 'instead of', sum(nums))
assert wrong != sum(nums)

# entries count: n log n growth; for n = 10^5
n = 10**5
cells = sum(n - (1 << j) + 1 for j in range(n.bit_length()) if (1 << j) <= n)
print('n = 10^5 table cells:', cells, '(about n * log2 n =', round(n * 16.6), ')')

random.seed(24)
for _ in range(600):
    n = random.randint(1, 40)
    nums = [random.randint(-5, 5) for _ in range(n)]      # small range = many ties
    qs = []
    for _ in range(30):
        l = random.randrange(n); qs.append([l, random.randint(l, n - 1)])
    assert optimal(nums, qs) == brute(nums, qs), (nums, qs)
print('random cross-check ok: 600 arrays x 30 queries, many duplicate minima')

# all equal: the leftmost index must be l itself
assert optimal([7] * 9, [[3, 8], [0, 8]])[0] == [[7, 3], [7, 0]]
big = [random.randint(0, 10**9) for _ in range(10**5)]
qs = [[l, random.randint(l, 10**5 - 1)] for l in (random.randrange(10**5) for _ in range(1000))]
assert optimal(big, qs) == brute(big, qs)
print('n = 10^5, 1000 random queries ok')
```

**Output (my run):**
```
examples: [[[2, 1], [2, 3], [5, 0]], 11] [[[3, 0]], 1]
overlapping blocks: sum would be 24 instead of 15
n = 10^5 table cells: 1568946 (about n * log2 n = 1660000 )
random cross-check ok: 600 arrays x 30 queries, many duplicate minima
n = 10^5, 1000 random queries ok
```

**Edge cases:**
- n = 1: one level, one cell, k = 0.
- Many ties (all equal): the leftmost index is l itself, tested.
- l == r: k = 0, both lookups are the same cell.
- Exact power-of-two lengths: the two blocks coincide.

**Follow-ups:**
- Which operations work? Any idempotent one: min, max, gcd, bitwise and/or. Not sum, product, xor.
- Can it handle updates? Not cheaply; a rebuild is O(n log n). Use Q23.
- Sum on a static array? Plain prefix sums are O(1) and O(n); no table needed.

**Common mistakes:**
- Using `math.log2` (float error at powers of two); use `bit_length`.
- Level j with the wrong cell count (reading past the end of the row).
- Comparing values only, losing the leftmost-index rule.
- Using it for sums, where the overlap double counts.

---

### Q25 ⭐⭐ 🟡 Count inversions with a Fenwick tree (BIT). `nums` has 0 <= len <= 10^5 integers (duplicates allowed, |value| <= 10^9). An inversion is a pair i < j with nums[i] > nums[j] (STRICTLY greater, equal values are not inversions). Return `[total, before_greater]` where `before_greater[j]` is the number of earlier elements strictly greater than nums[j] and `total` is their sum. Compress the values to ranks 1..m (Q17), scan left to right, and for each element add `j - prefix_count(rank[j])` before inserting its rank: `prefix_count` is a BIT prefix sum, update and query both use the loops `i += i & -i` and `i -= i & -i`. O(n log n) time, O(n) space. Compare with the merge-sort counter of Part 13 Q17 (same complexity, no extra per-element information) and say what changes for 'at most' instead of 'strictly'. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) double loop on small inputs. Example: nums=[3, 1, 2, 3, 1] -> [5, [0, 1, 1, 0, 3]]; nums=[] -> [0, []]; nums=[2, 2, 2] -> [0, [0, 0, 0]].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Fenwick tree (BIT) over compressed ranks, scanning left to right and counting earlier elements.

**Say this first (1 line):** "Compress values to ranks, then for each element ask the BIT how many earlier elements have rank <= mine; the earlier elements strictly greater are j minus that."

**Brute force:**
- Double loop over all pairs i < j with nums[i] > nums[j]. O(n^2). The oracle.

**Optimal:**
- Rank the sorted distinct values 1..m (Q17). Equal values get the same rank.
- Scan j = 0..n-1. `prefix_count(rank)` is the number of earlier elements with rank <= rank[j]; the others, `j - prefix_count`, are strictly greater. That is before_greater[j].
- Then add one at position rank[j] (`i += i & -i`). Queries walk `i -= i & -i`.
- Equal values land in the prefix (rank <= mine), so they are not counted: that is the STRICT rule.
- What changes for other comparisons: counting earlier elements >= (non-strict inversions) uses prefix_count(rank - 1) in place of prefix_count(rank); counting earlier elements "at most" mine is just prefix_count(rank) itself. The code checks the `>=` variant against a double loop.
- Versus the merge-sort counter of Part 13 Q17: same O(n log n), but this gives the per-element counts (before_greater) for free, and extends to "count of smaller numbers after self" by scanning right to left.

**Complexity:**
- Time O(n log n): sorting for ranks plus n updates and n queries of O(log m).
- Space O(n) for the rank map and the tree.
- The total can reach n(n-1)/2 (about 5 * 10^9 for n = 10^5); Python ints do not overflow.

**Dry run:** nums = [3, 1, 2, 3, 1], ranks 1, 2, 3 equal the values.
- j=0, v=3: prefix(3) = 0, so 0 - 0 = 0. Insert 3.
- j=1, v=1: prefix(1) = 0, so 1 - 0 = 1. Insert 1.
- j=2, v=2: prefix(2) = 1 (the 1), so 2 - 1 = 1. Insert 2.
- j=3, v=3: prefix(3) = 3 (3, 1, 2), so 3 - 3 = 0. Insert 3.
- j=4, v=1: prefix(1) = 1, so 4 - 1 = 3 (the two 3s and the 2). Total 0+1+1+0+3 = 5.

**Code:**
```python
import random

def optimal(nums):
    """Fenwick tree over compressed ranks. Returns [total, before_greater]."""
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}   # coordinate compression to 1..m
    m = len(ranks)
    tree = [0] * (m + 1)
    before = []
    for j, v in enumerate(nums):
        r = ranks[v]
        cnt, i = 0, r
        while i > 0:                                       # prefix_count(r): earlier elements with rank <= r
            cnt += tree[i]; i -= i & -i
        before.append(j - cnt)                             # earlier elements strictly greater
        i = r
        while i <= m:                                      # insert rank r
            tree[i] += 1; i += i & -i
    return [sum(before), before]

def brute(nums):
    before = [sum(1 for i in range(j) if nums[i] > nums[j]) for j in range(len(nums))]
    return [sum(before), before]

def at_most_variant(nums):
    """Pairs i < j with nums[i] >= nums[j] ('at most' side of the comparison): use prefix_count(rank - 1)."""
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(ranks); tree = [0] * (m + 1); total = 0
    for j, v in enumerate(nums):
        r = ranks[v]; cnt, i = 0, r - 1                    # strictly smaller earlier elements
        while i > 0: cnt += tree[i]; i -= i & -i
        total += j - cnt                                   # earlier elements >= v
        i = r
        while i <= m: tree[i] += 1; i += i & -i
    return total

assert optimal([3, 1, 2, 3, 1]) == [5, [0, 1, 1, 0, 3]]
assert optimal([]) == [0, []]
assert optimal([2, 2, 2]) == [0, [0, 0, 0]]
print('examples:', optimal([3, 1, 2, 3, 1]), optimal([]), optimal([2, 2, 2]))

# dry run of the Fenwick loops on the first example ranks: values 1,2,3 -> ranks 1,2,3
print('ranks:', {v: i + 1 for i, v in enumerate(sorted(set([3, 1, 2, 3, 1])))})

# edge cases
assert optimal([5]) == [0, [0]]
assert optimal([3, 2, 1]) == [3, [0, 1, 2]]                # strictly decreasing: n(n-1)/2
assert optimal([-10**9, 10**9, -10**9]) == [1, [0, 0, 1]]
n = 1000
assert optimal(list(range(n, 0, -1)))[0] == n * (n - 1) // 2

random.seed(25)
for _ in range(800):
    n = random.randint(0, 25)
    nums = [random.randint(-6, 6) for _ in range(n)]
    assert optimal(nums) == brute(nums), nums
    assert at_most_variant(nums) == sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] >= nums[j])
print('random cross-check ok: 800 arrays (duplicates heavy), strict and >= variants')

big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
total = optimal(big)[0]
print('n = 10^5 random: total inversions =', total, '(expected about n^2/4 =', 10**10 // 4, ')')
```

**Output (my run):**
```
examples: [5, [0, 1, 1, 0, 3]] [0, []] [0, [0, 0, 0]]
ranks: {1: 1, 2: 2, 3: 3}
random cross-check ok: 800 arrays (duplicates heavy), strict and >= variants
n = 10^5 random: total inversions = 2500528204 (expected about n^2/4 = 2500000000 )
```

**Edge cases:**
- Empty array: [0, []]. Single element: [0, [0]].
- All equal: no inversions. Strictly decreasing: n(n-1)/2.
- Values up to 10^9 in magnitude: that is why we compress instead of indexing by value.
- Rank 0 does not exist: a BIT is 1-indexed, `i = 0` would loop forever on update.

**Follow-ups:**
- Count of smaller numbers after self? Scan right to left, query prefix(rank - 1).
- Reverse pairs with nums[i] > 2 * nums[j]? Compress both values and doubled values together, or use merge sort; it is Q36 in this part.
- Online stream? Compression needs all values first; with an unknown range use a balanced structure or an offline pass.

**Common mistakes:**
- Using `<=` so equal values count as inversions.
- A 0-based BIT index (infinite loop on `i & -i` with i = 0).
- Updating before querying, so an element counts against itself.
- Compressing with a dict built from a set (unordered), instead of sorted distinct values.

---

### Q26 ⭐⭐ 🟡 [Set A, Q2 of 5, 7 min, 15 pts] Underground system (average trip times). Implement class `UndergroundSystem()` with `checkIn(id, station, t)`, `checkOut(id, station, t)` and `getAverageTime(start, end)`. A customer id has at most one open trip at a time; `checkOut` always closes the open trip of that id; the trip duration is t_out - t_in. `getAverageTime` returns the average duration (a float, total / count) over all COMPLETED trips that started at `start` and ended at `end` (direction matters: A to B and B to A are different); it is only called after at least one such trip. Here t is an argument of the call (a trip timestamp), not a live clock. Keep a dict id -> (station, t) for open trips and a dict (start, end) -> [total, count] for finished ones; every operation O(1). Say what you would do when a customer id checks out without having checked in (the checker never does it) and why storing a running total and count beats storing every duration. Hash-map idioms: Part 1 Q39. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[], ops=[['checkIn', [45, 'A', 3]], ['checkIn', [32, 'A', 8]], ['checkOut', [45, 'B', 15]], ['checkOut', [32, 'B', 22]], ['getAverageTime', ['A', 'B']], ['checkIn', [10, 'B', 24]], ['checkOut', [10, 'A', 40]], ['getAverageTime', ['B', 'A']], ['checkIn', [45, 'A', 30]], ['checkOut', [45, 'B', 36]], ['getAverageTime', ['A', 'B']]] -> [null, null, null, null, 13.0, null, null, 16.0, null, null, 10.666666666666666].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Two hash maps: open trips keyed by customer id, running (total, count) keyed by (start, end).

**Say this first (1 line):** "Open trips in a dict by id, finished trips folded into a running total and count per (start, end) pair, so every call is O(1) and memory does not grow with the number of trips."

**Brute force:**
- Keep a list of every open check-in and every finished trip with its duration; each `getAverageTime` rescans the list and averages. O(trips) per query, O(trips) memory. My oracle.

**Optimal:**
- `checkIn(id, station, t)`: `open[id] = (station, t)`.
- `checkOut(id, station, t)`: pop the open record, `rec = done[(start, station)]`, add `t - t_in` to the total and 1 to the count.
- `getAverageTime(start, end)`: `total / count`.
- Rules stated up front: direction matters (A to B is not B to A); a customer has at most one open trip; the duration is t_out - t_in (t is an argument, no clock is read); the average is a float over completed trips only; open trips do not count.
- Check-out with no check-in (the checker never does it): I would raise an error (ValueError here) and change nothing, rather than invent a trip or ignore it silently. Asking about a pair with no completed trip also raises (KeyError), where a real service might return None.
- Why a running total and count beat storing every duration: the average needs only those two numbers, so memory is O(distinct pairs) rather than O(trips), and the query does not scan. The cost is that you cannot later ask for median or maximum.

**Complexity:**
- `checkIn`, `checkOut`, `getAverageTime`: O(1) expected each (dict operations).
- Space O(open trips + distinct (start, end) pairs).
- Thread safety (concept only): the check-out does a pop plus a read-modify-write of the (total, count) pair, so two threads could lose an update; guard each method with one lock, or one lock per (start, end) record plus an atomic pop of the open trip.

**Dry run:** the first example.
- checkIn 45 at A, t=3; checkIn 32 at A, t=8.
- checkOut 45 at B, t=15: trip 12, (A,B) = [12, 1]. checkOut 32 at B, t=22: trip 14, (A,B) = [26, 2]. Average 26 / 2 = 13.0.
- checkIn 10 at B, t=24; checkOut 10 at A, t=40: trip 16, (B,A) = [16, 1]. Average 16.0.
- checkIn 45 at A, t=30; checkOut at B, t=36: trip 6, (A,B) = [32, 3]. Average 32 / 3 = 10.666666666666666.

**Code:**
```python
import random

class UndergroundSystem:
    def __init__(self):
        self.open = {}                      # id -> (station, t_in)
        self.done = {}                      # (start, end) -> [total, count]

    def checkIn(self, id, station, t):      # O(1)
        assert id not in self.open, 'one open trip per id'
        self.open[id] = (station, t)

    def checkOut(self, id, station, t):     # O(1)
        if id not in self.open:             # my rule: reject loudly, never invent a trip
            raise ValueError('check-out without check-in: %r' % (id,))
        start, t_in = self.open.pop(id)
        rec = self.done.setdefault((start, station), [0, 0])
        rec[0] += t - t_in
        rec[1] += 1

    def getAverageTime(self, start, end):   # O(1)
        total, count = self.done[(start, end)]
        return total / count

class Naive:
    """Keeps every trip and every duration, rescans lists on each query."""
    def __init__(self): self.open = []; self.trips = []
    def checkIn(self, id, station, t): self.open.append((id, station, t))
    def checkOut(self, id, station, t):
        for k, (i, s, ti) in enumerate(self.open):
            if i == id:
                del self.open[k]; self.trips.append((s, station, t - ti)); return
    def getAverageTime(self, start, end):
        d = [x for s, e, x in self.trips if s == start and e == end]
        return sum(d) / len(d)

def run(cls, ops):
    obj = cls()
    return [getattr(obj, m)(*a) for m, a in ops]

ex = [['checkIn', [45, 'A', 3]], ['checkIn', [32, 'A', 8]], ['checkOut', [45, 'B', 15]], ['checkOut', [32, 'B', 22]],
      ['getAverageTime', ['A', 'B']], ['checkIn', [10, 'B', 24]], ['checkOut', [10, 'A', 40]],
      ['getAverageTime', ['B', 'A']], ['checkIn', [45, 'A', 30]], ['checkOut', [45, 'B', 36]],
      ['getAverageTime', ['A', 'B']]]
want = [None, None, None, None, 13.0, None, None, 16.0, None, None, 10.666666666666666]
assert run(UndergroundSystem, ex) == want
print('example:', run(UndergroundSystem, ex))

# direction matters; check-out without check-in is rejected
u = UndergroundSystem()
u.checkIn(1, 'X', 0); u.checkOut(1, 'Y', 5)
assert u.getAverageTime('X', 'Y') == 5.0
try:
    u.getAverageTime('Y', 'X'); raise SystemExit('should raise')
except KeyError:
    print('Y -> X has no completed trip: KeyError (the checker never asks)')
try:
    u.checkOut(99, 'Y', 7); raise SystemExit('should raise')
except ValueError as e:
    print('rejected:', e)
u.checkIn(1, 'X', 10); u.checkOut(1, 'X', 10)             # zero-length trip, same start and end is allowed
assert u.getAverageTime('X', 'X') == 0.0

# operation-sequence oracle: random valid call sequences
random.seed(26)
stations = ['A', 'B', 'C']
n_ops = 0
for _ in range(500):
    ops, open_ids, finished, t = [], {}, set(), 0
    for _ in range(random.randint(1, 40)):
        t += random.randint(0, 5)
        r = random.random()
        free = [i for i in range(6) if i not in open_ids]
        if r < 0.4 and free:
            i = random.choice(free); s = random.choice(stations); open_ids[i] = s
            ops.append(['checkIn', [i, s, t]])
        elif r < 0.75 and open_ids:
            i = random.choice(list(open_ids)); s = random.choice(stations)
            finished.add((open_ids.pop(i), s)); ops.append(['checkOut', [i, s, t]])
        elif finished:
            a, b = random.choice(sorted(finished)); ops.append(['getAverageTime', [a, b]])
    assert run(UndergroundSystem, ops) == run(Naive, ops), ops
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 sequences,', n_ops, 'operations')
```

**Output (my run):**
```
example: [None, None, None, None, 13.0, None, None, 16.0, None, None, 10.666666666666666]
Y -> X has no completed trip: KeyError (the checker never asks)
rejected: check-out without check-in: 99
operation-sequence oracle ok: 500 sequences, 9176 operations
```

**Edge cases:**
- Same id reused after a check-out: allowed (the open record was popped).
- Start equals end, or a zero-length trip: allowed, average can be 0.0.
- A pair with no completed trip: the checker never asks; mine raises KeyError.
- Float output: `total / count`, as the example 10.666666666666666 shows (not rounded).

**Follow-ups:**
- Pacing and scoring: this is Set A, Q2 of 5, 7 minutes, 15 points. How I would pace this: about 1 minute to state the rules and tie-breaks aloud, 3 minutes to code the two dicts, 1 minute to run the example, 1 minute for complexity and the missing-check-in answer, 1 minute spare for the 60-second summary. Scoring by the part header rubric (15 points): about 4.5 for stating the rules (direction, one open trip, t as an argument, completed trips only), 4.5 for a correct solution that passes the example and a random operation-sequence check, 3 for O(1) per call with the reason, 1.5 for the edge cases (missing check-in, A to B vs B to A), 1.5 for a crisp spoken summary. Partial credit: a version that stores every duration and rescans is correct but loses most of the complexity points.
- Median of trip times? Then you must keep durations (two heaps or a sorted list per pair).
- Many threads? One lock per method as above, stated as a concept.

**Common mistakes:**
- Keying finished trips by start only, or by an unordered pair.
- Integer division for the average.
- Not removing the open trip on check-out, so a later check-in of the same id fails.
- Counting trips that are still open.

---

### Q27 ⭐⭐ 🟡 [Set A, Q3 of 5, 9 min, 20 pts] Leaderboard. Implement class `Leaderboard()` with `addScore(player, score)` (add the positive integer `score` to the player's total, creating the player if new; returns None), `top(K)` (the sum of the K highest player totals; when there are fewer than K players, the sum of all of them) and `reset(player)` (remove the player entirely, as if never seen; does nothing for an unknown player; returns None). A player's total can be added to many times. Up to 10^5 operations and 10^4 players. A dict of totals plus `heapq.nlargest(K, totals.values())` gives O(P log K) per `top`; say when that is enough and what you would use if `top` were called far more often than `addScore` (a sorted structure or two heaps with lazy deletion as in Part 8 Q31, or a Fenwick tree over scores). Heap basics are Part 8 Q1 and the kth-largest idea Part 8 Q4. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[], ops=[['addScore', [1, 73]], ['addScore', [2, 56]], ['addScore', [3, 39]], ['addScore', [4, 51]], ['addScore', [5, 4]], ['top', [1]], ['reset', [1]], ['reset', [9]], ['addScore', [2, 51]], ['top', [3]], ['top', [10]]] -> [null, null, null, null, null, 73, null, null, null, 197, 201].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Hash map of totals plus a top-K selection with `heapq.nlargest`.

**Say this first (1 line):** "A dict of player totals; `top(K)` sums `heapq.nlargest(K, totals.values())`, O(P log K); I would switch the structure only if `top` is called far more often than `addScore`."

**Brute force:**
- Keep a log of every add and reset and recompute all totals and a full sort on each `top`. My oracle.

**Optimal:**
- `addScore(p, s)`: `totals[p] = totals.get(p, 0) + s`. O(1).
- `reset(p)`: `totals.pop(p, None)`. O(1). The player vanishes entirely, so a later add starts from 0. An unknown player is a no-op.
- `top(K)`: `sum(heapq.nlargest(K, totals.values()))`. With fewer than K players it just sums all of them. Ties do not matter: only the sum of the K largest totals is returned.
- When this is enough: a few hundred or thousand players and moderate `top` calls. With P = 10^4 players one `top` is about P log K comparisons, a few tens of thousands: fine for 10^5 mixed operations.
- When `top` dominates: keep a sorted list of (total, player) with `bisect.insort`: `top` becomes a slice of K items (O(K)), update O(P) for the list shift, which is a fast memmove. The code has this as `LeaderboardSorted` and checks it against the other two. Beyond that: a heap with lazy deletion (Part 8 Q31 idea: push new (total, player), skip entries whose total no longer matches) or a Fenwick tree over score values with counts, which gives top-K sums in O(log maxScore) if scores are bounded. Heap basics: Part 8 Q1; kth-largest: Part 8 Q4.

**Complexity:**
- `addScore` O(1), `reset` O(1), `top(K)` O(P log K) time and O(K) extra space; total memory O(P).
- Sorted-list variant: `addScore` and `reset` O(P) worst case (index lookup is O(log P), shifting is O(P)), `top` O(K).
- Thread safety (concept only): `top` iterates the dict while another thread may insert, which in CPython raises "dictionary changed size during iteration"; one lock around every method (or iterate over a snapshot taken under the lock).

**Dry run:** the first example.
- Adds give totals {1:73, 2:56, 3:39, 4:51, 5:4}. `top(1)` = 73.
- `reset(1)` removes player 1. `reset(9)` does nothing.
- `addScore(2, 51)`: player 2 becomes 107. `top(3)` = 107 + 51 + 39 = 197. `top(10)` (only 4 players) = 107 + 51 + 39 + 4 = 201.

**Code:**
```python
import heapq, random
from bisect import insort, bisect_left

class Leaderboard:
    def __init__(self):
        self.totals = {}

    def addScore(self, player, score):      # O(1)
        self.totals[player] = self.totals.get(player, 0) + score

    def top(self, K):                       # O(P log K): heapq.nlargest keeps a heap of size K
        return sum(heapq.nlargest(K, self.totals.values()))

    def reset(self, player):                # O(1); unknown player is a no-op
        self.totals.pop(player, None)

class LeaderboardSorted:
    """For top-heavy workloads: keep a sorted list of (total, player). addScore/reset O(P) (list insert), top O(K)."""
    def __init__(self):
        self.totals = {}; self.order = []
    def addScore(self, player, score):
        old = self.totals.get(player)
        if old is not None:
            del self.order[bisect_left(self.order, (old, player))]
        new = (old or 0) + score
        self.totals[player] = new
        insort(self.order, (new, player))
    def top(self, K):
        return sum(t for t, _ in self.order[max(0, len(self.order) - K):]) if K > 0 else 0
    def reset(self, player):
        old = self.totals.pop(player, None)
        if old is not None:
            del self.order[bisect_left(self.order, (old, player))]

class Naive:
    def __init__(self): self.log = []                      # every (player, score) ever added, plus resets
    def addScore(self, player, score): self.log.append(('add', player, score))
    def reset(self, player): self.log.append(('reset', player, 0))
    def top(self, K):
        tot = {}
        for kind, p, s in self.log:
            if kind == 'add': tot[p] = tot.get(p, 0) + s
            else: tot.pop(p, None)
        return sum(sorted(tot.values(), reverse=True)[:K])

def run(cls, ops):
    obj = cls()
    return [getattr(obj, m)(*a) for m, a in ops]

ex = [['addScore', [1, 73]], ['addScore', [2, 56]], ['addScore', [3, 39]], ['addScore', [4, 51]], ['addScore', [5, 4]],
      ['top', [1]], ['reset', [1]], ['reset', [9]], ['addScore', [2, 51]], ['top', [3]], ['top', [10]]]
want = [None, None, None, None, None, 73, None, None, None, 197, 201]
for cls in (Leaderboard, LeaderboardSorted, Naive):
    assert run(cls, ex) == want, cls
print('example:', run(Leaderboard, ex))

# edge cases: empty board, K larger than players, reset then re-add starts from zero
lb = Leaderboard()
assert lb.top(5) == 0
lb.addScore(7, 10); lb.reset(7); lb.addScore(7, 3)
assert lb.top(1) == 3
lb.addScore(8, 3)
assert lb.top(2) == 6 and lb.top(100) == 6                 # ties do not matter: only the sum is returned

random.seed(27)
n_ops = 0
for _ in range(500):
    ops = []
    for _ in range(random.randint(1, 50)):
        r = random.random()
        p = random.randint(1, 6)
        if r < 0.5: ops.append(['addScore', [p, random.randint(1, 20)]])
        elif r < 0.65: ops.append(['reset', [p]])
        else: ops.append(['top', [random.randint(1, 8)]])
    a = run(Leaderboard, ops)
    assert a == run(Naive, ops) == run(LeaderboardSorted, ops), ops
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 sequences,', n_ops, 'operations, 3 implementations agree')
```

**Output (my run):**
```
example: [None, None, None, None, None, 73, None, None, None, 197, 201]
operation-sequence oracle ok: 500 sequences, 12398 operations, 3 implementations agree
```

**Edge cases:**
- Empty board: `top(K)` is 0.
- K larger than the number of players: sum of all.
- Reset then re-add: totals restart from the new score.
- Repeated adds to the same player accumulate. Equal totals are fine.

**Follow-ups:**
- Pacing and scoring: this is Set A, Q3 of 5, 9 minutes, 20 points. How I would pace this: 2 minutes to state the rules (reset deletes, fewer than K players, ties irrelevant), 3 minutes to code the dict version, 2 minutes to run the example and the oracle idea, 1 minute for complexity and the "when top is hot" alternative, 1 minute spare for the summary. Scoring by the part header rubric (20 points): about 6 for stating the rules out loud, 6 for a correct solution that passes the example and a random operation-sequence check, 4 for the stated complexity and why, 2 for the edge cases, 2 for the spoken summary. Partial credit: a full sort on each `top` is correct and earns most of the correctness points but loses on complexity.
- Return the rank of a player? Needs an order-statistics structure (sorted list with bisect, or a Fenwick tree).
- Distributed leaderboard? Out of scope here: that is a systems question (Book 4).

**Common mistakes:**
- `reset` that sets the score to 0 but leaves the player in the table (it would then still count in `top` and in the player count).
- `nlargest` on the dict instead of `.values()`.
- Raising KeyError on an unknown reset.
- Sorting the full list on every `top` and claiming it is O(P log K).

---

### Q28 ⭐⭐ 🟡 [Set B, Q2 of 5, 8 min, 15 pts] Components after deleting edges one by one. `n` nodes 0..n-1 (1 <= n <= 10^5), `edges` a list of undirected [u, v] pairs (0 <= len <= 2*10^5) numbered by position, and `removals` a list of DISTINCT edge indices giving the order in which edges are deleted. Return a list of len(removals) + 1 integers: the number of connected components before any deletion and after each deletion in turn. Process OFFLINE in reverse: start with all never-deleted edges in a union-find (Part 9 Q13), record the component count, then add the removed edges back from the last removal to the first, recording the count after each, and reverse the list; deleting is hard for union-find, adding is easy. O((n + m) alpha(n)). Compare with the online union-find of Part 9 Q43 and the plain component count of Part 9 Q3. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that recounts the components from scratch after every deletion on small inputs. Example: n=4, edges=[[0, 1], [1, 2], [2, 3]], removals=[1, 0] -> [1, 2, 3]; n=3, edges=[[0, 1], [0, 1], [1, 2]], removals=[0, 1, 2] -> [1, 1, 2, 3].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Offline reversal: deletions are hard for union-find, additions are easy, so process the deletions backwards.

**Say this first (1 line):** "I replay the deletions in reverse as insertions into a union-find that starts with only the never-deleted edges, record the component count each time, then reverse the list."

**Brute force:**
- After each deletion rebuild the graph and count components with a DFS. O(k (n + m)) for k deletions. My oracle.

**Optimal:**
- Put every edge whose index is not in `removals` into a union-find; `comps` starts at n and drops by one for each union that joins two different roots.
- Record `comps` (the count after ALL deletions). Then for idx in reversed(removals): union the endpoints of edge idx and record `comps`.
- The recorded list reads: after the last deletion, after the one before, ..., before any deletion. Reverse it to get the required order: initial count first.
- Why this is right: the graph after deletion i is exactly "never-deleted edges plus the edges deleted after i", which is what the reverse replay holds at that moment. The component count depends only on the edge set, not on the order edges were added.
- Parallel edges and self loops are fine: the second union of the same pair or a self loop changes nothing (find returns the same root).
- Compare: Part 9 Q43 is the online union-find (edges arrive over time); Part 9 Q3 counts components once. Here the future is known, which is what lets us avoid deletion support.

**Complexity:**
- Time O((n + m) alpha(n)) with path halving (plus union by size, or even without it in practice), O(len(removals) + m) for the set and loops.
- Space O(n + m) (parent array, removal set).
- Find is iterative (path halving), so a path of 10^5 nodes is no recursion problem.

**Dry run:** n=4, edges 0-1, 1-2, 2-3, removals [1, 0].
- Edges never deleted: index 2 (2-3). comps = 4 - 1 = 3. Record [3].
- Reverse replay: removal idx 0 (0-1): union, comps 2. Record [3, 2]. Then idx 1 (1-2): union, comps 1. Record [3, 2, 1].
- Reverse: [1, 2, 3]. Matches the example: 1 component at the start, 2 after deleting edge 1, 3 after deleting edge 0.
- Second example: edges 0-1, 0-1, 1-2, removals [0, 1, 2] gives [1, 1, 2, 3]: deleting one of the parallel edges changes nothing.

**Code:**
```python
import random

def optimal(n, edges, removals):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:                # iterative, path halving
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    comps = n
    def union(a, b):
        nonlocal comps
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            comps -= 1
    gone = set(removals)
    for i, (u, v) in enumerate(edges):       # edges that are never deleted
        if i not in gone:
            union(u, v)
    out = [comps]
    for idx in reversed(removals):           # add the deleted edges back, last deletion first
        union(*edges[idx])
        out.append(comps)
    out.reverse()
    return out

def count_components(n, edges, banned):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if i not in banned:
            adj[u].append(v); adj[v].append(u)
    seen = [False] * n; c = 0
    for s in range(n):
        if not seen[s]:
            c += 1; seen[s] = True; st = [s]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if not seen[y]:
                        seen[y] = True; st.append(y)
    return c

def brute(n, edges, removals):
    banned = set(); out = [count_components(n, edges, banned)]
    for idx in removals:
        banned.add(idx); out.append(count_components(n, edges, banned))
    return out

assert optimal(4, [[0, 1], [1, 2], [2, 3]], [1, 0]) == [1, 2, 3]
assert optimal(3, [[0, 1], [0, 1], [1, 2]], [0, 1, 2]) == [1, 1, 2, 3]
print('examples:', optimal(4, [[0, 1], [1, 2], [2, 3]], [1, 0]), optimal(3, [[0, 1], [0, 1], [1, 2]], [0, 1, 2]))

# edge cases
assert optimal(1, [], []) == [1]
assert optimal(2, [[0, 0]], [0]) == [2, 2]                 # self loop never merges anything
assert optimal(5, [], []) == [5]
assert optimal(3, [[0, 1], [1, 2]], []) == [1]             # no removals: one number

random.seed(28)
for _ in range(800):
    n = random.randint(1, 8)
    m = random.randint(0, 12)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    k = random.randint(0, m)
    removals = random.sample(range(m), k)
    assert optimal(n, edges, removals) == brute(n, edges, removals), (n, edges, removals)
print('random cross-check ok: 800 cases (parallel edges and self loops included)')

N = 10**5
edges = [[i, i + 1] for i in range(N - 1)] + [[i, i + 2] for i in range(N - 2)]
removals = list(range(len(edges)))
random.shuffle(removals)
res = optimal(N, edges, removals)
assert res[0] == 1 and res[-1] == N and len(res) == len(edges) + 1
assert all(res[i] <= res[i + 1] for i in range(len(res) - 1))   # deletions never reduce the count
print('n = 10^5, 2*10^5 deletions: monotone, starts at 1, ends at', res[-1])
```

**Output (my run):**
```
examples: [1, 2, 3] [1, 1, 2, 3]
random cross-check ok: 800 cases (parallel edges and self loops included)
n = 10^5, 2*10^5 deletions: monotone, starts at 1, ends at 100000
```

**Edge cases:**
- No removals: a one-element list with the initial count.
- No edges: n, repeated.
- Self loops and parallel edges (tested).
- Removing every edge ends at n.

**Follow-ups:**
- Pacing and scoring: this is Set B, Q2 of 5, 8 minutes, 15 points. How I would pace this: 1 minute to say the offline reverse idea and the rules (distinct indices, the output has k + 1 values, initial count first), 4 minutes to code it, 1 minute on the example, 1 minute for complexity, 1 minute for edge cases and the summary. Scoring by the part header rubric (15 points): about 4.5 for stating the rules and the reversal idea before coding, 4.5 for a correct solution that passes the example and the brute-force check, 3 for stating the complexity and why, 1.5 for the edge cases, 1.5 for a crisp summary. Partial credit: the per-deletion DFS recount is correct but O(k (n + m)), so it earns correctness but little for complexity.
- Edges deleted online, without knowing the future? Needs a dynamic-connectivity structure (offline divide and conquer over time or link-cut trees), beyond this question.
- Can the count go up when adding back? No: it never rises as edges are added, so the output list is non-decreasing in the deletion order (the code asserts it).

**Common mistakes:**
- Adding all edges including the removed ones to the initial union-find.
- Forgetting to reverse the recorded list, or reversing it but dropping the initial count.
- Recursive find on a long path (recursion limit 1000).
- Recording the count before the unions of the never-deleted edges.

---

### Q29 ⭐⭐ 🟡 [Set B, Q3 of 5, 9 min, 20 pts] Connect all cities, some roads already built. `n` cities 0..n-1 (1 <= n <= 10^4), `built`, a list of [u, v] roads that already exist (cost 0), and `edges`, a list of [u, v, cost] candidate new roads (1 <= cost <= 10^6, up to 5*10^4). Return the minimum total cost of new roads so that every pair of cities is connected, or -1 when impossible even with every candidate. Kruskal (Part 9 Q29): first union the already built roads for free, then take candidate roads in increasing cost order when they join two different components (union-find, Part 9 Q13); stop counting when one component is left. O(E log E). Explain why pre-merging the free roads keeps the greedy proof valid (contracting zero-cost edges) and why Prim would need the same pre-contraction. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an exhaustive oracle that tries every subset of candidate roads (at most 10 candidates) on small inputs. Example: n=4, built=[[0, 1]], edges=[[1, 2, 5], [2, 3, 1], [0, 3, 9], [0, 2, 4]] -> 5; n=3, built=[], edges=[[0, 1, 2]] -> -1; n=1, built=[], edges=[] -> 0.
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Kruskal's minimum spanning tree with the free edges contracted first (union-find).

**Say this first (1 line):** "Union all already-built roads for free, then run Kruskal over the candidates in increasing cost, and answer -1 if more than one component remains."

**Brute force:**
- Try every subset of the candidate roads, keep those that connect all cities together with the built roads, take the cheapest. O(2^E * (n + E)); the oracle for E <= 9.

**Optimal:**
- Union-find over n cities; `comps = n`. For each built road, union (each union that merges two roots lowers `comps`).
- Sort candidates by cost. For each, if its endpoints have different roots, union them, add the cost, lower `comps`. Stop when `comps == 1`.
- At the end, `comps == 1` gives the cost; otherwise -1. n = 1 gives 0.
- Why pre-merging keeps the greedy proof valid: a built road is an edge of weight 0, and zero-weight edges are the cheapest possible, so Kruskal would take them first anyway (a cycle-forming one is skipped). Contracting them leaves the same problem on the merged components, and the cut/cycle argument for Kruskal applies unchanged. Candidates that now join two cities of one component are skipped like any cycle edge (the code tests "3 cities, built 0-1 and 1-2, candidate 0-2 cost 7 gives 0").
- Prim would need the same pre-contraction: start from the merged components (or give built edges weight 0), otherwise it may pay for an edge that a free path makes redundant.
- Greedy reference: Part 9 Q29 (Kruskal), union-find: Part 9 Q13.

**Complexity:**
- Time O(E log E) for the sort plus O((n + E) alpha(n)) for the unions. Space O(n + E).
- The brute force is exponential in E and only an oracle.

**Dry run:** n=4, built 0-1, candidates (1,2,5), (2,3,1), (0,3,9), (0,2,4).
- Built: union 0-1, comps = 3: components {0,1}, {2}, {3}.
- Sorted by cost: (2,3,1), (0,2,4), (1,2,5), (0,3,9).
- (2,3,1): different components, take it, cost 1, comps 2.
- (0,2,4): {0,1} and {2,3} differ, take it, cost 5, comps 1. Stop. Answer 5.
- Example 2: n=3, no built road, one candidate 0-1: city 2 is never reached, comps stays 2, answer -1. Example 3: n=1 needs nothing: 0.

**Code:**
```python
import random
from itertools import combinations

def optimal(n, built, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    comps = n
    for u, v in built:                       # free roads first: contract them
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; comps -= 1
    cost = 0
    for u, v, c in sorted(edges, key=lambda e: e[2]):
        if comps == 1:
            break
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; comps -= 1; cost += c
    return cost if comps == 1 else -1

def connected(n, pairs):
    parent = list(range(n))
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    for u, v in pairs:
        parent[find(u)] = find(v)
    return len({find(x) for x in range(n)}) == 1

def brute(n, built, edges):
    best = None
    for mask in range(1 << len(edges)):
        chosen = [edges[i] for i in range(len(edges)) if mask >> i & 1]
        if connected(n, list(built) + [(u, v) for u, v, _ in chosen]):
            c = sum(e[2] for e in chosen)
            if best is None or c < best: best = c
    return -1 if best is None else best

assert optimal(4, [[0, 1]], [[1, 2, 5], [2, 3, 1], [0, 3, 9], [0, 2, 4]]) == 5
assert optimal(3, [], [[0, 1, 2]]) == -1
assert optimal(1, [], []) == 0
print('examples:', optimal(4, [[0, 1]], [[1, 2, 5], [2, 3, 1], [0, 3, 9], [0, 2, 4]]), optimal(3, [], [[0, 1, 2]]), optimal(1, [], []))

# edge cases: already connected by built roads, so candidates cost nothing; duplicates; self loop candidate
assert optimal(3, [[0, 1], [1, 2]], [[0, 2, 7]]) == 0
assert optimal(2, [], [[0, 1, 9], [0, 1, 4], [1, 1, 1]]) == 4
assert optimal(3, [[0, 1]], [[1, 2, 6], [0, 2, 3]]) == 3

random.seed(29)
for _ in range(600):
    n = random.randint(1, 6)
    built = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 3))]
    edges = [[random.randrange(n), random.randrange(n), random.randint(1, 9)] for _ in range(random.randint(0, 9))]
    assert optimal(n, built, edges) == brute(n, built, edges), (n, built, edges)
print('random cross-check ok: 600 cases against all subsets of <= 9 candidates')

# why contraction is needed: without pre-merging, Kruskal wastes budget on a road that is already implied
n, built, edges = 3, [[0, 1]], [[0, 1, 1], [1, 2, 5]]
print('with free road 0-1, answer =', optimal(n, built, edges), '(buying the cost-1 duplicate would add 1 for nothing)')
assert optimal(n, built, edges) == 5

N = 10**4
edges = [[i, i + 1, random.randint(1, 10**6)] for i in range(N - 1)] + [[random.randrange(N), random.randrange(N), random.randint(1, 10**6)] for _ in range(4 * 10**4)]
print('n = 10^4, 5*10^4 candidates -> cost', optimal(N, [], edges))
```

**Output (my run):**
```
examples: 5 -1 0
random cross-check ok: 600 cases against all subsets of <= 9 candidates
with free road 0-1, answer = 5 (buying the cost-1 duplicate would add 1 for nothing)
n = 10^4, 5*10^4 candidates -> cost 1161494664
```

**Edge cases:**
- Already connected by built roads: 0, whatever the candidates.
- n = 1: 0. Disconnected even with everything: -1.
- Self loop candidates and duplicate candidates (the cheaper one is picked, tested).
- Built roads that form a cycle: the extra union is a no-op.

**Follow-ups:**
- Pacing and scoring: this is Set B, Q3 of 5, 9 minutes, 20 points. How I would pace this: 2 minutes to state the plan and the rules (built roads are free, return -1 if impossible, n = 1 is 0), 4 minutes to code, 1 minute to run the example, 1 minute for complexity and the contraction argument, 1 minute spare for edge cases and the summary. Scoring by the part header rubric (20 points): about 6 for stating the rules and plan, 6 for a correct solution passing the example and a random subset-oracle check, 4 for the complexity and why, 2 for the edge cases, 2 for the spoken summary. Partial credit: plain Kruskal that ignores the built roads is a common wrong answer (example 1 would give 10, not 5); it earns the rules and complexity points but not the correctness points.
- Must the chosen roads form a tree? The cost is the same as a spanning forest over components, since extra roads only add cost (all costs are at least 1).
- Dense graph? Prim with a heap, with built roads contracted first (Part 9 Q37).

**Common mistakes:**
- Treating built roads as candidates of cost 0 inside the sort but forgetting the -1 check.
- Counting components wrongly (starting `comps` at n but not decrementing during the free unions).
- Returning the partial cost instead of -1 when the graph stays disconnected.
- Recursive find on long chains (use halving).

---

### Q30 ⭐⭐ 🟡 [Set C, Q1 of 4, 8 min, 15 pts] Range frequency queries. Implement class `RangeFreqQuery(arr)` (1 <= len <= 10^5, 1 <= value <= 10^4) with `query(left, right, value)` returning how many times `value` occurs in arr[left..right] (both ends included, 0 <= left <= right < len). Store, for each value, the sorted list of its positions (Part 1 style dict of lists); a query is two bisect calls: `bisect_right(pos, right) - bisect_left(pos, left)` (bounds semantics: Part 5 Q11, and the first/last position idea of Part 5 Q4), O(log k) per query and O(n) memory; a value that never occurs counts 0. Say why a prefix-count table per value would use O(n * distinct) memory and when it is still the right choice. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], ops=[['query', [1, 2, 4]], ['query', [0, 11, 33]], ['query', [3, 3, 56]], ['query', [0, 11, 99]], ['query', [4, 8, 22]]] -> [1, 2, 1, 0, 2].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Per-value sorted position lists plus two binary searches (`bisect_left`, `bisect_right`).

**Say this first (1 line):** "For each value I keep the sorted list of its positions; a query counts positions in [left, right] with `bisect_right(right) - bisect_left(left)`."

**Brute force:**
- Slice `arr[left:right+1]` and `.count(value)` on every query. O(n) per query. My oracle.

**Optimal:**
- Constructor: one pass, `pos[v].append(i)`. Indices arrive in increasing order, so every list is already sorted. O(n) time and memory.
- `query(left, right, value)`: look the list up with `.get` (an unseen value gives 0 and must not add a key). Then `bisect_right(p, right) - bisect_left(p, left)`.
- Bounds, both ends inclusive: `bisect_left(p, left)` is the first position >= left; `bisect_right(p, right)` is one past the last position <= right (semantics: Part 5 Q11; the first/last position idea: Part 5 Q4).
- Why not a prefix-count table per value: it needs (n + 1) cells for every distinct value, which for n = 10^5 and 10^4 distinct values is about 10^9 cells. It is still the right choice when the number of distinct values is tiny (say 2 to 26 letters) and you want O(1) queries.

**Complexity:**
- Build O(n). Query O(log k) for k occurrences of the value (at most log n). Space O(n).
- Thread safety (concept only): after construction the structure is read-only, so concurrent queries need no lock; a version with an `append` method would need a lock.

**Dry run:** arr = [12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56], positions: 12: [0, 9]; 33: [1, 7]; 4: [2]; 56: [3, 11]; 22: [4, 8]; 2: [5]; 34: [6, 10].
- query(1, 2, 4): p = [2]. `bisect_right(p, 2)` = 1, `bisect_left(p, 1)` = 0. Result 1.
- query(0, 11, 33): p = [1, 7]: 2 - 0 = 2. query(3, 3, 56): p = [3, 11]: right(3) = 1, left(3) = 0: 1.
- query(0, 11, 99): no list: 0.
- query(4, 8, 22): p = [4, 8]: right(8) = 2, left(4) = 0: 2.

**Code:**
```python
import random
from bisect import bisect_left, bisect_right
from collections import defaultdict

class RangeFreqQuery:
    def __init__(self, arr):
        self.pos = defaultdict(list)
        for i, v in enumerate(arr):                  # positions are appended in increasing order, so each list is sorted
            self.pos[v].append(i)

    def query(self, left, right, value):             # O(log k), k = occurrences of value
        p = self.pos.get(value)                      # .get: do not create an entry for an unseen value
        if not p:
            return 0
        return bisect_right(p, right) - bisect_left(p, left)

class Naive:
    def __init__(self, arr): self.a = list(arr)
    def query(self, left, right, value): return self.a[left:right + 1].count(value)

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

arr = [12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]
ops = [['query', [1, 2, 4]], ['query', [0, 11, 33]], ['query', [3, 3, 56]], ['query', [0, 11, 99]], ['query', [4, 8, 22]]]
assert run(RangeFreqQuery, [arr], ops) == [1, 2, 1, 0, 2]
print('example:', run(RangeFreqQuery, [arr], ops))

# bounds: both ends inclusive
q = RangeFreqQuery([5, 5, 5, 5])
assert q.query(0, 3, 5) == 4 and q.query(1, 2, 5) == 2 and q.query(2, 2, 5) == 1 and q.query(0, 0, 6) == 0
assert len(q.pos) == 1                                # querying an unseen value did not add a key
assert RangeFreqQuery([1]).query(0, 0, 1) == 1

random.seed(30)
n_ops = 0
for _ in range(500):
    n = random.randint(1, 20)
    arr = [random.randint(1, 5) for _ in range(n)]
    ops = []
    for _ in range(30):
        l = random.randrange(n); r = random.randint(l, n - 1)
        ops.append(['query', [l, r, random.randint(1, 7)]])      # 6 and 7 never occur
    assert run(RangeFreqQuery, [arr], ops) == run(Naive, [arr], ops), (arr, ops)
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 arrays,', n_ops, 'queries')

# memory claim: a prefix-count table per value needs (n + 1) * distinct cells
n, distinct = 10**5, 10**4
print('prefix table cells for n = 10^5 and 10^4 distinct values:', (n + 1) * distinct, 'vs positions lists:', n)
big = [random.randint(1, 10**4) for _ in range(10**5)]
f = RangeFreqQuery(big)
assert sum(len(v) for v in f.pos.values()) == 10**5
for _ in range(2000):
    l = random.randrange(10**5); r = random.randint(l, 10**5 - 1); v = random.randint(1, 10**4)
    assert f.query(l, r, v) == big[l:r + 1].count(v)
print('n = 10^5, 2000 random queries ok')
```

**Output (my run):**
```
example: [1, 2, 1, 0, 2]
operation-sequence oracle ok: 500 arrays, 15000 queries
prefix table cells for n = 10^5 and 10^4 distinct values: 1000010000 vs positions lists: 100000
n = 10^5, 2000 random queries ok
```

**Edge cases:**
- Value never present: 0, without creating a dict entry (tested with `len(q.pos)`).
- left == right, whole array, all elements equal.
- Single element array.
- Both ends inclusive: using `bisect_left` for the right end undercounts a match at `right`.

**Follow-ups:**
- Pacing and scoring: this is Set C, Q1 of 4, 8 minutes, 15 points. How I would pace this: 1 minute to state the rules (inclusive ends, absent value is 0), 3 minutes to code the dict of lists and the two bisects, 1 minute to run the example, 1 minute for complexity and the prefix-table memory remark, 2 minutes spare for edge cases and the summary. Scoring by the part header rubric (15 points): about 4.5 for stating the rules before coding, 4.5 for a correct solution passing the example and a random operation-sequence check, 3 for the complexity and why, 1.5 for the edge cases, 1.5 for a crisp summary. Partial credit: the slice-and-count version is correct but O(n) per query, so it gets correctness but no complexity points.
- Updates to the array? Positions lists need insertion into a sorted list (`insort`, O(k)); for heavy updates use a structure per value or an offline BIT.
- Why not a segment tree? It could answer "how many equal" only by storing a counter per node (too much memory with 10^4 values).

**Common mistakes:**
- `bisect_right` on the left bound, or `bisect_left` on the right bound.
- `pos[value]` on a defaultdict, which silently creates empty entries for absent values.
- Treating `right` as exclusive.
- Building the position lists by sorting each one again (unneeded).

---

### Q31 ⭐⭐ 🟡 [Set D, Q2 of 4, 10 min, 25 pts] Leader at any past time (online election). Implement class `TopVotedCandidate(persons, times)`: vote i was cast for `persons[i]` at time `times[i]` (strictly increasing times, 1 <= len <= 5000, persons are small integers). `q(t)` (with t >= times[0]) returns the person who is leading at time t counting all votes cast at times <= t; if several people tie for the lead, the one whose most recent vote is the latest wins. Precompute in the constructor the leader after each vote (a Counter and the rule `count[p] >= count[leader]` makes the newest voter win ties), then answer `q(t)` with `bisect_right(times, t) - 1` (bounds semantics: Part 5 Q11), O(log n) per query. Say why a tie goes to the person who just voted and what changes if the rule were 'smallest id wins'. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]], ops=[['q', [3]], ['q', [12]], ['q', [25]], ['q', [15]], ['q', [24]], ['q', [8]]] -> [0, 1, 1, 0, 0, 1].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Precompute then binary search. Replay the votes once, store the leader after each vote, and answer each query with `bisect_right` on the (strictly increasing) vote times. Online-assessment design question with a tie rule.

**Say this first (1 line):** "Rules first: a vote at time exactly t counts, a tie goes to whoever voted most recently, q is only asked for t >= times[0]; then I precompute the leader after every vote and binary search the time."

**Brute force:** For each `q(t)`, rescan all votes with time <= t, count per person, track each person's last vote index, and pick the max count with the latest last vote. O(n) per query, O(1) extra space. Fine for the oracle, too slow for many queries.

**Optimal:**
- Constructor: walk the votes with a `Counter`. After vote `p`, set `leader = p` when `count[p] >= count[leader]`, else keep the old leader. Append `leader` to `lead`.
- Query: `i = bisect_right(times, t) - 1` is the last vote cast at a time <= t (a vote exactly at t counts; Part 5 Q11 has the bound semantics). Return `lead[i]`.
- Why a tie goes to the voter who just voted: when `p` votes and `count[p] == count[leader]`, p now has the most recent vote of anyone. The rule says the most recent vote wins a tie, so p wins. If `count[p] > count[leader]`, p simply leads. If `count[p] < count[leader]`, the leader keeps the lead. The invariant is: after each vote, `leader` is the right answer for that prefix. With three or more people tied, the old leader was already the newest voter in the tied group, and p is newer still.
- If the rule were "smallest id wins": `>=` is no longer enough. You need `count[p] > count[leader] or (count[p] == count[leader] and p < leader)`. This works because the leader is always the smallest id in the max group, so one comparison keeps it that way. The code runs this variant too, against its own naive oracle.
- Thread safety (concept only): after the constructor the object is read-only (`times` and `lead` never change), so concurrent `q` calls need no lock. If votes could be appended while queries run, appends and queries would need a read-write lock, or an immutable snapshot swapped in atomically.

**Complexity:**
- Constructor: O(n) time, O(n) space for `lead` and the counter (one pass, O(1) per vote).
- `q(t)`: O(log n) time, O(1) extra space (one `bisect_right`).
- Naive reference: O(n) per query.

**Dry run:** `persons = [0,1,1,0,0,1,0]`, `times = [0,5,10,15,20,25,30]`.
- Vote 0 (person 0): count0=1, no leader yet so leader 0.
- Vote 1 (person 1): count1=1 >= count0=1, so leader 1 (tie, newest voter).
- Vote 2 (person 1): count1=2, leader 1.
- Vote 3 (person 0): count0=2 >= count1=2, leader 0.
- Vote 4 (person 0): count0=3, leader 0. Vote 5 (person 1): count1=3 >= 3, leader 1. Vote 6 (person 0): count0=4, leader 0.
- `lead = [0,1,1,0,0,1,0]`.
- `q(3)`: `bisect_right(times, 3) = 1`, index 0, answer 0. `q(12)`: 3 votes <= 12, index 2, answer 1. `q(25)`: index 5, answer 1. `q(15)`: index 3, answer 0. `q(24)`: index 4, answer 0. `q(8)`: index 1, answer 1.
- Result `[0, 1, 1, 0, 0, 1]`, matches the example.

**Code:**
```python
import random
from bisect import bisect_right
from collections import Counter, defaultdict

random.seed(3101)


class TopVotedCandidate:
    """Leader after each vote is precomputed; ties go to the person who voted most recently."""

    def __init__(self, persons, times):
        self.times = list(times)
        self.lead = []                      # lead[i] = leader right after vote i
        cnt = Counter()
        leader = None
        for p in persons:
            cnt[p] += 1
            if leader is None or cnt[p] >= cnt[leader]:   # >= : a tie goes to the newest voter
                leader = p
            self.lead.append(leader)

    def q(self, t):                         # O(log n)
        return self.lead[bisect_right(self.times, t) - 1]


class TopVotedSmallestId(TopVotedCandidate):
    """Variant: ties go to the smallest id. Needs the extra id comparison."""

    def __init__(self, persons, times):
        self.times = list(times)
        self.lead = []
        cnt = Counter()
        leader = None
        for p in persons:
            cnt[p] += 1
            if leader is None or cnt[p] > cnt[leader] or (cnt[p] == cnt[leader] and p < leader):
                leader = p
            self.lead.append(leader)


class Naive:
    """Rescan every vote with time <= t; tie -> the person whose last vote is latest."""

    def __init__(self, persons, times):
        self.p, self.t = list(persons), list(times)

    def q(self, t):
        cnt, last = defaultdict(int), {}
        for i, (p, tt) in enumerate(zip(self.p, self.t)):
            if tt > t:
                break
            cnt[p] += 1
            last[p] = i
        top = max(cnt.values())
        return max((last[p], p) for p in cnt if cnt[p] == top)[1]


class NaiveSmallestId:
    def __init__(self, persons, times):
        self.p, self.t = list(persons), list(times)

    def q(self, t):
        cnt = Counter(p for p, tt in zip(self.p, self.t) if tt <= t)
        top = max(cnt.values())
        return min(p for p in cnt if cnt[p] == top)


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's example, run through the same op format ---
init = [[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]]
ops = [['q', [3]], ['q', [12]], ['q', [25]], ['q', [15]], ['q', [24]], ['q', [8]]]
got = run(TopVotedCandidate, init, ops)
print('example:', got)
assert got == [0, 1, 1, 0, 0, 1] == run(Naive, init, ops)
print('leader after each vote:', TopVotedCandidate(*init).lead)

# --- random operation-sequence oracle (both tie rules) ---
checked = 0
for _ in range(600):
    n = random.randint(1, 12)
    persons = [random.randint(0, 3) for _ in range(n)]
    times = sorted(random.sample(range(0, 40), n))
    ops = [['q', [random.randint(times[0], 45)]] for _ in range(15)]
    ops += [['q', [t]] for t in times] + [['q', [t - 1]] for t in times if t - 1 >= times[0]]   # boundaries
    assert run(TopVotedCandidate, [persons, times], ops) == run(Naive, [persons, times], ops)
    assert run(TopVotedSmallestId, [persons, times], ops) == run(NaiveSmallestId, [persons, times], ops)
    checked += len(ops)
print('random queries compared (both tie rules):', checked)

# --- the two tie rules really differ ---
persons, times = [0, 1], [1, 2]            # after time 2: 0 and 1 tied 1-1
print('tie 0 vs 1 at t=2: newest-voter ->', TopVotedCandidate(persons, times).q(2),
      '| smallest-id ->', TopVotedSmallestId(persons, times).q(2))

# --- edge cases ---
assert TopVotedCandidate([7], [3]).q(3) == 7 and TopVotedCandidate([7], [3]).q(10 ** 9) == 7   # single vote
assert TopVotedCandidate([0, 1], [1, 2]).q(1) == 0       # t exactly on a vote counts that vote
assert TopVotedCandidate([0, 1], [1, 2]).q(2) == 1       # tie 1-1 at t=2: newest voter
assert TopVotedCandidate([0, 0, 1], [1, 2, 3]).q(3) == 0  # 2-1, no tie
big = TopVotedCandidate([i % 5 for i in range(5000)], list(range(1, 5001)))
assert big.q(5000) == 4 and big.q(1) == 0                  # n = 5000: ties go to the newest voter
print('edge asserts passed')
```

**Output (my run):**
```
example: [0, 1, 1, 0, 0, 1]
leader after each vote: [0, 1, 1, 0, 0, 1, 0]
random queries compared (both tie rules): 16420
tie 0 vs 1 at t=2: newest-voter -> 1 | smallest-id -> 0
edge asserts passed
```

**Edge cases:**
- Single vote: every `t >= times[0]` returns that person.
- `t` exactly equal to a vote time counts that vote (`bisect_right`, not `bisect_left`).
- `t` far beyond the last vote returns the final leader.
- A tie after the very first votes (1-1) goes to the second voter.
- Persons can be any small integers including 0, so the code uses `None` and not `-1` as "no leader yet".
- n = 5000 with five persons voting in rotation (checked): ties are constant, the newest voter wins each time.

**Follow-ups:**
- *Votes can arrive online (append only)?* Keep the `Counter`, current leader and the `times`/`lead` lists as running state; `vote(p, t)` is the same O(1) step. Queries stay O(log n) because times are increasing.
- *Query "top 3 at time t"?* Then one leader is not enough. You need a persistent structure or an offline sweep; say so rather than extend the array trick.
- *Scoring note (Set D, Q2 of 4, 25 pts):* rules spoken first (>= counts the vote at t, tie to newest voter, empty input not asked) = 7.5; correct code that passes the example and the random check against the naive rescan = 7.5; complexity O(n) build and O(log n) query with the reason = 5; edge cases (single vote, t on a vote time, n = 5000) = 2.5; a 60-second summary = 2.5. Partial credit: a correct O(n)-per-query rescan with the rules stated earns roughly 12 of 25; a correct build with the tie rule wrong (using `>`) loses most of the solution points. How I would pace this: about 10 minutes, so roughly 2 to state rules and the tie argument, 5 to code and run the example, 2 for the random test and 1 for the summary.

**Common mistakes:**
- Using `>` instead of `>=` (ties then keep the older leader, which is wrong under this rule).
- `bisect_left` (a vote exactly at t is dropped) or forgetting the `- 1`.
- Using `-1` as the "no leader" sentinel when persons can be 0 or negative.
- Recomputing counts per query (O(n) each).
- Assuming the leader is whoever last voted, rather than comparing counts.

### Q32 ⭐⭐ 🔴 LFU cache with O(1) operations. Implement class `LFUCache(capacity)` (0 <= capacity <= 10^4) with `get(key)` and `put(key, value)`, both O(1) on average. `get` returns the value or -1. Every successful `get` and every `put` (new or existing key) counts as one use of that key; a new key starts with frequency 1. When a NEW key arrives while the cache holds `capacity` keys, first evict the key with the smallest use count and, among keys with equal counts, the least recently used one (recency counts both gets and puts); then insert. `put` on an existing key replaces the value, adds one use and refreshes its recency. With capacity 0 every `put` does nothing and every `get` returns -1. `put` returns None. Use a dict key -> (value, freq), a dict freq -> OrderedDict of keys, and a `min_freq` pointer; explain why `min_freq` can be updated in O(1) (it becomes 1 on an insert and moves from f to f + 1 only when bucket f empties). State why a heap of (freq, time) would be O(log n). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[2], ops=[['put', [1, 1]], ['put', [2, 2]], ['get', [1]], ['put', [3, 3]], ['get', [2]], ['get', [3]], ['put', [4, 4]], ['get', [1]], ['get', [3]], ['get', [4]]] -> [null, null, 1, null, -1, 3, null, -1, 3, 4]; init=[0], ops=[['put', [0, 0]], ['get', [0]]] -> [null, -1].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** O(1) cache design with frequency buckets. A dict of values, a dict of use counts, `freq -> OrderedDict` buckets (keys in recency order inside each bucket) and a `min_freq` pointer.

**Say this first (1 line):** "Eviction rule first: smallest use count, ties broken by least recently used, gets and puts both count as a use, new keys start at 1; then buckets per frequency make every operation O(1)."

**Brute force:** Keep `[value, uses, last-use stamp]` per key and, on a new key at capacity, scan all keys for the minimum `(uses, stamp)`. get is O(1), put with eviction is O(capacity). A heap of `(uses, stamp, key)` with lazy deletion (also in the code) makes eviction O(log n) amortised, but every get and put pushes a heap entry, so every operation costs O(log n), not O(1).

**Optimal:**
- State: `val[key]`, `freq[key]`, `buckets[f]` = an `OrderedDict` of the keys with count f (oldest use first), and `min_freq`.
- Touch (a successful get, or a put on an existing key): remove the key from bucket f, add it to the END of bucket f + 1, set `freq[key] = f + 1`. If bucket f is now empty, delete it, and if `min_freq == f` set `min_freq = f + 1`.
- Why `min_freq` is O(1) to maintain: it only changes in two ways. (1) Inserting a new key gives count 1, which is always the smallest, so `min_freq = 1`. (2) A touch moves a key from f to f + 1; the minimum can only rise when the key came from the minimum bucket and that bucket just emptied, and then the new minimum is exactly f + 1 (the key itself is there). Eviction deletes from bucket `min_freq`, and the very next step inserts a new key, which resets `min_freq` to 1. No scan is ever needed.
- Evict (new key, cache full): `buckets[min_freq].popitem(last=False)` removes the oldest-used key of the lowest count. That is exactly "smallest count, then least recently used".
- Existing key at capacity: no eviction, it is only an update plus a touch.
- Capacity 0: put does nothing, get returns -1.
- Thread safety (concept only): get mutates counts and buckets, so even reads need a lock; a single mutex over the whole cache is the simple answer, sharding by key hash gives parallelism but then the global "lowest count" is per shard (approximate LFU).

**Complexity:**
- `get`: O(1) average (dict lookups, `OrderedDict` delete and append are O(1)).
- `put`: O(1) average (including eviction via `popitem(last=False)`).
- Space O(capacity): the three dicts and the buckets hold each key once.
- Heap version: O(log n) per get and put because each use pushes an entry; stale entries also inflate memory until popped.

**Dry run:** capacity 2, ops from the first example.
- `put 1`, `put 2`: bucket1 = {1, 2} (1 older), `min_freq = 1`.
- `get 1` -> 1: key 1 moves to bucket2; bucket1 = {2} is not empty, `min_freq` stays 1.
- `put 3`: full, evict oldest of bucket1 = key 2; insert 3 at count 1; bucket1 = {3}, bucket2 = {1}.
- `get 2` -> -1. `get 3` -> 3: bucket1 empties and `min_freq == 1`, so `min_freq = 2`; bucket2 = {1, 3}.
- `put 4`: full, evict oldest of bucket2 = key 1 (equal counts, 1 is least recent); insert 4 at count 1, `min_freq = 1`.
- `get 1` -> -1, `get 3` -> 3, `get 4` -> 4. Result `[None, None, 1, None, -1, 3, None, -1, 3, 4]`. The second example (capacity 0) gives `[None, -1]`.

**Code:**
```python
import heapq
import random
from collections import OrderedDict, defaultdict

random.seed(3201)


class LFUCache:
    """O(1) average get/put. freq -> OrderedDict (oldest use first), plus a min_freq pointer."""

    def __init__(self, capacity):
        self.cap = capacity
        self.val = {}                               # key -> value
        self.freq = {}                              # key -> use count
        self.buckets = defaultdict(OrderedDict)     # count -> keys in recency order (LRU first)
        self.min_freq = 0

    def _touch(self, key):                          # one more use: move key from bucket f to f + 1
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:                  # the only way min_freq can move up
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None             # newest end of the new bucket

    def get(self, key):
        if key not in self.val:
            return -1
        self._touch(key)
        return self.val[key]

    def put(self, key, value):
        if self.cap == 0:
            return None
        if key in self.val:                         # existing key: replace, one use, refresh recency
            self.val[key] = value
            self._touch(key)
            return None
        if len(self.val) == self.cap:               # new key at capacity: evict (lowest count, then LRU)
            victim, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.val[victim]
            del self.freq[victim]
        self.val[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1                           # a new key always has the smallest count
        return None


class NaiveLFU:
    """Reference: every key keeps [value, uses, last-use stamp]; evict by scanning for min (uses, stamp)."""

    def __init__(self, capacity):
        self.cap, self.d, self.clock = capacity, {}, 0

    def get(self, key):
        if key not in self.d:
            return -1
        self.clock += 1
        e = self.d[key]
        e[1] += 1
        e[2] = self.clock
        return e[0]

    def put(self, key, value):
        if self.cap == 0:
            return None
        self.clock += 1
        if key in self.d:
            e = self.d[key]
            e[0], e[1], e[2] = value, e[1] + 1, self.clock
            return None
        if len(self.d) == self.cap:
            victim = min(self.d, key=lambda k: (self.d[k][1], self.d[k][2]))
            del self.d[victim]
        self.d[key] = [value, 1, self.clock]
        return None


class HeapLFU:
    """The O(log n) alternative: lazy heap of (uses, stamp, key). Shown only to count the cost."""

    def __init__(self, capacity):
        self.cap, self.d, self.h, self.clock = capacity, {}, [], 0   # d: key -> [value, uses, stamp]

    def _push(self, key):
        self.clock += 1
        e = self.d[key]
        e[2] = self.clock
        heapq.heappush(self.h, (e[1], e[2], key))   # O(log n) on EVERY get/put

    def get(self, key):
        if key not in self.d:
            return -1
        self.d[key][1] += 1
        self._push(key)
        return self.d[key][0]

    def put(self, key, value):
        if self.cap == 0:
            return None
        if key in self.d:
            self.d[key][0] = value
            self.d[key][1] += 1
            self._push(key)
            return None
        if len(self.d) == self.cap:
            while True:                             # skip stale entries
                u, s, k = heapq.heappop(self.h)
                if k in self.d and self.d[k][1] == u and self.d[k][2] == s:
                    del self.d[k]
                    break
        self.d[key] = [value, 1, 0]
        self._push(key)
        return None


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's examples ---
ops1 = [['put', [1, 1]], ['put', [2, 2]], ['get', [1]], ['put', [3, 3]], ['get', [2]],
        ['get', [3]], ['put', [4, 4]], ['get', [1]], ['get', [3]], ['get', [4]]]
r1 = run(LFUCache, [2], ops1)
print('example 1:', r1)
assert r1 == [None, None, 1, None, -1, 3, None, -1, 3, 4]
r2 = run(LFUCache, [0], [['put', [0, 0]], ['get', [0]]])
print('example 2:', r2)
assert r2 == [None, -1]

# --- random operation-sequence oracle (small key space forces many evictions and ties) ---
total = 0
for _ in range(800):
    cap = random.randint(0, 4)
    ops = []
    for _ in range(random.randint(1, 40)):
        k = random.randint(0, 5)
        ops.append(['get', [k]] if random.random() < 0.4 else ['put', [k, random.randint(0, 99)]])
    a, b, c = run(LFUCache, [cap], ops), run(NaiveLFU, [cap], ops), run(HeapLFU, [cap], ops)
    assert a == b == c, (cap, ops)
    total += len(ops)
print('random ops compared (3 implementations):', total)

# --- min_freq invariant: after every op it equals the true minimum count ---
for _ in range(300):
    c = LFUCache(3)
    for _ in range(40):
        k = random.randint(0, 6)
        c.get(k) if random.random() < 0.5 else c.put(k, 0)
        if c.freq:
            assert c.min_freq == min(c.freq.values())
            assert all(c.buckets[f] for f in c.buckets)   # no empty buckets are kept
print('min_freq invariant held')

# --- tie rule demo: equal counts -> evict the least recently used (gets count as use) ---
c = LFUCache(2)
c.put(1, 'a'); c.put(2, 'b')          # both count 1; key 1 is older
c.put(3, 'c')                         # evicts 1 (tie -> LRU)
print('after put 3, get 1 ->', c.get(1), '| get 2 ->', c.get(2))   # 2 now has count 2
c.put(4, 'd')                         # 3 has count 1, 2 has count 2 -> evict 3
print('after put 4, get 3 ->', c.get(3), '| get 2 ->', c.get(2), '| get 4 ->', c.get(4))

# --- edge cases ---
z = LFUCache(0); assert z.put(1, 1) is None and z.get(1) == -1
o = LFUCache(1); o.put(1, 1); o.put(1, 5); assert o.get(1) == 5      # update at capacity: no eviction
o.put(2, 2); assert o.get(1) == -1 and o.get(2) == 2                 # new key evicts the only key
h = LFUCache(2); h.put(1, 1); h.put(2, 2)
for _ in range(5): h.get(1)
h.put(3, 3); assert h.get(2) == -1 and h.get(1) == 1                 # hot key survives (count 6 vs 1)
big = LFUCache(10 ** 4)
for i in range(2 * 10 ** 4): big.put(i, i)
assert len(big.val) == 10 ** 4 and big.get(0) == -1 and big.get(2 * 10 ** 4 - 1) == 2 * 10 ** 4 - 1
print('edge asserts passed')
```

**Output (my run):**
```
example 1: [None, None, 1, None, -1, 3, None, -1, 3, 4]
example 2: [None, -1]
random ops compared (3 implementations): 16627
min_freq invariant held
after put 3, get 1 -> -1 | get 2 -> b
after put 4, get 3 -> -1 | get 2 -> b | get 4 -> d
edge asserts passed
```

**Edge cases:**
- Capacity 0: put is a no-op, get is -1 (checked).
- `put` of an existing key at capacity does not evict and adds one use.
- A new key evicts even if it will be used heavily later: it starts at count 1.
- Capacity 1: every new key evicts the only key.
- A hot key (count 6) survives against a count-1 key even if it was used longer ago.
- Capacity 10^4 with 2 * 10^4 puts (checked).

**Follow-ups:**
- *Why not LRU order across all keys plus a count?* Evicting "lowest count" then needs a scan or a heap; buckets turn it into a pop.
- *What is the weakness of LFU?* An old key with a huge count never leaves (cache pollution). Real systems age counts (decay) or use windowed variants such as TinyLFU (editor knowledge, not tested here).
- *Thread safety?* One lock around every public method, because get changes state; finer locking must still protect the `min_freq` update with the bucket move.

**Common mistakes:**
- Not counting a `put` on an existing key as a use (or not refreshing its recency).
- Forgetting to reset `min_freq = 1` on insert, or to bump it when the minimum bucket empties.
- Evicting before checking whether the key already exists (evicting on an update).
- Using a plain `list` or `set` per bucket so the oldest key is not available in O(1).
- Leaving empty buckets in the dict and then reading `buckets[min_freq]` on an empty one.
- Forgetting the capacity 0 case.

### Q33 ⭐⭐ 🔴 Bridges in an undirected graph (critical connections). `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges`, a list of undirected [u, v] pairs (0 <= len <= 2*10^5; the graph may be disconnected, may contain parallel edges and self loops). A bridge is an edge whose removal increases the number of connected components. Return the bridges as [min(u, v), max(u, v)] pairs sorted ascending, each bridge once. Use the DFS discovery time `disc` and `low` (the smallest discovery time reachable from the subtree using at most one back edge): the tree edge (p, u) is a bridge exactly when low[u] > disc[p]. Skip the PARENT EDGE BY EDGE INDEX, not by parent node, so that two parallel edges between p and u are correctly not bridges. Write it iteratively (an explicit stack of (node, parent edge, next neighbour index)): a path of 10^5 nodes exceeds CPython's default recursion limit of 1000. The articulation-point variant is Q42. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that removes each edge in turn and recounts connected components on small inputs. Example: n=5, edges=[[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [[1, 3], [3, 4]]; n=2, edges=[[0, 1], [0, 1]] -> []; n=6, edges=[[0, 1], [2, 3], [3, 4], [4, 2], [5, 5]] -> [[0, 1]].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** DFS lowlink (Tarjan style) for bridges. Each node gets a discovery time `disc` and a `low` value, the smallest discovery time reachable from its subtree using tree edges plus at most one back edge.

**Say this first (1 line):** "Tree edge (p, u) is a bridge exactly when low[u] > disc[p], I skip the parent by EDGE INDEX so parallel edges work, and I do it with an explicit stack because 10^5 nodes break the recursion limit."

**Brute force:** For each edge, remove it and recount connected components (union-find or BFS); if the count goes up, it is a bridge. O(E * (V + E)). This is the oracle in the code.

**Optimal:**
- One DFS per unvisited node (the graph may be disconnected). `disc[u]` is the visit order; `low[u]` starts at `disc[u]`.
- For a neighbour `v` of `u` through edge `e`:
  - If `e` is the edge we arrived by, skip it (by index).
  - If `v` is unvisited: tree edge, descend. When `v` finishes, `low[u] = min(low[u], low[v])`, and if `low[v] > disc[u]` nothing in v's subtree reaches u or above, so (u, v) is a bridge.
  - If `v` is visited: back edge, `low[u] = min(low[u], disc[v])`.
- Parent by index, not by node: with two parallel edges between p and u, the second edge to p must count as a back edge. Skipping the parent node would hide it and wrongly report a bridge.
- Self loops are dropped when building adjacency (they cannot be bridges). Output is deduplicated, `[min, max]`, sorted.
- Iterative form: the stack holds `(node, parent edge, next neighbour position)`. Pop a frame; if neighbours remain, push the frame back with the position advanced, then either skip, push the child, or update `low`. When a frame has no neighbours left, the node is finished: the frame now on top is its parent, so update the parent's `low` and test the bridge condition.
- Recursion is not allowed here: a path of 10^5 nodes goes 10^5 frames deep and CPython stops at 1000. The code shows the recursive version failing on a 1600-node path.
- Thread safety: not relevant (pure function on its input).

**Complexity:** Time O(V + E): every adjacency entry is visited once per direction, `min` and set operations are O(1). Space O(V + E) for adjacency, `disc`, `low`, the stack (up to V frames) and the result. Sorting the output is O(B log B) for B bridges.

**Dry run:** `n = 5`, edges `[0,1] [1,2] [2,0] [1,3] [3,4]` (edge indexes 0 to 4).
- Start at 0: `disc0 = 0`. Go to 1 (edge 0): `disc1 = 1`. From 1, edge 0 is the parent edge, skip. Go to 2 (edge 1): `disc2 = 2`.
- At 2: edge 1 is the parent edge, skip. Edge 2 reaches 0, already visited: back edge, `low2 = min(2, 0) = 0`. Node 2 finishes: parent 1 gets `low1 = 0`. Test `low2 = 0 > disc1 = 1`? No, so (1, 2) is not a bridge.
- Back at 1: edge 3 to 3: `disc3 = 3`; then edge 4 to 4: `disc4 = 4`. Node 4 finishes: `low3 = 3`; `low4 = 4 > disc3 = 3`, so (3, 4) is a bridge.
- Node 3 finishes: `low1` stays 0; `low3 = 3 > disc1 = 1`, so (1, 3) is a bridge.
- Node 1 finishes: `low1 = 0 > disc0 = 0`? No. Result `[[1, 3], [3, 4]]`.

**Code:**
```python
import random
import sys

random.seed(3301)


def bridges(n, edges):
    """Iterative lowlink DFS. Stack frames: (node, parent edge index, next neighbour position)."""
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:                                   # a self loop is never a bridge
            g[u].append((v, i))
            g[v].append((u, i))
    disc = [-1] * n
    low = [0] * n
    timer = 0
    found = set()
    for s in range(n):                               # graph may be disconnected
        if disc[s] != -1:
            continue
        disc[s] = low[s] = timer
        timer += 1
        stack = [(s, -1, 0)]
        while stack:
            u, pe, i = stack.pop()
            if i < len(g[u]):
                stack.append((u, pe, i + 1))         # come back for the next neighbour
                v, e = g[u][i]
                if e == pe:                          # skip the parent EDGE (by index), not the parent node
                    continue
                if disc[v] == -1:                    # tree edge: descend
                    disc[v] = low[v] = timer
                    timer += 1
                    stack.append((v, e, 0))
                else:                                # back edge (or forward edge to a finished node)
                    low[u] = min(low[u], disc[v])
            elif stack:                              # u is finished: report to its parent p
                p = stack[-1][0]
                low[p] = min(low[p], low[u])
                if low[u] > disc[p]:
                    found.add((min(u, p), max(u, p)))
    return sorted([a, b] for a, b in found)


def recursive_bridges(n, edges):                     # the version the prompt forbids; shown only to fail
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i)); g[v].append((u, i))
    disc = [-1] * n; low = [0] * n; out = []; t = [0]

    def dfs(u, pe):
        disc[u] = low[u] = t[0]; t[0] += 1
        for v, e in g[u]:
            if e == pe: continue
            if disc[v] == -1:
                dfs(v, e); low[u] = min(low[u], low[v])
                if low[v] > disc[u]: out.append([min(u, v), max(u, v)])
            else:
                low[u] = min(low[u], disc[v])
    for s in range(n):
        if disc[s] == -1: dfs(s, -1)
    return sorted(out)


def components(n, edges, skip=-1):
    p = list(range(n))

    def find(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x
    for i, (u, v) in enumerate(edges):
        if i != skip:
            p[find(u)] = find(v)
    return len({find(x) for x in range(n)})


def brute(n, edges):
    """Remove each edge in turn; it is a bridge if the component count goes up."""
    base = components(n, edges)
    return sorted({(min(u, v), max(u, v)) for i, (u, v) in enumerate(edges)
                   if u != v and components(n, edges, skip=i) > base})


# --- the prompt's examples ---
ex = [(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]], [[1, 3], [3, 4]]),
      (2, [[0, 1], [0, 1]], []),
      (6, [[0, 1], [2, 3], [3, 4], [4, 2], [5, 5]], [[0, 1]])]
for n, e, want in ex:
    got = bridges(n, e)
    print(n, e, '->', got)
    assert got == want == [list(b) for b in brute(n, e)]

# --- random cross-check against the remove-each-edge oracle (parallel edges and self loops included) ---
cases = 0
for _ in range(1500):
    n = random.randint(1, 9)
    m = random.randint(0, 12)
    e = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    assert bridges(n, e) == [list(b) for b in brute(n, e)], (n, e)
    cases += 1
print('random cases passed:', cases)

# --- deep path: 10^5 nodes, every edge is a bridge; the recursive version dies ---
N = 10 ** 5
path = [[i, i + 1] for i in range(N - 1)]
res = bridges(N, path)
assert len(res) == N - 1 and res[0] == [0, 1] and res[-1] == [N - 2, N - 1]
try:
    recursive_bridges(1600, path[:1599])
    print('recursive: no error')
except RecursionError:
    print('recursive version on a 1600-node path: RecursionError (limit', sys.getrecursionlimit(), ')')
print('iterative on 10^5-node path: bridges =', len(res))

# --- edge cases ---
assert bridges(1, []) == []                                     # single node
assert bridges(3, []) == []                                     # no edges
assert bridges(4, [[0, 1], [1, 2], [2, 3], [3, 0]]) == []       # one cycle
assert bridges(4, [[0, 1], [1, 2], [2, 3]]) == [[0, 1], [1, 2], [2, 3]]
assert bridges(3, [[0, 1], [1, 0], [1, 2]]) == [[1, 2]]         # parallel edge protects 0-1 only
assert bridges(4, [[0, 1], [2, 3]]) == [[0, 1], [2, 3]]         # disconnected graph
ring = [[i, (i + 1) % 1000] for i in range(1000)] + [[0, 1000]]
assert bridges(1001, ring) == [[0, 1000]]                       # pendant edge off a big cycle
print('edge asserts passed')
```

**Output (my run):**
```
5 [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [[1, 3], [3, 4]]
2 [[0, 1], [0, 1]] -> []
6 [[0, 1], [2, 3], [3, 4], [4, 2], [5, 5]] -> [[0, 1]]
random cases passed: 1500
recursive version on a 1600-node path: RecursionError (limit 1000 )
iterative on 10^5-node path: bridges = 99999
edge asserts passed
```

**Edge cases:**
- `n = 1` or no edges: no bridges.
- Parallel edges (`[0,1]` twice): neither is a bridge.
- Self loop (`[5, 5]`): ignored; the node stays isolated.
- Disconnected graph: loop over all start nodes; each tree edge component is handled separately (checked).
- A single big cycle has no bridges; a pendant edge off it is a bridge.
- 10^5-node path: all 99,999 edges are bridges, no recursion error.

**Follow-ups:**
- *Articulation points?* Same DFS; non-root `p` is a cut vertex if some child has `low[child] >= disc[p]` (note `>=`), the root if it has two or more DFS children (Q42).
- *Why `>` for bridges but `>=` for cut vertices?* A back edge from the child's subtree to p itself keeps the edge (p, child) on a cycle, so a bridge needs `low[child] > disc[p]`. Removing the vertex p removes that back edge too, so reaching p is not enough and the cut-vertex test is `low[child] >= disc[p]`.
- *Could union-find do it?* Not directly online; an offline route is a spanning tree plus marking covered tree edges (editor knowledge, not run here).

**Common mistakes:**
- Skipping the parent NODE: parallel edges then produce false bridges.
- Using `low[u] >= disc[p]` for bridges (that is the articulation test and reports cycle edges).
- Updating `low[u]` from `low[v]` of a back edge instead of `disc[v]` (it still often works, but it is not the definition).
- Recursive DFS (RecursionError at about 1000 deep).
- Not looping over all start nodes, or emitting `[u, v]` unsorted or twice.
- Updating the parent's `low` before the child has finished.

### Q34 ⭐⭐ 🔴 Reconstruct the itinerary with Hierholzer's algorithm. `tickets` is a list of [from, to] airport codes (strings of 3 uppercase letters, 1 <= len <= 300; the same ticket can appear several times). The trip starts at 'JFK' and must use every ticket exactly once; the input is guaranteed to allow at least one such trip. Return the itinerary as the list of airports (length len(tickets) + 1) that is smallest in lexicographic order of the whole list (compare airports as strings, position by position) among all valid trips. Build adjacency lists sorted in DECREASING order so `pop()` takes the smallest destination, run an iterative DFS that appends a node to the answer only when it has no unused ticket left, and reverse at the end; explain why greedy 'always take the smallest' without this post-order trick fails (it can strand tickets in a dead end). Existence tests for Eulerian trails are Part 9 Q36 and are not repeated. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a backtracking oracle that tries the destinations in sorted order and keeps the first complete trip on small inputs. Example: tickets=[['JFK', 'KUL'], ['JFK', 'NRT'], ['NRT', 'JFK']] -> ['JFK', 'NRT', 'JFK', 'KUL']; tickets=[['JFK', 'SFO'], ['JFK', 'ATL'], ['SFO', 'ATL'], ['ATL', 'JFK'], ['ATL', 'SFO']] -> ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO'].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** Eulerian trail with Hierholzer's algorithm (iterative DFS, post-order, reverse). Every ticket is an edge to use exactly once; lexicographic smallest comes from taking the smallest destination first.

**Say this first (1 line):** "Sort each airport's destinations so pop() gives the smallest, DFS from JFK, append an airport to the route only when it has no unused ticket left, reverse at the end; plain greedy can strand tickets in a dead end."

**Brute force:** Backtracking: from the current airport try each distinct destination in sorted order, mark a matching ticket used, recurse, undo on failure; the first complete trip is the lexicographically smallest. Worst case exponential. This is the oracle.

**Optimal:**
- Adjacency: `g[a]` holds destinations sorted in DECREASING order, so `pop()` removes the smallest remaining. Duplicate tickets are just repeated entries.
- Iterative Hierholzer: `stack = ['JFK']`. While the stack is non-empty: if the top has unused tickets, pop one and push its destination; otherwise pop the top and append it to `route`. Reverse `route`.
- Why post-order works: an airport is appended only when it has no unused ticket. The first airport appended is the dead end where the trail must end (in a valid input there is at most one). Detours (cycles) taken earlier get spliced in front of it when the stack unwinds, so no ticket is stranded. Taking the smallest ticket first at each step makes the final order lexicographically smallest.
- Why plain greedy fails: on `JFK->KUL, JFK->NRT, NRT->JFK` the smallest first choice is KUL, which has no outgoing ticket, so the NRT tickets are never used. The code shows greedy giving `['JFK', 'KUL']`, and on random valid inputs greedy was wrong in 314 of 1000 cases. Hierholzer fixes that by deferring the dead end.
- Existence of an Eulerian trail is Part 9 Q36 and is guaranteed by the input here.
- Iterative, because 300 tickets are fine recursively but the iterative form has no depth limit at all and is the standard way to present it.

**Complexity:** Time O(E log E) (sorting adjacency lists once; the DFS itself is O(E) because each ticket is popped once). Space O(E) for adjacency, stack and route. With E <= 300 this is instant.

**Dry run:** tickets `JFK->KUL, JFK->NRT, NRT->JFK`.
- `g[JFK] = [NRT, KUL]` (decreasing), `g[NRT] = [JFK]`.
- Stack `[JFK]`; JFK has tickets: pop KUL, stack `[JFK, KUL]`. KUL has none: append KUL to route, pop. Route `[KUL]`.
- Top JFK: pop NRT, stack `[JFK, NRT]`; NRT: pop JFK, stack `[JFK, NRT, JFK]`. This JFK has no tickets left: route `[KUL, JFK]`; then NRT: `[KUL, JFK, NRT]`; then JFK: `[KUL, JFK, NRT, JFK]`.
- Reverse: `['JFK', 'NRT', 'JFK', 'KUL']`. Matches the example.

**Code:**
```python
import random
from collections import defaultdict

random.seed(3401)


def find_itinerary(tickets):
    """Hierholzer, iterative. Destinations sorted DEcreasing so pop() gives the smallest."""
    g = defaultdict(list)
    for a, b in tickets:
        g[a].append(b)
    for a in g:
        g[a].sort(reverse=True)
    route = []
    stack = ['JFK']
    while stack:
        while g[stack[-1]]:                      # still an unused ticket: walk it
            stack.append(g[stack[-1]].pop())
        route.append(stack.pop())                # dead end: this airport is the LAST of what remains
    return route[::-1]


def greedy_wrong(tickets):
    """Always take the smallest unused destination, never undo. Can strand tickets."""
    g = defaultdict(list)
    for a, b in tickets:
        g[a].append(b)
    for a in g:
        g[a].sort()
    path = ['JFK']
    while g[path[-1]]:
        path.append(g[path[-1]].pop(0))
    return path


def brute(tickets):
    """Backtracking: try destinations in sorted order, keep the first complete trip."""
    m = len(tickets)
    used = [False] * m

    def dfs(path):
        if len(path) == m + 1:
            return list(path)
        cur = path[-1]
        for dest in sorted({t[1] for i, t in enumerate(tickets) if not used[i] and t[0] == cur}):
            i = next(i for i, t in enumerate(tickets) if not used[i] and t == [cur, dest])
            used[i] = True
            path.append(dest)
            res = dfs(path)
            path.pop()
            used[i] = False
            if res:
                return res
        return None
    return dfs(['JFK'])


def random_trip(m, airports):
    """A random valid trail from JFK with m tickets (so an Eulerian trip exists), shuffled."""
    cur, tickets = 'JFK', []
    for _ in range(m):
        nxt = random.choice(airports)
        tickets.append([cur, nxt])
        cur = nxt
    random.shuffle(tickets)
    return tickets


# --- the prompt's examples ---
t1 = [['JFK', 'KUL'], ['JFK', 'NRT'], ['NRT', 'JFK']]
t2 = [['JFK', 'SFO'], ['JFK', 'ATL'], ['SFO', 'ATL'], ['ATL', 'JFK'], ['ATL', 'SFO']]
r1, r2 = find_itinerary(t1), find_itinerary(t2)
print(r1)
print(r2)
assert r1 == ['JFK', 'NRT', 'JFK', 'KUL'] == brute(t1)
assert r2 == ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO'] == brute(t2)
print('greedy on example 1 (wrong):', greedy_wrong(t1), '- stranded the NRT tickets')

# --- random cross-check against the backtracking oracle ---
airports = ['JFK', 'ATL', 'LAX', 'SFO', 'NRT']
bad = 0
for _ in range(1000):
    t = random_trip(random.randint(1, 9), airports)
    want = brute(t)
    assert find_itinerary(t) == want, t
    assert len(want) == len(t) + 1
    if greedy_wrong(t) != want:
        bad += 1
print('random cases passed: 1000; plain greedy was wrong on', bad, 'of them')

# --- edge cases ---
assert find_itinerary([['JFK', 'JFK']]) == ['JFK', 'JFK']                      # self loop ticket
assert find_itinerary([['JFK', 'AAA'], ['AAA', 'JFK'], ['JFK', 'AAA']]) == ['JFK', 'AAA', 'JFK', 'AAA']  # duplicates
assert find_itinerary([['JFK', 'ZZZ']]) == ['JFK', 'ZZZ']                      # one ticket
chain = [['JFK', 'A00']] + [['A%02d' % i, 'A%02d' % (i + 1)] for i in range(0, 99)]
assert find_itinerary(chain) == ['JFK'] + ['A%02d' % i for i in range(100)]   # forced path, 100 tickets
cyc = [['JFK', 'AAA'], ['AAA', 'JFK']] * 150                                   # 300 tickets, same pair repeated
assert len(find_itinerary(cyc)) == 301
print('edge asserts passed')
```

**Output (my run):**
```
['JFK', 'NRT', 'JFK', 'KUL']
['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO']
greedy on example 1 (wrong): ['JFK', 'KUL'] - stranded the NRT tickets
random cases passed: 1000; plain greedy was wrong on 314 of them
edge asserts passed
```

**Edge cases:**
- One ticket.
- A self-loop ticket (`JFK -> JFK`).
- Duplicate tickets between the same pair (kept as separate edges).
- A forced path (a chain of 100 tickets) has only one answer.
- 300 tickets alternating on one pair.
- Airports with no outgoing tickets other than the final one: `g[...]` with `defaultdict` returns an empty list.

**Follow-ups:**
- *Why is the answer length `len(tickets) + 1`?* A trail using E edges visits E + 1 airport positions.
- *Why reverse?* Airports are appended in finishing order, which is the trail read backwards.
- *Directed vs undirected Euler trail?* Same idea; for undirected graphs you must delete both directions of an edge when you use it (editor knowledge, not run here).

**Common mistakes:**
- Sorting ascending and using `pop(0)` (works but is O(n) per pop) or ascending with `pop()` (takes the largest).
- Appending a node when first visited instead of when stuck (that is plain greedy).
- Forgetting to reverse.
- Using a set for destinations, which collapses duplicate tickets.
- Recursing without thinking about depth.
- Starting the oracle's `used` bookkeeping on the destination only, so a duplicate ticket is consumed twice.

### Q35 ⭐⭐ 🔴 [Set B, Q4 of 5, 11 min, 25 pts] Redundant directed connection. `edges` is a list of n directed [parent, child] pairs over nodes 1..n (3 <= n <= 1000, no repeats, no self loops). It was a rooted tree (one root, every other node with exactly one parent, all nodes reachable from the root) plus ONE extra directed edge. Return the edge to remove so that the remaining n - 1 edges form a rooted tree again; if several edges work, return the one that appears LAST in `edges`. Two cases: a node with two parents (take the two candidate edges; try ignoring the later one and look for a cycle with union-find: a cycle means the earlier candidate is the answer, otherwise the later one), and no node with two parents (then there is a cycle and the answer is the last edge that closes it in union-find order, as in the undirected Part 9 Q14). Explain why a node with two parents plus a cycle forces the earlier candidate. O(n alpha(n)). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that tries to drop each edge from the last to the first and tests whether the rest is a rooted tree on small inputs. Example: edges=[[1, 2], [1, 3], [2, 3]] -> [2, 3]; edges=[[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]] -> [4, 1]; edges=[[2, 1], [3, 1], [4, 2], [1, 4]] -> [2, 1].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Union-find on a directed graph with two failure modes: a node with two parents, or a cycle. Extension of the undirected redundant-connection problem (Part 9 Q14).

**Say this first (1 line):** "Two cases: if some node has two parents, the answer is one of those two edges and I test with union-find while ignoring the later one; if not, it is the edge that closes the cycle."

**Brute force:** Try dropping each edge from the last to the first; the first removal that leaves a rooted tree (exactly one root with indegree 0, every other node indegree 1, all reachable from the root) is the answer. O(n^2) for n edges. This is the oracle.

**Optimal:**
- Pass 1: record each node's first parent. When a node `v` gets a second parent, set `cand1 = [first parent, v]` (earlier edge) and `cand2 = [this edge]` (later edge).
- Pass 2: union-find over all edges, skipping `cand2` if it exists. Remember the first edge whose endpoints are already connected (`cycle_edge`).
- No node with two parents (`cand2` is None): the extra edge made a cycle; return `cycle_edge`. It is the last cycle edge in input order, because the first edge that closes a cycle in input order must be the last edge of that cycle to appear.
- A node with two parents: if ignoring `cand2` still leaves a cycle, return `cand1`; otherwise return `cand2` (it is the later of two working choices).
- Why a two-parent node plus a leftover cycle forces the earlier candidate: the graph is a tree plus exactly one extra edge, so the only cycle must contain that extra edge, and the extra edge is one of the two candidates. If a cycle survives after ignoring `cand2`, the cycle does not use `cand2`, so the extra edge is `cand1`. Also, once `cand2` is removed every node has indegree at most 1, so any undirected cycle found by union-find is really a directed cycle.
- If there is no cycle after ignoring `cand2`, both candidates work (removing either leaves a rooted tree), and the rule says return the later one, `cand2`.

**Complexity:** Time O(n alpha(n)) with path compression (one pass for parents, one union-find pass). Space O(n) for `parent` and the union-find array.

**Dry run:** `edges = [[2,1],[3,1],[4,2],[1,4]]`.
- Pass 1: `[2,1]` sets parent[1] = 2. `[3,1]`: node 1 already has a parent: `cand1 = [2,1]`, `cand2 = [3,1]`. `[4,2]` sets parent[2] = 4. `[1,4]` sets parent[4] = 1.
- Pass 2 (skip `[3,1]`): union(2,1); union(4,2); edge `[1,4]`: 1 and 4 are already connected, so `cycle_edge = [1,4]`.
- `cand2` exists and a cycle remains, so return `cand1 = [2, 1]`. Matches the example.
- Check the first example `[[1,2],[1,3],[2,3]]`: `cand1 = [1,3]`, `cand2 = [2,3]`. Skipping `[2,3]`: union(1,2), union(1,3), no cycle, so return `cand2 = [2, 3]`. Cycle-only example `[[1,2],[2,3],[3,4],[4,1],[1,5]]`: no node with two parents; the first edge closing a cycle is `[4,1]`.

**Code:**
```python
import random

random.seed(3501)


def find_redundant_directed(edges):
    n = len(edges)
    parent = [0] * (n + 1)
    cand1 = cand2 = None                       # cand1: earlier edge into a 2-parent node; cand2: the later one
    for u, v in edges:
        if parent[v]:
            cand1, cand2 = [parent[v], v], [u, v]
        else:
            parent[v] = u
    uf = list(range(n + 1))

    def find(x):
        while uf[x] != x:
            uf[x] = uf[uf[x]]
            x = uf[x]
        return x
    cycle_edge = None
    for u, v in edges:
        if cand2 is not None and [u, v] == cand2:      # pretend the later candidate is not there
            continue
        a, b = find(u), find(v)
        if a == b:
            cycle_edge = [u, v]                        # first edge that closes a cycle
            break
        uf[b] = a
    if cand2 is None:                                  # case 2: no node has two parents -> pure cycle
        return cycle_edge
    return cand1 if cycle_edge else cand2              # case 1: cycle left => earlier candidate, else later


def is_rooted_tree(n, edges):
    indeg = [0] * (n + 1)
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        indeg[v] += 1
        g[u].append(v)
    roots = [v for v in range(1, n + 1) if indeg[v] == 0]
    if len(roots) != 1 or any(indeg[v] > 1 for v in range(1, n + 1)):
        return False
    seen, q = {roots[0]}, [roots[0]]
    for u in q:
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == n


def brute(edges):
    """Drop each edge from the last to the first; the first removal leaving a rooted tree is the answer."""
    n = len(edges)
    for i in range(n - 1, -1, -1):
        if is_rooted_tree(n, edges[:i] + edges[i + 1:]):
            return list(edges[i])


def random_instance(n):
    """Random rooted tree on 1..n plus one extra directed edge (no repeat, no self loop), shuffled."""
    order = list(range(1, n + 1))
    random.shuffle(order)
    edges = [[order[random.randrange(i)], order[i]] for i in range(1, n)]
    while True:
        u, v = random.randint(1, n), random.randint(1, n)
        if u != v and [u, v] not in edges:
            break
    edges.append([u, v])
    random.shuffle(edges)
    return edges


# --- the prompt's examples ---
ex = [([[1, 2], [1, 3], [2, 3]], [2, 3]),
      ([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]], [4, 1]),
      ([[2, 1], [3, 1], [4, 2], [1, 4]], [2, 1])]
for e, want in ex:
    got = find_redundant_directed(e)
    print(e, '->', got)
    assert got == want == brute(e)

# --- random cross-check ---
kinds = {'two parents, no cycle': 0, 'two parents + cycle': 0, 'cycle only': 0}
for _ in range(3000):
    e = random_instance(random.randint(3, 8))
    got = find_redundant_directed(e)
    assert got == brute(e), e
    indeg = {}
    for u, v in e:
        indeg[v] = indeg.get(v, 0) + 1
    if max(indeg.values()) < 2:
        kinds['cycle only'] += 1
    else:
        v2 = next(v for v, c in indeg.items() if c == 2)
        first, second = [x for x in e if x[1] == v2]          # in input order
        kinds['two parents + cycle' if got == first else 'two parents, no cycle'] += 1
print('random cases passed: 3000;', kinds)

# --- edge cases ---
assert find_redundant_directed([[1, 2], [2, 3], [3, 1]]) == [3, 1]            # n = 3, pure 3-cycle
assert find_redundant_directed([[1, 2], [1, 3], [3, 2]]) == [3, 2]            # later parent wins when no cycle
assert find_redundant_directed([[1, 2], [2, 1], [1, 3]]) == [2, 1]            # 2-cycle through the root
n = 1000
long = [[i, i + 1] for i in range(1, n)] + [[n, 1]]                           # n = 1000 ring
assert find_redundant_directed(long) == [n, 1]
assert find_redundant_directed([[i, i + 1] for i in range(1, n - 1)] + [[1, n - 1]]) == [1, n - 1]  # node n-1 has parents n-2 and 1; both removals work -> the later edge
print('edge asserts passed')
```

**Output (my run):**
```
[[1, 2], [1, 3], [2, 3]] -> [2, 3]
[[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]] -> [4, 1]
[[2, 1], [3, 1], [4, 2], [1, 4]] -> [2, 1]
random cases passed: 3000; {'two parents, no cycle': 1970, 'two parents + cycle': 206, 'cycle only': 824}
edge asserts passed
```

**Edge cases:**
- n = 3 with a pure 3-cycle: return the last edge of the cycle in input order.
- Two parents and no cycle: return the later of the two parent edges.
- A 2-cycle through the root (`[1,2],[2,1]` plus one more edge).
- n = 1000 ring (all nodes in one cycle).
- The extra edge may point to the root, which creates a cycle but no two-parent node.
- The extra edge may be anywhere in the list, not necessarily last.

**Follow-ups:**
- *Why not just run the undirected version?* It ignores direction, so it can return a valid-looking cycle edge that leaves a node with two parents.
- *Where does the 3000-case random test get its inputs?* A random rooted tree plus one random extra edge, shuffled; the run shows the split: 1970 two-parent cases that end in the later edge, 206 two-parent cases that need the earlier edge, 824 cycle-only cases.
- *Scoring note (Set B, Q4 of 5, 25 pts):* rules spoken first (the two cases, tie = later edge in input order, what a rooted tree means) = 7.5; correct code that passes all three examples and the drop-each-edge random check = 7.5; complexity O(n alpha(n)) with the reason = 5; edge cases (pure cycle, two parents without a cycle, edge into the root) = 2.5; a 60-second summary = 2.5. Partial credit: the two-case split described correctly but only one case coded earns about 12 of 25; the O(n^2) drop-each-edge brute force coded and correct earns about 15. How I would pace this: about 11 minutes, so 3 for the case analysis and the "why cand1" argument, 5 to code, 2 for the random test, 1 for the summary.

**Common mistakes:**
- Returning the first cycle edge in the two-parent case without skipping `cand2`.
- Swapping `cand1` and `cand2` (earlier versus later edge).
- Treating `[u, v]` as undirected in the cycle check, or forgetting that skipping `cand2` is required.
- Comparing edges by node instead of as pairs when skipping.
- Not returning the LAST edge when several answers work.

### Q36 ⭐⭐ 🔴 [Set C, Q3 of 4, 13 min, 30 pts] Reverse pairs. `nums` has 0 <= len <= 5*10^4 integers (|value| <= 2^31, duplicates allowed). Count the pairs i < j with nums[i] > 2 * nums[j] (strict). Python has no overflow, so 2 * nums[j] needs no care here (a 32-bit language would need 64-bit arithmetic: say it). Fenwick solution: coordinate-compress the values (Q17); scan j from left to right; the number of earlier elements greater than 2 * nums[j] is j minus the number of earlier elements <= 2 * nums[j], found with `bisect_right` of 2 * nums[j] in the sorted distinct values and a BIT prefix count; then insert nums[j]. The query key 2 * nums[j] is NOT one of the stored values, which is why you bisect instead of looking up a rank. O(n log n). Compare with the merge-sort counter of Part 13 Q17 and Part 13 Q47 and with Q25. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) double loop on small inputs. Example: nums=[1, 3, 2, 3, 1] -> 2; nums=[2, 4, 3, 5, 1] -> 3; nums=[-5, -5] -> 1; nums=[] -> 0.
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Count pairs with a Fenwick tree (BIT) over compressed values. Scan left to right, query how many earlier elements satisfy the condition, then insert the current element.

**Say this first (1 line):** "Strict inequality nums[i] > 2 * nums[j]; Python has no overflow so 2 * x is safe (in C++ or Java I would use 64-bit); I scan j, ask the BIT how many earlier values are <= 2 * x, subtract that from j, then insert x."

**Brute force:** Double loop over all pairs i < j, count `nums[i] > 2 * nums[j]`. O(n^2) time, O(1) space; for n = 5 * 10^4 that is about 1.25 * 10^9 pair checks, far too slow. This is the oracle.

**Optimal:**
- Compress: `vals = sorted(set(nums))`, rank of x is `bisect_left(vals, x) + 1` (1-based for the BIT). Compression keeps the BIT size at the number of distinct values (Q17).
- Scan j from 0. Before inserting `nums[j]`, the BIT holds exactly the j earlier elements. The count of earlier elements `<= 2x` is `prefix(bisect_right(vals, 2x))`. So the number of earlier elements `> 2x` is `j - that`. Add it to the answer, then `add(rank(nums[j]))`.
- Why `bisect_right` and not a rank lookup: `2x` is usually NOT one of the stored values, so it has no rank. `bisect_right(vals, 2x)` returns how many distinct values are `<= 2x`, which is the highest rank that qualifies (including 2x itself if it happens to be a value).
- Strictness: we want `> 2x`, so equal values must be on the "not greater" side. `bisect_right` puts them there.
- Insert after querying, so an element is never compared with itself or with later elements.
- Compare with the merge-sort counter (Part 13 Q17 and Part 13 Q47): same O(n log n), but the BIT version is online and shorter; merge sort needs a separate counting pass before merging because the condition (`> 2x`) differs from the sort order. Also relate to Q25 (inversions with a BIT): the only changes are the doubled key and the bisect.

**Complexity:** Time O(n log n): sort for compression O(n log n), then n times one `bisect_right`, one prefix query and one update, each O(log n). Space O(n) for `vals` and the tree. The answer can be as large as about n^2 / 4, which Python integers hold without overflow.

**Dry run:** `nums = [1, 3, 2, 3, 1]`; `vals = [1, 2, 3]`.
- j=0, x=1: `bisect_right(vals, 2) = 2`, `prefix(2) = 0`, add `0 - 0 = 0`; insert rank 1.
- j=1, x=3: `bisect_right(vals, 6) = 3`, `prefix(3) = 1`, add `1 - 1 = 0`; insert rank 3.
- j=2, x=2: `bisect_right(vals, 4) = 3`, `prefix(3) = 2`, add 0; insert rank 2.
- j=3, x=3: `bisect_right(vals, 6) = 3`, `prefix(3) = 3`, add 0; insert rank 3.
- j=4, x=1: `bisect_right(vals, 2) = 2`, `prefix(2) = 2` (the earlier 1 and 2), add `4 - 2 = 2`. The pairs are the two 3s against the final 1.
- Answer 2. The other examples give 3, 1 and 0.

**Code:**
```python
import random
from bisect import bisect_left, bisect_right

random.seed(3601)


def reverse_pairs(nums):
    """Count i < j with nums[i] > 2 * nums[j] using a Fenwick tree over compressed values."""
    if not nums:
        return 0
    vals = sorted(set(nums))                     # coordinate compression (distinct sorted values)
    m = len(vals)
    tree = [0] * (m + 1)                         # 1-indexed BIT of counts

    def add(i):                                  # i is a 1-based rank
        while i <= m:
            tree[i] += 1
            i += i & -i

    def prefix(i):                               # how many stored values have rank <= i
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    ans = 0
    for j, x in enumerate(nums):
        # earlier elements <= 2x: bisect_right gives how many DISTINCT values are <= 2x, i.e. the top rank to count
        # (2x need not be a stored value, so we cannot look up its rank)
        not_greater = prefix(bisect_right(vals, 2 * x))
        ans += j - not_greater                   # earlier elements are j in total; the rest are > 2x
        add(bisect_left(vals, x) + 1)            # insert nums[j] AFTER the query
    return ans


def brute(nums):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > 2 * nums[j])


# --- the prompt's examples ---
ex = [([1, 3, 2, 3, 1], 2), ([2, 4, 3, 5, 1], 3), ([-5, -5], 1), ([], 0)]
for nums, want in ex:
    got = reverse_pairs(nums)
    print(nums, '->', got)
    assert got == want == brute(nums)

# --- random cross-check against the O(n^2) double loop ---
for _ in range(1500):
    n = random.randint(0, 14)
    hi = random.choice([3, 10, 100])
    nums = [random.randint(-hi, hi) for _ in range(n)]
    assert reverse_pairs(nums) == brute(nums), nums
print('random cases passed: 1500')

# --- edge cases ---
assert reverse_pairs([0, 0, 0]) == 0                       # 0 > 0 is false
assert reverse_pairs([1]) == 0
assert reverse_pairs([-1, -1]) == 1                        # -1 > -2: negatives make equal values a pair
assert reverse_pairs([5, 2]) == 1 and reverse_pairs([4, 2]) == 0   # strict: 4 > 4 is false
assert reverse_pairs([2 ** 31, -2 ** 31]) == 1             # 2 * value exceeds 32 bits: fine in Python
assert reverse_pairs([2 ** 31] * 3) == 0
n = 5 * 10 ** 4
assert reverse_pairs(list(range(n))) == 0                  # increasing: no pair
d = reverse_pairs(list(range(n, 0, -1)))                   # decreasing n..1: pair (a, b) needs a > 2b
assert d == sum(n - 2 * b for b in range(1, n // 2 + 1))   # closed form
print('n = 50000 strictly decreasing ->', d)
print('edge asserts passed')
```

**Output (my run):**
```
[1, 3, 2, 3, 1] -> 2
[2, 4, 3, 5, 1] -> 3
[-5, -5] -> 1
[] -> 0
random cases passed: 1500
n = 50000 strictly decreasing -> 624975000
edge asserts passed
```

**Edge cases:**
- Empty list returns 0 (the code returns early; `max`/BIT size 0 would otherwise misbehave).
- All zeros: `0 > 0` is false, so 0 pairs.
- Negatives: `-1 > -2` is true, so `[-1, -1]` has 1 pair, and so does `[-5, -5]` in the prompt.
- Strict boundary: `[4, 2]` has no pair (4 > 4 false), `[5, 2]` has one.
- Values near 2^31: `2 * x` exceeds 32 bits, harmless in Python.
- Strictly decreasing 50,000 values: 624,975,000 pairs, matches the closed form `sum(n - 2b for b in 1..n/2)`.

**Follow-ups:**
- *Merge sort instead?* Count across the two sorted halves with two pointers before merging (Part 13 Q17 and Part 13 Q47). Same O(n log n), O(n) extra space.
- *Why not compress the keys 2x too?* You could compress `nums` and `2 * nums` together; `bisect_right` on the values alone is simpler.
- *Scoring note (Set C, Q3 of 4, 30 pts):* rules spoken first (strict `>`, i < j, empty returns 0, no overflow in Python but 64-bit elsewhere) = 9; correct code that passes the four examples and the O(n^2) random check = 9; complexity O(n log n) with the reason (n queries and updates of O(log n), plus the sort) = 6; edge cases (empty, negatives, equal values, strict boundary) = 3; a 60-second summary = 3. Partial credit: a correct merge-sort or O(n^2) solution with the rules stated earns about 15 of 30; a BIT that looks up `2x` by rank (crashes or miscounts) loses most of the solution points. How I would pace this: about 13 minutes, so 3 for rules and the bisect argument, 6 to code the BIT and the scan, 3 for the random test and 1 for the summary.

**Common mistakes:**
- Looking up the rank of `2x` in a dict (it is usually missing) instead of `bisect_right`.
- `bisect_left` (turns `<=` into `<` and counts equal-to-2x values as greater).
- Inserting before querying.
- BIT index 0 (an infinite loop: `0 & -0` is 0).
- Counting `prefix` of greater values with the wrong total (use `j`, the number inserted so far).
- Compressing with ranks that skip values so the BIT size is wrong.

### Q37 ⭐⭐ 🔴 [Set D, Q4 of 4, 14 min, 30 pts] The skyline problem. `buildings` is a list of 1 to 10^4 triples [left, right, height] with 0 <= left < right <= 2^31 - 1 and 1 <= height <= 2^31 - 1, sorted by `left` (equal lefts in any order). Return the skyline as the list of key points [x, height] from left to right: a key point is the left end of a horizontal segment, i.e. the x where the maximum height of the buildings covering x changes; the last key point has height 0 at the right end of the right-most building; no two consecutive key points may have the same height, and a gap between buildings shows as a drop to 0 and a rise again. Sweep events in sorted order (starts with (x, -height), ends with (x, 0), so starts at one x are handled before ends and taller starts first), keep a max-heap of (-height, right end) and pop the top lazily while its right end is <= x (Part 8 Q31); emit a point whenever the current maximum changes. O(n log n). Say why touching buildings [0, 2, 3] and [2, 4, 3] must not produce a point at x = 2 (equal heights) and relate the event sweep to Part 8 Q7 and Part 8 Q5. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that evaluates the maximum covering height at every integer x of a small coordinate range and extracts the changes on small inputs. Example: buildings=[[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]] -> [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]; buildings=[[0, 2, 3], [2, 4, 3]] -> [[0, 3], [4, 0]]; buildings=[[1, 5, 4], [1, 3, 6], [3, 7, 2]] -> [[1, 6], [3, 4], [5, 2], [7, 0]].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Event sweep with a max-heap and lazy deletion. Process building starts and ends left to right and emit a key point whenever the current maximum height changes.

**Say this first (1 line):** "Sort events so that at equal x the starts come first and taller starts first, keep a max-heap of (height, right end), drop tops whose right end is <= x lazily, and emit a point only when the max changes."

**Brute force:** For every integer x in the coordinate range compute the maximum height of buildings covering `l <= x < r`, then emit the x values where it changes. O(range * n); impossible for coordinates up to 2^31 - 1, fine as a small-range oracle.

**Optimal:**
- Events: each building gives `(l, -h, r)` (a start; the negative height sorts taller first) and `(r, 0, 0)` (an end). Sorting tuples orders by x, then starts before ends (negative before 0), then taller starts first.
- Heap: `(-height, right end)` so Python's min-heap acts as a max-heap. A sentinel `(0, infinity)` is the ground and never expires.
- At each event x: pop tops whose right end is `<= x` (building already over: lazy deletion, Part 8 Q31, so we never search inside the heap); push the building on a start event; the current height is `-heap[0][0]`. If it differs from the last emitted height, emit `[x, height]`.
- Why starts before ends at the same x: for touching buildings `[0,2,3]` and `[2,4,3]`, at x = 2 the second building is added before the first one expires, so the maximum stays 3 and nothing is emitted. If ends came first, the sweep would drop to 0 and rise again, producing the spurious points `[2, 0]` and `[2, 3]` (shown in the run).
- Why taller starts first at one x: otherwise a short building could emit a point that the taller one immediately overrides.
- The `changed height` check also merges equal-height neighbours, so no two consecutive points share a height; the final point is height 0 at the last right end because every building has expired by then.
- Relation to Part 8 Q7 (meeting rooms: sort events, track a running count) and Part 8 Q5 (merging intervals by sorted starts): same sweep, here with a max-heap instead of a counter.

**Complexity:** Time O(n log n): sorting 2n events, then each building is pushed once and popped at most once, each O(log n). Space O(n) for events and heap.

**Dry run:** `buildings = [[1,5,4],[1,3,6],[3,7,2]]`.
- Events sorted: `(1,-6,3)`, `(1,-4,5)`, `(3,-2,7)`, `(3,0,0)`, `(5,0,0)`, `(7,0,0)`.
- x=1, start 6: push; max 6, differs from 0: emit `[1, 6]`. x=1, start 4: push; max still 6, no emit.
- x=3, start 2: first pop the expired top `(-6, 3)` (3 <= 3); top is now `(-4, 5)`; push `(-2, 7)`; max 4: emit `[3, 4]`. The end event at x=3 changes nothing.
- x=5: pop `(-4, 5)`; top `(-2, 7)`: emit `[5, 2]`.
- x=7: pop `(-2, 7)`; only the ground is left: emit `[7, 0]`.
- Result `[[1,6],[3,4],[5,2],[7,0]]`. The other two examples give the five-building skyline in the prompt and `[[0,3],[4,0]]`.

**Code:**
```python
import heapq
import random

random.seed(3701)


def skyline(buildings):
    # event = (x, -height, right). Starts have negative second key; ends have 0.
    # Sorting puts, at equal x: taller starts first (more negative), then all starts before ends.
    events = [(l, -h, r) for l, r, h in buildings] + [(r, 0, 0) for l, r, h in buildings]
    events.sort()
    heap = [(0, float('inf'))]                    # (-height, right end); sentinel = ground, never expires
    res = []
    for x, neg_h, r in events:
        while heap[0][1] <= x:                    # lazy deletion: drop tops whose building has ended
            heapq.heappop(heap)
        if neg_h:                                 # a start event: add the building
            heapq.heappush(heap, (neg_h, r))
        while heap[0][1] <= x:                    # (a start with r <= x cannot occur, but keep the top clean)
            heapq.heappop(heap)
        cur = -heap[0][0]
        if not res or res[-1][1] != cur:          # emit only when the maximum height changes
            res.append([x, cur])
    return res


def brute(buildings):
    """Max covering height at every integer x of the range; key points are the changes."""
    hi = max(r for l, r, h in buildings)
    res, prev = [], 0
    for x in range(0, hi + 1):
        cur = max((h for l, r, h in buildings if l <= x < r), default=0)
        if cur != prev:
            res.append([x, cur])
            prev = cur
    return res


# --- the prompt's examples ---
ex = [([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],
       [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]),
      ([[0, 2, 3], [2, 4, 3]], [[0, 3], [4, 0]]),
      ([[1, 5, 4], [1, 3, 6], [3, 7, 2]], [[1, 6], [3, 4], [5, 2], [7, 0]])]
for b, want in ex:
    got = skyline(b)
    print(got)
    assert got == want == brute(b)

# --- what goes wrong if ends are handled before starts at the same x (touching buildings) ---
def skyline_ends_first(buildings):
    events = sorted([(l, h, r) for l, r, h in buildings] + [(r, -1, 0) for l, r, h in buildings])   # end key -1 < start key h
    heap, res = [(0, float('inf'))], []
    for x, h, r in events:
        if h > 0:
            heapq.heappush(heap, (-h, r))
        while heap[0][1] <= x:
            heapq.heappop(heap)
        cur = -heap[0][0]
        if not res or res[-1][1] != cur:
            res.append([x, cur])
    return res


print('ends-first on touching buildings:', skyline_ends_first([[0, 2, 3], [2, 4, 3]]), '(spurious [2, 0], [2, 3])')
assert skyline_ends_first([[0, 2, 3], [2, 4, 3]]) == [[0, 3], [2, 0], [2, 3], [4, 0]]

# --- random cross-check (sorted by left, equal lefts in random order, gaps and touching included) ---
for _ in range(2000):
    k = random.randint(1, 8)
    bs = []
    for _ in range(k):
        l = random.randint(0, 12)
        bs.append([l, random.randint(l + 1, 15), random.randint(1, 6)])
    bs.sort(key=lambda t: (t[0], random.random()))
    assert skyline(bs) == brute(bs), bs
print('random cases passed: 2000')

# --- edge cases ---
assert skyline([[1, 2, 5]]) == [[1, 5], [2, 0]]                          # single building
assert skyline([[1, 2, 5], [4, 6, 5]]) == [[1, 5], [2, 0], [4, 5], [6, 0]]   # gap: drop to 0, rise again
assert skyline([[0, 10, 1], [2, 4, 5], [3, 5, 5]]) == [[0, 1], [2, 5], [5, 1], [10, 0]]  # equal heights merge
assert skyline([[0, 5, 7], [0, 5, 7]]) == [[0, 7], [5, 0]]               # duplicate buildings
assert skyline([[0, 5, 3], [1, 2, 3]]) == [[0, 3], [5, 0]]               # fully inside, same height: no point
assert skyline([[0, 2 ** 31 - 1, 2 ** 31 - 1]]) == [[0, 2 ** 31 - 1], [2 ** 31 - 1, 0]]   # huge coordinates
many = [[i, i + 2, 1 + i % 7] for i in range(10 ** 4)]
assert len(skyline(many)) > 0                                            # n = 10^4 runs
print('edge asserts passed')
```

**Output (my run):**
```
[[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]
[[0, 3], [4, 0]]
[[1, 6], [3, 4], [5, 2], [7, 0]]
ends-first on touching buildings: [[0, 3], [2, 0], [2, 3], [4, 0]] (spurious [2, 0], [2, 3])
random cases passed: 2000
edge asserts passed
```

**Edge cases:**
- Single building: `[[l, h], [r, 0]]`.
- Gap between buildings: a drop to 0 and a later rise (checked).
- Touching buildings of equal height: no point at the touch (the example).
- A building fully inside a taller one: no point; inside one of equal height: also no point.
- Duplicate buildings.
- Coordinates and heights near 2^31 - 1: no overflow concern in Python, and no array of size `range` is allocated.
- 10^4 overlapping buildings (the maximum size) run in the edge asserts.

**Follow-ups:**
- *Why not a `SortedList` or a segment tree?* The heap with lazy deletion is enough because we only need the maximum, and a building only has to be removed once it can matter.
- *Why can stale entries stay in the heap?* An entry deep in the heap that has expired cannot affect the maximum until it reaches the top, and we pop it then. Each entry is popped once, which keeps O(n log n).
- *Scoring note (Set D, Q4 of 4, 30 pts):* rules spoken first (output format, key point = left end where the maximum changes, no consecutive equal heights, touching and gap cases, ends at height 0) = 9; correct code that passes the three examples and the per-integer-x random check = 9; complexity O(n log n) with the lazy-deletion argument = 6; edge cases (gap, touching, nested, duplicates) = 3; a 60-second summary = 3. Partial credit: a correct sweep that emits spurious equal-height points earns about 18 of 30; the O(range * n) scan earns about 8 because it cannot handle 2^31 coordinates. How I would pace this: about 14 minutes, so 3 for rules and event ordering, 7 to code, 3 for the random test and 1 for the summary.

**Common mistakes:**
- Handling ends before starts at the same x (spurious drops).
- Sorting starts by ascending height at the same x.
- Forgetting the sentinel ground, so the heap empties and `heap[0]` crashes.
- Emitting a point on every event instead of only on a change.
- Popping only once instead of `while` (several expired tops can stack up).
- Using the heap's `-height` without negating back when emitting.

### Q38 ⭐ 🟡 Zigzag iterator over k lists. Implement class `ZigzagIterator(lists)` where `lists` is a list of 0 <= k <= 100 lists of integers (some may be empty, total size <= 10^4) with `next()` and `hasNext()`: `next()` returns the elements round-robin, one from each non-exhausted list in list order, then the second element of each, and so on; a list that runs out is simply skipped in later rounds, so [[1, 2, 3], [4], [5, 6]] gives 1, 4, 5, 2, 6, 3. Keep a deque of (list, next index) pairs for the non-empty lists: `next` pops the front, reads its element and re-appends the pair when more elements remain, O(1) per call and O(k) memory (two lists only is the classic case; the deque handles any k). The checker never calls `next()` when `hasNext()` is False. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). Here `init` is a one-element list holding `lists`. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[[1, 2, 3], [4], [5, 6]]], ops=[['next', []], ['next', []], ['next', []], ['next', []], ['hasNext', []], ['next', []], ['next', []], ['hasNext', []]] -> [1, 4, 5, 2, True, 6, 3, False]; init=[[[], []]], ops=[['hasNext', []]] -> [False].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Iterator design with a queue of live cursors (round robin). Each list that still has elements waits in a deque as `(list, next index)`.

**Say this first (1 line):** "A deque of (list, next index) for the non-empty lists: next() pops the front, returns its element and re-appends the pair if the list has more; hasNext() is just 'is the deque non-empty'."

**Brute force:** In the constructor, build the whole zigzag order by rounds (round r takes element r from every list that has one) and serve it with a cursor. O(total) time and extra memory up front, simple and correct (this is the oracle), but it copies all the data and is wrong for lazy inputs.

**Optimal:**
- Constructor: `deque((lst, 0) for lst in lists if lst)`. Empty lists never enter, so `hasNext` needs no skipping logic.
- `next()`: `lst, i = popleft()`; if `i + 1 < len(lst)` re-append `(lst, i + 1)`; return `lst[i]`. The deque order is exactly the round-robin order: after a list serves one element it goes to the back of the line, behind every other live list, which is the next round.
- A list that runs out is simply not re-appended, so later rounds skip it automatically.
- Works for any k (the two-list case is the classic one). The checker never calls `next()` when `hasNext()` is False, so no exception handling is needed (real code would raise `StopIteration`).
- The input lists are never copied or changed (only referenced).
- Thread safety (concept only): `next()` does pop, read, append: two threads could take the same front element or interleave the rounds. A lock around `next` and `hasNext` together (a `hasNext` then `next` pair is not atomic on its own) would be required.

**Complexity:** Constructor O(k) time and O(k) space. `next()` O(1) (deque ends). `hasNext()` O(1). Total memory O(k) beyond the input; the naive version uses O(total).

**Dry run:** `lists = [[1,2,3],[4],[5,6]]`; deque `[(A,0),(B,0),(C,0)]`.
- `next`: pop `(A,0)`, A has more: append `(A,1)`; return 1. Deque `[B0, C0, A1]`.
- `next`: pop `(B,0)`, B is done (not re-appended); return 4. Deque `[C0, A1]`.
- `next`: pop `(C,0)`, append `(C,1)`; return 5. Deque `[A1, C1]`.
- `next`: pop `(A,1)`, append `(A,2)`; return 2. `hasNext` -> True. Deque `[C1, A2]`.
- `next`: `(C,1)` is last in C: return 6. `next`: `(A,2)` last: return 3. `hasNext` -> False.
- Result `[1, 4, 5, 2, True, 6, 3, False]`; for `[[], []]`, `hasNext` is `[False]`.

**Code:**
```python
import random
from collections import deque

random.seed(3801)


class ZigzagIterator:
    """Round-robin over k lists. Deque of (list, next index) for lists that still have elements."""

    def __init__(self, lists):
        self.q = deque((lst, 0) for lst in lists if lst)       # empty lists never enter

    def next(self):                                            # O(1); caller checked hasNext()
        lst, i = self.q.popleft()
        if i + 1 < len(lst):
            self.q.append((lst, i + 1))                        # back of the line for the next round
        return lst[i]

    def hasNext(self):
        return bool(self.q)


class NaiveZigzag:
    """Reference: precompute the whole order by rounds, then serve it with a cursor."""

    def __init__(self, lists):
        self.out = []
        longest = max((len(l) for l in lists), default=0)
        for r in range(longest):
            for l in lists:
                if r < len(l):
                    self.out.append(l[r])
        self.pos = 0

    def next(self):
        self.pos += 1
        return self.out[self.pos - 1]

    def hasNext(self):
        return self.pos < len(self.out)


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's examples ---
ops = [['next', []], ['next', []], ['next', []], ['next', []], ['hasNext', []], ['next', []], ['next', []], ['hasNext', []]]
r1 = run(ZigzagIterator, [[[1, 2, 3], [4], [5, 6]]], ops)
print('example 1:', r1)
assert r1 == [1, 4, 5, 2, True, 6, 3, False] == run(NaiveZigzag, [[[1, 2, 3], [4], [5, 6]]], ops)
r2 = run(ZigzagIterator, [[[], []]], [['hasNext', []]])
print('example 2:', r2)
assert r2 == [False]

# --- random operation sequences (next only when hasNext is True, as the checker promises) ---
total = 0
for _ in range(1000):
    lists = [[random.randint(0, 9) for _ in range(random.randint(0, 5))] for _ in range(random.randint(0, 5))]
    a, b = ZigzagIterator(lists), NaiveZigzag(lists)
    for _ in range(random.randint(1, 30)):
        if random.random() < 0.4 or not b.hasNext():
            assert a.hasNext() == b.hasNext()
        else:
            assert a.hasNext() and a.next() == b.next()
        total += 1
print('random ops compared:', total)

# --- the input lists are never copied or mutated ---
src = [[1, 2], [3]]
it = ZigzagIterator(src)
while it.hasNext():
    it.next()
assert src == [[1, 2], [3]]

# --- edge cases ---
assert run(ZigzagIterator, [[]], [['hasNext', []]]) == [False]                       # k = 0
assert run(ZigzagIterator, [[[7]]], [['hasNext', []], ['next', []], ['hasNext', []]]) == [True, 7, False]
one = ZigzagIterator([[], [1, 2, 3], []])                                            # one real list: plain order
assert [one.next() for _ in range(3)] == [1, 2, 3] and not one.hasNext()
dup = ZigzagIterator([[1, 1], [1, 1]])
assert [dup.next() for _ in range(4)] == [1, 1, 1, 1]
big = ZigzagIterator([list(range(i, 10 ** 4, 100)) for i in range(100)])             # k = 100, 10^4 elements total
seen = []
while big.hasNext():
    seen.append(big.next())
assert len(seen) == 10 ** 4 and seen[:3] == [0, 1, 2]
print('edge asserts passed')
```

**Output (my run):**
```
example 1: [1, 4, 5, 2, True, 6, 3, False]
example 2: [False]
random ops compared: 15319
edge asserts passed
```

**Edge cases:**
- `k = 0` (no lists) and all lists empty: `hasNext()` is False from the start.
- A single non-empty list among empties: plain in-order output.
- Lists of very different lengths: the long list finishes alone at the end.
- Duplicate values: order still follows lists, not values.
- k = 100 lists with 10^4 elements in total.
- The caller's lists are not mutated.

**Follow-ups:**
- *Generalise to iterators (not lists)?* Store the iterators in the deque; `next` calls `next(it)` and re-appends the iterator, and `hasNext` needs a one-element lookahead (see Q15 for the peeking pattern).
- *Why not `pop(0)` on a list?* `list.pop(0)` is O(n); a deque gives O(1) at both ends.
- *Why does the deque trick preserve order across rounds?* Each live list is re-appended after it serves, so every list is served once per cycle of the deque, in the original list order.

**Common mistakes:**
- Re-appending a list that just served its last element, then crashing on the next visit.
- Putting empty lists in the deque, so `hasNext` returns True when no element exists.
- Using `list.pop(0)` (O(n) per call).
- Tracking a global round counter with `i % k` and skipping exhausted lists in a loop (O(k) per call in the worst case).
- Copying elements in `__init__` (breaks laziness and doubles memory).

### Q39 ⭐ 🟡 Parallel courses with durations: the minimum time to finish everything. Courses are labelled 1..n (1 <= n <= 5*10^4); `relations` is a list of [prev, next] meaning prev must be fully finished before next can start (0 <= len <= 10^5); `time[i - 1]` (1 <= time <= 10^4) is how many months course i takes; any number of courses may run at the same time. Return `[total, finish]` where `finish[i - 1]` is the earliest month at which course i can be finished (start at the latest finish among its prerequisites, or month 0) and `total` is the maximum finish; if a cycle makes some course impossible return `[-1, []]`. Use Kahn's algorithm and propagate `start[next] = max(start[next], finish[prev])`; the answer is the longest weighted path in the DAG. Part 9 Q24 is the unit-time version (minimum semesters); this one weights the nodes. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a memoised recursive oracle on small DAGs with its own cycle detection on small inputs. Example: n=3, relations=[[1, 3], [2, 3]], time=[3, 2, 5] -> [8, [3, 2, 8]]; n=2, relations=[[1, 2], [2, 1]], time=[1, 1] -> [-1, []]; n=4, relations=[], time=[4, 9, 1, 2] -> [9, [4, 9, 1, 2]].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** Topological order (Kahn) with longest-path propagation on a DAG. Node weights are the course durations; the answer is the longest weighted path.

**Say this first (1 line):** "Kahn's algorithm, and when I finish a course I push start[next] = max(start[next], finish[course]); a cycle shows up as fewer than n courses ever reaching indegree zero, and then I return [-1, []]."

**Brute force:** Memoised recursion: `finish(v) = time[v] + max(finish(p) for p in prerequisites)` with a three-state mark (unvisited, in progress, done) to detect cycles. Correct, but recursion depth can reach n = 5 * 10^4, past CPython's limit of 1000, so the real solution must be iterative. The oracle uses it only on tiny graphs.

**Optimal:**
- Build adjacency from `relations` and count `indeg`. Put every course with indegree 0 in a queue (their start is month 0).
- Pop `u`: `finish[u] = start[u] + time[u - 1]`. For each course `v` after `u`: `start[v] = max(start[v], finish[u])` (v must wait for its slowest prerequisite), decrement `indeg[v]`, queue `v` when it reaches 0.
- When `u` is popped, all its prerequisites have been popped already (indegree 0), so `start[u]` is final. That is the invariant.
- Courses run in parallel without limit, so `finish[i]` is the earliest possible finish, and `total = max(finish)` is the length of the longest path measured in time.
- Cycle: courses on a cycle never reach indegree 0, so `done < n`; return `[-1, []]`. A cycle anywhere poisons the whole answer, even if other courses are fine.
- Duplicate relations are harmless (each copy raises `indeg` and lowers it once).
- Part 9 Q24 is the unit-time version asking for the number of semesters; here the weights make it a longest weighted path rather than a level count, so BFS levels are not enough.

**Complexity:** Time O(n + m) (each course and each relation handled once). Space O(n + m) for adjacency, `indeg`, `start`, `finish` and the queue.

**Dry run:** `n = 3`, `relations = [[1,3],[2,3]]`, `time = [3, 2, 5]`.
- `indeg = [_, 0, 0, 2]`; queue `[1, 2]`.
- Pop 1: `finish[1] = 0 + 3 = 3`; `start[3] = max(0, 3) = 3`; `indeg[3] = 1`.
- Pop 2: `finish[2] = 0 + 2 = 2`; `start[3] = max(3, 2) = 3`; `indeg[3] = 0`, queue 3.
- Pop 3: `finish[3] = 3 + 5 = 8`.
- Result `[8, [3, 2, 8]]`. Cycle example `[[1,2],[2,1]]`: both have indegree 1, the queue starts empty, `done = 0 < 2`, so `[-1, []]`. With no relations (`time = [4, 9, 1, 2]`) every finish equals its own time and the total is 9.

**Code:**
```python
import random
from collections import deque

random.seed(3901)


def min_time(n, relations, time):
    """Kahn's algorithm; start[v] = max finish of prerequisites; finish = start + time. Returns [total, finish]."""
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        g[a].append(b)
        indeg[b] += 1
    start = [0] * (n + 1)
    finish = [0] * (n + 1)
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        finish[u] = start[u] + time[u - 1]
        for v in g[u]:
            start[v] = max(start[v], finish[u])      # wait for the slowest prerequisite
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if done < n:                                     # a cycle leaves some courses with indegree > 0
        return [-1, []]
    return [max(finish[1:]), finish[1:]]


def brute(n, relations, time):
    """Memoised recursion over prerequisites with its own cycle detection (small n only)."""
    pre = {v: [] for v in range(1, n + 1)}
    for a, b in relations:
        pre[b].append(a)
    memo, state = {}, {}

    def fin(v):
        if state.get(v) == 1:
            raise ValueError('cycle')
        if v in memo:
            return memo[v]
        state[v] = 1
        memo[v] = max((fin(p) for p in pre[v]), default=0) + time[v - 1]
        state[v] = 2
        return memo[v]
    try:
        f = [fin(v) for v in range(1, n + 1)]
    except ValueError:
        return [-1, []]
    return [max(f), f]


def random_case(cyclic):
    n = random.randint(1, 7)
    order = list(range(1, n + 1))
    random.shuffle(order)
    rel = [[order[i], order[j]] for i in range(n) for j in range(i + 1, n) if random.random() < 0.35]
    if cyclic and n >= 2 and rel:
        a, b = random.choice(rel)
        rel.append([b, a])
    random.shuffle(rel)
    return n, rel, [random.randint(1, 9) for _ in range(n)]


# --- the prompt's examples ---
ex = [((3, [[1, 3], [2, 3]], [3, 2, 5]), [8, [3, 2, 8]]),
      ((2, [[1, 2], [2, 1]], [1, 1]), [-1, []]),
      ((4, [], [4, 9, 1, 2]), [9, [4, 9, 1, 2]])]
for args, want in ex:
    got = min_time(*args)
    print(args, '->', got)
    assert got == want == brute(*args)

# --- random cross-check (DAGs by construction, plus injected cycles) ---
cyc = 0
for i in range(2000):
    args = random_case(cyclic=(i % 3 == 0))
    got = min_time(*args)
    assert got == brute(*args), args
    cyc += got[0] == -1
print('random cases passed: 2000 (', cyc, 'with a cycle )')

# --- edge cases ---
assert min_time(1, [], [5]) == [5, [5]]                              # one course
assert min_time(3, [[1, 2], [2, 3]], [1, 1, 1]) == [3, [1, 2, 3]]    # chain: times add
assert min_time(3, [[1, 2], [1, 3], [2, 3], [1, 3]], [2, 3, 1]) == [6, [2, 5, 6]]   # duplicate relation is harmless
assert min_time(3, [[1, 2], [2, 3], [3, 1]], [1, 1, 1]) == [-1, []]  # 3-cycle
assert min_time(4, [[1, 2], [2, 1]], [1, 1, 1, 1]) == [-1, []]       # a cycle anywhere poisons the answer
n = 5 * 10 ** 4
chain = [[i, i + 1] for i in range(1, n)]
assert min_time(n, chain, [10 ** 4] * n)[0] == n * 10 ** 4          # n = 5*10^4, longest path, no recursion needed
print('edge asserts passed')
```

**Output (my run):**
```
(3, [[1, 3], [2, 3]], [3, 2, 5]) -> [8, [3, 2, 8]]
(2, [[1, 2], [2, 1]], [1, 1]) -> [-1, []]
(4, [], [4, 9, 1, 2]) -> [9, [4, 9, 1, 2]]
random cases passed: 2000 ( 472 with a cycle )
edge asserts passed
```

**Edge cases:**
- One course: `[time, [time]]`.
- A chain: durations add (n = 5 * 10^4 chain of 10^4-month courses gives 5 * 10^8, checked).
- No relations: total is the maximum single duration.
- A cycle in only part of the graph still returns `[-1, []]`.
- Duplicate relations (checked).
- Multiple roots and multiple leaves: the total is the max over all courses, not just the last popped.

**Follow-ups:**
- *Which courses are on the critical path?* Also store the predecessor that gave the max (or compare `finish[u] == start[v]` going backwards from the course with the largest finish).
- *Limited number of parallel courses?* Then it is a scheduling problem with a resource limit; a heap of running courses is the usual approach and the answer is no longer a pure longest path (editor knowledge, not tested here).
- *Why not Dijkstra?* Longest path in a DAG needs only one topological pass; Dijkstra's shortest-path logic does not apply to maximisation.

**Common mistakes:**
- Using `start[v] = finish[u]` (last writer wins) instead of `max`.
- Returning the finish of the last popped course instead of `max(finish)`.
- Counting levels (semesters) and ignoring durations.
- Forgetting to detect the cycle (returning a partial answer).
- Indexing `time` with `u` instead of `u - 1`.
- Recursive DFS on 5 * 10^4 courses.

### Q40 ⭐ 🔴 All-O(1) data structure. Implement class `AllOne()` with `inc(key)` (add one to the key's count, creating it at 1), `dec(key)` (subtract one; when the count reaches 0 the key disappears; `dec` of an unknown key does nothing), `getMaxKey()` and `getMinKey()`, all O(1). Both getters return '' when the structure is empty. Tie rule (the checker needs one answer): among keys with the maximum (minimum) count return the key that has held its CURRENT count the longest, that is whose count changed to this value earliest; a key that changes count joins the END of the new count's bucket. Use a doubly linked list of buckets ordered by count (dummy head and tail), each bucket holding an OrderedDict of its keys, plus a dict key -> bucket; moving a key to the neighbouring count is O(1) because the target bucket is adjacent, and an empty bucket is unlinked. `inc` and `dec` return None. Explain why a dict plus a heap would cost O(log n). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference that stores counts and a last-change stamp and scans all keys on small inputs. Example: init=[], ops=[['inc', ['a']], ['inc', ['b']], ['inc', ['b']], ['getMaxKey', []], ['getMinKey', []], ['inc', ['a']], ['inc', ['c']], ['getMaxKey', []], ['getMinKey', []], ['dec', ['b']], ['dec', ['b']], ['getMaxKey', []], ['dec', ['z']], ['getMinKey', []]] -> [null, null, null, 'b', 'a', null, null, 'b', 'c', null, null, 'a', null, 'c'].
**Asked at:** Design-problem lists and guides (a LeetCode Discuss post '10 Essential Design Problems for DSA Interviews', talentd.in design-topic pages, walkccc design-problem index, a designgurus snapshot-array write-up, techinterview.org LRU-cache and rate-limiter posts, InterviewBit LRU blog; search snippets only, not opened)

**Pattern:** Linked list of frequency buckets plus hash maps. Buckets are ordered by count; each bucket holds its keys in arrival order, and every move is to the adjacent bucket.

**Say this first (1 line):** "Tie rule: among keys at the max or min count I return the one that has held that count longest, and a key whose count changes joins the END of its new bucket; a doubly linked list of count buckets gives O(1) inc, dec, max and min."

**Brute force:** A dict of counts and a last-change stamp per key; both getters scan all keys for the max (min) count and the earliest stamp. inc and dec are O(1), the getters are O(n). This is the oracle. A dict plus a heap gives O(log n) for inc and dec (a push on every change, plus stale entries to skip), not O(1).

**Optimal:**
- Buckets: a doubly linked list with dummy head and tail, sorted by count ascending (head side = small counts). Each bucket stores its count and an `OrderedDict` of keys (arrival order, oldest first). A `where` dict maps key to its bucket.
- `inc(key)`: a new key goes to the bucket with count 1 (create it after the head if missing). An existing key in a bucket with count c moves to the bucket with count c + 1: use the next bucket if its count is c + 1, else create one right after the current bucket. Append the key at the END of the new bucket's `OrderedDict`. Delete it from the old bucket and unlink the old bucket if it became empty.
- `dec(key)`: unknown key, do nothing. Count 1: remove the key (it disappears). Otherwise move it to the bucket with count c - 1 (previous bucket if its count matches, else create one before), append at the end; unlink the old bucket if empty.
- `getMaxKey()`: the first key of the bucket just before the tail (the key that has held the max count longest). `getMinKey()`: the first key of the bucket just after the head. Empty structure: `''`.
- Why moves are O(1): a count only changes by 1, so its target bucket is adjacent or must be created exactly at that spot; no search. An empty bucket is unlinked in O(1) because it is a doubly linked node.
- Invariants (asserted over 3000 random steps): bucket counts strictly increase along the list, no bucket is empty, and the total keys in buckets equals `len(where)`.
- Thread safety (concept only): inc and dec touch two buckets and two dict entries; one lock around all methods keeps the list and `where` consistent. Reads like getMaxKey need the lock too if writers can be mid-move.

**Complexity:** `inc`, `dec`, `getMaxKey`, `getMinKey` all O(1) average (dict lookups, adjacent linked-list pointer changes, `OrderedDict` delete/append/first-item in O(1)). Space O(n) for n distinct live keys (each key appears in one bucket and in `where`); at most n buckets.

**Dry run:** the prompt's example.
- `inc a`: bucket `1:{a}`. `inc b`: `1:{a,b}`. `inc b`: b leaves bucket 1 and a new bucket 2 is created after it: `1:{a}`, `2:{b}`.
- `getMaxKey` -> b (first key of the last bucket). `getMinKey` -> a.
- `inc a`: a leaves bucket 1 (now empty, unlinked) and joins the end of bucket 2: `2:{b,a}`. `inc c`: new bucket `1:{c}` before it.
- `getMaxKey` -> b (b held count 2 before a did). `getMinKey` -> c.
- `dec b`: b moves to bucket 1: `1:{c,b}`, `2:{a}`. `dec b`: count 1, so b disappears: `1:{c}`, `2:{a}`.
- `getMaxKey` -> a. `dec z`: unknown, nothing. `getMinKey` -> c.
- Result `[None, None, None, 'b', 'a', None, None, 'b', 'c', None, None, 'a', None, 'c']`, matches.

**Code:**
```python
import random
from collections import OrderedDict

random.seed(4001)


class Bucket:
    """All keys that currently hold the same count; keys in order of arrival (oldest first)."""
    __slots__ = ('cnt', 'keys', 'prev', 'next')

    def __init__(self, cnt):
        self.cnt, self.keys, self.prev, self.next = cnt, OrderedDict(), None, None


class AllOne:
    def __init__(self):
        self.head, self.tail = Bucket(0), Bucket(0)          # dummies: head side = small counts
        self.head.next, self.tail.prev = self.tail, self.head
        self.where = {}                                      # key -> its bucket

    def _insert_after(self, node, cnt):
        b = Bucket(cnt)
        b.prev, b.next = node, node.next
        node.next.prev = b
        node.next = b
        return b

    def _drop_if_empty(self, b):
        if not b.keys:                                       # unlink an empty bucket: O(1)
            b.prev.next, b.next.prev = b.next, b.prev

    def inc(self, key):
        b = self.where.get(key)
        if b is None:                                        # new key: count 1
            nb = self.head.next if self.head.next.cnt == 1 else self._insert_after(self.head, 1)
        else:
            nb = b.next if (b.next is not self.tail and b.next.cnt == b.cnt + 1) else self._insert_after(b, b.cnt + 1)
            del b.keys[key]
            self._drop_if_empty(b)
        nb.keys[key] = None                                  # joins the END of the new bucket
        self.where[key] = nb

    def dec(self, key):
        b = self.where.get(key)
        if b is None:                                        # unknown key: nothing happens
            return
        del b.keys[key]
        if b.cnt == 1:
            del self.where[key]                              # count 0: the key disappears
        else:
            pb = b.prev if (b.prev is not self.head and b.prev.cnt == b.cnt - 1) else self._insert_after(b.prev, b.cnt - 1)
            pb.keys[key] = None
            self.where[key] = pb
        self._drop_if_empty(b)

    def getMaxKey(self):
        return next(iter(self.tail.prev.keys)) if self.where else ''      # oldest key in the top bucket

    def getMinKey(self):
        return next(iter(self.head.next.keys)) if self.where else ''


class NaiveAllOne:
    """Counts + a last-change stamp per key; getters scan every key."""

    def __init__(self):
        self.c, self.stamp, self.t = {}, {}, 0

    def inc(self, key):
        self.t += 1
        self.c[key] = self.c.get(key, 0) + 1
        self.stamp[key] = self.t

    def dec(self, key):
        if key not in self.c:
            return
        self.t += 1
        self.c[key] -= 1
        self.stamp[key] = self.t
        if self.c[key] == 0:
            del self.c[key], self.stamp[key]

    def getMaxKey(self):
        if not self.c:
            return ''
        m = max(self.c.values())
        return min((self.stamp[k], k) for k in self.c if self.c[k] == m)[1]     # earliest change wins

    def getMinKey(self):
        if not self.c:
            return ''
        m = min(self.c.values())
        return min((self.stamp[k], k) for k in self.c if self.c[k] == m)[1]


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's example ---
ops = [['inc', ['a']], ['inc', ['b']], ['inc', ['b']], ['getMaxKey', []], ['getMinKey', []], ['inc', ['a']],
       ['inc', ['c']], ['getMaxKey', []], ['getMinKey', []], ['dec', ['b']], ['dec', ['b']], ['getMaxKey', []],
       ['dec', ['z']], ['getMinKey', []]]
r = run(AllOne, [], ops)
print('example:', r)
assert r == [None, None, None, 'b', 'a', None, None, 'b', 'c', None, None, 'a', None, 'c'] == run(NaiveAllOne, [], ops)

# --- random operation-sequence oracle ---
keys = ['a', 'b', 'c', 'd', 'e']
total = 0
for _ in range(1500):
    ops = []
    for _ in range(random.randint(1, 40)):
        x = random.random()
        ops.append(['inc', [random.choice(keys)]] if x < 0.45 else ['dec', [random.choice(keys)]] if x < 0.75
                   else [random.choice(['getMaxKey', 'getMinKey']), []])
    assert run(AllOne, [], ops) == run(NaiveAllOne, [], ops), ops
    total += len(ops)
print('random ops compared:', total)

# --- structural invariant: bucket counts strictly increase and no bucket is empty ---
a = AllOne()
for _ in range(3000):
    k = random.choice(keys)
    a.inc(k) if random.random() < 0.55 else a.dec(k)
    n, last, seen = a.head.next, 0, 0
    while n is not a.tail:
        assert n.cnt > last and n.keys
        last = n.cnt
        seen += len(n.keys)
        n = n.next
    assert seen == len(a.where)
print('bucket list invariant held')

# --- the tie rule in action: who is "oldest at this count" ---
t = AllOne()
for k in ['x', 'y', 'z']:
    t.inc(k)                                     # all count 1, x arrived first
print('min key with x, y, z at 1:', t.getMinKey())
t.inc('x'); t.dec('x')                           # x goes 1 -> 2 -> 1: it rejoins the END of bucket 1
print('after x goes 1->2->1, min key:', t.getMinKey(), '(y has held count 1 the longest)')
assert t.getMinKey() == 'y'

# --- edge cases ---
e = AllOne()
assert e.getMaxKey() == '' and e.getMinKey() == ''                     # empty
e.dec('nope'); assert e.getMaxKey() == ''                              # dec of unknown key
e.inc('k'); assert e.getMaxKey() == e.getMinKey() == 'k'               # one key is both max and min
e.dec('k'); assert e.getMaxKey() == '' and not e.where                 # count 0 removes it
e.inc('k'); e.inc('k'); e.inc('k'); e.dec('k'); assert e.getMaxKey() == 'k'
for k in 'pq':
    e.inc(k)
assert e.getMinKey() == 'p' and e.getMaxKey() == 'k'
big = AllOne()
for i in range(10 ** 4):
    big.inc('key%d' % i)
for i in range(10 ** 4):
    big.inc('key%d' % i)
assert big.getMaxKey() == 'key0' and big.getMinKey() == 'key0'         # all at 2, key0 reached 2 first
print('edge asserts passed')
```

**Output (my run):**
```
example: [None, None, None, 'b', 'a', None, None, 'b', 'c', None, None, 'a', None, 'c']
random ops compared: 30805
bucket list invariant held
min key with x, y, z at 1: x
after x goes 1->2->1, min key: y (y has held count 1 the longest)
edge asserts passed
```

**Edge cases:**
- Empty structure: both getters return `''`.
- `dec` of an unknown key does nothing (and does not change the stamps used by ties).
- One key is both max and min.
- A key going to count 0 is removed, and `inc` later restarts it at 1 at the end of bucket 1.
- Tie after a round trip: `x` goes 1 -> 2 -> 1 and joins the end of bucket 1, so `y` (which has held 1 longest) is the min key (shown in the run).
- 10^4 keys each incremented twice: all share bucket 2 and the first to reach 2 is returned.

**Follow-ups:**
- *Why OrderedDict and not a set per bucket?* A set has no order, so the tie rule would be arbitrary; an `OrderedDict` gives the oldest key in O(1) with `next(iter(...))` and O(1) delete.
- *Why not a dict plus a heap?* Every inc or dec pushes a new entry, so each is O(log n), and stale entries need lazy cleanup.
- *Could the buckets be a sorted list?* Inserting or deleting a bucket in the middle is O(n); the adjacency argument is what makes the linked list O(1).

**Common mistakes:**
- Forgetting to unlink an empty bucket (the min or max getter then reads an empty bucket).
- Creating the new bucket on the wrong side of the current one on `dec`.
- Not removing the key from `where` when its count hits 0.
- Adding the key at the front of the new bucket (breaks the stated tie rule).
- Using a set per bucket and getting arbitrary ties.
- Treating `dec` of an unknown key as an error, or returning `None` instead of `''` from an empty getter.

### Q41 ⭐ 🔴 Tarjan's strongly connected components, iteratively, with a fixed numbering. `n` nodes 0..n-1 (1 <= n <= 10^5), `edges` directed [u, v] (0 <= len <= 2*10^5; repeats and self loops allowed). Run Tarjan's one-pass algorithm: start a DFS from node 0, 1, 2, ... in that order (skipping visited nodes) and follow each node's out-edges in the ORDER THEY APPEAR in `edges`; keep `idx` (discovery number), `low`, an `on_stack` flag and the node stack; when low[u] == idx[u] pop the stack down to u and give those nodes the next component number 0, 1, 2, ... (so components are numbered in the order they are completed). Return `[comp, count, cross]`: `comp[v]` is the component number of node v, `count` the number of components, and `cross` the number of DISTINCT pairs (comp[u], comp[v]) over edges with different components (the edge count of the condensation). Explain why this numbering is a reverse topological order of the condensation (every edge u -> v has comp[u] >= comp[v]), why only nodes still ON the stack may lower `low[u]` (a node already assigned to a finished component cannot be in u's component), and why the code must be iterative (a path graph of 10^5 nodes would exceed CPython's default recursion limit of 1000). Compare with Kosaraju (Q20): one DFS instead of two plus a reversed graph. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive Tarjan oracle with identical visiting order on small graphs (plus the property comp[u] >= comp[v] on every edge) on small inputs. Example: n=5, edges=[[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [[2, 2, 2, 1, 0], 3, 2]; n=3, edges=[[0, 1], [1, 0], [0, 2], [0, 2]] -> [[1, 1, 0], 2, 1].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)
**Pattern:** Strongly connected components with Tarjan's one-pass DFS (discovery index, low-link, node stack), written with an explicit stack. Directed graph, so "who can reach whom both ways" is the question.

**Say this first (1 line):** "One DFS gives each node a discovery number and a low-link; when a node's low equals its own number it is the root of a component, so I pop the stack down to it, and I keep the DFS on a hand-made stack because a 10^5-node path would blow CPython's 1000-frame limit."

**Brute force:** Compute reachability from every node (BFS each), then group nodes u, v with u reaches v and v reaches u. O(n * (n + m)); Floyd-Warshall style closure is O(n^3). Fine for 8 nodes, hopeless at 10^5. I use it only as the idea behind the definition.

**Optimal:**
- Visit nodes 0, 1, 2, ... and follow out-edges in input order. Each new node gets `idx` (discovery number), `low = idx`, and goes on the node stack with `on_stack = True`.
- Edge u -> v with v unvisited: tree edge, descend. When v finishes, `low[u] = min(low[u], low[v])`.
- Edge u -> v with v visited and still ON the stack: `low[u] = min(low[u], idx[v])`.
- When u finishes and `low[u] == idx[u]`, u is the root of a component: pop until u, give them the next number.
- Why only on-stack nodes may lower `low`: a visited node that is NOT on the stack already belongs to a finished component. If it could reach back to u, u would have been inside that component. So that edge is a cross edge to a finished component and must be ignored. Dropping the test corrupts the components (the run below finds a graph where it changes the answer).
- Why numbering is reverse topological: a component is numbered when its root finishes. For an edge u -> v across components, v's component must be complete before u's root can finish (v was either already finished or is explored beneath u), so comp[v] was numbered first: `comp[u] >= comp[v]`.
- Iterative: the work stack holds `(node, next edge position)`. Popping an entry with edges left means "continue u"; pushing a child means "recurse"; an exhausted entry means "return", where I push the child's `low` up into the parent (the parent is the entry below on the work stack).
- Versus Kosaraju (Q20): Kosaraju needs two DFS passes and a reversed graph; Tarjan needs one pass and no reversed graph, but the low-link logic is subtler.

**Complexity:**
- Time O(n + m): every node is pushed and popped from each stack once, every edge is looked at once. The `cross` count uses a set of at most m pairs.
- Space O(n + m) for the adjacency list, plus O(n) for idx, low, on_stack, comp, node stack and work stack.

**Dry run:** first example, n=5, edges 0->1, 1->2, 2->0, 1->3, 3->4.
- Visit 0 (idx 0), push. Edge 0->1: visit 1 (idx 1). Edge 1->2: visit 2 (idx 2). Stack is [0, 1, 2].
- Edge 2->0: 0 is on the stack, so low[2] = min(2, 0) = 0. Node 2 finishes with low 0 != idx 2: no pop. Parent 1 gets low[1] = 0.
- Back at 1, edge 1->3: visit 3 (idx 3), then 3->4: visit 4 (idx 4). Node 4 finishes with low 4 == idx 4: pop 4, comp 0.
- Node 3 finishes with low 3 == idx 3: pop 3, comp 1. Node 1 finishes with low 0, no pop; node 0 finishes with low 0 == idx 0: pop 2, 1, 0 as comp 2.
- Result comp = [2, 2, 2, 1, 0], count 3. Cross pairs: edge 1->3 gives (2, 1), edge 3->4 gives (1, 0), so cross = 2. Every edge has comp[u] >= comp[v].

**Code:**
```python
import random, sys
random.seed(41)

def tarjan_iter(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)                       # keep input order
    idx = [-1] * n; low = [0] * n; on = [False] * n
    comp = [-1] * n; stack = []; counter = 0; nc = 0
    for s in range(n):
        if idx[s] != -1:
            continue
        idx[s] = low[s] = counter; counter += 1
        stack.append(s); on[s] = True
        work = [(s, 0)]                      # (node, next edge position)
        while work:
            u, i = work.pop()
            if i < len(g[u]):
                work.append((u, i + 1))
                v = g[u][i]
                if idx[v] == -1:             # tree edge: "recurse"
                    idx[v] = low[v] = counter; counter += 1
                    stack.append(v); on[v] = True
                    work.append((v, 0))
                elif on[v]:                  # back/cross edge into the open stack
                    low[u] = min(low[u], idx[v])
            else:                            # u is finished
                if low[u] == idx[u]:         # u is the root of a component
                    while True:
                        w = stack.pop(); on[w] = False; comp[w] = nc
                        if w == u:
                            break
                    nc += 1
                if work:                     # "return" to the parent
                    p = work[-1][0]
                    low[p] = min(low[p], low[u])
    cross = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, nc, cross]

def tarjan_rec(n, edges):                    # oracle: textbook recursion, same visiting order
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n
    st = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; st.append(u); on[u] = True
        for v in g[u]:
            if idx[v] == -1:
                dfs(v); low[u] = min(low[u], low[v])
            elif on[v]:
                low[u] = min(low[u], idx[v])
        if low[u] == idx[u]:
            while True:
                w = st.pop(); on[w] = False; comp[w] = box[1]
                if w == u:
                    break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1:
            dfs(s)
    cross = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, box[1], cross]

# examples from the prompt
assert tarjan_iter(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == [[2, 2, 2, 1, 0], 3, 2]
assert tarjan_iter(3, [[0, 1], [1, 0], [0, 2], [0, 2]]) == [[1, 1, 0], 2, 1]
print('examples ok')

# seeded random cross-check vs the recursive oracle + reverse-topological property
for _ in range(600):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 16))]
    a = tarjan_iter(n, edges)
    assert a == tarjan_rec(n, edges), (n, edges)
    comp = a[0]
    assert all(comp[u] >= comp[v] for u, v in edges)
print('600 random graphs: iterative == recursive oracle, comp[u] >= comp[v] on every edge')

# edge cases
assert tarjan_iter(1, []) == [[0], 1, 0]
assert tarjan_iter(1, [[0, 0]]) == [[0], 1, 0]               # self loop
assert tarjan_iter(3, []) == [[0, 1, 2], 3, 0]               # isolated nodes, completed in order
assert tarjan_iter(3, [[0, 1], [1, 2], [2, 0]]) == [[0, 0, 0], 1, 0]

# why iterative: a path of 1500 nodes breaks the recursive version, 10^5 is fine iteratively
path = lambda N: [[i, i + 1] for i in range(N - 1)]
try:
    tarjan_rec(1500, path(1500)); print('recursive survived?!')
except RecursionError:
    print('recursive version: RecursionError at 1500-node path')
N = 10**5
comp, cnt, cross = tarjan_iter(N, path(N))
assert cnt == N and cross == N - 1 and comp[0] == N - 1 and comp[N - 1] == 0
print('iterative 10^5 path ok: components', cnt, 'condensation edges', cross)
print('first example:', tarjan_iter(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))

# the on-stack test matters: without it a cross edge into a finished component corrupts low and the answer is wrong
def tarjan_no_on_stack(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    idx = [-1] * n; low = [0] * n; comp = [-1] * n; st = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; st.append(u)
        for v in g[u]:
            if idx[v] == -1: dfs(v); low[u] = min(low[u], low[v])
            else: low[u] = min(low[u], idx[v])               # BUG: also fires for finished components
        if low[u] == idx[u]:
            while True:
                w = st.pop(); comp[w] = box[1]
                if w == u: break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1: dfs(s)
    return comp
for _ in range(5000):
    n = random.randint(2, 5)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(1, 7))]
    if tarjan_no_on_stack(n, edges) != tarjan_iter(n, edges)[0]:
        print('without the on-stack test:', n, edges, '->', tarjan_no_on_stack(n, edges), 'instead of', tarjan_iter(n, edges)[0]); break
else:
    raise SystemExit('no counterexample found')
```

**Output (my run):**
```
examples ok
600 random graphs: iterative == recursive oracle, comp[u] >= comp[v] on every edge
recursive version: RecursionError at 1500-node path
iterative 10^5 path ok: components 100000 condensation edges 99999
first example: [[2, 2, 2, 1, 0], 3, 2]
without the on-stack test: 3 [[1, 0], [0, 2], [0, 0], [2, 0]] -> [0, -1, 0] instead of [0, 1, 0]
```

**Edge cases:**
- n = 1, no edges: one component, cross 0.
- Self loop: a node with only a self loop is its own component (the loop is skipped by `comp[u] != comp[v]`).
- Repeated edges: `cross` counts DISTINCT component pairs, hence the set. The second example has two copies of 0 -> 2 and still gives cross = 1.
- No edges: every node is its own component, numbered 0..n-1 in visiting order.
- A long path (10^5 nodes): components are numbered from the far end, so comp[0] = n - 1.
- Disconnected graph: the outer loop restarts the DFS at the next unvisited node.

**Follow-ups:**
- *Why not just reuse Kosaraju?* Both are O(n + m). Tarjan needs one DFS and no transposed graph, which saves memory; Kosaraju is easier to explain and to get right under pressure (Q20).
- *Where do I read the condensation DAG?* The `cross` pairs are its edges; because of the numbering, they all go from a higher component number to a lower one, so listing components from the highest number down is a topological order of the condensation.
- *What breaks if I drop the `on_stack` check?* A cross edge into an already finished component would drag `low[u]` below `idx[u]`, so u never becomes a root and the components come out wrong (in the run, one node is never assigned at all). The run below prints a small graph where the answer changes.

**Common mistakes:**
- Using `low[u] = min(low[u], low[v])` for a non-tree edge instead of `idx[v]` (it still works in many tests but muddles the definition; keep `idx[v]`).
- Forgetting to propagate the child's low into the parent when simulating the return.
- Not following edges in input order, so the numbering differs from the required one.
- Writing the recursive version and trusting it: it raises RecursionError on the 1500-node path, as the output shows.
- Counting `cross` with a plain counter, so repeated edges are over-counted.

### Q42 ⭐ 🔴 Articulation points (cut vertices). `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` undirected [u, v] pairs (0 <= len <= 2*10^5; the graph may be disconnected; parallel edges and self loops may occur). A node is an articulation point when deleting it (and its edges) increases the number of connected components among the remaining nodes beyond what its own removal explains (an isolated node, or a node alone in its component, is NOT an articulation point). Return the articulation points sorted ascending. Use the discovery times and `low` values of Q33 with the two rules: a DFS ROOT is an articulation point when it has at least two DFS-tree children; a non-root p is one when some child u has low[u] >= disc[p] (note >=, where a bridge needs >). Write it iteratively because a path of 10^5 nodes exceeds CPython's default recursion limit of 1000. Say why >= is right for vertices and > for edges (a back edge that lands on p itself still leaves p as the cut vertex but saves the edge). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that deletes each node in turn and recounts connected components on small inputs. Example: n=5, edges=[[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [1, 3]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> []; n=4, edges=[[0, 1], [0, 2], [0, 3]] -> [0].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)
**Pattern:** Articulation points with DFS discovery times and low-link values, written iteratively. The same machinery as bridges (Q33), with a different test.

**Say this first (1 line):** "A DFS root is a cut vertex if it has two or more tree children; any other node p is one if some child u has low[u] >= disc[p], meaning u's subtree cannot climb above p."

**Brute force:** For each node v, delete it and count connected components again (union-find or BFS). O(n * (n + m)). It is my oracle for small inputs and the definition in code.

**Optimal:**
- One DFS per component. `disc[u]` is the discovery time; `low[u]` is the smallest discovery time reachable from u's subtree using tree edges down and at most one back edge up.
- When a child u of p finishes: `low[p] = min(low[p], low[u])`. If p is not the root and `low[u] >= disc[p]`, p is an articulation point.
- Root rule: the root has no ancestors, so it is a cut vertex only if it has at least two DFS-tree children (its children are then only connected through it).
- Why `>=` for vertices but `>` for edges: if the best u's subtree can do is reach p itself (`low[u] == disc[p]`), then deleting the EDGE p-u keeps the subtree attached via the back edge to p, so it is not a bridge. But deleting the VERTEX p removes that landing point, so the subtree is cut off, and p is a cut vertex. Example: two triangles sharing node 2; with `>` the code would miss node 2 (the output shows it).
- Skip the arrival edge by edge id, not by parent node, so a parallel edge to the parent counts as a back edge. Self loops are dropped.
- Iterative form: the work stack holds `(node, arrival edge id, next adjacency position)`; when an entry is exhausted, the entry below is the parent.

**Complexity:** Time O(n + m): each adjacency entry is read once. Space O(n + m): adjacency list, disc, low, work stack.

**Dry run:** first example, edges 0-1, 1-2, 2-0, 1-3, 3-4.
- DFS from 0: disc[0]=0; go to 1 (disc 1); from 1 go to 2 (disc 2); at 2, neighbour 0 is visited (not the arrival edge), so low[2] = 0.
- 2 finishes: low[1] = 0; check low[2] = 0 >= disc[1] = 1? No.
- From 1 go to 3 (disc 3), then 4 (disc 4). 4 finishes with low 4: 4 >= disc[3] = 3, so 3 is an articulation point.
- 3 finishes: low[3] = 3 >= disc[1] = 1, so 1 is an articulation point.
- 1 finishes, parent is the root 0 with one tree child, so 0 is not a cut vertex. Answer [1, 3].

**Code:**
```python
import random
random.seed(42)

def articulation(n, edges):
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:                            # self loops never matter
            g[u].append((v, i)); g[v].append((u, i))
    disc = [-1] * n; low = [0] * n; t = 0; arts = set()
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = t; t += 1; kids = 0
        st = [(s, -1, 0)]                     # (node, edge id used to arrive, next adjacency position)
        while st:
            u, pe, i = st.pop()
            if i < len(g[u]):
                st.append((u, pe, i + 1))
                v, e = g[u][i]
                if e == pe:                   # skip the arrival edge by id (parallel edges still count)
                    continue
                if disc[v] == -1:
                    disc[v] = low[v] = t; t += 1
                    st.append((v, e, 0))
                else:
                    low[u] = min(low[u], disc[v])
            elif st:                          # u finished; its parent entry is on top
                p = st[-1][0]
                low[p] = min(low[p], low[u])
                if p == s:
                    kids += 1
                elif low[u] >= disc[p]:       # >= : the back edge may land ON p
                    arts.add(p)
        if kids >= 2:
            arts.add(s)
    return sorted(arts)

def comps(n, edges, skip=-1):
    p = list(range(n))
    def f(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges:
        if u != skip and v != skip:
            p[f(u)] = f(v)
    return len({f(x) for x in range(n) if x != skip})

def oracle(n, edges):                         # delete each node and recount components
    base = comps(n, edges)
    out = []
    for v in range(n):
        isolated = not any((u == v) != (w == v) for u, w in edges)   # no edge to another node
        expected = base - 1 if isolated else base                     # removing it explains this much
        if comps(n, edges, v) > expected:
            out.append(v)
    return out

assert articulation(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == [1, 3]
assert articulation(3, [[0, 1], [1, 2], [2, 0]]) == []
assert articulation(4, [[0, 1], [0, 2], [0, 3]]) == [0]
print('examples ok')

for _ in range(800):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 12))]
    assert articulation(n, edges) == oracle(n, edges), (n, edges)
print('800 random graphs match the delete-each-node oracle')

assert articulation(1, []) == [] and articulation(2, [[0, 1]]) == []     # lone node, single edge
assert articulation(2, [[0, 1], [0, 1]]) == []                           # parallel edges
assert articulation(3, [[0, 1], [1, 2]]) == [1]                          # path
assert articulation(4, [[0, 0], [1, 2], [2, 3]]) == [2]                  # disconnected + self loop
assert articulation(4, [[0, 1], [1, 2], [2, 3], [3, 0]]) == []           # cycle

# '>' instead of '>=' is wrong for vertices: a cycle hanging off p has low[child] == disc[p]
def art_gt(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v); g[v].append(u)
    disc = [-1] * n; low = [0] * n; res = set(); t = [0]
    def dfs(u, p, root):
        disc[u] = low[u] = t[0]; t[0] += 1; kids = 0
        for v in g[u]:
            if v == p: continue
            if disc[v] == -1:
                kids += 1; dfs(v, u, False); low[u] = min(low[u], low[v])
                if not root and low[v] > disc[u]: res.add(u)
            else: low[u] = min(low[u], disc[v])
        if root and kids >= 2: res.add(u)
    for s in range(n):
        if disc[s] == -1: dfs(s, -1, True)
    return sorted(res)
bowtie = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]]               # two triangles sharing node 2
print('bowtie: >= gives', articulation(5, bowtie), ' > gives', art_gt(5, bowtie))
assert articulation(5, bowtie) == [2] and art_gt(5, bowtie) == []

N = 10**5
assert articulation(N, [[i, i + 1] for i in range(N - 1)]) == list(range(1, N - 1))
print('10^5 path iterative ok')
print('first example:', articulation(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))
```

**Output (my run):**
```
examples ok
800 random graphs match the delete-each-node oracle
bowtie: >= gives [2]  > gives []
10^5 path iterative ok
first example: [1, 3]
```

**Edge cases:**
- A single node, or two nodes with one edge: no articulation points (removing a node leaves one component or none).
- Isolated nodes and a node alone in its component are never articulation points.
- Parallel edges between the same pair: still no cut vertex; the second copy is a back edge because the arrival edge is skipped by id.
- Self loops: ignored.
- Disconnected graph: run the DFS from each unvisited node, and apply the root rule per DFS tree.
- Path of 10^5 nodes: every inner node is a cut vertex and nothing recurses.

**Follow-ups:**
- *How do I get bridges at the same time?* Same disc and low; test `low[u] > disc[p]` (Q33).
- *Why is the root special?* With no parent, `low[u] >= disc[root]` is always true, so the child test would flag every root. The real question is whether the root has at least two separate child subtrees.
- *Can I find the blocks (biconnected components)?* Yes: push edges on a stack and pop a block whenever `low[u] >= disc[p]`. Not needed for this question.

**Common mistakes:**
- Using `>` (bridge rule) and missing cut vertices that sit on a cycle through the parent.
- Applying the child test to the root, flagging it always.
- Skipping the parent by node instead of by edge id, which breaks parallel edges.
- Counting root children as DFS neighbours instead of DFS-tree children.
- Recursive DFS on a path of 10^5 nodes.

### Q43 ⭐ 🔴 Maximum bipartite matching with augmenting paths (Kuhn's algorithm). `L` left nodes 0..L-1 and `R` right nodes 0..R-1 (1 <= L, R <= 300) with `edges`, a list of [left, right] pairs (0 <= len <= 3000, repeats allowed). A matching pairs each node with at most one partner along an edge. Return `[size, saturated]`: the maximum number of matched pairs and whether it equals L (every left node matched). For each left node run a DFS that tries each neighbour v not yet seen in this attempt: if v is free or its current partner can be re-matched elsewhere (recursive call), take v. Time O(L * E); the recursion depth is at most L <= 300, far below CPython's default recursion limit of 1000, so recursion is fine (a version for much larger L would need an explicit stack or Hopcroft-Karp). Explain why an augmenting path is the only way a matching can grow (Berge's theorem, stated, not proved) and the link to the earlier basic colouring check Part 9 Q21 (a graph is bipartite exactly when it has no odd cycle) and to 'assign jobs to workers' questions. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an exhaustive oracle that tries every assignment of right nodes with a memoised DP over bitmasks (L, R <= 6) on small inputs. Example: L=3, R=3, edges=[[0, 0], [0, 1], [1, 0], [2, 0]] -> [2, False]; L=2, R=2, edges=[[0, 0], [0, 1], [1, 0]] -> [2, True].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)
**Pattern:** Maximum bipartite matching by repeated augmenting-path search (Kuhn's algorithm); the DFS depth is at most L <= 300 so ordinary recursion is fine.

**Say this first (1 line):** "For each left node I try to find an augmenting path: take a free right neighbour, or ask that neighbour's current partner to move elsewhere; each success grows the matching by one."

**Brute force:** Try every assignment of right nodes to left nodes (including "unmatched"), memoised over a bitmask of used right nodes: O(L * 2^R) states. Only feasible for R <= about 20; I use it as the oracle with L, R <= 6.

**Optimal:**
- Keep `match_r[v]`, the left partner of right node v (or -1).
- For left node u run `try_augment(u, seen)`. For each neighbour v not yet in `seen`: mark it, and if v is free, or `try_augment(match_r[v], seen)` succeeds, set `match_r[v] = u` and return True.
- `seen` is fresh for every left node. It stops the search from visiting a right node twice in one attempt, which bounds each attempt to O(E).
- Why augmenting paths are the only way to grow (Berge's theorem, stated, not proved): a matching is maximum exactly when it has no augmenting path, i.e. an alternating path from a free left node to a free right node. Flipping such a path adds one pair. So if the search from u fails, no later change can help u in this round, and the algorithm is correct.
- A plain greedy (first free neighbour) is not enough: left 0 grabs right 0 and left 1, whose only choice is right 0, is stuck. Kuhn moves left 0 to right 1.
- Link to Part 9 Q21: a graph is bipartite exactly when it has no odd cycle; matching assumes the two sides are already given. 'Assign jobs to workers' is this model: left = workers, right = jobs, an edge when the worker can do the job.

**Complexity:** Time O(L * E): up to L attempts, each visits each edge at most once. With L, R <= 300 and E <= 3000 that is under a million steps. Space O(L + R + E); the recursion depth is at most L (the code run below measures 300 on a worst-case chain). For much larger inputs use Hopcroft-Karp (O(E sqrt V)) with an explicit stack.

**Dry run:** second example, L=2, R=2, edges 0-0, 0-1, 1-0.
- Left 0: neighbour right 0 is free, so match_r[0] = 0.
- Left 1: neighbour right 0 is taken by left 0; mark it seen and ask left 0 to move. Left 0 skips right 0 (seen), tries right 1: free, so match_r[1] = 0. Back in left 1: match_r[0] = 1.
- Matching: left 0 with right 1, left 1 with right 0. Size 2 = L, so [2, True].
- First example (L=3, R=3, edges 0-0, 0-1, 1-0, 2-0): left 0 takes right 0; left 1 pushes left 0 to right 1; left 2 only knows right 0, whose owner (left 1) has no other choice, so it fails. Size 2, [2, False].

**Code:**
```python
import random, sys
from functools import lru_cache
random.seed(43)

def kuhn(L, R, edges):
    g = [[] for _ in range(L)]
    for u, v in edges:
        g[u].append(v)
    match_r = [-1] * R                        # match_r[v] = left partner of right node v

    def try_augment(u, seen):                 # recursion depth <= L <= 300
        for v in g[u]:
            if v in seen:
                continue
            seen.add(v)
            if match_r[v] == -1 or try_augment(match_r[v], seen):
                match_r[v] = u                # flip the augmenting path
                return True
        return False

    size = sum(1 for u in range(L) if try_augment(u, set()))
    return [size, size == L]

def oracle(L, R, edges):                      # exhaustive: memoised DP over bitmasks of used right nodes
    g = [set() for _ in range(L)]
    for u, v in edges:
        g[u].add(v)
    @lru_cache(None)
    def f(i, mask):
        if i == L:
            return 0
        best = f(i + 1, mask)                 # leave left node i unmatched
        for v in g[i]:
            if not mask >> v & 1:
                best = max(best, 1 + f(i + 1, mask | 1 << v))
        return best
    s = f(0, 0)
    return [s, s == L]

assert kuhn(3, 3, [[0, 0], [0, 1], [1, 0], [2, 0]]) == [2, False]
assert kuhn(2, 2, [[0, 0], [0, 1], [1, 0]]) == [2, True]
print('examples ok')

for _ in range(500):
    L, R = random.randint(1, 6), random.randint(1, 6)
    edges = [[random.randrange(L), random.randrange(R)] for _ in range(random.randint(0, 14))]
    assert kuhn(L, R, edges) == oracle(L, R, edges), (L, R, edges)
print('500 random small graphs match the bitmask oracle')

assert kuhn(1, 1, []) == [0, False]
assert kuhn(2, 2, [[0, 0], [0, 0], [1, 0]]) == [1, False]   # repeats, one right node
assert kuhn(3, 1, [[0, 0], [1, 0], [2, 0]]) == [1, False]
# greedy without re-matching is not enough: left 0 grabs right 0, then left 1 is stuck
def greedy(L, R, edges):
    used = set(); n = 0; g = [[] for _ in range(L)]
    for u, v in edges: g[u].append(v)
    for u in range(L):
        for v in g[u]:
            if v not in used: used.add(v); n += 1; break
    return n
E = [[0, 0], [0, 1], [1, 0]]
print('greedy gives', greedy(2, 2, E), 'Kuhn gives', kuhn(2, 2, E)[0])
assert greedy(2, 2, E) == 1 and kuhn(2, 2, E)[0] == 2
# max size: L = R = 300 where left i prefers right i-1 (already owned), forcing a ~300-deep augmenting path
L = 300
deep = [[0, 0]] + [[i, v] for i in range(1, L) for v in (i - 1, i)]
cur = [0, 0]                                  # current and max depth of try_augment, measured from outside
def prof(frame, event, arg):
    if frame.f_code.co_name == 'try_augment':
        if event == 'call':
            cur[0] += 1; cur[1] = max(cur[1], cur[0])
        elif event == 'return':
            cur[0] -= 1
sys.setprofile(prof); res = kuhn(L, L, deep); sys.setprofile(None)
print('300 x 300 deep case:', res, 'max recursion depth', cur[1])
assert res == [300, True] and cur[1] <= 300 < sys.getrecursionlimit()
print('first example:', kuhn(3, 3, [[0, 0], [0, 1], [1, 0], [2, 0]]))
```

**Output (my run):**
```
examples ok
500 random small graphs match the bitmask oracle
greedy gives 1 Kuhn gives 2
300 x 300 deep case: [300, True] max recursion depth 300
first example: [2, False]
```

**Edge cases:**
- No edges: size 0, saturated False (L >= 1).
- Repeated edges: harmless, `seen` handles them.
- More left nodes than right nodes: saturated must be False.
- A left node with no neighbours: stays unmatched, and `saturated` is False.
- Maximum size L = R = 300: recursion depth is at most 300, far below 1000.

**Follow-ups:**
- *Why reset `seen` per left node?* A right node that failed in one attempt may succeed after the matching changes in a later attempt.
- *When do I need Hopcroft-Karp?* When L, E are large: it finds many shortest augmenting paths per phase, O(E sqrt V). Kuhn is O(V E).
- *Is there a minimum cover link?* Konig's theorem: in a bipartite graph the maximum matching size equals the minimum vertex cover size. Mention it by name only.

**Common mistakes:**
- Sharing one `seen` across all left nodes (misses augmenting paths).
- Matching greedily and stopping, believing it is maximum.
- Forgetting to assign `match_r[v] = u` when the recursive re-match succeeds.
- Treating repeated edges as extra capacity.
- Reporting `saturated` by comparing with R instead of L.

### Q44 ⭐ 🔴 Segment tree with lazy propagation: range add and range sum. Implement class `RangeAddSum(nums)` (1 <= len <= 10^5) with `add(l, r, v)` (add v, |v| <= 10^9, to every element of nums[l..r], both ends included; returns None) and `sum(l, r)` (the sum of nums[l..r], both ends included). Use a top-down tree where node o covers [lo, hi] and stores `sm[o]` (the true sum of its range) and `lz[o]` (an addition promised to both children but not yet pushed down): when a query or update only partly overlaps a node, `push` the pending value down first (children's sums grow by value * length and their lazy tags by value), recurse, then recompute `sm[o]` from the children. Both operations O(log n), memory O(4n). State the invariant (`sm[o]` is always correct for node o itself; only the children may be stale), and that forgetting to push down before recursing, or using `v` instead of `v * length`, are the classic bugs. Segment-tree recursion depth is about log2(n) (under 20 here), far below CPython's default recursion limit of 1000, so recursion is fine. A shorter alternative for sum-only is two Fenwick trees; the difference-array version for offline updates is Part 13 Q4. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[1, 2, 3, 4, 5]], ops=[['sum', [0, 4]], ['add', [1, 3, 10]], ['sum', [0, 4]], ['sum', [2, 2]], ['add', [0, 4, -1]], ['sum', [0, 1]], ['sum', [3, 4]]] -> [15, null, 45, 13, null, 11, 17].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)
**Pattern:** Segment tree with lazy propagation: range add and range sum, both O(log n).

**Say this first (1 line):** "Each node stores the true sum of its range plus a lazy add it owes its children; I push the lazy value down before going deeper, and a range add of v changes a node's sum by v times its length."

**Brute force:** Plain list. `add` loops over l..r, `sum` slices and adds: O(n) per operation, O(n * q) overall. Fine as the oracle, too slow for 10^5 elements and 10^5 operations.

**Optimal:**
- Node o covers [lo, hi]. `sm[o]` is always the correct sum for o itself. `lz[o]` is an addition already counted in `sm[o]` but not yet pushed to the children, so the children may be stale.
- `_apply(o, v)`: `sm[o] += v * length` and `lz[o] += v`.
- `add(l, r, v)`: if the node is fully inside, apply and stop; if it only partly overlaps, push the pending value down, recurse into both children, then recompute `sm[o] = sm[left] + sm[right]`.
- `sum(l, r)`: same shape; a fully covered node returns `sm[o]`; a partial one pushes down first, then adds the children's answers.
- Push-down order matters: if I recurse before pushing, the children are stale and the children's totals mix old and new values.
- Operation costs: build O(n); `add` O(log n); `sum` O(log n). Memory O(4n) for two arrays. A query touches at most about 4 nodes per level.
- Recursion depth is about log2(n), under 20 for n = 10^5, so recursion is fine.
- Alternative for sum-only: two Fenwick trees (range update, range query). For offline updates a difference array is enough (Part 13 Q4).
- Thread-safety is a concept only here: every operation mutates shared arrays during push-down, even `sum`, so concurrent use needs a lock (or a read-write lock that treats `sum` as a writer).

**Complexity:** Build O(n) time. `add` and `sum` O(log n) time each. Space O(4n). Values grow to 10^5 * 10^9 * (number of adds), still fine for Python ints.

**Dry run:** nums = [1, 2, 3, 4, 5], example ops.
- `sum(0,4)`: the root is fully covered, so 15.
- `add(1,3,10)`: the root splits into [0,2] and [3,4]. In [0,2], [2,2] is fully covered (3 -> 13) and [0,1] splits, with [1,1] becoming 12; recomputing upward gives [0,1] = 13 and [0,2] = 26. In [3,4], [3,3] becomes 14, so [3,4] = 19. Root = 45.
- `sum(0,4)` is 45 and `sum(2,2)` is 13.
- `add(0,4,-1)`: the root is fully covered, so sm = 45 - 5 = 40 and lz[root] = -1 (not pushed).
- `sum(0,1)`: the root is partial, so push: [0,2] becomes 23 (lz -1), [3,4] becomes 17 (lz -1). Then [0,2] pushes: [0,1] becomes 11, [2,2] becomes 12. [0,1] is fully covered: 11.
- `sum(3,4)` reads [3,4] = 17. Results: [15, None, 45, 13, None, 11, 17].

**Code:**
```python
import random
random.seed(44)

class RangeAddSum:
    def __init__(self, nums):
        self.n = len(nums)
        self.sm = [0] * (4 * self.n)          # sm[o]: TRUE sum of node o's range
        self.lz = [0] * (4 * self.n)          # lz[o]: add promised to both children, not yet pushed
        self._build(1, 0, self.n - 1, nums)

    def _build(self, o, lo, hi, a):
        if lo == hi:
            self.sm[o] = a[lo]; return
        mid = (lo + hi) // 2
        self._build(2 * o, lo, mid, a); self._build(2 * o + 1, mid + 1, hi, a)
        self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]

    def _apply(self, o, lo, hi, v):           # v * LENGTH, not v
        self.sm[o] += v * (hi - lo + 1); self.lz[o] += v

    def _push(self, o, lo, hi):
        if self.lz[o]:
            mid = (lo + hi) // 2
            self._apply(2 * o, lo, mid, self.lz[o])
            self._apply(2 * o + 1, mid + 1, hi, self.lz[o])
            self.lz[o] = 0

    def _add(self, o, lo, hi, l, r, v):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self._apply(o, lo, hi, v); return
        self._push(o, lo, hi)                 # push BEFORE recursing
        mid = (lo + hi) // 2
        self._add(2 * o, lo, mid, l, r, v); self._add(2 * o + 1, mid + 1, hi, l, r, v)
        self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]

    def _sum(self, o, lo, hi, l, r):
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.sm[o]
        self._push(o, lo, hi)
        mid = (lo + hi) // 2
        return self._sum(2 * o, lo, mid, l, r) + self._sum(2 * o + 1, mid + 1, hi, l, r)

    def add(self, l, r, v):
        self._add(1, 0, self.n - 1, l, r, v)

    def sum(self, l, r):
        return self._sum(1, 0, self.n - 1, l, r)

class Naive:
    def __init__(self, nums): self.a = list(nums)
    def add(self, l, r, v):
        for i in range(l, r + 1): self.a[i] += v
    def sum(self, l, r): return sum(self.a[l:r + 1])

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ex_ops = [['sum', [0, 4]], ['add', [1, 3, 10]], ['sum', [0, 4]], ['sum', [2, 2]], ['add', [0, 4, -1]], ['sum', [0, 1]], ['sum', [3, 4]]]
got = run(RangeAddSum, [[1, 2, 3, 4, 5]], ex_ops)
assert got == [15, None, 45, 13, None, 11, 17], got
print('example ->', got)

for _ in range(500):
    n = random.randint(1, 9)
    init = [[random.randint(-5, 5) for _ in range(n)]]
    ops = []
    for _ in range(random.randint(0, 30)):
        l = random.randrange(n); r = random.randrange(l, n)
        ops.append(['add', [l, r, random.randint(-9, 9)]] if random.random() < .5 else ['sum', [l, r]])
    assert run(RangeAddSum, init, ops) == run(Naive, init, ops), (init, ops)
print('500 random operation sequences match the naive reference')

assert run(RangeAddSum, [[7]], [['sum', [0, 0]], ['add', [0, 0, -7]], ['sum', [0, 0]]]) == [7, None, 0]   # n = 1
big = 10**9
assert run(RangeAddSum, [[0] * 3], [['add', [0, 2, big]], ['add', [0, 2, big]], ['sum', [0, 2]]])[-1] == 6 * big
# the classic bug: using v instead of v * length
class Bug(RangeAddSum):
    def _apply(self, o, lo, hi, v): self.sm[o] += v; self.lz[o] += v
bad = run(Bug, [[1, 2, 3, 4, 5]], ex_ops)
print('bug (v instead of v*length) gives', bad)
assert bad != got

n = 10**5
obj = RangeAddSum([0] * n)
for i in range(0, n, 50): obj.add(i, n - 1, 1)
assert obj.sum(0, n - 1) == sum(n - i for i in range(0, n, 50))
print('n = 10^5 build + 2000 range adds ok')
```

**Output (my run):**
```
example -> [15, None, 45, 13, None, 11, 17]
500 random operation sequences match the naive reference
bug (v instead of v*length) gives [15, None, 45, 13, None, 12, 18]
n = 10^5 build + 2000 range adds ok
```

**Edge cases:**
- n = 1: the tree is one leaf; every range is [0, 0].
- Single-element ranges l == r.
- Negative v and large |v| up to 10^9: Python ints do not overflow.
- A whole-array update stays at the root (O(1)).
- Repeated adds on the same range accumulate in `lz` without descending.

**Follow-ups:**
- *Why not push in `sum` as well?* You could keep tags and add `lz * overlap` on the way back instead (no push); both work, but then the invariant changes, so choose one and keep it consistent.
- *Range assign instead of add?* Needs a different tag (an assigned value plus a "has tag" flag) and the assign must override pending adds.
- *Range min or max?* Store `mx[o]` with lazy add: `mx[o] = max(children) + lz[o]` (used in Q50).

**Common mistakes:**
- Adding `v` instead of `v * (hi - lo + 1)` to the sum (the output shows the wrong answers).
- Recursing before pushing down.
- Not recomputing `sm[o]` from the children after the recursive calls.
- Using size 2n instead of 4n for the arrays.
- Off-by-one in the half-open versus closed convention (this class is closed on both ends).

### Q45 ⭐ 🔴 Two-dimensional Fenwick tree. Implement class `NumMatrix2D(matrix)` (m x n with 1 <= m, n <= 200) with `update(r, c, v)` (set matrix[r][c] = v; returns None) and `sumRegion(r1, c1, r2, c2)` (the sum of the rectangle with corners (r1, c1) and (r2, c2), both included). Keep a 2D tree `t` of size (m + 1) x (n + 1): an update adds the DELTA (new value minus the stored old value) at every (i, j) with the loops `i += i & -i` over rows and `j += j & -j` over columns, a prefix query P(r, c) sums with `i -= i & -i`, `j -= j & -j`, and a region is P(r2+1, c2+1) - P(r1, c2+1) - P(r2+1, c1) + P(r1, c1) (inclusion-exclusion). Both operations O(log m * log n); the build can simply call `update` for every cell (O(m n log m log n)). This is the Fenwick answer promised in Part 13 Q40 (row prefix sums there cost O(m) per query). Say when a segment tree of segment trees or an offline method is preferred (range updates, memory). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]], ops=[['sumRegion', [0, 0, 2, 3]], ['sumRegion', [1, 1, 2, 2]], ['update', [1, 2, 10]], ['sumRegion', [1, 1, 2, 2]], ['sumRegion', [1, 2, 1, 2]]] -> [28, 11, null, 18, 10].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)
**Pattern:** Two-dimensional Fenwick (binary indexed) tree: point update, rectangle sum, O(log m * log n) each.

**Say this first (1 line):** "A Fenwick tree inside a Fenwick tree: update walks `i += i & -i` over rows and `j += j & -j` over columns adding a delta, prefix queries walk down with `-=`, and a rectangle is four prefixes by inclusion-exclusion."

**Brute force:** Rescan the rectangle on every query: O(m * n) per query; or keep row prefix sums (Part 13 Q40): O(m) per query, O(n) per update. Fine as the oracle.

**Optimal:**
- Tree `t` is (m + 1) x (n + 1), 1-indexed. Keep a copy `a` of current values so that `update(r, c, v)` can compute `delta = v - a[r][c]`.
- Update: for `i = r + 1` upward by `i += i & -i`, for `j = c + 1` upward by `j += j & -j`, add the delta to `t[i][j]`.
- `_pre(r, c)` sums the rectangle with rows < r and columns < c by walking down with `i -= i & -i` and `j -= j & -j`.
- Region: `P(r2+1, c2+1) - P(r1, c2+1) - P(r2+1, c1) + P(r1, c1)`; the last term puts back the corner that was subtracted twice.
- Build: call `update` per cell: O(m n log m log n). With m, n <= 200 that is about 40,000 * 64 steps at worst, instant.
- Costs per operation: `update` O(log m * log n); `sumRegion` O(log m * log n) (four prefix queries); memory O(m n) for the tree and O(m n) for the copy.
- When to prefer something else: range updates or range min/max need a segment tree of segment trees or a 2D lazy scheme; an offline workload may use sorting plus a 1D Fenwick; memory-sparse huge grids need coordinate compression.
- Thread-safety as a concept: updates touch many cells, so a reader could see a half-applied update. A single lock around both methods is the simple answer.

**Complexity:** Time O(log m * log n) per operation, O(m n log m log n) to build. Space O(m n).

**Dry run:** matrix [[3,0,1,4],[5,6,3,2],[1,2,0,1]].
- `sumRegion(0,0,2,3)`: every cell: 3+0+1+4+5+6+3+2+1+2+0+1 = 28.
- `sumRegion(1,1,2,2)` = P(3,3) - P(1,3) - P(3,1) + P(1,1) = 21 - 4 - 9 + 3 = 11 (the cells 6, 3, 2, 0).
- `update(1,2,10)`: old value 3, delta 7. Row positions visited: 2 (then 4 > 3 stops). Column positions: 3, 4 (then 8 > 4 stops). So t[2][3] and t[2][4] gain 7.
- `sumRegion(1,1,2,2)` is now 6 + 10 + 2 + 0 = 18; `sumRegion(1,2,1,2)` is the single cell 10. Results: [28, 11, None, 18, 10].

**Code:**
```python
import random
random.seed(45)

class NumMatrix2D:
    def __init__(self, matrix):
        self.m = len(matrix); self.n = len(matrix[0])
        self.a = [[0] * self.n for _ in range(self.m)]            # current values (for the delta)
        self.t = [[0] * (self.n + 1) for _ in range(self.m + 1)]  # 1-indexed tree
        for i in range(self.m):
            for j in range(self.n):
                self.update(i, j, matrix[i][j])

    def update(self, r, c, v):
        d = v - self.a[r][c]
        self.a[r][c] = v
        i = r + 1
        while i <= self.m:
            j = c + 1
            while j <= self.n:
                self.t[i][j] += d
                j += j & -j
            i += i & -i

    def _pre(self, r, c):                     # sum of rows < r and columns < c
        s = 0; i = r
        while i > 0:
            j = c
            while j > 0:
                s += self.t[i][j]
                j -= j & -j
            i -= i & -i
        return s

    def sumRegion(self, r1, c1, r2, c2):
        return (self._pre(r2 + 1, c2 + 1) - self._pre(r1, c2 + 1)
                - self._pre(r2 + 1, c1) + self._pre(r1, c1))

class Naive:
    def __init__(self, matrix): self.a = [list(r) for r in matrix]
    def update(self, r, c, v): self.a[r][c] = v
    def sumRegion(self, r1, c1, r2, c2):
        return sum(self.a[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

init = [[[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]]
ops = [['sumRegion', [0, 0, 2, 3]], ['sumRegion', [1, 1, 2, 2]], ['update', [1, 2, 10]], ['sumRegion', [1, 1, 2, 2]], ['sumRegion', [1, 2, 1, 2]]]
got = run(NumMatrix2D, init, ops)
assert got == [28, 11, None, 18, 10], got
print('example ->', got)

for _ in range(400):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    ops = []
    for _ in range(random.randint(0, 25)):
        if random.random() < .4:
            ops.append(['update', [random.randrange(m), random.randrange(n), random.randint(-9, 9)]])
        else:
            r1 = random.randrange(m); r2 = random.randrange(r1, m); c1 = random.randrange(n); c2 = random.randrange(c1, n)
            ops.append(['sumRegion', [r1, c1, r2, c2]])
    assert run(NumMatrix2D, [mat], ops) == run(Naive, [mat], ops), (mat, ops)
print('400 random operation sequences match the naive reference')

assert run(NumMatrix2D, [[[5]]], [['sumRegion', [0, 0, 0, 0]], ['update', [0, 0, -2]], ['sumRegion', [0, 0, 0, 0]]]) == [5, None, -2]
assert run(NumMatrix2D, [[[1, 2, 3]]], [['sumRegion', [0, 1, 0, 2]]]) == [5]     # single row
assert run(NumMatrix2D, [[[1], [2], [3]]], [['sumRegion', [0, 0, 2, 0]]]) == [6]  # single column
# update stores the DELTA: setting a cell to its current value changes nothing
assert run(NumMatrix2D, [[[4, 4], [4, 4]]], [['update', [1, 1, 4]], ['sumRegion', [0, 0, 1, 1]]]) == [None, 16]
t = NumMatrix2D([[1] * 200 for _ in range(200)])
assert t.sumRegion(0, 0, 199, 199) == 40000
t.update(199, 199, 101)
assert t.sumRegion(0, 0, 199, 199) == 40100 and t.sumRegion(199, 199, 199, 199) == 101
print('200 x 200 ok')
```

**Output (my run):**
```
example -> [28, 11, None, 18, 10]
400 random operation sequences match the naive reference
200 x 200 ok
```

**Edge cases:**
- 1 x 1 matrix; a single row or a single column.
- `update` to the same value: delta 0, no change.
- A region equal to the whole matrix: P(m, n) with the three other terms zero.
- Negative values and negative updates: fine, the tree stores signed deltas.
- Rectangle corners given with r1 <= r2 and c1 <= c2 (the prompt guarantees this).

**Follow-ups:**
- *Why store the delta and not the value?* Every tree cell holds a partial sum; adding the new value would double count what is already there.
- *Does 2D get cheaper with a 1D tree per row?* Each query then costs O(m log n) and each update O(log n); the 2D tree balances both at O(log m * log n).
- *Part 13 Q40 asked the row-prefix version; what is the trade?* That one is O(m) query and O(n) update; this is the Fenwick answer promised there.

**Common mistakes:**
- Forgetting the +1 shift between 0-indexed cells and the 1-indexed tree.
- Mixing up the inclusion-exclusion signs, or using r2 and c2 without +1.
- Adding `v` instead of the delta.
- Loop bound `<= m` and `<= n` written as `<` (drops the last row or column).
- Forgetting to store the new value back into `a`.

### Q46 ⭐ 🔴 Count of smaller numbers after self. `nums` has 0 <= len <= 10^5 integers (duplicates allowed, |value| <= 10^9). Return a list `res` where res[i] is the number of elements to the RIGHT of position i that are STRICTLY smaller than nums[i]. Compress the values to ranks (Q17), scan from the right, and for each element query the Fenwick prefix count of ranks smaller than its own (rank - 1) before inserting its rank; O(n log n). Explain the scan direction (right to left, so the tree holds exactly the elements to the right) and why the merge-sort alternative has to carry the original indices through the merge (compare Part 13 Q17 and Part 13 Q47 for merge-sort counting). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) double loop on small inputs. Example: nums=[5, 2, 6, 1] -> [2, 1, 1, 0]; nums=[2, 2, 2] -> [0, 0, 0]; nums=[] -> [].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)
**Pattern:** Fenwick tree over compressed ranks, scanning right to left (counting inversions per element).

**Say this first (1 line):** "I rank-compress the values, walk from the right, and before inserting each element's rank I ask the Fenwick tree how many ranks smaller than mine it already holds; that is exactly the count of smaller numbers to my right."

**Brute force:** For each i, loop over j > i and count `nums[j] < nums[i]`: O(n^2). At 10^5 elements that is 5 * 10^9 comparisons.

**Optimal:**
- Compress: sorted distinct values get ranks 1..k (equal values share a rank). Compression (Q17) keeps the tree at size k instead of 2 * 10^9.
- Scan i from n-1 down to 0. The tree currently holds exactly `nums[i+1:]`. `res[i] = prefix(rank - 1)` counts ranks strictly less than mine; then add 1 at my rank.
- Strictness: query `rank - 1`, never `rank`, so duplicates are not counted (the [2, 2, 2] example gives zeros).
- Why right to left: scanning left to right with the same query counts smaller elements on the LEFT (the output shows the different answer). 
- Merge-sort alternative: also O(n log n), but sorting moves elements, so you must carry the original indices through the merge and add to `res[original index]`, counting during the merge when a right-half element is placed before a left-half element (compare Part 13 Q17 and Part 13 Q47).

**Complexity:** Time O(n log n): sorting the distinct values, then one Fenwick query and one update per element, each O(log k). Space O(n) for ranks, tree and result.

**Dry run:** nums = [5, 2, 6, 1]. Sorted distinct [1, 2, 5, 6], ranks 1 -> 1, 2 -> 2, 5 -> 3, 6 -> 4.
- i=3, value 1 (rank 1): prefix(0) = 0, insert rank 1. res[3] = 0.
- i=2, value 6 (rank 4): prefix(3) counts rank 1 -> 1, insert rank 4. res[2] = 1.
- i=1, value 2 (rank 2): prefix(1) = 1, insert rank 2. res[1] = 1.
- i=0, value 5 (rank 3): prefix(2) counts ranks 1 and 2 -> 2. res[0] = 2.
- Result [2, 1, 1, 0].

**Code:**
```python
import random
random.seed(46)

def count_smaller(nums):
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}      # compress to 1..k
    t = [0] * (len(ranks) + 1)
    def add(i):
        while i < len(t):
            t[i] += 1; i += i & -i
    def pre(i):
        s = 0
        while i > 0:
            s += t[i]; i -= i & -i
        return s
    res = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):        # right to left: the tree holds exactly nums[i+1:]
        res[i] = pre(ranks[nums[i]] - 1)          # strictly smaller ranks only
        add(ranks[nums[i]])
    return res

def brute(nums):
    return [sum(1 for j in range(i + 1, len(nums)) if nums[j] < nums[i]) for i in range(len(nums))]

assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
assert count_smaller([2, 2, 2]) == [0, 0, 0]
assert count_smaller([]) == []
print('examples ok')

for _ in range(600):
    nums = [random.randint(-4, 4) for _ in range(random.randint(0, 12))]
    assert count_smaller(nums) == brute(nums), nums
print('600 random arrays match the O(n^2) double loop')

assert count_smaller([7]) == [0]
assert count_smaller([3, 2, 1]) == [2, 1, 0]                 # descending
assert count_smaller([1, 2, 3]) == [0, 0, 0]                 # ascending
assert count_smaller([-10**9, 10**9, -10**9]) == [0, 1, 0]   # extremes, duplicates
# direction matters: scanning left to right and using the same query counts elements to the LEFT instead
def left_count(nums):
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}; t = [0] * (len(ranks) + 1); out = []
    for v in nums:
        i = ranks[v] - 1; s = 0
        while i > 0: s += t[i]; i -= i & -i
        out.append(s); i = ranks[v]
        while i < len(t): t[i] += 1; i += i & -i
    return out
print('left-to-right scan gives', left_count([5, 2, 6, 1]), 'not', count_smaller([5, 2, 6, 1]))
assert left_count([5, 2, 6, 1]) != [2, 1, 1, 0]
nums = [random.randint(-10**9, 10**9) for _ in range(10**5)]
r = count_smaller(nums); assert len(r) == 10**5 and all(0 <= x < 10**5 for x in r)
print('n = 10^5 ok')
print('first example:', count_smaller([5, 2, 6, 1]))
```

**Output (my run):**
```
examples ok
600 random arrays match the O(n^2) double loop
left-to-right scan gives [0, 0, 2, 0] not [2, 1, 1, 0]
n = 10^5 ok
first example: [2, 1, 1, 0]
```

**Edge cases:**
- Empty list: return [] (the tree has size 1 and is never touched).
- One element: [0].
- All equal: all zeros, since smaller is strict.
- Strictly descending: [n-1, ..., 0]; ascending: all zeros.
- Values up to +-10^9: compression makes the range irrelevant, and negatives need no special care.

**Follow-ups:**
- *How would "smaller or equal" change it?* Query `prefix(rank)` instead of `prefix(rank - 1)`.
- *Can I do it without compressing?* If values are bounded and small, index the tree by value directly; otherwise use a dynamic structure or compress.
- *Related problems?* Inversion counts, reverse pairs (Set C) and the merge-sort counting questions Part 13 Q17 and Part 13 Q47 are the same idea; Q25 here also uses a Fenwick tree.

**Common mistakes:**
- Scanning left to right and answering a different question.
- Querying `rank` (counts equal values) instead of `rank - 1`.
- Using the raw values as tree indices, which fails for negatives and for 10^9.
- A 0-indexed Fenwick tree (index 0 loops forever with `i & -i`).
- Inserting before querying, so every element counts itself.

### Q47 ⭐ 🔴 [Set A, Q5 of 5, 12 min, 30 pts] Delayed job scheduler with cancellation. Implement class `Scheduler(clock)` with `submit(job_id, delay, priority)` (the job becomes ready at time now + delay, delay >= 0; smaller `priority` numbers are more urgent; a job id is never submitted while a job with the same id is still pending, but an id may be reused after it was polled or cancelled; returns None), `cancel(job_id)` (True when a pending job was removed, else False) and `poll(limit)` which removes and returns, in order, up to `limit` pending jobs that are ready (ready time <= now). Order: smaller ready time first, then smaller priority, then earlier submission. Jobs that are not yet ready are never returned, and a poll with nothing ready returns []. Use a heap of (ready, priority, seq, job_id) and a dict job_id -> seq of live jobs: `cancel` deletes from the dict only (lazy deletion: Part 8 Q31) and `poll` discards heap entries whose seq no longer matches; tie keys follow Part 8 Q29. Submit O(log n), cancel O(1), poll O(k log n) amortised. Explain why the `seq` check (not just the id) is needed when an id is reused after cancel. The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[], ops=[[0, 'submit', ['a', 5, 2]], [0, 'submit', ['b', 5, 1]], [0, 'submit', ['c', 0, 9]], [0, 'poll', [5]], [4, 'poll', [5]], [5, 'cancel', ['b']], [5, 'poll', [1]], [5, 'submit', ['b', 0, 3]], [5, 'poll', [5]], [6, 'cancel', ['a']], [6, 'poll', [5]]] -> [null, null, null, ['c'], [], True, ['a'], null, ['b'], False, []].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Min-heap with lazy deletion for a delayed, prioritised job queue, driven by an injected clock.

**Say this first (1 line):** "Order is ready time, then priority, then submission order; I keep a heap of (ready, priority, seq, id) plus a dict id -> seq of live jobs, cancel only touches the dict, and poll throws away heap entries whose seq no longer matches."

**Brute force:** Keep a plain list of pending jobs. `poll` sorts the ready ones and takes `limit`; `cancel` filters the list. O(n log n) per poll and O(n) per cancel. That is my reference model for the random test.

**Optimal:**
- Rules, stated first: a job is ready when `ready <= now` (a job ready exactly now IS returned). Order: smaller ready time, then smaller priority number, then earlier submission (`seq`, a counter). Not-yet-ready jobs are never returned. Nothing ready gives `[]`.
- `submit` pushes `(now + delay, priority, seq, job_id)` and records `live[job_id] = seq`.
- `cancel` does `live.pop(job_id)`: True if the job was pending. The heap entry stays (lazy deletion, Part 8 Q31); tie keys follow Part 8 Q29.
- `poll(limit)`: while the heap top is ready and fewer than `limit` jobs are out, pop it; if `live.get(job_id) == seq` it is a real job, return it and delete it from `live`; otherwise it is stale and is silently discarded (stale entries do not use up the limit).
- Why `seq` and not just the id: cancel `a`, then submit `a` again with a later ready time. Two heap entries now carry the id `a`. An id-only check would let the OLD entry (ready earlier) return the NEW job too early; the output shows that failure. The `seq` check accepts only the entry of the current submission.
- Costs: `submit` O(log n); `cancel` O(1) (the stale entry is cleaned later, paid by the poll that meets it); `poll(k)` O(k log n) amortised, because each heap entry is popped at most once.
- Memory: cancelled entries linger until they reach the top. That is acceptable here; if cancels dominate, rebuild the heap when stale entries exceed half of it.
- Thread-safety as a concept only: `submit`, `cancel` and `poll` mutate the heap and the dict together, so a real system guards them with one lock or a single worker thread; polling workers would claim jobs under that lock.

**Complexity:** `submit` O(log n), `cancel` O(1), `poll` O(k log n) amortised over all calls; space O(n) including stale entries.

**Dry run:** the example.
- t=0: submit a (ready 5, prio 2, seq 1), b (ready 5, prio 1, seq 2), c (ready 0, prio 9, seq 3).
- t=0 `poll(5)`: top is c (ready 0 <= 0), returned. Next top is b (ready 5 > 0): stop. -> ['c'].
- t=4 `poll(5)`: top ready is 5 > 4 -> [].
- t=5 `cancel('b')`: removed from `live` -> True. `poll(1)`: top is b's entry (5, 1, 2): `live.get('b')` is None, so discard it; next is a (5, 2, 1), live matches -> ['a'], limit reached.
- t=5 `submit('b', 0, 3)` (seq 4, ready 5), `poll(5)` -> ['b'].
- t=6 `cancel('a')`: a was already polled -> False. `poll(5)` -> [].

**Code:**
```python
import heapq, random
random.seed(47)

class Scheduler:
    def __init__(self, clock):
        self.clock = clock
        self.heap = []                        # (ready, priority, seq, job_id)
        self.live = {}                        # job_id -> seq of the live submission
        self.seq = 0

    def submit(self, job_id, delay, priority):
        self.seq += 1
        self.live[job_id] = self.seq
        heapq.heappush(self.heap, (self.clock() + delay, priority, self.seq, job_id))

    def cancel(self, job_id):
        return self.live.pop(job_id, None) is not None     # lazy: the heap entry stays, poll skips it

    def poll(self, limit):
        now = self.clock(); out = []
        while self.heap and len(out) < limit and self.heap[0][0] <= now:
            ready, pr, seq, job_id = heapq.heappop(self.heap)
            if self.live.get(job_id) == seq:               # stale entries (cancelled / reused id) fail this test
                out.append(job_id); del self.live[job_id]
        return out

class Naive:
    def __init__(self, clock): self.clock = clock; self.jobs = []; self.seq = 0
    def submit(self, job_id, delay, priority):
        self.seq += 1; self.jobs.append((self.clock() + delay, priority, self.seq, job_id))
    def cancel(self, job_id):
        n = len(self.jobs); self.jobs = [j for j in self.jobs if j[3] != job_id]; return len(self.jobs) < n
    def poll(self, limit):
        now = self.clock(); ready = sorted(j for j in self.jobs if j[0] <= now)[:limit]
        for j in ready: self.jobs.remove(j)
        return [j[3] for j in ready]

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

def run(cls, ops):
    clk = Clock(); obj = cls(clk); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(obj, m)(*a))
    return out

ex = [[0, 'submit', ['a', 5, 2]], [0, 'submit', ['b', 5, 1]], [0, 'submit', ['c', 0, 9]], [0, 'poll', [5]], [4, 'poll', [5]],
      [5, 'cancel', ['b']], [5, 'poll', [1]], [5, 'submit', ['b', 0, 3]], [5, 'poll', [5]], [6, 'cancel', ['a']], [6, 'poll', [5]]]
got = run(Scheduler, ex)
assert got == [None, None, None, ['c'], [], True, ['a'], None, ['b'], False, []], got
print('example ->', got)

def gen_ops():                                # never submits an id that is still pending (checked with the naive model)
    clk = Clock(); probe = Naive(clk); pending = set(); ops = []; t = 0
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 3); clk.t = t; r = random.random()
        if r < .45:
            jid = 'j%d' % random.randint(1, 6)
            if jid in pending: continue
            a = [jid, random.randint(0, 5), random.randint(0, 3)]; probe.submit(*a); pending.add(jid); ops.append([t, 'submit', a])
        elif r < .7:
            a = ['j%d' % random.randint(1, 6)]
            if probe.cancel(*a): pending.discard(a[0])
            ops.append([t, 'cancel', a])
        else:
            a = [random.randint(1, 4)]
            for j in probe.poll(*a): pending.discard(j)
            ops.append([t, 'poll', a])
    return ops
for _ in range(500):
    ops = gen_ops()
    assert run(Scheduler, ops) == run(Naive, ops), ops
print('500 random sequences with an injected clock match the naive reference')

# ties: same ready time, then priority, then submission order; ready exactly at `now` is returned
tie = [[0, 'submit', ['x', 3, 1]], [0, 'submit', ['y', 3, 1]], [0, 'submit', ['z', 3, 0]], [3, 'poll', [10]]]
assert run(Scheduler, tie)[-1] == ['z', 'x', 'y']
assert run(Scheduler, [[0, 'poll', [3]], [0, 'cancel', ['q']], [0, 'submit', ['q', 1, 0]], [0, 'poll', [3]], [1, 'poll', [0]], [1, 'poll', [3]]]) == [[], False, None, [], [], ['q']]

# why seq, not just the id: cancel then resubmit the SAME id with a later ready time
class IdOnly(Scheduler):
    def poll(self, limit):
        now = self.clock(); out = []
        while self.heap and len(out) < limit and self.heap[0][0] <= now:
            ready, pr, seq, job_id = heapq.heappop(self.heap)
            if job_id in self.live: out.append(job_id); del self.live[job_id]
        return out
reuse = [[0, 'submit', ['a', 1, 0]], [0, 'cancel', ['a']], [0, 'submit', ['a', 9, 0]], [1, 'poll', [5]], [9, 'poll', [5]]]
print('seq check:', run(Scheduler, reuse)[-2:], ' id-only check:', run(IdOnly, reuse)[-2:])
assert run(Scheduler, reuse)[-2:] == [[], ['a']] and run(IdOnly, reuse)[-2:] == [['a'], []]
```

**Output (my run):**
```
example -> [None, None, None, ['c'], [], True, ['a'], None, ['b'], False, []]
500 random sequences with an injected clock match the naive reference
seq check: [[], ['a']]  id-only check: [['a'], []]
```

**Edge cases:**
- `poll(0)` returns [] without touching anything.
- `delay = 0`: ready immediately at the submit time.
- Ties on ready time and priority: the earlier submission goes first (the `seq` field also stops Python from comparing job ids).
- Cancel of an unknown or already polled id: False.
- Reusing an id after poll or cancel: allowed, handled by `seq`.
- Many cancelled jobs: stale entries are skipped without consuming `limit`.

**Follow-ups:**
- *What if cancels are frequent?* Count stale entries and rebuild the heap when they exceed the live ones, keeping memory O(live).
- *How would workers run this?* A worker loop calls `poll`, and when nothing is ready it sleeps until `heap[0][0] - now`; submit wakes it if the new job is earlier (a condition variable).
- *What if two schedulers share a store?* A real system needs a database or Redis sorted set with an atomic claim; that is system design, not this data-structure answer.
- *Scoring note (30 pts, split per the part header rubric):* 9 pts for stating the rules before coding (ready `<=` now, the three-key order, id reuse, empty poll); 9 pts for a correct solution that passes the example and a random operation-sequence check; 6 pts for complexity and the reason it holds (amortised poll, lazy cancel); 3 pts for the seeded edge cases (limit larger than ready jobs, cancel of unknown id, reuse after cancel); 3 pts for a crisp under-60-second summary. Partial: a correct sort-on-every-poll version with the rules stated earns about 18 to 20; missing the `seq` check loses most of the correctness points for id reuse.
- *How I would pace this (12 min):* 2 min stating rules and tie order, 2 min choosing heap plus dict, 5 min coding, 2 min tracing the example (especially the cancel-then-poll step), 1 min complexity and the lazy-deletion caveat.

**Common mistakes:**
- Checking only `job_id in live`, which breaks id reuse after a cancel.
- Reading time from the `time` module instead of the injected `clock()`.
- Counting stale pops against `limit`.
- Using `<` instead of `<=`, so a job ready exactly now is missed.
- Pushing without `seq` so equal keys compare job ids (or crash on mixed types).

### Q48 ⭐ 🔴 [Set B, Q5 of 5, 12 min, 30 pts] Fewest starting nodes to reach everything. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges`, a list of directed [u, v] pairs (0 <= len <= 2*10^5; repeats and self loops allowed). Choose the smallest set of start nodes so that every node is reachable from at least one chosen node. Return that smallest set as a sorted list, and when several smallest sets exist return the lexicographically smallest one (compare the sorted lists). Condense the graph with the strongly connected components of Q20: the answer needs exactly one node from every component that has NO incoming edge from another component (a source component), and the smallest node of each source component gives the lexicographically smallest set. Explain why a non-source component is never needed and why one node per source component is enough (Part 9 Q3 counts undirected components; here direction matters). O(n + m) with an iterative DFS. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an exhaustive oracle that tries all subsets in order of size and lexicographic order (n <= 8) on small inputs. Example: n=5, edges=[[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]] -> [0, 3]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> [0]; n=3, edges=[] -> [0, 1, 2].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Strongly connected components, then the condensation DAG: exactly one start per source component.

**Say this first (1 line):** "Condense the graph into SCCs; every component with no incoming edge from another component needs one start, every other component is reached for free, and the smallest node of each source component gives the lexicographically smallest answer."

**Brute force:** Try all subsets in order of size, then lexicographic order, BFS from each subset and stop at the first that reaches every node: O(2^n * (n + m)). Only for n <= 8, as the oracle.

**Optimal:**
- Compute SCCs with an iterative DFS (the Tarjan code of Q41 here; Kosaraju of Q20 works equally well). Directed reachability inside a component is mutual, so one start anywhere in a component reaches the whole component.
- A component with an incoming edge from another component is reachable from it, so a non-source component is never needed in a smallest set.
- A source component can only be reached by starting inside it, so one start per source component is required, and one start suffices. The minimum count is therefore the number of source components.
- Lexicographic tie-break: within a source component any node works; pick its smallest node. Sorting those picks gives the lexicographically smallest sorted list (a smaller pick in any component can only help).
- Mark `has_in[comp[v]] = True` for every edge u -> v with `comp[u] != comp[v]`; self loops and edges inside a component do not count. Part 9 Q3 counts undirected components; with directions, only source components count.

**Complexity:** Time O(n + m) (iterative Tarjan, one pass over the edges, one pass over the nodes); space O(n + m).

**Dry run:** n=5, edges 0->1, 1->0, 1->2, 3->2, 3->4.
- SCCs: {0, 1}, {2}, {3}, {4}.
- Edges that cross components: 1->2 and 3->2 give {2} an incoming edge; 3->4 gives {4} one. {0, 1} and {3} have none, so they are the sources.
- Smallest node of {0, 1} is 0, of {3} is 3. Answer [0, 3].

**Code:**
```python
import itertools, random
random.seed(48)

def min_starts(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n; stack = []; counter = 0; nc = 0
    for s in range(n):                        # iterative Tarjan, as in Q41
        if idx[s] != -1:
            continue
        idx[s] = low[s] = counter; counter += 1; stack.append(s); on[s] = True
        work = [(s, 0)]
        while work:
            u, i = work.pop()
            if i < len(g[u]):
                work.append((u, i + 1)); v = g[u][i]
                if idx[v] == -1:
                    idx[v] = low[v] = counter; counter += 1; stack.append(v); on[v] = True; work.append((v, 0))
                elif on[v]:
                    low[u] = min(low[u], idx[v])
            else:
                if low[u] == idx[u]:
                    while True:
                        w = stack.pop(); on[w] = False; comp[w] = nc
                        if w == u:
                            break
                    nc += 1
                if work:
                    p = work[-1][0]; low[p] = min(low[p], low[u])
    has_in = [False] * nc
    for u, v in edges:
        if comp[u] != comp[v]:
            has_in[comp[v]] = True            # this component receives an edge from another one
    smallest = [None] * nc
    for v in range(n):                        # ascending v: the first node seen is the component minimum
        if smallest[comp[v]] is None:
            smallest[comp[v]] = v
    return sorted(smallest[c] for c in range(nc) if not has_in[c])

def oracle(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    def covers(starts):
        seen = set(starts); q = list(starts)
        for u in q:
            for v in g[u]:
                if v not in seen: seen.add(v); q.append(v)
        return len(seen) == n
    for k in range(1, n + 1):                 # smaller sets first; combinations come out in lexicographic order
        for combo in itertools.combinations(range(n), k):
            if covers(combo): return list(combo)

assert min_starts(5, [[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]]) == [0, 3]
assert min_starts(3, [[0, 1], [1, 2], [2, 0]]) == [0]
assert min_starts(3, []) == [0, 1, 2]
print('examples ok')

for _ in range(800):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 14))]
    assert min_starts(n, edges) == oracle(n, edges), (n, edges)
print('800 random graphs match the exhaustive subset oracle')

assert min_starts(1, [[0, 0]]) == [0]
assert min_starts(4, [[3, 2], [2, 1], [1, 0]]) == [3]                    # path against the node order
assert min_starts(4, [[0, 1], [1, 0], [2, 3], [3, 2]]) == [0, 2]        # two cycles
assert min_starts(3, [[0, 2], [1, 2], [0, 2]]) == [0, 1]                 # repeated edges
N = 10**5
assert min_starts(N, [[i + 1, i] for i in range(N - 1)]) == [N - 1]
assert min_starts(N, [[i, (i + 1) % N] for i in range(N)]) == [0]
print('10^5 path and 10^5 cycle ok (iterative)')
print('first example:', min_starts(5, [[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]]))
```

**Output (my run):**
```
examples ok
800 random graphs match the exhaustive subset oracle
10^5 path and 10^5 cycle ok (iterative)
first example: [0, 3]
```

**Edge cases:**
- No edges: every node is its own source, answer is all nodes in order.
- One big cycle: one component, answer [0].
- Self loops and repeated edges: ignored for the source test.
- A path against the numbering (3 -> 2 -> 1 -> 0): only [3].
- Several cycles with no links between them: one pick each, the smallest node.
- n = 10^5: iterative, no recursion.

**Follow-ups:**
- *Could I use a simpler method than SCC?* You still need to know which nodes can reach each other; counting nodes with in-degree 0 is wrong when a cycle is a source.
- *What if I wanted the largest reach with k starts?* That is a different (harder) problem; with the condensation it becomes a set-cover style question.
- *Scoring note (30 pts, split per the part header rubric):* 9 pts for saying out loud that components matter, that a source component needs exactly one start, that non-source ones are free, and the lexicographic rule; 9 pts for a correct iterative SCC plus source marking that passes the example and a random check; 6 pts for O(n + m) and why; 3 pts for the seeded edge cases (no edges, one cycle, self loops, repeats); 3 pts for the under-60-second summary. Partial: a correct in-degree-0 solution that ignores cycles earns about 12 to 15 once the cycle counterexample is pointed out.
- *How I would pace this (12 min):* 2 min on the SCC insight and tie rule, 7 min coding the iterative SCC and the source test, 2 min on the example, 1 min complexity.

**Common mistakes:**
- Counting nodes of in-degree 0, which misses cycle components that are sources.
- Counting the edges inside a component as incoming.
- Choosing an arbitrary node per source component instead of the smallest.
- Recursive DFS, which crashes on long paths.
- Forgetting isolated nodes (each is its own source).

### Q49 ⭐ 🔴 [Set C, Q2 of 4, 11 min, 25 pts] Order statistics on a dynamic multiset with a Fenwick tree. Implement class `OrderStats(max_value)` (1 <= max_value <= 10^6) storing a multiset of integers in [0, max_value], with `insert(x)` (returns None), `remove(x)` (removes ONE copy; returns True when a copy existed, else False), `count_le(x)` (the number of stored elements <= x; 0 for negative x and the full size for x >= max_value) and `kth(k)` (the k-th smallest element counting duplicates, 1-based, or -1 when k < 1 or k > size). Keep a Fenwick tree over the values shifted by +1. `kth` uses binary descent on the tree: start with the largest power of two <= n as `step`, and for each step try `pos + step`; if `t[pos + step] < k`, move there and subtract that count from k; the answer is the final `pos` (the value, because indices are shifted by one). All operations O(log max_value). Explain why the descent beats a binary search over `count_le` (O(log n) instead of O(log^2 n)) and why this is the order-statistics trick behind 'median of a changing multiset' (compare Part 8 Q17). Fenwick basics: Q10. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[10], ops=[['insert', [5]], ['insert', [3]], ['insert', [5]], ['insert', [9]], ['count_le', [5]], ['kth', [1]], ['kth', [3]], ['kth', [4]], ['kth', [5]], ['remove', [5]], ['remove', [7]], ['kth', [3]], ['count_le', [-1]], ['count_le', [10]]] -> [null, null, null, null, 3, 3, 5, 9, -1, True, False, 9, 0, 3].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Fenwick tree for order statistics over a value domain: count of elements <= x, and k-th smallest by binary descent.

**Say this first (1 line):** "A Fenwick tree of counts indexed by value gives `count_le` as a prefix sum, and the k-th smallest by descending the tree's power-of-two steps, so everything is O(log max_value) with no binary search on top."

**Brute force:** Keep a sorted list with `bisect.insort`: insert and remove O(n) (list shifting), `count_le` O(log n) with `bisect`, `kth` O(1). The naive reference in the code uses this; it is fine at small sizes but insert is O(n) at 10^6 distinct values.

**Optimal:**
- Values 0..max_value are shifted by +1 into positions 1..n (n = max_value + 1), because a Fenwick tree is 1-indexed. `t` holds the counts; `cnt[x]` keeps exact copies so `remove` can answer True/False.
- `insert(x)`: `cnt[x] += 1`, size += 1, Fenwick add 1 at x + 1. `remove(x)`: if `cnt[x] == 0` return False, else the reverse; True.
- `count_le(x)`: 0 if x < 0; otherwise the prefix sum up to `min(x, max_value) + 1` (so x >= max_value gives the full size).
- `kth(k)`: -1 if k < 1 or k > size. Otherwise `pos = 0`, `step` = largest power of two <= n; for each `step` going down by halves: if `pos + step <= n` and `t[pos + step] < k`, move `pos += step` and `k -= t[pos]`. At the end `pos` is the number of positions whose cumulative count stays below k, so position `pos + 1` holds the k-th element, whose value is `pos` (shift by one).
- Why descent beats binary search on `count_le`: a binary search needs O(log n) steps each costing an O(log n) prefix query, O(log^2 n). The descent reads one tree cell per step, O(log n), because a Fenwick cell already stores a power-of-two block sum.
- This is the order-statistics trick behind 'median of a changing multiset' (compare Part 8 Q17): the median is `kth((size + 1) // 2)`. Fenwick basics: Q10.
- Duplicates are counts, so the k-th smallest counts duplicates naturally.
- Thread-safety as a concept only: each call reads and writes `t`, `cnt` and `size`; a lock around all four methods is the simple answer.

**Complexity:** `insert`, `remove`, `count_le`, `kth` are all O(log max_value) time. Space O(max_value) for `t` and `cnt` (about 2 * 10^6 ints at the limit).

**Dry run:** max_value=10, so n = 11 and the largest power of two <= 11 is 8. Insert 5, 3, 5, 9: counts 3:1, 5:2, 9:1, size 4.
- `count_le(5)` = 1 + 2 = 3.
- `kth(1)`: step 8: t[8] covers values 0..7 = 3, not < 1, stay. Step 4: t[4] covers values 0..3 = 1, not < 1. Step 2: t[2] = 0 < 1, so pos = 2. Step 1: t[3] (value 2) = 0 < 1, so pos = 3. Answer 3.
- `kth(3)`: t[8] = 3 is not < 3; step 4: t[4] = 1 < 3, so pos = 4, k = 2; step 2: t[6] = 2 is not < 2; step 1: t[5] = 0 < 2, so pos = 5. Answer 5.
- `kth(4)`: t[8] = 3 < 4, so pos = 8, k = 1; step 4 overshoots (12 > 11); step 2: t[10] = 1 is not < 1; step 1: t[9] = 0 < 1, so pos = 9. Answer 9. `kth(5)` = -1.
- `remove(5)` True, `remove(7)` False, `kth(3)` = 9, `count_le(-1)` = 0, `count_le(10)` = 3.

**Code:**
```python
import bisect, random
random.seed(49)

class OrderStats:
    def __init__(self, max_value):
        self.n = max_value + 1                # values 0..max_value live at tree positions 1..n
        self.t = [0] * (self.n + 1)
        self.cnt = [0] * self.n               # exact copy counts, so remove can answer True/False
        self.size = 0
        self.top = 1
        while self.top * 2 <= self.n:         # largest power of two <= n
            self.top *= 2

    def _add(self, i, d):
        while i <= self.n:
            self.t[i] += d; i += i & -i

    def insert(self, x):
        self.cnt[x] += 1; self.size += 1; self._add(x + 1, 1)

    def remove(self, x):
        if x < 0 or x >= self.n or self.cnt[x] == 0:
            return False
        self.cnt[x] -= 1; self.size -= 1; self._add(x + 1, -1)
        return True

    def count_le(self, x):
        if x < 0:
            return 0
        i = min(x, self.n - 1) + 1; s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i
        return s

    def kth(self, k):
        if k < 1 or k > self.size:
            return -1
        pos = 0; step = self.top
        while step:                           # binary descent: never overshoot the k-th element
            nxt = pos + step
            if nxt <= self.n and self.t[nxt] < k:
                pos = nxt; k -= self.t[nxt]
            step >>= 1
        return pos                            # position pos+1 holds the answer, i.e. the value pos

class Naive:
    def __init__(self, max_value): self.a = []
    def insert(self, x): bisect.insort(self.a, x)
    def remove(self, x):
        if x in self.a: self.a.remove(x); return True
        return False
    def count_le(self, x): return sum(1 for v in self.a if v <= x)
    def kth(self, k): return self.a[k - 1] if 1 <= k <= len(self.a) else -1

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ops = [['insert', [5]], ['insert', [3]], ['insert', [5]], ['insert', [9]], ['count_le', [5]], ['kth', [1]], ['kth', [3]], ['kth', [4]],
       ['kth', [5]], ['remove', [5]], ['remove', [7]], ['kth', [3]], ['count_le', [-1]], ['count_le', [10]]]
got = run(OrderStats, [10], ops)
assert got == [None, None, None, None, 3, 3, 5, 9, -1, True, False, 9, 0, 3], got
print('example ->', got)

for _ in range(500):
    mv = random.randint(1, 12)
    ops = []
    for _ in range(random.randint(0, 40)):
        r = random.random()
        if r < .3: ops.append(['insert', [random.randint(0, mv)]])
        elif r < .45: ops.append(['remove', [random.randint(0, mv)]])
        elif r < .7: ops.append(['count_le', [random.randint(-2, mv + 2)]])
        else: ops.append(['kth', [random.randint(-1, 12)]])
    assert run(OrderStats, [mv], ops) == run(Naive, [mv], ops), (mv, ops)
print('500 random operation sequences match the naive reference (max_value 1..12)')

assert run(OrderStats, [1], [['kth', [1]], ['insert', [0]], ['kth', [1]], ['remove', [0]], ['remove', [0]], ['count_le', [5]]]) == [-1, None, 0, True, False, 0]
assert run(OrderStats, [8], [['insert', [8]], ['insert', [0]], ['kth', [2]], ['count_le', [100]]]) == [None, None, 8, 2]   # n = 9, not a power of two
M = 10**6
o = OrderStats(M)
vals = [random.randint(0, M) for _ in range(20000)]
for v in vals: o.insert(v)
s = sorted(vals)
assert all(o.kth(k) == s[k - 1] for k in (1, 2, 777, 10000, 20000)) and o.count_le(M) == 20000
print('max_value = 10^6 with 20000 inserts ok')
```

**Output (my run):**
```
example -> [None, None, None, None, 3, 3, 5, 9, -1, True, False, 9, 0, 3]
500 random operation sequences match the naive reference (max_value 1..12)
max_value = 10^6 with 20000 inserts ok
```

**Edge cases:**
- Empty structure: `kth` returns -1, `count_le` returns 0.
- `max_value = 1` or a value domain whose n is not a power of two (the `pos + step <= n` guard).
- Values 0 and max_value (the shifted positions 1 and n).
- `count_le` with x below 0 or above max_value.
- `remove` of a value never inserted, or removed twice: False and no change.
- k = 0 or negative: -1.

**Follow-ups:**
- *What if values are not small integers?* Compress offline (Q17) if all values are known; otherwise use a balanced tree or a sorted-list structure.
- *How do I get the median?* `kth((size + 1) // 2)` (lower median); for an even size average two `kth` calls.
- *Why keep `cnt` besides the tree?* To know whether a removal is legal in O(1) (the tree alone would need a point query).
- *Scoring note (25 pts, split per the part header rubric):* about 7.5 pts for stating the rules (shift by one, duplicates counted, `kth` bounds, `count_le` clamps); 7.5 pts for a correct solution that passes the example and a random operation-sequence check; 5 pts for complexity and the reason the descent is O(log n); 2.5 pts for edge cases (empty, out-of-range x, double remove); 2.5 pts for the crisp summary. Partial: a `bisect.insort` list with correct rules earns roughly 15 of 25; a Fenwick tree with binary search over `count_le` earns about 20.
- *How I would pace this (11 min):* 2 min on rules and the +1 shift, 5 min coding the tree and `kth`, 2 min tracing one `kth`, 2 min on complexity and the descent argument.

**Common mistakes:**
- Forgetting the +1 shift, so value 0 loops forever (`0 & -0 = 0`).
- Not guarding `pos + step <= n` in the descent.
- Returning `pos + 1` instead of `pos` from `kth`.
- Letting `remove` go negative when the value is absent.
- Using `max_value` instead of `max_value + 1` for the tree size.

### Q50 ⭐ 🔴 [Set C, Q4 of 4, 13 min, 30 pts] Maximum overlap after every booking (My Calendar III). `bookings` is a list of up to 400 [start, end) pairs with 0 <= start < end <= 10^9, HALF-OPEN: two bookings that only touch (one ends exactly where the next starts) do not overlap. Return a list with one integer per booking: after adding bookings[0..i], the largest number of bookings that cover a single moment. Offline solution: compress all endpoints (Q17) into elementary cells [xs[k], xs[k+1]), then use a segment tree with lazy range add and global maximum (Q44; the root max is the answer; here `mx[o] = max(children) + lazy[o]` needs no push-down). O(n log n) overall. Compare with the difference-array idea of Part 13 Q4 (which needs small coordinates) and with the sweep of Part 8 Q7 (one answer for the whole set, not after every insert). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that recomputes the maximum overlap from scratch after every booking on small inputs. Example: bookings=[[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]] -> [1, 1, 2, 3, 3, 3]; bookings=[[0, 5], [5, 10], [0, 10]] -> [1, 1, 2].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Coordinate compression plus a segment tree with lazy range add and a global maximum (My Calendar III, offline).

**Say this first (1 line):** "Bookings are half-open, so I compress all endpoints into elementary cells [xs[k], xs[k+1]) and add one to the cells a booking covers; the answer after each booking is the maximum over all cells, which the tree keeps at the root."

**Brute force:** After every booking, recompute the maximum overlap from scratch: for each endpoint of the bookings so far, count how many bookings contain it. O(n^2) per booking, O(n^3) total; at n = 400 that is already heavy, but it is a clean oracle.

**Optimal:**
- Half-open rule: [s, e) covers moment x when `s <= x < e`, so bookings that only touch (one ends where the next starts) do not overlap. In cells, booking [s, e) covers exactly the cells with indices `pos[s] .. pos[e] - 1`.
- Compress the sorted distinct endpoints `xs`; there are `m = len(xs) - 1` cells. Maximum overlap always occurs on a whole cell, since coverage only changes at endpoints.
- Segment tree over the m cells with lazy add and no push-down: `mx[o]` is the maximum inside o INCLUDING the tag stored at o, `lz[o]` is the add applied to the whole of o. A fully covered node does `mx += 1; lz += 1`. A partly covered node recurses and sets `mx[o] = max(mx[left], mx[right]) + lz[o]`. The root's `mx` is the answer after each booking (Q44 has the push-down version).
- Offline is fine because all bookings are known up front (the list is given). For an online version you would need a dynamic or sorted-list structure (a sorted dictionary of boundary counts).
- Compare: the difference-array idea of Part 13 Q4 needs small coordinates (here they reach 10^9, hence compression); the sweep of Part 8 Q7 gives one answer for the whole set, not an answer after every insert.

**Complexity:** Sorting the endpoints O(n log n); each booking's range add is O(log n); total O(n log n) for n <= 400. Space O(n) for `xs`, the map, and 4m for the tree arrays. Recursion depth about log2(800) < 10.

**Dry run:** bookings [10,20), [50,60), [10,40), [5,15), [5,10), [25,55).
- Endpoints sorted: 5, 10, 15, 20, 25, 40, 50, 55, 60 give 8 cells: 0 = [5,10), 1 = [10,15), 2 = [15,20), 3 = [20,25), 4 = [25,40), 5 = [40,50), 6 = [50,55), 7 = [55,60).
- [10,20) covers cells 1..2: max 1. [50,60) covers cells 6..7: max 1.
- [10,40) covers cells 1..4: cells 1 and 2 reach 2: max 2.
- [5,15) covers cells 0..1: cell 1 reaches 3: max 3.
- [5,10) covers cell 0 (now 2): max stays 3.
- [25,55) covers cells 4..6: cell 4 is 2, cell 5 is 1, cell 6 is 2; max stays 3.
- Result [1, 1, 2, 3, 3, 3].

**Code:**
```python
import random
random.seed(50)

def calendar_k(bookings):
    xs = sorted({x for s, e in bookings for x in (s, e)})
    pos = {x: i for i, x in enumerate(xs)}
    m = len(xs) - 1                           # elementary cells [xs[k], xs[k+1])
    mx = [0] * (4 * m); lz = [0] * (4 * m)    # mx[o] = best overlap inside o, INCLUDING o's own lz

    def add(o, lo, hi, l, r):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            mx[o] += 1; lz[o] += 1; return
        mid = (lo + hi) // 2
        add(2 * o, lo, mid, l, r); add(2 * o + 1, mid + 1, hi, l, r)
        mx[o] = max(mx[2 * o], mx[2 * o + 1]) + lz[o]     # no push-down: the tag stays here

    out = []
    for s, e in bookings:
        add(1, 0, m - 1, pos[s], pos[e] - 1)  # cells from s up to (not including) e
        out.append(mx[1])
    return out

def oracle(bookings):                         # recompute from scratch after every booking
    out = []
    for k in range(1, len(bookings) + 1):
        pts = sorted({x for s, e in bookings[:k] for x in (s, e)})
        out.append(max(sum(1 for s, e in bookings[:k] if s <= x < e) for x in pts))
    return out

assert calendar_k([[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]) == [1, 1, 2, 3, 3, 3]
assert calendar_k([[0, 5], [5, 10], [0, 10]]) == [1, 1, 2]
print('examples ok')

for _ in range(600):
    n = random.randint(1, 10)
    bk = []
    for _ in range(n):
        s = random.randint(0, 14); bk.append([s, random.randint(s + 1, 15)])
    assert calendar_k(bk) == oracle(bk), bk
print('600 random booking lists match the recompute-from-scratch oracle')

assert calendar_k([[0, 1]]) == [1]
assert calendar_k([[3, 7]] * 4) == [1, 2, 3, 4]                       # identical bookings
assert calendar_k([[0, 5], [5, 10], [10, 15]]) == [1, 1, 1]           # touching never overlaps
assert calendar_k([[0, 10**9], [0, 1], [10**9 - 1, 10**9]]) == [1, 2, 2]
bk = [[random.randint(0, 5 * 10**8), 0] for _ in range(400)]
for b in bk: b[1] = b[0] + random.randint(1, 5 * 10**8)
res = calendar_k(bk)
assert res == oracle(bk) and res == sorted(res)
print('400 bookings with endpoints up to 10^9 ok; answers never decrease, final max', res[-1])
print('first example:', calendar_k([[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]))
```

**Output (my run):**
```
examples ok
600 random booking lists match the recompute-from-scratch oracle
400 bookings with endpoints up to 10^9 ok; answers never decrease, final max 208
first example: [1, 1, 2, 3, 3, 3]
```

**Edge cases:**
- One booking: [1].
- Identical bookings repeated: the answer grows by one each time.
- Touching bookings ([0,5), [5,10), [10,15)): never overlap, answers stay 1.
- A booking [0, 10^9) with tiny ones inside: compression handles the span.
- The output is never decreasing (adding a booking cannot reduce a maximum).
- Duplicate endpoints: `set` collapses them, so every booking maps to valid cell indices (`pos[e] - 1 >= pos[s]` because s < e).

**Follow-ups:**
- *Why no push-down is needed?* Only a global maximum is queried, never a partial range, so the tag can stay on the node; each node's `mx` already includes its own tag, and ancestors add their tags on the way up.
- *What if bookings arrive online (unknown in advance)?* Use a dynamic segment tree over [0, 10^9] (nodes created on demand, O(log 10^9) per booking), or a sorted map of boundary deltas with an O(n) scan.
- *What changes for closed intervals?* Make the end exclusive by using `e + 1`, or compress with the closed convention; state the choice first.
- *Scoring note (30 pts, split per the part header rubric):* 9 pts for stating the half-open rule, the cell model, and that the answer is a maximum over cells; 9 pts for a correct solution that passes the examples and a random check against the recompute oracle; 6 pts for complexity and the reason compression plus lazy tags give O(n log n); 3 pts for the seeded edge cases (touching bookings, identical bookings, single booking); 3 pts for the crisp summary. Partial: the O(n^2) per-insert sweep with correct half-open handling earns roughly 18 of 30, and a difference array over raw coordinates scores low because coordinates reach 10^9.
- *How I would pace this (13 min):* 3 min on the boundary rule and the cell model, 6 min coding the compressed lazy tree, 2 min on the dry run, 2 min on complexity and the offline caveat.

**Common mistakes:**
- Adding to cells `pos[s] .. pos[e]` (closed) so touching bookings falsely overlap.
- Treating each endpoint as a point instead of a cell between endpoints.
- Mixing up the tree size: `m = len(xs) - 1` cells, not `len(xs)`.
- Forgetting `+ lz[o]` when recomputing `mx[o]` without push-down.
- Using a difference array over raw coordinates up to 10^9.

