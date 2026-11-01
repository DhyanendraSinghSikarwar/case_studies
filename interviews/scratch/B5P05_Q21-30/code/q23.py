import random
from itertools import product

BUDGET = 100


class Mountain:
    # hidden array with a call counter; get() refuses to go past the budget
    def __init__(self, a):
        self._a, self.calls = a, 0

    def length(self):                       # length() is free in the prompt (not counted)
        return len(self._a)

    def get(self, i):
        self.calls += 1
        assert self.calls <= BUDGET, "call budget exceeded"
        return self._a[i]


def find_peak(m):
    lo, hi = 0, m.length() - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if m.get(mid) < m.get(mid + 1):
            lo = mid + 1                    # still climbing: peak is to the right
        else:
            hi = mid                        # descending (or at peak): peak is at mid or left
    return lo


def bs_side(m, lo, hi, target, ascending):
    while lo <= hi:
        mid = (lo + hi) // 2
        v = m.get(mid)
        if v == target:
            return mid
        if (v < target) == ascending:       # ascending: too small -> go right; descending: too small -> go left
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def search_mountain(m, target):
    p = find_peak(m)
    i = bs_side(m, 0, p, target, True)      # left side (including the peak) first: smaller indices
    if i != -1:
        return i
    return bs_side(m, p + 1, m.length() - 1, target, False)


def search_brute(a, target):
    return a.index(target) if target in a else -1


def run(a, t):
    m = Mountain(a)
    return search_mountain(m, t), m.calls


for a, t, want in [([1, 2, 3, 4, 5, 3, 1], 3, 2), ([0, 1, 2, 4, 2, 1], 3, -1), ([1, 5, 2], 2, 2), ([1, 5, 2], 5, 1)]:
    got, calls = run(a, t)
    assert got == search_brute(a, t) == want, (a, t)
    print(a, "target", t, "->", got, "| get calls:", calls)

# exhaustive: every mountain of length 3..7 with values 0..6, every target -1..7
count, worst = 0, 0
for n in range(3, 8):
    for a in product(range(7), repeat=n):
        a = list(a)
        p = a.index(max(a))
        if not (all(a[i] < a[i + 1] for i in range(p)) and all(a[i] > a[i + 1] for i in range(p, n - 1)) and 0 < p < n - 1):
            continue
        for t in range(-1, 8):
            got, calls = run(a, t)
            assert got == search_brute(a, t), (a, t, got)
            worst = max(worst, calls)
            count += 1
print("exhaustive check passed:", count, "(array, target) pairs; worst calls at n<=7:", worst)

# random big mountains, n up to 10^4, counting calls
rng = random.Random(23)
worst_calls, worst_n = 0, 0
for _ in range(3000):
    n = rng.choice([3, 4, 5, 100, 1000, 9999, 10000, rng.randint(3, 10000)])
    p = rng.randint(1, n - 2)
    left = sorted(rng.sample(range(0, 40000), p))
    right = sorted(rng.sample(range(0, 40000), n - p - 1), reverse=True)
    a = left + [40000] + right              # strictly up to index p, strictly down after
    for t in [rng.choice(a), rng.choice(a), rng.randint(-1, 40001), a[0], a[-1], max(a)]:
        got, calls = run(a, t)
        assert got == search_brute(a, t), (n, t)
        if calls > worst_calls:
            worst_calls, worst_n = calls, n
print("random check passed; worst calls seen:", worst_calls, "at n =", worst_n, "(budget 100)")

# worst-case probe at n = 10^4 for EVERY peak position, target absent on both sides
n = 10 ** 4
w = 0
for p in range(1, n - 1):
    a = list(range(0, 2 * p, 2)) + [2 * p] + list(range(2 * p - 1, 2 * p - 1 - 2 * (n - p - 1), -2))
    for t in (-1, 1, 2 * p + 1):
        w = max(w, run(a, t)[1])
print("worst calls over all 9998 peak positions at n = 10^4, 3 absent targets each:", w)
assert w <= BUDGET
k = (n - 1).bit_length()
print("ceil(log2(10^4)) =", k, "| peak step: 2 gets per round ~", 2 * k, "| one side search ~", k, "| both sides ~", 2 * k, "| total ~", 4 * k)
