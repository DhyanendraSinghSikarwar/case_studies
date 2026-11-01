### Q29 ⭐⭐ 🟡 Modular inverse and n choose r modulo a prime. `a` is an integer with 1 <= a <= 10^9, `m` is an integer with 2 <= m <= 10^9, and `queries` has up to 1000 pairs [n, r] with 0 <= r <= n <= 10^5. Return `[inverse, answers]`: `inverse` is the integer x in [0, m - 1] with (a * x) % m == 1, or None if no such x exists; `answers[t]` is C(n, r) modulo 1000000007 for query t. Use `pow(a, -1, m)` (negative exponents with a modulus work from Python 3.8, a version note from editor knowledge; verified here on 3.13; it raises ValueError when gcd(a, m) > 1) and state when the inverse exists (exactly when gcd(a, m) = 1). Build the factorial table once and an inverse-factorial table from a single modular inverse of the largest factorial, so each query is O(1). Explain Fermat's little theorem a^(p-2) mod p as the inverse for PRIME p only (it is wrong for composite m) and the extended Euclidean algorithm as the general method, and why you cannot divide by r! (the exact quotient is not available after reducing modulo p). For modular powers without an inverse, `pow(x, n, m)` from Part 13's fast-power question is the tool (Q9). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a scan for the inverse and math.comb reduced modulo p on small inputs. Example: a=3, m=7, queries=[[5, 2], [10, 3]] -> [5, [10, 120]]; a=4, m=8, queries=[[0, 0]] -> [null, [1]]; a=10, m=1000000007, queries=[[100000, 50000]] -> [700000005, [149033233]].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Modular arithmetic: modular inverse, and binomial coefficients from factorial and inverse-factorial tables.

**Say this first (1 line):** "The inverse of a modulo m exists exactly when gcd(a, m) = 1; for C(n, r) mod a prime p, precompute factorials and inverse factorials once and answer each query with two multiplications."

**Brute force:** For the inverse, try every x in [0, m-1] and test `a * x % m == 1` (O(m)). For C(n, r), call `math.comb(n, r) % p`, which builds a huge integer (for n = 10^5 that is a number with tens of thousands of digits). Both are the oracle.

**Optimal:**
- Inverse: `pow(a, -1, m)`. Negative exponents with a modulus need Python 3.8 or later (that is editor knowledge; the behaviour was run here on 3.13). It raises `ValueError` ("base is not invertible for the given modulus") when gcd(a, m) > 1, so catch it and return `None`. The result is already in [0, m-1].
- The inverse exists exactly when gcd(a, m) = 1. If gcd = g > 1, then `a * x` and `m` are both multiples of g, so `a * x % m` is also a multiple of g and can never be 1. If gcd = 1, Bezout gives `a*x + m*y = 1`, so x is the inverse. The program checks all a, m up to 80 (6320 pairs).
- Extended Euclid is the general method: `ext_gcd(a, b)` returns `(g, x, y)` with `a*x + b*y = g`; if g = 1 then `x % m` is the inverse. For `(3, 7)` it returns `(1, -2, 1)`, meaning `3*(-2) + 7*1 = 1`, and `-2 mod 7 = 5`, the inverse.
- Fermat: for a PRIME modulus p and gcd(a, p) = 1, `a^(p-2) mod p` is the inverse. For a composite modulus it fails: the program finds it wrong for 7436 coprime (a, m) pairs with composite m below 200, for example a = 3, m = 4 gives 1 but the true inverse is 3. It was right for every prime modulus.
- nCr: `fact[i]` mod p for i up to the largest n. One inverse: `inv_fact[mx] = pow(fact[mx], -1, p)`. Then `inv_fact[i-1] = inv_fact[i] * i % p` going down. Each query is `fact[n] * inv_fact[r] % p * inv_fact[n-r] % p`.
- Why you cannot divide by r!: after reducing the product modulo p the exact quotient is gone. The program shows C(10, 3): `(10*9*8 mod 11) // 3!` gives 0 but the real answer mod 11 is 10. You must multiply by the modular inverse of r!, which exists because n < p means r! shares no factor with p.
- The tables need n < p (10^5 < 10^9 + 7 here). For n >= p you would need Lucas' theorem.

**Complexity:** Tables O(N) with N the largest n (at most 10^5), one `pow` of O(log p) multiplications, each query O(1). Total O(N + Q + log p). The inverse of a by `pow` is O(log m); the scan is O(m). Space O(N).

**Dry run:** `a=3, m=7`: `3 * 5 = 15 = 1 (mod 7)`, so the inverse is 5. Fermat gives `3^5 mod 7 = 5` too, because 7 is prime. For C(5, 2) = 120 / (2 * 6) = 10: `fact[5] * inv_fact[2] * inv_fact[3]` mod p gives 10. The program prints these.

**Code:**
```python
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
```

**Output (my run):**
```
(3, 7, [[5, 2], [10, 3]]) -> [5, [10, 120]]
(4, 8, [[0, 0]]) -> [None, [1]]
(10, 1000000007, [[100000, 50000]]) -> [700000005, [149033233]]
3 * 5 = 15 = 1 (mod 7)  -> inverse of 3 is 5
Fermat 3^(7-2) mod 7 = 5 ; ext_gcd(3, 7) = (1, -2, 1) (3*(-2) + 7*1 = 1, and -2 % 7 = 5)
C(5,2) = 5! * inv(2!) * inv(3!) = 120 * 500000004 * 166666668 mod p = 10
random cross-check ok: 3000 cases
exhaustive a, m <= 80: 6320 pairs: inverse exists iff gcd = 1
Fermat wrong for a prime modulus: 0 ; for a composite modulus (coprime a): 7436 ; first (a, m, fermat, true) = (3, 4, 1, 3)
pow(4, -1, 8) raises: 'base is not invertible for the given modulus'
nCr table n <= 120 ( 7381 queries) matches math.comb
1000 queries with n up to 10^5 built from one table; 15 spot-checked against math.comb
C(10,3) = 120; (10*9*8 mod 11) // 3! = 5 // 6 = 0 (wrong; true 120 mod 11 = 10 )
edge asserts ok
```

**Edge cases:**
- `a = 4, m = 8`: gcd 2, no inverse, answer `None` (the question's `null`).
- `a` larger than `m` or a multiple of `m`: reduce implicitly; `pow` handles it. `a = m` gives `None`.
- `m = 2`, `a = 1`: the inverse is 1.
- `r = 0` or `r = n`: both give 1.
- `n = 10^5`, `r = 50000`: the table has 100001 entries; the answer is 149033233.
- No queries: tables of size 1.

**Follow-ups:**
- *Modular power when there is no inverse?* `pow(x, n, m)` (the fast power in Q9) works for any m.
- *Inverse of all numbers 1..N in O(N)?* `inv[i] = -(p // i) * inv[p % i] % p`, for prime p.
- *Why mod 10^9 + 7?* It is a prime a bit below 2^30, so products of two residues fit in a 64-bit integer in other languages. Python does not care.

**Common mistakes:**
- Using Fermat for a composite modulus.
- Dividing with `//` after taking the modulus.
- Computing the inverse of `r!` and `(n-r)!` separately for each query with `pow` (works, but costs a log factor per query).
- Forgetting that `pow(a, -1, m)` raises when the inverse does not exist.
