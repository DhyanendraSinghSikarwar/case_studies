import itertools
import random
import sys
from collections import deque

random.seed(31)

def dfs_topo(n, edges):
    """Iterative three-colour DFS. 0 = new, 1 = on the current path, 2 = finished. Returns reverse postorder or [] on a cycle."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    post = []
    for s in range(n):                                   # start nodes in ascending order
        if color[s]:
            continue
        color[s] = 1
        stack = [(s, iter(adj[s]))]                      # each frame remembers how far we got in its edge list
        while stack:
            u, it = stack[-1]
            for v in it:                                 # resumes where it left off
                if color[v] == 1:                        # edge to a node on the path: cycle (also catches self loops)
                    return []
                if color[v] == 0:
                    color[v] = 1
                    stack.append((v, iter(adj[v])))
                    break                                # go deeper; come back to this frame later
            else:                                        # edge list exhausted: u is finished
                color[u] = 2
                post.append(u)
                stack.pop()
    return post[::-1]

def dfs_topo_recursive(n, edges):
    """Textbook recursive version: the specification for the order (small n only, or it hits the recursion limit)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    post = []
    cyc = [False]
    def go(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1:
                cyc[0] = True
            elif color[v] == 0:
                go(v)
        color[u] = 2
        post.append(u)
    for s in range(n):
        if color[s] == 0:
            go(s)
    return [] if cyc[0] else post[::-1]

def kahn(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == n else []

def is_topological(n, edges, order):
    pos = {x: i for i, x in enumerate(order)}
    return len(order) == n and len(pos) == n and all(pos[u] < pos[v] for u, v in edges)

for n, e, want in [(4, [[0, 1], [0, 2], [1, 3], [2, 3]], [0, 2, 1, 3]), (3, [[0, 1], [1, 2], [2, 0]], []),
                   (3, [], [2, 1, 0]), (5, [[3, 1], [4, 1], [4, 0], [2, 3]], [4, 2, 3, 1, 0])]:
    got = dfs_topo(n, e)
    assert got == want == dfs_topo_recursive(n, e), (n, e, got, want)
    print(n, e, '->', got, '| Kahn gives', kahn(n, e))

# ---- the recursion limit: a 5000-node path
n = 5000
path = [[i, i + 1] for i in range(n - 1)]
try:
    dfs_topo_recursive(n, path)
except RecursionError:
    print('recursive DFS on a', n, 'node path -> RecursionError (limit', sys.getrecursionlimit(), ')')
assert dfs_topo(n, path) == list(range(n))
n = 2 * 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
assert dfs_topo(n, path) == list(range(n))
assert dfs_topo(n, [[i + 1, i] for i in range(n - 1)]) == list(range(n - 1, -1, -1))
assert dfs_topo(n, path + [[n - 1, 0]]) == []                           # one back edge closes the cycle
print('iterative: 2*10^5-node path, its reverse, and the path closed into a cycle all handled')

# ---- exhaustive: every edge SET on n <= 4 (self loops included for n <= 3), plus ordered edge lists with repeats on n = 3
cnt = cyc = differs = 0
for n, loops in [(1, True), (2, True), (3, True), (4, False)]:
    pairs = [(a, b) for a in range(n) for b in range(n) if loops or a != b]
    for mask in range(1 << len(pairs)):
        e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        r = dfs_topo(n, e)
        assert r == dfs_topo_recursive(n, e), (n, e)
        k = kahn(n, e)
        assert (r == []) == (k == []), (n, e)                           # both detect exactly the cyclic graphs
        if r:
            assert is_topological(n, e, r) and is_topological(n, e, k)
            differs += r != k
        else:
            cyc += 1
        cnt += 1
print('exhaustive on', cnt, 'graphs:', cyc, 'cyclic ->', '[]; every acyclic one gives a valid order equal to the recursive DFS;',
      'DFS order differs from Kahn order on', differs)
opts = [(a, b) for a in range(3) for b in range(3)]
for k in range(4):
    for combo in itertools.product(opts, repeat=k):
        e = [list(p) for p in combo]
        assert dfs_topo(3, e) == dfs_topo_recursive(3, e)
print('ordered edge lists with repeats on 3 nodes also match the recursive version')

# ---- seeded random DAGs and cyclic graphs
for _ in range(500):
    n = random.randint(1, 9)
    perm = list(range(n))
    random.shuffle(perm)
    e = [[perm[min(a, b)], perm[max(a, b)]] for a, b in ((random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, 14))) if a != b]
    r = dfs_topo(n, e)
    assert r == dfs_topo_recursive(n, e) and is_topological(n, e, r)
print('500 seeded random DAGs: valid order, equal to the recursive DFS')

# ---- big: 10^5 nodes, 2*10^5 edges, random DAG over a shuffled labelling
n, E = 10 ** 5, 2 * 10 ** 5
perm = list(range(n))
random.shuffle(perm)
e = []
while len(e) < E:
    a, b = random.randrange(n), random.randrange(n)
    if a != b:
        e.append([perm[min(a, b)], perm[max(a, b)]])
r = dfs_topo(n, e)
assert is_topological(n, e, r)
print('n=10^5, E=2*10^5 random DAG: valid topological order of length', len(r))
assert dfs_topo(1, [[0, 0]]) == []
print('self loop -> []')
