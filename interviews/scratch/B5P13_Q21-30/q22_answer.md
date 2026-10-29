### Q22 ⭐⭐ 🟢 Rounding half to even and why floats surprise you. `values` is a list of 1 to 30 decimal strings such as '2.5' or '-1.005' with at most 3 digits after the point (a negative value has absolute value at least 0.01). For each string s return `[a, b, c, d]`: `a = round(float(s))` (Python 3 rounds ties to the nearest EVEN integer, so 2.5 gives 2 and 3.5 gives 4); `b` = the integer obtained by rounding the exact decimal value half away from zero (`Decimal(s)` with `ROUND_HALF_UP`, so 2.5 gives 3 and -2.5 gives -3); `c = repr(round(float(s), 2))`; `d = str(Decimal(s).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))` (always two decimals). Explain why `round(2.675, 2)` gives 2.67 (the stored binary double is slightly below 2.675, so it is not a tie at all), why `a` is a true tie rule only because .5 is exactly representable, why banks and statisticians prefer half-even (no systematic upward bias) and when to use Decimal instead of float (money). In the answer include a dry run on the first example and a seeded random cross-check of your solution against exact Fraction arithmetic on small inputs. Example: values=['2.5', '0.5', '-1.5', '2.675', '1.005', '3.5', '-0.5'] -> [[2, 3, '2.5', '2.50'], [0, 1, '0.5', '0.50'], [-2, -2, '-1.5', '-1.50'], [3, 3, '2.67', '2.68'], [1, 1, '1.0', '1.00'], [4, 4, '3.5', '3.50'], [0, -1, '-0.5', '-0.50']]; values=['10'] -> [[10, 10, '10.0', '10.00']].
**Asked at:** Python documentation for int, float, Decimal and Fraction (docs.python.org fetch failed with ENOTFOUND, not opened; behaviour verified by running Python 3.13)

**Pattern:** Number representation. Python's `round` works on the stored binary double. `Decimal` works on the written decimal. Know which one you are rounding.

**Say this first (1 line):** "round() on a float rounds the exact binary value, ties go to even; money is a Decimal job, because 2.675 is not stored as 2.675."

**Brute force:** Convert each string to an exact `Fraction`, do the rounding rules with integer arithmetic (floor, compare the remainder with 1/2, tie goes to the even neighbour), and format the result by hand. Exact but slow to write. It is the oracle here.

**Optimal:** Four one-liners per value:
- `a = round(float(s))`: ties to even. 2.5 gives 2, 3.5 gives 4, -1.5 gives -2, 0.5 gives 0.
- `b = int(Decimal(s).to_integral_value(ROUND_HALF_UP))`: exact decimal, ties away from zero. 2.5 gives 3, -2.5 gives -3, 0.5 gives 1.
- `c = repr(round(float(s), 2))`: the float is rounded, then printed with the shortest repr that round-trips.
- `d = str(Decimal(s).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))`: exact decimal, two places, tie to even, always two decimals.

Why `round(2.675, 2)` is 2.67: the double nearest 2.675 is 2.67499999999999982236431605997495353221893310546875. It is below the tie, so it is not a tie at all and it rounds down. `Decimal('2.675')` is exactly 2.675, a real tie, and half-even gives 2.68 (7 is odd, so go up to 8).

Why `a` is a true tie rule: x.5 is a sum of powers of two, so the double holds it exactly. Of all decimals with at most 3 digits, only the x.5 ones are exactly representable ties at integer rounding. At two places, a tie like x.xx5 is almost never exact. The program counts it: of the 10000 strings x.xx5 from 0.005 to 99.995, `round(f, 2)` differs from the exact half-even answer in 4800.

Why banks and statisticians use half-even: each tie goes up half the time and down half the time, so the rounding error averages to 0. Half-up always pushes ties the same way. For the ties 0.5, 1.5, ..., 9.5 the mean error is +0.5 for half-up and 0.0 for half-even (printed).

Use `Decimal` (or integer cents) for money. Use float for measurements.

**Complexity:** O(1) per value, O(len(values)) in total (the strings have at most a handful of digits).

**Dry run:** `'2.675'`. a: `float` is 2.67499..., `round` gives 3. b: Decimal 2.675 rounds half up to 3. c: `round(2.67499.., 2)` is 2.67, printed `'2.67'`. d: exact 2.675, tie, neighbours 2.67 (odd last digit) and 2.68 (even), so `'2.68'`. Result `[3, 3, '2.67', '2.68']`. The program prints the exact doubles behind 2.675 and 1.005.

**Code:**
```python
import math
import random
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from fractions import Fraction

random.seed(2201)

def solve(values):
    out = []
    for s in values:
        f, d = float(s), Decimal(s)
        a = round(f)                                              # ties to even
        b = int(d.to_integral_value(rounding=ROUND_HALF_UP))      # exact decimal, half away from 0
        c = repr(round(f, 2))                                     # rounds the BINARY double
        q = str(d.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))
        out.append([a, b, c, q])
    return out

def half_even(x):                      # Fraction -> int, ties to even
    fl = math.floor(x)
    r = x - fl
    return fl if r < Fraction(1, 2) else fl + 1 if r > Fraction(1, 2) else (fl if fl % 2 == 0 else fl + 1)

def brute(values):
    """Independent oracle: exact Fraction arithmetic only."""
    out = []
    for s in values:
        q, ex = Fraction(s), Fraction(float(s))              # ex = the exact value of the stored double
        hu = (1 if q >= 0 else -1) * math.floor(abs(q) + Fraction(1, 2))
        r2 = float(half_even(ex * 100) / Fraction(100))
        h2 = half_even(q * 100)
        sign, mag = ('-' if h2 < 0 else ''), abs(h2)
        out.append([half_even(ex), hu, repr(r2), f'{sign}{mag // 100}.{mag % 100:02d}'])
    return out

ex1 = ['2.5', '0.5', '-1.5', '2.675', '1.005', '3.5', '-0.5']
want1 = [[2, 3, '2.5', '2.50'], [0, 1, '0.5', '0.50'], [-2, -2, '-1.5', '-1.50'], [3, 3, '2.67', '2.68'],
         [1, 1, '1.0', '1.00'], [4, 4, '3.5', '3.50'], [0, -1, '-0.5', '-0.50']]
assert solve(ex1) == want1 == brute(ex1)
assert solve(['10']) == [[10, 10, '10.0', '10.00']] == brute(['10'])
for s, r in zip(ex1, solve(ex1)):
    print(f'{s:>6} -> {r}')

# why 2.675 surprises: the stored double is just below the tie
print('exact value of the double 2.675  :', Decimal(2.675))
print('exact value of the double 1.005  :', Decimal(1.005))
print('exact value of the double 2.5    :', Decimal(2.5), '(exact, a true tie)')
assert Decimal(2.675) < Decimal('2.675') and Decimal(1.005) < Decimal('1.005')

# which decimals with <=3 digits are exactly representable ties? only x.5 (a dyadic fraction)
assert all(Fraction(k, 1000) == Fraction(k / 1000) for k in range(500, 10001, 1000))
print('x.5 values 0.5..10.5 all exact doubles: True')

# how often do float rounding (c) and exact half-even decimal (d) disagree on x.xx5 strings?
bad = 0; total = 0
for k in range(0, 100000):
    s = f'{k // 1000}.{k % 1000:03d}'
    if s.endswith('5'):
        total += 1
        r = solve([s])[0]
        if float(r[2]) != float(r[3]):
            bad += 1
print(f'x.xx5 strings 0.005..99.995: {total}; float round(.,2) differs from exact half-even in {bad}')

# half-even removes the upward bias: average error over the ties 0.5, 1.5, ..., 9.5
ties = [k + 0.5 for k in range(10)]
up = sum(math.floor(t + 0.5) - t for t in ties) / 10
even = sum(round(t) - t for t in ties) / 10
print('mean error half-up:', up, ' half-even:', even)
assert up == 0.5 and even == 0.0

# seeded random cross-check against exact Fractions
def rand_dec():
    k = random.randint(0, 3); v = random.randint(-2000, 2000)
    if v == 0 or (v < 0 and abs(v) < 10 ** (k - 2 if k > 2 else 0)): v = 1
    sign = '-' if v < 0 else ''; v = abs(v)
    s = f'{sign}{v // 10 ** k}' + (f'.{v % 10 ** k:0{k}d}' if k else '')
    return s if abs(Fraction(s)) >= Fraction(1, 100) else '0.01'
for _ in range(3000):
    vals = [rand_dec() for _ in range(random.randint(1, 8))]
    assert solve(vals) == brute(vals), vals
print('random cross-check ok: 3000 lists')
assert solve(['-0.01'])[0] == [0, 0, '-0.01', '-0.01']
assert solve(['0.125', '0.135']) == [[0, 0, '0.12', '0.12'], [0, 0, '0.14', '0.14']]
print('edge asserts ok')
```

**Output (my run):**
```
   2.5 -> [2, 3, '2.5', '2.50']
   0.5 -> [0, 1, '0.5', '0.50']
  -1.5 -> [-2, -2, '-1.5', '-1.50']
 2.675 -> [3, 3, '2.67', '2.68']
 1.005 -> [1, 1, '1.0', '1.00']
   3.5 -> [4, 4, '3.5', '3.50']
  -0.5 -> [0, -1, '-0.5', '-0.50']
exact value of the double 2.675  : 2.67499999999999982236431605997495353221893310546875
exact value of the double 1.005  : 1.00499999999999989341858963598497211933135986328125
exact value of the double 2.5    : 2.5 (exact, a true tie)
x.5 values 0.5..10.5 all exact doubles: True
x.xx5 strings 0.005..99.995: 10000; float round(.,2) differs from exact half-even in 4800
mean error half-up: 0.5  half-even: 0.0
random cross-check ok: 3000 lists
edge asserts ok
```

**Edge cases:**
- Ties on both signs: -1.5 gives -2 in both `a` and `b`, but -0.5 gives 0 for `a` (even) and -1 for `b` (half away from zero).
- `'10'`: no fraction, `c = '10.0'`, `d = '10.00'`.
- `'-0.01'` gives `d = '-0.01'`. `a` is 0 (an int, so no negative zero is shown).
- `'1.005'`: float side gives `'1.0'` (the double is below 1.005), decimal side gives `'1.00'` (exact tie, 0 is even).
- `'0.125'` is exact in binary, so `round(0.125, 2)` really is a tie and gives 0.12. `'0.135'` is not exact and the program shows 0.14.

**Follow-ups:**
- *`math.isclose` vs `==`?* Floats are compared with a tolerance; `0.1 + 0.2 != 0.3`.
- *Why is `round(x)` an int but `round(x, 2)` a float?* With no digit argument `round` returns an int. With a digit argument it returns the same type as the input.
- *When is `Decimal` not enough?* If you need exact thirds or similar, use `Fraction`.

**Common mistakes:**
- Believing `round(2.675, 2)` is a bug in Python. The decimal you typed is simply not the number stored.
- Assuming Python rounds half up like school. It rounds half to even.
- Building a Decimal from a float: `Decimal(2.675)` gives the long binary expansion. Build it from the string.
- Using `ROUND_HALF_UP` and calling it "banker's rounding".
