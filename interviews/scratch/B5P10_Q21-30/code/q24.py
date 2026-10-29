import random, itertools, sys

random.seed(24)

def dp_reach(nums):
    """O(n^2) DP: reach[j] is True if some reachable i < j has i + nums[i] >= j."""
    n = len(nums); reach = [False] * n; reach[0] = True
    for j in range(1, n):
        reach[j] = any(reach[i] and i + nums[i] >= j for i in range(j))
    return reach

def solve(nums):
    """O(n): furthest reach R. Everything up to R is reachable (prefix), so count = min(R, n-1) + 1."""
    n = len(nums); R = 0; i = 0
    while i <= R and i < n:
        R = max(R, i + nums[i]); i += 1
    return [R >= n - 1, min(R, n - 1) + 1]

def graph_search(nums):
    n = len(nums); seen = {0}; stack = [0]
    while stack:
        i = stack.pop()
        for j in range(i + 1, min(n - 1, i + nums[i]) + 1):
            if j not in seen:
                seen.add(j); stack.append(j)
    return [n - 1 in seen, len(seen)]

def from_dp(nums):
    r = dp_reach(nums); return [r[-1], sum(r)]

for nums, exp in [([2, 3, 1, 1, 4], [True, 5]), ([3, 2, 1, 0, 4], [False, 4]), ([0], [True, 1]), ([1, 0, 5], [False, 2]), ([2, 0, 0], [True, 3])]:
    assert solve(nums) == graph_search(nums) == from_dp(nums) == exp, nums
    print('example', nums, '->', exp)

# walk-through on the first example
nums = [2, 3, 1, 1, 4]
print('DP table reach[j] for', nums, '=', dp_reach(nums))
R = 0
for i, x in enumerate(nums):
    if i > R: break
    R = max(R, i + x); print(f'greedy i={i} nums[i]={x} -> furthest R={R}')
print('answer', solve(nums))
nums = [3, 2, 1, 0, 4]; R = 0
for i, x in enumerate(nums):
    if i > R: print(f'greedy i={i}: i > R={R}, stuck'); break
    R = max(R, i + x); print(f'greedy i={i} nums[i]={x} -> furthest R={R}')

# claim: the reachable set is a prefix of the indices; exhaustive, length <= 6, values 0..3
cnt = 0
for n in range(1, 7):
    for t in itertools.product(range(4), repeat=n):
        l = list(t); r = dp_reach(l)
        k = sum(r)
        assert r == [True] * k + [False] * (n - k), l           # prefix
        assert solve(l) == graph_search(l) == [r[-1], k], l
        cnt += 1
print('exhaustive lists (len <= 6, values 0..3):', cnt, '- reachable set is a prefix on all, greedy = DP = graph search on all')

# seeded random cross-check
for _ in range(600):
    n = random.randint(1, 14); l = [random.choice([0, 0, 1, 1, 2, 3, 5]) for _ in range(n)]
    assert solve(l) == graph_search(l) == from_dp(l), l
print('600 seeded random lists: O(n) == graph search == O(n^2) DP')

# max size (O(n) only)
big = [random.randint(1, 3) for _ in range(10**4)]
print('n = 10^4 result', solve(big))
assert solve([0]) == [True, 1] and solve([1]) == [True, 1] and solve([0, 5]) == [False, 1] and solve([100, 0, 0]) == [True, 3]
print('limit', sys.getrecursionlimit(), '- top-down reach(j) recursion would be up to n = 10^4 deep, so loop')
print('edge asserts passed')
