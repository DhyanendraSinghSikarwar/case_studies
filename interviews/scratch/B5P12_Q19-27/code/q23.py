import itertools, random

random.seed(23)

def restore(s, prune_len=True):
    """Returns (sorted addresses, calls). Part lengths 1, 2, 3 tried in that order; no leading zero; value <= 255.
    prune_len=True also stops when the remaining characters cannot fit the remaining parts."""
    out = []; calls = 0
    def go(i, parts):
        nonlocal calls
        calls += 1
        left = 4 - len(parts)
        if left == 0:
            if i == len(s): out.append('.'.join(parts))
            return
        rest = len(s) - i
        if prune_len and not (left <= rest <= 3 * left): return
        for L in (1, 2, 3):
            t = s[i:i + L]
            if len(t) < L or (L > 1 and t[0] == '0') or int(t) > 255: continue
            go(i + L, parts + [t])
    go(0, [])
    return sorted(out), calls

def solve(s): return restore(s)[0]

def brute(s):
    n = len(s); out = []
    if n < 4: return out
    for cuts in itertools.combinations(range(1, n), 3):
        ps = [s[a:b] for a, b in zip((0,) + cuts, cuts + (n,))]
        if all(str(int(p)) == p and int(p) <= 255 for p in ps): out.append('.'.join(ps))
    return sorted(out)

for s, exp in [('1921681', ['1.9.216.81', '1.92.16.81', '1.92.168.1', '19.2.16.81', '19.2.168.1', '19.21.6.81', '19.21.68.1', '19.216.8.1', '192.1.6.81', '192.1.68.1', '192.16.8.1']),
               ('0000', ['0.0.0.0']), ('010010', ['0.10.0.10', '0.100.1.0']), ('111', []), ('', [])]:
    got = solve(s)
    assert got == exp == brute(s)
    print('example', repr(s), '->', got)

def tree(s):
    def go(i, parts, d):
        left = 4 - len(parts)
        if left == 0:
            print('  ' * d + ('-> address ' + '.'.join(parts) if i == len(s) else f'-> parts full but {len(s) - i} char(s) left: dead')); return
        rest = len(s) - i
        if not (left <= rest <= 3 * left): print('  ' * d + f'prune: {rest} char(s) cannot fill {left} part(s)'); return
        for L in (1, 2, 3):
            t = s[i:i + L]
            if len(t) < L: continue
            if L > 1 and t[0] == '0': print('  ' * d + f'{t!r}: leading zero'); continue
            if int(t) > 255: print('  ' * d + f'{t!r}: > 255'); continue
            print('  ' * d + f'part {t!r}'); go(i + L, parts + [t], d + 1)
    go(0, [], 0)
print("decision tree for '010010':"); tree('010010')

# node counts
print('calls: length-pruned vs basic (validity only), 3^4 = 81 leaf choices at most:')
for s in ['1921681', '010010', '0000', '111', '255255255255', '999999999999', '1' * 12, '1' * 13]:
    a, ca = restore(s, True); b, cb = restore(s, False)
    assert a == b
    print(f'  {s:14s} answers={len(a):3d} calls pruned={ca:4d} basic={cb:4d}')

# claim: tree has at most 3^4 = 81 leaves, so at most 1 + 3 + 9 + 27 + 81 = 121 calls
mx = 0; seen = 0
for L in range(0, 9):
    for tup in itertools.product('012', repeat=L):
        s = ''.join(tup); seen += 1
        r, c = restore(s, False); assert c <= 121 and r == brute(s); mx = max(mx, c)
for _ in range(3000):
    s = ''.join(random.choice('0123456789' if random.random() < .5 else '1250') for _ in range(random.randint(0, 12)))
    r, c = restore(s, False); assert c <= 121 and r == brute(s); mx = max(mx, c)
print('basic search never made more than', mx, 'calls (bound 121) over', seen, 'exhaustive strings (digits 0,1,2, length <= 8) + 3000 random ones')

# seeded random cross-check against three-cut-position oracle, with lengths 0..12
for _ in range(400):
    s = ''.join(random.choice('0012559') for _ in range(random.randint(0, 12)))
    assert solve(s) == brute(s), s
print('400 seeded random strings agree with itertools.combinations of cut positions')

# edge asserts
assert solve('') == [] and solve('111') == [] and solve('1' * 13) == [] and solve('0000') == ['0.0.0.0']
assert solve('25525511135') == ['255.255.11.135', '255.255.111.35']
assert solve('256256256256') == [] and solve('255255255255') == ['255.255.255.255'] and solve('00000') == []
assert solve('101023') == sorted(['1.0.10.23', '1.0.102.3', '10.1.0.23', '10.10.2.3', '101.0.2.3'])
print('edge asserts passed')
