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
