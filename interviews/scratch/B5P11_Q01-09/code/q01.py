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
