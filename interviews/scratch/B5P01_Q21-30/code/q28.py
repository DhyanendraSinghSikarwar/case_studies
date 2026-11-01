import random


def find_set(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)


def find_sort(nums):
    s = sorted(nums)                     # copy: the input stays untouched
    for a, b in zip(s, s[1:]):
        if a == b:
            return a


def find_binary(nums):
    """Binary search on the VALUE range 1..n using the pigeonhole count."""
    lo, hi = 1, len(nums) - 1            # values are in 1..n, len = n+1
    while lo < hi:
        mid = (lo + hi) // 2
        cnt = sum(1 for x in nums if x <= mid)
        if cnt > mid:                    # too many values <= mid: dup is in [lo, mid]
            hi = mid
        else:
            lo = mid + 1
    return lo


def find_floyd(nums):
    """Index i points to nums[i]. The repeated value is the cycle entrance."""
    slow = fast = 0                      # node 0 is the head: no value equals 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0                             # phase 2: restart one pointer at the head
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


for arr, want in [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3)]:
    r = (find_set(arr), find_sort(arr), find_binary(arr), find_floyd(arr))
    print(arr, "->", r)
    assert r == (want,) * 4

# --- edge cases
assert find_floyd([1, 1]) == 1 and find_binary([1, 1]) == 1
assert find_floyd([2, 2, 2, 2, 2]) == 2           # many copies
assert find_binary([2, 2, 2, 2, 2]) == 2
assert find_floyd([1, 1, 2]) == 1 and find_binary([1, 1, 2]) == 1
assert find_floyd([2, 1, 2]) == 2
big = list(range(1, 100001)) + [77777]
assert find_floyd(big) == find_binary(big) == find_set(big) == 77777
keep = [3, 1, 3, 4, 2]
find_floyd(keep); find_binary(keep); find_sort(keep)
assert keep == [3, 1, 3, 4, 2]                    # not modified
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(28)
for _ in range(2000):
    n = rng.randint(1, 12)
    c = rng.randint(2, n + 1)                      # copies of the repeated value
    d = rng.randint(1, n)
    others = rng.sample([v for v in range(1, n + 1) if v != d], n + 1 - c)
    nums = [d] * c + others
    rng.shuffle(nums)
    assert len(nums) == n + 1
    want = find_set(nums)
    assert want == d
    assert find_sort(nums) == find_binary(nums) == find_floyd(nums) == d, nums
print("2000 random cases OK")
