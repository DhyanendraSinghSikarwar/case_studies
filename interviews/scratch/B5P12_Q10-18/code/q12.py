import random

random.seed(1212)

def power_two_four(n):
    p2 = n > 0 and n & (n - 1) == 0          # '&' binds tighter than '==' in Python, so no extra brackets needed
    p4 = p2 and (n & 0x55555555) != 0
    return [p2, p4]

def power_by_division(n):
    """Loop version, O(log n): keep halving (quartering) while the remainder is zero."""
    def pw(n, base):
        if n <= 0: return False
        while n % base == 0: n //= base
        return n == 1
    return [pw(n, 2), pw(n, 4)]

POW2 = {2 ** k for k in range(31)}
POW4 = {4 ** k for k in range(16)}
def brute(n): return [n in POW2, n in POW4]

for n, want in [(16, [True, True]), (8, [True, False]), (0, [False, False]), (-4, [False, False]), (1, [True, True]),
                (1073741824, [True, True])]:
    assert power_two_four(n) == power_by_division(n) == brute(n) == want, n
print("6 prompt examples ok")

print("dry run n=16:  bin", bin(16), " n-1 =", bin(15), " n & (n-1) =", 16 & 15, " n & 0x55555555 =", hex(16 & 0x55555555))
print("dry run n=8 :  bin", bin(8), " n & (n-1) =", 8 & 7, " n & 0x55555555 =", 8 & 0x55555555)

# the mask: 4^k for k = 0..15 are exactly the powers of two in 1..2^30 at an even bit position
assert {4 ** k for k in range(16)} == {1 << i for i in range(0, 31, 2)}
print("mask 0x55555555 = %s ; its set bits are the even positions 0..30: %s" % (bin(0x55555555), [i for i in range(32) if 0x55555555 >> i & 1] == list(range(0, 32, 2))))

# exhaustive check over a wide window and over every power of two and its neighbours in range
window = list(range(-70000, 70001))
special = [s * (2 ** k + d) for k in range(31) for d in (-1, 0, 1) for s in (1, -1)] + [-2 ** 31, 2 ** 31 - 1]
for n in window + special:
    assert power_two_four(n) == power_by_division(n) == brute(n), n
print("exhaustive: %d values in [-70000, 70000] plus %d special values agree" % (len(window), len(special)))

# seeded random over the full 32-bit signed range
for _ in range(3000):
    n = random.randint(-2 ** 31, 2 ** 31 - 1)
    assert power_two_four(n) == brute(n)
print("3000 seeded random values over the full range agree with the explicit sets")

# why each part of the test is there
no_guard = [n for n in range(-1000, 1001) if (n & (n - 1) == 0) != (n in POW2)]
print("without 'n > 0', n & (n-1) == 0 is wrong for exactly:", no_guard)
mask_only = [n for n in range(1, 200) if bool(n & 0x55555555) != (n in POW4)]
print("mask alone (no power-of-two test) wrongly accepts, e.g.:", mask_only[:6], "-> you need BOTH tests")
print("outside the stated range: 4**16 =", 4 ** 16, "has the single bit at position 32; n & 0x55555555 =", (4 ** 16) & 0x55555555, "-> would report False")
# alternative for the second test that needs no mask and works for any size: a power of two 2^k has bit_length k+1
assert all(power_two_four(2 ** k)[1] == (k % 2 == 0) == ((2 ** k).bit_length() % 2 == 1) for k in range(0, 31))
assert all(((1 << k).bit_length() % 2 == 1) == (k % 2 == 0) for k in range(0, 200))
print("bit_length alternative: 2^k is a power of 4 exactly when its bit_length is odd (checked k = 0..199)")
assert all(((n - 1) % 3 == 0) == (n in POW4) for n in sorted(POW2))
assert all((1 << (n - 1).bit_length()) >= n and (1 << (n - 1).bit_length()) // 2 < n for n in range(1, 5000))
print("follow-up claims ok: (n-1) % 3 == 0 separates 4^k from 2*4^k; 1 << (n-1).bit_length() is the next power of two >= n")
edge = [(2 ** 31 - 1, [False, False]), (-2 ** 31, [False, False]), (2 ** 30, [True, True]), (2 ** 29, [True, False])]
for n, want in edge: assert power_two_four(n) == want
print("edge asserts ok")
