import random, string, heapq

random.seed(24)
K = 3

class AutoTrie:
    """Trie with, at every node, the best K (-count, word) pairs of the words at or below that node."""
    def __init__(self):
        self.root = {'c': {}, 'top': [], 'cnt': None}      # 'cnt' is the count if a word ends here
        self.nodes = 1
    def insert(self, word, count):
        nd = self.root
        path = [nd]
        for ch in word:
            if ch not in nd['c']:
                nd['c'][ch] = {'c': {}, 'top': [], 'cnt': None}; self.nodes += 1
            nd = nd['c'][ch]; path.append(nd)
        nd['cnt'] = count
        for p in path[1:]:                                  # update the whole path (the root list is never queried: prefixes are non-empty)
            p['top'] = sorted([e for e in p['top'] if e[1] != word] + [(-count, word)])[:K]
    def set_count(self, word, count):
        """Change a count later. Raising is a merge; LOWERING may need words that were not stored, so rebuild each list on the path from the children's lists."""
        nd = self.root; path = [nd]
        for ch in word:
            nd = nd['c'][ch]; path.append(nd)
        nd['cnt'] = count
        for p, w in zip(reversed(path[1:]), reversed(range(1, len(path)))):
            cand = [] if p['cnt'] is None else [(-p['cnt'], word[:w])]
            for child in p['c'].values(): cand += child['top']
            p['top'] = sorted(cand)[:K]
    def query(self, prefix):
        nd = self.root
        for ch in prefix:
            nd = nd['c'].get(ch)
            if nd is None: return []
        return [w for _, w in nd['top']]

def solve(entries, queries):
    t = AutoTrie()
    for w, c in entries: t.insert(w, c)
    return [t.query(p) for p in queries]

def brute(entries, queries):
    return [[w for c, w in sorted((-c, w) for w, c in entries if w.startswith(p))[:K]] for p in queries]

for ent, qs, exp in [([['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]], ['ca', 'car', 'd', 'x', 'cat'],
                       [['care', 'cart', 'car'], ['care', 'cart', 'car'], ['dog'], [], ['cat']]),
                     ([['a', 1]], ['a', 'ab'], [['a'], []]),
                     ([['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], ['a'], [['ab', 'ac', 'ad']])]:
    got = solve(ent, qs)
    assert got == exp == brute(ent, qs)
    print('example', ent, qs, '->', got)

# what is stored along the path for example 1
t = AutoTrie()
for w, c in [['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]]: t.insert(w, c)
print('stored top-3 per node, example 1:')
for pre in ['c', 'ca', 'car', 'cat', 'care', 'cart', 'd']:
    nd = t.root
    for ch in pre: nd = nd['c'][ch]
    print(f'  {pre!r:7}: {[(-c, w) for c, w in nd["top"]]}')

# work comparison on a larger set: words visited by "collect everything under the prefix and sort" versus stored lists
rnd = random.Random(240)
words = set()
while len(words) < 2000: words.add(''.join(rnd.choice('abc') for _ in range(rnd.randint(1, 8))) if rnd.random() < .5 else ''.join(rnd.choice(string.ascii_lowercase) for _ in range(rnd.randint(1, 8))))
big = [[w, rnd.randint(1, 100)] for w in sorted(words)]
def subtree_size(trie, prefix):
    nd = trie.root
    for ch in prefix:
        nd = nd['c'].get(ch)
        if nd is None: return 0
    seen = 0; stack = [nd]
    while stack:
        x = stack.pop(); seen += x['cnt'] is not None; stack += x['c'].values()
    return seen
bt = AutoTrie()
for w, c in big: bt.insert(w, c)
print('2000 words; words below prefix (what the collect-and-sort baseline must examine) versus stored entries read by a query:')
for p in ['a', 'ab', 'abc', 'q', 'zz']:
    print(f'  {p!r:6}: words below = {subtree_size(bt, p):4d}   query reads at most {K} stored entries after {len(p)} steps')
print('trie nodes for the 2000 words:', bt.nodes)

# seeded random cross-check vs startswith + sort
for _ in range(300):
    n = random.randint(1, 25)
    ws = sorted({''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(n)})
    ent = [[w, random.randint(1, 6)] for w in ws]; random.shuffle(ent)
    qs = [''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(8)]
    assert solve(ent, qs) == brute(ent, qs), (ent, qs)
print('300 seeded random cases agree with the filter-and-sort baseline (ties by word ascending)')

# later count changes: up and down, rebuilt along the path
bad = 0
for _ in range(200):
    ws = sorted({''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(20)})
    cur = {w: random.randint(1, 6) for w in ws}
    tr = AutoTrie()
    for w, c in cur.items(): tr.insert(w, c)
    for _ in range(15):
        w = random.choice(ws); cur[w] = random.randint(1, 6); tr.set_count(w, cur[w])
        qs = [''.join(random.choice('abc') for _ in range(random.randint(1, 3))) for _ in range(5)]
        assert [tr.query(p) for p in qs] == brute(list(cur.items()), qs)
print('200 x 15 random count changes (up and down) keep every answer equal to the baseline')
# showing why only "merge" is not enough when a count goes down
tr = AutoTrie()
for w, c in [['ab', 9], ['ac', 5], ['ad', 4], ['ae', 3]]: tr.insert(w, c)
before = tr.query('a'); tr.set_count('ab', 1); after = tr.query('a')
print("top-3 of 'a' before:", before, " after lowering 'ab' to 1:", after, "(ae was not stored; it had to come back from the children)")
assert before == ['ab', 'ac', 'ad'] and after == ['ac', 'ad', 'ae']

# edge asserts
assert solve([['a', 1]], ['a', 'ab', 'b']) == [['a'], [], []]
assert solve([['z' * 20, 5]], ['z' * 20, 'z' * 19]) == [['z' * 20], ['z' * 20]]
assert solve([['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], ['a']) == [['ab', 'ac', 'ad']]
print('edge asserts passed')
