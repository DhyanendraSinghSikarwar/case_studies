import itertools
import random
import sys
from functools import cache

random.seed(110)

def ways_combinations(coins, amount):
    """dp[a] = number of multisets summing to a. Coin loop OUTER: each coin is introduced once, so a multiset
    is built in one fixed coin order (all 1s, then 2s, ...) and counted once."""
    dp = [1] + [0] * amount
    for c in coins:                       # outer: coins
        for a in range(c, amount + 1):    # inner: amounts upward (a coin may repeat)
            dp[a] += dp[a - c]
    return dp[amount]

def ways_ordered(coins, amount):
    """Amount OUTER, coin inner: counts ORDERED sequences (compositions). Wrong for this question."""
    dp = [1] + [0] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] += dp[a - c]
    return dp[amount]

def table_after_each_coin(coins, amount):
    dp = [1] + [0] * amount; rows = []
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
        rows.append((c, dp[:]))
    return rows

def by_index(coins, amount):
    """Oracle: ways(i, rem) = take another copy of coin i, or move to coin i+1. No memo."""
    def f(i, rem):
        if rem == 0:
            return 1
        if i == len(coins) or rem < 0:
            return 0
        return f(i, rem - coins[i]) + f(i + 1, rem)
    return f(0, amount)

def by_index_memo(coins, amount):
    @cache
    def f(i, rem):
        if rem == 0:
            return 1
        if i == len(coins) or rem < 0:
            return 0
        return f(i, rem - coins[i]) + f(i + 1, rem)
    return f(0, amount)

def enumerate_multisets(coins, amount):
    """Independent oracle: enumerate counts of each coin with itertools."""
    ranges = [range(amount // c + 1) for c in coins]
    return sum(1 for ks in itertools.product(*ranges) if sum(k * c for k, c in zip(ks, coins)) == amount)

for cs, am, want in [([1, 2, 5], 5, 4), ([2], 3, 0), ([10], 0, 1), ([1, 2, 3], 4, 4)]:
    assert ways_combinations(cs, am) == by_index(cs, am) == enumerate_multisets(cs, am) == want
print('4 prompt examples ok')

print('coins [1, 2, 5], amount 5: dp[0..5] after each coin')
print('  start       ', [1, 0, 0, 0, 0, 0])
for c, row in table_after_each_coin([1, 2, 5], 5):
    print(f'  after coin {c}:', row)
print('  ordered (amount-outer) answer for the same input:', ways_ordered([1, 2, 5], 5), '(compositions, not multisets)')

for _ in range(1000):
    k = random.randint(1, 4)
    cs = random.sample(range(1, 9), k)
    am = random.randint(0, 14)
    a = ways_combinations(cs, am)
    assert a == by_index(cs, am) == by_index_memo(cs, am) == enumerate_multisets(cs, am), (cs, am)
    # coin order must not matter for the count
    sh = cs[:]; random.shuffle(sh)
    assert ways_combinations(sh, am) == a
print('1000 seeded random (<= 4 coins in 1..8, amount 0..14): DP == index recursion == itertools enumeration; coin order irrelevant')

# the loop-order claim, measured
diff = same = 0
for _ in range(600):
    cs = random.sample(range(1, 9), random.randint(1, 4)); am = random.randint(0, 14)
    if ways_combinations(cs, am) != ways_ordered(cs, am): diff += 1
    else: same += 1
print(f'swapped loop order (amount outer) differs from the combination count on {diff} of 600 seeded cases')
# the swapped version counts ordered sequences: verify against a direct composition count
def compositions(cs, am):
    @cache
    def g(r):
        return 1 if r == 0 else sum(g(r - c) for c in cs if c <= r)
    return g(am)
for _ in range(300):
    cs = random.sample(range(1, 9), random.randint(1, 4)); am = random.randint(0, 14)
    assert ways_ordered(cs, am) == compositions(cs, am)
print('amount-outer version == number of ORDERED sequences (checked on 300 seeded cases)')

print('coins [1, 2, 5], amount 11: combinations =', ways_combinations([1, 2, 5], 11), '(Q6 asks the min coins, 3, for the same input)')

# edge and large cases
assert ways_combinations([10], 0) == 1 and ways_combinations([7], 5) == 0 and ways_combinations([1], 5000) == 1
big_coins = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
big = ways_combinations(big_coins, 5000)
print('12 coins, amount 5000 ->', big, '(an exact big integer, no modulus)')
try:
    by_index_memo([1, 2, 5], 5000)
    print('memoised by-index amount 5000: ok')
except RecursionError:
    print('memoised by-index amount 5000: RecursionError (default limit', sys.getrecursionlimit(), ')')
print('memoised by-index amount 300 ->', by_index_memo([1, 2, 5], 300), '== bottom-up', ways_combinations([1, 2, 5], 300))
