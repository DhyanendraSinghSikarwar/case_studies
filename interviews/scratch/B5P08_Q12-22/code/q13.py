import random
import itertools
from collections import deque

random.seed(13)

def min_jumps_greedy(nums):
    jumps = 0
    level_end = 0                            # last index of the current BFS level
    far = 0                                  # farthest index reachable from the current level
    for i in range(len(nums) - 1):           # stop BEFORE the last index
        far = max(far, i + nums[i])
        if i == level_end:                   # finished scanning this level: one more jump
            jumps += 1
            level_end = far
    return jumps

def min_jumps_bfs(nums):                     # real BFS, O(n^2) worst case
    n = len(nums)
    dist = [-1] * n
    dist[0] = 0
    q = deque([0])
    while q:
        i = q.popleft()
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if dist[j] < 0:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist[-1]

def min_jumps_dp(nums):                      # forward relaxation, O(n^2)
    n = len(nums)
    INF = 10 ** 9
    d = [INF] * n
    d[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            d[j] = min(d[j], d[i] + 1)
    return d[-1]

def reachable(nums):
    far = 0
    for i, x in enumerate(nums):
        if i > far:
            return False
        far = max(far, i + x)
    return True

for nums, exp in [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2), ([0], 0), ([1, 1, 1, 1], 3)]:
    assert min_jumps_greedy(nums) == min_jumps_bfs(nums) == min_jumps_dp(nums) == exp
    print(nums, '->', min_jumps_greedy(nums))

# exhaustive: every list of length 1..6 over 0..4 whose last index is reachable
cnt = 0
for n in range(1, 7):
    for t in itertools.product(range(5), repeat=n):
        nums = list(t)
        if not reachable(nums):
            continue
        assert min_jumps_greedy(nums) == min_jumps_bfs(nums) == min_jumps_dp(nums), nums
        cnt += 1
print('exhaustive ok:', cnt, 'reachable lists')

# seeded random, longer lists (force reachability by lifting zeros to 1)
for _ in range(500):
    nums = [random.randint(1, 6) if random.random() < 0.7 else 1 for _ in range(random.randint(1, 40))]
    assert min_jumps_greedy(nums) == min_jumps_bfs(nums)
print('random ok: 500 lists')

# why the scan stops before the last index: with range(len(nums)) a final level end would add a phantom jump
def min_jumps_no_stop(nums):                 # WRONG on purpose
    jumps = end = far = 0
    for i in range(len(nums)):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps
print('no-stop variant on [2, 3, 1, 1, 4]:', min_jumps_no_stop([2, 3, 1, 1, 4]), '(wrong, answer is 2)')
print('no-stop variant on [0]:', min_jumps_no_stop([0]), '(wrong, answer is 0)')
assert min_jumps_no_stop([0]) == 1 and min_jumps_greedy([0]) == 0
assert min_jumps_no_stop([2, 3, 1, 1, 4]) == 3

# edge cases and a big input (iterative, no recursion)
assert min_jumps_greedy([7]) == 0
assert min_jumps_greedy([1] * 10000) == 9999
assert min_jumps_greedy([10000] + [1] * 9999) == 1
assert min_jumps_greedy([5, 4, 3, 2, 1, 1, 1]) == 2
print('edge cases ok')
