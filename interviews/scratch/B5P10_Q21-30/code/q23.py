import random, sys
from functools import cache

random.seed(23)
INF = float('inf')

def min_table(coins, amount):
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp

def coin_list(coins, amount):
    """Bottom-up table, then rebuild: at each amount take the SMALLEST coin c with dp[a-c] == dp[a]-1."""
    dp = min_table(coins, amount)
    if dp[amount] == INF:
        return None
    out, a = [], amount
    cs = sorted(coins)
    while a:
        for c in cs:
            if c <= a and dp[a - c] == dp[a] - 1:
                out.append(c); a -= c
                break
    return out                      # already non-decreasing (argued in the text, asserted below)

def naive_parent(coins, amount, order='input'):
    """Plain parent pointer: remember the first coin (in the given loop order) that achieves dp[a], rebuild, sort."""
    dp = [0] + [INF] * amount
    par = [0] * (amount + 1)
    cs = {'input': list(coins), 'asc': sorted(coins), 'desc': sorted(coins, reverse=True)}[order]
    for a in range(1, amount + 1):
        for c in cs:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1; par[a] = c
    if dp[amount] == INF:
        return None
    out, a = [], amount
    while a:
        out.append(par[a]); a -= par[a]
    return sorted(out)

def memo_len(coins, amount):
    @cache
    def f(a):
        if a == 0: return 0
        best = INF
        for c in coins:
            if c <= a:
                best = min(best, f(a - c) + 1)
        return best
    return f(amount)

def brute(coins, amount):
    """Enumerate every multiset with sum amount (k copies of each coin), pick min size then lexicographically smallest."""
    cs = sorted(coins); found = []
    def rec(i, rem, cur):
        if rem == 0:
            found.append(list(cur)); return
        if i == len(cs): return
        k = 0
        while k * cs[i] <= rem:
            rec(i + 1, rem - k * cs[i], cur + [cs[i]] * k); k += 1
    rec(0, amount, [])
    if not found: return None
    m = min(map(len, found))
    return min(f for f in found if len(f) == m)

for coins, amt, exp in [([1, 2, 5], 11, [1, 5, 5]), ([2], 3, None), ([3, 5], 0, []), ([1, 3, 4], 6, [3, 3]), ([2, 3], 7, [2, 2, 3])]:
    got = coin_list(coins, amt); assert got == brute(coins, amt) == exp, (coins, amt, got)
    print('example', coins, amt, '->', got)

# hand table for the first example
dp = min_table([1, 2, 5], 11)
print('dp[0..11] =', dp)
a, steps = 11, []
while a:
    for c in [1, 2, 5]:
        if c <= a and dp[a - c] == dp[a] - 1:
            steps.append((a, c)); a -= c; break
print('rebuild (amount, coin taken):', steps)

# seeded cross-check, amount <= 15
n = mism_in = mism_asc = mism_desc = none_cnt = 0
ex = None
for _ in range(2000):
    coins = random.sample(range(1, 10), random.randint(2, 4)); amt = random.randint(0, 15)
    got = coin_list(coins, amt); want = brute(coins, amt)
    assert got == want, (coins, amt, got, want)
    if got is not None: assert got == sorted(got)
    n += 1; none_cnt += got is None
    for key in ('input', 'asc', 'desc'):
        bad = naive_parent(coins, amt, key) != want
        if key == 'input':
            mism_in += bad
            if bad and ex is None: ex = (coins, amt)
        elif key == 'asc': mism_asc += bad
        else: mism_desc += bad
print('cross-check cases', n, '(of which unreachable:', none_cnt, ')')
print('naive parent pointer, coins looped in INPUT order, differs from the tie rule on', mism_in)
print('naive parent pointer, coins looped ascending, differs on', mism_asc)
print('naive parent pointer, coins looped descending, differs on', mism_desc)
print('example of a miss (input order):', ex, 'naive', naive_parent(ex[0], ex[1]), 'rule', brute(*ex))

# memo version agrees on small, recursion limit at large
for _ in range(100):
    coins = random.sample(range(1, 20), random.randint(1, 5)); amt = random.randint(0, 60)
    d = min_table(coins, amt)[amt]
    assert memo_len(coins, amt) == d
big = coin_list([1, 5, 10, 25, 100], 1000)
print('amount 1000, coins [1,5,10,25,100] ->', big, 'size', len(big))
assert sum(big) == 1000
print('limit =', sys.getrecursionlimit())
try:
    memo_len([1, 7], 1000); print('memo amount 1000 ok')
except RecursionError:
    print('memo amount 1000 with coin 1: RecursionError')
assert coin_list([1], 1000) == [1] * 1000
assert coin_list([7, 3], 2) is None and coin_list([4, 6], 0) == []
print('edge asserts passed')
