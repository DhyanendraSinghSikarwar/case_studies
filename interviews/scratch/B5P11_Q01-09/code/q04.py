import itertools
import random
import sys
from functools import lru_cache

random.seed(1104)
INF = float('inf')

def tri_bottom_up(triangle):
    """dp starts as the last row. Cell (r, j) has two children (r+1, j) and (r+1, j+1), always in range."""
    dp = list(triangle[-1])                       # copy: do not mutate the caller's input
    for r in range(len(triangle) - 2, -1, -1):
        for j in range(r + 1):
            dp[j] = triangle[r][j] + min(dp[j], dp[j + 1])
    return dp[0]

def tri_top_down(triangle):
    """Top-down rows (forward): cell (r, j) has parents (r-1, j-1) and (r-1, j); the edges miss one."""
    dp = [triangle[0][0]]
    for r in range(1, len(triangle)):
        new = []
        for j in range(r + 1):
            left = dp[j - 1] if j - 1 >= 0 else INF     # leftmost cell has no up-left parent
            right = dp[j] if j <= r - 1 else INF        # rightmost cell has no up parent
            new.append(triangle[r][j] + min(left, right))
        dp = new
    return min(dp)                                       # must scan the last row

def tri_top_down_inplace(triangle, descending=True):
    """One row top-down in place: needs j descending so dp[j-1] is still the previous row."""
    dp = [INF] * len(triangle)
    dp[0] = 0
    for r, row in enumerate(triangle):
        order = range(r, -1, -1) if descending else range(r + 1)
        for j in order:
            dp[j] = row[j] + min(dp[j], dp[j - 1] if j else INF)
    return min(dp[:len(triangle)])

def tri_plain(triangle):
    """Oracle: plain recursion, no memo."""
    def f(r, j):
        return triangle[r][j] + (min(f(r + 1, j), f(r + 1, j + 1)) if r + 1 < len(triangle) else 0)
    return f(0, 0)

def tri_memo(triangle):
    @lru_cache(maxsize=None)
    def f(r, j):
        return triangle[r][j] + (min(f(r + 1, j), f(r + 1, j + 1)) if r + 1 < len(triangle) else 0)
    return f(0, 0)

def make(r, lo=-10, hi=10):
    return [[random.randint(lo, hi) for _ in range(i + 1)] for i in range(r)]

for t, want in [([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]], 11), ([[-10]], -10), ([[1], [2, 3]], 3), ([[-1], [2, 3], [1, -1, -3]], -1)]:
    assert tri_bottom_up(t) == tri_top_down(t) == tri_plain(t) == tri_memo([tuple(x) for x in t]) == want, t
print("4 prompt examples ok")

t = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
print("walk-through triangle:", t)
dp = list(t[-1]); print("  start (last row):", dp)
for r in range(len(t) - 2, -1, -1):
    for j in range(r + 1):
        dp[j] = t[r][j] + min(dp[j], dp[j + 1])
    print("  after row", r, ":", dp[:r + 1])

orig = [list(x) for x in t]
tri_bottom_up(t)
assert t == orig
print("input not mutated: ok")

# exhaustive on all triangles with r <= 4 and values in {-1, 0, 1} (r=4 has 10 cells: 59049)
cnt = 0
for r in range(1, 5):
    for cells in itertools.product((-1, 0, 1), repeat=r * (r + 1) // 2):
        it = iter(cells)
        tri = [[next(it) for _ in range(i + 1)] for i in range(r)]
        o = tri_plain(tri)
        assert tri_bottom_up(tri) == tri_top_down(tri) == tri_top_down_inplace(tri) == o, tri
        cnt += 1
print("exhaustive:", cnt, "triangles (r <= 4, values -1..1): bottom-up == top-down == in-place == plain recursion")
for _ in range(500):
    r = random.randint(1, 8)
    tri = make(r, -10000, 10000)
    assert tri_bottom_up(tri) == tri_top_down(tri) == tri_plain(tri) == tri_top_down_inplace(tri)
print("500 seeded random triangles (r <= 8, |value| <= 10^4): ok")

# claim: the in-place top-down version needs j descending. Test it.
wrong = 0
total = 0
for r in range(2, 5):
    for cells in itertools.product((-1, 0, 1), repeat=r * (r + 1) // 2):
        it = iter(cells)
        tri = [[next(it) for _ in range(i + 1)] for i in range(r)]
        total += 1
        wrong += tri_top_down_inplace(tri, descending=False) != tri_plain(tri)
print("top-down in place with ASCENDING j: wrong on", wrong, "of", total, "small triangles")

# size 200
big = make(200, -10000, 10000)
a = tri_bottom_up(big)
assert a == tri_top_down(big) == tri_top_down_inplace(big)
print("r = 200: bottom-up == top-down == in-place:", a)
print("r = 200 memo (depth 200 frames, limit", sys.getrecursionlimit(), "):", tri_memo([tuple(x) for x in big]) == a)
