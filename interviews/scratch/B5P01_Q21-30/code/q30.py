import random
from collections import Counter


def maj3_brute(nums):
    n = len(nums)
    c = Counter(nums)
    return sorted(v for v, k in c.items() if k > n // 3)


def candidates(nums):
    """Pass 1: the two survivors of the pairing-off. Only POSSIBLE winners."""
    c1 = c2 = None
    n1 = n2 = 0
    for x in nums:
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:                         # three distinct values: cancel one of each
            n1 -= 1
            n2 -= 1
    return {c for c in (c1, c2) if c is not None}


def maj3_vote(nums):
    n = len(nums)
    cand = candidates(nums)
    # pass 2: verify (this is a count, still O(n) for two candidates)
    return sorted(c for c in cand if nums.count(c) > n // 3)


for arr, want in [([3, 2, 3], [3]), ([1, 2], [1, 2]), ([1], [1])]:
    print(arr, "->", maj3_vote(arr))
    assert maj3_vote(arr) == want == maj3_brute(arr)

# why verification: survivors are not always winners
for w in ([1, 2, 3], [1, 2, 3, 4, 5, 6, 7]):
    print(w, "survivors:", sorted(candidates(w)), "-> verified answer:", maj3_vote(w))
    assert maj3_vote(w) == []
assert sorted(candidates([1, 2, 3])) == [1, 2]

# --- edge cases
assert maj3_vote([]) == []
assert maj3_vote([2, 2]) == [2]
assert maj3_vote([0, 0, 0]) == [0]               # candidate value 0 is not None
assert maj3_vote([1, 1, 1, 2, 2, 2, 3]) == [1, 2]
assert maj3_vote([-1, -1, 5, 5, 7, 7]) == maj3_brute([-1, -1, 5, 5, 7, 7])
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(30)
for _ in range(3000):
    nums = [rng.randint(-3, 3) for _ in range(rng.randint(0, 15))]
    assert maj3_vote(nums) == maj3_brute(nums), nums
print("3000 random cases OK")
