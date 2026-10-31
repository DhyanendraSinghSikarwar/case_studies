import random

random.seed(1217)
M32 = 0xFFFFFFFF

def reverse_loop(n):
    n &= M32                                  # read the 32-bit two's-complement pattern; makes n non-negative
    r = 0
    for _ in range(32):
        r = (r << 1) | (n & 1)                # append the lowest bit of n to r
        n >>= 1
    return r

def reverse_dc(n):
    n &= M32
    n = ((n >> 16) | (n << 16)) & M32                                   # swap 16-bit halves (mask: << 16 grows past 32 bits)
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)               # swap bytes in each half
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)               # swap nibbles
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)               # swap bit pairs
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)               # swap adjacent bits
    return n

def brute(n):
    return int(format(n & M32, '032b')[::-1], 2)

for n, want in [(1, 2147483648), (6, 1610612736), (-1, 4294967295), (-2147483648, 1), (0, 0), (4294967295, 4294967295)]:
    assert reverse_loop(n) == reverse_dc(n) == brute(n) == want, n
print("6 prompt examples ok")

print("dry run n=6 as 32 bits:", format(6, '032b'))
print("  reversed             :", format(reverse_loop(6), '032b'), "=", reverse_loop(6))
print("divide-and-conquer on n=6, value after each of the five steps (32-bit hex):")
n = 6 & M32
steps = []
n = ((n >> 16) | (n << 16)) & M32; steps.append(n)
n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8); steps.append(n)
n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4); steps.append(n)
n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2); steps.append(n)
n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1); steps.append(n)
print("  ", ["%08x" % s for s in steps], "-> final", n)
assert n == 1610612736

# Python 3.13 behaviour without the mask (observed)
print("--- why the mask (Python 3.13, observed) ---")
print("-1 >> 1 =", -1 >> 1, "| -1 >> 100 =", -1 >> 100, "| -2147483648 >> 40 =", -2147483648 >> 40)
def reverse_no_mask_while(n, cap=40):
    steps = 0
    while n and steps < cap:                  # 'while n:' style loop on a negative n; capped so this demo stops
        n >>= 1; steps += 1
    return steps
print("loop 'while n: n >>= 1' on n=-1 stopped only because of the cap of 40 steps; after the cap n is still", end=' ')
m = -1
for _ in range(40): m >>= 1
print(m)
print("without the mask, -1 << 16 =", -1 << 16, "(no 32-bit wrap) ; with the mask, (-1 << 16) & 0xFFFFFFFF =", (-1 << 16) & M32)
print("-1 & 0xFFFFFFFF =", -1 & M32, "| -2147483648 & 0xFFFFFFFF =", -2147483648 & M32)

for n in range(-3000, 0):
    m = n
    for _ in range(64): m >>= 1
    assert m == -1                              # every negative n ends at -1, never at 0
print("every negative n in [-3000, -1] is -1 after 64 shifts: a 'while n' loop would never end")
def reverse_loop_nomask(n):
    r = 0
    for _ in range(32):
        r = (r << 1) | (n & 1); n >>= 1
    return r
assert all(reverse_loop_nomask(n) == brute(n) for n in range(-5000, 5000))
print("a fixed 32-round loop with no mask also gives the right answer on [-5000, 5000] (n & 1 and >> are arithmetic); the mask makes it explicit")
# seeded random + exhaustive-style checks
for _ in range(2000):
    n = random.choice([random.randint(-2 ** 31, 2 ** 32 - 1), random.randint(-8, 8), 1 << random.randint(0, 31)])
    assert reverse_loop(n) == reverse_dc(n) == brute(n), n
print("2000 seeded random values agree with the string-reversal oracle")
for n in range(-3000, 3001):
    assert reverse_loop(n) == reverse_dc(n) == brute(n)
for n in range(0, 2 ** 32, 2 ** 32 // 1000 + 1):
    assert reverse_loop(n) == reverse_dc(n) == brute(n)
print("exhaustive window [-3000, 3000] and a 1000-point sweep of 0..2^32 agree")
# involution and range
for _ in range(500):
    n = random.randint(0, M32)
    assert reverse_loop(reverse_loop(n)) == n and 0 <= reverse_loop(n) <= M32
print("reversing twice gives the original pattern (500 random), result always in 0..2^32-1")
# edge asserts
assert reverse_loop(2 ** 31) == 1 and reverse_loop(0) == 0 and reverse_dc(-1) == M32
assert reverse_loop(-2 ** 31) == 1
print("edge asserts ok")
