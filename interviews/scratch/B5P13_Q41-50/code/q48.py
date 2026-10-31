import random, time
random.seed(48)

# ---- optimal: (n+1) x (n+1) difference matrix, four corner updates per query, then two prefix passes
def add_rectangles(n, queries, rows_first=True):
    d = [[0] * (n + 1) for _ in range(n + 1)]
    for r1, c1, r2, c2 in queries:
        d[r1][c1] += 1; d[r1][c2 + 1] -= 1; d[r2 + 1][c1] -= 1; d[r2 + 1][c2 + 1] += 1
    def rows():
        for i in range(n + 1):
            for j in range(1, n + 1): d[i][j] += d[i][j - 1]
    def cols():
        for j in range(n + 1):
            for i in range(1, n + 1): d[i][j] += d[i - 1][j]
    if rows_first: rows(); cols()
    else: cols(); rows()
    return [row[:n] for row in d[:n]]

# ---- brute force: touch every cell of every rectangle
def brute(n, queries):
    a = [[0] * n for _ in range(n)]
    for r1, c1, r2, c2 in queries:
        for i in range(r1, r2 + 1):
            for j in range(c1, c2 + 1): a[i][j] += 1
    return a

# ---- examples
assert add_rectangles(3, [[1, 1, 2, 2], [0, 0, 1, 1]]) == [[1, 1, 0], [1, 2, 1], [0, 1, 1]]
assert add_rectangles(2, [[0, 0, 1, 1]]) == [[1, 1], [1, 1]]
assert add_rectangles(1, []) == [[0]]
print('examples ok:', add_rectangles(3, [[1, 1, 2, 2], [0, 0, 1, 1]]), add_rectangles(2, [[0, 0, 1, 1]]), add_rectangles(1, []))

# ---- seeded random cross-check against cell-by-cell updates, both pass orders
def rand_query(n):
    r1 = random.randrange(n); r2 = random.randint(r1, n - 1); c1 = random.randrange(n); c2 = random.randint(c1, n - 1)
    return [r1, c1, r2, c2]
for _ in range(2000):
    n = random.randint(1, 8); qs = [rand_query(n) for _ in range(random.randint(0, 10))]
    want = brute(n, qs)
    assert add_rectangles(n, qs, True) == want and add_rectangles(n, qs, False) == want
print('2000 random cases: difference matrix == cell-by-cell, and rows-first == columns-first')

# ---- the single-corner picture: one rectangle leaves exactly the rectangle after the passes
n = 6
for _ in range(200):
    q = rand_query(n); m = add_rectangles(n, [q])
    r1, c1, r2, c2 = q
    assert all(m[i][j] == (1 if r1 <= i <= r2 and c1 <= j <= c2 else 0) for i in range(n) for j in range(n))
print('one rectangle at a time: the matrix is 1 inside and 0 outside, 200 cases')

# ---- maximum size: n = 500, 10^4 queries; count the work instead of running the brute force
n = 500; qs = [rand_query(n) for _ in range(10000)]
cells = sum((r2 - r1 + 1) * (c2 - c1 + 1) for r1, c1, r2, c2 in qs)
t = time.perf_counter(); res = add_rectangles(n, qs); dt = time.perf_counter() - t
assert sum(map(sum, res)) == cells                     # the total added equals the total area of all rectangles
ops_fast = 4 * len(qs) + 2 * (n + 1) ** 2
print('n = 500, 10000 random rectangles: cell updates by brute force =', cells, '; difference-matrix operations about', ops_fast)
print('(sandbox timing for the difference matrix: about %.2f s)' % dt)

# ---- edge asserts
assert add_rectangles(3, [[0, 0, 2, 2]]) == [[1] * 3] * 3           # corners on the border: d[n][*] and d[*][n] are written, then dropped
assert add_rectangles(3, [[2, 2, 2, 2]]) == [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
assert add_rectangles(2, [[0, 0, 0, 0]] * 3) == [[3, 0], [0, 0]]    # repeated query
assert add_rectangles(4, [[0, 1, 3, 1]]) == [[0, 1, 0, 0]] * 4      # a full-height column
print('edge asserts ok')
