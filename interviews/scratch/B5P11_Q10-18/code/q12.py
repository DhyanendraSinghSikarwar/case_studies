import random
import sys
from functools import lru_cache

random.seed(1212)

def count_table(s):
    """Full interval table. dp[i][j] = s[i..j] is a palindrome. i DESCENDING, j ASCENDING so dp[i+1][j-1] is ready."""
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[i][j] = s[i] == s[j] and (j - i < 3 or dp[i + 1][j - 1])
            cnt += dp[i][j]
    return cnt, dp

def count_row(s):
    """ONE row. dp[j] means 'is s[i..j] a palindrome' for the current i. j DESCENDING so dp[j-1] still holds row i+1."""
    n = len(s)
    dp = [False] * n
    cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i - 1, -1):
            dp[j] = s[i] == s[j] and (j - i < 3 or dp[j - 1])
            cnt += dp[j]
    return cnt

def count_center(s):
    """Expand around each of the 2n-1 centres (Part 3 Q9 idea)."""
    n, cnt = len(s), 0
    for c in range(2 * n - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < n and s[l] == s[r]:
            cnt += 1; l -= 1; r += 1
    return cnt

def brute(s):
    return sum(s[i:j] == s[i:j][::-1] for i in range(len(s)) for j in range(i + 1, len(s) + 1))

def count_memo(s):
    @lru_cache(maxsize=None)
    def pal(i, j):
        if i >= j: return True
        return s[i] == s[j] and pal(i + 1, j - 1)
    return sum(pal(i, j) for i in range(len(s)) for j in range(i, len(s)))

for s, want in [('abc', 3), ('aaa', 6), ('abba', 6), ('a', 1), ('abacaba', 12)]:
    assert count_table(s)[0] == count_row(s) == count_center(s) == brute(s) == want, s
print('5 prompt examples ok')

cnt, dp = count_table('abba')
print("dp for s='abba' (row i, col j, T = palindrome):")
print('     ', ' '.join('abba'))
for i, row in enumerate(dp):
    print('  ', 'abba'[i], ' '.join('T' if v else '.' for v in row))
print('count =', cnt)

for _ in range(1000):
    s = ''.join(random.choice('ab') for _ in range(random.randint(1, 12)))
    assert count_table(s)[0] == count_row(s) == count_center(s) == brute(s) == count_memo(s), s
print('1000 seeded random strings (len 1..12, alphabet ab): table == one row == centres == enumeration == memo')

# what breaks if the one-row inner loop runs ASCENDING: dp[j-1] would already be row i, not row i+1
def bad_row(s):
    n = len(s); dp = [False] * n; cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[j] = s[i] == s[j] and (j - i < 3 or dp[j - 1]); cnt += dp[j]
    return cnt
wrong = sum(bad_row(s) != brute(s) for s in (''.join(random.choice('ab') for _ in range(8)) for _ in range(300)))
print('ascending inner loop in the one-row version is wrong on', wrong, 'of 300 random strings')
assert wrong > 0

big = 'a' * 1000
print('n = 1000 all a:', count_row(big), '== n(n+1)/2 =', 1000 * 1001 // 2)
assert count_row(big) == count_table(big)[0] == count_center(big) == 500500
rnd = ''.join(random.choice('ab') for _ in range(1000))
assert count_row(rnd) == count_center(rnd)
print('random 1000 over {a,b}: DP row == centres ==', count_row(rnd))

# memoised version: recursion depth is only ~n/2 per call chain, but the outer loop makes n^2/2 cache entries
print('recursion limit:', sys.getrecursionlimit(), '| memo n=1000 all a:', end=' ')
try:
    print(count_memo(big))
except RecursionError:
    print('RecursionError')
print('memo n=2100 all a (depth about 1050):', end=' ')
try:
    count_memo('a' * 2100); print('ok')
except RecursionError:
    print('RecursionError')
assert count_center('') == 0
print('edge asserts ok')
