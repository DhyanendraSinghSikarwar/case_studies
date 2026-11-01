import itertools, random
from collections import deque
random.seed(21)

def is_bipartite(graph):
    n = len(graph)
    color = [-1] * n                           # -1 unseen, 0 / 1 the two sides
    for s in range(n):                         # restart from every unseen node: the graph may be disconnected
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:     # an edge inside one side: an odd cycle exists
                    return False
    return True

def brute(graph):                              # try every 2-colouring
    n = len(graph)
    return any(all(c[u] != c[v] for u in range(n) for v in graph[u]) for c in itertools.product((0, 1), repeat=n))

def has_odd_cycle(graph):                      # independent test: BFS layers; an edge inside a layer means an odd cycle
    n = len(graph); dist = [-1] * n
    for s in range(n):
        if dist[s] != -1: continue
        dist[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if dist[v] == -1: dist[v] = dist[u] + 1; q.append(v)
    return any(dist[u] == dist[v] for u in range(n) for v in graph[u])

assert is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True
assert is_bipartite([[1, 2], [0, 2], [0, 1]]) is False
assert is_bipartite([[], []]) is True
assert is_bipartite([[1], [0], [3], [2]]) is True
print("examples ok: True False True True")

cnt = tot_false = 0
for n in range(1, 6):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        g = [[] for _ in range(n)]
        for k, (a, b) in enumerate(pairs):
            if mask >> k & 1:
                g[a].append(b); g[b].append(a)
        r = is_bipartite(g)
        assert r == brute(g) == (not has_odd_cycle(g))
        cnt += 1; tot_false += not r
print("exhaustive: all %d graphs on n <= 5 nodes agree with brute force and the odd-cycle test (%d not bipartite)" % (cnt, tot_false))

for _ in range(300):
    n = random.randint(1, 10)
    es = {(a, b) for a, b in (sorted(random.sample(range(n), 2)) for _ in range(random.randint(0, 12)) if n > 1)}
    g = [[] for _ in range(n)]
    for a, b in es:
        g[a].append(b); g[b].append(a)
    assert is_bipartite(g) == brute(g)
print("300 random n <= 10 graphs ok")

# disconnected: a bipartite component first, an odd cycle in a later component
assert is_bipartite([[1], [0], [3, 4], [2, 4], [2, 3]]) is False

# scale: n = 1e5, iterative
n = 10**5
path = [[] for _ in range(n)]
for i in range(n - 1):
    path[i].append(i + 1); path[i + 1].append(i)
assert is_bipartite(path) is True
odd = [[] for _ in range(n)]
m = n - 1                                      # cycle on 99,999 nodes (odd), one isolated node
for i in range(m):
    j = (i + 1) % m
    odd[i].append(j); odd[j].append(i)
assert is_bipartite(odd) is False
even = [[] for _ in range(n)]
for i in range(n):
    j = (i + 1) % n
    even[i].append(j); even[j].append(i)
assert is_bipartite(even) is True
print("n=1e5: path True, odd cycle (99999) False, even cycle (100000) True")
