import itertools, random
random.seed(14)

def find_redundant(edges):
    n = len(edges)
    parent = list(range(n + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # path halving, iterative
            x = parent[x]
        return x
    for u, v in edges:
        a, b = find(u), find(v)
        if a == b:
            return [u, v]                      # u and v were already connected: this edge closes the cycle
        parent[a] = b

def connected_without(n, edges, skip):
    adj = [[] for _ in range(n + 1)]
    for i, (u, v) in enumerate(edges):
        if i != skip:
            adj[u].append(v); adj[v].append(u)
    seen, stack = {1}, [1]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return len(seen) == n

def brute(edges):                              # try removing each edge from the back; first that leaves a connected graph
    n = len(edges)
    for i in range(n - 1, -1, -1):
        if connected_without(n, edges, i):
            return list(edges[i])

assert find_redundant([[1, 2], [1, 3], [2, 3]]) == [2, 3]
assert find_redundant([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
assert find_redundant([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]) == [1, 3]
print("examples ok")

# exhaustive: every labelled tree on n nodes (Pruefer) + every extra edge + every edge order, n = 3..5
def prufer_tree(seq, n):
    deg = [1] * (n + 1)
    for x in seq: deg[x] += 1
    out = []
    for x in seq:
        for j in range(1, n + 1):
            if deg[j] == 1:
                out.append([j, x]); deg[j] -= 1; deg[x] -= 1; break
    u, v = [i for i in range(1, n + 1) if deg[i] == 1]
    out.append([u, v]); return out

total = 0
for n in range(3, 6):
    for seq in itertools.product(range(1, n + 1), repeat=n - 2):
        tree = prufer_tree(seq, n)
        have = {frozenset(e) for e in tree}
        for a, b in itertools.combinations(range(1, n + 1), 2):
            if frozenset((a, b)) in have: continue
            base = tree + [[a, b]]
            for perm in itertools.permutations(base):
                es = [list(e) for e in perm]
                r = find_redundant(es)
                assert r == brute(es), es
                total += 1
print("exhaustive n=3..5: %d inputs, union-find answer == last removable edge each time" % total)

# random n = 6..9, including swapping endpoints
for _ in range(500):
    n = random.randint(6, 9)
    tree = [[random.randint(1, i), i + 1] for i in range(1, n)]
    have = {frozenset(e) for e in tree}
    while True:
        a, b = random.sample(range(1, n + 1), 2)
        if frozenset((a, b)) not in have: break
    es = tree + [[a, b]]; random.shuffle(es)
    es = [e if random.random() < .5 else e[::-1] for e in es]
    assert find_redundant(es) == brute(es)
print("500 random n=6..9 cases ok")

# every edge on the cycle qualifies, so 'last in the list' is a real tie-break
es = [[1, 2], [2, 3], [3, 1], [3, 4]]
ok = [e for i, e in enumerate(es) if connected_without(4, es, i)]
print("removable edges:", ok, "-> answer", find_redundant(es))
assert ok == [[1, 2], [2, 3], [3, 1]] and find_redundant(es) == [3, 1]

# largest allowed size is small (n <= 1000), but the scan is O(n * alpha) anyway
n = 1000
big = [[i, i + 1] for i in range(1, n)] + [[1, n]]
assert find_redundant(big) == [1, n]
print("n=1000 path plus closing edge ok")
