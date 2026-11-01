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
