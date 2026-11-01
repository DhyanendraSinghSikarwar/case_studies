# Runs EVERY example rendered into the Part 8 prompts (qs.py is the single source of truth) against reference solutions
# (refs.py), cross-checks each reference against independent brute force / validators, and tests every bound, uniqueness
# and equivalence claim made in the prompts exhaustively on small inputs. Run: python3 -I check_examples.py
import sys, os, random, itertools, heapq, copy, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
from qs import QS
import refs
from refs import S, B, OK
random.seed(8)
t0 = time.time()

# ---- 1. every example in every prompt
for st, d, key, text, exs, asked in QS:
    for kw, exp in exs:
        got = S[key](**copy.deepcopy(kw))
        if key in OK: assert OK[key](kw, got) and OK[key](kw, exp), (key, kw, got, exp)
        else: assert got == exp, (key, kw, got, exp)
        if key in B and key not in OK and key != 'quickselect': assert B[key](**copy.deepcopy(kw)) == exp, ('brute', key, kw)
    if key == 'queue_reconstruct':
        for kw, exp in exs: assert sorted(refs.pairs_of([p[0] for p in exp]) if False else [list(p) for p in exp]) == sorted(kw['people']) and [list(p) for p in refs.pairs_of([p[0] for p in exp])] == exp
print('examples ok', sum(len(q[4]) for q in QS))

R = random.randint
def rintervals(n, hi=12, closed=False):
    out = []
    for _ in range(n):
        a = R(0, hi); b = R(a if closed else a + 1, hi + (0 if closed else 1)); out.append([a, b])
    return out

# ---- 2. heapq_layout and build_heap
def manual_push(vals):
    h = []
    for v in vals:
        h.append(v); i = len(h) - 1
        while i > 0 and h[(i - 1) // 2] > h[i]: h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]; i = (i - 1) // 2
    return h
diff = tot = 0
for _ in range(3000):
    vals = [R(0, 20) for _ in range(R(0, 14))]
    pushed, hf, pops, top = S['heapq_layout'](vals)
    assert pushed == manual_push(vals) and refs.is_heap(hf) and sorted(hf) == sorted(vals) and refs.is_heap(pushed)
    assert pops == sorted(vals)[:3] and top == sorted(vals, reverse=True)[:3]
    tb = refs.s_build_heap(vals)
    assert tb[2] == pushed and refs.is_heap(tb[0]) and sorted(tb[0]) == sorted(vals)
    tot += 1; diff += tb[0] != hf
print(f'CPython heapify layout differs from textbook sift-down layout in {diff} of {tot} random lists (so the prompt asks for the textbook build separately)')
pc = lambda n: bin(n).count('1')
def heights_sum(n):
    return sum((n - 1 - i).bit_length() - 0 if False else 0 for i in range(n)) if False else None
def node_height(i, n):
    h = 0
    while 2 * i + 1 < n: i = 2 * i + 1; h += 1
    return h
for n in range(0, 2001): assert sum(node_height(i, n) for i in range(n)) == n - pc(n), n
worst = {}
for n in range(0, 9):
    mx = 0
    for p in itertools.permutations(range(n)):
        r = refs.s_build_heap(list(p)); assert refs.is_heap(r[0]); mx = max(mx, r[1]); assert r[1] <= n - pc(n)
    worst[n] = (mx, n - pc(n))
print('max bottom-up swaps over all permutations (max, bound n-popcount):', worst)
for n in (1000, 1023, 1024, 4096):
    r = refs.s_build_heap(list(range(n, 0, -1))); assert r[1] <= n - pc(n) and r[3] <= n * n.bit_length()
    print('descending n', n, 'bottom-up swaps', r[1], 'one-by-one swaps', r[3], 'n-popcount', n - pc(n))
assert refs.s_build_heap(list(range(1024, 0, -1)))[3] > 4 * refs.s_build_heap(list(range(1024, 0, -1)))[1]

# ---- 3. intervals
for _ in range(1500):
    iv = rintervals(R(0, 8), 10, closed=True) or [[1, 1]]
    assert S['merge_intervals'](copy.deepcopy(iv)) == B['merge_intervals'](iv)
    new = rintervals(1, 10, closed=True)[0]
    base = refs.s_merge_intervals(copy.deepcopy(iv))
    # make base strictly disjoint, non-touching, sorted for insert
    base2 = []
    for s, e in base:
        if base2 and s <= base2[-1][1] + 0: base2[-1][1] = max(base2[-1][1], e)
        else: base2.append([s, e])
    assert S['insert_interval'](copy.deepcopy(base2), new) == B['insert_interval'](base2, new)
    m = rintervals(R(0, 7), 12)
    assert S['meeting_rooms1'](m) == B['meeting_rooms1'](m)
    assert refs.s_meeting_rooms2(m) == refs.s_meeting_rooms2_sweep(m) == B['meeting_rooms2'](m)
    assert S['non_overlap'](m) == B['non_overlap'](m) if m else True
    a = refs.s_merge_intervals(rintervals(R(0, 4), 14, closed=True)); b = refs.s_merge_intervals(rintervals(R(0, 4), 14, closed=True))
    # disjoint non-touching lists
    def sep(l):
        out = []
        for s, e in l:
            if out and s <= out[-1][1] + 1 and False: pass
            out.append([s, e])
        return out
    assert S['intersections'](a, b) == B['intersections'](a, b), (a, b)
    ev = [[R(1, 6), 0] for _ in range(R(1, 6))]
    for e_ in ev: e_[1] = R(e_[0], 7)
    assert S['max_events'](copy.deepcopy(ev)) == B['max_events'](ev), ev
    pts = [[x, R(x, 8)] for x in [R(0, 8) for _ in range(R(1, 6))]]
    assert S['balloons'](pts) == B['balloons'](pts)
    sched = [refs.s_merge_intervals([[x, y] for x, y in rintervals(R(1, 3), 9)]) for _ in range(R(1, 3))]
    sched = [[iv for iv in e] for e in sched]
    assert S['free_time'](sched) == B['free_time'](sched), sched
# sweep tie order claim: +1 before -1 at equal time overcounts touching meetings
ev = sorted([(s, 1) for s, e in [[1, 5], [5, 8]]] + [(e, -1) for s, e in [[1, 5], [5, 8]]], key=lambda x: (x[0], -x[1]))
cur = best = 0
for t, dd in ev: cur += dd; best = max(best, cur)
assert best == 2 and refs.s_meeting_rooms2_sweep([[1, 5], [5, 8]]) == 1
for _ in range(300):    # intersections on lists that are disjoint and non-touching, as the prompt promises
    def gen():
        out = []; x = R(0, 3)
        for _ in range(R(0, 4)):
            s = x + R(0, 3); e = s + R(0, 4); out.append([s, e]); x = e + 2
        return out
    a, b = gen(), gen(); assert S['intersections'](a, b) == B['intersections'](a, b)
print('intervals ok')

# ---- 4. heaps and streams
for _ in range(2000):
    n = R(1, 9); nums = [R(-5, 5) for _ in range(n)]; k = R(1, n)
    assert S['kth_largest'](nums, k) == B['kth_largest'](nums, k)
    kk = R(1, 4); base = [R(-5, 5) for _ in range(R(max(0, kk - 1), kk + 2))]; adds = [R(-5, 5) for _ in range(R(1, 6))]
    assert S['kth_stream'](kk, base, adds) == B['kth_stream'](kk, base, adds)
    ls = [sorted(R(-5, 9) for _ in range(R(0, 5))) for _ in range(R(0, 6))]
    assert S['merge_k_arrays'](ls) == B['merge_k_arrays'](ls)
    w = [random.choice('abcd') for _ in range(R(1, 12))]; kw_ = R(1, len(set(w)))
    assert S['top_k_words'](w, kw_) == B['top_k_words'](w, kw_)
    pts = [[R(-3, 3), R(-3, 3)] for _ in range(R(1, 8))]; kc = R(1, len(pts)); assert OK['k_closest']({'points': pts, 'k': kc}, S['k_closest'](pts, kc))
    adds = [R(-9, 9) for _ in range(R(1, 12))]; assert S['median_stream'](adds) == B['median_stream'](adds)
    st = [R(1, 20) for _ in range(R(1, 7))]; assert S['last_stone'](st) == B['last_stone'](st)
    g = [R(1, 5) for _ in range(R(0, 5))]; s_ = [R(1, 5) for _ in range(R(0, 5))]; assert S['cookies'](g, s_) == B['cookies'](g, s_)
    sk = [R(1, 9) for _ in range(R(1, 6))]; assert S['sticks'](sk) == B['sticks'](sk)
    n1 = sorted(R(-4, 6) for _ in range(R(1, 4))); n2 = sorted(R(-4, 6) for _ in range(R(1, 4))); kp = R(1, len(n1) * len(n2))
    assert OK['k_pairs']({'nums1': n1, 'nums2': n2, 'k': kp}, S['k_pairs'](n1, n2, kp))
    hs = [R(1, 9) for _ in range(R(2, 8))]; br = R(0, 12); ld = R(0, 3)
    assert S['furthest_building'](hs, br, ld) == B['furthest_building'](hs, br, ld), (hs, br, ld)
    pr = [R(0, 5) for _ in range(R(1, 6))]; cp = [R(0, 7) for _ in pr]; kproj = R(0, 4); w0 = R(0, 3)
    assert S['ipo'](kproj, w0, pr, cp) == B['ipo'](kproj, w0, pr, cp)
    ls = [sorted(R(0, 9) for _ in range(R(1, 4))) for _ in range(R(1, 4))]
    assert S['smallest_range'](ls) == B['smallest_range'](ls), ls
    nm = [R(-4, 4) for _ in range(R(1, 14))]; kw2 = R(1, len(nm)); assert S['sliding_median'](nm, kw2) == B['sliding_median'](nm, kw2), (nm, kw2)
    wt = [R(1, 6) for _ in range(R(1, 8))]; cap = R(1, 14); assert S['greedy_days'](wt, cap) == B['greedy_days'](wt, cap)
    mt = sorted({R(0, 30) for _ in range(R(1, 8))}); meet = [[s, s + R(1, 8)] for s in mt]; nr = R(1, 3)
    random.shuffle(meet); assert S['rooms3'](nr, meet) == B['rooms3'](nr, meet), (nr, meet)
for n in (1, 2, 3, 7, 10, 12):
    pass
for _ in range(200):   # greedy_days monotone in capacity
    wt = [R(1, 9) for _ in range(R(1, 9))]; days = [S['greedy_days'](wt, c) for c in range(max(wt), sum(wt) + 2)]
    assert all(days[i] >= days[i + 1] for i in range(len(days) - 1)) and days[-1] == 1
# sliding median big and tie-heavy
nm = [R(0, 3) for _ in range(3000)]
for k in (1, 2, 5, 50, 3000): assert S['sliding_median'](nm, k) == B['sliding_median'](nm, k)
# huffman
for _ in range(400):
    fr = [R(1, 9) for _ in range(R(1, 7))]; assert OK['huffman']({'freqs': fr}, S['huffman'](fr)), fr
    # tie-break independence of the cost: random tie order
    h = [(f, random.random(), i) for i, f in enumerate(fr)]; heapq.heapify(h); cost = 0
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h); cost += a[0] + b[0]; heapq.heappush(h, (a[0] + b[0], random.random(), -1))
    assert cost == refs.opt_cost(fr) == sum(f * l for f, l in zip(fr, S['huffman'](fr)))
# sticks == huffman cost
for _ in range(300):
    sk = [R(1, 9) for _ in range(R(1, 6))]; assert S['sticks'](sk) == refs.opt_cost(sk)
# kth_stream guarantee
assert S['kth_stream'](3, [4, 5, 8, 2], [3])[0] == 4
print('heap questions ok')

# ---- 5. task scheduler (exhaustive-ish) and reorganize / rearrange (exhaustive)
for n in range(0, 4):
    for L in range(1, 8):
        for tasks in itertools.product('ABC', repeat=L):
            t = ''.join(tasks)
            if t != ''.join(sorted(t)): continue
            assert S['task_scheduler'](t, n) == refs.s_task_scheduler_heap(t, n) == B['task_scheduler'](t, n), (t, n)
for _ in range(300):
    t = ''.join(random.choice('ABCDE') for _ in range(R(1, 40))); n = R(0, 6)
    assert S['task_scheduler'](t, n) == refs.s_task_scheduler_heap(t, n)
cnt_imp = 0
for L in range(1, 8):
    for t in map(''.join, itertools.product('abc', repeat=L)):
        r = S['reorganize'](t); feasible = max(Counter(t).values()) <= (L + 1) // 2
        assert (r != '') == feasible and OK['reorganize']({'s': t}, r), t
        cnt_imp += not feasible
        for k in range(0, 6):
            rk = S['rearrange_k'](t, k); assert OK['rearrange_k']({'s': t, 'k': k}, rk), (t, k, rk)
        assert S['rearrange_k'](t, 2) == '' if not feasible else True
for _ in range(100):
    t = ''.join(random.choice('abcdef') for _ in range(R(1, 200))); r = S['reorganize'](t)
    assert (r != '') == (max(Counter(t).values()) <= (len(t) + 1) // 2)
    for k in (2, 3, 4):
        rk = S['rearrange_k'](t, k)
        if rk: assert OK['rearrange_k']({'s': t, 'k': k}, rk)
print('task scheduler, reorganize, rearrange ok; infeasible reorganize strings checked:', cnt_imp)

# ---- 6. jumps and gas
for _ in range(3000):
    nums = [R(0, 4) for _ in range(R(1, 9))]
    assert S['jump_game1'](nums) == B['jump_game1'](nums)
    if B['jump_game1'](nums): assert S['jump_game2'](nums) == B['jump_game2'](nums), nums
    n = R(1, 6); gas = [R(0, 5) for _ in range(n)]; cost = [R(0, 5) for _ in range(n)]
    assert S['gas_station'](gas, cost) == B['gas_station'](gas, cost), (gas, cost)
# non-uniqueness of the gas-station start
c = sum(1 for _ in [0] if B['gas_station']([1, 1], [1, 1]) == 0)
assert all(sum(1 for s in range(2) if True) for _ in [0]); 
def valid_starts(gas, cost):
    n = len(gas); out = []
    for s in range(n):
        t = 0; ok = True
        for k in range(n):
            i = (s + k) % n; t += gas[i] - cost[i]
            if t < 0: ok = False; break
        if ok: out.append(s)
    return out
assert valid_starts([1, 1], [1, 1]) == [0, 1]
multi = sum(1 for _ in range(3000) if len(valid_starts(*(lambda g: (g, [R(0, 5) for _ in g]))([R(0, 5) for _ in range(R(1, 6))]))) > 1)
print('jump and gas ok; random gas inputs with several valid starts (of 3000):', multi)

# ---- 7. greedy claims
# activity selection: earliest finish optimal; two wrong rules need >= 3 activities (times 0..6)
acts = [[a, b] for a in range(7) for b in range(a + 1, 7)]
def wrong(rule, A):
    return refs.greedy_by(A, rule)
rules = {'shortest': lambda x: (x[1] - x[0], x[0]), 'earliest_start': lambda x: (x[0], x[1])}
found = {k: None for k in rules}
for size in (1, 2, 3):
    for A in itertools.combinations_with_replacement(acts, size):
        A = list(A); opt = B['activity_selection'](A); assert S['activity_selection'](A) == opt
        for name, rule in rules.items():
            if wrong(rule, A) != opt:
                if found[name] is None: found[name] = (size, A)
assert found['shortest'] is not None and found['shortest'][0] == 3 and found['earliest_start'] is not None and found['earliest_start'][0] == 3, found
print('smallest counterexamples (size, example):', found)
for _ in range(500):
    A = rintervals(R(1, 8), 12); assert S['activity_selection'](A) == B['activity_selection'](A)
# non_overlap: sort-by-start greedy counter-example
assert refs.s_non_overlap([[1, 100], [11, 22], [1, 11], [2, 12]]) == 2
def by_start(iv):
    cnt = 0; end = -10 ** 9
    for s, e in sorted(iv):
        if s >= end: end = e
        else: cnt += 1
    return cnt
assert by_start([[1, 100], [11, 22], [1, 11], [2, 12]]) != 2 or True
bad = [A for A in ([[1, 10], [2, 3], [4, 5]],) if by_start(A) != refs.s_non_overlap(A)]
assert bad, 'start-sort counterexample'
# coin greedy: Kozen-Zaks bound exhaustive for largest coin <= 12, amounts to 200
nsys = ncx = 0
for top in range(2, 13):
    for mid in itertools.chain.from_iterable(itertools.combinations(range(2, top), r) for r in range(0, top - 1)):
        coins = [1, *mid, top]; nsys += 1
        b = B['coin_greedy'](coins); s = S['coin_greedy'](coins)
        assert b == s, (coins, b, s)
        if b != -1: ncx += 1; assert b < coins[-1] + coins[-2], coins
print('coin systems checked', nsys, 'non-canonical', ncx)
for coins in ([1, 5, 10, 25], [1, 2, 5, 10, 20, 50, 100]): assert S['coin_greedy'](coins) == -1
# also larger coins, random
for _ in range(300):
    top = R(5, 60); mid = sorted(random.sample(range(2, top), R(0, min(4, top - 2)))); coins = [1, *mid, top]
    b = B['coin_greedy'](coins); assert b == S['coin_greedy'](coins) and (b == -1 or b < coins[-1] + coins[-2])
# candy exhaustive
for n in range(1, 5):
    for r in itertools.product(range(3), repeat=n): assert S['candy'](list(r)) == B['candy'](list(r)), r
for _ in range(60):
    r = [R(0, 3) for _ in range(6)]; assert S['candy'](r) == B['candy'](r), r
# partition labels
for _ in range(600):
    s = ''.join(random.choice('abcd') for _ in range(R(1, 10))); assert S['partition_labels'](s) == B['partition_labels'](s), s
# queue reconstruction: reconstruct from random queues; uniqueness exhaustive for n <= 6 and heights 1..3
for _ in range(1000):
    q = [R(1, 5) for _ in range(R(1, 9))]; pairs = refs.pairs_of(q); sh = pairs[:]; random.shuffle(sh)
    assert [p[0] for p in S['queue_reconstruct'](sh)] == q and refs.pairs_of(q) == [list(p) for p in S['queue_reconstruct'](sh)]
for n in range(1, 7):
    groups = {}
    for q in itertools.product(range(1, 4), repeat=n):
        pr = refs.pairs_of(list(q)); assert len({tuple(p) for p in pr}) == n   # pairs are always distinct
        groups.setdefault(tuple(sorted(map(tuple, pr))), set()).add(q)
    assert all(len(v) == 1 for v in groups.values()), n
print('greedy claims ok')

# ---- 8. python heap API claims
# tie-break TypeError and the counter fix
h = []; heapq.heappush(h, (1, {'id': 'a'}))
try: heapq.heappush(h, (1, {'id': 'b'})); raise AssertionError('expected TypeError')
except TypeError: pass
ex_tasks = [[5, {'id': 'x'}], [5, {'id': 'y'}], [5, {'id': 'a'}]]
h = []
for p, pl in ex_tasks: heapq.heappush(h, (p, pl['id']))
assert [heapq.heappop(h)[1] for _ in range(3)] == ['a', 'x', 'y'] != S['tie_break'](ex_tasks)
for _ in range(500):
    tasks = [[R(0, 3), {'id': i}] for i in range(R(0, 10))]; assert S['tie_break'](tasks) == B['tie_break'](tasks)
for _ in range(500):
    ws = [''.join(random.choice('ab') for _ in range(R(1, 3))) for _ in range(R(0, 8))]
    for o in ('lex_desc', 'len_desc_lex_desc'): assert S['custom_order'](ws, o) == B['custom_order'](ws, o)
try: -'abc'; raise AssertionError
except TypeError: pass
# the (-len, w) tuple key gives 'longest first, then ascending' and heap == sorted
ws = ['pear', 'fig', 'kiwi', 'plum', 'date']; hh = [(-len(w), w) for w in ws]; heapq.heapify(hh)
assert [heapq.heappop(hh)[1] for _ in ws] == sorted(ws, key=lambda w: (-len(w), w)) == ['date', 'kiwi', 'pear', 'plum', 'fig']
# lazy deletion and pq update, random ops against brute (asserts inside the references enforce the size and pop bounds)
for _ in range(800):
    ops = []
    for _ in range(R(0, 25)): ops.append(random.choice([['push', R(0, 4)], ['push', R(0, 4)], ['remove', R(0, 4)], ['pop'], ['top'], ['size']]))
    assert S['lazy_pq'](ops) == B['lazy_pq'](ops), ops
    ops = []
    for _ in range(R(0, 25)):
        t = random.choice('abc'); ops.append(random.choice([['add', t, R(0, 3)], ['update', t, R(0, 3)], ['remove', t], ['pop'], ['size'], ['pop']]))
    assert S['pq_update'](ops) == B['pq_update'](ops), ops
# nlargest equivalence and stability, exhaustive
for L in range(0, 7):
    for sc in itertools.product(range(3), repeat=L):
        rec = [[f'n{i}', s] for i, s in enumerate(sc)]
        for k in range(1, L + 2):
            a = heapq.nlargest(k, rec, key=lambda r: r[1]); b = sorted(rec, key=lambda r: r[1], reverse=True)[:k]
            assert a == b and S['nlargest'](rec, k) == B['nlargest'](rec, k) == [r[0] for r in b]
            assert heapq.nsmallest(k, rec, key=lambda r: r[1]) == sorted(rec, key=lambda r: r[1])[:k]
# quickselect
for _ in range(1500):
    nums = [R(0, 6) for _ in range(R(1, 12))]; k = R(1, len(nums)); v, r = S['quickselect'](nums, k)
    assert v == B['quickselect'](nums, k) and 1 <= r <= len(nums)
for n in (1, 5, 50, 500): assert S['quickselect']([7] * n, max(1, n // 2)) == [7, 1] and S['quickselect'](list(range(1, n + 1)), 1) == [n, n]
print('python heap API claims ok')

# ---- 9. scale / recursion-free sanity (all solutions are iterative; sizes at the stated limits)
big = [R(-10**9, 10**9) for _ in range(10**5)]
assert S['kth_largest'](big, 500) == sorted(big)[-500]
assert len(S['sliding_median'](big, 1000)) == 10**5 - 999
assert S['merge_k_arrays']([sorted(big[i::100]) for i in range(100)]) == sorted(big)
print('ALL OK in %.1fs' % (time.time() - t0))
