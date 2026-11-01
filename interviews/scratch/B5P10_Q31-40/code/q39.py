import itertools
import random

random.seed(39)

def ones_zeroes(strs, m, n):
    """dp[a][b] = largest subset of the strings seen so far using at most a zeros and b ones."""
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        z = s.count('0')
        o = len(s) - z
        for a in range(m, z - 1, -1):              # both loops DOWNWARD: each string is used at most once
            for b in range(n, o - 1, -1):
                dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    return dp[m][n]

def upward_bug(strs, m, n):
    """WRONG: upward loops let a string be reused (it behaves like an unbounded item)."""
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        z = s.count('0')
        o = len(s) - z
        for a in range(z, m + 1):
            for b in range(o, n + 1):
                dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    return dp[m][n]

def brute(strs, m, n):
    k, best = len(strs), 0
    for mask in range(1 << k):
        ch = [strs[i] for i in range(k) if mask >> i & 1]
        if sum(s.count('0') for s in ch) <= m and sum(s.count('1') for s in ch) <= n:
            best = max(best, len(ch))
    return best

# ---- examples from the prompt
assert ones_zeroes(['10', '0001', '111001', '1', '0'], 5, 3) == 4
assert ones_zeroes(['10', '0', '1'], 1, 1) == 2
assert ones_zeroes(['0'], 0, 5) == 0
print('examples ok')

# ---- table for the first example: dp after each string (rows a = zeros allowed 0..5, columns b = ones allowed 0..3)
strs = ['10', '0001', '111001', '1', '0']
m, n = 5, 3
dp = [[0] * (n + 1) for _ in range(m + 1)]
for s in strs:
    z = s.count('0'); o = len(s) - z
    for a in range(m, z - 1, -1):
        for b in range(n, o - 1, -1):
            dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    print(f'after {s!r} (zeros {z}, ones {o}):', dp)
assert dp[m][n] == 4

# ---- seeded cross-check against the enumeration of all subsets (len <= 12)
cases = diff_upward = 0
for _ in range(500):
    k = random.randint(1, 12)
    strs = [''.join(random.choice('01') for _ in range(random.randint(1, 5))) for _ in range(k)]
    m, n = random.randint(0, 8), random.randint(0, 8)
    assert ones_zeroes(strs, m, n) == brute(strs, m, n), (strs, m, n)
    if upward_bug(strs, m, n) != ones_zeroes(strs, m, n):
        diff_upward += 1
    cases += 1
print('cross-check passed on', cases, 'cases; the upward-loop version was wrong on', diff_upward)
print("upward on ['0'], m=3, n=0:", upward_bug(['0'], 3, 0), '(true answer', ones_zeroes(['0'], 3, 0), ')')

# ---- edge cases and full size
assert ones_zeroes(['0'], 0, 5) == 0 and ones_zeroes(['1'], 5, 0) == 0 and ones_zeroes(['01'], 1, 1) == 1
assert ones_zeroes(['0', '0', '0'], 2, 0) == 2
big = [''.join(random.choice('01') for _ in range(random.randint(1, 100))) for _ in range(100)]
print('len = 100, m = n = 100:', ones_zeroes(big, 100, 100))
print('edge cases ok')
