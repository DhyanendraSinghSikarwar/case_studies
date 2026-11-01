import itertools, random, sys
from collections import deque
random.seed(19)

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_bfs(node):
    if node is None:
        return None
    copy_of = {node: Node(node.val)}          # original -> copy, doubles as the visited set
    q = deque([node])
    while q:
        u = q.popleft()
        for v in u.neighbors:
            if v not in copy_of:
                copy_of[v] = Node(v.val)
                q.append(v)
            copy_of[u].neighbors.append(copy_of[v])
    return copy_of[node]

def clone_dfs(node):                          # depth <= 100 nodes, so recursion is safe here
    if node is None:
        return None
    copy_of = {}
    def go(u):
        c = copy_of[u] = Node(u.val)
        for v in u.neighbors:
            if v not in copy_of:
                go(v)
            c.neighbors.append(copy_of[v])
    go(node)
    return copy_of[node]

def clone_without_map(node, depth=0):         # the broken idea: no dictionary, so cycles never stop
    c = Node(node.val)
    c.neighbors = [clone_without_map(v, depth + 1) for v in node.neighbors]
    return c

# ---- checker, as the prompt describes
def build(adj):
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, lst in enumerate(adj):
        nodes[i].neighbors = [nodes[v - 1] for v in lst]
    return nodes

def run_checker(adj, fn):
    if not adj:
        return [] if fn(None) is None else 'expected None'
    nodes = build(adj)
    originals = {id(x) for x in nodes}
    root = fn(nodes[0])
    seen, q, out = {root.val: root}, deque([root]), {}
    while q:
        u = q.popleft()
        assert id(u) not in originals, 'copy shares a node with the original'
        out[u.val] = [v.val for v in u.neighbors]
        for v in u.neighbors:
            if v.val not in seen:
                seen[v.val] = v
                q.append(v)
    assert len(seen) == len(adj)
    return [out[i] for i in range(1, len(adj) + 1)]

for adj in ([[2, 4], [1, 3], [2, 4], [1, 3]], [[]], [], [[2], [1, 3], [2]]):
    assert run_checker(adj, clone_bfs) == adj == run_checker(adj, clone_dfs)
print("examples ok")

# exhaustive: every connected simple graph on n <= 5 nodes (neighbour lists in ascending order)
cnt = 0
for n in range(1, 6):
    pairs = list(itertools.combinations(range(1, n + 1), 2))
    for mask in range(1 << len(pairs)):
        adj = [[] for _ in range(n)]
        for k, (a, b) in enumerate(pairs):
            if mask >> k & 1:
                adj[a - 1].append(b); adj[b - 1].append(a)
        seen, st = {1}, [1]
        while st:
            u = st.pop()
            for v in adj[u - 1]:
                if v not in seen: seen.add(v); st.append(v)
        if len(seen) != n:
            continue
        assert run_checker(adj, clone_bfs) == adj and run_checker(adj, clone_dfs) == adj
        cnt += 1
print("exhaustive: %d connected graphs with n <= 5, BFS and DFS clones both reproduce adj, no shared nodes" % cnt)

# random neighbour ORDER and up to 100 nodes (order of neighbours must be preserved)
for _ in range(200):
    n = random.randint(1, 100)
    edges = {(random.randrange(i), i) for i in range(1, n)}
    for _ in range(random.randint(0, n)):
        a, b = random.sample(range(n), 2) if n > 1 else (0, 0)
        if a != b: edges.add((min(a, b), max(a, b)))
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b + 1); adj[b].append(a + 1)
    for l in adj: random.shuffle(l)
    assert run_checker(adj, clone_bfs) == adj and run_checker(adj, clone_dfs) == adj
print("200 random connected graphs (n <= 100, shuffled neighbour order) ok")

# why the dictionary: copying without it on a 2-node cycle recurses forever
a, b = Node(1), Node(2); a.neighbors = [b]; b.neighbors = [a]
try:
    clone_without_map(a)
except RecursionError:
    print("no map on a 2-node cycle: RecursionError (limit %d)" % sys.getrecursionlimit())
# a copy with a map: the clone is a different object but has the same shape
c = clone_bfs(a)
assert c is not a and c.neighbors[0] is not b and c.neighbors[0].neighbors[0] is c
print("clone is a real cycle: c.neighbors[0].neighbors[0] is c ->", c.neighbors[0].neighbors[0] is c)
