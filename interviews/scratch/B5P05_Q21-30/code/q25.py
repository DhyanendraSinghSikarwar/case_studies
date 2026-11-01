import itertools
import random
from collections import Counter


def single_brute(nums):
    return next(v for v, c in Counter(nums).items() if c == 1)


def single_xor(nums):
    r = 0
    for v in nums:
        r ^= v                              # O(n) time, O(1) space: the linear baseline (pairs cancel)
    return r


def single_bs(nums):
    lo, hi = 0, len(nums) - 1               # lo and hi are always even
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2 == 1:
            mid -= 1                        # make mid even: pair partner is mid + 1
        if nums[mid] == nums[mid + 1]:      # pair intact at (even, odd): single is to the right
            lo = mid + 2
        else:                               # pair broken: single is at mid or to the left
            hi = mid
    return nums[lo]


for nums, want in [([1, 1, 2, 3, 3, 4, 4, 8, 8], 2), ([3, 3, 7, 7, 10, 11, 11], 10),
                   ([5], 5), ([1, 2, 2], 1), ([1, 1, 2], 2)]:
    assert single_bs(nums) == single_xor(nums) == single_brute(nums) == want, nums
    print(nums, "->", single_bs(nums))

# exhaustive: choose distinct values (the pair values plus the single), every position of the single,
# input is sorted and valid by construction; also assert the statement's promise (exactly one value with count 1)
tested = 0
for d in range(1, 9):                       # number of distinct values; length = 2*d - 1
    for vals in itertools.combinations(range(-3, 9), d):
        for s in range(d):                  # which distinct value is the single one
            nums = []
            for i, v in enumerate(vals):
                nums += [v] if i == s else [v, v]
            cnt = Counter(nums)
            assert sum(1 for c in cnt.values() if c == 1) == 1 and len(nums) % 2 == 1
            assert single_bs(nums) == vals[s] == single_brute(nums), nums
            tested += 1
print("exhaustive check passed:", tested, "valid inputs (up to 15 elements)")

# seeded random big input
rng = random.Random(25)
for _ in range(300):
    d = rng.randint(1, 600)
    vals = sorted(rng.sample(range(-10 ** 6, 10 ** 6), d))
    s = rng.randrange(d)
    nums = []
    for i, v in enumerate(vals):
        nums += [v] if i == s else [v, v]
    assert single_bs(nums) == vals[s]
print("random check passed: 300 inputs up to 1199 elements")

# edge cases
assert single_bs([0]) == 0
assert single_bs([1, 1, 2, 2, 3]) == 3                  # single at the very end
assert single_bs([0, 1, 1, 2, 2]) == 0                  # single at the very start
big = [v for i in range(50000) for v in (i, i)] + [10 ** 9]
assert single_bs(big) == 10 ** 9 and len(big) == 100001
print("edge asserts passed")
