# Book 5 Part 14: answers Q11-Q20 (Wave B)

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
