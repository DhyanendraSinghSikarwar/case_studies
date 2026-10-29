import random
from collections import deque

def is_tree(n, edges):                 # optimal: edge count, then union-find with path halving
    if len(edges) != n - 1: return False
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv: return False      # self loop, parallel edge or a longer cycle
        parent[ru] = rv
    return True

def is_tree_brute(n, edges):           # brute force: BFS connectivity + "no cycle" by edge count identity
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)   # a self loop adds u to its own list
    seen = {0}; q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen: seen.add(v); q.append(v)
    return len(seen) == n and len(edges) == n - 1           # connected and exactly n-1 edges

examples = [(5, [[0,1],[0,2],[0,3],[1,4]], True), (5, [[0,1],[1,2],[2,3],[1,3]], False),
            (1, [], True), (2, [[0,1],[0,1]], False)]
for n, e, w in examples:
    assert is_tree(n, e) == is_tree_brute(n, e) == w
print("examples:", [is_tree(n, e) for n, e, _ in examples])

random.seed(14); trues = 0
for _ in range(2000):
    n = random.randint(1, 7); m = random.choice([n - 1, n - 1, random.randint(0, 9)])
    if random.random() < .5 and n > 1:      # build a real tree half the time, then maybe perturb
        e = [[random.randrange(i), i] for i in range(1, n)]
        if random.random() < .3: e[random.randrange(len(e))] = [random.randrange(n), random.randrange(n)]
    else:
        e = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    random.shuffle(e); a = is_tree(n, e); assert a == is_tree_brute(n, e), (n, e); trues += a
print("2000 random small graphs agree with BFS + edge-count check;", trues, "were trees")

# edge cases
assert is_tree(1, []) and not is_tree(1, [[0, 0]])         # lone node ok, self loop is a cycle
assert not is_tree(3, [[0, 1]])                            # too few edges: disconnected
assert not is_tree(4, [[0, 1], [0, 1], [2, 3]])            # n-1 edges but a cycle, so also disconnected
assert not is_tree(3, [])                                  # no edges, n > 1
n = 10**5; path = [[i, i + 1] for i in range(n - 1)]
assert is_tree(n, path)                                    # deep path: no recursion used
assert not is_tree(n, path[:-1] + [[0, n - 2]])            # long path closed into a cycle
assert not is_tree(n, path + [[0, n - 1]])                 # n edges
print("edge asserts ok, including a 10^5-node path")
