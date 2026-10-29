import random, sys
from collections import Counter
from functools import cache

random.seed(27)

def delete_and_earn(nums):
    """Reduce to house robber over values: tot[v] = v * count(v); picking v forbids v-1 and v+1."""
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    take, skip = 0, 0                    # take = best with the previous value taken, skip = best with it not taken
    for v in range(len(tot)):
        take, skip = skip + tot[v], max(take, skip)
    return max(take, skip)

def rob(a):
    """House robber, rolling: prev2, prev1."""
    p2 = p1 = 0
    for v in a: p2, p1 = p1, max(p1, p2 + v)
    return p1

def via_robber(nums):
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    return rob(tot)

def memo(nums):
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    @cache
    def f(i):
        if i < 0: return 0
        return max(f(i - 1), f(i - 2) + tot[i])
    return f(len(tot) - 1)

def brute(nums):
    """All sets of distinct values with no two consecutive integers."""
    c = Counter(nums); vals = sorted(c); best = 0
    for m in range(1 << len(vals)):
        ch = [vals[i] for i in range(len(vals)) if m >> i & 1]
        if all(ch[i + 1] - ch[i] > 1 for i in range(len(ch) - 1)):
            best = max(best, sum(v * c[v] for v in ch))
    return best

def simulate(nums):
    """Direct simulation of the game on small lists (picks one value at a time), to justify the reduction."""
    @cache
    def g(state):
        best = 0
        for v in set(state):
            rest = tuple(sorted(y for y in state if y != v and y != v - 1 and y != v + 1))
            best = max(best, v * state.count(v) + g(rest))
        return best
    return g(tuple(sorted(nums)))

for nums, exp in [([3, 4, 2], 6), ([2, 2, 3, 3, 3, 4], 9), ([], 0), ([1, 1, 1, 2, 4, 5, 5, 5, 6], 18)]:
    assert delete_and_earn(nums) == brute(nums) == via_robber(nums) == memo(nums) == simulate(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [2, 2, 3, 3, 3, 4]
tot = [0] * (max(nums) + 1)
for x in nums: tot[x] += x
print('tot by value 0..4 =', tot)
take, skip = 0, 0
for v in range(len(tot)):
    take, skip = skip + tot[v], max(take, skip)
    print(f'value {v}: tot={tot[v]:2d}  best if value {v} taken={take:2d}  best if not taken={skip:2d}')
print('answer', max(take, skip))

for _ in range(800):
    n = random.randint(0, 9); l = [random.randint(1, 8) for _ in range(n)]
    want = brute(l)
    assert delete_and_earn(l) == want == via_robber(l) == memo(l), l
    assert simulate(l) == want, l
print('800 seeded random lists: DP == subset enumeration == game simulation == memo')

big = [random.randint(1, 10**4) for _ in range(2 * 10**4)]
print('n = 2*10^4, values <= 10^4 answer', delete_and_earn(big))
print('limit =', sys.getrecursionlimit())
try:
    memo([10**4]); print('memo ok')
except RecursionError:
    print('memo over a value table of 10^4 slots: RecursionError')
assert delete_and_earn([1]) == 1 and delete_and_earn([5, 5, 5]) == 15 and delete_and_earn([1, 2]) == 2
print('edge asserts passed')
