import random
from functools import lru_cache

random.seed(20)

def unbounded_knapsack(weights, values, cap):
    """Optimal: dp[c] = best value with total weight <= c, items reusable. O(n * cap) time, O(cap) space."""
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        for w, v in zip(weights, values):
            if w <= c and dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[cap]

def unbounded_item_outer(weights, values, cap):
    """Same answer, items outer and capacity UPWARD: the 0/1 code with one loop direction flipped."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack01(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def unbounded_memo(weights, values, cap):
    """Top-down over the remaining capacity. Depth can reach cap (weight-1 items), so it breaks past ~1000."""
    @lru_cache(maxsize=None)
    def f(c):
        return max([0] + [f(c - w) + v for w, v in zip(weights, values) if w <= c])
    return f(cap)

def brute(weights, values, cap):
    """Oracle: plain recursion over the remaining capacity, no cache."""
    def f(c):
        return max([0] + [f(c - w) + v for w, v in zip(weights, values) if w <= c])
    return f(cap)

for (w, v, c), want in [(([2, 3, 4], [3, 5, 7], 8), 14), (([5], [10], 4), 0), (([1, 5], [1, 8], 11), 17), (([3], [7], 9), 21)]:
    assert unbounded_knapsack(w, v, c) == unbounded_item_outer(w, v, c) == brute(w, v, c) == unbounded_memo(tuple(w), tuple(v), c) == want
print('4 prompt examples ok')

# walk-through on weights=[2,3,4], values=[3,5,7], cap=8
w, v, cap = [2, 3, 4], [3, 5, 7], 8
dp = [0] * (cap + 1)
print('c   dp[c]  candidates dp[c-w]+v for each item that fits')
print('0   0      base: nothing fits in capacity 0')
for c in range(1, cap + 1):
    cands = ['w=%d:dp[%d]+%d=%d' % (wi, c - wi, vi, dp[c - wi] + vi) for wi, vi in zip(w, v) if wi <= c]
    dp[c] = max([0] + [dp[c - wi] + vi for wi, vi in zip(w, v) if wi <= c])
    print('%-3d %-6d %s' % (c, dp[c], ', '.join(cands) if cands else 'nothing fits'))
print('dp[8] =', dp[8], '= 7 + 7 (two weight-4 items)')

# 0/1 versus unbounded: one loop direction
print('weights=[3], values=[7], cap=9 -> 0/1', knapsack01([3], [7], 9), ' unbounded', unbounded_knapsack([3], [7], 9))

# seeded cross-check against the plain recursion (cap <= 10)
for _ in range(500):
    n = random.randint(1, 4)
    w = [random.randint(1, 7) for _ in range(n)]
    v = [random.randint(1, 20) for _ in range(n)]
    cap = random.randint(0, 10)
    b = brute(w, v, cap)
    assert unbounded_knapsack(w, v, cap) == unbounded_item_outer(w, v, cap) == unbounded_memo(tuple(w), tuple(v), cap) == b, (w, v, cap)
print('500 random cases agree (capacity-outer = item-outer = memo = plain recursion)')

# recursion limit
try:
    unbounded_memo((1,), (1,), 10**4)
    print('memo at cap=10^4 with a weight-1 item: no error (unexpected)')
except RecursionError:
    print('memo at cap=10^4 with a weight-1 item: RecursionError under the default limit')
print('bottom-up cap=10^4, weights=[1] ->', unbounded_knapsack([1], [1], 10**4))

# edge cases and max size
assert unbounded_knapsack([5], [10], 0) == 0 and unbounded_knapsack([100], [1000], 99) == 0
big_w = [random.randint(1, 100) for _ in range(50)]
big_v = [random.randint(1, 1000) for _ in range(50)]
assert unbounded_knapsack(big_w, big_v, 10**4) == unbounded_item_outer(big_w, big_v, 10**4)
print('edge cases ok; max-size random input ->', unbounded_knapsack(big_w, big_v, 10**4))
