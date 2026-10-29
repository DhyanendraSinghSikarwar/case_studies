import random
from functools import lru_cache

random.seed(16)
INF = float('inf')

def perfect_squares(n):
    """Optimal: dp[i] = fewest squares summing to i. Bottom-up, O(n sqrt n) time, O(n) space."""
    dp = [0] + [INF] * n              # dp[0] = 0: the empty sum
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            if dp[i - j * j] + 1 < dp[i]:
                dp[i] = dp[i - j * j] + 1
            j += 1
    return dp[n]

def perfect_squares_memo(n):
    """Top-down: tries j = 1 first, so the first descent goes n deep."""
    @lru_cache(maxsize=None)
    def f(m):
        if m == 0:
            return 0
        return 1 + min(f(m - j * j) for j in range(1, int(m ** 0.5) + 1))
    return f(n)

def brute(n):
    """Oracle: plain recursion, no cache."""
    if n == 0:
        return 0
    return 1 + min(brute(n - j * j) for j in range(1, int(n ** 0.5) + 1))

for n, want in [(12, 3), (13, 2), (1, 1), (7, 4), (9999, 4)]:
    assert perfect_squares(n) == want, n
    if n < 900:
        assert perfect_squares_memo(n) == want
    if n <= 25:
        assert brute(n) == want
print('5 prompt examples ok')

# walk-through, n = 12
dp = [0] + [INF] * 12
print('i   dp[i]  best choice (j*j subtracted)')
print('0   0      base')
for i in range(1, 13):
    cands = [(dp[i - j * j] + 1, j * j) for j in range(1, int(i ** 0.5) + 1)]
    dp[i] = min(c[0] for c in cands)
    print('%-3d %-6d %s' % (i, dp[i], ', '.join('dp[%d]+1=%d' % (i - s, v) for v, s in cands)))
print('dp[12] = 3 : 4 + 4 + 4')

# step count of the double loop at n = 10^4 versus n^2/2 for a plain 1..n coin loop
steps = sum(int(i ** 0.5) for i in range(1, 10**4 + 1))
print('inner-loop steps at n=10^4:', steps, '(about n * sqrt(n) * 2/3 = 666667)')

# seeded cross-check against the plain recursion
for n in range(1, 26):
    assert perfect_squares(n) == brute(n) == perfect_squares_memo(n), n
for _ in range(300):
    n = random.randint(1, 25)
    assert perfect_squares(n) == brute(n)
print('all n in 1..25 and 300 random draws agree with the plain recursion')

# claims: answer never exceeds 4 (Lagrange); 4 exactly when n = 4^a (8b + 7) (Legendre)
def legendre4(n):
    while n % 4 == 0:
        n //= 4
    return n % 8 == 7
dp_all = [0] + [INF] * 10**4
for i in range(1, 10**4 + 1):
    j = 1
    while j * j <= i:
        dp_all[i] = min(dp_all[i], dp_all[i - j * j] + 1)
        j += 1
assert max(dp_all[1:]) == 4
assert all((dp_all[i] == 4) == legendre4(i) for i in range(1, 10**4 + 1))
print('for every n in 1..10^4 the answer is <= 4, and equals 4 exactly when n = 4^a * (8b + 7)')

# recursion limit
try:
    perfect_squares_memo(10**4)
    print('memo at n=10^4: no error (unexpected)')
except RecursionError:
    print('memo at n=10^4: RecursionError under the default limit')
print('bottom-up n=10^4 ->', perfect_squares(10**4))
assert perfect_squares(1) == 1 and perfect_squares(4) == 1 and perfect_squares(2) == 2
print('edge cases ok')
