import itertools
import random

random.seed(36)

def euler_kind(n, edges):
    """Degrees plus connectivity of the nodes that have edges. Never builds the trail."""
    if not edges:
        return 'circuit'
    deg = [0] * n
    parent = list(range(n))

    def find(x):                                   # iterative find with path halving
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        deg[u] += 1
        deg[v] += 1                                # a self loop adds 2 in total (1 + 1)
        parent[find(u)] = find(v)
    if len({find(u) for u, v in edges}) > 1:       # edges live in more than one component
        return 'none'
    odd = sum(d % 2 for d in deg)
    return 'circuit' if odd == 0 else 'path' if odd == 2 else 'none'

def euler_brute(n, edges):
    """Try every trail: from every start node, use each edge once in either direction."""
    m = len(edges)
    if m == 0:
        return 'circuit'
    found = set()

    def go(u, used, start, count):
        if count == m:
            found.add('circuit' if u == start else 'path')
            return
        for i, (a, b) in enumerate(edges):
            if not used >> i & 1:
                if a == u:
                    go(b, used | 1 << i, start, count + 1)
                if b == u and a != b:
                    go(a, used | 1 << i, start, count + 1)

    for s in range(n):
        go(s, 0, s, 0)
    return 'circuit' if 'circuit' in found else 'path' if 'path' in found else 'none'

# ---- examples from the prompt
assert euler_kind(4, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 2]]) == 'circuit'
assert euler_kind(4, [[0, 1], [1, 2], [2, 3]]) == 'path'
assert euler_kind(4, [[0, 1], [0, 2], [0, 3]]) == 'none'
assert euler_kind(5, [[0, 1], [2, 3]]) == 'none'
assert euler_kind(3, []) == 'circuit'
print('examples ok')

# ---- exhaustive: EVERY multiset of at most 5 edges (self loops and repeats included) on 4 nodes
types = [(u, v) for u in range(4) for v in range(u, 4)]       # 10 edge types
total = 0
tally = {'circuit': 0, 'path': 0, 'none': 0}
for m in range(0, 6):
    for combo in itertools.combinations_with_replacement(types, m):
        edges = [list(e) for e in combo]
        a, b = euler_kind(4, edges), euler_brute(4, edges)
        assert a == b, (edges, a, b)
        tally[a] += 1
        total += 1
print('exhaustive check:', total, 'edge multisets on 4 nodes, all agree with the trail search', tally)

# ---- seeded random check on 5-6 nodes with up to 7 edges
N = 600
for _ in range(N):
    n = random.randint(5, 6)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 7))]
    assert euler_kind(n, edges) == euler_brute(n, edges), (n, edges)
print('random check on', N, 'seeded graphs ok')

# ---- edge cases
assert euler_kind(1, [[0, 0]]) == 'circuit'                   # one self loop: degree 2, closes on itself
assert euler_kind(2, [[0, 1], [0, 1]]) == 'circuit'           # two parallel edges
assert euler_kind(2, [[0, 0], [1, 1]]) == 'none'              # two components, each with an edge
assert euler_kind(5, [[0, 1], [1, 2], [2, 0]]) == 'circuit'   # isolated nodes 3 and 4 do not matter
assert euler_kind(2, [[0, 1]]) == 'path'                      # exactly two odd nodes
assert euler_kind(20, [[i, (i + 1) % 20] for i in range(20)] * 2) == 'circuit'   # max n, 40 edges
print('edge cases ok')
