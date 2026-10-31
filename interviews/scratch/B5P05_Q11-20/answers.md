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
