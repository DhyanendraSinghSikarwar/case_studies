# Reference solutions (s_*) and independent brute-force / plain-recursion oracles (b_*) for Book 5 Part 11 (DP II).
import itertools, functools, sys, re, math
from functools import lru_cache
INF = float('inf')
M = 10**9 + 7
sys.setrecursionlimit(1000)

# ================= grids
def s_unique_paths(m, n):
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n): row[j] += row[j - 1]
    return row[-1]
def b_unique_paths(m, n):
    def f(i, j): return 1 if i == m - 1 and j == n - 1 else (f(i + 1, j) if i + 1 < m else 0) + (f(i, j + 1) if j + 1 < n else 0)
    return f(0, 0)
def s_unique_paths_obs(grid):
    m, n = len(grid), len(grid[0]); row = [0] * n
    for i in range(m):
        for j in range(n):
            if grid[i][j]: row[j] = 0
            elif i == 0 and j == 0: row[j] = 1
            elif j: row[j] += row[j - 1]
    return row[-1]
def b_unique_paths_obs(grid):
    m, n = len(grid), len(grid[0])
    def f(i, j):
        if grid[i][j]: return 0
        if i == m - 1 and j == n - 1: return 1
        return (f(i + 1, j) if i + 1 < m else 0) + (f(i, j + 1) if j + 1 < n else 0)
    return f(0, 0)
def s_min_path_sum(grid):
    m, n = len(grid), len(grid[0]); row = [INF] * n; row[0] = 0
    for i in range(m):
        for j in range(n):
            row[j] = min(row[j], row[j - 1] if j else INF) + grid[i][j]
    return row[-1]
def b_min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    def f(i, j):
        if i == m - 1 and j == n - 1: return grid[i][j]
        return grid[i][j] + min(f(i + 1, j) if i + 1 < m else INF, f(i, j + 1) if j + 1 < n else INF)
    return f(0, 0)
def s_triangle(triangle):
    dp = list(triangle[-1])
    for r in range(len(triangle) - 2, -1, -1):
        for j in range(r + 1): dp[j] = triangle[r][j] + min(dp[j], dp[j + 1])
    return dp[0]
def b_triangle(triangle):
    def f(r, j): return triangle[r][j] + (min(f(r + 1, j), f(r + 1, j + 1)) if r + 1 < len(triangle) else 0)
    return f(0, 0)
def s_max_square(matrix):
    n = len(matrix[0]); prev = [0] * (n + 1); best = 0
    for row in matrix:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if row[j - 1] == '1':
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1]); best = max(best, cur[j])
        prev = cur
    return best * best
def b_max_square(matrix):
    m, n = len(matrix), len(matrix[0]); best = 0
    for i in range(m):
        for j in range(n):
            for k in range(1, min(m - i, n - j) + 1):
                if all(matrix[a][b] == '1' for a in range(i, i + k) for b in range(j, j + k)): best = max(best, k)
    return best * best
def s_min_falling_path(matrix):
    n = len(matrix); dp = list(matrix[0])
    for r in range(1, n):
        dp = [matrix[r][j] + min(dp[max(0, j - 1):j + 2]) for j in range(n)]
    return min(dp)
def b_min_falling_path(matrix):
    n = len(matrix)
    def f(r, j):
        if r == n - 1: return matrix[r][j]
        return matrix[r][j] + min(f(r + 1, k) for k in (j - 1, j, j + 1) if 0 <= k < n)
    return min(f(0, j) for j in range(n))
def s_min_path_recon(grid):
    m, n = len(grid), len(grid[0]); f = [[INF] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            f[i][j] = grid[i][j] + (0 if i == m - 1 and j == n - 1 else min(f[i + 1][j], f[i][j + 1]))
    i = j = 0; out = []
    while (i, j) != (m - 1, n - 1):
        if f[i + 1][j] <= f[i][j + 1]: out.append('D'); i += 1      # tie: D before R
        else: out.append('R'); j += 1
    return [f[0][0], ''.join(out)]
def b_min_path_recon(grid):
    m, n = len(grid), len(grid[0]); best = None
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        i = j = 0; tot = grid[0][0]
        for c in s:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]
        cand = (tot, ''.join(s))
        if best is None or cand < best: best = cand
    return list(best)
def s_count_min_paths(grid):
    m, n = len(grid), len(grid[0]); cost = [[INF] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0: cost[0][0] = grid[0][0]; ways[0][0] = 1; continue
            best = min(cost[i - 1][j] if i else INF, cost[i][j - 1] if j else INF)
            w = 0
            if i and cost[i - 1][j] == best: w += ways[i - 1][j]
            if j and cost[i][j - 1] == best: w += ways[i][j - 1]
            cost[i][j] = best + grid[i][j]; ways[i][j] = w % M
    return [cost[-1][-1], ways[-1][-1]]
def b_count_min_paths(grid):
    m, n = len(grid), len(grid[0]); res = []
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        i = j = 0; tot = grid[0][0]
        for c in s:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]
        res.append(tot)
    mn = min(res); return [mn, res.count(mn) % M]
def s_paths_mod_k(grid, k):
    m, n = len(grid), len(grid[0])
    dp = [[[0] * k for _ in range(n)] for _ in range(m)]
    dp[0][0][grid[0][0] % k] = 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0: continue
            v = grid[i][j] % k; cell = dp[i][j]
            for src in ((dp[i - 1][j] if i else None), (dp[i][j - 1] if j else None)):
                if src:
                    for r in range(k):
                        if src[r]: cell[(r + v) % k] = (cell[(r + v) % k] + src[r]) % M
    return dp[-1][-1][0]
def b_paths_mod_k(grid, k):
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
    return cnt % M
def s_dungeon(grid):
    m, n = len(grid), len(grid[0]); need = [INF] * (n + 1)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            nxt = 1 if i == m - 1 and j == n - 1 else min(need[j] if i < m - 1 else INF, need[j + 1] if j < n - 1 else INF)
            need[j] = max(1, nxt - grid[i][j])
    return need[0]
def b_dungeon(grid):
    m, n = len(grid), len(grid[0]); best = INF
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        s = ['R'] * (m + n - 2)
        for d in ds: s[d] = 'D'
        i = j = 0; tot = grid[0][0]; low = tot
        for c in s:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]; low = min(low, tot)
        best = min(best, max(1, 1 - low))
    return best
def s_cherry_pickup(grid):
    n = len(grid); NEG = -10**9
    dp = [[NEG] * n for _ in range(n)]; dp[0][0] = grid[0][0]
    for k in range(1, 2 * n - 1):
        nd = [[NEG] * n for _ in range(n)]
        for r1 in range(max(0, k - n + 1), min(n, k + 1)):
            for r2 in range(max(0, k - n + 1), min(n, k + 1)):
                c1, c2 = k - r1, k - r2
                if grid[r1][c1] == -1 or grid[r2][c2] == -1: continue
                best = max(dp[a][b] for a in (r1, r1 - 1) for b in (r2, r2 - 1) if a >= 0 and b >= 0)
                if best < 0: continue
                nd[r1][r2] = best + grid[r1][c1] + (grid[r2][c2] if r1 != r2 else 0)
        dp = nd
    return max(0, dp[n - 1][n - 1])
def b_cherry_pickup(grid):
    n = len(grid)
    def paths():
        for ds in itertools.combinations(range(2 * n - 2), n - 1):
            s = ['R'] * (2 * n - 2)
            for d in ds: s[d] = 'D'
            i = j = 0; cells = [(0, 0)]
            for c in s:
                if c == 'D': i += 1
                else: j += 1
                cells.append((i, j))
            if all(grid[a][b] != -1 for a, b in cells): yield cells
    ps = list(paths()); best = 0
    for p in ps:
        for q in ps: best = max(best, sum(grid[a][b] for a, b in set(p) | set(q)))
    return best
def s_lis_matrix(matrix):
    m, n = len(matrix), len(matrix[0]); cells = sorted((matrix[i][j], i, j) for i in range(m) for j in range(n))
    L = [[1] * n for _ in range(m)]; best = 1
    # process by value; equal values are never adjacent-increasing, so ties need no special order
    for v, i, j in cells:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < m and 0 <= b < n and matrix[a][b] < v and L[a][b] + 1 > L[i][j]: L[i][j] = L[a][b] + 1
        best = max(best, L[i][j])
    return best
def b_lis_matrix(matrix):
    m, n = len(matrix), len(matrix[0])
    def f(i, j): return 1 + max([f(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)) if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[i][j]] or [0])
    return max(f(i, j) for i in range(m) for j in range(n))
def s_memo_stats(m, n, blocked):
    bl = {(r, c) for r, c in blocked}; called = [[False] * n for _ in range(m)]; ways = [[0] * n for _ in range(m)]
    called[0][0] = True; depth = 1
    for i in range(m):
        for j in range(n):
            if not called[i][j]:
                continue
            depth = max(depth, i + j + 1)
            if (i, j) in bl or (i, j) == (m - 1, n - 1): continue
            if i + 1 < m: called[i + 1][j] = True
            if j + 1 < n: called[i][j + 1] = True
    # path counts by a forward table
    w = [[0] * n for _ in range(m)]
    if (0, 0) not in bl: w[0][0] = 1
    for i in range(m):
        for j in range(n):
            if (i, j) in bl: w[i][j] = 0; continue
            if i or j: w[i][j] = (w[i - 1][j] if i else 0) + (w[i][j - 1] if j else 0)
    entries = sum(map(sum, called)) if False else sum(1 for i in range(m) for j in range(n) if called[i][j])
    return [w[-1][-1], entries, depth]
def b_memo_stats(m, n, blocked):
    bl = {(r, c) for r, c in blocked}; st = {'depth': 0, 'cur': 0}
    @lru_cache(maxsize=None)
    def f(i, j):
        st['cur'] += 1; st['depth'] = max(st['depth'], st['cur'])
        try:
            if (i, j) in bl: return 0
            if (i, j) == (m - 1, n - 1): return 1
            return (f(i + 1, j) if i + 1 < m else 0) + (f(i, j + 1) if j + 1 < n else 0)
        finally: st['cur'] -= 1
    r = f(0, 0)
    return [r, f.cache_info().currsize, st['depth']]

# ================= strings, two sequences
def lcs_table(a, b):
    f = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            f[i][j] = f[i + 1][j + 1] + 1 if a[i] == b[j] else max(f[i + 1][j], f[i][j + 1])
    return f
def s_lcs_length(a, b):
    if len(b) > len(a): a, b = b, a
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]
def b_lcs_length(a, b):
    def f(i, j):
        if i == len(a) or j == len(b): return 0
        return 1 + f(i + 1, j + 1) if a[i] == b[j] else max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)
def s_lps(s): return s_lcs_length(s, s[::-1])
def lps_interval(s):
    n = len(s); dp = [0] * n
    for i in range(n - 1, -1, -1):
        dp[i] = 1; prev = 0   # prev = dp_old[i+1][j-1]
        for j in range(i + 1, n):
            tmp = dp[j]
            dp[j] = prev + 2 if s[i] == s[j] else max(dp[j], dp[j - 1])
            prev = tmp
    return dp[n - 1]
def b_lps(s):
    best = 0; n = len(s)
    for mask in range(1 << n):
        t = [s[i] for i in range(n) if mask >> i & 1]
        if t == t[::-1]: best = max(best, len(t))
    return best
def s_edit_distance(a, b):
    if len(b) > len(a): a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = prev[j - 1] if ca == cb else 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[-1]
def b_edit_distance(a, b):
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        if a[i] == b[j]: return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))
    return f(0, 0)
def s_regex_match(s, p):
    m, n = len(s), len(p); f = [[False] * (n + 1) for _ in range(m + 1)]; f[m][n] = True
    for i in range(m, -1, -1):
        for j in range(n - 1, -1, -1):
            first = i < m and p[j] in (s[i], '.')
            if j + 1 < n and p[j + 1] == '*': f[i][j] = f[i][j + 2] or (first and f[i + 1][j])
            else: f[i][j] = first and f[i + 1][j + 1]
    return f[0][0]
def b_regex_match(s, p): return re.fullmatch(p, s, flags=re.S) is not None
def s_lcs_recon(a, b):
    f = lcs_table(a, b); i = j = 0; out = []
    while f[i][j]:
        for c in sorted(set(a[i:]) & set(b[j:])):
            ii, jj = a.index(c, i), b.index(c, j)
            if 1 + f[ii + 1][jj + 1] == f[i][j]:
                out.append(c); i, j = ii + 1, jj + 1; break
    return ''.join(out)
def b_lcs_recon(a, b):
    def subseqs(s):
        return {''.join(s[i] for i in range(len(s)) if mask >> i & 1) for mask in range(1 << len(s))}
    com = subseqs(a) & subseqs(b)
    return min(com, key=lambda t: (-len(t), t))
def s_lcs_substring(a, b):
    n = len(b); prev = [0] * (n + 1); best = (0, -1, -1); end = (0, 0)
    bl, bi, bj = 0, -1, -1
    for i in range(1, len(a) + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1; L = cur[j]; si, sj = i - L, j - L
                if L > bl or (L == bl and (si, sj) < (bi, bj)): bl, bi, bj = L, si, sj
        prev = cur
    return [bl, bi, bj]
def b_lcs_substring(a, b):
    best = [0, -1, -1]
    for L in range(min(len(a), len(b)), 0, -1):
        for i in range(len(a) - L + 1):
            for j in range(len(b) - L + 1):
                if a[i:i + L] == b[j:j + L]: return [L, i, j]
    return best
def s_scs(a, b):
    n, m = len(a), len(b); f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n: f[i][j] = m - j
            elif j == m: f[i][j] = n - i
            elif a[i] == b[j]: f[i][j] = 1 + f[i + 1][j + 1]
            else: f[i][j] = 1 + min(f[i + 1][j], f[i][j + 1])
    i = j = 0; out = []
    while i < n or j < m:
        if i == n: out.append(b[j]); j += 1
        elif j == m: out.append(a[i]); i += 1
        elif a[i] == b[j]: out.append(a[i]); i += 1; j += 1
        else:
            opts = []
            if f[i][j] == 1 + f[i + 1][j]: opts.append((a[i], 1, 0))
            if f[i][j] == 1 + f[i][j + 1]: opts.append((b[j], 0, 1))
            c, di, dj = min(opts); out.append(c); i += di; j += dj
    return ''.join(out)
def is_subseq(t, s):
    it = iter(s); return all(ch in it for ch in t)
def b_scs(a, b):
    L = len(a) + len(b) - s_lcs_length(a, b); alpha = sorted(set(a) | set(b))
    for t in itertools.product(alpha, repeat=L):
        t = ''.join(t)
        if is_subseq(a, t) and is_subseq(b, t): return t
def s_edit_script(a, b):
    n, m = len(a), len(b); f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n: f[i][j] = m - j
            elif j == m: f[i][j] = n - i
            else: f[i][j] = min(1 + f[i + 1][j], 1 + f[i][j + 1], f[i + 1][j + 1] + (a[i] != b[j]))
    i = j = 0; out = []
    while i < n or j < m:
        if i < n and f[i][j] == 1 + f[i + 1][j]: out.append('D'); i += 1
        elif j < m and f[i][j] == 1 + f[i][j + 1]: out.append('I'); j += 1
        elif a[i] == b[j]: out.append('M'); i += 1; j += 1      # (a[i]==b[j]) here means cost 0
        else: out.append('S'); i += 1; j += 1
    return [f[0][0], ''.join(out)]
def b_edit_script(a, b):
    res = []
    def go(i, j, script, cost):
        if i == len(a) and j == len(b): res.append((cost, script)); return
        if i < len(a): go(i + 1, j, script + 'D', cost + 1)
        if j < len(b): go(i, j + 1, script + 'I', cost + 1)
        if i < len(a) and j < len(b):
            if a[i] == b[j]: go(i + 1, j + 1, script + 'M', cost)
            else: go(i + 1, j + 1, script + 'S', cost + 1)
    go(0, 0, '', 0); return list(min(res))
def apply_script(a, b, script):
    i = j = 0; out = []
    for c in script:
        if c == 'D': i += 1
        elif c == 'I': out.append(b[j]); j += 1
        elif c == 'M': assert a[i] == b[j]; out.append(a[i]); i += 1; j += 1
        else: assert a[i] != b[j]; out.append(b[j]); i += 1; j += 1
    assert i == len(a) and j == len(b)
    return ''.join(out)
def s_wildcard_count(s, p):
    m, n = len(s), len(p); f = [[0] * (n + 1) for _ in range(m + 1)]; f[0][0] = 1
    for i in range(m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*': f[i][j] = f[i][j - 1] + (f[i - 1][j] if i else 0)
            elif i and p[j - 1] in ('?', s[i - 1]): f[i][j] = f[i - 1][j - 1]
    return [f[m][n] > 0, f[m][n]]
def b_wildcard_count(s, p):
    def go(i, j):
        if j == len(p): return 1 if i == len(s) else 0
        if p[j] == '*': return sum(go(i + k, j + 1) for k in range(len(s) - i + 1))
        return go(i + 1, j + 1) if i < len(s) and p[j] in ('?', s[i]) else 0
    c = go(0, 0); return [c > 0, c]
def s_interleaving(s1, s2, s3):
    if len(s1) + len(s2) != len(s3): return False
    dp = [False] * (len(s2) + 1)
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i == 0 and j == 0: dp[j] = True; continue
            ok = False
            if i and dp[j] and s1[i - 1] == s3[i + j - 1]: ok = True
            if j and dp[j - 1] and s2[j - 1] == s3[i + j - 1]: ok = True
            dp[j] = ok
    return dp[-1]
def b_interleaving(s1, s2, s3):
    def f(i, j):
        k = i + j
        if k == len(s3): return i == len(s1) and j == len(s2)
        return (i < len(s1) and s1[i] == s3[k] and f(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and f(i, j + 1))
    return len(s1) + len(s2) == len(s3) and f(0, 0)
def s_palin_substr_dp(s):
    n = len(s); dp = [False] * n; cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i - 1, -1):     # j descending: dp[j-1] still holds row i+1
            dp[j] = s[i] == s[j] and (j - i < 3 or dp[j - 1])
            cnt += dp[j]
    return cnt
def b_palin_substr_dp(s):
    return sum(s[i:j] == s[i:j][::-1] for i in range(len(s)) for j in range(i + 1, len(s) + 1))
def s_pal_cuts(s):
    n = len(s); pal = [[False] * n for _ in range(n)]
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):
            while l >= 0 and r < n and s[l] == s[r]: pal[l][r] = True; l -= 1; r += 1
    cuts = [0] * n
    for r in range(n):
        cuts[r] = 0 if pal[0][r] else min(cuts[l - 1] + 1 for l in range(1, r + 1) if pal[l][r])
    return cuts[-1]
def b_pal_cuts(s):
    def f(i):
        if i == len(s): return -1
        return min(1 + f(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return f(0)
def s_ascii_delete(s1, s2):
    n, m = len(s1), len(s2); prev = [0] * (m + 1)
    for i in range(n - 1, -1, -1):
        cur = [0] * (m + 1)
        for j in range(m - 1, -1, -1):
            cur[j] = prev[j + 1] + ord(s1[i]) if s1[i] == s2[j] else max(prev[j], cur[j + 1])
        prev = cur
    return sum(map(ord, s1)) + sum(map(ord, s2)) - 2 * prev[0]
def b_ascii_delete(s1, s2):
    def f(i, j):
        if i == len(s1): return sum(map(ord, s2[j:]))
        if j == len(s2): return sum(map(ord, s1[i:]))
        if s1[i] == s2[j]: return f(i + 1, j + 1)
        return min(ord(s1[i]) + f(i + 1, j), ord(s2[j]) + f(i, j + 1))
    return f(0, 0)
def s_distinct_subseq(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch: dp[j] += dp[j - 1]
    return dp[-1]
def b_distinct_subseq(s, t):
    return sum(1 for idx in itertools.combinations(range(len(s)), len(t)) if all(s[i] == c for i, c in zip(idx, t)))
def s_lrs(s):
    n = len(s); prev = [0] * (n + 1)
    for i in range(1, n + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if s[i - 1] == s[j - 1] and i != j else max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]
def b_lrs(s):
    n = len(s); best = 0
    for L in range(n, 0, -1):
        for P in itertools.combinations(range(n), L):
            t = [s[i] for i in P]
            for Q in itertools.combinations(range(n), L):
                if all(a != b for a, b in zip(P, Q)) and [s[i] for i in Q] == t: return L
    return 0

# ================= intervals
def s_burst_balloons(nums):
    a = [1] + list(nums) + [1]; n = len(a); dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            dp[l][r] = max(dp[l][k] + dp[k][r] + a[l] * a[k] * a[r] for k in range(l + 1, r))
    return dp[0][n - 1]
def b_burst_balloons(nums):
    def f(arr):
        if not arr: return 0
        return max((arr[i - 1] if i else 1) * arr[i] * (arr[i + 1] if i + 1 < len(arr) else 1) + f(arr[:i] + arr[i + 1:]) for i in range(len(arr)))
    return f(list(nums))
def s_matrix_chain(dims):
    n = len(dims) - 1; cost = [[0] * n for _ in range(n)]; split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1; best = None
            for k in range(i, j):
                c = cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if best is None or c < best: best = c; split[i][j] = k
            cost[i][j] = best
    def paren(i, j): return f"A{i}" if i == j else "(" + paren(i, split[i][j]) + paren(split[i][j] + 1, j) + ")"
    return [cost[0][n - 1], paren(0, n - 1)]
def b_matrix_chain(dims):
    n = len(dims) - 1
    def trees(i, j):     # yields (cost, key, string) for every parenthesisation; key orders by smallest root split, then left, then right
        if i == j: yield (0, (), f"A{i}"); return
        for k in range(i, j):
            for cl, kl, sl in trees(i, k):
                for cr, kr, sr in trees(k + 1, j):
                    yield (cl + cr + dims[i] * dims[k + 1] * dims[j + 1], (k, kl, kr), "(" + sl + sr + ")")
    best = min(trees(0, n - 1), key=lambda t: (t[0], t[1]))
    return [best[0], best[2]]
def s_cut_stick(n, cuts):
    c = [0] + sorted(cuts) + [n]; k = len(c); dp = [[0] * k for _ in range(k)]
    for length in range(2, k):
        for l in range(k - length):
            r = l + length
            dp[l][r] = c[r] - c[l] + min(dp[l][m] + dp[m][r] for m in range(l + 1, r))
    return dp[0][k - 1]
def b_cut_stick(n, cuts):
    best = INF
    for order in itertools.permutations(cuts):
        pieces = [(0, n)]; tot = 0
        for x in order:
            for idx, (l, r) in enumerate(pieces):
                if l < x < r: tot += r - l; pieces[idx:idx + 1] = [(l, x), (x, r)]; break
        best = min(best, tot)
    return best if cuts else 0
def s_triangulation(values):
    n = len(values); dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            dp[i][j] = min(dp[i][k] + dp[k][j] + values[i] * values[k] * values[j] for k in range(i + 1, j))
    return dp[0][n - 1]
def b_triangulation(values):
    def f(vs):
        if len(vs) < 3: return 0
        return min(vs[0] * vs[k] * vs[-1] + f(vs[:k + 1]) + f(vs[k:]) for k in range(1, len(vs) - 1))
    return f(list(values))
def s_strange_printer(s):
    t = ''.join(ch for i, ch in enumerate(s) if i == 0 or ch != s[i - 1]); n = len(t)
    if n == 0: return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            dp[i][j] = dp[i][j - 1] + 1
            for k in range(i, j):
                if t[k] == t[j]: dp[i][j] = min(dp[i][j], dp[i][k] + (dp[k + 1][j - 1] if k + 1 <= j - 1 else 0))
    return dp[0][n - 1]
def b_strange_printer(s):
    from collections import deque
    n = len(s)
    if n == 0: return 0
    start = '?' * n; seen = {start}; dq = deque([(start, 0)])
    while dq:
        cur, d = dq.popleft()
        if cur == s: return d
        for l in range(n):
            for r in range(l, n):
                if s[l] != s[r] and False: continue
                for ch in set(s):
                    nxt = cur[:l] + ch * (r - l + 1) + cur[r + 1:]
                    if nxt not in seen: seen.add(nxt); dq.append((nxt, d + 1))
def s_assign_tasks(cost):
    n = len(cost); f = [INF] * (1 << n); f[(1 << n) - 1] = 0
    for mask in range((1 << n) - 2, -1, -1):
        k = bin(mask).count('1')
        for t in range(n):
            if not mask >> t & 1: f[mask] = min(f[mask], cost[k][t] + f[mask | 1 << t])
    mask = 0; out = []
    for k in range(n):
        for t in range(n):
            if not mask >> t & 1 and cost[k][t] + f[mask | 1 << t] == f[mask]: out.append(t); mask |= 1 << t; break
    return [f[0], out]
def b_assign_tasks(cost):
    n = len(cost)
    return list(min((sum(cost[i][p[i]] for i in range(n)), list(p)) for p in itertools.permutations(range(n))))
def s_tsp(dist):
    n = len(dist)
    if n == 1: return 0
    f = [[INF] * n for _ in range(1 << n)]; f[1][0] = 0
    for mask in range(1, 1 << n, 2):
        for last in range(n):
            v = f[mask][last]
            if v == INF: continue
            for nx in range(1, n):
                if not mask >> nx & 1:
                    nm = mask | 1 << nx
                    if v + dist[last][nx] < f[nm][nx]: f[nm][nx] = v + dist[last][nx]
    full = (1 << n) - 1
    return min(f[full][l] + dist[l][0] for l in range(1, n))
def b_tsp(dist):
    n = len(dist)
    if n == 1: return 0
    return min(sum(dist[a][b] for a, b in zip((0,) + p, p + (0,))) for p in itertools.permutations(range(1, n)))

S = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('s_')}
B = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('b_')}
