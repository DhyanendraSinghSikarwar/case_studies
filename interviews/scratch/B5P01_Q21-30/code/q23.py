import random
from collections import Counter
from itertools import product


def four_sum_brute(A, B, C, D):
    return sum(1 for a, b, c, d in product(A, B, C, D) if a + b + c + d == 0)


def four_sum_count(A, B, C, D):
    ab = Counter(a + b for a in A for b in B)      # O(n^2) time and space
    total = 0
    for c in C:
        for d in D:
            total += ab.get(-(c + d), 0)           # .get: no key inserted
    return total


A, B, C, D = [1, 2], [-2, -1], [-1, 2], [0, 2]
print("example:", four_sum_count(A, B, C, D))
assert four_sum_count(A, B, C, D) == 2 == four_sum_brute(A, B, C, D)

# --- edge cases
assert four_sum_count([0], [0], [0], [0]) == 1
assert four_sum_count([1], [1], [1], [1]) == 0
assert four_sum_count([0] * 5, [0] * 5, [0] * 5, [0] * 5) == 5 ** 4   # all equal
assert four_sum_count([-1, -1], [1, 1], [-1, -1], [1, 1]) == 16
assert four_sum_count([10 ** 9], [-10 ** 9], [10 ** 9], [-10 ** 9]) == 1  # no overflow
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(23)
for _ in range(500):
    n = rng.randint(1, 5)
    lists = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(4)]
    assert four_sum_count(*lists) == four_sum_brute(*lists)
print("500 random cases OK")

# --- size note: n=200 -> 40,000 pair sums stored, 40,000 lookups
n = 200
rng = random.Random(1)
big = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(n)] for _ in range(4)]
print("n=200 result runs fine, pair sums stored <=", n * n, "; n^4 =", n ** 4)
four_sum_count(*big)
