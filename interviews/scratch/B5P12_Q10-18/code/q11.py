import random

random.seed(1211)
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def find_words(board, words, stats=None, prune=True, log=None):
    """Trie of all words + ONE DFS per start cell. The word is stored at its end node; found leaves are pruned."""
    R, C = len(board), len(board[0])
    root = {}
    for w in words:
        nd = root
        for ch in w:
            nd = nd.setdefault(ch, {})
        nd['$'] = w                                   # whole word stored at the end node
    g = [list(r) for r in board]
    found = []
    visits = 0
    def dfs(r, c, parent):
        nonlocal visits
        ch = g[r][c]
        nd = parent[ch]
        visits += 1                                   # one visit = one (cell, trie node) pair entered
        if log is not None: log.append('visit (%d,%d) %r%s' % (r, c, ch, '  -> found ' + nd['$'] if '$' in nd else ''))
        if '$' in nd:
            found.append(nd.pop('$'))                 # report once; pop so it cannot be reported twice
        g[r][c] = '#'                                 # mark the cell used on this path
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] in nd:   # '#' and '$' are never children letters
                dfs(nr, nc, nd)
        g[r][c] = ch                                  # undo
        if prune and not nd:                          # no words left below: cut the branch
            del parent[ch]
    for r in range(R):
        for c in range(C):
            if g[r][c] in root:
                dfs(r, c, root)
    if stats is not None: stats.append(visits)
    return sorted(found)

def single_word(board, word, counter=None):
    """Q9-style search for ONE word (recursive, marks and unmarks the cell)."""
    R, C = len(board), len(board[0])
    g = [list(r) for r in board]
    def go(r, c, k):
        if counter is not None: counter[0] += 1
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                g[r][c] = word[k]; return True
        g[r][c] = word[k]
        return False
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def brute(board, words, counter=None):
    return sorted(w for w in words if single_word(board, w, counter))

for b, ws, want in [(['cats', 'xaot', 'dgsr'], ['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot'], ['cat', 'cats']),
                    (['ab'], ['ab', 'ba', 'aba'], ['ab', 'ba']), (['a'], ['b'], [])]:
    assert find_words(b, ws) == brute(b, ws) == want, (b, ws)
print("3 prompt examples ok")

# dry run: which words the trie DFS reports on the first example, and how many (cell, node) visits it needs
b, ws = ['cats', 'xaot', 'dgsr'], ['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot']
st = []
print("first example:", find_words(b, ws, st), "trie visits:", st[0])
cnt = [0]; brute(b, ws, cnt)
lg = []; find_words(b, ws, [], log=lg)
print("\n".join(lg))
print("same example, one search per word: calls =", cnt[0])

# seeded random cross-check
for _ in range(400):
    R_, C_ = random.randint(1, 4), random.randint(1, 4)
    board = [''.join(random.choice('abc') for _ in range(C_)) for _ in range(R_)]
    words = list({''.join(random.choice('abc') for _ in range(random.randint(1, 6))) for _ in range(random.randint(1, 15))})
    assert find_words(board, words) == brute(board, words), (board, words)
print("400 seeded random boards agree with one single-word search per word")

# why the trie wins: many words, shared prefixes (10 x 10 board, 3000 words, alphabet 'abc')
board = [''.join(random.choice('abc') for _ in range(10)) for _ in range(10)]
words = set()
while len(words) < 3000:
    words.add(''.join(random.choice('abc') for _ in range(random.randint(1, 10))))
words = sorted(words)
st = []; a = find_words(board, words, st)
cnt = [0]; b2 = brute(board, words, cnt)
assert a == b2
print("10x10 board, 3000 words: found %d words | trie visits %d | single-word calls %d" % (len(a), st[0], cnt[0]))
# effect of deleting exhausted branches: same answer, fewer visits when many words are found
board = [''.join(random.choice('ab') for _ in range(8)) for _ in range(8)]
words = sorted({''.join(random.choice('ab') for _ in range(random.randint(1, 8))) for _ in range(300)})
s1, s2 = [], []
assert find_words(board, words, s1, prune=True) == find_words(board, words, s2, prune=False)
print("8x8 board, %d words: visits with branch deletion %d, without %d" % (len(words), s1[0], s2[0]))
assert s1[0] <= s2[0]
# max-size edge cases
assert find_words(['a' * 10] * 10, ['a' * 10]) == ['a' * 10]
assert find_words(['a'], ['a']) == ['a']
assert find_words(['ab'], ['abc']) == []
assert find_words(['aa'], ['aaa']) == []                  # a cell may not be reused in one path
assert find_words(['ab', 'cd'], ['abdc', 'acdb', 'ad']) == ['abdc', 'acdb']   # 'ad' is diagonal
print("edge asserts ok")
