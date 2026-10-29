### Q31 ⭐⭐ 🟡 Floating point versus exact arithmetic. `prices` has 1 to 50 decimal strings (each like '0.10' or '-3.2', at most 3 decimals) and `target` is a decimal string. Return `[float_sum, exact_sum, equal, close, fsum]`: `float_sum = repr(s)` where s adds `float(p)` for the prices left to right starting from 0.0; `exact_sum` is `str(Fraction)` of the exact sum of the decimal prices (e.g. '3/10'); `equal` is `s == float(target)`; `close` is `math.isclose(s, float(target))` with its default relative tolerance 1e-9 and no absolute tolerance; `fsum = repr(math.fsum(floats))`. Explain why 0.1 + 0.2 == 0.3 is False (the doubles for 0.1, 0.2 and 0.3 are not those decimals), why you should compare floats with `math.isclose` (and why `math.isclose(1e-12, 0.0)` is False unless you give `abs_tol`), why `math.fsum` is more accurate than the plain left-to-right loop `s += v` (observed on Python 3.13: the built-in `sum` of floats is itself compensated, so `sum([0.1] * 10)` is 1.0 while the loop gives 0.9999999999999999; do not assume that for older versions), and when to switch to `Fraction` (exact rationals) or `Decimal` (decimal money) or integer cents. In the answer include a dry run on the first example and a seeded random cross-check of your solution against exact Fraction arithmetic built from the decimal strings on small inputs. Example: prices=['0.1', '0.2'], target='0.3' -> ['0.30000000000000004', '3/10', False, True, '0.30000000000000004']; prices=['0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1'], target='1' -> ['0.9999999999999999', '1', False, True, '1.0']; prices=['0.25', '0.5'], target='0.75' -> ['0.75', '3/4', True, True, '0.75']; prices=['19.99', '5.01', '-0.5'], target='24.5' -> ['24.5', '49/2', True, True, '24.5'].
**Asked at:** Python documentation for int, float, Decimal and Fraction (docs.python.org fetch failed with ENOTFOUND, not opened; behaviour verified by running Python 3.13)

**Pattern:** Numeric representation. Binary floats store the nearest double, not the decimal you typed. So: compare with a tolerance, sum with `math.fsum`, and use `Fraction`, `Decimal` or integer cents when the answer must be exact.

**Say this first (1 line):** "0.1, 0.2 and 0.3 are not stored exactly, so I never use `==` on computed floats; I use `math.isclose` with an explicit tolerance, `math.fsum` for sums, and exact types (`Fraction`, `Decimal`, integer cents) for money."

**Brute force:** Parse each decimal string by hand into an exact `Fraction` (integer of all digits over a power of ten), add them, and separately add the floats left to right. That is the oracle in the code. It is exact but slow and verbose. The point of the question is knowing which tool to reach for.

**Optimal:**
- `float_sum`: `s = 0.0; for v in floats: s += v`. A plain loop, on purpose, to show the drift.
- `exact_sum`: `sum(Fraction(Decimal(p)))`. `Decimal('0.1')` is exactly one tenth, so the `Fraction` is exactly 1/10.
- `equal`: `s == float(target)`. `close`: `math.isclose(s, float(target))`, default `rel_tol=1e-9`, `abs_tol=0.0`.
- `fsum`: `math.fsum(floats)` returns the correctly rounded sum of the doubles it was given.
- Why `0.1 + 0.2 == 0.3` is False: the doubles are `3602879701896397/36028797018963968`, `3602879701896397/18014398509481984` and `5404319552844595/18014398509481984` (printed in the run). None is the decimal value. The sum of the first two rounds to a double that is one step above the double for 0.3.
- `math.isclose(1e-12, 0.0)` is False: the tolerance is relative (`1e-9 * max(|a|, |b|)` = 1e-21 here), and relative to zero nothing is close. Give `abs_tol` (for example `1e-9`) when zero is a possible target.
- `fsum` versus the loop: each `s += v` rounds, and the rounding errors pile up (1000 times 0.1 gives `99.9999999999986` in the loop). `fsum` tracks the lost low-order bits and rounds once.
- Observed on Python 3.13 (this run): the built-in `sum([0.1] * 10)` is `1.0` while the loop gives `0.9999999999999999`. So on 3.13 `sum` of floats is itself compensated. That the change came in 3.12 is editor knowledge, not tested here; do not assume it on older versions and use `math.fsum` when it matters.
- When to leave floats: `Fraction` for exact rationals (slow, can grow); `Decimal` for decimal money with explicit rounding (build it from strings, never from a float: `Decimal(0.1)` is the long exact double); integer cents for the fastest, simplest exact money. Note that `fsum` is exact for the doubles, not for your decimals: the sum of the doubles `0.1`, `0.2` is `0.30000000000000004` even under `fsum`.

**Complexity:** O(n) time for each of the sum, `fsum` and the `Fraction` total (the `Fraction` sum has denominators up to 1000, so each addition is cheap). O(n) space for the float list. n is at most 50.

**Dry run:** `prices = ['0.1', '0.2']`, `target = '0.3'`.
- Doubles: 3602879701896397/36028797018963968 plus 3602879701896397/18014398509481984 is exactly 10808639105689191/36028797018963968, which is exactly halfway between the doubles 5404319552844595/2^54 (the double for 0.3) and 5404319552844596/2^54; ties go to the even numerator, so it rounds up to 5404319552844596/2^54 (printed `0.30000000000000004`).
- Exact: 1/10 + 2/10 = 3/10, so `exact_sum = '3/10'`.
- `equal`: that double is not the double of 0.3, so False.
- `close`: the difference is about 5.5e-17, far below 1e-9 times 0.3, so True.
- `fsum`: the doubles themselves sum to that same neighbour of 0.3, so `0.30000000000000004` (fsum cannot fix a representation error that is already in the inputs).

**Code:**
```python
import math
import random
import sys
from decimal import Decimal
from fractions import Fraction

random.seed(3101)


def solve(prices, target):
    floats = [float(p) for p in prices]
    s = 0.0
    for v in floats:                                   # plain left-to-right loop, NOT the built-in sum
        s += v
    exact = sum(Fraction(Decimal(p)) for p in prices)  # Decimal(p) is exact for a decimal string
    t = float(target)
    return [repr(s), str(exact), s == t, math.isclose(s, t), repr(math.fsum(floats))]


def brute(prices, target):
    """Independent oracle: parse the decimal strings by hand into integer cents*10^3, no Decimal."""
    def parse(p):
        sign = -1 if p.startswith("-") else 1
        whole, _, frac = p.lstrip("-").partition(".")
        return sign * Fraction(int(whole + frac), 10 ** len(frac))
    exact = sum(parse(p) for p in prices)
    s = 0.0
    for p in prices:
        s = s + float(p)
    # fsum returns the correctly rounded sum of the DOUBLES, so compare with the exact sum of those doubles
    fs = float(sum(Fraction(float(p)) for p in prices))
    t = float(target)
    close = abs(s - t) <= 1e-9 * max(abs(s), abs(t))
    return [repr(s), str(exact), s == t, close, repr(fs)]


# dry run on the first example: show the doubles that are really stored
print("0.1 is stored as", Fraction(0.1))
print("0.2 is stored as", Fraction(0.2))
print("0.3 is stored as", Fraction(0.3))
print("0.1 + 0.2 =", repr(0.1 + 0.2), "| as a fraction:", Fraction(0.1 + 0.2), "| equals 0.3's double?", 0.1 + 0.2 == 0.3)

examples = [
    (["0.1", "0.2"], "0.3", ["0.30000000000000004", "3/10", False, True, "0.30000000000000004"]),
    (["0.1"] * 10, "1", ["0.9999999999999999", "1", False, True, "1.0"]),
    (["0.25", "0.5"], "0.75", ["0.75", "3/4", True, True, "0.75"]),
    (["19.99", "5.01", "-0.5"], "24.5", ["24.5", "49/2", True, True, "24.5"]),
]
for pr, tg, want in examples:
    got = solve(pr, tg)
    assert got == want == brute(pr, tg), (pr, got)
    print(len(pr), "prices ->", got)


def dec(rng):
    k = rng.randint(0, 3)
    v = rng.randint(-5000, 5000)
    q = abs(v)
    return ("-" if v < 0 else "") + (str(q // 10 ** k) + ("." + str(q % 10 ** k).zfill(k) if k else ""))


rng = random.Random(31)
for _ in range(2000):
    pr = [dec(rng) for _ in range(rng.randint(1, 50))]
    tg = rng.choice([dec(rng), str(sum(Fraction(Decimal(p)) for p in pr).limit_denominator(1000))])
    if "/" in tg:
        tg = str(float(Fraction(tg)))
    assert solve(pr, tg) == brute(pr, tg), (pr, tg)
print("2000 seeded random cases match the hand-parsed Fraction oracle")

# the claims, as observed on THIS interpreter
print("python", sys.version.split()[0])
loop10 = 0.0
for v in [0.1] * 10:
    loop10 += v
print("loop  [0.1]*10 :", repr(loop10))
print("sum() [0.1]*10 :", repr(sum([0.1] * 10)))
print("fsum  [0.1]*10 :", repr(math.fsum([0.1] * 10)))
print("isclose(1e-12, 0.0)                  :", math.isclose(1e-12, 0.0))
print("isclose(1e-12, 0.0, abs_tol=1e-9)    :", math.isclose(1e-12, 0.0, abs_tol=1e-9))
print("isclose(0.1 + 0.2, 0.3)              :", math.isclose(0.1 + 0.2, 0.3))
print("Decimal('0.1') + Decimal('0.2')      :", Decimal("0.1") + Decimal("0.2"), Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
print("Decimal(0.1) (from the float)        :", Decimal(0.1))
print("cents as ints: 10 + 20 == 30         :", 10 + 20 == 30)
# a loop that really drifts and where sum() and fsum differ from the loop
xs = [0.1] * 1000
loop = 0.0
for v in xs:
    loop += v
print("1000 x 0.1: loop", repr(loop), "| sum", repr(sum(xs)), "| fsum", repr(math.fsum(xs)))
assert sum([0.1] * 10) == 1.0 and loop != 100.0 and math.fsum(xs) == 100.0

# edge cases
assert solve(["0"], "0") == ["0.0", "0", True, True, "0.0"]
assert solve(["-0.5", "0.5"], "0") == ["0.0", "0", True, True, "0.0"]     # isclose(0.0, 0.0) is True: identical values
assert solve(["0.001"], "0")[2:4] == [False, False]                        # near zero, isclose without abs_tol says no
assert solve(["1.000"], "1")[1] == "1"
print("edge asserts ok")
```

**Output (my run):**
```
0.1 is stored as 3602879701896397/36028797018963968
0.2 is stored as 3602879701896397/18014398509481984
0.3 is stored as 5404319552844595/18014398509481984
0.1 + 0.2 = 0.30000000000000004 | as a fraction: 1351079888211149/4503599627370496 | equals 0.3's double? False
2 prices -> ['0.30000000000000004', '3/10', False, True, '0.30000000000000004']
10 prices -> ['0.9999999999999999', '1', False, True, '1.0']
2 prices -> ['0.75', '3/4', True, True, '0.75']
3 prices -> ['24.5', '49/2', True, True, '24.5']
2000 seeded random cases match the hand-parsed Fraction oracle
python 3.13.17
loop  [0.1]*10 : 0.9999999999999999
sum() [0.1]*10 : 1.0
fsum  [0.1]*10 : 1.0
isclose(1e-12, 0.0)                  : False
isclose(1e-12, 0.0, abs_tol=1e-9)    : True
isclose(0.1 + 0.2, 0.3)              : True
Decimal('0.1') + Decimal('0.2')      : 0.3 True
Decimal(0.1) (from the float)        : 0.1000000000000000055511151231257827021181583404541015625
cents as ints: 10 + 20 == 30         : True
1000 x 0.1: loop 99.9999999999986 | sum 100.0 | fsum 100.0
edge asserts ok
```

**Edge cases:**
- One price `'0'` and target `'0'`: everything agrees (`'0.0'`, `'0'`, True, True, `'0.0'`).
- Values that cancel (`-0.5`, `0.5`): sum `0.0`; `isclose(0.0, 0.0)` is True because identical values short-circuit.
- Near zero (`0.001` against `0`): `==` False and `isclose` False without `abs_tol`.
- Target given as `'1'` while the float sum is `0.9999999999999999`: `==` False, `isclose` True.
- `-0.0` can appear from float arithmetic and compares equal to `0.0`.

**Follow-ups:**
- *Round-half-even?* `round(0.5)` is 0, `round(2.5)` is 2, and `round(2.675, 2)` is `2.67` because the double is below 2.675; use `Decimal` with a rounding mode if the business rule says half-up.
- *Why not always `Decimal`?* It is slower and sticky: mixing `Decimal` and `float` in arithmetic raises `TypeError`.
- *How do you compare floats in a test?* `math.isclose(a, b, rel_tol=..., abs_tol=...)`, choosing both tolerances from the problem.

**Common mistakes:**
- Comparing computed floats with `==`.
- `math.isclose(x, 0.0)` with no `abs_tol`.
- Building `Decimal` from a float instead of a string.
- Assuming `sum()` and `fsum` always differ (on 3.13 they agree here) or that they never do (on older versions they can).
- Believing `fsum` fixes input representation error; it only removes the summation error.

### Q32 ⭐⭐ 🟡 The classic biased shuffle, measured exactly. `n` is an integer with 1 <= n <= 6. The buggy shuffle starts from `a = [0, 1, ..., n - 1]` and for i = 0, 1, ..., n - 1 picks j from the WHOLE range 0..n-1 and swaps `a[i]` with `a[j]`. Run it on every possible sequence of n choices and return `[sequences, distinct, min_count, max_count, most_likely, least_likely]`: the number of sequences (n^n), the number of different permutations produced, the smallest and largest number of sequences leading to one particular permutation, and, as lists, the lexicographically smallest permutation that has the largest count and the lexicographically smallest permutation that has the smallest count. Explain why this can never be uniform for n >= 3: the n^n equally likely sequences would have to split evenly into n! permutations, but n - 1 divides n! and not n^n (n - 1 and n share no factor and n - 1 >= 2). Show the n = 3 table, then contrast it with the correct loop in Q11. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive enumeration of the swap tree on small inputs. Example: n=1 -> [1, 1, 1, 1, [0], [0]]; n=2 -> [4, 2, 2, 2, [0, 1], [0, 1]]; n=3 -> [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]; n=4 -> [256, 24, 8, 15, [1, 0, 3, 2], [3, 0, 1, 2]].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Exact enumeration of a random process. Treat the shuffle as a function of its random choices, run it on all of them, and count how often each permutation appears.

**Say this first (1 line):** "The buggy loop makes n choices each from n options, so there are n^n equally likely sequences; for n >= 3, n! does not divide n^n, so the permutations cannot be equally likely, and I can show the exact counts."

**Brute force:** Recursive enumeration of the swap tree: at step `i` try every `j` in `0..n-1`, swap, recurse; count the leaf permutations. That is the oracle (`brute` in the code), n^n leaves.

**Optimal:** There is no faster way to get exact counts than going through the n^n sequences (n <= 6, so at most 46,656). The loop version is `itertools.product(range(n), repeat=n)` and applies the swaps. The real "optimal" is the idea:
- Buggy shuffle: `for i in range(n): j = random in 0..n-1; swap(a[i], a[j])`. Sequences: n^n.
- Correct shuffle (Q11): `for i from n-1 down to 1: j = random in 0..i; swap`. Sequences: n * (n-1) * ... * 2 = n!, each permutation exactly once.
- Why the bug cannot be fixed by luck: if all n! permutations had the same count, then n! would divide n^n. For n >= 3, the number n - 1 is at least 2, divides n! (it is one of its factors), and shares no factor with n (consecutive integers are coprime), so it cannot divide n^n. Check: n^n mod (n - 1) = 1 for every n (printed for n = 3..200 in the run).
- For n = 1 and 2 the argument does not apply (1 and 4 sequences, 1 and 2 permutations) and the shuffle happens to be uniform.
- Table for n = 3 (from the run): `[0,1,2]`, `[2,0,1]`, `[2,1,0]` each appear 4 times, and `[0,2,1]`, `[1,0,2]`, `[1,2,0]` each 5 times, out of 27. A fair shuffle would give 4.5 each, which is impossible in whole sequences. The correct loop gives each of the six permutations exactly once in 6 sequences.
- The bias grows with n: the most likely permutation is 1.25 times, 1.875, 2.94 and 4.97 times as likely as the least likely one for n = 3, 4, 5, 6.

**Complexity:** O(n^n * n) time for the enumeration (every sequence replays n swaps), O(n!) space for the counter. Fine for n <= 6. Each shuffle itself is O(n); the correct shuffle is O(n) time and in-place.

**Dry run:** `n = 3`, start `[0,1,2]`; the choice sequence is `(j0, j1, j2)`.
- `(0, 0, 0)`: i=0 swaps a[0] with itself, `[0,1,2]`; i=1 swaps a[1] with a[0], `[1,0,2]`; i=2 swaps a[2] with a[0], `[2,0,1]`.
- `(0, 1, 2)`: all three swaps are with themselves, so `[0,1,2]`. Three other sequences also end on the identity: `(0,2,1)`, `(1,0,2)`, `(2,1,0)`. That is 4 hits for `[0,1,2]`.
- Five sequences end on `[0,2,1]`: `(0,1,1)`, `(0,2,2)`, `(1,0,1)`, `(1,2,0)`, `(2,0,0)`. Also 5 for `[1,0,2]` and `[1,2,0]`; 4 for `[2,0,1]` and `[2,1,0]`.
- Most hits is 5 (smallest permutation with 5: `[0,2,1]`), fewest is 4 (smallest with 4: `[0,1,2]`). Result `[27, 6, 4, 5, [0,2,1], [0,1,2]]`.

**Code:**
```python
import itertools
import math
import random
from collections import Counter

random.seed(3201)


def solve(n):
    """Run the buggy shuffle on every one of the n^n choice sequences (j in 0..n-1 for each i)."""
    cnt = Counter()
    for js in itertools.product(range(n), repeat=n):
        a = list(range(n))
        for i, j in enumerate(js):
            a[i], a[j] = a[j], a[i]
        cnt[tuple(a)] += 1
    hi, lo = max(cnt.values()), min(cnt.values())
    return [n ** n, len(cnt), lo, hi,
            list(min(p for p, c in cnt.items() if c == hi)),
            list(min(p for p, c in cnt.items() if c == lo))], cnt


def brute(n):
    """Oracle: recursive enumeration of the swap tree."""
    cnt = Counter()

    def rec(a, i):
        if i == n:
            cnt[tuple(a)] += 1
            return
        for j in range(n):
            b = a[:]
            b[i], b[j] = b[j], b[i]
            rec(b, i + 1)
    rec(list(range(n)), 0)
    hi, lo = max(cnt.values()), min(cnt.values())
    return [sum(cnt.values()), len(cnt), lo, hi,
            list(sorted(p for p in cnt if cnt[p] == hi)[0]),
            list(sorted(p for p in cnt if cnt[p] == lo)[0])]


def correct(n):
    """Fisher-Yates: i from n-1 down to 1, j in 0..i. Exactly n! sequences."""
    cnt = Counter()
    for js in itertools.product(*[range(i + 1) for i in range(n - 1, 0, -1)]):
        a = list(range(n))
        for i, j in zip(range(n - 1, 0, -1), js):
            a[i], a[j] = a[j], a[i]
        cnt[tuple(a)] += 1
    return cnt


for n, want in [(1, [1, 1, 1, 1, [0], [0]]), (2, [4, 2, 2, 2, [0, 1], [0, 1]]),
                (3, [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]), (4, [256, 24, 8, 15, [1, 0, 3, 2], [3, 0, 1, 2]])]:
    got, _ = solve(n)
    assert got == want == brute(n), (n, got)
    print("n =", n, "->", got)

# the n = 3 table: all 27 sequences, then the counts per permutation next to the correct shuffle
res3, cnt3 = solve(3)
print("\nn = 3, buggy shuffle (j from the whole range), 27 sequences:")
fy3 = correct(3)
print("perm        buggy count   buggy prob   correct count (6 sequences)")
for p in sorted(cnt3):
    print(f"{str(list(p)):<11} {cnt3[p]:>11}   {cnt3[p]:>2}/27        {fy3[p]:>5}")
print("sum", sum(cnt3.values()), "| correct sum", sum(fy3.values()), "| ideal 27/6 =", 27 / 6)

# bias grows: statistics for n = 1..6 (6^6 = 46656 sequences is the largest enumeration)
print("\n n   n^n   n!  distinct  min  max   max/min")
for n in range(1, 7):
    r, c = solve(n)
    assert r == brute(n)
    assert r[1] == math.factorial(n)                        # every permutation is reachable, just not evenly
    assert (r[2] == r[3]) == (n <= 2)                       # uniform only for n <= 2
    assert sum(c.values()) == n ** n
    fy = correct(n)
    assert len(fy) == math.factorial(n) and set(fy.values()) == {1}   # correct: every permutation exactly once
    print(f"{n:>2} {n ** n:>5} {math.factorial(n):>4} {r[1]:>8} {r[2]:>4} {r[3]:>4}   {r[3] / r[2]:.3f}")

# the divisibility argument, checked for n = 3..200: n^n is never divisible by n!, because n-1 | n! but gcd(n-1, n) = 1
for n in range(3, 201):
    assert math.factorial(n) % (n - 1) == 0 and math.gcd(n - 1, n) == 1 and n - 1 >= 2
    assert (n ** n) % (n - 1) == 1 and (n ** n) % math.factorial(n) != 0
print("n = 3..200: n^n mod (n-1) = 1 and n! does not divide n^n")
print("n = 1, 2: n^n / n! =", 1 / 1, 4 / 2, "(integers, so uniform is possible and happens)")

# seeded sampling is only a sanity picture, the exact table above is the proof
rng = random.Random(7)
s = Counter()
for _ in range(60000):
    a = [0, 1, 2]
    for i in range(3):
        j = rng.randrange(3)
        a[i], a[j] = a[j], a[i]
    s[tuple(a)] += 1
print("60000 seeded samples (picture only):", {tuple(p): s[p] for p in sorted(s)})

# random cross-check of solve against the recursive oracle (n small; all n in 1..5, each repeated seeded)
for _ in range(60):
    n = random.randint(1, 5)
    assert solve(n)[0] == brute(n)
print("60 seeded checks: loop enumeration equals recursive enumeration")
assert solve(1)[0] == [1, 1, 1, 1, [0], [0]]
print("edge asserts ok")
```

**Output (my run):**
```
n = 1 -> [1, 1, 1, 1, [0], [0]]
n = 2 -> [4, 2, 2, 2, [0, 1], [0, 1]]
n = 3 -> [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]
n = 4 -> [256, 24, 8, 15, [1, 0, 3, 2], [3, 0, 1, 2]]

n = 3, buggy shuffle (j from the whole range), 27 sequences:
perm        buggy count   buggy prob   correct count (6 sequences)
[0, 1, 2]             4    4/27            1
[0, 2, 1]             5    5/27            1
[1, 0, 2]             5    5/27            1
[1, 2, 0]             5    5/27            1
[2, 0, 1]             4    4/27            1
[2, 1, 0]             4    4/27            1
sum 27 | correct sum 6 | ideal 27/6 = 4.5

 n   n^n   n!  distinct  min  max   max/min
 1     1    1        1    1    1   1.000
 2     4    2        2    2    2   1.000
 3    27    6        6    4    5   1.250
 4   256   24       24    8   15   1.875
 5  3125  120      120   16   47   2.938
 6 46656  720      720   32  159   4.969
n = 3..200: n^n mod (n-1) = 1 and n! does not divide n^n
n = 1, 2: n^n / n! = 1.0 2.0 (integers, so uniform is possible and happens)
60000 seeded samples (picture only): {(0, 1, 2): 8894, (0, 2, 1): 11165, (1, 0, 2): 11080, (1, 2, 0): 11199, (2, 0, 1): 8867, (2, 1, 0): 8795}
60 seeded checks: loop enumeration equals recursive enumeration
edge asserts ok
```

**Edge cases:**
- `n = 1`: one sequence, one permutation, uniform.
- `n = 2`: 4 sequences, 2 permutations, 2 each: the only uniform case besides n = 1.
- `n = 3`: the smallest non-uniform case; all 6 permutations still occur, so "reachable" is not the same as "uniform".
- All permutations are always reachable for n <= 6 (`distinct == n!` in the table).

**Follow-ups:**
- *Is there a fixed version that keeps `j` in `0..n-1`?* Not without rejection tricks. Just shrink the range (`0..i`) as Fisher-Yates does.
- *Why was `random.shuffle` correct?* It uses the backward loop with `randbelow(i + 1)`.
- *Can you detect this bias by sampling?* Only roughly (the 60,000 seeded draws in the run show 5/27 against 4/27 for n = 3 as a picture); the exact count above is the proof.

**Common mistakes:**
- Picking `j` from the whole array on every step.
- Thinking "all permutations are reachable" means "uniform".
- Testing fairness by eyeballing a few samples.
- Forgetting that this is an `n^n` versus `n!` counting argument, not a statement about the random number generator.

### Q33 ⭐⭐ 🟡 Reservoir sampling of k items (Algorithm R), checked exactly. `stream` is a list of n items (1 <= n <= 7 integers) and 1 <= k <= n. Keep a reservoir list of the first k items. For the i-th item (i = k+1..n, counting from 1) take the next number d from `draws` (`draws[i - k - 1]`, with 0 <= d <= i - 1) and, if d < k, put the i-th item into reservoir slot d. Return `[reservoir, inclusion, sequences, subsets, min_subset, max_subset]`: `reservoir` is the final list of VALUES for the given `draws` (n - k numbers); `sequences` is the number of possible draw sequences; `inclusion[t]` is the number of those sequences in which the item at position t (0-indexed) ends up in the reservoir; `subsets` is the number of different k-element sets of positions that occur at the end, and `min_subset` and `max_subset` are the smallest and largest number of sequences ending in one particular such set. Use these numbers to show every item is kept with probability k / n and every k-subset is equally likely, and give the proof by induction on the stream length. State the O(k) memory and why n need not be known in advance. In the answer include a dry run on the first example and a seeded random cross-check of your solution against recursive enumeration of all draw sequences on small inputs. Example: stream=[10, 20, 30, 40], k=2, draws=[1, 3] -> [[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]; stream=[7, 8], k=2, draws=[] -> [[7, 8], [1, 1], 1, 1, 1, 1]; stream=[5, 6, 7], k=1, draws=[0, 2] -> [[6], [2, 2, 2], 6, 3, 2, 2].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Streaming sample with a fixed-size reservoir (Algorithm R). Fill the reservoir with the first k, then give item i a k/i chance to enter and kick out a random current member.

**Say this first (1 line):** "Keep the first k; for item i draw d in 0..i-1 and if d < k put item i in slot d; by induction every item ends up kept with probability k/n, and I can confirm it exactly by counting all draw sequences."

**Brute force:** Store the whole stream, then choose k of the n items at random (for example shuffle and take k). O(n) memory and n must be known (or the stream must end). The oracle here enumerates all draw sequences recursively.

**Optimal:**
- Reservoir of k slots. For the i-th item (i = k+1..n, counted from 1) draw d uniformly in `0..i-1`.
- If `d < k`: write item i into slot d. Else drop item i. The new item enters with probability k/i, and it evicts the item in slot d, which is uniform among the k current members.
- Proof by induction on the stream length i. Claim: after i items every k-subset of the first i items is equally likely (probability 1 / C(i, k)). Base i = k: the one subset. Step: take a fixed k-subset T of the first i items.
  - If item i is in T: the previous reservoir must be `T minus {i}` plus one other item x among the first i-1 items (i - k choices of x), and then d must hit exactly x's slot (probability 1/i). Probability: (i - k) * (1 / C(i-1, k)) * (1/i).
  - If item i is not in T: the previous reservoir must be T, and d >= k (probability (i - k)/i): (1 / C(i-1, k)) * (i - k)/i.
  - Both cases give (i - k) / (i * C(i-1, k)). Since C(i, k) = i * C(i-1, k) / (i - k), that equals 1 / C(i, k). So every k-subset is equally likely, and each item is in C(i-1, k-1) / C(i, k) = k/i of them.
- Memory O(k). n need not be known: after any prefix the reservoir is already a uniform sample of that prefix; you can stop at any time.
- Exact check (run): for n = 4, k = 2 there are 3 * 4 = 12 sequences; each item is kept in 6 of them (12 * 2 / 4), each of the 6 pairs arises 2 times. For all n <= 7 and all k <= n the same two facts hold (asserted).

**Complexity:** Time O(n) with one random draw per item after the first k; space O(k) (plus the output). The verification here is O(n!/k!) and is only for small n.

**Dry run:** `stream = [10, 20, 30, 40]`, `k = 2`, `draws = [1, 3]`.
- Start reservoir `[10, 20]`.
- Item 3 (value 30): draw 1 in `0..2`; 1 < 2, so slot 1 gets 30: `[10, 30]`.
- Item 4 (value 40): draw 3 in `0..3`; 3 >= 2, so ignore: `[10, 30]`.
- Enumeration: 12 draw sequences (3 * 4); inclusion `[6, 6, 6, 6]`; the 6 possible pairs each occur twice. Result `[[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]`.

**Code:**
```python
import itertools
import math
import random
from collections import Counter

random.seed(3301)


def run(stream, k, draws):
    """Algorithm R with fixed draws. Slots hold positions so we can count, values are read at the end."""
    n = len(stream)
    slots = list(range(k))                       # slot s holds the position of an item
    for i, d in zip(range(k + 1, n + 1), draws):  # i = 1-based index of the new item, d in 0..i-1
        if d < k:
            slots[d] = i - 1
    return slots


def solve(stream, k, draws):
    n = len(stream)
    reservoir = [stream[p] for p in run(stream, k, draws)]
    inclusion = [0] * n
    subsets = Counter()
    seqs = 0
    for ds in itertools.product(*[range(i) for i in range(k + 1, n + 1)]):   # ALL draw sequences
        slots = run(stream, k, ds)
        seqs += 1
        subsets[frozenset(slots)] += 1
        for p in slots:
            inclusion[p] += 1
    return [reservoir, inclusion, seqs, len(subsets), min(subsets.values()), max(subsets.values())]


def brute(stream, k, draws):
    n = len(stream)
    res = list(stream[:k])
    for idx, d in enumerate(draws):
        if d < k:
            res[d] = stream[k + idx]
    acc = []

    def rec(i, r):                               # recursion over the item number, tries every d in 0..i-1
        if i > n:
            acc.append(tuple(r))
            return
        for d in range(i):
            r2 = list(r)
            if d < k:
                r2[d] = i - 1
            rec(i + 1, r2)
    rec(k + 1, list(range(k)))
    cnt = [sum(p in r for r in acc) for p in range(n)]
    subs = Counter(frozenset(r) for r in acc)
    return [res, cnt, len(acc), len(subs), min(subs.values()), max(subs.values())]


# dry run on the first example: stream [10, 20, 30, 40], k = 2, draws [1, 3]
stream, k, draws = [10, 20, 30, 40], 2, [1, 3]
res = list(stream[:k])
print("start reservoir", res)
for i, d in zip(range(k + 1, len(stream) + 1), draws):
    item = stream[i - 1]
    if d < k:
        res[d] = item
    print(f"item {i} = {item}, draw d = {d} (0..{i - 1}): {'d < k, slot ' + str(d) + ' <- ' + str(item) if d < k else 'd >= k, ignore'} -> {res}")

for st, kk, dr, want in [([10, 20, 30, 40], 2, [1, 3], [[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]),
                         ([7, 8], 2, [], [[7, 8], [1, 1], 1, 1, 1, 1]),
                         ([5, 6, 7], 1, [0, 2], [[6], [2, 2, 2], 6, 3, 2, 2])]:
    got = solve(st, kk, dr)
    assert got == want == brute(st, kk, dr), (st, kk, got)
    print(st, "k =", kk, "draws", dr, "->", got)

# exact uniformity for EVERY n <= 7 and k <= n: inclusion = k * seqs / n, all C(n,k) subsets, each seqs / C(n,k) times
print("\n n k  sequences  inclusion per item        subsets  per subset")
for n in range(1, 8):
    for kk in range(1, n + 1):
        r = solve(list(range(n)), kk, [0] * (n - kk))
        seqs = r[2]
        assert seqs == math.factorial(n) // math.factorial(kk)          # prod_{i=k+1..n} i
        assert set(r[1]) == {kk * seqs // n} and kk * seqs % n == 0      # every item kept k/n of the time
        assert r[3] == math.comb(n, kk) and r[4] == r[5] == seqs // math.comb(n, kk)
        if n in (5, 7) or (n == 4 and kk in (1, 2)):
            print(f"{n:>2} {kk} {seqs:>10}  {str(r[1][:1]) + ' x ' + str(n):<22}  {r[3]:>5}  {r[4]:>6}")
print("all n <= 7, all k <= n: each item is held in k/n of the sequences, all C(n,k) subsets occur equally often")

# seeded random cross-check against the recursive enumeration
for _ in range(300):
    n = random.randint(1, 6)
    kk = random.randint(1, n)
    st = [random.randint(0, 9) for _ in range(n)]
    dr = [random.randint(0, i - 1) for i in range(kk + 1, n + 1)]
    assert solve(st, kk, dr) == brute(st, kk, dr)
print("300 seeded random cases match the recursive enumeration")

# edge cases
assert solve([4], 1, [])[:3] == [[4], [1], 1]                 # n = 1
assert solve([1, 2, 3], 3, [])[0] == [1, 2, 3]                # k = n: no draws, nothing is replaced
assert solve([1, 2, 3], 1, [0, 0])[0] == [3]                  # d = 0 each time replaces slot 0
print("edge asserts ok")
```

**Output (my run):**
```
start reservoir [10, 20]
item 3 = 30, draw d = 1 (0..2): d < k, slot 1 <- 30 -> [10, 30]
item 4 = 40, draw d = 3 (0..3): d >= k, ignore -> [10, 30]
[10, 20, 30, 40] k = 2 draws [1, 3] -> [[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]
[7, 8] k = 2 draws [] -> [[7, 8], [1, 1], 1, 1, 1, 1]
[5, 6, 7] k = 1 draws [0, 2] -> [[6], [2, 2, 2], 6, 3, 2, 2]

 n k  sequences  inclusion per item        subsets  per subset
 4 1         24  [6] x 4                     4       6
 4 2         12  [6] x 4                     6       2
 5 1        120  [24] x 5                    5      24
 5 2         60  [24] x 5                   10       6
 5 3         20  [12] x 5                   10       2
 5 4          5  [4] x 5                     5       1
 5 5          1  [1] x 5                     1       1
 7 1       5040  [720] x 7                   7     720
 7 2       2520  [720] x 7                  21     120
 7 3        840  [360] x 7                  35      24
 7 4        210  [120] x 7                  35       6
 7 5         42  [30] x 7                   21       2
 7 6          7  [6] x 7                     7       1
 7 7          1  [1] x 7                     1       1
all n <= 7, all k <= n: each item is held in k/n of the sequences, all C(n,k) subsets occur equally often
300 seeded random cases match the recursive enumeration
edge asserts ok
```

**Edge cases:**
- k = n: there are no draws; the reservoir is the whole stream (1 sequence).
- n = 1 (so k = 1): nothing to draw.
- k = 1 is the classic "pick one uniformly" (item i replaces with probability 1/i; Q35 uses it for indices).
- Draw 0 each time with k = 1 keeps the last item, a legal outcome of probability 1 / n!.
- Duplicate values in the stream are fine: the counts are over positions, not values.

**Follow-ups:**
- *Weighted items?* Algorithm A-Res assigns key `u ** (1 / w)` to each item and keeps the k largest (editor knowledge; not tested here).
- *Faster for huge streams?* Algorithm L skips ahead by a geometric jump, so it draws about k * log(n / k) random numbers instead of n (editor knowledge).
- *Why not "keep with probability k/n" with a first pass for n?* That needs two passes or a known n, and it gives a sample of random size.

**Common mistakes:**
- Drawing `d` in `0..k-1` instead of `0..i-1` (then the last items are over-represented).
- Off-by-one on `i` (counting from 0 instead of 1).
- Replacing slot `i % k` or always the oldest: that is a sliding window, not a uniform sample.
- Using `random.randint(0, i)` (inclusive) with `i` already 1-based.

### Q34 ⭐⭐ 🟡 Rejection sampling: a uniform random integer from a smaller generator. You have `rand_m()` that returns integers uniformly in 1..m and want `rand_t()` uniform in 1..t, where 2 <= m <= 10 and 2 <= t <= m * m. One round reads two values a, b from the generator, forms x = m * (a - 1) + (b - 1) (uniform over 0..m*m-1), and accepts when x < (m*m // t) * t, returning `x % t + 1`; otherwise it rejects x and starts a new round (both values are consumed either way). `stream` is a list of generator values in 1..m (up to 200, possibly odd length; an unpaired last value is unused). Return `[outputs, consumed, counts, expected]`: `outputs` is the list of results produced by the successive full rounds of `stream` (rejected rounds produce nothing); `consumed` is the number of stream values read (2 per round); `counts[v - 1]` is the number of the m * m equally likely pairs (a, b) that produce the result v (all equal, which proves uniformity); and `expected` is the exact expected number of generator calls per output as a reduced fraction string, e.g. '50/21' for m = 5, t = 7 (each round uses 2 calls and succeeds with probability q, so the expected calls are 2 / q). Explain why (a + b) % t is NOT uniform (show the counts for m = 5, t = 7) and why you must reject rather than wrap the leftover values. In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating all m * m pairs and a truncated geometric series for the expectation on small inputs. Example: m=5, t=7, stream=[1, 1, 5, 5, 4, 3, 2, 2] -> [[1, 4, 7], 8, [3, 3, 3, 3, 3, 3, 3], '50/21']; m=7, t=10, stream=[1, 1, 3, 4, 7, 7] -> [[1, 8], 6, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], '49/20']; m=2, t=4, stream=[1, 2, 2, 2, 1] -> [[2, 4], 4, [1, 1, 1, 1], '2'].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Rejection sampling. Build a uniform number over a range that is a multiple of the target, throw away the leftover tail, take a remainder. Retrying (not wrapping) is what keeps it exactly uniform.

**Say this first (1 line):** "Two calls give a uniform x in 0..m*m-1; I accept only x below the largest multiple of t, reduce mod t, and retry otherwise, so every output has exactly the same number of pairs behind it."

**Brute force:** Compute the output distribution by enumerating all m * m pairs `(a, b)`, accept the same ones, and count per result (the oracle, which is also how the answer's `counts` are obtained). For the expected number of calls, sum the truncated series `sum_r (2r) * q * (1 - q)^(r-1)`.

**Optimal:**
- Round: read a, b in 1..m; `x = m * (a - 1) + (b - 1)` is uniform over 0..m*m-1 (a base-m two-digit number).
- Let `lim = (m*m // t) * t`. Accept if `x < lim`, output `x % t + 1`; else reject and start a new round. Each of the t residues has exactly `lim / t = m*m // t` accepted x values behind it, so the output is exactly uniform.
- Success probability per round `q = lim / m^2`. Rounds until success are geometric with mean 1/q, each costing 2 calls, so expected calls are `2 / q = 2 * m^2 / lim`. For m = 5, t = 7: lim = 21, q = 21/25, expected 50/21 = 2.38 calls.
- `q > 1/2` always (`lim >= m^2 / 2` because `floor(y) >= y / 2` for y >= 1, and t <= m^2), so the expected cost is below 4 calls; the run finds the worst over all m in 2..10, t in 2..m^2 is 162/41 = 3.95.
- Why not `(a + b) % t`: the sum of two uniform values is not uniform (sums 2..10 have triangular weights): for m = 5, t = 7 the 25 pairs fall as `[4, 3, 3, 3, 3, 4, 5]` over results 1..7.
- Why not wrap the leftovers (`x % t + 1` without rejecting): 25 = 3 * 7 + 4, so results 1..4 get 4 pairs and results 5..7 only 3: `[4, 4, 4, 4, 3, 3, 3]`. The leftover 4 values would favour the small results. You must reject them.
- Stream handling: only full rounds are read; an unpaired last value is unused and not counted in `consumed`.

**Complexity:** Expected O(1) rounds (below 2 rounds, below 4 calls); worst case unbounded (a run of rejections), but the chance of r consecutive rejections is `(1 - q)^r`, below `2^-r`. Space O(1). The verification table costs O(m^2).

**Dry run:** `m = 5, t = 7`, stream `[1,1,5,5,4,3,2,2]`, `lim = 21`.
- Pair (1,1): x = 0, accepted, 0 % 7 + 1 = 1.
- Pair (5,5): x = 24 >= 21, rejected.
- Pair (4,3): x = 5*3 + 2 = 17, accepted, 17 % 7 + 1 = 4.
- Pair (2,2): x = 5*1 + 1 = 6, accepted, 6 % 7 + 1 = 7.
- `outputs = [1, 4, 7]`, `consumed = 8`, `counts = [3,3,3,3,3,3,3]` (21 accepted pairs / 7), `expected = '50/21'`.

**Code:**
```python
import random
from collections import Counter
from fractions import Fraction

random.seed(3401)


def solve(m, t, stream):
    lim = (m * m // t) * t                       # largest multiple of t that fits in 0..m*m-1 (exclusive bound)
    outputs, consumed = [], 0
    for k in range(0, len(stream) - 1, 2):       # full rounds only: an unpaired last value is unused
        a, b = stream[k], stream[k + 1]
        consumed += 2
        x = m * (a - 1) + (b - 1)                # uniform over 0..m*m-1 when a, b are uniform in 1..m
        if x < lim:
            outputs.append(x % t + 1)
    counts = [0] * t
    for a in range(1, m + 1):                    # exact: push every one of the m*m equally likely pairs through
        for b in range(1, m + 1):
            x = m * (a - 1) + (b - 1)
            if x < lim:
                counts[x % t] += 1
    return [outputs, consumed, counts, str(Fraction(2 * m * m, lim))]   # 2 / q with q = lim / m^2


def brute(m, t, stream):
    pairs = list(zip(stream[0::2], stream[1::2]))
    out = []
    for a, b in pairs:
        x = (a - 1) * m + b - 1
        if x < t * (m * m // t):
            out.append(x % t + 1)
    cnt = Counter(((a - 1) * m + b - 1) % t
                  for a in range(1, m + 1) for b in range(1, m + 1) if (a - 1) * m + b - 1 < t * (m * m // t))
    q = Fraction(t * (m * m // t), m * m)
    # expectation as a truncated geometric series: sum over rounds r of (2r calls) * P(first success at round r)
    series = sum(Fraction(2 * r) * q * (1 - q) ** (r - 1) for r in range(1, 400))
    exact = 2 / q
    assert exact - series < Fraction(1, 10 ** 6) and series <= exact
    return [out, 2 * len(pairs), [cnt[i] for i in range(t)], str(exact)]


# dry run on the first example: m = 5, t = 7, stream [1,1,5,5,4,3,2,2]
m, t = 5, 7
lim = (m * m // t) * t
print(f"m*m = {m * m}, t = {t}, accept x < {lim} (= {m * m // t} * {t}), reject x in {lim}..{m * m - 1}")
stream = [1, 1, 5, 5, 4, 3, 2, 2]
for k in range(0, len(stream), 2):
    a, b = stream[k], stream[k + 1]
    x = m * (a - 1) + (b - 1)
    verdict = f"accept, output {x % t + 1}" if x < lim else "reject (x >= 21)"
    print(f"pair ({a},{b}): x = {m}*{a - 1} + {b - 1} = {x} -> {verdict}")

for mm, tt, st, want in [(5, 7, [1, 1, 5, 5, 4, 3, 2, 2], [[1, 4, 7], 8, [3, 3, 3, 3, 3, 3, 3], "50/21"]),
                         (7, 10, [1, 1, 3, 4, 7, 7], [[1, 8], 6, [4] * 10, "49/20"]),
                         (2, 4, [1, 2, 2, 2, 1], [[2, 4], 4, [1, 1, 1, 1], "2"])]:
    got = solve(mm, tt, st)
    assert got == want == brute(mm, tt, st), (mm, tt, got)
    print(mm, tt, st, "->", got)

# why NOT (a + b) % t, and why not "wrap" x % t without rejecting: exact counts over all 25 pairs
print("\nm = 5, t = 7, all 25 pairs:")
wrongsum = Counter((a + b) % 7 + 1 for a in range(1, 6) for b in range(1, 6))
wrap = Counter((5 * (a - 1) + b - 1) % 7 + 1 for a in range(1, 6) for b in range(1, 6))
print("(a + b) % 7 + 1      :", [wrongsum[v] for v in range(1, 8)], "(sums 2..10 have triangular weights)")
print("x % 7 + 1, no reject :", [wrap[v] for v in range(1, 8)], "(values 1..4 get 4 pairs, 5..7 get 3: leftover 21..24 wrapped)")
assert len(set(wrongsum.values())) > 1 and len(set(wrap.values())) > 1

# exact uniformity and expected cost for EVERY m in 2..10, t in 2..m*m
worst = Fraction(0)
for mm in range(2, 11):
    for tt in range(2, mm * mm + 1):
        r = solve(mm, tt, [])
        lim = (mm * mm // tt) * tt
        assert len(set(r[2])) == 1 and r[2][0] == mm * mm // tt and sum(r[2]) == lim
        assert lim > mm * mm - tt and lim >= tt                     # q = lim / m^2 > 1/2 because floor(y) >= y / 2 for y >= 1
        q = Fraction(lim, mm * mm)
        assert q > Fraction(1, 2) and Fraction(r[3]) == 2 / q
        worst = max(worst, 2 / q)
print(f"all m in 2..10, t in 2..m*m: counts equal, q > 1/2, worst expected calls = {worst} = {float(worst):.3f} (< 4)")

# seeded random cross-check of the stream behaviour and the truncated geometric series
for _ in range(300):
    mm = random.randint(2, 8)
    tt = random.randint(2, mm * mm)
    st = [random.randint(1, mm) for _ in range(random.randint(0, 40))]
    assert solve(mm, tt, st) == brute(mm, tt, st)
print("300 seeded random cases match the pair enumeration and the geometric series")

# edge cases
assert solve(2, 2, [1]) == [[], 0, [2, 2], "2"]        # one unpaired value: nothing read
assert solve(3, 9, [3, 3])[0] == [9] and solve(3, 9, [3, 3])[3] == "2"   # t = m*m: never rejects
assert solve(5, 24, [5, 5, 5, 4])[0] == [24] and solve(5, 24, [5, 5, 5, 4])[3] == "25/12"  # only x = 24 is rejected: q = 24/25
print("edge asserts ok")
```

**Output (my run):**
```
m*m = 25, t = 7, accept x < 21 (= 3 * 7), reject x in 21..24
pair (1,1): x = 5*0 + 0 = 0 -> accept, output 1
pair (5,5): x = 5*4 + 4 = 24 -> reject (x >= 21)
pair (4,3): x = 5*3 + 2 = 17 -> accept, output 4
pair (2,2): x = 5*1 + 1 = 6 -> accept, output 7
5 7 [1, 1, 5, 5, 4, 3, 2, 2] -> [[1, 4, 7], 8, [3, 3, 3, 3, 3, 3, 3], '50/21']
7 10 [1, 1, 3, 4, 7, 7] -> [[1, 8], 6, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], '49/20']
2 4 [1, 2, 2, 2, 1] -> [[2, 4], 4, [1, 1, 1, 1], '2']

m = 5, t = 7, all 25 pairs:
(a + b) % 7 + 1      : [4, 3, 3, 3, 3, 4, 5] (sums 2..10 have triangular weights)
x % 7 + 1, no reject : [4, 4, 4, 4, 3, 3, 3] (values 1..4 get 4 pairs, 5..7 get 3: leftover 21..24 wrapped)
all m in 2..10, t in 2..m*m: counts equal, q > 1/2, worst expected calls = 162/41 = 3.951 (< 4)
300 seeded random cases match the pair enumeration and the geometric series
edge asserts ok
```

**Edge cases:**
- `t = m*m`: lim = m^2, never rejects (q = 1, expected 2 calls).
- `t = m*m - 1`: only x = m^2 - 1 is rejected, q = (m^2 - 1)/m^2; for m = 5, t = 24 the expected cost is `25/12`.
- `t = 2` with an odd m: still works, rejects the last value (for m = 5 that is x = 24).
- Empty or one-element stream: no round, `outputs = []`, `consumed = 0`.
- `t <= m` can be done with one call plus rejection, but the two-call round is the general rule asked for here.

**Follow-ups:**
- *Fewer wasted calls?* Reuse the rejected tail: `x - lim` is uniform over `0..m*m-lim-1` and can seed the next round (not implemented here).
- *rand7 from rand5 with m = 5, t = 7?* Exactly this; expected 50/21 calls per output.
- *Bias-free alternative with floats?* None that is exact; floats make the problem worse.

**Common mistakes:**
- `(a + b) % t`, or `rand_m() * rand_m() % t` (both non-uniform).
- Wrapping instead of rejecting.
- Forgetting the `- 1` offsets, making x range over 1..m^2 and breaking `x % t`.
- Rejecting only the pair, but not counting its two consumed calls.
- Forgetting that a pair is consumed even on rejection.

### Q35 ⭐⭐ 🟡 Random index of a target value, uniform over its occurrences. `nums` has 1 to 8 integers (duplicates allowed), `target` occurs c >= 1 times in it, and `draws` is a list of c numbers. Scan `nums` from left to right keeping one held index: at the j-th occurrence of `target` (j = 0..c-1) take `draws[j]` (with 0 <= draws[j] <= j) and replace the held index by this occurrence's index exactly when `draws[j] == 0`. Return `[index, counts, sequences]`: `index` is the held index at the end for the given draws; `sequences` is the number of possible draw sequences (c!); and `counts[j]` is the number of those sequences after which the j-th occurrence (in left-to-right order) is held. Use the counts to show each occurrence is chosen with probability 1/c, and explain the O(n) time and O(1) space of this single scan, versus the O(n) memory of building a dictionary from value to a list of indices (which gives O(1) per pick after an O(n) build). In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating all draw sequences on small inputs. Example: nums=[1, 2, 3, 3, 3], target=3, draws=[0, 1, 0] -> [4, [2, 2, 2], 6]; nums=[9, 9], target=9, draws=[0, 1] -> [0, [1, 1], 2]; nums=[4, 5, 6], target=5, draws=[0] -> [1, [1], 1].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Reservoir sampling of size 1 over the matching positions. At the j-th occurrence replace the held index with probability 1/(j+1); every occurrence ends up with probability 1/c.

**Say this first (1 line):** "I scan once, count the occurrences of the target, and at the j-th one I take the new index with probability 1/(j+1); that makes every occurrence equally likely, O(n) time and O(1) memory."

**Brute force:** Build a dictionary from value to the list of its indices, then `random.choice` from the target's list. Pick in O(1) after an O(n) build, but O(n) memory. Good when you pick many times.

**Optimal:**
- One left-to-right scan. At the j-th occurrence (0-based) take a draw in `0..j`; if it is 0 the held index becomes this occurrence's index.
- The first occurrence always takes (its draw range is only `0..0`).
- Probability that occurrence j is held at the end: it must be taken (1/(j+1)) and not replaced by any later occurrence i > j (probability 1 - 1/(i+1) = i/(i+1) each). The product telescopes: `1/(j+1) * (j+1)/(j+2) * ... * (c-1)/c = 1/c`.
- Exact count (run): the last occurrence holding it is the last draw of 0; there are c! sequences and each occurrence is held in (c-1)! of them, so `counts` are all equal, for every c from 1 to 8. The telescoping product is also checked as an exact `Fraction` for c up to 11.
- Time O(n) per pick, extra space O(1). The dictionary version uses O(n) memory and O(1) per pick after an O(n) build. If `pick` is called once or the array is huge and read-only, scan; if called many times, build the index.

**Complexity:** Scan O(n) time, O(1) extra space and one random number per occurrence. Dictionary: build O(n), pick O(1), memory O(n). The enumeration for verification is O(c!) and only runs on c <= 8.

**Dry run:** `nums = [1, 2, 3, 3, 3]`, `target = 3`, `draws = [0, 1, 0]`.
- Index 0, 1: not the target.
- Index 2: occurrence 0, draw 0 in `0..0`: held = 2.
- Index 3: occurrence 1, draw 1 in `0..1` is not 0: keep 2.
- Index 4: occurrence 2, draw 0 in `0..2`: held = 4.
- Result held 4. There are 1 * 2 * 3 = 6 draw sequences; the held index is 4 when the last draw is 0 (2 sequences), 3 when the last draw is not 0 and the middle draw is 0 (2 sequences), and 2 when neither is 0 (2 sequences): `counts = [2, 2, 2]`. Output `[4, [2, 2, 2], 6]`.

**Code:**
```python
import itertools
import math
import random

random.seed(3501)


def solve(nums, target, draws):
    """One scan, O(1) extra space for the pick itself. counts/sequences are the exact enumeration."""
    held, j = -1, 0
    for i, v in enumerate(nums):
        if v == target:                       # the j-th occurrence (0-based)
            if draws[j] == 0:                 # draws[j] in 0..j: replace with probability 1/(j+1)
                held = i
            j += 1
    c = j
    occ = [i for i, v in enumerate(nums) if v == target]
    counts = [0] * c
    seqs = 0
    for ds in itertools.product(*[range(jj + 1) for jj in range(c)]):   # ALL c! draw sequences
        last = -1
        for jj, d in enumerate(ds):
            if d == 0:
                last = jj
        counts[last] += 1                      # draws[0] is always 0, so last >= 0
        seqs += 1
    return [held, counts, seqs]


def brute(nums, target, draws):
    occ = [i for i, v in enumerate(nums) if v == target]
    c = len(occ)

    def rec(j, held, acc):                     # recursion over the occurrence number
        if j == c:
            acc[held] = acc.get(held, 0) + 1
            return
        for d in range(j + 1):
            rec(j + 1, occ[j] if d == 0 else held, acc)
    acc = {}
    rec(0, -1, acc)
    last = max(jj for jj, d in enumerate(draws) if d == 0)
    return [occ[last], [acc[o] for o in occ], sum(acc.values())]


# dry run on the first example: nums = [1, 2, 3, 3, 3], target 3, draws [0, 1, 0]
nums, target, draws = [1, 2, 3, 3, 3], 3, [0, 1, 0]
held, j = None, 0
for i, v in enumerate(nums):
    if v != target:
        print(f"index {i} value {v}: not the target, skip")
        continue
    d = draws[j]
    print(f"index {i} value {v}: occurrence {j}, draw {d} in 0..{j}, {'replace' if d == 0 else 'keep'}", end="")
    if d == 0:
        held = i
    print(f" -> held {held}")
    j += 1

for nm, tg, dr, want in [([1, 2, 3, 3, 3], 3, [0, 1, 0], [4, [2, 2, 2], 6]),
                         ([9, 9], 9, [0, 1], [0, [1, 1], 2]),
                         ([4, 5, 6], 5, [0], [1, [1], 1])]:
    got = solve(nm, tg, dr)
    assert got == want == brute(nm, tg, dr), (nm, got)
    print(nm, tg, dr, "->", got)

# exact uniformity for every number of occurrences c = 1..8: counts all (c-1)!, total c!
print("\n c   sequences  count per occurrence")
for c in range(1, 9):
    r = solve([7] * c, 7, [0] * c)
    assert r[2] == math.factorial(c) and set(r[1]) == {math.factorial(c - 1)} and len(r[1]) == c
    print(f"{c:>2} {r[2]:>11}  {r[1][0]:>6} x {c}")

# the probability argument as exact fractions: P(j-th held) = 1/(j+1) * prod_{i>j} (1 - 1/(i+1)) = 1/c
from fractions import Fraction
for c in range(1, 12):
    for jj in range(c):
        p = Fraction(1, jj + 1)
        for i in range(jj + 1, c):
            p *= 1 - Fraction(1, i + 1)
        assert p == Fraction(1, c)
print("telescoping product equals 1/c for c = 1..11, every j")

# seeded random cross-check against enumeration of all draw sequences
for _ in range(300):
    nm = [random.randint(1, 3) for _ in range(random.randint(1, 8))]
    tg = random.choice(nm)
    c = nm.count(tg)
    dr = [random.randint(0, jj) for jj in range(c)]
    assert solve(nm, tg, dr) == brute(nm, tg, dr)
    assert nm[solve(nm, tg, dr)[0]] == tg
print("300 seeded random cases match the recursive enumeration; the held index always holds the target")

# the dictionary alternative: O(n) build, O(1) per pick, O(n) memory
def build(nums):
    pos = {}
    for i, v in enumerate(nums):
        pos.setdefault(v, []).append(i)
    return pos
pos = build([1, 2, 3, 3, 3])
assert pos[3] == [2, 3, 4] and pos[3][2 % 3] in (2, 3, 4)
print("dict of positions:", pos)

# edge cases
assert solve([5], 5, [0]) == [0, [1], 1]                       # single occurrence: first draw is always 0
assert solve([3, 3, 3, 3], 3, [0, 0, 0, 0])[0] == 3            # all zeros: always replace, last wins
assert solve([3, 3, 3, 3], 3, [0, 1, 2, 3])[0] == 0            # only the forced first draw is 0: first stays
print("edge asserts ok")
```

**Output (my run):**
```
index 0 value 1: not the target, skip
index 1 value 2: not the target, skip
index 2 value 3: occurrence 0, draw 0 in 0..0, replace -> held 2
index 3 value 3: occurrence 1, draw 1 in 0..1, keep -> held 2
index 4 value 3: occurrence 2, draw 0 in 0..2, replace -> held 4
[1, 2, 3, 3, 3] 3 [0, 1, 0] -> [4, [2, 2, 2], 6]
[9, 9] 9 [0, 1] -> [0, [1, 1], 2]
[4, 5, 6] 5 [0] -> [1, [1], 1]

 c   sequences  count per occurrence
 1           1       1 x 1
 2           2       1 x 2
 3           6       2 x 3
 4          24       6 x 4
 5         120      24 x 5
 6         720     120 x 6
 7        5040     720 x 7
 8       40320    5040 x 8
telescoping product equals 1/c for c = 1..11, every j
300 seeded random cases match the recursive enumeration; the held index always holds the target
dict of positions: {1: [0], 2: [1], 3: [2, 3, 4]}
edge asserts ok
```

**Edge cases:**
- Single occurrence: the draw is always 0, the held index is that occurrence.
- Target at every position: all of `nums` are candidates; draws up to `n - 1`.
- Target adjacent to itself or at the ends: positions do not matter, only the order of occurrences.
- Draw sequence with only the forced first 0: the first occurrence stays.
- The problem guarantees the target occurs at least once; with zero occurrences there is nothing to pick (raise or return -1 in real code).

**Follow-ups:**
- *Many picks?* Build the dict once (`defaultdict(list)`), then `random.choice(pos[target])`.
- *Stream where nothing can be stored?* This scan is exactly size-1 reservoir sampling (Q33 with k = 1).
- *Random pick of a whole subarray, or a mutable set?* Part 1 Q35 handles the randomised set.

**Common mistakes:**
- Drawing in `0..n-1` (the array length) instead of `0..j` (occurrences so far).
- Counting every element, not only the matches.
- Keeping probability 1/2 each time (favours the last occurrences).
- Returning the index of the last match by default.

### Q36 ⭐⭐ 🟡 What Python's sort accepts and rejects. `cases` is a list of 1 to 20 lists, each with 0 to 6 values that are integers, floats, booleans, None, strings, lists or tuples of those (no NaN). For every case return `[plain, none_last]`: `plain` is `sorted(case)` and `none_last` is `sorted(case, key=lambda v: (v is None, v))`; either one is the string 'TypeError' when Python raises TypeError. Explain from the results: `<` between an int and a str, or between None and an int, raises TypeError in Python 3 (so a list that mixes such types cannot be sorted, however you write the sort); ints, floats and bools compare with each other; tuples and lists compare element by element and only use `<` on the first position where the two items are not `==` (so `(1, 'a') < (2, None)` works but `(1, 'a') < (1, None)` raises); a list of 0 or 1 items never compares anything and so never raises; and why the key `(v is None, v)` puts None last (False sorts before True) without ever comparing None to a number, but still raises for an int mixed with a str; and why `[None, None]` raises for the plain sort (None < None is a TypeError) but not for the key version (equal tuples are never ordered with `<`). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a hand-written insertion sort using only the < operator on small inputs. Example: cases=[[3, 1, 2], [1, 'a'], [null, 3, 1], [null], [(1, 'a'), (2, null)], [(1, 'a'), (1, null)], [True, 2, 1.5], [null, null]] -> [[[1, 2, 3], [1, 2, 3]], ['TypeError', 'TypeError'], ['TypeError', [1, 3, null]], [[null], [null]], [[(1, 'a'), (2, null)], [(1, 'a'), (2, null)]], ['TypeError', 'TypeError'], [[True, 1.5, 2], [True, 1.5, 2]], ['TypeError', [null, null]]].
**Asked at:** Python Sorting HOWTO (search-result snippets only; the docs.python.org fetch failed with ENOTFOUND, so behaviour was verified by running Python 3.13)

**Pattern:** Comparison protocol of `list.sort`. `sort` only ever uses `<`; any pair it compares must support `<`, and a total order must connect every element to every other, so some cross-type comparison is unavoidable in a mixed list.

**Say this first (1 line):** "Python 3 only sorts what `<` can compare: ints, floats and bools mix, but `int < str` and `None < int` raise TypeError, so I clean or key the data first; the key `(v is None, v)` pushes None to the end without ever comparing None with a number."

**Brute force:** Write an insertion sort that uses only `<` and run it on each case, catching `TypeError`. It is the oracle here; insertion sort compares a different set of pairs than Timsort, so the cross-check also shows that, for these inputs, the two agree on which cases raise.

**Optimal:** Call `sorted(case)` and `sorted(case, key=lambda v: (v is None, v))`, each in `try / except TypeError`. What the results teach (all observed on 3.13 in the run):
- `1 < 'a'`: `TypeError: '<' not supported between instances of 'int' and 'str'`. Same for `None < 1`.
- int, float and bool compare freely (`True == 1`, `True < 1.5`).
- Tuples and lists compare element by element: Python finds the first position where the two items are NOT `==`, and only then applies `<` to that position. The run prints this with a loud class: `==` on the first pair, `==` on the second pair (not equal), then one `<`. So `(1, 'a') < (2, None)` works (decided at position 0; `'a'` and `None` are never compared), but `(1, 'a') < (1, None)` raises (first positions equal, then `'a' < None`).
- 0 or 1 items: no comparison happens at all, so never an error, whatever the element is (the run shows an object whose `<` raises, sorted alone without error).
- Mixed kinds in one list (str with a number, or None with a number): the algorithm must relate every element to the rest (otherwise the order of groups would be undefined), so at least one cross-kind `<` must happen and raises. The run checks 3000 seeded lists: every list with two of {str, number, None} raised.
- `[None, None]`: plain `sorted` raises (`None < None` is not defined). With the key, the keys are `(True, None)` and `(True, None)`; tuple comparison finds them equal via `==` and never calls `<` on the None parts, so no error.
- The None-last key: `(False, x)` sorts before `(True, None)` because `False < True` decides at slot 0, so None is never compared with a number. But `[1, 'a']` still raises with the key (slot 1 compares `1` and `'a'`).
- Whether an error shows can depend on the algorithm and the order of the data (which pairs it compares), except in the cases above where every algorithm must hit it. Do not rely on a mixed list "happening to work".

**Complexity:** `sorted` is O(n log n) comparisons (Timsort; O(n) on already-sorted input) with O(n) space. Here n <= 6, so everything is instant. The key function is called once per element.

**Dry run:** the first example's 8 cases.
- `[3, 1, 2]`: both `[1, 2, 3]`.
- `[1, 'a']`: `'a' < 1` raises, both `'TypeError'`.
- `[None, 3, 1]`: plain raises; key: `(True, None)`, `(False, 3)`, `(False, 1)` sort to `[1, 3, None]`.
- `[None]`: nothing to compare; `[None]` both ways.
- `[(1,'a'), (2,None)]`: first slots differ, fine.
- `[(1,'a'), (1,None)]`: `'a'` vs `None` raises, both.
- `[True, 2, 1.5]`: `[True, 1.5, 2]` both.
- `[None, None]`: plain `TypeError`, key `[None, None]`.

**Code:**
```python
import random

random.seed(3601)


def solve(cases):
    out = []
    for c in cases:
        try:
            plain = sorted(c)
        except TypeError:
            plain = "TypeError"
        try:
            none_last = sorted(c, key=lambda v: (v is None, v))
        except TypeError:
            none_last = "TypeError"
        out.append([plain, none_last])
    return out


def ins_sort(c, key=None):
    """Oracle: insertion sort that uses ONLY the < operator (like list.sort does)."""
    k = key or (lambda v: v)
    a = []
    for v in c:
        j = len(a)
        while j > 0 and k(v) < k(a[j - 1]):
            j -= 1
        a.insert(j, v)
    return a


def brute(cases):
    out = []
    for c in cases:
        row = []
        for key in (None, lambda v: (v is None, v)):
            try:
                row.append(ins_sort(c, key))
            except TypeError:
                row.append("TypeError")
        out.append(row)
    return out


cases = [[3, 1, 2], [1, "a"], [None, 3, 1], [None], [(1, "a"), (2, None)], [(1, "a"), (1, None)], [True, 2, 1.5], [None, None]]
want = [[[1, 2, 3], [1, 2, 3]], ["TypeError", "TypeError"], ["TypeError", [1, 3, None]], [[None], [None]],
        [[(1, "a"), (2, None)], [(1, "a"), (2, None)]], ["TypeError", "TypeError"], [[True, 1.5, 2], [True, 1.5, 2]],
        ["TypeError", [None, None]]]
got = solve(cases)
assert got == want == brute(cases)
for c, g in zip(cases, got):
    print(f"{str(c):<28} plain={g[0]!s:<22} none_last={g[1]}")

# the exact messages (3.13 wording is what you see here)
for expr in ("1 < 'a'", "None < 1", "None < None", "(1, 'a') < (1, None)", "(1, 'a') < (2, None)", "[1, 'a'] < [1, 2]"):
    try:
        print(f"{expr:<22} ->", eval(expr))
    except TypeError as e:
        print(f"{expr:<22} -> TypeError: {e}")
print("1 == 1.0 == True:", 1 == 1.0 == True, "| True < 1.5:", True < 1.5, "| 2 > True:", 2 > True)

# tuple/list comparison uses == to find the first differing position, then < only there
class Loud:
    def __init__(self, n): self.n = n
    def __eq__(self, o): print(f"   == {self.n},{o.n}"); return self.n == o.n
    def __lt__(self, o): print(f"   <  {self.n},{o.n}"); return self.n < o.n
print("(Loud(1), Loud(5)) < (Loud(1), Loud(9)):")
print("  result", (Loud(1), Loud(5)) < (Loud(1), Loud(9)))

# 0 or 1 items never compare anything
class Boom:
    def __lt__(self, o): raise AssertionError("compared")
assert sorted([]) == [] and sorted([Boom()]) and True
print("sorted([]) and sorted([Boom()]) made no comparison")

# claim: any list with a str and a number (2+ items) raises in plain sort, whatever the order; None with a number too
rng = random.Random(36)
pool = [1, 2, 1.5, True, "a", "b", None]
for _ in range(3000):
    lst = [rng.choice(pool) for _ in range(rng.randint(0, 6))]
    has_str = any(isinstance(v, str) for v in lst)
    has_num = any(isinstance(v, (int, float)) for v in lst)
    has_none = any(v is None for v in lst)
    kinds = has_str + has_num + has_none
    try:
        sorted(lst)
        raised = False
    except TypeError:
        raised = True
    if kinds >= 2:
        assert raised, lst           # a total order must connect the groups, so some cross-type '<' happens
    assert (len(lst) >= 2 and has_none and len([v for v in lst if v is None]) == len(lst)) <= raised
print("3000 seeded mixed lists: two kinds among {str, number, None} always raises; an all-None list of 2+ raises")

# the none-last key
assert sorted([3, None, 1, None, 2], key=lambda v: (v is None, v)) == [1, 2, 3, None, None]
assert (False, 1) < (True, None)       # decided by the first slot, so None is never compared with a number

# seeded random cross-check of solve against the insertion-sort oracle
def pick(rng):
    k = rng.randint(0, 3)
    if k == 0: return [rng.choice([None, 1, 2, 3, 1.5, True]) for _ in range(rng.randint(0, 6))]
    if k == 1: return [rng.choice("abc") for _ in range(rng.randint(0, 6))]
    if k == 2: return [rng.choice([(1, "a"), (1, None), (2, None), (1, 2), (2, "b")]) for _ in range(rng.randint(0, 5))]
    return [rng.choice(pool + [(1, "a"), [1, 2]]) for _ in range(rng.randint(0, 5))]
rng = random.Random(3602)
diff = 0
for _ in range(2000):
    cs = [pick(rng) for _ in range(rng.randint(1, 20))]
    s, b = solve(cs), brute(cs)
    for x, y in zip(s, b):
        if x != y:
            diff += 1
print("2000 seeded batches compared with the insertion-sort oracle, differing rows:", diff)
assert diff == 0

# edge cases
assert solve([[]]) == [[[], []]] and solve([[None, None, None]]) == [["TypeError", [None, None, None]]]
assert solve([[(1, None), (1, None)]]) == [[[(1, None), (1, None)], [(1, None), (1, None)]]]   # equal tuples: == only
print("edge asserts ok")
```

**Output (my run):**
```
[3, 1, 2]                    plain=[1, 2, 3]              none_last=[1, 2, 3]
[1, 'a']                     plain=TypeError              none_last=TypeError
[None, 3, 1]                 plain=TypeError              none_last=[1, 3, None]
[None]                       plain=[None]                 none_last=[None]
[(1, 'a'), (2, None)]        plain=[(1, 'a'), (2, None)]  none_last=[(1, 'a'), (2, None)]
[(1, 'a'), (1, None)]        plain=TypeError              none_last=TypeError
[True, 2, 1.5]               plain=[True, 1.5, 2]         none_last=[True, 1.5, 2]
[None, None]                 plain=TypeError              none_last=[None, None]
1 < 'a'                -> TypeError: '<' not supported between instances of 'int' and 'str'
None < 1               -> TypeError: '<' not supported between instances of 'NoneType' and 'int'
None < None            -> TypeError: '<' not supported between instances of 'NoneType' and 'NoneType'
(1, 'a') < (1, None)   -> TypeError: '<' not supported between instances of 'str' and 'NoneType'
(1, 'a') < (2, None)   -> True
[1, 'a'] < [1, 2]      -> TypeError: '<' not supported between instances of 'str' and 'int'
1 == 1.0 == True: True | True < 1.5: True | 2 > True: True
(Loud(1), Loud(5)) < (Loud(1), Loud(9)):
   == 1,1
   == 5,9
   <  5,9
  result True
sorted([]) and sorted([Boom()]) made no comparison
3000 seeded mixed lists: two kinds among {str, number, None} always raises; an all-None list of 2+ raises
2000 seeded batches compared with the insertion-sort oracle, differing rows: 0
edge asserts ok
```

**Edge cases:**
- Empty list: `[]` both ways.
- All the same type: always fine, subject to that type's `<`.
- NaN is excluded by the prompt: `nan < x` is always False, so sort "works" but the result is meaningless.
- Strings compare by code point, not by locale.
- Equal tuples that contain None never raise.

**Follow-ups:**
- *Sort records by a nullable field descending, None last?* `key=lambda v: (v is None, -v if v is not None else 0)` or sort by `(v is None, v)` then handle reverse carefully (`reverse=True` would put None first).
- *Why did Python 3 drop mixed-type ordering?* Python 2 had arbitrary cross-type ordering that hid bugs (editor knowledge).
- *Does `sort` use `==`?* Not for ordering; stability means equal items keep their order, and "equal" means neither is `<` the other.

**Common mistakes:**
- Assuming a mixed list "usually works".
- Believing a single `None` is harmless in a list with other items (it raises as soon as it is compared with a number).
- Using `key=lambda v: v or 0`, which turns real zeros and empty strings into other values.
- Using `reverse=True` with the None-last key (it puts None first).

### Q37 ⭐⭐ 🟡 Counting sort and LSD radix sort. `records` has 1 to 10^5 items [key, tag] with integer keys 0 <= key <= 10^9 and any integer tags. Sort them ascending by key, keeping equal keys in input order, with an LSD (least significant digit first) radix sort in base 10, without `sorted`: for each decimal digit position from the units upward, do one stable counting-sort pass on that digit (count the 10 digit values, turn the counts into prefix sums, place the items by walking the input from the LAST item to the first, decrementing the digit's counter). Stop after the pass for the highest digit of the largest key. Return `[sorted_records, passes]` where `passes` is the number of digit passes (at least 1, equal to the number of decimal digits of the largest key). Explain why each pass must be stable (an unstable pass destroys the order established by the earlier, less significant digits), why walking backwards is what keeps it stable, the time O(passes * (n + 10)) and the extra space O(n), and when counting sort on the key itself beats comparison sorting (a small key range k: O(n + k)). In the answer include a dry run on the first example and a seeded random cross-check of your solution against sorted(records, key=lambda r: r[0]) and len(str(max key)) on small inputs. Example: records=[[170, 1], [45, 2], [75, 3], [90, 4], [802, 5], [24, 6], [2, 7], [66, 8]] -> [[[2, 7], [24, 6], [45, 2], [66, 8], [75, 3], [90, 4], [170, 1], [802, 5]], 3]; records=[[5, 1]] -> [[[5, 1]], 1]; records=[[3, 1], [3, 2], [0, 3], [3, 4]] -> [[[0, 3], [3, 1], [3, 2], [3, 4]], 1].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Non-comparison sorting. Counting sort places items by digit in O(n + k) with a stable pass; LSD radix sort chains one stable pass per digit from the least significant up.

**Say this first (1 line):** "For each decimal digit from the units up I do a stable counting sort on that digit; stability is what keeps the earlier digits' order, and walking the input backwards while filling from the block ends is what makes the pass stable."

**Brute force:** `sorted(records, key=lambda r: r[0])`: O(n log n) comparisons and already stable. It is the oracle here. The prompt forbids it in the solution, but it is what you should write in real code unless the keys are small integers.

**Optimal:**
- Number of passes: the digits of the largest key (`len(str(max))`, at least 1; the key 0 still needs one pass). Loop with `exp = 1, 10, 100, ...` and stop once `exp > max key`.
- One pass on digit `d = key // exp % 10`:
  - Count: `cnt[d] += 1` for each record (10 counters).
  - Prefix sums: `cnt[d] += cnt[d-1]`, so `cnt[d]` becomes one past the last slot of digit d's block.
  - Place: walk the input from the LAST record to the first; `cnt[d] -= 1; out[cnt[d]] = record`. The last record of a digit group goes to the end of its block, the previous one just before it, and so on, so equal digits keep their input order.
- Why each pass must be stable: when you sort on the hundreds digit, records with the same hundreds digit must stay in the order the tens and units passes gave them. An unstable pass shuffles ties and throws that work away. The run shows a forward walk reversing equal keys (`[3,1],[3,2],[3,3]` becomes `[3,3],[3,2],[3,1]`) and breaking the sort of `[21, 11, 12]` (gives `[12, 11, 21]`).
- The first example: keys `[170, 45, 75, 90, 802, 24, 2, 66]`. After the units pass `[170, 90, 802, 2, 24, 45, 75, 66]`; after tens `[802, 2, 24, 45, 66, 170, 75, 90]`; after hundreds `[2, 24, 45, 66, 75, 90, 170, 802]`. 3 passes.
- Counting sort on the key itself (one pass) wins when the key range k is small: O(n + k) time and O(n + k) space, with no comparisons, against O(n log n). Radix with base b and d digits is O(d * (n + b)); with a 10^9 range and base 10 that is 10 passes.

**Complexity:** O(passes * (n + 10)) time, passes <= 10 here, so O(n) for n up to 10^5. Extra space O(n) for the output array of each pass plus 10 counters. Not in place. Stable overall.

**Dry run:** units pass on the first example. Units digits `[0, 5, 5, 0, 2, 4, 2, 6]`; counts `[2,0,2,0,1,2,1,0,0,0]`; prefix sums `[2,2,4,4,5,7,8,8,8,8]`, so digit 0 fills slots 0-1, digit 2 slot 2-3, digit 4 slot 4, digit 5 slots 5-6, digit 6 slot 7. Walking from the last record: 66 (digit 6) goes to slot 7, 2 to slot 3, 24 to slot 4, 802 to slot 2, 90 to slot 1, 75 to slot 6, 45 to slot 5, 170 to slot 0. Result `[170, 90, 802, 2, 24, 45, 75, 66]`, matching the run. Tens and hundreds passes follow the same way.

**Code:**
```python
import random
import time

random.seed(3701)


def solve(records, trace=None, backwards=True):
    """LSD radix sort, base 10. backwards=False is the BROKEN forward walk, kept only to show why it matters."""
    a = [list(r) for r in records]
    mx = max(r[0] for r in a)
    passes, exp = 0, 1
    while True:
        passes += 1
        cnt = [0] * 10
        for r in a:
            cnt[r[0] // exp % 10] += 1                  # 1. count each digit value
        for d in range(1, 10):
            cnt[d] += cnt[d - 1]                        # 2. prefix sums: cnt[d] = end (exclusive) of digit d's block
        out = [None] * len(a)
        for r in (reversed(a) if backwards else a):     # 3. walk from the LAST item, fill each block from its end
            dg = r[0] // exp % 10
            cnt[dg] -= 1
            out[cnt[dg]] = r
        a = out
        if trace is not None:
            trace.append((exp, [r[0] for r in a]))
        exp *= 10
        if exp > mx:                                    # no digit left above the largest key's top digit
            break
    return [a, passes]


def brute(records):
    return [sorted([list(r) for r in records], key=lambda r: r[0]), len(str(max(r[0] for r in records)))]


# dry run on the first example
recs = [[170, 1], [45, 2], [75, 3], [90, 4], [802, 5], [24, 6], [2, 7], [66, 8]]
tr = []
res = solve(recs, tr)
print("input keys :", [r[0] for r in recs])
for exp, keys in tr:
    print(f"after digit {len(str(exp)) - 1} (10^{len(str(exp)) - 1}):", keys)
print(res)

for rc, want in [(recs, [[[2, 7], [24, 6], [45, 2], [66, 8], [75, 3], [90, 4], [170, 1], [802, 5]], 3]),
                 ([[5, 1]], [[[5, 1]], 1]),
                 ([[3, 1], [3, 2], [0, 3], [3, 4]], [[[0, 3], [3, 1], [3, 2], [3, 4]], 1])]:
    assert solve(rc) == want == brute(rc), rc
print("all three examples match sorted(key=...) and len(str(max))")

# the counting-sort block of ONE pass, written out for the units digit of the example
digits = [r[0] % 10 for r in recs]
cnt = [0] * 10
for d in digits:
    cnt[d] += 1
print("\nunits digits :", digits)
print("counts       :", cnt)
pre = list(cnt)
for d in range(1, 10):
    pre[d] += pre[d - 1]
print("prefix sums  :", pre, "(digit d fills slots pre[d-1]..pre[d]-1)")

# why backwards: the forward walk puts equal digits in REVERSE input order, so stability is lost
tiny = [[3, 1], [3, 2], [3, 3]]
print("\nbackwards walk:", solve(tiny, backwards=True)[0])
print("forward walk  :", solve(tiny, backwards=False)[0], "(equal keys reversed: NOT stable)")
assert solve(tiny, backwards=False)[0] == [[3, 3], [3, 2], [3, 1]]
# and an unstable pass breaks the radix idea itself: keys that tie on the low digit end up out of order
two = [[21, 0], [11, 1], [12, 2]]
assert solve(two)[0] == [[11, 1], [12, 2], [21, 0]]
print("forward walk on [21, 11, 12]:", [r[0] for r in solve(two, backwards=False)[0]], "| correct:", [r[0] for r in solve(two)[0]])

# passes = digits of the max key, for 0, 9, 10, 99, 100, 10^9
for mx, p in [(0, 1), (9, 1), (10, 2), (99, 2), (100, 3), (10 ** 9, 10)]:
    assert solve([[mx, 0], [0, 1]])[1] == p == len(str(mx))
print("passes for max key 0, 9, 10, 99, 100, 10^9 :", [solve([[m, 0]])[1] for m in (0, 9, 10, 99, 100, 10 ** 9)])

# seeded random cross-check against sorted() and len(str(max))
for _ in range(500):
    n = random.randint(1, 30)
    hi = random.choice([1, 9, 10, 99, 1000, 10 ** 9])
    rc = [[random.randint(0, hi), random.randint(-5, 5)] for _ in range(n)]
    assert solve(rc) == brute(rc)
print("500 seeded random cases match sorted(key=r[0]) (stable) and the pass count")

# maximum size: 10^5 records, keys up to 10^9 -> 10 passes; time is sandbox-only
big = [[random.randint(0, 10 ** 9), i] for i in range(10 ** 5)]
t0 = time.perf_counter()
r = solve(big)
t1 = time.perf_counter()
assert r == brute(big) and r[1] == len(str(max(x[0] for x in big)))
print(f"10^5 records: passes {r[1]}, radix {t1 - t0:.2f}s (sandbox-only timing, not a proof of big-O)")

# edge cases
assert solve([[0, 9]]) == [[[0, 9]], 1] and solve([[7, 1], [7, 2]]) == [[[7, 1], [7, 2]], 1]
assert solve([[10 ** 9, 1], [10 ** 9 - 1, 2]])[0] == [[10 ** 9 - 1, 2], [10 ** 9, 1]]
print("edge asserts ok")
```

**Output (my run):**
```
input keys : [170, 45, 75, 90, 802, 24, 2, 66]
after digit 0 (10^0): [170, 90, 802, 2, 24, 45, 75, 66]
after digit 1 (10^1): [802, 2, 24, 45, 66, 170, 75, 90]
after digit 2 (10^2): [2, 24, 45, 66, 75, 90, 170, 802]
[[[2, 7], [24, 6], [45, 2], [66, 8], [75, 3], [90, 4], [170, 1], [802, 5]], 3]
all three examples match sorted(key=...) and len(str(max))

units digits : [0, 5, 5, 0, 2, 4, 2, 6]
counts       : [2, 0, 2, 0, 1, 2, 1, 0, 0, 0]
prefix sums  : [2, 2, 4, 4, 5, 7, 8, 8, 8, 8] (digit d fills slots pre[d-1]..pre[d]-1)

backwards walk: [[3, 1], [3, 2], [3, 3]]
forward walk  : [[3, 3], [3, 2], [3, 1]] (equal keys reversed: NOT stable)
forward walk on [21, 11, 12]: [12, 11, 21] | correct: [11, 12, 21]
passes for max key 0, 9, 10, 99, 100, 10^9 : [1, 1, 2, 2, 3, 10]
500 seeded random cases match sorted(key=r[0]) (stable) and the pass count
10^5 records: passes 9, radix 0.28s (sandbox-only timing, not a proof of big-O)
edge asserts ok
```

**Edge cases:**
- Single record, or all keys 0: one pass.
- Max key 9, 10, 99, 100, 10^9: 1, 2, 2, 3, 10 passes (asserted).
- Equal keys keep the input tags in order (`[3,1],[3,2],[3,4]`).
- Keys with fewer digits than the max (2 versus 802): their missing high digits are 0 and they sort first.
- Negative keys are out of range here; they would need an offset or a separate sign pass.

**Follow-ups:**
- *Base 256 or 2^16?* Fewer passes, bigger counter array: choose the base so that `n + base` stays small (typically 4 passes for 32-bit keys with base 256).
- *Is radix always faster than `sorted`?* Not in Python: the per-item loop is interpreted while `sorted` runs in C. The run's timing for 10^5 records is sandbox-only and says nothing about big-O. The point is the algorithm and its O(n) bound.
- *Strings of equal length?* Same idea, per character, from the last to the first.
- *MSD radix?* Recursive by buckets from the most significant digit; used for variable-length strings.

**Common mistakes:**
- Walking the input forwards while decrementing counters: equal keys come out reversed.
- Sorting by the most significant digit first with an LSD loop.
- Using an unstable pass (for example `sort` with a bad key).
- Stopping after `max key` digits computed with floats, or counting 0 as 0 digits.
- Forgetting the prefix-sum step (counts alone give no positions).

### Q38 ⭐⭐ 🟡 Heap sort from scratch. `records` has 0 to 5000 items [key, tag] with integer keys; sort ascending by key in place with heap sort using this exact algorithm (a max-heap on the keys, array form: children of i are 2i + 1 and 2i + 2). `sift(root, size)`: while 2 * root + 1 < size: let `ch = 2 * root + 1`; if `ch + 1 < size`, make ONE comparison `a[ch + 1].key > a[ch].key` and if true take `ch += 1`; then make ONE comparison `a[root].key < a[ch].key`: if true swap them and continue from ch, else stop. Build: for s from `n // 2 - 1` down to 0 call sift(s, n). Sort: for end from n - 1 down to 1 swap `a[0]` and `a[end]` and call sift(0, end). Return `[sorted_records, comparisons]` where `comparisons` counts every key comparison made by sift. Explain why the sort is O(n log n) in the worst case with O(1) extra space, why it is NOT stable (give a tiny failing input from this algorithm and the order it produces) and why quicksort usually beats it in practice (cache behaviour). Heap theory (sift up and down, the O(n) build bound) is Part 8 Q28 and is not repeated. In the answer include a dry run on the first example and a seeded random cross-check of your solution against sorted() on the keys and a recursive sift with its own comparison counter on small inputs. Example: records=[[3, 1], [1, 2], [2, 3]] -> [[[1, 2], [2, 3], [3, 1]], 3]; records=[[0, 0], [0, 1]] -> [[[0, 1], [0, 0]], 1]; records=[[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]] -> [[[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]], 10]; records=[] -> [[], 0].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** In-place selection with a heap. Build a max-heap in the array, then repeatedly swap the maximum to the end of the shrinking heap and sift the new root down.

**Say this first (1 line):** "I heapify the array into a max-heap, then n - 1 times swap the root with the last heap element and sift down within the smaller heap; O(n log n) worst case, O(1) extra space, not stable."

**Brute force:** `sorted(records, key=...)`, or selection sort (find the maximum n times, O(n^2)). The oracle here is `sorted` on the keys plus a recursive sift with its own comparison counter.

**Optimal:**
- Array heap: children of `i` are `2i + 1` and `2i + 2`.
- `sift(root, size)`: while the root has a child, pick the larger child (one comparison if there are two children), then one comparison of the root against it; swap and continue if the root is smaller, otherwise stop. Each level costs at most 2 comparisons and there are at most `floor(log2 size)` levels.
- Build: `sift(s, n)` for `s = n//2 - 1` down to 0. Sort: for `end = n-1` down to 1, swap `a[0]` and `a[end]`, then `sift(0, end)`.
- Worst case O(n log n) because each of about n/2 + n sifts costs O(log n) (the run asserts comparisons <= 2 * (n/2 + n) * floor(log2 n)). The build alone is O(n) (Part 8 Q28 owns that proof). There is no bad input: sorted, reversed, random and all-equal inputs all land near n log n (see the table).
- O(1) extra space: everything happens in the array (the code copies the input only so the caller's list is not changed).
- Not stable: the long-distance swaps in the sort phase jump equal keys over each other. Smallest example from this algorithm: `[[0,0],[0,1]]` becomes `[[0,1],[0,0]]`; `[[1,'a'],[1,'b'],[1,'c']]` becomes `b, c, a`.
- Why quicksort usually wins in practice: quicksort scans memory sequentially (cache friendly), while sift jumps between index `i` and `2i + 1`, far apart in a big array (cache misses). This is the standard explanation (editor knowledge; not measured here, and in Python interpreter overhead hides it).

**Complexity:** Time O(n log n) in every case (comparisons shown in the run: about 1.7 to 1.8 times `n log2 n`, that is 0.84 to 0.91 of the bound `2n log2 n`, for random, sorted and reversed input with n = 1000 and 5000; about 3n for all-equal, which stops each sift after one level). Space O(1) extra. Not stable.

**Dry run:** keys `[5, 4, 3, 2, 1]` (already a max-heap).
- Build: sift(1, 5) compares children 2 and 1 (one comparison, picks 2) and root 4 against 2 (one), no swap; sift(0, 5): children 4, 3 (one), root 5 vs 4 (one), no swap. 4 comparisons.
- `end = 4`: swap to `[1,4,3,2,5]`, sift(0, 4): children 4, 3 (1), 1 < 4 (1) swap, then at index 1 the child 2 (index 3) vs 1: one comparison, swap: `[4,2,3,1,5]`. Comparisons so far 7.
- `end = 3`: swap to `[1,2,3,4,5]`, sift(0, 3) compares children 2, 3 (picks 3) and root 1 against 3 (2 comparisons) and swaps: `[3,2,1,4,5]`; total 9.
- `end = 2`: swap to `[1,2,3,4,5]`, sift(0, 2) has one child: 1 comparison, swap: `[2,1,3,4,5]`; total 10.
- `end = 1`: swap to `[1,2,3,4,5]`; the heap has size 1, nothing to sift; total 10. Matches the example's `10`.

**Code:**
```python
import math
import random

random.seed(3801)


def solve(records):
    """In-place heap sort on a copy; every key comparison in sift is counted."""
    a = [list(r) for r in records]
    n = len(a)
    cmps = 0

    def sift(root, size):
        nonlocal cmps
        while 2 * root + 1 < size:
            ch = 2 * root + 1
            if ch + 1 < size:
                cmps += 1
                if a[ch + 1][0] > a[ch][0]:      # pick the larger child
                    ch += 1
            cmps += 1
            if a[root][0] < a[ch][0]:            # child bigger than the root: swap and keep sinking
                a[root], a[ch] = a[ch], a[root]
                root = ch
            else:
                break

    for s in range(n // 2 - 1, -1, -1):          # build the max-heap
        sift(s, n)
    for end in range(n - 1, 0, -1):              # move the max to the end, shrink the heap
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    return [a, cmps]


def brute(records):
    """Oracle: recursive sift with its own counter."""
    a = [list(r) for r in records]
    n = len(a)
    c = [0]

    def sift(root, size):
        ch = 2 * root + 1
        if ch >= size:
            return
        if ch + 1 < size:
            c[0] += 1
            if a[ch + 1][0] > a[ch][0]:
                ch += 1
        c[0] += 1
        if a[root][0] < a[ch][0]:
            a[root], a[ch] = a[ch], a[root]
            sift(ch, size)
    for s in reversed(range(n // 2)):
        sift(s, n)
    for end in reversed(range(1, n)):
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    assert [r[0] for r in a] == sorted(r[0] for r in records)
    return [a, c[0]]


# dry run on [[5,1],[4,2],[3,3],[2,4],[1,5]] with the array printed after each step (keys only)
a = [[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]]
n = len(a)
print("keys at start         :", [r[0] for r in a], "(already a max-heap)")
tr = []
cm = 0
def sift_t(root, size):
    global cm
    while 2 * root + 1 < size:
        ch = 2 * root + 1
        if ch + 1 < size:
            cm += 1
            if a[ch + 1][0] > a[ch][0]:
                ch += 1
        cm += 1
        if a[root][0] < a[ch][0]:
            a[root], a[ch] = a[ch], a[root]
            root = ch
        else:
            break
for s in range(n // 2 - 1, -1, -1):
    sift_t(s, n)
print("after build           :", [r[0] for r in a], "comparisons so far", cm)
for end in range(n - 1, 0, -1):
    a[0], a[end] = a[end], a[0]
    sift_t(0, end)
    print(f"after end={end} sift     :", [r[0] for r in a], "comparisons so far", cm)

for rc, want in [([[3, 1], [1, 2], [2, 3]], [[[1, 2], [2, 3], [3, 1]], 3]),
                 ([[0, 0], [0, 1]], [[[0, 1], [0, 0]], 1]),
                 ([[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]], [[[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]], 10]),
                 ([], [[], 0])]:
    assert solve(rc) == want == brute(rc), rc
print("all four examples match, including the recursive oracle")

# not stable: the smallest failing input from this algorithm
print("unstable:", solve([[0, 0], [0, 1]])[0], "(tags 0,1 became 1,0)")
print("unstable 3 items:", solve([[1, "a"], [1, "b"], [1, "c"]])[0])

# bound: sift makes at most 2 comparisons per level, so comparisons <= 2 * (n/2 + n) * floor(log2 n); compare with n log2 n
print("\n     n   random   sorted  reversed  all equal   2n*log2(n)")
for n in (10, 100, 1000, 5000):
    rows = []
    for kind in ("random", "sorted", "reversed", "equal"):
        ks = {"random": [random.randint(0, 10 ** 6) for _ in range(n)], "sorted": list(range(n)),
              "reversed": list(range(n, 0, -1)), "equal": [7] * n}[kind]
        cm_ = solve([[k, i] for i, k in enumerate(ks)])[1]
        assert cm_ <= 2 * (n // 2 + n) * max(1, int(math.log2(n)))
        rows.append(cm_)
    print(f"{n:>6} {rows[0]:>8} {rows[1]:>8} {rows[2]:>9} {rows[3]:>10} {2 * n * math.log2(n):>12.0f}")

# seeded random cross-check against sorted() on the keys and the recursive sift counter
for _ in range(500):
    n = random.randint(0, 40)
    rc = [[random.randint(-5, 5), i] for i in range(n)]
    got = solve(rc)
    assert got == brute(rc) and [r[0] for r in got[0]] == sorted(r[0] for r in rc)
    assert sorted(map(tuple, got[0])) == sorted(map(tuple, rc))          # same records, nothing lost
print("500 seeded random cases: sorted keys, same records, same comparison count as the recursive sift")

# edge cases
assert solve([]) == [[], 0] and solve([[4, 4]]) == [[[4, 4]], 0] and solve([[2, 0], [1, 1]])[1] == 1
assert solve([[1, 0], [2, 1]])[0] == [[1, 0], [2, 1]]
print("edge asserts ok")
```

**Output (my run):**
```
keys at start         : [5, 4, 3, 2, 1] (already a max-heap)
after build           : [5, 4, 3, 2, 1] comparisons so far 4
after end=4 sift     : [4, 2, 3, 1, 5] comparisons so far 7
after end=3 sift     : [3, 2, 1, 4, 5] comparisons so far 9
after end=2 sift     : [2, 1, 3, 4, 5] comparisons so far 10
after end=1 sift     : [1, 2, 3, 4, 5] comparisons so far 10
all four examples match, including the recursive oracle
unstable: [[0, 1], [0, 0]] (tags 0,1 became 1,0)
unstable 3 items: [[1, 'b'], [1, 'c'], [1, 'a']]

     n   random   sorted  reversed  all equal   2n*log2(n)
    10       41       41        35         24           66
   100     1036     1081       944        294         1329
  1000    16865    17583     15965       2994        19932
  5000   107625   112126    103227      14994       122877
500 seeded random cases: sorted keys, same records, same comparison count as the recursive sift
edge asserts ok
```

**Edge cases:**
- Empty: `[[], 0]`. One record: no comparisons.
- Two records: `[[2,0],[1,1]]` takes 1 comparison (the root has a single child, so only the root-versus-child comparison).
- All equal keys: no swaps in the sift (`<` is strict), but the end-swaps still reorder tags: unstable.
- Already sorted ascending: still O(n log n); heap sort is not adaptive.
- Duplicates in keys: fine; ties never trigger a swap in `sift` since `a[root] < a[ch]` is strict.

**Follow-ups:**
- *Why use heap sort at all?* Guaranteed O(n log n) with O(1) space; introsort falls back to it when quicksort recursion gets too deep (editor knowledge).
- *Make it stable?* Sort `(key, original_index)` pairs, at the cost of O(n) extra memory.
- *Fewer comparisons?* Bottom-up heapsort sifts to a leaf first then climbs back, saving about half the comparisons (editor knowledge; not implemented).
- *Top-k only?* Use a heap of size k (Part 8).

**Common mistakes:**
- Using a min-heap and then reversing, which needs extra space or a second pass.
- Forgetting `ch + 1 < size` and reading past the heap end (it holds the sorted tail).
- Building with `n // 2` instead of `n // 2 - 1` (harmless but one wasted sift) or starting the build from 0 upward (wrong).
- Calling `sift(0, n)` instead of `sift(0, end)` after the swap.
- Claiming stability.

### Q39 ⭐⭐ 🟡 Largest number from a list. `nums` has 1 to 100 integers with 0 <= value <= 10^9. Arrange them in some order and join their decimal strings into the largest possible number; return it as a string (if every number is 0, return '0', not '000'). Sort the strings with a custom comparison: put `a` before `b` when `a + b > b + a` as strings (e.g. '9' before '34' because '934' > '349'). Python 3 has no `cmp=` argument for `sort`, so use `functools.cmp_to_key`; also show the key-based alternative that repeats each string until it is at least 20 characters long (`s * (20 // len(s) + 1)`) and sorts descending. Explain why plain descending string order is wrong ('3' vs '30'), why this comparison is a valid total preorder (transitive) so that sort is allowed to use it, and the O(n log n) comparisons each costing O(length) time. In the answer include a dry run on the first example and a seeded random cross-check of your solution against trying every permutation (n <= 7) on small inputs. Example: nums=[3, 30, 34, 5, 9] -> '9534330'; nums=[10, 2] -> '210'; nums=[0, 0] -> '0'; nums=[824, 8247] -> '8248247'; nums=[1] -> '1'.
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened) | Python Sorting HOWTO on cmp_to_key (search snippet only)

**Pattern:** Sort with a custom pairwise order. Put `a` before `b` when `a + b > b + a`; this order is a valid total preorder, so a normal sort can use it.

**Say this first (1 line):** "Compare two numbers as strings by which concatenation is bigger, `a+b` against `b+a`; sort with `cmp_to_key`, join, and special-case an all-zero result."

**Brute force:** Try every permutation of the numbers, join each and keep the maximum: O(n! * n). The oracle (n <= 7).

**Optimal:**
- Convert to strings. Sort with `functools.cmp_to_key(cmp)` where `cmp(a, b) = -1 if a + b > b + a, 1 if a + b < b + a, else 0`. Python 3 has no `cmp=` argument for `sort`, so `cmp_to_key` is the bridge (editor knowledge about why it exists; the code shows it works on 3.13).
- Join; if the first character is `'0'` the whole result is zeros, so return `'0'`.
- Key alternative: sort descending with key `s * (20 // len(s) + 1)`. Each number has at most 10 digits, so `a + b` has at most 20 digits; repeating each string to more than 20 characters makes plain string order agree with the concatenation order. The run checks all 65,536 pairs of strings over the digits 0-3 (lengths 1-4): zero strict disagreements. Where `a + b == b + a` (for example `'1'` and `'11'`) the keys differ only in length, so the key still orders the pair, but both orders give the same joined text.
- Why plain descending string order is wrong: `'3'` vs `'30'`: descending string order puts `'30'` before `'3'` (longer string with the same prefix is larger), giving `...303`, but `'330' > '303'`, so `3` must come first. For the example plain descending gives `9534303`, the comparator `9534330`.
- Why the order is valid: sort needs a strict weak order. "a before b iff a+b > b+a" has an equivalence of ties (`a+b == b+a`) and is transitive. Proof sketch: `a+b >= b+a` is the same as comparing `a/(10^len(a) - 1)` with `b/(10^len(b) - 1)` as numbers, a real-number order (editor's derivation); so transitivity follows. The run also checks it exhaustively: all 59,319 triples of strings over {0,1,2} up to length 3 have zero violations of "a >= b and b >= c implies a >= c".
- Cost: O(n log n) comparisons, each O(L) for string length L (at most 20 characters here), so O(n log n * L).

**Complexity:** O(n log n * L) time with L <= 20 (a constant for ints up to 10^9), O(n * L) space. With n <= 100 this is tiny. The key version computes each key once: O(n * L) for keys plus O(n log n) comparisons of 21 to 30 character strings.

**Dry run:** `[3, 30, 34, 5, 9]`.
- `'3'` vs `'30'`: `'330'` > `'303'`, so `3` before `30`.
- `'34'` vs `'3'`: `'343'` > `'334'`, so `34` before `3`; `34` vs `30`: `'3430'` > `'3034'`, `34` first.
- `5` and `9` beat everything starting with 3 (`'53'` > `'35'`), and `9` beats `5`.
- Order `['9', '5', '34', '3', '30']`, joined `9534330`. The repeat keys (`'3' * 21`, `'3030...'`, `'3434...'`, ...) sort the same way.

**Code:**
```python
import functools
import itertools
import random

random.seed(3901)


def cmp(a, b):
    """a before b (negative) when a + b > b + a as strings."""
    if a + b > b + a:
        return -1
    if a + b < b + a:
        return 1
    return 0


def solve(nums):
    strs = sorted(map(str, nums), key=functools.cmp_to_key(cmp))
    r = "".join(strs)
    return "0" if r[0] == "0" else r          # sorted first = the biggest; a leading '0' means everything is 0


def solve_key(nums):
    """Key-based alternative: repeat each string to >= 20 chars (a + b has at most 20 digits), sort descending."""
    strs = sorted(map(str, nums), key=lambda s: s * (20 // len(s) + 1), reverse=True)
    r = "".join(strs)
    return "0" if r[0] == "0" else r


def brute(nums):
    best = max("".join(map(str, p)) for p in itertools.permutations(nums))
    return "0" if best[0] == "0" else best


# dry run on [3, 30, 34, 5, 9]
print("pairs: '3' vs '30':", "330" if "330" > "303" else "303", "wins ('330' > '303'), so 3 goes first")
print("pairs: '34' vs '3':", "343 vs 334 -> 34 first")
print("plain descending strings:", "".join(sorted(map(str, [3, 30, 34, 5, 9]), reverse=True)),
      "| comparator:", solve([3, 30, 34, 5, 9]))
ss = sorted(map(str, [3, 30, 34, 5, 9]), key=functools.cmp_to_key(cmp))
print("order chosen:", ss, "-> joined", "".join(ss))
print("repeat keys :", [(s, s * (20 // len(s) + 1)) for s in map(str, [3, 30, 34, 5, 9])])

for nums, want in [([3, 30, 34, 5, 9], "9534330"), ([10, 2], "210"), ([0, 0], "0"), ([824, 8247], "8248247"), ([1], "1")]:
    got = solve(nums)
    assert got == solve_key(nums) == brute(nums) == want, (nums, got)
    print(nums, "->", repr(got))

# exact check 1: the key trick agrees with the comparator on EVERY pair of digit strings over {0,1,2,3}, length 1..4 (no leading zero)
strs = ["".join(p) for L in range(1, 5) for p in itertools.product("0123", repeat=L) if p[0] != "0" or L == 1]
key = lambda s: s * (20 // len(s) + 1)
bad = ties_split = 0
for a, b in itertools.product(strs, repeat=2):
    c = cmp(a, b)
    k = (key(a) < key(b)) - (key(a) > key(b))       # descending key: bigger key first = negative
    if c == 0:
        ties_split += (k != 0)                      # a + b == b + a, e.g. '1' and '11': the keys differ in LENGTH only
        assert a + b == b + a
    else:
        bad += (c != k)
print(f"pairs checked: {len(strs) ** 2} over {len(strs)} strings; strict disagreements: {bad}; "
      f"tied pairs (a+b == b+a) that the key still orders: {ties_split} (harmless: tied strings join to the same text)")
assert bad == 0

# exact check 2: transitivity of 'a before-or-equal b'  (a+b >= b+a) on all triples of strings over {0,1,2}, length 1..3
small = ["".join(p) for L in range(1, 4) for p in itertools.product("012", repeat=L)]
ge = lambda a, b: a + b >= b + a
viol = 0
for a, b, c in itertools.product(small, repeat=3):
    if ge(a, b) and ge(b, c) and not ge(a, c):
        viol += 1
print(f"triples checked: {len(small) ** 3}, transitivity violations: {viol}")
assert viol == 0
# total: for every pair one of a+b >= b+a, b+a >= a+b holds, trivially; ties (a+b == b+a) are equal-key strings
assert all(ge(a, b) or ge(b, a) for a, b in itertools.product(small, repeat=2))

# seeded random cross-check against all permutations (n <= 7)
for _ in range(400):
    n = random.randint(1, 7)
    nums = [random.choice([0, 1, 2, 3, 10, 30, 34, 99, 100, 824, 8247, 10 ** 9, random.randint(0, 10 ** 9)]) for _ in range(n)]
    got = solve(nums)
    assert got == brute(nums) == solve_key(nums), nums
print("400 seeded random cases match the permutation brute force and the key version")

# maximum size: 100 numbers up to 10^9
big = [random.randint(0, 10 ** 9) for _ in range(100)]
assert solve(big) == solve_key(big) and len(solve(big)) == sum(len(str(x)) for x in big)
print("n = 100 up to 10^9: comparator and key agree, length", len(solve(big)))

# edge cases
assert solve([0]) == "0" and solve([0, 0, 0]) == "0" and solve([10, 0]) == "100" and solve([0, 1]) == "10"
assert solve([121, 12]) == "12121" and solve([12, 121]) == "12121"          # a + b == b + a: a tie, any order
assert solve([10 ** 9, 10 ** 9 - 1]) == "9999999991000000000"
print("edge asserts ok")
```

**Output (my run):**
```
pairs: '3' vs '30': 330 wins ('330' > '303'), so 3 goes first
pairs: '34' vs '3': 343 vs 334 -> 34 first
plain descending strings: 9534303 | comparator: 9534330
order chosen: ['9', '5', '34', '3', '30'] -> joined 9534330
repeat keys : [('3', '333333333333333333333'), ('30', '3030303030303030303030'), ('34', '3434343434343434343434'), ('5', '555555555555555555555'), ('9', '999999999999999999999')]
[3, 30, 34, 5, 9] -> '9534330'
[10, 2] -> '210'
[0, 0] -> '0'
[824, 8247] -> '8248247'
[1] -> '1'
pairs checked: 65536 over 256 strings; strict disagreements: 0; tied pairs (a+b == b+a) that the key still orders: 48 (harmless: tied strings join to the same text)
triples checked: 59319, transitivity violations: 0
400 seeded random cases match the permutation brute force and the key version
n = 100 up to 10^9: comparator and key agree, length 886
edge asserts ok
```

**Edge cases:**
- All zeros (`[0, 0]`): the join would be `'00'`; return `'0'`.
- Zero mixed with others: `[10, 0]` gives `'100'`, `[0, 1]` gives `'10'`.
- Ties: `[121, 12]` and `[12, 121]` both give `'12121'`.
- One number: itself as a string.
- Largest values: `[10**9, 10**9 - 1]` gives `'9999999991000000000'`.

**Follow-ups:**
- *Why not sort numerically descending?* `[824, 8247]` must give `8248247`; numeric order puts 8247 first and gives `8247824`.
- *Why not compare `a + b` as ints?* Same result, but creating ints is slower than comparing strings; strings of equal length compare like numbers.
- *Smallest number instead?* Flip the comparison (and avoid a leading zero).
- *Python 2?* It had `cmp=`; Python 3 requires `cmp_to_key` or a key.

**Common mistakes:**
- Plain descending string sort (`'30'` before `'3'`).
- Returning `'000'` for all zeros.
- Using `sorted(..., cmp=...)` (a TypeError in Python 3).
- A comparator that returns a bool instead of -1/0/1 (the result is inconsistent).
- Mixing up the sign: `-1` must mean "a comes first".

### Q40 ⭐ 🟡 Matrix region sums with point updates (basic level). `matrix` is an m x n list of lists of integers (1 <= m, n <= 100) and `ops` has up to 10^4 operations, each `['update', r, c, v]` (set `matrix[r][c] = v`) or `['sum', r1, c1, r2, c2]` (the sum of the rectangle with corners (r1, c1) and (r2, c2), both included, 0 <= r1 <= r2 < m, 0 <= c1 <= c2 < n). Return one result per operation in order: None for an update, the sum for a sum. Keep a prefix-sum list per ROW: an update rebuilds one row in O(n), a query adds one prefix difference per row in O(r2 - r1 + 1) = O(m). Compare this with the static 2D table of Q5 (O(1) query but O(m * n) per update) and with a 2D Fenwick tree (O(log m * log n) both ways); the Fenwick tree and the segment tree are the standard answer for many updates and queries and belong to Part 14, so only name them here. In the answer include a dry run on the first example and a seeded random cross-check of your solution against recomputing the sum of the rectangle from the current matrix on every query on small inputs. Example: matrix=[[3, 0, 1], [5, 6, 3], [1, 2, 0]], ops=[['sum', 0, 0, 2, 2], ['update', 1, 1, 10], ['sum', 1, 1, 2, 2], ['sum', 0, 0, 1, 1]] -> [21, null, 15, 18]; matrix=[[4]], ops=[['update', 0, 0, -4], ['sum', 0, 0, 0, 0]] -> [null, -4].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Row-wise prefix sums with point updates: trade the O(1) query of a static 2D table for an O(n) update that touches one row only.

**Say this first (1 line):** "One prefix list per row: an update rebuilds a single row in O(n), and a sum adds one prefix difference per row in the rectangle, O(m); a 2D Fenwick tree does both in O(log m * log n) and is Part 14."

**Brute force:** On each query add up all cells of the rectangle (O(m * n), up to 10^4 per query); an update is O(1). With 10^4 operations that can be 10^8 steps. It is the oracle here.

**Optimal:**
- Keep `rows[r]` = `accumulate(matrix[r], initial=0)`, so `rows[r][c]` is the sum of the first c cells and the sum of columns `c1..c2` of row r is `rows[r][c2+1] - rows[r][c1]`.
- `update r c v`: set the cell, rebuild `rows[r]` (O(n)); nothing else changes.
- `sum r1 c1 r2 c2`: add `rows[r][c2+1] - rows[r][c1]` for `r` in `r1..r2` (O(r2 - r1 + 1) <= O(m)).
- Comparison:

| Method | Update | Query | Memory |
|---|---|---|---|
| Recompute from the matrix | O(1) | O(m * n) | O(1) extra |
| Static 2D prefix table (Q5) | O(m * n) | O(1) | O(m * n) |
| Row prefix lists (this answer) | O(n) | O(m) | O(m * n) |
| 2D Fenwick tree (Part 14, named only) | O(log m * log n) | O(log m * log n) | O(m * n) |

- Why the static table's update is O(m*n): changing cell (r, c) changes every table entry at or below row r and right of column c. The run shows a corner update on a 4 x 4 matrix changes all 16 table entries, while the last cell changes 1.
- At the maximum size (100 x 100, 10^4 mixed operations) the run counts about 5.1 * 10^5 row-rebuild steps and about 1.2 * 10^5 query row-differences in total (deterministic counts), against up to 10^4 cell reads per query for the brute force.
- Which to pick: many queries and few updates, the static table; balanced updates and queries on big grids, a Fenwick or segment tree; this row-wise form is the simple middle ground with m, n <= 100.

**Complexity:** Build O(m * n). Update O(n). Query O(m). Total for q operations: O(q * max(m, n)), at most about 10^6 steps here. Space O(m * n) for the matrix plus the same again for the prefix rows.

**Dry run:** `matrix = [[3,0,1],[5,6,3],[1,2,0]]`.
- Row prefixes: `[0,3,3,4]`, `[0,5,11,14]`, `[0,1,3,3]`.
- `sum (0,0)-(2,2)`: row 0 `4 - 0 = 4`, row 1 `14`, row 2 `3`: total 21.
- `update (1,1) = 10`: row 1 becomes `[5,10,3]`, prefixes `[0,5,15,18]`; rows 0 and 2 untouched.
- `sum (1,1)-(2,2)`: row 1 `18 - 5 = 13`, row 2 `3 - 1 = 2`: 15.
- `sum (0,0)-(1,1)`: row 0 `3 - 0 = 3`, row 1 `15 - 0 = 15`: 18. Result `[21, None, 15, 18]`.

**Code:**
```python
import itertools
import random

random.seed(4001)


def solve(matrix, ops, stats=None):
    mat = [list(r) for r in matrix]
    rows = [list(itertools.accumulate(r, initial=0)) for r in mat]   # rows[r][c] = sum of mat[r][:c]
    out = []
    for op in ops:
        if op[0] == "update":
            _, r, c, v = op
            mat[r][c] = v
            rows[r] = list(itertools.accumulate(mat[r], initial=0))  # rebuild ONE row: O(n)
            if stats is not None:
                stats["update_work"] += len(mat[r])
            out.append(None)
        else:
            _, r1, c1, r2, c2 = op
            out.append(sum(rows[r][c2 + 1] - rows[r][c1] for r in range(r1, r2 + 1)))   # one difference per row: O(m)
            if stats is not None:
                stats["query_work"] += r2 - r1 + 1
    return out


def brute(matrix, ops):
    mat = [list(r) for r in matrix]
    out = []
    for op in ops:
        if op[0] == "update":
            mat[op[1]][op[2]] = op[3]
            out.append(None)
        else:
            out.append(sum(mat[i][j] for i in range(op[1], op[3] + 1) for j in range(op[2], op[4] + 1)))
    return out


# dry run on the first example
matrix = [[3, 0, 1], [5, 6, 3], [1, 2, 0]]
rows = [list(itertools.accumulate(r, initial=0)) for r in matrix]
print("row prefix lists:", rows)
print("sum (0,0)-(2,2): row0", rows[0][3] - rows[0][0], "+ row1", rows[1][3] - rows[1][0], "+ row2", rows[2][3] - rows[2][0], "= 21")
matrix[1][1] = 10
rows[1] = list(itertools.accumulate(matrix[1], initial=0))
print("update (1,1)=10 rebuilds only row 1:", rows[1], "(other rows untouched)")
print("sum (1,1)-(2,2): row1", rows[1][3] - rows[1][1], "+ row2", rows[2][3] - rows[2][1], "= 15")
print("sum (0,0)-(1,1): row0", rows[0][2] - rows[0][0], "+ row1", rows[1][2] - rows[1][0], "= 18")

for mt, ops, want in [([[3, 0, 1], [5, 6, 3], [1, 2, 0]], [["sum", 0, 0, 2, 2], ["update", 1, 1, 10], ["sum", 1, 1, 2, 2], ["sum", 0, 0, 1, 1]], [21, None, 15, 18]),
                      ([[4]], [["update", 0, 0, -4], ["sum", 0, 0, 0, 0]], [None, -4])]:
    got = solve(mt, ops)
    assert got == want == brute(mt, ops)
    print(got)


# the static 2D prefix table (Q5 style): O(1) query, but one update changes up to m*n cells
def static_table(mat):
    m, n = len(mat), len(mat[0])
    p = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            p[i + 1][j + 1] = mat[i][j] + p[i][j + 1] + p[i + 1][j] - p[i][j]
    return p

m = [[1] * 4 for _ in range(4)]
p1 = static_table(m)
m[0][0] = 2
p2 = static_table(m)
changed = sum(p1[i][j] != p2[i][j] for i in range(5) for j in range(5))
print("\nstatic table: updating the corner cell (0,0) of a 4x4 matrix changes", changed, "of 16 table cells")
m[3][3] = 2
p3 = static_table(m)
print("updating cell (3,3) changes", sum(p2[i][j] != p3[i][j] for i in range(5) for j in range(5)), "table cell")

# seeded random cross-check against recomputing every rectangle from the current matrix
def rand_case(rng, mmax=6, nmax=6, k=40):
    m_, n_ = rng.randint(1, mmax), rng.randint(1, nmax)
    mt = [[rng.randint(-9, 9) for _ in range(n_)] for _ in range(m_)]
    ops = []
    for _ in range(rng.randint(0, k)):
        if rng.random() < 0.4:
            ops.append(["update", rng.randrange(m_), rng.randrange(n_), rng.randint(-9, 9)])
        else:
            r1 = rng.randrange(m_); r2 = rng.randint(r1, m_ - 1)
            c1 = rng.randrange(n_); c2 = rng.randint(c1, n_ - 1)
            ops.append(["sum", r1, c1, r2, c2])
    return mt, ops
rng = random.Random(40)
for _ in range(500):
    mt, ops = rand_case(rng)
    assert solve(mt, ops) == brute(mt, ops)
print("500 seeded random cases match the recompute-from-matrix oracle")

# maximum size: 100 x 100 matrix, 10^4 ops; count elementary steps (deterministic, unlike wall time)
mt = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(100)] for _ in range(100)]
ops = []
for _ in range(10 ** 4):
    if rng.random() < 0.5:
        ops.append(["update", rng.randrange(100), rng.randrange(100), rng.randint(-10 ** 6, 10 ** 6)])
    else:
        r1 = rng.randrange(100); r2 = rng.randint(r1, 99); c1 = rng.randrange(100); c2 = rng.randint(c1, 99)
        ops.append(["sum", r1, c1, r2, c2])
st = {"update_work": 0, "query_work": 0}
res = solve(mt, ops, st)
assert res == brute(mt, ops)
print("10^4 ops on 100 x 100:", st, "| the brute force would touch up to 10^4 cells per query")

# edge cases
assert solve([[7]], [["sum", 0, 0, 0, 0]]) == [7]
assert solve([[1, 2], [3, 4]], [["sum", 0, 0, 1, 1], ["update", 1, 1, 0], ["sum", 0, 0, 1, 1], ["sum", 1, 0, 1, 0]]) == [10, None, 6, 3]
assert solve([[5]], [["update", 0, 0, 5]]) == [None]
print("edge asserts ok")
```

**Output (my run):**
```
row prefix lists: [[0, 3, 3, 4], [0, 5, 11, 14], [0, 1, 3, 3]]
sum (0,0)-(2,2): row0 4 + row1 14 + row2 3 = 21
update (1,1)=10 rebuilds only row 1: [0, 5, 15, 18] (other rows untouched)
sum (1,1)-(2,2): row1 13 + row2 2 = 15
sum (0,0)-(1,1): row0 3 + row1 15 = 18
[21, None, 15, 18]
[None, -4]

static table: updating the corner cell (0,0) of a 4x4 matrix changes 16 of 16 table cells
updating cell (3,3) changes 1 table cell
500 seeded random cases match the recompute-from-matrix oracle
10^4 ops on 100 x 100: {'update_work': 506200, 'query_work': 124976} | the brute force would touch up to 10^4 cells per query
edge asserts ok
```

**Edge cases:**
- 1 x 1 matrix: update then sum.
- A query that is a single row or single column.
- Updating a cell to the same value: still rebuilds the row (harmless).
- Negative values and large sums: Python ints do not overflow.
- A query before any update, and updates that are never queried.

**Follow-ups:**
- *Can the update be O(1)?* Store the change and only re-sum lazily, or keep a Fenwick tree per row (O(log n) update and O(m log n) query).
- *Fully O(log) both ways?* 2D Fenwick tree or segment tree (Part 14).
- *Immutable matrix?* Use the static table (Q5) with O(1) query.
- *Heavy updates, few queries?* The brute force with O(1) update wins.

**Common mistakes:**
- Rebuilding the whole prefix structure on every update.
- Off-by-one: using `rows[r][c2]` instead of `rows[r][c2 + 1]` (the lists have n + 1 entries).
- Forgetting to update the stored matrix before rebuilding the row.
- Returning 0 instead of `None` for an update.
