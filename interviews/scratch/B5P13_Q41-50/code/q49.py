import random, collections, time
random.seed(49)

# ---- optimal: cells of each ring in clockwise order from the top-left corner, rotate the flat list by r % L
def ring_cells(m, n, k):
    t, b, l, r = k, m - 1 - k, k, n - 1 - k
    return ([(t, j) for j in range(l, r + 1)] + [(i, r) for i in range(t + 1, b + 1)]
            + [(b, j) for j in range(r - 1, l - 1, -1)] + [(i, l) for i in range(b - 1, t, -1)])

def rotate_layers(matrix, r):
    m, n = len(matrix), len(matrix[0]); out = [row[:] for row in matrix]
    for k in range(min(m, n) // 2):
        cells = ring_cells(m, n, k); L = len(cells)
        vals = [matrix[i][j] for i, j in cells]; s = r % L
        for idx, (i, j) in enumerate(cells):
            out[i][j] = vals[(idx + s) % L]        # the value at position idx + s moves to position idx
    return out

# ---- independent check 1: ring positions found by WALKING (direction vectors), values rotated with a deque
def rotate_walk(matrix, r):
    m, n = len(matrix), len(matrix[0]); out = [row[:] for row in matrix]
    for k in range(min(m, n) // 2):
        h, w = m - 2 * k, n - 2 * k; L = 2 * (h + w) - 4
        pos = []; i = j = k
        for di, dj, steps in ((0, 1, w - 1), (1, 0, h - 1), (0, -1, w - 1), (-1, 0, h - 1)):
            for _ in range(steps): pos.append((i, j)); i += di; j += dj
        assert len(pos) == L and len(set(pos)) == L and (i, j) == (k, k)
        dq = collections.deque(matrix[a][b] for a, b in pos); dq.rotate(-(r % L))   # counter-clockwise by r
        for (a, b), v in zip(pos, dq): out[a][b] = v
    return out

# ---- independent check 2: simulate r single steps (only for small r)
def rotate_steps(matrix, r):
    cur = [row[:] for row in matrix]
    for _ in range(r): cur = rotate_layers(cur, 1)
    return cur

# ---- examples
g4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
assert rotate_layers(g4, 2) == [[3, 4, 8, 12], [2, 11, 10, 16], [1, 7, 6, 15], [5, 9, 13, 14]]
assert rotate_layers([[1, 2], [3, 4]], 1) == [[2, 4], [1, 3]]
assert rotate_layers([[1, 2, 3, 4], [5, 6, 7, 8]], 3) == [[4, 8, 7, 6], [3, 2, 1, 5]]
print('examples ok:', rotate_layers(g4, 2), rotate_layers([[1, 2], [3, 4]], 1), rotate_layers([[1, 2, 3, 4], [5, 6, 7, 8]], 3))

# ---- seeded random cross-check: walk + deque version, and single-step simulation for r <= 40
def rand_grid(m, n): return [[random.randint(0, 99) for _ in range(n)] for _ in range(m)]
for _ in range(1500):
    m, n = random.randint(2, 9), random.randint(2, 9)
    while min(m, n) % 2: m, n = random.randint(2, 9), random.randint(2, 9)
    g = rand_grid(m, n); r = random.choice([0, 1, 2, 3, 7, 40, random.randint(0, 10**9)])
    a = rotate_layers(g, r); assert a == rotate_walk(g, r)
    if r <= 40: assert a == rotate_steps(g, r)
print('1500 random even-min grids: flat-list rotation == walk + deque == r single steps (r <= 40)')

# ---- structural claims, checked
for m in range(2, 11):
    for n in range(2, 11):
        if min(m, n) % 2: continue
        cells = [c for k in range(min(m, n) // 2) for c in ring_cells(m, n, k)]
        assert len(cells) == m * n == len(set(cells))                        # the rings partition the matrix exactly
print('even min(m, n): rings cover every cell of every grid with 2 <= m, n <= 10 exactly once')
dup = ring_cells(3, 4, 1)
print('odd min (3 x 4): layer 1 is a single row; the generator lists', dup, '-> the cell (1, 1) appears twice, so it is not a ring')
g = rand_grid(6, 4); L = 2 * (6 + 4) - 4
assert rotate_layers(g, L * 5) == g and rotate_layers(rotate_layers(g, 3), 4) == rotate_layers(g, 7)
print('rotating by the ring length is the identity; rotating by 3 then 4 equals rotating by 7 (ring lengths differ per layer: here 16 and 8)')

# ---- maximum size, r = 10^9: never simulate r steps
big = [[i * 300 + j for j in range(300)] for i in range(300)]
t = time.perf_counter(); res = rotate_layers(big, 10**9); dt = time.perf_counter() - t
assert sorted(v for row in res for v in row) == list(range(90000))
print('300 x 300 with r = 10^9: a permutation of the values, rings of length 1196 down to 4 (sandbox timing about %.2f s)' % dt)

# ---- edge asserts
assert rotate_layers([[1, 2], [3, 4]], 0) == [[1, 2], [3, 4]]
assert rotate_layers([[1, 2], [3, 4]], 4) == [[1, 2], [3, 4]]
assert rotate_layers([[1, 2], [3, 4], [5, 6], [7, 8]], 1) == [[2, 4], [1, 6], [3, 8], [5, 7]]
print('edge asserts ok')
