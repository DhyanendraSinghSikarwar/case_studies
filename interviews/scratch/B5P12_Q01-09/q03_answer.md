### Q3 ⭐⭐⭐ 🟡 Implement a trie (prefix tree) over lowercase words. `ops` is a list of operations (1 <= len <= 3*10^4), each `['insert', w]`, `['search', w]` or `['startsWith', p]` with 1 <= len(w), len(p) <= 20. Return one result per operation in order: `null` (Python None) for insert, True or False for search (True only if exactly that whole word was inserted before) and True or False for startsWith (True if some inserted word begins with p, including a word equal to p). Duplicate inserts are allowed and change nothing. Build nodes as dicts of children plus an end-of-word flag, and compare with a list of 26 children per node. State the cost of each operation in terms of the word length L (not the number of words). Part 7 Q41 builds a trie at concept level to count words per prefix; here you write the full insert, search and prefix API as a reusable class. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a plain set of inserted words with `startswith` on small inputs. Example: ops=[['insert', 'apple'], ['search', 'apple'], ['search', 'app'], ['startsWith', 'app'], ['insert', 'app'], ['search', 'app']] -> [null, True, False, True, null, True]; ops=[['startsWith', 'a']] -> [False]; ops=[['insert', 'to'], ['insert', 'to'], ['search', 't'], ['startsWith', 'to'], ['startsWith', 'top']] -> [null, null, False, True, False].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie (prefix tree). Shared prefixes share nodes, so cost depends on the word length, not on the number of words.

**Say this first (1 line):** "Each node maps a letter to a child and has an end-of-word flag. insert, search and startsWith all walk one node per letter: O(L) time each, independent of how many words are stored. search needs the flag, startsWith does not."

**Brute force:** Keep a set of words. search is O(L) (hash), but startsWith must scan all words with `startswith`: O(N * L). Sorting the words and using bisect makes prefix queries O(L log N) but insertions O(N) in a list.

**Optimal:**
- Node = children map + `is_end`. The root represents the empty string.
- insert(w): walk from the root, create missing children, set `is_end = True` on the last node. A duplicate insert walks existing nodes and sets the flag to True again: no change.
- search(w): walk; if a letter is missing return False; at the end return `is_end`. So 'app' is not found after inserting only 'apple' (the node exists but is_end is False).
- startsWith(p): walk; return True if you reach a node, ignoring the flag. A word equal to p counts, because that node exists.
- Node representations:
  - dict of children: only the letters actually used are stored, any alphabet, small for sparse tries.
  - list of 26: O(1) index with no hashing and no key objects, but 26 pointers per node even if only one child is used, and it only works for lowercase letters.
  - In my run (sandbox only, `sys.getsizeof` summed over node containers, so a rough guide) 1000 random 8-letter words gave about 6500 nodes, about 1.56 MB with dicts and 2.04 MB with 26-slot lists. Random words share little, and the dict trie was still smaller. For dense tries on a small alphabet the list can win on speed.

**Complexity:** insert, search and startsWith are O(L) time each, where L is the length of the word or prefix (at most 20). Space O(total letters in the distinct words) nodes in the worst case, times the node size: dict nodes are proportional to the children present, list nodes are 26 slots each. Total time for q operations: O(q * L).

**Dry run:** first example. insert 'apple' creates a -> p -> p -> l -> e, `e.is_end = True`. search 'apple': walk 5 nodes, flag True, so True. search 'app': node exists but flag False, so False. startsWith 'app': reaches the node, True. insert 'app': flag on the third node set. search 'app': True. Output `[None, True, False, True, None, True]` (`null` is Python None). The program also prints the node chain after inserting apple and app: 'app' and 'apple' end flags are True, 'a', 'ap', 'appl' are False.

**Code:**
```python
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
```

**Output (my run):**
```
[None, True, False, True, None, True]
[False]
[None, None, False, True, False]
  node 'a'      end=False
  node 'ap'     end=False
  node 'app'    end=True
  node 'appl'   end=False
  node 'apple'  end=True
random cross-check ok: 2000 cases
nodes: 6531  dict-trie bytes: 1563528  array-trie bytes: 2037672
edge asserts ok
```

**Edge cases:**
- search for a proper prefix of an inserted word is False; startsWith is True.
- A prefix longer than any word (startsWith 'top' after 'to') is False.
- Duplicate inserts change nothing.
- Length 20 words, and the full alphabet `abcdefghijklmnopqrstuvwxyz` as one word.
- Never share a mutable default child dict between nodes (see mistakes).

**Follow-ups:**
- Delete a word? Clear the flag, then walk back and remove nodes that have no children and no flag.
- Autocomplete with counts or top-k? Store a count (or a cached top-k list) per node; writes cost more, reads become O(L).
- Why not a hash set of all prefixes? That is O(L^2) space per word and does not help with enumeration.

**Common mistakes:**
- Returning True from search when only the node exists (forgetting `is_end`): then 'app' would be found after inserting 'apple'.
- Making startsWith check the flag.
- `children = {}` as a class-level or default-argument attribute, so all nodes share one dict.
- Stating the cost as O(N) or O(number of words); it is O(L).
