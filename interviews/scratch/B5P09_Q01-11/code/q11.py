import random
from collections import deque

random.seed(11)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def rotting(grid):
    m, n = len(grid), len(grid[0])
    g = [row[:] for row in grid]
    q = deque(); fresh = 0
    for i in range(m):
        for j in range(n):
            if g[i][j] == 2: q.append((i, j))      # ALL rotten oranges are seeds at time 0
            elif g[i][j] == 1: fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):                    # one full level = one minute
            x, y = q.popleft()
            for dx, dy in D4:
                a, b = x + dx, y + dy
                if 0 <= a < m and 0 <= b < n and g[a][b] == 1:
                    g[a][b] = 2; fresh -= 1; q.append((a, b))
        minutes += 1
    return -1 if fresh else minutes

def brute(grid):
    """Simulate minute by minute on a copy until nothing changes."""
    m, n = len(grid), len(grid[0]); g = [row[:] for row in grid]; t = 0
    while True:
        new = [row[:] for row in g]; changed = False
        for i in range(m):
            for j in range(n):
                if g[i][j] == 1 and any(0 <= i + dx < m and 0 <= j + dy < n and g[i + dx][j + dy] == 2 for dx, dy in D4):
                    new[i][j] = 2; changed = True
        if not changed: break
        g = new; t += 1
    return -1 if any(1 in row for row in g) else t

def one_source_at_a_time(grid):
    """Wrong idea: BFS from the first rotten orange only."""
    m, n = len(grid), len(grid[0])
    src = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 2]
    if not src: return 0 if not any(1 in r for r in grid) else -1
    dist = {src[0]: 0}; q = deque([src[0]])
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and grid[a][b] != 0 and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + 1; q.append((a, b))
    fresh = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 1]
    if any(p not in dist for p in fresh): return -1
    return max((dist[p] for p in fresh), default=0)

assert rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert rotting([[0, 2]]) == 0
assert rotting([[1]]) == -1
print('4 prompt examples ok')

for _ in range(2000):
    m, n = random.randint(1, 5), random.randint(1, 5)
    g = [[random.choice([0, 1, 1, 2]) for _ in range(n)] for _ in range(m)]
    snap = [r[:] for r in g]
    assert rotting(g) == brute(g), g
    assert g == snap
print('2000 seeded random grids: multi-source BFS == minute-by-minute simulation; input untouched')

for mask in range(3 ** 6):                         # every 2x3 grid over {0,1,2}
    cells = [(mask // 3 ** k) % 3 for k in range(6)]
    g = [cells[:3], cells[3:]]
    assert rotting(g) == brute(g)
print('exhaustive on all 729 2x3 grids: ok')

bad = [[2, 1, 1, 1, 2]]
print('grid [[2,1,1,1,2]]: correct', rotting(bad), '| single-source (first rotten only)', one_source_at_a_time(bad))
wrong = 0
for _ in range(2000):
    g = [[random.choice([0, 1, 1, 2]) for _ in range(5)] for _ in range(4)]
    wrong += one_source_at_a_time(g) != rotting(g)
print('single-source BFS wrong on', wrong, 'of 2000 seeded 4x5 grids')

assert rotting([[1, 1], [1, 1]]) == -1             # fresh but no rotten at all
assert rotting([[0, 0]]) == 0 and rotting([[2]]) == 0
big = [[1] * 100 for _ in range(100)]; big[0][0] = 2
assert rotting(big) == 198                          # farthest cell is 99 + 99 steps away
print('100x100 with one rotten corner: 198 minutes (Manhattan distance to the opposite corner)')
