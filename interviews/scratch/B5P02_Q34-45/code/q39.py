import random

def brute(nums, x):
    n, best = len(nums), -1
    for a in range(n + 1):                # take a from the left
        for b in range(n - a + 1):        # take b from the right
            taken = sum(nums[:a]) + (sum(nums[n - b:]) if b else 0)
            if taken == x and (best == -1 or a + b < best):
                best = a + b
    return best

def min_ops(nums, x):
    target = sum(nums) - x
    if target < 0: return -1
    l = s = 0
    longest = -1                           # -1: no middle window found
    for r, v in enumerate(nums):
        s += v
        while s > target and l <= r:       # valid shrink because values are positive
            s -= nums[l]; l += 1
        if s == target:
            longest = max(longest, r - l + 1)
    if target == 0: longest = max(longest, 0)
    return -1 if longest == -1 else len(nums) - longest

for nums, x, exp in [([1, 1, 4, 2, 3], 5, 2), ([5, 6, 7, 8, 9], 4, -1), ([3, 2, 20, 1, 1, 3], 10, 5)]:
    assert min_ops(nums, x) == brute(nums, x) == exp
    print(nums, "x =", x, "->", min_ops(nums, x))
assert min_ops([1, 2, 3], 6) == 3 and min_ops([1, 2, 3], 7) == -1 and min_ops([5], 5) == 1 and min_ops([5], 3) == -1
assert min_ops([1, 1, 1, 1], 4) == 4 and min_ops([2, 3], 3) == 1
random.seed(39)
for _ in range(1500):
    nums = [random.randint(1, 5) for _ in range(random.randint(1, 8))]
    x = random.randint(1, 25)
    assert min_ops(nums, x) == brute(nums, x), (nums, x)
print("1500 seeded cases match brute force; edges pass")
