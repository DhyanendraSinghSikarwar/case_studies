import itertools
import random
import sys
from functools import cache

random.seed(106)
INF = float('inf')

def coin_min(coins, amount):
    """dp[a] = fewest coins to make exactly a. dp[0] = 0, dp[a] = 1 + min(dp[a - c]) over coins c <= a. INF = impossible."""
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1

def dp_table(coins, amount):
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp

def coin_memo(coins, amount):
    @cache
    def f(a):
        if a == 0:
            return 0
        best = INF
        for c in coins:
            if c <= a:
                best = min(best, f(a - c) + 1)
        return best
    r = f(amount)
    return r if r != INF else -1

def brute(coins, amount):
    """Plain recursion over the amount, no memo (amount <= 12)."""
    def f(a):
        if a == 0:
            return 0
        best = INF
        for c in coins:
            if c <= a:
                best = min(best, f(a - c) + 1)
        return best
    r = f(amount)
    return r if r != INF else -1

def greedy(coins, amount):
    """Largest coin first. Shown wrong."""
    n = 0
    for c in sorted(coins, reverse=True):
        n += amount // c
        amount %= c
    return n if amount == 0 else -1

for cs, am, want in [([1, 2, 5], 11, 3), ([2], 3, -1), ([7], 0, 0), ([1, 3, 4], 6, 2)]:
    assert coin_min(cs, am) == brute(cs, am) == coin_memo(cs, am) == want
print('4 prompt examples ok')

print('coins [1, 2, 5], dp[0..11] =', dp_table([1, 2, 5], 11))
print('coins [1, 3, 4], dp[0..6]  =', dp_table([1, 3, 4], 6))
print('greedy on coins [1, 3, 4], amount 6 ->', greedy([1, 3, 4], 6), '(4+1+1) but optimum is', coin_min([1, 3, 4], 6), '(3+3)')
print('greedy on coins [2, 5], amount 6 ->', greedy([2, 5], 6), 'but optimum is', coin_min([2, 5], 6), '(2+2+2)')

for _ in range(1000):
    k = random.randint(1, 5)
    cs = random.sample(range(1, 13), k)
    am = random.randint(0, 12)
    assert coin_min(cs, am) == brute(cs, am), (cs, am)
print('1000 seeded random (<= 5 coins in 1..12, amount 0..12): DP == plain recursion')

# exhaustive: every non-empty coin subset of 1..7, every amount 0..14; count where greedy fails
tot = bad_val = bad_imp = 0
for mask in range(1, 1 << 7):
    cs = [i + 1 for i in range(7) if mask >> i & 1]
    for am in range(15):
        d = coin_min(cs, am); g = greedy(cs, am); tot += 1
        assert d == brute(cs, am)
        if g != d:
            if g == -1: bad_imp += 1
            else: bad_val += 1
print(f'exhaustive coin sets in 1..7 x amounts 0..14 = {tot} cases: DP == recursion; greedy wrong on {bad_val + bad_imp} ({bad_imp} of them says -1 when a solution exists)')

assert greedy([1, 2, 5], 11) == 3
for cs in ([1, 5, 10, 25],):                              # canonical systems: greedy happens to work
    assert all(greedy(cs, a) == coin_min(cs, a) for a in range(200))

# large sizes
cs = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 5000, 7]
print('amount 10^4, 12 coins, bottom-up ->', coin_min(cs, 10**4))
print('coins [2], amount 9999 ->', coin_min([2], 9999), '; coins [2], amount 10^4 ->', coin_min([2], 10**4))
try:
    coin_memo([1, 2, 5], 10**4)
    print('memoised amount 10^4: ok')
except RecursionError:
    print('memoised amount 10^4: RecursionError (default limit', sys.getrecursionlimit(), ')')
print('memoised amount 500 ->', coin_memo([1, 2, 5], 500), '== bottom-up', coin_min([1, 2, 5], 500))
