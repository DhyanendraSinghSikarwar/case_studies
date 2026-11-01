import random

def brute(nums):
    return min(nums)

def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:       # min is strictly right of mid
            lo = mid + 1
        else:                          # nums[mid] < nums[hi] (distinct): mid may be the min
            hi = mid
    return nums[lo]

random.seed(6)
for n in range(1, 15):
    for _ in range(200):
        base = sorted(random.sample(range(-30, 30), n))
        k = random.randrange(n)
        nums = base[k:] + base[:k]
        assert find_min(nums) == brute(nums)
print("cross-check ok")
for a in ([3,4,5,1,2],[4,5,6,7,0,1,2],[11,13,15,17],[2,1],[7]):
    print(a, "->", find_min(a))
# nums[lo]-comparison counterexample: both [1,2,3] (rotation 0) and [2,3,1] have nums[mid] >= nums[lo]
print("[1,2,3] mid>=lo:", [1,2,3][1] >= [1,2,3][0], "| [2,3,1] mid>=lo:", [2,3,1][1] >= [2,3,1][0])
