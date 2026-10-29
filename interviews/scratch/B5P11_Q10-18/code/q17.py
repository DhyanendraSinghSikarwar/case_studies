import itertools
import random
import re
import sys
from functools import lru_cache
from math import comb

random.seed(1717)

def wildcard_table(s, p):
    """f[i][j] = number of ways the first j pattern symbols match the first i letters of s (each '*' counted separately)."""
    m, n = len(s), len(p)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    f[0][0] = 1
    for i in range(m + 1):
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                # zero characters: f[i][j-1]; one more character (absorbed by this star): f[i-1][j]
                f[i][j] = f[i][j - 1] + (f[i - 1][j] if i else 0)
            elif i and (c == '?' or c == s[i - 1]):
                f[i][j] = f[i - 1][j - 1]
    return f

def wildcard(s, p):
    f = wildcard_table(s, p)
    return [f[-1][-1] > 0, f[-1][-1]]

def wildcard_row(s, p):
    """One row over the pattern. Rows are indexed by i (letters of s used); row[j] holds f[i][j]."""
    m, n = len(s), len(p)
    row = [0] * (n + 1)
    row[0] = 1                                   # i = 0
    for j in range(1, n + 1):
        row[j] = row[j - 1] if p[j - 1] == '*' else 0
    for i in range(1, m + 1):
        new = [0] * (n + 1)
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                new[j] = new[j - 1] + row[j]     # f[i][j-1] + f[i-1][j]
            elif c == '?' or c == s[i - 1]:
                new[j] = row[j - 1]              # f[i-1][j-1]
        row = new
    return [row[n] > 0, row[n]]

def wildcard_bool(s, p):
    """Same shape, 'or' instead of '+'."""
    m, n = len(s), len(p)
    f = [[False] * (n + 1) for _ in range(m + 1)]
    f[0][0] = True
    for i in range(m + 1):
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                f[i][j] = f[i][j - 1] or (i > 0 and f[i - 1][j])
            elif i and (c == '?' or c == s[i - 1]):
                f[i][j] = f[i - 1][j - 1]
    return f[m][n]

def wildcard_memo(s, p):
    @lru_cache(maxsize=None)
    def go(i, j):                                # i letters, j pattern symbols consumed from the FRONT
        if j == len(p): return 1 if i == len(s) else 0
        if p[j] == '*': return go(i, j + 1) + (go(i + 1, j) if i < len(s) else 0)
        return go(i + 1, j + 1) if i < len(s) and p[j] in ('?', s[i]) else 0
    return go(0, 0)

def brute(s, p):
    """Enumerate every run-length assignment to the stars (plain recursion)."""
    def go(i, j):
        if j == len(p): return 1 if i == len(s) else 0
        if p[j] == '*': return sum(go(i + k, j + 1) for k in range(len(s) - i + 1))
        return go(i + 1, j + 1) if i < len(s) and p[j] in ('?', s[i]) else 0
    c = go(0, 0)
    return [c > 0, c]

def as_regex(p):
    return ''.join('.*' if c == '*' else '.' if c == '?' else c for c in p)

for s, p, want in [('aa', 'a', [False, 0]), ('aa', '*', [True, 1]), ('cb', '?a', [False, 0]), ('adceb', '*a*b', [True, 1]), ('', '**', [True, 1]), ('abc', 'a?c', [True, 1])]:
    assert wildcard(s, p) == wildcard_row(s, p) == brute(s, p) == want, (s, p)
    assert wildcard_bool(s, p) == want[0]
print('6 prompt examples ok')

f = wildcard_table('adceb', '*a*b')
print("f for s='adceb' (rows i=0..5 letters used), p='*a*b' (cols j=0..4 symbols used):")
print('      ', ' '.join('-*a*b'))
for i, row in enumerate(f):
    print('  ', '-adceb'[i], row)

pos = 0
for _ in range(1500):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 7)))
    p = ''.join(random.choice('ab?**') for _ in range(random.randint(0, 6)))
    r = wildcard(s, p)
    assert r == brute(s, p) == wildcard_row(s, p) == [wildcard_memo(s, p) > 0, wildcard_memo(s, p)], (s, p)
    assert r[0] == wildcard_bool(s, p) == (r[1] > 0) == (re.fullmatch(as_regex(p), s, re.S) is not None)
    pos += r[0]
print('1500 seeded random (s, p): table == plain recursion == one row == memo; boolean table == (ways > 0) == regex translation; True in', pos, 'of 1500')
assert 0 < pos < 1500

# closed form: s = a^n against k stars has C(n + k - 1, k - 1) assignments
for n_ in range(0, 9):
    for k in range(1, 6):
        assert wildcard('a' * n_, '*' * k)[1] == comb(n_ + k - 1, k - 1)
print('closed form checked: ways(a^n, k stars) == C(n + k - 1, k - 1) for n 0..8, k 1..5')
print("'**' on 'ab' gives", wildcard('ab', '**'), '(three splits: 0|2, 1|1, 2|0)')

print('recursion limit:', sys.getrecursionlimit())
s = 'a' * 300; p = '*a' * 150
r = wildcard(s, p)
print('max size 300 vs 300 symbols (150 stars): ways =', r[1] if r[1] < 10**12 else str(r[1])[:12] + '... (%d digits)' % len(str(r[1])), '| one row agrees:', wildcard_row(s, p) == r)
print('memoised version at 300 + 300 (depth <= 600):', 'agrees' if wildcard_memo(s, p) == r[1] else 'DIFFERS')
rs = ''.join(random.choice('ab') for _ in range(300)); rp = ''.join(random.choice('ab?*') for _ in range(300))
assert wildcard(rs, rp) == wildcard_row(rs, rp)
try:
    wildcard_memo('a' * 700, '*' * 700); print('memoised 700 + 700: ok')
except RecursionError:
    print('memoised 700 + 700 (outside the prompt sizes): RecursionError')

assert wildcard('', '') == [True, 1] and wildcard('a', '') == [False, 0] and wildcard('', 'a') == [False, 0] and wildcard('', '?') == [False, 0]
print('edge asserts ok')
