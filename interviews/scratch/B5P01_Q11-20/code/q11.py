import random
from math import prod

def brute(nums):
    return [prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]

def optimal(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):          # out[i] = product of everything left of i
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):   # multiply in product of everything right of i
        out[i] *= right
        right *= nums[i]
    return out

assert optimal([1, 2, 3, 4]) == [24, 12, 8, 6]
assert optimal([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert optimal([0, 0, 2]) == [0, 0, 0]
assert optimal([5]) == [1]          # empty product is 1
assert optimal([2, 3]) == [3, 2]
assert optimal([0, 4]) == [4, 0]
assert optimal([]) == []

rng = random.Random(11)
for _ in range(500):
    a = [rng.randint(-4, 4) for _ in range(rng.randint(0, 8))]
    assert optimal(a) == brute(a), a
print("500 random cases agree with brute force")
print(optimal([1, 2, 3, 4]), optimal([-1, 1, 0, -3, 3]), optimal([0, 0, 2]), optimal([5]))
