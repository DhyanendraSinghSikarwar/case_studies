import random
from itertools import combinations


def kth_pair_distance(nums, k):
    a = sorted(nums)
    n = len(a)

    def count_le(d):
        cnt, left = 0, 0
        for right in range(n):
            while a[right] - a[left] > d:
                left += 1
            cnt += right - left              # pairs (left..right-1, right) with distance <= d
        return cnt

    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_pair_distance_brute(nums, k):
    return sorted(abs(x - y) for x, y in combinations(nums, 2))[k - 1]


for nums, k, want in [([1, 3, 1], 1, 0), ([1, 1, 1], 2, 0), ([1, 6, 1], 3, 5), ([1, 3, 1], 2, 2), ([1, 3, 1], 3, 2)]:
    got = kth_pair_distance(nums, k)
    print(nums, "k =", k, "->", got, " brute:", kth_pair_distance_brute(nums, k))
    assert got == kth_pair_distance_brute(nums, k) == want

rng = random.Random(38)
cnt = 0
for _ in range(1500):
    n = rng.randint(2, 9)
    nums = [rng.randint(0, 12) for _ in range(n)]
    for k in range(1, n * (n - 1) // 2 + 1):
        assert kth_pair_distance(nums, k) == kth_pair_distance_brute(nums, k), (nums, k)
        cnt += 1
print("random (nums, k) cases checked:", cnt)

# size argument for n = 10**4
n = 10**4
pairs = n * (n - 1) // 2
print("pairs for n = 10**4:", pairs, " pointer slots alone at 8 bytes each: about", pairs * 8 // 10**6, "MB")
# runtime sanity on a big input (sandbox only): O(n log range), never builds pairs
big = [rng.randint(0, 10**6) for _ in range(n)]
v = kth_pair_distance(big, pairs // 2)
print("n = 10**4 median pair distance (sandbox run):", v)
# edge asserts
assert kth_pair_distance([5, 5], 1) == 0
assert kth_pair_distance([1, 100], 1) == 99
assert kth_pair_distance([0, 10**6], 1) == 10**6
assert kth_pair_distance([1, 2, 3, 4], 6) == 3
print("all checks passed")
