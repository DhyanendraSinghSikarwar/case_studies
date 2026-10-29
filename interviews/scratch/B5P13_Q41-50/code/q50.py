import random, itertools, time, math
random.seed(50)

# ---- optimal: bucket by value, keep min and max per bucket, scan the buckets once
def max_gap(nums):
    n = len(nums)
    if n < 2: return 0
    lo, hi = min(nums), max(nums)
    if lo == hi: return 0
    size = max(1, (hi - lo) // (n - 1))               # bucket width: never above the guaranteed minimum gap
    nb = (hi - lo) // size + 1
    mins = [None] * nb; maxs = [None] * nb
    for v in nums:
        b = (v - lo) // size
        if mins[b] is None or v < mins[b]: mins[b] = v
        if maxs[b] is None or v > maxs[b]: maxs[b] = v
    best = 0; prev_max = None
    for b in range(nb):
        if mins[b] is None: continue                   # empty bucket: skip it, the gap spans over it
        if prev_max is not None: best = max(best, mins[b] - prev_max)
        prev_max = maxs[b]
    return best

# ---- brute force: comparison sort and adjacent differences
def brute(nums):
    s = sorted(nums)
    return max((y - x for x, y in zip(s, s[1:])), default=0)

# ---- examples
assert max_gap([3, 6, 9, 1]) == 3 and max_gap([10]) == 0 and max_gap([5, 5, 5]) == 0 and max_gap([1, 10000000]) == 9999999
print('examples ok:', max_gap([3, 6, 9, 1]), max_gap([10]), max_gap([5, 5, 5]), max_gap([1, 10000000]))

# ---- seeded random cross-check against sorted()
for _ in range(5000):
    n = random.randint(0, 30); m = random.choice([3, 10, 100, 10**9])
    t = [random.randint(0, m) for _ in range(n)]
    assert max_gap(t) == brute(t), t
print('5000 random lists (n <= 30, values up to 3, 10, 100 or 10^9): equal to sorted() + adjacent differences')

# ---- the pigeonhole claims, checked exhaustively on small inputs: every list of length 2..5 over values 0..8
checked = 0
for n in range(2, 6):
    for t in itertools.product(range(9), repeat=n):
        lo, hi = min(t), max(t)
        if lo == hi: continue
        g = brute(t); size = max(1, (hi - lo) // (n - 1))
        assert g >= -(-(hi - lo) // (n - 1))                                  # max gap >= ceil((hi - lo) / (n - 1))
        assert size - 1 < g                                                   # two values in one bucket differ by at most size - 1 < the max gap
        s = sorted(t)
        for x, y in zip(s, s[1:]):
            if y - x == g: assert (x - lo) // size != (y - lo) // size        # a maximum gap pair never shares a bucket
        assert (hi - lo) // size + 1 <= 2 * n                                 # at most 2n buckets, so O(n) space
        checked += 1
print('exhaustive on', checked, 'lists: max gap >= ceil(range/(n-1)); bucket width - 1 < max gap; every maximum-gap pair straddles buckets; buckets <= 2n')

# ---- bucket count for large n (the 2n bound is checked above only on small lists; here is the actual number)
n = 10**5; big = [random.randint(0, 10**9) for _ in range(n)]
lo, hi = min(big), max(big); size = max(1, (hi - lo) // (n - 1))
print('n = 100000, values up to 10^9: bucket width', size, ', buckets', (hi - lo) // size + 1)
t = time.perf_counter(); r = max_gap(big); t1 = time.perf_counter() - t
t = time.perf_counter(); r2 = brute(big); t2 = time.perf_counter() - t
assert r == r2
print('max gap =', r, '; (sandbox timing, varies run to run) bucket method %.3f s, sorted() + differences %.3f s' % (t1, t2))

# ---- edge asserts
assert max_gap([]) == 0 and max_gap([7]) == 0 and max_gap([1, 1]) == 0
assert max_gap([0, 10**9]) == 10**9 and max_gap([1, 2, 3, 4, 5]) == 1
assert max_gap([1, 3]) == 2 and max_gap([0, 5, 5, 10]) == 5
assert max_gap([0, 1, 100]) == 99 and max_gap([100, 0, 1]) == 99
print('edge asserts ok')
