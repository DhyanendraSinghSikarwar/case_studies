import itertools
import random

random.seed(1105)

def max_square_table(matrix):
    """side[i][j] = side of the largest all-ones square with bottom-right corner (i, j). Padded with a 0 row/col."""
    m, n = len(matrix), len(matrix[0])
    side = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                side[i][j] = 1 + min(side[i - 1][j], side[i][j - 1], side[i - 1][j - 1])
                best = max(best, side[i][j])
    return side, best * best

def max_square_two_rows(matrix):
    n = len(matrix[0])
    prev = [0] * (n + 1)
    best = 0
    for row in matrix:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if row[j - 1] == '1':
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
                best = max(best, cur[j])
        prev = cur
    return best * best

def max_square_one_row(matrix):
    """One row plus a saved diagonal: diag = old row[j-1] (the up-left value) before it is overwritten."""
    n = len(matrix[0])
    row = [0] * (n + 1)
    best = 0
    for r in matrix:
        diag = 0                                    # up-left of column 1 is the padding 0
        for j in range(1, n + 1):
            up = row[j]                             # old value = cell above
            if r[j - 1] == '1':
                row[j] = 1 + min(up, row[j - 1], diag)   # row[j-1] already new = left
                best = max(best, row[j])
            else:
                row[j] = 0                          # MUST reset: stale 'up' would otherwise survive
            diag = up
    return best * best

def max_square_no_diag(matrix):
    """WRONG on purpose: min(up, left) only."""
    m, n = len(matrix), len(matrix[0])
    side = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == '1':
                side[i][j] = 1 + min(side[i - 1][j], side[i][j - 1])
                best = max(best, side[i][j])
    return best * best

def max_square_brute(matrix):
    """Oracle: try every top-left corner and every side length, check all cells."""
    m, n = len(matrix), len(matrix[0])
    best = 0
    for i in range(m):
        for j in range(n):
            for k in range(1, min(m - i, n - j) + 1):
                if all(matrix[a][b] == '1' for a in range(i, i + k) for b in range(j, j + k)):
                    best = max(best, k)
    return best * best

for mat, want in [(['10100', '10111', '11111', '10010'], 4), (['01', '10'], 1), (['0'], 0), (['11', '11'], 4)]:
    assert max_square_table(mat)[1] == max_square_two_rows(mat) == max_square_one_row(mat) == max_square_brute(mat) == want, mat
print("4 prompt examples ok")

mat = ['10100', '10111', '11111', '10010']
print("walk-through matrix:", mat)
side, area = max_square_table(mat)
for r in side[1:]:
    print("  side row:", r[1:])
print("  largest side", int(area ** 0.5), "-> area", area)

def grids(m, n):
    for cells in itertools.product('01', repeat=m * n):
        yield [''.join(cells[i * n:(i + 1) * n]) for i in range(m)]

cnt = 0
for m in range(1, 5):
    for n in range(1, 5):
        for g in grids(m, n):
            b = max_square_brute(g)
            assert max_square_table(g)[1] == max_square_two_rows(g) == max_square_one_row(g) == b, g
            cnt += 1
print("exhaustive: all", cnt, "binary matrices with m, n in 1..4: table == two rows == one row == brute force")
for _ in range(500):
    m, n = random.randint(1, 6), random.randint(1, 6)
    p = random.choice([0.5, 0.8, 0.95])
    g = [''.join('1' if random.random() < p else '0' for _ in range(n)) for _ in range(m)]
    assert max_square_two_rows(g) == max_square_brute(g) == max_square_one_row(g)
print("500 seeded random matrices (m, n <= 6, density 50/80/95%): ok")

# claim: dropping the up-left term is wrong; find where
bad = [g for g in grids(3, 3) if max_square_no_diag(g) != max_square_brute(g)]
print("min(up, left) without up-left is wrong on", len(bad), "of 512 3x3 matrices; e.g.", bad[0], "gives", max_square_no_diag(bad[0]), "not", max_square_brute(bad[0]))

big = [''.join('1' if random.random() < 0.97 else '0' for _ in range(300)) for _ in range(300)]
a = max_square_two_rows(big)
assert a == max_square_table(big)[1] == max_square_one_row(big)
print("300 x 300 (97% ones): largest square area", a, "(side", int(a ** 0.5), "); table == two rows == one row")
full = ['1' * 300] * 300
print("300 x 300 all ones:", max_square_two_rows(full), "= 300^2:", max_square_two_rows(full) == 90000)
