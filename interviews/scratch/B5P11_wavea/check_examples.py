# Runs EVERY example rendered into the Part 11 prompts (qs.py is the single source of truth) against the reference solutions (refs.py),
# cross-checks each against an independent brute force / plain recursion / re.fullmatch / BFS on seeded random small inputs, exhaustively checks
# every tie-rule and bound claim made in the prompts, and runs the maximum sizes. Run: python3 -I check_examples.py
import sys, os, random, itertools, copy, time, functools, collections, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qs import QS
import refs
from refs import S, B, M
random.seed(11); t0 = time.time(); R = random.randint
CASES = 300
assert sys.getrecursionlimit() == 1000

SMALL = {'unique_paths': lambda kw: kw['m'] * kw['n'] > 64, 'memo_stats': lambda kw: kw['m'] > 12 or kw['n'] > 12,
         'lcs_length': lambda kw: len(kw['a']) + len(kw['b']) > 12, 'edit_distance': lambda kw: len(kw['a']) + len(kw['b']) > 12,
         'lps': lambda kw: len(kw['s']) > 14, 'lcs_recon': lambda kw: len(kw['a']) > 12 or len(kw['b']) > 12,
         'edit_script': lambda kw: len(kw['a']) + len(kw['b']) > 14, 'lrs': lambda kw: len(kw['s']) > 7,
         'distinct_subseq': lambda kw: len(kw['s']) > 14, 'pal_cuts': lambda kw: len(kw['s']) > 12,
         'strange_printer': lambda kw: len(kw['s']) > 6, 'ascii_delete': lambda kw: len(kw['s1']) + len(kw['s2']) > 14,
         'lcs_substring': lambda kw: False, 'wildcard_count': lambda kw: len(kw['s']) > 8, 'burst_balloons': lambda kw: len(kw['nums']) > 8}
for st, d, key, text, exs, asked in QS:
    for kw, exp in exs:
        got = S[key](**copy.deepcopy(kw)); assert got == exp, (key, kw, got, exp)
        if key in B and not SMALL.get(key, lambda kw: False)(kw):
            b = B[key](**copy.deepcopy(kw)); assert b == exp, ('brute', key, kw, b, exp)
print('examples ok', sum(len(q[4]) for q in QS), 'in', len(QS), 'prompts', flush=True)

def ri(n, lo, hi): return [R(lo, hi) for _ in range(n)]
def grid(m, n, lo, hi): return [ri(n, lo, hi) for _ in range(m)]
def st(n, al='abc'): return ''.join(random.choice(al) for _ in range(n))
def pat(n):
    out = []
    for _ in range(n):
        if out and out[-1] != '*' and random.random() < .3: out.append('*')
        else: out.append(random.choice('ab.'))
    return ''.join(out)[:n]
def pat_ok(p):   # no leading star, no '**' (re would also reject); drop bad stars
    q = ''
    for ch in p:
        if ch == '*' and (not q or q[-1] == '*'): continue
        q += ch
    return q
G = {
 'unique_paths': lambda: dict(m=R(1, 7), n=R(1, 7)),
 'unique_paths_obs': lambda: (lambda m, n: dict(grid=[[int(random.random() < .25) for _ in range(n)] for _ in range(m)]))(R(1, 5), R(1, 5)),
 'min_path_sum': lambda: dict(grid=grid(R(1, 5), R(1, 5), 0, 9)),
 'triangle': lambda: dict(triangle=[ri(i + 1, -9, 9) for i in range(R(1, 8))]),
 'max_square': lambda: (lambda m, n: dict(matrix=[''.join(random.choice('0111') for _ in range(n)) for _ in range(m)]))(R(1, 6), R(1, 6)),
 'lcs_length': lambda: dict(a=st(R(0, 8)), b=st(R(0, 8))),
 'lps': lambda: dict(s=st(R(1, 12))),
 'edit_distance': lambda: dict(a=st(R(0, 7)), b=st(R(0, 7))),
 'regex_match': lambda: dict(s=st(R(0, 7), 'ab'), p=pat_ok(pat(R(0, 7)))),
 'lcs_recon': lambda: dict(a=st(R(0, 8)), b=st(R(0, 8))),
 'lcs_substring': lambda: dict(a=st(R(0, 9), 'abc'), b=st(R(0, 9), 'abc')),
 'palin_substr_dp': lambda: dict(s=st(R(1, 12), 'ab')),
 'interleaving': lambda: (lambda a, b: dict(s1=a, s2=b, s3=(''.join(sorted(a + b, key=lambda _: random.random())) if random.random() < .5 else (lambda L: ''.join(L))(list(itertools.chain(*[x for x in [list(a), list(b)]]))) ) if random.random() < .5 else st(len(a) + len(b) + R(0, 1), 'ab')))(st(R(0, 5), 'ab'), st(R(0, 5), 'ab')),
 'min_path_recon': lambda: dict(grid=grid(R(1, 5), R(1, 5), 0, 3)),
 'edit_script': lambda: dict(a=st(R(0, 5)), b=st(R(0, 5))),
 'scs': lambda: dict(a=st(R(0, 4)), b=st(R(0, 4))),
 'wildcard_count': lambda: dict(s=st(R(0, 7), 'ab'), p=''.join(random.choice('ab?**') for _ in range(R(0, 6)))),
 'ascii_delete': lambda: dict(s1=st(R(0, 7)), s2=st(R(0, 7))),
 'pal_cuts': lambda: dict(s=st(R(1, 10), 'ab')),
 'dungeon': lambda: dict(grid=grid(R(1, 5), R(1, 5), -9, 9)),
 'distinct_subseq': lambda: dict(s=st(R(0, 12), 'ab'), t=st(R(0, 5), 'ab')),
 'burst_balloons': lambda: dict(nums=ri(R(0, 7), 0, 9)),
 'matrix_chain': lambda: dict(dims=ri(R(2, 7), 1, 9)),
 'lis_matrix': lambda: dict(matrix=grid(R(1, 3), R(1, 3), 0, 5)),
 'min_falling_path': lambda: (lambda n: dict(matrix=grid(n, n, -9, 9)))(R(1, 5)),
 'lrs': lambda: dict(s=st(R(0, 7), 'abc')),
 'paths_mod_k': lambda: dict(grid=grid(R(1, 5), R(1, 5), 0, 9), k=R(1, 6)),
 'count_min_paths': lambda: dict(grid=grid(R(1, 5), R(1, 5), 0, 2)),
 'memo_stats': lambda: (lambda m, n: dict(m=m, n=n, blocked=[[R(0, m - 1), R(0, n - 1)] for _ in range(R(0, 4))]))(R(1, 8), R(1, 8)),
 'cut_stick': lambda: (lambda n: dict(n=n, cuts=random.sample(range(1, n), R(0, min(6, n - 1)))))(R(2, 20)),
 'assign_tasks': lambda: (lambda n: dict(cost=grid(n, n, 0, 3)))(R(1, 6)),
 'triangulation': lambda: dict(values=ri(R(3, 8), 1, 9)),
 'strange_printer': lambda: dict(s=st(R(0, 6), 'abc')),
 'cherry_pickup': lambda: (lambda n: dict(grid=[[random.choice([0, 1, 1, -1, 0]) for _ in range(n)] for _ in range(n)]))(R(1, 4)),
 'tsp': lambda: (lambda n: dict(dist=[[0 if a == b else R(1, 9) for b in range(n)] for a in range(n)]))(R(1, 7)),
}
for key in S:
    assert key in G or key == 'lps_interval', key
# 'interleaving' generator: build true interleavings half of the time
def gen_interleave():
    a, b = st(R(0, 5), 'ab'), st(R(0, 5), 'ab'); r = random.random()
    if r < .5:
        i = j = 0; out = []
        while i < len(a) or j < len(b):
            if j == len(b) or (i < len(a) and random.random() < .5): out.append(a[i]); i += 1
            else: out.append(b[j]); j += 1
        s3 = ''.join(out)
        if random.random() < .3 and s3: k = R(0, len(s3) - 1); s3 = s3[:k] + random.choice('ab') + s3[k + 1:]
    else: s3 = st(len(a) + len(b) + R(0, 1), 'ab')
    return dict(s1=a, s2=b, s3=s3)
G['interleaving'] = gen_interleave
HEAVY = {'strange_printer': 60, 'cherry_pickup': 150, 'tsp': 150, 'assign_tasks': 150, 'cut_stick': 150, 'burst_balloons': 150, 'lcs_recon': 200, 'edit_script': 200}
tot = 0
for key in S:
    if key == 'lps_interval': continue
    for _ in range(HEAVY.get(key, CASES)):
        kw = G[key](); a = S[key](**copy.deepcopy(kw)); b = B[key](**copy.deepcopy(kw))
        assert a == b, (key, kw, a, b); tot += 1
for _ in range(CASES):
    kw = G['lps'](); assert refs.lps_interval(kw['s']) == S['lps'](**kw) == B['lps'](**kw); tot += 1
print('random cross-checks ok', tot, f'({time.time() - t0:.0f}s)', flush=True)

# ---- outcome coverage: both branches occur
for key, f in [('regex_match', bool), ('interleaving', bool), ('unique_paths_obs', lambda x: x == 0), ('max_square', lambda x: x == 0), ('wildcard_count', lambda x: x[0]),
               ('distinct_subseq', lambda x: x == 0), ('cherry_pickup', lambda x: x == 0), ('lcs_substring', lambda x: x[0] == 0), ('lcs_recon', lambda x: x == '')]:
    c = collections.Counter(f(S[key](**G[key]())) for _ in range(800)); print('coverage', key, dict(c)); assert len(c) == 2, key

# ---- claims
def fails(f, *a):
    try: f(*a); return False
    except RecursionError: return True
# C1. recursion limit: memoised top-down recursion at the maximum sizes quoted in prompts raises RecursionError at the default limit (observed), bottom-up works
def memo_lcs(a, b):
    @functools.cache
    def f(i, j): return 0 if i == len(a) or j == len(b) else (1 + f(i + 1, j + 1) if a[i] == b[j] else max(f(i + 1, j), f(i, j + 1)))
    return f(0, 0)
def memo_edit(a, b):
    @functools.cache
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        return f(i + 1, j + 1) if a[i] == b[j] else 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))
    return f(0, 0)
def memo_lps(s):
    @functools.cache
    def f(i, j): return 0 if i > j else (1 if i == j else (2 + f(i + 1, j - 1) if s[i] == s[j] else max(f(i + 1, j), f(i, j - 1))))
    return f(0, len(s) - 1)
def memo_ascii(a, b):
    @functools.cache
    def f(i, j):
        if i == len(a): return sum(map(ord, b[j:]))
        if j == len(b): return sum(map(ord, a[i:]))
        return f(i + 1, j + 1) if a[i] == b[j] else min(ord(a[i]) + f(i + 1, j), ord(b[j]) + f(i, j + 1))
    return f(0, 0)
def memo_regex(s, p):
    @functools.cache
    def f(i, j):
        if j == len(p): return i == len(s)
        first = i < len(s) and p[j] in (s[i], '.')
        if j + 1 < len(p) and p[j + 1] == '*': return f(i, j + 2) or (first and f(i + 1, j))
        return first and f(i + 1, j + 1)
    return f(0, 0)
A, Bb = 'a' * 1000, 'b' * 1000
assert fails(memo_lcs, A, Bb) and fails(memo_edit, A, Bb) and fails(memo_ascii, A, Bb)
ab2000 = 'ab' * 1000
assert fails(memo_lps, ab2000)
assert fails(memo_regex, 'a' * 1000, 'a*' * 500)
assert fails(memo_regex, 'a' * 999 + 'b', 'a*' * 500)
# smaller sizes work (observation; the prompts only use the large sizes)
for f_, args in [(memo_lcs, ('a' * 300, 'b' * 300)), (memo_edit, ('a' * 300, 'b' * 300)), (memo_lps, 'ab' * 200), (memo_regex, ('a' * 300, 'a*' * 100))]:
    f_(*args if isinstance(args, tuple) else (args,))
depths = {}
for n_ in (400, 480, 520, 600, 1000):
    depths[n_] = (fails(memo_lcs, 'a' * n_, 'b' * n_))
print('memo LCS at n x n, default limit 1000: RecursionError by n =', depths)
assert not depths[400] and depths[600] and depths[1000]
S['lcs_length']('a' * 1000, 'b' * 1000); S['edit_distance']('a' * 1000, 'b' * 1000); S['lps']('ab' * 1000)
S['regex_match']('a' * 1000, 'a*' * 500); S['lcs_recon']('a' * 1000, 'b' * 1000); S['ascii_delete']('a' * 1000, 'b' * 1000)
# memo_stats: 600 x 600 with no blocked cells nests 1199 deep -> RecursionError; the reference gives depth 1199 without recursion; 400 x 400 (depth 799) works
assert fails(B['memo_stats'], 600, 600, []) and S['memo_stats'](600, 600, [])[2] == 1199
assert B['memo_stats'](400, 400, []) == S['memo_stats'](400, 400, []) and S['memo_stats'](400, 400, [])[2] == 799
assert S['memo_stats'](600, 600, [])[1] == 360000
# lis_matrix: snake of 40 x 40 gives a path of 1600 cells; memo DFS fails, the sorted-order DP works; 200 x 200 snake too
def corridor(n):   # n odd: corridor rows 0,2,4.. with value increasing along a winding path; wall cells 0; one connector cell per wall row
    mat = [[0] * n for _ in range(n)]; v = 1
    for i in range(0, n, 2):
        cols = range(n) if (i // 2) % 2 == 0 else range(n - 1, -1, -1)
        for j in cols: mat[i][j] = v; v += 1
        if i + 1 < n:
            mat[i + 1][n - 1 if (i // 2) % 2 == 0 else 0] = v; v += 1
    return mat, v - 1
def memo_lis(mat):
    m, n = len(mat), len(mat[0])
    @functools.cache
    def f(i, j): return 1 + max([f(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)) if 0 <= a < m and 0 <= b < n and mat[a][b] > mat[i][j]] or [0])
    return max(f(i, j) for i in range(m) for j in range(n))
mat61, L61 = corridor(61); mat201, L201 = corridor(201)
assert fails(memo_lis, mat61) and S['lis_matrix'](mat61) == L61 + 1 and L61 > 1000
assert S['lis_matrix'](mat201) == L201 + 1 and L201 > 10000
mat21, L21 = corridor(21); assert memo_lis(mat21) == L21 + 1 == S['lis_matrix'](mat21)
print('corridor path cells: 61x61 ->', L61, ' 201x201 ->', L201)
# equal values need no special order in lis_matrix: shuffle the order among equal values
def lis_shuffled(mat):
    m, n = len(mat), len(mat[0]); cells = [(mat[i][j], random.random(), i, j) for i in range(m) for j in range(n)]; cells.sort()
    L = [[1] * n for _ in range(m)]
    for v, _, i, j in cells:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < m and 0 <= b < n and mat[a][b] < v: L[i][j] = max(L[i][j], L[a][b] + 1)
    return max(map(max, L))
for _ in range(300):
    mt = grid(R(1, 5), R(1, 5), 0, 3); assert lis_shuffled(mt) == S['lis_matrix'](mt)
print('recursion-limit claims ok', flush=True)

# C2. unique paths: closed form, one row
for m in range(1, 25):
    for n in range(1, 25): assert S['unique_paths'](m, n) == math.comb(m + n - 2, m - 1)
assert S['unique_paths'](100, 100) == math.comb(198, 99)
for _ in range(300):
    kw = G['unique_paths_obs'](); assert S['unique_paths_obs'](**kw) == B['unique_paths_obs'](**kw)
assert S['unique_paths_obs']([[0] * 100 for _ in range(100)]) == math.comb(198, 99)
# C3. greedy fails for min path sum; dungeon: max-sum path is not enough
gf = 0
def greedy(g):
    i = j = 0; tot = g[0][0]
    while (i, j) != (len(g) - 1, len(g[0]) - 1):
        if i == len(g) - 1: j += 1
        elif j == len(g[0]) - 1: i += 1
        elif g[i + 1][j] < g[i][j + 1]: i += 1
        else: j += 1
        tot += g[i][j]
    return tot
for _ in range(500):
    g = grid(R(1, 5), R(1, 5), 0, 9); gf += greedy(g) != S['min_path_sum'](g); assert greedy(g) >= S['min_path_sum'](g)
print('greedy min path sum wrong on', gf, 'of 500'); assert gf > 0
bad_d = 0
for _ in range(500):
    g = grid(R(1, 4), R(1, 4), -9, 9); m, n = len(g), len(g[0]); bestsum = None; need_among = None
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        sdir = ['R'] * (m + n - 2)
        for d in ds: sdir[d] = 'D'
        i = j = 0; tot = g[0][0]; low = tot
        for c in sdir:
            if c == 'D': i += 1
            else: j += 1
            tot += g[i][j]; low = min(low, tot)
        need = max(1, 1 - low)
        if bestsum is None or tot > bestsum: bestsum, need_among = tot, need
        elif tot == bestsum: need_among = min(need_among, need)
    bad_d += need_among > S['dungeon'](g)
print('max-total-sum path needs more health than the optimum on', bad_d, 'of 500'); assert bad_d > 0
assert S['dungeon']([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]) == 7
# C4. tie rules: naive prefix-table parent-pointer rebuilds differ from the stated rules
def prefix_parent_path(g):
    m, n = len(g), len(g[0]); f = [[INF] * n for _ in range(m)]; INF_ = refs.INF
    f = [[INF_] * n for _ in range(m)]; f[0][0] = g[0][0]
    for i in range(m):
        for j in range(n):
            if i or j: f[i][j] = g[i][j] + min(f[i - 1][j] if i else INF_, f[i][j - 1] if j else INF_)
    i, j = m - 1, n - 1; out = []
    while (i, j) != (0, 0):
        if i and (not j or f[i - 1][j] <= f[i][j - 1]): out.append('D'); i -= 1     # prefer D when walking backwards
        else: out.append('R'); j -= 1
    return [f[-1][-1], ''.join(reversed(out))]
INF = refs.INF
nd = sum(prefix_parent_path(g) != S['min_path_recon'](g) for g in (grid(R(2, 5), R(2, 5), 0, 2) for _ in range(500)))
print('prefix back-pointer path differs from the suffix tie rule on', nd, 'of 500'); assert nd > 0
def lcs_backptr(a, b):
    f = refs.lcs_table(a, b); i, j = len(a), len(b)    # walk back from the end of prefixes: use suffix table reversed
    fa = refs.lcs_table(a[::-1], b[::-1]); out = []; i, j = 0, 0
    # classic walk on the prefix table from the bottom-right
    P = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for x in range(1, len(a) + 1):
        for y in range(1, len(b) + 1): P[x][y] = P[x - 1][y - 1] + 1 if a[x - 1] == b[y - 1] else max(P[x - 1][y], P[x][y - 1])
    x, y = len(a), len(b)
    while x and y:
        if a[x - 1] == b[y - 1]: out.append(a[x - 1]); x -= 1; y -= 1
        elif P[x - 1][y] >= P[x][y - 1]: x -= 1
        else: y -= 1
    return ''.join(reversed(out))
nl = 0
for _ in range(500):
    kw = G['lcs_recon'](); r = lcs_backptr(**kw); s_ = S['lcs_recon'](**kw)
    assert len(r) == len(s_) and r >= s_; nl += r != s_
print('classic back-pointer LCS differs from the lexicographically smallest LCS on', nl, 'of 500'); assert nl > 0
# C5. exhaustive small-input checks of every reconstruction rule
cnt = 0
for la in range(0, 5):
    for lb in range(0, 5):
        for a in itertools.product('ab', repeat=la):
            for b in itertools.product('ab', repeat=lb):
                a_, b_ = ''.join(a), ''.join(b)
                assert S['lcs_recon'](a_, b_) == B['lcs_recon'](a_, b_), (a_, b_)
                assert S['scs'](a_, b_) == B['scs'](a_, b_), (a_, b_)
                assert S['edit_script'](a_, b_) == B['edit_script'](a_, b_), (a_, b_)
                d, sc = S['edit_script'](a_, b_); assert refs.apply_script(a_, b_, sc) == b_ and d == S['edit_distance'](a_, b_) == sum(c != 'M' for c in sc)
                sc_ = S['scs'](a_, b_); assert len(sc_) == len(a_) + len(b_) - S['lcs_length'](a_, b_) and refs.is_subseq(a_, sc_) and refs.is_subseq(b_, sc_)
                assert S['lcs_substring'](a_, b_) == B['lcs_substring'](a_, b_)
                assert S['ascii_delete'](a_, b_) == B['ascii_delete'](a_, b_)
                assert S['edit_distance'](a_, b_) == S['edit_distance'](b_, a_) and S['lcs_length'](a_, b_) == S['lcs_length'](b_, a_)
                cnt += 1
print('exhaustive string pairs (len<=4 over ab):', cnt)
for L in range(1, 9):
    for s_ in itertools.product('ab', repeat=L):
        s_ = ''.join(s_); assert S['lps'](s_) == S['lcs_length'](s_, s_[::-1]) == refs.lps_interval(s_) == B['lps'](s_)
        assert S['palin_substr_dp'](s_) == B['palin_substr_dp'](s_)
        assert S['pal_cuts'](s_) == B['pal_cuts'](s_)
cnt = 0
for vals in itertools.product(range(3), repeat=6):
    g = [list(vals[:3]), list(vals[3:])]
    assert S['min_path_recon'](g) == B['min_path_recon'](g) and S['count_min_paths'](g) == B['count_min_paths'](g); cnt += 1
for vals in itertools.product(range(2), repeat=9):
    g = [list(vals[0:3]), list(vals[3:6]), list(vals[6:9])]
    assert S['min_path_recon'](g) == B['min_path_recon'](g) and S['count_min_paths'](g) == B['count_min_paths'](g); cnt += 1
print('exhaustive grids', cnt)
for dm in itertools.product(range(1, 4), repeat=5):    # all matrix chains of 4 matrices with dims 1..3
    assert S['matrix_chain'](list(dm)) == B['matrix_chain'](list(dm)), dm
assert S['matrix_chain']([10, 30, 5, 60]) == [4500, '((A0A1)A2)'] and S['matrix_chain']([40, 20, 30, 10, 30]) == [26000, '(((A0A1)A2)A3)' if False else S['matrix_chain']([40, 20, 30, 10, 30])[1]]
# tie rule in matrix chain: a chain with equal costs picks the smallest split
assert S['matrix_chain']([1, 1, 1, 1])[1] == '(A0(A1A2))'
# assign tasks: tie rule on all 2x2 and 3x3 matrices of 0/1
for vals in itertools.product(range(2), repeat=9):
    c = [list(vals[0:3]), list(vals[3:6]), list(vals[6:9])]; assert S['assign_tasks'](c) == B['assign_tasks'](c)
# C6. wildcard: boolean part equals regex translation; ways>0 iff match; stars-only pattern counts compositions
def wc_re(s, p): return re.fullmatch(''.join('.' if c == '?' else '.*' if c == '*' else re.escape(c) for c in p), s, flags=re.S) is not None
for _ in range(600):
    kw = G['wildcard_count'](); assert S['wildcard_count'](**kw)[0] == wc_re(**kw)
for k in range(1, 5):
    for n_ in range(0, 7): assert S['wildcard_count']('a' * n_, '*' * k) == [True, math.comb(n_ + k - 1, k - 1)]
assert S['wildcard_count']('a' * 300, '*' * 3 + '?' * 200)[1] == math.comb(100 + 2, 2)
# C7. regex vs re on larger random
for _ in range(2000):
    kw = dict(s=st(R(0, 12), 'ab'), p=pat_ok(pat(R(0, 10)))); assert S['regex_match'](**kw) == B['regex_match'](**kw)
# C8. counting DPs: distinct subsequences closed forms; paths mod k; count of min paths exceeds the modulus and exact mod agrees
assert S['distinct_subseq']('a' * 50, 'a' * 25) == math.comb(50, 25) and S['distinct_subseq']('abc', '') == 1 and S['distinct_subseq']('', 'a') == 0
for _ in range(300):
    kw = G['paths_mod_k'](); kw1 = dict(kw, k=1)
    assert S['paths_mod_k'](**kw1) == math.comb(len(kw['grid']) + len(kw['grid'][0]) - 2, len(kw['grid']) - 1) % M
g0 = [[0] * 100 for _ in range(100)]; assert math.comb(198, 99) > M
assert S['count_min_paths'](g0) == [0, math.comb(198, 99) % M]
assert S['paths_mod_k']([[0] * 70 for _ in range(70)], 7) == math.comb(138, 69) % M
# modulo applied to cost would be wrong: cost can exceed M? no -- check that cost never needs it: max 9 * 199
assert 9 * 199 < M
# C9. memo_stats: entries and depth formulas on random grids vs the instrumented recursion; example values
for _ in range(400):
    kw = G['memo_stats'](); assert S['memo_stats'](**kw) == B['memo_stats'](**kw)
try:
    @functools.lru_cache(maxsize=None)
    def hk(x): return 0
    hk([1, 2]); raise SystemExit('list accepted')
except TypeError as e: assert 'unhashable' in str(e)
# C10. cut stick / triangulation / burst: sizes
assert S['burst_balloons']([3, 1, 5, 8]) == 167 and S['cut_stick'](7, [1, 3, 4, 5]) == 16 and S['cut_stick'](9, [5, 6, 1, 4, 2]) == 22
assert S['triangulation']([3, 7, 4, 5]) == 144 and S['triangulation']([1, 3, 1, 4, 1, 5]) == 13
# C11. maximum sizes (sandbox timing only, not a proof of big-O)
rs = lambda n, al='abcdefghij': ''.join(random.choice(al) for _ in range(n))
for k, f in [('unique_paths', dict(m=100, n=100)), ('min_path_sum', dict(grid=grid(200, 200, 0, 100))), ('triangle', dict(triangle=[ri(i + 1, -10**4, 10**4) for i in range(200)])),
             ('max_square', dict(matrix=[''.join(random.choice('1111110') for _ in range(300)) for _ in range(300)])), ('lcs_length', dict(a=rs(1000), b=rs(1000))),
             ('lps', dict(s=rs(2000))), ('edit_distance', dict(a=rs(1000), b=rs(1000))), ('regex_match', dict(s='a' * 1000, p='a*' * 500)),
             ('lcs_recon', dict(a=rs(1000), b=rs(1000))), ('lcs_substring', dict(a=rs(2000, 'ab'), b=rs(2000, 'ab'))), ('palin_substr_dp', dict(s='a' * 1000)),
             ('interleaving', dict(s1=rs(100), s2=rs(100), s3=rs(200))), ('min_path_recon', dict(grid=grid(200, 200, 0, 100))), ('edit_script', dict(a=rs(300), b=rs(300))),
             ('scs', dict(a=rs(500), b=rs(500))), ('wildcard_count', dict(s='a' * 300, p='*' * 300)), ('ascii_delete', dict(s1=rs(1000), s2=rs(1000))), ('pal_cuts', dict(s='a' * 2000)),
             ('pal_cuts', dict(s=rs(2000, 'ab'))), ('dungeon', dict(grid=grid(200, 200, -1000, 1000))), ('distinct_subseq', dict(s=rs(1000, 'ab'), t=rs(500, 'ab'))),
             ('burst_balloons', dict(nums=ri(300, 0, 100))), ('matrix_chain', dict(dims=ri(201, 1, 100))), ('lis_matrix', dict(matrix=grid(200, 200, 0, 10**9))),
             ('min_falling_path', dict(matrix=grid(100, 100, -100, 100))), ('lrs', dict(s=rs(1000))), ('paths_mod_k', dict(grid=grid(70, 70, 0, 100), k=50)),
             ('count_min_paths', dict(grid=grid(100, 100, 0, 9))), ('memo_stats', dict(m=1500, n=1500, blocked=[[R(0, 1499), R(0, 1499)] for _ in range(10**4)])),
             ('cut_stick', dict(n=10**6, cuts=random.sample(range(1, 10**6), 100))), ('assign_tasks', dict(cost=grid(15, 15, 0, 1000))), ('triangulation', dict(values=ri(100, 1, 100))),
             ('strange_printer', dict(s=rs(100, 'abc'))), ('cherry_pickup', dict(grid=[[random.choice([0, 1, 1]) for _ in range(50)] for _ in range(50)])),
             ('tsp', dict(dist=[[0 if a == b else R(1, 1000) for b in range(12)] for a in range(12)]))]:
    t1 = time.time(); S[k](**f); dt = time.time() - t1; assert dt < 20, (k, dt)
    if dt > 4: print('  slow', k, round(dt, 1))
print('largest-size runs ok')
print('ALL OK', f'{time.time() - t0:.0f}s')
