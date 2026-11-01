import random
from collections import Counter


def exact_brute(nums, k):
    total = 0
    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            total += len(seen) == k
    return total


def at_most(nums, k):
    if k <= 0:
        return 0
    count = Counter()
    left = total = 0
    for right, x in enumerate(nums):
        count[x] += 1
        while len(count) > k:
            y = nums[left]
            count[y] -= 1
            if count[y] == 0:
                del count[y]  # keeps len(count) = distinct values, so memory stays O(k)
            left += 1
        total += right - left + 1
    return total


def exact_window(nums, k):
    return at_most(nums, k) - at_most(nums, k - 1)


print("[1,2,1,2,3], 2:", exact_window([1, 2, 1, 2, 3], 2), "(expected 7)")
print("[1,2,1,3,4], 3:", exact_window([1, 2, 1, 3, 4], 3), "(expected 3)")

random.seed(33)
for _ in range(1000):
    n = random.randint(0, 12)
    nums = [random.randint(1, 4) for _ in range(n)]
    k = random.randint(1, 5)
    assert exact_window(nums, k) == exact_brute(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert exact_window([], 1) == 0
assert exact_window([1], 1) == 1
assert exact_window([1, 1, 1], 1) == 6
assert exact_window([1, 1, 1], 2) == 0
assert exact_window([1, 2, 3], 3) == 1
assert exact_window([1, 2, 3], 4) == 0  # k above the distinct count
assert exact_window([1, 2], 1) == 2
big = [random.randint(1, 50) for _ in range(2 * 10 ** 4)]
assert exact_window(big, 5) > 0
assert exact_window(list(range(1, 20001)), 2) == 19999
print("edge asserts passed")
