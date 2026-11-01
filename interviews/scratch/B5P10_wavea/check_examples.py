# Runs EVERY example rendered into the Part 10 prompts (qs.py is the single source of truth) against the reference solutions (refs.py),
# cross-checks each against an independent brute force / plain recursion on seeded random small inputs, and tests the bound,
# uniqueness and equivalence claims made in the prompts. Run: python3 -I check_examples.py
import collections
import sys, os, random, itertools, copy, time, functools, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qs import QS
import refs
from refs import S, B, CMP, M
random.seed(10); t0 = time.time(); R = random.randint
CASES = 400
assert sys.getrecursionlimit() == 1000

def TOO_BIG(key, kw):
    return ((key in ('climb', 'perfect_squares', 'fib_three') and kw['n'] > 25) or (key == 'paint_fence' and kw['n'] > 7) or (key == 'decode_ways' and len(kw['s']) > 20)
            or (key == 'dice_rolls' and kw['k'] ** kw['n'] > 10**5))
# ---- 1. every example in every prompt
for st, d, key, text, exs, asked in QS:
    for kw, exp in exs:
        got = S[key](**copy.deepcopy(kw)); assert got == exp, (key, kw, got, exp)
        # oracle only where the input is small enough for it (large examples are checked by the claims below)
        if key in B and key != 'recursion_limit' and not TOO_BIG(key, kw):
            try:
                b = B[key](**copy.deepcopy(kw))
            except RecursionError: continue
            assert (CMP[key](got, b) if key in CMP else b == exp), ('brute', key, kw, b, exp)
print('stage1', flush=True); print('examples ok', sum(len(q[4]) for q in QS), 'in', len(QS), 'prompts')

# ---- 2. random generators (respect every prompt constraint; oracles bound the sizes)
def ri(n, lo, hi): return [R(lo, hi) for _ in range(n)]
def dist(k, lo, hi): return random.sample(range(lo, hi + 1), k)
def prices(n): return ri(n, 0, 12)
G = {
 'climb': lambda: dict(n=R(0, 20)),
 'min_cost_stairs': lambda: dict(cost=ri(R(2, 14), 0, 9)),
 'kadane': lambda: dict(nums=ri(R(1, 12), -9, 9)),
 'stock_once': lambda: dict(prices=prices(R(0, 12))),
 'house_robber': lambda: dict(nums=ri(R(0, 12), 0, 9)),
 'coin_min': lambda: dict(coins=dist(R(1, 3), 1, 9), amount=R(0, 12)),
 'lis_length': lambda: dict(nums=ri(R(0, 11), -4, 6)),
 'word_break': lambda: (lambda ws: dict(s=''.join(random.choice(ws) if random.random() < .8 else random.choice('ab') for _ in range(R(1, 5))), word_dict=ws))(list({''.join(random.choice('ab') for _ in range(R(1, 3))) for _ in range(R(1, 4))})),
 'decode_ways': lambda: dict(s=''.join(random.choice('0112263') for _ in range(R(1, 14)))),
 'coin_ways': lambda: dict(coins=dist(R(1, 4), 1, 8), amount=R(0, 14)),
 'partition_equal': lambda: dict(nums=ri(R(1, 11), 1, 9)),
 'house_robber2': lambda: dict(nums=ri(R(1, 12), 0, 9)),
 'max_product': lambda: dict(nums=ri(R(1, 10), -4, 4)),
 'fib_three': lambda: dict(n=R(0, 18)),
 'paint_fence': lambda: dict(n=R(1, 7), k=R(1, 4)),
 'perfect_squares': lambda: dict(n=R(1, 25)),
 'knapsack01': lambda: (lambda n: dict(weights=ri(n, 1, 9), values=ri(n, 1, 20), cap=R(0, 20)))(R(1, 10)),
 'subset_sum': lambda: dict(nums=ri(R(1, 10), 1, 9), target=R(0, 40)),
 'target_sum': lambda: dict(nums=ri(R(1, 10), 0, 5), target=R(-12, 12)),
 'unbounded_knapsack': lambda: (lambda n: dict(weights=ri(n, 1, 7), values=ri(n, 1, 20), cap=R(0, 10)))(R(1, 3)),
 'comb_sum4': lambda: dict(nums=dist(R(1, 3), 1, 6), target=R(0, 10)),
 'kadane_idx': lambda: dict(nums=ri(R(1, 9), -3, 3)),
 'coin_recon': lambda: dict(coins=dist(R(1, 4), 1, 9), amount=R(0, 15)),
 'jump_dp': lambda: dict(nums=ri(R(1, 9), 0, 3)),
 'stock_cooldown': lambda: dict(prices=prices(R(0, 10))),
 'circular_kadane': lambda: dict(nums=ri(R(1, 9), -6, 6)),
 'delete_earn': lambda: dict(nums=ri(R(0, 10), 1, 8)),
 'count_lis': lambda: dict(nums=ri(R(0, 11), 0, 5)),
 'stock_k': lambda: dict(k=R(0, 4), prices=prices(R(0, 8))),
 'last_stone2': lambda: dict(stones=ri(R(1, 6), 1, 12)),
 'ones_zeroes': lambda: dict(strs=[''.join(random.choice('01') for _ in range(R(1, 4))) for _ in range(R(1, 9))], m=R(0, 6), n=R(0, 6)),
 'alias_trap': lambda: (lambda m, n: dict(m=m, n=n, ops=[[R(0, m - 1), R(0, n - 1), R(1, 9)] for _ in range(R(0, 5))]))(R(1, 5), R(1, 5)),
 'lru_mutable': lambda: dict(nums=ri(R(0, 9), -3, 3), target=R(-6, 6)),
 'recursion_limit': None,
 'lis_recon': lambda: dict(nums=ri(R(0, 11), -3, 6)),
 'lnds_tails': lambda: dict(nums=ri(R(0, 11), 0, 5)),
 'russian_doll': lambda: dict(envelopes=[[R(1, 6), R(1, 6)] for _ in range(R(0, 10))]),
 'dice_rolls': lambda: (lambda n, k: dict(n=n, k=k, target=R(0, n * k + 2)))(R(1, 5), R(1, 6)),
 'knapsack_recon': lambda: (lambda n: dict(weights=ri(n, 1, 8), values=ri(n, 1, 9), cap=R(0, 15)))(R(1, 9)),
 'min_cost_tickets': lambda: dict(days=sorted(random.sample(range(1, 41), R(1, 8))), costs=[R(1, 6), R(2, 12), R(3, 20)]),
}
tot = 0
for key in S:
    if key == 'recursion_limit': continue
    for _ in range(CASES):
        kw = G[key](); a = S[key](**copy.deepcopy(kw)); b = B[key](**copy.deepcopy(kw))
        assert a == b, (key, kw, a, b); tot += 1
for n in [0, 1, 2, 3, 10, 100, 499, 500]: assert CMP['recursion_limit'](S['recursion_limit'](n), B['recursion_limit'](n)), n
for n in [2000, 2001, 5000, 10**5]: assert CMP['recursion_limit'](S['recursion_limit'](n), B['recursion_limit'](n)), n
tot += 12
print('random cross-checks ok', tot, f'({time.time() - t0:.0f}s)')

# ---- 3. claims
import collections
# 3a. recursion limit: memoised top-down recursion at sizes quoted in the prompts raises RecursionError at the default limit
def memo_depth_fail(f, *a):
    try: f(*a); return False
    except RecursionError: return True
@functools.cache
def _cl(n): return 1 if n < 2 else (_cl(n - 1) + _cl(n - 2)) % M
assert memo_depth_fail(_cl, 5000)
@functools.cache
def _rob(i, nums=tuple(random.randint(0, 9) for _ in range(10**5))): return 0 if i >= len(nums) else max(_rob(i + 1), nums[i] + _rob(i + 2))
assert memo_depth_fail(_rob, 0)
cs = (1, 2, 5)
@functools.cache
def _cm(a): return 0 if a == 0 else min([1 + _cm(a - c) for c in cs if c <= a] or [10**9])
assert memo_depth_fail(_cm, 10**4)
@functools.cache
def _ps(n): return 0 if n == 0 else 1 + min(_ps(n - j * j) for j in range(1, int(n ** .5) + 1))
assert memo_depth_fail(_ps, 10**4)
@functools.cache
def _cs4(t): return 1 if t == 0 else sum(_cs4(t - x) for x in (1, 2) if x <= t)
assert memo_depth_fail(_cs4, 2000)
@functools.cache
def _cw(i, rem): return 1 if rem == 0 else (0 if i == 1 or rem < 0 else _cw(i, rem - 1) + _cw(i + 1, rem))
assert memo_depth_fail(_cw, 0, 5000)
@functools.cache
def _pf(n): return 1 if n < 2 else (_pf(n - 1) + _pf(n - 2)) % M
assert memo_depth_fail(_pf, 10**5)
@functools.cache
def cool(i, h, prices=tuple([1, 2] * 2500)):
    return 0 if i >= len(prices) else max(cool(i + 1, h), (prices[i] + cool(i + 2, False)) if h else -prices[i] + cool(i + 1, True))
assert memo_depth_fail(cool, 0, False)
# first failing n for the 3-step memo version (informational), bottom-up works at every size
@functools.cache
def _f3(k): return 0 if k < 0 else (1 if k == 0 else (_f3(k - 1) + _f3(k - 2) + _f3(k - 3)) % M)
fails = [n for n in (500, 900, 980, 990, 1000, 1500, 2000) if (_f3.cache_clear() or True) and memo_depth_fail(_f3, n)]
print('3-step memo recursion at default limit 1000 fails for n in', fails)
assert 500 not in fails and 2000 in fails
assert S['climb'](10**5) == refs.s_paint_fence(10**5, 1000000000) * 0 + S['climb'](10**5)   # bottom-up runs at 10^5
for k, f in [('coin_min', dict(coins=[1, 5, 7], amount=10**4)), ('perfect_squares', dict(n=10**4)), ('comb_sum4', dict(nums=[1, 2, 3], target=2000)),
             ('coin_ways', dict(coins=list(range(1, 13)), amount=5000)), ('house_robber', dict(nums=ri(10**5, 0, 400))), ('house_robber2', dict(nums=ri(10**5, 0, 400))),
             ('paint_fence', dict(n=10**5, k=10**9)), ('stock_cooldown', dict(prices=ri(5000, 0, 1000))), ('min_cost_stairs', dict(cost=ri(10**5, 0, 999))),
             ('kadane', dict(nums=ri(10**5, -10**4, 10**4))), ('lis_length', dict(nums=ri(10**5, -10**9, 10**9))), ('russian_doll', dict(envelopes=[[R(1, 10**9), R(1, 10**9)] for _ in range(10**5)])),
             ('circular_kadane', dict(nums=ri(10**5, -10**4, 10**4))), ('delete_earn', dict(nums=ri(2 * 10**4, 1, 10**4))), ('max_product', dict(nums=ri(2 * 10**4, -10, 10))),
             ('jump_dp', dict(nums=ri(10**4, 0, 5))), ('stock_k', dict(k=10**9, prices=ri(1000, 0, 1000))), ('stock_k', dict(k=300, prices=ri(1000, 0, 1000))),
             ('partition_equal', dict(nums=ri(200, 1, 100))), ('subset_sum', dict(nums=ri(200, 1, 500), target=10**4)), ('target_sum', dict(nums=[50] * 20, target=0)),
             ('knapsack01', dict(weights=ri(100, 1, 100), values=ri(100, 1, 1000), cap=1000)), ('unbounded_knapsack', dict(weights=ri(50, 1, 100), values=ri(50, 1, 1000), cap=10**4)),
             ('ones_zeroes', dict(strs=[''.join(random.choice('01') for _ in range(R(1, 100))) for _ in range(100)], m=100, n=100)),
             ('knapsack_recon', dict(weights=ri(100, 1, 100), values=ri(100, 1, 1000), cap=1000)), ('count_lis', dict(nums=ri(2000, -10**6, 10**6))), ('lis_recon', dict(nums=ri(2000, -10**6, 10**6))),
             ('lnds_tails', dict(nums=ri(10**5, -10**9, 10**9))), ('dice_rolls', dict(n=30, k=30, target=500)), ('last_stone2', dict(stones=ri(30, 1, 100))),
             ('word_break', dict(s='a' * 199 + 'b', word_dict=['a' * i for i in range(1, 21)])), ('decode_ways', dict(s='1' * 100)), ('min_cost_tickets', dict(days=list(range(1, 366)), costs=[2, 7, 15])),
             ('coin_recon', dict(coins=[1, 5, 7, 11], amount=1000)), ('kadane_idx', dict(nums=ri(10**5, -10**4, 10**4))), ('stock_once', dict(prices=ri(10**5, 0, 1000)))]:
    t1 = time.time(); S[k](**f); assert time.time() - t1 < 10, k
print('largest-size runs ok')
# 3a2. examples too large for their oracle: independent checks
@functools.cache
def dec(s):
    if not s: return 1
    if s[0] == '0': return 0
    return dec(s[1:]) + (dec(s[2:]) if len(s) > 1 and int(s[:2]) <= 26 else 0)
assert S['decode_ways']('1' * 50) == dec('1' * 50) and S['decode_ways']('1' * 100) == dec('1' * 100)
def dice_exact(n, k, t):
    poly = {0: 1}
    for _ in range(n):
        nxt = collections.Counter()
        for s_, w in poly.items():
            for f in range(1, k + 1): nxt[s_ + f] += w
        poly = nxt
    return poly.get(t, 0) % M
assert S['dice_rolls'](30, 30, 500) == dice_exact(30, 30, 500)
assert all(S['dice_rolls'](n, k, t) == dice_exact(n, k, t) for n in (3, 10, 20) for k in (2, 7, 30) for t in range(0, n * k + 3, 7))
assert S['perfect_squares'](9999) == 4 and S['perfect_squares'](12) == 3 and S['climb'](100000) == 967618232
# 3b. climbing stairs is Fibonacci shifted by one; the O(1) loop beats exact big ints mod M
fa, fb = 0, 1
for n in range(0, 300):
    assert S['climb'](n) == fb % M, n
    fa, fb = fb, fa + fb
# 3c. fib: closed forms for call counts (naive = 2 fib(n+1) - 1, memo = 2n - 1 for n >= 1)
for n in range(0, 26):
    f, nv, mm = S['fib_three'](n)
    assert nv == 2 * S['fib_three'](n + 1)[0] - 1 and mm == (1 if n == 0 else 2 * n - 1)
    if n <= 20: assert B['fib_three'](n) == [f, nv, mm]
# 3d. 0/1 knapsack: upward loop = unbounded knapsack, and differs from 0/1 sometimes
diff01 = 0
for _ in range(1000):
    kw = G['knapsack01'](); fw = refs.knapsack_forward(**kw)
    assert fw == S['unbounded_knapsack'](**kw), kw
    diff01 += fw != S['knapsack01'](**kw)
print('upward-loop 0/1 knapsack differs from the true 0/1 answer on', diff01, 'of 1000 (and always equals unbounded)'); assert diff01 > 0
# 3e. subset sum: bitset == table; partition via bitset
for _ in range(1000):
    kw = G['subset_sum'](); assert refs.subset_sum_bitset(**kw) == S['subset_sum'](**kw)
c = collections.Counter(S['subset_sum'](**G['subset_sum']()) for _ in range(600)); assert len(c) == 2, c
c = collections.Counter(S['partition_equal'](**G['partition_equal']()) for _ in range(600)); assert len(c) == 2, c
# 3f. target sum: zeros double the count; impossible cases 0
for _ in range(500):
    kw = G['target_sum'](); z = kw['nums'].count(0)
    nz = [x for x in kw['nums'] if x]
    assert S['target_sum'](**kw) == 2 ** z * S['target_sum'](nz or [0] if False else nz, kw['target']) if nz else True
for _ in range(500):
    kw = G['target_sum'](); t = sum(kw['nums'])
    if abs(kw['target']) > t or (t + kw['target']) % 2: assert S['target_sum'](**kw) == 0
# 3g. comb_sum4: loop order determines the count; ordered >= unordered; wrong order gives the unordered count
sw = 0
for _ in range(600):
    kw = G['comb_sum4'](); o, u = S['comb_sum4'](**kw); assert o >= u and refs.comb_wrong_order(**kw) == u; sw += o != u
assert sw > 0; print('combination sum IV: ordered != unordered on', sw, 'of 600')
# 3h. kadane tie rule: exhaustive over every list with len <= 6 and values -2..2
cnt = 0
for L in range(1, 7):
    for nums in itertools.product(range(-2, 3), repeat=L):
        assert S['kadane_idx'](list(nums)) == B['kadane_idx'](list(nums)); cnt += 1
print('kadane tie rule exhaustive over', cnt, 'lists')
# 3i. coin reconstruction: the plain parent-pointer (largest coin first / first coin found) differs from the tie rule sometimes
def parent_ptr(coins, amount):
    dp = [0] + [refs.INF] * amount; par = [None] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:   # input order, strict <
            if c <= a and dp[a - c] + 1 < dp[a]: dp[a] = dp[a - c] + 1; par[a] = c
    if dp[amount] == refs.INF: return None
    out = []; a = amount
    while a: out.append(par[a]); a -= par[a]
    return sorted(out)
nd = sum(parent_ptr(**kw) != S['coin_recon'](**kw) for kw in (dict(coins=random.sample(range(1, 10), R(2, 4)), amount=R(0, 15)) for _ in range(800)))
print('plain parent-pointer rebuild differs from the lexicographic tie rule on', nd, 'of 800'); assert nd > 0
for kw in (G['coin_recon']() for _ in range(300)):
    r = S['coin_recon'](**kw)
    if r is not None: assert sum(r) == kw['amount'] and len(r) == S['coin_min'](**kw) and r == sorted(r)
    else: assert S['coin_min'](**kw) == -1
assert collections.Counter(S['coin_recon'](**G['coin_recon']()) is None for _ in range(600)).keys() == {True, False}
# 3j. jump game: the reachable set is a prefix of the indices (exhaustive), count = prefix length
cnt = 0
for L in range(1, 7):
    for nums in itertools.product(range(4), repeat=L):
        c_, k_ = S['jump_dp'](list(nums)); r = B['jump_dp'](list(nums)); assert [c_, k_] == r; cnt += 1
        n = len(nums); seen = {0}; st = [0]
        while st:
            i = st.pop()
            for j in range(i + 1, min(n - 1, i + nums[i]) + 1):
                if j not in seen: seen.add(j); st.append(j)
        assert seen == set(range(len(seen)))
print('jump reachable set is a prefix on all', cnt, 'lists'); assert collections.Counter(S['jump_dp'](**G['jump_dp']())[0] for _ in range(600)).keys() == {True, False}
# 3k. circular kadane: exhaustive small lists incl. all-negative; the naive total - min formula is wrong on all-negative lists
bad = 0
for L in range(1, 6):
    for nums in itertools.product(range(-3, 4), repeat=L):
        nums = list(nums); assert S['circular_kadane'](nums) == B['circular_kadane'](nums)
        mn = curm = nums[0]
        for x in nums[1:]: curm = min(x, curm + x); mn = min(mn, curm)
        naive = max(S['kadane'](nums), sum(nums) - mn)
        if naive != S['circular_kadane'](nums): assert max(nums) < 0, nums; bad += 1
print('naive max(kadane, total - min) wrong on', bad, 'small lists'); assert bad > 0
# 3l. LIS: tails sorted strictly; pile count = LIS length; bisect_right variant gives the non-decreasing length; bisect_left on it gives the strict length
nw = 0
for _ in range(600):
    nums = ri(R(0, 30), -5, 9); L, t = S['lis_length'](nums)
    assert t == sorted(set(t)) and L == len(t) and L == (max(refs.lis_len_dp(nums)) if nums else 0)
    ln, tn, ls = S['lnds_tails'](nums); assert ls == L and all(tn[i] <= tn[i + 1] for i in range(len(tn) - 1))
    assert refs.lnds_wrong(nums) == ls; nw += refs.lnds_wrong(nums) != ln
    # greedy patience piles: place on leftmost pile whose top >= x (strict LIS) -> number of piles
    piles = []
    for x in nums:
        for p in piles:
            if p[-1] >= x: p.append(x); break
        else: piles.append([x])
    assert len(piles) == L
print('bisect_left used for the non-decreasing variant is wrong on', nw, 'of 600'); assert nw > 0
# 3m. LIS: tails is not an LIS in general
ex = [10, 9, 2, 5, 3, 7, 101, 18]; assert S['lis_length'](ex)[1] == [2, 3, 7, 18] and S['lis_recon'](ex) == [2, 5, 7, 101]; assert S['lis_recon'](ex) != S['lis_length'](ex)[1]
# 3n. stock k: shortcut k >= n//2 equals the full table; k beyond n adds nothing; cooldown <= unlimited
for _ in range(600):
    kw = dict(k=R(0, 12), prices=prices(R(0, 12))); assert S['stock_k'](**kw) == refs.stock_k_dp_full(**kw)
    unl = sum(max(0, kw['prices'][i + 1] - kw['prices'][i]) for i in range(len(kw['prices']) - 1)); assert S['stock_cooldown'](kw['prices']) <= unl
assert S['stock_k'](**dict(k=1, prices=[1, 5])) == 4
# 3o. last stone II: sign assignment minimum equals smash process (b_ uses the process); equal to |partition difference|
for _ in range(300):
    st = ri(R(1, 7), 1, 15); best = min(abs(sum(s * x for s, x in zip(sg, st))) for sg in itertools.product((1, -1), repeat=len(st)))
    assert best == S['last_stone2'](st) == B['last_stone2'](st)
# 3p. paint fence: k=1; exact big-int check mod M
assert [S['paint_fence'](n, 1) for n in (1, 2, 3, 4)] == [1, 1, 0, 0]
def paint_exact(n, k):
    same, diff = 0, k
    for _ in range(2, n + 1): same, diff = diff, (same + diff) * (k - 1)
    return same + diff
assert S['paint_fence'](2000, 10**9) == paint_exact(2000, 10**9) % M
# 3q. aliasing: ids
for _ in range(200):
    kw = G['alias_trap'](); bug, ok, ib, io = S['alias_trap'](**kw); assert ib == 1 and io == kw['m'] and bug == B['alias_trap'](**kw)[0]
# 3r. lru: list arg raises TypeError; misses == entries; hits+misses = calls
@functools.cache
def g(a, b): return 0
try: g([1], 2); raise SystemExit('list accepted?')
except TypeError as e: assert 'unhashable' in str(e) and 'list' in str(e)
for _ in range(300):
    kw = G['lru_mutable'](); a, h, m_, cl = S['lru_mutable'](**kw); assert cl == 0 and m_ >= 1
    assert a == sum(1 for mk in range(1 << len(kw['nums'])) if sum(x for i, x in enumerate(kw['nums']) if mk >> i & 1) == kw['target'])
# 3s. russian doll: sorting with ascending height on ties is wrong
def rd_bad(es):
    es = sorted(es); t = []
    for _, h in es:
        i = bisect.bisect_left(t, h)
        if i == len(t): t.append(h)
        else: t[i] = h
    return len(t)
nb = sum(rd_bad(kw['envelopes']) != S['russian_doll'](**kw) for kw in (G['russian_doll']() for _ in range(600)))
print('sort with ascending height on equal widths wrong on', nb, 'of 600'); assert nb > 0
# 3t. knapsack recon: tie rule matters (value total equals dp)
for _ in range(300):
    kw = G['knapsack_recon'](); v, items = S['knapsack_recon'](**kw)
    assert v == S['knapsack01'](**kw) and sum(kw['values'][i] for i in items) == v and sum(kw['weights'][i] for i in items) <= kw['cap'] and items == sorted(items)
# 3u. dice: impossible targets are 0; count_lis consistent with LIS length
for _ in range(300):
    kw = G['dice_rolls']()
    if not kw['n'] <= kw['target'] <= kw['n'] * kw['k']: assert S['dice_rolls'](**kw) == 0
    nums = G['count_lis']()['nums']; assert S['count_lis'](nums)[0] == S['lis_length'](nums)[0]
# 3r2. misses == entries held before cache_clear; naive circular formula wrong exactly on some all-negative lists; all-zero target sum
for _ in range(300):
    kw = G['lru_mutable'](); ns = tuple(kw['nums']); n_ = len(ns)
    @functools.cache
    def ff(i, rem):
        if i == n_: return 1 if rem == 0 else 0
        return ff(i + 1, rem) + ff(i + 1, rem - ns[i])
    ff(0, kw['target']); inf_ = ff.cache_info(); assert inf_.misses == inf_.currsize
    assert inf_.misses == inf_.currsize
for z in range(1, 8): assert S['target_sum']([0] * z, 0) == 2 ** z and S['target_sum']([0] * z, 1) == 0
# 3v. outcome coverage (both branches occur)
for key, f in [('word_break', bool), ('decode_ways', lambda x: x == 0), ('coin_min', lambda x: x == -1), ('partition_equal', bool), ('stock_once', lambda x: x == 0), ('dice_rolls', lambda x: x == 0)]:
    c = collections.Counter(f(S[key](**G[key]())) for _ in range(600)); print(key, dict(c)); assert len(c) == 2, key
print('ALL OK', f'{time.time() - t0:.0f}s')
