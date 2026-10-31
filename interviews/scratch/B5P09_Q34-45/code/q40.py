import heapq
import random
from collections import deque

random.seed(40)
INF = float('inf')

def dag_shortest(n, edges, src):
    """Kahn topological order over the WHOLE graph, then relax out-edges in that order. O(V + E)."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, w in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    assert len(order) == n                      # the prompt guarantees a DAG
    dist = [INF] * n
    dist[src] = 0
    for u in order:
        if dist[u] == INF:                      # not reachable from src: its edges must not be relaxed
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return [None if x == INF else x for x in dist]

def bellman_ford(n, edges, src):
    """Brute force / reference: up to n - 1 passes over all edges, O(V * E)."""
    dist = [INF] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return [None if x == INF else x for x in dist]

def dijkstra_finalise(n, edges, src):
    """Finalise-on-first-pop Dijkstra (wrong with negative edges)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    h = [(0, src)]
    done = set()
    while h:
        d, u = heapq.heappop(h)
        if u in done:
            continue
        done.add(u)
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
    return [None if x == INF else x for x in dist]

# ---- examples from the prompt
E1 = [[0, 1, 2], [0, 2, 6], [1, 2, -3], [2, 3, 1], [1, 3, 4]]
assert dag_shortest(5, E1, 0) == [0, 2, -1, 0, None]
assert dag_shortest(3, [[1, 2, -5]], 0) == [0, None, None]
assert dag_shortest(1, [], 0) == [0]
print('examples ok')

# ---- Dijkstra fails: node 1 is popped and finalised at 4, then 0 -> 2 -> 1 (5 - 3 = 2) is found too late
E2 = [[0, 1, 4], [0, 2, 5], [2, 1, -3]]
print('DAG answer  :', dag_shortest(3, E2, 0))
print('Dijkstra    :', dijkstra_finalise(3, E2, 0))
assert dag_shortest(3, E2, 0) == [0, 2, 5] and dijkstra_finalise(3, E2, 0) == [0, 4, 5]

def random_dag(n, m, lo, hi):
    perm = list(range(n))
    random.shuffle(perm)                        # hidden topological order, labels are shuffled
    es = []
    for _ in range(m):
        if n < 2:
            break
        a, b = sorted(random.sample(range(n), 2))
        es.append([perm[a], perm[b], random.randint(lo, hi)])
    return es

# ---- seeded cross-check against Bellman-Ford (repeats, unreachable nodes, negative weights)
N = 1500
dij_wrong = 0
for _ in range(N):
    n = random.randint(1, 9)
    es = random_dag(n, random.randint(0, 16), -5, 5)
    s = random.randrange(n)
    a = dag_shortest(n, es, s)
    assert a == bellman_ford(n, es, s), (n, es, s)
    dij_wrong += dijkstra_finalise(n, es, s) != a
print('cross-check on', N, 'seeded DAGs: topological relaxation == Bellman-Ford;',
      'finalise-on-pop Dijkstra wrong on', dij_wrong)
assert dij_wrong > 0

# ---- edge cases
assert dag_shortest(4, [[2, 3, -1], [1, 2, -1]], 1) == [None, 0, -1, -2]      # source in the middle, earlier nodes unreachable
assert dag_shortest(3, [[0, 1, 5], [0, 1, -2], [0, 1, 7]], 0) == [0, -2, None]  # repeats: smallest wins
assert dag_shortest(2, [[0, 1, -100]], 1) == [None, 0]                          # edge leaving an unreachable node
# max size: 10^5 nodes, 2 * 10^5 edges, weights -100..100 (iterative, no recursion anywhere)
n, m = 100000, 200000
perm = list(range(n))
random.shuffle(perm)
big = [[perm[i], perm[i + 1], random.randint(-100, 100)] for i in range(n - 1)]      # a spine so everything is reachable
for _ in range(m - (n - 1)):
    a, b = sorted(random.sample(range(n), 2))
    big.append([perm[a], perm[b], random.randint(-100, 100)])
assert len(big) == m
d = dag_shortest(n, big, perm[0])
reach = sum(x is not None for x in d)
print('max size: reachable', reach, 'of', n, '| min distance', min(x for x in d if x is not None))
print('edge cases ok')
