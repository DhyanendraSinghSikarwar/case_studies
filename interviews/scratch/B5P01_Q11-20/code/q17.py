import random
from collections import Counter

def brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] == nums[j])

def running(nums):                   # count equal values seen before
    seen = {}
    ans = 0
    for x in nums:
        ans += seen.get(x, 0)
        seen[x] = seen.get(x, 0) + 1
    return ans

def closed_form(nums):
    return sum(c * (c - 1) // 2 for c in Counter(nums).values())

assert running([1, 2, 3, 1, 1, 3]) == closed_form([1, 2, 3, 1, 1, 3]) == 4
assert running([1, 1, 1, 1]) == closed_form([1, 1, 1, 1]) == 6
assert running([]) == closed_form([]) == 0
assert running([5]) == closed_form([5]) == 0
assert running([1, 2, 3]) == closed_form([1, 2, 3]) == 0
assert closed_form([7] * 100000) == 100000 * 99999 // 2     # no overflow in Python

rng = random.Random(17)
for _ in range(500):
    a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 12))]
    assert running(a) == closed_form(a) == brute(a), a
print("500 random cases agree")
print(running([1, 2, 3, 1, 1, 3]), closed_form([1, 1, 1, 1]), closed_form([7] * 100000))
