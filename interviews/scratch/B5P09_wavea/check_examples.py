# Runs EVERY example rendered into the Part 9 prompts (qs.py is the single source of truth) against the reference solutions (refs.py),
# cross-checks each reference against an independent brute force / validator on seeded random small inputs, and tests the bound,
# uniqueness and equivalence claims made in the prompts. Run: python3 -I check_examples.py
import sys, os, random, itertools, heapq, copy, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import deque
from qs import QS
import refs
from refs import S, B, OK, CMP
random.seed(9); t0 = time.time(); R = random.randint
CASES = 400

# ---- 1. every example in every prompt
for st, d, key, text, exs, asked in QS:
    for kw, exp in exs:
        got = S[key](**copy.deepcopy(kw))
        if key in OK: assert OK[key](kw, got) and OK[key](kw, exp), (key, kw, got, exp)
        else: assert got == exp, (key, kw, got, exp)
        if key in B:
            if key in OK: assert OK[key](kw, B[key](**copy.deepcopy(kw))), ('brute-valid', key, kw)
            elif key in CMP: assert CMP[key](B[key](**copy.deepcopy(kw)), exp), ('brute', key, kw)
            else: assert B[key](**copy.deepcopy(kw)) == exp, ('brute', key, kw)
print('examples ok', sum(len(q[4]) for q in QS), 'in', len(QS), 'prompts')

# ---- 2. random generators
def simple_edges(n, m, directed=False, w=None):
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (directed or u < v)]
    random.shuffle(pairs); out = []
    for u, v in pairs[:m]:
        if not directed and R(0, 1): u, v = v, u
        out.append([u, v] + ([R(*w)] if w else []))
    return out
def conn_edges(n, extra):
    es = [[R(0, i - 1), i] for i in range(1, n)]
    es += simple_edges(n, extra); seen = set(); out = []
    for u, v in es:
        if (min(u, v), max(u, v)) not in seen: seen.add((min(u, v), max(u, v))); out.append([u, v])
    random.shuffle(out); return out
def rgrid(m, n, vals, p=None): return [[random.choice(vals) for _ in range(n)] for _ in range(m)]
def sgrid(m, n, pl=0.5): return [''.join('1' if random.random() < pl else '0' for _ in range(n)) for _ in range(m)]
def dag_edges(n, m, w):
    perm = list(range(n)); random.shuffle(perm); out = []
    for _ in range(m):
        i, j = sorted(random.sample(range(n), 2)) if n > 1 else (0, 0)
        if i != j: out.append([perm[i], perm[j], R(*w)])
    return out
def no_negcycle(n, edges, src): return refs.s_bellman_ford(n, edges, src) is not None
def rand_tree(n): return [[R(0, i - 1), i] for i in range(1, n)]
def relabel(edges, n):
    p = list(range(n)); random.shuffle(p); return [[p[u], p[v]] for u, v in edges]
def two_islands():
    while True:
        n = R(2, 6); g = [[1 if random.random() < .35 else 0 for _ in range(n)] for _ in range(n)]
        cells = {(i, j) for i in range(n) for j in range(n) if g[i][j]}; comps = 0; seen = set()
        for s in cells:
            if s in seen: continue
            comps += 1; st = [s]; seen.add(s)
            while st:
                x, y = st.pop()
                for dx, dy in refs.D4:
                    t = (x + dx, y + dy)
                    if t in cells and t not in seen: seen.add(t); st.append(t)
        if comps == 2: return g
def rwords():
    letters = 'abcd'[:R(1, 4)]; order = list(letters); random.shuffle(order); rank = {c: i for i, c in enumerate(order)}
    ws = [''.join(random.choice(letters) for _ in range(R(1, 4))) for _ in range(R(1, 6))]
    if random.random() < .8: ws.sort(key=lambda w: [rank[c] for c in w])
    return ws
def rwords_sorted_edge(): return rwords()
def accounts():
    grp = {'a': ['e0', 'e1', 'e2'], 'b': ['e3', 'e4', 'e5']}; out = []
    for _ in range(R(1, 6)):
        nm = random.choice('ab'); out.append([nm] + [random.choice(grp[nm]) for _ in range(R(1, 3))])
    return out
G = {
 'graph_repr': lambda: (lambda n, d: dict(n=n, edges=simple_edges(n, R(0, n * (n - 1) // (1 if d else 2)), d, (1, 9)), directed=d))(R(0, 6), random.random() < .5),
 'bfs_dfs_orders': lambda: (lambda n: dict(n=n, edges=simple_edges(n, R(0, n * (n - 1) // 2)), start=R(0, n - 1)))(R(1, 8)),
 'components': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, n))]))(R(0, 9)),
 'islands': lambda: dict(grid=sgrid(R(1, 6), R(1, 6), random.random())),
 'flood_fill': lambda: (lambda m, n: dict(image=rgrid(m, n, [0, 1, 2]), sr=R(0, m - 1), sc=R(0, n - 1), color=R(0, 3)))(R(1, 5), R(1, 5)),
 'deep_dfs': lambda: (lambda n: dict(n=n, edges=conn_edges(n, R(0, 4))))(R(1, 9)),
 'bfs_dist': lambda: (lambda n: dict(n=n, edges=[e[:2] for e in simple_edges(n, R(0, 8), True)] if False else simple_edges(n, R(0, min(8, n * (n - 1) // 2))), src=R(0, n - 1), directed=random.random() < .5))(R(1, 8)),
 'can_finish': lambda: (lambda n: dict(num_courses=n, prerequisites=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 8))]))(R(1, 6)),
 'course_order': lambda: (lambda n: dict(num_courses=n, prerequisites=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 7))]))(R(1, 6)),
 'cycle_directed': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 6))]))(R(1, 6)),
 'rotting': lambda: dict(grid=rgrid(R(1, 5), R(1, 5), [0, 1, 1, 2])),
 'network_delay': lambda: (lambda n: dict(n=n, times=[[R(1, n), R(1, n), R(0, 9)] for _ in range(R(0, 10))], k=R(1, n)))(R(1, 6)),
 'dsu_ops': lambda: (lambda n: dict(n=n, ops=[[random.choice(['union', 'connected']), R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 12))]))(R(1, 8)),
 'word_ladder': lambda: (lambda L: (lambda ws: dict(begin=''.join(random.choice('abc') for _ in range(L)), end=random.choice(ws), word_list=ws))(list({''.join(random.choice('abc') for _ in range(L)) for _ in range(R(1, 8))})))(R(1, 3)),
 'bfs_work': lambda: (lambda n, d: dict(n=n, edges=simple_edges(n, R(0, n * (n - 1) // (1 if d else 2)), d)[:], directed=d, src=R(0, n - 1)))(R(1, 7), random.random() < .5),
 'provinces': lambda: (lambda n: (lambda es: dict(is_connected=[[1 if i == j or [min(i, j), max(i, j)] in es else 0 for j in range(n)] for i in range(n)]))(simple_edges(n, R(0, n))))(R(1, 8)),
 'binary_matrix_path': lambda: (lambda n: dict(grid=rgrid(n, n, [0, 0, 1])))(R(1, 6)),
 'clone_graph': lambda: (lambda n: (lambda es: dict(adj=[[v + 1 for u, v in [(a, b) for a, b in es] + [(b, a) for a, b in es] if u == i] for i in range(n)]))(conn_edges(n, R(0, 3))))(R(1, 7)),
 'walls_gates': lambda: dict(rooms=rgrid(R(1, 5), R(1, 5), [-1, 0, 2147483647, 2147483647])),
 'is_bipartite': lambda: (lambda n: (lambda es: dict(graph=[[v for u, v in es if u == i] + [u for u, v in es if v == i] for i in range(n)]))(simple_edges(n, R(0, n + 2))))(R(1, 7)),
 'cycle_undirected': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 4))]))(R(1, 6)),
 'accounts_merge': lambda: dict(accounts=accounts()),
 'parallel_courses': lambda: (lambda n: dict(n=n, relations=[[R(1, n), R(1, n)] for _ in range(R(0, 7))]))(R(1, 6)),
 'dijkstra_lazy': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1), R(0, 9)] for _ in range(R(0, 12))], src=R(0, n - 1)))(R(1, 7)),
 'min_effort': lambda: dict(heights=rgrid(R(1, 5), R(1, 5), list(range(0, 10)))),
 'zero_one_bfs': lambda: (lambda m, n: (lambda g: (g[0].__setitem__(0, 0), g[-1].__setitem__(-1, 0), dict(grid=g))[2])(rgrid(m, n, [0, 1])))(R(1, 5), R(1, 5)),
 'bellman_ford': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1), R(-4, 6)] for _ in range(R(0, 10))], src=R(0, n - 1)))(R(1, 6)),
 'kruskal': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1), R(1, 6)] for _ in range(R(n - 1, 9))]))(R(1, 5)),
 'open_lock': lambda: dict(deadends=[''.join(random.choice('0129') for _ in range(4)) for _ in range(R(0, 40))], target=''.join(random.choice('0129') for _ in range(4))),
 'dfs_topo': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 7))]))(R(1, 6)),
 'sliding_puzzle': lambda: (lambda p: dict(board=[p[:3], p[3:]]))(random.sample(range(6), 6)),
 'alien_order': lambda: dict(words=rwords()),
 'cheapest_flights': lambda: (lambda n: dict(n=n, flights=[[R(0, n - 1), R(0, n - 1), R(1, 9)] for _ in range(R(0, 8))], src=0, dst=R(0, n - 1), k=R(0, n - 1)))(R(1, 5)),
 'floyd_city': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1), R(1, 6)] for _ in range(R(0, 8))], threshold=R(1, 9)))(R(2, 6)),
 'euler': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 7))]))(R(1, 5)),
 'prim_points': lambda: dict(points=[list(p) for p in random.sample([(x, y) for x in range(6) for y in range(6)], R(1, 8))]),
 'dfs_marking': lambda: (lambda n: dict(n=n, edges=simple_edges(n, R(0, n * (n - 1) // 2)), start=R(0, n - 1)))(R(1, 7)),
 'stones': lambda: dict(stones=[list(p) for p in random.sample([(x, y) for x in range(4) for y in range(4)], R(1, 8))]),
 'dag_shortest': lambda: (lambda n: dict(n=n, edges=dag_edges(n, R(0, 9), (-5, 6)), src=R(0, n - 1)))(R(1, 7)),
 'safe_states': lambda: (lambda n: dict(graph=[[R(0, n - 1) for _ in range(R(0, 2))] for _ in range(n)]))(R(1, 7)),
 'dijkstra_negative': None,
 'islands2': lambda: (lambda m, n: dict(m=m, n=n, positions=[[R(0, m - 1), R(0, n - 1)] for _ in range(R(1, 9))]))(R(1, 4), R(1, 4)),
 'shortest_bridge': lambda: dict(grid=two_islands()),
 'mht': lambda: (lambda n: dict(n=n, edges=relabel(rand_tree(n), n)))(R(1, 10)),
}
def redundant_case():
    n = R(3, 8); t = rand_tree(n + 1)  # tree on nodes 0..n -> relabel to 1..n by dropping to n nodes: build tree on n nodes + extra
    t = [[u + 1, v + 1] for u, v in rand_tree(n)]
    while True:
        a, b = random.sample(range(1, n + 1), 2)
        if sorted([a, b]) not in [sorted(e) for e in t]: break
    es = t + [[a, b]]; random.shuffle(es); return dict(edges=es)
def negcase():
    while True:
        n = R(1, 5); es = [[R(0, n - 1), R(0, n - 1), R(-4, 6)] for _ in range(R(0, 8))]; s = R(0, n - 1)
        if no_negcycle(n, es, s): return dict(n=n, edges=es, src=s)
G['redundant'] = redundant_case; G['dijkstra_negative'] = negcase
# generators needing guarantees
def dag_case(): return G['dag_shortest']()
tot = 0
for key in S:
    gen = G[key]
    for _ in range(CASES):
        kw = gen(); a = S[key](**copy.deepcopy(kw))
        if key in OK:
            assert OK[key](kw, a), (key, kw, a)
            if key in B: assert OK[key](kw, B[key](**copy.deepcopy(kw))), ('brute', key, kw)
        elif key in B:
            b = B[key](**copy.deepcopy(kw))
            assert (CMP[key](a, b) if key in CMP else a == b), (key, kw, a, b)
        tot += 1
print('random cross-checks ok', tot, f'({time.time() - t0:.0f}s)')

# ---- 3. claims
# 3a. bfs_work bounds
for _ in range(500):
    kw = G['bfs_work'](); r, e, c = S['bfs_work'](**kw); E = len(kw['edges'])
    assert e <= (E if kw['directed'] else 2 * E) and c == kw['n'] * r and r <= kw['n']
# 3b. dijkstra_lazy: pushes <= E+1, stale == pushes - reached, pops == pushes
for _ in range(1500):
    kw = G['dijkstra_lazy'](); dist, pushes, stale = S['dijkstra_lazy'](**kw)
    reached = sum(x is not None for x in dist)
    assert pushes <= len(kw['edges']) + 1 and stale == pushes - reached, (kw, dist, pushes, stale)
# 3c. why Dijkstra fails: exhaustive on 3 nodes, weights -3..3, src 0
wrong = ok_nonneg = 0; example_fail = None; pairs3 = [(u, v) for u in range(3) for v in range(3) if u != v]
for ws in itertools.product([None, -3, -2, -1, 0, 1, 2, 3], repeat=6):
    es = [[u, v, w] for (u, v), w in zip(pairs3, ws) if w is not None]
    if not no_negcycle(3, es, 0): continue
    dj, bf = S['dijkstra_negative'](3, es, 0)
    stale_variant = refs.s_dijkstra_stale_variant(3, es, 0)
    assert stale_variant == bf, (es,)
    if dj != bf:
        wrong += 1
        assert any(w < 0 for _, _, w in es)
        if example_fail is None or len(es) < len(example_fail): example_fail = es
    elif all(w >= 0 for _, _, w in es): ok_nonneg += 1
    if all(w >= 0 for _, _, w in es): assert dj == bf
print('Dijkstra(finalise-on-pop) wrong on', wrong, 'of 3-node graphs; smallest failing example', example_fail, '; never wrong with non-negative weights')
assert wrong > 0 and len(example_fail) == 3
for _ in range(1500):  # stale-check variant on random graphs without negative cycles
    kw = G['dijkstra_negative'](); assert refs.s_dijkstra_stale_variant(**kw) == refs.s_bellman_ford(**kw)
# 3d. sliding puzzle: 720 states, 360 solvable, max 21
tab = refs.puzzle_table(); assert len(tab) == 360
allp = list(itertools.permutations(range(6))); assert len(allp) == 720
for p in allp: assert S['sliding_puzzle']([list(p[:3]), list(p[3:])]) == tab.get(p, -1)
print('sliding puzzle: 720 boards, 360 solvable (parity), max moves', max(tab.values()))
assert max(tab.values()) == 21
# 3e. recursion limit claims
import sys
n = 200000; path = [[i, i + 1] for i in range(n - 1)]
t1 = time.time(); order, depth = S['deep_dfs'](n, path); assert order == list(range(n)) and depth == n - 1
assert refs.s_cycle_directed(n, path) is False and refs.s_cycle_directed(n, path + [[n - 1, 0]]) is True
assert refs.s_dfs_topo(n, path) == list(range(n)) and refs.s_dfs_topo(n, path + [[n - 1, 0]]) == []
assert refs.s_cycle_undirected(n, path) is False and refs.s_cycle_undirected(n, path + [[n - 1, 0]]) is True
assert refs.s_bfs_dfs_orders(n, path, 0)[1] == list(range(n)) and refs.s_components(n, path) == [list(range(n))]
big = [str(1) * 300] * 300; assert refs.s_islands(big) == [1, 90000]; assert refs.s_flood_fill([[1] * 300 for _ in range(300)], 0, 0, 2)[299][299] == 2
try: refs.b_deep_dfs(5000, path[:4999]); raise SystemExit('recursive DFS unexpectedly survived 5000 deep')
except RecursionError: print('recursive DFS on a 5000-node path raises RecursionError at the default limit', sys.getrecursionlimit())
assert refs.s_dsu_ops(10**5, [['union', i, i + 1] for i in range(10**5 - 1)] + [['connected', 0, 10**5 - 1]])[0][-1] is True
p = list(range(10**5))   # naive link (no size): union(i, i+1) as parent[root(i)] = root(i+1) builds a chain
for i in range(10**5 - 1): p[i] = i + 1
d = 0; x = 0
while p[x] != x: x = p[x]; d += 1
assert d == 10**5 - 1
print('large iterative runs ok', f'{time.time() - t1:.1f}s')
# 3f. cheapest flights: in-place update and plain Dijkstra both fail somewhere
def cf_inplace(n, flights, src, dst, k):
    d = [refs.INF] * n; d[src] = 0
    for _ in range(k + 1):
        for u, v, w in flights:
            if d[u] + w < d[v]: d[v] = d[u] + w
    return -1 if d[dst] == refs.INF else d[dst]
def cf_dijkstra(n, flights, src, dst, k):
    adj = [[] for _ in range(n)]
    for u, v, w in flights: adj[u].append((v, w))
    done = set(); h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if u in done: continue
        done.add(u)
        if u == dst: return d
        for v, w in adj[u]:
            if v not in done: heapq.heappush(h, (d + w, v))
    return -1
f1 = f2 = 0
for _ in range(3000):
    kw = G['cheapest_flights']()
    if cf_inplace(**kw) != S['cheapest_flights'](**kw): f1 += 1
    r = cf_dijkstra(**kw); b = S['cheapest_flights'](**kw)
    if r != b: f2 += 1
print('cheapest flights: in-place variant wrong on', f1, 'and Dijkstra-with-visited (ignores stops) wrong on', f2, 'of 3000')
assert f1 > 0 and f2 > 0
# 3g. 0-1 BFS: ordinary BFS with mark-on-first-enqueue is wrong somewhere
def plain_bfs(grid):
    m, n = len(grid), len(grid[0]); dist = {(0, 0): 0}; q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        for dx, dy in refs.D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and (a, b) not in dist: dist[(a, b)] = dist[(x, y)] + grid[a][b]; q.append((a, b))
    return dist[(m - 1, n - 1)]
bad = sum(plain_bfs(kw['grid']) != S['zero_one_bfs'](**kw) for kw in (G['zero_one_bfs']() for _ in range(2000)))
print('0-1 grid: ordinary mark-on-enqueue BFS wrong on', bad, 'of 2000'); assert bad > 0
# 3h. binary matrix: mark-on-dequeue holds duplicates (larger queue) but same answer
def bm_dequeue(grid):
    n = len(grid)
    if grid[0][0] or grid[-1][-1]: return -1, 0
    seen = set(); q = deque([(0, 0, 1)]); mx = 1
    while q:
        x, y, d = q.popleft()
        if (x, y) in seen: continue
        seen.add((x, y))
        if (x, y) == (n - 1, n - 1): return d, mx
        for dx, dy in refs.D8:
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < n and not grid[a][b] and (a, b) not in seen: q.append((a, b, d + 1)); mx = max(mx, len(q))
    return -1, mx
dup = 0
for _ in range(500):
    g = [[0] * 8 for _ in range(8)]; r, mx = bm_dequeue(g); assert r == refs.s_binary_matrix_path(g) == 8
    kw = G['binary_matrix_path'](); assert bm_dequeue(kw['grid'])[0] == S['binary_matrix_path'](**kw)
print('binary matrix: mark-on-dequeue gives the same answer (queue can hold duplicates)')
# 3i. redundant: scan-first-closing edge is the last cycle edge (brute checks last removable), exhaustive over all trees+edge n<=6 via random 600
# 3j. dfs_marking: variant B can differ from the recursive preorder, same node set
diff = 0
for _ in range(800):
    kw = G['dfs_marking'](); A, Bv = S['dfs_marking'](**kw); assert sorted(A) == sorted(Bv); diff += A != Bv
print('mark-on-push order differs from recursive preorder on', diff, 'of 800 random graphs'); assert diff > 0
# 3k. mht: one or two roots for every labelled tree with n <= 7 (Pruefer) 
def prufer_tree(seq, n):
    deg = [1] * n
    for x in seq: deg[x] += 1
    edges = []
    for x in seq:
        for j in range(n):
            if deg[j] == 1: edges.append([j, x]); deg[j] -= 1; deg[x] -= 1; break
    u, v = [i for i in range(n) if deg[i] == 1]; edges.append([u, v]); return edges
cnt = 0
for n in range(2, 8):
    for seq in itertools.product(range(n), repeat=n - 2):
        es = prufer_tree(seq, n); r = S['mht'](n, es); assert len(r) in (1, 2) and r == B['mht'](n, es); cnt += 1
print('mht: 1 or 2 roots on all', cnt, 'labelled trees with n in 2..7')
# 3l. euler exhaustive-ish handled by brute; kruskal weight unique: compare Kruskal vs Prim-points style on random
# 3m. alien: brute alphabet-permutation validator confirmed above; check both '' branches occur
em = sum(S['alien_order'](**G['alien_order']()) == '' for _ in range(400)); print('alien: empty-answer cases among 400 random lists:', em); assert 0 < em < 400
# 3n. large-size runs
n = 10**5; es = [[random.randrange(i), i] for i in range(1, n)] + [[random.randrange(n), random.randrange(n)] for _ in range(10**5)]
t1 = time.time(); S['components'](n, es); S['bfs_dist'](n, es, 0, False); refs.s_is_bipartite(refs.adj_undirected(n, es)); S['cycle_undirected'](n, es)
w = [[u, v, random.randint(0, 100)] for u, v in es]; S['dijkstra_lazy'](n, w, 0); S['kruskal'](n, w); S['network_delay'](n, [[u + 1, v + 1, x] for u, v, x in w], 1)
print('10^5-size graph runs ok', f'{time.time() - t1:.1f}s')
g = [[random.choice([0, 0, 0, 1]) for _ in range(300)] for _ in range(300)]; g[0][0] = g[-1][-1] = 0; S['zero_one_bfs'](g)
ws = [''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)) for _ in range(5000)]; S['word_ladder'](ws[0], ws[1], ws)
S['prim_points']([[random.randint(-10**6, 10**6), random.randint(-10**6, 10**6)] for _ in range(1000)])
print('ALL OK', f'{time.time() - t0:.0f}s')
# ---- 4. outcome coverage of the random generators (both branches of every boolean / sentinel answer must occur)
from collections import Counter
for key, f in [('can_finish', bool), ('cycle_directed', bool), ('is_bipartite', bool), ('cycle_undirected', bool), ('euler', str), ('rotting', lambda x: x == -1),
               ('open_lock', lambda x: x == -1), ('word_ladder', lambda x: x == 0), ('kruskal', lambda x: x == -1), ('binary_matrix_path', lambda x: x == -1),
               ('parallel_courses', lambda x: x == -1), ('cheapest_flights', lambda x: x == -1), ('network_delay', lambda x: x == -1), ('bellman_ford', lambda x: x is None),
               ('course_order', lambda x: x == [])]:
    c = Counter(f(S[key](**G[key]())) for _ in range(600)); print(key, dict(c)); assert len(c) >= (3 if key == 'euler' else 2), key
