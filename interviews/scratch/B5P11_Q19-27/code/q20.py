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
