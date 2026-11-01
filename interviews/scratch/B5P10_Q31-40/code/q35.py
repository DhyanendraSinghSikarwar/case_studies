import bisect
import itertools
import random

random.seed(35)

def patience(nums, strict):
    """tails[k] = smallest possible last value of a valid subsequence of length k + 1."""
    find = bisect.bisect_left if strict else bisect.bisect_right
    tails = []
    for x in nums:
        p = find(tails, x)
        if p == len(tails):
            tails.append(x)
        else:
            tails[p] = x
    return tails

def solve(nums):
    nd = patience(nums, strict=False)      # bisect_right: an equal value goes AFTER the equals
    st = patience(nums, strict=True)       # bisect_left: an equal value REPLACES the equal
    return [len(nd), nd, len(st)]

def brute(nums):
    """Enumerate every subsequence; for each length keep the smallest last value."""
    n = len(nums)
    best_nd, best_st = {}, {}
    for L in range(1, n + 1):
        for c in itertools.combinations(range(n), L):
            v = [nums[i] for i in c]
            if all(v[t] <= v[t + 1] for t in range(L - 1)):
                best_nd[L] = min(best_nd.get(L, v[-1]), v[-1])
            if all(v[t] < v[t + 1] for t in range(L - 1)):
                best_st[L] = min(best_st.get(L, v[-1]), v[-1])
    return [len(best_nd), [best_nd[k] for k in sorted(best_nd)], len(best_st)]

def nondecreasing_with_bisect_left(nums):
    return len(patience(nums, strict=True))          # the classic slip

# ---- examples from the prompt
assert solve([1, 3, 3, 2, 3]) == [4, [1, 2, 3, 3], 3]
assert solve([5, 5, 5]) == [3, [5, 5, 5], 1]
assert solve([2, 1]) == [1, [1], 1]
assert solve([]) == [0, [], 0]
assert solve([4, 4, 2, 9, 9, 1]) == [4, [1, 4, 9, 9], 2]
print('examples ok')

# ---- step trace of the first example
nums = [1, 3, 3, 2, 3]
tr, tl = [], []
for x in nums:
    tr.append(x)
    tl.append((x, patience(tr, False), patience(tr, True)))
for x, a, b in tl:
    print(f'x={x}: non-decreasing tails (bisect_right) {a} | strict tails (bisect_left) {b}')

# ---- seeded random cross-check against the enumeration, plus an exhaustive sweep
cases = 0
for _ in range(500):
    nums = [random.randint(-5, 5) for _ in range(random.randint(0, 12))]
    assert solve(nums) == brute(nums), nums
    cases += 1
for n in range(0, 7):
    for nums in itertools.product(range(4), repeat=n):
        assert solve(list(nums)) == brute(list(nums)), nums
        cases += 1
print('cross-check passed on', cases, 'cases')

# ---- what bisect_left gives for the non-decreasing variant: the strict length, always
wrong = same = 0
for _ in range(600):
    nums = [random.randint(0, 5) for _ in range(random.randint(0, 10))]
    assert nondecreasing_with_bisect_left(nums) == solve(nums)[2]
    if nondecreasing_with_bisect_left(nums) != solve(nums)[0]:
        wrong += 1
print('bisect_left for non-decreasing equals the strict length on all 600; it is wrong for non-decreasing on', wrong)
print('example [5, 5, 5]: bisect_left gives', nondecreasing_with_bisect_left([5, 5, 5]), 'instead of 3')

# ---- edge cases and size
assert solve([7]) == [1, [7], 1]
assert solve([3, 2, 1]) == [1, [1], 1]
assert solve([1, 1, 2, 2]) == [4, [1, 1, 2, 2], 2]
big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
r = solve(big)
assert 1 <= r[2] <= r[0] <= len(big)
print('n = 10**5 random lengths (non-decreasing, strict):', r[0], r[2])
