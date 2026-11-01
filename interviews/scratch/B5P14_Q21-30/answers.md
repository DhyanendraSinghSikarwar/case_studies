# Book 5 Part 14: answers to Q21-Q30 (Wave B agent)

### Q21 ⭐⭐ 🟡 Lexicographically smallest topological order. `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` a list of [a, b] meaning a must come before b (0 <= len <= 2*10^5; repeats allowed). Return the topological order that is smallest when compared as a list (the first node as small as possible, then the second, and so on), or [] when a cycle makes any order impossible. Kahn's algorithm with a min-heap of the nodes whose in-degree is 0 (a plain FIFO queue gives a valid order but not the smallest); O((n + m) log n). Explain why taking the smallest available node at each step is optimal here (the choice set is exactly the available nodes) and why it is NOT the right rule for 'put label 0 as early as possible, then label 1, and so on' (for that goal reverse the graph, take the LARGEST available node each time, and reverse the result). Part 9 Q9 gives any valid order and Part 9 Q33 builds the order from word constraints; this question fixes the tie rule. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that tries all permutations in lexicographic order for n <= 6 and keeps the first valid one on small inputs. Example: n=4, edges=[[3, 0], [3, 1], [1, 2]] -> [3, 0, 1, 2]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> []; n=3, edges=[] -> [0, 1, 2].
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** Topological sort (Kahn) with a min-heap as the ready set. The tie rule is the whole question.

**Say this first (1 line):** "Kahn's algorithm, but the ready set is a min-heap, so each step takes the smallest node with in-degree 0; a cycle shows up as fewer than n nodes output."

**Brute force:**
- Try all n! permutations in lexicographic order and keep the first that respects every edge. O(n! * (n + m)). It is my oracle for n <= 6.

**Optimal:**
- Count in-degrees (repeated edges count twice and are decremented twice, so it stays consistent).
- Put every in-degree-0 node in a min-heap. Pop the smallest, append it, decrement its neighbours, push any that reach 0.
- If the output has fewer than n nodes, a cycle blocks the rest: return [].
- Why smallest-first is optimal: the first element of any valid order must be an available node (in-degree 0). So the smallest possible first element is the smallest available node. After removing it the rest is the same problem on the residual graph, and its choice set is again exactly its available nodes. A FIFO queue is valid but not smallest.
- Why it is NOT the rule for "label 0 as early as possible, then label 1, ...": that goal compares the position vector (pos[0], pos[1], ...), not the order list. Example n=3, edge 2 -> 0: smallest-first gives [1, 2, 0] (label 0 at position 2) but [2, 0, 1] puts label 0 at position 1. The fix: reverse the graph, take the LARGEST available node each time, reverse the result. The code checks both rules against brute force.

**Complexity:**
- Time O((n + m) log n): each node is pushed and popped once (log n each), each edge decrements once.
- Space O(n + m) for adjacency lists, in-degrees and heap.
- Iterative, so n = 10^5 is no recursion problem.

**Dry run:** n=4, edges 3->0, 3->1, 1->2.
- in-degrees: 0:1, 1:1, 2:1, 3:0. Heap [3].
- Pop 3, order [3]. 0 and 1 drop to 0, heap [0, 1].
- Pop 0, order [3, 0]. No out-edges.
- Pop 1, order [3, 0, 1]. Node 2 drops to 0, push.
- Pop 2. Order [3, 0, 1, 2], length 4 = n, so return it.
- Cycle example 0->1->2->0: no node has in-degree 0, heap empty at the start, output length 0 != 3, return [].

**Code:**
```python
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
```

**Output (my run):**
```
examples: [3, 0, 1, 2] [] [0, 1, 2]
smallest-first: [1, 2, 0]  label-0-early (brute): [2, 0, 1]  reverse+largest: [2, 0, 1]
random cross-check ok: 600 cases (n <= 6), both rules
n = 10^5 chain and fan ok
```

**Edge cases:**
- No edges: [0, 1, ..., n-1]. n = 1: [0].
- A self loop (a, a) is a cycle: [].
- Repeated edges: harmless as shown. A cycle in only part of the graph still returns [] (the whole answer is empty, not a partial order).
- Edge endpoints are within 0..n-1; isolated nodes are just ready from the start.

**Follow-ups:**
- Lexicographically smallest for a different tie rule, say the largest label first? Use a max-heap (push negatives in Python).
- Why not DFS? A DFS finish-time order gives a valid order but not the smallest one without extra work; Kahn with a heap is the natural fit. Part 9 Q9 has the any-order version and Part 9 Q33 builds the order from word constraints.
- Is the order unique? Only when the graph has a Hamiltonian path in the DAG: every step has exactly one ready node.

**Common mistakes:**
- Using a deque and calling it "smallest".
- Applying smallest-first to the "label 0 earliest" goal.
- Forgetting the cycle check (output shorter than n).
- Using `heapq` on a list that is not heapified after building it from a comprehension.

---

### Q22 ⭐⭐ 🟡 Cheapest path with one half-price edge. `n` nodes 0..n-1 (2 <= n <= 10^4) and `edges`, a list of directed [u, v, w] with integer cost 1 <= w <= 10^6 (0 <= len <= 5*10^4). Travel from node 0 to node n-1. You hold ONE coupon that you may use on at most one edge of your path, making that edge cost w // 2 (integer floor division). Return the minimum total cost, or -1 when n-1 is unreachable. Run Dijkstra on the layered state (node, coupon_used in {0, 1}) with a heap and lazy stale-entry skipping: the answer is min(dist[n-1][0], dist[n-1][1]). Say why a plain Dijkstra on the original graph cannot answer it, why positive weights keep the best walk simple, and why the same state-expansion idea handles 'at most k coupons' with k + 1 layers. The 'at most k stops' flight question is Part 9 Q34 and is not repeated. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a brute-force oracle that enumerates every simple path and subtracts the best single saving w - w // 2 on small inputs. Example: n=3, edges=[[0, 1, 10], [1, 2, 10], [0, 2, 25]] -> 12; n=3, edges=[[0, 1, 4]] -> -1; n=4, edges=[[0, 1, 1], [1, 3, 1], [0, 2, 3], [2, 3, 3]] -> 1.
**Asked at:** Advanced-graph interview guides (techinterview.org DFS advanced patterns and advanced graph algorithms posts, algocademy and Naukri Code360 Tarjan pages; search snippets only, not opened)

**Pattern:** Dijkstra on a layered state graph (node, coupons used). Positive weights, so a heap with lazy stale-entry skipping works.

**Say this first (1 line):** "State is (node, coupon_used); each edge can be taken at full price within a layer or at w // 2 moving from layer 0 to layer 1; the answer is the min of the two layers at n-1."

**Brute force:**
- Enumerate every simple path from 0 to n-1, sum its weights and subtract the best single saving w - w // 2 on that path. Exponential, my oracle for n <= 6.

**Optimal:**
- dist[v][c] = cheapest cost to reach v having used c coupons (c is 0 or 1). Start at (0, 0) with cost 0.
- From (u, c) with edge (v, w): go to (v, c) for cost w; if c == 0 also go to (v, 1) for cost w // 2.
- Pop from a heap of (cost, node, c); skip an entry if its cost is larger than the stored dist (stale).
- Answer min(dist[n-1][0], dist[n-1][1]), or -1 if both are infinite.
- Why plain Dijkstra on the original graph is not enough: the cheapest plain path is not always the cheapest with a coupon. In example 1 the plain best is 20 (via node 1), minus one saving of 5 gives 15, but the direct edge 25 with the coupon costs 12. The coupon changes which path wins, so the state has to remember it.
- Why a simple path is enough: weights are positive, and w // 2 >= 0, so deleting a cycle from a walk never raises the cost (if the coupon was inside the cycle the shortened walk can still use it, or not, at most the same cost). That is also why the brute-force oracle over simple paths is valid.
- "At most k coupons": the same idea with k + 1 layers; the code has `k_coupons` and checks it equals the one-coupon answer for k = 1 and plain Dijkstra for k = 0.

**Complexity:**
- 2n states and at most 2 * (edges) * 2 transitions. Each push is O(log) of the heap size.
- Time O((n + m) log(n + m)) (heap size is bounded by pushes, which is O(m)). Space O(n + m).
- For k coupons: states (k + 1) n, time O(k (n + m) log(...)).

**Dry run:** example 1, edges 0->1 (10), 1->2 (10), 0->2 (25), n=3.
- Start (0,0)=0. Edge 0->1: (1,0)=10 and with the coupon (1,1)=5. Edge 0->2: (2,0)=25, (2,1)=12.
- Pop (1,1)=5: edge 1->2 at full price gives 15, worse than (2,1)=12.
- Pop (1,0)=10: edge 1->2 gives (2,0)=20; the coupon gives (2,1)=10+5=15, no improvement.
- Answer min(20, 12) = 12.

**Code:**
```python
import heapq, random

def optimal(n, edges):
    """Dijkstra on states (node, coupon_used). Returns min cost 0 -> n-1 or -1."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [[INF, INF] for _ in range(n)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]                                  # (cost, node, used)
    while heap:
        d, u, c = heapq.heappop(heap)
        if d > dist[u][c]:
            continue                                    # stale entry
        for v, w in adj[u]:
            if d + w < dist[v][c]:
                dist[v][c] = d + w
                heapq.heappush(heap, (d + w, v, c))
            if c == 0 and d + w // 2 < dist[v][1]:      # spend the coupon on this edge
                dist[v][1] = d + w // 2
                heapq.heappush(heap, (d + w // 2, v, 1))
    ans = min(dist[n - 1])
    return -1 if ans == INF else ans

def brute(n, edges):
    """Enumerate every simple path 0 -> n-1; cost = sum - best single saving (w - w//2)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [float('inf')]
    seen = [False] * n
    def go(u, total, saving):
        if u == n - 1:
            best[0] = min(best[0], total - saving)
            return
        seen[u] = True
        for v, w in adj[u]:
            if not seen[v]:
                go(v, total + w, max(saving, w - w // 2))
        seen[u] = False
    go(0, 0, 0)
    return -1 if best[0] == float('inf') else best[0]

def k_coupons(n, edges, k):
    """Same idea with k + 1 layers: at most k half-price edges."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float('inf')
    dist = [[INF] * (k + 1) for _ in range(n)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        d, u, c = heapq.heappop(heap)
        if d > dist[u][c]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v][c]:
                dist[v][c] = d + w; heapq.heappush(heap, (d + w, v, c))
            if c < k and d + w // 2 < dist[v][c + 1]:
                dist[v][c + 1] = d + w // 2; heapq.heappush(heap, (d + w // 2, v, c + 1))
    ans = min(dist[n - 1])
    return -1 if ans == INF else ans

assert optimal(3, [[0, 1, 10], [1, 2, 10], [0, 2, 25]]) == 12
assert optimal(3, [[0, 1, 4]]) == -1
assert optimal(4, [[0, 1, 1], [1, 3, 1], [0, 2, 3], [2, 3, 3]]) == 1
print('examples:', optimal(3, [[0, 1, 10], [1, 2, 10], [0, 2, 25]]), optimal(3, [[0, 1, 4]]), optimal(4, [[0, 1, 1], [1, 3, 1], [0, 2, 3], [2, 3, 3]]))

# plain Dijkstra + 'best saving on that path' is wrong: the cheapest plain path is not always the cheapest with a coupon
n, e = 3, [[0, 1, 10], [1, 2, 10], [0, 2, 25]]          # plain best = 20 (via 1), with coupon 15 (via 1) vs 12 (direct)
plain = k_coupons(n, e, 0)                              # k = 0 layers is plain Dijkstra
assert plain == 20
print('plain shortest =', plain, ' with coupon =', optimal(n, e), '(direct edge 25 -> 12 beats 20 - 5 = 15)')
assert optimal(n, e) == 12 < plain - 5

# edge cases
assert optimal(2, [[0, 1, 1]]) == 0                     # coupon makes a weight-1 edge free (1 // 2 = 0)
assert optimal(2, [[1, 0, 5]]) == -1                    # wrong direction
assert optimal(2, [[0, 1, 7], [0, 1, 3]]) == 1          # parallel edges: 3 // 2 = 1

random.seed(22)
cases = 0
for _ in range(500):
    n = random.randint(2, 6)
    m = random.randint(0, 12)
    edges = [[random.randrange(n), random.randrange(n), random.randint(1, 20)] for _ in range(m)]
    assert optimal(n, edges) == brute(n, edges), (n, edges)
    assert k_coupons(n, edges, 1) == optimal(n, edges)
    assert k_coupons(n, edges, 3) == k_coupons(n, edges, 1) or k_coupons(n, edges, 3) < k_coupons(n, edges, 1)   # more coupons never hurt
    cases += 1
print('random cross-check ok:', cases, 'cases (n <= 6, w <= 20)')

# larger, just to be sure it runs: a 10^4 node chain with shortcuts
N = 10**4
big = [[i, i + 1, 10**6] for i in range(N - 1)] + [[i, i + 7, 5 * 10**6] for i in range(0, N - 7, 3)]
print('large run cost =', optimal(N, big))
```

**Output (my run):**
```
examples: 12 -1 1
plain shortest = 20  with coupon = 12 (direct edge 25 -> 12 beats 20 - 5 = 15)
random cross-check ok: 500 cases (n <= 6, w <= 20)
large run cost = 7774500000
```

**Edge cases:**
- Unreachable n-1: -1 (example 2). A weight-1 edge with the coupon is free (1 // 2 = 0).
- Parallel edges, edges into node 0 or out of n-1: harmless.
- Floor division, not a float: an odd 25 costs 12, not 12.5.
- The coupon is optional: min over both layers covers "do not use it".

**Follow-ups:**
- Can the coupon be used on a node instead of an edge? Same layering, different transition.
- What if weights can be 0? Still fine, stale-skipping handles ties; negative weights would break Dijkstra.
- Cheapest flights with at most k stops is Part 9 Q34: that constrains the number of edges, not a discount.

**Common mistakes:**
- Running plain Dijkstra and subtracting the largest saving on the plain shortest path (wrong, see example 1).
- Marking the coupon layer visited too early, so a cheaper path using the coupon later is missed.
- Using `w / 2` (float) instead of `w // 2`.
- Taking the coupon twice because the layer check was missing (`c == 0`).

---

### Q23 ⭐⭐ 🟡 Segment tree for range minimum with point updates. Implement class `MinSegTree(nums)` (1 <= len <= 10^5) with `update(i, v)` (set nums[i] = v, returns None) and `query(l, r)` (the minimum of nums[l..r], both ends included, 0 <= l <= r < len). Build a bottom-up array tree of size 2n: leaves at positions n..2n-1, node i holds min(tree[2i], tree[2i+1]); `update` walks up from the leaf, `query` shrinks the half-open range [l + n, r + n + 1) and takes a node whenever l is odd or r is odd. Both operations are O(log n), the build O(n) and the memory 2n. Explain why this bottom-up form works for any n (not only powers of two) for a commutative, associative operation such as min, sum or gcd, and when you need the recursive top-down form instead (lazy propagation: Q44, or a non-commutative merge). A plain Fenwick tree cannot answer min when values can be set to larger numbers (a prefix minimum cannot be undone, so there is no delta to add: explain in one line). The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[5, 3, 8, 1, 9, 2]], ops=[['query', [0, 5]], ['query', [2, 4]], ['update', [3, 10]], ['query', [0, 5]], ['query', [2, 4]], ['update', [0, 0]], ['query', [0, 1]]] -> [1, 1, null, 2, 8, null, 0]; init=[[4]], ops=[['query', [0, 0]], ['update', [0, -2]], ['query', [0, 0]]] -> [4, null, -2].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Bottom-up segment tree (array of size 2n) for a commutative, associative merge, here min.

**Say this first (1 line):** "Leaves live at positions n..2n-1, each inner node is the min of its two children, an update walks up from the leaf and a query takes whole nodes on the borders of a half-open range."

**Brute force:**
- Keep the plain list. `update` is O(1), `query` is min over a slice, O(n). My oracle (rescans the list on every query).

**Optimal:**
- Build: copy values into tree[n:], then for i from n-1 down to 1 set tree[i] = min(tree[2i], tree[2i+1]). O(n).
- Update: set the leaf, then i >>= 1 and recompute until the root. O(log n).
- Query [l, r] inclusive: use the half-open range [l + n, r + n + 1). While l < r: if l is odd (a right child) take tree[l] and move l right by one; if r is odd take tree[r - 1]; then halve both. O(log n).
- Why it works for any n, not only powers of two: the tree is not one balanced tree but a forest of perfect subtrees glued by the index arithmetic. Every node i >= 1 covers the leaves below it, and the loop only ever reads nodes that lie completely inside the range. Because min is commutative and associative, the order in which borders are collected does not matter, and a node that "wraps" (mixes the end and the start of the array) is never read by a query that stays inside [0, n). I verified it exhaustively for every (l, r) for n = 1..20.
- When you need the recursive top-down form: lazy propagation (Q44, pending updates need a place to sit on a node) or a non-commutative merge (e.g. string concatenation or matrix product), where the left-to-right order of the pieces matters. The bottom-up loop can be extended with a left and a right accumulator, but top-down is the safer interview answer.
- Why a Fenwick tree cannot do min with values that can grow: a BIT cell stores an aggregate that you update by adding a delta. For min there is no inverse: once a cell holds 1 you cannot "undo" it when that 1 is raised to 10. The code shows the prefix-min BIT staying at 1.

**Complexity:**
- Build O(n), `update` O(log n), `query` O(log n), memory 2n integers.
- Per operation: update walks at most log2(n) + 1 levels; query touches at most about 2 log2(n) nodes.
- Thread safety (concept only): a query reads several nodes and an update writes a whole root path, so a reader could see a half-updated path. One lock around update and query keeps it correct (or a readers-writer lock); a lock-free version needs versioned nodes.

**Dry run:** nums = [5, 3, 8, 1, 9, 2], n = 6, so leaves are tree[6..11] = 5, 3, 8, 1, 9, 2.
- Build: tree[5] = min(9, 2) = 2, tree[4] = min(8, 1) = 1, tree[3] = min(5, 3) = 3, tree[2] = min(1, 2) = 1, tree[1] = 1.
- query(2, 4): half-open [8, 11). l = 8 even; r = 11 odd so r = 10 and take tree[10] = 9. Halve: l = 4, r = 5. l even; r odd so r = 4 and take tree[4] = 1. Halve: l = 2, r = 2, stop. Answer min(9, 1) = 1.
- update(3, 10): leaf 9 becomes 10, tree[4] = min(8, 10) = 8, tree[2] = min(8, 2) = 2, tree[1] = min(2, 3) = 2. Then query(0, 5) = 2 and query(2, 4) = 8, as in the example.

**Code:**
```python
import random

class MinSegTree:
    """Bottom-up segment tree for range minimum with point assignment. tree[1] is the root, leaves at n..2n-1."""
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1):                 # O(n) build
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, v):                                # set nums[i] = v, O(log n)
        i += self.n
        self.tree[i] = v
        while i > 1:
            i >>= 1
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, l, r):                                 # min of nums[l..r] inclusive, O(log n)
        res = float('inf')
        l += self.n
        r += self.n + 1                                    # half-open [l, r)
        while l < r:
            if l & 1:                                      # l is a right child: take it, move right
                res = min(res, self.tree[l]); l += 1
            if r & 1:                                      # r is a right child: its left sibling r-1 is inside
                r -= 1; res = min(res, self.tree[r])
            l >>= 1; r >>= 1
        return res

class Naive:
    def __init__(self, nums): self.a = list(nums)
    def update(self, i, v): self.a[i] = v
    def query(self, l, r): return min(self.a[l:r + 1])

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ex1 = ([[5, 3, 8, 1, 9, 2]], [['query', [0, 5]], ['query', [2, 4]], ['update', [3, 10]], ['query', [0, 5]],
       ['query', [2, 4]], ['update', [0, 0]], ['query', [0, 1]]])
ex2 = ([[4]], [['query', [0, 0]], ['update', [0, -2]], ['query', [0, 0]]])
assert run(MinSegTree, *ex1) == [1, 1, None, 2, 8, None, 0]
assert run(MinSegTree, *ex2) == [4, None, -2]
print('example 1:', run(MinSegTree, *ex1))
print('example 2:', run(MinSegTree, *ex2))

# exhaustive check of every (l, r) for every length 1..20 (non powers of two included)
random.seed(23)
for n in range(1, 21):
    a = [random.randint(-9, 9) for _ in range(n)]
    t = MinSegTree(a)
    for l in range(n):
        for r in range(l, n):
            assert t.query(l, r) == min(a[l:r + 1]), (n, l, r)
print('exhaustive all (l, r), n = 1..20 ok (includes n = 3, 5, 6, 7 ... not powers of two)')

# the same bottom-up code with a different commutative, associative op (sum) also works for any n
class SumSeg(MinSegTree):
    def __init__(self, nums):
        self.n = len(nums); self.tree = [0] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1): self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    def update(self, i, v):
        i += self.n; self.tree[i] = v
        while i > 1: i >>= 1; self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    def query(self, l, r):
        res = 0; l += self.n; r += self.n + 1
        while l < r:
            if l & 1: res += self.tree[l]; l += 1
            if r & 1: r -= 1; res += self.tree[r]
            l >>= 1; r >>= 1
        return res
a = [random.randint(-9, 9) for _ in range(13)]
s = SumSeg(a)
assert all(s.query(l, r) == sum(a[l:r + 1]) for l in range(13) for r in range(l, 13))
print('same loop with + instead of min ok for n = 13')

# why a Fenwick tree cannot do min with raises: a 'prefix min' BIT only ever keeps the smaller value
class BadMinBIT:
    def __init__(self, n): self.t = [float('inf')] * (n + 1); self.n = n
    def set(self, i, v):                                   # i is 1-based
        while i <= self.n: self.t[i] = min(self.t[i], v); i += i & -i
    def prefix_min(self, i):
        res = float('inf')
        while i > 0: res = min(res, self.t[i]); i -= i & -i
        return res
b = BadMinBIT(4)
for i, v in enumerate([5, 3, 8, 1], 1): b.set(i, v)
b.set(4, 10)                                              # raise the 1 to 10: the stored 1 cannot be undone
print('BIT prefix_min after raising 1 -> 10:', b.prefix_min(4), '(true answer 3)')
assert b.prefix_min(4) == 1 != 3

# operation-sequence oracle against the naive version
cases = ops_total = 0
for _ in range(400):
    n = random.randint(1, 12)
    init = [[random.randint(-20, 20) for _ in range(n)]]
    ops = []
    for _ in range(random.randint(1, 40)):
        if random.random() < 0.4:
            ops.append(['update', [random.randrange(n), random.randint(-30, 30)]])
        else:
            l = random.randrange(n); r = random.randint(l, n - 1)
            ops.append(['query', [l, r]])
    assert run(MinSegTree, init, ops) == run(Naive, init, ops), (init, ops)
    cases += 1; ops_total += len(ops)
print('operation-sequence oracle ok:', cases, 'sequences,', ops_total, 'operations')
```

**Output (my run):**
```
example 1: [1, 1, None, 2, 8, None, 0]
example 2: [4, None, -2]
exhaustive all (l, r), n = 1..20 ok (includes n = 3, 5, 6, 7 ... not powers of two)
same loop with + instead of min ok for n = 13
BIT prefix_min after raising 1 -> 10: 1 (true answer 3)
operation-sequence oracle ok: 400 sequences, 7971 operations
```

**Edge cases:**
- n = 1: the tree is `[0, x]`, loop `while i > 1` does nothing, a query takes the leaf.
- Negative values and an update that makes a leaf larger (min must be recomputed, not min-ed in place).
- l == r, the full range, and n not a power of two (all in the exhaustive test).
- `query` is inclusive on both ends (the +1 builds the half-open range).

**Follow-ups:**
- Range sum instead? Same loop with `+` (the code does it); a BIT is shorter if there are no min/max queries (Q10, Q17).
- Static array, no updates? A sparse table answers min in O(1) (Q24).
- Range add? You need lazy propagation (Q44).

**Common mistakes:**
- Forgetting `r + n + 1` (querying [l, r) by accident).
- Mixing 0-based user indices with the 1-based heap layout of a recursive tree.
- Update that does `tree[i] = min(tree[i], v)`: only works for decreases.
- Starting the update loop at the root instead of the leaf.

---

### Q24 ⭐⭐ 🟡 Sparse table for static range minimum queries. `nums` has 1 <= len <= 10^5 integers (static, never updated) and `queries` is a list of up to 10^5 pairs [l, r] with 0 <= l <= r < len(nums). Return `[answers, entries]`: `answers` holds, for each query, `[minimum, index of its LEFTMOST occurrence inside l..r]`, and `entries` is the total number of cells stored in your table (level j stores one cell for every start i with i + 2^j <= n, for every level with 2^j <= n). Build `table[j][i]` = the best (value, index) pair for the block [i, i + 2^j) from two blocks of level j - 1 (compare (value, index) tuples so the leftmost index wins ties), and answer a query with k = floor(log2(r - l + 1)) from `table[k][l]` and `table[k][r - 2^k + 1]`: the two blocks overlap, which is harmless because min is idempotent (a sum would double count). Build O(n log n), query O(1); compare with the segment tree of Q23 (O(log n) query but supports updates) and say why Part 2 Q45 can also use a deque. In the answer include a dry run on the first example and a seeded random cross-check of your solution against slicing with min() and list.index on each query on small inputs. Example: nums=[5, 2, 4, 2, 7], queries=[[0, 4], [2, 4], [0, 0]] -> [[[2, 1], [2, 3], [5, 0]], 11]; nums=[3], queries=[[0, 0]] -> [[[3, 0]], 1].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Sparse table (binary lifting on blocks) for an idempotent operation on a static array.

**Say this first (1 line):** "Block j covers 2^j elements; I cover [l, r] with two possibly overlapping blocks of size 2^k, k = floor(log2(length)), which is fine for min because min(x, x) = x."

**Brute force:**
- For each query slice `nums[l:r+1]`, take `min` and `list.index`. O(n) per query, O(n * q) total. The oracle.

**Optimal:**
- Level 0 holds the pairs (value, index). Level j at start i holds min of the two level j-1 blocks at i and i + 2^(j-1).
- Compare (value, index) tuples: the smaller value wins, and on equal values the smaller index wins, so the leftmost occurrence survives every merge.
- Query: k = (r - l + 1).bit_length() - 1 (an exact floor of log2 without floats). Take min(table[k][l], table[k][r - 2^k + 1]).
- Overlap is harmless for min because it is idempotent. The code shows a sum would double count the middle.
- Entries: level j has n - 2^j + 1 cells, for every level with 2^j <= n. For the first example n = 5: 5 + 4 + 2 = 11. For n = 10^5 it is 1,568,946 cells (about n log2 n).
- Vs the segment tree of Q23: sparse table has O(1) query but O(n log n) build and memory and no updates. Segment tree has O(log n) query, O(n) build, supports updates.
- Part 2 Q45 can also use a monotonic deque: for sliding windows of a fixed size the deque gives all answers in O(n) total, without the n log n table.

**Complexity:**
- Build O(n log n) time and cells. Query O(1): two lookups and one comparison.
- Memory is the cost: about n log n tuples, so for large n it is heavy in Python; storing indices only (compare by nums[i], i) halves it.

**Dry run:** nums = [5, 2, 4, 2, 7].
- Level 0: (5,0) (2,1) (4,2) (2,3) (7,4).
- Level 1 (blocks of 2): (2,1) (2,1) (2,3) (2,3). Level 2 (blocks of 4): (2,1) (2,1). Total 5 + 4 + 2 = 11 cells.
- Query [2, 4]: length 3, k = 1. table[1][2] = (2,3) and table[1][4 - 2 + 1 = 3] = (2,3). Answer [2, 3].
- Query [0, 4]: length 5, k = 2. table[2][0] = (2,1), table[2][1] = (2,1). Answer [2, 1], the leftmost 2.

**Code:**
```python
import random

def build(nums):
    """table[j][i] = best (value, index) of block [i, i + 2^j). Tuples compare value first, then index: leftmost wins ties."""
    n = len(nums)
    table = [[(v, i) for i, v in enumerate(nums)]]
    j = 1
    while (1 << j) <= n:
        prev, half = table[-1], 1 << (j - 1)
        table.append([min(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)])
        j += 1
    return table

def optimal(nums, queries):
    table = build(nums)
    entries = sum(len(row) for row in table)
    answers = []
    for l, r in queries:
        k = (r - l + 1).bit_length() - 1                  # floor(log2(length)), no float log
        v, i = min(table[k][l], table[k][r - (1 << k) + 1])   # two overlapping blocks
        answers.append([v, i])
    return [answers, entries]

def brute(nums, queries):
    answers = []
    for l, r in queries:
        seg = nums[l:r + 1]
        m = min(seg)
        answers.append([m, l + seg.index(m)])             # list.index returns the leftmost
    n = len(nums)
    entries = sum(n - (1 << j) + 1 for j in range(n.bit_length()) if (1 << j) <= n)
    return [answers, entries]

assert optimal([5, 2, 4, 2, 7], [[0, 4], [2, 4], [0, 0]]) == [[[2, 1], [2, 3], [5, 0]], 11]
assert optimal([3], [[0, 0]]) == [[[3, 0]], 1]
print('examples:', optimal([5, 2, 4, 2, 7], [[0, 4], [2, 4], [0, 0]]), optimal([3], [[0, 0]]))

# the overlap is harmless for min (idempotent) but breaks a sum
nums = [1, 2, 3, 4, 5]
l, r = 0, 4; k = 2                                        # blocks [0,4) and [1,5) overlap on 1..3
wrong = sum(nums[0:4]) + sum(nums[1:5])
print('overlapping blocks: sum would be', wrong, 'instead of', sum(nums))
assert wrong != sum(nums)

# entries count: n log n growth; for n = 10^5
n = 10**5
cells = sum(n - (1 << j) + 1 for j in range(n.bit_length()) if (1 << j) <= n)
print('n = 10^5 table cells:', cells, '(about n * log2 n =', round(n * 16.6), ')')

random.seed(24)
for _ in range(600):
    n = random.randint(1, 40)
    nums = [random.randint(-5, 5) for _ in range(n)]      # small range = many ties
    qs = []
    for _ in range(30):
        l = random.randrange(n); qs.append([l, random.randint(l, n - 1)])
    assert optimal(nums, qs) == brute(nums, qs), (nums, qs)
print('random cross-check ok: 600 arrays x 30 queries, many duplicate minima')

# all equal: the leftmost index must be l itself
assert optimal([7] * 9, [[3, 8], [0, 8]])[0] == [[7, 3], [7, 0]]
big = [random.randint(0, 10**9) for _ in range(10**5)]
qs = [[l, random.randint(l, 10**5 - 1)] for l in (random.randrange(10**5) for _ in range(1000))]
assert optimal(big, qs) == brute(big, qs)
print('n = 10^5, 1000 random queries ok')
```

**Output (my run):**
```
examples: [[[2, 1], [2, 3], [5, 0]], 11] [[[3, 0]], 1]
overlapping blocks: sum would be 24 instead of 15
n = 10^5 table cells: 1568946 (about n * log2 n = 1660000 )
random cross-check ok: 600 arrays x 30 queries, many duplicate minima
n = 10^5, 1000 random queries ok
```

**Edge cases:**
- n = 1: one level, one cell, k = 0.
- Many ties (all equal): the leftmost index is l itself, tested.
- l == r: k = 0, both lookups are the same cell.
- Exact power-of-two lengths: the two blocks coincide.

**Follow-ups:**
- Which operations work? Any idempotent one: min, max, gcd, bitwise and/or. Not sum, product, xor.
- Can it handle updates? Not cheaply; a rebuild is O(n log n). Use Q23.
- Sum on a static array? Plain prefix sums are O(1) and O(n); no table needed.

**Common mistakes:**
- Using `math.log2` (float error at powers of two); use `bit_length`.
- Level j with the wrong cell count (reading past the end of the row).
- Comparing values only, losing the leftmost-index rule.
- Using it for sums, where the overlap double counts.

---

### Q25 ⭐⭐ 🟡 Count inversions with a Fenwick tree (BIT). `nums` has 0 <= len <= 10^5 integers (duplicates allowed, |value| <= 10^9). An inversion is a pair i < j with nums[i] > nums[j] (STRICTLY greater, equal values are not inversions). Return `[total, before_greater]` where `before_greater[j]` is the number of earlier elements strictly greater than nums[j] and `total` is their sum. Compress the values to ranks 1..m (Q17), scan left to right, and for each element add `j - prefix_count(rank[j])` before inserting its rank: `prefix_count` is a BIT prefix sum, update and query both use the loops `i += i & -i` and `i -= i & -i`. O(n log n) time, O(n) space. Compare with the merge-sort counter of Part 13 Q17 (same complexity, no extra per-element information) and say what changes for 'at most' instead of 'strictly'. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) double loop on small inputs. Example: nums=[3, 1, 2, 3, 1] -> [5, [0, 1, 1, 0, 3]]; nums=[] -> [0, []]; nums=[2, 2, 2] -> [0, [0, 0, 0]].
**Asked at:** Segment-tree and Fenwick-tree interview-pattern guides (several techinterview.org posts, a mintlify Fenwick snippet page, cp-algorithms sparse-table page, designgurus range-minimum-query lesson; search snippets only, not opened)

**Pattern:** Fenwick tree (BIT) over compressed ranks, scanning left to right and counting earlier elements.

**Say this first (1 line):** "Compress values to ranks, then for each element ask the BIT how many earlier elements have rank <= mine; the earlier elements strictly greater are j minus that."

**Brute force:**
- Double loop over all pairs i < j with nums[i] > nums[j]. O(n^2). The oracle.

**Optimal:**
- Rank the sorted distinct values 1..m (Q17). Equal values get the same rank.
- Scan j = 0..n-1. `prefix_count(rank)` is the number of earlier elements with rank <= rank[j]; the others, `j - prefix_count`, are strictly greater. That is before_greater[j].
- Then add one at position rank[j] (`i += i & -i`). Queries walk `i -= i & -i`.
- Equal values land in the prefix (rank <= mine), so they are not counted: that is the STRICT rule.
- What changes for other comparisons: counting earlier elements >= (non-strict inversions) uses prefix_count(rank - 1) in place of prefix_count(rank); counting earlier elements "at most" mine is just prefix_count(rank) itself. The code checks the `>=` variant against a double loop.
- Versus the merge-sort counter of Part 13 Q17: same O(n log n), but this gives the per-element counts (before_greater) for free, and extends to "count of smaller numbers after self" by scanning right to left.

**Complexity:**
- Time O(n log n): sorting for ranks plus n updates and n queries of O(log m).
- Space O(n) for the rank map and the tree.
- The total can reach n(n-1)/2 (about 5 * 10^9 for n = 10^5); Python ints do not overflow.

**Dry run:** nums = [3, 1, 2, 3, 1], ranks 1, 2, 3 equal the values.
- j=0, v=3: prefix(3) = 0, so 0 - 0 = 0. Insert 3.
- j=1, v=1: prefix(1) = 0, so 1 - 0 = 1. Insert 1.
- j=2, v=2: prefix(2) = 1 (the 1), so 2 - 1 = 1. Insert 2.
- j=3, v=3: prefix(3) = 3 (3, 1, 2), so 3 - 3 = 0. Insert 3.
- j=4, v=1: prefix(1) = 1, so 4 - 1 = 3 (the two 3s and the 2). Total 0+1+1+0+3 = 5.

**Code:**
```python
import random

def optimal(nums):
    """Fenwick tree over compressed ranks. Returns [total, before_greater]."""
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}   # coordinate compression to 1..m
    m = len(ranks)
    tree = [0] * (m + 1)
    before = []
    for j, v in enumerate(nums):
        r = ranks[v]
        cnt, i = 0, r
        while i > 0:                                       # prefix_count(r): earlier elements with rank <= r
            cnt += tree[i]; i -= i & -i
        before.append(j - cnt)                             # earlier elements strictly greater
        i = r
        while i <= m:                                      # insert rank r
            tree[i] += 1; i += i & -i
    return [sum(before), before]

def brute(nums):
    before = [sum(1 for i in range(j) if nums[i] > nums[j]) for j in range(len(nums))]
    return [sum(before), before]

def at_most_variant(nums):
    """Pairs i < j with nums[i] >= nums[j] ('at most' side of the comparison): use prefix_count(rank - 1)."""
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(ranks); tree = [0] * (m + 1); total = 0
    for j, v in enumerate(nums):
        r = ranks[v]; cnt, i = 0, r - 1                    # strictly smaller earlier elements
        while i > 0: cnt += tree[i]; i -= i & -i
        total += j - cnt                                   # earlier elements >= v
        i = r
        while i <= m: tree[i] += 1; i += i & -i
    return total

assert optimal([3, 1, 2, 3, 1]) == [5, [0, 1, 1, 0, 3]]
assert optimal([]) == [0, []]
assert optimal([2, 2, 2]) == [0, [0, 0, 0]]
print('examples:', optimal([3, 1, 2, 3, 1]), optimal([]), optimal([2, 2, 2]))

# dry run of the Fenwick loops on the first example ranks: values 1,2,3 -> ranks 1,2,3
print('ranks:', {v: i + 1 for i, v in enumerate(sorted(set([3, 1, 2, 3, 1])))})

# edge cases
assert optimal([5]) == [0, [0]]
assert optimal([3, 2, 1]) == [3, [0, 1, 2]]                # strictly decreasing: n(n-1)/2
assert optimal([-10**9, 10**9, -10**9]) == [1, [0, 0, 1]]
n = 1000
assert optimal(list(range(n, 0, -1)))[0] == n * (n - 1) // 2

random.seed(25)
for _ in range(800):
    n = random.randint(0, 25)
    nums = [random.randint(-6, 6) for _ in range(n)]
    assert optimal(nums) == brute(nums), nums
    assert at_most_variant(nums) == sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] >= nums[j])
print('random cross-check ok: 800 arrays (duplicates heavy), strict and >= variants')

big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
total = optimal(big)[0]
print('n = 10^5 random: total inversions =', total, '(expected about n^2/4 =', 10**10 // 4, ')')
```

**Output (my run):**
```
examples: [5, [0, 1, 1, 0, 3]] [0, []] [0, [0, 0, 0]]
ranks: {1: 1, 2: 2, 3: 3}
random cross-check ok: 800 arrays (duplicates heavy), strict and >= variants
n = 10^5 random: total inversions = 2500528204 (expected about n^2/4 = 2500000000 )
```

**Edge cases:**
- Empty array: [0, []]. Single element: [0, [0]].
- All equal: no inversions. Strictly decreasing: n(n-1)/2.
- Values up to 10^9 in magnitude: that is why we compress instead of indexing by value.
- Rank 0 does not exist: a BIT is 1-indexed, `i = 0` would loop forever on update.

**Follow-ups:**
- Count of smaller numbers after self? Scan right to left, query prefix(rank - 1).
- Reverse pairs with nums[i] > 2 * nums[j]? Compress both values and doubled values together, or use merge sort; it is Q36 in this part.
- Online stream? Compression needs all values first; with an unknown range use a balanced structure or an offline pass.

**Common mistakes:**
- Using `<=` so equal values count as inversions.
- A 0-based BIT index (infinite loop on `i & -i` with i = 0).
- Updating before querying, so an element counts against itself.
- Compressing with a dict built from a set (unordered), instead of sorted distinct values.

---

### Q26 ⭐⭐ 🟡 [Set A, Q2 of 5, 7 min, 15 pts] Underground system (average trip times). Implement class `UndergroundSystem()` with `checkIn(id, station, t)`, `checkOut(id, station, t)` and `getAverageTime(start, end)`. A customer id has at most one open trip at a time; `checkOut` always closes the open trip of that id; the trip duration is t_out - t_in. `getAverageTime` returns the average duration (a float, total / count) over all COMPLETED trips that started at `start` and ended at `end` (direction matters: A to B and B to A are different); it is only called after at least one such trip. Here t is an argument of the call (a trip timestamp), not a live clock. Keep a dict id -> (station, t) for open trips and a dict (start, end) -> [total, count] for finished ones; every operation O(1). Say what you would do when a customer id checks out without having checked in (the checker never does it) and why storing a running total and count beats storing every duration. Hash-map idioms: Part 1 Q39. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[], ops=[['checkIn', [45, 'A', 3]], ['checkIn', [32, 'A', 8]], ['checkOut', [45, 'B', 15]], ['checkOut', [32, 'B', 22]], ['getAverageTime', ['A', 'B']], ['checkIn', [10, 'B', 24]], ['checkOut', [10, 'A', 40]], ['getAverageTime', ['B', 'A']], ['checkIn', [45, 'A', 30]], ['checkOut', [45, 'B', 36]], ['getAverageTime', ['A', 'B']]] -> [null, null, null, null, 13.0, null, null, 16.0, null, null, 10.666666666666666].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Two hash maps: open trips keyed by customer id, running (total, count) keyed by (start, end).

**Say this first (1 line):** "Open trips in a dict by id, finished trips folded into a running total and count per (start, end) pair, so every call is O(1) and memory does not grow with the number of trips."

**Brute force:**
- Keep a list of every open check-in and every finished trip with its duration; each `getAverageTime` rescans the list and averages. O(trips) per query, O(trips) memory. My oracle.

**Optimal:**
- `checkIn(id, station, t)`: `open[id] = (station, t)`.
- `checkOut(id, station, t)`: pop the open record, `rec = done[(start, station)]`, add `t - t_in` to the total and 1 to the count.
- `getAverageTime(start, end)`: `total / count`.
- Rules stated up front: direction matters (A to B is not B to A); a customer has at most one open trip; the duration is t_out - t_in (t is an argument, no clock is read); the average is a float over completed trips only; open trips do not count.
- Check-out with no check-in (the checker never does it): I would raise an error (ValueError here) and change nothing, rather than invent a trip or ignore it silently. Asking about a pair with no completed trip also raises (KeyError), where a real service might return None.
- Why a running total and count beat storing every duration: the average needs only those two numbers, so memory is O(distinct pairs) rather than O(trips), and the query does not scan. The cost is that you cannot later ask for median or maximum.

**Complexity:**
- `checkIn`, `checkOut`, `getAverageTime`: O(1) expected each (dict operations).
- Space O(open trips + distinct (start, end) pairs).
- Thread safety (concept only): the check-out does a pop plus a read-modify-write of the (total, count) pair, so two threads could lose an update; guard each method with one lock, or one lock per (start, end) record plus an atomic pop of the open trip.

**Dry run:** the first example.
- checkIn 45 at A, t=3; checkIn 32 at A, t=8.
- checkOut 45 at B, t=15: trip 12, (A,B) = [12, 1]. checkOut 32 at B, t=22: trip 14, (A,B) = [26, 2]. Average 26 / 2 = 13.0.
- checkIn 10 at B, t=24; checkOut 10 at A, t=40: trip 16, (B,A) = [16, 1]. Average 16.0.
- checkIn 45 at A, t=30; checkOut at B, t=36: trip 6, (A,B) = [32, 3]. Average 32 / 3 = 10.666666666666666.

**Code:**
```python
import random

class UndergroundSystem:
    def __init__(self):
        self.open = {}                      # id -> (station, t_in)
        self.done = {}                      # (start, end) -> [total, count]

    def checkIn(self, id, station, t):      # O(1)
        assert id not in self.open, 'one open trip per id'
        self.open[id] = (station, t)

    def checkOut(self, id, station, t):     # O(1)
        if id not in self.open:             # my rule: reject loudly, never invent a trip
            raise ValueError('check-out without check-in: %r' % (id,))
        start, t_in = self.open.pop(id)
        rec = self.done.setdefault((start, station), [0, 0])
        rec[0] += t - t_in
        rec[1] += 1

    def getAverageTime(self, start, end):   # O(1)
        total, count = self.done[(start, end)]
        return total / count

class Naive:
    """Keeps every trip and every duration, rescans lists on each query."""
    def __init__(self): self.open = []; self.trips = []
    def checkIn(self, id, station, t): self.open.append((id, station, t))
    def checkOut(self, id, station, t):
        for k, (i, s, ti) in enumerate(self.open):
            if i == id:
                del self.open[k]; self.trips.append((s, station, t - ti)); return
    def getAverageTime(self, start, end):
        d = [x for s, e, x in self.trips if s == start and e == end]
        return sum(d) / len(d)

def run(cls, ops):
    obj = cls()
    return [getattr(obj, m)(*a) for m, a in ops]

ex = [['checkIn', [45, 'A', 3]], ['checkIn', [32, 'A', 8]], ['checkOut', [45, 'B', 15]], ['checkOut', [32, 'B', 22]],
      ['getAverageTime', ['A', 'B']], ['checkIn', [10, 'B', 24]], ['checkOut', [10, 'A', 40]],
      ['getAverageTime', ['B', 'A']], ['checkIn', [45, 'A', 30]], ['checkOut', [45, 'B', 36]],
      ['getAverageTime', ['A', 'B']]]
want = [None, None, None, None, 13.0, None, None, 16.0, None, None, 10.666666666666666]
assert run(UndergroundSystem, ex) == want
print('example:', run(UndergroundSystem, ex))

# direction matters; check-out without check-in is rejected
u = UndergroundSystem()
u.checkIn(1, 'X', 0); u.checkOut(1, 'Y', 5)
assert u.getAverageTime('X', 'Y') == 5.0
try:
    u.getAverageTime('Y', 'X'); raise SystemExit('should raise')
except KeyError:
    print('Y -> X has no completed trip: KeyError (the checker never asks)')
try:
    u.checkOut(99, 'Y', 7); raise SystemExit('should raise')
except ValueError as e:
    print('rejected:', e)
u.checkIn(1, 'X', 10); u.checkOut(1, 'X', 10)             # zero-length trip, same start and end is allowed
assert u.getAverageTime('X', 'X') == 0.0

# operation-sequence oracle: random valid call sequences
random.seed(26)
stations = ['A', 'B', 'C']
n_ops = 0
for _ in range(500):
    ops, open_ids, finished, t = [], {}, set(), 0
    for _ in range(random.randint(1, 40)):
        t += random.randint(0, 5)
        r = random.random()
        free = [i for i in range(6) if i not in open_ids]
        if r < 0.4 and free:
            i = random.choice(free); s = random.choice(stations); open_ids[i] = s
            ops.append(['checkIn', [i, s, t]])
        elif r < 0.75 and open_ids:
            i = random.choice(list(open_ids)); s = random.choice(stations)
            finished.add((open_ids.pop(i), s)); ops.append(['checkOut', [i, s, t]])
        elif finished:
            a, b = random.choice(sorted(finished)); ops.append(['getAverageTime', [a, b]])
    assert run(UndergroundSystem, ops) == run(Naive, ops), ops
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 sequences,', n_ops, 'operations')
```

**Output (my run):**
```
example: [None, None, None, None, 13.0, None, None, 16.0, None, None, 10.666666666666666]
Y -> X has no completed trip: KeyError (the checker never asks)
rejected: check-out without check-in: 99
operation-sequence oracle ok: 500 sequences, 9176 operations
```

**Edge cases:**
- Same id reused after a check-out: allowed (the open record was popped).
- Start equals end, or a zero-length trip: allowed, average can be 0.0.
- A pair with no completed trip: the checker never asks; mine raises KeyError.
- Float output: `total / count`, as the example 10.666666666666666 shows (not rounded).

**Follow-ups:**
- Pacing and scoring: this is Set A, Q2 of 5, 7 minutes, 15 points. How I would pace this: about 1 minute to state the rules and tie-breaks aloud, 3 minutes to code the two dicts, 1 minute to run the example, 1 minute for complexity and the missing-check-in answer, 1 minute spare for the 60-second summary. Scoring by the part header rubric (15 points): about 4.5 for stating the rules (direction, one open trip, t as an argument, completed trips only), 4.5 for a correct solution that passes the example and a random operation-sequence check, 3 for O(1) per call with the reason, 1.5 for the edge cases (missing check-in, A to B vs B to A), 1.5 for a crisp spoken summary. Partial credit: a version that stores every duration and rescans is correct but loses most of the complexity points.
- Median of trip times? Then you must keep durations (two heaps or a sorted list per pair).
- Many threads? One lock per method as above, stated as a concept.

**Common mistakes:**
- Keying finished trips by start only, or by an unordered pair.
- Integer division for the average.
- Not removing the open trip on check-out, so a later check-in of the same id fails.
- Counting trips that are still open.

---

### Q27 ⭐⭐ 🟡 [Set A, Q3 of 5, 9 min, 20 pts] Leaderboard. Implement class `Leaderboard()` with `addScore(player, score)` (add the positive integer `score` to the player's total, creating the player if new; returns None), `top(K)` (the sum of the K highest player totals; when there are fewer than K players, the sum of all of them) and `reset(player)` (remove the player entirely, as if never seen; does nothing for an unknown player; returns None). A player's total can be added to many times. Up to 10^5 operations and 10^4 players. A dict of totals plus `heapq.nlargest(K, totals.values())` gives O(P log K) per `top`; say when that is enough and what you would use if `top` were called far more often than `addScore` (a sorted structure or two heaps with lazy deletion as in Part 8 Q31, or a Fenwick tree over scores). Heap basics are Part 8 Q1 and the kth-largest idea Part 8 Q4. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[], ops=[['addScore', [1, 73]], ['addScore', [2, 56]], ['addScore', [3, 39]], ['addScore', [4, 51]], ['addScore', [5, 4]], ['top', [1]], ['reset', [1]], ['reset', [9]], ['addScore', [2, 51]], ['top', [3]], ['top', [10]]] -> [null, null, null, null, null, 73, null, null, null, 197, 201].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Hash map of totals plus a top-K selection with `heapq.nlargest`.

**Say this first (1 line):** "A dict of player totals; `top(K)` sums `heapq.nlargest(K, totals.values())`, O(P log K); I would switch the structure only if `top` is called far more often than `addScore`."

**Brute force:**
- Keep a log of every add and reset and recompute all totals and a full sort on each `top`. My oracle.

**Optimal:**
- `addScore(p, s)`: `totals[p] = totals.get(p, 0) + s`. O(1).
- `reset(p)`: `totals.pop(p, None)`. O(1). The player vanishes entirely, so a later add starts from 0. An unknown player is a no-op.
- `top(K)`: `sum(heapq.nlargest(K, totals.values()))`. With fewer than K players it just sums all of them. Ties do not matter: only the sum of the K largest totals is returned.
- When this is enough: a few hundred or thousand players and moderate `top` calls. With P = 10^4 players one `top` is about P log K comparisons, a few tens of thousands: fine for 10^5 mixed operations.
- When `top` dominates: keep a sorted list of (total, player) with `bisect.insort`: `top` becomes a slice of K items (O(K)), update O(P) for the list shift, which is a fast memmove. The code has this as `LeaderboardSorted` and checks it against the other two. Beyond that: a heap with lazy deletion (Part 8 Q31 idea: push new (total, player), skip entries whose total no longer matches) or a Fenwick tree over score values with counts, which gives top-K sums in O(log maxScore) if scores are bounded. Heap basics: Part 8 Q1; kth-largest: Part 8 Q4.

**Complexity:**
- `addScore` O(1), `reset` O(1), `top(K)` O(P log K) time and O(K) extra space; total memory O(P).
- Sorted-list variant: `addScore` and `reset` O(P) worst case (index lookup is O(log P), shifting is O(P)), `top` O(K).
- Thread safety (concept only): `top` iterates the dict while another thread may insert, which in CPython raises "dictionary changed size during iteration"; one lock around every method (or iterate over a snapshot taken under the lock).

**Dry run:** the first example.
- Adds give totals {1:73, 2:56, 3:39, 4:51, 5:4}. `top(1)` = 73.
- `reset(1)` removes player 1. `reset(9)` does nothing.
- `addScore(2, 51)`: player 2 becomes 107. `top(3)` = 107 + 51 + 39 = 197. `top(10)` (only 4 players) = 107 + 51 + 39 + 4 = 201.

**Code:**
```python
import heapq, random
from bisect import insort, bisect_left

class Leaderboard:
    def __init__(self):
        self.totals = {}

    def addScore(self, player, score):      # O(1)
        self.totals[player] = self.totals.get(player, 0) + score

    def top(self, K):                       # O(P log K): heapq.nlargest keeps a heap of size K
        return sum(heapq.nlargest(K, self.totals.values()))

    def reset(self, player):                # O(1); unknown player is a no-op
        self.totals.pop(player, None)

class LeaderboardSorted:
    """For top-heavy workloads: keep a sorted list of (total, player). addScore/reset O(P) (list insert), top O(K)."""
    def __init__(self):
        self.totals = {}; self.order = []
    def addScore(self, player, score):
        old = self.totals.get(player)
        if old is not None:
            del self.order[bisect_left(self.order, (old, player))]
        new = (old or 0) + score
        self.totals[player] = new
        insort(self.order, (new, player))
    def top(self, K):
        return sum(t for t, _ in self.order[max(0, len(self.order) - K):]) if K > 0 else 0
    def reset(self, player):
        old = self.totals.pop(player, None)
        if old is not None:
            del self.order[bisect_left(self.order, (old, player))]

class Naive:
    def __init__(self): self.log = []                      # every (player, score) ever added, plus resets
    def addScore(self, player, score): self.log.append(('add', player, score))
    def reset(self, player): self.log.append(('reset', player, 0))
    def top(self, K):
        tot = {}
        for kind, p, s in self.log:
            if kind == 'add': tot[p] = tot.get(p, 0) + s
            else: tot.pop(p, None)
        return sum(sorted(tot.values(), reverse=True)[:K])

def run(cls, ops):
    obj = cls()
    return [getattr(obj, m)(*a) for m, a in ops]

ex = [['addScore', [1, 73]], ['addScore', [2, 56]], ['addScore', [3, 39]], ['addScore', [4, 51]], ['addScore', [5, 4]],
      ['top', [1]], ['reset', [1]], ['reset', [9]], ['addScore', [2, 51]], ['top', [3]], ['top', [10]]]
want = [None, None, None, None, None, 73, None, None, None, 197, 201]
for cls in (Leaderboard, LeaderboardSorted, Naive):
    assert run(cls, ex) == want, cls
print('example:', run(Leaderboard, ex))

# edge cases: empty board, K larger than players, reset then re-add starts from zero
lb = Leaderboard()
assert lb.top(5) == 0
lb.addScore(7, 10); lb.reset(7); lb.addScore(7, 3)
assert lb.top(1) == 3
lb.addScore(8, 3)
assert lb.top(2) == 6 and lb.top(100) == 6                 # ties do not matter: only the sum is returned

random.seed(27)
n_ops = 0
for _ in range(500):
    ops = []
    for _ in range(random.randint(1, 50)):
        r = random.random()
        p = random.randint(1, 6)
        if r < 0.5: ops.append(['addScore', [p, random.randint(1, 20)]])
        elif r < 0.65: ops.append(['reset', [p]])
        else: ops.append(['top', [random.randint(1, 8)]])
    a = run(Leaderboard, ops)
    assert a == run(Naive, ops) == run(LeaderboardSorted, ops), ops
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 sequences,', n_ops, 'operations, 3 implementations agree')
```

**Output (my run):**
```
example: [None, None, None, None, None, 73, None, None, None, 197, 201]
operation-sequence oracle ok: 500 sequences, 12398 operations, 3 implementations agree
```

**Edge cases:**
- Empty board: `top(K)` is 0.
- K larger than the number of players: sum of all.
- Reset then re-add: totals restart from the new score.
- Repeated adds to the same player accumulate. Equal totals are fine.

**Follow-ups:**
- Pacing and scoring: this is Set A, Q3 of 5, 9 minutes, 20 points. How I would pace this: 2 minutes to state the rules (reset deletes, fewer than K players, ties irrelevant), 3 minutes to code the dict version, 2 minutes to run the example and the oracle idea, 1 minute for complexity and the "when top is hot" alternative, 1 minute spare for the summary. Scoring by the part header rubric (20 points): about 6 for stating the rules out loud, 6 for a correct solution that passes the example and a random operation-sequence check, 4 for the stated complexity and why, 2 for the edge cases, 2 for the spoken summary. Partial credit: a full sort on each `top` is correct and earns most of the correctness points but loses on complexity.
- Return the rank of a player? Needs an order-statistics structure (sorted list with bisect, or a Fenwick tree).
- Distributed leaderboard? Out of scope here: that is a systems question (Book 4).

**Common mistakes:**
- `reset` that sets the score to 0 but leaves the player in the table (it would then still count in `top` and in the player count).
- `nlargest` on the dict instead of `.values()`.
- Raising KeyError on an unknown reset.
- Sorting the full list on every `top` and claiming it is O(P log K).

---

### Q28 ⭐⭐ 🟡 [Set B, Q2 of 5, 8 min, 15 pts] Components after deleting edges one by one. `n` nodes 0..n-1 (1 <= n <= 10^5), `edges` a list of undirected [u, v] pairs (0 <= len <= 2*10^5) numbered by position, and `removals` a list of DISTINCT edge indices giving the order in which edges are deleted. Return a list of len(removals) + 1 integers: the number of connected components before any deletion and after each deletion in turn. Process OFFLINE in reverse: start with all never-deleted edges in a union-find (Part 9 Q13), record the component count, then add the removed edges back from the last removal to the first, recording the count after each, and reverse the list; deleting is hard for union-find, adding is easy. O((n + m) alpha(n)). Compare with the online union-find of Part 9 Q43 and the plain component count of Part 9 Q3. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an oracle that recounts the components from scratch after every deletion on small inputs. Example: n=4, edges=[[0, 1], [1, 2], [2, 3]], removals=[1, 0] -> [1, 2, 3]; n=3, edges=[[0, 1], [0, 1], [1, 2]], removals=[0, 1, 2] -> [1, 1, 2, 3].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Offline reversal: deletions are hard for union-find, additions are easy, so process the deletions backwards.

**Say this first (1 line):** "I replay the deletions in reverse as insertions into a union-find that starts with only the never-deleted edges, record the component count each time, then reverse the list."

**Brute force:**
- After each deletion rebuild the graph and count components with a DFS. O(k (n + m)) for k deletions. My oracle.

**Optimal:**
- Put every edge whose index is not in `removals` into a union-find; `comps` starts at n and drops by one for each union that joins two different roots.
- Record `comps` (the count after ALL deletions). Then for idx in reversed(removals): union the endpoints of edge idx and record `comps`.
- The recorded list reads: after the last deletion, after the one before, ..., before any deletion. Reverse it to get the required order: initial count first.
- Why this is right: the graph after deletion i is exactly "never-deleted edges plus the edges deleted after i", which is what the reverse replay holds at that moment. The component count depends only on the edge set, not on the order edges were added.
- Parallel edges and self loops are fine: the second union of the same pair or a self loop changes nothing (find returns the same root).
- Compare: Part 9 Q43 is the online union-find (edges arrive over time); Part 9 Q3 counts components once. Here the future is known, which is what lets us avoid deletion support.

**Complexity:**
- Time O((n + m) alpha(n)) with path halving (plus union by size, or even without it in practice), O(len(removals) + m) for the set and loops.
- Space O(n + m) (parent array, removal set).
- Find is iterative (path halving), so a path of 10^5 nodes is no recursion problem.

**Dry run:** n=4, edges 0-1, 1-2, 2-3, removals [1, 0].
- Edges never deleted: index 2 (2-3). comps = 4 - 1 = 3. Record [3].
- Reverse replay: removal idx 0 (0-1): union, comps 2. Record [3, 2]. Then idx 1 (1-2): union, comps 1. Record [3, 2, 1].
- Reverse: [1, 2, 3]. Matches the example: 1 component at the start, 2 after deleting edge 1, 3 after deleting edge 0.
- Second example: edges 0-1, 0-1, 1-2, removals [0, 1, 2] gives [1, 1, 2, 3]: deleting one of the parallel edges changes nothing.

**Code:**
```python
import random

def optimal(n, edges, removals):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:                # iterative, path halving
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    comps = n
    def union(a, b):
        nonlocal comps
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            comps -= 1
    gone = set(removals)
    for i, (u, v) in enumerate(edges):       # edges that are never deleted
        if i not in gone:
            union(u, v)
    out = [comps]
    for idx in reversed(removals):           # add the deleted edges back, last deletion first
        union(*edges[idx])
        out.append(comps)
    out.reverse()
    return out

def count_components(n, edges, banned):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if i not in banned:
            adj[u].append(v); adj[v].append(u)
    seen = [False] * n; c = 0
    for s in range(n):
        if not seen[s]:
            c += 1; seen[s] = True; st = [s]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if not seen[y]:
                        seen[y] = True; st.append(y)
    return c

def brute(n, edges, removals):
    banned = set(); out = [count_components(n, edges, banned)]
    for idx in removals:
        banned.add(idx); out.append(count_components(n, edges, banned))
    return out

assert optimal(4, [[0, 1], [1, 2], [2, 3]], [1, 0]) == [1, 2, 3]
assert optimal(3, [[0, 1], [0, 1], [1, 2]], [0, 1, 2]) == [1, 1, 2, 3]
print('examples:', optimal(4, [[0, 1], [1, 2], [2, 3]], [1, 0]), optimal(3, [[0, 1], [0, 1], [1, 2]], [0, 1, 2]))

# edge cases
assert optimal(1, [], []) == [1]
assert optimal(2, [[0, 0]], [0]) == [2, 2]                 # self loop never merges anything
assert optimal(5, [], []) == [5]
assert optimal(3, [[0, 1], [1, 2]], []) == [1]             # no removals: one number

random.seed(28)
for _ in range(800):
    n = random.randint(1, 8)
    m = random.randint(0, 12)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    k = random.randint(0, m)
    removals = random.sample(range(m), k)
    assert optimal(n, edges, removals) == brute(n, edges, removals), (n, edges, removals)
print('random cross-check ok: 800 cases (parallel edges and self loops included)')

N = 10**5
edges = [[i, i + 1] for i in range(N - 1)] + [[i, i + 2] for i in range(N - 2)]
removals = list(range(len(edges)))
random.shuffle(removals)
res = optimal(N, edges, removals)
assert res[0] == 1 and res[-1] == N and len(res) == len(edges) + 1
assert all(res[i] <= res[i + 1] for i in range(len(res) - 1))   # deletions never reduce the count
print('n = 10^5, 2*10^5 deletions: monotone, starts at 1, ends at', res[-1])
```

**Output (my run):**
```
examples: [1, 2, 3] [1, 1, 2, 3]
random cross-check ok: 800 cases (parallel edges and self loops included)
n = 10^5, 2*10^5 deletions: monotone, starts at 1, ends at 100000
```

**Edge cases:**
- No removals: a one-element list with the initial count.
- No edges: n, repeated.
- Self loops and parallel edges (tested).
- Removing every edge ends at n.

**Follow-ups:**
- Pacing and scoring: this is Set B, Q2 of 5, 8 minutes, 15 points. How I would pace this: 1 minute to say the offline reverse idea and the rules (distinct indices, the output has k + 1 values, initial count first), 4 minutes to code it, 1 minute on the example, 1 minute for complexity, 1 minute for edge cases and the summary. Scoring by the part header rubric (15 points): about 4.5 for stating the rules and the reversal idea before coding, 4.5 for a correct solution that passes the example and the brute-force check, 3 for stating the complexity and why, 1.5 for the edge cases, 1.5 for a crisp summary. Partial credit: the per-deletion DFS recount is correct but O(k (n + m)), so it earns correctness but little for complexity.
- Edges deleted online, without knowing the future? Needs a dynamic-connectivity structure (offline divide and conquer over time or link-cut trees), beyond this question.
- Can the count go up when adding back? No: it never rises as edges are added, so the output list is non-decreasing in the deletion order (the code asserts it).

**Common mistakes:**
- Adding all edges including the removed ones to the initial union-find.
- Forgetting to reverse the recorded list, or reversing it but dropping the initial count.
- Recursive find on a long path (recursion limit 1000).
- Recording the count before the unions of the never-deleted edges.

---

### Q29 ⭐⭐ 🟡 [Set B, Q3 of 5, 9 min, 20 pts] Connect all cities, some roads already built. `n` cities 0..n-1 (1 <= n <= 10^4), `built`, a list of [u, v] roads that already exist (cost 0), and `edges`, a list of [u, v, cost] candidate new roads (1 <= cost <= 10^6, up to 5*10^4). Return the minimum total cost of new roads so that every pair of cities is connected, or -1 when impossible even with every candidate. Kruskal (Part 9 Q29): first union the already built roads for free, then take candidate roads in increasing cost order when they join two different components (union-find, Part 9 Q13); stop counting when one component is left. O(E log E). Explain why pre-merging the free roads keeps the greedy proof valid (contracting zero-cost edges) and why Prim would need the same pre-contraction. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an exhaustive oracle that tries every subset of candidate roads (at most 10 candidates) on small inputs. Example: n=4, built=[[0, 1]], edges=[[1, 2, 5], [2, 3, 1], [0, 3, 9], [0, 2, 4]] -> 5; n=3, built=[], edges=[[0, 1, 2]] -> -1; n=1, built=[], edges=[] -> 0.
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Kruskal's minimum spanning tree with the free edges contracted first (union-find).

**Say this first (1 line):** "Union all already-built roads for free, then run Kruskal over the candidates in increasing cost, and answer -1 if more than one component remains."

**Brute force:**
- Try every subset of the candidate roads, keep those that connect all cities together with the built roads, take the cheapest. O(2^E * (n + E)); the oracle for E <= 9.

**Optimal:**
- Union-find over n cities; `comps = n`. For each built road, union (each union that merges two roots lowers `comps`).
- Sort candidates by cost. For each, if its endpoints have different roots, union them, add the cost, lower `comps`. Stop when `comps == 1`.
- At the end, `comps == 1` gives the cost; otherwise -1. n = 1 gives 0.
- Why pre-merging keeps the greedy proof valid: a built road is an edge of weight 0, and zero-weight edges are the cheapest possible, so Kruskal would take them first anyway (a cycle-forming one is skipped). Contracting them leaves the same problem on the merged components, and the cut/cycle argument for Kruskal applies unchanged. Candidates that now join two cities of one component are skipped like any cycle edge (the code tests "3 cities, built 0-1 and 1-2, candidate 0-2 cost 7 gives 0").
- Prim would need the same pre-contraction: start from the merged components (or give built edges weight 0), otherwise it may pay for an edge that a free path makes redundant.
- Greedy reference: Part 9 Q29 (Kruskal), union-find: Part 9 Q13.

**Complexity:**
- Time O(E log E) for the sort plus O((n + E) alpha(n)) for the unions. Space O(n + E).
- The brute force is exponential in E and only an oracle.

**Dry run:** n=4, built 0-1, candidates (1,2,5), (2,3,1), (0,3,9), (0,2,4).
- Built: union 0-1, comps = 3: components {0,1}, {2}, {3}.
- Sorted by cost: (2,3,1), (0,2,4), (1,2,5), (0,3,9).
- (2,3,1): different components, take it, cost 1, comps 2.
- (0,2,4): {0,1} and {2,3} differ, take it, cost 5, comps 1. Stop. Answer 5.
- Example 2: n=3, no built road, one candidate 0-1: city 2 is never reached, comps stays 2, answer -1. Example 3: n=1 needs nothing: 0.

**Code:**
```python
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
```

**Output (my run):**
```
examples: 5 -1 0
random cross-check ok: 600 cases against all subsets of <= 9 candidates
with free road 0-1, answer = 5 (buying the cost-1 duplicate would add 1 for nothing)
n = 10^4, 5*10^4 candidates -> cost 1161494664
```

**Edge cases:**
- Already connected by built roads: 0, whatever the candidates.
- n = 1: 0. Disconnected even with everything: -1.
- Self loop candidates and duplicate candidates (the cheaper one is picked, tested).
- Built roads that form a cycle: the extra union is a no-op.

**Follow-ups:**
- Pacing and scoring: this is Set B, Q3 of 5, 9 minutes, 20 points. How I would pace this: 2 minutes to state the plan and the rules (built roads are free, return -1 if impossible, n = 1 is 0), 4 minutes to code, 1 minute to run the example, 1 minute for complexity and the contraction argument, 1 minute spare for edge cases and the summary. Scoring by the part header rubric (20 points): about 6 for stating the rules and plan, 6 for a correct solution passing the example and a random subset-oracle check, 4 for the complexity and why, 2 for the edge cases, 2 for the spoken summary. Partial credit: plain Kruskal that ignores the built roads is a common wrong answer (example 1 would give 10, not 5); it earns the rules and complexity points but not the correctness points.
- Must the chosen roads form a tree? The cost is the same as a spanning forest over components, since extra roads only add cost (all costs are at least 1).
- Dense graph? Prim with a heap, with built roads contracted first (Part 9 Q37).

**Common mistakes:**
- Treating built roads as candidates of cost 0 inside the sort but forgetting the -1 check.
- Counting components wrongly (starting `comps` at n but not decrementing during the free unions).
- Returning the partial cost instead of -1 when the graph stays disconnected.
- Recursive find on long chains (use halving).

---

### Q30 ⭐⭐ 🟡 [Set C, Q1 of 4, 8 min, 15 pts] Range frequency queries. Implement class `RangeFreqQuery(arr)` (1 <= len <= 10^5, 1 <= value <= 10^4) with `query(left, right, value)` returning how many times `value` occurs in arr[left..right] (both ends included, 0 <= left <= right < len). Store, for each value, the sorted list of its positions (Part 1 style dict of lists); a query is two bisect calls: `bisect_right(pos, right) - bisect_left(pos, left)` (bounds semantics: Part 5 Q11, and the first/last position idea of Part 5 Q4), O(log k) per query and O(n) memory; a value that never occurs counts 0. Say why a prefix-count table per value would use O(n * distinct) memory and when it is still the right choice. The checker builds the object with `init` (the constructor arguments), then runs `ops`, a list of [method, [args]] calls in order, and collects one return value per call (None for a method that returns nothing). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a simple reference implementation (a naive version that rescans plain lists) on random operation sequences on small inputs. Example: init=[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], ops=[['query', [1, 2, 4]], ['query', [0, 11, 33]], ['query', [3, 3, 56]], ['query', [0, 11, 99]], ['query', [4, 8, 22]]] -> [1, 2, 1, 0, 2].
**Asked at:** Mock-set design by the editor in the style of timed online-assessment and onsite rounds at product companies (no source reports these exact sets); the individual problems are standard public-list problems known to the editor, indicative only, no company attribution

**Pattern:** Per-value sorted position lists plus two binary searches (`bisect_left`, `bisect_right`).

**Say this first (1 line):** "For each value I keep the sorted list of its positions; a query counts positions in [left, right] with `bisect_right(right) - bisect_left(left)`."

**Brute force:**
- Slice `arr[left:right+1]` and `.count(value)` on every query. O(n) per query. My oracle.

**Optimal:**
- Constructor: one pass, `pos[v].append(i)`. Indices arrive in increasing order, so every list is already sorted. O(n) time and memory.
- `query(left, right, value)`: look the list up with `.get` (an unseen value gives 0 and must not add a key). Then `bisect_right(p, right) - bisect_left(p, left)`.
- Bounds, both ends inclusive: `bisect_left(p, left)` is the first position >= left; `bisect_right(p, right)` is one past the last position <= right (semantics: Part 5 Q11; the first/last position idea: Part 5 Q4).
- Why not a prefix-count table per value: it needs (n + 1) cells for every distinct value, which for n = 10^5 and 10^4 distinct values is about 10^9 cells. It is still the right choice when the number of distinct values is tiny (say 2 to 26 letters) and you want O(1) queries.

**Complexity:**
- Build O(n). Query O(log k) for k occurrences of the value (at most log n). Space O(n).
- Thread safety (concept only): after construction the structure is read-only, so concurrent queries need no lock; a version with an `append` method would need a lock.

**Dry run:** arr = [12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56], positions: 12: [0, 9]; 33: [1, 7]; 4: [2]; 56: [3, 11]; 22: [4, 8]; 2: [5]; 34: [6, 10].
- query(1, 2, 4): p = [2]. `bisect_right(p, 2)` = 1, `bisect_left(p, 1)` = 0. Result 1.
- query(0, 11, 33): p = [1, 7]: 2 - 0 = 2. query(3, 3, 56): p = [3, 11]: right(3) = 1, left(3) = 0: 1.
- query(0, 11, 99): no list: 0.
- query(4, 8, 22): p = [4, 8]: right(8) = 2, left(4) = 0: 2.

**Code:**
```python
import random
from bisect import bisect_left, bisect_right
from collections import defaultdict

class RangeFreqQuery:
    def __init__(self, arr):
        self.pos = defaultdict(list)
        for i, v in enumerate(arr):                  # positions are appended in increasing order, so each list is sorted
            self.pos[v].append(i)

    def query(self, left, right, value):             # O(log k), k = occurrences of value
        p = self.pos.get(value)                      # .get: do not create an entry for an unseen value
        if not p:
            return 0
        return bisect_right(p, right) - bisect_left(p, left)

class Naive:
    def __init__(self, arr): self.a = list(arr)
    def query(self, left, right, value): return self.a[left:right + 1].count(value)

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

arr = [12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]
ops = [['query', [1, 2, 4]], ['query', [0, 11, 33]], ['query', [3, 3, 56]], ['query', [0, 11, 99]], ['query', [4, 8, 22]]]
assert run(RangeFreqQuery, [arr], ops) == [1, 2, 1, 0, 2]
print('example:', run(RangeFreqQuery, [arr], ops))

# bounds: both ends inclusive
q = RangeFreqQuery([5, 5, 5, 5])
assert q.query(0, 3, 5) == 4 and q.query(1, 2, 5) == 2 and q.query(2, 2, 5) == 1 and q.query(0, 0, 6) == 0
assert len(q.pos) == 1                                # querying an unseen value did not add a key
assert RangeFreqQuery([1]).query(0, 0, 1) == 1

random.seed(30)
n_ops = 0
for _ in range(500):
    n = random.randint(1, 20)
    arr = [random.randint(1, 5) for _ in range(n)]
    ops = []
    for _ in range(30):
        l = random.randrange(n); r = random.randint(l, n - 1)
        ops.append(['query', [l, r, random.randint(1, 7)]])      # 6 and 7 never occur
    assert run(RangeFreqQuery, [arr], ops) == run(Naive, [arr], ops), (arr, ops)
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 arrays,', n_ops, 'queries')

# memory claim: a prefix-count table per value needs (n + 1) * distinct cells
n, distinct = 10**5, 10**4
print('prefix table cells for n = 10^5 and 10^4 distinct values:', (n + 1) * distinct, 'vs positions lists:', n)
big = [random.randint(1, 10**4) for _ in range(10**5)]
f = RangeFreqQuery(big)
assert sum(len(v) for v in f.pos.values()) == 10**5
for _ in range(2000):
    l = random.randrange(10**5); r = random.randint(l, 10**5 - 1); v = random.randint(1, 10**4)
    assert f.query(l, r, v) == big[l:r + 1].count(v)
print('n = 10^5, 2000 random queries ok')
```

**Output (my run):**
```
example: [1, 2, 1, 0, 2]
operation-sequence oracle ok: 500 arrays, 15000 queries
prefix table cells for n = 10^5 and 10^4 distinct values: 1000010000 vs positions lists: 100000
n = 10^5, 2000 random queries ok
```

**Edge cases:**
- Value never present: 0, without creating a dict entry (tested with `len(q.pos)`).
- left == right, whole array, all elements equal.
- Single element array.
- Both ends inclusive: using `bisect_left` for the right end undercounts a match at `right`.

**Follow-ups:**
- Pacing and scoring: this is Set C, Q1 of 4, 8 minutes, 15 points. How I would pace this: 1 minute to state the rules (inclusive ends, absent value is 0), 3 minutes to code the dict of lists and the two bisects, 1 minute to run the example, 1 minute for complexity and the prefix-table memory remark, 2 minutes spare for edge cases and the summary. Scoring by the part header rubric (15 points): about 4.5 for stating the rules before coding, 4.5 for a correct solution passing the example and a random operation-sequence check, 3 for the complexity and why, 1.5 for the edge cases, 1.5 for a crisp summary. Partial credit: the slice-and-count version is correct but O(n) per query, so it gets correctness but no complexity points.
- Updates to the array? Positions lists need insertion into a sorted list (`insort`, O(k)); for heavy updates use a structure per value or an offline BIT.
- Why not a segment tree? It could answer "how many equal" only by storing a counter per node (too much memory with 10^4 values).

**Common mistakes:**
- `bisect_right` on the left bound, or `bisect_left` on the right bound.
- `pos[value]` on a defaultdict, which silently creates empty entries for absent values.
- Treating `right` as exclusive.
- Building the position lists by sorting each one again (unneeded).

---
