import random, sys
from functools import cache

random.seed(25)
NEG = float('-inf')

def cooldown(prices):
    """Bottom-up, O(1) space. States at the END of each day:
    hold = best profit while holding a share; sold = best profit if I sold today; free = best profit, no share, free to buy."""
    hold, sold, free = NEG, NEG, 0
    for p in prices:
        hold, sold, free = max(hold, free - p), hold + p, max(free, sold)
    return max(sold, free)

def cooldown_table(prices):
    """Same thing with full arrays, to print the walk-through."""
    hold, sold, free = [NEG], [NEG], [0]
    for p in prices:
        hold.append(max(hold[-1], free[-1] - p)); sold.append(hold[-2] + p); free.append(max(free[-1], sold[-2]))
    return hold, sold, free

def no_cooldown(prices):
    """Drop the cooldown: sold and free merge into one 'not holding' state."""
    hold, cash = NEG, 0
    for p in prices:
        hold, cash = max(hold, cash - p), max(cash, hold + p)
    return cash

def rises(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))

def memo(prices):
    n = len(prices)
    @cache
    def f(i, holding):
        if i >= n: return 0
        best = f(i + 1, holding)                                 # do nothing today
        if holding: best = max(best, prices[i] + f(i + 2, False))   # sell today; day i+1 is the cooldown day
        else: best = max(best, -prices[i] + f(i + 1, True))        # buy today
        return best
    return f(0, False)

def brute(prices):
    """Plain recursion over (day, holding), no cache."""
    n = len(prices)
    def f(i, holding):
        if i >= n: return 0
        best = f(i + 1, holding)
        if holding: best = max(best, prices[i] + f(i + 2, False))
        else: best = max(best, -prices[i] + f(i + 1, True))
        return best
    return f(0, False)

for pr, exp in [([1, 2, 3, 0, 2], 3), ([1], 0), ([], 0), ([6, 1, 3, 2, 4, 7], 6)]:
    assert cooldown(pr) == brute(pr) == memo(pr) == exp, pr
    print('example', pr, '->', exp)

h, s, f = cooldown_table([1, 2, 3, 0, 2])
print('day  price  hold  sold  free')
print('  0      -    ', h[0], s[0], f[0])
for i, p in enumerate([1, 2, 3, 0, 2], 1):
    print(f'  {i}    {p:3d}   {h[i]:4}  {s[i]:4}  {f[i]:4}')
print('answer = max(sold, free) at the end =', max(s[-1], f[-1]))

n_cases = 0; cd_lt = 0
for _ in range(800):
    n = random.randint(0, 10); pr = [random.randint(0, 9) for _ in range(n)]
    want = brute(pr)
    assert cooldown(pr) == want == memo(pr), pr
    nc = no_cooldown(pr)
    assert nc == rises(pr) and nc >= want       # without the cooldown it is the sum of positive daily rises
    n_cases += 1; cd_lt += nc > want
print('cross-check cases', n_cases, '| no-cooldown value strictly larger on', cd_lt, '| no-cooldown == sum of positive rises on all')

# max size: bottom-up fine, memo recursion not
big = [random.randint(0, 1000) for _ in range(5000)]
print('n = 5000 profit', cooldown(big))
print('limit =', sys.getrecursionlimit())
try:
    memo(big); print('memo n=5000 ok')
except RecursionError:
    print('memo n=5000: RecursionError')
assert cooldown([5, 4, 3]) == 0 and cooldown([1, 5]) == 4 and cooldown([2, 2, 2]) == 0
print('edge asserts passed')
