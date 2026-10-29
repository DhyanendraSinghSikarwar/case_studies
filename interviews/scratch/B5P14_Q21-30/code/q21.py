import heapq, random
from itertools import permutations

def optimal(n, edges):
    """Kahn's algorithm with a min-heap: lexicographically smallest topological order, or [] on a cycle."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in edges:                      # repeated edges are counted twice in indeg and twice in adj: consistent
        adj[a].append(b)
        indeg[b] += 1
    heap = [v for v in range(n) if indeg[v] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        v = heapq.heappop(heap)             # smallest available node
        order.append(v)
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                heapq.heappush(heap, w)
    return order if len(order) == n else []

def brute(n, edges):
    """Try permutations in lexicographic order, keep the first that respects every edge."""
    for p in permutations(range(n)):        # itertools yields lexicographic order for a sorted input
        pos = {v: i for i, v in enumerate(p)}
        if all(pos[a] < pos[b] for a, b in edges):
            return list(p)
    return []

def labels_early(n, edges):
    """'label 0 as early as possible, then label 1, ...': reverse the graph, take the LARGEST available, reverse."""
    adj = [[] for _ in range(n)]
    outdeg = [0] * n
    for a, b in edges:
        adj[b].append(a)                    # reversed edge
        outdeg[a] += 1
    heap = [-v for v in range(n) if outdeg[v] == 0]
    heapq.heapify(heap)
    rev = []
    while heap:
        v = -heapq.heappop(heap)            # largest available in the reversed graph
        rev.append(v)
        for w in adj[v]:
            outdeg[w] -= 1
            if outdeg[w] == 0:
                heapq.heappush(heap, -w)
    return rev[::-1] if len(rev) == n else []

def labels_brute(n, edges):
    """Minimise the vector (position of 0, position of 1, ...) over all valid orders."""
    best = None
    for p in permutations(range(n)):
        pos = [0] * n
        for i, v in enumerate(p):
            pos[v] = i
        if all(pos[a] < pos[b] for a, b in edges):
            if best is None or pos < best[0]:
                best = (pos, list(p))
    return best[1] if best else []

# examples from the prompt
assert optimal(4, [[3, 0], [3, 1], [1, 2]]) == [3, 0, 1, 2]
assert optimal(3, [[0, 1], [1, 2], [2, 0]]) == []
assert optimal(3, []) == [0, 1, 2]
print('examples:', optimal(4, [[3, 0], [3, 1], [1, 2]]), optimal(3, [[0, 1], [1, 2], [2, 0]]), optimal(3, []))

# why the other goal needs the reverse trick: smallest-first is NOT optimal for 'label 0 early'
n, e = 3, [[2, 0]]
print('smallest-first:', optimal(n, e), ' label-0-early (brute):', labels_brute(n, e), ' reverse+largest:', labels_early(n, e))
assert optimal(n, e) == [1, 2, 0] and labels_brute(n, e) == [2, 0, 1] == labels_early(n, e)

# edge cases
assert optimal(1, []) == [0]
assert optimal(1, [[0, 0]]) == []                       # self loop is a cycle
assert optimal(3, [[0, 1], [0, 1], [1, 2]]) == [0, 1, 2]  # repeated edges
assert optimal(2, [[1, 0]]) == [1, 0]

random.seed(21)
cases = 0
for _ in range(600):
    n = random.randint(1, 6)
    m = random.randint(0, 9)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    if random.random() < 0.7:                           # mostly acyclic: orient along a hidden permutation
        perm = list(range(n)); random.shuffle(perm)
        rank = {v: i for i, v in enumerate(perm)}
        edges = [[a, b] if rank[a] < rank[b] else [b, a] for a, b in edges if a != b]
    assert optimal(n, edges) == brute(n, edges), (n, edges)
    assert labels_early(n, edges) == labels_brute(n, edges), (n, edges)
    cases += 1
print('random cross-check ok:', cases, 'cases (n <= 6), both rules')

# size: a path 0 <- 1 <- ... (reverse chain) and a wide fan; iterative so no recursion issue
N = 10**5
chain = [[i + 1, i] for i in range(N - 1)]
assert optimal(N, chain) == list(range(N - 1, -1, -1))
fan = [[0, i] for i in range(1, N)]
assert optimal(N, fan) == list(range(N))
print('n = 10^5 chain and fan ok')
