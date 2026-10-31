import random, sys, bisect
from functools import cache

random.seed(28)

def count_lis(nums):
    """O(n^2). length[i] = longest strictly increasing subsequence ENDING at i, ways[i] = how many (by position)."""
    n = len(nums)
    if n == 0: return [0, 0]
    length = [1] * n; ways = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i], ways[i] = length[j] + 1, ways[j]      # strictly longer: replace the count
                elif length[j] + 1 == length[i]:
                    ways[i] += ways[j]                               # equally long: add the counts
    L = max(length)
    return [L, sum(w for l, w in zip(length, ways) if l == L)]

def tables(nums):
    n = len(nums); length = [1] * n; ways = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]: length[i], ways[i] = length[j] + 1, ways[j]
                elif length[j] + 1 == length[i]: ways[i] += ways[j]
    return length, ways

def lis_len_bisect(nums):
    tails = []
    for x in nums:
        k = bisect.bisect_left(tails, x)
        if k == len(tails): tails.append(x)
        else: tails[k] = x
    return len(tails)

def memo(nums):
    n = len(nums)
    @cache
    def f(i):                       # (length ending at i, ways)
        best, w = 1, 1
        for j in range(i):
            if nums[j] < nums[i]:
                l, c = f(j)
                if l + 1 > best: best, w = l + 1, c
                elif l + 1 == best: w += c
        return best, w
    if n == 0: return [0, 0]
    res = [f(i) for i in range(n)]       # forward order keeps the recursion shallow in this test; see text
    L = max(l for l, _ in res)
    return [L, sum(c for l, c in res if l == L)]

def brute(nums):
    n = len(nums); best = 0; cnt = 0
    for m in range(1, 1 << n):
        v = [nums[i] for i in range(n) if m >> i & 1]
        if all(v[i] < v[i + 1] for i in range(len(v) - 1)):
            if len(v) > best: best, cnt = len(v), 1
            elif len(v) == best: cnt += 1
    return [best, cnt] if n else [0, 0]

for nums, exp in [([1, 3, 5, 4, 7], [4, 2]), ([2, 2, 2, 2, 2], [1, 5]), ([], [0, 0]),
                  ([1, 2, 4, 3, 5, 4, 7, 2], [5, 3]), ([5, 4, 3], [1, 3])]:
    assert count_lis(nums) == brute(nums) == memo(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [1, 3, 5, 4, 7]
ln, wy = tables(nums)
print('i   x  length ways')
for i, x in enumerate(nums): print(f'{i}  {x:2d}  {ln[i]:5d} {wy[i]:4d}')
print('L =', max(ln), '| count = sum of ways where length == L =', sum(w for l, w in zip(ln, wy) if l == max(ln)))

cases = 0; bisect_agree = 0
for _ in range(700):
    n = random.randint(0, 12); l = [random.randint(-4, 6) for _ in range(n)]
    assert count_lis(l) == brute(l) == memo(l), l
    assert lis_len_bisect(l) == count_lis(l)[0]
    cases += 1
print('cross-check cases', cases, '| bisect_left length equals L on all (it gives the length, not the count)')

big = [random.randint(-10**6, 10**6) for _ in range(2000)]
print('n = 2000 random:', count_lis(big))
inc = list(range(2000))
print('n = 2000 increasing:', count_lis(inc))
print('n = 2000 all equal:', count_lis([7] * 2000))
print('limit =', sys.getrecursionlimit())
def top_down(seq, order):
    @cache
    def g(i):
        best, w = 1, 1
        for j in order(i):
            if seq[j] < seq[i]:
                l, c = g(j)
                if l + 1 > best: best, w = l + 1, c
                elif l + 1 == best: w += c
        return best, w
    return g
for name, order in (('j ascending', lambda i: range(i)), ('j descending', lambda i: reversed(range(i)))):
    try:
        top_down(inc, order)(1999); print('top-down, inner loop', name, ': ok on 0..1999 increasing')
    except RecursionError:
        print('top-down, inner loop', name, ': RecursionError on 0..1999 increasing')
assert count_lis([9]) == [1, 1] and count_lis([1, 2]) == [2, 1]
print('edge asserts passed')
