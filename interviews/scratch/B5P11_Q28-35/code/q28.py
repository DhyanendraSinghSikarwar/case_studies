import itertools, random
from math import comb

random.seed(2801)
MOD = 10**9 + 7
INF = float("inf")


def solve_tables(grid):
    """Bottom-up with two full tables: cost[i][j], ways[i][j] (best path into (i,j))."""
    m, n = len(grid), len(grid[0])
    cost = [[INF] * n for _ in range(m)]
    ways = [[0] * n for _ in range(m)]
    cost[0][0], ways[0][0] = grid[0][0], 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            up = cost[i - 1][j] if i else INF
            left = cost[i][j - 1] if j else INF
            best = min(up, left)
            w = 0
            if up == best:
                w += ways[i - 1][j]
            if left == best:
                w += ways[i][j - 1]
            cost[i][j] = best + grid[i][j]      # true value, never reduced
            ways[i][j] = w % MOD                # only the count is reduced
    return [cost[-1][-1], ways[-1][-1]], cost, ways


def solve(grid):
    return solve_tables(grid)[0]


def solve_one_row(grid):
    """Space O(n): one row of cost and one row of ways, updated left to right."""
    m, n = len(grid), len(grid[0])
    cost, ways = [INF] * n, [0] * n
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                cost[0], ways[0] = grid[0][0], 1
                continue
            up = cost[j] if i else INF            # still holds row i-1
            left = cost[j - 1] if j else INF      # already row i
            best = min(up, left)
            w = (ways[j] if up == best else 0) + (ways[j - 1] if j and left == best else 0)
            cost[j], ways[j] = best + grid[i][j], w % MOD
    return [cost[-1], ways[-1]]


def solve_memo(grid):
    """Top-down, the other direction: best (cost, ways) of a path from (i,j) to the end."""
    from functools import lru_cache
    m, n = len(grid), len(grid[0])

    @lru_cache(maxsize=None)
    def f(i, j):
        if i == m - 1 and j == n - 1:
            return (grid[i][j], 1)
        opts = []
        if i + 1 < m:
            opts.append(f(i + 1, j))
        if j + 1 < n:
            opts.append(f(i, j + 1))
        best = min(c for c, _ in opts)
        return (grid[i][j] + best, sum(w for c, w in opts if c == best) % MOD)

    return list(f(0, 0))


def brute(grid):
    """Enumerate every path: choose which of the m+n-2 moves are Down."""
    m, n = len(grid), len(grid[0])
    totals = []
    for downs in itertools.combinations(range(m + n - 2), m - 1):
        d = set(downs)
        i = j = 0
        tot = grid[0][0]
        for step in range(m + n - 2):
            if step in d:
                i += 1
            else:
                j += 1
            tot += grid[i][j]
        totals.append(tot)
    best = min(totals)
    return [best, totals.count(best) % MOD]


# ---- prompt examples
ex = [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], [7, 1]), ([[0, 0], [0, 0]], [0, 2]),
      ([[7]], [7, 1]), ([[1, 2], [2, 1]], [4, 2])]
for g, want in ex:
    assert solve(g) == solve_one_row(g) == solve_memo(g) == brute(g) == want, g
print("prompt examples OK")

# ---- table walk-through on example 1
res, cost, ways = solve_tables(ex[0][0])
print("grid  ", ex[0][0])
print("cost  ", cost)
print("ways  ", ways)
print("answer", res)
res2, cost2, ways2 = solve_tables(ex[3][0])
print("tie grid", ex[3][0], "cost", cost2, "ways", ways2, "answer", res2)

# ---- seeded cross-check against enumerating every path (m, n <= 5)
checked = ties = 0
for t in range(600):
    m, n = random.randint(1, 5), random.randint(1, 5)
    hi = random.choice([1, 2, 9])                 # small values force many ties
    g = [[random.randint(0, hi) for _ in range(n)] for _ in range(m)]
    want = brute(g)
    assert solve(g) == solve_one_row(g) == solve_memo(g) == want, (g, want)
    checked += 1
    ties += want[1] > 1
print("random cross-check:", checked, "grids agree;", ties, "had more than one optimal path")

# ---- why the count needs the modulus: all-zero 100 x 100, every path is optimal
big = [[0] * 100 for _ in range(100)]
r = solve(big)
true_count = comb(198, 99)
assert r == [0, true_count % MOD] == solve_one_row(big) == solve_memo(big)
print("100x100 zeros: cost", r[0], "| true count has", len(str(true_count)), "digits | mod ->", r[1])
assert true_count > MOD
print("largest possible cost 9*199 =", 9 * 199, "(far below the modulus)")

# ---- recursion depth of the memoised version is m + n - 1 (199 at the limit size)
import sys
print("recursion limit", sys.getrecursionlimit(), "| memo depth at 100x100 is", 100 + 100 - 1, "-> fine")

# ---- wrong variants, counted on the same random grids
def wrong_add_always(grid):
    m, n = len(grid), len(grid[0])
    cost = [[0] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == j == 0:
                cost[0][0], ways[0][0] = grid[0][0], 1; continue
            cands = ([(cost[i-1][j], ways[i-1][j])] if i else []) + ([(cost[i][j-1], ways[i][j-1])] if j else [])
            cost[i][j] = min(c for c, _ in cands) + grid[i][j]
            ways[i][j] = sum(w for _, w in cands) % MOD         # ignores which predecessor is cheaper
    return [cost[-1][-1], ways[-1][-1]]

def wrong_first_only(grid):
    m, n = len(grid), len(grid[0])
    cost = [[0] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == j == 0:
                cost[0][0], ways[0][0] = grid[0][0], 1; continue
            cands = ([(cost[i-1][j], ways[i-1][j])] if i else []) + ([(cost[i][j-1], ways[i][j-1])] if j else [])
            c, w = min(cands, key=lambda x: x[0])               # min() keeps the first on a tie: drops the other
            cost[i][j] = c + grid[i][j]; ways[i][j] = w
    return [cost[-1][-1], ways[-1][-1]]

def wrong_cost_mod(grid, p=5):
    """Artificial small modulus on the cost too: comparisons then lie."""
    m, n = len(grid), len(grid[0])
    cost = [[0] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == j == 0:
                cost[0][0], ways[0][0] = grid[0][0] % p, 1; continue
            cands = ([(cost[i-1][j], ways[i-1][j])] if i else []) + ([(cost[i][j-1], ways[i][j-1])] if j else [])
            b = min(c for c, _ in cands)
            cost[i][j] = (b + grid[i][j]) % p
            ways[i][j] = sum(w for c, w in cands if c == b) % MOD
    return [cost[-1][-1], ways[-1][-1]]

rnd = random.Random(2802)
bad = {"add both always": 0, "first on tie only": 0, "cost reduced (mod 5)": 0}
N = 500
for _ in range(N):
    m, n = rnd.randint(2, 5), rnd.randint(2, 5)
    g = [[rnd.randint(0, 3) for _ in range(n)] for _ in range(m)]
    want = brute(g)
    bad["add both always"] += wrong_add_always(g) != want
    bad["first on tie only"] += wrong_first_only(g) != want
    bad["cost reduced (mod 5)"] += wrong_cost_mod(g) != want
print("wrong variants differing from the oracle out of", N, ":", bad)

# ---- edge cases
assert solve([[0]]) == [0, 1]
assert solve([[5] * 7]) == [35, 1] and solve([[5]] * 7) == [35, 1]       # one row / one column: one path
assert solve([[9] * 100 for _ in range(100)]) == [9 * 199, comb(198, 99) % MOD]
print("edge cases OK")
