# Book 5 Part 1: answers Q31-Q40 (Wave B)

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
