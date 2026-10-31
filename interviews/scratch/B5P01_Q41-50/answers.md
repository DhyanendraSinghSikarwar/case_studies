### Q41 ⭐ 🟡 Designing hash keys. For grouping problems compare keys that are sorted strings, count tuples, frozensets, and polynomial or product hashes; discuss correctness (can two different groups share a key), cost in terms of key length and alphabet, and why a list or set cannot be a dict key. Example: group the words ['ab','ba','abb','bab'] and show a key that wrongly merges groups, such as the sum of character codes with a different multiset.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Python dict and set internals explainers (designgurus.io, a discuss.python.org thread, medium and dev.to posts, CPython dictobject.c excerpts; snippets only, not opened; sources disagree on probing details so verify against current CPython docs); interview-style Python Q&A, not company reports
**Pattern:** Hashing with a canonical key. Two items are in the same group exactly when their keys are equal, so the key must be a complete invariant of the group.

**Say this first (1 line):** A good key is a canonical form: equal keys if and only if same multiset of letters. Sorted string and count tuple are exact. Sum of character codes and frozenset of characters are not.

**Brute force:** Compare every pair of words by sorting both: O(n^2 * L log L). Fine for a sanity check, too slow to ship.

**Optimal:** Compute one key per word, put the word in `dict[key]`. The key must satisfy two things.
- Same group means same key (no false splits).
- Different group means different key (no false merges).

| Key | Exact? | Cost per word (length L, alphabet A) | Notes |
|---|---|---|---|
| sorted string | yes | O(L log L) | simplest, hashable str |
| 26-count tuple | yes | O(L + A) | best for long words, small alphabet |
| frozenset of (char, count) items | yes | O(L) | any alphabet, no fixed array |
| prime product | yes (unique factorisation) | O(L) multiplications on big ints | cute, numbers grow fast, slow for long words |
| frozenset of chars | NO | O(L) | drops multiplicity: 'ab' and 'abb' merge |
| sum of char codes | NO | O(L) | 'ad' and 'bc' both 197 |
| polynomial / power-sum hash mod p | NO (probabilistic) | O(L) | collisions exist; only safe if you verify or accept risk |

**Complexity:** n words, max length L. Sorted key: O(n L log L). Count tuple: O(n (L + A)). Space O(n L) for the keys and groups. Dict operations are average O(1) once the key is hashed; hashing a tuple of 26 ints or a string of length L costs O(A) or O(L).

**Dry run:** words ['ab','ba','abb','bab'] with sorted key.
- 'ab' -> 'ab', 'ba' -> 'ab': group 1.
- 'abb' -> 'abb', 'bab' -> 'abb': group 2.
- With `frozenset(w)`: all four become {a, b}, so one wrong group of four.

Important: the prompt's own example does NOT break the sum-of-codes key. 'ab' and 'ba' both sum to 195, 'abb' and 'bab' both sum to 293, and 195 != 293, so the sum key happens to give the right answer here (see the run: it prints OK). The sum key breaks on words like 'ad' and 'bc' (both 197). In the same example, `frozenset` is the key that does break. Say this plainly if asked.

**Code:**
```python
from collections import Counter, defaultdict
from itertools import combinations
import random

PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]

def key_sorted(w):   return "".join(sorted(w))                    # O(L log L), exact
def key_count(w):                                                  # O(L + 26), exact
    c = [0] * 26
    for ch in w: c[ord(ch) - 97] += 1
    return tuple(c)
def key_counter_items(w): return frozenset(Counter(w).items())    # O(L), exact, any alphabet
def key_primes(w):                                                 # exact (unique factorisation), big ints
    p = 1
    for ch in w: p *= PRIMES[ord(ch) - 97]
    return p
def key_frozenset(w): return frozenset(w)                          # WRONG: drops multiplicity
def key_sum(w):       return sum(map(ord, w))                      # WRONG: different multisets, same sum
def key_poly_mod(w, mod=101):                                      # sum of ord^2 mod small prime: collides
    return sum(ord(c) ** 2 for c in w) % mod

def group(words, key):
    d = defaultdict(list)
    for w in words: d[key(w)].append(w)
    return list(d.values())

def partition(groups):  # canonical form to compare groupings
    return sorted(sorted(g) for g in groups)

words = ['ab', 'ba', 'abb', 'bab']
truth = partition(group(words, key_sorted))
print("truth            :", truth)
for name, k in [("count tuple", key_count), ("counter items", key_counter_items),
                ("prime product", key_primes), ("frozenset(chars)", key_frozenset),
                ("sum of ords", key_sum)]:
    p = partition(group(words, k))
    print(f"{name:17}:", "OK " if p == truth else "WRONG", p)

# The prompt's example does NOT break the sum key, so find words that do:
print("sum('ad'), sum('bc'):", key_sum('ad'), key_sum('bc'), "-> merged although multisets differ")
print("frozenset('ab') == frozenset('abb'):", frozenset('ab') == frozenset('abb'))

# a deterministic collision for the small-modulus polynomial-style hash
col = next((a, b) for a, b in combinations(["".join(t) for t in
           [(x, y) for x in "abcdefgh" for y in "abcdefgh"]], 2)
           if sorted(a) != sorted(b) and key_poly_mod(a) == key_poly_mod(b))
print("mod-101 sum-of-squares collision:", col)

# unhashable keys
for bad in ([1, 2], {1, 2}):
    try: {bad: 1}
    except TypeError as e: print("TypeError:", e)
print("tuple/frozenset keys fine:", {(1, 2): 1, frozenset({1, 2}): 2})

# seeded cross-check: exact keys must equal truth partition, wrong keys must (often) not
rng = random.Random(41)
bad_counts = {"frozenset": 0, "sum": 0, "poly101": 0}
for _ in range(400):
    ws = ["".join(rng.choice("abcd") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(1, 8))]
    t = partition(group(ws, key_sorted))
    for k in (key_count, key_counter_items, key_primes):
        assert partition(group(ws, k)) == t
    bad_counts["frozenset"] += partition(group(ws, key_frozenset)) != t
    bad_counts["sum"] += partition(group(ws, key_sum)) != t
    bad_counts["poly101"] += partition(group(ws, key_poly_mod)) != t
print("exact keys matched on 400 seeded cases; wrong-key failures:", bad_counts)

# edge cases
assert group([], key_sorted) == []
assert partition(group(['', ''], key_count)) == [['', '']]
assert key_sorted('') == '' and key_primes('') == 1
assert key_count('a') != key_count('b')
print("edge asserts passed")
```

**Output (my run):**
```text
truth            : [['ab', 'ba'], ['abb', 'bab']]
count tuple      : OK  [['ab', 'ba'], ['abb', 'bab']]
counter items    : OK  [['ab', 'ba'], ['abb', 'bab']]
prime product    : OK  [['ab', 'ba'], ['abb', 'bab']]
frozenset(chars) : WRONG [['ab', 'abb', 'ba', 'bab']]
sum of ords      : OK  [['ab', 'ba'], ['abb', 'bab']]
sum('ad'), sum('bc'): 197 197 -> merged although multisets differ
frozenset('ab') == frozenset('abb'): True
mod-101 sum-of-squares collision: ('ab', 'ah')
TypeError: unhashable type: 'list'
TypeError: unhashable type: 'set'
tuple/frozenset keys fine: {(1, 2): 1, frozenset({1, 2}): 2}
exact keys matched on 400 seeded cases; wrong-key failures: {'frozenset': 129, 'sum': 24, 'poly101': 18}
edge asserts passed
```

**Edge cases:**
- Empty string: key '' or an all-zero tuple, fine.
- Empty list: return an empty list.
- Uppercase or Unicode: the 26-slot array breaks; use the Counter-items key or sorted.
- Repeated identical words go in the same group.

**Follow-ups:**
- Why can't a list or set be a key? Mutable, so the hash could change while stored; Python refuses (`TypeError: unhashable type`). Use a tuple or frozenset.
- Why does a tuple of counts beat sorting? O(L + A) versus O(L log L), but only when A is small and fixed.
- Can a hash collision still happen with an exact key? The dict key comparison uses equality after hash match, so grouping stays correct. Collisions only cost time.

**Common mistakes:**
- Using `sum(ord(c))` or `frozenset(word)` as the key.
- Using a float or a modded polynomial hash as the key and trusting it with no equality check.
- Forgetting that frozenset ignores duplicates.
- Using a list as the key.
- Claiming the prompt example breaks the sum key (it does not; it breaks `frozenset`).

---

### Q42 ⭐ 🟡 Bloom filter at concept level. A service wants to check 'have I seen this URL?' for 10^8 URLs with a few gigabytes of memory. Explain how a Bloom filter works (bit array, k hash functions), why it has false positives but no false negatives, the formula for false-positive rate p ~ (1 - e^(-kn/m))^k, and why deletion is not supported. Build a tiny one with hashlib-based hashes and compare measured versus predicted false-positive rate on invented data. This is concept level; no design of the whole service. Example: m=10,000 bits, n=1,000 items, k=3.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Python dict and set internals explainers (designgurus.io, a discuss.python.org thread, medium and dev.to posts, CPython dictobject.c excerpts; snippets only, not opened; sources disagree on probing details so verify against current CPython docs); interview-style Python Q&A, not company reports
**Pattern:** Probabilistic set membership. Trade a small, tunable false-positive rate for a large drop in memory. Hashing idea only, concept level.

**Say this first (1 line):** A Bloom filter is a bit array plus k hash functions. Add sets k bits; query checks the same k bits. All set means "probably seen", any zero means "definitely not seen".

**Brute force:** A Python `set` of the URLs. Exact, but 10^8 URLs at roughly 50+ bytes of string each plus set overhead is many gigabytes, and Python object overhead makes it worse.

**Optimal:** Bloom filter.
- Array of m bits, all zero.
- `add(x)`: compute k indices h1(x)..hk(x) mod m, set those bits.
- `query(x)`: True only if all k bits are 1.
- No false negatives: an added item's k bits are never cleared.
- False positives: other items may have set all k of x's bits by accident.
- No deletion: clearing a bit might erase evidence for other items, which would create false negatives. (Counting Bloom filters keep a small counter per slot instead.)

**Complexity:** add and query are O(k) time, independent of n. Space is m bits. After n inserts, a given bit is still 0 with probability about e^(-kn/m), so false-positive rate p ~ (1 - e^(-kn/m))^k. The best k is about (m/n) ln 2, and the needed size is m = -n ln p / (ln 2)^2, about 9.6 bits per item at p = 1%.

**Dry run:** tiny filter, m = 8, k = 2, with made-up hash values to show the idea.
- add 'a' sets bits 1 and 5; add 'b' sets bits 5 and 6. Bits set: {1, 5, 6}.
- query 'c' hashes to 1 and 6: both set, so "probably seen" (a false positive; 'c' was never added).
- query 'd' hashes to 2 and 5: bit 2 is zero, so "definitely not seen".

**Code:**
```python
import hashlib, math, random

class Bloom:
    def __init__(self, m, k):
        self.m, self.k, self.bits = m, k, bytearray(m)   # one byte per bit: simple, 8x wasteful
    def _idx(self, item):
        d = hashlib.sha256(item.encode()).digest()       # deterministic, unlike str hash()
        return [int.from_bytes(d[4*i:4*i+4], "big") % self.m for i in range(self.k)]  # k <= 8
    def add(self, item):
        for i in self._idx(item): self.bits[i] = 1
    def __contains__(self, item):
        return all(self.bits[i] for i in self._idx(item))

def predicted(m, n, k): return (1 - math.exp(-k * n / m)) ** k

m, n, k = 10_000, 1_000, 3
rng = random.Random(42)
members = [f"https://ex.test/in/{rng.getrandbits(48):012x}" for _ in range(n)]
others  = [f"https://ex.test/out/{rng.getrandbits(48):012x}" for _ in range(20_000)]
exact = set(members)                       # brute force: exact, but stores every URL
assert not (exact & set(others))

bf = Bloom(m, k)
for u in members: bf.add(u)
assert all(u in bf for u in members)       # no false negatives, ever
fp = sum(u in bf for u in others)
print(f"m={m} n={n} k={k}")
print(f"predicted FPR = {predicted(m, n, k):.4f}")
print(f"measured  FPR = {fp / len(others):.4f}  ({fp} of {len(others)} absent URLs said 'seen')")
print(f"fraction of bits set = {sum(bf.bits)/m:.3f}  (theory 1-e^(-kn/m) = {1-math.exp(-k*n/m):.3f})")

kopt = m / n * math.log(2)
print(f"optimal k = (m/n) ln2 = {kopt:.2f}; predicted FPR at k=7: {predicted(m, n, 7):.4f}")
bf7 = Bloom(m, 7)
for u in members: bf7.add(u)
fp7 = sum(u in bf7 for u in others)
print(f"measured FPR at k=7 = {fp7 / len(others):.4f}")

# sizing for the prompt: 1e8 URLs, target 1% false positives
N, p = 10**8, 0.01
bits = -N * math.log(p) / math.log(2) ** 2
print(f"1e8 URLs at p=1%: {bits/N:.2f} bits/item, {bits/8/1e6:.0f} MB, k={bits/N*math.log(2):.1f}")

# seeded cross-check: no false negatives on many random configurations
for seed in range(300):
    r = random.Random(seed)
    mm, nn, kk = r.randint(8, 200), r.randint(0, 30), r.randint(1, 8)
    b = Bloom(mm, kk); items = [f"x{r.getrandbits(32)}" for _ in range(nn)]
    for it in items: b.add(it)
    assert all(it in b for it in items)
print("300 seeded configs: zero false negatives")

# edge cases
empty = Bloom(100, 3)
assert "anything" not in empty
tiny = Bloom(1, 3); tiny.add("a")
assert "zzz" in tiny                       # m=1: everything is a false positive
print("edge asserts passed")
```

**Output (my run):**
```text
m=10000 n=1000 k=3
predicted FPR = 0.0174
measured  FPR = 0.0158  (316 of 20000 absent URLs said 'seen')
fraction of bits set = 0.258  (theory 1-e^(-kn/m) = 0.259)
optimal k = (m/n) ln2 = 6.93; predicted FPR at k=7: 0.0082
measured FPR at k=7 = 0.0089
1e8 URLs at p=1%: 9.59 bits/item, 120 MB, k=6.6
300 seeded configs: zero false negatives
edge asserts passed
```

Reading the run: predicted 1.74% against measured 1.58% is close (the gap is sampling noise on 20,000 trials plus slightly non-ideal hashing). Going from k=3 to k=7 halves the rate, as the formula says. For the prompt's scale, 10^8 URLs at 1% needs about 120 MB, so "a few gigabytes" is far more than needed; the memory budget would allow a much lower false-positive rate. The example in the prompt (m=10,000, n=1,000, k=3) is fine; it just gives about 1.7%, not a tiny rate.

**Edge cases:**
- Empty filter: every query is a definite "no".
- Overfilled filter (n much larger than m/k): most bits are 1 and nearly everything is a false positive.
- Duplicate adds change nothing.
- Python's built-in `hash(str)` changes per process (PYTHONHASHSEED), so a persisted filter must use a stable hash such as hashlib or mmh3-style.

**Follow-ups:**
- How do you pick k? About (m/n) ln 2; too many hashes fill the array faster, too few leave more collisions.
- How to delete? Counting Bloom filter (counters instead of bits) or a cuckoo filter.
- How do k hashes get computed cheaply? Double hashing: g_i = h1 + i*h2 mod m from two base hashes.
- What do you do on a "probably seen"? Fall back to an exact lookup (database or cache) only on those; the filter saves the lookups for definite "no" answers.

**Common mistakes:**
- Saying a Bloom filter can give false negatives (it cannot, unless you delete or corrupt bits).
- Using Python's randomised `hash()` for a filter you save to disk.
- Ignoring that the false-positive rate rises as you keep inserting past the designed n.
- Treating the formula as exact: it assumes independent uniform hashes.

---

### Q43 ⭐ 🟡 Two Sum at scale. The same Two Sum question, but the numbers arrive as a stream, or the file is too large to fit in memory. Discuss: a streaming hash set with eviction limits, an external sort then two-pointer approach, hash-partitioning values and their complements to the same bucket, and what answer is exact versus approximate. Then implement the in-memory partitioned version on a small input. Example: 12 numbers, target 20, split into 3 partitions by hash of min(x, target-x).
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports
**Pattern:** Complement lookup, scaled out. Same hash idea as Two Sum, but you split the data so each piece fits in memory. The key insight: x and its complement (target - x) must be routed to the same place.

**Say this first (1 line):** Partition by a symmetric key, min(x, target - x), so every number and its complement land in the same bucket, then solve each bucket in memory with a normal hash lookup.

**Brute force:** Two nested loops, O(n^2) time. Or one global hash set, O(n) time, but O(n) memory, which is the thing that does not fit.

**Optimal:** Pick by what is allowed.
| Situation | Approach | Exact? |
|---|---|---|
| Stream, bounded memory | hash set of last W values; check `target - x` on arrival | Approximate: misses pairs whose partner was evicted |
| Stream, unlimited time, disk | external merge sort, then two pointers in one sequential pass | Exact, O(n log n) I/O-heavy, O(1) extra memory in the pass |
| Too big for RAM but can shuffle | hash-partition by `min(x, t-x)` into P files, then in-memory Two Sum per file | Exact |
| Need only "does a pair exist?" with tiny memory | Bloom filter of seen values | Approximate (false positives); confirm with a second pass |

Why the symmetric key works: min(x, t-x) is the same for x and for t-x, so both go to one partition. If you partitioned by x alone, the complement would sit in a different file.

**Complexity:** Partitioned: one pass to write n values, one pass to read them back, then O(bucket size) per bucket. Total O(n) time, memory O(n / P) if the hash spreads values evenly. Skewed data (many equal values) gives one huge bucket; fix by also splitting on a second hash or counting duplicates instead of storing them. Sorted version: O(n log n) time.

**Dry run:** target 20, 12 numbers, 3 partitions by `min(x, 20 - x) % 3`.
- 3 and 17 both have key 3, partition 0. 1 and 19 both have key 1, partition 1. 8 and 12 both have key 8, partition 2.
- Within partition 1, the counter holds 1, 7, 10, 10, 13, 19: pairs (1, 19), (7, 13), and 10 + 10.
- For x = y = 10, count c*(c-1)/2 = 1.
- Total 6 index pairs.

**Code:**
```python
from collections import Counter, defaultdict
import random

def brute(nums, t):                      # O(n^2) reference: count index pairs i<j
    return sum(nums[i] + nums[j] == t for i in range(len(nums)) for j in range(i + 1, len(nums)))

def partition_of(x, t, parts):           # x and t-x MUST land in the same partition
    return min(x, t - x) % parts

def partitioned(nums, t, parts=3):
    buckets = defaultdict(list)          # stand-in for `parts` files on disk
    for x in nums: buckets[partition_of(x, t, parts)].append(x)
    total, pairs = 0, []
    for pid in sorted(buckets):          # each bucket fits in memory on its own
        c = Counter(buckets[pid])
        for x in sorted(c):
            y = t - x
            if x < y and y in c:
                total += c[x] * c[y]; pairs.append((x, y))
            elif x == y:
                total += c[x] * (c[x] - 1) // 2
                if c[x] > 1: pairs.append((x, y))
    return total, pairs, {p: sorted(v) for p, v in sorted(buckets.items())}

def sorted_two_pointer(nums, t):         # what external sort + one streaming pass gives you
    a = sorted(nums); i, j, total = 0, len(a) - 1, 0
    while i < j:
        s = a[i] + a[j]
        if s < t: i += 1
        elif s > t: j -= 1
        else:
            if a[i] == a[j]: total += (j - i + 1) * (j - i) // 2; break
            li, lj = a[i], a[j]; ci = cj = 0
            while a[i] == li: i += 1; ci += 1
            while a[j] == lj: j -= 1; cj += 1
            total += ci * cj
    return total

def bounded_stream(nums, t, cap):        # streaming with eviction: APPROXIMATE (can miss pairs)
    seen, order, found = set(), [], 0
    for x in nums:
        if t - x in seen: found += 1
        seen.add(x); order.append(x)
        if len(order) > cap: seen.discard(order.pop(0))   # pop(0) is O(n); use deque in real code
    return found

nums = [3, 17, 8, 12, 5, 15, 10, 10, 1, 19, 7, 13]
t = 20
total, pairs, buckets = partitioned(nums, t, 3)
print("buckets:", buckets)
print("pairs (value form):", pairs, "-> index pairs:", total)
print("brute:", brute(nums, t), "| sorted two-pointer:", sorted_two_pointer(nums, t))
print("bounded stream cap=12:", bounded_stream(nums, t, 12), "cap=2:", bounded_stream(nums, t, 2), "(exact is", brute(nums, t), ")")

far = [1, 5, 6, 7, 19]                   # partners 1 and 19 are four positions apart
print("far-apart pair: exact", brute(far, t), "| cap=2 stream finds", bounded_stream(far, t, 2), "| cap=5 finds", bounded_stream(far, t, 5))

rng = random.Random(43)
for _ in range(500):
    n = rng.randint(0, 14)
    a = [rng.randint(-6, 14) for _ in range(n)]; tt = rng.randint(-4, 12)
    parts = rng.randint(1, 5)
    assert partitioned(a, tt, parts)[0] == brute(a, tt) == sorted_two_pointer(a, tt), (a, tt, parts)
print("500 seeded cross-checks passed (partitioned == brute == sorted two-pointer)")

assert partitioned([], 5)[0] == 0
assert partitioned([5], 10)[0] == 0                 # single element cannot pair with itself
assert partitioned([5, 5], 10)[0] == 1
assert partitioned([5, 5, 5], 10)[0] == 3
assert partitioned([-3, 23], 20)[0] == 1            # negatives: Python % keeps bucket id non-negative
print("edge asserts passed")
```

**Output (my run):**
```text
buckets: {0: [3, 17], 1: [1, 7, 10, 10, 13, 19], 2: [5, 8, 12, 15]}
pairs (value form): [(3, 17), (1, 19), (7, 13), (10, 10), (5, 15), (8, 12)] -> index pairs: 6
brute: 6 | sorted two-pointer: 6
bounded stream cap=12: 6 cap=2: 6 (exact is 6 )
far-apart pair: exact 1 | cap=2 stream finds 0 | cap=5 finds 1
500 seeded cross-checks passed (partitioned == brute == sorted two-pointer)
edge asserts passed
```

Note the prompt did not give the 12 numbers, so I chose them. The cap=2 line on the first list still finds all 6 because each partner arrived close by; the "far-apart" line is the one that shows an evicted pair being missed.

**Edge cases:**
- x == target - x needs two copies of x: count c*(c-1)/2, not c.
- Negative numbers: in Python `%` on a negative number is non-negative, so bucket ids stay valid. In other languages mask the hash.
- Skewed buckets (all the same value): count duplicates, do not store them.
- Streaming answers are "found so far"; an evicted partner means a missed pair.

**Follow-ups:**
- What if you only need one pair, not the count? Stop at the first match in any bucket.
- What if values are small integers (say 0..10^6)? Use a bitmap or count array instead of hashing.
- Distributed? Same idea: hash on `min(x, t-x)` to pick the machine (a shuffle step), then each machine solves locally.

**Common mistakes:**
- Partitioning by x alone, so complements are in different buckets.
- Counting x + x twice, or pairing an element with itself.
- Claiming a bounded streaming set is exact.
- Using `list.pop(0)` in the eviction loop (O(n); use `collections.deque`).

---

### Q44 ⭐ 🟡 Number of bad pairs. Given `nums`, a pair (i, j) with i < j is bad if j - i != nums[j] - nums[i]. Count bad pairs in O(n) by rewriting the condition as nums[i] - i == nums[j] - j and counting good pairs, then subtract from the total. Example: [4,1,3,3] -> 5; [1,2,3,4,5] -> 0.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Rewrite the condition so it splits into a per-index key, then count equal keys with a hashmap (complement counting: total pairs minus good pairs).

**Say this first (1 line):** j - i == nums[j] - nums[i] is the same as nums[j] - j == nums[i] - i, so good pairs are pairs with equal key nums[k] - k; bad = total - good.

**Brute force:** Check every pair (i, j): O(n^2) time, O(1) space. Too slow for n around 10^5.

**Optimal:** Move all i terms to one side.
- Good means j - i = nums[j] - nums[i].
- Rearranged: nums[i] - i = nums[j] - j.
- Walk left to right, keep a Counter of keys seen so far. For each j, `seen[key]` is the number of good pairs ending at j.
- Answer = n(n-1)/2 - good. Or add `j - seen[key]` directly: that is the count of earlier indices with a different key.

**Complexity:** O(n) time (one pass, average O(1) dict operations), O(n) space for up to n distinct keys. Python ints do not overflow, so n(n-1)/2 is safe for any n.

**Dry run:** nums = [4, 1, 3, 3], keys nums[k] - k = [4, 0, 1, 0]. Total pairs = 6.
- j=0: key 4, seen empty, good += 0.
- j=1: key 0, good += 0.
- j=2: key 1, good += 0.
- j=3: key 0, seen[0] = 1 (index 1), good += 1.
- good = 1, bad = 6 - 1 = 5.

**Code:**
```python
from collections import Counter
import random

def brute(nums):                                   # O(n^2)
    n = len(nums)
    return sum(j - i != nums[j] - nums[i] for i in range(n) for j in range(i + 1, n))

def optimal(nums):                                 # O(n) time, O(n) space
    n = len(nums)
    total = n * (n - 1) // 2
    seen, good = Counter(), 0
    for i, v in enumerate(nums):
        key = v - i                                # j-i == nums[j]-nums[i]  <=>  nums[j]-j == nums[i]-i
        good += seen[key]                          # earlier indices with the same key form good pairs
        seen[key] += 1
    return total - good

def optimal_single_pass(nums):                     # count bad pairs directly: i - (earlier with same key)
    seen, bad = Counter(), 0
    for i, v in enumerate(nums):
        bad += i - seen[v - i]
        seen[v - i] += 1
    return bad

assert brute([4, 1, 3, 3]) == optimal([4, 1, 3, 3]) == optimal_single_pass([4, 1, 3, 3]) == 5
assert brute([1, 2, 3, 4, 5]) == optimal([1, 2, 3, 4, 5]) == 0
print("examples: [4,1,3,3] ->", optimal([4, 1, 3, 3]), "; [1,2,3,4,5] ->", optimal([1, 2, 3, 4, 5]))

rng = random.Random(44)
for _ in range(600):
    a = [rng.randint(-8, 8) for _ in range(rng.randint(0, 12))]
    assert brute(a) == optimal(a) == optimal_single_pass(a), a
print("600 seeded cross-checks passed")

assert optimal([]) == 0 and optimal([7]) == 0
assert optimal([5, 5, 5, 5]) == 6                  # all equal: keys 5,4,3,2 all different -> all pairs bad
assert optimal([0, 1, 2, 3]) == 0                  # v - i constant -> no bad pairs
assert optimal([-3, -2, -1]) == 0                  # negatives fine
big = list(range(10**5))
assert optimal(big) == 0
assert optimal([0] * 10**5) == 10**5 * (10**5 - 1) // 2   # no overflow in Python
print("edge asserts passed (incl. n = 10^5)")
```

**Output (my run):**
```text
examples: [4,1,3,3] -> 5 ; [1,2,3,4,5] -> 0
600 seeded cross-checks passed
edge asserts passed (incl. n = 10^5)
```

Both examples in the prompt are correct as written (5 and 0).

**Edge cases:**
- Empty or single element: no pairs, answer 0.
- Keys can be negative; fine for a dict.
- Strictly consecutive values (v[k] = k + c): every pair good, answer 0.
- All equal values: keys differ by index, so every pair is bad.

**Follow-ups:**
- Why not nested loops with early exit? Still O(n^2) worst case.
- Same trick elsewhere? Any condition of the form f(i) + g(j) = 0 or f(i) = g(j) can be hashed (Two Sum on a transformed array).
- Memory? Keys can be up to n distinct, so O(n); no way to do much better without sorting.

**Common mistakes:**
- Counting ordered pairs and double counting (use i < j only).
- Rearranging with the wrong sign (nums[i] + i instead of nums[i] - i).
- Counting good pairs including the element with itself.
- Using `n*(n-1)/2` with true division (a float); use `//`.

---

### Q45 ⭐ 🟡 Number of boomerangs. Given distinct points (x, y), a boomerang is an ordered tuple (i, j, k) where the distances from i to j and from i to k are equal. Count them in O(n^2) by hashing squared distances from each anchor point, and explain why squared integers avoid float error. Example: [[0,0],[1,0],[2,0]] -> 2; [[1,1]] -> 0.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Group by key per anchor. For each point as the "center", bucket all other points by distance, then count pairs inside each bucket.

**Say this first (1 line):** Fix point i, count other points by squared distance from i, and each bucket of m points gives m*(m-1) ordered boomerangs.

**Brute force:** Triple loop over (i, j, k) comparing distances: O(n^3). Fine for n up to a few hundred.

**Optimal:** For every anchor i:
- Build a Counter of squared distances `dx*dx + dy*dy` to every point (anchor included; it sits at distance 0 with count 1 because points are distinct).
- For a bucket with m points, ordered (j, k) with j != k is m*(m-1): that is choose j, then choose a different k.
- Sum over buckets and anchors.
- Squared integers avoid floats: sqrt of a big integer can round, so two different distances can compare equal (shown in the run).

**Complexity:** O(n^2) time (n anchors, n points each, O(1) average per dict update). O(n) space for the per-anchor counter, reused each anchor.

**Dry run:** points A(0,0), B(1,0), C(2,0).
- Anchor A: squared distances 0, 1, 4: all buckets size 1, contributes 0.
- Anchor B: 1, 0, 1: bucket for distance 1 has A and C, m=2, contributes 2*1 = 2.
- Anchor C: 4, 1, 0: contributes 0.
- Total 2: the tuples (B, A, C) and (B, C, A).

**Code:**
```python
from collections import Counter
import random, math

def brute(pts):                                    # O(n^3): ordered (i, j, k), j != k, i distinct from both
    n, cnt = len(pts), 0
    d2 = lambda a, b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and i != k and j != k and d2(pts[i], pts[j]) == d2(pts[i], pts[k]):
                    cnt += 1
    return cnt

def optimal(pts):                                  # O(n^2) time, O(n) space
    total = 0
    for (x0, y0) in pts:                           # anchor i
        c = Counter((x - x0) ** 2 + (y - y0) ** 2 for (x, y) in pts)   # squared integer distances
        for m in c.values():
            total += m * (m - 1)                   # ordered pairs (j, k) among m points at that distance
    return total
# note: the anchor itself lands at distance 0 with count 1 (points are distinct) and adds 1*0 = 0.

assert brute([[0, 0], [1, 0], [2, 0]]) == optimal([[0, 0], [1, 0], [2, 0]]) == 2
assert optimal([[1, 1]]) == 0
print("examples:", optimal([[0, 0], [1, 0], [2, 0]]), optimal([[1, 1]]))

# float danger: sqrt distances of large integer points can differ in exact value yet compare equal as floats
a, b = 10**8, 10**8 + 1
print("squared ints differ:", a * a + 1 != b * b, "| math.sqrt(a*a+1) == math.sqrt(a*a):", math.sqrt(a * a + 1) == math.sqrt(a * a))

rng = random.Random(45)
for _ in range(400):
    n = rng.randint(0, 9)
    s = set()
    while len(s) < n: s.add((rng.randint(-3, 3), rng.randint(-3, 3)))     # distinct points
    pts = [list(p) for p in s]
    assert brute(pts) == optimal(pts), pts
print("400 seeded cross-checks passed")

assert optimal([]) == 0
assert optimal([[0, 0], [1, 1]]) == 0
square = [[0, 0], [0, 1], [1, 1], [1, 0]]
assert optimal(square) == brute(square) == 8       # each corner: two neighbours at d=1 -> 2 ordered; plus diagonals none
print("square (4 corners):", optimal(square))
neg = [[-1, 0], [0, 0], [1, 0]]
assert optimal(neg) == 2
grid = [[x, y] for x in range(30) for y in range(30)]
print("30x30 grid (900 points):", optimal(grid))
```

**Output (my run):**
```text
examples: 2 0
squared ints differ: True | math.sqrt(a*a+1) == math.sqrt(a*a): True
400 seeded cross-checks passed
square (4 corners): 8
30x30 grid (900 points): 3122416
```

Both examples in the prompt are correct (2 and 0). The float demo uses the point at x = 10^8: sqrt(10^16 + 1) rounds to exactly 10^8 as a double, so two unequal distances compare equal. Boomerang counts for the 30x30 grid are just a sandbox result, not a known constant.

**Edge cases:**
- Fewer than 3 points: answer 0.
- Collinear equally spaced points: only the middle ones count (as in the example).
- Four corners of a square: each corner has two neighbours at distance 1, so 2 per anchor, 8 total.
- Negative coordinates are fine: squaring removes the sign.
- If points could repeat, the distance-0 bucket would have m > 1 and you must reconsider the definition; the prompt says distinct.

**Follow-ups:**
- Why m*(m-1) and not C(m, 2)? Tuples are ordered, so (i, j, k) and (i, k, j) are different.
- Unordered version? Use m*(m-1)/2 per bucket.
- Could you beat O(n^2)? Not by this method. One anchor with all other points on a circle already yields about n^2 tuples, so you count in buckets instead of listing them.

**Common mistakes:**
- Using `math.sqrt` or `**0.5` and comparing floats.
- Counting C(m, 2) instead of m*(m-1).
- Reusing one global counter across anchors without clearing.
- Counting the anchor itself in a bucket and pairing it (it only affects the distance-0 bucket, which has size 1).

---

### Q46 ⭐ 🟡 Tuple with same product. Given a list of distinct positive integers, count tuples (a, b, c, d) of its values with a*b == c*d where the four indices are different. Count how many pairs give each product and combine with a combinatorial factor of 8 per pair-of-pairs. Example: [2,3,4,6] -> 8; [1,2,4,5,10] -> 16.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Count equal keys over all pairs. The key is the pair product; two pairs with the same product make a valid tuple.

**Say this first (1 line):** Count how many unordered pairs give each product; every two pairs with the same product contribute 8 tuples, so answer = 8 * sum over products of C(c, 2).

**Brute force:** Four nested loops over indices, keep tuples with four different indices and a*b == c*d: O(n^4).

**Optimal:**
- Build a Counter of x*y over all unordered pairs (i < j).
- For a product seen c times, choose 2 of those pairs: c*(c-1)/2.
- Each choice of two pairs {a,b} and {c,d} gives 8 ordered tuples: swap a,b (2) times swap c,d (2) times swap the two sides of the equals sign (2).
- Why the pairs never share an element: values are distinct. If two pairs shared x and had equal product, x*y == x*z forces y == z, so they would be the same pair. So the four indices are automatically different.

**Complexity:** O(n^2) time to enumerate pairs, O(n^2) space in the worst case for the products dict (up to n(n-1)/2 distinct products). Python big ints keep products exact.

**Dry run:** [2, 3, 4, 6].
- Pair products: 2*3=6, 2*4=8, 2*6=12, 3*4=12, 3*6=18, 4*6=24.
- Product 12 appears twice: C(2,2) = 1.
- 8 * 1 = 8. The tuples are the orderings of (2,6,3,4) as a*b == c*d.

**Code:**
```python
from collections import Counter
from itertools import combinations
import random

def brute(nums):                                   # O(n^4): ordered tuples of 4 distinct indices
    n, cnt = len(nums), 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if len({a, b, c, d}) == 4 and nums[a] * nums[b] == nums[c] * nums[d]:
                        cnt += 1
    return cnt

def optimal(nums):                                 # O(n^2) time and space; needs DISTINCT values
    prod = Counter(x * y for x, y in combinations(nums, 2))
    return 8 * sum(c * (c - 1) // 2 for c in prod.values())
# Why 8: two unordered pairs {a,b},{c,d} with equal product. Swap inside pair 1 (2), inside pair 2 (2),
# and swap which pair is on the left of '==' (2): 2*2*2 = 8 ordered tuples.
# Why no overlap: distinct values and equal product => two different pairs sharing an element would share
# the other element too (x*y == x*z => y == z), so they would be the same pair.

assert brute([2, 3, 4, 6]) == optimal([2, 3, 4, 6]) == 8
assert brute([1, 2, 4, 5, 10]) == optimal([1, 2, 4, 5, 10]) == 16
print("examples:", optimal([2, 3, 4, 6]), optimal([1, 2, 4, 5, 10]))

rng = random.Random(46)
for _ in range(400):
    pool = list(range(1, 25)); rng.shuffle(pool)
    a = pool[:rng.randint(0, 9)]                   # distinct positive values
    assert brute(a) == optimal(a), a
print("400 seeded cross-checks passed")

# what goes wrong with duplicates (outside the stated constraints)
dup = [2, 2, 1, 4]
print("duplicates [2,2,1,4]: brute =", brute(dup), "optimal =", optimal(dup), "(optimal is not valid for non-distinct input)")

assert optimal([]) == 0 and optimal([5]) == 0 and optimal([1, 2, 3]) == 0
assert optimal([1, 2, 3, 6]) == 8                  # 1*6 == 2*3
assert optimal([1, 2, 3, 4]) == 0
big = list(range(1, 1001))                         # n = 1000 -> ~500k pair products
print("n=1000 (1..1000):", optimal(big))
assert optimal([10**9, 1, 10**9 - 1, 10**9 + 1]) == 0   # large values: exact ints, no overflow
print("edge asserts passed")
```

**Output (my run):**
```text
examples: 8 16
400 seeded cross-checks passed
duplicates [2,2,1,4]: brute = 8 optimal = 24 (optimal is not valid for non-distinct input)
n=1000 (1..1000): 5894072
edge asserts passed
```

Both examples in the prompt are correct (8 and 16; in the second, products 10 and 20 each appear twice, so 2 * 8 = 16). The "distinct values" line in the output shows what happens if duplicates are allowed: the formula overcounts (24 against the true 8) because pairs can share an index.

**Edge cases:**
- Fewer than 4 numbers: 0.
- All products unique: 0.
- Duplicates (not allowed here): the factor 8 and the no-overlap argument both fail; you would need a different count.
- Very large values: no overflow in Python; in fixed-width languages use 64-bit and watch for 10^9 * 10^9.
- Product 1 or repeated 1s do not matter because values are distinct.

**Follow-ups:**
- Why not sort and use two pointers? Product equality does not have a monotone structure like sums do, so hashing is the clean route.
- What about duplicates in the input? Count by value with multiplicities and handle same-value pairs separately; that is a different, longer problem.
- Can space be reduced? Not easily; you need counts per product.

**Common mistakes:**
- Forgetting the factor 8 (or using 4).
- Using C(c, 2) on ordered pairs, double counting.
- Applying the formula when values repeat.
- Counting a pair against itself.

---

### Q47 ⭐ 🔴 Insert, delete and getRandom with duplicates. Extend a randomised collection to a multiset: insert(x) returns True if x was not present, remove(x) deletes one occurrence, getRandom returns an element with probability proportional to its multiplicity, all in average O(1). Maintain a list plus a dict from value to a set of indices and handle the swap with last when the removed slot is the last one. Example: insert 1, insert 1, insert 2, remove 1, getRandom -> 1 with prob 1/2.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Dense array plus index map. The list gives uniform random access; the dict gives O(1) lookup by value; swap-with-last gives O(1) delete. Duplicates mean the dict stores a set of indices per value.

**Say this first (1 line):** Keep a list of all elements and a dict value -> set of positions; to remove, overwrite the removed slot with the last element, update the moved element's index set, and pop the list.

**Brute force:** A plain list. insert is O(1), getRandom is O(1), remove is O(n) (`list.remove` scans and shifts). `insert` returning "was it absent" is also O(n) with `count`.

**Optimal:**
- `a`: list of every element, duplicates included. `random.choice(a)` is uniform over elements, so a value with multiplicity m has probability m/len(a).
- `pos[v]`: set of indices where v sits in `a`.
- insert(x): `new = not pos[x]`, append, add the index. Return `new`.
- remove(x): if no indices, return False. Pop any index i of x. Let `last = len(a) - 1`. If i != last, move `a[last]` into slot i and fix its index set (add i, discard last). Pop the list. Delete empty sets.
- Order of the two set updates matters: add the new index first, then discard the old one. This also works when the last element has the same value as x.
- The special case i == last needs no move; just pop.

**Complexity:** Each operation does O(1) average list and hash-set work. Space O(n) for the list plus the index sets.

**Dry run:** insert 1, 1, 2 gives a = [1, 1, 2], pos = {1: {0, 1}, 2: {2}}.
- remove(1): pop index 0 from pos[1] (say), last = 2, y = 2. Set pos[2] = {0, 2} then discard 2 -> {0}. a[0] = 2, pop -> a = [2, 1]. pos = {1: {1}, 2: {0}}.
- getRandom: 1 and 2 each with probability 1/2.

**Code:**
```python
import random
from collections import Counter, defaultdict

class BruteMultiset:                               # list only: remove is O(n)
    def __init__(self, seed=0): self.a, self.rng = [], random.Random(seed)
    def insert(self, x): self.a.append(x); return self.a.count(x) == 1
    def remove(self, x):
        if x not in self.a: return False
        self.a.remove(x); return True
    def getRandom(self): return self.rng.choice(self.a)

class RandomizedCollection:                        # average O(1) for all three operations
    def __init__(self, seed=0):
        self.a = []                                # values, dense, so random index is uniform over elements
        self.pos = defaultdict(set)                # value -> set of indices where it sits in self.a
        self.rng = random.Random(seed)
    def insert(self, x):
        new = not self.pos[x]
        self.pos[x].add(len(self.a)); self.a.append(x)
        return new
    def remove(self, x):
        if not self.pos.get(x): return False
        i = self.pos[x].pop()                      # any slot holding x
        last = len(self.a) - 1
        if i != last:
            y = self.a[last]
            self.pos[y].add(i)                     # add the new slot FIRST ...
            self.pos[y].discard(last)              # ... then drop the old one (works when y == x too)
            self.a[i] = y
        self.a.pop()
        if not self.pos[x]: del self.pos[x]
        return True
    def getRandom(self): return self.rng.choice(self.a)

# prompt example
rc = RandomizedCollection(seed=47)
print("insert 1:", rc.insert(1), "| insert 1:", rc.insert(1), "| insert 2:", rc.insert(2))
print("remove 1:", rc.remove(1), "| remaining list:", sorted(rc.a))
draws = Counter(rc.getRandom() for _ in range(10_000))
print("getRandom over 10,000 draws:", dict(sorted(draws.items())), "(expect about 5000 / 5000)")

# the "last slot" trap: remove a value whose only/last copy is at the end, and a value equal to the last
t = RandomizedCollection()
for v in (5, 7, 7): t.insert(v)
assert t.remove(7) and sorted(t.a) == [5, 7] and t.pos[7] == {t.a.index(7)} and t.pos[5] == {0}
assert t.remove(7) and t.a == [5] and 7 not in t.pos
assert not t.remove(7)

# seeded randomized cross-check against Counter model, with invariant checks
rng = random.Random(471)
for trial in range(300):
    rc, model = RandomizedCollection(trial), Counter()
    for _ in range(60):
        x = rng.randint(0, 4)
        if rng.random() < 0.55:
            assert rc.insert(x) == (model[x] == 0); model[x] += 1
        else:
            assert rc.remove(x) == (model[x] > 0)
            if model[x] > 0: model[x] -= 1
        assert Counter(rc.a) == +model                                   # same multiset
        for v, s in rc.pos.items():
            assert s and all(rc.a[i] == v for i in s) and len(s) == model[v]   # index sets exact
        assert sum(len(s) for s in rc.pos.values()) == len(rc.a)
        if rc.a: assert rc.getRandom() in model and model[rc.getRandom()] > 0
print("300 seeded trials x 60 ops: multiset, index sets and return values all consistent")

# edge cases
e = RandomizedCollection()
assert e.remove(3) is False
assert e.insert(3) is True and e.insert(3) is False
assert e.remove(3) and e.remove(3) and not e.remove(3) and e.a == []
try: e.getRandom(); raise SystemExit("should fail")
except IndexError: print("getRandom on empty raises IndexError (the problem guarantees non-empty)")
print("edge asserts passed")
```

**Output (my run):**
```text
insert 1: True | insert 1: False | insert 2: True
remove 1: True | remaining list: [1, 2]
getRandom over 10,000 draws: {1: 4993, 2: 5007} (expect about 5000 / 5000)
300 seeded trials x 60 ops: multiset, index sets and return values all consistent
getRandom on empty raises IndexError (the problem guarantees non-empty)
edge asserts passed
```

The prompt's example (1 with probability 1/2) is correct: the run shows 4993 versus 5007 over 10,000 draws with a seeded generator, which is sampling noise around 50%, not a proof of uniformity.

**Edge cases:**
- Remove a value that is absent: return False, change nothing.
- Remove the element sitting in the last slot (i == last): no swap.
- Removed value equals the last element's value: the add-then-discard order keeps the set correct.
- Last copy removed: delete the key so `insert` returns True next time.
- getRandom on empty: the problem guarantees non-empty; `random.choice` would raise IndexError.

**Follow-ups:**
- Why a set of indices, not a list? Removing a specific index from a list is O(n); a set gives O(1).
- Why is `pos[x].pop()` fine? Any occurrence of x is interchangeable for a multiset.
- Why not a Counter alone? getRandom would need O(number of distinct values) to sample by weight.

**Common mistakes:**
- Discarding the old index before adding the new one when both values are equal, which loses the index.
- Forgetting the i == last case and corrupting the sets.
- Leaving empty sets in the dict so `insert` wrongly returns False.
- Returning "was present" instead of "was absent" from insert.

---

### Q48 ⭐ 🔴 Contains duplicate III. Given `nums` and integers indexDiff and valueDiff, decide whether there exist i != j with |i - j| <= indexDiff and |nums[i] - nums[j]| <= valueDiff. Solve with bucketing (bucket width valueDiff+1) in O(n), keeping only the last indexDiff elements; mention sortedcontainers.SortedList as the alternative at O(n log k). Example: nums=[1,2,3,1], indexDiff=3, valueDiff=0 -> True; nums=[1,5,9,1,5,9], indexDiff=2, valueDiff=3 -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Bucketing (pigeonhole) over a sliding window of the last k indices. Bucket width t+1 means two values in the same bucket are always within t, and only adjacent buckets can hold other close values.

**Say this first (1 line):** Put each value in bucket x // (t+1), keep only the last k values in a dict of buckets, and on each new value check its own bucket and the two neighbours.

**Brute force:** For each i compare with the next k elements: O(n * k) time, O(1) space. Too slow when both n and k are around 10^5.

**Optimal:**
- Width w = valueDiff + 1. Bucket id = x // w. Python floor division works for negatives (-1 // 3 is -1), so negative values bucket correctly. In C or Java the truncating division needs a fix.
- Same bucket as an existing value: the gap is at most w - 1 = t, so return True.
- Neighbour bucket b-1 or b+1: the stored value may or may not be within t, so compare the actual gap.
- Buckets two or more apart differ by at least w + 1 > t, so they cannot match.
- Invariant: each bucket holds at most one value (a second one would have returned True). After adding index i, evict nums[i-k] so only the last k values remain.
- Guard: indexDiff <= 0 or valueDiff < 0 means False.
- Alternative: a `SortedList` window. For x, bisect for the first stored value >= x - t and test it is <= x + t. O(n log k) time. `sortedcontainers` is third party; I use it only here, as the question says.

**Complexity:** Buckets: O(n) average time (each element does a constant number of dict operations), O(min(n, k)) space. SortedList: O(n log k) time, O(k) space.

**Dry run:** nums = [1, 5, 9, 1, 5, 9], k = 2, t = 3, so w = 4.
- 1 -> bucket 0, store. 5 -> bucket 1: neighbour bucket 0 holds 1, gap 4 > 3, no. Store.
- 9 -> bucket 2: neighbour bucket 1 holds 5, gap 4 > 3, no. Store. Evict nums[0] = 1 (bucket 0).
- 1 -> bucket 0: bucket 1 holds 5, gap 4, no. Evict 5. And so on: every adjacent gap is exactly 4, never within 3, so the answer is False.

**Code:**
```python
import random
from sortedcontainers import SortedList

def brute(nums, k, t):                             # O(n * k)
    n = len(nums)
    return any(abs(nums[i] - nums[j]) <= t for i in range(n) for j in range(i + 1, min(n, i + k + 1)))

def buckets(nums, k, t):                           # O(n) average time, O(min(n, k)) space
    if k <= 0 or t < 0: return False
    w, box = t + 1, {}                             # bucket id = x // w; two values in one bucket differ by <= t
    for i, x in enumerate(nums):
        b = x // w                                 # floor division: correct for negatives in Python
        if b in box: return True                   # same bucket
        if b - 1 in box and x - box[b - 1] <= t: return True    # neighbour buckets: check the actual gap
        if b + 1 in box and box[b + 1] - x <= t: return True
        box[b] = x                                 # at most one value per bucket (else we would have returned)
        if i >= k: del box[nums[i - k] // w]       # keep only the last k values
    return False

def sorted_list(nums, k, t):                       # O(n log k)
    if k <= 0 or t < 0: return False
    sl = SortedList()
    for i, x in enumerate(nums):
        j = sl.bisect_left(x - t)                  # first stored value >= x - t
        if j < len(sl) and sl[j] <= x + t: return True
        sl.add(x)
        if i >= k: sl.remove(nums[i - k])
    return False

for args, want in [(([1, 2, 3, 1], 3, 0), True), (([1, 5, 9, 1, 5, 9], 2, 3), False)]:
    assert brute(*args) == buckets(*args) == sorted_list(*args) == want
print("examples:", buckets([1, 2, 3, 1], 3, 0), buckets([1, 5, 9, 1, 5, 9], 2, 3))

rng = random.Random(48)
for _ in range(2000):
    n = rng.randint(0, 12)
    a = [rng.randint(-15, 15) for _ in range(n)]
    k, t = rng.randint(0, 5), rng.randint(0, 6)
    r = brute(a, k, t)
    assert buckets(a, k, t) == r == sorted_list(a, k, t), (a, k, t)
print("2000 seeded cross-checks passed (brute == buckets == SortedList)")

assert buckets([], 3, 0) is False and buckets([5], 3, 0) is False
assert buckets([1, 1], 0, 5) is False              # indexDiff 0: i != j impossible
assert buckets([1, 1], 1, 0) is True
assert buckets([-1, 1], 1, 2) is True              # negatives straddle zero: -1//3=-1, 1//3=0, neighbour check
assert buckets([-1, 1], 1, 1) is False
assert buckets([0, 10**9 * 2], 1, 10**9 * 2) is True
assert buckets([1, 3], 1, -1) is False            # negative valueDiff
assert buckets([8, 4, 12], 2, 3) is False and buckets([8, 4, 12], 2, 4) is True
big = list(range(0, 10**5, 7))                     # neighbours differ by exactly 7
assert buckets(big, 5, 6) is False and buckets(big, 5, 7) is True
print("edge asserts passed")
```

**Output (my run):**
```text
examples: True False
2000 seeded cross-checks passed (brute == buckets == SortedList)
edge asserts passed
```

Both prompt examples are correct (True and False).

**Edge cases:**
- indexDiff = 0: no two distinct indices are allowed, so False even for equal values.
- valueDiff = 0: width 1, only equal values match.
- Negative values and values straddling zero: floor division handles them; neighbour check catches -1 and 1 with t = 2.
- Very large values: Python ints, no overflow (in fixed-width languages the subtraction can overflow).
- Window eviction must use the bucket of the old value, `nums[i-k] // w`.

**Follow-ups:**
- Why must the neighbour check compare actual values? Adjacent buckets only guarantee a gap below 2w, not below t.
- Why evict after insert with `i >= k`? After inserting index i, the window must hold indices i-k+1..i, so i-k leaves.
- Which would you pick in an interview? Bucket if you can explain the pigeonhole in a minute; SortedList if the width idea is not coming, since the logic is shorter.

**Common mistakes:**
- Bucket width t instead of t+1 (breaks t = 0 with a divide by zero).
- Using truncating division for negatives.
- Evicting the wrong bucket or forgetting to evict.
- Storing a list per bucket rather than noticing one value suffices.
- Forgetting the guards for k <= 0 and t < 0.

---

### Q49 ⭐ 🔴 Max points on a line. Given distinct 2D integer points, return the maximum number of them lying on one straight line, in O(n^2). Hash the slope from each anchor as a reduced fraction using gcd and normalised sign, never as a float, and handle vertical lines. Example: [[1,1],[2,2],[3,3]] -> 3; [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]] -> 4.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Anchor plus hashed direction. Fix a point, hash the direction to every other point in a canonical exact form, and the biggest bucket plus the anchor is the best line through that anchor.

**Say this first (1 line):** For each anchor, count the other points by reduced (dx, dy) with a fixed sign, never by float slope; answer is 1 plus the biggest count over all anchors.

**Brute force:** For every pair define the line, then count points with zero cross product (dx1*dy2 == dx2*dy1): O(n^3), exact.

**Optimal:**
- For anchor i, for every other point compute dx, dy.
- Divide both by g = gcd(dx, dy). Equal directions then give identical pairs.
- Normalise the sign so the opposite direction maps to the same key: if dx < 0, or dx == 0 and dy < 0, negate both. This makes vertical lines (0, 1) and horizontal lines (1, 0) work with no special case and no division by zero.
- Count with a Counter; best through this anchor = 1 + max count.
- Points on the same line through the anchor share the same direction key, and any two lines through the anchor have different keys, so it counts exactly.
- Floats are wrong: slopes like (n-1)/n and n/(n+1) differ by about 1e-18, below double precision (shown in the run).

**Complexity:** n anchors times n points times a gcd on numbers up to the coordinate range (about log of the value, treat as small): O(n^2 log C) time, O(n) space for one Counter at a time. People say O(n^2); the gcd factor is small for 32-bit-size coordinates.

**Dry run:** points (1,1), (3,2), (5,3), (4,1), (2,3), (1,4); anchor (4,1).
- To (1,1): (-3, 0) -> (3, 0)/3 = (1, 0) after sign flip. To (3,2): (-1, 1) -> (1, -1). To (5,3): (1, 2). To (2,3): (-2, 2) -> (2, -2)/2 = (1, -1). To (1,4): (-3, 3) -> (1, -1).
- Direction (1, -1) has count 3, so 1 + 3 = 4: the points (4,1), (3,2), (2,3), (1,4).

**Code:**
```python
from math import gcd
from collections import Counter
import random

def brute(pts):                                    # O(n^3): for each pair, count points with zero cross product
    n = len(pts)
    if n <= 2: return n
    best = 2
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = pts[i], pts[j]
            c = sum((x2 - x1) * (y - y1) == (y2 - y1) * (x - x1) for x, y in pts)
            best = max(best, c)
    return best

def direction(dx, dy):                             # reduced, sign-normalised slope as an integer pair
    g = gcd(dx, dy)                                # gcd >= 0, and > 0 for distinct points
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
    return (dx, dy)                                # vertical line is (0, 1); horizontal is (1, 0)

def optimal(pts):                                  # O(n^2) time, O(n) space (distinct points)
    n = len(pts)
    if n <= 2: return n
    best = 1
    for i, (x0, y0) in enumerate(pts):
        c = Counter(direction(x - x0, y - y0) for j, (x, y) in enumerate(pts) if j != i)
        best = max(best, 1 + max(c.values()))      # anchor + the most common direction
    return best

for p, want in [([[1, 1], [2, 2], [3, 3]], 3),
                ([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]], 4)]:
    assert brute(p) == optimal(p) == want
print("examples:", optimal([[1, 1], [2, 2], [3, 3]]), optimal([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))

# why not floats: slopes (n-1)/n and n/(n+1) differ by about 1e-18, far below double precision
n = 10**9
fp = [[0, 0], [n, n - 1], [n + 1, n]]
print("not collinear: exact max =", brute(fp), "| optimal =", optimal(fp),
      "| float slopes equal:", (n - 1) / n == n / (n + 1))

rng = random.Random(49)
for _ in range(500):
    n = rng.randint(0, 10)
    s = set()
    while len(s) < n: s.add((rng.randint(-4, 4), rng.randint(-4, 4)))
    pts = [list(t) for t in s]
    assert brute(pts) == optimal(pts), pts
print("500 seeded cross-checks passed")

assert optimal([]) == 0 and optimal([[1, 1]]) == 1 and optimal([[1, 1], [2, 5]]) == 2
assert optimal([[3, 0], [3, 1], [3, 2], [4, 4]]) == 3              # vertical line
assert optimal([[0, 5], [1, 5], [2, 5], [-7, 5]]) == 4             # horizontal line, negative x
assert optimal([[0, 0], [1, 1], [-1, -1], [2, 2]]) == 4            # opposite directions share a normalised key
assert optimal([[0, 0], [1, 2], [2, 1], [3, 3]]) == 2              # two parallel-ish pairs, no triple
assert direction(-2, -4) == direction(2, 4) == (1, 2) and direction(0, -5) == (0, 1)
print("edge asserts passed")
```

**Output (my run):**
```text
examples: 3 4
not collinear: exact max = 2 | optimal = 2 | float slopes equal: True
500 seeded cross-checks passed
edge asserts passed
```

Both prompt examples are correct (3 and 4). The prompt says points are distinct; with duplicate points gcd(0, 0) = 0 would divide by zero, so you would count duplicates separately per anchor.

**Edge cases:**
- 0, 1 or 2 points: answer is n.
- Vertical line (dx = 0): key (0, 1), no divide by zero.
- Horizontal line: key (1, 0).
- Opposite directions from the anchor (left and right on the same line): sign normalisation merges them.
- Negative coordinates: `gcd` ignores sign, `//` on exact multiples is exact.
- Duplicate points (outside the stated constraints) need a duplicate counter.

**Follow-ups:**
- Why is the brute force exact but slow? Cross product is integer arithmetic, but it checks n points for each of n^2 pairs.
- Could you use `Fraction`? Yes (it normalises for you); it is slower per operation, and you still need vertical handled separately.
- Only look at points after the anchor? Yes, for j > i, since lines through earlier anchors were already counted; it halves the work.

**Common mistakes:**
- Float slope `dy / dx`: wrong for near-equal slopes and a crash at dx = 0.
- Not reducing by gcd, so (2, 4) and (1, 2) are different keys.
- Not normalising sign, so (-1, -2) and (1, 2) are different keys.
- Forgetting to add the anchor itself (answer off by one).
- Returning 0 or 1 for n = 2.

---

### Q50 ⭐ 🔴 Number of submatrices that sum to target. Given an m x n integer matrix (negatives allowed) and an integer target, count submatrices (contiguous rectangles) whose elements sum to target, in O(m^2 * n). Fix a pair of rows, collapse to a 1D array of column sums and reuse the subarray-sum-equals-k hashmap. Example: matrix=[[0,1,0],[1,1,1],[0,1,0]], target=0 -> 4.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Reduce 2D to 1D. Fix the top and bottom rows, collapse the rows between them into one array of column sums, then count subarrays summing to target with the prefix-sum hashmap (Subarray Sum Equals K).

**Say this first (1 line):** For each pair of rows keep running column sums, and run the 1D "count subarrays with sum k" hashmap on that array: O(m^2 * n).

**Brute force:** Build a 2D prefix-sum table, then test every rectangle with four corner lookups: O(m^2 n^2) time, O(mn) space.

**Optimal:**
- For each top row, start a column-sum array of zeros.
- For each bottom row from top downward, add that row into the column sums (O(n)).
- Now every rectangle with these top and bottom rows is a contiguous subarray of the column sums. Count subarrays with sum = target using a Counter of prefix sums seeded with {0: 1}: add `seen[pre - target]`, then record `pre`.
- The hashmap is needed because negatives break sliding windows and monotonic assumptions, same as the 1D problem.
- Pick the smaller dimension for the row pair loops: loop over pairs of the shorter side, so the cost is min(m, n)^2 * max(m, n).

**Complexity:** O(m^2 * n) time: m^2/2 row pairs, each does O(n) work for the update and O(n) average dict operations. Space O(n) for the column sums and the map. Brute is O(m^2 n^2).

**Dry run:** matrix [[0,1,0],[1,1,1],[0,1,0]], target 0.
- top=0, bottom=0: col = [0,1,0]. Start seen = {0: 1}.
  - v=0: pre=0, add seen[0] = 1 (subarray [0]); seen[0] becomes 2.
  - v=1: pre=1, add seen[1] = 0.
  - v=0: pre=1, add seen[1] = 1 (the last [0]). Count 2.
- Rows with a 1 in every column sum or any range crossing the middle column give sums >= 1: 0 more.
- top=2, bottom=2: col = [0,1,0] again: 2.
- Total 4: the four corner zeros.

**Code:**
```python
from collections import Counter
import random

def brute(mat, target):                            # O(m^2 n^2) with a 2D prefix-sum table
    m, n = len(mat), len(mat[0]) if mat else 0
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = mat[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    cnt = 0
    for r1 in range(m):
        for r2 in range(r1, m):
            for c1 in range(n):
                for c2 in range(c1, n):
                    s = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
                    cnt += s == target
    return cnt

def subarray_sum_k(arr, k):                        # the 1D hashmap routine: count subarrays with sum k
    seen, pre, cnt = Counter({0: 1}), 0, 0
    for v in arr:
        pre += v
        cnt += seen[pre - k]
        seen[pre] += 1
    return cnt

def optimal(mat, target):                          # O(m^2 * n) time, O(n) extra space (plus O(n) map)
    if not mat or not mat[0]: return 0
    m, n = len(mat), len(mat[0])
    total = 0
    for top in range(m):
        col = [0] * n                              # column sums of rows top..bottom
        for bottom in range(top, m):
            for j in range(n): col[j] += mat[bottom][j]
            total += subarray_sum_k(col, target)
    return total

ex = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
assert brute(ex, 0) == optimal(ex, 0) == 4
print("example target 0:", optimal(ex, 0), "| same matrix target 1:", optimal(ex, 1), "(brute", brute(ex, 1), ")")
ex2 = [[1, -1], [-1, 1]]
print("[[1,-1],[-1,1]] target 0:", optimal(ex2, 0), "(brute", brute(ex2, 0), ")")

rng = random.Random(50)
for _ in range(500):
    m, n = rng.randint(1, 5), rng.randint(1, 5)
    mat = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
    t = rng.randint(-4, 4)
    assert brute(mat, t) == optimal(mat, t), (mat, t)
print("500 seeded cross-checks passed (negatives included)")

assert optimal([], 0) == 0 and optimal([[]], 0) == 0
assert optimal([[5]], 5) == 1 and optimal([[5]], 4) == 0
assert optimal([[0] * 4 for _ in range(4)], 0) == (4 * 5 // 2) ** 2     # all zeros: every rectangle counts
assert optimal([[1, 2, 3]], 6) == 1                                       # single row degenerates to 1D
assert optimal([[1], [2], [3]], 5) == 1                                   # single column
assert optimal([[-1, -1], [-1, -1]], -2) == 4                             # negatives: 2 horizontal, 2 vertical
big = [[(i * 7 + j * 3) % 5 - 2 for j in range(60)] for i in range(60)]
print("60x60 pattern matrix, target 0:", optimal(big, 0))
print("edge asserts passed")
```

**Output (my run):**
```text
example target 0: 4 | same matrix target 1: 17 (brute 17 )
[[1,-1],[-1,1]] target 0: 5 (brute 5 )
500 seeded cross-checks passed (negatives included)
60x60 pattern matrix, target 0: 1577556
edge asserts passed
```

The prompt example is correct (4).

**Edge cases:**
- Empty matrix or empty rows: 0.
- Single row or column: reduces to the 1D problem.
- All zeros with target 0: every rectangle counts, (m(m+1)/2) * (n(n+1)/2).
- Negatives: handled by the hashmap; no window shrinking.
- Target not reachable: 0.

**Follow-ups:**
- Why seed the Counter with {0: 1}? So subarrays that start at index 0 are counted.
- Can you do better than O(m^2 n)? Not by this approach for general integers with negatives; it is the standard answer.
- What if values are non-negative? You can use a two-pointer window per row pair and skip the hash, still O(m^2 n).
- Space-time choice? 2D prefix sums are easier to explain, but O(m^2 n^2) and O(mn) space.

**Common mistakes:**
- Forgetting the {0: 1} seed.
- Updating the Counter before querying `pre - target` (wrong when target is 0).
- Rebuilding column sums from scratch for every row pair (O(m^3 n)).
- Looping over the longer dimension for pairs.
- Counting only maximal rectangles instead of all.
