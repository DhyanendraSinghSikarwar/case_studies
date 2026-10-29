### Q27 ⭐⭐ 🟡 Diagonal traverse of a matrix. `mat` is an m x n list of lists of integers (1 <= m, n <= 100). Return all elements by anti-diagonals (cells with equal i + j) alternating direction, starting with the diagonal of the top-left cell going up-right: that diagonal has one cell; the next goes down-left; the next goes up-right again, and so on, finishing at the bottom-right cell. For a 3 x 3 matrix [[1,2,3],[4,5,6],[7,8,9]] the order is 1, 2, 4, 7, 5, 3, 6, 8, 9. Explain that there are m + n - 1 anti-diagonals, that i + j is constant on each, and give two O(m * n) ways: a pointer walk with direction flips at the borders (the tricky part is the order of the border checks in the corners) and grouping by i + j then reversing every second group (O(m * n) extra space). Say what changes if you want the diagonals with constant i - j instead. In the answer include a dry run on the first example and a seeded random cross-check of your solution against grouping by i + j and reversing alternate groups on small inputs. Example: mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [1, 2, 4, 7, 5, 3, 6, 8, 9]; mat=[[1, 2], [3, 4]] -> [1, 2, 3, 4]; mat=[[1, 2, 3, 4]] -> [1, 2, 3, 4]; mat=[[1], [2], [3]] -> [1, 2, 3].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** Matrix traversal by anti-diagonals. All cells on one diagonal share `i + j`.

**Say this first (1 line):** "There are m + n - 1 diagonals; walk them with a direction flag and check the right and bottom borders before the top and left ones."

**Brute force / second method:** Put every cell into a bucket `groups[i + j]` (rows are visited top to bottom, so each bucket is in down-left order), then reverse the buckets with an even index (they go up-right). O(m * n) time and O(m * n) extra space. It is the oracle.

**Optimal (pointer walk):**
- Start at (0,0) going up. Emit `mat[i][j]`, then move:
  - Going up: if `j == n-1` move down one row (`i += 1`) and flip; else if `i == 0` move right (`j += 1`) and flip; else `i -= 1, j += 1`.
  - Going down: if `i == m-1` move right and flip; else if `j == 0` move down and flip; else `i += 1, j -= 1`.
- The order of the checks matters in the corners. At the top-right corner both `i == 0` and `j == n-1` are true while going up. The right border must win and move down, because moving right would leave the matrix. The same holds at the bottom-left corner going down: the bottom border (`i == m-1`) must come first. The program tests the swapped order and it walks off the grid (or returns nothing valid) on 33 of the 49 shapes up to 7 x 7.
- Total steps: exactly m * n.

**Complexity:** Time O(m * n), each cell is emitted once and each step is O(1). Space O(1) extra for the walk (the output is O(m * n)). The grouping method uses O(m * n) extra.

**Dry run:** 3 x 3. (0,0)=1 up, hits top border so go right: (0,1)=2 going down, left border not reached so (1,0)=4, then left border, go down: (2,0)=7 going up. (1,1)=5, (0,2)=3. At (0,2) the right border wins: go down to (1,2)=6 going down. (2,1)=8, then the bottom border: (2,2)=9. Order 1, 2, 4, 7, 5, 3, 6, 8, 9. The program prints the position and direction at every step.

**Code:**
```python
import itertools
import random

random.seed(2701)

def diag_walk(mat):
    m, n = len(mat), len(mat[0])
    i = j = 0
    up = True
    out = []
    for _ in range(m * n):
        out.append(mat[i][j])
        if up:
            if j == n - 1:   i += 1; up = False       # right border FIRST (this also covers the top-right corner)
            elif i == 0:     j += 1; up = False
            else:            i -= 1; j += 1
        else:
            if i == m - 1:   j += 1; up = True        # bottom border FIRST (covers the bottom-left corner)
            elif j == 0:     i += 1; up = True
            else:            i += 1; j -= 1
    return out

def group_by_sum(mat):
    m, n = len(mat), len(mat[0])
    groups = [[] for _ in range(m + n - 1)]
    for i in range(m):
        for j in range(n):
            groups[i + j].append(mat[i][j])          # row order: top to bottom = down-left direction
    out = []
    for s, g in enumerate(groups):
        out.extend(g[::-1] if s % 2 == 0 else g)     # even sums go up-right: reverse
    return out

def wrong_order(mat):
    """Same walk but checks the top/left border BEFORE the right/bottom border."""
    m, n = len(mat), len(mat[0])
    i = j = 0; up = True; out = []
    for _ in range(m * n):
        if not (0 <= i < m and 0 <= j < n):
            return None                              # walked off the grid
        out.append(mat[i][j])
        if up:
            if i == 0:       j += 1; up = False
            elif j == n - 1: i += 1; up = False
            else:            i -= 1; j += 1
        else:
            if j == 0:       i += 1; up = True
            elif i == m - 1: j += 1; up = True
            else:            i += 1; j -= 1
    return out

G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
examples = [(G, [1, 2, 4, 7, 5, 3, 6, 8, 9]), ([[1, 2], [3, 4]], [1, 2, 3, 4]),
            ([[1, 2, 3, 4]], [1, 2, 3, 4]), ([[1], [2], [3]], [1, 2, 3])]
for mat, want in examples:
    assert diag_walk(mat) == want == group_by_sum(mat)
    print(mat, '->', diag_walk(mat))

# dry run on the 3 x 3: position, direction, and which rule fired
i = j = 0; up = True; trace = []
for _ in range(9):
    trace.append(f'({i},{j})={G[i][j]}{"^" if up else "v"}')
    if up:
        if j == 2: i += 1; up = False
        elif i == 0: j += 1; up = False
        else: i -= 1; j += 1
    else:
        if i == 2: j += 1; up = True
        elif j == 0: i += 1; up = True
        else: i += 1; j -= 1
print(' '.join(trace))

# seeded random cross-check
for _ in range(2000):
    m, n = random.randint(1, 8), random.randint(1, 8)
    mat = [[random.randint(-50, 50) for _ in range(n)] for _ in range(m)]
    assert diag_walk(mat) == group_by_sum(mat)
print('random cross-check ok: 2000 cases')

# exhaustive over all shapes up to 7 x 7 using distinct labels (so any wrong order shows)
for m in range(1, 8):
    for n in range(1, 8):
        mat = [[i * n + j for j in range(n)] for i in range(m)]
        out = diag_walk(mat)
        assert out == group_by_sum(mat) and sorted(out) == list(range(m * n))
        assert out[0] == mat[0][0] and out[-1] == mat[m - 1][n - 1]
print('all shapes 1..7 x 1..7: permutation, starts top-left, ends bottom-right')

# the corner-order trap: how many shapes break when the border checks are in the wrong order
broken = [(m, n) for m in range(1, 8) for n in range(1, 8)
          if wrong_order([[i * n + j for j in range(n)] for i in range(m)]) != diag_walk([[i * n + j for j in range(n)] for i in range(m)])]
print('wrong check order breaks', len(broken), 'of 49 shapes, e.g.', broken[:4])
print('  wrong_order on the 3x3 ->', wrong_order(G))

# variant: constant i - j (main-direction diagonals), top-right start going down-right
def by_difference(mat):
    m, n = len(mat), len(mat[0])
    groups = {}
    for i in range(m):
        for j in range(n):
            groups.setdefault(j - i, []).append(mat[i][j])      # j - i from n-1 down to -(m-1)
    return [groups[k] for k in range(n - 1, -m, -1)]
print('i - j diagonals of the 3x3:', by_difference(G), '(count m + n - 1 =', 3 + 3 - 1, ')')
assert [len(g) for g in by_difference(G)] == [1, 2, 3, 2, 1]
assert diag_walk([[9]]) == [9]
big = [[i * 100 + j for j in range(100)] for i in range(100)]
assert len(diag_walk(big)) == 10000 and diag_walk(big) == group_by_sum(big)
print('edge asserts ok')
```

**Output (my run):**
```
[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [1, 2, 4, 7, 5, 3, 6, 8, 9]
[[1, 2], [3, 4]] -> [1, 2, 3, 4]
[[1, 2, 3, 4]] -> [1, 2, 3, 4]
[[1], [2], [3]] -> [1, 2, 3]
(0,0)=1^ (0,1)=2v (1,0)=4v (2,0)=7^ (1,1)=5^ (0,2)=3^ (1,2)=6v (2,1)=8v (2,2)=9^
random cross-check ok: 2000 cases
all shapes 1..7 x 1..7: permutation, starts top-left, ends bottom-right
wrong check order breaks 33 of 49 shapes, e.g. [(2, 1), (2, 2), (2, 3), (2, 4)]
  wrong_order on the 3x3 -> None
i - j diagonals of the 3x3: [[3], [2, 6], [1, 5, 9], [4, 8], [7]] (count m + n - 1 = 5 )
edge asserts ok
```

**Edge cases:**
- 1 x n: every step hits the top border going up, so the walk goes right one cell at a time: `[1,2,3,4]`.
- m x 1: the right border (`j == n-1 == 0`) fires first and moves down: `[1,2,3]`.
- 1 x 1: one emit, the final move is ignored.
- Non-square shapes: the diagonals grow, stay flat, then shrink; `m + n - 1` diagonals either way.

**Follow-ups:**
- *Diagonals with constant `i - j`?* Group by `j - i`, which runs from `n-1` down to `-(m-1)`. For the 3 x 3 you get `[3], [2, 6], [1, 5, 9], [4, 8], [7]` (printed). The count is the same, `m + n - 1`.
- *Zig-zag only the main-direction diagonals?* No direction flips are needed.
- *Spiral order?* Layer by layer with four bounds (the same border-check care).

**Common mistakes:**
- Checking `i == 0` before `j == n-1` when going up (or `j == 0` before `i == m-1` when going down).
- Moving after the last cell and indexing out of range (guard with a count of m * n, not a bounds check).
- Reversing the wrong parity of groups in the bucket method: even `i + j` goes up-right and is reversed.
