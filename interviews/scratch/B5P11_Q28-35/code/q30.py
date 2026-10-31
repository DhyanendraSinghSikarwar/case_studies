import itertools, random, sys, time
from functools import lru_cache

random.seed(3001)


def solve(n, cuts):
    """Bottom-up interval DP over boundary points. dp[l][r] = cost to make every cut strictly
    between points[l] and points[r]; the piece being cut first has length points[r] - points[l]."""
    pts = [0] + sorted(cuts) + [n]
    k = len(pts)
    dp = [[0] * k for _ in range(k)]                  # r = l + 1: no cut inside, cost 0
    for gap in range(2, k):                           # interval width in boundary indices
        for l in range(k - gap):
            r = l + gap
            dp[l][r] = pts[r] - pts[l] + min(dp[l][m] + dp[m][r] for m in range(l + 1, r))
    return dp[0][k - 1], pts, dp


def solve_memo(n, cuts):
    """Top-down version. Depth is at most len(cuts) + 2 <= 102, so memoisation is safe here."""
    pts = [0] + sorted(cuts) + [n]

    @lru_cache(maxsize=None)
    def f(l, r):
        if r - l < 2:
            return 0
        return pts[r] - pts[l] + min(f(l, m) + f(m, r) for m in range(l + 1, r))

    return f(0, len(pts) - 1)


def brute(n, cuts):
    """Try every order of the cuts; the cost of a cut is the length of the piece it lands in."""
    best = None
    for order in itertools.permutations(cuts):
        pieces = [(0, n)]
        total = 0
        for x in order:
            for idx, (lo, hi) in enumerate(pieces):
                if lo < x < hi:
                    total += hi - lo
                    pieces[idx:idx + 1] = [(lo, x), (x, hi)]
                    break
        best = total if best is None else min(best, total)
    return 0 if not cuts else best


def greedy_middle(n, cuts):
    """Tempting wrong idea: in each piece first cut the position closest to its middle."""
    def g(lo, hi, inside):
        if not inside:
            return 0
        x = min(inside, key=lambda c: (abs(2 * c - lo - hi), c))
        return (hi - lo) + g(lo, x, [c for c in inside if c < x]) + g(x, hi, [c for c in inside if c > x])
    return g(0, n, sorted(cuts))


# ---- prompt examples
ex = [(7, [1, 3, 4, 5], 16), (9, [5, 6, 1, 4, 2], 22), (10, [], 0), (10, [5], 10)]
for n, cuts, want in ex:
    assert solve(n, cuts)[0] == solve_memo(n, cuts) == brute(n, cuts) == want
print("prompt examples OK")

# ---- table walk-through, first example: points 0 1 3 4 5 7
total, pts, dp = solve(7, [1, 3, 4, 5])
print("points", pts)
print("dp[l][r] (l = row, r = column; only r >= l + 2 is filled by the loop)")
for l, row in enumerate(dp):
    print("  l=%d" % l, row)
print("answer dp[0][%d] = %d" % (len(pts) - 1, total))
# the last cell by hand: boundary 0..7, length 7, split at each inner point
print("dp[0][5] options, split m: " + ", ".join(
    f"m={m}: {dp[0][m]}+{dp[m][5]}" for m in range(1, 5)) + "; best + 7 =", 7 + min(dp[0][m] + dp[m][5] for m in range(1, 5)))

# ---- seeded random cross-check against all orders (len(cuts) <= 6)
cnt = 0
for _ in range(400):
    n = random.randint(2, 30)
    k = random.randint(0, min(6, n - 1))
    cuts = random.sample(range(1, n), k)
    want = brute(n, cuts)
    assert solve(n, cuts)[0] == solve_memo(n, cuts) == want, (n, cuts)
    cnt += 1
print("random cross-check:", cnt, "cases agree with every-order brute force")

# ---- order really matters: spread of costs over all orders of the first example
costs = []
for order in itertools.permutations([1, 3, 4, 5]):
    pieces, tot = [(0, 7)], 0
    for x in order:
        for idx, (lo, hi) in enumerate(pieces):
            if lo < x < hi:
                tot += hi - lo; pieces[idx:idx + 1] = [(lo, x), (x, hi)]; break
    costs.append(tot)
print("first example: 24 orders cost between", min(costs), "and", max(costs))

# ---- greedy 'cut near the middle' is wrong
bad = 0
rg = random.Random(3003)
for _ in range(400):
    n = rg.randint(2, 40)
    cuts = rg.sample(range(1, n), rg.randint(0, min(6, n - 1)))
    bad += greedy_middle(n, cuts) != brute(n, cuts)
print("greedy middle-cut differs from the optimum on", bad, "of 400 random cases")
assert bad > 0

# ---- largest sizes in the prompt: 100 cuts, n = 10^6
rng = random.Random(3002)
big_cuts = rng.sample(range(1, 10**6), 100)
t0 = time.perf_counter()
big = solve(10**6, big_cuts)[0]
dt = time.perf_counter() - t0
assert big == solve_memo(10**6, big_cuts)          # memo depth <= 102 < recursion limit 1000
print("100 cuts, n=10^6:", big, "(memo agrees, depth <= 102)", f"[sandbox time {dt:.2f}s]")

# ---- edge cases
assert solve(2, [1])[0] == 2 and solve(2, [])[0] == 0
assert solve(10, [1, 2, 3])[0] == brute(10, [1, 2, 3])
print("edge cases OK; limit", sys.getrecursionlimit())
