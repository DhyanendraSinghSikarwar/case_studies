import itertools
import random
import sys
from collections import deque

random.seed(2)

def adj_of(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    return adj

def optimal(n, edges, start):
    adj = adj_of(n, edges)
    # BFS: mark on enqueue, so a node is never in the queue twice
    seen = {start}; q = deque([start]); bfs = []
    while q:
        u = q.popleft(); bfs.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    # DFS: mark on pop; push neighbours in reverse so the first neighbour is popped first
    done = set(); stack = [start]; dfs = []
    while stack:
        u = stack.pop()
        if u in done:
            continue                      # a stale duplicate
        done.add(u); dfs.append(u)
        for v in reversed(adj[u]):
            stack.append(v)
    return [bfs, dfs]

def brute(n, edges, start):
    """Recursive DFS and level-by-level BFS with lists (fine for tiny n only)."""
    adj = adj_of(n, edges); dfs = []; seen = set()
    def go(u):
        seen.add(u); dfs.append(u)
        for v in adj[u]:
            if v not in seen:
                go(v)
    go(start)
    dist = {start: 0}; level = [start]; bfs = []
    while level:
        bfs += level; nxt = []
        for u in level:
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1; nxt.append(v)
        level = nxt
    return [bfs, dfs]

def dfs_mark_on_push(n, edges, start):
    """The tempting variant: mark when pushed. It is a valid DFS-like order but NOT the recursive preorder."""
    adj = adj_of(n, edges); seen = {start}; stack = [start]; out = []
    while stack:
        u = stack.pop(); out.append(u)
        for v in reversed(adj[u]):
            if v not in seen:
                seen.add(v); stack.append(v)
    return out

assert optimal(5, [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]], 0) == [[0, 1, 2, 3, 4], [0, 1, 3, 2, 4]]
assert optimal(4, [[0, 1], [2, 3]], 2) == [[2, 3], [2, 3]]
assert optimal(1, [], 0) == [[0], [0]]
print('3 prompt examples ok')

for _ in range(800):
    n = random.randint(1, 8)
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    random.shuffle(pairs)
    edges = [list(p) if random.random() < .5 else [p[1], p[0]] for p in pairs[:random.randint(0, len(pairs))]]
    s = random.randrange(n)
    assert optimal(n, edges, s) == brute(n, edges, s), (n, edges, s)
print('800 seeded random graphs: iterative == recursive preorder / level BFS')

# exhaustive: every simple graph on 4 nodes (64 edge subsets, fixed edge order), every start
pairs = [(u, v) for u in range(4) for v in range(u + 1, 4)]
cnt = 0; diff = None
for mask in range(1 << len(pairs)):
    edges = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    for s in range(4):
        assert optimal(4, edges, s) == brute(4, edges, s)
        cnt += 1
        if diff is None and dfs_mark_on_push(4, edges, s) != optimal(4, edges, s)[1]:
            diff = (edges, s, dfs_mark_on_push(4, edges, s), optimal(4, edges, s)[1])
print('exhaustive on all', cnt, '(graph, start) pairs of 4 nodes: ok')
print('mark-on-push DFS differs from the recursive preorder, e.g. edges, start, push-order, true preorder:', diff)

# scale: a path of 10^5 nodes, iterative is fine; recursion would need depth 10^5
n = 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
b, d = optimal(n, path, 0)
assert b == d == list(range(n))
print('10^5-node path ok, default recursion limit is', sys.getrecursionlimit())
try:
    brute(5000, path[:4999], 0)
except RecursionError:
    print('recursive DFS on a 5000-node path: RecursionError (limit 1000)')

# why deque: list.pop(0) shifts the whole list each time (O(n) per pop); deque.popleft is O(1)
q = list(range(10)); assert q.pop(0) == 0
dq = deque(range(10)); assert dq.popleft() == 0
assert optimal(3, [[0, 1]], 2) == [[2], [2]]    # isolated start sees only itself
print('isolated start, n=1 and disconnected graphs: only the start component appears')
