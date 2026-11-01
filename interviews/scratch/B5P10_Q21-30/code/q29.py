import random, sys
from functools import cache

random.seed(29)
NEG = float('-inf')

def table_k(k, prices):
    """O(n*k) time, O(k) space. buy[j] = best profit holding a share during the j-th transaction,
    sell[j] = best profit after completing j transactions."""
    buy = [NEG] * (k + 1); sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]

def unlimited(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))

def solve(k, prices):
    n = len(prices)
    if n < 2 or k == 0: return 0
    if k >= n // 2: return unlimited(prices)     # at most n // 2 transactions can ever be useful
    return table_k(k, prices)

def memo(k, prices):
    n = len(prices)
    @cache
    def f(i, t, hold):
        if i == n: return 0
        best = f(i + 1, t, hold)
        if hold: best = max(best, prices[i] + f(i + 1, t, 0))
        elif t > 0: best = max(best, -prices[i] + f(i + 1, t - 1, 1))
        return best
    return f(0, k, 0)

def brute(k, prices):
    n = len(prices)
    def f(i, t, hold):
        if i == n: return 0
        best = f(i + 1, t, hold)
        if hold: best = max(best, prices[i] + f(i + 1, t, 0))
        elif t > 0: best = max(best, -prices[i] + f(i + 1, t - 1, 1))
        return best
    return f(0, k, 0)

for k, pr, exp in [(2, [3, 2, 6, 5, 0, 3], 7), (1, [7, 6, 4, 3, 1], 0), (10**9, [1, 5, 2, 8, 3, 9], 16), (0, [1, 9], 0)]:
    assert solve(k, pr) == brute(k, pr) == exp, (k, pr)
    print('example k =', k, pr, '->', exp)

# walk-through for the first example
k, pr = 2, [3, 2, 6, 5, 0, 3]
buy = [NEG] * (k + 1); sell = [0] * (k + 1)
print('day price | buy1 sell1 buy2 sell2')
for d, p in enumerate(pr):
    for j in range(1, k + 1):
        buy[j] = max(buy[j], sell[j - 1] - p); sell[j] = max(sell[j], buy[j] + p)
    print(f' {d}   {p}   | {buy[1]:4} {sell[1]:4} {buy[2]:4} {sell[2]:4}')
print('answer sell[2] =', sell[2])

# the k >= n // 2 claim: full table vs unlimited, exhaustive over small price lists
cnt = 0; first_k_needed = {}
import itertools
for n in range(0, 8):
    for t in itertools.product(range(0, 4), repeat=n):
        pr = list(t); u = unlimited(pr)
        for kk in range(0, n + 3):
            full = table_k(kk, pr) if kk else 0
            if kk >= n // 2: assert full == u, (kk, pr)
            if kk < n // 2: assert full <= u
        cnt += 1
print('exhaustive price lists (len <= 7, values 0..3):', cnt, '- table(k) == unlimited for every k >= n // 2')
# is n // 2 tight? find a list where k = n // 2 - 1 is strictly worse
ex = None
for n in (4, 6):
    for t in itertools.product(range(0, 3), repeat=n):
        pr = list(t)
        if table_k(n // 2 - 1, pr) < unlimited(pr): ex = pr; break
    if ex: break
print('k = n // 2 - 1 is not enough on e.g.', ex, ':', table_k(len(ex) // 2 - 1, ex), '<', unlimited(ex))

# seeded cross-check against the recursion over (day, transactions left, holding)
n_cases = 0
for _ in range(600):
    n = random.randint(0, 8); pr = [random.randint(0, 9) for _ in range(n)]; kk = random.randint(0, 5)
    want = brute(kk, pr)
    assert solve(kk, pr) == want == memo(kk, pr) == (table_k(kk, pr) if kk else 0), (kk, pr)
    n_cases += 1
print('cross-check cases', n_cases, '(table, shortcut and memo all equal the recursion)')

big = [random.randint(0, 1000) for _ in range(1000)]
print('n = 1000, k = 10^9 ->', solve(10**9, big), '| k = 50 ->', solve(50, big))
print('limit =', sys.getrecursionlimit())
try:
    memo(3, big); print('memo n=1000 ok')
except RecursionError:
    print('memo n=1000: RecursionError')
assert solve(0, [1, 2]) == 0 and solve(5, []) == 0 and solve(5, [4]) == 0 and solve(1, [1, 2]) == 1
print('edge asserts passed')
