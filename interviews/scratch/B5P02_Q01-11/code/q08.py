import random
from itertools import combinations


def three_sum_brute(nums):
    out = set()
    for a, b, c in combinations(nums, 3):
        if a + b + c == 0:
            out.add(tuple(sorted((a, b, c))))
    return sorted(list(t) for t in out)


def three_sum(nums):
    nums = sorted(nums)
    n = len(nums)
    res = []
    for i in range(n - 2):
        if nums[i] > 0:
            break                              # smallest is positive: no zero sum left
        if i > 0 and nums[i] == nums[i - 1]:
            continue                           # skip duplicate first element
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                    # skip duplicate second element
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1                    # skip duplicate third element
    return res


def three_sum_hash(nums):
    # no-sort variant: set of sorted tuples, O(n^2) time, O(n) extra space
    seen_triples = set()
    n = len(nums)
    for i in range(n):
        seen = set()
        for j in range(i + 1, n):
            need = -nums[i] - nums[j]
            if need in seen:
                seen_triples.add(tuple(sorted((nums[i], nums[j], need))))
            seen.add(nums[j])
    return sorted(list(t) for t in seen_triples)


for nums in ([-1, 0, 1, 2, -1, -4], [0, 0, 0], [1, 2, 3]):
    print(nums, "->", three_sum(nums))
assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
assert three_sum([0, 0, 0]) == [[0, 0, 0]]
assert three_sum([1, 2, 3]) == []
assert three_sum([0, 0, 0, 0, 0]) == [[0, 0, 0]]              # many duplicates, one answer
assert three_sum([-2, 0, 0, 2, 2]) == [[-2, 0, 2]]
assert three_sum([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]) == three_sum_brute(
    [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6])
assert three_sum([-1, -2, -3]) == []                          # all negative

rng = random.Random(9)
cases = 0
for _ in range(2000):
    n = rng.randint(3, 10)
    nums = [rng.randint(-5, 5) for _ in range(n)]
    want = three_sum_brute(nums)
    assert three_sum(nums) == want, nums
    assert three_sum_hash(nums) == want, nums
    cases += 1
print("random cross-check passed:", cases, "cases")
