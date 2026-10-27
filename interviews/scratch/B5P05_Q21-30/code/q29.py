import itertools


def first_true(pred, n):
    # template 1: first index in [0, n) with pred True, else n.  invariant: answer in [lo, hi]
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2                # mid < hi always, so hi = mid and lo = mid + 1 both shrink
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def last_true(pred, n):
    # template 2: last index in [0, n) with pred True, else -1.  invariant: answer in [lo, hi]; lo is "known good"
    lo, hi = -1, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2            # upper-biased: mid > lo always, so lo = mid shrinks
        if pred(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def first_true_brute(pred, n):
    return next((i for i in range(n) if pred(i)), n)


def last_true_brute(pred, n):
    return max((i for i in range(n) if pred(i)), default=-1)


a = [0, 0, 1, 1, 1]
print("template 1, a[i]==1:", first_true(lambda i: a[i] == 1, 5))
print("template 2, a[i]==0:", last_true(lambda i: a[i] == 0, 5))
print("all False -> t1, t2:", first_true(lambda i: False, 5), last_true(lambda i: False, 5))
print("all True  -> t1, t2:", first_true(lambda i: True, 5), last_true(lambda i: True, 5))
assert first_true(lambda i: a[i] == 1, 5) == 2 and last_true(lambda i: a[i] == 0, 5) == 1
assert (first_true(lambda i: False, 5), last_true(lambda i: False, 5)) == (5, -1)
assert (first_true(lambda i: True, 5), last_true(lambda i: True, 5)) == (0, 4)

# exhaustive: every monotone predicate for n = 0..11 (False..True for t1, True..False for t2)
checked = 0
for n in range(0, 12):
    for cut in range(n + 1):
        up = lambda i, c=cut: i >= c        # False...False True...True
        down = lambda i, c=cut: i < c       # True...True False...False
        assert first_true(up, n) == first_true_brute(up, n) == cut
        assert last_true(down, n) == last_true_brute(down, n) == cut - 1
        checked += 2
print("exhaustive check passed:", checked, "monotone predicates, n = 0..11")


# the classic infinite loop: floor mid with lo = mid
def last_true_buggy(pred, n, cap=1000):
    lo, hi = -1, n - 1
    steps = 0
    while lo < hi:
        steps += 1
        if steps > cap:
            return "stuck", lo, hi
        mid = (lo + hi) // 2                # BUG: should be (lo + hi + 1) // 2 for lo = mid
        if pred(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


print("buggy template 2 on all-True, n=5:", last_true_buggy(lambda i: True, 5))
assert last_true_buggy(lambda i: True, 5)[0] == "stuck"
# the exact state from the prompt: lo=3, hi=4 -> mid = 3 and lo = mid changes nothing
lo, hi = 3, 4
assert (lo + hi) // 2 == 3 and (lo + hi + 1) // 2 == 4
# Python-specific trap: with lo = -1, (lo + hi) // 2 can be -1, and a[-1] silently reads the LAST element
assert (-1 + 0) // 2 == -1
print("lo=3, hi=4: floor mid =", (3 + 4) // 2, "| upper mid =", (3 + 4 + 1) // 2, "| (-1+0)//2 =", (-1 + 0) // 2)


# lo <= hi with mid +/- 1: the better fit for exact match (can return inside the loop)
def exact(a, t):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == t:
            return mid
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


for n in range(0, 9):
    arr = list(range(0, 2 * n, 2))
    for t in range(-1, 2 * n + 1):
        assert exact(arr, t) == (arr.index(t) if t in arr else -1)
print("exact-match closed template passed for all n < 9")

# edge cases
assert first_true(lambda i: True, 0) == 0 and last_true(lambda i: True, 0) == -1     # empty range
assert first_true(lambda i: i >= 10 ** 9, 10 ** 9 + 5) == 10 ** 9
print("edge asserts passed")
