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
