import random
from collections import Counter


def majority_brute(nums):
    n = len(nums)
    for x in nums:
        if sum(1 for y in nums if y == x) > n // 2:
            return x


def majority_counter(nums):
    return Counter(nums).most_common(1)[0][0]


def majority_boyer_moore(nums):
    cand, votes = None, 0
    for x in nums:
        if votes == 0:
            cand = x
        votes += 1 if x == cand else -1
    return cand  # valid only because a majority is GUARANTEED


def majority_verified(nums):
    cand = majority_boyer_moore(nums)
    return cand if nums.count(cand) > len(nums) // 2 else None  # second pass if not guaranteed


print("example:", majority_boyer_moore([2, 2, 1, 1, 1, 2, 2]), "(expected 2)")
print("counts:", dict(Counter([2, 2, 1, 1, 1, 2, 2])), "-> 2 appears 4 > 7//2 = 3")

random.seed(4)
for _ in range(1000):
    n = random.randint(1, 11)
    m = n // 2 + 1  # build an input that has a strict majority
    v = random.randint(-3, 3)
    a = [v] * random.randint(m, n)
    a += [random.randint(-3, 3) for _ in range(n - len(a))]
    random.shuffle(a)
    if a.count(v) <= n // 2:
        continue
    exp = majority_brute(a)
    assert majority_boyer_moore(a) == majority_counter(a) == exp == v, a
print("cross-check: 1000 seeded guaranteed-majority cases agree")

# without the guarantee Boyer-Moore returns a candidate, not a proof
no_maj = [1, 2, 3]
print("no majority [1,2,3]: candidate =", majority_boyer_moore(no_maj), "verified =", majority_verified(no_maj))

assert majority_boyer_moore([5]) == 5
assert majority_boyer_moore([3, 3]) == 3
assert majority_boyer_moore([1, 2, 1]) == 1
assert majority_boyer_moore([-1, -1, 2, 2, -1]) == -1
assert majority_boyer_moore([7] * 5) == 7
assert majority_verified([1, 2, 3]) is None
print("edge asserts passed")
