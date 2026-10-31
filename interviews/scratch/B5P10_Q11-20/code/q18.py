import random
from functools import lru_cache

random.seed(18)

def subset_sum(nums, target):
    """Boolean 1D table, capacity DOWNWARD. O(n * target) time, O(target) space."""
    dp = [True] + [False] * target                  # dp[t]: some subset of the items so far sums to exactly t
    for x in nums:
        for t in range(target, x - 1, -1):
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def subset_sum_bits(nums, target):
    """Big-int bitset: bit t set means sum t reachable. Mask to target+1 bits so the int never grows past the target."""
    mask = (1 << (target + 1)) - 1
    bits = 1
    for x in nums:
        bits |= (bits << x) & mask
    return bool(bits >> target & 1)

def subset_sum_memo(nums, target):
    """Top-down over (i, remaining). Depth <= len(nums) + 1, safe under the default limit."""
    @lru_cache(maxsize=None)
    def go(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return go(i + 1, rem - nums[i]) or go(i + 1, rem)
    return go(0, target)

def brute(nums, target):
    n = len(nums)
    return any(sum(nums[i] for i in range(n) if m >> i & 1) == target for m in range(1 << n))

for (nums, t), want in [(([3, 34, 4, 12, 5, 2], 9), True), (([3, 34, 4, 12, 5, 2], 30), False), (([7], 0), True), (([5, 5], 5), True)]:
    assert subset_sum(nums, t) is want and subset_sum_bits(nums, t) is want and subset_sum_memo(nums, t) is want and brute(nums, t) is want
print('4 prompt examples ok')

# walk-through: nums=[3,34,4,12,5,2], target=9; items bigger than the target do nothing (34, 12)
nums, target = [3, 34, 4, 12, 5, 2], 9
dp = [True] + [False] * target
print('columns t = 0..9')
print('start   ', ''.join('T' if x else '.' for x in dp))
for x in nums:
    for t in range(target, x - 1, -1):
        if dp[t - x]:
            dp[t] = True
    print('item %-3d' % x, ''.join('T' if y else '.' for y in dp))
print('dp[9] =', dp[9], '(4 + 5, or 4 + 3 + 2)')

bits = 1
mask = (1 << 10) - 1
print('bitset after each item (bit 0 on the right, masked to 10 bits):')
for x in nums:
    bits |= (bits << x) & mask
    print('  item %-3d %s' % (x, format(bits, '010b')))

# seeded cross-check: table vs bitset vs memo vs enumeration (len <= 12)
t_true = 0
for _ in range(600):
    nums = [random.randint(1, 15) for _ in range(random.randint(1, 12))]
    target = random.randint(0, sum(nums) + 3)
    b = brute(nums, target)
    assert subset_sum(nums, target) == subset_sum_bits(nums, target) == subset_sum_memo(nums, target) == b, (nums, target)
    t_true += b
print('600 random cases agree (table = bitset = memo = enumeration); True in', t_true)

# edge cases and max size, table against bitset
assert subset_sum([7], 0) and not subset_sum([7], 3) and subset_sum([1] * 200, 200) and not subset_sum([2] * 200, 399)
for _ in range(5):
    nums = [random.randint(1, 500) for _ in range(200)]
    target = random.randint(0, 10**4)
    assert subset_sum(nums, target) == subset_sum_bits(nums, target) == subset_sum_memo(nums, target)
print('edge cases ok; five max-size random inputs: table = bitset = memo')
print('table cell updates at max size (n=200, target=10^4): at most', 200 * 10**4, '; bitset: 200 shift-or operations on a', 10**4 + 1, 'bit integer (about', (10**4 + 1 + 63) // 64, '64-bit words each)')
