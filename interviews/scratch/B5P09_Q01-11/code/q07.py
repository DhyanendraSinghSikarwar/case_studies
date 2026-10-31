import random
from collections import deque

random.seed(7)
INF = float('inf')

def bfs_dist(n, edges, src, directed):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    dist = [-1] * n
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:               # first arrival is the shortest; -1 doubles as "unseen"
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def brute(n, edges, src, directed):
    """Bellman-Ford with unit weights: relax every edge n times."""
    d = [INF] * n; d[src] = 0
    for _ in range(n):
        for u, v in edges:
            if d[u] + 1 < d[v]: d[v] = d[u] + 1
            if not directed and d[v] + 1 < d[u]: d[u] = d[v] + 1
    return [-1 if x == INF else x for x in d]

assert bfs_dist(5, [[0, 1], [1, 2], [0, 3], [3, 2]], 0, True) == [0, 1, 2, 1, -1]
assert bfs_dist(4, [[1, 2], [2, 3]], 3, False) == [-1, 2, 1, 0]
assert bfs_dist(3, [], 1, False) == [-1, 0, -1]
print('3 prompt examples ok')

for _ in range(1000):
    n = random.randint(1, 8); d = random.random() < .5
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (d or u < v)]
    random.shuffle(pairs)
    e = [list(p) for p in pairs[:random.randint(0, min(10, len(pairs)))]]
    s = random.randrange(n)
    assert bfs_dist(n, e, s, d) == brute(n, e, s, d), (n, e, s, d)
print('1000 seeded random graphs: BFS == Bellman-Ford with unit weights')

# the level property: each edge u->v satisfies dist[v] <= dist[u] + 1 whenever u is reachable
n = 2000
e = [[random.randrange(n), random.randrange(n)] for _ in range(4000)]
e = [x for x in e if x[0] != x[1]]
dist = bfs_dist(n, e, 0, True)
assert all(dist[v] != -1 and dist[v] <= dist[u] + 1 for u, v in e if dist[u] != -1)
print('random directed graph n=2000: edge property dist[v] <= dist[u] + 1 holds for every edge out of a reached node')

N = 10 ** 5
path = [[i, i + 1] for i in range(N - 1)]
assert bfs_dist(N, path, 0, False)[-1] == N - 1 and bfs_dist(N, path, N - 1, True)[0] == -1
print('path of 10^5 nodes: far end at distance', N - 1, '; directed against the arrows: unreachable (-1)')

# why it fails with weights: BFS counts edges, not cost
w_edges = [(0, 1, 10), (0, 2, 1), (2, 1, 1)]          # 0->1 costs 10 directly, 2 via node 2
hops = bfs_dist(3, [[u, v] for u, v, _ in w_edges], 0, True)
cost = [0, INF, INF]
for _ in range(3):
    for u, v, w in w_edges:
        cost[v] = min(cost[v], cost[u] + w)
print('hop counts (BFS):', hops, '| cheapest costs:', cost, '-> BFS says node 1 is 1 hop but the best cost is 2, not 10')
