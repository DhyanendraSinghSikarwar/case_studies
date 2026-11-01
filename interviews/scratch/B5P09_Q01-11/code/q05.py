import random
import sys
from collections import Counter, deque

random.seed(5)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def islands(grid):
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    count = best = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1' and not seen[i][j]:
                count += 1
                seen[i][j] = True
                q = deque([(i, j)]); area = 0
                while q:                              # BFS: iterative, so no recursion limit
                    x, y = q.popleft(); area += 1
                    for dx, dy in D4:
                        a, b = x + dx, y + dy
                        if 0 <= a < m and 0 <= b < n and grid[a][b] == '1' and not seen[a][b]:
                            seen[a][b] = True        # mark on enqueue: each cell enters once
                            q.append((a, b))
                best = max(best, area)
    return [count, best]

def brute(grid):
    """Label propagation: every land cell repeatedly takes the smallest label among its land neighbours."""
    m, n = len(grid), len(grid[0])
    lab = {(i, j): (i, j) for i in range(m) for j in range(n) if grid[i][j] == '1'}
    changed = True
    while changed:
        changed = False
        for (i, j) in lab:
            for dx, dy in D4:
                p = (i + dx, j + dy)
                if p in lab and lab[p] < lab[(i, j)]:
                    lab[(i, j)] = lab[p]; changed = True
    c = Counter(lab.values())
    return [len(c), max(c.values()) if c else 0]

def recursive(grid):
    m, n = len(grid), len(grid[0]); seen = set()
    def go(x, y):
        seen.add((x, y))
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and grid[a][b] == '1' and (a, b) not in seen:
                go(a, b)
    go(0, 0)

assert islands(['11000', '11000', '00100', '00011']) == [3, 4]
assert islands(['000']) == [0, 0]
assert islands(['1']) == [1, 1]
assert islands(['101', '010', '101']) == [5, 1]          # diagonals do not connect
print('4 prompt examples ok')

for _ in range(1500):
    m, n = random.randint(1, 6), random.randint(1, 6); p = random.random()
    g = [''.join('1' if random.random() < p else '0' for _ in range(n)) for _ in range(m)]
    assert islands(g) == brute(g), g
print('1500 seeded random grids: BFS == label propagation')

# exhaustive: every 3x3 grid (512 of them)
for mask in range(512):
    g = [''.join('1' if mask >> (3 * i + j) & 1 else '0' for j in range(3)) for i in range(3)]
    assert islands(g) == brute(g)
print('exhaustive on all 512 3x3 grids: ok')

full = ['1' * 300] * 300
assert islands(full) == [1, 90000]
checker = [''.join('1' if (i + j) % 2 == 0 else '0' for j in range(300)) for i in range(300)]
assert islands(checker) == [45000, 1]
print('300x300 all land: [1, 90000]; checkerboard (no 4-neighbour touches): 45000 islands of size 1')

snake = []
for i in range(300):
    snake.append('1' * 300 if i % 2 == 0 else ('0' * 299 + '1' if (i // 2) % 2 == 0 else '1' + '0' * 299))
res = islands(snake)
print('serpentine grid:', res)
try:
    recursive(['1' * 300] * 300)
except RecursionError:
    print('recursive DFS on the 300x300 land block: RecursionError at limit', sys.getrecursionlimit())
