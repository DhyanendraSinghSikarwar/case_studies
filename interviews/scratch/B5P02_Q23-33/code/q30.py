import random
from collections import Counter


def nice_brute(nums, k):
    total = 0
    for i in range(len(nums)):
        odds = 0
        for j in range(i, len(nums)):
            odds += nums[j] & 1
            total += odds == k
    return total


def at_most(nums, k):
    # number of subarrays with at most k odd numbers; one shrink rule works here
    if k < 0:
        return 0
    left = odds = total = 0
    for right, x in enumerate(nums):
        odds += x & 1
        while odds > k:
            odds -= nums[left] & 1
            left += 1
        total += right - left + 1
    return total


def nice_window(nums, k):
    return at_most(nums, k) - at_most(nums, k - 1)


def nice_prefix(nums, k):
    # alternative: count prefix odd-counts (the Part 1 'subarray sum equals k' idea)
    seen = Counter({0: 1})
    odds = total = 0
    for x in nums:
        odds += x & 1
        total += seen[odds - k]
        seen[odds] += 1
    return total


print("[1,1,2,1,1], 3:", nice_window([1, 1, 2, 1, 1], 3), "(expected 2)")
print("[2,4,6], 1:", nice_window([2, 4, 6], 1), "(expected 0)")
t = [2, 2, 2, 1, 2, 2, 1, 2, 2, 2]
print("[2,2,2,1,2,2,1,2,2,2], 2:", nice_window(t, 2), nice_prefix(t, 2), "(expected 16)")

random.seed(30)
for _ in range(1000):
    n = random.randint(0, 12)
    nums = [random.randint(-5, 5) for _ in range(n)]  # negatives: x & 1 still gives parity
    k = random.randint(1, 4)
    b = nice_brute(nums, k)
    assert nice_window(nums, k) == b == nice_prefix(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert nice_window([], 1) == 0
assert nice_window([1], 1) == 1
assert nice_window([2], 1) == 0
assert nice_window([1, 1, 1], 1) == 3
assert nice_window([1, 1, 1], 4) == 0  # k above the number of odds
assert nice_window([2, 2, 2], 1) == 0
assert nice_window([1, 2, 3, 4, 5], 2) == nice_brute([1, 2, 3, 4, 5], 2)
big = [random.randint(1, 100) for _ in range(5 * 10 ** 4)]
assert nice_window(big, 3) == nice_prefix(big, 3)
print("edge asserts passed")
