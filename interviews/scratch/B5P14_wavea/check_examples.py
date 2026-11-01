# Runs EVERY example rendered into the Part 14 prompts (qs.py is the single source of truth) against the reference solutions (refs.py),
# cross-checks each against an independent oracle on seeded random small inputs / operation sequences, checks the claims made in the
# prompts (boundaries, WHY sentences, exhaustive enumerations) and runs the maximum sizes. Run: python3 -I check_examples.py
import sys, os, random, itertools, copy, time, collections, math, re, bisect, heapq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qs import QS
import refs
from refs import S, B, DES, run_design
random.seed(14); t0 = time.time(); R = random.randint
CASES = 250
assert sys.getrecursionlimit() == 1000 and sys.version_info[:2] == (3, 13)

for st, d, key, text, exs, asked in QS:
    for kw, exp in exs:
        got = S[key](**copy.deepcopy(kw)); assert got == exp, (key, kw, got, exp)
        b = B[key](**copy.deepcopy(kw)); assert b == exp, ('oracle', key, kw, b, exp)
print('examples ok', sum(len(q[4]) for q in QS), 'in', len(QS), 'prompts', flush=True)

def ri(n, lo, hi): return [R(lo, hi) for _ in range(n)]
def clock_times(n, step=4):
    t = 0; out = []
    for _ in range(n): t += R(0, step); out.append(t)
    return out
def seq_ops(n, gens):   # gens: list of (method, argfn)
    return [[m, f()] for m, f in (random.choice(gens) for _ in range(n))]
def timed(n, gens, step=4):
    return [[t] + [m, f()] for t, (m, f) in zip(clock_times(n, step), (random.choice(gens) for _ in range(n)))]

def g_lru(dll):
    def g():
        cap = R(1, 4); gens = [('get', lambda: [R(0, 5)]), ('put', lambda: [R(0, 5), R(0, 99)])]
        if dll: gens += [('order', lambda: []), ('size', lambda: [])]
        return dict(init=[cap], ops=seq_ops(R(0, 40), gens))
    return g
def g_timekv():
    last = {}; ops = []
    for _ in range(R(0, 30)):
        k = random.choice('ab')
        if random.random() < .5:
            last[k] = last.get(k, 0) + R(1, 4); ops.append(['set', [k, f"v{R(0, 99)}", last[k]]])
        else: ops.append(['get', [k, R(0, 25)]])
    return dict(init=[], ops=ops)
def g_nested():
    def mk(d):
        return [R(0, 9) if (d == 0 or random.random() < .6) else mk(d - 1) for _ in range(R(0, 4))]
    nested = mk(3); flat = []
    def go(x):
        for y in x: flat.append(y) if isinstance(y, int) else go(y)
    go(nested); ops = [['hasNext', []]]; left = len(flat)
    for _ in range(R(0, 12)):
        if left and random.random() < .6: ops.append(['next', []]); left -= 1
        else: ops.append(['hasNext', []])
    return dict(init=[nested], ops=ops)
def g_iterlist(lists_mode):
    def g():
        lists = [ri(R(0, 4), 0, 9) for _ in range(R(0, 4))] if lists_mode else ri(R(1, 8), 0, 9)
        total = sum(map(len, lists)) if lists_mode else len(lists); left = total; ops = []
        for _ in range(R(0, 14)):
            r = random.random()
            if left and r < .5: ops.append(['next', []]); left -= 1
            elif not lists_mode and left and r < .75: ops.append(['peek', []])
            else: ops.append(['hasNext', []])
        return dict(init=[lists] if True else None, ops=ops)
    return g
def g_twitter():
    n = [0]
    def post(): n[0] += 1; return [R(1, 4), n[0] * 10 + R(0, 9)]
    gens = [('postTweet', post), ('follow', lambda: [R(1, 4), R(1, 4)]), ('unfollow', lambda: [R(1, 4), R(1, 4)]), ('getNewsFeed', lambda: [R(1, 4)])]
    return dict(init=[R(1, 5)], ops=seq_ops(R(0, 40), gens))
def g_allone():
    k = lambda: [random.choice('abcd')]
    return dict(init=[], ops=seq_ops(R(0, 50), [('inc', k), ('inc', k), ('dec', k), ('getMaxKey', lambda: []), ('getMinKey', lambda: [])]))
def g_lfu():
    return dict(init=[R(0, 3)], ops=seq_ops(R(0, 40), [('get', lambda: [R(0, 5)]), ('put', lambda: [R(0, 5), R(0, 99)])]))
def g_snap():
    n = R(1, 4)
    return dict(init=[n], ops=seq_ops(R(0, 40), [('set', lambda: [R(0, n - 1), R(0, 9)]), ('snap', lambda: [])]) )
def fix_snap(case):   # get only with existing snapshot ids
    ops = []; snaps = 0
    for m, a in case['ops']:
        if m == 'snap': snaps += 1
        ops.append([m, a])
        if snaps and random.random() < .4: ops.append(['get', [R(0, case['init'][0] - 1), R(0, snaps - 1)]])
    case['ops'] = ops; return case
def g_bit():
    n = R(1, 8); return dict(init=[ri(n, -9, 9)], ops=seq_ops(R(0, 30), [('update', lambda: [R(0, n - 1), R(-9, 9)]), ('sumRange', lambda: (lambda l: [l, R(l, n - 1)])(R(0, n - 1)))]))
def g_minseg():
    n = R(1, 9); return dict(init=[ri(n, -9, 9)], ops=seq_ops(R(0, 30), [('update', lambda: [R(0, n - 1), R(-9, 9)]), ('query', lambda: (lambda l: [l, R(l, n - 1)])(R(0, n - 1)))]))
def g_lazy():
    n = R(1, 9); return dict(init=[ri(n, -9, 9)], ops=seq_ops(R(0, 30), [('add', lambda: (lambda l: [l, R(l, n - 1), R(-9, 9)])(R(0, n - 1))), ('sum', lambda: (lambda l: [l, R(l, n - 1)])(R(0, n - 1)))]))
def g_bit2d():
    m, n = R(1, 5), R(1, 5)
    def rect(): r1 = R(0, m - 1); c1 = R(0, n - 1); return [r1, c1, R(r1, m - 1), R(c1, n - 1)]
    return dict(init=[[ri(n, -9, 9) for _ in range(m)]], ops=seq_ops(R(0, 25), [('update', lambda: [R(0, m - 1), R(0, n - 1), R(-9, 9)]), ('sumRegion', rect)]))
def g_hit():
    t = 0; ops = []
    for _ in range(R(0, 30)):
        t += random.choice([0, 0, 1, 2, 100, 149, 150, 299, 300, 301]); ops.append([t, random.choice(['hit', 'getHits']), []])
    return dict(init=[], ops=ops)
def g_logger():
    return dict(init=[], ops=timed(R(0, 40), [('shouldPrint', lambda: [random.choice(['x', 'y', 'z'])])], step=R(1, 6)))
def g_limiter():
    return dict(init=[R(1, 3), R(1, 6)], ops=timed(R(0, 40), [('allow', lambda: [random.choice('uv')])], step=R(1, 4)))
def g_bucket():
    return dict(init=[R(1, 5), R(0, 3)], ops=timed(R(0, 40), [('allow', lambda: [R(1, 6)]), ('allow', lambda: [])], step=R(1, 4)))
def g_mov():
    return dict(init=[R(1, 4)], ops=seq_ops(R(0, 20), [('next', lambda: [R(-9, 9)])]))
def g_metro():
    ops = []; open_ = {}; t = 0
    for _ in range(R(0, 30)):
        t += R(0, 5); i = R(1, 4)
        if i in open_: ops.append(['checkOut', [i, random.choice('ABC'), t]]); st0 = open_.pop(i); done.append((st0, ops[-1][1][1])) if False else None
        else: ops.append(['checkIn', [i, random.choice('ABC'), t]]); open_[i] = 1
    return dict(init=[], ops=ops)
def fix_metro(case):
    ops = []; open_ = {}; done = set()
    for m, a in case['ops']:
        ops.append([m, a])
        if m == 'checkIn': open_[a[0]] = a[1]
        else: done.add((open_.pop(a[0]), a[1]))
        if done and random.random() < .4: ops.append(['getAverageTime', list(random.choice(sorted(done)))])
    case['ops'] = ops; return case
def g_board():
    return dict(init=[], ops=seq_ops(R(0, 30), [('addScore', lambda: [R(1, 5), R(1, 20)]), ('reset', lambda: [R(1, 6)]), ('top', lambda: [R(1, 6)])]))
def g_ttl():
    return dict(init=[R(1, 3)], ops=timed(R(0, 40), [('put', lambda: [R(0, 4), R(0, 99), R(1, 6)]), ('get', lambda: [R(0, 4)]), ('size', lambda: [])], step=R(1, 4)))
def g_sched():
    ids = list(range(1, 100)); pend = set()
    ops = []; cnt = [0]
    def sub(): cnt[0] += 1; return [cnt[0] % 5, R(0, 4), R(0, 3)]
    case = dict(init=[], ops=[])
    t = 0; out = []
    live = set()
    for _ in range(R(0, 30)):
        t += R(0, 3); r = random.random(); nxt = R(1, 6)
        if r < .45:
            out.append([t, 'submit', [f"j{nxt}", R(0, 5), R(0, 3)]])
        elif r < .7: out.append([t, 'cancel', [f"j{R(1, 6)}"]])
        else: out.append([t, 'poll', [R(1, 4)]])
    # drop submits of ids that are pending: replay with the oracle to remove illegal ones
    ok = []; probe = DES['scheduler'][1]; clk = refs.Clock(); obj = probe(clk); pending = set()
    for t, m, a in out:
        clk.t = t
        if m == 'submit':
            if a[0] in pending: continue
            pending.add(a[0]); obj.submit(*a)
        elif m == 'cancel':
            if obj.cancel(*a): pending.discard(a[0])
        else:
            for j in obj.poll(*a): pending.discard(j)
        ok.append([t, m, a])
    return dict(init=[], ops=ok)
def g_rf():
    arr = ri(R(1, 12), 1, 4)
    def q(): l = R(0, len(arr) - 1); return [l, R(l, len(arr) - 1), R(1, 5)]
    return dict(init=[arr], ops=seq_ops(R(0, 20), [('query', q)]))
def g_os():
    m = R(1, 10)
    return dict(init=[m], ops=seq_ops(R(0, 40), [('insert', lambda: [R(0, m)]), ('insert', lambda: [R(0, m)]), ('remove', lambda: [R(0, m)]), ('count_le', lambda: [R(-2, m + 2)]), ('kth', lambda: [R(0, 8)])]))
def g_stock():
    ops = []; seen = False
    for _ in range(R(1, 30)):
        if not seen or random.random() < .5: ops.append(['update', [R(1, 8), R(1, 9)]]); seen = True
        else: ops.append([random.choice(['current', 'maximum', 'minimum']), []])
    return dict(init=[], ops=ops)
def g_vote():
    n = R(1, 10); times = sorted(random.sample(range(1, 40), n)); persons = ri(n, 0, 3)
    return dict(init=[persons, times], ops=[['q', [R(times[0], 45)]] for _ in range(R(1, 10))])
def g_fs():
    ops = []; size = 0
    for _ in range(R(1, 40)):
        if size and random.random() < .45: ops.append(['pop', []]); size -= 1
        else: ops.append(['push', [R(0, 3)]]); size += 1
    return dict(init=[], ops=ops)

def rand_digraph(nmax=7, mmax=14):
    n = R(1, nmax); return n, [[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, mmax))]
def rand_ugraph(nmax=8, mmax=12):
    n = R(1, nmax); return n, [[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, mmax))]
def rand_dag(n, p=.4):
    perm = list(range(n)); random.shuffle(perm); return [[perm[i], perm[j]] for i in range(n) for j in range(i + 1, n) if random.random() < p]
def g_itin():
    cities = ['JFK', 'ATL', 'SFO', 'LAX']; cur = 'JFK'; t = []
    for _ in range(R(1, 7)):
        nxt = random.choice(cities); t.append([cur, nxt]); cur = nxt
    random.shuffle(t); return dict(tickets=t)
def g_sp():
    n = R(2, 6); return dict(n=n, edges=[[R(0, n - 1), R(0, n - 1), R(1, 12)] for _ in range(R(0, 10))])
def g_par():
    n = R(1, 6)
    rel = [[a + 1, b + 1] for a, b in rand_dag(n)]
    if random.random() < .15 and n > 1: rel.append([R(1, n), R(1, n)])
    return dict(n=n, relations=rel, time=ri(n, 1, 9))
def g_match():
    L, Rr = R(1, 6), R(1, 6); return dict(L=L, R=Rr, edges=[[R(0, L - 1), R(0, Rr - 1)] for _ in range(R(0, 12))])
def g_rdel():
    n, e = rand_ugraph(7, 10); m = len(e); k = R(0, m); return dict(n=n, edges=e, removals=random.sample(range(m), k))
def g_conn():
    n = R(1, 6); return dict(n=n, built=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 2))], edges=[[R(0, n - 1), R(0, n - 1), R(1, 9)] for _ in range(R(0, 8))])
def g_red2():
    n = R(3, 7); perm = list(range(1, n + 1)); random.shuffle(perm)
    tree = [[perm[R(0, i - 1)], perm[i]] for i in range(1, n)]
    while True:
        u, v = R(1, n), R(1, n)
        if u != v and [u, v] not in tree: break
    e = tree + [[u, v]]; random.shuffle(e); return dict(edges=e)
def g_calk():
    out = []
    for _ in range(R(0, 8)): s = R(0, 12); out.append([s, R(s + 1, 14)])
    return dict(bookings=out)
def g_sky():
    out = []
    for _ in range(R(1, 6)): l = R(0, 12); out.append([l, R(l + 1, 14), R(1, 9)])
    out.sort(key=lambda b: b[0]); return dict(buildings=out)

G = {
 'lru_ordereddict': g_lru(False), 'lru_dll': g_lru(True), 'lfu': g_lfu, 'time_kv': g_timekv,
 'sliding_log': g_limiter, 'fixed_window': g_limiter, 'token_bucket': g_bucket, 'hit_counter': g_hit, 'logger': g_logger,
 'flatten_iter': g_nested, 'peeking': g_iterlist(False), 'zigzag': g_iterlist(True), 'twitter': g_twitter, 'all_o1': g_allone,
 'snapshot': lambda: fix_snap(g_snap()), 'bit_point_range': g_bit, 'segtree_min': g_minseg, 'lazy_range': g_lazy, 'bit_2d': g_bit2d,
 'scc_kosaraju': lambda: dict(zip(('n', 'edges'), rand_digraph())), 'scc_tarjan': lambda: dict(zip(('n', 'edges'), rand_digraph())),
 'bridges': lambda: dict(zip(('n', 'edges'), rand_ugraph())), 'articulation': lambda: dict(zip(('n', 'edges'), rand_ugraph())),
 'itinerary': g_itin, 'topo_lex': lambda: (lambda n: dict(n=n, edges=rand_dag(n) + ([[R(0, n - 1), R(0, n - 1)]] if random.random() < .1 else [])))(R(1, 6)),
 'parallel_time': g_par, 'sp_coupon': g_sp, 'bipartite_matching': g_match,
 'sparse_table': lambda: (lambda n: dict(nums=ri(n, -5, 5), queries=[(lambda l: [l, R(l, n - 1)])(R(0, n - 1)) for _ in range(R(0, 8))]))(R(1, 20)),
 'coord_compress': lambda: dict(values=ri(R(0, 10), -10**18 if random.random() < .3 else -5, 10**18 if random.random() < .3 else 5)),
 'inversions_bit': lambda: dict(nums=ri(R(0, 12), -4, 4)), 'count_smaller': lambda: dict(nums=ri(R(0, 12), -4, 4)),
 'moving_avg': g_mov, 'underground': lambda: fix_metro(g_metro()), 'leaderboard': g_board, 'lru_ttl': g_ttl, 'scheduler': g_sched,
 'valid_tree': lambda: (lambda n: dict(n=n, edges=[[R(0, n - 1), R(0, n - 1)] for _ in range(R(max(0, n - 2), n + 1))]))(R(1, 6)),
 'reverse_delete': g_rdel, 'connect_cities': g_conn, 'redundant_II': g_red2, 'min_sources': lambda: dict(zip(('n', 'edges'), rand_digraph(7, 12))),
 'range_freq': g_rf, 'dyn_multiset': g_os, 'reverse_pairs': lambda: dict(nums=ri(R(0, 12), -6, 6)), 'calendar_k': g_calk,
 'stock_price': g_stock, 'top_voted': g_vote, 'freq_stack': g_fs, 'skyline': g_sky,
}
assert set(G) == {q[2] for q in QS} and set(G) == set(S) == set(B), set(G) ^ set(S)
SLOW = {'bipartite_matching': 120, 'scc_kosaraju': 250}
for key, gen in G.items():
    n = SLOW.get(key, CASES)
    for _ in range(n):
        kw = gen(); a = S[key](**copy.deepcopy(kw)); b = B[key](**copy.deepcopy(kw))
        assert a == b, (key, kw, a, b)
    print('oracle ok', key, flush=True)

# ---------------------------------------------------------------- claims made in the prompts
# time_kv: bisect_left would be wrong when the timestamp equals a stored one
t_, v_ = [10, 20], ['a', 'b']
assert bisect.bisect_right(t_, 20) - 1 == 1 and bisect.bisect_left(t_, 20) - 1 == 0
# sliding window vs fixed window boundary burst (limit 2, window 10, requests at 8, 9, 10, 11)
assert S['fixed_window'](init=[2, 10], ops=[[t, 'allow', ['u']] for t in (8, 9, 10, 11)]) == [True, True, True, True]
assert S['sliding_log'](init=[2, 10], ops=[[t, 'allow', ['u']] for t in (8, 9, 10, 11)]) == [True, True, False, False]
assert S['sliding_log'](init=[2, 10], ops=[[0, 'allow', ['u']], [5, 'allow', ['u']], [9, 'allow', ['u']], [10, 'allow', ['u']]]) == [True, True, False, True]
# logger steady stream every 3 seconds prints at 0, 12, 24
r = S['logger'](init=[], ops=[[t, 'shouldPrint', ['m']] for t in range(0, 31, 3)])
assert [t for t, x in zip(range(0, 31, 3), r) if x] == [0, 12, 24]
# hit counter: hit exactly 300 old is not counted
assert S['hit_counter'](init=[], ops=[[0, 'hit', []], [299, 'getHits', []], [300, 'getHits', []]]) == [None, 1, 0]
# token bucket: floats are fragile at boundaries; cost above capacity never succeeds
x = 0.0
for _ in range(10): x += 0.1
assert x != 1.0
assert S['token_bucket'](init=[3, 5], ops=[[0, 'allow', [4]], [100, 'allow', [4]]]) == [False, False]
# zigzag order claim
z = S['zigzag'](init=[[[1, 2, 3], [4], [5, 6]]], ops=[['next', []]] * 6); assert z == [1, 4, 5, 2, 6, 3]
# flatten: recursion limit claim; the stack-of-iterators version survives depth 5000
def deep(d):
    x = [7]
    for _ in range(d): x = [x]
    return x
def rec_flat(x, out):
    for y in x: rec_flat(y, out) if isinstance(y, list) else out.append(y)
try: rec_flat(deep(1500), []); assert False
except RecursionError: pass
it = refs.Nested_S(deep(5000)); assert (it.hasNext(), it.next(), it.hasNext()) == (True, 7, False)
# BIT: block length is i & -i; 'add val instead of delta' double counts
nums = ri(40, -9, 9); b = refs.BIT_S(nums)
for i in range(1, 41): assert b.t[i] == sum(nums[i - (i & -i):i])
b.update(3, nums[3] + 5); assert b.sumRange(0, 39) == sum(nums) + 5
bad = refs.BIT_S(nums); bad.a[3] = 0
def bad_update(self, i, val):
    self.a[i] = val; i += 1
    while i <= self.n: self.t[i] += val; i += i & -i
bad2 = refs.BIT_S([1, 2, 3]); bad_update(bad2, 1, 9); assert bad2.sumRange(0, 2) != 13
# bottom-up segment tree works for every n
for n in range(1, 40):
    a = ri(n, -9, 9); t = refs.MinSeg_S(a)
    for l in range(n):
        for r in range(l, n): assert t.query(l, r) == min(a[l:r + 1])
# sparse table: entries count = sum over levels, 2^j <= n; overlapping blocks harmless for min, not for sum
for n in range(1, 70): assert S['sparse_table'](nums=[0] * n, queries=[])[1] == sum(n - (1 << j) + 1 for j in range(n.bit_length()))
assert sum(range(3)) != sum([0, 1]) + sum([1, 2])   # overlap would double count a sum
# bridges: skipping the parent NODE instead of the parent EDGE reports a parallel edge as a bridge
def bridges_by_parent(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v); g[v].append(u)
    disc = [-1] * n; low = [0] * n; out = []; t = [0]
    def dfs(u, p):
        disc[u] = low[u] = t[0]; t[0] += 1
        for v in g[u]:
            if v == p: continue
            if disc[v] == -1:
                dfs(v, u); low[u] = min(low[u], low[v])
                if low[v] > disc[u]: out.append((u, v))
            else: low[u] = min(low[u], disc[v])
    for s in range(n):
        if disc[s] == -1: dfs(s, -1)
    return out
assert bridges_by_parent(2, [[0, 1], [0, 1]]) == [(0, 1)] and S['bridges'](n=2, edges=[[0, 1], [0, 1]]) == []
# articulation: using > instead of >= wrongly drops cut vertices (found by search), >= never disagrees with the oracle (above)
def art_gt(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        if u != v: g[u].append(v); g[v].append(u)
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
found = False
for _ in range(2000):
    n, e = rand_ugraph(7, 10)
    e = [x for x in e if x[0] != x[1]]
    if len({tuple(sorted(x)) for x in e}) != len(e): continue
    if art_gt(n, e) != S['articulation'](n=n, edges=e): found = True; break
assert found
# tarjan: the numbering is a reverse topological order of the condensation; the on-stack test matters; partition equals Kosaraju
for _ in range(400):
    n, e = rand_digraph(8, 16); comp, cnt, cross = S['scc_tarjan'](n=n, edges=e)
    assert all(comp[u] >= comp[v] for u, v in e)
    parts = collections.defaultdict(list)
    for v in range(n): parts[comp[v]].append(v)
    assert sorted(parts.values()) == S['scc_kosaraju'](n=n, edges=e)
def tarjan_no_onstack(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n; st = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; st.append(u); on[u] = True
        for v in g[u]:
            if idx[v] == -1: dfs(v); low[u] = min(low[u], low[v])
            else: low[u] = min(low[u], idx[v])
        if low[u] == idx[u]:
            while True:
                w = st.pop(); on[w] = False; comp[w] = box[1]
                if w == u: break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1: dfs(s)
    return comp
wrong = 0
for _ in range(3000):
    n, e = rand_digraph(6, 10)
    if tarjan_no_onstack(n, e) != S['scc_tarjan'](n=n, edges=e)[0]: wrong += 1
assert wrong > 0, 'dropping the on-stack test must break some graph'
# kosaraju: the node finishing last in pass 1 lies in a source component
for _ in range(300):
    n, e = rand_digraph(7, 12); g = [[] for _ in range(n)]
    for u, v in e: g[u].append(v)
    seen = [False] * n; order = []
    def dfs(u):
        seen[u] = True
        for v in g[u]:
            if not seen[v]: dfs(v)
        order.append(u)
    for s in range(n):
        if not seen[s]: dfs(s)
    comps = S['scc_kosaraju'](n=n, edges=e); cid = {v: i for i, c in enumerate(comps) for v in c}
    assert all(cid[u] == cid[v] or cid[v] != cid[order[-1]] for u, v in e)
# recursion claims for the graph questions: a recursive DFS fails at depth 1500, the iterative references handle 10^5 nodes
def rec_dfs(n, g):
    seen = [False] * n
    def go(u):
        seen[u] = True
        for v in g[u]:
            if not seen[v]: go(v)
    go(0)
try: rec_dfs(1500, [[i + 1] if i + 1 < 1500 else [] for i in range(1500)]); assert False
except RecursionError: pass
N = 10**5; path = [[i, i + 1] for i in range(N - 1)]
assert S['scc_kosaraju'](n=N, edges=path) == [[i] for i in range(N)]
cmp_, cnt, cross = S['scc_tarjan'](n=N, edges=path); assert cnt == N and cross == N - 1 and cmp_[0] == N - 1
assert S['bridges'](n=N, edges=path) == [[i, i + 1] for i in range(N - 1)]
assert S['articulation'](n=N, edges=path) == list(range(1, N - 1))
assert S['topo_lex'](n=N, edges=path) == list(range(N))
assert S['min_sources'](n=N, edges=path) == [0]
assert S['valid_tree'](n=N, edges=path) is True
print('graph claims ok', flush=True)
# topo_lex: FIFO Kahn is valid but not smallest on some DAG; 'labels early' needs the reverse + max-heap trick and differs
def kahn_fifo(n, edges):
    g = [[] for _ in range(n)]; indeg = [0] * n
    for u, v in edges: g[u].append(v); indeg[v] += 1
    q = collections.deque(v for v in range(n) if indeg[v] == 0); out = []
    while q:
        u = q.popleft(); out.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return out
diff_fifo = diff_labels = 0
for _ in range(500):
    n = R(2, 6); e = rand_dag(n)
    lex = S['topo_lex'](n=n, edges=e); fifo = kahn_fifo(n, e); assert lex <= fifo; diff_fifo += lex != fifo
    # labels-early: reverse graph, largest available first, reverse result
    h = []; indeg = [0] * n; g = [[] for _ in range(n)]
    for u, v in e: g[v].append(u); indeg[u] += 1
    h = [-v for v in range(n) if indeg[v] == 0]; heapq.heapify(h); out = []
    while h:
        u = -heapq.heappop(h); out.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(h, -v)
    early = out[::-1]
    best = min((p for p in itertools.permutations(range(n)) if all(p.index(u) < p.index(v) for u, v in e)), key=lambda p: [p.index(l) for l in range(n)])
    assert early == list(best); diff_labels += early != lex
assert diff_fifo > 0 and diff_labels > 0
# itinerary: plain greedy (smallest destination first, no post-order) strands tickets on the prompt's example
def greedy(tickets):
    g = collections.defaultdict(list)
    for a, b in tickets: g[a].append(b)
    for a in g: g[a].sort()
    path = ['JFK']
    while g[path[-1]]: path.append(g[path[-1]].pop(0))
    return path
tk = [['JFK', 'KUL'], ['JFK', 'NRT'], ['NRT', 'JFK']]
assert len(greedy(tk)) != len(tk) + 1 and S['itinerary'](tickets=tk) == ['JFK', 'NRT', 'JFK', 'KUL']
# sp_coupon: best path with a coupon is not the plain shortest path; k coupons = k + 1 layers (checked against enumeration)
ex = [[0, 1, 10], [1, 2, 10], [0, 2, 25]]
assert S['sp_coupon'](n=3, edges=ex) == 12 < 20 - 5
def sp_k(n, edges, K):
    g = [[] for _ in range(n)]
    for u, v, w in edges: g[u].append((v, w))
    INF = float('inf'); dist = {(0, 0): 0}; h = [(0, 0, 0)]
    while h:
        d, u, k = heapq.heappop(h)
        if d > dist.get((u, k), INF): continue
        for v, w in g[u]:
            for nk, c in ((k, w), (k + 1, w // 2)):
                if nk <= K and d + c < dist.get((v, nk), INF): dist[(v, nk)] = d + c; heapq.heappush(h, (d + c, v, nk))
    r = min((dist.get((n - 1, k), INF) for k in range(K + 1))); return -1 if r == INF else r
def brute_k(n, edges, K):
    best = [float('inf')]
    def dfs(u, seen, tot, sv):
        if u == n - 1: best[0] = min(best[0], tot - sum(sorted(sv, reverse=True)[:K])); return
        for a, b, w in edges:
            if a == u and b not in seen: seen.add(b); dfs(b, seen, tot + w, sv + [w - w // 2]); seen.discard(b)
    dfs(0, {0}, 0, []); return -1 if best[0] == float('inf') else best[0]
for _ in range(300):
    kw = g_sp(); K = R(0, 3); assert sp_k(kw['n'], kw['edges'], K) == brute_k(kw['n'], kw['edges'], K), (kw, K)
    assert sp_k(kw['n'], kw['edges'], 1) == S['sp_coupon'](**kw)
# valid_tree: n - 1 edges and no cycle imply connected (exhaustive, n <= 5, all multigraphs of size n - 1)
for n in range(1, 5):
    pairs = [(a, b) for a in range(n) for b in range(a, n)]
    for es in itertools.combinations_with_replacement(pairs, n - 1):
        e = [list(x) for x in es]
        assert S['valid_tree'](n=n, edges=e) == B['valid_tree'](n=n, edges=e)
        if S['valid_tree'](n=n, edges=e): assert refs._components(n, e) == 1
# redundant_II: a node with two parents AND a cycle forces the earlier candidate (all random cases pass vs the oracle above); both outcomes occur
outs = collections.Counter()
for _ in range(600):
    kw = g_red2(); e = kw['edges']; ans = S['redundant_II'](**kw); assert ans == B['redundant_II'](**kw)
    par = collections.Counter(v for u, v in e); outs[('two' if max(par.values()) == 2 else 'cycle')] += 1
assert outs['two'] > 0 and outs['cycle'] > 0
# kth by BIT descent equals sorted order (exhaustive small multisets)
for _ in range(300):
    m = R(1, 12); o = refs.OS_S(m); vals = ri(R(0, 15), 0, m)
    for v in vals: o.insert(v)
    sv = sorted(vals); assert [o.kth(k) for k in range(1, len(sv) + 1)] == sv and o.kth(len(sv) + 1) == -1
# reverse pairs: 2*x overflow remark: 2 * 2**31 exceeds the int32 range
assert 2 * 2**31 > 2**31 - 1
# 2D BIT inclusion-exclusion and lazy tree depth
assert (len(bin(10**5)) - 2) < 20
print('claims ok', flush=True)

# ---------------------------------------------------------------- maximum sizes
def big(key, kw, check=None):
    t = time.time(); r = S[key](**kw)
    if check: assert check(r), key
    assert time.time() - t < 20, key
n = 3000
big('lru_dll', dict(init=[3000], ops=[['put', [i, i]] for i in range(3000)] + [['get', [i]] for i in range(3000)]), lambda r: r[-1] == 2999)
big('lfu', dict(init=[10**4], ops=[['put', [i, i]] for i in range(10**4)] + [['get', [i]] for i in range(10**4)]), lambda r: r[-1] == 9999)
big('time_kv', dict(init=[], ops=[['set', ['k', str(i), i + 1]] for i in range(10**5)] + [['get', ['k', 55555]]]), lambda r: r[-1] == '55554')
big('snapshot', dict(init=[50000], ops=[['set', [i % 50000, i]] if i % 2 else ['snap', []] for i in range(50000)]))
big('bit_point_range', dict(init=[list(range(10**5))], ops=[['update', [i, 0]] for i in range(10**5)] + [['sumRange', [0, 10**5 - 1]]]), lambda r: r[-1] == 0)
big('lazy_range', dict(init=[[0] * 10**5], ops=[['add', [i, 10**5 - 1, 1]] for i in range(0, 10**5, 50)] + [['sum', [0, 10**5 - 1]]]), lambda r: r[-1] == sum(10**5 - i for i in range(0, 10**5, 50)))
big('segtree_min', dict(init=[list(range(10**5, 0, -1))], ops=[['query', [0, 10**5 - 1]]]), lambda r: r == [1])
big('bit_2d', dict(init=[[[1] * 200 for _ in range(200)]], ops=[['sumRegion', [0, 0, 199, 199]]]), lambda r: r == [40000])
big('sparse_table', dict(nums=ri(10**5, -10**9, 10**9), queries=[[0, 10**5 - 1]] * 10**5))
big('inversions_bit', dict(nums=list(range(10**5, 0, -1))), lambda r: r[0] == 10**5 * (10**5 - 1) // 2)
big('count_smaller', dict(nums=ri(10**5, -10**9, 10**9)))
big('coord_compress', dict(values=ri(10**5, -10**18, 10**18)))
big('reverse_pairs', dict(nums=ri(5 * 10**4, -2**31, 2**31)))
big('calendar_k', dict(bookings=[[R(0, 5 * 10**8), 5 * 10**8 + R(1, 5 * 10**8)] for _ in range(400)]))
big('skyline', dict(buildings=sorted([[l, l + R(1, 1000), R(1, 2**31 - 1)] for l in ri(10**4, 0, 10**6)])))
big('connect_cities', dict(n=10**4, built=[], edges=[[i, i + 1, 1] for i in range(10**4 - 1)] + [[R(0, 9999), R(0, 9999), R(1, 9)] for _ in range(4 * 10**4)]), lambda r: r == 9999)
big('sp_coupon', dict(n=10**4, edges=[[i, i + 1, 10**6] for i in range(10**4 - 1)] + [[R(0, 9999), R(0, 9999), R(1, 10**6)] for _ in range(4 * 10**4)]))
big('itinerary', dict(tickets=[['JFK', 'ATL'], ['ATL', 'JFK']] * 150), lambda r: len(r) == 301)
big('bipartite_matching', dict(L=300, R=300, edges=[[i, i] for i in range(300)] + [[i, i + 1] for i in range(299)]), lambda r: r == [300, True])
big('parallel_time', dict(n=5 * 10**4, relations=[[i, i + 1] for i in range(1, 5 * 10**4)], time=[10**4] * (5 * 10**4)), lambda r: r[0] == 5 * 10**8)
big('reverse_delete', dict(n=10**5, edges=path, removals=list(range(0, 10**5 - 1, 2))), lambda r: r[0] == 1 and r[-1] == 5 * 10**4 + 1)
# chain of 300 augmenting paths stays below the recursion limit
big('bipartite_matching', dict(L=300, R=300, edges=[[i, 299 - i] for i in range(300)] + [[i, 298 - i] for i in range(299)]))
print('ALL OK in %.1fs' % (time.time() - t0))
