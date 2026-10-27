import random


def bouquets_at(bloom, k, day):
    cnt = run = 0
    for b in bloom:
        if b <= day:
            run += 1
            if run == k:
                cnt += 1
                run = 0              # flowers are used once: start a fresh run
        else:
            run = 0                  # an unbloomed flower breaks adjacency
    return cnt


def min_days_bs(bloom, m, k):
    if len(bloom) < m * k:
        return -1
    lo, hi = min(bloom), max(bloom)      # at hi every flower is open, so hi is feasible
    while lo < hi:
        mid = (lo + hi) // 2
        if bouquets_at(bloom, k, mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


def min_days_brute(bloom, m, k):
    if len(bloom) < m * k:
        return -1
    for day in sorted(set(bloom)):       # try each candidate day ascending
        if bouquets_at(bloom, k, day) >= m:
            return day


def min_days_independent(bloom, m, k):
    """Different brute force: choose bouquets from windows by recursion (no greedy)."""
    n = len(bloom)
    best = [None]

    def go(i, made, cur_max):
        if made == m:
            best[0] = cur_max if best[0] is None else min(best[0], cur_max)
            return
        if i + k > n:
            return
        go(i + 1, made, cur_max)                                     # skip flower i
        go(i + k, made + 1, max(cur_max, max(bloom[i:i + k])))       # take window i..i+k-1
    go(0, 0, 0)
    return -1 if best[0] is None else best[0]


examples = [([1, 10, 3, 10, 2], 3, 1, 3), ([1, 10, 3, 10, 2], 3, 2, -1),
            ([7, 7, 7, 7, 12, 7, 7], 2, 3, 12), ([1, 10, 2, 9, 3, 8, 4, 7, 5, 6], 4, 2, 9)]
for bloom, m, k, exp in examples:
    got = min_days_bs(bloom, m, k)
    assert got == min_days_brute(bloom, m, k) == min_days_independent(bloom, m, k) == exp
    print(bloom, "m =", m, "k =", k, "->", got)

random.seed(19)
for _ in range(1500):
    n = random.randint(1, 9)
    bloom = [random.randint(1, 8) for _ in range(n)]
    m, k = random.randint(1, 4), random.randint(1, 4)
    a, b, c = min_days_bs(bloom, m, k), min_days_brute(bloom, m, k), min_days_independent(bloom, m, k)
    assert a == b == c, (bloom, m, k, a, b, c)
print("cross-check: 1500 seeded cases agree (binary search, scan of days, recursive window brute force)")

# monotonic in the day: more days never makes fewer bouquets
for _ in range(200):
    bloom = [random.randint(1, 20) for _ in range(random.randint(1, 15))]
    k = random.randint(1, 3)
    counts = [bouquets_at(bloom, k, d) for d in range(0, 22)]
    assert counts == sorted(counts)
print("monotone check: bouquet count never drops as the day grows (200 seeded lists)")

# edge cases
assert min_days_bs([5], 1, 1) == 5
assert min_days_bs([5], 2, 1) == -1
assert min_days_bs([3, 3, 3], 1, 3) == 3
assert min_days_bs([1, 2, 3], 1, 4) == -1
assert min_days_bs([10**9] * 6, 3, 2) == 10**9
big = [random.randint(1, 10**9) for _ in range(10**5)]
assert min_days_bs(big, 10**5, 1) == max(big)        # every flower needed
assert len(big) < 10**4 * 11 and min_days_bs(big, 10**4 + 1, 10) == -1
print("edge asserts passed")
