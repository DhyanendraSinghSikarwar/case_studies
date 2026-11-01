import random, itertools, bisect, time
random.seed(47)

# ---- optimal: prefix sums + merge sort; count BEFORE merging, with two forward-only pointers
def count_range_sum(nums, lo, hi):
    pre = [0] + list(itertools.accumulate(nums))        # pre[b] - pre[a] = sum of nums[a:b]
    count = 0
    def sort(a):                                         # returns the sorted list; depth about log2(n + 1)
        nonlocal count
        if len(a) <= 1: return a
        mid = len(a) // 2
        L, R = sort(a[:mid]), sort(a[mid:])             # L holds EARLIER positions than R
        x = y = 0
        for v in L:                                      # L is sorted ascending, so v + lo and v + hi only increase
            while x < len(R) and R[x] - v < lo: x += 1  # x: first R item with R - v >= lo
            while y < len(R) and R[y] - v <= hi: y += 1 # y: first R item with R - v > hi
            count += y - x                               # R[x:y] all lie in [v + lo, v + hi]
        out = []; i = j = 0                              # now merge (positions no longer matter above this level)
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(pre)
    return count

# ---- brute force: every subarray with a running sum, O(n^2)
def brute(nums, lo, hi):
    c = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if lo <= s <= hi: c += 1
    return c

# ---- second independent method: sorted list + bisect (counts earlier prefix sums in [pre - hi, pre - lo]); O(n^2) inserts but tiny n
def with_bisect(nums, lo, hi):
    seen = [0]; s = 0; c = 0
    for v in nums:
        s += v
        c += bisect.bisect_right(seen, s - lo) - bisect.bisect_left(seen, s - hi)
        bisect.insort(seen, s)
    return c

# ---- a WRONG version: merge first, then count (positions are lost, so it counts pairs in the wrong order)
def wrong_count_after_merge(nums, lo, hi):
    pre = [0] + list(itertools.accumulate(nums)); count = 0
    def sort(a):
        nonlocal count
        if len(a) <= 1: return a
        mid = len(a) // 2; L, R = sort(a[:mid]), sort(a[mid:])
        merged = sorted(L + R)                           # merge first ...
        x = y = 0
        for v in L:                                      # ... then the pointers see a mixed list
            while x < len(merged) and merged[x] - v < lo: x += 1
            while y < len(merged) and merged[y] - v <= hi: y += 1
            count += y - x
        return merged
    sort(pre); return count

# ---- examples
assert count_range_sum([-2, 5, -1], -2, 2) == 3
assert count_range_sum([0], 0, 0) == 1
assert count_range_sum([1, 2, 3], 3, 5) == 3
print('examples ok:', count_range_sum([-2, 5, -1], -2, 2), count_range_sum([0], 0, 0), count_range_sum([1, 2, 3], 3, 5))

# ---- seeded random cross-check against the O(n^2) double loop (and the bisect method)
for _ in range(3000):
    n = random.randint(1, 12); m = random.choice([1, 3, 10])
    nums = [random.randint(-m, m) for _ in range(n)]
    lo = random.randint(-3 * m, 3 * m); hi = lo + random.randint(0, 4 * m)
    r = count_range_sum(nums, lo, hi)
    assert r == brute(nums, lo, hi) == with_bisect(nums, lo, hi), (nums, lo, hi)
print('3000 random cases: merge-sort count == double loop == bisect count')
wrong = 0
for _ in range(500):
    nums = [random.randint(-5, 5) for _ in range(random.randint(2, 8))]
    lo = random.randint(-6, 3); hi = lo + random.randint(0, 6)
    wrong += wrong_count_after_merge(nums, lo, hi) != brute(nums, lo, hi)
print('counting AFTER the merge was wrong on', wrong, 'of 500 random cases')

# ---- maximum size: n = 50000, values up to 1e9, bounds up to 1e14
nums = [random.randint(-10**9, 10**9) for _ in range(50000)]
t = time.perf_counter(); r = count_range_sum(nums, -10**14, 10**14); dt = time.perf_counter() - t
assert r == 50000 * 50001 // 2                         # every subarray sum is within +-5*10^13, so all pairs count
t = time.perf_counter(); r2 = count_range_sum(nums, 10**14 - 1, 10**14); dt2 = time.perf_counter() - t
assert r2 == 0
r3 = count_range_sum(nums, -10**9, 10**9); assert r3 == with_bisect(nums, -10**9, 10**9)
print('n = 50000:', r, 'pairs counted (all of them, the bounds cover every sum); a window above every sum counts', r2, '; (sandbox timing) about %.2f s' % dt)
print('window [-1e9, 1e9] on the same 50000 values:', r3, '(agrees with the bisect method)')

# ---- edge asserts
assert count_range_sum([5], 6, 7) == 0 and count_range_sum([5], 5, 5) == 1
assert count_range_sum([0, 0, 0], 0, 0) == 6            # all 3 + 2 + 1 subarrays have sum 0
assert count_range_sum([-1, -1], -2, -1) == 3
assert count_range_sum([1, -1, 1], 0, 0) == 2          # [1, -1] and [-1, 1]
print('edge asserts ok')
