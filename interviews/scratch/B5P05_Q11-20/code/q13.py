import itertools
import random
from functools import lru_cache


def split_dp(nums, k):
    """Reference O(k * n^2): dp over (elements used, pieces left), exactly k pieces."""
    n = len(nums)
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    INF = float("inf")

    @lru_cache(maxsize=None)
    def f(i, j):
        if j == 0:
            return 0 if i == n else INF
        best = INF
        for m in range(i + 1, n - j + 2):      # leave at least j-1 elements for the rest
            best = min(best, max(pre[m] - pre[i], f(m, j - 1)))
        return best

    return f(0, k)


def pieces_needed(nums, cap):
    """Greedy: fewest pieces so every piece sum <= cap (needs cap >= max(nums))."""
    pieces, cur = 1, 0
    for x in nums:
        if cur + x > cap:
            pieces += 1
            cur = 0
        cur += x
    return pieces


def split_bs(nums, k):
    lo, hi = max(nums), sum(nums)       # answer lies in [max, sum]
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces_needed(nums, mid) <= k:   # 'at most k' is monotone in mid
            hi = mid
        else:
            lo = mid + 1
    return lo


def split_cuts(nums, k):
    """Second reference: try every set of k-1 cut points (exactly k pieces)."""
    n = len(nums)
    best = None
    for cuts in itertools.combinations(range(1, n), k - 1):
        b = (0,) + cuts + (n,)
        v = max(sum(nums[b[t]:b[t + 1]]) for t in range(k))
        best = v if best is None else min(best, v)
    return best


examples = [([7, 2, 5, 10, 8], 2, 18), ([1, 2, 3, 4, 5], 2, 9), ([1, 4, 4], 3, 4), ([5], 1, 5)]
for nums, k, exp in examples:
    got = split_bs(nums, k)
    assert got == split_dp(tuple(nums), k) == split_cuts(nums, k) == exp, (nums, k, got)
    print(nums, "k =", k, "->", got)

random.seed(13)
for _ in range(600):
    n = random.randint(1, 8)
    nums = [random.randint(0, 7) for _ in range(n)]
    k = random.randint(1, n)
    assert split_bs(nums, k) == split_dp(tuple(nums), k) == split_cuts(nums, k), (nums, k)
print("cross-check: 600 seeded cases agree (binary search, DP, all-cuts brute force)")

# exhaustive proof-by-enumeration of the 'at most k == exactly k' claim on all tiny inputs
checked = 0
for n in range(1, 6):
    for nums in itertools.product(range(0, 4), repeat=n):
        for k in range(1, n + 1):
            at_most = next(S for S in range(max(nums), sum(nums) + 1)
                           if pieces_needed(list(nums), S) <= k)
            assert at_most == split_cuts(list(nums), k), (nums, k)
            checked += 1
print("exhaustive: 'at most k pieces' == 'exactly k pieces' on %d (list, k) inputs" % checked)

# edge cases
assert split_bs([0, 0, 0], 2) == 0
assert split_bs([10], 1) == 10
assert split_bs([1, 1, 1, 1], 4) == 1          # k == len: every element alone -> max
assert split_bs([1, 1, 1, 1], 1) == 4          # k == 1: whole sum
assert split_bs([10**6] * 1000, 1) == 10**9    # max size: sum 10^9 fits easily in a Python int
assert split_bs([5, 5, 5, 5], 3) == 10         # pieces can't be balanced exactly
print("edge asserts passed")
