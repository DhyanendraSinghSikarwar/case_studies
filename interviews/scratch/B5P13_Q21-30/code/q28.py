import math
import random
import time

random.seed(2801)

def factorise(n):
    """Returns [factors, divisor_count, steps] with the exact loop from the question."""
    m, d, steps = n, 2, 0
    f = []
    while d * d <= m:
        steps += 1
        if m % d == 0:
            e = 0
            while m % d == 0:          # divide out d completely
                m //= d
                e += 1
            f.append([d, e])
        d += 1
    if m > 1:
        f.append([m, 1])               # leftover is prime (exponent 1)
    div = 1
    for p, e in f:
        div *= e + 1
    return [f, div, steps]

def solve(nums):
    return [factorise(n) for n in nums]

def is_prime(n):                       # independent: plain trial division on all d, no tricks
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))

def brute(nums):
    """Oracle: rebuild n from the factors, count divisors by direct enumeration (small n) or from exponents."""
    out = []
    for n in nums:
        f, div, steps = factorise(n)
        prod = 1
        for p, e in f:
            assert is_prime(p) if p < 10**7 else True
            prod *= p ** e
        assert prod == n and [p for p, _ in f] == sorted(p for p, _ in f)
        if n <= 30000:
            assert div == sum(1 for k in range(1, n + 1) if n % k == 0)
        out.append([f, div, steps])
    return out

examples = [([12, 97, 360, 1024], [[[[2, 2], [3, 1]], 6, 1], [[[97, 1]], 2, 8], [[[2, 3], [3, 2], [5, 1]], 24, 2], [[[2, 10]], 11, 1]]),
            ([2], [[[[2, 1]], 2, 0]]),
            ([999999999989], [[[[999999999989, 1]], 2, 999998]]),
            ([600851475143], [[[[71, 1], [839, 1], [1471, 1], [6857, 1]], 16, 1470]])]
for nums, want in examples:
    assert solve(nums) == want == brute(nums)
    print(nums, '->', solve(nums))

# dry run: n = 360 step by step
m, d = 360, 2
while d * d <= m:
    note = ''
    if m % d == 0:
        e = 0
        while m % d == 0: m //= d; e += 1
        note = f'divide out {d}^{e}, m = {m}'
    print(f'  d={d}: d*d={d * d} <= m -> step; {note}')
    d += 1
print(f'  d={d}: d*d={d * d} > m={m} -> stop; leftover m={m}', '(prime, add it)' if m > 1 else '')

# seeded random cross-check, plus every n from 2 to 20000
for _ in range(500):
    nums = [random.randint(2, 10**6) for _ in range(5)]
    assert solve(nums) == brute(nums)
for n in range(2, 20001):
    assert brute([n]) == [factorise(n)]
print('random cross-check ok: 500 lists; every n in 2..20000 ok')

# why composites never divide m: every d that divides m in the loop is prime (checked for all n <= 30000)
for n in range(2, 30001):
    m, d = n, 2
    while d * d <= m:
        if m % d == 0:
            assert is_prime(d), (n, d)
            while m % d == 0: m //= d
        d += 1
print('every divisor d met by the loop is prime for all n <= 30000: True')

# steps bound: steps <= isqrt(n) - 1 (d runs 2..isqrt(m)), reached only when n is prime
for n in range(2, 20001):
    st = factorise(n)[2]
    assert st <= max(0, math.isqrt(n) - 1)
    assert (st == max(0, math.isqrt(n) - 1)) or not is_prime(n)
print('steps <= isqrt(n) - 1 for n <= 20000, with equality for every prime: True')

# worst case near 10^12: prime
big = 999999999989
assert is_prime(big)
t = time.perf_counter(); r = factorise(big); dt = time.perf_counter() - t
print('prime near 10^12 steps:', r[2], '(sandbox time %.2f s, not a proof)' % dt)
print('10^12 =', factorise(10**12)[:2], 'steps', factorise(10**12)[2])
print('(10^6 + 3)^2 =', factorise((10**6 + 3) ** 2))

# smallest-prime-factor sieve below 10^6: O(n log log n) build, O(log n) per query
LIM = 10**6
spf = list(range(LIM + 1))
for p in range(2, math.isqrt(LIM) + 1):
    if spf[p] == p:
        for q in range(p * p, LIM + 1, p):
            if spf[q] == q:
                spf[q] = p
def spf_factor(n):
    f = []
    while n > 1:
        p = spf[n]; e = 0
        while n % p == 0: n //= p; e += 1
        f.append([p, e])
    return f
for n in [2, 360, 1024, 999983, 720720, 10**6]:
    assert spf_factor(n) == factorise(n)[0]
for _ in range(300):
    n = random.randint(2, LIM)
    assert spf_factor(n) == factorise(n)[0]
print('SPF sieve to 10^6 agrees with trial division on 306 values; 720720 ->', spf_factor(720720))
print('max query length: log2(10^6) =', math.floor(math.log2(LIM)), 'prime-factor pulls at most')

# edge asserts
assert factorise(2) == [[[2, 1]], 2, 0] and factorise(4) == [[[2, 2]], 3, 1] and factorise(9)[0] == [[3, 2]]
assert factorise(2**39)[0] == [[2, 39]] and factorise(2**39)[2] == 1
assert solve([10**12])[0][1] == 169          # (12 + 1) * (12 + 1)
print('edge asserts ok')
