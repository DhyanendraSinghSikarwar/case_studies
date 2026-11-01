import random
from collections import Counter

def brute(nums):
    # stable reference: evens then odds, any order inside is allowed so only the property is checked
    return [x for x in nums if x % 2 == 0] + [x for x in nums if x % 2 == 1]

def optimal(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        if nums[l] % 2 == 0:
            l += 1
        elif nums[r] % 2 == 1:
            r -= 1
        else:                      # left is odd, right is even: swap them
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
    return nums

def valid(before, after):
    if Counter(before) != Counter(after):
        return False
    seen_odd = False
    for x in after:
        if x % 2 == 1:
            seen_odd = True
        elif seen_odd:
            return False
    return True

def run(a):
    b = list(a)
    optimal(b)
    assert valid(a, b), (a, b)
    return b

print("example result:", run([3, 1, 2, 4]))
run([]); run([7]); run([2]); run([2, 4, 6]); run([1, 3, 5]); run([1, 2]); run([2, 1])
run([0, 0, 1]); run([-3, -2, 5, 8])      # negatives: use x % 2 (Python gives 0 or 1 for negatives)
run([3, 1, 2, 4])
rng = random.Random(18)
for _ in range(1000):
    a = [rng.randint(-6, 9) for _ in range(rng.randint(0, 12))]
    run(a)
    assert valid(a, brute(a))
print("1000 random cases satisfy the parity property")
print("order change example:", run([1, 2, 3, 4]), "(stable would give [2, 4, 1, 3])")
