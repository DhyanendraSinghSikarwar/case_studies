# Book 5 — Part 5: Binary search (including binary search on the answer)

**Topic:** Python DSA for product-company interviews: classic binary search and its loop invariants (closed versus half-open templates, lo<hi versus lo<=hi, mid rounding), lower and upper bound semantics and the bisect module (bisect_left, bisect_right, insort, the key= parameter on Python 3.10+), first and last position, search insert position, rotated sorted arrays (distinct values and with duplicates) and the minimum of a rotated array, peak element, mountain array search under a call budget, search in a 2D matrix (flattened and row-and-column sorted variants), integer square root, perfect square and integer k-th root, binary search on the answer (Koko eating bananas, capacity to ship packages, split array largest sum, allocate books, minimum days for bouquets, aggressive cows style max-min distance, cutting logs, k-th missing positive), median of two sorted arrays and the k-th element of two sorted arrays, k-th smallest in a sorted matrix, the median of a row-sorted matrix, k-th in a multiplication table and k-th smallest pair distance (search on value with counting), k closest elements, single element in a sorted array of pairs, exponential search in an array of unknown length, floating-point binary search and termination (fixed iterations versus epsilon: maximum average subarray, gas stations), and monotonic predicate design with counterexamples

**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 13, ⭐⭐ 16, ⭐ 11)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns binary search on indices, on values and on the answer, plus the bisect module. The greedy feasibility checks used as predicates (ship loading, cow placement, bouquet counting, split pieces) are only predicates here; the theory of why those greedy rules are optimal belongs to Part 8 (heaps, intervals, greedy). Part 1 owns hashing and the value-range plus Floyd solutions of find the duplicate number (cross-referenced only as 'Part 1 Q28', checked against its heading; the pair-distance question here is a different counting problem). Part 2 owns the two-pointer and window versions: longest mountain by one pass and the O(k) merge walk for the k-th element of two sorted lists (cross-referenced as 'Part 2 Q38, Q40', each checked against its heading; the questions here are the call-budget mountain search and the O(log) k-th element). Part 3 owns prefix queries with a sorted list and bisect and the rolling-hash plus binary-search longest repeated substring (cross-referenced as 'Part 3 Q36, Q40', each checked against its heading; the questions here contrast with them rather than repeat them). Part 7 owns binary search trees, Part 13 owns math and number theory and randomized algorithms (integer roots and square roots here are the binary-search forms only). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force or independent reference code (scratch/B5P05_wavea/check_examples.py, python3 -I) before freezing. Claims were tested exhaustively where they could be: exactly-k versus at-most-k splitting (400 random small cases), the is-bad call budget ceil(log2 n) for every n < 300 and every boundary, the two bisect templates on every monotone predicate with n < 12, the k-closest tie rule (3000 random small cases, tie-break by value versus by index gives the same list), k-th missing positive (1000 random), multiplication-table counting (all m, n <= 5 and every k), maximum average and gas-station predicates against brute force, the mountain search call count (worst observed 55 of the 100-call budget, including n = 10^4), the non-termination of an epsilon loop at eps = 1e-15 for x = 10**6, and that int(125 ** (1/3)) is 4 in CPython. The peak-element prompt states that its answer is NOT unique and the checker accepts any peak (both peaks of the second example were enumerated); the single-element prompt states that the lone value is unique by the statement. The prompts were written once, and all examples passed on the first full run of the checker. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org and neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part05_sources.md). Searches returned binary-search pattern guides and question roundups, a median-of-two-arrays explainer and candidate-reported Flipkart items on Naukri Code360 (an Allocate Books entry from 2021 and a rotated-array search entry; one aggregator, reports spanning 2015-2022); no Amazon India, Google or Microsoft report naming these problems was found (a jointaro page carried a Microsoft company filter but its content was not verified), so 'Asked at' tags name source types (pattern guides, practice lists, candidate-reported snippets, Python docs mirrors, editor knowledge of standard lists), not verified company reports. The bisect key= behaviour (key added in 3.10, not applied to the search value in bisect_left/bisect_right, applied to it in insort) rests on docs snippets plus a sandbox run on Python 3.13. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

### Q1 ⭐⭐⭐ 🟢 Classic binary search. `nums` is sorted ascending with distinct integers (1 <= len <= 10^5); given `target`, return its index or -1 in O(log n). Write it with the closed interval `lo, hi = 0, n - 1` and `while lo <= hi`; state the loop invariant (if target is present it lies in nums[lo..hi]) and why every branch shrinks the interval. Say why `mid = lo + (hi - lo) // 2` and `(lo + hi) // 2` behave identically in Python (integers do not overflow) and why the first form still matters in fixed-width languages. Example: [-1,0,3,5,9,12], 9 -> 4; the same list with 2 -> -1; [5], 5 -> 0; [5], 4 -> -1.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports

**Pattern:** Binary search on a sorted array. Sorted order lets one comparison throw away half the candidates.

**Say this first (1 line):** "Closed interval [lo, hi], loop while lo <= hi, and each step either returns or drops mid, so the interval always shrinks."

**Brute force:** Scan left to right. O(n) time, O(1) space. Correct, but ignores the sorted order.

**Optimal:**
- Invariant: if target is in the list, it is in `nums[lo..hi]`.
- If `nums[mid] < target`, everything in `lo..mid` is too small, so `lo = mid + 1`.
- If `nums[mid] > target`, everything in `mid..hi` is too big, so `hi = mid - 1`.
- Both moves exclude `mid`, so the interval strictly shrinks. When `lo > hi` it is empty and the target is absent.
- Midpoint: `lo + (hi - lo) // 2` and `(lo + hi) // 2` give the same value in Python because ints do not overflow. In C++ or Java `lo + hi` can overflow a 32-bit int, so the first form is the habit to keep.

**Complexity:** Time O(log n): the interval halves each iteration, so at most about log2(n) + 1 iterations (about 17 for 10^5). Space O(1).

**Dry run:** `[-1,0,3,5,9,12]`, target 9.
| lo | hi | mid | nums[mid] | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 3 | 3 < 9, lo = 3 |
| 3 | 5 | 4 | 9 | found, return 4 |

For target 2: mid=2 (3 > 2) so hi=1; mid=0 (-1 < 2) so lo=1; mid=1 (0 < 2) so lo=2; now lo > hi, return -1.

**Code:**
```python
import random

def brute(nums, target):
    for i, v in enumerate(nums):
        if v == target:
            return i
    return -1

def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1          # invariant: target, if present, is in nums[lo..hi]
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1               # nums[lo..mid] all < target
        else:
            hi = mid - 1               # nums[mid..hi] all > target
    return -1

random.seed(1)
for _ in range(2000):
    n = random.randint(0, 12)
    nums = sorted(random.sample(range(-20, 20), n))
    for t in range(-22, 22):
        assert binary_search(nums, t) == brute(nums, t)
    lo, hi = random.randint(0, 10**18), random.randint(10**18, 2*10**18)
    assert lo + (hi - lo) // 2 == (lo + hi) // 2
print("cross-check ok: 2000 random lists x 44 targets")

assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
assert binary_search([5], 5) == 0
assert binary_search([5], 4) == -1
assert binary_search([], 1) == -1
big = list(range(0, 2 * 10**5, 2))
assert binary_search(big, 199998) == 99999 and binary_search(big, 199999) == -1
print(binary_search([-1, 0, 3, 5, 9, 12], 9), binary_search([-1, 0, 3, 5, 9, 12], 2),
      binary_search([5], 5), binary_search([5], 4))
```

**Output (my run):**
```
cross-check ok: 2000 random lists x 44 targets
4 -1 0 -1
```

**Edge cases:**
- Empty list: hi = -1, loop never runs, return -1.
- One element, hit or miss.
- Target smaller than all or larger than all.
- Even and odd lengths.

**Follow-ups:**
- Duplicates? Then "any index" is returned; use a lower bound for the first (Q4).
- Recursive version? Same logic, depth O(log n), no recursion-limit risk.
- Why not `lo < hi`? That needs a different update rule (`hi = mid`) and a final check; mixing the two templates is the classic bug.

**Common mistakes:**
- `lo = mid` or `hi = mid` with `lo <= hi`: infinite loop.
- Using `<` in the loop condition with `hi = n - 1` and missing the last element.
- Saying overflow matters in Python (it does not; say why the habit is still good).

### Q2 ⭐⭐⭐ 🟢 Search insert position. `nums` is sorted ascending with distinct integers (0 <= len <= 10^4); return the index of `target` if present, otherwise the index where it would have to be inserted to keep the list sorted. Use the half-open interval `lo, hi = 0, n` with `while lo < hi`, and explain why this is exactly the first index whose value is >= target (the lower bound) and why the answer can equal n. Example: [1,3,5,6], 5 -> 2; [1,3,5,6], 2 -> 1; [1,3,5,6], 7 -> 4; [1,3,5,6], 0 -> 0; [], 3 -> 0.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Lower bound on a half-open interval: find the first index whose value is >= target.

**Say this first (1 line):** "That is the lower bound: first index with nums[i] >= target, searched on [0, n) so n is a legal answer."

**Brute force:** Scan for the first value >= target, else n. O(n).

**Optimal:**
- `lo, hi = 0, n`. Invariant: everything before `lo` is < target, everything from `hi` onward is >= target.
- If `nums[mid] < target`, `lo = mid + 1`. Otherwise `hi = mid`: mid may itself be the answer, so keep it.
- Loop ends at `lo == hi`, and that index is the first value >= target.
- Why it handles "insert": if target is present, the first >= is its index; if not, it is the first bigger element, the exact slot that keeps order.
- The answer can be `n` because hi starts at n (target bigger than all elements). Starting hi at n - 1 would be a bug.

**Complexity:** Time O(log n), since the range [lo, hi) halves each step. Space O(1).

**Dry run:** `[1,3,5,6]`, target 2. lo=0, hi=4. mid=2: 5 >= 2, hi=2. mid=1: 3 >= 2, hi=1. mid=0: 1 < 2, lo=1. lo == hi == 1, return 1.

**Code:**
```python
import random
from bisect import bisect_left

def brute(nums, target):
    for i, v in enumerate(nums):
        if v >= target:
            return i
    return len(nums)

def search_insert(nums, target):
    lo, hi = 0, len(nums)              # answer in [0, n]; invariant: nums[:lo] < target <= nums[hi:]
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid                   # mid might be the answer, keep it
    return lo

random.seed(2)
for _ in range(2000):
    nums = sorted(random.sample(range(-15, 15), random.randint(0, 10)))
    for t in range(-17, 17):
        r = search_insert(nums, t)
        assert r == brute(nums, t) == bisect_left(nums, t)
print("cross-check ok")
for a, t, e in [([1,3,5,6],5,2),([1,3,5,6],2,1),([1,3,5,6],7,4),([1,3,5,6],0,0),([],3,0)]:
    assert search_insert(a, t) == e
    print(a, t, "->", search_insert(a, t))
```

**Output (my run):**
```
cross-check ok
[1, 3, 5, 6] 5 -> 2
[1, 3, 5, 6] 2 -> 1
[1, 3, 5, 6] 7 -> 4
[1, 3, 5, 6] 0 -> 0
[] 3 -> 0
```

**Edge cases:**
- Empty list returns 0.
- Target above everything returns n.
- Target below everything returns 0.
- With distinct values, "present" and "insert" cases give the same formula.

**Follow-ups:**
- With duplicates? This returns the leftmost slot, same as `bisect_left`.
- Rightmost slot? Use `nums[mid] <= target` to move right: `bisect_right`.
- Why `hi = mid` not `mid - 1`? mid could be the answer.

**Common mistakes:**
- `hi = n - 1` so the answer n is unreachable.
- `hi = mid - 1` with `lo < hi`: skips the answer.
- Returning -1 for a miss.

### Q3 ⭐⭐⭐ 🟢 Integer square root. Given an integer x with 0 <= x <= 2^31 - 1, return floor(sqrt(x)) without `math.sqrt`, `** 0.5` or `math.isqrt`. Binary search on the value r in [0, x] for the largest r with r * r <= x (say why a 'last True' search needs the upper-biased mid or a closed template, and why you can also cap hi at 46341). Mention that `math.isqrt` is the exact library answer and why float sqrt is risky for very large integers. Example: 4 -> 2; 8 -> 2; 0 -> 0; 1 -> 1; 2147395599 -> 46339; 2147395600 -> 46340.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Binary search on the answer. The predicate `r * r <= x` is True for small r and False for large r, so we want the last True.

**Say this first (1 line):** "Search r in [0, x] for the largest r with r*r <= x, using an upper-biased mid so a 'last True' search cannot loop."

**Brute force:** Try r = 0, 1, 2, ... until (r+1)^2 > x. O(sqrt(x)), about 46340 steps for the max input. Fine here, but not for big numbers.

**Optimal:**
- Predicate P(r) = r*r <= x. It is monotone: True up to floor(sqrt(x)), False after.
- Last-True search: if `mid*mid <= x`, `lo = mid` (mid is still a candidate); else `hi = mid - 1`.
- Because `lo = mid` does not move past mid, the mid must round up: `mid = (lo + hi + 1) // 2`. With a floor mid and `lo = hi - 1`, mid equals lo, `lo = mid` changes nothing, infinite loop.
- Capping hi: 46340^2 = 2147395600 <= 2^31 - 1 < 46341^2, so hi = 46340 is enough for the stated range (46341 also safe). Using hi = x is also correct, just a few more steps.
- `math.isqrt` is the exact library answer (O(log) integer arithmetic). `x ** 0.5` goes through a 53-bit float, so for big ints it can round up to a wrong integer (see the last output line).

**Complexity:** Time O(log x) (about 16 iterations with the cap, 31 without); space O(1). Products stay small, and Python ints never overflow anyway.

**Dry run:** x = 8, lo=0, hi=8. mid=4: 16 > 8, hi=3. mid=2: 4 <= 8, lo=2. mid=3: 9 > 8, hi=2. lo == hi, return 2.

**Code:**
```python
import math, random

def brute(x):
    r = 0
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r

def isqrt_bs(x):
    lo, hi = 0, min(x, 46340)          # 46340^2 = 2147395600 <= 2^31-1 < 46341^2; hi = x also works
    while lo < hi:                     # last True: invariant r*r <= x holds at lo
        mid = (lo + hi + 1) // 2       # upper-biased, else lo = mid loops forever
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo

def isqrt_plain(x):                    # same search without the cap, hi = x
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x: lo = mid
        else: hi = mid - 1
    return lo

for x in range(0, 5000):
    assert isqrt_bs(x) == brute(x) == math.isqrt(x) == isqrt_plain(x)
random.seed(3)
for _ in range(3000):
    x = random.randint(0, 2**31 - 1)
    assert isqrt_bs(x) == math.isqrt(x) == isqrt_plain(x)
for r in (1, 2, 46339, 46340):
    assert isqrt_bs(r*r) == r and isqrt_bs(r*r - 1) == r - 1
assert 46340**2 <= 2**31 - 1 < 46341**2
assert isqrt_bs(2**31 - 1) == 46340
print("cross-check ok")
for x in (4, 8, 0, 1, 2147395599, 2147395600):
    print(x, "->", isqrt_bs(x))
# float risk for huge ints
n = 10**60 - 1
print("float sqrt of 10**60-1:", int(n ** 0.5), "| exact isqrt:", math.isqrt(n))
```

**Output (my run):**
```
cross-check ok
4 -> 2
8 -> 2
0 -> 0
1 -> 1
2147395599 -> 46339
2147395600 -> 46340
float sqrt of 10**60-1: 1000000000000000019884624838656 | exact isqrt: 999999999999999999999999999999
```

**Edge cases:**
- x = 0 and x = 1 (hi = 0 or 1, loop skipped or one step).
- Perfect squares and the numbers just below them.
- Max input 2^31 - 1 gives 46340.

**Follow-ups:**
- Newton's method? r = (r + x // r) // 2 from a start above the root converges quadratically; binary search is simpler to get right.
- Return the ceiling? Compute floor, add 1 unless it is a perfect square.
- Integer k-th root? Same search with `mid ** k <= x`.

**Common mistakes:**
- Floor mid with `lo = mid`: infinite loop.
- Returning hi or lo - 1 inconsistently after a first-True template.
- Using float sqrt for large inputs.

### Q4 ⭐⭐⭐ 🟡 First and last position of an element. `nums` is sorted non-decreasing and may hold duplicates (0 <= len <= 10^5); return [first, last] indices of `target`, or [-1, -1] if absent, in O(log n). Implement one lower-bound routine (first index with value >= x) and use it twice, and explain why a single binary search followed by walking outward is O(n) in the worst case (all equal values). Example: [5,7,7,8,8,10], 8 -> [3, 4]; [5,7,7,8,8,10], 6 -> [-1, -1]; [], 0 -> [-1, -1]; [1], 1 -> [0, 0]; [2,2,2,2], 2 -> [0, 3].
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Lower bound, used twice (first index >= t, and first index >= t + 1).

**Say this first (1 line):** "One lower-bound routine; first = lower_bound(t), last = lower_bound(t + 1) - 1; both are O(log n)."

**Brute force:** Scan once and record first and last match. O(n). The "binary search then walk outward" variant is also O(n): with all values equal, the walk covers the whole array.

**Optimal:**
- `lower_bound(x)` returns the first index with value >= x (n if none).
- `first = lower_bound(t)`. If `first == n` or `nums[first] != t`, target is absent.
- Values are integers, so "first index > t" is `lower_bound(t + 1)`; the last occurrence is that minus 1. (For non-integers, write an upper-bound routine with `<=` instead.)

**Complexity:** Two binary searches: O(log n) time, O(1) space.

**Dry run:** `[5,7,7,8,8,10]`, t = 8. lower_bound(8): lo=0, hi=6, mid=3: 8 >= 8, hi=3; mid=1: 7 < 8, lo=2; mid=2: 7 < 8, lo=3; result 3. lower_bound(9): finds 5 (value 10). last = 5 - 1 = 4. Answer [3, 4].

**Code:**
```python
import random
from bisect import bisect_left, bisect_right

def brute(nums, t):
    idx = [i for i, v in enumerate(nums) if v == t]
    return [idx[0], idx[-1]] if idx else [-1, -1]

def lower_bound(nums, x):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x: lo = mid + 1
        else: hi = mid
    return lo

def search_range(nums, t):
    first = lower_bound(nums, t)
    if first == len(nums) or nums[first] != t:
        return [-1, -1]
    last = lower_bound(nums, t + 1) - 1    # integers: first index >= t+1 minus one
    return [first, last]

random.seed(4)
for _ in range(3000):
    nums = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 14)))
    for t in range(-8, 9):
        r = search_range(nums, t)
        assert r == brute(nums, t)
        if r != [-1, -1]:
            assert r == [bisect_left(nums, t), bisect_right(nums, t) - 1]
print("cross-check ok")
for a, t in [([5,7,7,8,8,10],8),([5,7,7,8,8,10],6),([],0),([1],1),([2,2,2,2],2)]:
    print(a, t, "->", search_range(a, t))
assert search_range([2]*10**5, 2) == [0, 10**5 - 1]
```

**Output (my run):**
```
cross-check ok
[5, 7, 7, 8, 8, 10] 8 -> [3, 4]
[5, 7, 7, 8, 8, 10] 6 -> [-1, -1]
[] 0 -> [-1, -1]
[1] 1 -> [0, 0]
[2, 2, 2, 2] 2 -> [0, 3]
```

**Edge cases:**
- Empty list.
- Target absent but inside the range (6 in the example) or beyond it.
- All equal values: answer is [0, n - 1].
- Single occurrence.

**Follow-ups:**
- Count occurrences? last - first + 1, or `bisect_right - bisect_left`.
- Library version? `bisect_left(nums, t)` and `bisect_right(nums, t) - 1`.
- Floats or strings? Use a second routine with `<=` rather than `t + 1`.

**Common mistakes:**
- Forgetting the `first == n` check (IndexError).
- Walking outward after one search.
- Using `t + 1` on non-integer data.

### Q5 ⭐⭐⭐ 🟡 Search in a rotated sorted array (distinct values). A list that was sorted ascending with distinct integers was rotated at an unknown pivot (1 <= len <= 5000; rotation by 0 is allowed). Return the index of `target` or -1 in O(log n). At each step one half [lo, mid] or [mid, hi] is sorted; decide which, then check whether target lies in that sorted half. Explain why the comparison `nums[lo] <= nums[mid]` needs `<=` (two-element windows). Example: [4,5,6,7,0,1,2], 0 -> 4; [4,5,6,7,0,1,2], 3 -> -1; [1], 0 -> -1; [3,1], 1 -> 1; [1,3], 3 -> 1.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported Indian product-company online rounds (a Naukri Code360 Flipkart 2021 entry naming Allocate Books and a Flipkart entry naming rotated sorted array search; one aggregator, 2015-2022 reports, snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Modified binary search on a rotated sorted array: one half is always sorted.

**Say this first (1 line):** "At each mid, one side is sorted; I check whether the target falls in that sorted side and discard the other."

**Brute force:** Linear scan, O(n). Or find the pivot first and then run a normal binary search on the right part (two passes, still O(log n)).

**Optimal:**
- After `nums[mid] == t` check, ask: is `[lo..mid]` sorted? That is `nums[lo] <= nums[mid]`.
- If yes and `nums[lo] <= t < nums[mid]`, go left (`hi = mid - 1`), else go right.
- If no, `[mid..hi]` is sorted. If `nums[mid] < t <= nums[hi]`, go right, else go left.
- Why `<=`: in a two-element window `mid == lo`, so `nums[lo] == nums[mid]` and the left "half" is one sorted element. With `<` that case falls into the right-half branch and misjudges it: `[3,1]`, target 1 returns -1 (wrong; I checked by hand: 3 < 1 is False so the right-half test `3 < 1` fails and hi moves to -1). With `<=` it goes left-sorted, 1 is not in [3,3), so lo = 1 and the next step finds it.
- Distinct values mean the sorted-half test is never ambiguous.

**Complexity:** O(log n) time (the window halves each step), O(1) space.

**Dry run:** `[4,5,6,7,0,1,2]`, t=0. lo=0, hi=6, mid=3 (7). Left sorted (4 <= 7), but 0 is not in [4,7), lo=4. mid=5 (1): left [0..1] sorted, 0 in [0,1), hi=4. mid=4 (0): found, index 4.

**Code:**
```python
import random

def brute(nums, t):
    return nums.index(t) if t in nums else -1

def search_rotated(nums, t):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == t:
            return mid
        if nums[lo] <= nums[mid]:              # left half [lo..mid] sorted (<= for lo == mid)
            if nums[lo] <= t < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                  # right half [mid..hi] sorted
            if nums[mid] < t <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

random.seed(5)
cnt = 0
for n in range(1, 13):
    for _ in range(150):
        base = sorted(random.sample(range(-20, 40), n))
        k = random.randrange(n)
        nums = base[k:] + base[:k]
        for t in range(-22, 42):
            assert search_rotated(nums, t) == brute(nums, t)
            cnt += 1
print("cross-check ok:", cnt, "queries")
for a, t in [([4,5,6,7,0,1,2],0),([4,5,6,7,0,1,2],3),([1],0),([3,1],1),([1,3],3)]:
    print(a, t, "->", search_rotated(a, t))
```

**Output (my run):**
```
cross-check ok: 115200 queries
[4, 5, 6, 7, 0, 1, 2] 0 -> 4
[4, 5, 6, 7, 0, 1, 2] 3 -> -1
[1] 0 -> -1
[3, 1] 1 -> 1
[1, 3] 3 -> 1
```

**Edge cases:**
- Rotation by 0 (plain sorted).
- Single element; two elements.
- Target absent, below the min, above the max.
- Target at the pivot or at either end.

**Follow-ups:**
- Duplicates allowed? When `nums[lo] == nums[mid] == nums[hi]` you cannot tell which side is sorted; shrink both ends by one. Worst case O(n).
- Find the rotation count? It is the index of the minimum (Q6).
- Do it in one pass vs two? Both O(log n); one pass is shorter to write.

**Common mistakes:**
- `<` instead of `<=` in the sorted-half test.
- Wrong strictness in the range test (`t < nums[mid]` is right because mid was already checked).
- Assuming rotation is never 0.

### Q6 ⭐⭐⭐ 🟡 Find the minimum in a rotated sorted array (distinct values). Same setting as a sorted ascending list of distinct integers rotated at an unknown pivot (1 <= len <= 5000, rotation by 0 allowed). Return the smallest value in O(log n) using `while lo < hi` and comparing `nums[mid]` with `nums[hi]`. Explain why comparing with `nums[hi]` works but comparing with `nums[lo]` is ambiguous, and why `hi = mid` (not `mid - 1`) is required. Example: [3,4,5,1,2] -> 1; [4,5,6,7,0,1,2] -> 0; [11,13,15,17] -> 11; [2,1] -> 1; [7] -> 7.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search for a boundary (first element of the rotated part), comparing with the right end.

**Say this first (1 line):** "Compare nums[mid] to nums[hi]: bigger means the minimum is right of mid, otherwise mid might be the minimum so hi = mid."

**Brute force:** `min(nums)`, O(n).

**Optimal:**
- Use `lo < hi`. Distinct values, so `nums[mid] != nums[hi]` whenever `mid < hi` (mid is always < hi here).
- `nums[mid] > nums[hi]`: the drop (the minimum) is strictly right of mid, `lo = mid + 1`.
- `nums[mid] < nums[hi]`: mid to hi is increasing, so the minimum is at mid or left of it, `hi = mid`. Not `mid - 1`, because mid itself may be the minimum.
- Why not compare with `nums[lo]`: `nums[mid] >= nums[lo]` is True both for an unrotated list like `[1,2,3]` (minimum at the left) and for `[2,3,1]` (minimum at the right), so it does not tell you which way to go. The right end is clean: `nums[mid] > nums[hi]` can only happen when mid is in the high left part, so the drop is to its right.

**Complexity:** O(log n) time, O(1) space.

**Dry run:** `[3,4,5,1,2]`. lo=0, hi=4, mid=2 (5 > 2): lo=3. mid=3 (1 < 2): hi=3. lo == hi, return nums[3] = 1.

**Code:**
```python
import random

def brute(nums):
    return min(nums)

def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:       # min is strictly right of mid
            lo = mid + 1
        else:                          # nums[mid] < nums[hi] (distinct): mid may be the min
            hi = mid
    return nums[lo]

random.seed(6)
for n in range(1, 15):
    for _ in range(200):
        base = sorted(random.sample(range(-30, 30), n))
        k = random.randrange(n)
        nums = base[k:] + base[:k]
        assert find_min(nums) == brute(nums)
print("cross-check ok")
for a in ([3,4,5,1,2],[4,5,6,7,0,1,2],[11,13,15,17],[2,1],[7]):
    print(a, "->", find_min(a))
# nums[lo]-comparison counterexample: both [1,2,3] (rotation 0) and [2,3,1] have nums[mid] >= nums[lo]
print("[1,2,3] mid>=lo:", [1,2,3][1] >= [1,2,3][0], "| [2,3,1] mid>=lo:", [2,3,1][1] >= [2,3,1][0])
```

**Output (my run):**
```
cross-check ok
[3, 4, 5, 1, 2] -> 1
[4, 5, 6, 7, 0, 1, 2] -> 0
[11, 13, 15, 17] -> 11
[2, 1] -> 1
[7] -> 7
[1,2,3] mid>=lo: True | [2,3,1] mid>=lo: True
```

**Edge cases:**
- Not rotated: `nums[mid] < nums[hi]` always, hi shrinks to 0.
- Single element.
- Two elements, either order.

**Follow-ups:**
- Duplicates? If `nums[mid] == nums[hi]`, do `hi -= 1`; worst case O(n) (e.g. `[1,1,1,1]`), because you cannot tell which side holds the minimum.
- Return the rotation count? Return `lo`.
- Search afterwards? Q5.

**Common mistakes:**
- `hi = mid - 1`, which can skip the minimum.
- Comparing with `nums[lo]` and special-casing the unrotated list.
- Using `lo <= hi` with `hi = mid`: infinite loop.

### Q7 ⭐⭐⭐ 🟡 Koko eating bananas. `piles[i]` is the size of pile i (1 <= len <= 10^4, 1 <= piles[i] <= 10^9). Koko eats at a fixed integer speed k bananas per hour; in each hour she picks one pile and eats up to k from it (if the pile has fewer, she finishes it and wastes the rest of that hour). She must finish all piles within `h` hours, where len(piles) <= h <= 10^9. Return the minimum integer k. Binary search on k in [1, max(piles)] with a predicate 'hours needed at speed k <= h' that uses ceiling division; argue the predicate is monotone in k. Example: piles=[3,6,7,11], h=8 -> 4; piles=[30,11,23,4,20], h=5 -> 30; piles=[30,11,23,4,20], h=6 -> 23; piles=[5], h=5 -> 1.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports)

**Pattern:** Binary search on the answer: minimise k such that feasible(k) is True.

**Say this first (1 line):** "Speed k works if sum of ceil(pile / k) <= h. Larger k never needs more hours, so the predicate flips once and I search k in [1, max(piles)]."

**Brute force:** Try k = 1, 2, 3, ... and return the first feasible one. Up to max(piles) = 10^9 values times n piles each. Far too slow.

**Optimal:**
- hours(k) = sum of ceil(p / k). Ceil division: `(p + k - 1) // k`.
- Monotone: for k' > k, ceil(p / k') <= ceil(p / k) for every pile, so hours does not increase. So feasible(k) is False...False True...True.
- Bounds: lo = 1 (speed 0 is meaningless). hi = max(piles) is always feasible: each pile takes one hour, total n <= h. No speed beyond max helps.
- First-True search with `hi = mid` on success, `lo = mid + 1` on failure.

**Complexity:** log2(max) <= 30 iterations, each O(n): O(n log M), M = max(piles). Space O(1).

**Dry run:** piles [3,6,7,11], h=8. lo=1, hi=11. mid=6: 1+1+2+2 = 6 <= 8, hi=6. mid=3: 1+2+3+4 = 10 > 8, lo=4. mid=5: 1+2+2+3 = 8 <= 8, hi=5. mid=4: 1+2+2+3 = 8 <= 8, hi=4. Answer 4.

**Code:**
```python
import random
from math import ceil

def brute(piles, h):
    k = 1
    while sum(ceil(p / k) for p in piles) > h:
        k += 1
    return k

def min_speed(piles, h):
    lo, hi = 1, max(piles)             # at k = max, hours = len(piles) <= h, so hi is feasible
    while lo < hi:
        mid = (lo + hi) // 2
        if sum((p + mid - 1) // mid for p in piles) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo

random.seed(7)
for _ in range(3000):
    n = random.randint(1, 6)
    piles = [random.randint(1, 30) for _ in range(n)]
    h = random.randint(n, 40)
    assert min_speed(piles, h) == brute(piles, h)
print("cross-check ok")
for p, h in [([3,6,7,11],8),([30,11,23,4,20],5),([30,11,23,4,20],6),([5],5)]:
    print(p, h, "->", min_speed(p, h))
big = [10**9] * 10**4
assert min_speed(big, 10**4) == 10**9
assert min_speed(big, 10**9) == 10**4 * 10**9 // 10**9   # 10^4 piles, 10^9 hours -> k=10^4
print("big:", min_speed(big, 10**9))
```

**Output (my run):**
```
cross-check ok
[3, 6, 7, 11] 8 -> 4
[30, 11, 23, 4, 20] 5 -> 30
[30, 11, 23, 4, 20] 6 -> 23
[5] 5 -> 1
big: 10000
```

**Edge cases:**
- h == n: answer is max(piles).
- One pile: ceil(p / h).
- Huge piles (10^9 each): ints are fine in Python; in C++ the hour sum needs 64-bit.
- Speed larger than a pile wastes the rest of the hour; the ceiling models that.

**Follow-ups:**
- Tighter lo? `ceil(sum / h)` is a valid lower bound.
- Why monotone matters? Without it the halving step discards valid answers.
- Same template elsewhere? Capacity (Q8), split array, allocate books.

**Common mistakes:**
- Floor division instead of ceiling.
- lo = 0 (division by zero).
- Returning `hi + 1` or off-by-one from mixing templates.

### Q8 ⭐⭐⭐ 🟡 Capacity to ship packages within D days. `weights` are package weights in a fixed order (1 <= len <= 5*10^4, 1 <= weights[i] <= 500); each day the ship loads consecutive packages in that order, never exceeding capacity c. Return the least c such that all packages ship within `days` days (1 <= days <= len). Binary search c between max(weights) and sum(weights); explain why the lower bound is max(weights) (a single package must fit) and why the greedy day count is non-increasing as c grows (the greedy loading itself is Part 8's topic; here it is only the predicate). Example: weights=[1,2,3,4,5,6,7,8,9,10], days=5 -> 15; [3,2,2,4,1,4], days=3 -> 6; [1,2,3,1,1], days=4 -> 3; [7], days=1 -> 7.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports)

**Pattern:** Binary search on the answer (minimise the maximum): least capacity c with days_needed(c) <= days.

**Say this first (1 line):** "Capacity c is feasible if greedily loading in order takes at most D days; a bigger ship never needs more days, so I binary search c in [max(w), sum(w)]."

**Brute force:** Try c = max(w), max(w)+1, ... until feasible. Up to sum(w) - max(w) tries, each O(n). Or enumerate all ways to cut the list into D groups, exponential.

**Optimal:**
- Predicate: walk the list, start a new day when the next package would exceed c. Count days. (Why greedy is optimal is Part 8's topic; here it is only the predicate.)
- Monotone: any loading that fits in c also fits in c + 1, so days_needed is non-increasing in c.
- lo = max(w): a package cannot be split, so smaller c is impossible. hi = sum(w): one day suffices.
- First-True search.

**Complexity:** O(n log(sum(w))): log2(2.5 * 10^7) is about 25 iterations, each O(n) over at most 5 * 10^4 items. Space O(1).

**Dry run:** `[3,2,2,4,1,4]`, days=3. lo=4, hi=16. mid=10: days (3+2+2=7, 7+4 > 10 so day 2: 4+1+4=9) = 2 <= 3, hi=10. mid=7: day1 7, day2 4+1=5 (+4 = 9 > 7), day3 4: 3 days, hi=7. mid=5: 3+2 | 2 | 4+1 | 4 = 4 days > 3, lo=6. mid=6: 3+2 | 2+4 | 1+4 = 3 days, hi=6. Answer 6.

**Code:**
```python
import random

def days_needed(w, c):
    d, cur = 1, 0
    for x in w:
        if cur + x > c:
            d += 1; cur = 0
        cur += x
    return d

def brute(w, days):
    c = max(w)
    while days_needed(w, c) > days:
        c += 1
    return c

def ship(w, days):
    lo, hi = max(w), sum(w)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(w, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo

# exhaustive partition check: true optimum over all ways to cut into <= days contiguous groups
from itertools import combinations
def exact(w, days):
    n = len(w); best = None
    for k in range(0, days):
        for cuts in combinations(range(1, n), k):
            b = (0,) + cuts + (n,)
            m = max(sum(w[b[i]:b[i+1]]) for i in range(len(b) - 1))
            best = m if best is None else min(best, m)
    return best

random.seed(8)
for _ in range(2000):
    n = random.randint(1, 8)
    w = [random.randint(1, 12) for _ in range(n)]
    d = random.randint(1, n)
    assert ship(w, d) == brute(w, d) == exact(w, d)
print("cross-check ok (vs linear scan and exhaustive partitions)")
for w, d in [(list(range(1, 11)), 5), ([3,2,2,4,1,4], 3), ([1,2,3,1,1], 4), ([7], 1)]:
    print(w, d, "->", ship(w, d))
w = [500] * 5 * 10**4
assert ship(w, 1) == 500 * 5 * 10**4 and ship(w, len(w)) == 500
```

**Output (my run):**
```
cross-check ok (vs linear scan and exhaustive partitions)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 5 -> 15
[3, 2, 2, 4, 1, 4] 3 -> 6
[1, 2, 3, 1, 1] 4 -> 3
[7] 1 -> 7
```

**Edge cases:**
- days = 1: answer is sum(w).
- days = n: answer is max(w).
- One package.
- All equal weights.

**Follow-ups:**
- Split array largest sum / allocate books / painter's partition? Same code, different story.
- Why not DP? DP is O(n^2 * days); the search is much faster.
- Reduce the search range? Tighter lo: max(max(w), ceil(sum / days)).

**Common mistakes:**
- lo = 1 or 0 (the predicate then accepts impossible capacities, or loops on a package that never fits).
- Resetting `cur` to 0 and forgetting to add the current package to the new day.
- Reordering packages (order is fixed).

### Q9 ⭐⭐⭐ 🟡 Find a peak element. `nums` is a list of integers (1 <= len <= 1000) in which adjacent elements are never equal; imagine nums[-1] and nums[n] as negative infinity. A peak is an index whose value is strictly greater than both neighbours. Return the index of ANY peak in O(log n) (the answer is not unique: a list can have several peaks and any valid one is accepted). Compare nums[mid] with nums[mid + 1] and move toward the larger side; explain why a peak is guaranteed to stay inside the kept half. Example: [1,2,3,1] -> 2; [1,2,1,3,5,6,4] -> 1 or 5 (either is correct); [1] -> 0; [2,1] -> 0; [1,2] -> 1.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Binary search on a property, not on a sorted order: follow the uphill side.

**Say this first (1 line):** "Compare nums[mid] with nums[mid+1] and keep the side that goes up; a peak must exist there."

**Brute force:** Scan for any index bigger than its neighbours. O(n).

**Optimal:**
- Neighbours are never equal, and the ends count as -infinity.
- If `nums[mid] < nums[mid + 1]` the slope goes up to the right: `lo = mid + 1`. Climbing right either reaches a local maximum or reaches the end, which is a peak because of the -infinity wall.
- Otherwise (`nums[mid] > nums[mid + 1]`) the slope goes down: a peak is at mid or to its left, `hi = mid`.
- Invariant: nums[lo..hi] contains a peak of the whole array. `mid + 1` is always valid because `mid < hi`.
- The answer is not unique. I verified that `[1,2,1,3,5,6,4]` has exactly two peaks, at indices 1 and 5; my run returns 5 and returning 1 would also be accepted. A checker must test "is a peak", not "equals the brute-force index" (the cross-check does exactly that).

**Complexity:** O(log n) time, O(1) space.

**Dry run:** `[1,2,1,3,5,6,4]`. lo=0, hi=6, mid=3: 3 < 5, lo=4. mid=5: 6 > 4, hi=5. mid=4: 5 < 6, lo=5. Return 5.

**Code:**
```python
import random

def peaks(nums):
    n = len(nums)
    return [i for i in range(n)
            if (i == 0 or nums[i] > nums[i-1]) and (i == n-1 or nums[i] > nums[i+1])]

def brute(nums):
    return peaks(nums)[0]

def find_peak(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:   # uphill: a peak exists in mid+1..hi
            lo = mid + 1
        else:                           # downhill (never equal): a peak exists in lo..mid
            hi = mid
    return lo

random.seed(9)
for _ in range(5000):
    n = random.randint(1, 12)
    nums = [random.randint(-5, 5)]
    while len(nums) < n:
        v = random.randint(-5, 5)
        if v != nums[-1]:
            nums.append(v)
    assert find_peak(nums) in peaks(nums)       # any valid peak accepted; not equal to brute()'s index
print("cross-check ok: result always a valid peak")
for a in ([1,2,3,1],[1,2,1,3,5,6,4],[1],[2,1],[1,2]):
    print(a, "-> idx", find_peak(a), "all peaks", peaks(a))
assert peaks([1,2,1,3,5,6,4]) == [1, 5]
assert find_peak([1,2,1,3,5,6,4]) in (1, 5)
```

**Output (my run):**
```
cross-check ok: result always a valid peak
[1, 2, 3, 1] -> idx 2 all peaks [2]
[1, 2, 1, 3, 5, 6, 4] -> idx 5 all peaks [1, 5]
[1] -> idx 0 all peaks [0]
[2, 1] -> idx 0 all peaks [0]
[1, 2] -> idx 1 all peaks [1]
```

**Edge cases:**
- One element: index 0.
- Two elements.
- Strictly increasing (answer n - 1) or decreasing (answer 0).
- Many peaks (any is fine).

**Follow-ups:**
- Equal neighbours allowed? Then the guarantee breaks (a flat plateau hides the slope); worst case is linear.
- Global maximum instead? Needs O(n) in general.
- 2D peak? A harder variant, binary search on rows.

**Common mistakes:**
- Comparing with `mid - 1` and indexing out of range at 0.
- Using `lo <= hi` with `hi = mid`.
- Asserting the result equals a fixed index in tests.

### Q10 ⭐⭐⭐ 🟡 Search a 2D matrix with sorted rows (flattening variant). `matrix` has m rows and n columns (1 <= m, n <= 100); every row is sorted ascending and the first element of each row is greater than the last element of the previous row. Return True if `target` is present, in O(log(m*n)). Treat the matrix as one sorted list of length m*n and map index i to (i // n, i % n); also state the two-step alternative (binary search the row, then the column) and why both are O(log m + log n). Example: [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=3 -> True; the same matrix with target=13 -> False; [[1]], 1 -> True; [[1],[3]], 3 -> True.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search on a virtual flattened array (index math).

**Say this first (1 line):** "The rows chain into one sorted list of m*n items, so I binary search i in [0, m*n - 1] and read matrix[i // n][i % n]."

**Brute force:** Check every cell, O(m*n). Or binary search each row, O(m log n).

**Optimal:**
- Because each row starts above the previous row's last value, the row-major order is globally sorted.
- Standard closed-interval search on i, with `v = m[mid // n][mid % n]`. No copy is made.
- Two-step alternative: binary search over rows on first elements for the last row whose first value <= target, then binary search inside that row. That is O(log m + log n), and log m + log n = log(mn), so the two are the same order.

**Complexity:** O(log(m*n)) time, O(1) space.

**Dry run:** matrix 3x4, target 3. lo=0, hi=11, mid=5 -> row 1, col 1 = 11 > 3, hi=4. mid=2 -> row 0, col 2 = 5 > 3, hi=1. mid=0: 1 < 3, lo=1. mid=1: 3, found, True.

**Code:**
```python
import random

def brute(m, t):
    return any(t in row for row in m)

def search_matrix(m, t):
    R, C = len(m), len(m[0])
    lo, hi = 0, R * C - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = m[mid // C][mid % C]
        if v == t: return True
        if v < t: lo = mid + 1
        else: hi = mid - 1
    return False

def two_step(m, t):
    lo, hi = 0, len(m) - 1               # last row whose first element <= t
    row = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if m[mid][0] <= t: row, lo = mid, mid + 1
        else: hi = mid - 1
    if row < 0: return False
    r = m[row]; lo, hi = 0, len(r) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if r[mid] == t: return True
        if r[mid] < t: lo = mid + 1
        else: hi = mid - 1
    return False

random.seed(10)
for _ in range(2000):
    R, C = random.randint(1, 5), random.randint(1, 5)
    vals = sorted(random.sample(range(-20, 60), R * C))
    m = [vals[i*C:(i+1)*C] for i in range(R)]
    for t in range(-22, 62):
        assert search_matrix(m, t) == two_step(m, t) == brute(m, t)
print("cross-check ok")
M = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
print(search_matrix(M, 3), search_matrix(M, 13), search_matrix([[1]], 1), search_matrix([[1],[3]], 3))
```

**Output (my run):**
```
cross-check ok
True False True True
```

**Edge cases:**
- 1x1; one column; one row.
- Target below the first or above the last value.
- Target between rows (13 in the example) returns False.

**Follow-ups:**
- Rows sorted, columns sorted, but rows not chained? Staircase walk from the top-right corner in O(m + n), since binary search on the flattened index no longer works.
- Empty matrix? Guard `if not m or not m[0]` (constraints here forbid it).
- Why not `bisect` on a flattened copy? Building the copy is O(mn).

**Common mistakes:**
- Using `m` and `n` the wrong way round (`// m` instead of `// n`).
- Flattening to a list first, which wastes O(mn).
- Applying this to the weaker "rows and columns sorted" matrix.

### Q11 ⭐⭐⭐ 🟡 Lower and upper bound semantics and the bisect module. For a sorted list `a` (non-decreasing, duplicates allowed) write `lower_bound(a, x)` (first index with a[i] >= x) and `upper_bound(a, x)` (first index with a[i] > x) from scratch with `lo, hi = 0, len(a)`, show that they equal `bisect.bisect_left` and `bisect.bisect_right`, and use them for: the count of x, the count of values in [lo_v, hi_v], the largest element <= x (floor) and the smallest element > x (strict successor). Say what each returns when x is below everything or above everything. Example: a=[1,2,2,2,3,5]: lower_bound(2) -> 1, upper_bound(2) -> 4, count of 2 -> 3, count in [2,3] -> 4, floor(4) -> 3, strict successor of 5 -> None, lower_bound(0) -> 0, upper_bound(9) -> 6.
**Asked at:** Python documentation mirrors for bisect (docs.python.org 3.10 and current .rst source: key added in 3.10, key not applied to the search value in bisect_left/bisect_right, insort is O(n) overall; snippets only, direct fetch failed with ENOTFOUND; behaviour re-verified in the sandbox) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports

**Pattern:** Binary search for a boundary. One monotone predicate (`a[i] < x` or `a[i] <= x`) is True then False; the answer is where it flips. Every "count / floor / successor" question is a lower or upper bound plus index arithmetic.

**Say this first (1 line):** "Lower bound is the first index with a[i] >= x, upper bound is the first index with a[i] > x; they are `bisect_left` and `bisect_right`, and count, floor and successor all fall out of them in O(log n)."

**Brute force:** Scan the list and count or compare. O(n) per query. Fine once, too slow for many queries on a big list.

**Optimal:**
- Search the half-open range `[lo, hi) = [0, len(a))`. The answer can be `len(a)`, so `hi` starts at `len(a)`, not `len(a) - 1`.
- Lower bound: if `a[mid] < x`, the answer is right of mid, so `lo = mid + 1`; else `hi = mid`.
- Upper bound: same, but the test is `a[mid] <= x`. That one character is the whole difference.
- Invariant: everything left of `lo` fails the "go right" test; everything from `hi` on passes the "stop" test.
- The loop ends when `lo == hi`, and that index is the boundary.

| Question | Formula |
|---|---|
| count of x | `upper_bound(x) - lower_bound(x)` |
| count in [l, h] | `upper_bound(h) - lower_bound(l)` (clamp at 0 if l > h) |
| floor (largest <= x) | `i = upper_bound(x)`; `a[i-1]` if `i > 0` else None |
| ceiling (smallest >= x) | `i = lower_bound(x)`; `a[i]` if `i < n` else None |
| strict successor (smallest > x) | `i = upper_bound(x)`; `a[i]` if `i < n` else None |

| x is... | lower_bound | upper_bound | floor | successor |
|---|---|---|---|---|
| below everything | 0 | 0 | None | `a[0]` |
| above everything | n | n | `a[-1]` | None |

**Complexity:** Each step halves `hi - lo`, so O(log n) time, O(1) space. `bisect` does the same in C. `insort` is O(log n) to find the spot but O(n) to shift the list, so O(n) overall.

**Dry run:** `a = [1,2,2,2,3,5]`, `lower_bound(2)`
| lo | hi | mid | a[mid] | a[mid] < 2? | next |
|---|---|---|---|---|---|
| 0 | 6 | 3 | 2 | no | hi = 3 |
| 0 | 3 | 1 | 2 | no | hi = 1 |
| 0 | 1 | 0 | 1 | yes | lo = 1 |
Stop at `lo == hi == 1`. For `upper_bound(2)` the test is `<= 2`: mid=3 (2) go right, lo=4; mid=5 (5) hi=5; mid=4 (3) hi=4. Answer 4. Count = 4 - 1 = 3.

**Code:**
```python
import bisect
import random


def lower_bound(a, x):
    """First index i with a[i] >= x (len(a) if none)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(a, x):
    """First index i with a[i] > x (len(a) if none)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_eq(a, x):
    return upper_bound(a, x) - lower_bound(a, x)


def count_range(a, lo_v, hi_v):  # values in [lo_v, hi_v]
    return max(0, upper_bound(a, hi_v) - lower_bound(a, lo_v))


def floor_val(a, x):  # largest element <= x
    i = upper_bound(a, x)
    return a[i - 1] if i > 0 else None  # guard: a[-1] would wrap around


def ceil_val(a, x):  # smallest element >= x
    i = lower_bound(a, x)
    return a[i] if i < len(a) else None


def successor(a, x):  # smallest element > x (strict)
    i = upper_bound(a, x)
    return a[i] if i < len(a) else None


# ---- brute-force references (linear scans) ----
def b_lb(a, x): return sum(1 for v in a if v < x)
def b_ub(a, x): return sum(1 for v in a if v <= x)
def b_floor(a, x): return max((v for v in a if v <= x), default=None)
def b_succ(a, x): return min((v for v in a if v > x), default=None)
def b_cnt(a, l, h): return sum(1 for v in a if l <= v <= h)


a = [1, 2, 2, 2, 3, 5]
print("lower_bound(2) =", lower_bound(a, 2))
print("upper_bound(2) =", upper_bound(a, 2))
print("count of 2     =", count_eq(a, 2))
print("count in [2,3] =", count_range(a, 2, 3))
print("floor(4)       =", floor_val(a, 4))
print("successor(5)   =", successor(a, 5))
print("lower_bound(0) =", lower_bound(a, 0))
print("upper_bound(9) =", upper_bound(a, 9))
print("x below all (0): floor =", floor_val(a, 0), ", successor =", successor(a, 0))
print("x above all (9): floor =", floor_val(a, 9), ", successor =", successor(a, 9))
assert [lower_bound(a, 2), upper_bound(a, 2), count_eq(a, 2), count_range(a, 2, 3),
        floor_val(a, 4), successor(a, 5), lower_bound(a, 0), upper_bound(a, 9)] == [1, 4, 3, 4, 3, None, 0, 6]

random.seed(11)
n_checks = 0
for _ in range(500):
    arr = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 10)))
    for x in range(-7, 8):
        assert lower_bound(arr, x) == bisect.bisect_left(arr, x) == b_lb(arr, x), (arr, x)
        assert upper_bound(arr, x) == bisect.bisect_right(arr, x) == b_ub(arr, x), (arr, x)
        assert count_eq(arr, x) == arr.count(x)
        assert floor_val(arr, x) == b_floor(arr, x)
        assert successor(arr, x) == b_succ(arr, x)
        n_checks += 1
    for l in range(-6, 7):
        for h in range(-6, 7):
            assert count_range(arr, l, h) == b_cnt(arr, l, h), (arr, l, h)
print("cross-check: 500 seeded lists, %d (list, x) pairs agree with bisect and brute force" % n_checks)

# edge cases
assert lower_bound([], 3) == 0 and upper_bound([], 3) == 0
assert floor_val([], 3) is None and successor([], 3) is None
assert count_range([1, 2, 3], 5, 1) == 0          # inverted range must not go negative
assert floor_val([4, 4], 4) == 4 and successor([4, 4], 4) is None
# bisect key (3.10+): key applies to the elements, NOT to x
recs = [(1, "a"), (2, "b"), (2, "c"), (5, "d")]
assert bisect.bisect_left(recs, 2, key=lambda r: r[0]) == 1
assert bisect.bisect_right(recs, 2, key=lambda r: r[0]) == 3
# the classic wrap-around bug: a[upper_bound-1] with index -1 silently returns the LAST element
assert a[upper_bound(a, 0) - 1] == 5   # wrong 'floor(0)' if you forget the guard
print("edge asserts passed")
```

**Output (my run):**
```text
lower_bound(2) = 1
upper_bound(2) = 4
count of 2     = 3
count in [2,3] = 4
floor(4)       = 3
successor(5)   = None
lower_bound(0) = 0
upper_bound(9) = 6
x below all (0): floor = None , successor = 1
x above all (9): floor = 5 , successor = None
cross-check: 500 seeded lists, 7500 (list, x) pairs agree with bisect and brute force
edge asserts passed
```

**Edge cases:**
- Empty list: both bounds are 0, floor and successor are None.
- x below all or above all (table above).
- All elements equal x: lower 0, upper n, count n.
- Inverted range (`l > h`) in `count_range`: clamp with `max(0, ...)`.
- Floor with `i == 0`: `a[i-1]` is `a[-1]`, the last element. No error, silently wrong. Always guard.

**Follow-ups:**
- *What does `key=` do in `bisect`?* Added in Python 3.10. It is applied to the list elements, not to `x`, so pass the bare search value (as in my edge assert on tuples).
- *Is `insort` fast?* The search is O(log n), the insert shifts elements, so O(n) overall. For many inserts use a `SortedList` or a heap, depending on the need.
- *Why not `hi = len(a) - 1`?* Then "x larger than everything" cannot return `len(a)`. The half-open range keeps the boundary representable.

**Common mistakes:**
- Mixing up `<` and `<=` between the two bounds.
- `hi = len(a) - 1` with `while lo < hi`: misses the "after the end" answer.
- Using `a[bisect_right(a, x) - 1]` for floor without checking for 0.
- Treating count in a range as `upper(h) - upper(l)` (that drops values equal to l).

### Q12 ⭐⭐⭐ 🔴 Median of two sorted arrays. `a` and `b` are sorted ascending integer lists with len(a) + len(b) >= 1 (either may be empty; each up to 10^3 long in the examples, 10^6 in the constraints). Return the median of all elements combined (the middle value if the total is odd, the mean of the two middle values if even, as a float) in O(log(min(m, n))). Binary search the cut position in the shorter list so that the left halves of both lists together hold (m + n + 1) // 2 elements, and accept the cut when max(left parts) <= min(right parts); use +/- infinity for missing sides. Give the O(m + n) merge as the reference. Example: [1,3], [2] -> 2.0; [1,2], [3,4] -> 2.5; [], [5] -> 5.0; [0,0], [0,0] -> 0.0; [1,2,3], [] -> 2.0.
**Asked at:** Median-of-two-sorted-arrays pages (techinterview.org 'binary search's nastiest cousin' page saying the O(m+n) merge is the usual first answer and O(log) is the expected follow-up, educative.io grokking page, a jointaro page with a company filter; snippets only, not opened; no company report verified) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search on a partition (cut position), not on a value. Cut both lists so the left parts together hold half the elements; the cut is right when everything on the left is <= everything on the right.

**Say this first (1 line):** "Merge is O(m+n); for O(log(min(m,n))) I binary search how many elements of the shorter list go left, the longer list's cut follows from that, and I accept when max(left) <= min(right)."

**Brute force:** Merge the two sorted lists with two pointers (or concatenate and sort), then read the middle. O(m + n) time and space. This is the reference in the code.

**Optimal:**
- Make `a` the shorter list. Let `half = (m + n + 1) // 2`.
- Pick `i` = number of elements of `a` on the left. Then `j = half - i` elements of `b` are on the left. Because `m <= n`, `j` stays in `[0, n]` for every `i` in `[0, m]`.
- Four border values: `a_left = a[i-1]`, `a_right = a[i]`, `b_left = b[j-1]`, `b_right = b[j]`. Missing side: `-inf` on the left, `+inf` on the right.
- Each list is already sorted, so the cut is valid exactly when `a_left <= b_right` and `b_left <= a_right`.
- If `a_left > b_right`: took too many from `a`, `hi = i - 1`. Else `lo = i + 1`.
- Odd total: answer is `max(a_left, b_left)`. Even total: mean of `max(a_left, b_left)` and `min(a_right, b_right)`.
- `(m + n + 1) // 2` makes the left side the larger one when the total is odd, so the odd median is the left maximum.

**Complexity:** The search range is `[0, m]` with `m = min(m, n)`, halved each step: O(log(min(m, n))) time, O(1) space.

**Dry run:** `a = [1,2]`, `b = [3,4]`, `m = n = 2`, `half = 2`
| lo | hi | i | j | a_left | a_right | b_left | b_right | valid? |
|---|---|---|---|---|---|---|---|---|
| 0 | 2 | 1 | 1 | 1 | 2 | 3 | 4 | `b_left 3 <= a_right 2`? no, lo = 2 |
| 2 | 2 | 2 | 0 | 2 | +inf | -inf | 3 | yes |
Left max = 2, right min = 3, even total, so (2 + 3) / 2 = 2.5.

**Code:**
```python
import random

INF = float("inf")


def median_merge(a, b):
    """Reference: O(m+n) merge (two pointers) then pick the middle."""
    merged, i, j = [], 0, 0
    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            merged.append(a[i]); i += 1
        else:
            merged.append(b[j]); j += 1
    n = len(merged)
    if n % 2:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2


def median_bs(a, b):
    if len(a) > len(b):
        a, b = b, a                     # binary search the shorter list
    m, n = len(a), len(b)
    half = (m + n + 1) // 2             # size of the combined left side
    lo, hi = 0, m                       # i = how many of a go left
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i                    # how many of b go left (0 <= j <= n since m <= n)
        a_left = a[i - 1] if i > 0 else -INF
        a_right = a[i] if i < m else INF
        b_left = b[j - 1] if j > 0 else -INF
        b_right = b[j] if j < n else INF
        if a_left <= b_right and b_left <= a_right:
            left = max(a_left, b_left)
            if (m + n) % 2:
                return float(left)
            return (left + min(a_right, b_right)) / 2
        if a_left > b_right:
            hi = i - 1                  # took too many from a
        else:
            lo = i + 1                  # took too few from a
    raise ValueError("inputs not sorted or both empty")


examples = [([1, 3], [2], 2.0), ([1, 2], [3, 4], 2.5), ([], [5], 5.0),
            ([0, 0], [0, 0], 0.0), ([1, 2, 3], [], 2.0)]
for a, b, exp in examples:
    got = median_bs(a, b)
    assert got == median_merge(a, b) == exp, (a, b, got, exp)
    print(a, b, "->", got)

random.seed(12)
cases = 0
for _ in range(2000):
    a = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 7)))
    b = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 7)))
    if not a and not b:
        continue
    assert median_bs(a, b) == median_merge(a, b) == (lambda s: float(s[len(s)//2]) if len(s) % 2 else (s[len(s)//2-1] + s[len(s)//2]) / 2)(sorted(a + b)), (a, b)
    cases += 1
print("cross-check: %d seeded cases agree (merge, binary search, sorted()-based)" % cases)

# edge cases: argument order, one empty, disjoint ranges, big values, huge one-sided
assert median_bs([5], []) == 5.0
assert median_bs([1, 2, 3], [10, 11, 12]) == 6.5
assert median_bs([10, 11, 12], [1, 2, 3]) == 6.5
assert median_bs([-10**9], [10**9]) == 0.0
assert median_bs([7], [1, 2, 3, 4, 5, 6, 8, 9]) == 5.0
big_a = list(range(0, 2000, 2))
big_b = list(range(1, 2000, 2))
assert median_bs(big_a, big_b) == median_merge(big_a, big_b) == 999.5
print("edge asserts passed")
```

**Output (my run):**
```text
[1, 3] [2] -> 2.0
[1, 2] [3, 4] -> 2.5
[] [5] -> 5.0
[0, 0] [0, 0] -> 0.0
[1, 2, 3] [] -> 2.0
cross-check: 1978 seeded cases agree (merge, binary search, sorted()-based)
edge asserts passed
```

**Edge cases:**
- One list empty: `m = 0`, only `i = 0`, `j = half`, the median comes from the other list.
- Both lists identical or all equal: ties are allowed (`<=`), so a cut is found at once.
- Disjoint ranges (all of `a` below all of `b`): the cut sits at the end of `a` or at 0.
- Odd total versus even total. Even total returns a float, e.g. 2.5; odd returns `float(x)`.
- Negative numbers and large values: no arithmetic on them except the average, which Python ints handle exactly.

**Follow-ups:**
- *Why binary search the shorter list?* It keeps `j` in range and gives log of the smaller size. Searching the longer one can give a negative `j` or an out-of-range one.
- *Find the k-th smallest of two sorted lists?* Same idea with `half = k`; the cut is valid by the same rule.
- *Lists too big for memory?* Binary search needs random access. On streams, use two heaps for a running median instead.

**Common mistakes:**
- `half = (m + n) // 2` for odd totals: the left side ends one short.
- Forgetting the sentinels, then indexing `a[-1]` or `a[m]`.
- Using `<` instead of `<=` in the validity test: wrongly rejects equal borders.
- Returning an int for an even total with integer division.

### Q13 ⭐⭐⭐ 🔴 Split array largest sum. `nums` is a list of non-negative integers (1 <= len <= 1000, values up to 10^6) and k is an integer with 1 <= k <= len(nums). Split nums into exactly k non-empty contiguous subarrays so that the largest subarray sum is as small as possible, and return that value. Binary search the answer between max(nums) and sum(nums) with the predicate 'can be cut into at most S-sum pieces using <= k pieces'. Explain why requiring 'at most k pieces' in the predicate gives the same answer as 'exactly k' (splitting a piece further never raises the maximum, and k <= len(nums) leaves room to split), and give the O(k * n^2) DP as the reference. Example: [7,2,5,10,8], k=2 -> 18; [1,2,3,4,5], k=2 -> 9; [1,4,4], k=3 -> 4; [5], k=1 -> 5.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports)

**Pattern:** Binary search on the answer (min-max). The answer is a number in `[max(nums), sum(nums)]`; "can we do it with largest piece <= S?" is monotone in S, so find the first True.

**Say this first (1 line):** "Guess the largest allowed piece sum S, greedily cut left to right and count pieces; if the count is at most k, S works. Smaller S needs more pieces, so I binary search the smallest working S, O(n log(sum))."

**Brute force:** DP: `f(i, j)` = best largest-sum for the first `i` elements in `j` pieces, trying every last cut. O(k * n^2) with prefix sums (the code's reference, plus a second brute force over all cut sets).

**Optimal:**
- Lower bound `max(nums)`: some piece contains the biggest element. Upper bound `sum(nums)`: one piece (k = 1).
- Predicate `pieces_needed(S) <= k`. Greedy is optimal for a fixed S: extend a piece as long as it fits, start a new one only when forced. Fewest pieces for that cap.
- Monotone: raising S never needs more pieces. So the predicate is False...True; use the first-True template (`hi = mid` on True, `lo = mid + 1` on False).
- **Why "at most k" equals "exactly k":** if a split uses fewer than k pieces, split any piece with 2+ elements into two. Each new part has a sum no larger than the old piece, so the maximum does not rise. Repeat until there are k pieces. This needs enough elements to split, and `k <= len(nums)` guarantees that (the total pieces can reach `len(nums)`). So the smallest S with "at most k" is also feasible with exactly k, and nothing feasible with exactly k is excluded. I also checked this exhaustively in the code.
- Returned `lo` is always achievable: the first True value is a real piece sum, since the greedy max for that S equals some actual subarray sum.

**Complexity:** Each check is O(n); about `log2(sum)` checks (at most about 30 for sums up to 10^9). Total O(n log(sum)), O(1) space. The DP is O(k * n^2) time (n = 1000 gives up to 10^9 steps, too slow).

**Dry run:** `[7,2,5,10,8]`, k = 2, search `[10, 32]`
| lo | hi | mid | greedy pieces for cap mid | <= 2? | next |
|---|---|---|---|---|---|
| 10 | 32 | 21 | [7,2,5] [10,8] = 2 | yes | hi = 21 |
| 10 | 21 | 15 | [7,2,5] [10] [8] = 3 | no | lo = 16 |
| 16 | 21 | 18 | [7,2,5] [10,8] = 2 | yes | hi = 18 |
| 16 | 18 | 17 | [7,2,5] [10] [8] = 3 | no | lo = 18 |
Stop at 18.

**Code:**
```python
import itertools
import random
from functools import lru_cache


def split_dp(nums, k):
    """Reference O(k * n^2): dp over (elements used, pieces left), exactly k pieces."""
    n = len(nums)
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    INF = float("inf")

    @lru_cache(maxsize=None)
    def f(i, j):
        if j == 0:
            return 0 if i == n else INF
        best = INF
        for m in range(i + 1, n - j + 2):      # leave at least j-1 elements for the rest
            best = min(best, max(pre[m] - pre[i], f(m, j - 1)))
        return best

    return f(0, k)


def pieces_needed(nums, cap):
    """Greedy: fewest pieces so every piece sum <= cap (needs cap >= max(nums))."""
    pieces, cur = 1, 0
    for x in nums:
        if cur + x > cap:
            pieces += 1
            cur = 0
        cur += x
    return pieces


def split_bs(nums, k):
    lo, hi = max(nums), sum(nums)       # answer lies in [max, sum]
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces_needed(nums, mid) <= k:   # 'at most k' is monotone in mid
            hi = mid
        else:
            lo = mid + 1
    return lo


def split_cuts(nums, k):
    """Second reference: try every set of k-1 cut points (exactly k pieces)."""
    n = len(nums)
    best = None
    for cuts in itertools.combinations(range(1, n), k - 1):
        b = (0,) + cuts + (n,)
        v = max(sum(nums[b[t]:b[t + 1]]) for t in range(k))
        best = v if best is None else min(best, v)
    return best


examples = [([7, 2, 5, 10, 8], 2, 18), ([1, 2, 3, 4, 5], 2, 9), ([1, 4, 4], 3, 4), ([5], 1, 5)]
for nums, k, exp in examples:
    got = split_bs(nums, k)
    assert got == split_dp(tuple(nums), k) == split_cuts(nums, k) == exp, (nums, k, got)
    print(nums, "k =", k, "->", got)

random.seed(13)
for _ in range(600):
    n = random.randint(1, 8)
    nums = [random.randint(0, 7) for _ in range(n)]
    k = random.randint(1, n)
    assert split_bs(nums, k) == split_dp(tuple(nums), k) == split_cuts(nums, k), (nums, k)
print("cross-check: 600 seeded cases agree (binary search, DP, all-cuts brute force)")

# exhaustive proof-by-enumeration of the 'at most k == exactly k' claim on all tiny inputs
checked = 0
for n in range(1, 6):
    for nums in itertools.product(range(0, 4), repeat=n):
        for k in range(1, n + 1):
            at_most = next(S for S in range(max(nums), sum(nums) + 1)
                           if pieces_needed(list(nums), S) <= k)
            assert at_most == split_cuts(list(nums), k), (nums, k)
            checked += 1
print("exhaustive: 'at most k pieces' == 'exactly k pieces' on %d (list, k) inputs" % checked)

# edge cases
assert split_bs([0, 0, 0], 2) == 0
assert split_bs([10], 1) == 10
assert split_bs([1, 1, 1, 1], 4) == 1          # k == len: every element alone -> max
assert split_bs([1, 1, 1, 1], 1) == 4          # k == 1: whole sum
assert split_bs([10**6] * 1000, 1) == 10**9    # max size: sum 10^9 fits easily in a Python int
assert split_bs([5, 5, 5, 5], 3) == 10         # pieces can't be balanced exactly
print("edge asserts passed")
```

**Output (my run):**
```text
[7, 2, 5, 10, 8] k = 2 -> 18
[1, 2, 3, 4, 5] k = 2 -> 9
[1, 4, 4] k = 3 -> 4
[5] k = 1 -> 5
cross-check: 600 seeded cases agree (binary search, DP, all-cuts brute force)
exhaustive: 'at most k pieces' == 'exactly k pieces' on 6372 (list, k) inputs
edge asserts passed
```

**Edge cases:**
- `k = 1`: answer is `sum(nums)`. `k = len(nums)`: answer is `max(nums)`.
- Single element.
- All zeros: `max = sum = 0`, loop never runs, answer 0 (greedy cap 0 still works because `0 + 0 > 0` is False).
- Max size: sum up to 10^9, no overflow in Python (in C++ or Java use a 64-bit type anyway for safety).
- Pieces cannot be balanced exactly (`[5,5,5,5]`, k = 3 gives 10, not 7).

**Follow-ups:**
- *Same pattern elsewhere?* Capacity to ship in D days and book allocation are the same code; painter's partition too.
- *Why is greedy right for a fixed S?* Cutting later never hurts: any valid split can be shifted so each piece takes as much as fits (exchange argument).
- *Can you print the split?* Re-run the greedy at the final S; it gives a valid split with at most k pieces, and you can split further to reach exactly k.

**Common mistakes:**
- Lower bound 0 or 1 instead of `max(nums)`: the greedy would then place an element larger than the cap.
- Resetting `cur = x` instead of `cur = 0` then adding (double counting or off by one on the new piece).
- Using `pieces < k` or `== k` as the predicate. `== k` is not monotone.
- Returning `hi` after a loop that tests `lo <= hi` with the wrong shrink rule.

### Q14 ⭐⭐ 🟢 Valid perfect square without a square-root call. Given an integer `num` with 1 <= num <= 2^31 - 1, return True if it is the square of an integer, without `math.sqrt`, `**0.5` or `math.isqrt`. Binary search on the root r in [1, num] comparing r * r with num (or [1, 46341]); say why no floating point is needed. Example: 16 -> True; 14 -> False; 1 -> True; 2 -> False; 2147395600 -> True; 2147483647 -> False.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Binary search on the answer (the root), checked with exact integer arithmetic. The predicate `r * r >= num` is False...True in r.

**Say this first (1 line):** "Binary search r in [1, num] comparing r*r with num; integer multiplication is exact, so there is no float rounding to worry about, and the loop is O(log num)."

**Brute force:** Try r = 1, 2, 3, ... until `r*r >= num`. At most 46340 steps for a 32-bit input; O(sqrt(num)). Correct but the interviewer wants log.

**Optimal:**
- Search `lo, hi = 1, num` (or `min(num, 46341)`, since `46341^2 > 2^31 - 1`).
- `sq = mid * mid`. If `sq == num` return True. If `sq < num`, `lo = mid + 1`; else `hi = mid - 1`.
- If the range empties, no integer square equals num.
- Invariant: if a root exists, it lies in `[lo, hi]`.
- **Why no floating point:** `math.sqrt` returns a float. It is fine for 32-bit values, but a float sqrt can round wrongly for large integers (above 2^53 not every integer is representable), and the question forbids it anyway. `mid * mid` is exact in Python's big ints.
- In C++ or Java, `mid * mid` can overflow 32-bit ints. Use a 64-bit type or compare `mid <= num // mid`.

**Complexity:** O(log num) time (about 31 steps worst case; about 16 with the 46341 cap), O(1) space.

**Dry run:** `num = 14`, `lo = 1`, `hi = 14`
| lo | hi | mid | mid^2 | next |
|---|---|---|---|---|
| 1 | 14 | 7 | 49 > 14 | hi = 6 |
| 1 | 6 | 3 | 9 < 14 | lo = 4 |
| 4 | 6 | 5 | 25 > 14 | hi = 4 |
| 4 | 4 | 4 | 16 > 14 | hi = 3 |
`lo > hi`: return False.

**Code:**
```python
import math


def is_square_bs(num):
    lo, hi = 1, min(num, 46341)          # 46341^2 > 2^31 - 1, so the root is <= 46340
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def is_square_brute(num):
    r = 1
    while r * r < num:
        r += 1
    return r * r == num


def is_square_odd_sum(num):
    """1 + 3 + 5 + ... = k^2: subtract odd numbers until we hit 0 or go negative."""
    odd = 1
    while num > 0:
        num -= odd
        odd += 2
    return num == 0


examples = [(16, True), (14, False), (1, True), (2, False), (2147395600, True), (2147483647, False)]
for num, exp in examples:
    got = is_square_bs(num)
    assert got == exp, (num, got)
    print(num, "->", got)

# exhaustive over every num in 1..200000 against brute force and math.isqrt (checking tool only)
for num in range(1, 200001):
    expected = math.isqrt(num) ** 2 == num
    assert is_square_bs(num) == is_square_brute(num) == is_square_odd_sum(num) == expected, num
print("cross-check: all num in 1..200000 agree (binary search, linear scan, odd-sum, isqrt)")

# boundary of the 32-bit range: every perfect square near the top and its neighbours
for r in range(46330, 46341):
    assert is_square_bs(r * r)
    assert not is_square_bs(r * r - 1)
    if r * r + 1 <= 2**31 - 1:
        assert not is_square_bs(r * r + 1)
assert 46340 ** 2 == 2147395600 and 46341 ** 2 > 2**31 - 1
assert is_square_bs(2**31 - 1) is False
assert is_square_bs(2**30) is True          # 32768^2
print("edge asserts passed")
```

**Output (my run):**
```text
16 -> True
14 -> False
1 -> True
2 -> False
2147395600 -> True
2147483647 -> False
cross-check: all num in 1..200000 agree (binary search, linear scan, odd-sum, isqrt)
edge asserts passed
```

**Edge cases:**
- `num = 1`: root 1, found at the first probe.
- `num = 2`, `3`: no root.
- Largest values: `2147395600 = 46340^2` is True; `2147483647` is False.
- Perfect square minus or plus one (checked around the 32-bit limit in the code).

**Follow-ups:**
- *Integer square root?* Same loop returning the last r with `r*r <= num` (last-True template).
- *Other no-sqrt methods?* Subtract odd numbers 1, 3, 5... (O(sqrt n)), or Newton's iteration `r = (r + num // r) // 2`, which converges very fast.
- *Why is hi = num wasteful?* The root never exceeds about sqrt(num); capping hi saves a few steps but not the big-O.

**Common mistakes:**
- `lo = mid` or `hi = mid` in this `while lo <= hi` loop: infinite loop.
- `mid * mid` overflow in fixed-width languages.
- Starting `lo` at 0 and mishandling `num = 0` (not in the constraints, but check the range given).
- Using `int(num ** 0.5) ** 2 == num` and trusting it for big numbers.

### Q15 ⭐⭐ 🟢 First bad version. Versions are numbered 1..n (1 <= n <= 2^31 - 1). There is an unknown version f such that versions f..n are bad and 1..f-1 are good, and you may call only `is_bad(v)`. Find f using at most ceil(log2(n)) calls to is_bad. Use `lo, hi = 1, n` with `while lo < hi` and `hi = mid` on a bad mid; show why the loop never calls is_bad on an index twice and why this finds the first True of a monotone False...True predicate. Example: n=5, f=4 -> 4; n=1, f=1 -> 1; n=2, f=2 -> 2; n=10**9 with f=10**9 -> 10**9 using at most 30 calls.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** First True of a monotone False...True predicate (`is_bad`), with a call budget. The classic lower-bound template where the answer is always inside the range.

**Say this first (1 line):** "Versions 1 to f-1 are good, f to n are bad, so is_bad is False then True; binary search with `hi = mid` on bad and `lo = mid + 1` on good, at most ceil(log2 n) calls."

**Brute force:** Call `is_bad` on 1, 2, 3 ... until it says bad. Up to n calls. For n = 10^9 that is far over the 30-call budget.

**Optimal:**
- `lo, hi = 1, n`; `while lo < hi`.
- `mid = lo + (hi - lo) // 2` (same as `(lo + hi) // 2` in Python; the safe form avoids overflow in fixed-width ints).
- If `is_bad(mid)`: `hi = mid` (mid may be the first bad one, so keep it). Else `lo = mid + 1` (mid is good, the first bad is after it).
- Invariant: the first bad version is always in `[lo, hi]`. Version n is bad (f <= n), so the upper end is always a valid candidate.
- When `lo == hi`, that version is the answer. We never needed to call `is_bad` on it.
- **Never asks the same version twice:** after a good answer, `lo` moves above mid. After a bad answer, `hi = mid`, and the next probe is `lo + (mid - lo) // 2`, which is strictly below mid whenever `lo < mid` (if `lo == mid` the loop has ended). Every call is on a new index. I verified this by recording every call.
- **Why this finds the first True:** `hi` only ever moves to a version that answered bad; `lo` only ever moves past a version that answered good. By monotonicity everything below `lo` is good and everything from `hi` up is bad, so when they meet that version is the first bad one.

**Complexity:** With window size s = hi - lo + 1, a call leaves a window of at most ceil(s / 2). It starts at n and stops at 1, so at most `ceil(log2 n)` calls. O(1) space. The code counts calls with a wrapper class and asserts the budget for every n up to 600 and every f.

**Dry run:** `n = 5`, `f = 4`
| lo | hi | mid | is_bad(mid) | next |
|---|---|---|---|---|
| 1 | 5 | 3 | False | lo = 4 |
| 4 | 5 | 4 | True | hi = 4 |
Stop at 4 after 2 calls (budget ceil(log2 5) = 3).

**Code:**
```python
import math
import random


def first_bad(n, is_bad):
    lo, hi = 1, n
    while lo < hi:
        mid = lo + (hi - lo) // 2      # same as (lo+hi)//2 here; the safe form in fixed-width ints
        if is_bad(mid):
            hi = mid                   # mid might be the first bad: keep it
        else:
            lo = mid + 1               # mid is good: first bad is strictly after it
    return lo


def first_bad_linear(n, is_bad):
    for v in range(1, n + 1):
        if is_bad(v):
            return v


class Oracle:
    """Counts calls and records which versions were asked."""
    def __init__(self, f):
        self.f, self.calls, self.asked = f, 0, []

    def __call__(self, v):
        self.calls += 1
        self.asked.append(v)
        return v >= self.f


for n, f in [(5, 4), (1, 1), (2, 2)]:
    o = Oracle(f)
    got = first_bad(n, o)
    assert got == f
    print("n=%d f=%d -> %d (calls %d)" % (n, f, got, o.calls))
o = Oracle(10**9)
got = first_bad(10**9, o)
assert got == 10**9
print("n=10**9 f=10**9 -> %d with %d calls (budget ceil(log2 n) = %d)" % (got, o.calls, math.ceil(math.log2(10**9))))
assert o.calls <= 30

# exhaustive: every n up to 600 and every f: right answer, <= ceil(log2 n) calls, no version asked twice
worst = {}
for n in range(1, 601):
    budget = math.ceil(math.log2(n))
    for f in range(1, n + 1):
        o = Oracle(f)
        assert first_bad(n, o) == f == first_bad_linear(n, lambda v: v >= f), (n, f)
        assert o.calls <= budget, (n, f, o.calls, budget)
        assert len(set(o.asked)) == len(o.asked), (n, f, o.asked)
        worst[n] = max(worst.get(n, 0), o.calls)
print("exhaustive: n in 1..600, every f: correct, within ceil(log2 n) calls, no repeated call")
print("worst-case calls observed: n=1 ->", worst[1], ", n=2 ->", worst[2], ", n=5 ->", worst[5],
      ", n=512 ->", worst[512], ", n=600 ->", worst[600])

# seeded large n: sample f including both ends
random.seed(15)
for n in (2**31 - 1, 10**9, 2**20, 2**20 + 1):
    budget = math.ceil(math.log2(n))
    for f in [1, 2, n - 1, n, n // 2, n // 2 + 1] + [random.randint(1, n) for _ in range(300)]:
        f = max(1, min(n, f))
        o = Oracle(f)
        assert first_bad(n, o) == f and o.calls <= budget and len(set(o.asked)) == len(o.asked)
print("seeded large-n sample (n up to 2^31-1): all within budget")
assert first_bad(1, lambda v: True) == 1
print("edge asserts passed")
```

**Output (my run):**
```text
n=5 f=4 -> 4 (calls 2)
n=1 f=1 -> 1 (calls 0)
n=2 f=2 -> 2 (calls 1)
n=10**9 f=10**9 -> 1000000000 with 29 calls (budget ceil(log2 n) = 30)
exhaustive: n in 1..600, every f: correct, within ceil(log2 n) calls, no repeated call
worst-case calls observed: n=1 -> 0 , n=2 -> 1 , n=5 -> 3 , n=512 -> 9 , n=600 -> 10
seeded large-n sample (n up to 2^31-1): all within budget
edge asserts passed
```

**Edge cases:**
- `n = 1`: loop does not run, 0 calls, answer 1 (budget ceil(log2 1) = 0).
- `f = 1`: all versions bad, `hi` shrinks to 1.
- `f = n`: every probe is good until the end; `n = 10**9` took 29 calls, within the 30 budget.
- `n` near 2^31 - 1: `lo + hi` would overflow a 32-bit int; use `lo + (hi - lo) // 2`.

**Follow-ups:**
- *What if the predicate may be wrong for some versions?* Then it is not monotone and binary search has no guarantee.
- *Why `lo < hi` and not `lo <= hi`?* With `hi = mid` on bad, `lo <= hi` would loop forever once `lo == hi == mid`.
- *Unknown n?* Double an upper bound (1, 2, 4, ...) until bad, then search below it (galloping search).

**Common mistakes:**
- `hi = mid - 1` on bad: skips the true first bad version.
- `lo <= hi` with `hi = mid`: infinite loop.
- `(lo + hi) // 2` in a language with 32-bit ints.
- Calling `is_bad(lo)` once more at the end to "confirm": wastes a call and can break the budget.

### Q16 ⭐⭐ 🟢 Smallest letter greater than the target (circular). `letters` is a sorted non-decreasing list of lowercase letters with at least two distinct letters (2 <= len <= 10^4) and `target` is a lowercase letter. Return the smallest letter in `letters` that is strictly greater than target, wrapping around so that if none is greater you return letters[0]. Use the upper bound and a modulo. Example: ['c','f','j'], 'a' -> 'c'; ['c','f','j'], 'c' -> 'f'; ['c','f','j'], 'j' -> 'c'; ['x','x','y','y'], 'z' -> 'x'; ['x','x','y','y'], 'x' -> 'y'.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Python documentation mirrors for bisect (docs.python.org 3.10 and current .rst source: key added in 3.10, key not applied to the search value in bisect_left/bisect_right, insort is O(n) overall; snippets only, direct fetch failed with ENOTFOUND; behaviour re-verified in the sandbox) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Upper bound plus modulo wrap. "Smallest element strictly greater than the target" is `upper_bound`; running off the end wraps to index 0.

**Say this first (1 line):** "`i = bisect_right(letters, target)`, answer `letters[i % len(letters)]`: the first letter strictly greater than target, wrapping to the first letter when none is."

**Brute force:** Scan left to right, return the first letter greater than target; if none, return `letters[0]`. O(n).

**Optimal:**
- Binary search for the first index with `letters[i] > target` (upper bound): if `letters[mid] <= target`, `lo = mid + 1`; else `hi = mid`.
- Result `lo` is in `[0, n]`. `lo % n` turns `n` (nothing greater) into 0 (wrap).
- Using `<=` is what handles duplicates and the "strictly greater" rule: if target is in the list, we skip past all copies of it. Using `<` would return the target itself.
- Letters compare as strings (`'a' < 'b'`), so no conversion is needed.

**Complexity:** O(log n) time, O(1) space.

**Dry run:** `['c','f','j']`, target `'c'`
| lo | hi | mid | letters[mid] <= 'c'? | next |
|---|---|---|---|---|
| 0 | 3 | 1 | 'f' no | hi = 1 |
| 0 | 1 | 0 | 'c' yes | lo = 1 |
`lo = 1`, answer `letters[1] = 'f'`. For target `'j'`: lo ends at 3, `3 % 3 = 0`, answer `'c'`.

**Code:**
```python
import itertools
import random
from bisect import bisect_right


def next_letter(letters, target):
    return letters[bisect_right(letters, target) % len(letters)]


def next_letter_manual(letters, target):
    lo, hi = 0, len(letters)
    while lo < hi:                       # upper bound: first index with letters[i] > target
        mid = (lo + hi) // 2
        if letters[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return letters[lo % len(letters)]    # lo == len -> wrap to index 0


def next_letter_brute(letters, target):
    for c in letters:
        if c > target:
            return c
    return letters[0]


examples = [(['c', 'f', 'j'], 'a', 'c'), (['c', 'f', 'j'], 'c', 'f'), (['c', 'f', 'j'], 'j', 'c'),
            (list("xxyy"), 'z', 'x'), (list("xxyy"), 'x', 'y')]
for letters, t, exp in examples:
    got = next_letter(letters, t)
    assert got == next_letter_manual(letters, t) == next_letter_brute(letters, t) == exp
    print("".join(letters), t, "->", got)

# exhaustive over alphabet a..f: every sorted list of length 2..7 with >= 2 distinct letters, every target a..g
alpha = "abcdef"
n_lists = n_pairs = 0
for L in range(2, 8):
    for combo in itertools.combinations_with_replacement(alpha, L):
        if len(set(combo)) < 2:
            continue
        letters = list(combo)
        n_lists += 1
        for t in "abcdefg":
            assert next_letter(letters, t) == next_letter_manual(letters, t) == next_letter_brute(letters, t), (letters, t)
            n_pairs += 1
print("exhaustive: %d lists x 7 targets = %d cases agree" % (n_lists, n_pairs))

random.seed(16)
for _ in range(500):
    letters = sorted(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(random.randint(2, 30)))
    if len(set(letters)) < 2:
        continue
    t = random.choice("abcdefghijklmnopqrstuvwxyz")
    assert next_letter(letters, t) == next_letter_brute(letters, t)
print("seeded random check passed")

# edge cases
assert next_letter(['a', 'b'], 'z') == 'a'          # target after everything
assert next_letter(['a', 'b'], 'a') == 'b'
assert next_letter(['a', 'z'], 'a') == 'z'
assert next_letter(['a', 'z'], 'z') == 'a'          # target equals the largest letter: wrap
assert next_letter(['b', 'b', 'c'], 'a') == 'b'
print("edge asserts passed")
```

**Output (my run):**
```text
cfj a -> c
cfj c -> f
cfj j -> c
xxyy z -> x
xxyy x -> y
exhaustive: 1673 lists x 7 targets = 11711 cases agree
seeded random check passed
edge asserts passed
```

**Edge cases:**
- Target below all letters: upper bound 0, answer `letters[0]`.
- Target equals the last letter or is above it: wrap to `letters[0]`.
- Duplicates (`xxyy`): target `'x'` skips both x's and returns `'y'`.
- Target not in the list (`'a'`): works the same.
- The "at least two distinct letters" rule matters for the answer's meaning: with one distinct letter and target equal to it, wrapping would return a letter that is not strictly greater. I checked every sorted list over `a..f` of length 2 to 7 with two or more distinct letters.

**Follow-ups:**
- *Smallest letter greater than or equal?* Use the lower bound (`bisect_left`).
- *Why is the wrap a modulo and not an if?* Same thing; `% n` is shorter and has no branch to forget.
- *Letters unsorted?* One pass keeping the best candidate, O(n).

**Common mistakes:**
- Using `bisect_left`, which returns the target itself when present.
- `hi = n - 1`, so "greater than the last letter" cannot be represented.
- Forgetting the wrap and indexing `letters[n]`.
- Returning `letters[-1]` or `None` on no match.

### Q17 ⭐⭐ 🟡 Search in a rotated sorted array with duplicates. A list sorted non-decreasing (duplicates allowed) was rotated at an unknown pivot (1 <= len <= 5000). Return True if `target` is present. Adapt the 'which half is sorted' test: when nums[lo] == nums[mid] == nums[hi] you cannot tell, so shrink both ends by one. Explain why the worst case becomes O(n), and give one input where that happens. Example: [2,5,6,0,0,1,2], 0 -> True; [2,5,6,0,0,1,2], 3 -> False; [1,0,1,1,1], 0 -> True; [1,1,1,1], 2 -> False; [1,1,1,1,0,1,1], 0 -> True.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Modified binary search on a rotated array: one half is always sorted. Duplicates can hide which half, so in the ambiguous case we trim the ends.

**Say this first (1 line):** "Same as the distinct case, find the sorted half and check if the target is in it; when nums[lo] == nums[mid] == nums[hi] I cannot tell, so I shrink both ends by one, which makes the worst case O(n)."

**Brute force:** `target in nums`, O(n). It is also the reference in the code.

**Optimal:**
- Loop `while lo <= hi`. `mid = (lo + hi) // 2`. If `nums[mid] == target`, return True.
- **Ambiguous case:** `nums[lo] == nums[mid] == nums[hi]`. The target is not at mid, so it is not at `lo` or `hi` either (same value). Drop both: `lo += 1`, `hi -= 1`. This is safe because those two values equal `nums[mid]` and are not the target.
- Else if `nums[lo] <= nums[mid]`: left half `[lo..mid]` is sorted. If `nums[lo] <= target < nums[mid]`, go left (`hi = mid - 1`), else right.
- Else the right half `[mid..hi]` is sorted. If `nums[mid] < target <= nums[hi]`, go right, else left.
- Invariant: if the target exists, it is in `[lo, hi]`.

**Why the worst case is O(n):** with distinct values each step discards half. With duplicates, in the ambiguous case we only discard 2 elements, and the array can stay ambiguous every step. Input: `[1,1,1,1,...,1]` and target 2 (or all ones except one 0, target 0). Measured: all ones with n = 1000 needs 500 loop steps, n = 5000 needs 2500. That is n/2 steps, so O(n). With 1000 ones plus one 0 (target present) the worst position took 501 steps.

**Complexity:**
| Case | Time |
|---|---|
| Distinct or few duplicates | O(log n) |
| Worst case (long runs of equal values at lo, mid, hi) | O(n) |
Space O(1). No algorithm can beat O(n) in this worst case: one different element could be anywhere, and comparisons cannot find it faster.

**Dry run:** `[2,5,6,0,0,1,2]`, target 3
| lo | hi | mid | nums[mid] | case | next |
|---|---|---|---|---|---|
| 0 | 6 | 3 | 0 | `nums[lo]=2 > 0`, right half `[0,0,1,2]` sorted; 0 < 3 <= 2? no | hi = 2 |
| 0 | 2 | 1 | 5 | `2 <= 5` left sorted; 2 <= 3 < 5 yes | hi = 0 |
| 0 | 0 | 0 | 2 | `nums[lo] == nums[mid] == nums[hi]`, not the target: trim both ends | lo = 1, hi = -1 |
`lo > hi`: False. (3 loop steps, as the run shows.)

**Code:**
```python
import itertools
import random


def search_rot_dup(nums, target):
    """Returns (found, loop_iterations)."""
    lo, hi, steps = 0, len(nums) - 1, 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True, steps
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1                      # neither end can be the target (== nums[mid] != target)
            hi -= 1
        elif nums[lo] <= nums[mid]:      # left half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                            # right half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False, steps


def brute(nums, target):
    return target in nums


examples = [([2, 5, 6, 0, 0, 1, 2], 0, True), ([2, 5, 6, 0, 0, 1, 2], 3, False),
            ([1, 0, 1, 1, 1], 0, True), ([1, 1, 1, 1], 2, False), ([1, 1, 1, 1, 0, 1, 1], 0, True)]
for nums, t, exp in examples:
    got, steps = search_rot_dup(nums, t)
    assert got == exp == brute(nums, t)
    print(nums, t, "->", got, "(loop steps %d)" % steps)

# exhaustive: every sorted list over values 0..3 (len 1..8), every rotation, every target -1..4
cases = 0
for n in range(1, 9):
    for base in itertools.combinations_with_replacement(range(4), n):
        base = list(base)
        for r in range(n):
            nums = base[r:] + base[:r]
            for t in range(-1, 5):
                assert search_rot_dup(nums, t)[0] == brute(nums, t), (nums, t)
                cases += 1
print("exhaustive: %d (rotated list, target) cases agree with 'in'" % cases)

random.seed(17)
for _ in range(500):
    n = random.randint(1, 40)
    base = sorted(random.randint(0, 6) for _ in range(n))
    r = random.randrange(n)
    nums = base[r:] + base[:r]
    t = random.randint(-1, 7)
    assert search_rot_dup(nums, t)[0] == brute(nums, t)
print("seeded random check: 500 cases agree")

# worst case: all equal, target absent -> every step removes only 2 elements
for n in (100, 1000, 5000):
    found, steps = search_rot_dup([1] * n, 2)
    print("all ones, n=%d, target 2: found=%s, loop steps=%d" % (n, found, steps))
    assert not found and steps == (n + 1) // 2
# one odd element (a 0) in a sea of ones, target 0 present: worst position over all placements
n = 1000
worst = max(search_rot_dup([1] * p + [0] + [1] * (n - 1 - p), 0)[1] for p in range(n))
print("1000 ones with one 0, target 0 present: worst loop steps over all positions =", worst)
# distinct values: log steps
found, steps = search_rot_dup(list(range(2500, 5000)) + list(range(2500)), 7777)
print("5000 distinct rotated, absent target: steps =", steps)

# edge cases
assert search_rot_dup([1], 1)[0] is True and search_rot_dup([1], 0)[0] is False
assert search_rot_dup([3, 1], 1)[0] is True
assert search_rot_dup([1, 3, 1, 1, 1], 3)[0] is True
assert search_rot_dup([1, 1, 3, 1], 3)[0] is True
print("edge asserts passed")
```

**Output (my run):**
```text
[2, 5, 6, 0, 0, 1, 2] 0 -> True (loop steps 1)
[2, 5, 6, 0, 0, 1, 2] 3 -> False (loop steps 3)
[1, 0, 1, 1, 1] 0 -> True (loop steps 3)
[1, 1, 1, 1] 2 -> False (loop steps 2)
[1, 1, 1, 1, 0, 1, 1] 0 -> True (loop steps 4)
exhaustive: 19008 (rotated list, target) cases agree with 'in'
seeded random check: 500 cases agree
all ones, n=100, target 2: found=False, loop steps=50
all ones, n=1000, target 2: found=False, loop steps=500
all ones, n=5000, target 2: found=False, loop steps=2500
1000 ones with one 0, target 0 present: worst loop steps over all positions = 501
5000 distinct rotated, absent target: steps = 13
edge asserts passed
```

**Edge cases:**
- All elements equal: absent target costs about n/2 steps.
- Not rotated (or rotated by n): still works, the left half is always sorted.
- Duplicates straddling the pivot (`[1,0,1,1,1]`, `[1,1,1,1,0,1,1]`).
- One element.
- Target equal to `nums[lo]` or `nums[hi]` only (the shrink must not skip a real target: it only runs after `nums[mid] != target` and all three are equal).

**Follow-ups:**
- *Why not do `lo += 1` only?* Also correct, but trimming both ends halves the number of steps; we know both equal `nums[mid]`.
- *Find the rotation point?* That is the minimum search (next question), same O(n) worst case.
- *Return the index?* Possible, but with duplicates any matching index is acceptable unless the problem says first; state that.

**Common mistakes:**
- Using `nums[lo] < nums[mid]` instead of `<=` to detect the sorted left half (breaks when `lo == mid`).
- Shrinking without checking `nums[mid] == target` first.
- Claiming O(log n) for the duplicate version.
- Strict versus non-strict comparisons at the half's edges (`target < nums[mid]` on the left half, `target <= nums[hi]` on the right).

### Q18 ⭐⭐ 🟡 Find the minimum in a rotated sorted array with duplicates. The list was sorted non-decreasing, duplicates allowed, then rotated (1 <= len <= 5000). Return the smallest value. Compare nums[mid] with nums[hi]: if greater, go right; if smaller, `hi = mid`; if equal, do `hi -= 1`. Explain why dropping hi when nums[mid] == nums[hi] never loses the minimum (the value at hi is still represented at mid), why the worst case is O(n), and which line of the distinct-values solution this breaks. Example: [1,3,5] -> 1; [2,2,2,0,1] -> 0; [10,1,10,10,10] -> 1; [3,3,1,3] -> 1; [2,2,2,2] -> 2.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search on a rotated array comparing `nums[mid]` with `nums[hi]` (the right end tells which side the minimum is on). With duplicates, an equal comparison needs a linear shrink.

**Say this first (1 line):** "Compare mid with hi: bigger means the minimum is to the right, smaller means mid might be it, equal means I cannot tell so I drop hi by one; worst case O(n)."

**Brute force:** `min(nums)`, O(n). Used as the reference in the code.

**Optimal:**
- `lo, hi = 0, n - 1`; `while lo < hi`; `mid = (lo + hi) // 2`.
- `nums[mid] > nums[hi]`: the drop (the pivot) is in `(mid, hi]`, so `lo = mid + 1`.
- `nums[mid] < nums[hi]`: `[mid..hi]` is sorted, mid could be the minimum, so `hi = mid`.
- `nums[mid] == nums[hi]`: `hi -= 1`.
- **Why `hi -= 1` never loses the minimum value:** `mid < hi` (because `lo < hi`) and `nums[mid] == nums[hi]`. If `nums[hi]` was the minimum, the same value is still at `mid`, inside the new range. So the minimum value stays in `[lo, hi - 1]`. (The minimum's index may be lost, e.g. `[1,1]` loses index 1, which is fine for the value. If the question wanted the first index of the minimum, this needs care: check whether `nums[hi-1] > nums[hi]` before dropping.)
- **Which line breaks:** the distinct-values solution has only two branches: `if nums[mid] > nums[hi]: lo = mid + 1 else: hi = mid`. Its `else` lumps "equal" with "smaller". With duplicates, `[3,3,1,3]`: mid = 1, `3 == 3`, `hi = mid` throws away the 1 on the right. The code shows it returning 3. And `lo = mid + 1` on equal fails on `[10,1,10,10,10]`. So the equal case needs its own branch.
- Invariant: the minimum value is always in `nums[lo..hi]`.

**Complexity:**
| Case | Time |
|---|---|
| Distinct values | O(log n) |
| Worst case (all equal, or a hidden small value among equals) | O(n): every step is `hi -= 1` (n - 1 steps for all equal) |
Space O(1). Measured: all equal n = 5000 takes 4999 steps; a 1 hidden in 5000 tens took 2510 steps; 5000 distinct rotated values took 13.

**Dry run:** `[3,3,1,3]`
| lo | hi | mid | nums[mid] vs nums[hi] | action |
|---|---|---|---|---|
| 0 | 3 | 1 | 3 == 3 | hi = 2 |
| 0 | 2 | 1 | 3 > 1 | lo = 2 |
`lo == hi == 2`: answer `nums[2] = 1`.

**Code:**
```python
import itertools
import random


def find_min_dup(nums):
    """Returns (min value, loop steps)."""
    lo, hi, steps = 0, len(nums) - 1, 0
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1                 # min is strictly right of mid
        elif nums[mid] < nums[hi]:
            hi = mid                     # mid could be the min
        else:
            hi -= 1                      # equal: drop hi; value still held at mid
    return nums[lo], steps


def find_min_distinct(nums):
    """The distinct-values version: equal case is lumped with '<'. WRONG with duplicates."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


examples = [([1, 3, 5], 1), ([2, 2, 2, 0, 1], 0), ([10, 1, 10, 10, 10], 1), ([3, 3, 1, 3], 1), ([2, 2, 2, 2], 2)]
for nums, exp in examples:
    got, steps = find_min_dup(nums)
    assert got == exp == min(nums)
    print(nums, "->", got, "| distinct-version gives", find_min_distinct(nums))

cases = wrong = 0
for n in range(1, 9):
    for base in itertools.combinations_with_replacement(range(4), n):
        base = list(base)
        for r in range(n):
            nums = base[r:] + base[:r]
            assert find_min_dup(nums)[0] == min(nums), nums
            cases += 1
            if find_min_distinct(nums) != min(nums):
                wrong += 1
print("exhaustive: %d rotated lists, find_min_dup always == min(nums)" % cases)
print("the distinct-values version (equal lumped with '<') is wrong on %d of them" % wrong)

random.seed(18)
for _ in range(500):
    n = random.randint(1, 50)
    base = sorted(random.randint(-3, 3) for _ in range(n))
    r = random.randrange(n)
    nums = base[r:] + base[:r]
    assert find_min_dup(nums)[0] == min(nums)
print("seeded random check: 500 cases agree")

for n in (1000, 5000):
    print("all equal, n=%d: loop steps = %d" % (n, find_min_dup([4] * n)[1]))
    assert find_min_dup([4] * n)[1] == n - 1
nums = [10] * 5000
nums[2500] = 1
print("5000 tens with one 1 hidden mid-array: min, steps =", find_min_dup(nums))
print("5000 distinct rotated: steps =", find_min_dup(list(range(2500, 5000)) + list(range(2500)))[1])

assert find_min_dup([7])[0] == 7
assert find_min_dup([2, 1])[0] == 1
assert find_min_dup([1, 1, 1, 0, 1])[0] == 0
assert find_min_dup([0, 0, 0])[0] == 0
print("edge asserts passed")
```

**Output (my run):**
```text
[1, 3, 5] -> 1 | distinct-version gives 1
[2, 2, 2, 0, 1] -> 0 | distinct-version gives 0
[10, 1, 10, 10, 10] -> 1 | distinct-version gives 1
[3, 3, 1, 3] -> 1 | distinct-version gives 3
[2, 2, 2, 2] -> 2 | distinct-version gives 2
exhaustive: 3168 rotated lists, find_min_dup always == min(nums)
the distinct-values version (equal lumped with '<') is wrong on 147 of them
seeded random check: 500 cases agree
all equal, n=1000: loop steps = 999
all equal, n=5000: loop steps = 4999
5000 tens with one 1 hidden mid-array: min, steps = (1, 2510)
5000 distinct rotated: steps = 13
edge asserts passed
```

**Edge cases:**
- All equal: `hi` walks down, O(n), returns that value.
- Not rotated: `nums[mid] < nums[hi]` each time, `hi = mid` converges to index 0.
- Minimum hidden among equal values (`[10,1,10,10,10]`).
- Single element, two elements.
- Compare with `nums[hi]`, not `nums[lo]`: with `lo` the unrotated case is ambiguous.

**Follow-ups:**
- *Why not just compare with `nums[lo]`?* If `nums[mid] >= nums[lo]` you cannot tell whether the array is rotated at all (sorted array also satisfies it), so you need extra handling.
- *Can this be better than O(n) worst case?* No: with all equal but one smaller element, any algorithm may have to look at every position.
- *Use it to search?* Find the pivot, then binary search the correct sorted piece (the pivot step is still O(n) worst case with duplicates).

**Common mistakes:**
- Using the distinct-values code as is (wrong on 147 of the 3168 rotated lists in my exhaustive check).
- `lo = mid + 1` on equal (can skip the minimum).
- `hi = mid` on equal (can skip the minimum).
- Claiming O(log n) overall.

### Q19 ⭐⭐ 🟡 Minimum number of days to make m bouquets. `bloom_day[i]` is the day flower i blooms (1 <= len <= 10^5, values up to 10^9). A bouquet needs k adjacent flowers that have all bloomed. Return the minimum day on which you can make m bouquets using each flower at most once, or -1 if len < m * k. Binary search the day over [min(bloom_day), max(bloom_day)] with a left-to-right counter of consecutive bloomed flowers that resets after each bouquet and on each unbloomed flower. Example: bloom_day=[1,10,3,10,2], m=3, k=1 -> 3; the same list with m=3, k=2 -> -1; [7,7,7,7,12,7,7], m=2, k=3 -> 12; [1,10,2,9,3,8,4,7,5,6], m=4, k=2 -> 9.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports)

**Pattern:** Binary search on the answer (the day), with a greedy counting check. If you can make m bouquets by day d, you can by any later day, so the predicate is False...True.

**Say this first (1 line):** "Guess a day, count how many bouquets of k adjacent bloomed flowers I can form greedily left to right; if that is at least m the day works, so I binary search the earliest day, O(n log(max day))."

**Brute force:** Try each distinct bloom day in ascending order and count bouquets: O(n) per day, up to n days, O(n^2) overall (the code also has a recursive window brute force as an independent check).

**Optimal:**
- If `len(bloom) < m * k`, return -1: not enough flowers even when all are open. Otherwise at `max(bloom)` everything is open, and the greedy gives `len // k >= m`, so the answer exists.
- Count for day d: walk left to right with `run` (consecutive bloomed). Bloomed: `run += 1`; when `run == k`, `count += 1` and `run = 0` (those flowers are used). Not bloomed: `run = 0`.
- Search `lo, hi = min(bloom), max(bloom)` with first-True: `count >= m` gives `hi = mid`, else `lo = mid + 1`.
- Invariant: the answer is in `[lo, hi]`; `hi` is always feasible.
- Greedy is right: taking a bouquet as soon as `k` adjacent flowers are open leaves the most flowers for later ones (exchange argument).
- The answer is always one of the bloom days (the day a flower opens), and the search lands on one.

**Complexity:** O(n) per check, about `log2(max - min)` checks (up to about 30 for 10^9), so O(n log(max)) time, O(1) extra space. `m * k` can reach 10^10 but Python ints have no overflow (fixed-width languages need a 64-bit product).

**Dry run:** `[7,7,7,7,12,7,7]`, m = 2, k = 3, range `[7, 12]`
| lo | hi | mid | bouquets at day mid | >= 2? | next |
|---|---|---|---|---|---|
| 7 | 12 | 9 | 7s open: positions 0-2 make 1 bouquet; position 4 (12) is closed; positions 5-6 are only 2 flowers. Total 1 | no | lo = 10 |
| 10 | 12 | 11 | same as day 9: 1 | no | lo = 12 |
Stop at `lo = hi = 12`. At day 12 everything is open: positions 0-2 and 3-5 make 2 bouquets, position 6 is left over. Answer 12.

**Code:**
```python
import random


def bouquets_at(bloom, k, day):
    cnt = run = 0
    for b in bloom:
        if b <= day:
            run += 1
            if run == k:
                cnt += 1
                run = 0              # flowers are used once: start a fresh run
        else:
            run = 0                  # an unbloomed flower breaks adjacency
    return cnt


def min_days_bs(bloom, m, k):
    if len(bloom) < m * k:
        return -1
    lo, hi = min(bloom), max(bloom)      # at hi every flower is open, so hi is feasible
    while lo < hi:
        mid = (lo + hi) // 2
        if bouquets_at(bloom, k, mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


def min_days_brute(bloom, m, k):
    if len(bloom) < m * k:
        return -1
    for day in sorted(set(bloom)):       # try each candidate day ascending
        if bouquets_at(bloom, k, day) >= m:
            return day


def min_days_independent(bloom, m, k):
    """Different brute force: choose bouquets from windows by recursion (no greedy)."""
    n = len(bloom)
    best = [None]

    def go(i, made, cur_max):
        if made == m:
            best[0] = cur_max if best[0] is None else min(best[0], cur_max)
            return
        if i + k > n:
            return
        go(i + 1, made, cur_max)                                     # skip flower i
        go(i + k, made + 1, max(cur_max, max(bloom[i:i + k])))       # take window i..i+k-1
    go(0, 0, 0)
    return -1 if best[0] is None else best[0]


examples = [([1, 10, 3, 10, 2], 3, 1, 3), ([1, 10, 3, 10, 2], 3, 2, -1),
            ([7, 7, 7, 7, 12, 7, 7], 2, 3, 12), ([1, 10, 2, 9, 3, 8, 4, 7, 5, 6], 4, 2, 9)]
for bloom, m, k, exp in examples:
    got = min_days_bs(bloom, m, k)
    assert got == min_days_brute(bloom, m, k) == min_days_independent(bloom, m, k) == exp
    print(bloom, "m =", m, "k =", k, "->", got)

random.seed(19)
for _ in range(1500):
    n = random.randint(1, 9)
    bloom = [random.randint(1, 8) for _ in range(n)]
    m, k = random.randint(1, 4), random.randint(1, 4)
    a, b, c = min_days_bs(bloom, m, k), min_days_brute(bloom, m, k), min_days_independent(bloom, m, k)
    assert a == b == c, (bloom, m, k, a, b, c)
print("cross-check: 1500 seeded cases agree (binary search, scan of days, recursive window brute force)")

# monotonic in the day: more days never makes fewer bouquets
for _ in range(200):
    bloom = [random.randint(1, 20) for _ in range(random.randint(1, 15))]
    k = random.randint(1, 3)
    counts = [bouquets_at(bloom, k, d) for d in range(0, 22)]
    assert counts == sorted(counts)
print("monotone check: bouquet count never drops as the day grows (200 seeded lists)")

# edge cases
assert min_days_bs([5], 1, 1) == 5
assert min_days_bs([5], 2, 1) == -1
assert min_days_bs([3, 3, 3], 1, 3) == 3
assert min_days_bs([1, 2, 3], 1, 4) == -1
assert min_days_bs([10**9] * 6, 3, 2) == 10**9
big = [random.randint(1, 10**9) for _ in range(10**5)]
assert min_days_bs(big, 10**5, 1) == max(big)        # every flower needed
assert len(big) < 10**4 * 11 and min_days_bs(big, 10**4 + 1, 10) == -1
print("edge asserts passed")
```

**Output (my run):**
```text
[1, 10, 3, 10, 2] m = 3 k = 1 -> 3
[1, 10, 3, 10, 2] m = 3 k = 2 -> -1
[7, 7, 7, 7, 12, 7, 7] m = 2 k = 3 -> 12
[1, 10, 2, 9, 3, 8, 4, 7, 5, 6] m = 4 k = 2 -> 9
cross-check: 1500 seeded cases agree (binary search, scan of days, recursive window brute force)
monotone check: bouquet count never drops as the day grows (200 seeded lists)
edge asserts passed
```

**Edge cases:**
- `len < m * k`: return -1 before searching (second example: 5 flowers, need 6).
- `k = 1`: any m flowers; the answer is the m-th smallest bloom day.
- `m * k == len`: every flower needed, answer is `max(bloom)` (checked at size 10^5).
- All same day.
- Large day values up to 10^9: about 30 iterations.

**Follow-ups:**
- *Binary search over sorted distinct days instead?* Same result, slightly fewer checks but costs a sort.
- *Why reset `run = 0` after a bouquet?* A flower is used at most once.
- *Non-adjacent flowers allowed?* Then it is just the m*k-th smallest day.

**Common mistakes:**
- Not resetting the run after making a bouquet (reusing flowers).
- Not resetting it on an unbloomed flower.
- Forgetting the `m * k > n` check, returning `max(bloom)` for an impossible case.
- Using `count == m` instead of `count >= m`.

### Q20 ⭐⭐ 🟡 Aggressive cows (maximise the minimum distance). `stalls` is a list of distinct integer positions in arbitrary order (2 <= len <= 10^5, positions up to 10^9) and c is the number of cows (2 <= c <= len). Place all c cows in distinct stalls so that the smallest distance between any two cows is as large as possible and return that distance. Sort, then binary search the distance d with the greedy predicate 'place a cow, then the next stall at least d further'. Show the 'last True' template (upper-biased mid) and explain why this predicate is monotone in the opposite direction from Koko eating bananas. Example: [1,2,4,8,9], c=3 -> 3; [1,2,3,4,7], c=3 -> 3; [5,4,3,2,1,1000000000], c=2 -> 999999999; [1,2], c=2 -> 1.
**Asked at:** Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search on the answer, "maximise the minimum" version. Greedy check: can we place all cows with every gap at least d? Larger d is harder, so the predicate is True...True False...False and we want the last True.

**Say this first (1 line):** "Sort, then binary search the distance d; to test d, put a cow in the first stall and every next cow in the first stall at least d away, and if I place all c cows d works. I want the largest working d."

**Brute force:** Try every way to choose c stalls out of n and take the best minimum gap. O(C(n, c) * c). Fine for tiny inputs (the code's reference), impossible for 10^5.

**Optimal:**
- Sort the positions. Search `lo = 1` (always feasible: positions are distinct integers) to `hi = (max - min) // (c - 1)` (c cows have c - 1 gaps, so the smallest gap cannot exceed the average).
- `can_place(d)`: first cow at `s[0]`, then scan: whenever `x - last >= d`, place a cow there. Greedy leftmost placement is optimal: placing earlier leaves the most room.
- **Last-True template:** `while lo < hi`, `mid = (lo + hi + 1) // 2` (upper-biased). If `can_place(mid)`: `lo = mid`. Else `hi = mid - 1`.
- **Why upper-biased mid:** with `lo = mid`, a lower-biased `mid = (lo + hi) // 2` equals `lo` when `hi = lo + 1`; then `lo = mid` changes nothing and the loop never ends. The code runs this on `[1,2,3,4,9]`, c = 2 and shows it stuck (capped at 50 turns).
- **Opposite direction from Koko:** in Koko eating bananas a faster speed k is easier, so the predicate is False...True and we want the first True (`hi = mid`, lower-biased mid). Here a bigger d is harder, so True...False and we want the last True (`lo = mid`, upper-biased mid). I checked this shape on 200 seeded cases.
- Invariant: `can_place(lo)` is True (starts at d = 1), and the answer is `<= hi`.

**Complexity:** Sort O(n log n), then about `log2(10^9)` = 30 checks of O(n) each: O(n log n + n log(max - min)). O(1) extra space besides the sort.

**Dry run:** `[1,2,4,8,9]`, c = 3, `lo = 1`, `hi = 8 // 2 = 4`
| lo | hi | mid | placement for d = mid | placed | next |
|---|---|---|---|---|---|
| 1 | 4 | 3 | 1, then 4 (gap 3), then 8 | 3 | lo = 3 |
| 3 | 4 | 4 | 1, then 8 (gap 7), then none (9-8 = 1) | 2 | hi = 3 |
Stop at 3.

**Code:**
```python
import itertools
import random


def can_place(s, c, d):
    """Greedy on sorted stalls: put a cow at the first stall, then next stall >= d further."""
    placed, last = 1, s[0]
    for x in s[1:]:
        if x - last >= d:
            placed += 1
            last = x
            if placed == c:
                return True
    return placed >= c


def aggressive_cows(stalls, c):
    s = sorted(stalls)
    lo, hi = 1, (s[-1] - s[0]) // (c - 1)    # d=1 always works (distinct ints); d can't exceed span/(c-1)
    while lo < hi:
        mid = (lo + hi + 1) // 2              # upper-biased mid: lo = mid must make progress
        if can_place(s, c, mid):
            lo = mid                          # mid works: answer is mid or bigger
        else:
            hi = mid - 1
    return lo


def cows_brute(stalls, c):
    s = sorted(stalls)
    return max(min(b - a for a, b in zip(sub, sub[1:])) for sub in itertools.combinations(s, c))


def stuck_with_lower_mid(stalls, c, cap=50):
    """Shows why (lo+hi)//2 fails with lo = mid: counts loop turns, gives up at cap."""
    s = sorted(stalls)
    lo, hi, turns = 1, (s[-1] - s[0]) // (c - 1), 0
    while lo < hi and turns < cap:
        mid = (lo + hi) // 2
        if can_place(s, c, mid):
            lo = mid
        else:
            hi = mid - 1
        turns += 1
    return turns >= cap


examples = [([1, 2, 4, 8, 9], 3, 3), ([1, 2, 3, 4, 7], 3, 3),
            ([5, 4, 3, 2, 1, 10**9], 2, 10**9 - 1), ([1, 2], 2, 1)]
for stalls, c, exp in examples:
    got = aggressive_cows(stalls, c)
    assert got == exp == cows_brute(stalls, c)
    print(stalls, "c =", c, "->", got)

random.seed(20)
for _ in range(1500):
    n = random.randint(2, 9)
    stalls = random.sample(range(0, 30), n)
    c = random.randint(2, n)
    assert aggressive_cows(stalls, c) == cows_brute(stalls, c), (stalls, c)
print("cross-check: 1500 seeded cases agree with the brute force over all subsets")

# predicate shape: True...True False...False (opposite of Koko's False...True)
for _ in range(200):
    s = sorted(random.sample(range(0, 60), random.randint(2, 10)))
    c = random.randint(2, len(s))
    row = [can_place(s, c, d) for d in range(1, 62)]
    assert row == sorted(row, reverse=True)
print("monotone check: can_place(d) is True then False in d (200 seeded cases)")

print("lower mid + lo = mid never finishes on [1,2,3,4,9], c=2:", stuck_with_lower_mid([1, 2, 3, 4, 9], 2))
assert stuck_with_lower_mid([1, 2, 3, 4, 9], 2) is True
assert aggressive_cows([1, 2, 3, 4, 9], 2) == 8

# edge cases
assert aggressive_cows([1, 2], 2) == 1
assert aggressive_cows([1, 2, 3, 4, 5], 5) == 1          # c == n: all stalls used
assert aggressive_cows([1, 10**9], 2) == 10**9 - 1
assert aggressive_cows([0, 5, 10], 3) == 5
big = random.sample(range(0, 10**9), 10**5)
assert aggressive_cows(big, 2) == max(big) - min(big)
assert aggressive_cows(list(range(0, 10**5)), 10**5) == 1
print("edge asserts passed")
```

**Output (my run):**
```text
[1, 2, 4, 8, 9] c = 3 -> 3
[1, 2, 3, 4, 7] c = 3 -> 3
[5, 4, 3, 2, 1, 1000000000] c = 2 -> 999999999
[1, 2] c = 2 -> 1
cross-check: 1500 seeded cases agree with the brute force over all subsets
monotone check: can_place(d) is True then False in d (200 seeded cases)
lower mid + lo = mid never finishes on [1,2,3,4,9], c=2: True
edge asserts passed
```

**Edge cases:**
- `c = 2`: answer is `max - min` (checked at 10^5 stalls).
- `c = n`: every stall used, answer is the smallest adjacent gap (1 for consecutive positions).
- Unsorted input: sort first (`[5,4,3,2,1,10**9]` gives 999999999).
- Two stalls only (`[1,2]`, c = 2): `hi = lo = 1`, no loop.
- Positions up to 10^9: differences fit in Python ints; no overflow issue.

**Follow-ups:**
- *Same pattern?* Yes: any "maximise the minimum" problem (e.g. magnetic force between balls).
- *How do you recover the placement?* Re-run the greedy at the final d and record the stalls.
- *Why is greedy leftmost right?* An exchange argument: moving any cow later never helps the cows after it.

**Common mistakes:**
- Forgetting to sort.
- Lower-biased mid with `lo = mid`: infinite loop.
- Starting `lo` at 0 (gap 0 is meaningless; distances start at 1).
- Using the first-True template (`hi = mid`) on a True...False predicate and returning the smallest d.
- Off by one: counting `>= d` versus `> d`.

### Q21 ⭐⭐ 🟡 Allocate books (minimise the maximum pages). `pages[i]` is the page count of book i, in shelf order (1 <= len <= 10^5; the list is NOT sorted); m students each get a contiguous, non-empty block of books and every book is assigned. Return the smallest possible value of the largest page total any student receives, or -1 if m > len(pages). Binary search between max(pages) and sum(pages). Explain the -1 case, why the answer is always an actual sum of some contiguous block, and how this prompt differs from the split-array question only in the infeasible-input guard. Example: [12,34,67,90], m=2 -> 113; [25,46,28,49,24], m=4 -> 71; [10,20], m=3 -> -1; [10,20], m=2 -> 20; [5,5,5,5], m=1 -> 20.
**Asked at:** Candidate-reported Indian product-company online rounds (a Naukri Code360 Flipkart 2021 entry naming Allocate Books and a Flipkart entry naming rotated sorted array search; one aggregator, 2015-2022 reports, snippets only, not opened; candidate-reported, unverified, not evidence of current practice) | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search on the answer, "minimise the maximum". The answer is a number in [max(pages), sum(pages)]. A greedy feasibility check ("can m students cope if nobody reads more than S pages?") is monotone in S. So I search S, not the array.

**Say this first (1 line):** "If m is more than the number of books return -1; otherwise binary search the smallest cap S in [max, sum] for which a greedy left-to-right split needs at most m students."

**Brute force:** DP over prefixes: `dp[j][i]` is the best largest load when the first `i` books go to `j` students. Try every last cut. O(m * n^2) time, O(m * n) space. Fine as a checker, hopeless at n = 10^5.

**Optimal:**
- Floor: `max(pages)`. One book cannot be split, so some student holds at least the biggest book.
- Ceiling: `sum(pages)`. One student takes everything.
- Predicate `ok(S)`: walk the books, start a new student when the next book would push the load over S. Return `students <= m`.
- Monotone: if S works, S + 1 works (same split is still legal). So the sequence is False...False True...True. Find the first True with `lo < hi`, `hi = mid`.
- Invariant: the answer is always in [lo, hi], and `hi` is feasible.
- The -1 case: every student needs a non-empty block, so m > n is impossible. Without the guard the greedy would happily say "fits" using fewer students, which is not what the prompt asks. Check it before searching.
- Why the answer is a block sum: let S* be the smallest feasible cap. The greedy split under S* has some largest block with sum M <= S*. That same split is feasible for cap M, so M is feasible too. Minimality forces M = S*. So S* is the sum of a real contiguous block.
- Versus split-array (Q13): same binary search, same predicate. Only difference is that this prompt has to say -1 for m > n; split-array promised k <= n.
- "At most m" vs "exactly m": if greedy uses fewer than m students and m <= n, split a block further. Splitting never raises the maximum, and there are enough books to give everyone one. So both give the same answer.

**Complexity:** Time O(n log(sum)): each `ok` is one O(n) pass; the range has at most sum(pages) values, so about log2(sum) rounds. With n = 10^5 and, for example, pages up to 10^4, sum <= 10^9, so about 30 rounds. Space O(1).

**Dry run:** `[12, 34, 67, 90]`, m = 2. Range [90, 203].
| lo | hi | mid | students at cap mid | action |
|---|---|---|---|---|
| 90 | 203 | 146 | 12+34+67=113, +90 > 146 so new: 2 students | ok, hi = 146 |
| 90 | 146 | 118 | 113, then 90: 2 students | ok, hi = 118 |
| 90 | 118 | 104 | 12+34=46, +67=113 > 104 so new, 67 then +90 > 104 so new: 3 | no, lo = 105 |
| 105 | 118 | 111 | 3 students (113 > 111) | no, lo = 112 |
| 112 | 118 | 115 | 113 then 90: 2 | ok, hi = 115 |
| 112 | 115 | 113 | 113 then 90: 2 | ok, hi = 113 |
| 112 | 113 | 112 | 3 | no, lo = 113 |
Answer 113 = 12 + 34 + 67, a real block sum.

**Code:**
```python
import random
from itertools import accumulate


def allocate_brute(pages, m):
    # DP: dp[j][i] = best max-load splitting the first i books into j blocks. O(m * n^2).
    n = len(pages)
    if m > n:
        return -1
    pre = [0] + list(accumulate(pages))
    INF = float("inf")
    dp = [[INF] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    for j in range(1, m + 1):
        for i in range(j, n + 1):
            for p in range(j - 1, i):
                dp[j][i] = min(dp[j][i], max(dp[j - 1][p], pre[i] - pre[p]))
    return dp[m][n]


def students_needed(pages, cap):
    # greedy: fill the current student until the next book would overflow
    used, load = 1, 0
    for p in pages:
        if load + p > cap:
            used += 1
            load = 0
        load += p
    return used


def allocate_books(pages, m):
    if m > len(pages):                      # not enough books for one each: infeasible
        return -1
    lo, hi = max(pages), sum(pages)         # answer is in [max, sum]; hi is feasible (1 student)
    while lo < hi:                          # first True of: students_needed(cap) <= m
        mid = (lo + hi) // 2
        if students_needed(pages, mid) <= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


examples = [([12, 34, 67, 90], 2, 113), ([25, 46, 28, 49, 24], 4, 71),
            ([10, 20], 3, -1), ([10, 20], 2, 20), ([5, 5, 5, 5], 1, 20)]
for pages, m, want in examples:
    assert allocate_books(pages, m) == allocate_brute(pages, m) == want, (pages, m)
    print(pages, "m =", m, "->", allocate_books(pages, m))

# the answer is always the sum of some contiguous block (checked on every random case below)
rng = random.Random(21)
cnt = 0
for _ in range(1500):
    n = rng.randint(1, 9)
    pages = [rng.randint(1, 12) for _ in range(n)]
    m = rng.randint(1, n + 2)               # includes the infeasible m > n
    got, want = allocate_books(pages, m), allocate_brute(pages, m)
    assert got == want, (pages, m, got, want)
    if got != -1:
        sums = {sum(pages[i:j]) for i in range(n) for j in range(i + 1, n + 1)}
        assert got in sums, (pages, m, got)
        cnt += 1
print("random check passed: 1500 cases, feasible ones:", cnt, "(answer was a block sum every time)")

# edge cases
assert allocate_books([7], 1) == 7
assert allocate_books([7], 2) == -1
assert allocate_books([3, 3, 3], 3) == 3            # m == n: answer is max(pages)
assert allocate_books([1, 1, 1, 100], 2) == 100     # one huge book sets the floor
assert allocate_books([10 ** 4] * 10 ** 5, 10 ** 5) == 10 ** 4
assert allocate_books([10 ** 4] * 10 ** 5, 1) == 10 ** 9
print("edge asserts passed")
```

**Output (my run):**
```
[12, 34, 67, 90] m = 2 -> 113
[25, 46, 28, 49, 24] m = 4 -> 71
[10, 20] m = 3 -> -1
[10, 20] m = 2 -> 20
[5, 5, 5, 5] m = 1 -> 20
random check passed: 1500 cases, feasible ones: 1002 (answer was a block sum every time)
edge asserts passed
```
All five examples in the prompt are correct. The random check also asserts the "answer is a block sum" claim on every feasible case.

**Edge cases:**
- m > n: -1 (checked first).
- m = n: every student gets one book, answer is `max(pages)`.
- m = 1: answer is `sum(pages)`.
- One huge book: it sets the floor, extra students cannot reduce it.
- n = 10^5: about 30 passes of 10^5 steps; the edge asserts run n = 10^5 with 10^4-page books (sum 10^9).

**Follow-ups:**
- *Painter's partition?* Same code with "boards" and "painters". Time per unit just multiplies the sum.
- *Return the actual split?* Run the greedy once more with the final cap and record cut points.
- *Why not search in the array of books?* The array is unsorted and the answer is not an index; only the answer space is ordered.

**Common mistakes:**
- Floor of 1 or 0 instead of `max(pages)`: the predicate breaks because a book bigger than S can never fit and the greedy loops over-count silently.
- Forgetting the m > n guard.
- Using `mid = (lo + hi) // 2` with `lo = mid` (infinite loop). Here the update is `hi = mid` and `lo = mid + 1`, so the floor mid is correct.
- Resetting `load = p` incorrectly (off by one) when starting a new student.

### Q22 ⭐⭐ 🟡 Search a 2D matrix with sorted rows and sorted columns. `matrix` is m x n (1 <= m, n <= 300); each row is sorted ascending left to right and each column is sorted ascending top to bottom, but there is NO relation between the end of one row and the start of the next. Return True if `target` is present. Implement the O(m + n) staircase walk from the top-right corner, and the O(m log n) version that binary-searches each row, and explain why flattening plus one binary search is invalid here and which version wins when m is much smaller than n. Example: [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target=5 -> True; the same matrix with target=20 -> False; [[-5]], -5 -> True.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Search a matrix with partial order. Rows and columns are sorted, but rows do not chain. Use the staircase (eliminate a row or column per step), or binary search per row.

**Say this first (1 line):** "Start at the top-right: if the value is too big drop the column, if too small drop the row; that is O(m + n). Flattening is invalid because the flattened list is not sorted."

**Brute force:** Scan every cell, O(m * n). Used as the checker.

**Optimal:** Staircase walk from the top-right (row 0, last column).
- `v == target`: found.
- `v > target`: everything below `v` in its column is at least `v`, so too big. Drop the column (`c -= 1`).
- `v < target`: everything to the left of `v` in its row is at most `v`, so too small. Drop the row (`r += 1`).
- Invariant: if the target exists, it lies in the sub-rectangle rows `r..m-1`, columns `0..c`. Each step removes a row or a column, so at most m + n steps.
- Bottom-left works the same way (mirror). Top-left or bottom-right do not: both neighbours are bigger (or both smaller), so you cannot decide.
- Per-row binary search: `bisect_left` on each row, O(m log n).
- Which wins? Per-row bisect is better when m is much smaller than n (m = 1 gives log n versus n). The staircase is better when m is close to n (m = n gives 2n versus n log n). Best of both: loop over the shorter side and bisect the longer: O(min(m, n) * log(max(m, n))).
- Why flatten + bisect fails: row 0 ends at 15 but row 1 starts at 2, so the flattened list is not sorted. Binary search on it can miss a present value. The code shows it missing the 5 that is in the matrix.

**Complexity:** Staircase: time O(m + n), space O(1). Per-row: time O(m log n), space O(1). Both beat O(m n).

**Dry run:** target 5 in the example matrix. Start (0,4) = 15 > 5, column 4 out. (0,3) = 11 > 5, out. (0,2) = 7 > 5, out. (0,1) = 4 < 5, row 0 out. (1,1) = 5, found. Five steps.

**Code:**
```python
import random
from bisect import bisect_left


def search_brute(mat, t):
    return any(t in row for row in mat)


def search_staircase(mat, t, counter=None):
    # start top-right: left is smaller, down is larger. O(m + n)
    m, n = len(mat), len(mat[0])
    r, c = 0, n - 1
    while r < m and c >= 0:
        if counter is not None:
            counter[0] += 1
        v = mat[r][c]
        if v == t:
            return True
        if v > t:
            c -= 1          # everything below v in this column is bigger: drop the column
        else:
            r += 1          # everything left of v in this row is smaller: drop the row
    return False


def search_rows(mat, t, counter=None):
    # binary search every row. O(m log n)
    for row in mat:
        i = bisect_left(row, t)
        if counter is not None:
            counter[0] += max(1, len(row).bit_length())
        if i < len(row) and row[i] == t:
            return True
    return False


def search_short_side(mat, t):
    # binary search along the longer side, loop over the shorter one: O(min(m,n) * log(max(m,n)))
    m, n = len(mat), len(mat[0])
    if m <= n:
        return search_rows(mat, t)
    cols = [[mat[r][c] for r in range(m)] for c in range(n)]   # transpose (O(mn), only for the demo)
    return search_rows(cols, t)


M = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
for mat, t, want in [(M, 5, True), (M, 20, False), ([[-5]], -5, True)]:
    assert search_staircase(mat, t) == search_rows(mat, t) == search_brute(mat, t) == want
    print("target", t, "->", search_staircase(mat, t))

# why flattening is invalid: the flattened list is not sorted, so bisect on it can miss present values
flat = [v for row in M for v in row]
i = bisect_left(flat, 5)
print("flattened sorted?", flat == sorted(flat), "| bisect on flat finds 5?", i < len(flat) and flat[i] == 5)
assert flat != sorted(flat) and not (i < len(flat) and flat[i] == 5)   # 5 is in M, flatten+bisect says no

# comparison counts (worst over all targets) when m is much smaller than n (1 x 300) and when square (300 x 300)
for m, n in [(1, 300), (300, 300)]:
    mat = [[r * 1000 + c for c in range(n)] for r in range(m)]     # rows and columns both ascending
    worst_a = worst_b = 0
    for t in [-1] + [r * 1000 for r in range(m)] + [r * 1000 + n - 1 for r in range(m)]:
        a, b = [0], [0]
        search_staircase(mat, t, a)
        search_rows(mat, t, b)
        worst_a, worst_b = max(worst_a, a[0]), max(worst_b, b[0])
    print(f"{m} x {n}: staircase max steps over probe targets = {worst_a} (<= m+n-1 = {m + n - 1}), "
          f"row-bisect worst steps ~ {worst_b} (m * bit_length(n))")

# random cross-check: build a valid matrix by sorting rows, then sorting each column
rng = random.Random(22)
for _ in range(1500):
    m, n = rng.randint(1, 6), rng.randint(1, 6)
    mat = [sorted(rng.randint(-8, 20) for _ in range(n)) for _ in range(m)]
    cols = [sorted(mat[r][c] for r in range(m)) for c in range(n)]
    mat = [[cols[c][r] for c in range(n)] for r in range(m)]
    assert all(mat[r][c] <= mat[r][c + 1] for r in range(m) for c in range(n - 1))
    assert all(mat[r][c] <= mat[r + 1][c] for r in range(m - 1) for c in range(n))
    for t in range(-10, 23):
        w = search_brute(mat, t)
        assert search_staircase(mat, t) == search_rows(mat, t) == search_short_side(mat, t) == w, (mat, t)
print("random check passed: 1500 matrices x 33 targets")

# edge cases
assert search_staircase([[1, 2, 3]], 3) and not search_staircase([[1, 2, 3]], 4)
assert search_staircase([[1], [2], [3]], 1) and not search_staircase([[1], [2], [3]], 0)
assert search_staircase([[2, 2], [2, 2]], 2) and not search_staircase([[2, 2], [2, 2]], 3)
print("edge asserts passed")
```

**Output (my run):**
```
target 5 -> True
target 20 -> False
target -5 -> True
flattened sorted? False | bisect on flat finds 5? False
1 x 300: staircase max steps over probe targets = 300 (<= m+n-1 = 300), row-bisect worst steps ~ 9 (m * bit_length(n))
300 x 300: staircase max steps over probe targets = 599 (<= m+n-1 = 599), row-bisect worst steps ~ 2700 (m * bit_length(n))
random check passed: 1500 matrices x 33 targets
edge asserts passed
```
The three examples in the prompt are correct. The step counts are the worst I probed on the specific matrices shown, not a proof; the bounds come from the reasoning above.

**Edge cases:**
- 1 x n or m x 1: the staircase degenerates to a linear scan; per-row (or per-column) bisect is the better tool.
- Duplicates (all equal): the walk still works, it stops at the first hit.
- Target smaller than the top-left or bigger than the bottom-right: the walk falls off the edge, False.
- Negative values: nothing changes.

**Follow-ups:**
- *Count how many entries are <= v?* The same staircase from the bottom-left, adding a whole column segment per step. See Q26.
- *Can you beat O(m + n)?* Yes when the shape is lopsided: the combined form O(min(m,n) * log(max(m,n))) shown in the code. For a roughly square matrix the staircase is the standard answer.
- *Binary search the shorter side?* Yes, that is the combined form shown in the code.

**Common mistakes:**
- Treating it like Q10 (flattening). The chain condition is missing here.
- Starting at the top-left: both moves (right and down) increase the value, so you cannot decide.
- Mixing up which pointer moves: too big means drop the column, too small means drop the row.

### Q23 ⭐⭐ 🟡 Search in a mountain array with a call budget. A hidden array `A` (3 <= len <= 10^4) strictly increases up to a peak and then strictly decreases. You can only call `get(i)` and read `length()`, and you may call `get` at most 100 times. Return the smallest index whose value equals `target`, or -1. Find the peak by comparing get(mid) and get(mid+1), then binary search the increasing side first and only if that fails the decreasing side (with the comparison direction reversed). Explain why searching the left side first gives the smallest index, and why about 3 * ceil(log2 n) calls fit in the budget. Example: A=[1,2,3,4,5,3,1], target=3 -> 2; A=[0,1,2,4,2,1], target=3 -> -1; A=[1,5,2], target=2 -> 2; A=[1,5,2], target=5 -> 1. (See Part 2 Q38 for the same shape solved by one pass, without a budget.)
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Three binary searches under a call budget: find the peak, then an ascending search, then a descending search. Left side first.

**Say this first (1 line):** "Peak by comparing get(mid) with get(mid+1), then binary search the left slope including the peak, and only if that misses, the right slope with the comparison flipped; the left-first order gives the smallest index."

**Brute force:** Read every element (up to 10^4 calls) and return the first match. It breaks the 100-call budget, so it is only the checker (it works on the plain list, outside the budget).

**Optimal:**
1. Find the peak: `lo, hi = 0, n - 1`. If `get(mid) < get(mid + 1)` we are still climbing: `lo = mid + 1`. Otherwise `hi = mid`. Ends with `lo == hi` at the peak. Two `get` calls per round.
2. Search `[0, peak]` for the target, normal ascending binary search.
3. If not found, search `[peak + 1, n - 1]` with the comparison reversed: too small means go left (values get bigger towards the left), too big means go right.
- Why left first: every index on the left slope is smaller than every index on the right slope. A value that appears on both slopes (like 2 in `[1, 5, 2, ...]`) must be reported at its left position. On each slope values are distinct, so a slope has at most one match.
- The peak belongs to the left search (it is the last element of the increasing part). Searching only up to `peak - 1` would miss a target equal to the peak.
- Budget: n <= 10^4 gives ceil(log2 n) = 14. The peak search costs 2 gets per round, so about 28; each slope search is at most about 14. Total about 4 * 14 = 56 in the worst case. The prompt's "about 3 * ceil(log2 n)" counts the peak search as one call per round; with two calls per round (as coded, no caching) the honest worst case is about 4 * ceil(log2 n). Either way it is well under 100. You could cache `get` results to save calls.
- The budget rules out the linear scan, and it also rules out sloppy variants such as searching both slopes blindly.

**Complexity:** Time O(log n) `get` calls: measured worst 54 in my runs (budget 100). Space O(1).

**Dry run:** `A = [1, 2, 3, 4, 5, 3, 1]`, target 3. Peak: lo=0, hi=6, mid=3: 4 < 5, lo=4; mid=5: 3 < 1? No, hi=5; mid=4: 5 < 3? No, hi=4. Peak index 4. Left search on [0, 4]: mid=2, value 3, found at 2. The right slope is never touched. Answer 2 (the other 3 sits at index 5).

**Code:**
```python
import random
from itertools import product

BUDGET = 100


class Mountain:
    # hidden array with a call counter; get() refuses to go past the budget
    def __init__(self, a):
        self._a, self.calls = a, 0

    def length(self):                       # length() is free in the prompt (not counted)
        return len(self._a)

    def get(self, i):
        self.calls += 1
        assert self.calls <= BUDGET, "call budget exceeded"
        return self._a[i]


def find_peak(m):
    lo, hi = 0, m.length() - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if m.get(mid) < m.get(mid + 1):
            lo = mid + 1                    # still climbing: peak is to the right
        else:
            hi = mid                        # descending (or at peak): peak is at mid or left
    return lo


def bs_side(m, lo, hi, target, ascending):
    while lo <= hi:
        mid = (lo + hi) // 2
        v = m.get(mid)
        if v == target:
            return mid
        if (v < target) == ascending:       # ascending: too small -> go right; descending: too small -> go left
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def search_mountain(m, target):
    p = find_peak(m)
    i = bs_side(m, 0, p, target, True)      # left side (including the peak) first: smaller indices
    if i != -1:
        return i
    return bs_side(m, p + 1, m.length() - 1, target, False)


def search_brute(a, target):
    return a.index(target) if target in a else -1


def run(a, t):
    m = Mountain(a)
    return search_mountain(m, t), m.calls


for a, t, want in [([1, 2, 3, 4, 5, 3, 1], 3, 2), ([0, 1, 2, 4, 2, 1], 3, -1), ([1, 5, 2], 2, 2), ([1, 5, 2], 5, 1)]:
    got, calls = run(a, t)
    assert got == search_brute(a, t) == want, (a, t)
    print(a, "target", t, "->", got, "| get calls:", calls)

# exhaustive: every mountain of length 3..7 with values 0..6, every target -1..7
count, worst = 0, 0
for n in range(3, 8):
    for a in product(range(7), repeat=n):
        a = list(a)
        p = a.index(max(a))
        if not (all(a[i] < a[i + 1] for i in range(p)) and all(a[i] > a[i + 1] for i in range(p, n - 1)) and 0 < p < n - 1):
            continue
        for t in range(-1, 8):
            got, calls = run(a, t)
            assert got == search_brute(a, t), (a, t, got)
            worst = max(worst, calls)
            count += 1
print("exhaustive check passed:", count, "(array, target) pairs; worst calls at n<=7:", worst)

# random big mountains, n up to 10^4, counting calls
rng = random.Random(23)
worst_calls, worst_n = 0, 0
for _ in range(3000):
    n = rng.choice([3, 4, 5, 100, 1000, 9999, 10000, rng.randint(3, 10000)])
    p = rng.randint(1, n - 2)
    left = sorted(rng.sample(range(0, 40000), p))
    right = sorted(rng.sample(range(0, 40000), n - p - 1), reverse=True)
    a = left + [40000] + right              # strictly up to index p, strictly down after
    for t in [rng.choice(a), rng.choice(a), rng.randint(-1, 40001), a[0], a[-1], max(a)]:
        got, calls = run(a, t)
        assert got == search_brute(a, t), (n, t)
        if calls > worst_calls:
            worst_calls, worst_n = calls, n
print("random check passed; worst calls seen:", worst_calls, "at n =", worst_n, "(budget 100)")

# worst-case probe at n = 10^4 for EVERY peak position, target absent on both sides
n = 10 ** 4
w = 0
for p in range(1, n - 1):
    a = list(range(0, 2 * p, 2)) + [2 * p] + list(range(2 * p - 1, 2 * p - 1 - 2 * (n - p - 1), -2))
    for t in (-1, 1, 2 * p + 1):
        w = max(w, run(a, t)[1])
print("worst calls over all 9998 peak positions at n = 10^4, 3 absent targets each:", w)
assert w <= BUDGET
k = (n - 1).bit_length()
print("ceil(log2(10^4)) =", k, "| peak step: 2 gets per round ~", 2 * k, "| one side search ~", k, "| both sides ~", 2 * k, "| total ~", 4 * k)
```

**Output (my run):**
```
[1, 2, 3, 4, 5, 3, 1] target 3 -> 2 | get calls: 7
[0, 1, 2, 4, 2, 1] target 3 -> -1 | get calls: 10
[1, 5, 2] target 2 -> 2 | get calls: 7
[1, 5, 2] target 5 -> 1 | get calls: 6
exhaustive check passed: 30987 (array, target) pairs; worst calls at n<=7: 11
random check passed; worst calls seen: 54 at n = 9999 (budget 100)
worst calls over all 9998 peak positions at n = 10^4, 3 absent targets each: 53
ceil(log2(10^4)) = 14 | peak step: 2 gets per round ~ 28 | one side search ~ 14 | both sides ~ 28 | total ~ 56
```
All four examples in the prompt are correct. The exhaustive run covers every mountain of length 3 to 7 over values 0..6 and every target -1..7. The call counter raises if the budget of 100 is ever exceeded; it never was. The "about 3 * ceil(log2 n)" phrasing in the prompt is loose: the measured worst (53 to 54) is closer to 4 * ceil(log2 n) = 56 for the two-calls-per-round peak search.

**Edge cases:**
- Peak at index 1 or n - 2 (minimum length 3 is allowed).
- Target equals the peak value: found by the left search.
- Target on both slopes: left index wins.
- Absent target: both slopes searched, still within budget (worst case).
- Strictness is essential: no plateaus, so `get(mid) < get(mid + 1)` always decides.

**Follow-ups:**
- *Reduce the calls?* Cache `get` in a dict, or find the peak by comparing only `get(mid)` with a remembered neighbour.
- *No budget?* One pass or `list.index` (Part 2 Q38 is the same shape without a budget).
- *Why not a combined search?* Without the peak you cannot tell which slope mid is on.

**Common mistakes:**
- Searching the right slope first (wrong index when the value appears on both).
- Reusing the ascending comparison on the descending slope.
- Excluding the peak from the left search.
- Counting only calls in the binary searches and forgetting the peak step's two gets per round.

### Q24 ⭐⭐ 🟡 Find k closest elements. `arr` is sorted ascending (1 <= len <= 10^4, duplicates allowed), 1 <= k <= len(arr), and x is an integer. Return the k elements closest to x, sorted ascending; when two elements are equally close, the smaller value is preferred. The answer is a window of k consecutive elements, so binary search its left edge in [0, n - k] by comparing x - arr[mid] with arr[mid + k] - x (the answer list is uniquely determined by these rules: equal-distance ties favour the smaller value, and equal values are interchangeable). Example: [1,2,3,4,5], k=4, x=3 -> [1,2,3,4]; [1,2,3,4,5], k=4, x=-1 -> [1,2,3,4]; [1,3], k=1, x=2 -> [1]; [1,1,2,3,4,5], k=3, x=4 -> [3,4,5]; [1,2,3,4,5], k=2, x=10 -> [4,5].
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search on the left edge of a fixed-size window. The k closest elements to x in a sorted list are always k consecutive elements.

**Say this first (1 line):** "Search the window start in [0, n - k]: if x - arr[mid] is strictly greater than arr[mid + k] - x, the window must move right; otherwise keep mid."

**Brute force:** Sort a copy by `(distance to x, value)`, take the first k, sort those ascending. O(n log n). It is the checker.

**Optimal:**
- Candidate window starts are 0..n-k, so `lo, hi = 0, n - k`.
- Compare the two elements that decide a slide by one: `arr[mid]` (left end, leaves if we move right) and `arr[mid + k]` (right neighbour, enters).
- If `x - arr[mid] > arr[mid + k] - x`: the incoming element is strictly closer, so the best window starts after mid: `lo = mid + 1`.
- Else: `hi = mid`. This includes the tie, which keeps the smaller (left) values as the prompt requires.
- Invariant: the best window start is in [lo, hi]. Return `arr[lo:lo + k]`.
- Why only these two elements: the list is sorted, so the window must be contiguous, and whether sliding from mid to mid + 1 helps depends only on those two ends.
- Uniqueness of the result: the answer list is unique as a list of VALUES. I tested it exhaustively on all sorted lists with duplicates (values 0..6, length up to 7, every k, x from -2 to 8). Three formulations of the rule (distance then value; distance then smaller index; distance, value, then larger index) always produce the same value list, and the binary search matches them. Different tied elements can have different indices but equal values, so the output is the same.
- The tie rule matters: `[1, 3]`, k=1, x=2 must give `[1]`, not `[3]`.

**Complexity:** Time O(log(n - k)) for the search plus O(k) to slice the answer. Space O(k) for the output (O(1) extra).

**Dry run:** `[1,2,3,4,5]`, k=4, x=-1. lo=0, hi=1. mid=0: x - arr[0] = -2, arr[4] - x = 6; -2 > 6 is False, so hi=0. Window `arr[0:4] = [1,2,3,4]`.
`[1,1,2,3,4,5]`, k=3, x=4: lo=0, hi=3. mid=1: 4-1=3 > arr[4]-4=0, lo=2. mid=2: 4-2=2 > arr[5]-4=1, lo=3. Window `arr[3:6] = [3,4,5]`.

**Code:**
```python
import itertools
import random


def k_closest_brute(arr, k, x):
    # sort by (distance, value), take k, then sort the values ascending
    return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])


def k_closest(arr, k, x):
    lo, hi = 0, len(arr) - k               # candidate left edges of the window
    while lo < hi:
        mid = (lo + hi) // 2
        if x - arr[mid] > arr[mid + k] - x:    # right neighbour arr[mid+k] is strictly closer
            lo = mid + 1                       # window must start after mid
        else:
            hi = mid                           # tie or left side closer: keep mid (smaller values win ties)
    return arr[lo:lo + k]


examples = [([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]), ([1, 2, 3, 4, 5], 4, -1, [1, 2, 3, 4]),
            ([1, 3], 1, 2, [1]), ([1, 1, 2, 3, 4, 5], 3, 4, [3, 4, 5]), ([1, 2, 3, 4, 5], 2, 10, [4, 5])]
for arr, k, x, want in examples:
    assert k_closest(arr, k, x) == k_closest_brute(arr, k, x) == want, (arr, k, x)
    print(arr, "k =", k, "x =", x, "->", k_closest(arr, k, x))

# Exhaustive uniqueness test. The stated rule is: distance, then smaller value. Three ways to apply it must give
# the same VALUE list: (1) the value-keyed sort above, (2) distance then smaller INDEX (same thing on a sorted list),
# (3) distance, then value, then LARGER index (equal values at equal distance are interchangeable).
def by_index(arr, k, x, reverse_index):
    order = sorted(range(len(arr)), key=(lambda i: (abs(arr[i] - x), arr[i], -i)) if reverse_index else (lambda i: (abs(arr[i] - x), i)))
    return sorted(arr[i] for i in order[:k])


tested = 0
for n in range(1, 8):
    for arr in itertools.combinations_with_replacement(range(0, 7), n):   # every sorted list with duplicates
        arr = list(arr)
        for k in range(1, n + 1):
            for x in range(-2, 9):
                a = k_closest_brute(arr, k, x)
                assert a == by_index(arr, k, x, False) == by_index(arr, k, x, True), (arr, k, x)
                assert k_closest(arr, k, x) == a, (arr, k, x, k_closest(arr, k, x), a)
                tested += 1
print("exhaustive check passed:", tested, "(arr, k, x) triples; tie rules agree, binary search matches")

# a tie that is NOT resolved by value alone would break uniqueness: show the tie rule matters
assert k_closest([1, 3], 1, 2) == [1] and k_closest([1, 3], 1, 2) != [3]
print("tie case [1, 3], k=1, x=2 ->", k_closest([1, 3], 1, 2), "(smaller value wins; [3] would be wrong)")

# seeded random larger inputs
rng = random.Random(24)
for _ in range(1500):
    n = rng.randint(1, 40)
    arr = sorted(rng.randint(-20, 20) for _ in range(n))
    k = rng.randint(1, n)
    x = rng.randint(-30, 30)
    assert k_closest(arr, k, x) == k_closest_brute(arr, k, x), (arr, k, x)
print("random check passed: 1500 cases")

# edge cases
assert k_closest([5], 1, 100) == [5]
assert k_closest([2, 2, 2, 2], 2, 2) == [2, 2]
assert k_closest([1, 2, 3], 3, 0) == [1, 2, 3]          # k == n: window is the whole list
big = list(range(10 ** 4))
assert k_closest(big, 5, 10 ** 9) == big[-5:] and k_closest(big, 5, -10 ** 9) == big[:5]
print("edge asserts passed")
```

**Output (my run):**
```
[1, 2, 3, 4, 5] k = 4 x = 3 -> [1, 2, 3, 4]
[1, 2, 3, 4, 5] k = 4 x = -1 -> [1, 2, 3, 4]
[1, 3] k = 1 x = 2 -> [1]
[1, 1, 2, 3, 4, 5] k = 3 x = 4 -> [3, 4, 5]
[1, 2, 3, 4, 5] k = 2 x = 10 -> [4, 5]
exhaustive check passed: 231231 (arr, k, x) triples; tie rules agree, binary search matches
tie case [1, 3], k=1, x=2 -> [1] (smaller value wins; [3] would be wrong)
random check passed: 1500 cases
edge asserts passed
```
All five examples in the prompt are correct, and the "answer list is uniquely determined" claim holds: it was checked on the exhaustive set printed above (231231 triples).

**Edge cases:**
- x below everything: first k. x above everything: last k.
- k = n: `hi = 0`, the whole list.
- Duplicates around x: the tie goes left, and equal values give the same list.
- Negative x: nothing special; subtraction is fine in Python.

**Follow-ups:**
- *Return indices instead of values?* Same window; indices lo..lo+k-1 are one valid choice among tied equal values.
- *Unsorted input?* Heap of size k, O(n log k) (Part 8).
- *Simpler O(n) alternative?* Two pointers shrinking from both ends until the window has k elements.

**Common mistakes:**
- Searching in [0, n - 1]: `arr[mid + k]` runs off the end.
- Using `abs()` and then getting the tie direction wrong; the subtraction form puts the tie on the left.
- Using `<` instead of strict `>` in the move-right test, which returns the larger value on ties.

### Q25 ⭐⭐ 🟡 Single element in a sorted array of pairs. `nums` is sorted ascending; every value appears exactly twice except one value that appears exactly once (len is odd, 1 <= len <= 10^5), so that one value is unique by the statement. Return it in O(log n) time and O(1) space. Binary search over even indices e: before the odd value, pairs sit at (e, e+1), after it they are shifted; compare nums[mid] with its partner chosen by the parity of mid. Explain why the length of the left part being even or odd decides which half to keep. Example: [1,1,2,3,3,4,4,8,8] -> 2; [3,3,7,7,10,11,11] -> 10; [5] -> 5; [1,2,2] -> 1; [1,1,2] -> 2.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Binary search on a parity invariant. Before the single element every pair sits at (even, odd) indices; after it the pairs are shifted to (odd, even).

**Say this first (1 line):** "Always test at an even index mid: if nums[mid] == nums[mid + 1] the pairs are intact up to there, so the single is to the right; otherwise it is at mid or to the left."

**Brute force:** Count each value (or XOR everything). O(n) time. XOR is O(1) space but still linear, so it does not meet the O(log n) requirement. Both are checkers.

**Optimal:**
- `lo, hi = 0, n - 1`. Because n is odd, n - 1 is even; `lo` and `hi` both stay even.
- `mid = (lo + hi) // 2`; if mid is odd, do `mid -= 1` so mid is even. Then its partner is `mid + 1`.
- `nums[mid] == nums[mid + 1]`: the pair at (mid, mid + 1) is intact, so the left part [lo, mid + 1] holds whole pairs, an even-length block, nothing odd in it. The single is right of it: `lo = mid + 2`.
- Otherwise: nums[mid] is the single, or the pair is shifted, so the single is at mid or left: `hi = mid`.
- Parity argument: the left part before the single has even length (whole pairs). That is why intact pairs start at even indices. After the single, the left part has odd length, so pairs start at odd indices. Checking "does the pair starting at an even index match" asks which side of the single we are on.
- Invariant: the single lies in [lo, hi]; the loop ends when `lo == hi`.
- The prompt says the single value is unique by the statement. I checked that on every generated input: exactly one value has count 1, and the length is odd. (If the statement allowed a value to appear 3 times, none of this would hold.)

**Complexity:** Time O(log n), space O(1).

**Dry run:** `[1,1,2,3,3,4,4,8,8]`. lo=0, hi=8. mid=4 (even): nums[4]=3, nums[5]=4, not equal, hi=4. mid=2: nums[2]=2, nums[3]=3, not equal, hi=2. mid=1 is odd, becomes 0: nums[0]=1 == nums[1], lo=2. lo == hi = 2, answer nums[2] = 2.

**Code:**
```python
import itertools
import random
from collections import Counter


def single_brute(nums):
    return next(v for v, c in Counter(nums).items() if c == 1)


def single_xor(nums):
    r = 0
    for v in nums:
        r ^= v                              # O(n) time, O(1) space: the linear baseline (pairs cancel)
    return r


def single_bs(nums):
    lo, hi = 0, len(nums) - 1               # lo and hi are always even
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2 == 1:
            mid -= 1                        # make mid even: pair partner is mid + 1
        if nums[mid] == nums[mid + 1]:      # pair intact at (even, odd): single is to the right
            lo = mid + 2
        else:                               # pair broken: single is at mid or to the left
            hi = mid
    return nums[lo]


for nums, want in [([1, 1, 2, 3, 3, 4, 4, 8, 8], 2), ([3, 3, 7, 7, 10, 11, 11], 10),
                   ([5], 5), ([1, 2, 2], 1), ([1, 1, 2], 2)]:
    assert single_bs(nums) == single_xor(nums) == single_brute(nums) == want, nums
    print(nums, "->", single_bs(nums))

# exhaustive: choose distinct values (the pair values plus the single), every position of the single,
# input is sorted and valid by construction; also assert the statement's promise (exactly one value with count 1)
tested = 0
for d in range(1, 9):                       # number of distinct values; length = 2*d - 1
    for vals in itertools.combinations(range(-3, 9), d):
        for s in range(d):                  # which distinct value is the single one
            nums = []
            for i, v in enumerate(vals):
                nums += [v] if i == s else [v, v]
            cnt = Counter(nums)
            assert sum(1 for c in cnt.values() if c == 1) == 1 and len(nums) % 2 == 1
            assert single_bs(nums) == vals[s] == single_brute(nums), nums
            tested += 1
print("exhaustive check passed:", tested, "valid inputs (up to 15 elements)")

# seeded random big input
rng = random.Random(25)
for _ in range(300):
    d = rng.randint(1, 600)
    vals = sorted(rng.sample(range(-10 ** 6, 10 ** 6), d))
    s = rng.randrange(d)
    nums = []
    for i, v in enumerate(vals):
        nums += [v] if i == s else [v, v]
    assert single_bs(nums) == vals[s]
print("random check passed: 300 inputs up to 1199 elements")

# edge cases
assert single_bs([0]) == 0
assert single_bs([1, 1, 2, 2, 3]) == 3                  # single at the very end
assert single_bs([0, 1, 1, 2, 2]) == 0                  # single at the very start
big = [v for i in range(50000) for v in (i, i)] + [10 ** 9]
assert single_bs(big) == 10 ** 9 and len(big) == 100001
print("edge asserts passed")
```

**Output (my run):**
```
[1, 1, 2, 3, 3, 4, 4, 8, 8] -> 2
[3, 3, 7, 7, 10, 11, 11] -> 10
[5] -> 5
[1, 2, 2] -> 1
[1, 1, 2] -> 2
exhaustive check passed: 21792 valid inputs (up to 15 elements)
random check passed: 300 inputs up to 1199 elements
edge asserts passed
```
All five examples in the prompt are correct. The exhaustive check built every sorted valid input from up to 8 distinct values (drawn from -3..8) with every choice of which value is single.

**Edge cases:**
- Length 1: loop never runs, return `nums[0]`.
- Single at the start: `[0, 1, 1, 2, 2]`. At the end: `[1, 1, 2, 2, 3]`.
- Large values: only equality is tested.
- Do not use `nums[mid + 1]` with odd `hi`: that is why `hi` stays even.

**Follow-ups:**
- *Why not just XOR?* O(n); it is the right answer when the input is unsorted.
- *Trick with `mid ^= 1`?* `mid ^ 1` gives the partner index at any parity; the same idea written differently.
- *Every element appears three times except one?* Not sorted-pair logic; use bit counting (Part 12).

**Common mistakes:**
- Using `hi = mid - 1` or `lo = mid + 1`: loses the possibility that mid is the single, or lands on an odd index.
- Not forcing mid to be even.
- Forgetting that the length is odd, so `hi = n - 1` is even.

### Q26 ⭐⭐ 🟡 Kth smallest element in a sorted matrix. `matrix` is n x n (1 <= n <= 300); each row and each column is sorted ascending (no other structure); 1 <= k <= n*n, and k counts duplicates (the k-th element of the sorted flattened list). Binary search on the VALUE in [matrix[0][0], matrix[-1][-1]]: count(v) = number of entries <= v computed by a staircase walk in O(n), and return the smallest v with count(v) >= k. Explain why that v is guaranteed to be an entry of the matrix. (A heap solution exists and belongs to Part 8; mention it only as the alternative.) Example: [[1,5,9],[10,11,13],[12,13,15]], k=8 -> 13; [[-5]], k=1 -> -5; [[1,2],[1,3]], k=2 -> 1; [[1,2],[1,3]], k=3 -> 2.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports)

**Pattern:** Binary search on the VALUE with a counting function. The matrix is not a sorted list you can index, but "how many entries are <= v" is monotone in v.

**Say this first (1 line):** "Binary search v between the smallest and largest entry; count entries <= v with a staircase walk in O(n); the answer is the smallest v with count >= k."

**Brute force:** Flatten, sort, take index k - 1. O(n^2 log n) time, O(n^2) space. It is the checker.

**Optimal:**
- `lo, hi = matrix[0][0], matrix[-1][-1]` (the smallest and largest entries, because rows and columns ascend).
- `count_le(v)`: start at the bottom-left. If `mat[r][c] <= v`, then all `r + 1` entries above it in column c are `<= v`; add `r + 1` and move right. Else move up. At most 2n steps.
- Find the smallest v with `count_le(v) >= k`: `if count >= k: hi = mid else lo = mid + 1`.
- Duplicates are handled because count counts every entry (the prompt counts duplicates).
- Why the answer is an entry: let v be the smallest value with count(v) >= k. For integers, `count(v) - count(v - 1)` is the number of entries equal to v. If v were not an entry, that difference would be 0, so `count(v - 1) = count(v) >= k`, contradicting minimality of v. (v = matrix[0][0] is itself an entry.) The output shows count jumping from 6 at 12 to 8 at 13 in the example, and staying flat where no entry lives.
- Heap alternative: pop k times from a min-heap of row heads, O(k log n); that is Part 8's topic.

**Complexity:** Time O(n log(max - min)): about 31 rounds for values within 2 * 10^9, each O(n). Space O(1). For n = 300 that is a few thousand operations per round.

**Dry run:** `[[1,5,9],[10,11,13],[12,13,15]]`, k=8. Range [1, 15]. mid=8: count_le(8) = 2 (just 1 and 5) < 8, lo=9. mid=12: count 6 < 8, lo=13. mid=14: count 8 >= 8, hi=14. mid=13: count 8 >= 8, hi=13. Answer 13, which is an entry. Sorted flat list is [1,5,9,10,11,12,13,13,15], the 8th element is 13.

**Code:**
```python
import random


def kth_brute(mat, k):
    return sorted(v for row in mat for v in row)[k - 1]


def count_le(mat, v):
    # staircase from the bottom-left: number of entries <= v in O(n)
    n = len(mat)
    r, c, total = n - 1, 0, 0
    while r >= 0 and c < n:
        if mat[r][c] <= v:
            total += r + 1                  # the whole column segment above (and including) row r is <= v
            c += 1
        else:
            r -= 1
    return total


def kth_smallest(mat, k):
    lo, hi = mat[0][0], mat[-1][-1]         # smallest and largest entries
    while lo < hi:                          # smallest v with count_le(v) >= k
        mid = (lo + hi) // 2
        if count_le(mat, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


for mat, k, want in [([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8, 13), ([[-5]], 1, -5),
                     ([[1, 2], [1, 3]], 2, 1), ([[1, 2], [1, 3]], 3, 2)]:
    assert kth_smallest(mat, k) == kth_brute(mat, k) == want, (mat, k)
    print(mat, "k =", k, "->", kth_smallest(mat, k))


def random_matrix(rng, n, lo=-15, hi=30):
    mat = [sorted(rng.randint(lo, hi) for _ in range(n)) for _ in range(n)]     # rows sorted
    cols = [sorted(mat[r][c] for r in range(n)) for c in range(n)]               # then sort each column
    mat = [[cols[c][r] for c in range(n)] for r in range(n)]
    assert all(mat[r][c] <= mat[r][c + 1] for r in range(n) for c in range(n - 1))
    assert all(mat[r][c] <= mat[r + 1][c] for r in range(n - 1) for c in range(n))
    return mat


rng = random.Random(26)
hit_entry = 0
for _ in range(600):
    n = rng.randint(1, 6)
    mat = random_matrix(rng, n)
    entries = {v for row in mat for v in row}
    for k in range(1, n * n + 1):
        got = kth_smallest(mat, k)
        assert got == kth_brute(mat, k), (mat, k)
        assert got in entries                # the guarantee asked about: the answer is an entry
        hit_entry += 1
print("random check passed:", hit_entry, "(matrix, k) pairs; answer was always an entry")

# the argument in numbers: count_le changes only at entry values (integers), so the smallest v with count >= k is an entry
mat = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
print("count_le for v = 9..13:", [(v, count_le(mat, v)) for v in range(9, 14)])
assert count_le(mat, 12) == count_le(mat, 11) + 1 and count_le(mat, 13) == 8

# edge cases
assert kth_smallest([[7, 7], [7, 7]], 3) == 7          # all equal
assert kth_smallest([[1, 2], [3, 4]], 4) == 4 and kth_smallest([[1, 2], [3, 4]], 1) == 1
big = random_matrix(rng, 300, -10 ** 9, 10 ** 9)
assert kth_smallest(big, 45000) == kth_brute(big, 45000) and kth_smallest(big, 90000) == kth_brute(big, 90000)
print("edge asserts passed (including a 300 x 300 matrix)")
```

**Output (my run):**
```
[[1, 5, 9], [10, 11, 13], [12, 13, 15]] k = 8 -> 13
[[-5]] k = 1 -> -5
[[1, 2], [1, 3]] k = 2 -> 1
[[1, 2], [1, 3]] k = 3 -> 2
random check passed: 9819 (matrix, k) pairs; answer was always an entry
count_le for v = 9..13: [(9, 3), (10, 4), (11, 5), (12, 6), (13, 8)]
edge asserts passed (including a 300 x 300 matrix)
```
All four examples in the prompt are correct. The random check generates valid matrices (rows sorted, then each column sorted, which keeps the rows sorted) and asserts the result is an entry every time.

**Edge cases:**
- n = 1: `lo == hi`, returns the single entry.
- All equal entries: count jumps from 0 to n*n at that value.
- k = 1 returns the top-left, k = n*n returns the bottom-right.
- Negative values are fine; `(lo + hi) // 2` floors consistently and the interval still shrinks (`hi = mid` or `lo = mid + 1`).

**Follow-ups:**
- *Why can't I binary search the cells?* There is no total order along any path through a matrix with only row/column order.
- *Faster?* There are more specialised selection algorithms for sorted matrices; the value search is the expected answer.
- *Median of a row-sorted matrix?* Same value search with per-row bisect (Q37).

**Common mistakes:**
- Binary searching indices (0..n*n-1) instead of values.
- Returning `lo` from a plain "count == k" search: duplicates mean count may jump past k.
- Counting from the wrong corner (top-left or bottom-right cannot decide).

### Q27 ⭐⭐ 🟡 Cut logs to a maximum equal length. `logs` is a list of positive integer lengths (1 <= len <= 10^5, values up to 10^9) and k >= 1. You may cut logs into pieces of one common integer length L >= 1 (leftovers are discarded). Return the largest L that yields at least k pieces, or 0 if even L = 1 yields fewer than k. Binary search L in [1, max(logs)] using the upper-biased mid for a 'last True' search and explain why 'pieces(L) >= k' is True for small L and False for large L. Example: [232,124,456], k=7 -> 114; [5,5,5], k=2 -> 5; [1,2], k=10 -> 0; [5,5,5], k=3 -> 5; [5,5,5], k=4 -> 2.
**Asked at:** Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Binary search on the answer, "maximise the minimum / largest feasible value", a last-True search with an upper-biased mid.

**Say this first (1 line):** "pieces(L) = sum of log // L is non-increasing in L, so I want the last L with pieces(L) >= k, searched with the upper mid; if even L = 1 fails, the answer is 0."

**Brute force:** Try every L from max(logs) down to 1 and return the first with at least k pieces. O(max(logs) * n), which is 10^14 at the limits. It is the checker.

**Optimal:**
- Predicate `pieces(L) >= k`: True for small L, False for large L. Why: if L works and L' < L, each log gives `x // L' >= x // L` pieces, so L' works too. So the pattern is True...True False...False.
- Last-True search: `lo, hi = 0, max(logs)`; `mid = (lo + hi + 1) // 2`; if feasible `lo = mid` else `hi = mid - 1`. The upper bias is required: with a floor mid and `lo = mid`, the state lo = x, hi = x + 1 never moves.
- `lo = 0` is a stand-in for "no valid L"; the prompt wants 0 in that case, and mid is always >= 1, so `pieces` never divides by zero.
- Invariant: lo is feasible (or 0), and every L > hi is infeasible.
- When pieces(1) = sum(logs) < k, nothing is feasible and the loop walks down to 0.
- A tighter hi is `min(max(logs), sum(logs) // k)`, since pieces(L) <= sum / L; optional.

**Complexity:** Time O(n log(max)): about 30 rounds of an O(n) sum for values up to 10^9. Space O(1).

**Dry run:** `[5, 5, 5]`, k=4. lo=0, hi=5. mid=3: pieces=3 < 4, hi=2. mid=1: pieces=15 >= 4, lo=1. mid=2: pieces=6 >= 4, lo=2. lo == hi == 2. Check: L=3 gives 3 pieces, not enough; L=2 gives 6.

**Code:**
```python
import random


def cut_brute(logs, k):
    # try every L from big to small; first one that gives >= k pieces wins
    for L in range(max(logs), 0, -1):
        if sum(x // L for x in logs) >= k:
            return L
    return 0


def pieces(logs, L):
    return sum(x // L for x in logs)        # non-increasing in L


def cut_logs(logs, k):
    lo, hi = 0, max(logs)                   # lo = 0 means "no valid L yet"; lo is always feasible (0 by convention)
    while lo < hi:                          # last True of: L == 0 or pieces(L) >= k
        mid = (lo + hi + 1) // 2            # upper-biased so lo = mid always makes progress
        if pieces(logs, mid) >= k:
            lo = mid
        else:
            hi = mid - 1
    return lo


for logs, k, want in [([232, 124, 456], 7, 114), ([5, 5, 5], 2, 5), ([1, 2], 10, 0), ([5, 5, 5], 3, 5), ([5, 5, 5], 4, 2)]:
    assert cut_logs(logs, k) == cut_brute(logs, k) == want, (logs, k)
    print(logs, "k =", k, "->", cut_logs(logs, k))

rng = random.Random(27)
zero = 0
for _ in range(2000):
    logs = [rng.randint(1, 30) for _ in range(rng.randint(1, 6))]
    k = rng.randint(1, 40)
    got, want = cut_logs(logs, k), cut_brute(logs, k)
    assert got == want, (logs, k, got, want)
    if got:
        assert pieces(logs, got) >= k and pieces(logs, got + 1) < k     # largest feasible L
    zero += got == 0
    # monotone: pieces never increases as L grows
    assert all(pieces(logs, L) >= pieces(logs, L + 1) for L in range(1, 31))
print("random check passed: 2000 cases,", zero, "returned 0; pieces(L) was non-increasing every time")

# edge cases
assert cut_logs([1], 1) == 1 and cut_logs([1], 2) == 0
assert cut_logs([10 ** 9], 1) == 10 ** 9 and cut_logs([10 ** 9], 10 ** 9) == 1 and cut_logs([10 ** 9], 10 ** 9 + 1) == 0
assert cut_logs([10 ** 9] * 10 ** 5, 10 ** 5) == 10 ** 9
assert cut_logs([7, 7, 7], 21) == 1 and cut_logs([7, 7, 7], 22) == 0
print("edge asserts passed")
```

**Output (my run):**
```
[232, 124, 456] k = 7 -> 114
[5, 5, 5] k = 2 -> 5
[1, 2] k = 10 -> 0
[5, 5, 5] k = 3 -> 5
[5, 5, 5] k = 4 -> 2
random check passed: 2000 cases, 313 returned 0; pieces(L) was non-increasing every time
edge asserts passed
```
All five examples in the prompt are correct. The random check also verifies that pieces(L) is non-increasing and that `pieces(ans) >= k > pieces(ans + 1)` when the answer is positive.

**Edge cases:**
- Total length below k: 0.
- k = 1: `max(logs)`.
- One log, k = log length: L = 1.
- Huge values (10^9) and k up to 10^9 + 1: still about 30 rounds.
- Do not return -1 for infeasible: the prompt says 0.

**Follow-ups:**
- *Real-valued L?* Fixed iteration count (Q40 style); floor division becomes real division.
- *Cut only to be at least k pieces but minimise waste?* Different objective; not monotone the same way.
- *Why not sort?* The predicate does not depend on order.

**Common mistakes:**
- Floor mid with `lo = mid` (infinite loop).
- Starting `lo = 1` and then returning 1 when nothing is feasible (prompt wants 0).
- Searching only L >= 1 and returning `lo = 1` when nothing is feasible, instead of checking pieces(1) first.

### Q28 ⭐⭐ 🟡 The bisect module and the key= parameter (Python 3.10+). A list of (name, age) tuples `people` is already sorted by age. Using `bisect` with `key=lambda t: t[1]`: (a) count the people younger than 30 with `bisect_left`, (b) insert ('zed', 30) after all existing age-30 entries with `insort_right`, and (c) binary search on the answer by running `bisect_left(range(100), 50, key=lambda v: v * v)` to get the smallest v with v*v >= 50. State precisely where key is applied: to the list elements in `bisect_left`/`bisect_right`, and to the search value x as well in `insort_left`/`insort_right`. Explain why `insort` is O(n) in total even though the search is O(log n), and what the pre-3.10 workaround (a parallel list of keys) looks like. Example: people=[('ann',22),('bob',30),('cy',30),('di',41)] -> (a) 1, (b) [('ann',22),('bob',30),('cy',30),('zed',30),('di',41)], (c) 8. (A prefix-count use of sorted-list bisect is in Part 3 Q36.)
**Asked at:** Python documentation mirrors for bisect (docs.python.org 3.10 and current .rst source: key added in 3.10, key not applied to the search value in bisect_left/bisect_right, insort is O(n) overall; snippets only, direct fetch failed with ENOTFOUND; behaviour re-verified in the sandbox) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** The bisect module with `key=` (Python 3.10+). It turns "binary search a list of records" and "binary search an answer range" into one-liners.

**Say this first (1 line):** "key is applied to the list elements in bisect_left and bisect_right, but NOT to the value x; insort applies it to x as well, and inserting is still O(n) because of the shift."

**Brute force:** Linear scans: count ages below 30, `sorted()` after appending, first v with v*v >= 50. O(n) or O(n log n) each. Used as checkers.

**Optimal:**
- (a) `bisect_left(people, 30, key=lambda t: t[1])` is 1: the first index whose age is >= 30. x is the plain age 30, not a tuple. Count of people younger than 30 is that index.
- (b) `insort_right(people, ('zed', 30), key=...)`: insort applies the key to x too (so you pass the whole record) and inserts the record itself. insort_right puts it after existing equal keys, so zed lands after bob and cy. `insort_left` would put it before them.
- (c) `bisect_left(range(100), 50, key=lambda v: v * v)`: the key maps each candidate v to v*v, and the search finds the first v with v*v >= 50. `range` supports indexing without building a list, so this is binary search on the answer in one line. Result 8.
- Where key applies, precisely:
  | function | key applied to list elements | key applied to x |
  |---|---|---|
  | bisect_left / bisect_right | yes | no |
  | insort_left / insort_right | yes | yes |
  Passing a tuple as x to `bisect_left` with an age key compares an int with a tuple and raises TypeError (shown in the run).
- Why insort is O(n): the search is O(log n), but `list.insert` shifts the tail, O(n). So repeated insertions cost O(n^2). Use a heap, a balanced structure, or sort once if you need many inserts.
- Pre-3.10 workaround: keep a parallel list `keys = [p[1] for p in people]`; `i = bisect_right(keys, 30)`; then `keys.insert(i, 30)` and `people.insert(i, rec)` so both lists stay aligned.
- The sorted-by-key precondition still applies: the list must already be sorted by the key.

**Complexity:** `bisect_*`: O(log n) key calls (key is applied to O(log n) elements, not all n). `insort_*`: O(log n) search plus O(n) shift. Space O(1).

**Dry run:** people ages `[22, 30, 30, 41]`.
(a) Left bound of 30: index 1. (b) Right bound of 30: index 3, insert there, giving the list in the prompt. (c) v*v for v=0..99; first at least 50: 7*7 = 49 < 50, 8*8 = 64 >= 50, so 8.

**Code:**
```python
import random
import sys
from bisect import bisect_left, bisect_right, insort_left, insort_right

assert sys.version_info >= (3, 10), "key= needs Python 3.10+"
print("python", sys.version_info.major, sys.version_info.minor)

age = lambda t: t[1]
people = [('ann', 22), ('bob', 30), ('cy', 30), ('di', 41)]

# (a) count people younger than 30: x is a plain age, key is applied to the LIST ELEMENTS only
a = bisect_left(people, 30, key=age)
print("(a)", a)
assert a == 1 == sum(1 for p in people if p[1] < 30)

# (b) insert ('zed', 30) after the existing age-30 entries: insort applies key to x too, but inserts x itself
b = list(people)
insort_right(b, ('zed', 30), key=age)
print("(b)", b)
assert b == [('ann', 22), ('bob', 30), ('cy', 30), ('zed', 30), ('di', 41)]

# (c) binary search on the answer: smallest v in 0..99 with v*v >= 50
c = bisect_left(range(100), 50, key=lambda v: v * v)
print("(c)", c)
assert c == 8 == next(v for v in range(100) if v * v >= 50)

# where key is NOT applied: passing a whole tuple as x to bisect_left compares 30 (key of element) with a tuple
try:
    bisect_left(people, ('zed', 30), key=age)
except TypeError as e:
    print("bisect_left with a tuple x ->", type(e).__name__)
# insort_left, by contrast, applies key to x as well, so the tuple is fine and goes BEFORE the age-30 entries
d = list(people)
insort_left(d, ('zed', 30), key=age)
print("insort_left puts it first among age 30:", d)
assert d[1] == ('zed', 30)
# bisect_right on a plain age behaves like upper bound
assert bisect_right(people, 30, key=age) == 3 and bisect_right(people, 5, key=age) == 0 and bisect_right(people, 99, key=age) == 4

# pre-3.10 workaround: a parallel list of keys that is kept in step with the data
keys = [p[1] for p in people]
assert bisect_left(keys, 30) == a
pk, pd = list(keys), list(people)
i = bisect_right(pk, 30)
pk.insert(i, 30)
pd.insert(i, ('zed', 30))
assert pd == b, "parallel-list workaround gives the same list"
print("parallel-key workaround matches:", pd == b)

# seeded randomised cross-check against linear scans
rng = random.Random(28)
for _ in range(2000):
    lst = sorted(((rng.choice('abcdef'), rng.randint(15, 45)) for _ in range(rng.randint(0, 12))), key=age)
    x = rng.randint(10, 50)
    assert bisect_left(lst, x, key=age) == sum(1 for p in lst if p[1] < x)
    assert bisect_right(lst, x, key=age) == sum(1 for p in lst if p[1] <= x)
    new = ('n', x)
    r1 = list(lst); insort_right(r1, new, key=age)
    assert [p[1] for p in r1] == sorted(p[1] for p in lst + [new])
    assert r1[bisect_right(lst, x, key=age)] == new          # landed after all equal ages
print("random check passed: 2000 cases")

# edge cases
assert bisect_left([], 5, key=age) == 0
assert bisect_left(range(100), 0, key=lambda v: v * v) == 0 and bisect_left(range(100), 10 ** 9, key=lambda v: v * v) == 100
print("edge asserts passed")
```

**Output (my run):**
```
python 3 13
(a) 1
(b) [('ann', 22), ('bob', 30), ('cy', 30), ('zed', 30), ('di', 41)]
(c) 8
bisect_left with a tuple x -> TypeError
insort_left puts it first among age 30: [('ann', 22), ('zed', 30), ('bob', 30), ('cy', 30), ('di', 41)]
parallel-key workaround matches: True
random check passed: 2000 cases
edge asserts passed
```
All three results in the prompt (a) 1, (b) the list with zed after cy, (c) 8 are correct on Python 3.13. The TypeError line is the demonstration that key is not applied to x in bisect_left.

**Edge cases:**
- Empty list: index 0.
- Search value below all keys: 0; above all: len.
- key function that is expensive: it is called O(log n) times per search, fine.
- Python older than 3.10: `key=` raises TypeError; use the parallel list.

**Follow-ups:**
- *Why not bisect the tuples directly?* Tuples compare by name first, but the list is ordered by age, so the comparisons would be meaningless.
- *Many inserts?* `sortedcontainers.SortedList` amortises the shifting; in an interview say it and explain the idea (blocks).
- *Prefix counts with a sorted list?* See Part 3 Q36.

**Common mistakes:**
- Passing a record as x to bisect_left with a key.
- Assuming insort is O(log n).
- Using `bisect_left` where `insort_right` semantics (after equals) was wanted, which changes stability among equal keys.

### Q29 ⭐⭐ 🟡 Off-by-one invariants: closed versus half-open templates. Write the two standard templates for a monotone predicate over indices: (1) 'first index in [0, n) where pred is True, or n if none' using `lo, hi = 0, n`, `while lo < hi`, `mid = (lo + hi) // 2`, `hi = mid` or `lo = mid + 1`; (2) 'last index where pred is True, or -1 if none' using `while lo < hi` with `mid = (lo + hi + 1) // 2` and `lo = mid` or `hi = mid - 1` over [-1, n-1]. Give each template's loop invariant, and demonstrate the classic infinite loop: with `mid = (lo + hi) // 2` and the update `lo = mid` on lo=3, hi=4 mid stays 3 forever. Say when `lo <= hi` with `mid +/- 1` is the better fit (exact-match search). Example: a=[0,0,1,1,1], pred(i) = a[i] == 1 -> template 1 gives 2; pred(i) = a[i] == 0 -> template 2 gives 1; all-False predicate -> 5 for template 1 and -1 for template 2; all-True -> 0 for template 1 and 4 for template 2.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Off-by-one invariants. Two half-open templates, one for "first True" and one for "last True", and the closed template for exact match.

**Say this first (1 line):** "First True uses mid = floor with hi = mid or lo = mid + 1; last True needs the upper mid because lo = mid would otherwise stall; I always state what [lo, hi] means."

**Brute force:** A linear scan for the first True or last True. O(n). Used as the checker, plus an exhaustive test over every monotone predicate.

**Optimal:**
- Template 1, first True in [0, n), n if none: `lo, hi = 0, n`; `while lo < hi`; `mid = (lo + hi) // 2`; `if pred(mid): hi = mid else: lo = mid + 1`. Return `lo`.
  - Invariant: every index < lo is False, every index >= hi is True (hi = n counts as "virtually True"). The answer is in [lo, hi].
  - Floor mid satisfies `lo <= mid < hi`, so both updates shrink the interval: `hi = mid` makes hi smaller, `lo = mid + 1` makes lo larger. pred is never called at index n.
- Template 2, last True, -1 if none: `lo, hi = -1, n - 1`; `while lo < hi`; `mid = (lo + hi + 1) // 2`; `if pred(mid): lo = mid else: hi = mid - 1`. Return `lo`.
  - Invariant: lo is True or the virtual -1; every index > hi is False. The answer is in [lo, hi].
  - Upper mid satisfies `lo < mid <= hi`, so `lo = mid` moves forward and `hi = mid - 1` moves back. pred is never called at -1.
- The classic infinite loop: with `mid = (lo + hi) // 2` and `lo = mid`, when lo = 3 and hi = 4 mid is 3, lo stays 3, forever. The upper mid gives 4 and the interval shrinks. The run shows the buggy version getting stuck (an iteration cap catches it).
- A Python-only trap: with lo = -1 and hi = 0, `(lo + hi) // 2` is -1 (floor), and `a[-1]` silently reads the last element instead of raising an error.
- When `lo <= hi` with `mid +/- 1` is better: exact-match search. You can return as soon as `a[mid] == target`, and both updates skip mid. Use half-open templates when the answer is a boundary (first/last True), not an element you look for.

**Complexity:** O(log n) pred calls, O(1) space.

**Dry run:** `a = [0,0,1,1,1]`, pred `a[i] == 1`, template 1. lo=0, hi=5: mid=2, True, hi=2. mid=1, False, lo=2. lo == hi == 2.
Template 2 with pred `a[i] == 0`: lo=-1, hi=4: mid=2, False, hi=1. mid=(−1+1+1)//2 = 0, True, lo=0. mid=1, True, lo=1. Answer 1.

**Code:**
```python
import itertools


def first_true(pred, n):
    # template 1: first index in [0, n) with pred True, else n.  invariant: answer in [lo, hi]
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2                # mid < hi always, so hi = mid and lo = mid + 1 both shrink
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def last_true(pred, n):
    # template 2: last index in [0, n) with pred True, else -1.  invariant: answer in [lo, hi]; lo is "known good"
    lo, hi = -1, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2            # upper-biased: mid > lo always, so lo = mid shrinks
        if pred(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def first_true_brute(pred, n):
    return next((i for i in range(n) if pred(i)), n)


def last_true_brute(pred, n):
    return max((i for i in range(n) if pred(i)), default=-1)


a = [0, 0, 1, 1, 1]
print("template 1, a[i]==1:", first_true(lambda i: a[i] == 1, 5))
print("template 2, a[i]==0:", last_true(lambda i: a[i] == 0, 5))
print("all False -> t1, t2:", first_true(lambda i: False, 5), last_true(lambda i: False, 5))
print("all True  -> t1, t2:", first_true(lambda i: True, 5), last_true(lambda i: True, 5))
assert first_true(lambda i: a[i] == 1, 5) == 2 and last_true(lambda i: a[i] == 0, 5) == 1
assert (first_true(lambda i: False, 5), last_true(lambda i: False, 5)) == (5, -1)
assert (first_true(lambda i: True, 5), last_true(lambda i: True, 5)) == (0, 4)

# exhaustive: every monotone predicate for n = 0..11 (False..True for t1, True..False for t2)
checked = 0
for n in range(0, 12):
    for cut in range(n + 1):
        up = lambda i, c=cut: i >= c        # False...False True...True
        down = lambda i, c=cut: i < c       # True...True False...False
        assert first_true(up, n) == first_true_brute(up, n) == cut
        assert last_true(down, n) == last_true_brute(down, n) == cut - 1
        checked += 2
print("exhaustive check passed:", checked, "monotone predicates, n = 0..11")


# the classic infinite loop: floor mid with lo = mid
def last_true_buggy(pred, n, cap=1000):
    lo, hi = -1, n - 1
    steps = 0
    while lo < hi:
        steps += 1
        if steps > cap:
            return "stuck", lo, hi
        mid = (lo + hi) // 2                # BUG: should be (lo + hi + 1) // 2 for lo = mid
        if pred(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


print("buggy template 2 on all-True, n=5:", last_true_buggy(lambda i: True, 5))
assert last_true_buggy(lambda i: True, 5)[0] == "stuck"
# the exact state from the prompt: lo=3, hi=4 -> mid = 3 and lo = mid changes nothing
lo, hi = 3, 4
assert (lo + hi) // 2 == 3 and (lo + hi + 1) // 2 == 4
# Python-specific trap: with lo = -1, (lo + hi) // 2 can be -1, and a[-1] silently reads the LAST element
assert (-1 + 0) // 2 == -1
print("lo=3, hi=4: floor mid =", (3 + 4) // 2, "| upper mid =", (3 + 4 + 1) // 2, "| (-1+0)//2 =", (-1 + 0) // 2)


# lo <= hi with mid +/- 1: the better fit for exact match (can return inside the loop)
def exact(a, t):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == t:
            return mid
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


for n in range(0, 9):
    arr = list(range(0, 2 * n, 2))
    for t in range(-1, 2 * n + 1):
        assert exact(arr, t) == (arr.index(t) if t in arr else -1)
print("exact-match closed template passed for all n < 9")

# edge cases
assert first_true(lambda i: True, 0) == 0 and last_true(lambda i: True, 0) == -1     # empty range
assert first_true(lambda i: i >= 10 ** 9, 10 ** 9 + 5) == 10 ** 9
print("edge asserts passed")
```

**Output (my run):**
```
template 1, a[i]==1: 2
template 2, a[i]==0: 1
all False -> t1, t2: 5 -1
all True  -> t1, t2: 0 4
exhaustive check passed: 156 monotone predicates, n = 0..11
buggy template 2 on all-True, n=5: ('stuck', 3, 4)
lo=3, hi=4: floor mid = 3 | upper mid = 4 | (-1+0)//2 = -1
exact-match closed template passed for all n < 9
edge asserts passed
```
All four results in the prompt are correct (2, 1, 5 and -1, 0 and 4). The exhaustive check runs every monotone predicate (every cut position) for n from 0 to 11 against a linear scan.

**Edge cases:**
- Empty range (n = 0): template 1 returns 0, template 2 returns -1.
- All False: n and -1. All True: 0 and n - 1.
- Predicate that is not monotone: both templates return some boundary, not necessarily the first or last True. Prove monotonicity first (Q33).
- Huge n: the same loops, about 30 rounds for 10^9.

**Follow-ups:**
- *Express last True with template 1?* `first_true(not pred) - 1`.
- *Why not always lo <= hi?* It is fine for exact match; for boundaries the half-open forms avoid the "return lo or hi?" confusion.
- *C++ overflow?* Use `lo + (hi - lo) // 2` there (Q1).

**Common mistakes:**
- Floor mid with `lo = mid`.
- Using `hi = mid - 1` in template 1 (can skip the answer).
- Reading `a[mid]` when mid can be -1 or n.
- Not saying out loud what lo and hi mean.

### Q30 ⭐ 🟡 Search in a sorted array of unknown (effectively infinite) length. You can only call `get(i)`, which returns the i-th element of an ascending list of distinct integers, and returns the sentinel 2147483647 for any index past the end (all real values are smaller than the sentinel). Return the index of `target` or -1. First find a window by doubling `hi` (1, 2, 4, ...) until get(hi) >= target, then binary search inside it. Explain why the number of get calls is O(log p) where p is the answer position (or the insertion position), not O(log n) of any array size, and what happens with the sentinel inside the binary search. Example: hidden [-1,0,3,5,9,12], target=9 -> 4; target=2 -> -1; hidden [7], target=7 -> 0; hidden [7], target=8 -> -1.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Exponential (doubling) search, then ordinary binary search inside the window found.

**Say this first (1 line):** "Double hi until get(hi) >= target, which brackets the target in [hi/2, hi], then binary search that window; the cost is O(log p) where p is the position, not the array size."

**Brute force:** Call get(0), get(1), ... until the value reaches the target or the sentinel. O(p) calls. It is the checker's idea (the checker uses the plain list).

**Optimal:**
- `lo, hi = 0, 1`. While `get(hi) < target`: `lo = hi`, `hi *= 2`.
- Stop condition: `get(hi) >= target`, which includes the sentinel (2147483647 is bigger than any real target). Now the target, if present, is in `[lo, hi]`.
- Then closed binary search in `[lo, hi]`: `mid`, `get(mid)`; equal returns; smaller means `lo = mid + 1`; bigger means `hi = mid - 1`.
- The sentinel inside the binary search: it simply compares as "too big", so the search moves left. No special case is needed, as long as the target is below the sentinel. If the target could equal 2147483647 it would "match" a past-the-end index, so I guard `target >= SENT` and return -1 (real values are smaller than the sentinel).
- Why O(log p): doubling stops at the first power of two hi with get(hi) >= target, so hi < 2 * (p + 1) roughly, where p is the index of the first element >= target (the found or insertion position). That is about log2(p) + 1 doubling calls. The window has about p + 2 positions, so about log2(p) + 1 binary-search calls. Total roughly 2 log2 p + O(1). The array's real length never appears. A one-million-element array with the target at position 3 costs the same 4 calls as a 10-element array.
- Past-the-end reads are safe: `get` returns the sentinel, which the algorithm treats as +infinity.

**Complexity:** O(log p) `get` calls, O(1) space. Run output shows 2 calls at position 0 and 40 calls at position 999999 for n = 10^6.

**Dry run:** hidden `[-1, 0, 3, 5, 9, 12]`, target 9. hi=1: get(1)=0 < 9, lo=1, hi=2. get(2)=3 < 9, lo=2, hi=4. get(4)=9 not < 9, stop. Window [2, 4]: mid=3, get=5 < 9, lo=4; mid=4, get=9, found. Answer 4 (5 calls).

**Code:**
```python
import random

SENT = 2147483647


class Hidden:
    def __init__(self, a):
        self.a, self.calls = a, 0

    def get(self, i):
        self.calls += 1
        return self.a[i] if i < len(self.a) else SENT


def search_unknown(h, target):
    if target >= SENT:                      # real values are < SENT; do not let the sentinel "match"
        return -1
    lo, hi = 0, 1
    while h.get(hi) < target:               # doubling: stop at the first hi with get(hi) >= target
        lo = hi
        hi *= 2
    while lo <= hi:                         # closed binary search in [lo, hi]; the sentinel just reads as "too big"
        mid = (lo + hi) // 2
        v = h.get(mid)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def brute(a, t):
    return a.index(t) if t in a else -1


for a, t, want in [([-1, 0, 3, 5, 9, 12], 9, 4), ([-1, 0, 3, 5, 9, 12], 2, -1), ([7], 7, 0), ([7], 8, -1)]:
    h = Hidden(a)
    got = search_unknown(h, t)
    assert got == brute(a, t) == want
    print(a, "target", t, "->", got, "| get calls:", h.calls)

# call-count bound. p = index of the first element >= target (found or insertion position).
# doubling: hi is the first power of two with get(hi) >= target  -> at most bit_length(p) + 1 calls
# binary search in a window of size hi - lo + 1 <= p + 2 -> at most bit_length(p + 1) + 1 calls
worst_slack = 99
for n in range(0, 140):
    a = list(range(-3, 2 * n - 3, 2))      # distinct ascending, odd step so absent targets fall between
    for t in range(-6, 2 * n + 2):
        h = Hidden(a)
        assert search_unknown(h, t) == brute(a, t), (n, t)
        p = sum(1 for v in a if v < t)
        bound = 2 * (p + 2).bit_length() + 3
        assert h.calls <= bound, (n, t, p, h.calls, bound)
        worst_slack = min(worst_slack, bound - h.calls)
print("exhaustive check passed for lengths 0..139, every target; calls <= 2*bit_length(p+2)+3 (min slack", worst_slack, ")")

# big hidden array: calls depend on the position p, not on the array size
rng = random.Random(30)
n = 10 ** 6
big = sorted(rng.sample(range(-10 ** 9, 10 ** 9), n))
for p in (0, 5, 1000, 10 ** 6 - 1):
    h = Hidden(big)
    assert search_unknown(h, big[p]) == p
    print(f"n = 10^6, answer position {p}: {h.calls} get calls")
h = Hidden(list(range(10 ** 6)))
assert search_unknown(h, 3) == 3
small_calls = h.calls
h = Hidden(list(range(10)))
assert search_unknown(h, 3) == 3
assert h.calls == small_calls, "same position, different array size -> same call count"
print("position 3 costs", small_calls, "calls in a 10-element array and in a 10^6-element array")

# seeded random check
for _ in range(500):
    a = sorted(rng.sample(range(-50, 200), rng.randint(0, 40)))
    t = rng.randint(-60, 210)
    assert search_unknown(Hidden(a), t) == brute(a, t)
print("random check passed: 500 cases")

# edge cases
assert search_unknown(Hidden([]), 5) == -1                      # get(0) already the sentinel
assert search_unknown(Hidden([1, 2, 3]), SENT) == -1            # target equal to the sentinel must not "match" it
assert search_unknown(Hidden([1, 2, 3]), -10 ** 9) == -1
assert search_unknown(Hidden([1, 2, 3]), 3) == 2
assert search_unknown(Hidden(list(range(5))), 0) == 0
print("edge asserts passed")
```

**Output (my run):**
```
[-1, 0, 3, 5, 9, 12] target 9 -> 4 | get calls: 5
[-1, 0, 3, 5, 9, 12] target 2 -> -1 | get calls: 4
[7] target 7 -> 0 | get calls: 2
[7] target 8 -> -1 | get calls: 3
exhaustive check passed for lengths 0..139, every target; calls <= 2*bit_length(p+2)+3 (min slack 2 )
n = 10^6, answer position 0: 2 get calls
n = 10^6, answer position 5: 7 get calls
n = 10^6, answer position 1000: 17 get calls
n = 10^6, answer position 999999: 40 get calls
position 3 costs 4 calls in a 10-element array and in a 10^6-element array
random check passed: 500 cases
edge asserts passed
```
All four examples in the prompt are correct. The bound `calls <= 2 * bit_length(p + 2) + 3` was asserted for every target (present and absent) on every length from 0 to 139; the smallest slack was 2.

**Edge cases:**
- Empty hidden array: get(0) is already the sentinel; returns -1.
- Target smaller than everything: window [0, 1], returns -1.
- Target beyond the last real element: doubling reaches the sentinel, binary search walks left, -1.
- Target equal to the sentinel: guarded, -1.
- Do not double from 0 (0 * 2 = 0, infinite loop); start `hi` at 1.

**Follow-ups:**
- *Why double instead of adding a constant?* A fixed step costs O(p / step) calls; doubling gives O(log p).
- *Could a factor of 3 be better?* Same big-O; the constant changes slightly.
- *Where else?* Unbounded searches such as finding a first True of an unbounded monotone predicate.

**Common mistakes:**
- Starting hi at 0.
- Treating the sentinel as a real element and returning its index.
- Binary searching `[0, 2147483647]` directly (31 calls, always, and the sentinel region wastes them).
- Letting the binary-search step read `get(hi)` again after doubling (an extra call for no reason; the closed loop already covers it).

### Q31 ⭐ 🟡 Floating-point binary search: iterations versus epsilon. Return the square root of a real x with 0 <= x <= 10^6 so that |result - sqrt(x)| <= 10^-6, using binary search on reals with `hi = max(1.0, x)` (explain why hi = x is wrong for x < 1). Implement it twice: with a fixed number of iterations (100) and with `while hi - lo > eps`, then show with an iteration cap that `eps = 1e-15` never terminates for x = 10**6 (the interval cannot shrink below one float spacing), and say why a fixed iteration count is the safer default and how many halvings are needed to reach a given tolerance. Example: x=2 -> within 1e-6 of 1.41421356; x=0.25 -> within 1e-6 of 0.5; x=0 -> within 1e-6 of 0; x=10**6 -> within 1e-6 of 1000.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a real-valued answer. The predicate `mid * mid <= x` is True then False as mid grows, so I shrink an interval instead of an index range.

**Say this first (1 line):** "Square root by halving [0, max(1, x)]: keep lo where lo*lo <= x, move hi otherwise. I loop a fixed 100 times, because an epsilon loop can stall once the interval hits float spacing."

**Brute force:** Step r = 0, 1e-6, 2e-6, ... until r*r > x. For x = 10^6 that is about 10^9 steps. Too slow. A closer cousin is Newton's method, but the question asks for binary search.

**Optimal:**
- `lo = 0.0`, `hi = max(1.0, x)`. Loop: `mid = (lo + hi) / 2`; if `mid*mid <= x` then `lo = mid` else `hi = mid`.
- Why `hi = max(1.0, x)`: sqrt(x) <= x only when x >= 1. For x = 0.25 the root is 0.5, which is larger than x, so `hi = x` throws the answer out of the interval. The code run below shows `hi = x` returns 0.25.
- Invariant: `lo*lo <= x` and (`hi*hi > x` or hi is the initial bound). The root stays inside [lo, hi].
- Each halving halves the width. Halvings needed = smallest h with width / 2^h <= tol. For width 10^6 and tol 1e-6 that is 40. For width 1 it is 20. So 100 iterations is far more than enough.
- Epsilon loop trap: floats near 1000 are spaced about 1.1e-13 apart. With `eps = 1e-15`, lo and hi become neighbouring floats, `mid` equals one of them, the interval stops shrinking, and `hi - lo > eps` is True forever.
- A fixed count cannot hang. I would use an epsilon loop only when I know eps is comfortably above the float spacing at the answer.

**Complexity:** Time O(log(width / tol)), about 40 halvings for this tolerance, or exactly 100 with the fixed version. Space O(1).

**Dry run:** x = 2, lo = 0, hi = 2.
| step | mid | mid*mid vs 2 | new interval |
|---|---|---|---|
| 1 | 1 | 1 <= 2 | [1, 2] |
| 2 | 1.5 | 2.25 > 2 | [1, 1.5] |
| 3 | 1.25 | 1.5625 <= 2 | [1.25, 1.5] |
| 4 | 1.375 | 1.89 <= 2 | [1.375, 1.5] |
| 5 | 1.4375 | 2.07 > 2 | [1.375, 1.4375] |

The width halves every step: 2, 1, 0.5, 0.25, ... It heads to 1.41421356.

**Code:**
```python
import math
import random


def sqrt_fixed(x, iters=100):
    lo, hi = 0.0, max(1.0, x)            # sqrt(x) <= max(1, x) for every x >= 0
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sqrt_eps(x, eps=1e-9, cap=10**6):
    # returns (answer, loops used); cap stops a non-terminating loop for the demo
    lo, hi = 0.0, max(1.0, x)
    loops = 0
    while hi - lo > eps and loops < cap:
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
        loops += 1
    return (lo + hi) / 2, loops


def sqrt_bad_hi(x, iters=100):
    lo, hi = 0.0, x                      # WRONG for x < 1: sqrt(x) > x
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def halvings(width, tol):
    # smallest h with width / 2**h <= tol
    h = 0
    while width / 2 ** h > tol:
        h += 1
    return h


# examples from the prompt
for x, want in [(2, 1.41421356), (0.25, 0.5), (0, 0.0), (10**6, 1000.0)]:
    assert abs(sqrt_fixed(x) - want) <= 1e-6
    assert abs(sqrt_eps(x, 1e-9)[0] - want) <= 1e-6
    print("x =", x, "fixed:", sqrt_fixed(x), " eps loop:", sqrt_eps(x, 1e-9))

# hi = x is wrong below 1
print("hi = x with x=0.25 gives", sqrt_bad_hi(0.25), "(true 0.5)")
assert abs(sqrt_bad_hi(0.25) - 0.5) > 0.2

# eps below float spacing never terminates
ans, loops = sqrt_eps(10**6, 1e-15, cap=10**6)
print("eps=1e-15, x=10**6: loops =", loops, "(hit the 10**6 cap)", " spacing near 1000:", math.ulp(1000.0))
assert loops == 10**6
ans2, loops2 = sqrt_eps(10**6, 1e-9)
print("eps=1e-9, x=10**6: loops =", loops2)
assert loops2 < 100

# halvings needed
print("halvings for width 10**6 to tol 1e-6:", halvings(10**6, 1e-6))
print("halvings for width 1 to tol 1e-6:", halvings(1, 1e-6))
assert halvings(10**6, 1e-6) == 40 and halvings(1, 1e-6) == 20

# seeded cross-check against math.sqrt, including x < 1
rng = random.Random(31)
worst = 0.0
for _ in range(2000):
    x = rng.choice([rng.random(), rng.uniform(0, 10), rng.uniform(0, 10**6), float(rng.randint(0, 10**6))])
    err = abs(sqrt_fixed(x) - math.sqrt(x))
    worst = max(worst, err)
    assert err <= 1e-6
    assert abs(sqrt_eps(x, 1e-9)[0] - math.sqrt(x)) <= 1e-6
print("2000 random x: worst error of fixed-100 version =", worst)
print("all checks passed")
```

**Output (my run):**
```text
x = 2 fixed: 1.414213562373095  eps loop: (1.4142135619185865, 31)
x = 0.25 fixed: 0.5  eps loop: (0.5000000004656613, 30)
x = 0 fixed: 3.944304526105059e-31  eps loop: (4.656612873077393e-10, 30)
x = 1000000 fixed: 1000.0  eps loop: (999.99999999989, 50)
hi = x with x=0.25 gives 0.25 (true 0.5)
eps=1e-15, x=10**6: loops = 1000000 (hit the 10**6 cap)  spacing near 1000: 1.1368683772161603e-13
eps=1e-9, x=10**6: loops = 50
halvings for width 10**6 to tol 1e-6: 40
halvings for width 1 to tol 1e-6: 20
2000 random x: worst error of fixed-100 version = 1.1368683772161603e-13
all checks passed
```

All four prompt examples are right. The `eps = 1e-9` loop took about 30 to 50 loops. The `eps = 1e-15` loop for x = 10^6 hit my 10^6-loop cap, which proves it would never end. Timings were not needed; the loop counts are the evidence.

**Edge cases:**
- x = 0: the answer is 0 (the fixed version returns about 4e-31, inside tolerance).
- 0 < x < 1: needs `hi = 1`. x = 1: root is 1, fine.
- Large x = 10^6: root 1000, the float spacing near the answer is about 1.1e-13, so asking for less than that is impossible.
- Negative x: out of range; I would raise an error.

**Follow-ups:**
- "How many iterations for tolerance t?" ceil(log2(width / t)). Width 10^6, t = 1e-6 gives 40.
- "Why not `x ** 0.5`?" It is fine in real life. The question tests the search pattern.
- "Can I compare floats with ==?" No. Use the predicate with `<=` and a bounded loop.

**Common mistakes:**
- `hi = x` for x < 1.
- `while hi - lo > eps` with eps smaller than the float spacing (infinite loop).
- Stopping at `lo == hi` or checking `mid*mid == x` for equality on floats.
- Returning `lo` after a short loop; the midpoint `(lo + hi) / 2` is closer.

---

### Q32 ⭐ 🟡 Integer k-th root. Given integers x (0 <= x <= 10^18) and n (1 <= n <= 60), return floor(x^(1/n)) exactly. Binary search the integer r in [0, x] (hi = x is fine; Python integers are unbounded) with the predicate r**n <= x using Python's big integers. Show why `int(x ** (1 / n))` is unsafe (it rounds toward a wrong integer on exact roots) and why the predicate should be computed in integers. Example: x=27, n=3 -> 3; x=125, n=3 -> 5 (the float expression int(125 ** (1/3)) gives 4); x=80, n=4 -> 2; x=10**18, n=2 -> 10**9; x=0, n=5 -> 0; x=1, n=60 -> 1.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on an integer answer with an exact integer predicate. The answer is the last r with `r**n <= x`.

**Say this first (1 line):** "Binary search r in [0, x] for the largest r with r**n <= x, using Python big integers so the test is exact; the float `x ** (1/n)` rounds wrongly on exact roots."

**Brute force:** Increase r from 0 while `(r + 1)**n <= x`. That is about x^(1/n) steps, which is 10^9 for x = 10^18 and n = 2. Fine as a checker on small x only.

**Optimal:**
- `lo, hi = 0, x`. The predicate `r**n <= x` is True...True False...False, because r**n grows with r (n >= 1).
- I want the LAST True, so I use the upper middle: `mid = (lo + hi + 1) // 2`. If `mid**n <= x`, set `lo = mid`, else `hi = mid - 1`. With the lower middle the loop would not progress when `hi = lo + 1`.
- `hi = x` is safe in Python: no overflow, and r**n for r up to 10^18 and n = 60 is a number of about 1,000 digits, which is still cheap.
- Invariant: `lo**n <= x`, and every value above `hi` fails.
- Why floats fail: 125 ** (1/3) is 4.999999999999999 (the exponent 1/3 is not exact), so `int()` gives 4. My run found 888 exact roots r**n (n = 2..8, r < 300) where the float shortcut is wrong. It can also be wrong between roots: for x = 10^18 - 1 and n = 2, `x ** 0.5` becomes 1e9 but the exact answer is 999999999, because x itself rounds to 1e18 as a float.
- Speed-up (optional): start with `hi = 1 << (x.bit_length() // n + 1)`, which cuts the iterations from about 60 to about log2(root). Not needed here.

**Complexity:** About log2(x) <= 60 iterations; each computes `mid**n` on integers of up to ~n*60 bits. Time O(log x * M(n log x)), in plain words about 60 big-int powers. Space O(1) extra, aside from the big temporary.

**Dry run:** x = 80, n = 4, lo = 0, hi = 80.
| mid | mid**4 vs 80 | next |
|---|---|---|
| 40 | far above | hi = 39 |
| 20 | 160000 > 80 | hi = 19 |
| 10 | 10000 > 80 | hi = 9 |
| 5 | 625 > 80 | hi = 4 |
| 2 (lo=0, hi=4, mid=(0+4+1)//2) | 16 <= 80 | lo = 2 |
| 3 | 81 > 80 | hi = 2 |

lo == hi == 2, so the answer is 2.

**Code:**
```python
import random


def kth_root(x, n):
    lo, hi = 0, x                        # predicate r**n <= x is True...True False...False; find the last True
    while lo < hi:
        mid = (lo + hi + 1) // 2         # upper mid so the loop makes progress
        if mid ** n <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def kth_root_brute(x, n):
    r = 0
    while (r + 1) ** n <= x:
        r += 1
    return r


# prompt examples
for x, n, want in [(27, 3, 3), (125, 3, 5), (80, 4, 2), (10**18, 2, 10**9), (0, 5, 0), (1, 60, 1)]:
    assert kth_root(x, n) == want, (x, n)
    print("x =", x, "n =", n, "->", kth_root(x, n))
print("float 125 ** (1/3) =", 125 ** (1 / 3), "-> int() gives", int(125 ** (1 / 3)))
assert int(125 ** (1 / 3)) == 4

# how often is the float shortcut wrong on exact roots r**n?
bad = [(r, n) for n in range(2, 9) for r in range(1, 300) if int((r ** n) ** (1 / n)) != r]
print("exact roots r**n (n=2..8, r<300) where int(x ** (1/n)) is wrong:", len(bad), "e.g.", bad[:5])
assert (5, 3) in bad
# and it can be wrong off exact roots at large x
x = 10**18 - 1
print("float root of 10**18-1 (n=2):", int(x ** 0.5), "exact:", kth_root(x, 2))

# seeded cross-check
rng = random.Random(32)
for _ in range(600):
    n = rng.randint(1, 8)
    x = rng.randint(0, 5000)
    assert kth_root(x, n) == kth_root_brute(x, n), (x, n)
# exhaustive for small x and n
for n in range(1, 7):
    for x in range(0, 400):
        assert kth_root(x, n) == kth_root_brute(x, n)
# exact-boundary property on big values
for _ in range(300):
    n = rng.randint(1, 60)
    x = rng.randint(0, 10**18)
    r = kth_root(x, n)
    assert r ** n <= x < (r + 1) ** n
for n in range(1, 61):
    for r in (1, 2, 3, 7):
        assert kth_root(r ** n, n) == r and kth_root(r ** n - 1, n) == r - 1
# edge asserts
assert kth_root(0, 1) == 0 and kth_root(1, 1) == 1 and kth_root(10**18, 1) == 10**18
assert kth_root(10**18, 60) == 1      # 2**60 = 1.15e18 > 1e18, so only 1 fits
print("all checks passed")
```

**Output (my run):**
```text
x = 27 n = 3 -> 3
x = 125 n = 3 -> 5
x = 80 n = 4 -> 2
x = 1000000000000000000 n = 2 -> 1000000000
x = 0 n = 5 -> 0
x = 1 n = 60 -> 1
float 125 ** (1/3) = 4.999999999999999 -> int() gives 4
exact roots r**n (n=2..8, r<300) where int(x ** (1/n)) is wrong: 888 e.g. [(4, 3), (5, 3), (6, 3), (7, 3), (8, 3)]
float root of 10**18-1 (n=2): 1000000000 exact: 999999999
all checks passed
```

All six prompt examples match. The exhaustive check covers every x < 400 for n = 1..6. The boundary check shows `kth_root(r**n) == r` and `kth_root(r**n - 1) == r - 1` for n = 1..60.

**Edge cases:**
- x = 0: lo = hi = 0, returns 0. x = 1: returns 1 for any n.
- n = 1: the answer is x itself (the search still works).
- x < 2^n (such as 10^18 with n = 60): the root is 1.
- Perfect powers and their predecessors: tested above.

**Follow-ups:**
- "Can I use `round(x ** (1/n))` and correct it?" Yes: take that guess g, then fix it with `while g**n > x: g -= 1` and `while (g+1)**n <= x: g += 1`. It works, but the search is easier to prove.
- "What about floats x?" Then it is the real-valued search from Q31.
- "Is `**` exact on ints?" Yes, Python ints are unbounded.

**Common mistakes:**
- `int(x ** (1 / n))` with floats.
- Using the lower middle when searching for the last True (infinite loop).
- Restricting `hi` to something like `x // 2` and breaking x = 0 or x = 1.

---

### Q33 ⭐ 🟡 Designing and proving a monotone predicate. Binary search on the answer needs a predicate that is False...False True...True (or the reverse) over the whole search range. For each of two candidate predicates decide whether it is monotone and justify it, and for any that is not, give a concrete counterexample: (a) 'with capacity c the packages [1,2,3] take EXACTLY 2 days under greedy loading (False when a package exceeds c)', over c = 1..7; (b) 'some subarray of length L has sum >= 10' for arr=[5,-10,5,5] over L = 1..4, versus the same predicate on a list of non-negative numbers. Show how to restate (a) as 'at most 2 days' to make it monotone. Example: (a) with the rule that a capacity below the heaviest package is False, outputs for c=1..7 -> [False, False, True, True, True, False, False] (c=3..5 take 2 days, c>=6 take 1); (b) for arr=[5,-10,5,5] -> [False, True, False, False]. (For a monotone length predicate that does work, see Part 3 Q40.)
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Monotone predicate design for binary search on the answer. The search is only valid when the predicate flips once.

**Say this first (1 line):** "A predicate is searchable only if moving the parameter in one direction can never undo a True; 'exactly 2 days' fails that, 'at most 2 days' passes, and a subarray-sum test fails with negatives."

**Brute force:** Evaluate the predicate at every parameter value and check that the list has at most one flip. That is my monotonicity test, and I use it as a checker (exhaustive on small inputs).

**Optimal:** Decide by reasoning, then confirm by counterexample.
- (a) "Exactly 2 days" with greedy loading. Days by capacity for [1,2,3] are None, None, 2, 2, 2, 1, 1 for c = 1..7. Exactly-2 gives [F, F, T, T, T, F, F]: True then False, and the left False is the "too small" case. Not monotone. Counterexample: c = 5 is True, c = 6 is False, yet 6 > 5 means a looser limit.
- Why it breaks: more capacity can only lower the day count (never raise it), so the day count passes THROUGH 2 and keeps falling to 1. "Equal to" cannot be a threshold.
- Fix: "at most 2 days", i.e. `days(c) <= 2` with False for c below the heaviest package. That gives [F, F, T, T, T, T, T]. Reason: greedy days are non-increasing in c (a larger bin never needs more bins), and "non-increasing <= 2" is True from some point on. I checked this over 6,372 small (weights, d) cases.
- (b) "Some subarray of length L has sum >= 10" for [5, -10, 5, 5]: L = 1..4 gives [F, T, F, F]. Not monotone. Counterexample: L = 2 is True (the last two elements, 5 + 5 = 10) and L = 3 is False, because every length-3 window contains the -10.
- With non-negative numbers it IS monotone: a window of length L with sum >= T can be extended by one neighbour that adds >= 0, so L + 1 also works (when L < n). That is why the prefix-sum length search works in Part 3 Q40's setting.
- Rule: write the predicate as "answer <= p" or "answer >= p" (a threshold), not "answer == p".

**Complexity:** Each predicate evaluation here is O(n) (greedy loading pass, or window sums). Checking monotonicity by brute force costs the number of parameter values times that. For the search itself: O(n log range) once the predicate is monotone.

**Dry run:** Packages [1, 2, 3], c = 5: load 1, 2 (sum 3), adding 3 would give 6 > 5, so start day 2 with 3. Days = 2, so exactly-2 is True. c = 6: 1 + 2 + 3 = 6 fits, one day, so exactly-2 is False, but at-most-2 is True. For (b), L = 2 windows: [5, -10] = -5, [-10, 5] = -5, [5, 5] = 10, so True. L = 3: [5, -10, 5] = 0, [-10, 5, 5] = 0, so False.

**Code:**
```python
import random
from itertools import product


def days_needed(weights, c):
    # greedy loading in order; None when a package is heavier than c
    if any(w > c for w in weights):
        return None
    days, load = 1, 0
    for w in weights:
        if load + w > c:
            days += 1
            load = 0
        load += w
    return days


def pred_exact(weights, d, c):
    return days_needed(weights, c) == d


def pred_atmost(weights, d, c):
    t = days_needed(weights, c)
    return t is not None and t <= d


def has_sub_sum(arr, L, target):
    return any(sum(arr[i:i + L]) >= target for i in range(len(arr) - L + 1))


def is_monotone(seq):
    # True...True/False...False in either direction: at most one flip
    return sum(1 for a, b in zip(seq, seq[1:]) if a != b) <= 1


w = [1, 2, 3]
a = [pred_exact(w, 2, c) for c in range(1, 8)]
print("(a) exactly 2 days, c=1..7:", a, " monotone?", is_monotone(a))
assert a == [False, False, True, True, True, False, False]
print("    days by capacity:", [days_needed(w, c) for c in range(1, 8)])
a2 = [pred_atmost(w, 2, c) for c in range(1, 8)]
print("(a) at most 2 days, c=1..7:", a2, " monotone?", is_monotone(a2))
assert a2 == [False, False, True, True, True, True, True]

arr = [5, -10, 5, 5]
b = [has_sub_sum(arr, L, 10) for L in range(1, 5)]
print("(b) arr=[5,-10,5,5], L=1..4:", b, " monotone?", is_monotone(b))
assert b == [False, True, False, False]

# at-most-d predicate is monotone in c: exhaustive over small package lists
checked = 0
for n in range(1, 6):
    for ws in product(range(1, 5), repeat=n):
        for d in range(1, n + 1):
            seq = [pred_atmost(list(ws), d, c) for c in range(1, sum(ws) + 2)]
            assert is_monotone(seq) and (not seq or seq[-1]), (ws, d)
            checked += 1
print("at-most-d monotone in capacity: checked", checked, "(weights, d) cases")

# how often is the exact-d predicate NOT monotone? (random seeded)
rng = random.Random(33)
nonmono = 0
for _ in range(500):
    ws = [rng.randint(1, 6) for _ in range(rng.randint(2, 6))]
    d = rng.randint(1, len(ws))
    seq = [pred_exact(ws, d, c) for c in range(1, sum(ws) + 2)]
    nonmono += not is_monotone(seq)
print("exact-d predicate non-monotone in", nonmono, "of 500 random cases")
assert nonmono > 0

# (b) non-negative lists: 'some window of length L has sum >= T' is monotone in L (exhaustive small)
cnt = 0
for n in range(1, 6):
    for xs in product(range(0, 4), repeat=n):
        for T in range(0, 12):
            seq = [has_sub_sum(list(xs), L, T) for L in range(1, n + 1)]
            # larger L can only add non-negative amounts to a best window, so once True stays True
            assert all(not (a and not b) for a, b in zip(seq, seq[1:])), (xs, T)
            cnt += 1
print("non-negative: once True stays True for larger L, checked", cnt, "cases")
# with negatives it fails
neg_fail = 0
for _ in range(500):
    xs = [rng.randint(-5, 5) for _ in range(rng.randint(2, 6))]
    T = rng.randint(1, 6)
    seq = [has_sub_sum(xs, L, T) for L in range(1, len(xs) + 1)]
    neg_fail += any(a and not b for a, b in zip(seq, seq[1:]))
print("with negatives, True then False happened in", neg_fail, "of 500 random cases")
assert neg_fail > 0
print("all checks passed")
```

**Output (my run):**
```text
(a) exactly 2 days, c=1..7: [False, False, True, True, True, False, False]  monotone? False
    days by capacity: [None, None, 2, 2, 2, 1, 1]
(a) at most 2 days, c=1..7: [False, False, True, True, True, True, True]  monotone? True
(b) arr=[5,-10,5,5], L=1..4: [False, True, False, False]  monotone? False
at-most-d monotone in capacity: checked 6372 (weights, d) cases
exact-d predicate non-monotone in 279 of 500 random cases
non-negative: once True stays True for larger L, checked 16368 cases
with negatives, True then False happened in 172 of 500 random cases
all checks passed
```

Both prompt example lists are right as given: (a) [F, F, T, T, T, F, F] (with c < heaviest False) and (b) [F, T, F, F]. In 279 of 500 random package lists the exact-d predicate was not monotone, and with negatives, True-then-False appeared in 172 of 500 random lists.

**Edge cases:**
- Capacity below the heaviest package: define the predicate as False (no valid loading), so the False region starts at the left.
- d >= number of packages: at-most-d is True from c = heaviest.
- All-negative or zero-sum lists in (b): with target 10 everything is False, trivially monotone.
- A single flip may be True...False, so say which direction you search.

**Follow-ups:**
- "How do I prove monotone in an interview?" Give the exchange or extension argument: a solution for the stricter parameter also works for the looser one.
- "What if I need exactly k?" Search for the smallest c with at-most-k days; the exact count can then be adjusted separately.
- "Does the same trap appear elsewhere?" Yes: "is there a split with sum exactly S" is not a threshold; "largest part <= S" is.

**Common mistakes:**
- Using `==` in the predicate.
- Forgetting the infeasible region (c below the heaviest package).
- Assuming a sliding "length" predicate is monotone when values can be negative.
- Believing a True once found on a non-monotone predicate means every larger value works.

---

### Q34 ⭐ 🟡 K-th missing positive number: search on index versus on value. `arr` is a strictly increasing list of positive integers (1 <= len <= 1000) and k >= 1. Return the k-th positive integer that is not in arr. The count of missing positives before arr[i] is arr[i] - (i + 1), which is non-decreasing in i, so binary search the INDEX of the first i where that count >= k; the answer is then k + i (with i = len(arr) when none). Contrast this with searching over the VALUE range [1, arr[-1] + k] using the predicate 'missing positives <= v is >= k', and say which has fewer lines and which generalises. Example: [2,3,4,7,11], k=5 -> 9; [1,2,3,4], k=2 -> 6; [5,6], k=1 -> 1; [1,3], k=1 -> 2; [2], k=3 -> 4.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a derived non-decreasing array (missing count before each index), or on the value range with a counting predicate.

**Say this first (1 line):** "Before arr[i] there are arr[i] - (i + 1) missing positives, which never decreases, so I find the first index where that reaches k and the answer is k + i."

**Brute force:** Walk v = 1, 2, 3, ... using a set of arr, count the numbers not in the set, stop at the k-th. O(len + answer), where the answer can be up to arr[-1] + k.

**Optimal (index search):**
- `missing(i) = arr[i] - (i + 1)`. Strictly increasing arr means each step raises arr[i] by at least 1, so missing(i) is non-decreasing.
- Find the smallest i with `missing(i) >= k` (`lo = 0, hi = len(arr)`, `hi = len` meaning none). The k-th missing number is then before arr[i] and after arr[i-1].
- Answer is `k + i`. Why: among the numbers 1..answer there are exactly i array elements (those before index i), so answer - i of them are missing, and the k-th missing means answer - i = k.
- If no index qualifies, i = len(arr) and the answer is k + len(arr), past the end.

**Optimal (value search):** Search v in [1, arr[-1] + k] for the smallest v with `v - (count of arr <= v) >= k`. The counting uses an inner bisect, so it is O(log^2) unless you do it carefully.

**Which is better:** The index search is shorter (no inner count) and O(log n). The value search generalises: it works when the predicate is a count over values (multiplication table, pair distances) and there is no tidy per-index formula. Say both in an interview.

**Complexity:** Index search: time O(log n), space O(1). Value search: O(log(arr[-1] + k) * log n), space O(1).

**Dry run:** arr = [2, 3, 4, 7, 11], k = 5. missing(i) = 1, 1, 1, 3, 6.
| lo | hi | mid | missing(mid) | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 1 < 5 | lo = 3 |
| 3 | 5 | 4 | 6 >= 5 | hi = 4 |
| 3 | 4 | 3 | 3 < 5 | lo = 4 |

i = 4, answer = 5 + 4 = 9. Check: the missing numbers are 1, 5, 6, 8, 9, so the 5th is 9.

**Code:**
```python
import random


def kth_missing_index(arr, k):
    # first index i with arr[i] - (i + 1) >= k; answer k + i
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) >= k:
            hi = mid
        else:
            lo = mid + 1
    return k + lo


def kth_missing_value(arr, k):
    # smallest v with (missing positives <= v) >= k; missing(v) = v - (count of arr <= v)
    def missing_upto(v):
        # count of arr elements <= v by binary search
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= v:
                lo = mid + 1
            else:
                hi = mid
        return v - lo
    lo, hi = 1, arr[-1] + k
    while lo < hi:
        mid = (lo + hi) // 2
        if missing_upto(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_missing_brute(arr, k):
    s, v = set(arr), 0
    while k:
        v += 1
        if v not in s:
            k -= 1
    return v


for arr, k, want in [([2, 3, 4, 7, 11], 5, 9), ([1, 2, 3, 4], 2, 6), ([5, 6], 1, 1), ([1, 3], 1, 2), ([2], 3, 4)]:
    got = (kth_missing_index(arr, k), kth_missing_value(arr, k), kth_missing_brute(arr, k))
    print(arr, "k =", k, "-> index search, value search, brute:", got)
    assert got == (want, want, want)

rng = random.Random(34)
for _ in range(1500):
    n = rng.randint(1, 12)
    arr = sorted(rng.sample(range(1, 30), n))
    k = rng.randint(1, 40)
    b = kth_missing_brute(arr, k)
    assert kth_missing_index(arr, k) == b == kth_missing_value(arr, k), (arr, k)
# exhaustive: every strictly increasing list from 1..8, k = 1..12
from itertools import combinations
cnt = 0
for n in range(1, 9):
    for arr in combinations(range(1, 9), n):
        for k in range(1, 13):
            assert kth_missing_index(list(arr), k) == kth_missing_brute(list(arr), k)
            cnt += 1
print("exhaustive cases checked:", cnt)
# edge asserts
assert kth_missing_index([1], 1) == 2          # nothing missing before arr[0]
assert kth_missing_index([1000], 1) == 1       # missing count before first element is 999
assert kth_missing_index([1000], 999) == 999
assert kth_missing_index([1000], 1000) == 1001 # past the end
print("all checks passed")
```

**Output (my run):**
```text
[2, 3, 4, 7, 11] k = 5 -> index search, value search, brute: (9, 9, 9)
[1, 2, 3, 4] k = 2 -> index search, value search, brute: (6, 6, 6)
[5, 6] k = 1 -> index search, value search, brute: (1, 1, 1)
[1, 3] k = 1 -> index search, value search, brute: (2, 2, 2)
[2] k = 3 -> index search, value search, brute: (4, 4, 4)
exhaustive cases checked: 3060
all checks passed
```

All five prompt examples are right and the three methods agree. I also ran every strictly increasing list drawn from 1..8 against k = 1..12 (3,060 cases).

**Edge cases:**
- arr[0] = 1: nothing missing before it (missing(0) = 0).
- arr[0] large: [1000] with k = 1 gives 1.
- k beyond the last element: [1000] with k = 1000 gives 1001.
- Length 1, k = 1: still correct.

**Follow-ups:**
- "What if arr may have duplicates?" The formula breaks. Deduplicate first, or use the value search with a count of distinct values.
- "What if the list is not sorted?" Sort it or use a set; no binary search then.
- "What if arr is huge and k small?" Index search stays O(log n).

**Common mistakes:**
- Using `arr[i] - i` instead of `arr[i] - (i + 1)`.
- Returning `arr[lo - 1] + (k - missing(lo - 1))` and mishandling lo = 0.
- Forgetting the past-the-end case.

---

### Q35 ⭐ 🔴 K-th smallest element of two sorted arrays in O(log(min(m, n))). `a` and `b` are sorted ascending (not both empty), and k is 1-based with 1 <= k <= len(a) + len(b); k counts duplicates. Binary search how many elements i come from `a` (and k - i from `b`) so that the cut is consistent: a[i-1] <= b[k-i] and b[k-i-1] <= a[i]. Say how this generalises the median-of-two-arrays cut and why the merge walk is only O(k). (The merge-walk baseline is Part 2 Q40.) Example: a=[1,3,8], b=[2,4,6,9], k=4 -> 4; a=[1,2], b=[1,2], k=3 -> 2; a=[], b=[3,5], k=2 -> 5; a=[7], b=[1,2,3], k=1 -> 1; a=[7], b=[1,2,3], k=4 -> 7.
**Asked at:** Median-of-two-sorted-arrays pages (techinterview.org 'binary search's nastiest cousin' page saying the O(m+n) merge is the usual first answer and O(log) is the expected follow-up, educative.io grokking page, a jointaro page with a company filter; snippets only, not opened; no company report verified) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports
**Pattern:** Binary search on a partition point (how many of the k smallest come from `a`). It is the median-of-two-arrays idea with a free k.

**Say this first (1 line):** "Pick i elements from a and k - i from b so everything on the left is <= everything on the right; binary search i, and the k-th is the larger of the two left boundaries."

**Brute force:** Merge both lists and take the k-th. Sorting the concatenation is O((m + n) log(m + n)); the merge walk stops after k steps, O(k) (Part 2 Q40 is the merge-walk baseline). With k near the middle of two million values that is a million steps.

**Optimal:**
- The k smallest form a prefix of `a` of length i and a prefix of `b` of length j = k - i.
- Valid i satisfies `a[i-1] <= b[j]` and `b[j-1] <= a[i]` (missing neighbours count as infinity or minus infinity).
- Range: `lo = max(0, k - n)` (we cannot take more than n from b), `hi = min(k, m)`.
- While lo < hi: `i = (lo + hi) // 2`, `j = k - i`. If `a[i] < b[j-1]`, then a[i] belongs among the k smallest, so take more from a: `lo = i + 1`. Else `hi = i`.
- Why indexes are safe: i < hi <= m so a[i] exists; i < hi <= k so j >= 1; j <= k - lo <= n so b[j-1] exists.
- Answer: `max(a[i-1] if i else -inf, b[j-1] if j else -inf)`.
- Invariant: the correct cut lies in [lo, hi]. Duplicates are fine because the tests use `<` on one side and `<=` implicitly on the other.
- It generalises the median: the median is k = (m + n + 1) // 2 (and for even totals, also k + 1).

**Complexity:** Time O(log(min(m, n, k))): the search range is at most min(k, m) - max(0, k - n), no bigger than min(m, n). Space O(1). The merge walk is O(k).

**Dry run:** a = [1, 3, 8], b = [2, 4, 6, 9], k = 4. lo = 0, hi = 3.
| lo | hi | i | j | test | action |
|---|---|---|---|---|---|
| 0 | 3 | 1 | 3 | a[1] = 3 < b[2] = 6 | lo = 2 |
| 2 | 3 | 2 | 2 | a[2] = 8 < b[1] = 4? no | hi = 2 |

i = 2, j = 2: left parts are [1, 3] and [2, 4]. The larger boundary is max(a[1], b[1]) = max(3, 4) = 4. The merged order 1, 2, 3, 4, ... agrees.

**Code:**
```python
import random


def kth_two(a, b, k):
    m, n = len(a), len(b)
    lo, hi = max(0, k - n), min(k, m)      # i = how many of the k smallest come from a
    while lo < hi:
        i = (lo + hi) // 2
        j = k - i
        # i < hi <= m so a[i] exists; i < hi <= k so j >= 1; j <= k - lo <= n so b[j-1] exists
        if a[i] < b[j - 1]:
            lo = i + 1                      # a[i] must be among the k smallest: take more from a
        else:
            hi = i
    i, j = lo, k - lo
    left = []
    if i > 0:
        left.append(a[i - 1])
    if j > 0:
        left.append(b[j - 1])
    return max(left)


def kth_merge(a, b, k):
    # O(k) merge walk (Part 2 Q40 style)
    i = j = 0
    for _ in range(k):
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            v = a[i]; i += 1
        else:
            v = b[j]; j += 1
    return v


def kth_sorted(a, b, k):
    return sorted(a + b)[k - 1]


for a, b, k, want in [([1, 3, 8], [2, 4, 6, 9], 4, 4), ([1, 2], [1, 2], 3, 2), ([], [3, 5], 2, 5),
                      ([7], [1, 2, 3], 1, 1), ([7], [1, 2, 3], 4, 7)]:
    got = (kth_two(a, b, k), kth_merge(a, b, k), kth_sorted(a, b, k))
    print(a, b, "k =", k, "->", got)
    assert got == (want,) * 3

rng = random.Random(35)
cases = 0
for _ in range(4000):
    a = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 7)))
    b = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 7)))
    if not a and not b:
        continue
    for k in range(1, len(a) + len(b) + 1):
        assert kth_two(a, b, k) == kth_sorted(a, b, k), (a, b, k)
        cases += 1
print("random (a, b, k) cases checked:", cases)

# median from k-th (ties with duplicates included)
a, b = [1, 3], [2]
tot = len(a) + len(b)
assert kth_two(a, b, (tot + 1) // 2) == 2
# edges: one side empty, all equal, k = total, disjoint ranges
assert kth_two([], [5], 1) == 5 and kth_two([5], [], 1) == 5
assert kth_two([4, 4, 4], [4, 4], 5) == 4
assert kth_two([1, 2], [10, 11], 4) == 11 and kth_two([10, 11], [1, 2], 1) == 1
# big input: the search takes about 20 steps, not 10**6
big_a = list(range(0, 2 * 10**6, 2))
big_b = list(range(1, 2 * 10**6, 2))
assert kth_two(big_a, big_b, 10**6) == 10**6 - 1
print("all checks passed")
```

**Output (my run):**
```text
[1, 3, 8] [2, 4, 6, 9] k = 4 -> (4, 4, 4)
[1, 2] [1, 2] k = 3 -> (2, 2, 2)
[] [3, 5] k = 2 -> (5, 5, 5)
[7] [1, 2, 3] k = 1 -> (1, 1, 1)
[7] [1, 2, 3] k = 4 -> (7, 7, 7)
random (a, b, k) cases checked: 27983
all checks passed
```

All five prompt examples pass. The random check covers 27,983 (a, b, k) triples with duplicates and empty sides, each k from 1 to the total, against sorted concatenation.

**Edge cases:**
- One list empty: the range collapses (an empty `a` gives hi = 0, so i = 0), and the answer is the k-th of the other.
- k = 1: the minimum of the two heads. k = m + n: the overall maximum.
- All equal values: any cut works; the max of boundaries is the same value.
- Disjoint ranges: i is 0 or m.

**Follow-ups:**
- "How do I get the median?" k-th with k = (m + n + 1) // 2; for an even total average it with the (k + 1)-th.
- "Other approach?" Discard k/2 elements from one list each round (compare a[k/2 - 1] and b[k/2 - 1]), also O(log k).
- "Why search the shorter list?" It keeps the range small. Here the range is already clipped by `lo` and `hi`.

**Common mistakes:**
- Not clipping the range, so i or k - i falls outside a list.
- Off-by-one between 0-based indices and 1-based k.
- Treating missing neighbours as 0 instead of infinities (bad with negative numbers).

---

### Q36 ⭐ 🔴 Maximum average of a subarray with length at least k (binary search on a real answer). `nums` has 1 <= k <= len <= 10^4 integers (values may be negative). Return the largest average over all contiguous subarrays of length >= k, within 10^-5. Binary search the average t: a subarray of length >= k has average >= t iff after subtracting t from every element some such subarray has sum >= 0, checked with prefix sums and the minimum prefix seen so far at least k positions back. State the search range [min(nums), max(nums)], an iteration count that reaches 10^-5, and why 'some average >= t exists' is monotone in t. Example: [1,12,-5,-6,50,3], k=4 -> 12.75; [5], k=1 -> 5.0; [-3,-1,-2], k=2 -> -1.5; [0,4,0,3,2], k=1 -> 4.0.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a real answer with a feasibility check: "does some subarray of length >= k average at least t?"

**Say this first (1 line):** "Guess the average t, subtract it from every element, and ask whether some subarray of length >= k has sum >= 0; that test is monotone in t, so I search t between min and max."

**Brute force:** Try every subarray of length >= k with prefix sums, tracking the best sum / length. O(n^2) time. I use exact fractions to build my checker.

**Optimal:**
- Predicate `feasible(t)`: an average >= t exists iff some window of length >= k has `sum(x - t) >= 0`.
- Build prefix sums `P` of `x - t`. For each end index i >= k, the best start is the one with the smallest `P[j]` for j <= i - k. Keep `best_min` as a running minimum of `P[i - k]`. If `P[i] - best_min >= 0`, return True. That is O(n).
- Monotone in t: if a window has average >= t, it also has average >= any smaller t. So feasible is True for small t and False for large t. I checked this on 300 random lists over a grid of t.
- Range: `lo = min(nums)`, `hi = max(nums)`. Every average lies between them, so the answer does too.
- Move: if feasible(mid), `lo = mid` (try higher), else `hi = mid`.
- Iterations: if values are within +-10^4, the width is at most 2*10^4 and 31 halvings reach 1e-5. I use a fixed 50 (width up to about 10^10 at that tolerance).
- Note: the prompt gives no value bound, so state the assumption; a fixed 100 is a safe default.

**Complexity:** Time O(n log(range / tol)) (n per check, about 50 checks). Space O(n) for the prefix array (O(1) is possible by keeping two running prefix sums, one lagging k behind). Floating-point error is tiny at this scale (worst seen 3.6e-14).

**Dry run:** nums = [1, 12, -5, -6, 50, 3], k = 4.
- t = 12: x - t = -11, 0, -17, -18, 38, -9; prefix 0, -11, -11, -28, -46, -8, -17. At i = 5, best_min = min(P0, P1) = -11 and P5 - (-11) = 3 >= 0. Feasible.
- t = 13: prefix 0, -12, -13, -31, -50, -13, -23. At i = 5, best_min = -12 and P5 + 12 = -1. At i = 6, best_min = -13, P6 + 13 = -10. Not feasible.
So the answer is between 12 and 13. The exact value is 12.75 (window [12, -5, -6, 50], 51 / 4).

**Code:**
```python
import random
from fractions import Fraction


def feasible(nums, k, t):
    # some subarray of length >= k has average >= t  <=>  some such subarray has sum(x - t) >= 0
    pre = [0.0]
    for x in nums:
        pre.append(pre[-1] + (x - t))
    best_min = float("inf")
    for i in range(k, len(pre)):
        best_min = min(best_min, pre[i - k])     # smallest prefix at least k back
        if pre[i] - best_min >= 0:
            return True
    return False


def max_avg(nums, k, iters=50):
    lo, hi = float(min(nums)), float(max(nums))
    for _ in range(iters):
        mid = (lo + hi) / 2
        if feasible(nums, k, mid):
            lo = mid                              # t is achievable, try higher
        else:
            hi = mid
    return lo


def max_avg_brute(nums, k):
    best = None
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if j - i + 1 >= k:
                v = Fraction(s, j - i + 1)
                if best is None or v > best:
                    best = v
    return best


for nums, k, want in [([1, 12, -5, -6, 50, 3], 4, 12.75), ([5], 1, 5.0), ([-3, -1, -2], 2, -1.5), ([0, 4, 0, 3, 2], 1, 4.0)]:
    got = max_avg(nums, k)
    print(nums, "k =", k, "->", round(got, 6), " brute:", float(max_avg_brute(nums, k)))
    assert abs(got - want) <= 1e-5 and float(max_avg_brute(nums, k)) == want

rng = random.Random(36)
worst = 0.0
for _ in range(1500):
    n = rng.randint(1, 10)
    nums = [rng.randint(-20, 20) for _ in range(n)]
    k = rng.randint(1, n)
    err = abs(max_avg(nums, k) - float(max_avg_brute(nums, k)))
    worst = max(worst, err)
    assert err <= 1e-5, (nums, k)
print("random cases: worst error =", worst)

# monotone in t: exhaustive over a grid of t for small lists
for _ in range(300):
    nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 8))]
    k = rng.randint(1, len(nums))
    seq = [feasible(nums, k, t / 4) for t in range(-40, 41)]
    assert all(not (not a and b) for a, b in zip(seq, seq[1:])), (nums, k)   # True then False only
# iterations needed: width 2*10**4 down to 1e-5
w, it = 2 * 10**4, 0
while w > 1e-5:
    w /= 2; it += 1
print("halvings from width 2*10**4 to 1e-5:", it)
assert it == 31
# edge asserts
assert abs(max_avg([7, 7, 7], 2) - 7.0) <= 1e-5            # all equal: lo == hi from the start
assert abs(max_avg([-5], 1) - (-5.0)) <= 1e-5
assert abs(max_avg([1, 2, 3, 4], 4) - 2.5) <= 1e-5          # k = n: only the whole array
print("all checks passed")
```

**Output (my run):**
```text
[1, 12, -5, -6, 50, 3] k = 4 -> 12.75  brute: 12.75
[5] k = 1 -> 5.0  brute: 5.0
[-3, -1, -2] k = 2 -> -1.5  brute: -1.5
[0, 4, 0, 3, 2] k = 1 -> 4.0  brute: 4.0
random cases: worst error = 3.552713678800501e-14
halvings from width 2*10**4 to 1e-5: 31
all checks passed
```

All four prompt examples match the exact-fraction brute force. The 1,500 seeded random lists had worst error 3.6e-14, well under 1e-5.

**Edge cases:**
- k = len(nums): only the whole array, answer is its mean.
- Single element: that element, even if negative.
- All equal: lo = hi after the search, answer is that value.
- Negative values: the range [min, max] still holds; the prefix test handles them.

**Follow-ups:**
- "Can the exact answer be found?" The optimum is always some integer ratio sum / length, so you can finish with an exact check, or compare Fractions.
- "What if k = 1?" The answer is simply max(nums), no search needed.
- "Why not sliding window?" The best window is not forced to have length k, and longer windows can win; a fixed-size window misses them.

**Common mistakes:**
- Using only windows of length exactly k.
- Using prefix `P[i - k + 1]` (off by one) or the global minimum prefix (allows windows shorter than k).
- Searching an integer range and returning an integer.
- Tolerance compare with == on floats.

---

### Q37 ⭐ 🔴 Median of a row-sorted matrix. `matrix` is r x c with r and c both odd positive integers (so r*c is odd), each row sorted ascending, no relation between rows, values up to 10^9, r*c <= 10^6. Return the median of all elements in O(r log c log(range)): binary search the VALUE v and count elements <= v per row with `bisect_right`, then return the smallest v with count >= (r*c + 1) // 2. Explain why that v is an actual entry and why the matrix cannot simply be flattened and bisected. Example: [[1,3,5],[2,6,9],[3,6,9]] -> 5; [[1]] -> 1; [[1,1,1],[2,2,2],[3,3,3]] -> 2.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on the value range, with a monotone count: `count(<= v)` over rows, using `bisect_right` per row.

**Say this first (1 line):** "The matrix is not globally sorted, so I search the value v, count entries <= v row by row with bisect_right, and return the smallest v whose count reaches the middle rank."

**Brute force:** Flatten, sort, take element `len // 2`. O(rc log(rc)) time and O(rc) space. It is my checker.

**Optimal:**
- Middle rank `need = (r*c + 1) // 2`. With r*c odd, this is the 1-based position of the median.
- `lo = min(row[0])`, `hi = max(row[-1])`, since each row is sorted.
- `count(v) = sum(bisect_right(row, v) for row in matrix)`. It is non-decreasing in v, so find the smallest v with `count(v) >= need`.
- Why that v is an actual entry: for the smallest such v, `count(v - 1) < need <= count(v)`. So some entry equals v exactly (the count rose at v), and v is the need-th smallest value.
- Why not flatten-and-bisect: reading the rows one after another gives [1, 3, 5, 2, 6, 9, 3, 6, 9], which is not sorted, so there is no index to bisect. The rows are only sorted individually.
- Why r and c odd: r*c is odd, so there is one middle element and no averaging of two values.

**Complexity:** Time O(r * log c * log(range)): each value step does r bisects of O(log c). With range 10^9 that is about 30 steps (my run: 30 steps and 29,970 `bisect_right` calls for a 999 x 1001 matrix). Space O(1) extra.

**Dry run:** [[1,3,5],[2,6,9],[3,6,9]], need = 5, lo = 1, hi = 9.
| lo | hi | mid | count(<= mid) | action |
|---|---|---|---|---|
| 1 | 9 | 5 | 3 + 1 + 1 = 5 >= 5 | hi = 5 |
| 1 | 5 | 3 | 2 + 1 + 1 = 4 < 5 | lo = 4 |
| 4 | 5 | 4 | 2 + 1 + 1 = 4 < 5 | lo = 5 |

Answer 5, which is the 5th of 1, 2, 3, 3, 5, 6, 6, 9, 9.

**Code:**
```python
import random
from bisect import bisect_right

CALLS = 0


def count_le(matrix, v):
    global CALLS
    total = 0
    for row in matrix:
        CALLS += 1
        total += bisect_right(row, v)
    return total


def matrix_median(matrix):
    r, c = len(matrix), len(matrix[0])
    need = (r * c + 1) // 2                         # r*c odd, so this is the middle rank
    lo = min(row[0] for row in matrix)
    hi = max(row[-1] for row in matrix)
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(matrix, mid) >= need:
            hi = mid
        else:
            lo = mid + 1
    return lo


def matrix_median_brute(matrix):
    flat = sorted(x for row in matrix for x in row)
    return flat[len(flat) // 2]


for m, want in [([[1, 3, 5], [2, 6, 9], [3, 6, 9]], 5), ([[1]], 1), ([[1, 1, 1], [2, 2, 2], [3, 3, 3]], 2)]:
    print(m, "->", matrix_median(m), " brute:", matrix_median_brute(m))
    assert matrix_median(m) == matrix_median_brute(m) == want

rng = random.Random(37)
for _ in range(2000):
    r = rng.choice([1, 3, 5])
    c = rng.choice([1, 3, 5, 7])
    hi = rng.choice([3, 10, 100])
    m = [sorted(rng.randint(0, hi) for _ in range(c)) for _ in range(r)]
    v = matrix_median(m)
    assert v == matrix_median_brute(m), m
    assert any(v in row for row in m)               # the answer is an actual entry
print("2000 seeded random odd-by-odd matrices agree; answer was always an entry")

# why flattening-and-bisecting fails: flattening row by row is not sorted
m = [[1, 3, 5], [2, 6, 9], [3, 6, 9]]
flat = [x for row in m for x in row]
print("row-major flatten:", flat, "sorted?", flat == sorted(flat))
assert flat != sorted(flat)

# call count on a big case: r = 999, c = 1001 (about 10**6 entries), values up to 10**9
big = [sorted(rng.randint(0, 10**9) for _ in range(1001)) for _ in range(999)]
CALLS = 0
v = matrix_median(big)
steps = CALLS // 999
print("big matrix 999 x 1001: value-search steps =", steps, " bisect_right calls =", CALLS)
assert steps <= 30
assert v == matrix_median_brute(big)
# edge asserts
assert matrix_median([[7, 7, 7]]) == 7
assert matrix_median([[1], [2], [3]]) == 2
assert matrix_median([[5, 5, 5], [5, 5, 5], [5, 5, 5]]) == 5
assert matrix_median([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 5
print("all checks passed")
```

**Output (my run):**
```text
[[1, 3, 5], [2, 6, 9], [3, 6, 9]] -> 5  brute: 5
[[1]] -> 1  brute: 1
[[1, 1, 1], [2, 2, 2], [3, 3, 3]] -> 2  brute: 2
2000 seeded random odd-by-odd matrices agree; answer was always an entry
row-major flatten: [1, 3, 5, 2, 6, 9, 3, 6, 9] sorted? False
big matrix 999 x 1001: value-search steps = 30  bisect_right calls = 29970
all checks passed
```

The three prompt examples are correct. 2,000 seeded random odd-by-odd matrices with many duplicates agreed with the flatten-and-sort answer, and the result was always an entry.

**Edge cases:**
- 1 x 1: lo = hi, returns the value.
- Heavy duplicates: bisect_right counts all copies of mid, which is what the rank needs.
- Single row or single column: works the same.
- Negative values: fine, the range just starts lower.

**Follow-ups:**
- "Even r*c?" Take the average of the two middle ranks, found with two searches (need and need + 1).
- "Why bisect_right not bisect_left?" I need the count of entries <= v. bisect_left would count entries < v.
- "Heap alternative?" A k-way merge heap works but costs O(rc log r) time; Part 8 covers heaps.

**Common mistakes:**
- Using `bisect_left`.
- Using `need = r*c // 2` (zero-based index) against a count that is one-based.
- Using lo = 0 and hi = 10^9 blindly; fine, but the min/max of rows is tighter.

---

### Q38 ⭐ 🔴 K-th smallest pair distance. `nums` is a list of integers (2 <= len <= 10^4, values up to 10^6) and 1 <= k <= n*(n-1)/2. Consider the absolute difference |nums[i] - nums[j]| for every pair i < j; return the k-th smallest of these n*(n-1)/2 values (duplicates counted). Sort nums, binary search the distance d in [0, max - min], and count pairs with distance <= d in O(n) with two pointers; return the smallest d with count >= k. Give the O(n^2 log n) enumerate-and-sort reference and explain why the O(n^2) pair list is too big for n = 10^4. (A value-space binary search for a different counting problem is Part 1 Q28.) Example: [1,3,1], k=1 -> 0; [1,1,1], k=2 -> 0; [1,6,1], k=3 -> 5; [1,3,1], k=2 -> 2; [1,3,1], k=3 -> 2.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on the answer (a distance), with an O(n) two-pointer count on the sorted array.

**Say this first (1 line):** "Sort, then binary search the distance d; for each d count pairs with difference <= d by two pointers in O(n); the answer is the smallest d with at least k pairs."

**Brute force:** Build all n(n-1)/2 absolute differences, sort, take index k - 1: O(n^2 log n) time, O(n^2) space. For n = 10^4 there are 49,995,000 pairs; at just 8 bytes per list slot that is about 399 MB before counting the int objects. Too big. It is my checker for small n.

**Optimal:**
- Sort `nums`. Distances between pairs are then differences of sorted values, and the set of pair distances is the same.
- `count_le(d)`: for each `right`, move `left` forward while `a[right] - a[left] > d`; add `right - left` (the partners to its left within d). Left never moves backward, so this is O(n).
- `count_le` is non-decreasing in d. Search d in [0, a[-1] - a[0]] for the smallest d with `count_le(d) >= k`.
- Why that d is an actual distance: count(d - 1) < k <= count(d), so at least one pair has distance exactly d.
- Duplicates count: [1, 1, 1] has three pairs of distance 0.

**Complexity:** Time O(n log n) for the sort plus O(n log(max - min)) for the search, about 20 to 30 counting passes. Space O(1) beyond the sorted copy.

**Dry run:** nums = [1, 3, 1], k = 2. Sorted [1, 1, 3], range [0, 2].
- mid = 1: right = 1 (value 1): left 0, adds 1. right = 2 (value 3): 3 - 1 > 1 and 3 - 1 > 1, left goes to 2, adds 0. Total 1 < 2, so lo = 2.
- lo = hi = 2. Answer 2. Check: distances 0, 2, 2; the second smallest is 2.

**Code:**
```python
import random
from itertools import combinations


def kth_pair_distance(nums, k):
    a = sorted(nums)
    n = len(a)

    def count_le(d):
        cnt, left = 0, 0
        for right in range(n):
            while a[right] - a[left] > d:
                left += 1
            cnt += right - left              # pairs (left..right-1, right) with distance <= d
        return cnt

    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_pair_distance_brute(nums, k):
    return sorted(abs(x - y) for x, y in combinations(nums, 2))[k - 1]


for nums, k, want in [([1, 3, 1], 1, 0), ([1, 1, 1], 2, 0), ([1, 6, 1], 3, 5), ([1, 3, 1], 2, 2), ([1, 3, 1], 3, 2)]:
    got = kth_pair_distance(nums, k)
    print(nums, "k =", k, "->", got, " brute:", kth_pair_distance_brute(nums, k))
    assert got == kth_pair_distance_brute(nums, k) == want

rng = random.Random(38)
cnt = 0
for _ in range(1500):
    n = rng.randint(2, 9)
    nums = [rng.randint(0, 12) for _ in range(n)]
    for k in range(1, n * (n - 1) // 2 + 1):
        assert kth_pair_distance(nums, k) == kth_pair_distance_brute(nums, k), (nums, k)
        cnt += 1
print("random (nums, k) cases checked:", cnt)

# size argument for n = 10**4
n = 10**4
pairs = n * (n - 1) // 2
print("pairs for n = 10**4:", pairs, " pointer slots alone at 8 bytes each: about", pairs * 8 // 10**6, "MB")
# runtime sanity on a big input (sandbox only): O(n log range), never builds pairs
big = [rng.randint(0, 10**6) for _ in range(n)]
v = kth_pair_distance(big, pairs // 2)
print("n = 10**4 median pair distance (sandbox run):", v)
# edge asserts
assert kth_pair_distance([5, 5], 1) == 0
assert kth_pair_distance([1, 100], 1) == 99
assert kth_pair_distance([0, 10**6], 1) == 10**6
assert kth_pair_distance([1, 2, 3, 4], 6) == 3
print("all checks passed")
```

**Output (my run):**
```text
[1, 3, 1] k = 1 -> 0  brute: 0
[1, 1, 1] k = 2 -> 0  brute: 0
[1, 6, 1] k = 3 -> 5  brute: 5
[1, 3, 1] k = 2 -> 2  brute: 2
[1, 3, 1] k = 3 -> 2  brute: 2
random (nums, k) cases checked: 22297
pairs for n = 10**4: 49995000  pointer slots alone at 8 bytes each: about 399 MB
n = 10**4 median pair distance (sandbox run): 293341
all checks passed
```

All five prompt examples match the brute force. The random check ran every k for 1,500 seeded small lists with many ties (22,297 cases). I also ran n = 10^4 in the sandbox: it finishes without building any pair list (sandbox-only, not a proof of big-O).

**Edge cases:**
- n = 2: one pair, distance |a - b|.
- All equal: every distance 0.
- k = 1: the minimum gap (often 0 with duplicates); k = n(n-1)/2: max - min.
- Unsorted input: sort a copy first.

**Follow-ups:**
- "Faster than O(n log range)?" Not easily; the heap approach (pop and push neighbours) is O(k log n), worse for big k.
- "Is the pair set the same after sorting?" Yes: the multiset of |x - y| does not depend on order.
- "Does the count use <= or <?" `<= d`; with `< d` the smallest-d rule changes.

**Common mistakes:**
- Forgetting to sort before the two-pointer count.
- Counting `right - left + 1` (includes the element itself).
- Resetting `left = 0` for every right (O(n^2)).
- Searching [1, max - min] and missing distance 0.

---

### Q39 ⭐ 🔴 K-th smallest number in a multiplication table. The table has m rows and n columns where the entry in row i and column j (1-indexed) is i * j (1 <= m, n <= 3*10^4); k is 1-based with 1 <= k <= m*n and counts duplicates. Return the k-th smallest entry without building the table. Binary search the VALUE v in [1, m*n] with count(v) = sum over rows i of min(n, v // i), and return the smallest v with count(v) >= k. Explain why that v is always an entry of the table, and why this is a search over values (the table is not a sorted list you can index). Example: m=3, n=3, k=5 -> 3; m=2, n=3, k=6 -> 6; m=1, n=5, k=4 -> 4; m=3, n=3, k=9 -> 9; m=3, n=3, k=1 -> 1.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on the value, with a counting predicate: how many table entries are <= v.

**Say this first (1 line):** "The table is not a list I can index, so I binary search the value v and count entries <= v as the sum over rows of min(n, v // i); the answer is the smallest v with count >= k."

**Brute force:** Build the m x n table, sort, take index k - 1: O(mn log(mn)) time, O(mn) space. With m = n = 3*10^4 that is 9*10^8 entries. My checker uses it on small tables only.

**Optimal:**
- Row i holds i, 2i, ..., ni. Entries <= v in that row: `min(n, v // i)`.
- `count(v) = sum for i in 1..m of min(n, v // i)`. Rows with i > v contribute 0, so I loop to `min(m, v)`.
- count is non-decreasing in v. Search [1, m*n] for the smallest v with `count(v) >= k`.
- Why v is an entry: count(v - 1) < k <= count(v), so the count increases at v, which only happens if some i * j equals v.
- Why a value search: the table in row-major order is [1, 2, 3, 2, 4, 6, 3, 6, 9] for 3 x 3, which is not sorted, and sorted values can repeat; there is no array to bisect. The values are ordered, though, so I search them.

**Complexity:** Time O(m log(mn)): each count is O(m), and the value search takes about log2(9*10^8), roughly 30 steps. Space O(1). (Swap the roles to loop over the smaller of m and n.)

**Dry run:** m = 3, n = 3, k = 5, lo = 1, hi = 9.
| lo | hi | mid | count | action |
|---|---|---|---|---|
| 1 | 9 | 5 | 3 + 2 + 1 = 6 >= 5 | hi = 5 |
| 1 | 5 | 3 | 3 + 1 + 1 = 5 >= 5 | hi = 3 |
| 1 | 3 | 2 | 2 + 1 + 0 = 3 < 5 | lo = 3 |

Answer 3. Sorted table: 1, 2, 2, 3, 3, 4, 6, 6, 9, so the 5th is 3.

**Code:**
```python
def kth_table(m, n, k):
    def count_le(v):
        return sum(min(n, v // i) for i in range(1, min(m, v) + 1))   # rows beyond v contribute 0
    lo, hi = 1, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_table_brute(m, n, k):
    return sorted(i * j for i in range(1, m + 1) for j in range(1, n + 1))[k - 1]


for m, n, k, want in [(3, 3, 5, 3), (2, 3, 6, 6), (1, 5, 4, 4), (3, 3, 9, 9), (3, 3, 1, 1)]:
    got = kth_table(m, n, k)
    print("m =", m, "n =", n, "k =", k, "->", got, " brute:", kth_table_brute(m, n, k))
    assert got == kth_table_brute(m, n, k) == want

# exhaustive: all m, n up to 9 and every k
cnt = 0
for m in range(1, 10):
    for n in range(1, 10):
        table = {i * j for i in range(1, m + 1) for j in range(1, n + 1)}
        for k in range(1, m * n + 1):
            v = kth_table(m, n, k)
            assert v == kth_table_brute(m, n, k), (m, n, k)
            assert v in table                          # the answer is always an entry
            cnt += 1
print("exhaustive (m, n, k) cases checked:", cnt)

# the table is not a sorted list: row-major reading of the 3 x 3 table
print("row-major 3 x 3:", [i * j for i in range(1, 4) for j in range(1, 4)])
# big sizes: no table is built
v = kth_table(3 * 10**4, 3 * 10**4, 3 * 10**4 * 3 * 10**4)
assert v == 9 * 10**8
v = kth_table(3 * 10**4, 3 * 10**4, 4 * 10**8)
print("m = n = 3*10**4, k = 4*10**8 ->", v)
# edge asserts
assert kth_table(1, 1, 1) == 1
assert kth_table(1, 7, 7) == 7 and kth_table(7, 1, 1) == 1
assert kth_table(30000, 1, 30000) == 30000
print("all checks passed")
```

**Output (my run):**
```text
m = 3 n = 3 k = 5 -> 3  brute: 3
m = 2 n = 3 k = 6 -> 6  brute: 6
m = 1 n = 5 k = 4 -> 4  brute: 4
m = 3 n = 3 k = 9 -> 9  brute: 9
m = 3 n = 3 k = 1 -> 1  brute: 1
exhaustive (m, n, k) cases checked: 2025
row-major 3 x 3: [1, 2, 3, 2, 4, 6, 3, 6, 9]
m = n = 3*10**4, k = 4*10**8 -> 139742112
all checks passed
```

All five prompt examples are right. I tested every m, n in 1..9 and every k (2,025 cases): the result matched brute force and was always in the table. The m = n = 3*10^4 runs build no table.

**Edge cases:**
- m = 1 or n = 1: a single row or column, answer is k.
- k = 1: 1. k = m*n: m*n.
- Repeated values (6 appears twice in 3 x 3): handled since count includes duplicates.
- Large m and n: the count loop is the only cost.

**Follow-ups:**
- "Can I count faster?" Yes, group rows by v // i blocks in O(sqrt v), but O(m) is already fine here.
- "Same idea elsewhere?" Kth smallest in a sorted matrix (Part 8 for the heap version) and pair distance (Q38).
- "Why min(n, v // i)?" Row i stops at column n.

**Common mistakes:**
- Looping rows past v (harmless but wasteful) or forgetting the `min(n, ...)` cap.
- Returning `lo - 1` or `hi` wrongly with a mixed template.
- Building the table.

---

### Q40 ⭐ 🔴 Minimise the maximum gap after adding k gas stations (real-valued answer). `stations` is a sorted list of distinct integer positions along a line (2 <= len <= 2000) and k >= 0 new stations may be placed anywhere (real positions allowed). Return the smallest achievable value of the largest distance between adjacent stations, within 10^-6. Binary search the gap d with the predicate 'sum over gaps of ceil(gap / d) - 1 <= k'. Explain why the predicate is monotone in d, why a fixed iteration count beats an epsilon loop here, and how the exact answer relates to some gap / (c + 1) for an integer c. Example: [1,2,3,4,5,6,7,8,9,10], k=9 -> 0.5; [23,24,36,39,46,56,57,65,84,98], k=1 -> 14.0; [0,10], k=0 -> 10.0; [0,10], k=1 -> 5.0.
**Asked at:** Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a real answer d with the predicate "stations needed with max gap <= d is at most k".

**Say this first (1 line):** "A gap of length g needs ceil(g / d) - 1 new stations to get every piece <= d; if the total is <= k, d is achievable, so I shrink d, with a fixed 100 halvings."

**Brute force:** Greedy with a heap: always put one more station into the gap with the largest current piece (gap / (c + 1)). That is O(k log n), which is slow for huge k but exact. For small k I also try every way to split k stations over the gaps with exact fractions, which is my checker.

**Optimal:**
- `need(d) = sum(ceil((b - a) / d) - 1 for each adjacent pair)`.
- Monotone: a larger d never needs more stations, since ceil(g / d) is non-increasing in d. I checked `need` on 200 seeded lists over d = 0.25..49.75.
- Range: `lo = 0`, `hi = largest gap` (with d = hi, `need = 0 <= k`). Loop 100 times: `mid`; if `need(mid) <= k` then `hi = mid` else `lo = mid`. Return `hi`.
- Why a fixed count: the epsilon loop works with a sane eps (eps = 1e-6 took 24 loops for [0, 10], k = 1), but with a too-small eps it can never end, like Q31. On the 14.0 example, eps = 1e-17 ran into my 10^6-loop cap. A fixed count never hangs. I would say it plainly: a fixed count does not make the answer more correct, it just guarantees termination.
- Exact answer: the optimum is always some gap / (c + 1) for an integer c (one gap is the bottleneck and holds c extra stations, split evenly). In 600 seeded cases the exact optimum was always of that form, so a final snap to the nearest such value is possible.
- Float risk: ceil of a float quotient near an integer can flip, but the effect is on the order of the tolerance, and my cross-check found the worst error about 1.1e-16.

**Complexity:** Time O(n * iterations) = O(100 n), about 2*10^5 operations for n = 2000. Space O(1). The heap version is O(k log n).

**Dry run:** stations [0, 10], k = 1. lo = 0, hi = 10.
| mid | need = ceil(10 / mid) - 1 | action |
|---|---|---|
| 5 | 1 <= 1 | hi = 5 |
| 2.5 | 3 > 1 | lo = 2.5 |
| 3.75 | 2 > 1 | lo = 3.75 |
| 4.375 | 2 > 1 | lo = 4.375 |

It converges to 5.0 from above, exactly 10 / (1 + 1).

**Code:**
```python
import math
import random
from fractions import Fraction
from itertools import product


def need(stations, d):
    return sum(math.ceil((b - a) / d) - 1 for a, b in zip(stations, stations[1:]))


def min_max_gap(stations, k, iters=100):
    lo, hi = 0.0, float(max(b - a for a, b in zip(stations, stations[1:])))
    for _ in range(iters):
        mid = (lo + hi) / 2
        if need(stations, mid) <= k:
            hi = mid                        # mid is enough, try smaller
        else:
            lo = mid
    return hi


def min_max_gap_eps(stations, k, eps, cap=10**6):
    lo, hi = 0.0, float(max(b - a for a, b in zip(stations, stations[1:])))
    loops = 0
    while hi - lo > eps and loops < cap:
        mid = (lo + hi) / 2
        if need(stations, mid) <= k:
            hi = mid
        else:
            lo = mid
        loops += 1
    return hi, loops


def min_max_gap_exact(stations, k):
    # brute force: try every way to split k stations over the gaps (extra stations in a gap -> gap/(c+1)); exact Fractions
    gaps = [b - a for a, b in zip(stations, stations[1:])]
    best = None
    def go(i, left, cur):
        nonlocal best
        if i == len(gaps) - 1:
            v = max(cur, Fraction(gaps[i], left + 1))
            if best is None or v < best:
                best = v
            return
        for c in range(left + 1):
            go(i + 1, left - c, max(cur, Fraction(gaps[i], c + 1)))
    go(0, k, Fraction(0))
    return best


for st, k, want in [(list(range(1, 11)), 9, 0.5), ([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 14.0), ([0, 10], 0, 10.0), ([0, 10], 1, 5.0)]:
    got = min_max_gap(st, k)
    print(st, "k =", k, "->", round(got, 7))
    assert abs(got - want) <= 1e-6
print("eps=1e-6 loop on [0,10], k=1:", min_max_gap_eps([0, 10], 1, 1e-6))
print("eps=1e-17 loop on the 14.0 example, capped at 10**6:", min_max_gap_eps([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 1e-17)[1], "loops")
assert min_max_gap_eps([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 1e-17)[1] == 10**6

# seeded cross-check against exact brute force, and the 'gap/(c+1)' claim
rng = random.Random(40)
hit = 0
worst = 0.0
for _ in range(600):
    n = rng.randint(2, 5)
    st = sorted(rng.sample(range(0, 40), n))
    k = rng.randint(0, 5)
    ex = min_max_gap_exact(st, k)
    got = min_max_gap(st, k)
    worst = max(worst, abs(got - float(ex)))
    assert abs(got - float(ex)) <= 1e-6, (st, k)
    gaps = [b - a for a, b in zip(st, st[1:])]
    assert any(ex == Fraction(g, c + 1) for g in gaps for c in range(k + 1)), (st, k)
    hit += 1
print("600 seeded cases: worst |binary search - exact| =", worst, "; exact optimum was always some gap/(c+1)")

# monotone predicate: need() never increases as d grows
for _ in range(200):
    st = sorted(rng.sample(range(0, 60), rng.randint(2, 7)))
    seq = [need(st, d / 4) for d in range(1, 200)]
    assert all(x >= y for x, y in zip(seq, seq[1:]))
print("need(d) non-increasing in d on 200 seeded station lists")
# edge asserts
assert abs(min_max_gap([0, 1], 0) - 1.0) <= 1e-6
assert abs(min_max_gap([0, 1, 2], 100) - 1 / 51) <= 1e-6        # 100 stations over 2 equal gaps: 50 each, gap 1/51
assert abs(min_max_gap([0, 7], 3) - 1.75) <= 1e-6
assert abs(min_max_gap([0, 10, 11], 1) - 5.0) <= 1e-6
print("all checks passed")
```

**Output (my run):**
```text
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] k = 9 -> 0.5
[23, 24, 36, 39, 46, 56, 57, 65, 84, 98] k = 1 -> 14.0
[0, 10] k = 0 -> 10.0
[0, 10] k = 1 -> 5.0
eps=1e-6 loop on [0,10], k=1: (5.0, 24)
eps=1e-17 loop on the 14.0 example, capped at 10**6: 1000000 loops
600 seeded cases: worst |binary search - exact| = 1.1102230246251565e-16 ; exact optimum was always some gap/(c+1)
need(d) non-increasing in d on 200 seeded station lists
all checks passed
```

All four prompt examples are right (0.5, 14.0, 10.0, 5.0). For 600 seeded small cases the binary search agreed with exact-fraction brute force to within 1.1e-16.

**Edge cases:**
- k = 0: answer is the largest gap (`need(d) <= 0` only when d >= every gap).
- Two stations only: one gap g, answer g / (k + 1).
- Huge k: the answer approaches 0 (never negative or zero, since `mid > 0`).
- Equal gaps: stations are spread evenly across them.

**Follow-ups:**
- "Why not search integers?" New stations may sit at real positions, so the answer can be fractional (0.5 in the first example).
- "Can I get the exact value?" Candidates are gap / (c + 1); test the smallest feasible one with fractions.
- "How is this like Allocate Books / ship packages?" Same minimise-the-maximum shape, but the answer is real, so I loop a fixed number of times instead of stopping at lo == hi.

**Common mistakes:**
- `ceil(g / d)` instead of `ceil(g / d) - 1` (counts pieces, not stations).
- Initialising `lo` to the smallest gap (wrong: the answer can be below it).
- Looping `while hi - lo > 1e-6` with a smaller epsilon and hanging.
- Putting stations into only the largest gap.

