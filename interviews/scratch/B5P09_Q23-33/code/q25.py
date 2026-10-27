import heapq
import itertools
import random

random.seed(25)
INF = float('inf')

def dijkstra_lazy(n, edges, src):
    """Lazy deletion: push duplicates, skip a popped entry whose distance is worse than the best known."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    heap = [(0, src)]
    pushes, stale = 1, 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                       # a better entry for u was already processed
            stale += 1
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:               # strict: equal distance does not push
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
                pushes += 1
    return [[None if x == INF else x for x in dist], pushes, stale]

def bellman_ford_dist(n, edges, src):
    """Independent checker for the distances only (weights are >= 0 so no negative cycles)."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return [None if x == INF else x for x in d]

examples = [
    (4, [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]], 0, [[0, 3, 1, 4], 5, 1]),
    (3, [[0, 1, 1]], 2, [[None, None, 0], 1, 0]),
    (3, [[0, 1, 5], [0, 2, 5], [1, 2, 0], [2, 1, 0]], 0, [[0, 5, 5], 3, 0]),
]
for n, e, s, want in examples:
    got = dijkstra_lazy(n, e, s)
    assert got == want, (got, want)
    print(n, e, 'src', s, '->', got)

# ---- why (distance, node) tuples never raise TypeError: ints always compare, and equal pairs are fully equal
heap = []
for item in [(3, 1), (3, 1), (3, 0), (2, 5)]:
    heapq.heappush(heap, item)
print('tied distances pop in node order:', [heapq.heappop(heap) for _ in range(4)])
class Payload:                               # what goes wrong if you push objects (Part 8 Q29)
    pass
h = [(1, Payload())]
try:
    heapq.heappush(h, (1, Payload()))
except TypeError as err:
    print('(dist, object) with tied dist ->', err)

# ---- exhaustive: every multigraph on 3 nodes with up to 3 edges, weights 0..2, every source
opts = [(u, v, w) for u in range(3) for v in range(3) for w in range(3)]     # 27 possible edges (self loops included)
cnt = 0
for k in range(4):
    for combo in itertools.product(opts, repeat=k):                           # ordered, so repeats and input orders are covered
        edges = [list(x) for x in combo]
        for src in range(3):
            dist, pushes, stale = dijkstra_lazy(3, edges, src)
            reached = sum(x is not None for x in dist)
            assert dist == bellman_ford_dist(3, edges, src)
            assert pushes <= len(edges) + 1
            assert stale == pushes - reached
            cnt += 1
print('exhaustive on', cnt, '(graph, source) cases: distances right, pushes <= E + 1, stale == pushes - reached')

# ---- seeded random bigger graphs
for _ in range(500):
    n = random.randint(1, 12)
    edges = [[random.randrange(n), random.randrange(n), random.randint(0, 6)] for _ in range(random.randint(0, 40))]
    src = random.randrange(n)
    dist, pushes, stale = dijkstra_lazy(n, edges, src)
    reached = sum(x is not None for x in dist)
    assert dist == bellman_ford_dist(n, edges, src) and pushes <= len(edges) + 1 and stale == pushes - reached
print('500 seeded random graphs agree')

# ---- the stale check saves work: count edge scans with and without it on a graph with many improvable nodes
def scans(n, edges, src, skip_stale):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    heap, work = [(0, src)], 0
    while heap:
        d, u = heapq.heappop(heap)
        if skip_stale and d > dist[u]:
            continue
        for v, w in adj[u]:
            work += 1
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return work
# layer graph: node i reaches every later node; the first path found is the worst, later ones improve it
m = 60
edges = [[i, j, (j - i) ** 2] for i in range(m) for j in range(i + 1, m)]
edges.sort(key=lambda e: -e[2])
print('edge scans, 60-node graph: with stale check', scans(m, edges, 0, True), '| without', scans(m, edges, 0, False))

# ---- edge case and size: n=1; n = 10^5, E = 2*10^5 with repeated edges
assert dijkstra_lazy(1, [], 0) == [[0], 1, 0]
n, E = 10 ** 5, 2 * 10 ** 5
edges = [[random.randrange(n), random.randrange(n), random.randint(0, 100)] for _ in range(E)]
dist, pushes, stale = dijkstra_lazy(n, edges, 0)
reached = sum(x is not None for x in dist)
assert pushes <= E + 1 and stale == pushes - reached
print('n=10^5, E=2*10^5: reached', reached, 'pushes', pushes, '<= E + 1 =', E + 1, '| stale', stale, '== pushes - reached =', pushes - reached)
