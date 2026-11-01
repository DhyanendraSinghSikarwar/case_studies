import random


def squares_brute(nums):
    return sorted(x * x for x in nums)


def squares_two_pointers(nums):
    n = len(nums)
    out = [0] * n
    i, j = 0, n - 1
    for w in range(n - 1, -1, -1):          # fill from the back, largest first
        a, b = nums[i] * nums[i], nums[j] * nums[j]
        if a > b:
            out[w] = a
            i += 1
        else:
            out[w] = b
            j -= 1
    return out


print(squares_two_pointers([-4, -1, 0, 3, 10]))
print(squares_two_pointers([-7, -3, 2, 3, 11]))
assert squares_two_pointers([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
assert squares_two_pointers([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
assert squares_two_pointers([5]) == [25]
assert squares_two_pointers([-5]) == [25]
assert squares_two_pointers([-3, -2, -1]) == [1, 4, 9]     # all negative
assert squares_two_pointers([1, 2, 3]) == [1, 4, 9]        # all non-negative
assert squares_two_pointers([-2, -2, 2, 2]) == [4, 4, 4, 4]  # ties
assert squares_two_pointers([0, 0, 0]) == [0, 0, 0]

rng = random.Random(21)
cases = 0
for _ in range(2000):
    n = rng.randint(1, 10)
    nums = sorted(rng.randint(-8, 8) for _ in range(n))
    assert squares_two_pointers(nums) == squares_brute(nums), nums
    cases += 1
print("random cross-check passed:", cases, "cases")
