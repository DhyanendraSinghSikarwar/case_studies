import itertools
import random

random.seed(2401)

def block_sum(mat, k):
    m, n = len(mat), len(mat[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]        # P[i][j] = sum of mat[:i][:j]
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = mat[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            r1, r2 = max(0, i - k), min(m - 1, i + k)      # clip to the matrix
            c1, c2 = max(0, j - k), min(n - 1, j + k)
            row.append(P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1])
        out.append(row)
    return out

def brute(mat, k, count=None):
    m, n = len(mat), len(mat[0])
    visits = 0
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            s = 0
            for r in range(max(0, i - k), min(m - 1, i + k) + 1):
                for c in range(max(0, j - k), min(n - 1, j + k) + 1):
                    s += mat[r][c]; visits += 1
            row.append(s)
        out.append(row)
    if count is not None:
        count.append(visits)
    return out

G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
examples = [(G, 1, [[12, 21, 16], [27, 45, 33], [24, 39, 28]]),
            (G, 2, [[45] * 3] * 3), ([[5]], 3, [[5]]), ([[1, 2], [3, 4]], 0, [[1, 2], [3, 4]])]
for mat, k, want in examples:
    assert block_sum(mat, k) == want == brute(mat, k)
    print('k =', k, mat, '->', block_sum(mat, k))

# dry run: the prefix table of G and the cell (0, 0) with k = 1
P = [[0] * 4 for _ in range(4)]
for i in range(3):
    for j in range(3):
        P[i + 1][j + 1] = G[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
print('prefix table:', P)
print('cell (0,0), k=1: rows 0..1, cols 0..1 ->', P[2][2], '-', P[0][2], '-', P[2][0], '+', P[0][0], '=', P[2][2] - P[0][2] - P[2][0] + P[0][0])

# seeded random cross-check
for _ in range(2000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    k = random.randint(0, 7)
    assert block_sum(mat, k) == brute(mat, k)
print('random cross-check ok: 2000 cases')

# exhaustive: every 2 x 3 matrix over {-1,0,1} and k = 0..3
cnt = 0
for cells in itertools.product((-1, 0, 1), repeat=6):
    mat = [list(cells[:3]), list(cells[3:])]
    for k in range(4):
        assert block_sum(mat, k) == brute(mat, k); cnt += 1
print('exhaustive 2x3 ok:', cnt, 'cases')

# cost: cell reads of the direct method (from the clipped square sizes) versus 4 table reads per cell
def clipped_cells(m, n, k):          # number of cell reads the direct method makes
    rows = sum(min(m - 1, i + k) - max(0, i - k) + 1 for i in range(m))
    cols = sum(min(n - 1, j + k) - max(0, j - k) + 1 for j in range(n))
    return rows * cols
for m, n, k in [(100, 100, 1), (100, 100, 10), (100, 100, 100)]:
    print(f'{m}x{n}, k={k}: direct reads {clipped_cells(m, n, k)} cells; prefix table: 4 reads per cell = {4 * m * n}')
mat = [[random.randint(-5, 5) for _ in range(7)] for _ in range(6)]
v = []
brute(mat, 2, v)
assert v[0] == clipped_cells(6, 7, 2)
big = [[random.randint(-100, 100) for _ in range(100)] for _ in range(100)]
assert block_sum(big, 100) == [[sum(map(sum, big))] * 100] * 100          # whole-matrix sum everywhere
assert block_sum([[7]], 100) == [[7]]
print('edge asserts ok')
