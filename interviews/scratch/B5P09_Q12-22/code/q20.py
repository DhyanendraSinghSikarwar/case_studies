import itertools, random
from collections import deque
random.seed(20)
INF = 2147483647
D4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def walls_and_gates(rooms):
    m, n = len(rooms), len(rooms[0])
    g = [row[:] for row in rooms]              # new grid, input untouched
    q = deque((i, j) for i in range(m) for j in range(n) if g[i][j] == 0)   # ALL gates start together
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and g[a][b] == INF:   # INF doubles as "unvisited"
                g[a][b] = g[x][y] + 1
                q.append((a, b))
    return g

def brute(rooms, work=None):                   # one BFS per empty room, stop at the nearest gate
    m, n = len(rooms), len(rooms[0])
    g = [row[:] for row in rooms]
    for i in range(m):
        for j in range(n):
            if rooms[i][j] != INF:
                continue
            dist = {(i, j): 0}
            q = deque([(i, j)])
            found = INF
            while q:
                x, y = q.popleft()
                if work is not None: work[0] += 1
                if rooms[x][y] == 0:
                    found = dist[(x, y)]
                    break
                for dx, dy in D4:
                    a, b = x + dx, y + dy
                    if 0 <= a < m and 0 <= b < n and rooms[a][b] != -1 and (a, b) not in dist:
                        dist[(a, b)] = dist[(x, y)] + 1
                        q.append((a, b))
            g[i][j] = found
    return g

ex1 = [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]
assert walls_and_gates(ex1) == [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
assert walls_and_gates([[INF]]) == [[INF]]
assert walls_and_gates([[0, -1, INF]]) == [[0, -1, INF]]
print("examples ok")

cnt = 0
for m, n in ((1, 1), (1, 4), (2, 3), (3, 3)):
    for cells in itertools.product((-1, 0, INF), repeat=m * n):
        g = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
        snap = [r[:] for r in g]
        assert walls_and_gates(g) == brute(g)
        assert g == snap                         # input not modified
        cnt += 1
print("exhaustive: all %d grids of sizes 1x1, 1x4, 2x3, 3x3 agree with one-BFS-per-room" % cnt)

for _ in range(300):
    m, n = random.randint(1, 7), random.randint(1, 7)
    g = [[random.choice([-1, 0, INF, INF]) for _ in range(n)] for _ in range(m)]
    assert walls_and_gates(g) == brute(g)
print("300 random grids up to 7x7 agree")

# work comparison on a 30 x 30 grid with one gate in a corner (BFS pops counted)
m = n = 30
g = [[INF] * n for _ in range(m)]; g[0][0] = 0
w = [0]; brute(g, w)
q = deque([(0, 0)]); popped = 0; seen = {(0, 0)}
while q:
    x, y = q.popleft(); popped += 1
    for dx, dy in D4:
        a, b = x + dx, y + dy
        if 0 <= a < m and 0 <= b < n and (a, b) not in seen: seen.add((a, b)); q.append((a, b))
print("30x30, one gate in a corner: multi-source pops = %d, per-room BFS pops = %d (cells = %d)" % (popped, w[0], m * n))
assert popped == m * n and w[0] > 100 * popped

# full size
m = n = 100
g = [[random.choice([-1, 0, INF, INF, INF, INF]) for _ in range(n)] for _ in range(m)]
r = walls_and_gates(g)
print("100x100 random grid: max finite distance", max(v for row in r for v in row if v != INF), "| unreachable rooms", sum(v == INF for row in r for v in row))
