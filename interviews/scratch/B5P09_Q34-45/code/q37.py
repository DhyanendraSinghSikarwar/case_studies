import itertools
import random

random.seed(37)

def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def prim_dense(points):
    """O(n^2) Prim: dist[v] = cheapest edge from the tree to v. No heap, no edge list."""
    n = len(points)
    dist = [float('inf')] * n
    used = [False] * n
    dist[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        for i in range(n):                         # linear scan for the closest outside point
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        used[u] = True
        total += dist[u]
        pu = points[u]
        for v in range(n):
            if not used[v]:
                d = abs(pu[0] - points[v][0]) + abs(pu[1] - points[v][1])
                if d < dist[v]:
                    dist[v] = d
    return total

def kruskal_all_pairs(points):
    """Reference: sort all n(n-1)/2 edges, union-find (about 500000 edges when n = 1000)."""
    n = len(points)
    es = sorted((manhattan(points[i], points[j]), i, j) for i in range(n) for j in range(i + 1, n))
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = used = 0
    for w, i, j in es:
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            total += w
            used += 1
    return total

def all_spanning_trees(points):
    """Brute force: every labelled tree via Pruefer sequences (n <= 6). Returns (min weight, how many trees reach it)."""
    n = len(points)
    if n == 1:
        return 0, 1
    if n == 2:
        return manhattan(points[0], points[1]), 1
    best, count = None, 0
    for seq in itertools.product(range(n), repeat=n - 2):
        deg = [1] * n
        for x in seq:
            deg[x] += 1
        edges = []
        for x in seq:
            leaf = min(i for i in range(n) if deg[i] == 1)
            edges.append((leaf, x))
            deg[leaf] -= 1
            deg[x] -= 1
        u, v = [i for i in range(n) if deg[i] == 1]
        edges.append((u, v))
        w = sum(manhattan(points[a], points[b]) for a, b in edges)
        if best is None or w < best:
            best, count = w, 1
        elif w == best:
            count += 1
    return best, count

# ---- examples from the prompt
assert prim_dense([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
assert prim_dense([[3, 12], [-2, 5], [-4, 1]]) == 18
assert prim_dense([[0, 0]]) == 0
print('examples ok')

# ---- the weight is unique, the tree is not: three points, all pairwise distances 2
tie = [[0, 0], [2, 0], [1, 1]]
w, trees = all_spanning_trees(tie)
print('tie example: MST weight', w, 'reached by', trees, 'different trees; Prim returns', prim_dense(tie))
assert (w, trees) == (4, 3)

# ---- seeded cross-check: Prim vs Kruskal on random point sets, and vs ALL spanning trees on tiny ones
def rand_points(n, span):
    seen = set()
    while len(seen) < n:
        seen.add((random.randint(-span, span), random.randint(-span, span)))
    return [list(p) for p in seen]          # set order: shuffle below for a seeded start point
N = 600
for _ in range(N):
    n = random.randint(1, 9)
    pts = rand_points(n, random.choice([2, 5, 20]))
    pts.sort()
    random.shuffle(pts)
    assert prim_dense(pts) == kruskal_all_pairs(pts), pts
print('Prim == Kruskal on', N, 'seeded random point sets (heavy ties on the small grids)')
for _ in range(120):
    n = random.randint(1, 6)
    pts = rand_points(n, 3)
    pts.sort()
    random.shuffle(pts)
    assert prim_dense(pts) == all_spanning_trees(pts)[0], pts
print('Prim == minimum over ALL spanning trees on 120 tiny sets (n <= 6)')
# the start point does not change the weight
pts = rand_points(8, 10)
assert len({prim_dense(pts[i:] + pts[:i]) for i in range(8)}) == 1

# ---- edge cases and max size
assert prim_dense([[0, 0], [0, 1]]) == 1
assert prim_dense([[-10 ** 6, -10 ** 6], [10 ** 6, 10 ** 6]]) == 4 * 10 ** 6
line = [[i, 0] for i in range(10)]
assert prim_dense(line) == 9
big = rand_points(1000, 10 ** 6)
ans = prim_dense(big)
print('n = 1000: Prim weight', ans, '| pairs a Kruskal would have to sort:', 1000 * 999 // 2)
assert ans == kruskal_all_pairs(big)
print('edge cases ok')
