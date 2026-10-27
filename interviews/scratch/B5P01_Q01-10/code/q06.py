import random


def remove_dups_brute(nums):
    out = []
    for x in nums:
        if not out or out[-1] != x:
            out.append(x)
    nums[:len(out)] = out  # extra O(n) space
    return len(out)


def remove_dups(nums):
    if not nums:
        return 0
    w = 1  # nums[:w] = distinct values so far, strictly increasing
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:
            nums[w] = nums[r]
            w += 1
    return w


a = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k = remove_dups(a)
print("example:", "k =", k, "prefix =", a[:k], "(expected k=5, [0, 1, 2, 3, 4])")

random.seed(6)
for _ in range(1000):
    x = sorted(random.randint(-4, 4) for _ in range(random.randint(0, 12)))
    e, f = x[:], x[:]
    k1 = remove_dups_brute(e)
    k2 = remove_dups(f)
    assert k1 == k2 == len(set(x)), x
    assert e[:k1] == f[:k2] == sorted(set(x)), x
print("cross-check: 1000 seeded sorted cases agree")

for case, exp in (([], 0), ([7], 1), ([2, 2], 1), ([1, 2, 3], 3), ([5, 5, 5, 5], 1), ([-3, -3, 0, 0, 4], 3)):
    c = case[:]
    k = remove_dups(c)
    assert k == exp and c[:k] == sorted(set(case)), case
print("edge asserts passed")

# the tail is unspecified: show it is left as junk, not cleaned
b = [1, 1, 2]
kb = remove_dups(b)
print("tail left as is:", b, "k =", kb)
