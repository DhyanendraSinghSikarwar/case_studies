import random

def brute(matrix):                                       # visited set + direction turning, O(mn) extra space
    m, n = len(matrix), len(matrix[0])
    seen, out, i, j, di, dj = set(), [], 0, 0, 0, 1
    for _ in range(m * n):
        out.append(matrix[i][j]); seen.add((i, j))
        ni, nj = i + di, j + dj
        if not (0 <= ni < m and 0 <= nj < n and (ni, nj) not in seen):
            di, dj = dj, -di                             # turn right
            ni, nj = i + di, j + dj
        i, j = ni, nj
    return out

def optimal(matrix):                                     # four boundaries, O(1) extra space
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            out.append(matrix[top][j])
        for i in range(top + 1, bottom + 1):
            out.append(matrix[i][right])
        if top < bottom and left < right:                # guard: layer has 2+ rows AND 2+ columns
            for j in range(right - 1, left - 1, -1):
                out.append(matrix[bottom][j])
            for i in range(bottom - 1, top, -1):
                out.append(matrix[i][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out

def no_guard(matrix):                                    # the classic bug
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for j in range(left, right + 1): out.append(matrix[top][j])
        for i in range(top + 1, bottom + 1): out.append(matrix[i][right])
        for j in range(right - 1, left - 1, -1): out.append(matrix[bottom][j])
        for i in range(bottom - 1, top, -1): out.append(matrix[i][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out

ex = [([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
      ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]),
      ([[1], [2], [3]], [1, 2, 3]), ([[1, 2, 3]], [1, 2, 3])]
for M, want in ex:
    got = optimal(M)
    assert got == want == brute(M)
    print(M, '->', got)

random.seed(7)
for _ in range(500):
    m, n = random.randint(1, 6), random.randint(1, 6)
    M = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    assert optimal(M) == brute(M)
print('random cross-check ok: 500 cases')

# exhaustive over every shape up to 9 x 9: each cell exactly once, and the guard matters
bad = []
for m in range(1, 10):
    for n in range(1, 10):
        M = [[i * n + j for j in range(n)] for i in range(m)]
        assert sorted(optimal(M)) == list(range(m * n)) and optimal(M) == brute(M)
        if len(no_guard(M)) != m * n:
            bad.append((m, n))
print('shapes where the unguarded version returns the wrong length:', bad[:6], '...', len(bad), 'of 81')
# exact rule: the innermost layer is a single row of 2+ cells or a single column of 3+ cells
# (min(m, n) odd, and n > m, or m - n >= 2)
rule = {(m, n) for m in range(1, 10) for n in range(1, 10) if min(m, n) % 2 == 1 and (n > m or m - n >= 2)}
assert set(bad) == rule
print('bad shapes match the rule exactly:', len(rule), 'shapes; 2 x 1 and 1 x 1 are fine:', (2, 1) not in bad and (1, 1) not in bad)
