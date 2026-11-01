import heapq
import itertools
import random

random.seed(29)

def kruskal(n, edges):
    """Sort by weight, add an edge iff it joins two different components. Iterative find, path halving, union by size."""
    parent = list(range(n))
    size = [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    total = used = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a == b:                                  # self loops and cycle-forming edges are skipped here
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        total += w
        used += 1
        if used == n - 1:
            break
    return total if used == n - 1 else -1

def prim(n, edges):
    """Heap-based alternative: grow one tree from node 0 by the cheapest edge leaving it (lazy heap)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            adj[u].append((w, v))
            adj[v].append((w, u))
    seen = [False] * n
    seen[0] = True
    heap = list(adj[0])
    heapq.heapify(heap)
    total, cnt = 0, 1
    while heap and cnt < n:
        w, v = heapq.heappop(heap)
        if seen[v]:
            continue
        seen[v] = True
        total += w
        cnt += 1
        for item in adj[v]:
            if not seen[item[1]]:
                heapq.heappush(heap, item)
    return total if cnt == n else -1

def mst_brute(n, edges):
    """Try every (n-1)-edge subset: it is a spanning tree iff it has no cycle. Take the cheapest."""
    if n == 1:
        return 0
    best = None
    for sub in itertools.combinations(edges, n - 1):
        p = list(range(n))
        def find(x):
            while p[x] != x:
                x = p[x]
            return x
        ok = True
        for u, v, w in sub:
            a, b = find(u), find(v)
            if a == b:
                ok = False
                break
            p[a] = b
        if ok:
            t = sum(e[2] for e in sub)
            best = t if best is None or t < best else best
    return -1 if best is None else best

def count_min_trees(n, edges):
    """How many distinct (n-1)-edge spanning trees have the optimal weight? (tiny graphs; shows that the tree is not unique)"""
    best, cnt = None, 0
    for sub in itertools.combinations(range(len(edges)), n - 1):
        p = list(range(n))
        def find(x):
            while p[x] != x:
                x = p[x]
            return x
        ok = True
        for i in sub:
            u, v, _ = edges[i]
            a, b = find(u), find(v)
            if a == b:
                ok = False
                break
            p[a] = b
        if ok:
            t = sum(edges[i][2] for i in sub)
            if best is None or t < best:
                best, cnt = t, 1
            elif t == best:
                cnt += 1
    return best, cnt

for n, e, want in [(4, [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]], 7), (3, [[0, 1, 2]], -1), (1, [], 0),
                   (3, [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]], 4)]:
    got = kruskal(n, e)
    assert got == want == prim(n, e) == mst_brute(n, e), (n, e, got, want)
    print(n, e, '->', got)

# ---- ties: several different trees, one weight
n, e = 3, [[0, 1, 2], [1, 2, 2], [0, 2, 2]]
print('triangle with all weights 2: (weight, number of minimum trees) =', count_min_trees(n, e), '-> only the weight is unique')
n, e = 3, [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]]
print('example 4: (weight, number of minimum trees) =', count_min_trees(n, e), '; the weight-1 self loop is never usable')

# ---- exhaustive: all multisets of up to 4 edges on 3 nodes (weights 1..3, self loops included), and up to 4 edges on 4 nodes (weights 1..2)
cnt = 0
for n, W, K in [(3, 3, 4), (4, 2, 4)]:
    opts = [(u, v, w) for u in range(n) for v in range(n) for w in range(1, W + 1)]
    for k in range(K + 1):
        for combo in itertools.combinations_with_replacement(opts, k):
            edges = [list(x) for x in combo]
            r = kruskal(n, edges)
            assert r == prim(n, edges) == mst_brute(n, edges), (n, edges)
            cnt += 1
print('exhaustive on', cnt, 'multigraphs: Kruskal == Prim == best spanning subset')

for _ in range(500):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n), random.randint(1, 9)] for _ in range(random.randint(0, 12))]
    assert kruskal(n, edges) == prim(n, edges), (n, edges)
print('500 seeded random graphs: Kruskal == Prim (n up to 8)')

# ---- max size: n = 10^4, E = 10^5 with repeats and self loops; connected by a spine so the answer is not -1
n = 10 ** 4
edges = [[i, i + 1, random.randint(1, 10 ** 5)] for i in range(n - 1)]
edges += [[random.randrange(n), random.randrange(n), random.randint(1, 10 ** 5)] for _ in range(10 ** 5 - len(edges))]
k, p = kruskal(n, edges), prim(n, edges)
assert k == p and k != -1
print('n=10^4, E=10^5: Kruskal', k, '== Prim', p)
assert kruskal(n, [e for e in edges if e[0] != 5000 and e[1] != 5000]) == -1    # isolating one node disconnects the graph
print('removing every edge at node 5000 -> -1 (disconnected)')
assert kruskal(1, [[0, 0, 5]]) == 0
print('edge asserts passed')
