import random, itertools, sys

random.seed(25)

def falling(matrix):
    """One row. dp[c] = cheapest path sum ending at column c of the current row."""
    n = len(matrix)
    dp = list(matrix[0])                                      # base: row 0, any start
    for r in range(1, n):
        dp = [matrix[r][c] + min(dp[max(0, c - 1):c + 2])     # columns c-1, c, c+1, clipped at the edges by the slice
              for c in range(n)]
    return min(dp)                                            # end anywhere in the last row

def falling_explicit(matrix):
    """Same, with the edge handling written out (no slicing trick)."""
    n = len(matrix)
    dp = matrix[0][:]
    for r in range(1, n):
        new = []
        for c in range(n):
            best = dp[c]
            if c > 0: best = min(best, dp[c - 1])
            if c < n - 1: best = min(best, dp[c + 1])
            new.append(matrix[r][c] + best)
        dp = new
    return min(dp)

def brute(matrix):
    """Plain recursion, no memo."""
    n = len(matrix)
    def f(r, c):
        if r == n - 1: return matrix[r][c]
        return matrix[r][c] + min(f(r + 1, k) for k in (c - 1, c, c + 1) if 0 <= k < n)
    return min(f(0, c) for c in range(n))

def wrong_wraparound(matrix):
    """Bug: dp[c-1] at c = 0 is dp[-1], the LAST column, which is not a legal move."""
    n = len(matrix); dp = matrix[0][:]
    for r in range(1, n):
        dp = [matrix[r][c] + min(dp[c - 1], dp[c], dp[(c + 1) % n]) for c in range(n)]
    return min(dp)

def wrong_greedy(matrix):
    """Bug: start at the smallest top cell and keep stepping to the smallest reachable cell."""
    n = len(matrix); c = matrix[0].index(min(matrix[0])); tot = matrix[0][c]
    for r in range(1, n):
        c = min((k for k in (c - 1, c, c + 1) if 0 <= k < n), key=lambda k: matrix[r][k]); tot += matrix[r][c]
    return tot

# examples
for mat, exp in [([[2, 1, 3], [6, 5, 4], [7, 8, 9]], 13), ([[-19, 57], [-40, -5]], -59), ([[5]], 5)]:
    a, b, c = falling(mat), falling_explicit(mat), brute(mat)
    assert a == b == c == exp, (mat, a, b, c)
    print('example', mat, '->', a)

# hand table
mat = [[2, 1, 3], [6, 5, 4], [7, 8, 9]]
dp = mat[0][:]
print('row 0: dp =', dp)
for r in range(1, 3):
    print('row %d:' % r, end=' ')
    new = []
    for c in range(3):
        cand = [dp[k] for k in (c - 1, c, c + 1) if 0 <= k < 3]
        new.append(mat[r][c] + min(cand)); print('c=%d: %d + min%s = %d;' % (c, mat[r][c], cand, new[-1]), end=' ')
    dp = new; print('-> dp =', dp)
print('answer min(dp) =', min(dp))

# seeded cross-check, n <= 5
cases = 0; wa = gr = 0
for _ in range(600):
    n = random.randint(1, 5)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    exp = brute(mat)
    assert falling(mat) == falling_explicit(mat) == exp, mat
    wa += wrong_wraparound(mat) != exp; gr += wrong_greedy(mat) != exp
    cases += 1
print('cross-check cases', cases, '| wrap-around bug wrong on', wa, '| greedy wrong on', gr)

# edge cases
assert falling([[5]]) == 5 and falling([[-100] * 100 for _ in range(100)]) == -10000
assert falling([[100] * 100 for _ in range(100)]) == 10000
big = [[random.randint(-100, 100) for _ in range(100)] for _ in range(100)]
assert falling(big) == falling_explicit(big)
print('100 x 100 random:', falling(big))
print('recursion limit', sys.getrecursionlimit(), '| a memoised recursion here nests n = 100 frames, far below it')
print('edge asserts passed')
