import math
import random

random.seed(2901)
MOD = 1_000_000_007

def ext_gcd(a, b):
    """Returns (g, x, y) with a*x + b*y = g."""
    if b == 0:
        return a, 1, 0
    g, x, y = ext_gcd(b, a % b)
    return g, y, x - (a // b) * y

def inverse(a, m):
    try:
        return pow(a, -1, m)               # Python 3.8+ (editor knowledge); ValueError if gcd > 1
    except ValueError:
        return None

def inverse_ext(a, m):
    g, x, _ = ext_gcd(a % m, m)
    return x % m if g == 1 else None

def solve(a, m, queries):
    mx = max([n for n, _ in queries], default=0)
    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (mx + 1)
    inv_fact[mx] = pow(fact[mx], -1, MOD)           # ONE modular inverse
    for i in range(mx, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD     # (i-1)!^-1 = i! ^-1 * i
    return [inverse(a, m), [fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD for n, r in queries]]

def brute(a, m, queries):
    inv = next((x for x in range(m) if a * x % m == 1), None)
    return [inv, [math.comb(n, r) % MOD for n, r in queries]]

examples = [((3, 7, [[5, 2], [10, 3]]), [5, [10, 120]]),
            ((4, 8, [[0, 0]]), [None, [1]]),
            ((10, MOD, [[100000, 50000]]), [700000005, [149033233]])]
for args, want in examples[:2]:
    assert solve(*args) == want == brute(*args)
a, m, q = examples[2][0]
assert solve(a, m, q) == examples[2][1]
assert math.comb(100000, 50000) % MOD == 149033233 and 10 * 700000005 % MOD == 1
for args, want in examples:
    print(args if len(str(args)) < 60 else (args[0], args[1], args[2]), '->', solve(*args))

# dry run: 3 mod 7 by hand (search), by Fermat, by extended Euclid; C(5,2) from tables mod 7-free formula
print('3 * 5 =', 3 * 5, '=', 15 % 7, '(mod 7)  -> inverse of 3 is 5')
print('Fermat 3^(7-2) mod 7 =', pow(3, 5, 7), '; ext_gcd(3, 7) =', ext_gcd(3, 7), '(3*(-2) + 7*1 = 1, and -2 % 7 = 5)')
print('C(5,2) = 5! * inv(2!) * inv(3!) =', 120, '*', pow(2, -1, MOD), '*', pow(6, -1, MOD), 'mod p =', 120 * pow(2, -1, MOD) * pow(6, -1, MOD) % MOD)

# seeded random cross-check on small values against a scan and math.comb
for _ in range(3000):
    m = random.randint(2, 60); a = random.randint(1, 200)
    qs = [[n, random.randint(0, n)] for n in (random.randint(0, 40) for _ in range(5))]
    assert solve(a, m, qs) == brute(a, m, qs), (a, m)
print('random cross-check ok: 3000 cases')

# exhaustive: inverse exists exactly when gcd = 1, for every a, m <= 80; result in [0, m-1]; ext Euclid agrees
cnt = 0
for m in range(2, 81):
    for a in range(1, 81):
        inv = inverse(a, m)
        assert (inv is not None) == (math.gcd(a, m) == 1)
        assert inv == inverse_ext(a, m) == next((x for x in range(m) if a * x % m == 1), None)
        if inv is not None:
            assert 0 <= inv < m and a * inv % m == 1
        cnt += 1
print('exhaustive a, m <= 80:', cnt, 'pairs: inverse exists iff gcd = 1')

# Fermat's a^(m-2) is the inverse only for PRIME m
def is_prime(n): return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))
bad_comp = bad_prime = 0; ex = None
for m in range(3, 200):
    for a in range(1, m):
        if math.gcd(a, m) == 1:
            ok = pow(a, m - 2, m) == pow(a, -1, m)
            if is_prime(m): bad_prime += (not ok)
            elif not ok:
                bad_comp += 1; ex = ex or (a, m, pow(a, m - 2, m), pow(a, -1, m))
print('Fermat wrong for a prime modulus:', bad_prime, '; for a composite modulus (coprime a):', bad_comp, '; first (a, m, fermat, true) =', ex)
assert bad_prime == 0 and bad_comp > 0
print('pow(4, -1, 8) raises:', end=' ')
try: pow(4, -1, 8)
except ValueError as e: print(repr(str(e)))

# nCr: all n <= 120 vs math.comb, some large queries
qs = [[n, r] for n in range(0, 121) for r in range(0, n + 1)]
res = solve(1, 2, qs)[1]
assert res == [math.comb(n, r) % MOD for n, r in qs]
print('nCr table n <= 120 (', len(qs), 'queries) matches math.comb')
big = [[random.randint(0, 10**5), 0] for _ in range(1000)]
big = [[n, random.randint(0, n)] for n, _ in big]
res = solve(7, 10**9, big)[1]
for (n, r), v in list(zip(big, res))[:15]:
    assert v == math.comb(n, r) % MOD
print('1000 queries with n up to 10^5 built from one table; 15 spot-checked against math.comb')

# why you cannot divide by r!: floor-dividing the reduced products is wrong
n, r = 10, 3
reduced = 1
for i in range(n - r + 1, n + 1): reduced = reduced * i % 11
print('C(10,3) = 120; (10*9*8 mod 11) // 3! =', reduced, '// 6 =', reduced // 6, '(wrong; true 120 mod 11 =', 120 % 11, ')')

# edge asserts
assert solve(1, 2, [])[0] == 1 and solve(2, 2, [])[0] is None
assert solve(10**9, 10**9, [])[0] is None and solve(10**9, 10**9 - 1, [])[0] == 1
assert solve(5, 7, [[0, 0], [100000, 0], [100000, 100000]])[1] == [1, 1, 1]
print('edge asserts ok')
