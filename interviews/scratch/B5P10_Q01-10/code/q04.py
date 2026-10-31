import itertools
import random

random.seed(104)
NEG = float('-inf')

def stock_two_state(prices):
    """hold = best cash while holding a share, free = best cash while not holding (never bought, or sold).
    hold' = max(hold, -p)        (keep holding, or buy today: only ONE buy, so cash before it is 0)
    free' = max(free, hold + p)  (stay out, or sell today)"""
    hold, free = NEG, 0
    for p in prices:
        hold, free = max(hold, -p), max(free, hold + p)    # tuple assignment uses the OLD hold on the right
    return free

def stock_min_so_far(prices):
    best, low = 0, float('inf')
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best

def brute(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best

def table(prices):
    hold, free, rows = NEG, 0, []
    for p in prices:
        hold, free = max(hold, -p), max(free, hold + p)
        rows.append((p, hold, free))
    return rows

for pr, want in [([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0), ([], 0), ([3], 0)]:
    assert stock_two_state(pr) == stock_min_so_far(pr) == brute(pr) == want
print('4 prompt examples ok')

print('day price hold free   (prices [7, 1, 5, 3, 6, 4])')
for d, (p, h, f) in enumerate(table([7, 1, 5, 3, 6, 4])):
    print(f'{d:>3} {p:>5} {h:>4} {f:>4}')

for _ in range(1000):
    n = random.randint(0, 12)
    pr = [random.randint(0, 20) for _ in range(n)]
    assert stock_two_state(pr) == brute(pr) == stock_min_so_far(pr), pr
print('1000 seeded random lists (len 0..12, values 0..20): two-state == all-pairs == min-so-far')

cnt = 0
for n in range(0, 7):
    for pr in itertools.product(range(5), repeat=n):
        pr = list(pr)
        assert stock_two_state(pr) == brute(pr); cnt += 1
print('exhaustive len 0..6 values 0..4:', cnt, 'lists ok')

# the link: hold_i == -(min price so far), and free_i == best profit so far
for _ in range(300):
    pr = [random.randint(0, 20) for _ in range(random.randint(1, 12))]
    rows = table(pr)
    for i, (p, h, f) in enumerate(rows):
        assert h == -min(pr[:i + 1])
        assert f == brute(pr[:i + 1])
print('hold_i == -(min price so far) and free_i == best profit on the prefix: verified on 300 seeded lists')

big = [random.randint(0, 10**4) for _ in range(10**5)]
assert stock_two_state(big) == stock_min_so_far(big)
print('n = 10^5 ->', stock_two_state(big))
assert stock_two_state([]) == 0 and stock_two_state([5, 5, 5]) == 0 and stock_two_state([1, 2, 3, 4, 5]) == 4
print('edge asserts ok: empty, flat, strictly rising')
