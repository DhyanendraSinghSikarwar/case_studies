import random


def max_avg_brute(nums, k):
    return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1)) / k


def max_avg_window(nums, k):
    s = sum(nums[:k])
    best = s
    for r in range(k, len(nums)):
        s += nums[r] - nums[r - k]     # add entering, drop leaving
        if s > best:
            best = s
    return best / k


print(max_avg_window([1, 12, -5, -6, 50, 3], 4))
print(max_avg_window([5], 1))
assert max_avg_window([1, 12, -5, -6, 50, 3], 4) == 12.75
assert max_avg_window([5], 1) == 5.0
assert max_avg_window([-3, -1, -2], 2) == -1.5          # all negative: do not start best at 0
assert max_avg_window([4, 4, 4], 3) == 4.0              # k == len
assert max_avg_window([0, 0], 1) == 0.0
big = list(range(100000))
assert max_avg_window(big, 100000) == sum(big) / 100000  # max size, k == len

rng = random.Random(3)
cases = 0
for _ in range(1500):
    n = rng.randint(1, 12)
    nums = [rng.randint(-9, 9) for _ in range(n)]
    k = rng.randint(1, n)
    assert max_avg_window(nums, k) == max_avg_brute(nums, k)
    cases += 1
print("random cross-check passed:", cases, "cases")
