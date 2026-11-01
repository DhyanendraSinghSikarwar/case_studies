import random
from bisect import bisect_left, bisect_right

def brute(nums, t):
    idx = [i for i, v in enumerate(nums) if v == t]
    return [idx[0], idx[-1]] if idx else [-1, -1]

def lower_bound(nums, x):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x: lo = mid + 1
        else: hi = mid
    return lo

def search_range(nums, t):
    first = lower_bound(nums, t)
    if first == len(nums) or nums[first] != t:
        return [-1, -1]
    last = lower_bound(nums, t + 1) - 1    # integers: first index >= t+1 minus one
    return [first, last]

random.seed(4)
for _ in range(3000):
    nums = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 14)))
    for t in range(-8, 9):
        r = search_range(nums, t)
        assert r == brute(nums, t)
        if r != [-1, -1]:
            assert r == [bisect_left(nums, t), bisect_right(nums, t) - 1]
print("cross-check ok")
for a, t in [([5,7,7,8,8,10],8),([5,7,7,8,8,10],6),([],0),([1],1),([2,2,2,2],2)]:
    print(a, t, "->", search_range(a, t))
assert search_range([2]*10**5, 2) == [0, 10**5 - 1]
