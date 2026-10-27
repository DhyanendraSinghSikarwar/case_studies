import random
random.seed(41)

# ---- optimal: a trie. Each node = dict of children + count of words passing through it.
class TrieNode:
    __slots__ = ('kids', 'count')
    def __init__(self): self.kids = {}; self.count = 0

def trie_solve(words, queries):
    root, nodes = TrieNode(), 0
    for w in words:                                   # insert: L steps, one dict op each
        cur = root
        for ch in w:
            nxt = cur.kids.get(ch)
            if nxt is None: nxt = cur.kids[ch] = TrieNode(); nodes += 1
            cur = nxt; cur.count += 1                 # one more word passes through this prefix
    out = []
    for q in queries:                                 # query: at most len(q) steps
        cur = root
        for ch in q:
            cur = cur.kids.get(ch)
            if cur is None: break
        out.append(cur.count if cur is not None else 0)
    return out, nodes

# ---- brute force: scan every word per query; nodes = distinct non-empty prefixes
def brute(words, queries):
    counts = [sum(1 for w in words if w.startswith(q)) for q in queries]
    prefixes = {w[:i] for w in words for i in range(1, len(w) + 1)}
    return counts, len(prefixes)

# ---- examples from the question
assert trie_solve(['apple', 'app', 'apricot', 'bat'], ['app', 'ap', 'b', 'c']) == ([2, 3, 1, 0], 13)
assert trie_solve(['a', 'a'], ['a', 'aa']) == ([2, 0], 1)
print('examples ok:', trie_solve(['apple', 'app', 'apricot', 'bat'], ['app', 'ap', 'b', 'c']),
      trie_solve(['a', 'a'], ['a', 'aa']))

# ---- seeded cross-check (small alphabet forces shared prefixes, duplicates, prefix-of-another)
for _ in range(600):
    words = [''.join(random.choice('abc') for _ in range(random.randint(1, 6))) for _ in range(random.randint(1, 8))]
    queries = [''.join(random.choice('abc') for _ in range(random.randint(1, 7))) for _ in range(6)]
    assert trie_solve(words, queries) == brute(words, queries)
    nodes = trie_solve(words, queries)[1]
    assert nodes <= sum(map(len, words))              # at most one new node per inserted character
    assert nodes >= max(map(len, words))              # the longest word alone needs its whole path
print('600 random cases ok; nodes always between longest word and total letters')

# ---- edge cases
assert trie_solve(['abc'], ['abcd']) == ([0], 3)      # query longer than the word
assert trie_solve(['abc'], ['abc']) == ([1], 3)       # query equal to the word counts it
assert trie_solve(['a', 'ab', 'abc'], ['a', 'ab', 'abc']) == ([3, 2, 1], 3)   # chain: words are prefixes of each other
assert trie_solve(['x', 'y', 'z'], ['x', 'q']) == ([1, 0], 3)                 # disjoint first letters
print('edge asserts ok')

# ---- cost shape: a query costs at most len(query) dict lookups, whatever the number of words
def lookups(words, q):
    root = TrieNode()
    for w in words:
        cur = root
        for ch in w: cur = cur.kids.setdefault(ch, TrieNode())
    n, cur = 0, root
    for ch in q:
        n += 1; cur = cur.kids.get(ch)
        if cur is None: break
    return n
small = [''.join(random.choice('abcdefgh') for _ in range(10)) for _ in range(10)]
big = [''.join(random.choice('abcdefgh') for _ in range(10)) for _ in range(10000)]
q = big[0]
print('lookups for a 10-letter query with 10 words:', lookups(small + [q], q), '; with 10000 words:', lookups(big, q))
print('10000 words, 100000 letters in total -> trie nodes =', trie_solve(big, [])[1], '(shared prefixes are stored once)')
print('a set of the strings stores', sum(map(len, set(big))), 'letters and still scans all', len(set(big)), 'words for a prefix query')
