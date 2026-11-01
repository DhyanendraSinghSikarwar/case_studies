import itertools
import random
from collections import deque

random.seed(33)

def alien_order(words):
    """Edges from the first differing letters of ADJACENT words, then Kahn's algorithm. '' if impossible."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:                       # one edge per distinct ordered pair
                    adj[x].add(y)
                    indeg[y] += 1
                break
        else:                                             # no differing letter: one word is a prefix of the other
            if len(a) > len(b):                           # longer word first is impossible
                return ''
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''   # fewer than all letters: a cycle

def sorted_under(words, order):
    rank = {c: i for i, c in enumerate(order)}
    key = lambda w: [rank[c] for c in w]                  # list comparison: a proper prefix is smaller
    return all(key(a) <= key(b) for a, b in zip(words, words[1:]))

def valid(words, got):
    """The checker the prompt states: each letter exactly once and the list sorted under it; '' only if NO ordering works."""
    letters = sorted({c for w in words for c in w})
    if got == '':
        return not any(sorted_under(words, p) for p in itertools.permutations(letters))
    return sorted(got) == letters and sorted_under(words, got)

def alien_brute(words):
    letters = sorted({c for w in words for c in w})
    for p in itertools.permutations(letters):
        if sorted_under(words, p):
            return ''.join(p)
    return ''

def alien_all_pairs(words):
    """Same algorithm but with constraints from EVERY pair i < j: shows adjacent pairs already imply all of them."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a, b = words[i], words[j]
            for x, y in zip(a, b):
                if x != y:
                    adj[x].add(y)
                    break
            else:
                if len(a) > len(b):
                    return ''
    indeg = {c: 0 for c in letters}
    for u in letters:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''

def alien_no_prefix_check(words):
    """Bug: ignore the 'longer word before its own prefix' case."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:
                    adj[x].add(y)
                    indeg[y] += 1
                break
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''

for w, shown in [(['wrt', 'wrf', 'er', 'ett', 'rftt'], 'wertf'), (['z', 'x', 'z'], ''), (['abc', 'ab'], ''), (['a', 'b', 'a'], ''), (['ab'], 'ab')]:
    got = alien_order(w)
    assert valid(w, got) and valid(w, shown), (w, got, shown)
    print(w, '->', repr(got), '| prompt shows', repr(shown), '| both accepted')

print("no prefix check on ['abc','ab'] ->", repr(alien_no_prefix_check(['abc', 'ab'])), '(wrongly accepted: no differing letter, so no edge)')

# ---- exhaustive: every list of 1..4 words over {a,b,c}, lengths 1..2 (12 possible words): our answer is accepted by the validator,
# '' appears exactly when no permutation works, and adjacent-pair edges agree with all-pair edges
words_all = [''.join(p) for L in (1, 2) for p in itertools.product('abc', repeat=L)]
cnt = empties = 0
for k in range(1, 5):
    for combo in itertools.product(words_all, repeat=k):
        w = list(combo)
        got = alien_order(w)
        assert valid(w, got), (w, got)
        assert (got == '') == (alien_brute(w) == ''), w
        assert (alien_all_pairs(w) == '') == (got == ''), w
        empties += got == ''
        cnt += 1
print('exhaustive on', cnt, 'word lists:', empties, 'impossible; all answers accepted by the validator, adjacent pairs == all pairs')

# ---- seeded random lists over 5 letters: sample from a hidden alphabet order so most are solvable, then corrupt some
for t in range(400):
    alpha = random.sample('abcde', 5)
    rank = {c: i for i, c in enumerate(alpha)}
    ws = [''.join(random.choice('abcde') for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 8))]
    ws.sort(key=lambda s: [rank[c] for c in s])
    if t % 3 == 0 and len(ws) > 1:
        i, j = random.sample(range(len(ws)), 2)
        ws[i], ws[j] = ws[j], ws[i]                      # may break sortedness
    got = alien_order(ws)
    assert valid(ws, got), (ws, got)
    assert (alien_all_pairs(ws) == '') == (got == '')
print('400 seeded random lists (5 letters): accepted by the validator; adjacent == all pairs')

# ---- letters with no constraint must still appear exactly once
r = alien_order(['x', 'y', 'q'])
assert sorted(alien_order(['ab', 'cd'])) == list('abcd') and sorted(r) == list('qxy') and valid(['x', 'y', 'q'], r)
print("unconstrained letters: ['ab','cd'] ->", alien_order(['ab', 'cd']))

# ---- max size: 100 words of length 100 over 26 letters in one hidden order; plus a 26-letter chain
alpha = random.sample('abcdefghijklmnopqrstuvwxyz', 26)
rank = {c: i for i, c in enumerate(alpha)}
ws = sorted((''.join(random.choice(alpha) for _ in range(100)) for _ in range(100)), key=lambda s: [rank[c] for c in s])
got = alien_order(ws)
assert got != '' and sorted(got) == sorted(set(''.join(ws))) and sorted_under(ws, got)
print('100 words of length 100: letters', len(got), 'ordering accepted')
chain = [alpha[i] for i in range(26)]
assert alien_order(chain) == ''.join(alpha) and alien_order(['a']) == 'a'
print('edge asserts passed')
