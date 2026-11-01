import random, itertools, sys
from math import comb
from functools import lru_cache

random.seed(21)
MOD = 10**9 + 7

def table(s, t):
    """2D: dp[i][j] = ways to spell t[:j] from s[:i]."""
    dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
    for i in range(len(s) + 1):
        dp[i][0] = 1                                   # empty t: exactly one way (choose nothing)
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            dp[i][j] = dp[i - 1][j]                    # skip s[i-1]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]           # use s[i-1] as t[j-1]
    return dp

def one_row(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):                 # j DESCENDING: dp[j-1] must still be the previous row
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]

def one_row_ascending_wrong(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(1, len(t) + 1):                 # ascending: dp[j-1] is already the NEW row, so s[i-1] is reused
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]

def one_row_mod(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                dp[j] = (dp[j] + dp[j - 1]) % MOD      # addition only: (a + b) % M == ((a % M) + (b % M)) % M
    return dp[-1]

def brute(s, t):
    return sum(1 for idx in itertools.combinations(range(len(s)), len(t)) if all(s[i] == c for i, c in zip(idx, t)))

def memo(s, t):
    @lru_cache(maxsize=None)
    def f(i, j):
        if j == len(t): return 1
        if i == len(s): return 0
        r = f(i + 1, j)
        if s[i] == t[j]: r += f(i + 1, j + 1)
        return r
    return f(0, 0)

# examples
for s, t, exp in [('rabbbit', 'rabbit', 3), ('babgbag', 'bag', 5), ('abc', '', 1), ('a', 'aa', 0), ('aaaa', 'aa', 6)]:
    a, b, c = one_row(s, t), table(s, t)[-1][-1], brute(s, t)
    assert a == b == c == exp == memo(s, t), (s, t, a, b, c)
    print('example', repr(s), repr(t), '->', a)

# hand table, first example
s, t = 'rabbbit', 'rabbit'
dp = table(s, t)
print('2D table dp[i][j] for s=rabbbit, t=rabbit (rows i = letters of s used, columns j = letters of t):')
print('        ' + '  '.join(['-'] + list(t)))
for i, row in enumerate(dp):
    print('  %s  ' % ('-' if i == 0 else s[i - 1]), row)
# one row, printed after each letter of s
row = [1] + [0] * len(t)
print('one row after each letter of s:')
for ch in s:
    for j in range(len(t), 0, -1):
        if t[j - 1] == ch: row[j] += row[j - 1]
    print('  after', ch, row)

# seeded cross-check, len(s) <= 10
cases = nz = 0
for _ in range(600):
    alpha = random.choice(['ab', 'abc', 'a'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(0, 10)))
    t = ''.join(random.choice(alpha) for _ in range(random.randint(0, 5)))
    exp = brute(s, t)
    assert one_row(s, t) == table(s, t)[-1][-1] == one_row_mod(s, t) == memo(s, t) == exp, (s, t)
    cases += 1; nz += exp > 0
print('cross-check cases', cases, '| with a positive count', nz)
wrong = sum(one_row_ascending_wrong(s, t) != brute(s, t)
            for s, t in [(''.join(random.choice('ab') for _ in range(random.randint(0, 8))), ''.join(random.choice('ab') for _ in range(random.randint(0, 4)))) for _ in range(300)])
print('ascending inner loop gave a wrong answer on', wrong, 'of 300 random cases; for s=aaaa, t=aa it returns', one_row_ascending_wrong('aaaa', 'aa'), 'instead of 6')

# closed forms and the modulus
assert one_row('a' * 50, 'a' * 25) == comb(50, 25)
assert one_row('a' * 1000, 'a' * 500) == comb(1000, 500)
big = comb(1000, 500)
print('C(1000, 500) has', len(str(big)), 'digits; mod version equals exact % M:', one_row_mod('a' * 1000, 'a' * 500) == big % MOD)
for _ in range(200):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 60))); t = ''.join(random.choice('ab') for _ in range(random.randint(0, 6)))
    assert one_row_mod(s, t) == one_row(s, t) % MOD

# recursion limit (observed)
print('recursion limit', sys.getrecursionlimit())
for n, m in ((300, 150), (1000, 500)):
    s, t = 'a' * n, 'a' * m
    try:
        print('memoised s=%d, t=%d ->' % (n, m), memo(s, t) == one_row(s, t))
    except RecursionError:
        print('memoised s=%d, t=%d -> RecursionError (bottom-up is fine)' % (n, m))

# edge cases
assert one_row('', '') == 1 and one_row('', 'a') == 0 and one_row('abc', '') == 1 and one_row('a', 'aa') == 0
assert one_row('abc', 'abcd') == 0
print('edge asserts passed')
