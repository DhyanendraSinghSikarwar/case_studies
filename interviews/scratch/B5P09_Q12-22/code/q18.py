import itertools, random
from collections import deque
random.seed(18)
INF = float('inf')
D8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]

def shortest_path(grid, stats=None):         # BFS, mark when enqueued
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    seen = [[False] * n for _ in range(n)]
    seen[0][0] = True
    q = deque([(0, 0, 1)])
    peak = 1
    while q:
        x, y, d = q.popleft()
        if x == n - 1 and y == n - 1:
            if stats is not None: stats['peak'] = peak
            return d
        for dx, dy in D8:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and not seen[a][b]:
                seen[a][b] = True            # marking here means each cell enters the queue once
                q.append((a, b, d + 1))
        peak = max(peak, len(q))
    if stats is not None: stats['peak'] = peak
    return -1

def mark_on_dequeue(grid):                   # same answer, but the queue can hold a cell many times
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1, 0
    seen = set()
    q = deque([(0, 0, 1)])
    peak = 1
    while q:
        x, y, d = q.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if x == n - 1 and y == n - 1:
            return d, peak
        for dx, dy in D8:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and (a, b) not in seen:
                q.append((a, b, d + 1))
        peak = max(peak, len(q))
    return -1, peak

def brute(grid):                             # relax all cells until nothing changes (Bellman-Ford style)
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    d = {(i, j): INF for i in range(n) for j in range(n) if not grid[i][j]}
    d[(0, 0)] = 1
    changed = True
    while changed:
        changed = False
        for (x, y), v in list(d.items()):
            for dx, dy in D8:
                p = (x + dx, y + dy)
                if p in d and v + 1 < d[p]:
                    d[p] = v + 1; changed = True
    r = d[(n - 1, n - 1)]
    return -1 if r == INF else r

assert shortest_path([[0, 1], [1, 0]]) == 2
assert shortest_path([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
assert shortest_path([[1, 0], [0, 0]]) == -1
assert shortest_path([[0]]) == 1
print("examples ok: 2 4 -1 1")

cnt = 0
for n in (1, 2, 3, 4):
    for bits in itertools.product((0, 1), repeat=n * n):
        g = [list(bits[i * n:(i + 1) * n]) for i in range(n)]
        r = shortest_path(g)
        assert r == brute(g) == mark_on_dequeue(g)[0], g
        cnt += 1
print("exhaustive: all %d grids with n <= 4 agree (BFS, relaxation brute, mark-on-dequeue)" % cnt)

for _ in range(300):
    n = random.randint(5, 9)
    g = [[1 if random.random() < .3 else 0 for _ in range(n)] for _ in range(n)]
    assert shortest_path(g) == brute(g)
print("300 random n=5..9 grids ok")

# why mark on enqueue: peak queue size on an open 100 x 100 grid
n = 100
open_grid = [[0] * n for _ in range(n)]
s1 = {}
r1 = shortest_path(open_grid, s1)
r2, peak2 = mark_on_dequeue(open_grid)
assert r1 == r2 == n
print("open 100x100: answer", r1, "| peak queue, mark on enqueue:", s1['peak'], "| mark on dequeue:", peak2, "| cells:", n * n)
assert s1['peak'] <= n * n
