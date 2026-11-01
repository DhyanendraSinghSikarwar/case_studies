import random


def kth_two(a, b, k):
    m, n = len(a), len(b)
    lo, hi = max(0, k - n), min(k, m)      # i = how many of the k smallest come from a
    while lo < hi:
        i = (lo + hi) // 2
        j = k - i
        # i < hi <= m so a[i] exists; i < hi <= k so j >= 1; j <= k - lo <= n so b[j-1] exists
        if a[i] < b[j - 1]:
            lo = i + 1                      # a[i] must be among the k smallest: take more from a
        else:
            hi = i
    i, j = lo, k - lo
    left = []
    if i > 0:
        left.append(a[i - 1])
    if j > 0:
        left.append(b[j - 1])
    return max(left)


def kth_merge(a, b, k):
    # O(k) merge walk (Part 2 Q40 style)
    i = j = 0
    for _ in range(k):
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            v = a[i]; i += 1
        else:
            v = b[j]; j += 1
    return v


def kth_sorted(a, b, k):
    return sorted(a + b)[k - 1]


for a, b, k, want in [([1, 3, 8], [2, 4, 6, 9], 4, 4), ([1, 2], [1, 2], 3, 2), ([], [3, 5], 2, 5),
                      ([7], [1, 2, 3], 1, 1), ([7], [1, 2, 3], 4, 7)]:
    got = (kth_two(a, b, k), kth_merge(a, b, k), kth_sorted(a, b, k))
    print(a, b, "k =", k, "->", got)
    assert got == (want,) * 3

rng = random.Random(35)
cases = 0
for _ in range(4000):
    a = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 7)))
    b = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 7)))
    if not a and not b:
        continue
    for k in range(1, len(a) + len(b) + 1):
        assert kth_two(a, b, k) == kth_sorted(a, b, k), (a, b, k)
        cases += 1
print("random (a, b, k) cases checked:", cases)

# median from k-th (ties with duplicates included)
a, b = [1, 3], [2]
tot = len(a) + len(b)
assert kth_two(a, b, (tot + 1) // 2) == 2
# edges: one side empty, all equal, k = total, disjoint ranges
assert kth_two([], [5], 1) == 5 and kth_two([5], [], 1) == 5
assert kth_two([4, 4, 4], [4, 4], 5) == 4
assert kth_two([1, 2], [10, 11], 4) == 11 and kth_two([10, 11], [1, 2], 1) == 1
# big input: the search takes about 20 steps, not 10**6
big_a = list(range(0, 2 * 10**6, 2))
big_b = list(range(1, 2 * 10**6, 2))
assert kth_two(big_a, big_b, 10**6) == 10**6 - 1
print("all checks passed")
