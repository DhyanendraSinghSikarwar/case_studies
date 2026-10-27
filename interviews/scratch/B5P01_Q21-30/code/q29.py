import random
from collections import Counter


def sort_brute(nums):
    return sorted(nums, key=lambda x: (-nums.count(x), x))      # O(n^2) counts


def sort_freq(nums):
    cnt = Counter(nums)
    return sorted(nums, key=lambda x: (-cnt[x], x))


def sort_freq_no_tiebreak(nums):
    cnt = Counter(nums)
    return sorted(nums, key=lambda x: -cnt[x])      # relies on stability only


print(sort_freq([1, 1, 2, 2, 2, 3]), sort_freq([2, 3, 1, 3, 2]))
assert sort_freq([1, 1, 2, 2, 2, 3]) == [2, 2, 2, 1, 1, 3]
assert sort_freq([2, 3, 1, 3, 2]) == [2, 2, 3, 3, 1]

# stability alone breaks ties by first position, not by value
t = [3, 2, 2, 3, 1]
print("explicit tie-break  :", sort_freq(t))
print("stability only      :", sort_freq_no_tiebreak(t), "(3s before 2s: wrong)")
assert sort_freq(t) == [2, 2, 3, 3, 1]
assert sort_freq_no_tiebreak(t) == [3, 3, 2, 2, 1]

# --- edge cases
assert sort_freq([]) == []
assert sort_freq([5]) == [5]
assert sort_freq([4, 4, 4]) == [4, 4, 4]
assert sort_freq([3, 2, 1]) == [1, 2, 3]            # all frequency 1: by value
assert sort_freq([-1, -1, 2, 2, 0]) == [-1, -1, 2, 2, 0]
assert sort_freq([2, 2, -3, -3]) == [-3, -3, 2, 2]  # tie: smaller value first
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(29)
for _ in range(2000):
    nums = [rng.randint(-4, 4) for _ in range(rng.randint(0, 14))]
    assert sort_freq(nums) == sort_brute(nums), nums
print("2000 random cases OK")
