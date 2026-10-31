### Q1 ⭐⭐⭐ 🟢 Graph representations: build an adjacency list, an adjacency matrix and degree arrays from an edge list. `n` nodes are numbered 0..n-1 (0 <= n <= 100) and `edges` is a list of [u, v, w] with integer weight 1 <= w <= 99; there are no self loops and no repeated edges (for an undirected graph [u, v] and [v, u] are the same edge and do not both appear). If `directed` is true each edge goes u -> v only; otherwise it is undirected. Return `[adj, matrix, out_deg, in_deg]`: `adj[u]` is the list of [v, w] pairs in the order the edges were given (for an undirected edge, u gets v and v gets u, each at the position of that edge), `matrix[u][v]` is w or 0 if there is no edge (undirected edges fill both cells), and `out_deg`/`in_deg` count edges leaving/entering each node (equal for undirected graphs). Also state the memory of each representation, the cost of asking 'is there an edge u-v', and of listing the neighbours of u, for sparse and dense graphs. Example: n=4, edges=[[0, 1, 5], [0, 2, 3], [2, 3, 1]], directed=True -> [[[[1, 5], [2, 3]], [], [[3, 1]], []], [[0, 5, 3, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]], [2, 0, 1, 0], [0, 1, 1, 1]]; n=3, edges=[[0, 1, 2], [1, 2, 7]], directed=False -> [[[[1, 2]], [[0, 2], [2, 7]], [[1, 7]]], [[0, 2, 0], [2, 0, 7], [0, 7, 0]], [1, 2, 1], [1, 2, 1]]; n=0, edges=[], directed=False -> [[], [], [], []]; n=2, edges=[], directed=True -> [[[], []], [[0, 0], [0, 0]], [0, 0], [0, 0]].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Graph representation. Pick the storage first (adjacency list, adjacency matrix, edge list), then every algorithm after it is just a loop over neighbours.

**Say this first (1 line):** "An adjacency list stores only the edges that exist, so it is O(V + E); a matrix stores every pair, so it is O(V^2) but answers 'is there an edge' in O(1). For sparse graphs I use lists."

**Brute force:** Build the matrix first, then read the lists and degrees off it: for each node scan a whole row (n cells), for each in-degree scan a whole column. That is O(n^2) for the scans, even when the graph has 3 edges. It is fine for n <= 100, but it is the wrong habit.

**Optimal:**
- One pass over the edge list. For each `[u, v, w]`: append `[v, w]` to `adj[u]`, set `mat[u][v] = w`, bump `out_deg[u]` and `in_deg[v]`.
- If undirected, do the mirror image too: `adj[v]` gets `[u, w]`, `mat[v][u] = w`, and `out_deg[v]`, `in_deg[u]` go up. So degrees are equal.
- Order rule: neighbours are in edge-input order, not id order. Appending as you read gives that for free.
- Invariant: after k edges, every structure describes exactly the first k edges.
- Zero as "no edge" works only because weights are 1..99. If weight 0 were legal, use `None` or `inf` in the matrix.

| | Memory | Is edge u-v? | List neighbours of u |
|---|---|---|---|
| Adjacency list | O(V + E) | O(deg(u)) by scan; O(1) average if each node holds a dict/set | O(deg(u)) |
| Adjacency matrix | O(V^2) | O(1) | O(V): scan the row |
| Edge list | O(E) | O(E) | O(E) |

- Sparse (E about V): list is about 3V slots, matrix is V^2. For V = 10^5 a matrix is 10^10 cells: impossible. The list is trivial.
- Dense (E about V^2/2): both are Theta(V^2); the matrix has smaller constants and O(1) edge tests, and suits Floyd-Warshall.

**Complexity:** Time O(n^2 + E) here only because the output includes an n x n matrix; the lists and degrees alone take O(n + E). Space O(n^2 + E) for the returned structures.

**Dry run:** `n=3, edges=[[0,1,2],[1,2,7]]`, undirected.
- Edge `[0,1,2]`: `adj[0]=[[1,2]]`, `adj[1]=[[0,2]]`, `mat[0][1]=mat[1][0]=2`, degrees `[1,1,0]`.
- Edge `[1,2,7]`: `adj[1]=[[0,2],[2,7]]`, `adj[2]=[[1,7]]`, `mat[1][2]=mat[2][1]=7`, degrees `[1,2,1]`.
- Result matches the prompt: degrees `[1,2,1]` both ways.

**Code:**
```python
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
```

**Output (my run):**
```
4 prompt examples ok
adj[1] for edges [3,1],[1,0]: [[3, 4], [0, 6]]
600 seeded random graphs: optimal == brute, degree sums = E (directed) or 2E (undirected)
sparse n=100 E=99 : matrix cells  10000 | adjacency list slots about    298 (n + 2E undirected)
dense  n=100 E=4950: matrix cells  10000 | adjacency list slots about  10000 (n + 2E undirected)
hub node 0 has degree 99 | matrix[0][99] = 1 | list scan finds 99 after 99 probes
dict-of-dict lookup nbr[0].get(99): 1
edge cases: n=0 and n=2 with no edges asserted above; a 100x100 matrix always stores 10000 cells even with 99 edges
```

**Edge cases:**
- `n=0`: four empty lists. `n>0` with no edges: empty adjacency lists, zero matrix.
- Directed graph where `u -> v` and `v -> u` are two different edges (both allowed).
- Undirected edge given as `[v, u]` instead of `[u, v]`: same graph, different neighbour order.
- Weight 0 as 'no edge' is a trap if weights can be 0.

**Follow-ups:**
- *Which for Dijkstra on a road network?* Adjacency list: sparse, and you iterate neighbours.
- *Which for Floyd-Warshall?* Matrix: it needs `d[i][j]` for all pairs anyway.
- *Parallel edges?* A matrix cannot hold two weights; a list can. Say so before coding.

**Common mistakes:**
- Filling only one direction for an undirected edge.
- Counting an undirected edge once in the degrees.
- `[[0] * n] * n` for the matrix: every row is the same list object.
- Saying 'adjacency list edge test is O(1)'. It is O(deg) unless each node keeps a set or dict.

### Q2 ⭐⭐⭐ 🟢 BFS and DFS orders, iterative. `edges` is a list of [u, v] undirected edges on nodes 0..n-1 (1 <= n <= 10^5, no self loops or repeats) and `start` is a node. Build adjacency lists with neighbours in edge-input order (edge [u, v] appends v to u's list and u to v's list), then return `[bfs, dfs]`: `bfs` is the order nodes are dequeued by a breadth-first search that marks a node when it is enqueued, and `dfs` is the preorder of a recursive depth-first search that tries neighbours in list order, but you must produce it iteratively (an explicit stack; push each node's neighbours in reverse list order and mark a node visited when it is popped, skipping already-visited pops). Only nodes reachable from `start` appear. Use `collections.deque` for the queue, not `list.pop(0)` (see Part 4 Q4 for the cost difference, and Part 4 Q30 for the level-order queue idiom); state the time and space of both traversals. Example: n=5, edges=[[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]], start=0 -> [[0, 1, 2, 3, 4], [0, 1, 3, 2, 4]]; n=4, edges=[[0, 1], [2, 3]], start=2 -> [[2, 3], [2, 3]]; n=1, edges=[], start=0 -> [[0], [0]].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Graph traversal. BFS uses a queue (nearest first), DFS uses a stack (deepest first). Both visit each node once.

**Say this first (1 line):** "BFS: deque, mark when enqueued. DFS iterative: stack, push neighbours in reverse, mark when popped, skip stale pops. Both are O(V + E)."

**Brute force:** Recursive DFS plus a level-by-level BFS with Python lists. Same answers, but recursion dies at depth 1000 (the default limit), and a BFS built on `list.pop(0)` shifts the whole list on each pop, so it is O(V^2) in the worst case (see Part 4 Q4 for list versus deque and Part 4 Q30 for the level-order queue idiom).

**Optimal:**
- Build adjacency lists in edge-input order.
- BFS: `seen = {start}`, `deque([start])`. Pop left, append to the order, enqueue unseen neighbours and mark them right then. Marking on enqueue keeps every node in the queue at most once.
- DFS: stack starts as `[start]`. Pop `u`; if `u` is already done, skip it. Otherwise mark it, record it, push neighbours in reverse list order, so the first neighbour is popped next.
- Why mark on pop here: that reproduces the recursive preorder exactly. A node can sit on the stack several times; only its first pop counts.
- The tempting 'mark on push' version is a different order: in the code, edges `[[0,1],[0,2],[0,3],[1,2]]` from start 1 give `[1,0,3,2]` instead of the recursive `[1,0,2,3]`. Exhaustive check over all 4-node graphs finds such cases.
- Invariant (BFS): nodes leave the queue in non-decreasing distance. Invariant (DFS): the stack top is the next node the recursive version would visit.

**Complexity:** Time O(V + E) for both: each node is processed once and each adjacency entry is looked at once (the DFS stack can hold up to E entries, because stale duplicates stay until popped). Space O(V + E) for the adjacency lists, plus O(V) for the queue or O(E) for the stack, plus the seen set.

**Dry run:** `edges=[[0,1],[0,2],[1,3],[2,3],[3,4]]`, start 0. Adjacency: `0:[1,2]`, `1:[0,3]`, `2:[0,3]`, `3:[1,2,4]`, `4:[3]`.
- BFS: queue `[0]`; pop 0, enqueue 1, 2; pop 1, enqueue 3; pop 2 (3 already seen); pop 3, enqueue 4; pop 4. Order `[0,1,2,3,4]`.
- DFS: stack `[0]`. Pop 0, record, push 2 then 1: stack `[2,1]`.
- Pop 1, record, push 3 then 0: stack `[2,3,0]`. Pop 0: stale, skip.
- Pop 3, record, push 4, 2, 1: stack `[2,4,2,1]`. Pop 1: stale. Pop 2, record, push 3, 0: stack `[2,4,3,0]`.
- Pop 0, pop 3: stale. Pop 4, record, push 3: stale. Pop 2: stale. Order `[0,1,3,2,4]`, as in the prompt.

**Code:**
```python
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
```

**Output (my run):**
```
3 prompt examples ok
800 seeded random graphs: iterative == recursive preorder / level BFS
exhaustive on all 256 (graph, start) pairs of 4 nodes: ok
mark-on-push DFS differs from the recursive preorder, e.g. edges, start, push-order, true preorder: ([[0, 1], [0, 2], [0, 3], [1, 2]], 1, [1, 0, 3, 2], [1, 0, 2, 3])
10^5-node path ok, default recursion limit is 1000
recursive DFS on a 5000-node path: RecursionError (limit 1000)
isolated start, n=1 and disconnected graphs: only the start component appears
```

**Edge cases:**
- Start node with no edges: only itself appears.
- `n=1`: `[[0],[0]]`.
- Disconnected graph: only the start's component is returned; do not loop over all starts.
- Path of 10^5 nodes: the iterative DFS is fine; recursion would need depth 10^5.

**Follow-ups:**
- *Why not recursion?* Depth up to V; CPython allows about 1000 frames. `sys.setrecursionlimit` risks a C-stack crash; iterate.
- *Get shortest hop counts?* Store `dist` in BFS (Q7).
- *All components?* Loop over every unseen node and start a traversal (Q3).

**Common mistakes:**
- `list.pop(0)` as the BFS queue.
- Marking on dequeue in BFS: nodes get queued many times.
- Pushing neighbours in forward order and getting the mirror-image DFS order.
- Marking on push in the DFS and silently changing the order.

### Q3 ⭐⭐⭐ 🟢 Connected components of an undirected graph. `n` nodes numbered 0..n-1 (0 <= n <= 10^5) and `edges` a list of [u, v] (0 <= len <= 2*10^5; repeated edges and self loops are allowed and harmless). Return the list of components, each as an ascending list of its nodes, with the components ordered by their smallest node. Solve it with an iterative traversal and say how a union-find gives the same count; state the time and space. Example: n=6, edges=[[0, 1], [1, 2], [3, 4]] -> [[0, 1, 2], [3, 4], [5]]; n=3, edges=[] -> [[0], [1], [2]]; n=0, edges=[] -> []; n=4, edges=[[2, 2], [1, 3], [3, 1]] -> [[0], [1, 3], [2]].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Connected components: loop over all nodes; start a traversal at each unseen one; each traversal is one component.

**Say this first (1 line):** "I scan nodes 0..n-1; each unseen node starts an iterative DFS that collects its component. O(V + E). Union-find gives the same count as n minus successful unions."

**Brute force:** Label propagation: give every node its own label, then keep sweeping the edge list lowering both endpoints to the smaller label until a sweep changes nothing. Worst case about V sweeps of E edges, O(V * E). Used in the code as the checker.

**Optimal:**
- Adjacency lists (repeats and self loops are harmless: a repeat finds the neighbour already seen, a self loop finds the node itself seen).
- For `s` in `0..n-1`: if unseen, mark it, push on a stack, pop and collect, push unseen neighbours (mark on push).
- Sort each component (or, equivalently, post-sort) to get ascending lists. Because `s` ascends and the first node of a component found is its smallest, components come out ordered by smallest node.
- Union-find alternative: start with `n` sets; each `union(u, v)` that joins two different sets lowers the count by 1. Final count = components. Group by root to list the members.
- Invariant: when the outer loop reaches `s`, every node in an earlier component is already marked.

**Complexity:** Time O(V + E) plus O(V log V) total for sorting the members. Space O(V + E). Union-find: O((V + E) alpha(V)), where alpha (inverse Ackermann) is below 5 for any real input.

**Dry run:** `n=6, edges=[[0,1],[1,2],[3,4]]`.
- s=0 unseen: collect 0, 1, 2. Component `[0,1,2]`.
- s=1, 2 seen. s=3: collect 3, 4: `[3,4]`. s=4 seen. s=5: `[5]`.
- Union-find: 6 sets; unions (0,1), (1,2), (3,4) all succeed, so 6 - 3 = 3 sets.

**Code:**
```python
import random

random.seed(3)

def components(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    seen = [False] * n; out = []
    for s in range(n):                      # scanning in ascending order = components ordered by smallest node
        if seen[s]:
            continue
        seen[s] = True; stack = [s]; comp = []
        while stack:
            u = stack.pop(); comp.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True; stack.append(v)
        out.append(sorted(comp))
    return out

def components_dsu(n, edges):
    parent = list(range(n)); size = [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]    # path halving, iterative
            x = parent[x]
        return x
    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            if size[a] < size[b]: a, b = b, a
            parent[b] = a; size[a] += size[b]
    groups = {}
    for x in range(n):
        groups.setdefault(find(x), []).append(x)
    return sorted(groups.values())          # each group ascending already; order by smallest node

def brute(n, edges):
    """Label propagation: keep lowering labels to the neighbour minimum until nothing changes."""
    lab = list(range(n)); changed = True
    while changed:
        changed = False
        for u, v in edges:
            m = min(lab[u], lab[v])
            if lab[u] != m or lab[v] != m:
                lab[u] = lab[v] = m; changed = True
    g = {}
    for i, l in enumerate(lab):
        g.setdefault(l, []).append(i)
    return sorted(g.values())

for f in (components, components_dsu, brute):
    assert f(6, [[0, 1], [1, 2], [3, 4]]) == [[0, 1, 2], [3, 4], [5]]
    assert f(3, []) == [[0], [1], [2]]
    assert f(0, []) == []
    assert f(4, [[2, 2], [1, 3], [3, 1]]) == [[0], [1, 3], [2]]
print('4 prompt examples ok for DFS, union-find and brute force')

for _ in range(800):
    n = random.randint(0, 9)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 10))] if n else []
    a = components(n, edges)
    assert a == components_dsu(n, edges) == brute(n, edges), (n, edges)
    assert sum(map(len, a)) == n
print('800 seeded random multigraphs with self loops: three methods agree')

# exhaustive: all edge sets (loops allowed) on 3 nodes = 2^6 subsets of the 6 possible unordered pairs incl. loops
pairs = [(u, v) for u in range(3) for v in range(u, 3)]
for mask in range(1 << len(pairs)):
    e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert components(3, e) == components_dsu(3, e) == brute(3, e)
print('exhaustive on 3 nodes: ok')

# scale: 10^5 nodes, 2*10^5 edges, plus a 10^5-node path
n = 10 ** 5
big = [[random.randrange(n), random.randrange(n)] for _ in range(2 * 10 ** 5)]
c1, c2 = components(n, big), components_dsu(n, big)
assert c1 == c2
print('random graph n=10^5, E=2*10^5: components =', len(c1), ', largest =', max(map(len, c1)))
path = [[i, i + 1] for i in range(n - 1)]
assert components(n, path) == [list(range(n))] == components_dsu(n, path)
print('path of 10^5 nodes: one component (iterative, no RecursionError)')
print('union-find: sets = n - successful unions:', n, '-', n - len(c2), '=', len(c2))
```

**Output (my run):**
```
4 prompt examples ok for DFS, union-find and brute force
800 seeded random multigraphs with self loops: three methods agree
exhaustive on 3 nodes: ok
random graph n=10^5, E=2*10^5: components = 1882 , largest = 98023
path of 10^5 nodes: one component (iterative, no RecursionError)
union-find: sets = n - successful unions: 100000 - 98118 = 1882
```

**Edge cases:**
- `n=0`: `[]`. No edges: n singleton components.
- Self loop `[2,2]`: no effect. Repeated edge `[1,3]`, `[3,1]`: no effect.
- 10^5 nodes in one long path: iterative traversal, no recursion limit problem.

**Follow-ups:**
- *Why union-find?* Edges arrive as a stream, or you also need 'are a and b connected' queries online (Q13).
- *Count only?* `n - successful unions`, no member lists needed.
- *Largest component?* Track sizes while collecting.

**Common mistakes:**
- Recursive DFS on 10^5 nodes: RecursionError.
- Forgetting isolated nodes (they are components of size 1).
- Not sorting members, or ordering components by size or discovery in a different loop order.
- Counting edges instead of successful unions.

### Q4 ⭐⭐⭐ 🟢 Flood fill. `image` is an m x n grid of integers (1 <= m, n <= 300), `(sr, sc)` is a start cell and `color` an integer. Change the start cell and every cell connected to it through up, down, left, right moves that has the same original value to `color`, and return the new grid (do not mutate the input). If the start cell already has value `color`, the image is returned unchanged. Sizes are chosen so that a recursive DFS would exceed CPython's default recursion limit of 1000, so an iterative method (queue or explicit stack) is required. Explain why this case needs a guard when you do not keep a separate visited set. Example: image=[[1, 1, 1], [1, 1, 0], [1, 0, 1]], sr=1, sc=1, color=2 -> [[2, 2, 2], [2, 2, 0], [2, 0, 1]]; image=[[0, 0, 0], [0, 0, 0]], sr=0, sc=0, color=0 -> [[0, 0, 0], [0, 0, 0]]; image=[[5]], sr=0, sc=0, color=9 -> [[9]].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid as an implicit graph. Nodes are cells, edges join up/down/left/right neighbours with the same value. Flood fill is one traversal from one cell.

**Say this first (1 line):** "Iterative DFS or BFS from the start cell over equal-valued 4-neighbours, recolouring as I go. If the colour already equals the start value I return early."

**Brute force:** Recursive DFS with a visited set. It is correct, but a 300 x 300 region can need depth up to 90,000 and Python stops at 1000 frames. Used in the code only on small grids to check the answer.

**Optimal:**
- Copy the image (the input must not change).
- `old = image[sr][sc]`. If `old == color`, return the copy now.
- Recolour the start cell, push it on a stack. Pop a cell; for each of 4 neighbours inside the grid whose value is `old`, recolour it immediately and push it.
- Recolouring on push is the visited mark: a recoloured cell no longer equals `old`, so nobody pushes it twice.
- Invariant: every cell on the stack or already popped has been recoloured; every cell not yet touched still has its original value.
- The guard: with no separate visited set, the 'is it still `old`' test is the only thing stopping revisits. If `color == old`, recolouring changes nothing, so cells keep matching `old` and re-enter the stack forever. The code shows the unguarded loop still running after 10,000 pops.

**Complexity:** Time O(m * n): each cell is pushed at most once and examines 4 neighbours. Space O(m * n) for the copy plus up to O(m * n) on the stack.

**Dry run:** `image=[[1,1,1],[1,1,0],[1,0,1]]`, start (1,1), colour 2.
- `old=1`. Recolour (1,1). Pop it: up (0,1)=1 recolour, push; down (2,1)=0 skip; left (1,0)=1 recolour, push; right (1,2)=0 skip.
- Pop (1,0): up (0,0) recolour; down (2,0) recolour. Pop those and (0,1): (0,2) recolour.
- Cell (2,2) is 1 but not connected through 4-moves: stays 1. Result `[[2,2,2],[2,2,0],[2,0,1]]`.

**Code:**
```python
import random
import sys
from collections import deque

random.seed(4)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    img = [row[:] for row in image]          # do not mutate the input
    if old == color:
        return img                           # the guard (see below)
    m, n = len(img), len(img[0])
    img[sr][sc] = color                      # recolouring on push doubles as the visited mark
    stack = [(sr, sc)]
    while stack:
        x, y = stack.pop()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and img[a][b] == old:
                img[a][b] = color
                stack.append((a, b))
    return img

def brute(image, sr, sc, color):
    """Recursive DFS with an explicit visited set; only safe while the region is < ~1000 cells deep."""
    m, n = len(image), len(image[0]); old = image[sr][sc]; seen = set()
    def go(x, y):
        seen.add((x, y))
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and image[a][b] == old and (a, b) not in seen:
                go(a, b)
    go(sr, sc)
    return [[color if (i, j) in seen else image[i][j] for j in range(n)] for i in range(m)]

def unguarded(image, sr, sc, color, cap):
    """No visited set and no old == color guard. When old == color nothing ever changes, so cells re-enter forever."""
    img = [row[:] for row in image]; old = img[sr][sc]; m, n = len(img), len(img[0])
    stack = [(sr, sc)]; pops = 0
    while stack:
        pops += 1
        if pops > cap:
            return 'still running after %d pops' % cap
        x, y = stack.pop(); img[x][y] = color
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and img[a][b] == old:
                stack.append((a, b))
    return img

assert flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
assert flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == [[0, 0, 0], [0, 0, 0]]
assert flood_fill([[5]], 0, 0, 9) == [[9]]
print('3 prompt examples ok')

src = [[1, 0], [0, 1]]
flood_fill(src, 0, 0, 7); assert src == [[1, 0], [0, 1]]        # input untouched

for _ in range(1000):
    m, n = random.randint(1, 5), random.randint(1, 5)
    img = [[random.randint(0, 2) for _ in range(n)] for _ in range(m)]
    sr, sc, col = random.randrange(m), random.randrange(n), random.randint(0, 3)
    want = brute(img, sr, sc, col) if img[sr][sc] != col else img
    assert flood_fill(img, sr, sc, col) == want, (img, sr, sc, col)
print('1000 seeded random grids: iterative == recursive-with-visited')

# the guard: same colour, no visited set
print('unguarded, color == old:', unguarded([[0, 0], [0, 0]], 0, 0, 0, 10000))
print('unguarded, color != old:', unguarded([[0, 0], [0, 0]], 0, 0, 5, 10000))

# scale: 300 x 300 all the same colour = one region of 90000 cells
big = [[1] * 300 for _ in range(300)]
out = flood_fill(big, 0, 0, 2)
assert all(v == 2 for row in out for v in row) and all(v == 1 for row in big for v in row)
print('300x300 single region recoloured iteratively, 90000 cells')

# a serpentine corridor forces a DFS path 45000+ deep: recursion cannot cope
snake = [[0] * 300 for _ in range(300)]
for i in range(1, 300, 2):
    for j in range(300):
        snake[i][j] = 1                       # walls on odd rows ...
    snake[i][299 if (i // 2) % 2 == 0 else 0] = 0   # ... with one gap alternating sides
out = flood_fill(snake, 0, 0, 9)
assert sum(v == 9 for row in out for v in row) == sum(v == 0 for row in snake for v in row)
try:
    brute(snake, 0, 0, 9)
except RecursionError:
    print('recursive DFS on the snake: RecursionError at limit', sys.getrecursionlimit())
print('iterative handled the snake of', sum(v == 9 for row in out for v in row), 'cells')
```

**Output (my run):**
```
3 prompt examples ok
1000 seeded random grids: iterative == recursive-with-visited
unguarded, color == old: still running after 10000 pops
unguarded, color != old: [[5, 5], [5, 5]]
300x300 single region recoloured iteratively, 90000 cells
recursive DFS on the snake: RecursionError at limit 1000
iterative handled the snake of 45150 cells
```

**Edge cases:**
- Start already equals `color`: unchanged copy, and the guard is essential.
- 1 x 1 grid. Whole grid one region.
- Diagonal neighbours do not connect.
- A winding corridor makes DFS depth huge: the snake in the code.

**Follow-ups:**
- *8-directional?* Use 8 offsets.
- *Why not `sys.setrecursionlimit`?* Deep Python recursion can crash the interpreter's C stack. Iterate.
- *BFS instead?* Same answer; the queue stays shorter on open regions.

**Common mistakes:**
- Mutating the input.
- Missing the `old == color` guard.
- Recolouring after popping instead of when pushing, so cells are pushed many times.
- Using `==` to compare a cell with `color` rather than with the original value.

### Q5 ⭐⭐⭐ 🟡 Number of islands, with the largest island. `grid` is a list of m strings of equal length n (1 <= m, n <= 300) made of '1' (land) and '0' (water). An island is a maximal set of land cells connected through up, down, left, right moves (diagonals do not connect). Return `[count, largest_area]` where largest_area is the cell count of the biggest island (0 if there is none). Sizes are chosen so that a recursive DFS would exceed CPython's default recursion limit of 1000, so an iterative method (queue or explicit stack) is required. Treat the grid as an implicit graph: say what the nodes and edges are and the time and space. Example: grid=['11000', '11000', '00100', '00011'] -> [3, 4]; grid=['000'] -> [0, 0]; grid=['1'] -> [1, 1]; grid=['101', '010', '101'] -> [5, 1].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Candidate-reported rounds on Naukri Code360 and GeeksforGeeks (a Flipkart 2021 report with number of islands, a Flipkart 2025 online assessment and a GeeksforGeeks on-campus 2020 report with word ladder; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Connected components on an implicit grid graph. Count components and track the size of each.

**Say this first (1 line):** "Nodes are land cells, edges join 4-neighbour land cells. I scan the grid, and every unseen land cell starts a BFS that counts one island and its area. O(m*n)."

**Brute force:** Label propagation: every land cell takes the smallest label among its land neighbours, repeated until stable. Worst case a long snake needs about m*n sweeps, so O((m*n)^2). It is the checker. Recursive DFS is the usual teaching answer and is correct, but 300 x 300 land is deep enough to raise RecursionError at the default limit of 1000.

**Optimal:**
- `seen` grid of booleans, `count = 0`, `best = 0`.
- Scan every cell. At an unseen `'1'`: `count += 1`, mark, BFS with a deque, counting popped cells as `area`. Mark each neighbour when enqueued.
- `best = max(best, area)` after each island.
- Why it is right: when the scan reaches an unseen land cell, all cells of earlier islands are already marked, so it must belong to a new island; BFS then claims exactly its whole island.

**Complexity:** Time O(m*n): every cell is visited once by the scan and enqueued at most once, with 4 neighbour checks each. Space O(m*n) for `seen` and the queue.

**Dry run:** `['11000','11000','00100','00011']`.
- (0,0) land, new island, BFS takes (0,0), (0,1), (1,0), (1,1): area 4. count 1, best 4.
- (2,2) land, new: area 1. count 2.
- (3,3) land: BFS takes (3,3), (3,4): area 2. count 3. Answer `[3, 4]`.

**Code:**
```python
import random
import sys
from collections import Counter, deque

random.seed(5)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def islands(grid):
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    count = best = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1' and not seen[i][j]:
                count += 1
                seen[i][j] = True
                q = deque([(i, j)]); area = 0
                while q:                              # BFS: iterative, so no recursion limit
                    x, y = q.popleft(); area += 1
                    for dx, dy in D4:
                        a, b = x + dx, y + dy
                        if 0 <= a < m and 0 <= b < n and grid[a][b] == '1' and not seen[a][b]:
                            seen[a][b] = True        # mark on enqueue: each cell enters once
                            q.append((a, b))
                best = max(best, area)
    return [count, best]

def brute(grid):
    """Label propagation: every land cell repeatedly takes the smallest label among its land neighbours."""
    m, n = len(grid), len(grid[0])
    lab = {(i, j): (i, j) for i in range(m) for j in range(n) if grid[i][j] == '1'}
    changed = True
    while changed:
        changed = False
        for (i, j) in lab:
            for dx, dy in D4:
                p = (i + dx, j + dy)
                if p in lab and lab[p] < lab[(i, j)]:
                    lab[(i, j)] = lab[p]; changed = True
    c = Counter(lab.values())
    return [len(c), max(c.values()) if c else 0]

def recursive(grid):
    m, n = len(grid), len(grid[0]); seen = set()
    def go(x, y):
        seen.add((x, y))
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and grid[a][b] == '1' and (a, b) not in seen:
                go(a, b)
    go(0, 0)

assert islands(['11000', '11000', '00100', '00011']) == [3, 4]
assert islands(['000']) == [0, 0]
assert islands(['1']) == [1, 1]
assert islands(['101', '010', '101']) == [5, 1]          # diagonals do not connect
print('4 prompt examples ok')

for _ in range(1500):
    m, n = random.randint(1, 6), random.randint(1, 6); p = random.random()
    g = [''.join('1' if random.random() < p else '0' for _ in range(n)) for _ in range(m)]
    assert islands(g) == brute(g), g
print('1500 seeded random grids: BFS == label propagation')

# exhaustive: every 3x3 grid (512 of them)
for mask in range(512):
    g = [''.join('1' if mask >> (3 * i + j) & 1 else '0' for j in range(3)) for i in range(3)]
    assert islands(g) == brute(g)
print('exhaustive on all 512 3x3 grids: ok')

full = ['1' * 300] * 300
assert islands(full) == [1, 90000]
checker = [''.join('1' if (i + j) % 2 == 0 else '0' for j in range(300)) for i in range(300)]
assert islands(checker) == [45000, 1]
print('300x300 all land: [1, 90000]; checkerboard (no 4-neighbour touches): 45000 islands of size 1')

snake = []
for i in range(300):
    snake.append('1' * 300 if i % 2 == 0 else ('0' * 299 + '1' if (i // 2) % 2 == 0 else '1' + '0' * 299))
res = islands(snake)
print('serpentine grid:', res)
try:
    recursive(['1' * 300] * 300)
except RecursionError:
    print('recursive DFS on the 300x300 land block: RecursionError at limit', sys.getrecursionlimit())
```

**Output (my run):**
```
4 prompt examples ok
1500 seeded random grids: BFS == label propagation
exhaustive on all 512 3x3 grids: ok
300x300 all land: [1, 90000]; checkerboard (no 4-neighbour touches): 45000 islands of size 1
serpentine grid: [1, 45150]
recursive DFS on the 300x300 land block: RecursionError at limit 1000
```

**Edge cases:**
- All water: `[0, 0]`. One land cell: `[1, 1]`.
- Diagonal land cells are separate islands (`['101','010','101']` gives 5 islands).
- Full 300 x 300 land: one island of 90,000 cells. Checkerboard: 45,000 islands.
- Rows are strings, so you cannot overwrite cells in place; use `seen` (or convert to lists).

**Follow-ups:**
- *Save memory?* Convert to lists and sink land to `'0'` instead of a `seen` grid (mutates the input; say so).
- *Islands as land arrives?* Union-find (the dynamic version of this question).
- *Perimeter or distinct shapes?* Same traversal, different bookkeeping.

**Common mistakes:**
- Recursive DFS on a big grid.
- Counting diagonals as connected.
- Marking on dequeue, which enqueues cells repeatedly.
- Returning the island count only and forgetting that `largest_area` is 0 when there is no land.

### Q6 ⭐⭐⭐ 🟡 Iterative DFS on a very deep graph. `n` and `edges` (a list of [u, v]) describe a connected simple undirected graph on nodes 0..n-1 (1 <= n <= 2*10^5, edges are distinct, no self loops). Starting at node 0 and trying each node's neighbours in ascending order, return `[preorder, max_depth]`: the depth-first preorder visiting order of all n nodes and the greatest depth (number of edges from node 0 along the DFS tree) of any node. The graph can be a single path of 2*10^5 nodes, so the answer must be iterative (an explicit stack of (node, neighbour-iterator) pairs); a recursive version raises RecursionError at CPython's default limit of 1000 (compare Part 7 Q35 for deep trees). Do not rely on `sys.setrecursionlimit` as the answer; say what an iterative version costs in memory. Example: n=4, edges=[[0, 2], [0, 1], [1, 3], [2, 3]] -> [[0, 1, 3, 2], 3]; n=1, edges=[] -> [[0], 0]; n=5, edges=[[0, 1], [1, 2], [2, 3], [3, 4]] -> [[0, 1, 2, 3, 4], 4].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Iterative DFS that keeps the recursion's state explicitly: a stack of (node, neighbour iterator).

**Say this first (1 line):** "I replace the call stack by my own stack of (node, iterator over its neighbours). That gives exact recursive preorder and depth, and no RecursionError."

**Brute force:** Recursive DFS with sorted adjacency lists. It is the specification, and it is right for small graphs. On a 2*10^5-node path it needs depth 2*10^5, so CPython raises RecursionError at the default limit of 1000 (compare Part 7 Q35 for deep skewed trees). The code confirms this on a 5000-node path.

**Optimal:**
- Sort each adjacency list so neighbours are tried in ascending order.
- Mark node 0 seen, record it, push `(0, iter(adj[0]))`.
- Loop: look at the top `(u, it)`. Advance `it` until you find an unseen `v`: mark it, record it in the preorder, set `depth[v] = depth[u] + 1`, push `(v, iter(adj[v]))`, and `break` to go deeper. If the iterator runs out (the `for ... else`), pop: that is the return from the recursive call.
- Why iterators: the iterator remembers where `u`'s neighbour scan stopped, exactly like a stack frame remembers its loop position. A plain 'push all neighbours' version needs the mark-on-pop rule and extra bookkeeping to get the depth right.
- Invariant: the stack holds the current root-to-node DFS path; its length minus 1 is the current depth.
- Depth of a node is the length of the tree path found by DFS (which can be much longer than the shortest path).

**Complexity:** Time O(V + E) for the walk plus O(sum of d log d) = O(E log V) at worst for sorting the adjacency lists once. Space: the explicit stack holds at most depth+1 frames, O(V) worst case (the path: 200,000 frames, each a tuple plus a list iterator, so memory grows linearly with depth) and 2 frames for a star. Heap memory is cheaper per frame than C-stack frames, and it is only limited by RAM, not by a recursion limit.

**Dry run:** `n=4, edges=[[0,2],[0,1],[1,3],[2,3]]`. Sorted: `0:[1,2]`, `1:[0,3]`, `2:[0,3]`, `3:[1,2]`.
- Visit 0. Top (0): next unseen is 1: visit 1 (depth 1), push.
- Top (1): 0 seen, 3 unseen: visit 3 (depth 2), push.
- Top (3): 1 seen, 2 unseen: visit 2 (depth 3), push.
- Top (2): all seen, pop. Pop 3, 1, then (0) has 2 seen; pop. Preorder `[0,1,3,2]`, max depth 3.

**Code:**
```python
import random
import sys

random.seed(6)

def deep_dfs(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for lst in adj:
        lst.sort()                                  # ascending neighbours
    seen = [False] * n; seen[0] = True
    order = [0]; depth = [0] * n; best = 0
    stack = [(0, iter(adj[0]))]                     # (node, iterator over its neighbours): resumes where it left off
    peak = 1
    while stack:
        u, it = stack[-1]
        for v in it:                                # continues from the saved position
            if not seen[v]:
                seen[v] = True; order.append(v)
                depth[v] = depth[u] + 1
                best = max(best, depth[v])
                stack.append((v, iter(adj[v])))
                peak = max(peak, len(stack))
                break                               # go deeper; come back to the rest later
        else:
            stack.pop()                             # neighbours exhausted: backtrack
    return [order, best], peak

def brute(n, edges):
    """Recursive version: same answer while the depth stays under the recursion limit."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for lst in adj:
        lst.sort()
    order = []; seen = set(); best = [0]
    def go(u, d):
        seen.add(u); order.append(u); best[0] = max(best[0], d)
        for v in adj[u]:
            if v not in seen:
                go(v, d + 1)
    go(0, 0)
    return [order, best[0]]

assert deep_dfs(4, [[0, 2], [0, 1], [1, 3], [2, 3]])[0] == [[0, 1, 3, 2], 3]
assert deep_dfs(1, [])[0] == [[0], 0]
assert deep_dfs(5, [[0, 1], [1, 2], [2, 3], [3, 4]])[0] == [[0, 1, 2, 3, 4], 4]
print('3 prompt examples ok')

def rand_connected(n, extra):
    es = {(random.randrange(i), i) for i in range(1, n)}      # a random tree
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in es]
    random.shuffle(pairs); es |= set(pairs[:extra])
    out = [list(e) if random.random() < .5 else [e[1], e[0]] for e in es]
    random.shuffle(out); return out

for _ in range(800):
    n = random.randint(1, 10)
    e = rand_connected(n, random.randint(0, 4))
    assert deep_dfs(n, e)[0] == brute(n, e), (n, e)
print('800 seeded random connected graphs: iterative == recursive')

n = 2 * 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
(order, depth), peak = deep_dfs(n, path)
assert order == list(range(n)) and depth == n - 1
print('path of 2*10^5 nodes: depth', depth, '| explicit stack peaked at', peak, 'frames')
try:
    brute(5000, path[:4999])
except RecursionError:
    print('recursive DFS on a 5000-node path: RecursionError at limit', sys.getrecursionlimit())

star = [[0, i] for i in range(1, n)]
(order, depth), peak = deep_dfs(n, star)
assert order == list(range(n)) and depth == 1
print('star of 2*10^5 nodes: depth', depth, '| stack peak', peak, '(the stack tracks depth, not size)')

# a path whose labels are shuffled still gives the same shape of answer
perm = list(range(n)); random.shuffle(perm); perm.remove(0); perm = [0] + perm
sh = [[perm[i], perm[i + 1]] for i in range(n - 1)]
(order, depth), _ = deep_dfs(n, sh)
assert order == perm and depth == n - 1
print('shuffled-label path of 2*10^5 nodes: preorder is the path order, depth', depth)
```

**Output (my run):**
```
3 prompt examples ok
800 seeded random connected graphs: iterative == recursive
path of 2*10^5 nodes: depth 199999 | explicit stack peaked at 200000 frames
recursive DFS on a 5000-node path: RecursionError at limit 1000
star of 2*10^5 nodes: depth 1 | stack peak 2 (the stack tracks depth, not size)
shuffled-label path of 2*10^5 nodes: preorder is the path order, depth 199999
```

**Edge cases:**
- `n=1`: `[[0], 0]`.
- Path of 2*10^5 nodes: stack peaks at 200,000 frames; star: peak 2.
- Cycles: the seen array prevents re-entry.
- Labels shuffled along a path: preorder follows the path.

**Follow-ups:**
- *Why not `sys.setrecursionlimit(10**6)`?* Python frames also use the C stack in some paths, so a large limit can segfault the process; it is a hack, not a design.
- *Could `threading.stack_size` help?* It is another workaround; the explicit stack is portable.
- *Postorder?* Do the work at the pop (the `else` branch).

**Common mistakes:**
- Pushing all neighbours and marking on push, which changes the order and breaks depth tracking.
- Forgetting to `break` after pushing a child, so the loop pushes siblings first and the order is wrong.
- Using `sys.setrecursionlimit` as the answer.
- Sorting after pushing instead of before.

### Q7 ⭐⭐⭐ 🟡 Shortest path lengths in an unweighted graph. `n` nodes 0..n-1 (1 <= n <= 10^5), `edges` a list of [u, v] (0 <= len <= 2*10^5, no self loops), `src` a node and `directed` a boolean (if false every edge works both ways). Return a list `dist` of length n with `dist[v]` the minimum number of edges on a path from `src` to `v`, or -1 if v is unreachable. Explain why the first time BFS reaches a node is the shortest and why this fails once edges have different weights. Example: n=5, edges=[[0, 1], [1, 2], [0, 3], [3, 2]], src=0, directed=True -> [0, 1, 2, 1, -1]; n=4, edges=[[1, 2], [2, 3]], src=3, directed=False -> [-1, 2, 1, 0]; n=3, edges=[], src=1, directed=False -> [-1, 0, -1].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** BFS for shortest paths when every edge costs the same (unweighted).

**Say this first (1 line):** "BFS explores in layers of equal hop count, so the first time it reaches a node is by a shortest path. Distances in an array, -1 for unseen. O(V + E)."

**Brute force:** Bellman-Ford with unit weights: relax every edge up to V times. O(V * E), far too slow at 10^5 nodes and 2*10^5 edges (2*10^10 steps). Used in the code as the checker.

**Optimal:**
- `dist = [-1] * n`, `dist[src] = 0`, `deque([src])`.
- Pop `u`; for each neighbour `v` with `dist[v] == -1`: `dist[v] = dist[u] + 1`, enqueue.
- Directed: add `v` to `adj[u]` only. Undirected: add both ways.
- Why first arrival is shortest: the queue holds nodes in non-decreasing distance (layer k, then layer k+1). When a node at distance k is popped, any unseen neighbour must be at distance k+1 or less; it cannot be less, otherwise it would have been discovered from an earlier layer. Induction on the layer.
- Why weights break it: BFS counts edges, not cost. Edges `0->1` (cost 10), `0->2` (1), `2->1` (1): BFS says node 1 is 1 hop away, but the cheapest cost is 2 via node 2. With weights you need Dijkstra (non-negative) or Bellman-Ford (negative).

**Complexity:** Time O(V + E): each node enqueued once, each adjacency entry scanned once. Space O(V + E).

**Dry run:** Directed, edges `0->1, 1->2, 0->3, 3->2`, src 0.
- dist `[0,-1,-1,-1,-1]`; queue `[0]`.
- Pop 0: dist[1]=1, dist[3]=1. Pop 1: dist[2]=2. Pop 3: 2 already set. Pop 2: nothing.
- Result `[0,1,2,1,-1]`; node 4 is unreachable.

**Code:**
```python
import random
from collections import deque

random.seed(7)
INF = float('inf')

def bfs_dist(n, edges, src, directed):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    dist = [-1] * n
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:               # first arrival is the shortest; -1 doubles as "unseen"
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def brute(n, edges, src, directed):
    """Bellman-Ford with unit weights: relax every edge n times."""
    d = [INF] * n; d[src] = 0
    for _ in range(n):
        for u, v in edges:
            if d[u] + 1 < d[v]: d[v] = d[u] + 1
            if not directed and d[v] + 1 < d[u]: d[u] = d[v] + 1
    return [-1 if x == INF else x for x in d]

assert bfs_dist(5, [[0, 1], [1, 2], [0, 3], [3, 2]], 0, True) == [0, 1, 2, 1, -1]
assert bfs_dist(4, [[1, 2], [2, 3]], 3, False) == [-1, 2, 1, 0]
assert bfs_dist(3, [], 1, False) == [-1, 0, -1]
print('3 prompt examples ok')

for _ in range(1000):
    n = random.randint(1, 8); d = random.random() < .5
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (d or u < v)]
    random.shuffle(pairs)
    e = [list(p) for p in pairs[:random.randint(0, min(10, len(pairs)))]]
    s = random.randrange(n)
    assert bfs_dist(n, e, s, d) == brute(n, e, s, d), (n, e, s, d)
print('1000 seeded random graphs: BFS == Bellman-Ford with unit weights')

# the level property: each edge u->v satisfies dist[v] <= dist[u] + 1 whenever u is reachable
n = 2000
e = [[random.randrange(n), random.randrange(n)] for _ in range(4000)]
e = [x for x in e if x[0] != x[1]]
dist = bfs_dist(n, e, 0, True)
assert all(dist[v] != -1 and dist[v] <= dist[u] + 1 for u, v in e if dist[u] != -1)
print('random directed graph n=2000: edge property dist[v] <= dist[u] + 1 holds for every edge out of a reached node')

N = 10 ** 5
path = [[i, i + 1] for i in range(N - 1)]
assert bfs_dist(N, path, 0, False)[-1] == N - 1 and bfs_dist(N, path, N - 1, True)[0] == -1
print('path of 10^5 nodes: far end at distance', N - 1, '; directed against the arrows: unreachable (-1)')

# why it fails with weights: BFS counts edges, not cost
w_edges = [(0, 1, 10), (0, 2, 1), (2, 1, 1)]          # 0->1 costs 10 directly, 2 via node 2
hops = bfs_dist(3, [[u, v] for u, v, _ in w_edges], 0, True)
cost = [0, INF, INF]
for _ in range(3):
    for u, v, w in w_edges:
        cost[v] = min(cost[v], cost[u] + w)
print('hop counts (BFS):', hops, '| cheapest costs:', cost, '-> BFS says node 1 is 1 hop but the best cost is 2, not 10')
```

**Output (my run):**
```
3 prompt examples ok
1000 seeded random graphs: BFS == Bellman-Ford with unit weights
random directed graph n=2000: edge property dist[v] <= dist[u] + 1 holds for every edge out of a reached node
path of 10^5 nodes: far end at distance 99999 ; directed against the arrows: unreachable (-1)
hop counts (BFS): [0, 1, 1] | cheapest costs: [0, 2, 1] -> BFS says node 1 is 1 hop but the best cost is 2, not 10
```

**Edge cases:**
- Isolated source: only `dist[src]=0`, rest -1.
- Directed graph where reachability depends on direction.
- Path of 10^5 nodes: distance 99,999.
- Unreachable is -1, never 0 or infinity in the output.

**Follow-ups:**
- *Recover the path?* Store `parent[v] = u` on discovery and walk back.
- *Weights 0 or 1?* 0-1 BFS with a deque (appendleft for 0).
- *Many sources?* Seed the queue with all of them (Q11).

**Common mistakes:**
- Using a separate `seen` set and forgetting to mark on enqueue.
- Using BFS when weights differ.
- Initialising `dist` with 0, so a real distance of 0 and unseen look the same.
- Adding only one direction for an undirected edge.

### Q8 ⭐⭐⭐ 🟡 Course schedule: can all courses be finished? `num_courses` courses are labelled 0..num_courses-1 (1 <= num_courses <= 2000) and `prerequisites` is a list of [a, b] meaning b must be taken before a (0 <= len <= 5000; repeats and [a, a] are possible). Return True if there is an order in which every course can be taken, else False. Solve it with Kahn's algorithm (repeatedly remove nodes with no remaining prerequisites) and state why a leftover node means a cycle. Example: num_courses=2, prerequisites=[[1, 0]] -> True; num_courses=2, prerequisites=[[1, 0], [0, 1]] -> False; num_courses=3, prerequisites=[[1, 1]] -> False; num_courses=3, prerequisites=[] -> True.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort, Kahn's version. Cycle detection falls out of counting how many nodes you could remove.

**Say this first (1 line):** "Edge b -> a for each prerequisite. Repeatedly take courses with indegree 0. If I take all of them, it is feasible; if some are left, they sit on or behind a cycle."

**Brute force:** Compute the transitive closure (can course i reach itself through prerequisites?) with Floyd-Warshall style triple loops, O(n^3). For n = 2000 that is 8*10^9: too slow. It is the checker on tiny inputs.

**Optimal:**
- Build `adj[b].append(a)` and `indeg[a] += 1` for each pair `[a, b]`.
- Queue all courses with `indeg == 0`. Pop `u`, count it as taken, decrement the indegree of each `v` in `adj[u]`, enqueue those that reach 0.
- Return `taken == num_courses`.
- Repeats: `[1,0]` twice adds indegree 2 and the edge twice; popping 0 subtracts twice. Consistent, so nothing special.
- Self loop `[a, a]`: `a` has indegree at least 1 from itself and can never reach 0, so it is left over: False, correct.
- Why a leftover means a cycle: suppose a leftover node exists. Every leftover node still has indegree >= 1 from other leftover nodes (any prerequisite already taken would have been subtracted). Follow incoming edges backwards among leftovers; with finitely many nodes you must repeat one, which gives a cycle. Conversely a cycle node can never reach indegree 0, because its predecessor on the cycle is never taken.
- Leftovers include the cycle and everything downstream of it (shown in the code).

**Complexity:** Time O(V + E): each node enqueued once, each edge subtracted once. Space O(V + E).

**Dry run:** `2` courses, `[[1,0],[0,1]]`.
- Edges 0 -> 1 and 1 -> 0. Indegrees `[1,1]`. Queue empty at once, `taken = 0 != 2`: False.
- And `[[1,0]]`: indegrees `[0,1]`; take 0, indegree of 1 drops to 0, take 1: `taken = 2`: True.

**Code:**
```python
import itertools
import random
from collections import deque

random.seed(8)

def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:                 # b before a: edge b -> a
        adj[b].append(a)
        indeg[a] += 1                          # repeated pairs count twice and are subtracted twice: consistent
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    taken = 0
    while q:
        u = q.popleft(); taken += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return taken == num_courses                # leftovers all sit on, or behind, a cycle

def brute(num_courses, prerequisites):
    """Transitive closure (Floyd-Warshall style): feasible iff no course can reach itself."""
    n = num_courses
    r = [[False] * n for _ in range(n)]
    for a, b in prerequisites:
        r[b][a] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]:
                        r[i][j] = True
    return not any(r[i][i] for i in range(n))

def leftover(num_courses, prerequisites):
    """Which courses Kahn cannot take: the cycle plus everything downstream of it."""
    adj = [[] for _ in range(num_courses)]; indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a); indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0); gone = set()
    while q:
        u = q.popleft(); gone.add(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return sorted(set(range(num_courses)) - gone)

assert can_finish(2, [[1, 0]]) is True
assert can_finish(2, [[1, 0], [0, 1]]) is False
assert can_finish(3, [[1, 1]]) is False
assert can_finish(3, []) is True
print('4 prompt examples ok')

for _ in range(1500):
    n = random.randint(1, 6)
    pre = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 8))]
    assert can_finish(n, pre) == brute(n, pre), (n, pre)
print('1500 seeded random inputs (repeats and self loops included): Kahn == transitive closure')

# exhaustive: every set of ordered pairs (self loops included) on 3 courses = 2^9 sets
pairs = [(a, b) for a in range(3) for b in range(3)]
for mask in range(1 << 9):
    pre = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert can_finish(3, pre) == brute(3, pre)
print('exhaustive on 3 courses, all 512 prerequisite sets: ok')

# leftovers: a cycle plus a tail behind it
print('leftover for 0<->1 cycle with 2 after 1 and a free course 3:', leftover(4, [[0, 1], [1, 0], [2, 1]]))
# duplicates do not break the counting
assert can_finish(2, [[1, 0], [1, 0], [1, 0]]) is True
# scale: a chain of 2000 courses, then the same chain closed into a cycle
chain = [[i + 1, i] for i in range(1999)]
assert can_finish(2000, chain) is True and can_finish(2000, chain + [[0, 1999]]) is False
print('chain of 2000 courses: True; closed into a ring: False')
```

**Output (my run):**
```
4 prompt examples ok
1500 seeded random inputs (repeats and self loops included): Kahn == transitive closure
exhaustive on 3 courses, all 512 prerequisite sets: ok
leftover for 0<->1 cycle with 2 after 1 and a free course 3: [0, 1, 2]
chain of 2000 courses: True; closed into a ring: False
```

**Edge cases:**
- No prerequisites: True. Self loop: False.
- Duplicate prerequisite pairs.
- Courses with no edges at all start in the queue.
- Chain of 2000: True; the same chain closed into a ring: False.

**Follow-ups:**
- *Return an order?* Append popped nodes (Q9).
- *Which courses are stuck?* The leftover set (cycle plus downstream).
- *DFS version?* Three-colour cycle detection (Q10).

**Common mistakes:**
- Reversing the edge direction (a -> b). The count still works, but be consistent when you later need the order.
- De-duplicating pairs for the adjacency list but not for indegree (or the other way round).
- Checking `len(queue) == 0` instead of the number taken.
- Forgetting isolated courses.

### Q9 ⭐⭐⭐ 🟡 Course schedule II: produce an order. Same input as the course-schedule feasibility question: `num_courses` (1 <= num_courses <= 2000) and `prerequisites` as [a, b] pairs meaning b before a. Return a list of all courses in an order that satisfies every prerequisite, or [] if no such order exists. Many orders can be valid: the checker accepts any permutation of 0..num_courses-1 that puts b before a for every pair, and accepts [] only when a cycle exists; the example shows one accepted answer (the Kahn order with a FIFO queue seeded in ascending label order). Say when the order is unique. Example: num_courses=4, prerequisites=[[1, 0], [2, 0], [3, 1], [3, 2]] -> [0, 1, 2, 3]; num_courses=2, prerequisites=[[0, 1], [1, 0]] -> []; num_courses=1, prerequisites=[] -> [0].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort (Kahn). Same indegree process as feasibility; the pop order is the answer.

**Say this first (1 line):** "Kahn's algorithm with a FIFO queue seeded in ascending order; the pop order is a valid schedule; if I pop fewer than n courses there is a cycle and I return []."

**Brute force:** Try all n! permutations and keep one that respects every pair. Fine for n <= 6 (the checker uses this), impossible at n = 2000.

**Optimal:**
- Edge `b -> a` for each `[a, b]`; `indeg[a]` counts prerequisites.
- Queue = all indegree-0 courses in ascending order. Pop `u`, append to `order`, decrement neighbours, enqueue new zeros.
- `order if len(order) == n else []`.
- Validity: a course is appended only after every one of its prerequisites was popped (its indegree reached 0), so `b` is before `a` for every pair.
- Many answers are valid, so the checker accepts any permutation of `0..n-1` with `b` before `a` for every pair, and `[]` exactly when a cycle exists. The prompt's `[0,1,2,3]` is just the FIFO-ascending one; `[0,2,1,3]` is equally valid.
- When is the order unique? Exactly when, at every step of Kahn, there is exactly one node with indegree 0 (never two ready at once). Equivalent: consecutive courses in the order are joined by a prerequisite edge, i.e. a chain through all nodes exists. The code verifies this exhaustively on all 4165 prerequisite sets over 1 to 4 courses (loop-free pairs).

**Complexity:** Time O(V + E), space O(V + E).

**Dry run:** `4, [[1,0],[2,0],[3,1],[3,2]]`: edges 0->1, 0->2, 1->3, 2->3. Indegrees `[0,1,1,2]`.
- Queue `[0]`. Pop 0: indeg 1 and 2 become 0, queue `[1,2]`.
- Pop 1: indeg 3 becomes 1. Pop 2: indeg 3 becomes 0, queue `[3]`. Pop 3.
- Order `[0,1,2,3]`. Two nodes were ready together (1 and 2), so the order is not unique (2 valid orders).

**Code:**
```python
import itertools
import random
from collections import deque

random.seed(9)

def course_order(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a); indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)   # ascending seed
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []

def feasible_brute(n, pre):
    """Try every permutation (n <= 6)."""
    for p in itertools.permutations(range(n)):
        pos = {c: i for i, c in enumerate(p)}
        if all(pos[b] < pos[a] for a, b in pre):
            return True
    return False

def count_orders(n, pre):
    cnt = 0
    for p in itertools.permutations(range(n)):
        pos = {c: i for i, c in enumerate(p)}
        if all(pos[b] < pos[a] for a, b in pre):
            cnt += 1
    return cnt

def valid(n, pre, got):
    """Checker: [] only if a cycle exists, otherwise a permutation with b before a for every pair."""
    if not feasible_brute(n, pre):
        return got == []
    if sorted(got) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[b] < pos[a] for a, b in pre)

def kahn_always_one_ready(n, pre):
    """Unique-order test: at every step exactly one node has indegree 0."""
    adj = [[] for _ in range(n)]; indeg = [0] * n
    for a, b in pre:
        adj[b].append(a); indeg[a] += 1
    ready = [i for i in range(n) if indeg[i] == 0]; done = 0
    while ready:
        if len(ready) != 1:
            return False
        u = ready.pop(); done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: ready.append(v)
    return done == n

assert course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
assert course_order(2, [[0, 1], [1, 0]]) == []
assert course_order(1, []) == [0]
print('3 prompt examples ok')

for _ in range(1500):
    n = random.randint(1, 6)
    pre = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 7))]
    assert valid(n, pre, course_order(n, pre)), (n, pre)
print('1500 seeded random inputs: output accepted by the validator (permutation, every b before a, [] only on cycles)')

# the uniqueness claim: a topological order is unique  <=>  Kahn never has two ready nodes at once
# <=>  consecutive nodes of the order are joined by prerequisite edges. Exhaustive on n <= 4, all pair sets without loops.
checked = 0
for n in (1, 2, 3, 4):
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    for mask in range(1 << len(pairs)):
        pre = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        cnt = count_orders(n, pre)
        one = kahn_always_one_ready(n, pre)
        assert (cnt == 1) == one, (n, pre, cnt)
        if cnt == 1:
            o = course_order(n, pre)
            es = {(b, a) for a, b in pre}
            assert all((o[i], o[i + 1]) in es for i in range(n - 1)), (n, pre)   # Hamiltonian path in the DAG
        checked += 1
print('uniqueness claim verified exhaustively on', checked, 'prerequisite sets for n = 1..4: unique iff one node is ready at every step')

# example of a non-unique case and the count of valid orders
print('orders for 4 courses with [[1,0],[2,0],[3,1],[3,2]]:', count_orders(4, [[1, 0], [2, 0], [3, 1], [3, 2]]), '(0,1,2,3 and 0,2,1,3)')
print('FIFO Kahn gives', course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]), '; another valid answer is [0, 2, 1, 3]')
chain = [[i + 1, i] for i in range(1999)]
assert course_order(2000, chain) == list(range(2000)) and course_order(2000, chain + [[0, 1999]]) == []
print('chain of 2000: unique order; same chain closed into a ring: []')
```

**Output (my run):**
```
3 prompt examples ok
1500 seeded random inputs: output accepted by the validator (permutation, every b before a, [] only on cycles)
uniqueness claim verified exhaustively on 4165 prerequisite sets for n = 1..4: unique iff one node is ready at every step
orders for 4 courses with [[1,0],[2,0],[3,1],[3,2]]: 2 (0,1,2,3 and 0,2,1,3)
FIFO Kahn gives [0, 1, 2, 3] ; another valid answer is [0, 2, 1, 3]
chain of 2000: unique order; same chain closed into a ring: []
```

**Edge cases:**
- Cycle: `[]`. Self loop: `[]`.
- No prerequisites: `[0..n-1]` ascending.
- A single chain: unique answer.
- Duplicate pairs: harmless.

**Follow-ups:**
- *Lexicographically smallest order?* Use a min-heap instead of the FIFO queue.
- *DFS alternative?* Reverse postorder of a DFS, with cycle detection (Q10).
- *Count the orders?* Needs DP over subsets; it is #P-hard in general.

**Common mistakes:**
- Returning a partial order when there is a cycle.
- Reversing the answer when you built edges `a -> b`.
- Testing against a single expected list instead of validating, when many orders are correct.
- Claiming the order is unique whenever the graph is a tree: only a single chain is unique.

### Q10 ⭐⭐⭐ 🟡 Detect a cycle in a directed graph with three colours. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` a list of directed [u, v] (0 <= len <= 2*10^5; self loops allowed). Return True if the graph contains a directed cycle. Use depth-first search with the three states white (unseen), grey (on the current path) and black (finished), and explain why an edge to a grey node is a cycle while an edge to a black node is not. Sizes are chosen so that a recursive DFS would exceed CPython's default recursion limit of 1000, so an iterative method (queue or explicit stack) is required. Example: n=4, edges=[[0, 1], [1, 2], [2, 3], [3, 1]] -> True; n=3, edges=[[0, 1], [0, 2], [1, 2]] -> False; n=2, edges=[[1, 1]] -> True; n=1, edges=[] -> False.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** DFS cycle detection with three states: white (unseen), grey (on the current path), black (finished).

**Say this first (1 line):** "An edge into a grey node closes a loop on my current path, so that is a cycle; an edge into a black node is just a second way to a finished part, so it is not. Iterative, because depth can reach 10^5."

**Brute force:** Transitive closure: build reachability with triple loops and report whether any node reaches itself. O(V^3). For V = 10^5 impossible. Recursive three-colour DFS is the textbook answer; it fails on a long path (RecursionError at 1000).

**Optimal:**
- Colours in a list. For each white `s`: colour it grey and push `(s, iter(adj[s]))`.
- Top of stack `(u, it)`: take the next `v`. If `v` is grey: return True. If white: colour grey, push. If black: skip. When `it` is exhausted (the `for ... else`), colour `u` black and pop.
- Why grey means a cycle: grey nodes are exactly the stack, a path from the DFS root to `u`. An edge `u -> v` with `v` on that path gives `v ... u -> v`, a cycle. A self loop is `u -> u` with `u` grey: caught the same way.
- Why black is safe: `v` turns black only when its whole out-neighbourhood has been explored. If `u -> v` hits a black `v`, then `v` cannot reach `u`: `u` is grey now, so it was already grey (on the stack) when `v` was explored, and any path from `v` back to `u` would have hit that grey `u` and reported a cycle then. So no loop goes through this edge. The diamond `0->1, 0->2, 1->3, 2->3` reaches 3 twice and has no cycle; a plain 'seen' check wrongly says True (shown in the code).
- Invariant: grey set = current stack.

**Complexity:** Time O(V + E), space O(V + E). The explicit stack replaces the call stack, so there is no recursion limit.

**Dry run:** `0->1, 1->2, 2->3, 3->1`.
- Grey 0, then 1, 2, 3. At 3 the edge 3 -> 1 points to grey 1: cycle, True.
- For `0->1, 0->2, 1->2`: 0, 1, 2 grey in turn; 2 has no edges, black; back at 1 black; back at 0 the edge 0 -> 2 hits black 2: skip. All finish: False.

**Code:**
```python
import random
import sys

random.seed(10)
WHITE, GREY, BLACK = 0, 1, 2

def has_cycle(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [WHITE] * n
    for s in range(n):
        if color[s] != WHITE:
            continue
        color[s] = GREY
        stack = [(s, iter(adj[s]))]            # iterative DFS; the stack IS the grey path
        while stack:
            u, it = stack[-1]
            for v in it:
                if color[v] == GREY:           # back edge to the current path: cycle
                    return True
                if color[v] == WHITE:
                    color[v] = GREY
                    stack.append((v, iter(adj[v])))
                    break
                # BLACK: finished earlier, cannot lead back to u (see the explanation): ignore
            else:
                color[u] = BLACK               # all neighbours done
                stack.pop()
    return False

def brute(n, edges):
    """Transitive closure: a cycle exists iff some node reaches itself."""
    r = [[False] * n for _ in range(n)]
    for u, v in edges:
        r[u][v] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]:
                        r[i][j] = True
    return any(r[i][i] for i in range(n))

def recursive(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    def go(u):
        color[u] = GREY
        for v in adj[u]:
            if color[v] == GREY or (color[v] == WHITE and go(v)):
                return True
        color[u] = BLACK
        return False
    return any(color[s] == WHITE and go(s) for s in range(n))

assert has_cycle(4, [[0, 1], [1, 2], [2, 3], [3, 1]]) is True
assert has_cycle(3, [[0, 1], [0, 2], [1, 2]]) is False
assert has_cycle(2, [[1, 1]]) is True
assert has_cycle(1, []) is False
print('4 prompt examples ok')

for _ in range(1500):
    n = random.randint(1, 6)
    e = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 7))]
    assert has_cycle(n, e) == brute(n, e) == recursive(n, e), (n, e)
print('1500 seeded random digraphs: iterative == closure == recursive')

pairs = [(u, v) for u in range(3) for v in range(3)]
for mask in range(512):
    e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert has_cycle(3, e) == brute(3, e)
pairs = [(u, v) for u in range(4) for v in range(4)]
for mask in range(1 << 16):
    e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert has_cycle(4, e) == brute(4, e)
print('exhaustive: all 512 digraphs on 3 nodes and all 65536 on 4 nodes (self loops included): ok')

# BLACK edge is not a cycle: the diamond 0->1, 0->2, 1->3, 2->3 reaches 3 twice, once through a black node
assert has_cycle(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) is False
# treating BLACK like GREY (a plain 'seen' set) wrongly reports a cycle
def wrong_seen(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v)
    seen = set(); st = [0]
    while st:
        u = st.pop(); seen.add(u)
        for v in adj[u]:
            if v in seen: return True
            st.append(v)
    return False
print('diamond DAG: three-colour says', has_cycle(4, [[0, 1], [0, 2], [1, 3], [2, 3]]), '| naive "seen" check says', wrong_seen(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))

n = 2 * 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
assert has_cycle(n, path) is False and has_cycle(n, path + [[n - 1, 0]]) is True
print('path of 2*10^5 nodes: False; closed into a ring: True (iterative, no RecursionError)')
try:
    recursive(5000, path[:4999])
except RecursionError:
    print('recursive three-colour DFS on a 5000-node path: RecursionError at limit', sys.getrecursionlimit())
```

**Output (my run):**
```
4 prompt examples ok
1500 seeded random digraphs: iterative == closure == recursive
exhaustive: all 512 digraphs on 3 nodes and all 65536 on 4 nodes (self loops included): ok
diamond DAG: three-colour says False | naive "seen" check says True
path of 2*10^5 nodes: False; closed into a ring: True (iterative, no RecursionError)
recursive three-colour DFS on a 5000-node path: RecursionError at limit 1000
```

**Edge cases:**
- Self loop: True. Single node: False.
- Disconnected graph: start from every white node.
- Path of 2*10^5 nodes: False; with the closing edge: True.
- Diamond (shared descendants): False.

**Follow-ups:**
- *Find the cycle?* Keep `parent` and walk back from `u` to `v`.
- *Undirected graphs?* Different rule: ignore the parent edge, or use union-find.
- *Kahn instead?* Same answer; Q8.

**Common mistakes:**
- Using a single `visited` set (false positives on diamonds).
- Forgetting to turn the node black on exit.
- Not looping over all starts (cycle in a different component).
- Recursive DFS on a long chain.

### Q11 ⭐⭐⭐ 🟡 Rotting oranges (multi-source BFS). `grid` is an m x n grid (1 <= m, n <= 100) with 0 = empty, 1 = fresh orange, 2 = rotten orange. Every minute, each fresh orange that is up, down, left or right of a rotten orange becomes rotten. Return the minimum number of minutes until no fresh orange remains, 0 if there is none to begin with, or -1 if some fresh orange can never rot. Explain why all rotten oranges must start in the queue together, and the time and space. Example: grid=[[2, 1, 1], [1, 1, 0], [0, 1, 1]] -> 4; grid=[[2, 1, 1], [0, 1, 1], [1, 0, 1]] -> -1; grid=[[0, 2]] -> 0; grid=[[1]] -> -1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Multi-source BFS on a grid. Time advances level by level; all rotten oranges are sources at time 0.

**Say this first (1 line):** "Put every rotten orange in the queue first, then run BFS one level per minute, counting fresh oranges down; if any are left, return -1."

**Brute force:** Simulate: each minute, scan the whole grid and rot every fresh orange next to a rotten one; stop when nothing changes. O((m*n)^2) worst case (a snake takes about m*n/2 minutes of m*n work). It is the checker.

**Optimal:**
- Scan once: queue all `2` cells, count `1` cells as `fresh`.
- While the queue is non-empty and `fresh > 0`: process exactly the current queue length (one minute): for each popped orange, rot each fresh 4-neighbour, `fresh -= 1`, enqueue it. After the batch, `minutes += 1`.
- Return `-1` if `fresh > 0` at the end, else `minutes`. If there were no fresh oranges the loop never runs: 0.
- Why all sources together: rotting spreads from every rotten orange at the same time. The time a fresh orange rots is its distance to the nearest rotten one (min over sources); the answer is the max over fresh oranges. One BFS seeded with all sources computes the min for everyone in one pass. Running BFS from one source, or one after another, gives the wrong numbers (in the code, `[[2,1,1,1,2]]` is 2 minutes but a single-source BFS says 3; it is wrong on 1409 of 2000 seeded 4 x 5 grids).
- Invariant: after minute t, exactly the fresh oranges at distance <= t from some rotten orange are rotten.

**Complexity:** Time O(m*n): one scan, each cell enqueued at most once. Space O(m*n) for the copy and queue.

**Dry run:** `[[2,1,1],[1,1,0],[0,1,1]]`, fresh = 6, queue `[(0,0)]`.
- Minute 1: (0,1) and (1,0) rot, fresh 4. Minute 2: (0,2), (1,1) rot, fresh 2.
- Minute 3: (2,1) rots, fresh 1. Minute 4: (2,2) rots, fresh 0. Answer 4.

**Code:**
```python
import random
from collections import deque

random.seed(11)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def rotting(grid):
    m, n = len(grid), len(grid[0])
    g = [row[:] for row in grid]
    q = deque(); fresh = 0
    for i in range(m):
        for j in range(n):
            if g[i][j] == 2: q.append((i, j))      # ALL rotten oranges are seeds at time 0
            elif g[i][j] == 1: fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):                    # one full level = one minute
            x, y = q.popleft()
            for dx, dy in D4:
                a, b = x + dx, y + dy
                if 0 <= a < m and 0 <= b < n and g[a][b] == 1:
                    g[a][b] = 2; fresh -= 1; q.append((a, b))
        minutes += 1
    return -1 if fresh else minutes

def brute(grid):
    """Simulate minute by minute on a copy until nothing changes."""
    m, n = len(grid), len(grid[0]); g = [row[:] for row in grid]; t = 0
    while True:
        new = [row[:] for row in g]; changed = False
        for i in range(m):
            for j in range(n):
                if g[i][j] == 1 and any(0 <= i + dx < m and 0 <= j + dy < n and g[i + dx][j + dy] == 2 for dx, dy in D4):
                    new[i][j] = 2; changed = True
        if not changed: break
        g = new; t += 1
    return -1 if any(1 in row for row in g) else t

def one_source_at_a_time(grid):
    """Wrong idea: BFS from the first rotten orange only."""
    m, n = len(grid), len(grid[0])
    src = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 2]
    if not src: return 0 if not any(1 in r for r in grid) else -1
    dist = {src[0]: 0}; q = deque([src[0]])
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and grid[a][b] != 0 and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + 1; q.append((a, b))
    fresh = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 1]
    if any(p not in dist for p in fresh): return -1
    return max((dist[p] for p in fresh), default=0)

assert rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert rotting([[0, 2]]) == 0
assert rotting([[1]]) == -1
print('4 prompt examples ok')

for _ in range(2000):
    m, n = random.randint(1, 5), random.randint(1, 5)
    g = [[random.choice([0, 1, 1, 2]) for _ in range(n)] for _ in range(m)]
    snap = [r[:] for r in g]
    assert rotting(g) == brute(g), g
    assert g == snap
print('2000 seeded random grids: multi-source BFS == minute-by-minute simulation; input untouched')

for mask in range(3 ** 6):                         # every 2x3 grid over {0,1,2}
    cells = [(mask // 3 ** k) % 3 for k in range(6)]
    g = [cells[:3], cells[3:]]
    assert rotting(g) == brute(g)
print('exhaustive on all 729 2x3 grids: ok')

bad = [[2, 1, 1, 1, 2]]
print('grid [[2,1,1,1,2]]: correct', rotting(bad), '| single-source (first rotten only)', one_source_at_a_time(bad))
wrong = 0
for _ in range(2000):
    g = [[random.choice([0, 1, 1, 2]) for _ in range(5)] for _ in range(4)]
    wrong += one_source_at_a_time(g) != rotting(g)
print('single-source BFS wrong on', wrong, 'of 2000 seeded 4x5 grids')

assert rotting([[1, 1], [1, 1]]) == -1             # fresh but no rotten at all
assert rotting([[0, 0]]) == 0 and rotting([[2]]) == 0
big = [[1] * 100 for _ in range(100)]; big[0][0] = 2
assert rotting(big) == 198                          # farthest cell is 99 + 99 steps away
print('100x100 with one rotten corner: 198 minutes (Manhattan distance to the opposite corner)')
```

**Output (my run):**
```
4 prompt examples ok
2000 seeded random grids: multi-source BFS == minute-by-minute simulation; input untouched
exhaustive on all 729 2x3 grids: ok
grid [[2,1,1,1,2]]: correct 2 | single-source (first rotten only) 3
single-source BFS wrong on 1409 of 2000 seeded 4x5 grids
100x100 with one rotten corner: 198 minutes (Manhattan distance to the opposite corner)
```

**Edge cases:**
- No fresh orange: 0, even if there is no rotten one. Fresh but no rotten: -1.
- A fresh orange walled off by empty cells: -1.
- All rotten, or all empty: 0.
- 100 x 100 with one corner rotten: 198 minutes (Manhattan distance).

**Follow-ups:**
- *Do not mutate the input?* We copy the grid; or track `seen` separately.
- *Walls and gates (distance to nearest gate)?* Same multi-source seeding.
- *Why stop when `fresh == 0`?* Otherwise the queue's final level adds an extra, wrong minute.

**Common mistakes:**
- Off-by-one: counting the final level when nothing rots in it.
- Running a separate BFS from each rotten orange.
- Not counting fresh oranges, then having to rescan the grid.
- Returning 0 instead of -1 when a fresh orange is unreachable.
