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
