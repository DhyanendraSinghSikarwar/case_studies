import random
from fractions import Fraction


def feasible(nums, k, t):
    # some subarray of length >= k has average >= t  <=>  some such subarray has sum(x - t) >= 0
    pre = [0.0]
    for x in nums:
        pre.append(pre[-1] + (x - t))
    best_min = float("inf")
    for i in range(k, len(pre)):
        best_min = min(best_min, pre[i - k])     # smallest prefix at least k back
        if pre[i] - best_min >= 0:
            return True
    return False


def max_avg(nums, k, iters=50):
    lo, hi = float(min(nums)), float(max(nums))
    for _ in range(iters):
        mid = (lo + hi) / 2
        if feasible(nums, k, mid):
            lo = mid                              # t is achievable, try higher
        else:
            hi = mid
    return lo


def max_avg_brute(nums, k):
    best = None
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if j - i + 1 >= k:
                v = Fraction(s, j - i + 1)
                if best is None or v > best:
                    best = v
    return best


for nums, k, want in [([1, 12, -5, -6, 50, 3], 4, 12.75), ([5], 1, 5.0), ([-3, -1, -2], 2, -1.5), ([0, 4, 0, 3, 2], 1, 4.0)]:
    got = max_avg(nums, k)
    print(nums, "k =", k, "->", round(got, 6), " brute:", float(max_avg_brute(nums, k)))
    assert abs(got - want) <= 1e-5 and float(max_avg_brute(nums, k)) == want

rng = random.Random(36)
worst = 0.0
for _ in range(1500):
    n = rng.randint(1, 10)
    nums = [rng.randint(-20, 20) for _ in range(n)]
    k = rng.randint(1, n)
    err = abs(max_avg(nums, k) - float(max_avg_brute(nums, k)))
    worst = max(worst, err)
    assert err <= 1e-5, (nums, k)
print("random cases: worst error =", worst)

# monotone in t: exhaustive over a grid of t for small lists
for _ in range(300):
    nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 8))]
    k = rng.randint(1, len(nums))
    seq = [feasible(nums, k, t / 4) for t in range(-40, 41)]
    assert all(not (not a and b) for a, b in zip(seq, seq[1:])), (nums, k)   # True then False only
# iterations needed: width 2*10**4 down to 1e-5
w, it = 2 * 10**4, 0
while w > 1e-5:
    w /= 2; it += 1
print("halvings from width 2*10**4 to 1e-5:", it)
assert it == 31
# edge asserts
assert abs(max_avg([7, 7, 7], 2) - 7.0) <= 1e-5            # all equal: lo == hi from the start
assert abs(max_avg([-5], 1) - (-5.0)) <= 1e-5
assert abs(max_avg([1, 2, 3, 4], 4) - 2.5) <= 1e-5          # k = n: only the whole array
print("all checks passed")
