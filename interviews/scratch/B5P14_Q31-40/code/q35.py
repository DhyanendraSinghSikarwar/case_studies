import random

random.seed(3501)


def find_redundant_directed(edges):
    n = len(edges)
    parent = [0] * (n + 1)
    cand1 = cand2 = None                       # cand1: earlier edge into a 2-parent node; cand2: the later one
    for u, v in edges:
        if parent[v]:
            cand1, cand2 = [parent[v], v], [u, v]
        else:
            parent[v] = u
    uf = list(range(n + 1))

    def find(x):
        while uf[x] != x:
            uf[x] = uf[uf[x]]
            x = uf[x]
        return x
    cycle_edge = None
    for u, v in edges:
        if cand2 is not None and [u, v] == cand2:      # pretend the later candidate is not there
            continue
        a, b = find(u), find(v)
        if a == b:
            cycle_edge = [u, v]                        # first edge that closes a cycle
            break
        uf[b] = a
    if cand2 is None:                                  # case 2: no node has two parents -> pure cycle
        return cycle_edge
    return cand1 if cycle_edge else cand2              # case 1: cycle left => earlier candidate, else later


def is_rooted_tree(n, edges):
    indeg = [0] * (n + 1)
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        indeg[v] += 1
        g[u].append(v)
    roots = [v for v in range(1, n + 1) if indeg[v] == 0]
    if len(roots) != 1 or any(indeg[v] > 1 for v in range(1, n + 1)):
        return False
    seen, q = {roots[0]}, [roots[0]]
    for u in q:
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == n


def brute(edges):
    """Drop each edge from the last to the first; the first removal leaving a rooted tree is the answer."""
    n = len(edges)
    for i in range(n - 1, -1, -1):
        if is_rooted_tree(n, edges[:i] + edges[i + 1:]):
            return list(edges[i])


def random_instance(n):
    """Random rooted tree on 1..n plus one extra directed edge (no repeat, no self loop), shuffled."""
    order = list(range(1, n + 1))
    random.shuffle(order)
    edges = [[order[random.randrange(i)], order[i]] for i in range(1, n)]
    while True:
        u, v = random.randint(1, n), random.randint(1, n)
        if u != v and [u, v] not in edges:
            break
    edges.append([u, v])
    random.shuffle(edges)
    return edges


# --- the prompt's examples ---
ex = [([[1, 2], [1, 3], [2, 3]], [2, 3]),
      ([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]], [4, 1]),
      ([[2, 1], [3, 1], [4, 2], [1, 4]], [2, 1])]
for e, want in ex:
    got = find_redundant_directed(e)
    print(e, '->', got)
    assert got == want == brute(e)

# --- random cross-check ---
kinds = {'two parents, no cycle': 0, 'two parents + cycle': 0, 'cycle only': 0}
for _ in range(3000):
    e = random_instance(random.randint(3, 8))
    got = find_redundant_directed(e)
    assert got == brute(e), e
    indeg = {}
    for u, v in e:
        indeg[v] = indeg.get(v, 0) + 1
    if max(indeg.values()) < 2:
        kinds['cycle only'] += 1
    else:
        v2 = next(v for v, c in indeg.items() if c == 2)
        first, second = [x for x in e if x[1] == v2]          # in input order
        kinds['two parents + cycle' if got == first else 'two parents, no cycle'] += 1
print('random cases passed: 3000;', kinds)

# --- edge cases ---
assert find_redundant_directed([[1, 2], [2, 3], [3, 1]]) == [3, 1]            # n = 3, pure 3-cycle
assert find_redundant_directed([[1, 2], [1, 3], [3, 2]]) == [3, 2]            # later parent wins when no cycle
assert find_redundant_directed([[1, 2], [2, 1], [1, 3]]) == [2, 1]            # 2-cycle through the root
n = 1000
long = [[i, i + 1] for i in range(1, n)] + [[n, 1]]                           # n = 1000 ring
assert find_redundant_directed(long) == [n, 1]
assert find_redundant_directed([[i, i + 1] for i in range(1, n - 1)] + [[1, n - 1]]) == [1, n - 1]  # node n-1 has parents n-2 and 1; both removals work -> the later edge
print('edge asserts passed')
