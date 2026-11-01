import random
from collections import Counter

random.seed(2801)


def single_count_bits(nums):
    """For each of 32 bit positions count the set bits, mod 3, rebuild, then fix the sign."""
    ans = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3:   # v >> b works for negatives: sign bits are copied in
            ans |= 1 << b
    return ans - (1 << 32) if ans & (1 << 31) else ans   # bit 31 set -> negative in 32-bit two's complement


def no_sign_fix(nums):
    ans = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3:
            ans |= 1 << b
    return ans


def single_ones_twos(nums):
    """Two registers: ones = bits seen 1 mod 3 times, twos = bits seen 2 mod 3 times."""
    ones = twos = 0
    for x in nums:
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
    return ones          # Python ints sign-extend forever, so a negative answer is already negative


def brute(nums):
    return next(k for k, c in Counter(nums).items() if c == 1)


# dry run table for the first example
ex = [-5, 7, -5, 7, -5, 7, 9]
print("bit : count of set bits, count mod 3")
for b in (0, 1, 2, 3, 4, 31):
    c = sum((v >> b) & 1 for v in ex)
    print(f"{b:>3} : {c}, {c % 3}")

# the four prompt examples
for nums, want in [([-5, 7, -5, 7, -5, 7, 9], 9), ([-8, 3, 3, 3], -8), ([4], 4), ([1, 1, 1, -2147483648], -2147483648)]:
    got = single_count_bits(nums)
    assert got == single_ones_twos(nums) == brute(nums) == want, (nums, got)
    print(nums, "->", got)

# the sign fix, shown
raw = no_sign_fix([-8, 3, 3, 3])
print("without the fix:", raw, "= 2^32 - 8 =", 2**32 - 8, "| with the fix:", single_count_bits([-8, 3, 3, 3]))
print("bit 31 of the raw result:", (raw >> 31) & 1, "| 0xFFFFFFF8 as binary:", format(raw, "032b"))

# seeded random cross-check against Counter
done = 0
while done < 500:
    k = random.randint(0, 6)
    triples = random.sample(range(-20, 20), k) if random.random() < 0.7 else random.sample([-2**31, 2**31 - 1, -1, 0, 1, 2**30], min(k, 6))
    single = random.choice([v for v in range(-2**31, -2**31 + 3)] + [2**31 - 1, 0, -1, 5, -7])
    if single in triples:
        continue
    nums = [single] + [t for t in triples for _ in range(3)]
    random.shuffle(nums)
    assert single_count_bits(nums) == single_ones_twos(nums) == brute(nums) == single, nums
    done += 1
print("500 seeded random cases ok (extremes -2^31 and 2^31-1 included)")

# edge asserts
assert single_count_bits([2**31 - 1]) == 2**31 - 1
assert single_count_bits([-1, 0, 0, 0]) == -1
assert single_count_bits([-2**31, 5, 5, 5]) == -2**31
assert single_ones_twos([-2**31, 5, 5, 5]) == -2**31
print("edge asserts ok")
