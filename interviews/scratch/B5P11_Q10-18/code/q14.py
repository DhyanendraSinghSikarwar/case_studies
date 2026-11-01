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
