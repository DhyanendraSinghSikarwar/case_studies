import sys, math, random, time
random.seed(45)
MOD = 10**9 + 7

# ---- fast doubling: returns (F(n), F(n+1)); depth = bit length of n (about 17 for 10^5)
def fib_pair(n):
    if n == 0: return 0, 1
    a, b = fib_pair(n >> 1)                 # a = F(k), b = F(k+1), k = n // 2
    c = a * (2 * b - a)                     # F(2k)
    d = a * a + b * b                       # F(2k+1)
    return (d, c + d) if n & 1 else (c, d)

def fib_loop(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a

# ---- digit count and leading digits WITHOUT calling str() on a huge int:
#      estimate from the bit length, then fix by an exact comparison with a power of ten
def digits_and_lead(x):
    if x == 0: return 1, '0'
    d = max(1, int(x.bit_length() * 0.30102999566398114))      # a lower estimate of the digit count
    while x >= 10 ** d: d += 1                                 # exact: d is the smallest with x < 10^d
    while d > 1 and x < 10 ** (d - 1): d -= 1
    k = max(0, d - 5)
    lead = x // 10 ** k                                        # the first min(5, d) digits, as an int < 10^5 (str is safe)
    return d, str(lead)

def solve(n):
    f = fib_pair(n)[0]
    dg, lead = digits_and_lead(f)
    return [f % MOD, dg, lead]

# ---- examples
assert solve(10) == [55, 2, '55']
assert solve(0) == [0, 1, '0']
assert solve(100) == [687995182, 21, '35422']
assert solve(30000) == [393965141, 6270, '19042']
print('examples ok:', solve(10), solve(0), solve(100), solve(30000))

# ---- cross-check: O(n) addition loop; digits counted by chunked division (no str on a big int)
def digits_chunked(x):
    if x == 0: return 1
    chunk = 10 ** 1000; count = 0
    while x >= chunk: x //= chunk; count += 1000
    return count + len(str(x))                  # the remainder has < 1001 digits, so str() is safe
for n in list(range(0, 400)) + [random.randint(400, 20000) for _ in range(60)]:
    f = fib_loop(n)
    assert fib_pair(n)[0] == f
    dg, lead = digits_and_lead(f)
    assert dg == digits_chunked(f)
    # leading digits independent check: divide away the low digits in 1000-digit chunks, then use str on the small rest
    y, rest = f, dg
    while rest > 1000: y //= 10 ** 1000; rest -= 1000
    assert lead == str(y)[:5], (n, lead)
    assert solve(n) == [f % MOD, dg, lead]
print('460 values of n (0..399 and 60 random up to 20000): doubling == addition loop; digits and leading digits agree with chunked division')

# ---- the int-to-str digit limit (observed on this Python; the 3.11 introduction is editor knowledge)
big = fib_pair(30000)[0]
print('default limit:', sys.get_int_max_str_digits(), '; F(30000) has', digits_and_lead(big)[0], 'digits')
try: str(big)
except ValueError as e: print('str(F(30000)) ->', type(e).__name__)
try: int('9' * 5000)
except ValueError as e: print("int('9' * 5000) ->", type(e).__name__)
print('hex works (power-of-two base):', len(hex(big)), 'characters; bit_length', big.bit_length())
old = sys.get_int_max_str_digits(); sys.set_int_max_str_digits(0)
assert len(str(big)) == 6270 and str(big)[:5] == '19042'
sys.set_int_max_str_digits(old)
print('with the limit lifted str() gives the same 6270 digits and lead 19042; limit restored to', sys.get_int_max_str_digits())

# ---- maximum size and the cost shape (sandbox timings, not proof of big-O)
t = time.perf_counter(); r = solve(100000); t1 = time.perf_counter() - t
t = time.perf_counter(); f = fib_loop(100000); t2 = time.perf_counter() - t
assert f == fib_pair(100000)[0] and r[0] == f % MOD
print('n = 100000:', r, ', digits by length-estimate method;  (sandbox timing) doubling %.4f s, addition loop %.4f s' % (t1, t2))

# ---- Binet's formula in floats: where does it first go wrong?
a = 0
for n in range(200):
    if round(((1 + 5 ** 0.5) / 2) ** n / 5 ** 0.5) != fib_pair(n)[0]: break
print('float Binet first differs from the exact value at n =', n)

# ---- edge asserts
assert solve(1) == [1, 1, '1'] and solve(2) == [1, 1, '1'] and solve(5) == [5, 1, '5']
assert solve(12) == [144, 3, '144'] and solve(20) == [6765, 4, '6765']
assert fib_pair(0) == (0, 1) and fib_pair(1) == (1, 1)
print('edge asserts ok')
