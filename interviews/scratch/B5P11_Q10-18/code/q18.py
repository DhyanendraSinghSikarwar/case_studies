import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1818)

def weight_table(s1, s2):
    """w[i][j] = maximum total ASCII weight of a common subsequence of s1[i:] and s2[j:]."""
    n, m = len(s1), len(s2)
    w = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s1[i] == s2[j]:
                w[i][j] = ord(s1[i]) + w[i + 1][j + 1]
            else:
                w[i][j] = max(w[i + 1][j], w[i][j + 1])
    return w

def min_delete_sum(s1, s2):
    """total ASCII of both strings - 2 * (best common weight). Two rows."""
    n, m = len(s1), len(s2)
    prev = [0] * (m + 1)
    for i in range(n - 1, -1, -1):
        cur = [0] * (m + 1)
        for j in range(m - 1, -1, -1):
            if s1[i] == s2[j]:
                cur[j] = ord(s1[i]) + prev[j + 1]
            else:
                cur[j] = max(prev[j], cur[j + 1])
        prev = cur
    return sum(map(ord, s1)) + sum(map(ord, s2)) - 2 * prev[0]

def direct_delete_table(s1, s2):
    """The cost DP itself (no reduction): d[i][j] = min cost to make s1[i:] and s2[j:] equal."""
    n, m = len(s1), len(s2)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n: d[i][j] = sum(map(ord, s2[j:]))
            elif j == m: d[i][j] = sum(map(ord, s1[i:]))
            elif s1[i] == s2[j]: d[i][j] = d[i + 1][j + 1]
            else: d[i][j] = min(ord(s1[i]) + d[i + 1][j], ord(s2[j]) + d[i][j + 1])
    return d

def min_delete_memo(s1, s2):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(s1): return sum(map(ord, s2[j:]))
        if j == len(s2): return sum(map(ord, s1[i:]))
        if s1[i] == s2[j]: return f(i + 1, j + 1)
        return min(ord(s1[i]) + f(i + 1, j), ord(s2[j]) + f(i, j + 1))
    return f(0, 0)

def brute(s1, s2):
    """Plain recursion, no memo (len <= 7)."""
    def f(i, j):
        if i == len(s1): return sum(map(ord, s2[j:]))
        if j == len(s2): return sum(map(ord, s1[i:]))
        if s1[i] == s2[j]: return f(i + 1, j + 1)
        return min(ord(s1[i]) + f(i + 1, j), ord(s2[j]) + f(i, j + 1))
    return f(0, 0)

for a, b, want in [('sea', 'eat', 231), ('delete', 'leet', 403), ('', 'ab', 195), ('abc', 'abc', 0)]:
    assert min_delete_sum(a, b) == brute(a, b) == min_delete_memo(a, b) == direct_delete_table(a, b)[0][0] == want, (a, b)
print('4 prompt examples ok')

w = weight_table('sea', 'eat')
print("w (best common ASCII weight of s1[i:], s2[j:]) for s1='sea' (rows), s2='eat' (cols j=0..3):")
for i, row in enumerate(w):
    print(' ', 'sea-'[i], row)
tot = sum(map(ord, 'sea')) + sum(map(ord, 'eat'))
print('total ASCII =', tot, '| best common weight =', w[0][0], '| answer =', tot, '-', 2, '*', w[0][0], '=', tot - 2 * w[0][0])

for _ in range(1000):
    a = ''.join(random.choice('abcz') for _ in range(random.randint(0, 7)))
    b = ''.join(random.choice('abcz') for _ in range(random.randint(0, 7)))
    r = min_delete_sum(a, b)
    assert r == brute(a, b) == min_delete_memo(a, b) == direct_delete_table(a, b)[0][0], (a, b)
    assert r == sum(map(ord, a)) + sum(map(ord, b)) - 2 * weight_table(a, b)[0][0]
print('1000 seeded random pairs (len 0..7, alphabet abcz): two-row identity == plain recursion == memo == direct cost table')

cnt = 0
words = [''.join(x) for n in range(5) for x in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert min_delete_sum(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# why weight and not length: with lowercase letters a LONGER common subsequence can weigh LESS (5 x 'a' = 485 < 4 x 'z' = 488)
a, b = 'aaaaazzzz', 'zzzzaaaaa'
tot = sum(map(ord, a)) + sum(map(ord, b))
print("s1='aaaaazzzz', s2='zzzzaaaaa': longest common is 'aaaaa' (len 5, weight 485); best weight keeps 'zzzz' (len 4, weight 488)")
print('  answer by weight:', min_delete_sum(a, b), '== plain recursion', brute(a, b), '| a length-based shortcut would say', tot - 2 * 485)
assert min_delete_sum(a, b) == tot - 2 * 488 < tot - 2 * 485

print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcdefghij') for _ in range(1000)); y = ''.join(random.choice('abcdefghij') for _ in range(1000))
t = time.perf_counter(); r = min_delete_sum(x, y); dt = time.perf_counter() - t
assert r == sum(map(ord, x)) + sum(map(ord, y)) - 2 * weight_table(x, y)[0][0]
print('bottom-up 1000 x 1000 random:', r, '| sandbox time under 5 s:', dt < 5)
print('bottom-up disjoint 1000 + 1000 ->', min_delete_sum('a' * 1000, 'b' * 1000), '(= 97000 + 98000)')
print('memoised, two random 300-letter strings agrees:', min_delete_memo(x[:300], y[:300]) == min_delete_sum(x[:300], y[:300]))
try:
    min_delete_memo('a' * 1000, 'b' * 1000); print('memoised disjoint 1000 + 1000: ok')
except RecursionError:
    print('memoised disjoint 1000 + 1000: RecursionError')

assert min_delete_sum('', '') == 0 and min_delete_sum('a', 'a') == 0 and min_delete_sum('a', 'b') == 195 and min_delete_sum('z', '') == 122
print('edge asserts ok')
