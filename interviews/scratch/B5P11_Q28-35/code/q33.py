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
