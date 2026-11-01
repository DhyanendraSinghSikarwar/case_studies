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
