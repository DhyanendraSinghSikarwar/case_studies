import random


def merge_brute(a, m, b, n):
    """Extra-space version: sort the live parts, copy back."""
    merged = sorted(a[:m] + b)
    a[:] = merged
    return a


def merge_back(a, m, b, n):
    """Fill from the back. i: last live of a, j: last of b, w: write slot."""
    i, j, w = m - 1, n - 1, m + n - 1
    while j >= 0:                      # once b is used up, a's prefix is in place
        if i >= 0 and a[i] > b[j]:
            a[w] = a[i]
            i -= 1
        else:
            a[w] = b[j]
            j -= 1
        w -= 1
    return a


def merge_front_wrong(a, m, b, n):
    """Fill from the front in the same array: overwrites unread a values."""
    i, j = 0, 0
    a_copy_len = m
    for w in range(m + n):
        if j >= n or (i < a_copy_len and a[i] <= b[j]):
            a[w] = a[i]
            i += 1
        else:
            a[w] = b[j]
            j += 1
    return a


a = [1, 2, 3, 0, 0, 0]
print("back-fill  :", merge_back(a[:], 3, [2, 5, 6], 3))
assert merge_back(a[:], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]
try:
    bad = merge_front_wrong(a[:], 3, [2, 5, 6], 3)
    print("front-fill :", bad, "(wrong)")
    assert bad != [1, 2, 2, 3, 5, 6]
except IndexError as e:
    print("front-fill : IndexError", e)

# --- edge cases
assert merge_back([0], 0, [1], 1) == [1]            # a empty
assert merge_back([1], 1, [], 0) == [1]             # b empty
assert merge_back([], 0, [], 0) == []               # both empty
assert merge_back([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3) == [1, 2, 3, 4, 5, 6]
assert merge_back([1, 2, 3, 0, 0, 0], 3, [4, 5, 6], 3) == [1, 2, 3, 4, 5, 6]
assert merge_back([2, 2, 0, 0], 2, [2, 2], 2) == [2, 2, 2, 2]
assert merge_back([-3, -1, 0, 0], 2, [-2, -2], 2) == [-3, -2, -2, -1]
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(22)
for _ in range(1000):
    m, n = rng.randint(0, 8), rng.randint(0, 8)
    live = sorted(rng.randint(-5, 5) for _ in range(m))
    b = sorted(rng.randint(-5, 5) for _ in range(n))
    a1 = live + [0] * n
    a2 = live + [0] * n
    assert merge_back(a1, m, b, n) == merge_brute(a2, m, b, n)
print("1000 random cases OK")
