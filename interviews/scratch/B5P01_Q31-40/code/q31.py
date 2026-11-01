import random
from copy import deepcopy


def brute(mat):
    """Reference: collect zero rows/cols in two sets (O(m+n) space)."""
    m, n = len(mat), len(mat[0])
    rows = {i for i in range(m) for j in range(n) if mat[i][j] == 0}
    cols = {j for i in range(m) for j in range(n) if mat[i][j] == 0}
    return [[0 if (i in rows or j in cols) else mat[i][j] for j in range(n)] for i in range(m)]


def set_zeroes(mat):
    """O(1) extra space: row 0 / col 0 are the markers, two flags save their own fate."""
    m, n = len(mat), len(mat[0])
    first_row_zero = any(mat[0][j] == 0 for j in range(n))
    first_col_zero = any(mat[i][0] == 0 for i in range(m))
    for i in range(1, m):                      # record zeros of the inner block
        for j in range(1, n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
    for i in range(1, m):                      # apply markers to the inner block
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    if first_row_zero:                         # markers last, using the flags
        for j in range(n):
            mat[0][j] = 0
    if first_col_zero:
        for i in range(m):
            mat[i][0] = 0
    return mat


# Prompt example
ex = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
print("prompt example:", set_zeroes(ex))
assert ex == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

# Why the flags matter: the naive version (no flags) zeroes everything
def naive_no_flags(mat):
    m, n = len(mat), len(mat[0])
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                mat[i][j] = 0
    return mat

tricky = [[1, 0, 3], [4, 5, 6], [7, 8, 9]]   # zero lives in the first row
print("naive (no flags)  :", naive_no_flags(deepcopy(tricky)))
assert naive_no_flags(deepcopy(tricky)) != set_zeroes(deepcopy(tricky))
print("correct (two flags):", set_zeroes(deepcopy(tricky)))
tricky2 = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
print("naive on zero at [0][0]:", naive_no_flags(deepcopy(tricky2)))
print("zero at [0][0], correct:", set_zeroes(deepcopy(tricky2)))

# Edge cases
assert set_zeroes([[0]]) == [[0]]
assert set_zeroes([[5]]) == [[5]]
assert set_zeroes([[1, 0, 3]]) == [[0, 0, 0]]
assert set_zeroes([[1], [0], [3]]) == [[0], [0], [0]]
assert set_zeroes([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
assert set_zeroes([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
assert set_zeroes([[-1, 0], [2, -3]]) == [[0, 0], [2, 0]]
assert set_zeroes(deepcopy(tricky2)) == [[0, 0, 0], [0, 4, 5], [0, 7, 8]]

# Seeded randomised cross-check (zero-heavy and zero-light matrices, many shapes)
rng = random.Random(31)
for _ in range(1500):
    m, n = rng.randint(1, 6), rng.randint(1, 6)
    p = rng.choice([0.05, 0.2, 0.5])
    mat = [[0 if rng.random() < p else rng.randint(-5, 5) or 7 for _ in range(n)] for _ in range(m)]
    expect = brute(mat)
    got = set_zeroes(deepcopy(mat))
    assert got == expect, (mat, got, expect)
print("cross-check passed: 1500 random matrices")
