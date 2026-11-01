# Reference solutions (s_*), independent brute forces (b_*) and validators (ok_*) for Book 5 Part 9 (graphs).
import heapq, itertools, random, copy
from collections import deque, defaultdict
INF = float('inf')

def adj_undirected(n, edges):
    a = [[] for _ in range(n)]
    for e in edges:
        u, v = e[0], e[1]; a[u].append(v); a[v].append(u)
    return a

# ---------------- 3 stars
def s_graph_repr(n, edges, directed):
    adj = [[] for _ in range(n)]; mat = [[0] * n for _ in range(n)]
    out = [0] * n; inn = [0] * n
    for u, v, w in edges:
        adj[u].append([v, w]); mat[u][v] = w; out[u] += 1; inn[v] += 1
        if not directed:
            adj[v].append([u, w]); mat[v][u] = w; out[v] += 1; inn[u] += 1
    return [adj, mat, out, inn]
def b_graph_repr(n, edges, directed):
    mat = [[0] * n for _ in range(n)]
    for u, v, w in edges:
        mat[u][v] = w
        if not directed: mat[v][u] = w
    adj = [[[v, mat[u][v]] for v in range(n) if mat[u][v]] for u in range(n)]
    return [adj, mat, [sum(1 for x in r if x) for r in mat], [sum(1 for u in range(n) if mat[u][v]) for v in range(n)]]
def cmp_graph_repr(a, b):
    return [[sorted(x) for x in a[0]]] + a[1:] == [[sorted(x) for x in b[0]]] + b[1:]

def s_bfs_dfs_orders(n, edges, start):
    adj = adj_undirected(n, edges)
    seen = {start}; q = deque([start]); bfs = []
    while q:
        u = q.popleft(); bfs.append(u)
        for v in adj[u]:
            if v not in seen: seen.add(v); q.append(v)
    seen = set(); st = [start]; dfs = []
    while st:
        u = st.pop()
        if u in seen: continue
        seen.add(u); dfs.append(u)
        for v in reversed(adj[u]): st.append(v)
    return [bfs, dfs]
def b_bfs_dfs_orders(n, edges, start):
    adj = adj_undirected(n, edges); dfs = []; seen = set()
    def go(u):
        seen.add(u); dfs.append(u)
        for v in adj[u]:
            if v not in seen: go(v)
    go(start)
    dist = {start: 0}; fr = [start]; bfs = []
    while fr:
        bfs += fr; nxt = []
        for u in fr:
            for v in adj[u]:
                if v not in dist: dist[v] = dist[u] + 1; nxt.append(v)
        fr = nxt
    return [bfs, dfs]

def s_components(n, edges):
    adj = adj_undirected(n, edges); seen = [False] * n; out = []
    for s in range(n):
        if seen[s]: continue
        seen[s] = True; st = [s]; comp = []
        while st:
            u = st.pop(); comp.append(u)
            for v in adj[u]:
                if not seen[v]: seen[v] = True; st.append(v)
        out.append(sorted(comp))
    return out
def b_components(n, edges):
    lab = list(range(n)); ch = True
    while ch:
        ch = False
        for u, v in edges:
            m = min(lab[u], lab[v])
            if lab[u] != m or lab[v] != m: lab[u] = lab[v] = m; ch = True
    g = defaultdict(list)
    for i, l in enumerate(lab): g[l].append(i)
    return sorted(g.values())

D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
def s_islands(grid):
    m, n = len(grid), len(grid[0]); seen = [[False] * n for _ in range(m)]; cnt = best = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1' and not seen[i][j]:
                cnt += 1; seen[i][j] = True; q = deque([(i, j)]); area = 0
                while q:
                    x, y = q.popleft(); area += 1
                    for dx, dy in D4:
                        a, b = x + dx, y + dy
                        if 0 <= a < m and 0 <= b < n and grid[a][b] == '1' and not seen[a][b]: seen[a][b] = True; q.append((a, b))
                best = max(best, area)
    return [cnt, best]
def b_islands(grid):
    m, n = len(grid), len(grid[0]); lab = {}
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1': lab[(i, j)] = (i, j)
    ch = True
    while ch:
        ch = False
        for (i, j) in lab:
            for dx, dy in D4:
                p = (i + dx, j + dy)
                if p in lab and lab[p] < lab[(i, j)]: lab[(i, j)] = lab[p]; ch = True
    from collections import Counter
    c = Counter(lab.values())
    return [len(c), max(c.values()) if c else 0]

def s_flood_fill(image, sr, sc, color):
    old = image[sr][sc]; img = [r[:] for r in image]
    if old == color: return img
    img[sr][sc] = color; st = [(sr, sc)]
    while st:
        x, y = st.pop()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < len(img) and 0 <= b < len(img[0]) and img[a][b] == old: img[a][b] = color; st.append((a, b))
    return img
def b_flood_fill(image, sr, sc, color):
    old = image[sr][sc]; m, n = len(image), len(image[0]); img = [r[:] for r in image]
    def go(x, y, seen):
        seen.add((x, y))
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and image[a][b] == old and (a, b) not in seen: go(a, b, seen)
    seen = set(); go(sr, sc, seen)
    for x, y in seen: img[x][y] = color
    return img

def s_deep_dfs(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    for l in adj: l.sort()
    order = []; depth = {0: 0}; seen = [False] * n; st = [(0, iter(adj[0]))]; seen[0] = True; order.append(0); best = 0
    while st:
        u, it = st[-1]
        for v in it:
            if not seen[v]:
                seen[v] = True; order.append(v); depth[v] = depth[u] + 1; best = max(best, depth[v]); st.append((v, iter(adj[v]))); break
        else: st.pop()
    return [order, best]
def b_deep_dfs(n, edges):
    import sys
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    for l in adj: l.sort()
    order = []; seen = set(); best = [0]
    def go(u, d):
        seen.add(u); order.append(u); best[0] = max(best[0], d)
        for v in adj[u]:
            if v not in seen: go(v, d + 1)
    go(0, 0); return [order, best[0]]

def s_bfs_dist(n, edges, src, directed):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed: adj[v].append(u)
    dist = [-1] * n; dist[src] = 0; q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0: dist[v] = dist[u] + 1; q.append(v)
    return dist
def b_bfs_dist(n, edges, src, directed):
    d = [INF] * n; d[src] = 0
    for _ in range(n):
        for u, v in edges:
            if d[u] + 1 < d[v]: d[v] = d[u] + 1
            if not directed and d[v] + 1 < d[u]: d[u] = d[v] + 1
    return [-1 if x == INF else x for x in d]

def s_can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]; indeg = [0] * num_courses
    for a, b in prerequisites: adj[b].append(a); indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0); done = 0
    while q:
        u = q.popleft(); done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return done == num_courses
def closure(n, edges):
    r = [[False] * n for _ in range(n)]
    for u, v in edges: r[u][v] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]: r[i][j] = True
    return r
def b_can_finish(num_courses, prerequisites):
    r = closure(num_courses, [(b, a) for a, b in prerequisites])
    return not any(r[i][i] for i in range(num_courses))

def s_course_order(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]; indeg = [0] * num_courses
    for a, b in prerequisites: adj[b].append(a); indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0); out = []
    while q:
        u = q.popleft(); out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return out if len(out) == num_courses else []
def ok_course_order(kw, got):
    n, pre = kw['num_courses'], kw['prerequisites']
    if not b_can_finish(n, pre): return got == []
    if sorted(got) != list(range(n)): return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[b] < pos[a] for a, b in pre)

def s_cycle_directed(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v)
    color = [0] * n   # 0 white, 1 grey, 2 black
    for s in range(n):
        if color[s]: continue
        color[s] = 1; st = [(s, iter(adj[s]))]
        while st:
            u, it = st[-1]
            for v in it:
                if color[v] == 1: return True
                if color[v] == 0: color[v] = 1; st.append((v, iter(adj[v]))); break
            else: color[u] = 2; st.pop()
    return False
def b_cycle_directed(n, edges):
    r = closure(n, edges); return any(r[i][i] for i in range(n))

def s_rotting(grid):
    m, n = len(grid), len(grid[0]); g = [r[:] for r in grid]; q = deque(); fresh = 0
    for i in range(m):
        for j in range(n):
            if g[i][j] == 2: q.append((i, j))
            elif g[i][j] == 1: fresh += 1
    t = 0
    while q and fresh:
        for _ in range(len(q)):
            x, y = q.popleft()
            for dx, dy in D4:
                a, b = x + dx, y + dy
                if 0 <= a < m and 0 <= b < n and g[a][b] == 1: g[a][b] = 2; fresh -= 1; q.append((a, b))
        t += 1
    return -1 if fresh else t
def b_rotting(grid):
    m, n = len(grid), len(grid[0]); g = [r[:] for r in grid]; t = 0
    while True:
        new = [r[:] for r in g]; ch = False
        for i in range(m):
            for j in range(n):
                if g[i][j] == 1 and any(0 <= i + dx < m and 0 <= j + dy < n and g[i + dx][j + dy] == 2 for dx, dy in D4): new[i][j] = 2; ch = True
        if not ch: break
        g = new; t += 1
    return -1 if any(1 in r for r in g) else t

def s_network_delay(n, times, k):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in times: adj[u].append((v, w))
    dist = [INF] * (n + 1); dist[k] = 0; h = [(0, k)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if d + w < dist[v]: dist[v] = d + w; heapq.heappush(h, (d + w, v))
    m = max(dist[1:]); return -1 if m == INF else m
def b_network_delay(n, times, k):
    d = [INF] * (n + 1); d[k] = 0
    for _ in range(n):
        for u, v, w in times:
            if d[u] + w < d[v]: d[v] = d[u] + w
    m = max(d[1:]); return -1 if m == INF else m

def s_dsu_ops(n, ops):
    p = list(range(n)); sz = [1] * n
    def find(x):
        r = x
        while p[r] != r: r = p[r]
        while p[x] != r: p[x], x = r, p[x]
        return r
    res = []; sets = n
    for op, a, b in ops:
        ra, rb = find(a), find(b)
        if op == 'union':
            if ra == rb: res.append(False)
            else:
                if sz[ra] < sz[rb]: ra, rb = rb, ra
                p[rb] = ra; sz[ra] += sz[rb]; sets -= 1; res.append(True)
        else: res.append(ra == rb)
    return [res, sets, max(sz[find(i)] for i in range(n))]
def b_dsu_ops(n, ops):
    lab = list(range(n)); res = []
    for op, a, b in ops:
        if op == 'union':
            if lab[a] == lab[b]: res.append(False)
            else:
                old = lab[b]
                for i in range(n):
                    if lab[i] == old: lab[i] = lab[a]
                res.append(True)
        else: res.append(lab[a] == lab[b])
    from collections import Counter
    c = Counter(lab); return [res, len(c), max(c.values())]

def s_redundant(edges):
    n = len(edges); p = list(range(n + 1))
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges:
        a, b = find(u), find(v)
        if a == b: return [u, v]
        p[a] = b
def connected_without(n, edges, skip):
    adj = [[] for _ in range(n + 1)]
    for i, (u, v) in enumerate(edges):
        if i != skip: adj[u].append(v); adj[v].append(u)
    seen = {1}; st = [1]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); st.append(v)
    return len(seen) == n
def b_redundant(edges):
    n = len(edges)
    for i in range(n - 1, -1, -1):
        if connected_without(n, edges, i): return list(edges[i])

def s_word_ladder(begin, end, word_list):
    words = set(word_list)
    if end not in words: return 0
    q = deque([(begin, 1)]); seen = {begin}
    while q:
        w, d = q.popleft()
        if w == end: return d
        for i in range(len(w)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                x = w[:i] + c + w[i + 1:]
                if x in words and x not in seen: seen.add(x); q.append((x, d + 1))
    return 0
def b_word_ladder(begin, end, word_list):
    nodes = [begin] + [w for w in dict.fromkeys(word_list) if w != begin]
    if end not in nodes: return 0
    d = {w: INF for w in nodes}; d[begin] = 1
    adj = {w: [x for x in nodes if sum(a != b for a, b in zip(w, x)) == 1] for w in nodes}
    ch = True
    while ch:
        ch = False
        for w in nodes:
            for x in adj[w]:
                if d[w] + 1 < d[x]: d[x] = d[w] + 1; ch = True
    return 0 if d[end] == INF else d[end]

# ---------------- 2 stars
def s_bfs_work(n, edges, directed, src):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed: adj[v].append(u)
    seen = {src}; q = deque([src]); reached = entries = 0
    while q:
        u = q.popleft(); reached += 1; entries += len(adj[u])
        for v in adj[u]:
            if v not in seen: seen.add(v); q.append(v)
    return [reached, entries, n * reached]
def b_bfs_work(n, edges, directed, src):
    mat = [[0] * n for _ in range(n)]
    for u, v in edges:
        mat[u][v] = 1
        if not directed: mat[v][u] = 1
    seen = {src}; q = deque([src]); reached = entries = cells = 0
    while q:
        u = q.popleft(); reached += 1
        for v in range(n):
            cells += 1
            if mat[u][v]:
                entries += 1
                if v not in seen: seen.add(v); q.append(v)
    return [reached, entries, cells]

def s_provinces(is_connected):
    n = len(is_connected); p = list(range(n))
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    c = n
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                a, b = find(i), find(j)
                if a != b: p[a] = b; c -= 1
    return c
def b_provinces(is_connected):
    n = len(is_connected); seen = set(); c = 0
    for s in range(n):
        if s in seen: continue
        c += 1; st = [s]; seen.add(s)
        while st:
            u = st.pop()
            for v in range(n):
                if is_connected[u][v] and v not in seen: seen.add(v); st.append(v)
    return c

D8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
def s_binary_matrix_path(grid):
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]: return -1
    dist = {(0, 0): 1}; q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        if (x, y) == (n - 1, n - 1): return dist[(x, y)]
        for dx, dy in D8:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and (a, b) not in dist: dist[(a, b)] = dist[(x, y)] + 1; q.append((a, b))
    return -1
def b_binary_matrix_path(grid):
    n = len(grid); d = {(i, j): INF for i in range(n) for j in range(n) if not grid[i][j]}
    if (0, 0) not in d or (n - 1, n - 1) not in d: return -1
    d[(0, 0)] = 1; ch = True
    while ch:
        ch = False
        for (x, y), v in list(d.items()):
            for dx, dy in D8:
                p = (x + dx, y + dy)
                if p in d and v + 1 < d[p]: d[p] = v + 1; ch = True
    r = d[(n - 1, n - 1)]; return -1 if r == INF else r

class Node:
    def __init__(self, val): self.val = val; self.neighbors = []
def build_nodes(adj):
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, l in enumerate(adj): nodes[i].neighbors = [nodes[v - 1] for v in l]
    return nodes
def clone_solution(node):
    if node is None: return None
    m = {node: Node(node.val)}; q = deque([node])
    while q:
        u = q.popleft()
        for v in u.neighbors:
            if v not in m: m[v] = Node(v.val); q.append(v)
            m[u].neighbors.append(m[v])
    return m[node]
def nodes_to_adj(root, n):
    if root is None: return []
    seen = {root.val: root}; q = deque([root]); res = {}
    while q:
        u = q.popleft(); res[u.val] = [v.val for v in u.neighbors]
        for v in u.neighbors:
            if v.val not in seen: seen[v.val] = v; q.append(v)
    return [res[i] for i in range(1, n + 1)], seen
def s_clone_graph(adj):
    if not adj: return []
    nodes = build_nodes(adj); c = clone_solution(nodes[0])
    out, seen = nodes_to_adj(c, len(adj))
    orig = {id(x) for x in nodes}
    assert not any(id(x) in orig for x in seen.values()), 'shared node'
    return out
def b_clone_graph(adj):
    if not adj: return []
    nodes = build_nodes(adj); c = copy.deepcopy(nodes[0]); return nodes_to_adj(c, len(adj))[0]

def s_walls_gates(rooms):
    INFV = 2147483647; m, n = len(rooms), len(rooms[0]); g = [r[:] for r in rooms]
    q = deque((i, j) for i in range(m) for j in range(n) if g[i][j] == 0)
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and g[a][b] == INFV: g[a][b] = g[x][y] + 1; q.append((a, b))
    return g
def b_walls_gates(rooms):
    INFV = 2147483647; m, n = len(rooms), len(rooms[0]); g = [r[:] for r in rooms]
    for i in range(m):
        for j in range(n):
            if rooms[i][j] != INFV: continue
            dist = {(i, j): 0}; fr = [(i, j)]; found = INFV
            while fr and found == INFV:
                nxt = []
                for x, y in fr:
                    if rooms[x][y] == 0: found = dist[(x, y)]; break
                    for dx, dy in D4:
                        a, b = x + dx, y + dy
                        if 0 <= a < m and 0 <= b < n and rooms[a][b] != -1 and (a, b) not in dist: dist[(a, b)] = dist[(x, y)] + 1; nxt.append((a, b))
                fr = nxt
            g[i][j] = found
    return g

def s_is_bipartite(graph):
    n = len(graph); col = [-1] * n
    for s in range(n):
        if col[s] >= 0: continue
        col[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if col[v] < 0: col[v] = 1 - col[u]; q.append(v)
                elif col[v] == col[u]: return False
    return True
def b_is_bipartite(graph):
    n = len(graph)
    return any(all(c[u] != c[v] for u in range(n) for v in graph[u]) for c in itertools.product((0, 1), repeat=n))

def s_cycle_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges): adj[u].append((v, i)); adj[v].append((u, i))
    seen = [False] * n
    for s in range(n):
        if seen[s]: continue
        seen[s] = True; st = [(s, -1)]
        while st:
            u, pe = st.pop()
            for v, i in adj[u]:
                if i == pe: continue
                if seen[v]: return True
                seen[v] = True; st.append((v, i))
    return False
def b_cycle_undirected(n, edges):
    for i, (u, v) in enumerate(edges):
        if u == v: return True
        adj = [[] for _ in range(n)]
        for j, (a, b) in enumerate(edges):
            if j != i: adj[a].append(b); adj[b].append(a)
        seen = {u}; st = [u]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        if v in seen: return True
    return False

def s_accounts_merge(accounts):
    p = {}
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    name = {}
    for acc in accounts:
        for e in acc[1:]:
            p.setdefault(e, e); name[e] = acc[0]
        for e in acc[2:]: p[find(e)] = find(acc[1])
    g = defaultdict(list)
    for e in p: g[find(e)].append(e)
    return sorted([name[r], *sorted(es)] for r, es in g.items())
def b_accounts_merge(accounts):
    sets = [(a[0], set(a[1:])) for a in accounts]; ch = True
    while ch:
        ch = False
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                if sets[i][1] & sets[j][1]:
                    sets[i] = (sets[i][0], sets[i][1] | sets[j][1]); del sets[j]; ch = True; break
            if ch: break
    return sorted([nm, *sorted(es)] for nm, es in sets)

def s_parallel_courses(n, relations):
    adj = [[] for _ in range(n + 1)]; indeg = [0] * (n + 1)
    for a, b in relations: adj[a].append(b); indeg[b] += 1
    cur = [i for i in range(1, n + 1) if indeg[i] == 0]; sem = done = 0
    while cur:
        sem += 1; done += len(cur); nxt = []
        for u in cur:
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0: nxt.append(v)
        cur = nxt
    return sem if done == n else -1
def b_parallel_courses(n, relations):
    d = [1] * (n + 1)
    for _ in range(n):
        for a, b in relations:
            if d[a] + 1 > d[b]: d[b] = d[a] + 1
    if any(d[a] + 1 > d[b] for a, b in relations): return -1
    return max(d[1:]) if n else 0

def s_dijkstra_lazy(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v, w in edges: adj[u].append((v, w))
    dist = [INF] * n; dist[src] = 0; h = [(0, src)]; pushes = 1; stale = 0
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]: stale += 1; continue
        for v, w in adj[u]:
            if d + w < dist[v]: dist[v] = d + w; heapq.heappush(h, (d + w, v)); pushes += 1
    return [[None if x == INF else x for x in dist], pushes, stale]
def b_dijkstra_lazy(n, edges, src):
    d = [INF] * n; d[src] = 0
    for _ in range(n):
        for u, v, w in edges:
            if d[u] + w < d[v]: d[v] = d[u] + w
    return [[None if x == INF else x for x in d]]
def cmp_dijkstra_lazy(a, b): return a[0] == b[0]

def s_min_effort(heights):
    m, n = len(heights), len(heights[0]); best = [[INF] * n for _ in range(m)]; best[0][0] = 0; h = [(0, 0, 0)]
    while h:
        e, x, y = heapq.heappop(h)
        if e > best[x][y]: continue
        if (x, y) == (m - 1, n - 1): return e
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n:
                ne = max(e, abs(heights[a][b] - heights[x][y]))
                if ne < best[a][b]: best[a][b] = ne; heapq.heappush(h, (ne, a, b))
def b_min_effort(heights):
    m, n = len(heights), len(heights[0])
    for t in range(0, max(max(r) for r in heights) - min(min(r) for r in heights) + 1):
        seen = {(0, 0)}; st = [(0, 0)]
        while st:
            x, y = st.pop()
            for dx, dy in D4:
                a, b = x + dx, y + dy
                if 0 <= a < m and 0 <= b < n and (a, b) not in seen and abs(heights[a][b] - heights[x][y]) <= t: seen.add((a, b)); st.append((a, b))
        if (m - 1, n - 1) in seen: return t

def s_zero_one_bfs(grid):
    m, n = len(grid), len(grid[0]); dist = [[INF] * n for _ in range(m)]; dist[0][0] = 0; dq = deque([(0, 0)])
    while dq:
        x, y = dq.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n:
                w = grid[a][b]
                if dist[x][y] + w < dist[a][b]:
                    dist[a][b] = dist[x][y] + w
                    (dq.append if w else dq.appendleft)((a, b))
    return dist[m - 1][n - 1]
def b_zero_one_bfs(grid):
    m, n = len(grid), len(grid[0]); d = [[INF] * n for _ in range(m)]; d[0][0] = 0; ch = True
    while ch:
        ch = False
        for x in range(m):
            for y in range(n):
                for dx, dy in D4:
                    a, b = x + dx, y + dy
                    if 0 <= a < m and 0 <= b < n and d[x][y] + grid[a][b] < d[a][b]: d[a][b] = d[x][y] + grid[a][b]; ch = True
    return d[m - 1][n - 1]

def s_bellman_ford(n, edges, src):
    d = [INF] * n; d[src] = 0
    for _ in range(n - 1):
        ch = False
        for u, v, w in edges:
            if d[u] != INF and d[u] + w < d[v]: d[v] = d[u] + w; ch = True
        if not ch: break
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]: return None
    return [None if x == INF else x for x in d]
def b_bellman_ford(n, edges, src):
    f = [[INF] * n for _ in range(n)]
    for i in range(n): f[i][i] = 0
    for u, v, w in edges: f[u][v] = min(f[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if f[i][k] + f[k][j] < f[i][j]: f[i][j] = f[i][k] + f[k][j]
    if any(f[src][k] < INF and f[k][k] < 0 for k in range(n)): return None
    return [None if x == INF else x for x in f[src]]

def s_kruskal(n, edges):
    p = list(range(n))
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    tot = used = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a != b: p[a] = b; tot += w; used += 1
    return tot if used == n - 1 else -1
def b_kruskal(n, edges):
    best = None
    for sub in itertools.combinations(edges, n - 1):
        p = list(range(n))
        def find(x):
            while p[x] != x: x = p[x]
            return x
        ok = True
        for u, v, w in sub:
            a, b = find(u), find(v)
            if a == b: ok = False; break
            p[a] = b
        if ok:
            t = sum(e[2] for e in sub)
            if best is None or t < best: best = t
    return -1 if best is None else best

def s_open_lock(deadends, target):
    dead = set(deadends)
    if '0000' in dead: return -1
    seen = {'0000'}; q = deque([('0000', 0)])
    while q:
        s, d = q.popleft()
        if s == target: return d
        for i in range(4):
            for step in (1, -1):
                t = s[:i] + str((int(s[i]) + step) % 10) + s[i + 1:]
                if t not in dead and t not in seen: seen.add(t); q.append((t, d + 1))
    return -1
def b_open_lock(deadends, target):
    dead = set(deadends)
    if '0000' in dead: return -1
    level = {'0000'}; seen = set(level); d = 0
    while level:
        if target in level: return d
        nxt = set()
        for s in level:
            for i in range(4):
                for step in (1, 9):
                    t = s[:i] + str((int(s[i]) + step) % 10) + s[i + 1:]
                    if t not in dead and t not in seen: nxt.add(t)
        seen |= nxt; level = nxt; d += 1
    return -1

def s_dfs_topo(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v)
    color = [0] * n; post = []
    for s in range(n):
        if color[s]: continue
        color[s] = 1; st = [(s, iter(adj[s]))]
        while st:
            u, it = st[-1]
            for v in it:
                if color[v] == 1: return []
                if color[v] == 0: color[v] = 1; st.append((v, iter(adj[v]))); break
            else: color[u] = 2; post.append(u); st.pop()
    return post[::-1]
def b_dfs_topo(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v)
    color = [0] * n; post = []; cyc = [False]
    def go(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1: cyc[0] = True
            elif color[v] == 0: go(v)
        color[u] = 2; post.append(u)
    for s in range(n):
        if not color[s]: go(s)
    return [] if cyc[0] else post[::-1]

def s_sliding_puzzle(board):
    start = tuple(x for r in board for x in r); goal = (1, 2, 3, 4, 5, 0)
    nb = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}
    seen = {start}; q = deque([(start, 0)])
    while q:
        s, d = q.popleft()
        if s == goal: return d
        z = s.index(0)
        for j in nb[z]:
            l = list(s); l[z], l[j] = l[j], l[z]; t = tuple(l)
            if t not in seen: seen.add(t); q.append((t, d + 1))
    return -1
_PUZ = None
def puzzle_table():
    global _PUZ
    if _PUZ is None:
        goal = (1, 2, 3, 4, 5, 0); nb = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}
        d = {goal: 0}; fr = [goal]
        while fr:
            nxt = []
            for s in fr:
                z = s.index(0)
                for j in nb[z]:
                    l = list(s); l[z], l[j] = l[j], l[z]; t = tuple(l)
                    if t not in d: d[t] = d[s] + 1; nxt.append(t)
            fr = nxt
        _PUZ = d
    return _PUZ
def b_sliding_puzzle(board): return puzzle_table().get(tuple(x for r in board for x in r), -1)

def s_alien_order(words):
    letters = sorted({c for w in words for c in w}); adj = {c: set() for c in letters}; indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]: adj[x].add(y); indeg[y] += 1
                break
        else:
            if len(a) > len(b): return ''
    q = deque(c for c in letters if indeg[c] == 0); out = []
    while q:
        u = q.popleft(); out.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''
def sorted_under(words, order):
    rank = {c: i for i, c in enumerate(order)}
    key = lambda w: [rank[c] for c in w]
    return all(key(a) <= key(b) for a, b in zip(words, words[1:]))
def ok_alien_order(kw, got):
    words = kw['words']; letters = sorted({c for w in words for c in w})
    if got == '':
        return not any(sorted_under(words, p) for p in itertools.permutations(letters))
    return sorted(got) == letters and sorted_under(words, got)
def b_alien_order(words):
    letters = sorted({c for w in words for c in w})
    for p in itertools.permutations(letters):
        if sorted_under(words, p): return ''.join(p)
    return ''

def s_cheapest_flights(n, flights, src, dst, k):
    d = [INF] * n; d[src] = 0
    for _ in range(k + 1):
        nd = d[:]
        for u, v, w in flights:
            if d[u] + w < nd[v]: nd[v] = d[u] + w
        d = nd
    return -1 if d[dst] == INF else d[dst]
def b_cheapest_flights(n, flights, src, dst, k):
    best = INF
    def go(u, cost, left):
        nonlocal best
        if u == dst: best = min(best, cost)
        if left == 0: return
        for a, b, w in flights:
            if a == u: go(b, cost + w, left - 1)
    go(src, 0, k + 1); return -1 if best == INF else best

# ---------------- 1 star
def s_floyd_city(n, edges, threshold):
    f = [[INF] * n for _ in range(n)]
    for i in range(n): f[i][i] = 0
    for u, v, w in edges: f[u][v] = min(f[u][v], w); f[v][u] = min(f[v][u], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if f[i][k] + f[k][j] < f[i][j]: f[i][j] = f[i][k] + f[k][j]
    best = None
    for i in range(n):
        c = sum(1 for j in range(n) if j != i and f[i][j] <= threshold)
        if best is None or c <= best[0]: best = (c, i)
    return best[1]
def b_floyd_city(n, edges, threshold):
    adj = [[] for _ in range(n)]
    for u, v, w in edges: adj[u].append((v, w)); adj[v].append((u, w))
    best = None
    for s in range(n):
        d = [INF] * n; d[s] = 0; h = [(0, s)]
        while h:
            x, u = heapq.heappop(h)
            if x > d[u]: continue
            for v, w in adj[u]:
                if x + w < d[v]: d[v] = x + w; heapq.heappush(h, (x + w, v))
        c = sum(1 for j in range(n) if j != s and d[j] <= threshold)
        if best is None or c <= best[0]: best = (c, s)
    return best[1]

def s_euler(n, edges):
    if not edges: return 'circuit'
    deg = [0] * n; p = list(range(n))
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges: deg[u] += 1; deg[v] += 1; p[find(u)] = find(v)
    if len({find(u) for u, v in edges}) > 1: return 'none'
    odd = sum(d % 2 for d in deg)
    return 'circuit' if odd == 0 else 'path' if odd == 2 else 'none'
def b_euler(n, edges):
    m = len(edges)
    if m == 0: return 'circuit'
    res = set()
    def go(u, used, start, cnt):
        if cnt == m: res.add('circuit' if u == start else 'path'); return
        for i, (a, b) in enumerate(edges):
            if not used >> i & 1:
                if a == u: go(b, used | 1 << i, start, cnt + 1)
                if b == u and a != b: go(a, used | 1 << i, start, cnt + 1)
    for s in range(n): go(s, 0, s, 0)
    return 'circuit' if 'circuit' in res else 'path' if 'path' in res else 'none'

def s_prim_points(points):
    n = len(points); INFV = float('inf'); dist = [INFV] * n; used = [False] * n; dist[0] = 0; tot = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=lambda i: dist[i]); used[u] = True; tot += dist[u]
        for v in range(n):
            if not used[v]:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if d < dist[v]: dist[v] = d
    return tot
def b_prim_points(points):
    n = len(points); es = sorted((abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j) for i in range(n) for j in range(i + 1, n))
    p = list(range(n))
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    tot = 0
    for w, i, j in es:
        a, b = find(i), find(j)
        if a != b: p[a] = b; tot += w
    return tot

def s_dfs_marking(n, edges, start):
    adj = adj_undirected(n, edges)
    seen = set(); st = [start]; A = []
    while st:
        u = st.pop()
        if u in seen: continue
        seen.add(u); A.append(u)
        for v in reversed(adj[u]): st.append(v)
    seen = {start}; st = [start]; B = []
    while st:
        u = st.pop(); B.append(u)
        for v in adj[u]:
            if v not in seen: seen.add(v); st.append(v)
    return [A, B]
def b_dfs_marking(n, edges, start):
    adj = adj_undirected(n, edges); A = []; seen = set()
    def go(u):
        seen.add(u); A.append(u)
        for v in adj[u]:
            if v not in seen: go(v)
    go(start)
    return [A]
def cmp_dfs_marking(a, b): return a[0] == b[0]

def s_stones(stones):
    p = {}
    def find(x):
        p.setdefault(x, x)
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for r, c in stones: p[find(('r', r))] = find(('c', c))
    return len(stones) - len({find(('r', r)) for r, c in stones})
def b_stones(stones):
    n = len(stones); full = (1 << n) - 1; memo = {}
    def go(left):
        if left in memo: return memo[left]
        best = 0
        for i in range(n):
            if left >> i & 1 and any(j != i and left >> j & 1 and (stones[j][0] == stones[i][0] or stones[j][1] == stones[i][1]) for j in range(n)):
                best = max(best, 1 + go(left & ~(1 << i)))
        memo[left] = best; return best
    return go(full)

def s_dag_shortest(n, edges, src):
    adj = [[] for _ in range(n)]; indeg = [0] * n
    for u, v, w in edges: adj[u].append((v, w)); indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0); order = []
    while q:
        u = q.popleft(); order.append(u)
        for v, w in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    d = [INF] * n; d[src] = 0
    for u in order:
        if d[u] == INF: continue
        for v, w in adj[u]:
            if d[u] + w < d[v]: d[v] = d[u] + w
    return [None if x == INF else x for x in d]
def b_dag_shortest(n, edges, src):
    d = [INF] * n; d[src] = 0
    for _ in range(n):
        for u, v, w in edges:
            if d[u] + w < d[v]: d[v] = d[u] + w
    return [None if x == INF else x for x in d]

def s_safe_states(graph):
    n = len(graph); rev = [[] for _ in range(n)]; out = [len(graph[u]) for u in range(n)]
    for u in range(n):
        for v in graph[u]: rev[v].append(u)
    q = deque(i for i in range(n) if out[i] == 0); safe = []
    while q:
        u = q.popleft(); safe.append(u)
        for p in rev[u]:
            out[p] -= 1
            if out[p] == 0: q.append(p)
    return sorted(safe)
def b_safe_states(graph):
    n = len(graph); r = closure(n, [(u, v) for u in range(n) for v in graph[u]])
    cyc = [i for i in range(n) if r[i][i]]
    return [u for u in range(n) if not any(r[u][c] or u == c for c in cyc)]

def s_dijkstra_negative(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v, w in edges: adj[u].append((v, w))
    dist = [INF] * n; dist[src] = 0; h = [(0, src)]; done = set()
    while h:
        d, u = heapq.heappop(h)
        if u in done: continue
        done.add(u)
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]: dist[v] = d + w; heapq.heappush(h, (d + w, v))
    return [[None if x == INF else x for x in dist], s_bellman_ford(n, edges, src)]
def s_dijkstra_stale_variant(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v, w in edges: adj[u].append((v, w))
    dist = [INF] * n; dist[src] = 0; h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if d + w < dist[v]: dist[v] = d + w; heapq.heappush(h, (d + w, v))
    return [None if x == INF else x for x in dist]
def b_dijkstra_negative(n, edges, src):
    return [None, b_bellman_ford(n, edges, src)]
def cmp_dijkstra_negative(a, b): return a[1] == b[1]

def s_islands2(m, n, positions):
    p = {}; cnt = 0; out = []
    def find(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for x, y in positions:
        if (x, y) not in p:
            p[(x, y)] = (x, y); cnt += 1
            for dx, dy in D4:
                q = (x + dx, y + dy)
                if q in p:
                    a, b = find((x, y)), find(q)
                    if a != b: p[a] = b; cnt -= 1
        out.append(cnt)
    return out
def b_islands2(m, n, positions):
    land = set(); out = []
    for x, y in positions:
        land.add((x, y)); g = [''.join('1' if (i, j) in land else '0' for j in range(n)) for i in range(m)]
        out.append(b_islands(g)[0])
    return out

def s_shortest_bridge(grid):
    n = len(grid); first = None
    for i in range(n):
        for j in range(n):
            if grid[i][j]: first = (i, j); break
        if first: break
    seen = {first}; st = [first]
    while st:
        x, y = st.pop()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and grid[a][b] and (a, b) not in seen: seen.add((a, b)); st.append((a, b))
    q = deque((x, y, 0) for x, y in seen); vis = set(seen)
    while q:
        x, y, d = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and (a, b) not in vis:
                if grid[a][b]: return d
                vis.add((a, b)); q.append((a, b, d + 1))
def b_shortest_bridge(grid):
    n = len(grid); cells = [(i, j) for i in range(n) for j in range(n) if grid[i][j]]
    comp = {}; c = 0
    for s in cells:
        if s in comp: continue
        comp[s] = c; st = [s]
        while st:
            x, y = st.pop()
            for dx, dy in D4:
                t = (x + dx, y + dy)
                if t in cells and t not in comp: comp[t] = c; st.append(t)
        c += 1
    assert c == 2
    return min(abs(a[0] - b[0]) + abs(a[1] - b[1]) - 1 for a in cells for b in cells if comp[a] == 0 and comp[b] == 1)

def s_mht(n, edges):
    if n <= 2: return list(range(n))
    adj = [set() for _ in range(n)]
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    leaves = [i for i in range(n) if len(adj[i]) == 1]; left = n
    while left > 2:
        left -= len(leaves); nxt = []
        for u in leaves:
            v = adj[u].pop(); adj[v].discard(u)
            if len(adj[v]) == 1: nxt.append(v)
        leaves = nxt
    return sorted(leaves)
def b_mht(n, edges):
    adj = adj_undirected(n, edges); hs = []
    for r in range(n):
        d = {r: 0}; q = deque([r])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in d: d[v] = d[u] + 1; q.append(v)
        hs.append(max(d.values()))
    return [i for i in range(n) if hs[i] == min(hs)]

S = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('s_') and k not in ('s_dijkstra_stale_variant',)}
B = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('b_')}
OK = {'course_order': ok_course_order, 'alien_order': ok_alien_order}
CMP = {'graph_repr': cmp_graph_repr, 'dijkstra_lazy': cmp_dijkstra_lazy, 'dfs_marking': cmp_dfs_marking, 'dijkstra_negative': cmp_dijkstra_negative}
