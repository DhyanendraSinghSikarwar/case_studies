import random
from math import ceil

def brute(piles, h):
    k = 1
    while sum(ceil(p / k) for p in piles) > h:
        k += 1
    return k

def min_speed(piles, h):
    lo, hi = 1, max(piles)             # at k = max, hours = len(piles) <= h, so hi is feasible
    while lo < hi:
        mid = (lo + hi) // 2
        if sum((p + mid - 1) // mid for p in piles) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo

random.seed(7)
for _ in range(3000):
    n = random.randint(1, 6)
    piles = [random.randint(1, 30) for _ in range(n)]
    h = random.randint(n, 40)
    assert min_speed(piles, h) == brute(piles, h)
print("cross-check ok")
for p, h in [([3,6,7,11],8),([30,11,23,4,20],5),([30,11,23,4,20],6),([5],5)]:
    print(p, h, "->", min_speed(p, h))
big = [10**9] * 10**4
assert min_speed(big, 10**4) == 10**9
assert min_speed(big, 10**9) == 10**4 * 10**9 // 10**9   # 10^4 piles, 10^9 hours -> k=10^4
print("big:", min_speed(big, 10**9))
