import random


def move_zeroes_brute(nums):
    # extra space: build a new list, then copy back
    non = [x for x in nums if x != 0]
    non += [0] * (len(nums) - len(non))
    nums[:] = non


def move_zeroes(nums):
    w = 0  # next slot for a non-zero value; nums[:w] are all non-zero, in order
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[w] = nums[r]
            w += 1
    for i in range(w, len(nums)):
        nums[i] = 0


def move_zeroes_swap(nums):
    # one pass, swaps only when needed (skips self-writes when no zero seen yet)
    w = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            if r != w:
                nums[w], nums[r] = nums[r], nums[w]
            w += 1


a = [0, 1, 0, 3, 12]
move_zeroes(a)
print("example 1:", a, "(expected [1, 3, 12, 0, 0])")
b = [0]
move_zeroes(b)
print("example 2:", b, "(expected [0])")

random.seed(5)
for _ in range(1000):
    x = [random.choice([0, 0, 1, 2, -3]) for _ in range(random.randint(0, 10))]
    e, f, g = x[:], x[:], x[:]
    move_zeroes_brute(e)
    move_zeroes(f)
    move_zeroes_swap(g)
    assert e == f == g, x
print("cross-check: 1000 seeded cases agree")

# count writes: two-pass writes (#nonzero + #trailing zeros), swap version writes only when r != w
def writes_swap(nums):
    w = 0
    cnt = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            if r != w:
                cnt += 2  # a swap touches two slots
            w += 1
    return cnt


sample = [1, 2, 3, 0, 4]
print("swap writes on [1,2,3,0,4]:", writes_swap(sample), "| two-pass writes:", 4 + 1)
print("swap writes on all non-zero [1,2,3]:", writes_swap([1, 2, 3]))

for case in ([], [0, 0, 0], [1, 2, 3], [5], [0, 0, 1], [-1, 0, -2]):
    c = case[:]
    move_zeroes(c)
    d = case[:]
    move_zeroes_swap(d)
    assert c == d == [v for v in case if v] + [0] * case.count(0)
print("edge asserts passed")
