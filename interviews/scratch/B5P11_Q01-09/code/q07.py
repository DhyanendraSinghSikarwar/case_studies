import itertools
import random
import sys
from functools import lru_cache

random.seed(1107)

def lps_table(s):
    """dp[i][j] = LPS length inside s[i..j]. Fill i from n-1 down to 0, j from i+1 up to n-1:
    dp[i][j] needs dp[i+1][j-1], dp[i+1][j] (row below) and dp[i][j-1] (same row, left)."""
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp

def lps_one_row(s):
    """dp[j] holds dp[i+1][j] until overwritten with dp[i][j]; prev saves old dp[j-1] = dp[i+1][j-1]."""
    n = len(s)
    dp = [0] * n
    for i in range(n - 1, -1, -1):
        dp[i] = 1
        prev = 0                                   # dp[i+1][i] = empty range = 0
        for j in range(i + 1, n):
            keep = dp[j]                           # dp[i+1][j]
            dp[j] = prev + 2 if s[i] == s[j] else max(dp[j], dp[j - 1])
            prev = keep
    return dp[n - 1]

def lcs_len(a, b):
    if len(b) > len(a):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def lps_via_lcs(s):
    return lcs_len(s, s[::-1])

def lps_all_subsequences(s):
    """Oracle: every subsequence (bitmask), keep palindromes."""
    n, best = len(s), 0
    for mask in range(1 << n):
        t = [s[i] for i in range(n) if mask >> i & 1]
        if t == t[::-1]:
            best = max(best, len(t))
    return best

def lps_memo(s):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return 2 + f(i + 1, j - 1)
        return max(f(i + 1, j), f(i, j - 1))
    return f(0, len(s) - 1)

def min_insertions(s):
    return len(s) - lps_one_row(s)

def min_insertions_recursive(s):
    """Independent recursion for 'min insertions to make a palindrome'."""
    def f(i, j):
        if i >= j:
            return 0
        if s[i] == s[j]:
            return f(i + 1, j - 1)
        return 1 + min(f(i + 1, j), f(i, j - 1))
    return f(0, len(s) - 1)

def min_insertions_brute(s):
    """Shortest palindrome (over the alphabet of s) that has s as a subsequence, by enumeration."""
    def is_subseq(t, u):
        it = iter(u)
        return all(c in it for c in t)
    alpha = sorted(set(s))
    for L in range(len(s), 2 * len(s) + 1):
        half = (L + 1) // 2
        for h in itertools.product(alpha, repeat=half):
            pal = ''.join(h) + ''.join(h[:L // 2][::-1])
            if is_subseq(s, pal):
                return L - len(s)

for s, want in [('bbbab', 4), ('cbbd', 2), ('a', 1), ('abcd', 1), ('agbdba', 5)]:
    assert lps_table(s)[0][-1] == lps_one_row(s) == lps_via_lcs(s) == lps_all_subsequences(s) == lps_memo(s) == want, s
print("5 prompt examples ok")

s = 'bbbab'
print("walk-through s =", s, "(dp[i][j] for i <= j, '.' below the diagonal)")
t = lps_table(s)
print("        " + "  ".join(s))
for i in range(len(s)):
    print("   ", s[i], "  ", "  ".join(str(t[i][j]) if j >= i else '.' for j in range(len(s))))
print("  answer dp[0][4] =", t[0][-1])

cnt = 0
for n in range(1, 8):
    for tup in itertools.product('abc', repeat=n):
        s = ''.join(tup)
        o = lps_all_subsequences(s)
        assert lps_table(s)[0][-1] == lps_one_row(s) == lps_via_lcs(s) == o, s
        cnt += 1
print("exhaustive over {a,b,c}, len 1..7:", cnt, "strings: interval table == one row == LCS(s, reverse) == all subsequences")
for _ in range(400):
    s = ''.join(random.choice('abcde') for _ in range(random.randint(1, 12)))
    assert lps_one_row(s) == lps_all_subsequences(s) == lps_via_lcs(s) == lps_memo(s) == lps_table(s)[0][-1]
print("400 seeded random strings (len <= 12, alphabet abcde): ok")

# insertions / deletions claim: n - LPS
for n in range(1, 6):
    for tup in itertools.product('abc', repeat=n):
        s = ''.join(tup)
        assert min_insertions(s) == min_insertions_recursive(s) == min_insertions_brute(s), s
print("min insertions = n - LPS verified against recursion and shortest-palindromic-supersequence enumeration, all strings over {a,b,c}, len 1..5")
print("   e.g. 'abcd' needs", min_insertions('abcd'), "insertions (abcdcba), 'agbdba' needs", min_insertions('agbdba'))

# size 2000
rnd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(2000))
v = lps_one_row(rnd)
assert v == lps_via_lcs(rnd) == lps_table(rnd)[0][-1]
print("n = 2000 random letters: LPS =", v, "(one row == LCS with reverse == full table)")
print("n = 2000 'a' * 2000:", lps_one_row('a' * 2000))
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x):
    try:
        return "ok" if lps_memo(x) == lps_one_row(x) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion on 'abcd...' cycling strings (depth grows with n):")
for n in (300, 500, 2000):
    x = ''.join(chr(97 + i % 26) for i in range(n))
    print("   n = %4d: %s" % (n, memo_outcome(x)))
print("memoised recursion, n = 2000 random letters:", memo_outcome(rnd))
print("memoised recursion, 'a' * 1000 (ends always equal, depth about n/2):", memo_outcome('a' * 1000))
