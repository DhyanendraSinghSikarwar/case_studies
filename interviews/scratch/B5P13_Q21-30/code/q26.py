import collections
import itertools
import random

random.seed(2601)

def life(board, generations):
    m, n = len(board), len(board[0])
    for _ in range(generations):
        for i in range(m):
            for j in range(n):
                live = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n:
                            live += board[i + di][j + dj] & 1          # bit 0 = OLD state
                if live == 3 or (board[i][j] & 1 and live == 2):
                    board[i][j] |= 2                                   # bit 1 = NEW state
        for i in range(m):
            for j in range(n):
                board[i][j] >>= 1                                      # new becomes current
    return board

def counter_version(board, generations):
    m, n = len(board), len(board[0])
    cells = {(i, j) for i in range(m) for j in range(n) if board[i][j]}
    for _ in range(generations):
        cnt = collections.Counter((i + di, j + dj) for i, j in cells
                                  for di in (-1, 0, 1) for dj in (-1, 0, 1) if di or dj)
        cells = {p for p, c in cnt.items() if 0 <= p[0] < m and 0 <= p[1] < n and (c == 3 or (c == 2 and p in cells))}
    return [[1 if (i, j) in cells else 0 for j in range(n)] for i in range(m)]

def buggy_single_pass(board):
    """Overwrite in place with no encoding: later cells see already-updated neighbours."""
    m, n = len(board), len(board[0])
    for i in range(m):
        for j in range(n):
            live = sum(board[i + di][j + dj] for di in (-1, 0, 1) for dj in (-1, 0, 1)
                       if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n)
            board[i][j] = 1 if live == 3 or (board[i][j] and live == 2) else 0
    return board

def cp(x): return [r[:] for r in x]

examples = [([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]], 1, [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]),
            ([[1, 1], [1, 0]], 1, [[1, 1], [1, 1]]),
            ([[0, 0, 0], [1, 1, 1], [0, 0, 0]], 2, [[0, 0, 0], [1, 1, 1], [0, 0, 0]])]
for b, g, want in examples:
    a = cp(b); r = life(a, g)
    assert r is a and a == want == counter_version(b, g)
    print(b, 'x', g, '->', a)

# dry run on the first example: encoded board after the marking pass of generation 1
b = cp(examples[0][0]); m, n = 4, 3
for i in range(m):
    for j in range(n):
        live = sum(b[i + di][j + dj] & 1 for di in (-1, 0, 1) for dj in (-1, 0, 1)
                   if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n)
        if live == 3 or (b[i][j] & 1 and live == 2): b[i][j] |= 2
print('encoded (value = old + 2*new):', b)
print('after >> 1                   :', [[v >> 1 for v in r] for r in b])

# seeded random cross-check
for _ in range(1500):
    m, n = random.randint(1, 7), random.randint(1, 7)
    b = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    g = random.randint(1, 6)
    assert life(cp(b), g) == counter_version(b, g)
print('random cross-check ok: 1500 cases')

# exhaustive: every 3 x 3 board, 1 and 2 generations; every 2 x 4 board, 1 generation
count = 0
for cells in itertools.product((0, 1), repeat=9):
    b = [list(cells[:3]), list(cells[3:6]), list(cells[6:])]
    for g in (1, 2):
        assert life(cp(b), g) == counter_version(b, g); count += 1
for cells in itertools.product((0, 1), repeat=8):
    b = [list(cells[:4]), list(cells[4:])]
    assert life(cp(b), 1) == counter_version(b, 1); count += 1
print('exhaustive ok:', count, 'cases')

# the single-pass bug: how many of the 512 3x3 boards go wrong, and one example
wrong = 0; ex = None
for cells in itertools.product((0, 1), repeat=9):
    b = [list(cells[:3]), list(cells[3:6]), list(cells[6:])]
    if buggy_single_pass(cp(b)) != counter_version(b, 1):
        wrong += 1
        ex = ex or b
print('single-pass overwrite wrong on', wrong, 'of 512 3x3 boards; first:', ex)
print('  buggy:', buggy_single_pass(cp(ex)), ' right:', counter_version(ex, 1))
assert wrong > 0

# unbounded board: the live region grows. A glider on an infinite plane moves (1,1) every 4 generations.
def step_inf(cells):
    cnt = collections.Counter((i + di, j + dj) for i, j in cells for di in (-1, 0, 1) for dj in (-1, 0, 1) if di or dj)
    return {p for p, c in cnt.items() if c == 3 or (c == 2 and p in cells)}
glider = {(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
g = glider
for _ in range(4): g = step_inf(g)
assert g == {(i + 1, j + 1) for i, j in glider}
print('glider after 4 generations on an unbounded board is shifted by (1, 1): True')
# on a bounded 4x4 board the same glider hits the wall instead
b = [[0] * 4 for _ in range(4)]
for i, j in glider: b[i][j] = 1
print('bounded 4x4 glider after 8 generations:', life(b, 8))

# edge asserts and max size
assert life([[1]], 1) == [[0]] and life([[0]], 3) == [[0]]
assert life([[1, 1], [1, 1]], 10) == [[1, 1], [1, 1]]          # block is stable
big = [[random.randint(0, 1) for _ in range(30)] for _ in range(30)]
assert life(cp(big), 10) == counter_version(big, 10)
print('edge asserts ok')
