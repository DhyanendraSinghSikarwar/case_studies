import random

random.seed(39)

def days_greedy(weights, cap):
    if max(weights) > cap:
        return -1
    days, load = 1, 0
    for w in weights:
        if load + w > cap:       # next package would overflow today: close the day, start a new one
            days += 1
            load = 0
        load += w
    return days

def days_dp(weights, cap):
    """Exhaustive: d[i] = fewest days for the first i packages over ALL contiguous splits."""
    if max(weights) > cap:
        return -1
    n, INF = len(weights), float('inf')
    d = [0] + [INF] * n
    for i in range(1, n + 1):
        for j in range(i):
            if sum(weights[j:i]) <= cap:
                d[i] = min(d[i], d[j] + 1)
    return d[n]

def min_cap(weights, limit_days):
    """The outer binary search (Part 5 Q8 style) that uses days_greedy as its predicate."""
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_greedy(weights, mid) <= limit_days:
            hi = mid
        else:
            lo = mid + 1
    return lo

# ---- examples
for w, cap, want in [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 15, 5), ([3, 2, 2, 4, 1, 4], 6, 3), ([5, 5], 4, -1), ([7], 7, 1)]:
    assert days_greedy(w, cap) == days_dp(w, cap) == want, (w, cap)
    print(w, 'cap', cap, '->', days_greedy(w, cap))

# ---- greedy vs exhaustive DP, then monotonic in capacity, on seeded small inputs
for _ in range(1500):
    w = [random.randint(1, 6) for _ in range(random.randint(1, 8))]
    cap = random.randint(1, 14)
    assert days_greedy(w, cap) == days_dp(w, cap), (w, cap)
print('1500 random (weights, cap) agree with the exhaustive DP')

mono = 0
for _ in range(500):
    w = [random.randint(1, 9) for _ in range(random.randint(1, 9))]
    ds = [days_greedy(w, c) for c in range(max(w), sum(w) + 3)]       # all capacities that are feasible
    assert all(ds[i] >= ds[i + 1] for i in range(len(ds) - 1)), (w, ds)
    assert ds[0] >= 1 and ds[-1] == 1
    mono += 1
print('days(cap) is non-increasing on', mono, 'weight lists (so "days <= D" is a monotone predicate for binary search)')

# ---- the check inside the binary search: smallest cap for D days, against brute force over every cap
for _ in range(500):
    w = [random.randint(1, 8) for _ in range(random.randint(1, 8))]
    D = random.randint(1, len(w))
    brute = next(c for c in range(max(w), sum(w) + 1) if days_dp(w, c) <= D)
    assert min_cap(w, D) == brute, (w, D)
print('binary search over cap with the greedy check matches exhaustive search on 500 cases;',
      'sample: weights 1..10, 5 days ->', min_cap(list(range(1, 11)), 5))

# ---- edge asserts and maximum size
assert days_greedy([1], 1) == 1
assert days_greedy([5, 5], 5) == 2 and days_greedy([5, 5], 10) == 1 and days_greedy([5, 5], 9) == 2
assert days_greedy([500] * 3, 499) == -1
big = [random.randint(1, 500) for _ in range(5 * 10 ** 4)]
assert days_greedy(big, 500) >= 1 and days_greedy(big, sum(big)) == 1
print('size 5*10^4 ok; days at cap 500 =', days_greedy(big, 500), ', at sum(big) =', days_greedy(big, sum(big)))
