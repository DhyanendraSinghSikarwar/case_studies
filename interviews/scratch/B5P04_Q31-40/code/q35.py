import random
from collections import deque


def max_score_fast(nums, k):
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])                      # indices, dp values decreasing front to back
    for i in range(1, n):
        while dq[0] < i - k:             # front index slid out of the window
            dq.popleft()
        dp[i] = nums[i] + dp[dq[0]]
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()                     # dominated: older and not larger
        dq.append(i)
    return dp[-1]


def max_score_brute(nums, k):
    n = len(nums)
    dp = [float("-inf")] * n
    dp[0] = nums[0]
    for i in range(1, n):
        dp[i] = nums[i] + max(dp[max(0, i - k):i])
    return dp[-1]


def max_score_paths(nums, k):
    # independent: enumerate every legal path (tiny inputs only)
    n = len(nums)
    best = float("-inf")
    def go(i, s):
        nonlocal best
        if i == n - 1:
            best = max(best, s)
            return
        for j in range(i + 1, min(n - 1, i + k) + 1):
            go(j, s + nums[j])
    go(0, nums[0])
    return best


tests = [
    ([1, -1, -2, 4, -7, 3], 2, 7),
    ([10, -5, -2, 4, 0, 3], 3, 17),
    ([1, -5, -20, 4, -1, 3, -6, -3], 2, 0),
    ([5], 1, 5),
    ([-3], 4, -3),
    ([-1, -2, -3], 1, -6),
    ([-1, -2, -3], 2, -4),
    ([2, 2, 2, 2], 4, 8),             # positives: visit everything
    ([2, -9, -9, 2], 4, 4),           # jump straight over the holes
]
for nums, k, want in tests:
    assert max_score_fast(nums, k) == max_score_brute(nums, k) == max_score_paths(nums, k) == want, (nums, k)
print([max_score_fast(a, k) for a, k, _ in tests[:3]])

rng = random.Random(35)
for _ in range(1500):
    n = rng.randint(1, 9)
    nums = [rng.randint(-6, 6) for _ in range(n)]
    k = rng.randint(1, 10)
    f = max_score_fast(nums, k)
    assert f == max_score_brute(nums, k) == max_score_paths(nums, k), (nums, k)
print("1500 seeded cases: deque DP == O(nk) DP == path enumeration")

# bigger random check of fast vs O(nk) brute, equal values stress the <= pop rule
for _ in range(300):
    n = rng.randint(1, 60)
    nums = [rng.randint(-3, 3) for _ in range(n)]
    k = rng.randint(1, 12)
    assert max_score_fast(nums, k) == max_score_brute(nums, k)
print("300 larger cases with many ties: ok")
big = [(-1) ** i * (i % 7) - 2 for i in range(3000)]
assert max_score_fast(big, 100) == max_score_brute(big, 100)
print("n=3000, k=100 deque DP == O(nk) DP:", max_score_fast(big, 100))
