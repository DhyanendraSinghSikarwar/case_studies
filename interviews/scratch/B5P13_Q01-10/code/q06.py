import random, copy

def brute(matrix):                                       # new matrix, O(n^2) extra space
    return [list(r) for r in zip(*matrix[::-1])]

def optimal(matrix):                                     # transpose, then reverse each row
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix

def cycles(matrix):                                      # alternative: rotate 4-cell cycles
    n = len(matrix)
    for i in range(n // 2):
        for j in range((n + 1) // 2):
            tmp = matrix[n - 1 - j][i]
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]
            matrix[j][n - 1 - i] = matrix[i][j]
            matrix[i][j] = tmp
    return matrix

ex = [([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
      ([[5]], [[5]]), ([[1, 2], [3, 4]], [[3, 1], [4, 2]]),
      ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
       [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]])]
for M, want in ex:
    m = copy.deepcopy(M)
    got = optimal(m)
    assert got is m and got == want == brute(M) == cycles(copy.deepcopy(M))
    print(M, '->', got)

random.seed(6)
for _ in range(500):
    n = random.randint(1, 7)
    M = [[random.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    a = copy.deepcopy(M)
    assert optimal(a) == brute(M) == cycles(copy.deepcopy(M))
print('random cross-check ok: 500 cases (transpose+reverse, cycles, zip all agree)')

# claims, exhaustive over n = 1..9 with distinct labels
for n in range(1, 10):
    M = [[i * n + j for j in range(n)] for i in range(n)]
    cw = optimal(copy.deepcopy(M))
    assert all(cw[j][n - 1 - i] == M[i][j] for i in range(n) for j in range(n))   # (i,j) -> (j, n-1-i)
    # anticlockwise = transpose, then reverse the order of the rows
    ccw = [list(r) for r in zip(*M)][::-1]
    assert optimal(optimal(optimal(copy.deepcopy(M)))) == ccw
    seen = set()
    for i in range(n // 2):
        for j in range((n + 1) // 2):
            cyc = {(i, j), (j, n - 1 - i), (n - 1 - i, n - 1 - j), (n - 1 - j, i)}
            assert len(cyc) == 4 and not (cyc & seen)
            seen |= cyc
    assert len(seen) == n * n - n % 2                     # centre cell of odd n is left out
    assert (n // 2) * ((n + 1) // 2) * 4 == n * n - n % 2
print('claims ok for n=1..9: destination (j, n-1-i), anticlockwise recipe, 4-cycles cover each cell once, centre stays')
# four turns = identity
M = [[random.randint(0, 99) for _ in range(5)] for _ in range(5)]
r = copy.deepcopy(M)
for _ in range(4):
    optimal(r)
assert r == M
# max size
M = [[random.randint(-9, 9) for _ in range(200)] for _ in range(200)]
assert optimal(copy.deepcopy(M)) == brute(M)
print('max size 200x200 ok; four turns restore the matrix')
