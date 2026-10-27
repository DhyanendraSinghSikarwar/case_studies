import random


def nge_circ_brute(nums):
    n = len(nums)
    res = []
    for i in range(n):
        ans = -1
        for step in range(1, n):                 # at most one trip around, excluding i itself
            v = nums[(i + step) % n]
            if v > nums[i]:
                ans = v
                break
        res.append(ans)
    return res


def nge_circ(nums, depth=None):
    n = len(nums)
    res = [-1] * n
    stack = []                                   # indices with no greater value found yet
    for i in range(2 * n):
        v = nums[i % n]
        while stack and nums[stack[-1]] < v:
            res[stack.pop()] = v
        if i < n:                                # push only in the first pass
            stack.append(i)
        if depth is not None:
            depth.append(len(stack))
    return res


def nge_circ_pushall(nums, depth=None):
    # pushes in both passes: still correct here (duplicate entries only re-write the same value),
    # but the stack can hold up to 2n entries and the second pass resolves nothing new
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        v = nums[i % n]
        while stack and nums[stack[-1] % n] < v:
            res[stack.pop() % n] = v
        stack.append(i)
        if depth is not None:
            depth.append(len(stack))
    return res


examples = [([1, 2, 1], [2, -1, 2]), ([1, 2, 3, 4, 3], [2, 3, 4, -1, 4]), ([5, 5], [-1, -1])]
for nums, want in examples:
    assert nge_circ(nums) == nge_circ_brute(nums) == want, nums
    print(nums, "->", nge_circ(nums))

# edge cases
assert nge_circ([7]) == [-1]                              # single element: itself is not greater than itself
assert nge_circ([3, 3, 3]) == [-1, -1, -1]                # all equal
assert nge_circ([3, 2, 1]) == [-1, 3, 3]                  # decreasing: wraps to the front
assert nge_circ([1, 5, 1, 1]) == [5, -1, 5, 5]            # duplicates around the maximum
n = 10_000
assert nge_circ(list(range(n, 0, -1)))[1:] == [n] * (n - 1)       # max size
assert nge_circ(list(range(n))) == list(range(1, n)) + [-1]

# why a second pass must not push: measure the stack depth on a decreasing array
dec = list(range(1000, 0, -1))
d1, d2 = [], []
nge_circ(dec, d1)
nge_circ_pushall(dec, d2)
print("max stack size, push in pass 1 only:", max(d1), "; push in both passes:", max(d2))
assert max(d1) == 1000 and max(d2) >= max(d1)
print("pushes: pass-1-only", 1000, "vs both passes", 2000, "(the extra 1000 can never resolve anything new)")

# seeded randomised cross-check (small range for many ties)
rng = random.Random(17)
for _ in range(3000):
    nums = [rng.randint(-3, 5) for _ in range(rng.randint(1, 10))]
    assert nge_circ(nums) == nge_circ_brute(nums), nums
    assert nge_circ_pushall(nums) == nge_circ_brute(nums), nums   # same answers, just wasteful
print("random cross-check passed: 3000 cases")
