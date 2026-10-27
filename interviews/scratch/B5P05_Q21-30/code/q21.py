import random
from itertools import accumulate


def allocate_brute(pages, m):
    # DP: dp[j][i] = best max-load splitting the first i books into j blocks. O(m * n^2).
    n = len(pages)
    if m > n:
        return -1
    pre = [0] + list(accumulate(pages))
    INF = float("inf")
    dp = [[INF] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    for j in range(1, m + 1):
        for i in range(j, n + 1):
            for p in range(j - 1, i):
                dp[j][i] = min(dp[j][i], max(dp[j - 1][p], pre[i] - pre[p]))
    return dp[m][n]


def students_needed(pages, cap):
    # greedy: fill the current student until the next book would overflow
    used, load = 1, 0
    for p in pages:
        if load + p > cap:
            used += 1
            load = 0
        load += p
    return used


def allocate_books(pages, m):
    if m > len(pages):                      # not enough books for one each: infeasible
        return -1
    lo, hi = max(pages), sum(pages)         # answer is in [max, sum]; hi is feasible (1 student)
    while lo < hi:                          # first True of: students_needed(cap) <= m
        mid = (lo + hi) // 2
        if students_needed(pages, mid) <= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


examples = [([12, 34, 67, 90], 2, 113), ([25, 46, 28, 49, 24], 4, 71),
            ([10, 20], 3, -1), ([10, 20], 2, 20), ([5, 5, 5, 5], 1, 20)]
for pages, m, want in examples:
    assert allocate_books(pages, m) == allocate_brute(pages, m) == want, (pages, m)
    print(pages, "m =", m, "->", allocate_books(pages, m))

# the answer is always the sum of some contiguous block (checked on every random case below)
rng = random.Random(21)
cnt = 0
for _ in range(1500):
    n = rng.randint(1, 9)
    pages = [rng.randint(1, 12) for _ in range(n)]
    m = rng.randint(1, n + 2)               # includes the infeasible m > n
    got, want = allocate_books(pages, m), allocate_brute(pages, m)
    assert got == want, (pages, m, got, want)
    if got != -1:
        sums = {sum(pages[i:j]) for i in range(n) for j in range(i + 1, n + 1)}
        assert got in sums, (pages, m, got)
        cnt += 1
print("random check passed: 1500 cases, feasible ones:", cnt, "(answer was a block sum every time)")

# edge cases
assert allocate_books([7], 1) == 7
assert allocate_books([7], 2) == -1
assert allocate_books([3, 3, 3], 3) == 3            # m == n: answer is max(pages)
assert allocate_books([1, 1, 1, 100], 2) == 100     # one huge book sets the floor
assert allocate_books([10 ** 4] * 10 ** 5, 10 ** 5) == 10 ** 4
assert allocate_books([10 ** 4] * 10 ** 5, 1) == 10 ** 9
print("edge asserts passed")
