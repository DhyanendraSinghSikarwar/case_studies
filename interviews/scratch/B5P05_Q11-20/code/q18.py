import itertools
import random


def find_min_dup(nums):
    """Returns (min value, loop steps)."""
    lo, hi, steps = 0, len(nums) - 1, 0
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1                 # min is strictly right of mid
        elif nums[mid] < nums[hi]:
            hi = mid                     # mid could be the min
        else:
            hi -= 1                      # equal: drop hi; value still held at mid
    return nums[lo], steps


def find_min_distinct(nums):
    """The distinct-values version: equal case is lumped with '<'. WRONG with duplicates."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


examples = [([1, 3, 5], 1), ([2, 2, 2, 0, 1], 0), ([10, 1, 10, 10, 10], 1), ([3, 3, 1, 3], 1), ([2, 2, 2, 2], 2)]
for nums, exp in examples:
    got, steps = find_min_dup(nums)
    assert got == exp == min(nums)
    print(nums, "->", got, "| distinct-version gives", find_min_distinct(nums))

cases = wrong = 0
for n in range(1, 9):
    for base in itertools.combinations_with_replacement(range(4), n):
        base = list(base)
        for r in range(n):
            nums = base[r:] + base[:r]
            assert find_min_dup(nums)[0] == min(nums), nums
            cases += 1
            if find_min_distinct(nums) != min(nums):
                wrong += 1
print("exhaustive: %d rotated lists, find_min_dup always == min(nums)" % cases)
print("the distinct-values version (equal lumped with '<') is wrong on %d of them" % wrong)

random.seed(18)
for _ in range(500):
    n = random.randint(1, 50)
    base = sorted(random.randint(-3, 3) for _ in range(n))
    r = random.randrange(n)
    nums = base[r:] + base[:r]
    assert find_min_dup(nums)[0] == min(nums)
print("seeded random check: 500 cases agree")

for n in (1000, 5000):
    print("all equal, n=%d: loop steps = %d" % (n, find_min_dup([4] * n)[1]))
    assert find_min_dup([4] * n)[1] == n - 1
nums = [10] * 5000
nums[2500] = 1
print("5000 tens with one 1 hidden mid-array: min, steps =", find_min_dup(nums))
print("5000 distinct rotated: steps =", find_min_dup(list(range(2500, 5000)) + list(range(2500)))[1])

assert find_min_dup([7])[0] == 7
assert find_min_dup([2, 1])[0] == 1
assert find_min_dup([1, 1, 1, 0, 1])[0] == 0
assert find_min_dup([0, 0, 0])[0] == 0
print("edge asserts passed")
