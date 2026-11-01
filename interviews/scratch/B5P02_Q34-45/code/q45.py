import random
from collections import deque

def brute(nums, limit):
    best = 0
    for i in range(len(nums)):
        lo = hi = nums[i]
        for j in range(i, len(nums)):
            lo, hi = min(lo, nums[j]), max(hi, nums[j])
            if hi - lo <= limit: best = max(best, j - i + 1)
            else: break
    return best

def longest(nums, limit):
    maxd, mind = deque(), deque()      # store (index); maxd values decreasing, mind values increasing
    l = best = 0
    for r, v in enumerate(nums):
        while maxd and nums[maxd[-1]] <= v: maxd.pop()
        maxd.append(r)
        while mind and nums[mind[-1]] >= v: mind.pop()
        mind.append(r)
        while nums[maxd[0]] - nums[mind[0]] > limit:
            l += 1
            if maxd[0] < l: maxd.popleft()      # drop indices that left the window
            if mind[0] < l: mind.popleft()
        best = max(best, r - l + 1)
    return best

for a, lim, exp in [([8, 2, 4, 7], 4, 2), ([10, 1, 2, 4, 7, 2], 5, 4), ([4, 2, 2, 2, 4, 4, 2, 2], 0, 3)]:
    assert longest(a, lim) == brute(a, lim) == exp
    print(a, "limit", lim, "->", longest(a, lim))
assert longest([], 3) == 0 and longest([5], 0) == 1 and longest([1, 5, 9], 0) == 1 and longest([1, 5, 9], 100) == 3
assert longest([7, 7, 7], 0) == 3 and longest([-5, -1, -3], 4) == 3
random.seed(45)
for _ in range(3000):
    a = [random.randint(-6, 6) for _ in range(random.randint(0, 12))]
    lim = random.randint(0, 8)
    assert longest(a, lim) == brute(a, lim), (a, lim)
print("3000 seeded cases match brute force; edges pass")
