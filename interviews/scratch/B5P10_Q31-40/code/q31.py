import random

random.seed(31)

def alias_trap(m, n, ops):
    bug = [[0] * n] * m                                   # m references to ONE row list
    ok = [[0 for _ in range(n)] for _ in range(m)]        # m separate row lists
    for r, c, v in ops:
        bug[r][c] = v
        ok[r][c] = v
    return [bug, ok, len({id(row) for row in bug}), len({id(row) for row in ok})]

def model(m, n, ops):
    """Hand model: bug has ONE row, so a write at (r, c) changes column c everywhere."""
    one_row = [0] * n
    real = [[0] * n for _ in range(m)]
    for r, c, v in ops:
        one_row[c] = v          # the single shared row
        real[r][c] = v          # a real, independent cell
    return [[one_row[:] for _ in range(m)], real, 1, m]

# ---- examples from the prompt
assert alias_trap(2, 3, [[0, 1, 5]]) == [[[0, 5, 0], [0, 5, 0]], [[0, 5, 0], [0, 0, 0]], 1, 2]
assert alias_trap(3, 2, [[0, 0, 1], [2, 1, 7], [1, 0, 9]]) == [[[9, 7], [9, 7], [9, 7]], [[1, 0], [9, 0], [0, 7]], 1, 3]
assert alias_trap(1, 1, []) == [[[0]], [[0]], 1, 1]
print('examples ok')

# ---- show the mechanism: * copies the reference, not the list
row = [0] * 3
t = [row] * 2
print('t[0] is t[1]:', t[0] is t[1], '| [0]*3 elements share one int object:', row[0] is row[1])
row[0] = 5   # rebinding a slot never mutates the int 0, so [0]*n is safe
print('after row[0] = 5:', row)

# ---- DPs filled row by row on the aliased table. The shared row acts like a rolling array.
def grid(m, n, diagonal, aliased):
    dp = [[0] * n] * m if aliased else [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if r == 0 or c == 0:
                dp[r][c] = 1
            else:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1] + (dp[r - 1][c - 1] if diagonal else 0)
    return dp[m - 1][n - 1]
print('unique paths 3x3 (right/down moves): aliased =', grid(3, 3, False, True), ' correct =', grid(3, 3, False, False))
print('paths with a diagonal move 3x3:      aliased =', grid(3, 3, True, True), ' correct =', grid(3, 3, True, False))
assert grid(3, 3, False, True) == grid(3, 3, False, False) == 6      # the bug hides: reads of row r-1 see the old value
assert grid(3, 3, True, False) == 13 and grid(3, 3, True, True) != 13  # dp[r-1][c-1] was already overwritten

# ---- seeded cross-check: solution vs the hand model (and an exhaustive sweep of tiny shapes)
cases = 0
for _ in range(1000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    ops = [[random.randrange(m), random.randrange(n), random.randint(-9, 9)] for _ in range(random.randint(0, 8))]
    assert alias_trap(m, n, ops) == model(m, n, ops), (m, n, ops)
    cases += 1
for m in range(1, 4):
    for n in range(1, 4):
        for r in range(m):
            for c in range(n):
                assert alias_trap(m, n, [[r, c, 7]]) == model(m, n, [[r, c, 7]])
                cases += 1
print('cross-check passed on', cases, 'cases')

# ---- edge cases
assert alias_trap(1, 3, [[0, 2, 4]])[0] == alias_trap(1, 3, [[0, 2, 4]])[1]   # m = 1: no visible bug
assert alias_trap(4, 1, [[3, 0, 8]])[0] == [[8]] * 4
print('edge cases ok')
