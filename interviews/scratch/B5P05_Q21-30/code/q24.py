import itertools
import random


def k_closest_brute(arr, k, x):
    # sort by (distance, value), take k, then sort the values ascending
    return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])


def k_closest(arr, k, x):
    lo, hi = 0, len(arr) - k               # candidate left edges of the window
    while lo < hi:
        mid = (lo + hi) // 2
        if x - arr[mid] > arr[mid + k] - x:    # right neighbour arr[mid+k] is strictly closer
            lo = mid + 1                       # window must start after mid
        else:
            hi = mid                           # tie or left side closer: keep mid (smaller values win ties)
    return arr[lo:lo + k]


examples = [([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]), ([1, 2, 3, 4, 5], 4, -1, [1, 2, 3, 4]),
            ([1, 3], 1, 2, [1]), ([1, 1, 2, 3, 4, 5], 3, 4, [3, 4, 5]), ([1, 2, 3, 4, 5], 2, 10, [4, 5])]
for arr, k, x, want in examples:
    assert k_closest(arr, k, x) == k_closest_brute(arr, k, x) == want, (arr, k, x)
    print(arr, "k =", k, "x =", x, "->", k_closest(arr, k, x))

# Exhaustive uniqueness test. The stated rule is: distance, then smaller value. Three ways to apply it must give
# the same VALUE list: (1) the value-keyed sort above, (2) distance then smaller INDEX (same thing on a sorted list),
# (3) distance, then value, then LARGER index (equal values at equal distance are interchangeable).
def by_index(arr, k, x, reverse_index):
    order = sorted(range(len(arr)), key=(lambda i: (abs(arr[i] - x), arr[i], -i)) if reverse_index else (lambda i: (abs(arr[i] - x), i)))
    return sorted(arr[i] for i in order[:k])


tested = 0
for n in range(1, 8):
    for arr in itertools.combinations_with_replacement(range(0, 7), n):   # every sorted list with duplicates
        arr = list(arr)
        for k in range(1, n + 1):
            for x in range(-2, 9):
                a = k_closest_brute(arr, k, x)
                assert a == by_index(arr, k, x, False) == by_index(arr, k, x, True), (arr, k, x)
                assert k_closest(arr, k, x) == a, (arr, k, x, k_closest(arr, k, x), a)
                tested += 1
print("exhaustive check passed:", tested, "(arr, k, x) triples; tie rules agree, binary search matches")

# a tie that is NOT resolved by value alone would break uniqueness: show the tie rule matters
assert k_closest([1, 3], 1, 2) == [1] and k_closest([1, 3], 1, 2) != [3]
print("tie case [1, 3], k=1, x=2 ->", k_closest([1, 3], 1, 2), "(smaller value wins; [3] would be wrong)")

# seeded random larger inputs
rng = random.Random(24)
for _ in range(1500):
    n = rng.randint(1, 40)
    arr = sorted(rng.randint(-20, 20) for _ in range(n))
    k = rng.randint(1, n)
    x = rng.randint(-30, 30)
    assert k_closest(arr, k, x) == k_closest_brute(arr, k, x), (arr, k, x)
print("random check passed: 1500 cases")

# edge cases
assert k_closest([5], 1, 100) == [5]
assert k_closest([2, 2, 2, 2], 2, 2) == [2, 2]
assert k_closest([1, 2, 3], 3, 0) == [1, 2, 3]          # k == n: window is the whole list
big = list(range(10 ** 4))
assert k_closest(big, 5, 10 ** 9) == big[-5:] and k_closest(big, 5, -10 ** 9) == big[:5]
print("edge asserts passed")
