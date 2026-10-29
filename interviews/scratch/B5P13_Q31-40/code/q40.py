import itertools
import random

random.seed(4001)


def solve(matrix, ops, stats=None):
    mat = [list(r) for r in matrix]
    rows = [list(itertools.accumulate(r, initial=0)) for r in mat]   # rows[r][c] = sum of mat[r][:c]
    out = []
    for op in ops:
        if op[0] == "update":
            _, r, c, v = op
            mat[r][c] = v
            rows[r] = list(itertools.accumulate(mat[r], initial=0))  # rebuild ONE row: O(n)
            if stats is not None:
                stats["update_work"] += len(mat[r])
            out.append(None)
        else:
            _, r1, c1, r2, c2 = op
            out.append(sum(rows[r][c2 + 1] - rows[r][c1] for r in range(r1, r2 + 1)))   # one difference per row: O(m)
            if stats is not None:
                stats["query_work"] += r2 - r1 + 1
    return out


def brute(matrix, ops):
    mat = [list(r) for r in matrix]
    out = []
    for op in ops:
        if op[0] == "update":
            mat[op[1]][op[2]] = op[3]
            out.append(None)
        else:
            out.append(sum(mat[i][j] for i in range(op[1], op[3] + 1) for j in range(op[2], op[4] + 1)))
    return out


# dry run on the first example
matrix = [[3, 0, 1], [5, 6, 3], [1, 2, 0]]
rows = [list(itertools.accumulate(r, initial=0)) for r in matrix]
print("row prefix lists:", rows)
print("sum (0,0)-(2,2): row0", rows[0][3] - rows[0][0], "+ row1", rows[1][3] - rows[1][0], "+ row2", rows[2][3] - rows[2][0], "= 21")
matrix[1][1] = 10
rows[1] = list(itertools.accumulate(matrix[1], initial=0))
print("update (1,1)=10 rebuilds only row 1:", rows[1], "(other rows untouched)")
print("sum (1,1)-(2,2): row1", rows[1][3] - rows[1][1], "+ row2", rows[2][3] - rows[2][1], "= 15")
print("sum (0,0)-(1,1): row0", rows[0][2] - rows[0][0], "+ row1", rows[1][2] - rows[1][0], "= 18")

for mt, ops, want in [([[3, 0, 1], [5, 6, 3], [1, 2, 0]], [["sum", 0, 0, 2, 2], ["update", 1, 1, 10], ["sum", 1, 1, 2, 2], ["sum", 0, 0, 1, 1]], [21, None, 15, 18]),
                      ([[4]], [["update", 0, 0, -4], ["sum", 0, 0, 0, 0]], [None, -4])]:
    got = solve(mt, ops)
    assert got == want == brute(mt, ops)
    print(got)


# the static 2D prefix table (Q5 style): O(1) query, but one update changes up to m*n cells
def static_table(mat):
    m, n = len(mat), len(mat[0])
    p = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            p[i + 1][j + 1] = mat[i][j] + p[i][j + 1] + p[i + 1][j] - p[i][j]
    return p

m = [[1] * 4 for _ in range(4)]
p1 = static_table(m)
m[0][0] = 2
p2 = static_table(m)
changed = sum(p1[i][j] != p2[i][j] for i in range(5) for j in range(5))
print("\nstatic table: updating the corner cell (0,0) of a 4x4 matrix changes", changed, "of 16 table cells")
m[3][3] = 2
p3 = static_table(m)
print("updating cell (3,3) changes", sum(p2[i][j] != p3[i][j] for i in range(5) for j in range(5)), "table cell")

# seeded random cross-check against recomputing every rectangle from the current matrix
def rand_case(rng, mmax=6, nmax=6, k=40):
    m_, n_ = rng.randint(1, mmax), rng.randint(1, nmax)
    mt = [[rng.randint(-9, 9) for _ in range(n_)] for _ in range(m_)]
    ops = []
    for _ in range(rng.randint(0, k)):
        if rng.random() < 0.4:
            ops.append(["update", rng.randrange(m_), rng.randrange(n_), rng.randint(-9, 9)])
        else:
            r1 = rng.randrange(m_); r2 = rng.randint(r1, m_ - 1)
            c1 = rng.randrange(n_); c2 = rng.randint(c1, n_ - 1)
            ops.append(["sum", r1, c1, r2, c2])
    return mt, ops
rng = random.Random(40)
for _ in range(500):
    mt, ops = rand_case(rng)
    assert solve(mt, ops) == brute(mt, ops)
print("500 seeded random cases match the recompute-from-matrix oracle")

# maximum size: 100 x 100 matrix, 10^4 ops; count elementary steps (deterministic, unlike wall time)
mt = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(100)] for _ in range(100)]
ops = []
for _ in range(10 ** 4):
    if rng.random() < 0.5:
        ops.append(["update", rng.randrange(100), rng.randrange(100), rng.randint(-10 ** 6, 10 ** 6)])
    else:
        r1 = rng.randrange(100); r2 = rng.randint(r1, 99); c1 = rng.randrange(100); c2 = rng.randint(c1, 99)
        ops.append(["sum", r1, c1, r2, c2])
st = {"update_work": 0, "query_work": 0}
res = solve(mt, ops, st)
assert res == brute(mt, ops)
print("10^4 ops on 100 x 100:", st, "| the brute force would touch up to 10^4 cells per query")

# edge cases
assert solve([[7]], [["sum", 0, 0, 0, 0]]) == [7]
assert solve([[1, 2], [3, 4]], [["sum", 0, 0, 1, 1], ["update", 1, 1, 0], ["sum", 0, 0, 1, 1], ["sum", 1, 0, 1, 0]]) == [10, None, 6, 3]
assert solve([[5]], [["update", 0, 0, 5]]) == [None]
print("edge asserts ok")
