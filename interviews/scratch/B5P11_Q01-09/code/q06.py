import itertools
import random
import sys
from functools import lru_cache

random.seed(1106)

def lcs_table(a, b):
    """dp[i][j] = LCS length of a[:i] and b[:j]. Row 0 and column 0 are 0 (empty prefix)."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp

def lcs_two_rows(a, b):
    """Two rows indexed by the SHORTER string: extra space O(min(m, n))."""
    if len(b) > len(a):
        a, b = b, a                              # b is now the shorter one
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def lcs_one_row(a, b):
    """One row plus a saved diagonal."""
    if len(b) > len(a):
        a, b = b, a
    row = [0] * (len(b) + 1)
    for ch in a:
        diag = 0                                 # old row[j-1]
        for j in range(1, len(b) + 1):
            up = row[j]
            row[j] = diag + 1 if ch == b[j - 1] else max(up, row[j - 1])
            diag = up
    return row[-1]

def lcs_plain(a, b):
    """Oracle: plain recursion, no memo."""
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def lcs_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

for (a, b), want in [(('abcde', 'ace'), 3), (('abc', 'def'), 0), (('', 'abc'), 0), (('abcba', 'abcbcba'), 5)]:
    assert lcs_two_rows(a, b) == lcs_table(a, b)[-1][-1] == lcs_one_row(a, b) == lcs_plain(a, b) == lcs_memo(a, b) == want, (a, b)
print("4 prompt examples ok")

a, b = 'abcde', 'ace'
print("walk-through a =", a, " b =", b, " (rows = prefixes of a, columns = prefixes of b)")
print("        ", ["''"] + list(b))
for i, r in enumerate(lcs_table(a, b)):
    print("  ", ("'" + a[:i] + "'").ljust(8), r)

# exhaustive: all pairs over {a,b}, lengths 0..5
cnt = 0
for la in range(6):
    for lb in range(6):
        for x in itertools.product('ab', repeat=la):
            for y in itertools.product('ab', repeat=lb):
                x_, y_ = ''.join(x), ''.join(y)
                assert lcs_two_rows(x_, y_) == lcs_plain(x_, y_) == lcs_one_row(x_, y_), (x_, y_)
                cnt += 1
print("exhaustive over {a,b}, lengths 0..5:", cnt, "pairs: two rows == one row == plain recursion")
for _ in range(500):
    x = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    y = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    assert lcs_two_rows(x, y) == lcs_plain(x, y) == lcs_table(x, y)[-1][-1] == lcs_memo(x, y)
    assert lcs_two_rows(x, y) == lcs_two_rows(y, x)
print("500 seeded random pairs (len <= 8, alphabet abcd): ok; symmetric in (a, b)")

# size 1000: bottom-up works; memoised recursion nests deeper than the default limit
def letters(n, alpha):
    return ''.join(random.choice(alpha) for _ in range(n))
A, B = letters(1000, 'abcdefghijklmnopqrstuvwxyz'), letters(1000, 'abcdefghijklmnopqrstuvwxyz')
v = lcs_two_rows(A, B)
assert v == lcs_table(A, B)[-1][-1] == lcs_one_row(A, B)
print("1000 x 1000 random letters: LCS =", v, "(two rows == full table == one row)")
print("identical strings of 1000:", lcs_two_rows('a' * 1000, 'a' * 1000))
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x, y):
    try:
        return "ok" if lcs_memo(x, y) == lcs_two_rows(x, y) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion, disjoint strings (worst depth m + n):")
for n in (100, 300, 400, 1000):
    print("   n = %4d each: %s" % (n, memo_outcome('a' * n, 'b' * n)))
print("memoised recursion, 1000 x 1000 random letters:", memo_outcome(A, B))
