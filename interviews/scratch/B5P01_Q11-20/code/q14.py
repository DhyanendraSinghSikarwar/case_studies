import random

def brute(nums, k):
    n = len(nums)
    if n == 0:
        return []
    k %= n
    out = nums[:]
    for _ in range(k):               # rotate one step at a time
        out.insert(0, out.pop())
    return out

def rev(a, i, j):
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1; j -= 1

def optimal(nums, k):                # in place, returns the same list
    n = len(nums)
    if n == 0:
        return nums
    k %= n
    rev(nums, 0, n - 1)
    rev(nums, 0, k - 1)
    rev(nums, k, n - 1)
    return nums

def slice_version(nums, k):          # builds a temp copy: O(n) extra space
    n = len(nums)
    if n:
        k %= n
        nums[:] = nums[-k:] + nums[:-k] if k else nums[:]
    return nums

a = [1, 2, 3, 4, 5, 6, 7]
assert optimal(a, 3) == [5, 6, 7, 1, 2, 3, 4]
assert optimal([1, 2], 5) == [2, 1]          # k > n
assert optimal([1, 2, 3], 3) == [1, 2, 3]    # k == n
assert optimal([1, 2, 3], 0) == [1, 2, 3]
assert optimal([], 4) == []
assert optimal([9], 100) == [9]
assert slice_version([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]
# the classic bug: nums[-k:] when k == 0 returns the WHOLE list
print("nums[-0:] =", [1, 2, 3][-0:], "so the k == 0 guard matters")

rng = random.Random(14)
for _ in range(500):
    arr = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
    k = rng.randint(0, 25)
    assert optimal(arr[:], k) == brute(arr, k) == slice_version(arr[:], k), (arr, k)
print("500 random cases agree")
print(optimal([1, 2, 3, 4, 5, 6, 7], 3))
