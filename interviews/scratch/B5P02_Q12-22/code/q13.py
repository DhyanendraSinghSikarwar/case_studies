import random

def brute(nums):
    return sorted(nums)

def optimal(nums):
    low, mid, high = 0, 0, len(nums) - 1
    # [0, low) = 0s, [low, mid) = 1s, [mid, high] = unknown, (high, end) = 2s
    while mid <= high:
        v = nums[mid]
        if v == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif v == 1:
            mid += 1
        else:  # 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1          # do NOT advance mid: the swapped-in value is unseen
    return nums

def run(a):
    a = list(a)
    optimal(a)
    return a

assert run([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]
assert run([2, 0, 1]) == [0, 1, 2]
assert run([]) == []
assert run([1]) == [1]
assert run([2, 2, 2]) == [2, 2, 2]
assert run([0, 0, 0]) == [0, 0, 0]
assert run([2, 1, 0]) == [0, 1, 2]
assert run([1, 1, 1]) == [1, 1, 1]
assert run([2, 0]) == [0, 2]
# the in-place function really mutates its argument and returns the same object
x = [1, 0, 2]
assert optimal(x) is x and x == [0, 1, 2]

rng = random.Random(13)
for _ in range(800):
    a = [rng.randint(0, 2) for _ in range(rng.randint(0, 12))]
    assert run(a) == brute(a), a
print("800 random cases agree with sorted()")
print(run([2, 0, 2, 1, 1, 0]), run([2, 0, 1]))
# what goes wrong if mid advances after the swap with high
def buggy(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]; low += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]; high -= 1; mid += 1
    return nums
print("buggy on [1, 2, 0]:", buggy([1, 2, 0]))
