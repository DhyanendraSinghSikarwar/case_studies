import random


def kth_root(x, n):
    lo, hi = 0, x                        # predicate r**n <= x is True...True False...False; find the last True
    while lo < hi:
        mid = (lo + hi + 1) // 2         # upper mid so the loop makes progress
        if mid ** n <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def kth_root_brute(x, n):
    r = 0
    while (r + 1) ** n <= x:
        r += 1
    return r


# prompt examples
for x, n, want in [(27, 3, 3), (125, 3, 5), (80, 4, 2), (10**18, 2, 10**9), (0, 5, 0), (1, 60, 1)]:
    assert kth_root(x, n) == want, (x, n)
    print("x =", x, "n =", n, "->", kth_root(x, n))
print("float 125 ** (1/3) =", 125 ** (1 / 3), "-> int() gives", int(125 ** (1 / 3)))
assert int(125 ** (1 / 3)) == 4

# how often is the float shortcut wrong on exact roots r**n?
bad = [(r, n) for n in range(2, 9) for r in range(1, 300) if int((r ** n) ** (1 / n)) != r]
print("exact roots r**n (n=2..8, r<300) where int(x ** (1/n)) is wrong:", len(bad), "e.g.", bad[:5])
assert (5, 3) in bad
# and it can be wrong off exact roots at large x
x = 10**18 - 1
print("float root of 10**18-1 (n=2):", int(x ** 0.5), "exact:", kth_root(x, 2))

# seeded cross-check
rng = random.Random(32)
for _ in range(600):
    n = rng.randint(1, 8)
    x = rng.randint(0, 5000)
    assert kth_root(x, n) == kth_root_brute(x, n), (x, n)
# exhaustive for small x and n
for n in range(1, 7):
    for x in range(0, 400):
        assert kth_root(x, n) == kth_root_brute(x, n)
# exact-boundary property on big values
for _ in range(300):
    n = rng.randint(1, 60)
    x = rng.randint(0, 10**18)
    r = kth_root(x, n)
    assert r ** n <= x < (r + 1) ** n
for n in range(1, 61):
    for r in (1, 2, 3, 7):
        assert kth_root(r ** n, n) == r and kth_root(r ** n - 1, n) == r - 1
# edge asserts
assert kth_root(0, 1) == 0 and kth_root(1, 1) == 1 and kth_root(10**18, 1) == 10**18
assert kth_root(10**18, 60) == 1      # 2**60 = 1.15e18 > 1e18, so only 1 fits
print("all checks passed")
