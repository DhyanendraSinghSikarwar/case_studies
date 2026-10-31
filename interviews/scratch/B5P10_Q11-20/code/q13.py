import random
import itertools
from functools import lru_cache

random.seed(13)

def max_product(nums):
    """Optimal: keep the max AND min product of a subarray ending here. O(n) time, O(1) space."""
    best = hi = lo = nums[0]
    for x in nums[1:]:
        cands = (x, hi * x, lo * x)      # start fresh at x, or extend the old max / old min
        hi, lo = max(cands), min(cands)
        best = max(best, hi)
    return best

def max_product_no_min(nums):
    """The tempting bug: track only the maximum."""
    best = hi = nums[0]
    for x in nums[1:]:
        hi = max(x, hi * x)
        best = max(best, hi)
    return best

def max_product_memo(nums):
    """Top-down: (max, min) ending at i. Nests n deep."""
    @lru_cache(maxsize=None)
    def ending(i):
        if i == 0:
            return nums[0], nums[0]
        hi, lo = ending(i - 1)
        c = (nums[i], hi * nums[i], lo * nums[i])
        return max(c), min(c)
    ending(len(nums) - 1)                # ask for the LAST index first: the recursion goes n deep
    return max(ending(i)[0] for i in range(len(nums)))

def brute(nums):
    """Oracle: every subarray, O(n^2) with a running product."""
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best

for nums, want in [([2, 3, -2, 4], 6), ([-2, 0, -1], 0), ([-3], -3), ([-2, 3, -4], 24), ([0, 2], 2)]:
    assert max_product(nums) == max_product_memo(nums) == brute(nums) == want, nums
print('5 prompt examples ok')

# table walk-through on [2, 3, -2, 4]
nums = [2, 3, -2, 4]
print('i  x   max_end  min_end  best')
best = hi = lo = nums[0]
print('0  %-3d %-8d %-8d %d' % (nums[0], hi, lo, best))
for i in range(1, len(nums)):
    x = nums[i]
    c = (x, hi * x, lo * x)
    hi, lo = max(c), min(c)
    best = max(best, hi)
    print('%d  %-3d %-8d %-8d %d' % (i, x, hi, lo, best))
print('zero resets both: trace on [-2, 0, -1]')
hi = lo = best = -2
print('  i=0 x=-2 max_end=-2 min_end=-2')
for i, x in enumerate([0, -1], start=1):
    c = (x, hi * x, lo * x)
    hi, lo = max(c), min(c)
    best = max(best, hi)
    print('  i=%d x=%-2d max_end=%d min_end=%d best=%d' % (i, x, hi, lo, best))
print('[-2, 3, -4]: with min ->', max_product([-2, 3, -4]), ' max-only ->', max_product_no_min([-2, 3, -4]))

# exhaustive: all lists of length 1..6 with values -3..3
count = bad_no_min = 0
for n in range(1, 7):
    for nums in itertools.product(range(-3, 4), repeat=n):
        nums = list(nums)
        assert max_product(nums) == brute(nums), nums
        bad_no_min += max_product_no_min(nums) != brute(nums)
        count += 1
print('exhaustive small inputs agree:', count, '; max-only variant wrong on', bad_no_min)

# seeded random cross-check
for _ in range(500):
    nums = [random.randint(-6, 6) for _ in range(random.randint(1, 12))]
    assert max_product(nums) == max_product_memo(nums) == brute(nums), nums
print('500 random cases agree (bottom-up = memo = O(n^2) enumeration)')

# recursion limit at large n
big = [random.randint(-10, 10) for _ in range(2 * 10**4)]
try:
    max_product_memo(big)
    print('memo at n=2*10^4: no error (unexpected)')
except RecursionError:
    print('memo at n=2*10^4: RecursionError under the default limit')
print('bottom-up at n=2*10^4 has', len(str(max_product(big))), 'digit answer (Python ints do not overflow)')
assert max_product([-1] * 3) == 1 and max_product([0]) == 0 and max_product([-2, -3]) == 6 and max_product([0, 0, -1]) == 0
print('edge cases ok')
