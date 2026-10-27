# Book 5 — Part 9: Graphs (BFS/DFS, Topological Sort, Dijkstra, Union-Find)

**Topic:** Python DSA for product-company interviews: graph representations (adjacency list, adjacency matrix, edge list; directed, undirected and weighted; building them from an edge list and the cost of each), BFS and DFS written iteratively (and why recursive DFS is limited by CPython's recursion limit of 1000), connected components, number of islands and grids as implicit graphs, flood fill, clone graph, shortest paths in unweighted graphs (BFS, grid variants, 8-directional moves), multi-source BFS (rotting oranges, walls and gates, shortest bridge), word ladder, state-space BFS on implicit graphs (open the lock, sliding puzzle), course schedule with Kahn's algorithm and DFS three-colour topological sort, parallel courses, eventual safe nodes, alien dictionary (topological order from constraints), cycle detection in directed and undirected graphs, bipartite check, Dijkstra with heapq and lazy deletion (no decrease-key; counting pushes and stale pops; why a negative edge breaks it), minimum-effort paths, 0-1 BFS, Bellman-Ford with negative cycles, cheapest flights within k stops, Floyd-Warshall, shortest paths in a DAG, union-find (path compression, union by size, redundant connection, accounts merge, number of provinces, stones removed, number of islands II), minimum spanning tree at basic level (Kruskal and a dense Prim), minimum height trees by leaf peeling, Eulerian path and circuit as a concept (existence test only), and graph complexity (O(V + E) with lists, O(V^2) with a matrix, O((V + E) log V) for Dijkstra with a binary heap)

**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 15, ⭐⭐ 19, ⭐ 11)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns the graph algorithms listed above. Part 4 owns stacks and queues (the BFS queue idioms are cross-referenced as 'Part 4 Q4', the deque-versus-list cost, and 'Part 4 Q30', the level-order queue idiom), Part 7 owns trees (tree level-order and DFS are reused by reference as 'Part 7 Q9' and the deep-skewed-tree recursion limit as 'Part 7 Q35'; trees here appear only as a special graph in minimum height trees), Part 8 owns heaps (heapq lazy deletion, tie-breaking and priority updates without decrease-key are cross-referenced as 'Part 8 Q31', 'Part 8 Q29' and 'Part 8 Q38'; this part uses heapq only inside Dijkstra and Prim), Parts 10 and 11 own dynamic programming (shortest-path-style DP variants are handed off by part number only; Bellman-Ford and Floyd-Warshall here are the graph algorithms), and Part 14 owns advanced graphs and design problems (strongly connected components, bridges and articulation points, deeper minimum spanning tree theory such as the cut property, Boruvka and second-best trees, bipartite matching and flow, and design problems; this part gives only the basic colouring check, Kruskal and a dense Prim, and mentions them at concept level); each Part N Qn reference was checked against its heading by build.py. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: nodes are numbered 0..n-1 unless a prompt says 1..n; a graph is given as an edge list (`n` plus a list of [u, v] or [u, v, w]), an adjacency list (`graph[u]` lists neighbours) or an adjacency matrix, and each prompt states which, whether it is directed, whether repeated edges and self loops can occur, and whether weights can be negative; grids are lists of lists or lists of strings with 4-directional moves unless a prompt says 8-directional. Recursion: every prompt whose natural solution is a DFS and whose size reaches the thousands (up to 10^5 nodes or a 300 x 300 grid) says an iterative solution is required, because a recursive DFS exceeds CPython's default limit of 1000 (the claim is demonstrated: a recursive DFS on a 5000-node path raises RecursionError, while the iterative versions finish 2*10^5-node paths, a 300 x 300 all-land grid and 10^5-node random graphs); no prompt relies on raising the limit, and no claim is made about the C stack. Questions whose output is not unique say what the checker accepts: course schedule II (any order that respects every prerequisite; [] exactly when a cycle exists) and alien dictionary (any string that lists every letter once and under which the words are sorted; '' exactly when no ordering of the letters works) are validated by property and the examples show one accepted answer; topological order by DFS, the BFS and DFS visiting orders, the Dijkstra push counts and the iterative DFS variants are defined step by step so their outputs are unique; minimum spanning tree questions accept only the total weight (the trees may differ, the weight does not); redundant connection asks for the last cycle edge in input order; minimum height trees returns every optimal root; the Floyd-Warshall city question fixes the tie rule (largest index). Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P09_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force or validator on 400 seeded random small inputs per question (18000 in all), for example edge-list-to-matrix reconstruction, label propagation for components and islands, a recursive DFS and level-by-level BFS for the traversal orders, transitive closure for cycle detection, course feasibility and safe nodes, Bellman-Ford and Floyd-Warshall for Dijkstra, DAG shortest paths and network delay, a binary search on a threshold for minimum effort, removal of each edge in turn for redundant connection and undirected cycles, all subsets of n - 1 edges for Kruskal, Kruskal against Prim for the point MST, all removal orders for stones, all edge sequences for Eulerian trails, all permutations of the alphabet for the alien dictionary, all two-island pairs for the shortest bridge (minimum Manhattan distance minus one), a per-room BFS for walls and gates, all two-colourings for bipartite checks, and a full-grid flood fill after every addition for islands II. Claims tested by running code: for every one of the 720 sliding-puzzle boards the BFS agrees with a table built backwards from the goal, exactly 360 boards are solvable and the hardest needs 21 moves; the finalise-on-first-pop Dijkstra is wrong on 2897 of the three-node graphs with weights in -3..3 (without a negative cycle) and is never wrong when all weights are non-negative, while the stale-check variant matches Bellman-Ford on 1500 random negative-edge graphs; in lazy-deletion Dijkstra pushes never exceed E + 1 and stale pops always equal pushes minus reached nodes (1500 random graphs); minimum height trees have one or two roots for all 18248 labelled trees with 2 to 7 nodes; in the cheapest-flights question an in-place update and a Dijkstra with a visited set are each wrong on some random inputs (seeded counts 22 and 35 of 3000); an ordinary BFS with marking on first enqueue is wrong on the 0-1 grid problem (803 of 2000 seeded grids); the mark-on-push iterative DFS order differs from the recursive preorder on 367 of 800 random graphs while visiting the same nodes; mark-on-dequeue BFS on the binary matrix gives the same answers; a naive link of union(i, i + 1) without union by size builds a 10^5-deep parent chain, which is why `find` must be iterative; BFS entries examined are at most E (directed) or 2E (undirected) and matrix cells are n times the reached nodes. Both branches of every boolean or sentinel answer occurred in the random tests. All solutions run at the stated sizes (10^5-node graphs, a 300 x 300 grid, 5000 words for word ladder, 1000 points for Prim) in a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part09_sources.md). Searches returned graph pattern guides (techinterview.org, DesignGurus, Techie Delight), candidate-reported Flipkart rounds that mention number of islands and word ladder (Naukri Code360 and GeeksforGeeks, self-reported), and Dijkstra lazy-deletion write-ups (PracHub, Codeforces tutorials, a python-dev thread); nothing was found tying course schedule, Dijkstra, union-find or the other items to a named company, so 'Asked at' tags name source types, not verified company reports. Items such as accounts merge, alien dictionary, parallel courses, shortest bridge, minimum height trees, stones removed and sliding puzzle come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

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

### Q12 ⭐⭐⭐ 🟡 Network delay time (Dijkstra with heapq). Nodes are labelled 1..n (1 <= n <= 10^5) and `times` is a list of directed edges [u, v, w] (signal travels u -> v in w time units, 0 <= w <= 100, up to 2*10^5 edges, repeats and self loops possible). A signal is sent from node `k`. Return the time at which the last node receives it, i.e. the largest shortest-path distance from k, or -1 if some node is never reached. Use a binary heap with lazy deletion (push a new entry on each improvement and skip stale entries when popped); state the complexity in V and E and why non-negative weights are needed (see Part 8 Q31 for lazy deletion in a priority queue). Example: n=4, times=[[2, 1, 1], [2, 3, 1], [3, 4, 1]], k=2 -> 2; n=2, times=[[1, 2, 1]], k=2 -> -1; n=1, times=[], k=1 -> 0; n=3, times=[[1, 2, 5], [1, 3, 2], [3, 2, 1]], k=1 -> 3.
**Asked at:** Dijkstra and lazy-deletion write-ups (a PracHub guide on Dijkstra stale heap entries and negative edges, Codeforces lazy-deletion tutorials, a python-dev heapq thread; search snippets only, not opened; docs.python.org was unreachable) | Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened)

**Pattern:** Single-source shortest path with non-negative weights: Dijkstra with a binary heap. The answer is the largest shortest distance (the signal reaches the last node then), or -1 if any node has distance infinity.

**Say this first (1 line):** "Dijkstra with heapq and lazy deletion: push on every improvement, skip stale pops, answer is max distance or -1; it needs weights >= 0."

**Brute force:** Bellman-Ford. Relax every edge, repeat n times. O(V * E) = 10^5 * 2*10^5 = 2*10^10. Too slow, but it is a fine checker and it also copes with negative weights.

**Optimal:**
- `dist[k] = 0`, heap holds `(distance, node)`.
- Pop the smallest. If `d > dist[u]` the entry is stale (a better one was pushed later), skip it.
- Otherwise relax each edge `u -> v`: if `d + w < dist[v]`, update and push `(d + w, v)`.
- `heapq` has no decrease-key, so we push a duplicate and ignore the old one when it surfaces (same trick as Part 8 Q31).
- Invariant: when a node is popped non-stale, its distance is final. Any other path must leave the settled set through an edge to a node whose heap key is >= d, and weights are >= 0, so it cannot be shorter.
- Why non-negative: with a negative edge, a node popped earlier could still be improved later through that edge. The invariant breaks. Use Bellman-Ford then.
- Ties: the heap entries are `(int, int)` so ties compare on the node and never raise TypeError (Part 8 Q29 covers tied unorderable payloads).

**Complexity:**
- Each push comes from a successful relaxation, so pushes <= E + 1 (the +1 is the source). Each pop costs O(log heap size) and log(E + 1) <= 2 log V, so O(log V).
- Time O((V + E) log V). Space O(V + E) for adjacency lists plus up to E + 1 heap entries.
- Zero weights are fine. Repeated edges and self loops are harmless: a self loop never improves anything.

**Dry run:** `n=3, times=[[1,2,5],[1,3,2],[3,2,1]], k=1`.
- Heap `[(0,1)]`. Pop (0,1): relax 1->2 gives dist[2]=5, push (5,2); relax 1->3 gives dist[3]=2, push (2,3).
- Pop (2,3): relax 3->2: 2+1=3 < 5, dist[2]=3, push (3,2).
- Pop (3,2): fine, no out edges. Pop (5,2): 5 > 3, stale, skip.
- dist = [0, 3, 2], max = 3.

**Code:**

```python
import heapq, itertools, random
random.seed(12)
INF = float('inf')

def network_delay(n, times, k):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in times:
        adj[u].append((v, w))
    dist = [INF] * (n + 1)
    dist[k] = 0
    heap = [(0, k)]
    pushes, stale = 1, 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:            # stale entry: a better one was already processed
            stale += 1
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
                pushes += 1
    best = max(dist[1:])
    return (-1 if best == INF else best), pushes, stale

def delay(n, times, k):
    return network_delay(n, times, k)[0]

def brute(n, times, k):            # Bellman-Ford, n rounds over the edge list
    d = [INF] * (n + 1)
    d[k] = 0
    for _ in range(n):
        for u, v, w in times:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    best = max(d[1:])
    return -1 if best == INF else best

# examples
assert delay(4, [[2, 1, 1], [2, 3, 1], [3, 4, 1]], 2) == 2
assert delay(2, [[1, 2, 1]], 2) == -1
assert delay(1, [], 1) == 0
assert delay(3, [[1, 2, 5], [1, 3, 2], [3, 2, 1]], 1) == 3
print("examples ok: 2 -1 0 3")

# edge cases: self loop, repeated edges, zero weights, unreachable
assert delay(2, [[1, 1, 7], [1, 2, 4], [1, 2, 3], [1, 2, 9]], 1) == 3
assert delay(3, [[1, 2, 0], [2, 3, 0]], 1) == 0
assert delay(3, [[1, 2, 1]], 1) == -1
print("edge cases ok")

# seeded cross-check against Bellman-Ford
for _ in range(600):
    n = random.randint(1, 7)
    times = [[random.randint(1, n), random.randint(1, n), random.randint(0, 9)] for _ in range(random.randint(0, 14))]
    k = random.randint(1, n)
    assert delay(n, times, k) == brute(n, times, k), (n, times, k)
print("600 random cases match Bellman-Ford")

# exhaustive: all 3-node graphs, each ordered pair absent or weight 0/1/2
pairs = [(u, v) for u in (1, 2, 3) for v in (1, 2, 3) if u != v]
cnt = 0
for ws in itertools.product([None, 0, 1, 2], repeat=len(pairs)):
    times = [[u, v, w] for (u, v), w in zip(pairs, ws) if w is not None]
    for k in (1, 2, 3):
        r, pushes, stale = network_delay(3, times, k)
        assert r == brute(3, times, k) and pushes <= len(times) + 1
        cnt += 1
print("exhaustive 3-node graphs:", cnt, "runs, results match, pushes <= E + 1 always")

# why non-negative weights: finalise-on-first-pop breaks with a negative edge
def finalise_on_pop(n, times, k):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in times:
        adj[u].append((v, w))
    dist = [INF] * (n + 1); dist[k] = 0; done = set(); heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in done: continue
        done.add(u)
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist[1:]
neg = [[1, 2, 1], [1, 3, 2], [3, 2, -3]]
print("negative edge: finalise-on-pop gives", finalise_on_pop(3, neg, 1), "but true distances are", [0, -1, 2])

# scale: 10^5 nodes, 2*10^5 edges, iterative so no recursion issue
n = 10**5
times = [[i, i + 1, random.randint(0, 100)] for i in range(1, n)]
times += [[random.randint(1, n), random.randint(1, n), random.randint(0, 100)] for _ in range(n + 1)]
r, pushes, stale = network_delay(n, times, 1)
print("n=1e5, E=%d: delay=%d, pushes=%d (<= E+1), stale pops=%d" % (len(times), r, pushes, stale))
assert pushes <= len(times) + 1
```

**Output (my run):**

```text
examples ok: 2 -1 0 3
edge cases ok
600 random cases match Bellman-Ford
exhaustive 3-node graphs: 12288 runs, results match, pushes <= E + 1 always
negative edge: finalise-on-pop gives [0, 1, 2] but true distances are [0, -1, 2]
n=1e5, E=200000: delay=1257, pushes=107206 (<= E+1), stale pops=7206
```

**Edge cases:**
- n = 1 and no edges: answer 0.
- Source cannot reach some node: -1 (check `max(dist) == INF`).
- Self loops, repeated edges with different weights (the cheapest wins), zero-weight edges.
- Nodes are 1-indexed, so allocate n + 1 and ignore index 0 when taking the max.
- Do not forget that the answer is the max over all nodes, not the distance to one target.

**Follow-ups:**
- Negative edges? Dijkstra with finalise-on-pop gives wrong answers (the run above shows 1 instead of -1). Use Bellman-Ford O(V E), and a negative cycle reachable from k makes distances undefined.
- Dense graph, V^2 ~ E? An O(V^2) array Dijkstra without a heap can win.
- Weights only 0 or 1? 0-1 BFS with a deque gives O(V + E).

**Common mistakes:**
- Marking a node done when it is pushed instead of when it is popped.
- Forgetting the stale check, which re-expands nodes and can blow the time bound.
- Returning the sum of distances or the distance to the last node instead of the max.
- Using n instead of n + 1 for a 1-indexed array.
- Using float `inf` comparisons carelessly: `max(dist[1:])` is fine, but `dist[0]` must be excluded.

---

### Q13 ⭐⭐⭐ 🟡 Union-find with path compression and union by size. Nodes are 0..n-1 (1 <= n <= 10^5) and `ops` is a list of up to 2*10^5 operations, each [kind, a, b] with kind 'union' or 'connected'. For 'union', merge the sets of a and b and report True if they were different sets (a merge happened) or False if already together; for 'connected', report whether a and b are in the same set without changing anything. Return `[results, num_sets, largest_set]`: the list of reported booleans in operation order, the number of sets at the end and the size of the largest set at the end. `find` must be iterative (a chain of unions without union by size can build a path of 10^5 nodes, beyond the recursion limit of 1000). State the amortised cost (inverse Ackermann) and why compression alone, or by-size alone, is already good. Example: n=5, ops=[['union', 0, 1], ['union', 1, 2], ['connected', 0, 2], ['union', 0, 2], ['connected', 3, 4]] -> [[True, True, True, False, False], 3, 3]; n=1, ops=[['union', 0, 0], ['connected', 0, 0]] -> [[False, True], 1, 1]; n=3, ops=[] -> [[], 3, 1].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Disjoint-set union (union-find). It answers "are these two in the same group" and "merge two groups" in near-constant amortised time, with no graph traversal.

**Say this first (1 line):** "Parent array, iterative find with path compression, union by size; the set count drops by one on each real merge, and I track the largest size from the root's size."

**Brute force:** Keep a label per node. `connected` compares two labels, O(1). `union` relabels every node of one group, O(n). Total O(n * ops) = 10^5 * 2*10^5 = 2*10^10. Too slow, but it is the checker.

**Optimal:**
- `parent[i] = i`, `size[i] = 1`.
- `find(x)`: walk up to the root, then walk again and point every node on the path at the root (path compression). Written as two loops, not recursion.
- `union(a, b)`: find both roots. Same root: return False. Else hang the smaller tree under the larger, add sizes, `sets -= 1`, return True.
- `connected` is just `find(a) == find(b)` and changes nothing structurally that matters (compression only shortens paths).
- Largest set at the end: `max(size[find(i)])`, or track it on each merge.
- Why iterative: without union by size, `union(i, i+1)` repeated can make a 10^5 chain; a recursive `find` on it hits CPython's limit of 1000 (the run below shows the RecursionError).

**Complexity:**
- With both tricks, m operations on n elements cost O(m * alpha(n)) amortised, where alpha is the inverse Ackermann function (at most 4 for any n you can store). Treat it as constant.
- By size alone (no compression): a node at depth h sits in a set of size >= 2^h, so depth <= log2 n and every find is O(log n) worst case. The run checks this.
- Compression alone: a single find can still be O(n) once, but it flattens the path, and the amortised cost over m ops is O(log n) per op.
- Space O(n).

**Dry run:** `n=5` and the first example.
- union(0,1): roots 0,1 differ, sizes 1,1, tie so root 0 stays, parent[1]=0, size[0]=2, sets=4, True.
- union(1,2): find(1)=0, find(2)=2, size[0]=2 >= 1, parent[2]=0, size[0]=3, sets=3, True.
- connected(0,2): both root 0, True. union(0,2): same root, False. connected(3,4): roots 3 and 4, False.
- Result `[[True, True, True, False, False], 3, 3]`.

**Code:**

```python
import random, sys
random.seed(13)

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.size = [1] * n
        self.sets = n
    def find(self, x):                 # iterative: find the root, then compress the path
        r = x
        while self.p[r] != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra                # smaller tree under the larger
        self.size[ra] += self.size[rb]
        self.sets -= 1
        return True

def solve(n, ops):
    d = DSU(n)
    res = []
    for kind, a, b in ops:
        res.append(d.union(a, b) if kind == 'union' else d.find(a) == d.find(b))
    return [res, d.sets, max(d.size[d.find(i)] for i in range(n))]

def brute(n, ops):                     # relabel the whole array on every merge, O(n) per union
    lab = list(range(n)); res = []
    for kind, a, b in ops:
        if kind == 'union':
            if lab[a] == lab[b]:
                res.append(False)
            else:
                old = lab[b]
                lab = [lab[a] if x == old else x for x in lab]
                res.append(True)
        else:
            res.append(lab[a] == lab[b])
    counts = {}
    for x in lab: counts[x] = counts.get(x, 0) + 1
    return [res, len(counts), max(counts.values())]

assert solve(5, [['union', 0, 1], ['union', 1, 2], ['connected', 0, 2], ['union', 0, 2], ['connected', 3, 4]]) == [[True, True, True, False, False], 3, 3]
assert solve(1, [['union', 0, 0], ['connected', 0, 0]]) == [[False, True], 1, 1]
assert solve(3, []) == [[], 3, 1]
print("examples ok")

for _ in range(500):
    n = random.randint(1, 9)
    ops = [[random.choice(['union', 'connected']), random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 14))]
    assert solve(n, ops) == brute(n, ops), (n, ops)
print("500 random cases match the relabel brute force")

# the recursion-limit failure: a plain recursive find on the chain that unions build without size
def find_recursive(p, x):
    return x if p[x] == x else find_recursive(p, p[x])
n = 10**5
chain = list(range(n))
for i in range(n - 1):                 # union(i, i+1) always linking root(i) under root(i+1), no size rule
    chain[i] = i + 1
try:
    find_recursive(chain, 0)
except RecursionError:
    print("recursive find on a 1e5 chain: RecursionError (limit %d)" % sys.getrecursionlimit())

# the same chain through the iterative DSU with union by size: tiny depth, no error
big = solve(n, [['union', i, i + 1] for i in range(n - 1)] + [['connected', 0, n - 1]])
assert big[0][-1] is True and big[1] == 1 and big[2] == n
print("iterative DSU, 1e5 chained unions: sets=%d largest=%d" % (big[1], big[2]))

# union by size alone (NO compression): tree height stays <= log2(n)
def height_by_size_only(n, pairs):
    p = list(range(n)); sz = [1] * n
    def root(x):
        while p[x] != x: x = p[x]
        return x
    for a, b in pairs:
        ra, rb = root(a), root(b)
        if ra != rb:
            if sz[ra] < sz[rb]: ra, rb = rb, ra
            p[rb] = ra; sz[ra] += sz[rb]
    worst = 0
    for x in range(n):
        d = 0
        while p[x] != x: x = p[x]; d += 1
        worst = max(worst, d)
    return worst
worst = 0
for _ in range(400):
    n2 = random.randint(1, 64)
    h = height_by_size_only(n2, [(random.randrange(n2), random.randrange(n2)) for _ in range(random.randint(0, 150))])
    assert 2 ** h <= n2, (n2, h)       # a node at depth h implies a set of size >= 2^h
    worst = max(worst, h)
print("by-size only: 400 random runs, max depth seen %d, always 2^depth <= n" % worst)

# compression alone: the first find on the chain is O(n), but it flattens the whole path
p = list(range(1000))
for i in range(999): p[i] = i + 1
d = DSU(1000); d.p = p
d.find(0)
assert all(d.p[i] == 999 for i in range(1000))
print("compression only: one find on a 1000-chain walks 999 links and flattens every node to the root")
```

**Output (my run):**

```text
examples ok
500 random cases match the relabel brute force
recursive find on a 1e5 chain: RecursionError (limit 1000)
iterative DSU, 1e5 chained unions: sets=1 largest=100000
by-size only: 400 random runs, max depth seen 4, always 2^depth <= n
compression only: one find on a 1000-chain walks 999 links and flattens every node to the root
```

**Edge cases:**
- `union(x, x)` is False (already together) and does not change counts.
- `connected(x, x)` is always True.
- n = 1, empty `ops`: largest set is 1, set count is n.
- Many repeated unions of the same pair: only the first returns True.
- Do not mutate sizes on `connected`.

**Follow-ups:**
- Union by rank instead of size? Same bound; size is handy when the question asks for component sizes.
- Path halving (`p[x] = p[p[x]]`) is a one-pass alternative with the same amortised bound.
- Need to undo unions (offline dynamic connectivity)? Drop path compression, keep union by size and a rollback stack, each find is O(log n).

**Common mistakes:**
- A recursive `find` on a chain: RecursionError at depth 1000.
- Comparing nodes instead of roots when deciding union size or equality.
- Reading `size[x]` for a non-root `x` when computing the largest set (use `size[find(x)]`).
- Forgetting to decrement the set count only on a real merge.
- Adding sizes after swapping the roots in the wrong order.

---

### Q14 ⭐⭐⭐ 🟡 Redundant connection (union-find). `edges` is a list of n undirected edges [u, v] (3 <= n <= 1000) on nodes 1..n: the graph is connected, simple (no repeats, no self loops) and is a tree plus exactly one extra edge. Return the edge that can be removed so that what is left is a tree; if several edges qualify (every edge on the single cycle does), return the one that appears last in `edges`. Explain why scanning with union-find and returning the first edge whose endpoints are already joined gives exactly that edge. Example: edges=[[1, 2], [1, 3], [2, 3]] -> [2, 3]; edges=[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]] -> [1, 4]; edges=[[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]] -> [1, 3].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Union-find as an online cycle detector. Add edges one by one; the first edge whose two ends are already in the same set closes a cycle.

**Say this first (1 line):** "Scan the edges with union-find and return the first edge whose endpoints already share a root; that is the last edge of the cycle in input order."

**Brute force:** For each edge from the back, remove it and test whether the other n - 1 edges still connect all nodes (DFS). The first one that keeps the graph connected is the answer. O(n) edges times O(n) DFS = O(n^2), about 10^6 for n = 1000. Fine here, and it is the checker.

**Optimal:**
- `parent[i] = i` for nodes 1..n.
- For each `[u, v]` in order: find both roots. Equal: return `[u, v]`. Different: link them.
- Why this is exactly the wanted edge: the graph is a tree plus one edge, so it has exactly one cycle. Before the scan reaches the last cycle edge, the cycle's edges seen so far form a path (no cycle yet), so no earlier edge finds its ends already joined. When the last cycle edge arrives, the rest of the cycle is already there, so its ends are joined. Edges not on the cycle can never have both ends joined by earlier edges, because the only second route between two nodes goes around the cycle.
- Every cycle edge can be removed (removing any edge of a cycle leaves a spanning tree), and the one that appears last in the list is the one the scan returns.

**Complexity:** O(n * alpha(n)) time, O(n) space. A single pass.

**Dry run:** `edges=[[1,4],[3,4],[1,3],[1,2],[4,5]]`.
- [1,4]: roots 1,4 differ, link. [3,4]: 3 and root of 4 differ, link (now {1,3,4}).
- [1,3]: both already in {1,3,4}, same root, return `[1, 3]`.
- Cycle is 1-4-3-1 with edges [1,4],[3,4],[1,3]; the last of them in the list is [1,3]. Correct.

**Code:**

```python
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
```

**Output (my run):**

```text
examples ok
exhaustive n=3..5: 91170 inputs, union-find answer == last removable edge each time
500 random n=6..9 cases ok
removable edges: [[1, 2], [2, 3], [3, 1]] -> answer [3, 1]
n=1000 path plus closing edge ok
```

**Edge cases:**
- Smallest case: a triangle. The third edge is returned.
- Edge order matters: the same graph in a different order returns a different edge. Endpoint order inside the answer must be as given (`[1, 3]`, not `[3, 1]`).
- The extra edge may connect nodes far apart (long cycle) or neighbours (cycle of length 3).
- The cycle edge is not always the last edge of the input; extra tree edges can come after it (example 2).

**Follow-ups:**
- Directed version (a rooted tree plus one extra edge)? Harder: a node may get two parents, or a cycle appears; handle the two-parents case by trying to drop each candidate edge.
- Which edges are *on* the cycle? Remove leaves repeatedly (degree 1 peeling); what is left is the cycle.
- Return all edges that could be removed? Walk the cycle: the edges on the path between the closing edge's endpoints plus the closing edge.

**Common mistakes:**
- Returning the first removable edge in input order instead of the last. The prompt wants the last.
- Using the DFS "parent node" trick for the cycle test and still returning edges in the wrong order.
- Forgetting 1-indexing and allocating `n` instead of `n + 1` slots.
- Reversing the endpoints in the answer.

---

### Q15 ⭐⭐⭐ 🔴 Word ladder: shortest transformation length. `begin` and `end` are lowercase words of the same length L (1 <= L <= 10) and `word_list` a list of distinct lowercase words of length L (1 <= len <= 5000). One move changes exactly one letter and the new word must be in `word_list` (`begin` itself need not be). Return the number of words on the shortest sequence from `begin` to `end` counting both ends, or 0 if impossible (also 0 when `end` is not in `word_list`; when `begin` equals `end` and `end` is in `word_list`, return 1). Build neighbours by trying the 26 letters at each position (or with wildcard buckets such as 'h*t') instead of comparing all pairs, and give the complexity of each approach. Example: begin='hit', end='cog', word_list=['hot', 'dot', 'dog', 'lot', 'log', 'cog'] -> 5; begin='hit', end='cog', word_list=['hot', 'dot', 'dog', 'lot', 'log'] -> 0; begin='a', end='c', word_list=['a', 'b', 'c'] -> 2.
**Asked at:** Candidate-reported rounds on Naukri Code360 and GeeksforGeeks (a Flipkart 2021 report with number of islands, a Flipkart 2025 online assessment and a GeeksforGeeks on-campus 2020 report with word ladder; search-result summaries only, pages not opened; self-reported, unverified) | Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened)

**Pattern:** BFS on an implicit, unweighted graph. Words are nodes, two words are linked if they differ in exactly one letter. Shortest path in edges plus 1 equals the word count.

**Say this first (1 line):** "BFS from `begin`, generating neighbours by changing one letter at a time, with a visited set; the first time I pop `end` I have the shortest ladder."

**Brute force:** Build the whole graph by comparing every pair of words (L letters each): O(N^2 * L) = 5000^2 * 10 / 2 = about 1.25 * 10^8 character comparisons, then BFS. It works and is my checker, but it is too slow for the upper bound in Python.

**Optimal:** Two ways to get neighbours without comparing all pairs.
- Letters: for each position try the 26 letters, keep candidates that are in the word set. Cost per word: L * 26 string builds, each O(L) to build and hash, so O(26 * L^2) per word. Total O(N * 26 * L^2) = 5000 * 26 * 100 = 1.3 * 10^7.
- Buckets: map `h*t`-style patterns to the words that match. A word has L patterns; neighbours are the words in its L buckets. Build cost O(N * L^2) (L patterns of length L), BFS cost O(sum of bucket sizes touched) with no factor 26. Worst case a bucket is large, but each word is enqueued once, and each bucket is scanned once per word that contains that pattern.
- BFS invariant: nodes are dequeued in order of distance, so the first time `end` comes out its depth is minimal. Mark visited when enqueuing so nothing is queued twice.
- Return 0 at once when `end` is not in the list.

**Complexity:**
- Letters: O(N * 26 * L^2) time, O(N * L) space.
- Buckets: O(N * L^2) time to build and to search (a bucket of size B visited from each of its members costs B per member in the worst case, but the visited check keeps the queue at N), O(N * L^2) space for the pattern strings.
- All pairs: O(N^2 * L) time. For N = 5000 and L = 10 it is the slowest by far.

**Dry run:** `hit -> cog`, list `hot dot dog lot log cog`.
- Level 1: hit. Neighbours in the list: hot (hit -> hot).
- Level 2: hot. Neighbours: dot, lot. Level 3: dot -> dog; lot -> log. Level 4: dog -> cog; log -> cog (cog already queued).
- Pop cog at depth 5: hit, hot, dot, dog, cog. Answer 5.

**Code:**

```python
import itertools, random, string
from collections import deque, defaultdict
random.seed(15)
INF = float('inf')

def ladder_letters(begin, end, word_list):      # try all 26 letters at each position
    words = set(word_list)
    if end not in words:
        return 0
    seen = {begin}
    q = deque([(begin, 1)])
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for c in string.ascii_lowercase:
                x = w[:i] + c + w[i + 1:]
                if x in words and x not in seen:
                    seen.add(x)
                    q.append((x, d + 1))
    return 0

def ladder_buckets(begin, end, word_list):      # wildcard buckets: 'h*t' -> words matching it
    words = list(dict.fromkeys(word_list))
    if end not in words:
        return 0
    bucket = defaultdict(list)
    for w in words + [begin]:
        for i in range(len(w)):
            bucket[w[:i] + '*' + w[i + 1:]].append(w)
    seen = {begin}
    q = deque([(begin, 1)])
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for x in bucket[w[:i] + '*' + w[i + 1:]]:
                if x not in seen:
                    seen.add(x)
                    q.append((x, d + 1))
    return 0

def brute(begin, end, word_list):               # explicit all-pairs graph, then relax to a fixed point
    nodes = [begin] + [w for w in dict.fromkeys(word_list) if w != begin]
    if end not in word_list:
        return 0
    adj = {w: [x for x in nodes if sum(a != b for a, b in zip(w, x)) == 1] for w in nodes}
    d = {w: INF for w in nodes}; d[begin] = 1
    changed = True
    while changed:
        changed = False
        for w in nodes:
            for x in adj[w]:
                if d[w] + 1 < d[x]:
                    d[x] = d[w] + 1; changed = True
    return 0 if d[end] == INF else d[end]

wl = ['hot', 'dot', 'dog', 'lot', 'log', 'cog']
assert ladder_letters('hit', 'cog', wl) == ladder_buckets('hit', 'cog', wl) == brute('hit', 'cog', wl) == 5
assert ladder_letters('hit', 'cog', wl[:-1]) == ladder_buckets('hit', 'cog', wl[:-1]) == 0
assert ladder_letters('a', 'c', ['a', 'b', 'c']) == ladder_buckets('a', 'c', ['a', 'b', 'c']) == 2
print("examples ok: 5 0 2")

# convention when begin == end and it is in the list: one word, length 1 (the prompt does not say; all three methods agree)
assert ladder_letters('a', 'a', ['a']) == ladder_buckets('a', 'a', ['a']) == brute('a', 'a', ['a']) == 1

# exhaustive: alphabet abc, length 2 -> 9 words, every subset as word_list, every begin and end
allw = [''.join(p) for p in itertools.product('abc', repeat=2)]
cnt = 0
for mask in range(1, 1 << 9):
    wl = [w for i, w in enumerate(allw) if mask >> i & 1]
    for b in allw:
        for e in allw:
            r = ladder_letters(b, e, wl)
            assert r == ladder_buckets(b, e, wl) == brute(b, e, wl), (b, e, wl)
            cnt += 1
print("exhaustive abc/length 2: %d cases, all three methods agree" % cnt)

for _ in range(300):
    L = random.randint(1, 4)
    ws = list({''.join(random.choice('abc') for _ in range(L)) for _ in range(random.randint(1, 12))})
    b = ''.join(random.choice('abc') for _ in range(L)); e = random.choice(ws)
    assert ladder_letters(b, e, ws) == ladder_buckets(b, e, ws) == brute(b, e, ws)
print("300 random cases ok")

# edge cases
assert ladder_letters('abc', 'xyz', ['xyz']) == 0          # no one-letter path
assert ladder_letters('abc', 'abd', ['abd']) == 2          # begin not in the list
assert ladder_letters('abc', 'abd', ['abc']) == 0          # end not in the list
print("edge cases ok")

# scale: 5000 words of length 10 (complexity depends on neighbour structure, not only the pair count)
ws = list({''.join(random.choice(string.ascii_lowercase) for _ in range(10)) for _ in range(5000)})
r1 = ladder_letters(ws[0], ws[1], ws); r2 = ladder_buckets(ws[0], ws[1], ws)
assert r1 == r2
print("5000 random 10-letter words: both give", r1, "(random words are rarely 1 letter apart)")
dense = [''.join(p) for p in itertools.product('abcde', repeat=4)][:625]
assert ladder_letters('aaaa', 'eeee', dense) == ladder_buckets('aaaa', 'eeee', dense) == 5
print("625 dense 4-letter words over 'abcde': shortest ladder aaaa -> eeee has", ladder_letters('aaaa', 'eeee', dense), "words")
```

**Output (my run):**

```text
examples ok: 5 0 2
exhaustive abc/length 2: 41391 cases, all three methods agree
300 random cases ok
edge cases ok
5000 random 10-letter words: both give 0 (random words are rarely 1 letter apart)
625 dense 4-letter words over 'abcde': shortest ladder aaaa -> eeee has 5 words
```

**Edge cases:**
- `end` not in `word_list`: 0 (even if reachable in the abstract).
- `begin` is not required to be in the list; it is only the start.
- No path: BFS ends with an empty queue, return 0.
- `begin == end`: the prompt does not say. All my methods return 1 when `end` is in the list (a one-word sequence). A checker that expects something else would need that stated.
- L = 1: every pair of different one-letter words is a neighbour.
- Duplicates are excluded by the prompt (distinct words), but a `set` handles them anyway.

**Follow-ups:**
- Print the actual ladder? Store a parent pointer per word and walk back from `end`.
- Faster for huge lists? Bidirectional BFS: expand the smaller frontier each step; roughly cuts the work from b^d to 2 * b^(d/2).
- All shortest ladders (Word Ladder II)? BFS to get levels, then DFS or backtracking over parents; the number of answers can be exponential.

**Common mistakes:**
- Counting edges instead of words (off by one: the answer counts both ends).
- Comparing all pairs; times out.
- Marking visited on dequeue, so the same word is queued many times.
- Using a list for `word_list` membership (O(N) per test); convert to a set.
- Forgetting to check that `end` is in the list.

---

### Q16 ⭐⭐ 🟢 Counting the work of BFS on lists versus a matrix (graph complexity). `edges` are [u, v] pairs on nodes 0..n-1 (1 <= n <= 60, no self loops, no repeated edges; for an undirected graph [u, v] and [v, u] are not both given), `directed` says whether they are one-way, and `src` is the start node. Run a standard BFS that marks nodes on enqueue. Return `[reached, entries_list, cells_matrix]`: `reached` is the number of nodes dequeued; `entries_list` is the number of adjacency-list entries examined when the graph is stored as adjacency lists (the sum of out-degrees of reached nodes); `cells_matrix` is the number of matrix cells examined when the graph is an n x n matrix (n per reached node). Then state why BFS and DFS are O(V + E) with lists and O(V^2) with a matrix, why an undirected edge is examined twice, and the bound O((V + E) log V) for Dijkstra with a binary heap (why log E is at most 2 log V). Example: n=5, edges=[[0, 1], [1, 2], [2, 0], [3, 4]], directed=False, src=0 -> [3, 6, 15]; n=4, edges=[[0, 1], [1, 2], [2, 3]], directed=True, src=1 -> [3, 2, 12]; n=3, edges=[], directed=True, src=2 -> [1, 0, 3].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Cost model of graph storage. BFS is the same algorithm either way; what changes is how much it costs to ask "who are the neighbours of u".

**Say this first (1 line):** "BFS touches each reached node once and scans its neighbours: with lists that is the out-degree, so O(V + E); with a matrix it is a whole row of n cells, so O(V^2)."

**Brute force:** Not a different algorithm here. The "brute" is the matrix version: build an n x n matrix and scan a full row per dequeued node. It is also my checker, because it counts cells by actually scanning.

**Optimal:** Adjacency lists, with BFS marking nodes when they are enqueued.
- `reached`: nodes dequeued (each at most once, since marked on enqueue).
- `entries_list`: for each dequeued node add `len(adj[u])`. In an undirected graph an edge `[u, v]` is stored in both lists, so it is examined from each end.
- `cells_matrix`: `n * reached`, because the row of a node is scanned in full whether it has 1 neighbour or 50.

**Complexity:**
- BFS or DFS with lists: each node dequeued once, each list entry examined once. Entries sum to E (directed) or 2E (undirected). Time O(V + E), space O(V + E) for the lists plus O(V) for the queue and seen set.
- With a matrix: O(V) rows times O(V) cells = O(V^2) time, O(V^2) space. Better only when the graph is dense (E near V^2); then V^2 and V + E are the same order.
- Dijkstra with a binary heap: at most E + 1 pushes, each push and pop O(log heap size). In a simple graph E <= V^2, so log E <= 2 log V, and the heap work is O(E log V). Add the V + E scanning: O((V + E) log V).
- Check the claim on small graphs: the run tries every directed graph on up to 4 nodes and every undirected one, and `E <= n^2` and `entries <= E or 2E` hold in all of them.

**Dry run:** `n=5, edges=[[0,1],[1,2],[2,0],[3,4]]`, undirected, src 0.
- Lists: 0:[1,2], 1:[0,2], 2:[1,0], 3:[4], 4:[3].
- Dequeue 0 (2 entries), then 1 (2), then 2 (2). Nodes 3 and 4 are never reached.
- reached = 3, entries = 2 + 2 + 2 = 6, cells = 3 rows * 5 = 15. Answer `[3, 6, 15]`.

**Code:**

```python
import itertools, random
from collections import deque
random.seed(16)

def bfs_lists(n, edges, directed, src):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)                  # an undirected edge is stored twice
    seen = {src}
    q = deque([src])
    reached = entries = 0
    while q:
        u = q.popleft()
        reached += 1
        entries += len(adj[u])                # every list entry of a dequeued node is examined
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return [reached, entries, n * reached]    # a matrix row has n cells, scanned once per reached node

def bfs_matrix_counted(n, edges, directed, src):   # really scans the matrix and counts cells and ones
    mat = [[0] * n for _ in range(n)]
    for u, v in edges:
        mat[u][v] = 1
        if not directed:
            mat[v][u] = 1
    seen = {src}
    q = deque([src])
    reached = entries = cells = 0
    while q:
        u = q.popleft()
        reached += 1
        for v in range(n):
            cells += 1
            if mat[u][v]:
                entries += 1
                if v not in seen:
                    seen.add(v)
                    q.append(v)
    return [reached, entries, cells]

assert bfs_lists(5, [[0, 1], [1, 2], [2, 0], [3, 4]], False, 0) == [3, 6, 15]
assert bfs_lists(4, [[0, 1], [1, 2], [2, 3]], True, 1) == [3, 2, 12]
assert bfs_lists(3, [], True, 2) == [1, 0, 3]
print("examples ok")

# exhaustive: every directed graph on n <= 4 nodes, every source; every undirected graph with every orientation choice
cnt = 0
for n in range(1, 5):
    allp = [(u, v) for u in range(n) for v in range(n) if u != v]
    for mask in range(1 << len(allp)):
        es = [list(p) for i, p in enumerate(allp) if mask >> i & 1]
        for s in range(n):
            r = bfs_lists(n, es, True, s)
            assert r == bfs_matrix_counted(n, es, True, s)
            assert r[1] <= len(es) and len(es) <= n * n and r[0] <= n
            cnt += 1
    und = [(u, v) for u in range(n) for v in range(u + 1, n)]
    for mask in range(1 << len(und)):
        es = [[u, v] if (u + v + mask) % 2 else [v, u] for i, (u, v) in enumerate(und) if mask >> i & 1]
        for s in range(n):
            r = bfs_lists(n, es, False, s)
            assert r == bfs_matrix_counted(n, es, False, s)
            assert r[1] <= 2 * len(es)
            cnt += 1
print("exhaustive n<=4: %d (graph, source) runs; list count == scanned matrix ones; entries <= E (directed) or 2E (undirected); E <= n^2" % cnt)

# random larger graphs up to n = 60
for _ in range(300):
    n = random.randint(1, 60); d = random.random() < .5
    pool = [(u, v) for u in range(n) for v in range(n) if u != v and (d or u < v)]
    es = [list(p) for p in random.sample(pool, random.randint(0, min(len(pool), 150)))]
    s = random.randrange(n)
    assert bfs_lists(n, es, d, s) == bfs_matrix_counted(n, es, d, s)
print("300 random graphs (n <= 60) agree")

# the shape of the gap: a path of 60 nodes, directed, from node 0
n = 60; path = [[i, i + 1] for i in range(n - 1)]
r = bfs_lists(n, path, True, 0)
print("path of 60: reached=%d list entries=%d matrix cells=%d" % tuple(r))
assert r == [60, 59, 3600]
# undirected: each edge examined twice
r = bfs_lists(n, path, False, 0)
print("same path undirected: list entries=%d (= 2E = %d)" % (r[1], 2 * len(path)))
assert r[1] == 2 * len(path)
```

**Output (my run):**

```text
examples ok
exhaustive n<=4: 16870 (graph, source) runs; list count == scanned matrix ones; entries <= E (directed) or 2E (undirected); E <= n^2
300 random graphs (n <= 60) agree
path of 60: reached=60 list entries=59 matrix cells=3600
same path undirected: list entries=118 (= 2E = 118)
```

**Edge cases:**
- No edges: only the source is reached, entries 0, cells n.
- Unreachable parts of the graph cost nothing in the list version (never dequeued).
- Directed versus undirected: the same edge list gives different entry counts (E versus 2E for the part that is reached).
- The count is for BFS that marks on enqueue; marking on dequeue would examine entries of duplicates too.

**Follow-ups:**
- When is a matrix the right choice? Dense graphs, and when you need O(1) "is there an edge u-v" (Floyd-Warshall also wants it).
- Edge list as the storage? Neighbour lookup is O(E) per node, so BFS becomes O(V * E); build lists first (Kruskal is the case where an edge list is natural).
- Memory for V = 10^5? A matrix would be 10^10 cells, impossible; lists are the only option.

**Common mistakes:**
- Saying undirected BFS is O(E) with no 2: the work is 2E entries, same order but worth saying.
- Claiming BFS is O(V + E) for a matrix input: it is O(V^2).
- Writing Dijkstra as O(E log E) without noting it equals O(E log V).
- Counting all n nodes instead of only reached nodes in the matrix cost.

---

### Q17 ⭐⭐ 🟢 Number of provinces from an adjacency matrix. `is_connected` is an n x n matrix of 0 and 1 (1 <= n <= 200) that is symmetric with 1s on the diagonal; `is_connected[i][j] = 1` means cities i and j are directly connected. A province is a group of cities connected directly or indirectly. Return the number of provinces. Give both a traversal and a union-find solution and state the complexity for a matrix input (reading it is already O(n^2)). Example: is_connected=[[1, 1, 0], [1, 1, 0], [0, 0, 1]] -> 2; is_connected=[[1, 0, 0], [0, 1, 0], [0, 0, 1]] -> 3; is_connected=[[1]] -> 1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Connected components on a graph given as an adjacency matrix. A province is one component.

**Say this first (1 line):** "Count components: start a traversal from every unseen city and add one each time; or union-find and subtract one per real merge. Either way it is O(n^2) because the matrix has n^2 cells."

**Brute force:** Transitive closure with Warshall (three nested loops over n), then count cities that are the smallest member of their group. O(n^3) = 8 * 10^6 for n = 200. Fine here, and it is my checker.

**Optimal:** Two standard solutions.
- Traversal: `seen` array. For each city not seen, `count += 1` and run DFS or BFS over `row[v] == 1` neighbours. I use an explicit stack so there is no recursion-limit worry. Mark when pushing.
- Union-find: start with `count = n`. For each pair `i < j` with `is_connected[i][j] == 1`, union them; every successful merge does `count -= 1`. Only the upper triangle is needed because the matrix is symmetric.
- Invariant (traversal): each traversal visits exactly one whole component, so the number of traversal starts is the number of components.

**Complexity:**
- Both read the matrix, which alone is O(n^2). Traversal: each node dequeued once, a row scan of n cells each, so O(n^2). Union-find: n^2/2 cell checks plus at most n - 1 merges at O(alpha(n)). O(n^2) total.
- Space O(n) extra (seen or parent array), not counting the input.
- With n = 200 this is 40,000 cells; trivial.

**Dry run:** `[[1,1,0],[1,1,0],[0,0,1]]`.
- Traversal: start at 0 (count 1), see 1 connected, mark it; row 1 gives 0 (seen). Start at 2 (count 2). Answer 2.
- Union-find: count = 3. Pair (0,1) is 1, roots differ, merge, count = 2. Pairs (0,2), (1,2) are 0. Answer 2.

**Code:**

```python
import itertools, random
random.seed(17)

def provinces_dfs(m):                       # iterative DFS with an explicit stack
    n = len(m)
    seen = [False] * n
    count = 0
    for s in range(n):
        if seen[s]:
            continue
        count += 1
        seen[s] = True
        stack = [s]
        while stack:
            u = stack.pop()
            row = m[u]
            for v in range(n):
                if row[v] and not seen[v]:
                    seen[v] = True
                    stack.append(v)
    return count

def provinces_uf(m):
    n = len(m)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    count = n
    for i in range(n):
        for j in range(i + 1, n):           # symmetric: only the upper triangle is needed
            if m[i][j]:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    count -= 1
    return count

def brute(m):                               # transitive closure (Warshall), then count distinct rows' minimum members
    n = len(m)
    r = [[bool(x) for x in row] for row in m]
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]:
                        r[i][j] = True
    return sum(1 for i in range(n) if not any(r[i][j] for j in range(i)))   # i is the smallest member of its group

cases = [([[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2), ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3), ([[1]], 1)]
for m, exp in cases:
    assert provinces_dfs(m) == provinces_uf(m) == brute(m) == exp
print("examples ok: 2 3 1")

cnt = 0
for n in range(1, 6):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                m[i][j] = m[j][i] = 1
        a = provinces_dfs(m)
        assert a == provinces_uf(m) == brute(m)
        cnt += 1
print("exhaustive: all %d symmetric matrices with n <= 5 agree (DFS, union-find, Warshall closure)" % cnt)

for _ in range(200):
    n = random.randint(1, 30); p = random.random() * 0.15
    m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                m[i][j] = m[j][i] = 1
    assert provinces_dfs(m) == provinces_uf(m) == brute(m)
print("200 random n <= 30 matrices agree")

n = 200
ident = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
full = [[1] * n for _ in range(n)]
chain = [[1 if abs(i - j) <= 1 else 0 for j in range(n)] for i in range(n)]
print("n=200: identity ->", provinces_dfs(ident), "| all ones ->", provinces_uf(full), "| chain ->", provinces_dfs(chain))
assert (provinces_dfs(ident), provinces_dfs(full), provinces_uf(chain)) == (200, 1, 1)
```

**Output (my run):**

```text
examples ok: 2 3 1
exhaustive: all 1099 symmetric matrices with n <= 5 agree (DFS, union-find, Warshall closure)
200 random n <= 30 matrices agree
n=200: identity -> 200 | all ones -> 1 | chain -> 1
```

**Edge cases:**
- n = 1: one province.
- Identity matrix: n provinces. All ones: 1 province.
- The diagonal is always 1; do not treat `m[i][i]` as a union (it would be a no-op anyway).
- Indirect connection: 0-1 and 1-2 joined, 0-2 not directly: still one province (the chain case).

**Follow-ups:**
- Input as an edge list instead? Union-find or list-based BFS in O(V + E); no need to ever build a matrix.
- Return the sizes of the provinces? Keep a counter per traversal, or use union by size.
- Cities added over time? Union-find answers it online (see Number of Islands II in this part).

**Common mistakes:**
- Treating the matrix like an edge list and running O(n^3).
- Recursive DFS with n = 200 is fine, but the habit fails at 10^5; write the stack version.
- Counting the number of 1s or the number of rows with a 1.
- Forgetting `seen` marking on the neighbour loop and revisiting nodes.

---

### Q18 ⭐⭐ 🟡 Shortest path in a binary matrix with 8-directional moves. `grid` is an n x n matrix (1 <= n <= 100) of 0 (open) and 1 (blocked). You move between cells that share an edge or a corner. Return the number of cells on the shortest path from the top-left to the bottom-right cell (both endpoints counted), or -1 if either endpoint is blocked or no path exists. State why BFS is right and why marking a cell when it is enqueued (not when it is dequeued) matters for the queue size. Example: grid=[[0, 1], [1, 0]] -> 2; grid=[[0, 0, 0], [1, 1, 0], [1, 1, 0]] -> 4; grid=[[1, 0], [0, 0]] -> -1; grid=[[0]] -> 1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** BFS on a grid as an implicit graph. Every move costs 1, so BFS order is shortest-path order. The only change from the 4-direction version is 8 neighbour offsets.

**Say this first (1 line):** "BFS from the top-left with 8 directions, mark a cell when I enqueue it, and the depth of the bottom-right cell is the answer, counted in cells."

**Brute force:** Distance relaxation: set `dist[start] = 1`, then keep sweeping every open cell and its 8 neighbours until nothing improves. Each sweep is O(n^2), and up to O(n^2) sweeps, so O(n^4) = 10^8 for n = 100. It is my checker, not the solution.

**Optimal:**
- If either endpoint is 1, return -1 at once.
- Queue of `(row, col, length)`, start `(0, 0, 1)` (cells counted, so the start is 1).
- Pop a cell, if it is the target return its length. Otherwise for each of 8 offsets in bounds, open, and not seen: mark seen, push with length + 1.
- Why BFS is right: all edges have the same cost, so cells leave the queue in non-decreasing length. The first time the target is dequeued is its shortest length.
- Why mark on enqueue: a cell is reached first by the shortest route, so later routes to it are useless. If you mark on dequeue, the same cell can sit in the queue several times (up to once per neighbour, so up to 8). The answer stays correct, but the queue is bigger and you do repeated work. The run shows peak queue 199 against 788 on an open 100 x 100 grid.

**Complexity:** O(n^2) time (each cell enqueued once, 8 neighbour checks each), O(n^2) space for the seen array and the queue (the queue holds at most one frontier, which is O(n) in practice).

**Dry run:** `[[0,0,0],[1,1,0],[1,1,0]]`.
- Start (0,0) length 1. Neighbours open: (0,1) length 2. (1,0), (1,1) are blocked.
- Pop (0,1): neighbours (0,2) open, length 3. (1,2) is diagonal-adjacent too: open, length 3.
- Pop (0,2) length 3: its neighbours (1,2) already seen. Pop (1,2) length 3: neighbour (2,2) open, length 4.
- Pop (2,2): target, return 4.

**Code:**

```python
import itertools, random
from collections import deque
random.seed(18)
INF = float('inf')
D8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]

def shortest_path(grid, stats=None):         # BFS, mark when enqueued
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    seen = [[False] * n for _ in range(n)]
    seen[0][0] = True
    q = deque([(0, 0, 1)])
    peak = 1
    while q:
        x, y, d = q.popleft()
        if x == n - 1 and y == n - 1:
            if stats is not None: stats['peak'] = peak
            return d
        for dx, dy in D8:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and not seen[a][b]:
                seen[a][b] = True            # marking here means each cell enters the queue once
                q.append((a, b, d + 1))
        peak = max(peak, len(q))
    if stats is not None: stats['peak'] = peak
    return -1

def mark_on_dequeue(grid):                   # same answer, but the queue can hold a cell many times
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1, 0
    seen = set()
    q = deque([(0, 0, 1)])
    peak = 1
    while q:
        x, y, d = q.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if x == n - 1 and y == n - 1:
            return d, peak
        for dx, dy in D8:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and (a, b) not in seen:
                q.append((a, b, d + 1))
        peak = max(peak, len(q))
    return -1, peak

def brute(grid):                             # relax all cells until nothing changes (Bellman-Ford style)
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    d = {(i, j): INF for i in range(n) for j in range(n) if not grid[i][j]}
    d[(0, 0)] = 1
    changed = True
    while changed:
        changed = False
        for (x, y), v in list(d.items()):
            for dx, dy in D8:
                p = (x + dx, y + dy)
                if p in d and v + 1 < d[p]:
                    d[p] = v + 1; changed = True
    r = d[(n - 1, n - 1)]
    return -1 if r == INF else r

assert shortest_path([[0, 1], [1, 0]]) == 2
assert shortest_path([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
assert shortest_path([[1, 0], [0, 0]]) == -1
assert shortest_path([[0]]) == 1
print("examples ok: 2 4 -1 1")

cnt = 0
for n in (1, 2, 3, 4):
    for bits in itertools.product((0, 1), repeat=n * n):
        g = [list(bits[i * n:(i + 1) * n]) for i in range(n)]
        r = shortest_path(g)
        assert r == brute(g) == mark_on_dequeue(g)[0], g
        cnt += 1
print("exhaustive: all %d grids with n <= 4 agree (BFS, relaxation brute, mark-on-dequeue)" % cnt)

for _ in range(300):
    n = random.randint(5, 9)
    g = [[1 if random.random() < .3 else 0 for _ in range(n)] for _ in range(n)]
    assert shortest_path(g) == brute(g)
print("300 random n=5..9 grids ok")

# why mark on enqueue: peak queue size on an open 100 x 100 grid
n = 100
open_grid = [[0] * n for _ in range(n)]
s1 = {}
r1 = shortest_path(open_grid, s1)
r2, peak2 = mark_on_dequeue(open_grid)
assert r1 == r2 == n
print("open 100x100: answer", r1, "| peak queue, mark on enqueue:", s1['peak'], "| mark on dequeue:", peak2, "| cells:", n * n)
assert s1['peak'] <= n * n
```

**Output (my run):**

```text
examples ok: 2 4 -1 1
exhaustive: all 66066 grids with n <= 4 agree (BFS, relaxation brute, mark-on-dequeue)
300 random n=5..9 grids ok
open 100x100: answer 100 | peak queue, mark on enqueue: 199 | mark on dequeue: 788 | cells: 10000
```

**Edge cases:**
- 1 x 1 grid with 0: answer 1 (the start is the target). With 1: -1.
- Start or end blocked: -1, check before the loop.
- Target reachable only diagonally between two blocked cells (corner moves): allowed here, since cells share a corner.
- Fully blocked middle: BFS empties the queue, return -1.

**Follow-ups:**
- 4 directions only? Same code with 4 offsets.
- Return the path itself? Keep a parent array and walk it back from the target.
- Several blockers you may remove (k obstacles)? BFS over (cell, removals used), state space n^2 * k.

**Common mistakes:**
- Counting steps instead of cells (the answer counts both ends, so start at 1).
- Marking on dequeue, which inflates the queue and, with a plain set of dequeued cells, adds duplicates.
- Forgetting the blocked-start check, then returning 1 for a 1 x 1 blocked grid.
- Using `list.pop(0)` instead of `deque.popleft()` (O(n) per pop; see Part 4 Q4).
- Only 4 offsets, missing diagonal moves.

---

### Q19 ⭐⭐ 🟡 Clone a connected undirected graph. A node is `Node(val, neighbors)` where `neighbors` is a list of Node references. You are given the node with val 1 of a connected undirected graph whose nodes have vals 1..n (0 <= n <= 100; no self loops, no repeats, cycles are possible; the node count may be 0, in which case the input is None), and must return the corresponding node of a deep copy: every node is a new object, and no new node refers to an original node. The checker builds the graph from `adj` (where `adj[i]` lists the vals of the neighbours of node i + 1, in order), runs your function, then verifies that no node of the copy is an original object and returns the adjacency list of the copy in the same format, which must equal `adj`. Explain why a dictionary from original node to copy is needed (the cycle problem) and compare a BFS and a DFS version. Example: adj=[[2, 4], [1, 3], [2, 4], [1, 3]] -> [[2, 4], [1, 3], [2, 4], [1, 3]]; adj=[[]] -> [[]]; adj=[] -> []; adj=[[2], [1, 3], [2]] -> [[2], [1, 3], [2]].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Graph traversal (BFS or DFS) with a hash map from original node to its copy. The map is both the "visited" set and the way to wire copied neighbours.

**Say this first (1 line):** "Traverse the graph once; keep a dict original -> clone; create a clone the first time I see a node, and always append the clone of each neighbour."

**Brute force:** `copy.deepcopy(node)`. It handles cycles by its own memo dict, so it is correct, but it is a library call that hides the idea, and its recursion depth equals the longest DFS path. I use it only to know the expected shape. Copying recursively with no memo is the broken idea: any cycle (even two nodes pointing at each other) recurses forever (the run shows the RecursionError).

**Optimal:**
- `None` in, `None` out.
- `copy_of = {node: Node(node.val)}`, queue (BFS) or stack (DFS) holding original nodes.
- For each popped node `u` and each neighbour `v`: if `v` has no clone yet, create it and queue `v`. Then `copy_of[u].neighbors.append(copy_of[v])`.
- Why the dict is needed: the graph has cycles and each undirected edge appears from both ends. Without a map you cannot tell "already copied" from "new", and a node would be copied once per path, or forever.
- Neighbour order is preserved because each node's neighbours are appended in the original order.
- BFS vs DFS: both are O(V + E). BFS uses a queue and no recursion. DFS recursion depth can be V; here V <= 100 so it is safe, but for 10^5 nodes use an explicit stack. For this question the choice is style.

**Complexity:** O(V + E) time (each node cloned once, each adjacency entry visited once), O(V) extra space for the map and queue, plus the O(V + E) output.

**Dry run:** `adj=[[2],[1,3],[2]]` (a path 1-2-3).
- copy_of = {1: 1'}; queue [1]. Pop 1: neighbour 2 is new, create 2', queue it; 1'.neighbors = [2'].
- Pop 2: neighbour 1 is in the map, 2'.neighbors = [1']; neighbour 3 is new, create 3'; 2'.neighbors = [1', 3'].
- Pop 3: neighbour 2 in the map, 3'.neighbors = [2']. Return 1'. The copy has the same adjacency, all new objects.

**Code:**

```python
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
```

**Output (my run):**

```text
examples ok
exhaustive: 772 connected graphs with n <= 5, BFS and DFS clones both reproduce adj, no shared nodes
200 random connected graphs (n <= 100, shuffled neighbour order) ok
no map on a 2-node cycle: RecursionError (limit 1000)
clone is a real cycle: c.neighbors[0].neighbors[0] is c -> True
```

**Edge cases:**
- Empty graph: input `None`, return `None` (the checker passes `None` when `adj == []`).
- Single node with no neighbours.
- A node adjacent to a node that points back (every edge, since the graph is undirected): handled by the map.
- Neighbour order must be kept (the checker compares lists exactly).
- The copy must not contain any original object; appending `v` instead of `copy_of[v]` is the classic leak.

**Follow-ups:**
- Directed graph, or graph not connected from the given node? Same code copies only what is reachable; for a whole graph, loop over all nodes.
- Deep graph (10^5 nodes)? The iterative BFS version already works; a recursive DFS needs an explicit stack.
- Cloning a linked list with random pointers? Same idea: map old -> new, then wire.

**Common mistakes:**
- No dict, or checking "visited" by `val` on the original but then creating a second clone anyway.
- Appending the original neighbour into the copy's list.
- Creating the clone only when a node is popped, so a neighbour's clone does not exist yet when you want to append it.
- Forgetting the `None` case.

---

### Q20 ⭐⭐ 🟡 Walls and gates (multi-source BFS). `rooms` is an m x n grid (1 <= m, n <= 100) where -1 is a wall, 0 is a gate and 2147483647 stands for an empty room (infinity). Return a new grid in which every empty room holds the number of steps (up, down, left, right moves, not through walls) to its nearest gate, and stays 2147483647 if no gate can be reached. Explain why one BFS started from all gates at once beats one BFS per room, and give both complexities. Example: rooms=[[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], [2147483647, -1, 2147483647, -1], [0, -1, 2147483647, 2147483647]] -> [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]; rooms=[[2147483647]] -> [[2147483647]]; rooms=[[0, -1, 2147483647]] -> [[0, -1, 2147483647]].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Multi-source BFS. Put every source in the queue at distance 0 and run one BFS; each cell gets the distance to its nearest source.

**Say this first (1 line):** "Reverse the question: instead of searching from each room for a gate, start from all gates together; the first time BFS reaches a room is its nearest-gate distance."

**Brute force:** For every empty room run its own BFS until it hits a gate. One BFS is O(mn), there are up to mn rooms, so O((mn)^2) = 10^8 for 100 x 100. On a 30 x 30 grid with one gate in the corner the run below counts 596,584 queue pops against 900 for the right method.

**Optimal:**
- Copy the grid (the prompt wants a new grid). Queue = all cells equal to 0.
- Pop `(x, y)`. For each of 4 neighbours in bounds that still holds 2147483647: set it to `g[x][y] + 1` and enqueue.
- The sentinel value does two jobs: "unvisited" and "still unreachable". Walls (-1) and gates (0) are never overwritten.
- Why it works: this is the same as adding a virtual super-source joined to every gate by a zero-cost edge. BFS pops cells in order of distance from that super-source, so the first writer of a cell is its nearest gate.
- Rooms never reached keep 2147483647, exactly the required output.

**Complexity:**
- Multi-source BFS: each cell enqueued at most once, 4 neighbour checks each, so O(mn) time and O(mn) space (queue plus copied grid).
- One BFS per room: O(mn) rooms times O(mn) each, O((mn)^2) time.

**Dry run:** the 1 x 3 grid `[0, -1, INF]`.
- Queue [(0,0)]. Pop it: neighbour (0,1) is a wall (-1, not INF), skip. Queue empty.
- (0,2) was never written, stays INF. Result `[0, -1, INF]`, as expected.
- On the 4 x 4 example the gates at (0,2) and (3,0) both start in the queue; the cell (1,2) is reached from (0,2) at distance 1 and keeps that value even though (3,0) would give a longer one.

**Code:**

```python
import itertools, random
from collections import deque
random.seed(20)
INF = 2147483647
D4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def walls_and_gates(rooms):
    m, n = len(rooms), len(rooms[0])
    g = [row[:] for row in rooms]              # new grid, input untouched
    q = deque((i, j) for i in range(m) for j in range(n) if g[i][j] == 0)   # ALL gates start together
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and g[a][b] == INF:   # INF doubles as "unvisited"
                g[a][b] = g[x][y] + 1
                q.append((a, b))
    return g

def brute(rooms, work=None):                   # one BFS per empty room, stop at the nearest gate
    m, n = len(rooms), len(rooms[0])
    g = [row[:] for row in rooms]
    for i in range(m):
        for j in range(n):
            if rooms[i][j] != INF:
                continue
            dist = {(i, j): 0}
            q = deque([(i, j)])
            found = INF
            while q:
                x, y = q.popleft()
                if work is not None: work[0] += 1
                if rooms[x][y] == 0:
                    found = dist[(x, y)]
                    break
                for dx, dy in D4:
                    a, b = x + dx, y + dy
                    if 0 <= a < m and 0 <= b < n and rooms[a][b] != -1 and (a, b) not in dist:
                        dist[(a, b)] = dist[(x, y)] + 1
                        q.append((a, b))
            g[i][j] = found
    return g

ex1 = [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]
assert walls_and_gates(ex1) == [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
assert walls_and_gates([[INF]]) == [[INF]]
assert walls_and_gates([[0, -1, INF]]) == [[0, -1, INF]]
print("examples ok")

cnt = 0
for m, n in ((1, 1), (1, 4), (2, 3), (3, 3)):
    for cells in itertools.product((-1, 0, INF), repeat=m * n):
        g = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
        snap = [r[:] for r in g]
        assert walls_and_gates(g) == brute(g)
        assert g == snap                         # input not modified
        cnt += 1
print("exhaustive: all %d grids of sizes 1x1, 1x4, 2x3, 3x3 agree with one-BFS-per-room" % cnt)

for _ in range(300):
    m, n = random.randint(1, 7), random.randint(1, 7)
    g = [[random.choice([-1, 0, INF, INF]) for _ in range(n)] for _ in range(m)]
    assert walls_and_gates(g) == brute(g)
print("300 random grids up to 7x7 agree")

# work comparison on a 30 x 30 grid with one gate in a corner (BFS pops counted)
m = n = 30
g = [[INF] * n for _ in range(m)]; g[0][0] = 0
w = [0]; brute(g, w)
q = deque([(0, 0)]); popped = 0; seen = {(0, 0)}
while q:
    x, y = q.popleft(); popped += 1
    for dx, dy in D4:
        a, b = x + dx, y + dy
        if 0 <= a < m and 0 <= b < n and (a, b) not in seen: seen.add((a, b)); q.append((a, b))
print("30x30, one gate in a corner: multi-source pops = %d, per-room BFS pops = %d (cells = %d)" % (popped, w[0], m * n))
assert popped == m * n and w[0] > 100 * popped

# full size
m = n = 100
g = [[random.choice([-1, 0, INF, INF, INF, INF]) for _ in range(n)] for _ in range(m)]
r = walls_and_gates(g)
print("100x100 random grid: max finite distance", max(v for row in r for v in row if v != INF), "| unreachable rooms", sum(v == INF for row in r for v in row))
```

**Output (my run):**

```text
examples ok
exhaustive: all 20496 grids of sizes 1x1, 1x4, 2x3, 3x3 agree with one-BFS-per-room
300 random grids up to 7x7 agree
30x30, one gate in a corner: multi-source pops = 900, per-room BFS pops = 596584 (cells = 900)
100x100 random grid: max finite distance 7 | unreachable rooms 7
```

**Edge cases:**
- No gates: nothing is queued, the grid comes back unchanged.
- 1 x 1 grid: return as is.
- Rooms walled off from every gate stay at 2147483647 (not -1).
- Gate next to gate: both stay 0, no overwrite.
- Do not overwrite walls or gates; the check `== INF` takes care of it.

**Follow-ups:**
- Rotting oranges is the same pattern with levels counted per minute (a sibling question in this part).
- Different step costs per cell? Then it is Dijkstra from all sources (push all sources with distance 0).
- Return which gate is nearest? Store the gate id along with the distance in the queue.

**Common mistakes:**
- BFS from every room (times out).
- Starting from one gate at a time and keeping the minimum (that is also O(gates * mn)).
- Using `0` as the unvisited marker, so gates look unvisited.
- Mutating the input when a new grid is required.
- Checking `g[a][b] != -1` only, which lets BFS overwrite already-set smaller distances.

---

### Q21 ⭐⭐ 🟡 Is the graph bipartite? `graph` is an adjacency list of an undirected graph on nodes 0..n-1 (1 <= n <= 10^5): `graph[u]` lists the neighbours of u, the lists are symmetric, with no self loops and no repeated neighbours; the graph may be disconnected. Return True if the nodes can be split into two sets such that every edge joins the two sets. Use BFS two-colouring, restart from every unseen node, and state the link to odd cycles (the full theory of bipartite graphs and matching belongs to Part 14, this question is the colouring check only). Example: graph=[[1, 3], [0, 2], [1, 3], [0, 2]] -> True; graph=[[1, 2], [0, 2], [0, 1]] -> False; graph=[[], []] -> True; graph=[[1], [0], [3], [2]] -> True.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-colouring a graph with BFS (or DFS). A graph is bipartite exactly when it has no odd cycle, and the colouring check finds one if it exists.

**Say this first (1 line):** "Colour a start node 0, give every neighbour the other colour, and if an edge ever joins two nodes of the same colour it is not bipartite; restart from every unseen node because the graph may be disconnected."

**Brute force:** Try all 2^n assignments of side 0 or 1 and test every edge. O(2^n * E). Only usable for n <= 20; it is my checker.

**Optimal:**
- `color = [-1] * n`. For each `s` with `color[s] == -1`: colour it 0, BFS.
- For `u` popped and each neighbour `v`: if `v` is uncoloured, give it `1 - color[u]` and enqueue; else if `color[v] == color[u]`, return False.
- If every component finishes cleanly, return True.
- Link to odd cycles: in BFS every edge joins nodes whose depths differ by 0 or 1. A same-colour edge means equal depths, and the two paths back to their common ancestor plus that edge form an odd cycle. Conversely an odd cycle can never be coloured with 2 colours (colours must alternate around it). So "no conflict found" is equivalent to "no odd cycle".
- The run checks this equivalence on all 1099 graphs with up to 5 nodes, against both the 2^n brute force and a separate BFS-layer odd-cycle test.
- A node with no edges is its own component and always fine.

**Complexity:** O(V + E) time (each node queued once, each adjacency entry read once), O(V) space for colours and the queue. All iterative: V is 10^5, so a recursive DFS would exceed CPython's recursion limit of 1000.

**Dry run:** `[[1,2],[0,2],[0,1]]` (a triangle).
- Colour 0 -> 0. Neighbours 1 and 2 get colour 1; queue [1, 2].
- Pop 1: neighbour 0 has colour 0 != 1, fine; neighbour 2 has colour 1 == colour of 1: conflict, return False.
- A 4-cycle `[[1,3],[0,2],[1,3],[0,2]]` colours 0,1,0,1 with no conflict: True.

**Code:**

```python
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
```

**Output (my run):**

```text
examples ok: True False True True
exhaustive: all 1099 graphs on n <= 5 nodes agree with brute force and the odd-cycle test (672 not bipartite)
300 random n <= 10 graphs ok
n=1e5: path True, odd cycle (99999) False, even cycle (100000) True
```

**Edge cases:**
- Disconnected graph: the outer loop must restart. One odd cycle in a later component makes the answer False even when the first component is fine.
- Isolated nodes (empty lists): True.
- Single node: True.
- Even cycle: True; odd cycle of length 99,999: False (checked at full size in the run).
- No self loops by the prompt (a self loop would make it False immediately).

**Follow-ups:**
- Return the two sets? Collect nodes by colour.
- Possible bipartition (dislike pairs)? The same problem with edges as "dislikes".
- Find the odd cycle itself? Store parents; on a conflict walk both nodes up to their common ancestor.
- Matching and flow on bipartite graphs are in Part 14.

**Common mistakes:**
- Colouring only from node 0 (misses other components).
- Comparing with the parent only; any visited neighbour with the same colour is a conflict, not just the parent.
- Marking colour on dequeue instead of enqueue, which lets a node be given two colours.
- Recursive DFS on a 10^5 path: RecursionError.

---

### Q22 ⭐⭐ 🟡 Cycle detection in an undirected graph, including repeated edges. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` a list of [u, v] (up to 2*10^5). The edges may include self loops and repeated pairs, and each of those counts as a cycle (a self loop is a cycle of length 1, two copies of [u, v] a cycle of length 2). Return True if any cycle exists. Use an iterative DFS that tracks the edge it arrived by (the edge index, not the parent node), and explain when tracking only the parent node misses a repeated edge (it does with set- or dict-based adjacency that collapses repeated pairs into one entry, but not with list adjacency that stores every edge at both ends) and why the edge index is correct for any storage. Sizes are chosen so that a recursive DFS would exceed CPython's default recursion limit of 1000, so an iterative method (queue or explicit stack) is required. Example: n=4, edges=[[0, 1], [1, 2], [2, 3]] -> False; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> True; n=2, edges=[[0, 1], [1, 0]] -> True; n=2, edges=[[1, 1]] -> True.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Cycle detection in an undirected multigraph with an iterative DFS. A cycle exists when a traversal reaches an already-seen node by an edge other than the one it arrived by.

**Say this first (1 line):** "Iterative DFS where each stack entry carries the index of the edge I came by; I skip only that exact edge, and any other edge to a seen node is a cycle. Self loops and repeated pairs are cycles automatically."

**Brute force:** For each edge, remove it and check with a DFS whether its two ends are still connected; a self loop counts at once. O(E * (V + E)), about 6 * 10^10 at the limits. It is my checker.

**Optimal:**
- Adjacency lists of `(neighbour, edge_index)`, each edge stored at both ends (a self loop lands twice in the same list).
- For each unseen start: mark it, push `(start, -1)`.
- Pop `(u, arrived_by)`. For each `(v, i)` in `adj[u]`: if `i == arrived_by` skip (that is the edge we just walked). Else if `v` is seen, return True. Else mark `v`, push `(v, i)`.
- Why this is correct: in a forest, a DFS only ever meets a seen node through the tree edge it arrived by. Any other edge to a seen node closes a cycle, including a parallel edge (a different index, same endpoints) and a self loop (a different index leading to the node itself).
- Why the edge index and not the parent node: skipping "the parent node" skips every edge to the parent, so a second copy of that edge is skipped too. The run shows what happens in practice. With list adjacency, the parent's own loop still meets the second copy later and finds the node seen, so the cycle is reported anyway. The bug is real when repeated edges are collapsed: with a `set` or `dict` of neighbours (very common) the second copy is gone and `[[0, 1], [0, 1]]` is wrongly called acyclic. Tracking the edge index makes the answer right for any storage that keeps each edge.
- A union-find alternative also works: an edge whose ends already share a root closes a cycle, and a repeated edge or self loop does so trivially.

**Complexity:** O(V + E) time with the DFS (each node pushed once, each adjacency entry read once), O(V + E) space. The explicit stack replaces recursion: a path of 10^5 nodes is deeper than CPython's limit of 1000 and would raise RecursionError (the run shows it at 5000).

**Dry run:** `n=2, edges=[[0,1],[1,0]]`.
- adj[0] = [(1,0),(1,1)], adj[1] = [(0,0),(0,1)]. Start 0, stack [(0,-1)].
- Pop (0,-1): (1,0): 1 unseen, mark it, push (1,0). (1,1): 1 is seen and 1 != -1: return True.
- With a set-based "parent node" version adj[0] = {1}: only one entry, no cycle found: wrong.

**Code:**

```python
import itertools, random, sys
random.seed(22)

def has_cycle(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))                 # remember the edge index, not just the neighbour
        adj[v].append((u, i))                 # a self loop is stored twice at u, which is fine
    seen = [False] * n
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, -1)]                     # (node, index of the edge we arrived by)
        while stack:
            u, arrived_by = stack.pop()
            for v, i in adj[u]:
                if i == arrived_by:           # do not walk back along the same edge
                    continue
                if seen[v]:                   # reached by a different edge: a cycle
                    return True
                seen[v] = True
                stack.append((v, i))
    return False

def has_cycle_uf(n, edges):                   # second method: an edge joining two already-joined nodes closes a cycle
    p = list(range(n))
    def find(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges:
        a, b = find(u), find(v)
        if a == b:
            return True
        p[a] = b
    return False

def has_cycle_parent_only(n, edges, use_set):   # the tempting version: skip the parent NODE
    adj = [set() if use_set else [] for _ in range(n)]
    for u, v in edges:
        if use_set:
            adj[u].add(v); adj[v].add(u)         # a set (or dict) collapses a repeated edge into one entry
        else:
            adj[u].append(v); adj[v].append(u)
    seen = [False] * n
    for s in range(n):
        if seen[s]: continue
        seen[s] = True; stack = [(s, -1)]
        while stack:
            u, par = stack.pop()
            for v in adj[u]:
                if v == par: continue
                if seen[v]: return True
                seen[v] = True; stack.append((v, u))
    return False

def brute(n, edges):                          # remove each edge in turn: does its end still reach its start?
    for i, (u, v) in enumerate(edges):
        if u == v:
            return True
        adj = [[] for _ in range(n)]
        for j, (a, b) in enumerate(edges):
            if j != i:
                adj[a].append(b); adj[b].append(a)
        seen, st = {u}, [u]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); st.append(y)
        if v in seen:
            return True
    return False

assert has_cycle(4, [[0, 1], [1, 2], [2, 3]]) is False
assert has_cycle(3, [[0, 1], [1, 2], [2, 0]]) is True
assert has_cycle(2, [[0, 1], [1, 0]]) is True
assert has_cycle(2, [[1, 1]]) is True
print("examples ok: False True True True")

# exhaustive over ALL edge lists (order and endpoint direction included): n=3 up to 4 edges, n=4 up to 3 edges
cnt = true_n = 0
for n, maxe in ((1, 3), (2, 4), (3, 4), (4, 3)):
    ordered = [[u, v] for u in range(n) for v in range(n)]
    for k in range(maxe + 1):
        for es in itertools.product(ordered, repeat=k):
            es = [list(e) for e in es]
            r = has_cycle(n, es)
            assert r == brute(n, es) == has_cycle_uf(n, es), (n, es)
            cnt += 1; true_n += r
print("exhaustive: %d edge lists (n<=4, <=4 edges), DFS == brute == union-find; %d contain a cycle" % (cnt, true_n))

# the parent-node idea: how often is it wrong over every edge list with n <= 3 and <= 3 edges?
wrong = {False: 0, True: 0}; first = {False: None, True: None}
for n in (1, 2, 3):
    ordered = [[u, v] for u in range(n) for v in range(n)]
    for k in range(4):
        for es in itertools.product(ordered, repeat=k):
            es = [list(e) for e in es]
            truth = brute(n, es)
            for use_set in (False, True):
                if has_cycle_parent_only(n, es, use_set) != truth:
                    wrong[use_set] += 1
                    if first[use_set] is None or len(es) < len(first[use_set]): first[use_set] = es
print("parent-node skip with LIST adjacency: wrong on", wrong[False], "lists (the parent's own loop still meets the second copy of a repeated edge)")
print("parent-node skip with SET adjacency: wrong on", wrong[True], "lists; smallest failing edges:", first[True])
assert wrong[False] == 0 and wrong[True] > 0

for _ in range(500):
    n = random.randint(1, 8)
    es = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 9))]
    assert has_cycle(n, es) == brute(n, es)
print("500 random multigraphs with self loops ok")

# deep paths: iterative copes with 2e5 nodes; a recursive DFS dies at the default limit
n = 200000
path = [[i, i + 1] for i in range(n - 1)]
assert has_cycle(n, path) is False and has_cycle(n, path + [[n - 1, 0]]) is True
assert has_cycle(n, path + [[7, 7]]) is True and has_cycle(n, path + [[7, 8]]) is True
def rec_cycle(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges): adj[u].append((v, i)); adj[v].append((u, i))
    seen = [False] * n
    def dfs(u, pe):
        seen[u] = True
        for v, i in adj[u]:
            if i == pe: continue
            if seen[v] or dfs(v, i): return True
        return False
    return any(not seen[s] and dfs(s, -1) for s in range(n))
try:
    rec_cycle(5000, path[:4999])
except RecursionError:
    print("recursive DFS on a 5000-node path: RecursionError (limit %d); iterative handled n=200000" % sys.getrecursionlimit())
```

**Output (my run):**

```text
examples ok: False True True True
exhaustive: 12095 edge lists (n<=4, <=4 edges), DFS == brute == union-find; 11159 contain a cycle
parent-node skip with LIST adjacency: wrong on 0 lists (the parent's own loop still meets the second copy of a repeated edge)
parent-node skip with SET adjacency: wrong on 192 lists; smallest failing edges: [[0, 1], [0, 1]]
500 random multigraphs with self loops ok
recursive DFS on a 5000-node path: RecursionError (limit 1000); iterative handled n=200000
```

**Edge cases:**
- Self loop `[u, u]`: True (found at the first look at `u`'s list).
- Two copies of `[u, v]` (either order, `[1, 0]` is the same pair as `[0, 1]`): True.
- Disconnected graph: the outer loop restarts from every unseen node; a cycle in a later component counts.
- No edges, single node: False.
- A path of 200,000 nodes: False; plus an extra edge anywhere: True (checked above).

**Follow-ups:**
- Directed graph? Different problem: you need three states (unseen, on the stack, done), or Kahn's algorithm (see Part 9 cycle-in-directed-graph question).
- Which edge closes the cycle? Union-find returns it directly (see the redundant connection question in this part).
- Count the independent cycles? E - V + C (edges, nodes, components), the cyclomatic number.

**Common mistakes:**
- Skipping the parent node instead of the arrival edge, then storing neighbours in a set or dict.
- Recursion on large inputs.
- Treating a self loop as harmless.
- Running only from node 0.
- Using the "directed" three-colour logic on an undirected graph, which reports the tree edge back to the parent as a cycle.

---

### Q23 ⭐⭐ 🟡 Accounts merge (union-find on emails). `accounts` is a list of accounts, each `[name, email1, email2, ...]` (1 <= len(accounts) <= 1000, each with at least one email, emails lowercase). Two accounts belong to the same person if they share at least one email (directly or through a chain of accounts); different people may have the same name, and one email always maps to a single name. Return the merged accounts as `[name, sorted unique emails...]`, with the returned list sorted ascending as ordinary Python lists, so the answer is unique. Say what the union-find nodes are and the complexity. Example: accounts=[['john', 'a@x', 'b@x'], ['john', 'c@x'], ['john', 'b@x', 'd@x'], ['mary', 'e@x']] -> [['john', 'a@x', 'b@x', 'd@x'], ['john', 'c@x'], ['mary', 'e@x']]; accounts=[['sam', 's@x'], ['sam', 't@x']] -> [['sam', 's@x'], ['sam', 't@x']]; accounts=[['kim', 'k@x', 'k@x']] -> [['kim', 'k@x']].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Union-find (disjoint sets) for grouping by shared keys. The shared email is the link, so the emails are the nodes.

**Say this first (1 line):** "Names are not identities, emails are. I union all emails inside one account, then group emails by root, attach the name, sort."

**Brute force:** Keep a list of (name, email set). Find any two sets that intersect, merge them, restart. Repeat until no pair intersects. Each pass is O(A^2) set intersections and there can be O(A) passes, so O(A^2 * rounds) with big constants. It is the checker in the code.

**Optimal:**
- Nodes: every distinct email string. Not accounts (two accounts can be linked only through a third) and not names (two different people can be called "sam").
- For each account, `union(email_j, first_email)` for the other emails. Also record `name[email] = account name` (one email maps to one name, so overwriting is safe).
- After all unions, bucket every email by `find(email)`. Each bucket is one person. Output `[name, *sorted(bucket)]`, then sort the outer list.
- Chains work for free: A shares with B, B shares with C, so A and C end in one set although they share nothing directly.
- `find` is iterative with path halving, so no recursion limit problem on a chain of 1000 accounts.

**Complexity:** Let N be the total number of emails over all accounts (at most about 1000 times the longest account). Unions and finds: O(N * alpha(N)) with union by rank, and about O(N log N) worst case with path halving alone (what the code does; either is tiny). Sorting: O(N log N) for the emails inside buckets plus the sort of the result lists. Space O(N) for the parent map and groups.

**Dry run:** `[['john','a@x','b@x'], ['john','c@x'], ['john','b@x','d@x'], ['mary','e@x']]`.
- Account 1: parent has a, b. Union b into a's set: {a, b}.
- Account 2: c alone: {c}.
- Account 3: b already exists; d is new; union d with b's root: {a, b, d}.
- Account 4: {e}.
- Buckets: {a, b, d} named john, {c} named john, {e} named mary. Sorted: `[['john','a@x','b@x','d@x'], ['john','c@x'], ['mary','e@x']]`.

**Code:**
```python
import random
from collections import defaultdict

random.seed(23)

def accounts_merge(accounts):
    """Union-find over EMAILS (not accounts, not names). Iterative find with path halving."""
    parent, name = {}, {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for acc in accounts:
        for e in acc[1:]:
            parent.setdefault(e, e)
            name[e] = acc[0]
        for e in acc[2:]:                       # chain every email of the account to its first one
            ra, rb = find(e), find(acc[1])
            if ra != rb:
                parent[ra] = rb
    groups = defaultdict(list)
    for e in parent:
        groups[find(e)].append(e)
    return sorted([name[r], *sorted(es)] for r, es in groups.items())

def accounts_merge_brute(accounts):
    """Keep merging any two sets that share an email until nothing changes. O(A^2 * rounds)."""
    sets = [(a[0], set(a[1:])) for a in accounts]
    changed = True
    while changed:
        changed = False
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                if sets[i][1] & sets[j][1]:
                    sets[i] = (sets[i][0], sets[i][1] | sets[j][1])
                    del sets[j]
                    changed = True
                    break
            if changed:
                break
    return sorted([nm, *sorted(es)] for nm, es in sets)

def merge_by_name_wrong(accounts):
    """Common bug: treat the name as the identity."""
    by = defaultdict(set)
    for a in accounts:
        by[a[0]] |= set(a[1:])
    return sorted([n, *sorted(s)] for n, s in by.items())

# ---- examples from the prompt
ex = [
    ([['john', 'a@x', 'b@x'], ['john', 'c@x'], ['john', 'b@x', 'd@x'], ['mary', 'e@x']],
     [['john', 'a@x', 'b@x', 'd@x'], ['john', 'c@x'], ['mary', 'e@x']]),
    ([['sam', 's@x'], ['sam', 't@x']], [['sam', 's@x'], ['sam', 't@x']]),
    ([['kim', 'k@x', 'k@x']], [['kim', 'k@x']]),
]
for acc, want in ex:
    got = accounts_merge(acc)
    assert got == want == accounts_merge_brute(acc), (acc, got, want)
    print(acc, '->', got)

# ---- the name-as-identity bug
acc = ex[1][0]
print('merge by name (wrong) on the two sams ->', merge_by_name_wrong(acc))

# ---- chain: A-B share, B-C share, so A and C merge through B even though they share nothing directly
chain = [['z', 'e1', 'e2'], ['z', 'e3', 'e4'], ['z', 'e2', 'e3']]
print('chain ->', accounts_merge(chain))
assert accounts_merge(chain) == [['z', 'e1', 'e2', 'e3', 'e4']]

# ---- random cross-check, small email pool so merges and chains are frequent
def rand_accounts():
    k = random.randint(1, 8)
    emails = [f'{random.choice("abcdefgh")}{i}@x' for i in range(random.randint(1, 10))]
    emails = sorted(set(emails))
    owner = {e: random.choice(['ann', 'bob', 'cy']) for e in emails}      # one email -> one name
    accts = []
    for _ in range(k):
        sub = [random.choice(emails) for _ in range(random.randint(1, 4))]  # duplicates inside an account allowed
        # keep names consistent: the account name is the owner of its first email; all its emails must share that owner
        nm = owner[sub[0]]
        sub = [x for x in sub if owner[x] == nm]
        accts.append([nm, *sub])
    return accts
for _ in range(1000):
    acc = rand_accounts()
    assert accounts_merge(acc) == accounts_merge_brute(acc), acc
print('1000 seeded random inputs: union-find on emails == repeated set merging')

# ---- size: 1000 accounts forming one long chain (worst case for a naive recursive find)
n = 1000
big = [['w', f'm{i}@x', f'm{i+1}@x'] for i in range(n)]
res = accounts_merge(big)
assert len(res) == 1 and len(res[0]) == n + 2
print('1000-account chain merges into one account with', len(res[0]) - 1, 'emails')

# ---- edge cases
assert accounts_merge([['a', 'x@x']]) == [['a', 'x@x']]
assert accounts_merge([['a', 'x@x'], ['a', 'x@x']]) == [['a', 'x@x']]
assert accounts_merge([['b', 'p@x'], ['a', 'q@x']]) == [['a', 'q@x'], ['b', 'p@x']]
print('edge asserts passed')
```

**Output (my run):**
```
[['john', 'a@x', 'b@x'], ['john', 'c@x'], ['john', 'b@x', 'd@x'], ['mary', 'e@x']] -> [['john', 'a@x', 'b@x', 'd@x'], ['john', 'c@x'], ['mary', 'e@x']]
[['sam', 's@x'], ['sam', 't@x']] -> [['sam', 's@x'], ['sam', 't@x']]
[['kim', 'k@x', 'k@x']] -> [['kim', 'k@x']]
merge by name (wrong) on the two sams -> [['sam', 's@x', 't@x']]
chain -> [['z', 'e1', 'e2', 'e3', 'e4']]
1000 seeded random inputs: union-find on emails == repeated set merging
1000-account chain merges into one account with 1001 emails
edge asserts passed
```

**Edge cases:**
- Duplicate email inside one account (`['kim','k@x','k@x']`): union of a node with itself is a no-op, and the output has one copy.
- Same name, no shared email: stay separate (the second example).
- Same email in two accounts with the same name only: merges; one email maps to one name, so there is no name conflict to resolve.
- One account, one email: trivial group.
- Output ordering: sorting `[name, emails...]` lists compares the name first, then the first email, so ties between two people with the same name are broken by their smallest email. That is why the answer is unique.

**Follow-ups:**
- Why not nodes = accounts? You would need a map from email to the first account that owned it, then union accounts. It works too, but the email version has fewer moving parts.
- Why not DFS on an email graph? Also O(N), but you must build adjacency lists first, and with 1000 accounts you can still hit deep recursion; union-find does not.
- Online version (accounts arrive one at a time)? Union-find handles it directly; the group lists are rebuilt only when queried.

**Common mistakes:**
- Merging by name (the code prints the wrong answer for two sams).
- Forgetting to sort the emails or the final list.
- Recursive `find` without a depth guard on a long chain.
- Using the root's account name when roots are emails: fine, but only because one email has one name; do not take the name from an arbitrary account of the group if the statement allowed conflicts.

### Q24 ⭐⭐ 🟡 Parallel courses: minimum number of semesters. Courses are labelled 1..n (1 <= n <= 5000) and `relations` is a list of [prev, next] meaning prev must be finished in an earlier semester than next (0 <= len <= 5000). In each semester you may take any number of courses whose prerequisites were all completed in earlier semesters. Return the minimum number of semesters to finish all courses, or -1 if a cycle makes it impossible. Use Kahn's algorithm one level at a time and say what the answer is in terms of a longest path. Example: n=3, relations=[[1, 3], [2, 3]] -> 2; n=3, relations=[[1, 2], [2, 3], [3, 1]] -> -1; n=4, relations=[[1, 2], [2, 3], [3, 4]] -> 4; n=2, relations=[] -> 1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort by Kahn's algorithm, processed level by level. The number of levels is the length of the longest prerequisite chain.

**Say this first (1 line):** "Each semester I take everything with no unfinished prerequisite. That is one BFS level of Kahn's algorithm, so the answer is the number of levels, or -1 if some course never reaches in-degree zero."

**Brute force:** Longest-chain by relaxation: `d[c] = 1` for all courses, then repeat n times `d[next] = max(d[next], d[prev] + 1)` over every relation. If an edge can still improve after n rounds there is a cycle, so -1. Otherwise the answer is `max(d)`. O(n * E), about 25 million steps at the limits. It is the checker in the code.

**Optimal:**
- Build adjacency lists and in-degrees for courses 1..n.
- `cur` = all courses with in-degree 0. Each loop iteration is one semester: count it, add `len(cur)` to `done`, and for every course in `cur` decrement its neighbours' in-degrees; a neighbour that hits 0 goes into `nxt`.
- Stop when `cur` is empty. If `done == n` return the semester count, else a cycle blocked some courses: return -1.
- Why the number of levels is the longest path: a course can be taken no earlier than one semester after its latest prerequisite, and Kahn takes it exactly then. So the semester of a course is 1 + max(semester of prerequisites), which is the length (counted in courses) of the longest chain ending there. The answer is the maximum, the longest path in the DAG.
- Taking courses as early as possible never hurts, because finishing a course earlier only unlocks more.
- Duplicate relations are fine: the in-degree counts the edge twice and it is decremented twice.

**Complexity:** Time O(n + E): each course enters `cur` once, each relation is touched once. Space O(n + E) for the adjacency lists, in-degrees and level lists.

**Dry run:** `n=3, relations=[[1,3],[2,3]]`.
- In-degrees: 1 -> 0, 2 -> 0, 3 -> 2.
- Semester 1: `cur=[1,2]`, done = 2. Course 1 drops 3 to 1; course 2 drops 3 to 0, so `nxt=[3]`.
- Semester 2: `cur=[3]`, done = 3. No neighbours.
- `cur` empty, done == 3 == n, answer 2.
- Cycle case `[[1,2],[2,3],[3,1]]`: every in-degree is 1, `cur` is empty at the start, semesters 0, done 0 < 3, so -1.

**Code:**
```python
import itertools
import random

random.seed(24)

def min_semesters(n, relations):
    """Kahn's algorithm one level (= one semester) at a time."""
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        adj[a].append(b)
        indeg[b] += 1
    cur = [i for i in range(1, n + 1) if indeg[i] == 0]
    semesters = done = 0
    while cur:
        semesters += 1
        done += len(cur)
        nxt = []
        for u in cur:
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        cur = nxt
    return semesters if done == n else -1

def min_semesters_brute(n, relations):
    """Longest chain (in courses) by n rounds of relaxation; a cycle never settles, so any still-improving edge means -1."""
    d = [1] * (n + 1)
    for _ in range(n):
        for a, b in relations:
            if d[a] + 1 > d[b]:
                d[b] = d[a] + 1
    if any(d[a] + 1 > d[b] for a, b in relations):
        return -1
    return max(d[1:])

for n, rel, want in [(3, [[1, 3], [2, 3]], 2), (3, [[1, 2], [2, 3], [3, 1]], -1),
                     (4, [[1, 2], [2, 3], [3, 4]], 4), (2, [], 1)]:
    got = min_semesters(n, rel)
    assert got == want == min_semesters_brute(n, rel), (n, rel, got, want)
    print(n, rel, '->', got)

# ---- exhaustive: EVERY relation set on n <= 3 including self loops (2^9 sets for n=3), and every set without self loops on n = 4 (2^12)
cnt = 0
for n, loops in [(1, True), (2, True), (3, True), (4, False)]:
    pairs = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if loops or a != b]
    for mask in range(1 << len(pairs)):
        rel = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        assert min_semesters(n, rel) == min_semesters_brute(n, rel), (n, rel)
        cnt += 1
print('exhaustive check on', cnt, 'relation sets (all graphs on n<=3 with self loops, n=4 without): longest chain == Kahn levels')

# ---- seeded random larger cases, with duplicate relations allowed
for _ in range(500):
    n = random.randint(1, 9)
    rel = [[random.randint(1, n), random.randint(1, n)] for _ in range(random.randint(0, 12))]
    assert min_semesters(n, rel) == min_semesters_brute(n, rel), (n, rel)
print('500 seeded random cases agree')

# ---- the answer is a longest path: a DAG that is a single chain has n semesters, a star has 2
n = 5000
chain = [[i, i + 1] for i in range(1, n)]
assert min_semesters(n, chain) == n
assert min_semesters(n, [[1, i] for i in range(2, n + 1)]) == 2
assert min_semesters(n, []) == 1
assert min_semesters(n, chain + [[n, 1]]) == -1                    # one back edge makes a cycle
assert min_semesters(1, [[1, 1]]) == -1                            # self loop
print('n=5000 chain ->', min_semesters(n, chain), 'semesters; star ->', 2, '; no relations ->', 1)

# ---- a partial cycle: courses before the cycle finish, but done < n exposes the cycle
assert min_semesters(4, [[1, 2], [2, 3], [3, 2]]) == -1
print('cycle hidden behind a valid prefix is still caught by done < n')
```

**Output (my run):**
```
3 [[1, 3], [2, 3]] -> 2
3 [[1, 2], [2, 3], [3, 1]] -> -1
4 [[1, 2], [2, 3], [3, 4]] -> 4
2 [] -> 1
exhaustive check on 4626 relation sets (all graphs on n<=3 with self loops, n=4 without): longest chain == Kahn levels
500 seeded random cases agree
n=5000 chain -> 5000 semesters; star -> 2 ; no relations -> 1
cycle hidden behind a valid prefix is still caught by done < n
```

**Edge cases:**
- No relations: all courses in one semester (answer 1, not 0; n >= 1 so there is always at least one course).
- Self loop `[a, a]`: a course that needs itself; in-degree never reaches 0, so -1. The code asserts it.
- A cycle behind a valid prefix (`1 -> 2`, `2 <-> 3`): course 1 is taken, then nothing, so `done < n` and -1. Checking only "did we process something" is not enough.
- Single chain of 5000 courses: 5000 semesters. The loop is iterative, so there is no recursion issue.

**Follow-ups:**
- At most k courses per semester (Parallel courses II)? The level trick breaks: you must choose which k of the ready courses, and that choice is NP-hard in general; the usual interview version uses bitmask DP for n <= 15.
- Return the schedule, not the count? Keep each `cur` list: it is the semester's courses.
- Why not DFS longest path? Works with memoisation on a DAG plus a three-colour cycle check; Kahn does both in one pass.

**Common mistakes:**
- Counting semesters as the number of edges on the longest path (off by one: a single course is 1 semester).
- Returning the semester count without checking `done == n`.
- Using 0-based arrays for courses labelled 1..n and silently dropping course n.
- Processing one course at a time with a single queue and losing the level boundaries.

### Q25 ⭐⭐ 🟡 Dijkstra with lazy deletion: count pushes and stale pops. `n` nodes 0..n-1 (1 <= n <= 10^5), `edges` a list of directed [u, v, w] with 0 <= w <= 100 (up to 2*10^5, repeats allowed) and `src`. Run this exact algorithm: dist[src] = 0; the heap holds (distance, node) tuples and starts with (0, src); pop the smallest entry (d, u); if d > dist[u] the entry is stale, so count it and skip it; otherwise, for each edge (u, v, w) in input order, if d + w < dist[v] (strictly) set dist[v] = d + w and push (d + w, v). Return `[dist, pushes, stale_pops]` where dist has None for unreachable nodes, `pushes` counts every heappush including the first one, and `stale_pops` counts skipped entries. Python's heapq has no decrease-key, so duplicates are pushed instead (see Part 8 Q38); explain why the (distance, node) tuples never hit the unorderable-tie TypeError seen with payload objects (Part 8 Q29), why pushes is at most E + 1, and that stale_pops always equals pushes minus the number of reached nodes. Example: n=4, edges=[[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]], src=0 -> [[0, 3, 1, 4], 5, 1]; n=3, edges=[[0, 1, 1]], src=2 -> [[null, null, 0], 1, 0]; n=3, edges=[[0, 1, 5], [0, 2, 5], [1, 2, 0], [2, 1, 0]], src=0 -> [[0, 5, 5], 3, 0].
**Asked at:** Dijkstra and lazy-deletion write-ups (a PracHub guide on Dijkstra stale heap entries and negative edges, Codeforces lazy-deletion tutorials, a python-dev heapq thread; search snippets only, not opened; docs.python.org was unreachable) | Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened)

**Pattern:** Single-source shortest paths with non-negative weights: Dijkstra on a `heapq` min-heap, using lazy deletion because `heapq` has no decrease-key.

**Say this first (1 line):** "Pop the closest entry; if its distance is worse than what I already know, it is stale, skip it. Otherwise relax its edges and push every improvement as a new entry. Duplicates are cheap, a decrease-key is not available."

**Brute force:** Bellman-Ford style: n rounds of relaxing every edge, O(n * E). Too slow at 10^5 by 2*10^5, and it does not give the push and stale counts. It is the checker for the distances.

**Optimal:**
- `dist[src] = 0`, heap `[(0, src)]`, `pushes = 1`, `stale = 0`.
- Pop `(d, u)`. If `d > dist[u]`: count it as stale, `continue`. Else for each edge `(u, v, w)` in input order: if `d + w < dist[v]` (strict), set it and push `(d + w, v)`.
- Why it is right: with weights >= 0 the first time a node is popped with `d == dist[u]` that distance is final (any other route goes through an entry that is at least as large). Stale entries are exactly the entries for a node that were beaten after being pushed.
- Why `(distance, node)` never raises `TypeError`: both items are ints, so tuples always compare. If two entries tie on distance the node number decides, and if both are equal the tuples are equal, which `heapq` does not mind. The `TypeError` in Part 8 Q29 came from tied priorities followed by an unorderable payload object (the code shows it). Part 8 Q38 is the same trick, push a new entry and ignore the old one.
- Why `pushes <= E + 1`: every push after the first happens while relaxing an edge. A node's edges are relaxed only when its non-stale entry is popped, and each node has exactly one non-stale pop, so each edge is relaxed at most once. So at most E pushes from edges plus the initial one.
- Why `stale == pushes - reached`: every entry pushed is popped eventually. A reached node has exactly one entry whose distance equals its final `dist` (equal distances are never pushed twice because the comparison is strict, and weights are >= 0 so the final value is never lowered after its pop). That entry is the one non-stale pop; every other entry is stale. The source's first entry counts as its non-stale one.

**Complexity:** Time O((V + E) log E) which is O((V + E) log V) because E <= V^2 only changes the log by a factor of 2: at most E + 1 pushes, each push and pop O(log heap size). Space O(V + E) (adjacency lists, plus a heap of at most E + 1 entries).

**Dry run:** `n=4, edges=[[0,1,4],[0,2,1],[2,1,2],[1,3,1]], src=0`.
- Pop (0,0). Relax 0->1: dist[1]=4, push (4,1). Relax 0->2: dist[2]=1, push (1,2). Pushes 3.
- Pop (1,2). Relax 2->1: 1+2=3 < 4, dist[1]=3, push (3,1). Pushes 4.
- Pop (3,1). Relax 1->3: dist[3]=4, push (4,3). Pushes 5.
- Pop (4,1): 4 > dist[1]=3, stale (count 1). Pop (4,3): fine.
- Result `[[0,3,1,4], 5, 1]`; reached = 4, and 5 - 4 = 1 = stale.

**Code:**
```python
import heapq
import itertools
import random

random.seed(25)
INF = float('inf')

def dijkstra_lazy(n, edges, src):
    """Lazy deletion: push duplicates, skip a popped entry whose distance is worse than the best known."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    heap = [(0, src)]
    pushes, stale = 1, 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                       # a better entry for u was already processed
            stale += 1
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:               # strict: equal distance does not push
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
                pushes += 1
    return [[None if x == INF else x for x in dist], pushes, stale]

def bellman_ford_dist(n, edges, src):
    """Independent checker for the distances only (weights are >= 0 so no negative cycles)."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return [None if x == INF else x for x in d]

examples = [
    (4, [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]], 0, [[0, 3, 1, 4], 5, 1]),
    (3, [[0, 1, 1]], 2, [[None, None, 0], 1, 0]),
    (3, [[0, 1, 5], [0, 2, 5], [1, 2, 0], [2, 1, 0]], 0, [[0, 5, 5], 3, 0]),
]
for n, e, s, want in examples:
    got = dijkstra_lazy(n, e, s)
    assert got == want, (got, want)
    print(n, e, 'src', s, '->', got)

# ---- why (distance, node) tuples never raise TypeError: ints always compare, and equal pairs are fully equal
heap = []
for item in [(3, 1), (3, 1), (3, 0), (2, 5)]:
    heapq.heappush(heap, item)
print('tied distances pop in node order:', [heapq.heappop(heap) for _ in range(4)])
class Payload:                               # what goes wrong if you push objects (Part 8 Q29)
    pass
h = [(1, Payload())]
try:
    heapq.heappush(h, (1, Payload()))
except TypeError as err:
    print('(dist, object) with tied dist ->', err)

# ---- exhaustive: every multigraph on 3 nodes with up to 3 edges, weights 0..2, every source
opts = [(u, v, w) for u in range(3) for v in range(3) for w in range(3)]     # 27 possible edges (self loops included)
cnt = 0
for k in range(4):
    for combo in itertools.product(opts, repeat=k):                           # ordered, so repeats and input orders are covered
        edges = [list(x) for x in combo]
        for src in range(3):
            dist, pushes, stale = dijkstra_lazy(3, edges, src)
            reached = sum(x is not None for x in dist)
            assert dist == bellman_ford_dist(3, edges, src)
            assert pushes <= len(edges) + 1
            assert stale == pushes - reached
            cnt += 1
print('exhaustive on', cnt, '(graph, source) cases: distances right, pushes <= E + 1, stale == pushes - reached')

# ---- seeded random bigger graphs
for _ in range(500):
    n = random.randint(1, 12)
    edges = [[random.randrange(n), random.randrange(n), random.randint(0, 6)] for _ in range(random.randint(0, 40))]
    src = random.randrange(n)
    dist, pushes, stale = dijkstra_lazy(n, edges, src)
    reached = sum(x is not None for x in dist)
    assert dist == bellman_ford_dist(n, edges, src) and pushes <= len(edges) + 1 and stale == pushes - reached
print('500 seeded random graphs agree')

# ---- the stale check saves work: count edge scans with and without it on a graph with many improvable nodes
def scans(n, edges, src, skip_stale):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    heap, work = [(0, src)], 0
    while heap:
        d, u = heapq.heappop(heap)
        if skip_stale and d > dist[u]:
            continue
        for v, w in adj[u]:
            work += 1
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return work
# layer graph: node i reaches every later node; the first path found is the worst, later ones improve it
m = 60
edges = [[i, j, (j - i) ** 2] for i in range(m) for j in range(i + 1, m)]
edges.sort(key=lambda e: -e[2])
print('edge scans, 60-node graph: with stale check', scans(m, edges, 0, True), '| without', scans(m, edges, 0, False))

# ---- edge case and size: n=1; n = 10^5, E = 2*10^5 with repeated edges
assert dijkstra_lazy(1, [], 0) == [[0], 1, 0]
n, E = 10 ** 5, 2 * 10 ** 5
edges = [[random.randrange(n), random.randrange(n), random.randint(0, 100)] for _ in range(E)]
dist, pushes, stale = dijkstra_lazy(n, edges, 0)
reached = sum(x is not None for x in dist)
assert pushes <= E + 1 and stale == pushes - reached
print('n=10^5, E=2*10^5: reached', reached, 'pushes', pushes, '<= E + 1 =', E + 1, '| stale', stale, '== pushes - reached =', pushes - reached)
```

**Output (my run):**
```
4 [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]] src 0 -> [[0, 3, 1, 4], 5, 1]
3 [[0, 1, 1]] src 2 -> [[None, None, 0], 1, 0]
3 [[0, 1, 5], [0, 2, 5], [1, 2, 0], [2, 1, 0]] src 0 -> [[0, 5, 5], 3, 0]
tied distances pop in node order: [(2, 5), (3, 0), (3, 1), (3, 1)]
(dist, object) with tied dist -> '<' not supported between instances of 'Payload' and 'Payload'
exhaustive on 61320 (graph, source) cases: distances right, pushes <= E + 1, stale == pushes - reached
500 seeded random graphs agree
edge scans, 60-node graph: with stale check 1770 | without 34279
n=10^5, E=2*10^5: reached 79852 pushes 85195 <= E + 1 = 200001 | stale 5343 == pushes - reached = 5343
```

**Edge cases:**
- Unreachable nodes stay `None`; their entries never exist, so they add nothing to the counts (second example: `[[None, None, 0], 1, 0]`).
- Zero-weight edges and zero-weight cycles (third example): the strict `<` stops infinite pushing, the count stays 3.
- Parallel edges and self loops: a self loop never improves anything with weight >= 0.
- `n = 1`: `[[0], 1, 0]`.
- Negative weights break the "first pop is final" claim and the counting argument (Q28 and Q42 in this part).

**Follow-ups:**
- Why not skip the stale check? The result stays correct for non-negative weights, but each stale entry re-scans its edges. The code counts 34279 edge scans against 1770 on a 60-node graph.
- Can you avoid duplicates? An indexed heap with decrease-key (or a Fibonacci heap) does, at the cost of much more code; in Python the lazy version is nearly always faster.
- Early exit when only one target matters? Return when the target is popped non-stale.

**Common mistakes:**
- Pushing the node first, `(node, d)`, so the heap orders by node.
- Using `<=` in the relaxation: equal distances get pushed again and the push bound breaks (zero-weight cycles can loop forever).
- Marking nodes done on push instead of on pop.
- Counting `reached` as the number of finite distances but forgetting the source.

### Q26 ⭐⭐ 🟡 Path with minimum effort. `heights` is an m x n grid of integers (1 <= m, n <= 100, 0 <= value <= 10^6). Moving up, down, left or right between adjacent cells costs |difference of heights|, and the effort of a route is the largest single step cost on it. Return the minimum possible effort over all routes from the top-left to the bottom-right cell. Solve it with Dijkstra where the path 'length' is the maximum edge instead of the sum, and say why that still works; mention the binary-search-on-answer alternative. Example: heights=[[1, 2, 2], [3, 8, 2], [5, 3, 5]] -> 2; heights=[[1, 2, 3], [3, 8, 4], [5, 3, 5]] -> 1; heights=[[7]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Dijkstra and lazy-deletion write-ups (a PracHub guide on Dijkstra stale heap entries and negative edges, Codeforces lazy-deletion tutorials, a python-dev heapq thread; search snippets only, not opened; docs.python.org was unreachable)

**Pattern:** Minimax path (bottleneck shortest path) on a grid: Dijkstra with `max` in place of `+`. Binary search on the answer plus a DFS/BFS reachability test is the alternative.

**Say this first (1 line):** "It is Dijkstra, but a route's cost is its largest step so far. Extending a route can never make that smaller, and a cheaper prefix never gives a worse result, so the greedy pop order is still correct."

**Brute force:** Enumerate every simple path from corner to corner and take the one with the smallest maximum step. Exponential in the number of cells; fine only on 3 x 3 grids. It is one checker in the code.

**Optimal:**
- Heap entries `(effort, row, col)`, `best[r][c] = INF` except `best[0][0] = 0`.
- Pop the smallest. If `effort > best[r][c]` it is stale, skip. If it is the bottom-right cell, return it.
- For each of the 4 neighbours: `ne = max(effort, abs(h[nb] - h[cell]))`; if `ne < best[nb]`, update and push.
- Why `max` still works. Dijkstra needs two properties of the path cost:
  - Extending a path never lowers its cost: `max(e, w) >= e`.
  - The extension is monotone in the prefix: if `e1 <= e2` then `max(e1, w) <= max(e2, w)`.
  - With these, when a cell is popped with effort `e`, any other route reaches it through a cell not yet popped, whose effort is already `>= e`, so that route costs at least `e`. So the first pop of a cell is final. Sum satisfies both properties for non-negative steps, and so does max.
- Binary search alternative: for a threshold T, flood fill only through steps `<= T`; feasibility is monotone in T, so binary search T in `[0, max - min]`. Cost O(mn * log(10^6)), about 20 floods. The code runs both and they agree.
- The two answers are not the same as the sum version: on example 1 the sum-of-steps answer is 4 but the minimum effort is 2 (code prints it).

**Complexity:** Dijkstra: each cell pushes at most one entry per improvement, at most 4mn pushes, each O(log(mn)), so O(mn log(mn)) time, O(mn) space. Binary search: O(mn log(range)) time, O(mn) space; at 100 x 100 and range 10^6 that is about 20 * 10^4 cell visits. Both are fine at this size; the binary search has no heap.

**Dry run:** `[[1,2,2],[3,8,2],[5,3,5]]`.
- Start (0,0) effort 0. Push right (0,1): max(0,1) = 1; push down (1,0): max(0,2) = 2.
- Pop (0,1) effort 1: right (0,2) step 0, effort 1; down (1,1) step 6, effort 6.
- Pop (0,2) effort 1: down (1,2) step 0, effort 1. Pop (1,2) effort 1: down (2,2) step 3, effort 3.
- Pop (1,0) effort 2: down (2,0) step 2, effort 2. Pop (2,0) effort 2: right (2,1) step 2, effort 2. Pop (2,1) effort 2: right (2,2) step 2, effort max(2,2) = 2 < 3, update.
- Pop (2,2) with effort 2. Answer 2.

**Code:**
```python
import heapq
import itertools
import random

random.seed(26)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
INF = float('inf')

def min_effort(h):
    """Dijkstra where a path's cost is the MAX step so far instead of the sum."""
    m, n = len(h), len(h[0])
    best = [[INF] * n for _ in range(m)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        e, x, y = heapq.heappop(heap)
        if e > best[x][y]:                         # stale entry (lazy deletion)
            continue
        if (x, y) == (m - 1, n - 1):
            return e
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n:
                ne = max(e, abs(h[a][b] - h[x][y]))    # the only change from ordinary Dijkstra
                if ne < best[a][b]:
                    best[a][b] = ne
                    heapq.heappush(heap, (ne, a, b))

def min_effort_bsearch(h):
    """Binary search on the answer T; feasibility = reachable using only steps <= T (iterative DFS). O(mn log(maxdiff))."""
    m, n = len(h), len(h[0])
    def ok(T):
        seen = {(0, 0)}
        st = [(0, 0)]
        while st:
            x, y = st.pop()
            if (x, y) == (m - 1, n - 1):
                return True
            for dx, dy in D4:
                a, b = x + dx, y + dy
                if 0 <= a < m and 0 <= b < n and (a, b) not in seen and abs(h[a][b] - h[x][y]) <= T:
                    seen.add((a, b))
                    st.append((a, b))
        return False
    lo, hi = 0, max(map(max, h)) - min(map(min, h))
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def min_effort_paths(h):
    """Brute force: enumerate every simple path (tiny grids only) and take the best max step."""
    m, n = len(h), len(h[0])
    best = [INF]
    def go(x, y, seen, cur):
        if (x, y) == (m - 1, n - 1):
            best[0] = min(best[0], cur)
            return
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and (a, b) not in seen:
                seen.add((a, b))
                go(a, b, seen, max(cur, abs(h[a][b] - h[x][y])))
                seen.discard((a, b))
    go(0, 0, {(0, 0)}, 0)
    return best[0]

def min_sum_wrong(h):
    """Ordinary Dijkstra (sum of step costs): answers a different question."""
    m, n = len(h), len(h[0])
    best = [[INF] * n for _ in range(m)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        e, x, y = heapq.heappop(heap)
        if e > best[x][y]:
            continue
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and e + abs(h[a][b] - h[x][y]) < best[a][b]:
                best[a][b] = e + abs(h[a][b] - h[x][y])
                heapq.heappush(heap, (best[a][b], a, b))
    return best[m - 1][n - 1]

for g, want in [([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2), ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1), ([[7]], 0)]:
    got = min_effort(g)
    assert got == want == min_effort_bsearch(g) == min_effort_paths(g), (g, got, want)
    print(g, '->', got)

# ---- sum-Dijkstra is a different problem: same grids, different answers
g = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
print('example 1: max-step answer', min_effort(g), '| sum-of-steps answer (different question)', min_sum_wrong(g))
g = [[0, 5, 5, 5], [1, 9, 9, 5], [2, 3, 4, 5]]
print('another grid: max-step', min_effort(g), '| sum of steps', min_sum_wrong(g))

# ---- exhaustive: every 2x3 grid with values 0..3 and every 3x3 grid with values 0..2
cnt = 0
for m, n, V in [(1, 1, 4), (1, 4, 3), (2, 2, 4), (2, 3, 4), (3, 3, 3)]:
    for vals in itertools.product(range(V), repeat=m * n):
        g = [list(vals[i * n:(i + 1) * n]) for i in range(m)]
        r = min_effort(g)
        assert r == min_effort_bsearch(g) == min_effort_paths(g), g
        cnt += 1
print('exhaustive on', cnt, 'small grids: Dijkstra(max) == binary search on answer == all simple paths')

# ---- seeded random larger grids (no path enumeration, two independent methods)
for _ in range(300):
    m, n = random.randint(1, 7), random.randint(1, 7)
    g = [[random.randint(0, 20) for _ in range(n)] for _ in range(m)]
    assert min_effort(g) == min_effort_bsearch(g), g
print('300 seeded random grids up to 7x7 agree')

# ---- size: 100 x 100 with values up to 10^6, and a snake that forces a long route
m = n = 100
g = [[random.randint(0, 10 ** 6) for _ in range(n)] for _ in range(m)]
assert min_effort(g) == min_effort_bsearch(g)
print('100x100 random, values <= 10^6 ->', min_effort(g))
m = 99                                    # odd number of rows would end on a wall row, so use 99 rows
snake = [[0 if (i % 2 == 0 or (i % 4 == 1 and j == n - 1) or (i % 4 == 3 and j == 0)) else 10 ** 6 for j in range(n)] for i in range(m)]
assert min_effort(snake) == min_effort_bsearch(snake) == 0
print('99x100 snake corridor of equal heights -> 0 (a route of about 5000 cells, no recursion used)')
```

**Output (my run):**
```
[[1, 2, 2], [3, 8, 2], [5, 3, 5]] -> 2
[[1, 2, 3], [3, 8, 4], [5, 3, 5]] -> 1
[[7]] -> 0
example 1: max-step answer 2 | sum-of-steps answer (different question) 4
another grid: max-step 1 | sum of steps 5
exhaustive on 24120 small grids: Dijkstra(max) == binary search on answer == all simple paths
300 seeded random grids up to 7x7 agree
100x100 random, values <= 10^6 -> 335144
99x100 snake corridor of equal heights -> 0 (a route of about 5000 cells, no recursion used)
```

**Edge cases:**
- 1 x 1 grid: start is the goal, effort 0.
- Equal heights everywhere: 0.
- Going away from the goal is allowed and sometimes necessary (the snake corridor winds through about 5000 cells).
- Huge heights (10^6): ints, no overflow in Python.
- Return when the target is popped, not when it is first pushed (a later, better push can still arrive).

**Follow-ups:**
- Why not BFS or DFS with a visited set directly? The best route to a cell depends on its effort, not on who arrived first, so a plain visited set can lock in a worse effort.
- Union-find version? Sort all adjacent-cell edges by step cost and add them until top-left and bottom-right join: the last edge added is the answer (Kruskal-style bottleneck), O(mn log(mn)).
- Why is the maximum spanning-path idea related to MST? The minimax path between two nodes lies on the minimum spanning tree; that is the Q29 connection.

**Common mistakes:**
- Summing the steps (Dijkstra by habit).
- Taking `abs` of the wrong pair, or using the neighbour's height only.
- Returning at the first push of the target.
- Marking cells visited when pushed.

### Q27 ⭐⭐ 🟡 0-1 BFS: minimum obstacles to remove. `grid` is an m x n grid (1 <= m*n <= 10^5) of 0 (empty) and 1 (obstacle) with grid[0][0] = grid[m-1][n-1] = 0. You move up, down, left or right, and stepping onto an obstacle cell costs 1 (you remove it) while stepping onto an empty cell costs 0. Return the minimum number of obstacles removed to get from the top-left to the bottom-right cell. Solve it in O(m*n) with a deque (push 0-cost neighbours to the front, 1-cost to the back) and explain why an ordinary BFS that marks a cell visited the first time it is enqueued gives wrong answers here, and why this beats Dijkstra's log factor. Example: grid=[[0, 1, 1], [1, 1, 0], [1, 1, 0]] -> 2; grid=[[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]] -> 0; grid=[[0]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Shortest path with edge weights only 0 or 1: 0-1 BFS on a deque. Stepping into an obstacle cell costs 1, into an empty cell costs 0.

**Say this first (1 line):** "It is Dijkstra where the heap only ever holds two distances, d and d+1, so a deque replaces it: free moves go to the front, paid moves to the back."

**Brute force:** Bellman-Ford over the grid: sweep every cell and neighbour, relax, and repeat until nothing changes. Up to O((mn)^2) in the worst case. Plain Dijkstra with `heapq` is the middle option, O(mn log(mn)). Both are checkers in the code.

**Optimal:**
- `dist[0][0] = 0`, deque `[(0,0)]`. Pop from the left. For each neighbour with cost `w = grid[nb]` (cost of stepping INTO it): if `dist[cell] + w < dist[nb]`, update; `w == 0` -> `appendleft`, `w == 1` -> `append`.
- Invariant: the deque is always sorted by distance and holds at most two different values, d and d+1. Popping from the left takes the smallest. A 0-move produces distance d, which belongs in front of the d+1 entries; a 1-move produces d+1, which belongs at the back. The code asserts the invariant before every pop on all small grids.
- Why a cell can be queued more than once: it may first be reached with d+1 and later with d. The strict `<` allows that improvement. Since only two values exist at a time, a cell improves at most about twice, so total work stays O(mn). A stale copy is harmless: when popped, its relaxations all fail.
- Why ordinary BFS fails: BFS finalises a cell when it is first enqueued and assumes every edge costs one step. With costs 0 and 1 the first route found (fewest steps) is not the cheapest route (fewest obstacles). The code counts the plain version wrong on 12914 of the 17557 exhaustively tested grids; example 1 gives 3 instead of 2.
- Versus Dijkstra: same relaxations, but a heap push/pop costs O(log) and the deque costs O(1), because the "priority" only takes two consecutive values.

**Complexity:** Time O(mn): each cell is queued a constant number of times (at most twice per improvement level) and scans 4 neighbours. Space O(mn) for `dist` and the deque. The log factor of Dijkstra disappears.

**Dry run:** `[[0,1,1],[1,1,0],[1,1,0]]`.
- Start (0,0), dist 0. Right (0,1): cost 1, dist 1, append. Down (1,0): cost 1, dist 1, append. Deque: (0,1), (1,0).
- Pop (0,1) (dist 1): right (0,2) cost 1 -> 2, append; down (1,1) cost 1 -> 2, append.
- Pop (1,0) (dist 1): down (2,0) -> 2, append; right (1,1) 2 is not less than 2, no change.
- Pop (0,2) dist 2: down (1,2) cost 0 -> 2, appendleft. Pop (1,2): down (2,2) cost 0 -> 2, appendleft. Pop (2,2).
- dist[2][2] = 2.

**Code:**
```python
import heapq
import itertools
import random
from collections import deque

random.seed(27)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
INF = float('inf')

def min_obstacles(grid, check_invariant=False):
    """0-1 BFS: relax like Dijkstra, but a 0-cost move goes to the FRONT of the deque and a 1-cost move to the BACK."""
    m, n = len(grid), len(grid[0])
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0
    dq = deque([(0, 0)])
    while dq:
        if check_invariant:                                  # deque distances are non-decreasing and span at most two values
            ds = [dist[x][y] for x, y in dq]
            assert ds == sorted(ds) and ds[-1] - ds[0] <= 1, ds
        x, y = dq.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n:
                w = grid[a][b]                               # cost of stepping INTO (a, b)
                if dist[x][y] + w < dist[a][b]:              # strict: a cell can be re-queued when a cheaper route appears
                    dist[a][b] = dist[x][y] + w
                    if w:
                        dq.append((a, b))
                    else:
                        dq.appendleft((a, b))
    return dist[m - 1][n - 1]

def dijkstra_obstacles(grid):
    m, n = len(grid), len(grid[0])
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0
    h = [(0, 0, 0)]
    while h:
        d, x, y = heapq.heappop(h)
        if d > dist[x][y]:
            continue
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and d + grid[a][b] < dist[a][b]:
                dist[a][b] = d + grid[a][b]
                heapq.heappush(h, (dist[a][b], a, b))
    return dist[m - 1][n - 1]

def fixpoint_brute(grid):
    """Independent brute force: keep relaxing every cell pair until nothing changes (Bellman-Ford over the grid)."""
    m, n = len(grid), len(grid[0])
    d = [[INF] * n for _ in range(m)]
    d[0][0] = 0
    changed = True
    while changed:
        changed = False
        for x in range(m):
            for y in range(n):
                for dx, dy in D4:
                    a, b = x + dx, y + dy
                    if 0 <= a < m and 0 <= b < n and d[x][y] + grid[a][b] < d[a][b]:
                        d[a][b] = d[x][y] + grid[a][b]
                        changed = True
    return d[m - 1][n - 1]

def plain_bfs_wrong(grid):
    """The tempting bug: ordinary BFS, a cell is finalised the first time it is enqueued, obstacle cost added on the way."""
    m, n = len(grid), len(grid[0])
    dist = {(0, 0): 0}
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + grid[a][b]
                q.append((a, b))
    return dist[(m - 1, n - 1)]

for g, want in [([[0, 1, 1], [1, 1, 0], [1, 1, 0]], 2), ([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0), ([[0]], 0)]:
    got = min_obstacles(g, check_invariant=True)
    assert got == want == dijkstra_obstacles(g) == fixpoint_brute(g), (g, got, want)
    print(g, '->', got, '| plain BFS says', plain_bfs_wrong(g))

# ---- exhaustive over every grid with free corners: 2x3, 3x3, 3x4, 4x4
total = bad_bfs = 0
for m, n in [(1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]:
    inner = [(i, j) for i in range(m) for j in range(n) if (i, j) not in ((0, 0), (m - 1, n - 1))]
    for bits in itertools.product((0, 1), repeat=len(inner)):
        g = [[0] * n for _ in range(m)]
        for (i, j), b in zip(inner, bits):
            g[i][j] = b
        r = min_obstacles(g, check_invariant=True)
        assert r == dijkstra_obstacles(g) == fixpoint_brute(g), g
        total += 1
        bad_bfs += plain_bfs_wrong(g) != r
print('exhaustive on', total, 'grids: 0-1 BFS == Dijkstra == fixpoint, deque stays sorted with span <= 1')
print('plain visited-on-enqueue BFS is wrong on', bad_bfs, 'of those grids')

# ---- seeded random cross-check on bigger grids
for _ in range(300):
    m, n = random.randint(1, 8), random.randint(1, 8)
    g = [[int(random.random() < 0.45) for _ in range(n)] for _ in range(m)]
    g[0][0] = 0
    g[m - 1][n - 1] = 0
    assert min_obstacles(g) == dijkstra_obstacles(g) == fixpoint_brute(g), g
print('300 seeded random grids up to 8x8 agree')

# ---- sizes: m*n = 10^5 (a single row, a single column, 316x316), iterative so no recursion limit
row = [[0] + [1] * (10 ** 5 - 2) + [0]]
assert min_obstacles(row) == 10 ** 5 - 2
col = [[v] for v in row[0]]
assert min_obstacles(col) == 10 ** 5 - 2
big = [[int(random.random() < 0.4) for _ in range(316)] for _ in range(316)]
big[0][0] = big[315][315] = 0
assert min_obstacles(big) == dijkstra_obstacles(big)
print('10^5-cell row and column ->', min_obstacles(row), '; 316x316 random ->', min_obstacles(big))
```

**Output (my run):**
```
[[0, 1, 1], [1, 1, 0], [1, 1, 0]] -> 2 | plain BFS says 3
[[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]] -> 0 | plain BFS says 1
[[0]] -> 0 | plain BFS says 0
exhaustive on 17557 grids: 0-1 BFS == Dijkstra == fixpoint, deque stays sorted with span <= 1
plain visited-on-enqueue BFS is wrong on 12914 of those grids
300 seeded random grids up to 8x8 agree
10^5-cell row and column -> 99998 ; 316x316 random -> 4
```

**Edge cases:**
- 1 x 1 grid: 0.
- Start and end are guaranteed free, so the start cell's own value is never paid.
- A grid that is one long row or column of obstacles: answer is the number of obstacles in the middle; sizes up to 10^5 cells are fine because the loop is iterative.
- A free corridor that is longer than a path through one obstacle: still the corridor wins (cost 0). Example 2 shows it.

**Follow-ups:**
- Cost on edges rather than cells (a weight 0 or 1 per edge)? Same algorithm; the cost is read from the edge.
- Weights 0..K? Dial's algorithm: K + 1 buckets instead of a deque.
- Why not a visited set instead of the strict distance check? With a visited-on-pop set it also works (skip a cell that was already finalised), but then you must set it on pop, never on push.

**Common mistakes:**
- Marking a cell visited when it is enqueued (the BFS bug above).
- Pushing the 0-cost neighbour to the back, which breaks the sorted invariant.
- Adding the cost of the cell you leave instead of the one you enter (the start would be charged).
- Using `<=` in the relaxation and re-queueing forever on zero-cost cycles.

### Q28 ⭐⭐ 🟡 Bellman-Ford with negative edges and negative cycles. `n` nodes 0..n-1 (1 <= n <= 500), `edges` a list of directed [u, v, w] with -100 <= w <= 100 (up to 5000) and `src`. If a negative-weight cycle is reachable from `src`, return None. Otherwise return the list of shortest distances from `src` (None for unreachable nodes). Use n-1 rounds of relaxing every edge, then one extra round to detect a cycle; explain why n-1 rounds suffice, why the check must only consider cycles reachable from src (not just any negative edge), and the O(V*E) cost. Example: n=4, edges=[[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]], src=0 -> [0, 2, 5, 4]; n=3, edges=[[0, 1, 1], [1, 2, -3], [2, 1, 1]], src=0 -> null; n=3, edges=[[1, 2, -1], [2, 1, -1]], src=0 -> [0, null, null].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Single-source shortest paths with negative edge weights: Bellman-Ford (relax every edge V-1 times), plus one more round as a negative-cycle detector.

**Say this first (1 line):** "Dijkstra is out because of the negative edges. Bellman-Ford relaxes every edge n-1 times, since a shortest path has at most n-1 edges; if an edge still improves in round n, a negative cycle reachable from the source exists."

**Brute force:** Floyd-Warshall on all pairs, O(n^3) (125 million steps at n = 500, too slow in Python), then declare a cycle if some node k reachable from `src` has `f[k][k] < 0`. It is the independent checker in the code.

**Optimal:**
- `d = [INF]*n`, `d[src] = 0`.
- Repeat n-1 times: for every edge `(u, v, w)`, if `d[u] != INF and d[u] + w < d[v]`, set `d[v] = d[u] + w`. Stop early if a whole round changes nothing.
- One more round: if any edge with `d[u] != INF` still improves, return `None`.
- Why n-1 rounds suffice: with no negative cycle, some shortest path to each node is simple, so it has at most n-1 edges. By induction, after round k every node whose shortest path has at most k edges holds its correct distance, because round k relaxes the k-th edge of that path after the (k-1)-th was fixed. The worst case is edges listed against the path direction: each round then advances one edge, and the code shows n-2 rounds are not enough on a path of 8 nodes (the check round fires although there is no cycle).
- Why the detector only counts reachable cycles: a negative cycle that `src` cannot reach never gets finite distances, and the answer for the reachable part is still well defined. The guard `d[u] != INF` keeps unreached nodes out of the arithmetic. If you represent INF by a big integer and skip the guard, `INF - 1 < INF` is true for the unreachable cycle in example 3, and the code returns `None` wrongly (the code prints it, and counts 110 of 1000 random graphs wrong).
- Why one extra round finds a reachable negative cycle: going around such a cycle lowers some distance on every lap, so after any number of rounds at least one edge of the cycle can still relax. Conversely, if no negative cycle is reachable, all distances are final after n-1 rounds and nothing improves.
- With `float('inf')`, `inf + w < inf` is already false, so the guard is implicit; with an integer sentinel it is mandatory. The explicit test is the safe habit.

**Complexity:** Time O(V * E) worst case (500 * 5000 = 2.5 million relaxations at the limits, fine); early exit often makes it much faster. Space O(V) for `d` plus the edge list. Dijkstra's O((V + E) log V) needs non-negative weights.

**Dry run:** `n=3, edges=[[0,1,1],[1,2,-3],[2,1,1]], src=0`.
- Start `d = [0, INF, INF]`.
- Round 1: 0->1 gives d1 = 1. 1->2: 1 - 3 = -2, d2 = -2. 2->1: -2 + 1 = -1 < 1, d1 = -1.
- Round 2 (n-1 = 2): 1->2: -1 - 3 = -4, d2 = -4. 2->1: -4 + 1 = -3, d1 = -3.
- Check round: 1->2 would give -6 < -4. An edge still improves, so return `None`.
- Example 1 for contrast: `[0, 2, 5, 4]` settles in 2 rounds with no improvement in the check round (the path 0 -> 2 -> 1 uses the negative edge 2 -> 1 and beats the direct edge).

**Code:**
```python
import itertools
import random

random.seed(28)
INF = float('inf')

def bellman_ford(n, edges, src, rounds=None, guard=True):
    """n-1 rounds of relaxing every edge, then one more round: any improvement means a reachable negative cycle."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n - 1 if rounds is None else rounds):
        changed = False
        for u, v, w in edges:
            if d[u] != INF and d[u] + w < d[v]:          # never relax out of an unreached node
                d[v] = d[u] + w
                changed = True
        if not changed:                                  # early exit: distances are final
            break
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            return None
    return [None if x == INF else x for x in d]

def bellman_ford_unguarded(n, edges, src, big=10 ** 9):
    """Bug: unreached nodes get a large finite number and are relaxed like real ones."""
    d = [big] * n
    d[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] + w < d[v]:
            return None
    return [None if x >= big // 2 else x for x in d]

def floyd_brute(n, edges, src):
    """Independent brute force: all-pairs Floyd-Warshall; a negative cycle shows up as f[k][k] < 0 for a k reachable from src."""
    f = [[INF] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 0
    for u, v, w in edges:
        f[u][v] = min(f[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if f[i][k] + f[k][j] < f[i][j]:
                    f[i][j] = f[i][k] + f[k][j]
    if any(f[src][k] < INF and f[k][k] < 0 for k in range(n)):
        return None
    return [None if x == INF else x for x in f[src]]

for n, e, s, want in [(4, [[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]], 0, [0, 2, 5, 4]),
                      (3, [[0, 1, 1], [1, 2, -3], [2, 1, 1]], 0, None),
                      (3, [[1, 2, -1], [2, 1, -1]], 0, [0, None, None])]:
    got = bellman_ford(n, e, s)
    assert got == want == floyd_brute(n, e, s), (got, want)
    print(n, e, 'src', s, '->', got)

# ---- the two classic bugs on example 3: a negative cycle that is NOT reachable from src
e3 = [[1, 2, -1], [2, 1, -1]]
print('unguarded INF arithmetic on example 3 ->', bellman_ford_unguarded(3, e3, 0), '(false alarm: that cycle is unreachable)')

# ---- why n-1 rounds suffice: a shortest path without a negative cycle has at most n-1 edges, and round k fixes the k-th edge of every
# shortest path. Worst case = path edges listed in REVERSE order, so each round advances only one edge.
n = 8
path = [[i, i + 1, 1] for i in range(n - 1)][::-1]
full = bellman_ford(n, path, 0)
short = bellman_ford(n, path, 0, rounds=n - 2)            # one round too few: distances are not final, so the check round fires
print('reverse-ordered path, n=8: n-1 rounds ->', full, '| n-2 rounds ->', short)
assert full == list(range(n)) and short is None

# ---- exhaustive: every ordered list of up to 3 edges on 3 nodes with weights -2..2 (self loops included), every source
opts = [(u, v, w) for u in range(3) for v in range(3) for w in range(-2, 3)]    # 45 edge options
cnt = neg = 0
for k in range(4):
    for combo in itertools.product(opts, repeat=k):
        edges = [list(x) for x in combo]
        for src in range(3):
            a = bellman_ford(3, edges, src)
            assert a == floyd_brute(3, edges, src), (edges, src)
            neg += a is None
            cnt += 1
print('exhaustive on', cnt, '(graph, source) cases, of which', neg, 'have a reachable negative cycle: Bellman-Ford == Floyd-Warshall')

# ---- seeded random graphs up to n = 7 with a mix of negative edges
for _ in range(1000):
    n = random.randint(1, 7)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-5, 8)] for _ in range(random.randint(0, 14))]
    src = random.randrange(n)
    assert bellman_ford(n, edges, src) == floyd_brute(n, edges, src), (n, edges, src)
print('1000 seeded random graphs agree')

# ---- the unguarded bug versus the correct code over the same random graphs
wrong = 0
for _ in range(1000):
    n = random.randint(1, 7)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-5, 8)] for _ in range(random.randint(0, 14))]
    src = random.randrange(n)
    wrong += bellman_ford_unguarded(n, edges, src) != floyd_brute(n, edges, src)
print('unguarded variant disagrees with the checker on', wrong, 'of 1000 random graphs')

# ---- max size: n = 500, E = 5000, worst-case O(V*E) = about 2.5 * 10^6 relaxations
n, E = 500, 5000
pot = [random.randint(0, 50) for _ in range(n)]
edges = []
for _ in range(E):
    u, v = random.randrange(n), random.randrange(n)
    edges.append([u, v, random.randint(0, 50) + pot[u] - pot[v]])              # reduced-cost form: negative edges, but no negative cycle
assert min(w for _, _, w in edges) < 0
r = bellman_ford(n, edges, 0)
assert r is not None and r[0] == 0
edges += [[0, 1, -100], [1, 0, -100]]                                            # a reachable negative 2-cycle
assert bellman_ford(n, edges, 0) is None
print('n=500, E=5000 with negative edges but no negative cycle: reached', sum(x is not None for x in r),
      'nodes; adding a 2-cycle of weight -200 -> None')
assert bellman_ford(1, [], 0) == [0]
assert bellman_ford(1, [[0, 0, -1]], 0) is None and bellman_ford(1, [[0, 0, 1]], 0) == [0]
print('edge asserts passed (n=1, negative and positive self loops)')
```

**Output (my run):**
```
4 [[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]] src 0 -> [0, 2, 5, 4]
3 [[0, 1, 1], [1, 2, -3], [2, 1, 1]] src 0 -> None
3 [[1, 2, -1], [2, 1, -1]] src 0 -> [0, None, None]
unguarded INF arithmetic on example 3 -> None (false alarm: that cycle is unreachable)
reverse-ordered path, n=8: n-1 rounds -> [0, 1, 2, 3, 4, 5, 6, 7] | n-2 rounds -> None
exhaustive on 279588 (graph, source) cases, of which 69036 have a reachable negative cycle: Bellman-Ford == Floyd-Warshall
1000 seeded random graphs agree
unguarded variant disagrees with the checker on 110 of 1000 random graphs
n=500, E=5000 with negative edges but no negative cycle: reached 500 nodes; adding a 2-cycle of weight -200 -> None
edge asserts passed (n=1, negative and positive self loops)
```

**Edge cases:**
- Negative cycle not reachable from `src` (example 3): distances for the reachable part (just `src`) are returned, unreachable nodes `None`, no error.
- Negative self loop (`[0,0,-1]`): a one-edge negative cycle, `None`; a positive self loop is ignored.
- A negative edge that is not on a cycle is fine (example 1).
- A zero-weight cycle does not improve anything: no detection, correct distances.
- `n = 1`, no edges: `[0]`.
- Undirected graph with a negative edge is itself a negative cycle (go back and forth); treat each undirected edge as two directed ones and Bellman-Ford returns `None`.

**Follow-ups:**
- Which nodes are on the cycle, or which distances are -infinity? Run one more n rounds, mark every node that still improves, and propagate the mark along edges (everything reachable from a marked node is -infinity).
- Cheapest flights within K stops: Bellman-Ford with exactly K+1 rounds, but each round must read the previous round's array (a copy), or the in-place version lets a path use more edges than allowed (Q34 in this part).
- Faster in practice? SPFA (queue-based) often wins, but its worst case is still O(V * E) and it can be attacked.

**Common mistakes:**
- Running too few rounds (n-2), or checking for a cycle before the n-1 rounds are done.
- Dropping the `d[u] != INF` guard with an integer sentinel (false negative-cycle alarms).
- Reporting a cycle if any edge is negative.
- Forgetting the early exit, or using it before the detection round.

### Q29 ⭐⭐ 🟡 Minimum spanning tree weight with Kruskal. `n` nodes 0..n-1 (1 <= n <= 10^4) and `edges` a list of undirected [u, v, w] with 1 <= w <= 10^5 (up to 10^5 edges; repeats and self loops possible). Return the total weight of a minimum spanning tree, or -1 if the graph is disconnected. Several different trees can tie, but their total weight is the same, and the checker accepts only that number. Sort edges by weight and join components with union-find; state the complexity (O(E log E)) and name Prim's algorithm as the heap-based alternative (cut property, Borůvka and second-best trees belong to Part 14). Example: n=4, edges=[[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]] -> 7; n=3, edges=[[0, 1, 2]] -> -1; n=1, edges=[] -> 0; n=3, edges=[[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]] -> 4.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Minimum spanning tree by Kruskal's greedy algorithm, with union-find to test "does this edge close a cycle?".

**Say this first (1 line):** "Sort edges by weight, take an edge if it joins two different components, skip it otherwise. If I end with fewer than n-1 edges, the graph is disconnected, so -1."

**Brute force:** Try every subset of n-1 edges, keep the ones that are acyclic (n-1 edges with no cycle on n nodes is a spanning tree), take the cheapest. That is C(E, n-1) subsets, only usable on tiny graphs. It is a checker in the code.

**Optimal:**
- Sort edges by weight (`sorted(..., key=...)`; ties in any order).
- Union-find with an iterative `find` (path halving) and union by size. For each edge: if `find(u) == find(v)` skip it (a cycle, and this also skips self loops and repeated edges); else union, add `w`, count it.
- Stop early at n-1 edges. At the end, `used == n-1` means connected: return the total, else -1. For n = 1 there is nothing to add: 0.
- Why greedy works (cut property, informally): the cheapest edge crossing any cut between two parts of the nodes belongs to some MST. When Kruskal looks at an edge that joins two components, it is the cheapest edge leaving one of them that has not been considered, so it is safe to take. Skipped edges would close a cycle in which they are the heaviest edge seen so far, so they are safe to drop. The full proof, Borůvka and second-best trees belong to Part 14.
- Ties: several different trees can have the same minimum weight, and which one Kruskal returns depends on the order of equal-weight edges. The code counts 3 minimum trees in the all-equal triangle. The checker only accepts the total, which is unique.
- Prim's algorithm is the heap-based alternative: start from one node, repeatedly pop the cheapest edge leaving the current tree from a heap (lazy deletion of edges to already-visited nodes). Total cost is O(E log V). It wins on dense graphs and when the graph is given as adjacency lists; Kruskal wins when edges are already a list or easy to sort. The code runs both and they agree on every case.

**Complexity:** Sorting: O(E log E). Union-find: O(E * alpha(V)) with path compression and union by size (alpha is the inverse Ackermann function, at most 4 or so here). Total O(E log E), which equals O(E log V) since E <= V^2. Space O(V + E): parent and size arrays, plus the sorted copy of the edges.

**Dry run:** `n=4, edges=[[0,1,1],[1,2,2],[0,2,3],[2,3,4],[1,3,5]]`.
- Sorted by weight: (0,1,1), (1,2,2), (0,2,3), (2,3,4), (1,3,5).
- (0,1,1): different components, take it, total 1.
- (1,2,2): take, total 3. Now {0,1,2}.
- (0,2,3): both in {0,1,2}, skip (cycle).
- (2,3,4): 3 is alone, take, total 7, used = 3 = n-1: stop.
- Answer 7.

**Code:**
```python
import heapq
import itertools
import random

random.seed(29)

def kruskal(n, edges):
    """Sort by weight, add an edge iff it joins two different components. Iterative find, path halving, union by size."""
    parent = list(range(n))
    size = [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    total = used = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a == b:                                  # self loops and cycle-forming edges are skipped here
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        total += w
        used += 1
        if used == n - 1:
            break
    return total if used == n - 1 else -1

def prim(n, edges):
    """Heap-based alternative: grow one tree from node 0 by the cheapest edge leaving it (lazy heap)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            adj[u].append((w, v))
            adj[v].append((w, u))
    seen = [False] * n
    seen[0] = True
    heap = list(adj[0])
    heapq.heapify(heap)
    total, cnt = 0, 1
    while heap and cnt < n:
        w, v = heapq.heappop(heap)
        if seen[v]:
            continue
        seen[v] = True
        total += w
        cnt += 1
        for item in adj[v]:
            if not seen[item[1]]:
                heapq.heappush(heap, item)
    return total if cnt == n else -1

def mst_brute(n, edges):
    """Try every (n-1)-edge subset: it is a spanning tree iff it has no cycle. Take the cheapest."""
    if n == 1:
        return 0
    best = None
    for sub in itertools.combinations(edges, n - 1):
        p = list(range(n))
        def find(x):
            while p[x] != x:
                x = p[x]
            return x
        ok = True
        for u, v, w in sub:
            a, b = find(u), find(v)
            if a == b:
                ok = False
                break
            p[a] = b
        if ok:
            t = sum(e[2] for e in sub)
            best = t if best is None or t < best else best
    return -1 if best is None else best

def count_min_trees(n, edges):
    """How many distinct (n-1)-edge spanning trees have the optimal weight? (tiny graphs; shows that the tree is not unique)"""
    best, cnt = None, 0
    for sub in itertools.combinations(range(len(edges)), n - 1):
        p = list(range(n))
        def find(x):
            while p[x] != x:
                x = p[x]
            return x
        ok = True
        for i in sub:
            u, v, _ = edges[i]
            a, b = find(u), find(v)
            if a == b:
                ok = False
                break
            p[a] = b
        if ok:
            t = sum(edges[i][2] for i in sub)
            if best is None or t < best:
                best, cnt = t, 1
            elif t == best:
                cnt += 1
    return best, cnt

for n, e, want in [(4, [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]], 7), (3, [[0, 1, 2]], -1), (1, [], 0),
                   (3, [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]], 4)]:
    got = kruskal(n, e)
    assert got == want == prim(n, e) == mst_brute(n, e), (n, e, got, want)
    print(n, e, '->', got)

# ---- ties: several different trees, one weight
n, e = 3, [[0, 1, 2], [1, 2, 2], [0, 2, 2]]
print('triangle with all weights 2: (weight, number of minimum trees) =', count_min_trees(n, e), '-> only the weight is unique')
n, e = 3, [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]]
print('example 4: (weight, number of minimum trees) =', count_min_trees(n, e), '; the weight-1 self loop is never usable')

# ---- exhaustive: all multisets of up to 4 edges on 3 nodes (weights 1..3, self loops included), and up to 4 edges on 4 nodes (weights 1..2)
cnt = 0
for n, W, K in [(3, 3, 4), (4, 2, 4)]:
    opts = [(u, v, w) for u in range(n) for v in range(n) for w in range(1, W + 1)]
    for k in range(K + 1):
        for combo in itertools.combinations_with_replacement(opts, k):
            edges = [list(x) for x in combo]
            r = kruskal(n, edges)
            assert r == prim(n, edges) == mst_brute(n, edges), (n, edges)
            cnt += 1
print('exhaustive on', cnt, 'multigraphs: Kruskal == Prim == best spanning subset')

for _ in range(500):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n), random.randint(1, 9)] for _ in range(random.randint(0, 12))]
    assert kruskal(n, edges) == prim(n, edges), (n, edges)
print('500 seeded random graphs: Kruskal == Prim (n up to 8)')

# ---- max size: n = 10^4, E = 10^5 with repeats and self loops; connected by a spine so the answer is not -1
n = 10 ** 4
edges = [[i, i + 1, random.randint(1, 10 ** 5)] for i in range(n - 1)]
edges += [[random.randrange(n), random.randrange(n), random.randint(1, 10 ** 5)] for _ in range(10 ** 5 - len(edges))]
k, p = kruskal(n, edges), prim(n, edges)
assert k == p and k != -1
print('n=10^4, E=10^5: Kruskal', k, '== Prim', p)
assert kruskal(n, [e for e in edges if e[0] != 5000 and e[1] != 5000]) == -1    # isolating one node disconnects the graph
print('removing every edge at node 5000 -> -1 (disconnected)')
assert kruskal(1, [[0, 0, 5]]) == 0
print('edge asserts passed')
```

**Output (my run):**
```
4 [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]] -> 7
3 [[0, 1, 2]] -> -1
1 [] -> 0
3 [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]] -> 4
triangle with all weights 2: (weight, number of minimum trees) = (4, 3) -> only the weight is unique
example 4: (weight, number of minimum trees) = (4, 3) ; the weight-1 self loop is never usable
exhaustive on 90370 multigraphs: Kruskal == Prim == best spanning subset
500 seeded random graphs: Kruskal == Prim (n up to 8)
n=10^4, E=10^5: Kruskal 58934380 == Prim 58934380
removing every edge at node 5000 -> -1 (disconnected)
edge asserts passed
```

**Edge cases:**
- Disconnected graph: fewer than n-1 usable edges, return -1 (example 2). Do not return a spanning forest weight.
- `n = 1` and no edges: 0.
- Self loops: `find(u) == find(u)`, always skipped (the weight-1 self loop in example 4 is never counted).
- Repeated edges between the same pair: the cheaper one is processed first; the second then closes a cycle and is skipped.
- Many equal weights: any order gives the same total (checked exhaustively against the brute force).

**Follow-ups:**
- Maximum spanning tree? Sort descending, or negate the weights.
- Is the MST path also the minimax (bottleneck) path between two nodes? Yes. That is the idea behind the minimum-effort grid question (Q26 in this part), where union-find over sorted edges is the alternative solution.
- Kruskal or Prim for 10^4 nodes and 10^5 edges? Either; the sort in Kruskal runs in C and is fast in Python. For a complete graph given as points (about n^2/2 edges), Prim with an O(n^2) array avoids materialising the edges (Q37).

**Common mistakes:**
- Not handling disconnected graphs (returning the sum of what was joined).
- Comparing `u != v` instead of components (misses cycles of length 3 and more).
- Recursive `find` without compression on a path-shaped union order.
- Claiming the MST itself is unique: only the weight is, unless all weights are distinct.

### Q30 ⭐⭐ 🟡 Open the lock (BFS over an implicit graph). A lock has four wheels, each showing a digit 0-9; one move turns one wheel one step up or down and 9 and 0 wrap around. It starts at '0000'. `deadends` is a list of up to 500 four-digit strings that jam the lock (if you reach one you cannot continue from it) and `target` is a four-digit string. Return the minimum number of moves to reach `target`, or -1 if impossible (also -1 if '0000' itself is a dead end; if `target` is a dead end it is unreachable). Describe the implicit graph (10^4 states, 8 neighbours each) and why you do not build it up front. Example: deadends=['0201', '0101', '0102', '1212', '2002'], target='0202' -> 6; deadends=['8888'], target='0009' -> 1; deadends=['0000'], target='8888' -> -1; deadends=['8887', '8889', '8878', '8898', '8788', '8988', '7888', '9888'], target='8888' -> -1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Shortest path in an unweighted implicit graph: BFS where a state is a string and neighbours are computed on demand.

**Say this first (1 line):** "Each four-digit combination is a node, each single-wheel turn is an edge, every edge costs one move, so BFS from '0000' gives the fewest moves. Dead ends are nodes I refuse to enter."

**Brute force:** DFS or enumerating all move sequences is exponential and finds a path, not the shortest. A level-by-level BFS using sets (no queue, no distance dictionary) is a second, independent implementation, and is used as the checker in the code, together with a bidirectional BFS.

**Optimal:**
- Nodes: the 10^4 strings `'0000'..'9999'`. Edges: 4 wheels times 2 directions, so exactly 8 neighbours per state; for example `'0000'` goes to `'1000'`, `'9000'`, `'0100'`, `'0900'` and so on. The code checks that all 10^4 states have 8 distinct neighbours (so 40000 undirected edges) and that all are reachable.
- Why not build it up front: the neighbours follow from a rule in two lines, so a generator function is shorter than an adjacency table, needs no memory for edges, and generalises to states where the graph is too large to store (sliding puzzle, Q32 in this part). With only 10^4 states, building it would also work here; the habit is the point.
- Algorithm: if `'0000'` is a dead end, return -1. Queue of `(state, moves)`, `seen = {'0000'}`. Pop; if it is the target, return its moves; for each neighbour not dead and not seen, mark seen and push (mark on push, so a state is queued once).
- Dead ends are simply never entered. The target being a dead end means it is never reached, so the answer is -1 without a special case, but the start being dead needs the explicit check (the start is added to `seen` before any dead-end test; the code shows the bug returning 8 instead of -1).
- BFS correctness: all edges cost 1, so the first time a state is popped its distance is minimal.
- Without dead ends the answer is the sum over wheels of `min(digit, 10 - digit)`; the code confirms it on 1429 sampled targets, and the farthest state `5555` is 20 moves away.

**Complexity:** Time O(S * 8) with S = 10^4 states, so at most 80000 neighbour visits; each costs O(1) string building (4 characters) and set lookups. Space O(S) for `seen` and the queue. With the 500 dead ends of the prompt only fewer states are visited.

**Dry run:** `deadends=['8888'], target='0009'`.
- Start `'0000'`, 0 moves. Neighbours: `'1000'`, `'9000'`, `'0100'`, `'0900'`, `'0010'`, `'0090'`, `'0001'`, `'0009'` (all 1 move).
- The target `'0009'` is one of them (the last wheel turned down from 0 to 9 by wrap-around). Pop it at 1 move: answer 1.
- Example 1 (answer 6): each of the six 4-move routes to `'0202'` hits a dead end (`'0101'`, `'0102'` or `'0201'`). One shortest route found by BFS is 0000, 1000, 1100, 1200, 1201, 1202, 0202: six moves.

**Code:**
```python
import random
from collections import deque

random.seed(30)

def neighbours(s):
    """The implicit graph: 8 neighbours computed on demand (4 wheels x up/down, with wrap-around)."""
    for i in range(4):
        d = int(s[i])
        for step in (1, 9):                               # +1 and -1 mod 10
            yield s[:i] + str((d + step) % 10) + s[i + 1:]

def open_lock(deadends, target):
    dead = set(deadends)
    if '0000' in dead:
        return -1
    seen = {'0000'}
    q = deque([('0000', 0)])
    while q:
        s, d = q.popleft()
        if s == target:
            return d
        for t in neighbours(s):
            if t not in dead and t not in seen:           # mark on PUSH so no state is queued twice
                seen.add(t)
                q.append((t, d + 1))
    return -1

def open_lock_levels(deadends, target):
    """Independent brute force: expand one whole level at a time with sets (no queue, no per-node distance)."""
    dead = set(deadends)
    if '0000' in dead:
        return -1
    level, seen, d = {'0000'}, {'0000'}, 0
    while level:
        if target in level:
            return d
        nxt = set()
        for s in level:
            for t in neighbours(s):
                if t not in dead and t not in seen:
                    nxt.add(t)
        seen |= nxt
        level, d = nxt, d + 1
    return -1

def open_lock_bidirectional(deadends, target):
    """Follow-up: grow the smaller frontier from each end; meet in the middle."""
    dead = set(deadends)
    if '0000' in dead or target in dead:
        return -1
    if target == '0000':
        return 0
    a, b, seen_a, seen_b, d = {'0000'}, {target}, {'0000'}, {target}, 0
    while a and b:
        if len(a) > len(b):
            a, b, seen_a, seen_b = b, a, seen_b, seen_a
        nxt = set()
        d += 1
        for s in a:
            for t in neighbours(s):
                if t in seen_b:
                    return d
                if t not in dead and t not in seen_a:
                    seen_a.add(t)
                    nxt.add(t)
        a = nxt
    return -1

def open_lock_no_start_check(deadends, target):
    """Bug: forget that '0000' itself may be jammed."""
    dead = set(deadends)
    seen = {'0000'}
    q = deque([('0000', 0)])
    while q:
        s, d = q.popleft()
        if s == target:
            return d
        for t in neighbours(s):
            if t not in dead and t not in seen:
                seen.add(t)
                q.append((t, d + 1))
    return -1

for de, tg, want in [(['0201', '0101', '0102', '1212', '2002'], '0202', 6), (['8888'], '0009', 1),
                     (['0000'], '8888', -1), (['8887', '8889', '8878', '8898', '8788', '8988', '7888', '9888'], '8888', -1)]:
    got = open_lock(de, tg)
    assert got == want == open_lock_levels(de, tg) == open_lock_bidirectional(de, tg), (de, tg, got, want)
    print(de, tg, '->', got)
print("forgetting the '0000' dead-end check on example 3 ->", open_lock_no_start_check(['0000'], '8888'), '(should be -1)')

# ---- the graph itself: 10^4 states, every state has exactly 8 distinct neighbours, all reachable, distance = sum of wheel distances
states = [f'{i:04d}' for i in range(10 ** 4)]
assert all(len(set(neighbours(s))) == 8 for s in states)
dist = {'0000': 0}
q = deque(['0000'])
while q:
    s = q.popleft()
    for t in neighbours(s):
        if t not in dist:
            dist[t] = dist[s] + 1
            q.append(t)
assert len(dist) == 10 ** 4
assert all(dist[s] == sum(min(int(c), 10 - int(c)) for c in s) for s in states)
print('states', len(states), '| neighbours each 8 | edges', 8 * len(states) // 2, '| farthest state', max(dist, key=dist.get), 'at', max(dist.values()), 'moves')

# ---- every possible target with no dead ends equals the wheel-distance formula
for s in states[::7]:
    assert open_lock([], s) == dist[s]
print('open_lock([], target) == sum of per-wheel distances on', len(states[::7]), 'sampled targets')

# ---- seeded random cross-check with up to 500 dead ends
def rnd():
    return f'{random.randrange(10 ** 4):04d}'
for _ in range(300):
    de = [rnd() for _ in range(random.choice([0, 5, 50, 500, 2000]))]
    tg = rnd()
    r = open_lock(de, tg)
    assert r == open_lock_levels(de, tg) == open_lock_bidirectional(de, tg), (de[:5], tg)
print('300 seeded random cases: queue BFS == level-set BFS == bidirectional BFS')

# ---- edge cases
assert open_lock([], '0000') == 0
assert open_lock(['0000'], '0000') == -1
assert open_lock(['0001'], '0001') == -1                  # target is a dead end
assert open_lock(['1000', '9000', '0100', '0900', '0010', '0090', '0001', '0009'], '5555') == -1   # all 8 neighbours of the start jammed
print('edge asserts passed')
```

**Output (my run):**
```
['0201', '0101', '0102', '1212', '2002'] 0202 -> 6
['8888'] 0009 -> 1
['0000'] 8888 -> -1
['8887', '8889', '8878', '8898', '8788', '8988', '7888', '9888'] 8888 -> -1
forgetting the '0000' dead-end check on example 3 -> 8 (should be -1)
states 10000 | neighbours each 8 | edges 40000 | farthest state 5555 at 20 moves
open_lock([], target) == sum of per-wheel distances on 1429 sampled targets
300 seeded random cases: queue BFS == level-set BFS == bidirectional BFS
edge asserts passed
```

**Edge cases:**
- Target `'0000'` and not dead: 0 moves.
- `'0000'` dead: -1 at once, even if the target is `'0000'`.
- Target dead: -1.
- Start enclosed by 8 dead neighbours: BFS exhausts and returns -1 (the last example, and the 4th prompt example).
- Duplicate dead ends in the list: a set handles them.
- 9 to 0 and 0 to 9 wrap, so `'0009'` is one move away.

**Follow-ups:**
- Faster in the worst case? Bidirectional BFS (in the code) searches from both ends and cuts the work from about b^d to 2 * b^(d/2); here the graph is small, so the gain is modest.
- Return the actual sequence? Store a parent dictionary and walk it back from the target.
- Many targets from one start? One BFS gives all distances; the code builds the full distance table that way.

**Common mistakes:**
- Marking states visited when popped (queues duplicates, up to 8 times more work).
- Forgetting the wrap-around (`(d + 1) % 10`, `(d + 9) % 10`).
- Not checking the start against the dead ends.
- Using a list for `deadends` lookups (O(500) per check instead of O(1)); convert to a set once.

### Q31 ⭐⭐ 🟡 Topological sort by DFS (reverse postorder). `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` a list of directed [u, v] (0 <= len <= 2*10^5; self loops possible). Run an iterative three-colour DFS: loop over start nodes 0, 1, ..., n-1 in ascending order, explore each node's out-edges in input order, append a node to `post` when it finishes, and return `post` reversed. If any edge reaches a node currently on the DFS path, return []. This order is deterministic, and the checker accepts exactly this list. Explain why reverse postorder puts every edge u -> v with u before v, and why the order generally differs from Kahn's. Sizes are chosen so that a recursive DFS would exceed CPython's default recursion limit of 1000, so an iterative method (queue or explicit stack) is required. Example: n=4, edges=[[0, 1], [0, 2], [1, 3], [2, 3]] -> [0, 2, 1, 3]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> []; n=3, edges=[] -> [2, 1, 0]; n=5, edges=[[3, 1], [4, 1], [4, 0], [2, 3]] -> [4, 2, 3, 1, 0].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort by depth-first search: reverse postorder, with three colours (new, on the path, finished) for cycle detection. Iterative, because the input is deep.

**Say this first (1 line):** "A node is appended after everything reachable from it has finished, so reversing that finish order puts every node before its successors. An edge into a node still on the current path is a cycle. The DFS must be iterative: a 10^5-node chain breaks CPython's recursion limit of 1000."

**Brute force:** The textbook recursive DFS gives the same list (it is the specification in the code), but a path of 5000 nodes already raises `RecursionError`, so it fails the stated sizes. Another brute force is to try every permutation of the nodes and check all edges, O(n! * E), used mentally for n <= 8. For the cycle test the code also compares with Kahn's algorithm.

**Optimal:**
- `color`: 0 new, 1 on the current DFS path, 2 finished. `post` is the list of finished nodes.
- For each start node `s` in ascending order: if new, mark 1 and push a frame `(s, iterator over adj[s])`.
- Loop on the top frame. Take the next out-neighbour `v` from its iterator:
  - `color[v] == 1`: back edge, so there is a cycle: return `[]`. This includes a self loop.
  - `color[v] == 0`: mark 1, push a frame for `v`, `break` out of the `for` (go deeper). The iterator keeps its position, so when `v` finishes we continue with the next edge.
  - `color[v] == 2`: already finished, ignore.
- If the iterator is exhausted (the `for ... else` branch), `u` is finished: mark 2, append to `post`, pop the frame.
- Return `post[::-1]`.
- Why reverse postorder is topological: take an edge `u -> v` in an acyclic graph. When DFS first examines the edge, `v` is either new (then `v` finishes before `u` does, since `u` is still open), or already finished (so `v` finished before `u`). A third possibility, `v` on the path, is a cycle and has been excluded. So in every case `v` is finished before `u`, and in the reversed list `u` comes before `v`.
- Why the order generally differs from Kahn's: Kahn emits nodes as their in-degrees reach 0, which is a breadth-first flavour, ascending by label here; DFS order depends on the visiting order and ends with the last start node first (the empty graph gives `[2, 1, 0]`, Kahn gives `[0, 1, 2]`). Both are valid topological orders. The code counts the graphs where they differ (364 of the 572 acyclic graphs tested).
- The checker accepts exactly this list, so the deterministic rules matter: start nodes ascending, out-edges in input order, post appended on finish, final reversal.

**Complexity:** Time O(V + E): each node gets one frame and each edge is examined once through the iterator. Space O(V + E) for the adjacency lists, colours, the explicit stack (up to V frames) and `post`.

**Dry run:** `n=4, edges=[[0,1],[0,2],[1,3],[2,3]]`.
- Start 0: colour 1. Edges of 0: 1, then 2. Go to 1 (colour 1).
- Node 1: edge to 3, new, go to 3. Node 3 has no edges: finish, `post=[3]`.
- Back in 1: no more edges, finish, `post=[3,1]`.
- Back in 0: next edge to 2, new, go to 2. Edge 2->3: 3 is finished, ignore. Finish 2: `post=[3,1,2]`. Finish 0: `post=[3,1,2,0]`.
- Starts 1, 2, 3 are already done. Reverse: `[0,2,1,3]`, the prompt's answer. Kahn would give `[0,1,2,3]`.

**Code:**
```python
import itertools
import random
import sys
from collections import deque

random.seed(31)

def dfs_topo(n, edges):
    """Iterative three-colour DFS. 0 = new, 1 = on the current path, 2 = finished. Returns reverse postorder or [] on a cycle."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    post = []
    for s in range(n):                                   # start nodes in ascending order
        if color[s]:
            continue
        color[s] = 1
        stack = [(s, iter(adj[s]))]                      # each frame remembers how far we got in its edge list
        while stack:
            u, it = stack[-1]
            for v in it:                                 # resumes where it left off
                if color[v] == 1:                        # edge to a node on the path: cycle (also catches self loops)
                    return []
                if color[v] == 0:
                    color[v] = 1
                    stack.append((v, iter(adj[v])))
                    break                                # go deeper; come back to this frame later
            else:                                        # edge list exhausted: u is finished
                color[u] = 2
                post.append(u)
                stack.pop()
    return post[::-1]

def dfs_topo_recursive(n, edges):
    """Textbook recursive version: the specification for the order (small n only, or it hits the recursion limit)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    post = []
    cyc = [False]
    def go(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1:
                cyc[0] = True
            elif color[v] == 0:
                go(v)
        color[u] = 2
        post.append(u)
    for s in range(n):
        if color[s] == 0:
            go(s)
    return [] if cyc[0] else post[::-1]

def kahn(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == n else []

def is_topological(n, edges, order):
    pos = {x: i for i, x in enumerate(order)}
    return len(order) == n and len(pos) == n and all(pos[u] < pos[v] for u, v in edges)

for n, e, want in [(4, [[0, 1], [0, 2], [1, 3], [2, 3]], [0, 2, 1, 3]), (3, [[0, 1], [1, 2], [2, 0]], []),
                   (3, [], [2, 1, 0]), (5, [[3, 1], [4, 1], [4, 0], [2, 3]], [4, 2, 3, 1, 0])]:
    got = dfs_topo(n, e)
    assert got == want == dfs_topo_recursive(n, e), (n, e, got, want)
    print(n, e, '->', got, '| Kahn gives', kahn(n, e))

# ---- the recursion limit: a 5000-node path
n = 5000
path = [[i, i + 1] for i in range(n - 1)]
try:
    dfs_topo_recursive(n, path)
except RecursionError:
    print('recursive DFS on a', n, 'node path -> RecursionError (limit', sys.getrecursionlimit(), ')')
assert dfs_topo(n, path) == list(range(n))
n = 2 * 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
assert dfs_topo(n, path) == list(range(n))
assert dfs_topo(n, [[i + 1, i] for i in range(n - 1)]) == list(range(n - 1, -1, -1))
assert dfs_topo(n, path + [[n - 1, 0]]) == []                           # one back edge closes the cycle
print('iterative: 2*10^5-node path, its reverse, and the path closed into a cycle all handled')

# ---- exhaustive: every edge SET on n <= 4 (self loops included for n <= 3), plus ordered edge lists with repeats on n = 3
cnt = cyc = differs = 0
for n, loops in [(1, True), (2, True), (3, True), (4, False)]:
    pairs = [(a, b) for a in range(n) for b in range(n) if loops or a != b]
    for mask in range(1 << len(pairs)):
        e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        r = dfs_topo(n, e)
        assert r == dfs_topo_recursive(n, e), (n, e)
        k = kahn(n, e)
        assert (r == []) == (k == []), (n, e)                           # both detect exactly the cyclic graphs
        if r:
            assert is_topological(n, e, r) and is_topological(n, e, k)
            differs += r != k
        else:
            cyc += 1
        cnt += 1
print('exhaustive on', cnt, 'graphs:', cyc, 'cyclic ->', '[]; every acyclic one gives a valid order equal to the recursive DFS;',
      'DFS order differs from Kahn order on', differs)
opts = [(a, b) for a in range(3) for b in range(3)]
for k in range(4):
    for combo in itertools.product(opts, repeat=k):
        e = [list(p) for p in combo]
        assert dfs_topo(3, e) == dfs_topo_recursive(3, e)
print('ordered edge lists with repeats on 3 nodes also match the recursive version')

# ---- seeded random DAGs and cyclic graphs
for _ in range(500):
    n = random.randint(1, 9)
    perm = list(range(n))
    random.shuffle(perm)
    e = [[perm[min(a, b)], perm[max(a, b)]] for a, b in ((random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, 14))) if a != b]
    r = dfs_topo(n, e)
    assert r == dfs_topo_recursive(n, e) and is_topological(n, e, r)
print('500 seeded random DAGs: valid order, equal to the recursive DFS')

# ---- big: 10^5 nodes, 2*10^5 edges, random DAG over a shuffled labelling
n, E = 10 ** 5, 2 * 10 ** 5
perm = list(range(n))
random.shuffle(perm)
e = []
while len(e) < E:
    a, b = random.randrange(n), random.randrange(n)
    if a != b:
        e.append([perm[min(a, b)], perm[max(a, b)]])
r = dfs_topo(n, e)
assert is_topological(n, e, r)
print('n=10^5, E=2*10^5 random DAG: valid topological order of length', len(r))
assert dfs_topo(1, [[0, 0]]) == []
print('self loop -> []')
```

**Output (my run):**
```
4 [[0, 1], [0, 2], [1, 3], [2, 3]] -> [0, 2, 1, 3] | Kahn gives [0, 1, 2, 3]
3 [[0, 1], [1, 2], [2, 0]] -> [] | Kahn gives []
3 [] -> [2, 1, 0] | Kahn gives [0, 1, 2]
5 [[3, 1], [4, 1], [4, 0], [2, 3]] -> [4, 2, 3, 1, 0] | Kahn gives [2, 4, 3, 0, 1]
recursive DFS on a 5000 node path -> RecursionError (limit 1000 )
iterative: 2*10^5-node path, its reverse, and the path closed into a cycle all handled
exhaustive on 4626 graphs: 4054 cyclic -> []; every acyclic one gives a valid order equal to the recursive DFS; DFS order differs from Kahn order on 364
ordered edge lists with repeats on 3 nodes also match the recursive version
500 seeded random DAGs: valid order, equal to the recursive DFS
n=10^5, E=2*10^5 random DAG: valid topological order of length 100000
self loop -> []
```

**Edge cases:**
- Self loop: the neighbour is the node itself with colour 1, so `[]`.
- No edges: all nodes isolated, order `[n-1, ..., 0]` (reverse of the start order).
- A cycle that is only reachable from a later start node is still found, since every unvisited node becomes a start.
- A cycle that sits next to a valid part (the 3-cycle example) returns `[]`, not a partial order.
- Repeated edges: the second one sees colour 2 or 1 and behaves correctly (tested with repeats on 3 nodes).
- Deep chains (2 * 10^5 nodes, both directions) run without recursion.

**Follow-ups:**
- Can I raise the recursion limit instead? `sys.setrecursionlimit` lets the interpreter try deeper, but each frame still uses C stack and a very deep chain can crash the process; the explicit stack is the safe fix. Part 7 Q35 covers the same trap for skewed trees.
- Why two colours are not enough: a visited flag cannot tell a back edge (cycle) from an edge to an already finished node (harmless cross or forward edge). Both look "visited".
- DFS or Kahn? Kahn gives levels (used in Q24) and the cycle check is a count; DFS gives a canonical order and generalises to strongly connected components (Part 14).

**Common mistakes:**
- Appending to `post` when a node is pushed instead of when it finishes.
- Forgetting to reverse.
- A single `visited` set for cycle detection (false cycles on diamonds like 0->1, 0->2, 1->3, 2->3).
- Processing the stack as plain "pop and push all neighbours": that gives a different order and does not know when a node finishes.

### Q32 ⭐⭐ 🔴 Sliding puzzle (state-space BFS). The board is a 2 x 3 grid holding the numbers 0-5 once each, where 0 is the blank. One move slides a tile that is up, down, left or right of the blank into it. Return the minimum number of moves to reach [[1,2,3],[4,5,0]], or -1 if it is unreachable. Treat each board as one node (flatten it to a tuple) and BFS; state the number of states (720), why exactly half of them are unreachable, and why the same code on a bigger board needs a smarter search. Example: board=[[1, 2, 3], [4, 0, 5]] -> 1; board=[[1, 2, 3], [5, 4, 0]] -> -1; board=[[4, 1, 2], [5, 0, 3]] -> 5; board=[[1, 2, 3], [4, 5, 0]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** State-space BFS: each configuration is a node, each legal move is an edge, all edges cost one move.

**Say this first (1 line):** "Flatten the board to a tuple so it is hashable, BFS from the start to the goal with a visited set. There are only 720 boards, so it is instant, and exactly half of them cannot reach the goal."

**Brute force:** DFS or random walks do not give the minimum and can loop forever without a visited set. A second exact method is one BFS backwards from the goal over all boards: moves are reversible, so the distance from the goal to a board equals the distance from the board to the goal. That gives the whole answer table at once, and it is the checker in the code (all 720 boards agree).

**Optimal:**
- State: the board read row by row as a 6-tuple, for example `(4, 1, 2, 5, 0, 3)`. Goal: `(1, 2, 3, 4, 5, 0)`.
- Neighbours of the blank: a precomputed table of adjacent positions for the 2 x 3 shape (position 0 touches 1 and 3, position 1 touches 0, 2 and 4, and so on). Swap the blank with each neighbour to get the next board.
- BFS with a `deque` of `(state, moves)` and a `seen` set. First time the goal appears, its move count is the minimum, because every move costs 1. If the queue empties without the goal, return -1.
- Why 720 states: the 6 cells hold 6 distinct values, so 6! = 720 boards.
- Why exactly half are unreachable: look at the 5 numbered tiles read row by row and count inversions (pairs in the wrong order). Sliding a tile horizontally does not change the reading order. Sliding a tile vertically jumps it over exactly 2 other tiles on a 3-wide board, which changes the inversion count by 0 or +-2, so the parity never changes. The goal has 0 inversions (even), so only even-inversion boards are reachable. The code verifies on all 720 boards that "reachable" and "even inversions" are the same set: 360 and 360. Example 2 (`1 2 3 5 4`, one inversion) is therefore -1.
- Bigger boards: 3 x 3 has 9! = 362,880 boards (181,440 reachable); BFS still fits in memory (the code runs it, hardest board 31 moves). 4 x 4 has 16! = about 2 * 10^13 boards, so plain BFS is hopeless: use A* or IDA* with the Manhattan-distance heuristic (or pattern databases), which explores only promising boards.

**Complexity:** Time O(S * b) with S <= 720 states and branching factor b <= 3, so at most 2160 successor checks; each builds a 6-tuple, O(6). Space O(S) for `seen` and the queue. For an n x m board: S = (nm)!, so factorial growth.

**Dry run:** `[[4,1,2],[5,0,3]]` -> flat `(4,1,2,5,0,3)`, answer 5.
- Blank at position 4. One shortest route (found by the BFS): slide 5 right -> `(4,1,2,0,5,3)`; slide 4 down -> `(0,1,2,4,5,3)`; slide 1 left -> `(1,0,2,4,5,3)`; slide 2 left -> `(1,2,0,4,5,3)`; slide 3 up -> `(1,2,3,4,5,0)`.
- That is 5 moves. BFS tries all boards at distance 1, 2, ..., and the goal first appears at level 5.

**Code:**
```python
import itertools
import math
from collections import Counter, deque

GOAL = (1, 2, 3, 4, 5, 0)
# neighbours of each flat position on a 2 x 3 board: index = 3 * row + col
NB = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}

def sliding_puzzle(board):
    """BFS over boards. A node is the whole board flattened to a tuple (hashable, so it can live in a set)."""
    start = tuple(x for row in board for x in row)
    if start == GOAL:
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        s, d = q.popleft()
        z = s.index(0)
        for j in NB[z]:                                   # slide the tile at j into the blank
            l = list(s)
            l[z], l[j] = l[j], l[z]
            t = tuple(l)
            if t not in seen:
                if t == GOAL:
                    return d + 1
                seen.add(t)
                q.append((t, d + 1))
    return -1

def distance_table():
    """Independent method: one BFS BACKWARDS from the goal over all boards. Moves are reversible, so distance is symmetric."""
    dist = {GOAL: 0}
    frontier = [GOAL]
    while frontier:
        nxt = []
        for s in frontier:
            z = s.index(0)
            for j in NB[z]:
                l = list(s)
                l[z], l[j] = l[j], l[z]
                t = tuple(l)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    nxt.append(t)
        frontier = nxt
    return dist

def inversions_even(flat):
    tiles = [x for x in flat if x]
    inv = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inv % 2 == 0

for b, want in [([[1, 2, 3], [4, 0, 5]], 1), ([[1, 2, 3], [5, 4, 0]], -1), ([[4, 1, 2], [5, 0, 3]], 5), ([[1, 2, 3], [4, 5, 0]], 0)]:
    got = sliding_puzzle(b)
    assert got == want, (b, got, want)
    print(b, '->', got)

# ---- all 720 boards: forward BFS equals the backward table, and exactly half are unreachable
table = distance_table()
boards = list(itertools.permutations(range(6)))
assert len(boards) == 720
res = {}
for p in boards:
    b = [list(p[:3]), list(p[3:])]
    res[p] = sliding_puzzle(b)
    assert res[p] == table.get(p, -1), p
reach = sum(v >= 0 for v in res.values())
print('boards', len(boards), '| reachable', reach, '| unreachable', len(boards) - reach, '| hardest board needs', max(res.values()), 'moves')
print('boards per distance:', sorted(Counter(v for v in res.values() if v >= 0).items()))

# ---- why exactly half: a move never changes the parity of inversions among the 5 tiles (read row by row), and the goal has 0 inversions
assert all((res[p] >= 0) == inversions_even(p) for p in boards)
print('reachable  <=>  even number of inversions among tiles 1..5: holds for all 720 boards')
# a horizontal slide keeps the reading order of the tiles; a vertical slide jumps one tile over exactly 2 others (3-wide board), an even change
unsolvable = [[1, 2, 3], [5, 4, 0]]
print('example 2 has tiles read 1 2 3 5 4: one inversion (odd) ->', sliding_puzzle(unsolvable))

# ---- the state space grows too fast for the same code on bigger boards
print('states: 2x3', math.factorial(6), 'reachable', math.factorial(6) // 2, '| 3x3', math.factorial(9), 'reachable', math.factorial(9) // 2,
      '| 4x4', math.factorial(16), 'reachable', math.factorial(16) // 2)

# ---- the same BFS code does handle the 3x3 (8-puzzle) in memory, to show where the limit starts
def bfs_count_3x3():
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    seen = {goal}
    fr = [goal]
    depth = 0
    while True:
        nxt = []
        for s in fr:
            z = s.index(0)
            r, c = divmod(z, 3)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = r + dr, c + dc
                if 0 <= a < 3 and 0 <= b < 3:
                    j = 3 * a + b
                    l = list(s)
                    l[z], l[j] = l[j], l[z]
                    t = tuple(l)
                    if t not in seen:
                        seen.add(t)
                        nxt.append(t)
        if not nxt:
            return len(seen), depth
        fr, depth = nxt, depth + 1
n3, depth3 = bfs_count_3x3()
assert n3 == math.factorial(9) // 2
print('3x3 BFS from the goal visits', n3, 'boards, hardest needs', depth3, 'moves; 4x4 would need about 10^13 (use A* or IDA* with a heuristic)')

# ---- edge asserts
assert sliding_puzzle([[1, 2, 3], [4, 5, 0]]) == 0
assert sliding_puzzle([[1, 2, 3], [4, 0, 5]]) == 1
assert sliding_puzzle([[0, 1, 2], [3, 4, 5]]) == table[(0, 1, 2, 3, 4, 5)] == 15
print('edge asserts passed')
```

**Output (my run):**
```
[[1, 2, 3], [4, 0, 5]] -> 1
[[1, 2, 3], [5, 4, 0]] -> -1
[[4, 1, 2], [5, 0, 3]] -> 5
[[1, 2, 3], [4, 5, 0]] -> 0
boards 720 | reachable 360 | unreachable 360 | hardest board needs 21 moves
boards per distance: [(0, 1), (1, 2), (2, 3), (3, 5), (4, 6), (5, 7), (6, 10), (7, 12), (8, 12), (9, 16), (10, 23), (11, 25), (12, 28), (13, 39), (14, 44), (15, 40), (16, 29), (17, 21), (18, 18), (19, 12), (20, 6), (21, 1)]
reachable  <=>  even number of inversions among tiles 1..5: holds for all 720 boards
example 2 has tiles read 1 2 3 5 4: one inversion (odd) -> -1
states: 2x3 720 reachable 360 | 3x3 362880 reachable 181440 | 4x4 20922789888000 reachable 10461394944000
3x3 BFS from the goal visits 181440 boards, hardest needs 31 moves; 4x4 would need about 10^13 (use A* or IDA* with a heuristic)
edge asserts passed
```

**Edge cases:**
- Already solved: 0 moves (checked before the loop, so no queue work).
- One move away: 1.
- Unsolvable (odd inversions): the search exhausts all 360 reachable boards and returns -1.
- Hardest solvable board: 21 moves. The code lists how many boards sit at each distance.
- Input as lists of lists: convert to a tuple, lists are not hashable and cannot go in a set.

**Follow-ups:**
- Print the moves? Store a parent pointer per state and walk it back from the goal.
- Test solvability without search? The inversion parity rule for odd width (this 2 x 3 board and the 3 x 3 puzzle); for even width the blank's row also matters.
- Bidirectional BFS? Meets in the middle and cuts nodes explored; on 720 states it is not needed, on larger ones it helps.

**Common mistakes:**
- Using a list as the state (unhashable) or mutating a shared list between neighbours (copy before swapping).
- Marking states seen when popped, which queues duplicates.
- Swapping the wrong pair: the blank swaps with a neighbour, never two tiles with each other.
- Forgetting the start-equals-goal case (answer 0), or returning from the loop before the goal check on the first board.

### Q33 ⭐⭐ 🔴 Alien dictionary (topological order from constraints). `words` is a list of 1 to 100 non-empty lowercase words (length <= 100) claimed to be sorted in an alien alphabet's lexicographic order (a proper prefix comes before the longer word). Return a string containing each distinct letter that appears in `words` exactly once, in an order under which `words` is sorted, or '' if no such order exists (a cycle among the constraints, or a longer word placed before its own prefix). Many alphabets can be valid: the checker accepts any string that contains each letter once and under which the list is sorted, and accepts '' only if no ordering of the letters works; the example shows one accepted answer. Explain how the first differing letters of adjacent words give edges, and why only adjacent pairs are needed. Example: words=['wrt', 'wrf', 'er', 'ett', 'rftt'] -> 'wertf'; words=['z', 'x', 'z'] -> ''; words=['abc', 'ab'] -> ''; words=['a', 'b', 'a'] -> ''; words=['ab'] -> 'ab'.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort on a graph built from constraints: letters are nodes, "this letter comes before that letter" is an edge.

**Say this first (1 line):** "Compare each adjacent pair of words, find the first position where they differ, and that gives one edge: the letter in the first word comes before the letter in the second. Then topologically sort the letters; a cycle, or a longer word before its own prefix, means there is no valid alphabet."

**Brute force:** Try every permutation of the distinct letters and test whether the word list is sorted under it. That is up to 26! orders, so it only works for at most 7 or 8 letters. It is the checker in the code: it decides when `''` is a correct answer.

**Optimal:**
- Nodes: every distinct letter in any word (including letters that get no constraint: they must still appear exactly once in the answer).
- For each adjacent pair `(a, b)`: scan for the first index where `a[i] != b[i]`. If found, add the edge `a[i] -> b[i]` (once per distinct pair; a repeated edge must not double-count the in-degree) and stop looking at this pair. If no difference is found, one word is a prefix of the other: fine if `a` is the shorter or they are equal, impossible if `len(a) > len(b)` (for example `abc` before `ab`): return `''`.
- Kahn's algorithm: queue of in-degree-0 letters, pop, output, decrease the successors. If the output has fewer letters than the alphabet, there is a cycle: return `''`.
- Why only adjacent pairs: the list is sorted, so for `i < j` the order of `words[i]` and `words[j]` follows from the chain `words[i] <= words[i+1] <= ... <= words[j]` by transitivity. Any constraint from a non-adjacent pair is implied by the adjacent ones. Using all pairs would add up to 4950 candidate pairs and the same answer. The code checks it: on all 22,620 small word lists plus 400 random ones, the all-pairs version is impossible exactly when the adjacent-only version is.
- Why only the first difference counts: after the first differing letters the rest of the words says nothing about the order.
- Many answers are valid when the constraints leave letters unordered. The code's validator accepts any string containing each letter once under which the list is sorted, and accepts `''` only when the exhaustive permutation search finds no order. The prompt's `'wertf'` is accepted and so is our output.

**Complexity:** Let L be the total length of all words (up to 100 * 100 = 10^4) and K the alphabet size (up to 26). Building edges: O(L) (each adjacent pair is scanned once, up to the shorter length). Kahn: O(K + number of edges), and the edges are at most min(99, K^2). Total O(L + K). Space O(K + edges).

**Dry run:** `['wrt','wrf','er','ett','rftt']`.
- wrt vs wrf: first difference at index 2, t vs f: edge t -> f.
- wrf vs er: index 0, w vs e: edge w -> e.
- er vs ett: index 1, r vs t: edge r -> t.
- ett vs rftt: index 0, e vs r: edge e -> r.
- Graph: w -> e -> r -> t -> f. In-degrees: only w is 0. Kahn outputs w, e, r, t, f: `'wertf'`.
- Example `['z','x','z']`: z -> x, x -> z: a cycle, nothing has in-degree 0, output empty, so `''`.

**Code:**
```python
import itertools
import random
from collections import deque

random.seed(33)

def alien_order(words):
    """Edges from the first differing letters of ADJACENT words, then Kahn's algorithm. '' if impossible."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:                       # one edge per distinct ordered pair
                    adj[x].add(y)
                    indeg[y] += 1
                break
        else:                                             # no differing letter: one word is a prefix of the other
            if len(a) > len(b):                           # longer word first is impossible
                return ''
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''   # fewer than all letters: a cycle

def sorted_under(words, order):
    rank = {c: i for i, c in enumerate(order)}
    key = lambda w: [rank[c] for c in w]                  # list comparison: a proper prefix is smaller
    return all(key(a) <= key(b) for a, b in zip(words, words[1:]))

def valid(words, got):
    """The checker the prompt states: each letter exactly once and the list sorted under it; '' only if NO ordering works."""
    letters = sorted({c for w in words for c in w})
    if got == '':
        return not any(sorted_under(words, p) for p in itertools.permutations(letters))
    return sorted(got) == letters and sorted_under(words, got)

def alien_brute(words):
    letters = sorted({c for w in words for c in w})
    for p in itertools.permutations(letters):
        if sorted_under(words, p):
            return ''.join(p)
    return ''

def alien_all_pairs(words):
    """Same algorithm but with constraints from EVERY pair i < j: shows adjacent pairs already imply all of them."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a, b = words[i], words[j]
            for x, y in zip(a, b):
                if x != y:
                    adj[x].add(y)
                    break
            else:
                if len(a) > len(b):
                    return ''
    indeg = {c: 0 for c in letters}
    for u in letters:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''

def alien_no_prefix_check(words):
    """Bug: ignore the 'longer word before its own prefix' case."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:
                    adj[x].add(y)
                    indeg[y] += 1
                break
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''

for w, shown in [(['wrt', 'wrf', 'er', 'ett', 'rftt'], 'wertf'), (['z', 'x', 'z'], ''), (['abc', 'ab'], ''), (['a', 'b', 'a'], ''), (['ab'], 'ab')]:
    got = alien_order(w)
    assert valid(w, got) and valid(w, shown), (w, got, shown)
    print(w, '->', repr(got), '| prompt shows', repr(shown), '| both accepted')

print("no prefix check on ['abc','ab'] ->", repr(alien_no_prefix_check(['abc', 'ab'])), '(wrongly accepted: no differing letter, so no edge)')

# ---- exhaustive: every list of 1..4 words over {a,b,c}, lengths 1..2 (12 possible words): our answer is accepted by the validator,
# '' appears exactly when no permutation works, and adjacent-pair edges agree with all-pair edges
words_all = [''.join(p) for L in (1, 2) for p in itertools.product('abc', repeat=L)]
cnt = empties = 0
for k in range(1, 5):
    for combo in itertools.product(words_all, repeat=k):
        w = list(combo)
        got = alien_order(w)
        assert valid(w, got), (w, got)
        assert (got == '') == (alien_brute(w) == ''), w
        assert (alien_all_pairs(w) == '') == (got == ''), w
        empties += got == ''
        cnt += 1
print('exhaustive on', cnt, 'word lists:', empties, 'impossible; all answers accepted by the validator, adjacent pairs == all pairs')

# ---- seeded random lists over 5 letters: sample from a hidden alphabet order so most are solvable, then corrupt some
for t in range(400):
    alpha = random.sample('abcde', 5)
    rank = {c: i for i, c in enumerate(alpha)}
    ws = [''.join(random.choice('abcde') for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 8))]
    ws.sort(key=lambda s: [rank[c] for c in s])
    if t % 3 == 0 and len(ws) > 1:
        i, j = random.sample(range(len(ws)), 2)
        ws[i], ws[j] = ws[j], ws[i]                      # may break sortedness
    got = alien_order(ws)
    assert valid(ws, got), (ws, got)
    assert (alien_all_pairs(ws) == '') == (got == '')
print('400 seeded random lists (5 letters): accepted by the validator; adjacent == all pairs')

# ---- letters with no constraint must still appear exactly once
r = alien_order(['x', 'y', 'q'])
assert sorted(alien_order(['ab', 'cd'])) == list('abcd') and sorted(r) == list('qxy') and valid(['x', 'y', 'q'], r)
print("unconstrained letters: ['ab','cd'] ->", alien_order(['ab', 'cd']))

# ---- max size: 100 words of length 100 over 26 letters in one hidden order; plus a 26-letter chain
alpha = random.sample('abcdefghijklmnopqrstuvwxyz', 26)
rank = {c: i for i, c in enumerate(alpha)}
ws = sorted((''.join(random.choice(alpha) for _ in range(100)) for _ in range(100)), key=lambda s: [rank[c] for c in s])
got = alien_order(ws)
assert got != '' and sorted(got) == sorted(set(''.join(ws))) and sorted_under(ws, got)
print('100 words of length 100: letters', len(got), 'ordering accepted')
chain = [alpha[i] for i in range(26)]
assert alien_order(chain) == ''.join(alpha) and alien_order(['a']) == 'a'
print('edge asserts passed')
```

**Output (my run):**
```
['wrt', 'wrf', 'er', 'ett', 'rftt'] -> 'wertf' | prompt shows 'wertf' | both accepted
['z', 'x', 'z'] -> '' | prompt shows '' | both accepted
['abc', 'ab'] -> '' | prompt shows '' | both accepted
['a', 'b', 'a'] -> '' | prompt shows '' | both accepted
['ab'] -> 'ab' | prompt shows 'ab' | both accepted
no prefix check on ['abc','ab'] -> 'abc' (wrongly accepted: no differing letter, so no edge)
exhaustive on 22620 word lists: 16140 impossible; all answers accepted by the validator, adjacent pairs == all pairs
400 seeded random lists (5 letters): accepted by the validator; adjacent == all pairs
unconstrained letters: ['ab','cd'] -> abdc
100 words of length 100: letters 26 ordering accepted
edge asserts passed
```

**Edge cases:**
- One word: the letters of the word, in any order that keeps each once; there are no constraints (the prompt shows `'ab'`, but `'ba'` is equally valid, and the validator accepts both).
- Prefix cases: `['ab','abc']` is fine (no edge); `['abc','ab']` is impossible. Missing this check is the most common bug: the code shows it returning `'abc'`.
- Identical adjacent words: no difference, lengths equal, no constraint.
- A cycle across non-adjacent words (`['a','b','a']`): transitive through adjacent edges, found as the cycle a -> b -> a.
- Letters that never get an edge still count: they must be in the output once. Compare the output's sorted letters with the alphabet.
- Deduplicate edges: two adjacent pairs giving the same letter pair must not add 2 to the in-degree and then decrement once.

**Follow-ups:**
- Return all valid orders or count them? That is counting topological orders, exponential in general; for ties, Kahn with a lexicographic-smallest heap gives a unique canonical answer.
- Is the order unique? Only if the Kahn queue never holds two letters at once (a Hamiltonian path in the constraint DAG). The code's `['ab','cd']` example has several.
- DFS version? Same edges, reverse postorder with a three-colour cycle check (Q31 in this part).

**Common mistakes:**
- Adding edges for every differing position instead of only the first.
- Omitting the prefix check.
- Counting a duplicate edge twice in the in-degree.
- Building the graph only from letters that appear in an edge, so unconstrained letters vanish from the answer.
- Comparing with the example string and expecting `'wertf'`: other valid answers exist when constraints do not pin the order.

### Q34 ⭐⭐ 🔴 Cheapest flights with at most k stops. `n` cities 0..n-1 (1 <= n <= 100), `flights` a list of directed [u, v, price] (price 1 <= price <= 10^4, up to 5000 flights) and integers `src`, `dst`, `k` with 0 <= k < n. Return the lowest total price of a route from `src` to `dst` using at most k intermediate cities (so at most k + 1 flights), or -1 if none. Use Bellman-Ford for k + 1 rounds, each round relaxing from a copy of the previous round's distances, and explain why using the same array in-place can allow too many flights per round and why plain Dijkstra with a visited set can give a wrong answer here. Example: n=4, flights=[[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], src=0, dst=3, k=1 -> 700; n=3, flights=[[0, 1, 100], [1, 2, 100], [0, 2, 500]], src=0, dst=2, k=0 -> 500; n=3, flights=[[0, 1, 100], [1, 2, 100], [0, 2, 500]], src=0, dst=2, k=1 -> 200; n=2, flights=[], src=0, dst=1, k=0 -> -1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Layered shortest path. The flight count is part of the state, so I run Bellman-Ford for exactly k + 1 rounds. Round r holds the best price using at most r flights.

**Say this first (1 line):** "Prices are positive but the stop limit makes plain Dijkstra unsafe, so I do k + 1 rounds of Bellman-Ford, each round reading last round's distances from a copy, which caps every route at k + 1 flights."

**Brute force:** Walk every route of at most k + 1 flights from `src` and keep the cheapest one that ends at `dst`. With out-degree up to 5000 this is exponential in k, so it only runs on tiny inputs. It is the cross-check.

**Optimal:**
- `d[v]` after round r = cheapest price to reach `v` with at most r flights. Start: `d[src] = 0`, rest infinite.
- One round: `nd = d[:]`, then for each flight `(u, v, w)` try `d[u] + w < nd[v]`. The read side is the old array `d`, the write side is the new array `nd`.
- After k + 1 rounds, `d[dst]` is the answer (or -1 if infinite).
- Why the copy matters: if I read and write the same array, a relaxation early in the round can feed a later one in the same round. Route 0 -> 1 -> 2 then uses two flights in round 1. With k = 0 that lets a two-flight route through, so the answer is too cheap. It can also depend on the order of the flight list, which is a sign of a bug.
- Why Dijkstra with a visited set breaks: it finalises a city at its cheapest price, but the cheapest route may use many flights. That city may be finalised through a route that is already out of flights, and the pricier route with fewer flights (the only legal one) is then thrown away. In the code: 0 -> 1 -> 2 costs 2 with 2 flights, 0 -> 2 costs 5 with 1 flight, k = 1. City 2 is finalised at price 2 with no flight left to reach 3, the direct 5 is blocked, and the visited-set version returns -1 when the true answer is 6.
- The fix for Dijkstra is to make the state `(city, flights used)`. Then nothing is thrown away, but it is heavier than Bellman-Ford here.

**Complexity:** Time O(k * E): k + 1 rounds, each scans all E flights (at most about 100 * 5000 = 5 * 10^5 relaxations). Space O(V) for two arrays. The state-Dijkstra is O((V * k + E * k) log) in the worst case.

**Dry run:** `n=3, flights=[[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1` (two rounds).
- Start `d = [0, inf, inf]`.
- Round 1 reads `[0, inf, inf]`: `0 -> 1` gives 100, `0 -> 2` gives 500, `1 -> 2` reads inf and does nothing. `d = [0, 100, 500]`.
- Round 2 reads `[0, 100, 500]`: `1 -> 2` gives 200 < 500. `d = [0, 100, 200]`.
- Answer 200. With k = 0 only round 1 runs and the answer is 500.

**Code:**
```python
import heapq
import itertools
import random

random.seed(34)
INF = float('inf')

def flights_brute(n, flights, src, dst, k):
    """Try every walk of at most k + 1 flights (exponential, tiny inputs only)."""
    best = INF
    def go(u, cost, left):
        nonlocal best
        if u == dst:
            best = min(best, cost)
        if left == 0:
            return
        for a, b, w in flights:
            if a == u:
                go(b, cost + w, left - 1)
    go(src, 0, k + 1)
    return -1 if best == INF else best

def flights_bf(n, flights, src, dst, k):
    """Bellman-Ford, k + 1 rounds, each round reads the PREVIOUS round's distances (a copy)."""
    d = [INF] * n
    d[src] = 0
    for _ in range(k + 1):
        nd = d[:]                       # copy: round r only extends round r-1 routes by one flight
        for u, v, w in flights:
            if d[u] + w < nd[v]:
                nd[v] = d[u] + w
        d = nd
    return -1 if d[dst] == INF else d[dst]

def flights_inplace(n, flights, src, dst, k):
    """WRONG: relaxes into the same array, so one round can chain several flights."""
    d = [INF] * n
    d[src] = 0
    for _ in range(k + 1):
        for u, v, w in flights:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return -1 if d[dst] == INF else d[dst]

def flights_dijkstra_visited(n, flights, src, dst, k):
    """WRONG: Dijkstra by price with a visited set per city (and a flight counter on the heap)."""
    adj = [[] for _ in range(n)]
    for u, v, w in flights:
        adj[u].append((v, w))
    h = [(0, src, 0)]
    seen = set()
    while h:
        c, u, f = heapq.heappop(h)
        if u == dst:
            return c
        if u in seen:
            continue
        seen.add(u)
        if f == k + 1:
            continue
        for v, w in adj[u]:
            heapq.heappush(h, (c + w, v, f + 1))
    return -1

def flights_dijkstra_state(n, flights, src, dst, k):
    """Correct Dijkstra: the state is (city, flights used), so no pruning by city alone."""
    adj = [[] for _ in range(n)]
    for u, v, w in flights:
        adj[u].append((v, w))
    h = [(0, src, 0)]
    best = {}
    while h:
        c, u, f = heapq.heappop(h)
        if u == dst:
            return c
        if best.get((u, f), INF) < c or f == k + 1:
            continue
        for v, w in adj[u]:
            if c + w < best.get((v, f + 1), INF):
                best[(v, f + 1)] = c + w
                heapq.heappush(h, (c + w, v, f + 1))
    return -1

# ---- examples from the prompt
assert flights_bf(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
F3 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
assert flights_bf(3, F3, 0, 2, 0) == 500
assert flights_bf(3, F3, 0, 2, 1) == 200
assert flights_bf(2, [], 0, 1, 0) == -1
print('examples ok')

# ---- why in-place is wrong: with k = 0 (one flight) it still chains 0 -> 1 -> 2 in ONE round
print('k=0 in-place:', flights_inplace(3, F3, 0, 2, 0), ' copy:', flights_bf(3, F3, 0, 2, 0), ' (true answer 500)')
# the order of the edge list decides it, so the bug is also input-order dependent
print('k=0 in-place, reversed list:', flights_inplace(3, F3[::-1], 0, 2, 0))

# ---- why Dijkstra with a visited set is wrong: city 2 is finalised cheaply but with too many flights
FD = [[0, 1, 1], [1, 2, 1], [0, 2, 5], [2, 3, 1]]
print('k=1 true:', flights_bf(4, FD, 0, 3, 1), ' dijkstra+visited:', flights_dijkstra_visited(4, FD, 0, 3, 1),
      ' dijkstra on (city, flights):', flights_dijkstra_state(4, FD, 0, 3, 1))

# ---- seeded cross-check on random small graphs (repeats and cycles allowed)
def rand_case():
    n = random.randint(1, 6)
    fl = [[random.randrange(n), random.randrange(n), random.randint(1, 9)] for _ in range(random.randint(0, 12))]
    src, dst = random.randrange(n), random.randrange(n)
    return n, fl, src, dst, random.randint(0, n - 1)

bad_inplace = bad_dij = 0
N = 2000
for _ in range(N):
    n, fl, s, t, k = rand_case()
    exp = flights_brute(n, fl, s, t, k)
    assert flights_bf(n, fl, s, t, k) == exp, (n, fl, s, t, k)
    assert flights_dijkstra_state(n, fl, s, t, k) == exp
    bad_inplace += flights_inplace(n, fl, s, t, k) != exp
print('cross-check on', N, 'seeded cases: copy-based Bellman-Ford and state Dijkstra match brute force')
# the visited-set bug is rarer, so hunt it on a denser, skewed-price family (Bellman-Ford is the reference)
M = 20000
for _ in range(M):
    n = random.randint(3, 6)
    fl = [[random.randrange(n), random.randrange(n), random.choice([1, 1, 2, 3, 10])] for _ in range(random.randint(4, 12))]
    s, t, k = random.randrange(n), random.randrange(n), random.randint(0, 2)
    bad_dij += flights_dijkstra_visited(n, fl, s, t, k) != flights_bf(n, fl, s, t, k)
print('in-place wrong on', bad_inplace, 'of', N, '| visited-set Dijkstra wrong on', bad_dij, 'of', M, '(skewed family)')
assert bad_inplace > 0 and bad_dij > 0

# ---- edge cases
assert flights_bf(1, [], 0, 0, 0) == 0                          # src == dst costs nothing
assert flights_bf(3, [[0, 1, 5]], 0, 2, 2) == -1                # unreachable
assert flights_bf(2, [[0, 1, 9], [0, 1, 4]], 0, 1, 0) == 4      # parallel flights, take the cheaper
assert flights_bf(3, [[0, 1, 1], [1, 0, 1], [1, 2, 1]], 0, 2, 5) == 2   # cycles never help (positive prices)
# max size: n = 100, 5000 flights, k = 99 -> 100 rounds * 5000 edges = 5*10^5 relaxations
n = 100
big = [[random.randrange(n), random.randrange(n), random.randint(1, 10 ** 4)] for _ in range(5000)]
print('max-size run:', flights_bf(n, big, 0, n - 1, n - 1))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
k=0 in-place: 200  copy: 500  (true answer 500)
k=0 in-place, reversed list: 500
k=1 true: 6  dijkstra+visited: -1  dijkstra on (city, flights): 6
cross-check on 2000 seeded cases: copy-based Bellman-Ford and state Dijkstra match brute force
in-place wrong on 29 of 2000 | visited-set Dijkstra wrong on 13 of 20000 (skewed family)
max-size run: 1601
edge cases ok
```

**Edge cases:**
- `src == dst`: price 0 (d[src] starts at 0).
- `dst` unreachable, or reachable only with more than k + 1 flights: -1.
- k = 0: only direct flights count.
- Parallel flights between the same pair: the relaxation keeps the cheaper one.
- Cycles in the flight map: harmless, prices are positive and rounds are capped.
- Stopping the rounds early when nothing changed is a safe optimisation, but only if you compare with the previous round, not the same array.

**Follow-ups:**
- *Could you do better than O(k * E)?* Dijkstra on `(city, flights used)` with a best-price table per state; it also prunes well when k is small. Worst case it is about the same order.
- *Why not a BFS by number of flights?* BFS orders by flights, not by price, so it would need to keep price per layer anyway, which is the Bellman-Ford rounds.
- *What if prices could be negative?* The k + 1 round bound still holds (negative cycles cannot loop forever), but Dijkstra-style methods are out.

**Common mistakes:**
- Relaxing into the same array in each round (allows more than k + 1 flights).
- Running k rounds instead of k + 1: k stops means k + 1 flights.
- Pruning by city alone in Dijkstra (visited set) and ignoring the flight count.
- Forgetting that unreachable is infinity, not 0, and printing infinity instead of -1.

### Q35 ⭐ 🟡 Floyd-Warshall: the city with the fewest neighbours within a distance threshold. `n` cities 0..n-1 (2 <= n <= 100), `edges` a list of undirected [u, v, w] with 1 <= w <= 10^4 (up to 4000; repeats possible) and an integer `threshold`. For each city count the other cities whose shortest-path distance is at most `threshold`. Return the city with the smallest count, and the largest index if several tie. Use the O(n^3) all-pairs dynamic programme (loop k outermost) and explain why k must be the outer loop and when you would run Dijkstra from every node instead. Example: n=4, edges=[[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], threshold=4 -> 3; n=3, edges=[], threshold=5 -> 2; n=5, edges=[[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], threshold=2 -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** All-pairs shortest paths by dynamic programming over "allowed intermediate cities" (Floyd-Warshall), then a count per row.

**Say this first (1 line):** "n is at most 100, so I run Floyd-Warshall in O(n^3), count the cities within the threshold per row, and take the smallest count with the largest index on ties; k must be the outermost loop."

**Brute force:** Run Dijkstra with a heap from every city and count. It is O(n * (E + n) log n). That is not slow, it is simply the alternative: it is the cross-check in the code and the better choice on a big sparse graph.

**Optimal:**
- `f[i][j]` starts as 0 on the diagonal, the cheapest direct edge (repeats possible, so take the min) in both directions, infinity otherwise.
- For `k` from 0 to n-1, for every pair `(i, j)`: `f[i][j] = min(f[i][j], f[i][k] + f[k][j])`.
- Invariant: after finishing round `k`, `f[i][j]` is the shortest path from i to j that uses only cities `0..k` as intermediates. Round k adds "may now go through k".
- Why k must be the outer loop: the invariant needs round k to be complete for ALL pairs before round k + 1 starts. With k inner, a pair `(i, j)` considers its middle cities one after another while `f[i][k]` and `f[k][j]` are not final yet and the pair is never revisited. The code shows path 0-1-3-2 where inner k gives distance infinity for (0, 2).
- Count: for each city `i`, the number of `j != i` with `f[i][j] <= threshold`. Pick the minimum count, break ties with the larger index (use `<=` when scanning upward).
- Floyd-Warshall versus Dijkstra from every node: n = 100 and dense graphs favour Floyd-Warshall (3 simple loops, handles negative edges). For large sparse graphs, n Dijkstras at O(n (E + n) log n) beat O(n^3). Floyd-Warshall also needs O(n^2) memory.

**Complexity:** Time O(n^3) = about 10^6 steps for n = 100. Space O(n^2). Dijkstra from every node: O(n (E + n) log n) time, O(n + E) space plus the answer.

**Dry run:** `n=3, edges=[[0,1,1],[1,2,1]], threshold=2`.
- Start: `f[0][1] = f[1][0] = 1`, `f[1][2] = f[2][1] = 1`, `f[0][2] = inf`.
- k = 0: nothing new (0 only connects to 1). k = 1: `f[0][2] = f[0][1] + f[1][2] = 2`, and symmetric.
- Counts within 2: city 0 sees 1 and 2, city 1 sees 0 and 2, city 2 sees 0 and 1. All 2, so the tie goes to the largest index: 2.

**Code:**
```python
import heapq
import random

random.seed(35)
INF = float('inf')

def city_dijkstra(n, edges, threshold):
    """Brute force / alternative: Dijkstra from every node with a heap (O(n (E + n) log n))."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    best = None
    for s in range(n):
        d = [INF] * n
        d[s] = 0
        h = [(0, s)]
        while h:
            x, u = heapq.heappop(h)
            if x > d[u]:
                continue
            for v, w in adj[u]:
                if x + w < d[v]:
                    d[v] = x + w
                    heapq.heappush(h, (x + w, v))
        c = sum(1 for j in range(n) if j != s and d[j] <= threshold)
        if best is None or c <= best[0]:          # <= so the larger index wins a tie
            best = (c, s)
    return best[1]

def all_pairs(n, edges):
    """Floyd-Warshall. k is the OUTER loop: after round k, f[i][j] is the best path using only
    intermediate cities from {0..k}."""
    f = [[INF] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 0
    for u, v, w in edges:                         # repeats possible: keep the cheapest
        f[u][v] = min(f[u][v], w)
        f[v][u] = min(f[v][u], w)
    for k in range(n):
        fk = f[k]
        for i in range(n):
            fik = f[i][k]
            if fik == INF:
                continue
            fi = f[i]
            for j in range(n):
                if fik + fk[j] < fi[j]:
                    fi[j] = fik + fk[j]
    return f

def city_floyd(n, edges, threshold):
    f = all_pairs(n, edges)
    best = None
    for i in range(n):
        c = sum(1 for j in range(n) if j != i and f[i][j] <= threshold)
        if best is None or c <= best[0]:
            best = (c, i)
    return best[1]

def all_pairs_wrong_order(n, edges):
    """WRONG: k as the INNER loop."""
    f = [[INF] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 0
    for u, v, w in edges:
        f[u][v] = min(f[u][v], w)
        f[v][u] = min(f[v][u], w)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if f[i][k] + f[k][j] < f[i][j]:
                    f[i][j] = f[i][k] + f[k][j]
    return f

# ---- examples from the prompt
assert city_floyd(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3
assert city_floyd(3, [], 5) == 2
assert city_floyd(5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2) == 0
print('examples ok')

# ---- why k is outer: path 0-1-3-2. Inner k never revisits a pair after a later k improves its parts
P = [[0, 1, 1], [1, 3, 1], [2, 3, 1]]
good = all_pairs(4, P)
bad = all_pairs_wrong_order(4, P)
print('dist(0, 2) true:', good[0][2], '| with k inner:', bad[0][2])
assert good[0][2] == 3 and bad[0][2] != 3
wrong_cases = 0
for _ in range(300):
    n = random.randint(3, 6)
    E = [[random.randrange(n), random.randrange(n), random.randint(1, 5)] for _ in range(random.randint(2, 8))]
    wrong_cases += all_pairs(n, E) != all_pairs_wrong_order(n, E)
print('k-inner differs from k-outer on', wrong_cases, 'of 300 seeded small graphs')
assert wrong_cases > 0

# ---- seeded cross-check: Floyd-Warshall vs Dijkstra-from-every-node (ties and repeated edges included)
N = 1500
for _ in range(N):
    n = random.randint(2, 8)
    E = [[random.randrange(n), random.randrange(n), random.randint(1, 6)] for _ in range(random.randint(0, 14))]
    E = [e for e in E if e[0] != e[1]]
    th = random.randint(1, 10)
    assert city_floyd(n, E, th) == city_dijkstra(n, E, th), (n, E, th)
print('cross-check on', N, 'seeded cases: Floyd-Warshall == Dijkstra from every node')

# ---- edge cases
assert city_floyd(2, [], 1) == 1                         # nobody reaches anybody, everyone has 0 -> largest index
assert city_floyd(2, [[0, 1, 5]], 4) == 1                # edge longer than the threshold: still a 0-0 tie
assert city_floyd(2, [[0, 1, 5], [0, 1, 2]], 2) == 1     # repeated edge: cheaper one counts, both have 1 -> index 1
assert city_floyd(3, [[0, 1, 1], [1, 2, 1]], 2) == 2     # all three see 2 others: tie, largest index
f = all_pairs(3, [[0, 1, 1], [1, 2, 1]])
print('path 0-1-2 counts:', [sum(1 for j in range(3) if j != i and f[i][j] <= 2) for i in range(3)])
# max size: n = 100, 4000 edges, 10^6 inner steps
n = 100
big = [[random.randrange(n), random.randrange(n), random.randint(1, 10 ** 4)] for _ in range(4000)]
big = [e for e in big if e[0] != e[1]]
print('max-size city:', city_floyd(n, big, 3000), city_dijkstra(n, big, 3000))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
dist(0, 2) true: 3 | with k inner: inf
k-inner differs from k-outer on 22 of 300 seeded small graphs
cross-check on 1500 seeded cases: Floyd-Warshall == Dijkstra from every node
path 0-1-2 counts: [2, 2, 2]
max-size city: 99 99
edge cases ok
```

**Edge cases:**
- No edges: everyone has 0 neighbours, answer n - 1.
- All ties: the largest index, not the first.
- Repeated edges: keep the minimum weight, do not overwrite with the last one.
- An edge longer than the threshold may still be part of no useful path, but the shortest path through other cities may be shorter than the edge itself.
- Use infinity as a float and test `f[i][k] == INF` before adding, or the sum silently stays infinite (it is fine in Python, but in C++ it would overflow).
- Do not count the city itself.

**Follow-ups:**
- *Detect a negative cycle?* After the loops, any `f[i][i] < 0`.
- *Recover the path?* Keep a `next[i][j]` matrix updated together with `f`.
- *Directed edges?* Drop the symmetric assignments; the algorithm is unchanged.

**Common mistakes:**
- k in the inner loop (wrong answers on some graphs).
- Keeping the first or last duplicate edge instead of the minimum.
- Strict `<` on the tie scan, which returns the smallest index.
- Counting the city itself, or counting distance `< threshold` instead of `<=`.

### Q36 ⭐ 🟡 Eulerian path and circuit: existence only. `n` nodes 0..n-1 (1 <= n <= 20) and `edges` a list of undirected [u, v] (0 <= len <= 40; repeats and self loops allowed, a self loop adds 2 to its node's degree). A trail uses every edge exactly once. Return 'circuit' if some trail uses every edge exactly once and ends where it starts, 'path' if one exists but none closes, and 'none' if no such trail exists (a graph with no edges counts as 'circuit'; isolated nodes do not matter). Decide it from degrees (the number of odd-degree nodes) and the connectivity of the nodes that have edges, without constructing the trail; say why the Hierholzer construction is O(E) but is not needed here. Example: n=4, edges=[[0, 1], [1, 2], [2, 0], [2, 3], [3, 2]] -> 'circuit'; n=4, edges=[[0, 1], [1, 2], [2, 3]] -> 'path'; n=4, edges=[[0, 1], [0, 2], [0, 3]] -> 'none'; n=5, edges=[[0, 1], [2, 3]] -> 'none'; n=3, edges=[] -> 'circuit'.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Euler's degree rule plus a connectivity check. A property of the degrees, so no search is needed.

**Say this first (1 line):** "Ignore isolated nodes. If the nodes with edges are not all connected, it is none. Otherwise count odd-degree nodes: zero is a circuit, two is a path, anything else is none."

**Brute force:** Try every trail: from each start node, extend by any unused edge in either direction until all edges are used, then see whether it ended at the start. That is exponential in the number of edges (E <= 40 here, so it is only usable on tiny graphs). It is the cross-check, run over every small multigraph.

**Optimal:**
- Degrees: each edge adds 1 to both ends. A self loop adds 2 to its node (1 + 1 in the code), so it never changes parity.
- Every time a trail passes through a node it uses one edge in and one edge out, so that node uses edges in pairs. Only the first and the last node of an open trail can have an odd degree.
- Zero odd nodes (and connected): a circuit exists. Exactly two odd nodes (and connected): a path exists, and it must start at one odd node and end at the other. One odd node is impossible (the degree sum is even), so the odd count is 0, 2, 4, 6...; four or more means no trail.
- Connectivity: one trail cannot jump between components, so all edges must lie in one component. Check it with union-find or a BFS over the nodes that have at least one edge. A node with no edges is ignored.
- No edges: nothing to traverse, the prompt calls that a circuit.
- Hierholzer's algorithm builds the actual trail in O(E): walk until stuck, splice in sub-circuits. It is not needed to decide existence, which is O(V + E) from degrees and one connectivity pass. Construction, directed graphs and the full theory belong to Part 14.

**Complexity:** Time O(V + E) (union-find with path halving, near-linear). Space O(V). The brute force is exponential.

**Dry run:** `n=4, edges=[[0,1],[1,2],[2,3]]`.
- Degrees: 0 -> 1, 1 -> 2, 2 -> 2, 3 -> 1.
- Union-find merges 0-1, 1-2, 2-3: one component.
- Odd nodes: 0 and 3, so exactly two: `'path'`, starting at 0 and ending at 3.
- For `[[0,1],[0,2],[0,3]]` the degrees are 3, 1, 1, 1: four odd nodes, `'none'`.

**Code:**
```python
import itertools
import random

random.seed(36)

def euler_kind(n, edges):
    """Degrees plus connectivity of the nodes that have edges. Never builds the trail."""
    if not edges:
        return 'circuit'
    deg = [0] * n
    parent = list(range(n))

    def find(x):                                   # iterative find with path halving
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        deg[u] += 1
        deg[v] += 1                                # a self loop adds 2 in total (1 + 1)
        parent[find(u)] = find(v)
    if len({find(u) for u, v in edges}) > 1:       # edges live in more than one component
        return 'none'
    odd = sum(d % 2 for d in deg)
    return 'circuit' if odd == 0 else 'path' if odd == 2 else 'none'

def euler_brute(n, edges):
    """Try every trail: from every start node, use each edge once in either direction."""
    m = len(edges)
    if m == 0:
        return 'circuit'
    found = set()

    def go(u, used, start, count):
        if count == m:
            found.add('circuit' if u == start else 'path')
            return
        for i, (a, b) in enumerate(edges):
            if not used >> i & 1:
                if a == u:
                    go(b, used | 1 << i, start, count + 1)
                if b == u and a != b:
                    go(a, used | 1 << i, start, count + 1)

    for s in range(n):
        go(s, 0, s, 0)
    return 'circuit' if 'circuit' in found else 'path' if 'path' in found else 'none'

# ---- examples from the prompt
assert euler_kind(4, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 2]]) == 'circuit'
assert euler_kind(4, [[0, 1], [1, 2], [2, 3]]) == 'path'
assert euler_kind(4, [[0, 1], [0, 2], [0, 3]]) == 'none'
assert euler_kind(5, [[0, 1], [2, 3]]) == 'none'
assert euler_kind(3, []) == 'circuit'
print('examples ok')

# ---- exhaustive: EVERY multiset of at most 5 edges (self loops and repeats included) on 4 nodes
types = [(u, v) for u in range(4) for v in range(u, 4)]       # 10 edge types
total = 0
tally = {'circuit': 0, 'path': 0, 'none': 0}
for m in range(0, 6):
    for combo in itertools.combinations_with_replacement(types, m):
        edges = [list(e) for e in combo]
        a, b = euler_kind(4, edges), euler_brute(4, edges)
        assert a == b, (edges, a, b)
        tally[a] += 1
        total += 1
print('exhaustive check:', total, 'edge multisets on 4 nodes, all agree with the trail search', tally)

# ---- seeded random check on 5-6 nodes with up to 7 edges
N = 600
for _ in range(N):
    n = random.randint(5, 6)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 7))]
    assert euler_kind(n, edges) == euler_brute(n, edges), (n, edges)
print('random check on', N, 'seeded graphs ok')

# ---- edge cases
assert euler_kind(1, [[0, 0]]) == 'circuit'                   # one self loop: degree 2, closes on itself
assert euler_kind(2, [[0, 1], [0, 1]]) == 'circuit'           # two parallel edges
assert euler_kind(2, [[0, 0], [1, 1]]) == 'none'              # two components, each with an edge
assert euler_kind(5, [[0, 1], [1, 2], [2, 0]]) == 'circuit'   # isolated nodes 3 and 4 do not matter
assert euler_kind(2, [[0, 1]]) == 'path'                      # exactly two odd nodes
assert euler_kind(20, [[i, (i + 1) % 20] for i in range(20)] * 2) == 'circuit'   # max n, 40 edges
print('edge cases ok')
```

**Output (my run):**
```
examples ok
exhaustive check: 3003 edge multisets on 4 nodes, all agree with the trail search {'circuit': 226, 'path': 1362, 'none': 1415}
random check on 600 seeded graphs ok
edge cases ok
```

**Edge cases:**
- No edges: `'circuit'` (by the prompt), whatever n is.
- A single self loop: degree 2, a circuit.
- Parallel edges are separate edges: two parallel edges give degrees 2 and 2, a circuit.
- Two components that both have edges: `'none'`, even if every degree is even.
- Isolated nodes must not make a connected graph look disconnected.
- Counting a self loop as 1 instead of 2 gives wrong parity.

**Follow-ups:**
- *Directed graph?* Circuit needs in-degree equal to out-degree everywhere (and connectivity); a path needs one node with out - in = 1 and one with in - out = 1.
- *How would you print the trail?* Hierholzer, O(E); see Part 14.
- *Is it the same as a Hamiltonian path?* No. Euler visits every edge once and is easy; Hamiltonian visits every node once and is NP-hard.

**Common mistakes:**
- Forgetting the connectivity check (the degrees alone say 'circuit' for two separate triangles).
- Including isolated nodes in the connectivity check.
- Counting self loops as degree 1.
- Answering 'path' for one or three odd nodes (impossible), or for any number of odd nodes above two.

### Q37 ⭐ 🟡 Prim's algorithm on a dense graph: connect points at minimum cost. `points` is a list of n distinct integer points [x, y] (1 <= n <= 1000, |coordinate| <= 10^6); the cost between two points is their Manhattan distance |x1 - x2| + |y1 - y2|, and every pair may be connected. Return the minimum total cost of edges that connect all points. Use Prim in O(n^2) with a plain distance array (no heap, no edge list of about 500000 edges) and say when a heap-based Prim or Kruskal is better; state why the answer is a minimum spanning tree weight and therefore unique even if the trees are not. Example: points=[[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]] -> 20; points=[[3, 12], [-2, 5], [-4, 1]] -> 18; points=[[0, 0]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Minimum spanning tree on a complete (dense) graph. Prim with a plain distance array, no heap and no explicit edges.

**Say this first (1 line):** "With n up to 1000 every pair is an edge, about 500000 of them, so I use array-based Prim in O(n^2): keep the cheapest link from the tree to each outside point, take the closest, update the rest."

**Brute force:** Build all n(n-1)/2 edges, sort them and run Kruskal with union-find: O(n^2 log n) time and O(n^2) memory (about 500000 tuples). It works but the memory and the sort are wasteful. The code uses it as a reference, and also compares against all spanning trees (Pruefer sequences) for n <= 6.

**Optimal:**
- `dist[v]` = cheapest edge from the current tree to `v`. Start with `dist[0] = 0`, the rest infinite.
- Repeat n times: pick the unused point `u` with the smallest `dist` (a linear scan), add `dist[u]` to the total, mark it used. Then for each unused `v`, `dist[v] = min(dist[v], manhattan(u, v))`.
- Why it is right: the cut property. For the tree built so far, the cheapest edge leaving it is in some minimum spanning tree, so adding it never hurts.
- Why a heap is not used: the heap version is O((E) log V) with E = n^2/2 edges, which is worse than the O(n^2) scan. Distances are computed on the fly, so no edge list is stored.
- When something else is better: a sparse graph (E much less than V^2). Then heap-based Prim at O(E log V) or Kruskal at O(E log E) wins. Kruskal is also nicer when edges arrive as a list or when you want to stop at k components. Kruskal details are in Part 14.
- Unique weight, not unique tree: every minimum spanning tree has the same total weight by definition (the minimum), so the answer is well-defined. Trees can differ when edge weights tie. Three points with all pairwise distances 2 have three different minimum spanning trees, all of weight 4 (shown in the code by trying every spanning tree).

**Complexity:** Time O(n^2): n rounds, each a linear scan plus a linear update. About 10^6 distance computations for n = 1000. Space O(n) for `dist` and `used`.

**Dry run:** `points=[[3,12],[-2,5],[-4,1]]`.
- Distances: P0-P1 = 5 + 7 = 12, P0-P2 = 7 + 11 = 18, P1-P2 = 2 + 4 = 6.
- Start: `dist = [0, inf, inf]`. Take P0 (cost 0): `dist = [_, 12, 18]`.
- Take P1 (12, the smallest): total 12. Update P2: `min(18, 6) = 6`.
- Take P2: total 18. Answer 18 (edges P0-P1 and P1-P2).

**Code:**
```python
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
```

**Output (my run):**
```
examples ok
tie example: MST weight 4 reached by 3 different trees; Prim returns 4
Prim == Kruskal on 600 seeded random point sets (heavy ties on the small grids)
Prim == minimum over ALL spanning trees on 120 tiny sets (n <= 6)
n = 1000: Prim weight 52092136 | pairs a Kruskal would have to sort: 499500
edge cases ok
```

**Edge cases:**
- One point: 0 (the loop adds `dist[0] = 0` once).
- Two points: their distance.
- Collinear points: the sum of consecutive gaps.
- Many equal distances (a small grid): the weight is still unique although the tree is not.
- Largest coordinates: `|x| <= 10^6` gives sums around 4 * 10^6 per edge, and Python integers do not overflow.
- The start point does not matter; the code checks that rotating the list gives the same weight.

**Follow-ups:**
- *Euclidean distance instead?* Same algorithm; compare squared distances while choosing but keep real distances for the total.
- *Faster than O(n^2)?* For Manhattan distance, a plane-sweep with a BIT builds only O(n) candidate edges, then Kruskal: O(n log n). Euclidean uses a Delaunay triangulation.
- *Connect all but k components?* Kruskal, stop after n - k merges.

**Common mistakes:**
- Building all 500000 edges and a heap for dense input.
- Using `dist[u]` of a point that is already in the tree when updating (always check `used`).
- Adding the full edge list to the total instead of the picked `dist[u]`.
- Believing the MST is unique; only its weight is.

### Q38 ⭐ 🟡 Iterative DFS: mark on pop versus mark on push. `edges` is a list of undirected [u, v] on nodes 0..n-1 (1 <= n <= 10^5, no self loops or repeats), adjacency lists in input order as in the BFS/DFS-orders question, and `start` a node. Return `[A, B]`. A: stack = [start]; pop u; skip it if already visited; mark and record u; push its neighbours in reverse list order. This is exactly the recursive preorder. B: mark start as seen when pushed; pop u and record it; for each neighbour v in list order, if v is not yet seen, mark it and push it. Both visit the same set of nodes but B can give a different order that is not a true DFS preorder. Explain why, and which variant keeps the stack smaller. Example: n=4, edges=[[0, 1], [0, 2], [1, 3], [2, 3]], start=0 -> [[0, 1, 3, 2], [0, 2, 3, 1]]; n=4, edges=[[0, 1], [1, 2], [2, 3]], start=0 -> [[0, 1, 2, 3], [0, 1, 2, 3]]; n=3, edges=[[0, 1], [0, 2], [1, 2]], start=0 -> [[0, 1, 2], [0, 2, 1]].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Iterative DFS with an explicit stack. The only question is when a node is marked: when it is popped or when it is pushed.

**Say this first (1 line):** "Marking on pop gives the exact recursive preorder; marking on push gives a smaller stack but a different order, because a node is claimed by the first node that sees it, not by the DFS path that reaches it first."

**Brute force:** The recursive DFS, which defines the right preorder (neighbours in list order). It is the reference in the code, but it dies on a long path at the default recursion limit of 1000.

**Optimal:**
- A, mark on pop: `stack = [start]`. Pop `u`. If already visited, skip it. Else mark it, record it, push its neighbours in reverse list order. The first neighbour goes on top, so it is explored first. This is exactly the recursive preorder.
- A can hold the same node many times (every edge pushes a copy). That is fine because the stale copies are skipped on pop.
- B, mark on push: mark `start` when pushed. Pop `u`, record it, and for each neighbour in list order that is not seen, mark it and push it.
- B visits the same set of nodes (every reachable node is pushed exactly once and so popped exactly once), but not necessarily the same order.
- Why the order differs: when `u` is expanded B marks ALL its unseen neighbours at once. A true DFS would first go deep through one neighbour, and that branch might reach another neighbour `w` as its own child. B has already marked `w` as a child of `u`, so the branch cannot take it. Also B pops the last pushed neighbour first, which already reverses the list order.
- Example in the code: edges 0-1, 0-2, 0-3, 3-1. True preorder `[0, 1, 3, 2]`. B gives `[0, 3, 2, 1]`.
- Stack size: B pushes each node at most once, so the stack never holds more than n entries. A pushes one entry per edge entry in the adjacency list, so it can reach about 2E entries. On a complete graph of 300 nodes, A peaks at 44850 and B at 299. On all 10810 small cases B never had a larger peak than A.
- B is fine when you only need to visit everything (reachability, counting components). Use A when the order itself matters (preorder, tree-like timestamps).

**Complexity:** Time O(V + E) for both. Space: A O(E) in the worst case (stack entries), B O(V).

**Dry run:** `n=3, edges=[[0,1],[0,2],[1,2]], start=0`. Adjacency: 0 -> [1, 2], 1 -> [0, 2], 2 -> [0, 1].
- A: stack `[0]`. Pop 0, record it, push 2 then 1: `[2, 1]`. Pop 1, record, push neighbours reversed (2, 0): `[2, 2, 0]`. Pop 0: stale. Pop 2: record, push 1, 0: stale entries remain. Order `[0, 1, 2]`.
- B: mark 0. Pop 0, record. Neighbours 1, 2 unseen: mark and push `[1, 2]`. Pop 2, record: its neighbours are already seen. Pop 1, record. Order `[0, 2, 1]`.
- Same set, different order, and B never pushed a duplicate.

**Code:**
```python
import itertools
import random

random.seed(38)

def build_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:                     # input order, both directions
        adj[u].append(v)
        adj[v].append(u)
    return adj

def dfs_mark_on_pop(adj, start):
    """A: push everything, skip stale entries on pop. Exactly the recursive preorder."""
    seen, stack, order, peak = set(), [start], [], 1
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        for v in reversed(adj[u]):         # reversed, so the FIRST neighbour is popped first
            stack.append(v)
        peak = max(peak, len(stack))
    return order, peak

def dfs_mark_on_push(adj, start):
    """B: mark when pushed. Each node enters the stack at most once, but the order is not preorder."""
    seen, stack, order, peak = {start}, [start], [], 1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
        peak = max(peak, len(stack))
    return order, peak

def dfs_recursive(adj, start):
    """Brute force / reference preorder (fine on small inputs only)."""
    seen, order = set(), []
    def go(u):
        seen.add(u)
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                go(v)
    go(start)
    return order

def solve(n, edges, start):
    adj = build_adj(n, edges)
    return [dfs_mark_on_pop(adj, start)[0], dfs_mark_on_push(adj, start)[0]]

# ---- examples from the prompt
assert solve(4, [[0, 1], [0, 2], [1, 3], [2, 3]], 0) == [[0, 1, 3, 2], [0, 2, 3, 1]]
assert solve(4, [[0, 1], [1, 2], [2, 3]], 0) == [[0, 1, 2, 3], [0, 1, 2, 3]]
assert solve(3, [[0, 1], [0, 2], [1, 2]], 0) == [[0, 1, 2], [0, 2, 1]]
print('examples ok')

# ---- why B differs: expanding 0 marks 1, 2, 3 as seen at once. In a real DFS the walk 0 -> 1 -> 3 reaches 3 as
#      a child of 1; B pops 3 first and 1 is already marked, so 1 can never be explored from inside 3's branch.
E = [[0, 1], [0, 2], [0, 3], [3, 1]]
adj = build_adj(4, E)
print('A (true preorder):', dfs_mark_on_pop(adj, 0)[0], ' B:', dfs_mark_on_push(adj, 0)[0], ' recursive:', dfs_recursive(adj, 0))

# ---- exhaustive over EVERY simple graph on <= 5 nodes (input order and reversed order), every start
total = diff = b_bigger = 0
for n in range(1, 6):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for m in range(len(pairs) + 1):
        for es in itertools.combinations(pairs, m):
            for edges in (list(es), list(reversed(es))):
                adj = build_adj(n, edges)
                for s in range(n):
                    oa, pa = dfs_mark_on_pop(adj, s)
                    ob, pb = dfs_mark_on_push(adj, s)
                    assert oa == dfs_recursive(adj, s)            # A is exactly the recursive preorder
                    assert sorted(oa) == sorted(ob)               # B visits the same set
                    total += 1
                    diff += oa != ob
                    b_bigger += pb > pa
print('exhaustive:', total, 'cases; A == recursive preorder always; same node set always;')
print('  B order differs from A on', diff, 'cases; B peak stack larger than A on', b_bigger)
assert b_bigger == 0 and diff > 0

# ---- seeded random cross-check on larger graphs
N = 400
dif = 0
for _ in range(N):
    n = random.randint(2, 12)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    edges = [list(e) for e in random.sample(pairs, random.randint(0, len(pairs)))]
    s = random.randrange(n)
    adj = build_adj(n, edges)
    a, b = solve(n, edges, s)
    assert a == dfs_recursive(adj, s) and sorted(a) == sorted(b)
    dif += a != b
print('random check on', N, 'seeded graphs ok; B differs from preorder on', dif)

# ---- stack size: complete graph. A stacks every neighbour entry (about n^2 / 2), B at most n
n = 300
K = [[i, j] for i in range(n) for j in range(i + 1, n)]
adj = build_adj(n, K)
print('K300 peak stack: A =', dfs_mark_on_pop(adj, 0)[1], ' B =', dfs_mark_on_push(adj, 0)[1], ' (n =', n, ')')
assert dfs_mark_on_push(adj, 0)[1] <= n and dfs_mark_on_pop(adj, 0)[1] > n

# ---- deep path: both iterative versions are fine, the recursive one hits the recursion limit
n = 100000
path = [[i, i + 1] for i in range(n - 1)]
adj = build_adj(n, path)
assert dfs_mark_on_pop(adj, 0)[0] == list(range(n)) and dfs_mark_on_push(adj, 0)[0] == list(range(n))
try:
    dfs_recursive(adj, 0)
except RecursionError:
    print('recursive DFS on a 100000-node path: RecursionError (default limit 1000)')

# ---- edge cases
assert solve(1, [], 0) == [[0], [0]]
assert solve(5, [[0, 1]], 3) == [[3], [3]]            # start in its own component: only that node
assert solve(2, [[0, 1]], 1) == [[1, 0], [1, 0]]
print('edge cases ok')
```

**Output (my run):**
```
examples ok
A (true preorder): [0, 1, 3, 2]  B: [0, 3, 2, 1]  recursive: [0, 1, 3, 2]
exhaustive: 10810 cases; A == recursive preorder always; same node set always;
  B order differs from A on 8876 cases; B peak stack larger than A on 0
random check on 400 seeded graphs ok; B differs from preorder on 275
K300 peak stack: A = 44850  B = 299  (n = 300 )
recursive DFS on a 100000-node path: RecursionError (default limit 1000)
edge cases ok
```

**Edge cases:**
- Single node: both give `[start]`.
- Start in a small component: only that component appears.
- Path graph: both orders equal.
- Dense graph: A's stack holds many stale entries; B's is bounded by n.
- A long path (10^5 nodes): both iterative versions work; the recursive one raises `RecursionError` at the default limit of 1000.
- Neighbour order: pushing in list order (not reversed) in A reverses the visit order, which is no longer the recursive preorder.

**Follow-ups:**
- *Can you get true preorder with mark on push?* Not with a plain stack of nodes. Push `(node, neighbour iterator)` pairs instead and advance the iterator, which is the iterative form of the recursion and keeps O(V) space.
- *Does the choice matter for connected components or cycle detection in undirected graphs?* Reachability does not care about order. Cycle detection needs the parent, so mark on push must remember who pushed.
- *Why not use `list.pop(0)`?* That would be a queue (BFS) and O(n) per pop; DFS pops from the end, which is O(1).

**Common mistakes:**
- Marking on push but claiming the result is the recursive preorder.
- Pushing neighbours in list order and expecting the first neighbour to be visited first.
- Forgetting the "already visited" check on pop in version A (revisits nodes and may loop forever).
- Using recursion on a 10^5-node path.

### Q39 ⭐ 🟡 Most stones removed (union-find on rows and columns). `stones` is a list of n distinct integer points [row, col] (1 <= n <= 1000, 0 <= row, col <= 10^4). A stone can be removed if another stone that has not been removed shares its row or its column. Return the maximum number of stones that can be removed. Show that the answer is n minus the number of connected groups when stones sharing a row or column are linked, with rows and columns as union-find nodes. Example: stones=[[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]] -> 5; stones=[[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]] -> 3; stones=[[0, 0]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Union-find with rows and columns as the nodes. A stone is an edge joining its row and its column.

**Say this first (1 line):** "Stones sharing a row or column form groups, and in each group I can remove all but one stone, so the answer is n minus the number of groups; I count groups with union-find on row and column nodes."

**Brute force:** Try every removal order: from the set of stones still standing, remove any stone that has a partner in its row or column and recurse, memoised on the bitmask of stones left. It is exponential, so it runs only for n <= 10. It is the cross-check.

**Optimal:**
- Make a node for every row and every column. Tag them (`('r', r)` and `('c', c)`) so row 3 and column 3 are different nodes. A stone at `(r, c)` unions its row node and its column node.
- Two stones that share a row (or column) end up in the same set, because both are joined to that same row node. So the sets are exactly the groups of linked stones.
- Count the distinct roots of the stones' row nodes. That is the number of groups with at least one stone.
- Answer = n - groups.
- Why a group of s stones loses exactly s - 1: remove stones in the reverse of a DFS/BFS discovery order, farthest leaf first. The stone being removed always still has its DFS parent (which shares a row or column with it) in place, until only the root is left. So s - 1 can go. The last stone has no neighbour left once its group is down to one stone, and a stone in one group never helps another group (they share no row or column). So the maximum is exactly s - 1 per group.
- Why not union every pair of stones: that is O(n^2) pairs. Joining each stone to its own row and column is one union per stone.
- `find` is iterative (path halving), so deep chains in the structure cannot hit the recursion limit.

**Complexity:** Time O(n * alpha(n)) with path compression, about linear, plus O(n) to collect roots. Space O(n) for the parent map (at most 2n nodes, so the 10001 x 10001 coordinate range never costs memory).

**Dry run:** `stones=[[0,0],[0,2],[1,1],[2,0],[2,2]]`.
- Stone (0,0): union r0 with c0. Stone (0,2): union r0 with c2. Stone (1,1): union r1 with c1. Stone (2,0): union r2 with c0 (c0 is already with r0, so r2 joins). Stone (2,2): union r2 with c2 (already in the same set).
- Groups: `{r0, c0, c2, r2}` and `{r1, c1}`: two groups.
- Answer 5 - 2 = 3.

**Code:**
```python
import random
from functools import lru_cache

random.seed(39)

def remove_stones(stones):
    """Union-find where a stone (r, c) unions the ROW node r with the COLUMN node c.
    Answer = n - (number of groups that contain at least one stone)."""
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:                      # iterative, path halving
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r, c in stones:
        parent[find(('r', r))] = find(('c', c))    # tag the kind so row 3 and column 3 are different nodes
    groups = {find(('r', r)) for r, c in stones}
    return len(stones) - len(groups)

def remove_stones_brute(stones):
    """Try every removal order with memoisation over the set of stones still standing (n <= 12)."""
    n = len(stones)

    @lru_cache(maxsize=None)
    def best(left):
        out = 0
        for i in range(n):
            if left >> i & 1:
                ri, ci = stones[i]
                if any(j != i and left >> j & 1 and (stones[j][0] == ri or stones[j][1] == ci) for j in range(n)):
                    out = max(out, 1 + best(left & ~(1 << i)))
        return out

    return best((1 << n) - 1)

def groups_dfs(stones):
    """Second reference: connected groups by an explicit stack over stones (same row or column)."""
    n = len(stones)
    seen = [False] * n
    cnt = 0
    for s in range(n):
        if not seen[s]:
            cnt += 1
            seen[s] = True
            st = [s]
            while st:
                u = st.pop()
                for v in range(n):
                    if not seen[v] and (stones[v][0] == stones[u][0] or stones[v][1] == stones[u][1]):
                        seen[v] = True
                        st.append(v)
    return cnt

# ---- examples from the prompt
assert remove_stones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]) == 5
assert remove_stones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]) == 3
assert remove_stones([[0, 0]]) == 0
print('examples ok')

# ---- the claim: answer == n - groups (a group of size s loses s - 1 stones, the last one has no partner)
S = [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]
print('second example: n =', len(S), 'groups =', groups_dfs(S), '-> removable', len(S) - groups_dfs(S))

# ---- seeded cross-check against the exhaustive removal-order search (and the DFS group count)
N = 500
for _ in range(N):
    n = random.randint(1, 10)
    side = random.randint(2, 5)
    cells = [(r, c) for r in range(side) for c in range(side)]
    n = min(n, len(cells))
    st = [list(p) for p in random.sample(cells, n)]
    a = remove_stones(st)
    assert a == remove_stones_brute(tuple(map(tuple, st))), st
    assert a == len(st) - groups_dfs(st)
print('cross-check on', N, 'seeded small stone sets: union-find == exhaustive search == n - groups')

# ---- why one union per stone (not per pair of stones) is enough: a full row of stones is ONE group
row = [[5, c] for c in range(8)]
assert remove_stones(row) == 7
# a diagonal has no shared row or column: nothing can be removed
assert remove_stones([[i, i] for i in range(8)]) == 0

# ---- edge cases: same index as row and as column must stay separate nodes
assert remove_stones([[3, 7], [7, 3]]) == 0
assert remove_stones([[0, 0], [0, 1]]) == 1
assert remove_stones([[10000, 10000], [10000, 0], [0, 10000]]) == 2       # extreme coordinates
# max size: 1000 distinct stones in the 10001 x 10001 range
big = random.sample([(r, c) for r in range(0, 10001, 7) for c in range(0, 10001, 11)], 1000)
big = [list(p) for p in big]
print('n = 1000 random stones: removable', remove_stones(big), '| groups', 1000 - remove_stones(big))
# one staircase group of 1000 stones in a chain: remove 999
chain = [[i // 2 + (i % 2), i // 2] for i in range(1000)]
print('staircase chain of 1000 stones: removable', remove_stones(chain))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
second example: n = 5 groups = 2 -> removable 3
cross-check on 500 seeded small stone sets: union-find == exhaustive search == n - groups
n = 1000 random stones: removable 692 | groups 308
staircase chain of 1000 stones: removable 999
edge cases ok
```

**Edge cases:**
- One stone: 0 (it is its own group).
- All stones in one row: n - 1.
- A diagonal: no two stones share a line, answer 0.
- A stone at `(3, 7)` and one at `(7, 3)` share nothing: row 7 and column 7 are different nodes (the tag matters).
- Extreme coordinates (10^4): a dict-based union-find is fine; an array of 10^4 rows and columns is also fine.
- A chain through many rows and columns is one group.

**Follow-ups:**
- *Do it with DFS instead?* Build row-to-stones and column-to-stones maps, then DFS over stones; same count of groups, O(n) time.
- *Why does removal order not matter for the count?* Any group can always be reduced to one stone, and groups never merge when stones are removed.
- *What if stones can be added too?* Union-find handles additions, which is the online connectivity pattern of the number-of-islands-II question later in this part.

**Common mistakes:**
- Using the raw row and column numbers as node ids so that row 3 and column 3 collide.
- Counting groups as the number of roots over all row and column nodes (rows or columns without stones would be counted if you pre-create them).
- Union-ing all pairs of stones (O(n^2)).
- Returning the number of groups instead of n minus the number of groups.

### Q40 ⭐ 🟡 Shortest paths in a DAG with negative weights. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` a list of directed [u, v, w] with -100 <= w <= 100 forming a directed acyclic graph (guaranteed, up to 2*10^5 edges, repeats allowed) and `src`. Return the list of shortest distances from `src` (None for unreachable nodes) in O(V + E): process nodes in topological order and relax their out-edges. Explain why this beats Bellman-Ford and why Dijkstra would be wrong with negative edges. Example: n=5, edges=[[0, 1, 2], [0, 2, 6], [1, 2, -3], [2, 3, 1], [1, 3, 4]], src=0 -> [0, 2, -1, 0, null]; n=3, edges=[[1, 2, -5]], src=0 -> [0, null, null]; n=1, edges=[], src=0 -> [0].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Shortest path on a DAG: topological order, then relax each node's out-edges once, in that order.

**Say this first (1 line):** "In a DAG every edge goes forward in topological order, so when I reach a node its distance is final; one pass in that order in O(V + E) handles negative weights, which Dijkstra cannot."

**Brute force:** Bellman-Ford: up to V - 1 passes over all edges, O(V * E). With V = 10^5 and E = 2 * 10^5 that is about 2 * 10^10 steps in the worst case. It is the cross-check on small inputs.

**Optimal:**
- Topological order with Kahn's algorithm over the whole graph (a queue of in-degree-zero nodes). It is iterative, which matters at 10^5 nodes.
- `dist[src] = 0`, everything else infinite. For each `u` in the topological order: skip it if `dist[u]` is infinite (not reachable from `src`), otherwise for each edge `(u, v, w)` set `dist[v] = min(dist[v], dist[u] + w)`.
- Why one pass is enough: every path to `v` comes through predecessors that are earlier in the order. When `v` is processed, all its in-edges were already relaxed from nodes whose distance is final. This is an induction on the order. No negative-cycle issue exists in a DAG.
- Why skip unreachable nodes: an infinite distance plus a negative weight must not turn into a finite number. In Python `inf + w` stays `inf`, but the explicit skip also saves work and keeps the reasoning clean.
- Why it beats Bellman-Ford: each edge is relaxed once, not up to V - 1 times, so O(V + E) instead of O(V * E).
- Why Dijkstra is wrong with negative edges: it finalises a node when popped, assuming nothing later can be shorter. A negative edge from a later node breaks that. In the code, edges 0->1 (4), 0->2 (5), 2->1 (-3): Dijkstra pops and finalises node 1 at 4, but the true distance is 5 - 3 = 2 via node 2. Output `[0, 4, 5]` against the correct `[0, 2, 5]`.
- Unreachable nodes are returned as `None`, as the prompt asks.

**Complexity:** Time O(V + E): Kahn's algorithm is O(V + E), the relaxation pass is O(V + E). Space O(V + E) for the adjacency lists, the in-degrees and the order.

**Dry run:** `n=5, edges=[[0,1,2],[0,2,6],[1,2,-3],[2,3,1],[1,3,4]], src=0`.
- Kahn order: in-degrees are 0, 1, 2, 2, 0, so the queue starts `[0, 4]` and the order is 0, 4, 1, 2, 3.
- `dist = [0, inf, inf, inf, inf]`. Process 0: `dist[1] = 2`, `dist[2] = 6`.
- Process 4: infinite, skipped. Process 1: `dist[2] = 2 - 3 = -1`, `dist[3] = 2 + 4 = 6`.
- Process 2: `dist[3] = min(6, -1 + 1) = 0`. Process 3: no out-edges.
- Result `[0, 2, -1, 0, None]`.

**Code:**
```python
import heapq
import random
from collections import deque

random.seed(40)
INF = float('inf')

def dag_shortest(n, edges, src):
    """Kahn topological order over the WHOLE graph, then relax out-edges in that order. O(V + E)."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, w in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    assert len(order) == n                      # the prompt guarantees a DAG
    dist = [INF] * n
    dist[src] = 0
    for u in order:
        if dist[u] == INF:                      # not reachable from src: its edges must not be relaxed
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return [None if x == INF else x for x in dist]

def bellman_ford(n, edges, src):
    """Brute force / reference: up to n - 1 passes over all edges, O(V * E)."""
    dist = [INF] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return [None if x == INF else x for x in dist]

def dijkstra_finalise(n, edges, src):
    """Finalise-on-first-pop Dijkstra (wrong with negative edges)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    h = [(0, src)]
    done = set()
    while h:
        d, u = heapq.heappop(h)
        if u in done:
            continue
        done.add(u)
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
    return [None if x == INF else x for x in dist]

# ---- examples from the prompt
E1 = [[0, 1, 2], [0, 2, 6], [1, 2, -3], [2, 3, 1], [1, 3, 4]]
assert dag_shortest(5, E1, 0) == [0, 2, -1, 0, None]
assert dag_shortest(3, [[1, 2, -5]], 0) == [0, None, None]
assert dag_shortest(1, [], 0) == [0]
print('examples ok')

# ---- Dijkstra fails: node 1 is popped and finalised at 4, then 0 -> 2 -> 1 (5 - 3 = 2) is found too late
E2 = [[0, 1, 4], [0, 2, 5], [2, 1, -3]]
print('DAG answer  :', dag_shortest(3, E2, 0))
print('Dijkstra    :', dijkstra_finalise(3, E2, 0))
assert dag_shortest(3, E2, 0) == [0, 2, 5] and dijkstra_finalise(3, E2, 0) == [0, 4, 5]

def random_dag(n, m, lo, hi):
    perm = list(range(n))
    random.shuffle(perm)                        # hidden topological order, labels are shuffled
    es = []
    for _ in range(m):
        if n < 2:
            break
        a, b = sorted(random.sample(range(n), 2))
        es.append([perm[a], perm[b], random.randint(lo, hi)])
    return es

# ---- seeded cross-check against Bellman-Ford (repeats, unreachable nodes, negative weights)
N = 1500
dij_wrong = 0
for _ in range(N):
    n = random.randint(1, 9)
    es = random_dag(n, random.randint(0, 16), -5, 5)
    s = random.randrange(n)
    a = dag_shortest(n, es, s)
    assert a == bellman_ford(n, es, s), (n, es, s)
    dij_wrong += dijkstra_finalise(n, es, s) != a
print('cross-check on', N, 'seeded DAGs: topological relaxation == Bellman-Ford;',
      'finalise-on-pop Dijkstra wrong on', dij_wrong)
assert dij_wrong > 0

# ---- edge cases
assert dag_shortest(4, [[2, 3, -1], [1, 2, -1]], 1) == [None, 0, -1, -2]      # source in the middle, earlier nodes unreachable
assert dag_shortest(3, [[0, 1, 5], [0, 1, -2], [0, 1, 7]], 0) == [0, -2, None]  # repeats: smallest wins
assert dag_shortest(2, [[0, 1, -100]], 1) == [None, 0]                          # edge leaving an unreachable node
# max size: 10^5 nodes, 2 * 10^5 edges, weights -100..100 (iterative, no recursion anywhere)
n, m = 100000, 200000
perm = list(range(n))
random.shuffle(perm)
big = [[perm[i], perm[i + 1], random.randint(-100, 100)] for i in range(n - 1)]      # a spine so everything is reachable
for _ in range(m - (n - 1)):
    a, b = sorted(random.sample(range(n), 2))
    big.append([perm[a], perm[b], random.randint(-100, 100)])
assert len(big) == m
d = dag_shortest(n, big, perm[0])
reach = sum(x is not None for x in d)
print('max size: reachable', reach, 'of', n, '| min distance', min(x for x in d if x is not None))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
DAG answer  : [0, 2, 5]
Dijkstra    : [0, 4, 5]
cross-check on 1500 seeded DAGs: topological relaxation == Bellman-Ford; finalise-on-pop Dijkstra wrong on 49
max size: reachable 100000 of 100000 | min distance -172858
edge cases ok
```

**Edge cases:**
- Source with no out-edges: only the source is finite.
- A node before `src` in topological order: it stays `None`; its edges are never relaxed.
- Repeated edges between the same pair: the smallest weight wins automatically.
- An edge leaving an unreachable node, even with weight -100: it must not create a distance.
- One node: `[0]`.
- 10^5 nodes and 2 * 10^5 edges: all iterative; a distance is at most 10^7 in magnitude (10^5 edges of weight 100) and Python integers do not overflow.

**Follow-ups:**
- *Longest path in a DAG?* Negate the weights (or take max in the same pass). It is NP-hard in general graphs but linear here.
- *If the graph might have a cycle?* Kahn's order would be shorter than n; fall back to Bellman-Ford (which also detects negative cycles).
- *Could you use DFS post-order instead of Kahn?* Yes, reverse post-order is also topological, but it must be iterative at this size.

**Common mistakes:**
- Relaxing from nodes whose distance is still infinite.
- Running the pass over only the nodes reachable by BFS without a topological order.
- Using Dijkstra "because there is a heap" and getting wrong answers with negative edges.
- A recursive DFS topological sort on 10^5 nodes (RecursionError at the default limit of 1000).

### Q41 ⭐ 🟡 Eventual safe nodes. `graph` is a directed graph in adjacency-list form on nodes 0..n-1 (1 <= n <= 10^4): `graph[u]` lists the nodes u points to (up to 4*10^4 entries in total; repeats and self loops allowed). A node is terminal if it has no outgoing edge and safe if every path starting there reaches a terminal node (so a node that can reach a cycle is unsafe). Return the ascending list of safe nodes. Solve it by running Kahn's algorithm on the reversed graph and explain why that works. Example: graph=[[1, 2], [2, 3], [5], [0], [5], [], []] -> [2, 4, 5, 6]; graph=[[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []] -> [4]; graph=[[0]] -> []; graph=[[]] -> [0].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological peeling (Kahn's algorithm) on the reversed graph. Safe nodes are the ones that can be peeled off starting from the terminal nodes.

**Say this first (1 line):** "A node is safe when all its targets are safe, so I start from the terminal nodes, walk the edges backwards, and mark a node safe when its out-degree counter hits zero; nodes that never reach zero can reach a cycle."

**Brute force:** Compute reachability between all pairs (transitive closure, O(n^3)), find the nodes that lie on a cycle (they reach themselves), and call a node unsafe if it can reach one of them. It is the cross-check. The code also has a recursive three-colour DFS, which is correct but needs depth up to n.

**Optimal:**
- `out[u]` = number of entries in `graph[u]`. Build `rev[v]` = the nodes that point to `v`.
- Queue = all nodes with `out == 0` (terminal nodes are safe).
- Pop `u` (now known safe). For every predecessor `p` in `rev[u]`, decrement `out[p]`. If it hits 0, every target of `p` is safe, so `p` is safe: push it.
- Answer = the popped nodes, sorted ascending.
- Why reversing is what makes it Kahn: in ordinary Kahn we remove nodes with in-degree 0 and lower the in-degree of their targets. Here the "dependency" is the other way: `p` depends on all its targets being safe, so the counter is the out-degree and we release `p` through the reversed edges.
- Why nodes that reach a cycle are never released: a node on a cycle always has at least one target (the next cycle node) that never becomes safe, so its counter never reaches 0, and everything that can reach it is stuck as well. Conversely, if every path from `p` ends at a terminal node, the graph below `p` is acyclic, and then peeling reaches it by induction on the longest path.
- Repeated edges: `out[u]` counts every entry, and `rev` has a matching entry for each, so each repeat decrements once. They cancel out correctly.
- Self loops: `graph[u]` contains `u`, so `out[u] >= 1` and `u` can only be released by itself being safe. It never happens, so `u` is unsafe.

**Complexity:** Time O(V + E): every edge is looked at once while building `rev` and once while decrementing. Space O(V + E) for `rev`, the counters and the queue.

**Dry run:** `graph=[[1,2],[2,3],[5],[0],[5],[],[]]`.
- Out-degrees: `[2, 2, 1, 1, 1, 0, 0]`. Terminals 5 and 6 go into the queue.
- Pop 5: its predecessors are 2 and 4. `out[2] = 0` (safe, push), `out[4] = 0` (safe, push).
- Pop 6: no predecessors. Pop 2: predecessors 0 and 1: `out[0] = 1`, `out[1] = 1`. Pop 4: no predecessors.
- Queue empty. Safe nodes sorted: `[2, 4, 5, 6]`. Nodes 0, 1, 3 form or reach the cycle 0 -> 1 -> 3 -> 0.

**Code:**
```python
import itertools
import random
from collections import deque

random.seed(41)

def safe_nodes(graph):
    """Kahn's algorithm on the REVERSED graph. A node is safe when all its out-neighbours are safe."""
    n = len(graph)
    rev = [[] for _ in range(n)]
    out = [len(graph[u]) for u in range(n)]          # counts repeats, as the reversed lists will too
    for u in range(n):
        for v in graph[u]:
            rev[v].append(u)
    q = deque(i for i in range(n) if out[i] == 0)    # terminal nodes are safe
    safe = []
    while q:
        u = q.popleft()
        safe.append(u)
        for p in rev[u]:                             # p points to u, and u is now known safe
            out[p] -= 1
            if out[p] == 0:                          # all of p's targets are safe, so p is safe
                q.append(p)
    return sorted(safe)

def safe_brute(graph):
    """Reference: transitive closure. A node is unsafe iff it can reach a node that lies on a cycle."""
    n = len(graph)
    reach = [[False] * n for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    on_cycle = [i for i in range(n) if reach[i][i]]
    return [u for u in range(n) if u not in on_cycle and not any(reach[u][c] for c in on_cycle)]

def safe_recursive(graph):
    """Three-colour DFS (0 new, 1 in progress, 2 safe) written recursively, to show the recursion limit."""
    n = len(graph)
    color = [0] * n
    def ok(u):
        if color[u]:
            return color[u] == 2
        color[u] = 1
        for v in graph[u]:
            if not ok(v):
                return False
        color[u] = 2
        return True
    return [u for u in range(n) if ok(u)]

# ---- examples from the prompt
assert safe_nodes([[1, 2], [2, 3], [5], [0], [5], [], []]) == [2, 4, 5, 6]
assert safe_nodes([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]) == [4]
assert safe_nodes([[0]]) == []
assert safe_nodes([[]]) == [0]
print('examples ok')

# ---- exhaustive: every adjacency-list graph with lists of length <= 2 (repeats and self loops allowed)
def all_lists(n, maxlen):
    opts = [list(t) for L in range(maxlen + 1) for t in itertools.product(range(n), repeat=L)]
    return itertools.product(opts, repeat=n)

count = 0
for n, maxlen in ((1, 3), (2, 3), (3, 2), (4, 2)):
    for g in all_lists(n, maxlen):
        g = [list(x) for x in g]
        assert safe_nodes(g) == safe_brute(g), g
        count += 1
print('exhaustive check:', count, 'graphs on 1-4 nodes (repeats and self loops included), all agree')

# ---- seeded random check on bigger graphs, also against the colour DFS
N = 500
for _ in range(N):
    n = random.randint(1, 12)
    g = [[random.randrange(n) for _ in range(random.choice([0, 0, 1, 2, 3]))] for _ in range(n)]
    a = safe_nodes(g)
    assert a == safe_brute(g) == safe_recursive(g), g
print('random check on', N, 'seeded graphs: Kahn on reversed graph == closure == colour DFS')

# ---- edge cases
assert safe_nodes([[1], [1]]) == []                    # a node leading into a self loop is unsafe
assert safe_nodes([[1, 1], [2], []]) == [0, 1, 2]      # repeated edges: the counter counts both, both get decremented
assert safe_nodes([[1], [0], [2, 3], []]) == [3]       # cycle {0,1}; node 2 reaches a terminal and a self loop at 2
assert safe_nodes([[], [], []]) == [0, 1, 2]
# max size: n = 10^4, a chain of 10^4 nodes (deep) plus extra edges to reach 4 * 10^4 entries
n = 10000
g = [[i + 1] for i in range(n - 1)] + [[]]
for _ in range(4 * 10 ** 4 - (n - 1)):
    u = random.randrange(n - 1)
    g[u].append(random.randrange(u + 1, n))            # forward edges only: acyclic, so everything is safe
assert safe_nodes(g) == list(range(n))
try:
    safe_recursive(g)
except RecursionError:
    print('recursive colour DFS on the 10^4-node chain: RecursionError; Kahn on the reversed graph is fine')
g[n - 1] = [n - 1]                                    # one self loop at the end: everything that reaches it is unsafe
assert safe_nodes(g) == []
print('edge cases ok')
```

**Output (my run):**
```
examples ok
exhaustive check: 196907 graphs on 1-4 nodes (repeats and self loops included), all agree
random check on 500 seeded graphs: Kahn on reversed graph == closure == colour DFS
recursive colour DFS on the 10^4-node chain: RecursionError; Kahn on the reversed graph is fine
edge cases ok
```

**Edge cases:**
- A single node with a self loop: no safe nodes.
- A single node with no edges: it is terminal, so safe.
- Repeated edges: counts stay consistent because both the counter and `rev` see every copy.
- A node that points into a cycle but is not on it: unsafe.
- A long chain of 10^4 nodes: Kahn is iterative; the recursive colour DFS raises `RecursionError` at the default limit of 1000.
- Output must be ascending: the queue order is not, so sort.

**Follow-ups:**
- *How would you do it with DFS?* Three colours: unvisited, in progress, safe. Meeting an in-progress node means a cycle; everything on that path is unsafe. It must be written with an explicit stack at this size.
- *How is this related to cycle detection?* A graph has no cycle exactly when every node is safe.
- *What is the time if you reverse nothing and scan for the next safe node?* O(V * E) in the worst case; the reversed adjacency is what gives linear time.

**Common mistakes:**
- Running ordinary Kahn on the forward graph (it finds nodes not reachable from a cycle, the wrong set).
- Using `set(graph[u])` for the counter but a list for `rev`, so repeated edges are counted differently.
- Forgetting to sort the result.
- Treating a self loop as harmless.

### Q42 ⭐ 🟡 Why Dijkstra fails with a negative edge. `edges` are directed [u, v, w] on nodes 0..n-1 (1 <= n <= 8, -10 <= w <= 10) with no negative cycle reachable from `src`. Run the finalise-on-first-pop version of Dijkstra: dist[src] = 0, heap of (distance, node) with (0, src); pop (d, u); skip it if u is already finalised; finalise u; for each edge (u, v, w) in input order, if v is NOT finalised and d + w < dist[v], set dist[v] = d + w and push (d + w, v). Return `[dijkstra_dist, true_dist]` with None for unreachable nodes, where true_dist comes from Bellman-Ford. Give a three-node graph where the two differ and explain the exact step at which Dijkstra's reasoning (a finalised distance cannot be improved) breaks; mention that the stale-check variant, which does re-expand nodes, is correct on these graphs but has no good running-time guarantee. Example: n=3, edges=[[0, 1, 4], [0, 2, 5], [2, 1, -3]], src=0 -> [[0, 4, 5], [0, 2, 5]]; n=3, edges=[[0, 1, 1], [1, 2, 2]], src=0 -> [[0, 1, 3], [0, 1, 3]]; n=4, edges=[[0, 1, 2], [0, 2, 3], [2, 1, -2], [1, 3, 1]], src=0 -> [[0, 2, 3, 3], [0, 1, 3, 2]].
**Asked at:** Dijkstra and lazy-deletion write-ups (a PracHub guide on Dijkstra stale heap entries and negative edges, Codeforces lazy-deletion tutorials, a python-dev heapq thread; search snippets only, not opened; docs.python.org was unreachable) | Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened)

**Pattern:** Why a greedy shortest-path argument needs non-negative edges. Finalise-on-first-pop Dijkstra against Bellman-Ford as the truth.

**Say this first (1 line):** "Dijkstra finalises a node when it is popped because any other route would add non-negative weight to something at least as long; one negative edge breaks that, and a finalised node can still be improved."

**Brute force:** Bellman-Ford: n - 1 passes over all edges, O(V * E), correct with negative edges as long as no negative cycle is reachable. It supplies `true_dist`, and it is also what the code compares against.

**Optimal:** This question is about understanding the failure, so here is the argument and the two versions.
- Finalise-on-first-pop Dijkstra (as written in the prompt): pop `(d, u)`, skip if finalised, finalise it, relax only unfinalised neighbours.
- The invariant it relies on: when `u` is popped with the smallest key in the heap, every other node outside the finalised set has a tentative distance at least `d`. Any path to `u` that goes through another unfinalised node `x` costs at least `dist[x]` plus the rest of the path. If all remaining edges are non-negative, the rest adds nothing, so the path cannot beat `d`. That is the "cannot be improved" step.
- With a negative edge, the rest of the path can lower the cost. The exact step that breaks: the moment `u` is finalised while another unfinalised node `x` with a larger tentative distance still has a negative edge leading to `u` (or to something that leads to `u`).
- Three-node example: edges 0->1 (4), 0->2 (5), 2->1 (-3). Pops: finalise 0 at 0, finalise 1 at 4, finalise 2 at 5. Then the edge 2->1 offers 5 - 3 = 2 < 4, but node 1 is finalised and the relaxation is skipped. The code prints exactly this trace. Result `[0, 4, 5]` instead of `[0, 2, 5]`.
- The stale-check variant (skip a heap entry only if `d > dist[u]`, no finalised set) re-expands a node when a shorter distance arrives. On all graphs without a reachable negative cycle it ends with correct distances (tested below), because it behaves like a label-correcting algorithm. But it loses the guarantee: a node can be expanded many times. A blow-up family in the code (outside the n <= 8 bound, to show the shape) goes from 4 expansions on 3 nodes to 12286 on 25 nodes, roughly doubling every two nodes, so it is exponential. Bellman-Ford's O(V * E) bound is the safe choice.
- A negative cycle reachable from the source would make the stale-check variant loop forever; that is why the prompt excludes it.

**Complexity:** Finalise-on-pop Dijkstra O((V + E) log V). Stale-check variant: O((V + E) log V) with non-negative weights, but with negative edges only an exponential worst-case bound. Bellman-Ford O(V * E).

**Dry run:** `n=4, edges=[[0,1,2],[0,2,3],[2,1,-2],[1,3,1]], src=0`.
- Heap `(0, 0)`. Pop 0, finalise. Relax 1 to 2 and 2 to 3: heap `(2,1), (3,2)`.
- Pop `(2, 1)`: finalise 1 at 2. Relax 3 to 3. Heap `(3,2), (3,3)`.
- Pop `(3, 2)`: finalise 2 at 3. The edge 2->1 would give 1, but 1 is finalised: skipped. Pop `(3, 3)`: finalise 3 at 3.
- Dijkstra `[0, 2, 3, 3]`. Truth: 0->2->1 costs 1, then 3 costs 2: `[0, 1, 3, 2]`. Node 3 is wrong too: the error spreads to everything downstream.

**Code:**
```python
import heapq
import itertools
import random

random.seed(42)
INF = float('inf')

def to_list(d):
    return [None if x == INF else x for x in d]

def dijkstra_finalise(n, edges, src, trace=None):
    """Finalise-on-first-pop Dijkstra, exactly as the prompt describes."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    h = [(0, src)]
    done = set()
    while h:
        d, u = heapq.heappop(h)
        if u in done:
            continue
        done.add(u)                                  # u's distance is now treated as final
        if trace is not None:
            trace.append(f'finalise {u} at {d}')
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
            elif v in done and d + w < dist[v] and trace is not None:
                trace.append(f'   edge {u}->{v} would give {d + w} < {dist[v]}, but {v} is finalised: ignored')
    return to_list(dist)

def dijkstra_stale_check(n, edges, src):
    """Stale-check variant: a node may be expanded again whenever a shorter distance is found."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    h = [(0, src)]
    expansions = 0
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue                                 # stale entry
        expansions += 1
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
    return to_list(dist), expansions

def bellman_ford(n, edges, src):
    """True distances; None if a negative cycle is reachable from src."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] != INF and d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            return None
    return to_list(d)

def solve(n, edges, src):
    return [dijkstra_finalise(n, edges, src), bellman_ford(n, edges, src)]

# ---- examples from the prompt
assert solve(3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], 0) == [[0, 4, 5], [0, 2, 5]]
assert solve(3, [[0, 1, 1], [1, 2, 2]], 0) == [[0, 1, 3], [0, 1, 3]]
assert solve(4, [[0, 1, 2], [0, 2, 3], [2, 1, -2], [1, 3, 1]], 0) == [[0, 2, 3, 3], [0, 1, 3, 2]]
print('examples ok')

# ---- the exact step where the reasoning breaks (smallest case, 3 nodes)
tr = []
dijkstra_finalise(3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], 0, tr)
print('\n'.join(tr))

# ---- exhaustive on three nodes: every edge (6 possible directed pairs) absent or weight -3..3, src = 0
pairs = [(u, v) for u in range(3) for v in range(3) if u != v]
total = wrong = wrong_nonneg = valid = 0
for choice in itertools.product([None, -3, -2, -1, 0, 1, 2, 3], repeat=len(pairs)):
    edges = [[u, v, w] for (u, v), w in zip(pairs, choice) if w is not None]
    true = bellman_ford(3, edges, 0)
    total += 1
    if true is None:                                 # negative cycle reachable: outside the prompt's guarantee
        continue
    valid += 1
    bad = dijkstra_finalise(3, edges, 0) != true
    wrong += bad
    if all(w >= 0 for _, _, w in edges):
        wrong_nonneg += bad
    assert dijkstra_stale_check(3, edges, 0)[0] == true      # the stale-check variant is always right here
print('exhaustive 3-node graphs:', total, 'built,', valid, 'without a reachable negative cycle;',
      'finalise-on-pop wrong on', wrong, '| with all weights >= 0 wrong on', wrong_nonneg)
assert wrong > 0 and wrong_nonneg == 0

# ---- seeded random graphs up to the prompt's limits (n <= 8, weights -10..10), valid ones only
N = 3000
used = diff = 0
for _ in range(N):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-10, 10)] for _ in range(random.randint(0, 16))]
    edges = [e for e in edges if e[0] != e[1]]
    src = random.randrange(n)
    true = bellman_ford(n, edges, src)
    if true is None:
        continue
    used += 1
    assert dijkstra_stale_check(n, edges, src)[0] == true
    diff += dijkstra_finalise(n, edges, src) != true
print('random check:', used, 'valid seeded graphs; stale-check Dijkstra == Bellman-Ford on all;',
      'finalise-on-pop differs on', diff)

# ---- no running-time guarantee for the stale-check variant (family OUTSIDE the prompt's n <= 8 bound)
def blowup(k):
    """k gadgets x -> y: a direct 0-edge and a detour x -> h -> y that is cheaper only once h is popped."""
    edges = []
    for i in range(k):
        x, h, y = 2 * i, 2 * i + 1, 2 * i + 2
        a = 2 ** (k - i)
        edges += [[x, y, 0], [x, h, a], [h, y, -2 * a]]
    return 2 * k + 1, edges
rows = []
for k in (1, 2, 3, 4, 8, 12):
    n, e = blowup(k)
    dist, exp = dijkstra_stale_check(n, e, 0)
    assert dist == bellman_ford(n, e, 0)
    rows.append((n, exp))
print('expansions on the blow-up family (n nodes, expansions):', rows)
assert rows[-1][1] > 2 ** 12

# ---- edge cases
assert solve(1, [], 0) == [[0], [0]]
assert solve(3, [[1, 2, -5]], 0) == [[0, None, None], [0, None, None]]      # negative edge, unreachable: no effect
assert solve(2, [[0, 1, 0]], 0) == [[0, 0], [0, 0]]
assert solve(2, [[0, 1, -10], [0, 1, 10]], 0) == [[0, -10], [0, -10]]          # parallel edges, negative one wins
print('edge cases ok')
```

**Output (my run):**
```
examples ok
finalise 0 at 0
finalise 1 at 4
finalise 2 at 5
   edge 2->1 would give 2 < 4, but 1 is finalised: ignored
exhaustive 3-node graphs: 262144 built, 64927 without a reachable negative cycle; finalise-on-pop wrong on 2897 | with all weights >= 0 wrong on 0
random check: 2047 valid seeded graphs; stale-check Dijkstra == Bellman-Ford on all; finalise-on-pop differs on 20
expansions on the blow-up family (n nodes, expansions): [(3, 4), (5, 10), (7, 22), (9, 46), (17, 766), (25, 12286)]
edge cases ok
```

**Edge cases:**
- All weights non-negative: both agree (checked exhaustively on three nodes).
- A negative edge that is unreachable from `src`: no effect.
- A negative edge whose source node is popped before its target is finalised: no harm. The bug only shows when the negative edge is discovered after the target was finalised.
- Parallel edges with a negative one: Bellman-Ford and the heap both see the smaller.
- Zero-weight edges are fine.
- Negative cycle reachable from the source: excluded by the prompt; Bellman-Ford detects it on pass n.

**Follow-ups:**
- *How do you fix Dijkstra for negative edges without a negative cycle?* Johnson's reweighting: run Bellman-Ford once to get potentials, make every edge non-negative, then run Dijkstra.
- *Could you just add a big constant to every weight?* No. Paths with more edges get penalised more, so the shortest path itself changes.
- *Which is faster, SPFA (queue-based Bellman-Ford)?* Often, on typical graphs, but its worst case is still O(V * E).

**Common mistakes:**
- Saying "Dijkstra fails because of negative cycles". It already fails with a single negative edge and no cycle.
- Adding a constant to all edges.
- Believing the stale-check variant is as fast as Dijkstra with negative edges.
- Forgetting that the error spreads to all nodes reached through the wrongly finalised node.

### Q43 ⭐ 🔴 Number of islands II (online union-find). A grid of `m` rows and `n` columns (1 <= m, n, m*n <= 10^4) starts as all water. `positions` is a list of up to 10^4 cells [r, c]; cells are turned into land one at a time and a cell may be listed more than once (turning land into land changes nothing). After each addition return the current number of islands (4-directional connectivity). Return the list of counts. Use union-find with the count adjusted on each merge (O(k * alpha) in total) and explain why re-running a flood fill after each addition is O(k * m * n). Example: m=3, n=3, positions=[[0, 0], [0, 1], [1, 2], [2, 1]] -> [1, 1, 2, 3]; m=3, n=3, positions=[[0, 0], [0, 1], [1, 2], [1, 1], [1, 1]] -> [1, 1, 2, 1, 1]; m=1, n=1, positions=[[0, 0]] -> [1].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Online connectivity with union-find. Land is only ever added, so components only merge.

**Say this first (1 line):** "Each new land cell adds one island, then every union with a land neighbour that really joins two different islands takes one away, so union-find gives each answer in near-constant time."

**Brute force:** After every addition rebuild the grid and count islands by flood fill. One count is O(m * n), so k additions cost O(k * m * n). With m * n = 10^4 and k = 10^4 that is about 10^8 steps in Python, too slow. It is the cross-check in the code.

**Optimal:**
- Number cells as `r * n + c`. A cell is land when it is in the `parent` dict.
- For each `[r, c]`: if it is already land, append the current count and move on (turning land into land changes nothing, and it must not be counted twice).
- Otherwise create it as its own set and `count += 1`.
- For each of the four neighbours that is inside the grid and already land: `union(cell, neighbour)`. If the two roots differ (a real merge), `count -= 1`. If they are the same set, nothing changes, which is what stops double counting when two neighbours are already in one island.
- Append `count` to the answer.
- Diagonal cells are not neighbours, so they do not merge (checked in the code).
- The count is not monotone: it goes up when an isolated cell appears and down when a bridge cell joins islands, e.g. `[1, 2, 3, 2, 1]`.
- Union by size plus path halving keeps `find` almost constant (inverse Ackermann). `find` is iterative on purpose: a recursive find on a long chain hits the recursion limit (the code shows `RecursionError` on a 10000-long chain).
- Why re-running flood fill is O(k * m * n): each rerun touches every land cell, up to m * n of them, and it is done after each of the k additions.

**Complexity:** Time O(k * alpha(m * n)) in total, with 4 neighbour checks per addition, so about O(k). Space O(number of land cells) for `parent` and `size`. Brute force: O(k * m * n) time.

**Dry run:** `m=3, n=3, positions=[[0,0],[0,1],[1,2],[1,1],[1,1]]`.
- `[0,0]`: new island, count 1.
- `[0,1]`: new cell, count 2; neighbour `[0,0]` is land, real merge, count 1.
- `[1,2]`: new, count 2; neighbours `[0,2]`, `[2,2]`, `[1,1]` are water: no merge. Count 2.
- `[1,1]`: new, count 3; neighbours `[0,1]` (merge, count 2), `[1,2]` (merge, count 1). Count 1.
- `[1,1]` again: already land, count stays 1.
- Answer `[1, 1, 2, 1, 1]`.

**Code:**
```python
import random

random.seed(43)

def islands_online(m, n, positions):
    """Union-find over cells numbered r * n + c. The island count changes by +1 for a new land cell and
    by -1 for every union that really merges two different islands."""
    parent = {}
    size = {}
    count = 0
    out = []

    def find(x):                                    # iterative, path halving
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    for r, c in positions:
        x = r * n + c
        if x not in parent:                         # a repeated cell changes nothing
            parent[x] = x
            size[x] = 1
            count += 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < m and 0 <= cc < n and rr * n + cc in parent:
                    if union(x, rr * n + cc):
                        count -= 1
        out.append(count)
    return out

def islands_flood(m, n, positions):
    """Brute force: after every addition rebuild the grid and count islands by an iterative flood fill. O(k * m * n)."""
    land = set()
    out = []
    for r, c in positions:
        land.add((r, c))
        seen = set()
        cnt = 0
        for cell in land:
            if cell in seen:
                continue
            cnt += 1
            seen.add(cell)
            st = [cell]
            while st:
                a, b = st.pop()
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    t = (a + da, b + db)
                    if t in land and t not in seen:
                        seen.add(t)
                        st.append(t)
        out.append(cnt)
    return out

# ---- examples from the prompt
assert islands_online(3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]]) == [1, 1, 2, 3]
assert islands_online(3, 3, [[0, 0], [0, 1], [1, 2], [1, 1], [1, 1]]) == [1, 1, 2, 1, 1]
assert islands_online(1, 1, [[0, 0]]) == [1]
print('examples ok')

# ---- seeded cross-check against the flood-fill rebuild (duplicates, 1-wide grids, full grids)
N = 800
for _ in range(N):
    m, n = random.randint(1, 5), random.randint(1, 5)
    pos = [[random.randrange(m), random.randrange(n)] for _ in range(random.randint(1, 15))]
    assert islands_online(m, n, pos) == islands_flood(m, n, pos), (m, n, pos)
print('cross-check on', N, 'seeded grids: union-find == flood fill after every addition')

# ---- the count is NOT monotone: it can go up (new island), stay, or go down (a bridge cell merges islands)
print('counts:', islands_online(3, 3, [[0, 0], [2, 2], [1, 1], [0, 1], [1, 2]]))

# ---- edge cases
assert islands_online(1, 5, [[0, 0], [0, 4], [0, 2], [0, 1], [0, 3]]) == [1, 2, 3, 2, 1]
assert islands_online(2, 2, [[0, 0], [0, 0], [0, 0]]) == [1, 1, 1]        # same cell again and again
assert islands_online(2, 2, [[0, 0], [1, 1], [0, 1]]) == [1, 2, 1]          # diagonal cells are NOT connected
assert islands_online(2, 2, [[0, 0], [1, 1], [0, 1], [1, 0]]) == [1, 2, 1, 1]
# max size: 100 x 100 grid and 10^4 positions with repeats; and a 1 x 10^4 strip filled so unions chain
m = n = 100
pos = [[random.randrange(m), random.randrange(n)] for _ in range(10 ** 4)]
res = islands_online(m, n, pos)
print('100 x 100 grid, 10^4 random additions: final islands', res[-1], 'max seen', max(res))
strip = [[0, c] for c in range(0, 10000, 2)] + [[0, c] for c in range(1, 10000, 2)]
res = islands_online(1, 10000, strip)
print('1 x 10000 strip, even cells then odd cells: peak', max(res), 'final', res[-1])
assert max(res) == 5000 and res[-1] == 1

# ---- why the find must be iterative and the union must not build a long chain
def find_recursive(parent, x):
    return x if parent[x] == x else find_recursive(parent, parent[x])
parent = {i: i for i in range(10000)}
for i in range(9999):
    parent[i] = i + 1                              # naive linking in the unlucky direction: a chain of depth 9999
try:
    find_recursive(parent, 0)
except RecursionError:
    print('recursive find on a 10000-long chain: RecursionError (default limit 1000); the code above uses size + halving')
print('edge cases ok')
```

**Output (my run):**
```
examples ok
cross-check on 800 seeded grids: union-find == flood fill after every addition
counts: [1, 2, 3, 2, 1]
100 x 100 grid, 10^4 random additions: final islands 182 max seen 1316
1 x 10000 strip, even cells then odd cells: peak 5000 final 1
recursive find on a 10000-long chain: RecursionError (default limit 1000); the code above uses size + halving
edge cases ok
```

**Edge cases:**
- A repeated cell: the answer repeats, and nothing is unioned twice.
- Diagonal neighbours: not connected.
- 1-wide grids (1 x n or m x 1): only two neighbours exist per cell.
- A cell that merges up to four different islands at once: the count drops by up to 3 after the +1.
- A cell whose land neighbours are already one island: the roots match, so no decrement.
- 10^4 positions on a 100 x 100 grid: fast, since each addition is near-constant.

**Follow-ups:**
- *What if cells can be removed (land turns back to water)?* Plain union-find cannot split sets. Process offline in reverse, or use a different structure.
- *What if the grid is huge (10^9 x 10^9) but k is small?* The dict-based union-find above only stores land cells, so memory is O(k).
- *Why a dict and not an array of m * n?* Either works at 10^4 cells; the dict also covers the sparse huge-grid case.

**Common mistakes:**
- Not checking for a repeated position (count goes up twice).
- Decrementing the count for every land neighbour, not only for real merges.
- Unioning with a neighbour that is not land yet.
- Using `c * m + r` with the wrong dimension for the id (rows and columns mixed up on non-square grids).

### Q44 ⭐ 🔴 Shortest bridge (DFS then multi-source BFS). `grid` is an n x n matrix (2 <= n <= 100) of 0 (water) and 1 (land) containing exactly two islands (4-directional connectivity). You may flip water cells to land. Return the minimum number of flips that joins the two islands into one. Find one island with an iterative DFS, then run a BFS that starts from all its cells at once and stops when it first touches the other island. Sizes are chosen so that a recursive DFS would exceed CPython's default recursion limit of 1000, so an iterative method (queue or explicit stack) is required. Example: grid=[[0, 1], [1, 0]] -> 1; grid=[[0, 1, 0], [0, 0, 0], [0, 0, 1]] -> 2; grid=[[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]] -> 1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** DFS to find and label one island, then multi-source BFS from all of its cells. BFS levels are the flips needed.

**Say this first (1 line):** "I find one island with an iterative DFS, then start a BFS from every cell of it at once; the level at which the BFS first touches land that is not in the first island is the number of water cells to flip."

**Brute force:** Label both islands, then for every pair of cells (one from each) take the Manhattan distance minus 1 and keep the smallest. With up to 10^4 cells that is O(L1 * L2), up to 25 million pairs. It is correct (for the closest pair, any staircase path between them crosses only water, because a land cell in between would belong to one of the islands and be closer to the other; and Manhattan distance minus 1 is a lower bound for any pair) but slow. It is the cross-check in the code.

**Optimal:**
- Scan row by row for the first land cell. Run a DFS with an explicit stack from it and collect all cells of that island into a set. Iterative is required: a snake-shaped island of about 5000 cells makes a recursive DFS exceed CPython's default recursion limit of 1000 (the code shows `RecursionError`).
- Put every cell of the first island in a queue at distance 0 and in the `seen` set. This is a multi-source BFS: it expands the whole island outwards one ring at a time.
- Pop `(x, y, d)`. For each in-grid neighbour not seen: if it is land (it cannot be in the first island, as those are all seen), return `d`. Otherwise it is water: mark it seen, push it with `d + 1`.
- Why `d` is the answer: a water cell at BFS level `d` is reached from the island through exactly `d` water cells (the first ring is level 1, and so on, the cell itself included). If its neighbour is land of the other island, the path to it uses exactly `d` water cells, and BFS reaches the smallest such `d` first.
- Why a multi-source BFS and not one BFS per cell: it is a single pass over the grid, O(n^2), and levels are measured from the nearest source automatically.
- Diagonal land cells are different islands (4-directional connectivity).

**Complexity:** Time O(n^2): the DFS touches each cell once, the BFS touches each cell at most once. Space O(n^2) for the island set, the `seen` set and the queue.

**Dry run:** `grid=[[0,1,0],[0,0,0],[0,0,1]]`.
- First land cell (0,1). DFS island = `{(0,1)}`.
- Queue `[(0,1,0)]`. Pop it: neighbours (1,1) water, (0,0) water, (0,2) water. Push all with distance 1.
- Pop `(1,1,1)`: neighbours (2,1) water (push, d = 2), (1,0), (1,2) water (push, d = 2). Pop `(0,0,1)` and `(0,2,1)`: their new neighbours (1,0) and (1,2) are already seen or pushed.
- Pop `(2,1,2)`: neighbour (2,2) is land, not in the first island: return 2. Two flips, for example (1,1) and (2,1).

**Code:**
```python
import random
import sys
from collections import deque

random.seed(44)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def shortest_bridge(grid):
    n = len(grid)
    start = next((i, j) for i in range(n) for j in range(n) if grid[i][j] == 1)
    # 1) iterative DFS (explicit stack) collects every cell of the first island
    island = {start}
    stack = [start]
    while stack:
        x, y = stack.pop()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and (a, b) not in island:
                island.add((a, b))
                stack.append((a, b))
    # 2) multi-source BFS from the whole island; level = number of water cells flipped so far
    q = deque((x, y, 0) for x, y in island)
    seen = set(island)
    while q:
        x, y, d = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and (a, b) not in seen:
                if grid[a][b] == 1:                   # touched the other island: d water cells were crossed
                    return d
                seen.add((a, b))
                q.append((a, b, d + 1))
    return -1

def components(grid):
    n = len(grid)
    comp = {}
    c = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and (i, j) not in comp:
                comp[(i, j)] = c
                st = [(i, j)]
                while st:
                    x, y = st.pop()
                    for dx, dy in D4:
                        a, b = x + dx, y + dy
                        if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and (a, b) not in comp:
                            comp[(a, b)] = c
                            st.append((a, b))
                c += 1
    return comp, c

def bridge_brute(grid):
    """Closest pair of land cells from different islands: Manhattan distance minus 1 water cells in between."""
    comp, c = components(grid)
    assert c == 2
    A = [p for p in comp if comp[p] == 0]
    B = [p for p in comp if comp[p] == 1]
    return min(abs(a[0] - b[0]) + abs(a[1] - b[1]) - 1 for a in A for b in B)

def first_island_recursive(grid):
    n = len(grid)
    start = next((i, j) for i in range(n) for j in range(n) if grid[i][j] == 1)
    seen = set()
    def go(x, y):
        seen.add((x, y))
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and (a, b) not in seen:
                go(a, b)
    go(*start)
    return seen

# ---- examples from the prompt
assert shortest_bridge([[0, 1], [1, 0]]) == 1
assert shortest_bridge([[0, 1, 0], [0, 0, 0], [0, 0, 1]]) == 2
assert shortest_bridge([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]) == 1
print('examples ok')

# ---- exhaustive: every 3 x 3 and 4 x 4 grid that has exactly two islands
tested = 0
for n in (3, 4):
    for mask in range(1 << (n * n)):
        g = [[mask >> (i * n + j) & 1 for j in range(n)] for i in range(n)]
        if components(g)[1] == 2:
            assert shortest_bridge(g) == bridge_brute(g), g
            tested += 1
print('exhaustive:', tested, 'grids with exactly two islands (n = 3, 4): BFS answer == closest-pair answer')

# ---- seeded random 5-8 grids with exactly two islands
N = 400
done = 0
while done < N:
    n = random.randint(5, 8)
    g = [[1 if random.random() < 0.3 else 0 for _ in range(n)] for _ in range(n)]
    if components(g)[1] == 2:
        assert shortest_bridge(g) == bridge_brute(g), g
        done += 1
print('random check on', N, 'seeded grids with exactly two islands ok')

# ---- max size n = 100: one snake-shaped island of about 5000 cells plus a single cell
n = 100
g = [[0] * n for _ in range(n)]
for r in range(0, n, 2):
    for c in range(0, 98):
        g[r][c] = 1                                   # even rows: long horizontal bars
for r in range(1, n, 2):
    g[r][97 if (r // 2) % 2 == 0 else 0] = 1          # odd rows: one connector, alternating ends
g[50][99] = 1                                         # the second island: one cell, one water cell (50, 98) away
comp, c = components(g)
assert c == 2
snake = sum(v == 0 for v in comp.values())
print('snake island cells:', snake, '| islands:', c)
print('bridge on the snake grid:', shortest_bridge(g), '| closest-pair check:', bridge_brute(g))
assert shortest_bridge(g) == bridge_brute(g) == 1
print('recursion limit:', sys.getrecursionlimit())
try:
    first_island_recursive(g)
except RecursionError:
    print('recursive DFS over the snake island: RecursionError (the island has', snake, 'cells in one long path)')

# ---- edge cases
assert shortest_bridge([[1, 0], [0, 1]]) == 1                    # diagonal cells are different islands
assert shortest_bridge([[1, 1, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == 1
big = [[0] * 100 for _ in range(100)]
big[0][0] = 1
big[99][99] = 1
assert shortest_bridge(big) == 197                              # opposite corners: 198 steps, 197 water cells
print('edge cases ok')
```

**Output (my run):**
```
examples ok
exhaustive: 21380 grids with exactly two islands (n = 3, 4): BFS answer == closest-pair answer
random check on 400 seeded grids with exactly two islands ok
snake island cells: 4950 | islands: 2
bridge on the snake grid: 1 | closest-pair check: 1
recursion limit: 1000
recursive DFS over the snake island: RecursionError (the island has 4950 cells in one long path)
edge cases ok
```

**Edge cases:**
- Islands touching only diagonally: distance 1 (one flip joins them).
- Islands at opposite corners of a 100 x 100 grid: 197 flips (the code asserts it).
- The first island is the one with the first land cell in row-major order; the answer does not depend on which island is first.
- A very long, thin first island: iterative DFS needed.
- An island that surrounds the other (a ring around a single cell): the BFS from the outer ring still finds the inner cell at level 1.
- Marking cells as seen when pushed (not when popped) keeps each cell in the queue at most once.

**Follow-ups:**
- *Do it with BFS only?* You can also find the first island with BFS; the DFS is just one way to collect it. Any traversal works.
- *Why not Dijkstra?* All steps cost 1 (a flip), except moving across the first island, which costs 0 and is handled by starting from all its cells at distance 0. That is a 0-1 BFS in disguise.
- *What if there are more than two islands?* Connect them all: that is a minimum spanning tree over islands, a different problem.

**Common mistakes:**
- Starting a BFS from one cell of the island only (wrong levels).
- Returning `d + 1` or counting the first land cell as a flip.
- Not marking the whole first island as seen before the BFS (it would be re-entered and distances become 0).
- A recursive DFS on a 100 x 100 grid (RecursionError).

### Q45 ⭐ 🔴 Minimum height trees (peeling leaves). `edges` is the list of n - 1 undirected [u, v] edges of a tree on nodes 0..n-1 (1 <= n <= 2*10^4). If you pick any node as the root, the tree has a height (the longest downward path in edges). Return the ascending list of all root choices that give the minimum height; there are one or two of them. Do it in O(n) by repeatedly removing all current leaves until at most two nodes remain, and explain why this is Kahn's algorithm on degrees and why at most two nodes can be centres. For n = 1 the answer is [0]. Example: n=4, edges=[[1, 0], [1, 2], [1, 3]] -> [1]; n=6, edges=[[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]] -> [3, 4]; n=1, edges=[] -> [0]; n=2, edges=[[0, 1]] -> [0, 1].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Peel leaves layer by layer, which is Kahn's algorithm on degrees. What survives is the centre of the tree.

**Say this first (1 line):** "The best roots are the centre of the tree, so I keep removing all current leaves until one or two nodes are left; those are the answer, in O(n)."

**Brute force:** Try every node as root, run a BFS to get the height, keep the minimum and all nodes that reach it. That is O(n^2): about 4 * 10^8 steps at n = 2 * 10^4. It is the cross-check.

**Optimal:**
- Build adjacency lists and the degree of every node. For n <= 2 return `list(range(n))` (`[0]` for one node, `[0, 1]` for two: both heights are 1).
- Leaves = all nodes with degree 1. While more than two nodes remain: subtract the number of leaves from the node count, remove every current leaf at once (for each leaf, decrement the degree of its neighbour), and the neighbours whose degree dropped to 1 form the next layer of leaves.
- When two or fewer nodes remain, the current leaf layer is the answer. Sort it.
- Why it is Kahn: Kahn removes nodes with in-degree 0. Here the degree-1 nodes of an undirected tree play that role, and removing them lowers the neighbours' degrees. The layers are the BFS levels from the outside in.
- Why leaves are never good roots (for n >= 3): a leaf root has height at least that of its neighbour plus 1. Move the root one step inwards and the height drops or stays, so removing leaves never loses an optimal root.
- Why at most two centres: the height of the best root is half the longest path (the diameter), rounded up. The centres are the middle of any longest path: one node if it has an even number of edges, two adjacent nodes if odd. All longest paths share the same centre(s). A third centre would have to be at the same distance from both ends of the longest path, which is impossible on a tree path. The code checks it on all 18248 labelled trees with 2 to 7 nodes, and that the minimum height is the ceiling of half the diameter.
- Why we stop at two and do not remove the last pair: removing both would leave nothing; peeling a layer when exactly two nodes remain would empty the tree.

**Complexity:** Time O(n): each node enters a leaf layer once, and each edge is looked at twice (once per endpoint). Space O(n) for the adjacency lists, degrees and layers.

**Dry run:** `n=6, edges=[[3,0],[3,1],[3,2],[3,4],[5,4]]`.
- Degrees: 0, 1, 2 have 1; node 3 has 4; node 4 has 2; node 5 has 1.
- Leaves `[0, 1, 2, 5]`, remaining 6 > 2. Remove them: remaining 2. Node 3's degree drops 4 -> 1 (three removed), node 4's drops 2 -> 1.
- Next leaves `[3, 4]` (both reached degree 1). Remaining is 2, so stop.
- Answer `[3, 4]`. Rooting at 3 gives height 2, rooting at 4 also 2; any other node gives 3.

**Code:**
```python
import itertools
import random
from collections import deque

random.seed(45)

def min_height_roots(n, edges):
    """Peel all current leaves layer by layer (Kahn's algorithm on degrees) until at most two nodes remain."""
    if n <= 2:
        return list(range(n))                      # n = 1 -> [0]; n = 2 -> [0, 1] (both heights are 1)
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(a) for a in adj]
    leaves = [i for i in range(n) if deg[i] == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)                   # the whole layer is removed at once
        nxt = []
        for u in leaves:
            for v in adj[u]:
                deg[v] -= 1
                if deg[v] == 1:                    # v has become a leaf of the smaller tree
                    nxt.append(v)
        leaves = nxt
    return sorted(leaves)

def heights_brute(n, edges):
    """Brute force: BFS from every root and take the longest distance (O(n^2))."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    hs = []
    for r in range(n):
        d = {r: 0}
        q = deque([r])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1
                    q.append(v)
        hs.append(max(d.values()))
    return hs

def mht_brute(n, edges):
    hs = heights_brute(n, edges)
    return [i for i in range(n) if hs[i] == min(hs)]

def prufer_tree(seq, n):
    """Decode a Pruefer sequence into the n - 1 edges of a labelled tree (every labelled tree appears once)."""
    deg = [1] * n
    for x in seq:
        deg[x] += 1
    edges = []
    for x in seq:
        leaf = min(i for i in range(n) if deg[i] == 1)
        edges.append([leaf, x])
        deg[leaf] -= 1
        deg[x] -= 1
    u, v = [i for i in range(n) if deg[i] == 1]
    edges.append([u, v])
    return edges

# ---- examples from the prompt
assert min_height_roots(4, [[1, 0], [1, 2], [1, 3]]) == [1]
assert min_height_roots(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]) == [3, 4]
assert min_height_roots(1, []) == [0]
assert min_height_roots(2, [[0, 1]]) == [0, 1]
print('examples ok')

# ---- exhaustive: EVERY labelled tree on 2..7 nodes (Pruefer: n^(n-2) of them), against the all-roots BFS
total = 0
counts = {1: 0, 2: 0}
for n in range(2, 8):
    for seq in itertools.product(range(n), repeat=n - 2):
        e = prufer_tree(seq, n)
        a = min_height_roots(n, e)
        assert a == mht_brute(n, e), (n, e)
        assert len(a) in (1, 2)                    # the prompt's claim: one or two minimum-height roots
        counts[len(a)] += 1
        total += 1
print('exhaustive:', total, 'labelled trees on 2..7 nodes; answers always match; number of roots:', counts)

# ---- the two roots are adjacent, and the height is ceil(diameter / 2): check on seeded random trees
N = 400
for _ in range(N):
    n = random.randint(1, 30)
    e = [[random.randrange(i), i] for i in range(1, n)]
    random.shuffle(e)
    a = min_height_roots(n, e)
    assert a == mht_brute(n, e)
    if len(a) == 2:
        assert [a[0], a[1]] in e or [a[1], a[0]] in e
    hs = heights_brute(n, e)
    diam = max(hs)                                 # eccentricity of a node on a diameter equals the diameter
    assert min(hs) == (diam + 1) // 2
print('random check on', N, 'seeded trees: answers match, two roots are adjacent, min height = ceil(diameter / 2)')

# ---- edge cases and max size
assert min_height_roots(3, [[0, 1], [1, 2]]) == [1]                 # path with odd node count
assert min_height_roots(4, [[0, 1], [1, 2], [2, 3]]) == [1, 2]      # path with even node count
star = [[0, i] for i in range(1, 20000)]
assert min_height_roots(20000, star) == [0]
path = [[i, i + 1] for i in range(19999)]
assert min_height_roots(20000, path) == [9999, 10000]
random.shuffle(path)
assert min_height_roots(20000, path) == [9999, 10000]              # edge order does not matter
rt = [[random.randrange(i), i] for i in range(1, 20000)]
print('max size n = 20000, random tree roots:', min_height_roots(20000, rt), '| path roots:', min_height_roots(20000, path))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
exhaustive: 18248 labelled trees on 2..7 nodes; answers always match; number of roots: {1: 9415, 2: 8833}
random check on 400 seeded trees: answers match, two roots are adjacent, min height = ceil(diameter / 2)
max size n = 20000, random tree roots: [1, 5] | path roots: [9999, 10000]
edge cases ok
```

**Edge cases:**
- One node: `[0]`. Two nodes: `[0, 1]`.
- Path with an odd node count: one centre; even: two adjacent centres.
- Star: the centre only.
- A node whose degree falls to 1 only after its neighbours are removed becomes a leaf of the NEXT layer, not the current one.
- Edge order in the input does not matter.
- 2 * 10^4 nodes in a path: iterative layers, no recursion at all.

**Follow-ups:**
- *Do it with two BFS passes?* Yes: BFS from any node to the farthest `a`, BFS from `a` to the farthest `b`, then take the middle one or two nodes of the `a`-`b` path. Also O(n).
- *Does it work if the graph is not a tree?* No. A cycle never produces leaves, so the peeling stops with the cycle left.
- *Why not just compute heights with rerooting DP?* It works but is longer; this is the shortest linear solution.

**Common mistakes:**
- Removing one leaf at a time instead of a whole layer (the stopping rule then breaks).
- Forgetting n = 1 and n = 2.
- Looping while the leaf list is not empty instead of while more than two nodes remain.
- Returning an unsorted list.

