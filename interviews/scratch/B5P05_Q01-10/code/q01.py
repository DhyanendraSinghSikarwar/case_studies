import random

def brute(nums, target):
    for i, v in enumerate(nums):
        if v == target:
            return i
    return -1

def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1          # invariant: target, if present, is in nums[lo..hi]
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1               # nums[lo..mid] all < target
        else:
            hi = mid - 1               # nums[mid..hi] all > target
    return -1

random.seed(1)
for _ in range(2000):
    n = random.randint(0, 12)
    nums = sorted(random.sample(range(-20, 20), n))
    for t in range(-22, 22):
        assert binary_search(nums, t) == brute(nums, t)
    lo, hi = random.randint(0, 10**18), random.randint(10**18, 2*10**18)
    assert lo + (hi - lo) // 2 == (lo + hi) // 2
print("cross-check ok: 2000 random lists x 44 targets")

assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
assert binary_search([5], 5) == 0
assert binary_search([5], 4) == -1
assert binary_search([], 1) == -1
big = list(range(0, 2 * 10**5, 2))
assert binary_search(big, 199998) == 99999 and binary_search(big, 199999) == -1
print(binary_search([-1, 0, 3, 5, 9, 12], 9), binary_search([-1, 0, 3, 5, 9, 12], 2),
      binary_search([5], 5), binary_search([5], 4))
