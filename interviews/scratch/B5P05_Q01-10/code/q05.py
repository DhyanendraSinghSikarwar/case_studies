import random

def brute(nums, t):
    return nums.index(t) if t in nums else -1

def search_rotated(nums, t):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == t:
            return mid
        if nums[lo] <= nums[mid]:              # left half [lo..mid] sorted (<= for lo == mid)
            if nums[lo] <= t < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                  # right half [mid..hi] sorted
            if nums[mid] < t <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

random.seed(5)
cnt = 0
for n in range(1, 13):
    for _ in range(150):
        base = sorted(random.sample(range(-20, 40), n))
        k = random.randrange(n)
        nums = base[k:] + base[:k]
        for t in range(-22, 42):
            assert search_rotated(nums, t) == brute(nums, t)
            cnt += 1
print("cross-check ok:", cnt, "queries")
for a, t in [([4,5,6,7,0,1,2],0),([4,5,6,7,0,1,2],3),([1],0),([3,1],1),([1,3],3)]:
    print(a, t, "->", search_rotated(a, t))
