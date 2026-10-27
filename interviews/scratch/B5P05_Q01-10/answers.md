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
