import random


def nge_brute(nums1, nums2):
    res = []
    for x in nums1:
        i = nums2.index(x)
        ans = -1
        for y in nums2[i + 1:]:
            if y > x:
                ans = y
                break
        res.append(ans)
    return res


def nge_stack(nums1, nums2):
    nxt = {}                                  # value -> next greater value
    stack = []                                # decreasing values, waiting for a bigger one
    for y in nums2:
        while stack and stack[-1] < y:
            nxt[stack.pop()] = y              # y is the first greater element to the right
        stack.append(y)
    # whatever is left on the stack has no greater element: default -1
    return [nxt.get(x, -1) for x in nums1]


assert nge_stack([4, 1, 2], [1, 3, 4, 2]) == nge_brute([4, 1, 2], [1, 3, 4, 2]) == [-1, 3, -1]
assert nge_stack([2, 4], [1, 2, 3, 4]) == nge_brute([2, 4], [1, 2, 3, 4]) == [3, -1]
print("[4,1,2] in [1,3,4,2] ->", nge_stack([4, 1, 2], [1, 3, 4, 2]))
print("[2,4] in [1,2,3,4] ->", nge_stack([2, 4], [1, 2, 3, 4]))

# edge cases
assert nge_stack([1], [1]) == [-1]                       # single element
assert nge_stack([5, 4, 3], [5, 4, 3]) == [-1, -1, -1]   # decreasing: nothing greater
assert nge_stack([1, 2, 3], [1, 2, 3]) == [2, 3, -1]     # increasing
assert nge_stack([], [1, 2]) == []                       # empty nums1 (outside the limits, harmless)
assert nge_stack([-3, -1], [-3, -2, -1]) == [-2, -1]  # negatives
big = list(range(10_000, 0, -1)) + [10_001]
assert nge_stack([10_000, 1], big) == [10_001, 10_001]   # one big pop cascade (n = 10^4)

# seeded randomised cross-check
rng = random.Random(8)
for _ in range(1000):
    n = rng.randint(1, 9)
    nums2 = rng.sample(range(-10, 20), n)                # distinct values
    nums1 = rng.sample(nums2, rng.randint(1, n))
    assert nge_stack(nums1, nums2) == nge_brute(nums1, nums2), (nums1, nums2)
print("random cross-check passed: 1000 cases")
