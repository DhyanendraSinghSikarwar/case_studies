import itertools
import random
import sys
from functools import cache

random.seed(105)

def rob(nums):
    """dp[i] = best total using houses 0..i, dp[i] = max(dp[i-1] (skip i), dp[i-2] + nums[i] (take i)),
    with dp[-1] = dp[-2] = 0 (no houses). Two variables."""
    skip, take = 0, 0          # dp[i-2], dp[i-1]
    for x in nums:
        skip, take = take, max(take, skip + x)
    return take

def rob_table(nums):
    dp = []                       # dp[i] = best using houses 0..i
    for i, x in enumerate(nums):
        dp.append(max(dp[i - 1] if i >= 1 else 0, (dp[i - 2] if i >= 2 else 0) + x))
    return dp

def rob_memo(nums):
    @cache
    def f(i):                      # best using houses 0..i
        if i < 0:
            return 0
        return max(f(i - 1), f(i - 2) + nums[i])
    return f(len(nums) - 1)

def brute(nums):
    """All subsets with no two adjacent houses (n <= 12): 4096 masks."""
    n = len(nums); best = 0
    for mask in range(1 << n):
        if mask & (mask >> 1):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best

for a, want in [([1, 2, 3, 1], 4), ([2, 7, 9, 3, 1], 12), ([], 0), ([5], 5), ([4, 1, 1, 4], 8)]:
    assert rob(a) == rob_memo(a) == brute(a) == want
print('5 prompt examples ok')

print('nums =', [2, 7, 9, 3, 1])
print('dp   =', rob_table([2, 7, 9, 3, 1]), ' (dp[i] = best using houses 0..i)')

for _ in range(1000):
    n = random.randint(0, 12)
    a = [random.randint(0, 400) for _ in range(n)]
    assert rob(a) == brute(a) == (rob_table(a) or [0])[-1] == rob_memo(a), a
print('1000 seeded random streets (len 0..12, cash 0..400): DP == subset enumeration')

cnt = 0
for n in range(0, 8):
    for a in itertools.product(range(4), repeat=n):
        assert rob(list(a)) == brute(list(a)); cnt += 1
print('exhaustive len 0..7 values 0..3:', cnt, 'streets ok')

# greedy "take the biggest house first" is wrong: 4 1 1 4 style
a = [2, 3, 2]
print('greedy-by-largest on [2, 3, 2] takes 3 -> 3, optimum is', rob(a))
assert rob(a) == 4

big = [random.randint(0, 400) for _ in range(10**5)]
print('n = 10^5 bottom-up ->', rob(big))
try:
    rob_memo(big)
    print('memoised: ok')
except RecursionError:
    print('memoised n = 10^5: RecursionError (default limit', sys.getrecursionlimit(), ')')
print('memoised n = 300 ->', rob_memo(big[:300]), '== bottom-up', rob(big[:300]))
