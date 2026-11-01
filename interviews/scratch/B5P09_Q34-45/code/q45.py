import itertools
import random
from collections import deque

random.seed(45)

def min_height_roots(n, edges):
    """Peel all current leaves layer by layer (Kahn's algorithm on degrees) until at most two nodes remain."""
    if n <= 2:
        return list(range(n))                      # n = 1 -> [0]; n = 2 -> [0, 1] (both heights are 1)
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(a) for a in adj]
    leaves = [i for i in range(n) if deg[i] == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)                   # the whole layer is removed at once
        nxt = []
        for u in leaves:
            for v in adj[u]:
                deg[v] -= 1
                if deg[v] == 1:                    # v has become a leaf of the smaller tree
                    nxt.append(v)
        leaves = nxt
    return sorted(leaves)

def heights_brute(n, edges):
    """Brute force: BFS from every root and take the longest distance (O(n^2))."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    hs = []
    for r in range(n):
        d = {r: 0}
        q = deque([r])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1
                    q.append(v)
        hs.append(max(d.values()))
    return hs

def mht_brute(n, edges):
    hs = heights_brute(n, edges)
    return [i for i in range(n) if hs[i] == min(hs)]

def prufer_tree(seq, n):
    """Decode a Pruefer sequence into the n - 1 edges of a labelled tree (every labelled tree appears once)."""
    deg = [1] * n
    for x in seq:
        deg[x] += 1
    edges = []
    for x in seq:
        leaf = min(i for i in range(n) if deg[i] == 1)
        edges.append([leaf, x])
        deg[leaf] -= 1
        deg[x] -= 1
    u, v = [i for i in range(n) if deg[i] == 1]
    edges.append([u, v])
    return edges

# ---- examples from the prompt
assert min_height_roots(4, [[1, 0], [1, 2], [1, 3]]) == [1]
assert min_height_roots(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]) == [3, 4]
assert min_height_roots(1, []) == [0]
assert min_height_roots(2, [[0, 1]]) == [0, 1]
print('examples ok')

# ---- exhaustive: EVERY labelled tree on 2..7 nodes (Pruefer: n^(n-2) of them), against the all-roots BFS
total = 0
counts = {1: 0, 2: 0}
for n in range(2, 8):
    for seq in itertools.product(range(n), repeat=n - 2):
        e = prufer_tree(seq, n)
        a = min_height_roots(n, e)
        assert a == mht_brute(n, e), (n, e)
        assert len(a) in (1, 2)                    # the prompt's claim: one or two minimum-height roots
        counts[len(a)] += 1
        total += 1
print('exhaustive:', total, 'labelled trees on 2..7 nodes; answers always match; number of roots:', counts)

# ---- the two roots are adjacent, and the height is ceil(diameter / 2): check on seeded random trees
N = 400
for _ in range(N):
    n = random.randint(1, 30)
    e = [[random.randrange(i), i] for i in range(1, n)]
    random.shuffle(e)
    a = min_height_roots(n, e)
    assert a == mht_brute(n, e)
    if len(a) == 2:
        assert [a[0], a[1]] in e or [a[1], a[0]] in e
    hs = heights_brute(n, e)
    diam = max(hs)                                 # eccentricity of a node on a diameter equals the diameter
    assert min(hs) == (diam + 1) // 2
print('random check on', N, 'seeded trees: answers match, two roots are adjacent, min height = ceil(diameter / 2)')

# ---- edge cases and max size
assert min_height_roots(3, [[0, 1], [1, 2]]) == [1]                 # path with odd node count
assert min_height_roots(4, [[0, 1], [1, 2], [2, 3]]) == [1, 2]      # path with even node count
star = [[0, i] for i in range(1, 20000)]
assert min_height_roots(20000, star) == [0]
path = [[i, i + 1] for i in range(19999)]
assert min_height_roots(20000, path) == [9999, 10000]
random.shuffle(path)
assert min_height_roots(20000, path) == [9999, 10000]              # edge order does not matter
rt = [[random.randrange(i), i] for i in range(1, 20000)]
print('max size n = 20000, random tree roots:', min_height_roots(20000, rt), '| path roots:', min_height_roots(20000, path))
print('edge cases ok')
