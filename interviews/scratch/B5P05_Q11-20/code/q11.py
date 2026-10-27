import bisect
import random


def lower_bound(a, x):
    """First index i with a[i] >= x (len(a) if none)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(a, x):
    """First index i with a[i] > x (len(a) if none)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_eq(a, x):
    return upper_bound(a, x) - lower_bound(a, x)


def count_range(a, lo_v, hi_v):  # values in [lo_v, hi_v]
    return max(0, upper_bound(a, hi_v) - lower_bound(a, lo_v))


def floor_val(a, x):  # largest element <= x
    i = upper_bound(a, x)
    return a[i - 1] if i > 0 else None  # guard: a[-1] would wrap around


def ceil_val(a, x):  # smallest element >= x
    i = lower_bound(a, x)
    return a[i] if i < len(a) else None


def successor(a, x):  # smallest element > x (strict)
    i = upper_bound(a, x)
    return a[i] if i < len(a) else None


# ---- brute-force references (linear scans) ----
def b_lb(a, x): return sum(1 for v in a if v < x)
def b_ub(a, x): return sum(1 for v in a if v <= x)
def b_floor(a, x): return max((v for v in a if v <= x), default=None)
def b_succ(a, x): return min((v for v in a if v > x), default=None)
def b_cnt(a, l, h): return sum(1 for v in a if l <= v <= h)


a = [1, 2, 2, 2, 3, 5]
print("lower_bound(2) =", lower_bound(a, 2))
print("upper_bound(2) =", upper_bound(a, 2))
print("count of 2     =", count_eq(a, 2))
print("count in [2,3] =", count_range(a, 2, 3))
print("floor(4)       =", floor_val(a, 4))
print("successor(5)   =", successor(a, 5))
print("lower_bound(0) =", lower_bound(a, 0))
print("upper_bound(9) =", upper_bound(a, 9))
print("x below all (0): floor =", floor_val(a, 0), ", successor =", successor(a, 0))
print("x above all (9): floor =", floor_val(a, 9), ", successor =", successor(a, 9))
assert [lower_bound(a, 2), upper_bound(a, 2), count_eq(a, 2), count_range(a, 2, 3),
        floor_val(a, 4), successor(a, 5), lower_bound(a, 0), upper_bound(a, 9)] == [1, 4, 3, 4, 3, None, 0, 6]

random.seed(11)
n_checks = 0
for _ in range(500):
    arr = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 10)))
    for x in range(-7, 8):
        assert lower_bound(arr, x) == bisect.bisect_left(arr, x) == b_lb(arr, x), (arr, x)
        assert upper_bound(arr, x) == bisect.bisect_right(arr, x) == b_ub(arr, x), (arr, x)
        assert count_eq(arr, x) == arr.count(x)
        assert floor_val(arr, x) == b_floor(arr, x)
        assert successor(arr, x) == b_succ(arr, x)
        n_checks += 1
    for l in range(-6, 7):
        for h in range(-6, 7):
            assert count_range(arr, l, h) == b_cnt(arr, l, h), (arr, l, h)
print("cross-check: 500 seeded lists, %d (list, x) pairs agree with bisect and brute force" % n_checks)

# edge cases
assert lower_bound([], 3) == 0 and upper_bound([], 3) == 0
assert floor_val([], 3) is None and successor([], 3) is None
assert count_range([1, 2, 3], 5, 1) == 0          # inverted range must not go negative
assert floor_val([4, 4], 4) == 4 and successor([4, 4], 4) is None
# bisect key (3.10+): key applies to the elements, NOT to x
recs = [(1, "a"), (2, "b"), (2, "c"), (5, "d")]
assert bisect.bisect_left(recs, 2, key=lambda r: r[0]) == 1
assert bisect.bisect_right(recs, 2, key=lambda r: r[0]) == 3
# the classic wrap-around bug: a[upper_bound-1] with index -1 silently returns the LAST element
assert a[upper_bound(a, 0) - 1] == 5   # wrong 'floor(0)' if you forget the guard
print("edge asserts passed")
