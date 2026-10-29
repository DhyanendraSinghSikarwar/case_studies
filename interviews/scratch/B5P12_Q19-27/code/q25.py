import random, time

random.seed(25)
FULL = 0x3FE            # bits 1..9 set: digit d is bit d. Python's ~ gives a NEGATIVE number, so we always mask with FULL.

def digits_of(m):
    return [i for i in range(1, 10) if m >> i & 1]

def solve_mrv(board, trace=None):
    """Bitmask backtracking, most-constrained empty cell first. Returns (solution rows, nodes)."""
    g = [[0 if ch == '.' else int(ch) for ch in row] for row in board]
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9; empties = []
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]; rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b
            else: empties.append((r, c))
    nodes = 0
    def solve():
        nonlocal nodes
        nodes += 1
        if not empties: return True
        best = -1; bm = 0; bk = 10
        for idx, (r, c) in enumerate(empties):
            m = ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & FULL        # candidates of this cell
            k = m.bit_count()
            if k < bk:
                best, bm, bk = idx, m, k
                if k <= 1: break                                                 # a forced cell (or a dead end) cannot be beaten
        if bk == 0: return False                                                 # some cell has no candidate: prune
        empties[best], empties[-1] = empties[-1], empties[best]
        r, c = empties.pop(); bi = r // 3 * 3 + c // 3
        if trace is not None and len(trace) < 6: trace.append(((r, c), digits_of(bm)))
        while bm:
            low = bm & -bm; bm ^= low; v = low.bit_length() - 1                   # lowest candidate bit, then its digit
            g[r][c] = v; rows[r] |= low; cols[c] |= low; boxes[bi] |= low
            if solve(): return True
            rows[r] ^= low; cols[c] ^= low; boxes[bi] ^= low; g[r][c] = 0
        empties.append((r, c)); empties[best], empties[-1] = empties[-1], empties[best]
        return False
    assert solve(), 'no solution'
    return [''.join(map(str, row)) for row in g], nodes

def solve_fixed_order(board, cap=None):
    """Same masks, same candidate extraction, but cells in reading order (no heuristic). Returns (rows or None, nodes)."""
    g = [[0 if ch == '.' else int(ch) for ch in row] for row in board]
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9; empties = []
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]; rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b
            else: empties.append((r, c))
    nodes = 0
    def go(i):
        nonlocal nodes
        nodes += 1
        if cap and nodes > cap: raise OverflowError
        if i == len(empties): return True
        r, c = empties[i]; bi = r // 3 * 3 + c // 3
        m = ~(rows[r] | cols[c] | boxes[bi]) & FULL
        while m:
            low = m & -m; m ^= low; v = low.bit_length() - 1
            g[r][c] = v; rows[r] |= low; cols[c] |= low; boxes[bi] |= low
            if go(i + 1): return True
            rows[r] ^= low; cols[c] ^= low; boxes[bi] ^= low
        return False
    try: ok = go(0)
    except OverflowError: return None, nodes
    return ([''.join(map(str, row)) for row in g] if ok else None), nodes

def plain(board, limit=1):
    """Oracle: cell by cell, tries '1'..'9', checks row, column and box by scanning; counts solutions up to `limit`."""
    g = [list(r) for r in board]; found = []
    def ok(r, c, ch):
        if any(g[r][k] == ch or g[k][c] == ch for k in range(9)): return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        if len(found) >= limit: return
        while pos < 81 and g[pos // 9][pos % 9] != '.': pos += 1
        if pos == 81: found.append([''.join(r) for r in g]); return
        r, c = divmod(pos, 9)
        for ch in '123456789':
            if ok(r, c, ch): g[r][c] = ch; go(pos + 1); g[r][c] = '.'
    go(0); return found

def valid(rows):
    if len(rows) != 9 or any(len(r) != 9 for r in rows): return False
    want = set('123456789')
    for i in range(9):
        if set(rows[i]) != want or set(rows[j][i] for j in range(9)) != want: return False
        if {rows[3 * (i // 3) + a][3 * (i % 3) + b] for a in range(3) for b in range(3)} != want: return False
    return True

EX = ['.1....3..', '.586.3.24', '..92..5..', '.4.1...5.', '..6.24.17', '.8...94.2', '8.5...74.', '471...2..', '.....7..5']
EXP = ['214785369', '758693124', '639241578', '342178956', '596324817', '187569432', '865932741', '471856293', '923417685']
trace = []
sol, n_mrv = solve_mrv(EX, trace)
assert sol == EXP == plain(EX, 2)[0] and len(plain(EX, 2)) == 1 and valid(sol)
print('example solved:', sol)
print('empty cells:', sum(r.count('.') for r in EX), '| search calls with most-constrained cell first:', n_mrv)
for (rc, cands) in trace: print(f'  step: choose cell {rc} with candidates {cands}')

# the Python negative-integer point, as observed on Python 3.13
m = 0b0000100110
print('~m =', ~m, '(negative); ~m & FULL =', bin(~m & FULL), '-> digits', digits_of(~m & FULL))
x = 0b101000
print('x & -x =', bin(x & -x), '(lowest set bit);  (x & -x).bit_length() - 1 =', (x & -x).bit_length() - 1)
print('digit d as a bit: 1 << 7 =', bin(1 << 7), '; row mask with 5 and 9 set =', bin((1 << 5) | (1 << 9)))

# search cost of the heuristic: same masks, reading-order cells
sol2, n_fixed = solve_fixed_order(EX)
assert sol2 == EXP
print('same example, reading-order cells with the same masks:', n_fixed, 'calls (against', n_mrv, 'with the heuristic)')

# a puzzle that is hard for reading order (empty-heavy first row; unique solution)
HARD = ['.........', '.....3.85', '..1.2....', '...5.7...', '..4...1..', '.9.......', '5......73', '..2.1....', '....4...9']
h_sol, n_h = solve_mrv(HARD)
assert valid(h_sol) and all(a == '.' or a == b for ra, rb in zip(HARD, h_sol) for a, b in zip(ra, rb))
t0 = time.time(); r_fixed, n_f = solve_fixed_order(HARD, cap=3_000_000); t1 = time.time() - t0
print('hard puzzle (17 givens):', 'heuristic', n_h, 'calls;', ('reading order ' + str(n_f) + ' calls') if r_fixed else 'reading order gave up after ' + str(n_f) + ' calls (cap 3,000,000)', f'(sandbox timing of that run {t1:.1f} s)')
assert r_fixed is None or r_fixed == h_sol

# seeded random puzzles with a unique solution; compare with the plain oracle and check validity
def random_full(rnd):
    g = [['.'] * 9 for _ in range(9)]
    def ok(r, c, ch):
        if any(g[r][k] == ch or g[k][c] == ch for k in range(9)): return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        if pos == 81: return True
        r, c = divmod(pos, 9); ds = list('123456789'); rnd.shuffle(ds)
        for ch in ds:
            if ok(r, c, ch):
                g[r][c] = ch
                if go(pos + 1): return True
                g[r][c] = '.'
        return False
    go(0); return [''.join(r) for r in g]
def make_puzzle(rnd, remove):
    full = random_full(rnd); g = [list(r) for r in full]
    cells = [(r, c) for r in range(9) for c in range(9)]; rnd.shuffle(cells); removed = 0
    for r, c in cells:
        if removed >= remove: break
        keep = g[r][c]; g[r][c] = '.'
        if len(plain([''.join(x) for x in g], 2)) == 1: removed += 1
        else: g[r][c] = keep
    return [''.join(x) for x in g], full
rnd = random.Random(250)
nm = []; nf = []
for i in range(40):
    puz, full = make_puzzle(rnd, rnd.randint(30, 50))
    s1, a = solve_mrv(puz); assert s1 == full == plain(puz, 1)[0] and valid(s1)
    assert all(p == '.' or p == q for rp, rq in zip(puz, s1) for p, q in zip(rp, rq))
    s2, b = solve_fixed_order(puz); assert s2 == full
    nm.append(a); nf.append(b)
print('40 seeded random puzzles with a unique solution: all agree with the plain solver and are valid grids')
print('  calls with heuristic: total', sum(nm), 'max', max(nm), '| reading order: total', sum(nf), 'max', max(nf))

# edge asserts: an already solved board, one empty cell
assert solve_mrv(EXP)[0] == EXP
one = [EXP[0][:4] + '.' + EXP[0][5:]] + EXP[1:]
assert solve_mrv(one)[0] == EXP
print('edge asserts passed (solved board; one empty cell); recursion depth = empty cells <= 81')
