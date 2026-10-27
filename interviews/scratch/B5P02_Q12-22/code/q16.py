import random
from collections import deque

def brute(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]

def optimal(nums, k):
    dq = deque()          # indices; values nums[dq[0]] >= nums[dq[1]] >= ... (decreasing)
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:    # smaller-or-equal elements can never be a max again
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                 # front slid out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out

assert optimal([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert optimal([1], 1) == [1]
assert optimal([4, 2, 12, 3], 1) == [4, 2, 12, 3]
assert optimal([4, 2, 12, 3], 4) == [12]
assert optimal([5, 5, 5, 5], 2) == [5, 5, 5]
assert optimal([-3, -2, -1], 2) == [-2, -1]
assert optimal([9, 8, 7, 6], 2) == [9, 8, 7]        # decreasing: deque keeps everything
assert optimal([1, 2, 3, 4], 2) == [2, 3, 4]        # increasing: deque has one element

rng = random.Random(16)
for _ in range(1000):
    n = rng.randint(1, 12)
    a = [rng.randint(-5, 5) for _ in range(n)]
    k = rng.randint(1, n)
    assert optimal(a, k) == brute(a, k), (a, k)
print("1000 random cases agree with brute force")
print(optimal([1, 3, -1, -3, 5, 3, 6, 7], 3), optimal([1], 1))
big = [(i * 31337) % 10007 for i in range(100000)]
assert optimal(big[:3000], 500) == brute(big[:3000], 500)
print("n = 100000, k = 500 windows:", len(optimal(big, 500)))
