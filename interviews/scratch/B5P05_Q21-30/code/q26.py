import random


def kth_brute(mat, k):
    return sorted(v for row in mat for v in row)[k - 1]


def count_le(mat, v):
    # staircase from the bottom-left: number of entries <= v in O(n)
    n = len(mat)
    r, c, total = n - 1, 0, 0
    while r >= 0 and c < n:
        if mat[r][c] <= v:
            total += r + 1                  # the whole column segment above (and including) row r is <= v
            c += 1
        else:
            r -= 1
    return total


def kth_smallest(mat, k):
    lo, hi = mat[0][0], mat[-1][-1]         # smallest and largest entries
    while lo < hi:                          # smallest v with count_le(v) >= k
        mid = (lo + hi) // 2
        if count_le(mat, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


for mat, k, want in [([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8, 13), ([[-5]], 1, -5),
                     ([[1, 2], [1, 3]], 2, 1), ([[1, 2], [1, 3]], 3, 2)]:
    assert kth_smallest(mat, k) == kth_brute(mat, k) == want, (mat, k)
    print(mat, "k =", k, "->", kth_smallest(mat, k))


def random_matrix(rng, n, lo=-15, hi=30):
    mat = [sorted(rng.randint(lo, hi) for _ in range(n)) for _ in range(n)]     # rows sorted
    cols = [sorted(mat[r][c] for r in range(n)) for c in range(n)]               # then sort each column
    mat = [[cols[c][r] for c in range(n)] for r in range(n)]
    assert all(mat[r][c] <= mat[r][c + 1] for r in range(n) for c in range(n - 1))
    assert all(mat[r][c] <= mat[r + 1][c] for r in range(n - 1) for c in range(n))
    return mat


rng = random.Random(26)
hit_entry = 0
for _ in range(600):
    n = rng.randint(1, 6)
    mat = random_matrix(rng, n)
    entries = {v for row in mat for v in row}
    for k in range(1, n * n + 1):
        got = kth_smallest(mat, k)
        assert got == kth_brute(mat, k), (mat, k)
        assert got in entries                # the guarantee asked about: the answer is an entry
        hit_entry += 1
print("random check passed:", hit_entry, "(matrix, k) pairs; answer was always an entry")

# the argument in numbers: count_le changes only at entry values (integers), so the smallest v with count >= k is an entry
mat = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
print("count_le for v = 9..13:", [(v, count_le(mat, v)) for v in range(9, 14)])
assert count_le(mat, 12) == count_le(mat, 11) + 1 and count_le(mat, 13) == 8

# edge cases
assert kth_smallest([[7, 7], [7, 7]], 3) == 7          # all equal
assert kth_smallest([[1, 2], [3, 4]], 4) == 4 and kth_smallest([[1, 2], [3, 4]], 1) == 1
big = random_matrix(rng, 300, -10 ** 9, 10 ** 9)
assert kth_smallest(big, 45000) == kth_brute(big, 45000) and kth_smallest(big, 90000) == kth_brute(big, 90000)
print("edge asserts passed (including a 300 x 300 matrix)")
