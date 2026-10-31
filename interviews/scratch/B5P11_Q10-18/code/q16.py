import itertools
import random
import sys
from functools import lru_cache

random.seed(1616)

def suffix_table(a, b):
    """g[i][j] = length of a shortest common supersequence of a[i:] and b[j:]."""
    n, m = len(a), len(b)
    g = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                g[i][j] = m - j                       # only b's rest is left: emit it
            elif j == m:
                g[i][j] = n - i
            elif a[i] == b[j]:
                g[i][j] = 1 + g[i + 1][j + 1]         # equal heads: emit once
            else:
                g[i][j] = 1 + min(g[i + 1][j], g[i][j + 1])
    return g

def scs(a, b):
    """Lexicographically smallest shortest common supersequence."""
    n, m = len(a), len(b)
    g = suffix_table(a, b)
    i = j = 0
    out = []
    while i < n and j < m:
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        else:
            options = []                              # (letter, move) for the moves that keep the total optimal
            if g[i][j] == 1 + g[i + 1][j]: options.append((a[i], 'a'))
            if g[i][j] == 1 + g[i][j + 1]: options.append((b[j], 'b'))
            letter, move = min(options)               # letters differ, so no tie inside min
            out.append(letter)
            if move == 'a': i += 1
            else: j += 1
    out.append(a[i:]); out.append(b[j:])              # at most one of these is non-empty
    return ''.join(out)

def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def scs_length_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        if a[i] == b[j]: return 1 + f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def is_subseq(t, s):
    it = iter(s)
    return all(ch in it for ch in t)

def brute(a, b):
    """Every string of the right length in alphabetical order; the first that contains both is the answer."""
    L = len(a) + len(b) - lcs_length(a, b)
    alpha = sorted(set(a) | set(b))
    for t in itertools.product(alpha, repeat=L):
        t = ''.join(t)
        if is_subseq(a, t) and is_subseq(b, t):
            return t
    return None

def brute_length(a, b):
    """Independent length check (does not use the LCS formula): shortest L for which some string works."""
    alpha = sorted(set(a) | set(b))
    for L in range(max(len(a), len(b)), len(a) + len(b) + 1):
        for t in itertools.product(alpha, repeat=L):
            t = ''.join(t)
            if is_subseq(a, t) and is_subseq(b, t):
                return L

for a, b, want in [('abac', 'cab', 'cabac'), ('abc', 'abc', 'abc'), ('', 'xy', 'xy'), ('ab', 'ba', 'aba')]:
    assert scs(a, b) == brute(a, b) == want, (a, b)
print('4 prompt examples ok')

g = suffix_table('abac', 'cab')
print("g (SCS length of a[i:], b[j:]) for a='abac' (rows), b='cab' (cols j=0..3):")
for i, row in enumerate(g):
    print(' ', 'abac-'[i], row)
print('walk ->', scs('abac', 'cab'))

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 4)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 4)))
    r = scs(a, b)
    assert r == brute(a, b), (a, b)
    assert len(r) == len(a) + len(b) - lcs_length(a, b) == suffix_table(a, b)[0][0] == scs_length_memo(a, b)
    assert is_subseq(a, r) and is_subseq(b, r)
print('500 seeded random pairs (len 0..4, alphabet abc): walk == alphabetical enumeration; length == m + n - LCS == memo; both inputs are subsequences')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        r = scs(a, b)
        assert r == brute(a, b) and len(r) == brute_length(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok (also the length equals the shortest length found by search, not by the LCS formula)')

print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(500)); y = ''.join(random.choice('abcd') for _ in range(500))
r = scs(x, y)
assert len(r) == 1000 - lcs_length(x, y) and is_subseq(x, r) and is_subseq(y, r)
print('bottom-up 500 + 500 random: length', len(r), '(= 1000 - LCS)')
print('memoised length, two random 300-letter strings:', scs_length_memo(x[:300], y[:300]))
try:
    scs_length_memo('a' * 500, 'b' * 500); print('memoised disjoint 500 + 500: ok')
except RecursionError:
    print('memoised disjoint 500 + 500: RecursionError (depth up to 1000)')
print('disjoint 500 + 500 bottom-up length:', len(scs('a' * 500, 'b' * 500)))

assert scs('', '') == '' and scs('abc', '') == 'abc' and scs('a', 'a') == 'a' and scs('b', 'a') == 'ab'
print('edge asserts ok')
