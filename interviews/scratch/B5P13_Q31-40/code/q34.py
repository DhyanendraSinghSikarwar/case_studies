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
