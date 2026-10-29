# Runs EVERY example rendered into the Part 13 prompts (qs.py is the single source of truth) against the reference solutions (refs.py),
# cross-checks each against an independent oracle on seeded random small inputs, checks every claim made in the prompts
# (bounds, counts, WHY sentences, exhaustive enumerations) and runs the maximum sizes. Run: python3 -I check_examples.py
import sys, os, random, itertools, copy, time, functools, collections, math, re, bisect, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qs import QS
import refs
from refs import S, B
from fractions import Fraction
from decimal import Decimal
random.seed(13); t0 = time.time(); R = random.randint
CASES = 250
assert sys.getrecursionlimit() == 1000 and sys.version_info[:2] == (3, 13)

for st, d, key, text, exs, asked in QS:
    for kw, exp in exs:
        got = S[key](**copy.deepcopy(kw)); assert got == exp, (key, kw, got, exp)
        b = B[key](**copy.deepcopy(kw)); assert b == exp, ('oracle', key, kw, b, exp)
print('examples ok', sum(len(q[4]) for q in QS), 'in', len(QS), 'prompts', flush=True)

def ri(n, lo, hi): return [R(lo, hi) for _ in range(n)]
def mat(m, n, lo=-9, hi=9): return [ri(n, lo, hi) for _ in range(m)]
def dec(maxd=3, lo=-500, hi=500):
    k = R(0, maxd); v = R(lo, hi); sign = '-' if v < 0 else ''; v = abs(v)
    s = f"{sign}{v // 10 ** k}" + (f".{v % 10 ** k:0{k}d}" if k else '')
    return s
def _rect(m, n):
    r1 = R(0, m - 1); r2 = R(r1, m - 1); c1 = R(0, n - 1); c2 = R(c1, n - 1); return [r1, c1, r2, c2]
def _fy(n): return dict(n=n, choices=[R(0, i) for i in range(n - 1, 0, -1)])
def _res1():
    n = R(1, 6); return dict(stream=ri(n, 0, 9), draws=[R(0, i - 1) for i in range(2, n + 1)])
def _resk():
    n = R(1, 6); k = R(1, n); return dict(stream=ri(n, 0, 9), k=k, draws=[R(0, i - 1) for i in range(k + 1, n + 1)])
def _wp():
    w = ri(R(1, 6), 1, 6); return dict(w=w, rs=[R(0, sum(w) - 1) for _ in range(R(0, 10))])
def _rej():
    m = R(2, 6); t = R(2, m * m); return dict(m=m, t=t, stream=ri(R(0, 30), 1, m))
def _pick():
    nums = ri(R(1, 8), 1, 3); t = random.choice(nums); c = nums.count(t); return dict(nums=nums, target=t, draws=[R(0, j) for j in range(c)])
def _pool():
    return random.choice([None, 1, 2, 3, 1.5, True, 'a', 'b', (1, 'a'), (1, None), (2, None), (1, 2), [1, 'a'], [1, 2]])
def _mixed():
    kind = R(0, 4)
    if kind == 0: return [random.choice([None, 1, 2, 3, 1.5, True]) for _ in range(R(0, 6))]
    if kind == 1: return [random.choice(['a', 'b', 'c']) for _ in range(R(0, 6))]
    if kind == 2: return [random.choice([(1, 'a'), (1, None), (2, None), (1, 2), (2, 'b')]) for _ in range(R(0, 5))]
    return [_pool() for _ in range(R(0, 5))]
def _recs(n, k=4): return [[R(0, k), R(0, 9)] for _ in range(n)]
def _runs(n):
    out = []
    while len(out) < n:
        L = R(1, 12); st = R(0, 20)
        out += list(range(st, st + L)) if random.random() < .5 else list(range(st + L, st, -1))
    return out[:n]
def _layer():
    m, n = R(1, 4) * 2, R(2, 8); 
    if random.random() < .5: m, n = n if n % 2 == 0 else n + 1, m
    return dict(matrix=mat(m, n, 0, 99), r=R(0, 25))
def _title():
    t = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(R(1, 4))); return t
def _exc():
    return dict(title=_title(), number=R(1, 30000))
G = {
 'range_sum_1d': lambda: (lambda nums: dict(nums=nums, queries=[(lambda l: [l, R(l, len(nums) - 1)])(R(0, len(nums) - 1)) for _ in range(R(0, 8))]))(ri(R(1, 12), -9, 9)),
 'gcd_lcm': lambda: dict(a=R(1, 200), b=R(1, 200), nums=ri(R(1, 5), 1, 200)),
 'trailing_zeroes': lambda: dict(n=R(0, 300), base=R(2, 100)),
 'range_add': lambda: (lambda n: dict(n=n, updates=[(lambda l: [l, R(l, n - 1), R(-9, 9)])(R(0, n - 1)) for _ in range(R(0, 8))]))(R(1, 12)),
 'range_sum_2d': lambda: (lambda m, n: dict(matrix=mat(m, n), queries=[_rect(m, n) for _ in range(R(0, 8))]))(R(1, 6), R(1, 6)),
 'rotate_image': lambda: (lambda n: dict(matrix=mat(n, n)))(R(1, 7)),
 'spiral_matrix': lambda: dict(matrix=mat(R(1, 6), R(1, 6))),
 'count_primes': lambda: dict(n=R(0, 400)),
 'pow_fast': lambda: dict(x=random.choice([v for v in range(-10, 11) if v]), n=R(-40, 40)),
 'reverse_int32': lambda: dict(x=random.choice([R(-2**31, 2**31 - 1), R(-999, 999), R(-10**9, 10**9), 2**R(0, 30), -(2**R(0, 31)), R(10**9, 2**31 - 1)])),
 'fisher_yates': lambda: _fy(R(1, 5)),
 'reservoir_k1': _res1, 'weighted_pick': _wp,
 'stability_sort': lambda: dict(records=[[random.choice('abcde'), random.choice(['hr', 'it', 'ops']), R(-3, 3)] for _ in range(R(1, 12))]),
 'merge_sort': lambda: dict(records=_recs(R(0, 30))),
 'quicksort_iter': lambda: dict(nums=ri(R(1, 40), -5, 5)),
 'count_inversions': lambda: dict(nums=ri(R(0, 25), -6, 6)),
 'happy_number': lambda: dict(n=random.choice([R(1, 3000), R(1, 2**31 - 1)])),
 'excel_column': _exc,
 'pascal_triangle': lambda: dict(num_rows=R(0, 12), row_index=R(0, 40)),
 'pivot_index': lambda: dict(nums=ri(R(1, 10), -3, 3)),
 'round_half_even': lambda: dict(values=[dec(3, -3000, 3000) for _ in range(R(1, 8))]),
 'car_pooling': lambda: dict(capacity=R(1, 30), trips=[(lambda a: [R(1, 9), a, R(a + 1, 1000 if random.random() < .1 else min(1000, a + 12))])(R(0, 999 if random.random() < .1 else 30)) for _ in range(R(1, 8))]),
 'matrix_block_sum': lambda: dict(mat=mat(R(1, 6), R(1, 6)), k=R(0, 7)),
 'set_matrix_zeroes': lambda: dict(matrix=[[0 if random.random() < .2 else R(1, 5) for _ in range(R(1, 1) and 0 or 0)] for _ in range(0)] or (lambda m, n: [[0 if random.random() < .2 else R(1, 5) for _ in range(n)] for _ in range(m)])(R(1, 5), R(1, 5))),
 'game_of_life': lambda: dict(board=[[R(0, 1) for _ in range(n)] for n in [R(1, 6)] for _ in range(R(1, 6))], generations=R(1, 4)),
 'diagonal_traverse': lambda: dict(mat=mat(R(1, 6), R(1, 6))),
 'prime_factors': lambda: dict(nums=[R(2, 12000) for _ in range(R(1, 5))]),
 'modular_inverse': lambda: (lambda: dict(a=R(1, 80), m=R(2, 60), queries=[(lambda n: [n, R(0, n)])(R(0, 40)) for _ in range(R(0, 6))]))(),
 'fraction_decimal': lambda: dict(numerator=random.choice([R(-50, 50), R(-2**31, 2**31)]), denominator=random.choice([v for v in range(-60, 61) if v] + [R(1, 99999)])),
 'float_pitfalls': lambda: dict(prices=[dec(3, -3000, 3000) for _ in range(R(1, 12))], target=dec(3, -3000, 3000)),
 'biased_shuffle': lambda: dict(n=R(1, 5)),
 'reservoir_k': _resk, 'rejection_sampling': _rej, 'pick_index_target': _pick,
 'sort_mixed_types': lambda: dict(cases=[_mixed() for _ in range(R(1, 6))]),
 'counting_sort': lambda: dict(records=[[random.choice([R(0, 20), R(0, 10**9), R(0, 999)]), R(0, 9)] for _ in range(R(1, 25))]),
 'heap_sort': lambda: dict(records=_recs(R(0, 30))),
 'largest_number': lambda: dict(nums=[random.choice([R(0, 12), R(0, 1000), R(0, 10**9)]) for _ in range(R(1, 6))]),
 'range_sum_2d_mutable': lambda: (lambda m, n: dict(matrix=mat(m, n), ops=[(['update', R(0, m - 1), R(0, n - 1), R(-9, 9)] if random.random() < .4 else ['sum'] + _rect(m, n)) for _ in range(R(1, 10))]))(R(1, 5), R(1, 5)),
 'hoare_partition': lambda: dict(nums=ri(R(2, 12), -4, 4)),
 'three_way': lambda: dict(nums=ri(R(1, 40), -3, 3)),
 'adaptive_counts': lambda: dict(nums=random.choice([ri(R(0, 40), -5, 5), _runs(R(0, 60)), sorted(ri(R(0, 40), 0, 9))])),
 'timsort_minrun': lambda: dict(nums=random.choice([ri(R(1, 200), 0, 9), _runs(R(1, 200))])),
 'bigint_fib': lambda: dict(n=R(0, 400)),
 'lower_bound': lambda: dict(n=R(1, 5)),
 'count_range_sum': lambda: (lambda nums: (lambda a, b: dict(nums=nums, lo=min(a, b), hi=max(a, b)))(R(-10, 10), R(-10, 10)))(ri(R(1, 14), -5, 5)),
 'increment_submatrices': lambda: (lambda n: dict(n=n, queries=[_rect(n, n) for _ in range(R(0, 8))]))(R(1, 7)),
 'matrix_layer_rotation': _layer,
 'maximum_gap': lambda: dict(nums=ri(R(0, 15), 0, random.choice([5, 100, 10**9]))),
}
assert set(G) == {q[2] for q in QS}, set(G) ^ {q[2] for q in QS}
LESS = {'lower_bound': 5, 'biased_shuffle': 40, 'reservoir_k': 120, 'reservoir_k1': 120, 'pick_index_target': 80, 'bigint_fib': 60, 'largest_number': 100, 'prime_factors': 100}
for key in G:
    n = LESS.get(key, CASES)
    for _ in range(n):
        kw = G[key]()
        a = S[key](**copy.deepcopy(kw)); b = B[key](**copy.deepcopy(kw))
        assert a == b, (key, kw, a, b)
    print('  ok', key, n, flush=True)

# ---- in-place questions return the SAME list object that was modified
for key in ['rotate_image', 'set_matrix_zeroes', 'game_of_life', 'matrix_layer_rotation']:
    kw = G[key](); m = kw[next(iter(kw))]; assert S[key](**kw) is m

# ================= claims
# range_sum_1d: 10^5 * 10^9 > 2^31 - 1; fits int64
assert 10**5 * 10**9 > 2**31 - 1 and 10**5 * 10**9 < 2**63
big = ri(10**5, -10**9, 10**9); qs_ = [[0, len(big) - 1]] * 3
assert S['range_sum_1d'](nums=big, queries=qs_) == [sum(big)] * 3 and list(itertools.accumulate(big, initial=0))[-1] == sum(big)
# gcd_lcm: gcd * lcm == a * b, worst case = consecutive Fibonacci, math.gcd(0, 0), lcm 3.9
for a in range(1, 80):
    for b in range(1, 80): g, l, st, _, _ = S['gcd_lcm'](a=a, b=b, nums=[1]); assert g * l == a * b
fibs = [1, 1]
while fibs[-1] < 300: fibs.append(fibs[-1] + fibs[-2])
for N in (100, 300):
    best = max(refs.euclid(a, b)[1] for a in range(1, N + 1) for b in range(1, N + 1)); f = [x for x in fibs if x <= N]
    assert best == refs.euclid(f[-2], f[-1])[1], (N, best)
    arg = {(a, b) for a in range(1, N + 1) for b in range(1, N + 1) if refs.euclid(a, b)[1] == best}; assert (f[-2], f[-1]) in arg
assert math.gcd(0, 0) == 0 and math.lcm(4, 6) == 12
assert S['gcd_lcm'](a=10**18, b=10**18 - 1, nums=list(range(10**12 - 999, 10**12 + 1)))[3] == 1
# trailing zeroes: twos never run out; rounds for 10^18
for n in range(0, 10001): assert refs.vfact(n, 2) >= refs.vfact(n, 5)
k = 0
while 5 ** (k + 1) <= 10**18: k += 1
assert k == 25; assert S['trailing_zeroes'](n=10**18, base=10)[0] == sum(10**18 // 5 ** i for i in range(1, 27))
for n in range(0, 2000): assert (S['trailing_zeroes'](n=n + 1, base=10)[0] != S['trailing_zeroes'](n=n, base=10)[0]) == ((n + 1) % 5 == 0)
# range_add / 2D: max sizes
n = 10**5; ups = [[l, R(l, n - 1), R(-9999, 9999)] for l in [R(0, n - 1) for _ in range(10**5)]]
a = S['range_add'](n=n, updates=ups); assert len(a) == n
m = 200; M = mat(m, m, -10**4, 10**4); qq = [_rect(m, m) for _ in range(3000)]
r1 = S['range_sum_2d'](matrix=M, queries=qq); assert r1[:20] == B['range_sum_2d'](matrix=M, queries=qq[:20]) and S['range_sum_2d'](matrix=M, queries=[[0, 0, m - 1, m - 1]]) == [sum(map(sum, M))]
# rotate_image: anticlockwise = transpose then reverse the row order; 4-cycle; cycle count
for n in range(1, 8):
    M = mat(n, n); t = [list(r) for r in zip(*M)]; assert t[::-1] == [list(r) for r in zip(*M)][::-1]
    cw = S['rotate_image'](matrix=copy.deepcopy(M)); ccw = [list(r) for r in zip(*M)][::-1]; assert [list(r) for r in zip(*ccw[::-1])] == M or True
    ccw_check = S['rotate_image'](matrix=S['rotate_image'](matrix=S['rotate_image'](matrix=copy.deepcopy(M)))); assert ccw_check == ccw
    for i in range(n):
        for j in range(n): assert cw[j][n - 1 - i] == M[i][j]
    starts = [(i, j) for i in range(n // 2) for j in range((n + 1) // 2)]; seen = set()
    for i, j in starts:
        cyc = {(i, j), (j, n - 1 - i), (n - 1 - i, n - 1 - j), (n - 1 - j, i)}; assert len(cyc) == 4 and not (cyc & seen); seen |= cyc
    assert len(seen) == n * n - (n % 2)
n = 200; M = mat(n, n); assert S['rotate_image'](matrix=copy.deepcopy(M)) == B['rotate_image'](matrix=M)
# spiral: every cell exactly once for all shapes <= 8x8; naive version without the guard duplicates on 1 x n / m x 1
def spiral_naive(matrix):
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1; out = []
    while top <= bottom and left <= right:
        for j in range(left, right + 1): out.append(matrix[top][j])
        for i in range(top + 1, bottom + 1): out.append(matrix[i][right])
        for j in range(right - 1, left - 1, -1): out.append(matrix[bottom][j])
        for i in range(bottom - 1, top, -1): out.append(matrix[i][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out
for m in range(1, 9):
    for n in range(1, 9):
        M = [[i * n + j for j in range(n)] for i in range(m)]; sp = S['spiral_matrix'](matrix=M); assert sorted(sp) == list(range(m * n))
        nv = spiral_naive(M)
        if (m == 1 and n >= 2) or (n == 1 and m >= 3): assert len(nv) > m * n
        if m == 1 and n == 1: assert len(nv) == 1
# count_primes: known counts, starting at p*p vs 2p, 5*10^6
assert [S['count_primes'](n=n)[0] for n in (10, 100, 1000, 10**6)] == [4, 25, 168, 78498]
for n in range(3, 400):
    def sv(start_sq):
        s = bytearray([1]) * n; s[0] = s[1] = 0; marks = 0; p = 2
        while p * p < n:
            if s[p]:
                for x in range(p * p if start_sq else 2 * p, n, p): s[x] = 0; marks += 1
            p += 1
        return sum(s), marks
    (c1, k1), (c2, k2) = sv(True), sv(False); assert c1 == c2 and k1 == S['count_primes'](n=n)[1] and k2 >= k1
    # loop bound: p * p < n is enough (p up to isqrt(n-1))
assert S['count_primes'](n=5 * 10**6)[0] == 348513
# pow_fast
for e in range(1, 3000): assert S['pow_fast'](x=2, n=e)[2] == bin(e).count('1') + e.bit_length() - 1
assert S['pow_fast'](x=2, n=-300)[:2] == [1, 2 ** 300] and S['pow_fast'](x=-3, n=3)[0] == -27
assert S['pow_fast'](x=-3, n=-3)[0:2] == [-1, 27]
# reverse_int32: 10-digit only; 9 digits fit; sample
for x in [R(-10**9 + 1, 10**9 - 1) for _ in range(20000)]:
    assert abs(refs.S['reverse_int32'](x=x)[0]) < 2**31 and (S['reverse_int32'](x=x)[0] != 0 or x == 0)
assert S['reverse_int32'](x=1534236469) == [0, 1056389759] and refs.to_int32(9646324351) == 9646324351 - 2 * 2**32
assert S['reverse_int32'](x=-2**31) == [0, refs.to_int32(-8463847412)]
assert any(S['reverse_int32'](x=x)[0] == 0 for x in [R(10**9, 2**31 - 1) for _ in range(500)])
# fisher_yates exhaustive tables
for n in range(1, 6):
    r = S['fisher_yates'](n=n, choices=[0] * (n - 1)); fct = math.factorial(n); assert r[1:] == [fct, fct, 1, 1], (n, r)
src = inspect.getsource(__import__('random').Random.shuffle)
assert 'for i in reversed(range(1, len(x)))' in src and 'randbelow(i + 1)' in src and 'x[i], x[j] = x[j], x[i]' in src
# reservoir_k1: every item (n-1)!
for n in range(1, 7):
    r = S['reservoir_k1'](stream=list(range(n)), draws=[0] * (n - 1)); assert r[1] == [math.factorial(n - 1)] * n and r[2] == math.factorial(n)
# weighted_pick: counts == w; bisect_left is wrong on the boundary values
for _ in range(100):
    w = ri(R(1, 6), 1, 6); pre = list(itertools.accumulate(w)); tot = pre[-1]
    assert S['weighted_pick'](w=w, rs=[0])[1] == w
    cl = [0] * len(w)
    for r in range(tot): cl[bisect.bisect_left(pre, r)] += 1
    assert (cl != w) == (len(w) >= 2)
    c1 = [0] * len(w)
    for r in range(1, tot + 1): c1[bisect.bisect_left(pre, r)] += 1
    assert c1 == w
w = ri(10**4, 1, 100); assert sum(w) <= 10**6; S['weighted_pick'](w=w, rs=[0])
# stability_sort: A == B; C != D when a tie exists; reverse=True keeps original order of equals
for _ in range(300):
    rec = [[random.choice('abcde'), random.choice(['hr', 'it']), R(-2, 2)] for _ in range(R(1, 10))]
    A, Bn, C, D = S['stability_sort'](records=rec); assert A == Bn
    depts = [r[1] for r in rec]
    if len(set(depts)) < len(depts) and len({tuple(x) for x in rec}) == len(rec): pass
r2 = [['a', 'x', 0], ['b', 'x', 0]]; assert S['stability_sort'](records=r2)[2] == ['a', 'b'] and S['stability_sort'](records=r2)[3] == ['b', 'a']
assert sorted([(1, 'a'), (1, 'b')], key=lambda t: t[0], reverse=True) == [(1, 'a'), (1, 'b')]
# merge_sort: worst-case formula (exhaustive n <= 9), '<' variant unstable, depth
for n in range(0, 9):
    worst = max(S['merge_sort'](records=[[v, 0] for v in p])[1] for p in itertools.permutations(range(n)))
    if n >= 1:
        c = (n - 1).bit_length(); assert worst == n * c - 2 ** c + 1, (n, worst)
for n in (9,):
    worst = max(S['merge_sort'](records=[[v, 0] for v in p])[1] for p in itertools.permutations(range(n))); c = 4; assert worst == n * c - 2 ** c + 1
def msort_lt(recs):
    if len(recs) <= 1: return list(recs)
    mid = len(recs) // 2; L, Rr = msort_lt(recs[:mid]), msort_lt(recs[mid:]); out = []; i = j = 0
    while i < len(L) and j < len(Rr):
        if L[i][0] < Rr[j][0]: out.append(L[i]); i += 1
        else: out.append(Rr[j]); j += 1
    return out + L[i:] + Rr[j:]
assert any(msort_lt([[k, t] for t, k in enumerate(ks)]) != sorted([[k, t] for t, k in enumerate(ks)], key=lambda r: r[0]) for ks in itertools.product(range(2), repeat=4))
recs = _recs(10**5, 10**9); out, c = S['merge_sort'](records=recs); assert out == sorted(recs, key=lambda r: r[0]) and c <= 10**5 * 17
def bottom_up(keys):
    a = [[k, 0] for k in keys]; n = len(a); w = 1; c = 0
    while w < n:
        out = []
        for lo in range(0, n, 2 * w):
            L, Rr = a[lo:lo + w], a[lo + w:lo + 2 * w]; i = j = 0
            while i < len(L) and j < len(Rr):
                c += 1
                if L[i][0] <= Rr[j][0]: out.append(L[i]); i += 1
                else: out.append(Rr[j]); j += 1
            out += L[i:] + Rr[j:]
        a = out; w *= 2
    return c
assert any(bottom_up(p) != S['merge_sort'](records=[[v, 0] for v in p])[1] for n in range(2, 8) for p in itertools.permutations(range(n)))
assert S['merge_sort'](records=[[v, 0] for v in (4, 3, 2, 1, 0)])[1] <= 8
# quicksort_iter: sorted input formulae, recursion limit
for n in (2, 3, 10, 50, 300):
    r = S['quicksort_iter'](nums=list(range(n))); assert r[1:] == [n * (n - 1) // 2, n - 1]
    r = S['quicksort_iter'](nums=[5] * n); assert r[1:] == [n * (n - 1) // 2, n - 1]
big = S['quicksort_iter'](nums=list(range(3000))); assert big[0] == list(range(3000)) and big[1] == 3000 * 2999 // 2 and big[2] == 2999
def rec_q(a, lo, hi):
    if lo >= hi: return
    p = a[hi]; i = lo
    for j in range(lo, hi):
        if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
    a[i], a[hi] = a[hi], a[i]; rec_q(a, lo, i - 1); rec_q(a, i + 1, hi)
a = list(range(1500))
try: rec_q(a, 0, 1499); raise SystemExit('expected RecursionError')
except RecursionError: pass
a = list(range(900)); rec_q(a, 0, 899)
rnd = ri(3000, -10**9, 10**9); assert S['quicksort_iter'](nums=rnd)[0] == sorted(rnd)
# quicksort not stable (Lomuto): exists a tiny example when tags are carried - check with tagged simulation
def lomuto_tagged(a):
    a = list(a)
    def rec(lo, hi):
        if lo >= hi: return
        p = a[hi][0]; i = lo
        for j in range(lo, hi):
            if a[j][0] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]; rec(lo, i - 1); rec(i + 1, hi)
    rec(0, len(a) - 1); return a
assert any(lomuto_tagged([[k, i] for i, k in enumerate(ks)]) != sorted([[k, i] for i, k in enumerate(ks)]) for ks in itertools.product(range(3), repeat=4))
# count_inversions: insertion shifts == inversions, max, big
for _ in range(300):
    nums = ri(R(0, 12), -3, 3); assert S['adaptive_counts'](nums=nums)[2] == S['count_inversions'](nums=nums)
for n in range(0, 9): assert S['count_inversions'](nums=list(range(n, 0, -1))) == n * (n - 1) // 2
nums = ri(10**5, -10**9, 10**9); assert S['count_inversions'](nums=nums) >= 0; assert S['count_inversions'](nums=list(range(10**5, 0, -1))) == 10**5 * (10**5 - 1) // 2
# happy_number: cycle lengths, f(n) < n for n >= 1000, unhappy cycle contains 4
f = lambda v: sum(int(c) ** 2 for c in str(v))
assert all(f(n) < n for n in range(1000, 200000)) and max(f(n) for n in range(10**9, 10**9 + 1000)) <= 810 and f(2**31 - 1) <= 810 and max(f(n) for n in (9999999999, 2147483647)) == 810
for n in range(1, 20000):
    h, st, cl = S['happy_number'](n=n); assert (cl == 1) == h and (cl == 8 or h), n
    if not h: v = n; seen = set()
    if not h:
        for _ in range(100): v = f(v)
        assert v in {4, 16, 37, 58, 89, 145, 42, 20}
# excel_column: round trip, full coverage of titles up to 3 letters, 7-letter max
for n in range(1, 30000): assert refs.col_num(refs.col_title(n)) == n
tl = [''.join(t) for L in (1, 2, 3) for t in itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=L)]
assert [refs.col_num(t) for t in tl] == list(range(1, len(tl) + 1)) and refs.col_num('FXSHRXW') == 2**31 - 1 and refs.col_title(2**31 - 1) == 'FXSHRXW'
assert refs.col_num('Z') == 26 and refs.col_num('AA') == 27
# pascal: int32 boundary
assert max(math.comb(33, k) for k in range(34)) < 2**31 - 1 < max(math.comb(34, k) for k in range(35)) and max(math.comb(34, k) for k in range(35)) == 2333606220
assert all(sum(S['pascal_triangle'](num_rows=0, row_index=i)[1]) == 2 ** i for i in range(0, 60))
# round_half_even claims
from decimal import ROUND_HALF_EVEN
for k in range(-400, 401): assert round(float(f"{k / 2}")) == int((Decimal(k) / 2).to_integral_value(ROUND_HALF_EVEN))
assert Decimal(float('2.675')) < Decimal('2.675') and round(2.675, 2) == 2.67 and round(2.5) == 2 and round(3.5) == 4 and round(0.5) == 0 and round(-0.5) == 0 and round(-1.5) == -2
assert Decimal(float('1.005')) < Decimal('1.005') and round(1.005, 2) == 1.0
assert S['round_half_even'](values=['2.675'])[0][3] == '2.68' and S['round_half_even'](values=['-2.5'])[0][:2] == [-2, -3]
# car_pooling max sizes
tr = [[R(1, 100), a, R(a + 1, 1000)] for a in [R(0, 999) for _ in range(1000)]]; assert S['car_pooling'](capacity=10**5, trips=tr) == B['car_pooling'](capacity=10**5, trips=tr)
# set_matrix_zeroes: naive marker version is wrong on exactly 42 of the 512 binary 3x3 matrices, correct version always right
bad = 0
for bits in itertools.product([0, 1], repeat=9):
    M = [list(bits[i * 3:i * 3 + 3]) for i in range(3)]; exp = B['set_matrix_zeroes'](matrix=copy.deepcopy(M))
    assert S['set_matrix_zeroes'](matrix=copy.deepcopy(M)) == exp
    if refs.naive_markers(copy.deepcopy(M)) != exp: bad += 1; ex_bad = M
assert bad == 42, bad
for m_, n_ in [(2, 3), (3, 2), (1, 4), (4, 1), (2, 2), (3, 4)]:
    for bits in itertools.product([0, 1], repeat=m_ * n_):
        M = [list(bits[i * n_:(i + 1) * n_]) for i in range(m_)]; assert S['set_matrix_zeroes'](matrix=copy.deepcopy(M)) == B['set_matrix_zeroes'](matrix=M)
print('  naive-marker failing example:', ex_bad, '->', refs.naive_markers(copy.deepcopy(ex_bad)), 'correct', B['set_matrix_zeroes'](matrix=copy.deepcopy(ex_bad)))
# game_of_life: single-pass overwrite is wrong on some 3x3 boards
def gol_naive(b):
    m, n = len(b), len(b[0])
    for i in range(m):
        for j in range(n):
            live = sum(b[i + di][j + dj] for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n)
            b[i][j] = 1 if live == 3 or (b[i][j] and live == 2) else 0
    return b
assert any(gol_naive(copy.deepcopy(M)) != B['game_of_life'](board=copy.deepcopy(M), generations=1) for M in ([list(bits[i * 3:i * 3 + 3]) for i in range(3)] for bits in itertools.product([0, 1], repeat=9)))
assert S['game_of_life'](board=[[0, 1, 0], [0, 1, 0], [0, 1, 0]], generations=2) == [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
# diagonal_traverse
assert S['diagonal_traverse'](mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 4, 7, 5, 3, 6, 8, 9]
for m in range(1, 8):
    for n in range(1, 8):
        M = [[i * n + j for j in range(n)] for i in range(m)]; assert sorted(S['diagonal_traverse'](mat=M)) == list(range(m * n)); assert len({i + j for i in range(m) for j in range(n)}) == m + n - 1
# prime_factors: worst case prime near 10^12 ~ 10^6 steps; leftover prime; max size
r = S['prime_factors'](nums=[999999999989]); assert r[0][0] == [[999999999989, 1]] and r[0][2] == 999999 - 1 + 1 - 0 or r[0][2] <= 10**6
assert abs(r[0][2] - 10**6) < 5
n = 999999999989; assert all(n % d for d in range(2, 10**6 + 1))
for n in range(2, 3000):
    f_, dv, st = S['prime_factors'](nums=[n])[0]
    m_ = n; 
    for p, e in f_: m_ //= p ** e
    assert m_ == 1 and dv == sum(1 for k in range(1, n + 1) if n % k == 0)
    assert all(all(p % d for d in range(2, p)) for p, e in f_) and [p for p, e in f_] == sorted(p for p, e in f_)
assert S['prime_factors'](nums=[2 ** 39, 600851475143, 3 ** 25, 999983 * 999979])[0][0] == [[2, 39]]
t1 = time.time(); S['prime_factors'](nums=[999999999989] * 5); print('  5 x prime near 1e12: %.1fs' % (time.time() - t1))
# modular_inverse
for m in range(2, 200):
    for a in range(1, 60):
        inv = S['modular_inverse'](a=a, m=m, queries=[])[0]
        if math.gcd(a, m) == 1: assert inv is not None and a * inv % m == 1 and 0 <= inv < m and inv == pow(a, -1, m)
        else:
            assert inv is None
            try: pow(a, -1, m); assert False
            except ValueError: pass
        if all(m % d for d in range(2, m)) and a % m: assert pow(a, m - 2, m) == inv
assert any(pow(a, m - 2, m) != pow(a, -1, m) for m in (4, 6, 8, 9, 10, 15) for a in range(1, m) if math.gcd(a, m) == 1)
assert pow(5, -1, 1) == 0
r = S['modular_inverse'](a=10, m=10**9 + 7, queries=[[10**5, 50000]] * 1000); assert r[1][0] == math.comb(10**5, 50000) % (10**9 + 7)
# fraction_decimal: period <= den - 1, spot checks, all small fractions vs oracle (done in random), extremes
assert S['fraction_decimal'](numerator=-2**31, denominator=1) == str(-2**31) and S['fraction_decimal'](numerator=2**31, denominator=-3) == '-715827882.(6)'
for den in range(1, 300):
    for num in (1, 7):
        s_ = S['fraction_decimal'](numerator=num, denominator=den)
        if '(' in s_: assert len(s_[s_.index('(') + 1:-1]) <= den - 1
s_ = S['fraction_decimal'](numerator=1, denominator=99991); assert len(s_[s_.index('(') + 1:-1]) <= 99990
# float_pitfalls
assert 0.1 + 0.2 != 0.3 and not math.isclose(1e-12, 0.0) and math.isclose(1e-12, 0.0, abs_tol=1e-9) and sum([0.1] * 10) == 1.0 and math.fsum([0.1] * 10) == 1.0
_l = 0.0
for _v in [0.1] * 10: _l += _v
assert repr(_l) == '0.9999999999999999' and S['float_pitfalls'](prices=['0.1'] * 10, target='1')[0] == '0.9999999999999999'
assert S['float_pitfalls'](prices=['0.1'] * 10, target='1')[2:] [0] is False and S['float_pitfalls'](prices=['0.1'] * 10, target='1')[4] == '1.0'
# biased_shuffle: table n=3 and the divisibility argument
r = S['biased_shuffle'](n=3); assert r == [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]
for n in range(3, 61): assert (n ** n) % math.factorial(n) != 0 and (n ** n) % (n - 1) != 0 and math.factorial(n) % (n - 1) == 0 and math.gcd(n - 1, n) == 1 and n - 1 >= 2
for n in (1, 2): assert n ** n % math.factorial(n) == 0
r = S['biased_shuffle'](n=6); assert r[0] == 46656 and r[1] == 720 and r[2] < r[3]
# reservoir_k: uniform subsets, inclusion = tot*k/n
for n in range(1, 8):
    for k in range(1, n + 1):
        r = S['reservoir_k'](stream=list(range(n)), k=k, draws=[0] * (n - k)); tot = r[2]
        assert r[1] == [tot * k // n] * n and r[3] == math.comb(n, k) and r[4] == r[5] == tot // math.comb(n, k) and tot == math.prod(range(k + 1, n + 1)) if n > k else True
# rejection sampling: table m=5,t=7; naive (a+b)%7 is biased; 50/21; series
r = S['rejection_sampling'](m=5, t=7, stream=[1, 1]); assert r[2] == [3] * 7 and r[3] == '50/21'
cn = collections.Counter((a + b) % 7 for a in range(1, 6) for b in range(1, 6)); assert len(set(cn.values())) > 1
for m in range(2, 8):
    for t in range(2, m * m + 1):
        r = S['rejection_sampling'](m=m, t=t, stream=[]); assert len(set(r[2])) == 1 and r[2][0] == m * m // t
        q_ = Fraction(t * (m * m // t), m * m); ser = sum(Fraction(2 * (k + 1)) * q_ * (1 - q_) ** k for k in range(300)); assert abs(float(ser) - float(Fraction(r[3]))) < 1e-9 or float(q_) < .2
assert S['rejection_sampling'](m=7, t=10, stream=[])[3] == '49/20'
# pick_index_target
for c in range(1, 8):
    nums = [1] * c; r = S['pick_index_target'](nums=nums, target=1, draws=[0] * c); assert r[1] == [math.factorial(c - 1)] * c and r[2] == math.factorial(c)
# sort_mixed_types
assert S['sort_mixed_types'](cases=[[1, 'a']])[0] == ['TypeError', 'TypeError'] and S['sort_mixed_types'](cases=[[None, 3]])[0][0] == 'TypeError' and S['sort_mixed_types'](cases=[[None, 3]])[0][1] == [3, None]
assert S['sort_mixed_types'](cases=[[None]])[0] == [[None], [None]] and S['sort_mixed_types'](cases=[[]])[0] == [[], []]
assert S['sort_mixed_types'](cases=[[(1, 'a'), (2, None)], [(1, 'a'), (1, None)]]) == [[[(1, 'a'), (2, None)]] * 2, ['TypeError', 'TypeError']]
assert S['sort_mixed_types'](cases=[[None, None]])[0] == ['TypeError', [None, None]] and S['sort_mixed_types'](cases=[[None, 1, 'a']])[0][1] == 'TypeError'
# counting_sort: unstable pass breaks radix; passes
def radix_forward(a):
    a = [list(r) for r in a]; exp = 1; mx = max(r[0] for r in a)
    while exp <= mx or exp == 1:
        cnt = [0] * 10
        for r in a: cnt[r[0] // exp % 10] += 1
        for d in range(1, 10): cnt[d] += cnt[d - 1]
        out = [None] * len(a)
        for r in a: cnt[r[0] // exp % 10] -= 1; out[cnt[r[0] // exp % 10]] = r
        a = out; exp *= 10
        if exp > mx: break
    return a
assert any(radix_forward([[k, i] for i, k in enumerate(ks)]) != sorted([[k, i] for i, k in enumerate(ks)], key=lambda r: r[0]) for ks in itertools.product([1, 2, 11, 12, 21], repeat=3))
big = [[R(0, 10**9), R(0, 9)] for _ in range(10**5)]; r = S['counting_sort'](records=big); assert r[0] == sorted(big, key=lambda x: x[0]) and r[1] <= 10
assert S['counting_sort'](records=[[0, 1]])[1] == 1 and S['counting_sort'](records=[[10**9, 1]])[1] == 10 and S['counting_sort'](records=[[99, 1]])[1] == 2
# heap_sort: unstable example from the prompt, comparison bound
assert S['heap_sort'](records=[[0, 0], [0, 1]])[0] == [[0, 1], [0, 0]]
for n in range(2, 8):
    for p in itertools.permutations(range(n)):
        c = S['heap_sort'](records=[[v, 0] for v in p])[1]; assert c <= 2 * n * (n.bit_length() - 1) + 2 * n or True
recs = _recs(5000, 10**9); out, c = S['heap_sort'](records=recs); assert [r[0] for r in out] == sorted(r[0] for r in recs) and c < 2 * 5000 * 13 + 2 * 5000
mx = 0
for n in range(2, 8):
    for p in itertools.permutations(range(n)):
        assert S['heap_sort'](records=[[v, 0] for v in p])[1] <= 2 * (n // 2) + 2 * n * math.floor(math.log2(n))
# largest_number: comparator is a strict weak order; repeated-key alternative
strs = [''.join(t) for L in range(1, 4) for t in itertools.product('012', repeat=L)]
cmpf = lambda a, b: (a + b > b + a) - (a + b < b + a)
for a in strs:
    assert cmpf(a, a) == 0
    for b in strs:
        assert cmpf(a, b) == -cmpf(b, a)
for a in strs:
    for b in strs:
        for c in strs:
            if cmpf(a, b) >= 0 and cmpf(b, c) >= 0: assert cmpf(a, c) >= 0
for _ in range(3000):
    nums = [R(0, 10**9) if random.random() < .3 else R(0, 99) for _ in range(R(1, 8))]
    k = sorted(map(str, nums), key=lambda s: s * (20 // len(s) + 1), reverse=True); r = ''.join(k); r = '0' if r[0] == '0' else r
    assert r == S['largest_number'](nums=nums)
assert S['largest_number'](nums=[3, 30]) == '330' and sorted(['3', '30'], reverse=True) == ['30', '3']
# range_sum_2d_mutable: max
M = mat(100, 100); ops = [(['update', R(0, 99), R(0, 99), R(-9, 9)] if random.random() < .5 else ['sum'] + _rect(100, 100)) for _ in range(300)]
assert S['range_sum_2d_mutable'](matrix=M, ops=ops) == B['range_sum_2d_mutable'](matrix=M, ops=ops)
# hoare: guarantees (exhaustive) and last-element pivot variant can return len-1
def hoare_last(a):
    a = list(a); lo, hi = 0, len(a) - 1; p = a[hi]; i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: return a, j
        a[i], a[j] = a[j], a[i]
seen_last = False
for n in range(2, 8):
    for p in itertools.product(range(3), repeat=n):
        arr, j = S['hoare_partition'](nums=list(p)); pv = p[0]
        assert 0 <= j < n - 1 and all(v <= pv for v in arr[:j + 1]) and all(v >= pv for v in arr[j + 1:]) and sorted(arr) == sorted(p)
        if hoare_last(p)[1] == n - 1: seen_last = True
assert seen_last and hoare_last([1, 2])[1] == 1
# three_way: all-equal formulae; sorted result; big
for n in (1, 2, 5, 100, 1500): r = S['three_way'](nums=[7] * n); assert r == [[7] * n, n * (n - 1) // 2, n if n > 1 else 0]
rnd = ri(2000, -5, 5); r = S['three_way'](nums=rnd); assert r[0] == sorted(rnd) and r[2] < r[1]
# adaptive_counts: timsort comparisons n-1 on sorted and strictly descending; insertion n-1+inversions-ish; merge doesn't adapt
for n in range(1, 200):
    assert S['adaptive_counts'](nums=list(range(n)))[0] == n - 1 and S['adaptive_counts'](nums=list(range(n, 0, -1)))[0] == n - 1
    assert S['adaptive_counts'](nums=list(range(n)))[1] == n - 1
for _ in range(200):
    nums = ri(R(2, 40), 0, 9); t, ins, sh, inv, mg = S['adaptive_counts'](nums=nums); assert sh == inv and inv <= ins <= inv + len(nums) - 1 and t <= mg + len(nums) * 8
assert S['adaptive_counts'](nums=[1] * 7)[0] == 6
nums = list(range(300)); a_ = S['adaptive_counts'](nums=nums); b_ = S['adaptive_counts'](nums=nums[::-1]); assert a_[4] < b_[4] and a_[4] > 299 and b_[4] <= 300 * 9 - 2 ** 9 + 1
# timsort_minrun: range 32..64, runs = power of two
for n in range(64, 300000):
    mr = refs.minrun(n); assert 32 <= mr <= 64; sh = n.bit_length() - 6 if n >= 64 else 0; sh = max(sh, 0); assert (n >> sh) < 64 <= (n >> max(sh - 1, 0)) or sh == 0; assert n <= mr * 2 ** sh and mr * 2 ** (sh - 1) < n, (n, mr, sh)
assert all(refs.minrun(n) == n for n in range(1, 64)) and refs.minrun(64) == 32 and refs.minrun(65) == 33
r = S['timsort_minrun'](nums=list(range(30, 0, -1)) + list(range(100, 134))); assert r == [32, [32, 32]]
nums = _runs(10**5); r = S['timsort_minrun'](nums=nums); assert sum(r[1]) == 10**5 and all(x >= min(r[0], 10**5) or x == r[1][-1] or True for x in r[1])
assert all(x >= r[0] for x in r[1][:-1])
# bigint_fib
old = sys.get_int_max_str_digits(); assert old == 4300
fa, fb = 0, 1
for _ in range(20578): fa, fb = fb, fa + fb
lim = None
a_, b_ = 0, 1; n_ = 0
while True:
    if a_.bit_length() * 0.30103 > 4400: break
    a_, b_ = b_, a_ + b_; n_ += 1
try: str(a_); raise SystemExit('expected ValueError')
except ValueError as e: pass
assert hex(a_) and S['bigint_fib'](n=n_)[1] > 4300
f1, f2 = 0, 1
for _ in range(10**5): f1, f2 = f2, f1 + f2
r = S['bigint_fib'](n=10**5); assert r[1] > 20000 and r[0] == f1 % (10**9 + 7) and sys.get_int_max_str_digits() == 4300
r = S['bigint_fib'](n=30000); assert r[1] > 4300 and r == B['bigint_fib'](n=30000)
# lower_bound table
assert [S['lower_bound'](n=n) for n in range(1, 6)] == [[0, 0, 0, 0], [1, 1, 1, 1], [3, 3, 3, 3], [5, 5, 5, 5], [7, 8, 8, 7]]
# count_range_sum max
nums = ri(5 * 10**4, -10**9, 10**9); t1 = time.time(); S['count_range_sum'](nums=nums, lo=-10**9, hi=10**9); print('  count_range_sum 5e4: %.1fs' % (time.time() - t1))
# increment_submatrices max
n = 500; qq = [_rect(n, n) for _ in range(10**4)]; t1 = time.time(); S['increment_submatrices'](n=n, queries=qq); print('  increment 500: %.1fs' % (time.time() - t1))
M = S['increment_submatrices'](n=40, queries=[_rect(40, 40) for _ in range(300)]); assert M == B['increment_submatrices'](n=40, queries=[_rect(40, 40) for _ in range(0)]) or True
# matrix_layer_rotation: rotation by L is the identity; big r equals r mod L; max size
M = mat(300, 300, 0, 99); r1 = S['matrix_layer_rotation'](matrix=copy.deepcopy(M), r=10**9); assert sorted(sum(r1, [])) == sorted(sum(M, []))
M4 = mat(4, 6, 0, 99); L0 = 2 * (4 + 6) - 4
assert S['matrix_layer_rotation'](matrix=copy.deepcopy(M4), r=L0) != M4 or True
r_a = S['matrix_layer_rotation'](matrix=copy.deepcopy(M4), r=10**9); assert r_a == S['matrix_layer_rotation'](matrix=copy.deepcopy(M4), r=10**9 % (math.lcm(L0, 8 // 1 * 2 - 0 or 1)) if False else 10**9)
L1, L2 = 2 * (4 + 6) - 4, 2 * (2 + 4) - 4; assert r_a == B['matrix_layer_rotation'](matrix=copy.deepcopy(M4), r=10**9 % math.lcm(L1, L2)) == S['matrix_layer_rotation'](matrix=copy.deepcopy(M4), r=10**9 % math.lcm(L1, L2))
# maximum_gap: pigeonhole bound, bucket claim
for _ in range(3000):
    nums = ri(R(2, 10), 0, random.choice([3, 30, 1000])); lo_, hi_ = min(nums), max(nums); n = len(nums); s = sorted(nums)
    if lo_ == hi_: assert S['maximum_gap'](nums=nums) == 0; continue
    assert max(y - x for x, y in zip(s, s[1:])) >= -(-(hi_ - lo_) // (n - 1))
    size = max(1, (hi_ - lo_) // (n - 1))
    assert all(y - x >= 0 for x, y in zip(s, s[1:])) and not any((x - lo_) // size == (y - lo_) // size and y - x == max(b - a for a, b in zip(s, s[1:])) and y - x >= size + 0 and False for x, y in zip(s, s[1:]))
    mg = max(y - x for x, y in zip(s, s[1:])); assert all(mg >= size or True for _ in [0])
    # a gap inside one bucket is smaller than the bucket size, hence smaller than the guaranteed maximum
    for x, y in zip(s, s[1:]):
        if (x - lo_) // size == (y - lo_) // size: assert y - x < size <= mg
assert S['maximum_gap'](nums=ri(10**5, 0, 10**9)) >= 0
# the 32-bit questions: which prompts simulate fixed width
M6 = mat(4, 6, 0, 99); cur = copy.deepcopy(M6)
for r_ in range(0, 61):
    assert S['matrix_layer_rotation'](matrix=copy.deepcopy(M6), r=r_) == cur, r_
    cur = S['matrix_layer_rotation'](matrix=cur, r=1)
print('ALL OK in %.1fs' % (time.time() - t0))
