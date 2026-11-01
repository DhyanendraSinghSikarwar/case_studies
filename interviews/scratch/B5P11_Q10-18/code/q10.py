import itertools
import random
import sys
from functools import lru_cache

random.seed(1010)

def suffix_table(a, b):
    """f[i][j] = LCS length of a[i:] and b[j:]; row len(a) and column len(b) stay 0 (empty suffix)."""
    m, n = len(a), len(b)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                f[i][j] = 1 + f[i + 1][j + 1]
            else:
                f[i][j] = max(f[i + 1][j], f[i][j + 1])
    return f

def lcs_smallest(a, b):
    """Lexicographically smallest longest common subsequence, bottom-up, no recursion."""
    f = suffix_table(a, b)
    i = j = 0
    out = []
    while f[i][j]:
        # candidate letters are those present in both remaining suffixes, tried a..z
        for c in sorted(set(a[i:]) & set(b[j:])):
            ii, jj = a.index(c, i), b.index(c, j)        # FIRST occurrences at or after i / j
            if 1 + f[ii + 1][jj + 1] == f[i][j]:
                out.append(c)
                i, j = ii + 1, jj + 1
                break
    return ''.join(out)

def lcs_backpointer(a, b):
    """The classic walk: prefix table, start at the bottom-right cell, go up/left. NOT lexicographically smallest."""
    m, n = len(a), len(b)
    g = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            g[i][j] = g[i-1][j-1] + 1 if a[i-1] == b[j-1] else max(g[i-1][j], g[i][j-1])
    i, j, out = m, n, []
    while i and j:
        if a[i-1] == b[j-1]:
            out.append(a[i-1]); i -= 1; j -= 1
        elif g[i-1][j] >= g[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(out))

def lcs_memo(a, b):
    """Top-down version of the same table (shows the recursion-limit problem)."""
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def subseqs(s):
    return {''.join(s[i] for i in range(len(s)) if mask >> i & 1) for mask in range(1 << len(s))}

def brute(a, b):
    """Every common subsequence (len <= 8), longest first, then smallest."""
    common = subseqs(a) & subseqs(b)
    return min(common, key=lambda t: (-len(t), t))

# 1. prompt examples
for a, b, want in [('abcde', 'ace', 'ace'), ('abcbdab', 'bdcaba', 'bcab'), ('abc', 'def', ''), ('zxy', 'xyz', 'xy'), ('', '', '')]:
    assert lcs_smallest(a, b) == brute(a, b) == want, (a, b)
print('5 prompt examples ok')

# 2. hand-table source: suffix table for a='abcde', b='ace'
f = suffix_table('abcde', 'ace')
print("f for a='abcde' (rows i=0..5), b='ace' (cols j=0..3):")
for i, row in enumerate(f):
    print(' ', ('abcde' + '-')[i], row)

# 3. seeded random cross-check against full enumeration
for _ in range(400):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert lcs_smallest(a, b) == brute(a, b), (a, b)
print('400 seeded random pairs (len 0..8, alphabet abc): smallest-LCS walk == enumeration')

# 4. exhaustive: all pairs up to length 4 over {a,b} (961 pairs)
cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert lcs_smallest(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# 5. the claim: the back-pointer walk is NOT automatically the smallest string (but it is still a longest one)
diff = 0
for _ in range(500):
    a = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    x, y = lcs_backpointer(a, b), lcs_smallest(a, b)
    assert len(x) == len(y)
    diff += x != y
print('back-pointer walk differs from the smallest LCS on', diff, 'of 500 random pairs')
print("example: abcbdab / bdcaba -> back-pointer", lcs_backpointer('abcbdab', 'bdcaba'), "vs smallest", lcs_smallest('abcbdab', 'bdcaba'))

# 6. size and recursion limit (default limit)
print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(1000)); y = ''.join(random.choice('abcd') for _ in range(1000))
r = lcs_smallest(x, y)
assert len(r) == len(lcs_backpointer(x, y))
print('bottom-up 1000 x 1000 random: LCS length', len(r))
print('memoised, two 300-letter random strings ->', lcs_memo(x[:300], y[:300]))
try:
    lcs_memo('a' * 1000, 'b' * 1000)
    print('memoised disjoint 1000 + 1000: ok')
except RecursionError:
    print('memoised disjoint 1000 + 1000: RecursionError')
print('bottom-up disjoint 1000 + 1000 ->', repr(lcs_smallest('a' * 1000, 'b' * 1000)))

# 7. edge cases
assert lcs_smallest('', 'abc') == '' and lcs_smallest('abc', '') == ''
assert lcs_smallest('aaa', 'aa') == 'aa' and lcs_smallest('ba', 'ab') == 'a'
assert lcs_smallest('abc', 'abc') == 'abc'
print('edge asserts ok')
