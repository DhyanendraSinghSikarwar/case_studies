import random
from functools import reduce
from collections import defaultdict


def brute(nums, k):
    n = len(nums)
    cnt = 0
    for i in range(n):
        x = 0
        for j in range(i, n):
            x ^= nums[j]
            cnt += (x == k)
    return cnt


def sub_xor_k(nums, k):
    """prefix[j] ^ prefix[i] == k  <=>  prefix[i] == prefix[j] ^ k (XOR is its own inverse)."""
    seen = defaultdict(int)
    seen[0] = 1
    pref = ans = 0
    for x in nums:
        pref ^= x
        ans += seen[pref ^ k]
        seen[pref] += 1
    return ans


ex = [4, 2, 2, 6, 4]
print(ex, "k=6 ->", sub_xor_k(ex, 6))
assert sub_xor_k(ex, 6) == 4

# The four subarrays, by brute force
subs = [ex[i:j + 1] for i in range(len(ex)) for j in range(i, len(ex))
        if reduce(lambda a, b: a ^ b, ex[i:j + 1]) == 6]
print("subarrays with XOR 6:", subs)
assert len(subs) == 4

# Edge cases
assert sub_xor_k([], 0) == 0
assert sub_xor_k([0], 0) == 1
assert sub_xor_k([5], 5) == 1
assert sub_xor_k([5], 4) == 0
assert sub_xor_k([3, 3], 0) == 1          # k = 0 counts pairs of equal prefixes
assert sub_xor_k([0, 0, 0], 0) == 6
assert sub_xor_k([1, 2, 3], 0) == 1       # 1^2^3 == 0
assert sub_xor_k([7] * 5, 7) == 9         # odd-length subarrays of five 7s: 5+3+1
assert sub_xor_k([10**9, 10**9, 5], 5) == 2

rng = random.Random(36)
for _ in range(1500):
    nums = [rng.randint(0, 15) for _ in range(rng.randint(0, 14))]
    k = rng.randint(0, 15)
    assert sub_xor_k(nums, k) == brute(nums, k), (nums, k)
print("cross-check passed: 1500 random lists")
