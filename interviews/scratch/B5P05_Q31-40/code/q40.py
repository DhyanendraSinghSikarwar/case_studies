import math
import random
from fractions import Fraction
from itertools import product


def need(stations, d):
    return sum(math.ceil((b - a) / d) - 1 for a, b in zip(stations, stations[1:]))


def min_max_gap(stations, k, iters=100):
    lo, hi = 0.0, float(max(b - a for a, b in zip(stations, stations[1:])))
    for _ in range(iters):
        mid = (lo + hi) / 2
        if need(stations, mid) <= k:
            hi = mid                        # mid is enough, try smaller
        else:
            lo = mid
    return hi


def min_max_gap_eps(stations, k, eps, cap=10**6):
    lo, hi = 0.0, float(max(b - a for a, b in zip(stations, stations[1:])))
    loops = 0
    while hi - lo > eps and loops < cap:
        mid = (lo + hi) / 2
        if need(stations, mid) <= k:
            hi = mid
        else:
            lo = mid
        loops += 1
    return hi, loops


def min_max_gap_exact(stations, k):
    # brute force: try every way to split k stations over the gaps (extra stations in a gap -> gap/(c+1)); exact Fractions
    gaps = [b - a for a, b in zip(stations, stations[1:])]
    best = None
    def go(i, left, cur):
        nonlocal best
        if i == len(gaps) - 1:
            v = max(cur, Fraction(gaps[i], left + 1))
            if best is None or v < best:
                best = v
            return
        for c in range(left + 1):
            go(i + 1, left - c, max(cur, Fraction(gaps[i], c + 1)))
    go(0, k, Fraction(0))
    return best


for st, k, want in [(list(range(1, 11)), 9, 0.5), ([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 14.0), ([0, 10], 0, 10.0), ([0, 10], 1, 5.0)]:
    got = min_max_gap(st, k)
    print(st, "k =", k, "->", round(got, 7))
    assert abs(got - want) <= 1e-6
print("eps=1e-6 loop on [0,10], k=1:", min_max_gap_eps([0, 10], 1, 1e-6))
print("eps=1e-17 loop on the 14.0 example, capped at 10**6:", min_max_gap_eps([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 1e-17)[1], "loops")
assert min_max_gap_eps([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 1e-17)[1] == 10**6

# seeded cross-check against exact brute force, and the 'gap/(c+1)' claim
rng = random.Random(40)
hit = 0
worst = 0.0
for _ in range(600):
    n = rng.randint(2, 5)
    st = sorted(rng.sample(range(0, 40), n))
    k = rng.randint(0, 5)
    ex = min_max_gap_exact(st, k)
    got = min_max_gap(st, k)
    worst = max(worst, abs(got - float(ex)))
    assert abs(got - float(ex)) <= 1e-6, (st, k)
    gaps = [b - a for a, b in zip(st, st[1:])]
    assert any(ex == Fraction(g, c + 1) for g in gaps for c in range(k + 1)), (st, k)
    hit += 1
print("600 seeded cases: worst |binary search - exact| =", worst, "; exact optimum was always some gap/(c+1)")

# monotone predicate: need() never increases as d grows
for _ in range(200):
    st = sorted(rng.sample(range(0, 60), rng.randint(2, 7)))
    seq = [need(st, d / 4) for d in range(1, 200)]
    assert all(x >= y for x, y in zip(seq, seq[1:]))
print("need(d) non-increasing in d on 200 seeded station lists")
# edge asserts
assert abs(min_max_gap([0, 1], 0) - 1.0) <= 1e-6
assert abs(min_max_gap([0, 1, 2], 100) - 1 / 51) <= 1e-6        # 100 stations over 2 equal gaps: 50 each, gap 1/51
assert abs(min_max_gap([0, 7], 3) - 1.75) <= 1e-6
assert abs(min_max_gap([0, 10, 11], 1) - 5.0) <= 1e-6
print("all checks passed")
