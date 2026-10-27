import random


def del_brute(nums):
    best = 0
    for d in range(len(nums)):
        rest = nums[:d] + nums[d + 1:]
        run = 0
        for x in rest:
            run = run + 1 if x == 1 else 0
            best = max(best, run)
    return best


def del_window(nums):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > 1:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left)  # window length minus the one forced deletion
    return best


print("[1,1,0,1]:", del_window([1, 1, 0, 1]), "(expected 3)")
print("[0,1,1,1,0,1,1,0,1]:", del_window([0, 1, 1, 1, 0, 1, 1, 0, 1]), "(expected 5)")
print("[1,1,1]:", del_window([1, 1, 1]), "(expected 2)")

random.seed(29)
for _ in range(1000):
    n = random.randint(1, 12)
    nums = [random.randint(0, 1) for _ in range(n)]
    assert del_window(nums) == del_brute(nums), nums
print("cross-check: 1000 seeded cases agree")

assert del_window([0]) == 0
assert del_window([1]) == 0  # delete the only element, nothing left
assert del_window([0, 0, 0]) == 0
assert del_window([1, 0]) == 1
assert del_window([1, 0, 1]) == 2
assert del_window([1, 1, 1, 1]) == 3
assert del_window([1] * 10 ** 5) == 10 ** 5 - 1
assert del_window([0] * 10 ** 5) == 0
print("edge asserts passed")
