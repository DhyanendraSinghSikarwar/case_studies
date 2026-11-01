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
