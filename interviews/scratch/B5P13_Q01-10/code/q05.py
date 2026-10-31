import random

def brute(matrix, queries):
    return [sum(matrix[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
            for r1, c1, r2, c2 in queries]

def optimal(matrix, queries):
    m, n = len(matrix), len(matrix[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]            # zero row 0 and zero column 0
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = matrix[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    return [P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
            for r1, c1, r2, c2 in queries]

ex = [([[3, 0, 1], [5, 6, 3], [1, 2, 0]], [[0, 0, 2, 2], [1, 1, 2, 2], [1, 0, 1, 0]], [21, 11, 5]),
      ([[-4]], [[0, 0, 0, 0]], [-4]),
      ([[1, 2], [3, 4]], [[0, 1, 1, 1], [0, 0, 0, 1]], [6, 3])]
for M, qs, want in ex:
    got = optimal(M, qs)
    assert got == want == brute(M, qs)
    print(M, qs, '->', got)

random.seed(5)
for _ in range(500):
    m, n = random.randint(1, 6), random.randint(1, 6)
    M = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    qs = []
    for _ in range(random.randint(0, 8)):
        r1 = random.randint(0, m - 1); r2 = random.randint(r1, m - 1)
        c1 = random.randint(0, n - 1); c2 = random.randint(c1, n - 1)
        qs.append([r1, c1, r2, c2])
    assert optimal(M, qs) == brute(M, qs)
print('random cross-check ok: 500 cases')

# exhaustive: every rectangle of a fixed 4 x 5 matrix
M = [[random.randint(-9, 9) for _ in range(5)] for _ in range(4)]
allq = [[a, b, c, d] for a in range(4) for c in range(a, 4) for b in range(5) for d in range(b, 5)]
assert optimal(M, allq) == brute(M, allq)
print('all', len(allq), 'rectangles of a 4x5 matrix ok')

# max-size: 200 x 200, whole-matrix query equals sum of everything; |value| <= 10^4
M = [[random.randint(-10**4, 10**4) for _ in range(200)] for _ in range(200)]
assert optimal(M, [[0, 0, 199, 199]]) == [sum(map(sum, M))]
assert optimal(M, [[0, 0, 0, 0], [199, 199, 199, 199]]) == [M[0][0], M[199][199]]
print('max size 200x200 ok')
