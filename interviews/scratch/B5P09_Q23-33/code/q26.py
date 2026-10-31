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
