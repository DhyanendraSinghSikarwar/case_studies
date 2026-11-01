from collections import Counter
import random

def brute(mat, target):                            # O(m^2 n^2) with a 2D prefix-sum table
    m, n = len(mat), len(mat[0]) if mat else 0
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = mat[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    cnt = 0
    for r1 in range(m):
        for r2 in range(r1, m):
            for c1 in range(n):
                for c2 in range(c1, n):
                    s = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
                    cnt += s == target
    return cnt

def subarray_sum_k(arr, k):                        # the 1D hashmap routine: count subarrays with sum k
    seen, pre, cnt = Counter({0: 1}), 0, 0
    for v in arr:
        pre += v
        cnt += seen[pre - k]
        seen[pre] += 1
    return cnt

def optimal(mat, target):                          # O(m^2 * n) time, O(n) extra space (plus O(n) map)
    if not mat or not mat[0]: return 0
    m, n = len(mat), len(mat[0])
    total = 0
    for top in range(m):
        col = [0] * n                              # column sums of rows top..bottom
        for bottom in range(top, m):
            for j in range(n): col[j] += mat[bottom][j]
            total += subarray_sum_k(col, target)
    return total

ex = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
assert brute(ex, 0) == optimal(ex, 0) == 4
print("example target 0:", optimal(ex, 0), "| same matrix target 1:", optimal(ex, 1), "(brute", brute(ex, 1), ")")
ex2 = [[1, -1], [-1, 1]]
print("[[1,-1],[-1,1]] target 0:", optimal(ex2, 0), "(brute", brute(ex2, 0), ")")

rng = random.Random(50)
for _ in range(500):
    m, n = rng.randint(1, 5), rng.randint(1, 5)
    mat = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
    t = rng.randint(-4, 4)
    assert brute(mat, t) == optimal(mat, t), (mat, t)
print("500 seeded cross-checks passed (negatives included)")

assert optimal([], 0) == 0 and optimal([[]], 0) == 0
assert optimal([[5]], 5) == 1 and optimal([[5]], 4) == 0
assert optimal([[0] * 4 for _ in range(4)], 0) == (4 * 5 // 2) ** 2     # all zeros: every rectangle counts
assert optimal([[1, 2, 3]], 6) == 1                                       # single row degenerates to 1D
assert optimal([[1], [2], [3]], 5) == 1                                   # single column
assert optimal([[-1, -1], [-1, -1]], -2) == 4                             # negatives: 2 horizontal, 2 vertical
big = [[(i * 7 + j * 3) % 5 - 2 for j in range(60)] for i in range(60)]
print("60x60 pattern matrix, target 0:", optimal(big, 0))
print("edge asserts passed")
