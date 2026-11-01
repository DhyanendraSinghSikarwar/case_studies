import random
from bisect import bisect_right

CALLS = 0


def count_le(matrix, v):
    global CALLS
    total = 0
    for row in matrix:
        CALLS += 1
        total += bisect_right(row, v)
    return total


def matrix_median(matrix):
    r, c = len(matrix), len(matrix[0])
    need = (r * c + 1) // 2                         # r*c odd, so this is the middle rank
    lo = min(row[0] for row in matrix)
    hi = max(row[-1] for row in matrix)
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(matrix, mid) >= need:
            hi = mid
        else:
            lo = mid + 1
    return lo


def matrix_median_brute(matrix):
    flat = sorted(x for row in matrix for x in row)
    return flat[len(flat) // 2]


for m, want in [([[1, 3, 5], [2, 6, 9], [3, 6, 9]], 5), ([[1]], 1), ([[1, 1, 1], [2, 2, 2], [3, 3, 3]], 2)]:
    print(m, "->", matrix_median(m), " brute:", matrix_median_brute(m))
    assert matrix_median(m) == matrix_median_brute(m) == want

rng = random.Random(37)
for _ in range(2000):
    r = rng.choice([1, 3, 5])
    c = rng.choice([1, 3, 5, 7])
    hi = rng.choice([3, 10, 100])
    m = [sorted(rng.randint(0, hi) for _ in range(c)) for _ in range(r)]
    v = matrix_median(m)
    assert v == matrix_median_brute(m), m
    assert any(v in row for row in m)               # the answer is an actual entry
print("2000 seeded random odd-by-odd matrices agree; answer was always an entry")

# why flattening-and-bisecting fails: flattening row by row is not sorted
m = [[1, 3, 5], [2, 6, 9], [3, 6, 9]]
flat = [x for row in m for x in row]
print("row-major flatten:", flat, "sorted?", flat == sorted(flat))
assert flat != sorted(flat)

# call count on a big case: r = 999, c = 1001 (about 10**6 entries), values up to 10**9
big = [sorted(rng.randint(0, 10**9) for _ in range(1001)) for _ in range(999)]
CALLS = 0
v = matrix_median(big)
steps = CALLS // 999
print("big matrix 999 x 1001: value-search steps =", steps, " bisect_right calls =", CALLS)
assert steps <= 30
assert v == matrix_median_brute(big)
# edge asserts
assert matrix_median([[7, 7, 7]]) == 7
assert matrix_median([[1], [2], [3]]) == 2
assert matrix_median([[5, 5, 5], [5, 5, 5], [5, 5, 5]]) == 5
assert matrix_median([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 5
print("all checks passed")
