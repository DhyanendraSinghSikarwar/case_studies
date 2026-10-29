### Q26 ⭐⭐ 🟡 Conway's Game of Life in place. `board` is an m x n list of lists of 0 (dead) and 1 (live), 1 <= m, n <= 30, and `generations` is an integer with 1 <= generations <= 10. Advance the board that many generations simultaneously (all cells change at once) and return the final board; modify `board` in place and return it. Each cell has up to 8 neighbours (cells beyond the border count as dead); a live cell with 2 or 3 live neighbours survives, a dead cell with exactly 3 live neighbours becomes live, every other cell is dead in the next generation. Use O(1) extra space per generation by encoding each cell in two bits (bit 0 = current state, bit 1 = next state, so you can still read the old state of cells you already updated), then shift every cell right by one. Explain why overwriting cells in a single pass without such an encoding gives wrong answers (later cells would see updated neighbours), and say what changes on an unbounded board (the live region can grow, so you would store live cells in a set). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a copy-based version that counts neighbours of live cells in a Counter on small inputs. Example: board=[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]], generations=1 -> [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]; board=[[1, 1], [1, 0]], generations=1 -> [[1, 1], [1, 1]]; board=[[0, 0, 0], [1, 1, 1], [0, 0, 0]], generations=2 -> [[0, 0, 0], [1, 1, 1], [0, 0, 0]].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** Simultaneous in-place update by encoding old and new state in one cell (two bits).

**Say this first (1 line):** "Bit 0 is the old state, bit 1 is the new state; count neighbours with `& 1`, write the new state with `|= 2`, and shift everything right by one at the end."

**Brute force:** Copy the board, compute the next board from the copy. O(m * n) time and O(m * n) space per generation. A second oracle keeps only the live cells and counts neighbours of live cells in a `Counter`: O(live cells) per generation, and it is easy to extend to an unbounded board.

**Optimal:**
- A cell holds 0 to 3. `value & 1` is the state in the current generation, `value >> 1` the state in the next.
- For each cell count live neighbours with `board[x][y] & 1` (the old state, even for cells already marked). If `live == 3`, or the cell is alive and `live == 2`, do `board[i][j] |= 2`.
- After the whole board is marked, do `board[i][j] >>= 1` for every cell. Dead-to-dead (0) and live-to-dead (1) both become 0, dead-to-live (2) and live-to-live (3) become 1.
- Repeat for each generation.
- Why a single pass without encoding fails: when you write the new value of a cell, the cells after it (to the right and below) read that new value as a neighbour. Those cells then count the wrong number of live neighbours. The program counts it: the plain overwrite is wrong on 417 of the 512 3 x 3 boards, for example `[[0,0,0],[0,0,0],[1,1,1]]` (it returns `[[0,0,0],[0,1,1],[1,0,1]]`, right is `[[0,0,0],[0,1,0],[0,1,0]]`).
- Unbounded board: the live region can grow, so a fixed array does not work. Store the live cells in a set and count neighbours in a `Counter`, as the oracle does. A glider moves one cell diagonally every 4 generations (checked in the program); on the bounded 4 x 4 board it crashes into the wall and ends as a 2 x 2 block.

**Complexity:** Per generation O(m * n * 8) = O(m * n) time, O(1) extra space. For `g` generations O(g * m * n); the maximum is 10 * 30 * 30 = 9000 cell updates, each looking at 8 neighbours.

**Dry run:** First example, 4 x 3. Encoded after marking: `[[0,1,0],[2,0,3],[1,3,3],[0,2,0]]`. Cell (1,2): old 1 with three live neighbours ((0,1), (2,1), (2,2)), so it survives, and the `3` is old 1 plus new 1. Cell (0,1): old 1, only one live neighbour, so it dies (stays `1`, new bit 0). After `>> 1`: `[[0,0,0],[1,0,1],[0,1,1],[0,1,0]]`, which matches.

**Code:**
```python
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
```

**Output (my run):**
```
[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]] x 1 -> [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
[[1, 1], [1, 0]] x 1 -> [[1, 1], [1, 1]]
[[0, 0, 0], [1, 1, 1], [0, 0, 0]] x 2 -> [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
encoded (value = old + 2*new): [[0, 1, 0], [2, 0, 3], [1, 3, 3], [0, 2, 0]]
after >> 1                   : [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
random cross-check ok: 1500 cases
exhaustive ok: 1280 cases
single-pass overwrite wrong on 417 of 512 3x3 boards; first: [[0, 0, 0], [0, 0, 0], [1, 1, 1]]
  buggy: [[0, 0, 0], [0, 1, 1], [1, 0, 1]]  right: [[0, 0, 0], [0, 1, 0], [0, 1, 0]]
glider after 4 generations on an unbounded board is shifted by (1, 1): True
bounded 4x4 glider after 8 generations: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
edge asserts ok
```

**Edge cases:**
- Border cells have fewer than 8 neighbours; cells beyond the border count as dead.
- 1 x 1 board: a live cell has 0 neighbours and dies.
- A 2 x 2 block of live cells is stable (10 generations leave it unchanged).
- Oscillators like the blinker return to start after 2 generations (example 3).
- 30 x 30 random board with 10 generations matches the Counter version.

**Follow-ups:**
- *Other encodings?* Use `-1` for live-to-dead and `2` for dead-to-live, then convert at the end. Same idea.
- *Very sparse infinite board?* The set-based version, O(live cells) per generation.
- *Toroidal board?* Use modulo indexes for the neighbours.

**Common mistakes:**
- Reading `board[x][y]` instead of `board[x][y] & 1` for neighbours (the new bit makes the count wrong).
- Shifting inside the cell loop instead of after the whole board is marked.
- Applying the rule to dead cells as "survive with 2 or 3".
- Forgetting that the shift must happen once per generation, not once in total.
