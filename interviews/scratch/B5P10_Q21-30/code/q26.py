import random, itertools

random.seed(26)

def kadane_max_min(nums):
    mx = cur = mn = curm = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x); mx = max(mx, cur)
        curm = min(x, curm + x); mn = min(mn, curm)
    return mx, mn

def circular(nums):
    """max(best normal subarray, total - min subarray), except when every element is negative (then the
    minimum subarray is the whole list and total - mn = 0 would be an EMPTY subarray)."""
    mx, mn = kadane_max_min(nums)
    if mx < 0:
        return mx
    return max(mx, sum(nums) - mn)

def naive(nums):
    mx, mn = kadane_max_min(nums)
    return max(mx, sum(nums) - mn)

def brute(nums):
    n = len(nums); best = None
    for s in range(n):
        tot = 0
        for L in range(1, n + 1):
            tot += nums[(s + L - 1) % n]
            if best is None or tot > best: best = tot
    return best

for nums, exp in [([1, -2, 3, -2], 3), ([5, -3, 5], 10), ([-3, -2, -3], -2), ([3, -1, 2, -1], 4), ([4], 4)]:
    assert circular(nums) == brute(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [5, -3, 5]
mx, mn = kadane_max_min(nums)
print('walk-through', nums, ': total', sum(nums), '| best normal', mx, '| min middle', mn, '| wrap =', sum(nums), '-', mn, '=', sum(nums) - mn, '| answer', circular(nums))
nums = [-3, -2, -3]
mx, mn = kadane_max_min(nums)
print('all-negative', nums, ': best normal', mx, '| min', mn, '| total - min =', sum(nums) - mn, '(empty subarray!) | answer', circular(nums))

# exhaustive: every list of length 1..5 with values -3..3, plus seeded random
cnt = bad_naive = 0
for n in range(1, 6):
    for t in itertools.product(range(-3, 4), repeat=n):
        l = list(t); assert circular(l) == brute(l), l
        cnt += 1; bad_naive += naive(l) != brute(l)
print('exhaustive lists', cnt, '| naive formula wrong on', bad_naive)
allneg_bad = 0
for n in range(1, 6):
    for t in itertools.product(range(-3, 4), repeat=n):
        l = list(t)
        if naive(l) != brute(l):
            assert max(l) < 0; allneg_bad += 1
print('every naive failure is an all-negative list:', allneg_bad == bad_naive)
for _ in range(500):
    n = random.randint(1, 12); l = [random.randint(-9, 9) for _ in range(n)]
    assert circular(l) == brute(l), l
print('500 seeded random lists agree with the O(n^2) circular enumeration')

big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
print('n = 10^5 answer', circular(big))
assert circular([4]) == 4 and circular([-1]) == -1 and circular([2, 2]) == 4 and circular([-1, 5, -1]) == 5
print('edge asserts passed')
