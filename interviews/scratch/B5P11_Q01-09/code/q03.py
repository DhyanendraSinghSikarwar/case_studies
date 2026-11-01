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
