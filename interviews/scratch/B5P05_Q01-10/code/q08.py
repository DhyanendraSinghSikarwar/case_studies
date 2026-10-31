import random

def days_needed(w, c):
    d, cur = 1, 0
    for x in w:
        if cur + x > c:
            d += 1; cur = 0
        cur += x
    return d

def brute(w, days):
    c = max(w)
    while days_needed(w, c) > days:
        c += 1
    return c

def ship(w, days):
    lo, hi = max(w), sum(w)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(w, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo

# exhaustive partition check: true optimum over all ways to cut into <= days contiguous groups
from itertools import combinations
def exact(w, days):
    n = len(w); best = None
    for k in range(0, days):
        for cuts in combinations(range(1, n), k):
            b = (0,) + cuts + (n,)
            m = max(sum(w[b[i]:b[i+1]]) for i in range(len(b) - 1))
            best = m if best is None else min(best, m)
    return best

random.seed(8)
for _ in range(2000):
    n = random.randint(1, 8)
    w = [random.randint(1, 12) for _ in range(n)]
    d = random.randint(1, n)
    assert ship(w, d) == brute(w, d) == exact(w, d)
print("cross-check ok (vs linear scan and exhaustive partitions)")
for w, d in [(list(range(1, 11)), 5), ([3,2,2,4,1,4], 3), ([1,2,3,1,1], 4), ([7], 1)]:
    print(w, d, "->", ship(w, d))
w = [500] * 5 * 10**4
assert ship(w, 1) == 500 * 5 * 10**4 and ship(w, len(w)) == 500
