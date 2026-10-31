import random

SENT = 2147483647


class Hidden:
    def __init__(self, a):
        self.a, self.calls = a, 0

    def get(self, i):
        self.calls += 1
        return self.a[i] if i < len(self.a) else SENT


def search_unknown(h, target):
    if target >= SENT:                      # real values are < SENT; do not let the sentinel "match"
        return -1
    lo, hi = 0, 1
    while h.get(hi) < target:               # doubling: stop at the first hi with get(hi) >= target
        lo = hi
        hi *= 2
    while lo <= hi:                         # closed binary search in [lo, hi]; the sentinel just reads as "too big"
        mid = (lo + hi) // 2
        v = h.get(mid)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def brute(a, t):
    return a.index(t) if t in a else -1


for a, t, want in [([-1, 0, 3, 5, 9, 12], 9, 4), ([-1, 0, 3, 5, 9, 12], 2, -1), ([7], 7, 0), ([7], 8, -1)]:
    h = Hidden(a)
    got = search_unknown(h, t)
    assert got == brute(a, t) == want
    print(a, "target", t, "->", got, "| get calls:", h.calls)

# call-count bound. p = index of the first element >= target (found or insertion position).
# doubling: hi is the first power of two with get(hi) >= target  -> at most bit_length(p) + 1 calls
# binary search in a window of size hi - lo + 1 <= p + 2 -> at most bit_length(p + 1) + 1 calls
worst_slack = 99
for n in range(0, 140):
    a = list(range(-3, 2 * n - 3, 2))      # distinct ascending, odd step so absent targets fall between
    for t in range(-6, 2 * n + 2):
        h = Hidden(a)
        assert search_unknown(h, t) == brute(a, t), (n, t)
        p = sum(1 for v in a if v < t)
        bound = 2 * (p + 2).bit_length() + 3
        assert h.calls <= bound, (n, t, p, h.calls, bound)
        worst_slack = min(worst_slack, bound - h.calls)
print("exhaustive check passed for lengths 0..139, every target; calls <= 2*bit_length(p+2)+3 (min slack", worst_slack, ")")

# big hidden array: calls depend on the position p, not on the array size
rng = random.Random(30)
n = 10 ** 6
big = sorted(rng.sample(range(-10 ** 9, 10 ** 9), n))
for p in (0, 5, 1000, 10 ** 6 - 1):
    h = Hidden(big)
    assert search_unknown(h, big[p]) == p
    print(f"n = 10^6, answer position {p}: {h.calls} get calls")
h = Hidden(list(range(10 ** 6)))
assert search_unknown(h, 3) == 3
small_calls = h.calls
h = Hidden(list(range(10)))
assert search_unknown(h, 3) == 3
assert h.calls == small_calls, "same position, different array size -> same call count"
print("position 3 costs", small_calls, "calls in a 10-element array and in a 10^6-element array")

# seeded random check
for _ in range(500):
    a = sorted(rng.sample(range(-50, 200), rng.randint(0, 40)))
    t = rng.randint(-60, 210)
    assert search_unknown(Hidden(a), t) == brute(a, t)
print("random check passed: 500 cases")

# edge cases
assert search_unknown(Hidden([]), 5) == -1                      # get(0) already the sentinel
assert search_unknown(Hidden([1, 2, 3]), SENT) == -1            # target equal to the sentinel must not "match" it
assert search_unknown(Hidden([1, 2, 3]), -10 ** 9) == -1
assert search_unknown(Hidden([1, 2, 3]), 3) == 2
assert search_unknown(Hidden(list(range(5))), 0) == 0
print("edge asserts passed")
