import random
import sys
from functools import cache

random.seed(109)

def decode_ways(s):
    """dp[i] = ways to decode s[:i]. dp[0] = 1.
    + dp[i-1] if s[i-1] is '1'..'9' ; + dp[i-2] if s[i-2:i] is '10'..'26'. Two variables."""
    prev, cur = 0, 1                      # dp[i-2] (placeholder), dp[i-1] = dp[0]
    for i in range(1, len(s) + 1):
        new = 0
        if s[i - 1] != '0':
            new += cur
        if i >= 2 and '10' <= s[i - 2:i] <= '26':
            new += prev
        prev, cur = cur, new
    return cur

def table(s):
    dp = [1] + [0] * len(s)
    for i in range(1, len(s) + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]
    return dp

def memo(s):
    @cache
    def f(i):
        if i == len(s):
            return 1
        if s[i] == '0':
            return 0
        r = f(i + 1)
        if i + 1 < len(s) and 10 <= int(s[i:i + 2]) <= 26:
            r += f(i + 2)
        return r
    return f(0)

def brute(s):
    """Plain recursion: take one digit or two digits."""
    def f(rest):
        if rest == '':
            return 1
        if rest[0] == '0':
            return 0
        r = f(rest[1:])
        if len(rest) >= 2 and 10 <= int(rest[:2]) <= 26:
            r += f(rest[2:])
        return r
    return f(s)

ex = [('12', 2), ('226', 3), ('06', 0), ('10', 1), ('2101', 1), ('1' * 50, 20365011074)]
for s, want in ex:
    assert decode_ways(s) == memo(s) == table(s)[-1] == want, (s, decode_ways(s))
    if len(s) <= 25:
        assert brute(s) == want
print('6 prompt examples ok (the 50-digit one: 20365011074 = Fibonacci(51))')

print('s = 226  dp[0..3] =', table('226'))
print('s = 2101 dp[0..4] =', table('2101'))
print('s = 06   dp[0..2] =', table('06'))

for _ in range(1500):
    n = random.randint(1, 14)
    s = ''.join(random.choice('0123456789' if random.random() < 0.5 else '0126') for _ in range(n))
    assert decode_ways(s) == brute(s) == memo(s) == table(s)[-1], s
print('1500 seeded random digit strings (len 1..14): DP == plain recursion == memo == table')

# exhaustive: every digit string over {0,1,2,3,6,7} up to length 7 (the digits that matter for 10..26 boundaries)
import itertools
cnt = 0
for n in range(1, 8):
    top = 0
    for t in itertools.product('012367', repeat=n):
        s = ''.join(t)
        d = decode_ways(s)
        assert d == brute(s); cnt += 1
        top = max(top, d)
    assert top == decode_ways('1' * n)          # the all-ones string has the most decodings
print('exhaustive over alphabet 0,1,2,3,6,7 up to length 7:', cnt, 'strings ok; the all-ones string is the maximum at every length')

# claim: no modulus needed up to len 100: max is F(101) (all ones), about 5.7e20, python ints are exact
mx = decode_ways('1' * 100)
print('len 100 all ones ->', mx, '(exact big integer; no modulus needed)')
assert mx == 573147844013817084101
assert max(decode_ways(''.join(random.choice('12') for _ in range(100))) for _ in range(200)) <= mx

# zero handling
assert decode_ways('0') == 0 and decode_ways('00') == 0 and decode_ways('100') == 0 and decode_ways('30') == 0
assert decode_ways('27') == 1 and decode_ways('20') == 1 and decode_ways('1') == 1 and decode_ways('101') == 1
print('zero cases ok: 0, 00, 100, 30 -> 0;  20, 27, 101 -> 1')

# memoised depth <= len(s) <= 100, far below the limit; outside the limits it fails
print('memo on len 100 ->', memo('1' * 100) == mx, '; default limit', sys.getrecursionlimit())
try:
    memo('1' * 5000); print('memo len 5000: ok')
except RecursionError:
    print('memo len 5000 (outside the stated limit): RecursionError')
