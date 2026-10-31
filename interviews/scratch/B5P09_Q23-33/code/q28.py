import itertools
import random

random.seed(28)
INF = float('inf')

def bellman_ford(n, edges, src, rounds=None, guard=True):
    """n-1 rounds of relaxing every edge, then one more round: any improvement means a reachable negative cycle."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n - 1 if rounds is None else rounds):
        changed = False
        for u, v, w in edges:
            if d[u] != INF and d[u] + w < d[v]:          # never relax out of an unreached node
                d[v] = d[u] + w
                changed = True
        if not changed:                                  # early exit: distances are final
            break
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            return None
    return [None if x == INF else x for x in d]

def bellman_ford_unguarded(n, edges, src, big=10 ** 9):
    """Bug: unreached nodes get a large finite number and are relaxed like real ones."""
    d = [big] * n
    d[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] + w < d[v]:
            return None
    return [None if x >= big // 2 else x for x in d]

def floyd_brute(n, edges, src):
    """Independent brute force: all-pairs Floyd-Warshall; a negative cycle shows up as f[k][k] < 0 for a k reachable from src."""
    f = [[INF] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 0
    for u, v, w in edges:
        f[u][v] = min(f[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if f[i][k] + f[k][j] < f[i][j]:
                    f[i][j] = f[i][k] + f[k][j]
    if any(f[src][k] < INF and f[k][k] < 0 for k in range(n)):
        return None
    return [None if x == INF else x for x in f[src]]

for n, e, s, want in [(4, [[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]], 0, [0, 2, 5, 4]),
                      (3, [[0, 1, 1], [1, 2, -3], [2, 1, 1]], 0, None),
                      (3, [[1, 2, -1], [2, 1, -1]], 0, [0, None, None])]:
    got = bellman_ford(n, e, s)
    assert got == want == floyd_brute(n, e, s), (got, want)
    print(n, e, 'src', s, '->', got)

# ---- the two classic bugs on example 3: a negative cycle that is NOT reachable from src
e3 = [[1, 2, -1], [2, 1, -1]]
print('unguarded INF arithmetic on example 3 ->', bellman_ford_unguarded(3, e3, 0), '(false alarm: that cycle is unreachable)')

# ---- why n-1 rounds suffice: a shortest path without a negative cycle has at most n-1 edges, and round k fixes the k-th edge of every
# shortest path. Worst case = path edges listed in REVERSE order, so each round advances only one edge.
n = 8
path = [[i, i + 1, 1] for i in range(n - 1)][::-1]
full = bellman_ford(n, path, 0)
short = bellman_ford(n, path, 0, rounds=n - 2)            # one round too few: distances are not final, so the check round fires
print('reverse-ordered path, n=8: n-1 rounds ->', full, '| n-2 rounds ->', short)
assert full == list(range(n)) and short is None

# ---- exhaustive: every ordered list of up to 3 edges on 3 nodes with weights -2..2 (self loops included), every source
opts = [(u, v, w) for u in range(3) for v in range(3) for w in range(-2, 3)]    # 45 edge options
cnt = neg = 0
for k in range(4):
    for combo in itertools.product(opts, repeat=k):
        edges = [list(x) for x in combo]
        for src in range(3):
            a = bellman_ford(3, edges, src)
            assert a == floyd_brute(3, edges, src), (edges, src)
            neg += a is None
            cnt += 1
print('exhaustive on', cnt, '(graph, source) cases, of which', neg, 'have a reachable negative cycle: Bellman-Ford == Floyd-Warshall')

# ---- seeded random graphs up to n = 7 with a mix of negative edges
for _ in range(1000):
    n = random.randint(1, 7)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-5, 8)] for _ in range(random.randint(0, 14))]
    src = random.randrange(n)
    assert bellman_ford(n, edges, src) == floyd_brute(n, edges, src), (n, edges, src)
print('1000 seeded random graphs agree')

# ---- the unguarded bug versus the correct code over the same random graphs
wrong = 0
for _ in range(1000):
    n = random.randint(1, 7)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-5, 8)] for _ in range(random.randint(0, 14))]
    src = random.randrange(n)
    wrong += bellman_ford_unguarded(n, edges, src) != floyd_brute(n, edges, src)
print('unguarded variant disagrees with the checker on', wrong, 'of 1000 random graphs')

# ---- max size: n = 500, E = 5000, worst-case O(V*E) = about 2.5 * 10^6 relaxations
n, E = 500, 5000
pot = [random.randint(0, 50) for _ in range(n)]
edges = []
for _ in range(E):
    u, v = random.randrange(n), random.randrange(n)
    edges.append([u, v, random.randint(0, 50) + pot[u] - pot[v]])              # reduced-cost form: negative edges, but no negative cycle
assert min(w for _, _, w in edges) < 0
r = bellman_ford(n, edges, 0)
assert r is not None and r[0] == 0
edges += [[0, 1, -100], [1, 0, -100]]                                            # a reachable negative 2-cycle
assert bellman_ford(n, edges, 0) is None
print('n=500, E=5000 with negative edges but no negative cycle: reached', sum(x is not None for x in r),
      'nodes; adding a 2-cycle of weight -200 -> None')
assert bellman_ford(1, [], 0) == [0]
assert bellman_ford(1, [[0, 0, -1]], 0) is None and bellman_ford(1, [[0, 0, 1]], 0) == [0]
print('edge asserts passed (n=1, negative and positive self loops)')
