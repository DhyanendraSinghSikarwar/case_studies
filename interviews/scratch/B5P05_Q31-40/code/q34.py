import random


def kth_missing_index(arr, k):
    # first index i with arr[i] - (i + 1) >= k; answer k + i
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) >= k:
            hi = mid
        else:
            lo = mid + 1
    return k + lo


def kth_missing_value(arr, k):
    # smallest v with (missing positives <= v) >= k; missing(v) = v - (count of arr <= v)
    def missing_upto(v):
        # count of arr elements <= v by binary search
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= v:
                lo = mid + 1
            else:
                hi = mid
        return v - lo
    lo, hi = 1, arr[-1] + k
    while lo < hi:
        mid = (lo + hi) // 2
        if missing_upto(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_missing_brute(arr, k):
    s, v = set(arr), 0
    while k:
        v += 1
        if v not in s:
            k -= 1
    return v


for arr, k, want in [([2, 3, 4, 7, 11], 5, 9), ([1, 2, 3, 4], 2, 6), ([5, 6], 1, 1), ([1, 3], 1, 2), ([2], 3, 4)]:
    got = (kth_missing_index(arr, k), kth_missing_value(arr, k), kth_missing_brute(arr, k))
    print(arr, "k =", k, "-> index search, value search, brute:", got)
    assert got == (want, want, want)

rng = random.Random(34)
for _ in range(1500):
    n = rng.randint(1, 12)
    arr = sorted(rng.sample(range(1, 30), n))
    k = rng.randint(1, 40)
    b = kth_missing_brute(arr, k)
    assert kth_missing_index(arr, k) == b == kth_missing_value(arr, k), (arr, k)
# exhaustive: every strictly increasing list from 1..8, k = 1..12
from itertools import combinations
cnt = 0
for n in range(1, 9):
    for arr in combinations(range(1, 9), n):
        for k in range(1, 13):
            assert kth_missing_index(list(arr), k) == kth_missing_brute(list(arr), k)
            cnt += 1
print("exhaustive cases checked:", cnt)
# edge asserts
assert kth_missing_index([1], 1) == 2          # nothing missing before arr[0]
assert kth_missing_index([1000], 1) == 1       # missing count before first element is 999
assert kth_missing_index([1000], 999) == 999
assert kth_missing_index([1000], 1000) == 1001 # past the end
print("all checks passed")
