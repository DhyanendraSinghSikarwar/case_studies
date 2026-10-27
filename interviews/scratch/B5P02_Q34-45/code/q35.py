import random
from collections import defaultdict

# (a) longest subarray with sum <= k, non-negative values
def a_brute(nums, k):
    return max([j - i for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if sum(nums[i:j]) <= k] or [0])
def a_window(nums, k):
    l = s = best = 0
    for r, v in enumerate(nums):
        s += v
        while s > k and l <= r:
            s -= nums[l]; l += 1
        best = max(best, r - l + 1)
    return best

# (c) count subarrays with at most k distinct
def c_brute(nums, k):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if len(set(nums[i:j])) <= k)
def c_window(nums, k):
    if k < 0: return 0
    cnt = defaultdict(int); l = total = 0
    for r, v in enumerate(nums):
        cnt[v] += 1
        while len(cnt) > k:
            cnt[nums[l]] -= 1
            if cnt[nums[l]] == 0: del cnt[nums[l]]
            l += 1
        total += r - l + 1
    return total

# (d) longest subarray with exactly k distinct (length only)
def d_brute(nums, k):
    return max([j - i for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if len(set(nums[i:j])) == k] or [0])
def d_window(nums, k):
    cnt = defaultdict(int); l = best = 0
    for r, v in enumerate(nums):
        cnt[v] += 1
        while len(cnt) > k:
            cnt[nums[l]] -= 1
            if cnt[nums[l]] == 0: del cnt[nums[l]]
            l += 1
        if len(cnt) == k:           # the at-most-k window is also the longest exactly-k one ending at r
            best = max(best, r - l + 1)
    return best

# (e) shortest subarray with sum >= k, non-negative values
def e_brute(nums, k):
    return min([j - i for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if sum(nums[i:j]) >= k] or [0])
def e_window(nums, k):
    l = s = 0; best = 0
    for r, v in enumerate(nums):
        s += v
        while s >= k and l <= r:
            best = r - l + 1 if best == 0 else min(best, r - l + 1)
            s -= nums[l]; l += 1
    return best

# (b) the same as (a) but with negatives: the window is wrong
print("(b) nums=[4,-3,1], k=2: true", a_brute([4, -3, 1], 2), "window", a_window([4, -3, 1], 2))
assert a_brute([4, -3, 1], 2) == 3 and a_window([4, -3, 1], 2) == 2
print("(a) nums=[1,2,3], k=3:", a_window([1, 2, 3], 3))
assert a_window([1, 2, 3], 3) == a_brute([1, 2, 3], 3) == 2
# (d) failing case for the NAIVE idea "shrink while distinct != k" (not monotone): shows why we shrink on > k only
print("(d) [1,2,1,2,3], k=2 ->", d_window([1, 2, 1, 2, 3], 2), "; (c) at most 2 ->", c_window([1, 2, 1, 2, 3], 2))
assert d_window([1, 2, 1, 2, 3], 2) == 4 and c_window([1, 2, 1, 2, 3], 2) == 12
# (c) exactly-k COUNT with one window is not possible: a window with exactly k can start in many places
assert d_window([], 1) == 0 and e_window([], 1) == 0 and d_window([7], 2) == 0 and d_window([7], 1) == 1

random.seed(35)
for _ in range(1500):
    n = random.randint(0, 9)
    nn = [random.randint(0, 5) for _ in range(n)]
    k = random.randint(1, 12)
    assert a_window(nn, k) == a_brute(nn, k), (nn, k)
    assert e_window(nn, max(k, 1)) == e_brute(nn, max(k, 1)), (nn, k)
    vals = [random.randint(1, 4) for _ in range(n)]
    kd = random.randint(1, 4)
    assert c_window(vals, kd) == c_brute(vals, kd), (vals, kd)
    assert d_window(vals, kd) == d_brute(vals, kd), (vals, kd)
print("(a), (c), (d), (e) match brute force on 1500 seeded cases each")
