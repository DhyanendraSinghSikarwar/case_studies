import random


def ones_brute(nums, k):
    best = 0
    for i in range(len(nums)):
        zeros = 0
        for j in range(i, len(nums)):
            zeros += nums[j] == 0
            if zeros > k:
                break
            best = max(best, j - i + 1)
    return best


def ones_window(nums, k):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:  # shrink until the window has at most k zeros
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


a = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
b = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
print("example 1:", ones_window(a, 2), "(expected 6)")
print("example 2:", ones_window(b, 3), "(expected 10)")

random.seed(23)
for _ in range(1000):
    n = random.randint(0, 12)
    nums = [random.randint(0, 1) for _ in range(n)]
    k = random.randint(0, 4)
    assert ones_window(nums, k) == ones_brute(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert ones_window([], 3) == 0
assert ones_window([0], 0) == 0
assert ones_window([0], 1) == 1
assert ones_window([1, 1, 1], 0) == 3
assert ones_window([0, 0, 0], 0) == 0
assert ones_window([0, 0, 0], 5) == 3  # k larger than the zero count: whole list
assert ones_window([1, 0, 1, 0, 1], 0) == 1
big = [random.randint(0, 1) for _ in range(10 ** 5)]
assert ones_window(big, 10) >= 11
assert ones_window([1] * 10 ** 5, 0) == 10 ** 5
print("edge asserts passed")
