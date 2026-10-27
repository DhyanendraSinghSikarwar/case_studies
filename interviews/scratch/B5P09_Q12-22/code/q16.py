import itertools, random
from collections import deque
random.seed(16)

def bfs_lists(n, edges, directed, src):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)                  # an undirected edge is stored twice
    seen = {src}
    q = deque([src])
    reached = entries = 0
    while q:
        u = q.popleft()
        reached += 1
        entries += len(adj[u])                # every list entry of a dequeued node is examined
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return [reached, entries, n * reached]    # a matrix row has n cells, scanned once per reached node

def bfs_matrix_counted(n, edges, directed, src):   # really scans the matrix and counts cells and ones
    mat = [[0] * n for _ in range(n)]
    for u, v in edges:
        mat[u][v] = 1
        if not directed:
            mat[v][u] = 1
    seen = {src}
    q = deque([src])
    reached = entries = cells = 0
    while q:
        u = q.popleft()
        reached += 1
        for v in range(n):
            cells += 1
            if mat[u][v]:
                entries += 1
                if v not in seen:
                    seen.add(v)
                    q.append(v)
    return [reached, entries, cells]

assert bfs_lists(5, [[0, 1], [1, 2], [2, 0], [3, 4]], False, 0) == [3, 6, 15]
assert bfs_lists(4, [[0, 1], [1, 2], [2, 3]], True, 1) == [3, 2, 12]
assert bfs_lists(3, [], True, 2) == [1, 0, 3]
print("examples ok")

# exhaustive: every directed graph on n <= 4 nodes, every source; every undirected graph with every orientation choice
cnt = 0
for n in range(1, 5):
    allp = [(u, v) for u in range(n) for v in range(n) if u != v]
    for mask in range(1 << len(allp)):
        es = [list(p) for i, p in enumerate(allp) if mask >> i & 1]
        for s in range(n):
            r = bfs_lists(n, es, True, s)
            assert r == bfs_matrix_counted(n, es, True, s)
            assert r[1] <= len(es) and len(es) <= n * n and r[0] <= n
            cnt += 1
    und = [(u, v) for u in range(n) for v in range(u + 1, n)]
    for mask in range(1 << len(und)):
        es = [[u, v] if (u + v + mask) % 2 else [v, u] for i, (u, v) in enumerate(und) if mask >> i & 1]
        for s in range(n):
            r = bfs_lists(n, es, False, s)
            assert r == bfs_matrix_counted(n, es, False, s)
            assert r[1] <= 2 * len(es)
            cnt += 1
print("exhaustive n<=4: %d (graph, source) runs; list count == scanned matrix ones; entries <= E (directed) or 2E (undirected); E <= n^2" % cnt)

# random larger graphs up to n = 60
for _ in range(300):
    n = random.randint(1, 60); d = random.random() < .5
    pool = [(u, v) for u in range(n) for v in range(n) if u != v and (d or u < v)]
    es = [list(p) for p in random.sample(pool, random.randint(0, min(len(pool), 150)))]
    s = random.randrange(n)
    assert bfs_lists(n, es, d, s) == bfs_matrix_counted(n, es, d, s)
print("300 random graphs (n <= 60) agree")

# the shape of the gap: a path of 60 nodes, directed, from node 0
n = 60; path = [[i, i + 1] for i in range(n - 1)]
r = bfs_lists(n, path, True, 0)
print("path of 60: reached=%d list entries=%d matrix cells=%d" % tuple(r))
assert r == [60, 59, 3600]
# undirected: each edge examined twice
r = bfs_lists(n, path, False, 0)
print("same path undirected: list entries=%d (= 2E = %d)" % (r[1], 2 * len(path)))
assert r[1] == 2 * len(path)
