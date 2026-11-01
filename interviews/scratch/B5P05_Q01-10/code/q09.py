import random

def peaks(nums):
    n = len(nums)
    return [i for i in range(n)
            if (i == 0 or nums[i] > nums[i-1]) and (i == n-1 or nums[i] > nums[i+1])]

def brute(nums):
    return peaks(nums)[0]

def find_peak(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:   # uphill: a peak exists in mid+1..hi
            lo = mid + 1
        else:                           # downhill (never equal): a peak exists in lo..mid
            hi = mid
    return lo

random.seed(9)
for _ in range(5000):
    n = random.randint(1, 12)
    nums = [random.randint(-5, 5)]
    while len(nums) < n:
        v = random.randint(-5, 5)
        if v != nums[-1]:
            nums.append(v)
    assert find_peak(nums) in peaks(nums)       # any valid peak accepted; not equal to brute()'s index
print("cross-check ok: result always a valid peak")
for a in ([1,2,3,1],[1,2,1,3,5,6,4],[1],[2,1],[1,2]):
    print(a, "-> idx", find_peak(a), "all peaks", peaks(a))
assert peaks([1,2,1,3,5,6,4]) == [1, 5]
assert find_peak([1,2,1,3,5,6,4]) in (1, 5)
