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
