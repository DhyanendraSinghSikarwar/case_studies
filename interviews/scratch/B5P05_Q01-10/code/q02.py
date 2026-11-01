import random
from bisect import bisect_left

def brute(nums, target):
    for i, v in enumerate(nums):
        if v >= target:
            return i
    return len(nums)

def search_insert(nums, target):
    lo, hi = 0, len(nums)              # answer in [0, n]; invariant: nums[:lo] < target <= nums[hi:]
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid                   # mid might be the answer, keep it
    return lo

random.seed(2)
for _ in range(2000):
    nums = sorted(random.sample(range(-15, 15), random.randint(0, 10)))
    for t in range(-17, 17):
        r = search_insert(nums, t)
        assert r == brute(nums, t) == bisect_left(nums, t)
print("cross-check ok")
for a, t, e in [([1,3,5,6],5,2),([1,3,5,6],2,1),([1,3,5,6],7,4),([1,3,5,6],0,0),([],3,0)]:
    assert search_insert(a, t) == e
    print(a, t, "->", search_insert(a, t))
