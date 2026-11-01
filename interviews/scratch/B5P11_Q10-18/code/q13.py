import itertools
import random
import sys
from functools import lru_cache

random.seed(1313)

def interleave_table(s1, s2, s3):
    """dp[i][j] = first i letters of s1 and first j of s2 interleave into the first i + j of s3."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return None
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for i in range(m + 1):
        for j in range(n + 1):
            if i and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = True
            if j and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = True
    return dp

def interleave(s1, s2, s3):
    """One row of length len(s2) + 1. Before the update dp[j] is (i-1, j); dp[j-1] is already (i, j-1)."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [False] * (n + 1)
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                dp[0] = True
                continue
            ok = False
            if i and dp[j] and s1[i - 1] == s3[i + j - 1]:        # last letter came from s1
                ok = True
            if j and dp[j - 1] and s2[j - 1] == s3[i + j - 1]:    # last letter came from s2
                ok = True
            dp[j] = ok          # overwrites (i-1, j); for i = 0 the old value is not read (guarded by `i and`)
    return dp[n]

def interleave_memo(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    @lru_cache(maxsize=None)
    def f(i, j):
        k = i + j
        if k == len(s3):
            return True
        return (i < len(s1) and s1[i] == s3[k] and f(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and f(i, j + 1))
    return f(0, 0)

def brute(s1, s2, s3):
    """Plain recursion, no memo (len(s1), len(s2) <= 6)."""
    def f(i, j):
        k = i + j
        if k == len(s3):
            return i == len(s1) and j == len(s2)
        return (i < len(s1) and s1[i] == s3[k] and f(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and f(i, j + 1))
    return len(s1) + len(s2) == len(s3) and f(0, 0)

for a, b, c, want in [('aabcc', 'dbbca', 'aadbbcbcac', True), ('aabcc', 'dbbca', 'aadbbbaccc', False), ('', '', '', True), ('a', '', 'b', False)]:
    assert interleave(a, b, c) == interleave_memo(a, b, c) == brute(a, b, c) == want, (a, b, c)
print('4 prompt examples ok')

dp = interleave_table('aabcc', 'dbbca', 'aadbbcbcac')
print("dp for s1='aabcc' (rows i=0..5), s2='dbbca' (cols j=0..5), T = true:")
print('      ', ' '.join('-dbbca'))
for i, row in enumerate(dp):
    print('  ', '-aabcc'[i], ' '.join('T' if v else '.' for v in row))

true_cases = 0
for _ in range(2000):
    s1 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    s2 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    if random.random() < 0.5:                       # build a true interleaving
        pool, i, j, out = (s1, s2), 0, 0, []
        while i < len(s1) or j < len(s2):
            if j == len(s2) or (i < len(s1) and random.random() < 0.5): out.append(s1[i]); i += 1
            else: out.append(s2[j]); j += 1
        s3 = ''.join(out)
        if random.random() < 0.3 and s3:           # corrupt one letter sometimes
            k = random.randrange(len(s3)); s3 = s3[:k] + random.choice('abc') + s3[k + 1:]
    else:
        s3 = ''.join(random.choice('abc') for _ in range(random.randint(0, 12)))
    r = interleave(s1, s2, s3)
    assert r == brute(s1, s2, s3) == interleave_memo(s1, s2, s3), (s1, s2, s3)
    assert (interleave_table(s1, s2, s3) or [[False]])[-1][-1] == r
    true_cases += r
print('2000 seeded random triples: one row == plain recursion == memo == table; True in', true_cases, 'of 2000 (both answers occur)')
assert 0 < true_cases < 2000

cnt = 0
for l1 in range(4):
    for l2 in range(4):
        for s1 in itertools.product('ab', repeat=l1):
            for s2 in itertools.product('ab', repeat=l2):
                for s3 in itertools.product('ab', repeat=l1 + l2):
                    a, b, c = ''.join(s1), ''.join(s2), ''.join(s3)
                    assert interleave(a, b, c) == brute(a, b, c); cnt += 1
print('exhaustive over {a,b}, len(s1), len(s2) <= 3, len(s3) = len(s1) + len(s2):', cnt, 'ok')

# maximum size and recursion depth (the memo recursion depth is len(s3) <= 200)
print('recursion limit:', sys.getrecursionlimit())
x, y = 'a' * 100, 'a' * 100
print('max size 100 + 100 -> 200, all a: row', interleave(x, y, 'a' * 200), '| memo (depth 200)', interleave_memo(x, y, 'a' * 200))
x = ''.join(random.choice('ab') for _ in range(100)); y = ''.join(random.choice('ab') for _ in range(100))
z = ''.join(x[i // 2] if i % 2 == 0 else y[i // 2] for i in range(200))      # strict alternation is a valid interleaving
assert interleave(x, y, z) and interleave_memo(x, y, z)
print('alternating merge of two random 100-letter strings:', interleave(x, y, z))

assert interleave('', 'abc', 'abc') and interleave('abc', '', 'abc') and not interleave('a', 'b', 'a')
assert not interleave('a', 'b', 'abc')
print('edge asserts ok')
