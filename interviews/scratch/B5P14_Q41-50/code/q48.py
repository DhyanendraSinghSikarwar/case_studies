import itertools, random
random.seed(48)

def min_starts(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n; stack = []; counter = 0; nc = 0
    for s in range(n):                        # iterative Tarjan, as in Q41
        if idx[s] != -1:
            continue
        idx[s] = low[s] = counter; counter += 1; stack.append(s); on[s] = True
        work = [(s, 0)]
        while work:
            u, i = work.pop()
            if i < len(g[u]):
                work.append((u, i + 1)); v = g[u][i]
                if idx[v] == -1:
                    idx[v] = low[v] = counter; counter += 1; stack.append(v); on[v] = True; work.append((v, 0))
                elif on[v]:
                    low[u] = min(low[u], idx[v])
            else:
                if low[u] == idx[u]:
                    while True:
                        w = stack.pop(); on[w] = False; comp[w] = nc
                        if w == u:
                            break
                    nc += 1
                if work:
                    p = work[-1][0]; low[p] = min(low[p], low[u])
    has_in = [False] * nc
    for u, v in edges:
        if comp[u] != comp[v]:
            has_in[comp[v]] = True            # this component receives an edge from another one
    smallest = [None] * nc
    for v in range(n):                        # ascending v: the first node seen is the component minimum
        if smallest[comp[v]] is None:
            smallest[comp[v]] = v
    return sorted(smallest[c] for c in range(nc) if not has_in[c])

def oracle(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    def covers(starts):
        seen = set(starts); q = list(starts)
        for u in q:
            for v in g[u]:
                if v not in seen: seen.add(v); q.append(v)
        return len(seen) == n
    for k in range(1, n + 1):                 # smaller sets first; combinations come out in lexicographic order
        for combo in itertools.combinations(range(n), k):
            if covers(combo): return list(combo)

assert min_starts(5, [[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]]) == [0, 3]
assert min_starts(3, [[0, 1], [1, 2], [2, 0]]) == [0]
assert min_starts(3, []) == [0, 1, 2]
print('examples ok')

for _ in range(800):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 14))]
    assert min_starts(n, edges) == oracle(n, edges), (n, edges)
print('800 random graphs match the exhaustive subset oracle')

assert min_starts(1, [[0, 0]]) == [0]
assert min_starts(4, [[3, 2], [2, 1], [1, 0]]) == [3]                    # path against the node order
assert min_starts(4, [[0, 1], [1, 0], [2, 3], [3, 2]]) == [0, 2]        # two cycles
assert min_starts(3, [[0, 2], [1, 2], [0, 2]]) == [0, 1]                 # repeated edges
N = 10**5
assert min_starts(N, [[i + 1, i] for i in range(N - 1)]) == [N - 1]
assert min_starts(N, [[i, (i + 1) % N] for i in range(N)]) == [0]
print('10^5 path and 10^5 cycle ok (iterative)')
print('first example:', min_starts(5, [[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]]))
