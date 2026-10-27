import random
from sortedcontainers import SortedList

def brute(nums, k, t):                             # O(n * k)
    n = len(nums)
    return any(abs(nums[i] - nums[j]) <= t for i in range(n) for j in range(i + 1, min(n, i + k + 1)))

def buckets(nums, k, t):                           # O(n) average time, O(min(n, k)) space
    if k <= 0 or t < 0: return False
    w, box = t + 1, {}                             # bucket id = x // w; two values in one bucket differ by <= t
    for i, x in enumerate(nums):
        b = x // w                                 # floor division: correct for negatives in Python
        if b in box: return True                   # same bucket
        if b - 1 in box and x - box[b - 1] <= t: return True    # neighbour buckets: check the actual gap
        if b + 1 in box and box[b + 1] - x <= t: return True
        box[b] = x                                 # at most one value per bucket (else we would have returned)
        if i >= k: del box[nums[i - k] // w]       # keep only the last k values
    return False

def sorted_list(nums, k, t):                       # O(n log k)
    if k <= 0 or t < 0: return False
    sl = SortedList()
    for i, x in enumerate(nums):
        j = sl.bisect_left(x - t)                  # first stored value >= x - t
        if j < len(sl) and sl[j] <= x + t: return True
        sl.add(x)
        if i >= k: sl.remove(nums[i - k])
    return False

for args, want in [(([1, 2, 3, 1], 3, 0), True), (([1, 5, 9, 1, 5, 9], 2, 3), False)]:
    assert brute(*args) == buckets(*args) == sorted_list(*args) == want
print("examples:", buckets([1, 2, 3, 1], 3, 0), buckets([1, 5, 9, 1, 5, 9], 2, 3))

rng = random.Random(48)
for _ in range(2000):
    n = rng.randint(0, 12)
    a = [rng.randint(-15, 15) for _ in range(n)]
    k, t = rng.randint(0, 5), rng.randint(0, 6)
    r = brute(a, k, t)
    assert buckets(a, k, t) == r == sorted_list(a, k, t), (a, k, t)
print("2000 seeded cross-checks passed (brute == buckets == SortedList)")

assert buckets([], 3, 0) is False and buckets([5], 3, 0) is False
assert buckets([1, 1], 0, 5) is False              # indexDiff 0: i != j impossible
assert buckets([1, 1], 1, 0) is True
assert buckets([-1, 1], 1, 2) is True              # negatives straddle zero: -1//3=-1, 1//3=0, neighbour check
assert buckets([-1, 1], 1, 1) is False
assert buckets([0, 10**9 * 2], 1, 10**9 * 2) is True
assert buckets([1, 3], 1, -1) is False            # negative valueDiff
assert buckets([8, 4, 12], 2, 3) is False and buckets([8, 4, 12], 2, 4) is True
assert buckets(list(range(0, 10**5, 7)), 5, 6) is True
print("edge asserts passed")
