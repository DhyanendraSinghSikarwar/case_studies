import random

random.seed(3)

def components(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    seen = [False] * n; out = []
    for s in range(n):                      # scanning in ascending order = components ordered by smallest node
        if seen[s]:
            continue
        seen[s] = True; stack = [s]; comp = []
        while stack:
            u = stack.pop(); comp.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True; stack.append(v)
        out.append(sorted(comp))
    return out

def components_dsu(n, edges):
    parent = list(range(n)); size = [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]    # path halving, iterative
            x = parent[x]
        return x
    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            if size[a] < size[b]: a, b = b, a
            parent[b] = a; size[a] += size[b]
    groups = {}
    for x in range(n):
        groups.setdefault(find(x), []).append(x)
    return sorted(groups.values())          # each group ascending already; order by smallest node

def brute(n, edges):
    """Label propagation: keep lowering labels to the neighbour minimum until nothing changes."""
    lab = list(range(n)); changed = True
    while changed:
        changed = False
        for u, v in edges:
            m = min(lab[u], lab[v])
            if lab[u] != m or lab[v] != m:
                lab[u] = lab[v] = m; changed = True
    g = {}
    for i, l in enumerate(lab):
        g.setdefault(l, []).append(i)
    return sorted(g.values())

for f in (components, components_dsu, brute):
    assert f(6, [[0, 1], [1, 2], [3, 4]]) == [[0, 1, 2], [3, 4], [5]]
    assert f(3, []) == [[0], [1], [2]]
    assert f(0, []) == []
    assert f(4, [[2, 2], [1, 3], [3, 1]]) == [[0], [1, 3], [2]]
print('4 prompt examples ok for DFS, union-find and brute force')

for _ in range(800):
    n = random.randint(0, 9)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 10))] if n else []
    a = components(n, edges)
    assert a == components_dsu(n, edges) == brute(n, edges), (n, edges)
    assert sum(map(len, a)) == n
print('800 seeded random multigraphs with self loops: three methods agree')

# exhaustive: all edge sets (loops allowed) on 3 nodes = 2^6 subsets of the 6 possible unordered pairs incl. loops
pairs = [(u, v) for u in range(3) for v in range(u, 3)]
for mask in range(1 << len(pairs)):
    e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert components(3, e) == components_dsu(3, e) == brute(3, e)
print('exhaustive on 3 nodes: ok')

# scale: 10^5 nodes, 2*10^5 edges, plus a 10^5-node path
n = 10 ** 5
big = [[random.randrange(n), random.randrange(n)] for _ in range(2 * 10 ** 5)]
c1, c2 = components(n, big), components_dsu(n, big)
assert c1 == c2
print('random graph n=10^5, E=2*10^5: components =', len(c1), ', largest =', max(map(len, c1)))
path = [[i, i + 1] for i in range(n - 1)]
assert components(n, path) == [list(range(n))] == components_dsu(n, path)
print('path of 10^5 nodes: one component (iterative, no RecursionError)')
print('union-find: sets = n - successful unions:', n, '-', n - len(c2), '=', len(c2))
