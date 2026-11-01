import random
from itertools import combinations

def optimal(n, built, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    comps = n
    for u, v in built:                       # free roads first: contract them
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; comps -= 1
    cost = 0
    for u, v, c in sorted(edges, key=lambda e: e[2]):
        if comps == 1:
            break
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; comps -= 1; cost += c
    return cost if comps == 1 else -1

def connected(n, pairs):
    parent = list(range(n))
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    for u, v in pairs:
        parent[find(u)] = find(v)
    return len({find(x) for x in range(n)}) == 1

def brute(n, built, edges):
    best = None
    for mask in range(1 << len(edges)):
        chosen = [edges[i] for i in range(len(edges)) if mask >> i & 1]
        if connected(n, list(built) + [(u, v) for u, v, _ in chosen]):
            c = sum(e[2] for e in chosen)
            if best is None or c < best: best = c
    return -1 if best is None else best

assert optimal(4, [[0, 1]], [[1, 2, 5], [2, 3, 1], [0, 3, 9], [0, 2, 4]]) == 5
assert optimal(3, [], [[0, 1, 2]]) == -1
assert optimal(1, [], []) == 0
print('examples:', optimal(4, [[0, 1]], [[1, 2, 5], [2, 3, 1], [0, 3, 9], [0, 2, 4]]), optimal(3, [], [[0, 1, 2]]), optimal(1, [], []))

# edge cases: already connected by built roads, so candidates cost nothing; duplicates; self loop candidate
assert optimal(3, [[0, 1], [1, 2]], [[0, 2, 7]]) == 0
assert optimal(2, [], [[0, 1, 9], [0, 1, 4], [1, 1, 1]]) == 4
assert optimal(3, [[0, 1]], [[1, 2, 6], [0, 2, 3]]) == 3

random.seed(29)
for _ in range(600):
    n = random.randint(1, 6)
    built = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 3))]
    edges = [[random.randrange(n), random.randrange(n), random.randint(1, 9)] for _ in range(random.randint(0, 9))]
    assert optimal(n, built, edges) == brute(n, built, edges), (n, built, edges)
print('random cross-check ok: 600 cases against all subsets of <= 9 candidates')

# why contraction is needed: without pre-merging, Kruskal wastes budget on a road that is already implied
n, built, edges = 3, [[0, 1]], [[0, 1, 1], [1, 2, 5]]
print('with free road 0-1, answer =', optimal(n, built, edges), '(buying the cost-1 duplicate would add 1 for nothing)')
assert optimal(n, built, edges) == 5

N = 10**4
edges = [[i, i + 1, random.randint(1, 10**6)] for i in range(N - 1)] + [[random.randrange(N), random.randrange(N), random.randint(1, 10**6)] for _ in range(4 * 10**4)]
print('n = 10^4, 5*10^4 candidates -> cost', optimal(N, [], edges))
