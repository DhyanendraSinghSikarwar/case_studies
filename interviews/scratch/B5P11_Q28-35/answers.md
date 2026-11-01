### Q28 ⭐ 🟡 Count the minimum-cost paths (counting versus optimising). `grid` is an m x n list of lists (1 <= m, n <= 100) of integers in 0..9. Moves are right or down from the top-left to the bottom-right. Return `[best, ways]`: the minimum path sum and the number of distinct paths that reach it, modulo 10^9 + 7. Keep two tables (cost and count), say how the count merges when both predecessors tie, when it is taken from one predecessor and when it is added, and why the modulus is applied to the count only, never to the cost (comparisons need the true value). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) on small inputs. Example: grid=[[1, 3, 1], [1, 5, 1], [4, 2, 1]] -> [7, 1]; grid=[[0, 0], [0, 0]] -> [0, 2]; grid=[[7]] -> [7, 1]; grid=[[1, 2], [2, 1]] -> [4, 2].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 2D grid DP with a second table. One table optimises (minimum cost into each cell), one counts (how many paths achieve that minimum). It is "optimise, then count the optimal ones" on a DAG.

**Say this first (1 line):** "Two tables: `cost[i][j]` is the cheapest sum of a path into the cell, `ways[i][j]` is how many paths reach that cost; ties add the counts, a strictly cheaper predecessor hands over its count, and only the count is taken modulo 10^9 + 7. O(m*n) time, O(n) space."

**Brute force:** Enumerate every right/down path: choose which `m + n - 2` moves are Down, that is C(m+n-2, m-1) paths (70 for 5 x 5, but about 10^58 for 100 x 100). Take the minimum and count how often it occurs. It is the oracle for m, n <= 5.

**Optimal:**
- State: `cost[i][j]` = minimum sum over paths from (0,0) to (i,j) inclusive; `ways[i][j]` = number of paths that achieve exactly that sum (mod p).
- Transition: the last move came from above or from the left. `best = min(cost[i-1][j], cost[i][j-1])`, then `cost[i][j] = best + grid[i][j]`.
- Count merge, three cases:
  - Both predecessors have cost == best (a tie): `ways = ways[up] + ways[left]`. Both families of paths are optimal and disjoint (different last move).
  - Exactly one predecessor has cost == best: `ways` is copied from that one. The other predecessor's paths are strictly worse into this cell, so they do not count.
  - Border cell (first row or column): only one predecessor exists, so the count is copied from it.
- Base: `cost[0][0] = grid[0][0]`, `ways[0][0] = 1` (the empty path is one path). Missing predecessors are treated as cost infinity, which never ties with a real number.
- Why the modulus touches the count only: the count is compared with nothing, it is only added, and it grows like a binomial coefficient (the all-zero 100 x 100 grid has C(198,99), a 59-digit number of optimal paths, hence the modulus). The cost is compared with `min` and `==` at every cell, so it must stay the true value. A reduced cost can make a worse path look cheaper or break a tie. In this prompt the cost is at most 9 * 199 = 1791, far below 10^9 + 7, so reducing it would happen to be harmless here; the rule matters as soon as values are large, and the code shows the damage with an artificial modulus of 5.
- Memoised version: `f(i, j)` returns the best `(cost, ways)` of a path from (i,j) to the end (the other direction). Its recursion nests m + n - 1 deep, at most 199 for 100 x 100, which is under CPython's default limit of 1000 (observed on 3.13: the 100 x 100 run is fine). If the grid size were not capped, a depth of m + n - 1 above the limit would fail (Q29 measures exactly that), so bottom-up is the safe default.
- Space: row i reads row i-1 (same column) and the cell to its left, so one row of `cost` and one row of `ways`, updated left to right, is enough: O(n).

**Complexity:** Time O(m*n), each cell does O(1) work. Space O(m*n) for two full tables, O(n) with the single-row version. Reconstructing one optimal path would need the full table (or a parent pointer), counting does not.

**Dry run:** the first example, `grid = [[1,3,1],[1,5,1],[4,2,1]]`.

| cell | cost | ways | why |
|---|---|---|---|
| (0,0) | 1 | 1 | base |
| (0,1), (0,2) | 4, 5 | 1, 1 | first row, one predecessor |
| (1,0), (2,0) | 2, 6 | 1, 1 | first column |
| (1,1) | 7 | 1 | up 4, left 2: left is strictly cheaper, copy its count, 2 + 5 = 7 |
| (1,2) | 6 | 1 | up 5, left 7: up wins, 5 + 1 = 6 |
| (2,1) | 8 | 1 | up 7, left 6: left wins, 6 + 2 = 8 |
| (2,2) | 7 | 1 | up 6, left 8: up wins, 6 + 1 = 7 |

Answer `[7, 1]`. No tie occurs here, so the ways table is all ones. A tie appears in the fourth example `[[1,2],[2,1]]`: both predecessors of (1,1) cost 3, so `ways = 1 + 1 = 2` and the answer is `[4, 2]` (the run prints that table).

**Code:**
```python
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
```

**Output (my run):**
```
prompt examples OK
grid   [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
cost   [[1, 4, 5], [2, 7, 6], [6, 8, 7]]
ways   [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
answer [7, 1]
tie grid [[1, 2], [2, 1]] cost [[1, 3], [3, 4]] ways [[1, 1], [1, 2]] answer [4, 2]
random cross-check: 600 grids agree; 176 had more than one optimal path
100x100 zeros: cost 0 | true count has 59 digits | mod -> 690285631
largest possible cost 9*199 = 1791 (far below the modulus)
recursion limit 1000 | memo depth at 100x100 is 199 -> fine
wrong variants differing from the oracle out of 500 : {'add both always': 485, 'first on tie only': 214, 'cost reduced (mod 5)': 450}
edge cases OK
```

**Edge cases:**
- 1 x 1: the cost is the single value and the count is 1.
- A single row or a single column: exactly one path, count 1.
- All zeros: every path ties, the count is C(m+n-2, m-1) mod p (the code checks 100 x 100 against `math.comb`).
- A true count that is a multiple of 10^9 + 7 would show as 0 after the modulus, so never use `ways == 0` to mean "unreachable" (here every cell is reachable, so it does not come up).
- Compare costs before adding the cell value: adding `grid[i][j]` to both candidates does not change which is smaller, but the tie test must use the predecessors' costs.

**Follow-ups:**
- Print one optimal path? Keep the full cost table and walk back from the end, going to a predecessor whose cost equals `cost[i][j] - grid[i][j]`; for a fixed tie rule choose up or left consistently.
- Obstacles? Treat a blocked cell as cost infinity and count 0; its neighbours then read infinity and never tie.
- Count paths with sum divisible by k (not minimum)? Then the state grows by the remainder; counting all paths needs no cost table at all.

**Common mistakes:**
- Adding both predecessors' counts always (wrong 485 times in 500 random grids in the code).
- Taking the count from the first minimum only and losing the tied one (wrong 214 of 500).
- Reducing the cost modulo the prime (or any modulus): comparisons lie (450 of 500 wrong with an artificial modulus of 5; harmless here only because 10^9 + 7 is far above the cost bound 1791).
- Using `<=` instead of `==` for the count test: a strictly worse predecessor must contribute nothing.

### Q29 ⭐ 🟡 Top-down grid DP: cache size and recursion depth. For a grid with `m` rows and `n` columns (1 <= m, n <= 1500) and a list `blocked` of at most 10^4 distinct cells `[r, c]` (any cell may be blocked, including the start and the end), a memoised function `f(i, j)` decorated with `functools.lru_cache(maxsize=None)` (the tuple `(i, j)` is the cache key) is evaluated as follows: it is only ever called on in-bounds cells; a blocked cell returns 0; the bottom-right cell returns 1; any other cell returns `f(i+1, j) + f(i, j+1)` over its in-bounds neighbours. The program calls `f(0, 0)` once. Return `[paths, entries, depth]`: the value of `f(0, 0)`, the number of distinct cells for which `f` was called (the cache size afterwards, blocked cells that were called included) and the maximum nesting depth of calls (the call `f(0, 0)` itself is depth 1). Compute all three WITHOUT recursion (a forward table over reachable cells), then explain which of the three would make the recursive version raise RecursionError: with no blocked cells and m = n = 600 the depth is 1199, past CPython's default limit of 1000. Also say why a cache key must be hashable (tuple, not list). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an instrumented lru_cache recursion on small grids (m, n <= 12) on small inputs. Example: m=3, n=3, blocked=[] -> [6, 9, 5]; m=3, n=3, blocked=[[1, 1]] -> [2, 9, 5]; m=2, n=4, blocked=[[0, 0]] -> [0, 1, 1]; m=1, n=1, blocked=[] -> [1, 1, 1]; m=4, n=3, blocked=[[0, 1], [1, 0]] -> [0, 3, 2]; m=600, n=600, blocked=[] -> [99210086628716100259395166354279999048776028950823599117066277392523790644939432481289087348273094564714767859517126896912283379860500428775241021388504367225251065302219729434487397626171671117422766919562944453912539279922435761841185334794928872418804619319119133993547860003208493900609497280018766204610934683472222291824312173152433569864759061895320000, 360000, 1199].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; behaviour verified by running Python 3.13) | 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened)

**Pattern:** Top-down grid DP with `lru_cache`, analysed instead of just run. Three numbers describe one memoised recursion: its answer, its cache size and its nesting depth. Only one of them can break the program.

**Say this first (1 line):** "Every call at cell (i, j) sits at depth i + j + 1 because each call moves one step right or down; the cache holds the cells that some call reaches, and the answer is a forward path count. The depth is what raises RecursionError, not the cache size and not the (huge) answer."

**Brute force:** Run the real recursion with an instrumented `lru_cache` (a depth counter incremented on entry and decremented in `finally`, and `cache_info().currsize` afterwards). Exact, but it fails on big grids with RecursionError, and it is the oracle for m, n <= 12.

**Optimal:** No recursion at all, a forward table row by row.
- `called[i][j]`: some call of `f` reaches (i, j). (0,0) is called; (i, j) is called when the cell above or the cell to its left is **expanded**.
- `expanded[i][j]` = called, not blocked and not the bottom-right cell (those two return immediately and call nothing).
- `entries` = number of called cells. Blocked cells that are called count (they enter the cache), and so does a blocked end cell. Cells behind a wall are never called, so they are not counted.
- `depth` = max over called cells of `i + j + 1`. Why: the call tree starts at depth 1 for (0,0), and every call goes to (i+1, j) or (i, j+1), so a call at cell (i, j) is always exactly at depth i + j + 1, however it got there. The deepest call is therefore the called cell with the largest i + j.
- `paths`: `w[0][0] = 1` if (0,0) is not blocked; for other cells `w = w[above] + w[left]` and `w = 0` for a blocked cell. This counts right/down paths through open cells, which equals `f(0,0)`: `f` sums the two neighbours, a blocked cell returns 0, the end returns 1. The count is the exact integer (no modulus in this prompt); Python integers have no overflow.
- Only two rows of `w` and of the `expanded` flags are kept, so memory is O(n).
- Which one raises RecursionError: the **depth**. With no blocked cells and m = n = 600 the depth is 1199, past the default limit of 1000. The path count is a 359-digit integer, which Python handles fine, and 360,000 cache entries are only memory, not stack. In the sandbox on Python 3.13 the memoised 400 x 400 run (depth 799) worked and 600 x 600 raised RecursionError; the exact failing depth depends on version and call path, so treat the pass/fail as an observation, not a rule, and keep clear of the boundary. The fix is bottom-up, not `sys.setrecursionlimit`.
- Cache key must be hashable: the cache is a dict, and the key `(i, j)` is hashed. A tuple is hashable, a list is not (`lru_cache` raises `TypeError: unhashable type: 'list'`, shown in the code). Hashable also means immutable by convention: a key that could change after insertion would corrupt lookups.

**Complexity:** Forward table: time O(m*n) cell visits (each adds two integers, which for the big counts costs O(digits)), space O(n) with two rolling rows. Blocked cells are looked up in a per-row set, built in O(B), B <= 10^4. The recursion would be O(m*n) time too, O(m*n) cache, but O(m+n) stack depth, and that stack depth is the problem.

**Dry run:** `m = 3, n = 3, blocked = []`, expected `[6, 9, 5]`.

| cell depth `i+j+1` | | | paths from start `w` | | |
|---|---|---|---|---|---|
| 1 | 2 | 3 | 1 | 1 | 1 |
| 2 | 3 | 4 | 1 | 2 | 3 |
| 3 | 4 | 5 | 1 | 3 | 6 |

- All 9 cells are called, so `entries = 9`.
- The largest depth is at (2,2): 2 + 2 + 1 = 5.
- `w[2][2] = 3 + 3 = 6` (above 3, left 3).

Second example, `blocked = [[1,1]]`: the centre is called (entries still 9) but returns 0 and calls nothing; `w` becomes `[1,1,1],[1,0,1],[1,1,2]`, so paths = 2; depth is still 5 because (2,2) is reached through (0,2) then (1,2). Third example `m=2, n=4, blocked=[[0,0]]`: the start is blocked, so `f(0,0)` returns 0 straight away: entries 1, depth 1, paths 0.

**Code:**
```python
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
```

**Output (my run):**
```
examples OK; 600x600 -> 359 digit path count, 360000 entries, depth 1199
3x3 no blocks: depth of a call at (i,j) is i+j+1
   [1, 2, 3]   paths-from-start [1, 1, 1]
   [2, 3, 4]   paths-from-start [1, 2, 3]
   [3, 4, 5]   paths-from-start [1, 3, 6]
  forward answer [6, 9, 5]
random cross-check: 1500 cases agree; 364 of them have 0 paths
anti-diagonal wall at i+j=5 on 10x10 (all 6 cells blocked): [0, 21, 6] -> depth 6 = 5 + 1
default recursion limit: 1000
  memoised 400x400: depth 799, entries 160000 -> ran fine
  memoised 600x600: expected depth 1199, entries 360000 -> RecursionError
tuple key: 3
list key -> TypeError: unhashable type: 'list'
1500x1500, 10^4 blocked: paths has 895 digits (or 0 if blocked start/end), entries 2238582 depth 2999 [sandbox time 0.8s]
edge cases OK
```

**Edge cases:**
- Start blocked: answer `[0, 1, 1]`, no further cells are called.
- End blocked but start open: the end is still called (it counts in `entries`) and returns 0 (`[0, 4, 3]` for 2 x 2 in the code).
- A wall across an anti-diagonal: the cells behind it are never called, so `entries` and `depth` are smaller than in the open grid (21 entries, depth 6 in the code's 10 x 10 wall example).
- One row or one column: a straight chain, depth m + n - 1 = the number of cells.
- 1 x 1: `[1, 1, 1]`, or `[0, 1, 1]` when the single cell is blocked.
- The blocked list may include the end cell; membership is checked before the end test.

**Follow-ups:**
- What about the cache size at 1500 x 1500? Up to 2.25 million tuple entries (the code's 10^4-blocked run has 2,238,582 called cells); the forward version with two rows holds none of them.
- Does `sys.setrecursionlimit(10**6)` fix it? It may let the recursion run, but a very deep recursion risks exhausting the real C stack (a crash, not a clean exception), which I did not test here; the portable fix is the loop.
- How would you add a modulus? Reduce `w` after each addition if a modulus is requested; it changes nothing about depth or entries.

**Common mistakes:**
- Blaming the cache size or the big integer for RecursionError. Only the nesting depth counts.
- Counting a blocked called cell out of `entries`, or counting cells behind a wall.
- Saying depth = m * n; it is m + n - 1 at most (1199 for 600 x 600), not 360,000.
- Using a list `[i, j]` as the key, which raises `TypeError`.
- Forgetting that a blocked end cell returns 0 before the end test (blocked is checked first).

### Q30 ⭐ 🟡 Minimum cost to cut a stick. A stick has length `n` (2 <= n <= 10^6) and `cuts` lists distinct integer positions strictly inside it (0 <= len(cuts) <= 100, each in 1..n-1). You may make the cuts in any order. One cut costs the length of the piece being cut; return the minimum total cost to make all cuts (0 when there are no cuts). Sort the cut positions and add 0 and n as boundary points, define `dp[l][r]` as the cost to make all cuts strictly between boundary points l and r, and explain why 'which cut comes FIRST in the interval' is the right choice here (the same shape as burst balloons with the last-burst view). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every order of the cuts (len(cuts) <= 6) on small inputs. Example: n=7, cuts=[1, 3, 4, 5] -> 16; n=9, cuts=[5, 6, 1, 4, 2] -> 22; n=10, cuts=[] -> 0; n=10, cuts=[5] -> 10.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP over boundary points. The state is a pair of boundaries (l, r), smaller intervals are solved first, and the transition scans every split point, so it is O(k^3) for k boundary points.

**Say this first (1 line):** "Sort the cuts, add 0 and n, let `dp[l][r]` be the cheapest way to make every cut strictly between points l and r, and choose which cut comes FIRST in that piece: it costs the whole piece, `points[r] - points[l]`, and leaves two independent sub-intervals."

**Brute force:** Try every order of the cuts: `len(cuts)!` orders (720 for 6 cuts), simulate the pieces and add the length of the piece each cut lands in. It is the oracle for at most 6 cuts, and exponential beyond that.

**Optimal:**
- Points: `pts = [0] + sorted(cuts) + [n]`, k = len(cuts) + 2 points. The cut positions are the only things that matter; n itself (up to 10^6) is never iterated.
- State: `dp[l][r]` (l < r) = minimum total cost to make all cuts strictly between `pts[l]` and `pts[r]`, assuming the piece `[pts[l], pts[r]]` exists as one stick.
- Base: `dp[l][l+1] = 0` (no cut inside) and the whole table starts at 0.
- Transition: pick the first cut m (`l < m < r`) in this piece. It costs the length of the piece, `pts[r] - pts[l]`, and then the two new pieces are independent: `dp[l][r] = pts[r] - pts[l] + min over m of (dp[l][m] + dp[m][r])`.
- Why FIRST and not last: the first cut in a piece has a known cost, the full length, no matter what else happens. If you chose the last cut instead, the piece it cuts is bounded by the nearest cuts already made, which are not determined by (l, r), so the cost would not be a function of the state. (In burst balloons it is the other way round: the first burst changes neighbours, so you think of the last burst, whose neighbours are the fixed ends. Same interval shape, opposite time direction.)
- Order of filling: increasing gap `r - l`, because `dp[l][r]` reads `dp[l][m]` and `dp[m][r]` with smaller gaps.
- Answer: `dp[0][k-1]`; no cuts gives k = 2 and 0.
- Memoised version: `f(l, r)` with `lru_cache`; its recursion depth is at most k <= 102, so it is safe at default limit 1000 (the code runs the largest size, 100 cuts, with the memo and gets the same answer). No setrecursionlimit is needed here.
- Space: the full triangle is read by every cell (`dp[l][m]` and `dp[m][r]` for all m), so there is no simple 1D reduction; O(k^2) memory is fine for k <= 102. (Knuth's optimisation could bring O(k^3) to O(k^2) time, not needed here and not checked.)

**Complexity:** Time O(k^3): about k^2/2 intervals times up to k split points (exactly C(k,3) inner steps, 171,700 for k = 102). Space O(k^2). Independent of n.

**Dry run:** `n = 7, cuts = [1,3,4,5]`, points `[0,1,3,4,5,7]` (indices 0..5). Entry dp[l][r], width = r - l:

| l \ r | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| 0 | 3 | 7 | 10 | 16 |
| 1 |  | 3 | 6 | 12 |
| 2 |  |  | 2 | 6 |
| 3 |  |  |  | 3 |

(entries with r = l + 1 are 0 and omitted.)
- `dp[0][2]` (cut at 1 inside 0..3): the only cut is 1, cost 3 - 0 = 3.
- `dp[2][4]` (3..5, cut at 4): cost 2. `dp[3][5]` (4..7, cut at 5): cost 3.
- `dp[0][5]` (whole stick, length 7): try first cut m = 1: 0 + 12, m = 2: 3 + 6, m = 3: 7 + 3, m = 4: 10 + 0. The minimum of the sums is 9, so the cost is 7 + 9 = 16, which matches the prompt. (m = 2 means cutting at 3 first, then 1 on the left piece 0..3 for 3, and 4 then 5 on 3..7 for 6.)
- Costs over all 24 orders range from 16 to 20, so order really matters.

**Code:**
```python
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
```

**Output (my run):**
```
prompt examples OK
points [0, 1, 3, 4, 5, 7]
dp[l][r] (l = row, r = column; only r >= l + 2 is filled by the loop)
  l=0 [0, 0, 3, 7, 10, 16]
  l=1 [0, 0, 0, 3, 6, 12]
  l=2 [0, 0, 0, 0, 2, 6]
  l=3 [0, 0, 0, 0, 0, 3]
  l=4 [0, 0, 0, 0, 0, 0]
  l=5 [0, 0, 0, 0, 0, 0]
answer dp[0][5] = 16
dp[0][5] options, split m: m=1: 0+12, m=2: 3+6, m=3: 7+3, m=4: 10+0; best + 7 = 16
random cross-check: 400 cases agree with every-order brute force
first example: 24 orders cost between 16 and 20
greedy middle-cut differs from the optimum on 32 of 400 random cases
100 cuts, n=10^6: 6035974 (memo agrees, depth <= 102) [sandbox time 0.03s]
edge cases OK; limit 1000
```

**Edge cases:**
- No cuts: 0 (just the two boundaries).
- One cut: n (the full stick is cut once).
- n = 2 with the single cut at 1: 2.
- Cuts given unsorted (example 2 is): sorting first is required, since the intervals are by position.
- Cuts are distinct and strictly inside (1..n-1); a cut at 0 or n would cost a piece for nothing and is excluded by the prompt.
- n up to 10^6 changes nothing: only the number of cuts sets the work.

**Follow-ups:**
- Return the order too? Store the best m per cell and read the cuts off recursively (first cut at the root, then the left and right halves).
- Why is this the same as optimal merging of pieces? Reverse time: the last cut is the first merge, and each merge of adjacent pieces costs the merged length, which is the same interval shape as matrix-chain multiplication.
- Greedy "cut near the middle"? Wrong: it differs from the optimum on 32 of 400 random cases in the code.

**Common mistakes:**
- Forgetting to sort the cuts, or forgetting the 0 and n boundaries.
- Letting the memo depend on n instead of the cut positions (a table of size n would be 10^6 x 10^6).
- Filling the table by `l` then `r` in row order, so a cell reads an unfilled smaller interval; fill by increasing gap.
- Choosing the last cut and still charging `pts[r] - pts[l]`.

### Q31 ⭐ 🟡 Assign tasks to workers (bitmask DP basics). `cost` is an n x n matrix (1 <= n <= 15, entries 0..1000): `cost[w][t]` is the price of worker w doing task t; each worker gets exactly one task and each task exactly one worker. Return `[best, assignment]` where `assignment[w]` is the task of worker w. Several optimal assignments can exist, so the tie rule is fixed: among minimum-cost assignments return the lexicographically smallest list. Use `f[mask]` = minimum cost for the workers `popcount(mask)`, ..., n-1 to take the tasks NOT in `mask` (so the worker index is implied by the mask), fill masks from full to empty, then walk forward picking the smallest task that keeps the total optimal. State O(2^n * n) time and O(2^n) space, and why n is capped at about 20. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every permutation (n <= 7) and taking the smallest (cost, list) pair on small inputs. Example: cost=[[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]] -> [13, [1, 0, 2, 3]]; cost=[[5]] -> [5, [0]]; cost=[[1, 1], [1, 1]] -> [2, [0, 1]]; cost=[[3, 1], [1, 3]] -> [2, [1, 0]].
**Asked at:** Advanced DP pattern guides covering bitmask DP (techinterview.org advanced and optimisation DP pattern posts; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Bitmask DP basics: a set of at most about 20 items is stored as an integer, one bit per task, so "which tasks are already taken" becomes a table index. Assignment problem by subset DP.

**Say this first (1 line):** "Worker index is the number of set bits in the mask, so the state is just the mask: `f[mask]` is the cheapest way for the remaining workers to take the remaining tasks; fill from the full mask down, then walk forward taking the smallest task that keeps the total optimal. O(2^n * n) time, O(2^n) space."

**Brute force:** Try every permutation of the tasks, n! of them (5,040 for n = 7), cost each, and keep the smallest `(cost, list)` pair; comparing the pair gives the lexicographic tie rule for free. It is the oracle for n <= 7 and is hopeless at n = 15 (1.3 * 10^12).

**Optimal:**
- Encoding: bit t of `mask` is 1 when task t is already taken. Workers are served in order 0, 1, 2, ..., so the next worker is `w = popcount(mask)`; the mask alone says who is next.
- State: `f[mask]` = minimum cost for workers `popcount(mask)`, ..., n-1 to take exactly the tasks NOT in `mask`, one each.
- Base: `f[full] = 0` (full = 2^n - 1): every task is taken, nothing left to pay.
- Transition: worker w picks a free task t: `f[mask] = min over free t of cost[w][t] + f[mask | 1<<t]`. `mask | 1<<t` is larger than `mask`, so iterating masks from `full - 1` down to 0 always finds the right-hand side final.
- Answer: `f[0]`.
- Reconstruction with the fixed tie rule (lexicographically smallest list): start at mask 0; for worker w = 0, 1, ..., scan tasks t in increasing order and take the first free t with `cost[w][t] + f[mask | 1<<t] == f[mask]`. Why this is the lexicographically smallest optimal list: `f` is exact, so every task that passes the test can start some optimal completion, and the smallest such t for worker 0 gives the smallest first entry; given that choice, the same argument applies to worker 1, and so on. Verified against the permutation oracle using the same `(cost, list)` order.
- Memoised version: `g(mask)` with `lru_cache`; the recursion depth is n + 1 <= 16, far under 1000, so there is no recursion-limit issue at this size. Bottom-up avoids call overhead.
- Space: `f` holds 2^n values. Computing only the value could be done layer by layer (masks with k bits depend only on masks with k+1 bits), but reconstruction needs `f` for every mask, so keep the whole array.
- Why n is capped near 20: states double with every extra task. n = 15 gives 32,768 masks and 491,520 transitions; n = 20 gives 1,048,576 masks and 20,971,520 transitions; n = 25 gives 838,860,800 transitions and a table of 33 million entries. Python's int lists make n = 20 slow and heavy; n = 15 is tiny (the code times it).

**Complexity:** Time O(2^n * n): each mask loops over n tasks; the `popcount` is O(1) in practice via `int.bit_count`. Space O(2^n). Compare n!: n = 15 gives 1.3 * 10^12 permutations against 491,520 transitions.

**Dry run:** `cost = [[9,2,7,8],[6,4,3,7],[5,8,1,8],[7,6,9,4]]`. A mask is written with bit 3 on the left (`0101` = tasks 0 and 2 taken). Selected rows of the table (the run prints all 16):

| mask | next worker | f | how |
|---|---|---|---|
| 1111 | | 0 | base |
| 0111 | 3 | 4 | only task 3 free: 4 + 0 |
| 1011 | 3 | 9 | only task 2 free: 9 + 0 |
| 0011 | 2 | 5 | t2: 1 + f[0111]=4 gives 5; t3: 8 + f[1011]=9 gives 17 |
| 0001 | 1 | 9 | t1: 4 + f[0011]=5 gives 9; t2: 3 + 12; t3: 7 + 7 |
| 0000 | 0 | 13 | t0: 9 + 9 = 18; t1: 2 + f[0010]=11 gives 13; t2: 7 + 13; t3: 8 + 12 |

Walk forward from mask 0000 with `f[0] = 13`: worker 0 tries t0 (9 + 9 = 18, not 13), then t1 (2 + 11 = 13, yes), so take 1. Mask is 0010. Worker 1 tries t0: 6 + f[0011]=5 gives 11 = f[0010], yes, take 0. Worker 2 takes 2 (1 + 4 = 5 = f[0011]), worker 3 takes 3. Result `[13, [1, 0, 2, 3]]`, as in the prompt. (Mask 0001 is "task 0 taken", so `f[0001] = 9` is the cost for workers 1..3 to take tasks 1, 2, 3.)

**Code:**
```python
import itertools, random, sys, time
from functools import lru_cache

random.seed(3101)
INF = float("inf")


def assign(cost):
    """f[mask] = min cost for workers popcount(mask)..n-1 to take exactly the tasks NOT in mask.
    Filled from the full mask down to 0; then walk forward taking the smallest task that stays optimal."""
    n = len(cost)
    full = (1 << n) - 1
    f = [INF] * (1 << n)
    f[full] = 0                                       # everyone has a task: nothing left to pay
    for mask in range(full - 1, -1, -1):
        w = mask.bit_count()                          # the next worker is w
        best = INF
        for t in range(n):
            if not mask >> t & 1:                     # task t still free
                v = cost[w][t] + f[mask | 1 << t]
                if v < best:
                    best = v
        f[mask] = best
    mask, out = 0, []
    for w in range(n):
        for t in range(n):                            # ascending t -> lexicographically smallest list
            if not mask >> t & 1 and cost[w][t] + f[mask | 1 << t] == f[mask]:
                out.append(t)
                mask |= 1 << t
                break
    return [f[0], out], f


def assign_memo(cost):
    """Top-down: same state, depth n + 1 <= 16, so recursion is no problem here."""
    n = len(cost)

    @lru_cache(maxsize=None)
    def g(mask):
        w = mask.bit_count()
        if w == n:
            return 0
        return min(cost[w][t] + g(mask | 1 << t) for t in range(n) if not mask >> t & 1)

    mask, out = 0, []
    for w in range(n):
        for t in range(n):
            if not mask >> t & 1 and cost[w][t] + g(mask | 1 << t) == g(mask):
                out.append(t); mask |= 1 << t; break
    return [g(0), out]


def brute(cost):
    n = len(cost)
    return list(min((sum(cost[i][p[i]] for i in range(n)), list(p)) for p in itertools.permutations(range(n))))


# ---- prompt examples
ex = [([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]], [13, [1, 0, 2, 3]]),
      ([[5]], [5, [0]]), ([[1, 1], [1, 1]], [2, [0, 1]]), ([[3, 1], [1, 3]], [2, [1, 0]])]
for c, want in ex:
    assert assign(c)[0] == assign_memo(c) == brute(c) == want, c
print("prompt examples OK")

# ---- hand table for the first example (bit t of the mask = task t is taken)
c = ex[0][0]
res, f = assign(c)
print("f[mask]: workers popcount(mask).. take the tasks NOT in mask")
for mask in range((1 << 4) - 1, -1, -1):
    w = mask.bit_count()
    if w == 4:
        why = "base"
    else:
        opts = [f"t{t}:{c[w][t]}+{f[mask | 1 << t]}" for t in range(4) if not mask >> t & 1]
        why = "worker %d: " % w + "  ".join(opts)
    print(f"  mask {mask:04b}  f={f[mask]:>2}   {why}")
print("walk forward:", res)

# ---- seeded cross-check against every permutation (n <= 7), lexicographic tie rule included
cnt = ties = 0
for _ in range(300):
    n = random.randint(1, 7)
    hi = random.choice([1, 3, 20])                    # tiny values make many tied optimal assignments
    cost = [[random.randint(0, hi) for _ in range(n)] for _ in range(n)]
    got, want = assign(cost)[0], brute(cost)
    assert got == assign_memo(cost) == want, (cost, got, want)
    best = want[0]
    nopt = sum(sum(cost[i][p[i]] for i in range(n)) == best for p in itertools.permutations(range(n)))
    ties += nopt > 1
    cnt += 1
print("random cross-check:", cnt, "matrices agree;", ties, "had several optimal assignments")

# ---- exhaustive: every 2x2 matrix with entries 0..3 and every 3x3 matrix with entries 0..2
ex_cnt = 0
for n, hi in ((2, 3), (3, 2)):
    for flat in itertools.product(range(hi + 1), repeat=n * n):
        cost = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
        assert assign(cost)[0] == brute(cost), cost
        ex_cnt += 1
print("exhaustive:", ex_cnt, "small matrices agree")

# ---- why a naive greedy (each worker takes the cheapest free task, in order) fails
def greedy(cost):
    used, tot, out = set(), 0, []
    for w, row in enumerate(cost):
        t = min((x for x in range(len(cost)) if x not in used), key=lambda x: row[x])
        used.add(t); tot += row[t]; out.append(t)
    return [tot, out]
rg = random.Random(3102)
bad = 0
for _ in range(300):
    cost = [[rg.randint(0, 9) for _ in range(5)] for _ in range(5)]
    bad += greedy(cost)[0] != brute(cost)[0]
print("greedy gives a worse total on", bad, "of 300 random 5x5 matrices")

# ---- the size limit in the prompt: n = 15 (2^15 * 15 transitions); 18 shown for scale, timing is sandbox-only
rng = random.Random(3103)
for n in (12, 15, 18):
    cost = [[rng.randint(0, 1000) for _ in range(n)] for _ in range(n)]
    t0 = time.perf_counter()
    r = assign(cost)[0]
    dt = time.perf_counter() - t0
    assert sorted(r[1]) == list(range(n)) and sum(cost[w][t] for w, t in enumerate(r[1])) == r[0]
    print(f"n={n}: {(1 << n) * n:>9,} transitions, best {r[0]}  [sandbox time {dt:.2f}s]")
print("n=20 would be", f"{(1 << 20) * 20:,}", "transitions and a table of", f"{1 << 20:,}", "entries; n=25 gives", f"{(1 << 25) * 25:,}")

# ---- edge cases
assert assign([[0]])[0] == [0, [0]]
assert assign([[7, 7], [7, 7]])[0] == [14, [0, 1]]
assert assign([[0] * 3 for _ in range(3)])[0] == [0, [0, 1, 2]]
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
f[mask]: workers popcount(mask).. take the tasks NOT in mask
  mask 1111  f= 0   base
  mask 1110  f= 7   worker 3: t0:7+0
  mask 1101  f= 6   worker 3: t1:6+0
  mask 1100  f=11   worker 2: t0:5+6  t1:8+7
  mask 1011  f= 9   worker 3: t2:9+0
  mask 1010  f= 8   worker 2: t0:5+9  t2:1+7
  mask 1001  f= 7   worker 2: t1:8+9  t2:1+6
  mask 1000  f=12   worker 1: t0:6+7  t1:4+8  t2:3+11
  mask 0111  f= 4   worker 3: t3:4+0
  mask 0110  f= 9   worker 2: t0:5+4  t3:8+7
  mask 0101  f=12   worker 2: t1:8+4  t3:8+6
  mask 0100  f=13   worker 1: t0:6+12  t1:4+9  t3:7+11
  mask 0011  f= 5   worker 2: t2:1+4  t3:8+9
  mask 0010  f=11   worker 1: t0:6+5  t2:3+9  t3:7+8
  mask 0001  f= 9   worker 1: t1:4+5  t2:3+12  t3:7+7
  mask 0000  f=13   worker 0: t0:9+9  t1:2+11  t2:7+13  t3:8+12
walk forward: [13, [1, 0, 2, 3]]
random cross-check: 300 matrices agree; 124 had several optimal assignments
exhaustive: 19939 small matrices agree
greedy gives a worse total on 206 of 300 random 5x5 matrices
n=12:    49,152 transitions, best 2234  [sandbox time 0.00s]
n=15:   491,520 transitions, best 1420  [sandbox time 0.04s]
n=18: 4,718,592 transitions, best 1289  [sandbox time 0.42s]
n=20 would be 20,971,520 transitions and a table of 1,048,576 entries; n=25 gives 838,860,800
edge cases OK; limit 1000
```

**Edge cases:**
- n = 1: `[cost[0][0], [0]]`.
- All entries equal: every assignment ties, so the identity list `[0, 1, ..., n-1]` is returned.
- Zero costs: same, the smallest list wins.
- Ties between different optimal assignments, such as `[[3,1],[1,3]]`: both `[0,1]` (cost 6) and `[1,0]` (cost 2) exist, only the second is optimal here, so the answer is `[2, [1, 0]]`; for `[[1,1],[1,1]]` both tie and `[0, 1]` wins by the rule.
- Fill direction: iterate masks downward, or the right-hand side is not ready (for the top-down version, recursion handles the order).

**Follow-ups:**
- Hungarian algorithm? It solves the same problem in O(n^3), which wins at n beyond 20; the bitmask DP is the answer when a short, easy-to-prove solution is wanted for n <= about 20.
- Maximise instead of minimise? Replace `min` by `max` and use `-inf` initial values; the tie rule is unchanged.
- More tasks than workers, or some pairs forbidden? Forbid by infinite cost; with more tasks than workers the mask has more bits than workers and the base case is `popcount == workers`.

**Common mistakes:**
- Iterating masks upward when the transition goes to `mask | bit`: the cell is read before it is final.
- Storing the worker index in the state as well (a factor n wasted).
- Greedy per worker (cheapest free task): worse on 206 of 300 random 5 x 5 matrices in the code.
- Tie rule: choosing the first task that is merely cheap for this worker, not one for which `cost + f[next] == f[mask]`. Only the latter preserves optimality.

### Q32 ⭐ 🟡 Minimum score triangulation of a convex polygon. `values` lists the labels of the vertices in order around a convex polygon (3 <= len <= 100, each in 1..100). A triangulation cuts the polygon into len - 2 triangles by non-crossing diagonals; a triangle scores the product of its three vertex labels, and the score of a triangulation is the sum over its triangles. Return the minimum score. Define `dp[i][j]` for the sub-polygon of vertices i..j, say why edge (i, j) belongs to exactly one triangle with some third vertex k (i < k < j), give the recurrence and the O(n^3) time. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the apex of the triangle on the edge (first, last) (len <= 8) on small inputs. Example: values=[1, 2, 3] -> 6; values=[3, 7, 4, 5] -> 144; values=[1, 3, 1, 4, 1, 5] -> 13; values=[2, 2, 2, 2, 2] -> 24.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP on a polygon (the matrix-chain shape). The state is a range of consecutive vertices, the split point is the apex of the triangle that sits on the closing edge.

**Say this first (1 line):** "`dp[i][j]` is the cheapest triangulation of the sub-polygon i, i+1, ..., j; the edge (i, j) belongs to exactly one triangle, with some third vertex k strictly between, so `dp[i][j] = min over k of dp[i][k] + dp[k][j] + v[i]*v[k]*v[j]`, O(n^3)."

**Brute force:** Plain recursion over the apex of the triangle on the edge (first, last): try every k, recurse on the two sub-polygons `vs[:k+1]` and `vs[k:]`. It visits every triangulation: there are Catalan(n-2) of them (1, 2, 5, 14, 42, 132 for n = 3..8, checked in the code), so it is exponential. The oracle for n <= 8. The code also enumerates all triangulations explicitly and scores each as a second oracle.

**Optimal:**
- State: `dp[i][j]` for i < j = minimum total score of a triangulation of the convex sub-polygon with vertices i, i+1, ..., j, closed by the chord (i, j).
- Base: `dp[i][i+1] = 0`: two vertices form an edge, no triangle. A triangle (j = i + 2) has one triangle: `dp[i][i+2] = v[i]*v[i+1]*v[i+2]`, which falls out of the recurrence with k = i + 1.
- Why the edge (i, j) belongs to exactly one triangle: in any triangulation of a polygon, each edge is a side of precisely one of its triangles, and that triangle's third vertex k lies on the polygon side between i and j (i < k < j). Cutting along the new chords (i, k) and (k, j) splits the problem into two smaller convex polygons that are triangulated independently. Every triangulation is counted once, by its k.
- Transition: `dp[i][j] = min(dp[i][k] + dp[k][j] + v[i]*v[k]*v[j])` over i < k < j.
- Fill by increasing gap `j - i` (2, 3, ..., n-1); the answer is `dp[0][n-1]`.
- Memoised version: `f(i, j)` with `lru_cache`. Recursion depth is at most n <= 100 (each call shrinks the range by at least one), so it is safe under the default limit of 1000 (the code runs n = 100 both ways).
- Space: the cell reads `dp[i][k]` and `dp[k][j]` for all k, so the whole upper triangle is live, O(n^2); there is no row-by-row reduction.
- A tempting greedy, "fan every triangle from the smallest label", is wrong: it differs from the optimum on 78 of 500 random polygons in the code.

**Complexity:** Time O(n^3): about n^2/2 cells times up to n apexes, exactly C(n,3) = 161,700 inner steps at n = 100. Space O(n^2).

**Dry run:** `values = [3, 7, 4, 5]` (the run also prints `[1, 2, 3]`, the first example: only `dp[0][2] = 1*2*3 = 6`).

| cell | options over k | value |
|---|---|---|
| dp[0][2] (3,7,4) | k=1: 0 + 0 + 3*7*4 = 84 | 84 |
| dp[1][3] (7,4,5) | k=2: 0 + 0 + 7*4*5 = 140 | 140 |
| dp[0][3] (all four) | k=1: 0 + 140 + 3*7*5 = 245; k=2: 84 + 0 + 3*4*5 = 144 | 144 |

The two triangulations of a quadrilateral are the two diagonals; 144 uses the diagonal 0-2 (triangles 3,7,4 and 3,4,5). For the first example of the prompt `[1,2,3]` there is a single triangle, so the answer is 6.

**Code:**
```python
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
```

**Output (my run):**
```
prompt examples OK
values [1, 2, 3]
  dp[0][2] = min(k=1: 0+0+1*2*3=6) = 6
  answer 6
values [3, 7, 4, 5]
  dp[0][2] = min(k=1: 0+0+3*7*4=84) = 84
  dp[0][3] = min(k=1: 0+140+3*7*5=245; k=2: 84+0+3*4*5=144) = 144
  dp[1][3] = min(k=2: 0+0+7*4*5=140) = 140
  answer 144
triangulation counts for n = 3..8: [1, 2, 5, 14, 42, 132]
random cross-check: 500 polygons agree with the apex recursion
enumerate-all-triangulations check: 100 polygons agree
fan from the smallest label differs from the optimum on 78 of 500 random polygons
n=100: 273789 (memoised version agrees, recursion depth <= 100) [sandbox time 0.02s]
edge cases OK; limit 1000
```

**Edge cases:**
- n = 3: one triangle, the product of the three labels (`[1,2,3]` gives 6).
- n = 4: two triangulations; take the cheaper (144 for `[3,7,4,5]`).
- All labels equal to v: every triangulation costs (n-2) * v^3 (24 for five 2's).
- Labels as large as 100, n = 100: the answer fits easily, and Python has no overflow anyway.
- The polygon is circular, but the DP fixes the chord (0, n-1) as the closing edge, which is also a real edge, so no rotation is needed.

**Follow-ups:**
- Why is it the same as matrix-chain multiplication? A chain of n - 1 matrices with dimensions `d` is the same recurrence with the product `d[i]*d[k]*d[j]`.
- Return the diagonals too? Store the best k per cell and recurse: the chord (i, k) and (k, j) are emitted for each triple.
- Maximum score instead? Swap `min` for `max`; the triangle product structure is the same.

**Common mistakes:**
- Choosing k from the whole range instead of strictly between i and j (a triangle with a repeated vertex).
- Treating the polygon as a line and forgetting that edge (0, n-1) closes it; it is already included as the outer edge of the sub-polygon.
- Fan greedy from the smallest label.
- Filling `dp` by row order so `dp[k][j]` has not been computed; fill by gap.

### Q33 ⭐ 🔴 Strange printer (interval DP, concept level). A printer prints a run of one repeated letter over any contiguous range of positions in one turn, and each print overwrites whatever was there. `s` is a lowercase string with 0 <= len <= 100. Return the minimum number of turns to print exactly `s` (0 for the empty string). Collapse equal neighbours first, define `dp[i][j]` for the substring i..j, give the transition `dp[i][j-1] + 1` versus joining the print of s[j] with the print of an equal letter s[k] (i <= k < j), and say why printing the first letter across a wider range is never worse. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a breadth-first search over all printed states (len <= 6, alphabet a-c) on small inputs. Example: s='aaabbb' -> 2; s='aba' -> 2; s='' -> 0; s='abcabc' -> 5; s='a' -> 1.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP, concept level. State is a substring i..j; the transition either prints the last letter separately, or lets the print of that letter be shared with an equal letter earlier in the range.

**Say this first (1 line):** "Merge equal neighbours first, then `dp[i][j]` is the fewest turns for t[i..j]: either `dp[i][j-1] + 1` (print t[j] alone) or, for each k with t[k] == t[j], print t[k] and t[j] with one wide stroke: `dp[i][k] + dp[k+1][j-1]`; O(n^3)."

**Brute force:** Breadth-first search over strip states: start from all blanks, each move overwrites any range with one letter, stop when the strip equals `s`. The number of states grows like 4^n for the alphabet a-c (4 symbols with the blank), each with up to n(n+1)/2 * 3 moves. It is the oracle for len <= 6 over a, b, c.

**Optimal:**
- Collapse first: `aaabbb` is the same job as `ab`, because one stroke can cover a whole run of equal letters at no extra cost. The code checks that the DP gives the same answers with and without the collapse for all 255 strings up to length 7 over {a, b}; collapsing just shrinks n.
- State: `dp[i][j]` = minimum turns to print `t[i..j]` onto a blank strip (t is the collapsed string).
- Base: `dp[i][i] = 1`; an empty string needs 0 turns.
- Transition: first candidate `dp[i][j-1] + 1`: print the first j - i letters, then one more stroke for t[j]. Second candidate for every k in [i, j) with `t[k] == t[j]`: print t[j] with the same stroke as t[k]. That stroke is laid down while printing `t[i..k]` (so cost `dp[i][k]`, the stroke simply extends to column j) and then everything between, `t[k+1..j-1]`, is printed on top afterwards (cost `dp[k+1][j-1]`, 0 if that range is empty). Take the minimum.
- Why the answer needs only "the first letter can be printed across a wider range": in an optimal plan, the stroke that paints the leftmost position can be extended to the right, to cover another equal letter, without ever hurting, because every later stroke over that range overwrites it anyway. So, the leftmost letter is either printed alone or together with an equal letter; the code's DP states the mirror form (last letter t[j]), which is the same argument read right to left. An exchange argument, checked rather than proved here: the DP equals the BFS for all 364 strings of length <= 5 over a, b, c and 60 random strings of length 6.
- Wrong version: only splitting into two independent parts (`dp[i][k] + dp[k+1][j]`) never shares a stroke, so `aba` costs 3 instead of 2; it is wrong on 864 strings of length <= 6 in the code.
- Memoised version: `f(i, j)` with `lru_cache`, depth <= n <= 100 (each call shrinks the range), so there is no recursion-limit problem at this size; bottom-up is shown as the main solution.
- Space: `dp` reads cells inside `[i, j]` for the same i and larger i, so the full triangle is kept: O(n^2).

**Complexity:** Time O(n^3): n^2/2 cells, each scanning up to n values of k (at n = 100 that is about 166,000 inner steps). Space O(n^2). The code's random 26-letter string of length 100 runs in a blink (sandbox only).

**Dry run:**
- `aaabbb` collapses to `ab`: `dp[0][0] = 1`, `dp[1][1] = 1`, `dp[0][1] = dp[0][0] + 1 = 2` (the letters differ, so no sharing). Answer 2.
- `aba`, the interesting one (upper triangle, rows i):

| i \ j | 0 (a) | 1 (b) | 2 (a) |
|---|---|---|---|
| 0 (a) | 1 | 2 | 2 |
| 1 (b) |  | 1 | 2 |
| 2 (a) |  |  | 1 |

`dp[0][2]`: candidate one is `dp[0][1] + 1 = 3`. Candidate two uses k = 0 (t[0] == t[2] == a): `dp[0][0] + dp[1][1] = 1 + 1 = 2`. So print `aaa` first, then `b` over the middle. Answer 2.
- `abcabc` -> 5 (the run prints that 6 x 6 table; `dp[0][5] = 5`: printing the last c alone gives `dp[0][4] + 1 = 5`, sharing it with the c at k = 2 gives `dp[0][2] + dp[3][4] = 3 + 2 = 5`, a tie).

**Code:**
```python
import itertools, random, sys, time
from collections import deque
from functools import lru_cache

random.seed(3301)


def collapse(s):
    return "".join(ch for i, ch in enumerate(s) if i == 0 or ch != s[i - 1])


def solve(s, do_collapse=True):
    """dp[i][j] = fewest turns to print t[i..j] on a blank strip (t = s with equal neighbours merged)."""
    t = collapse(s) if do_collapse else s
    n = len(t)
    if n == 0:
        return 0, t, []
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            best = dp[i][j - 1] + 1                       # print t[j] on its own
            for k in range(i, j):
                if t[k] == t[j]:                          # share one print of the letter with t[k]
                    mid = dp[k + 1][j - 1] if k + 1 <= j - 1 else 0
                    best = min(best, dp[i][k] + mid)
            dp[i][j] = best
    return dp[0][n - 1], t, dp


def solve_memo(s):
    """Top-down, the same recurrence. Depth is at most len(t) <= 100: safe."""
    t = collapse(s)
    n = len(t)

    @lru_cache(maxsize=None)
    def f(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        best = f(i, j - 1) + 1
        for k in range(i, j):
            if t[k] == t[j]:
                best = min(best, f(i, k) + f(k + 1, j - 1))
        return best

    return f(0, n - 1) if n else 0


def bfs(s, alphabet="abc"):
    """Oracle: shortest number of turns over all strip states ('?' = blank), every range and letter."""
    n = len(s)
    if n == 0:
        return 0
    start = "?" * n
    seen = {start}
    dq = deque([(start, 0)])
    while dq:
        cur, d = dq.popleft()
        if cur == s:
            return d
        for l in range(n):
            for r in range(l, n):
                for ch in alphabet:
                    nxt = cur[:l] + ch * (r - l + 1) + cur[r + 1:]
                    if nxt not in seen:
                        seen.add(nxt)
                        dq.append((nxt, d + 1))


def split_only(s):
    """Wrong: only split into two independent parts, never share a print between them."""
    t = collapse(s)
    n = len(t)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] for k in range(i, j))
    return dp[0][n - 1]


# ---- prompt examples
ex = [("aaabbb", 2), ("aba", 2), ("", 0), ("abcabc", 5), ("a", 1)]
for s, want in ex:
    assert solve(s)[0] == solve_memo(s) == bfs(s) == want, s
print("prompt examples OK")

# ---- table walk-throughs (collapsed string; entry [i][j], upper triangle)
for s in ("aaabbb", "aba", "abcabc"):
    res, t, dp = solve(s)
    print(f"s={s!r} collapsed={t!r} answer={res}")
    for i, row in enumerate(dp):
        print("   ", t[i], [row[j] if j >= i else "." for j in range(len(t))])
# the decisive cell of 'aba': dp[0][2], j = 2 (letter a), k = 0 (also a)
_, t, dp = solve("aba")
print("aba: dp[0][1] + 1 =", dp[0][1] + 1, "vs share the a at k=0: dp[0][0] + dp[1][1] =", dp[0][0] + dp[1][1], "-> 2")

# ---- collapsing does not change the answer (the DP gives the same value without it)
cnt = 0
for L in range(0, 8):
    for tup in itertools.product("ab", repeat=L):
        s = "".join(tup)
        assert solve(s, True)[0] == solve(s, False)[0], s
        cnt += 1
print("collapse check: all", cnt, "strings over {a,b} up to length 7 give the same answer with and without it")

# ---- exhaustive vs BFS: every string of length <= 5 over {a,b,c}
cnt = 0
for L in range(0, 6):
    for tup in itertools.product("abc", repeat=L):
        s = "".join(tup)
        assert solve(s)[0] == solve_memo(s) == bfs(s), s
        cnt += 1
print("exhaustive vs BFS:", cnt, "strings (len <= 5, alphabet a-c) agree")

# ---- seeded random, length 6
for _ in range(60):
    s = "".join(random.choice("abc") for _ in range(6))
    assert solve(s)[0] == solve_memo(s) == bfs(s), s
print("random cross-check: 60 strings of length 6 agree with the BFS over printed states")

# ---- the 'split only' variant is wrong
bad = [s for L in range(1, 7) for tup in itertools.product("abc", repeat=L)
       for s in ["".join(tup)] if split_only(s) != solve(s)[0]]
print("split-only (no sharing) is wrong on", len(bad), "strings of length <= 6; first:", bad[0])
assert "aba" in bad

# ---- bounds
assert solve("a" * 100)[0] == 1 and solve("ab" * 50)[0] == 51        # ababab...: one 'a' sweep + 50 b's
t0 = time.perf_counter()
rg = random.Random(3302)
big = "".join(rg.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(100))
res = solve(big)[0]
dt = time.perf_counter() - t0
assert res == solve_memo(big)
print("length 100 random:", res, "(memo agrees; recursion depth <= 100)", f"[sandbox time {dt:.2f}s]")
assert solve("abcdefghijklmnopqrstuvwxyz")[0] == 26
print("edge cases OK; limit", sys.getrecursionlimit())
```

**Output (my run):**
```
prompt examples OK
s='aaabbb' collapsed='ab' answer=2
    a [1, 2]
    b ['.', 1]
s='aba' collapsed='aba' answer=2
    a [1, 2, 2]
    b ['.', 1, 2]
    a ['.', '.', 1]
s='abcabc' collapsed='abcabc' answer=5
    a [1, 2, 3, 3, 4, 5]
    b ['.', 1, 2, 3, 3, 4]
    c ['.', '.', 1, 2, 3, 3]
    a ['.', '.', '.', 1, 2, 3]
    b ['.', '.', '.', '.', 1, 2]
    c ['.', '.', '.', '.', '.', 1]
aba: dp[0][1] + 1 = 3 vs share the a at k=0: dp[0][0] + dp[1][1] = 2 -> 2
collapse check: all 255 strings over {a,b} up to length 7 give the same answer with and without it
exhaustive vs BFS: 364 strings (len <= 5, alphabet a-c) agree
random cross-check: 60 strings of length 6 agree with the BFS over printed states
split-only (no sharing) is wrong on 864 strings of length <= 6; first: aba
length 100 random: 72 (memo agrees; recursion depth <= 100) [sandbox time 0.01s]
edge cases OK; limit 1000
```

**Edge cases:**
- Empty string: 0.
- One letter, or a single repeated letter (`aaa`, 100 a's): 1.
- All letters different (26 distinct): n turns, nothing to share.
- Alternating `abab...` of length 100: 51 (the code asserts it): one stroke of a across everything, then 50 strokes of b.

**Follow-ups:**
- Why O(n^3) and not better? n^2 states with O(n) transitions each; with n <= 100 that is about 166,000 steps, so nothing faster is needed.
- How would you recover the strokes? Store which candidate won per cell and replay: stroke (k..j) of letter t[j] first, then the middle.
- How does it differ from burst balloons / cut a stick? Same interval shape; here the split condition is "equal letters" instead of "any split point", so only the matching k are tried.

**Common mistakes:**
- Skipping the collapse (not wrong for correctness, but it blows up the table with redundant cells).
- Using `dp[k+1][j]` instead of `dp[k+1][j-1]`: the letter t[j] is already painted by the shared stroke.
- Forgetting the base for an empty middle range (`k + 1 > j - 1` must give 0).
- Only splitting into independent halves: it never shares a stroke and is wrong on `aba`.

### Q34 ⭐ 🔴 Cherry pickup (two walkers, concept level). `grid` is an n x n list of lists (1 <= n <= 50) with 0 (empty), 1 (one cherry) and -1 (thorns, impassable). Go from the top-left to the bottom-right moving only right or down, then back to the top-left moving only left or up, picking each cherry you pass over (a picked cherry cell becomes empty). Return the maximum cherries, or 0 if no path exists from the top-left to the bottom-right. Explain why the return trip is the same as a second walker going down-right at the same time, so the state is (step k, row of walker 1, row of walker 2) with the columns implied, give the transition over the four previous-state choices, how a cell shared by both walkers is counted once, and why two separate greedy trips fail. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every pair of right/down paths (n <= 5) on small inputs. Example: grid=[[0, 1, -1], [1, 0, -1], [1, 1, 1]] -> 5; grid=[[1, 1, -1], [1, -1, 1], [-1, 1, 1]] -> 0; grid=[[1]] -> 1; grid=[[0, 0], [0, 0]] -> 0.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** DP over time with two agents moving in lock-step. Two walkers that move at the same pace share a "step number" k, so their columns follow from their rows and the state is (k, r1, r2).

**Say this first (1 line):** "The trip back is the same as a second walker going down-right at the same time, so run both at once: `dp[k][r1][r2]` is the most cherries the pair has picked after k moves, with columns `k - r1` and `k - r2`; four predecessor choices, a shared cell counts once, O(n^3)."

**Brute force:** Enumerate every right/down path (C(2n-2, n-1) of them, 70 for n = 5), keep those without thorns, and for every pair of paths add the cherries on the **union** of their cells (a shared cell once). The code also checks, for n <= 3, the statement read literally: pick a path, remove its cherries, then pick the best return path, and shows the two readings agree. Oracle for n <= 5.

**Optimal:**
- Why the return trip is a second down-right walker: a left/up path from the bottom-right to the top-left, read backwards, is a right/down path from the top-left to the bottom-right. Picking the cherries "on the way back" is then picking the cherries of a second right/down path, with the rule that a cherry already picked (a cell on both paths) is counted once. So the answer is the best union over a pair of right/down paths.
- State: after k moves each (k = 0..2n-2), walker 1 is at row r1 and column `k - r1`, walker 2 at row r2 and column `k - r2`. `dp[k][r1][r2]` = max cherries picked by the pair so far, or -infinity if the pair cannot be there (thorn, off-grid or unreachable).
- Base: `dp[0][0][0] = grid[0][0]` (0 or 1; -1 means no path and the answer is 0).
- Transition: each walker came from above (row - 1, same k - 1) or from the left (same row at k - 1). Four predecessor pairs: `(r1, r2)`, `(r1-1, r2)`, `(r1, r2-1)`, `(r1-1, r2-1)` at step k - 1. So `dp[k][r1][r2] = max(four predecessors) + grid[r1][k-r1] + (grid[r2][k-r2] if r1 != r2 else 0)`; skip any pair that stands on a thorn.
- Shared cell: when `r1 == r2` the columns are equal too (same k), so the walkers are on the same cell; add its cherry once.
- Answer: `max(0, dp[2n-2][n-1][n-1])`: if no pair arrives (thorns cut every path) the value is -infinity and the answer is 0.
- Symmetry: swapping the two walkers changes nothing, so only `r1 <= r2` is stored (about half the states); the code does this.
- Space: step k reads only step k - 1, so two n x n layers suffice: O(n^2) (the code keeps one rolling layer).
- Memoised version: `f(k, r1, r2)` = best from here to the end, depth 2n - 1 = 99 at n = 50, which is below the default limit of 1000, so memoisation is safe (the code runs n = 50 both ways). Bottom-up is still preferred.
- Why two separate greedy trips fail: taking the best single trip first can use up cherries and force a poor return. The smallest counterexample the code found: `[[0,1,0],[0,1,1],[1,1,0]]`: the greedy two-trip total is 4 but the best is 5. It is wrong on 34 of 500 random small grids.

**Complexity:** Time O(n^3): 2n - 1 steps times at most n^2/2 row pairs, 4 predecessors each. Space O(n^2) with rolling layers. At n = 50 that is about 99 * 1,250 * 4 operations.

**Dry run:** `grid = [[0,1,-1],[1,0,-1],[1,1,1]]`, pairs `(r1, r2)` kept with r1 <= r2 (the run prints this):

| k | reachable pairs (r1, r2): value | note |
|---|---|---|
| 0 | (0,0): 0 | start cell value 0 |
| 1 | (0,0): 1, (0,1): 2, (1,1): 1 | (0,0) means both on cell (0,1), counted once; (0,1) means one on (0,1), one on (1,0): 1 + 1 |
| 2 | (1,1): 2, (1,2): 3, (2,2): 2 | (0,2) is a thorn, so no pair uses row 0; (1,2) = cells (1,1)=0 and (2,0)=1 on top of the best earlier 2 |
| 3 | (2,2): 4 | cell (2,1) = 1; (1,2) is a thorn; best predecessor 3 |
| 4 | (2,2): 5 | cell (2,2) = 1 counted once |

Answer 5. The pair of paths: down, down, right, right and right, down, down, right (so both pass (2,1)). The second example has thorns that cut every route: no pair reaches k = 4, so the answer is 0.

**Code:**
```python
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
```

**Output (my run):**
```
prompt examples OK
grid [[0, 1, -1], [1, 0, -1], [1, 1, 1]]
  k=0: {'r1=0,r2=0 (c=0,0)': 0}
  k=1: {'r1=0,r2=0 (c=1,1)': 1, 'r1=0,r2=1 (c=1,0)': 2, 'r1=1,r2=1 (c=0,0)': 1}
  k=2: {'r1=1,r2=1 (c=1,1)': 2, 'r1=1,r2=2 (c=1,0)': 3, 'r1=2,r2=2 (c=0,0)': 2}
  k=3: {'r1=2,r2=2 (c=1,1)': 4}
  k=4: {'r1=2,r2=2 (c=2,2)': 5}
answer dp[k=4][2][2] = 5
random cross-check: 500 grids agree with the pair-of-paths brute force; 167 have answer 0
exhaustive 0/1 grids n <= 3: 530 agree, literal reading included
two greedy trips wrong on 34 of 500 random grids; smallest: ([[0, 1, 0], [0, 1, 1], [1, 1, 0]], 4, 5)
n=50 random: 161 (memo agrees, recursion depth 99) [sandbox time 0.03s]
edge cases OK; limit 1000
```

**Edge cases:**
- n = 1: the cell value if it is not a thorn (the walkers are the same cell, counted once), else 0.
- Thorn at the start or the end: 0.
- Thorns that disconnect the corners: 0, never a negative number.
- All zeros: 0.
- All ones: the two paths share only the corners, so 4n - 4 for n >= 2 (12 for n = 4), not the sum of two full paths (the code asserts it).
- A cell on both paths counted twice is the standard bug: only when `r1 == r2`.

**Follow-ups:**
- Why does only the row pair matter, not the columns? Same step count k makes `c = k - r` for both walkers.
- Return the actual two paths? Keep the full 3D table (or a parent choice per state) and walk back from `(2n-2, n-1, n-1)`.
- Why not just rows and columns of both walkers (four coordinates)? The step number ties them together, so one coordinate per walker is redundant: n^4 states drop to n^3.

**Common mistakes:**
- Running the best path twice (greedy) and removing the cherries between trips.
- Counting a shared cell twice (add the second cherry only when `r1 != r2`).
- Allowing a walker to step on a thorn, or treating -infinity as 0 and returning a positive total for an unreachable end.
- Returning -infinity instead of 0 when no path exists.

### Q35 ⭐ 🔴 Travelling salesman with a small number of cities (bitmask DP basics). `dist` is an n x n matrix (1 <= n <= 12) of non-negative integers (at most 1000; `dist[a][b]` may differ from `dist[b][a]`, `dist[a][a]` = 0). Start at city 0, visit every other city exactly once and return to city 0; return the minimum total distance (0 for n = 1). Define `f[mask][last]` = minimum cost of a path that starts at 0, visits exactly the cities in `mask` and ends at `last`, give the transition, the answer `min(f[full][last] + dist[last][0])`, and the time O(2^n * n^2) and space O(2^n * n). Say why the (n-1)! permutation search is hopeless beyond n around 11 and what the DP buys. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every permutation of the other cities (n <= 8) on small inputs. Example: dist=[[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]] -> 80; dist=[[0]] -> 0; dist=[[0, 3], [5, 0]] -> 8; dist=[[0, 1, 9], [9, 0, 1], [1, 9, 0]] -> 3.
**Asked at:** Advanced DP pattern guides covering bitmask DP (techinterview.org advanced and optimisation DP pattern posts; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Bitmask DP basics (Held-Karp). The set of visited cities is an integer mask; the state adds the current city; transitions extend the path by one unvisited city.

**Say this first (1 line):** "`f[mask][last]` is the cheapest path that starts at city 0, visits exactly the cities in mask and ends at last; extend by one unvisited city, close the tour back to 0 at the end: O(2^n * n^2) time, O(2^n * n) space, against (n-1)! for trying all orders."

**Brute force:** Try every permutation of cities 1..n-1 as the visiting order, add the distances along `0 -> p1 -> ... -> p(n-1) -> 0` and take the minimum: (n-1)! tours (5,040 for n = 8, the oracle size). Distances may be asymmetric, so a tour and its reverse can differ and both are tried.

**Optimal:**
- State: bit c of `mask` is 1 when city c is visited; bit 0 is always set (the tour starts there). `f[mask][last]` = minimum cost of a path that starts at 0, visits exactly the cities in `mask` and ends at `last`.
- Base: `f[1][0] = 0` (only city 0, standing on it). Everything else is infinity until reached.
- Transition: from `(mask, last)` go to any city `nxt` not in the mask: `f[mask | 1<<nxt][nxt] = min(..., f[mask][last] + dist[last][nxt])`. Masks are processed in increasing numeric order, and a target mask is always larger than its source, so every state is final when it is read.
- Answer: close the tour: `min over last != 0 of f[full][last] + dist[last][0]`, where `full = 2^n - 1`. For n = 1 the answer is 0.
- Why O(2^n * n^2): there are 2^n masks times n values of `last` (about 2^(n-1) * n states reached) and each tries up to n next cities. Space O(2^n * n) for the table.
- Space reduction: city 0 is always in the mask, so leave it out and index by the other n - 1 cities (2^(n-1) masks instead of 2^n); the code does this as a second solver and checks it. Reconstructing a tour needs the whole table, the code recovers one tour by walking the table backwards.
- Memoised version: `g(mask, last)` = cheapest way to finish from here (the other direction), depth at most n <= 12, so no recursion-limit issue, and it agrees in the code.
- Why (n-1)! is hopeless beyond n around 11: the number of tours grows factorially. In the table printed by the run: 8 cities give 5,040 tours, 10 give 362,880, 11 give 3,628,800, 12 give 39,916,800, 13 give 479,001,600 and 15 give about 8.7 * 10^10. The DP step count at the same sizes is 16,384, 102,400, 247,808, 589,824, 1,384,448 and 7,372,800. In the sandbox the permutation search took 0.35 s at n = 10 against a few milliseconds for the DP (timings are sandbox-only, not proof; the growth is reasoned from the counts above). The cutoff of "about 11" is relative to an interview time limit of roughly a second or so; the DP handles n = 12 as a trivial case.
- What the DP buys: it notices that two different orders of the same set ending at the same city have the same future, so only the cheaper one is kept: subsets and an endpoint replace whole orders.

**Complexity:** Time O(2^n * n^2), space O(2^n * n) (halved by dropping city 0 from the mask). For n = 12: 4,096 masks * 12 endpoints = 49,152 states, under 600,000 transitions.

**Dry run:** `dist = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]`. Masks list the visited cities, always including 0; entry = cost ending at the given city (the run prints all of them):

| mask (cities) | f by ending city |
|---|---|
| {0} | 0 at city 0 |
| {0,1} | city 1: 10 |
| {0,2} | city 2: 15 |
| {0,3} | city 3: 20 |
| {0,1,2} | city 1: 15 + 35 = 50 (via 2); city 2: 10 + 35 = 45 (via 1) |
| {0,1,3} | city 1: 20 + 25 = 45; city 3: 10 + 25 = 35 |
| {0,2,3} | city 2: 20 + 30 = 50; city 3: 15 + 30 = 45 |
| {0,1,2,3} | city 1: 70 (from {0,2,3} ending 3: 45 + 25; ending 2 would give 50 + 35 = 85); city 2: 65 (from {0,1,3} ending 3: 35 + 30; ending 1 gives 45 + 35 = 80); city 3: 75 (from {0,1,2} ending 1: 50 + 25, or ending 2: 45 + 30, a tie) |

Closing the tour: ending at 1: 70 + 10 = 80; at 2: 65 + 15 = 80; at 3: 75 + 20 = 95. The minimum is 80, as in the prompt. One optimal tour is 0 -> 2 -> 3 -> 1 -> 0 (15 + 30 + 25 + 10).

**Code:**
```python
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
```

**Output (my run):**
```
prompt examples OK
f[mask][last]  (cities in mask, ending at last)
  mask 0001 [0]: {0: 0}
  mask 0011 [0, 1]: {1: 10}
  mask 0101 [0, 2]: {2: 15}
  mask 0111 [0, 1, 2]: {1: 50, 2: 45}
  mask 1001 [0, 3]: {3: 20}
  mask 1011 [0, 1, 3]: {1: 45, 3: 35}
  mask 1101 [0, 2, 3]: {2: 50, 3: 45}
  mask 1111 [0, 1, 2, 3]: {1: 70, 2: 65, 3: 75}
closing: {1: '70+10=80', 2: '65+15=80', 3: '75+20=95'} -> best 80
one optimal tour: (80, [0, 2, 3, 1, 0])
random cross-check: 300 matrices agree (also the half-size table, the memo and the recovered tour)
 n | (n-1)! tours | 2^n * n^2 DP steps
 8 |         5,040 |       16,384
10 |       362,880 |      102,400
11 |     3,628,800 |      247,808
12 |    39,916,800 |      589,824
13 |   479,001,600 |    1,384,448
15 | 87,178,291,200 |    7,372,800
n=9: permutations 0.03s, DP 0.001s  [sandbox time only]
n=10: permutations 0.32s, DP 0.003s  [sandbox time only]
n=12: DP 0.02s -> 911; 11! = 39,916,800 tours would need the permutation loop to run that many times (not run)
edge cases OK; limit 1000
```

**Edge cases:**
- n = 1: 0, no travel (the code special-cases it, since there is no `last != 0`).
- n = 2: `dist[0][1] + dist[1][0]` (`[[0,3],[5,0]]` gives 8: the matrix is asymmetric).
- Asymmetric distances: the direction matters; `[[0,1,9],[9,0,1],[1,9,0]]` gives 3 by going 0 -> 1 -> 2 -> 0 and would be 27 the other way round (0 -> 2 -> 1 -> 0: 9 + 9 + 9).
- All distances 0 or all equal: the answer is 0 or n * d.
- Zero-cost edges are fine (costs are only required to be non-negative by the prompt).
- Mask must always contain bit 0; starting from `f[0][0]` or a mask without bit 0 breaks the closing step.

**Follow-ups:**
- Print the tour? Walk the table backwards from the best `last` (the code does it): at each step find the previous city whose value plus the edge equals the current value.
- Dropping the return to city 0 (Hamiltonian path)? Answer `min over last of f[full][last]` and let every city be the start.
- n = 20? 2^20 * 20^2 = 4.2 * 10^8 steps is too slow in plain Python; use bit tricks or another language, or a heuristic when exactness is not required.

**Common mistakes:**
- Forgetting to add `dist[last][0]` for the return leg.
- Letting `last` equal 0 in the closing minimum for n > 1 (a path that visited everything must not end at 0 before closing).
- Iterating masks in the wrong order: transitions go to a larger mask, so ascending order is correct.
- Assuming symmetry: `dist[a][b] != dist[b][a]` is allowed.
