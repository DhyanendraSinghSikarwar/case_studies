import itertools
import random

random.seed(2101)

def pivot_index(nums):
    """O(n): returns [leftmost pivot or -1, running sums]."""
    running = list(itertools.accumulate(nums))
    total = running[-1]
    for i, x in enumerate(nums):
        left = running[i] - x            # sum of nums[:i]
        right = total - running[i]       # sum of nums[i+1:]
        if left == right:
            return [i, running]          # first hit = leftmost
    return [-1, running]

def brute(nums):
    run, s = [], 0
    for v in nums:
        s += v
        run.append(s)
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1:]):   # rescan both sides: O(n^2)
            return [i, run]
    return [-1, run]

examples = [([1, 7, 3, 6, 5, 6], [3, [1, 8, 11, 17, 22, 28]]),
            ([1, 2, 3], [-1, [1, 3, 6]]),
            ([2, 1, -1], [0, [2, 3, 2]]),
            ([0], [0, [0]])]
for nums, want in examples:
    assert pivot_index(nums) == want == brute(nums)
    print(nums, '->', pivot_index(nums))

# dry run on the first example
nums = [1, 7, 3, 6, 5, 6]
run = list(itertools.accumulate(nums)); total = run[-1]
for i, x in enumerate(nums):
    print(f'  i={i} x={x} left={run[i] - x} right={total - run[i]}')

# seeded random cross-check
for _ in range(3000):
    nums = [random.randint(-4, 4) for _ in range(random.randint(1, 9))]
    assert pivot_index(nums) == brute(nums)
print('random cross-check ok: 3000 cases')

# exhaustive: every list of length 1..6 over -2..2
total_lists = several = 0
for n in range(1, 7):
    for nums in itertools.product(range(-2, 3), repeat=n):
        nums = list(nums)
        assert pivot_index(nums) == brute(nums)
        total_lists += 1
        all_piv = [i for i in range(n) if sum(nums[:i]) == sum(nums[i + 1:])]
        if len(all_piv) > 1:
            several += 1
            assert pivot_index(nums)[0] == all_piv[0]     # leftmost wins
print('exhaustive ok:', total_lists, 'lists; with 2+ valid pivots:', several)
print('example with 2 pivots:', [0, 0], '->', pivot_index([0, 0])[0], '(index 1 also qualifies)')

# edge asserts
assert pivot_index([5])[0] == 0                      # both sides empty
assert pivot_index([-1, 3, -1])[0] == 1             # negatives are fine: -1 on both sides
assert pivot_index([1, -1])[0] == -1
big = [1000] * 10**4
assert pivot_index(big)[0] == -1 and pivot_index(big)[1][-1] == 10**7
print('edge asserts ok')
