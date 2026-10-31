import collections
import random

random.seed(1215)

def dup_missing(nums):
    n = len(nums)
    x = 0
    for i, v in enumerate(nums, 1):          # x = dup ^ missing: every value that is both present and in 1..n cancels
        x ^= i ^ v
    low = x & -x                              # a bit where dup and missing differ (x != 0 because dup != missing)
    a = b = 0
    for i, v in enumerate(nums, 1):
        if i & low: a ^= i
        else: b ^= i
        if v & low: a ^= v
        else: b ^= v
    # a and b are {dup, missing} in some order; one more O(n) pass tells which is which
    return [a, b] if nums.count(a) == 2 else [b, a]

def brute(nums):
    c = collections.Counter(nums)
    return [[k for k, v in c.items() if v == 2][0], [i for i in range(1, len(nums) + 1) if i not in c][0]]

for nums, want in [([1, 3, 3, 4], [3, 2]), ([2, 2], [2, 1]), ([1, 1, 3, 4, 5], [1, 2]), ([3, 1, 2, 5, 5], [5, 4])]:
    assert dup_missing(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# dry run [1, 3, 3, 4]
nums = [1, 3, 3, 4]
x = 0
for i, v in enumerate(nums, 1): x ^= i ^ v
low = x & -x
print("dry run [1,3,3,4]: x = dup ^ missing =", x, bin(x), "| low bit =", low)
print("  group with bit set   : numbers", [v for v in nums if v & low], "indices", [i for i in range(1, 5) if i & low])
print("  group with bit clear : numbers", [v for v in nums if not v & low], "indices", [i for i in range(1, 5) if not i & low])
print("  results:", dup_missing(nums), "(duplicate, missing)")

for _ in range(500):
    n = random.randint(2, 12)
    dup, miss = random.sample(range(1, n + 1), 2)
    nums = [v for v in range(1, n + 1) if v != miss] + [dup]
    random.shuffle(nums)
    assert dup_missing(nums) == brute(nums) == [dup, miss], nums
print("500 seeded random cases agree with Counter + membership scan")
# every possible (dup, missing) pair for n = 2..7, exhaustively
for n in range(2, 8):
    for dup in range(1, n + 1):
        for miss in range(1, n + 1):
            if dup == miss: continue
            nums = [v for v in range(1, n + 1) if v != miss] + [dup]
            assert dup_missing(nums) == [dup, miss]
print("exhaustive: every (duplicate, missing) pair for n = 2..7 correct")

# XOR swap
a, b = 5, 9
a ^= b; b ^= a; a ^= b
assert (a, b) == (9, 5)
lst = [4, 7]
i = j = 0                                     # both names point at the same slot
lst[i] ^= lst[j]; lst[j] ^= lst[i]; lst[i] ^= lst[j]
print("XOR swap on 5, 9 ->", (a, b), "| same slot [4, 7] with i == j ->", lst, "(slot zeroed, value lost)")
assert lst == [0, 7]
# edge asserts
assert dup_missing([2, 2]) == [2, 1]
assert dup_missing([1, 1]) == [1, 2]
assert dup_missing([2, 3, 3]) == [3, 1]
n = 10 ** 5
big = list(range(1, n + 1)); big[-1] = 1                  # drop n, duplicate 1
assert dup_missing(big) == [1, n]
print("edge asserts ok (including n = 10^5)")
