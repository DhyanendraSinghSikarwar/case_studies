### Q28 ⭐⭐ 🟡 Prime factorisation by trial division. `nums` has 1 to 200 integers with 2 <= value <= 10^12. For each value n return `[factors, divisors, steps]`: `factors` is the list of [prime, exponent] pairs in increasing prime order; `divisors` is the number of positive divisors of n (the product of (exponent + 1)); `steps` is the number of iterations of this loop: `m = n; d = 2`, then `while d * d <= m:` count one step, divide out d completely if it divides m, and do `d += 1`; after the loop, if m > 1 it is a prime factor with exponent 1. Explain why the loop may stop at d * d <= m (the leftover m is then prime), why the worst case is a prime n near 10^12 with about 10^6 steps, why d never needs to skip composites for correctness, and how a smallest-prime-factor sieve answers many queries below 10^6 in O(log n) each after one O(n log log n) build. In the answer include a dry run on the first example and a seeded random cross-check of your solution against reconstructing n from the factors and an independent divisor count on small inputs. Example: nums=[12, 97, 360, 1024] -> [[[[2, 2], [3, 1]], 6, 1], [[[97, 1]], 2, 8], [[[2, 3], [3, 2], [5, 1]], 24, 2], [[[2, 10]], 11, 1]]; nums=[2] -> [[[[2, 1]], 2, 0]]; nums=[999999999989] -> [[[[999999999989, 1]], 2, 999998]]; nums=[600851475143] -> [[[[71, 1], [839, 1], [1471, 1], [6857, 1]], 16, 1470]].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Number theory: trial division up to the square root, shrinking `m` as factors are removed.

**Say this first (1 line):** "Try d = 2, 3, 4, ... while d*d <= m, divide each d out fully, and whatever is left above 1 is a prime."

**Brute force:** Try every d from 2 to n. O(n), which is 10^12 steps for the largest input. The oracle here rebuilds n from the factors and counts the divisors independently (by listing all of 1..n when n is small).

**Optimal:**
- Exactly the loop in the question. `steps` counts each time the `while d * d <= m` test passes.
- Why stopping at `d * d <= m` is enough: if m is composite it has a divisor at most `sqrt(m)`. If no d up to `sqrt(m)` divides m, then m is prime. The leftover is prime with exponent 1.
- Why composites never divide: before d is tried, all smaller primes have been divided out of m completely. A composite d would need a prime factor smaller than itself, which is already gone. The program asserts that every d that divides m is prime for all n up to 30000. So skipping composites would not change the answer, only the step count.
- Divisor count: the product of `(exponent + 1)`.
- Worst case: a prime n near 10^12 never shrinks m, so d runs to `isqrt(n)`. `999999999989` takes 999,998 steps (equal to `isqrt(n) - 1`). The program checks `steps <= isqrt(n) - 1` for all n up to 20000, with equality for every prime. A square of a prime like (10^6 + 3)^2 also costs about 10^6 steps.
- Many queries below 10^6: build the smallest-prime-factor array with a sieve in O(n log log n). Then factorising n takes one array lookup per prime factor, at most about log2(n) = 19 for n up to 10^6, so O(log n) per query. The program builds it and compares with trial division.

**Complexity:** Time O(sqrt(n)) per number, so at most about 10^6 iterations for n up to 10^12, and 200 numbers is roughly 2 * 10^8 loop iterations in the worst case (do not give 200 large primes to a Python loop without thinking). Space O(number of distinct primes). The sandbox ran the single worst number in well under a second (a sandbox timing, not a proof).

**Dry run:** `n = 360`. d = 2: 4 <= 360, step 1, divide out 2^3, m = 45. d = 3: 9 <= 45, step 2, divide out 3^2, m = 5. d = 4: 16 > 5, stop. Leftover m = 5 is prime. Factors `[[2,3],[3,2],[5,1]]`, divisors (3+1)(2+1)(1+1) = 24, steps 2. The program prints this.

**Code:**
```python
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
```

**Output (my run):**
```
[12, 97, 360, 1024] -> [[[[2, 2], [3, 1]], 6, 1], [[[97, 1]], 2, 8], [[[2, 3], [3, 2], [5, 1]], 24, 2], [[[2, 10]], 11, 1]]
[2] -> [[[[2, 1]], 2, 0]]
[999999999989] -> [[[[999999999989, 1]], 2, 999998]]
[600851475143] -> [[[[71, 1], [839, 1], [1471, 1], [6857, 1]], 16, 1470]]
  d=2: d*d=4 <= m -> step; divide out 2^3, m = 45
  d=3: d*d=9 <= m -> step; divide out 3^2, m = 5
  d=4: d*d=16 > m=5 -> stop; leftover m=5 (prime, add it)
random cross-check ok: 500 lists; every n in 2..20000 ok
every divisor d met by the loop is prime for all n <= 30000: True
steps <= isqrt(n) - 1 for n <= 20000, with equality for every prime: True
prime near 10^12 steps: 999998 (sandbox time 0.08 s, not a proof)
10^12 = [[[2, 12], [5, 12]], 169] steps 4
(10^6 + 3)^2 = [[[1000003, 2]], 3, 1000002]
SPF sieve to 10^6 agrees with trial division on 306 values; 720720 -> [[2, 4], [3, 2], [5, 1], [7, 1], [11, 1], [13, 1]]
max query length: log2(10^6) = 19 prime-factor pulls at most
edge asserts ok
```

**Edge cases:**
- n = 2: the loop does not run (4 > 2), steps 0, leftover 2.
- Powers of a prime: `1024` is `2^10` and costs 1 step (m drops to 1 immediately).
- n = 10^12 = 2^12 * 5^12: 4 steps, 169 divisors.
- Prime near 10^12 and a square of a large prime: about 10^6 steps.
- Perfect squares like 36: d = 6 is never needed because 2 and 3 are removed first.

**Follow-ups:**
- *Speed up the loop?* Handle 2 once and then try only odd d, or only 6k +- 1. It halves or thirds the steps; the big-O stays.
- *Primality of a single 64-bit number?* Miller-Rabin (not covered here).
- *Many big numbers?* Pollard's rho. Mention only.

**Common mistakes:**
- Looping `d <= n` instead of `d * d <= m`; or testing `d * d <= n` with the original n so the loop does not shrink.
- Forgetting the leftover prime above 1.
- Dividing `m` only once per d (so 12 becomes `[2,1],[3,1]` plus a leftover 2).
- Using float `sqrt` for 10^12-sized values; use `d * d <= m` or `math.isqrt`.
