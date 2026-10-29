import random
random.seed(44)
# Editor-level description of Timsort's run detection (NOT checked against the CPython source here).

def minrun(n):
    r = 0
    while n >= 64:
        r |= n & 1                 # remember if any 1 bit was shifted out
        n >>= 1
    return n + r

def solve(nums):
    n = len(nums); mr = minrun(n); runs = []; lo = 0
    while lo < n:
        i = lo + 1
        if i < n:
            if nums[i] < nums[lo]:                              # strictly descending run
                while i < n and nums[i] < nums[i - 1]: i += 1
            else:                                               # non-decreasing run
                while i < n and nums[i] >= nums[i - 1]: i += 1
        length = max(i - lo, min(mr, n - lo))                   # short runs are padded to minrun by insertion sort
        runs.append(length); lo += length
    return [mr, runs]

# ---- recursive scan that rebuilds the run boundaries, written separately
def solve_rec(nums):
    n = len(nums)
    k, r = n, 0
    while k >= 64: r |= k & 1; k >>= 1
    m = k + r
    def natural(lo):
        if lo == n - 1: return 1
        desc = nums[lo + 1] < nums[lo]
        e = lo + 1
        while e < n and ((nums[e] < nums[e - 1]) if desc else (nums[e] >= nums[e - 1])): e += 1
        return e - lo
    def go(lo):
        if lo >= n: return []
        rl = max(natural(lo), min(m, n - lo))
        return [rl] + go(lo + rl)            # depth = number of runs: keep the lists small
    return [m, go(0)]

# ---- examples
ex1 = list(range(30, 0, -1)) + list(range(100, 134))
assert solve(ex1) == [32, [32, 32]]
assert solve([9]) == [1, [1]]
assert solve([4, 4, 4, 3]) == [4, [4]]
assert solve([1, 2, 3, 2, 1, 0, 5, 6]) == [8, [8]]
print('examples ok:', solve(ex1), solve([9]), solve([4, 4, 4, 3]), solve([1, 2, 3, 2, 1, 0, 5, 6]))

# ---- seeded random cross-check (short inputs so the recursion in solve_rec stays shallow)
for _ in range(3000):
    n = random.randint(1, 120)
    mode = random.choice(['rand', 'runs', 'few'])
    if mode == 'rand': t = [random.randint(0, 30) for _ in range(n)]
    elif mode == 'few': t = [random.randint(0, 2) for _ in range(n)]
    else:
        t = []
        while len(t) < n:
            L = random.randint(1, 40); s = random.randint(0, 100); d = random.choice([-1, 1, 0])
            t += [s + d * k for k in range(L)]
        t = t[:n]
    assert solve(t) == solve_rec(t), t
    mr, runs = solve(t); assert sum(runs) == n and all(r >= min(mr, n) or r == runs[-1] for r in runs)
print('3000 random inputs: scan == recursive rebuild; run lengths sum to n; every run but the last is >= minrun')

# ---- claims about minrun, checked for EVERY n up to 10^5
for n in range(1, 100001):
    m = minrun(n)
    if n < 64: assert m == n; continue
    k, s = n, 0
    while k >= 64: k >>= 1; s += 1
    assert 32 <= m <= 64
    assert n <= m * 2 ** s and m * 2 ** (s - 1) < n
print('every n in 1..100000: n < 64 -> minrun = n; n >= 64 -> 32 <= minrun <= 64, n <= minrun * 2^s and minrun * 2^(s-1) < n')
print('examples of minrun:', {n: minrun(n) for n in (63, 64, 65, 127, 128, 1000, 2048, 2049, 100000)})
print('n / minrun for some n (always <= the next power of two, here 2, 2, 16, 64, 2048):',
      {n: round(n / minrun(n), 3) for n in (65, 127, 1000, 2049, 100000)})

# ---- a run-structure demonstration at the maximum size
big = [random.randint(0, 10**9) for _ in range(100000)]
mr, runs = solve(big)
print('random 100000 items: minrun', mr, ', number of runs', len(runs), ', first runs', runs[:3], ', last run', runs[-1])
inc = list(range(100000)); mr, runs = solve(inc)
print('sorted 100000 items: runs', runs)

# ---- edge asserts
assert solve([2, 1]) == [2, [2]]
assert solve([3, 3, 3]) == [3, [3]]
assert minrun(64) == 32 and minrun(65) == 33 and minrun(127) == 64 and minrun(128) == 32
n = 130; t = list(range(100, 0, -1)) + list(range(30))       # 100..1 then 0..29
assert solve(t) == [33, [101, 29]]     # the 0 after 1 continues the strict descent
print('edge asserts ok')
