import random, ctypes

I32_MIN, I32_MAX = -2**31, 2**31 - 1

def to_int32(v):                                         # two's-complement wrap, as a machine would hold it
    return ((v + 2**31) % 2**32) - 2**31

def optimal(x):
    sign = -1 if x < 0 else 1
    v, r = abs(x), 0
    while v:
        r = r * 10 + v % 10                              # in C this line needs a pre-check against INT_MAX // 10
        v //= 10
    r *= sign
    return [r if I32_MIN <= r <= I32_MAX else 0, to_int32(r)]

def brute(x):                                            # string reversal + ctypes wraparound
    s = str(x)
    r = int('-' + s[:0:-1]) if x < 0 else int(s[::-1])
    w = ctypes.c_int32(r).value
    return [r if w == r else 0, w]

for x, want in [(123, [321, 321]), (-120, [-21, -21]), (1534236469, [0, 1056389759]),
                (-2147483648, [0, 126087180]), (0, [0, 0]), (1463847412, [2147483641, 2147483641])]:
    got = optimal(x)
    assert got == want == brute(x)
    print('x =', x, '->', got)

random.seed(10)
pool = [0, I32_MIN, I32_MAX, -I32_MAX, 10**9, 10**9 - 1, 2**31 - 10, 1000000003, 2000000003, 1147483647]
for _ in range(20000):
    pool.append(random.choice([random.randint(I32_MIN, I32_MAX), random.randint(-999, 999),
                               random.randint(10**9, I32_MAX), -random.randint(10**9, 2**31)]))
for x in pool:
    assert optimal(x) == brute(x)
print('random cross-check ok:', len(pool), 'inputs incl. boundaries')

# claim: a 9-digit (or shorter) input can never leave the range: its reversal has at most 9 digits < 10**9 < 2**31
assert 10**9 - 1 < I32_MAX
for x in range(-10**6, 10**6):                           # exhaustive on the small side
    assert optimal(x)[0] == int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)
for x in [random.randint(-10**9 + 1, 10**9 - 1) for _ in range(50000)]:
    assert optimal(x)[0] == optimal(x)[1] and (optimal(x)[0] != 0 or x == 0)
# 10-digit inputs: some overflow, some do not
ten = [random.randint(10**9, I32_MAX) for _ in range(50000)]
bad = sum(optimal(x)[0] == 0 for x in ten)
print('10-digit sample: overflow in', bad, 'of', len(ten))
# reversed last digit >= 3 always overflows for a positive 10-digit input; last digit 0 or 1 never does
assert all((optimal(x)[0] == 0) for x in ten if x % 10 >= 3)
assert all((optimal(x)[0] != 0) for x in ten if x % 10 <= 1)
print('10-digit rule on the sample: last digit >= 3 always overflows, last digit 0 or 1 never does')
# the pre-check a C solution uses, translated: before r = r*10 + d, need r <= INT_MAX // 10 (with the last digit rule)
def checked(x):
    sign, v, r = (-1 if x < 0 else 1), abs(x), 0
    while v:
        d = v % 10
        if r > I32_MAX // 10 or (r == I32_MAX // 10 and d > 7 + (sign < 0)):
            return 0
        r = r * 10 + d; v //= 10
    return sign * r
assert all(checked(x) == optimal(x)[0] for x in pool)
print('pre-check form (r > INT_MAX // 10 test) agrees on all', len(pool), 'inputs')
