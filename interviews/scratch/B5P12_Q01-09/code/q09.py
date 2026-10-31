import random

random.seed(1209)

def exists(board, word, stats=None):
    """Grid backtracking. The mark '#' is safe because boards hold letters only."""
    g = [list(r) for r in board]            # strings are immutable: work on a copy
    R, C = len(g), len(g[0])
    if stats is None:
        stats = {}
    stats['calls'] = 0
    def go(r, c, k):
        stats['calls'] += 1
        if g[r][c] != word[k]:              # prune first: wrong letter (or the '#' mark) ends this branch
            return False
        if k == len(word) - 1:
            return True
        saved, g[r][c] = g[r][c], '#'       # choose: mark the cell as on the current path
        found = False
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                found = True
                break
        g[r][c] = saved                     # undo: restore on EVERY way out, after the neighbours were tried
        return found
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def exists_no_restore(board, word):
    """WRONG on purpose: the cell is marked and never restored."""
    g = [list(r) for r in board]; R, C = len(g), len(g[0])
    def go(r, c, k):
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1): return True
        return False                                # the undo line is missing
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def brute(board, word):
    """Visited cells carried as an immutable tuple; nothing to undo."""
    R, C = len(board), len(board[0])
    def go(r, c, k, seen):
        if board[r][c] != word[k] or (r, c) in seen: return False
        if k == len(word) - 1: return True
        seen = seen + ((r, c),)
        return any(0 <= r + dr < R and 0 <= c + dc < C and go(r + dr, c + dc, k + 1, seen)
                   for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return any(go(r, c, 0, ()) for r in range(R) for c in range(C))

B0 = ['CATS', 'OXAT', 'DOGS']
examples = [(B0, 'CATS', True), (B0, 'TACO', True), (B0, 'SAT', False), (['AA'], 'AAA', False), (['Z'], 'Z', True)]
for b, w, want in examples:
    assert exists(b, w) == want == brute(b, w)
    print(b, repr(w), '->', exists(b, w))

# decision tree for TACO on B0: starting cells that pass the first-letter check, then the path
def trace(board, word):
    g = [list(r) for r in board]; R, C = len(g), len(g[0])
    def go(r, c, k, d):
        if g[r][c] != word[k]:
            print('  ' * d + f'({r},{c}) {g[r][c]!r} != {word[k]!r}: prune'); return False
        print('  ' * d + f'({r},{c}) {g[r][c]!r} matches word[{k}]')
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] != '#':
                if go(nr, nc, k + 1, d + 1): return True
        g[r][c] = board[r][c]
        return False
    for r in range(R):
        for c in range(C):
            if board[r][c] == word[0]:
                print(f'start ({r},{c})')
                if go(r, c, 0, 1): return True
    return False
print('found:', trace(B0, 'TACO'))

# calls with the first-letter check vs searching every self-avoiding path without any letter pruning
def count_paths(R, C, L):
    """Number of calls if letters are ignored: every self-avoiding walk of up to L cells is expanded."""
    seen = [[False] * C for _ in range(R)]; tot = [0]
    def go(r, c, k):
        tot[0] += 1
        if k == L - 1: return
        seen[r][c] = True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc]: go(nr, nc, k + 1)
        seen[r][c] = False
    for r in range(R):
        for c in range(C): go(r, c, 0)
    return tot[0]
st = {}
exists(B0, 'SAT', st); print('SAT on 3x4: pruned calls', st['calls'], ' letter-blind calls', count_paths(3, 4, 3))
exists(B0, 'CATSX', st); print('CATSX on 3x4: pruned calls', st['calls'], ' letter-blind calls', count_paths(3, 4, 5))
# adversarial: all 'A' and a word that ends in a letter that never appears: no letter prunes anything until the very end
st = {}
b6 = ['A' * 6] * 6
assert exists(b6, 'A' * 11 + 'B', st) is False
bound = 36 * 3 ** 11
print('worst-ish 6x6 all A, L=12: calls', st['calls'], ' R*C*3^(L-1) =', bound, ' within bound:', st['calls'] <= bound)

# seeded cross-check, and how often forgetting the undo is wrong
def rand_board():
    C = random.randint(1, 4)
    return [''.join(random.choice('ab') for _ in range(C)) for _ in range(random.randint(1, 4))]
bad = 0
for _ in range(2000):
    b = rand_board(); w = ''.join(random.choice('ab') for _ in range(random.randint(1, 7)))
    r = exists(b, w); assert r == brute(b, w)
    bad += exists_no_restore(b, w) != r
print('random cross-check ok: 2000 cases; no-restore variant wrong on', bad, 'of them')

# edge asserts
assert exists(['A'], 'AA') is False and exists(['AB'], 'BA') is True and exists(['A', 'B'], 'BA') is True
assert exists(['ABA'], 'ABA') is True and exists(['AB'], 'ABA') is False   # no cell reuse
assert exists(['ABCDEF'] * 1, 'F') and exists(['AAAAAA'] * 6, 'A' * 12) is True
print('edge asserts ok')
