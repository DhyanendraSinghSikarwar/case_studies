import random
from functools import lru_cache

random.seed(11)

def can_partition(nums):
    """Optimal: boolean 1D table, capacity looped DOWNWARD. O(n * total/2) time, O(total/2) space."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target            # dp[t]: some subset of the items seen so far sums to t
    for x in nums:
        for t in range(target, x - 1, -1):     # downward: dp[t - x] is still the value from BEFORE this item
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def can_partition_bits(nums):
    """Bitset: bit t of `bits` is set when sum t is reachable. One shift-or per item."""
    total = sum(nums)
    if total % 2:
        return False
    bits = 1
    for x in nums:
        bits |= bits << x
    return bool(bits >> (total // 2) & 1)

def can_partition_memo(nums):
    """Top-down: depth is len(nums) (<= 200 here), so the default recursion limit is fine for this one."""
    total = sum(nums)
    if total % 2:
        return False
    @lru_cache(maxsize=None)
    def go(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return go(i + 1, rem - nums[i]) or go(i + 1, rem)
    return go(0, total // 2)

def can_partition_upward_bug(nums):
    """Same table, capacity loop UPWARD: an item can be reused, so it answers a different question."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for t in range(x, target + 1):
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def brute(nums):
    """Oracle: enumerate every subset, test 2 * sum == total."""
    n, total = len(nums), sum(nums)
    return any(2 * sum(nums[i] for i in range(n) if m >> i & 1) == total for m in range(1 << n))

# prompt examples
for nums, want in [([1, 5, 11, 5], True), ([1, 2, 3, 5], False), ([2], False), ([3, 3], True)]:
    assert can_partition(nums) is want and can_partition_bits(nums) is want and can_partition_memo(nums) is want and brute(nums) is want
print('4 prompt examples ok')

# table walk-through on the first example: total 22, target 11
nums = [1, 5, 11, 5]
target = sum(nums) // 2
dp = [True] + [False] * target
print('target =', target, '  columns t = 0..%d' % target)
print('start    ', ''.join('T' if v else '.' for v in dp))
for x in nums:
    for t in range(target, x - 1, -1):
        if dp[t - x]:
            dp[t] = True
    print('item %-4d' % x, ''.join('T' if v else '.' for v in dp))
bits = 1
for x in [1, 5, 11, 5]:
    bits |= bits << x
    print('bitset after item %-3d (bit 0 on the right): %s' % (x, bin(bits)[2:]))

# why DOWNWARD: [1, 5] has total 6, target 3, and no subset sums to 3
print('nums=[1, 5]: correct', can_partition([1, 5]), ' upward-loop', can_partition_upward_bug([1, 5]), ' (the upward loop used the 1 three times)')

# seeded cross-check against subset enumeration (len <= 12)
trues = 0
wrong_upward = 0
for _ in range(600):
    nums = [random.randint(1, 12) for _ in range(random.randint(1, 12))]
    b = brute(nums)
    assert can_partition(nums) == b == can_partition_bits(nums) == can_partition_memo(nums), nums
    trues += b
    wrong_upward += can_partition_upward_bug(nums) != b
print('600 random cases agree (table = bitset = memo = enumeration); True in', trues, 'of them; upward-loop bug wrong in', wrong_upward)

# edge cases
assert can_partition([1]) is False and can_partition([1, 1]) is True and can_partition([100] * 200) is True
assert can_partition([100] * 199 + [99]) is False          # odd total
assert can_partition_bits([100] * 200) is True
big = [random.randint(1, 100) for _ in range(200)]
assert can_partition(big) == can_partition_bits(big) == can_partition_memo(big)
print('edge cases ok; max-size random input ->', can_partition(big))
