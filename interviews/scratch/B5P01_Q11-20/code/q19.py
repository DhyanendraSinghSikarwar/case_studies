import random
from collections import Counter

def brute(nums):
    for i, x in enumerate(nums):
        if nums.count(x) == 1:       # O(n) each -> O(n^2)
            return x
    return -1

def two_pass(nums):
    c = Counter(nums)
    for x in nums:
        if c[x] == 1:
            return x
    return -1

def one_pass(nums):
    # dict keeps first-seen order; value True = still unique, False = seen again
    uniq = {}
    for x in nums:
        uniq[x] = x not in uniq      # first time True, any repeat False
    for x, ok in uniq.items():       # scans distinct values, not the whole list
        if ok:
            return x
    return -1

for f in (brute, two_pass, one_pass):
    assert f([4, 5, 1, 2, 0, 4]) == 5
    assert f([7, 7]) == -1
    assert f([]) == -1
    assert f([3]) == 3
    assert f([1, 1, 2, 2, 3]) == 3
    assert f([-1, 2, -1, 2]) == -1
    assert f([0, 0, 9]) == 9         # a 0 answer must not be confused with falsy 'none'
    assert f([5, 6, 5]) == 6
assert one_pass([0, 1, 1]) == 0      # unique value 0 is a valid answer
print("sentinel clash: [-1,2,2] returns", two_pass([-1, 2, 2]), "which is a real answer AND the 'none' marker")

rng = random.Random(19)
for _ in range(1000):
    a = [rng.randint(-3, 5) for _ in range(rng.randint(0, 10))]
    assert brute(a) == two_pass(a) == one_pass(a), a
print("1000 random cases agree")
print(two_pass([4, 5, 1, 2, 0, 4]), two_pass([7, 7]))
