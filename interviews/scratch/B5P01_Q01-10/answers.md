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
