import random
import sys
from functools import cache

random.seed(102)

def min_cost(cost):
    """dp[i] = cheapest price to stand on position i (0..n). dp[0] = dp[1] = 0 (free start).
    dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]). Two variables."""
    a, b = 0, 0                                  # dp[i-2], dp[i-1] for i = 2
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b                                     # dp[n]  (n >= 2 guaranteed)

def min_cost_table(cost):
    n = len(cost)
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
    return dp

def min_cost_forward_memo(cost):
    """Top-down, other direction: f(i) = cheapest cost to finish from step i (about to pay cost[i])."""
    n = len(cost)
    @cache
    def f(i):
        if i >= n:
            return 0
        return cost[i] + min(f(i + 1), f(i + 2))
    return min(f(0), f(1))

def min_cost_oracle(cost):
    """Same as above, no memo, n <= 15."""
    n = len(cost)
    def f(i):
        if i >= n:
            return 0
        return cost[i] + min(f(i + 1), f(i + 2))
    return min(f(0), f(1))

for c, want in [([10, 15, 20], 15), ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], 6), ([0, 0], 0), ([5, 1], 1)]:
    assert min_cost(c) == min_cost_oracle(c) == min_cost_forward_memo(c) == want
print('4 prompt examples ok')

c = [10, 15, 20]
print('walk-through cost =', c, ' positions 0..3')
print('dp =', min_cost_table(c))

for _ in range(500):
    n = random.randint(2, 15)
    c = [random.randint(0, 999) for _ in range(n)]
    assert min_cost(c) == min_cost_oracle(c) == min_cost_table(c)[-1], c
print('500 seeded random lists (len 2..15, values 0..999): bottom-up == forward recursion')
# exhaustive over small lists
import itertools
cnt = 0
for n in range(2, 7):
    for c in itertools.product(range(4), repeat=n):
        assert min_cost(list(c)) == min_cost_oracle(list(c)); cnt += 1
print('exhaustive, len 2..6 values 0..3:', cnt, 'lists ok')

# the claim "start on step 0 or 1 for free": dp[0]=dp[1]=0, answer dp[n]; equals min over the two forward starts
big = [random.randint(0, 999) for _ in range(10**5)]
print('n = 10^5 bottom-up ->', min_cost(big))
try:
    min_cost_forward_memo(big)
    print('forward memo at 10^5: ok')
except RecursionError:
    print('forward memo at 10^5: RecursionError (default limit', sys.getrecursionlimit(), ')')
