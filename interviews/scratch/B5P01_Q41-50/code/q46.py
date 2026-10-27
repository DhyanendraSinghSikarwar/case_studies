from collections import Counter
from itertools import combinations
import random

def brute(nums):                                   # O(n^4): ordered tuples of 4 distinct indices
    n, cnt = len(nums), 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if len({a, b, c, d}) == 4 and nums[a] * nums[b] == nums[c] * nums[d]:
                        cnt += 1
    return cnt

def optimal(nums):                                 # O(n^2) time and space; needs DISTINCT values
    prod = Counter(x * y for x, y in combinations(nums, 2))
    return 8 * sum(c * (c - 1) // 2 for c in prod.values())
# Why 8: two unordered pairs {a,b},{c,d} with equal product. Swap inside pair 1 (2), inside pair 2 (2),
# and swap which pair is on the left of '==' (2): 2*2*2 = 8 ordered tuples.
# Why no overlap: distinct values and equal product => two different pairs sharing an element would share
# the other element too (x*y == x*z => y == z), so they would be the same pair.

assert brute([2, 3, 4, 6]) == optimal([2, 3, 4, 6]) == 8
assert brute([1, 2, 4, 5, 10]) == optimal([1, 2, 4, 5, 10]) == 16
print("examples:", optimal([2, 3, 4, 6]), optimal([1, 2, 4, 5, 10]))

rng = random.Random(46)
for _ in range(400):
    pool = list(range(1, 25)); rng.shuffle(pool)
    a = pool[:rng.randint(0, 9)]                   # distinct positive values
    assert brute(a) == optimal(a), a
print("400 seeded cross-checks passed")

# what goes wrong with duplicates (outside the stated constraints)
dup = [2, 2, 1, 4]
print("duplicates [2,2,1,4]: brute =", brute(dup), "optimal =", optimal(dup), "(optimal is not valid for non-distinct input)")

assert optimal([]) == 0 and optimal([5]) == 0 and optimal([1, 2, 3]) == 0
assert optimal([1, 2, 3, 6]) == 8                  # 1*6 == 2*3
assert optimal([1, 2, 3, 4]) == 0
big = list(range(1, 1001))                         # n = 1000 -> ~500k pair products
print("n=1000 (1..1000):", optimal(big))
assert optimal([10**9, 1, 10**9 - 1, 10**9 + 1]) == 0   # large values: exact ints, no overflow
print("edge asserts passed")
