import random
from collections import deque

def brute(nums, k):
    best = -1
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s >= k:
                if best == -1 or j - i + 1 < best: best = j - i + 1
                break
    return best

def shortest(nums, k):
    n = len(nums)
    P = [0] * (n + 1)
    for i, v in enumerate(nums): P[i + 1] = P[i] + v
    dq = deque()                     # indices with strictly increasing prefix values
    best = n + 1
    for j in range(n + 1):
        while dq and P[j] - P[dq[0]] >= k:      # front start is good: record it, and it can never help later (any later end is longer)
            best = min(best, j - dq.popleft())
        while dq and P[dq[-1]] >= P[j]:         # back start is dominated: later AND not larger prefix means longer-never, sum-never-worse
            dq.pop()
        dq.append(j)
    return best if best <= n else -1

for nums, k, exp in [([1], 1, 1), ([1, 2], 4, -1), ([2, -1, 2], 3, 3)]:
    assert shortest(nums, k) == brute(nums, k) == exp
    print(nums, "k =", k, "->", shortest(nums, k))
assert shortest([], 1) == -1 and shortest([-5], 1) == -1 and shortest([84, -37, 32, 40, 95], 167) == 3
assert shortest([5, -10, 7], 7) == 1 and shortest([1, 1, 1], 3) == 3 and shortest([-1, -1], 1) == -1
random.seed(43)
for _ in range(2500):
    nums = [random.randint(-4, 6) for _ in range(random.randint(0, 10))]
    k = random.randint(1, 10)
    assert shortest(nums, k) == brute(nums, k), (nums, k)
print("2500 seeded cases match brute force; edges pass")
