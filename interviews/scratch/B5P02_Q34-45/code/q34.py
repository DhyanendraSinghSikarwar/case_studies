import random
from bisect import bisect_left

def brute_le(nums, k):
    best = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s <= k:
                best = max(best, j - i + 1)
    return best

def naive_window_le(nums, k):
    # shrink-while-too-big: only valid for non-negative values
    l = s = best = 0
    for r, v in enumerate(nums):
        s += v
        while s > k and l <= r:
            s -= nums[l]; l += 1
        best = max(best, r - l + 1)
    return best

def correct_le(nums, k):
    # prefix sums P; want smallest i<=j with P[i] >= P[j]-k.
    # Smallest such i is always a prefix-maximum record, so binary search the records.
    rec_idx, rec_val, p = [0], [0], 0
    best = 0
    for j, v in enumerate(nums, 1):
        p += v
        # records have strictly increasing values; first record with value >= p-k
        pos = bisect_left(rec_val, p - k)
        if pos < len(rec_val):
            best = max(best, j - rec_idx[pos])
        if p > rec_val[-1]:
            rec_idx.append(j); rec_val.append(p)
    return best

def brute_eq(nums, k):
    best = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s == k:
                best = max(best, j - i + 1)
    return best

def longest_eq(nums, k):
    first = {0: -1}          # prefix sum -> FIRST index seen (earliest start = longest)
    p = best = 0
    for i, v in enumerate(nums):
        p += v
        if p - k in first:
            best = max(best, i - first[p - k])
        first.setdefault(p, i)   # never overwrite
    return best

# prompt examples
assert brute_le([4, -3, 1], 2) == 3 and correct_le([4, -3, 1], 2) == 3
print("nums=[4,-3,1] k=2: true", brute_le([4, -3, 1], 2), "| naive window", naive_window_le([4, -3, 1], 2), "| prefix+bisect", correct_le([4, -3, 1], 2))
assert naive_window_le([4, -3, 1], 2) == 2
for nums, k, exp in [([1, -1, 5, -2, 3], 3, 4), ([-2, -1, 2, 1], 1, 2)]:
    assert longest_eq(nums, k) == brute_eq(nums, k) == exp
    print("exact", nums, k, "->", longest_eq(nums, k))
# edge cases
assert longest_eq([], 0) == 0 and longest_eq([5], 5) == 1 and longest_eq([5], 4) == 0
assert longest_eq([0, 0, 0], 0) == 3 and longest_eq([1, -1, 1, -1], 0) == 4
assert correct_le([], 5) == 0 and correct_le([-5], -6) == 0 and correct_le([-5], -5) == 1

random.seed(34)
bad_neg = bad_nonneg = 0
for _ in range(1500):
    n = random.randint(0, 9)
    nums = [random.randint(-5, 5) for _ in range(n)]
    k = random.randint(-6, 8)
    assert longest_eq(nums, k) == brute_eq(nums, k), (nums, k)
    assert correct_le(nums, k) == brute_le(nums, k), (nums, k)
    if naive_window_le(nums, k) != brute_le(nums, k): bad_neg += 1
    pos = [abs(x) for x in nums]
    kk = abs(k)
    if naive_window_le(pos, kk) != brute_le(pos, kk): bad_nonneg += 1
print("random cases with negatives where naive window is wrong:", bad_neg, "of 1500")
print("random cases with non-negatives where naive window is wrong:", bad_nonneg)
assert bad_neg > 0 and bad_nonneg == 0
print("all checks passed")
