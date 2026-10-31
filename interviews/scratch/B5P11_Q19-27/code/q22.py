import random, sys, time
from functools import lru_cache

random.seed(22)

def burst(nums):
    """dp[l][r] = best coins for the balloons strictly between l and r, which stay un-burst until the end (open interval)."""
    a = [1] + list(nums) + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):                   # r - l = 2 is one balloon between; shorter intervals are empty (0)
        for l in range(0, n - length):
            r = l + length
            best = 0
            for k in range(l + 1, r):            # k = the balloon burst LAST inside (l, r)
                c = dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]
                if c > best: best = c
            dp[l][r] = best
    return dp[0][n - 1]

def burst_table(nums):
    a = [1] + list(nums) + [1]; n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            dp[l][r] = max(dp[l][k] + dp[k][r] + a[l] * a[k] * a[r] for k in range(l + 1, r))
    return a, dp

def memo(nums):
    a = [1] + list(nums) + [1]
    @lru_cache(maxsize=None)
    def f(l, r):
        return max((f(l, k) + f(k, r) + a[l] * a[k] * a[r] for k in range(l + 1, r)), default=0)
    return f(0, len(a) - 1)

def brute(nums):
    """Every burst order by plain recursion on the current list (neighbours are the CURRENT neighbours)."""
    def f(arr):
        if not arr: return 0
        return max((arr[i - 1] if i else 1) * arr[i] * (arr[i + 1] if i + 1 < len(arr) else 1) + f(arr[:i] + arr[i + 1:])
                   for i in range(len(arr)))
    return f(list(nums))

def first_burst_wrong(nums):
    """Tempting split on the FIRST balloon: pretend the two sides become independent, each with outer neighbours 1."""
    nums = list(nums)
    if not nums: return 0
    best = 0
    for k in range(len(nums)):
        left = nums[k - 1] if k else 1
        right = nums[k + 1] if k + 1 < len(nums) else 1
        best = max(best, left * nums[k] * right + first_burst_wrong(nums[:k]) + first_burst_wrong(nums[k + 1:]))
    return best

# examples
for nums, exp in [([3, 1, 5, 8], 167), ([1, 5], 10), ([7], 7), ([], 0), ([2, 2, 2], 14)]:
    a, b, c = burst(nums), brute(nums), memo(nums)
    assert a == b == c == exp, (nums, a, b, c)
    print('example', nums, '->', a)

# hand table for [3,1,5,8]
a, dp = burst_table([3, 1, 5, 8])
print('padded list', a)
print('dp[l][r] (open interval, rows l, columns r):')
for l in range(len(a)):
    print('  l=%d' % l, dp[l])
print('dp[0][5] = 167, last balloon k tried in (0,5):')
for k in range(1, 5):
    print('   k=%d (value %d): dp[0][%d] + dp[%d][5] + 1*%d*1 = %d + %d + %d = %d' % (k, a[k], k, k, a[k], dp[0][k], dp[k][5], a[0] * a[k] * a[5], dp[0][k] + dp[k][5] + a[0] * a[k] * a[5]))

# seeded cross-check, len <= 7
cases = 0
for _ in range(400):
    nums = [random.randint(0, 9) for _ in range(random.randint(0, 7))]
    assert burst(nums) == brute(nums) == memo(nums), nums
    cases += 1
print('cross-check cases', cases)
wrong = 0
for _ in range(300):
    nums = [random.randint(1, 9) for _ in range(random.randint(2, 6))]
    wrong += first_burst_wrong(nums) != burst(nums)
print('first-burst split disagrees with the true optimum on', wrong, 'of 300 random lists; e.g. [3, 1, 5, 8] gives', first_burst_wrong([3, 1, 5, 8]), 'not 167')

# edge cases (values 0..100, zeros included)
assert burst([0]) == 0 and burst([0, 0, 0]) == 0 and burst([100]) == 100
assert burst([100, 100]) == 100 * 100 + 100
print('edge asserts passed')

# max size n = 300, bottom-up; memo depth
print('recursion limit', sys.getrecursionlimit())
nums = [random.randint(0, 100) for _ in range(300)]
t0 = time.perf_counter(); r = burst(nums); t1 = time.perf_counter()
print('n=300 bottom-up:', r, '(sandbox timing %.1f s)' % (t1 - t0))
try:
    print('n=300 memoised equals bottom-up:', memo(nums) == r)
except RecursionError:
    print('n=300 memoised: RecursionError')
big = [random.randint(0, 100) for _ in range(1100)]
try:
    memo(big); print('n=1100 memoised ran')
except RecursionError:
    print('n=1100 memoised: RecursionError (depth grows with n; outside the stated sizes)')
