# Book 5 — Part 11: Dynamic Programming II (2D Grids, Two-String DPs, Intervals and Bitmasks)

**Topic:** Python DSA for product-company interviews: two-dimensional DP states and how to derive the transition, grid DP (unique paths with and without obstacles, minimum path sum with the path recovered under an explicit tie rule, triangle, minimum falling path, counting minimum-cost paths, paths whose sum is divisible by k with a modulus, maximal square, the dungeon game solved backwards, cherry pickup as a two-walker DP), two-sequence string DPs (longest common subsequence as a length and as the lexicographically smallest string, longest common substring, edit distance as a value and as an edit script, shortest common supersequence, minimum ASCII delete sum, interleaving string, distinct subsequences as a counting DP, longest repeating subsequence, regular expression matching, wildcard matching as a counting table), palindromic DPs (longest palindromic subsequence, counting palindromic substrings with a table, palindrome partitioning with minimum cuts), interval DP (burst balloons, matrix chain multiplication with its parenthesisation, minimum cost to cut a stick, minimum score triangulation, strange printer), a DAG DP over a matrix (longest increasing path), bitmask DP at a basic level (assigning tasks, travelling salesman with a small number of cities), space optimisation to one or two rows, reconstruction of solutions with explicit tie rules, counting versus optimising DPs, modulo arithmetic, and Python specifics (memoised recursion on an n x m state grid versus bottom-up, `functools.lru_cache` with tuple keys, cache size and recursion depth)

**Target:** 35  |  **Actual:** 35 (⭐⭐⭐ 9, ⭐⭐ 15, ⭐ 11)  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns two-dimensional DP: grids, two-string tables, interval DP and basic bitmask DP. Part 3 owns the string patterns around it (expand-around-center and the longest palindromic substring are 'Part 3 Q9' and 'Part 3 Q8', the single-edit test is 'Part 3 Q34', edit distance and LCS at concept level with a memoised recursion are 'Part 3 Q35', and the two-pointer boolean wildcard matcher is 'Part 3 Q38'; here the same ideas appear as full tabulated DPs, with space optimisation and reconstruction, and the wildcard question Q17 adds a counting table instead of repeating the boolean matcher; the palindromic-substring question Q12 reuses the Part 3 Q9 problem only to build the interval table and a one-row version), Part 5 owns binary search, Part 9 owns graphs (shortest paths on a DAG as a DP are 'Part 9 Q40'; Q24, the longest increasing path in a matrix, is the matrix version solved bottom-up and does not repeat the graph material), Part 10 owns DP I (the at-most-k stock table is 'Part 10 Q29', the `[[0]*n]*m` aliasing trap is 'Part 10 Q31' and 'ones and zeroes', the two-capacity knapsack, is 'Part 10 Q39'; none of them is duplicated here, Q1 and Q6 only point to Q31 and Q29, and Q39 is named only to mark the edge of this part), Part 12 owns backtracking (enumerating the paths, cuts or orderings instead of counting or optimising them: every question here returns a count, a length, an optimum or one optimal object under a tie rule), and Part 13 owns math. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each Part N Qn reference was checked against its heading by build.py, and every within-part reference (Q17 in Q9) was checked by build.py against the final question numbers. Conventions: every question states its constraints, whether the answer is returned exactly (Python integers do not overflow) or modulo 10^9 + 7 (Q27 and Q28 only), and its return value for degenerate input (an empty string, an empty list, a 1 x 1 grid, an impossible or zero-length case as the prompt says). Every prompt asks the answer to include a table walk-through on the first example and a seeded random cross-check of the solution against a brute-force, plain-recursion or standard-library oracle on small inputs. Recursion: the prompts whose natural top-down recursion nests past 1000 say a bottom-up solution is required, because CPython's default recursion limit is 1000 and the call depth of a memoised recursion on a two-sequence or a grid table grows with the sum of the two sizes (demonstrated by running code, an observation and not a rule: a memoised LCS on two 300-letter strings runs and on two 400-letter strings runs, the same recursion raises RecursionError for two disjoint 520-, 600- and 1000-letter strings; a memoised edit distance, ASCII delete sum at 1000 x 1000, a memoised longest palindromic subsequence on 2000 letters and a memoised regular-expression match of 1000 letters against `a*` repeated 500 times all raise RecursionError; memoised grid recursion with the cache key `(i, j)` on a 600 x 600 grid is 1199 deep and raises RecursionError while 400 x 400 is 799 deep and works; a memoised longest-increasing-path DFS on a 61 x 61 winding corridor of increasing values raises RecursionError), and no prompt relies on raising the limit and no claim is made about the C stack. Questions whose answer would not be unique say exactly what is accepted: every reconstruction question fixes an explicit tie rule (minimum path moves: lexicographically smallest string with 'D' < 'R', Q14; LCS string: lexicographically smallest, Q10; edit script: lexicographically smallest over D < I < M < S, Q15; shortest common supersequence: lexicographically smallest, Q16; matrix-chain parenthesisation: smallest split index, applied recursively, Q23; task assignment: lexicographically smallest list, Q31; longest common substring: smallest i then smallest j, Q11), and each rule was verified against an oracle that enumerates every candidate and applies the same rule. Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P11_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force, plain recursion, `re.fullmatch` (regular expressions), a breadth-first search over printed states (strange printer) or an instrumented `lru_cache` recursion (cache size and depth) on 300 seeded random small inputs per question (fewer for the slowest oracles), for example all subsequences for the palindromic and common-subsequence questions, every path for the grid questions, every pair of paths for cherry pickup, every permutation for assignment, travelling salesman and cut-a-stick, every parenthesisation for matrix chain and every index combination for distinct subsequences. Claims tested by running code: every pair of strings of length up to 4 over {a, b} (961 pairs) agrees with the oracle for the lexicographically smallest LCS, the shortest common supersequence, the edit script (which also turns `a` into `b` and has as many non-match letters as the edit distance), the longest common substring and the ASCII delete sum; every binary-string table up to length 8 gives the longest palindromic subsequence equal to the LCS of the string with its reverse, the one-row interval version and the oracle, and the palindromic-substring count and minimum cuts agree with their oracles; every 2 x 3 grid with values 0..2 and every 3 x 3 grid with values 0..1 (1241 grids) gives the same minimum-path string and minimum-path count as the oracle, and every assignment matrix of 0 and 1 of size 3 x 3 the same assignment; every matrix chain of 4 matrices with dimensions 1..3 agrees with the enumeration; the closed forms C(m + n - 2, m - 1) for unique paths (and for the obstacle-free grid), C(n + k - 1, k - 1) for k stars in the wildcard count, C(50, 25) for distinct subsequences of a^50 equal to a^25 and C(198, 99) for the minimum-cost path count on a zero grid (which exceeds 10^9 + 7, so the modulus matters); a greedy move fails for minimum path sum on 98 of 500 random grids; the maximum-total-sum path needs more health than the optimum on 5 of 500 random dungeon grids (so a forward DP is not enough); a parent-pointer rebuild from a prefix table gives a different minimum path than the suffix tie rule on 244 of 500 and the classic back-pointer LCS walk gives a different string than the lexicographically smallest one on 39 of 500; the order among equal values does not matter for the longest increasing path (300 shuffles); the boolean wildcard result equals a regular-expression translation on 600 random inputs and equals ways > 0; the cache of an `lru_cache` function rejects a list argument with TypeError (unhashable). Both branches of every boolean or sentinel answer occurred in the random tests, and all solutions run at the stated maximum sizes (1000 x 1000 string tables, 2000-letter palindrome tables, 200 x 200 grids, 300 balloons, 200 matrices, 1500 x 1500 grid statistics, 15 tasks, 12 cities) in a fraction of a second to a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part11_sources.md). Searches returned DP pattern guides (techinterview.org 2D and interval and advanced DP posts, a LeetCode Discuss 13-patterns post, codemia, a DP pattern cheat sheet) that group LCS, edit distance, regular-expression and wildcard matching, grid paths, burst balloons, matrix chain and bitmask DP, and candidate-reported Flipkart rounds (a 2020 on-campus report with a longest palindromic substring solved by a 2-D boolean table and a 2024 off-campus SDE-1 report with a 2D DP array-splitting question; self-reported, unverified); nothing was found tying edit distance, LCS or any other item to a named company, so 'Asked at' tags name source types, not verified company reports. Items such as dungeon game, distinct subsequences, minimum cost to cut a stick, strange printer, cherry pickup and minimum score triangulation come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

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

### Q10 ⭐⭐ 🟡 Recover the longest common subsequence itself. `a` and `b` are lowercase strings with 0 <= len <= 1000. Return a longest common subsequence as a string ('' if there is none). Many LCS strings can exist, so the tie rule is fixed: return the lexicographically smallest among all longest common subsequences. Build the table on suffixes (`f[i][j]` = LCS length of a[i:] and b[j:]) and walk forward, at each step taking the smallest letter c that has a next occurrence i' >= i in `a` and j' >= j in `b` with `1 + f[i'+1][j'+1] == f[i][j]`, using the FIRST such occurrences. Explain why the usual back-pointer walk from the bottom-right cell does not give this string by itself. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every common subsequence of strings of length at most 8 and taking the longest, then the smallest on small inputs. Example: a='abcde', b='ace' -> 'ace'; a='abcbdab', b='bdcaba' -> 'bcab'; a='abc', b='def' -> ''; a='zxy', b='xyz' -> 'xy'; a='', b='' -> ''.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-sequence DP on suffixes, then a forward walk with an explicit tie rule. The table gives the LENGTH; the rule picks WHICH string.

**Say this first (1 line):** "f[i][j] is the LCS length of a[i:] and b[j:]; I fill it bottom-up, then walk forward from (0,0), at each step taking the smallest letter c whose first occurrences keep the total optimal, so the string comes out lexicographically smallest."

**Brute force:** Enumerate every subsequence of each string (2^len each), intersect the two sets, take the longest, break ties by the smaller string. Fine for len <= 8 (256 subsets each). Exponential, so it is only the checker.

**Optimal:**
- State: `f[i][j]` = LCS length of the suffixes `a[i:]` and `b[j:]`.
- Transition: if `a[i] == b[j]` then `f[i][j] = 1 + f[i+1][j+1]`; else `max(f[i+1][j], f[i][j+1])`.
- Base cases: `f[len(a)][j] = 0` and `f[i][len(b)] = 0` (an empty suffix has no common letters). That is why the table is `(m+1) x (n+1)` and starts as all zeros.
- Walk forward from `(0, 0)` while `f[i][j] > 0`. Try letters in order a..z. For letter c, let `i'` be the first index `>= i` with `a[i'] == c` and `j'` the first `>= j` with `b[j'] == c`. If both exist and `1 + f[i'+1][j'+1] == f[i][j]`, emit c and jump to `(i'+1, j'+1)`. Stop at the first letter that works.
- Why FIRST occurrences: jumping to the earliest match leaves the largest suffixes, so `f` can only be as large or larger than from a later match. If any occurrence of c works, the first one works. Taking the smallest working letter at every step gives the smallest string, because every longest answer has the same length (the length is fixed, so comparing letter by letter is valid).
- Why the usual back-pointer walk fails: it starts at the bottom-right of a PREFIX table and decides "up or left" on a tie by a fixed direction. That chooses a path, not a letter order. It builds the string from the END, and a good last letter says nothing about the first letters. It returns a correct longest subsequence, just not the smallest one. Measured below: it differs from the smallest on 49 of 500 random pairs, e.g. `abcbdab` / `bdcaba` gives `bcba`, the smallest is `bcab`.
- Space: reconstruction needs the whole table (it needs `f` at arbitrary cells), so O(mn). Two rows give only the length. Hirschberg's divide and conquer recovers one LCS in O(n) space, but the smallest-string rule is easier with the table.
- Recursion: the top-down version `f(i, j)` nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two random 300-letter strings run fine; two disjoint 1000-letter strings (worst case: depth 2000) raise `RecursionError`. The prompt needs 1000 x 1000, so use the loops. Observation, not a rule: depth depends on the strings and the call path.

**Complexity:** Table O(mn) time and space. The walk does at most `min(m, n)` steps, each scanning up to 26 letters with `str.index` (O(len) each), so O(min(m,n) * 26 * (m+n)) worst case, which stays below the table cost for the prompt sizes. Brute force O(2^m + 2^n).

**Dry run:** `a = 'abcde'`, `b = 'ace'`. Rows are `i` (suffix of a), columns `j` (suffix of b).

| | j=0 `ace` | j=1 `ce` | j=2 `e` | j=3 `` |
|---|---|---|---|---|
| i=0 `abcde` | 3 | 2 | 1 | 0 |
| i=1 `bcde` | 2 | 2 | 1 | 0 |
| i=2 `cde` | 2 | 2 | 1 | 0 |
| i=3 `de` | 1 | 1 | 1 | 0 |
| i=4 `e` | 1 | 1 | 1 | 0 |
| i=5 `` | 0 | 0 | 0 | 0 |

Walk: at `(0,0)` f=3. Letters common to both suffixes: a, c, e. Try `a`: first a at i'=0, j'=0, `1 + f[1][1] = 3` equals 3, emit `a`, go to (1,1). Now f=2: common letters c, e. Try `c`: i'=2, j'=1, `1 + f[3][2] = 2`, emit `c`, go to (3,2). f=1: only `e` is common, i'=4, j'=2, `1 + f[5][3] = 1`, emit `e`, go to (5,3). f=0, stop. Result `ace`.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1010)

def suffix_table(a, b):
    """f[i][j] = LCS length of a[i:] and b[j:]; row len(a) and column len(b) stay 0 (empty suffix)."""
    m, n = len(a), len(b)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                f[i][j] = 1 + f[i + 1][j + 1]
            else:
                f[i][j] = max(f[i + 1][j], f[i][j + 1])
    return f

def lcs_smallest(a, b):
    """Lexicographically smallest longest common subsequence, bottom-up, no recursion."""
    f = suffix_table(a, b)
    i = j = 0
    out = []
    while f[i][j]:
        # candidate letters are those present in both remaining suffixes, tried a..z
        for c in sorted(set(a[i:]) & set(b[j:])):
            ii, jj = a.index(c, i), b.index(c, j)        # FIRST occurrences at or after i / j
            if 1 + f[ii + 1][jj + 1] == f[i][j]:
                out.append(c)
                i, j = ii + 1, jj + 1
                break
    return ''.join(out)

def lcs_backpointer(a, b):
    """The classic walk: prefix table, start at the bottom-right cell, go up/left. NOT lexicographically smallest."""
    m, n = len(a), len(b)
    g = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            g[i][j] = g[i-1][j-1] + 1 if a[i-1] == b[j-1] else max(g[i-1][j], g[i][j-1])
    i, j, out = m, n, []
    while i and j:
        if a[i-1] == b[j-1]:
            out.append(a[i-1]); i -= 1; j -= 1
        elif g[i-1][j] >= g[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(out))

def lcs_memo(a, b):
    """Top-down version of the same table (shows the recursion-limit problem)."""
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def subseqs(s):
    return {''.join(s[i] for i in range(len(s)) if mask >> i & 1) for mask in range(1 << len(s))}

def brute(a, b):
    """Every common subsequence (len <= 8), longest first, then smallest."""
    common = subseqs(a) & subseqs(b)
    return min(common, key=lambda t: (-len(t), t))

# 1. prompt examples
for a, b, want in [('abcde', 'ace', 'ace'), ('abcbdab', 'bdcaba', 'bcab'), ('abc', 'def', ''), ('zxy', 'xyz', 'xy'), ('', '', '')]:
    assert lcs_smallest(a, b) == brute(a, b) == want, (a, b)
print('5 prompt examples ok')

# 2. hand-table source: suffix table for a='abcde', b='ace'
f = suffix_table('abcde', 'ace')
print("f for a='abcde' (rows i=0..5), b='ace' (cols j=0..3):")
for i, row in enumerate(f):
    print(' ', ('abcde' + '-')[i], row)

# 3. seeded random cross-check against full enumeration
for _ in range(400):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert lcs_smallest(a, b) == brute(a, b), (a, b)
print('400 seeded random pairs (len 0..8, alphabet abc): smallest-LCS walk == enumeration')

# 4. exhaustive: all pairs up to length 4 over {a,b} (961 pairs)
cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert lcs_smallest(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# 5. the claim: the back-pointer walk is NOT automatically the smallest string (but it is still a longest one)
diff = 0
for _ in range(500):
    a = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    x, y = lcs_backpointer(a, b), lcs_smallest(a, b)
    assert len(x) == len(y)
    diff += x != y
print('back-pointer walk differs from the smallest LCS on', diff, 'of 500 random pairs')
print("example: abcbdab / bdcaba -> back-pointer", lcs_backpointer('abcbdab', 'bdcaba'), "vs smallest", lcs_smallest('abcbdab', 'bdcaba'))

# 6. size and recursion limit (default limit)
print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(1000)); y = ''.join(random.choice('abcd') for _ in range(1000))
r = lcs_smallest(x, y)
assert len(r) == len(lcs_backpointer(x, y))
print('bottom-up 1000 x 1000 random: LCS length', len(r))
print('memoised, two 300-letter random strings ->', lcs_memo(x[:300], y[:300]))
try:
    lcs_memo('a' * 1000, 'b' * 1000)
    print('memoised disjoint 1000 + 1000: ok')
except RecursionError:
    print('memoised disjoint 1000 + 1000: RecursionError')
print('bottom-up disjoint 1000 + 1000 ->', repr(lcs_smallest('a' * 1000, 'b' * 1000)))

# 7. edge cases
assert lcs_smallest('', 'abc') == '' and lcs_smallest('abc', '') == ''
assert lcs_smallest('aaa', 'aa') == 'aa' and lcs_smallest('ba', 'ab') == 'a'
assert lcs_smallest('abc', 'abc') == 'abc'
print('edge asserts ok')
```

**Output (my run):**
```
5 prompt examples ok
f for a='abcde' (rows i=0..5), b='ace' (cols j=0..3):
  a [3, 2, 1, 0]
  b [2, 2, 1, 0]
  c [2, 2, 1, 0]
  d [1, 1, 1, 0]
  e [1, 1, 1, 0]
  - [0, 0, 0, 0]
400 seeded random pairs (len 0..8, alphabet abc): smallest-LCS walk == enumeration
exhaustive pairs over {a,b}, len <= 4: 961 ok
back-pointer walk differs from the smallest LCS on 49 of 500 random pairs
example: abcbdab / bdcaba -> back-pointer bcba vs smallest bcab
recursion limit: 1000
bottom-up 1000 x 1000 random: LCS length 651
memoised, two 300-letter random strings -> 191
memoised disjoint 1000 + 1000: RecursionError
bottom-up disjoint 1000 + 1000 -> ''
edge asserts ok
```

**Edge cases:**
- Both empty returns `''`; one empty returns `''`; no common letter returns `''` (the walk never starts because `f[0][0] == 0`).
- Equal strings return the string itself.
- `a='zxy'`, `b='xyz'` returns `'xy'`, not `'z'`: two letters beat one.
- Repeated letters (`'aaa'` vs `'aa'`) return `'aa'`.

**Follow-ups:**
- Count how many distinct LCS strings exist? Another table with the same suffix idea, but you must avoid counting one string many times (use first occurrences per letter, exactly as the walk does).
- Only the length, in less memory? Two rows (or one row plus a saved diagonal), O(min(m,n)) space.
- One LCS in linear space? Hirschberg: split `a` in half, find the best split point of `b` from forward and backward length rows, recurse.

**Common mistakes:**
- Using the back-pointer walk and assuming the answer is the smallest string.
- Picking the smallest letter that merely appears in both suffixes, without checking `1 + f[i'+1][j'+1] == f[i][j]`.
- Using the LAST occurrence instead of the first.
- Memoised recursion at 1000 x 1000 (`RecursionError` on the default limit) and a `[[0]*n]*m` table (see Part 10 Q31).

### Q11 ⭐⭐ 🟡 Longest common substring (contiguous). `a` and `b` are lowercase strings with 0 <= len <= 2000. Return `[length, i, j]` where `length` is the largest L such that a[i:i+L] == b[j:j+L] for some i, j; if several pairs reach it, return the smallest i and, for that i, the smallest j. If there is no common character return `[0, -1, -1]`. Use `dp[i][j]` = length of the common suffix of a[:i] and b[:j] (reset to 0 on a mismatch, unlike LCS) and say why one row suffices and why the answer is the maximum over all cells, not the last cell. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a brute force over all lengths and start pairs (len <= 8) on small inputs. Example: a='abcdxyz', b='xyzabcd' -> [4, 0, 3]; a='abc', b='def' -> [0, -1, -1]; a='aaa', b='aa' -> [2, 0, 0]; a='xabcx', b='yabcy' -> [3, 1, 1].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP where the state is "common block ENDING here". A mismatch resets to 0, which is the whole difference from LCS.

**Say this first (1 line):** "d[i][j] is the length of the longest common suffix of a[:i] and b[:j]: equal letters give d[i-1][j-1] + 1, a mismatch gives 0; the answer is the maximum over all cells, tracked as I go, and one row is enough."

**Brute force:** For every length L from the largest possible down to 1, for every start i in `a` and j in `b`, compare `a[i:i+L]` with `b[j:j+L]`. The first hit in (L desc, i asc, j asc) order is the answer. About O(min(m,n) * m * n * L) work, so only for len <= 8. It is the checker.

**Optimal:**
- State: `d[i][j]` = length of the longest common suffix of `a[:i]` and `b[:j]` (a block that must end at `a[i-1]` and `b[j-1]`).
- Transition: `a[i-1] == b[j-1]` gives `d[i-1][j-1] + 1`; otherwise `0`. A block cannot skip a letter, so there is no `max(up, left)`.
- Base cases: row 0 and column 0 are 0 (empty prefix).
- Answer: the maximum over ALL cells, not `d[m][n]`. `d[m][n]` is only the common suffix of the two whole strings. On the first example the last cell is 0 but the answer is 4.
- Position: a cell with value L at `(i, j)` means the block starts at `a[i-L]` and `b[j-L]`. Update the best when `L` is larger, or equal with a smaller `(i-L, j-L)`. Because the prompt wants the smallest start i and then the smallest j, compare the pair of starts; do not rely on scan order.
- One row: `d[i][j]` needs only `d[i-1][j-1]`, the diagonal. Keep one list `row` of length n+1 and run j DESCENDING: when you write `row[j]`, `row[j-1]` has not been touched yet this pass, so it still holds `d[i-1][j-1]`. On a mismatch you MUST write `row[j] = 0`; an old value left there would be a fake block.
- Recursion: the problem is naturally a loop; a memoised version has the same n x m state grid, so use the loops at 2000 x 2000.

**Complexity:** Time O(mn) (4M cell updates at 2000 x 2000; sandbox time is a few seconds at most, not a proof). Space O(n) with the row, O(mn) with the full table. Brute force is far worse.

**Dry run:** `a = 'abcdxyz'`, `b = 'xyzabcd'`. Only the non-zero cells are listed; all other cells are 0.

| cell (i, j) | letters | value |
|---|---|---|
| (1, 4) | a = a | 1 |
| (2, 5) | b = b, diagonal was 1 | 2 |
| (3, 6) | c = c | 3 |
| (4, 7) | d = d | 4 |
| (5, 1) | x = x | 1 |
| (6, 2) | y = y, diagonal was 1 | 2 |
| (7, 3) | z = z | 3 |

The maximum is 4 at `(4, 7)`, so the block starts at `i = 4 - 4 = 0` and `j = 7 - 4 = 3`: `[4, 0, 3]` (`'abcd'`). The last cell `(7, 7)` is 0.

**Code:**
```python
import itertools
import random
import time

random.seed(1111)

def table(a, b):
    """Full table: d[i][j] = length of the common SUFFIX of a[:i] and b[:j] (0 on a mismatch)."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                d[i][j] = d[i - 1][j - 1] + 1
    return d

def lcsubstr(a, b):
    """One row. Returns [length, i, j]; ties: smallest i, then smallest j; no common letter -> [0, -1, -1]."""
    n = len(b)
    row = [0] * (n + 1)              # row[j] = d[i-1][j] before the update, d[i][j] after it
    best_len, best_i, best_j = 0, -1, -1
    for i in range(1, len(a) + 1):
        for j in range(n, 0, -1):    # descending: row[j-1] still holds d[i-1][j-1] (the diagonal)
            if a[i - 1] == b[j - 1]:
                row[j] = row[j - 1] + 1
                L = row[j]
                si, sj = i - L, j - L            # start indices of this common block
                if L > best_len or (L == best_len and (si, sj) < (best_i, best_j)):
                    best_len, best_i, best_j = L, si, sj
            else:
                row[j] = 0           # the reset that makes it a SUBSTRING table
    return [best_len, best_i, best_j]

def brute(a, b):
    """All lengths, longest first, all start pairs in order (len <= 8)."""
    for L in range(min(len(a), len(b)), 0, -1):
        for i in range(len(a) - L + 1):
            for j in range(len(b) - L + 1):
                if a[i:i + L] == b[j:j + L]:
                    return [L, i, j]
    return [0, -1, -1]

for a, b, want in [('abcdxyz', 'xyzabcd', [4, 0, 3]), ('abc', 'def', [0, -1, -1]), ('aaa', 'aa', [2, 0, 0]), ('xabcx', 'yabcy', [3, 1, 1])]:
    assert lcsubstr(a, b) == brute(a, b) == want, (a, b)
print('4 prompt examples ok')

d = table('abcdxyz', 'xyzabcd')
print("d for a='abcdxyz' (rows) vs b='xyzabcd' (cols):")
print('       ', '  '.join(c for c in ' ' + 'xyzabcd'))
for i, row in enumerate(d):
    print('  ', ' ' if i == 0 else 'abcdxyz'[i - 1], row)

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert lcsubstr(a, b) == brute(a, b), (a, b)
print('500 seeded random pairs (len 0..8, alphabet abc): one-row DP == brute force')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert lcsubstr(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# why the answer is the MAX over all cells, not the last cell: d[m][n] is only the common suffix length
a, b = 'abcdxyz', 'xyzabcd'
print('last cell d[m][n] =', table(a, b)[-1][-1], 'but the answer is', lcsubstr(a, b)[0])
assert table(a, b)[-1][-1] == 0

# max size 2000 x 2000 (sandbox timing only)
x = ''.join(random.choice('ab') for _ in range(2000)); y = ''.join(random.choice('ab') for _ in range(2000))
t = time.perf_counter(); r = lcsubstr(x, y); dt = time.perf_counter() - t
assert x[r[1]:r[1] + r[0]] == y[r[2]:r[2] + r[0]]
print('2000 x 2000 over {a,b}: length', r[0], 'found; sandbox time under 5 s:', dt < 5)
print('2000 a vs 2000 a ->', lcsubstr('a' * 2000, 'a' * 2000))

assert lcsubstr('', '') == [0, -1, -1] and lcsubstr('a', '') == [0, -1, -1]
assert lcsubstr('abab', 'abab') == [4, 0, 0] and lcsubstr('ab', 'ba') == [1, 0, 1]
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
d for a='abcdxyz' (rows) vs b='xyzabcd' (cols):
           x  y  z  a  b  c  d
     [0, 0, 0, 0, 0, 0, 0, 0]
   a [0, 0, 0, 0, 1, 0, 0, 0]
   b [0, 0, 0, 0, 0, 2, 0, 0]
   c [0, 0, 0, 0, 0, 0, 3, 0]
   d [0, 0, 0, 0, 0, 0, 0, 4]
   x [0, 1, 0, 0, 0, 0, 0, 0]
   y [0, 0, 2, 0, 0, 0, 0, 0]
   z [0, 0, 0, 3, 0, 0, 0, 0]
500 seeded random pairs (len 0..8, alphabet abc): one-row DP == brute force
exhaustive pairs over {a,b}, len <= 4: 961 ok
last cell d[m][n] = 0 but the answer is 4
2000 x 2000 over {a,b}: length 25 found; sandbox time under 5 s: True
2000 a vs 2000 a -> [2000, 0, 0]
edge asserts ok
```

**Edge cases:**
- Nothing in common returns `[0, -1, -1]`; either string empty returns the same.
- `a='aaa'`, `b='aa'` returns `[2, 0, 0]` (smallest i, then smallest j), not `[2, 1, 0]`.
- Identical strings return `[n, 0, 0]`.
- Several blocks of the same length: the smaller start in `a` wins, then the smaller start in `b`.

**Follow-ups:**
- Linear space AND fast for huge strings? A suffix automaton or suffix array solves it in O(m + n) or O(n log n); the DP is the interview baseline.
- Return the substring itself? `a[i:i+length]`.
- Why not LCS code with a tweak? In LCS a mismatch carries `max(up, left)`; a substring must be contiguous, so the mismatch must reset.

**Common mistakes:**
- Returning `d[m][n]` instead of the maximum over all cells.
- Forgetting the reset to 0 on a mismatch (it silently turns the code into something between LCS and nonsense).
- Running j ascending in the one-row version (the diagonal gets overwritten).
- Reporting the END indices instead of the START indices the prompt asks for.

### Q12 ⭐⭐ 🟡 Count palindromic substrings with a DP table. `s` is a lowercase string with 1 <= len <= 1000. Count the substrings (by position) that are palindromes. Part 3 Q9 owns expand-around-center and Part 3 Q8 the longest palindromic substring; here use the interval table `dp[i][j] = s[i] == s[j] and (j - i < 3 or dp[i+1][j-1])`, say in which order i and j must be filled so that `dp[i+1][j-1]` is ready, then shrink it to ONE row and say which direction the inner loop must run. State the time and space of both this and expand-around-center, and when each wins. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every substring and checking it, and expand-around-center on small inputs. Example: s='abc' -> 3; s='aaa' -> 6; s='abba' -> 6; s='a' -> 1; s='abacaba' -> 12.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2020 on-campus Naukri Code360 report with a longest palindromic substring solved by a 2-D boolean DP table, a 2024 off-campus SDE-1 LeetCode Discuss report with a 2D DP array-splitting question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Interval DP on substrings `[i, j]`: a substring is a palindrome if its ends match and the inside is a palindrome.

**Say this first (1 line):** "dp[i][j] is true if s[i..j] is a palindrome: s[i] == s[j] and (the inside is at most one letter, or dp[i+1][j-1]); I fill i from the end and j upward so the inside is ready, count the trues, and one row suffices if j runs downward."

**Brute force:** Take every substring (n(n+1)/2 of them), reverse it, compare. O(n^3) time. It is the checker.

**Optimal:**
- State: `dp[i][j]` = `s[i..j]` is a palindrome (`i <= j`).
- Transition: `dp[i][j] = s[i] == s[j] and (j - i < 3 or dp[i+1][j-1])`. When `j - i < 3` the inside has length 0 or 1 (`j-i = 1` is a pair, `j-i = 2` has one middle letter), which is always a palindrome, so no lookup is needed.
- Base cases: every `dp[i][i]` is true (single letters); the `j - i < 3` branch covers pairs and triples.
- Order: `dp[i][j]` reads `dp[i+1][j-1]`, the row BELOW and one column left. So `i` must go from `n-1` down to 0 (or, equivalently, by increasing length). Within a row `j` can go either way for the full table.
- Count: add 1 for every true cell.
- One row: keep `dp[j]` meaning "`s[i..j]` is a palindrome for the current i". Cell `(i, j)` needs old-row `dp[j-1]`. Run `j` DESCENDING (from `n-1` to `i`): `dp[j-1]` has not yet been overwritten when you compute `dp[j]`. Ascending would read the new row's value and is wrong; the code measures this: wrong on 248 of 300 random strings of length 8.
- Compared with expand-around-center (Part 3 Q9): centres use 2n-1 centres, each expands while the ends match, O(n^2) time worst case (all letters equal), O(n) typical, and O(1) space. The DP is O(n^2) time always, O(n^2) space for the table, O(n) for the row. For this question centres win (less space, usually faster, simpler); the DP wins when you will ask many "is s[i..j] a palindrome?" queries or need the table for another DP (such as minimum palindrome cuts).
- Recursion: `pal(i, j)` recursion peels two letters per call, so its depth is about n/2. As observed on Python 3.13 with the default limit, the memoised version works at n = 1000 (all `a`, depth about 500), well inside 1000. At n = 2100 (all `a`, depth about 1050) it raises `RecursionError` (shown in the code). The prompt stops at 1000, but the safe habit is still the loops; the exact depth is an observation, not a rule.

**Complexity:** DP: time O(n^2), space O(n^2) for the table or O(n) for one row. Centres: time O(n^2) worst case, O(1) space. Brute force O(n^3).

**Dry run:** `s = 'abba'`. T marks a palindrome.

| i \ j | 0 `a` | 1 `b` | 2 `b` | 3 `a` |
|---|---|---|---|---|
| 0 `a` | T | . | . | T |
| 1 `b` | | T | T | . |
| 2 `b` | | | T | . |
| 3 `a` | | | | T |

Fill order i = 3, 2, 1, 0. Row 3: `(3,3)` T. Row 2: `(2,2)` T, `(2,3)` b != a so `.`. Row 1: `(1,1)` T; `(1,2)` b = b and `j-i = 1 < 3`, T; `(1,3)` b != a, `.`. Row 0: `(0,0)` T; `(0,1)` a != b; `(0,2)` a != b; `(0,3)` a = a and `j-i = 3` is not below 3, so it needs `dp[1][2]`, which is T, so T. Total 4 singles + `bb` + `abba` = 6.

**Code:**
```python
import random
import sys
from functools import lru_cache

random.seed(1212)

def count_table(s):
    """Full interval table. dp[i][j] = s[i..j] is a palindrome. i DESCENDING, j ASCENDING so dp[i+1][j-1] is ready."""
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[i][j] = s[i] == s[j] and (j - i < 3 or dp[i + 1][j - 1])
            cnt += dp[i][j]
    return cnt, dp

def count_row(s):
    """ONE row. dp[j] means 'is s[i..j] a palindrome' for the current i. j DESCENDING so dp[j-1] still holds row i+1."""
    n = len(s)
    dp = [False] * n
    cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i - 1, -1):
            dp[j] = s[i] == s[j] and (j - i < 3 or dp[j - 1])
            cnt += dp[j]
    return cnt

def count_center(s):
    """Expand around each of the 2n-1 centres (Part 3 Q9 idea)."""
    n, cnt = len(s), 0
    for c in range(2 * n - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < n and s[l] == s[r]:
            cnt += 1; l -= 1; r += 1
    return cnt

def brute(s):
    return sum(s[i:j] == s[i:j][::-1] for i in range(len(s)) for j in range(i + 1, len(s) + 1))

def count_memo(s):
    @lru_cache(maxsize=None)
    def pal(i, j):
        if i >= j: return True
        return s[i] == s[j] and pal(i + 1, j - 1)
    return sum(pal(i, j) for i in range(len(s)) for j in range(i, len(s)))

for s, want in [('abc', 3), ('aaa', 6), ('abba', 6), ('a', 1), ('abacaba', 12)]:
    assert count_table(s)[0] == count_row(s) == count_center(s) == brute(s) == want, s
print('5 prompt examples ok')

cnt, dp = count_table('abba')
print("dp for s='abba' (row i, col j, T = palindrome):")
print('     ', ' '.join('abba'))
for i, row in enumerate(dp):
    print('  ', 'abba'[i], ' '.join('T' if v else '.' for v in row))
print('count =', cnt)

for _ in range(1000):
    s = ''.join(random.choice('ab') for _ in range(random.randint(1, 12)))
    assert count_table(s)[0] == count_row(s) == count_center(s) == brute(s) == count_memo(s), s
print('1000 seeded random strings (len 1..12, alphabet ab): table == one row == centres == enumeration == memo')

# what breaks if the one-row inner loop runs ASCENDING: dp[j-1] would already be row i, not row i+1
def bad_row(s):
    n = len(s); dp = [False] * n; cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[j] = s[i] == s[j] and (j - i < 3 or dp[j - 1]); cnt += dp[j]
    return cnt
wrong = sum(bad_row(s) != brute(s) for s in (''.join(random.choice('ab') for _ in range(8)) for _ in range(300)))
print('ascending inner loop in the one-row version is wrong on', wrong, 'of 300 random strings')
assert wrong > 0

big = 'a' * 1000
print('n = 1000 all a:', count_row(big), '== n(n+1)/2 =', 1000 * 1001 // 2)
assert count_row(big) == count_table(big)[0] == count_center(big) == 500500
rnd = ''.join(random.choice('ab') for _ in range(1000))
assert count_row(rnd) == count_center(rnd)
print('random 1000 over {a,b}: DP row == centres ==', count_row(rnd))

# memoised version: recursion depth is only ~n/2 per call chain, but the outer loop makes n^2/2 cache entries
print('recursion limit:', sys.getrecursionlimit(), '| memo n=1000 all a:', end=' ')
try:
    print(count_memo(big))
except RecursionError:
    print('RecursionError')
print('memo n=2100 all a (depth about 1050):', end=' ')
try:
    count_memo('a' * 2100); print('ok')
except RecursionError:
    print('RecursionError')
assert count_center('') == 0
print('edge asserts ok')
```

**Output (my run):**
```
5 prompt examples ok
dp for s='abba' (row i, col j, T = palindrome):
      a b b a
   a T . . T
   b . T T .
   b . . T .
   a . . . T
count = 6
1000 seeded random strings (len 1..12, alphabet ab): table == one row == centres == enumeration == memo
ascending inner loop in the one-row version is wrong on 248 of 300 random strings
n = 1000 all a: 500500 == n(n+1)/2 = 500500
random 1000 over {a,b}: DP row == centres == 3065
recursion limit: 1000 | memo n=1000 all a: 500500
memo n=2100 all a (depth about 1050): RecursionError
edge asserts ok
```

**Edge cases:**
- `'a'` returns 1; all-equal letters of length n return n(n+1)/2 (500500 at n = 1000).
- No equal neighbours (`'abc'`) returns n.
- Count by position: `'aaa'` has 6 (three `a`, two `aa`, one `aaa`), not 3 distinct strings.
- The `j - i < 3` guard: without it you would read `dp[i+1][j-1]` with `j-1 < i+1`, an empty interval, a classic off-by-one.

**Follow-ups:**
- Longest palindromic substring? Track the longest true cell (Part 3 Q8); same table.
- Minimum cuts into palindromes? Use the table as `pal[l][r]` and a 1D cuts array.
- Manacher's algorithm? O(n) time; mention it, you rarely code it.

**Common mistakes:**
- Filling rows top to bottom (`dp[i+1][j-1]` is not ready).
- Using `j - i < 2` and then reading an empty or out-of-range interval, or `<= 3` which wrongly accepts `abca`.
- Running the one-row loop upward.
- Counting distinct palindromes instead of positions.

### Q13 ⭐⭐ 🟡 Interleaving string. `s1`, `s2` and `s3` are lowercase strings with 0 <= len(s1), len(s2) <= 100 and 0 <= len(s3) <= 200. `s3` is an interleaving of `s1` and `s2` if it can be formed by merging them while keeping the relative order of the letters of each (take letters from either string in turn, any number at a time). Return True or False (all three empty is True; unequal lengths is False). Define `dp[i][j]` = the first i letters of s1 and the first j of s2 interleave into the first i + j of s3, give the transition, and then use one row of length len(s2) + 1. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (len(s1), len(s2) <= 6) on small inputs. Example: s1='aabcc', s2='dbbca', s3='aadbbcbcac' -> True; s1='aabcc', s2='dbbca', s3='aadbbbaccc' -> False; s1='', s2='', s3='' -> True; s1='a', s2='', s3='b' -> False.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP where the position in the THIRD string is forced: `k = i + j`. The table only needs the pair (i, j).

**Say this first (1 line):** "dp[i][j] is true if the first i letters of s1 and the first j of s2 can interleave into the first i + j of s3: the last letter of that prefix came from s1 (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or from s2 (dp[i][j-1] and s2[j-1] == s3[i+j-1]); one row of length len(s2) + 1 is enough."

**Brute force:** Plain recursion `f(i, j)`: look at `s3[i+j]` and branch into "take from s1" and "take from s2" when the letters match. Up to 2^(m+n) calls when many letters are equal, so only for len(s1), len(s2) <= 6. It is the checker.

**Optimal:**
- Quick reject: `len(s1) + len(s2) != len(s3)` is False.
- State: `dp[i][j]` = the first i letters of s1 and the first j letters of s2 interleave into the first `i + j` letters of s3.
- Transition: `dp[i][j] = (i > 0 and dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (j > 0 and dp[i][j-1] and s2[j-1] == s3[i+j-1])`.
- Base case: `dp[0][0] = True` (all three empty). Row 0 and column 0 come out of the same transition with one term guarded away.
- Why `s3` needs no index of its own: after taking i letters from s1 and j from s2, exactly i + j letters of s3 are used.
- One row: keep `dp[j]` for the current i. Before you overwrite it, `dp[j]` still holds `(i-1, j)` (the "from s1" term), and `dp[j-1]` was just written for this row, so it holds `(i, j-1)` (the "from s2" term). Loop j upward and assign `dp[j] = ok` every time (set it to False when neither term holds, never leave the old value).
- Recursion: the top-down depth is `len(s3) <= 200`, far under 1000. As observed on Python 3.13 the memoised version runs at the maximum size 100 + 100 (all `a`, depth 200). Nothing here needs bottom-up for safety, but the table is still the cleaner interview answer.
- Greedy matching ("take from s1 whenever the letters match") is wrong when both strings offer the same letter; the table keeps both possibilities.

**Complexity:** Time O(mn), space O(n) with the row (O(mn) with the table). Brute force up to O(2^(m+n)).

**Dry run:** `s1 = 'aabcc'`, `s2 = 'dbbca'`, `s3 = 'aadbbcbcac'`. T = true, `.` = false. Row label = letters of s1 used so far, column label = letters of s2 used so far.

| i \ j | 0 | 1 `d` | 2 `db` | 3 `dbb` | 4 `dbbc` | 5 `dbbca` |
|---|---|---|---|---|---|---|
| 0 | T | . | . | . | . | . |
| 1 `a` | T | . | . | . | . | . |
| 2 `aa` | T | T | T | T | T | . |
| 3 `aab` | . | T | T | . | T | . |
| 4 `aabc` | . | . | T | T | T | T |
| 5 `aabcc` | . | . | . | T | . | T |

Check a few cells. `(2,1)`: s3 prefix of 3 letters is `aad`; from `(2,0)` T plus `s2[0] = d == s3[2] = d`, so T. `(1,1)`: prefix `aa`; from `(0,1)` F (s2 letter `d` != `a`) and `(1,0)` T with `s2[0] = d != s3[1] = a`, so F. `(2,5)`: prefix of 7 is `aadbbcb`, last letter `b`, but `s1[1] = a` and `s2[4] = a`: F. `(5,5)`: last letter `c` (s3[9]); the s1 term needs `dp[4][5]` T and `s1[4] = c`: T. The answer is `dp[5][5] = True`.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1313)

def interleave_table(s1, s2, s3):
    """dp[i][j] = first i letters of s1 and first j of s2 interleave into the first i + j of s3."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return None
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for i in range(m + 1):
        for j in range(n + 1):
            if i and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = True
            if j and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = True
    return dp

def interleave(s1, s2, s3):
    """One row of length len(s2) + 1. Before the update dp[j] is (i-1, j); dp[j-1] is already (i, j-1)."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [False] * (n + 1)
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                dp[0] = True
                continue
            ok = False
            if i and dp[j] and s1[i - 1] == s3[i + j - 1]:        # last letter came from s1
                ok = True
            if j and dp[j - 1] and s2[j - 1] == s3[i + j - 1]:    # last letter came from s2
                ok = True
            dp[j] = ok          # overwrites (i-1, j); for i = 0 the old value is not read (guarded by `i and`)
    return dp[n]

def interleave_memo(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    @lru_cache(maxsize=None)
    def f(i, j):
        k = i + j
        if k == len(s3):
            return True
        return (i < len(s1) and s1[i] == s3[k] and f(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and f(i, j + 1))
    return f(0, 0)

def brute(s1, s2, s3):
    """Plain recursion, no memo (len(s1), len(s2) <= 6)."""
    def f(i, j):
        k = i + j
        if k == len(s3):
            return i == len(s1) and j == len(s2)
        return (i < len(s1) and s1[i] == s3[k] and f(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and f(i, j + 1))
    return len(s1) + len(s2) == len(s3) and f(0, 0)

for a, b, c, want in [('aabcc', 'dbbca', 'aadbbcbcac', True), ('aabcc', 'dbbca', 'aadbbbaccc', False), ('', '', '', True), ('a', '', 'b', False)]:
    assert interleave(a, b, c) == interleave_memo(a, b, c) == brute(a, b, c) == want, (a, b, c)
print('4 prompt examples ok')

dp = interleave_table('aabcc', 'dbbca', 'aadbbcbcac')
print("dp for s1='aabcc' (rows i=0..5), s2='dbbca' (cols j=0..5), T = true:")
print('      ', ' '.join('-dbbca'))
for i, row in enumerate(dp):
    print('  ', '-aabcc'[i], ' '.join('T' if v else '.' for v in row))

true_cases = 0
for _ in range(2000):
    s1 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    s2 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    if random.random() < 0.5:                       # build a true interleaving
        pool, i, j, out = (s1, s2), 0, 0, []
        while i < len(s1) or j < len(s2):
            if j == len(s2) or (i < len(s1) and random.random() < 0.5): out.append(s1[i]); i += 1
            else: out.append(s2[j]); j += 1
        s3 = ''.join(out)
        if random.random() < 0.3 and s3:           # corrupt one letter sometimes
            k = random.randrange(len(s3)); s3 = s3[:k] + random.choice('abc') + s3[k + 1:]
    else:
        s3 = ''.join(random.choice('abc') for _ in range(random.randint(0, 12)))
    r = interleave(s1, s2, s3)
    assert r == brute(s1, s2, s3) == interleave_memo(s1, s2, s3), (s1, s2, s3)
    assert (interleave_table(s1, s2, s3) or [[False]])[-1][-1] == r
    true_cases += r
print('2000 seeded random triples: one row == plain recursion == memo == table; True in', true_cases, 'of 2000 (both answers occur)')
assert 0 < true_cases < 2000

cnt = 0
for l1 in range(4):
    for l2 in range(4):
        for s1 in itertools.product('ab', repeat=l1):
            for s2 in itertools.product('ab', repeat=l2):
                for s3 in itertools.product('ab', repeat=l1 + l2):
                    a, b, c = ''.join(s1), ''.join(s2), ''.join(s3)
                    assert interleave(a, b, c) == brute(a, b, c); cnt += 1
print('exhaustive over {a,b}, len(s1), len(s2) <= 3, len(s3) = len(s1) + len(s2):', cnt, 'ok')

# maximum size and recursion depth (the memo recursion depth is len(s3) <= 200)
print('recursion limit:', sys.getrecursionlimit())
x, y = 'a' * 100, 'a' * 100
print('max size 100 + 100 -> 200, all a: row', interleave(x, y, 'a' * 200), '| memo (depth 200)', interleave_memo(x, y, 'a' * 200))
x = ''.join(random.choice('ab') for _ in range(100)); y = ''.join(random.choice('ab') for _ in range(100))
z = ''.join(x[i // 2] if i % 2 == 0 else y[i // 2] for i in range(200))      # strict alternation is a valid interleaving
assert interleave(x, y, z) and interleave_memo(x, y, z)
print('alternating merge of two random 100-letter strings:', interleave(x, y, z))

assert interleave('', 'abc', 'abc') and interleave('abc', '', 'abc') and not interleave('a', 'b', 'a')
assert not interleave('a', 'b', 'abc')
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
dp for s1='aabcc' (rows i=0..5), s2='dbbca' (cols j=0..5), T = true:
       - d b b c a
   - T . . . . .
   a T . . . . .
   a T T T T T .
   b . T T . T .
   c . . T T T T
   c . . . T . T
2000 seeded random triples: one row == plain recursion == memo == table; True in 828 of 2000 (both answers occur)
exhaustive over {a,b}, len(s1), len(s2) <= 3, len(s3) = len(s1) + len(s2): 7225 ok
recursion limit: 1000
max size 100 + 100 -> 200, all a: row True | memo (depth 200) True
alternating merge of two random 100-letter strings: True
edge asserts ok
```

**Edge cases:**
- All three empty returns True; `s1 = ''` reduces to `s2 == s3`.
- Length mismatch returns False before any table work.
- `s1 = 'a'`, `s2 = ''`, `s3 = 'b'` returns False.
- Same letters everywhere (`a` repeated): every split works, so a greedy "prefer s1" stays right by luck; random letters expose it.

**Follow-ups:**
- Count the number of ways? Replace `or` by `+` (and `and` by multiplication of the flag), same table.
- Three strings and an interleaving of k strings? State grows to a k-tuple; the idea is the same, the cost is the product of the lengths.
- Return one interleaving? Keep the full table and walk back from `(m, n)`, choosing the term that is true.

**Common mistakes:**
- Forgetting the length check, then indexing `s3` out of range.
- Off-by-one on `s3`: the letter being placed is `s3[i+j-1]` (1-based prefix lengths), not `s3[i+j]`.
- In the one-row version, leaving `dp[j]` unchanged when neither term holds (a stale True survives).
- Using `[[False]*(n+1)]*(m+1)` for the table (see Part 10 Q31).

### Q14 ⭐⭐ 🟡 Minimum path sum, and the path itself. `grid` is an m x n list of lists (1 <= m, n <= 200) of integers in 0..100. Moves are right 'R' or down 'D'. Return `[best, moves]` where `best` is the minimum path sum and `moves` is the string of m + n - 2 moves of an optimal path. Several optimal paths may exist, so the tie rule is fixed: among all minimum-sum paths return the lexicographically smallest move string with 'D' < 'R'. Build the table on SUFFIXES (cost from the cell to the end) so that at each cell you can step 'D' whenever it keeps the total optimal, and explain why walking back from the end with parent pointers does not give this string automatically. The 1 x 1 grid returns `[value, '']`. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) and taking the smallest (sum, string) pair on small inputs. Example: grid=[[1, 3, 1], [1, 5, 1], [4, 2, 1]] -> [7, 'RRDD']; grid=[[1, 1], [1, 1]] -> [3, 'DR']; grid=[[5]] -> [5, '']; grid=[[0, 0, 0], [0, 0, 0]] -> [0, 'DRR'].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP (right/down moves) plus path reconstruction under an explicit tie rule. The tie rule decides the table direction.

**Say this first (1 line):** "f[i][j] is the cheapest cost from (i, j) to the bottom-right cell; f[i][j] = grid[i][j] + min(f[i+1][j], f[i][j+1]); then I walk from the start and step D whenever D still keeps the total optimal, otherwise R, which gives the smallest D < R string."

**Brute force:** Enumerate every path: choose which of the `m + n - 2` moves are D (`C(m+n-2, m-1)` paths), sum the cells, keep the smallest `(sum, string)` pair. Fine for m, n <= 5 (at most 70 paths). It is the checker, and it applies the same tie rule by comparing the move strings.

**Optimal:**
- State: `f[i][j]` = minimum sum of a path from `(i, j)` to `(m-1, n-1)`, including the cell `(i, j)`. This is the SUFFIX direction.
- Transition: `f[i][j] = grid[i][j] + min(f[i+1][j], f[i][j+1])` (down or right). Use a border of infinity on row m and column n so edge cells have only one real option.
- Base case: `f[m-1][n-1] = grid[m-1][n-1]`.
- Walk forward from `(0, 0)`: at each cell, D is allowed to be chosen when `f[i+1][j] <= f[i][j+1]`, because then the remaining cost after stepping down equals the best remaining cost. If `D` is cheaper or equal, take `D` (tie goes to D, since `'D' < 'R'`); otherwise take `R`. On the last row or column the infinite border forces the only legal move.
- Why this is the lexicographically smallest optimal string: the first move is the most significant character. The suffix table tells us, at every cell, exactly which first moves stay optimal, so choosing the smaller letter among them at every step is greedy-correct.
- Why parent pointers from the end do not do it: with a PREFIX table (cost from the start) you walk back from the end and decide the LAST move first. A tie rule there ("came from above") fixes the last letters, not the first letters, so the string it returns is some optimal path but not the smallest. Measured below: on `[[1,1],[1,1]]` it gives `RD`, the rule wants `DR`; it differs on 264 of 500 random grids. The sum is the same, the string is not.
- Greedy "step to the cheaper neighbour" is not the DP at all: it gets the sum wrong on 184 of 500 random 4 x 4 grids.
- One row: the value alone needs only `row[j] = grid[i][j] + min(row[j], row[j+1])` going j downward (old `row[j]` is the cell below, `row[j+1]` is the cell to the right, just updated). Reconstruction needs the full table.
- Recursion: memoised `f(i, j)` nests `m + n - 1` frames. As observed on Python 3.13 with the default limit 1000: 200 x 200 (depth 399) runs, 600 x 600 (depth 1199) raises `RecursionError`. The prompt's maximum, 200 x 200, is safe, but bottom-up is the habit.

**Complexity:** Time O(mn), space O(mn) for the table (needed for the walk), O(n) for the value only. Walk O(m + n). Brute force O(C(m+n-2, m-1) * (m+n)).

**Dry run:** `grid = [[1,3,1],[1,5,1],[4,2,1]]`. Suffix table `f`:

| | j=0 | j=1 | j=2 |
|---|---|---|---|
| i=0 | 7 | 6 | 3 |
| i=1 | 8 | 7 | 2 |
| i=2 | 7 | 3 | 1 |

Fill order bottom-right to top-left: `f[2][2] = 1`; `f[2][1] = 2 + 1 = 3`; `f[2][0] = 4 + 3 = 7`; `f[1][2] = 1 + 1 = 2`; `f[1][1] = 5 + min(3, 2) = 7`; `f[1][0] = 1 + min(7, 7) = 8`; `f[0][2] = 1 + 2 = 3`; `f[0][1] = 3 + min(7, 3) = 6`; `f[0][0] = 1 + min(8, 6) = 7`. Best sum 7.
Walk: at `(0,0)` D leads to 8, R to 6, so R (f = 1 + 6). At `(0,1)` D leads to 7, R to 3, so R. At `(0,2)` only D (border): D. At `(1,2)` only D: D. Result `RRDD`.
A tie example is `[[1,1],[1,1]]`: at `(0,0)` D and R both lead to 2, so the rule picks D, giving `DR`.

**Code:**
```python
import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1414)
INF = float('inf')

def suffix_table(grid):
    """f[i][j] = minimum cost of a path from (i, j) to the bottom-right cell, cell (i, j) included."""
    m, n = len(grid), len(grid[0])
    f = [[INF] * (n + 1) for _ in range(m + 1)]        # a border of INF so out-of-grid moves never win
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                f[i][j] = grid[i][j]
            else:
                f[i][j] = grid[i][j] + min(f[i + 1][j], f[i][j + 1])
    return f

def min_path(grid):
    """[best, moves]: smallest sum, then lexicographically smallest move string with 'D' < 'R'."""
    m, n = len(grid), len(grid[0])
    f = suffix_table(grid)
    i = j = 0
    out = []
    while (i, j) != (m - 1, n - 1):
        if f[i + 1][j] <= f[i][j + 1]:          # D keeps the total optimal whenever it is no worse; tie -> D
            out.append('D'); i += 1
        else:
            out.append('R'); j += 1
    return [f[0][0], ''.join(out)]

def min_sum_one_row(grid):
    """Value only, one row (reconstruction needs the full table). row[j] = cost from (i, j) to the end."""
    m, n = len(grid), len(grid[0])
    row = [INF] * (n + 1)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                row[j] = grid[i][j]
            else:
                row[j] = grid[i][j] + min(row[j], row[j + 1])    # row[j] = below (old row), row[j+1] = right (new row)
    return row[0]

def prefix_parent_walk(grid):
    """The tempting alternative: prefix table g (cost from the start), then walk back from the end by parent pointers."""
    m, n = len(grid), len(grid[0])
    g = [[INF] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            g[i][j] = grid[i][j] + (0 if i == j == 0 else min(g[i - 1][j] if i else INF, g[i][j - 1] if j else INF))
    i, j, out = m - 1, n - 1, []
    while (i, j) != (0, 0):
        if i and (not j or g[i - 1][j] <= g[i][j - 1]):    # tie: arrived by D
            out.append('D'); i -= 1
        else:
            out.append('R'); j -= 1
    return [g[m - 1][n - 1], ''.join(reversed(out))]

def min_path_memo(grid):
    m, n = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == m - 1 and j == n - 1:
            return grid[i][j]
        best = INF
        if i + 1 < m: best = min(best, f(i + 1, j))
        if j + 1 < n: best = min(best, f(i, j + 1))
        return grid[i][j] + best
    return f(0, 0)

def brute(grid):
    """Every path (m, n <= 5): all choices of which of the m+n-2 moves are D; min of (sum, string)."""
    m, n = len(grid), len(grid[0]); best = None
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        mv = ['R'] * (m + n - 2)
        for d in ds: mv[d] = 'D'
        i = j = 0; tot = grid[0][0]
        for c in mv:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]
        cand = (tot, ''.join(mv))
        if best is None or cand < best: best = cand
    return list(best)

for g, want in [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], [7, 'RRDD']), ([[1, 1], [1, 1]], [3, 'DR']), ([[5]], [5, '']), ([[0, 0, 0], [0, 0, 0]], [0, 'DRR'])]:
    assert min_path(g) == brute(g) == want, g
    assert min_sum_one_row(g) == want[0] == min_path_memo(g)
print('4 prompt examples ok')

g = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
print('suffix table f (cost from the cell to the end) for', g)
for row in suffix_table(g)[:-1]:
    print(' ', row[:-1])
print('walk ->', min_path(g))

for _ in range(1000):
    m, n = random.randint(1, 5), random.randint(1, 5)
    grid = [[random.randint(0, 3) for _ in range(n)] for _ in range(m)]
    assert min_path(grid) == brute(grid), grid
    assert min_sum_one_row(grid) == min_path_memo(grid) == brute(grid)[0]
print('1000 seeded random grids (m, n <= 5, values 0..3): table walk == enumeration of (sum, string); one row and memo give the same sum')

# exhaustive: every 2 x 3 grid with values 0..2 (729) and every 3 x 3 grid with values 0..1 (512)
cnt = 0
for m, n, vmax in ((2, 3, 3), (3, 3, 2)):
    for cells in itertools.product(range(vmax), repeat=m * n):
        grid = [list(cells[r * n:(r + 1) * n]) for r in range(m)]
        assert min_path(grid) == brute(grid); cnt += 1
print('exhaustive 2x3 (values 0..2) and 3x3 (values 0..1) grids:', cnt, 'ok')

# claim: parent pointers from the end do not give the D < R smallest string automatically
diff = 0
for _ in range(500):
    m, n = random.randint(2, 5), random.randint(2, 5)
    grid = [[random.randint(0, 2) for _ in range(n)] for _ in range(m)]
    a, b = prefix_parent_walk(grid), min_path(grid)
    assert a[0] == b[0]
    diff += a[1] != b[1]
print('prefix-table parent walk (tie: arrived by D) returns a different path than the suffix tie rule on', diff, 'of 500 random grids')
assert diff > 0
print('example [[1,1],[1,1]]: parent walk', prefix_parent_walk([[1, 1], [1, 1]]), 'vs suffix walk', min_path([[1, 1], [1, 1]]))

# greedy "step to the cheaper neighbour" is not the DP
def greedy(grid):
    m, n = len(grid), len(grid[0]); i = j = 0; tot = grid[0][0]
    while (i, j) != (m - 1, n - 1):
        if i == m - 1: j += 1
        elif j == n - 1: i += 1
        elif grid[i + 1][j] <= grid[i][j + 1]: i += 1
        else: j += 1
        tot += grid[i][j]
    return tot
bad = 0
for _ in range(500):
    grid = [[random.randint(0, 9) for _ in range(4)] for _ in range(4)]
    bad += greedy(grid) != min_path(grid)[0]
print('greedy cheaper-neighbour sum is wrong on', bad, 'of 500 random 4x4 grids')

# max size and recursion
print('recursion limit:', sys.getrecursionlimit())
big = [[random.randint(0, 100) for _ in range(200)] for _ in range(200)]
t = time.perf_counter(); r = min_path(big); dt = time.perf_counter() - t
assert r[0] == min_sum_one_row(big) == min_path_memo(big) and len(r[1]) == 398 and r[1].count('D') == 199
print('200 x 200: best', r[0], 'path length', len(r[1]), '| memo (depth 399) agrees | sandbox time under 2 s:', dt < 2)
huge = [[1] * 600 for _ in range(600)]
print('bottom-up 600 x 600 all ones ->', min_path(huge)[0], end=' | memo 600 x 600: ')
try:
    min_path_memo(huge); print('ok')
except RecursionError:
    print('RecursionError (depth 1199)')

assert min_path([[7]]) == [7, ''] and min_path([[1, 2, 3]]) == [6, 'RR'] and min_path([[1], [2], [3]]) == [6, 'DD']
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
suffix table f (cost from the cell to the end) for [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
  [7, 6, 3]
  [8, 7, 2]
  [7, 3, 1]
walk -> [7, 'RRDD']
1000 seeded random grids (m, n <= 5, values 0..3): table walk == enumeration of (sum, string); one row and memo give the same sum
exhaustive 2x3 (values 0..2) and 3x3 (values 0..1) grids: 1241 ok
prefix-table parent walk (tie: arrived by D) returns a different path than the suffix tie rule on 264 of 500 random grids
example [[1,1],[1,1]]: parent walk [3, 'RD'] vs suffix walk [3, 'DR']
greedy cheaper-neighbour sum is wrong on 184 of 500 random 4x4 grids
recursion limit: 1000
200 x 200: best 10070 path length 398 | memo (depth 399) agrees | sandbox time under 2 s: True
bottom-up 600 x 600 all ones -> 1199 | memo 600 x 600: RecursionError (depth 1199)
edge asserts ok
```

**Edge cases:**
- 1 x 1 returns `[value, '']`.
- One row or one column has exactly one path (`'RR'`, `'DD'`).
- All zeros returns `'D'` repeated, then `'R'` repeated (`'DRR'` for 2 x 3): D first as long as it is optimal.
- Zeros and large values mixed: ties are common with 0..3 values, which is why the random tests use a tiny range.

**Follow-ups:**
- Count how many minimum paths exist? A second table with the same shape (add the counts of the cells that achieve the minimum), with the modulus rule of that prompt.
- Largest sum instead of smallest? Swap `min` for `max` (same table, same walk rule).
- Allow diagonal moves? Add `f[i+1][j+1]` to the `min`, and a third letter to the tie rule.

**Common mistakes:**
- Using a prefix table and walking back with a tie rule, expecting the smallest string.
- Walking with `<` instead of `<=` (then ties go to R, giving `RD` on `[[1,1],[1,1]]`).
- Forgetting the infinity border and reading out of range on the last row or column.
- Adding `grid[i][j]` twice, or leaving out the end cell in the base case.

### Q15 ⭐⭐ 🟡 Edit distance with the edit script. `a` and `b` are lowercase strings with 0 <= len <= 300 each. Return `[distance, script]` where `script` is a string over the letters D (delete the next letter of `a`), I (insert the next letter of `b`), M (match: the next letters are equal and both advance) and S (substitute: the next letters differ, both advance); D, I and S cost 1, M costs 0, and the script consumes all of `a` and all of `b`. Many optimal scripts can exist, so the tie rule is fixed: return the lexicographically smallest script among the optimal ones (alphabet order D < I < M < S). Fill the table on suffixes and walk forward trying D, I, M, S in that order. Show that applying the script to `a` gives `b`. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every valid script by plain recursion (len <= 5) and taking the smallest (cost, script) pair on small inputs. Example: a='horse', b='ros' -> [3, 'SMDMD']; a='ab', b='ba' -> [2, 'DMI']; a='', b='ab' -> [2, 'II']; a='abc', b='abc' -> [0, 'MMM']; a='kitten', b='sitting' -> [3, 'SMMMSMI'].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP (edit distance) on SUFFIXES, then a forward walk that tries the operations in the tie-rule order D, I, M, S.

**Say this first (1 line):** "f[i][j] is the edit distance between a[i:] and b[j:]: delete costs 1 + f[i+1][j], insert costs 1 + f[i][j+1], and a diagonal step costs f[i+1][j+1] plus 1 if the letters differ; I fill it bottom-up and walk forward trying D, I, M, S in that order, which is exactly the smallest optimal script."

**Brute force:** Plain recursion over `(i, j)`: at each point try D, I, and the diagonal (M when the letters are equal, S otherwise), collect every complete script with its cost, and take the smallest `(cost, script)` pair. Exponential (about 3^(m+n) leaves), so only for len <= 5. It is the checker and applies the same tie rule.

**Optimal:**
- State: `f[i][j]` = minimum cost to turn `a[i:]` into `b[j:]`.
- Transition (`i < n` and `j < m`): `f[i][j] = min(1 + f[i+1][j] (D), 1 + f[i][j+1] (I), f[i+1][j+1] + (a[i] != b[j]) (M if equal, S if not))`.
- Base cases: `f[n][j] = m - j` (only inserts remain), `f[i][m] = n - i` (only deletes remain), `f[n][m] = 0`.
- Walk from `(0, 0)` until both strings are consumed. At each cell check in order:
  1. `D` if `i < n` and `f[i][j] == 1 + f[i+1][j]`.
  2. `I` if `j < m` and `f[i][j] == 1 + f[i][j+1]`.
  3. `M` if both letters exist, are equal and `f[i][j] == f[i+1][j+1]` (when letters are equal this always holds if D and I did not apply; the code asserts it).
  4. otherwise `S` (letters differ and `f[i][j] == 1 + f[i+1][j+1]`).
- Why lexicographically smallest: the table tells which first operations keep the total optimal; trying them in alphabet order D < I < M < S and committing to the first that works makes every character as small as possible from the front.
- Replaying the script: `D` skips the next letter of `a`, `I` copies the next letter of `b`, `M` and `S` consume one letter of each and write the letter of `b`. After the whole script you have consumed all of `a` and all of `b`, and the output equals `b`. The number of non-M letters equals the distance because D, I, S cost 1 and M costs 0.
- Space: the value alone needs two rows (`prev` = row i+1, `cur` = row i). The script needs the full table (or Hirschberg's linear-space method, not required here).
- Recursion: the top-down version nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two 300-letter strings run (depth at most 600); two disjoint 600-letter strings (depth 1200) raise `RecursionError`. The prompt's maximum is 300 each, but I still use bottom-up. Observation, not a rule.

**Complexity:** Time O(mn), space O(mn) for the script, O(min(m, n)) for the distance alone. Walk O(m + n). Brute force exponential.

**Dry run:** `a = 'horse'`, `b = 'ros'`. Rows are suffixes of `a`, columns suffixes of `b`.

| | j=0 `ros` | j=1 `os` | j=2 `s` | j=3 `` |
|---|---|---|---|---|
| i=0 `horse` | 3 | 3 | 4 | 5 |
| i=1 `orse` | 3 | 2 | 3 | 4 |
| i=2 `rse` | 2 | 2 | 2 | 3 |
| i=3 `se` | 3 | 2 | 1 | 2 |
| i=4 `e` | 3 | 2 | 1 | 1 |
| i=5 `` | 3 | 2 | 1 | 0 |

Walk. `(0,0)` f=3: D gives `1 + f[1][0] = 4` no; I gives `1 + f[0][1] = 4` no; `h != r`, so S (`1 + f[1][1] = 3`). `(1,1)` f=2: D `1 + f[2][1] = 3` no; I `1 + f[1][2] = 4` no; `o == o` and `f[2][2] = 2`, so M. `(2,2)` f=2 (`rse` vs `s`): D `1 + f[3][2] = 2` yes, D. `(3,2)` f=1 (`se` vs `s`): D `1 + f[4][2] = 2` no; I `1 + f[3][3] = 3` no; `s == s`, `f[4][3] = 1`, M. `(4,3)` f=1: only `e` left in `a`, D. Script `SMDMD`, distance 3. Replay on `horse`: S writes `r`, M writes `o`, D skips `r`, M writes `s`, D skips `e`: `ros`.

**Code:**
```python
import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1515)

def suffix_table(a, b):
    """f[i][j] = edit distance between a[i:] and b[j:]. Base: f[n][j] = m - j (insert the rest), f[i][m] = n - i (delete the rest)."""
    n, m = len(a), len(b)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                f[i][j] = m - j
            elif j == m:
                f[i][j] = n - i
            else:
                f[i][j] = min(1 + f[i + 1][j],                              # D: delete a[i]
                              1 + f[i][j + 1],                              # I: insert b[j]
                              f[i + 1][j + 1] + (a[i] != b[j]))             # M (free) or S (cost 1)
    return f

def edit_script(a, b):
    """[distance, script], lexicographically smallest optimal script with D < I < M < S."""
    n, m = len(a), len(b)
    f = suffix_table(a, b)
    i = j = 0
    out = []
    while i < n or j < m:
        if i < n and f[i][j] == 1 + f[i + 1][j]:
            out.append('D'); i += 1
        elif j < m and f[i][j] == 1 + f[i][j + 1]:
            out.append('I'); j += 1
        elif i < n and j < m and a[i] == b[j] and f[i][j] == f[i + 1][j + 1]:
            out.append('M'); i += 1; j += 1
        else:
            assert i < n and j < m and a[i] != b[j] and f[i][j] == 1 + f[i + 1][j + 1]
            out.append('S'); i += 1; j += 1
    return [f[0][0], ''.join(out)]

def distance_two_rows(a, b):
    """Value only, O(min) space: prev = row i+1, cur = row i."""
    n, m = len(a), len(b)
    prev = [m - j for j in range(m + 1)]                    # row i = n
    for i in range(n - 1, -1, -1):
        cur = [0] * (m + 1)
        cur[m] = n - i
        for j in range(m - 1, -1, -1):
            cur[j] = min(1 + prev[j], 1 + cur[j + 1], prev[j + 1] + (a[i] != b[j]))
        prev = cur
    return prev[0]

def distance_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        return min(1 + f(i + 1, j), 1 + f(i, j + 1), f(i + 1, j + 1) + (a[i] != b[j]))
    return f(0, 0)

def apply_script(a, b, script):
    """Replay the script on a; asserts every M is a real match, every S a real difference, and everything is consumed."""
    i = j = 0; out = []
    for c in script:
        if c == 'D': i += 1
        elif c == 'I': out.append(b[j]); j += 1
        elif c == 'M': assert a[i] == b[j]; out.append(a[i]); i += 1; j += 1
        else: assert a[i] != b[j]; out.append(b[j]); i += 1; j += 1
    assert i == len(a) and j == len(b)
    return ''.join(out)

def brute(a, b):
    """Every valid script by plain recursion (len <= 5); smallest (cost, script)."""
    res = []
    def go(i, j, s, cost):
        if i == len(a) and j == len(b): res.append((cost, s)); return
        if i < len(a): go(i + 1, j, s + 'D', cost + 1)
        if j < len(b): go(i, j + 1, s + 'I', cost + 1)
        if i < len(a) and j < len(b):
            go(i + 1, j + 1, s + ('M' if a[i] == b[j] else 'S'), cost + (a[i] != b[j]))
    go(0, 0, '', 0)
    return list(min(res))

for a, b, want in [('horse', 'ros', [3, 'SMDMD']), ('ab', 'ba', [2, 'DMI']), ('', 'ab', [2, 'II']), ('abc', 'abc', [0, 'MMM']), ('kitten', 'sitting', [3, 'SMMMSMI'])]:
    r = edit_script(a, b)
    assert r == brute(a, b) == want and distance_two_rows(a, b) == distance_memo(a, b) == want[0], (a, b)
    assert apply_script(a, b, r[1]) == b
print('5 prompt examples ok')

f = suffix_table('horse', 'ros')
print("f (distance of a[i:], b[j:]) for a='horse' (rows), b='ros' (cols j=0..3):")
for i, row in enumerate(f):
    print(' ', ('horse-')[i], row)
print('script ->', edit_script('horse', 'ros'))

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 5)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 5)))
    r = edit_script(a, b)
    assert r == brute(a, b), (a, b)
    assert distance_two_rows(a, b) == distance_memo(a, b) == r[0]
    assert apply_script(a, b, r[1]) == b and sum(c != 'M' for c in r[1]) == r[0]
print('500 seeded random pairs (len 0..5, alphabet abc): script == enumeration, two-row == memo, script turns a into b, non-M count == distance')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        r = edit_script(a, b)
        assert r == brute(a, b) and apply_script(a, b, r[1]) == b and sum(c != 'M' for c in r[1]) == r[0]; cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok (script == smallest optimal, replay gives b, non-M letters == distance)')

# recursion and size
print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(300)); y = ''.join(random.choice('abcd') for _ in range(300))
t = time.perf_counter(); r = edit_script(x, y); dt = time.perf_counter() - t
assert r[0] == distance_two_rows(x, y) and apply_script(x, y, r[1]) == y
print('bottom-up 300 x 300: distance', r[0], 'script length', len(r[1]), '| memo 300 x 300 agrees:', distance_memo(x, y) == r[0])
try:
    distance_memo('a' * 600, 'b' * 600); print('memo 600 + 600 disjoint: ok')
except RecursionError:
    print('memo 600 + 600 disjoint: RecursionError')
assert edit_script('', '') == [0, ''] and edit_script('abc', '') == [3, 'DDD'] and edit_script('a', 'b') == [1, 'S']
print('edge asserts ok')
```

**Output (my run):**
```
5 prompt examples ok
f (distance of a[i:], b[j:]) for a='horse' (rows), b='ros' (cols j=0..3):
  h [3, 3, 4, 5]
  o [3, 2, 3, 4]
  r [2, 2, 2, 3]
  s [3, 2, 1, 2]
  e [3, 2, 1, 1]
  - [3, 2, 1, 0]
script -> [3, 'SMDMD']
500 seeded random pairs (len 0..5, alphabet abc): script == enumeration, two-row == memo, script turns a into b, non-M count == distance
exhaustive pairs over {a,b}, len <= 4: 961 ok (script == smallest optimal, replay gives b, non-M letters == distance)
recursion limit: 1000
bottom-up 300 x 300: distance 157 script length 343 | memo 300 x 300 agrees: True
memo 600 + 600 disjoint: RecursionError
edge asserts ok
```

**Edge cases:**
- `a = ''`, `b = 'ab'` returns `[2, 'II']`; `a = 'abc'`, `b = ''` returns `[3, 'DDD']`; both empty returns `[0, '']`.
- Equal strings return all `M`.
- `'ab'` to `'ba'`: distance 2 (no swap operation), script `DMI` (delete `a`, match `b`, insert `a`).
- Several optimal scripts exist for most inputs; the tie rule picks one (for `'ab'`, `'ba'` the alternative `SS` also costs 2 but sorts after `DMI`).

**Follow-ups:**
- Allow a transposition (Damerau)? Add a fourth transition when `a[i] == b[j+1]` and `a[i+1] == b[j]`.
- Different costs for D, I, S? Put the weights into the transitions; the walk compares against the weighted values.
- Linear space with the script? Hirschberg: forward and backward distance rows around the middle row of `a`, recurse.

**Common mistakes:**
- Treating a mismatch diagonal as free, or an equal-letter diagonal as cost 1.
- Wrong bases (`f[0][j] = j` is the PREFIX version; for suffixes it is `m - j`).
- Trying M before D and I in the walk, so the script is optimal but not the smallest.
- Replaying with `S` when the letters are equal (the script must use `M` there, which costs 0).

### Q16 ⭐⭐ 🟡 Shortest common supersequence. `a` and `b` are lowercase strings with 0 <= len <= 500 each. Return a shortest string that has both `a` and `b` as subsequences. Several shortest strings can exist, so the tie rule is fixed: return the lexicographically smallest of the shortest. State the length as len(a) + len(b) - LCS(a, b) and why, build the table on suffixes (`f[i][j]` = SCS length of a[i:] and b[j:]) and walk forward: equal heads are emitted once, otherwise emit the smaller head letter among the moves that keep the total optimal. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every string of the right length in alphabetical order (len <= 4, alphabet a-c) on small inputs. Example: a='abac', b='cab' -> 'cabac'; a='abc', b='abc' -> 'abc'; a='', b='xy' -> 'xy'; a='ab', b='ba' -> 'aba'.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** LCS in disguise. The supersequence shares every common letter once and pays for the rest. The table is on suffixes so the walk can fix the smallest letter first.

**Say this first (1 line):** "g[i][j] is the shortest common supersequence length of a[i:] and b[j:]: equal heads cost one letter, otherwise 1 + min(skip a's head, skip b's head); the length is m + n - LCS, and I rebuild the string forward, emitting equal heads once and otherwise the smaller head among the moves that keep the total optimal."

**Brute force:** Compute the target length `L`, then try every string of length L over the letters of `a` and `b` in alphabetical order; the first one that contains both inputs as subsequences is the answer. Exponential, so only len <= 4 over a-c (the check also verifies the length against a pure search that does not use the LCS formula).

**Optimal:**
- State: `g[i][j]` = length of a shortest common supersequence of `a[i:]` and `b[j:]`.
- Transition: if `a[i] == b[j]` then `g[i][j] = 1 + g[i+1][j+1]`; else `g[i][j] = 1 + min(g[i+1][j], g[i][j+1])` (emit `a[i]` and move in `a`, or emit `b[j]` and move in `b`).
- Base cases: `g[n][j] = m - j`, `g[i][m] = n - i` (emit what remains of the other string).
- Length identity: `g[0][0] = m + n - LCS(a, b)`. Each letter of an LCS is emitted once for two inputs, so we save one letter per common letter and no more can be saved.
- Walk from `(0, 0)` while both strings have letters left:
  - equal heads: emit the letter once, move both;
  - different heads: collect the moves that keep the total (`g[i][j] == 1 + g[i+1][j]` means emit `a[i]`; `g[i][j] == 1 + g[i][j+1]` means emit `b[j]`) and take the one with the smaller letter (the two letters differ, so there is no tie);
  - when one string is exhausted, append the rest of the other.
- Why lexicographically smallest: the first emitted letter is the most significant, and the table says exactly which letters can come first in some shortest answer; take the smallest at every step. Equal heads: emitting the shared letter once is optimal, and the string starts with that letter either way. The exhaustive check below confirms it against the alphabetical enumeration for all 961 pairs over {a, b} up to length 4.
- Space: length alone needs two rows (as in LCS); the string needs the table (or Hirschberg).
- Recursion: top-down nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two random 300-letter strings run; two disjoint 500-letter strings (depth up to 1000) raise `RecursionError`. The prompt allows 500 each, so use the loops.

**Complexity:** Time O(mn), space O(mn) for the string (O(min(m, n)) for the length only). Walk O(m + n). Brute force O(k^L * L), exponential.

**Dry run:** `a = 'abac'`, `b = 'cab'`.

| | j=0 `cab` | j=1 `ab` | j=2 `b` | j=3 `` |
|---|---|---|---|---|
| i=0 `abac` | 5 | 4 | 4 | 4 |
| i=1 `bac` | 5 | 4 | 3 | 3 |
| i=2 `ac` | 4 | 3 | 3 | 2 |
| i=3 `c` | 3 | 3 | 2 | 1 |
| i=4 `` | 3 | 2 | 1 | 0 |

Length 5 = 4 + 3 - 2 (LCS `ab`). Walk: `(0,0)`: heads `a` and `c` differ. Emit `a` would need `1 + g[1][0] = 6`, not 5, so it is not allowed; emit `c` needs `1 + g[0][1] = 5`, allowed. Emit `c`, go to `(0,1)`. Heads `a` and `a` are equal: emit `a`, go to `(1,2)`. Heads `b` and `b`: emit `b`, go to `(2,3)`. `b` is exhausted: append `a[2:] = 'ac'`. Result `cabac`.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1616)

def suffix_table(a, b):
    """g[i][j] = length of a shortest common supersequence of a[i:] and b[j:]."""
    n, m = len(a), len(b)
    g = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                g[i][j] = m - j                       # only b's rest is left: emit it
            elif j == m:
                g[i][j] = n - i
            elif a[i] == b[j]:
                g[i][j] = 1 + g[i + 1][j + 1]         # equal heads: emit once
            else:
                g[i][j] = 1 + min(g[i + 1][j], g[i][j + 1])
    return g

def scs(a, b):
    """Lexicographically smallest shortest common supersequence."""
    n, m = len(a), len(b)
    g = suffix_table(a, b)
    i = j = 0
    out = []
    while i < n and j < m:
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        else:
            options = []                              # (letter, move) for the moves that keep the total optimal
            if g[i][j] == 1 + g[i + 1][j]: options.append((a[i], 'a'))
            if g[i][j] == 1 + g[i][j + 1]: options.append((b[j], 'b'))
            letter, move = min(options)               # letters differ, so no tie inside min
            out.append(letter)
            if move == 'a': i += 1
            else: j += 1
    out.append(a[i:]); out.append(b[j:])              # at most one of these is non-empty
    return ''.join(out)

def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def scs_length_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        if a[i] == b[j]: return 1 + f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def is_subseq(t, s):
    it = iter(s)
    return all(ch in it for ch in t)

def brute(a, b):
    """Every string of the right length in alphabetical order; the first that contains both is the answer."""
    L = len(a) + len(b) - lcs_length(a, b)
    alpha = sorted(set(a) | set(b))
    for t in itertools.product(alpha, repeat=L):
        t = ''.join(t)
        if is_subseq(a, t) and is_subseq(b, t):
            return t
    return None

def brute_length(a, b):
    """Independent length check (does not use the LCS formula): shortest L for which some string works."""
    alpha = sorted(set(a) | set(b))
    for L in range(max(len(a), len(b)), len(a) + len(b) + 1):
        for t in itertools.product(alpha, repeat=L):
            t = ''.join(t)
            if is_subseq(a, t) and is_subseq(b, t):
                return L

for a, b, want in [('abac', 'cab', 'cabac'), ('abc', 'abc', 'abc'), ('', 'xy', 'xy'), ('ab', 'ba', 'aba')]:
    assert scs(a, b) == brute(a, b) == want, (a, b)
print('4 prompt examples ok')

g = suffix_table('abac', 'cab')
print("g (SCS length of a[i:], b[j:]) for a='abac' (rows), b='cab' (cols j=0..3):")
for i, row in enumerate(g):
    print(' ', 'abac-'[i], row)
print('walk ->', scs('abac', 'cab'))

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 4)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 4)))
    r = scs(a, b)
    assert r == brute(a, b), (a, b)
    assert len(r) == len(a) + len(b) - lcs_length(a, b) == suffix_table(a, b)[0][0] == scs_length_memo(a, b)
    assert is_subseq(a, r) and is_subseq(b, r)
print('500 seeded random pairs (len 0..4, alphabet abc): walk == alphabetical enumeration; length == m + n - LCS == memo; both inputs are subsequences')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        r = scs(a, b)
        assert r == brute(a, b) and len(r) == brute_length(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok (also the length equals the shortest length found by search, not by the LCS formula)')

print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(500)); y = ''.join(random.choice('abcd') for _ in range(500))
r = scs(x, y)
assert len(r) == 1000 - lcs_length(x, y) and is_subseq(x, r) and is_subseq(y, r)
print('bottom-up 500 + 500 random: length', len(r), '(= 1000 - LCS)')
print('memoised length, two random 300-letter strings:', scs_length_memo(x[:300], y[:300]))
try:
    scs_length_memo('a' * 500, 'b' * 500); print('memoised disjoint 500 + 500: ok')
except RecursionError:
    print('memoised disjoint 500 + 500: RecursionError (depth up to 1000)')
print('disjoint 500 + 500 bottom-up length:', len(scs('a' * 500, 'b' * 500)))

assert scs('', '') == '' and scs('abc', '') == 'abc' and scs('a', 'a') == 'a' and scs('b', 'a') == 'ab'
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
g (SCS length of a[i:], b[j:]) for a='abac' (rows), b='cab' (cols j=0..3):
  a [5, 4, 4, 4]
  b [5, 4, 3, 3]
  a [4, 3, 3, 2]
  c [3, 3, 2, 1]
  - [3, 2, 1, 0]
walk -> cabac
500 seeded random pairs (len 0..4, alphabet abc): walk == alphabetical enumeration; length == m + n - LCS == memo; both inputs are subsequences
exhaustive pairs over {a,b}, len <= 4: 961 ok (also the length equals the shortest length found by search, not by the LCS formula)
recursion limit: 1000
bottom-up 500 + 500 random: length 677 (= 1000 - LCS)
memoised length, two random 300-letter strings: 408
memoised disjoint 500 + 500: RecursionError (depth up to 1000)
disjoint 500 + 500 bottom-up length: 1000
edge asserts ok
```

**Edge cases:**
- One or both empty: the other string (or `''`).
- Equal strings return the string; `a` a subsequence of `b` returns `b`.
- `'ab'` and `'ba'` give `'aba'` (length 3 = 2 + 2 - 1), not `'abba'`.
- Disjoint alphabets: the answer has length m + n and the smaller letters come first where allowed.

**Follow-ups:**
- Why is the answer length m + n - LCS? Every common letter that is shared saves one; the best sharing is an LCS.
- Count the shortest supersequences? Counting DP with care for duplicates; ask for the distinct strings or the ways.
- Minimum insertions to make a string a palindrome? `n - LPS(s)` (LPS is the LCS of `s` and its reverse).

**Common mistakes:**
- Emitting the equal letter twice.
- Picking "the first option that works" without comparing the letters (gives a shortest, not the smallest).
- Building the answer from the end of a prefix table (the tie rule is on the front of the string).
- Forgetting to append the leftover tail once one string runs out.

### Q17 ⭐⭐ 🟡 Wildcard matching as a counting DP. `s` is a lowercase string (0 <= len <= 300) and `p` a pattern (0 <= len <= 300) of lowercase letters, '?' (exactly one character) and '*' (any run of characters, possibly empty). Return `[matches, ways]` where `matches` is True when `p` matches the whole of `s` and `ways` is the number of distinct assignments of run lengths to the '*' symbols (in order, each '*' counted separately, so '**' is two stars) that make the pattern match; `ways` is exact, and `matches` equals `ways > 0`. The boolean question solved with two pointers is Part 3 Q38; here fill the 2D table and show that the boolean and counting tables have the same shape, with `or` becoming `+` (a '*' takes `f[i][j-1]` for zero characters plus `f[i-1][j]` for one more). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every run-length assignment by plain recursion (len(s) <= 7) on small inputs. Example: s='aa', p='a' -> [False, 0]; s='aa', p='*' -> [True, 1]; s='cb', p='?a' -> [False, 0]; s='adceb', p='*a*b' -> [True, 1]; s='', p='**' -> [True, 1]; s='abc', p='a?c' -> [True, 1].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-sequence DP where the pattern symbol decides the move. The boolean table becomes a counting table by turning `or` into `+`. (The two-pointer boolean matcher is Part 3 Q38.)

**Say this first (1 line):** "f[i][j] is the number of ways the first j pattern symbols match the first i letters; a letter or '?' copies f[i-1][j-1] when it fits, and a '*' adds f[i][j-1] (matches nothing) and f[i-1][j] (eats one more letter); matches is just ways > 0."

**Brute force:** Plain recursion over `(i, j)`; at a `*` try every run length `k = 0 .. len(s) - i` and recurse, which enumerates every assignment of run lengths to the stars. Exponential, only for len(s) <= 7. It returns the same `[matches, ways]` pair.

**Optimal:**
- State: `f[i][j]` = number of distinct run-length assignments to the stars among `p[:j]` such that `p[:j]` matches exactly `s[:i]`. (Each `*` is counted separately, so `**` is two stars.)
- Base: `f[0][0] = 1`. Column 0 is 0 for `i > 0` (an empty pattern matches only the empty string). Row 0 follows from the transition: `f[0][j] = f[0][j-1]` if `p[j-1]` is `*`, else 0.
- Transition for symbol `c = p[j-1]`:
  - `c == '*'`: `f[i][j] = f[i][j-1] + f[i-1][j]` (the star takes zero letters; or it takes one more letter, and `f[i-1][j]` already counts the star having taken the others). For `i = 0` only the first term exists.
  - `c == '?'` or `c == s[i-1]`: `f[i][j] = f[i-1][j-1]`.
  - otherwise `0`.
- Boolean vs counting: the boolean table has `f[i][j] = f[i][j-1] or f[i-1][j]` for a star and `f[i-1][j-1]` for a letter. Same shape, same loops; `or` becomes `+`, `and`-with-flag becomes copy. That is why `matches == (ways > 0)`; the code checks it, and also against a regular-expression translation (`*` to `.*`, `?` to `.`).
- Counting is exact (Python integers). With `s = 'a' * n` and `k` stars the count is `C(n + k - 1, k - 1)` (stars and bars); the code checks it. For `s='ab'`, `p='**'` the answer is `[True, 3]`; the prompt's `s=''`, `p='**'` gives one way (both stars take 0).
- Space: row `i` reads row `i-1` only, so two rows (or one row plus one saved diagonal) suffice, O(n).
- Recursion: top-down `go(i, j)` consumes one symbol of `i` or `j` per call, so the depth is up to `m + n`. As observed on Python 3.13 with the default limit 1000: at the prompt's maximum 300 + 300 (depth <= 600) the memoised version runs and agrees; at 700 + 700 (outside the prompt) it raises `RecursionError`. The prompt does not require bottom-up here, but the loops are safer.

**Complexity:** Time O(mn), space O(mn) for the table, O(n) for the two rows. The counts can have many digits (89 digits in the max-size test), so each addition is not strictly O(1); say so. Brute force is exponential in the number of stars.

**Dry run:** `s = 'adceb'`, `p = '*a*b'`. Rows = letters of s used (i), columns = pattern symbols used (j).

| i \ j | 0 | 1 `*` | 2 `a` | 3 `*` | 4 `b` |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | 0 | 0 |
| 1 `a` | 0 | 1 | 1 | 1 | 0 |
| 2 `d` | 0 | 1 | 0 | 1 | 0 |
| 3 `c` | 0 | 1 | 0 | 1 | 0 |
| 4 `e` | 0 | 1 | 0 | 1 | 0 |
| 5 `b` | 0 | 1 | 0 | 1 | 1 |

Cells: `f[0][1]` is a star over zero letters: `f[0][0] = 1`. `f[1][1] = f[1][0] + f[0][1] = 0 + 1 = 1` (the first star eats `a`). `f[1][2]`: `a == a`, copy `f[0][1] = 1`. `f[1][3] = f[1][2] + f[0][3] = 1 + 0 = 1`. `f[2][3] = f[2][2] + f[1][3] = 0 + 1 = 1` (second star eats `d`), and likewise down the column. `f[5][4]`: `b == b`, copy `f[4][3] = 1`. Answer `f[5][4] = 1`, so `[True, 1]`.

**Code:**
```python
import itertools
import random
import re
import sys
from functools import lru_cache
from math import comb

random.seed(1717)

def wildcard_table(s, p):
    """f[i][j] = number of ways the first j pattern symbols match the first i letters of s (each '*' counted separately)."""
    m, n = len(s), len(p)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    f[0][0] = 1
    for i in range(m + 1):
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                # zero characters: f[i][j-1]; one more character (absorbed by this star): f[i-1][j]
                f[i][j] = f[i][j - 1] + (f[i - 1][j] if i else 0)
            elif i and (c == '?' or c == s[i - 1]):
                f[i][j] = f[i - 1][j - 1]
    return f

def wildcard(s, p):
    f = wildcard_table(s, p)
    return [f[-1][-1] > 0, f[-1][-1]]

def wildcard_row(s, p):
    """One row over the pattern. Rows are indexed by i (letters of s used); row[j] holds f[i][j]."""
    m, n = len(s), len(p)
    row = [0] * (n + 1)
    row[0] = 1                                   # i = 0
    for j in range(1, n + 1):
        row[j] = row[j - 1] if p[j - 1] == '*' else 0
    for i in range(1, m + 1):
        new = [0] * (n + 1)
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                new[j] = new[j - 1] + row[j]     # f[i][j-1] + f[i-1][j]
            elif c == '?' or c == s[i - 1]:
                new[j] = row[j - 1]              # f[i-1][j-1]
        row = new
    return [row[n] > 0, row[n]]

def wildcard_bool(s, p):
    """Same shape, 'or' instead of '+'."""
    m, n = len(s), len(p)
    f = [[False] * (n + 1) for _ in range(m + 1)]
    f[0][0] = True
    for i in range(m + 1):
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                f[i][j] = f[i][j - 1] or (i > 0 and f[i - 1][j])
            elif i and (c == '?' or c == s[i - 1]):
                f[i][j] = f[i - 1][j - 1]
    return f[m][n]

def wildcard_memo(s, p):
    @lru_cache(maxsize=None)
    def go(i, j):                                # i letters, j pattern symbols consumed from the FRONT
        if j == len(p): return 1 if i == len(s) else 0
        if p[j] == '*': return go(i, j + 1) + (go(i + 1, j) if i < len(s) else 0)
        return go(i + 1, j + 1) if i < len(s) and p[j] in ('?', s[i]) else 0
    return go(0, 0)

def brute(s, p):
    """Enumerate every run-length assignment to the stars (plain recursion)."""
    def go(i, j):
        if j == len(p): return 1 if i == len(s) else 0
        if p[j] == '*': return sum(go(i + k, j + 1) for k in range(len(s) - i + 1))
        return go(i + 1, j + 1) if i < len(s) and p[j] in ('?', s[i]) else 0
    c = go(0, 0)
    return [c > 0, c]

def as_regex(p):
    return ''.join('.*' if c == '*' else '.' if c == '?' else c for c in p)

for s, p, want in [('aa', 'a', [False, 0]), ('aa', '*', [True, 1]), ('cb', '?a', [False, 0]), ('adceb', '*a*b', [True, 1]), ('', '**', [True, 1]), ('abc', 'a?c', [True, 1])]:
    assert wildcard(s, p) == wildcard_row(s, p) == brute(s, p) == want, (s, p)
    assert wildcard_bool(s, p) == want[0]
print('6 prompt examples ok')

f = wildcard_table('adceb', '*a*b')
print("f for s='adceb' (rows i=0..5 letters used), p='*a*b' (cols j=0..4 symbols used):")
print('      ', ' '.join('-*a*b'))
for i, row in enumerate(f):
    print('  ', '-adceb'[i], row)

pos = 0
for _ in range(1500):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 7)))
    p = ''.join(random.choice('ab?**') for _ in range(random.randint(0, 6)))
    r = wildcard(s, p)
    assert r == brute(s, p) == wildcard_row(s, p) == [wildcard_memo(s, p) > 0, wildcard_memo(s, p)], (s, p)
    assert r[0] == wildcard_bool(s, p) == (r[1] > 0) == (re.fullmatch(as_regex(p), s, re.S) is not None)
    pos += r[0]
print('1500 seeded random (s, p): table == plain recursion == one row == memo; boolean table == (ways > 0) == regex translation; True in', pos, 'of 1500')
assert 0 < pos < 1500

# closed form: s = a^n against k stars has C(n + k - 1, k - 1) assignments
for n_ in range(0, 9):
    for k in range(1, 6):
        assert wildcard('a' * n_, '*' * k)[1] == comb(n_ + k - 1, k - 1)
print('closed form checked: ways(a^n, k stars) == C(n + k - 1, k - 1) for n 0..8, k 1..5')
print("'**' on 'ab' gives", wildcard('ab', '**'), '(three splits: 0|2, 1|1, 2|0)')

print('recursion limit:', sys.getrecursionlimit())
s = 'a' * 300; p = '*a' * 150
r = wildcard(s, p)
print('max size 300 vs 300 symbols (150 stars): ways =', r[1] if r[1] < 10**12 else str(r[1])[:12] + '... (%d digits)' % len(str(r[1])), '| one row agrees:', wildcard_row(s, p) == r)
print('memoised version at 300 + 300 (depth <= 600):', 'agrees' if wildcard_memo(s, p) == r[1] else 'DIFFERS')
rs = ''.join(random.choice('ab') for _ in range(300)); rp = ''.join(random.choice('ab?*') for _ in range(300))
assert wildcard(rs, rp) == wildcard_row(rs, rp)
try:
    wildcard_memo('a' * 700, '*' * 700); print('memoised 700 + 700: ok')
except RecursionError:
    print('memoised 700 + 700 (outside the prompt sizes): RecursionError')

assert wildcard('', '') == [True, 1] and wildcard('a', '') == [False, 0] and wildcard('', 'a') == [False, 0] and wildcard('', '?') == [False, 0]
print('edge asserts ok')
```

**Output (my run):**
```
6 prompt examples ok
f for s='adceb' (rows i=0..5 letters used), p='*a*b' (cols j=0..4 symbols used):
       - * a * b
   - [1, 1, 0, 0, 0]
   a [0, 1, 1, 1, 0]
   d [0, 1, 0, 1, 0]
   c [0, 1, 0, 1, 0]
   e [0, 1, 0, 1, 0]
   b [0, 1, 0, 1, 1]
1500 seeded random (s, p): table == plain recursion == one row == memo; boolean table == (ways > 0) == regex translation; True in 489 of 1500
closed form checked: ways(a^n, k stars) == C(n + k - 1, k - 1) for n 0..8, k 1..5
'**' on 'ab' gives [True, 3] (three splits: 0|2, 1|1, 2|0)
recursion limit: 1000
max size 300 vs 300 symbols (150 stars): ways = 468798513864... (89 digits) | one row agrees: True
memoised version at 300 + 300 (depth <= 600): agrees
memoised 700 + 700 (outside the prompt sizes): RecursionError
edge asserts ok
```

**Edge cases:**
- `s = ''`, `p = ''` returns `[True, 1]`; `s='a'`, `p=''` returns `[False, 0]`; `s=''`, `p='?'` returns `[False, 0]`.
- `s = ''`, `p = '**'` returns `[True, 1]` (each star takes nothing, one assignment).
- `s='ab'`, `p='**'` returns `[True, 3]`: consecutive stars multiply the count.
- `'?'` never matches the empty string.

**Follow-ups:**
- Same for regular expressions with `.` and `*` meaning "zero or more of the previous element"? Different transition: a starred element can repeat or vanish. The shape of the table is the same.
- Count modulo 10^9 + 7 for huge answers? Take the modulus in each cell; exactness is needed only for the question as stated here.
- Collapse repeated stars first? `**` and `*` match the same strings, but the COUNT of assignments differs, which is why the prompt counts them separately.

**Common mistakes:**
- Handling row 0 wrongly (`f[0][j]` is 1 only while the pattern prefix is all stars).
- In the star case, using `f[i-1][j-1]` instead of `f[i-1][j]` (the star can eat more than one letter).
- Treating `matches` as a separate calculation instead of `ways > 0`.
- Memoised recursion at larger sizes than the prompt (`RecursionError` when depth passes the limit).

### Q18 ⭐⭐ 🟡 Minimum ASCII delete sum. `s1` and `s2` are lowercase strings with 0 <= len <= 1000. You may delete letters from either string; deleting a letter costs its ASCII code (a = 97, ..., z = 122). Return the minimum total cost to make the two strings equal. Reduce it to a maximum-weight common subsequence, give the transition, and state the identity `total ASCII - 2 * (best common weight)`. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (len <= 7) on small inputs. Example: s1='sea', s2='eat' -> 231; s1='delete', s2='leet' -> 403; s1='', s2='ab' -> 195; s1='abc', s2='abc' -> 0.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP; deleting letters until the strings are equal means keeping a common subsequence, and the cheapest plan keeps the heaviest one. LCS with weights.

**Say this first (1 line):** "Whatever I keep is a common subsequence, everything else is deleted, so cost = total ASCII of both strings - 2 * (ASCII weight of what I keep); I maximise that weight with the LCS table where a match adds ord(letter) instead of 1."

**Brute force:** Plain recursion `f(i, j)`: if the heads are equal, advance both for free; otherwise delete one head, paying its ASCII code, and try both. Exponential, only for len <= 7. It is the checker (it is the cost recursion itself, not the reduction).

**Optimal:**
- Reduction: the two final equal strings are a common subsequence `t` of `s1` and `s2`. Deleted cost = `(total(s1) - weight(t)) + (total(s2) - weight(t))`. So minimise cost by maximising `weight(t)`.
- State: `w[i][j]` = maximum ASCII weight of a common subsequence of `s1[i:]` and `s2[j:]`.
- Transition: if `s1[i] == s2[j]` then `w[i][j] = ord(s1[i]) + w[i+1][j+1]`; else `max(w[i+1][j], w[i][j+1])`.
- Base cases: `w[n][j] = 0` and `w[i][m] = 0` (empty suffix).
- Answer: `sum(ord) of s1 + sum(ord) of s2 - 2 * w[0][0]`.
- Why weight, not length: the code uses `aaaaazzzz` / `zzzzaaaaa`. The longest common subsequence is `aaaaa` (length 5, weight 485), but `zzzz` (length 4) weighs 488, so the best plan keeps `zzzz`: answer 970, while a length-based shortcut gives 976.
- The direct cost DP (`d[i][j]` = min cost to equalise the suffixes) gives the same numbers; the code checks all three (reduction, direct table, plain recursion).
- Space: two rows (`prev` = row i+1, `cur` = row i). This question needs only the value, so no table is stored.
- Recursion: the top-down version nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two random 300-letter strings work; two disjoint 1000-letter strings (depth 2000) raise `RecursionError`. The prompt allows 1000 each, so the solution is bottom-up. Observation, not a rule: depth depends on the strings.

**Complexity:** Time O(mn) (1,000,000 cells at the maximum; sandbox time well under a few seconds, not a proof), space O(min(m, n)) with two rows if you put the shorter string on the column axis (O(n) for the code as written). Brute force exponential.

**Dry run:** `s1 = 'sea'`, `s2 = 'eat'`. `ord('s') = 115`, `ord('e') = 101`, `ord('a') = 97`, `ord('t') = 116`. Table `w` (rows = suffix of s1, columns = suffix of s2):

| | j=0 `eat` | j=1 `at` | j=2 `t` | j=3 `` |
|---|---|---|---|---|
| i=0 `sea` | 198 | 97 | 0 | 0 |
| i=1 `ea` | 198 | 97 | 0 | 0 |
| i=2 `a` | 97 | 97 | 0 | 0 |
| i=3 `` | 0 | 0 | 0 | 0 |

Cells: `w[2][1]`: `a == a`, so `97 + w[3][2] = 97`. `w[2][0]`: `a != e`, `max(w[3][0] = 0, w[2][1] = 97) = 97`. `w[1][0]`: `e == e`, so `101 + w[2][1] = 198`. `w[0][0]`: `s != e`, `max(w[1][0] = 198, w[0][1] = 97) = 198`. The best kept string is `ea`, weight 198. Total ASCII = `(115 + 101 + 97) + (101 + 97 + 116) = 313 + 314 = 627`. Answer `627 - 2 * 198 = 231` (delete `s` = 115 and `t` = 116).

**Code:**
```python
import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1818)

def weight_table(s1, s2):
    """w[i][j] = maximum total ASCII weight of a common subsequence of s1[i:] and s2[j:]."""
    n, m = len(s1), len(s2)
    w = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s1[i] == s2[j]:
                w[i][j] = ord(s1[i]) + w[i + 1][j + 1]
            else:
                w[i][j] = max(w[i + 1][j], w[i][j + 1])
    return w

def min_delete_sum(s1, s2):
    """total ASCII of both strings - 2 * (best common weight). Two rows."""
    n, m = len(s1), len(s2)
    prev = [0] * (m + 1)
    for i in range(n - 1, -1, -1):
        cur = [0] * (m + 1)
        for j in range(m - 1, -1, -1):
            if s1[i] == s2[j]:
                cur[j] = ord(s1[i]) + prev[j + 1]
            else:
                cur[j] = max(prev[j], cur[j + 1])
        prev = cur
    return sum(map(ord, s1)) + sum(map(ord, s2)) - 2 * prev[0]

def direct_delete_table(s1, s2):
    """The cost DP itself (no reduction): d[i][j] = min cost to make s1[i:] and s2[j:] equal."""
    n, m = len(s1), len(s2)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n: d[i][j] = sum(map(ord, s2[j:]))
            elif j == m: d[i][j] = sum(map(ord, s1[i:]))
            elif s1[i] == s2[j]: d[i][j] = d[i + 1][j + 1]
            else: d[i][j] = min(ord(s1[i]) + d[i + 1][j], ord(s2[j]) + d[i][j + 1])
    return d

def min_delete_memo(s1, s2):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(s1): return sum(map(ord, s2[j:]))
        if j == len(s2): return sum(map(ord, s1[i:]))
        if s1[i] == s2[j]: return f(i + 1, j + 1)
        return min(ord(s1[i]) + f(i + 1, j), ord(s2[j]) + f(i, j + 1))
    return f(0, 0)

def brute(s1, s2):
    """Plain recursion, no memo (len <= 7)."""
    def f(i, j):
        if i == len(s1): return sum(map(ord, s2[j:]))
        if j == len(s2): return sum(map(ord, s1[i:]))
        if s1[i] == s2[j]: return f(i + 1, j + 1)
        return min(ord(s1[i]) + f(i + 1, j), ord(s2[j]) + f(i, j + 1))
    return f(0, 0)

for a, b, want in [('sea', 'eat', 231), ('delete', 'leet', 403), ('', 'ab', 195), ('abc', 'abc', 0)]:
    assert min_delete_sum(a, b) == brute(a, b) == min_delete_memo(a, b) == direct_delete_table(a, b)[0][0] == want, (a, b)
print('4 prompt examples ok')

w = weight_table('sea', 'eat')
print("w (best common ASCII weight of s1[i:], s2[j:]) for s1='sea' (rows), s2='eat' (cols j=0..3):")
for i, row in enumerate(w):
    print(' ', 'sea-'[i], row)
tot = sum(map(ord, 'sea')) + sum(map(ord, 'eat'))
print('total ASCII =', tot, '| best common weight =', w[0][0], '| answer =', tot, '-', 2, '*', w[0][0], '=', tot - 2 * w[0][0])

for _ in range(1000):
    a = ''.join(random.choice('abcz') for _ in range(random.randint(0, 7)))
    b = ''.join(random.choice('abcz') for _ in range(random.randint(0, 7)))
    r = min_delete_sum(a, b)
    assert r == brute(a, b) == min_delete_memo(a, b) == direct_delete_table(a, b)[0][0], (a, b)
    assert r == sum(map(ord, a)) + sum(map(ord, b)) - 2 * weight_table(a, b)[0][0]
print('1000 seeded random pairs (len 0..7, alphabet abcz): two-row identity == plain recursion == memo == direct cost table')

cnt = 0
words = [''.join(x) for n in range(5) for x in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert min_delete_sum(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# why weight and not length: with lowercase letters a LONGER common subsequence can weigh LESS (5 x 'a' = 485 < 4 x 'z' = 488)
a, b = 'aaaaazzzz', 'zzzzaaaaa'
tot = sum(map(ord, a)) + sum(map(ord, b))
print("s1='aaaaazzzz', s2='zzzzaaaaa': longest common is 'aaaaa' (len 5, weight 485); best weight keeps 'zzzz' (len 4, weight 488)")
print('  answer by weight:', min_delete_sum(a, b), '== plain recursion', brute(a, b), '| a length-based shortcut would say', tot - 2 * 485)
assert min_delete_sum(a, b) == tot - 2 * 488 < tot - 2 * 485

print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcdefghij') for _ in range(1000)); y = ''.join(random.choice('abcdefghij') for _ in range(1000))
t = time.perf_counter(); r = min_delete_sum(x, y); dt = time.perf_counter() - t
assert r == sum(map(ord, x)) + sum(map(ord, y)) - 2 * weight_table(x, y)[0][0]
print('bottom-up 1000 x 1000 random:', r, '| sandbox time under 5 s:', dt < 5)
print('bottom-up disjoint 1000 + 1000 ->', min_delete_sum('a' * 1000, 'b' * 1000), '(= 97000 + 98000)')
print('memoised, two random 300-letter strings agrees:', min_delete_memo(x[:300], y[:300]) == min_delete_sum(x[:300], y[:300]))
try:
    min_delete_memo('a' * 1000, 'b' * 1000); print('memoised disjoint 1000 + 1000: ok')
except RecursionError:
    print('memoised disjoint 1000 + 1000: RecursionError')

assert min_delete_sum('', '') == 0 and min_delete_sum('a', 'a') == 0 and min_delete_sum('a', 'b') == 195 and min_delete_sum('z', '') == 122
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
w (best common ASCII weight of s1[i:], s2[j:]) for s1='sea' (rows), s2='eat' (cols j=0..3):
  s [198, 97, 0, 0]
  e [198, 97, 0, 0]
  a [97, 97, 0, 0]
  - [0, 0, 0, 0]
total ASCII = 627 | best common weight = 198 | answer = 627 - 2 * 198 = 231
1000 seeded random pairs (len 0..7, alphabet abcz): two-row identity == plain recursion == memo == direct cost table
exhaustive pairs over {a,b}, len <= 4: 961 ok
s1='aaaaazzzz', s2='zzzzaaaaa': longest common is 'aaaaa' (len 5, weight 485); best weight keeps 'zzzz' (len 4, weight 488)
  answer by weight: 970 == plain recursion 970 | a length-based shortcut would say 976
recursion limit: 1000
bottom-up 1000 x 1000 random: 107150 | sandbox time under 5 s: True
bottom-up disjoint 1000 + 1000 -> 195000 (= 97000 + 98000)
memoised, two random 300-letter strings agrees: True
memoised disjoint 1000 + 1000: RecursionError
edge asserts ok
```

**Edge cases:**
- Both empty returns 0; identical strings return 0.
- One empty: the answer is the total ASCII of the other (`''`, `'ab'` gives 195).
- No common letter: the answer is the total of both strings (disjoint 1000 + 1000 gives 195000).
- A longer common subsequence is not always the better one (see the `a`/`z` example).

**Follow-ups:**
- Minimum number of deletions (not weighted)? `m + n - 2 * LCS`, same table with weight 1.
- Return the strings that remain? Keep the table and walk forward like Q10, choosing the tie rule you state.
- Why is the identity `total - 2 * best`? Every kept letter is counted once in each string and is never deleted from either.

**Common mistakes:**
- Counting kept letters by length (LCS) instead of by weight.
- Subtracting the weight once instead of twice.
- Memoised recursion at 1000 x 1000 (`RecursionError`).
- Wrong base case: when one string is empty, the other's whole tail must be paid (its ASCII sum), not zero.

### Q19 ⭐⭐ 🔴 Palindrome partitioning II: minimum cuts. `s` is a lowercase string with 1 <= len <= 2000. Cut it into pieces so that every piece is a palindrome; return the minimum number of cuts (0 if `s` is already a palindrome). Build a boolean table `pal[l][r]` in O(n^2) (by expanding around every center, or by the interval recurrence), then run a 1D DP `cuts[r] = 0 if pal[0][r] else min(cuts[l-1] + 1 over l with pal[l][r])`, and state the total time and space. A 2000 x 2000 table of Python booleans is large; say how much memory it needs roughly and one way to avoid it. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over all cut positions (len <= 10) on small inputs. Example: s='aab' -> 1; s='a' -> 0; s='ab' -> 1; s='aaaa' -> 0; s='abcbm' -> 2.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2020 on-campus Naukri Code360 report with a longest palindromic substring solved by a 2-D boolean DP table, a 2024 off-campus SDE-1 LeetCode Discuss report with a 2D DP array-splitting question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Two DPs stacked. An interval table (`pal[l][r]` = is `s[l..r]` a palindrome) feeds a 1D prefix DP (`cuts[r]`). Partition DP: the last piece is a palindrome `s[l..r]`, the rest is a smaller prefix.

**Say this first (1 line):** "First I make palindrome lookups O(1) with an O(n^2) table by expanding around every centre. Then `cuts[r]` is zero if the whole prefix is a palindrome, otherwise one more than the best prefix that ends just before the last palindromic piece."

**Brute force:** Recursion over all cut positions: `f(i)` = fewest cuts for `s[i:]`, try every `j` where `s[i:j]` is a palindrome, take `1 + f(j)`. Without a memo it can try up to 2^(n-1) partitions (every letter equal is the worst case). With a memo it is O(n^2) states times an O(n) palindrome check, so O(n^3). That is the oracle (len <= 10), not the answer.

**Optimal:**
- Table. `pal[l][r]` is true when `s[l] == s[r]` and the inside `pal[l+1][r-1]` is true (or the inside is empty or one letter). Expanding around each of the 2n-1 centres fills exactly the true cells: from `(l, r)` move out while the two ends match. Each true cell is touched once, each centre stops at its first mismatch, so the total is O(n^2) (worst case all letters equal).
- State: `cuts[r]` = fewest cuts for the prefix `s[0..r]` (r is the last index).
- Transition: if `pal[0][r]` then `cuts[r] = 0`. Otherwise the last piece is `s[l..r]` with `l >= 1` and `pal[l][r]` true, and the prefix before it is `s[0..l-1]`, so `cuts[r] = min(cuts[l-1] + 1)` over those `l`. The `+1` is the cut between the prefix and the last piece.
- Base: `cuts[0] = 0` (one letter is a palindrome). Answer `cuts[n-1]`. `l = r` is always valid, so the `min` is never empty.
- Time O(n^2), space O(n^2) for the table. 
- Memory at n = 2000: a list of lists holds 4,000,000 pointers at 8 bytes, about 32 MB (printed below; `True` and `False` are shared singletons, so the cost is the pointers, not the booleans). Ways out: (1) `bytearray` rows, about 4 MB; (2) triangle only, about 2 MB; (3) no table at all: while expanding around a centre, every palindrome `s[l..r]` found is a candidate last piece, so relax `cuts[r+1] = min(cuts[r+1], cuts[l] + 1)` on the spot (prefix-length indexing, `cuts[0] = -1`). That is O(n) extra space and the same O(n^2) time. The code has both versions and they agree.

**Complexity:** Time O(n^2): table O(n^2) (or relaxation during the expansion), then the `cuts` loop is O(n) per `r`, so O(n^2) again. Space O(n^2) with the table, O(n) with the relax-while-expanding version. Python's `min` over a generator makes the second loop the slow part for n = 2000 but still well inside a second.

**Dry run:** `s = 'aab'`.
- Table (`T` true, rows `l`, columns `r`): `l=0: T T F`, `l=1: . T F`, `l=2: . . T`. So `'aa'` is a palindrome and `'aab'`, `'ab'` are not.
- `r=0`: `pal[0][0]` true, `cuts[0] = 0`.
- `r=1`: `pal[0][1]` (`'aa'`) true, `cuts[1] = 0`.
- `r=2`: `pal[0][2]` false. Candidates `l` in 1..2 with `pal[l][2]` true: only `l=2` (`'b'`). `cuts[2] = cuts[1] + 1 = 1`.
- Answer 1: `aa | b`.

**Code:**
```python
import random, sys
from functools import lru_cache

random.seed(19)

def min_cuts(s):
    """Palindrome table by expanding around every centre, then cuts[r] over l with pal[l][r]."""
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):          # odd and even centres
            while l >= 0 and r < n and s[l] == s[r]:
                pal[l][r] = True
                l -= 1
                r += 1
    cuts = [0] * n                                    # cuts[r] = min cuts for s[0..r]
    for r in range(n):
        if pal[0][r]:
            cuts[r] = 0
        else:
            cuts[r] = min(cuts[l - 1] + 1 for l in range(1, r + 1) if pal[l][r])
    return cuts[-1]

def min_cuts_light(s):
    """O(n) extra space: no table. cuts[] is relaxed forward from every palindrome found while expanding."""
    n = len(s)
    cuts = list(range(-1, n))                         # cuts[k] = best cuts for the prefix of length k (cuts[0] = -1 sentinel)
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):
            while l >= 0 and r < n and s[l] == s[r]:
                # s[l..r] is a palindrome: the prefix of length r+1 can end with this piece
                if cuts[l] + 1 < cuts[r + 1]:
                    cuts[r + 1] = cuts[l] + 1
                l -= 1
                r += 1
    return cuts[n]

def brute(s):
    """Plain recursion over all cut positions: f(i) = fewest cuts for s[i:]."""
    def f(i):
        if i == len(s):
            return -1                                  # no piece left: the cut after the last piece is not made
        return min(1 + f(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return f(0)

# examples
for s, exp in [('aab', 1), ('a', 0), ('ab', 1), ('aaaa', 0), ('abcbm', 2)]:
    a, b, c = min_cuts(s), min_cuts_light(s), brute(s)
    assert a == b == c == exp, (s, a, b, c)
    print('example', repr(s), '->', a)

# hand table for 'aab'
s = 'aab'; n = len(s)
pal = [[s[l:r + 1] == s[l:r + 1][::-1] if l <= r else None for r in range(n)] for l in range(n)]
print('pal table for aab (rows l, cols r; None below diagonal):')
for l in range(n):
    print('  l=%d' % l, [('T' if v else 'F') if v is not None else '.' for v in pal[l]])
cuts = []
for r in range(n):
    if pal[0][r]:
        cuts.append(0); print('  r=%d pal[0][%d] is True -> cuts=0' % (r, r))
    else:
        cands = [(l, cuts[l - 1] + 1) for l in range(1, r + 1) if pal[l][r]]
        cuts.append(min(v for _, v in cands)); print('  r=%d candidates (l, cuts[l-1]+1) %s -> cuts=%d' % (r, cands, cuts[-1]))
print('cuts =', cuts)

# seeded cross-check: len <= 10, small alphabets so palindromes occur
cases = 0; hist = {}
for _ in range(600):
    alpha = random.choice(['ab', 'abc', 'a', 'abcd'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(1, 10)))
    exp = brute(s)
    assert min_cuts(s) == min_cuts_light(s) == exp, s
    cases += 1; hist[exp] = hist.get(exp, 0) + 1
print('cross-check cases', cases, '| answer histogram', dict(sorted(hist.items())))
# exhaustive over all binary strings up to length 10
cnt = 0
for L in range(1, 11):
    for bits in range(1 << L):
        s = format(bits, '0%db' % L)
        assert min_cuts(s) == min_cuts_light(s) == brute(s); cnt += 1
print('exhaustive binary strings len 1..10:', cnt)

# edge cases
assert min_cuts('a' * 2000) == 0
assert min_cuts('ab' * 50) == 1 == min_cuts_light('ab' * 50)   # 'a' + 'bab...ab' (the rest is a palindrome)
assert min_cuts('abcdefghij' * 5) == 49     # no palindrome longer than 1: every letter is its own piece
assert min_cuts_light('abcdefghij' * 5) == 49
assert min_cuts('a') == 0 == min_cuts_light('a')
print('edge asserts passed')

# memory of the table at n = 2000
n = 2000
tbl = [[False] * n for _ in range(n)]
outer = sys.getsizeof(tbl); rows = sum(sys.getsizeof(r) for r in tbl)
print('list-of-lists 2000x2000: rows', rows, 'bytes + outer', outer, '= about %.1f MB' % ((rows + outer) / 1e6))
tb = [bytearray(n) for _ in range(n)]
print('list of bytearrays 2000x2000: about %.1f MB' % ((sum(sys.getsizeof(r) for r in tb) + sys.getsizeof(tb)) / 1e6))
tri = [bytearray(n - l) for l in range(n)]
print('upper triangle only (l <= r): about %.1f MB' % (sum(sys.getsizeof(r) for r in tri) / 1e6))
import time
t0 = time.perf_counter(); r1 = min_cuts('ab' * 1000); t1 = time.perf_counter(); r2 = min_cuts_light('ab' * 1000); t2 = time.perf_counter()
print('n=2000 "ab"*1000 (sandbox timing): table version', r1, round(t1 - t0, 2), 's; light version', r2, round(t2 - t1, 2), 's')
import random as _r
_r.seed(5); w = ''.join(_r.choice('ab') for _ in range(2000))
t0 = time.perf_counter(); r1 = min_cuts(w); t1 = time.perf_counter(); r2 = min_cuts_light(w); t2 = time.perf_counter()
assert r1 == r2
print('n=2000 random binary (sandbox timing):', r1, round(t1 - t0, 2), 's;', round(t2 - t1, 2), 's')

# recursion: a memoised f(i) on a string with no palindrome longer than 1 nests n deep (observed on this Python, default limit)
def memo_cuts(s):
    @lru_cache(maxsize=None)
    def f(i):
        if i == len(s):
            return -1
        return min(1 + f(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return f(0)
print('recursion limit', sys.getrecursionlimit())
for n in (300, 2000):
    w = ('abc' * n)[:n]
    try:
        print('memoised recursion, n =', n, '->', memo_cuts(w), '(bottom-up gives', min_cuts_light(w), ')')
    except RecursionError:
        print('memoised recursion, n =', n, '-> RecursionError (bottom-up gives', min_cuts_light(w), ')')
```

**Output (my run):**
```
example 'aab' -> 1
example 'a' -> 0
example 'ab' -> 1
example 'aaaa' -> 0
example 'abcbm' -> 2
pal table for aab (rows l, cols r; None below diagonal):
  l=0 ['T', 'T', 'F']
  l=1 ['.', 'T', 'F']
  l=2 ['.', '.', 'T']
  r=0 pal[0][0] is True -> cuts=0
  r=1 pal[0][1] is True -> cuts=0
  r=2 candidates (l, cuts[l-1]+1) [(2, 1)] -> cuts=1
cuts = [0, 0, 1]
cross-check cases 600 | answer histogram {0: 226, 1: 162, 2: 106, 3: 53, 4: 25, 5: 18, 6: 6, 7: 4}
exhaustive binary strings len 1..10: 2046
edge asserts passed
list-of-lists 2000x2000: rows 32112000 bytes + outer 16184 = about 32.1 MB
list of bytearrays 2000x2000: about 4.1 MB
upper triangle only (l <= r): about 2.1 MB
n=2000 "ab"*1000 (sandbox timing): table version 1 0.24 s; light version 1 0.1 s
n=2000 random binary (sandbox timing): 320 0.17 s; 0.0 s
recursion limit 1000
memoised recursion, n = 300 -> 299 (bottom-up gives 299 )
memoised recursion, n = 2000 -> RecursionError (bottom-up gives 1999 )
```

Reading the output:
- All five examples match the table version, the light version and the plain recursion.
- 600 seeded random strings (len <= 10, alphabets of 1 to 4 letters) and all 2046 binary strings of length 1 to 10 agree across the three solutions. The histogram shows answers from 0 to 7 occurred, so both the "already a palindrome" branch and long chains of cuts were tested.
- Memory: a 2000 x 2000 list of lists is about 32 MB, `bytearray` rows about 4 MB, the triangle about 2 MB. Timings are sandbox-only.
- Recursion: the memoised top-down recursion on a 300-letter string with no palindrome longer than one letter works (depth about 300), and on 2000 letters it raises `RecursionError` at the default limit of 1000 (observation on Python 3.13, not a rule for every call path). The bottom-up code has no such limit.

**Edge cases:**
- `len(s) == 1`: 0 cuts.
- Whole string a palindrome: 0 (that is the `pal[0][r]` branch; without it the code would return at least 1 for a palindrome of length 2 or more, and crash on a single letter, because `l` starts at 1).
- All letters distinct (or no palindrome longer than 1): `n - 1`, every letter alone.
- Even-length centres (`(c, c+1)`) are easy to forget: without them `'aa'` and `'aaaa'` break.
- n = 2000 all equal: table fill is the worst case (about 2 million true cells), still fine.

**Follow-ups:**
- "Return the actual pieces?" Store `prev[r] = l` for the chosen minimum and walk back from `n-1`. Any tie rule must be stated; the count is unique, the partition is not.
- "Can you do it without the O(n^2) table?" Yes, the relax-while-expanding version above: O(n) extra space, same O(n^2) time.
- "Palindrome partitioning that lists all partitions?" That is enumeration, a backtracking problem (Part 12); the number of results can be exponential.

**Common mistakes:**
- Counting pieces instead of cuts (off by one: pieces = cuts + 1).
- Skipping even-length centres.
- Using `cuts[l]` instead of `cuts[l-1]` in the table version (the prefix ends at `l-1`).
- Building `pal` with `[[False]*n]*n` (all rows alias, see Part 10 Q31) or recomputing `s[l:r+1] == s[l:r+1][::-1]` inside the DP (O(n^3)).
- Plain recursion with no memo at n = 2000: exponential time; memoised recursion: `RecursionError`.

### Q20 ⭐⭐ 🔴 Dungeon game. `grid` is an m x n list of lists (1 <= m, n <= 200) of integers in -1000..1000: a negative cell costs health when entered, a positive cell gives health, and the start and end cells are included. A knight starts at the top-left with some positive integer health and moves only right or down to the bottom-right. His health must be at least 1 after every cell (including the first and the last). Return the smallest initial health that makes some path survive. Explain why the table must be filled from the bottom-right corner backwards (a forward DP on 'best sum so far' is not enough: give a small counter-example), give `need[i][j] = max(1, min(need[i+1][j], need[i][j+1]) - grid[i][j])` and its base case, and use one row. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) and computing the needed health for each on small inputs. Example: grid=[[-2, -3, 3], [-5, -10, 1], [10, 30, -5]] -> 7; grid=[[0]] -> 1; grid=[[100]] -> 1; grid=[[1, -3, 3], [0, -2, 0], [-3, -3, -3]] -> 3; grid=[[-5]] -> 6.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP, but backwards. The quantity "health I need when I stand here" depends only on what lies ahead, so the table is filled from the goal to the start.

**Say this first (1 line):** "Forward DP on 'best sum so far' fails because the best sum and the lowest dip are two different things. So I go backwards: `need[i][j]` is the minimum health I must have when I ENTER this cell, and it only depends on the cells after it."

**Brute force:** Enumerate all `C(m+n-2, m-1)` right/down paths. For each path walk it, track the running sum, and the needed health is `max(1, 1 - lowest prefix sum)`. Answer is the minimum over paths. Exponential; used as the oracle for m, n <= 5.

**Optimal:**
- State: `need[i][j]` = smallest health on entering `(i, j)` (before the cell's effect) that lets the knight reach the end alive.
- Transition: from `(i, j)` he goes to the cheaper of the two next cells, so he must leave with at least `min(need[i+1][j], need[i][j+1])`. His health after the cell is `h + grid[i][j]`, so `h >= nxt - grid[i][j]`. Health must also be at least 1 after the cell, and `nxt >= 1` already guarantees that on the way out; the outer `max(1, ...)` guarantees at least 1 on entering (this is what protects the first cell). So `need[i][j] = max(1, min(need[i+1][j], need[i][j+1]) - grid[i][j])`.
- Base: the end cell has `nxt = 1` (after the last cell he needs 1), so `need[m-1][n-1] = max(1, 1 - grid[m-1][n-1])`. Missing neighbours on the last row or column count as infinity.
- Why not forward: a forward DP wants one number per cell, "best sum so far". But a path with a bigger total can have dipped lower on the way (it needs a bigger starting health), and a path with a smaller total may never have dipped. Two paths to a cell are compared by (sum, lowest dip), which is not a total order. Backwards, the future is summarised by ONE number (health required), and smaller is always better. Counter-example in the code: `[[-3,-3,2],[-2,0,3]]`; the path with the largest total (-1, going right, right, down) needs 7, but the path down, right, right (total -2) needs only 6.
- One row: `need[j]` holds row `i+1` until it is overwritten with row `i`. Loop `i` from the bottom, `j` from the right. Then `need[j]` (not yet overwritten) is the cell below, and `need[j+1]` (already overwritten) is the cell to the right. The answer is `need[0]`.

**Complexity:** Time O(m * n). Space O(n) with one row (O(m * n) with the full table).

**Dry run:** `grid = [[-2,-3,3],[-5,-10,1],[10,30,-5]]`, filled from the bottom right.
- `(2,2)`: grid -5, nxt 1, need `max(1, 1+5) = 6`.
- `(2,1)`: grid 30, next is `(2,2)` need 6, `6 - 30 < 1` so 1. `(2,0)`: grid 10, next need 1, so 1. Bottom row `[1, 1, 6]`.
- Row 1: `(1,2)`: grid 1, below 6, `6 - 1 = 5`. `(1,1)`: grid -10, `min(below 1, right 5) = 1`, `1 + 10 = 11`. `(1,0)`: grid -5, `min(below 1, right 11) = 1`, `1 + 5 = 6`. Row `[6, 11, 5]`.
- Row 0: `(0,2)`: grid 3, below 5, `5 - 3 = 2`. `(0,1)`: grid -3, `min(below 11, right 2) = 2`, `2 + 3 = 5`. `(0,0)`: grid -2, `min(below 6, right 5) = 5`, `5 + 2 = 7`. Row `[7, 5, 2]`.
- Answer 7: follow right, right, down, down with health 7: after the cells 5, 2, 5, 6, 1. Never below 1, and 6 would end at 0.

**Code:**
```python
import random, itertools

random.seed(20)
INF = float('inf')

def dungeon(grid):
    """need[j] holds the row below until overwritten by row i. Filled from the bottom-right corner backwards."""
    m, n = len(grid), len(grid[0])
    need = [INF] * (n + 1)                      # need[n] is a sentinel to the right of the last column
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                nxt = 1                          # base: after the last cell health must be >= 1
            else:
                nxt = min(need[j] if i < m - 1 else INF,   # need[j] is still row i+1 (down)
                          need[j + 1] if j < n - 1 else INF)  # need[j+1] is already row i (right)
            need[j] = max(1, nxt - grid[i][j])
    return need[0]

def need_for_path(grid, moves):
    """Health needed to survive one fixed path: 1 - lowest prefix sum, at least 1."""
    i = j = 0; tot = grid[0][0]; low = tot
    for c in moves:
        if c == 'D': i += 1
        else: j += 1
        tot += grid[i][j]; low = min(low, tot)
    return max(1, 1 - low), tot

def all_paths(m, n):
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        yield s

def brute(grid):
    m, n = len(grid), len(grid[0])
    return min(need_for_path(grid, s)[0] for s in all_paths(m, n))

def forward_max_sum_wrong(grid):
    """The tempting forward DP: take the path with the largest total, then price that one path."""
    m, n = len(grid), len(grid[0]); best = None
    for s in all_paths(m, n):
        h, tot = need_for_path(grid, s)
        if best is None or tot > best[1]: best = (h, tot)
    return best[0]

# examples
for g, exp in [([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]], 7), ([[0]], 1), ([[100]], 1),
               ([[1, -3, 3], [0, -2, 0], [-3, -3, -3]], 3), ([[-5]], 6)]:
    a, b = dungeon(g), brute(g)
    assert a == b == exp, (g, a, b)
    print('example', g, '->', a)

# hand table for example 1 (full 2D version, printed)
g = [[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]
m, n = 3, 3
T = [[0] * n for _ in range(m)]
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
        if i == m - 1 and j == n - 1: nxt = 1
        else: nxt = min(T[i + 1][j] if i < m - 1 else INF, T[i][j + 1] if j < n - 1 else INF)
        T[i][j] = max(1, nxt - g[i][j])
print('need table (full 2D) for example 1:')
for row in T: print('  ', row)
assert T[0][0] == dungeon(g)

# counter-example to the forward 'best sum so far' DP
cx = [[-3, -3, 2], [-2, 0, 3]]
print('counter-example grid', cx, ': optimum', dungeon(cx), '| path with largest sum needs', forward_max_sum_wrong(cx))
assert dungeon(cx) == brute(cx) == 6 and forward_max_sum_wrong(cx) == 7
for s in all_paths(2, 3):
    print('   moves', ''.join(s), '-> (health needed, total sum) =', need_for_path(cx, s))

# seeded random cross-check, m, n <= 5
wrong = 0; cases = 0
for _ in range(500):
    m, n = random.randint(1, 5), random.randint(1, 5)
    g = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
    assert dungeon(g) == brute(g), g
    wrong += forward_max_sum_wrong(g) != brute(g)
    cases += 1
print('cross-check cases', cases, '| max-sum path was NOT optimal on', wrong)
# all 2 x 3 grids with values in -2..2
cnt = 0
for vals in itertools.product(range(-2, 3), repeat=6):
    g = [list(vals[:3]), list(vals[3:])]
    assert dungeon(g) == brute(g); cnt += 1
print('exhaustive 2 x 3 grids, values -2..2:', cnt)

# edge cases and max size
assert dungeon([[0]]) == 1 and dungeon([[100]]) == 1 and dungeon([[-5]]) == 6
assert dungeon([[-1000] * 200 for _ in range(200)]) == 1000 * 399 + 1   # 399 cells of -1000 (start included) -> 399000 + 1
print('200 x 200 all -1000 ->', dungeon([[-1000] * 200 for _ in range(200)]))
big = [[random.randint(-1000, 1000) for _ in range(200)] for _ in range(200)]
print('200 x 200 random ->', dungeon(big))
print('edge asserts passed')

# memoised top-down version: depth is at most m + n - 1 frames, so 200 x 200 (399 deep) is below the default limit of 1000
import sys
from functools import lru_cache
def dungeon_memo(grid):
    m, n = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == m - 1 and j == n - 1: nxt = 1
        else: nxt = min(f(i + 1, j) if i + 1 < m else INF, f(i, j + 1) if j + 1 < n else INF)
        return max(1, nxt - grid[i][j])
    return f(0, 0)
print('recursion limit', sys.getrecursionlimit(), '| memoised 200 x 200 equals bottom-up:', dungeon_memo(big) == dungeon(big))
g1 = [[-1] * 200 for _ in range(200)]
assert dungeon_memo(g1) == dungeon(g1)
print('memoised on 200 x 200 all -1:', dungeon_memo(g1))
```

**Output (my run):**
```
example [[-2, -3, 3], [-5, -10, 1], [10, 30, -5]] -> 7
example [[0]] -> 1
example [[100]] -> 1
example [[1, -3, 3], [0, -2, 0], [-3, -3, -3]] -> 3
example [[-5]] -> 6
need table (full 2D) for example 1:
   [7, 5, 2]
   [6, 11, 5]
   [1, 1, 6]
counter-example grid [[-3, -3, 2], [-2, 0, 3]] : optimum 6 | path with largest sum needs 7
   moves DRR -> (health needed, total sum) = (6, -2)
   moves RDR -> (health needed, total sum) = (7, -3)
   moves RRD -> (health needed, total sum) = (7, -1)
cross-check cases 500 | max-sum path was NOT optimal on 15
exhaustive 2 x 3 grids, values -2..2: 15625
200 x 200 all -1000 -> 399001
200 x 200 random -> 1
edge asserts passed
recursion limit 1000 | memoised 200 x 200 equals bottom-up: True
memoised on 200 x 200 all -1: 400
```

Reading the output:
- All five examples match the one-row DP and the path enumeration. The printed full table is the one in the dry run.
- The counter-example is real: the path with the largest sum needs 7, the optimum is 6. On 500 seeded random grids (m, n <= 5, values -10..10) the one-row DP equals the enumeration every time, and the largest-sum path was not optimal on 15 of them. So the failure of forward "best sum" is not a corner case, but it is not frequent on these random grids either.
- All 15,625 grids of shape 2 x 3 with values -2..2 agree.
- 200 x 200 runs instantly (sandbox, not a proof of big-O). A memoised top-down version nests at most m + n - 1 = 399 deep on 200 x 200, so it also runs at the default limit (printed); a much larger grid would not, which is why bottom-up is the safe default.

**Edge cases:**
- `[[100]]` is 1, not negative: the `max(1, ...)` clamp is the whole point.
- `[[-5]]` is 6 (needs 6 so that 6 - 5 = 1).
- Start or end cell may be negative; both are included.
- First row or column: the missing neighbour is infinity, not 0.
- Worst case values: all -1000 on 200 x 200 gives 399,001, because every path has 200 + 200 - 1 = 399 cells.

**Follow-ups:**
- "Why is greedy 'go to the bigger neighbour' wrong?" It ignores the future; the DP compares the true future requirement.
- "Can you move in four directions?" Then the grid is not a DAG and you need a shortest-path style search (binary search on health plus BFS, or Dijkstra on 'minimum health needed').
- "Print the path?" Walk forward from `(0,0)`, always stepping to the neighbour with the smaller `need`. That needs the full table, not one row.

**Common mistakes:**
- Forgetting `max(1, ...)` (answer 0 or negative).
- Filling top-left to bottom-right.
- Treating the end cell as a plain cell with no base (it needs `1 - grid`, clamped).
- Treating out-of-grid neighbours as 0 instead of infinity, which lets the knight "exit" early.
- Updating the one-row array left to right (then `need[j-1]`, not `need[j+1]`, is already overwritten).

### Q21 ⭐⭐ 🔴 Distinct subsequences (counting). `s` has 0 <= len <= 1000 and `t` has 0 <= len <= 500 lowercase letters. Return the exact number of ways to choose positions in `s` (increasing indices, so equal letters at different positions count separately) that spell `t`; the empty `t` has exactly 1 way. Define `dp[i][j]` = ways for the first i letters of s and the first j of t, give the transition (always add the ways that skip s[i-1], and add the ways that use it when it equals t[j-1]), and then use one row; say which direction the inner loop over j must run and why. Python integers do not overflow, but say where you would insert `% (10**9 + 7)` if a modulus were required and why the counting DP uses addition only. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every index combination (len(s) <= 10) on small inputs. Example: s='rabbbit', t='rabbit' -> 3; s='babgbag', t='bag' -> 5; s='abc', t='' -> 1; s='a', t='aa' -> 0; s='aaaa', t='aa' -> 6.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string counting DP. Prefix-by-prefix table over `(i, j)`: how many ways do the first `i` letters of `s` produce the first `j` letters of `t`. Counting, so addition only, no `max`.

**Say this first (1 line):** "`dp[i][j]` always includes the ways that skip `s[i-1]`, and adds the ways that use it when it equals `t[j-1]`. Row `i` only needs row `i-1`, so I keep one row and run `j` downwards."

**Brute force:** Try every choice of `len(t)` increasing positions in `s` (`itertools.combinations`) and count those that spell `t`. That is `C(len(s), len(t))` choices, exponential. A memoised recursion `f(i, j)` is polynomial (O(len(s) * len(t)) states) but nests about `len(s)` deep. Brute force is the oracle for `len(s) <= 10`.

**Optimal:**
- State: `dp[i][j]` = number of index sequences inside `s[:i]` that spell `t[:j]`.
- Transition: look at the last available letter `s[i-1]`. Either it is not used: `dp[i-1][j]` ways. Or it is used as the final letter of `t[:j]`, which needs `s[i-1] == t[j-1]`, and then the rest `t[:j-1]` is spelled inside `s[:i-1]`: `dp[i-1][j-1]` ways. The two cases are disjoint (used or not), so add: `dp[i][j] = dp[i-1][j] + (dp[i-1][j-1] if s[i-1] == t[j-1])`.
- Base: `dp[i][0] = 1` for every `i` (empty `t`: choose nothing, one way, even for empty `s`); `dp[0][j] = 0` for `j >= 1`.
- One row: `dp[j]` plays `dp[i-1][j]` until updated, and the update reads `dp[j-1]` from the PREVIOUS row. So `j` must run from `len(t)` down to 1. Run it ascending and `dp[j-1]` is already the new row, so `s[i-1]` gets used twice (for `t[j-2]` and `t[j-1]` in the same pass). The code shows this: `s='aaaa', t='aa'` gives 10 instead of 6, and the ascending loop was wrong on 93 of 300 random cases.
- Modulus: if the problem asked for `% (10**9 + 7)`, write `dp[j] = (dp[j] + dp[j-1]) % MOD` at the one place where two counts are added. The count is built only from additions of non-negative counts, so reducing after each addition is exact: `(a + b) % M == ((a % M) + (b % M)) % M`. There is no comparison, subtraction or division anywhere, so the residue is all that is ever needed. Python integers do not overflow, so here the modulus is only about the answer's required form; the true value for `'a'*1000` and `'a'*500` is `C(1000, 500)`, 300 digits.

**Complexity:** Time O(len(s) * len(t)) (at most 1000 x 500 = 500,000 cell updates). Space O(len(t)) with one row, O(len(s) * len(t)) with the full table. Big-integer additions grow with the count's digits; with the modulus each is O(1).

**Dry run:** `s = 'rabbbit'`, `t = 'rabbit'`. Rows below are the one-row array after each letter of `s` (columns j = 0..6 for `-,r,a,b,b,i,t`).
- start `[1,0,0,0,0,0,0]`
- after `r`: `[1,1,0,0,0,0,0]`; after `a`: `[1,1,1,0,0,0,0]`; after the first `b`: `[1,1,1,1,0,0,0]`.
- second `b`: `dp[4] += dp[3]` (1) and `dp[3] += dp[2]` (1+1): `[1,1,1,2,1,0,0]`.
- third `b`: `dp[4] += dp[3]` (1+2=3), `dp[3] += dp[2]` (2+1=3): `[1,1,1,3,3,0,0]`.
- `i`: `dp[5] += dp[4]` gives 3; `t`: `dp[6] += dp[5]` gives 3. Answer 3: choose which of the three `b`s is dropped.

**Code:**
```python
import random, itertools, sys
from math import comb
from functools import lru_cache

random.seed(21)
MOD = 10**9 + 7

def table(s, t):
    """2D: dp[i][j] = ways to spell t[:j] from s[:i]."""
    dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
    for i in range(len(s) + 1):
        dp[i][0] = 1                                   # empty t: exactly one way (choose nothing)
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            dp[i][j] = dp[i - 1][j]                    # skip s[i-1]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]           # use s[i-1] as t[j-1]
    return dp

def one_row(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):                 # j DESCENDING: dp[j-1] must still be the previous row
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]

def one_row_ascending_wrong(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(1, len(t) + 1):                 # ascending: dp[j-1] is already the NEW row, so s[i-1] is reused
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]

def one_row_mod(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                dp[j] = (dp[j] + dp[j - 1]) % MOD      # addition only: (a + b) % M == ((a % M) + (b % M)) % M
    return dp[-1]

def brute(s, t):
    return sum(1 for idx in itertools.combinations(range(len(s)), len(t)) if all(s[i] == c for i, c in zip(idx, t)))

def memo(s, t):
    @lru_cache(maxsize=None)
    def f(i, j):
        if j == len(t): return 1
        if i == len(s): return 0
        r = f(i + 1, j)
        if s[i] == t[j]: r += f(i + 1, j + 1)
        return r
    return f(0, 0)

# examples
for s, t, exp in [('rabbbit', 'rabbit', 3), ('babgbag', 'bag', 5), ('abc', '', 1), ('a', 'aa', 0), ('aaaa', 'aa', 6)]:
    a, b, c = one_row(s, t), table(s, t)[-1][-1], brute(s, t)
    assert a == b == c == exp == memo(s, t), (s, t, a, b, c)
    print('example', repr(s), repr(t), '->', a)

# hand table, first example
s, t = 'rabbbit', 'rabbit'
dp = table(s, t)
print('2D table dp[i][j] for s=rabbbit, t=rabbit (rows i = letters of s used, columns j = letters of t):')
print('        ' + '  '.join(['-'] + list(t)))
for i, row in enumerate(dp):
    print('  %s  ' % ('-' if i == 0 else s[i - 1]), row)
# one row, printed after each letter of s
row = [1] + [0] * len(t)
print('one row after each letter of s:')
for ch in s:
    for j in range(len(t), 0, -1):
        if t[j - 1] == ch: row[j] += row[j - 1]
    print('  after', ch, row)

# seeded cross-check, len(s) <= 10
cases = nz = 0
for _ in range(600):
    alpha = random.choice(['ab', 'abc', 'a'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(0, 10)))
    t = ''.join(random.choice(alpha) for _ in range(random.randint(0, 5)))
    exp = brute(s, t)
    assert one_row(s, t) == table(s, t)[-1][-1] == one_row_mod(s, t) == memo(s, t) == exp, (s, t)
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a positive count', nz)
wrong = sum(one_row_ascending_wrong(s, t) != brute(s, t)
            for s, t in [(''.join(random.choice('ab') for _ in range(random.randint(0, 8))), ''.join(random.choice('ab') for _ in range(random.randint(0, 4)))) for _ in range(300)])
print('ascending inner loop gave a wrong answer on', wrong, 'of 300 random cases; for s=aaaa, t=aa it returns', one_row_ascending_wrong('aaaa', 'aa'), 'instead of 6')

# closed forms and the modulus
assert one_row('a' * 50, 'a' * 25) == comb(50, 25)
assert one_row('a' * 1000, 'a' * 500) == comb(1000, 500)
big = comb(1000, 500)
print('C(1000, 500) has', len(str(big)), 'digits; mod version equals exact % M:', one_row_mod('a' * 1000, 'a' * 500) == big % MOD)
for _ in range(200):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 60))); t = ''.join(random.choice('ab') for _ in range(random.randint(0, 6)))
    assert one_row_mod(s, t) == one_row(s, t) % MOD

# recursion limit (observed)
print('recursion limit', sys.getrecursionlimit())
for n, m in ((300, 150), (1000, 500)):
    s, t = 'a' * n, 'a' * m
    try:
        print('memoised s=%d, t=%d ->' % (n, m), memo(s, t) == one_row(s, t))
    except RecursionError:
        print('memoised s=%d, t=%d -> RecursionError (bottom-up is fine)' % (n, m))

# edge cases
assert one_row('', '') == 1 and one_row('', 'a') == 0 and one_row('abc', '') == 1 and one_row('a', 'aa') == 0
assert one_row('abc', 'abcd') == 0
print('edge asserts passed')
```

**Output (my run):**
```
example 'rabbbit' 'rabbit' -> 3
example 'babgbag' 'bag' -> 5
example 'abc' '' -> 1
example 'a' 'aa' -> 0
example 'aaaa' 'aa' -> 6
2D table dp[i][j] for s=rabbbit, t=rabbit (rows i = letters of s used, columns j = letters of t):
        -  r  a  b  b  i  t
  -   [1, 0, 0, 0, 0, 0, 0]
  r   [1, 1, 0, 0, 0, 0, 0]
  a   [1, 1, 1, 0, 0, 0, 0]
  b   [1, 1, 1, 1, 0, 0, 0]
  b   [1, 1, 1, 2, 1, 0, 0]
  b   [1, 1, 1, 3, 3, 0, 0]
  i   [1, 1, 1, 3, 3, 3, 0]
  t   [1, 1, 1, 3, 3, 3, 3]
one row after each letter of s:
  after r [1, 1, 0, 0, 0, 0, 0]
  after a [1, 1, 1, 0, 0, 0, 0]
  after b [1, 1, 1, 1, 0, 0, 0]
  after b [1, 1, 1, 2, 1, 0, 0]
  after b [1, 1, 1, 3, 3, 0, 0]
  after i [1, 1, 1, 3, 3, 3, 0]
  after t [1, 1, 1, 3, 3, 3, 3]
cross-check cases 600 | with a positive count 351
ascending inner loop gave a wrong answer on 93 of 300 random cases; for s=aaaa, t=aa it returns 10 instead of 6
C(1000, 500) has 300 digits; mod version equals exact % M: True
recursion limit 1000
memoised s=300, t=150 -> True
memoised s=1000, t=500 -> RecursionError (bottom-up is fine)
edge asserts passed
```

Reading the output:
- All five examples match the one-row DP, the 2D table, the memoised recursion and the combination enumeration. The 2D table printed is the full version of the dry run.
- 600 seeded random cases (`len(s) <= 10`) agree across five implementations; 351 had a positive count, so both zero and non-zero answers were tested.
- The ascending inner loop is wrong (10 instead of 6 on `aaaa`/`aa`, wrong on 93 of 300 random cases).
- `C(1000, 500)` has 300 digits and the modulus version equals `exact % M`.
- Recursion: the memoised version on 300 x 150 works; on `s` of 1000 and `t` of 500 equal letters it raises `RecursionError` at the default limit of 1000, because it nests about `len(s)` deep (observation on Python 3.13). Bottom-up is unaffected.

**Edge cases:**
- Empty `t`: 1, even when `s` is empty (`('', '')` is 1, `('', 'a')` is 0).
- `len(t) > len(s)`: 0 (the DP finds it by itself).
- Equal letters count by position: `'aaaa'`/`'aa'` is 6 = `C(4, 2)`.
- Big answers: `'a'*1000` / `'a'*500` is a 300-digit integer; fine in Python, would overflow in C++ or Java.

**Follow-ups:**
- "Why does the counting DP use only `+`?" Each way is counted exactly once by its last-letter decision, so ways add; nothing is compared, so residues are safe.
- "Return the answer modulo 10^9+7?" Put `% MOD` on the single addition (and on the 2D version's cell). Do not mod the loop bounds or the letters.
- "Edit distance or LCS instead?" Same grid, `min`/`max` instead of `+` (Q8 edit distance and Q6 LCS of this part are the full tabulated versions).

**Common mistakes:**
- Inner loop ascending in the one-row version (reuses `s[i-1]`).
- Forgetting `dp[0] = 1` (everything becomes 0).
- Using `dp[i-1][j-1]` only when letters match, and forgetting to add the skip case `dp[i-1][j]` always.
- Counting distinct subsequence STRINGS (that is a different problem); here equal letters at different positions count separately.
- Memoised recursion at `len(s) = 1000`: `RecursionError`.

### Q22 ⭐⭐ 🔴 Burst balloons. `nums` has 0 <= len <= 300 integers in 0..100, one per balloon. Bursting the balloon at position i gives `left * nums[i] * right` coins, where `left` and `right` are the CURRENT neighbours (a missing neighbour counts as 1); the balloon then disappears. Return the maximum coins for bursting all balloons in the best order (0 for an empty list). Explain why 'which balloon bursts first' does not split the problem and 'which bursts LAST in the interval' does, give `dp[l][r]` on a list padded with a 1 at each end (open interval), the order in which interval lengths grow, and the O(n^3) time. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every burst order by plain recursion (len <= 7) on small inputs. Example: nums=[3, 1, 5, 8] -> 167; nums=[1, 5] -> 10; nums=[7] -> 7; nums=[] -> 0; nums=[2, 2, 2] -> 14.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP. The state is a range, ranges grow by length, and the transition picks a split point. The trick is choosing the right thing to split on: the LAST balloon, not the first.

**Say this first (1 line):** "If I pick the first balloon to burst, its neighbours change and the two sides still touch each other, so the problem does not split. If I pick the last balloon in an interval, everything else in it is already gone, so its neighbours are fixed: the two interval ends. Then the two sides are independent."

**Brute force:** Try every balloon as the next burst on the current list, recurse on the shorter list. `n!` orders. The recursion without a memo is the oracle (len <= 7, 5040 orders).

**Optimal:**
- Pad the list: `a = [1] + nums + [1]`. Use the OPEN interval `(l, r)`: the balloons strictly between indices `l` and `r`, with `a[l]` and `a[r]` still alive.
- State: `dp[l][r]` = best coins for bursting everything strictly between `l` and `r`.
- Transition: let `k` (`l < k < r`) be the balloon burst LAST inside `(l, r)`. At that moment only `a[l]` and `a[r]` remain next to it, so it earns `a[l] * a[k] * a[r]`. Before that, the balloons in `(l, k)` were burst with `a[l]` and `a[k]` as their outer neighbours and the balloons in `(k, r)` with `a[k]` and `a[r]`. These two sub-problems never see each other, because `a[k]` stands between them the whole time. So `dp[l][r] = max over k of dp[l][k] + dp[k][r] + a[l]*a[k]*a[r]`.
- Why "first" fails: after bursting `k` first, the left neighbour of `k`'s right neighbour is now `k`'s left neighbour. The left and right sides interact through every later burst near the gap, so `dp[left] + dp[right]` is not a valid split. The code shows a naive first-burst split that disagrees with the true optimum on 236 of 300 random lists (on `[3,1,5,8]` it gives 66, not 167).
- Base: `dp[l][l+1] = 0` (nothing between), and the table is zero-initialised. An empty `nums` gives `dp[0][1] = 0`.
- Order: by interval length (`r - l` from 2 up), because `dp[l][r]` needs shorter intervals `dp[l][k]` and `dp[k][r]`. Answer `dp[0][n+1]`.

**Complexity:** O(n^2) states times an O(n) scan over `k`: O(n^3) time (about n^3 / 6 inner steps, 4.5 million for n = 300), O(n^2) space. Python handles n = 300 in well under a second here (sandbox timing). Space can't drop to O(n) easily because `dp[l][r]` reads both `dp[l][k]` (same row) and `dp[k][r]` (later rows).

**Dry run:** `nums = [3, 1, 5, 8]`, padded `[1, 3, 1, 5, 8, 1]` (indices 0..5).
- Length 2 (one balloon between): `dp[0][2] = 1*3*1 = 3`, `dp[1][3] = 3*1*5 = 15`, `dp[2][4] = 1*5*8 = 40`, `dp[3][5] = 5*8*1 = 40`.
- Length 3: `dp[0][3]`: last `k=1`: `0 + dp[1][3] + 1*3*5 = 30`; last `k=2`: `dp[0][2] + 0 + 1*1*5 = 8`. Best 30. Similarly `dp[1][4] = 135`, `dp[2][5] = 48`.
- Length 4: `dp[0][4] = 159`, `dp[1][5] = 159`.
- Length 5, `dp[0][5]`: last is `3` gives `0 + 159 + 3 = 162`; last is `1` gives 52; last is `5` gives 75; last is `8` gives `159 + 0 + 8 = 167`. Answer 167 (burst 1, 5, 3, 8 in that order: 15 + 120 + 24 + 8).

**Code:**
```python
import random, sys, time
from functools import lru_cache

random.seed(22)

def burst(nums):
    """dp[l][r] = best coins for the balloons strictly between l and r, which stay un-burst until the end (open interval)."""
    a = [1] + list(nums) + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):                   # r - l = 2 is one balloon between; shorter intervals are empty (0)
        for l in range(0, n - length):
            r = l + length
            best = 0
            for k in range(l + 1, r):            # k = the balloon burst LAST inside (l, r)
                c = dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]
                if c > best: best = c
            dp[l][r] = best
    return dp[0][n - 1]

def burst_table(nums):
    a = [1] + list(nums) + [1]; n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            dp[l][r] = max(dp[l][k] + dp[k][r] + a[l] * a[k] * a[r] for k in range(l + 1, r))
    return a, dp

def memo(nums):
    a = [1] + list(nums) + [1]
    @lru_cache(maxsize=None)
    def f(l, r):
        return max((f(l, k) + f(k, r) + a[l] * a[k] * a[r] for k in range(l + 1, r)), default=0)
    return f(0, len(a) - 1)

def brute(nums):
    """Every burst order by plain recursion on the current list (neighbours are the CURRENT neighbours)."""
    def f(arr):
        if not arr: return 0
        return max((arr[i - 1] if i else 1) * arr[i] * (arr[i + 1] if i + 1 < len(arr) else 1) + f(arr[:i] + arr[i + 1:])
                   for i in range(len(arr)))
    return f(list(nums))

def first_burst_wrong(nums):
    """Tempting split on the FIRST balloon: pretend the two sides become independent, each with outer neighbours 1."""
    nums = list(nums)
    if not nums: return 0
    best = 0
    for k in range(len(nums)):
        left = nums[k - 1] if k else 1
        right = nums[k + 1] if k + 1 < len(nums) else 1
        best = max(best, left * nums[k] * right + first_burst_wrong(nums[:k]) + first_burst_wrong(nums[k + 1:]))
    return best

# examples
for nums, exp in [([3, 1, 5, 8], 167), ([1, 5], 10), ([7], 7), ([], 0), ([2, 2, 2], 14)]:
    a, b, c = burst(nums), brute(nums), memo(nums)
    assert a == b == c == exp, (nums, a, b, c)
    print('example', nums, '->', a)

# hand table for [3,1,5,8]
a, dp = burst_table([3, 1, 5, 8])
print('padded list', a)
print('dp[l][r] (open interval, rows l, columns r):')
for l in range(len(a)):
    print('  l=%d' % l, dp[l])
print('dp[0][5] = 167, last balloon k tried in (0,5):')
for k in range(1, 5):
    print('   k=%d (value %d): dp[0][%d] + dp[%d][5] + 1*%d*1 = %d + %d + %d = %d' % (k, a[k], k, k, a[k], dp[0][k], dp[k][5], a[0] * a[k] * a[5], dp[0][k] + dp[k][5] + a[0] * a[k] * a[5]))

# seeded cross-check, len <= 7
cases = 0
for _ in range(400):
    nums = [random.randint(0, 9) for _ in range(random.randint(0, 7))]
    assert burst(nums) == brute(nums) == memo(nums), nums
    cases += 1
print('cross-check cases', cases)
wrong = 0
for _ in range(300):
    nums = [random.randint(1, 9) for _ in range(random.randint(2, 6))]
    wrong += first_burst_wrong(nums) != burst(nums)
print('first-burst split disagrees with the true optimum on', wrong, 'of 300 random lists; e.g. [3, 1, 5, 8] gives', first_burst_wrong([3, 1, 5, 8]), 'not 167')

# edge cases (values 0..100, zeros included)
assert burst([0]) == 0 and burst([0, 0, 0]) == 0 and burst([100]) == 100
assert burst([100, 100]) == 100 * 100 + 100
print('edge asserts passed')

# max size n = 300, bottom-up; memo depth
print('recursion limit', sys.getrecursionlimit())
nums = [random.randint(0, 100) for _ in range(300)]
t0 = time.perf_counter(); r = burst(nums); t1 = time.perf_counter()
print('n=300 bottom-up:', r, '(sandbox timing %.1f s)' % (t1 - t0))
try:
    print('n=300 memoised equals bottom-up:', memo(nums) == r)
except RecursionError:
    print('n=300 memoised: RecursionError')
big = [random.randint(0, 100) for _ in range(1100)]
try:
    memo(big); print('n=1100 memoised ran')
except RecursionError:
    print('n=1100 memoised: RecursionError (depth grows with n; outside the stated sizes)')
```

**Output (my run):**
```
example [3, 1, 5, 8] -> 167
example [1, 5] -> 10
example [7] -> 7
example [] -> 0
example [2, 2, 2] -> 14
padded list [1, 3, 1, 5, 8, 1]
dp[l][r] (open interval, rows l, columns r):
  l=0 [0, 0, 3, 30, 159, 167]
  l=1 [0, 0, 0, 15, 135, 159]
  l=2 [0, 0, 0, 0, 40, 48]
  l=3 [0, 0, 0, 0, 0, 40]
  l=4 [0, 0, 0, 0, 0, 0]
  l=5 [0, 0, 0, 0, 0, 0]
dp[0][5] = 167, last balloon k tried in (0,5):
   k=1 (value 3): dp[0][1] + dp[1][5] + 1*3*1 = 0 + 159 + 3 = 162
   k=2 (value 1): dp[0][2] + dp[2][5] + 1*1*1 = 3 + 48 + 1 = 52
   k=3 (value 5): dp[0][3] + dp[3][5] + 1*5*1 = 30 + 40 + 5 = 75
   k=4 (value 8): dp[0][4] + dp[4][5] + 1*8*1 = 159 + 0 + 8 = 167
cross-check cases 400
first-burst split disagrees with the true optimum on 236 of 300 random lists; e.g. [3, 1, 5, 8] gives 66 not 167
edge asserts passed
recursion limit 1000
n=300 bottom-up: 113082798 (sandbox timing 0.6 s)
n=300 memoised equals bottom-up: True
n=1100 memoised: RecursionError (depth grows with n; outside the stated sizes)
```

Reading the output:
- All five examples match the O(n^3) table, the memoised version and the every-order recursion. The printed table is the one in the dry run, and the last `for k` lines show the four candidates for `dp[0][5]`.
- 400 seeded random lists of length 0 to 7 (values 0..9, so zero-value balloons appear) agree across the three implementations.
- Recursion: the memoised recursion nests about `n` deep. On 300 balloons it equals the table; on 1100 it raises `RecursionError` at the default limit of 1000 (observation on Python 3.13; 1100 is outside the stated size and shown only to mark the cause). The stated limit n = 300 is safe either way, and bottom-up has no depth issue.

**Edge cases:**
- Empty list: 0 (padding gives two 1s and no balloons between).
- One balloon: its own value (`1 * v * 1`).
- Zeros: allowed; bursting a zero earns nothing but removes it as a neighbour. Padding with 1, not 0, keeps ends from erasing everything.
- All equal values and n = 300: the table is full but still O(n^3).

**Follow-ups:**
- "Recover the burst order?" Store the best `k` per `(l, r)`, then recurse: the order is the last balloon of the whole interval being burst last, so print the order for `(l, k)` and `(k, r)` first, then `k`.
- "Why O(n^3) and not O(n^2)?" Each of O(n^2) intervals scans O(n) split points. Same shape as matrix chain (Q23).
- "Same idea elsewhere?" Minimum cost to cut a stick and minimum score triangulation: choose the last cut or the last triangle on the edge, so the pieces are independent.

**Common mistakes:**
- Splitting on the first balloon (the sides are not independent).
- Using a closed interval and forgetting that the neighbours at the ends are the interval ends, not the balloons next to them in the original list.
- Padding with 0 instead of 1 (everything becomes 0).
- Iterating `l` and `r` in plain nested order instead of by length (reads cells that are not filled yet).
- Mutating the list while recursing in the brute force instead of building a new list.

### Q23 ⭐⭐ 🔴 Matrix chain multiplication with the parenthesisation. `dims` has 2 <= len <= 201 positive integers (each <= 100); matrix i (0-indexed) has dims[i] rows and dims[i+1] columns, so there are n = len(dims) - 1 matrices. Multiplying an a x b matrix by a b x c matrix costs a*b*c scalar multiplications. Return `[cost, expr]`: the minimum total cost to multiply all matrices in order, and one optimal parenthesisation written as a string such as `((A0A1)A2)` (a single matrix is `A0`). Several parenthesisations can tie, so the tie rule is fixed: split an interval at the smallest k (left part A_i..A_k) that achieves the minimum, applied recursively. Define `dp[i][j]`, the split recurrence and the interval order, and state O(n^3) time and O(n^2) space. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every parenthesisation (n <= 6) and choosing by cost then by smallest root split, recursively on small inputs. Example: dims=[10, 30, 5, 60] -> [4500, '((A0A1)A2)']; dims=[40, 20, 30, 10, 30] -> [26000, '((A0(A1A2))A3)']; dims=[5, 7] -> [0, 'A0']; dims=[1, 2, 3, 4, 5] -> [38, '(((A0A1)A2)A3)'].
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP with a split point, plus reconstruction from a split table. `dp[i][j]` is the best cost for the sub-chain `A_i..A_j`, built from shorter sub-chains.

**Say this first (1 line):** "The last multiplication splits the chain at some `k`: left part `A_i..A_k`, right part `A_k+1..A_j`. Both parts are optimal on their own, and the final product costs `dims[i] * dims[k+1] * dims[j+1]`. I try every `k`, keep the smallest one that achieves the minimum, and rebuild the string from the split table."

**Brute force:** Enumerate every full parenthesisation: Catalan(n-1) of them (5 for 4 matrices, 14 for 5, 42 for 6, a 117-digit number for 200). For each compute the cost, then pick by cost and by the tie rule (smallest root split `k`, then recursively the left tree, then the right tree). That is the oracle for n <= 6.

**Optimal:**
- Matrix `A_i` is `dims[i] x dims[i+1]`. The product `A_i..A_j` is `dims[i] x dims[j+1]`.
- State: `cost[i][j]` for `0 <= i <= j < n`, `split[i][j]` = chosen `k`.
- Transition: `cost[i][j] = min over k in [i, j-1] of cost[i][k] + cost[k+1][j] + dims[i] * dims[k+1] * dims[j+1]`. The first two terms are the two sub-chains; the last is the final multiplication of a `dims[i] x dims[k+1]` by a `dims[k+1] x dims[j+1]` matrix.
- Base: `cost[i][i] = 0` (a single matrix needs no multiplication).
- Order: by chain length 2, 3, ..., n, so shorter sub-chains are ready. Answer `cost[0][n-1]`.
- Tie rule: scan `k` upwards and update only on a STRICT improvement (`c < best`). The first, smallest `k` is kept. Applying the rule at every interval gives the oracle's choice: the oracle compares trees by cost, then by `(k, left key, right key)`; for a fixed root `k` the best total needs both sub-chains optimal, and among those the smallest keys are what the same rule picks inside each sub-chain. Verified exhaustively below.
- Rebuild: `paren(i, j)` returns `A_i` when `i == j`, else `'(' + paren(i, k) + paren(k+1, j) + ')'` with `k = split[i][j]`. The recursion depth is at most `n - 1 = 199` for the stated size, below CPython's default limit of 1000, so plain recursion is fine here.
- Time O(n^3): O(n^2) intervals times an O(n) scan. Space O(n^2) for the two tables.

**Complexity:** Time O(n^3) (about n^3 / 6 split evaluations, 1.3 million for 200 matrices; the table loop ran in a fraction of a second here, sandbox timing). Space O(n^2). The string has about 5n characters, so building it is O(n) per level and O(n^2) in the worst case, small beside the DP.

**Dry run:** `dims = [10, 30, 5, 60]`: A0 is 10x30, A1 is 30x5, A2 is 5x60.
- Length 2: `cost[0][1] = 10*30*5 = 1500` (split 0); `cost[1][2] = 30*5*60 = 9000` (split 1).
- Length 3, `cost[0][2]`: `k=0`: `cost[0][0] + cost[1][2] + 10*30*60 = 0 + 9000 + 18000 = 27000`. `k=1`: `cost[0][1] + cost[2][2] + 10*5*60 = 1500 + 0 + 3000 = 4500`. The minimum is 4500 at `k=1`.
- Rebuild: root split 1, so `(` + `paren(0,1)` + `paren(2,2)` + `)` = `((A0A1)A2)`. Answer `[4500, '((A0A1)A2)']`.
- A tie: `dims = [2, 2, 2, 2]` makes both parenthesisations cost 16, and the rule returns `(A0(A1A2))` (root split `k=0` is smaller than `k=1`).

**Code:**
```python
import random, itertools, sys, time

random.seed(23)

def matrix_chain(dims):
    """cost[i][j] = fewest scalar multiplications for matrices A_i..A_j; split[i][j] = smallest k achieving it."""
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = None
            for k in range(i, j):                      # left part A_i..A_k, right part A_k+1..A_j
                c = cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if best is None or c < best:           # STRICT <: the first (smallest) k wins ties
                    best = c
                    split[i][j] = k
            cost[i][j] = best

    def paren(i, j):
        if i == j:
            return 'A%d' % i
        k = split[i][j]
        return '(' + paren(i, k) + paren(k + 1, j) + ')'
    return [cost[0][n - 1], paren(0, n - 1)], cost, split

def solve(dims):
    return matrix_chain(dims)[0]

def brute(dims):
    """Enumerate every parenthesisation; choose by cost, then by smallest root split, then (recursively) left tree, then right tree."""
    n = len(dims) - 1
    def trees(i, j):
        if i == j:
            yield (0, (), 'A%d' % i)
            return
        for k in range(i, j):
            for cl, kl, sl in trees(i, k):
                for cr, kr, sr in trees(k + 1, j):
                    yield (cl + cr + dims[i] * dims[k + 1] * dims[j + 1], (k, kl, kr), '(' + sl + sr + ')')
    best = min(trees(0, n - 1), key=lambda t: (t[0], t[1]))
    return [best[0], best[2]]

def count_trees(n):                                     # Catalan(n - 1)
    from math import comb
    return comb(2 * (n - 1), n - 1) // n

# examples
for dims, exp in [([10, 30, 5, 60], [4500, '((A0A1)A2)']), ([40, 20, 30, 10, 30], [26000, '((A0(A1A2))A3)']),
                  ([5, 7], [0, 'A0']), ([1, 2, 3, 4, 5], [38, '(((A0A1)A2)A3)'])]:
    a, b = solve(dims), brute(dims)
    assert a == b == exp, (dims, a, b)
    print('example', dims, '->', a)

# hand table for dims = [10, 30, 5, 60]
dims = [10, 30, 5, 60]
_, cost, split = matrix_chain(dims)
print('dims', dims, '-> matrices A0 10x30, A1 30x5, A2 5x60')
print('cost table (rows i, columns j):')
for row in cost: print('  ', row)
print('split table:')
for row in split: print('  ', row)
print('cost[0][2]: k=0 ->', cost[0][0] + cost[1][2] + 10 * 30 * 60, ' k=1 ->', cost[0][1] + cost[2][2] + 10 * 5 * 60)

# a tie to show the smallest-k rule: all dims equal, every parenthesisation costs the same
print('tie example dims [2,2,2,2] ->', solve([2, 2, 2, 2]), '(all', count_trees(3), 'trees cost 16; smallest root split k=0 wins)')
assert solve([2, 2, 2, 2]) == [16, '(A0(A1A2))']

# seeded cross-check, n <= 6 matrices, small dims so ties are common
cases = 0
for _ in range(400):
    n = random.randint(1, 6)
    dims = [random.randint(1, 4) for _ in range(n + 1)]
    got, want = solve(dims), brute(dims)
    assert got == want, (dims, got, want)
    cases += 1
print('cross-check cases', cases)

# exhaustive: all chains of 4 matrices (5 dims) with dims in 1..3, and all of 3 matrices with dims 1..5
cnt = 0
for dims in itertools.product(range(1, 4), repeat=5):
    assert solve(list(dims)) == brute(list(dims)); cnt += 1
for dims in itertools.product(range(1, 6), repeat=4):
    assert solve(list(dims)) == brute(list(dims)); cnt += 1
print('exhaustive chains checked:', cnt)

# how many random chains had more than one optimal tree (so the tie rule mattered)
def all_optimal(dims):
    n = len(dims) - 1
    def trees(i, j):
        if i == j:
            yield (0, 'A%d' % i); return
        for k in range(i, j):
            for cl, sl in trees(i, k):
                for cr, sr in trees(k + 1, j):
                    yield (cl + cr + dims[i] * dims[k + 1] * dims[j + 1], '(' + sl + sr + ')')
    ts = list(trees(0, n - 1)); m = min(t[0] for t in ts)
    return sum(1 for t in ts if t[0] == m)
multi = 0
random.seed(230)
for _ in range(300):
    n = random.randint(2, 6)
    dims = [random.randint(1, 4) for _ in range(n + 1)]
    multi += all_optimal(dims) > 1
print('of 300 more random chains (n 2..6), several optimal parenthesisations existed in', multi)

# edge cases
assert solve([5, 7]) == [0, 'A0']
assert solve([3, 4, 5]) == [60, '(A0A1)']

# max size: 200 matrices (dims 201 long), recursion depth of paren() is at most n
print('recursion limit', sys.getrecursionlimit())
dims = [random.randint(1, 100) for _ in range(201)]
t0 = time.perf_counter(); res = solve(dims); t1 = time.perf_counter()
print('n=200 matrices: cost', res[0], '| string length', len(res[1]), '(sandbox timing %.1f s)' % (t1 - t0))
# all-ones dims: every tree costs n - 1, the smallest-k rule gives the right-deep tree, nesting depth 199 (below the default limit of 1000)
d2 = [1] * 201
res2 = solve(d2); print('n=200 all-ones dims: cost', res2[0], '| string starts', res2[1][:20])
assert res2[0] == 199 and res2[1].count('(') == 199
```

**Output (my run):**
```
example [10, 30, 5, 60] -> [4500, '((A0A1)A2)']
example [40, 20, 30, 10, 30] -> [26000, '((A0(A1A2))A3)']
example [5, 7] -> [0, 'A0']
example [1, 2, 3, 4, 5] -> [38, '(((A0A1)A2)A3)']
dims [10, 30, 5, 60] -> matrices A0 10x30, A1 30x5, A2 5x60
cost table (rows i, columns j):
   [0, 1500, 4500]
   [0, 0, 9000]
   [0, 0, 0]
split table:
   [0, 0, 1]
   [0, 0, 1]
   [0, 0, 0]
cost[0][2]: k=0 -> 27000  k=1 -> 4500
tie example dims [2,2,2,2] -> [16, '(A0(A1A2))'] (all 2 trees cost 16; smallest root split k=0 wins)
cross-check cases 400
exhaustive chains checked: 868
of 300 more random chains (n 2..6), several optimal parenthesisations existed in 70
recursion limit 1000
n=200 matrices: cost 503525 | string length 1088 (sandbox timing 0.3 s)
n=200 all-ones dims: cost 199 | string starts (A0(A1(A2(A3(A4(A5(A
```

Reading the output:
- All four examples match the DP and the enumeration. The cost and split tables printed are the ones in the dry run; the `k=0` and `k=1` candidates for `cost[0][2]` are 27000 and 4500.
- 400 seeded random chains (n <= 6, dims 1..4) match the oracle in both cost AND string, and in the extra 300 random chains several optimal parenthesisations existed in 70, so the tie rule was really exercised.
- Exhaustive: all 243 chains of 4 matrices with dims in 1..3 and all 625 chains of 3 matrices with dims in 1..5 agree (868 in all).
- 200 matrices: runs in a fraction of a second here (sandbox timing). With all dims 1 every tree costs 199, and the smallest-`k` rule produces the right-deep tree with nesting depth 199, still far from the limit.

**Edge cases:**
- One matrix (`len(dims) == 2`): cost 0, string `A0`, no loop runs.
- Two matrices: one product, string `(A0A1)`.
- Ties: many optimal trees; the strict `<` is what makes the answer match the stated rule. With `<=` you would get the LARGEST `k`.
- Dimension 1 entries (vectors): fine, they just make some products cheap.
- All equal dims: every tree ties.

**Follow-ups:**
- "Can you print it without recursion?" Yes, with an explicit stack of `(i, j)`. At n <= 200 recursion is fine; for thousands of matrices (the O(n^3) table would not fit anyway) you would need it.
- "Faster than O(n^3)?" Hu and Shing's O(n log n) algorithm exists; it is not an interview expectation.
- "Same pattern?" Optimal BST, minimum cost to cut a stick, burst balloons (Q22), polygon triangulation: all `dp[i][j] = min over k of dp[i][k] + dp[k][j] + merge cost`.

**Common mistakes:**
- Using `dims[i] * dims[k] * dims[j]`, off by one: matrix `A_i` has `dims[i]` rows and `dims[i+1]` columns, so the product of the two halves is `dims[i] * dims[k+1] * dims[j+1]`.
- Iterating by `i` then `j` instead of by length (reads cells not computed yet).
- `<=` instead of `<` in the minimum, so ties pick the largest `k` and the string differs from the required one.
- Not clearing or sizing the tables for `n = len(dims) - 1` (using `len(dims)` adds a phantom matrix).
- Returning the cost only; the prompt wants `[cost, expr]`.

### Q24 ⭐⭐ 🔴 Longest increasing path in a matrix. `matrix` is an m x n list of lists (1 <= m, n <= 200) of integers in 0..10^9. From a cell you may move up, down, left or right to a cell with a STRICTLY larger value; return the number of cells on the longest such path (a single cell counts as 1). The cells form a directed acyclic graph, so this is a DP over a DAG (the shortest-path-on-a-DAG version is Part 9 Q40). A memoised DFS nests as deep as the longest increasing path it follows, and a winding corridor of increasing values (with walls of value 0 between its rows) makes that thousands of cells, far beyond CPython's recursion limit of 1000, so a bottom-up solution is required: process the cells in increasing order of value (and say why equal values need no special order) or use a topological sort on in-degrees. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain DFS from every cell without a memo (m, n <= 3) on small inputs. Example: matrix=[[9, 9, 4], [6, 6, 8], [2, 1, 1]] -> 4; matrix=[[3, 4, 5], [3, 2, 6], [2, 2, 1]] -> 4; matrix=[[1]] -> 1; matrix=[[1, 1], [1, 1]] -> 1.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** DP over a DAG on a grid. An edge goes from a cell to a strictly larger neighbour, so there are no cycles. Longest path in a DAG = process vertices in topological order. Here the topological order is just "sort by value". (The shortest-path-on-a-DAG version is Part 9 Q40.)

**Say this first (1 line):** "Strictly increasing means the cells form a DAG. If I process cells from small to large value, every smaller neighbour is already final, so `L[i][j] = 1 + max(L of strictly smaller neighbours)`. No recursion, so no depth problem."

**Brute force:** DFS from every cell with no memo, trying all four moves to strictly larger cells. Each cell can be reached along many paths, so time is exponential in the path length. It is the oracle for m, n <= 3.

**Optimal:**
- State: `L[i][j]` = number of cells on the longest increasing path that ENDS at `(i, j)`. Answer is the maximum over all cells.
- Transition: `L[i][j] = 1 + max(L[a][b])` over the four neighbours with `matrix[a][b] < matrix[i][j]`, or 1 if there is none. Base: every cell starts at 1 (the path of one cell).
- Order: sort all cells by value (`sorted` on tuples `(value, i, j)`) and fill in that order. A strictly smaller neighbour has a strictly smaller value, so it is earlier in the order and its `L` is final.
- Why equal values need no special order: an equal neighbour is never read (the test is `<`), so the position of equal cells relative to each other changes nothing. The code shuffles the order among equal values and checks all 19,683 3 x 3 matrices with values 0..2 (the shuffle on every 7th) and the answer never changes.
- Alternative, Kahn's topological sort: in-degree of a cell = number of strictly smaller neighbours. Start from in-degree 0 (local minima). Peel layer by layer; the number of layers is the longest path length. It is O(mn) with no sort.
- Why bottom-up is required: a memoised DFS `f(i, j)` nests as deep as the longest increasing path it follows. A winding corridor of increasing values, with walls of value 0 between its rows, makes that path thousands of cells long. On a 61 x 61 corridor (1921 corridor cells) the memoised DFS raises `RecursionError` at the default limit of 1000 (observation on Python 3.13; a 21 x 21 corridor with 241 cells runs). The sorted-order DP and Kahn take the same input in a few hundredths of a second (sandbox timing), even on the 199 x 199 corridor with about 20,000 cells.

**Complexity:** Sorted version: O(mn log(mn)) time for the sort plus O(mn) for the relaxations (4 neighbours per cell); space O(mn). Kahn: O(mn) time, O(mn) space. For 200 x 200 that is 40,000 cells.

**Dry run:** `[[9,9,4],[6,6,8],[2,1,1]]`. Cells in increasing value (ties in position order); `L` after each:
- The two 1s, `(2,1)` and `(2,2)`: no smaller neighbour, `L = 1`.
- `2` at `(2,0)`: neighbour `(2,1)` has value 1, so `L = 2`.
- `4` at `(0,2)`: neighbours `9` and `8` are larger, none smaller, `L = 1`.
- `6` at `(1,0)`: neighbour `(2,0)` has `L = 2`, so `L = 3`. `6` at `(1,1)`: smaller neighbour `(2,1)` (1), `L = 2`.
- `8` at `(1,2)`: smaller neighbours `4` (L 1), `6` at `(1,1)` (L 2), `1` (L 1): `L = 3`.
- `9` at `(0,0)`: smaller neighbour `6` at `(1,0)` (L 3), so `L = 4`. `9` at `(0,1)`: `6` below (L 2), `4` to its right (L 1): `L = 3`.
- Final `L = [[4,3,1],[3,2,3],[2,1,1]]`, answer 4: `1 -> 2 -> 6 -> 9`.

**Code:**
```python
import random, sys, time, itertools
from collections import deque
from functools import cache

random.seed(24)
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def lip_sorted(matrix):
    """L[i][j] = cells on the longest increasing path that ENDS at (i, j). Cells in increasing value order."""
    m, n = len(matrix), len(matrix[0])
    order = sorted((matrix[i][j], i, j) for i in range(m) for j in range(n))
    L = [[1] * n for _ in range(m)]
    best = 1
    for v, i, j in order:
        for di, dj in DIRS:
            a, b = i + di, j + dj
            if 0 <= a < m and 0 <= b < n and matrix[a][b] < v:       # strictly smaller neighbour: already final
                if L[a][b] + 1 > L[i][j]:
                    L[i][j] = L[a][b] + 1
        if L[i][j] > best:
            best = L[i][j]
    return best

def lip_kahn(matrix):
    """Topological peel: edge small -> big; in-degree = number of strictly smaller neighbours. Answer = number of layers."""
    m, n = len(matrix), len(matrix[0])
    indeg = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for di, dj in DIRS:
                a, b = i + di, j + dj
                if 0 <= a < m and 0 <= b < n and matrix[a][b] < matrix[i][j]:
                    indeg[i][j] += 1
    q = deque((i, j) for i in range(m) for j in range(n) if indeg[i][j] == 0)
    layers = 0
    while q:
        layers += 1
        for _ in range(len(q)):
            i, j = q.popleft()
            for di, dj in DIRS:
                a, b = i + di, j + dj
                if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[i][j]:
                    indeg[a][b] -= 1
                    if indeg[a][b] == 0:
                        q.append((a, b))
    return layers

def lip_memo(matrix):
    m, n = len(matrix), len(matrix[0])
    @cache
    def f(i, j):
        return 1 + max([f(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                        if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[i][j]] or [0])
    return max(f(i, j) for i in range(m) for j in range(n))

def brute(matrix):
    """Plain DFS from every cell, no memo."""
    m, n = len(matrix), len(matrix[0])
    def f(i, j):
        return 1 + max([f(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                        if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[i][j]] or [0])
    return max(f(i, j) for i in range(m) for j in range(n))

def lip_sorted_shuffled(matrix):
    """Same as lip_sorted but the order among EQUAL values is random."""
    m, n = len(matrix), len(matrix[0])
    cells = [(i, j) for i in range(m) for j in range(n)]
    random.shuffle(cells)
    cells.sort(key=lambda c: matrix[c[0]][c[1]])               # stable: equal values keep the shuffled order
    L = [[1] * n for _ in range(m)]
    for i, j in cells:
        for di, dj in DIRS:
            a, b = i + di, j + dj
            if 0 <= a < m and 0 <= b < n and matrix[a][b] < matrix[i][j]:
                L[i][j] = max(L[i][j], L[a][b] + 1)
    return max(map(max, L))

# examples
for mat, exp in [([[9, 9, 4], [6, 6, 8], [2, 1, 1]], 4), ([[3, 4, 5], [3, 2, 6], [2, 2, 1]], 4), ([[1]], 1), ([[1, 1], [1, 1]], 1)]:
    a, b, c, d = lip_sorted(mat), lip_kahn(mat), brute(mat), lip_memo(mat)
    assert a == b == c == d == exp, (mat, a, b, c, d)
    print('example', mat, '->', a)

# hand table, example 1
mat = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
m, n = 3, 3
L = [[1] * n for _ in range(m)]
print('process cells in increasing value; L = longest path ending at the cell')
for v, i, j in sorted((mat[i][j], i, j) for i in range(m) for j in range(n)):
    for di, dj in DIRS:
        a, b = i + di, j + dj
        if 0 <= a < m and 0 <= b < n and mat[a][b] < v:
            L[i][j] = max(L[i][j], L[a][b] + 1)
    print('  value %d at (%d,%d): L = %d' % (v, i, j, L[i][j]))
print('final L:')
for row in L: print('  ', row)

# seeded cross-check, m, n <= 3
cases = 0
for _ in range(600):
    m, n = random.randint(1, 3), random.randint(1, 3)
    hi = random.choice([1, 2, 4, 9])
    mat = [[random.randint(0, hi) for _ in range(n)] for _ in range(m)]
    assert lip_sorted(mat) == lip_kahn(mat) == brute(mat) == lip_memo(mat), mat
    cases += 1
print('cross-check cases', cases)
# exhaustive: all 3 x 3 matrices with values 0..2 (19683), and equal-value order shuffled
cnt = 0
for vals in itertools.product(range(3), repeat=9):
    mat = [list(vals[:3]), list(vals[3:6]), list(vals[6:])]
    exp = brute(mat)
    assert lip_sorted(mat) == lip_kahn(mat) == exp
    if cnt % 7 == 0:
        assert all(lip_sorted_shuffled(mat) == exp for _ in range(3))
    cnt += 1
print('exhaustive 3 x 3 matrices with values 0..2:', cnt, '(equal-value order shuffled on every 7th)')

# edge cases
assert lip_sorted([[5]]) == 1 and lip_sorted([[1, 2, 3, 4]]) == 4 and lip_sorted([[4], [3], [2], [1]]) == 4
assert lip_sorted([[7, 7, 7]]) == 1 and lip_sorted([[0, 10**9]]) == 2

# winding corridor: rows 0, 2, 4, ... hold increasing values along a snake; walls (value 0) between; one connector per wall row
def corridor(n):
    mat = [[0] * n for _ in range(n)]; v = 1
    for i in range(0, n, 2):
        cols = range(n) if (i // 2) % 2 == 0 else range(n - 1, -1, -1)
        for j in cols:
            mat[i][j] = v; v += 1
        if i + 1 < n:
            mat[i + 1][n - 1 if (i // 2) % 2 == 0 else 0] = v; v += 1
    return mat, v - 1
print('recursion limit', sys.getrecursionlimit())
for size in (21, 61):
    mat, cells = corridor(size)
    try:
        r = lip_memo(mat); res = 'memoised DFS ok (%d)' % r
    except RecursionError:
        res = 'memoised DFS RecursionError'
    print('corridor %d x %d: path has %d cells (plus the 0 wall cell next to its start = %d); sorted DP %d, Kahn %d; %s'
          % (size, size, cells, cells + 1, lip_sorted(mat), lip_kahn(mat), res))
mat, cells = corridor(199)
t0 = time.perf_counter(); r = lip_sorted(mat); t1 = time.perf_counter(); r2 = lip_kahn(mat); t2 = time.perf_counter()
print('corridor 199 x 199 (the largest odd size within 200): path cells', cells, '-> sorted DP', r, ', Kahn', r2, '(sandbox timing %.2f s, %.2f s)' % (t1 - t0, t2 - t1))
assert r == r2 == cells + 1
big = [[random.randint(0, 10**9) for _ in range(200)] for _ in range(200)]
assert lip_sorted(big) == lip_kahn(big)
print('200 x 200 random:', lip_sorted(big))
print('edge asserts passed')
```

**Output (my run):**
```
example [[9, 9, 4], [6, 6, 8], [2, 1, 1]] -> 4
example [[3, 4, 5], [3, 2, 6], [2, 2, 1]] -> 4
example [[1]] -> 1
example [[1, 1], [1, 1]] -> 1
process cells in increasing value; L = longest path ending at the cell
  value 1 at (2,1): L = 1
  value 1 at (2,2): L = 1
  value 2 at (2,0): L = 2
  value 4 at (0,2): L = 1
  value 6 at (1,0): L = 3
  value 6 at (1,1): L = 2
  value 8 at (1,2): L = 3
  value 9 at (0,0): L = 4
  value 9 at (0,1): L = 3
final L:
   [4, 3, 1]
   [3, 2, 3]
   [2, 1, 1]
cross-check cases 600
exhaustive 3 x 3 matrices with values 0..2: 19683 (equal-value order shuffled on every 7th)
recursion limit 1000
corridor 21 x 21: path has 241 cells (plus the 0 wall cell next to its start = 242); sorted DP 242, Kahn 242; memoised DFS ok (242)
corridor 61 x 61: path has 1921 cells (plus the 0 wall cell next to its start = 1922); sorted DP 1922, Kahn 1922; memoised DFS RecursionError
corridor 199 x 199 (the largest odd size within 200): path cells 19999 -> sorted DP 20000 , Kahn 20000 (sandbox timing 0.03 s, 0.06 s)
200 x 200 random: 12
edge asserts passed
```

Reading the output:
- All four examples match the sorted-order DP, Kahn, the memoised DFS and the plain DFS. The processing table printed is the one in the dry run, and equals the printed final `L`.
- 600 seeded random matrices (m, n <= 3, values in 0..1, 0..2, 0..4 or 0..9) agree across all four methods. The exhaustive run covers all 19,683 3 x 3 matrices with values 0..2, which is where ties and plateaus occur most.
- Corridor: the 21 x 21 case runs everywhere; the 61 x 61 corridor breaks only the memoised DFS. The path length reported by both bottom-up methods is `corridor cells + 1`, not `corridor cells`: the corridor starts at value 1 and a wall cell of value 0 sits beside the start, so the longest path begins one cell earlier at the wall (found while testing).
- 200 x 200 of random values up to 10^9 gives an answer of 12 (random matrices have short paths); the corridor is the adversarial input.

**Edge cases:**
- 1 x 1: 1. All equal: 1 (strict `<`, never `<=`).
- One row or column, strictly increasing: its length.
- Values up to `10^9`: no problem for Python ints; compare directly, no arithmetic on them.
- Equal neighbours are not edges; two equal cells never extend each other.
- Single-row increasing 4 cells: 4; reversed order: still 4 (the path may go leftwards).

**Follow-ups:**
- "Return the path itself?" Keep a parent per cell (the neighbour that gave the max), walk back from the cell with the best `L`. Ties: state a rule.
- "Why not DFS with `@cache`?" Correct but its recursion depth equals the path length; use `sys.setrecursionlimit` only as a last resort (version and call-path dependent, and a thread stack size problem), or go bottom-up.
- "What if the move were non-strict (`>=`)?" Then equal cells form cycles and it is no longer a DAG.

**Common mistakes:**
- Using `<=`/`>=`, which allows plateaus and breaks the DAG.
- Sorting by value but processing equal values as if one must come first (unnecessary) or reading a neighbour that is not yet final (only possible if you forget the strict test).
- Memoising on the matrix with a list key (`@cache` on a function taking the matrix, unhashable).
- Starting with `best = 0` for an empty path count when the matrix is 1 x 1 and returning 0.
- Assuming a snake matrix always breaks recursion: it depends on the DFS order; a corridor with walls is the reliable adversary.

### Q25 ⭐ 🟢 Minimum falling path sum. `matrix` is an n x n list of lists (1 <= n <= 100) of integers in -100..100. Start in any cell of the first row; from (r, c) move to (r+1, c-1), (r+1, c) or (r+1, c+1) (staying inside the matrix). Return the smallest sum over all paths that reach the last row. Give the state, the edge handling at columns 0 and n-1, and the one-row version. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (n <= 5) on small inputs. Example: matrix=[[2, 1, 3], [6, 5, 4], [7, 8, 9]] -> 13; matrix=[[-19, 57], [-40, -5]] -> -59; matrix=[[5]] -> 5.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP, one row at a time, with three predecessors instead of two (up-left, up, up-right). Start anywhere in the top row, end anywhere in the bottom row.

**Say this first (1 line):** "`dp[c]` is the cheapest sum of a falling path that ends at column `c` of the current row. The next row reads the three nearest columns of the previous row, clipped at the edges, so one array is enough."

**Brute force:** Plain recursion `f(r, c)`: cell value plus the best of up to three cells below; the answer is the best `f(0, c)`. Without a memo it is up to 3^(n-1) paths per start. It is the oracle for n <= 5.

**Optimal:**
- State: `dp[r][c]` = smallest sum over falling paths from any cell of row 0 to `(r, c)`.
- Transition: `dp[r][c] = matrix[r][c] + min(dp[r-1][c-1], dp[r-1][c], dp[r-1][c+1])`, using only the columns that exist.
- Edge handling: at column 0 there is no `c-1`; at column `n-1` there is no `c+1`. In Python the slice `dp[max(0, c-1):c+2]` clips on its own (the right end is clipped by slicing, the left end needs the `max(0, ...)`). Writing `dp[c-1]` for `c = 0` does not raise: it silently reads the LAST column, which is not a legal move (the code shows this bug is wrong on 118 of 600 random matrices).
- Base: row 0, `dp[c] = matrix[0][c]` (any start is allowed, which is why the base is the whole row and not one cell).
- Answer: `min(dp)` after the last row (any end is allowed).
- One row: build the new row from the old one with a list comprehension, so there is no in-place overwrite problem (an in-place update would overwrite `dp[c-1]` before column `c` reads it).

**Complexity:** Time O(n^2) (n^2 cells, 3 reads each), space O(n) for one row. For n = 100 that is 10,000 cells.

**Dry run:** `[[2,1,3],[6,5,4],[7,8,9]]`.
- Row 0: `dp = [2, 1, 3]`.
- Row 1: `c=0`: `6 + min(2, 1) = 7`; `c=1`: `5 + min(2, 1, 3) = 6`; `c=2`: `4 + min(1, 3) = 5`. `dp = [7, 6, 5]`.
- Row 2: `c=0`: `7 + min(7, 6) = 13`; `c=1`: `8 + min(7, 6, 5) = 13`; `c=2`: `9 + min(6, 5) = 14`. `dp = [13, 13, 14]`.
- Answer `min(dp) = 13`: the path `1, 5, 7` (columns 1, 1, 0; each step moves to the same column or one column left or right).

**Code:**
```python
import random, itertools, sys

random.seed(25)

def falling(matrix):
    """One row. dp[c] = cheapest path sum ending at column c of the current row."""
    n = len(matrix)
    dp = list(matrix[0])                                      # base: row 0, any start
    for r in range(1, n):
        dp = [matrix[r][c] + min(dp[max(0, c - 1):c + 2])     # columns c-1, c, c+1, clipped at the edges by the slice
              for c in range(n)]
    return min(dp)                                            # end anywhere in the last row

def falling_explicit(matrix):
    """Same, with the edge handling written out (no slicing trick)."""
    n = len(matrix)
    dp = matrix[0][:]
    for r in range(1, n):
        new = []
        for c in range(n):
            best = dp[c]
            if c > 0: best = min(best, dp[c - 1])
            if c < n - 1: best = min(best, dp[c + 1])
            new.append(matrix[r][c] + best)
        dp = new
    return min(dp)

def brute(matrix):
    """Plain recursion, no memo."""
    n = len(matrix)
    def f(r, c):
        if r == n - 1: return matrix[r][c]
        return matrix[r][c] + min(f(r + 1, k) for k in (c - 1, c, c + 1) if 0 <= k < n)
    return min(f(0, c) for c in range(n))

def wrong_wraparound(matrix):
    """Bug: dp[c-1] at c = 0 is dp[-1], the LAST column, which is not a legal move."""
    n = len(matrix); dp = matrix[0][:]
    for r in range(1, n):
        dp = [matrix[r][c] + min(dp[c - 1], dp[c], dp[(c + 1) % n]) for c in range(n)]
    return min(dp)

def wrong_greedy(matrix):
    """Bug: start at the smallest top cell and keep stepping to the smallest reachable cell."""
    n = len(matrix); c = matrix[0].index(min(matrix[0])); tot = matrix[0][c]
    for r in range(1, n):
        c = min((k for k in (c - 1, c, c + 1) if 0 <= k < n), key=lambda k: matrix[r][k]); tot += matrix[r][c]
    return tot

# examples
for mat, exp in [([[2, 1, 3], [6, 5, 4], [7, 8, 9]], 13), ([[-19, 57], [-40, -5]], -59), ([[5]], 5)]:
    a, b, c = falling(mat), falling_explicit(mat), brute(mat)
    assert a == b == c == exp, (mat, a, b, c)
    print('example', mat, '->', a)

# hand table
mat = [[2, 1, 3], [6, 5, 4], [7, 8, 9]]
dp = mat[0][:]
print('row 0: dp =', dp)
for r in range(1, 3):
    print('row %d:' % r, end=' ')
    new = []
    for c in range(3):
        cand = [dp[k] for k in (c - 1, c, c + 1) if 0 <= k < 3]
        new.append(mat[r][c] + min(cand)); print('c=%d: %d + min%s = %d;' % (c, mat[r][c], cand, new[-1]), end=' ')
    dp = new; print('-> dp =', dp)
print('answer min(dp) =', min(dp))

# seeded cross-check, n <= 5
cases = 0; wa = gr = 0
for _ in range(600):
    n = random.randint(1, 5)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    exp = brute(mat)
    assert falling(mat) == falling_explicit(mat) == exp, mat
    wa += wrong_wraparound(mat) != exp; gr += wrong_greedy(mat) != exp
    cases += 1
print('cross-check cases', cases, '| wrap-around bug wrong on', wa, '| greedy wrong on', gr)

# edge cases
assert falling([[5]]) == 5 and falling([[-100] * 100 for _ in range(100)]) == -10000
assert falling([[100] * 100 for _ in range(100)]) == 10000
big = [[random.randint(-100, 100) for _ in range(100)] for _ in range(100)]
assert falling(big) == falling_explicit(big)
print('100 x 100 random:', falling(big))
print('recursion limit', sys.getrecursionlimit(), '| a memoised recursion here nests n = 100 frames, far below it')
print('edge asserts passed')
```

**Output (my run):**
```
example [[2, 1, 3], [6, 5, 4], [7, 8, 9]] -> 13
example [[-19, 57], [-40, -5]] -> -59
example [[5]] -> 5
row 0: dp = [2, 1, 3]
row 1: c=0: 6 + min[2, 1] = 7; c=1: 5 + min[2, 1, 3] = 6; c=2: 4 + min[1, 3] = 5; -> dp = [7, 6, 5]
row 2: c=0: 7 + min[7, 6] = 13; c=1: 8 + min[7, 6, 5] = 13; c=2: 9 + min[6, 5] = 14; -> dp = [13, 13, 14]
answer min(dp) = 13
cross-check cases 600 | wrap-around bug wrong on 118 | greedy wrong on 100
100 x 100 random: -6532
recursion limit 1000 | a memoised recursion here nests n = 100 frames, far below it
edge asserts passed
```

Reading the output:
- All three examples match the slice version, the explicit-edge version and the plain recursion. The hand table printed is the dry run.
- 600 seeded random matrices (n <= 5, values -9..9) agree. The same loop shows two tempting bugs are real: the wrap-around index bug is wrong on 118 of the 600 and a greedy "step to the smallest reachable cell" is wrong on 100.
- The 100 x 100 case runs instantly (sandbox, not a proof of big-O). The recursion limit is 1000 and a memoised top-down recursion here is only `n = 100` frames deep, so it would also work; bottom-up is simply shorter.

**Edge cases:**
- `n = 1`: the single value (the slice has one element).
- Negative values: the answer can be negative; do not initialise a `best` with 0.
- All values equal: `n` times the value.
- Edge columns: the clip, not wrap-around.

**Follow-ups:**
- "Print the path?" Keep the full table (or parent column per cell) and walk back from the best last-row cell. State a tie rule.
- "Allow k columns of jump (not just +-1)?" Then each cell needs a sliding-window minimum of the previous row (monotonic deque) to stay O(n^2).
- "Falling path with non-zero start constraint?" Change only the base row.

**Common mistakes:**
- Negative index wrap-around at column 0 (silent, wrong).
- `IndexError` at column `n-1` from `dp[c+1]`.
- Starting from `dp[0][0]` only, or ending at the bottom-right only.
- Greedy "pick the smallest neighbour".
- Updating one list in place so column `c` reads an already overwritten `dp[c-1]`.

### Q26 ⭐ 🟡 Longest repeating subsequence. `s` is a lowercase string with 0 <= len <= 1000. Find two index sequences p and q (each strictly increasing, same length L) such that s[p[0]] s[p[1]] ... equals s[q[0]] s[q[1]] ... and p[k] != q[k] for EVERY k (the two sequences may share an index, but never at the same position k); return the largest L (0 for len < 2). Reduce it to LCS of `s` with itself and say which single condition removes the trivial answer len(s): the two matched positions must differ (i != j). Give the transition and two rows. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every pair of index sequences (len <= 7) on small inputs. Example: s='aabebcdd' -> 3; s='abc' -> 0; s='aaa' -> 2; s='' -> 0; s='axxxy' -> 2.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP (LCS) applied to one string against itself, with one extra condition on the match.

**Say this first (1 line):** "It is LCS of `s` with `s`, but a match `s[i] == s[j]` only counts when `i != j`. Without that condition every position matches itself and the answer is just `len(s)`."

**Brute force:** Enumerate pairs of strictly increasing index sequences `p` and `q` of the same length `L`, from the largest `L` down, and accept when the letters spell the same word and `p[k] != q[k]` for every `k`. About `C(n, L)^2` pairs per length, so only for `len(s) <= 7` here. It is the oracle.

**Optimal:**
- Why LCS fits: choosing two increasing index sequences `p` and `q` that spell the same word is exactly an alignment of `s` against `s`; each pair `(p[k], q[k])` is a matched pair `(i, j)`. The stated condition `p[k] != q[k]` is exactly `i != j` for every matched pair. The two sequences may share an index at different positions `k` (one position can be `p[0]` and `q[1]`), and the table allows that.
- State: `dp[i][j]` = longest valid common subsequence of `s[:i]` and `s[:j]`.
- Transition: if `s[i-1] == s[j-1]` and `i != j` then `dp[i][j] = dp[i-1][j-1] + 1`, else `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
- Base: `dp[0][j] = dp[i][0] = 0`. Answer `dp[n][n]`. For `len(s) < 2` it is 0 automatically.
- The single condition that removes the trivial answer: `i != j`. Without it the diagonal matches every letter with itself and `dp[n][n] = n` for every string (checked below on 30 random strings, lengths 0 to 29).
- Two rows: `dp[i]` needs `dp[i-1][j-1]`, `dp[i-1][j]` (previous row) and `dp[i][j-1]` (this row), so keep `prev` and `cur`.
- Note on the statement: the pairs may share an index at different positions. A different (and also common) reading requires the two index SETS to be disjoint. That reading gives 1 for `'aaa'` while the stated one gives 2, and the two readings differ on 125 of 300 random binary strings (printed below). Use the stated `p[k] != q[k]` rule with the `i != j` condition.

**Complexity:** Time O(n^2) (1,000,000 cell updates for n = 1000), space O(n) with two rows, O(n^2) with the full table.

**Dry run:** `s = 'aabebcdd'` (positions 1..8: a a b e b c d d). The printed table has rows `i` and columns `j`, both over `s`.
- Row 1 (`a`): matches `a` at `j = 2` (letters equal, `i != j`), so from `j = 2` on the row is 1. `j = 1` is the same cell as `i = 1`, not allowed.
- Row 2 (`a`): `j = 1` matches (`dp[1][0] + 1 = 1`), then it stays 1.
- Row 3 (`b`): `j = 5` is the other `b` (`dp[2][4] + 1 = 2`). Row 5 (`b`): `j = 3` gives 2.
- Rows 7 and 8 (`d`, `d`): `dp[7][8] = dp[6][7] + 1 = 3` (the `ab` from earlier is extended by the pair of `d`s), so `dp[8][8] = 3`.
- Answer 3: the word `abd` taken at positions 1, 3, 7 and 2, 5, 8; each pair of indices differs (1 vs 2, 3 vs 5, 7 vs 8).

**Code:**
```python
import random, itertools, sys
from functools import lru_cache

random.seed(26)

def lrs(s):
    """LCS of s with itself where two positions may only match if i != j. Two rows."""
    n = len(s)
    prev = [0] * (n + 1)                                      # row i-1
    for i in range(1, n + 1):
        cur = [0] * (n + 1)                                   # row i, cur[0] = 0
        for j in range(1, n + 1):
            if s[i - 1] == s[j - 1] and i != j:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]

def lrs_table(s):
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if s[i - 1] == s[j - 1] and i != j else max(dp[i - 1][j], dp[i][j - 1])
    return dp

def lcs_no_condition(s):
    """Without i != j: LCS(s, s) = len(s), the trivial answer."""
    n = len(s); prev = [0] * (n + 1)
    for i in range(1, n + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if s[i - 1] == s[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]

def brute(s):
    """All pairs of strictly increasing index sequences P, Q of equal length L with s[P] == s[Q] and P[k] != Q[k] for every k."""
    n = len(s)
    for L in range(n, 0, -1):
        for P in itertools.combinations(range(n), L):
            word = [s[i] for i in P]
            for Q in itertools.combinations(range(n), L):
                if all(a != b for a, b in zip(P, Q)) and [s[i] for i in Q] == word:
                    return L
    return 0

def brute_disjoint(s):
    """The OTHER reading (index sets must be disjoint), for comparison only."""
    n = len(s)
    for L in range(n // 2, 0, -1):
        for P in itertools.combinations(range(n), L):
            word = [s[i] for i in P]
            rest = [i for i in range(n) if i not in P]
            for Q in itertools.combinations(rest, L):
                if [s[i] for i in Q] == word:
                    return L
    return 0

def memo(s):
    n = len(s)
    @lru_cache(maxsize=None)
    def f(i, j):                                              # suffix form: s[i:], s[j:]
        if i == n or j == n: return 0
        if s[i] == s[j] and i != j: return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

# examples
for s, exp in [('aabebcdd', 3), ('abc', 0), ('aaa', 2), ('', 0), ('axxxy', 2)]:
    a, b, c, d = lrs(s), lrs_table(s)[-1][-1], brute(s), memo(s)
    assert a == b == c == d == exp, (s, a, b, c, d)
    print('example', repr(s), '->', a, '| without the i != j condition:', lcs_no_condition(s))

# hand table for 'aabebcdd' (row i = letter s[i-1], column j = letter s[j-1])
s = 'aabebcdd'
dp = lrs_table(s)
print('dp table for', s, '(rows i, columns j; match only if letters equal and i != j):')
print('      ' + '  '.join(['-'] + list(s)))
for i, row in enumerate(dp):
    print('  %s ' % ('-' if i == 0 else s[i - 1]), row)
print('answer dp[8][8] =', dp[-1][-1], '-> the repeated subsequence abd: positions 1,3,7 and 2,5,8 (1-indexed)')

# seeded cross-check, len <= 7
cases = nz = 0
for _ in range(500):
    alpha = random.choice(['a', 'ab', 'abc'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(0, 7)))
    exp = brute(s)
    assert lrs(s) == lrs_table(s)[-1][-1] == memo(s) == exp, s
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a non-zero answer', nz)
cnt = 0
for L in range(0, 9):
    for bits in range(1 << L):
        s = format(bits, '0%db' % L) if L else ''
        if L <= 7:
            assert lrs(s) == brute(s)
        else:
            assert lrs(s) == lrs_table(s)[-1][-1] == memo(s)
        cnt += 1
print('exhaustive binary strings len 0..8 checked:', cnt)

# the condition matters: without it the answer is len(s) on every string; and the 'disjoint index sets' reading is a different problem
assert all(lcs_no_condition(''.join(random.choice('abc') for _ in range(L))) == L for L in range(0, 30))
diff = sum(brute(s) != brute_disjoint(s) for s in (''.join(random.choice('ab') for _ in range(random.randint(0, 7))) for _ in range(300)))
print("'aaa': stated definition", brute('aaa'), "| disjoint-index reading", brute_disjoint('aaa'), '| the two readings differ on', diff, 'of 300 random strings')

# edge cases and max size
assert lrs('a') == 0 and lrs('aa') == 1 and lrs('ab') == 0 and lrs('a' * 1000) == 999
big = ''.join(random.choice('ab') for _ in range(1000))
print('n = 1000 random binary string:', lrs(big))
per = lrs('abc' * 300)
assert per >= 897                      # s[3:] against s[:-3] is a valid pair (shift by 3), so at least n - 3
print("'abc' * 300 (n = 900):", per)
print('edge asserts passed')

# recursion limit (observed): the memoised suffix recursion nests up to about 2n frames
print('recursion limit', sys.getrecursionlimit())
for n in (200, 1000):
    w = 'a' * n
    try:
        print('memoised n = %d ->' % n, memo(w) == lrs(w), '(bottom-up gives', lrs(w), ')')
    except RecursionError:
        print('memoised n = %d -> RecursionError (bottom-up gives %d)' % (n, lrs(w)))
```

**Output (my run):**
```
example 'aabebcdd' -> 3 | without the i != j condition: 8
example 'abc' -> 0 | without the i != j condition: 3
example 'aaa' -> 2 | without the i != j condition: 3
example '' -> 0 | without the i != j condition: 0
example 'axxxy' -> 2 | without the i != j condition: 5
dp table for aabebcdd (rows i, columns j; match only if letters equal and i != j):
      -  a  a  b  e  b  c  d  d
  -  [0, 0, 0, 0, 0, 0, 0, 0, 0]
  a  [0, 0, 1, 1, 1, 1, 1, 1, 1]
  a  [0, 1, 1, 1, 1, 1, 1, 1, 1]
  b  [0, 1, 1, 1, 1, 2, 2, 2, 2]
  e  [0, 1, 1, 1, 1, 2, 2, 2, 2]
  b  [0, 1, 1, 2, 2, 2, 2, 2, 2]
  c  [0, 1, 1, 2, 2, 2, 2, 2, 2]
  d  [0, 1, 1, 2, 2, 2, 2, 2, 3]
  d  [0, 1, 1, 2, 2, 2, 2, 3, 3]
answer dp[8][8] = 3 -> the repeated subsequence abd: positions 1,3,7 and 2,5,8 (1-indexed)
cross-check cases 500 | with a non-zero answer 345
exhaustive binary strings len 0..8 checked: 511
'aaa': stated definition 2 | disjoint-index reading 1 | the two readings differ on 125 of 300 random strings
n = 1000 random binary string: 804
'abc' * 300 (n = 900): 897
edge asserts passed
recursion limit 1000
memoised n = 200 -> True (bottom-up gives 199 )
memoised n = 1000 -> RecursionError (bottom-up gives 999)
```

Reading the output:
- All five examples match the two-row DP, the table, the memoised recursion and the pair-of-sequences enumeration. The extra column on the example lines shows what you would get without the `i != j` test: always `len(s)` (5 for `'axxxy'`).
- 500 seeded random strings (len <= 7, alphabets of 1 to 3 letters; 345 with a non-zero answer) and all 511 binary strings of length 0 to 8 agree.
- The disjoint-index reading differs from the stated definition on `'aaa'` (1 versus 2) and on 125 of 300 random binary strings, so the stated rule matters.
- Recursion: a memoised version works on 200 equal letters but raises `RecursionError` at 1000 (default limit 1000, observation on Python 3.13), because the suffix recursion can nest about `2n` frames; the bottom-up version handles n = 1000 directly.

**Edge cases:**
- `''` and one letter: 0.
- All letters equal, length n: `n - 1` (shift by one).
- All distinct letters: 0.
- Two equal letters (`'aa'`): 1.
- `n = 1000`: a million cells; fine in two rows.

**Follow-ups:**
- "Why not require disjoint index sets?" That is a different problem (it is harder to state as a table and gives different answers, as the `'aaa'` case shows).
- "Return the subsequence?" Use the full table and walk back from `(n, n)`: on a match step diagonally and prepend the letter; otherwise step to the larger neighbour. State a tie rule.
- "Relation to LPS?" Longest palindromic subsequence is LCS of `s` with its REVERSE (Q7); here it is LCS of `s` with itself plus a condition.

**Common mistakes:**
- Forgetting `i != j` (answer `n`).
- Off-by-one between 0-indexed letters and the 1-indexed table: compare `s[i-1] == s[j-1]` together with `i != j` (do not write `s[i] == s[j]` against a table indexed from 1).
- Memoised recursion at n = 1000 (`RecursionError`).

### Q27 ⭐ 🟡 Paths whose sum is divisible by k, with a modulus. `grid` is an m x n list of lists (1 <= m, n <= 70) of integers in 0..100 and `k` is an integer with 1 <= k <= 50. Moves are right or down from the top-left to the bottom-right. Return the number of paths whose cell sum (both ends included) is divisible by k, modulo 10^9 + 7. State `dp[i][j][r]` = paths to (i, j) whose sum has remainder r, give the transition `(r + grid[i][j]) % k`, the base case and the time O(m*n*k); say why taking the modulus at every addition is safe for a counting DP, and why the remainder is tracked mod k and not the full sum. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) on small inputs. Example: grid=[[5, 2, 4], [3, 0, 5], [0, 7, 2]], k=3 -> 2; grid=[[0, 0]], k=5 -> 1; grid=[[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]], k=1 -> 10; grid=[[1, 1], [1, 1]], k=2 -> 0.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP with an extra dimension: the state carries the remainder of the sum modulo `k`. A counting DP, so the transitions add; and a modulus on the counts.

**Say this first (1 line):** "`dp[i][j][r]` is the number of paths to `(i, j)` whose sum is `r` mod `k`. Each cell shifts the remainder by `grid[i][j] % k`. The answer is `dp[m-1][n-1][0]`. I only need the remainder because divisibility by `k` depends on the sum mod `k` alone, and I reduce the counts mod 10^9 + 7 after each addition."

**Brute force:** Enumerate all `C(m+n-2, m-1)` right/down paths, add up the cells, count the sums divisible by `k`, reduce modulo 10^9 + 7. Exponential; the oracle for m, n <= 5.

**Optimal:**
- State: `dp[i][j][r]` = number of right/down paths from `(0, 0)` to `(i, j)` (both ends included) with `sum % k == r`.
- Transition: arriving at `(i, j)` from above or from the left with remainder `r` there gives remainder `(r + grid[i][j]) % k` here. So `dp[i][j][(r + v) % k] += dp[i-1][j][r] + dp[i][j-1][r]` with `v = grid[i][j] % k`. Nothing is overwritten from the same cell: each target remainder collects from different `r`, and the shift `r -> (r + v) % k` is a permutation.
- Base: `dp[0][0][grid[0][0] % k] = 1`, everything else 0 (not `dp[0][0][0]`; the start cell's value already counts).
- Answer: `dp[m-1][n-1][0]`.
- Why the remainder and not the full sum: `(a + b) % k` depends only on `a % k` and `b % k`, and the question asks only about divisibility. The full sum can be as large as 100 * 139 = 13,900 for a 70 x 70 grid, so about 13,901 values per cell instead of at most 50, a state space about 280 times larger for no benefit.
- Why the modulus is safe at every addition: a path count only ever gets additions of non-negative counts, with no subtraction, comparison or division of counts. And `(a + b) % M = ((a % M) + (b % M)) % M`, so reducing early gives the same final residue as reducing at the end. The code checks this on a 40 x 40 grid with `k = 7`: the exact count has 22 digits, and the version that reduces at every step equals `exact % MOD`. (A 70 x 70 all-zero grid has C(138, 69) paths, 41 digits, also checked.) The `% k` for remainders and `% (10**9 + 7)` for counts are two different moduli; do not mix them.
- Rolling rows: row `i` needs only row `i-1` and the cell to its left, so keep one list of `n` vectors of length `k`: O(n * k) space. The code does this; a 3D version is printed for the walk-through and cross-check.

**Complexity:** Time O(m * n * k) (at most 70 * 70 * 50 = 245,000 states, two transitions each), space O(n * k) with rolling rows (O(m * n * k) for the full 3D table).

**Dry run:** grid `[[5,2,4],[3,0,5],[0,7,2]]`, `k = 3`. Each cell is a vector `[r=0, r=1, r=2]`.
- `(0,0)`: value 5, `5 % 3 = 2`, so `[0, 0, 1]`.
- Row 0: `(0,1)` value 2: remainder `(2 + 2) % 3 = 1`, `[0, 1, 0]`; `(0,2)` value 4 (`1`): `(1 + 1) % 3 = 2`, `[0, 0, 1]`.
- Column 0: `(1,0)` value 3 (`0`): `[0, 0, 1]`; `(2,0)` value 0: `[0, 0, 1]`.
- `(1,1)` value 0: above `[0, 1, 0]` and left `[0, 0, 1]` add up to `[0, 1, 1]`.
- `(1,2)` value 5 (`2`): above `[0, 0, 1]` shifts by 2 to `[0, 1, 0]`; left `[0, 1, 1]` shifts to `[1, 1, 0]` (remainder 1 goes to 0, remainder 2 goes to 1). Sum `[1, 2, 0]`.
- `(2,1)` value 7 (`1`): above `[0, 1, 1]` shifts by 1 to `[1, 0, 1]`; left `[0, 0, 1]` shifts to `[1, 0, 0]`. Sum `[2, 0, 1]`.
- `(2,2)` value 2 (`2`): above `[1, 2, 0]` shifts by 2 to `[2, 0, 1]`; left `[2, 0, 1]` shifts to `[0, 1, 2]`. Sum `[2, 1, 3]`; its remainder-0 entry is 2.
- Answer 2.

**Code:**
```python
import random, itertools, sys, time
from math import comb

random.seed(27)
MOD = 10**9 + 7

def count_paths(grid, k, mod=MOD):
    """dp[j][r] = number of paths to (current row, j) whose sum has remainder r mod k. One row of k-vectors."""
    m, n = len(grid), len(grid[0])
    dp = [[0] * k for _ in range(n)]
    for i in range(m):
        new = [[0] * k for _ in range(n)]
        for j in range(n):
            v = grid[i][j] % k
            if i == 0 and j == 0:
                new[0][v] = 1                                   # base: the start cell alone, sum % k = grid[0][0] % k
                continue
            cell = new[j]
            for src in ((dp[j] if i else None), (new[j - 1] if j else None)):   # from above, from the left
                if src is None:
                    continue
                for r in range(k):
                    c = src[r]
                    if c:
                        t = (r + v) % k
                        cell[t] = (cell[t] + c) % mod if mod else cell[t] + c
        dp = new
    return dp[n - 1][0]

def count_paths_full(grid, k, mod=MOD):
    """3D table dp[i][j][r], the version in the statement (used for the printed walk-through)."""
    m, n = len(grid), len(grid[0])
    dp = [[[0] * k for _ in range(n)] for _ in range(m)]
    dp[0][0][grid[0][0] % k] = 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            v = grid[i][j] % k
            for r in range(k):
                tot = (dp[i - 1][j][r] if i else 0) + (dp[i][j - 1][r] if j else 0)
                if tot:
                    dp[i][j][(r + v) % k] = (dp[i][j][(r + v) % k] + tot) % mod if mod else dp[i][j][(r + v) % k] + tot
    return dp

def brute(grid, k):
    m, n = len(grid), len(grid[0]); cnt = 0
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        i = j = 0; tot = grid[0][0]
        for c in s:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]
        cnt += tot % k == 0
    return cnt % MOD

# examples
for grid, k, exp in [([[5, 2, 4], [3, 0, 5], [0, 7, 2]], 3, 2), ([[0, 0]], 5, 1),
                     ([[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]], 1, 10), ([[1, 1], [1, 1]], 2, 0)]:
    a, b, c = count_paths(grid, k), brute(grid, k), count_paths_full(grid, k)[-1][-1][0]
    assert a == b == c == exp, (grid, k, a, b, c)
    print('example', grid, 'k =', k, '->', a)

# hand table for example 1
grid, k = [[5, 2, 4], [3, 0, 5], [0, 7, 2]], 3
dp = count_paths_full(grid, k)
print('dp[i][j] = [paths with remainder 0, 1, 2] for grid', grid, 'k =', k)
for i in range(3):
    print('  ', [dp[i][j] for j in range(3)])
print('answer = dp[2][2][0] =', dp[2][2][0])

# seeded cross-check, m, n <= 5
cases = nz = 0
for _ in range(500):
    m, n = random.randint(1, 5), random.randint(1, 5)
    k = random.randint(1, 6)
    grid = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
    exp = brute(grid, k)
    assert count_paths(grid, k) == count_paths_full(grid, k)[-1][-1][0] == exp, (grid, k)
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a non-zero count', nz)

# the modulus: counts beyond 10^9+7 occur, and reducing after each addition equals reducing at the end (exact big-int run)
g = [[random.randint(0, 100) for _ in range(40)] for _ in range(40)]
exact = count_paths(g, 7, mod=None)
print('40 x 40, k = 7: exact count has', len(str(exact)), 'digits; mod result', count_paths(g, 7), '== exact % MOD:', count_paths(g, 7) == exact % MOD)
assert count_paths(g, 7) == exact % MOD and exact > MOD
ones = [[0] * 70 for _ in range(70)]
assert count_paths(ones, 1, mod=None) == comb(138, 69) and count_paths(ones, 1) == comb(138, 69) % MOD
print('70 x 70 all zeros, k = 1: all C(138, 69) paths:', comb(138, 69) % MOD, '(exact value has', len(str(comb(138, 69))), 'digits)')

# why remainder and not the full sum: the number of distinct sums is far larger than k
print('largest possible path sum at 70 x 70, cells <= 100:', 100 * (70 + 70 - 1), '-> up to', 100 * 139 + 1, 'sum values per cell versus k <= 50 remainders')

# edge cases and the maximum size
assert count_paths([[5]], 5) == 1 and count_paths([[5]], 3) == 0 and count_paths([[0]], 1) == 1
assert count_paths([[3, 4]], 7) == 1 and count_paths([[3, 4]], 5) == 0
big = [[random.randint(0, 100) for _ in range(70)] for _ in range(70)]
t0 = time.perf_counter(); r = count_paths(big, 50); t1 = time.perf_counter()
assert r == count_paths_full(big, 50)[-1][-1][0]
print('70 x 70, k = 50:', r, '(sandbox timing %.2f s)' % (t1 - t0))
print('recursion limit', sys.getrecursionlimit(), '| the DP is iterative; a memoised f(i, j, r) would nest m + n - 1 = 139 frames, also fine at this size')
print('edge asserts passed')
```

**Output (my run):**
```
example [[5, 2, 4], [3, 0, 5], [0, 7, 2]] k = 3 -> 2
example [[0, 0]] k = 5 -> 1
example [[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]] k = 1 -> 10
example [[1, 1], [1, 1]] k = 2 -> 0
dp[i][j] = [paths with remainder 0, 1, 2] for grid [[5, 2, 4], [3, 0, 5], [0, 7, 2]] k = 3
   [[0, 0, 1], [0, 1, 0], [0, 0, 1]]
   [[0, 0, 1], [0, 1, 1], [1, 2, 0]]
   [[0, 0, 1], [2, 0, 1], [2, 1, 3]]
answer = dp[2][2][0] = 2
cross-check cases 500 | with a non-zero count 362
40 x 40, k = 7: exact count has 22 digits; mod result 602190882 == exact % MOD: True
70 x 70 all zeros, k = 1: all C(138, 69) paths: 982546699 (exact value has 41 digits)
largest possible path sum at 70 x 70, cells <= 100: 13900 -> up to 13901 sum values per cell versus k <= 50 remainders
70 x 70, k = 50: 282366776 (sandbox timing 0.05 s)
recursion limit 1000 | the DP is iterative; a memoised f(i, j, r) would nest m + n - 1 = 139 frames, also fine at this size
edge asserts passed
```

Reading the output:
- All four examples match the rolling-row DP, the 3D table and the path enumeration. The printed table is the one traced above (each cell lists the counts for remainders 0, 1, 2).
- 500 seeded random cases (m, n <= 5, `k` 1 to 6, values 0..100; 362 with a non-zero answer) agree.
- The modulus check: for a 40 x 40 grid the exact count is a 22-digit number and the reduce-every-step result equals `exact % MOD`; for 70 x 70 zeros the reduced result is C(138, 69) mod 10^9 + 7. So counts above the modulus do occur at the stated sizes, and early reduction is exact.
- 70 x 70 with `k = 50` takes a few hundredths of a second here (sandbox timing). The code is iterative, so no recursion limit applies; a memoised `f(i, j, r)` would nest only `m + n - 1 = 139` frames anyway.

**Edge cases:**
- `k = 1`: every path counts (the answer is the number of paths, reduced).
- A 1 x 1 grid: 1 when `grid[0][0] % k == 0`, else 0.
- Single row or column: 0 or 1.
- Zeros everywhere: all paths count for every `k`.
- Large `k` close to the sums: remainders are just the values themselves; no special case.

**Follow-ups:**
- "Why not track the sum?" The state space grows by a factor of about 280 here and `k` already captures everything the question asks.
- "Return the actual number, not mod?" Python integers are unbounded: drop the modulus (the code's `mod=None` path). The count for 70 x 70 has 41 digits.
- "Moves right, down and diagonal?" Add a third predecessor; the shape is the same.

**Common mistakes:**
- Base `dp[0][0][0] = 1` (forgets the start cell's own value).
- Taking `% k` of the count or `% MOD` of the remainder (mixing the two moduli).
- Updating the remainder dimension in place so a state feeds itself within the same cell.
- Not reducing the counts, which is harmless in Python for correctness but makes numbers huge and slow.
- Skipping the `% k` on the new remainder index (`r + v` can reach `2k - 2`, so the list index runs out or lands on the wrong slot).

### Q28 ⭐ 🟡 Count the minimum-cost paths (counting versus optimising). `grid` is an m x n list of lists (1 <= m, n <= 100) of integers in 0..9. Moves are right or down from the top-left to the bottom-right. Return `[best, ways]`: the minimum path sum and the number of distinct paths that reach it, modulo 10^9 + 7. Keep two tables (cost and count), say how the count merges when both predecessors tie, when it is taken from one predecessor and when it is added, and why the modulus is applied to the count only, never to the cost (comparisons need the true value). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) on small inputs. Example: grid=[[1, 3, 1], [1, 5, 1], [4, 2, 1]] -> [7, 1]; grid=[[0, 0], [0, 0]] -> [0, 2]; grid=[[7]] -> [7, 1]; grid=[[1, 2], [2, 1]] -> [4, 2].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 2D grid DP with a second table. One table optimises (minimum cost into each cell), one counts (how many paths achieve that minimum). It is "optimise, then count the optimal ones" on a DAG.

**Say this first (1 line):** "Two tables: `cost[i][j]` is the cheapest sum of a path into the cell, `ways[i][j]` is how many paths reach that cost; ties add the counts, a strictly cheaper predecessor hands over its count, and only the count is taken modulo 10^9 + 7. O(m*n) time, O(n) space."

**Brute force:** Enumerate every right/down path: choose which `m + n - 2` moves are Down, that is C(m+n-2, m-1) paths (70 for 5 x 5, but about 10^58 for 100 x 100). Take the minimum and count how often it occurs. It is the oracle for m, n <= 5.

**Optimal:**
- State: `cost[i][j]` = minimum sum over paths from (0,0) to (i,j) inclusive; `ways[i][j]` = number of paths that achieve exactly that sum (mod p).
- Transition: the last move came from above or from the left. `best = min(cost[i-1][j], cost[i][j-1])`, then `cost[i][j] = best + grid[i][j]`.
- Count merge, three cases:
  - Both predecessors have cost == best (a tie): `ways = ways[up] + ways[left]`. Both families of paths are optimal and disjoint (different last move).
  - Exactly one predecessor has cost == best: `ways` is copied from that one. The other predecessor's paths are strictly worse into this cell, so they do not count.
  - Border cell (first row or column): only one predecessor exists, so the count is copied from it.
- Base: `cost[0][0] = grid[0][0]`, `ways[0][0] = 1` (the empty path is one path). Missing predecessors are treated as cost infinity, which never ties with a real number.
- Why the modulus touches the count only: the count is compared with nothing, it is only added, and it grows like a binomial coefficient (the all-zero 100 x 100 grid has C(198,99), a 59-digit number of optimal paths, hence the modulus). The cost is compared with `min` and `==` at every cell, so it must stay the true value. A reduced cost can make a worse path look cheaper or break a tie. In this prompt the cost is at most 9 * 199 = 1791, far below 10^9 + 7, so reducing it would happen to be harmless here; the rule matters as soon as values are large, and the code shows the damage with an artificial modulus of 5.
- Memoised version: `f(i, j)` returns the best `(cost, ways)` of a path from (i,j) to the end (the other direction). Its recursion nests m + n - 1 deep, at most 199 for 100 x 100, which is under CPython's default limit of 1000 (observed on 3.13: the 100 x 100 run is fine). If the grid size were not capped, a depth of m + n - 1 above the limit would fail (Q29 measures exactly that), so bottom-up is the safe default.
- Space: row i reads row i-1 (same column) and the cell to its left, so one row of `cost` and one row of `ways`, updated left to right, is enough: O(n).

**Complexity:** Time O(m*n), each cell does O(1) work. Space O(m*n) for two full tables, O(n) with the single-row version. Reconstructing one optimal path would need the full table (or a parent pointer), counting does not.

**Dry run:** the first example, `grid = [[1,3,1],[1,5,1],[4,2,1]]`.

| cell | cost | ways | why |
|---|---|---|---|
| (0,0) | 1 | 1 | base |
| (0,1), (0,2) | 4, 5 | 1, 1 | first row, one predecessor |
| (1,0), (2,0) | 2, 6 | 1, 1 | first column |
| (1,1) | 7 | 1 | up 4, left 2: left is strictly cheaper, copy its count, 2 + 5 = 7 |
| (1,2) | 6 | 1 | up 5, left 7: up wins, 5 + 1 = 6 |
| (2,1) | 8 | 1 | up 7, left 6: left wins, 6 + 2 = 8 |
| (2,2) | 7 | 1 | up 6, left 8: up wins, 6 + 1 = 7 |

Answer `[7, 1]`. No tie occurs here, so the ways table is all ones. A tie appears in the fourth example `[[1,2],[2,1]]`: both predecessors of (1,1) cost 3, so `ways = 1 + 1 = 2` and the answer is `[4, 2]` (the run prints that table).

**Code:**
```python
import itertools, random
from math import comb

random.seed(2801)
MOD = 10**9 + 7
INF = float("inf")


def solve_tables(grid):
    """Bottom-up with two full tables: cost[i][j], ways[i][j] (best path into (i,j))."""
    m, n = len(grid), len(grid[0])
    cost = [[INF] * n for _ in range(m)]
    ways = [[0] * n for _ in range(m)]
    cost[0][0], ways[0][0] = grid[0][0], 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            up = cost[i - 1][j] if i else INF
            left = cost[i][j - 1] if j else INF
            best = min(up, left)
            w = 0
            if up == best:
                w += ways[i - 1][j]
            if left == best:
                w += ways[i][j - 1]
            cost[i][j] = best + grid[i][j]      # true value, never reduced
            ways[i][j] = w % MOD                # only the count is reduced
    return [cost[-1][-1], ways[-1][-1]], cost, ways


def solve(grid):
    return solve_tables(grid)[0]


def solve_one_row(grid):
    """Space O(n): one row of cost and one row of ways, updated left to right."""
    m, n = len(grid), len(grid[0])
    cost, ways = [INF] * n, [0] * n
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                cost[0], ways[0] = grid[0][0], 1
                continue
            up = cost[j] if i else INF            # still holds row i-1
            left = cost[j - 1] if j else INF      # already row i
            best = min(up, left)
            w = (ways[j] if up == best else 0) + (ways[j - 1] if j and left == best else 0)
            cost[j], ways[j] = best + grid[i][j], w % MOD
    return [cost[-1], ways[-1]]


def solve_memo(grid):
    """Top-down, the other direction: best (cost, ways) of a path from (i,j) to the end."""
    from functools import lru_cache
    m, n = len(grid), len(grid[0])

    @lru_cache(maxsize=None)
    def f(i, j):
        if i == m - 1 and j == n - 1:
            return (grid[i][j], 1)
        opts = []
        if i + 1 < m:
            opts.append(f(i + 1, j))
        if j + 1 < n:
            opts.append(f(i, j + 1))
        best = min(c for c, _ in opts)
        return (grid[i][j] + best, sum(w for c, w in opts if c == best) % MOD)

    return list(f(0, 0))


def brute(grid):
    """Enumerate every path: choose which of the m+n-2 moves are Down."""
    m, n = len(grid), len(grid[0])
    totals = []
    for downs in itertools.combinations(range(m + n - 2), m - 1):
        d = set(downs)
        i = j = 0
        tot = grid[0][0]
        for step in range(m + n - 2):
            if step in d:
                i += 1
            else:
                j += 1
            tot += grid[i][j]
        totals.append(tot)
    best = min(totals)
    return [best, totals.count(best) % MOD]


# ---- prompt examples
ex = [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], [7, 1]), ([[0, 0], [0, 0]], [0, 2]),
      ([[7]], [7, 1]), ([[1, 2], [2, 1]], [4, 2])]
for g, want in ex:
    assert solve(g) == solve_one_row(g) == solve_memo(g) == brute(g) == want, g
print("prompt examples OK")

# ---- table walk-through on example 1
res, cost, ways = solve_tables(ex[0][0])
print("grid  ", ex[0][0])
print("cost  ", cost)
print("ways  ", ways)
print("answer", res)
res2, cost2, ways2 = solve_tables(ex[3][0])
print("tie grid", ex[3][0], "cost", cost2, "ways", ways2, "answer", res2)

# ---- seeded cross-check against enumerating every path (m, n <= 5)
checked = ties = 0
for t in range(600):
    m, n = random.randint(1, 5), random.randint(1, 5)
    hi = random.choice([1, 2, 9])                 # small values force many ties
    g = [[random.randint(0, hi) for _ in range(n)] for _ in range(m)]
    want = brute(g)
    assert solve(g) == solve_one_row(g) == solve_memo(g) == want, (g, want)
    checked += 1
    ties += want[1] > 1
print("random cross-check:", checked, "grids agree;", ties, "had more than one optimal path")

# ---- why the count needs the modulus: all-zero 100 x 100, every path is optimal
big = [[0] * 100 for _ in range(100)]
r = solve(big)
true_count = comb(198, 99)
assert r == [0, true_count % MOD] == solve_one_row(big) == solve_memo(big)
print("100x100 zeros: cost", r[0], "| true count has", len(str(true_count)), "digits | mod ->", r[1])
assert true_count > MOD
print("largest possible cost 9*199 =", 9 * 199, "(far below the modulus)")

# ---- recursion depth of the memoised version is m + n - 1 (199 at the limit size)
import sys
print("recursion limit", sys.getrecursionlimit(), "| memo depth at 100x100 is", 100 + 100 - 1, "-> fine")

# ---- wrong variants, counted on the same random grids
def wrong_add_always(grid):
    m, n = len(grid), len(grid[0])
    cost = [[0] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == j == 0:
                cost[0][0], ways[0][0] = grid[0][0], 1; continue
            cands = ([(cost[i-1][j], ways[i-1][j])] if i else []) + ([(cost[i][j-1], ways[i][j-1])] if j else [])
            cost[i][j] = min(c for c, _ in cands) + grid[i][j]
            ways[i][j] = sum(w for _, w in cands) % MOD         # ignores which predecessor is cheaper
    return [cost[-1][-1], ways[-1][-1]]

def wrong_first_only(grid):
    m, n = len(grid), len(grid[0])
    cost = [[0] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == j == 0:
                cost[0][0], ways[0][0] = grid[0][0], 1; continue
            cands = ([(cost[i-1][j], ways[i-1][j])] if i else []) + ([(cost[i][j-1], ways[i][j-1])] if j else [])
            c, w = min(cands, key=lambda x: x[0])               # min() keeps the first on a tie: drops the other
            cost[i][j] = c + grid[i][j]; ways[i][j] = w
    return [cost[-1][-1], ways[-1][-1]]

def wrong_cost_mod(grid, p=5):
    """Artificial small modulus on the cost too: comparisons then lie."""
    m, n = len(grid), len(grid[0])
    cost = [[0] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == j == 0:
                cost[0][0], ways[0][0] = grid[0][0] % p, 1; continue
            cands = ([(cost[i-1][j], ways[i-1][j])] if i else []) + ([(cost[i][j-1], ways[i][j-1])] if j else [])
            b = min(c for c, _ in cands)
            cost[i][j] = (b + grid[i][j]) % p
            ways[i][j] = sum(w for c, w in cands if c == b) % MOD
    return [cost[-1][-1], ways[-1][-1]]

rnd = random.Random(2802)
bad = {"add both always": 0, "first on tie only": 0, "cost reduced (mod 5)": 0}
N = 500
for _ in range(N):
    m, n = rnd.randint(2, 5), rnd.randint(2, 5)
    g = [[rnd.randint(0, 3) for _ in range(n)] for _ in range(m)]
    want = brute(g)
    bad["add both always"] += wrong_add_always(g) != want
    bad["first on tie only"] += wrong_first_only(g) != want
    bad["cost reduced (mod 5)"] += wrong_cost_mod(g) != want
print("wrong variants differing from the oracle out of", N, ":", bad)

# ---- edge cases
assert solve([[0]]) == [0, 1]
assert solve([[5] * 7]) == [35, 1] and solve([[5]] * 7) == [35, 1]       # one row / one column: one path
assert solve([[9] * 100 for _ in range(100)]) == [9 * 199, comb(198, 99) % MOD]
print("edge cases OK")
```

**Output (my run):**
```
prompt examples OK
grid   [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
cost   [[1, 4, 5], [2, 7, 6], [6, 8, 7]]
ways   [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
answer [7, 1]
tie grid [[1, 2], [2, 1]] cost [[1, 3], [3, 4]] ways [[1, 1], [1, 2]] answer [4, 2]
random cross-check: 600 grids agree; 176 had more than one optimal path
100x100 zeros: cost 0 | true count has 59 digits | mod -> 690285631
largest possible cost 9*199 = 1791 (far below the modulus)
recursion limit 1000 | memo depth at 100x100 is 199 -> fine
wrong variants differing from the oracle out of 500 : {'add both always': 485, 'first on tie only': 214, 'cost reduced (mod 5)': 450}
edge cases OK
```

**Edge cases:**
- 1 x 1: the cost is the single value and the count is 1.
- A single row or a single column: exactly one path, count 1.
- All zeros: every path ties, the count is C(m+n-2, m-1) mod p (the code checks 100 x 100 against `math.comb`).
- A true count that is a multiple of 10^9 + 7 would show as 0 after the modulus, so never use `ways == 0` to mean "unreachable" (here every cell is reachable, so it does not come up).
- Compare costs before adding the cell value: adding `grid[i][j]` to both candidates does not change which is smaller, but the tie test must use the predecessors' costs.

**Follow-ups:**
- Print one optimal path? Keep the full cost table and walk back from the end, going to a predecessor whose cost equals `cost[i][j] - grid[i][j]`; for a fixed tie rule choose up or left consistently.
- Obstacles? Treat a blocked cell as cost infinity and count 0; its neighbours then read infinity and never tie.
- Count paths with sum divisible by k (not minimum)? Then the state grows by the remainder; counting all paths needs no cost table at all.

**Common mistakes:**
- Adding both predecessors' counts always (wrong 485 times in 500 random grids in the code).
- Taking the count from the first minimum only and losing the tied one (wrong 214 of 500).
- Reducing the cost modulo the prime (or any modulus): comparisons lie (450 of 500 wrong with an artificial modulus of 5; harmless here only because 10^9 + 7 is far above the cost bound 1791).
- Using `<=` instead of `==` for the count test: a strictly worse predecessor must contribute nothing.

### Q29 ⭐ 🟡 Top-down grid DP: cache size and recursion depth. For a grid with `m` rows and `n` columns (1 <= m, n <= 1500) and a list `blocked` of at most 10^4 distinct cells `[r, c]` (any cell may be blocked, including the start and the end), a memoised function `f(i, j)` decorated with `functools.lru_cache(maxsize=None)` (the tuple `(i, j)` is the cache key) is evaluated as follows: it is only ever called on in-bounds cells; a blocked cell returns 0; the bottom-right cell returns 1; any other cell returns `f(i+1, j) + f(i, j+1)` over its in-bounds neighbours. The program calls `f(0, 0)` once. Return `[paths, entries, depth]`: the value of `f(0, 0)`, the number of distinct cells for which `f` was called (the cache size afterwards, blocked cells that were called included) and the maximum nesting depth of calls (the call `f(0, 0)` itself is depth 1). Compute all three WITHOUT recursion (a forward table over reachable cells), then explain which of the three would make the recursive version raise RecursionError: with no blocked cells and m = n = 600 the depth is 1199, past CPython's default limit of 1000. Also say why a cache key must be hashable (tuple, not list). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an instrumented lru_cache recursion on small grids (m, n <= 12) on small inputs. Example: m=3, n=3, blocked=[] -> [6, 9, 5]; m=3, n=3, blocked=[[1, 1]] -> [2, 9, 5]; m=2, n=4, blocked=[[0, 0]] -> [0, 1, 1]; m=1, n=1, blocked=[] -> [1, 1, 1]; m=4, n=3, blocked=[[0, 1], [1, 0]] -> [0, 3, 2]; m=600, n=600, blocked=[] -> [99210086628716100259395166354279999048776028950823599117066277392523790644939432481289087348273094564714767859517126896912283379860500428775241021388504367225251065302219729434487397626171671117422766919562944453912539279922435761841185334794928872418804619319119133993547860003208493900609497280018766204610934683472222291824312173152433569864759061895320000, 360000, 1199].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; behaviour verified by running Python 3.13) | 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened)

**Pattern:** Top-down grid DP with `lru_cache`, analysed instead of just run. Three numbers describe one memoised recursion: its answer, its cache size and its nesting depth. Only one of them can break the program.

**Say this first (1 line):** "Every call at cell (i, j) sits at depth i + j + 1 because each call moves one step right or down; the cache holds the cells that some call reaches, and the answer is a forward path count. The depth is what raises RecursionError, not the cache size and not the (huge) answer."

**Brute force:** Run the real recursion with an instrumented `lru_cache` (a depth counter incremented on entry and decremented in `finally`, and `cache_info().currsize` afterwards). Exact, but it fails on big grids with RecursionError, and it is the oracle for m, n <= 12.

**Optimal:** No recursion at all, a forward table row by row.
- `called[i][j]`: some call of `f` reaches (i, j). (0,0) is called; (i, j) is called when the cell above or the cell to its left is **expanded**.
- `expanded[i][j]` = called, not blocked and not the bottom-right cell (those two return immediately and call nothing).
- `entries` = number of called cells. Blocked cells that are called count (they enter the cache), and so does a blocked end cell. Cells behind a wall are never called, so they are not counted.
- `depth` = max over called cells of `i + j + 1`. Why: the call tree starts at depth 1 for (0,0), and every call goes to (i+1, j) or (i, j+1), so a call at cell (i, j) is always exactly at depth i + j + 1, however it got there. The deepest call is therefore the called cell with the largest i + j.
- `paths`: `w[0][0] = 1` if (0,0) is not blocked; for other cells `w = w[above] + w[left]` and `w = 0` for a blocked cell. This counts right/down paths through open cells, which equals `f(0,0)`: `f` sums the two neighbours, a blocked cell returns 0, the end returns 1. The count is the exact integer (no modulus in this prompt); Python integers have no overflow.
- Only two rows of `w` and of the `expanded` flags are kept, so memory is O(n).
- Which one raises RecursionError: the **depth**. With no blocked cells and m = n = 600 the depth is 1199, past the default limit of 1000. The path count is a 359-digit integer, which Python handles fine, and 360,000 cache entries are only memory, not stack. In the sandbox on Python 3.13 the memoised 400 x 400 run (depth 799) worked and 600 x 600 raised RecursionError; the exact failing depth depends on version and call path, so treat the pass/fail as an observation, not a rule, and keep clear of the boundary. The fix is bottom-up, not `sys.setrecursionlimit`.
- Cache key must be hashable: the cache is a dict, and the key `(i, j)` is hashed. A tuple is hashable, a list is not (`lru_cache` raises `TypeError: unhashable type: 'list'`, shown in the code). Hashable also means immutable by convention: a key that could change after insertion would corrupt lookups.

**Complexity:** Forward table: time O(m*n) cell visits (each adds two integers, which for the big counts costs O(digits)), space O(n) with two rolling rows. Blocked cells are looked up in a per-row set, built in O(B), B <= 10^4. The recursion would be O(m*n) time too, O(m*n) cache, but O(m+n) stack depth, and that stack depth is the problem.

**Dry run:** `m = 3, n = 3, blocked = []`, expected `[6, 9, 5]`.

| cell depth `i+j+1` | | | paths from start `w` | | |
|---|---|---|---|---|---|
| 1 | 2 | 3 | 1 | 1 | 1 |
| 2 | 3 | 4 | 1 | 2 | 3 |
| 3 | 4 | 5 | 1 | 3 | 6 |

- All 9 cells are called, so `entries = 9`.
- The largest depth is at (2,2): 2 + 2 + 1 = 5.
- `w[2][2] = 3 + 3 = 6` (above 3, left 3).

Second example, `blocked = [[1,1]]`: the centre is called (entries still 9) but returns 0 and calls nothing; `w` becomes `[1,1,1],[1,0,1],[1,1,2]`, so paths = 2; depth is still 5 because (2,2) is reached through (0,2) then (1,2). Third example `m=2, n=4, blocked=[[0,0]]`: the start is blocked, so `f(0,0)` returns 0 straight away: entries 1, depth 1, paths 0.

**Code:**
```python
import random, sys, time
from functools import lru_cache
from math import comb

random.seed(2901)


def stats_forward(m, n, blocked):
    """[paths, entries, depth] with NO recursion: a forward table, one row at a time.
    called = the cell is reached by some call of f; expanded = called, open and not the end,
    so it calls its right/down neighbours. w = number of right/down paths from (0,0)."""
    rows = {}
    for r, c in blocked:
        rows.setdefault(r, set()).add(c)
    w_prev = [0] * n
    ex_prev = [False] * n                    # expanded flags of the previous row
    entries, depth = 0, 1
    for i in range(m):
        bl = rows.get(i, ())
        w_cur = [0] * n
        ex_cur = [False] * n
        last = -1                            # last called column in this row
        for j in range(n):
            called = (i == 0 and j == 0) or (i > 0 and ex_prev[j]) or (j > 0 and ex_cur[j - 1])
            if not called:
                continue
            entries += 1
            if i + j + 1 > depth:
                depth = i + j + 1
            if j in bl:
                continue                     # blocked: f returns 0, calls nothing, w stays 0
            ex_cur[j] = not (i == m - 1 and j == n - 1)
        for j in range(n):
            if j in bl:
                continue
            if i == 0 and j == 0:
                w_cur[0] = 1
            else:
                w_cur[j] = (w_prev[j] if i else 0) + (w_cur[j - 1] if j else 0)
        w_prev, ex_prev = w_cur, ex_cur
    return [w_prev[n - 1], entries, depth]


def stats_recursive(m, n, blocked):
    """Oracle: the real lru_cache recursion, instrumented for depth and cache size."""
    bl = {(r, c) for r, c in blocked}
    st = {"now": 0, "max": 0}

    @lru_cache(maxsize=None)
    def f(i, j):
        st["now"] += 1
        st["max"] = max(st["max"], st["now"])
        try:
            if (i, j) in bl:
                return 0
            if (i, j) == (m - 1, n - 1):
                return 1
            total = 0
            if i + 1 < m:
                total += f(i + 1, j)
            if j + 1 < n:
                total += f(i, j + 1)
            return total
        finally:
            st["now"] -= 1

    r = f(0, 0)
    return [r, f.cache_info().currsize, st["max"]]


# ---- prompt examples (the 600 x 600 one is checked against C(1198, 599) as well)
ex = [(3, 3, [], [6, 9, 5]), (3, 3, [[1, 1]], [2, 9, 5]), (2, 4, [[0, 0]], [0, 1, 1]),
      (1, 1, [], [1, 1, 1]), (4, 3, [[0, 1], [1, 0]], [0, 3, 2])]
for m, n, b, want in ex:
    assert stats_forward(m, n, b) == stats_recursive(m, n, b) == want, (m, n, b)
r = stats_forward(600, 600, [])
assert r == [comb(1198, 599), 360000, 1199]
print("examples OK; 600x600 ->", len(str(r[0])), "digit path count,", r[1], "entries, depth", r[2])

# ---- walk-through on the first example: which cells are called, path counts, depth = i + j + 1
m, n = 3, 3
print("3x3 no blocks: depth of a call at (i,j) is i+j+1")
for i in range(m):
    print("  ", [i + j + 1 for j in range(n)], "  paths-from-start", [comb(i + j, i) for j in range(n)])
print("  forward answer", stats_forward(3, 3, []))

# ---- seeded cross-check against the instrumented recursion, m, n <= 12
cnt = zero = 0
for _ in range(1500):
    m, n = random.randint(1, 12), random.randint(1, 12)
    cells = [[r, c] for r in range(m) for c in range(n)]
    k = random.randint(0, min(len(cells), random.choice([0, 3, m * n // 3])))
    blocked = random.sample(cells, k)
    got, want = stats_forward(m, n, blocked), stats_recursive(m, n, blocked)
    assert got == want, (m, n, blocked, got, want)
    cnt += 1
    zero += got[0] == 0
print("random cross-check:", cnt, "cases agree;", zero, "of them have 0 paths")

# ---- claim: every call at cell (i, j) sits at depth i + j + 1, so depth = 1 + max(i+j) over called cells.
# Tested through the instrumented oracle on cases with a blocked wall that cuts the grid short.
r = stats_recursive(10, 10, [[0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0]])
print("anti-diagonal wall at i+j=5 on 10x10 (all 6 cells blocked):", r, "-> depth 6 = 5 + 1")
assert r == [0, 21, 6] == stats_forward(10, 10, [[0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0]])

# ---- what actually raises RecursionError: depth, not path count and not cache size
print("default recursion limit:", sys.getrecursionlimit())
for size in (400, 600):
    try:
        out = stats_recursive(size, size, [])
        print(f"  memoised {size}x{size}: depth {out[2]}, entries {out[1]} -> ran fine")
    except RecursionError:
        print(f"  memoised {size}x{size}: expected depth {2 * size - 1}, entries 360000 -> RecursionError")

# ---- hashable key: a tuple works, a list does not
@lru_cache(maxsize=None)
def g(cell):
    return sum(cell)
print("tuple key:", g((1, 2)))
try:
    g([1, 2])
except TypeError as e:
    print("list key ->", type(e).__name__ + ":", e)

# ---- size limit of the prompt: forward table, 1500 x 1500 with 10^4 blocked cells (timing is sandbox-only)
rng = random.Random(2902)
blocked = [[r // 1500, r % 1500] for r in rng.sample(range(1500 * 1500), 10**4)]
t0 = time.perf_counter()
res = stats_forward(1500, 1500, blocked)
dt = time.perf_counter() - t0
print("1500x1500, 10^4 blocked: paths has", len(str(res[0])), "digits (or 0 if blocked start/end),",
      "entries", res[1], "depth", res[2], f"[sandbox time {dt:.1f}s]")

# ---- edge cases
assert stats_forward(1, 1, [[0, 0]]) == [0, 1, 1] == stats_recursive(1, 1, [[0, 0]])
assert stats_forward(2, 2, [[1, 1]]) == [0, 4, 3] == stats_recursive(2, 2, [[1, 1]])     # end blocked: still called
assert stats_forward(1, 7, []) == [1, 7, 7]                                              # one row: a chain
print("edge cases OK")
```

**Output (my run):**
```
examples OK; 600x600 -> 359 digit path count, 360000 entries, depth 1199
3x3 no blocks: depth of a call at (i,j) is i+j+1
   [1, 2, 3]   paths-from-start [1, 1, 1]
   [2, 3, 4]   paths-from-start [1, 2, 3]
   [3, 4, 5]   paths-from-start [1, 3, 6]
  forward answer [6, 9, 5]
random cross-check: 1500 cases agree; 364 of them have 0 paths
anti-diagonal wall at i+j=5 on 10x10 (all 6 cells blocked): [0, 21, 6] -> depth 6 = 5 + 1
default recursion limit: 1000
  memoised 400x400: depth 799, entries 160000 -> ran fine
  memoised 600x600: expected depth 1199, entries 360000 -> RecursionError
tuple key: 3
list key -> TypeError: unhashable type: 'list'
1500x1500, 10^4 blocked: paths has 895 digits (or 0 if blocked start/end), entries 2238582 depth 2999 [sandbox time 0.8s]
edge cases OK
```

**Edge cases:**
- Start blocked: answer `[0, 1, 1]`, no further cells are called.
- End blocked but start open: the end is still called (it counts in `entries`) and returns 0 (`[0, 4, 3]` for 2 x 2 in the code).
- A wall across an anti-diagonal: the cells behind it are never called, so `entries` and `depth` are smaller than in the open grid (21 entries, depth 6 in the code's 10 x 10 wall example).
- One row or one column: a straight chain, depth m + n - 1 = the number of cells.
- 1 x 1: `[1, 1, 1]`, or `[0, 1, 1]` when the single cell is blocked.
- The blocked list may include the end cell; membership is checked before the end test.

**Follow-ups:**
- What about the cache size at 1500 x 1500? Up to 2.25 million tuple entries (the code's 10^4-blocked run has 2,238,582 called cells); the forward version with two rows holds none of them.
- Does `sys.setrecursionlimit(10**6)` fix it? It may let the recursion run, but a very deep recursion risks exhausting the real C stack (a crash, not a clean exception), which I did not test here; the portable fix is the loop.
- How would you add a modulus? Reduce `w` after each addition if a modulus is requested; it changes nothing about depth or entries.

**Common mistakes:**
- Blaming the cache size or the big integer for RecursionError. Only the nesting depth counts.
- Counting a blocked called cell out of `entries`, or counting cells behind a wall.
- Saying depth = m * n; it is m + n - 1 at most (1199 for 600 x 600), not 360,000.
- Using a list `[i, j]` as the key, which raises `TypeError`.
- Forgetting that a blocked end cell returns 0 before the end test (blocked is checked first).

### Q30 ⭐ 🟡 Minimum cost to cut a stick. A stick has length `n` (2 <= n <= 10^6) and `cuts` lists distinct integer positions strictly inside it (0 <= len(cuts) <= 100, each in 1..n-1). You may make the cuts in any order. One cut costs the length of the piece being cut; return the minimum total cost to make all cuts (0 when there are no cuts). Sort the cut positions and add 0 and n as boundary points, define `dp[l][r]` as the cost to make all cuts strictly between boundary points l and r, and explain why 'which cut comes FIRST in the interval' is the right choice here (the same shape as burst balloons with the last-burst view). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every order of the cuts (len(cuts) <= 6) on small inputs. Example: n=7, cuts=[1, 3, 4, 5] -> 16; n=9, cuts=[5, 6, 1, 4, 2] -> 22; n=10, cuts=[] -> 0; n=10, cuts=[5] -> 10.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP over boundary points. The state is a pair of boundaries (l, r), smaller intervals are solved first, and the transition scans every split point, so it is O(k^3) for k boundary points.

**Say this first (1 line):** "Sort the cuts, add 0 and n, let `dp[l][r]` be the cheapest way to make every cut strictly between points l and r, and choose which cut comes FIRST in that piece: it costs the whole piece, `points[r] - points[l]`, and leaves two independent sub-intervals."

**Brute force:** Try every order of the cuts: `len(cuts)!` orders (720 for 6 cuts), simulate the pieces and add the length of the piece each cut lands in. It is the oracle for at most 6 cuts, and exponential beyond that.

**Optimal:**
- Points: `pts = [0] + sorted(cuts) + [n]`, k = len(cuts) + 2 points. The cut positions are the only things that matter; n itself (up to 10^6) is never iterated.
- State: `dp[l][r]` (l < r) = minimum total cost to make all cuts strictly between `pts[l]` and `pts[r]`, assuming the piece `[pts[l], pts[r]]` exists as one stick.
- Base: `dp[l][l+1] = 0` (no cut inside) and the whole table starts at 0.
- Transition: pick the first cut m (`l < m < r`) in this piece. It costs the length of the piece, `pts[r] - pts[l]`, and then the two new pieces are independent: `dp[l][r] = pts[r] - pts[l] + min over m of (dp[l][m] + dp[m][r])`.
- Why FIRST and not last: the first cut in a piece has a known cost, the full length, no matter what else happens. If you chose the last cut instead, the piece it cuts is bounded by the nearest cuts already made, which are not determined by (l, r), so the cost would not be a function of the state. (In burst balloons it is the other way round: the first burst changes neighbours, so you think of the last burst, whose neighbours are the fixed ends. Same interval shape, opposite time direction.)
- Order of filling: increasing gap `r - l`, because `dp[l][r]` reads `dp[l][m]` and `dp[m][r]` with smaller gaps.
- Answer: `dp[0][k-1]`; no cuts gives k = 2 and 0.
- Memoised version: `f(l, r)` with `lru_cache`; its recursion depth is at most k <= 102, so it is safe at default limit 1000 (the code runs the largest size, 100 cuts, with the memo and gets the same answer). No setrecursionlimit is needed here.
- Space: the full triangle is read by every cell (`dp[l][m]` and `dp[m][r]` for all m), so there is no simple 1D reduction; O(k^2) memory is fine for k <= 102. (Knuth's optimisation could bring O(k^3) to O(k^2) time, not needed here and not checked.)

**Complexity:** Time O(k^3): about k^2/2 intervals times up to k split points (exactly C(k,3) inner steps, 171,700 for k = 102). Space O(k^2). Independent of n.

**Dry run:** `n = 7, cuts = [1,3,4,5]`, points `[0,1,3,4,5,7]` (indices 0..5). Entry dp[l][r], width = r - l:

| l \ r | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| 0 | 3 | 7 | 10 | 16 |
| 1 |  | 3 | 6 | 12 |
| 2 |  |  | 2 | 6 |
| 3 |  |  |  | 3 |

(entries with r = l + 1 are 0 and omitted.)
- `dp[0][2]` (cut at 1 inside 0..3): the only cut is 1, cost 3 - 0 = 3.
- `dp[2][4]` (3..5, cut at 4): cost 2. `dp[3][5]` (4..7, cut at 5): cost 3.
- `dp[0][5]` (whole stick, length 7): try first cut m = 1: 0 + 12, m = 2: 3 + 6, m = 3: 7 + 3, m = 4: 10 + 0. The minimum of the sums is 9, so the cost is 7 + 9 = 16, which matches the prompt. (m = 2 means cutting at 3 first, then 1 on the left piece 0..3 for 3, and 4 then 5 on 3..7 for 6.)
- Costs over all 24 orders range from 16 to 20, so order really matters.

**Code:**
```python
import itertools, random, sys, time
from functools import lru_cache

random.seed(3001)


def solve(n, cuts):
    """Bottom-up interval DP over boundary points. dp[l][r] = cost to make every cut strictly
    between points[l] and points[r]; the piece being cut first has length points[r] - points[l]."""
    pts = [0] + sorted(cuts) + [n]
    k = len(pts)
    dp = [[0] * k for _ in range(k)]                  # r = l + 1: no cut inside, cost 0
    for gap in range(2, k):                           # interval width in boundary indices
        for l in range(k - gap):
            r = l + gap
            dp[l][r] = pts[r] - pts[l] + min(dp[l][m] + dp[m][r] for m in range(l + 1, r))
    return dp[0][k - 1], pts, dp


def solve_memo(n, cuts):
    """Top-down version. Depth is at most len(cuts) + 2 <= 102, so memoisation is safe here."""
    pts = [0] + sorted(cuts) + [n]

    @lru_cache(maxsize=None)
    def f(l, r):
        if r - l < 2:
            return 0
        return pts[r] - pts[l] + min(f(l, m) + f(m, r) for m in range(l + 1, r))

    return f(0, len(pts) - 1)


def brute(n, cuts):
    """Try every order of the cuts; the cost of a cut is the length of the piece it lands in."""
    best = None
    for order in itertools.permutations(cuts):
        pieces = [(0, n)]
        total = 0
        for x in order:
            for idx, (lo, hi) in enumerate(pieces):
                if lo < x < hi:
                    total += hi - lo
                    pieces[idx:idx + 1] = [(lo, x), (x, hi)]
                    break
        best = total if best is None else min(best, total)
    return 0 if not cuts else best


def greedy_middle(n, cuts):
    """Tempting wrong idea: in each piece first cut the position closest to its middle."""
    def g(lo, hi, inside):
        if not inside:
            return 0
        x = min(inside, key=lambda c: (abs(2 * c - lo - hi), c))
        return (hi - lo) + g(lo, x, [c for c in inside if c < x]) + g(x, hi, [c for c in inside if c > x])
    return g(0, n, sorted(cuts))


# ---- prompt examples
ex = [(7, [1, 3, 4, 5], 16), (9, [5, 6, 1, 4, 2], 22), (10, [], 0), (10, [5], 10)]
for n, cuts, want in ex:
    assert solve(n, cuts)[0] == solve_memo(n, cuts) == brute(n, cuts) == want
print("prompt examples OK")

# ---- table walk-through, first example: points 0 1 3 4 5 7
total, pts, dp = solve(7, [1, 3, 4, 5])
print("points", pts)
print("dp[l][r] (l = row, r = column; only r >= l + 2 is filled by the loop)")
for l, row in enumerate(dp):
    print("  l=%d" % l, row)
print("answer dp[0][%d] = %d" % (len(pts) - 1, total))
# the last cell by hand: boundary 0..7, length 7, split at each inner point
print("dp[0][5] options, split m: " + ", ".join(
    f"m={m}: {dp[0][m]}+{dp[m][5]}" for m in range(1, 5)) + "; best + 7 =", 7 + min(dp[0][m] + dp[m][5] for m in range(1, 5)))

# ---- seeded random cross-check against all orders (len(cuts) <= 6)
cnt = 0
for _ in range(400):
    n = random.randint(2, 30)
    k = random.randint(0, min(6, n - 1))
    cuts = random.sample(range(1, n), k)
    want = brute(n, cuts)
    assert solve(n, cuts)[0] == solve_memo(n, cuts) == want, (n, cuts)
    cnt += 1
print("random cross-check:", cnt, "cases agree with every-order brute force")

# ---- order really matters: spread of costs over all orders of the first example
costs = []
for order in itertools.permutations([1, 3, 4, 5]):
    pieces, tot = [(0, 7)], 0
    for x in order:
        for idx, (lo, hi) in enumerate(pieces):
            if lo < x < hi:
                tot += hi - lo; pieces[idx:idx + 1] = [(lo, x), (x, hi)]; break
    costs.append(tot)
print("first example: 24 orders cost between", min(costs), "and", max(costs))

# ---- greedy 'cut near the middle' is wrong
bad = 0
rg = random.Random(3003)
for _ in range(400):
    n = rg.randint(2, 40)
    cuts = rg.sample(range(1, n), rg.randint(0, min(6, n - 1)))
    bad += greedy_middle(n, cuts) != brute(n, cuts)
print("greedy middle-cut differs from the optimum on", bad, "of 400 random cases")
assert bad > 0

# ---- largest sizes in the prompt: 100 cuts, n = 10^6
rng = random.Random(3002)
big_cuts = rng.sample(range(1, 10**6), 100)
t0 = time.perf_counter()
big = solve(10**6, big_cuts)[0]
dt = time.perf_counter() - t0
assert big == solve_memo(10**6, big_cuts)          # memo depth <= 102 < recursion limit 1000
print("100 cuts, n=10^6:", big, "(memo agrees, depth <= 102)", f"[sandbox time {dt:.2f}s]")

# ---- edge cases
assert solve(2, [1])[0] == 2 and solve(2, [])[0] == 0
assert solve(10, [1, 2, 3])[0] == brute(10, [1, 2, 3])
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
points [0, 1, 3, 4, 5, 7]
dp[l][r] (l = row, r = column; only r >= l + 2 is filled by the loop)
  l=0 [0, 0, 3, 7, 10, 16]
  l=1 [0, 0, 0, 3, 6, 12]
  l=2 [0, 0, 0, 0, 2, 6]
  l=3 [0, 0, 0, 0, 0, 3]
  l=4 [0, 0, 0, 0, 0, 0]
  l=5 [0, 0, 0, 0, 0, 0]
answer dp[0][5] = 16
dp[0][5] options, split m: m=1: 0+12, m=2: 3+6, m=3: 7+3, m=4: 10+0; best + 7 = 16
random cross-check: 400 cases agree with every-order brute force
first example: 24 orders cost between 16 and 20
greedy middle-cut differs from the optimum on 32 of 400 random cases
100 cuts, n=10^6: 6035974 (memo agrees, depth <= 102) [sandbox time 0.03s]
edge cases OK; limit 1000
```

**Edge cases:**
- No cuts: 0 (just the two boundaries).
- One cut: n (the full stick is cut once).
- n = 2 with the single cut at 1: 2.
- Cuts given unsorted (example 2 is): sorting first is required, since the intervals are by position.
- Cuts are distinct and strictly inside (1..n-1); a cut at 0 or n would cost a piece for nothing and is excluded by the prompt.
- n up to 10^6 changes nothing: only the number of cuts sets the work.

**Follow-ups:**
- Return the order too? Store the best m per cell and read the cuts off recursively (first cut at the root, then the left and right halves).
- Why is this the same as optimal merging of pieces? Reverse time: the last cut is the first merge, and each merge of adjacent pieces costs the merged length, which is the same interval shape as matrix-chain multiplication.
- Greedy "cut near the middle"? Wrong: it differs from the optimum on 32 of 400 random cases in the code.

**Common mistakes:**
- Forgetting to sort the cuts, or forgetting the 0 and n boundaries.
- Letting the memo depend on n instead of the cut positions (a table of size n would be 10^6 x 10^6).
- Filling the table by `l` then `r` in row order, so a cell reads an unfilled smaller interval; fill by increasing gap.
- Choosing the last cut and still charging `pts[r] - pts[l]`.

### Q31 ⭐ 🟡 Assign tasks to workers (bitmask DP basics). `cost` is an n x n matrix (1 <= n <= 15, entries 0..1000): `cost[w][t]` is the price of worker w doing task t; each worker gets exactly one task and each task exactly one worker. Return `[best, assignment]` where `assignment[w]` is the task of worker w. Several optimal assignments can exist, so the tie rule is fixed: among minimum-cost assignments return the lexicographically smallest list. Use `f[mask]` = minimum cost for the workers `popcount(mask)`, ..., n-1 to take the tasks NOT in `mask` (so the worker index is implied by the mask), fill masks from full to empty, then walk forward picking the smallest task that keeps the total optimal. State O(2^n * n) time and O(2^n) space, and why n is capped at about 20. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every permutation (n <= 7) and taking the smallest (cost, list) pair on small inputs. Example: cost=[[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]] -> [13, [1, 0, 2, 3]]; cost=[[5]] -> [5, [0]]; cost=[[1, 1], [1, 1]] -> [2, [0, 1]]; cost=[[3, 1], [1, 3]] -> [2, [1, 0]].
**Asked at:** Advanced DP pattern guides covering bitmask DP (techinterview.org advanced and optimisation DP pattern posts; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Bitmask DP basics: a set of at most about 20 items is stored as an integer, one bit per task, so "which tasks are already taken" becomes a table index. Assignment problem by subset DP.

**Say this first (1 line):** "Worker index is the number of set bits in the mask, so the state is just the mask: `f[mask]` is the cheapest way for the remaining workers to take the remaining tasks; fill from the full mask down, then walk forward taking the smallest task that keeps the total optimal. O(2^n * n) time, O(2^n) space."

**Brute force:** Try every permutation of the tasks, n! of them (5,040 for n = 7), cost each, and keep the smallest `(cost, list)` pair; comparing the pair gives the lexicographic tie rule for free. It is the oracle for n <= 7 and is hopeless at n = 15 (1.3 * 10^12).

**Optimal:**
- Encoding: bit t of `mask` is 1 when task t is already taken. Workers are served in order 0, 1, 2, ..., so the next worker is `w = popcount(mask)`; the mask alone says who is next.
- State: `f[mask]` = minimum cost for workers `popcount(mask)`, ..., n-1 to take exactly the tasks NOT in `mask`, one each.
- Base: `f[full] = 0` (full = 2^n - 1): every task is taken, nothing left to pay.
- Transition: worker w picks a free task t: `f[mask] = min over free t of cost[w][t] + f[mask | 1<<t]`. `mask | 1<<t` is larger than `mask`, so iterating masks from `full - 1` down to 0 always finds the right-hand side final.
- Answer: `f[0]`.
- Reconstruction with the fixed tie rule (lexicographically smallest list): start at mask 0; for worker w = 0, 1, ..., scan tasks t in increasing order and take the first free t with `cost[w][t] + f[mask | 1<<t] == f[mask]`. Why this is the lexicographically smallest optimal list: `f` is exact, so every task that passes the test can start some optimal completion, and the smallest such t for worker 0 gives the smallest first entry; given that choice, the same argument applies to worker 1, and so on. Verified against the permutation oracle using the same `(cost, list)` order.
- Memoised version: `g(mask)` with `lru_cache`; the recursion depth is n + 1 <= 16, far under 1000, so there is no recursion-limit issue at this size. Bottom-up avoids call overhead.
- Space: `f` holds 2^n values. Computing only the value could be done layer by layer (masks with k bits depend only on masks with k+1 bits), but reconstruction needs `f` for every mask, so keep the whole array.
- Why n is capped near 20: states double with every extra task. n = 15 gives 32,768 masks and 491,520 transitions; n = 20 gives 1,048,576 masks and 20,971,520 transitions; n = 25 gives 838,860,800 transitions and a table of 33 million entries. Python's int lists make n = 20 slow and heavy; n = 15 is tiny (the code times it).

**Complexity:** Time O(2^n * n): each mask loops over n tasks; the `popcount` is O(1) in practice via `int.bit_count`. Space O(2^n). Compare n!: n = 15 gives 1.3 * 10^12 permutations against 491,520 transitions.

**Dry run:** `cost = [[9,2,7,8],[6,4,3,7],[5,8,1,8],[7,6,9,4]]`. A mask is written with bit 3 on the left (`0101` = tasks 0 and 2 taken). Selected rows of the table (the run prints all 16):

| mask | next worker | f | how |
|---|---|---|---|
| 1111 | | 0 | base |
| 0111 | 3 | 4 | only task 3 free: 4 + 0 |
| 1011 | 3 | 9 | only task 2 free: 9 + 0 |
| 0011 | 2 | 5 | t2: 1 + f[0111]=4 gives 5; t3: 8 + f[1011]=9 gives 17 |
| 0001 | 1 | 9 | t1: 4 + f[0011]=5 gives 9; t2: 3 + 12; t3: 7 + 7 |
| 0000 | 0 | 13 | t0: 9 + 9 = 18; t1: 2 + f[0010]=11 gives 13; t2: 7 + 13; t3: 8 + 12 |

Walk forward from mask 0000 with `f[0] = 13`: worker 0 tries t0 (9 + 9 = 18, not 13), then t1 (2 + 11 = 13, yes), so take 1. Mask is 0010. Worker 1 tries t0: 6 + f[0011]=5 gives 11 = f[0010], yes, take 0. Worker 2 takes 2 (1 + 4 = 5 = f[0011]), worker 3 takes 3. Result `[13, [1, 0, 2, 3]]`, as in the prompt. (Mask 0001 is "task 0 taken", so `f[0001] = 9` is the cost for workers 1..3 to take tasks 1, 2, 3.)

**Code:**
```python
import itertools, random, sys, time
from functools import lru_cache

random.seed(3101)
INF = float("inf")


def assign(cost):
    """f[mask] = min cost for workers popcount(mask)..n-1 to take exactly the tasks NOT in mask.
    Filled from the full mask down to 0; then walk forward taking the smallest task that stays optimal."""
    n = len(cost)
    full = (1 << n) - 1
    f = [INF] * (1 << n)
    f[full] = 0                                       # everyone has a task: nothing left to pay
    for mask in range(full - 1, -1, -1):
        w = mask.bit_count()                          # the next worker is w
        best = INF
        for t in range(n):
            if not mask >> t & 1:                     # task t still free
                v = cost[w][t] + f[mask | 1 << t]
                if v < best:
                    best = v
        f[mask] = best
    mask, out = 0, []
    for w in range(n):
        for t in range(n):                            # ascending t -> lexicographically smallest list
            if not mask >> t & 1 and cost[w][t] + f[mask | 1 << t] == f[mask]:
                out.append(t)
                mask |= 1 << t
                break
    return [f[0], out], f


def assign_memo(cost):
    """Top-down: same state, depth n + 1 <= 16, so recursion is no problem here."""
    n = len(cost)

    @lru_cache(maxsize=None)
    def g(mask):
        w = mask.bit_count()
        if w == n:
            return 0
        return min(cost[w][t] + g(mask | 1 << t) for t in range(n) if not mask >> t & 1)

    mask, out = 0, []
    for w in range(n):
        for t in range(n):
            if not mask >> t & 1 and cost[w][t] + g(mask | 1 << t) == g(mask):
                out.append(t); mask |= 1 << t; break
    return [g(0), out]


def brute(cost):
    n = len(cost)
    return list(min((sum(cost[i][p[i]] for i in range(n)), list(p)) for p in itertools.permutations(range(n))))


# ---- prompt examples
ex = [([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]], [13, [1, 0, 2, 3]]),
      ([[5]], [5, [0]]), ([[1, 1], [1, 1]], [2, [0, 1]]), ([[3, 1], [1, 3]], [2, [1, 0]])]
for c, want in ex:
    assert assign(c)[0] == assign_memo(c) == brute(c) == want, c
print("prompt examples OK")

# ---- hand table for the first example (bit t of the mask = task t is taken)
c = ex[0][0]
res, f = assign(c)
print("f[mask]: workers popcount(mask).. take the tasks NOT in mask")
for mask in range((1 << 4) - 1, -1, -1):
    w = mask.bit_count()
    if w == 4:
        why = "base"
    else:
        opts = [f"t{t}:{c[w][t]}+{f[mask | 1 << t]}" for t in range(4) if not mask >> t & 1]
        why = "worker %d: " % w + "  ".join(opts)
    print(f"  mask {mask:04b}  f={f[mask]:>2}   {why}")
print("walk forward:", res)

# ---- seeded cross-check against every permutation (n <= 7), lexicographic tie rule included
cnt = ties = 0
for _ in range(300):
    n = random.randint(1, 7)
    hi = random.choice([1, 3, 20])                    # tiny values make many tied optimal assignments
    cost = [[random.randint(0, hi) for _ in range(n)] for _ in range(n)]
    got, want = assign(cost)[0], brute(cost)
    assert got == assign_memo(cost) == want, (cost, got, want)
    best = want[0]
    nopt = sum(sum(cost[i][p[i]] for i in range(n)) == best for p in itertools.permutations(range(n)))
    ties += nopt > 1
    cnt += 1
print("random cross-check:", cnt, "matrices agree;", ties, "had several optimal assignments")

# ---- exhaustive: every 2x2 matrix with entries 0..3 and every 3x3 matrix with entries 0..2
ex_cnt = 0
for n, hi in ((2, 3), (3, 2)):
    for flat in itertools.product(range(hi + 1), repeat=n * n):
        cost = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
        assert assign(cost)[0] == brute(cost), cost
        ex_cnt += 1
print("exhaustive:", ex_cnt, "small matrices agree")

# ---- why a naive greedy (each worker takes the cheapest free task, in order) fails
def greedy(cost):
    used, tot, out = set(), 0, []
    for w, row in enumerate(cost):
        t = min((x for x in range(len(cost)) if x not in used), key=lambda x: row[x])
        used.add(t); tot += row[t]; out.append(t)
    return [tot, out]
rg = random.Random(3102)
bad = 0
for _ in range(300):
    cost = [[rg.randint(0, 9) for _ in range(5)] for _ in range(5)]
    bad += greedy(cost)[0] != brute(cost)[0]
print("greedy gives a worse total on", bad, "of 300 random 5x5 matrices")

# ---- the size limit in the prompt: n = 15 (2^15 * 15 transitions); 18 shown for scale, timing is sandbox-only
rng = random.Random(3103)
for n in (12, 15, 18):
    cost = [[rng.randint(0, 1000) for _ in range(n)] for _ in range(n)]
    t0 = time.perf_counter()
    r = assign(cost)[0]
    dt = time.perf_counter() - t0
    assert sorted(r[1]) == list(range(n)) and sum(cost[w][t] for w, t in enumerate(r[1])) == r[0]
    print(f"n={n}: {(1 << n) * n:>9,} transitions, best {r[0]}  [sandbox time {dt:.2f}s]")
print("n=20 would be", f"{(1 << 20) * 20:,}", "transitions and a table of", f"{1 << 20:,}", "entries; n=25 gives", f"{(1 << 25) * 25:,}")

# ---- edge cases
assert assign([[0]])[0] == [0, [0]]
assert assign([[7, 7], [7, 7]])[0] == [14, [0, 1]]
assert assign([[0] * 3 for _ in range(3)])[0] == [0, [0, 1, 2]]
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
f[mask]: workers popcount(mask).. take the tasks NOT in mask
  mask 1111  f= 0   base
  mask 1110  f= 7   worker 3: t0:7+0
  mask 1101  f= 6   worker 3: t1:6+0
  mask 1100  f=11   worker 2: t0:5+6  t1:8+7
  mask 1011  f= 9   worker 3: t2:9+0
  mask 1010  f= 8   worker 2: t0:5+9  t2:1+7
  mask 1001  f= 7   worker 2: t1:8+9  t2:1+6
  mask 1000  f=12   worker 1: t0:6+7  t1:4+8  t2:3+11
  mask 0111  f= 4   worker 3: t3:4+0
  mask 0110  f= 9   worker 2: t0:5+4  t3:8+7
  mask 0101  f=12   worker 2: t1:8+4  t3:8+6
  mask 0100  f=13   worker 1: t0:6+12  t1:4+9  t3:7+11
  mask 0011  f= 5   worker 2: t2:1+4  t3:8+9
  mask 0010  f=11   worker 1: t0:6+5  t2:3+9  t3:7+8
  mask 0001  f= 9   worker 1: t1:4+5  t2:3+12  t3:7+7
  mask 0000  f=13   worker 0: t0:9+9  t1:2+11  t2:7+13  t3:8+12
walk forward: [13, [1, 0, 2, 3]]
random cross-check: 300 matrices agree; 124 had several optimal assignments
exhaustive: 19939 small matrices agree
greedy gives a worse total on 206 of 300 random 5x5 matrices
n=12:    49,152 transitions, best 2234  [sandbox time 0.00s]
n=15:   491,520 transitions, best 1420  [sandbox time 0.04s]
n=18: 4,718,592 transitions, best 1289  [sandbox time 0.42s]
n=20 would be 20,971,520 transitions and a table of 1,048,576 entries; n=25 gives 838,860,800
edge cases OK; limit 1000
```

**Edge cases:**
- n = 1: `[cost[0][0], [0]]`.
- All entries equal: every assignment ties, so the identity list `[0, 1, ..., n-1]` is returned.
- Zero costs: same, the smallest list wins.
- Ties between different optimal assignments, such as `[[3,1],[1,3]]`: both `[0,1]` (cost 6) and `[1,0]` (cost 2) exist, only the second is optimal here, so the answer is `[2, [1, 0]]`; for `[[1,1],[1,1]]` both tie and `[0, 1]` wins by the rule.
- Fill direction: iterate masks downward, or the right-hand side is not ready (for the top-down version, recursion handles the order).

**Follow-ups:**
- Hungarian algorithm? It solves the same problem in O(n^3), which wins at n beyond 20; the bitmask DP is the answer when a short, easy-to-prove solution is wanted for n <= about 20.
- Maximise instead of minimise? Replace `min` by `max` and use `-inf` initial values; the tie rule is unchanged.
- More tasks than workers, or some pairs forbidden? Forbid by infinite cost; with more tasks than workers the mask has more bits than workers and the base case is `popcount == workers`.

**Common mistakes:**
- Iterating masks upward when the transition goes to `mask | bit`: the cell is read before it is final.
- Storing the worker index in the state as well (a factor n wasted).
- Greedy per worker (cheapest free task): worse on 206 of 300 random 5 x 5 matrices in the code.
- Tie rule: choosing the first task that is merely cheap for this worker, not one for which `cost + f[next] == f[mask]`. Only the latter preserves optimality.

### Q32 ⭐ 🟡 Minimum score triangulation of a convex polygon. `values` lists the labels of the vertices in order around a convex polygon (3 <= len <= 100, each in 1..100). A triangulation cuts the polygon into len - 2 triangles by non-crossing diagonals; a triangle scores the product of its three vertex labels, and the score of a triangulation is the sum over its triangles. Return the minimum score. Define `dp[i][j]` for the sub-polygon of vertices i..j, say why edge (i, j) belongs to exactly one triangle with some third vertex k (i < k < j), give the recurrence and the O(n^3) time. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the apex of the triangle on the edge (first, last) (len <= 8) on small inputs. Example: values=[1, 2, 3] -> 6; values=[3, 7, 4, 5] -> 144; values=[1, 3, 1, 4, 1, 5] -> 13; values=[2, 2, 2, 2, 2] -> 24.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP on a polygon (the matrix-chain shape). The state is a range of consecutive vertices, the split point is the apex of the triangle that sits on the closing edge.

**Say this first (1 line):** "`dp[i][j]` is the cheapest triangulation of the sub-polygon i, i+1, ..., j; the edge (i, j) belongs to exactly one triangle, with some third vertex k strictly between, so `dp[i][j] = min over k of dp[i][k] + dp[k][j] + v[i]*v[k]*v[j]`, O(n^3)."

**Brute force:** Plain recursion over the apex of the triangle on the edge (first, last): try every k, recurse on the two sub-polygons `vs[:k+1]` and `vs[k:]`. It visits every triangulation: there are Catalan(n-2) of them (1, 2, 5, 14, 42, 132 for n = 3..8, checked in the code), so it is exponential. The oracle for n <= 8. The code also enumerates all triangulations explicitly and scores each as a second oracle.

**Optimal:**
- State: `dp[i][j]` for i < j = minimum total score of a triangulation of the convex sub-polygon with vertices i, i+1, ..., j, closed by the chord (i, j).
- Base: `dp[i][i+1] = 0`: two vertices form an edge, no triangle. A triangle (j = i + 2) has one triangle: `dp[i][i+2] = v[i]*v[i+1]*v[i+2]`, which falls out of the recurrence with k = i + 1.
- Why the edge (i, j) belongs to exactly one triangle: in any triangulation of a polygon, each edge is a side of precisely one of its triangles, and that triangle's third vertex k lies on the polygon side between i and j (i < k < j). Cutting along the new chords (i, k) and (k, j) splits the problem into two smaller convex polygons that are triangulated independently. Every triangulation is counted once, by its k.
- Transition: `dp[i][j] = min(dp[i][k] + dp[k][j] + v[i]*v[k]*v[j])` over i < k < j.
- Fill by increasing gap `j - i` (2, 3, ..., n-1); the answer is `dp[0][n-1]`.
- Memoised version: `f(i, j)` with `lru_cache`. Recursion depth is at most n <= 100 (each call shrinks the range by at least one), so it is safe under the default limit of 1000 (the code runs n = 100 both ways).
- Space: the cell reads `dp[i][k]` and `dp[k][j]` for all k, so the whole upper triangle is live, O(n^2); there is no row-by-row reduction.
- A tempting greedy, "fan every triangle from the smallest label", is wrong: it differs from the optimum on 78 of 500 random polygons in the code.

**Complexity:** Time O(n^3): about n^2/2 cells times up to n apexes, exactly C(n,3) = 161,700 inner steps at n = 100. Space O(n^2).

**Dry run:** `values = [3, 7, 4, 5]` (the run also prints `[1, 2, 3]`, the first example: only `dp[0][2] = 1*2*3 = 6`).

| cell | options over k | value |
|---|---|---|
| dp[0][2] (3,7,4) | k=1: 0 + 0 + 3*7*4 = 84 | 84 |
| dp[1][3] (7,4,5) | k=2: 0 + 0 + 7*4*5 = 140 | 140 |
| dp[0][3] (all four) | k=1: 0 + 140 + 3*7*5 = 245; k=2: 84 + 0 + 3*4*5 = 144 | 144 |

The two triangulations of a quadrilateral are the two diagonals; 144 uses the diagonal 0-2 (triangles 3,7,4 and 3,4,5). For the first example of the prompt `[1,2,3]` there is a single triangle, so the answer is 6.

**Code:**
```python
import random, sys, time
from functools import lru_cache

random.seed(3201)


def solve(values):
    """dp[i][j] = min score to triangulate the sub-polygon with vertices i, i+1, ..., j (edge i-j closes it)."""
    n = len(values)
    dp = [[0] * n for _ in range(n)]                    # j = i + 1: a single edge, no triangle
    for gap in range(2, n):                             # sub-polygon has gap + 1 vertices
        for i in range(n - gap):
            j = i + gap
            dp[i][j] = min(dp[i][k] + dp[k][j] + values[i] * values[k] * values[j]
                           for k in range(i + 1, j))    # apex k of the triangle on edge (i, j)
    return dp[0][n - 1], dp


def solve_memo(values):
    n = len(values)

    @lru_cache(maxsize=None)
    def f(i, j):                                        # depth at most n, safe for n <= 100
        if j - i < 2:
            return 0
        return min(f(i, k) + f(k, j) + values[i] * values[k] * values[j] for k in range(i + 1, j))

    return f(0, n - 1)


def triangulations(vs):
    """Every triangulation of the polygon vs as a list of triangles, by the apex of the edge (first, last)."""
    if len(vs) < 3:
        yield []
        return
    for k in range(1, len(vs) - 1):
        for left in triangulations(vs[:k + 1]):
            for right in triangulations(vs[k:]):
                yield left + right + [(vs[0], vs[k], vs[-1])]


def brute(values):
    """Plain recursion over the apex of the triangle on the edge (first, last)."""
    def f(vs):
        if len(vs) < 3:
            return 0
        return min(vs[0] * vs[k] * vs[-1] + f(vs[:k + 1]) + f(vs[k:]) for k in range(1, len(vs) - 1))
    return f(list(values))


def fan_from_smallest(values):
    """Tempting wrong idea: fan every triangle from the smallest label."""
    n = len(values)
    s = values.index(min(values))
    others = [values[(s + t) % n] for t in range(1, n)]
    return sum(values[s] * others[t] * others[t + 1] for t in range(n - 2))


# ---- prompt examples
ex = [([1, 2, 3], 6), ([3, 7, 4, 5], 144), ([1, 3, 1, 4, 1, 5], 13), ([2, 2, 2, 2, 2], 24)]
for v, want in ex:
    assert solve(v)[0] == solve_memo(v) == brute(v) == want, v
print("prompt examples OK")

# ---- table walk-throughs
for v in ([1, 2, 3], [3, 7, 4, 5]):
    total, dp = solve(v)
    print("values", v)
    for i in range(len(v) - 1):
        for j in range(i + 2, len(v)):
            opts = [f"k={k}: {dp[i][k]}+{dp[k][j]}+{v[i]}*{v[k]}*{v[j]}={dp[i][k] + dp[k][j] + v[i] * v[k] * v[j]}" for k in range(i + 1, j)]
            print(f"  dp[{i}][{j}] = min({'; '.join(opts)}) = {dp[i][j]}")
    print("  answer", total)

# ---- the number of triangulations is a Catalan number; every one has n - 2 triangles
catalan = [1, 1, 2, 5, 14, 42, 132]          # for n = 3..9 vertices: C(n-2)
for n in range(3, 9):
    ts = list(triangulations(list(range(1, n + 1))))
    assert len(ts) == catalan[n - 2] and all(len(t) == n - 2 for t in ts)
print("triangulation counts for n = 3..8:", [len(list(triangulations(list(range(1, n + 1))))) for n in range(3, 9)])

# ---- seeded random cross-check (len <= 8)
cnt = 0
for _ in range(500):
    n = random.randint(3, 8)
    v = [random.randint(1, 100) for _ in range(n)]
    assert solve(v)[0] == solve_memo(v) == brute(v), v
    cnt += 1
print("random cross-check:", cnt, "polygons agree with the apex recursion")

# ---- a second independent oracle: enumerate every triangulation and score it
sc = 0
for _ in range(100):
    n = random.randint(3, 8)
    v = [random.randint(1, 9) for _ in range(n)]
    best = min(sum(a * b * c for a, b, c in t) for t in triangulations(v))
    assert best == solve(v)[0]
    sc += 1
print("enumerate-all-triangulations check:", sc, "polygons agree")

# ---- fan from the smallest vertex is not always optimal
rg = random.Random(3202)
bad = 0
for _ in range(500):
    v = [rg.randint(1, 20) for _ in range(rg.randint(4, 8))]
    bad += fan_from_smallest(v) != solve(v)[0]
print("fan from the smallest label differs from the optimum on", bad, "of 500 random polygons")
assert bad > 0

# ---- largest size: n = 100 (C(100,3) = 161,700 inner steps)
rb = random.Random(3203)
big = [rb.randint(1, 100) for _ in range(100)]
t0 = time.perf_counter()
res = solve(big)[0]
dt = time.perf_counter() - t0
assert res == solve_memo(big)
print("n=100:", res, "(memoised version agrees, recursion depth <= 100)", f"[sandbox time {dt:.2f}s]")

# ---- edge cases
assert solve([1, 1, 1])[0] == 1 and solve([100] * 3)[0] == 10**6
assert solve([5, 5, 5, 5])[0] == 250
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
values [1, 2, 3]
  dp[0][2] = min(k=1: 0+0+1*2*3=6) = 6
  answer 6
values [3, 7, 4, 5]
  dp[0][2] = min(k=1: 0+0+3*7*4=84) = 84
  dp[0][3] = min(k=1: 0+140+3*7*5=245; k=2: 84+0+3*4*5=144) = 144
  dp[1][3] = min(k=2: 0+0+7*4*5=140) = 140
  answer 144
triangulation counts for n = 3..8: [1, 2, 5, 14, 42, 132]
random cross-check: 500 polygons agree with the apex recursion
enumerate-all-triangulations check: 100 polygons agree
fan from the smallest label differs from the optimum on 78 of 500 random polygons
n=100: 273789 (memoised version agrees, recursion depth <= 100) [sandbox time 0.02s]
edge cases OK; limit 1000
```

**Edge cases:**
- n = 3: one triangle, the product of the three labels (`[1,2,3]` gives 6).
- n = 4: two triangulations; take the cheaper (144 for `[3,7,4,5]`).
- All labels equal to v: every triangulation costs (n-2) * v^3 (24 for five 2's).
- Labels as large as 100, n = 100: the answer fits easily, and Python has no overflow anyway.
- The polygon is circular, but the DP fixes the chord (0, n-1) as the closing edge, which is also a real edge, so no rotation is needed.

**Follow-ups:**
- Why is it the same as matrix-chain multiplication? A chain of n - 1 matrices with dimensions `d` is the same recurrence with the product `d[i]*d[k]*d[j]`.
- Return the diagonals too? Store the best k per cell and recurse: the chord (i, k) and (k, j) are emitted for each triple.
- Maximum score instead? Swap `min` for `max`; the triangle product structure is the same.

**Common mistakes:**
- Choosing k from the whole range instead of strictly between i and j (a triangle with a repeated vertex).
- Treating the polygon as a line and forgetting that edge (0, n-1) closes it; it is already included as the outer edge of the sub-polygon.
- Fan greedy from the smallest label.
- Filling `dp` by row order so `dp[k][j]` has not been computed; fill by gap.

### Q33 ⭐ 🔴 Strange printer (interval DP, concept level). A printer prints a run of one repeated letter over any contiguous range of positions in one turn, and each print overwrites whatever was there. `s` is a lowercase string with 0 <= len <= 100. Return the minimum number of turns to print exactly `s` (0 for the empty string). Collapse equal neighbours first, define `dp[i][j]` for the substring i..j, give the transition `dp[i][j-1] + 1` versus joining the print of s[j] with the print of an equal letter s[k] (i <= k < j), and say why printing the first letter across a wider range is never worse. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a breadth-first search over all printed states (len <= 6, alphabet a-c) on small inputs. Example: s='aaabbb' -> 2; s='aba' -> 2; s='' -> 0; s='abcabc' -> 5; s='a' -> 1.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP, concept level. State is a substring i..j; the transition either prints the last letter separately, or lets the print of that letter be shared with an equal letter earlier in the range.

**Say this first (1 line):** "Merge equal neighbours first, then `dp[i][j]` is the fewest turns for t[i..j]: either `dp[i][j-1] + 1` (print t[j] alone) or, for each k with t[k] == t[j], print t[k] and t[j] with one wide stroke: `dp[i][k] + dp[k+1][j-1]`; O(n^3)."

**Brute force:** Breadth-first search over strip states: start from all blanks, each move overwrites any range with one letter, stop when the strip equals `s`. The number of states grows like 4^n for the alphabet a-c (4 symbols with the blank), each with up to n(n+1)/2 * 3 moves. It is the oracle for len <= 6 over a, b, c.

**Optimal:**
- Collapse first: `aaabbb` is the same job as `ab`, because one stroke can cover a whole run of equal letters at no extra cost. The code checks that the DP gives the same answers with and without the collapse for all 255 strings up to length 7 over {a, b}; collapsing just shrinks n.
- State: `dp[i][j]` = minimum turns to print `t[i..j]` onto a blank strip (t is the collapsed string).
- Base: `dp[i][i] = 1`; an empty string needs 0 turns.
- Transition: first candidate `dp[i][j-1] + 1`: print the first j - i letters, then one more stroke for t[j]. Second candidate for every k in [i, j) with `t[k] == t[j]`: print t[j] with the same stroke as t[k]. That stroke is laid down while printing `t[i..k]` (so cost `dp[i][k]`, the stroke simply extends to column j) and then everything between, `t[k+1..j-1]`, is printed on top afterwards (cost `dp[k+1][j-1]`, 0 if that range is empty). Take the minimum.
- Why the answer needs only "the first letter can be printed across a wider range": in an optimal plan, the stroke that paints the leftmost position can be extended to the right, to cover another equal letter, without ever hurting, because every later stroke over that range overwrites it anyway. So, the leftmost letter is either printed alone or together with an equal letter; the code's DP states the mirror form (last letter t[j]), which is the same argument read right to left. An exchange argument, checked rather than proved here: the DP equals the BFS for all 364 strings of length <= 5 over a, b, c and 60 random strings of length 6.
- Wrong version: only splitting into two independent parts (`dp[i][k] + dp[k+1][j]`) never shares a stroke, so `aba` costs 3 instead of 2; it is wrong on 864 strings of length <= 6 in the code.
- Memoised version: `f(i, j)` with `lru_cache`, depth <= n <= 100 (each call shrinks the range), so there is no recursion-limit problem at this size; bottom-up is shown as the main solution.
- Space: `dp` reads cells inside `[i, j]` for the same i and larger i, so the full triangle is kept: O(n^2).

**Complexity:** Time O(n^3): n^2/2 cells, each scanning up to n values of k (at n = 100 that is about 166,000 inner steps). Space O(n^2). The code's random 26-letter string of length 100 runs in a blink (sandbox only).

**Dry run:**
- `aaabbb` collapses to `ab`: `dp[0][0] = 1`, `dp[1][1] = 1`, `dp[0][1] = dp[0][0] + 1 = 2` (the letters differ, so no sharing). Answer 2.
- `aba`, the interesting one (upper triangle, rows i):

| i \ j | 0 (a) | 1 (b) | 2 (a) |
|---|---|---|---|
| 0 (a) | 1 | 2 | 2 |
| 1 (b) |  | 1 | 2 |
| 2 (a) |  |  | 1 |

`dp[0][2]`: candidate one is `dp[0][1] + 1 = 3`. Candidate two uses k = 0 (t[0] == t[2] == a): `dp[0][0] + dp[1][1] = 1 + 1 = 2`. So print `aaa` first, then `b` over the middle. Answer 2.
- `abcabc` -> 5 (the run prints that 6 x 6 table; `dp[0][5] = 5`: printing the last c alone gives `dp[0][4] + 1 = 5`, sharing it with the c at k = 2 gives `dp[0][2] + dp[3][4] = 3 + 2 = 5`, a tie).

**Code:**
```python
import itertools, random, sys, time
from collections import deque
from functools import lru_cache

random.seed(3301)


def collapse(s):
    return "".join(ch for i, ch in enumerate(s) if i == 0 or ch != s[i - 1])


def solve(s, do_collapse=True):
    """dp[i][j] = fewest turns to print t[i..j] on a blank strip (t = s with equal neighbours merged)."""
    t = collapse(s) if do_collapse else s
    n = len(t)
    if n == 0:
        return 0, t, []
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            best = dp[i][j - 1] + 1                       # print t[j] on its own
            for k in range(i, j):
                if t[k] == t[j]:                          # share one print of the letter with t[k]
                    mid = dp[k + 1][j - 1] if k + 1 <= j - 1 else 0
                    best = min(best, dp[i][k] + mid)
            dp[i][j] = best
    return dp[0][n - 1], t, dp


def solve_memo(s):
    """Top-down, the same recurrence. Depth is at most len(t) <= 100: safe."""
    t = collapse(s)
    n = len(t)

    @lru_cache(maxsize=None)
    def f(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        best = f(i, j - 1) + 1
        for k in range(i, j):
            if t[k] == t[j]:
                best = min(best, f(i, k) + f(k + 1, j - 1))
        return best

    return f(0, n - 1) if n else 0


def bfs(s, alphabet="abc"):
    """Oracle: shortest number of turns over all strip states ('?' = blank), every range and letter."""
    n = len(s)
    if n == 0:
        return 0
    start = "?" * n
    seen = {start}
    dq = deque([(start, 0)])
    while dq:
        cur, d = dq.popleft()
        if cur == s:
            return d
        for l in range(n):
            for r in range(l, n):
                for ch in alphabet:
                    nxt = cur[:l] + ch * (r - l + 1) + cur[r + 1:]
                    if nxt not in seen:
                        seen.add(nxt)
                        dq.append((nxt, d + 1))


def split_only(s):
    """Wrong: only split into two independent parts, never share a print between them."""
    t = collapse(s)
    n = len(t)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] for k in range(i, j))
    return dp[0][n - 1]


# ---- prompt examples
ex = [("aaabbb", 2), ("aba", 2), ("", 0), ("abcabc", 5), ("a", 1)]
for s, want in ex:
    assert solve(s)[0] == solve_memo(s) == bfs(s) == want, s
print("prompt examples OK")

# ---- table walk-throughs (collapsed string; entry [i][j], upper triangle)
for s in ("aaabbb", "aba", "abcabc"):
    res, t, dp = solve(s)
    print(f"s={s!r} collapsed={t!r} answer={res}")
    for i, row in enumerate(dp):
        print("   ", t[i], [row[j] if j >= i else "." for j in range(len(t))])
# the decisive cell of 'aba': dp[0][2], j = 2 (letter a), k = 0 (also a)
_, t, dp = solve("aba")
print("aba: dp[0][1] + 1 =", dp[0][1] + 1, "vs share the a at k=0: dp[0][0] + dp[1][1] =", dp[0][0] + dp[1][1], "-> 2")

# ---- collapsing does not change the answer (the DP gives the same value without it)
cnt = 0
for L in range(0, 8):
    for tup in itertools.product("ab", repeat=L):
        s = "".join(tup)
        assert solve(s, True)[0] == solve(s, False)[0], s
        cnt += 1
print("collapse check: all", cnt, "strings over {a,b} up to length 7 give the same answer with and without it")

# ---- exhaustive vs BFS: every string of length <= 5 over {a,b,c}
cnt = 0
for L in range(0, 6):
    for tup in itertools.product("abc", repeat=L):
        s = "".join(tup)
        assert solve(s)[0] == solve_memo(s) == bfs(s), s
        cnt += 1
print("exhaustive vs BFS:", cnt, "strings (len <= 5, alphabet a-c) agree")

# ---- seeded random, length 6
for _ in range(60):
    s = "".join(random.choice("abc") for _ in range(6))
    assert solve(s)[0] == solve_memo(s) == bfs(s), s
print("random cross-check: 60 strings of length 6 agree with the BFS over printed states")

# ---- the 'split only' variant is wrong
bad = [s for L in range(1, 7) for tup in itertools.product("abc", repeat=L)
       for s in ["".join(tup)] if split_only(s) != solve(s)[0]]
print("split-only (no sharing) is wrong on", len(bad), "strings of length <= 6; first:", bad[0])
assert "aba" in bad

# ---- bounds
assert solve("a" * 100)[0] == 1 and solve("ab" * 50)[0] == 51        # ababab...: one 'a' sweep + 50 b's
t0 = time.perf_counter()
rg = random.Random(3302)
big = "".join(rg.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(100))
res = solve(big)[0]
dt = time.perf_counter() - t0
assert res == solve_memo(big)
print("length 100 random:", res, "(memo agrees; recursion depth <= 100)", f"[sandbox time {dt:.2f}s]")
assert solve("abcdefghijklmnopqrstuvwxyz")[0] == 26
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
s='aaabbb' collapsed='ab' answer=2
    a [1, 2]
    b ['.', 1]
s='aba' collapsed='aba' answer=2
    a [1, 2, 2]
    b ['.', 1, 2]
    a ['.', '.', 1]
s='abcabc' collapsed='abcabc' answer=5
    a [1, 2, 3, 3, 4, 5]
    b ['.', 1, 2, 3, 3, 4]
    c ['.', '.', 1, 2, 3, 3]
    a ['.', '.', '.', 1, 2, 3]
    b ['.', '.', '.', '.', 1, 2]
    c ['.', '.', '.', '.', '.', 1]
aba: dp[0][1] + 1 = 3 vs share the a at k=0: dp[0][0] + dp[1][1] = 2 -> 2
collapse check: all 255 strings over {a,b} up to length 7 give the same answer with and without it
exhaustive vs BFS: 364 strings (len <= 5, alphabet a-c) agree
random cross-check: 60 strings of length 6 agree with the BFS over printed states
split-only (no sharing) is wrong on 864 strings of length <= 6; first: aba
length 100 random: 72 (memo agrees; recursion depth <= 100) [sandbox time 0.01s]
edge cases OK; limit 1000
```

**Edge cases:**
- Empty string: 0.
- One letter, or a single repeated letter (`aaa`, 100 a's): 1.
- All letters different (26 distinct): n turns, nothing to share.
- Alternating `abab...` of length 100: 51 (the code asserts it): one stroke of a across everything, then 50 strokes of b.

**Follow-ups:**
- Why O(n^3) and not better? n^2 states with O(n) transitions each; with n <= 100 that is about 166,000 steps, so nothing faster is needed.
- How would you recover the strokes? Store which candidate won per cell and replay: stroke (k..j) of letter t[j] first, then the middle.
- How does it differ from burst balloons / cut a stick? Same interval shape; here the split condition is "equal letters" instead of "any split point", so only the matching k are tried.

**Common mistakes:**
- Skipping the collapse (not wrong for correctness, but it blows up the table with redundant cells).
- Using `dp[k+1][j]` instead of `dp[k+1][j-1]`: the letter t[j] is already painted by the shared stroke.
- Forgetting the base for an empty middle range (`k + 1 > j - 1` must give 0).
- Only splitting into independent halves: it never shares a stroke and is wrong on `aba`.

### Q34 ⭐ 🔴 Cherry pickup (two walkers, concept level). `grid` is an n x n list of lists (1 <= n <= 50) with 0 (empty), 1 (one cherry) and -1 (thorns, impassable). Go from the top-left to the bottom-right moving only right or down, then back to the top-left moving only left or up, picking each cherry you pass over (a picked cherry cell becomes empty). Return the maximum cherries, or 0 if no path exists from the top-left to the bottom-right. Explain why the return trip is the same as a second walker going down-right at the same time, so the state is (step k, row of walker 1, row of walker 2) with the columns implied, give the transition over the four previous-state choices, how a cell shared by both walkers is counted once, and why two separate greedy trips fail. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every pair of right/down paths (n <= 5) on small inputs. Example: grid=[[0, 1, -1], [1, 0, -1], [1, 1, 1]] -> 5; grid=[[1, 1, -1], [1, -1, 1], [-1, 1, 1]] -> 0; grid=[[1]] -> 1; grid=[[0, 0], [0, 0]] -> 0.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** DP over time with two agents moving in lock-step. Two walkers that move at the same pace share a "step number" k, so their columns follow from their rows and the state is (k, r1, r2).

**Say this first (1 line):** "The trip back is the same as a second walker going down-right at the same time, so run both at once: `dp[k][r1][r2]` is the most cherries the pair has picked after k moves, with columns `k - r1` and `k - r2`; four predecessor choices, a shared cell counts once, O(n^3)."

**Brute force:** Enumerate every right/down path (C(2n-2, n-1) of them, 70 for n = 5), keep those without thorns, and for every pair of paths add the cherries on the **union** of their cells (a shared cell once). The code also checks, for n <= 3, the statement read literally: pick a path, remove its cherries, then pick the best return path, and shows the two readings agree. Oracle for n <= 5.

**Optimal:**
- Why the return trip is a second down-right walker: a left/up path from the bottom-right to the top-left, read backwards, is a right/down path from the top-left to the bottom-right. Picking the cherries "on the way back" is then picking the cherries of a second right/down path, with the rule that a cherry already picked (a cell on both paths) is counted once. So the answer is the best union over a pair of right/down paths.
- State: after k moves each (k = 0..2n-2), walker 1 is at row r1 and column `k - r1`, walker 2 at row r2 and column `k - r2`. `dp[k][r1][r2]` = max cherries picked by the pair so far, or -infinity if the pair cannot be there (thorn, off-grid or unreachable).
- Base: `dp[0][0][0] = grid[0][0]` (0 or 1; -1 means no path and the answer is 0).
- Transition: each walker came from above (row - 1, same k - 1) or from the left (same row at k - 1). Four predecessor pairs: `(r1, r2)`, `(r1-1, r2)`, `(r1, r2-1)`, `(r1-1, r2-1)` at step k - 1. So `dp[k][r1][r2] = max(four predecessors) + grid[r1][k-r1] + (grid[r2][k-r2] if r1 != r2 else 0)`; skip any pair that stands on a thorn.
- Shared cell: when `r1 == r2` the columns are equal too (same k), so the walkers are on the same cell; add its cherry once.
- Answer: `max(0, dp[2n-2][n-1][n-1])`: if no pair arrives (thorns cut every path) the value is -infinity and the answer is 0.
- Symmetry: swapping the two walkers changes nothing, so only `r1 <= r2` is stored (about half the states); the code does this.
- Space: step k reads only step k - 1, so two n x n layers suffice: O(n^2) (the code keeps one rolling layer).
- Memoised version: `f(k, r1, r2)` = best from here to the end, depth 2n - 1 = 99 at n = 50, which is below the default limit of 1000, so memoisation is safe (the code runs n = 50 both ways). Bottom-up is still preferred.
- Why two separate greedy trips fail: taking the best single trip first can use up cherries and force a poor return. The smallest counterexample the code found: `[[0,1,0],[0,1,1],[1,1,0]]`: the greedy two-trip total is 4 but the best is 5. It is wrong on 34 of 500 random small grids.

**Complexity:** Time O(n^3): 2n - 1 steps times at most n^2/2 row pairs, 4 predecessors each. Space O(n^2) with rolling layers. At n = 50 that is about 99 * 1,250 * 4 operations.

**Dry run:** `grid = [[0,1,-1],[1,0,-1],[1,1,1]]`, pairs `(r1, r2)` kept with r1 <= r2 (the run prints this):

| k | reachable pairs (r1, r2): value | note |
|---|---|---|
| 0 | (0,0): 0 | start cell value 0 |
| 1 | (0,0): 1, (0,1): 2, (1,1): 1 | (0,0) means both on cell (0,1), counted once; (0,1) means one on (0,1), one on (1,0): 1 + 1 |
| 2 | (1,1): 2, (1,2): 3, (2,2): 2 | (0,2) is a thorn, so no pair uses row 0; (1,2) = cells (1,1)=0 and (2,0)=1 on top of the best earlier 2 |
| 3 | (2,2): 4 | cell (2,1) = 1; (1,2) is a thorn; best predecessor 3 |
| 4 | (2,2): 5 | cell (2,2) = 1 counted once |

Answer 5. The pair of paths: down, down, right, right and right, down, down, right (so both pass (2,1)). The second example has thorns that cut every route: no pair reaches k = 4, so the answer is 0.

**Code:**
```python
import itertools, random, sys, time
from functools import lru_cache

random.seed(3401)
NEG = float("-inf")


def solve(grid, trace=None):
    """State (k, r1, r2): both walkers have made k right/down moves, so their columns are k - r1, k - r2.
    dp[r1][r2] = most cherries collected by the pair so far; NEG = unreachable. Rolls over k: O(n^2) space."""
    n = len(grid)
    dp = [[NEG] * n for _ in range(n)]
    if grid[0][0] == -1:
        return 0
    dp[0][0] = grid[0][0]
    if trace is not None:
        trace.append((0, {(0, 0): dp[0][0]}))
    for k in range(1, 2 * n - 1):
        nd = [[NEG] * n for _ in range(n)]
        for r1 in range(max(0, k - n + 1), min(n, k + 1)):
            c1 = k - r1
            if grid[r1][c1] == -1:
                continue
            for r2 in range(r1, min(n, k + 1)):          # r2 >= r1 by symmetry: swapping walkers changes nothing
                c2 = k - r2
                if r2 < max(0, k - n + 1) or grid[r2][c2] == -1:
                    continue
                best = max(dp[a][b] for a in (r1, r1 - 1) for b in (r2, r2 - 1)
                           if a >= 0 and b >= 0 and (a <= b))    # previous row pair, kept in r1 <= r2 form
                if best == NEG:
                    continue
                gain = grid[r1][c1] + (grid[r2][c2] if r2 != r1 else 0)   # a shared cell counts once
                nd[r1][r2] = best + gain
        dp = nd
        if trace is not None:
            trace.append((k, {(a, b): dp[a][b] for a in range(n) for b in range(n) if dp[a][b] != NEG}))
    return 0 if dp[n - 1][n - 1] == NEG else dp[n - 1][n - 1]


def solve_memo(grid):
    """Top-down version: depth 2n - 1 <= 99 for n <= 50, so memoisation is safe."""
    n = len(grid)

    @lru_cache(maxsize=None)
    def f(k, r1, r2):                                    # best total from step k to the end, walkers at rows r1, r2
        c1, c2 = k - r1, k - r2
        if r1 >= n or r2 >= n or c1 >= n or c2 >= n or grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return NEG
        gain = grid[r1][c1] + (grid[r2][c2] if r1 != r2 else 0)
        if k == 2 * n - 2:
            return gain
        nxt = max(f(k + 1, r1 + a, r2 + b) for a in (0, 1) for b in (0, 1))
        return NEG if nxt == NEG else gain + nxt

    r = f(0, 0, 0)
    return 0 if r == NEG else r


def all_paths(n):
    for downs in itertools.combinations(range(2 * n - 2), n - 1):
        d = set(downs)
        i = j = 0
        cells = [(0, 0)]
        for s in range(2 * n - 2):
            if s in d:
                i += 1
            else:
                j += 1
            cells.append((i, j))
        yield cells


def brute(grid):
    """Every pair of right/down paths; cherries on the union of cells (a shared cell once)."""
    n = len(grid)
    ps = [p for p in all_paths(n) if all(grid[a][b] != -1 for a, b in p)]
    best = 0
    for p in ps:
        for q in ps:
            best = max(best, sum(grid[a][b] for a, b in set(p) | set(q)))
    return best


def literal_trip(grid):
    """The statement read literally (tiny n): walk down-right picking cherries, then walk back up-left
    over the same grid with those cherries gone. Tests the 'second walker' reduction itself."""
    n = len(grid)
    best = 0
    for p in all_paths(n):
        if any(grid[a][b] == -1 for a, b in p):
            continue
        got = sum(grid[a][b] for a, b in p)
        g2 = [row[:] for row in grid]
        for a, b in p:
            g2[a][b] = 0 if g2[a][b] == 1 else g2[a][b]
        # return trip: left/up moves from (n-1, n-1) to (0, 0) = a right/down path read backwards
        back = 0
        for q in all_paths(n):
            if any(g2[a][b] == -1 for a, b in q):
                continue
            back = max(back, sum(g2[a][b] for a, b in q))
        best = max(best, got + back)
    return best


def greedy_two_trips(grid):
    """Wrong: take the best single trip, clear it, then take the best second trip."""
    n = len(grid)
    ps = [p for p in all_paths(n) if all(grid[a][b] != -1 for a, b in p)]
    if not ps:
        return 0
    first = max(ps, key=lambda p: sum(grid[a][b] for a, b in p))
    g2 = [row[:] for row in grid]
    for a, b in first:
        g2[a][b] = 0 if g2[a][b] == 1 else g2[a][b]
    return sum(grid[a][b] for a, b in first) + max(sum(g2[a][b] for a, b in p) for p in ps)


# ---- prompt examples
ex = [([[0, 1, -1], [1, 0, -1], [1, 1, 1]], 5), ([[1, 1, -1], [1, -1, 1], [-1, 1, 1]], 0),
      ([[1]], 1), ([[0, 0], [0, 0]], 0)]
for g, want in ex:
    assert solve(g) == solve_memo(g) == brute(g) == want, g
print("prompt examples OK")

# ---- walk-through of the first example: reachable (r1, r2) pairs per step (r1 <= r2), value = cherries so far
g = ex[0][0]
tr = []
solve(g, tr)
print("grid", g)
for k, cells in tr:
    print(f"  k={k}:", {f"r1={a},r2={b} (c={k - a},{k - b})": v for (a, b), v in cells.items()})
print("answer dp[k=4][2][2] =", solve(g))

# ---- seeded cross-check: DP vs every pair of paths (n <= 5); small n also vs the literal go-and-return reading
cnt = zero = 0
for _ in range(500):
    n = random.randint(1, 5)
    p_thorn = random.choice([0.0, 0.15, 0.3])
    g = [[(-1 if random.random() < p_thorn else random.randint(0, 1)) for _ in range(n)] for _ in range(n)]
    g[0][0] = random.choice([g[0][0], 0, 1]) if random.random() < 0.8 else g[0][0]
    want = brute(g)
    assert solve(g) == solve_memo(g) == want, (g, want)
    if n <= 3:
        assert literal_trip(g) == want, g
    cnt += 1
    zero += want == 0
print("random cross-check:", cnt, "grids agree with the pair-of-paths brute force;", zero, "have answer 0")

# ---- the reduction itself: literal go-and-return reading equals the pair of paths (exhaustive, n <= 3, no thorns)
c = 0
for n in (1, 2, 3):
    for flat in itertools.product((0, 1), repeat=n * n):
        g = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
        assert literal_trip(g) == brute(g) == solve(g)
        c += 1
print("exhaustive 0/1 grids n <= 3:", c, "agree, literal reading included")

# ---- two separate greedy trips fail
bad = 0
rg = random.Random(3402)
example = None
for _ in range(500):
    n = rg.randint(3, 5)
    g = [[rg.choice((0, 0, 1, 1, 1, -1)) for _ in range(n)] for _ in range(n)]
    g[0][0] = g[n - 1][n - 1] = 0
    want = brute(g)
    if greedy_two_trips(g) != want:
        bad += 1
        if example is None or n < len(example[0]):
            example = (g, greedy_two_trips(g), want)
print("two greedy trips wrong on", bad, "of 500 random grids; smallest:", example)
assert bad > 0

# ---- largest size n = 50 (2n-1 steps, about n^2 / 2 row pairs each), sandbox time only
rb = random.Random(3403)
n = 50
big = [[(-1 if rb.random() < 0.08 else rb.randint(0, 1)) for _ in range(n)] for _ in range(n)]
big[0][0] = big[n - 1][n - 1] = 0
t0 = time.perf_counter()
res = solve(big)
dt = time.perf_counter() - t0
assert res == solve_memo(big)
print("n=50 random:", res, "(memo agrees, recursion depth 99)", f"[sandbox time {dt:.2f}s]")

# ---- edge cases
assert solve([[-1]]) == 0 and solve([[0]]) == 0
assert solve([[1, 1], [1, 1]]) == 4
assert solve([[0, -1], [-1, 0]]) == 0                # both ways blocked
assert solve([[1] * 4 for _ in range(4)]) == 12 == brute([[1] * 4 for _ in range(4)])   # 2*7 cells - the 2 shared ends
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
grid [[0, 1, -1], [1, 0, -1], [1, 1, 1]]
  k=0: {'r1=0,r2=0 (c=0,0)': 0}
  k=1: {'r1=0,r2=0 (c=1,1)': 1, 'r1=0,r2=1 (c=1,0)': 2, 'r1=1,r2=1 (c=0,0)': 1}
  k=2: {'r1=1,r2=1 (c=1,1)': 2, 'r1=1,r2=2 (c=1,0)': 3, 'r1=2,r2=2 (c=0,0)': 2}
  k=3: {'r1=2,r2=2 (c=1,1)': 4}
  k=4: {'r1=2,r2=2 (c=2,2)': 5}
answer dp[k=4][2][2] = 5
random cross-check: 500 grids agree with the pair-of-paths brute force; 167 have answer 0
exhaustive 0/1 grids n <= 3: 530 agree, literal reading included
two greedy trips wrong on 34 of 500 random grids; smallest: ([[0, 1, 0], [0, 1, 1], [1, 1, 0]], 4, 5)
n=50 random: 161 (memo agrees, recursion depth 99) [sandbox time 0.03s]
edge cases OK; limit 1000
```

**Edge cases:**
- n = 1: the cell value if it is not a thorn (the walkers are the same cell, counted once), else 0.
- Thorn at the start or the end: 0.
- Thorns that disconnect the corners: 0, never a negative number.
- All zeros: 0.
- All ones: the two paths share only the corners, so 4n - 4 for n >= 2 (12 for n = 4), not the sum of two full paths (the code asserts it).
- A cell on both paths counted twice is the standard bug: only when `r1 == r2`.

**Follow-ups:**
- Why does only the row pair matter, not the columns? Same step count k makes `c = k - r` for both walkers.
- Return the actual two paths? Keep the full 3D table (or a parent choice per state) and walk back from `(2n-2, n-1, n-1)`.
- Why not just rows and columns of both walkers (four coordinates)? The step number ties them together, so one coordinate per walker is redundant: n^4 states drop to n^3.

**Common mistakes:**
- Running the best path twice (greedy) and removing the cherries between trips.
- Counting a shared cell twice (add the second cherry only when `r1 != r2`).
- Allowing a walker to step on a thorn, or treating -infinity as 0 and returning a positive total for an unreachable end.
- Returning -infinity instead of 0 when no path exists.

### Q35 ⭐ 🔴 Travelling salesman with a small number of cities (bitmask DP basics). `dist` is an n x n matrix (1 <= n <= 12) of non-negative integers (at most 1000; `dist[a][b]` may differ from `dist[b][a]`, `dist[a][a]` = 0). Start at city 0, visit every other city exactly once and return to city 0; return the minimum total distance (0 for n = 1). Define `f[mask][last]` = minimum cost of a path that starts at 0, visits exactly the cities in `mask` and ends at `last`, give the transition, the answer `min(f[full][last] + dist[last][0])`, and the time O(2^n * n^2) and space O(2^n * n). Say why the (n-1)! permutation search is hopeless beyond n around 11 and what the DP buys. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every permutation of the other cities (n <= 8) on small inputs. Example: dist=[[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]] -> 80; dist=[[0]] -> 0; dist=[[0, 3], [5, 0]] -> 8; dist=[[0, 1, 9], [9, 0, 1], [1, 9, 0]] -> 3.
**Asked at:** Advanced DP pattern guides covering bitmask DP (techinterview.org advanced and optimisation DP pattern posts; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Bitmask DP basics (Held-Karp). The set of visited cities is an integer mask; the state adds the current city; transitions extend the path by one unvisited city.

**Say this first (1 line):** "`f[mask][last]` is the cheapest path that starts at city 0, visits exactly the cities in mask and ends at last; extend by one unvisited city, close the tour back to 0 at the end: O(2^n * n^2) time, O(2^n * n) space, against (n-1)! for trying all orders."

**Brute force:** Try every permutation of cities 1..n-1 as the visiting order, add the distances along `0 -> p1 -> ... -> p(n-1) -> 0` and take the minimum: (n-1)! tours (5,040 for n = 8, the oracle size). Distances may be asymmetric, so a tour and its reverse can differ and both are tried.

**Optimal:**
- State: bit c of `mask` is 1 when city c is visited; bit 0 is always set (the tour starts there). `f[mask][last]` = minimum cost of a path that starts at 0, visits exactly the cities in `mask` and ends at `last`.
- Base: `f[1][0] = 0` (only city 0, standing on it). Everything else is infinity until reached.
- Transition: from `(mask, last)` go to any city `nxt` not in the mask: `f[mask | 1<<nxt][nxt] = min(..., f[mask][last] + dist[last][nxt])`. Masks are processed in increasing numeric order, and a target mask is always larger than its source, so every state is final when it is read.
- Answer: close the tour: `min over last != 0 of f[full][last] + dist[last][0]`, where `full = 2^n - 1`. For n = 1 the answer is 0.
- Why O(2^n * n^2): there are 2^n masks times n values of `last` (about 2^(n-1) * n states reached) and each tries up to n next cities. Space O(2^n * n) for the table.
- Space reduction: city 0 is always in the mask, so leave it out and index by the other n - 1 cities (2^(n-1) masks instead of 2^n); the code does this as a second solver and checks it. Reconstructing a tour needs the whole table, the code recovers one tour by walking the table backwards.
- Memoised version: `g(mask, last)` = cheapest way to finish from here (the other direction), depth at most n <= 12, so no recursion-limit issue, and it agrees in the code.
- Why (n-1)! is hopeless beyond n around 11: the number of tours grows factorially. In the table printed by the run: 8 cities give 5,040 tours, 10 give 362,880, 11 give 3,628,800, 12 give 39,916,800, 13 give 479,001,600 and 15 give about 8.7 * 10^10. The DP step count at the same sizes is 16,384, 102,400, 247,808, 589,824, 1,384,448 and 7,372,800. In the sandbox the permutation search took 0.35 s at n = 10 against a few milliseconds for the DP (timings are sandbox-only, not proof; the growth is reasoned from the counts above). The cutoff of "about 11" is relative to an interview time limit of roughly a second or so; the DP handles n = 12 as a trivial case.
- What the DP buys: it notices that two different orders of the same set ending at the same city have the same future, so only the cheaper one is kept: subsets and an endpoint replace whole orders.

**Complexity:** Time O(2^n * n^2), space O(2^n * n) (halved by dropping city 0 from the mask). For n = 12: 4,096 masks * 12 endpoints = 49,152 states, under 600,000 transitions.

**Dry run:** `dist = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]`. Masks list the visited cities, always including 0; entry = cost ending at the given city (the run prints all of them):

| mask (cities) | f by ending city |
|---|---|
| {0} | 0 at city 0 |
| {0,1} | city 1: 10 |
| {0,2} | city 2: 15 |
| {0,3} | city 3: 20 |
| {0,1,2} | city 1: 15 + 35 = 50 (via 2); city 2: 10 + 35 = 45 (via 1) |
| {0,1,3} | city 1: 20 + 25 = 45; city 3: 10 + 25 = 35 |
| {0,2,3} | city 2: 20 + 30 = 50; city 3: 15 + 30 = 45 |
| {0,1,2,3} | city 1: 70 (from {0,2,3} ending 3: 45 + 25; ending 2 would give 50 + 35 = 85); city 2: 65 (from {0,1,3} ending 3: 35 + 30; ending 1 gives 45 + 35 = 80); city 3: 75 (from {0,1,2} ending 1: 50 + 25, or ending 2: 45 + 30, a tie) |

Closing the tour: ending at 1: 70 + 10 = 80; at 2: 65 + 15 = 80; at 3: 75 + 20 = 95. The minimum is 80, as in the prompt. One optimal tour is 0 -> 2 -> 3 -> 1 -> 0 (15 + 30 + 25 + 10).

**Code:**
```python
import itertools, math, random, sys, time
from functools import lru_cache

random.seed(3501)
INF = float("inf")


def tsp(dist):
    """f[mask][last] = cheapest path that starts at 0, visits exactly the cities in mask (bit 0 always set)
    and ends at last. Masks are filled in increasing order, so every predecessor mask is already final."""
    n = len(dist)
    if n == 1:
        return 0, None
    f = [[INF] * n for _ in range(1 << n)]
    f[1][0] = 0                                           # only city 0 visited, standing at 0
    for mask in range(1, 1 << n, 2):                      # odd masks = contain city 0
        for last in range(n):
            cur = f[mask][last]
            if cur == INF:
                continue
            for nxt in range(1, n):
                if not mask >> nxt & 1:
                    nm = mask | 1 << nxt
                    v = cur + dist[last][nxt]
                    if v < f[nm][nxt]:
                        f[nm][nxt] = v
    full = (1 << n) - 1
    return min(f[full][last] + dist[last][0] for last in range(1, n)), f


def tsp_halved(dist):
    """Same DP with city 0 left out of the mask: 2^(n-1) masks instead of 2^n (half the table)."""
    n = len(dist)
    if n == 1:
        return 0
    m = n - 1                                             # cities 1..n-1 get bits 0..m-1
    f = [[INF] * m for _ in range(1 << m)]
    for c in range(m):
        f[1 << c][c] = dist[0][c + 1]
    for mask in range(1, 1 << m):
        for last in range(m):
            cur = f[mask][last]
            if cur == INF:
                continue
            for nxt in range(m):
                if not mask >> nxt & 1:
                    nm = mask | 1 << nxt
                    v = cur + dist[last + 1][nxt + 1]
                    if v < f[nm][nxt]:
                        f[nm][nxt] = v
    return min(f[(1 << m) - 1][last] + dist[last + 1][0] for last in range(m))


def tsp_memo(dist):
    """Top-down, the other direction: g(mask, last) = cheapest way to finish from here. Depth n <= 12."""
    n = len(dist)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def g(mask, last):
        if mask == full:
            return dist[last][0]
        return min(dist[last][c] + g(mask | 1 << c, c) for c in range(n) if not mask >> c & 1)

    return 0 if n == 1 else g(1, 0)


def tsp_route(dist):
    """Follow-up: recover one optimal tour by walking the table backwards (ties: smallest previous city)."""
    n = len(dist)
    if n == 1:
        return 0, [0, 0]
    best, f = tsp(dist)
    full = (1 << n) - 1
    last = min((l for l in range(1, n) if f[full][l] + dist[l][0] == best))
    route, mask = [0], full
    while mask != 1:
        route.append(last)
        pm = mask ^ (1 << last)
        prev = next(p for p in range(n) if pm >> p & 1 and f[pm][p] + dist[p][last] == f[mask][last])
        mask, last = pm, prev
    route.append(0)
    route.reverse()
    return best, route


def brute(dist):
    n = len(dist)
    if n == 1:
        return 0
    return min(sum(dist[a][b] for a, b in zip((0,) + p, p + (0,))) for p in itertools.permutations(range(1, n)))


# ---- prompt examples
ex = [([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], 80),
      ([[0]], 0), ([[0, 3], [5, 0]], 8), ([[0, 1, 9], [9, 0, 1], [1, 9, 0]], 3)]
for d, want in ex:
    assert tsp(d)[0] == tsp_halved(d) == tsp_memo(d) == brute(d) == want, d
print("prompt examples OK")

# ---- hand table, first example: f[mask][last] (mask lists cities visited, city 0 always in it)
d = ex[0][0]
best, f = tsp(d)
print("f[mask][last]  (cities in mask, ending at last)")
for mask in range(1, 16, 2):
    cities = [c for c in range(4) if mask >> c & 1]
    cells = {l: f[mask][l] for l in range(4) if f[mask][l] != INF}
    print(f"  mask {mask:04b} {cities}: {cells}")
full = 15
print("closing:", {l: f"{f[full][l]}+{d[l][0]}={f[full][l] + d[l][0]}" for l in range(1, 4)}, "-> best", best)
print("one optimal tour:", tsp_route(d))

# ---- seeded cross-check against every permutation (n <= 8), asymmetric distances, many ties
cnt = 0
for _ in range(300):
    n = random.randint(1, 8)
    hi = random.choice([2, 10, 1000])
    d = [[0 if a == b else random.randint(0, hi) for b in range(n)] for a in range(n)]
    want = brute(d)
    assert tsp(d)[0] == tsp_halved(d) == tsp_memo(d) == want, (d, want)
    cost, route = tsp_route(d)
    assert cost == want and sorted(route[:-1]) == list(range(n)) and route[0] == route[-1] == 0
    if n > 1:
        assert sum(d[a][b] for a, b in zip(route, route[1:])) == want
    cnt += 1
print("random cross-check:", cnt, "matrices agree (also the half-size table, the memo and the recovered tour)")

# ---- the permutation search against the DP
print(" n | (n-1)! tours | 2^n * n^2 DP steps")
for n in (8, 10, 11, 12, 13, 15):
    print(f"{n:>2} | {math.factorial(n - 1):>13,} | {(1 << n) * n * n:>12,}")
rg = random.Random(3502)
for n in (9, 10):
    d = [[0 if a == b else rg.randint(0, 1000) for b in range(n)] for a in range(n)]
    t0 = time.perf_counter(); a = brute(d); t_b = time.perf_counter() - t0
    t0 = time.perf_counter(); b = tsp(d)[0]; t_d = time.perf_counter() - t0
    assert a == b
    print(f"n={n}: permutations {t_b:.2f}s, DP {t_d:.3f}s  [sandbox time only]")
d = [[0 if a == b else rg.randint(0, 1000) for b in range(12)] for a in range(12)]
t0 = time.perf_counter(); r12 = tsp(d)[0]; t_d = time.perf_counter() - t0
assert r12 == tsp_halved(d) == tsp_memo(d)
print(f"n=12: DP {t_d:.2f}s -> {r12}; 11! = {math.factorial(11):,} tours would need the permutation loop to run that many times (not run)")

# ---- edge cases
assert tsp([[0]])[0] == 0 and tsp([[0, 7], [2, 0]])[0] == 9
assert tsp([[0] * 5 for _ in range(5)])[0] == 0
assert tsp([[0 if a == b else 1000 for b in range(12)] for a in range(12)])[0] == 12000
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
f[mask][last]  (cities in mask, ending at last)
  mask 0001 [0]: {0: 0}
  mask 0011 [0, 1]: {1: 10}
  mask 0101 [0, 2]: {2: 15}
  mask 0111 [0, 1, 2]: {1: 50, 2: 45}
  mask 1001 [0, 3]: {3: 20}
  mask 1011 [0, 1, 3]: {1: 45, 3: 35}
  mask 1101 [0, 2, 3]: {2: 50, 3: 45}
  mask 1111 [0, 1, 2, 3]: {1: 70, 2: 65, 3: 75}
closing: {1: '70+10=80', 2: '65+15=80', 3: '75+20=95'} -> best 80
one optimal tour: (80, [0, 2, 3, 1, 0])
random cross-check: 300 matrices agree (also the half-size table, the memo and the recovered tour)
 n | (n-1)! tours | 2^n * n^2 DP steps
 8 |         5,040 |       16,384
10 |       362,880 |      102,400
11 |     3,628,800 |      247,808
12 |    39,916,800 |      589,824
13 |   479,001,600 |    1,384,448
15 | 87,178,291,200 |    7,372,800
n=9: permutations 0.03s, DP 0.001s  [sandbox time only]
n=10: permutations 0.32s, DP 0.003s  [sandbox time only]
n=12: DP 0.02s -> 911; 11! = 39,916,800 tours would need the permutation loop to run that many times (not run)
edge cases OK; limit 1000
```

**Edge cases:**
- n = 1: 0, no travel (the code special-cases it, since there is no `last != 0`).
- n = 2: `dist[0][1] + dist[1][0]` (`[[0,3],[5,0]]` gives 8: the matrix is asymmetric).
- Asymmetric distances: the direction matters; `[[0,1,9],[9,0,1],[1,9,0]]` gives 3 by going 0 -> 1 -> 2 -> 0 and would be 27 the other way round (0 -> 2 -> 1 -> 0: 9 + 9 + 9).
- All distances 0 or all equal: the answer is 0 or n * d.
- Zero-cost edges are fine (costs are only required to be non-negative by the prompt).
- Mask must always contain bit 0; starting from `f[0][0]` or a mask without bit 0 breaks the closing step.

**Follow-ups:**
- Print the tour? Walk the table backwards from the best `last` (the code does it): at each step find the previous city whose value plus the edge equals the current value.
- Dropping the return to city 0 (Hamiltonian path)? Answer `min over last of f[full][last]` and let every city be the start.
- n = 20? 2^20 * 20^2 = 4.2 * 10^8 steps is too slow in plain Python; use bit tricks or another language, or a heuristic when exactness is not required.

**Common mistakes:**
- Forgetting to add `dist[last][0]` for the return leg.
- Letting `last` equal 0 in the closing minimum for n > 1 (a path that visited everything must not end at 0 before closing).
- Iterating masks in the wrong order: transitions go to a larger mask, so ascending order is correct.
- Assuming symmetry: `dist[a][b] != dist[b][a]` is allowed.

