import collections
import functools
import random

random.seed(1216)

def single_number_iii(nums):
    x = 0
    for v in nums:
        x ^= v                                # x = a ^ b: all pairs cancel
    low = x & -x                              # lowest set bit of x; x != 0 because a != b
    a = 0
    for v in nums:
        if v & low:                           # group 1: numbers with that bit set (a pair always lands in one group together)
            a ^= v
    return sorted([a, x ^ a])

def brute(nums):
    return sorted(k for k, v in collections.Counter(nums).items() if v == 1)

for nums, want in [([4, 9, 4, -6, 2, 9], [-6, 2]), ([1, 2], [1, 2]), ([-1, 1, 3, 3], [-1, 1]), ([0, 5, 0, 7, 7, -2], [-2, 5])]:
    assert single_number_iii(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# dry run [4, 9, 4, -6, 2, 9]
nums = [4, 9, 4, -6, 2, 9]
x = 0
for v in nums: x ^= v
low = x & -x
print("dry run:", nums)
print("  x = a ^ b =", x, "(-6 ^ 2) | low = x & -x =", low, bin(low))
print("  numbers with that bit set  :", [v for v in nums if v & low], "-> XOR =", functools.reduce(lambda p, q: p ^ q, [v for v in nums if v & low]))
print("  numbers with that bit clear:", [v for v in nums if not v & low], "-> XOR =", functools.reduce(lambda p, q: p ^ q, [v for v in nums if not v & low]))
print("  answer:", single_number_iii(nums))

# Python 3.13 behaviour with negatives, as observed
print("--- negatives in Python 3.13 (observed) ---")
for v in (12, -12, -2, -1, -8):
    print("x = %3d  -x = %3d  x & -x = %2d  ~x + 1 = %3d  bin(x & -x) = %s" % (v, -v, v & -v, ~v + 1, bin(v & -v)))
print("-6 ^ 2 =", -6 ^ 2, "(a negative XOR: the two singles have different signs, so the sign 'bit' differs)")
print("-1 ^ 1 =", -1 ^ 1, "| (-1 ^ 1) & -(-1 ^ 1) =", (-1 ^ 1) & -(-1 ^ 1))
for v in range(-2000, 2001):
    if v:
        low = v & -v
        assert low > 0 and low & (low - 1) == 0 and v & (low - 1) == 0 and v & low        # power of two, and the lowest set bit of v
print("x & -x is the lowest set bit (a positive power of two) for every nonzero x in [-2000, 2000]")

# seeded random cross-check, values of both signs up to 2^31
for _ in range(500):
    k = random.randint(2, 7)
    vals = random.sample(range(-2 ** 31 + 1, 2 ** 31), k)
    singles, pairs = vals[:2], vals[2:]
    nums = singles + [p for p in pairs for _ in range(2)]
    random.shuffle(nums)
    assert single_number_iii(nums) == brute(nums) == sorted(singles), nums
print("500 seeded random cases (values of both signs) agree with Counter")
# exhaustive: every pair of distinct singles in -4..4 with one extra pair value
for a in range(-4, 5):
    for b in range(-4, 5):
        if a >= b: continue
        for p in range(-4, 5):
            if p in (a, b): continue
            assert single_number_iii([p, a, p, b]) == [a, b]
print("exhaustive small values ok")
# edge asserts
assert single_number_iii([0, 1]) == [0, 1]
assert single_number_iii([-2 ** 31 + 1, 2 ** 31 - 1]) == [-2 ** 31 + 1, 2 ** 31 - 1]
big = [1, 2] + [v for v in range(3, 50003) for _ in range(2)]
assert single_number_iii(big) == [1, 2]
print("edge asserts ok (including 10^5 numbers)")
