import random
import sys

random.seed(1203)

class TrieDict:
    """Nodes are dicts: children by letter; the key '$' is NOT used, the flag is a separate tuple slot."""
    __slots__ = ('root',)
    def __init__(self):
        self.root = [{}, False]            # [children, is_end]
    def insert(self, w):
        node = self.root
        for ch in w:
            nxt = node[0].get(ch)
            if nxt is None:
                nxt = node[0][ch] = [{}, False]
            node = nxt
        node[1] = True                      # duplicate insert just sets True again
    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node[0].get(ch)
            if node is None:
                return None
        return node
    def search(self, w):
        node = self._walk(w)
        return node is not None and node[1]
    def startsWith(self, p):
        return self._walk(p) is not None

class TrieArray:
    """Same API, 26-slot list per node (lowercase only)."""
    __slots__ = ('kids', 'end')
    def __init__(self):
        self.kids = [None] * 26
        self.end = False
    def insert(self, w):
        node = self
        for ch in w:
            i = ord(ch) - 97
            if node.kids[i] is None:
                node.kids[i] = TrieArray()
            node = node.kids[i]
        node.end = True
    def _walk(self, s):
        node = self
        for ch in s:
            node = node.kids[ord(ch) - 97]
            if node is None:
                return None
        return node
    def search(self, w):
        node = self._walk(w)
        return node is not None and node.end
    def startsWith(self, p):
        return self._walk(p) is not None

def run(ops, cls=TrieDict):
    t, out = cls(), []
    for op, arg in ops:
        if op == 'insert':
            t.insert(arg); out.append(None)
        elif op == 'search':
            out.append(t.search(arg))
        else:
            out.append(t.startsWith(arg))
    return out

def brute(ops):                      # plain set + startswith
    words, out = set(), []
    for op, arg in ops:
        if op == 'insert':
            words.add(arg); out.append(None)
        elif op == 'search':
            out.append(arg in words)
        else:
            out.append(any(w.startswith(arg) for w in words))
    return out

examples = [
    ([['insert', 'apple'], ['search', 'apple'], ['search', 'app'], ['startsWith', 'app'], ['insert', 'app'], ['search', 'app']],
     [None, True, False, True, None, True]),
    ([['startsWith', 'a']], [False]),
    ([['insert', 'to'], ['insert', 'to'], ['search', 't'], ['startsWith', 'to'], ['startsWith', 'top']],
     [None, None, False, True, False]),
]
for ops, want in examples:
    for cls in (TrieDict, TrieArray):
        assert run(ops, cls) == want == brute(ops)
    print(run(ops))

# dry run: structure after inserting apple then app
t = TrieDict(); t.insert('apple'); t.insert('app')
node, path = t.root, ''
while node[0]:
    ch = next(iter(node[0])); node = node[0][ch]; path += ch
    print(f'  node {path!r:8} end={node[1]}')

# seeded random cross-check
for _ in range(2000):
    ops = [[random.choice(['insert', 'search', 'startsWith']), ''.join(random.choice('abc') for _ in range(random.randint(1, 4)))]
           for _ in range(random.randint(1, 30))]
    want = brute(ops)
    assert run(ops, TrieDict) == want and run(ops, TrieArray) == want
print('random cross-check ok: 2000 cases')

# edge cases: length-20 words, whole alphabet, prefix equal to a word
w = 'z' * 20
assert run([['insert', w], ['search', w], ['startsWith', w[:7]], ['search', w[:7]]]) == [None, True, True, False]
alpha = 'abcdefghijklmnopqrstuvwxyz'
assert run([['insert', alpha], ['startsWith', alpha[:13]], ['startsWith', alpha[:13] + 'z']], TrieArray) == [None, True, False]

# memory comparison for 1000 random 8-letter words (sys.getsizeof counts only the container itself: a rough guide)
words = [''.join(random.choice(alpha) for _ in range(8)) for _ in range(1000)]
td, ta = TrieDict(), TrieArray()
for x in words:
    td.insert(x); ta.insert(x)
def size_dict(node):
    return sys.getsizeof(node) + sys.getsizeof(node[0]) + sum(size_dict(c) for c in node[0].values())
def size_arr(node):
    return sys.getsizeof(node) + sys.getsizeof(node.kids) + sum(size_arr(c) for c in node.kids if c)
def count(node):
    return 1 + sum(count(c) for c in node[0].values())
print('nodes:', count(td.root), ' dict-trie bytes:', size_dict(td.root), ' array-trie bytes:', size_arr(ta))
print('edge asserts ok')
