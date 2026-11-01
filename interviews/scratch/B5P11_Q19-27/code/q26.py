import random, itertools, sys
from functools import lru_cache

random.seed(26)

def lrs(s):
    """LCS of s with itself where two positions may only match if i != j. Two rows."""
    n = len(s)
    prev = [0] * (n + 1)                                      # row i-1
    for i in range(1, n + 1):
        cur = [0] * (n + 1)                                   # row i, cur[0] = 0
        for j in range(1, n + 1):
            if s[i - 1] == s[j - 1] and i != j:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]

def lrs_table(s):
    n = len(s)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if s[i - 1] == s[j - 1] and i != j else max(dp[i - 1][j], dp[i][j - 1])
    return dp

def lcs_no_condition(s):
    """Without i != j: LCS(s, s) = len(s), the trivial answer."""
    n = len(s); prev = [0] * (n + 1)
    for i in range(1, n + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if s[i - 1] == s[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]

def brute(s):
    """All pairs of strictly increasing index sequences P, Q of equal length L with s[P] == s[Q] and P[k] != Q[k] for every k."""
    n = len(s)
    for L in range(n, 0, -1):
        for P in itertools.combinations(range(n), L):
            word = [s[i] for i in P]
            for Q in itertools.combinations(range(n), L):
                if all(a != b for a, b in zip(P, Q)) and [s[i] for i in Q] == word:
                    return L
    return 0

def brute_disjoint(s):
    """The OTHER reading (index sets must be disjoint), for comparison only."""
    n = len(s)
    for L in range(n // 2, 0, -1):
        for P in itertools.combinations(range(n), L):
            word = [s[i] for i in P]
            rest = [i for i in range(n) if i not in P]
            for Q in itertools.combinations(rest, L):
                if [s[i] for i in Q] == word:
                    return L
    return 0

def memo(s):
    n = len(s)
    @lru_cache(maxsize=None)
    def f(i, j):                                              # suffix form: s[i:], s[j:]
        if i == n or j == n: return 0
        if s[i] == s[j] and i != j: return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

# examples
for s, exp in [('aabebcdd', 3), ('abc', 0), ('aaa', 2), ('', 0), ('axxxy', 2)]:
    a, b, c, d = lrs(s), lrs_table(s)[-1][-1], brute(s), memo(s)
    assert a == b == c == d == exp, (s, a, b, c, d)
    print('example', repr(s), '->', a, '| without the i != j condition:', lcs_no_condition(s))

# hand table for 'aabebcdd' (row i = letter s[i-1], column j = letter s[j-1])
s = 'aabebcdd'
dp = lrs_table(s)
print('dp table for', s, '(rows i, columns j; match only if letters equal and i != j):')
print('      ' + '  '.join(['-'] + list(s)))
for i, row in enumerate(dp):
    print('  %s ' % ('-' if i == 0 else s[i - 1]), row)
print('answer dp[8][8] =', dp[-1][-1], '-> the repeated subsequence abd: positions 1,3,7 and 2,5,8 (1-indexed)')

# seeded cross-check, len <= 7
cases = nz = 0
for _ in range(500):
    alpha = random.choice(['a', 'ab', 'abc'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(0, 7)))
    exp = brute(s)
    assert lrs(s) == lrs_table(s)[-1][-1] == memo(s) == exp, s
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a non-zero answer', nz)
cnt = 0
for L in range(0, 9):
    for bits in range(1 << L):
        s = format(bits, '0%db' % L) if L else ''
        if L <= 7:
            assert lrs(s) == brute(s)
        else:
            assert lrs(s) == lrs_table(s)[-1][-1] == memo(s)
        cnt += 1
print('exhaustive binary strings len 0..8 checked:', cnt)

# the condition matters: without it the answer is len(s) on every string; and the 'disjoint index sets' reading is a different problem
assert all(lcs_no_condition(''.join(random.choice('abc') for _ in range(L))) == L for L in range(0, 30))
diff = sum(brute(s) != brute_disjoint(s) for s in (''.join(random.choice('ab') for _ in range(random.randint(0, 7))) for _ in range(300)))
print("'aaa': stated definition", brute('aaa'), "| disjoint-index reading", brute_disjoint('aaa'), '| the two readings differ on', diff, 'of 300 random strings')

# edge cases and max size
assert lrs('a') == 0 and lrs('aa') == 1 and lrs('ab') == 0 and lrs('a' * 1000) == 999
big = ''.join(random.choice('ab') for _ in range(1000))
print('n = 1000 random binary string:', lrs(big))
per = lrs('abc' * 300)
assert per >= 897                      # s[3:] against s[:-3] is a valid pair (shift by 3), so at least n - 3
print("'abc' * 300 (n = 900):", per)
print('edge asserts passed')

# recursion limit (observed): the memoised suffix recursion nests up to about 2n frames
print('recursion limit', sys.getrecursionlimit())
for n in (200, 1000):
    w = 'a' * n
    try:
        print('memoised n = %d ->' % n, memo(w) == lrs(w), '(bottom-up gives', lrs(w), ')')
    except RecursionError:
        print('memoised n = %d -> RecursionError (bottom-up gives %d)' % (n, lrs(w)))
