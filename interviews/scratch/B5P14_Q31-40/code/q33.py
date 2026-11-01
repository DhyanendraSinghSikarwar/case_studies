import random
import sys

random.seed(3301)


def bridges(n, edges):
    """Iterative lowlink DFS. Stack frames: (node, parent edge index, next neighbour position)."""
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:                                   # a self loop is never a bridge
            g[u].append((v, i))
            g[v].append((u, i))
    disc = [-1] * n
    low = [0] * n
    timer = 0
    found = set()
    for s in range(n):                               # graph may be disconnected
        if disc[s] != -1:
            continue
        disc[s] = low[s] = timer
        timer += 1
        stack = [(s, -1, 0)]
        while stack:
            u, pe, i = stack.pop()
            if i < len(g[u]):
                stack.append((u, pe, i + 1))         # come back for the next neighbour
                v, e = g[u][i]
                if e == pe:                          # skip the parent EDGE (by index), not the parent node
                    continue
                if disc[v] == -1:                    # tree edge: descend
                    disc[v] = low[v] = timer
                    timer += 1
                    stack.append((v, e, 0))
                else:                                # back edge (or forward edge to a finished node)
                    low[u] = min(low[u], disc[v])
            elif stack:                              # u is finished: report to its parent p
                p = stack[-1][0]
                low[p] = min(low[p], low[u])
                if low[u] > disc[p]:
                    found.add((min(u, p), max(u, p)))
    return sorted([a, b] for a, b in found)


def recursive_bridges(n, edges):                     # the version the prompt forbids; shown only to fail
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i)); g[v].append((u, i))
    disc = [-1] * n; low = [0] * n; out = []; t = [0]

    def dfs(u, pe):
        disc[u] = low[u] = t[0]; t[0] += 1
        for v, e in g[u]:
            if e == pe: continue
            if disc[v] == -1:
                dfs(v, e); low[u] = min(low[u], low[v])
                if low[v] > disc[u]: out.append([min(u, v), max(u, v)])
            else:
                low[u] = min(low[u], disc[v])
    for s in range(n):
        if disc[s] == -1: dfs(s, -1)
    return sorted(out)


def components(n, edges, skip=-1):
    p = list(range(n))

    def find(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x
    for i, (u, v) in enumerate(edges):
        if i != skip:
            p[find(u)] = find(v)
    return len({find(x) for x in range(n)})


def brute(n, edges):
    """Remove each edge in turn; it is a bridge if the component count goes up."""
    base = components(n, edges)
    return sorted({(min(u, v), max(u, v)) for i, (u, v) in enumerate(edges)
                   if u != v and components(n, edges, skip=i) > base})


# --- the prompt's examples ---
ex = [(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]], [[1, 3], [3, 4]]),
      (2, [[0, 1], [0, 1]], []),
      (6, [[0, 1], [2, 3], [3, 4], [4, 2], [5, 5]], [[0, 1]])]
for n, e, want in ex:
    got = bridges(n, e)
    print(n, e, '->', got)
    assert got == want == [list(b) for b in brute(n, e)]

# --- random cross-check against the remove-each-edge oracle (parallel edges and self loops included) ---
cases = 0
for _ in range(1500):
    n = random.randint(1, 9)
    m = random.randint(0, 12)
    e = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    assert bridges(n, e) == [list(b) for b in brute(n, e)], (n, e)
    cases += 1
print('random cases passed:', cases)

# --- deep path: 10^5 nodes, every edge is a bridge; the recursive version dies ---
N = 10 ** 5
path = [[i, i + 1] for i in range(N - 1)]
res = bridges(N, path)
assert len(res) == N - 1 and res[0] == [0, 1] and res[-1] == [N - 2, N - 1]
try:
    recursive_bridges(1600, path[:1599])
    print('recursive: no error')
except RecursionError:
    print('recursive version on a 1600-node path: RecursionError (limit', sys.getrecursionlimit(), ')')
print('iterative on 10^5-node path: bridges =', len(res))

# --- edge cases ---
assert bridges(1, []) == []                                     # single node
assert bridges(3, []) == []                                     # no edges
assert bridges(4, [[0, 1], [1, 2], [2, 3], [3, 0]]) == []       # one cycle
assert bridges(4, [[0, 1], [1, 2], [2, 3]]) == [[0, 1], [1, 2], [2, 3]]
assert bridges(3, [[0, 1], [1, 0], [1, 2]]) == [[1, 2]]         # parallel edge protects 0-1 only
assert bridges(4, [[0, 1], [2, 3]]) == [[0, 1], [2, 3]]         # disconnected graph
ring = [[i, (i + 1) % 1000] for i in range(1000)] + [[0, 1000]]
assert bridges(1001, ring) == [[0, 1000]]                       # pendant edge off a big cycle
print('edge asserts passed')
