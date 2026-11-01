import random
import itertools
from functools import lru_cache

random.seed(19)

def target_sum(nums, target):
    """Optimal: signs = split into P (plus) and N (minus). P - N = target, P + N = S, so P = (S + target) / 2.
    Count subsets with sum P. O(n * P) time, O(P) space."""
    s = sum(nums)
    if abs(target) > s or (s + target) % 2:
        return 0
    need = (s + target) // 2
    dp = [1] + [0] * need                           # dp[w]: number of subsets (by index) with sum w
    for x in nums:
        for w in range(need, x - 1, -1):            # downward; for x = 0 this runs w = need..0 and doubles every cell
            dp[w] += dp[w - x]
    return dp[need]

def target_sum_memo(nums, target):
    """Top-down over (i, running signed total). Depth = len(nums) <= 20."""
    @lru_cache(maxsize=None)
    def go(i, total):
        if i == len(nums):
            return 1 if total == target else 0
        return go(i + 1, total + nums[i]) + go(i + 1, total - nums[i])
    return go(0, 0)

def target_sum_dict(nums, target):
    """Direct DP over signed totals (no reduction), the version you give first if you do not see the trick."""
    ways = {0: 1}
    for x in nums:
        nxt = {}
        for t, c in ways.items():
            nxt[t + x] = nxt.get(t + x, 0) + c
            nxt[t - x] = nxt.get(t - x, 0) + c
        ways = nxt
    return ways.get(target, 0)

def brute(nums, target):
    """Oracle: all 2^n sign assignments."""
    return sum(1 for signs in itertools.product((1, -1), repeat=len(nums)) if sum(a * b for a, b in zip(signs, nums)) == target)

for (nums, t), want in [(([1, 1, 1, 1, 1], 3), 5), (([1], 1), 1), (([0, 0, 1], 1), 4), (([1, 2], 4), 0)]:
    assert target_sum(nums, t) == target_sum_memo(nums, t) == target_sum_dict(nums, t) == brute(nums, t) == want
print('4 prompt examples ok')

# walk-through on [1,1,1,1,1], target 3: S = 5, P = (5 + 3) / 2 = 4
nums, target = [1, 1, 1, 1, 1], 3
s = sum(nums); need = (s + target) // 2
dp = [1] + [0] * need
print('S =', s, ' need P =', need, ' columns w = 0..%d' % need)
print('start   ', dp)
for x in nums:
    for w in range(need, x - 1, -1):
        dp[w] += dp[w - x]
    print('item %d  ' % x, dp)
print('dp[4] =', dp[need], '= C(5,4) ways to pick which four numbers get a plus')

# zero check on [0,0,1], target 1: S=1, need=1
dp = [1, 0]
print('[0,0,1] target 1: need = 1')
print('start   ', dp)
for x in [0, 0, 1]:
    for w in range(1, x - 1, -1):
        dp[w] += dp[w - x]
    print('item %d  ' % x, dp)

# immediate zeros
print('|target| > S  ->', target_sum([1, 2], 4), ';  S + target odd ->', target_sum([1, 2], 2), ' (S=3, 5 is odd)')

# claim: every zero doubles the count (exhaustive)
count = 0
for n in range(1, 7):
    for nums in itertools.product(range(0, 4), repeat=n):
        nums = list(nums)
        for target in range(-sum(nums) - 1, sum(nums) + 2):
            got = target_sum(nums, target)
            assert got == brute(nums, target), (nums, target)
            nz = [x for x in nums if x]
            z = n - len(nz)
            if nz:
                assert got == 2 ** z * target_sum(nz, target)
            count += 1
print('exhaustive (all lists len<=6, values 0..3, every target in range):', count, 'checks; each zero doubles the count, and the DP matches the 2^n enumeration')

# seeded random cross-check, len <= 12
for _ in range(500):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 12))]
    target = random.randint(-sum(nums) - 2, sum(nums) + 2)
    b = brute(nums, target)
    assert target_sum(nums, target) == target_sum_memo(nums, target) == target_sum_dict(nums, target) == b, (nums, target)
print('500 random cases agree (reduction = memo = signed-total dict = enumeration)')

# edge cases / max size
assert target_sum([0], 0) == 2 and target_sum([0] * 20, 0) == 2**20 and target_sum([0] * 20, 1) == 0
assert target_sum([50] * 20, 0) == target_sum_dict([50] * 20, 0) == 184756
assert target_sum([1000], -1000) == 1 and target_sum([1000], 0) == 0
print('edge cases ok: twenty zeros -> 2^20 =', target_sum([0] * 20, 0), '; twenty 50s, target 0 ->', target_sum([50] * 20, 0))
