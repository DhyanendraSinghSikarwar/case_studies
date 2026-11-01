import itertools, random, sys, time
from functools import lru_cache

random.seed(3401)
NEG = float("-inf")


def solve(grid, trace=None):
    """State (k, r1, r2): both walkers have made k right/down moves, so their columns are k - r1, k - r2.
    dp[r1][r2] = most cherries collected by the pair so far; NEG = unreachable. Rolls over k: O(n^2) space."""
    n = len(grid)
    dp = [[NEG] * n for _ in range(n)]
    if grid[0][0] == -1:
        return 0
    dp[0][0] = grid[0][0]
    if trace is not None:
        trace.append((0, {(0, 0): dp[0][0]}))
    for k in range(1, 2 * n - 1):
        nd = [[NEG] * n for _ in range(n)]
        for r1 in range(max(0, k - n + 1), min(n, k + 1)):
            c1 = k - r1
            if grid[r1][c1] == -1:
                continue
            for r2 in range(r1, min(n, k + 1)):          # r2 >= r1 by symmetry: swapping walkers changes nothing
                c2 = k - r2
                if r2 < max(0, k - n + 1) or grid[r2][c2] == -1:
                    continue
                best = max(dp[a][b] for a in (r1, r1 - 1) for b in (r2, r2 - 1)
                           if a >= 0 and b >= 0 and (a <= b))    # previous row pair, kept in r1 <= r2 form
                if best == NEG:
                    continue
                gain = grid[r1][c1] + (grid[r2][c2] if r2 != r1 else 0)   # a shared cell counts once
                nd[r1][r2] = best + gain
        dp = nd
        if trace is not None:
            trace.append((k, {(a, b): dp[a][b] for a in range(n) for b in range(n) if dp[a][b] != NEG}))
    return 0 if dp[n - 1][n - 1] == NEG else dp[n - 1][n - 1]


def solve_memo(grid):
    """Top-down version: depth 2n - 1 <= 99 for n <= 50, so memoisation is safe."""
    n = len(grid)

    @lru_cache(maxsize=None)
    def f(k, r1, r2):                                    # best total from step k to the end, walkers at rows r1, r2
        c1, c2 = k - r1, k - r2
        if r1 >= n or r2 >= n or c1 >= n or c2 >= n or grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return NEG
        gain = grid[r1][c1] + (grid[r2][c2] if r1 != r2 else 0)
        if k == 2 * n - 2:
            return gain
        nxt = max(f(k + 1, r1 + a, r2 + b) for a in (0, 1) for b in (0, 1))
        return NEG if nxt == NEG else gain + nxt

    r = f(0, 0, 0)
    return 0 if r == NEG else r


def all_paths(n):
    for downs in itertools.combinations(range(2 * n - 2), n - 1):
        d = set(downs)
        i = j = 0
        cells = [(0, 0)]
        for s in range(2 * n - 2):
            if s in d:
                i += 1
            else:
                j += 1
            cells.append((i, j))
        yield cells


def brute(grid):
    """Every pair of right/down paths; cherries on the union of cells (a shared cell once)."""
    n = len(grid)
    ps = [p for p in all_paths(n) if all(grid[a][b] != -1 for a, b in p)]
    best = 0
    for p in ps:
        for q in ps:
            best = max(best, sum(grid[a][b] for a, b in set(p) | set(q)))
    return best


def literal_trip(grid):
    """The statement read literally (tiny n): walk down-right picking cherries, then walk back up-left
    over the same grid with those cherries gone. Tests the 'second walker' reduction itself."""
    n = len(grid)
    best = 0
    for p in all_paths(n):
        if any(grid[a][b] == -1 for a, b in p):
            continue
        got = sum(grid[a][b] for a, b in p)
        g2 = [row[:] for row in grid]
        for a, b in p:
            g2[a][b] = 0 if g2[a][b] == 1 else g2[a][b]
        # return trip: left/up moves from (n-1, n-1) to (0, 0) = a right/down path read backwards
        back = 0
        for q in all_paths(n):
            if any(g2[a][b] == -1 for a, b in q):
                continue
            back = max(back, sum(g2[a][b] for a, b in q))
        best = max(best, got + back)
    return best


def greedy_two_trips(grid):
    """Wrong: take the best single trip, clear it, then take the best second trip."""
    n = len(grid)
    ps = [p for p in all_paths(n) if all(grid[a][b] != -1 for a, b in p)]
    if not ps:
        return 0
    first = max(ps, key=lambda p: sum(grid[a][b] for a, b in p))
    g2 = [row[:] for row in grid]
    for a, b in first:
        g2[a][b] = 0 if g2[a][b] == 1 else g2[a][b]
    return sum(grid[a][b] for a, b in first) + max(sum(g2[a][b] for a, b in p) for p in ps)


# ---- prompt examples
ex = [([[0, 1, -1], [1, 0, -1], [1, 1, 1]], 5), ([[1, 1, -1], [1, -1, 1], [-1, 1, 1]], 0),
      ([[1]], 1), ([[0, 0], [0, 0]], 0)]
for g, want in ex:
    assert solve(g) == solve_memo(g) == brute(g) == want, g
print("prompt examples OK")

# ---- walk-through of the first example: reachable (r1, r2) pairs per step (r1 <= r2), value = cherries so far
g = ex[0][0]
tr = []
solve(g, tr)
print("grid", g)
for k, cells in tr:
    print(f"  k={k}:", {f"r1={a},r2={b} (c={k - a},{k - b})": v for (a, b), v in cells.items()})
print("answer dp[k=4][2][2] =", solve(g))

# ---- seeded cross-check: DP vs every pair of paths (n <= 5); small n also vs the literal go-and-return reading
cnt = zero = 0
for _ in range(500):
    n = random.randint(1, 5)
    p_thorn = random.choice([0.0, 0.15, 0.3])
    g = [[(-1 if random.random() < p_thorn else random.randint(0, 1)) for _ in range(n)] for _ in range(n)]
    g[0][0] = random.choice([g[0][0], 0, 1]) if random.random() < 0.8 else g[0][0]
    want = brute(g)
    assert solve(g) == solve_memo(g) == want, (g, want)
    if n <= 3:
        assert literal_trip(g) == want, g
    cnt += 1
    zero += want == 0
print("random cross-check:", cnt, "grids agree with the pair-of-paths brute force;", zero, "have answer 0")

# ---- the reduction itself: literal go-and-return reading equals the pair of paths (exhaustive, n <= 3, no thorns)
c = 0
for n in (1, 2, 3):
    for flat in itertools.product((0, 1), repeat=n * n):
        g = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
        assert literal_trip(g) == brute(g) == solve(g)
        c += 1
print("exhaustive 0/1 grids n <= 3:", c, "agree, literal reading included")

# ---- two separate greedy trips fail
bad = 0
rg = random.Random(3402)
example = None
for _ in range(500):
    n = rg.randint(3, 5)
    g = [[rg.choice((0, 0, 1, 1, 1, -1)) for _ in range(n)] for _ in range(n)]
    g[0][0] = g[n - 1][n - 1] = 0
    want = brute(g)
    if greedy_two_trips(g) != want:
        bad += 1
        if example is None or n < len(example[0]):
            example = (g, greedy_two_trips(g), want)
print("two greedy trips wrong on", bad, "of 500 random grids; smallest:", example)
assert bad > 0

# ---- largest size n = 50 (2n-1 steps, about n^2 / 2 row pairs each), sandbox time only
rb = random.Random(3403)
n = 50
big = [[(-1 if rb.random() < 0.08 else rb.randint(0, 1)) for _ in range(n)] for _ in range(n)]
big[0][0] = big[n - 1][n - 1] = 0
t0 = time.perf_counter()
res = solve(big)
dt = time.perf_counter() - t0
assert res == solve_memo(big)
print("n=50 random:", res, "(memo agrees, recursion depth 99)", f"[sandbox time {dt:.2f}s]")

# ---- edge cases
assert solve([[-1]]) == 0 and solve([[0]]) == 0
assert solve([[1, 1], [1, 1]]) == 4
assert solve([[0, -1], [-1, 0]]) == 0                # both ways blocked
assert solve([[1] * 4 for _ in range(4)]) == 12 == brute([[1] * 4 for _ in range(4)])   # 2*7 cells - the 2 shared ends
print("edge cases OK; limit", sys.getrecursionlimit())
