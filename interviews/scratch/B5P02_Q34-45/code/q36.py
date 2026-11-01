import random

def window_sums(nums, k):
    n = len(nums)
    if k <= 0 or k > n:
        return []
    s = sum(nums[:k])                 # first full window: indices 0..k-1, complete at r = k-1
    out = [s]
    for r in range(k, n):             # r enters, r-k leaves
        s += nums[r] - nums[r - k]
        out.append(s)
    return out

def brute(nums, k):
    return [sum(nums[i:i + k]) for i in range(len(nums) - k + 1)] if 0 < k <= len(nums) else []

nums, k = [1, 3, 2, 6, -1, 4, 1, 8, 2], 5
ws = window_sums(nums, k)
print("n =", len(nums), "k =", k, "windows =", len(ws), "(n-k+1 =", len(nums) - k + 1, ")")
print("window sums:", ws, "max:", max(ws))
assert ws == [11, 14, 12, 18, 14] and max(ws) == 18 and len(ws) == len(nums) - k + 1
# formulas
l, r = 3, 7
print("inclusive [3,7] length", r - l + 1, "| half-open [3,8) length", 8 - 3)
# the three bugs, each shown
wrong_drop = []  # bug: drop nums[r-k+1] instead of nums[r-k]
s = sum(nums[:k]); wrong_drop.append(s)
for r in range(k, len(nums)):
    s += nums[r] - nums[r - k + 1]
    wrong_drop.append(s)
print("bug (drop nums[r-k+1]) gives", wrong_drop, "-> wrong")
assert wrong_drop != ws
# edges
assert window_sums([], 3) == [] and window_sums([5], 1) == [5] and window_sums([1, 2], 3) == [] and window_sums([1, 2], 2) == [3]
assert window_sums([2, 2, 2], 0) == []
random.seed(36)
for _ in range(1000):
    a = [random.randint(-9, 9) for _ in range(random.randint(0, 12))]
    kk = random.randint(0, 14)
    assert window_sums(a, kk) == brute(a, kk)
print("1000 seeded random cases match brute force; edges pass")
