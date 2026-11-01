import random, sys, time
from functools import lru_cache

random.seed(3201)


def solve(values):
    """dp[i][j] = min score to triangulate the sub-polygon with vertices i, i+1, ..., j (edge i-j closes it)."""
    n = len(values)
    dp = [[0] * n for _ in range(n)]                    # j = i + 1: a single edge, no triangle
    for gap in range(2, n):                             # sub-polygon has gap + 1 vertices
        for i in range(n - gap):
            j = i + gap
            dp[i][j] = min(dp[i][k] + dp[k][j] + values[i] * values[k] * values[j]
                           for k in range(i + 1, j))    # apex k of the triangle on edge (i, j)
    return dp[0][n - 1], dp


def solve_memo(values):
    n = len(values)

    @lru_cache(maxsize=None)
    def f(i, j):                                        # depth at most n, safe for n <= 100
        if j - i < 2:
            return 0
        return min(f(i, k) + f(k, j) + values[i] * values[k] * values[j] for k in range(i + 1, j))

    return f(0, n - 1)


def triangulations(vs):
    """Every triangulation of the polygon vs as a list of triangles, by the apex of the edge (first, last)."""
    if len(vs) < 3:
        yield []
        return
    for k in range(1, len(vs) - 1):
        for left in triangulations(vs[:k + 1]):
            for right in triangulations(vs[k:]):
                yield left + right + [(vs[0], vs[k], vs[-1])]


def brute(values):
    """Plain recursion over the apex of the triangle on the edge (first, last)."""
    def f(vs):
        if len(vs) < 3:
            return 0
        return min(vs[0] * vs[k] * vs[-1] + f(vs[:k + 1]) + f(vs[k:]) for k in range(1, len(vs) - 1))
    return f(list(values))


def fan_from_smallest(values):
    """Tempting wrong idea: fan every triangle from the smallest label."""
    n = len(values)
    s = values.index(min(values))
    others = [values[(s + t) % n] for t in range(1, n)]
    return sum(values[s] * others[t] * others[t + 1] for t in range(n - 2))


# ---- prompt examples
ex = [([1, 2, 3], 6), ([3, 7, 4, 5], 144), ([1, 3, 1, 4, 1, 5], 13), ([2, 2, 2, 2, 2], 24)]
for v, want in ex:
    assert solve(v)[0] == solve_memo(v) == brute(v) == want, v
print("prompt examples OK")

# ---- table walk-throughs
for v in ([1, 2, 3], [3, 7, 4, 5]):
    total, dp = solve(v)
    print("values", v)
    for i in range(len(v) - 1):
        for j in range(i + 2, len(v)):
            opts = [f"k={k}: {dp[i][k]}+{dp[k][j]}+{v[i]}*{v[k]}*{v[j]}={dp[i][k] + dp[k][j] + v[i] * v[k] * v[j]}" for k in range(i + 1, j)]
            print(f"  dp[{i}][{j}] = min({'; '.join(opts)}) = {dp[i][j]}")
    print("  answer", total)

# ---- the number of triangulations is a Catalan number; every one has n - 2 triangles
catalan = [1, 1, 2, 5, 14, 42, 132]          # for n = 3..9 vertices: C(n-2)
for n in range(3, 9):
    ts = list(triangulations(list(range(1, n + 1))))
    assert len(ts) == catalan[n - 2] and all(len(t) == n - 2 for t in ts)
print("triangulation counts for n = 3..8:", [len(list(triangulations(list(range(1, n + 1))))) for n in range(3, 9)])

# ---- seeded random cross-check (len <= 8)
cnt = 0
for _ in range(500):
    n = random.randint(3, 8)
    v = [random.randint(1, 100) for _ in range(n)]
    assert solve(v)[0] == solve_memo(v) == brute(v), v
    cnt += 1
print("random cross-check:", cnt, "polygons agree with the apex recursion")

# ---- a second independent oracle: enumerate every triangulation and score it
sc = 0
for _ in range(100):
    n = random.randint(3, 8)
    v = [random.randint(1, 9) for _ in range(n)]
    best = min(sum(a * b * c for a, b, c in t) for t in triangulations(v))
    assert best == solve(v)[0]
    sc += 1
print("enumerate-all-triangulations check:", sc, "polygons agree")

# ---- fan from the smallest vertex is not always optimal
rg = random.Random(3202)
bad = 0
for _ in range(500):
    v = [rg.randint(1, 20) for _ in range(rg.randint(4, 8))]
    bad += fan_from_smallest(v) != solve(v)[0]
print("fan from the smallest label differs from the optimum on", bad, "of 500 random polygons")
assert bad > 0

# ---- largest size: n = 100 (C(100,3) = 161,700 inner steps)
rb = random.Random(3203)
big = [rb.randint(1, 100) for _ in range(100)]
t0 = time.perf_counter()
res = solve(big)[0]
dt = time.perf_counter() - t0
assert res == solve_memo(big)
print("n=100:", res, "(memoised version agrees, recursion depth <= 100)", f"[sandbox time {dt:.2f}s]")

# ---- edge cases
assert solve([1, 1, 1])[0] == 1 and solve([100] * 3)[0] == 10**6
assert solve([5, 5, 5, 5])[0] == 250
print("edge cases OK; limit", sys.getrecursionlimit())
