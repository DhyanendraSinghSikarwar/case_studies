### Q41 ⭐ 🟢 A trie as a tree, at concept level. A trie is a rooted tree with one edge per character; the full design and its variations belong to Part 12, and Part 3 Q36 compares it with a sorted list for prefix queries. Build one over a list of lowercase words (insert each word letter by letter, a node holds a dict of children and a count of words passing through it) and return the tuple (counts, nodes): counts[i] is how many of the words start with queries[i] (the empty prefix is not asked), and nodes is the number of trie nodes excluding the root. 1 <= words <= 10^4, total length <= 10^5. Explain the cost of insert and of a prefix query in terms of the word length L (not the number of words) and the memory cost compared with a set of words. Example: words=['apple', 'app', 'apricot', 'bat'], queries=['app', 'ap', 'b', 'c'] -> ([2, 3, 1, 0], 13); words=['a', 'a'], queries=['a', 'aa'] -> ([2, 0], 1).
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** A trie is a rooted tree where each edge is one character and each node is one prefix. This question is concept level: the tree idea and the cost model. The full design (delete, wildcard search, compressed tries, autocomplete ranking) belongs to Part 12. Part 3 Q36 compares a trie with a sorted list for prefix queries.

**Say this first (1 line):** "I walk the word one letter at a time, creating child nodes as needed and bumping a counter on every node I pass, so a prefix query is just a walk of len(prefix) steps and the counter is the answer."

**Brute force:** For each query, scan all words and test `startswith`. That is O(Q x total letters) time. Counting the nodes is the number of distinct non-empty prefixes, which a set comprehension gives. Both are in the code as the checker.

**Optimal:**
- Node = a dict of children plus `count` = how many inserted words pass through this node.
- Insert word w: start at the root, for each letter get or create the child, move down, add 1 to its count. A new child adds 1 to the node total.
- Query q: walk down; if a letter is missing the answer is 0, else it is the count where the walk ends.
- Why the counter works: every word that starts with q passed through exactly that node once. A duplicate word counts twice, which matches the example `['a','a']`.
- Invariant: after inserting k words, the node for prefix p holds the number of those words that start with p.

**Complexity:**
- Insert O(L) dict operations, L = the word length. Query O(len(q)). Neither depends on how many words are stored. That is the whole point of the trie.
- Build time O(total letters), about 10^5 steps for the stated limits.
- Memory: at most one node per inserted letter, so nodes <= total letters (asserted in the code). Words that share prefixes share nodes.
- Honest memory comparison: a node here is a Python object plus a dict, much heavier than one letter of a string in a set. A trie wins on prefix queries, not on bytes. For words with no shared prefixes it is strictly worse on memory than a set of strings.
- A set answers "is this exact word present" in O(L) too (hashing a string reads it all), but cannot answer a prefix question without a scan.

**Dry run:** words = apple, app, apricot, bat.
| inserted | new nodes | counts on the path |
|---|---|---|
| apple | a, ap, app, appl, apple (5) | each 1 |
| app | none | a=2, ap=2, app=2 |
| apricot | apr, apri, apric, aprico, apricot (5) | a=3, ap=3, apr..=1 |
| bat | b, ba, bat (3) | each 1 |
Total nodes 13. Queries: app -> 2, ap -> 3, b -> 1, c -> 0 (no child of the root).

**Code:**
```python
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
```

**Output (my run):**
```text
examples ok: ([2, 3, 1, 0], 13) ([2, 0], 1)
600 random cases ok; nodes always between longest word and total letters
edge asserts ok
lookups for a 10-letter query with 10 words: 10 ; with 10000 words: 10
10000 words, 100000 letters in total -> trie nodes = 62780 (shared prefixes are stored once)
a set of the strings stores 100000 letters and still scans all 10000 words for a prefix query
```

**Edge cases:**
- Query longer than any word: the walk falls off, answer 0.
- Query equal to a whole word counts that word (and every longer word with the prefix).
- Duplicates: counters go up, the node total does not.
- A word that is a prefix of another (`a`, `ab`, `abc`): a chain, no new node for the shorter word.
- Counting the root as a node: the question says no, so start `nodes` at 0.

**Follow-ups:**
- How do you tell which words end at a node? Add an `end` counter, separate from the pass-through `count`. Details in Part 12.
- Can the dict per node be an array of 26? Yes, faster lookups but 26 slots per node even when empty, so more memory on sparse data.
- Delete a word? Walk down decrementing counts and prune nodes whose count reaches 0. Part 12.

**Common mistakes:**
- Saying the cost is O(number of words). It is O(L).
- Counting only words that END at the queried node, which gives 1 instead of 3 for `ap` in the example.
- Storing the node count after inserting duplicates without checking whether the child already existed.
- Claiming a trie always saves memory.

---

### Q42 ⭐ 🟡 Tree identity versus value equality: validate that a pointer structure is really a tree. In tests, trees are often built by hand and can accidentally contain a cycle or a shared node (aliasing), which makes traversals loop forever or visit a node twice. Nodes are given as a list `nodes` of triples [val, left_index, right_index] with -1 for none; the root is index 0, and indices unreachable from the root are ignored. Return 'cycle' if some node is its own descendant, else 'shared' if some node is reachable by two different paths (two parents, or the same child on both sides), else 'tree'. Solve it with a visited set of `id(node)` (the nodes are objects; the default hash and `==` are by identity) in O(n) time with an iterative walk that has a step cap. Also explain why `a == b` is False for two separately built equal trees and which function gives value equality. Example: nodes=[[1, 1, 2], [2, -1, -1], [3, -1, -1]] -> 'tree'; nodes=[[1, 1, 2], [2, 3, -1], [3, 3, -1], [4, -1, -1]] -> 'shared'; nodes=[[1, 1, -1], [2, 0, -1]] -> 'cycle'; nodes=[[1, 1, 1], [2, -1, -1]] -> 'shared'; nodes=[[1, -1, -1], [9, 1, 0]] -> 'tree'.
**Asked at:** Python recursion-limit explainers (techinterview.org depth-of-a-tree page, a OneUptime guide, DataCamp DFS tutorial; snippets only, not opened: default limit 1000, raising it risks a crash, explicit stack preferred) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Graph hygiene on a tree. A tree is a connected structure where every node has one path from the root. Hand-built tests can break that with a back edge (cycle) or a node reachable twice (aliasing). A visited set keyed by `id(node)` catches both in one iterative walk.

**Say this first (1 line):** "I walk from the root with an explicit stack, track each node by `id` as on-the-path or finished, and if I meet an on-the-path node it is a cycle, if I meet a finished one it is shared, and a step cap makes sure the walk itself can never hang."

**Brute force:** Count walks from the root: repeat "follow every child pointer" for n + 1 steps while tallying how many distinct walks end at each node. If walks are still alive after n steps some node repeats, so it is a cycle. Otherwise any node with 2 or more walks is shared. It needs no visited set at all, which makes it a genuinely independent checker. It is O(n^2) or worse and is only the test oracle.

**Optimal:**
- Build the node objects first. Then walk with a stack of (node, phase). Phase 0 = arrive, phase 1 = leave.
- State per `id(node)`: 1 = on the current root-to-here path, 2 = finished.
- Arriving at a node already in state 1: it is its own descendant, return 'cycle' at once.
- Arriving at a node already in state 2: a second route to it, so remember `shared = True` and do not walk into it again (this keeps the walk linear).
- At the end return 'shared' if flagged, else 'tree'. Cycle wins over shared because the check returns immediately.
- Why a plain visited set is not enough: it tells you "seen twice" but not whether the second sight is a back edge (cycle) or a cross edge (shared). The on-path colour makes the difference.
- Step cap: each node is expanded at most once, so the loop runs at most 2n + (number of pointers) steps. The code asserts a cap of 4n + 8 and it held on every table tested. Indices unreachable from the root are never touched, which is why the last example is a 'tree' even though node 1 points back at node 0.
- Equality: `==` on a class with no `__eq__` falls back to identity. Two separately built equal trees are two sets of objects, so `a == b` is False. Value equality is a function, `same_tree(p, q)`, that compares values and shape pairwise.

**Complexity:** Time O(n) and space O(n) for the object list, state dict and stack. Each node is expanded once, each pointer is looked at once.

**Dry run:** nodes = [[1,1,2],[2,3,-1],[3,3,-1],[4,-1,-1]]. Root 0 has children 1 and 2. Node 1 has child 3. Node 2 also has child 3.
| step | action | state |
|---|---|---|
| visit 0 | on path | {0:1} |
| visit 1 | on path | {0:1, 1:1} |
| visit 3 | on path, leaf, leave | 3 finished |
| leave 1 | | 1 finished |
| visit 2 | on path | 2 on path |
| node 2's child 3 | already finished (state 2) | shared = True, skip |
| end | | return 'shared' |

**Code:**
```python
import itertools

class TreeNode:
    __slots__ = ('val', 'left', 'right')          # no __eq__ defined: == and hash are by identity
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def classify(nodes):
    objs = [TreeNode(v) for v, l, r in nodes]
    for o, (v, l, r) in zip(objs, nodes):
        o.left = objs[l] if l != -1 else None
        o.right = objs[r] if r != -1 else None
    state, shared = {}, False                      # id(node) -> 1 on the current path, 2 finished
    st, steps, cap = [(objs[0], 0)], 0, 4 * len(objs) + 8
    while st:
        steps += 1
        assert steps <= cap, 'step cap hit: the walk must never loop'
        n, phase = st.pop()
        if phase == 1: state[id(n)] = 2; continue  # all descendants done: leave the path
        if id(n) in state:
            if state[id(n)] == 1: return 'cycle'   # reached a node that is still on the path
            shared = True; continue                # reached a finished node by a second route
        state[id(n)] = 1
        st.append((n, 1))
        for c in (n.right, n.left):
            if c is not None: st.append((c, 0))
    return 'shared' if shared else 'tree'

# ---- brute force: count walks from the root, never touching the visited set
def brute(nodes):
    n = len(nodes)
    walks = {0: 1}; level = {0: 1}                 # level[i] = number of walks of the current length ending at i
    reach = {0}
    for step in range(n + 1):                      # a walk longer than n-1 edges must repeat a node
        nxt = {}
        for i, c in level.items():
            for ch in nodes[i][1:]:
                if ch != -1: nxt[ch] = nxt.get(ch, 0) + c
        if not nxt: break
        for i, c in nxt.items(): walks[i] = walks.get(i, 0) + c; reach.add(i)
        level = nxt
    else:
        return 'cycle'                             # still walking after n+1 steps
    return 'tree' if all(c == 1 for c in walks.values()) else 'shared'

# ---- examples from the question
ex = [([[1, 1, 2], [2, -1, -1], [3, -1, -1]], 'tree'),
      ([[1, 1, 2], [2, 3, -1], [3, 3, -1], [4, -1, -1]], 'shared'),
      ([[1, 1, -1], [2, 0, -1]], 'cycle'),
      ([[1, 1, 1], [2, -1, -1]], 'shared'),
      ([[1, -1, -1], [9, 1, 0]], 'tree')]
for nodes, want in ex:
    assert classify(nodes) == want == brute(nodes), nodes
print('examples ok:', [w for _, w in ex])

# ---- exhaustive: every pointer table with n = 1..4 nodes (children in -1..n-1)
total, seen = 0, {'tree': 0, 'shared': 0, 'cycle': 0}
for n in range(1, 5):
    for ch in itertools.product(range(-1, n), repeat=2 * n):
        nodes = [[i, ch[2 * i], ch[2 * i + 1]] for i in range(n)]
        r = classify(nodes)
        assert r == brute(nodes), nodes
        seen[r] += 1; total += 1
print('exhaustive tables checked:', total, seen)

# ---- value equality vs identity
a = TreeNode(1, TreeNode(2), TreeNode(3)); b = TreeNode(1, TreeNode(2), TreeNode(3))
def same_tree(p, q):
    st = [(p, q)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st += [(x.left, y.left), (x.right, y.right)]
    return True
print('a == b:', a == b, '| same_tree(a, b):', same_tree(a, b), '| id sets disjoint:', not ({id(a), id(a.left), id(a.right)} & {id(b), id(b.left), id(b.right)}))
assert (a == b) is False and same_tree(a, b) and a == a

# ---- a hand-built shared node and what a naive recursive walk does
x = TreeNode(5); root = TreeNode(1, x, x)          # the same object on both sides
def count_visits(r):
    st, k = [r], 0
    while st:
        n = st.pop(); k += 1
        st += [c for c in (n.left, n.right) if c is not None]
    return k
print('visits for a 1-root tree with the same child twice:', count_visits(root), '(3 visits, only 2 distinct nodes)')
print('table with a back edge, capped visited-set walk ->', classify([[1, 1, 1], [5, 0, -1]]), '(it stops; a plain recursive or stack walk on cyclic nodes would loop forever)')
```

**Output (my run):**
```text
examples ok: ['tree', 'shared', 'cycle', 'shared', 'tree']
exhaustive tables checked: 394806 {'tree': 20551, 'shared': 4258, 'cycle': 369997}
a == b: False | same_tree(a, b): True | id sets disjoint: True
visits for a 1-root tree with the same child twice: 3 (3 visits, only 2 distinct nodes)
table with a back edge, capped visited-set walk -> cycle (it stops; a plain recursive or stack walk on cyclic nodes would loop forever)
```

**Edge cases:**
- Root that points to itself: cycle on the first step.
- Same child on both sides (`[1,1,1]`): shared, not a cycle.
- Cycle among unreachable nodes: ignored, answer 'tree'.
- A cycle AND a shared node: reported as 'cycle'.
- Single node with two -1 pointers: 'tree'.
- A recursive walk on a cyclic structure never returns or hits the recursion limit; the iterative walk with a cap ends.

**Follow-ups:**
- Why not rely on Python's recursion limit to catch a cycle? It also trips on a legal deep tree, so it cannot tell the two apart.
- Shared node in a DAG test but only values matter? Then it is not a tree anyway: identity, not value, defines sharing.
- Floyd's cycle detection? Works for a single next pointer (Part 6). A tree has two pointers per node, so the colour walk is simpler.

**Common mistakes:**
- Using `val` as the visited key: equal values in different nodes would look shared.
- Reporting 'shared' for what is really a cycle, because the first repeat was seen before the on-path check.
- Walking into an already finished node again, which can blow up to exponential time on a DAG.
- Expecting `a == b` to compare values when the class defines no `__eq__`.

---

### Q43 ⭐ 🟡 Maximum width of a binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The width of a level is the number of positions from its leftmost non-null node to its rightmost non-null node inclusive, counting the missing positions between them as if the tree were perfect (give a node at index i the children 2i and 2i + 1). Return the largest width over all levels (0 for an empty tree, n <= 3000). Use BFS with (node, index) and subtract the level's first index before doubling, so indexes stay small on a deep skewed tree (Python integers do not overflow, but their size and the cost of arithmetic grow with depth). Say why counting only non-null nodes per level is a different, easier problem. Example: root=[1, 3, 2, 5, 3, null, 9] -> 4; root=[1, 3, 2, 5] -> 2; root=[1, 3, null, 5, 3] -> 2; root=[1, 2, 3, 4, null, null, 5] -> 4; root=[1] -> 1; root=[] -> 0.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)
**Pattern:** Level-order BFS with positions. Give every node the index it would have in a perfect tree (root 0, children 2i and 2i + 1). The width of a level is last index minus first index plus 1.

**Say this first (1 line):** "BFS by level carrying (node, index); width is last index minus first index plus 1; and before I double indexes I subtract the level's first index so they stay tiny even on a deep skewed tree."

**Brute force:** Compute raw heap positions for every node (root 1, children 2i, 2i + 1) in a recursive pass, group by depth, take max minus min plus 1 per depth. It is correct but the integers grow by one bit per level. It is the checker in the code (on tuples).

**Optimal:**
- Keep one list per level of (node, index).
- First index `base` and last index give the width of the level.
- When building the next level compute `i -= base` first, then children get `2 * i` and `2 * i + 1`.
- Why subtracting is safe: widths are differences, and a difference is the same if every index in a level is shifted by the same amount. Doubling then keeps the shift consistent (the next level is shifted by 2 x base, and the next iteration subtracts its own base).
- Invariant: inside a level the indexes are relative, the leftmost one is always 0.
- Counting non-null nodes per level is a different, easier problem: the answer is just the biggest `len(level)`. It ignores the gaps. The example `[1,2,3,4,null,null,5]` has width 4 but at most 2 nodes per level.

**Complexity:** O(n) time, each node enters one level list once. Space O(w) for the widest level (up to n / 2). Arithmetic is on small integers with the re-basing. Without it, Python integers do not overflow but a skewed 3000-deep tree has indexes about 3000 bits long, so each operation costs more than O(1) (see the output).

**Dry run:** [1,3,2,5,3,null,9].
| level | (node:index) | width |
|---|---|---|
| 0 | 1:0 | 1 |
| 1 | 3:0, 2:1 | 2 |
| 2 | 5:0, 3:1, 9:3 (2's right child is 2*1+1 = 3) | 3 - 0 + 1 = 4 |
Answer 4.

**Code:**
```python
import random
random.seed(43)

def max_width(root):
    if root is None: return 0
    best, level = 0, [(root, 0)]
    while level:
        base = level[0][1]
        best = max(best, level[-1][1] - base + 1)       # leftmost to rightmost, gaps included
        nxt = []
        for node, i in level:
            i -= base                                   # re-base BEFORE doubling: indexes stay small
            if node.left: nxt.append((node.left, 2 * i))
            if node.right: nxt.append((node.right, 2 * i + 1))
        level = nxt
    return best

def max_width_no_rebase(root):                          # same idea, raw heap indexes (kept to show the cost)
    if root is None: return 0, 0
    best, big, level = 0, 0, [(root, 1)]
    while level:
        best = max(best, level[-1][1] - level[0][1] + 1)
        big = max(big, level[-1][1].bit_length())
        level = [(c, 2 * i + k) for n, i in level for k, c in ((0, n.left), (1, n.right)) if c]
    return best, big

def max_count(root):                                    # the easier, different question: most nodes on one level
    if root is None: return 0
    best, level = 0, [root]
    while level:
        best = max(best, len(level)); level = [c for n in level for c in (n.left, n.right) if c]
    return best

# ---- brute force on nested tuples: absolute heap positions, grouped by depth
def brute(t):
    pos = {}
    def go(t, d, idx):
        if t is None: return
        pos.setdefault(d, []).append(idx); go(t[1], d + 1, 2 * idx); go(t[2], d + 1, 2 * idx + 1)
    go(t, 0, 1)
    return max((max(v) - min(v) + 1 for v in pos.values()), default=0)

# ---- helpers
class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
def build_tree(arr):
    from collections import deque
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root
def from_tup(t): return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def shapes(n, _c={0: [None]}):
    if n not in _c: _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

# ---- examples from the question
N = None
cases = [([1, 3, 2, 5, 3, N, 9], 4), ([1, 3, 2, 5], 2), ([1, 3, N, 5, 3], 2), ([1, 2, 3, 4, N, N, 5], 4), ([1], 1), ([], 0)]
for arr, want in cases:
    assert max_width(build_tree(arr)) == want, arr
print('examples ok:', [w for _, w in cases])

# ---- exhaustive over every shape with 0..8 nodes
count = 0
for n in range(9):
    for sh in shapes(n):
        def addv(s):
            return None if s is None else (0, addv(s[0]), addv(s[1]))
        tv = addv(sh); r = from_tup(tv)
        assert max_width(r) == brute(tv) == max_width_no_rebase(r)[0], tv
        count += 1
print('shapes checked exhaustively (0..8 nodes):', count)

# ---- seeded random trees up to 60 nodes, level-order arrays with holes
for _ in range(300):
    n = random.randint(1, 60); root = TreeNode(0); nodes = [root]
    for v in range(1, n):
        p = random.choice(nodes)
        side = random.random() < .5
        if getattr(p, 'left' if side else 'right') is None:
            c = TreeNode(v); setattr(p, 'left' if side else 'right', c); nodes.append(c)
    def tupr(x): return None if x is None else (x.val, tupr(x.left), tupr(x.right))
    assert max_width(root) == brute(tupr(root))
print('300 random trees ok')

# ---- width is NOT the same as the largest level
wide = build_tree([1, 2, 3, 4, N, N, 5])
print('[1,2,3,4,null,null,5]: width =', max_width(wide), ' largest level count =', max_count(wide))
assert (max_width(wide), max_count(wide)) == (4, 2)

# ---- deep skewed trees: a zig-zag chain of 3000 nodes (left, right, left, ...)
root = TreeNode(0); cur = root
for i in range(1, 3000):
    nxt = TreeNode(i)
    if i % 2: cur.left = nxt
    else: cur.right = nxt
    cur = nxt
w, bits = max_width_no_rebase(root)
print('zig-zag chain, 3000 nodes: width =', max_width(root), '; without re-basing the biggest index has', bits, 'bits')
assert max_width(root) == 1 and bits == 3000   # raw heap index doubles at every level
# right-only chain: raw index grows like 2^depth, re-based index stays at 0 or 1
chain = TreeNode(0); cur = chain
for i in range(1, 3000):
    cur.right = TreeNode(i); cur = cur.right
print('right chain, 3000 nodes: width =', max_width(chain), '; raw-index bits =', max_width_no_rebase(chain)[1])
assert max_width(chain) == 1
```

**Output (my run):**
```text
examples ok: [4, 2, 2, 4, 1, 0]
shapes checked exhaustively (0..8 nodes): 2056
300 random trees ok
[1,2,3,4,null,null,5]: width = 4  largest level count = 2
zig-zag chain, 3000 nodes: width = 1 ; without re-basing the biggest index has 3000 bits
right chain, 3000 nodes: width = 1 ; raw-index bits = 3000
```

**Edge cases:**
- Empty tree: 0. Single node: 1.
- A level with one node: width 1, however far right it sits.
- Skewed chain: width 1, the raw index is huge, the re-based index stays 0 or 1.
- The gap between the leftmost and rightmost nodes counts only if those two nodes exist, so missing outer slots do not count.

**Follow-ups:**
- DFS instead of BFS? Record the first index seen at each depth in a dict and compute `index - first[depth] + 1`. Same idea, indexes still need care.
- Does the width ever exceed n? Yes for sparse trees: a long left spine and a long right spine can give widths near 2^depth in the raw definition. The re-based BFS still reports it correctly in O(n).
- Use a deque? Only if you pop from the front of a single queue; per-level lists avoid that.

**Common mistakes:**
- Using `len(level)` instead of index difference.
- Forgetting the +1.
- Not re-basing, then paying for huge integers on deep trees (the reason this question is asked).
- Mixing re-based and raw indexes inside one level, which makes the difference meaningless.

---

### Q44 ⭐ 🟡 Build a BST from its preorder traversal. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given the preorder of a BST with distinct values (1 <= n <= 3000), rebuild the BST and return it (the tree is unique because the BST rule decides where each value goes). Give the O(n log n)-or-worse insert-one-by-one solution, then the O(n) solution with an upper bound and a moving index (a value larger than the current bound ends the subtree), and say why the inorder (just the sorted values) is not needed. Example: preorder=[8, 5, 1, 7, 10, 12] -> [8, 5, 10, 1, 7, null, 12]; preorder=[1] -> [1]; preorder=[3, 1, 2] -> [3, 1, null, null, 2]; preorder=[1, 2, 3] -> [1, null, 2, null, 3].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)
**Pattern:** Recursive construction with a bound (or a stack). In a BST preorder each subtree is a contiguous block, and every value in the left block is smaller than the root. A node's value is the upper bound of its left subtree; the bound inherited from an ancestor limits its right subtree.

**Say this first (1 line):** "Preorder gives root first; I build the left subtree while values stay below the root, and the first value that breaks the upper bound belongs to an ancestor's right side, so one moving index and a bound builds the tree in O(n)."

**Brute force:** Insert the preorder values one by one into an empty BST. Because preorder lists each parent before its children, inserting in that order rebuilds the same tree. Cost O(n x height), so O(n log n) on balanced trees and O(n^2) on a skewed one. The insert is iterative in the code.

**Optimal:**
- `go(bound)`: if the next value is missing or larger than `bound`, return None (it belongs further up).
- Else create a node with the next value, advance the index.
- Its left child is `go(node.val)` (values must be smaller than this node).
- Its right child is `go(bound)` (smaller than whatever limit this node inherited).
- Start with bound infinity.
- Why inorder is not needed: the inorder of a BST is the sorted values, so it adds no information. The BST rule supplies the "left or right" decision that other traversal pairs need an inorder for.
- Unique tree: different BSTs never have the same preorder (tested exhaustively below), so the answer is the only one possible.
- Precondition: the input must be a valid BST preorder. The code does not check it. `[1,2,0]` builds a garbage tree (shown in the output). To validate, add a lower bound too.
- Iterative alternative: keep a stack of the current right spine. For a new value, pop while the stack top is smaller; the last popped node gets the new value as its right child; if nothing popped, it is the left child of the top. Also O(n) and has no recursion limit problem.

**Complexity:** Optimal O(n) time: each value is placed once, the index never moves back. Space O(h) for the recursion (O(n) on a skewed tree) or O(h) for the stack in the iterative version, plus the output tree. Insert-one-by-one: O(n h) time, up to O(n^2).

**Dry run:** [8,5,1,7,10,12], bound = inf.
| call | next value | action |
|---|---|---|
| go(inf) | 8 | node 8; left = go(8) |
| go(8) | 5 | node 5; left = go(5) |
| go(5) | 1 | node 1; left go(1): 7 > 1 returns None; right go(5): 7 > 5 returns None |
| back in 5: right = go(8) | 7 | node 7; children go(7), go(8): 10 > 8 -> None |
| back in 8: right = go(inf) | 10 | node 10; left go(10): 12 > 10 None; right go(inf): 12 |
Result [8,5,10,1,7,null,12].

**Code:**
```python
from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
import itertools

# ---- brute force: insert values one by one (iterative; O(n * height), O(n^2) on a skewed tree)
def build_insert(pre):
    root = None
    for v in pre:
        nd = TreeNode(v)
        if root is None: root = nd; continue
        cur = root
        while True:
            side = 'left' if v < cur.val else 'right'
            nxt = getattr(cur, side)
            if nxt is None: setattr(cur, side, nd); break
            cur = nxt
    return root

# ---- optimal: upper bound + moving index, O(n). Recursive form (depth = tree height).
def build_bound(pre):
    i = 0
    def go(bound):
        nonlocal i
        if i == len(pre) or pre[i] > bound: return None      # next value belongs to an ancestor's right side
        nd = TreeNode(pre[i]); i += 1
        nd.left = go(nd.val)                                  # left subtree: values below nd.val
        nd.right = go(bound)                                  # right subtree: values below the inherited bound
        return nd
    return go(float('inf'))

# ---- same O(n), explicit stack: safe for a 3000-deep skewed input
def build_stack(pre):
    if not pre: return None
    root = TreeNode(pre[0]); st = [root]
    for v in pre[1:]:
        nd = TreeNode(v); last = None
        while st and st[-1].val < v: last = st.pop()          # v is bigger: climb to the parent whose right slot is free
        if last: last.right = nd
        else: st[-1].left = nd
        st.append(nd)
    return root

def preorder(root):
    out, st = [], [root] if root else []
    while st:
        n = st.pop(); out.append(n.val)
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def inorder(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

# ---- examples from the question
N = None
ex = [([8, 5, 1, 7, 10, 12], [8, 5, 10, 1, 7, N, 12]), ([1], [1]), ([3, 1, 2], [3, 1, N, N, 2]), ([1, 2, 3], [1, N, 2, N, 3])]
for pre, want in ex:
    for f in (build_insert, build_bound, build_stack):
        assert to_arr(f(pre)) == want, (f.__name__, pre)
print('examples ok:', [to_arr(build_bound(p)) for p, _ in ex])

# ---- exhaustive: every BST shape up to 8 nodes; the three builders agree and recover the tree
seen, count = set(), 0
for n in range(1, 9):
    for sh in shapes(n):
        t = label(sh, 'in'); pre = preorder(from_tup(t))
        assert tup(build_insert(pre)) == tup(build_bound(pre)) == tup(build_stack(pre)) == t
        assert tuple(pre) not in seen                           # different trees never share a preorder
        seen.add(tuple(pre)); count += 1
print('BST shapes 1..8 nodes: all three builders recover the tree;', count, 'distinct preorders (preorder is injective)')

# ---- exhaustive count: which permutations of 0..n-1 are a valid BST preorder? exactly Catalan(n) of them
for n in range(1, 8):
    ok = 0
    for p in itertools.permutations(range(n)):
        r = build_bound(list(p))
        if preorder(r) == list(p) and inorder(r) == sorted(p): ok += 1   # a real BST whose preorder is p
    assert ok == len(shapes(n)), (n, ok)
print('valid preorders among all permutations of n<=7 = number of shapes (1,2,5,14,42,132,429)')

# ---- precondition: the bound builder does NOT validate its input. [1, 2, 0] is not a BST preorder:
bad = build_bound([1, 2, 0])
print('invalid preorder [1, 2, 0] -> built a tree whose inorder is', inorder(bad), '(not sorted: garbage in, garbage out)')
assert inorder(bad) != sorted(inorder(bad))

# ---- seeded random distinct values, including negatives
random.seed(44)
for _ in range(400):
    vals = random.sample(range(-50, 50), random.randint(1, 12))
    r1 = build_insert(vals); pre = preorder(r1)
    assert tup(build_bound(pre)) == tup(build_stack(pre)) == tup(r1)
print('400 random cases ok')

# ---- inorder is not needed: sorted(pre) is the inorder, so it adds no information
sh = shapes(6)[17]; t = label(sh, 'in'); pre = preorder(from_tup(t))
assert sorted(pre) == list(range(6))
print('inorder of a BST is sorted(pre):', sorted(pre))

# ---- worst case: 3000 ascending values = right-skewed tree of height 3000
pre = list(range(1, 3001))
r = build_stack(pre); assert preorder(r) == pre
try: build_bound(pre); print('recursive built it?')
except RecursionError: print('build_bound on 3000 ascending values: RecursionError (default limit 1000); build_stack is fine')
```

**Output (my run):**
```text
examples ok: [[8, 5, 10, 1, 7, None, 12], [1], [3, 1, None, None, 2], [1, None, 2, None, 3]]
BST shapes 1..8 nodes: all three builders recover the tree; 2055 distinct preorders (preorder is injective)
valid preorders among all permutations of n<=7 = number of shapes (1,2,5,14,42,132,429)
invalid preorder [1, 2, 0] -> built a tree whose inorder is [1, 0, 2] (not sorted: garbage in, garbage out)
400 random cases ok
inorder of a BST is sorted(pre): [0, 1, 2, 3, 4, 5]
build_bound on 3000 ascending values: RecursionError (default limit 1000); build_stack is fine
```

**Edge cases:**
- One value: single node.
- Ascending preorder `[1,2,3]`: a right chain. With n = 3000 the recursive version needs depth 3000, and the default limit 1000 raises RecursionError (shown). The stack version is the safe one for the stated limit.
- Descending preorder: a left chain, same depth problem.
- Invalid input: not detected unless you add a lower bound.

**Follow-ups:**
- Preorder of a general binary tree? Not unique; you need the inorder as well (an earlier Part 7 question).
- Postorder of a BST? Same idea from the right end of the array with the mirrored rule.
- Validate the preorder without building? Use the stack with a `lower` value: if a value is below `lower` it is invalid. O(n).

**Common mistakes:**
- Searching the array for the split point each time: that is O(n^2) in the worst case.
- Using the bound as a lower bound for the left child.
- Forgetting that the index must be shared across calls (a global, nonlocal or list cell).
- Trusting recursion at depth 3000.

---

### Q45 ⭐ 🟡 House Robber III, at concept level. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Each node holds money; you may take a set of nodes so that no two chosen nodes are parent and child. Return the largest total (0 for an empty tree, values >= 0, n <= 10^4). Each call returns a pair (best if this node is taken, best if it is not taken); the node taken adds its value to the 'not taken' results of its children, and a node not taken adds the better option of each child. Explain why a greedy 'take every other level' is wrong. The general tree-DP theory belongs to Part 10; here the point is the return-a-tuple pattern. Example: root=[3, 2, 3, null, 3, null, 1] -> 7; root=[3, 4, 5, 1, 3, null, 1] -> 9; root=[] -> 0; root=[2, 1, 3, null, 4] -> 7.
**Asked at:** Tree-DP pattern guides (techinterview.org tree-DP and DP-on-trees pages, AlgoMaster and Vultr House Robber III pages; snippets only, not opened: a (rob, skip) pair per subtree; camera states not covered / has camera / covered); full tree DP belongs to Part 10 | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)
**Pattern:** Tree DP at concept level: each subtree returns a small tuple, here (best if the root is taken, best if the root is not taken), and the parent combines the two children's tuples. Part 10 has the full tree-DP treatment.

**Say this first (1 line):** "Each call returns a pair: take this node, which forces both children to be skipped, or skip it, which lets each child choose its better option; the answer is the max of the root's pair."

**Brute force:** Try every subset of nodes, throw out any subset containing a parent and child together, keep the best sum. O(2^n x n). It is the oracle in the code for trees up to 7 nodes.

**Optimal:**
- `go(n)` returns `(take, skip)`. For a missing node it is `(0, 0)`.
- `take = n.val + left.skip + right.skip` (children cannot be chosen).
- `skip = max(left) + max(right)` (each child is free to be taken or skipped).
- Answer: `max(go(root))`.
- Why the pair is needed: the best for a subtree depends on whether its parent was taken. The pair stores both answers, so nobody recomputes. The naive recursion "take me plus my grandchildren, or skip me and use my children" without the pair calls the same subtrees over and over (the call counts in the output grow about 3.2x per level while the nodes only double).
- Why "take every other level" is wrong: it fixes the choice by depth, but the best set can mix levels along different branches. On `[2,1,3,null,4]` the best is 3 + 4 = 7 (nodes at depth 1 and 2), while the better of even or odd levels gives 6. The output counts how often the level-parity rule is wrong over every tree shape up to 7 nodes.
- Invariant: after `go(n)` returns, `take` and `skip` are the true optimum for the subtree rooted at n under the two possibilities.

**Complexity:** O(n) time, one call per node (plus one per missing child). O(h) stack space for the recursion, O(n) worst case for a skewed tree. Because n can be 10^4 and Python's default recursion limit is about 1000, a skewed input fails in the recursive form; the code has an iterative post-order version that is safe (see the output).

**Dry run:** [3,2,3,null,3,null,1].
| node | (take, skip) |
|---|---|
| leaf 3 (left's right) | (3, 0) |
| leaf 1 | (1, 0) |
| node 2 (right child is that leaf 3) | take = 2 + 0 + 0 = 2; skip = max(0,0) + max(3,0) = 3 -> (2, 3) |
| node 3 (right child is leaf 1) | take = 3 + 0 + 0 = 3; skip = 0 + 1 = 1 -> (3, 1) |
| root 3 | take = 3 + 3 + 1 = 7; skip = max(2,3) + max(3,1) = 6 -> (7, 6) |
Answer 7.

**Code:**
```python
from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
import itertools

# ---- optimal: each subtree returns (best if its root is taken, best if its root is not taken)
def rob(root):
    def go(n):
        if n is None: return (0, 0)
        a, b = go(n.left), go(n.right)
        return (n.val + a[1] + b[1], max(a) + max(b))
    return max(go(root))

# ---- same thing with an explicit post-order stack: safe for n = 10^4 skewed
def rob_iter(root):
    if root is None: return 0
    res, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if s == 0: st += [(n, 1)] + [(c, 0) for c in (n.left, n.right) if c]
        else:
            a, b = res.pop(id(n.left), (0, 0)), res.pop(id(n.right), (0, 0))
            res[id(n)] = (n.val + a[1] + b[1], max(a) + max(b))
    return max(res[id(root)])

# ---- brute force: try every subset of nodes with no parent-child pair
def brute(root):
    nodes, par = [], {}
    st = [root] if root else []
    while st:
        n = st.pop(); nodes.append(n)
        for c in (n.left, n.right):
            if c: par[id(c)] = n; st.append(c)
    best = 0
    for mask in range(1 << len(nodes)):
        chosen = {id(nodes[i]) for i in range(len(nodes)) if mask >> i & 1}
        if any(par.get(i) is not None and id(par[i]) in chosen for i in chosen): continue
        best = max(best, sum(nodes[i].val for i in range(len(nodes)) if mask >> i & 1))
    return best

# ---- the tempting but wrong greedy: take the better of "all even levels" and "all odd levels"
def level_parity(root):
    if root is None: return 0
    sums, level = [0, 0], [root]; d = 0
    while level:
        sums[d % 2] += sum(n.val for n in level); level = [c for n in level for c in (n.left, n.right) if c]; d += 1
    return max(sums)

def naive_run(root):                                  # the real recursion, counting its calls
    calls = [0]
    def go(n):
        calls[0] += 1
        if n is None: return 0
        take = n.val
        for c in (n.left, n.right):
            if c: take += go(c.left) + go(c.right)
        return max(take, go(n.left) + go(n.right))
    return go(root), calls[0]

# ---- examples from the question
N = None
ex = [([3, 2, 3, N, 3, N, 1], 7), ([3, 4, 5, 1, 3, N, 1], 9), ([], 0), ([2, 1, 3, N, 4], 7)]
for arr, want in ex:
    r = build_tree(arr)
    assert rob(r) == rob_iter(r) == brute(r) == want, arr
print('examples ok:', [w for _, w in ex])

# ---- exhaustive over every shape up to 7 nodes, with seeded random non-negative values
random.seed(45)
count = fails = 0
for n in range(8):
    for sh in shapes(n):
        for _ in range(3):
            def addv(s): return None if s is None else (random.randint(0, 9), addv(s[0]), addv(s[1]))
            r = from_tup(addv(sh))
            b = brute(r)
            assert rob(r) == rob_iter(r) == b
            if level_parity(r) != b: fails += 1
            count += 1
print('trees checked:', count, '| the level-parity greedy was wrong on', fails, 'of them')
assert level_parity(build_tree([2, 1, 3, N, 4])) == 6 and rob(build_tree([2, 1, 3, N, 4])) == 7
print('counter-example [2,1,3,null,4]: parity greedy =', level_parity(build_tree([2, 1, 3, N, 4])), ', true answer = 7 (take 3 and 4)')

# ---- zero values and single node
assert rob(build_tree([0, 0, 0])) == 0 and rob(build_tree([5])) == 5

def perfect(h): return from_tup(label_perfect(h))
def label_perfect(h): return None if h < 0 else (1, label_perfect(h - 1), label_perfect(h - 1))
for h in range(0, 8):
    v, calls = naive_run(perfect(h)); assert v == rob(perfect(h))
print('naive calls, perfect tree heights 0..7 (None children counted):', [naive_run(perfect(h))[1] for h in range(8)])
# ---- cost: pair version visits each node once; the naive 'grandchildren' recursion without memo blows up
print('nodes in those trees:', [2 ** (h + 1) - 1 for h in range(8)], '(the pair version makes one call per node plus one per missing child)')

# ---- deep input: skewed chain of 10^4 nodes
root = TreeNode(1); cur = root
for i in range(2, 10001):
    cur.left = TreeNode(1); cur = cur.left
print('chain of 10000 nodes, all values 1: iterative answer =', rob_iter(root))
assert rob_iter(root) == 5000
try: rob(root); print('recursive version survived')
except RecursionError: print('recursive version: RecursionError at depth 10000 (default limit 1000)')
```

**Output (my run):**
```text
examples ok: [7, 9, 0, 7]
trees checked: 1878 | the level-parity greedy was wrong on 640 of them
counter-example [2,1,3,null,4]: parity greedy = 6 , true answer = 7 (take 3 and 4)
naive calls, perfect tree heights 0..7 (None children counted): [3, 11, 35, 115, 371, 1203, 3891, 12595]
nodes in those trees: [1, 3, 7, 15, 31, 63, 127, 255] (the pair version makes one call per node plus one per missing child)
chain of 10000 nodes, all values 1: iterative answer = 5000
recursive version: RecursionError at depth 10000 (default limit 1000)
```

**Edge cases:**
- Empty tree: 0. Single node: its value.
- Values are 0 or more, so taking a node is never harmful on its own; the conflict is only with neighbours.
- Equal values: both options tie, any is fine.
- Skewed chain of 10^4: use the iterative version.

**Follow-ups:**
- Return the chosen nodes too? Carry the sets (or backpointers) with each pair.
- Negative values? The `(0, 0)` base and `max` already handle it if "choose nothing" is allowed; check the problem statement.
- Linear House Robber? A path is the same recurrence with one child (Part 10).

**Common mistakes:**
- Returning only one number per subtree.
- Taking a node and also adding the better option of its children, instead of the children's `skip` values.
- Using the max of even or odd levels.
- Recursing on a 10^4-deep tree without raising the limit or going iterative.

---

### Q46 ⭐ 🟡 BST to a sorted circular doubly linked list, in place. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Reuse the nodes of a BST with distinct values (0 <= n <= 10^4): afterwards `left` is the previous (smaller) node and `right` is the next (larger) node, the smallest node is the head, and the list is circular (head.left is the largest node and the largest node's `right` is the head). Return the head (None for an empty tree) using the same node objects, checked by identity. Do it with an inorder walk that remembers the previous node, and keep the recursion depth in mind on a skewed tree. The example shows the values walking from the head along `right` for n steps. Example: root=[4, 2, 5, 1, 3] -> [1, 2, 3, 4, 5]; root=[] -> []; root=[7] -> [7]; root=[2, null, 3] -> [2, 3].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Inorder traversal with a "previous node" pointer. Inorder visits a BST in ascending order, so linking each visited node to the previous one builds the sorted list in place.

**Say this first (1 line):** "I walk the BST inorder, keep a `prev` pointer, set `prev.right = cur` and `cur.left = prev` for each node, remember the first as head, and at the end close the circle; I use an explicit stack so a skewed tree does not blow the recursion limit."

**Brute force:** Collect all nodes, sort them by value, then rewire `left` and `right` through the sorted list with modulo indexing. O(n log n) time (the sort), O(n) extra memory. It is the checker in the code.

**Optimal:**
- Inorder with an explicit stack: push the left spine, pop, visit, move to the right child.
- Read `nxt = cur.right` BEFORE you rewrite pointers, because linking overwrites it. That is the one classic bug.
- Link: if `prev` exists, `prev.right = cur`, `cur.left = prev`; else this is the head.
- After the loop, `head.left = prev` and `prev.right = head`.
- It reuses the nodes. The code checks by identity (`id`) that the set of node objects after is exactly the set before, that n steps along `right` returns to the head, and that `left` walks the same list backwards.
- Invariant: when `cur` is visited, `prev` is the largest node smaller than cur and everything up to prev is already a linked sorted chain.

**Complexity:** O(n) time, each node pushed and popped once. Extra space O(h) for the stack, O(n) worst case on a skewed tree. Pointers are rewired in place, so no new node objects. (Morris traversal could make the extra space O(1), but is not needed here.)

**Dry run:** [4,2,5,1,3].
| visit | prev | action |
|---|---|---|
| 1 | None | head = 1 |
| 2 | 1 | 1.right = 2, 2.left = 1 |
| 3 | 2 | 2.right = 3, 3.left = 2 |
| 4 | 3 | 3.right = 4, 4.left = 3 |
| 5 | 4 | 4.right = 5, 5.left = 4 |
| end | 5 | head.left = 5, 5.right = 1 |
Walking right from 1 for 5 steps: 1,2,3,4,5 and back to 1.

**Code:**
```python
from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
# ---- optimal: inorder walk remembering the previous node; relink left=prev, right=next; close the circle at the end.
# Iterative inorder (explicit stack) so a 10^4-deep skewed tree is safe.
def to_dll(root):
    head = prev = None
    st, cur = [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); nxt = cur.right                  # read the old right child BEFORE overwriting it
        if prev is None: head = cur
        else: prev.right = cur; cur.left = prev
        prev = cur; cur = nxt
    if head: head.left = prev; prev.right = head          # make it circular
    return head

# ---- the recursive version (shown for comparison; depth = tree height)
def to_dll_rec(root):
    prev = head = None
    def go(n):
        nonlocal prev, head
        if n is None: return
        go(n.left)
        if prev is None: head = n
        else: prev.right = n; n.left = prev
        prev = n
        go(n.right)
    go(root)
    if head: head.left = prev; prev.right = head
    return head

# ---- brute force: collect nodes in sorted order, then relink them
def brute(root):
    nodes, st = [], [root] if root else []
    while st:
        n = st.pop(); nodes.append(n)
        for c in (n.left, n.right):
            if c: st.append(c)
    nodes.sort(key=lambda n: n.val)                       # distinct values, so the order is the sorted order
    for i, n in enumerate(nodes):
        n.left, n.right = nodes[i - 1], nodes[(i + 1) % len(nodes)]
    return nodes[0] if nodes else None

def walk(head, n): 
    out, cur = [], head
    for _ in range(n): out.append(cur.val); cur = cur.right
    return out, cur

def verify(head, ids_before, n):
    """identity checks: same node objects, right walk sorted and circular, left walk is the reverse"""
    if n == 0: assert head is None; return
    vals, back = walk(head, n)
    assert back is head                                   # n steps along right returns to the head (circular)
    assert vals == sorted(vals) and len(set(vals)) == n
    seen, cur = [], head
    for _ in range(n): seen.append(id(cur)); cur = cur.right
    assert set(seen) == ids_before and len(seen) == n     # exactly the original node objects, none lost, none new
    cur, back_vals = head, []
    for _ in range(n): cur = cur.left; back_vals.append(cur.val)
    assert back_vals == vals[::-1]                        # left walk from head visits the largest first
    assert head.left.val == vals[-1] and head.left.right is head

def ids_of(root):
    out, st = set(), [root] if root else []
    while st:
        n = st.pop(); out.add(id(n)); st += [c for c in (n.left, n.right) if c]
    return out

# ---- examples from the question
N = None
for arr, want in [([4, 2, 5, 1, 3], [1, 2, 3, 4, 5]), ([], []), ([7], [7]), ([2, N, 3], [2, 3])]:
    r = build_tree(arr); ids = ids_of(r); h = to_dll(r)
    verify(h, ids, len(ids))
    assert (walk(h, len(ids))[0] if h else []) == want
print('examples ok')
one = build_tree([7]); h = to_dll(one); assert h is one and h.left is h and h.right is h
print('single node points at itself on both sides: head.left is head and head.right is head')

# ---- exhaustive over every BST shape up to 8 nodes; three algorithms, node identity checked
count = 0
for n in range(9):
    for sh in shapes(n):
        t = label(sh, 'in')
        for fn in (to_dll, to_dll_rec, brute):
            r = from_tup(t); ids = ids_of(r); verify(fn(r), ids, n)
        count += 1
print('BST shapes checked (0..8 nodes), three methods each, identity verified:', count)

# ---- seeded random BSTs with negatives
random.seed(46)
for _ in range(300):
    vals = random.sample(range(-100, 100), random.randint(1, 30))
    root = None
    for v in vals:
        nd = TreeNode(v)
        if root is None: root = nd; continue
        cur = root
        while True:
            side = 'left' if v < cur.val else 'right'
            if getattr(cur, side) is None: setattr(cur, side, nd); break
            cur = getattr(cur, side)
    ids = ids_of(root); verify(to_dll(root), ids, len(vals))
print('300 random BSTs ok')

# ---- deep skewed input: 10^4 nodes, left chain (values descending down the chain)
root = TreeNode(10000); cur = root
for v in range(9999, 0, -1): cur.left = TreeNode(v); cur = cur.left
ids = ids_of(root)
deep = TreeNode(10000); cur = deep
for v in range(9999, 0, -1): cur.left = TreeNode(v); cur = cur.left
try: to_dll_rec(deep); print('recursive version survived')
except RecursionError: print('recursive version on a 10000-deep chain: RecursionError (default limit 1000)')
h = to_dll(root); verify(h, ids, 10000)
print('iterative version on the same chain: head =', h.val, ', head.left =', h.left.val, ', n steps along right returns to head')
```

**Output (my run):**
```text
examples ok
single node points at itself on both sides: head.left is head and head.right is head
BST shapes checked (0..8 nodes), three methods each, identity verified: 2056
300 random BSTs ok
recursive version on a 10000-deep chain: RecursionError (default limit 1000)
iterative version on the same chain: head = 1 , head.left = 10000 , n steps along right returns to head
```

**Edge cases:**
- Empty tree: return None.
- One node: it points to itself on both sides (the code asserts it).
- Two nodes: each is the other's `left` and `right`.
- Skewed tree of 10^4: the recursive version raises RecursionError at the default limit; the stack version works.
- Walking a circular list with `while cur:` never ends. Always walk n steps or stop at the head.

**Follow-ups:**
- Non-circular, doubly linked? Skip the last two lines.
- Singly linked sorted list from a BST? Use only `right` and set `left` to None (Part 6 covers lists).
- Reverse conversion, sorted list to balanced BST? See the earlier Part 7 question.

**Common mistakes:**
- Overwriting `cur.right` before reading it.
- Forgetting the circular links, or setting them when the tree is empty.
- Comparing only values in tests, which would pass even if the answer used new nodes.
- Recursion on deep input.

---

### Q47 ⭐ 🟡 Smallest subtree containing all the deepest nodes. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the subtree (as a level-order array) rooted at the lowest node that has all the deepest leaves in its subtree (1 <= n <= 500); if there is a single deepest leaf the answer is that leaf alone. Each call returns (depth, node): when the two child depths are equal this node is the answer so far, otherwise take the deeper child's answer. Explain why this is the same idea as the LCA of the deepest leaves. Example: root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4] -> [2, 7, 4]; root=[1] -> [1]; root=[0, 1, 3, null, 2] -> [2]; root=[1, 2, 3] -> [1, 2, 3].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified)
**Pattern:** Post-order DFS returning two things, (depth, node). It is the lowest common ancestor of the deepest leaves, found without ever listing the leaves.

**Say this first (1 line):** "Each call returns the depth of its subtree and the answer node inside it: if both children are equally deep, this node is the answer; otherwise the answer comes from the deeper child."

**Brute force:** Record the root-path string of every node ('L','R' steps), find the maximum length, keep the nodes whose path is a prefix of all deepest paths, and take the longest such prefix. About O(n x depth) with strings. It is the checker, and it returns the real node object so identity can be compared.

**Optimal:**
- `go(None)` returns `(0, None)`.
- Else get `(dl, al)` and `(dr, ar)`.
- Equal depths: the deepest leaves lie in both children, so this node is their lowest meeting point, return `(dl + 1, node)`.
- Different depths: all the deepest leaves are on the deeper side, so return that side's answer and `max + 1`.
- Same idea as "LCA of the deepest leaves": the code also checks it against a generic LCA over the set of deepest leaves.
- Invariant: for every subtree, the returned node is the smallest subtree containing all the deepest leaves of THAT subtree.
- A single deepest leaf returns that leaf, because every ancestor above it has a shallower sibling (unequal depths).

**Complexity:** O(n) time, one visit per node. O(h) recursion stack, at most 500 here so the default limit is fine (a chain of 500 is in the test).

**Dry run:** [3,5,1,6,2,0,8,null,null,7,4]. Deepest leaves are 7 and 4 (depth 4).
| node | (depth, answer) |
|---|---|
| 7 | (1, 7) |
| 4 | (1, 4) |
| 2 | equal child depths -> (2, 2) |
| 6 | (1, 6) |
| 5 | left 6 depth 1, right 2 depth 2 -> deeper side, (3, 2) |
| 1 (children 0, 8) | equal -> (2, 1) |
| 3 | left 3 vs right 2 -> (4, 2) |
Answer node 2, whose subtree is [2,7,4].

**Code:**
```python
from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
# ---- optimal: each call returns (depth, answer node). Equal child depths -> this node; else the deeper child's answer.
def deepest_subtree(root):
    def go(n):
        if n is None: return 0, None
        dl, al = go(n.left); dr, ar = go(n.right)
        if dl == dr: return dl + 1, n
        return (dl + 1, al) if dl > dr else (dr + 1, ar)
    return go(root)[1]

# ---- brute force: list every node with its path from the root; find the deepest; keep the nodes that are a
# prefix (ancestor-or-self) of every deepest node; the lowest of them is the longest path.
def brute(root):
    items, st = [], [(root, '')]
    while st:
        n, p = st.pop(); items.append((n, p))
        if n.left: st.append((n.left, p + 'L'))
        if n.right: st.append((n.right, p + 'R'))
    deepest = max(len(p) for _, p in items)
    paths = [p for _, p in items if len(p) == deepest]
    best = max((x for x in items if all(q.startswith(x[1]) for q in paths)), key=lambda x: len(x[1]))
    return best[0]

def all_nodes(root):
    out, st = [], [root]
    while st:
        n = st.pop(); out.append(n); st += [c for c in (n.left, n.right) if c]
    return out

# ---- examples from the question
N = None
ex = [([3, 5, 1, 6, 2, 0, 8, N, N, 7, 4], [2, 7, 4]), ([1], [1]), ([0, 1, 3, N, 2], [2]), ([1, 2, 3], [1, 2, 3])]
for arr, want in ex:
    r = build_tree(arr); ans = deepest_subtree(r)
    assert to_arr(ans) == want and ans is brute(r)
    assert any(ans is n for n in all_nodes(r))             # a real node of the input tree, not a copy
print('examples ok:', [to_arr(deepest_subtree(build_tree(a))) for a, _ in ex])

# ---- exhaustive: every shape with 1..9 nodes, distinct values (so identity is also checked by `is`)
count = 0
for n in range(1, 10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre'))
        a, b = deepest_subtree(r), brute(r)
        assert a is b
        count += 1
print('shapes checked exhaustively (1..9 nodes):', count)

# ---- seeded random trees with holes, n up to 80
random.seed(47)
for _ in range(400):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 80)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    assert deepest_subtree(nodes[0]) is brute(nodes[0])
print('400 random trees ok')

# ---- same idea as 'LCA of the deepest leaves': check against a generic LCA on the deepest leaf set
def lca(root, targets):
    if root is None or root in targets: return root
    l, r = lca(root.left, targets), lca(root.right, targets)
    return root if l and r else (l or r)
for _ in range(200):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 60)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    depth, st, deep = {}, [(nodes[0], 0)], []
    while st:
        n, d = st.pop(); depth[n] = d
        st += [(c, d + 1) for c in (n.left, n.right) if c]
    m = max(depth.values()); deep = {n for n in nodes if depth[n] == m}
    assert lca(nodes[0], deep) is deepest_subtree(nodes[0])
print('LCA of the deepest-leaf set gives the same node on 200 random trees')

# ---- skewed chain of 500 nodes (the allowed maximum): the deepest node is the only leaf
root = TreeNode(0); cur = root
for i in range(1, 500): cur.right = TreeNode(i); cur = cur.right
assert deepest_subtree(root) is cur
print('chain of 500: the answer is the single leaf', cur.val)
```

**Output (my run):**
```text
examples ok: [[2, 7, 4], [1], [2], [1, 2, 3]]
shapes checked exhaustively (1..9 nodes): 6917
400 random trees ok
LCA of the deepest-leaf set gives the same node on 200 random trees
chain of 500: the answer is the single leaf 499
```

**Edge cases:**
- Single node: returns itself.
- Only one deepest leaf: the answer is that leaf.
- All leaves at the same depth: the root.
- A chain: the last node.
- Return the node itself, not a copy; the output is converted to a level-order array only for display, and tests compare with `is`.

**Follow-ups:**
- Two passes instead? First compute the max depth, then do an LCA. Same O(n).
- Iterative? Post-order with a stack and a dict of results by `id`.
- Values duplicated? Fine: nothing depends on values.

**Common mistakes:**
- Returning the child's node when depths are equal.
- Comparing depths of leaves instead of subtree heights.
- Off by one in the base case (0 for None, so a leaf has depth 1).
- Building a new tree for the answer.

---

### Q48 ⭐ 🔴 Morris inorder traversal in O(1) extra space. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return (values, iterations): the inorder values and the number of iterations of the main loop of Morris traversal, using no stack and no recursion by temporarily threading the right pointer of each node's inorder predecessor to the node itself, then removing the thread; the tree must be restored exactly (the tests compare by identity and by values afterwards). The loop is `while cur: if no left child: visit, cur = cur.right; else find the predecessor (rightmost node of cur.left, stopping if its right is cur); if its right is None: set it to cur, cur = cur.left; else: reset it to None, visit, cur = cur.right`. Show that the loop runs exactly n + L times where L is the number of nodes with a left child (each such node is reached twice), and explain why total time is still O(n) even though each predecessor search can be long. Mention when threading is unsafe (concurrent readers, or an exception midway). Example: root=[1, null, 2, 3] -> ([1, 3, 2], 4); root=[4, 2, 6, 1, 3, 5, 7] -> ([1, 2, 3, 4, 5, 6, 7], 10); root=[] -> ([], 0); root=[1, 2, null, 3] -> ([3, 2, 1], 5).
**Asked at:** Morris traversal explanations (Wikipedia threaded binary tree, GeeksforGeeks, a DEV Community post, a Codemia thread; snippets only, not opened: predecessor threading, O(1) extra space, restores the tree, risky if the tree is shared) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)
**Pattern:** Threaded traversal (Morris). Instead of a stack, borrow the empty right pointer of each node's inorder predecessor as a temporary "way back" to the node, then remove it.

**Say this first (1 line):** "For a node with a left child I find its inorder predecessor, the rightmost node of the left subtree; the first time I thread predecessor.right to the node and go left, the second time I see the thread, I remove it, visit the node and go right, so I need no stack and the tree ends up exactly as it started."

**Brute force:** Standard inorder with a recursion or an explicit stack. O(n) time, O(h) extra space (O(n) on a skewed tree). It is the checker in the code.

**Optimal:** The loop from the question.
- No left child: visit, move right (the right pointer may be a thread that leads back up).
- Left child present: walk `pred` down the right spine of `cur.left`, stopping at the end or at a node whose right is `cur`.
- `pred.right is None` (first arrival): set `pred.right = cur`, go left.
- `pred.right is cur` (second arrival): set `pred.right = None`, visit `cur`, go right. This restoring step is what leaves the tree unchanged.
- Loop count n + L: every node is the loop's `cur` once when it is visited. A node with a left child is also `cur` once earlier, on the first arrival. So iterations = n + L, L = nodes with a left child. The code asserts this on every tree shape with up to 9 nodes: `[1,null,2,3]` has n = 3, L = 1 (node 2), giving 4.
- Why O(n) total despite the inner search: a node on the right spine of some `cur.left` is walked over by that `cur`'s search. A node belongs to the right spine of at most one such left subtree, and the search runs at most twice per `cur`. So the inner loop runs at most 2n steps in total. The output shows the largest ratio measured is below 2.
- Invariant: when the loop arrives at `cur` for the first time, every node before cur's subtree in inorder has been output and all threads inside cur.left are gone.

**Complexity:** Time O(n) (at most n + L loop iterations plus at most 2n predecessor steps). Extra space O(1): only `cur` and `pred`, and the output list is not counted. No recursion, so a 20000-deep chain works.

**Dry run:** [1,null,2,3] (1 has right child 2, 2 has left child 3).
| it | cur | action | output |
|---|---|---|---|
| 1 | 1 | no left: visit, go right | 1 |
| 2 | 2 | left = 3; pred = 3, 3.right is None: thread 3.right = 2, go left | |
| 3 | 3 | no left: visit, cur = 3.right = 2 (the thread) | 1, 3 |
| 4 | 2 | pred = 3, 3.right is 2: remove thread, visit 2, go right (None) | 1, 3, 2 |
Four iterations, tree restored.

**Code:**
```python
from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
def morris(root, visit=None, stats=None):
    """Inorder with O(1) extra space. Returns (values, loop iterations). stats['walk'] counts predecessor steps."""
    out, cur, it = [], root, 0
    while cur:
        it += 1
        if cur.left is None:
            out.append(cur.val)
            if visit: visit(cur)
            cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur:   # rightmost of the left subtree, or the thread
                pred = pred.right
                if stats is not None: stats['walk'] += 1
            if pred.right is None:
                pred.right = cur; cur = cur.left                      # first arrival: thread, go left
            else:
                pred.right = None                                     # second arrival: remove the thread
                out.append(cur.val)
                if visit: visit(cur)
                cur = cur.right
    return out, it

def inorder_stack(root):                                              # reference
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

def snapshot(root):                                                   # identity picture of the tree: (node, left, right)
    out, st = [], [root] if root else []
    while st:
        n = st.pop(); out.append((id(n), id(n.left), id(n.right))); st += [c for c in (n.left, n.right) if c]
    return sorted(out)

def count_left(root):
    return sum(1 for n in all_nodes(root) if n.left)
def all_nodes(root):
    out, st = [], [root] if root else []
    while st:
        n = st.pop(); out.append(n); st += [c for c in (n.left, n.right) if c]
    return out

# ---- examples from the question
N = None
ex = [([1, N, 2, 3], ([1, 3, 2], 4)), ([4, 2, 6, 1, 3, 5, 7], ([1, 2, 3, 4, 5, 6, 7], 10)), ([], ([], 0)), ([1, 2, N, 3], ([3, 2, 1], 5))]
for arr, want in ex:
    r = build_tree(arr); before = snapshot(r)
    assert morris(r) == want, arr
    assert snapshot(r) == before and to_arr(r) == arr            # restored: same objects, same pointers, same values
print('examples ok:', [morris(build_tree(a)) for a, _ in ex])

# ---- exhaustive: every shape 0..9 nodes: values, loop count n + L, restoration by identity, walk bound
count = 0
for n in range(10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre')); before = snapshot(r)
        st = {'walk': 0}
        vals, it = morris(r, stats=st)
        assert vals == inorder_stack(r)
        assert it == n + count_left(r)                            # each node with a left child is reached twice
        assert snapshot(r) == before                              # every pointer back where it was
        assert st['walk'] <= 2 * n                                # total predecessor steps never above 2n
        count += 1
print('shapes checked (0..9 nodes):', count, '- loop count = n + L, tree restored by identity, predecessor steps <= 2n')

# ---- tightness of the 2n bound? largest ratio seen
best = 0
for n in range(1, 10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre')); st = {'walk': 0}; morris(r, stats=st); best = max(best, st['walk'] / n)
print('largest (predecessor steps) / n over all shapes up to 9 nodes: %.3f' % best)

# ---- seeded random trees: same checks
random.seed(48)
for _ in range(300):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 150)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    r = nodes[0]; before = snapshot(r)
    vals, it = morris(r)
    assert vals == inorder_stack(r) and it == len(nodes) + count_left(r) and snapshot(r) == before
print('300 random trees ok')

# ---- unsafe if interrupted: a visit() that raises leaves threads behind (compare pointers on the saved node list,
# because a normal traversal of a threaded tree would loop forever)
r = build_tree([4, 2, 6, 1, 3, 5, 7]); nodes = all_nodes(r); before = [(id(n.left), id(n.right)) for n in nodes]
def boom(n):
    if n.val == 3: raise RuntimeError('stop midway')
try: morris(r, visit=boom)
except RuntimeError: pass
after = [(id(n.left), id(n.right)) for n in nodes]
print('after an exception at value 3, pointers restored?', after == before)
assert after != before
was_none = [b[1] == id(None) for b in before]
leftover = [(n.val, n.right.val) for n, w in zip(nodes, was_none) if w and n.right is not None]
print('nodes that had no right child but now point to one (value, target) - the thread left behind:', leftover)
assert leftover

# ---- deep skewed trees: fine, no recursion at all
chain = TreeNode(0); cur = chain
for i in range(1, 20000): cur.left = TreeNode(i); cur = cur.left
vals, it = morris(chain)
print('left chain of 20000 nodes: first values', vals[:3], ', loop iterations =', it, '(n + L = 20000 + 19999)')
assert it == 39999 and vals == list(range(19999, -1, -1))
```

**Output (my run):**
```text
examples ok: [([1, 3, 2], 4), ([1, 2, 3, 4, 5, 6, 7], 10), ([], 0), ([3, 2, 1], 5)]
shapes checked (0..9 nodes): 6918 - loop count = n + L, tree restored by identity, predecessor steps <= 2n
largest (predecessor steps) / n over all shapes up to 9 nodes: 1.556
300 random trees ok
after an exception at value 3, pointers restored? False
nodes that had no right child but now point to one (value, target) - the thread left behind: [(3, 4)]
left chain of 20000 nodes: first values [19999, 19998, 19997] , loop iterations = 39999 (n + L = 20000 + 19999)
```

**Edge cases:**
- Empty tree: `([], 0)`.
- Right-only chain: L = 0, so n iterations and no threads.
- Left chain: every node has a left child, so 2n - 1 iterations (n + L with L = n - 1).
- Exception in the middle (a `visit` that raises): threads stay in the tree and an ordinary traversal of it would loop forever. The output shows a leftover thread. Wrap the walk in try/finally with a repair pass if that matters.
- Unsafe when other readers or threads traverse the same tree at the same time: they see right pointers that are not real children. Also unsafe on a read-only or shared tree.

**Follow-ups:**
- Preorder with Morris? Visit on the first arrival instead of the second.
- Is the O(1) space real? The output list is O(n); with a callback instead of a list the extra space is O(1).
- Why not Morris all the time? Mutation, no concurrency, slightly more pointer work than a stack.

**Common mistakes:**
- Forgetting the `pred.right is not cur` stop in the predecessor search, which loops forever on the second arrival.
- Not removing the thread.
- Visiting on the first arrival (that gives preorder).
- Claiming the inner loop makes it O(n^2).

---

### Q49 ⭐ 🔴 Boundary of a binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the boundary values anticlockwise starting at the root: the root; then the left boundary top-down (from the root's left child follow the left child when present, otherwise the right child, until a leaf, and the leaf is NOT included here); then all leaves left to right; then the right boundary BOTTOM-UP (from the root's right child, follow the right child when present, otherwise the left, until a leaf, which is not included). If the root has no left child the left boundary is empty, and likewise for the right; the root is never repeated, and a single-node tree gives [root]. 0 <= n <= 10^4. Write it in one pass with an iterative leaf collection so that a skewed tree does not overflow the stack. Example: root=[1, null, 2, 3, 4] -> [1, 3, 4, 2]; root=[1, 2, 3, 4, 5, 6, null, null, null, 7, 8, 9, 10] -> [1, 2, 4, 7, 8, 9, 10, 6, 3]; root=[1] -> [1]; root=[1, 2] -> [1, 2]; root=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)
**Pattern:** Three tree walks stitched together (left edge, leaves, right edge), all done with loops and an explicit stack so a skewed tree is safe.

**Say this first (1 line):** "Root first, then the left boundary top-down without its leaf, then every leaf left to right, then the right boundary bottom-up without its leaf; the root is never repeated and a missing left or right child just makes that edge empty."

**Brute force:** One recursive DFS with two flags (on-left-edge, on-right-edge): record left-edge nodes on entry, leaves as they appear, right-edge nodes on exit. It needs one pass but recursion, so it fails on a deep skew. It is the independent checker in the code.

**Optimal:**
- Output starts with the root value (nothing more if the tree has one node).
- Left boundary: start at `root.left`; while the node exists and is not a leaf, record it, then step to `left` if present, else `right`.
- Leaves: iterative DFS with a stack (push right then left), record each leaf except the root. Left-to-right order comes for free.
- Right boundary: start at `root.right`; while the node exists and is not a leaf, record it, step to `right` if present, else `left`. Reverse the list at the end for bottom-up.
- Why each leaf appears once: both edge walks stop BEFORE the leaf, and the leaf pass adds it. Why the root is not repeated: the leaf pass skips the root, and the edges start at its children.
- Why leaves hanging off an edge are fine: an edge walk that ends on a leaf stops one short, and the leaf pass picks that leaf up in its normal left-to-right position.

**Complexity:** O(n) time: the leaf pass visits every node once, the two edge walks follow at most h nodes each. O(h) extra space for the edge lists plus the stack, which is O(n) worst case on a skewed tree. No recursion.

**Dry run:** [1,null,2,3,4] (1 has right 2; 2 has children 3 and 4).
| part | result |
|---|---|
| root | 1 |
| left boundary | no left child, empty |
| leaves, left to right | 3, 4 |
| right boundary | start 2 (not a leaf): record 2, next is right child 4 (leaf): stop. Bottom-up [2] |
Answer [1,3,4,2].

**Code:**
```python
from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
def is_leaf(n): return n.left is None and n.right is None

# ---- optimal: three iterative pieces, no recursion
def boundary(root):
    if root is None: return []
    out = [root.val]
    n = root.left                                     # left boundary, top-down, leaf excluded
    while n and not is_leaf(n):
        out.append(n.val); n = n.left or n.right
    st = [root]                                       # leaves, left to right (root excluded, so a lone root is not repeated)
    while st:
        n = st.pop()
        if is_leaf(n) and n is not root: out.append(n.val)
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    right, n = [], root.right                         # right boundary, collected top-down, leaf excluded
    while n and not is_leaf(n):
        right.append(n.val); n = n.right or n.left
    return out + right[::-1]                          # ... then reversed to go bottom-up

# ---- brute force: one recursive DFS with two flags; left-boundary nodes on entry, leaves in order, right-boundary on exit
def brute(root):
    if root is None: return []
    res = [root.val]
    def go(n, onl, onr):
        if n is None: return
        leaf = n.left is None and n.right is None
        if onl and not leaf: res.append(n.val)
        if leaf: res.append(n.val)
        # a left-boundary node passes the flag to its left child, or to its right child when the left is missing
        go(n.left, onl, onr and n.right is None)
        go(n.right, onl and n.left is None, onr)
        if onr and not leaf: res.append(n.val)
    # the root is already in res; its left/right children start the two boundaries
    go(root.left, True, False)
    go(root.right, False, True)
    return res

# ---- examples from the question
N = None
ex = [([1, N, 2, 3, 4], [1, 3, 4, 2]),
      ([1, 2, 3, 4, 5, 6, N, N, N, 7, 8, 9, 10], [1, 2, 4, 7, 8, 9, 10, 6, 3]),
      ([1], [1]), ([1, 2], [1, 2]), ([], [])]
for arr, want in ex:
    r = build_tree(arr)
    assert boundary(r) == want == brute(r), arr
print('examples ok:', [w for _, w in ex])

# ---- exhaustive: every shape with 0..9 nodes (distinct values), plus a no-duplicates check
count = 0
for n in range(10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre'))
        a, b = boundary(r), brute(r)
        assert a == b, (tup(r), a, b)
        assert len(a) == len(set(a)) and set(a) <= set(range(n))     # no value repeated, only real nodes
        count += 1
print('shapes checked exhaustively (0..9 nodes):', count)

# ---- seeded random trees
random.seed(49)
for _ in range(400):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 100)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    a = boundary(nodes[0]); assert a == brute(nodes[0]) and len(a) == len(set(a))
print('400 random trees ok')

# ---- skewed input of 10^4 nodes: iterative code survives, the recursive brute force does not
chain = TreeNode(0); cur = chain
for i in range(1, 10000): cur.left = TreeNode(i); cur = cur.left
b = boundary(chain)
print('left chain of 10000: boundary length =', len(b), ', first 3 =', b[:3], ', last =', b[-1])
assert b == list(range(10000))
rchain = TreeNode(0); cur = rchain
for i in range(1, 10000): cur.right = TreeNode(i); cur = cur.right
b = boundary(rchain)
print('right chain of 10000: boundary length =', len(b), ', first 3 =', b[:3], ', last =', b[-1])
assert b == [0, 9999] + list(range(9998, 0, -1))
try: brute(chain); print('recursive survived')
except RecursionError: print('recursive brute force on the 10000-deep chain: RecursionError (default limit 1000)')
```

**Output (my run):**
```text
examples ok: [[1, 3, 4, 2], [1, 2, 4, 7, 8, 9, 10, 6, 3], [1], [1, 2], []]
shapes checked exhaustively (0..9 nodes): 6918
400 random trees ok
left chain of 10000: boundary length = 10000 , first 3 = [0, 1, 2] , last = 9999
right chain of 10000: boundary length = 10000 , first 3 = [0, 9999, 9998] , last = 1
recursive brute force on the 10000-deep chain: RecursionError (default limit 1000)
```

**Edge cases:**
- Empty tree: `[]`. Single node: `[root]`, not `[root, root]`.
- Root with only a left child: the right boundary is empty.
- A left-edge node with only a right child: the edge continues through its right child (`left or right`).
- A leaf at the end of an edge is listed once, in the leaf section.
- Skewed trees of 10^4 nodes: the iterative code runs, the recursive checker hits the recursion limit (shown).

**Follow-ups:**
- Clockwise instead? Reverse the whole answer except the root, with the same edge rules.
- Strictly one pass? The only full traversal is the leaf pass; the two edge walks touch at most h nodes each. The flagged DFS in the checker is a true single pass but recursive.
- Duplicate values? Fine, nothing depends on values.

**Common mistakes:**
- Including the edge's leaf twice (in the edge and in the leaves).
- Repeating the root when it is a leaf.
- Taking only `left` for the left edge and stopping at a missing left child, instead of falling back to `right`.
- Forgetting to reverse the right edge.

---

### Q50 ⭐ 🔴 Binary tree cameras, at concept level. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). A camera placed on a node watches that node, its parent and its children. Return the minimum number of cameras so every node is watched (0 for an empty tree; n <= 1000; the values are ignored). Use the greedy post-order rule with three states returned by each call: not watched, has a camera, watched by a child; put a camera on a node when any child is not watched, and treat the empty child as watched. Explain why the greedy places cameras on the parents of leaves and not on leaves, and why a root left unwatched at the end needs one more. Full tree DP belongs to Part 10. Example: root=[0, 0, null, 0, 0] -> 1; root=[0, 0, null, 0, null, 0, null, null, 0] -> 2; root=[0] -> 1; root=[0, 0, 0] -> 1; root=[] -> 0.
**Asked at:** Tree-DP pattern guides (techinterview.org tree-DP and DP-on-trees pages, AlgoMaster and Vultr House Robber III pages; snippets only, not opened: a (rob, skip) pair per subtree; camera states not covered / has camera / covered); full tree DP belongs to Part 10 | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)
**Pattern:** Greedy post-order with a three-state return value (tree DP at concept level; Part 10 covers the general DP). Decide a node's state from its children's states, working bottom-up.

**Say this first (1 line):** "Post-order, each node returns not-watched, has-camera or watched; if any child is not watched I put a camera here, if any child has a camera I am watched, else I am not watched yet and let my parent deal with it; and an empty child counts as watched."

**Brute force:** Try every subset of nodes in increasing size and test whether every node is watched by itself, its parent or a child. Exponential. It is the oracle for trees up to 9 nodes.

**Optimal:**
- States: 0 = not watched, 1 = has a camera, 2 = watched (by a child's camera).
- `None` returns 2: it needs nothing and offers nothing.
- If either child is 0: put a camera here (count + 1), return 1. This camera covers both children and the parent.
- Else if either child is 1: return 2.
- Else (both children watched, neither has a camera): return 0, my parent must handle me.
- After the root call, if the root is 0 add one more camera.
- Why parents of leaves and not the leaves: a leaf camera watches the leaf and its parent. A camera on the parent watches the leaf, the parent, the parent's other child and the grandparent, a superset. The output confirms on every tree shape up to 9 nodes that for n >= 2 some optimal placement uses no leaf. Example `[0,0,0]`: leaf cameras need 2, the greedy needs 1.
- Why the root fix: the rule defers "not watched" to the parent, but the root has none. A single node gives state 0, hence one camera.
- Invariant: when a node returns, every node strictly below it is watched and the count is minimal for that subtree, subject to the returned state.

**Complexity:** O(n) time, one visit per node. Space O(h) for the stack. The recursive form needs depth up to n = 1000, right at Python's default limit, and the output shows it fails on a 1000-node chain; the code's explicit-stack version handles it. A chain of k nodes needs ceil(k/3) cameras (tested).

**Dry run:** [0,0,null,0,0] (root with left child; that child has two leaf children).
| node | children states | decision | return |
|---|---|---|---|
| left leaf | 2, 2 | no camera needed | 0 (not watched) |
| right leaf | 2, 2 | | 0 |
| middle node | 0, 0 | camera here (count 1) | 1 |
| root | left 1, right None = 2 | child has camera | 2 |
Root is 2, no fix needed. Answer 1.

**Code:**
```python
from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
import itertools
NOT_WATCHED, CAMERA, WATCHED = 0, 1, 2

# ---- optimal greedy, recursive form (clear, fine up to depth ~900 under the default limit)
def cameras_rec(root):
    count = 0
    def go(n):
        nonlocal count
        if n is None: return WATCHED                      # an empty child never needs a camera
        a, b = go(n.left), go(n.right)
        if a == NOT_WATCHED or b == NOT_WATCHED: count += 1; return CAMERA
        if a == CAMERA or b == CAMERA: return WATCHED
        return NOT_WATCHED
    if go(root) == NOT_WATCHED: count += 1                # an unwatched root needs its own camera
    return count

# ---- same rule with an explicit post-order stack (safe for any depth)
def cameras(root):
    if root is None: return 0
    state, count, st = {}, 0, [(root, 0)]
    while st:
        n, s = st.pop()
        if s == 0:
            st.append((n, 1))
            for c in (n.left, n.right):
                if c: st.append((c, 0))
        else:
            a = state.get(id(n.left), WATCHED) if n.left else WATCHED
            b = state.get(id(n.right), WATCHED) if n.right else WATCHED
            if a == NOT_WATCHED or b == NOT_WATCHED: count += 1; state[id(n)] = CAMERA
            elif a == CAMERA or b == CAMERA: state[id(n)] = WATCHED
            else: state[id(n)] = NOT_WATCHED
    if state[id(root)] == NOT_WATCHED: count += 1
    return count

# ---- brute force: smallest subset of nodes that watches everyone (a camera watches itself, its parent, its children)
def watchers(root):
    """for each node (in a list), the set of node indexes whose camera would watch it; plus is_leaf flags"""
    nodes, st = [], [root] if root else []
    while st:
        n = st.pop(); nodes.append(n); st += [c for c in (n.left, n.right) if c]
    idx = {id(n): i for i, n in enumerate(nodes)}
    w = [{i} for i in range(len(nodes))]
    for i, n in enumerate(nodes):
        for c in (n.left, n.right):
            if c: w[i].add(idx[id(c)]); w[idx[id(c)]].add(i)
    leaf = [n.left is None and n.right is None for n in nodes]
    return w, leaf

def optimal_sets(root):
    w, leaf = watchers(root)
    for k in range(len(w) + 1):
        good = [c for c in itertools.combinations(range(len(w)), k) if all(w[i] & set(c) for i in range(len(w)))]
        if good: return k, good, leaf
def brute(root): return optimal_sets(root)[0] if root else 0

# ---- examples from the question
N = None
ex = [([0, 0, N, 0, 0], 1), ([0, 0, N, 0, N, 0, N, N, 0], 2), ([0], 1), ([0, 0, 0], 1), ([], 0)]
for arr, want in ex:
    r = build_tree(arr)
    assert cameras(r) == cameras_rec(r) == brute(r) == want, arr
print('examples ok:', [w for _, w in ex])

# ---- exhaustive: every shape with 0..9 nodes
count, no_leaf = 0, 0
for n in range(10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre'))
        g = cameras(r)
        assert g == cameras_rec(r) == brute(r), tup(r)
        if n >= 2:                                        # some optimal placement avoids every leaf (parent watches a superset)
            k, good, leaf = optimal_sets(r)
            assert any(not any(leaf[i] for i in c) for c in good)
            no_leaf += 1
        count += 1
print('shapes checked exhaustively (0..9 nodes):', count)
print('trees with n >= 2 where an optimal placement with no camera on a leaf exists:', no_leaf, '(all of them)')
print('[0,0,0]: a camera on each leaf needs 2, the greedy needs', cameras(build_tree([0, 0, 0])), '(the root watches all three)')

# ---- the root-unwatched case
single = build_tree([0]); chain3 = build_tree([0, 0, N, 0])
print('single node: greedy count =', cameras(single), '(the final root fix adds the camera)')
print('chain of 3: greedy count =', cameras(chain3), '(camera on the middle node)')
assert cameras(single) == 1 and cameras(chain3) == 1

# ---- seeded random trees up to 14 nodes against brute force
random.seed(50)
for _ in range(300):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 14)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    assert cameras(nodes[0]) == brute(nodes[0])
print('300 random trees (up to 14 nodes) ok')

# ---- depth: a chain of 1000 nodes (the allowed maximum)
root = TreeNode(0); cur = root
for i in range(1, 1000): cur.left = TreeNode(0); cur = cur.left
print('chain of 1000 nodes: iterative =', cameras(root))
assert cameras(root) == 334                           # ceil(n/3)
try: print('recursive =', cameras_rec(root))
except RecursionError: print('recursive version: RecursionError (default limit 1000)')
print('chain sizes 1..12 -> cameras:', [cameras(build_tree([0] + [0, N] * (k - 1))) for k in range(1, 13)], '(= ceil(k/3))')
assert all(cameras(build_tree([0] + [0, N] * (k - 1))) == -(-k // 3) for k in range(1, 40))
```

**Output (my run):**
```text
examples ok: [1, 2, 1, 1, 0]
shapes checked exhaustively (0..9 nodes): 6918
trees with n >= 2 where an optimal placement with no camera on a leaf exists: 6916 (all of them)
[0,0,0]: a camera on each leaf needs 2, the greedy needs 1 (the root watches all three)
single node: greedy count = 1 (the final root fix adds the camera)
chain of 3: greedy count = 1 (camera on the middle node)
300 random trees (up to 14 nodes) ok
chain of 1000 nodes: iterative = 334
recursive version: RecursionError (default limit 1000)
chain sizes 1..12 -> cameras: [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4] (= ceil(k/3))
```

**Edge cases:**
- Empty tree: 0. Single node: 1 (the root fix).
- Chain of 3: 1 camera on the middle node. Chain of 4: 2.
- Values are ignored.

**Follow-ups:**
- Why is the greedy optimal? Exchange argument: moving a camera from a leaf to its parent never loses coverage (shown above). Part 10 gives the DP version with the same answer.
- Different camera cost per node? The greedy breaks; use the full DP with states and costs.
- Camera covers distance 2? More states needed.

**Common mistakes:**
- Treating `None` as not watched, which forces cameras on leaves.
- Treating `None` as having a camera, which gives wrong answers.
- Forgetting the extra camera for an unwatched root.
- Recursing 1000 levels without thinking about the recursion limit.
