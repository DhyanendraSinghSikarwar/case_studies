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
