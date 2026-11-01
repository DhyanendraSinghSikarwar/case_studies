import itertools
import random
from collections import deque

random.seed(41)

def safe_nodes(graph):
    """Kahn's algorithm on the REVERSED graph. A node is safe when all its out-neighbours are safe."""
    n = len(graph)
    rev = [[] for _ in range(n)]
    out = [len(graph[u]) for u in range(n)]          # counts repeats, as the reversed lists will too
    for u in range(n):
        for v in graph[u]:
            rev[v].append(u)
    q = deque(i for i in range(n) if out[i] == 0)    # terminal nodes are safe
    safe = []
    while q:
        u = q.popleft()
        safe.append(u)
        for p in rev[u]:                             # p points to u, and u is now known safe
            out[p] -= 1
            if out[p] == 0:                          # all of p's targets are safe, so p is safe
                q.append(p)
    return sorted(safe)

def safe_brute(graph):
    """Reference: transitive closure. A node is unsafe iff it can reach a node that lies on a cycle."""
    n = len(graph)
    reach = [[False] * n for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    on_cycle = [i for i in range(n) if reach[i][i]]
    return [u for u in range(n) if u not in on_cycle and not any(reach[u][c] for c in on_cycle)]

def safe_recursive(graph):
    """Three-colour DFS (0 new, 1 in progress, 2 safe) written recursively, to show the recursion limit."""
    n = len(graph)
    color = [0] * n
    def ok(u):
        if color[u]:
            return color[u] == 2
        color[u] = 1
        for v in graph[u]:
            if not ok(v):
                return False
        color[u] = 2
        return True
    return [u for u in range(n) if ok(u)]

# ---- examples from the prompt
assert safe_nodes([[1, 2], [2, 3], [5], [0], [5], [], []]) == [2, 4, 5, 6]
assert safe_nodes([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]) == [4]
assert safe_nodes([[0]]) == []
assert safe_nodes([[]]) == [0]
print('examples ok')

# ---- exhaustive: every adjacency-list graph with lists of length <= 2 (repeats and self loops allowed)
def all_lists(n, maxlen):
    opts = [list(t) for L in range(maxlen + 1) for t in itertools.product(range(n), repeat=L)]
    return itertools.product(opts, repeat=n)

count = 0
for n, maxlen in ((1, 3), (2, 3), (3, 2), (4, 2)):
    for g in all_lists(n, maxlen):
        g = [list(x) for x in g]
        assert safe_nodes(g) == safe_brute(g), g
        count += 1
print('exhaustive check:', count, 'graphs on 1-4 nodes (repeats and self loops included), all agree')

# ---- seeded random check on bigger graphs, also against the colour DFS
N = 500
for _ in range(N):
    n = random.randint(1, 12)
    g = [[random.randrange(n) for _ in range(random.choice([0, 0, 1, 2, 3]))] for _ in range(n)]
    a = safe_nodes(g)
    assert a == safe_brute(g) == safe_recursive(g), g
print('random check on', N, 'seeded graphs: Kahn on reversed graph == closure == colour DFS')

# ---- edge cases
assert safe_nodes([[1], [1]]) == []                    # a node leading into a self loop is unsafe
assert safe_nodes([[1, 1], [2], []]) == [0, 1, 2]      # repeated edges: the counter counts both, both get decremented
assert safe_nodes([[1], [0], [2, 3], []]) == [3]       # cycle {0,1}; node 2 reaches a terminal and a self loop at 2
assert safe_nodes([[], [], []]) == [0, 1, 2]
# max size: n = 10^4, a chain of 10^4 nodes (deep) plus extra edges to reach 4 * 10^4 entries
n = 10000
g = [[i + 1] for i in range(n - 1)] + [[]]
for _ in range(4 * 10 ** 4 - (n - 1)):
    u = random.randrange(n - 1)
    g[u].append(random.randrange(u + 1, n))            # forward edges only: acyclic, so everything is safe
assert safe_nodes(g) == list(range(n))
try:
    safe_recursive(g)
except RecursionError:
    print('recursive colour DFS on the 10^4-node chain: RecursionError; Kahn on the reversed graph is fine')
g[n - 1] = [n - 1]                                    # one self loop at the end: everything that reaches it is unsafe
assert safe_nodes(g) == []
print('edge cases ok')
