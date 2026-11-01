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
