import random


def check_brute(nums, k):
    n = len(nums)
    for i in range(n):
        s = nums[i]
        for j in range(i + 1, n):          # length >= 2
            s += nums[j]
            if (s == 0) if k == 0 else (s % k == 0):
                return True
    return False


def check_hash(nums, k):
    first = {0: -1}                         # empty prefix "ends" at index -1
    p = 0
    for i, x in enumerate(nums):
        p += x
        r = p % k if k else p               # k == 0: need an equal prefix sum
        if r in first:
            if i - first[r] >= 2:           # length at least 2
                return True
        else:
            first[r] = i                    # keep the EARLIEST index only
    return False


print(check_hash([23, 2, 4, 6, 7], 6), check_hash([23, 2, 6, 4, 7], 13))
assert check_hash([23, 2, 4, 6, 7], 6) is True
assert check_hash([23, 2, 6, 4, 7], 13) is False

# --- why length >= 2 matters: without it, one element can qualify
print("[6], k=6 ->", check_hash([6], 6), "(a single 6 is a multiple but length 1)")
assert check_hash([6], 6) is False and check_hash([6, 0], 6) is True

# --- edge cases
assert check_hash([], 5) is False
assert check_hash([0], 1) is False
assert check_hash([0, 0], 1) is True
assert check_hash([0, 0], 0) is True          # k = 0: sum must be exactly 0
assert check_hash([1, 0], 0) is False
assert check_hash([5, 0, 0], 0) is True
assert check_hash([1, 2], 1) is True          # k = 1: every sum qualifies
assert check_hash([23, 2, 6, 4, 7], 6) is True    # whole array sums to 42
assert check_hash([1, 1], 3) is False
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(25)
for _ in range(2000):
    n = rng.randint(0, 8)
    nums = [rng.randint(0, 9) for _ in range(n)]
    k = rng.randint(0, 9)
    assert check_hash(nums, k) == check_brute(nums, k), (nums, k)
print("2000 random cases OK")
