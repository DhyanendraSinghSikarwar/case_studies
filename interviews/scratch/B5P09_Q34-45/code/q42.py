import heapq
import itertools
import random

random.seed(42)
INF = float('inf')

def to_list(d):
    return [None if x == INF else x for x in d]

def dijkstra_finalise(n, edges, src, trace=None):
    """Finalise-on-first-pop Dijkstra, exactly as the prompt describes."""
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
        done.add(u)                                  # u's distance is now treated as final
        if trace is not None:
            trace.append(f'finalise {u} at {d}')
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
            elif v in done and d + w < dist[v] and trace is not None:
                trace.append(f'   edge {u}->{v} would give {d + w} < {dist[v]}, but {v} is finalised: ignored')
    return to_list(dist)

def dijkstra_stale_check(n, edges, src):
    """Stale-check variant: a node may be expanded again whenever a shorter distance is found."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    h = [(0, src)]
    expansions = 0
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue                                 # stale entry
        expansions += 1
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
    return to_list(dist), expansions

def bellman_ford(n, edges, src):
    """True distances; None if a negative cycle is reachable from src."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] != INF and d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            return None
    return to_list(d)

def solve(n, edges, src):
    return [dijkstra_finalise(n, edges, src), bellman_ford(n, edges, src)]

# ---- examples from the prompt
assert solve(3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], 0) == [[0, 4, 5], [0, 2, 5]]
assert solve(3, [[0, 1, 1], [1, 2, 2]], 0) == [[0, 1, 3], [0, 1, 3]]
assert solve(4, [[0, 1, 2], [0, 2, 3], [2, 1, -2], [1, 3, 1]], 0) == [[0, 2, 3, 3], [0, 1, 3, 2]]
print('examples ok')

# ---- the exact step where the reasoning breaks (smallest case, 3 nodes)
tr = []
dijkstra_finalise(3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], 0, tr)
print('\n'.join(tr))

# ---- exhaustive on three nodes: every edge (6 possible directed pairs) absent or weight -3..3, src = 0
pairs = [(u, v) for u in range(3) for v in range(3) if u != v]
total = wrong = wrong_nonneg = valid = 0
for choice in itertools.product([None, -3, -2, -1, 0, 1, 2, 3], repeat=len(pairs)):
    edges = [[u, v, w] for (u, v), w in zip(pairs, choice) if w is not None]
    true = bellman_ford(3, edges, 0)
    total += 1
    if true is None:                                 # negative cycle reachable: outside the prompt's guarantee
        continue
    valid += 1
    bad = dijkstra_finalise(3, edges, 0) != true
    wrong += bad
    if all(w >= 0 for _, _, w in edges):
        wrong_nonneg += bad
    assert dijkstra_stale_check(3, edges, 0)[0] == true      # the stale-check variant is always right here
print('exhaustive 3-node graphs:', total, 'built,', valid, 'without a reachable negative cycle;',
      'finalise-on-pop wrong on', wrong, '| with all weights >= 0 wrong on', wrong_nonneg)
assert wrong > 0 and wrong_nonneg == 0

# ---- seeded random graphs up to the prompt's limits (n <= 8, weights -10..10), valid ones only
N = 3000
used = diff = 0
for _ in range(N):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-10, 10)] for _ in range(random.randint(0, 16))]
    edges = [e for e in edges if e[0] != e[1]]
    src = random.randrange(n)
    true = bellman_ford(n, edges, src)
    if true is None:
        continue
    used += 1
    assert dijkstra_stale_check(n, edges, src)[0] == true
    diff += dijkstra_finalise(n, edges, src) != true
print('random check:', used, 'valid seeded graphs; stale-check Dijkstra == Bellman-Ford on all;',
      'finalise-on-pop differs on', diff)

# ---- no running-time guarantee for the stale-check variant (family OUTSIDE the prompt's n <= 8 bound)
def blowup(k):
    """k gadgets x -> y: a direct 0-edge and a detour x -> h -> y that is cheaper only once h is popped."""
    edges = []
    for i in range(k):
        x, h, y = 2 * i, 2 * i + 1, 2 * i + 2
        a = 2 ** (k - i)
        edges += [[x, y, 0], [x, h, a], [h, y, -2 * a]]
    return 2 * k + 1, edges
rows = []
for k in (1, 2, 3, 4, 8, 12):
    n, e = blowup(k)
    dist, exp = dijkstra_stale_check(n, e, 0)
    assert dist == bellman_ford(n, e, 0)
    rows.append((n, exp))
print('expansions on the blow-up family (n nodes, expansions):', rows)
assert rows[-1][1] > 2 ** 12

# ---- edge cases
assert solve(1, [], 0) == [[0], [0]]
assert solve(3, [[1, 2, -5]], 0) == [[0, None, None], [0, None, None]]      # negative edge, unreachable: no effect
assert solve(2, [[0, 1, 0]], 0) == [[0, 0], [0, 0]]
assert solve(2, [[0, 1, -10], [0, 1, 10]], 0) == [[0, -10], [0, -10]]          # parallel edges, negative one wins
print('edge cases ok')
