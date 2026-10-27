import math, random

def brute(x):
    r = 0
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r

def isqrt_bs(x):
    lo, hi = 0, min(x, 46340)          # 46340^2 = 2147395600 <= 2^31-1 < 46341^2; hi = x also works
    while lo < hi:                     # last True: invariant r*r <= x holds at lo
        mid = (lo + hi + 1) // 2       # upper-biased, else lo = mid loops forever
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo

def isqrt_plain(x):                    # same search without the cap, hi = x
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x: lo = mid
        else: hi = mid - 1
    return lo

for x in range(0, 5000):
    assert isqrt_bs(x) == brute(x) == math.isqrt(x) == isqrt_plain(x)
random.seed(3)
for _ in range(3000):
    x = random.randint(0, 2**31 - 1)
    assert isqrt_bs(x) == math.isqrt(x) == isqrt_plain(x)
for r in (1, 2, 46339, 46340):
    assert isqrt_bs(r*r) == r and isqrt_bs(r*r - 1) == r - 1
assert 46340**2 <= 2**31 - 1 < 46341**2
assert isqrt_bs(2**31 - 1) == 46340
print("cross-check ok")
for x in (4, 8, 0, 1, 2147395599, 2147395600):
    print(x, "->", isqrt_bs(x))
# float risk for huge ints
n = 10**60 - 1
print("float sqrt of 10**60-1:", int(n ** 0.5), "| exact isqrt:", math.isqrt(n))
