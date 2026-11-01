import random


def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_sorted(nums, target):
    i, j = 0, len(nums) - 1
    while i < j:
        s = nums[i] + nums[j]
        if s == target:
            return (i, j)
        if s < target:
            i += 1
        else:
            j -= 1
    return None


for nums, t in [([2, 7, 11, 15], 9), ([2, 3, 4], 6), ([-1, 0], -1)]:
    print(nums, t, "->", two_sum_sorted(nums, t))
assert two_sum_sorted([2, 7, 11, 15], 9) == (0, 1)
assert two_sum_sorted([2, 3, 4], 6) == (0, 2)
assert two_sum_sorted([-1, 0], -1) == (0, 1)
assert two_sum_sorted([3, 3], 6) == (0, 1)             # duplicates, different positions
assert two_sum_sorted([-5, -3, -1], -8) == (0, 1)      # all negative
assert two_sum_sorted([1, 2], 100) is None             # no pair (outside the promise)

rng = random.Random(11)
cases = 0
for _ in range(2000):
    n = rng.randint(2, 9)
    nums = sorted(rng.randint(-6, 6) for _ in range(n))
    # pick a target; keep only inputs with exactly one valid pair (the promise)
    i, j = sorted(rng.sample(range(n), 2))
    t = nums[i] + nums[j]
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if nums[a] + nums[b] == t]
    if len(pairs) != 1:
        continue
    assert two_sum_sorted(nums, t) == two_sum_brute(nums, t) == pairs[0]
    cases += 1
print("random cross-check passed:", cases, "unique-pair cases")
