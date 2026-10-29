import random
import sys
from bisect import bisect_left
from functools import cache

random.seed(107)

def lis_tails(nums):
    """Patience sorting. tails[k] = smallest last value of a strictly increasing subsequence of length k+1.
    Replace the first entry >= x (bisect_left), or append when x is bigger than all."""
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return [len(tails), tails]

def lis_n2(nums):
    """O(n^2) DP: dp[i] = length of the longest strictly increasing subsequence ENDING at i."""
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp, default=0), dp

def lis_memo(nums):
    n = len(nums)
    @cache
    def f(i):                                   # LIS ending at i
        best = 1
        for j in range(i - 1, -1, -1):
            if nums[j] < nums[i]:
                best = max(best, f(j) + 1)
        return best
    return max((f(i) for i in range(n - 1, -1, -1)), default=0)   # start from the end: deepest chain first

def brute(nums):
    """Enumerate every subsequence (len <= 12). For each strictly increasing one, record the smallest last value per length."""
    n = len(nums)
    best_last = {}                              # length -> smallest last value
    for mask in range(1, 1 << n):
        sub = [nums[i] for i in range(n) if mask >> i & 1]
        if all(sub[k] < sub[k + 1] for k in range(len(sub) - 1)):
            L = len(sub)
            if L not in best_last or sub[-1] < best_last[L]:
                best_last[L] = sub[-1]
    if not best_last:
        return [0, []]
    L = max(best_last)
    return [L, [best_last[k] for k in range(1, L + 1)]]

def piles(nums):
    """Patience sorting as cards: put x on the leftmost pile whose top is >= x, else open a new pile."""
    tops = []
    for x in nums:
        for k, t in enumerate(tops):
            if t >= x:
                tops[k] = x; break
        else:
            tops.append(x)
    return tops

def is_subseq(sub, nums):
    it = iter(nums)
    return all(any(x == y for y in it) for x in sub)

for a, want in [([10, 9, 2, 5, 3, 7, 101, 18], [4, [2, 3, 7, 18]]), ([0, 1, 0, 3, 2, 3], [4, [0, 1, 2, 3]]),
                ([7, 7, 7], [1, [7]]), ([], [0, []]), ([4, 10, 4, 3, 8, 9], [3, [3, 8, 9]])]:
    assert lis_tails(a) == brute(a) == want, a
    assert lis_n2(a)[0] == want[0] == lis_memo(a)
print('5 prompt examples ok')

a = [10, 9, 2, 5, 3, 7, 101, 18]
t = []
print('x     tails after x   (nums =', a, ')')
for x in a:
    i = bisect_left(t, x)
    if i == len(t): t.append(x)
    else: t[i] = x
    print(f'{x:<5} {t}')
print('O(n^2) table (LIS ending at i):', lis_n2(a)[1])

for _ in range(500):
    n = random.randint(0, 12)
    a = [random.randint(-6, 6) for _ in range(n)]
    got = lis_tails(a)
    assert got == brute(a), a
    assert lis_n2(a)[0] == got[0] == lis_memo(a)
    assert all(got[1][k] < got[1][k + 1] for k in range(len(got[1]) - 1))      # tails strictly increasing
    assert piles(a) == got[1]                                                   # piles == tails
    # prefix property: tails after every prefix equals the brute force on that prefix
    for p in range(0, n + 1, 4):
        assert lis_tails(a[:p]) == brute(a[:p])
print('500 seeded random lists (len 0..12, values -6..6): tails, length, piles, O(n^2) DP, memo all agree with subsequence enumeration')

# tails itself is generally NOT a subsequence of nums, hence not an LIS
cnt = 0; tot = 0; ex = None
for _ in range(2000):
    a = [random.randint(0, 9) for _ in range(random.randint(1, 8))]
    tot += 1
    tl = lis_tails(a)[1]
    if not is_subseq(tl, a):
        cnt += 1
        ex = ex or a
print(f'tails is not a subsequence of nums in {cnt} of {tot} seeded lists; first example {ex} -> tails {lis_tails(ex)[1]}')
assert lis_tails([2, 5, 3, 1]) == [2, [1, 3]]       # 1 comes after 3 in nums, so [1, 3] is not a subsequence

# larger: O(n^2) vs O(n log n) lengths
for _ in range(5):
    a = [random.randint(-10**9, 10**9) for _ in range(2500)]
    assert lis_tails(a)[0] == lis_n2(a)[0]
print('5 seeded lists of length 2500 (O(n^2) DP vs O(n log n) length): equal')

# sorted input is the O(n) piles / worst depth case
for n_ in (10**5,):
    inc = list(range(n_)); dec = list(range(n_, 0, -1))
    assert lis_tails(inc)[0] == n_ and lis_tails(dec)[0] == 1 and lis_tails(dec)[1] == [1]
big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
print('n = 10^5 random: LIS length', lis_tails(big)[0], ', strictly increasing 0..99999 -> 100000, strictly decreasing -> 1')

# recursion limit for the memoised O(n^2) version
print('default recursion limit:', sys.getrecursionlimit())
for n_ in (300, 1500):
    try:
        lis_memo(list(range(n_)))
        print(f'memoised LIS on increasing list n={n_}: ok')
    except RecursionError:
        print(f'memoised LIS on increasing list n={n_}: RecursionError')
