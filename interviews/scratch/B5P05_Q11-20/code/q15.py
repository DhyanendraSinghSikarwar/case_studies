import math
import random


def first_bad(n, is_bad):
    lo, hi = 1, n
    while lo < hi:
        mid = lo + (hi - lo) // 2      # same as (lo+hi)//2 here; the safe form in fixed-width ints
        if is_bad(mid):
            hi = mid                   # mid might be the first bad: keep it
        else:
            lo = mid + 1               # mid is good: first bad is strictly after it
    return lo


def first_bad_linear(n, is_bad):
    for v in range(1, n + 1):
        if is_bad(v):
            return v


class Oracle:
    """Counts calls and records which versions were asked."""
    def __init__(self, f):
        self.f, self.calls, self.asked = f, 0, []

    def __call__(self, v):
        self.calls += 1
        self.asked.append(v)
        return v >= self.f


for n, f in [(5, 4), (1, 1), (2, 2)]:
    o = Oracle(f)
    got = first_bad(n, o)
    assert got == f
    print("n=%d f=%d -> %d (calls %d)" % (n, f, got, o.calls))
o = Oracle(10**9)
got = first_bad(10**9, o)
assert got == 10**9
print("n=10**9 f=10**9 -> %d with %d calls (budget ceil(log2 n) = %d)" % (got, o.calls, math.ceil(math.log2(10**9))))
assert o.calls <= 30

# exhaustive: every n up to 600 and every f: right answer, <= ceil(log2 n) calls, no version asked twice
worst = {}
for n in range(1, 601):
    budget = math.ceil(math.log2(n))
    for f in range(1, n + 1):
        o = Oracle(f)
        assert first_bad(n, o) == f == first_bad_linear(n, lambda v: v >= f), (n, f)
        assert o.calls <= budget, (n, f, o.calls, budget)
        assert len(set(o.asked)) == len(o.asked), (n, f, o.asked)
        worst[n] = max(worst.get(n, 0), o.calls)
print("exhaustive: n in 1..600, every f: correct, within ceil(log2 n) calls, no repeated call")
print("worst-case calls observed: n=1 ->", worst[1], ", n=2 ->", worst[2], ", n=5 ->", worst[5],
      ", n=512 ->", worst[512], ", n=600 ->", worst[600])

# seeded large n: sample f including both ends
random.seed(15)
for n in (2**31 - 1, 10**9, 2**20, 2**20 + 1):
    budget = math.ceil(math.log2(n))
    for f in [1, 2, n - 1, n, n // 2, n // 2 + 1] + [random.randint(1, n) for _ in range(300)]:
        f = max(1, min(n, f))
        o = Oracle(f)
        assert first_bad(n, o) == f and o.calls <= budget and len(set(o.asked)) == len(o.asked)
print("seeded large-n sample (n up to 2^31-1): all within budget")
assert first_bad(1, lambda v: True) == 1
print("edge asserts passed")
