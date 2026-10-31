import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1515)

def suffix_table(a, b):
    """f[i][j] = edit distance between a[i:] and b[j:]. Base: f[n][j] = m - j (insert the rest), f[i][m] = n - i (delete the rest)."""
    n, m = len(a), len(b)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                f[i][j] = m - j
            elif j == m:
                f[i][j] = n - i
            else:
                f[i][j] = min(1 + f[i + 1][j],                              # D: delete a[i]
                              1 + f[i][j + 1],                              # I: insert b[j]
                              f[i + 1][j + 1] + (a[i] != b[j]))             # M (free) or S (cost 1)
    return f

def edit_script(a, b):
    """[distance, script], lexicographically smallest optimal script with D < I < M < S."""
    n, m = len(a), len(b)
    f = suffix_table(a, b)
    i = j = 0
    out = []
    while i < n or j < m:
        if i < n and f[i][j] == 1 + f[i + 1][j]:
            out.append('D'); i += 1
        elif j < m and f[i][j] == 1 + f[i][j + 1]:
            out.append('I'); j += 1
        elif i < n and j < m and a[i] == b[j] and f[i][j] == f[i + 1][j + 1]:
            out.append('M'); i += 1; j += 1
        else:
            assert i < n and j < m and a[i] != b[j] and f[i][j] == 1 + f[i + 1][j + 1]
            out.append('S'); i += 1; j += 1
    return [f[0][0], ''.join(out)]

def distance_two_rows(a, b):
    """Value only, O(min) space: prev = row i+1, cur = row i."""
    n, m = len(a), len(b)
    prev = [m - j for j in range(m + 1)]                    # row i = n
    for i in range(n - 1, -1, -1):
        cur = [0] * (m + 1)
        cur[m] = n - i
        for j in range(m - 1, -1, -1):
            cur[j] = min(1 + prev[j], 1 + cur[j + 1], prev[j + 1] + (a[i] != b[j]))
        prev = cur
    return prev[0]

def distance_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        return min(1 + f(i + 1, j), 1 + f(i, j + 1), f(i + 1, j + 1) + (a[i] != b[j]))
    return f(0, 0)

def apply_script(a, b, script):
    """Replay the script on a; asserts every M is a real match, every S a real difference, and everything is consumed."""
    i = j = 0; out = []
    for c in script:
        if c == 'D': i += 1
        elif c == 'I': out.append(b[j]); j += 1
        elif c == 'M': assert a[i] == b[j]; out.append(a[i]); i += 1; j += 1
        else: assert a[i] != b[j]; out.append(b[j]); i += 1; j += 1
    assert i == len(a) and j == len(b)
    return ''.join(out)

def brute(a, b):
    """Every valid script by plain recursion (len <= 5); smallest (cost, script)."""
    res = []
    def go(i, j, s, cost):
        if i == len(a) and j == len(b): res.append((cost, s)); return
        if i < len(a): go(i + 1, j, s + 'D', cost + 1)
        if j < len(b): go(i, j + 1, s + 'I', cost + 1)
        if i < len(a) and j < len(b):
            go(i + 1, j + 1, s + ('M' if a[i] == b[j] else 'S'), cost + (a[i] != b[j]))
    go(0, 0, '', 0)
    return list(min(res))

for a, b, want in [('horse', 'ros', [3, 'SMDMD']), ('ab', 'ba', [2, 'DMI']), ('', 'ab', [2, 'II']), ('abc', 'abc', [0, 'MMM']), ('kitten', 'sitting', [3, 'SMMMSMI'])]:
    r = edit_script(a, b)
    assert r == brute(a, b) == want and distance_two_rows(a, b) == distance_memo(a, b) == want[0], (a, b)
    assert apply_script(a, b, r[1]) == b
print('5 prompt examples ok')

f = suffix_table('horse', 'ros')
print("f (distance of a[i:], b[j:]) for a='horse' (rows), b='ros' (cols j=0..3):")
for i, row in enumerate(f):
    print(' ', ('horse-')[i], row)
print('script ->', edit_script('horse', 'ros'))

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 5)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 5)))
    r = edit_script(a, b)
    assert r == brute(a, b), (a, b)
    assert distance_two_rows(a, b) == distance_memo(a, b) == r[0]
    assert apply_script(a, b, r[1]) == b and sum(c != 'M' for c in r[1]) == r[0]
print('500 seeded random pairs (len 0..5, alphabet abc): script == enumeration, two-row == memo, script turns a into b, non-M count == distance')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        r = edit_script(a, b)
        assert r == brute(a, b) and apply_script(a, b, r[1]) == b and sum(c != 'M' for c in r[1]) == r[0]; cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok (script == smallest optimal, replay gives b, non-M letters == distance)')

# recursion and size
print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(300)); y = ''.join(random.choice('abcd') for _ in range(300))
t = time.perf_counter(); r = edit_script(x, y); dt = time.perf_counter() - t
assert r[0] == distance_two_rows(x, y) and apply_script(x, y, r[1]) == y
print('bottom-up 300 x 300: distance', r[0], 'script length', len(r[1]), '| memo 300 x 300 agrees:', distance_memo(x, y) == r[0])
try:
    distance_memo('a' * 600, 'b' * 600); print('memo 600 + 600 disjoint: ok')
except RecursionError:
    print('memo 600 + 600 disjoint: RecursionError')
assert edit_script('', '') == [0, ''] and edit_script('abc', '') == [3, 'DDD'] and edit_script('a', 'b') == [1, 'S']
print('edge asserts ok')
