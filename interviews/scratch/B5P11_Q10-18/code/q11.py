import itertools
import random
import time

random.seed(1111)

def table(a, b):
    """Full table: d[i][j] = length of the common SUFFIX of a[:i] and b[:j] (0 on a mismatch)."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                d[i][j] = d[i - 1][j - 1] + 1
    return d

def lcsubstr(a, b):
    """One row. Returns [length, i, j]; ties: smallest i, then smallest j; no common letter -> [0, -1, -1]."""
    n = len(b)
    row = [0] * (n + 1)              # row[j] = d[i-1][j] before the update, d[i][j] after it
    best_len, best_i, best_j = 0, -1, -1
    for i in range(1, len(a) + 1):
        for j in range(n, 0, -1):    # descending: row[j-1] still holds d[i-1][j-1] (the diagonal)
            if a[i - 1] == b[j - 1]:
                row[j] = row[j - 1] + 1
                L = row[j]
                si, sj = i - L, j - L            # start indices of this common block
                if L > best_len or (L == best_len and (si, sj) < (best_i, best_j)):
                    best_len, best_i, best_j = L, si, sj
            else:
                row[j] = 0           # the reset that makes it a SUBSTRING table
    return [best_len, best_i, best_j]

def brute(a, b):
    """All lengths, longest first, all start pairs in order (len <= 8)."""
    for L in range(min(len(a), len(b)), 0, -1):
        for i in range(len(a) - L + 1):
            for j in range(len(b) - L + 1):
                if a[i:i + L] == b[j:j + L]:
                    return [L, i, j]
    return [0, -1, -1]

for a, b, want in [('abcdxyz', 'xyzabcd', [4, 0, 3]), ('abc', 'def', [0, -1, -1]), ('aaa', 'aa', [2, 0, 0]), ('xabcx', 'yabcy', [3, 1, 1])]:
    assert lcsubstr(a, b) == brute(a, b) == want, (a, b)
print('4 prompt examples ok')

d = table('abcdxyz', 'xyzabcd')
print("d for a='abcdxyz' (rows) vs b='xyzabcd' (cols):")
print('       ', '  '.join(c for c in ' ' + 'xyzabcd'))
for i, row in enumerate(d):
    print('  ', ' ' if i == 0 else 'abcdxyz'[i - 1], row)

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert lcsubstr(a, b) == brute(a, b), (a, b)
print('500 seeded random pairs (len 0..8, alphabet abc): one-row DP == brute force')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert lcsubstr(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# why the answer is the MAX over all cells, not the last cell: d[m][n] is only the common suffix length
a, b = 'abcdxyz', 'xyzabcd'
print('last cell d[m][n] =', table(a, b)[-1][-1], 'but the answer is', lcsubstr(a, b)[0])
assert table(a, b)[-1][-1] == 0

# max size 2000 x 2000 (sandbox timing only)
x = ''.join(random.choice('ab') for _ in range(2000)); y = ''.join(random.choice('ab') for _ in range(2000))
t = time.perf_counter(); r = lcsubstr(x, y); dt = time.perf_counter() - t
assert x[r[1]:r[1] + r[0]] == y[r[2]:r[2] + r[0]]
print('2000 x 2000 over {a,b}: length', r[0], 'found; sandbox time under 5 s:', dt < 5)
print('2000 a vs 2000 a ->', lcsubstr('a' * 2000, 'a' * 2000))

assert lcsubstr('', '') == [0, -1, -1] and lcsubstr('a', '') == [0, -1, -1]
assert lcsubstr('abab', 'abab') == [4, 0, 0] and lcsubstr('ab', 'ba') == [1, 0, 1]
print('edge asserts ok')
