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
