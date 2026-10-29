import random, itertools, sys, time
from math import comb

random.seed(27)
MOD = 10**9 + 7

def count_paths(grid, k, mod=MOD):
    """dp[j][r] = number of paths to (current row, j) whose sum has remainder r mod k. One row of k-vectors."""
    m, n = len(grid), len(grid[0])
    dp = [[0] * k for _ in range(n)]
    for i in range(m):
        new = [[0] * k for _ in range(n)]
        for j in range(n):
            v = grid[i][j] % k
            if i == 0 and j == 0:
                new[0][v] = 1                                   # base: the start cell alone, sum % k = grid[0][0] % k
                continue
            cell = new[j]
            for src in ((dp[j] if i else None), (new[j - 1] if j else None)):   # from above, from the left
                if src is None:
                    continue
                for r in range(k):
                    c = src[r]
                    if c:
                        t = (r + v) % k
                        cell[t] = (cell[t] + c) % mod if mod else cell[t] + c
        dp = new
    return dp[n - 1][0]

def count_paths_full(grid, k, mod=MOD):
    """3D table dp[i][j][r], the version in the statement (used for the printed walk-through)."""
    m, n = len(grid), len(grid[0])
    dp = [[[0] * k for _ in range(n)] for _ in range(m)]
    dp[0][0][grid[0][0] % k] = 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            v = grid[i][j] % k
            for r in range(k):
                tot = (dp[i - 1][j][r] if i else 0) + (dp[i][j - 1][r] if j else 0)
                if tot:
                    dp[i][j][(r + v) % k] = (dp[i][j][(r + v) % k] + tot) % mod if mod else dp[i][j][(r + v) % k] + tot
    return dp

def brute(grid, k):
    m, n = len(grid), len(grid[0]); cnt = 0
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        i = j = 0; tot = grid[0][0]
        for c in s:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]
        cnt += tot % k == 0
    return cnt % MOD

# examples
for grid, k, exp in [([[5, 2, 4], [3, 0, 5], [0, 7, 2]], 3, 2), ([[0, 0]], 5, 1),
                     ([[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]], 1, 10), ([[1, 1], [1, 1]], 2, 0)]:
    a, b, c = count_paths(grid, k), brute(grid, k), count_paths_full(grid, k)[-1][-1][0]
    assert a == b == c == exp, (grid, k, a, b, c)
    print('example', grid, 'k =', k, '->', a)

# hand table for example 1
grid, k = [[5, 2, 4], [3, 0, 5], [0, 7, 2]], 3
dp = count_paths_full(grid, k)
print('dp[i][j] = [paths with remainder 0, 1, 2] for grid', grid, 'k =', k)
for i in range(3):
    print('  ', [dp[i][j] for j in range(3)])
print('answer = dp[2][2][0] =', dp[2][2][0])

# seeded cross-check, m, n <= 5
cases = nz = 0
for _ in range(500):
    m, n = random.randint(1, 5), random.randint(1, 5)
    k = random.randint(1, 6)
    grid = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
    exp = brute(grid, k)
    assert count_paths(grid, k) == count_paths_full(grid, k)[-1][-1][0] == exp, (grid, k)
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a non-zero count', nz)

# the modulus: counts beyond 10^9+7 occur, and reducing after each addition equals reducing at the end (exact big-int run)
g = [[random.randint(0, 100) for _ in range(40)] for _ in range(40)]
exact = count_paths(g, 7, mod=None)
print('40 x 40, k = 7: exact count has', len(str(exact)), 'digits; mod result', count_paths(g, 7), '== exact % MOD:', count_paths(g, 7) == exact % MOD)
assert count_paths(g, 7) == exact % MOD and exact > MOD
ones = [[0] * 70 for _ in range(70)]
assert count_paths(ones, 1, mod=None) == comb(138, 69) and count_paths(ones, 1) == comb(138, 69) % MOD
print('70 x 70 all zeros, k = 1: all C(138, 69) paths:', comb(138, 69) % MOD, '(exact value has', len(str(comb(138, 69))), 'digits)')

# why remainder and not the full sum: the number of distinct sums is far larger than k
print('largest possible path sum at 70 x 70, cells <= 100:', 100 * (70 + 70 - 1), '-> up to', 100 * 139 + 1, 'sum values per cell versus k <= 50 remainders')

# edge cases and the maximum size
assert count_paths([[5]], 5) == 1 and count_paths([[5]], 3) == 0 and count_paths([[0]], 1) == 1
assert count_paths([[3, 4]], 7) == 1 and count_paths([[3, 4]], 5) == 0
big = [[random.randint(0, 100) for _ in range(70)] for _ in range(70)]
t0 = time.perf_counter(); r = count_paths(big, 50); t1 = time.perf_counter()
assert r == count_paths_full(big, 50)[-1][-1][0]
print('70 x 70, k = 50:', r, '(sandbox timing %.2f s)' % (t1 - t0))
print('recursion limit', sys.getrecursionlimit(), '| the DP is iterative; a memoised f(i, j, r) would nest m + n - 1 = 139 frames, also fine at this size')
print('edge asserts passed')
