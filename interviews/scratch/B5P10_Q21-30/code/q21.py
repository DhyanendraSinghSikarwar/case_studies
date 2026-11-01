import random, sys
from functools import cache

random.seed(21)

def count_both(nums, target):
    """Bottom-up. ordered: target loop OUTER, coin loop inner. unordered: coin loop OUTER, target inner."""
    ordered = [1] + [0] * target
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                ordered[t] += ordered[t - x]
    unordered = [1] + [0] * target
    for x in nums:
        for t in range(x, target + 1):
            unordered[t] += unordered[t - x]
    return [ordered[target], unordered[target]]

def swapped(nums, target):
    """The classic swap: each loop order with the other count's name."""
    a = [1] + [0] * target            # coin outer, target inner -> this is the UNORDERED count
    for x in nums:
        for t in range(x, target + 1):
            a[t] += a[t - x]
    b = [1] + [0] * target            # target outer, coin inner -> this is the ORDERED count
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                b[t] += b[t - x]
    return a[target], b[target]

def memo_ordered(nums, target):
    @cache
    def f(rem):
        if rem == 0:
            return 1
        return sum(f(rem - x) for x in nums if x <= rem)
    return f(target)

def brute(nums, target):
    """Enumerate every sequence (ordered) and every non-decreasing sequence = multiset (unordered)."""
    seqs = []
    def rec(rem, cur):
        if rem == 0:
            seqs.append(tuple(cur)); return
        for x in nums:
            if x <= rem:
                cur.append(x); rec(rem - x, cur); cur.pop()
    rec(target, [])
    ms = set()
    for s in seqs:
        ms.add(tuple(sorted(s)))        # a multiset is a sorted sequence
    sets2 = []
    sn = sorted(nums)
    def rec2(i, rem, cur):
        if rem == 0:
            sets2.append(tuple(cur)); return
        if i == len(sn): return
        k = 0
        while k * sn[i] <= rem:
            rec2(i + 1, rem - k * sn[i], cur + [sn[i]] * k); k += 1
    rec2(0, target, [])
    assert set(sets2) == ms and len(sets2) == len(ms)   # two independent ways to enumerate multisets agree
    return [len(seqs), len(sets2)]

# examples
for nums, t, exp in [([1, 2, 3], 4, [7, 4]), ([9], 3, [0, 0]), ([2, 5], 0, [1, 1]), ([1, 2], 6, [13, 4])]:
    got = count_both(nums, t); assert got == exp == brute(nums, t), (nums, t, got)
    print('example', nums, t, '->', got)

# hand table for the first example
nums, t = [1, 2, 3], 4
o = [1] + [0] * t
for tt in range(1, t + 1):
    o[tt] = sum(o[tt - x] for x in nums if x <= tt)
print('ordered   t=0..4:', o)
u = [1] + [0] * t
for x in nums:
    for tt in range(x, t + 1):
        u[tt] += u[tt - x]
    print('unordered after coin', x, ':', u)

# seeded cross-check
n_cases = diff = swap_ok = 0
for _ in range(600):
    k = random.randint(1, 4)
    nums = random.sample(range(1, 7), k)
    target = random.randint(0, 10)
    got = count_both(nums, target)
    assert got == brute(nums, target), (nums, target)
    a, b = swapped(nums, target)
    assert (a, b) == (got[1], got[0])     # coin-outer gives unordered, target-outer gives ordered, always
    n_cases += 1; diff += got[0] != got[1]
    swap_ok += got[0] >= got[1]  # ordered count >= unordered count always
print('cross-check cases', n_cases, '| ordered != unordered on', diff, '| ordered >= unordered on', swap_ok)
for _ in range(100):
    nums = random.sample(range(1, 30), random.randint(1, 6)); target = random.randint(0, 120)
    assert count_both(nums, target)[0] == memo_ordered(nums, target)
print('memo (depth <= 120) equals bottom-up on 100 random cases')

# big sizes: bottom-up is fine, memo recursion is not
big = count_both([1, 2, 3], 2000)
print('target 2000, nums [1,2,3]: ordered has', len(str(big[0])), 'digits, unordered =', big[1])
print('limit =', sys.getrecursionlimit())
for n in (500, 2000):
    try:
        v = memo_ordered([1, 2, 3], n); print('memo target', n, 'ok', v == count_both([1, 2, 3], n)[0])
    except RecursionError:
        print('memo target', n, 'RecursionError')
def memo_ok(n):
    try:
        memo_ordered([1, 2, 3], n); return True
    except RecursionError:
        return False
lo, hi = 1, 2000          # largest n that works in a fresh cache (the sum(...) generator costs a second frame per level)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if memo_ok(mid): lo = mid
    else: hi = mid - 1
print('largest target the memo handles at limit 1000 (this layout, called from module level):', lo)
assert count_both([1], 2000) == [1, 1]
assert count_both([100] * 1, 2000) == [1, 1] and count_both([100, 99], 1) == [0, 0]
print('edge asserts passed')
