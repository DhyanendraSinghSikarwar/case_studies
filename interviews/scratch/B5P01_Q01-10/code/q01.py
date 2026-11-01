import random


def dup_brute(nums):
    n = len(nums)
    return any(nums[i] == nums[j] for i in range(n) for j in range(i + 1, n))


def dup_set(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def dup_len(nums):
    return len(set(nums)) != len(nums)


def dup_sort(nums):
    s = sorted(nums)  # copy, input untouched; use nums.sort() for O(1) extra if allowed
    return any(s[i] == s[i + 1] for i in range(len(s) - 1))


print("example 1:", dup_set([1, 2, 3, 1]), "(expected True)")
print("example 2:", dup_set([1, 2, 3, 4]), "(expected False)")

random.seed(1)
for _ in range(500):
    a = [random.randint(-6, 6) for _ in range(random.randint(0, 9))]
    b = dup_brute(a)
    assert dup_set(a) == b == dup_len(a) == dup_sort(a), a
print("cross-check: 500 seeded cases agree")

assert dup_set([]) is False
assert dup_set([7]) is False
assert dup_set([5, 5]) is True
assert dup_set([-10**9, 10**9]) is False
assert dup_set([0, 0, 0]) is True
assert dup_sort([2, 1, 2]) is True
print("edge asserts passed")
