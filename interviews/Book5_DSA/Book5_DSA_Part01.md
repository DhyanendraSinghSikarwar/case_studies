# Book 5 — Part 1: Arrays and hashing

**Topic:** Python DSA for product-company interviews: two-sum family and complement lookup, frequency counting, anagram grouping, duplicates and set membership, prefix and suffix products, subarray sums with a hashmap, longest consecutive sequence, top-k frequent, majority element and Boyer-Moore, in-place array rewrites (remove duplicates, move zeroes, rotate, next permutation), index-as-marker and matrix encoding tricks, hash-key design (tuples, sorted strings, counts), Python dict and set internals, collisions and ordering, Counter and defaultdict idioms, sorting versus hashing trade-offs, and concept-level notes on randomised hashing (Bloom filter)

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 16, ⭐⭐ 20, ⭐ 14)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns arrays, hash maps and hash sets, frequency counting, in-place array rewrites and the prefix-sum-plus-hashmap pattern in its basic form. Part 2 owns two pointers and sliding window; Part 3 strings (anagram and isomorphism questions here are about hashing, not string algorithms); Part 4 stacks, queues and monotonic stacks; Part 5 binary search; Part 6 linked lists; Part 7 trees; Part 8 heaps, intervals and greedy (no interval questions here; heaps appear only as the top-k alternative to bucket counting); Part 9 graphs; Parts 10 and 11 dynamic programming; Part 12 backtracking, tries and bit manipulation (the XOR question here is a prefix-hashmap question); Part 13 owns deep prefix sums, matrices and grids, math and randomised algorithms (this part uses prefix sums only with a hashmap and the Bloom filter only as a concept); Part 14 owns full design problems (LRU, LFU, rate limiter), so the randomised-set questions here are limited to the list-plus-dict trick. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part01_sources.md). No page was found that reports problems asked by a named company, so 'Asked at' tags name source types (public pattern lists, Indian placement and online-assessment prep sheets, commercial prep lists, Python internals explainers), not verified company reports, and company tags inside community sheets contradict each other. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only (sortedcontainers 2.4.0, hypothesis and pytest are installed in the sandbox but used only where a question says so).

---

### Q1 ⭐⭐⭐ 🟢 Contains duplicate. Given a list of integers `nums` (1 <= len <= 10^5, values in [-10^9, 10^9]), return True if any value appears at least twice, else False. Give the hash-set version, the sort-first version and say when each wins. Example: [1,2,3,1] -> True; [1,2,3,4] -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** Hash set for membership ("have I seen this?"). Sorting is the alternative: equal values become neighbours.

**Say this first (1 line):** "One pass with a set: the first value already in the set is a duplicate, O(n) time and O(n) space; if memory matters I sort and compare neighbours in O(n log n) with O(1) extra space."

**Brute force:** Compare every pair. O(n^2) time, O(1) space. At n = 10^5 that is about 5 x 10^9 comparisons. Too slow.

**Optimal:**
- Walk the list. If `x` is already in `seen`, return True. Otherwise add it.
- Invariant: before step i, `seen` holds exactly the distinct values of `nums[:i]`, and none of them repeated (or we would have returned).
- Set lookup and insert are O(1) on average.
- Early exit is a real win: the answer is often found before the end.

**Complexity:**
| Version | Time | Extra space |
|---|---|---|
| Pairs | O(n^2) | O(1) |
| Hash set | O(n) average, O(n^2) worst case if hashes collide badly (not for ints in practice) | O(n) |
| Sort then scan | O(n log n) | O(1) with `nums.sort()` in place, O(n) with `sorted` (Timsort needs up to n/2 temp space anyway) |

**When each wins:**
- Set: default. Fastest on random data and exits early.
- Sort: memory is tight, or the data is already sorted (Timsort is O(n) on sorted input), or you are allowed to mutate the input.
- Say this out loud: the sort version is not "free space"; it changes the caller's list if you sort in place.

**Dry run:** `[1,2,3,1]`
| x | in seen? | seen after |
|---|---|---|
| 1 | no | {1} |
| 2 | no | {1,2} |
| 3 | no | {1,2,3} |
| 1 | yes | return True |

**Code:**
```python
import random


def dup_brute(nums):
    n = len(nums)
    return any(nums[i] == nums[j] for i in range(n) for j in range(i + 1, n))


def dup_set(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def dup_len(nums):
    return len(set(nums)) != len(nums)


def dup_sort(nums):
    s = sorted(nums)  # copy, input untouched; use nums.sort() for O(1) extra if allowed
    return any(s[i] == s[i + 1] for i in range(len(s) - 1))


print("example 1:", dup_set([1, 2, 3, 1]), "(expected True)")
print("example 2:", dup_set([1, 2, 3, 4]), "(expected False)")

random.seed(1)
for _ in range(500):
    a = [random.randint(-6, 6) for _ in range(random.randint(0, 9))]
    b = dup_brute(a)
    assert dup_set(a) == b == dup_len(a) == dup_sort(a), a
print("cross-check: 500 seeded cases agree")

assert dup_set([]) is False
assert dup_set([7]) is False
assert dup_set([5, 5]) is True
assert dup_set([-10**9, 10**9]) is False
assert dup_set([0, 0, 0]) is True
assert dup_sort([2, 1, 2]) is True
print("edge asserts passed")
```

**Output (my run):**
```text
example 1: True (expected True)
example 2: False (expected False)
cross-check: 500 seeded cases agree
edge asserts passed
```

Both prompt examples are correct as written ([1,2,3,1] gives True, [1,2,3,4] gives False).

**Edge cases:**
- Empty list or one element: False.
- Two equal values: True.
- Extremes -10^9 and 10^9: Python ints, no overflow, nothing special.
- All equal: True at the second element.

**Follow-ups:**
- Duplicates within distance k? Keep a dict value -> last index, or a set of the last k values (sliding window, Part 2 territory).
- Duplicates within a value difference? Needs buckets or a sorted structure (Contains duplicate III).
- One-liner? `len(set(nums)) != len(nums)`. Clean, but it always builds the whole set; no early exit.

**Common mistakes:**
- Sorting `nums` in place and not saying the caller's list changed.
- Claiming the sort version is O(1) space while using `sorted()`.
- Adding to the set before checking (always True).
- Calling the hash version O(n) worst case without the word "average".

### Q2 ⭐⭐⭐ 🟢 Two Sum. Given `nums` and an integer `target`, return the indices (i, j), i != j, of two elements whose sum is target; exactly one valid pair is guaranteed and you may not reuse an element. Explain the complement lookup and why inserting after the check is safe for equal values. Example: nums=[2,7,11,15], target=9 -> (0,1); nums=[3,3], target=6 -> (0,1).
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Complement lookup in a hash map: for each x, ask "have I already seen target - x?"

**Say this first (1 line):** "One pass, a dict from value to index; for each element I look up target minus it before inserting it, so O(n) time and O(n) space."

**Brute force:** Try every pair (i, j). O(n^2) time, O(1) space.

**Optimal:**
- `seen` maps value -> index for elements to the left of j.
- At j, the partner must be `target - nums[j]`. If it is in `seen`, we are done.
- Else store `nums[j]`.
- Invariant: `seen` only contains indices < j, so any hit is a different element.
- Why insert after the check is safe for equal values: for [3,3], target 6. At j=0 we look up 3, miss, then store 3->0. At j=1 we look up 3, hit index 0, return (0,1). If we inserted first, a single 3 would find itself and give (0,0), which reuses an element.
- Duplicates overwrite the stored index with the latest one. That is harmless here: if the pair uses a duplicated value, the second copy finds the first one before it overwrites it; and the prompt guarantees a single valid pair, so no other pairing is ever lost.

**Complexity:** Time O(n) average (n lookups and inserts, each O(1) average). Space O(n) for the dict.

**Dry run:** `[2,7,11,15]`, target 9
| j | x | need | seen before | action |
|---|---|---|---|---|
| 0 | 2 | 7 | {} | miss, store 2->0 |
| 1 | 7 | 2 | {2:0} | hit, return (0,1) |

**Code:**
```python
import random


def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum(nums, target):
    seen = {}  # value -> index of an earlier element
    for j, x in enumerate(nums):
        i = seen.get(target - x)
        if i is not None:
            return (i, j)
        seen[x] = j  # insert AFTER the check: an element never pairs with itself
    return None


print("example 1:", two_sum([2, 7, 11, 15], 9), "(expected (0, 1))")
print("example 2:", two_sum([3, 3], 6), "(expected (0, 1))")
print("single 3, target 6:", two_sum([3], 6), "(no pair, element not reused)")

random.seed(2)
cases = 0
for _ in range(1000):
    n = random.randint(2, 9)
    a = [random.randint(-5, 5) for _ in range(n)]
    i, j = random.sample(range(n), 2)
    t = a[i] + a[j]
    # the prompt guarantees exactly one pair; skip inputs with several valid pairs
    pairs = [(p, q) for p in range(n) for q in range(p + 1, n) if a[p] + a[q] == t]
    if len(pairs) != 1:
        continue
    cases += 1
    assert two_sum(a, t) == two_sum_brute(a, t) == pairs[0], (a, t)
print("cross-check: %d seeded unique-pair cases agree" % cases)

# with several valid pairs both may differ in WHICH pair they return, but both must be valid
for _ in range(500):
    a = [random.randint(-3, 3) for _ in range(random.randint(2, 8))]
    t = random.randint(-6, 6)
    r1, r2 = two_sum(a, t), two_sum_brute(a, t)
    assert (r1 is None) == (r2 is None)
    if r1:
        assert r1[0] != r1[1] and a[r1[0]] + a[r1[1]] == t
print("validity check on inputs with many pairs: ok")

assert two_sum([3, 3], 6) == (0, 1)
assert two_sum([3, 2, 4], 6) == (1, 2)  # 3 + 3 would reuse index 0
assert two_sum([0, 4, 3, 0], 0) == (0, 3)
assert two_sum([-1, -2, -3, -4, -5], -8) == (2, 4)
assert two_sum([5], 10) is None
print("edge asserts passed")
```

**Output (my run):**
```text
example 1: (0, 1) (expected (0, 1))
example 2: (0, 1) (expected (0, 1))
single 3, target 6: None (no pair, element not reused)
cross-check: 506 seeded unique-pair cases agree
validity check on inputs with many pairs: ok
edge asserts passed
```

Both prompt examples are correct as written.

**Edge cases:**
- Equal values forming the pair ([3,3]).
- Target needs the same value twice but it appears once ([3], target 6): must return nothing.
- Zeros and negatives: the dict does not care.
- Several valid pairs: the brute force and the one-pass may return different valid pairs; the prompt rules this out, but in an interview ask.

**Follow-ups:**
- Return values, not indices, and input is sorted? Two pointers, O(1) space (Part 2).
- All unique pairs? Sort plus two pointers, or a set of seen values with a set of pairs.
- Stream of numbers, many queries? Keep the dict, same lookup.

**Common mistakes:**
- Inserting before checking, which pairs an element with itself.
- Building the full dict first and then looking up, without checking `index != j`.
- Returning values instead of indices.
- Sorting first and losing the original indices.

### Q3 ⭐⭐⭐ 🟢 Valid anagram. Given two strings s and t of lowercase English letters (up to 5*10^4 chars), decide whether t is a rearrangement of s. Solve with a fixed 26-slot count array and with Counter, then answer the follow-up: what changes if inputs are arbitrary Unicode. Example: s='listen', t='silent' -> True; s='rat', t='car' -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** Frequency counting. Two strings are anagrams exactly when every character has the same count in both.

**Say this first (1 line):** "Same length, then one pass adding for s and subtracting for t in a 26-slot array; all zeros means anagram. O(n) time, O(1) space for lowercase letters."

**Brute force:** `sorted(s) == sorted(t)`. O(n log n) time, O(n) space. Simple and a fine first answer, and I use it as the checker.

**Optimal:**
- If lengths differ, return False at once.
- `cnt[ord(c) - 97]` is +1 for each char of s and -1 for each char of t.
- Invariant: after processing i pairs, `cnt[k]` = (count of letter k in s[:i]) - (count in t[:i]). At the end all zeros means equal multisets.
- With equal lengths, no need to check "any negative" separately: the counts sum to zero, so all-zero is the only success.
- `Counter(s) == Counter(t)` is the same idea with a dict.

**Complexity:** Time O(n). Space O(26) = O(1) for the array. `Counter` is O(k) where k is the number of distinct characters (O(1) for lowercase; up to O(n) for Unicode).

**Dry run:** `s='rat'`, `t='car'`
| step | s char | t char | non-zero slots |
|---|---|---|---|
| 1 | r +1 | c -1 | r:+1, c:-1 |
| 2 | a +1 | a -1 | r:+1, c:-1 |
| 3 | t +1 | r -1 | t:+1, c:-1 |
Non-zero slots remain, so False.

**Code:**
```python
import random
import string
from collections import Counter


def anagram_brute(s, t):
    return sorted(s) == sorted(t)


def anagram_array(s, t):
    if len(s) != len(t):
        return False
    cnt = [0] * 26
    for a, b in zip(s, t):
        cnt[ord(a) - 97] += 1
        cnt[ord(b) - 97] -= 1
    return not any(cnt)


def anagram_counter(s, t):
    # works for any Unicode string: Counter keys are code points
    return len(s) == len(t) and Counter(s) == Counter(t)


print("listen/silent:", anagram_array("listen", "silent"), "(expected True)")
print("rat/car:", anagram_array("rat", "car"), "(expected False)")

random.seed(3)
for _ in range(1000):
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
    if random.random() < 0.5:
        t = list(s)
        random.shuffle(t)
        t = "".join(t)
    else:
        t = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
    b = anagram_brute(s, t)
    assert anagram_array(s, t) == b == anagram_counter(s, t), (s, t)
print("cross-check: 1000 seeded cases agree")

assert anagram_array("", "") is True
assert anagram_array("a", "a") is True
assert anagram_array("ab", "a") is False
assert anagram_array("aab", "abb") is False
big = "".join(random.choice(string.ascii_lowercase) for _ in range(50000))
shuf = list(big)
random.shuffle(shuf)
assert anagram_array(big, "".join(shuf)) is True

# Unicode: the 26-slot array breaks (ord - 97 can be negative or huge); Counter is fine
try:
    anagram_array("\u00e9a", "a\u00e9")
except IndexError:
    print("26-slot array on e-acute: IndexError (ord 233 - 97 = 136, out of range)")
# worse: a char whose index lands in -26..-1 wraps silently (negative list index)
print("26-slot array on '[' vs 'u' (wrong True):", anagram_array("[", "u"))
print("Counter on Unicode:", anagram_counter("naïve", "ïvena"), anagram_counter("éa", "ae"))
# combining characters: same text, different code points
a, b = "é", "é"
print("precomposed vs combining look equal but len:", len(a), len(b), "Counter equal:", anagram_counter(a, b))
import unicodedata
print("after NFC normalisation:", anagram_counter(unicodedata.normalize("NFC", a), unicodedata.normalize("NFC", b)))
print("edge asserts passed")
```

**Output (my run):**
```text
listen/silent: True (expected True)
rat/car: False (expected False)
cross-check: 1000 seeded cases agree
26-slot array on e-acute: IndexError (ord 233 - 97 = 136, out of range)
26-slot array on '[' vs 'u' (wrong True): True
Counter on Unicode: True False
precomposed vs combining look equal but len: 1 2 Counter equal: False
after NFC normalisation: True
edge asserts passed
```

Both prompt examples are correct as written.

**Unicode follow-up (what changes):**
- The 26-slot array breaks. `ord(c) - 97` can be out of range (IndexError), or worse a negative index in -26..-1 wraps around silently and gives a wrong True (see the `'['` vs `'u'` line above).
- Use `Counter` (a dict keyed by code point). Space becomes O(k) distinct characters.
- Mind normalisation: "e-acute" as one code point and "e" plus a combining accent are the same text but different code points. Normalise (NFC) first if the product wants them equal.
- Also decide case and whitespace rules; ask.

**Edge cases:**
- Both empty: True.
- Different lengths: False immediately.
- Same letters, different counts ("aab" vs "abb"): False.
- n = 5 x 10^4: trivial for O(n).

**Follow-ups:**
- One string is a long text and t is a pattern (find all anagram windows)? Sliding window with counts, Part 2 or 3.
- Group many words? See Group anagrams (Q9 in this part).
- Why not compare the sums of ords? Collisions: "ad" and "bc" have the same sum.

**Common mistakes:**
- Forgetting the length check: `zip` stops at the shorter string, so "ab" vs "abc" would wrongly return True.
- Using a sum or product of characters as the key.
- Assuming 26 slots for Unicode input.
- `Counter(s) - Counter(t)` empty does not prove equality when t has extra letters; compare both ways or use `==`.

### Q4 ⭐⭐⭐ 🟢 Majority element. An integer list of length n (1 <= n <= 5*10^4) is guaranteed to contain a value that appears more than n/2 times. Return it in O(n) time. Show the Counter solution and the Boyer-Moore voting solution with O(1) space and explain why the vote pairing argument works. Example: [2,2,1,1,1,2,2] -> 2.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** Frequency counting, then Boyer-Moore voting (pair off different values; the majority survives).

**Say this first (1 line):** "A Counter works in O(n) time and O(n) space; Boyer-Moore gets O(n) time and O(1) space because a value with more than half the votes cannot be cancelled out by all the others."

**Brute force:** For each element count its occurrences. O(n^2) time, O(1) space.

**Optimal (Boyer-Moore):**
- Keep `cand` and `votes`.
- If `votes == 0`, take the current element as the candidate.
- If x equals `cand`, votes + 1, else votes - 1.
- Why the pairing argument works: every time we decrement, we cancel one copy of `cand` against one different element. Think of removing a pair of different values. The majority has more than n/2 copies, so it cannot be fully cancelled: each removed pair takes at most one majority copy, and all other values together are fewer than n/2.
- Careful: this is a proof for "a majority exists". If it might not exist, add a second pass to verify `count(cand) > n // 2`.

**Complexity:**
| Version | Time | Space |
|---|---|---|
| Counter | O(n) average | O(n) |
| Boyer-Moore | O(n) | O(1) |
| Sorting, take `nums[n//2]` | O(n log n) | O(1) to O(n) |

**Dry run:** `[2,2,1,1,1,2,2]`
| x | cand before | votes before | cand, votes after |
|---|---|---|---|
| 2 | None | 0 | 2, 1 |
| 2 | 2 | 1 | 2, 2 |
| 1 | 2 | 2 | 2, 1 |
| 1 | 2 | 1 | 2, 0 |
| 1 | 2 | 0 | 1, 1 (new candidate) |
| 2 | 1 | 1 | 1, 0 |
| 2 | 1 | 0 | 2, 1 |
End: candidate 2. Note the candidate flipped to 1 mid-way, and only the end matters.

**Code:**
```python
import random
from collections import Counter


def majority_brute(nums):
    n = len(nums)
    for x in nums:
        if sum(1 for y in nums if y == x) > n // 2:
            return x


def majority_counter(nums):
    return Counter(nums).most_common(1)[0][0]


def majority_boyer_moore(nums):
    cand, votes = None, 0
    for x in nums:
        if votes == 0:
            cand = x
        votes += 1 if x == cand else -1
    return cand  # valid only because a majority is GUARANTEED


def majority_verified(nums):
    cand = majority_boyer_moore(nums)
    return cand if nums.count(cand) > len(nums) // 2 else None  # second pass if not guaranteed


print("example:", majority_boyer_moore([2, 2, 1, 1, 1, 2, 2]), "(expected 2)")
print("counts:", dict(Counter([2, 2, 1, 1, 1, 2, 2])), "-> 2 appears 4 > 7//2 = 3")

random.seed(4)
for _ in range(1000):
    n = random.randint(1, 11)
    m = n // 2 + 1  # build an input that has a strict majority
    v = random.randint(-3, 3)
    a = [v] * random.randint(m, n)
    a += [random.randint(-3, 3) for _ in range(n - len(a))]
    random.shuffle(a)
    if a.count(v) <= n // 2:
        continue
    exp = majority_brute(a)
    assert majority_boyer_moore(a) == majority_counter(a) == exp == v, a
print("cross-check: 1000 seeded guaranteed-majority cases agree")

# without the guarantee Boyer-Moore returns a candidate, not a proof
no_maj = [1, 2, 3]
print("no majority [1,2,3]: candidate =", majority_boyer_moore(no_maj), "verified =", majority_verified(no_maj))

assert majority_boyer_moore([5]) == 5
assert majority_boyer_moore([3, 3]) == 3
assert majority_boyer_moore([1, 2, 1]) == 1
assert majority_boyer_moore([-1, -1, 2, 2, -1]) == -1
assert majority_boyer_moore([7] * 5) == 7
assert majority_verified([1, 2, 3]) is None
print("edge asserts passed")
```

**Output (my run):**
```text
example: 2 (expected 2)
counts: {2: 4, 1: 3} -> 2 appears 4 > 7//2 = 3
cross-check: 1000 seeded guaranteed-majority cases agree
no majority [1,2,3]: candidate = 3 verified = None
edge asserts passed
```

The prompt example is correct (2 appears 4 times out of 7, and 4 > 3).

**Edge cases:**
- n = 1: that element.
- Exactly half is NOT a majority (needs strictly more than n/2).
- No guarantee: Boyer-Moore returns some candidate, so verify with a second pass (shown above for [1,2,3]).
- Negative values and all-equal arrays: fine.

**Follow-ups:**
- Elements appearing more than n/3 times? At most 2 such values; keep two candidates and two counters, then verify both.
- Stream where you cannot store data? Boyer-Moore is the streaming answer.
- Why is votes not "the count of cand"? It is a surplus, not a count.

**Common mistakes:**
- Using `>= n/2` instead of `> n/2`.
- Skipping the verification pass when the problem does not guarantee a majority.
- Resetting the candidate when votes hits 0 only after processing the element (off-by-one); check `votes == 0` before counting x.
- Thinking `votes` equals the candidate's frequency.

### Q5 ⭐⭐⭐ 🟢 Move zeroes. Given a list `nums`, move every 0 to the end in place while keeping the relative order of the non-zero values, using O(1) extra space and as few writes as you can. Example: [0,1,0,3,12] -> [1,3,12,0,0]; [0] -> [0].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Read/write pointers (a stable in-place filter). Not really hashing; it is the first in-place array rewrite of this part.

**Say this first (1 line):** "One read pointer, one write pointer; every non-zero goes to the write slot in order, then the tail is zeros. O(n) time, O(1) space; I swap only when the pointers differ to keep writes minimal."

**Brute force:** Build `[x for x in nums if x] + zeros` and copy back. O(n) time but O(n) extra space, so it breaks the O(1) rule. Repeated `pop`/`append(0)` or `remove(0)` in a loop is O(n^2) because each `list.pop(i)` shifts the tail.

**Optimal:**
- `w` is the next slot for a non-zero. Invariant: `nums[:w]` holds the non-zero values seen so far, in original order.
- For each `r`, if `nums[r] != 0`, put it at `w` and advance `w`.
- Swap version: `swap(nums[w], nums[r])` when `r != w`. After a swap, the zero lands at r, ahead of the read pointer, so nothing is lost and no second pass is needed.
- Order of non-zeros is preserved because r only moves forward and w never passes r.

**Complexity:** Time O(n), one pass. Space O(1). Writes: the swap version does at most 2 per non-zero that moved, and none when the array has no zero before the element (an array with no zeros does 0 writes). The two-pass version always writes every non-zero plus every trailing zero.

**Dry run:** `[0,1,0,3,12]` (swap version)
| r | nums[r] | w | action | array |
|---|---|---|---|---|
| 0 | 0 | 0 | skip | [0,1,0,3,12] |
| 1 | 1 | 0 | swap(0,1), w=1 | [1,0,0,3,12] |
| 2 | 0 | 1 | skip | [1,0,0,3,12] |
| 3 | 3 | 1 | swap(1,3), w=2 | [1,3,0,0,12] |
| 4 | 12 | 2 | swap(2,4), w=3 | [1,3,12,0,0] |

**Code:**
```python
import random


def move_zeroes_brute(nums):
    # extra space: build a new list, then copy back
    non = [x for x in nums if x != 0]
    non += [0] * (len(nums) - len(non))
    nums[:] = non


def move_zeroes(nums):
    w = 0  # next slot for a non-zero value; nums[:w] are all non-zero, in order
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[w] = nums[r]
            w += 1
    for i in range(w, len(nums)):
        nums[i] = 0


def move_zeroes_swap(nums):
    # one pass, swaps only when needed (skips self-writes when no zero seen yet)
    w = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            if r != w:
                nums[w], nums[r] = nums[r], nums[w]
            w += 1


a = [0, 1, 0, 3, 12]
move_zeroes(a)
print("example 1:", a, "(expected [1, 3, 12, 0, 0])")
b = [0]
move_zeroes(b)
print("example 2:", b, "(expected [0])")

random.seed(5)
for _ in range(1000):
    x = [random.choice([0, 0, 1, 2, -3]) for _ in range(random.randint(0, 10))]
    e, f, g = x[:], x[:], x[:]
    move_zeroes_brute(e)
    move_zeroes(f)
    move_zeroes_swap(g)
    assert e == f == g, x
print("cross-check: 1000 seeded cases agree")

# count writes: two-pass writes (#nonzero + #trailing zeros), swap version writes only when r != w
def writes_swap(nums):
    w = 0
    cnt = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            if r != w:
                cnt += 2  # a swap touches two slots
            w += 1
    return cnt


sample = [1, 2, 3, 0, 4]
print("swap writes on [1,2,3,0,4]:", writes_swap(sample), "| two-pass writes:", 4 + 1)
print("swap writes on all non-zero [1,2,3]:", writes_swap([1, 2, 3]))

for case in ([], [0, 0, 0], [1, 2, 3], [5], [0, 0, 1], [-1, 0, -2]):
    c = case[:]
    move_zeroes(c)
    d = case[:]
    move_zeroes_swap(d)
    assert c == d == [v for v in case if v] + [0] * case.count(0)
print("edge asserts passed")
```

**Output (my run):**
```text
example 1: [1, 3, 12, 0, 0] (expected [1, 3, 12, 0, 0])
example 2: [0] (expected [0])
cross-check: 1000 seeded cases agree
swap writes on [1,2,3,0,4]: 2 | two-pass writes: 5
swap writes on all non-zero [1,2,3]: 0
edge asserts passed
```

Both prompt examples are correct as written.

**Edge cases:**
- Empty list, a single 0, all zeros, no zeros (the `r != w` guard means no writes at all).
- Negative numbers are non-zero; do not test `> 0`.
- `0.0` and `False` are `== 0` in Python; mention it if the list may hold floats or bools.

**Follow-ups:**
- Move zeroes to the front? Scan from the right with the same idea.
- Minimise writes even more? The swap version already writes only moved elements.
- Partition by another predicate, keeping stability? Same pattern; stable partition needs care, the two-pointer swap-from-both-ends version is not stable.

**Common mistakes:**
- Swapping without the `r != w` check is still correct but does wasteful self-swaps.
- Returning a new list when the task says in place.
- Using `nums.remove(0)` or `pop(i)` in a loop: O(n^2).
- Rebinding `nums = ...` inside the function, which does not change the caller's list; use `nums[:] = ...` or index writes.

### Q6 ⭐⭐⭐ 🟢 Remove duplicates from a sorted array in place. `nums` is sorted non-decreasing; rewrite it so the first k positions hold the distinct values in order and return k; contents beyond k do not matter. Explain the read/write pointer invariant. Example: [0,0,1,1,1,2,2,3,3,4] -> k=5 and the prefix [0,1,2,3,4].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Read/write pointers on a sorted array (equal values are adjacent, so "new value" means "different from the last kept one").

**Say this first (1 line):** "Sorted means duplicates are neighbours; a write pointer marks the end of the distinct prefix, and I copy `nums[r]` forward whenever it differs from `nums[w-1]`. O(n) time, O(1) space."

**Brute force:** `sorted(set(nums))` or build a new list of distinct values and copy back: O(n) time but O(n) extra space (and `set` plus `sorted` costs O(n log n)). Deleting duplicates with `del nums[i]` or `pop(i)` in a loop is O(n^2).

**Optimal:**
- `w` = length of the distinct prefix. Start with `w = 1` because the first element is always kept.
- For `r` from 1: if `nums[r] != nums[w-1]`, write it to `nums[w]` and `w += 1`.
- Invariant: `nums[:w]` is the sorted list of distinct values of `nums[:r+1]`; `w <= r + 1` so we never overwrite something unread.
- Comparing with `nums[w-1]` (last kept) rather than `nums[r-1]` is equivalent on sorted input, and generalises to "keep at most 2" variants.

**Complexity:** Time O(n), one pass. Space O(1).

**Dry run:** `[0,0,1,1,1,2,2,3,3,4]`
| r | nums[r] | last kept | action | w |
|---|---|---|---|---|
| 1 | 0 | 0 | same, skip | 1 |
| 2 | 1 | 0 | write nums[1]=1 | 2 |
| 3,4 | 1 | 1 | skip | 2 |
| 5 | 2 | 1 | write nums[2]=2 | 3 |
| 6 | 2 | 2 | skip | 3 |
| 7 | 3 | 2 | write nums[3]=3 | 4 |
| 8 | 3 | 3 | skip | 4 |
| 9 | 4 | 3 | write nums[4]=4 | 5 |
Result k=5, prefix [0,1,2,3,4].

**Code:**
```python
import random


def remove_dups_brute(nums):
    out = []
    for x in nums:
        if not out or out[-1] != x:
            out.append(x)
    nums[:len(out)] = out  # extra O(n) space
    return len(out)


def remove_dups(nums):
    if not nums:
        return 0
    w = 1  # nums[:w] = distinct values so far, strictly increasing
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:
            nums[w] = nums[r]
            w += 1
    return w


a = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k = remove_dups(a)
print("example:", "k =", k, "prefix =", a[:k], "(expected k=5, [0, 1, 2, 3, 4])")

random.seed(6)
for _ in range(1000):
    x = sorted(random.randint(-4, 4) for _ in range(random.randint(0, 12)))
    e, f = x[:], x[:]
    k1 = remove_dups_brute(e)
    k2 = remove_dups(f)
    assert k1 == k2 == len(set(x)), x
    assert e[:k1] == f[:k2] == sorted(set(x)), x
print("cross-check: 1000 seeded sorted cases agree")

for case, exp in (([], 0), ([7], 1), ([2, 2], 1), ([1, 2, 3], 3), ([5, 5, 5, 5], 1), ([-3, -3, 0, 0, 4], 3)):
    c = case[:]
    k = remove_dups(c)
    assert k == exp and c[:k] == sorted(set(case)), case
print("edge asserts passed")

# the tail is unspecified: show it is left as junk, not cleaned
b = [1, 1, 2]
kb = remove_dups(b)
print("tail left as is:", b, "k =", kb)
```

**Output (my run):**
```text
example: k = 5 prefix = [0, 1, 2, 3, 4] (expected k=5, [0, 1, 2, 3, 4])
cross-check: 1000 seeded sorted cases agree
edge asserts passed
tail left as is: [1, 2, 2] k = 2
```

The prompt example is correct as written.

**Edge cases:**
- Empty list: return 0 (guard before reading `nums[0]`).
- One element, or all equal: k = 1.
- All distinct: no writes change anything.
- Beyond k the contents are junk (see the last print); do not rely on them.

**Follow-ups:**
- Allow each value at most twice? Compare with `nums[w-2]` instead and start `w = 2`.
- Input not sorted? Use a set (O(n) space), or sort first (O(n log n)); the order-preserving unsorted version needs the set.
- Return the list rather than k? `nums[:k]` is a copy.

**Common mistakes:**
- Forgetting the empty-list guard.
- Comparing `nums[r]` with `nums[w]` (a stale slot) instead of `nums[w-1]`.
- Returning the last index instead of the count.
- Assuming it works on unsorted input.

### Q7 ⭐⭐⭐ 🟢 Intersection of two arrays. Given two integer lists a and b, return the distinct values present in both (any order). Then do the multiset variant where a value appears min(count in a, count in b) times. Example: a=[1,2,2,1], b=[2,2] -> distinct [2], multiset [2,2].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Hash set for "is it in both?", Counter for "how many times in both?" (the multiset version takes the minimum count).

**Say this first (1 line):** "Distinct: `set(a) & set(b)`. Multiset: count one list, walk the other, and take a value only while its remaining count is positive. O(n + m) time."

**Brute force:** For each x in a, scan b (`x in b`). O(n x m). For the multiset version, `b.remove(x)` on a copy is also O(m) per element.

**Optimal:**
- Distinct version: build `set(a)`, then keep the values of `set(b)` found in it (the `&` operator does this, iterating the smaller set). O(n + m) average.
- Multiset version: `ca = Counter(a)`. For each x in b: if `ca[x] > 0`, output x and decrement. Invariant: `ca[x]` = copies of x in a not yet matched to a copy in b. The output count for x is min(count_a, count_b).
- `Counter(a) & Counter(b)` does the same and `.elements()` expands it.
- Space: the set version holds both sets, O(n + m). The multiset version holds one Counter, O(n); count the shorter list to make it O(min(n, m)).

**Complexity:** Time O(n + m) average. Space as above. Output order is "any" for the distinct version because sets are unordered; I sort only to compare in the test.

**Dry run:** a=[1,2,2,1], b=[2,2], multiset
| x in b | ca before | take? | ca after |
|---|---|---|---|
| 2 | {1:2, 2:2} | yes | 2:1 |
| 2 | {1:2, 2:1} | yes | 2:0 |
Output [2, 2]. Distinct version: {1,2} & {2} = {2}.

**Code:**
```python
import random
from collections import Counter


def inter_brute(a, b):
    return sorted({x for x in a if x in b})  # `in` on a list is O(len(b)) -> O(n*m)


def inter_multi_brute(a, b):
    b = list(b)
    out = []
    for x in a:
        if x in b:
            b.remove(x)  # O(m) each
            out.append(x)
    return sorted(out)


def inter_set(a, b):
    return sorted(set(a) & set(b))


def inter_multi(a, b):
    ca = Counter(a)
    out = []
    for x in b:
        if ca[x] > 0:
            out.append(x)
            ca[x] -= 1
    return sorted(out)


def inter_multi_counter_and(a, b):
    return sorted((Counter(a) & Counter(b)).elements())  # & takes min of counts


print("distinct:", inter_set([1, 2, 2, 1], [2, 2]), "(expected [2])")
print("multiset:", inter_multi([1, 2, 2, 1], [2, 2]), "(expected [2, 2])")

random.seed(7)
for _ in range(1000):
    a = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    b = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    assert inter_set(a, b) == inter_brute(a, b), (a, b)
    m = inter_multi_brute(a, b)
    assert inter_multi(a, b) == m == inter_multi_counter_and(a, b), (a, b)
print("cross-check: 1000 seeded cases agree")

# the asymmetry matters: swapping inputs must give the same multiset
assert inter_multi([1, 1, 1], [1]) == inter_multi([1], [1, 1, 1]) == [1]
assert inter_set([], [1]) == [] and inter_multi([], []) == []
assert inter_set([4, 4], [4]) == [4]
assert inter_multi([4, 9, 5], [9, 4, 9, 8, 4]) == [4, 9]
assert inter_set([1, 2], [3, 4]) == []
print("edge asserts passed")
```

**Output (my run):**
```text
distinct: [2] (expected [2])
multiset: [2, 2] (expected [2, 2])
cross-check: 1000 seeded cases agree
edge asserts passed
```

Both prompt examples are correct as written.

**Edge cases:**
- Either list empty: empty result.
- No overlap: empty result.
- Heavy duplicates in one list only: the multiset version caps at the smaller count (the swap assert).
- Negative values: nothing special.

**Follow-ups:**
- Both lists already sorted? Two pointers, O(1) extra space, O(n + m).
- One list is tiny, the other huge and on disk? Put the tiny one in a Counter and stream the big one.
- Both too big for memory? External sort, or hash-partition both lists into buckets that fit and intersect per bucket.

**Common mistakes:**
- Using `a` as a list for membership tests (`x in list` is O(n)).
- Returning duplicates from the distinct version.
- In the multiset version, forgetting to decrement, which counts too many.
- Assuming the set result is ordered.

### Q8 ⭐⭐⭐ 🟢 Missing number. `nums` holds n distinct integers from the range 0..n, so exactly one value of that range is absent. Return it three ways: hash set, sort, and the arithmetic sum formula; say what happens to the sum approach in languages with fixed-width ints and why Python is unaffected. Example: [3,0,1] -> 2; [0,1] -> 2.
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Hash set for membership, and a math identity (expected sum minus actual sum) when the range is known. Same family as "index as marker" ideas later in this part.

**Say this first (1 line):** "The values are 0..n with one gone, so expected sum is n(n+1)/2; subtract the actual sum and the difference is the missing value. O(n) time, O(1) space, and Python ints cannot overflow."

**Brute force / alternatives:**
- Hash set: put everything in a set, then test v = 0..n. O(n) time, O(n) space.
- Sort: after sorting, the first index i with `nums[i] != i` is the answer; if none, the answer is n. O(n log n) time, O(1) to O(n) space.
- Checking `v in nums` for each v with a list is O(n^2).

**Optimal (sum formula):**
- The list has n values out of n + 1 possible (0..n). The full sum is n(n+1)/2.
- Missing = full sum - `sum(nums)`.
- Invariant behind it: the values are distinct and inside 0..n, so the only difference between the full range and the list is the one absent value.
- Use `//` (integer division). `n * (n + 1)` is always even, so this is exact.

**Complexity:**
| Version | Time | Extra space |
|---|---|---|
| Set | O(n) | O(n) |
| Sort | O(n log n) | O(1) (in place) or O(n) |
| Sum | O(n) | O(1) |

**Overflow point:**
- In C, C++ or Java with 32-bit ints, n(n+1)/2 exceeds 2^31 - 1 once n reaches about 65,536, and the n * (n+1) product overflows even earlier (about n = 46,341). The run above shows n = 10^5: the true sum 5,000,050,000 wraps to 705,082,704 as an int32.
- Fixes there: use 64-bit, or accumulate `missing ^= i ^ nums[i]` (XOR, no overflow) or `missing += i - nums[i]` starting from n (the differences stay small and cancel as you go).
- Python ints have arbitrary precision, so the sum is exact at any size (cost: big ints are slower and larger than machine ints, but at this size, irrelevant).

**Dry run:** `[3,0,1]`, n = 3
- Full sum = 3 x 4 / 2 = 6.
- Actual sum = 4.
- Missing = 2.

**Code:**
```python
import random


def missing_set(nums):
    s = set(nums)
    for v in range(len(nums) + 1):
        if v not in s:
            return v


def missing_sort(nums):
    s = sorted(nums)
    for i, v in enumerate(s):
        if v != i:
            return i
    return len(s)


def missing_sum(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


print("example 1:", missing_sum([3, 0, 1]), "(expected 2)")
print("example 2:", missing_sum([0, 1]), "(expected 2)")

random.seed(8)
for _ in range(1000):
    n = random.randint(0, 12)
    full = list(range(n + 1))
    miss = random.choice(full)
    a = [v for v in full if v != miss]
    random.shuffle(a)
    assert missing_set(a) == missing_sort(a) == missing_sum(a) == miss, a
print("cross-check: 1000 seeded cases agree")

assert missing_sum([]) == 0 and missing_set([]) == 0 and missing_sort([]) == 0
assert missing_sum([1]) == 0 and missing_sum([0]) == 1
assert missing_sort([0, 1, 2, 3]) == 4
# large n: Python ints never overflow, the sum stays exact
n = 10**6
big = list(range(n + 1))
big.remove(123456)
assert missing_sum(big) == 123456
print("n = 10**6 sum formula exact:", missing_sum(big))
# what a 32-bit language would see: n*(n+1)/2 for n=10**5 is 5000050000 > 2**31-1
n32 = 10**5
total = n32 * (n32 + 1) // 2
wrapped = (total + 2**31) % 2**32 - 2**31  # simulate signed 32-bit wrap
print("n=10**5: true sum", total, "| as signed int32", wrapped, "| int32 max", 2**31 - 1)
print("edge asserts passed")
```

**Output (my run):**
```text
example 1: 2 (expected 2)
example 2: 2 (expected 2)
cross-check: 1000 seeded cases agree
n = 10**6 sum formula exact: 123456
n=10**5: true sum 5000050000 | as signed int32 705082704 | int32 max 2147483647
edge asserts passed
```

Both prompt examples are correct as written ([3,0,1] gives 2, [0,1] gives 2).

**Edge cases:**
- Empty list: n = 0, the range is {0}, answer 0.
- Missing value is n (the top of the range): sort version needs the fall-through `return len(s)`.
- Missing value is 0.
- n = 1: [0] -> 1, [1] -> 0.

**Follow-ups:**
- Two values missing? Sum plus sum of squares gives two equations, or partition by the XOR of the two missing values (bit trick, Part 12).
- A duplicate and a missing in 1..n? Index marking or sum plus sum of squares.
- Why not XOR here? It is the overflow-safe equivalent; mention it, do not detail it.

**Common mistakes:**
- Using `n * (n + 1) / 2` (float division) and returning a float.
- Assuming the range is 1..n when it is 0..n.
- Forgetting the answer can be n (sorted scan falls through).
- Saying the sum trick fails in Python; it does not.

### Q9 ⭐⭐⭐ 🟡 Group anagrams. Given a list of lowercase strings, group together the strings that are anagrams of one another; output order does not matter. Compare keying a dict by the sorted string against keying by a 26-count tuple and state the cost of each in terms of word length L. Example: ['eat','tea','tan','ate','nat','bat'] -> [['eat','tea','ate'],['tan','nat'],['bat']] in any order.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Hash-key design. Find a canonical form that is the same for all anagrams and use it as the dict key.

**Say this first (1 line):** "Key a dict by a canonical form of each word: the sorted string costs O(L log L), the 26-count tuple costs O(L); append each word to its key's list. Total O(n x L log L) or O(n x L)."

**Brute force:** For each word, compare against the first word of every existing group by sorting both. Worst case n groups, so O(n^2 x L log L).

**Optimal:**
- Two interchangeable keys:
  - Sorted string: `"".join(sorted(w))`. "eat", "tea", "ate" all give "aet".
  - Count tuple: 26 counts. Must be a tuple (hashable), not a list.
- `defaultdict(list)` collects words per key. Return `list(d.values())`.
- Invariant: two words share a key if and only if they have identical letter multisets, so each dict value is exactly one anagram class.
- Why not a sum or product of letters as the key: different words collide ("ad" vs "bc").

**Complexity (n words, max length L):**
| Key | Per word | Total time | Space |
|---|---|---|---|
| Sorted string | O(L log L) to sort | O(n L log L) | O(n L) for keys and groups |
| 26-count tuple | O(L) to count + O(26) to hash | O(n (L + 26)) = O(n L) | O(n L) for groups plus O(26 n) for keys |

- The count key wins asymptotically for long words. For short words (L under about 10 to 20) sorting is often faster in CPython, because `sorted` and `join` run in C while the counting loop is Python-level. The two sandbox timing lines above show both sides (long words: count key faster; short words: sorted key faster). They are sandbox measurements, not proof; the big-O comes from the code.
- The count key only works because the alphabet is fixed at 26. For Unicode use `tuple(sorted(Counter(w).items()))` or just the sorted string.

**Dry run:** `['eat','tea','tan','ate','nat','bat']`
| word | key (sorted) | dict after |
|---|---|---|
| eat | aet | aet:[eat] |
| tea | aet | aet:[eat,tea] |
| tan | ant | + ant:[tan] |
| ate | aet | aet:[eat,tea,ate] |
| nat | ant | ant:[tan,nat] |
| bat | abt | + abt:[bat] |

**Code:**
```python
import random
import string
from collections import defaultdict


def group_brute(words):
    # O(n^2 * L log L): compare each word against each existing group's first word
    groups = []
    for w in words:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return groups


def group_sorted_key(words):
    d = defaultdict(list)
    for w in words:
        d["".join(sorted(w))].append(w)  # O(L log L) per word
    return list(d.values())


def group_count_key(words):
    d = defaultdict(list)
    for w in words:
        cnt = [0] * 26
        for ch in w:  # O(L) per word to build, O(26) to hash the tuple
            cnt[ord(ch) - 97] += 1
        d[tuple(cnt)].append(w)  # a list is unhashable, a tuple is fine
    return list(d.values())


def norm(groups):
    return sorted(sorted(g) for g in groups)


ex = ["eat", "tea", "tan", "ate", "nat", "bat"]
print("sorted key:", group_sorted_key(ex))
print("count key :", group_count_key(ex))
print("example ok (any order):", norm(group_sorted_key(ex)) == norm([["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]))

random.seed(9)
for _ in range(1000):
    ws = ["".join(random.choice("abc") for _ in range(random.randint(0, 4))) for _ in range(random.randint(0, 8))]
    e = norm(group_brute(ws))
    assert norm(group_sorted_key(ws)) == e == norm(group_count_key(ws)), ws
print("cross-check: 1000 seeded cases agree")

assert group_sorted_key([]) == []
assert norm(group_sorted_key([""])) == [[""]]
assert norm(group_count_key(["a"])) == [["a"]]
assert norm(group_sorted_key(["", ""])) == [["", ""]]
assert norm(group_count_key(["ab", "ba", "ab"])) == [["ab", "ab", "ba"]]
assert norm(group_sorted_key(["abc", "def"])) == [["abc"], ["def"]]
# duplicates kept, not merged
assert sum(len(g) for g in group_sorted_key(["x", "x", "x"])) == 3
print("edge asserts passed")

# sandbox-only timing, long words (big-O comes from the code, not from this)
import time
L = 20000
words = ["".join(random.choice(string.ascii_lowercase) for _ in range(L)) for _ in range(50)]
for f in (group_sorted_key, group_count_key):
    t = time.perf_counter()
    f(words)
    print(f.__name__, "50 words of length 20000 (sandbox only): %.3fs" % (time.perf_counter() - t))
short = ["".join(random.choice(string.ascii_lowercase) for _ in range(6)) for _ in range(100000)]
for f in (group_sorted_key, group_count_key):
    t = time.perf_counter()
    f(short)
    print(f.__name__, "100000 words of length 6 (sandbox only): %.3fs" % (time.perf_counter() - t))
```

**Output (my run):**
```text
sorted key: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
count key : [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
example ok (any order): True
cross-check: 1000 seeded cases agree
edge asserts passed
group_sorted_key 50 words of length 20000 (sandbox only): 0.095s
group_count_key 50 words of length 20000 (sandbox only): 0.035s
group_sorted_key 100000 words of length 6 (sandbox only): 0.061s
group_count_key 100000 words of length 6 (sandbox only): 0.169s
```

The prompt example is correct: the groups are [eat, tea, ate], [tan, nat], [bat], with groups appearing in first-seen order here (the prompt says any order is fine).

**Edge cases:**
- Empty list: empty result. Empty string: it is its own group (key is empty).
- Repeated words stay in the output (a group may contain the same word twice).
- Words of different lengths never share a key.
- A list as a dict key raises `TypeError: unhashable type`.

**Follow-ups:**
- Unicode or large alphabet? Sorted string, or a sorted tuple of (char, count).
- Reduce key size? A string like "1a0b..." or a tuple with only the non-zero entries, a sparse count.
- Do I need to sort the count tuple? No, the fixed-position 26-tuple is already canonical.

**Common mistakes:**
- Using a list as the key.
- Using sum of ords as the key (collisions).
- Calling the sorted-string key O(n L) without the log factor.
- Claiming the count key is always faster in practice.

### Q10 ⭐⭐⭐ 🟡 Top K frequent elements. Given integers `nums` and k, return the k most frequent values (any order; the answer is unique). Beat O(n log n) by giving both a heap solution (O(n log k)) and a bucket-by-frequency solution (O(n)). Example: nums=[1,1,1,2,2,3], k=2 -> [1,2].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Frequency counting, then top-k selection: a size-k min-heap, or bucket sort by frequency because a frequency is at most n.

**Say this first (1 line):** "Count with a Counter, then either keep a min-heap of size k over the distinct values for O(n log k), or drop values into buckets indexed by frequency and read from the top for O(n)."

**Brute force:** Count, then sort the distinct values by frequency and take k. O(n log n) in the worst case (all values distinct). It is correct and often fine; the prompt asks to beat it.

**Optimal:**
- Step 1, both versions: `Counter(nums)`, O(n).
- Heap: push `(freq, value)` for each distinct value; when the heap holds k and a new item has a higher frequency than the root, `heapreplace`. `heapq` is a min-heap, so the root is the weakest of the current top k. At the end the heap holds the k most frequent. Cost: O(m log k) for m distinct values, m <= n.
- Bucket: `buckets[f]` = values with frequency f, for f in 1..n. Scan f from n down to 1 and collect until you have k. Frequency is an integer in 1..n, so no comparison sort is needed.
- Invariant (bucket): after the scan from n down to f, the output holds the most frequent values in descending frequency order.
- `heapq.nlargest(k, cnt, key=cnt.get)` is the one-line heap version.

**Complexity:**
| Version | Time | Space |
|---|---|---|
| Sort | O(n log n) | O(m) |
| Heap of size k | O(n + m log k) | O(m) for the Counter plus O(k) heap |
| Bucket | O(n) | O(n) |

Both need the Counter (O(m)). The heap adds only O(k); the bucket list adds O(n) slots.

**Dry run:** `nums=[1,1,1,2,2,3]`, k=2
- Counter: {1:3, 2:2, 3:1}.
- Buckets: [ [], [3], [2], [1], [], [], [] ] (index 0 to 6).
- Scan f = 6 down: empty until f = 3 gives 1, f = 2 gives 2. Now 2 items collected, stop. Answer [1, 2].
- Heap version: push (3,1), push (2,2); then (1,3) does not beat the root (2,2); result {1,2}.

**Code:**
```python
import heapq
import random
from collections import Counter


def topk_brute(nums, k):
    # sort distinct values by frequency: O(n log n)
    return [v for v, _ in sorted(Counter(nums).items(), key=lambda p: -p[1])[:k]]


def topk_heap(nums, k):
    cnt = Counter(nums)
    h = []  # min-heap of (freq, value), size <= k: the root is the weakest of the current top k
    for v, c in cnt.items():
        if len(h) < k:
            heapq.heappush(h, (c, v))
        elif c > h[0][0]:
            heapq.heapreplace(h, (c, v))
    return [v for _, v in h]


def topk_bucket(nums, k):
    cnt = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]  # index = frequency, 1..n
    for v, c in cnt.items():
        buckets[c].append(v)
    out = []
    for c in range(len(nums), 0, -1):
        for v in buckets[c]:
            out.append(v)
            if len(out) == k:
                return out
    return out


def topk_nlargest(nums, k):
    cnt = Counter(nums)
    return heapq.nlargest(k, cnt, key=cnt.get)


print("heap  :", sorted(topk_heap([1, 1, 1, 2, 2, 3], 2)), "(expected [1, 2])")
print("bucket:", sorted(topk_bucket([1, 1, 1, 2, 2, 3], 2)), "(expected [1, 2])")

random.seed(10)
cases = 0
for _ in range(1000):
    n = random.randint(1, 14)
    a = [random.randint(-4, 4) for _ in range(n)]
    cnt = Counter(a)
    # prompt guarantees a unique answer: frequency of k-th and (k+1)-th must differ
    freqs = sorted(cnt.values(), reverse=True)
    
    k = random.randint(1, len(freqs))
    if k < len(freqs) and freqs[k - 1] == freqs[k]:
        continue
    cases += 1
    exp = sorted(topk_brute(a, k))
    assert sorted(topk_heap(a, k)) == exp == sorted(topk_bucket(a, k)) == sorted(topk_nlargest(a, k)), (a, k)
print("cross-check: %d seeded unique-answer cases agree" % cases)

assert topk_heap([1], 1) == [1] == topk_bucket([1], 1)
assert sorted(topk_bucket([4, 4, 4, 4], 1)) == [4]
assert sorted(topk_heap([-1, -1, 2, 2, 2, 3], 1)) == [2]
assert sorted(topk_bucket([5, 6, 7, 5, 6, 5], 3)) == [5, 6, 7]
# k equal to number of distinct values returns everything, even with ties
assert sorted(topk_heap([1, 2, 3], 3)) == [1, 2, 3] == sorted(topk_bucket([1, 2, 3], 3))
print("edge asserts passed")
```

**Output (my run):**
```text
heap  : [1, 2] (expected [1, 2])
bucket: [1, 2] (expected [1, 2])
cross-check: 502 seeded unique-answer cases agree
edge asserts passed
```

The prompt example is correct as written.

**Edge cases:**
- k equals the number of distinct values: return everything.
- All values equal: one bucket entry.
- Ties at the boundary make the answer non-unique; the prompt rules that out. In an interview, ask what to do on ties.
- Negative values: they are only dict keys, so fine.
- n = 1.

**Follow-ups:**
- Top k from a stream or very large data? Count-min sketch or Space-Saving for approximate counts; exact needs all counts in memory or external aggregation.
- Why is bucket O(n) and not O(n log n)? Because the sort key is a small integer (at most n); this is a counting sort.
- Return the k least frequent? Same code, scan buckets upward or use a max-heap.

**Common mistakes:**
- Pushing every element (not every distinct value) onto the heap.
- Using `heapq` as if it were a max-heap (it is a min-heap): keep a min-heap of size k and compare against the root.
- Making `n` buckets and indexing with frequency n (off-by-one: need n + 1).
- Calling `Counter.most_common(k)` "O(n)": it uses `heapq.nlargest` for a given k, so it is O(n log k)-ish, not linear.

### Q11 ⭐⭐⭐ 🟡 Product of array except self. For each index i return the product of all other elements without using division and in O(n) time; extra space beyond the output list should be O(1). Handle zeros. Example: [1,2,3,4] -> [24,12,8,6]; [-1,1,0,-3,3] -> [0,0,9,0,0].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Prefix and suffix products (two passes). The answer for i is "everything left of i" times "everything right of i". No division needed, so zeros are harmless.

**Say this first (1 line):** One left-to-right pass writes the product of everything before each index into the output; one right-to-left pass multiplies in the product of everything after, using a single running variable.

**Brute force:** For each i, multiply all other elements. O(n^2) time, O(1) extra. Too slow for large n.

**Optimal:**
- Pass 1: `out[i] = product of nums[0..i-1]`. Keep a running `left`, start at 1.
- Pass 2 from the right: `out[i] *= product of nums[i+1..]`. Keep a running `right`, start at 1.
- The output list does not count as extra space, so this is O(1) extra.
- Division approach (total product / nums[i]) is banned, and it breaks on zeros anyway.
- Zeros need no special case: a zero lands inside `left` or `right` for every other index and zeroes them. The index of the zero itself gets the product of the rest.

**Complexity:** Time O(n): two passes. Extra space O(1) beyond the output: two scalars. (The brute force is O(n^2).)

**Dry run:** `[1,2,3,4]`
- Pass 1 (left products): out = [1, 1, 2, 6].
- Pass 2 (right running value 1, then 4, 12, 24): i=3: 6*1=6, right=4. i=2: 2*4=8, right=12. i=1: 1*12=12, right=24. i=0: 1*24=24.
- Result [24, 12, 8, 6].

**Code:**
```python
import random
from math import prod

def brute(nums):
    return [prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]

def optimal(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):          # out[i] = product of everything left of i
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):   # multiply in product of everything right of i
        out[i] *= right
        right *= nums[i]
    return out

assert optimal([1, 2, 3, 4]) == [24, 12, 8, 6]
assert optimal([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert optimal([0, 0, 2]) == [0, 0, 0]
assert optimal([5]) == [1]          # empty product is 1
assert optimal([2, 3]) == [3, 2]
assert optimal([0, 4]) == [4, 0]
assert optimal([]) == []

rng = random.Random(11)
for _ in range(500):
    a = [rng.randint(-4, 4) for _ in range(rng.randint(0, 8))]
    assert optimal(a) == brute(a), a
print("500 random cases agree with brute force")
print(optimal([1, 2, 3, 4]), optimal([-1, 1, 0, -3, 3]), optimal([0, 0, 2]), optimal([5]))
```

**Output (my run):**
```
500 random cases agree with brute force
[24, 12, 8, 6] [0, 0, 9, 0, 0] [0, 0, 0] [1]
```

**Edge cases:**
- Single element: answer is `[1]` (empty product). Say it out loud.
- One zero: only that index is non-zero. Two or more zeros: everything is 0 (`[0,0,2]` gives all zeros).
- Negatives: sign handled naturally by multiplication.
- Large values: Python ints do not overflow. In fixed-width languages mention overflow.

**Follow-ups:**
- *Why not division?* Banned by the prompt, and zeros make it fail. You would need to count zeros separately.
- *Can you do it with prefix and suffix arrays?* Yes, simpler to explain but O(n) extra. The running-variable version removes it.
- *What if only a modulus of the product is wanted?* Same two passes with `% m`; division would need a modular inverse and fails for zero residues.

**Common mistakes:**
- Updating `left` before writing `out[i]` (off by one: includes nums[i]).
- Starting the running products at 0 instead of 1.
- Using the total product divided by nums[i] and crashing on zero.
- Claiming O(1) space but allocating separate prefix and suffix lists.

---

### Q12 ⭐⭐⭐ 🟡 Longest consecutive sequence. Given an unsorted list of integers, return the length of the longest run of values that are consecutive integers (x, x+1, x+2, ...), regardless of position, in O(n) expected time. Explain why starting only from values whose predecessor is absent keeps it linear. Example: [100,4,200,1,3,2] -> 4 (the run 1,2,3,4); [0,3,7,2,5,8,4,6,0,1] -> 9.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Hash set membership. A set gives O(1) "is x present", so you can walk a run without sorting. The trick is to start walks only at run starts.

**Say this first (1 line):** Put everything in a set; for each value whose predecessor x-1 is not in the set, count upward x+1, x+2 while present; each run is walked once, so it is linear.

**Brute force:**
- Sort and scan, tracking the current run: O(n log n).
- Or from every value walk upward in a set: O(n) per start, O(n^2) worst case (for a fully consecutive list, every start re-walks its tail).

**Optimal:**
- Build `s = set(nums)`. Duplicates vanish.
- For each x in s: if `x-1 in s`, skip. It is inside a run that another value will start.
- Otherwise x is a run start. Walk `x+1, x+2, ...` while in s. Length = end - x.
- Why linear: a value is walked over only as part of the run whose start is unique, since every run has exactly one start. Total inner-loop steps across all starts is at most the number of distinct values. Outer loop is n. Total O(n) expected (hash lookups are O(1) on average).

**Complexity:** Time O(n) expected: set build n, outer loop n, inner steps sum to at most n. Space O(n) for the set. Sorting alternative is O(n log n) time, O(1) to O(n) space depending on whether you may modify the input.

**Dry run:** `[100,4,200,1,3,2]`, set = {100,4,200,1,3,2}.
- 100: 99 absent, start. 101 absent, length 1.
- 4: 3 present, skip.
- 200: 199 absent, start, length 1.
- 1: 0 absent, start. 2,3,4 present, 5 absent. Length 4.
- 3 and 2: predecessor present, skip.
- Answer 4.

**Code:**
```python
import random

def brute(nums):
    s = set(nums)
    best = 0
    for x in s:                      # try every value as a start, walk up
        y = x
        while y in s:
            y += 1
        best = max(best, y - x)
    return best

def optimal(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:               # not a run start, skip
            continue
        y = x + 1
        while y in s:
            y += 1
        best = max(best, y - x)
    return best

assert optimal([100, 4, 200, 1, 3, 2]) == 4
assert optimal([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert optimal([]) == 0
assert optimal([7]) == 1
assert optimal([5, 5, 5]) == 1
assert optimal([-2, -1, 0, 1]) == 4
assert optimal([10**9, -10**9]) == 1
assert optimal([1, 3, 5, 7]) == 1
assert optimal(list(range(100000))) == 100000

rng = random.Random(12)
for _ in range(500):
    a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 15))]
    assert optimal(a) == brute(a), a
# independent oracle: sort and scan
def by_sort(nums):
    u = sorted(set(nums))
    best = cur = 0
    for i, v in enumerate(u):
        cur = cur + 1 if i and v == u[i - 1] + 1 else 1
        best = max(best, cur)
    return best
for _ in range(500):
    a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 15))]
    assert optimal(a) == by_sort(a)
print("1000 random cases agree")
print(optimal([100, 4, 200, 1, 3, 2]), optimal([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
```

**Output (my run):**
```
1000 random cases agree
4 9
```

**Edge cases:**
- Empty list gives 0. Single value gives 1.
- Duplicates must not inflate the count (`[5,5,5]` is 1). The set handles it.
- Negatives and large values (`-2..1` is length 4; 10^9 and -10^9 are not consecutive).
- Iterate over the set, not the list, so a list with many duplicates does not repeat work.

**Follow-ups:**
- *Union-find version?* Union x with x+1 if present and track the biggest component. Also near-linear, more code.
- *Why is the skip check enough?* Each maximal run has exactly one element with no predecessor.
- *Worst-case hash behaviour?* Expected O(n) assumes a decent hash spread; with many colliding keys a set degrades toward O(n) per lookup. Mention it, do not dwell on it.

**Common mistakes:**
- Skipping the predecessor check: it still passes small tests but is O(n^2) on a long run. Tell the interviewer you know this.
- Looping over `nums` with duplicates and re-walking.
- Sorting and forgetting to de-duplicate (a repeat resets or double-counts the run).
- Returning the largest value in the run rather than its length.

---

### Q13 ⭐⭐⭐ 🟡 Subarray sum equals k. Given integers `nums` (negatives allowed, len up to 2*10^4) and an integer k, count the contiguous subarrays whose sum is exactly k. Use prefix sums with a hashmap of how many times each prefix has occurred and explain why a sliding window fails with negatives. Example: nums=[1,1,1], k=2 -> 2; nums=[1,2,3], k=3 -> 2.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Prefix sum plus hashmap of counts. Subarray `(i, j]` sums to k exactly when `prefix[j] - prefix[i] = k`.

**Say this first (1 line):** Keep a running prefix sum and a dict of how many times each prefix has occurred; at every position add `seen[prefix - k]` to the answer, then record the current prefix.

**Brute force:** Two loops over start and end with a running sum. O(n^2) time, O(1) space. With n up to 2*10^4 that is about 2*10^8 steps, too slow in Python.

**Optimal:**
- Seed `seen[0] = 1`: the empty prefix, so subarrays that start at index 0 are counted.
- For each x: `pref += x`; `ans += seen[pref - k]`; then `seen[pref] += 1`.
- Look up before inserting, so a subarray of length zero is never counted (matters when k = 0).
- Why a count and not a set: several earlier starts can share a prefix value and each is a different subarray.
- Why sliding window fails with negatives: it assumes extending the window only increases the sum and shrinking only decreases it. With negatives that is false, so you cannot decide whether to move the left or the right edge. Example below: `[1,-1,1]`, k=1.

**Complexity:** Time O(n): one pass, average O(1) dict operations. Space O(n) for the dict in the worst case (all prefixes distinct).

**Dry run:** `[1,2,3]`, k=3. seen={0:1}, pref=0, ans=0.
- x=1: pref=1, seen[-2]=0, ans=0. seen={0:1,1:1}.
- x=2: pref=3, seen[0]=1, ans=1 (that is [1,2]). seen has 3:1.
- x=3: pref=6, seen[3]=1, ans=2 (that is [3]). Answer 2.

**Code:**
```python
import random
from collections import defaultdict

def brute(nums, k):
    n, cnt = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == k:
                cnt += 1
    return cnt

def optimal(nums, k):
    seen = defaultdict(int)
    seen[0] = 1                      # empty prefix
    pref = cnt = 0
    for x in nums:
        pref += x
        cnt += seen[pref - k]        # look up BEFORE inserting current prefix
        seen[pref] += 1
    return cnt

def sliding_window_wrong(nums, k):   # valid only for non-negative values
    lo = s = cnt = 0
    for hi, x in enumerate(nums):
        s += x
        while s > k and lo <= hi:
            s -= nums[lo]; lo += 1
        if s == k:
            cnt += 1
    return cnt

assert optimal([1, 1, 1], 2) == 2
assert optimal([1, 2, 3], 3) == 2
assert optimal([], 0) == 0
assert optimal([0, 0, 0], 0) == 6          # all subarrays of zeros
assert optimal([1, -1, 0], 0) == 3
assert optimal([5], 5) == 1
assert optimal([-1, -1, 1], 0) == 1
assert optimal([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4

rng = random.Random(13)
for _ in range(500):
    a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 10))]
    k = rng.randint(-4, 4)
    assert optimal(a, k) == brute(a, k), (a, k)
print("500 random cases agree with brute force")
print("sliding window on [1,-1,1], k=1:", sliding_window_wrong([1, -1, 1], 1), "but truth is", optimal([1, -1, 1], 1))
print(optimal([1, 1, 1], 2), optimal([1, 2, 3], 3))
```

**Output (my run):**
```
500 random cases agree with brute force
sliding window on [1,-1,1], k=1: 2 but truth is 3
2 2
```

**Edge cases:**
- Empty list: 0 (even for k = 0, no non-empty subarray).
- All zeros with k = 0: n(n+1)/2 subarrays, `[0,0,0]` gives 6. Needs the count dict, not a set.
- Negative k and negative values are fine.
- Single element equal to k.

**Follow-ups:**
- *Non-negative values only?* A sliding window works in O(1) space. State why it relies on monotonic sums.
- *Return the longest such subarray?* Store the first index of each prefix instead of a count.
- *Why defaultdict reads are safe here?* Reading `seen[pref-k]` inserts a zero entry in a defaultdict. It does not change the answer, but it grows memory; `seen.get(pref-k, 0)` avoids it.

**Common mistakes:**
- Forgetting `seen[0] = 1`.
- Inserting the current prefix before the lookup (breaks k = 0).
- Using a set, which loses multiplicities.
- Trying sliding window with negatives.

---

### Q14 ⭐⭐⭐ 🟡 Rotate array in place. Rotate `nums` to the right by k steps (k can exceed len) using O(1) extra space. Give the three-reversal method, state why k must be reduced modulo n, and mention the slice-assignment one-liner and its extra space. Example: nums=[1,2,3,4,5,6,7], k=3 -> [5,6,7,1,2,3,4].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** In-place array transformation by reversal. Rotating right by k is the same as reverse all, reverse the first k, reverse the rest.

**Say this first (1 line):** Reduce k modulo n, then reverse the whole list, reverse the first k items, reverse the remaining n-k: O(n) time, O(1) extra space.

**Brute force:** Rotate by one step k times (pop the last, insert at front): O(n*k) time. Or copy into a new list at index `(i+k) % n`: O(n) time but O(n) space.

**Optimal:**
- `k %= n`. Rotating by n returns the original list, so only k mod n matters; this also stops k > n from indexing out of range, and avoids pointless work when k is huge.
- Reverse everything: `[1..7]` becomes `[7,6,5,4,3,2,1]`.
- Reverse positions 0..k-1: `[5,6,7,4,3,2,1]`. Reverse positions k..n-1: `[5,6,7,1,2,3,4]`.
- Why it works: the last k items must go to the front in their original order. The full reversal puts them in front but backwards; the second reversal fixes their order, the third fixes the rest.
- Guard n = 0 before the modulo (modulo by zero raises ZeroDivisionError).

**Complexity:** Time O(n): every element is swapped a constant number of times (about 2 writes each). Space O(1): two indices. Slice one-liner `nums[:] = nums[-k:] + nums[:-k]` is also O(n) time but builds temporary lists, so O(n) extra space; and the `nums[:] =` part matters, because `nums = ...` rebinds the local name and does not change the caller's list.

**Dry run:** `[1,2,3,4,5,6,7]`, k=3.
- Reverse all: [7,6,5,4,3,2,1].
- Reverse first 3: [5,6,7,4,3,2,1].
- Reverse last 4: [5,6,7,1,2,3,4].

**Code:**
```python
import random

def brute(nums, k):
    n = len(nums)
    if n == 0:
        return []
    k %= n
    out = nums[:]
    for _ in range(k):               # rotate one step at a time
        out.insert(0, out.pop())
    return out

def rev(a, i, j):
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1; j -= 1

def optimal(nums, k):                # in place, returns the same list
    n = len(nums)
    if n == 0:
        return nums
    k %= n
    rev(nums, 0, n - 1)
    rev(nums, 0, k - 1)
    rev(nums, k, n - 1)
    return nums

def slice_version(nums, k):          # builds a temp copy: O(n) extra space
    n = len(nums)
    if n:
        k %= n
        nums[:] = nums[-k:] + nums[:-k] if k else nums[:]
    return nums

a = [1, 2, 3, 4, 5, 6, 7]
assert optimal(a, 3) == [5, 6, 7, 1, 2, 3, 4]
assert optimal([1, 2], 5) == [2, 1]          # k > n
assert optimal([1, 2, 3], 3) == [1, 2, 3]    # k == n
assert optimal([1, 2, 3], 0) == [1, 2, 3]
assert optimal([], 4) == []
assert optimal([9], 100) == [9]
assert slice_version([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]
# the classic bug: nums[-k:] when k == 0 returns the WHOLE list
print("nums[-0:] =", [1, 2, 3][-0:], "so the k == 0 guard matters")

rng = random.Random(14)
for _ in range(500):
    arr = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
    k = rng.randint(0, 25)
    assert optimal(arr[:], k) == brute(arr, k) == slice_version(arr[:], k), (arr, k)
print("500 random cases agree")
print(optimal([1, 2, 3, 4, 5, 6, 7], 3))
```

**Output (my run):**
```
nums[-0:] = [1, 2, 3] so the k == 0 guard matters
500 random cases agree
[5, 6, 7, 1, 2, 3, 4]
```

**Edge cases:**
- k = 0, k = n, k a multiple of n: list unchanged.
- k > n (`[1,2]`, k=5 gives `[2,1]`).
- Empty and single-element list.
- The slice trap: `nums[-0:]` is the whole list, so slice code needs a guard for `k == 0` (shown in the run).

**Follow-ups:**
- *Rotate left instead?* Reverse the first k, reverse the rest, reverse all. Or use `k = n - k % n`.
- *Cycle-leader method?* Move elements along gcd(n,k) cycles, one write per element, also O(1) space.
- *Use `collections.deque.rotate`?* Fine if the data lives in a deque already; O(k).

**Common mistakes:**
- Skipping `k %= n`.
- Returning a new list when the prompt says in place.
- Off-by-one on the reversal boundaries (k-1 and k).
- `nums = nums[-k:] + nums[:-k]` which does not mutate the caller's list.

---

### Q15 ⭐⭐⭐ 🟡 Valid Sudoku. Given a 9x9 board of characters (digits 1-9 or '.' for empty), decide whether the filled cells so far break no rule: no repeated digit in any row, column or 3x3 box (you do not have to solve it). Show how to key sets by (row), (col) and (row//3, col//3) in one pass. Example: a board with two '5' in the first row -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Set-per-group membership in one pass. A cell is a clash if its digit is already in its row set, column set or box set.

**Say this first (1 line):** Walk the 81 cells once, keep 9 row sets, 9 column sets and a dict of box sets keyed by `(r//3, c//3)`, and return False the moment a digit is already in any of its three sets.

**Brute force:** For each of 9 rows, 9 columns and 9 boxes extract the cells and compare `len(digits)` to `len(set(digits))`. Three separate sweeps, 243 cell reads. Also correct and still O(1) because the board is fixed at 81 cells.

**Optimal:**
- Skip '.' cells.
- Box key `(r // 3, c // 3)` maps the 9 cells of a 3x3 box to one key (or use `r//3*3 + c//3`).
- Check all three sets before adding, then add to all three.
- The board size is fixed, so the time is O(81) = O(1); for an N x N generalisation it is O(N^2) time and O(N^2) space.
- You are only validating the filled cells; a valid board may still be unsolvable.

**Complexity:** Time O(81), constant (O(N^2) for the general board). Space O(81) for the sets, constant.

**Dry run:** Take the classic puzzle row 0 `5 3 . . 7 . . . .` then change cell (0,2) to '5'.
- (0,0)='5': row0={5}, col0={5}, box(0,0)={5}.
- (0,1)='3': added to its sets.
- (0,2)='5': `'5' in rows[0]` is True, return False.

**Code:**
```python
import random

def brute(board):
    def ok(cells):
        d = [c for c in cells if c != '.']
        return len(d) == len(set(d))
    for i in range(9):
        if not ok(board[i]) or not ok([board[r][i] for r in range(9)]):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if not ok([board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]):
                return False
    return True

def optimal(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = {}
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == '.':
                continue
            b = boxes.setdefault((r // 3, c // 3), set())
            if v in rows[r] or v in cols[c] or v in b:
                return False
            rows[r].add(v); cols[c].add(v); b.add(v)
    return True

base = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
        "7...2...6", ".6....28.", "...419..5", "....8..79"]
good = [list(r) for r in base]
assert optimal(good) and brute(good)

bad_row = [list(r) for r in base]; bad_row[0][2] = '5'          # two 5s in row 0
bad_col = [list(r) for r in base]; bad_col[8][0] = '5'          # 5 twice in col 0
assert not optimal(bad_row) and not optimal(bad_col)
empty = [['.'] * 9 for _ in range(9)]
assert optimal(empty)

# the example in the prompt: a board with two '5' in the first row
assert optimal(bad_row) is False
# ok-looking trap: a rows-and-cols-only check misses a box clash
box_only = [['.'] * 9 for _ in range(9)]
box_only[0][0] = '7'; box_only[1][1] = '7'
assert optimal(box_only) is False

rng = random.Random(15)
agree = 0
for _ in range(500):
    b = [['.'] * 9 for _ in range(9)]
    for _ in range(rng.randint(0, 30)):
        b[rng.randrange(9)][rng.randrange(9)] = str(rng.randint(1, 9))
    assert optimal(b) == brute(b)
    agree += 1
print(agree, "random boards agree with brute force")
print(optimal(good), optimal(bad_row), optimal(bad_col), optimal(box_only))
```

**Output (my run):**
```
500 random boards agree with brute force
True False False False
```

**Edge cases:**
- All empty board is valid.
- Clash only inside a box (two 7s at (0,0) and (1,1)), which a rows-and-columns-only check misses.
- A clash only in a column.
- Digits are characters, so `'5'` and `5` differ if you mix types.

**Follow-ups:**
- *Solve it?* Backtracking with the same three structures, usually with bitmasks per row, column and box (Book 5 backtracking part).
- *Use bitmasks?* One integer per group, `mask & (1 << d)`; faster, less readable.
- *Why not one set of tuples?* Store `(row, d)`, `(col, d)`, `(box, d)` in one set; it works and is a neat single-set trick.

**Common mistakes:**
- Wrong box key (`r//3 + c//3` collides: (0,3) and (3,0) both give 1).
- Treating '.' as a digit and reporting duplicate dots.
- Checking only rows and columns.
- Believing a valid board is solvable.

---

### Q16 ⭐⭐⭐ 🔴 First missing positive. Given an unsorted integer list (negatives and duplicates allowed), return the smallest positive integer that is not in it, in O(n) time and O(1) extra space beyond the input (you may modify it). Explain the answer is in 1..n+1 and the place-each-value-at-its-own-index trick. Example: [3,4,-1,1] -> 2; [1,2,0] -> 3; [7,8,9,11,12] -> 1.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Index as hash (cyclic placement). Use the array itself as the "set" of which small positive values are present.

**Say this first (1 line):** The answer is always in 1..n+1, so swap each value v in 1..n into slot v-1, then the first slot i where `nums[i] != i+1` gives answer i+1; if none, answer n+1.

**Brute force:**
- Put everything in a set, then test 1, 2, 3, ... until one is missing: O(n) time, O(n) space (this is the easy, standard answer and is fine if extra space is allowed).
- Sort and scan for the first gap above zero: O(n log n).

**Optimal:**
- Why 1..n+1: n values can fill at most 1..n. If they are exactly 1..n the answer is n+1; otherwise some value in 1..n is missing and the smallest missing is at most n. Anything <= 0 or > n can be ignored.
- Loop i from 0. While `nums[i]` is in 1..n and the slot it belongs in does not already hold it, swap it home: `j = nums[i]-1; swap(nums[i], nums[j])`.
- The condition `nums[j] != nums[i]` is what stops infinite loops on duplicates.
- Then scan for the first `nums[i] != i+1`.
- Each swap puts at least one value in its final slot, so there are at most n swaps in total. The inner `while` looks nested but is amortised O(n).

**Complexity:** Time O(n): at most n successful swaps plus two scans. Space O(1) extra (it modifies the input, which the prompt allows).

**Dry run:** `[3,4,-1,1]` (n=4). Output below shows it.
- i=0: 3 goes to slot 2: [-1,4,3,1]. -1 is out of range, stop.
- i=1: 4 goes to slot 3: [-1,1,3,4]. Now 1 goes to slot 0: [1,-1,3,4]. -1 stops.
- i=2, i=3: already home.
- Scan: slot 1 holds -1, not 2, so the answer is 2.

**Code:**
```python
import random

def brute(nums):
    s = set(nums)
    i = 1
    while i in s:
        i += 1
    return i

def optimal(nums):                    # modifies nums; O(1) extra space
    n = len(nums)
    for i in range(n):
        # keep swapping until slot i holds a value that cannot go home
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

assert optimal([3, 4, -1, 1]) == 2
assert optimal([1, 2, 0]) == 3
assert optimal([7, 8, 9, 11, 12]) == 1
assert optimal([]) == 1
assert optimal([1]) == 2
assert optimal([2]) == 1
assert optimal([1, 1]) == 2              # duplicates must not loop forever
assert optimal([2, 2, 2, 2]) == 1
assert optimal([-5, 0]) == 1
assert optimal(list(range(1, 1001))) == 1001
assert optimal([10**9, 1]) == 2

# a tracing helper for the dry run
def trace(nums):
    nums = nums[:]
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
        print(" after i =", i, nums)
    return nums
print("dry run [3,4,-1,1]:")
trace([3, 4, -1, 1])

rng = random.Random(16)
for _ in range(1000):
    a = [rng.randint(-3, 9) for _ in range(rng.randint(0, 8))]
    assert optimal(a[:]) == brute(a), a
print("1000 random cases agree")
print(optimal([3, 4, -1, 1]), optimal([1, 2, 0]), optimal([7, 8, 9, 11, 12]))
```

**Output (my run):**
```
dry run [3,4,-1,1]:
 after i = 0 [-1, 4, 3, 1]
 after i = 1 [1, -1, 3, 4]
 after i = 2 [1, -1, 3, 4]
 after i = 3 [1, -1, 3, 4]
1000 random cases agree
2 3 1
```

**Edge cases:**
- Empty list gives 1. `[1]` gives 2. `[2]` gives 1.
- Duplicates (`[1,1]`, `[2,2,2,2]`): the equality check prevents a swap loop.
- Huge or negative values are ignored by the range check.
- Already a full 1..n permutation returns n+1.

**Follow-ups:**
- *Can you avoid mutating?* Not in O(1) space for this problem. If you must restore, copy first (O(n) space).
- *Sign-marking version?* Replace out-of-range values with n+1, mark presence by negating `nums[v-1]`; same complexity.
- *Why not sum or XOR tricks?* They solve "one missing in 0..n", not arbitrary values with duplicates.

**Common mistakes:**
- Swapping with `nums[i]-1` written in the wrong order in the tuple assignment, so the index changes mid-swap. Compute `j` first.
- Using `if` instead of `while` for the swap.
- No duplicate check, so `[1,1]` loops forever.
- Forgetting the n+1 case.

---

### Q17 ⭐⭐ 🟢 Number of good pairs. Given `nums`, count index pairs (i, j) with i < j and nums[i] == nums[j]. Do it in O(n) by counting how many equal values were seen before, then show the closed form c*(c-1)/2 per value. Example: [1,2,3,1,1,3] -> 4; [1,1,1,1] -> 6.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Frequency counting. Equal values form groups, and pairs inside a group of size c number c choose 2.

**Say this first (1 line):** Loop once, and for each element add how many equal values came before it; equivalently count each value and add c*(c-1)/2.

**Brute force:** Two loops over i < j and compare: O(n^2) time, O(1) space.

**Optimal:**
- Running count: keep `seen[x]`. When x arrives, every earlier equal value forms one new pair with it, so `ans += seen[x]`, then increment.
- Closed form: a value that appears c times contributes c*(c-1)/2 pairs (choose 2 of c). Sum over `Counter(nums).values()`.
- Both are the same count; the running version is one pass, the closed form is clearer.
- Use `//` (integer division); c*(c-1) is always even so it is exact.

**Complexity:** Time O(n), average O(1) dict operations. Space O(d) where d is the number of distinct values.

**Dry run:** `[1,2,3,1,1,3]`.
- 1: seen 0, ans 0. 2: 0. 3: 0.
- 1: seen[1]=1, ans 1. 1: seen[1]=2, ans 3.
- 3: seen[3]=1, ans 4.
- Closed form: 1 appears 3 times (3 pairs), 3 appears 2 times (1 pair), 2 once (0). Total 4.

**Code:**
```python
import random
from collections import Counter

def brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] == nums[j])

def running(nums):                   # count equal values seen before
    seen = {}
    ans = 0
    for x in nums:
        ans += seen.get(x, 0)
        seen[x] = seen.get(x, 0) + 1
    return ans

def closed_form(nums):
    return sum(c * (c - 1) // 2 for c in Counter(nums).values())

assert running([1, 2, 3, 1, 1, 3]) == closed_form([1, 2, 3, 1, 1, 3]) == 4
assert running([1, 1, 1, 1]) == closed_form([1, 1, 1, 1]) == 6
assert running([]) == closed_form([]) == 0
assert running([5]) == closed_form([5]) == 0
assert running([1, 2, 3]) == closed_form([1, 2, 3]) == 0
assert closed_form([7] * 100000) == 100000 * 99999 // 2     # no overflow in Python

rng = random.Random(17)
for _ in range(500):
    a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 12))]
    assert running(a) == closed_form(a) == brute(a), a
print("500 random cases agree")
print(running([1, 2, 3, 1, 1, 3]), closed_form([1, 1, 1, 1]), closed_form([7] * 100000))
```

**Output (my run):**
```
500 random cases agree
4 6 4999950000
```

**Edge cases:**
- Empty or one element: 0.
- All equal: n(n-1)/2, so `[1,1,1,1]` gives 6.
- All distinct: 0.
- Large n: Python ints do not overflow; in fixed-width languages use 64 bits (n = 10^5 gives about 5*10^9, which exceeds 32 bits, as the run shows: 4,999,950,000).

**Follow-ups:**
- *Count bad pairs?* Total pairs minus good pairs of a transformed key (Q44 in this part).
- *Space O(1)?* Sort first, count runs: O(n log n).
- *Ordered pairs or i != j?* Multiply by 2.

**Common mistakes:**
- Using `c*(c-1)/2` with `/`, which gives a float.
- Using c*c/2 or c choose 2 off by one.
- Adding after incrementing the count, which double counts.

---

### Q18 ⭐⭐ 🟢 Ransom note. Given strings `note` and `magazine` of lowercase letters, decide whether note can be built using each magazine letter at most once. Use Counter subtraction and a manual-count version and explain a pitfall of Counter subtraction (non-positive counts). Example: note='aa', magazine='aab' -> True; note='aa', magazine='ab' -> False.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** Frequency counting with a budget: the magazine is a supply of letters, the note is demand.

**Say this first (1 line):** Count the magazine's letters, then consume one per note letter; if any count would go below zero, the note cannot be built.

**Brute force:** For every note letter, find it in the magazine list and remove it. `list.remove` and `in` are O(m) each, so O(n*m) time.

**Optimal:**
- Manual: 26-slot (or dict) count of the magazine; for each note letter decrement and return False if it drops below 0. O(n+m).
- Counter: `Counter(note) - Counter(magazine)`; the note is buildable if the result is empty (no letter is still needed).
- The pitfall: Counter subtraction with `-` keeps only positive counts. Negative and zero results are dropped silently. That is exactly why the empty-result check works here, but it makes `-` the wrong tool when you need to see surpluses (magazine leftovers) or negative balances. `Counter.subtract()` keeps all counts including zero and negative. The direction also matters: `magazine - note` tells you about leftover magazine letters, not whether the note can be built.

**Complexity:** Time O(n + m). Space O(1) for lowercase letters (26 slots), O(k) for k distinct characters in general.

**Dry run:** note `aa`, magazine `aab`.
- Magazine counts: a=2, b=1.
- Note letter a: a becomes 1. Note letter a: a becomes 0. Never negative, so True.
- For `aa` vs `ab`: a=1, b=1. First note a makes a=0. Second note a makes a=-1, below zero, so False.

**Code:**
```python
import random
from collections import Counter

def brute(note, magazine):
    mag = list(magazine)
    for ch in note:
        if ch in mag:
            mag.remove(ch)           # O(len(magazine)) each time
        else:
            return False
    return True

def counter_version(note, magazine):
    need = Counter(note) - Counter(magazine)   # keeps only POSITIVE leftovers
    return not need                             # empty Counter means nothing missing

def manual(note, magazine):
    have = [0] * 26
    for ch in magazine:
        have[ord(ch) - 97] += 1
    for ch in note:
        i = ord(ch) - 97
        have[i] -= 1
        if have[i] < 0:
            return False
    return True

for f in (brute, counter_version, manual):
    assert f('aa', 'aab') is True
    assert f('aa', 'ab') is False
    assert f('', '') is True
    assert f('', 'abc') is True
    assert f('a', '') is False
    assert f('abc', 'cba') is True
    assert f('aab', 'baa') is True

# the pitfall: subtraction silently drops non-positive counts
d = Counter('aa') - Counter('aab')
print("Counter('aa') - Counter('aab') =", d, "(b:-1 is gone, a:0 is gone)")
d2 = Counter('aa'); d2.subtract(Counter('aab'))
print("subtract() keeps them:", d2)
# wrong direction: magazine - note is NOT the check
print("wrong direction magazine - note:", Counter('aab') - Counter('aa'), "(leftover b, says nothing about note)")

rng = random.Random(18)
for _ in range(1000):
    note = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 6)))
    mag = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
    assert brute(note, mag) == counter_version(note, mag) == manual(note, mag), (note, mag)
print("1000 random cases agree")
print(manual('aa', 'aab'), manual('aa', 'ab'))
```

**Output (my run):**
```
Counter('aa') - Counter('aab') = Counter() (b:-1 is gone, a:0 is gone)
subtract() keeps them: Counter({'a': 0, 'b': -1})
wrong direction magazine - note: Counter({'b': 1}) (leftover b, says nothing about note)
1000 random cases agree
True False
```

**Edge cases:**
- Empty note is always True, even with an empty magazine.
- Empty magazine with a non-empty note is False.
- Note longer than the magazine is False immediately (early exit `len(note) > len(magazine)`).
- Uppercase or Unicode: use a dict instead of the 26-slot array.

**Follow-ups:**
- *Why does the Counter version work at all?* Positive leftovers are exactly the unmet demand.
- *Arbitrary characters?* Use `Counter` or a dict, the 26-slot array only fits lowercase letters.
- *Faster for repeated queries on one magazine?* Build the magazine Counter once and test each note by looping its letters.

**Common mistakes:**
- Reversing the subtraction.
- Checking `Counter(note) <= Counter(magazine)`: it works on Python 3.10+ (multiset comparison), but not on older versions; know the version.
- Using a set, which ignores repeated letters.
- Assuming Counter subtraction keeps negative counts.

---

### Q19 ⭐⭐ 🟢 First non-repeating element. Given a list of integers, return the first element (by position) that occurs exactly once, or -1 if none. Do it in two passes with a Counter and then discuss a single-pass variant with a dict that keeps insertion order. Example: [4,5,1,2,0,4] -> 5; [7,7] -> -1.
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** Frequency count, then first-match scan in original order. Counting tells you "which", the original list tells you "first".

**Say this first (1 line):** Count every value, then walk the list again and return the first value whose count is 1; if none, return -1.

**Brute force:** For each element call `nums.count(x)`, which is O(n), so O(n^2) overall.

**Optimal:**
- Two passes: `Counter(nums)`, then scan `nums` in order and return the first with count 1. O(n) time, O(d) space for d distinct values.
- Single-pass variant: since Python 3.7 a dict remembers first-insertion order. While reading, set `uniq[x] = x not in uniq` (True first time, False on any repeat). Then iterate `uniq.items()` and return the first True. Re-assigning an existing key keeps its original position, which is what makes this work.
- It is still two traversals in practice (one over the input, one over the dict), but the second one is over distinct values only, and it is the right shape for streaming: the dict can answer "first unique so far" at any moment.

**Complexity:** Time O(n) average for both versions. Space O(d), d distinct values.

**Dry run:** `[4,5,1,2,0,4]`.
- Counts: 4:2, 5:1, 1:1, 2:1, 0:1.
- Scan in order: 4 has count 2, skip. 5 has count 1, return 5.
- `[7,7]`: 7 has count 2, nothing else, return -1.

**Code:**
```python
import random
from collections import Counter

def brute(nums):
    for i, x in enumerate(nums):
        if nums.count(x) == 1:       # O(n) each -> O(n^2)
            return x
    return -1

def two_pass(nums):
    c = Counter(nums)
    for x in nums:
        if c[x] == 1:
            return x
    return -1

def one_pass(nums):
    # dict keeps first-seen order; value True = still unique, False = seen again
    uniq = {}
    for x in nums:
        uniq[x] = x not in uniq      # first time True, any repeat False
    for x, ok in uniq.items():       # scans distinct values, not the whole list
        if ok:
            return x
    return -1

for f in (brute, two_pass, one_pass):
    assert f([4, 5, 1, 2, 0, 4]) == 5
    assert f([7, 7]) == -1
    assert f([]) == -1
    assert f([3]) == 3
    assert f([1, 1, 2, 2, 3]) == 3
    assert f([-1, 2, -1, 2]) == -1
    assert f([0, 0, 9]) == 9         # a 0 answer must not be confused with falsy 'none'
    assert f([5, 6, 5]) == 6
assert one_pass([0, 1, 1]) == 0      # unique value 0 is a valid answer
print("sentinel clash: [-1,2,2] returns", two_pass([-1, 2, 2]), "which is a real answer AND the 'none' marker")

rng = random.Random(19)
for _ in range(1000):
    a = [rng.randint(-3, 5) for _ in range(rng.randint(0, 10))]
    assert brute(a) == two_pass(a) == one_pass(a), a
print("1000 random cases agree")
print(two_pass([4, 5, 1, 2, 0, 4]), two_pass([7, 7]))
```

**Output (my run):**
```
sentinel clash: [-1,2,2] returns -1 which is a real answer AND the 'none' marker
1000 random cases agree
5 -1
```

**Edge cases:**
- Empty list returns -1.
- A unique value of 0 is a valid answer (do not test truthiness).
- The sentinel clash: if -1 is itself a legitimate value (`[-1,2,2]`), the return value -1 is ambiguous. Ask the interviewer, or return `None` or an index.
- All duplicates returns -1. Single element returns that element.

**Follow-ups:**
- *Return the index?* Scan with `enumerate`.
- *Streaming?* Keep an ordered dict (or a queue plus counts) and drop duplicates lazily from the front.
- *Memory?* O(d); if the stream is huge you cannot do it exactly in less (a sketch can only approximate).

**Common mistakes:**
- Iterating the Counter and assuming order matches positions (it does in modern Python for insertion order, but be explicit and scan the list).
- Using `if value:` to test the answer, which breaks on 0.
- Calling `list.count` in a loop.

---

### Q20 ⭐⭐ 🟢 Isomorphic strings and word pattern. Two strings s and t of equal length are isomorphic if you can map each character of s to a character of t consistently and one-to-one. Decide it using two dicts (or one dict and a set) and explain why one direction alone is wrong. Example: 'egg','add' -> True; 'foo','bar' -> False; 'badc','baba' -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Bijection check with two hash maps. A consistent one-to-one map needs both directions to hold.

**Say this first (1 line):** Walk both strings together, keep s-to-t and t-to-s maps, and fail on any pair that contradicts either map.

**Brute force:** Convert each string to a canonical "first-occurrence pattern" (`egg` becomes 0,1,1; `add` becomes 0,1,1) and compare the patterns. Also O(n); the two-map version is just the direct version.

**Optimal:**
- Different lengths: return False first.
- For each pair (a, b): `s2t.setdefault(a, b) != b` means a was already mapped to something else. `t2s.setdefault(b, a) != a` means b was already claimed by another letter.
- Why one direction is wrong: with only s-to-t, `badc` vs `baba` passes. b->b, a->a, d->b, c->a is a consistent function, but b and d both map to b, and a and c both map to a. Two source letters sharing one target breaks one-to-one. The run shows the one-direction check returns True while the truth is False.
- Equivalent: one dict plus a set of used targets.
- Word pattern is the same logic with a pattern letter on one side and a whole word on the other (split the sentence, check the lengths match).

**Complexity:** Time O(n). Space O(k) for k distinct characters (O(1) for a fixed alphabet).

**Dry run:** `badc` vs `baba`.
- b-b: s2t {b:b}, t2s {b:b}.
- a-a: s2t {b:b, a:a}, t2s {b:b, a:a}.
- d-b: s2t gets d:b fine, but `t2s[b]` is already b, and b != d, so return False.

**Code:**
```python
import random
from itertools import product

def brute(s, t):
    # isomorphic iff a consistent one-to-one map exists: check via canonical pattern
    def pat(x):
        first = {}
        return [first.setdefault(ch, len(first)) for ch in x]
    return len(s) == len(t) and pat(s) == pat(t)

def optimal(s, t):
    if len(s) != len(t):
        return False
    s2t, t2s = {}, {}
    for a, b in zip(s, t):
        if s2t.setdefault(a, b) != b or t2s.setdefault(b, a) != a:
            return False
    return True

def one_direction_only(s, t):        # the classic wrong answer
    m = {}
    for a, b in zip(s, t):
        if m.setdefault(a, b) != b:
            return False
    return True

def word_pattern(pattern, sentence):
    words = sentence.split()
    if len(pattern) != len(words):
        return False
    p2w, w2p = {}, {}
    for p, w in zip(pattern, words):
        if p2w.setdefault(p, w) != w or w2p.setdefault(w, p) != p:
            return False
    return True

assert optimal('egg', 'add') is True
assert optimal('foo', 'bar') is False
assert optimal('badc', 'baba') is False
assert optimal('paper', 'title') is True
assert optimal('', '') is True
assert optimal('a', 'a') is True
assert optimal('ab', 'aa') is False
assert optimal('ab', 'abc') is False
print("one direction only on ('badc','baba'):", one_direction_only('badc', 'baba'), "(wrong, truth False)")
assert word_pattern('abba', 'dog cat cat dog') is True
assert word_pattern('abba', 'dog cat cat fish') is False
assert word_pattern('abba', 'dog dog dog dog') is False
assert word_pattern('aaaa', 'dog cat cat dog') is False
assert word_pattern('a', 'dog cat') is False

rng = random.Random(20)
for _ in range(1000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 6)))
    t = ''.join(rng.choice('xyz') for _ in range(len(s)))
    assert optimal(s, t) == brute(s, t), (s, t)
# exhaustive on a tiny alphabet and length 4
for s in map(''.join, product('ab', repeat=4)):
    for t in map(''.join, product('xy', repeat=4)):
        assert optimal(s, t) == brute(s, t)
print("1000 random + 256 exhaustive cases agree")
print(optimal('egg', 'add'), optimal('foo', 'bar'), optimal('badc', 'baba'))
```

**Output (my run):**
```
one direction only on ('badc','baba'): True (wrong, truth False)
1000 random + 256 exhaustive cases agree
True False False
```

**Edge cases:**
- Empty strings are isomorphic.
- Unequal lengths are not.
- A letter may map to itself; the same letter may repeat as long as it keeps the same target.
- Word pattern: `'abba'` with `'dog dog dog dog'` is False (two pattern letters, one word); `'aaaa'` with distinct words is False.

**Follow-ups:**
- *Single-dict approach?* Compare `s.index(a)` with `t.index(b)` at each position; correct but O(n^2).
- *Group isomorphic strings together?* Use the canonical first-occurrence pattern as the dict key.
- *Why setdefault?* It inserts on first sight and returns the stored value, so one call does the check and the store.

**Common mistakes:**
- Checking one direction only.
- Forgetting the length check (zip silently truncates).
- In word pattern, using `list(sentence)` instead of `sentence.split()`.

---

### Q21 ⭐⭐ 🟢 Remove element in place. Given list `nums` and a value `val`, remove all occurrences in place and return the new length k, the first k slots holding the kept values in any order. Give the order-preserving write-pointer version and the swap-from-the-end version that does fewer writes when matches are rare. Example: nums=[3,2,2,3], val=3 -> k=2, prefix [2,2].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Read/write pointers (in-place filtering). One pass decides what to keep; a second index decides where it goes. The array is the output.

**Say this first (1 line):** "Walk once, copy every value that is not `val` to the write slot, return the write count; if matches are rare I swap each match with the last live value instead, so I write only once per match."

**Brute force:** Build a new list with a comprehension and copy it back. O(n) time, O(n) extra space. It fails the "in place" ask and the extra list is the whole cost.

**Optimal:** Two versions.
- **Order-preserving write pointer:** `w` is the next free slot. For each `x`, if `x != val`, write `nums[w] = x; w += 1`. Invariant: `nums[:w]` holds the kept values seen so far, in order.
- **Swap from the end:** keep `n` as the live length. If `nums[i] == val`, overwrite it with `nums[n-1]` and shrink `n`. Do not advance `i`, because the value that came in is unchecked. Invariant: `nums[:i]` has no `val`, and `nums[n:]` is dead. Order changes, which the question allows.

**Complexity:**
- Both are O(n) time and O(1) space.
- Writes differ. Write pointer writes once per kept value. Swap writes once per match. So swap wins when matches are rare, write pointer wins when almost everything matches.
- Swap does at most n steps because each step either advances `i` or shrinks `n`.

**Dry run:** `[3,2,2,3]`, `val=3`, swap version.
| step | i | n | array | action |
|---|---|---|---|---|
| 1 | 0 | 4 | [3,2,2,3] | match: nums[0]=nums[3]=3, n=3 |
| 2 | 0 | 3 | [3,2,2,3] | match again: nums[0]=nums[2]=2, n=2 |
| 3 | 0 | 2 | [2,2,2,3] | keep, i=1 |
| 4 | 1 | 2 | [2,2,2,3] | keep, i=2, stop |

Result: k=2, prefix `[2,2]`. Note step 2: the swapped-in value was 3 and had to be rechecked.

The prompt's example is correct, and my run confirms k=2 with prefix [2,2] for both versions.

**Code:**
```python
import random


def remove_brute(nums, val):
    """Build a new list of kept values (extra O(n) space)."""
    return [x for x in nums if x != val]


def remove_stable(nums, val):
    """Write pointer: keeps order. Returns (k, writes)."""
    w = 0
    writes = 0
    for x in nums:
        if x != val:
            nums[w] = x
            w += 1
            writes += 1
    return w, writes


def remove_swap(nums, val):
    """Overwrite a match with the last live value. Order changes.
    Returns (k, writes). Writes == number of matches."""
    i, n = 0, len(nums)
    writes = 0
    while i < n:
        if nums[i] == val:
            nums[i] = nums[n - 1]
            n -= 1
            writes += 1
            # do NOT advance i: the swapped-in value is unchecked
        else:
            i += 1
    return n, writes


# --- the example from the prompt
a = [3, 2, 2, 3]
k, _ = remove_stable(a, 3)
print("stable  [3,2,2,3] val=3 ->", k, a[:k])
assert k == 2 and a[:k] == [2, 2]
a = [3, 2, 2, 3]
k, _ = remove_swap(a, 3)
print("swap    [3,2,2,3] val=3 ->", k, a[:k])
assert k == 2 and sorted(a[:k]) == [2, 2]

# --- writes: rare matches
big = list(range(1, 11))          # one match, at the front
s1, s2 = big[:], big[:]
k1, w1 = remove_stable(s1, 1)
k2, w2 = remove_swap(s2, 1)
print("rare match  : stable writes =", w1, " swap writes =", w2)
assert (w1, w2) == (9, 1)
# many matches: swap does more writes than stable when matches dominate
mostly = [7] * 9 + [1]
s1, s2 = mostly[:], mostly[:]
k1, w1 = remove_stable(s1, 7)
k2, w2 = remove_swap(s2, 7)
print("many matches: stable writes =", w1, " swap writes =", w2)
assert (w1, w2) == (1, 9)

# --- edge cases
for nums, val in [([], 1), ([1], 1), ([1], 2), ([2, 2, 2], 2),
                  ([2, 2, 2], 3), ([0, 0, 1], 0), ([-1, -1, 5], -1)]:
    want = remove_brute(nums, val)
    a = nums[:]
    k, _ = remove_stable(a, val)
    assert a[:k] == want
    a = nums[:]
    k, _ = remove_swap(a, val)
    assert sorted(a[:k]) == sorted(want)
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(21)
for _ in range(1000):
    n = rng.randint(0, 12)
    nums = [rng.randint(-3, 3) for _ in range(n)]
    val = rng.randint(-3, 3)
    want = remove_brute(nums, val)
    a = nums[:]
    k, wr = remove_stable(a, val)
    assert k == len(want) and a[:k] == want
    a = nums[:]
    k, wr = remove_swap(a, val)
    assert k == len(want) and sorted(a[:k]) == sorted(want)
    assert wr == nums.count(val)
print("1000 random cases OK")
```

**Output (my run):**
```
stable  [3,2,2,3] val=3 -> 2 [2, 2]
swap    [3,2,2,3] val=3 -> 2 [2, 2]
rare match  : stable writes = 9  swap writes = 1
many matches: stable writes = 1  swap writes = 9
edge cases OK
1000 random cases OK
```

**Edge cases:**
- Empty list: k=0.
- No match: nothing changes, k=n.
- All match: k=0.
- `val` equal to the last element: the swap copies a value onto itself, harmless.
- Negative values and 0 are ordinary values.

**Follow-ups:**
- *Why not advance `i` after a swap?* The value copied in from the end has not been tested yet.
- *Which do you ship?* The write pointer: simple and stable. Use the swap when order is free and matches are rare.
- *What if the array is huge and the matches are few?* Swap, since writes can cost more than reads (flash, copy-on-write pages).

**Common mistakes:**
- Using `nums.remove(val)` in a loop, or `del` / `pop(i)` in a loop. Each is O(n), so the total is O(n^2).
- Advancing `i` after a swap, which skips the value just moved in.
- Returning the list instead of k, or checking beyond the first k slots.

### Q22 ⭐⭐ 🟢 Merge sorted array in place. `a` has length m+n where the first m slots are sorted values and the last n are zeros as placeholders; `b` is a sorted list of n values. Merge b into a in place in O(m+n) time by filling from the back and explain why filling from the front fails. Example: a=[1,2,3,0,0,0], m=3, b=[2,5,6], n=3 -> [1,2,2,3,5,6].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports
**Pattern:** Two pointers from the back (merge in place). The free space is at the end, so the largest values go there first and nothing unread is overwritten.

**Say this first (1 line):** "I fill `a` from the back: compare the last live value of `a` with the last of `b`, put the larger at the last free slot, and move that pointer left; this never overwrites an unread `a` value."

**Brute force:** Copy `a[:m]` and `b`, concatenate, sort, write back. O((m+n) log(m+n)) time, O(m+n) space. It ignores the fact that both inputs are already sorted.

**Optimal:** Pointers `i = m-1` (last live in `a`), `j = n-1` (last in `b`), `w = m+n-1` (write slot).
- Take the larger of `a[i]` and `b[j]`, write it at `w`, move that pointer and `w` left.
- Loop while `j >= 0`. When `b` is used up, what is left of `a` is already in the right place.
- Invariant: `a[w+1:]` holds the largest values in final order, and `w >= i` always, so a write never lands on an unread `a` value. The gap between `w` and `i` is exactly the number of `b` values still unplaced.

**Why the front fails:** Writing at slot 0 overwrites `a[0]`, `a[1]`, ... before they are read. To go from the front you would need to shift `a` right or copy it, which is extra space or O(n^2). From the back, the free slots are exactly the zeros.

**Complexity:** O(m+n) time, each step moves one pointer. O(1) extra space.

**Dry run:** `a=[1,2,3,0,0,0]`, `b=[2,5,6]`.
| step | i | j | w | compare | write |
|---|---|---|---|---|---|
| 1 | 2 | 2 | 5 | 3 vs 6 | a[5]=6 |
| 2 | 2 | 1 | 4 | 3 vs 5 | a[4]=5 |
| 3 | 2 | 0 | 3 | 3 vs 2 | a[3]=3 |
| 4 | 1 | 0 | 2 | 2 vs 2 (not >) | a[2]=2 from b |
Then `j < 0`, stop. Array: `[1,2,2,3,5,6]`.

The prompt's example is correct. My run also shows a naive front-fill giving a wrong answer on it.

**Code:**
```python
import random


def merge_brute(a, m, b, n):
    """Extra-space version: sort the live parts, copy back."""
    merged = sorted(a[:m] + b)
    a[:] = merged
    return a


def merge_back(a, m, b, n):
    """Fill from the back. i: last live of a, j: last of b, w: write slot."""
    i, j, w = m - 1, n - 1, m + n - 1
    while j >= 0:                      # once b is used up, a's prefix is in place
        if i >= 0 and a[i] > b[j]:
            a[w] = a[i]
            i -= 1
        else:
            a[w] = b[j]
            j -= 1
        w -= 1
    return a


def merge_front_wrong(a, m, b, n):
    """Fill from the front in the same array: overwrites unread a values."""
    i, j = 0, 0
    a_copy_len = m
    for w in range(m + n):
        if j >= n or (i < a_copy_len and a[i] <= b[j]):
            a[w] = a[i]
            i += 1
        else:
            a[w] = b[j]
            j += 1
    return a


a = [1, 2, 3, 0, 0, 0]
print("back-fill  :", merge_back(a[:], 3, [2, 5, 6], 3))
assert merge_back(a[:], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]
try:
    bad = merge_front_wrong(a[:], 3, [2, 5, 6], 3)
    print("front-fill :", bad, "(wrong)")
    assert bad != [1, 2, 2, 3, 5, 6]
except IndexError as e:
    print("front-fill : IndexError", e)

# --- edge cases
assert merge_back([0], 0, [1], 1) == [1]            # a empty
assert merge_back([1], 1, [], 0) == [1]             # b empty
assert merge_back([], 0, [], 0) == []               # both empty
assert merge_back([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3) == [1, 2, 3, 4, 5, 6]
assert merge_back([1, 2, 3, 0, 0, 0], 3, [4, 5, 6], 3) == [1, 2, 3, 4, 5, 6]
assert merge_back([2, 2, 0, 0], 2, [2, 2], 2) == [2, 2, 2, 2]
assert merge_back([-3, -1, 0, 0], 2, [-2, -2], 2) == [-3, -2, -2, -1]
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(22)
for _ in range(1000):
    m, n = rng.randint(0, 8), rng.randint(0, 8)
    live = sorted(rng.randint(-5, 5) for _ in range(m))
    b = sorted(rng.randint(-5, 5) for _ in range(n))
    a1 = live + [0] * n
    a2 = live + [0] * n
    assert merge_back(a1, m, b, n) == merge_brute(a2, m, b, n)
print("1000 random cases OK")
```

**Output (my run):**
```
back-fill  : [1, 2, 2, 3, 5, 6]
front-fill : [1, 2, 2, 2, 5, 6] (wrong)
edge cases OK
1000 random cases OK
```

**Edge cases:**
- `m = 0`: all of `b` copies in.
- `n = 0`: `a` is already done, the loop never runs.
- All of `b` smaller than `a`: `a`'s values shift right one by one.
- All of `b` larger: `b` copies straight over the zeros.
- Duplicates: on a tie the code takes `b`'s value for the later slot, so equal values from `a` stay left of equal values from `b`.

**Follow-ups:**
- *Is it stable?* Yes. Filling from the back, a tie writes `b`'s value at the later slot, so `a`'s equal values stay before `b`'s.
- *What if there is no spare room?* Then you need a gap-method merge or a new list.
- *Linked lists?* Merging from the front is natural there; no trouble with overwriting.

**Common mistakes:**
- Merging from the front and clobbering `a`.
- Looping `while i >= 0 and j >= 0` and then forgetting to copy leftover `b`.
- Using `a[:] = sorted(...)` and calling it O(m+n).

### Q23 ⭐⭐ 🟡 Four sum count (4Sum II). Given four integer lists A, B, C, D each of length n (n <= 200), count tuples (i, j, k, l) with A[i]+B[j]+C[k]+D[l] == 0. Reduce to a two-sum over pair sums to get O(n^2) time and space instead of O(n^4). Example: A=[1,2], B=[-2,-1], C=[-1,2], D=[0,2] -> 2.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Meet in the middle with a hashmap (split a 4-way sum into two pair sums). Count what you need to find, then look it up.

**Say this first (1 line):** "Count every sum `a+b` in a Counter, then for every `c+d` add how many times `-(c+d)` was counted: O(n^2) instead of O(n^4)."

**Brute force:** Four nested loops (or `itertools.product`) testing the sum. O(n^4). For n=200 that is 1.6 billion tuples, too slow.

**Optimal:**
- Build `ab = Counter(a+b)` over all n^2 pairs.
- For each of the n^2 pairs `(c, d)`, add `ab[-(c+d)]`.
- The count of matching `(a, b)` pairs for one `(c, d)` is the number of tuples it completes, so the answer is the sum. Duplicates are handled for free because the Counter stores multiplicities.
- Use `.get(key, 0)` on the lookup, not `ab[key]` on a plain `defaultdict`, so the lookup does not insert keys.

**Complexity:** Time O(n^2) (n^2 inserts plus n^2 lookups, average O(1) each). Space O(n^2) for up to n^2 distinct sums: 40,000 at n=200, which is fine.

**Dry run:** `A=[1,2]`, `B=[-2,-1]`, `C=[-1,2]`, `D=[0,2]`.
- A+B sums: 1-2=-1, 1-1=0, 2-2=0, 2-1=1. Counter: {-1:1, 0:2, 1:1}.
- C+D sums: -1+0=-1 (need 1: count 1), -1+2=1 (need -1: count 1), 2+0=2 (need -2: 0), 2+2=4 (need -4: 0).
- Total = 1 + 1 = 2.

The prompt's example is correct (my run prints 2, and brute force agrees).

**Code:**
```python
import random
from collections import Counter
from itertools import product


def four_sum_brute(A, B, C, D):
    return sum(1 for a, b, c, d in product(A, B, C, D) if a + b + c + d == 0)


def four_sum_count(A, B, C, D):
    ab = Counter(a + b for a in A for b in B)      # O(n^2) time and space
    total = 0
    for c in C:
        for d in D:
            total += ab.get(-(c + d), 0)           # .get: no key inserted
    return total


A, B, C, D = [1, 2], [-2, -1], [-1, 2], [0, 2]
print("example:", four_sum_count(A, B, C, D))
assert four_sum_count(A, B, C, D) == 2 == four_sum_brute(A, B, C, D)

# --- edge cases
assert four_sum_count([0], [0], [0], [0]) == 1
assert four_sum_count([1], [1], [1], [1]) == 0
assert four_sum_count([0] * 5, [0] * 5, [0] * 5, [0] * 5) == 5 ** 4   # all equal
assert four_sum_count([-1, -1], [1, 1], [-1, -1], [1, 1]) == 16
assert four_sum_count([10 ** 9], [-10 ** 9], [10 ** 9], [-10 ** 9]) == 1  # no overflow
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(23)
for _ in range(500):
    n = rng.randint(1, 5)
    lists = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(4)]
    assert four_sum_count(*lists) == four_sum_brute(*lists)
print("500 random cases OK")

# --- size note: n=200 -> 40,000 pair sums stored, 40,000 lookups
n = 200
rng = random.Random(1)
big = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(n)] for _ in range(4)]
print("n=200 result runs fine, pair sums stored <=", n * n, "; n^4 =", n ** 4)
four_sum_count(*big)
```

**Output (my run):**
```
example: 2
edge cases OK
500 random cases OK
n=200 result runs fine, pair sums stored <= 40000 ; n^4 = 1600000000
```

**Edge cases:**
- All zeros: every tuple counts, n^4.
- No solution: 0.
- Big values: Python ints do not overflow.
- Unequal list lengths would also work with the same code.

**Follow-ups:**
- *Four sum (return the quadruples)?* A different problem: sort plus two pointers, O(n^3), with dedupe care.
- *Can you cut space?* Not easily; you can store only the smaller side, but both sides are n^2 here.
- *k lists?* Split in half: O(n^(k/2)) time and space.

**Common mistakes:**
- Using a set of sums, which loses multiplicity.
- Counting `(i, j)` pairs once and forgetting `(k, l)` multiplicity, or the reverse.
- Reading `defaultdict` on lookup and bloating memory.

### Q24 ⭐⭐ 🟡 Encode and decode a list of strings. Design `encode(strs) -> str` and `decode(s) -> list` so that any list of strings, including empty strings and strings containing your delimiter or digits, round-trips exactly. Use a length-prefix scheme and justify why a plain separator character is unsafe. Example: ['we','say',':','yes'] encodes to one string that decodes back to the same four items.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports
**Pattern:** Length-prefix framing (a self-describing serialisation). It is a design question dressed as a hashing-section problem: the key idea is that the format must be unambiguous for every possible string.

**Say this first (1 line):** "I write each string as its length, a `#`, then the string itself; the decoder reads the length, then takes exactly that many characters without looking at them, so content can never be confused with structure."

**Brute force:** Join with a delimiter (a comma) and split on decode. It breaks as soon as a string contains the delimiter, and `[]` and `['']` both encode to `''`. Escaping the delimiter works but needs a careful two-sided scheme.

**Optimal:**
- `encode`: `"".join(f"{len(s)}#{s}" for s in strs)`.
- `decode`: from position `i`, find the next `#` (the length field is digits only, so the first `#` after `i` is ours), parse the number, slice exactly that many characters, jump `i` past them.
- Why it is safe: the decoder never inspects payload characters, only counts them. A payload `'3#abc'` or `'1#1#1'` is just data.
- `[]` encodes to `''`; `['']` encodes to `'0#'`. Different, so empty cases round-trip.

**Complexity:** Encode and decode are O(total characters). Space O(total characters) for the output. Each character is touched a constant number of times; `str.index` scans only the short length field.

**Dry run:** `['we','say',':','yes']` encodes to `2#we3#say1#:3#yes`.
Decode: i=0, `#` at 1, length 2, take `we`, i=4. `#` at 5, length 3, take `say`, i=9. `#` at 10, length 1, take `:`, i=13. Then length 3, `yes`. Done.

The prompt's example round-trips in my run, as the output shows.

**Code:**
```python
import random


def encode_naive(strs):
    return ",".join(strs)


def decode_naive(s):
    return s.split(",")


def encode(strs):
    """length + '#' + payload, concatenated."""
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode(s):
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)           # first '#' after i ends the length field
        length = int(s[i:j])          # digits only, so the first '#' is ours
        out.append(s[j + 1:j + 1 + length])   # take exactly `length` chars
        i = j + 1 + length            # jump over the payload unread
    return out


ex = ["we", "say", ":", "yes"]
enc = encode(ex)
print("encoded:", repr(enc))
print("decoded:", decode(enc))
assert decode(enc) == ex

# why a separator is unsafe
bad = ["a,b", "c"]
print("naive round trip of", bad, "->", decode_naive(encode_naive(bad)))
assert decode_naive(encode_naive(bad)) != bad
print("naive round trip of [] ->", decode_naive(encode_naive([])), "(wrong: one empty string)")
assert decode_naive(encode_naive([])) != []

# --- edge cases
for case in ([], [""], ["", ""], ["#"], ["3#abc"], ["12", "3"], ["0#"],
             ["a" * 1000], ["héllo", "日本語", "😀"], ["1#1#1"], ["\n", " "]):
    assert decode(encode(case)) == case, case
assert encode([]) == "" and encode([""]) == "0#"
print("edge cases OK")

# --- seeded randomised check (adversarial alphabet: digits, '#', ',', letters)
rng = random.Random(24)
alpha = "#0123456789,ab "
for _ in range(2000):
    strs = ["".join(rng.choice(alpha) for _ in range(rng.randint(0, 6)))
            for _ in range(rng.randint(0, 6))]
    assert decode(encode(strs)) == strs
print("2000 random round trips OK")
```

**Output (my run):**
```
encoded: '2#we3#say1#:3#yes'
decoded: ['we', 'say', ':', 'yes']
naive round trip of ['a,b', 'c'] -> ['a', 'b', 'c']
naive round trip of [] -> [''] (wrong: one empty string)
edge cases OK
2000 random round trips OK
```

**Edge cases:**
- Empty list versus a list of one empty string.
- Strings that contain `#`, digits or newlines.
- Unicode: lengths count characters, so it works as long as encode and decode both use `str` (if you move to bytes, use byte lengths and keep it consistent).
- Very long strings: the length has more digits, still fine.

**Follow-ups:**
- *Over a network?* Encode to bytes and use a fixed-width length header (4 bytes), so you can read without scanning.
- *Why not JSON?* It is perfectly valid and the sane production answer; the interviewer usually wants you to build the framing yourself.
- *Escaping instead?* Works, but every delimiter and escape character must be handled, and the decoder is a state machine.

**Common mistakes:**
- Splitting on `'#'` in decode, which breaks on payloads that contain `#`.
- Parsing the length with a fixed single digit.
- Not handling `''` (length 0) strings.

### Q25 ⭐⭐ 🟡 Continuous subarray sum multiple of k. Given `nums` (non-negative) and an integer k, return True if some contiguous subarray of length at least 2 has a sum that is a multiple of k (0 counts). Store the first index of each prefix-sum remainder and explain why length at least 2 matters. Example: nums=[23,2,4,6,7], k=6 -> True (2+4); nums=[23,2,6,4,7], k=13 -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Prefix sums with a remainder map (first-seen index). If two prefix sums leave the same remainder mod k, the stretch between them sums to a multiple of k.

**Say this first (1 line):** "Track the prefix sum mod k and store the first index where each remainder appeared; if I see a remainder again at least two positions later, the subarray between them has sum divisible by k."

**Brute force:** Try every start and extend the end, keeping a running sum, test `sum % k == 0` for lengths of at least 2. O(n^2) time, O(1) space.

**Optimal:**
- `prefix[i]` = sum of the first `i` values. Subarray `(a, b]` has sum `prefix[b] - prefix[a]`. It is a multiple of k exactly when both prefixes have equal remainders.
- Seed the map with `{0: -1}` so a prefix that is itself a multiple of k counts (the empty prefix "ends" at -1).
- At index `i`: compute `r = prefix % k`. If `r` is in the map and `i - first[r] >= 2`, return True. If `r` is not in the map, store `first[r] = i`. Never overwrite: the earliest index gives the longest span, the best chance of clearing length 2.
- **Why length at least 2 matters:** for `[6]` with k=6 the prefix remainder 0 repeats at index 0 with the seed at -1, giving a length-1 subarray. The check `i - first[r] >= 2` rejects it.
- **k = 0:** a multiple of 0 means sum exactly 0, so the key is the raw prefix sum (`p % k` would divide by zero). With non-negative values that means a run of zeros, which the same code handles.

**Complexity:** O(n) time, O(min(n, k)) space (at most k remainders).

**Dry run:** `[23,2,4,6,7]`, k=6.
| i | x | prefix | r | map | action |
|---|---|---|---|---|---|
| seed | | 0 | 0 | {0:-1} | |
| 0 | 23 | 23 | 5 | {0:-1,5:0} | store |
| 1 | 2 | 25 | 1 | +{1:1} | store |
| 2 | 4 | 29 | 5 | | seen at 0, 2-0=2 >= 2: True (subarray 2+4=6) |

The prompt's examples are correct: True for the first, False for `[23,2,6,4,7]`, k=13 (my run shows both).

**Code:**
```python
import random


def check_brute(nums, k):
    n = len(nums)
    for i in range(n):
        s = nums[i]
        for j in range(i + 1, n):          # length >= 2
            s += nums[j]
            if (s == 0) if k == 0 else (s % k == 0):
                return True
    return False


def check_hash(nums, k):
    first = {0: -1}                         # empty prefix "ends" at index -1
    p = 0
    for i, x in enumerate(nums):
        p += x
        r = p % k if k else p               # k == 0: need an equal prefix sum
        if r in first:
            if i - first[r] >= 2:           # length at least 2
                return True
        else:
            first[r] = i                    # keep the EARLIEST index only
    return False


print(check_hash([23, 2, 4, 6, 7], 6), check_hash([23, 2, 6, 4, 7], 13))
assert check_hash([23, 2, 4, 6, 7], 6) is True
assert check_hash([23, 2, 6, 4, 7], 13) is False

# --- why length >= 2 matters: without it, one element can qualify
print("[6], k=6 ->", check_hash([6], 6), "(a single 6 is a multiple but length 1)")
assert check_hash([6], 6) is False and check_hash([6, 0], 6) is True

# --- edge cases
assert check_hash([], 5) is False
assert check_hash([0], 1) is False
assert check_hash([0, 0], 1) is True
assert check_hash([0, 0], 0) is True          # k = 0: sum must be exactly 0
assert check_hash([1, 0], 0) is False
assert check_hash([5, 0, 0], 0) is True
assert check_hash([1, 2], 1) is True          # k = 1: every sum qualifies
assert check_hash([23, 2, 6, 4, 7], 6) is True    # whole array sums to 42
assert check_hash([1, 1], 3) is False
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(25)
for _ in range(2000):
    n = rng.randint(0, 8)
    nums = [rng.randint(0, 9) for _ in range(n)]
    k = rng.randint(0, 9)
    assert check_hash(nums, k) == check_brute(nums, k), (nums, k)
print("2000 random cases OK")
```

**Output (my run):**
```
True False
[6], k=6 -> False (a single 6 is a multiple but length 1)
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty or one element: False.
- `[0, 0]`: True for any k (sum 0 is a multiple of anything, including 0 as the problem allows).
- `k = 1`: any pair works.
- `k = 0`: need a zero-sum subarray of length at least 2.
- `k` larger than every sum: only a zero-sum run works.

**Follow-ups:**
- *Negative numbers?* Python's `%` already returns a non-negative remainder for positive k, so the idea still holds. Without that guarantee, normalise with `((p % k) + k) % k`.
- *Count them instead of existence?* Count remainder frequencies and add `c*(c-1)/2` per remainder (this is a later question in this part).
- *Why a dict and not a set?* You need the index, to enforce length at least 2.

**Common mistakes:**
- Overwriting the stored index with the latest one, which loses long spans.
- Forgetting the `{0: -1}` seed.
- Dividing by `k = 0`.
- Accepting length-1 subarrays.

### Q26 ⭐⭐ 🟡 Contiguous array. Given a list of 0s and 1s, return the length of the longest contiguous subarray with equally many 0s and 1s. Map 0 to -1 and use first-seen prefix sums. Example: [0,1] -> 2; [0,1,0] -> 2; [0,0,1,0,0,0,1,1] -> 6.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Prefix sums with a first-seen map after a transform (0 becomes -1). Equal count of 0s and 1s means a net balance of zero.

**Say this first (1 line):** "Treat 0 as -1, keep a running balance, and remember the first index of each balance; whenever a balance repeats, the stretch between has equal 0s and 1s, so I take the longest such gap."

**Brute force:** For each start, extend the end with a running balance, record the length when it hits 0. O(n^2) time, O(1) space.

**Optimal:**
- Balance after index `i` is `#1s - #0s` so far.
- Same balance at positions `a < b` means the subarray `(a, b]` has net zero.
- Store only the first index of each balance (seed `{0: -1}`), since the earliest occurrence gives the longest span.
- Answer is the maximum `i - first[balance]`.

**Complexity:** O(n) time. Space O(n) worst case (balances range within [-n, n], so at most 2n+1 keys).

**Dry run:** `[0,0,1,0,0,0,1,1]`.
| i | x | balance | first seen? | length |
|---|---|---|---|---|
| seed | | 0 | at -1 | |
| 0 | 0 | -1 | store 0 | |
| 1 | 0 | -2 | store 1 | |
| 2 | 1 | -1 | seen at 0 | 2 |
| 3 | 0 | -2 | seen at 1 | 2 |
| 4 | 0 | -3 | store 4 | |
| 5 | 0 | -4 | store 5 | |
| 6 | 1 | -3 | seen at 4 | 2 |
| 7 | 1 | -2 | seen at 1 | 6 |
Answer 6.

All three examples in the prompt are correct; my run matches each and the brute force.

**Code:**
```python
import random


def longest_brute(nums):
    best = 0
    for i in range(len(nums)):
        bal = 0
        for j in range(i, len(nums)):
            bal += 1 if nums[j] == 1 else -1
            if bal == 0:
                best = max(best, j - i + 1)
    return best


def longest_hash(nums):
    first = {0: -1}               # balance 0 before index 0
    bal = best = 0
    for i, x in enumerate(nums):
        bal += 1 if x == 1 else -1
        if bal in first:
            best = max(best, i - first[bal])
        else:
            first[bal] = i        # earliest index gives the longest span
    return best


for arr, want in [([0, 1], 2), ([0, 1, 0], 2), ([0, 0, 1, 0, 0, 0, 1, 1], 6)]:
    got = longest_hash(arr)
    print(arr, "->", got)
    assert got == want == longest_brute(arr)

# --- edge cases
assert longest_hash([]) == 0
assert longest_hash([0]) == 0 and longest_hash([1]) == 0
assert longest_hash([0, 0, 0]) == 0
assert longest_hash([1, 1, 1, 1]) == 0
assert longest_hash([1, 0, 1, 0, 1, 0]) == 6
assert longest_hash([1, 1, 0, 0]) == 4
assert longest_hash([0, 0, 0, 1, 1]) == 4
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(26)
for _ in range(2000):
    arr = [rng.randint(0, 1) for _ in range(rng.randint(0, 14))]
    assert longest_hash(arr) == longest_brute(arr), arr
print("2000 random cases OK")
```

**Output (my run):**
```
[0, 1] -> 2
[0, 1, 0] -> 2
[0, 0, 1, 0, 0, 0, 1, 1] -> 6
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty list: 0.
- All 0s or all 1s: 0 (the balance never repeats).
- Whole array balanced: the answer is n.
- A single element: 0.

**Follow-ups:**
- *Why not a sliding window?* A window cannot decide when to shrink: a balance can go down and come back up, so there is no monotone signal.
- *Generalise?* Subarray with sum k, or equal counts of three kinds (use a tuple of differences as the key).
- *Space?* Can use an array of size 2n+1 offset by n instead of a dict.

**Common mistakes:**
- Forgetting the `{0: -1}` seed, which loses prefixes that start at index 0.
- Updating the stored index on every repeat (shortens the answer).
- Mapping 0 to 0 instead of -1.

### Q27 ⭐⭐ 🟡 Find all duplicates in place. A list of n integers has every value in 1..n, each value appearing once or twice. Return all values that appear twice in O(n) time and O(1) extra space (output excluded) by using the sign or index of the array itself as a marker, and say what you do to restore the input. Example: [4,3,2,7,8,2,3,1] -> [2,3].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Use the array itself as a hash set (index marking). Because every value is in 1..n, value `v` has a home slot `v-1`, and a sign bit on that slot records "seen".

**Say this first (1 line):** "For each value I flip the sign of the slot at its own index; if that slot is already negative, I have seen the value before, so it is a duplicate; at the end I take absolute values to restore the input."

**Brute force:** Counter or set: O(n) time and O(n) space. Or sort and compare neighbours: O(n log n) and it modifies the input. Both miss the O(1) extra space ask (sorting mutates).

**Optimal:**
- For each `x`, take `v = abs(x)` (the slot may have been negated earlier, but the value stored there still identifies a real value).
- If `nums[v-1] < 0`, then `v` was seen: add `v` to the answer.
- Otherwise negate `nums[v-1]`.
- Each duplicate is reported exactly once because a value appears at most twice. A third visit would break the guarantee.
- **Restore** with a final pass that sets every cell to its absolute value. Without it, the caller's data is corrupted, so state this out loud.

**Complexity:** O(n) time (two passes). O(1) extra space excluding the output. It does temporarily mutate the input.

**Dry run:** `[4,3,2,7,8,2,3,1]`.
- Marks negate slots 3, 2, 1, 6, 7 (values 4, 3, 2, 7, 8).
- Next x=2: slot 1 is already negative: report 2.
- Next x=3: slot 2 negative: report 3.
- x=1: slot 0 positive, negate. Final abs pass restores. Answer `[2,3]`.

The prompt's example is correct and the output order [2,3] is what this method produces (order of the second occurrence).

**Code:**
```python
import random
from collections import Counter


def dups_brute(nums):
    c = Counter(nums)
    return sorted(v for v, cnt in c.items() if cnt == 2)


def dups_inplace(nums):
    """Mark value v by negating nums[v-1]. A second visit sees a negative."""
    out = []
    for x in nums:
        v = abs(x)                      # x may already be negated by a marker
        if nums[v - 1] < 0:
            out.append(v)               # seen before
        else:
            nums[v - 1] = -nums[v - 1]
    for i in range(len(nums)):          # restore the input
        nums[i] = abs(nums[i])
    return out


a = [4, 3, 2, 7, 8, 2, 3, 1]
orig = a[:]
res = dups_inplace(a)
print("duplicates:", res, "| input restored:", a == orig)
assert res == [2, 3] and a == orig

# --- edge cases
assert dups_inplace([]) == []
assert dups_inplace([1]) == []
assert dups_inplace([1, 1]) == [1]
assert dups_inplace([1, 2, 3]) == []
assert dups_inplace([2, 2]) == [2]
assert sorted(dups_inplace([1, 1, 2, 2])) == [1, 2]   # stays valid: 3, 4 missing
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(27)
for _ in range(2000):
    n = rng.randint(0, 10)
    pool = list(range(1, n + 1)) * 2     # each value at most twice
    rng.shuffle(pool)
    nums = pool[:n]
    before = nums[:]
    got = sorted(dups_inplace(nums))
    assert got == dups_brute(before), before
    assert nums == before                # restored
print("2000 random cases OK")
```

**Output (my run):**
```
duplicates: [2, 3] | input restored: True
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty or single value: nothing.
- `[1,1]`: reports 1.
- A value that is a duplicate and also the slot that was negated: `abs(x)` handles it.
- Input already containing negatives or 0 or values out of range: the trick does not apply; state the precondition.

**Follow-ups:**
- *Could you do it without mutating?* Not in O(1) space for this problem in general; with the mutation you must restore. Cyclic sort is the other in-place option.
- *Multi-threaded callers?* The temporary mutation is not safe to share; copy first or take a lock.
- *Related?* Find all numbers missing from 1..n: the slots still positive after marking.

**Common mistakes:**
- Forgetting `abs()` when reading `x`, giving a negative index.
- Not restoring the input.
- Using the trick when values can be 0 or above n.

### Q28 ⭐⭐ 🟡 Find the duplicate number. A list of n+1 integers holds values in 1..n and exactly one value is repeated (possibly many times). Find it without modifying the list and using O(1) extra space. Compare a set (O(n) space), sorting (modifies), binary search on value range and Floyd cycle detection treating values as next pointers. Example: [1,3,4,2,2] -> 2; [3,1,3,4,2] -> 3.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Pigeonhole plus Floyd's cycle detection on an implicit linked list. Treat each index `i` as a node pointing to `nums[i]`. Two indices with the same value mean two edges into one node, which is where the cycle begins.

**Say this first (1 line):** "With n+1 values in 1..n, I treat `nums` as next pointers; the repeated value is the entrance of the cycle, so I find it with tortoise and hare without touching the array and with O(1) space."

**Brute force / alternatives (compared):**
| Method | Time | Extra space | Modifies input |
|---|---|---|---|
| Set of seen values | O(n) | O(n) | no |
| Sort and scan neighbours | O(n log n) | O(1) if in place, O(n) for a copy | yes if in place |
| Binary search on value range | O(n log n) | O(1) | no |
| Floyd cycle detection | O(n) | O(1) | no |

**Optimal (Floyd):**
- Start both pointers at node 0. Node 0 is never a value, so nothing points back to it, and it is outside the cycle: the head.
- Phase 1: slow moves one step (`nums[slow]`), fast moves two. They meet inside the cycle.
- Phase 2: put slow back at node 0 and move both one step at a time. They meet at the cycle entrance, which is the duplicate.
- Why: let `a` be the tail length and `c` the cycle length. At the meeting, slow has walked `s` steps and fast `2s`; both are in the cycle, so `s` is a multiple of `c`. The meeting point is `x = s - a` steps past the entrance, so walking `a` more steps from it gives `s` steps total, a multiple of `c`, which is the entrance. Walking `a` steps from the head also reaches the entrance. So the two pointers meet there.

**Binary search on values (the alternative):** for a candidate `mid`, count values `<= mid`. If the count exceeds `mid`, the duplicate is in `[lo, mid]`; otherwise in `[mid+1, hi]`. Pigeonhole guarantees the sign. O(n log n), O(1) space, simpler to defend.

**Complexity:** Floyd: O(n) time, O(1) space. Each phase walks at most a small constant times n steps.

**Dry run:** `[1,3,4,2,2]`. Edges: 0→1, 1→3, 3→2, 2→4, 4→2. The cycle is 2→4→2, entrance 2.
- Phase 1 (slow, fast): (1,3), (3,4), (2,4), (4,4). They meet at node 4.
- Phase 2 (slow from 0, fast from 4): (1,2), (3,4), (2,2). They meet at 2, the answer.

The prompt's examples are correct; all four methods agree on both in my run.

**Code:**
```python
import random


def find_set(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)


def find_sort(nums):
    s = sorted(nums)                     # copy: the input stays untouched
    for a, b in zip(s, s[1:]):
        if a == b:
            return a


def find_binary(nums):
    """Binary search on the VALUE range 1..n using the pigeonhole count."""
    lo, hi = 1, len(nums) - 1            # values are in 1..n, len = n+1
    while lo < hi:
        mid = (lo + hi) // 2
        cnt = sum(1 for x in nums if x <= mid)
        if cnt > mid:                    # too many values <= mid: dup is in [lo, mid]
            hi = mid
        else:
            lo = mid + 1
    return lo


def find_floyd(nums):
    """Index i points to nums[i]. The repeated value is the cycle entrance."""
    slow = fast = 0                      # node 0 is the head: no value equals 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0                             # phase 2: restart one pointer at the head
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


for arr, want in [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3)]:
    r = (find_set(arr), find_sort(arr), find_binary(arr), find_floyd(arr))
    print(arr, "->", r)
    assert r == (want,) * 4

# --- edge cases
assert find_floyd([1, 1]) == 1 and find_binary([1, 1]) == 1
assert find_floyd([2, 2, 2, 2, 2]) == 2           # many copies
assert find_binary([2, 2, 2, 2, 2]) == 2
assert find_floyd([1, 1, 2]) == 1 and find_binary([1, 1, 2]) == 1
assert find_floyd([2, 1, 2]) == 2
big = list(range(1, 100001)) + [77777]
assert find_floyd(big) == find_binary(big) == find_set(big) == 77777
keep = [3, 1, 3, 4, 2]
find_floyd(keep); find_binary(keep); find_sort(keep)
assert keep == [3, 1, 3, 4, 2]                    # not modified
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(28)
for _ in range(2000):
    n = rng.randint(1, 12)
    c = rng.randint(2, n + 1)                      # copies of the repeated value
    d = rng.randint(1, n)
    others = rng.sample([v for v in range(1, n + 1) if v != d], n + 1 - c)
    nums = [d] * c + others
    rng.shuffle(nums)
    assert len(nums) == n + 1
    want = find_set(nums)
    assert want == d
    assert find_sort(nums) == find_binary(nums) == find_floyd(nums) == d, nums
print("2000 random cases OK")
```

**Output (my run):**
```
[1, 3, 4, 2, 2] -> (2, 2, 2, 2)
[3, 1, 3, 4, 2] -> (3, 3, 3, 3)
edge cases OK
2000 random cases OK
```

**Edge cases:**
- `[1,1]`: n=1, answer 1.
- The duplicate appears many times: fine, the argument only needs one repeated target.
- The duplicate is the first element (`[2,1,2]` etc.): node 0 still sits outside the cycle.
- The values are never 0 and never above n: this precondition is what keeps the walk inside the array.

**Follow-ups:**
- *Why start at node 0?* No value equals 0, so nothing points back to node 0. It is outside the cycle, which the proof needs.
- *What if values include 0?* The walk could loop on node 0 and the proof breaks; use another method.
- *How is this related to linked list cycle detection?* It is the same two phases, with `nums[i]` as the `next` pointer.

**Common mistakes:**
- Sorting the input, which breaks the "do not modify" rule.
- Starting phase 1 at `nums[0]` but restarting phase 2 at node 0. The two phases must share the same head, or the loop may never end.
- Returning the meeting point of phase 1 instead of the phase-2 meeting.

### Q29 ⭐⭐ 🟡 Sort by frequency. Given a list of integers, return it sorted by frequency in descending order, ties broken by smaller value first. Show Counter plus sorted with a tuple key and explain stability of sorted and why tie-breaking must be explicit. Example: [1,1,2,2,2,3] -> [2,2,2,1,1,3]; [2,3,1,3,2] -> [2,2,3,3,1].
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports
**Pattern:** Frequency counting plus a composite sort key (a tuple key). Count once, then sort by `(-count, value)`.

**Say this first (1 line):** "Counter for frequencies, then `sorted(nums, key=lambda x: (-cnt[x], x))`; the tuple makes the tie-break explicit: higher count first, smaller value first."

**Brute force:** Key by `nums.count(x)` inside the sort. Each call is O(n), so O(n^2) overall. Correct but slow.

**Optimal:**
- `cnt = Counter(nums)`, O(n).
- `sorted(nums, key=lambda x: (-cnt[x], x))`. Negating the count sorts descending without `reverse`, so the value part still sorts ascending. (`reverse=True` would flip both.)
- Equal values come out together because they share the same key.

**Stability, and why the tie-break must be explicit:** `sorted` is stable: items with equal keys keep their input order. If you key only on `-cnt[x]`, tied values keep first-position order, and worse, the tied values interleave. On `[3,2,2,3,1]` that gives `[3,2,2,3,1]`: 3s and 2s are not grouped. Adding `x` to the key groups them and orders them as required.

**Complexity:** Time O(n log n) for the sort plus O(n) counting. Space O(n) for the counter and the output list. Sorting the n elements rather than the d distinct values costs a bit more than needed; you can instead sort the distinct values and expand with `[v] * c`, giving O(n + d log d).

**Dry run:** `[2,3,1,3,2]`. Counts: 2→2, 3→2, 1→1. Keys: 2→(-2,2), 3→(-2,3), 1→(-1,1). Sorted by key: 2,2 then 3,3 then 1 = `[2,2,3,3,1]`.

Both prompt examples are correct and my run reproduces them.

**Code:**
```python
import random
from collections import Counter


def sort_brute(nums):
    return sorted(nums, key=lambda x: (-nums.count(x), x))      # O(n^2) counts


def sort_freq(nums):
    cnt = Counter(nums)
    return sorted(nums, key=lambda x: (-cnt[x], x))


def sort_freq_no_tiebreak(nums):
    cnt = Counter(nums)
    return sorted(nums, key=lambda x: -cnt[x])      # relies on stability only


print(sort_freq([1, 1, 2, 2, 2, 3]), sort_freq([2, 3, 1, 3, 2]))
assert sort_freq([1, 1, 2, 2, 2, 3]) == [2, 2, 2, 1, 1, 3]
assert sort_freq([2, 3, 1, 3, 2]) == [2, 2, 3, 3, 1]

# stability alone keeps first-position order inside a tie: equal-count values interleave
t = [3, 2, 2, 3, 1]
print("explicit tie-break  :", sort_freq(t))
print("stability only      :", sort_freq_no_tiebreak(t), "(tied values interleaved: wrong)")
assert sort_freq(t) == [2, 2, 3, 3, 1]
assert sort_freq_no_tiebreak(t) == [3, 2, 2, 3, 1]

# --- edge cases
assert sort_freq([]) == []
assert sort_freq([5]) == [5]
assert sort_freq([4, 4, 4]) == [4, 4, 4]
assert sort_freq([3, 2, 1]) == [1, 2, 3]            # all frequency 1: by value
assert sort_freq([-1, -1, 2, 2, 0]) == [-1, -1, 2, 2, 0]
assert sort_freq([2, 2, -3, -3]) == [-3, -3, 2, 2]  # tie: smaller value first
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(29)
for _ in range(2000):
    nums = [rng.randint(-4, 4) for _ in range(rng.randint(0, 14))]
    assert sort_freq(nums) == sort_brute(nums), nums
print("2000 random cases OK")
```

**Output (my run):**
```
[2, 2, 2, 1, 1, 3] [2, 2, 3, 3, 1]
explicit tie-break  : [2, 2, 3, 3, 1]
stability only      : [3, 2, 2, 3, 1] (tied values interleaved: wrong)
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty list.
- All equal.
- All distinct: sorted ascending by value.
- Negative values: the tie-break "smaller value first" means -3 before 2.

**Follow-ups:**
- *Return distinct values with counts?* Use `sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))`.
- *Only the top k?* Heap or bucket by frequency (an earlier question in this part).
- *Strings?* The same, which is a common variant.

**Common mistakes:**
- Relying on stability alone and thinking it breaks ties by value.
- Using `reverse=True` with a `(count, value)` key, which sorts values descending too.
- Calling `.count` inside the key (hidden O(n^2)).

### Q30 ⭐⭐ 🟡 Majority element II. Return all values that appear more than n/3 times in a list of integers in O(n) time and O(1) extra space. Generalise Boyer-Moore with two candidates, then add a verification pass and say why it is needed. Example: [3,2,3] -> [3]; [1,2] -> [1,2]; [1] -> [1].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Boyer-Moore voting generalised to k = 2 candidates. Cancel off groups of three distinct values; whatever survives is the only possible winners.

**Say this first (1 line):** "At most two values can appear more than n/3 times, so I keep two candidates with counters, cancel triples of distinct values, then run a second pass to verify the survivors really exceed n/3."

**Brute force:** Counter and filter `count > n // 3`. O(n) time, O(n) space. Or sort and scan runs.

**Optimal:**
- Two candidates `c1, c2` with counts `n1, n2`.
- For each `x`: if it equals a candidate, increment that count. Else if a count is 0, adopt `x` there. Else decrement both.
- A decrement of both removes three distinct values from consideration (`x`, one `c1`, one `c2`). A value with more than n/3 occurrences cannot be fully cancelled, since each cancelled triple holds at most one copy of it, and at most n/3 triples can be cancelled.
- **Verification is required:** the survivors are only possible winners. `[1,2,3]` leaves candidates 1 and 2 although neither exceeds n/3 = 1 (each appears once). The second pass counts both candidates: O(n) total, O(1) space.
- Check order matters: test equality with a candidate before testing for a zero count, or a value can be adopted twice.

**Complexity:** O(n) time (two passes), O(1) extra space.

**Dry run:** `[3,2,3]`. 3 becomes c1 (1). 2 becomes c2 (1). 3 matches c1 (2). Candidates {3, 2}. Verify with n//3 = 1: 3 appears 2 > 1 yes, 2 appears 1 > 1 no. Answer `[3]`.

All three prompt examples are correct; `[1,2]` gives both since 1 > 0.67 (n//3 = 0 and counts must exceed it).

**Code:**
```python
import random
from collections import Counter


def maj3_brute(nums):
    n = len(nums)
    c = Counter(nums)
    return sorted(v for v, k in c.items() if k > n // 3)


def candidates(nums):
    """Pass 1: the two survivors of the pairing-off. Only POSSIBLE winners."""
    c1 = c2 = None
    n1 = n2 = 0
    for x in nums:
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:                         # three distinct values: cancel one of each
            n1 -= 1
            n2 -= 1
    return {c for c in (c1, c2) if c is not None}


def maj3_vote(nums):
    n = len(nums)
    cand = candidates(nums)
    # pass 2: verify (this is a count, still O(n) for two candidates)
    return sorted(c for c in cand if nums.count(c) > n // 3)


for arr, want in [([3, 2, 3], [3]), ([1, 2], [1, 2]), ([1], [1])]:
    print(arr, "->", maj3_vote(arr))
    assert maj3_vote(arr) == want == maj3_brute(arr)

# why verification: survivors are not always winners
for w in ([1, 2, 3], [1, 2, 3, 4, 5, 6, 7]):
    print(w, "survivors:", sorted(candidates(w)), "-> verified answer:", maj3_vote(w))
    assert maj3_vote(w) == []
assert sorted(candidates([1, 2, 3])) == [1, 2]

# --- edge cases
assert maj3_vote([]) == []
assert maj3_vote([2, 2]) == [2]
assert maj3_vote([0, 0, 0]) == [0]               # candidate value 0 is not None
assert maj3_vote([1, 1, 1, 2, 2, 2, 3]) == [1, 2]
assert maj3_vote([-1, -1, 5, 5, 7, 7]) == maj3_brute([-1, -1, 5, 5, 7, 7])
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(30)
for _ in range(3000):
    nums = [rng.randint(-3, 3) for _ in range(rng.randint(0, 15))]
    assert maj3_vote(nums) == maj3_brute(nums), nums
print("3000 random cases OK")
```

**Output (my run):**
```
[3, 2, 3] -> [3]
[1, 2] -> [1, 2]
[1] -> [1]
[1, 2, 3] survivors: [1, 2] -> verified answer: []
[1, 2, 3, 4, 5, 6, 7] survivors: [5, 7] -> verified answer: []
edge cases OK
3000 random cases OK
```

**Edge cases:**
- Empty list: nothing.
- A candidate value of 0: initialise candidates to `None`, not 0, or a real 0 may be confused with "no candidate".
- Fewer than two distinct values: one candidate only.
- At most two answers exist, so output is size 0, 1 or 2.

**Follow-ups:**
- *More than n/k?* Keep k-1 candidates (Misra-Gries). O(nk) time, O(k) space.
- *Why `> n // 3` and not `> n / 3`?* Counts are integers, so both are equivalent.
- *Streaming?* The first pass works on a stream; verification needs a second pass or a stored sample.

**Common mistakes:**
- Skipping the verification pass.
- Initialising both candidates to the same value, e.g. 0.
- Checking for a zero count before checking equality.

### Q31 ⭐⭐ 🟡 Set matrix zeroes. Given an m x n integer matrix, if a cell is 0 set its entire row and column to 0, in place, with O(1) extra space beyond the matrix by using the first row and first column as markers. Explain the two extra flags. Example: [[1,1,1],[1,0,1],[1,1,1]] -> [[1,0,1],[0,0,0],[1,0,1]].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** In-place matrix encoding. The matrix's own first row and first column become the "this row/column must be zeroed" memory, so the O(m+n) side sets disappear. It is the hashmap idea (remember what you saw) with the array itself as the table.

**Say this first (1 line):** "I record each zero in its row's first cell and its column's first cell, apply those marks to the inner block, then zero the first row and column last, using two flags that remember whether they held a zero before I started writing marks."

**Brute force:** Two sets, `rows` and `cols`. One scan to fill them, one scan to write zeros. O(mn) time, O(m+n) extra space. Even simpler: zero a row and column the moment you see a zero. That is wrong, because the new zeros look like original zeros and wipe the whole matrix.

**Optimal:**
- Flag 1: `first_row_zero`, true if row 0 has a zero.
- Flag 2: `first_col_zero`, true if column 0 has a zero.
- Scan the inner block (rows 1.., cols 1..). On a zero at (i, j), set `mat[i][0] = 0` and `mat[0][j] = 0`.
- Second scan of the inner block: zero (i, j) if `mat[i][0] == 0` or `mat[0][j] == 0`.
- Last: if `first_row_zero`, zero row 0. If `first_col_zero`, zero column 0.
- Why two flags: row 0 and column 0 are used as marker storage, so after marking you cannot tell if a zero there was original or a mark. The flags save the original truth. The cell (0, 0) is shared by both, which is why you need two flags and not one.
- Invariant: until the final step, the inner block is only read through the markers, and the markers are never overwritten by the apply step.

**Complexity:** Time O(mn): four passes at most, each touching every cell once or fewer. Extra space O(1): two booleans. Python note: a matrix is a list of lists; row assignment `mat[i][j] = 0` is O(1).

**Dry run:** `[[1,0,3],[4,5,6],[7,8,9]]`
- Flags: row 0 has a zero, so `first_row_zero = True`. Column 0 is `1,4,7`, so `first_col_zero = False`.
- Inner block has no zeros, so no marks are written (the zero at (0,1) is already a marker for column 1).
- Apply: column 1 marker `mat[0][1] == 0`, so (1,1) and (2,1) become 0.
- Final: `first_row_zero` is True, so row 0 becomes `0,0,0`. Result `[[0,0,0],[4,0,6],[7,0,9]]`.
- Prompt example `[[1,1,1],[1,0,1],[1,1,1]]`: the zero at (1,1) marks `mat[1][0]` and `mat[0][1]`. Apply zeroes row 1 and column 1. Result `[[1,0,1],[0,0,0],[1,0,1]]`. The prompt example is correct (verified by the run below).

**Code:**

```python
import random
from copy import deepcopy


def brute(mat):
    """Reference: collect zero rows/cols in two sets (O(m+n) space)."""
    m, n = len(mat), len(mat[0])
    rows = {i for i in range(m) for j in range(n) if mat[i][j] == 0}
    cols = {j for i in range(m) for j in range(n) if mat[i][j] == 0}
    return [[0 if (i in rows or j in cols) else mat[i][j] for j in range(n)] for i in range(m)]


def set_zeroes(mat):
    """O(1) extra space: row 0 / col 0 are the markers, two flags save their own fate."""
    m, n = len(mat), len(mat[0])
    first_row_zero = any(mat[0][j] == 0 for j in range(n))
    first_col_zero = any(mat[i][0] == 0 for i in range(m))
    for i in range(1, m):                      # record zeros of the inner block
        for j in range(1, n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
    for i in range(1, m):                      # apply markers to the inner block
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    if first_row_zero:                         # markers last, using the flags
        for j in range(n):
            mat[0][j] = 0
    if first_col_zero:
        for i in range(m):
            mat[i][0] = 0
    return mat


# Prompt example
ex = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
print("prompt example:", set_zeroes(ex))
assert ex == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

# Why the flags matter: the naive version (no flags) zeroes everything
def naive_no_flags(mat):
    m, n = len(mat), len(mat[0])
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    return mat

tricky = [[1, 0, 3], [4, 5, 6], [7, 8, 9]]   # zero lives in the first row
print("naive (no flags)  :", naive_no_flags(deepcopy(tricky)))
assert naive_no_flags(deepcopy(tricky)) != set_zeroes(deepcopy(tricky))
print("correct (two flags):", set_zeroes(deepcopy(tricky)))
tricky2 = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
print("naive on zero at [0][0]:", naive_no_flags(deepcopy(tricky2)))
print("zero at [0][0], correct:", set_zeroes(deepcopy(tricky2)))

# Edge cases
assert set_zeroes([[0]]) == [[0]]
assert set_zeroes([[5]]) == [[5]]
assert set_zeroes([[1, 0, 3]]) == [[0, 0, 0]]
assert set_zeroes([[1], [0], [3]]) == [[0], [0], [0]]
assert set_zeroes([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
assert set_zeroes([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
assert set_zeroes([[-1, 0], [2, -3]]) == [[0, 0], [2, 0]]
assert set_zeroes(deepcopy(tricky2)) == [[0, 0, 0], [0, 4, 5], [0, 7, 8]]

# Seeded randomised cross-check (zero-heavy and zero-light matrices, many shapes)
rng = random.Random(31)
for _ in range(1500):
    m, n = rng.randint(1, 6), rng.randint(1, 6)
    p = rng.choice([0.05, 0.2, 0.5])
    mat = [[0 if rng.random() < p else rng.randint(-5, 5) or 7 for _ in range(n)] for _ in range(m)]
    expect = brute(mat)
    got = set_zeroes(deepcopy(mat))
    assert got == expect, (mat, got, expect)
print("cross-check passed: 1500 random matrices")
```

**Output (my run):**

```text
prompt example: [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
naive (no flags)  : [[0, 0, 3], [4, 0, 6], [7, 0, 9]]
correct (two flags): [[0, 0, 0], [4, 0, 6], [7, 0, 9]]
naive on zero at [0][0]: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
zero at [0][0], correct: [[0, 0, 0], [0, 4, 5], [0, 7, 8]]
cross-check passed: 1500 random matrices
```

**Edge cases:**
- 1x1 matrix, single row, single column.
- Zero at (0,0): both flags true.
- Zero only in the first row or only in the first column.
- All zeros, no zeros, negative numbers (only exact 0 counts).
- A marker cell that already held a non-zero value: overwriting it is fine because the flags protect the real first row and column.

**Follow-ups:**
- *Can you do it with one flag?* Yes: use (0,0) as the marker for row 0 and one flag for column 0. It works, but it is harder to explain. Two flags are safer to say aloud.
- *Why not use a sentinel like None?* It needs a cell value not otherwise present and breaks if the matrix holds it. It also changes the type. The marker-in-place trick keeps values numeric.
- *Space if you can allocate?* The two-set version is O(m+n) and easier to get right first. Say it, then optimise.

**Common mistakes:**
- Zeroing first row and column before the inner block is processed: marks are destroyed.
- Scanning the inner block from (0,0) and forgetting flags: first row or column zeroed by a mark that was not an original zero. The "naive" lines in the output show exactly this.
- Using `0` as a marker when the value could be changed by the apply step in the wrong order.
- Zeroing in the first scan: new zeros trigger more zeros.

---

### Q32 ⭐⭐ 🟡 Pairs of songs divisible by 60. Given a list of durations in seconds, count pairs (i < j) whose sum is divisible by 60. Count remainders in a dict or 60-slot array and treat remainders 0 and 30 carefully. Example: [30,20,150,100,40] -> 3; [60,60,60] -> 3.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Complement counting over residues. Two numbers sum to a multiple of 60 exactly when their remainders add to 0 or 60. So only 60 classes matter, not the values. It is Two Sum with `x % 60` as the key.

**Say this first (1 line):** "I take each duration mod 60, count how many earlier values have the matching remainder `(60 - r) % 60`, and add that to the answer before recording r."

**Brute force:** Check all pairs `i < j` and test `(t[i] + t[j]) % 60 == 0`. O(n^2) time, O(1) space.

**Optimal:**
- Remainder `r = x % 60`. Its partner remainder is `(60 - r) % 60`. The outer `% 60` fixes `r = 0`, where the partner is 0 itself, not 60.
- Remainder 30 also pairs with 30. The formula covers it, since `(60 - 30) % 60 = 30`.
- One pass: look up first, then increment. Looking up before inserting makes sure an element never pairs with itself.
- A fixed `[0] * 60` array beats a dict: no hashing, and the key space is tiny.
- Invariant: before processing index j, `cnt[r]` is the number of earlier values with remainder r.

**Complexity:** Time O(n), one pass with O(1) work per element. Space O(60) = O(1).

**Dry run:** `[30,20,150,100,40]`, remainders `30,20,30,40,40`.
- 30: partner 30, `cnt[30] = 0`. Total 0. Record 30.
- 20: partner 40, count 0. Record 20.
- 150 (r = 30): partner 30, `cnt[30] = 1`. Total 1. Record 30 (now 2).
- 100 (r = 40): partner 20, `cnt[20] = 1`. Total 2. Record 40.
- 40 (r = 40): partner 20, `cnt[20] = 1`. Total 3. Done: 3. The prompt example is correct.
- `[60,60,60]`: remainders 0,0,0. Look up 0 each time: 0, 1, 2. Total 3. Correct.

**Code:**

```python
import random
from collections import Counter


def brute(t):
    n = len(t)
    return sum(1 for i in range(n) for j in range(i + 1, n) if (t[i] + t[j]) % 60 == 0)


def pairs_div60(t):
    """One pass: for x, partners are earlier values with remainder (60 - x%60) % 60."""
    cnt = [0] * 60
    total = 0
    for x in t:
        r = x % 60
        total += cnt[(60 - r) % 60]   # r=0 -> looks up 0, r=30 -> looks up 30
        cnt[r] += 1
    return total


def pairs_div60_counts(t):
    """Same answer from final counts: r<30 pairs with 60-r, 0 and 30 pair with themselves."""
    c = Counter(x % 60 for x in t)
    total = c[0] * (c[0] - 1) // 2 + c[30] * (c[30] - 1) // 2
    total += sum(c[r] * c[60 - r] for r in range(1, 30))
    return total


ex1 = [30, 20, 150, 100, 40]
ex2 = [60, 60, 60]
print(ex1, "->", pairs_div60(ex1), "| counts form:", pairs_div60_counts(ex1))
print(ex2, "->", pairs_div60(ex2), "| counts form:", pairs_div60_counts(ex2))
assert pairs_div60(ex1) == 3 and pairs_div60(ex2) == 3

# Trap: forgetting the % 60 on the complement gives 60 - 0 = 60 (a slot that never fills)
def buggy(t):
    cnt = [0] * 61
    total = 0
    for x in t:
        r = x % 60
        total += cnt[60 - r]
        cnt[r] += 1
    return total
print("buggy (no outer %60) on [60,60,60]:", buggy(ex2), "(should be 3)")

# Edge cases
assert pairs_div60([]) == 0
assert pairs_div60([60]) == 0
assert pairs_div60([30, 30]) == 1
assert pairs_div60([30, 30, 30]) == 3
assert pairs_div60([1, 59]) == 1
assert pairs_div60([60, 120, 180, 240]) == 6
assert pairs_div60([1, 2, 3]) == 0
assert pairs_div60([500] * 4) == 0       # 500 % 60 == 20, 20+20 != 60

rng = random.Random(32)
for _ in range(1500):
    t = [rng.randint(1, 500) for _ in range(rng.randint(0, 25))]
    b = brute(t)
    assert pairs_div60(t) == b == pairs_div60_counts(t), t
print("cross-check passed: 1500 random lists (three implementations agree)")
```

**Output (my run):**

```text
[30, 20, 150, 100, 40] -> 3 | counts form: 3
[60, 60, 60] -> 3 | counts form: 3
buggy (no outer %60) on [60,60,60]: 0 (should be 3)
cross-check passed: 1500 random lists (three implementations agree)
```

**Edge cases:**
- Empty list and a single element: 0.
- Remainder 0 (multiples of 60) and remainder 30: pairs within the same class, `c*(c-1)/2`.
- Large values: `x % 60` handles any size. Python has no overflow.
- Values already below 60 or above: only the remainder counts.

**Follow-ups:**
- *Generalise to any modulus m?* Same code with `m` in place of 60. Classes 0 and `m/2` (if m is even) pair with themselves.
- *Count pairs where sum is divisible by k, with negatives?* Python's `%` already returns a non-negative result, so the code is unchanged.
- *Return the pairs, not the count?* Store index lists per remainder. Output size can be O(n^2), so say that.

**Common mistakes:**
- Using `60 - r` without the outer `% 60`: remainder 0 looks up slot 60 and finds nothing. The "buggy" line in the output shows 0 instead of 3.
- Incrementing before looking up: pairs an element with itself when r is 0 or 30.
- Counting ordered pairs and double counting.
- Using a dict and forgetting that a missing key must return 0.

---

### Q33 ⭐⭐ 🟡 Subarray sums divisible by k. Given integers `nums` (negatives allowed) and a positive k, count non-empty contiguous subarrays whose sum is divisible by k. Count prefix remainders, and explain how Python's modulo of negative numbers helps compared with languages where the result can be negative. Example: nums=[4,5,0,-2,-3,1], k=5 -> 7.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Prefix sums with a hashmap of residue classes. A slice sums to a multiple of k exactly when its two bounding prefix sums have the same remainder mod k. Count equal-remainder pairs.

**Say this first (1 line):** "I keep a running prefix mod k and a count per remainder, seeded with remainder 0 once for the empty prefix, and for each new prefix I add how many earlier prefixes had the same remainder."

**Brute force:** Try every `(i, j)` and sum the slice: O(n^3), or O(n^2) with a running sum. Fine for the cross-check, too slow for n = 10^5.

**Optimal:**
- `P[j] - P[i]` divisible by k means `P[j] % k == P[i] % k`. So the slice `i..j-1` qualifies.
- Seed `seen[0] = 1`. That stands for the empty prefix. Without it you miss slices that start at index 0.
- For each x: `pref = (pref + x) % k`, `ans += seen[pref]`, then `seen[pref] += 1`.
- Python's `%` with a positive k always returns a value in `[0, k)`, even for negative numbers: `-7 % 5 == 3`. So -2 and 3 land in the same bucket automatically.
- In C, Java or `math.fmod`, `-7 % 5` is `-2`. You must write `((r % k) + k) % k` or equal classes split into two keys and you undercount.
- Invariant: before step j, `seen` counts every earlier prefix (including the empty one) by remainder.

**Complexity:** Time O(n): one pass, O(1) expected per dict operation. Space O(min(n, k)) for the remainder counts. A list of size k also works when k is small.

**Dry run:** `nums=[4,5,0,-2,-3,1]`, k=5.
- Prefix remainders after each element: 4, 4, 4, 2, 4, 0. Start `seen = {0:1}`.
- 4: seen[4] = 0, ans 0. 4: seen[4] = 1, ans 1. 4: seen[4] = 2, ans 3.
- 2: seen[2] = 0, ans 3. 4: seen[4] = 3, ans 6. 0: seen[0] = 1 (the empty prefix), ans 7.
- Answer 7. The prompt example is correct.

**Code:**

```python
import math
import random
from collections import defaultdict


def brute(nums, k):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i, n) if sum(nums[i:j + 1]) % k == 0)


def sub_div_k(nums, k):
    """Two equal prefix remainders mean the slice between them sums to a multiple of k."""
    seen = defaultdict(int)
    seen[0] = 1            # empty prefix
    pref = 0
    ans = 0
    for x in nums:
        pref = (pref + x) % k      # Python: result is in [0, k) even if pref+x < 0
        ans += seen[pref]
        seen[pref] += 1
    return ans


ex = [4, 5, 0, -2, -3, 1]
print(ex, "k=5 ->", sub_div_k(ex, 5))
assert sub_div_k(ex, 5) == 7

# Negative modulo: Python vs a C-style remainder (math.fmod truncates toward zero)
print("Python  -7 % 5 =", -7 % 5, "| C-style fmod(-7,5) =", int(math.fmod(-7, 5)))


def sub_div_k_c_style(nums, k):
    seen = defaultdict(int)
    seen[0] = 1
    pref = ans = 0
    for x in nums:
        pref = int(math.fmod(pref + x, k))     # may be negative: -2 and 3 are the same class but different keys
        ans += seen[pref]
        seen[pref] += 1
    return ans

bad = sub_div_k_c_style(ex, 5)
print("C-style remainders without the (r + k) % k fix ->", bad, "(wrong, expected 7)")
assert bad != 7

# Edge cases
assert sub_div_k([], 3) == 0
assert sub_div_k([5], 5) == 1
assert sub_div_k([3], 5) == 0
assert sub_div_k([-5], 5) == 1
assert sub_div_k([0, 0, 0], 7) == 6
assert sub_div_k([1, 2, 3], 1) == 6          # k=1: every non-empty subarray
assert sub_div_k([-1, -1, -1], 3) == 1
assert sub_div_k([7, -7], 7) == 3

rng = random.Random(33)
for _ in range(1500):
    nums = [rng.randint(-9, 9) for _ in range(rng.randint(0, 14))]
    k = rng.randint(1, 8)
    assert sub_div_k(nums, k) == brute(nums, k), (nums, k)
print("cross-check passed: 1500 random lists with negatives")
```

**Output (my run):**

```text
[4, 5, 0, -2, -3, 1] k=5 -> 7
Python  -7 % 5 = 3 | C-style fmod(-7,5) = -2
C-style remainders without the (r + k) % k fix -> 4 (wrong, expected 7)
cross-check passed: 1500 random lists with negatives
```

**Edge cases:**
- Empty list: 0. k = 1: every non-empty subarray counts, n(n+1)/2.
- A single element that is a multiple of k, including 0 and negatives.
- All zeros: n(n+1)/2.
- Large positive and negative values: Python ints do not overflow.
- Remainders from negative prefixes: handled by Python's non-negative modulo.

**Follow-ups:**
- *Why does a sliding window not work?* Negatives break monotonicity, and "divisible" is not monotone anyway.
- *Do it with a fixed array?* `cnt = [0]*k` instead of a dict. Faster for small k.
- *Longest such subarray instead of count?* Store the first index of each remainder (see Q25).

**Common mistakes:**
- Forgetting `seen[0] = 1`.
- Updating `seen` before adding to the answer: counts a slice of length 0.
- In languages with truncating `%`, forgetting to normalise negatives. The "C-style" lines in the output give 4 instead of 7.
- Counting prefix pairs by `c * (c - 1) / 2` on a different pass and mixing it with the running approach.

---

### Q34 ⭐⭐ 🟡 Next permutation. Rearrange a list of integers in place into the next lexicographically greater permutation; if it is already the largest, rearrange to the smallest (ascending). Use O(1) extra space. Example: [1,2,3] -> [1,3,2]; [3,2,1] -> [1,2,3]; [1,1,5] -> [1,5,1].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** In-place array rewrite using suffix structure. The next permutation changes the shortest possible suffix: find the rightmost place where you can still increase, bump it by the smallest larger value, then make the tail as small as possible.

**Say this first (1 line):** "Find the rightmost ascent `a[i] < a[i+1]`, swap `a[i]` with the rightmost value greater than it, then reverse everything after i; if there is no ascent, just reverse the whole list."

**Brute force:** Generate all permutations, sort the distinct ones and take the one after the input (wrapping to the first). Time O(n! * n). Only useful as a reference.

**Optimal:**
- The suffix after the pivot `i` is non-increasing, so it is already the largest arrangement of those values. Nothing inside it can be bumped.
- Pivot `i`: the rightmost index with `a[i] < a[i+1]`. Use `>=` when scanning back so equal neighbours are skipped (duplicates).
- Swap target `j`: the rightmost value `> a[i]`. Because the suffix is non-increasing, scanning from the right finds the smallest value that is larger.
- After the swap the suffix is still non-increasing. Reverse it to get the smallest suffix.
- No pivot (whole list non-increasing): this is the last permutation. Reversing the whole list gives the smallest, as the prompt asks.
- Invariant: every permutation between the input and the output would need a different prefix or a smaller suffix, and neither is possible.

**Complexity:** Time O(n): at most three linear passes. Space O(1) extra. Note: the slice reversal `a[i+1:] = a[i+1:][::-1]` makes a temporary copy of the suffix, so strictly it is O(n) temporary space in Python. For a true O(1) version use two-pointer swaps; say this if asked.

**Dry run:** `[1,5,8,4,7,6,5,3,1]`
- From the right, `7 > 4`, so the pivot is 4 at index 3 (the suffix `7,6,5,3,1` is non-increasing).
- Rightmost value greater than 4 is 5. Swap: `[1,5,8,5,7,6,4,3,1]`.
- Reverse the suffix after index 3: `[1,5,8,5,1,3,4,6,7]`.
- `[1,1,5]`: scanning from the right, `1 < 5` at index 1, so the pivot is the second 1 (the first 1 is not the rightmost ascent). Swap it with 5: `[1,5,1]`. The tail has one element, so reversing changes nothing. Result `[1,5,1]`.
- `[3,2,1]` has no ascent, so reverse all: `[1,2,3]`. All three prompt examples match (verified by the run).

**Code:**

```python
import random
from itertools import permutations


def brute(a):
    """Enumerate distinct permutations in order; take the one after a (wrap to the smallest)."""
    perms = sorted(set(permutations(a)))
    i = perms.index(tuple(a))
    return list(perms[(i + 1) % len(perms)])


def next_permutation(a):
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:     # >= so equal values are skipped (duplicates)
        i -= 1
    if i >= 0:
        j = n - 1
        while a[j] <= a[i]:                # rightmost value strictly greater than the pivot
            j -= 1
        a[i], a[j] = a[j], a[i]
    a[i + 1:] = a[i + 1:][::-1]            # suffix was non-increasing: reverse to ascending
    return a


for ex, want in [([1, 2, 3], [1, 3, 2]), ([3, 2, 1], [1, 2, 3]), ([1, 1, 5], [1, 5, 1])]:
    got = next_permutation(ex[:])
    print(ex, "->", got)
    assert got == want

# Trace of a longer one
a = [1, 5, 8, 4, 7, 6, 5, 3, 1]
print(a, "->", next_permutation(a[:]))
assert next_permutation(a[:]) == [1, 5, 8, 5, 1, 3, 4, 6, 7]

# Edge cases
assert next_permutation([]) == []
assert next_permutation([7]) == [7]
assert next_permutation([2, 2, 2]) == [2, 2, 2]
assert next_permutation([1, 2]) == [2, 1]
assert next_permutation([2, 1]) == [1, 2]
assert next_permutation([1, 3, 2]) == [2, 1, 3]
assert next_permutation([-1, 0, -1]) == [0, -1, -1]

# Applying it repeatedly walks every distinct permutation exactly once, then wraps
a = [1, 1, 2, 2]
seen = [tuple(a)]
for _ in range(6):
    next_permutation(a)
    seen.append(tuple(a))
print("walk of [1,1,2,2]:", seen)
assert len(set(seen[:6])) == 6 and len(seen) == 7 and seen[-1] == seen[0]

rng = random.Random(34)
for _ in range(1500):
    a = [rng.randint(0, 3) for _ in range(rng.randint(1, 7))]
    assert next_permutation(a[:]) == brute(a), a
print("cross-check passed: 1500 random lists (duplicates included)")
```

**Output (my run):**

```text
[1, 2, 3] -> [1, 3, 2]
[3, 2, 1] -> [1, 2, 3]
[1, 1, 5] -> [1, 5, 1]
[1, 5, 8, 4, 7, 6, 5, 3, 1] -> [1, 5, 8, 5, 1, 3, 4, 6, 7]
walk of [1,1,2,2]: [(1, 1, 2, 2), (1, 2, 1, 2), (1, 2, 2, 1), (2, 1, 1, 2), (2, 1, 2, 1), (2, 2, 1, 1), (1, 1, 2, 2)]
cross-check passed: 1500 random lists (duplicates included)
```

**Edge cases:**
- Empty and single element: unchanged.
- Descending list: wraps to ascending.
- All equal values: unchanged (only one distinct permutation).
- Duplicates: use `>=` on the pivot scan and `<=` on the swap scan.
- Applying it repeatedly walks every distinct permutation exactly once, then wraps (the output shows it for `[1,1,2,2]`).

**Follow-ups:**
- *Previous permutation?* Mirror the comparisons: find the rightmost descent, swap with the rightmost smaller value, reverse the suffix.
- *k-th permutation?* Use the factorial number system, not repeated next-permutation.
- *Why reverse and not sort?* The suffix is already in descending order, so reversing is O(n) where sorting is O(n log n).

**Common mistakes:**
- Using `>` instead of `>=` in the pivot scan: with duplicates it stops on an equal pair and swaps equal values.
- Picking the leftmost larger value instead of the rightmost.
- Sorting the suffix instead of reversing it (correct but slower).
- Forgetting the wrap case, or returning a new list when the prompt says in place.

---

### Q35 ⭐⭐ 🟡 Randomised set with O(1) operations. Implement insert(x), remove(x) and getRandom() on a set of distinct integers, each in average O(1), where getRandom returns every present element with equal probability. Combine a list and a dict value-to-index and show the swap-with-last removal. Example: insert 1, insert 2, remove 1, getRandom -> always 2.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** List plus dict (value to index). The list gives O(1) random access for uniform sampling. The dict gives O(1) membership. Removal swaps the victim with the last element so the list stays dense.

**Say this first (1 line):** "A list for uniform sampling, a dict from value to its index for lookup, and removal by moving the last element into the hole, so everything stays O(1) on average."

**Brute force:** Keep only a list. Insert checks `x in list` (O(n)), remove calls `list.remove` (O(n)). A plain `set` has O(1) insert and remove but `random.choice(list(s))` is O(n), and `random.choice(s)` does not work on a set.

**Optimal:**
- `insert(x)`: if x is in the dict, return False. Else store `pos[x] = len(items)` and append.
- `remove(x)`: look up index i. Copy the last element into `items[i]`. Update `pos[last] = i`. Pop the list. Delete `pos[x]`.
- Order inside remove matters when x is itself the last element: re-point first, delete after. Then the final `del` removes the key that the re-point just wrote.
- `get_random`: `items[rng.randrange(len(items))]`. Every present element has exactly one slot, so each has probability 1/size.
- Invariant: `items[pos[v]] == v` for every v, and `len(items) == len(pos)`.

**Complexity:** `insert`, `remove` and `get_random` are O(1) average (dict operations are expected O(1); `list.append` is amortised O(1); `list.pop()` from the end is O(1)). Space O(n). Never `list.pop(0)` or `list.remove`: those are O(n).

**Dry run:** insert 10, 20, 30: `items=[10,20,30]`, `pos={10:0,20:1,30:2}`.
- `remove(10)`: i = 0, last = 30. `items[0] = 30`, `pos[30] = 0`, pop gives `[30,20]`, delete 10. `pos={30:0,20:1}`.
- Prompt example: insert 1, insert 2, remove 1: `items=[2]`, so `getRandom` is always 2. Correct.
- `remove(20)` now (the last element): i = 1, last = 20. `items[1] = 20`, `pos[20] = 1`, pop, delete 20. Clean.

**Code:**

```python
import random
from collections import Counter


class RandomizedSet:
    """list holds the elements densely; dict maps value -> index in that list."""

    def __init__(self, rng=None):
        self.items = []
        self.pos = {}
        self.rng = rng or random

    def insert(self, x):
        if x in self.pos:
            return False
        self.pos[x] = len(self.items)
        self.items.append(x)
        return True

    def remove(self, x):
        if x not in self.pos:
            return False
        i = self.pos[x]
        last = self.items[-1]
        self.items[i] = last          # move last element into the hole
        self.pos[last] = i            # update ITS index first ...
        self.items.pop()
        del self.pos[x]               # ... then delete x (order matters when x is last)
        return True

    def get_random(self):
        return self.items[self.rng.randrange(len(self.items))]


class BruteSet:
    """Reference with O(n) operations."""

    def __init__(self):
        self.items = []

    def insert(self, x):
        if x in self.items:
            return False
        self.items.append(x)
        return True

    def remove(self, x):
        if x not in self.items:
            return False
        self.items.remove(x)
        return True


# Prompt example
s = RandomizedSet(random.Random(35))
print(s.insert(1), s.insert(2), s.remove(1), "getRandom x5 ->", [s.get_random() for _ in range(5)])
assert all(s.get_random() == 2 for _ in range(50))

# Removing the LAST element (the classic bug if you delete before re-pointing)
s = RandomizedSet(random.Random(1))
for v in (10, 20, 30):
    s.insert(v)
assert s.remove(30) and s.items == [10, 20] and s.pos == {10: 0, 20: 1}
assert s.remove(10) and s.items == [20] and s.pos == {20: 0}
assert s.remove(20) and s.items == [] and s.pos == {}
assert not s.remove(20) and not s.remove(99)
assert s.insert(20) and not s.insert(20)
print("last-element removal and re-insert OK")

# Buggy variant: pop the list and delete the key BEFORE re-pointing the moved element
class Buggy(RandomizedSet):
    def remove(self, x):
        if x not in self.pos:
            return False
        i = self.pos.pop(x)
        last = self.items.pop()
        if i < len(self.items):
            self.items[i] = last
        self.pos[last] = i          # when x was last, this re-adds x with a stale index
        return True
b = Buggy()
b.insert(1); b.insert(2)
b.remove(2)
print("buggy remove-last leaves pos =", b.pos, "items =", b.items, "(ghost key 2)")
assert 2 in b.pos and b.items == [1]

# Seeded randomised cross-check of membership semantics against the O(n) reference
rng = random.Random(350)
for trial in range(300):
    fast, ref = RandomizedSet(random.Random(trial)), BruteSet()
    for _ in range(60):
        op = rng.choice(["i", "i", "r", "g"])
        x = rng.randint(0, 9)
        if op == "i":
            assert fast.insert(x) == ref.insert(x)
        elif op == "r":
            assert fast.remove(x) == ref.remove(x)
        elif ref.items:
            assert fast.get_random() in ref.items
        assert sorted(fast.items) == sorted(ref.items)
        assert all(fast.items[i] == v for v, i in fast.pos.items())
        assert len(fast.pos) == len(fast.items)
print("cross-check passed: 300 random op sequences (18,000 ops)")

# Uniformity check (seeded): 4 elements, 40,000 draws, each should be near 10,000
s = RandomizedSet(random.Random(7))
for v in (5, 6, 7, 8):
    s.insert(v)
s.remove(6); s.insert(9)
c = Counter(s.get_random() for _ in range(30000))
print("draw counts over {5,7,8,9}:", dict(sorted(c.items())))
assert set(c) == {5, 7, 8, 9} and all(abs(v - 7500) < 400 for v in c.values())
```

**Output (my run):**

```text
True True True getRandom x5 -> [2, 2, 2, 2, 2]
last-element removal and re-insert OK
buggy remove-last leaves pos = {1: 0, 2: 1} items = [1] (ghost key 2)
cross-check passed: 300 random op sequences (18,000 ops)
draw counts over {5,7,8,9}: {5: 7512, 7: 7496, 8: 7525, 9: 7467}
```

**Edge cases:**
- Remove the only element, remove the last element, remove a missing value (return False).
- Insert a duplicate (return False, no change).
- `get_random` on an empty collection: the prompt does not define it. Say you would raise or assume it is never called. The code raises `ValueError` from `randrange(0)`.
- Negative values and 0 are fine as keys.

**Follow-ups:**
- *Duplicates allowed?* Use value to set of indices; see Q47.
- *Why not a set with random pop?* `set.pop` is arbitrary, not uniform random, and it removes the element.
- *Thread safety?* None here. You would need a lock around the list and dict together.

**Common mistakes:**
- Deleting `pos[x]` before re-pointing `pos[last]` when x is last: a ghost key remains. The "Buggy" class in the code shows `pos = {1: 0, 2: 1}` with `items = [1]`.
- Using `list.remove` or `index` in a loop.
- Forgetting to update the moved element's index.
- Testing randomness with one draw: use many draws and compare counts, as the code does.

---

### Q36 ⭐⭐ 🟡 Subarray XOR equals k. Given a list of non-negative integers and a target k, count the contiguous subarrays whose bitwise XOR equals k. Adapt the prefix-sum hashmap idea to prefix XOR and explain which algebraic property makes the complement lookup valid. Example: nums=[4,2,2,6,4], k=6 -> 4.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Prefix sums with a hashmap, using XOR in place of addition. Same shape as Subarray Sum Equals K (Q13).

**Say this first (1 line):** "XOR undoes itself, so the XOR of a slice is `prefix[j] ^ prefix[i]`; I count how many earlier prefixes equal `current_prefix ^ k`."

**Brute force:** For each start i, extend j and keep a running XOR. Count matches. O(n^2) time, O(1) space.

**Optimal:**
- Let `P[j]` be the XOR of the first j elements, with `P[0] = 0`.
- The slice `i..j-1` has XOR `P[j] ^ P[i]`.
- We want `P[j] ^ P[i] == k`. XOR both sides by `P[i] ^ k`: `P[i] == P[j] ^ k`. That works because XOR is associative, commutative, has identity 0 and every value is its own inverse (`a ^ a == 0`). In sum-language, XOR is both addition and subtraction.
- Seed `seen[0] = 1` for the empty prefix.
- For each x: `pref ^= x`, `ans += seen[pref ^ k]`, `seen[pref] += 1`. Look up before inserting.
- Invariant: `seen` holds the counts of all prefixes before the current position.

**Complexity:** Time O(n) expected, one pass with O(1) dict work. Space O(n) for distinct prefix XORs. Since values are non-negative and bounded by some B, distinct prefixes are fewer than the next power of two above B. That bounds the dict size when values are small.

**Dry run:** `[4,2,2,6,4]`, k=6.
- Prefixes: 4, 6, 4, 2, 6. Start `seen={0:1}`.
- 4: look for `4^6 = 2`: 0. seen {0:1, 4:1}.
- 2: pref = 6, look for `6^6 = 0`: 1. ans 1 (the slice `[4,2]`). seen[6] = 1.
- 2: pref = 4, look for 2: 0. seen[4] = 2.
- 6: pref = 2, look for `2^6 = 4`: 2. ans 3 (the slices `[2,2,6]` and `[6]`). seen[2] = 1.
- 4: pref = 6, look for 0: 1. ans 4 (the whole list). Answer 4. The prompt example is correct, and the code prints the four subarrays.

**Code:**

```python
import random
from functools import reduce
from collections import defaultdict


def brute(nums, k):
    n = len(nums)
    cnt = 0
    for i in range(n):
        x = 0
        for j in range(i, n):
            x ^= nums[j]
            cnt += (x == k)
    return cnt


def sub_xor_k(nums, k):
    """prefix[j] ^ prefix[i] == k  <=>  prefix[i] == prefix[j] ^ k (XOR is its own inverse)."""
    seen = defaultdict(int)
    seen[0] = 1
    pref = ans = 0
    for x in nums:
        pref ^= x
        ans += seen[pref ^ k]
        seen[pref] += 1
    return ans


ex = [4, 2, 2, 6, 4]
print(ex, "k=6 ->", sub_xor_k(ex, 6))
assert sub_xor_k(ex, 6) == 4

# The four subarrays, by brute force
subs = [ex[i:j + 1] for i in range(len(ex)) for j in range(i, len(ex))
        if reduce(lambda a, b: a ^ b, ex[i:j + 1]) == 6]
print("subarrays with XOR 6:", subs)
assert len(subs) == 4

# Edge cases
assert sub_xor_k([], 0) == 0
assert sub_xor_k([0], 0) == 1
assert sub_xor_k([5], 5) == 1
assert sub_xor_k([5], 4) == 0
assert sub_xor_k([3, 3], 0) == 1          # k = 0 counts pairs of equal prefixes
assert sub_xor_k([0, 0, 0], 0) == 6
assert sub_xor_k([1, 2, 3], 0) == 1       # 1^2^3 == 0
assert sub_xor_k([7] * 5, 7) == 9         # odd-length subarrays of five 7s: 5+3+1
assert sub_xor_k([10**9, 10**9, 5], 5) == 2

rng = random.Random(36)
for _ in range(1500):
    nums = [rng.randint(0, 15) for _ in range(rng.randint(0, 14))]
    k = rng.randint(0, 15)
    assert sub_xor_k(nums, k) == brute(nums, k), (nums, k)
print("cross-check passed: 1500 random lists")
```

**Output (my run):**

```text
[4, 2, 2, 6, 4] k=6 -> 4
subarrays with XOR 6: [[4, 2], [4, 2, 2, 6, 4], [2, 2, 6], [6]]
cross-check passed: 1500 random lists
```

**Edge cases:**
- Empty list: 0.
- `k = 0`: counts slices whose XOR is 0, which is pairs of equal prefixes. The seed `{0:1}` handles slices starting at index 0.
- Elements equal to 0 add no information: they create equal consecutive prefixes.
- Large values: Python ints are arbitrary precision, so no overflow worry.
- Single element equal to k.

**Follow-ups:**
- *Same idea with AND or OR?* No. They are not invertible, so the complement lookup is invalid.
- *Longest subarray with XOR k?* Store the first index of each prefix instead of a count.
- *Why does `k = 0` still work?* The lookup `pref ^ 0 = pref` finds earlier equal prefixes, which is exactly what XOR 0 means.

**Common mistakes:**
- Looking up `pref - k` or `pref + k`. The inverse of XOR is XOR.
- Missing `seen[0] = 1`.
- Updating `seen` before the lookup (counts empty slices when `k = 0`).
- Treating a sliding window as valid: XOR is not monotone, so it is not.

---

### Q37 ⭐ 🟡 Python dict and set internals. Explain how a CPython dict stores entries (hash table plus a dense entries array), what insertion order guarantee holds since which version, what the load factor and resize behaviour mean for amortised O(1), why keys must be hashable and consistent with equality, and why mutating a dict while iterating it raises an error. Show a short demo of each claim. Say where your knowledge ends (probing details change between versions). Example check: {1:'a',2:'b'} keeps 1 before 2 after deleting and reinserting 1? Show it moves to the end.
**Asked at:** Python dict and set internals explainers (designgurus.io, a discuss.python.org thread, medium and dev.to posts, CPython dictobject.c excerpts; snippets only, not opened; sources disagree on probing details so verify against current CPython docs); interview-style Python Q&A, not company reports

**Pattern:** Hash table internals, explained with runnable demos. Not an algorithm question: the interviewer wants correct claims and honest limits.

**Say this first (1 line):** "A CPython dict is an open-addressing hash table of small indexes pointing into a dense, insertion-ordered entries array; it resizes geometrically, which is why inserts are amortised O(1)."

**Brute force:** The naive mental model is "a dict is a list of buckets with chained lists", or "a dict is a list of pairs you scan". Scanning is O(n) per lookup. Chaining is how Java's HashMap and textbooks do it, not how CPython does it.

**Optimal:** (what I would say, each claim backed by a demo in the code)
- **Layout.** Two arrays. A sparse index table of small ints (1, 2, 4 or 8 bytes each, depending on size) and a dense array of `(hash, key, value)` entries in insertion order. Lookup: hash, take the slot from the index table, follow it to the entry, compare hash and then key (identity first, then `==`). Collisions are resolved by probing to another slot (open addressing with a perturbation scheme that mixes in the higher hash bits). I will not claim exact probe formulas: they are an implementation detail that has changed between versions.
- **Order.** Insertion order was an implementation detail of CPython 3.6 and is a language guarantee since 3.7. Updating an existing key keeps its position. Deleting and reinserting moves the key to the end. The prompt check: `{1:'a',2:'b'}` becomes `[2, 1]`. `popitem()` removes the last inserted.
- **Load factor and resize.** The table is kept at most about two-thirds full. When it fills, it is rebuilt at a larger size and every entry is reinserted. Growth is geometric, so the total rehash work over n inserts is O(n), which gives amortised O(1) per insert with an occasional O(n) spike. The demo prints the sizes where `getsizeof` jumps: after 5, 10, 21, 42, 85, 170 keys, i.e. two-thirds of 8, 16, 32, 64, 128, 256.
- **Hashability.** Keys must have a stable hash, and `a == b` must imply `hash(a) == hash(b)`. Otherwise equal keys land in different slots. That is why lists, sets and dicts (mutable, `__eq__` by content) are unhashable. Defining `__eq__` without `__hash__` sets `__hash__` to None. Mutating a key that is in a dict changes its hash and the entry becomes unreachable. Also `1`, `1.0` and `True` are the same key.
- **Mutation during iteration.** The iterator tracks the dict's size. If it changes (add or delete), Python raises `RuntimeError: dictionary changed size during iteration`. Changing the value of an existing key is allowed. Safe patterns: iterate `list(d)`, or build a new dict.
- **Where my knowledge ends.** Exact growth factors, the probing formula, the key-sharing dicts for instances, the split-table layout and the free-list tricks have all changed across versions (3.6, 3.11, 3.13). Check `dictobject.c` for the version you target. Set internals differ too: sets store hashes and keys only, have no order guarantee, and use a different probing and resize policy.

**Complexity:** Lookup, insert and delete are O(1) on average and O(n) worst case (every key collides). Resizes make a single insert O(n) occasionally, O(1) amortised. Memory: the dense entries array plus the index table. A dict costs more per item than a list but far less than a chained table.

**Dry run:** Reinsert example. Start `{1:'a', 2:'b'}`: entries `[(1,'a'), (2,'b')]`. `del d[1]`: entry 0 is marked deleted (a hole), the dict now yields `[2]`. `d[1] = 'a'`: appended as entry 2, so iteration order is `[2, 1]`. (The hole is reclaimed at the next resize.)

**Code:**

```python
import sys

# 1. Insertion order and the reinsert example from the prompt
d = {1: 'a', 2: 'b'}
del d[1]
d[1] = 'a'
print("1) after delete + reinsert of 1:", list(d))
assert list(d) == [2, 1]
d2 = {1: 'a', 2: 'b'}
d2[1] = 'z'                                   # updating an existing key keeps its slot
print("   update in place keeps position:", list(d2))
assert list(d2) == [1, 2]
print("   popitem is LIFO:", {1: 'a', 2: 'b', 3: 'c'}.popitem())

# 2. Resize behaviour: getsizeof jumps in steps; growth is geometric, so inserts are amortised O(1)
d, last, jumps = {}, sys.getsizeof({}), []
for i in range(200):
    d[i] = i
    s = sys.getsizeof(d)
    if s != last:
        jumps.append((len(d), s))
        last = s
print("2) (len when the table grew, getsizeof bytes):", jumps)
assert len(jumps) < 12                         # ~10 resizes for 200 keys, not 200
assert jumps[-1][0] < 200

# 3. Hashable and consistent with equality
for bad in ([1], {1}, {'a': 1}):
    try:
        {bad: 1}
    except TypeError as e:
        print("3) unhashable key:", type(bad).__name__, "->", e)
print("   1, 1.0 and True are one key:", {1: 'x', 1.0: 'y', True: 'z'})
assert {1: 'x', 1.0: 'y', True: 'z'} == {1: 'z'}


class OnlyEq:
    def __eq__(self, other):
        return True
print("   defining __eq__ alone sets __hash__ to", OnlyEq.__hash__)
assert OnlyEq.__hash__ is None


class Bad:                                     # hash NOT consistent with equality
    def __init__(self, v): self.v = v
    def __eq__(self, o): return self.v == o.v
    def __hash__(self): return id(self)
s = {Bad(1)}
print("   equal objects, different hashes -> Bad(1) in {Bad(1)}:", Bad(1) in s)
assert Bad(1) not in s


class Mut:                                     # mutating a key changes its hash: lost entry
    def __init__(self, v): self.v = v
    def __eq__(self, o): return self.v == o.v
    def __hash__(self): return hash(self.v)
m = Mut(1)
dm = {m: 'x'}
m.v = 2
print("   after mutating the key, lookup by the same object:", m in dm, "| len still", len(dm))
assert m not in dm and len(dm) == 1

# 4. Mutating size while iterating
d = {1: 'a', 2: 'b', 3: 'c'}
try:
    for k in d:
        d[k + 10] = 'new'
except RuntimeError as e:
    print("4) add during iteration ->", e)
d = {1: 'a', 2: 'b', 3: 'c'}
try:
    for k in d:
        del d[k]
except RuntimeError as e:
    print("   delete during iteration ->", e)
d = {1: 'a', 2: 'b', 3: 'c'}
for k in d:
    d[k] = d[k].upper()                        # changing a value does not change size: allowed
print("   updating values while iterating is fine:", d)
d = {k: v for k, v in d.items() if k != 2}      # safe pattern: build a new dict
for k in list(d):                               # or iterate over a snapshot
    if k == 1:
        del d[k]
print("   safe patterns leave:", d)
assert d == {3: 'C'}

# 5. Sets use the same hash-table idea but keep no insertion order and no values
print("5) list({3, 1, 2}) =", list({3, 1, 2}), "(slot order of the small-int hashes, not insertion order; never rely on set order)")
print("   the growth points above are 6, 11, 22, 43, 86, 171: each is one past 2/3 of a power-of-two table (5/8, 10/16, 21/32, 42/64, 85/128, 170/256)")
```

**Output (my run):**

```text
1) after delete + reinsert of 1: [2, 1]
   update in place keeps position: [1, 2]
   popitem is LIFO: (3, 'c')
2) (len when the table grew, getsizeof bytes): [(1, 224), (6, 352), (11, 632), (22, 1168), (43, 2264), (86, 4688), (171, 9304)]
3) unhashable key: list -> unhashable type: 'list'
3) unhashable key: set -> unhashable type: 'set'
3) unhashable key: dict -> unhashable type: 'dict'
   1, 1.0 and True are one key: {1: 'z'}
   defining __eq__ alone sets __hash__ to None
   equal objects, different hashes -> Bad(1) in {Bad(1)}: False
   after mutating the key, lookup by the same object: False | len still 1
4) add during iteration -> dictionary changed size during iteration
   delete during iteration -> dictionary changed size during iteration
   updating values while iterating is fine: {1: 'A', 2: 'B', 3: 'C'}
   safe patterns leave: {3: 'C'}
5) list({3, 1, 2}) = [1, 2, 3] (slot order of the small-int hashes, not insertion order; never rely on set order)
   the growth points above are 6, 11, 22, 43, 86, 171: each is one past 2/3 of a power-of-two table (5/8, 10/16, 21/32, 42/64, 85/128, 170/256)
```

**Edge cases:**
- `1 == 1.0 == True`: one key, and the first inserted key object is kept while the value is overwritten.
- `nan` as a key: `nan != nan`, but lookup by the same object works through the identity shortcut.
- Tuples are hashable only if all their items are.
- Deleting keys leaves holes; a dict that shrinks a lot does not shrink until it is rebuilt.

**Follow-ups:**
- *Is a dict thread safe?* Single operations are atomic under the GIL (and in the free-threaded build there is internal locking), but "check then set" is not.
- *Why does `set` give a different order?* It does not keep insertion order. The order is by slot, which depends on hashes.
- *Key-sharing dictionaries?* Instance `__dict__`s of the same class can share key tables to save memory. A detail, version dependent.

**Common mistakes:**
- Saying "dict is a binary tree" or "dict uses linked-list buckets in CPython".
- Saying order is guaranteed in all Pythons: 3.7 and later only (3.6 only in CPython).
- Claiming an exact load factor or probe sequence as a spec.
- Mutating a dict inside a `for` loop over itself.
- Using a mutable object as a key and then changing it.

---

### Q38 ⭐ 🟡 Hash collisions and randomised hashing. Explain what happens on a collision in a Python dict, why hash(-1) == hash(-2) in CPython, why str hashes change between runs (PYTHONHASHSEED) while int hashes do not, and what an adversarial input can do to a hash table's worst case. Demonstrate with a class that defines a constant __hash__ and measure how insertion cost grows (label timings as sandbox-only). Example: 5,000 keys all hashing to 0.
**Asked at:** Python dict and set internals explainers (designgurus.io, a discuss.python.org thread, medium and dev.to posts, CPython dictobject.c excerpts; snippets only, not opened; sources disagree on probing details so verify against current CPython docs); interview-style Python Q&A, not company reports

**Pattern:** Hash table collisions and worst case. Hashing gives O(1) on average only when hashes spread. The adversarial case degrades every operation to a scan of a probe chain.

**Say this first (1 line):** "A collision just means two keys want the same slot; Python probes to the next candidate slot and compares with `==`, so correctness holds but if everything collides each operation costs O(n) and n inserts cost O(n^2)."

**Brute force:** The wrong mental model: "on a collision the dict loses or overwrites a key". It does not. Equality decides: same hash and equal keys are one key, same hash and unequal keys coexist.

**Optimal:** (the claims, each shown in the code)
- **Collision handling.** Open addressing. Compare stored hash, then identity, then `==`. A colliding key is placed at another probed slot. The demo has five keys with `__hash__` returning 0, and all five are found correctly.
- **`hash(-1) == hash(-2)`.** In CPython's C API, a hash function returns -1 to signal an error. So a real hash of -1 is remapped to -2. For ints, `hash(x)` is otherwise `x` modulo `2**61 - 1` (on 64-bit builds), so `-1` becomes `-2` and collides with `-2`. A one-off, harmless in practice.
- **Strings change between runs, ints do not.** `str` and `bytes` hashes are salted with a random per-process key (SipHash, `PYTHONHASHSEED`). Ints hash to their value. The demo launches child interpreters with seed 1 and 2: the string hash differs, the int hash is `12345` in both. Setting `PYTHONHASHSEED=0` disables randomisation (useful for reproducible tests, not for production). Note the code runs with `-I`, which ignores environment variables in the parent; the child processes pass the variable explicitly.
- **Adversarial input.** If an attacker knows the hash function, they pick many keys that land in the same slots: the old hash-flooding denial of service. Salting the hash stops precomputed collisions for strings. But ints are not salted. Since `hash(x) = x mod (2**61 - 1)`, the keys `M, 2M, 3M, ...` with `M = 2**61 - 1` all hash to 0. The demo shows it. For competitive-style tests, the defence is a custom wrapper or a random xor on integer keys.
- **Measured effect.** Insert n objects with a constant `__hash__` (identity equality, compared in C) into a set. The time per insert grows with n, so total time grows about quadratically. Timings are sandbox-only. The shape matters, not the digits.

**Complexity:** Average O(1) per operation with a well-spread hash. Worst case O(n) per operation, so O(n^2) for n inserts, when all keys share a probe path. Reason from the code: insert number k probes through about k occupied slots, so the total is 1 + 2 + ... + n = n(n+1)/2.

**Dry run:** Five keys with hash 0. Insert key 1: slot 0. Key 2: slot 0 is taken and not equal, probe to the next slot. Key 3: probes slot 0 (taken), then the next (taken), then a free one. Each new key walks past all earlier ones. Lookup of the fifth key compares against up to four others first.

**Code:**

```python
import subprocess
import sys
import time

# 1. Collisions are resolved by probing and then comparing keys with ==
class K:
    def __init__(self, v): self.v = v
    def __hash__(self): return 0               # every key collides
    def __eq__(self, o): return self.v == o.v

d = {K(i): i for i in range(5)}
print("1) all-collide dict still correct:", d[K(3)], len(d), K(9) in d)
assert d[K(3)] == 3 and len(d) == 5 and K(9) not in d

# 2. hash(-1) == hash(-2)
print("2) hash(-1) =", hash(-1), "| hash(-2) =", hash(-2), "| hash(-3) =", hash(-3))
assert hash(-1) == hash(-2) == -2
print("   small ints hash to themselves:", [hash(i) for i in (0, 1, 2, 1000)])
M = 2**61 - 1                                  # CPython int hash modulus on 64-bit builds
print("   int hash is x mod (2**61 - 1): hash(M) =", hash(M), ", hash(M + 5) =", hash(M + 5), ", hash(-M - 1) =", hash(-M - 1))
assert sys.hash_info.modulus == M and hash(M) == 0 and hash(M + 5) == 5

# 3. str hashes change between runs; int hashes do not
def run(seed, expr):
    out = subprocess.run([sys.executable, "-P", "-c", f"print({expr})"], env={"PYTHONHASHSEED": seed},
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()
s1, s2, s3 = run("1", "hash('apple')"), run("2", "hash('apple')"), run("1", "hash('apple')")
i1, i2 = run("1", "hash(12345)"), run("2", "hash(12345)")
print("3) hash('apple') under seed 1 vs seed 2 equal?", s1 == s2, "| seed 1 twice equal?", s1 == s3)
print("   hash(12345) under seed 1 vs 2:", i1, i2)
assert s1 != s2 and s1 == s3 and i1 == i2 == "12345"
print("   str ordering of a set can differ between runs:",
      run("1", "list({'a','b','c','d','e'})") != run("2", "list({'a','b','c','d','e'})"))

# 4. Adversarial inputs: real ints that all collide (no custom class needed)
keys = [i * M for i in range(1, 6)]
print("4) hashes of 1*M..5*M:", [hash(k) for k in keys])
assert all(hash(k) == 0 for k in keys)

# 5. Insertion cost with a constant __hash__ vs a normal hash (sandbox timings, not proof of big-O)
class Const:
    __slots__ = ()
    def __hash__(self): return 0               # no __eq__: default identity compare, done in C

class Normal:
    __slots__ = ()                             # default hash from id(): spreads well

def build(cls, n):
    objs = [cls() for _ in range(n)]
    t = time.perf_counter()
    s = set()
    for o in objs:
        s.add(o)
    return time.perf_counter() - t

print("5) insert n keys into a set (sandbox-only timings, seconds):")
print("   n      constant-hash   normal-hash")
rows = []
for n in (625, 1250, 2500, 5000):
    tc, tn = min(build(Const, n) for _ in range(3)), min(build(Normal, n) for _ in range(3))
    rows.append((n, tc, tn))
    print(f"   {n:<6} {tc:12.5f}   {tn:12.5f}")
growth = rows[-1][1] / rows[0][1]
print(f"   constant-hash time grew about {growth:.0f}x for 8x the keys; the normal hash grew about {rows[-1][2] / rows[0][2]:.0f}x")
assert growth > 12                              # far above linear (8x); quadratic would be ~64x
```

**Output (my run):**

```text
1) all-collide dict still correct: 3 5 False
2) hash(-1) = -2 | hash(-2) = -2 | hash(-3) = -3
   small ints hash to themselves: [0, 1, 2, 1000]
   int hash is x mod (2**61 - 1): hash(M) = 0 , hash(M + 5) = 5 , hash(-M - 1) = -2
3) hash('apple') under seed 1 vs seed 2 equal? False | seed 1 twice equal? True
   hash(12345) under seed 1 vs 2: 12345 12345
   str ordering of a set can differ between runs: True
4) hashes of 1*M..5*M: [0, 0, 0, 0, 0]
5) insert n keys into a set (sandbox-only timings, seconds):
   n      constant-hash   normal-hash
   625         0.00155        0.00001
   1250        0.00678        0.00004
   2500        0.02416        0.00006
   5000        0.11170        0.00009
   constant-hash time grew about 72x for 8x the keys; the normal hash grew about 9x
```

**Edge cases:**
- `__eq__` defined in Python makes the collision cost much worse than the C identity check used in the timing demo.
- `hash(-1)` vs a custom `__hash__` that returns -1: Python converts it to -2.
- Floats that are integers hash like the equal int (`hash(2.0) == hash(2)`).
- Tuples of ints hash by combining item hashes, so adversarial tuples are harder but possible.

**Follow-ups:**
- *Why not just use a tree for collisions (like Java's HashMap)?* CPython chose open addressing and salted hashes for speed and simplicity. Java treeifies long buckets to cap worst case at O(log n).
- *How do you defend a service?* Randomised hashing, limits on the number of keys from one request, and rate limits. For integers, xor with a per-process random value.
- *Is the timing proof of big-O?* No. It shows a trend on one machine. The O(n^2) claim comes from the probing argument above.

**Common mistakes:**
- Claiming a collision overwrites data.
- Saying all hashes are randomised: ints are not, and `PYTHONHASHSEED` affects only str, bytes and datetime-family types.
- Defining `__eq__` and forgetting `__hash__`, or the reverse.
- Relying on hash values across runs (storing `hash(s)` to a file).

---

### Q39 ⭐ 🟡 Counter and defaultdict idioms and traps. List the idioms you use for frequency counting (Counter, defaultdict(int), dict.get, setdefault) and the traps: defaultdict inserts a key on a read, Counter arithmetic drops non-positive counts, Counter.most_common ordering of ties, defaultdict(list) shared state mistakes, and `in` on a defaultdict. Show one runnable example per trap. Example: c = Counter('aab'); c - Counter('abbb') keeps which keys?
**Asked at:** Python dict and set internals explainers (designgurus.io, a discuss.python.org thread, medium and dev.to posts, CPython dictobject.c excerpts; snippets only, not opened; sources disagree on probing details so verify against current CPython docs); interview-style Python Q&A, not company reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Frequency counting idioms and their traps. One runnable demo per trap.

**Say this first (1 line):** "Counter for plain counting, defaultdict for grouping into lists, `dict.get` for one-offs; and I watch four traps: reads that insert, arithmetic that drops zeros, tie order, and shared mutable defaults."

**Brute force:** Repeated `list.count(x)` per distinct x: O(n * distinct). Or `if x in d: d[x] += 1 else: d[x] = 1`, which is correct but verbose.

**Optimal:** the idiom list:
- `Counter(iterable)`: the default. Missing keys read as 0 without being inserted. Has `most_common`, `update` (adds), `subtract`, `total()`.
- `defaultdict(int)`: `d[x] += 1`. Good when you also need other value types.
- `d[x] = d.get(x, 0) + 1`: no import, explicit.
- `d.setdefault(k, []).append(v)`: grouping without defaultdict. It builds the default argument every call, so it is slower for lists.

The traps:
1. **Counter arithmetic drops non-positive counts.** The prompt example: `Counter('aab') - Counter('abbb')` keeps only `a: 1`. The `b` count would be -2 and is silently dropped. `subtract` keeps negatives; unary `+` strips them. `+` and `-` between Counters always return positive-only results.
2. **defaultdict inserts on read.** `d['ghost']` creates the key. `in` and `.get` do not. A Counter read returns 0 without inserting. So a debug print that reads a missing key can change `len(d)`.
3. **`most_common` ties** come out in first-insertion order (the sort is stable), not key order. Use `sorted(items, key=lambda kv: (-kv[1], kv[0]))` for a fixed order.
4. **Shared mutable defaults.** `dict.fromkeys(keys, [])` and `[[0]] * 3` share one object. `defaultdict(list)` is safe because it calls the factory per key. A factory that returns a pre-built list is not.
5. **`default_factory` only runs in `__getitem__`**, so `.get` returns None, not the default.
6. **`Counter.update` adds; `dict.update` replaces.**

**Complexity:** Building a Counter is O(n) expected. `most_common(k)` is O(n log k) (heap) and `most_common()` without k is O(n log n). Space O(distinct).

**Dry run:** `c = Counter('aab')` is `{a:2, b:1}`. `Counter('abbb')` is `{a:1, b:3}`. Subtract per key: a: 2-1 = 1 (kept), b: 1-3 = -2 (dropped). Result `Counter({'a': 1})`. The prompt's answer: only `'a'`.

**Code:**

```python
from collections import Counter, defaultdict

words = ['b', 'a', 'b', 'c', 'a', 'b']

# Idioms: all give the same counts
c1 = Counter(words)
c2 = defaultdict(int)
for w in words:
    c2[w] += 1
c3 = {}
for w in words:
    c3[w] = c3.get(w, 0) + 1
c4 = {}
for w in words:
    c4.setdefault(w, [0])[0] += 1               # setdefault is for list/set values, shown only for contrast
assert dict(c1) == dict(c2) == c3 == {k: v[0] for k, v in c4.items()}
print("idioms agree:", dict(c1))

# Trap 1: Counter arithmetic drops non-positive counts (the prompt's example)
r = Counter('aab') - Counter('abbb')
print("1) Counter('aab') - Counter('abbb') ->", r)
assert r == Counter({'a': 1})
s = Counter('aab')
s.subtract(Counter('abbb'))
print("   .subtract keeps negatives         ->", s)
assert s == {'a': 1, 'b': -2}
print("   unary + strips them               ->", +s, "| total() =", s.total())
print("   '+' also drops: Counter(a=1) + Counter(a=-3) ->", Counter(a=1) + Counter(a=-3))

# Trap 2: defaultdict inserts on a READ; Counter and plain dict do not
dd = defaultdict(int)
_ = dd['ghost']
print("2) defaultdict read inserts a key:", dict(dd), "| 'ghost' in dd:", 'ghost' in dd)
assert 'ghost' in dd
cc = Counter()
_ = cc['ghost']
print("   Counter read returns 0, no insert:", dict(cc))
assert 'ghost' not in cc
dd2 = defaultdict(int)
print("   `in` on a defaultdict never inserts:", 'x' in dd2, dict(dd2))
assert 'x' not in dd2 and dd2.get('x') is None and 'x' not in dd2   # .get also safe

# Trap 3: most_common ties follow first-insertion order (sort is stable), not key order
t = Counter('zzyyxx')
print("3) Counter('zzyyxx').most_common():", t.most_common())
assert t.most_common() == [('z', 2), ('y', 2), ('x', 2)]
print("   explicit tie-break by key        :", sorted(t.items(), key=lambda kv: (-kv[1], kv[0])))

# Trap 4: shared mutable defaults
bad = dict.fromkeys('ab', [])
bad['a'].append(1)
print("4) dict.fromkeys('ab', []) shares ONE list:", bad)
assert bad['b'] == [1]
grid = [[0]] * 3
grid[0][0] = 9
print("   [[0]] * 3 aliases rows:", grid)
assert grid == [[9], [9], [9]]
good = defaultdict(list)
good['a'].append(1)
print("   defaultdict(list) makes a fresh list per key:", dict(good), "| 'b' separate:", good['b'], dict(good))
shared = []
oops = defaultdict(lambda: shared)
oops['a'].append(1)
print("   factory returning one shared object is the same bug:", oops['b'])
assert oops['b'] == [1]

# Trap 5: defaultdict default_factory is only used by __getitem__
dd3 = defaultdict(list)
print("5) .get on missing key ->", dd3.get('k'), "| dd3['k'] ->", dd3['k'], "| now:", dict(dd3))

# Trap 6: Counter.update adds, dict.update replaces
x = Counter(a=2)
x.update({'a': 3})
y = dict(a=2)
y.update({'a': 3})
print("6) Counter.update adds:", dict(x), "| dict.update replaces:", y)
assert x['a'] == 5 and y['a'] == 3
```

**Output (my run):**

```text
idioms agree: {'b': 3, 'a': 2, 'c': 1}
1) Counter('aab') - Counter('abbb') -> Counter({'a': 1})
   .subtract keeps negatives         -> Counter({'a': 1, 'b': -2})
   unary + strips them               -> Counter({'a': 1}) | total() = -1
   '+' also drops: Counter(a=1) + Counter(a=-3) -> Counter()
2) defaultdict read inserts a key: {'ghost': 0} | 'ghost' in dd: True
   Counter read returns 0, no insert: {}
   `in` on a defaultdict never inserts: False {}
3) Counter('zzyyxx').most_common(): [('z', 2), ('y', 2), ('x', 2)]
   explicit tie-break by key        : [('x', 2), ('y', 2), ('z', 2)]
4) dict.fromkeys('ab', []) shares ONE list: {'a': [1], 'b': [1]}
   [[0]] * 3 aliases rows: [[9], [9], [9]]
   defaultdict(list) makes a fresh list per key: {'a': [1]} | 'b' separate: [] {'a': [1], 'b': []}
   factory returning one shared object is the same bug: [1]
5) .get on missing key -> None | dd3['k'] -> [] | now: {'k': []}
6) Counter.update adds: {'a': 5} | dict.update replaces: {'a': 3}
```

**Edge cases:**
- Counting unhashable items (lists): convert to tuples first.
- Counter of an empty iterable is falsy; `max(counter.values())` on it raises.
- Counter keys are not required to be strings; floats such as `1` and `1.0` merge.
- Python 3.10+: `Counter.total()` sums the values (negatives included).

**Follow-ups:**
- *Counter equality?* Since 3.10, missing and zero counts compare equal (`Counter(a=0) == Counter()` is True).
- *Multiset operations?* `&` is the minimum of counts, `|` the maximum, both drop non-positive results.
- *Speed?* Counter's counting loop is implemented in C for iterables, so `Counter(list)` beats a Python `for` loop.

**Common mistakes:**
- Using `d[key]` on a defaultdict to "check" a key.
- Expecting `c1 - c2` to leave negative counts.
- Expecting ties in `most_common` to be alphabetical.
- Building a 2D structure with `[[]] * n`.
- Mutating the dict while iterating `d.items()` after a read that inserts.

---

### Q40 ⭐ 🟡 Sorting versus hashing trade-offs. For duplicate detection, pair-sum lookup and anagram grouping, compare a hash approach with a sort approach on time, extra space, mutation of input, determinism and worst case, and decide which you would pick for n = 10^7 integers on a memory-limited machine. Back one claim with a sandbox-only timing and say it is not proof of big-O. Example: detect duplicates in a list of 10^7 ints with 200 MB of memory.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Choosing between hashing and sorting under real constraints (time, memory, mutation, determinism, worst case). The same three problems, two tools.

**Say this first (1 line):** "Hash is O(n) average with O(n) extra space; sort is O(n log n) with little or no extra space if you may mutate; with 10^7 ints and 200 MB, memory decides, not speed."

**Brute force:** Compare all pairs, O(n^2). Fine as the reference, hopeless at n = 10^7.

**Optimal:** the comparison table.

| Problem | Hash approach | Sort approach |
|---|---|---|
| Duplicate detection | set; stop at first repeat; O(n) avg time, O(n) space | sort, scan neighbours; O(n log n); `list.sort()` is O(1) extra but mutates, `sorted()` copies |
| Pair sum exists | set of seen values; look up `t - x` | sort, two pointers from both ends; indices are lost unless you sort `(value, index)` |
| Anagram grouping | dict keyed by sorted string or 26-count tuple | sort `(key, word)` pairs, cut runs of equal keys |

| Criterion | Hash | Sort |
|---|---|---|
| Time | O(n) average, O(n^2) adversarial worst case | O(n log n) guaranteed (Timsort) |
| Extra space | O(n), with a large constant (a set costs about 50 bytes per int in my run below) | O(1) in place, O(n) for a copy |
| Mutates input | no | yes if in place |
| Determinism | order of iteration depends on insertion; str hashes are salted per run but results are the same | fully deterministic, stable |
| Early exit | yes, on the first duplicate | no, sorting finishes first |
| Streaming | yes | no, needs all data |

**The 10^7 ints with 200 MB decision.**
- A Python `list` of 10^7 ints is about 80 MB of pointers plus 28 bytes per int object (values above 256), about 360 MB in total. It does not fit. Neither does a set (about 50 bytes per element by my measurement, so about 500 MB).
- Store the data as `array('q')` (8 bytes each, 80 MB) or read it in chunks.
- Option A, in place sort in a compact array: the standard library `array` has no sort, so you would use numpy (`ndarray.sort()`) if allowed. That is O(n log n) time, O(1) extra, but mutates.
- Option B, multi-pass partition (the code): pass p keeps only values with `x % P == p` in a set. Peak extra memory is about one P-th of the full set. With P = 8 and 10^7 values, each set has about 1.25 million items, so about 60 MB on my measured ratio. Total: 80 MB array + 60 MB set, under 200 MB. Cost: P scans of the data. It is exact, and exits early on a duplicate.
- Option C, if values are bounded (for example 0 to 10^9): a bitmap in a `bytearray` of 125 MB marks seen values in O(n).
- Option D, external: hash-partition to files on disk, then process each file in memory.
- My pick: B if stdlib only, A if numpy is allowed, C if the range is bounded.

**Complexity:** Hash O(n) expected time and O(n) space. Sort O(n log n) time (comparison lower bound) and O(1) to O(n) space. Partition O(P * n) time with O(n / P) extra space. Sandbox-only timings below: they show the constants on this machine and are not proof of big-O.

**Dry run:** `[7, 3, 9, 3]` with P = 2. Pass 0 (even values): none. Pass 1 (odd): 7, 3, 9 enter the set, then 3 is already there: duplicate found on pass 1. Memory held at most three values.

**Code:**

```python
import random
import time
import tracemalloc
from array import array
from collections import defaultdict
from itertools import groupby


# ---------- 1. duplicate detection ----------
def dup_brute(a):
    return any(a[i] == a[j] for i in range(len(a)) for j in range(i + 1, len(a)))

def dup_hash(a):                      # O(n) avg time, O(n) extra space, input untouched
    seen = set()
    for x in a:
        if x in seen:
            return True
        seen.add(x)
    return False

def dup_sort(a):                      # O(n log n) time, sorted() copy = O(n) space (list.sort() in place = O(1) extra but mutates)
    b = sorted(a)
    return any(b[i] == b[i + 1] for i in range(len(b) - 1))

def dup_partition(arr, parts):        # memory-limited: `parts` passes, each holds only ~n/parts values in a set
    for p in range(parts):
        seen = set()
        for x in arr:
            if x % parts == p:
                if x in seen:
                    return True
                seen.add(x)
    return False


# ---------- 2. pair-sum existence ----------
def pair_brute(a, t):
    return any(a[i] + a[j] == t for i in range(len(a)) for j in range(i + 1, len(a)))

def pair_hash(a, t):
    seen = set()
    for x in a:
        if t - x in seen:
            return True
        seen.add(x)
    return False

def pair_sort(a, t):                  # sort + two pointers; loses original indices unless you sort (value, index) pairs
    b = sorted(a)
    i, j = 0, len(b) - 1
    while i < j:
        s = b[i] + b[j]
        if s == t:
            return True
        if s < t:
            i += 1
        else:
            j -= 1
    return False


# ---------- 3. anagram grouping ----------
def group_hash(words):
    g = defaultdict(list)
    for w in words:
        g["".join(sorted(w))].append(w)
    return sorted(sorted(v) for v in g.values())

def group_sort(words):                # sort (key, word) pairs, then cut runs of equal keys
    keyed = sorted(("".join(sorted(w)), w) for w in words)
    return sorted(sorted(w for _, w in run) for _, run in groupby(keyed, key=lambda kw: kw[0]))

def group_brute(words):
    groups = []
    for w in words:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return sorted(sorted(g) for g in groups)


# ---------- edge cases ----------
assert dup_hash([]) is False and dup_sort([]) is False and dup_partition(array('q'), 4) is False
assert dup_hash([5]) is False and dup_sort([5]) is False
assert dup_hash([-3, 7, -3]) and dup_sort([-3, 7, -3]) and dup_partition(array('q', [-3, 7, -3]), 4)
assert pair_hash([], 0) is False and pair_sort([], 0) is False
assert pair_hash([5], 10) is False and pair_sort([5], 10) is False      # one element must not pair with itself
assert pair_hash([5, 5], 10) and pair_sort([5, 5], 10)
assert group_hash([]) == group_sort([]) == []
assert group_hash(['', '']) == group_sort(['', '']) == [['', '']]

# ---------- seeded cross-checks ----------
rng = random.Random(40)
for _ in range(1500):
    a = [rng.randint(-8, 8) for _ in range(rng.randint(0, 10))]
    t = rng.randint(-10, 10)
    d = dup_brute(a)
    assert dup_hash(a) == dup_sort(a) == dup_partition(array('q', a), 3) == d, a
    p = pair_brute(a, t)
    assert pair_hash(a, t) == pair_sort(a, t) == p, (a, t)
    w = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 4))) for _ in range(rng.randint(0, 8))]
    assert group_hash(w) == group_sort(w) == group_brute(w), w
print("cross-check passed: 1500 random cases across dup / pair-sum / anagram (hash, sort, brute agree)")

# ---------- sandbox-only memory and time at n = 10^6 (extrapolate by reasoning, not by trusting numbers) ----------
n = 1_000_000
arr = array('q', random.Random(1).sample(range(10**9), n))      # all distinct: no early exit, worst case for both
lst = list(arr)

def peak_extra(fn):
    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]
    tracemalloc.reset_peak()
    fn()
    peak = tracemalloc.get_traced_memory()[1] - base
    tracemalloc.stop()
    return peak / 1e6

print(f"\nsandbox-only, n = {n:,} distinct ints, extra peak memory beyond the input (MB):")
print(f"  set-based         : {peak_extra(lambda: dup_hash(lst)):7.1f}")
print(f"  sorted() copy     : {peak_extra(lambda: dup_sort(lst)):7.1f}")
print(f"  8-pass partition  : {peak_extra(lambda: dup_partition(arr, 8)):7.1f}")
print(f"  (input as list of ints: {(len(lst) * 8 + sum(x.__sizeof__() for x in lst)) / 1e6:.0f} MB; as array('q'): {arr.itemsize * len(arr) / 1e6:.0f} MB)")

def best(fn, reps=3):
    out = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        out.append(time.perf_counter() - t0)
    return min(out)

print(f"\nsandbox-only timings, seconds, n = {n:,} (a single machine, not proof of big-O):")
print(f"  set-based dup check : {best(lambda: dup_hash(lst)):.3f}")
print(f"  sorted + scan       : {best(lambda: dup_sort(lst)):.3f}")
print(f"  8-pass partition    : {best(lambda: dup_partition(arr, 8), 1):.3f}")
```

**Output (my run):**

```text
cross-check passed: 1500 random cases across dup / pair-sum / anagram (hash, sort, brute agree)

sandbox-only, n = 1,000,000 distinct ints, extra peak memory beyond the input (MB):
  set-based         :    50.3
  sorted() copy     :    12.0
  8-pass partition  :     8.8
  (input as list of ints: 36 MB; as array('q'): 8 MB)

sandbox-only timings, seconds, n = 1,000,000 (a single machine, not proof of big-O):
  set-based dup check : 0.109
  sorted + scan       : 0.223
  8-pass partition    : 0.321
```

Reading the numbers: the timings are one machine and one input, and the relative order can change with data size, cache and Python version. The memory numbers are measured at 10^6; the 10^7 figures above are a linear extrapolation (reasoned, not run).

**Edge cases:**
- Empty or single element: no duplicates, no pair.
- A pair of equal values summing to target (`[5,5]`, target 10) is valid, but a single `5` is not (no element reuse).
- Negative numbers: `x % P` is non-negative in Python, so partitioning is safe.
- Adversarial integers that all collide (see Q38) hurt the hash approach, not the sort.

**Follow-ups:**
- *Why not a Bloom filter?* It has false positives, so it cannot give an exact yes. It can prune before an exact check.
- *Sorted input already?* Then sort-based is O(n) and zero-space.
- *Distributed?* Hash-partition by key to machines, then each machine dedupes locally.

**Common mistakes:**
- Saying a set of 10^7 ints "is 80 MB". Python objects and the hash table cost far more.
- Using `sorted()` and calling it O(1) space.
- Sorting to find pair indices and losing the original positions.
- Treating the timing as proof that hash is always faster.

---

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

