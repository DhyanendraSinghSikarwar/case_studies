import random
from itertools import combinations


def four_brute(nums, target):
    res = set()
    for q in combinations(nums, 4):
        if sum(q) == target:
            res.add(tuple(sorted(q)))
    return sorted(list(t) for t in res)


def k_sum(a, start, k, target):
    # a is sorted; returns unique k-tuples from a[start:] summing to target
    n = len(a)
    res = []
    if k == 2:
        lo, hi = start, n - 1
        while lo < hi:
            s = a[lo] + a[hi]
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                res.append([a[lo], a[hi]])
                lo += 1
                hi -= 1
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
                while lo < hi and a[hi] == a[hi + 1]:
                    hi -= 1
        return res
    for i in range(start, n - k + 1):
        if i > start and a[i] == a[i - 1]:
            continue
        # prune: smallest possible sum too big, or largest possible too small
        if sum(a[i:i + k]) > target:
            break
        if a[i] + sum(a[n - k + 1:]) < target:
            continue
        for rest in k_sum(a, i + 1, k - 1, target - a[i]):
            res.append([a[i]] + rest)
    return res


def four_sum(nums, target):
    return k_sum(sorted(nums), 0, 4, target)


def four_sum_loops(nums, target):
    # the explicit two-loop version most people write on a whiteboard
    a = sorted(nums)
    n = len(a)
    res = []
    for i in range(n - 3):
        if i and a[i] == a[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and a[j] == a[j - 1]:
                continue
            lo, hi = j + 1, n - 1
            while lo < hi:
                s = a[i] + a[j] + a[lo] + a[hi]
                if s < target:
                    lo += 1
                elif s > target:
                    hi -= 1
                else:
                    res.append([a[i], a[j], a[lo], a[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and a[lo] == a[lo - 1]:
                        lo += 1
                    while lo < hi and a[hi] == a[hi + 1]:
                        hi -= 1
    return res


e1 = four_sum([1, 0, -1, 0, -2, 2], 0)
e2 = four_sum([2, 2, 2, 2, 2], 8)
print("example 1:", e1)
print("example 2:", e2)
assert e1 == [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
assert e2 == [[2, 2, 2, 2]]
print("3-sum via k_sum:", k_sum(sorted([-1, 0, 1, 2, -1, -4]), 0, 3, 0))

random.seed(32)
for _ in range(1000):
    n = random.randint(0, 9)
    nums = [random.randint(-4, 4) for _ in range(n)]
    t = random.randint(-8, 8)
    b = four_brute(nums, t)
    assert four_sum(nums, t) == b, (nums, t)
    assert four_sum_loops(nums, t) == b, (nums, t)
print("cross-check: 1000 seeded cases agree (k_sum, explicit loops, brute)")

assert four_sum([], 0) == []
assert four_sum([1, 2, 3], 6) == []
assert four_sum([0, 0, 0, 0], 0) == [[0, 0, 0, 0]]
assert four_sum([0] * 200, 0) == [[0, 0, 0, 0]]
big = 10 ** 9
assert four_sum([big, big, big, big], 4 * big) == [[big, big, big, big]]
assert four_sum([-big, -big, big, big], 0) == [[-big, -big, big, big]]
assert four_sum([big, big, big, big], 0) == []
nums = [random.randint(-10 ** 9, 10 ** 9) for _ in range(200)]
r = four_sum(nums, 0)
assert r == sorted(r)
print("edge asserts passed")
