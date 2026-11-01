import itertools
import random

random.seed(2501)

def set_zeroes(matrix):
    """O(1) extra space: row 0 and column 0 are the marker arrays."""
    m, n = len(matrix), len(matrix[0])
    row0 = any(matrix[0][j] == 0 for j in range(n))      # saved BEFORE markers overwrite row 0
    col0 = any(matrix[i][0] == 0 for i in range(m))      # saved BEFORE markers overwrite col 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if row0:
        for j in range(n): matrix[0][j] = 0
    if col0:
        for i in range(m): matrix[i][0] = 0
    return matrix

def naive_markers(matrix):
    """The TRAP: marks for every zero (including row 0 / col 0 ones), then decides row 0 and col 0 from matrix[0][0]."""
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if matrix[0][0] == 0:
        for j in range(n): matrix[0][j] = 0
        for i in range(m): matrix[i][0] = 0
    return matrix

def two_sets(matrix):
    """O(m + n) extra space oracle: collect zero rows and columns, then write."""
    rows = {i for i, r in enumerate(matrix) if 0 in r}
    cols = {j for r in matrix for j, v in enumerate(r) if v == 0}
    return [[0 if i in rows or j in cols else v for j, v in enumerate(r)] for i, r in enumerate(matrix)]

def cp(x): return [r[:] for r in x]

examples = [([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
            ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
            ([[1, 2], [3, 4]], [[1, 2], [3, 4]]), ([[1, 0]], [[0, 0]])]
for mat, want in examples:
    a = cp(mat); r = set_zeroes(a)
    assert r is a and a == want == two_sets(mat)           # in place AND returned
    print(mat, '->', a)

# dry run: example 1, stage by stage
mat = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
print('row0 has zero:', any(v == 0 for v in mat[0]), ' col0 has zero:', any(r[0] == 0 for r in mat))
mark = cp(mat)
mark[1][0] = mark[0][1] = 0                  # the only inner zero is (1,1): mark its row and column
print('after marking :', mark)
for i in range(1, 3):
    for j in range(1, 3):
        if mark[i][0] == 0 or mark[0][j] == 0: mark[i][j] = 0
print('after inner pass:', mark, '(row 0 and col 0 hold the zeros their markers made; both saved flags are False, so nothing more to do)')

# seeded random cross-check against the two-set version (values 0..3, zeros common)
for _ in range(3000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.choice([0, 0, 1, 2, 3]) for _ in range(n)] for _ in range(m)]
    a = cp(mat)
    assert set_zeroes(a) == two_sets(mat)
print('random cross-check ok: 3000 cases')

# exhaustive over every binary matrix of shapes up to 3 x 3 (and 1 x n, m x 1 up to 6)
shapes = [(m, n) for m in range(1, 4) for n in range(1, 4)] + [(1, 6), (6, 1), (2, 5), (5, 2)]
total = 0
wrong = 0
first_bad = None
for m, n in shapes:
    for cells in itertools.product((0, 1), repeat=m * n):
        mat = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
        want = two_sets(mat)
        assert set_zeroes(cp(mat)) == want
        total += 1
        if (m, n) == (3, 3):
            if naive_markers(cp(mat)) != want:
                wrong += 1
                if first_bad is None or sum(map(sum, mat)) > sum(map(sum, first_bad)):
                    first_bad = mat
print('correct version exhaustive ok:', total, 'binary matrices over', len(shapes), 'shapes')
print('naive marker version wrong on', wrong, 'of 512 binary 3x3 matrices')
bad = [[1, 1, 1], [0, 1, 1], [1, 0, 1]]
print('failing input :', bad)
print('naive returns :', naive_markers(cp(bad)))
print('correct       :', two_sets(bad))
assert wrong == 42 and naive_markers(cp(bad)) != two_sets(bad)

# edge asserts: zero at the corner, whole zero matrix, single cell, non-binary values stay
assert set_zeroes([[0]]) == [[0]] and set_zeroes([[7]]) == [[7]]
assert set_zeroes([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
assert set_zeroes([[5, 6, 7], [8, 0, 9]]) == [[5, 0, 7], [0, 0, 0]]
big = [[1] * 200 for _ in range(200)]; big[199][199] = 0
r = set_zeroes(big)
assert sum(map(sum, r)) == 199 * 199
print('edge asserts ok')
