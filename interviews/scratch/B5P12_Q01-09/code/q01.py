import random
from collections import Counter

random.seed(1201)

def single_xor(nums):
    x = 0
    for v in nums:
        x ^= v          # a ^ a = 0, 0 ^ b = b; order does not matter
    return x

def single_counter(nums):          # brute force: O(n) extra space
    return next(k for k, c in Counter(nums).items() if c == 1)

def single_set(nums):              # another O(n)-space version: toggle membership
    seen = set()
    for v in nums:
        seen.symmetric_difference_update({v})
    return next(iter(seen))

examples = [([6, 3, 9, 3, 6], 9), ([7], 7), ([-3, -3, 5], 5), ([0, 1, 0], 1), ([-8, 2, 2, -8, -1], -1)]
for nums, want in examples:
    got = single_xor(nums)
    assert got == want == single_counter(nums) == single_set(nums)
    print(nums, '->', got)

# dry run trace of the first example
x = 0
for v in [6, 3, 9, 3, 6]:
    x ^= v
    print(f'  x ^= {v:>2} -> {x:>2}  ({x:04b})')

# seeded cross-check: 3000 random inputs, negatives included, big magnitudes included
for _ in range(3000):
    pairs = random.sample(range(-50, 50), random.randint(0, 6))
    odd = random.choice([v for v in range(-60, 60) if v not in pairs] + [10**12, -10**12])
    nums = [odd] + pairs * 2
    random.shuffle(nums)
    assert single_xor(nums) == single_counter(nums) == odd
print('random cross-check ok: 3000 cases')

# Python specifics: no mask needed, negatives XOR like infinite two's complement
assert -3 ^ -3 == 0 and -3 ^ 0 == -3 and (-8 ^ 2) ^ 2 == -8
assert single_xor([-(2**70), 5, 5]) == -(2**70)
print('-8 ^ 2 =', -8 ^ 2, ' (-8 ^ 2) ^ 2 =', (-8 ^ 2) ^ 2)
print('big:', single_xor([2**100, 7, 2**100, 7, -(2**90)]) == -(2**90))
print('edge asserts ok')
