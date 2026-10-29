import random
from functools import lru_cache

random.seed(17)

def knapsack_2d(weights, values, cap):
    """2D table: dp[i][c] = best value using the first i items with capacity c. O(n * cap) time and space."""
    n = len(weights)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]          # row 0: no items, value 0 for every capacity
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(cap + 1):
            dp[i][c] = dp[i - 1][c]                        # skip item i
            if c >= w:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)   # take item i once
    return dp

def knapsack_1d(weights, values, cap):
    """Optimal: one row, capacity looped DOWNWARD. O(n * cap) time, O(cap) space."""
    dp = [0] * (cap + 1)                                   # dp[c] = best value with weight <= c
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack_upward(weights, values, cap):
    """The classic bug: capacity looped UPWARD. dp[c - w] may already include this item, so it can be taken again."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def unbounded(weights, values, cap):
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        for w, v in zip(weights, values):
            if w <= c:
                dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack_memo(weights, values, cap):
    """Top-down: state (i, remaining capacity); depth is len(weights) <= 100, safe under the default limit."""
    @lru_cache(maxsize=None)
    def go(i, rem):
        if i == len(weights):
            return 0
        best = go(i + 1, rem)
        if weights[i] <= rem:
            best = max(best, go(i + 1, rem - weights[i]) + values[i])
        return best
    return go(0, cap)

def brute(weights, values, cap):
    """Oracle: every subset."""
    n, best = len(weights), 0
    for m in range(1 << n):
        if sum(weights[i] for i in range(n) if m >> i & 1) <= cap:
            best = max(best, sum(values[i] for i in range(n) if m >> i & 1))
    return best

for (w, v, c), want in [(([1, 3, 4, 5], [1, 4, 5, 7], 7), 9), (([5], [10], 4), 0), (([2, 2, 3], [3, 3, 5], 4), 6), (([3, 4], [5, 6], 0), 0)]:
    assert knapsack_2d(w, v, c)[-1][c] == knapsack_1d(w, v, c) == knapsack_memo(w, v, c) == brute(w, v, c) == want
print('4 prompt examples ok')

# walk-through on weights=[1,3,4,5], values=[1,4,5,7], cap=7
w, v, cap = [1, 3, 4, 5], [1, 4, 5, 7], 7
print('2D table, columns c = 0..7')
print('no items ', knapsack_2d([], [], cap)[0])
dp2 = knapsack_2d(w, v, cap)
for i in range(1, 5):
    print('item %d (w=%d,v=%d)' % (i, w[i - 1], v[i - 1]), dp2[i])
print('1D table, same final row; each line is the single row after one item (downward loop)')
dp = [0] * (cap + 1)
for wi, vi in zip(w, v):
    for c in range(cap, wi - 1, -1):
        dp[c] = max(dp[c], dp[c - wi] + vi)
    print('after w=%d' % wi, dp)
assert dp == dp2[-1]
print('answer', dp[cap], '= items weight 3 + 4 (values 4 + 5)')

# what the upward loop computes: a different problem
print('upward loop on the same input:', knapsack_upward(w, v, cap), '; unbounded answer:', unbounded(w, v, cap), '; true 0/1 answer:', knapsack_1d(w, v, cap))
print('example where it breaks: one item weight 2, value 5, cap 6 -> 0/1', knapsack_1d([2], [5], 6), 'upward', knapsack_upward([2], [5], 6))

# seeded cross-check against subset enumeration (len <= 12)
diff = 0
for _ in range(500):
    n = random.randint(1, 12)
    w = [random.randint(1, 9) for _ in range(n)]
    v = [random.randint(1, 30) for _ in range(n)]
    cap = random.randint(0, 40)
    b = brute(w, v, cap)
    assert knapsack_1d(w, v, cap) == knapsack_2d(w, v, cap)[-1][cap] == knapsack_memo(w, v, cap) == b, (w, v, cap)
    assert knapsack_upward(w, v, cap) == unbounded(w, v, cap)
    diff += knapsack_upward(w, v, cap) != b
print('500 random cases agree (1D = 2D = memo = enumeration); upward loop equals the unbounded answer every time and differs from 0/1 in', diff)

# edge cases and max size
assert knapsack_1d([100], [1000], 99) == 0 and knapsack_1d([100], [1000], 100) == 1000
big_w = [random.randint(1, 100) for _ in range(100)]
big_v = [random.randint(1, 1000) for _ in range(100)]
assert knapsack_1d(big_w, big_v, 1000) == knapsack_memo(big_w, big_v, 1000) == knapsack_2d(big_w, big_v, 1000)[-1][1000]
print('edge cases ok; max-size random input ->', knapsack_1d(big_w, big_v, 1000))
