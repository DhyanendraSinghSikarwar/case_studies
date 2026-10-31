import heapq
import itertools
import random
from collections import deque

random.seed(27)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
INF = float('inf')

def min_obstacles(grid, check_invariant=False):
    """0-1 BFS: relax like Dijkstra, but a 0-cost move goes to the FRONT of the deque and a 1-cost move to the BACK."""
    m, n = len(grid), len(grid[0])
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0
    dq = deque([(0, 0)])
    while dq:
        if check_invariant:                                  # deque distances are non-decreasing and span at most two values
            ds = [dist[x][y] for x, y in dq]
            assert ds == sorted(ds) and ds[-1] - ds[0] <= 1, ds
        x, y = dq.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n:
                w = grid[a][b]                               # cost of stepping INTO (a, b)
                if dist[x][y] + w < dist[a][b]:              # strict: a cell can be re-queued when a cheaper route appears
                    dist[a][b] = dist[x][y] + w
                    if w:
                        dq.append((a, b))
                    else:
                        dq.appendleft((a, b))
    return dist[m - 1][n - 1]

def dijkstra_obstacles(grid):
    m, n = len(grid), len(grid[0])
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0
    h = [(0, 0, 0)]
    while h:
        d, x, y = heapq.heappop(h)
        if d > dist[x][y]:
            continue
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and d + grid[a][b] < dist[a][b]:
                dist[a][b] = d + grid[a][b]
                heapq.heappush(h, (dist[a][b], a, b))
    return dist[m - 1][n - 1]

def fixpoint_brute(grid):
    """Independent brute force: keep relaxing every cell pair until nothing changes (Bellman-Ford over the grid)."""
    m, n = len(grid), len(grid[0])
    d = [[INF] * n for _ in range(m)]
    d[0][0] = 0
    changed = True
    while changed:
        changed = False
        for x in range(m):
            for y in range(n):
                for dx, dy in D4:
                    a, b = x + dx, y + dy
                    if 0 <= a < m and 0 <= b < n and d[x][y] + grid[a][b] < d[a][b]:
                        d[a][b] = d[x][y] + grid[a][b]
                        changed = True
    return d[m - 1][n - 1]

def plain_bfs_wrong(grid):
    """The tempting bug: ordinary BFS, a cell is finalised the first time it is enqueued, obstacle cost added on the way."""
    m, n = len(grid), len(grid[0])
    dist = {(0, 0): 0}
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + grid[a][b]
                q.append((a, b))
    return dist[(m - 1, n - 1)]

for g, want in [([[0, 1, 1], [1, 1, 0], [1, 1, 0]], 2), ([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0), ([[0]], 0)]:
    got = min_obstacles(g, check_invariant=True)
    assert got == want == dijkstra_obstacles(g) == fixpoint_brute(g), (g, got, want)
    print(g, '->', got, '| plain BFS says', plain_bfs_wrong(g))

# ---- exhaustive over every grid with free corners: 2x3, 3x3, 3x4, 4x4
total = bad_bfs = 0
for m, n in [(1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]:
    inner = [(i, j) for i in range(m) for j in range(n) if (i, j) not in ((0, 0), (m - 1, n - 1))]
    for bits in itertools.product((0, 1), repeat=len(inner)):
        g = [[0] * n for _ in range(m)]
        for (i, j), b in zip(inner, bits):
            g[i][j] = b
        r = min_obstacles(g, check_invariant=True)
        assert r == dijkstra_obstacles(g) == fixpoint_brute(g), g
        total += 1
        bad_bfs += plain_bfs_wrong(g) != r
print('exhaustive on', total, 'grids: 0-1 BFS == Dijkstra == fixpoint, deque stays sorted with span <= 1')
print('plain visited-on-enqueue BFS is wrong on', bad_bfs, 'of those grids')

# ---- seeded random cross-check on bigger grids
for _ in range(300):
    m, n = random.randint(1, 8), random.randint(1, 8)
    g = [[int(random.random() < 0.45) for _ in range(n)] for _ in range(m)]
    g[0][0] = 0
    g[m - 1][n - 1] = 0
    assert min_obstacles(g) == dijkstra_obstacles(g) == fixpoint_brute(g), g
print('300 seeded random grids up to 8x8 agree')

# ---- sizes: m*n = 10^5 (a single row, a single column, 316x316), iterative so no recursion limit
row = [[0] + [1] * (10 ** 5 - 2) + [0]]
assert min_obstacles(row) == 10 ** 5 - 2
col = [[v] for v in row[0]]
assert min_obstacles(col) == 10 ** 5 - 2
big = [[int(random.random() < 0.4) for _ in range(316)] for _ in range(316)]
big[0][0] = big[315][315] = 0
assert min_obstacles(big) == dijkstra_obstacles(big)
print('10^5-cell row and column ->', min_obstacles(row), '; 316x316 random ->', min_obstacles(big))
