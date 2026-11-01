import random
import itertools
from functools import lru_cache

random.seed(12)

def rob_line(nums):
    """Linear house robber, bottom-up, O(1) space: best[i] = max(best[i-1], best[i-2] + nums[i])."""
    prev2, prev1 = 0, 0                 # best for the prefixes of length i-2 and i-1
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

def rob_circle(nums):
    """Circular: house 0 and house n-1 are neighbours, so one of them is skipped. Try both ranges."""
    if len(nums) == 1:
        return nums[0]
    return max(rob_line(nums[:-1]), rob_line(nums[1:]))

def rob_circle_memo(nums):
    """Top-down version of the same thing. Fine for small n; nests ~n deep, so it breaks past the recursion limit."""
    def solve(arr):
        @lru_cache(maxsize=None)
        def best(i):                    # best total using houses 0..i of arr
            if i < 0:
                return 0
            return max(best(i - 1), best(i - 2) + arr[i])
        return best(len(arr) - 1)
    if len(nums) == 1:
        return nums[0]
    return max(solve(tuple(nums[:-1])), solve(tuple(nums[1:])))

def brute(nums):
    """Oracle: every subset, valid only if no two chosen houses are neighbours around the circle."""
    n, best = len(nums), 0
    for mask in range(1 << n):
        if n > 1 and any(mask >> i & 1 and mask >> ((i + 1) % n) & 1 for i in range(n) if (i + 1) % n != i):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best

for nums, want in [([2, 3, 2], 3), ([1, 2, 3, 1], 4), ([7], 7), ([5, 1], 5), ([4, 1, 1, 4], 5)]:
    assert rob_circle(nums) == rob_circle_memo(nums) == brute(nums) == want, nums
print('5 prompt examples ok')

# table walk-through on [2, 3, 2]: range A = houses 0..1 = [2, 3], range B = houses 1..2 = [3, 2]
def table(arr):
    best = []
    for i, x in enumerate(arr):
        best.append(max(best[i - 1] if i >= 1 else 0, (best[i - 2] if i >= 2 else 0) + x))
    return best
nums = [2, 3, 2]
print('range A nums[:-1] =', nums[:-1], 'best =', table(nums[:-1]))
print('range B nums[1:]  =', nums[1:], 'best =', table(nums[1:]))
print('answer = max(%d, %d) = %d' % (table(nums[:-1])[-1], table(nums[1:])[-1], rob_circle(nums)))
print('the (wrong) line answer 2+2 on [2,3,2] would be', rob_line(nums), '- it takes both ends, which are neighbours in a circle')

# claim: every valid circular choice skips house 0 or skips house n-1 (so the two ranges cover everything)
for n in range(2, 13):
    for mask in range(1 << n):
        valid = all(not (mask >> i & 1 and mask >> ((i + 1) % n) & 1) for i in range(n))
        if valid:
            assert not (mask & 1 and mask >> (n - 1) & 1)
print('claim checked for n = 2..12: no valid circular selection holds both house 0 and house n-1')

# exhaustive: every list of length 1..6 with values 0..3
count = 0
for n in range(1, 7):
    for nums in itertools.product(range(4), repeat=n):
        assert rob_circle(list(nums)) == brute(list(nums)), nums
        count += 1
print('exhaustive small inputs agree:', count)

# seeded random cross-check, len <= 12
for _ in range(500):
    nums = [random.randint(0, 400) for _ in range(random.randint(1, 12))]
    assert rob_circle(nums) == rob_circle_memo(nums) == brute(nums), nums
print('500 random cases agree (bottom-up = memo = subset enumeration)')

# recursion limit: memoised top-down at large n
big = [random.randint(0, 400) for _ in range(10**5)]
try:
    rob_circle_memo(big)
    print('memo at n=10^5: no error (unexpected)')
except RecursionError:
    print('memo at n=10^5: RecursionError under the default limit')
print('bottom-up at n=10^5 ->', rob_circle(big))

# edge cases
assert rob_circle([0]) == 0 and rob_circle([0, 0]) == 0 and rob_circle([9, 9, 9]) == 9
assert rob_circle([1, 2, 3, 4, 5, 6]) == brute([1, 2, 3, 4, 5, 6]) == 12
print('edge cases ok')
