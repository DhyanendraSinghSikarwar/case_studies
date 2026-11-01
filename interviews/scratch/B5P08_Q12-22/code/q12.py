import random
import itertools

random.seed(12)

def can_reach_greedy(nums):
    far = 0                                  # farthest index reachable so far
    for i, x in enumerate(nums):
        if i > far:                          # index i is out of reach: stuck
            return False
        far = max(far, i + x)
        if far >= len(nums) - 1:             # early exit, optional
            return True
    return True

def can_reach_dp(nums):                      # forward marking, O(n^2) worst case
    n = len(nums)
    ok = [False] * n
    ok[0] = True
    for i in range(n):
        if ok[i]:
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                ok[j] = True
    return ok[-1]

def can_reach_bfs(nums):                     # explicit queue, also O(n^2) worst case
    from collections import deque
    n = len(nums)
    seen = [False] * n
    seen[0] = True
    q = deque([0])
    while q:
        i = q.popleft()
        if i == n - 1:
            return True
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if not seen[j]:
                seen[j] = True
                q.append(j)
    return False

# --- the four examples in the prompt
for nums, exp in [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False), ([0], True), ([1, 0, 1], False)]:
    assert can_reach_greedy(nums) == can_reach_dp(nums) == can_reach_bfs(nums) == exp
    print(nums, '->', can_reach_greedy(nums))

# --- exhaustive: every list of length 1..6 with values 0..4 (5^1 + ... + 5^6 = 19530 lists)
cnt = 0
for n in range(1, 7):
    for nums in itertools.product(range(5), repeat=n):
        nums = list(nums)
        g = can_reach_greedy(nums)
        assert g == can_reach_dp(nums) == can_reach_bfs(nums), nums
        cnt += 1
print('exhaustive ok:', cnt, 'lists')

# --- seeded random
for _ in range(500):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 30))]
    assert can_reach_greedy(nums) == can_reach_dp(nums)
print('random ok: 500 lists')

# --- worst case for the DP: huge jumps, every index reachable, n inner steps each
n = 2000
big = [n] * n
ops = sum(min(n, i + big[i] + 1) - (i + 1) for i in range(n))
print('DP inner steps on n=2000 all-big jumps:', ops, '(about n^2 / 2); greedy scans', n)
assert ops == n * (n - 1) // 2

# --- edge cases
assert can_reach_greedy([0]) is True
assert can_reach_greedy([0, 1]) is False       # stuck at index 0
assert can_reach_greedy([1, 0]) is True        # a 0 on the last index is fine
assert can_reach_greedy([5, 0, 0, 0, 0, 0]) is True
assert can_reach_greedy([1, 1, 0, 1]) is False
assert can_reach_greedy([0] * 10000) is False
assert can_reach_greedy([1] * 10000) is True
print('edge cases ok')
