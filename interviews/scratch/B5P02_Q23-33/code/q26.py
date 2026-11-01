import random


def prod_brute(nums, k):
    total = 0
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            if p < k:
                total += 1
    return total


def prod_window(nums, k):
    if k <= 1:  # every product is >= 1, so none is < 1
        return 0
    left = total = 0
    prod = 1
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:
            prod //= nums[left]  # exact: prod is a multiple of nums[left]
            left += 1
        total += right - left + 1  # subarrays ending at right
    return total


print("[10,5,2,6], 100:", prod_window([10, 5, 2, 6], 100), "(expected 8)")
print("[1,2,3], 0:", prod_window([1, 2, 3], 0), "(expected 0)")

random.seed(26)
for _ in range(1000):
    n = random.randint(0, 9)
    nums = [random.randint(1, 6) for _ in range(n)]
    k = random.randint(0, 60)
    assert prod_window(nums, k) == prod_brute(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert prod_window([], 10) == 0
assert prod_window([1], 1) == 0
assert prod_window([1], 2) == 1
assert prod_window([1, 1, 1], 2) == 6  # all 3+2+1 subarrays have product 1
assert prod_window([5], 5) == 0  # strictly less
assert prod_window([100], 100) == 0
assert prod_window([10 ** 6, 1], 10 ** 6) == 1  # only [1] qualifies
n = 3 * 10 ** 4
assert prod_window([1] * n, 2) == n * (n + 1) // 2
# big k: Python ints never overflow, the running product just stays below k
assert prod_window([2] * 60, 2 ** 70) == 60 * 61 // 2
print("edge asserts passed")
