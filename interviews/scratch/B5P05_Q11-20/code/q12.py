import random

INF = float("inf")


def median_merge(a, b):
    """Reference: O(m+n) merge (two pointers) then pick the middle."""
    merged, i, j = [], 0, 0
    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            merged.append(a[i]); i += 1
        else:
            merged.append(b[j]); j += 1
    n = len(merged)
    if n % 2:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2


def median_bs(a, b):
    if len(a) > len(b):
        a, b = b, a                     # binary search the shorter list
    m, n = len(a), len(b)
    half = (m + n + 1) // 2             # size of the combined left side
    lo, hi = 0, m                       # i = how many of a go left
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i                    # how many of b go left (0 <= j <= n since m <= n)
        a_left = a[i - 1] if i > 0 else -INF
        a_right = a[i] if i < m else INF
        b_left = b[j - 1] if j > 0 else -INF
        b_right = b[j] if j < n else INF
        if a_left <= b_right and b_left <= a_right:
            left = max(a_left, b_left)
            if (m + n) % 2:
                return float(left)
            return (left + min(a_right, b_right)) / 2
        if a_left > b_right:
            hi = i - 1                  # took too many from a
        else:
            lo = i + 1                  # took too few from a
    raise ValueError("inputs not sorted or both empty")


examples = [([1, 3], [2], 2.0), ([1, 2], [3, 4], 2.5), ([], [5], 5.0),
            ([0, 0], [0, 0], 0.0), ([1, 2, 3], [], 2.0)]
for a, b, exp in examples:
    got = median_bs(a, b)
    assert got == median_merge(a, b) == exp, (a, b, got, exp)
    print(a, b, "->", got)

random.seed(12)
cases = 0
for _ in range(2000):
    a = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 7)))
    b = sorted(random.randint(-6, 6) for _ in range(random.randint(0, 7)))
    if not a and not b:
        continue
    assert median_bs(a, b) == median_merge(a, b) == (lambda s: float(s[len(s)//2]) if len(s) % 2 else (s[len(s)//2-1] + s[len(s)//2]) / 2)(sorted(a + b)), (a, b)
    cases += 1
print("cross-check: %d seeded cases agree (merge, binary search, sorted()-based)" % cases)

# edge cases: argument order, one empty, disjoint ranges, big values, huge one-sided
assert median_bs([5], []) == 5.0
assert median_bs([1, 2, 3], [10, 11, 12]) == 6.5
assert median_bs([10, 11, 12], [1, 2, 3]) == 6.5
assert median_bs([-10**9], [10**9]) == 0.0
assert median_bs([7], [1, 2, 3, 4, 5, 6, 8, 9]) == 5.0
big_a = list(range(0, 2000, 2))
big_b = list(range(1, 2000, 2))
assert median_bs(big_a, big_b) == median_merge(big_a, big_b) == 999.5
print("edge asserts passed")
