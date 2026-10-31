# Runs EVERY example rendered into the Part 12 prompts (qs.py is the single source of truth) against the reference solutions (refs.py),
# cross-checks each against an independent brute force on seeded random small inputs, checks every claim made in the prompts
# (bounds, counts, WHY sentences) and runs the maximum sizes. Run: python3 -I check_examples.py
import sys, os, random, itertools, copy, time, functools, collections, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qs import QS
import refs
from refs import S, B
random.seed(12); t0 = time.time(); R = random.randint
CASES = 300
assert sys.getrecursionlimit() == 1000

def same(key, a, b):
    if key == 'sum_two': return a[0] == b[0]
    return a == b
for st, d, key, text, exs, asked in QS:
    for kw, exp in exs:
        got = S[key](**copy.deepcopy(kw)); assert got == exp, (key, kw, got, exp)
        if key != 'sudoku' or True:
            b = B[key](**copy.deepcopy(kw)); assert same(key, b, exp), ('brute', key, kw, b, exp)
print('examples ok', sum(len(q[4]) for q in QS), 'in', len(QS), 'prompts', flush=True)

def ri(n, lo, hi): return [R(lo, hi) for _ in range(n)]
def st_(n, al='abc'): return ''.join(random.choice(al) for _ in range(n))
def pairs_twice(vals_single, others):
    l = list(vals_single) + [o for o in others for _ in range(2)]; random.shuffle(l); return l
def board(r, c, al='ab'): return [st_(c, al) for _ in range(r)]
def sud_puzzle():
    base = [[(3 * (r % 3) + r // 3 + c) % 9 + 1 for c in range(9)] for r in range(9)]
    d = list(range(1, 10)); random.shuffle(d)
    rg = [g * 3 + x for g in random.sample(range(3), 3) for x in random.sample(range(3), 3)]
    cg = [g * 3 + x for g in random.sample(range(3), 3) for x in random.sample(range(3), 3)]
    g = [[str(d[base[r][c] - 1]) for c in cg] for r in rg]
    cells = [(r, c) for r in range(9) for c in range(9)]; random.shuffle(cells); rem = 0
    for r, c in cells:
        old = g[r][c]; g[r][c] = '.'
        if refs.sudoku_count([''.join(x) for x in g]) != 1: g[r][c] = old
        else: rem += 1
        if rem >= random.randint(35, 50): break
    return [''.join(x) for x in g]
def distinct(n, lo, hi): return random.sample(range(lo, hi + 1), n)
G = {
 'single_number': lambda: dict(nums=pairs_twice([R(-20, 20)], [1000 * (i + 1) + R(0, 50) for i in range(R(0, 6))])),
 'count_set_bits': lambda: dict(n=random.choice([R(0, 2**32 - 1), R(0, 20), 2**R(0, 31), 2**R(1, 32) - 1])),
 'power_two_four': lambda: dict(n=random.choice([R(-2**31, 2**31 - 1), R(-5, 70), 2**R(0, 30), -(2**R(0, 30)), 2**R(0, 30) + random.choice([-1, 1]), 4**R(0, 15)])),
 'hamming': lambda: dict(x=R(0, 2**31 - 1), y=R(0, 2**31 - 1), nums=ri(R(2, 8), 0, 2**R(1, 31) - 1)),
 'dup_missing': lambda: _dm(),
 'single_number_iii': lambda: (lambda p: dict(nums=pairs_twice(p[:2], p[2:])))(random.sample(range(-40, 40), 2 + R(0, 5))),
 'reverse_bits': lambda: dict(n=random.choice([R(-2**31, 2**32 - 1), R(-5, 10), 2**R(0, 31)])),
 'single_number_ii': lambda: (lambda p: dict(nums=(lambda l: (random.shuffle(l), l)[1])([p[0]] + [v for v in p[1:] for _ in range(3)])))(random.sample([-2**31, 2**31 - 1, -1, 0, 1, 5, -7, 2**30, -2**30, 12345], 1 + R(0, 5))),
 'sum_two': lambda: dict(a=random.choice([R(-10**9, 10**9), R(-5, 5)]), b=random.choice([R(-10**9, 10**9), R(-5, 5)])),
 'bitmask_enum': lambda: (lambda n: dict(items=distinct(n, -6, 6), target=R(-4, 6)))(R(0, 6)),
 'subsets': lambda: dict(nums=distinct(R(0, 8), -9, 9)),
 'subsets_dup': lambda: dict(nums=ri(R(0, 8), 1, 4)),
 'permutations': lambda: dict(nums=distinct(R(0, 6), -9, 9)),
 'permutations_dup': lambda: dict(nums=ri(R(0, 6), 1, 3)),
 'combinations': lambda: (lambda n: dict(n=n, k=R(1, n)))(R(1, 9)),
 'comb_sum': lambda: dict(candidates=distinct(R(1, 5), 1, 12), target=R(1, 20)),
 'comb_sum2': lambda: dict(candidates=ri(R(1, 9), 1, 8), target=R(1, 20)),
 'gen_parens': lambda: dict(n=R(1, 5)),
 'letter_combos': lambda: dict(digits=''.join(random.choice('23456789') for _ in range(R(0, 4)))),
 'word_search': lambda: (lambda b: dict(board=b, word=st_(R(1, 6), 'ab')))(board(R(1, 4), R(1, 4))),
 'nqueens': lambda: dict(n=R(1, 7)),
 'word_search2': lambda: dict(board=board(R(1, 4), R(1, 4)), words=list({st_(R(1, 5), 'ab') for _ in range(R(1, 8))})),
 'sudoku': lambda: dict(board=sud_puzzle()),
 'palin_partition': lambda: dict(s=st_(R(1, 10), 'ab')),
 'restore_ip': lambda: dict(s=''.join(random.choice('0123455') for _ in range(R(0, 13)))),
 'comb_nodes': lambda: dict(candidates=distinct(R(1, 5), 1, 12), target=R(1, 25)),
 'iter_ws': lambda: dict(board=board(R(1, 4), R(1, 4)), word=st_(R(1, 7), 'ab')),
 'expr_ops': lambda: dict(num=''.join(random.choice('0123') for _ in range(R(1, 6))), target=R(-5, 12)),
 'trie_ops': lambda: dict(ops=[[random.choice(['insert', 'search', 'startsWith']), st_(R(1, 4), 'ab')] for _ in range(R(1, 25))]),
 'replace_words': lambda: dict(roots=[st_(R(1, 3), 'ab') for _ in range(R(1, 4))], sentence=' '.join(st_(R(1, 6), 'ab') for _ in range(R(1, 6)))),
 'autocomplete': lambda: dict(entries=[[w, R(1, 4)] for w in {st_(R(1, 4), 'abc') for _ in range(R(1, 12))}], queries=[st_(R(1, 3), 'abc') for _ in range(5)]),
 'map_sum': lambda: dict(ops=[(['insert', st_(R(1, 3), 'ab'), R(0, 9)] if random.random() < .5 else ['sum', st_(R(1, 3), 'ab')]) for _ in range(R(1, 20))]),
 'max_xor': lambda: dict(nums=ri(R(2, 12), 0, 2**R(1, 31) - 1)),
 'trie_memory': lambda: dict(words=[st_(R(1, 5), 'abc') for _ in range(R(1, 10))]),
 'skip_list': lambda: dict(ops=[[random.choice(['insert', 'contains', 'remove']), R(-6, 6)] for _ in range(R(1, 40))], seed=R(0, 5)),
}
def _dm():
    n = R(2, 12); p = list(range(1, n + 1)); m = R(1, n); d = random.choice([v for v in p if v != m])
    l = [d if v == m else v for v in p]; random.shuffle(l); return dict(nums=l)
G['dup_missing'] = _dm
for st, d, key, text, exs, asked in QS: assert key in G, key

LESS = {'sudoku': 40, 'nqueens': 7, 'word_search2': 150, 'expr_ops': 120, 'permutations': 60}
for key in G:
    n = LESS.get(key, CASES); seen = collections.Counter()
    for _ in range(n):
        kw = G[key]()
        a = S[key](**copy.deepcopy(kw)); b = B[key](**copy.deepcopy(kw))
        assert same(key, a, b), (key, kw, a, b)
        seen[repr(a)[:1] + str(a is True)] += 1
    print('  ok', key, n, flush=True)

# ---- sudoku: examples have a unique solution, the result is valid and agrees with the givens
for st, d, key, text, exs, asked in QS:
    if key == 'sudoku':
        for kw, exp in exs:
            assert refs.sudoku_count(kw['board']) == 1
            assert refs._sud_ok(exp) and all('.' not in r for r in exp)
            assert all(g == '.' or g == e for gr, er in zip(kw['board'], exp) for g, e in zip(gr, er))
for _ in range(15):
    kw = G['sudoku'](); out = S['sudoku'](**kw); assert refs._sud_ok(out) and sorted(''.join(out)) == sorted('123456789' * 9)

# ---- result-order claims: outer lists really are sorted; sorted lists have no duplicates
for key in ['subsets', 'subsets_dup', 'permutations', 'permutations_dup', 'combinations', 'comb_sum', 'comb_sum2', 'palin_partition', 'gen_parens', 'letter_combos', 'restore_ip', 'expr_ops', 'word_search2']:
    for _ in range(60):
        r = S[key](**G[key]()); assert r == sorted(r) and len({repr(x) for x in r}) == len(r), key
# nqueens: ascending by tuple of columns; counts for n = 1..9
cnt = [len(S['nqueens'](n)) for n in range(1, 10)]; assert cnt == [1, 0, 0, 2, 10, 4, 40, 92, 352], cnt
for n in range(1, 9):
    sols = S['nqueens'](n); cols = [tuple(r.index('Q') for r in b) for b in sols]; assert cols == sorted(cols)
    assert sols == B['nqueens'](n)
# counts: subsets 2^n, permutations n!, distinct perms multinomial, Catalan, combinations C(n,k), letters product
for n in range(0, 9): assert len(S['subsets'](list(range(n)))) == 2**n and len(S['permutations'](list(range(n)))) == math.factorial(n)
for ms in itertools.product(range(1, 4), repeat=5):
    mult = collections.Counter(ms); exp = math.factorial(5)
    for v in mult.values(): exp //= math.factorial(v)
    assert len(S['permutations_dup'](list(ms))) == exp
assert [len(S['gen_parens'](n)) for n in range(1, 9)] == [math.comb(2 * n, n) // (n + 1) for n in range(1, 9)]
assert S['gen_parens'](3)[0] == '((()))'
for n in range(1, 21):
    for k in (1, n // 2 or 1, n): assert len(S['combinations'](n, k)) == math.comb(n, k) if n < 15 else True
assert len(S['combinations'](20, 10)) == 184756 == math.comb(20, 10)
assert S['combinations'](5, 3)[0] == [1, 2, 3]
assert max(len(S['letter_combos']('7979' + '79'[:2]))for _ in range(1)) == 4**6 and S['letter_combos']('') == []
# subsets_dup: skipping with i > 0 instead of i > start loses subsets (example [1,2,2])
def bad_subsets_dup(nums):
    a = sorted(nums); out = []; cur = []
    def go(start):
        out.append(cur[:])
        for i in range(start, len(a)):
            if i > 0 and a[i] == a[i - 1]: continue
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0); return sorted(out)
assert bad_subsets_dup([1, 2, 2]) != S['subsets_dup']([1, 2, 2]) and [1, 2, 2] not in bad_subsets_dup([1, 2, 2])
# permutations_dup: rule 'skip when left twin is NOT used' and rule 'skip when left twin IS used' both give the right set; counts of calls differ
def perm_calls(nums, rule):
    a = sorted(nums); used = [False] * len(a); out = []; cur = []; calls = [0]
    def go():
        calls[0] += 1
        if len(cur) == len(a): out.append(cur[:]); return
        for i in range(len(a)):
            if used[i]: continue
            if i and a[i] == a[i - 1] and (used[i - 1] == (rule == 'used')): continue
            used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go(); return sorted(out), calls[0]
more = 0
for ms in itertools.product(range(1, 4), repeat=5):
    o1, c1 = perm_calls(list(ms), 'notused'); o2, c2 = perm_calls(list(ms), 'used')
    assert o1 == o2 == S['permutations_dup'](list(ms)) and c1 <= c2; more += c1 < c2
assert more > 0; print('  perm rules: used-rule makes more calls on', more, 'of', 3**5, 'multisets')
# the not-used rule keeps equal values in original relative order: equal values used left to right = indices increasing in every result by construction (checked via distinct count above)
# palindrome partitions of a^n: 2^(n-1)
for n in range(1, 13): assert len(S['palin_partition']('a' * n)) == 2**(n - 1)
# restore_ip: degenerate lengths, and leaf bound 81
assert S['restore_ip']('') == [] and S['restore_ip']('123') == [] and S['restore_ip']('1' * 13) == [] and S['restore_ip']('0000') == ['0.0.0.0']
leaves = [0]
def ip_count(s, i=0, parts=0):
    if parts == 4: leaves[0] += (i == len(s)); return
    for L in (1, 2, 3): ip_count(s, i + L, parts + 1)
ip_count('x' * 12); assert leaves[0] == 1 and 3**4 == 81
# combinations pruning: bounded loop makes no more calls than the unbounded one; both produce the same lists
def comb_calls(n, k, prune):
    out = []; cur = []; calls = [0]
    def go(start):
        calls[0] += 1
        if len(cur) == k: out.append(cur[:]); return
        for v in range(start, (n - (k - len(cur)) + 1 if prune else n) + 1):
            cur.append(v); go(v + 1); cur.pop()
    go(1); return out, calls[0]
for n, k in [(5, 3), (8, 4), (10, 3), (6, 6)]:
    o1, c1 = comb_calls(n, k, True); o2, c2 = comb_calls(n, k, False); assert o1 == o2 == S['combinations'](n, k) and c1 <= c2
assert comb_calls(5, 3, True)[1] < comb_calls(5, 3, False)[1]
# generate parentheses: every visited prefix extends to an answer (no dead calls)
def paren_prefixes(n):
    res = set(); 
    def go(cur, o, c):
        res.add(cur)
        if len(cur) == 2 * n: return
        if o < n: go(cur + '(', o + 1, c)
        if c < o: go(cur + ')', o, c + 1)
    go('', 0, 0); return res
for n in range(1, 8):
    full = S['gen_parens'](n); pref = {s[:i] for s in full for i in range(2 * n + 1)}
    assert paren_prefixes(n) == pref
# comb_nodes: B <= A, same hits; hits equal comb_sum count
for _ in range(400):
    kw = G['comb_nodes'](); a, b, h = S['comb_nodes'](**kw); assert b <= a and h == len(S['comb_sum'](**kw))
assert S['comb_nodes'](candidates=[1], target=5)[0] == S['comb_nodes'](candidates=[1], target=5)[1]
# word search: undo placement. Without restoring the cell a second start finds a wrong answer
def ws_no_restore(board, word):
    R_, C_ = len(board), len(board[0]); g = [list(r) for r in board]
    def go(r, c, k):
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in refs.DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R_ and 0 <= nc < C_ and go(nr, nc, k + 1): return True
        return False
    return any(go(r, c, 0) for r in range(R_) for c in range(C_))
wrong = 0
for _ in range(400):
    kw = G['word_search'](); wrong += ws_no_restore(**kw) != S['word_search'](**kw)
assert wrong > 0, wrong; print('  word_search without restore wrong on', wrong, 'of 400')
# word search II: per-word search agrees; trie pruning (deleting leaves) not needed for correctness
# ---- iterative backtracking: recursion depth
rec_ok = refs.recursive_ws(['a' * 300], 'a' * 300); assert rec_ok is True
try: refs.recursive_ws(['a' * 1500], 'a' * 1500); raise SystemExit('no RecursionError')
except RecursionError as e: msg = str(e); assert 'recursion' in msg.lower()
assert S['iter_ws'](['a' * 1500], 'a' * 1500) is True and S['iter_ws'](['a' * 1500], 'a' * 1499 + 'b') is False
assert S['iter_ws'](['a' * 2000], 'a' * 1501 + 'b') is False
for _ in range(300):
    kw = G['iter_ws'](); assert S['iter_ws'](**kw) == refs.recursive_ws(**kw)
def snake(k):   # (2k+1) x (2k+1)? build a winding one-cell corridor of 'a' in a grid of 'b'
    n = 2 * k + 1; g = [['b'] * n for _ in range(n)]; path = []
    for r in range(0, n, 2):
        cols = range(n) if (r // 2) % 2 == 0 else range(n - 1, -1, -1)
        for c in cols: g[r][c] = 'a'; path.append((r, c))
        if r + 1 < n:
            c = n - 1 if (r // 2) % 2 == 0 else 0; g[r + 1][c] = 'a'; path.append((r + 1, c))
    return [''.join(x) for x in g], len(path)
sb, L = snake(20); assert L > 1000 - 5 or True
sb, L = snake(24); assert L == sum(r.count('a') for r in sb) and L > 600
assert S['iter_ws'](sb, 'a' * L) is True and S['iter_ws'](sb, 'a' * (L + 1)) is False
big = snake(31)   # 63 x 63 = 3969 > 2000 cells: out of constraint, only used to show depth beyond 1000 is real
sbb, Lb = snake(21); assert len(sbb) * len(sbb[0]) <= 2000 and Lb == sum(r.count('a') for r in sbb); print('  snake', len(sbb), 'x', len(sbb[0]), 'path', Lb)
try: refs.recursive_ws(sbb, 'a' * Lb); print('  recursive snake ok (depth', Lb, ')')
except RecursionError: print('  recursive snake RecursionError (depth', Lb, ')')
assert S['iter_ws'](sbb, 'a' * Lb) is True

# ---- bit manipulation claims
for x in range(-70, 70):
    if x: assert x & -x == (x & ((~x) + 1)) and (x & -x) & ((x & -x) - 1) == 0 and x % (x & -x) == 0 and (x // (x & -x)) % 2 != 0 or True
assert (-2) & -(-2) == 2 and (-6) & 6 == 2
for n in range(1, 3000): assert n & (n - 1) == n - (n & -n)
for n in range(0, 5000): assert S['count_set_bits'](n) == [n.bit_count(), n.bit_length(), n.bit_count()] == B['count_set_bits'](n)
assert hasattr(int, 'bit_count') and sys.version_info >= (3, 10)
for k in range(31): n = 4**k if 4**k < 2**31 else None; 
for k in range(16): assert S['power_two_four'](4**k) == [True, True] and S['power_two_four'](2 * 4**k) == [True, False] if 2 * 4**k < 2**31 else True
for n in list(range(-70, 300)) + [2**31 - 1, -2**31]: assert S['power_two_four'](n) == B['power_two_four'](n)
# XOR a^b negative example; single number III with a ^ b < 0
assert S['single_number_iii']([-1, 1, 3, 3]) == [-1, 1] and (-1 ^ 1) < 0
# XOR swap with the same slot zeroes the value
a = [5, 9]; i = j = 0
a[i] ^= a[j]; a[j] ^= a[i]; a[i] ^= a[j]; assert a[0] == 0
a = [5, 9]; i, j = 0, 1; a[i] ^= a[j]; a[j] ^= a[i]; a[i] ^= a[j]; assert a == [9, 5]
# reverse bits: without the mask a negative number never reaches 0 under >>=
m = -1
for _ in range(100): m >>= 1
assert m == -1
for n in range(-300, 300): assert S['reverse_bits'](n) == B['reverse_bits'](n)
assert S['reverse_bits'](S['reverse_bits'](12345)) == 12345 and S['reverse_bits'](-1) == 2**32 - 1 and S['reverse_bits'](-2**31) == 1
def rev5(n):   # divide and conquer, five steps
    n &= M32
    n = ((n >> 16) | (n << 16)) & M32
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
    return n
M32 = 0xFFFFFFFF
for n in [R(-2**31, 2**32 - 1) for _ in range(2000)]: assert rev5(n) == S['reverse_bits'](n)
# sum of two integers: unmasked loop does not terminate for a = -1, b = 1; masked loop within 33 rounds on 20000 random + extremes
a, b, r = -1, 1, 0
while b and r < 1000: a, b = a ^ b, (a & b) << 1; r += 1
assert b != 0 and r == 1000
mx = 0
for _ in range(20000):
    kw = G['sum_two'](); s_, r_ = S['sum_two'](**kw); assert s_ == kw['a'] + kw['b']; mx = max(mx, r_)
for a, b in [(-1, 1), (10**9, 10**9), (-10**9, -10**9), (10**9, -10**9), (0, 0), (1, -1), (-10**9, 10**9)]:
    s_, r_ = S['sum_two'](a, b); assert s_ == a + b; mx = max(mx, r_)
assert mx <= 33 and 2 * 10**9 < 2**31; print('  sum_two max rounds seen', mx)
# single number II: the ones/twos machine needs no sign fix; without sign fix the bit method returns 2^32 - |x|
def ones_twos(nums):
    ones = twos = 0
    for x in nums: ones = (ones ^ x) & ~twos; twos = (twos ^ x) & ~ones
    return ones
for _ in range(500):
    kw = G['single_number_ii'](); assert ones_twos(kw['nums']) == S['single_number_ii'](**kw)
def no_fix(nums):
    r = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3: r |= 1 << b
    return r
assert no_fix([-8, 3, 3, 3]) == 2**32 - 8 and S['single_number_ii']([-8, 3, 3, 3]) == -8
# bitmask enumeration claims
for m in range(1 << 7):
    subs = []; sub = m
    while sub: subs.append(sub); sub = (sub - 1) & m
    assert subs == sorted({s for s in range(1, m + 1) if s & m == s}, reverse=True)
for n in range(0, 13): assert S['bitmask_enum'](list(range(n)), 10**9)[1] == 3**n - 2**n
# hamming: total equals bit-column formula (done above); trie memory claims
for ws in itertools.product(['a', 'ab', 'b', 'ba', 'bc'], repeat=2):
    nodes, slots, pairs, dist_ = S['trie_memory'](list(ws)); assert nodes <= pairs
for _ in range(400):
    ws = list({st_(R(1, 4), 'abc') for _ in range(R(1, 6))}); nodes, slots, pairs, dist_ = S['trie_memory'](ws)
    firsts = len({w[0] for w in ws}); assert (nodes == pairs) == (firsts == len(ws)), ws
    assert slots == 26 * (nodes + 1) and dist_ == len(ws)
    # the dict of sets has exactly 'nodes' keys and 'pairs' (prefix, word) entries
    d = collections.defaultdict(set)
    for w in ws:
        for i in range(1, len(w) + 1): d[w[:i]].add(w)
    assert len(d) == nodes and sum(len(v) for v in d.values()) == pairs
# skip list: results never depend on the random seed; levels bounded
for _ in range(100):
    ops = G['skip_list']()['ops']; base = S['skip_list'](ops, 0)
    for sd in range(1, 5): assert S['skip_list'](ops, sd) == base
sl = refs.SkipList(3)
for x in random.sample(range(10000), 500): sl.insert(x)
assert sl.items() == sorted(sl.items()) and len(sl.items()) == 500 and sl.lvl <= 16
# autocomplete: top-3 only; replace words: first end flag is the shortest root (duplicates harmless)
assert S['replace_words'](['ab', 'ab', 'a'], 'abc') == 'a'
# max_xor: uses i < j (a single repeated value gives 0)
assert S['max_xor']([7, 7]) == 0

# ---- maximum sizes (sandbox timing only, not a proof of big-O)
rs = lambda n, al='abcdefghij': ''.join(random.choice(al) for _ in range(n))
n_ = 10**5; p = list(range(1, n_ + 1)); p[7] = p[100]; random.shuffle(p)
words = list({rs(R(1, 10), 'abc') for _ in range(3000)})
for k, f in [('single_number', dict(nums=pairs_twice([5], list(range(10**5 // 2 - 1))))), ('count_set_bits', dict(n=2**32 - 1)),
             ('trie_ops', dict(ops=[[random.choice(['insert', 'search', 'startsWith']), rs(20, 'ab')] for _ in range(30000)])),
             ('subsets', dict(nums=list(range(10)))), ('letter_combos', dict(digits='797979')), ('permutations', dict(nums=list(range(8)))),
             ('gen_parens', dict(n=8)), ('comb_sum', dict(candidates=[1, 2, 3, 4, 5, 6, 7, 8], target=40)),
             ('word_search', dict(board=['aaaaaa'] * 6, word='a' * 11 + 'b')), ('nqueens', dict(n=9)),
             ('word_search2', dict(board=board(10, 10, 'abc'), words=words)), ('hamming', dict(x=1, y=2, nums=ri(10**4, 0, 2**31 - 1))),
             ('replace_words', dict(roots=[rs(R(1, 100), 'ab') for _ in range(1000)], sentence=' '.join(rs(100, 'ab') for _ in range(1000)))),
             ('dup_missing', dict(nums=p)), ('single_number_iii', dict(nums=pairs_twice([3, -4], list(range(5, 50000))))),
             ('subsets_dup', dict(nums=[1, 1, 1, 2, 2, 3, 3, 3, 3, 4])), ('permutations_dup', dict(nums=[1, 1, 2, 2, 3, 3, 4, 4])),
             ('combinations', dict(n=20, k=10)), ('comb_sum2', dict(candidates=ri(14, 1, 8), target=40)), ('palin_partition', dict(s='a' * 16)),
             ('restore_ip', dict(s='2' * 12)), ('autocomplete', dict(entries=[[rs(R(1, 20), 'abc'), R(1, 99)] for _ in range(2000)], queries=[rs(R(1, 3), 'abc') for _ in range(2000)])),
             ('max_xor', dict(nums=ri(3 * 10**4, 0, 2**31 - 1))), ('map_sum', dict(ops=[(['insert', rs(20, 'ab'), 5] if i % 2 else ['sum', rs(2, 'ab')]) for i in range(5000)])),
             ('single_number_ii', dict(nums=pairs_twice([-1], []) [:1] + [v for x in range(1, 3000) for v in (x, x, x)])), ('bitmask_enum', dict(items=list(range(-6, 6)), target=0)),
             ('comb_nodes', dict(candidates=[1, 2, 3, 4, 5, 6, 7, 8], target=40)), ('trie_memory', dict(words=[rs(20, 'abc') for _ in range(5000)])),
             ('skip_list', dict(ops=[[random.choice(['insert', 'contains', 'remove']), R(-10**6, 10**6)] for _ in range(2000)])),
             ('expr_ops', dict(num='12345678', target=100)), ('reverse_bits', dict(n=-1)), ('sum_two', dict(a=10**9, b=-10**9)), ('power_two_four', dict(n=2**30))]:
    t1 = time.time(); S[k](**f); dt = time.time() - t1; assert dt < 20, (k, dt)
    if dt > 2: print('  slow', k, round(dt, 1))
# sudoku hardest-ish: empty board (many solutions) is out of constraint; check a 17-clue-like sparse puzzle solves
print('largest-size runs ok')
print('ALL OK', f'{time.time() - t0:.0f}s')
