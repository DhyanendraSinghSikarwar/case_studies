import random
from functools import cache

random.seed(101)
MOD = 10**9 + 7

def ways_bottom_up(n):
    """dp[i] = ways to reach step i. dp[0]=1, dp[1]=1, dp[i]=dp[i-1]+dp[i-2]. O(1) space: two variables."""
    a, b = 1, 1                      # a = dp[i-1], b = dp[i] starting at i = 1  (dp[0], dp[1])
    if n == 0:
        return 1
    for _ in range(n - 1):           # advance from dp[1] to dp[n]
        a, b = b, (a + b) % MOD
    return b

def ways_table(n):
    """Same recurrence with the full table (for the walk-through)."""
    dp = [0] * (n + 1)
    dp[0] = 1
    if n >= 1:
        dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = (dp[i - 1] + dp[i - 2]) % MOD
    return dp

def ways_memo(n):
    """Top-down with a cache: correct, but depth n."""
    @cache
    def f(i):
        if i <= 1:
            return 1
        return (f(i - 1) + f(i - 2)) % MOD
    return f(n)

def ways_plain(n):
    """Oracle: plain recursion, no memo, exponential. Returns the exact (unreduced) count."""
    if n <= 1:
        return 1
    return ways_plain(n - 1) + ways_plain(n - 2)

def fib(n):                          # F(1)=F(2)=1, exact, iterative
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def ways_doubling(n):
    """Extra: fast doubling, O(log n). ways(n) = F(n+1)."""
    def fd(k):                       # returns (F(k), F(k+1)) mod MOD
        if k == 0:
            return 0, 1
        a, b = fd(k >> 1)
        c = a * ((2 * b - a) % MOD) % MOD
        d = (a * a + b * b) % MOD
        return (d, (c + d) % MOD) if k & 1 else (c, d)
    return fd(n + 1)[0]              # recursion depth is only log2(n)

# --- prompt examples
for n, want in [(0, 1), (1, 1), (5, 8), (45, 836311896), (100000, 967618232)]:
    assert ways_bottom_up(n) == want, (n, ways_bottom_up(n))
    assert ways_doubling(n) == want
print('5 prompt examples ok (n = 0, 1, 5, 45, 100000)')

# --- table walk-through for n = 5
print('table n=5: i  ', list(range(6)))
print('           dp ', ways_table(5))

# --- oracle cross-check: every n in 0..20, plus seeded random draws
for n in range(21):
    assert ways_bottom_up(n) == ways_plain(n) % MOD == ways_memo(n) == ways_table(n)[n]
for _ in range(300):
    n = random.randint(0, 20)
    assert ways_bottom_up(n) == ways_plain(n) % MOD
print('cross-check vs plain recursion: all n in 0..20 and 300 seeded draws agree')

# --- shifted Fibonacci claim, exact integers
for n in range(0, 300):
    assert ways_bottom_up(n) == fib(n + 1) % MOD
assert fib(46) == 1836311903 and 1836311903 % MOD == 836311896   # n=45 example, reduced
print('ways(n) == Fibonacci(n+1) for n in 0..299 (F(1)=F(2)=1); n=45: F(46) = 1836311903 -> mod = 836311896')

# --- fast doubling agrees with the loop on seeded large n
for _ in range(50):
    n = random.randint(0, 10**5)
    assert ways_doubling(n) == ways_bottom_up(n)
print('fast doubling == linear loop on 50 seeded n up to 10^5')

# --- number of calls made by the plain recursion (why it is exponential)
calls = [0]
def counted(n):
    calls[0] += 1
    return 1 if n <= 1 else counted(n - 1) + counted(n - 2)
for n in (10, 20, 25):
    calls[0] = 0; counted(n)
    print(f'plain recursion n={n}: {calls[0]} calls (2*F(n+1) - 1 = {2 * fib(n + 1) - 1})')
    assert calls[0] == 2 * fib(n + 1) - 1

# --- recursion limit: memoised recursion at large n fails under the default limit (1000)
import sys
print('default recursion limit:', sys.getrecursionlimit())
for n in (500, 5000, 100000):
    try:
        ways_memo(n)
        print(f'memoised n={n}: ok')
    except RecursionError:
        print(f'memoised n={n}: RecursionError')
print('bottom-up n=100000 ->', ways_bottom_up(100000))
