### Q25 ⭐⭐ 🟡 Set matrix zeroes in O(1) extra space. `matrix` is an m x n list of lists of integers (1 <= m, n <= 200). If a cell is 0, set its whole row and whole column to 0. Modify the matrix in place and also return it, using O(1) extra space beyond the matrix: first remember in two booleans whether row 0 and column 0 contain a zero, then use row 0 and column 0 as the marker arrays for the other rows and columns, then zero the inner cells from the markers, and finally zero row 0 and column 0 from the two booleans. Part 1 Q31 states this problem at concept level; here you must write it fully and explain the trap: a version that marks `matrix[i][0] = 0` and `matrix[0][j] = 0` for every zero at (i, j) and later zeroes row 0 and column 0 whenever `matrix[0][0] == 0` (instead of using two saved booleans) gives a wrong result for 42 of the 512 binary 3 x 3 matrices (it cannot tell whether row 0 and column 0 held a zero themselves or were only marked). Give one failing 3 x 3 input of that version and say what it returns. Compare with the O(m + n) extra-space version that keeps two sets. In the answer include a dry run on the first example and a seeded random cross-check of your solution against two sets of zero rows and zero columns on small inputs. Example: matrix=[[1, 1, 1], [1, 0, 1], [1, 1, 1]] -> [[1, 0, 1], [0, 0, 0], [1, 0, 1]]; matrix=[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]] -> [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]; matrix=[[1, 2], [3, 4]] -> [[1, 2], [3, 4]]; matrix=[[1, 0]] -> [[0, 0]].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** In-place matrix with the first row and first column reused as marker arrays. This trades the O(m + n) sets for O(1) extra space.

**Say this first (1 line):** "Save two booleans first (does row 0 or column 0 hold a zero?), then use row 0 and column 0 as flags for the rest, zero the inner cells, and last fix row 0 and column 0 from the booleans."

**Brute force:** Two sets: rows that contain a zero and columns that contain a zero. A second pass sets a cell to 0 if its row or column is in a set. O(m * n) time, O(m + n) space. Even simpler: copy the matrix. O(m * n) space. The two-set version is the oracle here.

**Optimal:**
1. `row0 = any zero in matrix[0]`, `col0 = any zero in matrix[i][0]`. Do this before touching anything.
2. For i, j from 1: if `matrix[i][j] == 0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`.
3. For i, j from 1: if `matrix[i][0] == 0` or `matrix[0][j] == 0`, set `matrix[i][j] = 0`.
4. If `row0`, zero all of row 0. If `col0`, zero all of column 0.

Invariant: after step 2 each marker cell `matrix[i][0]` or `matrix[0][j]` is 0 if and only if row i or column j needs clearing, as far as the inner cells are concerned. The original zeros in row 0 and column 0 are not lost because step 1 saved them in two booleans.

The trap: if you mark for every zero (including zeros that were in row 0 or column 0 already) and later look at `matrix[0][0] == 0` to decide about row 0 and column 0, you cannot tell "row 0 had a zero" from "I wrote a marker into row 0". That version is wrong on 42 of the 512 binary 3 x 3 matrices (counted exhaustively below). One failing input: `[[1,1,1],[0,1,1],[1,0,1]]`. Zeros are at (1,0) and (2,1). The correct result is `[[0,0,1],[0,0,0],[0,0,0]]`. The naive code marks `matrix[0][0] = 0` while handling the zero at (1,0), and then wipes the whole of row 0 and returns all zeros.

**Complexity:** Time O(m * n): a constant number of passes. Extra space O(1): two booleans. The two-set version takes O(m + n) extra space.

**Dry run:** `[[1,1,1],[1,0,1],[1,1,1]]`. Row 0 has no zero, column 0 has no zero. The only inner zero is at (1,1), so mark `matrix[1][0] = 0` and `matrix[0][1] = 0`: `[[1,0,1],[0,0,1],[1,1,1]]`. Inner pass: (1,2) has marker `matrix[1][0] = 0` so it becomes 0, (2,1) has marker `matrix[0][1] = 0` so it becomes 0. Result `[[1,0,1],[0,0,0],[1,0,1]]`. Both flags are False, so nothing else changes. The program prints the stages.

**Code:**
```python
import itertools
import random

random.seed(2501)

def set_zeroes(matrix):
    """O(1) extra space: row 0 and column 0 are the marker arrays."""
    m, n = len(matrix), len(matrix[0])
    row0 = any(matrix[0][j] == 0 for j in range(n))      # saved BEFORE markers overwrite row 0
    col0 = any(matrix[i][0] == 0 for i in range(m))      # saved BEFORE markers overwrite col 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if row0:
        for j in range(n): matrix[0][j] = 0
    if col0:
        for i in range(m): matrix[i][0] = 0
    return matrix

def naive_markers(matrix):
    """The TRAP: marks for every zero (including row 0 / col 0 ones), then decides row 0 and col 0 from matrix[0][0]."""
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if matrix[0][0] == 0:
        for j in range(n): matrix[0][j] = 0
        for i in range(m): matrix[i][0] = 0
    return matrix

def two_sets(matrix):
    """O(m + n) extra space oracle: collect zero rows and columns, then write."""
    rows = {i for i, r in enumerate(matrix) if 0 in r}
    cols = {j for r in matrix for j, v in enumerate(r) if v == 0}
    return [[0 if i in rows or j in cols else v for j, v in enumerate(r)] for i, r in enumerate(matrix)]

def cp(x): return [r[:] for r in x]

examples = [([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
            ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
            ([[1, 2], [3, 4]], [[1, 2], [3, 4]]), ([[1, 0]], [[0, 0]])]
for mat, want in examples:
    a = cp(mat); r = set_zeroes(a)
    assert r is a and a == want == two_sets(mat)           # in place AND returned
    print(mat, '->', a)

# dry run: example 1, stage by stage
mat = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
print('row0 has zero:', any(v == 0 for v in mat[0]), ' col0 has zero:', any(r[0] == 0 for r in mat))
mark = cp(mat)
mark[1][0] = mark[0][1] = 0                  # the only inner zero is (1,1): mark its row and column
print('after marking :', mark)
for i in range(1, 3):
    for j in range(1, 3):
        if mark[i][0] == 0 or mark[0][j] == 0: mark[i][j] = 0
print('after inner pass:', mark, '(row 0 and col 0 hold the zeros their markers made; both saved flags are False, so nothing more to do)')

# seeded random cross-check against the two-set version (values 0..3, zeros common)
for _ in range(3000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.choice([0, 0, 1, 2, 3]) for _ in range(n)] for _ in range(m)]
    a = cp(mat)
    assert set_zeroes(a) == two_sets(mat)
print('random cross-check ok: 3000 cases')

# exhaustive over every binary matrix of shapes up to 3 x 3 (and 1 x n, m x 1 up to 6)
shapes = [(m, n) for m in range(1, 4) for n in range(1, 4)] + [(1, 6), (6, 1), (2, 5), (5, 2)]
total = 0
wrong = 0
first_bad = None
for m, n in shapes:
    for cells in itertools.product((0, 1), repeat=m * n):
        mat = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
        want = two_sets(mat)
        assert set_zeroes(cp(mat)) == want
        total += 1
        if (m, n) == (3, 3):
            if naive_markers(cp(mat)) != want:
                wrong += 1
                if first_bad is None or sum(map(sum, mat)) > sum(map(sum, first_bad)):
                    first_bad = mat
print('correct version exhaustive ok:', total, 'binary matrices over', len(shapes), 'shapes')
print('naive marker version wrong on', wrong, 'of 512 binary 3x3 matrices')
bad = [[1, 1, 1], [0, 1, 1], [1, 0, 1]]
print('failing input :', bad)
print('naive returns :', naive_markers(cp(bad)))
print('correct       :', two_sets(bad))
assert wrong == 42 and naive_markers(cp(bad)) != two_sets(bad)

# edge asserts: zero at the corner, whole zero matrix, single cell, non-binary values stay
assert set_zeroes([[0]]) == [[0]] and set_zeroes([[7]]) == [[7]]
assert set_zeroes([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
assert set_zeroes([[5, 6, 7], [8, 0, 9]]) == [[5, 0, 7], [0, 0, 0]]
big = [[1] * 200 for _ in range(200)]; big[199][199] = 0
r = set_zeroes(big)
assert sum(map(sum, r)) == 199 * 199
print('edge asserts ok')
```

**Output (my run):**
```
[[1, 1, 1], [1, 0, 1], [1, 1, 1]] -> [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]] -> [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
[[1, 2], [3, 4]] -> [[1, 2], [3, 4]]
[[1, 0]] -> [[0, 0]]
row0 has zero: False  col0 has zero: False
after marking : [[1, 0, 1], [0, 0, 1], [1, 1, 1]]
after inner pass: [[1, 0, 1], [0, 0, 0], [1, 0, 1]] (row 0 and col 0 hold the zeros their markers made; both saved flags are False, so nothing more to do)
random cross-check ok: 3000 cases
correct version exhaustive ok: 2858 binary matrices over 13 shapes
naive marker version wrong on 42 of 512 binary 3x3 matrices
failing input : [[1, 1, 1], [0, 1, 1], [1, 0, 1]]
naive returns : [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
correct       : [[0, 0, 1], [0, 0, 0], [0, 0, 0]]
edge asserts ok
```

**Edge cases:**
- 1 x n and m x 1: the inner loops are empty and only the flags work (`[[1,0]]` gives `[[0,0]]`).
- A zero at (0,0): both flags become True.
- Zero only in row 0: only the columns of those zeros are cleared, and row 0 itself.
- All zeros and non-binary values (the real test uses any integers): only the zero test matters.
- Return the same list object (the program asserts `r is a`).
- 200 x 200 with one zero in the corner: result keeps 199 x 199 cells.

**Follow-ups:**
- *Why not use a sentinel like None or -1?* It works for simple values but needs a value that cannot appear; the marker trick has no such assumption.
- *Time cost compared with the two sets?* Same O(m * n); you save only the memory.
- *Part 1 Q31 is the concept version; why does the order of steps matter here?* Because the markers live inside the data, anything that reads them before the saved booleans are applied sees a polluted state.

**Common mistakes:**
- Clearing row 0 or column 0 before the inner cells are processed (the markers disappear).
- Starting the inner loops at 0 instead of 1.
- Using `matrix[0][0]` for both row 0 and column 0 (the 42-of-512 bug above).
- Returning a new matrix when the problem says modify in place.
