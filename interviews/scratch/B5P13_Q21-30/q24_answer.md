### Q24 ⭐⭐ 🟡 Matrix block sum. `mat` is an m x n list of lists of integers (1 <= m, n <= 100, |value| <= 100) and `k` is an integer with 0 <= k <= 100. Return an m x n matrix `ans` where `ans[i][j]` is the sum of `mat[r][c]` over all cells with i - k <= r <= i + k and j - k <= c <= j + k that lie inside the matrix (the square is clipped at the borders). Use a 2D prefix-sum table so each cell costs O(1) after an O(m * n) build, clamping the four corners with `max(0, i - k)` and `min(m - 1, i + k)` (and the same for columns). Explain why the clamping is correct, and compare with the O(m * n * k^2) direct method. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the direct double loop over the clipped square on small inputs. Example: mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], k=1 -> [[12, 21, 16], [27, 45, 33], [24, 39, 28]]; mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], k=2 -> [[45, 45, 45], [45, 45, 45], [45, 45, 45]]; mat=[[5]], k=3 -> [[5]]; mat=[[1, 2], [3, 4]], k=0 -> [[1, 2], [3, 4]].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** 2D prefix sums. One table lets you read any rectangle sum with four lookups.

**Say this first (1 line):** "Build `P` where `P[i][j]` is the sum of the top-left i x j block; each answer cell is a rectangle with clamped corners, read with inclusion-exclusion in O(1)."

**Brute force:** For each cell, loop over the clipped (2k+1) x (2k+1) square and add. O(m * n * k^2) in the worst case. For a 100 x 100 matrix with k = 100 the clipped squares are the whole matrix: 100,000,000 reads (computed from the formula in the program, not run).

**Optimal:**
- `P` has size (m+1) x (n+1), with a zero first row and column. `P[i+1][j+1] = mat[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]`. The last term removes the overlap that was added twice.
- For cell (i, j): `r1 = max(0, i-k)`, `r2 = min(m-1, i+k)`, `c1 = max(0, j-k)`, `c2 = min(n-1, j+k)`.
- Sum = `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`.
- Why clamping is right: the problem says cells outside the matrix do not exist, so the sum over the square equals the sum over the square intersected with the matrix. That intersection is still a rectangle, whose corners are exactly the clamped values. Without clamping you would index outside the table, or, with negative indexes, silently read from the other end in Python.

**Complexity:** Build O(m * n), queries O(m * n) (4 lookups each). Total O(m * n), space O(m * n) for `P` and for the answer. For the 100 x 100 case with k = 10 the direct method reads 3,960,100 cells, the table 40,000 (the program prints these).

**Dry run:** `[[1,2,3],[4,5,6],[7,8,9]]`, k = 1. Prefix table: `[[0,0,0,0],[0,1,3,6],[0,5,12,21],[0,12,27,45]]`. Cell (0,0): rows 0..1, columns 0..1, so `P[2][2] - P[0][2] - P[2][0] + P[0][0] = 12 - 0 - 0 + 0 = 12`. That is 1 + 2 + 4 + 5. Center cell (1,1): rows 0..2, columns 0..2, so `45 - 0 - 0 + 0 = 45`.

**Code:**
```python
import itertools
import random

random.seed(2401)

def block_sum(mat, k):
    m, n = len(mat), len(mat[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]        # P[i][j] = sum of mat[:i][:j]
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = mat[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            r1, r2 = max(0, i - k), min(m - 1, i + k)      # clip to the matrix
            c1, c2 = max(0, j - k), min(n - 1, j + k)
            row.append(P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1])
        out.append(row)
    return out

def brute(mat, k, count=None):
    m, n = len(mat), len(mat[0])
    visits = 0
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            s = 0
            for r in range(max(0, i - k), min(m - 1, i + k) + 1):
                for c in range(max(0, j - k), min(n - 1, j + k) + 1):
                    s += mat[r][c]; visits += 1
            row.append(s)
        out.append(row)
    if count is not None:
        count.append(visits)
    return out

G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
examples = [(G, 1, [[12, 21, 16], [27, 45, 33], [24, 39, 28]]),
            (G, 2, [[45] * 3] * 3), ([[5]], 3, [[5]]), ([[1, 2], [3, 4]], 0, [[1, 2], [3, 4]])]
for mat, k, want in examples:
    assert block_sum(mat, k) == want == brute(mat, k)
    print('k =', k, mat, '->', block_sum(mat, k))

# dry run: the prefix table of G and the cell (0, 0) with k = 1
P = [[0] * 4 for _ in range(4)]
for i in range(3):
    for j in range(3):
        P[i + 1][j + 1] = G[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
print('prefix table:', P)
print('cell (0,0), k=1: rows 0..1, cols 0..1 ->', P[2][2], '-', P[0][2], '-', P[2][0], '+', P[0][0], '=', P[2][2] - P[0][2] - P[2][0] + P[0][0])

# seeded random cross-check
for _ in range(2000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    k = random.randint(0, 7)
    assert block_sum(mat, k) == brute(mat, k)
print('random cross-check ok: 2000 cases')

# exhaustive: every 2 x 3 matrix over {-1,0,1} and k = 0..3
cnt = 0
for cells in itertools.product((-1, 0, 1), repeat=6):
    mat = [list(cells[:3]), list(cells[3:])]
    for k in range(4):
        assert block_sum(mat, k) == brute(mat, k); cnt += 1
print('exhaustive 2x3 ok:', cnt, 'cases')

# cost: cell reads of the direct method (from the clipped square sizes) versus 4 table reads per cell
def clipped_cells(m, n, k):          # number of cell reads the direct method makes
    rows = sum(min(m - 1, i + k) - max(0, i - k) + 1 for i in range(m))
    cols = sum(min(n - 1, j + k) - max(0, j - k) + 1 for j in range(n))
    return rows * cols
for m, n, k in [(100, 100, 1), (100, 100, 10), (100, 100, 100)]:
    print(f'{m}x{n}, k={k}: direct reads {clipped_cells(m, n, k)} cells; prefix table: 4 reads per cell = {4 * m * n}')
mat = [[random.randint(-5, 5) for _ in range(7)] for _ in range(6)]
v = []
brute(mat, 2, v)
assert v[0] == clipped_cells(6, 7, 2)
big = [[random.randint(-100, 100) for _ in range(100)] for _ in range(100)]
assert block_sum(big, 100) == [[sum(map(sum, big))] * 100] * 100          # whole-matrix sum everywhere
assert block_sum([[7]], 100) == [[7]]
print('edge asserts ok')
```

**Output (my run):**
```
k = 1 [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[12, 21, 16], [27, 45, 33], [24, 39, 28]]
k = 2 [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[45, 45, 45], [45, 45, 45], [45, 45, 45]]
k = 3 [[5]] -> [[5]]
k = 0 [[1, 2], [3, 4]] -> [[1, 2], [3, 4]]
prefix table: [[0, 0, 0, 0], [0, 1, 3, 6], [0, 5, 12, 21], [0, 12, 27, 45]]
cell (0,0), k=1: rows 0..1, cols 0..1 -> 12 - 0 - 0 + 0 = 12
random cross-check ok: 2000 cases
exhaustive 2x3 ok: 2916 cases
100x100, k=1: direct reads 88804 cells; prefix table: 4 reads per cell = 40000
100x100, k=10: direct reads 3960100 cells; prefix table: 4 reads per cell = 40000
100x100, k=100: direct reads 100000000 cells; prefix table: 4 reads per cell = 40000
edge asserts ok
```

**Edge cases:**
- k = 0: each cell equals itself.
- k larger than the matrix: every answer is the total sum (checked at 100 x 100, k = 100).
- 1 x 1, 1 x n and m x 1 matrices: clamping handles them.
- Negative values: nothing assumes the sums are non-negative.
- Values up to 100 over 10^4 cells: at most 10^6 in magnitude, no overflow in Python (and fits int32 in other languages).

**Follow-ups:**
- *Region queries on a fixed matrix?* Same table; each query is 4 lookups (matrix region sum).
- *Point updates between queries?* Rebuild is O(m * n); use a 2D Fenwick tree (Part 14) or per-row prefix sums (Q40).
- *Add a value over a rectangle many times?* Use a 2D difference array and one 2D prefix pass at the end.

**Common mistakes:**
- Forgetting to add back `P[r1][c1]` (the corner subtracted twice).
- Mixing inclusive and exclusive bounds: with the (m+1) x (n+1) table the upper indexes are `r2+1`, `c2+1`.
- Clamping only one side (`max` but not `min`).
- Building `P` without the zero padding row and column, which forces special cases for the first row and column.
