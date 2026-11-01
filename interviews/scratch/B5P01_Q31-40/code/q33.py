import math
import random
from collections import defaultdict


def brute(nums, k):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i, n) if sum(nums[i:j + 1]) % k == 0)


def sub_div_k(nums, k):
    """Two equal prefix remainders mean the slice between them sums to a multiple of k."""
    seen = defaultdict(int)
    seen[0] = 1            # empty prefix
    pref = 0
    ans = 0
    for x in nums:
        pref = (pref + x) % k      # Python: result is in [0, k) even if pref+x < 0
        ans += seen[pref]
        seen[pref] += 1
    return ans


ex = [4, 5, 0, -2, -3, 1]
print(ex, "k=5 ->", sub_div_k(ex, 5))
assert sub_div_k(ex, 5) == 7

# Negative modulo: Python vs a C-style remainder (math.fmod truncates toward zero)
print("Python  -7 % 5 =", -7 % 5, "| C-style fmod(-7,5) =", int(math.fmod(-7, 5)))


def sub_div_k_c_style(nums, k):
    seen = defaultdict(int)
    seen[0] = 1
    pref = ans = 0
    for x in nums:
        pref = int(math.fmod(pref + x, k))     # may be negative: -2 and 3 are the same class but different keys
        ans += seen[pref]
        seen[pref] += 1
    return ans

bad = sub_div_k_c_style(ex, 5)
print("C-style remainders without the (r + k) % k fix ->", bad, "(wrong, expected 7)")
assert bad != 7

# Edge cases
assert sub_div_k([], 3) == 0
assert sub_div_k([5], 5) == 1
assert sub_div_k([3], 5) == 0
assert sub_div_k([-5], 5) == 1
assert sub_div_k([0, 0, 0], 7) == 6
assert sub_div_k([1, 2, 3], 1) == 6          # k=1: every non-empty subarray
assert sub_div_k([-1, -1, -1], 3) == 1
assert sub_div_k([7, -7], 7) == 3

rng = random.Random(33)
for _ in range(1500):
    nums = [rng.randint(-9, 9) for _ in range(rng.randint(0, 14))]
    k = rng.randint(1, 8)
    assert sub_div_k(nums, k) == brute(nums, k), (nums, k)
print("cross-check passed: 1500 random lists with negatives")
