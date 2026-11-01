import itertools
import random

random.seed(1213)
BITS = 31

def hamming_pair(x, y):
    return bin(x ^ y).count('1')

def hamming_total(nums):
    n, total = len(nums), 0
    for b in range(BITS):
        ones = sum((v >> b) & 1 for v in nums)
        total += ones * (n - ones)                # pairs that differ at bit b: one with 1, one with 0
    return total

def solve(x, y, nums):
    return [hamming_pair(x, y), hamming_total(nums)]

def brute(x, y, nums):
    h = lambda a, b: sum(1 for i in range(BITS) if ((a >> i) & 1) != ((b >> i) & 1))
    return [h(x, y), sum(h(a, b) for a, b in itertools.combinations(nums, 2))]

for (x, y, nums), want in [((1, 4, [5, 9, 12, 3]), [2, 14]), ((0, 0, [7, 7]), [0, 0]),
                           ((2147483647, 0, [0, 2147483647]), [31, 31]), ((6, 5, [1, 2, 4]), [2, 6])]:
    assert solve(x, y, nums) == brute(x, y, nums) == want, (x, y, nums)
print("4 prompt examples ok")

print("dry run nums = [5, 9, 12, 3]:")
nums = [5, 9, 12, 3]
tot = 0
for b in range(4):
    ones = sum((v >> b) & 1 for v in nums)
    tot += ones * (len(nums) - ones)
    print("  bit %d: set in %s -> ones=%d zeros=%d pairs=%d" % (b, [v for v in nums if v >> b & 1], ones, len(nums) - ones, ones * (len(nums) - ones)))
print("  total", tot, "| popcount(1 ^ 4) = popcount(%s) = %d" % (bin(1 ^ 4), hamming_pair(1, 4)))

for _ in range(500):
    nums = [random.randint(0, 2 ** random.randint(1, 31) - 1) for _ in range(random.randint(2, 8))]
    x, y = random.randint(0, 2 ** 31 - 1), random.randint(0, 2 ** 31 - 1)
    assert solve(x, y, nums) == brute(x, y, nums), (x, y, nums)
print("500 seeded random cases agree with the pairwise bit-by-bit brute force")

# edge / size asserts
assert hamming_total([7, 7, 7]) == 0
assert hamming_total([0, 2 ** 31 - 1]) == 31
assert hamming_total([0] * 5000 + [2 ** 31 - 1] * 5000) == 31 * 5000 * 5000      # n = 10^4, max total
assert solve(0, 0, [0, 0]) == [0, 0]
print("max case n=10^4 total:", hamming_total([0] * 5000 + [2 ** 31 - 1] * 5000), "| fits easily: Python ints do not overflow")
print("edge asserts ok")
