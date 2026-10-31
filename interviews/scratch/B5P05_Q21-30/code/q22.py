import random
from bisect import bisect_left


def search_brute(mat, t):
    return any(t in row for row in mat)


def search_staircase(mat, t, counter=None):
    # start top-right: left is smaller, down is larger. O(m + n)
    m, n = len(mat), len(mat[0])
    r, c = 0, n - 1
    while r < m and c >= 0:
        if counter is not None:
            counter[0] += 1
        v = mat[r][c]
        if v == t:
            return True
        if v > t:
            c -= 1          # everything below v in this column is bigger: drop the column
        else:
            r += 1          # everything left of v in this row is smaller: drop the row
    return False


def search_rows(mat, t, counter=None):
    # binary search every row. O(m log n)
    for row in mat:
        i = bisect_left(row, t)
        if counter is not None:
            counter[0] += max(1, len(row).bit_length())
        if i < len(row) and row[i] == t:
            return True
    return False


def search_short_side(mat, t):
    # binary search along the longer side, loop over the shorter one: O(min(m,n) * log(max(m,n)))
    m, n = len(mat), len(mat[0])
    if m <= n:
        return search_rows(mat, t)
    cols = [[mat[r][c] for r in range(m)] for c in range(n)]   # transpose (O(mn), only for the demo)
    return search_rows(cols, t)


M = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
for mat, t, want in [(M, 5, True), (M, 20, False), ([[-5]], -5, True)]:
    assert search_staircase(mat, t) == search_rows(mat, t) == search_brute(mat, t) == want
    print("target", t, "->", search_staircase(mat, t))

# why flattening is invalid: the flattened list is not sorted, so bisect on it can miss present values
flat = [v for row in M for v in row]
i = bisect_left(flat, 5)
print("flattened sorted?", flat == sorted(flat), "| bisect on flat finds 5?", i < len(flat) and flat[i] == 5)
assert flat != sorted(flat) and not (i < len(flat) and flat[i] == 5)   # 5 is in M, flatten+bisect says no

# comparison counts (worst over all targets) when m is much smaller than n (1 x 300) and when square (300 x 300)
for m, n in [(1, 300), (300, 300)]:
    mat = [[r * 1000 + c for c in range(n)] for r in range(m)]     # rows and columns both ascending
    worst_a = worst_b = 0
    for t in [-1] + [r * 1000 for r in range(m)] + [r * 1000 + n - 1 for r in range(m)]:
        a, b = [0], [0]
        search_staircase(mat, t, a)
        search_rows(mat, t, b)
        worst_a, worst_b = max(worst_a, a[0]), max(worst_b, b[0])
    print(f"{m} x {n}: staircase max steps over probe targets = {worst_a} (<= m+n-1 = {m + n - 1}), "
          f"row-bisect worst steps ~ {worst_b} (m * bit_length(n))")

# random cross-check: build a valid matrix by sorting rows, then sorting each column
rng = random.Random(22)
for _ in range(1500):
    m, n = rng.randint(1, 6), rng.randint(1, 6)
    mat = [sorted(rng.randint(-8, 20) for _ in range(n)) for _ in range(m)]
    cols = [sorted(mat[r][c] for r in range(m)) for c in range(n)]
    mat = [[cols[c][r] for c in range(n)] for r in range(m)]
    assert all(mat[r][c] <= mat[r][c + 1] for r in range(m) for c in range(n - 1))
    assert all(mat[r][c] <= mat[r + 1][c] for r in range(m - 1) for c in range(n))
    for t in range(-10, 23):
        w = search_brute(mat, t)
        assert search_staircase(mat, t) == search_rows(mat, t) == search_short_side(mat, t) == w, (mat, t)
print("random check passed: 1500 matrices x 33 targets")

# edge cases
assert search_staircase([[1, 2, 3]], 3) and not search_staircase([[1, 2, 3]], 4)
assert search_staircase([[1], [2], [3]], 1) and not search_staircase([[1], [2], [3]], 0)
assert search_staircase([[2, 2], [2, 2]], 2) and not search_staircase([[2, 2], [2, 2]], 3)
print("edge asserts passed")
