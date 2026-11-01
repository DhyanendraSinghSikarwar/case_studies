import random, sys, time
from functools import lru_cache
from math import comb

random.seed(2901)


def stats_forward(m, n, blocked):
    """[paths, entries, depth] with NO recursion: a forward table, one row at a time.
    called = the cell is reached by some call of f; expanded = called, open and not the end,
    so it calls its right/down neighbours. w = number of right/down paths from (0,0)."""
    rows = {}
    for r, c in blocked:
        rows.setdefault(r, set()).add(c)
    w_prev = [0] * n
    ex_prev = [False] * n                    # expanded flags of the previous row
    entries, depth = 0, 1
    for i in range(m):
        bl = rows.get(i, ())
        w_cur = [0] * n
        ex_cur = [False] * n
        last = -1                            # last called column in this row
        for j in range(n):
            called = (i == 0 and j == 0) or (i > 0 and ex_prev[j]) or (j > 0 and ex_cur[j - 1])
            if not called:
                continue
            entries += 1
            if i + j + 1 > depth:
                depth = i + j + 1
            if j in bl:
                continue                     # blocked: f returns 0, calls nothing, w stays 0
            ex_cur[j] = not (i == m - 1 and j == n - 1)
        for j in range(n):
            if j in bl:
                continue
            if i == 0 and j == 0:
                w_cur[0] = 1
            else:
                w_cur[j] = (w_prev[j] if i else 0) + (w_cur[j - 1] if j else 0)
        w_prev, ex_prev = w_cur, ex_cur
    return [w_prev[n - 1], entries, depth]


def stats_recursive(m, n, blocked):
    """Oracle: the real lru_cache recursion, instrumented for depth and cache size."""
    bl = {(r, c) for r, c in blocked}
    st = {"now": 0, "max": 0}

    @lru_cache(maxsize=None)
    def f(i, j):
        st["now"] += 1
        st["max"] = max(st["max"], st["now"])
        try:
            if (i, j) in bl:
                return 0
            if (i, j) == (m - 1, n - 1):
                return 1
            total = 0
            if i + 1 < m:
                total += f(i + 1, j)
            if j + 1 < n:
                total += f(i, j + 1)
            return total
        finally:
            st["now"] -= 1

    r = f(0, 0)
    return [r, f.cache_info().currsize, st["max"]]


# ---- prompt examples (the 600 x 600 one is checked against C(1198, 599) as well)
ex = [(3, 3, [], [6, 9, 5]), (3, 3, [[1, 1]], [2, 9, 5]), (2, 4, [[0, 0]], [0, 1, 1]),
      (1, 1, [], [1, 1, 1]), (4, 3, [[0, 1], [1, 0]], [0, 3, 2])]
for m, n, b, want in ex:
    assert stats_forward(m, n, b) == stats_recursive(m, n, b) == want, (m, n, b)
r = stats_forward(600, 600, [])
assert r == [comb(1198, 599), 360000, 1199]
print("examples OK; 600x600 ->", len(str(r[0])), "digit path count,", r[1], "entries, depth", r[2])

# ---- walk-through on the first example: which cells are called, path counts, depth = i + j + 1
m, n = 3, 3
print("3x3 no blocks: depth of a call at (i,j) is i+j+1")
for i in range(m):
    print("  ", [i + j + 1 for j in range(n)], "  paths-from-start", [comb(i + j, i) for j in range(n)])
print("  forward answer", stats_forward(3, 3, []))

# ---- seeded cross-check against the instrumented recursion, m, n <= 12
cnt = zero = 0
for _ in range(1500):
    m, n = random.randint(1, 12), random.randint(1, 12)
    cells = [[r, c] for r in range(m) for c in range(n)]
    k = random.randint(0, min(len(cells), random.choice([0, 3, m * n // 3])))
    blocked = random.sample(cells, k)
    got, want = stats_forward(m, n, blocked), stats_recursive(m, n, blocked)
    assert got == want, (m, n, blocked, got, want)
    cnt += 1
    zero += got[0] == 0
print("random cross-check:", cnt, "cases agree;", zero, "of them have 0 paths")

# ---- claim: every call at cell (i, j) sits at depth i + j + 1, so depth = 1 + max(i+j) over called cells.
# Tested through the instrumented oracle on cases with a blocked wall that cuts the grid short.
r = stats_recursive(10, 10, [[0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0]])
print("anti-diagonal wall at i+j=5 on 10x10 (all 6 cells blocked):", r, "-> depth 6 = 5 + 1")
assert r == [0, 21, 6] == stats_forward(10, 10, [[0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0]])

# ---- what actually raises RecursionError: depth, not path count and not cache size
print("default recursion limit:", sys.getrecursionlimit())
for size in (400, 600):
    try:
        out = stats_recursive(size, size, [])
        print(f"  memoised {size}x{size}: depth {out[2]}, entries {out[1]} -> ran fine")
    except RecursionError:
        print(f"  memoised {size}x{size}: expected depth {2 * size - 1}, entries 360000 -> RecursionError")

# ---- hashable key: a tuple works, a list does not
@lru_cache(maxsize=None)
def g(cell):
    return sum(cell)
print("tuple key:", g((1, 2)))
try:
    g([1, 2])
except TypeError as e:
    print("list key ->", type(e).__name__ + ":", e)

# ---- size limit of the prompt: forward table, 1500 x 1500 with 10^4 blocked cells (timing is sandbox-only)
rng = random.Random(2902)
blocked = [[r // 1500, r % 1500] for r in rng.sample(range(1500 * 1500), 10**4)]
t0 = time.perf_counter()
res = stats_forward(1500, 1500, blocked)
dt = time.perf_counter() - t0
print("1500x1500, 10^4 blocked: paths has", len(str(res[0])), "digits (or 0 if blocked start/end),",
      "entries", res[1], "depth", res[2], f"[sandbox time {dt:.1f}s]")

# ---- edge cases
assert stats_forward(1, 1, [[0, 0]]) == [0, 1, 1] == stats_recursive(1, 1, [[0, 0]])
assert stats_forward(2, 2, [[1, 1]]) == [0, 4, 3] == stats_recursive(2, 2, [[1, 1]])     # end blocked: still called
assert stats_forward(1, 7, []) == [1, 7, 7]                                              # one row: a chain
print("edge cases OK")
