import itertools, math, random, sys, time
from functools import lru_cache

random.seed(3501)
INF = float("inf")


def tsp(dist):
    """f[mask][last] = cheapest path that starts at 0, visits exactly the cities in mask (bit 0 always set)
    and ends at last. Masks are filled in increasing order, so every predecessor mask is already final."""
    n = len(dist)
    if n == 1:
        return 0, None
    f = [[INF] * n for _ in range(1 << n)]
    f[1][0] = 0                                           # only city 0 visited, standing at 0
    for mask in range(1, 1 << n, 2):                      # odd masks = contain city 0
        for last in range(n):
            cur = f[mask][last]
            if cur == INF:
                continue
            for nxt in range(1, n):
                if not mask >> nxt & 1:
                    nm = mask | 1 << nxt
                    v = cur + dist[last][nxt]
                    if v < f[nm][nxt]:
                        f[nm][nxt] = v
    full = (1 << n) - 1
    return min(f[full][last] + dist[last][0] for last in range(1, n)), f


def tsp_halved(dist):
    """Same DP with city 0 left out of the mask: 2^(n-1) masks instead of 2^n (half the table)."""
    n = len(dist)
    if n == 1:
        return 0
    m = n - 1                                             # cities 1..n-1 get bits 0..m-1
    f = [[INF] * m for _ in range(1 << m)]
    for c in range(m):
        f[1 << c][c] = dist[0][c + 1]
    for mask in range(1, 1 << m):
        for last in range(m):
            cur = f[mask][last]
            if cur == INF:
                continue
            for nxt in range(m):
                if not mask >> nxt & 1:
                    nm = mask | 1 << nxt
                    v = cur + dist[last + 1][nxt + 1]
                    if v < f[nm][nxt]:
                        f[nm][nxt] = v
    return min(f[(1 << m) - 1][last] + dist[last + 1][0] for last in range(m))


def tsp_memo(dist):
    """Top-down, the other direction: g(mask, last) = cheapest way to finish from here. Depth n <= 12."""
    n = len(dist)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def g(mask, last):
        if mask == full:
            return dist[last][0]
        return min(dist[last][c] + g(mask | 1 << c, c) for c in range(n) if not mask >> c & 1)

    return 0 if n == 1 else g(1, 0)


def tsp_route(dist):
    """Follow-up: recover one optimal tour by walking the table backwards (ties: smallest previous city)."""
    n = len(dist)
    if n == 1:
        return 0, [0, 0]
    best, f = tsp(dist)
    full = (1 << n) - 1
    last = min((l for l in range(1, n) if f[full][l] + dist[l][0] == best))
    route, mask = [0], full
    while mask != 1:
        route.append(last)
        pm = mask ^ (1 << last)
        prev = next(p for p in range(n) if pm >> p & 1 and f[pm][p] + dist[p][last] == f[mask][last])
        mask, last = pm, prev
    route.append(0)
    route.reverse()
    return best, route


def brute(dist):
    n = len(dist)
    if n == 1:
        return 0
    return min(sum(dist[a][b] for a, b in zip((0,) + p, p + (0,))) for p in itertools.permutations(range(1, n)))


# ---- prompt examples
ex = [([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], 80),
      ([[0]], 0), ([[0, 3], [5, 0]], 8), ([[0, 1, 9], [9, 0, 1], [1, 9, 0]], 3)]
for d, want in ex:
    assert tsp(d)[0] == tsp_halved(d) == tsp_memo(d) == brute(d) == want, d
print("prompt examples OK")

# ---- hand table, first example: f[mask][last] (mask lists cities visited, city 0 always in it)
d = ex[0][0]
best, f = tsp(d)
print("f[mask][last]  (cities in mask, ending at last)")
for mask in range(1, 16, 2):
    cities = [c for c in range(4) if mask >> c & 1]
    cells = {l: f[mask][l] for l in range(4) if f[mask][l] != INF}
    print(f"  mask {mask:04b} {cities}: {cells}")
full = 15
print("closing:", {l: f"{f[full][l]}+{d[l][0]}={f[full][l] + d[l][0]}" for l in range(1, 4)}, "-> best", best)
print("one optimal tour:", tsp_route(d))

# ---- seeded cross-check against every permutation (n <= 8), asymmetric distances, many ties
cnt = 0
for _ in range(300):
    n = random.randint(1, 8)
    hi = random.choice([2, 10, 1000])
    d = [[0 if a == b else random.randint(0, hi) for b in range(n)] for a in range(n)]
    want = brute(d)
    assert tsp(d)[0] == tsp_halved(d) == tsp_memo(d) == want, (d, want)
    cost, route = tsp_route(d)
    assert cost == want and sorted(route[:-1]) == list(range(n)) and route[0] == route[-1] == 0
    if n > 1:
        assert sum(d[a][b] for a, b in zip(route, route[1:])) == want
    cnt += 1
print("random cross-check:", cnt, "matrices agree (also the half-size table, the memo and the recovered tour)")

# ---- the permutation search against the DP
print(" n | (n-1)! tours | 2^n * n^2 DP steps")
for n in (8, 10, 11, 12, 13, 15):
    print(f"{n:>2} | {math.factorial(n - 1):>13,} | {(1 << n) * n * n:>12,}")
rg = random.Random(3502)
for n in (9, 10):
    d = [[0 if a == b else rg.randint(0, 1000) for b in range(n)] for a in range(n)]
    t0 = time.perf_counter(); a = brute(d); t_b = time.perf_counter() - t0
    t0 = time.perf_counter(); b = tsp(d)[0]; t_d = time.perf_counter() - t0
    assert a == b
    print(f"n={n}: permutations {t_b:.2f}s, DP {t_d:.3f}s  [sandbox time only]")
d = [[0 if a == b else rg.randint(0, 1000) for b in range(12)] for a in range(12)]
t0 = time.perf_counter(); r12 = tsp(d)[0]; t_d = time.perf_counter() - t0
assert r12 == tsp_halved(d) == tsp_memo(d)
print(f"n=12: DP {t_d:.2f}s -> {r12}; 11! = {math.factorial(11):,} tours would need the permutation loop to run that many times (not run)")

# ---- edge cases
assert tsp([[0]])[0] == 0 and tsp([[0, 7], [2, 0]])[0] == 9
assert tsp([[0] * 5 for _ in range(5)])[0] == 0
assert tsp([[0 if a == b else 1000 for b in range(12)] for a in range(12)])[0] == 12000
print("edge cases OK; limit", sys.getrecursionlimit())
