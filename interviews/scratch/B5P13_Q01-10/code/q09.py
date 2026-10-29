import random
from fractions import Fraction

def brute(x, n):                                         # |n| multiplications by repeated product
    e, r = abs(n), 1
    for _ in range(e):
        r *= x
    f = Fraction(1, r) if n < 0 else Fraction(r)
    return [f.numerator, f.denominator, max(e - 1, 0)]

def optimal(x, n):
    e, result, base, mult = abs(n), 1, x, 0
    while e:
        if e & 1:
            result *= base; mult += 1
        e >>= 1
        if e:
            base *= base; mult += 1
    f = Fraction(1, result) if n < 0 else Fraction(result)   # reduced, denominator > 0
    return [f.numerator, f.denominator, mult]

def pow_rec(x, e):                                       # x^e = (x^(e//2))^2 * x^(e%2), depth ~ log2(e)
    if e == 0:
        return 1
    h = pow_rec(x, e // 2)
    return h * h * (x if e & 1 else 1)

def closed_form(n):
    e = abs(n)
    return bin(e).count('1') + e.bit_length() - 1 if e else 0

for (x, n), want in [((2, 10), [1024, 1, 5]), ((3, -2), [1, 9, 2]), ((-2, 5), [-32, 1, 4]),
                     ((7, 0), [1, 1, 0]), ((10, 1), [10, 1, 1])]:
    got = optimal(x, n)
    assert got == want
    print('x =', x, 'n =', n, '->', got)

# exhaustive over the whole input space: every nonzero |x| <= 10 and every |n| <= 300
for x in [v for v in range(-10, 11) if v]:
    for n in range(-300, 301):
        got = optimal(x, n)
        f = Fraction(x) ** n
        assert got[:2] == [f.numerator, f.denominator] and got[2] == closed_form(n)
        assert got[1] > 0 and Fraction(got[0], got[1]) == f
        assert pow_rec(abs(x), abs(n)) == abs(x) ** abs(n)
        if abs(n) <= 40:
            assert brute(x, n)[:2] == got[:2]
print('exhaustive check ok: 20 values of x times 601 values of n; count equals popcount + bit_length - 1')
random.seed(9)
for _ in range(300):
    x = random.choice([v for v in range(-10, 11) if v]); n = random.randint(-40, 40)
    assert optimal(x, n)[:2] == brute(x, n)[:2]
print('seeded random cross-check vs repeated multiplication ok')

# claim: n = -2**31 overflows when negated in 32-bit C/Java; Python has no such limit
n = -2**31
print('abs(-2**31) =', abs(n), '> 2**31 - 1 =', 2**31 - 1, '(a 32-bit int cannot hold it)')
# modular exponentiation: pow with three arguments never builds the huge number
assert pow(7, 10**18, 10**9 + 7) == pow(7, 10**18 % (10**9 + 6), 10**9 + 7)   # Fermat, p prime
print('pow(7, 10**18, 10**9+7) =', pow(7, 10**18, 10**9 + 7))
# max case: x = 10, n = -300
assert optimal(10, -300) == [1, 10**300, closed_form(300)] and closed_form(300) == 4 + 9 - 1
print('x=10, n=-300 -> denominator has', len(str(10**300)), 'digits; multiplications', closed_form(300))
