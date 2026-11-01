import heapq
import itertools
import random

random.seed(34)
INF = float('inf')

def flights_brute(n, flights, src, dst, k):
    """Try every walk of at most k + 1 flights (exponential, tiny inputs only)."""
    best = INF
    def go(u, cost, left):
        nonlocal best
        if u == dst:
            best = min(best, cost)
        if left == 0:
            return
        for a, b, w in flights:
            if a == u:
                go(b, cost + w, left - 1)
    go(src, 0, k + 1)
    return -1 if best == INF else best

def flights_bf(n, flights, src, dst, k):
    """Bellman-Ford, k + 1 rounds, each round reads the PREVIOUS round's distances (a copy)."""
    d = [INF] * n
    d[src] = 0
    for _ in range(k + 1):
        nd = d[:]                       # copy: round r only extends round r-1 routes by one flight
        for u, v, w in flights:
            if d[u] + w < nd[v]:
                nd[v] = d[u] + w
        d = nd
    return -1 if d[dst] == INF else d[dst]

def flights_inplace(n, flights, src, dst, k):
    """WRONG: relaxes into the same array, so one round can chain several flights."""
    d = [INF] * n
    d[src] = 0
    for _ in range(k + 1):
        for u, v, w in flights:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return -1 if d[dst] == INF else d[dst]

def flights_dijkstra_visited(n, flights, src, dst, k):
    """WRONG: Dijkstra by price with a visited set per city (and a flight counter on the heap)."""
    adj = [[] for _ in range(n)]
    for u, v, w in flights:
        adj[u].append((v, w))
    h = [(0, src, 0)]
    seen = set()
    while h:
        c, u, f = heapq.heappop(h)
        if u == dst:
            return c
        if u in seen:
            continue
        seen.add(u)
        if f == k + 1:
            continue
        for v, w in adj[u]:
            heapq.heappush(h, (c + w, v, f + 1))
    return -1

def flights_dijkstra_state(n, flights, src, dst, k):
    """Correct Dijkstra: the state is (city, flights used), so no pruning by city alone."""
    adj = [[] for _ in range(n)]
    for u, v, w in flights:
        adj[u].append((v, w))
    h = [(0, src, 0)]
    best = {}
    while h:
        c, u, f = heapq.heappop(h)
        if u == dst:
            return c
        if best.get((u, f), INF) < c or f == k + 1:
            continue
        for v, w in adj[u]:
            if c + w < best.get((v, f + 1), INF):
                best[(v, f + 1)] = c + w
                heapq.heappush(h, (c + w, v, f + 1))
    return -1

# ---- examples from the prompt
assert flights_bf(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
F3 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
assert flights_bf(3, F3, 0, 2, 0) == 500
assert flights_bf(3, F3, 0, 2, 1) == 200
assert flights_bf(2, [], 0, 1, 0) == -1
print('examples ok')

# ---- why in-place is wrong: with k = 0 (one flight) it still chains 0 -> 1 -> 2 in ONE round
print('k=0 in-place:', flights_inplace(3, F3, 0, 2, 0), ' copy:', flights_bf(3, F3, 0, 2, 0), ' (true answer 500)')
# the order of the edge list decides it, so the bug is also input-order dependent
print('k=0 in-place, reversed list:', flights_inplace(3, F3[::-1], 0, 2, 0))

# ---- why Dijkstra with a visited set is wrong: city 2 is finalised cheaply but with too many flights
FD = [[0, 1, 1], [1, 2, 1], [0, 2, 5], [2, 3, 1]]
print('k=1 true:', flights_bf(4, FD, 0, 3, 1), ' dijkstra+visited:', flights_dijkstra_visited(4, FD, 0, 3, 1),
      ' dijkstra on (city, flights):', flights_dijkstra_state(4, FD, 0, 3, 1))

# ---- seeded cross-check on random small graphs (repeats and cycles allowed)
def rand_case():
    n = random.randint(1, 6)
    fl = [[random.randrange(n), random.randrange(n), random.randint(1, 9)] for _ in range(random.randint(0, 12))]
    src, dst = random.randrange(n), random.randrange(n)
    return n, fl, src, dst, random.randint(0, n - 1)

bad_inplace = bad_dij = 0
N = 2000
for _ in range(N):
    n, fl, s, t, k = rand_case()
    exp = flights_brute(n, fl, s, t, k)
    assert flights_bf(n, fl, s, t, k) == exp, (n, fl, s, t, k)
    assert flights_dijkstra_state(n, fl, s, t, k) == exp
    bad_inplace += flights_inplace(n, fl, s, t, k) != exp
print('cross-check on', N, 'seeded cases: copy-based Bellman-Ford and state Dijkstra match brute force')
# the visited-set bug is rarer, so hunt it on a denser, skewed-price family (Bellman-Ford is the reference)
M = 20000
for _ in range(M):
    n = random.randint(3, 6)
    fl = [[random.randrange(n), random.randrange(n), random.choice([1, 1, 2, 3, 10])] for _ in range(random.randint(4, 12))]
    s, t, k = random.randrange(n), random.randrange(n), random.randint(0, 2)
    bad_dij += flights_dijkstra_visited(n, fl, s, t, k) != flights_bf(n, fl, s, t, k)
print('in-place wrong on', bad_inplace, 'of', N, '| visited-set Dijkstra wrong on', bad_dij, 'of', M, '(skewed family)')
assert bad_inplace > 0 and bad_dij > 0

# ---- edge cases
assert flights_bf(1, [], 0, 0, 0) == 0                          # src == dst costs nothing
assert flights_bf(3, [[0, 1, 5]], 0, 2, 2) == -1                # unreachable
assert flights_bf(2, [[0, 1, 9], [0, 1, 4]], 0, 1, 0) == 4      # parallel flights, take the cheaper
assert flights_bf(3, [[0, 1, 1], [1, 0, 1], [1, 2, 1]], 0, 2, 5) == 2   # cycles never help (positive prices)
# max size: n = 100, 5000 flights, k = 99 -> 100 rounds * 5000 edges = 5*10^5 relaxations
n = 100
big = [[random.randrange(n), random.randrange(n), random.randint(1, 10 ** 4)] for _ in range(5000)]
print('max-size run:', flights_bf(n, big, 0, n - 1, n - 1))
print('edge cases ok')
