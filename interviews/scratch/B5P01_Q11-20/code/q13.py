import random
from collections import defaultdict

def brute(nums, k):
    n, cnt = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == k:
                cnt += 1
    return cnt

def optimal(nums, k):
    seen = defaultdict(int)
    seen[0] = 1                      # empty prefix
    pref = cnt = 0
    for x in nums:
        pref += x
        cnt += seen[pref - k]        # look up BEFORE inserting current prefix
        seen[pref] += 1
    return cnt

def sliding_window_wrong(nums, k):   # valid only for non-negative values
    lo = s = cnt = 0
    for hi, x in enumerate(nums):
        s += x
        while s > k and lo <= hi:
            s -= nums[lo]; lo += 1
        if s == k:
            cnt += 1
    return cnt

assert optimal([1, 1, 1], 2) == 2
assert optimal([1, 2, 3], 3) == 2
assert optimal([], 0) == 0
assert optimal([0, 0, 0], 0) == 6          # all subarrays of zeros
assert optimal([1, -1, 0], 0) == 3
assert optimal([5], 5) == 1
assert optimal([-1, -1, 1], 0) == 1
assert optimal([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4

rng = random.Random(13)
for _ in range(500):
    a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 10))]
    k = rng.randint(-4, 4)
    assert optimal(a, k) == brute(a, k), (a, k)
print("500 random cases agree with brute force")
print("sliding window on [1,-1,1], k=1:", sliding_window_wrong([1, -1, 1], 1), "but truth is", optimal([1, -1, 1], 1))
print(optimal([1, 1, 1], 2), optimal([1, 2, 3], 3))
