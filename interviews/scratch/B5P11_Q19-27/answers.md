### Q19 ⭐⭐ 🔴 Palindrome partitioning II: minimum cuts. `s` is a lowercase string with 1 <= len <= 2000. Cut it into pieces so that every piece is a palindrome; return the minimum number of cuts (0 if `s` is already a palindrome). Build a boolean table `pal[l][r]` in O(n^2) (by expanding around every center, or by the interval recurrence), then run a 1D DP `cuts[r] = 0 if pal[0][r] else min(cuts[l-1] + 1 over l with pal[l][r])`, and state the total time and space. A 2000 x 2000 table of Python booleans is large; say how much memory it needs roughly and one way to avoid it. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over all cut positions (len <= 10) on small inputs. Example: s='aab' -> 1; s='a' -> 0; s='ab' -> 1; s='aaaa' -> 0; s='abcbm' -> 2.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2020 on-campus Naukri Code360 report with a longest palindromic substring solved by a 2-D boolean DP table, a 2024 off-campus SDE-1 LeetCode Discuss report with a 2D DP array-splitting question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Two DPs stacked. An interval table (`pal[l][r]` = is `s[l..r]` a palindrome) feeds a 1D prefix DP (`cuts[r]`). Partition DP: the last piece is a palindrome `s[l..r]`, the rest is a smaller prefix.

**Say this first (1 line):** "First I make palindrome lookups O(1) with an O(n^2) table by expanding around every centre. Then `cuts[r]` is zero if the whole prefix is a palindrome, otherwise one more than the best prefix that ends just before the last palindromic piece."

**Brute force:** Recursion over all cut positions: `f(i)` = fewest cuts for `s[i:]`, try every `j` where `s[i:j]` is a palindrome, take `1 + f(j)`. Without a memo it can try up to 2^(n-1) partitions (every letter equal is the worst case). With a memo it is O(n^2) states times an O(n) palindrome check, so O(n^3). That is the oracle (len <= 10), not the answer.

**Optimal:**
- Table. `pal[l][r]` is true when `s[l] == s[r]` and the inside `pal[l+1][r-1]` is true (or the inside is empty or one letter). Expanding around each of the 2n-1 centres fills exactly the true cells: from `(l, r)` move out while the two ends match. Each true cell is touched once, each centre stops at its first mismatch, so the total is O(n^2) (worst case all letters equal).
- State: `cuts[r]` = fewest cuts for the prefix `s[0..r]` (r is the last index).
- Transition: if `pal[0][r]` then `cuts[r] = 0`. Otherwise the last piece is `s[l..r]` with `l >= 1` and `pal[l][r]` true, and the prefix before it is `s[0..l-1]`, so `cuts[r] = min(cuts[l-1] + 1)` over those `l`. The `+1` is the cut between the prefix and the last piece.
- Base: `cuts[0] = 0` (one letter is a palindrome). Answer `cuts[n-1]`. `l = r` is always valid, so the `min` is never empty.
- Time O(n^2), space O(n^2) for the table. 
- Memory at n = 2000: a list of lists holds 4,000,000 pointers at 8 bytes, about 32 MB (printed below; `True` and `False` are shared singletons, so the cost is the pointers, not the booleans). Ways out: (1) `bytearray` rows, about 4 MB; (2) triangle only, about 2 MB; (3) no table at all: while expanding around a centre, every palindrome `s[l..r]` found is a candidate last piece, so relax `cuts[r+1] = min(cuts[r+1], cuts[l] + 1)` on the spot (prefix-length indexing, `cuts[0] = -1`). That is O(n) extra space and the same O(n^2) time. The code has both versions and they agree.

**Complexity:** Time O(n^2): table O(n^2) (or relaxation during the expansion), then the `cuts` loop is O(n) per `r`, so O(n^2) again. Space O(n^2) with the table, O(n) with the relax-while-expanding version. Python's `min` over a generator makes the second loop the slow part for n = 2000 but still well inside a second.

**Dry run:** `s = 'aab'`.
- Table (`T` true, rows `l`, columns `r`): `l=0: T T F`, `l=1: . T F`, `l=2: . . T`. So `'aa'` is a palindrome and `'aab'`, `'ab'` are not.
- `r=0`: `pal[0][0]` true, `cuts[0] = 0`.
- `r=1`: `pal[0][1]` (`'aa'`) true, `cuts[1] = 0`.
- `r=2`: `pal[0][2]` false. Candidates `l` in 1..2 with `pal[l][2]` true: only `l=2` (`'b'`). `cuts[2] = cuts[1] + 1 = 1`.
- Answer 1: `aa | b`.

**Code:**
```python
import random, sys
from functools import lru_cache

random.seed(19)

def min_cuts(s):
    """Palindrome table by expanding around every centre, then cuts[r] over l with pal[l][r]."""
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):          # odd and even centres
            while l >= 0 and r < n and s[l] == s[r]:
                pal[l][r] = True
                l -= 1
                r += 1
    cuts = [0] * n                                    # cuts[r] = min cuts for s[0..r]
    for r in range(n):
        if pal[0][r]:
            cuts[r] = 0
        else:
            cuts[r] = min(cuts[l - 1] + 1 for l in range(1, r + 1) if pal[l][r])
    return cuts[-1]

def min_cuts_light(s):
    """O(n) extra space: no table. cuts[] is relaxed forward from every palindrome found while expanding."""
    n = len(s)
    cuts = list(range(-1, n))                         # cuts[k] = best cuts for the prefix of length k (cuts[0] = -1 sentinel)
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):
            while l >= 0 and r < n and s[l] == s[r]:
                # s[l..r] is a palindrome: the prefix of length r+1 can end with this piece
                if cuts[l] + 1 < cuts[r + 1]:
                    cuts[r + 1] = cuts[l] + 1
                l -= 1
                r += 1
    return cuts[n]

def brute(s):
    """Plain recursion over all cut positions: f(i) = fewest cuts for s[i:]."""
    def f(i):
        if i == len(s):
            return -1                                  # no piece left: the cut after the last piece is not made
        return min(1 + f(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return f(0)

# examples
for s, exp in [('aab', 1), ('a', 0), ('ab', 1), ('aaaa', 0), ('abcbm', 2)]:
    a, b, c = min_cuts(s), min_cuts_light(s), brute(s)
    assert a == b == c == exp, (s, a, b, c)
    print('example', repr(s), '->', a)

# hand table for 'aab'
s = 'aab'; n = len(s)
pal = [[s[l:r + 1] == s[l:r + 1][::-1] if l <= r else None for r in range(n)] for l in range(n)]
print('pal table for aab (rows l, cols r; None below diagonal):')
for l in range(n):
    print('  l=%d' % l, [('T' if v else 'F') if v is not None else '.' for v in pal[l]])
cuts = []
for r in range(n):
    if pal[0][r]:
        cuts.append(0); print('  r=%d pal[0][%d] is True -> cuts=0' % (r, r))
    else:
        cands = [(l, cuts[l - 1] + 1) for l in range(1, r + 1) if pal[l][r]]
        cuts.append(min(v for _, v in cands)); print('  r=%d candidates (l, cuts[l-1]+1) %s -> cuts=%d' % (r, cands, cuts[-1]))
print('cuts =', cuts)

# seeded cross-check: len <= 10, small alphabets so palindromes occur
cases = 0; hist = {}
for _ in range(600):
    alpha = random.choice(['ab', 'abc', 'a', 'abcd'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(1, 10)))
    exp = brute(s)
    assert min_cuts(s) == min_cuts_light(s) == exp, s
    cases += 1; hist[exp] = hist.get(exp, 0) + 1
print('cross-check cases', cases, '| answer histogram', dict(sorted(hist.items())))
# exhaustive over all binary strings up to length 10
cnt = 0
for L in range(1, 11):
    for bits in range(1 << L):
        s = format(bits, '0%db' % L)
        assert min_cuts(s) == min_cuts_light(s) == brute(s); cnt += 1
print('exhaustive binary strings len 1..10:', cnt)

# edge cases
assert min_cuts('a' * 2000) == 0
assert min_cuts('ab' * 50) == 1 == min_cuts_light('ab' * 50)   # 'a' + 'bab...ab' (the rest is a palindrome)
assert min_cuts('abcdefghij' * 5) == 49     # no palindrome longer than 1: every letter is its own piece
assert min_cuts_light('abcdefghij' * 5) == 49
assert min_cuts('a') == 0 == min_cuts_light('a')
print('edge asserts passed')

# memory of the table at n = 2000
n = 2000
tbl = [[False] * n for _ in range(n)]
outer = sys.getsizeof(tbl); rows = sum(sys.getsizeof(r) for r in tbl)
print('list-of-lists 2000x2000: rows', rows, 'bytes + outer', outer, '= about %.1f MB' % ((rows + outer) / 1e6))
tb = [bytearray(n) for _ in range(n)]
print('list of bytearrays 2000x2000: about %.1f MB' % ((sum(sys.getsizeof(r) for r in tb) + sys.getsizeof(tb)) / 1e6))
tri = [bytearray(n - l) for l in range(n)]
print('upper triangle only (l <= r): about %.1f MB' % (sum(sys.getsizeof(r) for r in tri) / 1e6))
import time
t0 = time.perf_counter(); r1 = min_cuts('ab' * 1000); t1 = time.perf_counter(); r2 = min_cuts_light('ab' * 1000); t2 = time.perf_counter()
print('n=2000 "ab"*1000 (sandbox timing): table version', r1, round(t1 - t0, 2), 's; light version', r2, round(t2 - t1, 2), 's')
import random as _r
_r.seed(5); w = ''.join(_r.choice('ab') for _ in range(2000))
t0 = time.perf_counter(); r1 = min_cuts(w); t1 = time.perf_counter(); r2 = min_cuts_light(w); t2 = time.perf_counter()
assert r1 == r2
print('n=2000 random binary (sandbox timing):', r1, round(t1 - t0, 2), 's;', round(t2 - t1, 2), 's')

# recursion: a memoised f(i) on a string with no palindrome longer than 1 nests n deep (observed on this Python, default limit)
def memo_cuts(s):
    @lru_cache(maxsize=None)
    def f(i):
        if i == len(s):
            return -1
        return min(1 + f(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return f(0)
print('recursion limit', sys.getrecursionlimit())
for n in (300, 2000):
    w = ('abc' * n)[:n]
    try:
        print('memoised recursion, n =', n, '->', memo_cuts(w), '(bottom-up gives', min_cuts_light(w), ')')
    except RecursionError:
        print('memoised recursion, n =', n, '-> RecursionError (bottom-up gives', min_cuts_light(w), ')')
```

**Output (my run):**
```
example 'aab' -> 1
example 'a' -> 0
example 'ab' -> 1
example 'aaaa' -> 0
example 'abcbm' -> 2
pal table for aab (rows l, cols r; None below diagonal):
  l=0 ['T', 'T', 'F']
  l=1 ['.', 'T', 'F']
  l=2 ['.', '.', 'T']
  r=0 pal[0][0] is True -> cuts=0
  r=1 pal[0][1] is True -> cuts=0
  r=2 candidates (l, cuts[l-1]+1) [(2, 1)] -> cuts=1
cuts = [0, 0, 1]
cross-check cases 600 | answer histogram {0: 226, 1: 162, 2: 106, 3: 53, 4: 25, 5: 18, 6: 6, 7: 4}
exhaustive binary strings len 1..10: 2046
edge asserts passed
list-of-lists 2000x2000: rows 32112000 bytes + outer 16184 = about 32.1 MB
list of bytearrays 2000x2000: about 4.1 MB
upper triangle only (l <= r): about 2.1 MB
n=2000 "ab"*1000 (sandbox timing): table version 1 0.24 s; light version 1 0.1 s
n=2000 random binary (sandbox timing): 320 0.17 s; 0.0 s
recursion limit 1000
memoised recursion, n = 300 -> 299 (bottom-up gives 299 )
memoised recursion, n = 2000 -> RecursionError (bottom-up gives 1999 )
```

Reading the output:
- All five examples match the table version, the light version and the plain recursion.
- 600 seeded random strings (len <= 10, alphabets of 1 to 4 letters) and all 2046 binary strings of length 1 to 10 agree across the three solutions. The histogram shows answers from 0 to 7 occurred, so both the "already a palindrome" branch and long chains of cuts were tested.
- Memory: a 2000 x 2000 list of lists is about 32 MB, `bytearray` rows about 4 MB, the triangle about 2 MB. Timings are sandbox-only.
- Recursion: the memoised top-down recursion on a 300-letter string with no palindrome longer than one letter works (depth about 300), and on 2000 letters it raises `RecursionError` at the default limit of 1000 (observation on Python 3.13, not a rule for every call path). The bottom-up code has no such limit.

**Edge cases:**
- `len(s) == 1`: 0 cuts.
- Whole string a palindrome: 0 (that is the `pal[0][r]` branch; without it the code would return at least 1 for a palindrome of length 2 or more, and crash on a single letter, because `l` starts at 1).
- All letters distinct (or no palindrome longer than 1): `n - 1`, every letter alone.
- Even-length centres (`(c, c+1)`) are easy to forget: without them `'aa'` and `'aaaa'` break.
- n = 2000 all equal: table fill is the worst case (about 2 million true cells), still fine.

**Follow-ups:**
- "Return the actual pieces?" Store `prev[r] = l` for the chosen minimum and walk back from `n-1`. Any tie rule must be stated; the count is unique, the partition is not.
- "Can you do it without the O(n^2) table?" Yes, the relax-while-expanding version above: O(n) extra space, same O(n^2) time.
- "Palindrome partitioning that lists all partitions?" That is enumeration, a backtracking problem (Part 12); the number of results can be exponential.

**Common mistakes:**
- Counting pieces instead of cuts (off by one: pieces = cuts + 1).
- Skipping even-length centres.
- Using `cuts[l]` instead of `cuts[l-1]` in the table version (the prefix ends at `l-1`).
- Building `pal` with `[[False]*n]*n` (all rows alias, see Part 10 Q31) or recomputing `s[l:r+1] == s[l:r+1][::-1]` inside the DP (O(n^3)).
- Plain recursion with no memo at n = 2000: exponential time; memoised recursion: `RecursionError`.

### Q20 ⭐⭐ 🔴 Dungeon game. `grid` is an m x n list of lists (1 <= m, n <= 200) of integers in -1000..1000: a negative cell costs health when entered, a positive cell gives health, and the start and end cells are included. A knight starts at the top-left with some positive integer health and moves only right or down to the bottom-right. His health must be at least 1 after every cell (including the first and the last). Return the smallest initial health that makes some path survive. Explain why the table must be filled from the bottom-right corner backwards (a forward DP on 'best sum so far' is not enough: give a small counter-example), give `need[i][j] = max(1, min(need[i+1][j], need[i][j+1]) - grid[i][j])` and its base case, and use one row. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) and computing the needed health for each on small inputs. Example: grid=[[-2, -3, 3], [-5, -10, 1], [10, 30, -5]] -> 7; grid=[[0]] -> 1; grid=[[100]] -> 1; grid=[[1, -3, 3], [0, -2, 0], [-3, -3, -3]] -> 3; grid=[[-5]] -> 6.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP, but backwards. The quantity "health I need when I stand here" depends only on what lies ahead, so the table is filled from the goal to the start.

**Say this first (1 line):** "Forward DP on 'best sum so far' fails because the best sum and the lowest dip are two different things. So I go backwards: `need[i][j]` is the minimum health I must have when I ENTER this cell, and it only depends on the cells after it."

**Brute force:** Enumerate all `C(m+n-2, m-1)` right/down paths. For each path walk it, track the running sum, and the needed health is `max(1, 1 - lowest prefix sum)`. Answer is the minimum over paths. Exponential; used as the oracle for m, n <= 5.

**Optimal:**
- State: `need[i][j]` = smallest health on entering `(i, j)` (before the cell's effect) that lets the knight reach the end alive.
- Transition: from `(i, j)` he goes to the cheaper of the two next cells, so he must leave with at least `min(need[i+1][j], need[i][j+1])`. His health after the cell is `h + grid[i][j]`, so `h >= nxt - grid[i][j]`. Health must also be at least 1 after the cell, and `nxt >= 1` already guarantees that on the way out; the outer `max(1, ...)` guarantees at least 1 on entering (this is what protects the first cell). So `need[i][j] = max(1, min(need[i+1][j], need[i][j+1]) - grid[i][j])`.
- Base: the end cell has `nxt = 1` (after the last cell he needs 1), so `need[m-1][n-1] = max(1, 1 - grid[m-1][n-1])`. Missing neighbours on the last row or column count as infinity.
- Why not forward: a forward DP wants one number per cell, "best sum so far". But a path with a bigger total can have dipped lower on the way (it needs a bigger starting health), and a path with a smaller total may never have dipped. Two paths to a cell are compared by (sum, lowest dip), which is not a total order. Backwards, the future is summarised by ONE number (health required), and smaller is always better. Counter-example in the code: `[[-3,-3,2],[-2,0,3]]`; the path with the largest total (-1, going right, right, down) needs 7, but the path down, right, right (total -2) needs only 6.
- One row: `need[j]` holds row `i+1` until it is overwritten with row `i`. Loop `i` from the bottom, `j` from the right. Then `need[j]` (not yet overwritten) is the cell below, and `need[j+1]` (already overwritten) is the cell to the right. The answer is `need[0]`.

**Complexity:** Time O(m * n). Space O(n) with one row (O(m * n) with the full table).

**Dry run:** `grid = [[-2,-3,3],[-5,-10,1],[10,30,-5]]`, filled from the bottom right.
- `(2,2)`: grid -5, nxt 1, need `max(1, 1+5) = 6`.
- `(2,1)`: grid 30, next is `(2,2)` need 6, `6 - 30 < 1` so 1. `(2,0)`: grid 10, next need 1, so 1. Bottom row `[1, 1, 6]`.
- Row 1: `(1,2)`: grid 1, below 6, `6 - 1 = 5`. `(1,1)`: grid -10, `min(below 1, right 5) = 1`, `1 + 10 = 11`. `(1,0)`: grid -5, `min(below 1, right 11) = 1`, `1 + 5 = 6`. Row `[6, 11, 5]`.
- Row 0: `(0,2)`: grid 3, below 5, `5 - 3 = 2`. `(0,1)`: grid -3, `min(below 11, right 2) = 2`, `2 + 3 = 5`. `(0,0)`: grid -2, `min(below 6, right 5) = 5`, `5 + 2 = 7`. Row `[7, 5, 2]`.
- Answer 7: follow right, right, down, down with health 7: after the cells 5, 2, 5, 6, 1. Never below 1, and 6 would end at 0.

**Code:**
```python
import random, itertools

random.seed(20)
INF = float('inf')

def dungeon(grid):
    """need[j] holds the row below until overwritten by row i. Filled from the bottom-right corner backwards."""
    m, n = len(grid), len(grid[0])
    need = [INF] * (n + 1)                      # need[n] is a sentinel to the right of the last column
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                nxt = 1                          # base: after the last cell health must be >= 1
            else:
                nxt = min(need[j] if i < m - 1 else INF,   # need[j] is still row i+1 (down)
                          need[j + 1] if j < n - 1 else INF)  # need[j+1] is already row i (right)
            need[j] = max(1, nxt - grid[i][j])
    return need[0]

def need_for_path(grid, moves):
    """Health needed to survive one fixed path: 1 - lowest prefix sum, at least 1."""
    i = j = 0; tot = grid[0][0]; low = tot
    for c in moves:
        if c == 'D': i += 1
        else: j += 1
        tot += grid[i][j]; low = min(low, tot)
    return max(1, 1 - low), tot

def all_paths(m, n):
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        yield s

def brute(grid):
    m, n = len(grid), len(grid[0])
    return min(need_for_path(grid, s)[0] for s in all_paths(m, n))

def forward_max_sum_wrong(grid):
    """The tempting forward DP: take the path with the largest total, then price that one path."""
    m, n = len(grid), len(grid[0]); best = None
    for s in all_paths(m, n):
        h, tot = need_for_path(grid, s)
        if best is None or tot > best[1]: best = (h, tot)
    return best[0]

# examples
for g, exp in [([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]], 7), ([[0]], 1), ([[100]], 1),
               ([[1, -3, 3], [0, -2, 0], [-3, -3, -3]], 3), ([[-5]], 6)]:
    a, b = dungeon(g), brute(g)
    assert a == b == exp, (g, a, b)
    print('example', g, '->', a)

# hand table for example 1 (full 2D version, printed)
g = [[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]
m, n = 3, 3
T = [[0] * n for _ in range(m)]
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
        if i == m - 1 and j == n - 1: nxt = 1
        else: nxt = min(T[i + 1][j] if i < m - 1 else INF, T[i][j + 1] if j < n - 1 else INF)
        T[i][j] = max(1, nxt - g[i][j])
print('need table (full 2D) for example 1:')
for row in T: print('  ', row)
assert T[0][0] == dungeon(g)

# counter-example to the forward 'best sum so far' DP
cx = [[-3, -3, 2], [-2, 0, 3]]
print('counter-example grid', cx, ': optimum', dungeon(cx), '| path with largest sum needs', forward_max_sum_wrong(cx))
assert dungeon(cx) == brute(cx) == 6 and forward_max_sum_wrong(cx) == 7
for s in all_paths(2, 3):
    print('   moves', ''.join(s), '-> (health needed, total sum) =', need_for_path(cx, s))

# seeded random cross-check, m, n <= 5
wrong = 0; cases = 0
for _ in range(500):
    m, n = random.randint(1, 5), random.randint(1, 5)
    g = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
    assert dungeon(g) == brute(g), g
    wrong += forward_max_sum_wrong(g) != brute(g)
    cases += 1
print('cross-check cases', cases, '| max-sum path was NOT optimal on', wrong)
# all 2 x 3 grids with values in -2..2
cnt = 0
for vals in itertools.product(range(-2, 3), repeat=6):
    g = [list(vals[:3]), list(vals[3:])]
    assert dungeon(g) == brute(g); cnt += 1
print('exhaustive 2 x 3 grids, values -2..2:', cnt)

# edge cases and max size
assert dungeon([[0]]) == 1 and dungeon([[100]]) == 1 and dungeon([[-5]]) == 6
assert dungeon([[-1000] * 200 for _ in range(200)]) == 1000 * 399 + 1   # 399 cells of -1000 (start included) -> 399000 + 1
print('200 x 200 all -1000 ->', dungeon([[-1000] * 200 for _ in range(200)]))
big = [[random.randint(-1000, 1000) for _ in range(200)] for _ in range(200)]
print('200 x 200 random ->', dungeon(big))
print('edge asserts passed')

# memoised top-down version: depth is at most m + n - 1 frames, so 200 x 200 (399 deep) is below the default limit of 1000
import sys
from functools import lru_cache
def dungeon_memo(grid):
    m, n = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == m - 1 and j == n - 1: nxt = 1
        else: nxt = min(f(i + 1, j) if i + 1 < m else INF, f(i, j + 1) if j + 1 < n else INF)
        return max(1, nxt - grid[i][j])
    return f(0, 0)
print('recursion limit', sys.getrecursionlimit(), '| memoised 200 x 200 equals bottom-up:', dungeon_memo(big) == dungeon(big))
g1 = [[-1] * 200 for _ in range(200)]
assert dungeon_memo(g1) == dungeon(g1)
print('memoised on 200 x 200 all -1:', dungeon_memo(g1))
```

**Output (my run):**
```
example [[-2, -3, 3], [-5, -10, 1], [10, 30, -5]] -> 7
example [[0]] -> 1
example [[100]] -> 1
example [[1, -3, 3], [0, -2, 0], [-3, -3, -3]] -> 3
example [[-5]] -> 6
need table (full 2D) for example 1:
   [7, 5, 2]
   [6, 11, 5]
   [1, 1, 6]
counter-example grid [[-3, -3, 2], [-2, 0, 3]] : optimum 6 | path with largest sum needs 7
   moves DRR -> (health needed, total sum) = (6, -2)
   moves RDR -> (health needed, total sum) = (7, -3)
   moves RRD -> (health needed, total sum) = (7, -1)
cross-check cases 500 | max-sum path was NOT optimal on 15
exhaustive 2 x 3 grids, values -2..2: 15625
200 x 200 all -1000 -> 399001
200 x 200 random -> 1
edge asserts passed
recursion limit 1000 | memoised 200 x 200 equals bottom-up: True
memoised on 200 x 200 all -1: 400
```

Reading the output:
- All five examples match the one-row DP and the path enumeration. The printed full table is the one in the dry run.
- The counter-example is real: the path with the largest sum needs 7, the optimum is 6. On 500 seeded random grids (m, n <= 5, values -10..10) the one-row DP equals the enumeration every time, and the largest-sum path was not optimal on 15 of them. So the failure of forward "best sum" is not a corner case, but it is not frequent on these random grids either.
- All 15,625 grids of shape 2 x 3 with values -2..2 agree.
- 200 x 200 runs instantly (sandbox, not a proof of big-O). A memoised top-down version nests at most m + n - 1 = 399 deep on 200 x 200, so it also runs at the default limit (printed); a much larger grid would not, which is why bottom-up is the safe default.

**Edge cases:**
- `[[100]]` is 1, not negative: the `max(1, ...)` clamp is the whole point.
- `[[-5]]` is 6 (needs 6 so that 6 - 5 = 1).
- Start or end cell may be negative; both are included.
- First row or column: the missing neighbour is infinity, not 0.
- Worst case values: all -1000 on 200 x 200 gives 399,001, because every path has 200 + 200 - 1 = 399 cells.

**Follow-ups:**
- "Why is greedy 'go to the bigger neighbour' wrong?" It ignores the future; the DP compares the true future requirement.
- "Can you move in four directions?" Then the grid is not a DAG and you need a shortest-path style search (binary search on health plus BFS, or Dijkstra on 'minimum health needed').
- "Print the path?" Walk forward from `(0,0)`, always stepping to the neighbour with the smaller `need`. That needs the full table, not one row.

**Common mistakes:**
- Forgetting `max(1, ...)` (answer 0 or negative).
- Filling top-left to bottom-right.
- Treating the end cell as a plain cell with no base (it needs `1 - grid`, clamped).
- Treating out-of-grid neighbours as 0 instead of infinity, which lets the knight "exit" early.
- Updating the one-row array left to right (then `need[j-1]`, not `need[j+1]`, is already overwritten).

### Q21 ⭐⭐ 🔴 Distinct subsequences (counting). `s` has 0 <= len <= 1000 and `t` has 0 <= len <= 500 lowercase letters. Return the exact number of ways to choose positions in `s` (increasing indices, so equal letters at different positions count separately) that spell `t`; the empty `t` has exactly 1 way. Define `dp[i][j]` = ways for the first i letters of s and the first j of t, give the transition (always add the ways that skip s[i-1], and add the ways that use it when it equals t[j-1]), and then use one row; say which direction the inner loop over j must run and why. Python integers do not overflow, but say where you would insert `% (10**9 + 7)` if a modulus were required and why the counting DP uses addition only. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every index combination (len(s) <= 10) on small inputs. Example: s='rabbbit', t='rabbit' -> 3; s='babgbag', t='bag' -> 5; s='abc', t='' -> 1; s='a', t='aa' -> 0; s='aaaa', t='aa' -> 6.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string counting DP. Prefix-by-prefix table over `(i, j)`: how many ways do the first `i` letters of `s` produce the first `j` letters of `t`. Counting, so addition only, no `max`.

**Say this first (1 line):** "`dp[i][j]` always includes the ways that skip `s[i-1]`, and adds the ways that use it when it equals `t[j-1]`. Row `i` only needs row `i-1`, so I keep one row and run `j` downwards."

**Brute force:** Try every choice of `len(t)` increasing positions in `s` (`itertools.combinations`) and count those that spell `t`. That is `C(len(s), len(t))` choices, exponential. A memoised recursion `f(i, j)` is polynomial (O(len(s) * len(t)) states) but nests about `len(s)` deep. Brute force is the oracle for `len(s) <= 10`.

**Optimal:**
- State: `dp[i][j]` = number of index sequences inside `s[:i]` that spell `t[:j]`.
- Transition: look at the last available letter `s[i-1]`. Either it is not used: `dp[i-1][j]` ways. Or it is used as the final letter of `t[:j]`, which needs `s[i-1] == t[j-1]`, and then the rest `t[:j-1]` is spelled inside `s[:i-1]`: `dp[i-1][j-1]` ways. The two cases are disjoint (used or not), so add: `dp[i][j] = dp[i-1][j] + (dp[i-1][j-1] if s[i-1] == t[j-1])`.
- Base: `dp[i][0] = 1` for every `i` (empty `t`: choose nothing, one way, even for empty `s`); `dp[0][j] = 0` for `j >= 1`.
- One row: `dp[j]` plays `dp[i-1][j]` until updated, and the update reads `dp[j-1]` from the PREVIOUS row. So `j` must run from `len(t)` down to 1. Run it ascending and `dp[j-1]` is already the new row, so `s[i-1]` gets used twice (for `t[j-2]` and `t[j-1]` in the same pass). The code shows this: `s='aaaa', t='aa'` gives 10 instead of 6, and the ascending loop was wrong on 93 of 300 random cases.
- Modulus: if the problem asked for `% (10**9 + 7)`, write `dp[j] = (dp[j] + dp[j-1]) % MOD` at the one place where two counts are added. The count is built only from additions of non-negative counts, so reducing after each addition is exact: `(a + b) % M == ((a % M) + (b % M)) % M`. There is no comparison, subtraction or division anywhere, so the residue is all that is ever needed. Python integers do not overflow, so here the modulus is only about the answer's required form; the true value for `'a'*1000` and `'a'*500` is `C(1000, 500)`, 300 digits.

**Complexity:** Time O(len(s) * len(t)) (at most 1000 x 500 = 500,000 cell updates). Space O(len(t)) with one row, O(len(s) * len(t)) with the full table. Big-integer additions grow with the count's digits; with the modulus each is O(1).

**Dry run:** `s = 'rabbbit'`, `t = 'rabbit'`. Rows below are the one-row array after each letter of `s` (columns j = 0..6 for `-,r,a,b,b,i,t`).
- start `[1,0,0,0,0,0,0]`
- after `r`: `[1,1,0,0,0,0,0]`; after `a`: `[1,1,1,0,0,0,0]`; after the first `b`: `[1,1,1,1,0,0,0]`.
- second `b`: `dp[4] += dp[3]` (1) and `dp[3] += dp[2]` (1+1): `[1,1,1,2,1,0,0]`.
- third `b`: `dp[4] += dp[3]` (1+2=3), `dp[3] += dp[2]` (2+1=3): `[1,1,1,3,3,0,0]`.
- `i`: `dp[5] += dp[4]` gives 3; `t`: `dp[6] += dp[5]` gives 3. Answer 3: choose which of the three `b`s is dropped.

**Code:**
```python
import random, itertools, sys
from math import comb
from functools import lru_cache

random.seed(21)
MOD = 10**9 + 7

def table(s, t):
    """2D: dp[i][j] = ways to spell t[:j] from s[:i]."""
    dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
    for i in range(len(s) + 1):
        dp[i][0] = 1                                   # empty t: exactly one way (choose nothing)
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            dp[i][j] = dp[i - 1][j]                    # skip s[i-1]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]           # use s[i-1] as t[j-1]
    return dp

def one_row(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):                 # j DESCENDING: dp[j-1] must still be the previous row
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]

def one_row_ascending_wrong(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(1, len(t) + 1):                 # ascending: dp[j-1] is already the NEW row, so s[i-1] is reused
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]

def one_row_mod(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                dp[j] = (dp[j] + dp[j - 1]) % MOD      # addition only: (a + b) % M == ((a % M) + (b % M)) % M
    return dp[-1]

def brute(s, t):
    return sum(1 for idx in itertools.combinations(range(len(s)), len(t)) if all(s[i] == c for i, c in zip(idx, t)))

def memo(s, t):
    @lru_cache(maxsize=None)
    def f(i, j):
        if j == len(t): return 1
        if i == len(s): return 0
        r = f(i + 1, j)
        if s[i] == t[j]: r += f(i + 1, j + 1)
        return r
    return f(0, 0)

# examples
for s, t, exp in [('rabbbit', 'rabbit', 3), ('babgbag', 'bag', 5), ('abc', '', 1), ('a', 'aa', 0), ('aaaa', 'aa', 6)]:
    a, b, c = one_row(s, t), table(s, t)[-1][-1], brute(s, t)
    assert a == b == c == exp == memo(s, t), (s, t, a, b, c)
    print('example', repr(s), repr(t), '->', a)

# hand table, first example
s, t = 'rabbbit', 'rabbit'
dp = table(s, t)
print('2D table dp[i][j] for s=rabbbit, t=rabbit (rows i = letters of s used, columns j = letters of t):')
print('        ' + '  '.join(['-'] + list(t)))
for i, row in enumerate(dp):
    print('  %s  ' % ('-' if i == 0 else s[i - 1]), row)
# one row, printed after each letter of s
row = [1] + [0] * len(t)
print('one row after each letter of s:')
for ch in s:
    for j in range(len(t), 0, -1):
        if t[j - 1] == ch: row[j] += row[j - 1]
    print('  after', ch, row)

# seeded cross-check, len(s) <= 10
cases = nz = 0
for _ in range(600):
    alpha = random.choice(['ab', 'abc', 'a'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(0, 10)))
    t = ''.join(random.choice(alpha) for _ in range(random.randint(0, 5)))
    exp = brute(s, t)
    assert one_row(s, t) == table(s, t)[-1][-1] == one_row_mod(s, t) == memo(s, t) == exp, (s, t)
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a positive count', nz)
wrong = sum(one_row_ascending_wrong(s, t) != brute(s, t)
            for s, t in [(''.join(random.choice('ab') for _ in range(random.randint(0, 8))), ''.join(random.choice('ab') for _ in range(random.randint(0, 4)))) for _ in range(300)])
print('ascending inner loop gave a wrong answer on', wrong, 'of 300 random cases; for s=aaaa, t=aa it returns', one_row_ascending_wrong('aaaa', 'aa'), 'instead of 6')

# closed forms and the modulus
assert one_row('a' * 50, 'a' * 25) == comb(50, 25)
assert one_row('a' * 1000, 'a' * 500) == comb(1000, 500)
big = comb(1000, 500)
print('C(1000, 500) has', len(str(big)), 'digits; mod version equals exact % M:', one_row_mod('a' * 1000, 'a' * 500) == big % MOD)
for _ in range(200):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 60))); t = ''.join(random.choice('ab') for _ in range(random.randint(0, 6)))
    assert one_row_mod(s, t) == one_row(s, t) % MOD

# recursion limit (observed)
print('recursion limit', sys.getrecursionlimit())
for n, m in ((300, 150), (1000, 500)):
    s, t = 'a' * n, 'a' * m
    try:
        print('memoised s=%d, t=%d ->' % (n, m), memo(s, t) == one_row(s, t))
    except RecursionError:
        print('memoised s=%d, t=%d -> RecursionError (bottom-up is fine)' % (n, m))

# edge cases
assert one_row('', '') == 1 and one_row('', 'a') == 0 and one_row('abc', '') == 1 and one_row('a', 'aa') == 0
assert one_row('abc', 'abcd') == 0
print('edge asserts passed')
```

**Output (my run):**
```
example 'rabbbit' 'rabbit' -> 3
example 'babgbag' 'bag' -> 5
example 'abc' '' -> 1
example 'a' 'aa' -> 0
example 'aaaa' 'aa' -> 6
2D table dp[i][j] for s=rabbbit, t=rabbit (rows i = letters of s used, columns j = letters of t):
        -  r  a  b  b  i  t
  -   [1, 0, 0, 0, 0, 0, 0]
  r   [1, 1, 0, 0, 0, 0, 0]
  a   [1, 1, 1, 0, 0, 0, 0]
  b   [1, 1, 1, 1, 0, 0, 0]
  b   [1, 1, 1, 2, 1, 0, 0]
  b   [1, 1, 1, 3, 3, 0, 0]
  i   [1, 1, 1, 3, 3, 3, 0]
  t   [1, 1, 1, 3, 3, 3, 3]
one row after each letter of s:
  after r [1, 1, 0, 0, 0, 0, 0]
  after a [1, 1, 1, 0, 0, 0, 0]
  after b [1, 1, 1, 1, 0, 0, 0]
  after b [1, 1, 1, 2, 1, 0, 0]
  after b [1, 1, 1, 3, 3, 0, 0]
  after i [1, 1, 1, 3, 3, 3, 0]
  after t [1, 1, 1, 3, 3, 3, 3]
cross-check cases 600 | with a positive count 351
ascending inner loop gave a wrong answer on 93 of 300 random cases; for s=aaaa, t=aa it returns 10 instead of 6
C(1000, 500) has 300 digits; mod version equals exact % M: True
recursion limit 1000
memoised s=300, t=150 -> True
memoised s=1000, t=500 -> RecursionError (bottom-up is fine)
edge asserts passed
```

Reading the output:
- All five examples match the one-row DP, the 2D table, the memoised recursion and the combination enumeration. The 2D table printed is the full version of the dry run.
- 600 seeded random cases (`len(s) <= 10`) agree across five implementations; 351 had a positive count, so both zero and non-zero answers were tested.
- The ascending inner loop is wrong (10 instead of 6 on `aaaa`/`aa`, wrong on 93 of 300 random cases).
- `C(1000, 500)` has 300 digits and the modulus version equals `exact % M`.
- Recursion: the memoised version on 300 x 150 works; on `s` of 1000 and `t` of 500 equal letters it raises `RecursionError` at the default limit of 1000, because it nests about `len(s)` deep (observation on Python 3.13). Bottom-up is unaffected.

**Edge cases:**
- Empty `t`: 1, even when `s` is empty (`('', '')` is 1, `('', 'a')` is 0).
- `len(t) > len(s)`: 0 (the DP finds it by itself).
- Equal letters count by position: `'aaaa'`/`'aa'` is 6 = `C(4, 2)`.
- Big answers: `'a'*1000` / `'a'*500` is a 300-digit integer; fine in Python, would overflow in C++ or Java.

**Follow-ups:**
- "Why does the counting DP use only `+`?" Each way is counted exactly once by its last-letter decision, so ways add; nothing is compared, so residues are safe.
- "Return the answer modulo 10^9+7?" Put `% MOD` on the single addition (and on the 2D version's cell). Do not mod the loop bounds or the letters.
- "Edit distance or LCS instead?" Same grid, `min`/`max` instead of `+` (Q8 edit distance and Q6 LCS of this part are the full tabulated versions).

**Common mistakes:**
- Inner loop ascending in the one-row version (reuses `s[i-1]`).
- Forgetting `dp[0] = 1` (everything becomes 0).
- Using `dp[i-1][j-1]` only when letters match, and forgetting to add the skip case `dp[i-1][j]` always.
- Counting distinct subsequence STRINGS (that is a different problem); here equal letters at different positions count separately.
- Memoised recursion at `len(s) = 1000`: `RecursionError`.

### Q22 ⭐⭐ 🔴 Burst balloons. `nums` has 0 <= len <= 300 integers in 0..100, one per balloon. Bursting the balloon at position i gives `left * nums[i] * right` coins, where `left` and `right` are the CURRENT neighbours (a missing neighbour counts as 1); the balloon then disappears. Return the maximum coins for bursting all balloons in the best order (0 for an empty list). Explain why 'which balloon bursts first' does not split the problem and 'which bursts LAST in the interval' does, give `dp[l][r]` on a list padded with a 1 at each end (open interval), the order in which interval lengths grow, and the O(n^3) time. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against trying every burst order by plain recursion (len <= 7) on small inputs. Example: nums=[3, 1, 5, 8] -> 167; nums=[1, 5] -> 10; nums=[7] -> 7; nums=[] -> 0; nums=[2, 2, 2] -> 14.
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP. The state is a range, ranges grow by length, and the transition picks a split point. The trick is choosing the right thing to split on: the LAST balloon, not the first.

**Say this first (1 line):** "If I pick the first balloon to burst, its neighbours change and the two sides still touch each other, so the problem does not split. If I pick the last balloon in an interval, everything else in it is already gone, so its neighbours are fixed: the two interval ends. Then the two sides are independent."

**Brute force:** Try every balloon as the next burst on the current list, recurse on the shorter list. `n!` orders. The recursion without a memo is the oracle (len <= 7, 5040 orders).

**Optimal:**
- Pad the list: `a = [1] + nums + [1]`. Use the OPEN interval `(l, r)`: the balloons strictly between indices `l` and `r`, with `a[l]` and `a[r]` still alive.
- State: `dp[l][r]` = best coins for bursting everything strictly between `l` and `r`.
- Transition: let `k` (`l < k < r`) be the balloon burst LAST inside `(l, r)`. At that moment only `a[l]` and `a[r]` remain next to it, so it earns `a[l] * a[k] * a[r]`. Before that, the balloons in `(l, k)` were burst with `a[l]` and `a[k]` as their outer neighbours and the balloons in `(k, r)` with `a[k]` and `a[r]`. These two sub-problems never see each other, because `a[k]` stands between them the whole time. So `dp[l][r] = max over k of dp[l][k] + dp[k][r] + a[l]*a[k]*a[r]`.
- Why "first" fails: after bursting `k` first, the left neighbour of `k`'s right neighbour is now `k`'s left neighbour. The left and right sides interact through every later burst near the gap, so `dp[left] + dp[right]` is not a valid split. The code shows a naive first-burst split that disagrees with the true optimum on 236 of 300 random lists (on `[3,1,5,8]` it gives 66, not 167).
- Base: `dp[l][l+1] = 0` (nothing between), and the table is zero-initialised. An empty `nums` gives `dp[0][1] = 0`.
- Order: by interval length (`r - l` from 2 up), because `dp[l][r]` needs shorter intervals `dp[l][k]` and `dp[k][r]`. Answer `dp[0][n+1]`.

**Complexity:** O(n^2) states times an O(n) scan over `k`: O(n^3) time (about n^3 / 6 inner steps, 4.5 million for n = 300), O(n^2) space. Python handles n = 300 in well under a second here (sandbox timing). Space can't drop to O(n) easily because `dp[l][r]` reads both `dp[l][k]` (same row) and `dp[k][r]` (later rows).

**Dry run:** `nums = [3, 1, 5, 8]`, padded `[1, 3, 1, 5, 8, 1]` (indices 0..5).
- Length 2 (one balloon between): `dp[0][2] = 1*3*1 = 3`, `dp[1][3] = 3*1*5 = 15`, `dp[2][4] = 1*5*8 = 40`, `dp[3][5] = 5*8*1 = 40`.
- Length 3: `dp[0][3]`: last `k=1`: `0 + dp[1][3] + 1*3*5 = 30`; last `k=2`: `dp[0][2] + 0 + 1*1*5 = 8`. Best 30. Similarly `dp[1][4] = 135`, `dp[2][5] = 48`.
- Length 4: `dp[0][4] = 159`, `dp[1][5] = 159`.
- Length 5, `dp[0][5]`: last is `3` gives `0 + 159 + 3 = 162`; last is `1` gives 52; last is `5` gives 75; last is `8` gives `159 + 0 + 8 = 167`. Answer 167 (burst 1, 5, 3, 8 in that order: 15 + 120 + 24 + 8).

**Code:**
```python
import random, sys, time
from functools import lru_cache

random.seed(22)

def burst(nums):
    """dp[l][r] = best coins for the balloons strictly between l and r, which stay un-burst until the end (open interval)."""
    a = [1] + list(nums) + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):                   # r - l = 2 is one balloon between; shorter intervals are empty (0)
        for l in range(0, n - length):
            r = l + length
            best = 0
            for k in range(l + 1, r):            # k = the balloon burst LAST inside (l, r)
                c = dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]
                if c > best: best = c
            dp[l][r] = best
    return dp[0][n - 1]

def burst_table(nums):
    a = [1] + list(nums) + [1]; n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            dp[l][r] = max(dp[l][k] + dp[k][r] + a[l] * a[k] * a[r] for k in range(l + 1, r))
    return a, dp

def memo(nums):
    a = [1] + list(nums) + [1]
    @lru_cache(maxsize=None)
    def f(l, r):
        return max((f(l, k) + f(k, r) + a[l] * a[k] * a[r] for k in range(l + 1, r)), default=0)
    return f(0, len(a) - 1)

def brute(nums):
    """Every burst order by plain recursion on the current list (neighbours are the CURRENT neighbours)."""
    def f(arr):
        if not arr: return 0
        return max((arr[i - 1] if i else 1) * arr[i] * (arr[i + 1] if i + 1 < len(arr) else 1) + f(arr[:i] + arr[i + 1:])
                   for i in range(len(arr)))
    return f(list(nums))

def first_burst_wrong(nums):
    """Tempting split on the FIRST balloon: pretend the two sides become independent, each with outer neighbours 1."""
    nums = list(nums)
    if not nums: return 0
    best = 0
    for k in range(len(nums)):
        left = nums[k - 1] if k else 1
        right = nums[k + 1] if k + 1 < len(nums) else 1
        best = max(best, left * nums[k] * right + first_burst_wrong(nums[:k]) + first_burst_wrong(nums[k + 1:]))
    return best

# examples
for nums, exp in [([3, 1, 5, 8], 167), ([1, 5], 10), ([7], 7), ([], 0), ([2, 2, 2], 14)]:
    a, b, c = burst(nums), brute(nums), memo(nums)
    assert a == b == c == exp, (nums, a, b, c)
    print('example', nums, '->', a)

# hand table for [3,1,5,8]
a, dp = burst_table([3, 1, 5, 8])
print('padded list', a)
print('dp[l][r] (open interval, rows l, columns r):')
for l in range(len(a)):
    print('  l=%d' % l, dp[l])
print('dp[0][5] = 167, last balloon k tried in (0,5):')
for k in range(1, 5):
    print('   k=%d (value %d): dp[0][%d] + dp[%d][5] + 1*%d*1 = %d + %d + %d = %d' % (k, a[k], k, k, a[k], dp[0][k], dp[k][5], a[0] * a[k] * a[5], dp[0][k] + dp[k][5] + a[0] * a[k] * a[5]))

# seeded cross-check, len <= 7
cases = 0
for _ in range(400):
    nums = [random.randint(0, 9) for _ in range(random.randint(0, 7))]
    assert burst(nums) == brute(nums) == memo(nums), nums
    cases += 1
print('cross-check cases', cases)
wrong = 0
for _ in range(300):
    nums = [random.randint(1, 9) for _ in range(random.randint(2, 6))]
    wrong += first_burst_wrong(nums) != burst(nums)
print('first-burst split disagrees with the true optimum on', wrong, 'of 300 random lists; e.g. [3, 1, 5, 8] gives', first_burst_wrong([3, 1, 5, 8]), 'not 167')

# edge cases (values 0..100, zeros included)
assert burst([0]) == 0 and burst([0, 0, 0]) == 0 and burst([100]) == 100
assert burst([100, 100]) == 100 * 100 + 100
print('edge asserts passed')

# max size n = 300, bottom-up; memo depth
print('recursion limit', sys.getrecursionlimit())
nums = [random.randint(0, 100) for _ in range(300)]
t0 = time.perf_counter(); r = burst(nums); t1 = time.perf_counter()
print('n=300 bottom-up:', r, '(sandbox timing %.1f s)' % (t1 - t0))
try:
    print('n=300 memoised equals bottom-up:', memo(nums) == r)
except RecursionError:
    print('n=300 memoised: RecursionError')
big = [random.randint(0, 100) for _ in range(1100)]
try:
    memo(big); print('n=1100 memoised ran')
except RecursionError:
    print('n=1100 memoised: RecursionError (depth grows with n; outside the stated sizes)')
```

**Output (my run):**
```
example [3, 1, 5, 8] -> 167
example [1, 5] -> 10
example [7] -> 7
example [] -> 0
example [2, 2, 2] -> 14
padded list [1, 3, 1, 5, 8, 1]
dp[l][r] (open interval, rows l, columns r):
  l=0 [0, 0, 3, 30, 159, 167]
  l=1 [0, 0, 0, 15, 135, 159]
  l=2 [0, 0, 0, 0, 40, 48]
  l=3 [0, 0, 0, 0, 0, 40]
  l=4 [0, 0, 0, 0, 0, 0]
  l=5 [0, 0, 0, 0, 0, 0]
dp[0][5] = 167, last balloon k tried in (0,5):
   k=1 (value 3): dp[0][1] + dp[1][5] + 1*3*1 = 0 + 159 + 3 = 162
   k=2 (value 1): dp[0][2] + dp[2][5] + 1*1*1 = 3 + 48 + 1 = 52
   k=3 (value 5): dp[0][3] + dp[3][5] + 1*5*1 = 30 + 40 + 5 = 75
   k=4 (value 8): dp[0][4] + dp[4][5] + 1*8*1 = 159 + 0 + 8 = 167
cross-check cases 400
first-burst split disagrees with the true optimum on 236 of 300 random lists; e.g. [3, 1, 5, 8] gives 66 not 167
edge asserts passed
recursion limit 1000
n=300 bottom-up: 113082798 (sandbox timing 0.6 s)
n=300 memoised equals bottom-up: True
n=1100 memoised: RecursionError (depth grows with n; outside the stated sizes)
```

Reading the output:
- All five examples match the O(n^3) table, the memoised version and the every-order recursion. The printed table is the one in the dry run, and the last `for k` lines show the four candidates for `dp[0][5]`.
- 400 seeded random lists of length 0 to 7 (values 0..9, so zero-value balloons appear) agree across the three implementations.
- Recursion: the memoised recursion nests about `n` deep. On 300 balloons it equals the table; on 1100 it raises `RecursionError` at the default limit of 1000 (observation on Python 3.13; 1100 is outside the stated size and shown only to mark the cause). The stated limit n = 300 is safe either way, and bottom-up has no depth issue.

**Edge cases:**
- Empty list: 0 (padding gives two 1s and no balloons between).
- One balloon: its own value (`1 * v * 1`).
- Zeros: allowed; bursting a zero earns nothing but removes it as a neighbour. Padding with 1, not 0, keeps ends from erasing everything.
- All equal values and n = 300: the table is full but still O(n^3).

**Follow-ups:**
- "Recover the burst order?" Store the best `k` per `(l, r)`, then recurse: the order is the last balloon of the whole interval being burst last, so print the order for `(l, k)` and `(k, r)` first, then `k`.
- "Why O(n^3) and not O(n^2)?" Each of O(n^2) intervals scans O(n) split points. Same shape as matrix chain (Q23).
- "Same idea elsewhere?" Minimum cost to cut a stick and minimum score triangulation: choose the last cut or the last triangle on the edge, so the pieces are independent.

**Common mistakes:**
- Splitting on the first balloon (the sides are not independent).
- Using a closed interval and forgetting that the neighbours at the ends are the interval ends, not the balloons next to them in the original list.
- Padding with 0 instead of 1 (everything becomes 0).
- Iterating `l` and `r` in plain nested order instead of by length (reads cells that are not filled yet).
- Mutating the list while recursing in the brute force instead of building a new list.

### Q23 ⭐⭐ 🔴 Matrix chain multiplication with the parenthesisation. `dims` has 2 <= len <= 201 positive integers (each <= 100); matrix i (0-indexed) has dims[i] rows and dims[i+1] columns, so there are n = len(dims) - 1 matrices. Multiplying an a x b matrix by a b x c matrix costs a*b*c scalar multiplications. Return `[cost, expr]`: the minimum total cost to multiply all matrices in order, and one optimal parenthesisation written as a string such as `((A0A1)A2)` (a single matrix is `A0`). Several parenthesisations can tie, so the tie rule is fixed: split an interval at the smallest k (left part A_i..A_k) that achieves the minimum, applied recursively. Define `dp[i][j]`, the split recurrence and the interval order, and state O(n^3) time and O(n^2) space. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every parenthesisation (n <= 6) and choosing by cost then by smallest root split, recursively on small inputs. Example: dims=[10, 30, 5, 60] -> [4500, '((A0A1)A2)']; dims=[40, 20, 30, 10, 30] -> [26000, '((A0(A1A2))A3)']; dims=[5, 7] -> [0, 'A0']; dims=[1, 2, 3, 4, 5] -> [38, '(((A0A1)A2)A3)'].
**Asked at:** Interval DP guides (techinterview.org DP on intervals and advanced DP patterns, a LeetCode Discuss interval-DP study guide, a DP pattern cheat sheet; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval DP with a split point, plus reconstruction from a split table. `dp[i][j]` is the best cost for the sub-chain `A_i..A_j`, built from shorter sub-chains.

**Say this first (1 line):** "The last multiplication splits the chain at some `k`: left part `A_i..A_k`, right part `A_k+1..A_j`. Both parts are optimal on their own, and the final product costs `dims[i] * dims[k+1] * dims[j+1]`. I try every `k`, keep the smallest one that achieves the minimum, and rebuild the string from the split table."

**Brute force:** Enumerate every full parenthesisation: Catalan(n-1) of them (5 for 4 matrices, 14 for 5, 42 for 6, a 117-digit number for 200). For each compute the cost, then pick by cost and by the tie rule (smallest root split `k`, then recursively the left tree, then the right tree). That is the oracle for n <= 6.

**Optimal:**
- Matrix `A_i` is `dims[i] x dims[i+1]`. The product `A_i..A_j` is `dims[i] x dims[j+1]`.
- State: `cost[i][j]` for `0 <= i <= j < n`, `split[i][j]` = chosen `k`.
- Transition: `cost[i][j] = min over k in [i, j-1] of cost[i][k] + cost[k+1][j] + dims[i] * dims[k+1] * dims[j+1]`. The first two terms are the two sub-chains; the last is the final multiplication of a `dims[i] x dims[k+1]` by a `dims[k+1] x dims[j+1]` matrix.
- Base: `cost[i][i] = 0` (a single matrix needs no multiplication).
- Order: by chain length 2, 3, ..., n, so shorter sub-chains are ready. Answer `cost[0][n-1]`.
- Tie rule: scan `k` upwards and update only on a STRICT improvement (`c < best`). The first, smallest `k` is kept. Applying the rule at every interval gives the oracle's choice: the oracle compares trees by cost, then by `(k, left key, right key)`; for a fixed root `k` the best total needs both sub-chains optimal, and among those the smallest keys are what the same rule picks inside each sub-chain. Verified exhaustively below.
- Rebuild: `paren(i, j)` returns `A_i` when `i == j`, else `'(' + paren(i, k) + paren(k+1, j) + ')'` with `k = split[i][j]`. The recursion depth is at most `n - 1 = 199` for the stated size, below CPython's default limit of 1000, so plain recursion is fine here.
- Time O(n^3): O(n^2) intervals times an O(n) scan. Space O(n^2) for the two tables.

**Complexity:** Time O(n^3) (about n^3 / 6 split evaluations, 1.3 million for 200 matrices; the table loop ran in a fraction of a second here, sandbox timing). Space O(n^2). The string has about 5n characters, so building it is O(n) per level and O(n^2) in the worst case, small beside the DP.

**Dry run:** `dims = [10, 30, 5, 60]`: A0 is 10x30, A1 is 30x5, A2 is 5x60.
- Length 2: `cost[0][1] = 10*30*5 = 1500` (split 0); `cost[1][2] = 30*5*60 = 9000` (split 1).
- Length 3, `cost[0][2]`: `k=0`: `cost[0][0] + cost[1][2] + 10*30*60 = 0 + 9000 + 18000 = 27000`. `k=1`: `cost[0][1] + cost[2][2] + 10*5*60 = 1500 + 0 + 3000 = 4500`. The minimum is 4500 at `k=1`.
- Rebuild: root split 1, so `(` + `paren(0,1)` + `paren(2,2)` + `)` = `((A0A1)A2)`. Answer `[4500, '((A0A1)A2)']`.
- A tie: `dims = [2, 2, 2, 2]` makes both parenthesisations cost 16, and the rule returns `(A0(A1A2))` (root split `k=0` is smaller than `k=1`).

**Code:**
```python
import random, itertools, sys, time

random.seed(23)

def matrix_chain(dims):
    """cost[i][j] = fewest scalar multiplications for matrices A_i..A_j; split[i][j] = smallest k achieving it."""
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = None
            for k in range(i, j):                      # left part A_i..A_k, right part A_k+1..A_j
                c = cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if best is None or c < best:           # STRICT <: the first (smallest) k wins ties
                    best = c
                    split[i][j] = k
            cost[i][j] = best

    def paren(i, j):
        if i == j:
            return 'A%d' % i
        k = split[i][j]
        return '(' + paren(i, k) + paren(k + 1, j) + ')'
    return [cost[0][n - 1], paren(0, n - 1)], cost, split

def solve(dims):
    return matrix_chain(dims)[0]

def brute(dims):
    """Enumerate every parenthesisation; choose by cost, then by smallest root split, then (recursively) left tree, then right tree."""
    n = len(dims) - 1
    def trees(i, j):
        if i == j:
            yield (0, (), 'A%d' % i)
            return
        for k in range(i, j):
            for cl, kl, sl in trees(i, k):
                for cr, kr, sr in trees(k + 1, j):
                    yield (cl + cr + dims[i] * dims[k + 1] * dims[j + 1], (k, kl, kr), '(' + sl + sr + ')')
    best = min(trees(0, n - 1), key=lambda t: (t[0], t[1]))
    return [best[0], best[2]]

def count_trees(n):                                     # Catalan(n - 1)
    from math import comb
    return comb(2 * (n - 1), n - 1) // n

# examples
for dims, exp in [([10, 30, 5, 60], [4500, '((A0A1)A2)']), ([40, 20, 30, 10, 30], [26000, '((A0(A1A2))A3)']),
                  ([5, 7], [0, 'A0']), ([1, 2, 3, 4, 5], [38, '(((A0A1)A2)A3)'])]:
    a, b = solve(dims), brute(dims)
    assert a == b == exp, (dims, a, b)
    print('example', dims, '->', a)

# hand table for dims = [10, 30, 5, 60]
dims = [10, 30, 5, 60]
_, cost, split = matrix_chain(dims)
print('dims', dims, '-> matrices A0 10x30, A1 30x5, A2 5x60')
print('cost table (rows i, columns j):')
for row in cost: print('  ', row)
print('split table:')
for row in split: print('  ', row)
print('cost[0][2]: k=0 ->', cost[0][0] + cost[1][2] + 10 * 30 * 60, ' k=1 ->', cost[0][1] + cost[2][2] + 10 * 5 * 60)

# a tie to show the smallest-k rule: all dims equal, every parenthesisation costs the same
print('tie example dims [2,2,2,2] ->', solve([2, 2, 2, 2]), '(all', count_trees(3), 'trees cost 16; smallest root split k=0 wins)')
assert solve([2, 2, 2, 2]) == [16, '(A0(A1A2))']

# seeded cross-check, n <= 6 matrices, small dims so ties are common
cases = 0
for _ in range(400):
    n = random.randint(1, 6)
    dims = [random.randint(1, 4) for _ in range(n + 1)]
    got, want = solve(dims), brute(dims)
    assert got == want, (dims, got, want)
    cases += 1
print('cross-check cases', cases)

# exhaustive: all chains of 4 matrices (5 dims) with dims in 1..3, and all of 3 matrices with dims 1..5
cnt = 0
for dims in itertools.product(range(1, 4), repeat=5):
    assert solve(list(dims)) == brute(list(dims)); cnt += 1
for dims in itertools.product(range(1, 6), repeat=4):
    assert solve(list(dims)) == brute(list(dims)); cnt += 1
print('exhaustive chains checked:', cnt)

# how many random chains had more than one optimal tree (so the tie rule mattered)
def all_optimal(dims):
    n = len(dims) - 1
    def trees(i, j):
        if i == j:
            yield (0, 'A%d' % i); return
        for k in range(i, j):
            for cl, sl in trees(i, k):
                for cr, sr in trees(k + 1, j):
                    yield (cl + cr + dims[i] * dims[k + 1] * dims[j + 1], '(' + sl + sr + ')')
    ts = list(trees(0, n - 1)); m = min(t[0] for t in ts)
    return sum(1 for t in ts if t[0] == m)
multi = 0
random.seed(230)
for _ in range(300):
    n = random.randint(2, 6)
    dims = [random.randint(1, 4) for _ in range(n + 1)]
    multi += all_optimal(dims) > 1
print('of 300 more random chains (n 2..6), several optimal parenthesisations existed in', multi)

# edge cases
assert solve([5, 7]) == [0, 'A0']
assert solve([3, 4, 5]) == [60, '(A0A1)']

# max size: 200 matrices (dims 201 long), recursion depth of paren() is at most n
print('recursion limit', sys.getrecursionlimit())
dims = [random.randint(1, 100) for _ in range(201)]
t0 = time.perf_counter(); res = solve(dims); t1 = time.perf_counter()
print('n=200 matrices: cost', res[0], '| string length', len(res[1]), '(sandbox timing %.1f s)' % (t1 - t0))
# all-ones dims: every tree costs n - 1, the smallest-k rule gives the right-deep tree, nesting depth 199 (below the default limit of 1000)
d2 = [1] * 201
res2 = solve(d2); print('n=200 all-ones dims: cost', res2[0], '| string starts', res2[1][:20])
assert res2[0] == 199 and res2[1].count('(') == 199
```

**Output (my run):**
```
example [10, 30, 5, 60] -> [4500, '((A0A1)A2)']
example [40, 20, 30, 10, 30] -> [26000, '((A0(A1A2))A3)']
example [5, 7] -> [0, 'A0']
example [1, 2, 3, 4, 5] -> [38, '(((A0A1)A2)A3)']
dims [10, 30, 5, 60] -> matrices A0 10x30, A1 30x5, A2 5x60
cost table (rows i, columns j):
   [0, 1500, 4500]
   [0, 0, 9000]
   [0, 0, 0]
split table:
   [0, 0, 1]
   [0, 0, 1]
   [0, 0, 0]
cost[0][2]: k=0 -> 27000  k=1 -> 4500
tie example dims [2,2,2,2] -> [16, '(A0(A1A2))'] (all 2 trees cost 16; smallest root split k=0 wins)
cross-check cases 400
exhaustive chains checked: 868
of 300 more random chains (n 2..6), several optimal parenthesisations existed in 70
recursion limit 1000
n=200 matrices: cost 503525 | string length 1088 (sandbox timing 0.3 s)
n=200 all-ones dims: cost 199 | string starts (A0(A1(A2(A3(A4(A5(A
```

Reading the output:
- All four examples match the DP and the enumeration. The cost and split tables printed are the ones in the dry run; the `k=0` and `k=1` candidates for `cost[0][2]` are 27000 and 4500.
- 400 seeded random chains (n <= 6, dims 1..4) match the oracle in both cost AND string, and in the extra 300 random chains several optimal parenthesisations existed in 70, so the tie rule was really exercised.
- Exhaustive: all 243 chains of 4 matrices with dims in 1..3 and all 625 chains of 3 matrices with dims in 1..5 agree (868 in all).
- 200 matrices: runs in a fraction of a second here (sandbox timing). With all dims 1 every tree costs 199, and the smallest-`k` rule produces the right-deep tree with nesting depth 199, still far from the limit.

**Edge cases:**
- One matrix (`len(dims) == 2`): cost 0, string `A0`, no loop runs.
- Two matrices: one product, string `(A0A1)`.
- Ties: many optimal trees; the strict `<` is what makes the answer match the stated rule. With `<=` you would get the LARGEST `k`.
- Dimension 1 entries (vectors): fine, they just make some products cheap.
- All equal dims: every tree ties.

**Follow-ups:**
- "Can you print it without recursion?" Yes, with an explicit stack of `(i, j)`. At n <= 200 recursion is fine; for thousands of matrices (the O(n^3) table would not fit anyway) you would need it.
- "Faster than O(n^3)?" Hu and Shing's O(n log n) algorithm exists; it is not an interview expectation.
- "Same pattern?" Optimal BST, minimum cost to cut a stick, burst balloons (Q22), polygon triangulation: all `dp[i][j] = min over k of dp[i][k] + dp[k][j] + merge cost`.

**Common mistakes:**
- Using `dims[i] * dims[k] * dims[j]`, off by one: matrix `A_i` has `dims[i]` rows and `dims[i+1]` columns, so the product of the two halves is `dims[i] * dims[k+1] * dims[j+1]`.
- Iterating by `i` then `j` instead of by length (reads cells not computed yet).
- `<=` instead of `<` in the minimum, so ties pick the largest `k` and the string differs from the required one.
- Not clearing or sizing the tables for `n = len(dims) - 1` (using `len(dims)` adds a phantom matrix).
- Returning the cost only; the prompt wants `[cost, expr]`.

### Q24 ⭐⭐ 🔴 Longest increasing path in a matrix. `matrix` is an m x n list of lists (1 <= m, n <= 200) of integers in 0..10^9. From a cell you may move up, down, left or right to a cell with a STRICTLY larger value; return the number of cells on the longest such path (a single cell counts as 1). The cells form a directed acyclic graph, so this is a DP over a DAG (the shortest-path-on-a-DAG version is Part 9 Q40). A memoised DFS nests as deep as the longest increasing path it follows, and a winding corridor of increasing values (with walls of value 0 between its rows) makes that thousands of cells, far beyond CPython's recursion limit of 1000, so a bottom-up solution is required: process the cells in increasing order of value (and say why equal values need no special order) or use a topological sort on in-degrees. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain DFS from every cell without a memo (m, n <= 3) on small inputs. Example: matrix=[[9, 9, 4], [6, 6, 8], [2, 1, 1]] -> 4; matrix=[[3, 4, 5], [3, 2, 6], [2, 2, 1]] -> 4; matrix=[[1]] -> 1; matrix=[[1, 1], [1, 1]] -> 1.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** DP over a DAG on a grid. An edge goes from a cell to a strictly larger neighbour, so there are no cycles. Longest path in a DAG = process vertices in topological order. Here the topological order is just "sort by value". (The shortest-path-on-a-DAG version is Part 9 Q40.)

**Say this first (1 line):** "Strictly increasing means the cells form a DAG. If I process cells from small to large value, every smaller neighbour is already final, so `L[i][j] = 1 + max(L of strictly smaller neighbours)`. No recursion, so no depth problem."

**Brute force:** DFS from every cell with no memo, trying all four moves to strictly larger cells. Each cell can be reached along many paths, so time is exponential in the path length. It is the oracle for m, n <= 3.

**Optimal:**
- State: `L[i][j]` = number of cells on the longest increasing path that ENDS at `(i, j)`. Answer is the maximum over all cells.
- Transition: `L[i][j] = 1 + max(L[a][b])` over the four neighbours with `matrix[a][b] < matrix[i][j]`, or 1 if there is none. Base: every cell starts at 1 (the path of one cell).
- Order: sort all cells by value (`sorted` on tuples `(value, i, j)`) and fill in that order. A strictly smaller neighbour has a strictly smaller value, so it is earlier in the order and its `L` is final.
- Why equal values need no special order: an equal neighbour is never read (the test is `<`), so the position of equal cells relative to each other changes nothing. The code shuffles the order among equal values and checks all 19,683 3 x 3 matrices with values 0..2 (the shuffle on every 7th) and the answer never changes.
- Alternative, Kahn's topological sort: in-degree of a cell = number of strictly smaller neighbours. Start from in-degree 0 (local minima). Peel layer by layer; the number of layers is the longest path length. It is O(mn) with no sort.
- Why bottom-up is required: a memoised DFS `f(i, j)` nests as deep as the longest increasing path it follows. A winding corridor of increasing values, with walls of value 0 between its rows, makes that path thousands of cells long. On a 61 x 61 corridor (1921 corridor cells) the memoised DFS raises `RecursionError` at the default limit of 1000 (observation on Python 3.13; a 21 x 21 corridor with 241 cells runs). The sorted-order DP and Kahn take the same input in a few hundredths of a second (sandbox timing), even on the 199 x 199 corridor with about 20,000 cells.

**Complexity:** Sorted version: O(mn log(mn)) time for the sort plus O(mn) for the relaxations (4 neighbours per cell); space O(mn). Kahn: O(mn) time, O(mn) space. For 200 x 200 that is 40,000 cells.

**Dry run:** `[[9,9,4],[6,6,8],[2,1,1]]`. Cells in increasing value (ties in position order); `L` after each:
- The two 1s, `(2,1)` and `(2,2)`: no smaller neighbour, `L = 1`.
- `2` at `(2,0)`: neighbour `(2,1)` has value 1, so `L = 2`.
- `4` at `(0,2)`: neighbours `9` and `8` are larger, none smaller, `L = 1`.
- `6` at `(1,0)`: neighbour `(2,0)` has `L = 2`, so `L = 3`. `6` at `(1,1)`: smaller neighbour `(2,1)` (1), `L = 2`.
- `8` at `(1,2)`: smaller neighbours `4` (L 1), `6` at `(1,1)` (L 2), `1` (L 1): `L = 3`.
- `9` at `(0,0)`: smaller neighbour `6` at `(1,0)` (L 3), so `L = 4`. `9` at `(0,1)`: `6` below (L 2), `4` to its right (L 1): `L = 3`.
- Final `L = [[4,3,1],[3,2,3],[2,1,1]]`, answer 4: `1 -> 2 -> 6 -> 9`.

**Code:**
```python
import random, sys, time, itertools
from collections import deque
from functools import cache

random.seed(24)
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def lip_sorted(matrix):
    """L[i][j] = cells on the longest increasing path that ENDS at (i, j). Cells in increasing value order."""
    m, n = len(matrix), len(matrix[0])
    order = sorted((matrix[i][j], i, j) for i in range(m) for j in range(n))
    L = [[1] * n for _ in range(m)]
    best = 1
    for v, i, j in order:
        for di, dj in DIRS:
            a, b = i + di, j + dj
            if 0 <= a < m and 0 <= b < n and matrix[a][b] < v:       # strictly smaller neighbour: already final
                if L[a][b] + 1 > L[i][j]:
                    L[i][j] = L[a][b] + 1
        if L[i][j] > best:
            best = L[i][j]
    return best

def lip_kahn(matrix):
    """Topological peel: edge small -> big; in-degree = number of strictly smaller neighbours. Answer = number of layers."""
    m, n = len(matrix), len(matrix[0])
    indeg = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for di, dj in DIRS:
                a, b = i + di, j + dj
                if 0 <= a < m and 0 <= b < n and matrix[a][b] < matrix[i][j]:
                    indeg[i][j] += 1
    q = deque((i, j) for i in range(m) for j in range(n) if indeg[i][j] == 0)
    layers = 0
    while q:
        layers += 1
        for _ in range(len(q)):
            i, j = q.popleft()
            for di, dj in DIRS:
                a, b = i + di, j + dj
                if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[i][j]:
                    indeg[a][b] -= 1
                    if indeg[a][b] == 0:
                        q.append((a, b))
    return layers

def lip_memo(matrix):
    m, n = len(matrix), len(matrix[0])
    @cache
    def f(i, j):
        return 1 + max([f(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                        if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[i][j]] or [0])
    return max(f(i, j) for i in range(m) for j in range(n))

def brute(matrix):
    """Plain DFS from every cell, no memo."""
    m, n = len(matrix), len(matrix[0])
    def f(i, j):
        return 1 + max([f(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                        if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[i][j]] or [0])
    return max(f(i, j) for i in range(m) for j in range(n))

def lip_sorted_shuffled(matrix):
    """Same as lip_sorted but the order among EQUAL values is random."""
    m, n = len(matrix), len(matrix[0])
    cells = [(i, j) for i in range(m) for j in range(n)]
    random.shuffle(cells)
    cells.sort(key=lambda c: matrix[c[0]][c[1]])               # stable: equal values keep the shuffled order
    L = [[1] * n for _ in range(m)]
    for i, j in cells:
        for di, dj in DIRS:
            a, b = i + di, j + dj
            if 0 <= a < m and 0 <= b < n and matrix[a][b] < matrix[i][j]:
                L[i][j] = max(L[i][j], L[a][b] + 1)
    return max(map(max, L))

# examples
for mat, exp in [([[9, 9, 4], [6, 6, 8], [2, 1, 1]], 4), ([[3, 4, 5], [3, 2, 6], [2, 2, 1]], 4), ([[1]], 1), ([[1, 1], [1, 1]], 1)]:
    a, b, c, d = lip_sorted(mat), lip_kahn(mat), brute(mat), lip_memo(mat)
    assert a == b == c == d == exp, (mat, a, b, c, d)
    print('example', mat, '->', a)

# hand table, example 1
mat = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
m, n = 3, 3
L = [[1] * n for _ in range(m)]
print('process cells in increasing value; L = longest path ending at the cell')
for v, i, j in sorted((mat[i][j], i, j) for i in range(m) for j in range(n)):
    for di, dj in DIRS:
        a, b = i + di, j + dj
        if 0 <= a < m and 0 <= b < n and mat[a][b] < v:
            L[i][j] = max(L[i][j], L[a][b] + 1)
    print('  value %d at (%d,%d): L = %d' % (v, i, j, L[i][j]))
print('final L:')
for row in L: print('  ', row)

# seeded cross-check, m, n <= 3
cases = 0
for _ in range(600):
    m, n = random.randint(1, 3), random.randint(1, 3)
    hi = random.choice([1, 2, 4, 9])
    mat = [[random.randint(0, hi) for _ in range(n)] for _ in range(m)]
    assert lip_sorted(mat) == lip_kahn(mat) == brute(mat) == lip_memo(mat), mat
    cases += 1
print('cross-check cases', cases)
# exhaustive: all 3 x 3 matrices with values 0..2 (19683), and equal-value order shuffled
cnt = 0
for vals in itertools.product(range(3), repeat=9):
    mat = [list(vals[:3]), list(vals[3:6]), list(vals[6:])]
    exp = brute(mat)
    assert lip_sorted(mat) == lip_kahn(mat) == exp
    if cnt % 7 == 0:
        assert all(lip_sorted_shuffled(mat) == exp for _ in range(3))
    cnt += 1
print('exhaustive 3 x 3 matrices with values 0..2:', cnt, '(equal-value order shuffled on every 7th)')

# edge cases
assert lip_sorted([[5]]) == 1 and lip_sorted([[1, 2, 3, 4]]) == 4 and lip_sorted([[4], [3], [2], [1]]) == 4
assert lip_sorted([[7, 7, 7]]) == 1 and lip_sorted([[0, 10**9]]) == 2

# winding corridor: rows 0, 2, 4, ... hold increasing values along a snake; walls (value 0) between; one connector per wall row
def corridor(n):
    mat = [[0] * n for _ in range(n)]; v = 1
    for i in range(0, n, 2):
        cols = range(n) if (i // 2) % 2 == 0 else range(n - 1, -1, -1)
        for j in cols:
            mat[i][j] = v; v += 1
        if i + 1 < n:
            mat[i + 1][n - 1 if (i // 2) % 2 == 0 else 0] = v; v += 1
    return mat, v - 1
print('recursion limit', sys.getrecursionlimit())
for size in (21, 61):
    mat, cells = corridor(size)
    try:
        r = lip_memo(mat); res = 'memoised DFS ok (%d)' % r
    except RecursionError:
        res = 'memoised DFS RecursionError'
    print('corridor %d x %d: path has %d cells (plus the 0 wall cell next to its start = %d); sorted DP %d, Kahn %d; %s'
          % (size, size, cells, cells + 1, lip_sorted(mat), lip_kahn(mat), res))
mat, cells = corridor(199)
t0 = time.perf_counter(); r = lip_sorted(mat); t1 = time.perf_counter(); r2 = lip_kahn(mat); t2 = time.perf_counter()
print('corridor 199 x 199 (the largest odd size within 200): path cells', cells, '-> sorted DP', r, ', Kahn', r2, '(sandbox timing %.2f s, %.2f s)' % (t1 - t0, t2 - t1))
assert r == r2 == cells + 1
big = [[random.randint(0, 10**9) for _ in range(200)] for _ in range(200)]
assert lip_sorted(big) == lip_kahn(big)
print('200 x 200 random:', lip_sorted(big))
print('edge asserts passed')
```

**Output (my run):**
```
example [[9, 9, 4], [6, 6, 8], [2, 1, 1]] -> 4
example [[3, 4, 5], [3, 2, 6], [2, 2, 1]] -> 4
example [[1]] -> 1
example [[1, 1], [1, 1]] -> 1
process cells in increasing value; L = longest path ending at the cell
  value 1 at (2,1): L = 1
  value 1 at (2,2): L = 1
  value 2 at (2,0): L = 2
  value 4 at (0,2): L = 1
  value 6 at (1,0): L = 3
  value 6 at (1,1): L = 2
  value 8 at (1,2): L = 3
  value 9 at (0,0): L = 4
  value 9 at (0,1): L = 3
final L:
   [4, 3, 1]
   [3, 2, 3]
   [2, 1, 1]
cross-check cases 600
exhaustive 3 x 3 matrices with values 0..2: 19683 (equal-value order shuffled on every 7th)
recursion limit 1000
corridor 21 x 21: path has 241 cells (plus the 0 wall cell next to its start = 242); sorted DP 242, Kahn 242; memoised DFS ok (242)
corridor 61 x 61: path has 1921 cells (plus the 0 wall cell next to its start = 1922); sorted DP 1922, Kahn 1922; memoised DFS RecursionError
corridor 199 x 199 (the largest odd size within 200): path cells 19999 -> sorted DP 20000 , Kahn 20000 (sandbox timing 0.03 s, 0.06 s)
200 x 200 random: 12
edge asserts passed
```

Reading the output:
- All four examples match the sorted-order DP, Kahn, the memoised DFS and the plain DFS. The processing table printed is the one in the dry run, and equals the printed final `L`.
- 600 seeded random matrices (m, n <= 3, values in 0..1, 0..2, 0..4 or 0..9) agree across all four methods. The exhaustive run covers all 19,683 3 x 3 matrices with values 0..2, which is where ties and plateaus occur most.
- Corridor: the 21 x 21 case runs everywhere; the 61 x 61 corridor breaks only the memoised DFS. The path length reported by both bottom-up methods is `corridor cells + 1`, not `corridor cells`: the corridor starts at value 1 and a wall cell of value 0 sits beside the start, so the longest path begins one cell earlier at the wall (found while testing).
- 200 x 200 of random values up to 10^9 gives an answer of 12 (random matrices have short paths); the corridor is the adversarial input.

**Edge cases:**
- 1 x 1: 1. All equal: 1 (strict `<`, never `<=`).
- One row or column, strictly increasing: its length.
- Values up to `10^9`: no problem for Python ints; compare directly, no arithmetic on them.
- Equal neighbours are not edges; two equal cells never extend each other.
- Single-row increasing 4 cells: 4; reversed order: still 4 (the path may go leftwards).

**Follow-ups:**
- "Return the path itself?" Keep a parent per cell (the neighbour that gave the max), walk back from the cell with the best `L`. Ties: state a rule.
- "Why not DFS with `@cache`?" Correct but its recursion depth equals the path length; use `sys.setrecursionlimit` only as a last resort (version and call-path dependent, and a thread stack size problem), or go bottom-up.
- "What if the move were non-strict (`>=`)?" Then equal cells form cycles and it is no longer a DAG.

**Common mistakes:**
- Using `<=`/`>=`, which allows plateaus and breaks the DAG.
- Sorting by value but processing equal values as if one must come first (unnecessary) or reading a neighbour that is not yet final (only possible if you forget the strict test).
- Memoising on the matrix with a list key (`@cache` on a function taking the matrix, unhashable).
- Starting with `best = 0` for an empty path count when the matrix is 1 x 1 and returning 0.
- Assuming a snake matrix always breaks recursion: it depends on the DFS order; a corridor with walls is the reliable adversary.

### Q25 ⭐ 🟢 Minimum falling path sum. `matrix` is an n x n list of lists (1 <= n <= 100) of integers in -100..100. Start in any cell of the first row; from (r, c) move to (r+1, c-1), (r+1, c) or (r+1, c+1) (staying inside the matrix). Return the smallest sum over all paths that reach the last row. Give the state, the edge handling at columns 0 and n-1, and the one-row version. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (n <= 5) on small inputs. Example: matrix=[[2, 1, 3], [6, 5, 4], [7, 8, 9]] -> 13; matrix=[[-19, 57], [-40, -5]] -> -59; matrix=[[5]] -> 5.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP, one row at a time, with three predecessors instead of two (up-left, up, up-right). Start anywhere in the top row, end anywhere in the bottom row.

**Say this first (1 line):** "`dp[c]` is the cheapest sum of a falling path that ends at column `c` of the current row. The next row reads the three nearest columns of the previous row, clipped at the edges, so one array is enough."

**Brute force:** Plain recursion `f(r, c)`: cell value plus the best of up to three cells below; the answer is the best `f(0, c)`. Without a memo it is up to 3^(n-1) paths per start. It is the oracle for n <= 5.

**Optimal:**
- State: `dp[r][c]` = smallest sum over falling paths from any cell of row 0 to `(r, c)`.
- Transition: `dp[r][c] = matrix[r][c] + min(dp[r-1][c-1], dp[r-1][c], dp[r-1][c+1])`, using only the columns that exist.
- Edge handling: at column 0 there is no `c-1`; at column `n-1` there is no `c+1`. In Python the slice `dp[max(0, c-1):c+2]` clips on its own (the right end is clipped by slicing, the left end needs the `max(0, ...)`). Writing `dp[c-1]` for `c = 0` does not raise: it silently reads the LAST column, which is not a legal move (the code shows this bug is wrong on 118 of 600 random matrices).
- Base: row 0, `dp[c] = matrix[0][c]` (any start is allowed, which is why the base is the whole row and not one cell).
- Answer: `min(dp)` after the last row (any end is allowed).
- One row: build the new row from the old one with a list comprehension, so there is no in-place overwrite problem (an in-place update would overwrite `dp[c-1]` before column `c` reads it).

**Complexity:** Time O(n^2) (n^2 cells, 3 reads each), space O(n) for one row. For n = 100 that is 10,000 cells.

**Dry run:** `[[2,1,3],[6,5,4],[7,8,9]]`.
- Row 0: `dp = [2, 1, 3]`.
- Row 1: `c=0`: `6 + min(2, 1) = 7`; `c=1`: `5 + min(2, 1, 3) = 6`; `c=2`: `4 + min(1, 3) = 5`. `dp = [7, 6, 5]`.
- Row 2: `c=0`: `7 + min(7, 6) = 13`; `c=1`: `8 + min(7, 6, 5) = 13`; `c=2`: `9 + min(6, 5) = 14`. `dp = [13, 13, 14]`.
- Answer `min(dp) = 13`: the path `1, 5, 7` (columns 1, 1, 0; each step moves to the same column or one column left or right).

**Code:**
```python
import random, itertools, sys

random.seed(25)

def falling(matrix):
    """One row. dp[c] = cheapest path sum ending at column c of the current row."""
    n = len(matrix)
    dp = list(matrix[0])                                      # base: row 0, any start
    for r in range(1, n):
        dp = [matrix[r][c] + min(dp[max(0, c - 1):c + 2])     # columns c-1, c, c+1, clipped at the edges by the slice
              for c in range(n)]
    return min(dp)                                            # end anywhere in the last row

def falling_explicit(matrix):
    """Same, with the edge handling written out (no slicing trick)."""
    n = len(matrix)
    dp = matrix[0][:]
    for r in range(1, n):
        new = []
        for c in range(n):
            best = dp[c]
            if c > 0: best = min(best, dp[c - 1])
            if c < n - 1: best = min(best, dp[c + 1])
            new.append(matrix[r][c] + best)
        dp = new
    return min(dp)

def brute(matrix):
    """Plain recursion, no memo."""
    n = len(matrix)
    def f(r, c):
        if r == n - 1: return matrix[r][c]
        return matrix[r][c] + min(f(r + 1, k) for k in (c - 1, c, c + 1) if 0 <= k < n)
    return min(f(0, c) for c in range(n))

def wrong_wraparound(matrix):
    """Bug: dp[c-1] at c = 0 is dp[-1], the LAST column, which is not a legal move."""
    n = len(matrix); dp = matrix[0][:]
    for r in range(1, n):
        dp = [matrix[r][c] + min(dp[c - 1], dp[c], dp[(c + 1) % n]) for c in range(n)]
    return min(dp)

def wrong_greedy(matrix):
    """Bug: start at the smallest top cell and keep stepping to the smallest reachable cell."""
    n = len(matrix); c = matrix[0].index(min(matrix[0])); tot = matrix[0][c]
    for r in range(1, n):
        c = min((k for k in (c - 1, c, c + 1) if 0 <= k < n), key=lambda k: matrix[r][k]); tot += matrix[r][c]
    return tot

# examples
for mat, exp in [([[2, 1, 3], [6, 5, 4], [7, 8, 9]], 13), ([[-19, 57], [-40, -5]], -59), ([[5]], 5)]:
    a, b, c = falling(mat), falling_explicit(mat), brute(mat)
    assert a == b == c == exp, (mat, a, b, c)
    print('example', mat, '->', a)

# hand table
mat = [[2, 1, 3], [6, 5, 4], [7, 8, 9]]
dp = mat[0][:]
print('row 0: dp =', dp)
for r in range(1, 3):
    print('row %d:' % r, end=' ')
    new = []
    for c in range(3):
        cand = [dp[k] for k in (c - 1, c, c + 1) if 0 <= k < 3]
        new.append(mat[r][c] + min(cand)); print('c=%d: %d + min%s = %d;' % (c, mat[r][c], cand, new[-1]), end=' ')
    dp = new; print('-> dp =', dp)
print('answer min(dp) =', min(dp))

# seeded cross-check, n <= 5
cases = 0; wa = gr = 0
for _ in range(600):
    n = random.randint(1, 5)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    exp = brute(mat)
    assert falling(mat) == falling_explicit(mat) == exp, mat
    wa += wrong_wraparound(mat) != exp; gr += wrong_greedy(mat) != exp
    cases += 1
print('cross-check cases', cases, '| wrap-around bug wrong on', wa, '| greedy wrong on', gr)

# edge cases
assert falling([[5]]) == 5 and falling([[-100] * 100 for _ in range(100)]) == -10000
assert falling([[100] * 100 for _ in range(100)]) == 10000
big = [[random.randint(-100, 100) for _ in range(100)] for _ in range(100)]
assert falling(big) == falling_explicit(big)
print('100 x 100 random:', falling(big))
print('recursion limit', sys.getrecursionlimit(), '| a memoised recursion here nests n = 100 frames, far below it')
print('edge asserts passed')
```

**Output (my run):**
```
example [[2, 1, 3], [6, 5, 4], [7, 8, 9]] -> 13
example [[-19, 57], [-40, -5]] -> -59
example [[5]] -> 5
row 0: dp = [2, 1, 3]
row 1: c=0: 6 + min[2, 1] = 7; c=1: 5 + min[2, 1, 3] = 6; c=2: 4 + min[1, 3] = 5; -> dp = [7, 6, 5]
row 2: c=0: 7 + min[7, 6] = 13; c=1: 8 + min[7, 6, 5] = 13; c=2: 9 + min[6, 5] = 14; -> dp = [13, 13, 14]
answer min(dp) = 13
cross-check cases 600 | wrap-around bug wrong on 118 | greedy wrong on 100
100 x 100 random: -6532
recursion limit 1000 | a memoised recursion here nests n = 100 frames, far below it
edge asserts passed
```

Reading the output:
- All three examples match the slice version, the explicit-edge version and the plain recursion. The hand table printed is the dry run.
- 600 seeded random matrices (n <= 5, values -9..9) agree. The same loop shows two tempting bugs are real: the wrap-around index bug is wrong on 118 of the 600 and a greedy "step to the smallest reachable cell" is wrong on 100.
- The 100 x 100 case runs instantly (sandbox, not a proof of big-O). The recursion limit is 1000 and a memoised top-down recursion here is only `n = 100` frames deep, so it would also work; bottom-up is simply shorter.

**Edge cases:**
- `n = 1`: the single value (the slice has one element).
- Negative values: the answer can be negative; do not initialise a `best` with 0.
- All values equal: `n` times the value.
- Edge columns: the clip, not wrap-around.

**Follow-ups:**
- "Print the path?" Keep the full table (or parent column per cell) and walk back from the best last-row cell. State a tie rule.
- "Allow k columns of jump (not just +-1)?" Then each cell needs a sliding-window minimum of the previous row (monotonic deque) to stay O(n^2).
- "Falling path with non-zero start constraint?" Change only the base row.

**Common mistakes:**
- Negative index wrap-around at column 0 (silent, wrong).
- `IndexError` at column `n-1` from `dp[c+1]`.
- Starting from `dp[0][0]` only, or ending at the bottom-right only.
- Greedy "pick the smallest neighbour".
- Updating one list in place so column `c` reads an already overwritten `dp[c-1]`.

### Q26 ⭐ 🟡 Longest repeating subsequence. `s` is a lowercase string with 0 <= len <= 1000. Find two index sequences p and q (each strictly increasing, same length L) such that s[p[0]] s[p[1]] ... equals s[q[0]] s[q[1]] ... and p[k] != q[k] for EVERY k (the two sequences may share an index, but never at the same position k); return the largest L (0 for len < 2). Reduce it to LCS of `s` with itself and say which single condition removes the trivial answer len(s): the two matched positions must differ (i != j). Give the transition and two rows. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every pair of index sequences (len <= 7) on small inputs. Example: s='aabebcdd' -> 3; s='abc' -> 0; s='aaa' -> 2; s='' -> 0; s='axxxy' -> 2.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP (LCS) applied to one string against itself, with one extra condition on the match.

**Say this first (1 line):** "It is LCS of `s` with `s`, but a match `s[i] == s[j]` only counts when `i != j`. Without that condition every position matches itself and the answer is just `len(s)`."

**Brute force:** Enumerate pairs of strictly increasing index sequences `p` and `q` of the same length `L`, from the largest `L` down, and accept when the letters spell the same word and `p[k] != q[k]` for every `k`. About `C(n, L)^2` pairs per length, so only for `len(s) <= 7` here. It is the oracle.

**Optimal:**
- Why LCS fits: choosing two increasing index sequences `p` and `q` that spell the same word is exactly an alignment of `s` against `s`; each pair `(p[k], q[k])` is a matched pair `(i, j)`. The stated condition `p[k] != q[k]` is exactly `i != j` for every matched pair. The two sequences may share an index at different positions `k` (one position can be `p[0]` and `q[1]`), and the table allows that.
- State: `dp[i][j]` = longest valid common subsequence of `s[:i]` and `s[:j]`.
- Transition: if `s[i-1] == s[j-1]` and `i != j` then `dp[i][j] = dp[i-1][j-1] + 1`, else `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
- Base: `dp[0][j] = dp[i][0] = 0`. Answer `dp[n][n]`. For `len(s) < 2` it is 0 automatically.
- The single condition that removes the trivial answer: `i != j`. Without it the diagonal matches every letter with itself and `dp[n][n] = n` for every string (checked below on 30 random strings, lengths 0 to 29).
- Two rows: `dp[i]` needs `dp[i-1][j-1]`, `dp[i-1][j]` (previous row) and `dp[i][j-1]` (this row), so keep `prev` and `cur`.
- Note on the statement: the pairs may share an index at different positions. A different (and also common) reading requires the two index SETS to be disjoint. That reading gives 1 for `'aaa'` while the stated one gives 2, and the two readings differ on 125 of 300 random binary strings (printed below). Use the stated `p[k] != q[k]` rule with the `i != j` condition.

**Complexity:** Time O(n^2) (1,000,000 cell updates for n = 1000), space O(n) with two rows, O(n^2) with the full table.

**Dry run:** `s = 'aabebcdd'` (positions 1..8: a a b e b c d d). The printed table has rows `i` and columns `j`, both over `s`.
- Row 1 (`a`): matches `a` at `j = 2` (letters equal, `i != j`), so from `j = 2` on the row is 1. `j = 1` is the same cell as `i = 1`, not allowed.
- Row 2 (`a`): `j = 1` matches (`dp[1][0] + 1 = 1`), then it stays 1.
- Row 3 (`b`): `j = 5` is the other `b` (`dp[2][4] + 1 = 2`). Row 5 (`b`): `j = 3` gives 2.
- Rows 7 and 8 (`d`, `d`): `dp[7][8] = dp[6][7] + 1 = 3` (the `ab` from earlier is extended by the pair of `d`s), so `dp[8][8] = 3`.
- Answer 3: the word `abd` taken at positions 1, 3, 7 and 2, 5, 8; each pair of indices differs (1 vs 2, 3 vs 5, 7 vs 8).

**Code:**
```python
import random, itertools, sys
from functools import lru_cache

random.seed(26)

def lrs(s):
    """LCS of s with itself where two positions may only match if i != j. Two rows."""
    n = len(s)
    prev = [0] * (n + 1)                                      # row i-1
    for i in range(1, n + 1):
        cur = [0] * (n + 1)                                   # row i, cur[0] = 0
        for j in range(1, n + 1):
            if s[i - 1] == s[j - 1] and i != j:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]

def lrs_table(s):
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if s[i - 1] == s[j - 1] and i != j else max(dp[i - 1][j], dp[i][j - 1])
    return dp

def lcs_no_condition(s):
    """Without i != j: LCS(s, s) = len(s), the trivial answer."""
    n = len(s); prev = [0] * (n + 1)
    for i in range(1, n + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if s[i - 1] == s[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]

def brute(s):
    """All pairs of strictly increasing index sequences P, Q of equal length L with s[P] == s[Q] and P[k] != Q[k] for every k."""
    n = len(s)
    for L in range(n, 0, -1):
        for P in itertools.combinations(range(n), L):
            word = [s[i] for i in P]
            for Q in itertools.combinations(range(n), L):
                if all(a != b for a, b in zip(P, Q)) and [s[i] for i in Q] == word:
                    return L
    return 0

def brute_disjoint(s):
    """The OTHER reading (index sets must be disjoint), for comparison only."""
    n = len(s)
    for L in range(n // 2, 0, -1):
        for P in itertools.combinations(range(n), L):
            word = [s[i] for i in P]
            rest = [i for i in range(n) if i not in P]
            for Q in itertools.combinations(rest, L):
                if [s[i] for i in Q] == word:
                    return L
    return 0

def memo(s):
    n = len(s)
    @lru_cache(maxsize=None)
    def f(i, j):                                              # suffix form: s[i:], s[j:]
        if i == n or j == n: return 0
        if s[i] == s[j] and i != j: return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

# examples
for s, exp in [('aabebcdd', 3), ('abc', 0), ('aaa', 2), ('', 0), ('axxxy', 2)]:
    a, b, c, d = lrs(s), lrs_table(s)[-1][-1], brute(s), memo(s)
    assert a == b == c == d == exp, (s, a, b, c, d)
    print('example', repr(s), '->', a, '| without the i != j condition:', lcs_no_condition(s))

# hand table for 'aabebcdd' (row i = letter s[i-1], column j = letter s[j-1])
s = 'aabebcdd'
dp = lrs_table(s)
print('dp table for', s, '(rows i, columns j; match only if letters equal and i != j):')
print('      ' + '  '.join(['-'] + list(s)))
for i, row in enumerate(dp):
    print('  %s ' % ('-' if i == 0 else s[i - 1]), row)
print('answer dp[8][8] =', dp[-1][-1], '-> the repeated subsequence abd: positions 1,3,7 and 2,5,8 (1-indexed)')

# seeded cross-check, len <= 7
cases = nz = 0
for _ in range(500):
    alpha = random.choice(['a', 'ab', 'abc'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(0, 7)))
    exp = brute(s)
    assert lrs(s) == lrs_table(s)[-1][-1] == memo(s) == exp, s
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a non-zero answer', nz)
cnt = 0
for L in range(0, 9):
    for bits in range(1 << L):
        s = format(bits, '0%db' % L) if L else ''
        if L <= 7:
            assert lrs(s) == brute(s)
        else:
            assert lrs(s) == lrs_table(s)[-1][-1] == memo(s)
        cnt += 1
print('exhaustive binary strings len 0..8 checked:', cnt)

# the condition matters: without it the answer is len(s) on every string; and the 'disjoint index sets' reading is a different problem
assert all(lcs_no_condition(''.join(random.choice('abc') for _ in range(L))) == L for L in range(0, 30))
diff = sum(brute(s) != brute_disjoint(s) for s in (''.join(random.choice('ab') for _ in range(random.randint(0, 7))) for _ in range(300)))
print("'aaa': stated definition", brute('aaa'), "| disjoint-index reading", brute_disjoint('aaa'), '| the two readings differ on', diff, 'of 300 random strings')

# edge cases and max size
assert lrs('a') == 0 and lrs('aa') == 1 and lrs('ab') == 0 and lrs('a' * 1000) == 999
big = ''.join(random.choice('ab') for _ in range(1000))
print('n = 1000 random binary string:', lrs(big))
per = lrs('abc' * 300)
assert per >= 897                      # s[3:] against s[:-3] is a valid pair (shift by 3), so at least n - 3
print("'abc' * 300 (n = 900):", per)
print('edge asserts passed')

# recursion limit (observed): the memoised suffix recursion nests up to about 2n frames
print('recursion limit', sys.getrecursionlimit())
for n in (200, 1000):
    w = 'a' * n
    try:
        print('memoised n = %d ->' % n, memo(w) == lrs(w), '(bottom-up gives', lrs(w), ')')
    except RecursionError:
        print('memoised n = %d -> RecursionError (bottom-up gives %d)' % (n, lrs(w)))
```

**Output (my run):**
```
example 'aabebcdd' -> 3 | without the i != j condition: 8
example 'abc' -> 0 | without the i != j condition: 3
example 'aaa' -> 2 | without the i != j condition: 3
example '' -> 0 | without the i != j condition: 0
example 'axxxy' -> 2 | without the i != j condition: 5
dp table for aabebcdd (rows i, columns j; match only if letters equal and i != j):
      -  a  a  b  e  b  c  d  d
  -  [0, 0, 0, 0, 0, 0, 0, 0, 0]
  a  [0, 0, 1, 1, 1, 1, 1, 1, 1]
  a  [0, 1, 1, 1, 1, 1, 1, 1, 1]
  b  [0, 1, 1, 1, 1, 2, 2, 2, 2]
  e  [0, 1, 1, 1, 1, 2, 2, 2, 2]
  b  [0, 1, 1, 2, 2, 2, 2, 2, 2]
  c  [0, 1, 1, 2, 2, 2, 2, 2, 2]
  d  [0, 1, 1, 2, 2, 2, 2, 2, 3]
  d  [0, 1, 1, 2, 2, 2, 2, 3, 3]
answer dp[8][8] = 3 -> the repeated subsequence abd: positions 1,3,7 and 2,5,8 (1-indexed)
cross-check cases 500 | with a non-zero answer 345
exhaustive binary strings len 0..8 checked: 511
'aaa': stated definition 2 | disjoint-index reading 1 | the two readings differ on 125 of 300 random strings
n = 1000 random binary string: 804
'abc' * 300 (n = 900): 897
edge asserts passed
recursion limit 1000
memoised n = 200 -> True (bottom-up gives 199 )
memoised n = 1000 -> RecursionError (bottom-up gives 999)
```

Reading the output:
- All five examples match the two-row DP, the table, the memoised recursion and the pair-of-sequences enumeration. The extra column on the example lines shows what you would get without the `i != j` test: always `len(s)` (5 for `'axxxy'`).
- 500 seeded random strings (len <= 7, alphabets of 1 to 3 letters; 345 with a non-zero answer) and all 511 binary strings of length 0 to 8 agree.
- The disjoint-index reading differs from the stated definition on `'aaa'` (1 versus 2) and on 125 of 300 random binary strings, so the stated rule matters.
- Recursion: a memoised version works on 200 equal letters but raises `RecursionError` at 1000 (default limit 1000, observation on Python 3.13), because the suffix recursion can nest about `2n` frames; the bottom-up version handles n = 1000 directly.

**Edge cases:**
- `''` and one letter: 0.
- All letters equal, length n: `n - 1` (shift by one).
- All distinct letters: 0.
- Two equal letters (`'aa'`): 1.
- `n = 1000`: a million cells; fine in two rows.

**Follow-ups:**
- "Why not require disjoint index sets?" That is a different problem (it is harder to state as a table and gives different answers, as the `'aaa'` case shows).
- "Return the subsequence?" Use the full table and walk back from `(n, n)`: on a match step diagonally and prepend the letter; otherwise step to the larger neighbour. State a tie rule.
- "Relation to LPS?" Longest palindromic subsequence is LCS of `s` with its REVERSE (Q7); here it is LCS of `s` with itself plus a condition.

**Common mistakes:**
- Forgetting `i != j` (answer `n`).
- Off-by-one between 0-indexed letters and the 1-indexed table: compare `s[i-1] == s[j-1]` together with `i != j` (do not write `s[i] == s[j]` against a table indexed from 1).
- Memoised recursion at n = 1000 (`RecursionError`).

### Q27 ⭐ 🟡 Paths whose sum is divisible by k, with a modulus. `grid` is an m x n list of lists (1 <= m, n <= 70) of integers in 0..100 and `k` is an integer with 1 <= k <= 50. Moves are right or down from the top-left to the bottom-right. Return the number of paths whose cell sum (both ends included) is divisible by k, modulo 10^9 + 7. State `dp[i][j][r]` = paths to (i, j) whose sum has remainder r, give the transition `(r + grid[i][j]) % k`, the base case and the time O(m*n*k); say why taking the modulus at every addition is safe for a counting DP, and why the remainder is tracked mod k and not the full sum. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) on small inputs. Example: grid=[[5, 2, 4], [3, 0, 5], [0, 7, 2]], k=3 -> 2; grid=[[0, 0]], k=5 -> 1; grid=[[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]], k=1 -> 10; grid=[[1, 1], [1, 1]], k=2 -> 0.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP with an extra dimension: the state carries the remainder of the sum modulo `k`. A counting DP, so the transitions add; and a modulus on the counts.

**Say this first (1 line):** "`dp[i][j][r]` is the number of paths to `(i, j)` whose sum is `r` mod `k`. Each cell shifts the remainder by `grid[i][j] % k`. The answer is `dp[m-1][n-1][0]`. I only need the remainder because divisibility by `k` depends on the sum mod `k` alone, and I reduce the counts mod 10^9 + 7 after each addition."

**Brute force:** Enumerate all `C(m+n-2, m-1)` right/down paths, add up the cells, count the sums divisible by `k`, reduce modulo 10^9 + 7. Exponential; the oracle for m, n <= 5.

**Optimal:**
- State: `dp[i][j][r]` = number of right/down paths from `(0, 0)` to `(i, j)` (both ends included) with `sum % k == r`.
- Transition: arriving at `(i, j)` from above or from the left with remainder `r` there gives remainder `(r + grid[i][j]) % k` here. So `dp[i][j][(r + v) % k] += dp[i-1][j][r] + dp[i][j-1][r]` with `v = grid[i][j] % k`. Nothing is overwritten from the same cell: each target remainder collects from different `r`, and the shift `r -> (r + v) % k` is a permutation.
- Base: `dp[0][0][grid[0][0] % k] = 1`, everything else 0 (not `dp[0][0][0]`; the start cell's value already counts).
- Answer: `dp[m-1][n-1][0]`.
- Why the remainder and not the full sum: `(a + b) % k` depends only on `a % k` and `b % k`, and the question asks only about divisibility. The full sum can be as large as 100 * 139 = 13,900 for a 70 x 70 grid, so about 13,901 values per cell instead of at most 50, a state space about 280 times larger for no benefit.
- Why the modulus is safe at every addition: a path count only ever gets additions of non-negative counts, with no subtraction, comparison or division of counts. And `(a + b) % M = ((a % M) + (b % M)) % M`, so reducing early gives the same final residue as reducing at the end. The code checks this on a 40 x 40 grid with `k = 7`: the exact count has 22 digits, and the version that reduces at every step equals `exact % MOD`. (A 70 x 70 all-zero grid has C(138, 69) paths, 41 digits, also checked.) The `% k` for remainders and `% (10**9 + 7)` for counts are two different moduli; do not mix them.
- Rolling rows: row `i` needs only row `i-1` and the cell to its left, so keep one list of `n` vectors of length `k`: O(n * k) space. The code does this; a 3D version is printed for the walk-through and cross-check.

**Complexity:** Time O(m * n * k) (at most 70 * 70 * 50 = 245,000 states, two transitions each), space O(n * k) with rolling rows (O(m * n * k) for the full 3D table).

**Dry run:** grid `[[5,2,4],[3,0,5],[0,7,2]]`, `k = 3`. Each cell is a vector `[r=0, r=1, r=2]`.
- `(0,0)`: value 5, `5 % 3 = 2`, so `[0, 0, 1]`.
- Row 0: `(0,1)` value 2: remainder `(2 + 2) % 3 = 1`, `[0, 1, 0]`; `(0,2)` value 4 (`1`): `(1 + 1) % 3 = 2`, `[0, 0, 1]`.
- Column 0: `(1,0)` value 3 (`0`): `[0, 0, 1]`; `(2,0)` value 0: `[0, 0, 1]`.
- `(1,1)` value 0: above `[0, 1, 0]` and left `[0, 0, 1]` add up to `[0, 1, 1]`.
- `(1,2)` value 5 (`2`): above `[0, 0, 1]` shifts by 2 to `[0, 1, 0]`; left `[0, 1, 1]` shifts to `[1, 1, 0]` (remainder 1 goes to 0, remainder 2 goes to 1). Sum `[1, 2, 0]`.
- `(2,1)` value 7 (`1`): above `[0, 1, 1]` shifts by 1 to `[1, 0, 1]`; left `[0, 0, 1]` shifts to `[1, 0, 0]`. Sum `[2, 0, 1]`.
- `(2,2)` value 2 (`2`): above `[1, 2, 0]` shifts by 2 to `[2, 0, 1]`; left `[2, 0, 1]` shifts to `[0, 1, 2]`. Sum `[2, 1, 3]`; its remainder-0 entry is 2.
- Answer 2.

**Code:**
```python
import random, itertools, sys, time
from math import comb

random.seed(27)
MOD = 10**9 + 7

def count_paths(grid, k, mod=MOD):
    """dp[j][r] = number of paths to (current row, j) whose sum has remainder r mod k. One row of k-vectors."""
    m, n = len(grid), len(grid[0])
    dp = [[0] * k for _ in range(n)]
    for i in range(m):
        new = [[0] * k for _ in range(n)]
        for j in range(n):
            v = grid[i][j] % k
            if i == 0 and j == 0:
                new[0][v] = 1                                   # base: the start cell alone, sum % k = grid[0][0] % k
                continue
            cell = new[j]
            for src in ((dp[j] if i else None), (new[j - 1] if j else None)):   # from above, from the left
                if src is None:
                    continue
                for r in range(k):
                    c = src[r]
                    if c:
                        t = (r + v) % k
                        cell[t] = (cell[t] + c) % mod if mod else cell[t] + c
        dp = new
    return dp[n - 1][0]

def count_paths_full(grid, k, mod=MOD):
    """3D table dp[i][j][r], the version in the statement (used for the printed walk-through)."""
    m, n = len(grid), len(grid[0])
    dp = [[[0] * k for _ in range(n)] for _ in range(m)]
    dp[0][0][grid[0][0] % k] = 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            v = grid[i][j] % k
            for r in range(k):
                tot = (dp[i - 1][j][r] if i else 0) + (dp[i][j - 1][r] if j else 0)
                if tot:
                    dp[i][j][(r + v) % k] = (dp[i][j][(r + v) % k] + tot) % mod if mod else dp[i][j][(r + v) % k] + tot
    return dp

def brute(grid, k):
    m, n = len(grid), len(grid[0]); cnt = 0
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        i = j = 0; tot = grid[0][0]
        for c in s:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]
        cnt += tot % k == 0
    return cnt % MOD

# examples
for grid, k, exp in [([[5, 2, 4], [3, 0, 5], [0, 7, 2]], 3, 2), ([[0, 0]], 5, 1),
                     ([[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]], 1, 10), ([[1, 1], [1, 1]], 2, 0)]:
    a, b, c = count_paths(grid, k), brute(grid, k), count_paths_full(grid, k)[-1][-1][0]
    assert a == b == c == exp, (grid, k, a, b, c)
    print('example', grid, 'k =', k, '->', a)

# hand table for example 1
grid, k = [[5, 2, 4], [3, 0, 5], [0, 7, 2]], 3
dp = count_paths_full(grid, k)
print('dp[i][j] = [paths with remainder 0, 1, 2] for grid', grid, 'k =', k)
for i in range(3):
    print('  ', [dp[i][j] for j in range(3)])
print('answer = dp[2][2][0] =', dp[2][2][0])

# seeded cross-check, m, n <= 5
cases = nz = 0
for _ in range(500):
    m, n = random.randint(1, 5), random.randint(1, 5)
    k = random.randint(1, 6)
    grid = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
    exp = brute(grid, k)
    assert count_paths(grid, k) == count_paths_full(grid, k)[-1][-1][0] == exp, (grid, k)
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a non-zero count', nz)

# the modulus: counts beyond 10^9+7 occur, and reducing after each addition equals reducing at the end (exact big-int run)
g = [[random.randint(0, 100) for _ in range(40)] for _ in range(40)]
exact = count_paths(g, 7, mod=None)
print('40 x 40, k = 7: exact count has', len(str(exact)), 'digits; mod result', count_paths(g, 7), '== exact % MOD:', count_paths(g, 7) == exact % MOD)
assert count_paths(g, 7) == exact % MOD and exact > MOD
ones = [[0] * 70 for _ in range(70)]
assert count_paths(ones, 1, mod=None) == comb(138, 69) and count_paths(ones, 1) == comb(138, 69) % MOD
print('70 x 70 all zeros, k = 1: all C(138, 69) paths:', comb(138, 69) % MOD, '(exact value has', len(str(comb(138, 69))), 'digits)')

# why remainder and not the full sum: the number of distinct sums is far larger than k
print('largest possible path sum at 70 x 70, cells <= 100:', 100 * (70 + 70 - 1), '-> up to', 100 * 139 + 1, 'sum values per cell versus k <= 50 remainders')

# edge cases and the maximum size
assert count_paths([[5]], 5) == 1 and count_paths([[5]], 3) == 0 and count_paths([[0]], 1) == 1
assert count_paths([[3, 4]], 7) == 1 and count_paths([[3, 4]], 5) == 0
big = [[random.randint(0, 100) for _ in range(70)] for _ in range(70)]
t0 = time.perf_counter(); r = count_paths(big, 50); t1 = time.perf_counter()
assert r == count_paths_full(big, 50)[-1][-1][0]
print('70 x 70, k = 50:', r, '(sandbox timing %.2f s)' % (t1 - t0))
print('recursion limit', sys.getrecursionlimit(), '| the DP is iterative; a memoised f(i, j, r) would nest m + n - 1 = 139 frames, also fine at this size')
print('edge asserts passed')
```

**Output (my run):**
```
example [[5, 2, 4], [3, 0, 5], [0, 7, 2]] k = 3 -> 2
example [[0, 0]] k = 5 -> 1
example [[7, 3, 4, 9], [2, 3, 6, 2], [2, 3, 7, 0]] k = 1 -> 10
example [[1, 1], [1, 1]] k = 2 -> 0
dp[i][j] = [paths with remainder 0, 1, 2] for grid [[5, 2, 4], [3, 0, 5], [0, 7, 2]] k = 3
   [[0, 0, 1], [0, 1, 0], [0, 0, 1]]
   [[0, 0, 1], [0, 1, 1], [1, 2, 0]]
   [[0, 0, 1], [2, 0, 1], [2, 1, 3]]
answer = dp[2][2][0] = 2
cross-check cases 500 | with a non-zero count 362
40 x 40, k = 7: exact count has 22 digits; mod result 602190882 == exact % MOD: True
70 x 70 all zeros, k = 1: all C(138, 69) paths: 982546699 (exact value has 41 digits)
largest possible path sum at 70 x 70, cells <= 100: 13900 -> up to 13901 sum values per cell versus k <= 50 remainders
70 x 70, k = 50: 282366776 (sandbox timing 0.05 s)
recursion limit 1000 | the DP is iterative; a memoised f(i, j, r) would nest m + n - 1 = 139 frames, also fine at this size
edge asserts passed
```

Reading the output:
- All four examples match the rolling-row DP, the 3D table and the path enumeration. The printed table is the one traced above (each cell lists the counts for remainders 0, 1, 2).
- 500 seeded random cases (m, n <= 5, `k` 1 to 6, values 0..100; 362 with a non-zero answer) agree.
- The modulus check: for a 40 x 40 grid the exact count is a 22-digit number and the reduce-every-step result equals `exact % MOD`; for 70 x 70 zeros the reduced result is C(138, 69) mod 10^9 + 7. So counts above the modulus do occur at the stated sizes, and early reduction is exact.
- 70 x 70 with `k = 50` takes a few hundredths of a second here (sandbox timing). The code is iterative, so no recursion limit applies; a memoised `f(i, j, r)` would nest only `m + n - 1 = 139` frames anyway.

**Edge cases:**
- `k = 1`: every path counts (the answer is the number of paths, reduced).
- A 1 x 1 grid: 1 when `grid[0][0] % k == 0`, else 0.
- Single row or column: 0 or 1.
- Zeros everywhere: all paths count for every `k`.
- Large `k` close to the sums: remainders are just the values themselves; no special case.

**Follow-ups:**
- "Why not track the sum?" The state space grows by a factor of about 280 here and `k` already captures everything the question asks.
- "Return the actual number, not mod?" Python integers are unbounded: drop the modulus (the code's `mod=None` path). The count for 70 x 70 has 41 digits.
- "Moves right, down and diagonal?" Add a third predecessor; the shape is the same.

**Common mistakes:**
- Base `dp[0][0][0] = 1` (forgets the start cell's own value).
- Taking `% k` of the count or `% MOD` of the remainder (mixing the two moduli).
- Updating the remainder dimension in place so a state feeds itself within the same cell.
- Not reducing the counts, which is harmless in Python for correctness but makes numbers huge and slow.
- Skipping the `% k` on the new remainder index (`r + v` can reach `2k - 2`, so the list index runs out or lands on the wrong slot).
