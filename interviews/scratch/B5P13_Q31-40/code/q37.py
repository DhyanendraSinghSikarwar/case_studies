import random
import time

random.seed(3701)


def solve(records, trace=None, backwards=True):
    """LSD radix sort, base 10. backwards=False is the BROKEN forward walk, kept only to show why it matters."""
    a = [list(r) for r in records]
    mx = max(r[0] for r in a)
    passes, exp = 0, 1
    while True:
        passes += 1
        cnt = [0] * 10
        for r in a:
            cnt[r[0] // exp % 10] += 1                  # 1. count each digit value
        for d in range(1, 10):
            cnt[d] += cnt[d - 1]                        # 2. prefix sums: cnt[d] = end (exclusive) of digit d's block
        out = [None] * len(a)
        for r in (reversed(a) if backwards else a):     # 3. walk from the LAST item, fill each block from its end
            dg = r[0] // exp % 10
            cnt[dg] -= 1
            out[cnt[dg]] = r
        a = out
        if trace is not None:
            trace.append((exp, [r[0] for r in a]))
        exp *= 10
        if exp > mx:                                    # no digit left above the largest key's top digit
            break
    return [a, passes]


def brute(records):
    return [sorted([list(r) for r in records], key=lambda r: r[0]), len(str(max(r[0] for r in records)))]


# dry run on the first example
recs = [[170, 1], [45, 2], [75, 3], [90, 4], [802, 5], [24, 6], [2, 7], [66, 8]]
tr = []
res = solve(recs, tr)
print("input keys :", [r[0] for r in recs])
for exp, keys in tr:
    print(f"after digit {len(str(exp)) - 1} (10^{len(str(exp)) - 1}):", keys)
print(res)

for rc, want in [(recs, [[[2, 7], [24, 6], [45, 2], [66, 8], [75, 3], [90, 4], [170, 1], [802, 5]], 3]),
                 ([[5, 1]], [[[5, 1]], 1]),
                 ([[3, 1], [3, 2], [0, 3], [3, 4]], [[[0, 3], [3, 1], [3, 2], [3, 4]], 1])]:
    assert solve(rc) == want == brute(rc), rc
print("all three examples match sorted(key=...) and len(str(max))")

# the counting-sort block of ONE pass, written out for the units digit of the example
digits = [r[0] % 10 for r in recs]
cnt = [0] * 10
for d in digits:
    cnt[d] += 1
print("\nunits digits :", digits)
print("counts       :", cnt)
pre = list(cnt)
for d in range(1, 10):
    pre[d] += pre[d - 1]
print("prefix sums  :", pre, "(digit d fills slots pre[d-1]..pre[d]-1)")

# why backwards: the forward walk puts equal digits in REVERSE input order, so stability is lost
tiny = [[3, 1], [3, 2], [3, 3]]
print("\nbackwards walk:", solve(tiny, backwards=True)[0])
print("forward walk  :", solve(tiny, backwards=False)[0], "(equal keys reversed: NOT stable)")
assert solve(tiny, backwards=False)[0] == [[3, 3], [3, 2], [3, 1]]
# and an unstable pass breaks the radix idea itself: keys that tie on the low digit end up out of order
two = [[21, 0], [11, 1], [12, 2]]
assert solve(two)[0] == [[11, 1], [12, 2], [21, 0]]
print("forward walk on [21, 11, 12]:", [r[0] for r in solve(two, backwards=False)[0]], "| correct:", [r[0] for r in solve(two)[0]])

# passes = digits of the max key, for 0, 9, 10, 99, 100, 10^9
for mx, p in [(0, 1), (9, 1), (10, 2), (99, 2), (100, 3), (10 ** 9, 10)]:
    assert solve([[mx, 0], [0, 1]])[1] == p == len(str(mx))
print("passes for max key 0, 9, 10, 99, 100, 10^9 :", [solve([[m, 0]])[1] for m in (0, 9, 10, 99, 100, 10 ** 9)])

# seeded random cross-check against sorted() and len(str(max))
for _ in range(500):
    n = random.randint(1, 30)
    hi = random.choice([1, 9, 10, 99, 1000, 10 ** 9])
    rc = [[random.randint(0, hi), random.randint(-5, 5)] for _ in range(n)]
    assert solve(rc) == brute(rc)
print("500 seeded random cases match sorted(key=r[0]) (stable) and the pass count")

# maximum size: 10^5 records, keys up to 10^9 -> 10 passes; time is sandbox-only
big = [[random.randint(0, 10 ** 9), i] for i in range(10 ** 5)]
t0 = time.perf_counter()
r = solve(big)
t1 = time.perf_counter()
assert r == brute(big) and r[1] == len(str(max(x[0] for x in big)))
print(f"10^5 records: passes {r[1]}, radix {t1 - t0:.2f}s (sandbox-only timing, not a proof of big-O)")

# edge cases
assert solve([[0, 9]]) == [[[0, 9]], 1] and solve([[7, 1], [7, 2]]) == [[[7, 1], [7, 2]], 1]
assert solve([[10 ** 9, 1], [10 ** 9 - 1, 2]])[0] == [[10 ** 9 - 1, 2], [10 ** 9, 1]]
print("edge asserts ok")
