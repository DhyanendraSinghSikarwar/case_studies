import itertools
import random

random.seed(37)

def best_1d(weights, values, cap):
    """Value only, O(cap) space. Capacity loop goes DOWNWARD so each item is used at most once."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack(weights, values, cap):
    """f[i][c] = best value using items i..n-1 with capacity c. Built from the right so the walk reads left to right."""
    n = len(weights)
    f = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for c in range(cap + 1):
            f[i][c] = f[i + 1][c]                                   # skip item i
            if weights[i] <= c:
                f[i][c] = max(f[i][c], values[i] + f[i + 1][c - weights[i]])   # take item i
    items, c = [], cap
    for i in range(n):
        if f[i][c] == 0:                      # values >= 1: nothing more is worth taking; stop (shorter prefix wins)
            break
        if weights[i] <= c and values[i] + f[i + 1][c - weights[i]] == f[i][c]:
            items.append(i)                   # taking i can still reach the optimum; i is the smallest such index
            c -= weights[i]
    return [f[0][cap], items], f

def brute(weights, values, cap):
    n = len(weights)
    cands = []
    for L in range(n + 1):
        for comb in itertools.combinations(range(n), L):
            if sum(weights[i] for i in comb) <= cap:
                cands.append((sum(values[i] for i in comb), list(comb)))
    mv = max(v for v, _ in cands)
    return [mv, min(c for v, c in cands if v == mv)]       # list comparison: prefix is smaller

def solve(weights, values, cap):
    return knapsack(weights, values, cap)[0]

# ---- examples from the prompt
assert solve([1, 3, 4, 5], [1, 4, 5, 7], 7) == [9, [1, 2]]
assert solve([5], [10], 4) == [0, []]
assert solve([2, 2, 3], [3, 3, 5], 4) == [6, [0, 1]]
assert solve([1, 1, 1], [4, 4, 4], 2) == [8, [0, 1]]
print('examples ok')

# ---- the table of the first example (rows i = items i..n-1 allowed, columns = capacity 0..7)
res, f = knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
print('cap       ', list(range(8)))
for i in range(5):
    print(f'from item {i}', f[i])
print('result', res)

# ---- seeded cross-check against the subset enumeration with the same tie rule
cases = 0
for _ in range(600):
    n = random.randint(1, 10)
    ws = [random.randint(1, 6) for _ in range(n)]
    vs = [random.randint(1, 9) for _ in range(n)]
    cap = random.randint(0, 20)
    got = solve(ws, vs, cap)
    assert got == brute(ws, vs, cap), (ws, vs, cap, got)
    assert best_1d(ws, vs, cap) == got[0]
    assert sum(ws[i] for i in got[1]) <= cap and sum(vs[i] for i in got[1]) == got[0]
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- why the 1D table cannot rebuild the items: dp[c] forgets which items made it
dp = [0] * 8
for w, v in zip([1, 3, 4, 5], [1, 4, 5, 7]):
    for c in range(7, w - 1, -1):
        dp[c] = max(dp[c], dp[c - w] + v)
print('1D table after all items:', dp, '-> value', dp[7], 'but nothing says WHICH items')

# ---- edge cases and full size
assert solve([3], [5], 3) == [5, [0]]
assert solve([1, 1], [1, 1], 0) == [0, []]
assert solve([2, 2], [3, 3], 2) == [3, [0]]                  # tie: smallest index list
W = [random.randint(1, 100) for _ in range(100)]
V = [random.randint(1, 1000) for _ in range(100)]
r = solve(W, V, 1000)
assert r[0] == best_1d(W, V, 1000) and sum(W[i] for i in r[1]) <= 1000
print('n = 100, cap = 1000 ok: value', r[0], 'with', len(r[1]), 'items')
