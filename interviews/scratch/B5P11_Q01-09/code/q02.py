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
