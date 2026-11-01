import math
import random


def sqrt_fixed(x, iters=100):
    lo, hi = 0.0, max(1.0, x)            # sqrt(x) <= max(1, x) for every x >= 0
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sqrt_eps(x, eps=1e-9, cap=10**6):
    # returns (answer, loops used); cap stops a non-terminating loop for the demo
    lo, hi = 0.0, max(1.0, x)
    loops = 0
    while hi - lo > eps and loops < cap:
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
        loops += 1
    return (lo + hi) / 2, loops


def sqrt_bad_hi(x, iters=100):
    lo, hi = 0.0, x                      # WRONG for x < 1: sqrt(x) > x
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def halvings(width, tol):
    # smallest h with width / 2**h <= tol
    h = 0
    while width / 2 ** h > tol:
        h += 1
    return h


# examples from the prompt
for x, want in [(2, 1.41421356), (0.25, 0.5), (0, 0.0), (10**6, 1000.0)]:
    assert abs(sqrt_fixed(x) - want) <= 1e-6
    assert abs(sqrt_eps(x, 1e-9)[0] - want) <= 1e-6
    print("x =", x, "fixed:", sqrt_fixed(x), " eps loop:", sqrt_eps(x, 1e-9))

# hi = x is wrong below 1
print("hi = x with x=0.25 gives", sqrt_bad_hi(0.25), "(true 0.5)")
assert abs(sqrt_bad_hi(0.25) - 0.5) > 0.2

# eps below float spacing never terminates
ans, loops = sqrt_eps(10**6, 1e-15, cap=10**6)
print("eps=1e-15, x=10**6: loops =", loops, "(hit the 10**6 cap)", " spacing near 1000:", math.ulp(1000.0))
assert loops == 10**6
ans2, loops2 = sqrt_eps(10**6, 1e-9)
print("eps=1e-9, x=10**6: loops =", loops2)
assert loops2 < 100

# halvings needed
print("halvings for width 10**6 to tol 1e-6:", halvings(10**6, 1e-6))
print("halvings for width 1 to tol 1e-6:", halvings(1, 1e-6))
assert halvings(10**6, 1e-6) == 40 and halvings(1, 1e-6) == 20

# seeded cross-check against math.sqrt, including x < 1
rng = random.Random(31)
worst = 0.0
for _ in range(2000):
    x = rng.choice([rng.random(), rng.uniform(0, 10), rng.uniform(0, 10**6), float(rng.randint(0, 10**6))])
    err = abs(sqrt_fixed(x) - math.sqrt(x))
    worst = max(worst, err)
    assert err <= 1e-6
    assert abs(sqrt_eps(x, 1e-9)[0] - math.sqrt(x)) <= 1e-6
print("2000 random x: worst error of fixed-100 version =", worst)
print("all checks passed")
