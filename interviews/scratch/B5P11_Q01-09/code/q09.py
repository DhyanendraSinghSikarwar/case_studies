import itertools
import random
import re
import sys
from functools import lru_cache

random.seed(1109)

def match_table(s, p):
    """f[i][j] = True iff s[i:] matches p[j:] completely. Suffix form: fill i from m down, j from n down."""
    m, n = len(s), len(p)
    f = [[False] * (n + 1) for _ in range(m + 1)]
    f[m][n] = True                                    # empty vs empty
    for i in range(m, -1, -1):
        for j in range(n - 1, -1, -1):
            first = i < m and p[j] in (s[i], '.')     # does the head of p match the head of s?
            if j + 1 < n and p[j + 1] == '*':
                f[i][j] = f[i][j + 2] or (first and f[i + 1][j])   # zero copies, or one more copy
            else:
                f[i][j] = first and f[i + 1][j + 1]
    return f

def match_two_rows(s, p):
    """Row i needs row i+1 and itself at j+2: keep two rows."""
    m, n = len(s), len(p)
    nxt = [False] * (n + 1)                           # row m
    for i in range(m, -1, -1):
        cur = [False] * (n + 1)
        if i == m:
            cur[n] = True
        for j in range(n - 1, -1, -1):
            first = i < m and p[j] in (s[i], '.')
            if j + 1 < n and p[j + 1] == '*':
                cur[j] = cur[j + 2] or (first and nxt[j])
            else:
                cur[j] = first and nxt[j + 1]
        nxt = cur
    return nxt[0]

def match_prefix(s, p):
    """Prefix form: g[i][j] = s[:i] matches p[:j]. A '*' at p[j-1] works with the item p[j-2]."""
    m, n = len(s), len(p)
    g = [[False] * (n + 1) for _ in range(m + 1)]
    g[0][0] = True
    for i in range(m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                g[i][j] = g[i][j - 2] or (i > 0 and p[j - 2] in (s[i - 1], '.') and g[i - 1][j])
            else:
                g[i][j] = i > 0 and p[j - 1] in (s[i - 1], '.') and g[i - 1][j - 1]
    return g[m][n]

def match_stdlib(s, p):
    return re.fullmatch(p, s) is not None

def match_memo(s, p):
    m, n = len(s), len(p)
    @lru_cache(maxsize=None)
    def f(i, j):
        if j == n:
            return i == m
        first = i < m and p[j] in (s[i], '.')
        if j + 1 < n and p[j + 1] == '*':
            return f(i, j + 2) or (first and f(i + 1, j))
        return first and f(i + 1, j + 1)
    return f(0, 0)

for (s, p), want in [(('aa', 'a'), False), (('aa', 'a*'), True), (('ab', '.*'), True), (('aab', 'c*a*b'), True),
                     (('mississippi', 'mis*is*p*.'), False), (('', 'a*b*'), True)]:
    assert match_table(s, p)[0][0] == match_two_rows(s, p) == match_prefix(s, p) == match_stdlib(s, p) == match_memo(s, p) == want, (s, p)
print("6 prompt examples ok")

def show(s, p):
    f = match_table(s, p)
    print("walk-through s =", repr(s), " p =", repr(p), "(f[i][j]: s[i:] matches p[j:]; T/F)")
    print("          " + "  ".join(list(p) + ["$"]))
    for i in range(len(s) + 1):
        print("   ", (repr(s[i:]) if i < len(s) else "''").ljust(6), "  ".join("T" if v else "F" for v in f[i]))
    print("  answer f[0][0] =", f[0][0])
show('aa', 'a')
show('aab', 'c*a*b')

# valid patterns: items (letter or '.') each optionally followed by one '*'
def patterns(max_items, alpha='ab.'):
    yield ''
    for k in range(1, max_items + 1):
        for items in itertools.product(alpha, repeat=k):
            for stars in itertools.product((0, 1), repeat=k):
                yield ''.join(c + ('*' if st else '') for c, st in zip(items, stars))
pats = list(patterns(4))
strs = [''.join(t) for k in range(6) for t in itertools.product('ab', repeat=k)]
cnt = 0
for p in pats:
    for s in strs:
        want = match_stdlib(s, p)
        assert match_table(s, p)[0][0] == match_two_rows(s, p) == match_prefix(s, p) == want, (s, p)
        cnt += 1
print("exhaustive vs re.fullmatch:", len(pats), "patterns (up to 4 items over a, b, '.', each with optional '*') x", len(strs), "strings (len <= 5 over {a,b}) =", cnt, "pairs ok")
trues = sum(match_stdlib(s, p) for p in pats for s in strs)
print("   of which", trues, "are matches, so both outcomes are well covered")
for _ in range(1000):
    k = random.randint(0, 6)
    p = ''.join(random.choice('abc.') + random.choice(['', '*']) for _ in range(k))
    s = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert match_table(s, p)[0][0] == match_stdlib(s, p) == match_memo(s, p) == match_two_rows(s, p), (s, p)
print("1000 seeded random (s, p) with s <= 8 and up to 6 pattern items: ok")

# size 1000
S = 'a' * 1000
P = 'a*' * 500
print("1000 x 1000: 'a'*1000 vs 'a*'*500 ->", match_two_rows(S, P), "; vs 'a*'*499 + 'b' ->", match_two_rows(S, 'a*' * 499 + 'b'))
R = ''.join(random.choice('ab') for _ in range(1000))
Q = ''.join(random.choice('ab.') + random.choice(['', '*']) for _ in range(333))[:1000]
assert match_table(R, Q)[0][0] == match_two_rows(R, Q) == match_prefix(R, Q)
print("random 1000-letter s vs random pattern of", len(Q), "chars: table == two rows == prefix form ->", match_two_rows(R, Q))
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x, y):
    try:
        return "ok" if match_memo(x, y) == match_two_rows(x, y) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion on 'a' * n vs 'a*' * (n/2):")
for n in (100, 300, 400, 1000):
    print("   n = %4d: %s" % (n, memo_outcome('a' * n, 'a*' * (n // 2))))
