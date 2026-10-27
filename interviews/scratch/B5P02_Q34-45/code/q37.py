import random
from functools import lru_cache

def brute(people, limit):
    n = len(people)
    @lru_cache(maxsize=None)
    def go(mask):
        if mask == (1 << n) - 1: return 0
        i = next(b for b in range(n) if not mask >> b & 1)
        best = 1 + go(mask | 1 << i)                      # i rides alone
        for j in range(i + 1, n):
            if not mask >> j & 1 and people[i] + people[j] <= limit:
                best = min(best, 1 + go(mask | 1 << i | 1 << j))
        return best
    return go(0)

def boats(people, limit):
    p = sorted(people)
    l, r, cnt = 0, len(p) - 1, 0
    while l <= r:
        if p[l] + p[r] <= limit:
            l += 1               # lightest rides with heaviest
        r -= 1                   # heaviest always leaves in this boat
        cnt += 1
    return cnt

for ppl, lim, exp in [([3, 2, 2, 1], 3, 3), ([3, 5, 3, 4], 5, 4), ([1, 2], 3, 1)]:
    assert boats(ppl, lim) == brute(tuple(ppl), lim) == exp
    print(ppl, "limit", lim, "->", boats(ppl, lim))
assert boats([], 5) == 0 and boats([5], 5) == 1 and boats([2, 2, 2, 2], 4) == 2 and boats([5, 5, 5], 5) == 3
random.seed(37)
for _ in range(600):
    lim = random.randint(1, 10)
    ppl = [random.randint(1, lim) for _ in range(random.randint(0, 9))]
    assert boats(ppl, lim) == brute(tuple(ppl), lim), (ppl, lim)
print("600 seeded cases match the bitmask brute force; edges pass")
