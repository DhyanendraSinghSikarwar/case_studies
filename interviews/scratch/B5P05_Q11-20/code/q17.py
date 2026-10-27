import itertools
import random


def search_rot_dup(nums, target):
    """Returns (found, loop_iterations)."""
    lo, hi, steps = 0, len(nums) - 1, 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True, steps
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1                      # neither end can be the target (== nums[mid] != target)
            hi -= 1
        elif nums[lo] <= nums[mid]:      # left half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                            # right half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False, steps


def brute(nums, target):
    return target in nums


examples = [([2, 5, 6, 0, 0, 1, 2], 0, True), ([2, 5, 6, 0, 0, 1, 2], 3, False),
            ([1, 0, 1, 1, 1], 0, True), ([1, 1, 1, 1], 2, False), ([1, 1, 1, 1, 0, 1, 1], 0, True)]
for nums, t, exp in examples:
    got, steps = search_rot_dup(nums, t)
    assert got == exp == brute(nums, t)
    print(nums, t, "->", got, "(loop steps %d)" % steps)

# exhaustive: every sorted list over values 0..3 (len 1..8), every rotation, every target -1..4
cases = 0
for n in range(1, 9):
    for base in itertools.combinations_with_replacement(range(4), n):
        base = list(base)
        for r in range(n):
            nums = base[r:] + base[:r]
            for t in range(-1, 5):
                assert search_rot_dup(nums, t)[0] == brute(nums, t), (nums, t)
                cases += 1
print("exhaustive: %d (rotated list, target) cases agree with 'in'" % cases)

random.seed(17)
for _ in range(500):
    n = random.randint(1, 40)
    base = sorted(random.randint(0, 6) for _ in range(n))
    r = random.randrange(n)
    nums = base[r:] + base[:r]
    t = random.randint(-1, 7)
    assert search_rot_dup(nums, t)[0] == brute(nums, t)
print("seeded random check: 500 cases agree")

# worst case: all equal, target absent -> every step removes only 2 elements
for n in (100, 1000, 5000):
    found, steps = search_rot_dup([1] * n, 2)
    print("all ones, n=%d, target 2: found=%s, loop steps=%d" % (n, found, steps))
    assert not found and steps == (n + 1) // 2
# another bad shape: one odd element hidden away from mid
n = 5000
nums = [1] * n
nums[1] = 0                                 # rotated [0,1,1,...] style with the 0 near the front
found, steps = search_rot_dup(nums, 0)
print("5000 ones with a 0 at index 1, target 0: found=%s, loop steps=%d" % (found, steps))
# distinct values: log steps
found, steps = search_rot_dup(list(range(2500, 5000)) + list(range(2500)), 7777)
print("5000 distinct rotated, absent target: steps =", steps)

# edge cases
assert search_rot_dup([1], 1)[0] is True and search_rot_dup([1], 0)[0] is False
assert search_rot_dup([3, 1], 1)[0] is True
assert search_rot_dup([1, 3, 1, 1, 1], 3)[0] is True
assert search_rot_dup([1, 1, 3, 1], 3)[0] is True
print("edge asserts passed")
