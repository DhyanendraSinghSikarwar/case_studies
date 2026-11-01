import random

random.seed(1)

def build(n, edges, directed):
    """Optimal: one pass over the edge list. O(n^2 + E) because of the matrix, O(n + E) without it."""
    adj = [[] for _ in range(n)]
    mat = [[0] * n for _ in range(n)]
    out_deg = [0] * n
    in_deg = [0] * n
    for u, v, w in edges:
        adj[u].append([v, w]); mat[u][v] = w
        out_deg[u] += 1; in_deg[v] += 1
        if not directed:
            adj[v].append([u, w]); mat[v][u] = w
            out_deg[v] += 1; in_deg[u] += 1
    return [adj, mat, out_deg, in_deg]

def brute(n, edges, directed):
    """Brute force: matrix first, then read everything else off it (n^2 scans)."""
    mat = [[0] * n for _ in range(n)]
    for u, v, w in edges:
        mat[u][v] = w
        if not directed:
            mat[v][u] = w
    adj = [[[v, mat[u][v]] for v in range(n) if mat[u][v]] for u in range(n)]
    out_deg = [sum(1 for x in row if x) for row in mat]
    in_deg = [sum(1 for u in range(n) if mat[u][v]) for v in range(n)]
    return [adj, mat, out_deg, in_deg]

def same_up_to_neighbour_order(a, b):
    # the brute force lists neighbours by node id; the optimal one by edge order
    return [[sorted(x) for x in a[0]]] + a[1:] == [[sorted(x) for x in b[0]]] + b[1:]

# the four prompt examples (exact lists, edge order preserved)
assert build(4, [[0, 1, 5], [0, 2, 3], [2, 3, 1]], True) == [[[[1, 5], [2, 3]], [], [[3, 1]], []], [[0, 5, 3, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]], [2, 0, 1, 0], [0, 1, 1, 1]]
assert build(3, [[0, 1, 2], [1, 2, 7]], False) == [[[[1, 2]], [[0, 2], [2, 7]], [[1, 7]]], [[0, 2, 0], [2, 0, 7], [0, 7, 0]], [1, 2, 1], [1, 2, 1]]
assert build(0, [], False) == [[], [], [], []]
assert build(2, [], True) == [[[], []], [[0, 0], [0, 0]], [0, 0], [0, 0]]
print('4 prompt examples ok')

# the order rule: undirected edge [3,1] then [1,0]: node 1 sees 3 first, then 0 (edge order, not id order)
print('adj[1] for edges [3,1],[1,0]:', build(4, [[3, 1, 4], [1, 0, 6]], False)[0][1])

def rand_case():
    n = random.randint(0, 6)
    directed = random.random() < 0.5
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (directed or u < v)]
    random.shuffle(pairs)
    edges = []
    for u, v in pairs[:random.randint(0, len(pairs))]:
        if not directed and random.random() < 0.5:
            u, v = v, u                      # [u, v] and [v, u] are the same undirected edge
        edges.append([u, v, random.randint(1, 99)])
    return n, edges, directed

for _ in range(600):
    n, edges, directed = rand_case()
    a, b = build(n, edges, directed), brute(n, edges, directed)
    assert same_up_to_neighbour_order(a, b), (n, edges, directed)
    adj, mat, od, idg = a
    assert sum(od) == sum(idg) == (len(edges) if directed else 2 * len(edges))
    if not directed:
        assert od == idg and all(mat[u][v] == mat[v][u] for u in range(n) for v in range(n))
print('600 seeded random graphs: optimal == brute, degree sums = E (directed) or 2E (undirected)')

# memory and query cost, counted in stored cells (not bytes)
def cells(n, e):
    return n * n, n + e          # matrix cells vs list headers + directed entries
for label, n, e in [('sparse n=100 E=99 ', 100, 99), ('dense  n=100 E=4950', 100, 4950)]:
    m, l = cells(n, e)
    print(f'{label}: matrix cells {m:6d} | adjacency list slots about {l + e:6d} (n + 2E undirected)')

# is-edge query: matrix is O(1); a list is O(deg(u)); a dict-of-dict (or set) per node is O(1) on average
n = 100
edges = [[0, v, 1] for v in range(1, n)]
adj, mat, _, _ = build(n, edges, False)
print('hub node 0 has degree', len(adj[0]), '| matrix[0][99] =', mat[0][99], '| list scan finds 99 after', 1 + [v for v, _ in adj[0]].index(99), 'probes')
nbr = {u: {v: w for v, w in adj[u]} for u in range(n)}
print('dict-of-dict lookup nbr[0].get(99):', nbr[0].get(99))
print('edge cases: n=0 and n=2 with no edges asserted above; a 100x100 matrix always stores', 100 * 100, 'cells even with 99 edges')
