from collections import Counter
import random

def brute(nums):                                   # O(n^2)
    n = len(nums)
    return sum(j - i != nums[j] - nums[i] for i in range(n) for j in range(i + 1, n))

def optimal(nums):                                 # O(n) time, O(n) space
    n = len(nums)
    total = n * (n - 1) // 2
    seen, good = Counter(), 0
    for i, v in enumerate(nums):
        key = v - i                                # j-i == nums[j]-nums[i]  <=>  nums[j]-j == nums[i]-i
        good += seen[key]                          # earlier indices with the same key form good pairs
        seen[key] += 1
    return total - good

def optimal_single_pass(nums):                     # count bad pairs directly: i - (earlier with same key)
    seen, bad = Counter(), 0
    for i, v in enumerate(nums):
        bad += i - seen[v - i]
        seen[v - i] += 1
    return bad

assert brute([4, 1, 3, 3]) == optimal([4, 1, 3, 3]) == optimal_single_pass([4, 1, 3, 3]) == 5
assert brute([1, 2, 3, 4, 5]) == optimal([1, 2, 3, 4, 5]) == 0
print("examples: [4,1,3,3] ->", optimal([4, 1, 3, 3]), "; [1,2,3,4,5] ->", optimal([1, 2, 3, 4, 5]))

rng = random.Random(44)
for _ in range(600):
    a = [rng.randint(-8, 8) for _ in range(rng.randint(0, 12))]
    assert brute(a) == optimal(a) == optimal_single_pass(a), a
print("600 seeded cross-checks passed")

assert optimal([]) == 0 and optimal([7]) == 0
assert optimal([5, 5, 5, 5]) == 6                  # all equal: keys 5,4,3,2 all different -> all pairs bad
assert optimal([0, 1, 2, 3]) == 0                  # v - i constant -> no bad pairs
assert optimal([-3, -2, -1]) == 0                  # negatives fine
big = list(range(10**5))
assert optimal(big) == 0
assert optimal([0] * 10**5) == 10**5 * (10**5 - 1) // 2   # no overflow in Python
print("edge asserts passed (incl. n = 10^5)")
