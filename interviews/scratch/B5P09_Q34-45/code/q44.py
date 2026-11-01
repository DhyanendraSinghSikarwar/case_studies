import random
import sys
from collections import deque

random.seed(44)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def shortest_bridge(grid):
    n = len(grid)
    start = next((i, j) for i in range(n) for j in range(n) if grid[i][j] == 1)
    # 1) iterative DFS (explicit stack) collects every cell of the first island
    island = {start}
    stack = [start]
    while stack:
        x, y = stack.pop()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and (a, b) not in island:
                island.add((a, b))
                stack.append((a, b))
    # 2) multi-source BFS from the whole island; level = number of water cells flipped so far
    q = deque((x, y, 0) for x, y in island)
    seen = set(island)
    while q:
        x, y, d = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and (a, b) not in seen:
                if grid[a][b] == 1:                   # touched the other island: d water cells were crossed
                    return d
                seen.add((a, b))
                q.append((a, b, d + 1))
    return -1

def components(grid):
    n = len(grid)
    comp = {}
    c = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and (i, j) not in comp:
                comp[(i, j)] = c
                st = [(i, j)]
                while st:
                    x, y = st.pop()
                    for dx, dy in D4:
                        a, b = x + dx, y + dy
                        if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and (a, b) not in comp:
                            comp[(a, b)] = c
                            st.append((a, b))
                c += 1
    return comp, c

def bridge_brute(grid):
    """Closest pair of land cells from different islands: Manhattan distance minus 1 water cells in between."""
    comp, c = components(grid)
    assert c == 2
    A = [p for p in comp if comp[p] == 0]
    B = [p for p in comp if comp[p] == 1]
    return min(abs(a[0] - b[0]) + abs(a[1] - b[1]) - 1 for a in A for b in B)

def first_island_recursive(grid):
    n = len(grid)
    start = next((i, j) for i in range(n) for j in range(n) if grid[i][j] == 1)
    seen = set()
    def go(x, y):
        seen.add((x, y))
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and (a, b) not in seen:
                go(a, b)
    go(*start)
    return seen

# ---- examples from the prompt
assert shortest_bridge([[0, 1], [1, 0]]) == 1
assert shortest_bridge([[0, 1, 0], [0, 0, 0], [0, 0, 1]]) == 2
assert shortest_bridge([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]) == 1
print('examples ok')

# ---- exhaustive: every 3 x 3 and 4 x 4 grid that has exactly two islands
tested = 0
for n in (3, 4):
    for mask in range(1 << (n * n)):
        g = [[mask >> (i * n + j) & 1 for j in range(n)] for i in range(n)]
        if components(g)[1] == 2:
            assert shortest_bridge(g) == bridge_brute(g), g
            tested += 1
print('exhaustive:', tested, 'grids with exactly two islands (n = 3, 4): BFS answer == closest-pair answer')

# ---- seeded random 5-8 grids with exactly two islands
N = 400
done = 0
while done < N:
    n = random.randint(5, 8)
    g = [[1 if random.random() < 0.3 else 0 for _ in range(n)] for _ in range(n)]
    if components(g)[1] == 2:
        assert shortest_bridge(g) == bridge_brute(g), g
        done += 1
print('random check on', N, 'seeded grids with exactly two islands ok')

# ---- max size n = 100: one snake-shaped island of about 5000 cells plus a single cell
n = 100
g = [[0] * n for _ in range(n)]
for r in range(0, n, 2):
    for c in range(0, 98):
        g[r][c] = 1                                   # even rows: long horizontal bars
for r in range(1, n, 2):
    g[r][97 if (r // 2) % 2 == 0 else 0] = 1          # odd rows: one connector, alternating ends
g[50][99] = 1                                         # the second island: one cell, one water cell (50, 98) away
comp, c = components(g)
assert c == 2
snake = sum(v == 0 for v in comp.values())
print('snake island cells:', snake, '| islands:', c)
print('bridge on the snake grid:', shortest_bridge(g), '| closest-pair check:', bridge_brute(g))
assert shortest_bridge(g) == bridge_brute(g) == 1
print('recursion limit:', sys.getrecursionlimit())
try:
    first_island_recursive(g)
except RecursionError:
    print('recursive DFS over the snake island: RecursionError (the island has', snake, 'cells in one long path)')

# ---- edge cases
assert shortest_bridge([[1, 0], [0, 1]]) == 1                    # diagonal cells are different islands
assert shortest_bridge([[1, 1, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == 1
big = [[0] * 100 for _ in range(100)]
big[0][0] = 1
big[99][99] = 1
assert shortest_bridge(big) == 197                              # opposite corners: 198 steps, 197 water cells
print('edge cases ok')
