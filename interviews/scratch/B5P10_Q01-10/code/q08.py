import random
import string
import sys
from functools import cache

random.seed(108)

def word_break(s, word_dict, counter=None):
    """dp[i] = True if s[:i] can be segmented. dp[0] = True (empty prefix).
    dp[i] = any(dp[i - L] and s[i-L:i] in words) over the DISTINCT word lengths L <= i."""
    words = set(word_dict)
    lengths = sorted({len(w) for w in words})
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for L in lengths:
            if L > i:
                break
            if counter is not None:
                counter[0] += 1
            if dp[i - L] and s[i - L:i] in words:
                dp[i] = True
                break
    return dp[n]

def dp_row(s, word_dict):
    words = set(word_dict); dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(i >= len(w) and dp[i - len(w)] and s[i - len(w):i] == w for w in words)
    return dp

def memo(s, word_dict):
    words = set(word_dict)
    @cache
    def f(i):                      # can s[i:] be segmented?
        if i == len(s):
            return True
        return any(s.startswith(w, i) and f(i + len(w)) for w in words)
    return f(0)

def brute(s, word_dict):
    """Plain recursion over prefixes, no memo."""
    words = set(word_dict)
    def f(rest):
        if rest == '':
            return True
        return any(rest.startswith(w) and f(rest[len(w):]) for w in words)
    return f(s)

for s, wd, want in [('leetcode', ['leet', 'code'], True), ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], False),
                    ('aaaa', ['a', 'aa'], True), ('x', ['y'], False)]:
    assert word_break(s, wd) == brute(s, wd) == memo(s, wd) == want
print('4 prompt examples ok')

print('s = leetcode, words = [leet, code]; dp[0..8] =', dp_row('leetcode', ['leet', 'code']))
print('s = catsandog, words = [cats, dog, sand, and, cat]; dp[0..9] =', dp_row('catsandog', ['cats', 'dog', 'sand', 'and', 'cat']))

yes = 0
for _ in range(1500):
    alpha = 'ab' if random.random() < 0.7 else 'abc'
    words = sorted({''.join(random.choice(alpha) for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 5))})
    if random.random() < 0.5:                          # build a segmentable string half of the time
        s = ''.join(random.choice(words) for _ in range(random.randint(1, 5)))
        if random.random() < 0.4:
            s = s[:-1] + random.choice(alpha) if len(s) else s
    else:
        s = ''.join(random.choice(alpha) for _ in range(random.randint(1, 12)))
    s = s[:14] or 'a'
    a = word_break(s, words)
    assert a == brute(s, words) == memo(s, words) == dp_row(s, words)[-1], (s, words)
    yes += a
print(f'1500 seeded random cases: DP == plain recursion == memo ({yes} True, {1500 - yes} False)')

# check-count claim: at most n * (#distinct word lengths); count them, worst case = all false so no early break
for _ in range(300):
    n = random.randint(1, 200)
    words = sorted({''.join(random.choice('ab') for _ in range(random.randint(1, 20))) for _ in range(random.randint(1, 100))})
    s = ''.join(random.choice('ab') for _ in range(n))
    c = [0]; word_break(s, words, c)
    dl = len({len(w) for w in words})
    assert c[0] <= n * dl
print('substring checks <= n * (distinct word lengths) on 300 seeded cases with n up to 200, 100 words')

# worst case: nothing ever matches (early break never fires), 20 distinct word lengths: every position tries every length
n = 200; words = ['a' * k for k in range(1, 21)]; s = 'b' * n
c = [0]; r = word_break(s, words, c)
print('worst case n=200, 20 word lengths: result', r, ', checks =', c[0], ', bound n * 20 =', n * 20)
assert r is False and c[0] <= n * 20
# plain recursion blows up on the same input family (count calls on a smaller one)
calls = [0]
def counted(rest, words):
    calls[0] += 1
    return rest == '' or any(rest.startswith(w) and counted(rest[len(w):], words) for w in words)
counted('a' * 22 + 'b', ['a', 'aa', 'aaa']); print('plain recursion on a^22 b with [a, aa, aaa]:', calls[0], 'calls')

# recursion depth: memo depth <= len(s) <= 200, below the limit of 1000, so no RecursionError here
print('memoised depth is at most len(s) = 200; limit', sys.getrecursionlimit(), '->', memo('a' * 200, ['a']))
try:
    memo('a' * 5000, ['a']); print('memo n=5000: ok')
except RecursionError:
    print('memo n=5000 (outside the stated limits): RecursionError')
assert word_break('a' * 200, ['a']) is True
