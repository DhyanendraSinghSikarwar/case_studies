# Book 5 Part 11 answers Q1-Q9 (Wave B)

### Q1 ⭐⭐⭐ 🟢 Unique paths in a grid. A robot starts at the top-left cell of an `m` x `n` grid (1 <= m, n <= 100) and may only move one cell right or one cell down. Return the exact number of distinct paths to the bottom-right cell (Python integers do not overflow, so no modulus). Define `dp[i][j]`, the transition and the base row and column, then shrink the table to ONE row of length n and say which direction the inner loop must run and why the in-place update is safe. Build any 2D table with a comprehension, never `[[0]*n]*m` (see Part 10 Q31). Also show the closed form with `math.comb` and why it agrees. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (m, n <= 8) and the closed form with math.comb on small inputs. Example: m=3, n=7 -> 28; m=3, n=2 -> 3; m=1, n=1 -> 1; m=1, n=5 -> 1; m=100, n=100 -> 22750883079422934966181954039568885395604168260154104734000.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 2D grid DP, counting. Every cell is reached from exactly two neighbours, so the count is the sum of two smaller counts.

**Say this first (1 line):** "dp[i][j] is the number of paths from the start to cell (i, j); it is dp[i-1][j] + dp[i][j-1], the first row and column are all 1, and I can keep one row because I only need the row above. O(m*n) time, O(n) space; the closed form is C(m+n-2, m-1)."

**Brute force:** Plain recursion from the start: `f(i, j) = f(i+1, j) + f(i, j+1)`, 1 at the end cell, no memo. It re-counts the same cells. The number of calls grows like the answer itself, so it is exponential.

**Optimal:**
- State: `dp[i][j]` = number of distinct right/down paths from (0, 0) to (i, j).
- Transition: the last move into (i, j) was either down from (i-1, j) or right from (i, j-1). Those two sets of paths are disjoint, so `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
- Base: the first row and first column are 1 (only straight moves reach them). The start cell is 1.
- One row: keep `row` of length n. Before cell (i, j) is processed, `row[j]` still holds `dp[i-1][j]` (up). `row[j-1]` has just been overwritten, so it holds `dp[i][j-1]` (left). So `row[j] += row[j-1]` is exactly the transition.
- Direction: the inner loop must run left to right (ascending j). Descending, `row[j-1]` would still be the old "up" value and you would add the wrong neighbour. I tested this exactly in the code: for m, n in 1..8 the descending loop is wrong precisely when m >= 2 and n >= 3 (for n = 2 there is only one update per row, so there is nothing to get wrong; for m = 1 nothing runs).
- Closed form: any path has m-1 downs and n-1 rights in some order, so the count is the number of ways to choose which of the m+n-2 moves are downs: `math.comb(m+n-2, m-1)`. The DP is Pascal's triangle read along diagonals, which is why the two agree.
- Python: build tables with `[[1] * n for _ in range(m)]`. With `[[1] * n] * m` all rows are the same list object (shown in the code), so one write appears in every row.

**Complexity:** Time O(m*n). Space O(n) for the row (O(m*n) for the full table). `math.comb` is O(min(m, n)) big-integer multiplications. Memoised top-down is also O(m*n) states, with a recursion depth of m+n-1 frames, which is fine here.

**Dry run:** m = 3, n = 7. Each row below is the full table row, and is also the contents of the single `row` list after that grid row has been processed.

| row | j=0 | j=1 | j=2 | j=3 | j=4 | j=5 | j=6 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 2 | 1 | 3 | 6 | 10 | 15 | 21 | 28 |

Example cell: row 2, j=3 is up (4) + left (6) = 10. Answer 28 = C(8, 2).

**Code:**
```python
import math
import random
import sys
from functools import lru_cache

random.seed(1101)

def paths_table(m, n):
    """Full table. dp[i][j] = paths from (0,0) to (i,j). First row and column are all 1."""
    dp = [[1] * n for _ in range(m)]          # comprehension: every row is a separate list
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp

def paths_row(m, n):
    """One row of length n. row[j] holds 'above' until overwritten, then 'this cell'."""
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):                 # ascending: row[j-1] is already this row's value
            row[j] += row[j - 1]              # row[j] (old) = up, row[j-1] (new) = left
    return row[-1]

def paths_row_descending(m, n):
    """WRONG on purpose: descending reads row[j-1] before it is updated (it is still 'up')."""
    row = [1] * n
    for _ in range(1, m):
        for j in range(n - 1, 0, -1):
            row[j] += row[j - 1]
    return row[-1]

def paths_comb(m, n):
    """Every path is m-1 downs and n-1 rights in some order: choose where the downs go."""
    return math.comb(m + n - 2, m - 1)

def paths_plain(m, n):
    """Oracle: plain recursion, no memo."""
    def f(i, j):
        if i == m - 1 and j == n - 1:
            return 1
        return (f(i + 1, j) if i + 1 < m else 0) + (f(i, j + 1) if j + 1 < n else 0)
    return f(0, 0)

def paths_memo(m, n):
    @lru_cache(maxsize=None)
    def f(i, j):                              # paths from (i,j) to the end, tuple key
        if i == m - 1 or j == n - 1:
            return 1
        return f(i + 1, j) + f(i, j + 1)
    return f(0, 0)

# prompt examples
for (m, n), want in [((3, 7), 28), ((3, 2), 3), ((1, 1), 1), ((1, 5), 1),
                     ((100, 100), 22750883079422934966181954039568885395604168260154104734000)]:
    assert paths_row(m, n) == paths_table(m, n)[-1][-1] == paths_comb(m, n) == paths_memo(m, n) == want
print("5 prompt examples ok (incl. 100 x 100, a " + str(len(str(paths_comb(100, 100)))) + "-digit exact integer)")

# walk-through table
print("table 3 x 7:")
for r in paths_table(3, 7):
    print("  ", r)
row = [1] * 7
print("one row after each row of the grid:")
print("  row 0 :", row)
for i in range(1, 3):
    for j in range(1, 7):
        row[j] += row[j - 1]
    print("  row", i, ":", row)

# aliasing trap, exact claim: rows are the same object, so a write shows in every row
bad = [[0] * 3] * 2
bad[0][0] = 7
print("aliased rows:", bad, "same object:", bad[0] is bad[1])
good = [[0] * 3 for _ in range(2)]
good[0][0] = 7
print("comprehension rows:", good)

# exhaustive oracle check, 1..8 x 1..8, all three methods + closed form
for m in range(1, 9):
    for n in range(1, 9):
        o = paths_plain(m, n)
        assert paths_row(m, n) == paths_table(m, n)[-1][-1] == paths_comb(m, n) == paths_memo(m, n) == o, (m, n)
print("exhaustive 1..8 x 1..8 (64 grids): row == table == comb == memo == plain recursion")
for _ in range(300):
    m, n = random.randint(1, 8), random.randint(1, 8)
    assert paths_row(m, n) == paths_plain(m, n) == paths_comb(m, n)
print("300 seeded random (m, n <= 8): ok")

# descending claim, tested exhaustively on 1..8
bad_pairs = [(m, n) for m in range(1, 9) for n in range(1, 9) if paths_row_descending(m, n) != paths_comb(m, n)]
ok_pairs = [(m, n) for m in range(1, 9) for n in range(1, 9) if paths_row_descending(m, n) == paths_comb(m, n)]
print("descending inner loop wrong for", len(bad_pairs), "of 64 grids; all have m>=2 and n>=3:",
      all(m >= 2 and n >= 3 for m, n in bad_pairs), "; and every grid with m>=2,n>=3 is wrong:",
      all((m, n) in bad_pairs for m in range(2, 9) for n in range(3, 9)))
print("example: 3 x 3 descending gives", paths_row_descending(3, 3), "instead of", paths_comb(3, 3))

# recursion limit on the memoised version (default limit 1000)
print("recursion limit:", sys.getrecursionlimit())
print("memo 100 x 100 ok, depth about m + n = 200 frames:", paths_memo(100, 100) == paths_comb(100, 100))
```

**Output (my run):**
```
5 prompt examples ok (incl. 100 x 100, a 59-digit exact integer)
table 3 x 7:
   [1, 1, 1, 1, 1, 1, 1]
   [1, 2, 3, 4, 5, 6, 7]
   [1, 3, 6, 10, 15, 21, 28]
one row after each row of the grid:
  row 0 : [1, 1, 1, 1, 1, 1, 1]
  row 1 : [1, 2, 3, 4, 5, 6, 7]
  row 2 : [1, 3, 6, 10, 15, 21, 28]
aliased rows: [[7, 0, 0], [7, 0, 0]] same object: True
comprehension rows: [[7, 0, 0], [0, 0, 0]]
exhaustive 1..8 x 1..8 (64 grids): row == table == comb == memo == plain recursion
300 seeded random (m, n <= 8): ok
descending inner loop wrong for 42 of 64 grids; all have m>=2 and n>=3: True ; and every grid with m>=2,n>=3 is wrong: True
example: 3 x 3 descending gives 4 instead of 6
recursion limit: 1000
memo 100 x 100 ok, depth about m + n = 200 frames: True
```

**Edge cases:**
- 1 x 1 is 1 (the start is the end); 1 x n and m x 1 are 1.
- 100 x 100 is a 59-digit integer. Python ints are exact, so no modulus and no overflow.
- Swapping m and n gives the same answer (symmetric).
- With n = 1 the inner loop does nothing and `row[-1]` is still 1.

**Follow-ups:**
- Obstacles? Zero the cell; see Q2.
- Cheapest path instead of count? Same table with `min` and costs; see Q3.
- Memoised top-down? `lru_cache` on `(i, j)` works at 100 x 100 (depth about 200 frames, well under the default limit of 1000). Bottom-up is still the safer habit for grids with a long side.
- Modulus 10^9+7? Add `% MOD` in the update, or use the closed form with modular inverses.

**Common mistakes:**
- `[[0]*n]*m`: all rows alias.
- Inner loop descending in the one-row version (wrong, see above).
- Forgetting that the first row and column are 1, so they get 0 and everything is 0.
- Using the closed form with `m+n` instead of `m+n-2`.

---

### Q2 ⭐⭐⭐ 🟡 Unique paths with obstacles. `grid` is an m x n list of lists (1 <= m, n <= 100) of 0 (free) and 1 (blocked). Move only right or down through free cells. Return the exact number of paths from the top-left to the bottom-right cell; return 0 if the start or the end is blocked. Give the state, the transition (a blocked cell has 0 paths) and the base cases, then the one-row version, and say what happens to the row value of a blocked cell when you reuse the row. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (m, n <= 5) on small inputs. Example: grid=[[0, 0, 0], [0, 1, 0], [0, 0, 0]] -> 2; grid=[[0, 1], [0, 0]] -> 1; grid=[[1, 0]] -> 0; grid=[[0, 0], [0, 1]] -> 0; grid=[[0]] -> 1.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid counting DP with forbidden cells. Same recurrence as Q1; a blocked cell simply has zero paths.

**Say this first (1 line):** "dp[i][j] is the number of paths to (i, j), 0 if the cell is blocked, otherwise up + left, with dp[0][0] = 1 if the start is free; in one row I must explicitly write 0 into a blocked cell, because otherwise it keeps the count from the row above. O(m*n) time, O(n) space."

**Brute force:** Plain recursion from the start: a blocked cell returns 0, the end returns 1, else `f(i+1, j) + f(i, j+1)`. Exponential without a memo.

**Optimal:**
- State: `dp[i][j]` = number of right/down paths from (0, 0) to (i, j) that only touch free cells.
- Transition: blocked means 0. Free means `dp[i-1][j] + dp[i][j-1]` (a neighbour outside the grid counts 0).
- Base: `dp[0][0] = 1` if free, else 0. Everything downstream of a blocked start is then 0 by the transition. A blocked end gets 0 by the same rule, so both special cases need no separate code.
- First row: once a cell is blocked, everything to its right in row 0 is 0 (the only way in is through it). The same holds down column 0. The formula gives this automatically.
- One row: `row[j]` holds the cell above before it is processed. For a blocked cell you must write `row[j] = 0`. If you skip it, the stale above-count survives and the cell below and the cell to the right wrongly count paths through the wall. I tested it: skipping instead of zeroing is wrong on 210 of the 682 grids of size up to 3 x 3 (smallest: a column `[[0], [1]]` returns 1 instead of 0).
- For a free cell with j = 0 and i > 0 there is no left neighbour, so `row[0]` just keeps the value from above. That is right.

**Complexity:** Time O(m*n), space O(n). The answer can be large (an empty 100 x 100 grid gives a 59-digit integer), but Python ints do not overflow.

**Dry run:** `grid = [[0,0,0],[0,1,0],[0,0,0]]`.

| row | j=0 | j=1 | j=2 | note |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | start = 1, then left only |
| 1 | 1 | 0 | 1 | (1,1) blocked, written as 0; (1,2) = up 1 + left 0 |
| 2 | 1 | 1 | 2 | (2,1) = 0 + 1; (2,2) = up 1 + left 1 |

Answer 2: right-right-down-down and down-down-right-right.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1102)

def paths_obs_table(grid):
    """dp[i][j] = paths to (i,j); 0 if the cell is blocked."""
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[i][j] = 0
            elif i == 0 and j == 0:
                dp[i][j] = 1
            else:
                dp[i][j] = (dp[i - 1][j] if i else 0) + (dp[i][j - 1] if j else 0)
    return dp

def paths_obs(grid):
    """One row. A blocked cell must set row[j] = 0, otherwise the stale 'up' value leaks through."""
    m, n = len(grid), len(grid[0])
    row = [0] * n
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                row[j] = 0                      # kill the value inherited from the row above
            elif i == 0 and j == 0:
                row[j] = 1
            elif j:
                row[j] += row[j - 1]            # up (old row[j]) + left (new row[j-1])
            # j == 0, i > 0, free: row[0] keeps the value from above, which is right
    return row[-1]

def paths_obs_forgot_zero(grid):
    """WRONG on purpose: blocked cells are skipped instead of zeroed."""
    m, n = len(grid), len(grid[0])
    row = [0] * n
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                continue
            if i == 0 and j == 0:
                row[j] = 1
            elif j:
                row[j] += row[j - 1]
    return row[-1]

def paths_obs_plain(grid):
    """Oracle: plain recursion, no memo."""
    m, n = len(grid), len(grid[0])
    def f(i, j):
        if grid[i][j]:
            return 0
        if i == m - 1 and j == n - 1:
            return 1
        return (f(i + 1, j) if i + 1 < m else 0) + (f(i, j + 1) if j + 1 < n else 0)
    return f(0, 0)

def paths_obs_memo(grid):
    m, n = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def f(i, j):
        if grid[i][j]:
            return 0
        if i == m - 1 and j == n - 1:
            return 1
        return (f(i + 1, j) if i + 1 < m else 0) + (f(i, j + 1) if j + 1 < n else 0)
    return f(0, 0)

for g, want in [([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2), ([[0, 1], [0, 0]], 1), ([[1, 0]], 0),
                ([[0, 0], [0, 1]], 0), ([[0]], 1)]:
    assert paths_obs(g) == paths_obs_table(g)[-1][-1] == paths_obs_plain(g) == paths_obs_memo(g) == want, g
print("5 prompt examples ok")

g = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
print("walk-through grid:", g)
for r in paths_obs_table(g):
    print("  table row:", r)
row = [0] * 3
for i in range(3):
    for j in range(3):
        if g[i][j] == 1:
            row[j] = 0
        elif i == 0 and j == 0:
            row[j] = 1
        elif j:
            row[j] += row[j - 1]
    print("  one row after grid row", i, ":", row)

# exhaustive: every grid of shape (m, n) with m, n in 1..3, all 0/1 contents
cnt = 0
for m in range(1, 4):
    for n in range(1, 4):
        for cells in itertools.product((0, 1), repeat=m * n):
            grid = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
            assert paths_obs(grid) == paths_obs_plain(grid) == paths_obs_table(grid)[-1][-1], grid
            cnt += 1
print("exhaustive: all", cnt, "grids with m, n in 1..3: row == table == plain recursion")

for _ in range(500):
    m, n = random.randint(1, 5), random.randint(1, 5)
    p = random.choice([0.1, 0.25, 0.4])
    grid = [[1 if random.random() < p else 0 for _ in range(n)] for _ in range(m)]
    assert paths_obs(grid) == paths_obs_plain(grid) == paths_obs_memo(grid), grid
print("500 seeded random grids (m, n <= 5, block rate 10/25/40%): ok")

# claim: skipping instead of zeroing a blocked cell is wrong. Test it exactly.
wrong = total = 0
first = None
for m in range(1, 4):
    for n in range(1, 4):
        for cells in itertools.product((0, 1), repeat=m * n):
            grid = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
            total += 1
            if paths_obs_forgot_zero(grid) != paths_obs_plain(grid):
                wrong += 1
                if first is None and m > 1:
                    first = (grid, paths_obs_forgot_zero(grid), paths_obs_plain(grid))
print("forgetting to zero a blocked cell is wrong on", wrong, "of", total, "small grids; first with m > 1:", first)

# the start/end rules
assert paths_obs([[1]]) == 0 and paths_obs([[0, 0], [0, 1]]) == 0 and paths_obs([[1, 0], [0, 0]]) == 0
print("blocked start -> 0, blocked end -> 0, 1 x 1 blocked -> 0: ok")

# size check: 100 x 100 empty grid equals the unique-paths count; memo depth stays about m + n
big = [[0] * 100 for _ in range(100)]
print("100 x 100 empty grid:", paths_obs(big) == paths_obs_memo(big), "(memo depth about 200, default limit", sys.getrecursionlimit(), ")")
# a 100 x 100 grid with a random 3% of cells blocked, row version vs table
big2 = [[1 if random.random() < 0.03 else 0 for _ in range(100)] for _ in range(100)]
big2[0][0] = big2[-1][-1] = 0
print("100 x 100 random 3% blocked: row == table:", paths_obs(big2) == paths_obs_table(big2)[-1][-1], "paths:", paths_obs(big2))
```

**Output (my run):**
```
5 prompt examples ok
walk-through grid: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
  table row: [1, 1, 1]
  table row: [1, 0, 1]
  table row: [1, 1, 2]
  one row after grid row 0 : [1, 1, 1]
  one row after grid row 1 : [1, 0, 1]
  one row after grid row 2 : [1, 1, 2]
exhaustive: all 682 grids with m, n in 1..3: row == table == plain recursion
500 seeded random grids (m, n <= 5, block rate 10/25/40%): ok
forgetting to zero a blocked cell is wrong on 210 of 682 small grids; first with m > 1: ([[0], [1]], 1, 0)
blocked start -> 0, blocked end -> 0, 1 x 1 blocked -> 0: ok
100 x 100 empty grid: True (memo depth about 200, default limit 1000 )
100 x 100 random 3% blocked: row == table: True paths: 80388713916727791708092888398206924862625780650048271672
```

**Edge cases:**
- Start blocked: 0. End blocked: 0 (both tested). `[[1]]` is 0, `[[0]]` is 1.
- A single row or column with a wall in it: 0.
- A wall that cuts the grid (full anti-diagonal of ones): 0.
- Answers can be huge on big open grids; do not apply a modulus unless the problem asks.

**Follow-ups:**
- Obstacles given as coordinates only? Same DP over a dense table, or sort the obstacles and use inclusion-exclusion with binomials if the grid is huge and obstacles are few.
- Can you also return one path? Keep the table on suffixes and walk; see Q14 for the tie-rule version.
- Moves in 4 directions? Then it is no longer a DAG; that is BFS or Dijkstra, not this DP.

**Common mistakes:**
- Not zeroing a blocked cell in the one-row version (stale count leaks).
- Setting `dp[0][0] = 1` without checking that the start is free.
- Initialising the first row to all 1s even after an obstacle.
- Reading `dp[i-1][j]` for i = 0 (index -1 silently wraps in Python and gives the last row).

---

### Q3 ⭐⭐⭐ 🟡 Minimum path sum. `grid` is an m x n list of lists (1 <= m, n <= 200) of integers in 0..100. Move only right or down from the top-left to the bottom-right cell; return the smallest possible sum of the cells on the path, including both ends. Give the state and transition, the one-row version, and explain why a greedy choice (always step to the cheaper neighbour) fails with a small counter-example. Return the value only (the path itself is a separate question). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (m, n <= 5) on small inputs. Example: grid=[[1, 3, 1], [1, 5, 1], [4, 2, 1]] -> 7; grid=[[1, 2, 3], [4, 5, 6]] -> 12; grid=[[7]] -> 7; grid=[[1, 2, 5], [3, 2, 1]] -> 6.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2020 on-campus Naukri Code360 report with a longest palindromic substring solved by a 2-D boolean DP table, a 2024 off-campus SDE-1 LeetCode Discuss report with a 2D DP array-splitting question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Grid DP, optimising (min). Same shape as Q1 with `min` and cell costs in place of `+` and counts.

**Say this first (1 line):** "dp[i][j] is the cheapest sum of a path from the top-left to (i, j) inclusive: grid[i][j] plus the smaller of up and left; first row and column have only one way in, so they are running sums. O(m*n) time, one row of space. Greedy fails because a cheap step can lead into an expensive region."

**Brute force:** Recursion over every right/down path: `f(i, j) = grid[i][j] + min(f(i+1, j), f(i, j+1))`. There are C(m+n-2, m-1) paths, so it is exponential. Memoising on `(i, j)` makes it O(m*n).

**Optimal:**
- State: `dp[i][j]` = minimum sum over all right/down paths from (0, 0) to (i, j), both cells included.
- Transition: the last step came from above or from the left, so `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`.
- Base: `dp[0][0] = grid[0][0]`. First row: only the left neighbour exists, so it is a running sum; first column likewise. In code I treat a missing neighbour as infinity, which handles both.
- One row: `row[j]` is the above value until overwritten, `row[j-1]` the already-updated left value, so `row[j] = grid[i][j] + min(row[j], row[j-1])` with j ascending. Initialise `row = [INF] * n; row[0] = 0`: a virtual zero-cost cell above (0, 0) makes the first row come out right with no special case.
- Why greedy fails: it looks one step ahead only. On `[[1,3,1],[2,9,1]]` greedy sees 3 (right) versus 2 (down), takes 2, and is forced through the 9: total 1+2+9+1 = 13. The optimal path goes right, right, down: 1+3+1+1 = 6. My code also finds by exhaustive search the smallest counter-example by cell total over 2 x 3 grids with values 0..9, `[[0,1,0],[0,2,0]]` (greedy 2, optimal 1), and measures that greedy was wrong on 141 of 500 random grids at this seed.
- Value only. The path needs either parent pointers or a suffix table, see Q14.

**Complexity:** Time O(m*n), space O(n) (O(m*n) for the full table). Values are at most 100, so sums are at most about 40,000; nothing overflows anyway.

**Dry run:** `grid = [[1,3,1],[1,5,1],[4,2,1]]`.

| dp | j=0 | j=1 | j=2 |
|---|---|---|---|
| row 0 | 1 | 4 (1+3) | 5 (4+1) |
| row 1 | 2 (1+1) | 7 (5 + min(4, 2)) | 6 (1 + min(5, 7)) |
| row 2 | 6 (4+2) | 8 (2 + min(7, 6)) | 7 (1 + min(6, 8)) |

Answer 7, path 1 -> 3 -> 1 -> 1 -> 1 (right, right, down, down). The one-row version prints exactly these three rows in turn.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1103)
INF = float('inf')

def min_path_table(grid):
    """dp[i][j] = cheapest sum from (0,0) to (i,j), both ends included."""
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                dp[i][j] = grid[0][0]
            else:
                dp[i][j] = grid[i][j] + min(dp[i - 1][j] if i else INF, dp[i][j - 1] if j else INF)
    return dp

def min_path_row(grid):
    """One row: row[j] is 'up' until overwritten, then 'this cell'. Ascending j so row[j-1] is 'left'."""
    n = len(grid[0])
    row = [INF] * n
    row[0] = 0                                   # virtual cell above (0,0) costs 0
    for r in grid:
        for j in range(n):
            row[j] = r[j] + min(row[j], row[j - 1] if j else INF)
    return row[-1]

def min_path_plain(grid):
    """Oracle: plain recursion, no memo."""
    m, n = len(grid), len(grid[0])
    def f(i, j):
        if i == m - 1 and j == n - 1:
            return grid[i][j]
        return grid[i][j] + min(f(i + 1, j) if i + 1 < m else INF, f(i, j + 1) if j + 1 < n else INF)
    return f(0, 0)

def min_path_memo(grid):
    m, n = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == m - 1 and j == n - 1:
            return grid[i][j]
        return grid[i][j] + min(f(i + 1, j) if i + 1 < m else INF, f(i, j + 1) if j + 1 < n else INF)
    return f(0, 0)

def greedy(grid):
    """Always step to the cheaper neighbour (ties go right). Not correct."""
    m, n = len(grid), len(grid[0])
    i = j = 0
    total = grid[0][0]
    while (i, j) != (m - 1, n - 1):
        if i == m - 1:
            j += 1
        elif j == n - 1:
            i += 1
        elif grid[i][j + 1] <= grid[i + 1][j]:
            j += 1
        else:
            i += 1
        total += grid[i][j]
    return total

for g, want in [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7), ([[1, 2, 3], [4, 5, 6]], 12), ([[7]], 7), ([[1, 2, 5], [3, 2, 1]], 6)]:
    assert min_path_row(g) == min_path_table(g)[-1][-1] == min_path_plain(g) == min_path_memo(g) == want, g
print("4 prompt examples ok")

g = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
print("walk-through grid:", g)
for r in min_path_table(g):
    print("  table row:", r)
row = [INF, INF, INF]; row[0] = 0
for i, r in enumerate(g):
    for j in range(3):
        row[j] = r[j] + min(row[j], row[j - 1] if j else INF)
    print("  one row after grid row", i, ":", row)

# smallest greedy counter-example by exhaustive search: 2 x 3 grids, values 0..9, fewest total, no tie at any greedy choice
best = None
for cells in itertools.product(range(10), repeat=6):
    grid = [list(cells[:3]), list(cells[3:])]
    if greedy(grid) != min_path_plain(grid):
        key = (sum(cells), cells)
        if best is None or key < best[0]:
            best = (key, grid)
cg = best[1]
print("smallest 2x3 counter-example by cell total:", cg, "greedy =", greedy(cg), "optimal =", min_path_plain(cg))
cg2 = [[1, 3, 1], [2, 9, 1]]
print("hand example", cg2, "greedy =", greedy(cg2), "optimal =", min_path_plain(cg2))

# exhaustive: all 2x3 and 3x2 grids with values 0..3, and 3x3 with values 0..2
cnt = 0
for (m, n, vmax) in [(1, 4, 3), (2, 2, 4), (2, 3, 3), (3, 2, 3), (3, 3, 2)]:
    for cells in itertools.product(range(vmax), repeat=m * n):
        grid = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
        assert min_path_row(grid) == min_path_plain(grid) == min_path_table(grid)[-1][-1], grid
        cnt += 1
print("exhaustive:", cnt, "small grids: row == table == plain recursion")
for _ in range(500):
    m, n = random.randint(1, 5), random.randint(1, 5)
    grid = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
    assert min_path_row(grid) == min_path_plain(grid) == min_path_memo(grid)
print("500 seeded random grids (m, n <= 5, values 0..100): ok")

# how often does greedy fail on random grids?
fails = 0
for _ in range(500):
    m, n = random.randint(2, 5), random.randint(2, 5)
    grid = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
    fails += greedy(grid) != min_path_plain(grid)
print("greedy was wrong on", fails, "of 500 random grids (this seed)")

big = [[random.randint(0, 100) for _ in range(200)] for _ in range(200)]
print("200 x 200 row == table:", min_path_row(big) == min_path_table(big)[-1][-1], "->", min_path_row(big))
print("200 x 200 memo (depth about 399 frames, limit", sys.getrecursionlimit(), "):", min_path_memo(big) == min_path_row(big))
```

**Output (my run):**
```
4 prompt examples ok
walk-through grid: [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
  table row: [1, 4, 5]
  table row: [2, 7, 6]
  table row: [6, 8, 7]
  one row after grid row 0 : [1, 4, 5]
  one row after grid row 1 : [2, 7, 6]
  one row after grid row 2 : [6, 8, 7]
smallest 2x3 counter-example by cell total: [[0, 1, 0], [0, 2, 0]] greedy = 2 optimal = 1
hand example [[1, 3, 1], [2, 9, 1]] greedy = 13 optimal = 6
exhaustive: 2307 small grids: row == table == plain recursion
500 seeded random grids (m, n <= 5, values 0..100): ok
greedy was wrong on 141 of 500 random grids (this seed)
200 x 200 row == table: True -> 10054
200 x 200 memo (depth about 399 frames, limit 1000 ): True
```

**Edge cases:**
- 1 x 1 returns the cell itself (`[[7]]` -> 7).
- 1 x n or m x 1: the sum of the whole line.
- All zeros returns 0. Ties between up and left are harmless for the value.
- Starting `row` as `[0] * n` is a bug: it lets the first row choose a free cell above it.

**Follow-ups:**
- Return the path? Table on suffixes and a tie rule, Q14.
- Count how many paths achieve the minimum? Carry a second table of counts, add counts on ties.
- Negative cells? The DP is unchanged (it is a DAG); only a greedy or Dijkstra would break.
- 4-direction moves? Then it is Dijkstra, not this DP.

**Common mistakes:**
- Greedy neighbour choice.
- Forgetting the first row and column have one predecessor (indexing -1 wraps to the last column or row in Python).
- Initialising the row to 0 instead of INF with a zero seed.
- Reading the full table when only the previous row is needed (fine for correctness, wasteful on memory).

---

### Q4 ⭐⭐⭐ 🟡 Triangle: minimum path from top to bottom. `triangle` has 1 <= r <= 200 rows, row i has i + 1 integers (|value| <= 10^4). From index j in a row you may move to index j or j + 1 of the next row. Return the smallest sum from the top to any cell in the last row. Solve it bottom-up in O(r) extra space by overwriting one row, and say why top-down rows need the edge handling that the bottom-up version avoids. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (r <= 8) on small inputs. Example: triangle=[[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]] -> 11; triangle=[[-10]] -> -10; triangle=[[1], [2, 3]] -> 3; triangle=[[-1], [2, 3], [1, -1, -3]] -> -1.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Triangle DP, optimising (min), solved bottom-up so the answer collapses into one cell.

**Say this first (1 line):** "From cell (r, j) the best remaining sum is its value plus the smaller of its two children; start from the last row, fold upwards, and the answer is dp[0]. One array of length r, O(r^2) time."

**Brute force:** Recursion from the apex: `f(r, j) = t[r][j] + min(f(r+1, j), f(r+1, j+1))`. There are 2^(r-1) paths, so it is exponential without a memo. Memoised it is O(r^2) states.

**Optimal:**
- State: `dp[j]` after processing row r = the minimum sum from cell (r, j) down to the last row.
- Base: the last row: `dp = triangle[-1]` (copy it, do not mutate the input).
- Transition: for r from the second-last row up to 0, `dp[j] = t[r][j] + min(dp[j], dp[j+1])` for j = 0..r. Row r has r+1 cells and row r+1 has r+2, so both children `j` and `j+1` always exist: no edge case.
- In-place safety: `dp[j]` and `dp[j+1]` are read before `dp[j]` is overwritten, and `dp[j+1]` is only overwritten later (when going to j+1, which is not needed again). Ascending j works here.
- Why top-down needs edge handling: forward, cell (r, j) has parents (r-1, j-1) and (r-1, j). The leftmost cell (j = 0) has no up-left parent and the rightmost (j = r) has no up parent, so you need `INF` guards (or you wrap to index -1 in Python, silently wrong). You also have to `min(...)` the final row, and an in-place one-row forward version must run j descending. I tested that: ascending j in the in-place forward version is wrong on 34,638 of 59,805 small triangles with r from 2 to 4. Bottom-up has none of these problems.

**Complexity:** Time O(r^2) (one visit per cell, r(r+1)/2 cells). Space O(r) for `dp`. With r <= 200 that is about 20,000 cell visits.

**Dry run:** `[[2],[3,4],[6,5,7],[4,1,8,3]]`.

| step | dp |
|---|---|
| start (last row) | [4, 1, 8, 3] |
| row 2: 6+min(4,1), 5+min(1,8), 7+min(8,3) | [7, 6, 10] |
| row 1: 3+min(7,6), 4+min(6,10) | [9, 10] |
| row 0: 2+min(9,10) | [11] |

Answer 11 (path 2 -> 3 -> 5 -> 1).

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1104)
INF = float('inf')

def tri_bottom_up(triangle):
    """dp starts as the last row. Cell (r, j) has two children (r+1, j) and (r+1, j+1), always in range."""
    dp = list(triangle[-1])                       # copy: do not mutate the caller's input
    for r in range(len(triangle) - 2, -1, -1):
        for j in range(r + 1):
            dp[j] = triangle[r][j] + min(dp[j], dp[j + 1])
    return dp[0]

def tri_top_down(triangle):
    """Top-down rows (forward): cell (r, j) has parents (r-1, j-1) and (r-1, j); the edges miss one."""
    dp = [triangle[0][0]]
    for r in range(1, len(triangle)):
        new = []
        for j in range(r + 1):
            left = dp[j - 1] if j - 1 >= 0 else INF     # leftmost cell has no up-left parent
            right = dp[j] if j <= r - 1 else INF        # rightmost cell has no up parent
            new.append(triangle[r][j] + min(left, right))
        dp = new
    return min(dp)                                       # must scan the last row

def tri_top_down_inplace(triangle, descending=True):
    """One row top-down in place: needs j descending so dp[j-1] is still the previous row."""
    dp = [INF] * len(triangle)
    dp[0] = 0
    for r, row in enumerate(triangle):
        order = range(r, -1, -1) if descending else range(r + 1)
        for j in order:
            dp[j] = row[j] + min(dp[j], dp[j - 1] if j else INF)
    return min(dp[:len(triangle)])

def tri_plain(triangle):
    """Oracle: plain recursion, no memo."""
    def f(r, j):
        return triangle[r][j] + (min(f(r + 1, j), f(r + 1, j + 1)) if r + 1 < len(triangle) else 0)
    return f(0, 0)

def tri_memo(triangle):
    @lru_cache(maxsize=None)
    def f(r, j):
        return triangle[r][j] + (min(f(r + 1, j), f(r + 1, j + 1)) if r + 1 < len(triangle) else 0)
    return f(0, 0)

def make(r, lo=-10, hi=10):
    return [[random.randint(lo, hi) for _ in range(i + 1)] for i in range(r)]

for t, want in [([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]], 11), ([[-10]], -10), ([[1], [2, 3]], 3), ([[-1], [2, 3], [1, -1, -3]], -1)]:
    assert tri_bottom_up(t) == tri_top_down(t) == tri_plain(t) == tri_memo([tuple(x) for x in t]) == want, t
print("4 prompt examples ok")

t = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
print("walk-through triangle:", t)
dp = list(t[-1]); print("  start (last row):", dp)
for r in range(len(t) - 2, -1, -1):
    for j in range(r + 1):
        dp[j] = t[r][j] + min(dp[j], dp[j + 1])
    print("  after row", r, ":", dp[:r + 1])

orig = [list(x) for x in t]
tri_bottom_up(t)
assert t == orig
print("input not mutated: ok")

# exhaustive on all triangles with r <= 4 and values in {-1, 0, 1} (r=4 has 10 cells: 59049)
cnt = 0
for r in range(1, 5):
    for cells in itertools.product((-1, 0, 1), repeat=r * (r + 1) // 2):
        it = iter(cells)
        tri = [[next(it) for _ in range(i + 1)] for i in range(r)]
        o = tri_plain(tri)
        assert tri_bottom_up(tri) == tri_top_down(tri) == tri_top_down_inplace(tri) == o, tri
        cnt += 1
print("exhaustive:", cnt, "triangles (r <= 4, values -1..1): bottom-up == top-down == in-place == plain recursion")
for _ in range(500):
    r = random.randint(1, 8)
    tri = make(r, -10000, 10000)
    assert tri_bottom_up(tri) == tri_top_down(tri) == tri_plain(tri) == tri_top_down_inplace(tri)
print("500 seeded random triangles (r <= 8, |value| <= 10^4): ok")

# claim: the in-place top-down version needs j descending. Test it.
wrong = 0
total = 0
for r in range(2, 5):
    for cells in itertools.product((-1, 0, 1), repeat=r * (r + 1) // 2):
        it = iter(cells)
        tri = [[next(it) for _ in range(i + 1)] for i in range(r)]
        total += 1
        wrong += tri_top_down_inplace(tri, descending=False) != tri_plain(tri)
print("top-down in place with ASCENDING j: wrong on", wrong, "of", total, "small triangles")

# size 200
big = make(200, -10000, 10000)
a = tri_bottom_up(big)
assert a == tri_top_down(big) == tri_top_down_inplace(big)
print("r = 200: bottom-up == top-down == in-place:", a)
print("r = 200 memo (depth 200 frames, limit", sys.getrecursionlimit(), "):", tri_memo([tuple(x) for x in big]) == a)
```

**Output (my run):**
```
4 prompt examples ok
walk-through triangle: [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
  start (last row): [4, 1, 8, 3]
  after row 2 : [7, 6, 10]
  after row 1 : [9, 10]
  after row 0 : [11]
input not mutated: ok
exhaustive: 59808 triangles (r <= 4, values -1..1): bottom-up == top-down == in-place == plain recursion
500 seeded random triangles (r <= 8, |value| <= 10^4): ok
top-down in place with ASCENDING j: wrong on 34638 of 59805 small triangles
r = 200: bottom-up == top-down == in-place: -964713
r = 200 memo (depth 200 frames, limit 1000 ): True
```

**Edge cases:**
- One row: `dp = [value]`, the loop does not run, the answer is that value (`[[-10]]` -> -10).
- Negative values: fine, there is no greedy or pruning that assumes non-negative.
- All values equal: answer is r times the value.
- Mutating the caller's last row: use `list(triangle[-1])`.

**Follow-ups:**
- Print the path? Keep the choice per cell, or rebuild from the full table, walking down choosing the child that matches.
- Maximum instead of minimum? Swap `min` for `max`.
- Memoised version at r = 200? Depth is about r frames, so it works (shown). Keep r well under 1000 for the recursive form (depth is about r frames).

**Common mistakes:**
- Top-down with no guards: `dp[j-1]` for j = 0 reads the last element.
- Forgetting to take the minimum over the final row in the top-down version.
- Overwriting the caller's triangle.
- Looping j to `len(row)` of the wrong row and indexing `dp[j+1]` out of range.

---

### Q5 ⭐⭐⭐ 🟡 Maximal square. `matrix` is a list of m strings of equal length n (1 <= m, n <= 300) made of '0' and '1'. Return the AREA of the largest square sub-block that contains only '1' (0 if there is none). Define `dp[i][j]` as the side of the largest all-ones square whose bottom-right corner is (i, j), derive `1 + min(up, left, up-left)`, justify the min with a small picture in words, and use two rows (or one row plus a saved diagonal value) instead of the full table. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a brute force that tests every square (m, n <= 6) on small inputs. Example: matrix=['10100', '10111', '11111', '10010'] -> 4; matrix=['01', '10'] -> 1; matrix=['0'] -> 0; matrix=['11', '11'] -> 4.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP on "largest shape ending at this cell" (bottom-right corner state).

**Say this first (1 line):** "side[i][j] is the side of the largest all-ones square whose bottom-right corner is (i, j): 0 if the cell is '0', else 1 + min(up, left, up-left). Answer is the biggest side squared. O(m*n) time, O(n) space with two rows."

**Brute force:** For every top-left corner and every side length k, check all k*k cells. That is O(m*n*min(m,n)^3) with the naive check. Fine for 6 x 6, hopeless for 300 x 300.

**Optimal:**
- State: `side[i][j]` = side length of the largest square of all '1' with (i, j) as its bottom-right corner. A cell contains a square only ending at it, so every square is counted at exactly its own corner; the answer is the max over all cells, not the last cell.
- Transition: `'0'` gives 0. `'1'` gives `1 + min(side[i-1][j], side[i][j-1], side[i-1][j-1])`.
- Why the min, in words. Suppose a k x k square of ones ends at (i, j). Remove the corner cell and you can see three overlapping (k-1) x (k-1) squares: one ending directly above (i-1, j), one ending directly left (i, j-1), one ending up-left (i-1, j-1). Together they cover the whole k x k block except the corner. So all three neighbours have side at least k-1. Conversely, if all three neighbours have side at least s and the corner is '1', their squares fit together and the k = s+1 square is all ones. So the best k is exactly 1 + the smallest of the three. The up-left term is needed: it can be 0 (a hole in the middle) while up and left are large. I tested the version without it: wrong on 98 of the 512 matrices of size 3 x 3 (for example `['000','001','011']` gives area 4, true answer 1).
- Base: pad the table with an extra row and column of zeros, so no index guards are needed.
- Two rows: `prev` and `cur`, each of length n+1 (index 0 is the zero pad). One row plus a saved `diag` also works: `diag` stores the old `row[j-1]` before it is overwritten. In that version a '0' cell must be written back as 0 explicitly, otherwise the value from the row above survives.

**Complexity:** Time O(m*n). Space O(n) for two rows (O(m*n) for the full table). Return area = best^2, not the side.

**Dry run:** `['10100','10111','11111','10010']`. The side table:

| i\j | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 2 | 2 |
| 3 | 1 | 0 | 0 | 1 | 0 |

Cell (2, 3): it is '1', up `side[1][3]` = 1, left `side[2][2]` = 1, up-left `side[1][2]` = 1, so 1 + 1 = 2. Largest side 2, area 4.

**Code:**
```python
import itertools
import random

random.seed(1105)

def max_square_table(matrix):
    """side[i][j] = side of the largest all-ones square with bottom-right corner (i, j). Padded with a 0 row/col."""
    m, n = len(matrix), len(matrix[0])
    side = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                side[i][j] = 1 + min(side[i - 1][j], side[i][j - 1], side[i - 1][j - 1])
                best = max(best, side[i][j])
    return side, best * best

def max_square_two_rows(matrix):
    n = len(matrix[0])
    prev = [0] * (n + 1)
    best = 0
    for row in matrix:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if row[j - 1] == '1':
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
                best = max(best, cur[j])
        prev = cur
    return best * best

def max_square_one_row(matrix):
    """One row plus a saved diagonal: diag = old row[j-1] (the up-left value) before it is overwritten."""
    n = len(matrix[0])
    row = [0] * (n + 1)
    best = 0
    for r in matrix:
        diag = 0                                    # up-left of column 1 is the padding 0
        for j in range(1, n + 1):
            up = row[j]                             # old value = cell above
            if r[j - 1] == '1':
                row[j] = 1 + min(up, row[j - 1], diag)   # row[j-1] already new = left
                best = max(best, row[j])
            else:
                row[j] = 0                          # MUST reset: stale 'up' would otherwise survive
            diag = up
    return best * best

def max_square_no_diag(matrix):
    """WRONG on purpose: min(up, left) only."""
    m, n = len(matrix), len(matrix[0])
    side = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                side[i][j] = 1 + min(side[i - 1][j], side[i][j - 1])
                best = max(best, side[i][j])
    return best * best

def max_square_brute(matrix):
    """Oracle: try every top-left corner and every side length, check all cells."""
    m, n = len(matrix), len(matrix[0])
    best = 0
    for i in range(m):
        for j in range(n):
            for k in range(1, min(m - i, n - j) + 1):
                if all(matrix[a][b] == '1' for a in range(i, i + k) for b in range(j, j + k)):
                    best = max(best, k)
    return best * best

for mat, want in [(['10100', '10111', '11111', '10010'], 4), (['01', '10'], 1), (['0'], 0), (['11', '11'], 4)]:
    assert max_square_table(mat)[1] == max_square_two_rows(mat) == max_square_one_row(mat) == max_square_brute(mat) == want, mat
print("4 prompt examples ok")

mat = ['10100', '10111', '11111', '10010']
print("walk-through matrix:", mat)
side, area = max_square_table(mat)
for r in side[1:]:
    print("  side row:", r[1:])
print("  largest side", int(area ** 0.5), "-> area", area)

def grids(m, n):
    for cells in itertools.product('01', repeat=m * n):
        yield [''.join(cells[i * n:(i + 1) * n]) for i in range(m)]

cnt = 0
for m in range(1, 5):
    for n in range(1, 5):
        for g in grids(m, n):
            b = max_square_brute(g)
            assert max_square_table(g)[1] == max_square_two_rows(g) == max_square_one_row(g) == b, g
            cnt += 1
print("exhaustive: all", cnt, "binary matrices with m, n in 1..4: table == two rows == one row == brute force")
for _ in range(500):
    m, n = random.randint(1, 6), random.randint(1, 6)
    p = random.choice([0.5, 0.8, 0.95])
    g = [''.join('1' if random.random() < p else '0' for _ in range(n)) for _ in range(m)]
    assert max_square_two_rows(g) == max_square_brute(g) == max_square_one_row(g)
print("500 seeded random matrices (m, n <= 6, density 50/80/95%): ok")

# claim: dropping the up-left term is wrong; find where
bad = [g for g in grids(3, 3) if max_square_no_diag(g) != max_square_brute(g)]
print("min(up, left) without up-left is wrong on", len(bad), "of 512 3x3 matrices; e.g.", bad[0], "gives", max_square_no_diag(bad[0]), "not", max_square_brute(bad[0]))

big = [''.join('1' if random.random() < 0.97 else '0' for _ in range(300)) for _ in range(300)]
a = max_square_two_rows(big)
assert a == max_square_table(big)[1] == max_square_one_row(big)
print("300 x 300 (97% ones): largest square area", a, "(side", int(a ** 0.5), "); table == two rows == one row")
full = ['1' * 300] * 300
print("300 x 300 all ones:", max_square_two_rows(full), "= 300^2:", max_square_two_rows(full) == 90000)
```

**Output (my run):**
```
4 prompt examples ok
walk-through matrix: ['10100', '10111', '11111', '10010']
  side row: [1, 0, 1, 0, 0]
  side row: [1, 0, 1, 1, 1]
  side row: [1, 1, 1, 2, 2]
  side row: [1, 0, 0, 1, 0]
  largest side 2 -> area 4
exhaustive: all 74954 binary matrices with m, n in 1..4: table == two rows == one row == brute force
500 seeded random matrices (m, n <= 6, density 50/80/95%): ok
min(up, left) without up-left is wrong on 98 of 512 3x3 matrices; e.g. ['000', '001', '011'] gives 4 not 1
300 x 300 (97% ones): largest square area 324 (side 18 ); table == two rows == one row
300 x 300 all ones: 90000 = 300^2: True
```

**Edge cases:**
- All zeros: 0 (return area 0, not side 1).
- All ones: min(m, n)^2 (300 x 300 gives 90000).
- A single row or column: 1 if any '1', else 0.
- The area, not the side, is the answer (`['0']` -> 0, `['11','11']` -> 4).

**Follow-ups:**
- Largest rectangle of ones? Different DP: heights plus a monotonic stack per row (Part 4).
- Count all all-ones squares? Sum the `side` table: a corner with side k adds k squares.
- Input as ints instead of strings? Change `== '1'` to `== 1`; do not compare `'1' == 1`.

**Common mistakes:**
- Using `min(up, left)` only.
- Returning the side, or the max of the last cell only.
- In the one-row version, not resetting a '0' cell and not saving the diagonal before overwriting.
- Treating input characters as ints.

---

### Q6 ⭐⭐⭐ 🟡 Longest common subsequence (length). `a` and `b` are lowercase strings with 0 <= len <= 1000 each. Return the length of their longest common subsequence (characters in the same order in both, not necessarily adjacent; 0 if either is empty). Define `dp[i][j]`, give both cases of the transition, then use two rows indexed by the shorter string and state the extra space. Contrast it with the concept-level treatment in Part 3 Q35. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). Mention that rolling layers is the same idea as the transaction layers of Part 10 Q29. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (len <= 8) on small inputs. Example: a='abcde', b='ace' -> 3; a='abc', b='def' -> 0; a='', b='abc' -> 0; a='abcba', b='abcbcba' -> 5.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-sequence DP on prefixes (the "LCS family": edit distance, supersequence, ASCII delete sum, interleaving all share this table).

**Say this first (1 line):** "dp[i][j] is the LCS length of the first i letters of a and the first j of b: if the last letters match it is dp[i-1][j-1] + 1, otherwise the better of dropping one last letter. O(m*n) time; I keep two rows indexed by the shorter string, so O(min(m, n)) extra space; bottom-up because a memoised recursion can pass the recursion limit."

**Brute force:** Recursion on suffixes: `f(i, j) = 1 + f(i+1, j+1)` if `a[i] == b[j]`, else `max(f(i+1, j), f(i, j+1))`; 0 when either string is used up. Without a memo it is exponential. Another brute force is to enumerate all 2^m subsequences of `a` and test each against `b`.

**Optimal:**
- State: `dp[i][j]` = LCS length of `a[:i]` and `b[:j]`.
- Base: `dp[0][j] = dp[i][0] = 0` (an empty prefix has nothing in common).
- Transition, case 1: `a[i-1] == b[j-1]`. Matching these two letters is never worse than skipping either, so `dp[i][j] = dp[i-1][j-1] + 1`.
- Transition, case 2: they differ, so at most one of them is in the common subsequence at the end: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
- Answer: `dp[m][n]`.
- Two rows: row i needs only row i-1 and the cell to its left in row i. Make the columns the shorter string, so the rows have length min(m, n) + 1. Space O(min(m, n)). One row plus a saved diagonal also works (the code checks it).
- Contrast with Part 3 Q35: there the idea is shown at concept level with a memoised recursion. Here the table is filled bottom-up, with space optimisation, and the recursion-limit consequence is part of the answer.
- Rolling layers is the same trick as the transaction layers of Part 10 Q29: the layer index (here the row i, there the number of transactions k) is the outer loop, and only the previous layer is kept.
- Recursion limit, observed on Python 3.13 at the default limit of 1000: the memoised top-down version has depth up to m + n (each call moves i or j one step). On two completely different strings of length n each it passed at n = 100, 300 and 400 and raised `RecursionError` at n = 1000; on two random 1000-letter strings it also raised. The bottom-up version has no recursion and handled 1000 x 1000. Raising the limit is not the fix asked for here.

**Complexity:** Time O(m*n) (1,000,000 cell updates at the maximum size). Space O(min(m, n)) for two rows, O(m*n) for the full table. The recursion without a memo is exponential.

**Dry run:** `a = 'abcde'`, `b = 'ace'`.

| prefix of a \ prefix of b | '' | a | ac | ace |
|---|---|---|---|---|
| '' | 0 | 0 | 0 | 0 |
| a | 0 | 1 | 1 | 1 |
| ab | 0 | 1 | 1 | 1 |
| abc | 0 | 1 | 2 | 2 |
| abcd | 0 | 1 | 2 | 2 |
| abcde | 0 | 1 | 2 | 3 |

Row `abc`, column `ac`: the last letters match (`c`), so 1 + dp[ab][a] = 1 + 1 = 2. Row `abcde`, column `ace`: `e` matches `e`, so 1 + dp[abcd][ac] = 3. The answer is 3 (`ace`).

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1106)

def lcs_table(a, b):
    """dp[i][j] = LCS length of a[:i] and b[:j]. Row 0 and column 0 are 0 (empty prefix)."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp

def lcs_two_rows(a, b):
    """Two rows indexed by the SHORTER string: extra space O(min(m, n))."""
    if len(b) > len(a):
        a, b = b, a                              # b is now the shorter one
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def lcs_one_row(a, b):
    """One row plus a saved diagonal."""
    if len(b) > len(a):
        a, b = b, a
    row = [0] * (len(b) + 1)
    for ch in a:
        diag = 0                                 # old row[j-1]
        for j in range(1, len(b) + 1):
            up = row[j]
            row[j] = diag + 1 if ch == b[j - 1] else max(up, row[j - 1])
            diag = up
    return row[-1]

def lcs_plain(a, b):
    """Oracle: plain recursion, no memo."""
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def lcs_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

for (a, b), want in [(('abcde', 'ace'), 3), (('abc', 'def'), 0), (('', 'abc'), 0), (('abcba', 'abcbcba'), 5)]:
    assert lcs_two_rows(a, b) == lcs_table(a, b)[-1][-1] == lcs_one_row(a, b) == lcs_plain(a, b) == lcs_memo(a, b) == want, (a, b)
print("4 prompt examples ok")

a, b = 'abcde', 'ace'
print("walk-through a =", a, " b =", b, " (rows = prefixes of a, columns = prefixes of b)")
print("        ", ["''"] + list(b))
for i, r in enumerate(lcs_table(a, b)):
    print("  ", ("'" + a[:i] + "'").ljust(8), r)

# exhaustive: all pairs over {a,b}, lengths 0..5
cnt = 0
for la in range(6):
    for lb in range(6):
        for x in itertools.product('ab', repeat=la):
            for y in itertools.product('ab', repeat=lb):
                x_, y_ = ''.join(x), ''.join(y)
                assert lcs_two_rows(x_, y_) == lcs_plain(x_, y_) == lcs_one_row(x_, y_), (x_, y_)
                cnt += 1
print("exhaustive over {a,b}, lengths 0..5:", cnt, "pairs: two rows == one row == plain recursion")
for _ in range(500):
    x = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    y = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    assert lcs_two_rows(x, y) == lcs_plain(x, y) == lcs_table(x, y)[-1][-1] == lcs_memo(x, y)
    assert lcs_two_rows(x, y) == lcs_two_rows(y, x)
print("500 seeded random pairs (len <= 8, alphabet abcd): ok; symmetric in (a, b)")

# size 1000: bottom-up works; memoised recursion nests deeper than the default limit
def letters(n, alpha):
    return ''.join(random.choice(alpha) for _ in range(n))
A, B = letters(1000, 'abcdefghijklmnopqrstuvwxyz'), letters(1000, 'abcdefghijklmnopqrstuvwxyz')
v = lcs_two_rows(A, B)
assert v == lcs_table(A, B)[-1][-1] == lcs_one_row(A, B)
print("1000 x 1000 random letters: LCS =", v, "(two rows == full table == one row)")
print("identical strings of 1000:", lcs_two_rows('a' * 1000, 'a' * 1000))
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x, y):
    try:
        return "ok" if lcs_memo(x, y) == lcs_two_rows(x, y) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion, disjoint strings (worst depth m + n):")
for n in (100, 300, 400, 1000):
    print("   n = %4d each: %s" % (n, memo_outcome('a' * n, 'b' * n)))
print("memoised recursion, 1000 x 1000 random letters:", memo_outcome(A, B))
```

**Output (my run):**
```
4 prompt examples ok
walk-through a = abcde  b = ace  (rows = prefixes of a, columns = prefixes of b)
         ["''", 'a', 'c', 'e']
   ''       [0, 0, 0, 0]
   'a'      [0, 1, 1, 1]
   'ab'     [0, 1, 1, 1]
   'abc'    [0, 1, 2, 2]
   'abcd'   [0, 1, 2, 2]
   'abcde'  [0, 1, 2, 3]
exhaustive over {a,b}, lengths 0..5: 3969 pairs: two rows == one row == plain recursion
500 seeded random pairs (len <= 8, alphabet abcd): ok; symmetric in (a, b)
1000 x 1000 random letters: LCS = 322 (two rows == full table == one row)
identical strings of 1000: 1000
recursion limit: 1000
memoised recursion, disjoint strings (worst depth m + n):
   n =  100 each: ok
   n =  300 each: ok
   n =  400 each: ok
   n = 1000 each: RecursionError
memoised recursion, 1000 x 1000 random letters: RecursionError
```

**Edge cases:**
- Either string empty: 0 (tested).
- Identical strings: the length of the string (tested at 1000).
- No common letter: 0.
- Symmetry: `LCS(a, b) == LCS(b, a)`, which is why swapping to index by the shorter string is safe.
- A subsequence, not a substring: letters may be non-adjacent.

**Follow-ups:**
- Print the string itself? Walk the table; the tie rule matters, see Q10.
- Shortest common supersequence length? `m + n - LCS` (Q16).
- Minimum deletions to make two strings equal? `m + n - 2 * LCS`.
- Longest common substring? Reset to 0 on mismatch, take the max cell (Q11).

**Common mistakes:**
- Not resetting `cur` per row (or reusing one list without saving the diagonal).
- Using `dp[i-1][j-1] + 1` unconditionally, i.e. forgetting the equal-letter condition.
- Memoised recursion at m, n = 1000: `RecursionError` at the default limit.
- Confusing subsequence with substring.

---

### Q7 ⭐⭐⭐ 🟡 Longest palindromic subsequence (length). `s` is a lowercase string with 1 <= len <= 2000. Return the length of the longest subsequence that reads the same forwards and backwards (not necessarily contiguous; the contiguous version is Part 3 Q8). Give the interval recurrence on `dp[i][j]` (equal ends: 2 + inside; otherwise the better of dropping either end), the order in which i and j must be filled, and then the link `LPS(s) = LCS(s, reversed s)`. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). Add one line on the minimum number of insertions (or deletions) that make `s` a palindrome. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against all subsequences enumerated (len <= 12), and the LCS-with-the-reverse formulation on small inputs. Example: s='bbbab' -> 4; s='cbbd' -> 2; s='a' -> 1; s='abcd' -> 1; s='agbdba' -> 5.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2020 on-campus Naukri Code360 report with a longest palindromic substring solved by a 2-D boolean DP table, a 2024 off-campus SDE-1 LeetCode Discuss report with a 2D DP array-splitting question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Interval DP (state is a range [i, j]; shorter ranges first), with a bridge to the LCS table.

**Say this first (1 line):** "dp[i][j] is the longest palindromic subsequence inside s[i..j]: if the ends match it is 2 + dp[i+1][j-1], otherwise the better of dp[i+1][j] and dp[i][j-1]; fill i from the end down and j upwards. It equals LCS(s, reverse s). O(n^2) time; bottom-up because the recursion depth can reach n."

**Brute force:** Enumerate all 2^n subsequences and keep the longest palindrome: O(n * 2^n). Or the plain recursion `f(i, j)` below with no memo, exponential.

**Optimal:**
- State: `dp[i][j]` = length of the longest palindromic subsequence of `s[i..j]` (inclusive).
- Base: `dp[i][i] = 1` (one letter). An empty range (i > j) is 0; that case arises for `dp[i+1][j-1]` when j = i+1, and the code guards it.
- Transition, ends equal: `s[i] == s[j]`. Wrapping both ends around the best palindrome inside is optimal: `dp[i][j] = 2 + dp[i+1][j-1]`.
- Transition, ends differ: they cannot both be used, so `dp[i][j] = max(dp[i+1][j], dp[i][j-1])` (drop the left end, or drop the right end).
- Fill order: `dp[i][j]` depends on the row below (i+1) and the cell to its left (j-1), so i runs from n-1 down to 0 and j ascends from i+1 to n-1 (any order that finishes shorter ranges first works, for example by length).
- One row: `dp[j]` holds `dp[i+1][j]` until it is overwritten with `dp[i][j]`. The diagonal term `dp[i+1][j-1]` is the old `dp[j-1]`, so save it in `prev` before it is overwritten.
- Link: the longest palindromic subsequence of `s` is the LCS of `s` and `s[::-1]`. A common subsequence of `s` and its reverse, read in `s`, is also a subsequence that reads the same backwards, and conversely. Verified on every string over {a,b,c} up to length 7.
- One line on insertions/deletions: the minimum number of insertions (or of deletions) that make `s` a palindrome is `n - LPS(s)`: keep the LPS letters, mirror each of the other n - LPS letters. I checked it against an independent recursion and against enumerating the shortest palindrome that has `s` as a subsequence, for every string over {a,b,c} up to length 5 (`'abcd'` needs 3 insertions: `abcdcba`).
- Recursion limit, observed on Python 3.13 at the default of 1000: the memoised top-down version shrinks the range by 1 or 2 per call, so its depth is up to n. At n = 300 and 500 it worked; at n = 2000 it raised `RecursionError` on a cycling-alphabet string and on random letters. For `'a' * 1000` the depth is about n/2 and it still passed, which shows the depth depends on the string. The bottom-up version has no recursion.

**Complexity:** Time O(n^2) (n(n+1)/2 cells, 2 million at n = 2000). Space O(n) for one row, O(n^2) for the full table (4 million Python ints in lists at n = 2000, which is memory-heavy: roughly 32 MB of pointers alone). With the LCS route you need two rows of length n+1 and the same O(n^2) time.

**Dry run:** `s = 'bbbab'`; cells below the diagonal are empty.

| i\j | 0 b | 1 b | 2 b | 3 a | 4 b |
|---|---|---|---|---|---|
| 0 b | 1 | 2 | 3 | 3 | 4 |
| 1 b | . | 1 | 2 | 2 | 3 |
| 2 b | . | . | 1 | 1 | 3 |
| 3 a | . | . | . | 1 | 1 |
| 4 b | . | . | . | . | 1 |

Cell (2, 4): ends `b` and `b` match: 2 + dp[3][3] = 3 (`bab`). Cell (0, 4): ends match: 2 + dp[1][3] = 2 + 2 = 4 (`bbbb`). Cell (0, 3): `b` vs `a` differ: max(dp[1][3], dp[0][2]) = max(2, 3) = 3.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1107)

def lps_table(s):
    """dp[i][j] = LPS length inside s[i..j]. Fill i from n-1 down to 0, j from i+1 up to n-1:
    dp[i][j] needs dp[i+1][j-1], dp[i+1][j] (row below) and dp[i][j-1] (same row, left)."""
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp

def lps_one_row(s):
    """dp[j] holds dp[i+1][j] until overwritten with dp[i][j]; prev saves old dp[j-1] = dp[i+1][j-1]."""
    n = len(s)
    dp = [0] * n
    for i in range(n - 1, -1, -1):
        dp[i] = 1
        prev = 0                                   # dp[i+1][i] = empty range = 0
        for j in range(i + 1, n):
            keep = dp[j]                           # dp[i+1][j]
            dp[j] = prev + 2 if s[i] == s[j] else max(dp[j], dp[j - 1])
            prev = keep
    return dp[n - 1]

def lcs_len(a, b):
    if len(b) > len(a):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def lps_via_lcs(s):
    return lcs_len(s, s[::-1])

def lps_all_subsequences(s):
    """Oracle: every subsequence (bitmask), keep palindromes."""
    n, best = len(s), 0
    for mask in range(1 << n):
        t = [s[i] for i in range(n) if mask >> i & 1]
        if t == t[::-1]:
            best = max(best, len(t))
    return best

def lps_memo(s):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return 2 + f(i + 1, j - 1)
        return max(f(i + 1, j), f(i, j - 1))
    return f(0, len(s) - 1)

def min_insertions(s):
    return len(s) - lps_one_row(s)

def min_insertions_recursive(s):
    """Independent recursion for 'min insertions to make a palindrome'."""
    def f(i, j):
        if i >= j:
            return 0
        if s[i] == s[j]:
            return f(i + 1, j - 1)
        return 1 + min(f(i + 1, j), f(i, j - 1))
    return f(0, len(s) - 1)

def min_insertions_brute(s):
    """Shortest palindrome (over the alphabet of s) that has s as a subsequence, by enumeration."""
    def is_subseq(t, u):
        it = iter(u)
        return all(c in it for c in t)
    alpha = sorted(set(s))
    for L in range(len(s), 2 * len(s) + 1):
        half = (L + 1) // 2
        for h in itertools.product(alpha, repeat=half):
            pal = ''.join(h) + ''.join(h[:L // 2][::-1])
            if is_subseq(s, pal):
                return L - len(s)

for s, want in [('bbbab', 4), ('cbbd', 2), ('a', 1), ('abcd', 1), ('agbdba', 5)]:
    assert lps_table(s)[0][-1] == lps_one_row(s) == lps_via_lcs(s) == lps_all_subsequences(s) == lps_memo(s) == want, s
print("5 prompt examples ok")

s = 'bbbab'
print("walk-through s =", s, "(dp[i][j] for i <= j, '.' below the diagonal)")
t = lps_table(s)
print("        " + "  ".join(s))
for i in range(len(s)):
    print("   ", s[i], "  ", "  ".join(str(t[i][j]) if j >= i else '.' for j in range(len(s))))
print("  answer dp[0][4] =", t[0][-1])

cnt = 0
for n in range(1, 8):
    for tup in itertools.product('abc', repeat=n):
        s = ''.join(tup)
        o = lps_all_subsequences(s)
        assert lps_table(s)[0][-1] == lps_one_row(s) == lps_via_lcs(s) == o, s
        cnt += 1
print("exhaustive over {a,b,c}, len 1..7:", cnt, "strings: interval table == one row == LCS(s, reverse) == all subsequences")
for _ in range(400):
    s = ''.join(random.choice('abcde') for _ in range(random.randint(1, 12)))
    assert lps_one_row(s) == lps_all_subsequences(s) == lps_via_lcs(s) == lps_memo(s) == lps_table(s)[0][-1]
print("400 seeded random strings (len <= 12, alphabet abcde): ok")

# insertions / deletions claim: n - LPS
for n in range(1, 6):
    for tup in itertools.product('abc', repeat=n):
        s = ''.join(tup)
        assert min_insertions(s) == min_insertions_recursive(s) == min_insertions_brute(s), s
print("min insertions = n - LPS verified against recursion and shortest-palindromic-supersequence enumeration, all strings over {a,b,c}, len 1..5")
print("   e.g. 'abcd' needs", min_insertions('abcd'), "insertions (abcdcba), 'agbdba' needs", min_insertions('agbdba'))

# size 2000
rnd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(2000))
v = lps_one_row(rnd)
assert v == lps_via_lcs(rnd) == lps_table(rnd)[0][-1]
print("n = 2000 random letters: LPS =", v, "(one row == LCS with reverse == full table)")
print("n = 2000 'a' * 2000:", lps_one_row('a' * 2000))
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x):
    try:
        return "ok" if lps_memo(x) == lps_one_row(x) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion on 'abcd...' cycling strings (depth grows with n):")
for n in (300, 500, 2000):
    x = ''.join(chr(97 + i % 26) for i in range(n))
    print("   n = %4d: %s" % (n, memo_outcome(x)))
print("memoised recursion, n = 2000 random letters:", memo_outcome(rnd))
print("memoised recursion, 'a' * 1000 (ends always equal, depth about n/2):", memo_outcome('a' * 1000))
```

**Output (my run):**
```
5 prompt examples ok
walk-through s = bbbab (dp[i][j] for i <= j, '.' below the diagonal)
        b  b  b  a  b
    b    1  2  3  3  4
    b    .  1  2  2  3
    b    .  .  1  1  3
    a    .  .  .  1  1
    b    .  .  .  .  1
  answer dp[0][4] = 4
exhaustive over {a,b,c}, len 1..7: 3279 strings: interval table == one row == LCS(s, reverse) == all subsequences
400 seeded random strings (len <= 12, alphabet abcde): ok
min insertions = n - LPS verified against recursion and shortest-palindromic-supersequence enumeration, all strings over {a,b,c}, len 1..5
   e.g. 'abcd' needs 3 insertions (abcdcba), 'agbdba' needs 1
n = 2000 random letters: LPS = 643 (one row == LCS with reverse == full table)
n = 2000 'a' * 2000: 2000
recursion limit: 1000
memoised recursion on 'abcd...' cycling strings (depth grows with n):
   n =  300: ok
   n =  500: ok
   n = 2000: RecursionError
memoised recursion, n = 2000 random letters: RecursionError
memoised recursion, 'a' * 1000 (ends always equal, depth about n/2): ok
```

**Edge cases:**
- Single letter: 1. All different letters: 1 (`'abcd'`). Already a palindrome: n.
- Length 2 equal ends: `dp[i+1][j-1]` is an empty range, treat it as 0 (the guard in the code).
- n = 2000: 2 million cell updates in bottom-up, fine; memo recursion fails.
- Subsequence vs substring: the contiguous version is Part 3 Q8.

**Follow-ups:**
- Print the palindrome? Walk from (0, n-1): equal ends both go in, else follow the larger neighbour; tie rule as in Q10.
- Minimum deletions to make a palindrome: `n - LPS`.
- Count palindromic subsequences? Different recurrence (inclusion-exclusion on equal ends).

**Common mistakes:**
- Filling i ascending (needs `dp[i+1][...]` before it exists).
- Missing the empty-range case for j = i + 1.
- Using `dp[i+1][j-1] + 2` when the ends differ.
- In the one-row version, overwriting the diagonal value before saving it.

---

### Q8 ⭐⭐⭐ 🟡 Edit distance (Levenshtein). `a` and `b` are lowercase strings with 0 <= len <= 1000 each. One edit is inserting a character, deleting a character or replacing a character; return the minimum number of edits that turn `a` into `b`. Define `dp[i][j]` on prefixes, give the three transitions and the base row and column, then use two rows. The concept-level treatment is Part 3 Q35 and the single-edit test is Part 3 Q34; do not repeat them. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (len <= 7) on small inputs. Example: a='horse', b='ros' -> 3; a='intention', b='execution' -> 5; a='', b='abc' -> 3; a='same', b='same' -> 0; a='a', b='b' -> 1.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-sequence DP on prefixes with three moves (the LCS table with a cost per edit).

**Say this first (1 line):** "dp[i][j] is the fewest edits to turn the first i letters of a into the first j of b; equal last letters cost nothing (dp[i-1][j-1]), otherwise 1 + the best of replace, delete, insert; the first row and column are i and j. O(m*n) time, two rows of space, bottom-up."

**Brute force:** Recursion on suffixes: equal heads advance both; different heads try delete (advance i), insert (advance j) and replace (advance both), each at cost 1; when one string runs out, the rest of the other costs its length. Without a memo it is exponential (three branches per mismatch).

**Optimal:**
- State: `dp[i][j]` = minimum edits to turn `a[:i]` into `b[:j]`.
- Base: `dp[i][0] = i` (delete all i letters), `dp[0][j] = j` (insert j letters).
- Transition, equal last letters: `dp[i][j] = dp[i-1][j-1]`. Taking the match is never worse than another move: neighbouring cells differ by at most 1, so `dp[i-1][j-1] <= 1 + dp[i-1][j]` and `<= 1 + dp[i][j-1]`.
- Transition, different: `dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])`. Diagonal is replace `a[i-1]` by `b[j-1]`; up is delete `a[i-1]`; left is insert `b[j-1]` after the prefix.
- Answer: `dp[m][n]`.
- Two rows: the three inputs come from the previous row (diagonal, up) and the current row (left). Index the columns by the shorter string; edit distance is symmetric (insert and delete swap roles), so swapping the arguments is safe, and the code asserts it.
- The concept-level treatment is Part 3 Q35 and the single-edit test is Part 3 Q34; this answer is the tabulated, space-optimised version.
- Recursion limit, observed on Python 3.13 at the default of 1000: the memoised top-down version has depth up to m + n. On two disjoint strings it passed at n = 100, 300, 400 each and raised `RecursionError` at n = 1000; random 1000-letter strings also raised. Bottom-up handles 1000 x 1000.
- Sanity bounds checked on 500 random pairs: `|len(a) - len(b)| <= distance <= max(len(a), len(b))`.

**Complexity:** Time O(m*n) (1,000,000 updates at the maximum). Space O(min(m, n)) with two rows. The recursion without a memo is exponential.

**Dry run:** `a = 'horse'`, `b = 'ros'`.

| a-prefix \ b-prefix | '' | r | ro | ros |
|---|---|---|---|---|
| '' | 0 | 1 | 2 | 3 |
| h | 1 | 1 | 2 | 3 |
| ho | 2 | 2 | 1 | 2 |
| hor | 3 | 2 | 2 | 2 |
| hors | 4 | 3 | 3 | 2 |
| horse | 5 | 4 | 4 | 3 |

Cell (h, r): different, 1 + min(diag 0, up 1, left 1) = 1 (replace h by r). Cell (ho, ro): `o == o`, so it copies the diagonal dp[h][r] = 1. Cell (horse, ros): `e` vs `s` differ: diagonal dp[hors][ro] = 3, up dp[hors][ros] = 2, left dp[horse][ro] = 4, so 1 + min(3, 2, 4) = 3. Answer 3: horse -> rorse (replace h) -> rose (delete r) -> ros (delete e).

**Code:**
```python
import itertools
import random
import sys
from collections import deque
from functools import lru_cache

random.seed(1108)

def edit_table(a, b):
    """dp[i][j] = min edits to turn a[:i] into b[:j]."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                              # delete i letters
    for j in range(n + 1):
        dp[0][j] = j                              # insert j letters
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],   # replace
                                   dp[i - 1][j],       # delete a[i-1]
                                   dp[i][j - 1])       # insert b[j-1]
    return dp

def edit_two_rows(a, b):
    """Two rows over the shorter string (edit distance is symmetric, so swapping is safe)."""
    if len(b) > len(a):
        a, b = b, a
    prev = list(range(len(b) + 1))                # row i = 0
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = prev[j - 1] if ca == cb else 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def edit_plain(a, b):
    """Oracle: plain recursion on suffixes, no memo."""
    def f(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))
    return f(0, 0)

def edit_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))
    return f(0, 0)

def edit_bfs(a, b, alpha='ab'):
    """Independent oracle: breadth-first search over strings, one edit per step. Tiny inputs only."""
    seen = {a}
    q = deque([(a, 0)])
    while q:
        s, d = q.popleft()
        if s == b:
            return d
        nxt = set()
        for i in range(len(s) + 1):
            for c in alpha:
                nxt.add(s[:i] + c + s[i:])                    # insert
        for i in range(len(s)):
            nxt.add(s[:i] + s[i + 1:])                        # delete
            for c in alpha:
                nxt.add(s[:i] + c + s[i + 1:])                # replace
        for t in nxt:
            if t not in seen and len(t) <= len(a) + len(b):
                seen.add(t)
                q.append((t, d + 1))

for (a, b), want in [(('horse', 'ros'), 3), (('intention', 'execution'), 5), (('', 'abc'), 3), (('same', 'same'), 0), (('a', 'b'), 1)]:
    assert edit_two_rows(a, b) == edit_table(a, b)[-1][-1] == edit_plain(a, b) == edit_memo(a, b) == want, (a, b)
print("5 prompt examples ok")

a, b = 'horse', 'ros'
print("walk-through a =", a, " b =", b, "(rows = prefixes of a, columns = prefixes of b)")
print("        ", ["''"] + list(b))
for i, r in enumerate(edit_table(a, b)):
    print("  ", ("'" + a[:i] + "'").ljust(8), r)

cnt = 0
for la in range(6):
    for lb in range(6):
        for x in itertools.product('ab', repeat=la):
            for y in itertools.product('ab', repeat=lb):
                x_, y_ = ''.join(x), ''.join(y)
                d = edit_two_rows(x_, y_)
                assert d == edit_plain(x_, y_) == edit_table(x_, y_)[-1][-1] == edit_two_rows(y_, x_), (x_, y_)
                cnt += 1
print("exhaustive over {a,b}, lengths 0..5:", cnt, "pairs: two rows == table == plain recursion; symmetric")
cnt = 0
for la in range(4):
    for lb in range(4):
        for x in itertools.product('ab', repeat=la):
            for y in itertools.product('ab', repeat=lb):
                x_, y_ = ''.join(x), ''.join(y)
                assert edit_bfs(x_, y_) == edit_two_rows(x_, y_), (x_, y_)
                cnt += 1
print("independent BFS over strings (insert/delete/replace one letter per step), lengths 0..3 over {a,b}:", cnt, "pairs agree")
for _ in range(500):
    x = ''.join(random.choice('abcd') for _ in range(random.randint(0, 7)))
    y = ''.join(random.choice('abcd') for _ in range(random.randint(0, 7)))
    assert edit_two_rows(x, y) == edit_plain(x, y) == edit_table(x, y)[-1][-1] == edit_memo(x, y)
    assert abs(len(x) - len(y)) <= edit_two_rows(x, y) <= max(len(x), len(y))   # bounds
print("500 seeded random pairs (len <= 7, alphabet abcd): ok; |len diff| <= dist <= max len holds")

A = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(1000))
B = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(1000))
v = edit_two_rows(A, B)
assert v == edit_table(A, B)[-1][-1]
print("1000 x 1000 random letters: distance =", v, "(two rows == full table)")
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x, y):
    try:
        return "ok" if edit_memo(x, y) == edit_two_rows(x, y) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion on disjoint strings (a's vs b's, depth about 2n):")
for n in (100, 300, 400, 1000):
    print("   n = %4d each: %s" % (n, memo_outcome('a' * n, 'b' * n)))
print("memoised recursion, 1000 x 1000 random letters:", memo_outcome(A, B))
```

**Output (my run):**
```
5 prompt examples ok
walk-through a = horse  b = ros (rows = prefixes of a, columns = prefixes of b)
         ["''", 'r', 'o', 's']
   ''       [0, 1, 2, 3]
   'h'      [1, 1, 2, 3]
   'ho'     [2, 2, 1, 2]
   'hor'    [3, 2, 2, 2]
   'hors'   [4, 3, 3, 2]
   'horse'  [5, 4, 4, 3]
exhaustive over {a,b}, lengths 0..5: 3969 pairs: two rows == table == plain recursion; symmetric
independent BFS over strings (insert/delete/replace one letter per step), lengths 0..3 over {a,b}: 225 pairs agree
500 seeded random pairs (len <= 7, alphabet abcd): ok; |len diff| <= dist <= max len holds
1000 x 1000 random letters: distance = 882 (two rows == full table)
recursion limit: 1000
memoised recursion on disjoint strings (a's vs b's, depth about 2n):
   n =  100 each: ok
   n =  300 each: ok
   n =  400 each: ok
   n = 1000 each: RecursionError
memoised recursion, 1000 x 1000 random letters: RecursionError
```

**Edge cases:**
- One string empty: the length of the other (`'' -> 'abc'` = 3).
- Equal strings: 0. One letter each: 0 or 1.
- Fully disjoint strings of equal length n: n (all replacements).
- Do not confuse with LCS-based "delete and insert only" distance, which is `m + n - 2 * LCS` and has no replace.

**Follow-ups:**
- Print the edits? Keep the table and walk, with a tie rule (Q15).
- Cost-weighted edits? Replace the 1s by per-operation costs; the base row and column become cumulative costs.
- Edit distance at most k only? Limit to a band of width 2k+1 around the diagonal: O(k*n).
- Many words against one query? Different tools (trie plus DP rows).

**Common mistakes:**
- Wrong base row and column (initialising to 0).
- Using `1 + dp[i-1][j-1]` on equal letters.
- Forgetting that `cur[0] = i` for each new row in the two-row version.
- Memoised recursion at 1000 x 1000.

---

### Q9 ⭐⭐⭐ 🔴 Regular expression matching. `s` is a lowercase string (0 <= len <= 1000) and `p` a pattern (0 <= len <= 1000) over lowercase letters, '.' (matches any single character) and '*' (matches zero or more copies of the character or '.' just before it). A '*' never starts the pattern and never follows another '*'. Return True only if `p` matches the WHOLE string `s`. Define `dp[i][j]` on suffixes or prefixes, give the transitions for a plain character, '.', and a starred item (zero copies versus one more copy), and state the complexity. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). Wildcard matching with '?' and '*' is a different grammar (Part 3 Q38 and Q17 of this part). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against re.fullmatch from the standard library on small inputs. Example: s='aa', p='a' -> False; s='aa', p='a*' -> True; s='ab', p='.*' -> True; s='aab', p='c*a*b' -> True; s='mississippi', p='mis*is*p*.' -> False; s='', p='a*b*' -> True.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-sequence DP where one pattern item can consume 0, 1 or many letters (a "star" state with two exits).

**Say this first (1 line):** "f[i][j] is True when s[i:] matches p[j:]; a plain item or '.' needs the heads to match and then f[i+1][j+1]; an item followed by '*' is either zero copies (f[i][j+2]) or one more copy when the heads match (f[i+1][j]). Fill i and j from the end. O(m*n) time, bottom-up because of recursion depth."

**Brute force:** Backtracking recursion with the same case split and no memo. For patterns such as `a*a*a*a*b` against `aaaa...a` it retries the same (i, j) pairs and is exponential. The standard-library `re` engine is also a backtracking engine, which is fine as a test oracle on small inputs.

**Optimal:**
- State: `f[i][j]` = True if `s[i:]` is matched completely by `p[j:]` (suffix form). A mirrored prefix form also works; the code includes both and they agree.
- Base: `f[m][n] = True` (both exhausted). `f[m][j]` for j < n is computed by the same rule, with `first = False`: it becomes True only when the rest of the pattern is all `x*` items (zero copies each). `f[i][n] = False` for i < m (letters left, no pattern).
- Define `first = i < m and p[j] in (s[i], '.')`: the head of the pattern matches the head of the string.
- Transition, plain item (`p[j+1]` is not `'*'`): `f[i][j] = first and f[i+1][j+1]`.
- Transition, starred item (`p[j+1] == '*'`): `f[i][j] = f[i][j+2] or (first and f[i+1][j])`. Zero copies skips the item and its star (j + 2). One more copy consumes `s[i]` but stays on the same starred item (j unchanged), so any number of copies is covered.
- A `*` never starts the pattern and never follows another `*` (from the prompt), so `p[j]` is never `*` when we read it as an item, and `j + 2` stays in range because the star sits at j + 1 <= n - 1.
- Answer: `f[0][0]`.
- Space: row i needs row i+1 and itself at j+2, so two rows of length n + 1 suffice.
- Wildcard matching with `?` and `*` is a different grammar (there `*` stands alone and matches any run): Part 3 Q38 for the two-pointer boolean version and Q17 of this part for the counting table.
- Recursion limit, observed on Python 3.13 at the default of 1000: a memoised top-down version nests deeper as the strings grow (about n frames in the case below). For `'a' * n` against `'a*' * (n/2)` it passed at n = 100, 300 and 400 and raised `RecursionError` at n = 1000. The bottom-up version has no recursion.

**Complexity:** Time O(m*n), space O(n) with two rows (O(m*n) for the table). Each cell does O(1) work. Backtracking without a memo can be exponential.

**Dry run, first example:** `s = 'aa'`, `p = 'a'`. Columns are j = 0 (`a`) and the end `$`.

| s[i:] \ p[j:] | `a` | `$` |
|---|---|---|
| `aa` | F | F |
| `a` | T | F |
| `` (empty) | F | T |

`f[2][1] = True` (both empty). `f[1][0]`: heads match, `f[2][1]` is True, so True. `f[0][0]`: heads match but `f[1][1]` is False (a letter left, pattern used up), so False. Answer False.

**A starred example:** `s = 'aab'`, `p = 'c*a*b'` (the star columns are meaningless alone, they show F).

| s[i:] \ p[j:] | c | * | a | * | b | $ |
|---|---|---|---|---|---|---|
| `aab` | T | F | T | F | F | F |
| `ab` | T | F | T | F | F | F |
| `b` | T | F | T | F | T | F |
| `` | F | F | F | F | F | T |

`f[3][4]` row `` col `b`: no letters, plain item `b`: False. `f[3][2]` (empty vs `a*b`): zero copies leads to `f[3][4]` = F, so F. `f[2][4]` (`b` vs `b`) = first and `f[3][5]` = T. `f[2][2]` (`b` vs `a*b`): zero copies -> `f[2][4]` = T. `f[0][0]` (`aab` vs `c*a*b`): zero copies of `c` -> `f[0][2]` (`aab` vs `a*b`) = True (take one `a`, one `a`, then `b`). Answer True.

**Code:**
```python
import itertools
import random
import re
import sys
from functools import lru_cache

random.seed(1109)

def match_table(s, p):
    """f[i][j] = True iff s[i:] matches p[j:] completely. Suffix form: fill i from m down, j from n down."""
    m, n = len(s), len(p)
    f = [[False] * (n + 1) for _ in range(m + 1)]
    f[m][n] = True                                    # empty vs empty
    for i in range(m, -1, -1):
        for j in range(n - 1, -1, -1):
            first = i < m and p[j] in (s[i], '.')     # does the head of p match the head of s?
            if j + 1 < n and p[j + 1] == '*':
                f[i][j] = f[i][j + 2] or (first and f[i + 1][j])   # zero copies, or one more copy
            else:
                f[i][j] = first and f[i + 1][j + 1]
    return f

def match_two_rows(s, p):
    """Row i needs row i+1 and itself at j+2: keep two rows."""
    m, n = len(s), len(p)
    nxt = [False] * (n + 1)                           # row m
    for i in range(m, -1, -1):
        cur = [False] * (n + 1)
        if i == m:
            cur[n] = True
        for j in range(n - 1, -1, -1):
            first = i < m and p[j] in (s[i], '.')
            if j + 1 < n and p[j + 1] == '*':
                cur[j] = cur[j + 2] or (first and nxt[j])
            else:
                cur[j] = first and nxt[j + 1]
        nxt = cur
    return nxt[0]

def match_prefix(s, p):
    """Prefix form: g[i][j] = s[:i] matches p[:j]. A '*' at p[j-1] works with the item p[j-2]."""
    m, n = len(s), len(p)
    g = [[False] * (n + 1) for _ in range(m + 1)]
    g[0][0] = True
    for i in range(m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                g[i][j] = g[i][j - 2] or (i > 0 and p[j - 2] in (s[i - 1], '.') and g[i - 1][j])
            else:
                g[i][j] = i > 0 and p[j - 1] in (s[i - 1], '.') and g[i - 1][j - 1]
    return g[m][n]

def match_stdlib(s, p):
    return re.fullmatch(p, s) is not None

def match_memo(s, p):
    m, n = len(s), len(p)
    @lru_cache(maxsize=None)
    def f(i, j):
        if j == n:
            return i == m
        first = i < m and p[j] in (s[i], '.')
        if j + 1 < n and p[j + 1] == '*':
            return f(i, j + 2) or (first and f(i + 1, j))
        return first and f(i + 1, j + 1)
    return f(0, 0)

for (s, p), want in [(('aa', 'a'), False), (('aa', 'a*'), True), (('ab', '.*'), True), (('aab', 'c*a*b'), True),
                     (('mississippi', 'mis*is*p*.'), False), (('', 'a*b*'), True)]:
    assert match_table(s, p)[0][0] == match_two_rows(s, p) == match_prefix(s, p) == match_stdlib(s, p) == match_memo(s, p) == want, (s, p)
print("6 prompt examples ok")

def show(s, p):
    f = match_table(s, p)
    print("walk-through s =", repr(s), " p =", repr(p), "(f[i][j]: s[i:] matches p[j:]; T/F)")
    print("          " + "  ".join(list(p) + ["$"]))
    for i in range(len(s) + 1):
        print("   ", (repr(s[i:]) if i < len(s) else "''").ljust(6), "  ".join("T" if v else "F" for v in f[i]))
    print("  answer f[0][0] =", f[0][0])
show('aa', 'a')
show('aab', 'c*a*b')

# valid patterns: items (letter or '.') each optionally followed by one '*'
def patterns(max_items, alpha='ab.'):
    yield ''
    for k in range(1, max_items + 1):
        for items in itertools.product(alpha, repeat=k):
            for stars in itertools.product((0, 1), repeat=k):
                yield ''.join(c + ('*' if st else '') for c, st in zip(items, stars))
pats = list(patterns(4))
strs = [''.join(t) for k in range(6) for t in itertools.product('ab', repeat=k)]
cnt = 0
for p in pats:
    for s in strs:
        want = match_stdlib(s, p)
        assert match_table(s, p)[0][0] == match_two_rows(s, p) == match_prefix(s, p) == want, (s, p)
        cnt += 1
print("exhaustive vs re.fullmatch:", len(pats), "patterns (up to 4 items over a, b, '.', each with optional '*') x", len(strs), "strings (len <= 5 over {a,b}) =", cnt, "pairs ok")
trues = sum(match_stdlib(s, p) for p in pats for s in strs)
print("   of which", trues, "are matches, so both outcomes are well covered")
for _ in range(1000):
    k = random.randint(0, 6)
    p = ''.join(random.choice('abc.') + random.choice(['', '*']) for _ in range(k))
    s = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert match_table(s, p)[0][0] == match_stdlib(s, p) == match_memo(s, p) == match_two_rows(s, p), (s, p)
print("1000 seeded random (s, p) with s <= 8 and up to 6 pattern items: ok")

# size 1000
S = 'a' * 1000
P = 'a*' * 500
print("1000 x 1000: 'a'*1000 vs 'a*'*500 ->", match_two_rows(S, P), "; vs 'a*'*499 + 'b' ->", match_two_rows(S, 'a*' * 499 + 'b'))
R = ''.join(random.choice('ab') for _ in range(1000))
Q = ''.join(random.choice('ab.') + random.choice(['', '*']) for _ in range(333))[:1000]
assert match_table(R, Q)[0][0] == match_two_rows(R, Q) == match_prefix(R, Q)
print("random 1000-letter s vs random pattern of", len(Q), "chars: table == two rows == prefix form ->", match_two_rows(R, Q))
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x, y):
    try:
        return "ok" if match_memo(x, y) == match_two_rows(x, y) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion on 'a' * n vs 'a*' * (n/2):")
for n in (100, 300, 400, 1000):
    print("   n = %4d: %s" % (n, memo_outcome('a' * n, 'a*' * (n // 2))))
```

**Output (my run):**
```
6 prompt examples ok
walk-through s = 'aa'  p = 'a' (f[i][j]: s[i:] matches p[j:]; T/F)
          a  $
    'aa'   F  F
    'a'    T  F
    ''     F  T
  answer f[0][0] = False
walk-through s = 'aab'  p = 'c*a*b' (f[i][j]: s[i:] matches p[j:]; T/F)
          c  *  a  *  b  $
    'aab'  T  F  T  F  F  F
    'ab'   T  F  T  F  F  F
    'b'    T  F  T  F  T  F
    ''     F  F  F  F  F  T
  answer f[0][0] = True
exhaustive vs re.fullmatch: 1555 patterns (up to 4 items over a, b, '.', each with optional '*') x 63 strings (len <= 5 over {a,b}) = 97965 pairs ok
   of which 37945 are matches, so both outcomes are well covered
1000 seeded random (s, p) with s <= 8 and up to 6 pattern items: ok
1000 x 1000: 'a'*1000 vs 'a*'*500 -> True ; vs 'a*'*499 + 'b' -> False
random 1000-letter s vs random pattern of 511 chars: table == two rows == prefix form -> False
recursion limit: 1000
memoised recursion on 'a' * n vs 'a*' * (n/2):
   n =  100: ok
   n =  300: ok
   n =  400: ok
   n = 1000: RecursionError
```

**Edge cases:**
- `s = ''` with `p = 'a*b*'` is True (every item takes zero copies); `s = ''` with `p = 'a'` is False.
- `.*` matches everything, including the empty string.
- Match must cover the WHOLE string: `s = 'aa'`, `p = 'a'` is False (not a prefix match). In the standard library use `re.fullmatch`, not `re.match`.
- `p = ''`: True only when `s = ''`.
- The 1000 x 1000 adversarial case `'a'*1000` vs `'a*'*499 + 'b'` is False and the DP answers it instantly.

**Follow-ups:**
- Why not just use `re`? You can in real code (`re.fullmatch`), but the interviewer wants the DP; the stdlib is also your test oracle here.
- Count the ways to match? See the counting table for the wildcard grammar in Q17.
- Linear space and early exit? Two rows (shown). Early exit if a whole row is False.
- NFA simulation is another O(m*n) route.

**Common mistakes:**
- Treating `x*` as "x repeated at least once".
- On a star, only looking at `f[i+1][j]` and forgetting the zero-copy branch `f[i][j+2]`.
- Prefix-matching instead of whole-string matching.
- Indexing `p[j+1]` without checking `j + 1 < n`.
- Memoised recursion on 1000-letter inputs: `RecursionError`.

---
