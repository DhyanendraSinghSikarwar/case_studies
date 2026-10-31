import random
from itertools import combinations


def closest_brute(nums, target):
    best = None
    for a, b, c in combinations(nums, 3):  # distinct positions
        s = a + b + c
        if best is None or abs(s - target) < abs(best - target):
            best = s
    return best


def closest_two_pointers(nums, target):
    a = sorted(nums)
    n = len(a)
    best = a[0] + a[1] + a[2]
    for i in range(n - 2):
        if i and a[i] == a[i - 1]:
            continue  # same first value gives the same triples
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s == target:
                return s
            if s < target:
                lo += 1
            else:
                hi -= 1
    return best


print("[-1,2,1,-4], 1:", closest_two_pointers([-1, 2, 1, -4], 1), "(expected 2)")
print("[0,0,0], 1:", closest_two_pointers([0, 0, 0], 1), "(expected 0)")

random.seed(27)
for _ in range(1000):
    n = random.randint(3, 8)
    nums = [random.randint(-6, 6) for _ in range(n)]
    t = random.randint(-15, 15)
    got, want = closest_two_pointers(nums, t), closest_brute(nums, t)
    # ties (equally close sums) are possible in random data, so compare distance
    assert abs(got - t) == abs(want - t), (nums, t, got, want)
print("cross-check: 1000 seeded cases agree (on distance to target)")

assert closest_two_pointers([1, 1, 1], 5) == 3
assert closest_two_pointers([1, 1, 1, 0], -100) == 2
assert closest_two_pointers([-5, -4, -3], 0) == -12
assert closest_two_pointers([1, 2, 3, 4], 6) == 6  # exact hit
assert closest_two_pointers([0, 0, 0], 0) == 0
assert closest_two_pointers([1000, -1000, 0, 5], 7) == 5
nums = [random.randint(-1000, 1000) for _ in range(500)]
r = closest_two_pointers(nums, 123)
assert isinstance(r, int)
print("edge asserts passed")
