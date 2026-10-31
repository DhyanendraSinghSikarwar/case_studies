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
