### Q41 ⭐ 🔴 Tarjan's strongly connected components, iteratively, with a fixed numbering. `n` nodes 0..n-1 (1 <= n <= 10^5), `edges` directed [u, v] (0 <= len <= 2*10^5; repeats and self loops allowed). Run Tarjan's one-pass algorithm: start a DFS from node 0, 1, 2, ... in that order (skipping visited nodes) and follow each node's out-edges in the ORDER THEY APPEAR in `edges`; keep `idx` (discovery number), `low`, an `on_stack` flag and the node stack; when low[u] == idx[u] pop the stack down to u and give those nodes the next component number 0, 1, 2, ... (so components are numbered in the order they are completed). Return `[comp, count, cross]`: `comp[v]` is the component number of node v, `count` the number of components, and `cross` the number of DISTINCT pairs (comp[u], comp[v]) over edges with different components (the edge count of the condensation). Explain why this numbering is a reverse topological order of the condensation (every edge u -> v has comp[u] >= comp[v]), why only nodes still ON the stack may lower `low[u]` (a node already assigned to a finished component cannot be in u's component), and why the code must be iterative (a path graph of 10^5 nodes would exceed CPython's default recursion limit of 1000). Compare with Kosaraju (Q20): one DFS instead of two plus a reversed graph. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive Tarjan oracle with identical visiting order on small graphs (plus the property comp[u] >= comp[v] on every edge) on small inputs. Example: n=5, edges=[[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [[2, 2, 2, 1, 0], 3, 2]; n=3, edges=[[0, 1], [1, 0], [0, 2], [0, 2]] -> [[1, 1, 0], 2, 1].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)
**Pattern:** Strongly connected components with Tarjan's one-pass DFS (discovery index, low-link, node stack), written with an explicit stack. Directed graph, so "who can reach whom both ways" is the question.

**Say this first (1 line):** "One DFS gives each node a discovery number and a low-link; when a node's low equals its own number it is the root of a component, so I pop the stack down to it, and I keep the DFS on a hand-made stack because a 10^5-node path would blow CPython's 1000-frame limit."

**Brute force:** Compute reachability from every node (BFS each), then group nodes u, v with u reaches v and v reaches u. O(n * (n + m)); Floyd-Warshall style closure is O(n^3). Fine for 8 nodes, hopeless at 10^5. I use it only as the idea behind the definition.

**Optimal:**
- Visit nodes 0, 1, 2, ... and follow out-edges in input order. Each new node gets `idx` (discovery number), `low = idx`, and goes on the node stack with `on_stack = True`.
- Edge u -> v with v unvisited: tree edge, descend. When v finishes, `low[u] = min(low[u], low[v])`.
- Edge u -> v with v visited and still ON the stack: `low[u] = min(low[u], idx[v])`.
- When u finishes and `low[u] == idx[u]`, u is the root of a component: pop until u, give them the next number.
- Why only on-stack nodes may lower `low`: a visited node that is NOT on the stack already belongs to a finished component. If it could reach back to u, u would have been inside that component. So that edge is a cross edge to a finished component and must be ignored. Dropping the test corrupts the components (the run below finds a graph where it changes the answer).
- Why numbering is reverse topological: a component is numbered when its root finishes. For an edge u -> v across components, v's component must be complete before u's root can finish (v was either already finished or is explored beneath u), so comp[v] was numbered first: `comp[u] >= comp[v]`.
- Iterative: the work stack holds `(node, next edge position)`. Popping an entry with edges left means "continue u"; pushing a child means "recurse"; an exhausted entry means "return", where I push the child's `low` up into the parent (the parent is the entry below on the work stack).
- Versus Kosaraju (Q20): Kosaraju needs two DFS passes and a reversed graph; Tarjan needs one pass and no reversed graph, but the low-link logic is subtler.

**Complexity:**
- Time O(n + m): every node is pushed and popped from each stack once, every edge is looked at once. The `cross` count uses a set of at most m pairs.
- Space O(n + m) for the adjacency list, plus O(n) for idx, low, on_stack, comp, node stack and work stack.

**Dry run:** first example, n=5, edges 0->1, 1->2, 2->0, 1->3, 3->4.
- Visit 0 (idx 0), push. Edge 0->1: visit 1 (idx 1). Edge 1->2: visit 2 (idx 2). Stack is [0, 1, 2].
- Edge 2->0: 0 is on the stack, so low[2] = min(2, 0) = 0. Node 2 finishes with low 0 != idx 2: no pop. Parent 1 gets low[1] = 0.
- Back at 1, edge 1->3: visit 3 (idx 3), then 3->4: visit 4 (idx 4). Node 4 finishes with low 4 == idx 4: pop 4, comp 0.
- Node 3 finishes with low 3 == idx 3: pop 3, comp 1. Node 1 finishes with low 0, no pop; node 0 finishes with low 0 == idx 0: pop 2, 1, 0 as comp 2.
- Result comp = [2, 2, 2, 1, 0], count 3. Cross pairs: edge 1->3 gives (2, 1), edge 3->4 gives (1, 0), so cross = 2. Every edge has comp[u] >= comp[v].

**Code:**
```python
import random, sys
random.seed(41)

def tarjan_iter(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)                       # keep input order
    idx = [-1] * n; low = [0] * n; on = [False] * n
    comp = [-1] * n; stack = []; counter = 0; nc = 0
    for s in range(n):
        if idx[s] != -1:
            continue
        idx[s] = low[s] = counter; counter += 1
        stack.append(s); on[s] = True
        work = [(s, 0)]                      # (node, next edge position)
        while work:
            u, i = work.pop()
            if i < len(g[u]):
                work.append((u, i + 1))
                v = g[u][i]
                if idx[v] == -1:             # tree edge: "recurse"
                    idx[v] = low[v] = counter; counter += 1
                    stack.append(v); on[v] = True
                    work.append((v, 0))
                elif on[v]:                  # back/cross edge into the open stack
                    low[u] = min(low[u], idx[v])
            else:                            # u is finished
                if low[u] == idx[u]:         # u is the root of a component
                    while True:
                        w = stack.pop(); on[w] = False; comp[w] = nc
                        if w == u:
                            break
                    nc += 1
                if work:                     # "return" to the parent
                    p = work[-1][0]
                    low[p] = min(low[p], low[u])
    cross = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, nc, cross]

def tarjan_rec(n, edges):                    # oracle: textbook recursion, same visiting order
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n
    st = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; st.append(u); on[u] = True
        for v in g[u]:
            if idx[v] == -1:
                dfs(v); low[u] = min(low[u], low[v])
            elif on[v]:
                low[u] = min(low[u], idx[v])
        if low[u] == idx[u]:
            while True:
                w = st.pop(); on[w] = False; comp[w] = box[1]
                if w == u:
                    break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1:
            dfs(s)
    cross = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, box[1], cross]

# examples from the prompt
assert tarjan_iter(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == [[2, 2, 2, 1, 0], 3, 2]
assert tarjan_iter(3, [[0, 1], [1, 0], [0, 2], [0, 2]]) == [[1, 1, 0], 2, 1]
print('examples ok')

# seeded random cross-check vs the recursive oracle + reverse-topological property
for _ in range(600):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 16))]
    a = tarjan_iter(n, edges)
    assert a == tarjan_rec(n, edges), (n, edges)
    comp = a[0]
    assert all(comp[u] >= comp[v] for u, v in edges)
print('600 random graphs: iterative == recursive oracle, comp[u] >= comp[v] on every edge')

# edge cases
assert tarjan_iter(1, []) == [[0], 1, 0]
assert tarjan_iter(1, [[0, 0]]) == [[0], 1, 0]               # self loop
assert tarjan_iter(3, []) == [[0, 1, 2], 3, 0]               # isolated nodes, completed in order
assert tarjan_iter(3, [[0, 1], [1, 2], [2, 0]]) == [[0, 0, 0], 1, 0]

# why iterative: a path of 1500 nodes breaks the recursive version, 10^5 is fine iteratively
path = lambda N: [[i, i + 1] for i in range(N - 1)]
try:
    tarjan_rec(1500, path(1500)); print('recursive survived?!')
except RecursionError:
    print('recursive version: RecursionError at 1500-node path')
N = 10**5
comp, cnt, cross = tarjan_iter(N, path(N))
assert cnt == N and cross == N - 1 and comp[0] == N - 1 and comp[N - 1] == 0
print('iterative 10^5 path ok: components', cnt, 'condensation edges', cross)
print('first example:', tarjan_iter(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))

# the on-stack test matters: without it a cross edge into a finished component corrupts low and the answer is wrong
def tarjan_no_on_stack(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    idx = [-1] * n; low = [0] * n; comp = [-1] * n; st = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; st.append(u)
        for v in g[u]:
            if idx[v] == -1: dfs(v); low[u] = min(low[u], low[v])
            else: low[u] = min(low[u], idx[v])               # BUG: also fires for finished components
        if low[u] == idx[u]:
            while True:
                w = st.pop(); comp[w] = box[1]
                if w == u: break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1: dfs(s)
    return comp
for _ in range(5000):
    n = random.randint(2, 5)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(1, 7))]
    if tarjan_no_on_stack(n, edges) != tarjan_iter(n, edges)[0]:
        print('without the on-stack test:', n, edges, '->', tarjan_no_on_stack(n, edges), 'instead of', tarjan_iter(n, edges)[0]); break
else:
    raise SystemExit('no counterexample found')
```

**Output (my run):**
```
examples ok
600 random graphs: iterative == recursive oracle, comp[u] >= comp[v] on every edge
recursive version: RecursionError at 1500-node path
iterative 10^5 path ok: components 100000 condensation edges 99999
first example: [[2, 2, 2, 1, 0], 3, 2]
without the on-stack test: 3 [[1, 0], [0, 2], [0, 0], [2, 0]] -> [0, -1, 0] instead of [0, 1, 0]
```

**Edge cases:**
- n = 1, no edges: one component, cross 0.
- Self loop: a node with only a self loop is its own component (the loop is skipped by `comp[u] != comp[v]`).
- Repeated edges: `cross` counts DISTINCT component pairs, hence the set. The second example has two copies of 0 -> 2 and still gives cross = 1.
- No edges: every node is its own component, numbered 0..n-1 in visiting order.
- A long path (10^5 nodes): components are numbered from the far end, so comp[0] = n - 1.
- Disconnected graph: the outer loop restarts the DFS at the next unvisited node.

**Follow-ups:**
- *Why not just reuse Kosaraju?* Both are O(n + m). Tarjan needs one DFS and no transposed graph, which saves memory; Kosaraju is easier to explain and to get right under pressure (Q20).
- *Where do I read the condensation DAG?* The `cross` pairs are its edges; because of the numbering, they all go from a higher component number to a lower one, so listing components from the highest number down is a topological order of the condensation.
- *What breaks if I drop the `on_stack` check?* A cross edge into an already finished component would drag `low[u]` below `idx[u]`, so u never becomes a root and the components come out wrong (in the run, one node is never assigned at all). The run below prints a small graph where the answer changes.

**Common mistakes:**
- Using `low[u] = min(low[u], low[v])` for a non-tree edge instead of `idx[v]` (it still works in many tests but muddles the definition; keep `idx[v]`).
- Forgetting to propagate the child's low into the parent when simulating the return.
- Not following edges in input order, so the numbering differs from the required one.
- Writing the recursive version and trusting it: it raises RecursionError on the 1500-node path, as the output shows.
- Counting `cross` with a plain counter, so repeated edges are over-counted.

### Q42 ⭐ 🔴 Articulation points (cut vertices). `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` undirected [u, v] pairs (0 <= len <= 2*10^5; the graph may be disconnected; parallel edges and self loops may occur). A node is an articulation point when deleting it (and its edges) increases the number of connected components among the remaining nodes beyond what its own removal explains (an isolated node, or a node alone in its component, is NOT an articulation point). Return the articulation points sorted ascending. Use the discovery times and `low` values of Q33 with the two rules: a DFS ROOT is an articulation point when it has at least two DFS-tree children; a non-root p is one when some child u has low[u] >= disc[p] (note >=, where a bridge needs >). Write it iteratively because a path of 10^5 nodes exceeds CPython's default recursion limit of 1000. Say why >= is right for vertices and > for edges (a back edge that lands on p itself still leaves p as the cut vertex but saves the edge). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that deletes each node in turn and recounts connected components on small inputs. Example: n=5, edges=[[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]] -> [1, 3]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> []; n=4, edges=[[0, 1], [0, 2], [0, 3]] -> [0].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)
**Pattern:** Articulation points with DFS discovery times and low-link values, written iteratively. The same machinery as bridges (Q33), with a different test.

**Say this first (1 line):** "A DFS root is a cut vertex if it has two or more tree children; any other node p is one if some child u has low[u] >= disc[p], meaning u's subtree cannot climb above p."

**Brute force:** For each node v, delete it and count connected components again (union-find or BFS). O(n * (n + m)). It is my oracle for small inputs and the definition in code.

**Optimal:**
- One DFS per component. `disc[u]` is the discovery time; `low[u]` is the smallest discovery time reachable from u's subtree using tree edges down and at most one back edge up.
- When a child u of p finishes: `low[p] = min(low[p], low[u])`. If p is not the root and `low[u] >= disc[p]`, p is an articulation point.
- Root rule: the root has no ancestors, so it is a cut vertex only if it has at least two DFS-tree children (its children are then only connected through it).
- Why `>=` for vertices but `>` for edges: if the best u's subtree can do is reach p itself (`low[u] == disc[p]`), then deleting the EDGE p-u keeps the subtree attached via the back edge to p, so it is not a bridge. But deleting the VERTEX p removes that landing point, so the subtree is cut off, and p is a cut vertex. Example: two triangles sharing node 2; with `>` the code would miss node 2 (the output shows it).
- Skip the arrival edge by edge id, not by parent node, so a parallel edge to the parent counts as a back edge. Self loops are dropped.
- Iterative form: the work stack holds `(node, arrival edge id, next adjacency position)`; when an entry is exhausted, the entry below is the parent.

**Complexity:** Time O(n + m): each adjacency entry is read once. Space O(n + m): adjacency list, disc, low, work stack.

**Dry run:** first example, edges 0-1, 1-2, 2-0, 1-3, 3-4.
- DFS from 0: disc[0]=0; go to 1 (disc 1); from 1 go to 2 (disc 2); at 2, neighbour 0 is visited (not the arrival edge), so low[2] = 0.
- 2 finishes: low[1] = 0; check low[2] = 0 >= disc[1] = 1? No.
- From 1 go to 3 (disc 3), then 4 (disc 4). 4 finishes with low 4: 4 >= disc[3] = 3, so 3 is an articulation point.
- 3 finishes: low[3] = 3 >= disc[1] = 1, so 1 is an articulation point.
- 1 finishes, parent is the root 0 with one tree child, so 0 is not a cut vertex. Answer [1, 3].

**Code:**
```python
import random
random.seed(42)

def articulation(n, edges):
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:                            # self loops never matter
            g[u].append((v, i)); g[v].append((u, i))
    disc = [-1] * n; low = [0] * n; t = 0; arts = set()
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = t; t += 1; kids = 0
        st = [(s, -1, 0)]                     # (node, edge id used to arrive, next adjacency position)
        while st:
            u, pe, i = st.pop()
            if i < len(g[u]):
                st.append((u, pe, i + 1))
                v, e = g[u][i]
                if e == pe:                   # skip the arrival edge by id (parallel edges still count)
                    continue
                if disc[v] == -1:
                    disc[v] = low[v] = t; t += 1
                    st.append((v, e, 0))
                else:
                    low[u] = min(low[u], disc[v])
            elif st:                          # u finished; its parent entry is on top
                p = st[-1][0]
                low[p] = min(low[p], low[u])
                if p == s:
                    kids += 1
                elif low[u] >= disc[p]:       # >= : the back edge may land ON p
                    arts.add(p)
        if kids >= 2:
            arts.add(s)
    return sorted(arts)

def comps(n, edges, skip=-1):
    p = list(range(n))
    def f(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges:
        if u != skip and v != skip:
            p[f(u)] = f(v)
    return len({f(x) for x in range(n) if x != skip})

def oracle(n, edges):                         # delete each node and recount components
    base = comps(n, edges)
    out = []
    for v in range(n):
        isolated = not any((u == v) != (w == v) for u, w in edges)   # no edge to another node
        expected = base - 1 if isolated else base                     # removing it explains this much
        if comps(n, edges, v) > expected:
            out.append(v)
    return out

assert articulation(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == [1, 3]
assert articulation(3, [[0, 1], [1, 2], [2, 0]]) == []
assert articulation(4, [[0, 1], [0, 2], [0, 3]]) == [0]
print('examples ok')

for _ in range(800):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 12))]
    assert articulation(n, edges) == oracle(n, edges), (n, edges)
print('800 random graphs match the delete-each-node oracle')

assert articulation(1, []) == [] and articulation(2, [[0, 1]]) == []     # lone node, single edge
assert articulation(2, [[0, 1], [0, 1]]) == []                           # parallel edges
assert articulation(3, [[0, 1], [1, 2]]) == [1]                          # path
assert articulation(4, [[0, 0], [1, 2], [2, 3]]) == [2]                  # disconnected + self loop
assert articulation(4, [[0, 1], [1, 2], [2, 3], [3, 0]]) == []           # cycle

# '>' instead of '>=' is wrong for vertices: a cycle hanging off p has low[child] == disc[p]
def art_gt(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v); g[v].append(u)
    disc = [-1] * n; low = [0] * n; res = set(); t = [0]
    def dfs(u, p, root):
        disc[u] = low[u] = t[0]; t[0] += 1; kids = 0
        for v in g[u]:
            if v == p: continue
            if disc[v] == -1:
                kids += 1; dfs(v, u, False); low[u] = min(low[u], low[v])
                if not root and low[v] > disc[u]: res.add(u)
            else: low[u] = min(low[u], disc[v])
        if root and kids >= 2: res.add(u)
    for s in range(n):
        if disc[s] == -1: dfs(s, -1, True)
    return sorted(res)
bowtie = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]]               # two triangles sharing node 2
print('bowtie: >= gives', articulation(5, bowtie), ' > gives', art_gt(5, bowtie))
assert articulation(5, bowtie) == [2] and art_gt(5, bowtie) == []

N = 10**5
assert articulation(N, [[i, i + 1] for i in range(N - 1)]) == list(range(1, N - 1))
print('10^5 path iterative ok')
print('first example:', articulation(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))
```

**Output (my run):**
```
examples ok
800 random graphs match the delete-each-node oracle
bowtie: >= gives [2]  > gives []
10^5 path iterative ok
first example: [1, 3]
```

**Edge cases:**
- A single node, or two nodes with one edge: no articulation points (removing a node leaves one component or none).
- Isolated nodes and a node alone in its component are never articulation points.
- Parallel edges between the same pair: still no cut vertex; the second copy is a back edge because the arrival edge is skipped by id.
- Self loops: ignored.
- Disconnected graph: run the DFS from each unvisited node, and apply the root rule per DFS tree.
- Path of 10^5 nodes: every inner node is a cut vertex and nothing recurses.

**Follow-ups:**
- *How do I get bridges at the same time?* Same disc and low; test `low[u] > disc[p]` (Q33).
- *Why is the root special?* With no parent, `low[u] >= disc[root]` is always true, so the child test would flag every root. The real question is whether the root has at least two separate child subtrees.
- *Can I find the blocks (biconnected components)?* Yes: push edges on a stack and pop a block whenever `low[u] >= disc[p]`. Not needed for this question.

**Common mistakes:**
- Using `>` (bridge rule) and missing cut vertices that sit on a cycle through the parent.
- Applying the child test to the root, flagging it always.
- Skipping the parent by node instead of by edge id, which breaks parallel edges.
- Counting root children as DFS neighbours instead of DFS-tree children.
- Recursive DFS on a path of 10^5 nodes.

### Q43 ⭐ 🔴 Maximum bipartite matching with augmenting paths (Kuhn's algorithm). `L` left nodes 0..L-1 and `R` right nodes 0..R-1 (1 <= L, R <= 300) with `edges`, a list of [left, right] pairs (0 <= len <= 3000, repeats allowed). A matching pairs each node with at most one partner along an edge. Return `[size, saturated]`: the maximum number of matched pairs and whether it equals L (every left node matched). For each left node run a DFS that tries each neighbour v not yet seen in this attempt: if v is free or its current partner can be re-matched elsewhere (recursive call), take v. Time O(L * E); the recursion depth is at most L <= 300, far below CPython's default recursion limit of 1000, so recursion is fine (a version for much larger L would need an explicit stack or Hopcroft-Karp). Explain why an augmenting path is the only way a matching can grow (Berge's theorem, stated, not proved) and the link to the earlier basic colouring check Part 9 Q21 (a graph is bipartite exactly when it has no odd cycle) and to 'assign jobs to workers' questions. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an exhaustive oracle that tries every assignment of right nodes with a memoised DP over bitmasks (L, R <= 6) on small inputs. Example: L=3, R=3, edges=[[0, 0], [0, 1], [1, 0], [2, 0]] -> [2, False]; L=2, R=2, edges=[[0, 0], [0, 1], [1, 0]] -> [2, True].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)
**Pattern:** Maximum bipartite matching by repeated augmenting-path search (Kuhn's algorithm); the DFS depth is at most L <= 300 so ordinary recursion is fine.

**Say this first (1 line):** "For each left node I try to find an augmenting path: take a free right neighbour, or ask that neighbour's current partner to move elsewhere; each success grows the matching by one."

**Brute force:** Try every assignment of right nodes to left nodes (including "unmatched"), memoised over a bitmask of used right nodes: O(L * 2^R) states. Only feasible for R <= about 20; I use it as the oracle with L, R <= 6.

**Optimal:**
- Keep `match_r[v]`, the left partner of right node v (or -1).
- For left node u run `try_augment(u, seen)`. For each neighbour v not yet in `seen`: mark it, and if v is free, or `try_augment(match_r[v], seen)` succeeds, set `match_r[v] = u` and return True.
- `seen` is fresh for every left node. It stops the search from visiting a right node twice in one attempt, which bounds each attempt to O(E).
- Why augmenting paths are the only way to grow (Berge's theorem, stated, not proved): a matching is maximum exactly when it has no augmenting path, i.e. an alternating path from a free left node to a free right node. Flipping such a path adds one pair. So if the search from u fails, no later change can help u in this round, and the algorithm is correct.
- A plain greedy (first free neighbour) is not enough: left 0 grabs right 0 and left 1, whose only choice is right 0, is stuck. Kuhn moves left 0 to right 1.
- Link to Part 9 Q21: a graph is bipartite exactly when it has no odd cycle; matching assumes the two sides are already given. 'Assign jobs to workers' is this model: left = workers, right = jobs, an edge when the worker can do the job.

**Complexity:** Time O(L * E): up to L attempts, each visits each edge at most once. With L, R <= 300 and E <= 3000 that is under a million steps. Space O(L + R + E); the recursion depth is at most L (the code run below measures 300 on a worst-case chain). For much larger inputs use Hopcroft-Karp (O(E sqrt V)) with an explicit stack.

**Dry run:** second example, L=2, R=2, edges 0-0, 0-1, 1-0.
- Left 0: neighbour right 0 is free, so match_r[0] = 0.
- Left 1: neighbour right 0 is taken by left 0; mark it seen and ask left 0 to move. Left 0 skips right 0 (seen), tries right 1: free, so match_r[1] = 0. Back in left 1: match_r[0] = 1.
- Matching: left 0 with right 1, left 1 with right 0. Size 2 = L, so [2, True].
- First example (L=3, R=3, edges 0-0, 0-1, 1-0, 2-0): left 0 takes right 0; left 1 pushes left 0 to right 1; left 2 only knows right 0, whose owner (left 1) has no other choice, so it fails. Size 2, [2, False].

**Code:**
```python
import random, sys
from functools import lru_cache
random.seed(43)

def kuhn(L, R, edges):
    g = [[] for _ in range(L)]
    for u, v in edges:
        g[u].append(v)
    match_r = [-1] * R                        # match_r[v] = left partner of right node v

    def try_augment(u, seen):                 # recursion depth <= L <= 300
        for v in g[u]:
            if v in seen:
                continue
            seen.add(v)
            if match_r[v] == -1 or try_augment(match_r[v], seen):
                match_r[v] = u                # flip the augmenting path
                return True
        return False

    size = sum(1 for u in range(L) if try_augment(u, set()))
    return [size, size == L]

def oracle(L, R, edges):                      # exhaustive: memoised DP over bitmasks of used right nodes
    g = [set() for _ in range(L)]
    for u, v in edges:
        g[u].add(v)
    @lru_cache(None)
    def f(i, mask):
        if i == L:
            return 0
        best = f(i + 1, mask)                 # leave left node i unmatched
        for v in g[i]:
            if not mask >> v & 1:
                best = max(best, 1 + f(i + 1, mask | 1 << v))
        return best
    s = f(0, 0)
    return [s, s == L]

assert kuhn(3, 3, [[0, 0], [0, 1], [1, 0], [2, 0]]) == [2, False]
assert kuhn(2, 2, [[0, 0], [0, 1], [1, 0]]) == [2, True]
print('examples ok')

for _ in range(500):
    L, R = random.randint(1, 6), random.randint(1, 6)
    edges = [[random.randrange(L), random.randrange(R)] for _ in range(random.randint(0, 14))]
    assert kuhn(L, R, edges) == oracle(L, R, edges), (L, R, edges)
print('500 random small graphs match the bitmask oracle')

assert kuhn(1, 1, []) == [0, False]
assert kuhn(2, 2, [[0, 0], [0, 0], [1, 0]]) == [1, False]   # repeats, one right node
assert kuhn(3, 1, [[0, 0], [1, 0], [2, 0]]) == [1, False]
# greedy without re-matching is not enough: left 0 grabs right 0, then left 1 is stuck
def greedy(L, R, edges):
    used = set(); n = 0; g = [[] for _ in range(L)]
    for u, v in edges: g[u].append(v)
    for u in range(L):
        for v in g[u]:
            if v not in used: used.add(v); n += 1; break
    return n
E = [[0, 0], [0, 1], [1, 0]]
print('greedy gives', greedy(2, 2, E), 'Kuhn gives', kuhn(2, 2, E)[0])
assert greedy(2, 2, E) == 1 and kuhn(2, 2, E)[0] == 2
# max size: L = R = 300 where left i prefers right i-1 (already owned), forcing a ~300-deep augmenting path
L = 300
deep = [[0, 0]] + [[i, v] for i in range(1, L) for v in (i - 1, i)]
cur = [0, 0]                                  # current and max depth of try_augment, measured from outside
def prof(frame, event, arg):
    if frame.f_code.co_name == 'try_augment':
        if event == 'call':
            cur[0] += 1; cur[1] = max(cur[1], cur[0])
        elif event == 'return':
            cur[0] -= 1
sys.setprofile(prof); res = kuhn(L, L, deep); sys.setprofile(None)
print('300 x 300 deep case:', res, 'max recursion depth', cur[1])
assert res == [300, True] and cur[1] <= 300 < sys.getrecursionlimit()
print('first example:', kuhn(3, 3, [[0, 0], [0, 1], [1, 0], [2, 0]]))
```

**Output (my run):**
```
examples ok
500 random small graphs match the bitmask oracle
greedy gives 1 Kuhn gives 2
300 x 300 deep case: [300, True] max recursion depth 300
first example: [2, False]
```

**Edge cases:**
- No edges: size 0, saturated False (L >= 1).
- Repeated edges: harmless, `seen` handles them.
- More left nodes than right nodes: saturated must be False.
- A left node with no neighbours: stays unmatched, and `saturated` is False.
- Maximum size L = R = 300: recursion depth is at most 300, far below 1000.

**Follow-ups:**
- *Why reset `seen` per left node?* A right node that failed in one attempt may succeed after the matching changes in a later attempt.
- *When do I need Hopcroft-Karp?* When L, E are large: it finds many shortest augmenting paths per phase, O(E sqrt V). Kuhn is O(V E).
- *Is there a minimum cover link?* Konig's theorem: in a bipartite graph the maximum matching size equals the minimum vertex cover size. Mention it by name only.

**Common mistakes:**
- Sharing one `seen` across all left nodes (misses augmenting paths).
- Matching greedily and stopping, believing it is maximum.
- Forgetting to assign `match_r[v] = u` when the recursive re-match succeeds.
- Treating repeated edges as extra capacity.
- Reporting `saturated` by comparing with R instead of L.

### Q44 ⭐ 🔴 Segment tree with lazy propagation: range add and range sum. Implement class `RangeAddSum(nums)` (1 <= len <= 10^5) with `add(l, r, v)` (add v, |v| <= 10^9, to every element of nums[l..r], both ends included; returns None) and `sum(l, r)` (the sum of nums[l..r], both ends included). Use a top-down tree where node o covers [lo, hi] and stores `sm[o]` (the true sum of its range) and `lz[o]` (an addition promised to both children but not yet pushed down): when a query or update only partly overlaps a node, `push` the pending value down first (children's sums grow by value * length and their lazy tags by value), recurse, then recompute `sm[o]` from the children. Both operations O(log n), memory O(4n). State the invariant (`sm[o]` is always correct for node o itself; only the children may be stale), and that forgetting to push down before recursing, or using `v` instead of `v * length`, are the classic bugs. Segment-tree recursion depth is about log2(n) (under 20 here), far below CPython's default recursion limit of 1000, so recursion is fine. A shorter alternative for sum-only is two Fenwick trees; the difference-array version for offline updates is Part 13 Q4. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[1, 2, 3, 4, 5]], ops=[['sum', [0, 4]], ['add', [1, 3, 10]], ['sum', [0, 4]], ['sum', [2, 2]], ['add', [0, 4, -1]], ['sum', [0, 1]], ['sum', [3, 4]]] -> [15, null, 45, 13, null, 11, 17].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)
**Pattern:** Segment tree with lazy propagation: range add and range sum, both O(log n).

**Say this first (1 line):** "Each node stores the true sum of its range plus a lazy add it owes its children; I push the lazy value down before going deeper, and a range add of v changes a node's sum by v times its length."

**Brute force:** Plain list. `add` loops over l..r, `sum` slices and adds: O(n) per operation, O(n * q) overall. Fine as the oracle, too slow for 10^5 elements and 10^5 operations.

**Optimal:**
- Node o covers [lo, hi]. `sm[o]` is always the correct sum for o itself. `lz[o]` is an addition already counted in `sm[o]` but not yet pushed to the children, so the children may be stale.
- `_apply(o, v)`: `sm[o] += v * length` and `lz[o] += v`.
- `add(l, r, v)`: if the node is fully inside, apply and stop; if it only partly overlaps, push the pending value down, recurse into both children, then recompute `sm[o] = sm[left] + sm[right]`.
- `sum(l, r)`: same shape; a fully covered node returns `sm[o]`; a partial one pushes down first, then adds the children's answers.
- Push-down order matters: if I recurse before pushing, the children are stale and the children's totals mix old and new values.
- Operation costs: build O(n); `add` O(log n); `sum` O(log n). Memory O(4n) for two arrays. A query touches at most about 4 nodes per level.
- Recursion depth is about log2(n), under 20 for n = 10^5, so recursion is fine.
- Alternative for sum-only: two Fenwick trees (range update, range query). For offline updates a difference array is enough (Part 13 Q4).
- Thread-safety is a concept only here: every operation mutates shared arrays during push-down, even `sum`, so concurrent use needs a lock (or a read-write lock that treats `sum` as a writer).

**Complexity:** Build O(n) time. `add` and `sum` O(log n) time each. Space O(4n). Values grow to 10^5 * 10^9 * (number of adds), still fine for Python ints.

**Dry run:** nums = [1, 2, 3, 4, 5], example ops.
- `sum(0,4)`: the root is fully covered, so 15.
- `add(1,3,10)`: the root splits into [0,2] and [3,4]. In [0,2], [2,2] is fully covered (3 -> 13) and [0,1] splits, with [1,1] becoming 12; recomputing upward gives [0,1] = 13 and [0,2] = 26. In [3,4], [3,3] becomes 14, so [3,4] = 19. Root = 45.
- `sum(0,4)` is 45 and `sum(2,2)` is 13.
- `add(0,4,-1)`: the root is fully covered, so sm = 45 - 5 = 40 and lz[root] = -1 (not pushed).
- `sum(0,1)`: the root is partial, so push: [0,2] becomes 23 (lz -1), [3,4] becomes 17 (lz -1). Then [0,2] pushes: [0,1] becomes 11, [2,2] becomes 12. [0,1] is fully covered: 11.
- `sum(3,4)` reads [3,4] = 17. Results: [15, None, 45, 13, None, 11, 17].

**Code:**
```python
import random
random.seed(44)

class RangeAddSum:
    def __init__(self, nums):
        self.n = len(nums)
        self.sm = [0] * (4 * self.n)          # sm[o]: TRUE sum of node o's range
        self.lz = [0] * (4 * self.n)          # lz[o]: add promised to both children, not yet pushed
        self._build(1, 0, self.n - 1, nums)

    def _build(self, o, lo, hi, a):
        if lo == hi:
            self.sm[o] = a[lo]; return
        mid = (lo + hi) // 2
        self._build(2 * o, lo, mid, a); self._build(2 * o + 1, mid + 1, hi, a)
        self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]

    def _apply(self, o, lo, hi, v):           # v * LENGTH, not v
        self.sm[o] += v * (hi - lo + 1); self.lz[o] += v

    def _push(self, o, lo, hi):
        if self.lz[o]:
            mid = (lo + hi) // 2
            self._apply(2 * o, lo, mid, self.lz[o])
            self._apply(2 * o + 1, mid + 1, hi, self.lz[o])
            self.lz[o] = 0

    def _add(self, o, lo, hi, l, r, v):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self._apply(o, lo, hi, v); return
        self._push(o, lo, hi)                 # push BEFORE recursing
        mid = (lo + hi) // 2
        self._add(2 * o, lo, mid, l, r, v); self._add(2 * o + 1, mid + 1, hi, l, r, v)
        self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]

    def _sum(self, o, lo, hi, l, r):
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.sm[o]
        self._push(o, lo, hi)
        mid = (lo + hi) // 2
        return self._sum(2 * o, lo, mid, l, r) + self._sum(2 * o + 1, mid + 1, hi, l, r)

    def add(self, l, r, v):
        self._add(1, 0, self.n - 1, l, r, v)

    def sum(self, l, r):
        return self._sum(1, 0, self.n - 1, l, r)

class Naive:
    def __init__(self, nums): self.a = list(nums)
    def add(self, l, r, v):
        for i in range(l, r + 1): self.a[i] += v
    def sum(self, l, r): return sum(self.a[l:r + 1])

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ex_ops = [['sum', [0, 4]], ['add', [1, 3, 10]], ['sum', [0, 4]], ['sum', [2, 2]], ['add', [0, 4, -1]], ['sum', [0, 1]], ['sum', [3, 4]]]
got = run(RangeAddSum, [[1, 2, 3, 4, 5]], ex_ops)
assert got == [15, None, 45, 13, None, 11, 17], got
print('example ->', got)

for _ in range(500):
    n = random.randint(1, 9)
    init = [[random.randint(-5, 5) for _ in range(n)]]
    ops = []
    for _ in range(random.randint(0, 30)):
        l = random.randrange(n); r = random.randrange(l, n)
        ops.append(['add', [l, r, random.randint(-9, 9)]] if random.random() < .5 else ['sum', [l, r]])
    assert run(RangeAddSum, init, ops) == run(Naive, init, ops), (init, ops)
print('500 random operation sequences match the naive reference')

assert run(RangeAddSum, [[7]], [['sum', [0, 0]], ['add', [0, 0, -7]], ['sum', [0, 0]]]) == [7, None, 0]   # n = 1
big = 10**9
assert run(RangeAddSum, [[0] * 3], [['add', [0, 2, big]], ['add', [0, 2, big]], ['sum', [0, 2]]])[-1] == 6 * big
# the classic bug: using v instead of v * length
class Bug(RangeAddSum):
    def _apply(self, o, lo, hi, v): self.sm[o] += v; self.lz[o] += v
bad = run(Bug, [[1, 2, 3, 4, 5]], ex_ops)
print('bug (v instead of v*length) gives', bad)
assert bad != got

n = 10**5
obj = RangeAddSum([0] * n)
for i in range(0, n, 50): obj.add(i, n - 1, 1)
assert obj.sum(0, n - 1) == sum(n - i for i in range(0, n, 50))
print('n = 10^5 build + 2000 range adds ok')
```

**Output (my run):**
```
example -> [15, None, 45, 13, None, 11, 17]
500 random operation sequences match the naive reference
bug (v instead of v*length) gives [15, None, 45, 13, None, 12, 18]
n = 10^5 build + 2000 range adds ok
```

**Edge cases:**
- n = 1: the tree is one leaf; every range is [0, 0].
- Single-element ranges l == r.
- Negative v and large |v| up to 10^9: Python ints do not overflow.
- A whole-array update stays at the root (O(1)).
- Repeated adds on the same range accumulate in `lz` without descending.

**Follow-ups:**
- *Why not push in `sum` as well?* You could keep tags and add `lz * overlap` on the way back instead (no push); both work, but then the invariant changes, so choose one and keep it consistent.
- *Range assign instead of add?* Needs a different tag (an assigned value plus a "has tag" flag) and the assign must override pending adds.
- *Range min or max?* Store `mx[o]` with lazy add: `mx[o] = max(children) + lz[o]` (used in Q50).

**Common mistakes:**
- Adding `v` instead of `v * (hi - lo + 1)` to the sum (the output shows the wrong answers).
- Recursing before pushing down.
- Not recomputing `sm[o]` from the children after the recursive calls.
- Using size 2n instead of 4n for the arrays.
- Off-by-one in the half-open versus closed convention (this class is closed on both ends).

### Q45 ⭐ 🔴 Two-dimensional Fenwick tree. Implement class `NumMatrix2D(matrix)` (m x n with 1 <= m, n <= 200) with `update(r, c, v)` (set matrix[r][c] = v; returns None) and `sumRegion(r1, c1, r2, c2)` (the sum of the rectangle with corners (r1, c1) and (r2, c2), both included). Keep a 2D tree `t` of size (m + 1) x (n + 1): an update adds the DELTA (new value minus the stored old value) at every (i, j) with the loops `i += i & -i` over rows and `j += j & -j` over columns, a prefix query P(r, c) sums with `i -= i & -i`, `j -= j & -j`, and a region is P(r2+1, c2+1) - P(r1, c2+1) - P(r2+1, c1) + P(r1, c1) (inclusion-exclusion). Both operations O(log m * log n); the build can simply call `update` for every cell (O(m n log m log n)). This is the Fenwick answer promised in Part 13 Q40 (row prefix sums there cost O(m) per query). Say when a segment tree of segment trees or an offline method is preferred (range updates, memory). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]], ops=[['sumRegion', [0, 0, 2, 3]], ['sumRegion', [1, 1, 2, 2]], ['update', [1, 2, 10]], ['sumRegion', [1, 1, 2, 2]], ['sumRegion', [1, 2, 1, 2]]] -> [28, 11, null, 18, 10].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)
**Pattern:** Two-dimensional Fenwick (binary indexed) tree: point update, rectangle sum, O(log m * log n) each.

**Say this first (1 line):** "A Fenwick tree inside a Fenwick tree: update walks `i += i & -i` over rows and `j += j & -j` over columns adding a delta, prefix queries walk down with `-=`, and a rectangle is four prefixes by inclusion-exclusion."

**Brute force:** Rescan the rectangle on every query: O(m * n) per query; or keep row prefix sums (Part 13 Q40): O(m) per query, O(n) per update. Fine as the oracle.

**Optimal:**
- Tree `t` is (m + 1) x (n + 1), 1-indexed. Keep a copy `a` of current values so that `update(r, c, v)` can compute `delta = v - a[r][c]`.
- Update: for `i = r + 1` upward by `i += i & -i`, for `j = c + 1` upward by `j += j & -j`, add the delta to `t[i][j]`.
- `_pre(r, c)` sums the rectangle with rows < r and columns < c by walking down with `i -= i & -i` and `j -= j & -j`.
- Region: `P(r2+1, c2+1) - P(r1, c2+1) - P(r2+1, c1) + P(r1, c1)`; the last term puts back the corner that was subtracted twice.
- Build: call `update` per cell: O(m n log m log n). With m, n <= 200 that is about 40,000 * 64 steps at worst, instant.
- Costs per operation: `update` O(log m * log n); `sumRegion` O(log m * log n) (four prefix queries); memory O(m n) for the tree and O(m n) for the copy.
- When to prefer something else: range updates or range min/max need a segment tree of segment trees or a 2D lazy scheme; an offline workload may use sorting plus a 1D Fenwick; memory-sparse huge grids need coordinate compression.
- Thread-safety as a concept: updates touch many cells, so a reader could see a half-applied update. A single lock around both methods is the simple answer.

**Complexity:** Time O(log m * log n) per operation, O(m n log m log n) to build. Space O(m n).

**Dry run:** matrix [[3,0,1,4],[5,6,3,2],[1,2,0,1]].
- `sumRegion(0,0,2,3)`: every cell: 3+0+1+4+5+6+3+2+1+2+0+1 = 28.
- `sumRegion(1,1,2,2)` = P(3,3) - P(1,3) - P(3,1) + P(1,1) = 21 - 4 - 9 + 3 = 11 (the cells 6, 3, 2, 0).
- `update(1,2,10)`: old value 3, delta 7. Row positions visited: 2 (then 4 > 3 stops). Column positions: 3, 4 (then 8 > 4 stops). So t[2][3] and t[2][4] gain 7.
- `sumRegion(1,1,2,2)` is now 6 + 10 + 2 + 0 = 18; `sumRegion(1,2,1,2)` is the single cell 10. Results: [28, 11, None, 18, 10].

**Code:**
```python
import random
random.seed(45)

class NumMatrix2D:
    def __init__(self, matrix):
        self.m = len(matrix); self.n = len(matrix[0])
        self.a = [[0] * self.n for _ in range(self.m)]            # current values (for the delta)
        self.t = [[0] * (self.n + 1) for _ in range(self.m + 1)]  # 1-indexed tree
        for i in range(self.m):
            for j in range(self.n):
                self.update(i, j, matrix[i][j])

    def update(self, r, c, v):
        d = v - self.a[r][c]
        self.a[r][c] = v
        i = r + 1
        while i <= self.m:
            j = c + 1
            while j <= self.n:
                self.t[i][j] += d
                j += j & -j
            i += i & -i

    def _pre(self, r, c):                     # sum of rows < r and columns < c
        s = 0; i = r
        while i > 0:
            j = c
            while j > 0:
                s += self.t[i][j]
                j -= j & -j
            i -= i & -i
        return s

    def sumRegion(self, r1, c1, r2, c2):
        return (self._pre(r2 + 1, c2 + 1) - self._pre(r1, c2 + 1)
                - self._pre(r2 + 1, c1) + self._pre(r1, c1))

class Naive:
    def __init__(self, matrix): self.a = [list(r) for r in matrix]
    def update(self, r, c, v): self.a[r][c] = v
    def sumRegion(self, r1, c1, r2, c2):
        return sum(self.a[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

init = [[[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]]
ops = [['sumRegion', [0, 0, 2, 3]], ['sumRegion', [1, 1, 2, 2]], ['update', [1, 2, 10]], ['sumRegion', [1, 1, 2, 2]], ['sumRegion', [1, 2, 1, 2]]]
got = run(NumMatrix2D, init, ops)
assert got == [28, 11, None, 18, 10], got
print('example ->', got)

for _ in range(400):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    ops = []
    for _ in range(random.randint(0, 25)):
        if random.random() < .4:
            ops.append(['update', [random.randrange(m), random.randrange(n), random.randint(-9, 9)]])
        else:
            r1 = random.randrange(m); r2 = random.randrange(r1, m); c1 = random.randrange(n); c2 = random.randrange(c1, n)
            ops.append(['sumRegion', [r1, c1, r2, c2]])
    assert run(NumMatrix2D, [mat], ops) == run(Naive, [mat], ops), (mat, ops)
print('400 random operation sequences match the naive reference')

assert run(NumMatrix2D, [[[5]]], [['sumRegion', [0, 0, 0, 0]], ['update', [0, 0, -2]], ['sumRegion', [0, 0, 0, 0]]]) == [5, None, -2]
assert run(NumMatrix2D, [[[1, 2, 3]]], [['sumRegion', [0, 1, 0, 2]]]) == [5]     # single row
assert run(NumMatrix2D, [[[1], [2], [3]]], [['sumRegion', [0, 0, 2, 0]]]) == [6]  # single column
# update stores the DELTA: setting a cell to its current value changes nothing
assert run(NumMatrix2D, [[[4, 4], [4, 4]]], [['update', [1, 1, 4]], ['sumRegion', [0, 0, 1, 1]]]) == [None, 16]
t = NumMatrix2D([[1] * 200 for _ in range(200)])
assert t.sumRegion(0, 0, 199, 199) == 40000
t.update(199, 199, 101)
assert t.sumRegion(0, 0, 199, 199) == 40100 and t.sumRegion(199, 199, 199, 199) == 101
print('200 x 200 ok')
```

**Output (my run):**
```
example -> [28, 11, None, 18, 10]
400 random operation sequences match the naive reference
200 x 200 ok
```

**Edge cases:**
- 1 x 1 matrix; a single row or a single column.
- `update` to the same value: delta 0, no change.
- A region equal to the whole matrix: P(m, n) with the three other terms zero.
- Negative values and negative updates: fine, the tree stores signed deltas.
- Rectangle corners given with r1 <= r2 and c1 <= c2 (the prompt guarantees this).

**Follow-ups:**
- *Why store the delta and not the value?* Every tree cell holds a partial sum; adding the new value would double count what is already there.
- *Does 2D get cheaper with a 1D tree per row?* Each query then costs O(m log n) and each update O(log n); the 2D tree balances both at O(log m * log n).
- *Part 13 Q40 asked the row-prefix version; what is the trade?* That one is O(m) query and O(n) update; this is the Fenwick answer promised there.

**Common mistakes:**
- Forgetting the +1 shift between 0-indexed cells and the 1-indexed tree.
- Mixing up the inclusion-exclusion signs, or using r2 and c2 without +1.
- Adding `v` instead of the delta.
- Loop bound `<= m` and `<= n` written as `<` (drops the last row or column).
- Forgetting to store the new value back into `a`.

### Q46 ⭐ 🔴 Count of smaller numbers after self. `nums` has 0 <= len <= 10^5 integers (duplicates allowed, |value| <= 10^9). Return a list `res` where res[i] is the number of elements to the RIGHT of position i that are STRICTLY smaller than nums[i]. Compress the values to ranks (Q17), scan from the right, and for each element query the Fenwick prefix count of ranks smaller than its own (rank - 1) before inserting its rank; O(n log n). Explain the scan direction (right to left, so the tree holds exactly the elements to the right) and why the merge-sort alternative has to carry the original indices through the merge (compare Part 13 Q17 and Part 13 Q47 for merge-sort counting). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) double loop on small inputs. Example: nums=[5, 2, 6, 1] -> [2, 1, 1, 0]; nums=[2, 2, 2] -> [0, 0, 0]; nums=[] -> [].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)
**Pattern:** Fenwick tree over compressed ranks, scanning right to left (counting inversions per element).

**Say this first (1 line):** "I rank-compress the values, walk from the right, and before inserting each element's rank I ask the Fenwick tree how many ranks smaller than mine it already holds; that is exactly the count of smaller numbers to my right."

**Brute force:** For each i, loop over j > i and count `nums[j] < nums[i]`: O(n^2). At 10^5 elements that is 5 * 10^9 comparisons.

**Optimal:**
- Compress: sorted distinct values get ranks 1..k (equal values share a rank). Compression (Q17) keeps the tree at size k instead of 2 * 10^9.
- Scan i from n-1 down to 0. The tree currently holds exactly `nums[i+1:]`. `res[i] = prefix(rank - 1)` counts ranks strictly less than mine; then add 1 at my rank.
- Strictness: query `rank - 1`, never `rank`, so duplicates are not counted (the [2, 2, 2] example gives zeros).
- Why right to left: scanning left to right with the same query counts smaller elements on the LEFT (the output shows the different answer). 
- Merge-sort alternative: also O(n log n), but sorting moves elements, so you must carry the original indices through the merge and add to `res[original index]`, counting during the merge when a right-half element is placed before a left-half element (compare Part 13 Q17 and Part 13 Q47).

**Complexity:** Time O(n log n): sorting the distinct values, then one Fenwick query and one update per element, each O(log k). Space O(n) for ranks, tree and result.

**Dry run:** nums = [5, 2, 6, 1]. Sorted distinct [1, 2, 5, 6], ranks 1 -> 1, 2 -> 2, 5 -> 3, 6 -> 4.
- i=3, value 1 (rank 1): prefix(0) = 0, insert rank 1. res[3] = 0.
- i=2, value 6 (rank 4): prefix(3) counts rank 1 -> 1, insert rank 4. res[2] = 1.
- i=1, value 2 (rank 2): prefix(1) = 1, insert rank 2. res[1] = 1.
- i=0, value 5 (rank 3): prefix(2) counts ranks 1 and 2 -> 2. res[0] = 2.
- Result [2, 1, 1, 0].

**Code:**
```python
import random
random.seed(46)

def count_smaller(nums):
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}      # compress to 1..k
    t = [0] * (len(ranks) + 1)
    def add(i):
        while i < len(t):
            t[i] += 1; i += i & -i
    def pre(i):
        s = 0
        while i > 0:
            s += t[i]; i -= i & -i
        return s
    res = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):        # right to left: the tree holds exactly nums[i+1:]
        res[i] = pre(ranks[nums[i]] - 1)          # strictly smaller ranks only
        add(ranks[nums[i]])
    return res

def brute(nums):
    return [sum(1 for j in range(i + 1, len(nums)) if nums[j] < nums[i]) for i in range(len(nums))]

assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
assert count_smaller([2, 2, 2]) == [0, 0, 0]
assert count_smaller([]) == []
print('examples ok')

for _ in range(600):
    nums = [random.randint(-4, 4) for _ in range(random.randint(0, 12))]
    assert count_smaller(nums) == brute(nums), nums
print('600 random arrays match the O(n^2) double loop')

assert count_smaller([7]) == [0]
assert count_smaller([3, 2, 1]) == [2, 1, 0]                 # descending
assert count_smaller([1, 2, 3]) == [0, 0, 0]                 # ascending
assert count_smaller([-10**9, 10**9, -10**9]) == [0, 1, 0]   # extremes, duplicates
# direction matters: scanning left to right and using the same query counts elements to the LEFT instead
def left_count(nums):
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}; t = [0] * (len(ranks) + 1); out = []
    for v in nums:
        i = ranks[v] - 1; s = 0
        while i > 0: s += t[i]; i -= i & -i
        out.append(s); i = ranks[v]
        while i < len(t): t[i] += 1; i += i & -i
    return out
print('left-to-right scan gives', left_count([5, 2, 6, 1]), 'not', count_smaller([5, 2, 6, 1]))
assert left_count([5, 2, 6, 1]) != [2, 1, 1, 0]
nums = [random.randint(-10**9, 10**9) for _ in range(10**5)]
r = count_smaller(nums); assert len(r) == 10**5 and all(0 <= x < 10**5 for x in r)
print('n = 10^5 ok')
print('first example:', count_smaller([5, 2, 6, 1]))
```

**Output (my run):**
```
examples ok
600 random arrays match the O(n^2) double loop
left-to-right scan gives [0, 0, 2, 0] not [2, 1, 1, 0]
n = 10^5 ok
first example: [2, 1, 1, 0]
```

**Edge cases:**
- Empty list: return [] (the tree has size 1 and is never touched).
- One element: [0].
- All equal: all zeros, since smaller is strict.
- Strictly descending: [n-1, ..., 0]; ascending: all zeros.
- Values up to +-10^9: compression makes the range irrelevant, and negatives need no special care.

**Follow-ups:**
- *How would "smaller or equal" change it?* Query `prefix(rank)` instead of `prefix(rank - 1)`.
- *Can I do it without compressing?* If values are bounded and small, index the tree by value directly; otherwise use a dynamic structure or compress.
- *Related problems?* Inversion counts, reverse pairs (Set C) and the merge-sort counting questions Part 13 Q17 and Part 13 Q47 are the same idea; Q25 here also uses a Fenwick tree.

**Common mistakes:**
- Scanning left to right and answering a different question.
- Querying `rank` (counts equal values) instead of `rank - 1`.
- Using the raw values as tree indices, which fails for negatives and for 10^9.
- A 0-indexed Fenwick tree (index 0 loops forever with `i & -i`).
- Inserting before querying, so every element counts itself.

### Q47 ⭐ 🔴 [Set A, Q5 of 5, 12 min, 30 pts] Delayed job scheduler with cancellation. Implement class `Scheduler(clock)` with `submit(job_id, delay, priority)` (the job becomes ready at time now + delay, delay >= 0; smaller `priority` numbers are more urgent; a job id is never submitted while a job with the same id is still pending, but an id may be reused after it was polled or cancelled; returns None), `cancel(job_id)` (True when a pending job was removed, else False) and `poll(limit)` which removes and returns, in order, up to `limit` pending jobs that are ready (ready time <= now). Order: smaller ready time first, then smaller priority, then earlier submission. Jobs that are not yet ready are never returned, and a poll with nothing ready returns []. Use a heap of (ready, priority, seq, job_id) and a dict job_id -> seq of live jobs: `cancel` deletes from the dict only (lazy deletion: Part 8 Q31) and `poll` discards heap entries whose seq no longer matches; tie keys follow Part 8 Q29. Submit O(log n), cancel O(1), poll O(k log n) amortised. Explain why the `seq` check (not just the id) is needed when an id is reused after cancel. The constructor's FIRST argument is `clock`, a zero-argument callable that returns the current time as an integer number of seconds; `init` holds the remaining constructor arguments, and ops are [time, method, [args]] with non-decreasing times: the checker sets the clock to `time` before each call. Read the time only through `clock()`, never from the `time` module. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a naive reference implementation on random operation sequences with an injected clock on small inputs. Example: init=[], ops=[[0, 'submit', ['a', 5, 2]], [0, 'submit', ['b', 5, 1]], [0, 'submit', ['c', 0, 9]], [0, 'poll', [5]], [4, 'poll', [5]], [5, 'cancel', ['b']], [5, 'poll', [1]], [5, 'submit', ['b', 0, 3]], [5, 'poll', [5]], [6, 'cancel', ['a']], [6, 'poll', [5]]] -> [null, null, null, ['c'], [], True, ['a'], null, ['b'], False, []].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Min-heap with lazy deletion for a delayed, prioritised job queue, driven by an injected clock.

**Say this first (1 line):** "Order is ready time, then priority, then submission order; I keep a heap of (ready, priority, seq, id) plus a dict id -> seq of live jobs, cancel only touches the dict, and poll throws away heap entries whose seq no longer matches."

**Brute force:** Keep a plain list of pending jobs. `poll` sorts the ready ones and takes `limit`; `cancel` filters the list. O(n log n) per poll and O(n) per cancel. That is my reference model for the random test.

**Optimal:**
- Rules, stated first: a job is ready when `ready <= now` (a job ready exactly now IS returned). Order: smaller ready time, then smaller priority number, then earlier submission (`seq`, a counter). Not-yet-ready jobs are never returned. Nothing ready gives `[]`.
- `submit` pushes `(now + delay, priority, seq, job_id)` and records `live[job_id] = seq`.
- `cancel` does `live.pop(job_id)`: True if the job was pending. The heap entry stays (lazy deletion, Part 8 Q31); tie keys follow Part 8 Q29.
- `poll(limit)`: while the heap top is ready and fewer than `limit` jobs are out, pop it; if `live.get(job_id) == seq` it is a real job, return it and delete it from `live`; otherwise it is stale and is silently discarded (stale entries do not use up the limit).
- Why `seq` and not just the id: cancel `a`, then submit `a` again with a later ready time. Two heap entries now carry the id `a`. An id-only check would let the OLD entry (ready earlier) return the NEW job too early; the output shows that failure. The `seq` check accepts only the entry of the current submission.
- Costs: `submit` O(log n); `cancel` O(1) (the stale entry is cleaned later, paid by the poll that meets it); `poll(k)` O(k log n) amortised, because each heap entry is popped at most once.
- Memory: cancelled entries linger until they reach the top. That is acceptable here; if cancels dominate, rebuild the heap when stale entries exceed half of it.
- Thread-safety as a concept only: `submit`, `cancel` and `poll` mutate the heap and the dict together, so a real system guards them with one lock or a single worker thread; polling workers would claim jobs under that lock.

**Complexity:** `submit` O(log n), `cancel` O(1), `poll` O(k log n) amortised over all calls; space O(n) including stale entries.

**Dry run:** the example.
- t=0: submit a (ready 5, prio 2, seq 1), b (ready 5, prio 1, seq 2), c (ready 0, prio 9, seq 3).
- t=0 `poll(5)`: top is c (ready 0 <= 0), returned. Next top is b (ready 5 > 0): stop. -> ['c'].
- t=4 `poll(5)`: top ready is 5 > 4 -> [].
- t=5 `cancel('b')`: removed from `live` -> True. `poll(1)`: top is b's entry (5, 1, 2): `live.get('b')` is None, so discard it; next is a (5, 2, 1), live matches -> ['a'], limit reached.
- t=5 `submit('b', 0, 3)` (seq 4, ready 5), `poll(5)` -> ['b'].
- t=6 `cancel('a')`: a was already polled -> False. `poll(5)` -> [].

**Code:**
```python
import heapq, random
random.seed(47)

class Scheduler:
    def __init__(self, clock):
        self.clock = clock
        self.heap = []                        # (ready, priority, seq, job_id)
        self.live = {}                        # job_id -> seq of the live submission
        self.seq = 0

    def submit(self, job_id, delay, priority):
        self.seq += 1
        self.live[job_id] = self.seq
        heapq.heappush(self.heap, (self.clock() + delay, priority, self.seq, job_id))

    def cancel(self, job_id):
        return self.live.pop(job_id, None) is not None     # lazy: the heap entry stays, poll skips it

    def poll(self, limit):
        now = self.clock(); out = []
        while self.heap and len(out) < limit and self.heap[0][0] <= now:
            ready, pr, seq, job_id = heapq.heappop(self.heap)
            if self.live.get(job_id) == seq:               # stale entries (cancelled / reused id) fail this test
                out.append(job_id); del self.live[job_id]
        return out

class Naive:
    def __init__(self, clock): self.clock = clock; self.jobs = []; self.seq = 0
    def submit(self, job_id, delay, priority):
        self.seq += 1; self.jobs.append((self.clock() + delay, priority, self.seq, job_id))
    def cancel(self, job_id):
        n = len(self.jobs); self.jobs = [j for j in self.jobs if j[3] != job_id]; return len(self.jobs) < n
    def poll(self, limit):
        now = self.clock(); ready = sorted(j for j in self.jobs if j[0] <= now)[:limit]
        for j in ready: self.jobs.remove(j)
        return [j[3] for j in ready]

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

def run(cls, ops):
    clk = Clock(); obj = cls(clk); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(obj, m)(*a))
    return out

ex = [[0, 'submit', ['a', 5, 2]], [0, 'submit', ['b', 5, 1]], [0, 'submit', ['c', 0, 9]], [0, 'poll', [5]], [4, 'poll', [5]],
      [5, 'cancel', ['b']], [5, 'poll', [1]], [5, 'submit', ['b', 0, 3]], [5, 'poll', [5]], [6, 'cancel', ['a']], [6, 'poll', [5]]]
got = run(Scheduler, ex)
assert got == [None, None, None, ['c'], [], True, ['a'], None, ['b'], False, []], got
print('example ->', got)

def gen_ops():                                # never submits an id that is still pending (checked with the naive model)
    clk = Clock(); probe = Naive(clk); pending = set(); ops = []; t = 0
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 3); clk.t = t; r = random.random()
        if r < .45:
            jid = 'j%d' % random.randint(1, 6)
            if jid in pending: continue
            a = [jid, random.randint(0, 5), random.randint(0, 3)]; probe.submit(*a); pending.add(jid); ops.append([t, 'submit', a])
        elif r < .7:
            a = ['j%d' % random.randint(1, 6)]
            if probe.cancel(*a): pending.discard(a[0])
            ops.append([t, 'cancel', a])
        else:
            a = [random.randint(1, 4)]
            for j in probe.poll(*a): pending.discard(j)
            ops.append([t, 'poll', a])
    return ops
for _ in range(500):
    ops = gen_ops()
    assert run(Scheduler, ops) == run(Naive, ops), ops
print('500 random sequences with an injected clock match the naive reference')

# ties: same ready time, then priority, then submission order; ready exactly at `now` is returned
tie = [[0, 'submit', ['x', 3, 1]], [0, 'submit', ['y', 3, 1]], [0, 'submit', ['z', 3, 0]], [3, 'poll', [10]]]
assert run(Scheduler, tie)[-1] == ['z', 'x', 'y']
assert run(Scheduler, [[0, 'poll', [3]], [0, 'cancel', ['q']], [0, 'submit', ['q', 1, 0]], [0, 'poll', [3]], [1, 'poll', [0]], [1, 'poll', [3]]]) == [[], False, None, [], [], ['q']]

# why seq, not just the id: cancel then resubmit the SAME id with a later ready time
class IdOnly(Scheduler):
    def poll(self, limit):
        now = self.clock(); out = []
        while self.heap and len(out) < limit and self.heap[0][0] <= now:
            ready, pr, seq, job_id = heapq.heappop(self.heap)
            if job_id in self.live: out.append(job_id); del self.live[job_id]
        return out
reuse = [[0, 'submit', ['a', 1, 0]], [0, 'cancel', ['a']], [0, 'submit', ['a', 9, 0]], [1, 'poll', [5]], [9, 'poll', [5]]]
print('seq check:', run(Scheduler, reuse)[-2:], ' id-only check:', run(IdOnly, reuse)[-2:])
assert run(Scheduler, reuse)[-2:] == [[], ['a']] and run(IdOnly, reuse)[-2:] == [['a'], []]
```

**Output (my run):**
```
example -> [None, None, None, ['c'], [], True, ['a'], None, ['b'], False, []]
500 random sequences with an injected clock match the naive reference
seq check: [[], ['a']]  id-only check: [['a'], []]
```

**Edge cases:**
- `poll(0)` returns [] without touching anything.
- `delay = 0`: ready immediately at the submit time.
- Ties on ready time and priority: the earlier submission goes first (the `seq` field also stops Python from comparing job ids).
- Cancel of an unknown or already polled id: False.
- Reusing an id after poll or cancel: allowed, handled by `seq`.
- Many cancelled jobs: stale entries are skipped without consuming `limit`.

**Follow-ups:**
- *What if cancels are frequent?* Count stale entries and rebuild the heap when they exceed the live ones, keeping memory O(live).
- *How would workers run this?* A worker loop calls `poll`, and when nothing is ready it sleeps until `heap[0][0] - now`; submit wakes it if the new job is earlier (a condition variable).
- *What if two schedulers share a store?* A real system needs a database or Redis sorted set with an atomic claim; that is system design, not this data-structure answer.
- *Scoring note (30 pts, split per the part header rubric):* 9 pts for stating the rules before coding (ready `<=` now, the three-key order, id reuse, empty poll); 9 pts for a correct solution that passes the example and a random operation-sequence check; 6 pts for complexity and the reason it holds (amortised poll, lazy cancel); 3 pts for the seeded edge cases (limit larger than ready jobs, cancel of unknown id, reuse after cancel); 3 pts for a crisp under-60-second summary. Partial: a correct sort-on-every-poll version with the rules stated earns about 18 to 20; missing the `seq` check loses most of the correctness points for id reuse.
- *How I would pace this (12 min):* 2 min stating rules and tie order, 2 min choosing heap plus dict, 5 min coding, 2 min tracing the example (especially the cancel-then-poll step), 1 min complexity and the lazy-deletion caveat.

**Common mistakes:**
- Checking only `job_id in live`, which breaks id reuse after a cancel.
- Reading time from the `time` module instead of the injected `clock()`.
- Counting stale pops against `limit`.
- Using `<` instead of `<=`, so a job ready exactly now is missed.
- Pushing without `seq` so equal keys compare job ids (or crash on mixed types).

### Q48 ⭐ 🔴 [Set B, Q5 of 5, 12 min, 30 pts] Fewest starting nodes to reach everything. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges`, a list of directed [u, v] pairs (0 <= len <= 2*10^5; repeats and self loops allowed). Choose the smallest set of start nodes so that every node is reachable from at least one chosen node. Return that smallest set as a sorted list, and when several smallest sets exist return the lexicographically smallest one (compare the sorted lists). Condense the graph with the strongly connected components of Q20: the answer needs exactly one node from every component that has NO incoming edge from another component (a source component), and the smallest node of each source component gives the lexicographically smallest set. Explain why a non-source component is never needed and why one node per source component is enough (Part 9 Q3 counts undirected components; here direction matters). O(n + m) with an iterative DFS. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an exhaustive oracle that tries all subsets in order of size and lexicographic order (n <= 8) on small inputs. Example: n=5, edges=[[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]] -> [0, 3]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> [0]; n=3, edges=[] -> [0, 1, 2].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Strongly connected components, then the condensation DAG: exactly one start per source component.

**Say this first (1 line):** "Condense the graph into SCCs; every component with no incoming edge from another component needs one start, every other component is reached for free, and the smallest node of each source component gives the lexicographically smallest answer."

**Brute force:** Try all subsets in order of size, then lexicographic order, BFS from each subset and stop at the first that reaches every node: O(2^n * (n + m)). Only for n <= 8, as the oracle.

**Optimal:**
- Compute SCCs with an iterative DFS (the Tarjan code of Q41 here; Kosaraju of Q20 works equally well). Directed reachability inside a component is mutual, so one start anywhere in a component reaches the whole component.
- A component with an incoming edge from another component is reachable from it, so a non-source component is never needed in a smallest set.
- A source component can only be reached by starting inside it, so one start per source component is required, and one start suffices. The minimum count is therefore the number of source components.
- Lexicographic tie-break: within a source component any node works; pick its smallest node. Sorting those picks gives the lexicographically smallest sorted list (a smaller pick in any component can only help).
- Mark `has_in[comp[v]] = True` for every edge u -> v with `comp[u] != comp[v]`; self loops and edges inside a component do not count. Part 9 Q3 counts undirected components; with directions, only source components count.

**Complexity:** Time O(n + m) (iterative Tarjan, one pass over the edges, one pass over the nodes); space O(n + m).

**Dry run:** n=5, edges 0->1, 1->0, 1->2, 3->2, 3->4.
- SCCs: {0, 1}, {2}, {3}, {4}.
- Edges that cross components: 1->2 and 3->2 give {2} an incoming edge; 3->4 gives {4} one. {0, 1} and {3} have none, so they are the sources.
- Smallest node of {0, 1} is 0, of {3} is 3. Answer [0, 3].

**Code:**
```python
import itertools, random
random.seed(48)

def min_starts(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n; stack = []; counter = 0; nc = 0
    for s in range(n):                        # iterative Tarjan, as in Q41
        if idx[s] != -1:
            continue
        idx[s] = low[s] = counter; counter += 1; stack.append(s); on[s] = True
        work = [(s, 0)]
        while work:
            u, i = work.pop()
            if i < len(g[u]):
                work.append((u, i + 1)); v = g[u][i]
                if idx[v] == -1:
                    idx[v] = low[v] = counter; counter += 1; stack.append(v); on[v] = True; work.append((v, 0))
                elif on[v]:
                    low[u] = min(low[u], idx[v])
            else:
                if low[u] == idx[u]:
                    while True:
                        w = stack.pop(); on[w] = False; comp[w] = nc
                        if w == u:
                            break
                    nc += 1
                if work:
                    p = work[-1][0]; low[p] = min(low[p], low[u])
    has_in = [False] * nc
    for u, v in edges:
        if comp[u] != comp[v]:
            has_in[comp[v]] = True            # this component receives an edge from another one
    smallest = [None] * nc
    for v in range(n):                        # ascending v: the first node seen is the component minimum
        if smallest[comp[v]] is None:
            smallest[comp[v]] = v
    return sorted(smallest[c] for c in range(nc) if not has_in[c])

def oracle(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    def covers(starts):
        seen = set(starts); q = list(starts)
        for u in q:
            for v in g[u]:
                if v not in seen: seen.add(v); q.append(v)
        return len(seen) == n
    for k in range(1, n + 1):                 # smaller sets first; combinations come out in lexicographic order
        for combo in itertools.combinations(range(n), k):
            if covers(combo): return list(combo)

assert min_starts(5, [[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]]) == [0, 3]
assert min_starts(3, [[0, 1], [1, 2], [2, 0]]) == [0]
assert min_starts(3, []) == [0, 1, 2]
print('examples ok')

for _ in range(800):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 14))]
    assert min_starts(n, edges) == oracle(n, edges), (n, edges)
print('800 random graphs match the exhaustive subset oracle')

assert min_starts(1, [[0, 0]]) == [0]
assert min_starts(4, [[3, 2], [2, 1], [1, 0]]) == [3]                    # path against the node order
assert min_starts(4, [[0, 1], [1, 0], [2, 3], [3, 2]]) == [0, 2]        # two cycles
assert min_starts(3, [[0, 2], [1, 2], [0, 2]]) == [0, 1]                 # repeated edges
N = 10**5
assert min_starts(N, [[i + 1, i] for i in range(N - 1)]) == [N - 1]
assert min_starts(N, [[i, (i + 1) % N] for i in range(N)]) == [0]
print('10^5 path and 10^5 cycle ok (iterative)')
print('first example:', min_starts(5, [[0, 1], [1, 0], [1, 2], [3, 2], [3, 4]]))
```

**Output (my run):**
```
examples ok
800 random graphs match the exhaustive subset oracle
10^5 path and 10^5 cycle ok (iterative)
first example: [0, 3]
```

**Edge cases:**
- No edges: every node is its own source, answer is all nodes in order.
- One big cycle: one component, answer [0].
- Self loops and repeated edges: ignored for the source test.
- A path against the numbering (3 -> 2 -> 1 -> 0): only [3].
- Several cycles with no links between them: one pick each, the smallest node.
- n = 10^5: iterative, no recursion.

**Follow-ups:**
- *Could I use a simpler method than SCC?* You still need to know which nodes can reach each other; counting nodes with in-degree 0 is wrong when a cycle is a source.
- *What if I wanted the largest reach with k starts?* That is a different (harder) problem; with the condensation it becomes a set-cover style question.
- *Scoring note (30 pts, split per the part header rubric):* 9 pts for saying out loud that components matter, that a source component needs exactly one start, that non-source ones are free, and the lexicographic rule; 9 pts for a correct iterative SCC plus source marking that passes the example and a random check; 6 pts for O(n + m) and why; 3 pts for the seeded edge cases (no edges, one cycle, self loops, repeats); 3 pts for the under-60-second summary. Partial: a correct in-degree-0 solution that ignores cycles earns about 12 to 15 once the cycle counterexample is pointed out.
- *How I would pace this (12 min):* 2 min on the SCC insight and tie rule, 7 min coding the iterative SCC and the source test, 2 min on the example, 1 min complexity.

**Common mistakes:**
- Counting nodes of in-degree 0, which misses cycle components that are sources.
- Counting the edges inside a component as incoming.
- Choosing an arbitrary node per source component instead of the smallest.
- Recursive DFS, which crashes on long paths.
- Forgetting isolated nodes (each is its own source).

### Q49 ⭐ 🔴 [Set C, Q2 of 4, 11 min, 25 pts] Order statistics on a dynamic multiset with a Fenwick tree. Implement class `OrderStats(max_value)` (1 <= max_value <= 10^6) storing a multiset of integers in [0, max_value], with `insert(x)` (returns None), `remove(x)` (removes ONE copy; returns True when a copy existed, else False), `count_le(x)` (the number of stored elements <= x; 0 for negative x and the full size for x >= max_value) and `kth(k)` (the k-th smallest element counting duplicates, 1-based, or -1 when k < 1 or k > size). Keep a Fenwick tree over the values shifted by +1. `kth` uses binary descent on the tree: start with the largest power of two <= n as `step`, and for each step try `pos + step`; if `t[pos + step] < k`, move there and subtract that count from k; the answer is the final `pos` (the value, because indices are shifted by one). All operations O(log max_value). Explain why the descent beats a binary search over `count_le` (O(log n) instead of O(log^2 n)) and why this is the order-statistics trick behind 'median of a changing multiset' (compare Part 8 Q17). Fenwick basics: Q10. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[10], ops=[['insert', [5]], ['insert', [3]], ['insert', [5]], ['insert', [9]], ['count_le', [5]], ['kth', [1]], ['kth', [3]], ['kth', [4]], ['kth', [5]], ['remove', [5]], ['remove', [7]], ['kth', [3]], ['count_le', [-1]], ['count_le', [10]]] -> [null, null, null, null, 3, 3, 5, 9, -1, True, False, 9, 0, 3].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Fenwick tree for order statistics over a value domain: count of elements <= x, and k-th smallest by binary descent.

**Say this first (1 line):** "A Fenwick tree of counts indexed by value gives `count_le` as a prefix sum, and the k-th smallest by descending the tree's power-of-two steps, so everything is O(log max_value) with no binary search on top."

**Brute force:** Keep a sorted list with `bisect.insort`: insert and remove O(n) (list shifting), `count_le` O(log n) with `bisect`, `kth` O(1). The naive reference in the code uses this; it is fine at small sizes but insert is O(n) at 10^6 distinct values.

**Optimal:**
- Values 0..max_value are shifted by +1 into positions 1..n (n = max_value + 1), because a Fenwick tree is 1-indexed. `t` holds the counts; `cnt[x]` keeps exact copies so `remove` can answer True/False.
- `insert(x)`: `cnt[x] += 1`, size += 1, Fenwick add 1 at x + 1. `remove(x)`: if `cnt[x] == 0` return False, else the reverse; True.
- `count_le(x)`: 0 if x < 0; otherwise the prefix sum up to `min(x, max_value) + 1` (so x >= max_value gives the full size).
- `kth(k)`: -1 if k < 1 or k > size. Otherwise `pos = 0`, `step` = largest power of two <= n; for each `step` going down by halves: if `pos + step <= n` and `t[pos + step] < k`, move `pos += step` and `k -= t[pos]`. At the end `pos` is the number of positions whose cumulative count stays below k, so position `pos + 1` holds the k-th element, whose value is `pos` (shift by one).
- Why descent beats binary search on `count_le`: a binary search needs O(log n) steps each costing an O(log n) prefix query, O(log^2 n). The descent reads one tree cell per step, O(log n), because a Fenwick cell already stores a power-of-two block sum.
- This is the order-statistics trick behind 'median of a changing multiset' (compare Part 8 Q17): the median is `kth((size + 1) // 2)`. Fenwick basics: Q10.
- Duplicates are counts, so the k-th smallest counts duplicates naturally.
- Thread-safety as a concept only: each call reads and writes `t`, `cnt` and `size`; a lock around all four methods is the simple answer.

**Complexity:** `insert`, `remove`, `count_le`, `kth` are all O(log max_value) time. Space O(max_value) for `t` and `cnt` (about 2 * 10^6 ints at the limit).

**Dry run:** max_value=10, so n = 11 and the largest power of two <= 11 is 8. Insert 5, 3, 5, 9: counts 3:1, 5:2, 9:1, size 4.
- `count_le(5)` = 1 + 2 = 3.
- `kth(1)`: step 8: t[8] covers values 0..7 = 3, not < 1, stay. Step 4: t[4] covers values 0..3 = 1, not < 1. Step 2: t[2] = 0 < 1, so pos = 2. Step 1: t[3] (value 2) = 0 < 1, so pos = 3. Answer 3.
- `kth(3)`: t[8] = 3 is not < 3; step 4: t[4] = 1 < 3, so pos = 4, k = 2; step 2: t[6] = 2 is not < 2; step 1: t[5] = 0 < 2, so pos = 5. Answer 5.
- `kth(4)`: t[8] = 3 < 4, so pos = 8, k = 1; step 4 overshoots (12 > 11); step 2: t[10] = 1 is not < 1; step 1: t[9] = 0 < 1, so pos = 9. Answer 9. `kth(5)` = -1.
- `remove(5)` True, `remove(7)` False, `kth(3)` = 9, `count_le(-1)` = 0, `count_le(10)` = 3.

**Code:**
```python
import bisect, random
random.seed(49)

class OrderStats:
    def __init__(self, max_value):
        self.n = max_value + 1                # values 0..max_value live at tree positions 1..n
        self.t = [0] * (self.n + 1)
        self.cnt = [0] * self.n               # exact copy counts, so remove can answer True/False
        self.size = 0
        self.top = 1
        while self.top * 2 <= self.n:         # largest power of two <= n
            self.top *= 2

    def _add(self, i, d):
        while i <= self.n:
            self.t[i] += d; i += i & -i

    def insert(self, x):
        self.cnt[x] += 1; self.size += 1; self._add(x + 1, 1)

    def remove(self, x):
        if x < 0 or x >= self.n or self.cnt[x] == 0:
            return False
        self.cnt[x] -= 1; self.size -= 1; self._add(x + 1, -1)
        return True

    def count_le(self, x):
        if x < 0:
            return 0
        i = min(x, self.n - 1) + 1; s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i
        return s

    def kth(self, k):
        if k < 1 or k > self.size:
            return -1
        pos = 0; step = self.top
        while step:                           # binary descent: never overshoot the k-th element
            nxt = pos + step
            if nxt <= self.n and self.t[nxt] < k:
                pos = nxt; k -= self.t[nxt]
            step >>= 1
        return pos                            # position pos+1 holds the answer, i.e. the value pos

class Naive:
    def __init__(self, max_value): self.a = []
    def insert(self, x): bisect.insort(self.a, x)
    def remove(self, x):
        if x in self.a: self.a.remove(x); return True
        return False
    def count_le(self, x): return sum(1 for v in self.a if v <= x)
    def kth(self, k): return self.a[k - 1] if 1 <= k <= len(self.a) else -1

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ops = [['insert', [5]], ['insert', [3]], ['insert', [5]], ['insert', [9]], ['count_le', [5]], ['kth', [1]], ['kth', [3]], ['kth', [4]],
       ['kth', [5]], ['remove', [5]], ['remove', [7]], ['kth', [3]], ['count_le', [-1]], ['count_le', [10]]]
got = run(OrderStats, [10], ops)
assert got == [None, None, None, None, 3, 3, 5, 9, -1, True, False, 9, 0, 3], got
print('example ->', got)

for _ in range(500):
    mv = random.randint(1, 12)
    ops = []
    for _ in range(random.randint(0, 40)):
        r = random.random()
        if r < .3: ops.append(['insert', [random.randint(0, mv)]])
        elif r < .45: ops.append(['remove', [random.randint(0, mv)]])
        elif r < .7: ops.append(['count_le', [random.randint(-2, mv + 2)]])
        else: ops.append(['kth', [random.randint(-1, 12)]])
    assert run(OrderStats, [mv], ops) == run(Naive, [mv], ops), (mv, ops)
print('500 random operation sequences match the naive reference (max_value 1..12)')

assert run(OrderStats, [1], [['kth', [1]], ['insert', [0]], ['kth', [1]], ['remove', [0]], ['remove', [0]], ['count_le', [5]]]) == [-1, None, 0, True, False, 0]
assert run(OrderStats, [8], [['insert', [8]], ['insert', [0]], ['kth', [2]], ['count_le', [100]]]) == [None, None, 8, 2]   # n = 9, not a power of two
M = 10**6
o = OrderStats(M)
vals = [random.randint(0, M) for _ in range(20000)]
for v in vals: o.insert(v)
s = sorted(vals)
assert all(o.kth(k) == s[k - 1] for k in (1, 2, 777, 10000, 20000)) and o.count_le(M) == 20000
print('max_value = 10^6 with 20000 inserts ok')
```

**Output (my run):**
```
example -> [None, None, None, None, 3, 3, 5, 9, -1, True, False, 9, 0, 3]
500 random operation sequences match the naive reference (max_value 1..12)
max_value = 10^6 with 20000 inserts ok
```

**Edge cases:**
- Empty structure: `kth` returns -1, `count_le` returns 0.
- `max_value = 1` or a value domain whose n is not a power of two (the `pos + step <= n` guard).
- Values 0 and max_value (the shifted positions 1 and n).
- `count_le` with x below 0 or above max_value.
- `remove` of a value never inserted, or removed twice: False and no change.
- k = 0 or negative: -1.

**Follow-ups:**
- *What if values are not small integers?* Compress offline (Q17) if all values are known; otherwise use a balanced tree or a sorted-list structure.
- *How do I get the median?* `kth((size + 1) // 2)` (lower median); for an even size average two `kth` calls.
- *Why keep `cnt` besides the tree?* To know whether a removal is legal in O(1) (the tree alone would need a point query).
- *Scoring note (25 pts, split per the part header rubric):* about 7.5 pts for stating the rules (shift by one, duplicates counted, `kth` bounds, `count_le` clamps); 7.5 pts for a correct solution that passes the example and a random operation-sequence check; 5 pts for complexity and the reason the descent is O(log n); 2.5 pts for edge cases (empty, out-of-range x, double remove); 2.5 pts for the crisp summary. Partial: a `bisect.insort` list with correct rules earns roughly 15 of 25; a Fenwick tree with binary search over `count_le` earns about 20.
- *How I would pace this (11 min):* 2 min on rules and the +1 shift, 5 min coding the tree and `kth`, 2 min tracing one `kth`, 2 min on complexity and the descent argument.

**Common mistakes:**
- Forgetting the +1 shift, so value 0 loops forever (`0 & -0 = 0`).
- Not guarding `pos + step <= n` in the descent.
- Returning `pos + 1` instead of `pos` from `kth`.
- Letting `remove` go negative when the value is absent.
- Using `max_value` instead of `max_value + 1` for the tree size.

### Q50 ⭐ 🔴 [Set C, Q4 of 4, 13 min, 30 pts] Maximum overlap after every booking (My Calendar III). `bookings` is a list of up to 400 [start, end) pairs with 0 <= start < end <= 10^9, HALF-OPEN: two bookings that only touch (one ends exactly where the next starts) do not overlap. Return a list with one integer per booking: after adding bookings[0..i], the largest number of bookings that cover a single moment. Offline solution: compress all endpoints (Q17) into elementary cells [xs[k], xs[k+1]), then use a segment tree with lazy range add and global maximum (Q44; the root max is the answer; here `mx[o] = max(children) + lazy[o]` needs no push-down). O(n log n) overall. Compare with the difference-array idea of Part 13 Q4 (which needs small coordinates) and with the sweep of Part 8 Q7 (one answer for the whole set, not after every insert). In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that recomputes the maximum overlap from scratch after every booking on small inputs. Example: bookings=[[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]] -> [1, 1, 2, 3, 3, 3]; bookings=[[0, 5], [5, 10], [0, 10]] -> [1, 1, 2].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution
**Pattern:** Coordinate compression plus a segment tree with lazy range add and a global maximum (My Calendar III, offline).

**Say this first (1 line):** "Bookings are half-open, so I compress all endpoints into elementary cells [xs[k], xs[k+1]) and add one to the cells a booking covers; the answer after each booking is the maximum over all cells, which the tree keeps at the root."

**Brute force:** After every booking, recompute the maximum overlap from scratch: for each endpoint of the bookings so far, count how many bookings contain it. O(n^2) per booking, O(n^3) total; at n = 400 that is already heavy, but it is a clean oracle.

**Optimal:**
- Half-open rule: [s, e) covers moment x when `s <= x < e`, so bookings that only touch (one ends where the next starts) do not overlap. In cells, booking [s, e) covers exactly the cells with indices `pos[s] .. pos[e] - 1`.
- Compress the sorted distinct endpoints `xs`; there are `m = len(xs) - 1` cells. Maximum overlap always occurs on a whole cell, since coverage only changes at endpoints.
- Segment tree over the m cells with lazy add and no push-down: `mx[o]` is the maximum inside o INCLUDING the tag stored at o, `lz[o]` is the add applied to the whole of o. A fully covered node does `mx += 1; lz += 1`. A partly covered node recurses and sets `mx[o] = max(mx[left], mx[right]) + lz[o]`. The root's `mx` is the answer after each booking (Q44 has the push-down version).
- Offline is fine because all bookings are known up front (the list is given). For an online version you would need a dynamic or sorted-list structure (a sorted dictionary of boundary counts).
- Compare: the difference-array idea of Part 13 Q4 needs small coordinates (here they reach 10^9, hence compression); the sweep of Part 8 Q7 gives one answer for the whole set, not an answer after every insert.

**Complexity:** Sorting the endpoints O(n log n); each booking's range add is O(log n); total O(n log n) for n <= 400. Space O(n) for `xs`, the map, and 4m for the tree arrays. Recursion depth about log2(800) < 10.

**Dry run:** bookings [10,20), [50,60), [10,40), [5,15), [5,10), [25,55).
- Endpoints sorted: 5, 10, 15, 20, 25, 40, 50, 55, 60 give 8 cells: 0 = [5,10), 1 = [10,15), 2 = [15,20), 3 = [20,25), 4 = [25,40), 5 = [40,50), 6 = [50,55), 7 = [55,60).
- [10,20) covers cells 1..2: max 1. [50,60) covers cells 6..7: max 1.
- [10,40) covers cells 1..4: cells 1 and 2 reach 2: max 2.
- [5,15) covers cells 0..1: cell 1 reaches 3: max 3.
- [5,10) covers cell 0 (now 2): max stays 3.
- [25,55) covers cells 4..6: cell 4 is 2, cell 5 is 1, cell 6 is 2; max stays 3.
- Result [1, 1, 2, 3, 3, 3].

**Code:**
```python
import random
random.seed(50)

def calendar_k(bookings):
    xs = sorted({x for s, e in bookings for x in (s, e)})
    pos = {x: i for i, x in enumerate(xs)}
    m = len(xs) - 1                           # elementary cells [xs[k], xs[k+1])
    mx = [0] * (4 * m); lz = [0] * (4 * m)    # mx[o] = best overlap inside o, INCLUDING o's own lz

    def add(o, lo, hi, l, r):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            mx[o] += 1; lz[o] += 1; return
        mid = (lo + hi) // 2
        add(2 * o, lo, mid, l, r); add(2 * o + 1, mid + 1, hi, l, r)
        mx[o] = max(mx[2 * o], mx[2 * o + 1]) + lz[o]     # no push-down: the tag stays here

    out = []
    for s, e in bookings:
        add(1, 0, m - 1, pos[s], pos[e] - 1)  # cells from s up to (not including) e
        out.append(mx[1])
    return out

def oracle(bookings):                         # recompute from scratch after every booking
    out = []
    for k in range(1, len(bookings) + 1):
        pts = sorted({x for s, e in bookings[:k] for x in (s, e)})
        out.append(max(sum(1 for s, e in bookings[:k] if s <= x < e) for x in pts))
    return out

assert calendar_k([[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]) == [1, 1, 2, 3, 3, 3]
assert calendar_k([[0, 5], [5, 10], [0, 10]]) == [1, 1, 2]
print('examples ok')

for _ in range(600):
    n = random.randint(1, 10)
    bk = []
    for _ in range(n):
        s = random.randint(0, 14); bk.append([s, random.randint(s + 1, 15)])
    assert calendar_k(bk) == oracle(bk), bk
print('600 random booking lists match the recompute-from-scratch oracle')

assert calendar_k([[0, 1]]) == [1]
assert calendar_k([[3, 7]] * 4) == [1, 2, 3, 4]                       # identical bookings
assert calendar_k([[0, 5], [5, 10], [10, 15]]) == [1, 1, 1]           # touching never overlaps
assert calendar_k([[0, 10**9], [0, 1], [10**9 - 1, 10**9]]) == [1, 2, 2]
bk = [[random.randint(0, 5 * 10**8), 0] for _ in range(400)]
for b in bk: b[1] = b[0] + random.randint(1, 5 * 10**8)
res = calendar_k(bk)
assert res == oracle(bk) and res == sorted(res)
print('400 bookings with endpoints up to 10^9 ok; answers never decrease, final max', res[-1])
print('first example:', calendar_k([[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]))
```

**Output (my run):**
```
examples ok
600 random booking lists match the recompute-from-scratch oracle
400 bookings with endpoints up to 10^9 ok; answers never decrease, final max 208
first example: [1, 1, 2, 3, 3, 3]
```

**Edge cases:**
- One booking: [1].
- Identical bookings repeated: the answer grows by one each time.
- Touching bookings ([0,5), [5,10), [10,15)): never overlap, answers stay 1.
- A booking [0, 10^9) with tiny ones inside: compression handles the span.
- The output is never decreasing (adding a booking cannot reduce a maximum).
- Duplicate endpoints: `set` collapses them, so every booking maps to valid cell indices (`pos[e] - 1 >= pos[s]` because s < e).

**Follow-ups:**
- *Why no push-down is needed?* Only a global maximum is queried, never a partial range, so the tag can stay on the node; each node's `mx` already includes its own tag, and ancestors add their tags on the way up.
- *What if bookings arrive online (unknown in advance)?* Use a dynamic segment tree over [0, 10^9] (nodes created on demand, O(log 10^9) per booking), or a sorted map of boundary deltas with an O(n) scan.
- *What changes for closed intervals?* Make the end exclusive by using `e + 1`, or compress with the closed convention; state the choice first.
- *Scoring note (30 pts, split per the part header rubric):* 9 pts for stating the half-open rule, the cell model, and that the answer is a maximum over cells; 9 pts for a correct solution that passes the examples and a random check against the recompute oracle; 6 pts for complexity and the reason compression plus lazy tags give O(n log n); 3 pts for the seeded edge cases (touching bookings, identical bookings, single booking); 3 pts for the crisp summary. Partial: the O(n^2) per-insert sweep with correct half-open handling earns roughly 18 of 30, and a difference array over raw coordinates scores low because coordinates reach 10^9.
- *How I would pace this (13 min):* 3 min on the boundary rule and the cell model, 6 min coding the compressed lazy tree, 2 min on the dry run, 2 min on complexity and the offline caveat.

**Common mistakes:**
- Adding to cells `pos[s] .. pos[e]` (closed) so touching bookings falsely overlap.
- Treating each endpoint as a point instead of a cell between endpoints.
- Mixing up the tree size: `m = len(xs) - 1` cells, not `len(xs)`.
- Forgetting `+ lz[o]` when recomputing `mx[o]` without push-down.
- Using a difference array over raw coordinates up to 10^9.
