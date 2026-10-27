# Book 5 — Part 7: Trees and BST

**Topic:** Python DSA for product-company interviews: the TreeNode class (with __slots__) and a builder from level-order arrays with null, tree traversals recursive and iterative (preorder, inorder, postorder, level order, zigzag, right side view, vertical order, boundary), depth, height, diameter and balance, same tree, symmetric tree and subtree of another tree, inverting, the path-sum family (root to leaf, all root-to-leaf paths, any downward path counted with prefix sums), lowest common ancestor in a binary tree and in a BST, BST validate, insert, delete, k-th smallest, inorder successor, range sum, recover a BST with two swapped values and two-sum in a BST, building trees from preorder plus inorder, inorder plus postorder and from a BST preorder, sorted array and sorted list to a balanced BST, serialize and deserialize (preorder and BFS formats), flatten to a linked list, counting the nodes of a complete tree in O(log^2 n), maximum path sum, house robber III and binary tree cameras at concept level, Morris traversal, the O(h)-space BST iterator, converting a BST to a circular doubly linked list, N-ary tree basics, a trie as a tree at concept level, recursion limit and deep skewed trees with iterative alternatives, tree identity versus value equality (cycle and shared-node validation), and the complexity of traversals (time O(n), space O(h) versus O(w) versus O(n))

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 18, ⭐⭐ 21, ⭐ 11)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns binary trees, BSTs and N-ary tree basics. Part 4 owns stacks and queues (the iterative-stack and level-order queue ideas are cross-referenced only as 'Part 4 Q25' and 'Part 4 Q30'), Part 6 owns linked lists (the middle-of-list technique, the node-identity conventions and the recursion limit on long lists are cross-referenced as 'Part 6 Q2', 'Part 6 Q17' and 'Part 6 Q26'), Part 1 owns the array prefix-sum counting idea ('Part 1 Q13', which the tree version extends) and Part 3 the trie-versus-sorted-list comparison ('Part 3 Q36'); each of these references was checked against its heading by build.py. Part 8 owns heaps and greedy, Part 9 graphs (BFS and DFS on general graphs; the distance-K question uses a parent map and a BFS on a tree only), Parts 10 and 11 dynamic programming (house robber III and binary tree cameras appear here only as the return-a-tuple and greedy-state patterns), Part 12 backtracking and tries (the trie question is concept level), and Part 14 design problems. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: every prompt states its tree as a level-order array in the examples (null for a missing child, the children of a null are not listed, trailing nulls omitted) and uses `class TreeNode: __slots__ = ('val', 'left', 'right')` with constructor `TreeNode(val, left, right)`; N-ary trees use the LeetCode-style array with null separating each node's children, and the identity-validation question gives nodes as [val, left_index, right_index] triples. Questions that say 'in place' require the result to consist of the same node objects, which the tests verify by node identity. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example below is rendered from the same data that scratch/B5P07_wavea/check_examples.py executes (python3 -I) against node-based reference solutions, so no example can differ from what was run. Cross-checks: all 626 tree shapes with 0 to 7 nodes (label sets by preorder and by inorder) against independent brute force on tuple-encoded trees and on node-pair graphs for traversals in all orders (recursive against iterative), levels, zigzag, right view, vertical order, depth, minimum depth, balance, diameter (all-pairs distance), symmetry, invert, root-to-leaf and downward path sums (every target from -1 to 11), maximum width, serialization round trips in both formats, subtree, boundary (independent path-based definition), deepest-subtree, Morris traversal, flatten, binary tree cameras (smallest covering subset) and the lowest common ancestor and distance-K answers for every value pair; all BST shapes with 0 to 7 nodes against sorted-list brute force for validate, k-th smallest, LCA, range sum for every range, insert and delete of every present and absent key, successor, two-sum for every target, the BST iterator, BST from preorder and the doubly-linked-list conversion; plus seeded random cases: 1500 trees for maximum path sum (all node pairs), 600 for house robber III (all subsets), 3000 for validate BST (all ancestor constraints), 3000 random pointer graphs for identity validation, 400 N-ary trees and 500 tries. Claims tested exhaustively: preorder plus inorder and inorder plus postorder identify the tree for every shape up to 7 nodes, while preorder plus postorder does not (for n = 2 exactly one pair of trees collides, and the colliding trees are never full binary trees, while for full binary trees the pair is unique); the serialized string has exactly 2n + 1 tokens for n = 0..7 in both formats; the BST iterator never holds more than h nodes; the recover-BST pair to swap back is unique (for every BST shape up to 7 nodes and every swapped pair, exactly one value pair restores a BST); the three sorted-to-BST constructions (array, list with slow and fast pointers, list by inorder simulation) give the same height-balanced tree for every length 0 to 59; the Morris loop runs exactly n + L times (L = nodes with a left child) and restores every pointer; the level-order queue peaks at 2^(k-1) on a perfect tree of height k; the spine-step bound of the count-complete solution is at most 2h^2 for every n up to 2^11, exactly 2h for the perfect tree and exactly h(2h - 1) at n = 2^(h+1) - 2 for h >= 2, checked at the boundary cases n = 2^h, 2^(h+1) - 2 and 2^(h+1) - 1 for every h up to 13 (a first draft of the prompt said (h + 1)^2, which the run refuted at n = 22 where 26 steps exceed 25, and it was corrected before freezing); recursive depth on a skewed tree raises RecursionError at 2000 nodes under the default limit of 1000 while the iterative version handles 10^5; and the index-normalised width and the iterative deserializer both handle a 3000-node skewed tree. The prompts state their uniqueness rules (sorted-to-BST uses the lower middle, insert adds a leaf, delete uses the inorder successor, vertical-order ties take the smaller value, BFS serialization never trims markers). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part07_sources.md). Searches returned tree-pattern guides (techinterview.org), Naukri Code360 candidate-reported entries (Flipkart November 2021 online round with vertical order traversal, Amazon March 2022 SDE-2 with LCA of a binary tree), a Glassdoor Flipkart 2025 LCA report and a LeetCode discuss Facebook intern report (serialize and deserialize, LCA, smallest subtree with the deepest nodes), Morris traversal and count-complete-nodes explainers, tree-DP guides for house robber III and cameras, recover-BST write-ups and Python recursion-limit explainers; nothing was found tying construct-from-traversals, BST delete, flatten or boundary traversal to a named company, so 'Asked at' tags name source types (pattern guides, practice lists, candidate-reported snippets, editor knowledge of standard lists), not verified company reports. The pre/in/post-order uniqueness claims, the Morris iteration count and the count-complete step bounds were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

### Q1 ⭐⭐⭐ 🟢 Build a tree from a level-order array and print it back. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Write `build_tree(arr)` that returns the root (None for an empty array) and `to_level_order(root)` that returns the canonical array: the root, then for every non-null node in queue order its left and right child (null when missing), with trailing nulls removed. Use a `deque` for the queue (not `list.pop(0)`), keep an index into the array, and make `build_tree` O(n). Input arrays are canonical except that they may carry trailing nulls, which are ignored. Also say what the class needs (`__slots__`, default `None` children) and why a tree test harness should compare with `to_level_order` and not with `==`. Constraint: 0 <= n <= 10^4, values are integers. Example: arr=[1, 2, 3, null, 4, null, null] -> [1, 2, 3, null, 4]; arr=[3, 9, 20, null, null, 15, 7] -> [3, 9, 20, null, null, 15, 7]; arr=[] -> []; arr=[1, null, 2, null, 3] -> [1, null, 2, null, 3].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Queue-driven level-order construction. The array lists children in the same order a BFS would visit nodes, so a queue of "nodes waiting for children" plus one index into the array rebuilds the tree. (`null` in the prompt is `None` in Python.)

**Say this first (1 line):** "Make the root, put it on a deque; for each node I pop, the next two array slots are its left and right child. One index, one pass, O(n)."

**Brute force:** Same idea but with `list.pop(0)` for the queue and for consuming the array. Correct, but each `pop(0)` shifts the whole list, so O(n^2). Another brute force is index arithmetic (children of i at 2i+1 and 2i+2), which is wrong here because the array does NOT list the children of a null, so positions drift.

**Optimal:**
- `build_tree`: if the array is empty or starts with null, return None. Create the root, push it. While the queue is non-empty and the index is in range: pop a node, read `arr[i]` as its left child and `arr[i+1]` as its right child, create and push non-null ones, advance the index by 2.
- Invariant: the queue holds exactly the created nodes that still wait for their children, in the order their children appear in the array.
- Trailing nulls need no special code: the loop ends when the index runs out. Missing slots at the end simply mean "no child".
- `to_level_order`: BFS that pushes both children (even None) for every non-null node and appends None when it pops one. Then strip trailing Nones. That gives the canonical form.
- Class needs: `__slots__ = ('val', 'left', 'right')` (smaller nodes, no per-node `__dict__`, typos like `node.lef = x` raise) and defaults `left=None, right=None` so a leaf is `TreeNode(5)`.
- Harness rule: do NOT compare with `==`. `TreeNode` has no `__eq__`, so `==` is identity and two identical trees compare False. Compare `to_level_order(a) == to_level_order(b)`. It is canonical (one array per tree) and it also catches a cycle, because the guard asserts no node is seen twice.

**Complexity:** `build_tree`: each node is created once, pushed once, popped once, and the index moves by 2 per pop, so O(n) time and O(w) extra space for the queue, where w is the maximum width (O(n) worst case, for example a perfect tree). `to_level_order` is O(n) time and O(n) space (the output plus the queue and the seen set).

**Dry run:** `[1, 2, 3, null, 4]`. Root 1, queue [1]. Pop 1: left = arr[1] = 2, right = arr[2] = 3, queue [2, 3], i = 3. Pop 2: left = arr[3] = null (nothing), right = arr[4] = 4, queue [3, 4], i = 5. Pop 3: i = 5 is out of range, no children. Pop 4: nothing. Done. Tree: 1 -> (2 -> (null, 4), 3). Printing back: 1, 2, 3, null, 4, then 3 and 4 have no children and add trailing Nones which are stripped: `[1, 2, 3, null, 4]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force: same idea with list.pop(0) (O(n) per pop, so O(n^2) overall) ----------
def build_slow(arr):
    arr = list(arr)
    while arr and arr[-1] is None:
        arr.pop()
    if not arr:
        return None
    root = TreeNode(arr.pop(0)); q = [root]
    while q and arr:
        node = q.pop(0)                      # the O(n) pop
        l = arr.pop(0) if arr else None
        r = arr.pop(0) if arr else None
        if l is not None: node.left = TreeNode(l); q.append(node.left)
        if r is not None: node.right = TreeNode(r); q.append(node.right)
    return root

# ---------- examples ----------
for arr in ([1, 2, 3, None, 4, None, None], [3, 9, 20, None, None, 15, 7], [], [1, None, 2, None, 3]):
    print(arr, '->', to_level_order(build_tree(arr)))

# ---------- == versus to_level_order ----------
a, b = build_tree([1, 2, 3]), build_tree([1, 2, 3])
print('a == b:', a == b, '| same shape and values:', to_level_order(a) == to_level_order(b))
assert not hasattr(a, '__dict__')            # __slots__: no per-node dict
try:
    a.extra = 1
except AttributeError:
    print('slots block new attributes')

# ---------- cross-check: every shape up to 7 nodes, then seeded random trees ----------
count = 0
for t in all_trees(7):
    root = from_tuple(t)
    arr = to_level_order(root)
    assert to_tuple(build_tree(arr)) == t
    assert to_tuple(build_slow(arr)) == t
    assert to_tuple(build_tree(arr + [None, None, None])) == t   # trailing nulls ignored
    assert to_level_order(build_tree(arr)) == arr
    count += 1
print('shapes round-tripped:', count)

random.seed(5)
def random_tuple(n, lo=-9, hi=9):
    if n == 0:
        return None
    l = random.randint(0, n - 1)
    return (random.randint(lo, hi), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(500):
    t = random_tuple(random.randint(0, 40))
    arr = to_level_order(from_tuple(t))
    assert to_tuple(build_tree(arr)) == t == to_tuple(build_slow(arr))
print('random trees ok: 500')

# ---------- edge cases ----------
assert build_tree([]) is None and to_level_order(None) == []
assert build_tree([None]) is None            # a lone null is an empty tree
assert to_level_order(build_tree([7])) == [7]
# a long right chain (n = 10^4) builds without recursion
chain = [1]
for _ in range(9999):
    chain += [None, 1]
assert len(to_level_order(build_tree(chain))) == len(chain)
# cycle guard in the harness
c = TreeNode(1); c.left = c
try:
    to_level_order(c)
except AssertionError as e:
    print('guard fired:', e)
print('all asserts passed')
```

**Output (my run):**
```
[1, 2, 3, None, 4, None, None] -> [1, 2, 3, None, 4]
[3, 9, 20, None, None, 15, 7] -> [3, 9, 20, None, None, 15, 7]
[] -> []
[1, None, 2, None, 3] -> [1, None, 2, None, 3]
a == b: False | same shape and values: True
slots block new attributes
shapes round-tripped: 626
random trees ok: 500
guard fired: cycle or shared node
all asserts passed
```

**Edge cases:**
- Empty array, or `[null]`: return None; printing None gives `[]`.
- Single node: `[7]`.
- Input with trailing nulls: ignored, output has none.
- Long chain (n = 10^4): the builder is iterative, so no recursion limit problem.
- A null in the middle: its children are not listed, which is why index arithmetic (2i+1) fails.

**Follow-ups:**
- Why not recurse? Both functions would hit the recursion limit on a 10^4 chain; the queue version never does.
- Why strip trailing nulls? Without it two arrays describing one tree would differ and the harness comparison would give false failures.
- How do you test that a function changed a tree in place? Collect `id(node)` for all nodes before and after; the sets must be equal. The array form cannot show that.

**Common mistakes:**
- Using `list.pop(0)` as the queue (O(n^2)).
- Using 2i+1 / 2i+2 indexing on an array that skips the children of nulls.
- Forgetting to skip the index for a null child, so the right child is read from the wrong slot.
- Comparing trees with `==` and getting False for identical trees.
- Not stripping trailing nulls, or stripping them with `arr[:-1]` once instead of a loop.

### Q2 ⭐⭐⭐ 🟢 Maximum depth of a binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the number of nodes on the longest path from the root down to a leaf (0 for an empty tree), 0 <= n <= 10^5. Give the recursive version, then an iterative BFS version that counts levels and an iterative DFS version with a stack of (node, depth) pairs; state the time and the extra space of each in terms of n and the height h, and which tree shapes make the BFS use O(n) and the recursion use O(n). Example: root=[3, 9, 20, null, null, 15, 7] -> 3; root=[1, null, 2] -> 2; root=[] -> 0; root=[5] -> 1.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Tree height by divide and conquer (height = 1 + max of the children), or by walking level by level (BFS) or carrying the depth down (DFS).

**Say this first (1 line):** "Height of an empty tree is 0, otherwise 1 + max(left, right). Recursion is the clean answer; for a 10^5 chain I would switch to BFS or an explicit stack because Python's recursion limit is 1000."

**Brute force:** There is no real slower method for this problem. One naive option is to collect every root-to-leaf path and take the longest, which costs O(n) time on a chain but more space (a perfect tree has about n/2 paths of length log n each). The three versions below are all O(n) time. I use the tuple-based recursive height in the code as the independent checker.

**Optimal:** Three O(n) versions, all correct.
- Recursive: `0` for None, else `1 + max(depth(left), depth(right))`. Invariant: each call returns the height of its own subtree.
- BFS: process the queue one level at a time using the size snapshot (`for _ in range(len(q))`). The number of rounds is the height.
- DFS with a stack of `(node, depth)`: pop, update `best = max(best, depth)`, push both children with `depth + 1`. Order does not matter because we take a maximum.

**Complexity:**
| Version | Time | Extra space | Worst shape |
|---|---|---|---|
| Recursive | O(n) | O(h) call stack | skewed chain: h = n, so O(n), and it fails at the recursion limit |
| BFS | O(n) | O(w), w = widest level | perfect tree: the last level has (n + 1) / 2 nodes, so O(n) |
| DFS with stack | O(n) | O(h): at most one waiting sibling per level (the run checked stack <= h on all 626 shapes) | a comb where every node has a leaf sibling waiting while the long side is explored: the stack grows to about h, so O(n) |

Every node is visited once, so time is O(n) for all three. In my run on a perfect tree with 1023 nodes the BFS queue peaked at 512 while the recursion went only 10 deep; on a 100,000-node chain it is the reverse: the BFS queue held 1 node and the recursion would need 100,000 frames.

**Dry run:** `[3, 9, 20, null, null, 15, 7]`. Recursive: depth(9) = 1, depth(20) = 1 + max(depth(15), depth(7)) = 2, depth(3) = 1 + max(1, 2) = 3. BFS: level 1 is [3], level 2 is [9, 20], level 3 is [15, 7], then the queue is empty: 3 rounds.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force on tuples (independent of the node code) ----------
def height_tuple(t):
    return 0 if t is None else 1 + max(height_tuple(t[1]), height_tuple(t[2]))

# ---------- 1. recursive: height = 1 + max(children); tracks its own call depth ----------
def depth_rec(root, stats=None, d=1):
    if root is None:
        return 0
    if stats is not None:
        stats['rec'] = max(stats['rec'], d)          # deepest call stack of real nodes
    return 1 + max(depth_rec(root.left, stats, d + 1), depth_rec(root.right, stats, d + 1))

# ---------- 2. BFS: count levels with a size snapshot ----------
def depth_bfs(root, stats=None):
    if root is None:
        return 0
    q, levels = deque([root]), 0
    while q:
        levels += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        if stats is not None:
            stats['q'] = max(stats['q'], len(q))
    return levels

# ---------- 3. iterative DFS: stack of (node, depth) ----------
def depth_dfs(root, stats=None):
    best, st = 0, ([(root, 1)] if root else [])
    while st:
        node, d = st.pop()
        best = max(best, d)
        if node.left: st.append((node.left, d + 1))
        if node.right: st.append((node.right, d + 1))
        if stats is not None:
            stats['st'] = max(stats['st'], len(st))
    return best

def width_tuple(t):                                   # widest level, independent brute force
    lv, w = [t] if t else [], 0
    while lv:
        w = max(w, len(lv))
        lv = [c for x in lv for c in (x[1], x[2]) if c is not None]
    return w

# ---------- examples ----------
for arr in ([3, 9, 20, None, None, 15, 7], [1, None, 2], [], [5]):
    r = build_tree(arr)
    print(arr, '->', depth_rec(r), depth_bfs(r), depth_dfs(r))

# ---------- cross-check: all shapes up to 7 nodes; measure the space claims ----------
worst_st_gap = 0
for t in all_trees(7):
    r, h = from_tuple(t), height_tuple(t)
    s = {'rec': 0, 'q': 0, 'st': 0}
    assert depth_rec(r, s) == depth_bfs(r, s) == depth_dfs(r, s) == h
    assert s['rec'] == h                              # recursion depth = height
    assert s['q'] <= width_tuple(t)                   # BFS queue never exceeds the widest level (children of a level)
    assert s['st'] <= h                               # DFS stack never exceeds h entries
print('shapes ok: 626; rec depth == h; BFS queue <= widest level; DFS stack <= h')

random.seed(11)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (0, random_tuple(l), random_tuple(n - 1 - l))
for _ in range(400):
    t = random_tuple(random.randint(0, 60)); r = from_tuple(t)
    assert depth_rec(r) == depth_bfs(r) == depth_dfs(r) == height_tuple(t)
print('random ok: 400')

# ---------- shapes that make the space O(n) ----------
def perfect(k):                                       # k levels, n = 2^k - 1
    return None if k == 0 else TreeNode(0, perfect(k - 1), perfect(k - 1))
for k in (1, 4, 10):
    s = {'rec': 0, 'q': 0, 'st': 0}; r = perfect(k)
    depth_bfs(r, s); depth_dfs(r, s); depth_rec(r, s)
    print('perfect k=%d n=%d: BFS queue peak %d, DFS stack peak %d, recursion depth %d' % (k, 2**k - 1, s['q'], s['st'], s['rec']))
def skewed(n):                                        # right chain, built without recursion
    root = None
    for _ in range(n): root = TreeNode(0, None, root)
    return root
n = 100_000
r = skewed(n); s = {'rec': 0, 'q': 0, 'st': 0}
assert depth_bfs(r, s) == depth_dfs(r, s) == n
print('skewed n=%d: BFS queue peak %d, DFS stack peak %d' % (n, s['q'], s['st']))
try:
    depth_rec(r)
except RecursionError:
    print('skewed n=%d: recursive version raises RecursionError (default limit)' % n)

# ---------- edge cases ----------
assert depth_rec(None) == depth_bfs(None) == depth_dfs(None) == 0
assert depth_rec(TreeNode(5)) == 1
print('all asserts passed')
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> 3 3 3
[1, None, 2] -> 2 2 2
[] -> 0 0 0
[5] -> 1 1 1
shapes ok: 626; rec depth == h; BFS queue <= widest level; DFS stack <= h
random ok: 400
perfect k=1 n=1: BFS queue peak 0, DFS stack peak 0, recursion depth 1
perfect k=4 n=15: BFS queue peak 8, DFS stack peak 4, recursion depth 4
perfect k=10 n=1023: BFS queue peak 512, DFS stack peak 10, recursion depth 10
skewed n=100000: BFS queue peak 1, DFS stack peak 1
skewed n=100000: recursive version raises RecursionError (default limit)
all asserts passed
```

**Edge cases:**
- Empty tree: 0, not -1 (the prompt counts nodes, not edges).
- Single node: 1.
- Chain of 10^5 nodes: the recursive version raises `RecursionError`; BFS and DFS return 100000.
- The perfect-tree BFS queue peak counts the next level waiting, which is the widest level.

**Follow-ups:**
- Min depth? Same idea, but a node with one child is NOT a leaf, so you cannot take `min(left, right)` blindly when one side is None; BFS can stop at the first leaf.
- Could you raise `sys.setrecursionlimit`? You can, but very deep recursion can crash the interpreter (a C stack overflow). The explicit stack is the safe fix (see Part 4 Q25).
- Which of BFS and DFS uses less memory? It depends on the shape: DFS O(h) wins on bushy trees, BFS O(w) wins on skinny ones.

**Common mistakes:**
- Returning 1 for the empty tree, or counting edges when the prompt counts nodes.
- Using `list.pop(0)` for the BFS queue.
- Forgetting the size snapshot, so levels get mixed up and the count is wrong.
- Claiming the recursive version is O(1) space. It is O(h) on the call stack.

### Q3 ⭐⭐⭐ 🟢 Same tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given two trees p and q (each with 0 to 100 nodes), return True when they have the same shape and equal values at every position. Two empty trees are the same. Write it recursively in O(min(m, n)) time, and say why `p == q` on `TreeNode` objects (default equality) is False for two separately built identical trees while your function returns True, and why a lone None check must come before reading `.val`. Example: p=[1, 2, 3], q=[1, 2, 3] -> True; p=[1, 2], q=[1, null, 2] -> False; p=[1, 2, 1], q=[1, 1, 2] -> False; p=[], q=[] -> True; p=[], q=[1] -> False.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Walk two trees in lockstep (parallel recursion). Same tree means: same emptiness, same value, same left subtrees, same right subtrees.

**Say this first (1 line):** "Compare node by node: both None is True, exactly one None is False, then values equal and both children pairs the same. It stops at the first mismatch."

**Brute force:** Serialise both trees to the canonical level-order array and compare the lists. Correct (canonical form is one-to-one with trees), O(m + n) time and O(m + n) space, and it always builds both arrays even when the roots already differ.

**Optimal:**
- `same(p, q)`: if both are None return True. If only one is None return False. Else return `p.val == q.val and same(p.left, q.left) and same(p.right, q.right)`.
- Invariant: a call returns True exactly when the two subtrees it was given are identical in shape and values.
- The `and` chain short-circuits, so the first mismatch ends the whole comparison.
- Order of the checks matters: the "one is None" test must come before `.val`. Reading `.val` on None raises `AttributeError`.
- `p == q` on `TreeNode` objects is False for two separately built identical trees because the class defines no `__eq__`, so Python falls back to identity (`is`). Our function compares content; `p is q` compares objects. Both trees being the same object is a quick True but is not required.

**Complexity:** A call that sees two real nodes consumes one node from each tree, and no node is compared twice, so there are at most min(m, n) such calls. Each makes two child calls, so total calls are at most 2 * min(m, n) + 1: O(min(m, n)) time. I checked this bound on all 1058 pairs of trees with up to 4 nodes (including all-equal values, the worst case); equal trees with n nodes use exactly 2n + 1 calls. Space is O(min(h1, h2)) for the call stack (the recursion stops when the shallower tree ends).

**Dry run:** `p = [1, 2]`, `q = [1, null, 2]`. same(1, 1): values equal. Left: p.left = 2, q.left = None, exactly one is None, return False. The `and` stops, so the right children are never looked at. Result False. For `[1, 2, 1]` against `[1, 1, 2]`: roots equal, then left values 2 and 1 differ, False.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force: serialise both with the canonical level-order array and compare ----------
def same_brute(p, q):
    return to_level_order(p) == to_level_order(q)

# ---------- optimal: walk both trees together; counts calls so the bound can be tested ----------
def same_tree(p, q, calls=None):
    if calls is not None:
        calls[0] += 1
    if p is None and q is None:          # both empty: same
        return True
    if p is None or q is None:           # exactly one empty: different (checked BEFORE .val)
        return False
    return (p.val == q.val
            and same_tree(p.left, q.left, calls)
            and same_tree(p.right, q.right, calls))

# ---------- examples ----------
cases = [([1, 2, 3], [1, 2, 3]), ([1, 2], [1, None, 2]), ([1, 2, 1], [1, 1, 2]), ([], []), ([], [1])]
for a, b in cases:
    p, q = build_tree(a), build_tree(b)
    print(a, b, '->', same_tree(p, q), '| p == q:', p == q)

# ---------- == is identity; the function ignores identity ----------
p, q = build_tree([1, 2, 3]), build_tree([1, 2, 3])
assert p != q and same_tree(p, q) and same_tree(p, p)
assert p is not q and p.left is not q.left        # different objects, same content

# ---------- cross-check: every pair of shapes up to 4 nodes with all-equal values (worst case for work),
# and every pair of preorder-labelled trees (values differ by position) ----------
def sized(t, v):
    """same shape, every value set to v"""
    return None if t is None else (v, sized(t[1], v), sized(t[2], v))
def size(t):
    return 0 if t is None else 1 + size(t[1]) + size(t[2])
pairs = 0
trees = all_trees(4)
for t1 in trees:
    for t2 in trees:
        for a, b in ((t1, t2), (sized(t1, 0), sized(t2, 0))):
            p, q, c = from_tuple(a), from_tuple(b), [0]
            got = same_tree(p, q, c)
            assert got == (a == b) == same_brute(p, q)
            m = min(size(a), size(b))
            assert c[0] <= 2 * m + 1                 # at most 1 + 2 * min(m, n) calls
            pairs += 1
print('pairs checked:', pairs, '| calls never exceed 2*min(m,n)+1')

# the bound is tight for equal trees: n nodes -> n real comparisons + n + 1 empty-pair calls
c = [0]; same_tree(build_tree(list(range(1, 8))), build_tree(list(range(1, 8))), c)
print('equal 7-node trees: calls =', c[0], '(2n + 1 = 15)')

random.seed(3)
for _ in range(500):
    n = random.randint(0, 12)
    arr = [random.randint(0, 1) for _ in range(n)]
    arr2 = list(arr)
    if arr2 and random.random() < 0.5:
        arr2[random.randrange(len(arr2))] = random.randint(0, 1)
    p, q = build_tree(arr), build_tree(arr2)
    assert same_tree(p, q) == same_brute(p, q) == (to_tuple(p) == to_tuple(q))
print('random ok: 500')

# ---------- edge cases ----------
assert same_tree(None, None) and not same_tree(None, TreeNode(0)) and not same_tree(TreeNode(0), None)
assert same_tree(TreeNode(0), TreeNode(0)) and not same_tree(TreeNode(0), TreeNode(1))
try:
    (lambda a, b: a.val == b.val)(None, TreeNode(1))
except AttributeError:
    print('reading .val before the None check would raise AttributeError')
print('all asserts passed')
```

**Output (my run):**
```
[1, 2, 3] [1, 2, 3] -> True | p == q: False
[1, 2] [1, None, 2] -> False | p == q: False
[1, 2, 1] [1, 1, 2] -> False | p == q: False
[] [] -> True | p == q: True
[] [1] -> False | p == q: False
pairs checked: 1058 | calls never exceed 2*min(m,n)+1
equal 7-node trees: calls = 15 (2n + 1 = 15)
random ok: 500
reading .val before the None check would raise AttributeError
all asserts passed
```

**Edge cases:**
- Both empty: True. One empty: False.
- Same shape, one different value: False.
- Same values and same multiset but different shape (`[1, 2]` vs `[1, null, 2]`): False.
- Same object passed twice: True without special code.
- A tree with 100 nodes is within the default recursion limit only if it is not a chain; a 100-node chain is still fine (depth 100).

**Follow-ups:**
- Iterative version? A stack (or deque) of node pairs: pop a pair, apply the same three checks, push the two child pairs.
- Is one tree a subtree of another? Reuse this function at every node of the big tree (O(m * n) worst case); see the subtree question later in this part.
- Compare as a set of values only? That is a different problem; shape and position would be ignored.

**Common mistakes:**
- Reading `.val` before the None checks.
- Using `p == q` and getting False for identical trees (or, worse, True only because someone defined `__eq__` carelessly).
- Comparing only the preorder (or only the inorder) values: different shapes can give the same list unless null markers are included.
- Forgetting the case "both None", so a leaf pair returns False.

### Q4 ⭐⭐⭐ 🟢 Invert a binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Swap the left and right child of every node and return the root, in place: the result must consist of the same node objects, which the tests check by identity (0 <= n <= 10^5, so the iterative version matters; see Part 4 Q25 for the explicit-stack idea). Give the recursive version and an iterative version using a stack or a deque, and explain why the order in which you visit nodes does not matter here but the swap must happen once per node. Example: [4,2,7,1,3,6,9] -> [4,7,2,9,6,3,1]. Example: root=[4, 2, 7, 1, 3, 6, 9] -> [4, 7, 2, 9, 6, 3, 1]; root=[2, 1, 3] -> [2, 3, 1]; root=[] -> []; root=[1, 2] -> [1, null, 2].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Tree recursion with a local rewrite: do one small operation (swap the two child pointers) at every node. Any traversal order works.

**Say this first (1 line):** "At every node swap left and right, exactly once. In place means I rewire pointers on the existing nodes and return the same root; no new nodes."

**Brute force:** Build a mirrored copy: `TreeNode(v, copy(right), copy(left))`. Values and shape are right, but it allocates n new nodes (O(n) extra memory) and fails the identity check, because the result does not consist of the original objects.

**Optimal:**
- Recursive: `root.left, root.right = invert(root.right), invert(root.left)`. The two calls return the inverted subtrees, and the tuple assignment puts them in swapped slots.
- Iterative: stack of nodes. Pop a node, swap its two children, push the (new) children that exist. Preorder, postorder or level order all work, and a `deque` gives the same result.
- Why the order does not matter: the swap at one node only touches that node's two pointers, and a node's swap does not depend on what happened below it. What matters is that every node is swapped exactly once.
- Why "once": swapping twice undoes itself. The run shows a version that swaps before and after recursing and leaves `[2, 1, 3]` unchanged. Inverting the whole tree twice also returns the original.

**Complexity:** Time O(n): one visit and one swap per node. Extra space: recursive O(h) call stack (O(n) on a chain); iterative with a stack O(h) (it holds at most about one waiting sibling per level), with a deque O(w), the widest level. Either is O(n) in the worst case. No new nodes are allocated.

**Dry run:** `[2, 1, 3]`. Pop 2: swap, now left = 3, right = 1; push both. Pop 1 (a leaf): swap None with None, nothing to push. Pop 3: same. Level order of the result: `[2, 3, 1]`. For `[1, 2]`: root 1 has left 2; swap gives right = 2, so `[1, null, 2]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force: build a NEW mirrored tree (correct values, but not in place) ----------
def invert_copy(root):
    if root is None:
        return None
    return TreeNode(root.val, invert_copy(root.right), invert_copy(root.left))

# ---------- optimal 1: recursive, in place ----------
def invert_rec(root):
    if root is None:
        return None
    root.left, root.right = invert_rec(root.right), invert_rec(root.left)   # one swap per node
    return root

# ---------- optimal 2: iterative, in place (stack; a deque gives the same result) ----------
def invert_iter(root):
    st = [root] if root else []
    while st:
        node = st.pop()
        node.left, node.right = node.right, node.left                       # one swap per node
        if node.left: st.append(node.left)
        if node.right: st.append(node.right)
    return root

# ---------- helpers ----------
def all_nodes(root):
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(n)
        for c in (n.left, n.right):
            if c: st.append(c)
    return out
def tmirror(t):
    return None if t is None else (t[0], tmirror(t[2]), tmirror(t[1]))

# ---------- examples ----------
for arr in ([4, 2, 7, 1, 3, 6, 9], [2, 1, 3], [], [1, 2]):
    print(arr, '->', to_level_order(invert_iter(build_tree(arr))), to_level_order(invert_rec(build_tree(arr))))

# ---------- cross-check: every shape up to 7 nodes; identity verified ----------
for t in all_trees(7):
    for fn in (invert_rec, invert_iter):
        root = from_tuple(t)
        before = all_nodes(root)
        ids_before = {id(n) for n in before}
        old_kids = {id(n): (n.left, n.right) for n in before}      # keep references so ids stay valid
        res = fn(root)
        assert res is root                                         # same root object returned
        assert to_tuple(res) == tmirror(t)                         # values/shape mirrored
        after = all_nodes(res)
        assert len(after) == len(before) and {id(n) for n in after} == ids_before   # same node objects
        for n in before:                                           # every node swapped exactly once
            assert (n.left, n.right) == old_kids[id(n)][::-1]
    c = from_tuple(t)
    assert to_tuple(invert_copy(c)) == tmirror(t)
print('all 626 shapes: mirrored, same root, same node objects, each node swapped once')

# the copy version fails the identity test, which is why the prompt checks identity
root = build_tree([1, 2, 3]); ids = {id(n) for n in all_nodes(root)}
new = invert_copy(root)
print('copy reuses nodes:', bool(ids & {id(n) for n in all_nodes(new)}))

# invert twice = original (so a "swap before and after" bug cancels itself out)
root = build_tree([4, 2, 7, 1, 3, 6, 9]); orig = to_level_order(root)
invert_iter(invert_iter(root)); assert to_level_order(root) == orig
def invert_twice_bug(root):
    if root is None: return None
    root.left, root.right = root.right, root.left
    invert_twice_bug(root.left); invert_twice_bug(root.right)
    root.left, root.right = root.right, root.left     # second swap undoes the first
    return root
r = build_tree([2, 1, 3]); invert_twice_bug(r)
print('swapping twice per node leaves', to_level_order(r), '(unchanged)')

random.seed(1)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 99), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(300):
    t = random_tuple(random.randint(0, 80))
    r1, r2 = from_tuple(t), from_tuple(t)
    assert to_tuple(invert_rec(r1)) == to_tuple(invert_iter(r2)) == tmirror(t)
print('random ok: 300')

# ---------- edge cases and depth ----------
assert invert_rec(None) is None and invert_iter(None) is None
one = TreeNode(9); assert invert_iter(one) is one and to_level_order(one) == [9]
n = 100_000
root = None
for i in range(n): root = TreeNode(i, root, None)             # left chain of 10^5 nodes
root = invert_iter(root)
depth, cur = 0, root
while cur: depth, cur = depth + 1, cur.right                  # now it is a right chain
assert depth == n
try:
    invert_rec(root)
except RecursionError:
    print('recursive version raises RecursionError on a 10^5 chain')
print('all asserts passed')
```

**Output (my run):**
```
[4, 2, 7, 1, 3, 6, 9] -> [4, 7, 2, 9, 6, 3, 1] [4, 7, 2, 9, 6, 3, 1]
[2, 1, 3] -> [2, 3, 1] [2, 3, 1]
[] -> [] []
[1, 2] -> [1, None, 2] [1, None, 2]
all 626 shapes: mirrored, same root, same node objects, each node swapped once
copy reuses nodes: False
swapping twice per node leaves [2, 1, 3] (unchanged)
random ok: 300
recursive version raises RecursionError on a 10^5 chain
all asserts passed
```

**Edge cases:**
- Empty tree: return None (both versions guard it).
- Single node: unchanged, same object.
- Skewed tree of 10^5 nodes: the iterative version flips the chain; the recursive one raises `RecursionError` (default limit 1000), so the iterative one is the safe answer (see Part 4 Q25).
- Nodes reachable twice (a DAG or shared subtree) would be swapped twice and so restored; the tests build proper trees, and the harness aliasing guard catches shared nodes.

**Follow-ups:**
- Check "symmetric" using invert? You could invert a copy and compare with `same_tree`, but the direct mirror comparison (next questions) needs no copy.
- In-place proof in a test? Collect `id(node)` before and after; the sets must be equal, and each node's children must be the old pair reversed. The run does exactly this on all 626 shapes up to 7 nodes.
- Why return the root? Callers can write `root = invert(root)`; the root object itself never changes.

**Common mistakes:**
- Swapping twice per node (before and after recursing), which cancels.
- Swapping only at the root, or only at internal nodes with two children (single-child nodes must swap too).
- Building new nodes and claiming it is in place.
- Using recursion for 10^5 nodes without noting the recursion limit.

### Q5 ⭐⭐⭐ 🟢 Symmetric tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Decide whether a tree is a mirror image of itself around its root (the left subtree is the mirror of the right subtree: same values, with left and right swapped), 0 <= n <= 1000. Write the recursive two-node comparison `mirror(a, b)` and an iterative version with a queue of pairs. Note that comparing the in-order sequences is not enough (explain with a counter-example, or run one). An empty tree is symmetric. Example: root=[1, 2, 2, 3, 4, 4, 3] -> True; root=[1, 2, 2, null, 3, null, 3] -> False; root=[1, 2, 2, null, 3, 3] -> True; root=[1, 2, 3] -> False; root=[1] -> True.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Two-pointer recursion on a tree: walk the left subtree and the right subtree at the same time, with the children paired crosswise (outer with outer, inner with inner).

**Say this first (1 line):** "A tree is symmetric if its left subtree is the mirror of its right subtree. `mirror(a, b)` compares a.left with b.right and a.right with b.left."

**Brute force:** Make a mirrored copy of the whole tree and compare it with the original using the same-tree check. Correct, O(n) time but O(n) extra space for the copy, and you do the work twice. Another idea, comparing the inorder sequence for a palindrome, is WRONG (see below).

**Optimal:**
- `mirror(a, b)`: both None means True; exactly one None means False; otherwise `a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)`.
- `is_symmetric(root)`: True for an empty tree, else `mirror(root.left, root.right)`.
- Invariant: `mirror(a, b)` is True exactly when `b`'s subtree is the left-right reflection of `a`'s.
- Iterative: a deque of pairs starting with `(root.left, root.right)`. Pop a pair; skip it if both are None; return False if only one is None or the values differ; else push `(a.left, b.right)` and `(a.right, b.left)`.
- Why inorder is not enough: the tree `[1, null, 1]` has inorder `[1, 1]`, a palindrome, but it is not symmetric (the only child sits on the right). Likewise the left chain `[2, 1, null, 2]` reads 2, 1, 2 in order. Inorder (or preorder) values without null markers lose the shape. The code searched all small labelled trees and found the first one automatically.

**Complexity:** Time O(n): each node is part of exactly one pair, so every node is visited once (about n/2 pair comparisons). Space: recursive O(h); iterative queue O(w).

**Dry run:** `[1, 2, 2, null, 3, null, 3]`. Pair (2, 2): values equal. Outer pair: (2.left = None, 2.right = 3): exactly one is None, so False. Result False. For `[1, 2, 2, null, 3, 3]`: left 2 has right child 3, right 2 has left child 3. Pair (2, 2) equal; outer pair (None, None) fine; inner pair (3, 3): equal, their children are all None. True.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

import itertools

# ---------- brute force: mirror the whole tree on tuples, compare with the original ----------
def tmirror(t):
    return None if t is None else (t[0], tmirror(t[2]), tmirror(t[1]))
def symmetric_brute(root):
    t = to_tuple(root)
    return t == tmirror(t)

# ---------- optimal 1: recursive two-node comparison ----------
def mirror(a, b):
    if a is None and b is None: return True
    if a is None or b is None: return False
    return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
def is_symmetric(root):
    return root is None or mirror(root.left, root.right)

# ---------- optimal 2: iterative, queue of pairs ----------
def is_symmetric_iter(root):
    if root is None: return True
    q = deque([(root.left, root.right)])
    while q:
        a, b = q.popleft()
        if a is None and b is None: continue
        if a is None or b is None or a.val != b.val: return False
        q.append((a.left, b.right))       # outer pair
        q.append((a.right, b.left))       # inner pair
    return True

# ---------- examples ----------
for arr in ([1, 2, 2, 3, 4, 4, 3], [1, 2, 2, None, 3, None, 3], [1, 2, 2, None, 3, 3], [1, 2, 3], [1]):
    r = build_tree(arr)
    print(arr, '->', is_symmetric(r), is_symmetric_iter(r))

# ---------- cross-check: every shape up to 7 nodes, every labelling with values {0, 1}; then values 0..2 on 5 nodes ----------
def relabel(shape_tree, vals):
    it = iter(vals)
    def go(t):
        if t is None: return None
        v = next(it); L = go(t[1]); return (v, L, go(t[2]))
    return go(shape_tree)
checked = sym_count = 0
for n in range(8):
    for s in shapes(n):
        base = label_pre(s)
        for vals in itertools.product((0, 1), repeat=n):
            t = relabel(base, vals); r = from_tuple(t)
            e = t == tmirror(t)
            assert is_symmetric(r) == is_symmetric_iter(r) == symmetric_brute(r) == e
            checked += 1; sym_count += e
print('labelled trees checked:', checked, '| symmetric among them:', sym_count)
for s in shapes(5):
    for vals in itertools.product((0, 1, 2), repeat=5):
        t = relabel(label_pre(s), vals); assert is_symmetric(from_tuple(t)) == (t == tmirror(t))

# ---------- why comparing inorder values is NOT enough: search for a counter-example ----------
def tin(t): return [] if t is None else tin(t[1]) + [t[0]] + tin(t[2])
found = None
for n in range(1, 6):
    for s in shapes(n):
        for vals in itertools.product((1, 2), repeat=n):
            t = relabel(label_pre(s), vals)
            if t != tmirror(t) and tin(t) == tin(t)[::-1]:
                found = t; break
        if found: break
    if found: break
r = from_tuple(found)
print('palindromic inorder but NOT symmetric:', to_level_order(r), 'inorder', tin(found))
assert not is_symmetric(r) and tin(found) == tin(found)[::-1]
# a bigger one: values 1,2,1 in a left chain also reads 1,2,1 in order
r2 = build_tree([2, 1, None, 2])  # left chain 2 -> 1 -> 2
print('left chain', to_level_order(r2), 'inorder', tin(to_tuple(r2)), 'symmetric:', is_symmetric(r2))

# ---------- random trees built to be symmetric, then perturbed ----------
random.seed(9)
def random_tuple(n, k=3):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, k - 1), random_tuple(l, k), random_tuple(n - 1 - l, k))
for _ in range(500):
    half = random_tuple(random.randint(0, 20))
    t = (7, half, tmirror(half)); assert is_symmetric(from_tuple(t)) and is_symmetric_iter(from_tuple(t))
    if half is not None:                      # change one value on the right side
        u = (7, half, (tmirror(half)[0] + 1,) + tmirror(half)[1:]); r = from_tuple(u)
        assert not is_symmetric(r) and not is_symmetric_iter(r)
print('random ok: 500 symmetric, 500 perturbed')

# ---------- edge cases ----------
assert is_symmetric(None) and is_symmetric_iter(None)
assert is_symmetric(TreeNode(1)) and not is_symmetric(build_tree([1, 2]))
assert not is_symmetric(build_tree([1, None, 1]))
print('all asserts passed')
```

**Output (my run):**
```
[1, 2, 2, 3, 4, 4, 3] -> True True
[1, 2, 2, None, 3, None, 3] -> False False
[1, 2, 2, None, 3, 3] -> True True
[1, 2, 3] -> False False
[1] -> True True
labelled trees checked: 64979 | symmetric among them: 103
palindromic inorder but NOT symmetric: [1, None, 1] inorder [1, 1]
left chain [2, 1, None, 2] inorder [2, 1, 2] symmetric: False
random ok: 500 symmetric, 500 perturbed
all asserts passed
```

**Edge cases:**
- Empty tree: True. Single node: True.
- Root with only one child: False.
- Equal values but a different shape: False, that is the whole point of the null checks.
- Many duplicates (`[2, 2, 2]` shapes): the shape check still decides.
- I checked both versions against the brute force on all 64,979 labelled trees (values 0 or 1) with up to 7 nodes; only 103 of them are symmetric.

**Follow-ups:**
- Symmetric by structure only (ignore values)? Drop the value comparison.
- Why a queue of pairs and not a stack? Either works; the order of checking pairs does not change the answer, only which mismatch is found first.
- Relate to invert: `mirror(a, b)` is "same_tree(a, invert(b))" without building the inverted copy (see Q3 and Q4 above).

**Common mistakes:**
- Comparing `a.left` with `b.left` (that is the same-tree check, not the mirror).
- Comparing inorder sequences, or preorder values without null markers.
- Forgetting that the root with a single child is not symmetric.
- Reading `.val` before the None checks.

### Q6 ⭐⭐⭐ 🟢 Lowest common ancestor in a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is a binary search tree with distinct values (smaller values left, larger right) with 2 <= n <= 10^5 nodes; p and q are two different values that exist in the tree. Return the value of their lowest common ancestor (a node may be its own ancestor). Use the BST order to walk down once, iteratively, in O(h) time and O(1) extra space, and say exactly when the walk stops (the first node whose value lies between p and q, inclusive). Example: root=[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5], p=2, q=8 -> 6; root=[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5], p=2, q=4 -> 2; root=[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5], p=3, q=5 -> 4; root=[2, 1], p=2, q=1 -> 2.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified)

**Pattern:** BST order as a compass. Each comparison tells you which side both targets are on, so you never need to search both subtrees.

**Say this first (1 line):** "Start at the root. If both values are smaller, go left; if both are larger, go right; otherwise this node is the split point, and that is the answer."

**Brute force:** Find the root-to-p path and the root-to-q path (each a walk down using the BST order) and return the last node the two paths share. O(h) time but O(h) extra space for the two paths. A generic binary-tree LCA (no ordering) is O(n) and ignores the BST property.

**Optimal:**
- Let `lo = min(p, q)`, `hi = max(p, q)`. Loop from the root:
  - `hi < cur.val`: both targets are in the left subtree, move left.
  - `lo > cur.val`: both are in the right subtree, move right.
  - otherwise `lo <= cur.val <= hi`: stop and return `cur.val`.
- Why the stop is correct: if `lo < cur.val < hi`, p and q are in different subtrees, so `cur` is the lowest node having both below it. If `cur.val == lo` or `hi`, `cur` is one of the targets and the other is in its subtree (a node is its own ancestor). Distinct values mean the three cases never overlap.
- Invariant: at every step both p and q lie in the subtree of `cur`, so the answer is `cur` or below it.
- The walk never needs a stack or recursion: O(1) extra space, and it works on a chain of 10^5 nodes.

**Complexity:** Time O(h): one step per level, at most h steps (I verified step count <= h for every ordered pair on every BST shape up to 7 nodes). O(log n) on a balanced BST, O(n) on a chain. Extra space O(1).

**Dry run:** `[6, 2, 8, 0, 4, 7, 9, null, null, 3, 5]`, p = 3, q = 5. lo = 3, hi = 5. At 6: hi = 5 < 6, go left. At 2: lo = 3 > 2, go right. At 4: lo = 3 <= 4 <= hi = 5, stop. Answer 4. For p = 2, q = 8: at 6, 2 <= 6 <= 8, stop immediately: 6. For p = 2, q = 4: at 6 both smaller, left; at 2: 2 <= 2 <= 4, stop: 2.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force: root-to-node paths, last common node ----------
def path_to(root, x):
    out, cur = [], root
    while cur is not None:
        out.append(cur)
        if x == cur.val: return out
        cur = cur.left if x < cur.val else cur.right
    raise ValueError('value not in tree')
def lca_brute(root, p, q):
    a, b, last = path_to(root, p), path_to(root, q), None
    for x, y in zip(a, b):
        if x is y: last = x
        else: break
    return last.val

# ---------- optimal: walk down once ----------
def lca_bst(root, p, q, steps=None):
    lo, hi = (p, q) if p < q else (q, p)
    cur, n = root, 0
    while cur is not None:
        n += 1
        if hi < cur.val:            # both are smaller: go left
            cur = cur.left
        elif lo > cur.val:          # both are larger: go right
            cur = cur.right
        else:                       # lo <= cur.val <= hi: the paths split here (or cur is p or q)
            if steps is not None: steps.append(n)
            return cur.val
    raise ValueError('p or q not in tree')

# ---------- examples ----------
big = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
for arr, p, q in ((big, 2, 8), (big, 2, 4), (big, 3, 5), ([2, 1], 2, 1)):
    print(arr, p, q, '->', lca_bst(build_tree(arr), p, q))

# ---------- cross-check: every BST shape up to 7 nodes (distinct values 0..n-1, labelled by inorder), every pair ----------
def label_in(s, c=None):
    c = c if c is not None else [0]
    if s is None: return None
    L = label_in(s[0], c); v = c[0]; c[0] += 1
    return (v, L, label_in(s[1], c))
def height(t): return 0 if t is None else 1 + max(height(t[1]), height(t[2]))
pairs = 0
for n in range(2, 8):
    for s in shapes(n):
        t = label_in(s); root = from_tuple(t); h = height(t)
        for p in range(n):
            for q in range(n):
                if p == q: continue
                st = []
                got = lca_bst(root, p, q, st)
                assert got == lca_brute(root, p, q)
                assert st[0] <= h                        # at most h loop rounds
                pairs += 1
print('BST shapes up to 7 nodes, all ordered pairs checked:', pairs)

# ---------- random BSTs with non-consecutive values (insert in random order) ----------
def insert(root, v):
    if root is None: return TreeNode(v)
    cur = root
    while True:
        if v < cur.val:
            if cur.left is None: cur.left = TreeNode(v); break
            cur = cur.left
        else:
            if cur.right is None: cur.right = TreeNode(v); break
            cur = cur.right
    return root
random.seed(2)
for _ in range(300):
    vals = random.sample(range(-50, 50), random.randint(2, 30)); root = None
    for v in vals: root = insert(root, v)
    for _ in range(20):
        p, q = random.sample(vals, 2)
        assert lca_bst(root, p, q) == lca_brute(root, p, q)
print('random BSTs ok: 300')

# ---------- edge cases: ancestor of the other, argument order, skewed chain ----------
r = build_tree(big)
assert lca_bst(r, 8, 2) == lca_bst(r, 2, 8) == 6
assert lca_bst(r, 4, 2) == 2 and lca_bst(r, 0, 5) == 2
n = 100_000
chain = None
for v in range(n - 1, -1, -1): chain = TreeNode(v, None, chain)     # 0 -> 1 -> ... right chain
assert lca_bst(chain, n - 1, n - 2) == n - 2 and lca_bst(chain, 0, n - 1) == 0
print('chain of 10^5 handled iteratively; all asserts passed')
```

**Output (my run):**
```
[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5] 2 8 -> 6
[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5] 2 4 -> 2
[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5] 3 5 -> 4
[2, 1] 2 1 -> 2
BST shapes up to 7 nodes, all ordered pairs checked: 23020
random BSTs ok: 300
chain of 10^5 handled iteratively; all asserts passed
```

**Edge cases:**
- One value is an ancestor of the other: the walk stops on the ancestor (`[2, 1]`, p = 2, q = 1 gives 2).
- p > q in the call: handled by the lo/hi swap, so the order of arguments is irrelevant.
- Skewed tree: still O(h) = O(n) time, with no recursion limit problem.
- If a value were missing, the walk could end at None; the prompt guarantees both exist, and my code raises `ValueError` in that case rather than returning a wrong answer.
- This relies on the BST property and distinct values. With duplicates the "go left or right" rule becomes ambiguous.

**Follow-ups:**
- LCA of a plain binary tree? Post-order DFS: return the node when it equals p or q, combine the two child results; O(n). See the binary-tree LCA question later in this part.
- Return the node instead of the value? Same loop, return `cur`.
- Many queries on one tree? For an offline set, binary lifting or Euler tour plus RMQ gives O(log n) or O(1) per query after preprocessing.

**Common mistakes:**
- Using the plain binary-tree DFS and ignoring the BST order (still correct, but O(n) instead of O(h)).
- Using strict inequalities in the stop test, which skips the case where one target is the ancestor.
- Assuming p < q without checking.
- Recursing on a skewed BST (the prompt allows n up to 10^5).

### Q7 ⭐⭐⭐ 🟢 Path sum, root to leaf. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a tree (0 <= n <= 5000, values may be negative) and an integer target, return True if some path from the ROOT down to a LEAF has values summing to the target. A leaf is a node with no children, so a path must end at a leaf (a node with one child is not a leaf), and an empty tree has no path, even for target 0. Write the recursive version (subtract the value on the way down) and an iterative version with a stack of (node, remaining). Example: root=[5, 4, 8, 11, null, 13, 4, 7, 2, null, null, null, 1], target=22 -> True; root=[1, 2, 3], target=5 -> False; root=[1, 2], target=1 -> False; root=[], target=0 -> False; root=[-2, null, -3], target=-5 -> True.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Root-to-leaf DFS carrying a running value down (here the remaining target). The decision is made at the leaves.

**Say this first (1 line):** "Subtract each node's value from the target on the way down; at a leaf, the path works if what is left is exactly 0. A leaf means both children are None, so a node with one child is not a leaf."

**Brute force:** Enumerate every root-to-leaf path as a list, sum each, and test the target. O(n) paths of up to h length each, so O(n * h) time worst case and O(h) per path stored (or O(n * h) if all are stored). The code uses it on tuple trees as the checker.

**Optimal:**
- `has_path(node, rem)`: None returns False (so an empty tree is False even for target 0). Set `rem -= node.val`. If both children are None, return `rem == 0`. Otherwise return `has_path(left, rem) or has_path(right, rem)`.
- Invariant: `rem` is the target minus the sum of the values from the root down to the parent of the current node.
- Do NOT prune when `rem` goes negative or below some bound: values may be negative, so the sum can recover later.
- Do NOT treat `None` as the end of a path. If you return `rem == 0` on None, then `[1, 2]` with target 1 wrongly succeeds, because the missing right child of the root looks like a path of sum 1.
- Iterative: stack of `(node, remaining)`. Pop, subtract, test at a leaf, otherwise push the children with the new remaining value. Both versions short-circuit on the first success.

**Complexity:** Time O(n): each node is visited at most once (and every node is visited when the answer is False). Space O(h) for the call stack or the explicit stack, O(n) on a chain.

**Dry run:** `[1, 2, 3]`, target 5. Root: rem = 4, not a leaf. Left leaf 2: rem = 2, not 0. Right leaf 3: rem = 1, not 0. No path: False. For `[-2, null, -3]`, target -5: root rem = -3 (a pruning rule "stop when rem < 0" would wrongly cut here). Right child -3 is a leaf: rem = -3 - (-3) = 0. True.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

import itertools

# ---------- brute force: list every root-to-leaf path on tuples, sum each ----------
def paths_leaf(t, pre=()):
    if t is None: return []
    p = pre + (t[0],)
    if t[1] is None and t[2] is None: return [p]
    return paths_leaf(t[1], p) + paths_leaf(t[2], p)
def has_path_brute(t, target):
    return any(sum(p) == target for p in paths_leaf(t))

# ---------- optimal 1: recursive, subtract on the way down ----------
def has_path(root, target):
    if root is None:
        return False                                   # empty tree: no path, even for target 0
    rem = target - root.val
    if root.left is None and root.right is None:       # a LEAF: both children missing
        return rem == 0
    return has_path(root.left, rem) or has_path(root.right, rem)

# ---------- optimal 2: iterative, stack of (node, remaining) ----------
def has_path_iter(root, target):
    st = [(root, target)] if root else []
    while st:
        node, rem = st.pop()
        rem -= node.val
        if node.left is None and node.right is None:
            if rem == 0: return True
            continue
        if node.right: st.append((node.right, rem))
        if node.left: st.append((node.left, rem))
    return False

# ---------- examples ----------
ex = [([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22), ([1, 2, 3], 5), ([1, 2], 1), ([], 0), ([-2, None, -3], -5)]
for arr, tg in ex:
    r = build_tree(arr)
    print(arr, tg, '->', has_path(r, tg), has_path_iter(r, tg))

# ---------- cross-check: every shape up to 7 nodes, three labellings (preorder index, negative mix, all ones),
# every target from -12 to 30 ----------
def relabel(t, f, c=None):
    c = c if c is not None else [0]
    if t is None: return None
    v = f(c[0]); c[0] += 1
    L = relabel(t[1], f, c)
    return (v, L, relabel(t[2], f, c))
labellers = (lambda i: i, lambda i: (-1) ** i * (i + 1), lambda i: 1)
cases = 0
for n in range(8):
    for s in shapes(n):
        for f in labellers:
            t = relabel(label_pre(s), f); r = from_tuple(t)
            ps = {sum(p) for p in paths_leaf(t)}
            for target in range(-12, 31):
                exp = target in ps
                assert has_path(r, target) == has_path_iter(r, target) == has_path_brute(t, target) == exp
                cases += 1
print('cases checked:', cases)

# the leaf rule: a node with one child is NOT a leaf
r = build_tree([1, 2])
assert not has_path(r, 1) and has_path(r, 3)       # path must end at 2, not stop at the root
assert not has_path(None, 0) and not has_path_iter(None, 0)
assert has_path(TreeNode(0), 0) and not has_path(TreeNode(0), 1)

random.seed(4)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(-5, 5), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(400):
    t = random_tuple(random.randint(0, 40)); r = from_tuple(t)
    target = random.randint(-15, 15)
    assert has_path(r, target) == has_path_iter(r, target) == has_path_brute(t, target)
print('random ok: 400')

# deep chain: iterative handles 5000 nodes at default depth; recursion is also fine at 5000? check
n = 5000
chain = None
for _ in range(n): chain = TreeNode(1, chain, None)
print('chain of 5000, target 5000 ->', has_path_iter(chain, 5000))
try:
    has_path(chain, 5000)
    print('recursive version also finished')
except RecursionError:
    print('recursive version: RecursionError at depth 5000 (default limit 1000)')
print('all asserts passed')
```

**Output (my run):**
```
[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1] 22 -> True True
[1, 2, 3] 5 -> False False
[1, 2] 1 -> False False
[] 0 -> False False
[-2, None, -3] -5 -> True True
cases checked: 80754
random ok: 400
chain of 5000, target 5000 -> True
recursive version: RecursionError at depth 5000 (default limit 1000)
all asserts passed
```

**Edge cases:**
- Empty tree with target 0: False (no path exists).
- Root with one child: the root is not a leaf, so `[1, 2]` with target 1 is False.
- Single node: True only if its value equals the target.
- Negative values and zero values: never prune on the running sum.
- A chain of 5000 nodes (the prompt allows it): the recursive version raised `RecursionError` in my run at the default limit 1000, while the iterative version answered. So the stack version is the safe one (see Part 4 Q25).
- I checked both versions against the brute force on every shape up to 7 nodes, three value patterns and 43 targets (80,754 cases).

**Follow-ups:**
- Return the paths themselves? DFS with a path list and backtracking (pop after each child): the next question in the family.
- Count downward paths with sum k that need not start at the root? Prefix sums with a hash map, as in Part 1 Q13.
- Does the sum have to end at a leaf in the any-node version? No, that problem allows any downward path; the leaf rule here is what makes this one simpler.

**Common mistakes:**
- Returning `rem == 0` at a None child (accepts paths that stop at an internal node).
- Pruning on `rem < 0` or `rem > target` even though values can be negative.
- Returning True for the empty tree when target is 0.
- Using `and`/`or` on the sums in a way that treats 0 as False (compare to 0 explicitly).

### Q8 ⭐⭐⭐ 🟡 Preorder, inorder and postorder, recursive and iterative. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the three traversals as a triple of value lists (preorder, inorder, postorder) for a tree with 0 <= n <= 10^5 nodes, so a skewed tree must not hit Python's recursion limit (compare Part 4 Q25, recursion limit versus an explicit stack). Write each order recursively first, then iteratively with one explicit stack: preorder with a stack, inorder by pushing the left spine, postorder either by reversing a modified preorder or with a last-visited pointer. State the time and the space of each in terms of n and the height h. Example: root=[1, null, 2, 3] -> ([1, 2, 3], [1, 3, 2], [3, 2, 1]); root=[4, 2, 6, 1, 3, 5, 7] -> ([4, 2, 1, 3, 6, 5, 7], [1, 2, 3, 4, 5, 6, 7], [1, 3, 2, 5, 7, 6, 4]); root=[] -> ([], [], []); root=[1, 2] -> ([1, 2], [2, 1], [2, 1]).
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge) | Python recursion-limit explainers (techinterview.org depth-of-a-tree page, a OneUptime guide, DataCamp DFS tutorial; snippets only, not opened: default limit 1000, raising it risks a crash, explicit stack preferred)

**Pattern:** Depth-first traversal. The three orders differ only in WHEN the node is visited relative to its two subtrees (before, between, after). Iterative versions replace the call stack with an explicit one.

**Say this first (1 line):** "Preorder is node, left, right; inorder is left, node, right; postorder is left, right, node. Recursion is three lines each, but on a 10^5 chain I need an explicit stack because Python stops at about 1000 frames."

**Brute force:** The recursive versions. They are correct and O(n) time (append to one shared list; building the answer with `left + [v] + right` list concatenation would copy lists and cost O(n * h)). Space is O(h) for the call stack, which is O(n) on a skewed tree, and that crashes at the recursion limit.

**Optimal:** One explicit stack per traversal.
- Preorder: push the root. Pop a node, record it, push its right child and then its left (so the left pops first).
- Inorder: keep `cur`. Push the whole left spine; pop one node, record it, move to its right child and repeat. Invariant: the stack holds the ancestors whose own value and right subtree are still waiting.
- Postorder, version A (last-visited pointer): push the left spine, look at the stack top. If it has a right child that is not `last` (the node we just finished), go into that right subtree. Otherwise record the top and pop it, set `last`. The pointer prevents re-entering a finished right subtree forever.
- Postorder, version B: run preorder with the order (node, right, left) by pushing left then right, then reverse the output. Simpler to remember; it uses an O(n) output list in any case.

**Complexity:** All six versions: time O(n), each node is pushed and popped once. Extra space O(h): the recursive call stack, or the explicit stack (the run checked stack <= h on every small shape for inorder). On a chain h = n so O(n). The output list itself is O(n).

**Dry run:** `[1, null, 2, 3]` (1 has right child 2, which has left child 3). Preorder stack: [1] -> record 1, push 2 -> record 2, push 3 -> record 3: `[1, 2, 3]`. Inorder: spine from 1 is [1]; pop 1, record 1, cur = 2; spine [2, 3]; pop 3 record, cur = None; pop 2 record: `[1, 3, 2]`. Postorder: spine [1]; top 1 has right child 2, not yet last, so cur = 2, spine [1, 2, 3]; top 3 has no right child, record 3, last = 3; top 2 has no right child, record 2; top 1: right child 2 is `last`, record 1: `[3, 2, 1]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- recursive (the brute force: simple, but call depth = h) ----------
def pre_rec(root):
    out = []
    def go(n):
        if n is None: return
        out.append(n.val); go(n.left); go(n.right)
    go(root); return out
def in_rec(root):
    out = []
    def go(n):
        if n is None: return
        go(n.left); out.append(n.val); go(n.right)
    go(root); return out
def post_rec(root):
    out = []
    def go(n):
        if n is None: return
        go(n.left); go(n.right); out.append(n.val)
    go(root); return out

# ---------- iterative: one explicit stack each ----------
def pre_iter(root):
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(n.val)
        if n.right: st.append(n.right)          # right first so left pops first
        if n.left: st.append(n.left)
    return out

def in_iter(root, peak=None):
    out, st, cur = [], [], root
    while cur or st:
        while cur:                              # push the whole left spine
            st.append(cur); cur = cur.left
        if peak is not None: peak[0] = max(peak[0], len(st))
        cur = st.pop(); out.append(cur.val)     # visit, then go to the right subtree
        cur = cur.right
    return out

def post_iter(root):                            # last-visited pointer
    out, st, cur, last = [], [], root, None
    while cur or st:
        while cur:
            st.append(cur); cur = cur.left
        top = st[-1]
        if top.right and top.right is not last:  # right subtree not done yet
            cur = top.right
        else:
            out.append(top.val); last = st.pop()
    return out

def post_iter2(root):                           # reverse of (root, right, left)
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(n.val)
        if n.left: st.append(n.left)
        if n.right: st.append(n.right)
    return out[::-1]

def traversals(root):
    return pre_iter(root), in_iter(root), post_iter(root)

# ---------- examples ----------
for arr in ([1, None, 2, 3], [4, 2, 6, 1, 3, 5, 7], [], [1, 2]):
    print(arr, '->', traversals(build_tree(arr)))

# ---------- cross-check on every shape up to 7 nodes (values = preorder labels), plus identity of the tree afterwards ----------
def tpre(t): return [] if t is None else [t[0]] + tpre(t[1]) + tpre(t[2])
def tin(t): return [] if t is None else tin(t[1]) + [t[0]] + tin(t[2])
def tpost(t): return [] if t is None else tpost(t[1]) + tpost(t[2]) + [t[0]]
def height(t): return 0 if t is None else 1 + max(height(t[1]), height(t[2]))
for t in all_trees(7):
    r = from_tuple(t)
    exp = (tpre(t), tin(t), tpost(t))
    assert (pre_rec(r), in_rec(r), post_rec(r)) == exp
    assert traversals(r) == exp and post_iter2(r) == exp[2]
    assert to_tuple(r) == t                                   # traversals do not modify the tree
    pk = [0]; in_iter(r, pk); assert pk[0] <= height(t)       # stack never deeper than h
print('626 shapes: recursive == iterative == tuple brute force; stack <= h')

random.seed(6)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 9), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(400):
    t = random_tuple(random.randint(0, 60)); r = from_tuple(t)
    assert traversals(r) == (tpre(t), tin(t), tpost(t)) and post_iter2(r) == tpost(t)
print('random ok: 400')

# ---------- deep trees: 10^5 nodes, left chain and right chain ----------
n = 100_000
left = right = None
for i in range(n):
    left = TreeNode(i, left, None); right = TreeNode(i, None, right)
for name, r in (('left chain', left), ('right chain', right)):
    p, i_, q = traversals(r)
    assert len(p) == len(i_) == len(q) == n and post_iter2(r) == q
    print(name, 'n = 100000: iterative ok; first values', p[:2], i_[:2], q[:2])
try:
    in_rec(left)
except RecursionError:
    print('recursive inorder: RecursionError on the 10^5 chain (default limit 1000)')

# ---------- edge cases ----------
assert traversals(None) == ([], [], []) and traversals(TreeNode(3)) == ([3], [3], [3])
print('all asserts passed')
```

**Output (my run):**
```
[1, None, 2, 3] -> ([1, 2, 3], [1, 3, 2], [3, 2, 1])
[4, 2, 6, 1, 3, 5, 7] -> ([4, 2, 1, 3, 6, 5, 7], [1, 2, 3, 4, 5, 6, 7], [1, 3, 2, 5, 7, 6, 4])
[] -> ([], [], [])
[1, 2] -> ([1, 2], [2, 1], [2, 1])
626 shapes: recursive == iterative == tuple brute force; stack <= h
random ok: 400
left chain n = 100000: iterative ok; first values [99999, 99998] [0, 1] [0, 1]
right chain n = 100000: iterative ok; first values [99999, 99998] [99999, 99998] [0, 1]
recursive inorder: RecursionError on the 10^5 chain (default limit 1000)
all asserts passed
```

**Edge cases:**
- Empty tree: three empty lists (the stack versions never enter the loop).
- One node: all three give `[v]`.
- Skewed tree: on a left chain of 10^5 nodes preorder and postorder iterative runs are fine; the recursive inorder raised `RecursionError` in my run.
- Postorder version A with `last` compared by identity (`is`), not by value: duplicate values would break a value comparison.
- The traversals do not modify the tree (the run checks the tuple form is unchanged).

**Follow-ups:**
- Can inorder be done in O(1) extra space? Yes, Morris traversal temporarily threads the tree (see the Morris question in this part); it modifies the tree while running.
- Which traversal gives a BST in sorted order? Inorder. Which one lets you delete or free children before the parent? Postorder.
- Does a pair of traversals identify the tree? Preorder with inorder, or inorder with postorder, does (with distinct values); preorder with postorder does not.

**Common mistakes:**
- Pushing the left child before the right in iterative preorder (visits right first).
- In postorder with `last`, forgetting the pointer, which loops forever or visits the right subtree twice.
- Building results with list concatenation inside recursion (O(n * h)).
- Raising `sys.setrecursionlimit` instead of using a stack; very deep recursion can crash the interpreter.

### Q9 ⭐⭐⭐ 🟡 Level-order traversal. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the values level by level, top to bottom, left to right, as a list of lists (0 <= n <= 2000). Use a `collections.deque` and the level-size snapshot idiom (see Part 4 Q30 for the queue idiom), and say why `list.pop(0)` would make the traversal O(n^2) in the worst case. State the maximum queue length for a perfect tree with n = 2^k - 1 nodes. Example: root=[3, 9, 20, null, null, 15, 7] -> [[3], [9, 20], [15, 7]]; root=[1] -> [[1]]; root=[] -> []; root=[1, 2, null, 3] -> [[1], [2], [3]].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Breadth-first search on a tree with a queue. The level-size snapshot (`for _ in range(len(q))`) separates one level from the next.

**Say this first (1 line):** "BFS with a `deque`. At the start of each round the queue holds exactly one level, so I take `len(q)` nodes, collect their values, and enqueue their children for the next round."

**Brute force:** DFS that carries the depth and appends each value to `groups[depth]`. Visiting left before right keeps each level in left-to-right order. Correct, O(n) time, O(n) for the groups plus O(h) recursion. It is a fine cross-check but on a deep tree it needs recursion; the queue version does not.

**Optimal:**
- Put the root on a `deque`. While the queue is not empty: `size = len(q)`, then repeat `size` times: `popleft()`, record the value, append the left then the right child when present. After the loop the collected values are one level.
- Invariant: at the top of each round the queue holds exactly the nodes of one level, left to right, because children are appended in the order their parents were popped.
- Why not `list.pop(0)`: removing the first element shifts every other element, so each pop is O(n) and a wide tree costs O(n^2) in total (a 2000-node tree is small enough to survive, but the habit does not scale). `deque.popleft()` is O(1).
- Why not index tricks on the array form: the array skips the children of nulls, so level boundaries cannot be read from it; do the BFS on nodes (Part 4 Q30 shows the same queue idiom on other inputs).

**Complexity:** Time O(n): each node is enqueued and dequeued once. Space O(w), where w is the widest level (the queue), plus O(n) for the output. For a perfect tree with n = 2^k - 1 nodes the queue peaks at 2^(k-1) = (n + 1) / 2: once the last-but-one level has been fully processed, the queue holds the whole last level. I measured it for k = 1..10 (1, 2, 4, ..., 512). On a chain the queue never holds more than one node.

**Dry run:** `[3, 9, 20, null, null, 15, 7]`. Queue [3]: round 1 pops 3, records [3], pushes 9 and 20. Round 2: size 2, pops 9 (no children) and 20 (pushes 15, 7), records [9, 20]. Round 3: size 2, pops 15 and 7, records [15, 7]. Queue empty: `[[3], [9, 20], [15, 7]]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force: pair each node with its depth by DFS, then group ----------
def levels_brute(t):
    groups = {}
    def go(x, d):
        if x is None: return
        groups.setdefault(d, []).append(x[0])        # left subtree is visited first, so left-to-right order
        go(x[1], d + 1); go(x[2], d + 1)
    go(t, 0)
    return [groups[d] for d in sorted(groups)]

# ---------- optimal: BFS with a deque and a level-size snapshot ----------
def level_order(root, peak=None):
    if root is None:
        return []
    out, q = [], deque([root])
    if peak is not None: peak[0] = 1                 # the root alone is already in the queue
    while q:
        level = []
        for _ in range(len(q)):                      # snapshot: only this level's nodes
            node = q.popleft()                       # O(1); list.pop(0) would be O(n)
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
            if peak is not None: peak[0] = max(peak[0], len(q))
        out.append(level)
    return out

# ---------- examples ----------
for arr in ([3, 9, 20, None, None, 15, 7], [1], [], [1, 2, None, 3]):
    print(arr, '->', level_order(build_tree(arr)))

# ---------- cross-check: all shapes up to 7 nodes, then random trees ----------
for t in all_trees(7):
    r = from_tuple(t)
    assert level_order(r) == levels_brute(t)
    flat = [v for lv in level_order(r) for v in lv]
    assert flat == [x for x in to_level_order(r) if x is not None]      # same order as the canonical array
print('626 shapes ok')
random.seed(8)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 99), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(400):
    t = random_tuple(random.randint(0, 100))
    assert level_order(from_tuple(t)) == levels_brute(t)
print('random ok: 400')

# ---------- maximum queue length on a perfect tree, n = 2^k - 1 ----------
def perfect(k):
    return None if k == 0 else TreeNode(0, perfect(k - 1), perfect(k - 1))
for k in range(1, 11):
    pk = [0]; level_order(perfect(k), pk)
    assert pk[0] == 2 ** (k - 1)
    print('k=%2d n=%4d peak queue %4d  (2^(k-1) = %d, about n/2)' % (k, 2**k - 1, pk[0], 2 ** (k - 1)))

# ---------- edge cases ----------
assert level_order(None) == [] and level_order(TreeNode(7)) == [[7]]
chain = None
for i in range(2000): chain = TreeNode(i, chain, None)
lv = level_order(chain); assert len(lv) == 2000 and all(len(x) == 1 for x in lv)
print('2000-node chain: 2000 levels of one node; all asserts passed')
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> [[3], [9, 20], [15, 7]]
[1] -> [[1]]
[] -> []
[1, 2, None, 3] -> [[1], [2], [3]]
626 shapes ok
random ok: 400
k= 1 n=   1 peak queue    1  (2^(k-1) = 1, about n/2)
k= 2 n=   3 peak queue    2  (2^(k-1) = 2, about n/2)
k= 3 n=   7 peak queue    4  (2^(k-1) = 4, about n/2)
k= 4 n=  15 peak queue    8  (2^(k-1) = 8, about n/2)
k= 5 n=  31 peak queue   16  (2^(k-1) = 16, about n/2)
k= 6 n=  63 peak queue   32  (2^(k-1) = 32, about n/2)
k= 7 n= 127 peak queue   64  (2^(k-1) = 64, about n/2)
k= 8 n= 255 peak queue  128  (2^(k-1) = 128, about n/2)
k= 9 n= 511 peak queue  256  (2^(k-1) = 256, about n/2)
k=10 n=1023 peak queue  512  (2^(k-1) = 512, about n/2)
2000-node chain: 2000 levels of one node; all asserts passed
```

**Edge cases:**
- Empty tree: `[]` (not `[[]]`).
- Single node: `[[v]]`.
- Chain: one value per level, n levels.
- Only a left or only a right child: the `if` guards skip the missing side; never enqueue None (or the next round would crash on `.val`).
- The flattened result equals the canonical level-order array without the null markers; the run asserts this for every small shape.

**Follow-ups:**
- Zigzag order? Same BFS, reverse every other level's list (or use a deque per level and `appendleft`).
- Right-side view? Last value of each level.
- Bottom-up order? Reverse the list of levels at the end.

**Common mistakes:**
- Using `list.pop(0)` (O(n) each).
- Using `len(q)` inside the loop condition without a snapshot, so a level absorbs its children's values.
- Enqueuing None children and then reading `.val`.
- Returning `[[]]` for an empty tree.

### Q10 ⭐⭐⭐ 🟡 Balanced binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). A tree is height-balanced when at EVERY node the heights of the left and right subtrees differ by at most 1 (height of an empty tree is 0). Return True or False for 0 <= n <= 5000. Give the top-down version that recomputes the height at every node, then the single-pass version where each call returns the height or a -1 sentinel for 'unbalanced', and explain why checking only the root's two subtree heights is not enough. Example: root=[3, 9, 20, null, null, 15, 7] -> True; root=[1, 2, 2, 3, 3, null, null, 4, 4] -> False; root=[] -> True; root=[1, 2, null, 3] -> False.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Bottom-up tree recursion that returns a value (the height) and carries a failure signal in the same return (the -1 sentinel), so one pass does the work that two nested passes would.

**Say this first (1 line):** "Balanced must hold at every node, not just the root. Top-down recomputes heights at every node and is O(n * h); the single pass returns the height or -1 and is O(n)."

**Brute force (top-down):** At each node compute `height(left)` and `height(right)` from scratch, test the difference, then recurse into both children. Correct, but each node's height is recomputed once per ancestor that runs a check, so total work is O(n * h): O(n log n) on a balanced tree (my run on a perfect tree of 4095 nodes: 40,962 node visits against 4,095 for the single pass), and it gets worse as the tree gets taller before a failure shows up.

**Optimal (single pass):**
- `check(node)` returns the height of the subtree, or -1 if some node inside it is unbalanced.
- None returns 0. Get `lh`; if it is -1 return -1 right away. Get `rh`; if it is -1 or `abs(lh - rh) > 1` return -1. Otherwise return `1 + max(lh, rh)`.
- Answer is `check(root) != -1`.
- Invariant: a non-negative return is the exact height AND every node inside the subtree is balanced.
- Why the root-only check is wrong: it only compares the two top heights. The tree `[1, 2, 2, 3, null, null, 3, 4, null, null, 4]` has two chains of height 3 under the root (heights equal, difference 0), but each `2` has a child of height 2 on one side and nothing on the other. The run found the smallest counter-example by search: the 6-node tree `[0, 1, 3, null, 2, null, 4, null, null, null, 5]` (the root's heights are 2 and 3, but node 3 has heights 0 and 2). Root-only gave a wrong answer on 552 of the 6918 shapes up to 9 nodes. (The prompt's own example `[1, 2, 2, 3, 3, null, null, 4, 4]` is False even for the root-only check, since its root heights are 3 and 1, so it does not show the trap; the twin-chain tree does.)
- The recursion limit matters here: n can be 5000, and on a 5000-node chain the recursive single pass hit `RecursionError` in my run. The code therefore also has an iterative post-order version with an explicit stack and a dict of heights keyed by `id(node)`. It returns False at the first bad node and is the safe one for deep trees.

**Complexity:** Single pass: each node is visited at most once, so O(n) time (checked: visits <= n on all shapes up to 9 nodes); space O(h) for the call stack (the iterative version uses O(n) for the heights dict). Top-down: O(n * h) time as argued above, same O(h) space.

**Dry run:** `[1, 2, null, 3]` (a left chain of three). check(3) = 1. check(2): lh = 1, rh = 0, difference 1, returns 2. check(1): lh = 2, rh = 0, difference 2 > 1, returns -1. Answer False. For `[3, 9, 20, null, null, 15, 7]`: check(9) = 1, check(15) = 1, check(7) = 1, check(20) = 2, check(3): heights 1 and 2, difference 1, returns 3. True.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force on tuples: definition at every node ----------
def th(t): return 0 if t is None else 1 + max(th(t[1]), th(t[2]))
def balanced_def(t):
    return t is None or (abs(th(t[1]) - th(t[2])) <= 1 and balanced_def(t[1]) and balanced_def(t[2]))

# ---------- top-down: recompute the height at every node (counts node visits made by height) ----------
def height(n, c):
    if n is None: return 0
    c[0] += 1
    return 1 + max(height(n.left, c), height(n.right, c))
def balanced_top_down(root, c=None):
    c = c if c is not None else [0]
    if root is None: return True
    return (abs(height(root.left, c) - height(root.right, c)) <= 1
            and balanced_top_down(root.left, c) and balanced_top_down(root.right, c))

# ---------- single pass: return the height, or -1 as "unbalanced" ----------
def check(n, c):
    if n is None: return 0
    c[0] += 1
    lh = check(n.left, c)
    if lh == -1: return -1
    rh = check(n.right, c)
    if rh == -1 or abs(lh - rh) > 1: return -1
    return 1 + max(lh, rh)
def balanced(root, c=None):
    return check(root, c if c is not None else [0]) != -1

# ---------- single pass, iterative (post-order with an explicit stack): safe for a 5000-node chain ----------
def balanced_iter(root):
    if root is None: return True
    h, st = {}, [(root, False)]                 # h maps id(node) -> height of its subtree
    while st:
        n, done = st.pop()
        if not done:
            st.append((n, True))
            if n.right: st.append((n.right, False))
            if n.left: st.append((n.left, False))
        else:
            lh = h[id(n.left)] if n.left else 0
            rh = h[id(n.right)] if n.right else 0
            if abs(lh - rh) > 1: return False
            h[id(n)] = 1 + max(lh, rh)
    return True

# ---------- wrong: only the root's two heights ----------
def root_only(root):
    c = [0]
    return root is None or abs(height(root.left, c) - height(root.right, c)) <= 1

# ---------- examples ----------
for arr in ([3, 9, 20, None, None, 15, 7], [1, 2, 2, 3, 3, None, None, 4, 4], [], [1, 2, None, 3]):
    r = build_tree(arr)
    print(arr, '->', balanced(r), balanced_top_down(r))

# ---------- cross-check: every shape up to 9 nodes (4862 shapes at n = 9) ----------
total = bad_root = 0; worst_top = worst_one = 0
first_counter = None
for n in range(10):
    for s in shapes(n):
        t = label_pre(s); r = from_tuple(t)
        exp = balanced_def(t)
        c1, c2 = [0], [0]
        assert balanced(r, c1) == balanced_top_down(r, c2) == balanced_iter(r) == exp
        assert c1[0] <= n                                    # single pass: at most one visit per node
        worst_one = max(worst_one, c1[0]); worst_top = max(worst_top, c2[0])
        if root_only(r) != exp:
            bad_root += 1
            if first_counter is None: first_counter = to_level_order(r)
        total += 1
print('shapes checked:', total, '| root-only check wrong on', bad_root, '| smallest counter-example', first_counter)
r = build_tree([1, 2, 2, 3, None, None, 3, 4, None, None, 4])
print('tall twin chains: root heights equal ->', root_only(r), '| balanced ->', balanced(r))
assert root_only(r) and not balanced(r)

# ---------- cost: height recomputation (top-down) versus one pass ----------
def perfect(k): return None if k == 0 else TreeNode(0, perfect(k - 1), perfect(k - 1))
for k in (4, 8, 12):
    c1, c2 = [0], [0]; r = perfect(k)
    assert balanced(r, c1) and balanced_top_down(r, c2)
    print('perfect k=%2d n=%5d: single pass %5d visits, top-down %6d visits (about n*log2(n+1) = %d)' % (k, 2**k - 1, c1[0], c2[0], (2**k - 1) * k))

random.seed(12)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 9), random_tuple(l), random_tuple(n - 1 - l))
def near_balanced(n):                  # split sizes almost evenly so that many trees are balanced
    if n == 0: return None
    l = (n - 1) // 2 + random.choice((0, 0, 0, 1, -1)) if n > 2 else random.randint(0, n - 1)
    l = max(0, min(n - 1, l)); return (0, near_balanced(l), near_balanced(n - 1 - l))
yes = 0
for _ in range(600):
    t = random_tuple(random.randint(0, 40)) if _ % 2 else near_balanced(random.randint(0, 60))
    r = from_tuple(t); e = balanced_def(t); yes += e
    assert balanced(r) == balanced_top_down(r) == balanced_iter(r) == e
print('random ok: 600 (balanced among them: %d)' % yes)

# ---------- edge cases ----------
assert balanced(None) and balanced(TreeNode(1))
assert not balanced(build_tree([1, 2, None, 3]))
chain = None
for _ in range(5000): chain = TreeNode(0, chain, None)          # n = 5000, the prompt's maximum
assert not balanced_iter(chain)
try:
    balanced(chain)
except RecursionError:
    print('recursive single pass: RecursionError on a 5000-node chain (default limit 1000); iterative answers False')
assert balanced_iter(build_tree([1, 2, 3, 4, 5, 6, 7]))
print('all asserts passed')
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> True True
[1, 2, 2, 3, 3, None, None, 4, 4] -> False False
[] -> True True
[1, 2, None, 3] -> False False
shapes checked: 6918 | root-only check wrong on 552 | smallest counter-example [0, 1, 3, None, 2, None, 4, None, None, None, 5]
tall twin chains: root heights equal -> True | balanced -> False
perfect k= 4 n=   15: single pass    15 visits, top-down     34 visits (about n*log2(n+1) = 60)
perfect k= 8 n=  255: single pass   255 visits, top-down   1538 visits (about n*log2(n+1) = 2040)
perfect k=12 n= 4095: single pass  4095 visits, top-down  40962 visits (about n*log2(n+1) = 49140)
random ok: 600 (balanced among them: 98)
recursive single pass: RecursionError on a 5000-node chain (default limit 1000); iterative answers False
all asserts passed
```

**Edge cases:**
- Empty tree: True (height 0).
- Single node: True.
- Difference exactly 1 is allowed; the test is `> 1`.
- Failure deep in one subtree must propagate: the `-1` must be checked before the difference test, or `-1` would be treated as a height.
- Chain of 5000: recursion fails at the default limit; use the iterative version.

**Follow-ups:**
- Why return -1 and not a tuple? A tuple `(balanced, height)` is clearer; -1 saves an allocation. Both are O(n).
- Can the top-down version ever win? On a tree that fails near the root it exits early; but the single pass also exits at the first failure it meets, so there is no reason to prefer it.
- AVL trees? They keep this property with rotations on insert and delete, so the height stays O(log n).

**Common mistakes:**
- Checking only the root's two heights.
- Forgetting to propagate -1 (a child returns -1 and the parent computes `1 + max(...)` from it).
- Treating height difference 1 as failure.
- Using recursion on a 5000-node chain without noting the recursion limit.

### Q11 ⭐⭐⭐ 🟡 Diameter of a binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The diameter is the number of EDGES on the longest path between any two nodes; the path need not pass through the root (0 <= n <= 10^4; an empty tree and a single node both have diameter 0). Compute it in one pass: each call returns the height and updates a running best with left_height + right_height. Explain why the best path through a node is that sum and why you need a nonlocal or a mutable holder, and what goes wrong with the O(n^2) version that recomputes heights. Example: root=[1, 2, 3, 4, 5] -> 3; root=[1, 2] -> 1; root=[1] -> 0; root=[1, null, 2, 3, 4, 5, null, null, 6, 7] -> 5; root=[] -> 0.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Tree DP with a return value plus a side-channel answer. Each call returns the height, and a running best records the answer that "bends" at this node.

**Say this first (1 line):** "The longest path has a topmost node, and through that node it is left height plus right height in edges, so one post-order pass returns heights and keeps the max of that sum."

**Brute force:**
- For every node, compute the height of its left and right subtree from scratch, take `hl + hr`, and recurse into both children for the best.
- Each height call walks a whole subtree. On a chain of n nodes that is n + (n-1) + ... = O(n^2).
- Another brute force: BFS from every node, take the farthest distance. O(n^2) as well. I use it below as an independent check.

**Optimal:**
- `height(node)` returns the number of nodes on the longest downward path (empty = 0). It also does `best = max(best, l + r)`.
- Why `l + r`: any path has one topmost node. If that node is `n`, the path goes down the left side and down the right side. The height `l` (in nodes) of the left child equals the number of edges from `n` down to its deepest left node, and the same for `r`. So the longest path through `n` has `l + r` edges.
- The diameter is the best over all nodes as the top node, so the answer may skip the root.
- `best` is an int, and an inner function that rebinds it needs `nonlocal best` (or a one-element list holder like `best = [0]`). Without it Python makes `best` local and raises `UnboundLocalError`.
- The slow version recomputes heights inside every call, which is the O(n^2) trap.

**Complexity:** Time O(n): every node is visited once and does O(1) work. Space O(h) for the call stack: O(log n) balanced, O(n) on a chain. Slow version: O(n^2) worst case (the run shows n^2 + n height calls on a chain).

**Dry run:** `[1, 2, 3, 4, 5]`. Nodes 4 and 5 are leaves: height 1 each, and `l + r = 0` so best stays 0. At node 2: `l = 1, r = 1`, best = 2, return 2. Node 3 is a leaf: return 1. At root: `l = 2, r = 1`, best = max(2, 3) = 3. Answer 3 (path 4-2-1-3).

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- brute force: recompute heights at every node, O(n^2) on a chain ----------
H_CALLS = 0
def height_slow(n):
    global H_CALLS
    H_CALLS += 1
    return 0 if n is None else 1 + max(height_slow(n.left), height_slow(n.right))

def diameter_slow(root):
    if root is None:
        return 0
    through = height_slow(root.left) + height_slow(root.right)      # edges through this node
    return max(through, diameter_slow(root.left), diameter_slow(root.right))

# ---------- optimal: one pass, return height, update a running best ----------
def diameter(root):
    best = 0
    def height(n):
        nonlocal best                      # rebinding an int needs nonlocal (or a 1-element list)
        if n is None:
            return 0
        l, r = height(n.left), height(n.right)
        best = max(best, l + r)            # best path whose top node is n
        return 1 + max(l, r)
    height(root)
    return best

# ---------- same idea, iterative post-order (safe on a 10^4-node chain) ----------
def diameter_iter(root):
    if root is None:
        return 0
    h, best, st = {}, 0, [(root, False)]   # h: id(node) -> height
    while st:
        n, done = st.pop()
        if not done:
            st.append((n, True))
            for c in (n.left, n.right):
                if c: st.append((c, False))
        else:
            l = h[id(n.left)] if n.left else 0
            r = h[id(n.right)] if n.right else 0
            h[id(n)] = 1 + max(l, r)
            best = max(best, l + r)
    return best

# ---------- independent brute force: longest shortest path over all node pairs ----------
def diameter_pairs(root):
    nodes = all_nodes(root)
    adj = {id(n): [] for n in nodes}
    for n in nodes:
        for c in (n.left, n.right):
            if c:
                adj[id(n)].append(id(c)); adj[id(c)].append(id(n))
    best = 0
    for s in adj:
        dist, q = {s: 0}, deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1; q.append(y)
        best = max(best, max(dist.values()))
    return best

examples = [([1, 2, 3, 4, 5], 3), ([1, 2], 1), ([1], 0),
            ([1, None, 2, 3, 4, 5, None, None, 6, 7], 5), ([], 0)]
for arr, want in examples:
    root = build_tree(arr)
    assert diameter(root) == diameter_iter(root) == diameter_slow(root) == diameter_pairs(root) == want
    print(arr, "->", diameter(root))

# exhaustive: every tree shape with 0..7 nodes (626 shapes)
total = 0
for n in range(8):
    for s in shapes(n):
        root = from_tup(label(s, "pre"))
        want = diameter_pairs(root)
        assert diameter(root) == diameter_iter(root) == diameter_slow(root) == want
        total += 1
print("exhaustive ok:", total, "shapes with 0..7 nodes")

# random bigger trees
random.seed(11)
for _ in range(300):
    arr = [random.randint(0, 9)]
    for _ in range(random.randint(0, 40)):
        arr.append(None if random.random() < 0.35 else random.randint(0, 9))
    root = build_tree(arr)
    assert diameter(root) == diameter_pairs(root)
print("random ok: 300 trees")

# the diameter need not pass through the root: the deep part is on the left
t = build_tree([1, 2, None, 3, 4, 5, None, None, 6])
print("not through the root:", diameter(t), "(root has one child, path is below it)")

# cost of recomputing heights on a chain of n nodes
for n in (50, 100, 200):
    H_CALLS = 0
    diameter_slow(chain(n))
    print("chain n=%d: height_slow calls = %d, n*n = %d" % (n, H_CALLS, n * n))

# deep tree: recursion vs iterative
deep = chain(10000)
print("chain 10000 recursive:", deep_ok(diameter, deep), "| iterative:", diameter_iter(deep))
zig = None
for v in range(5000):                       # zig-zag chain, 5000 nodes
    zig = TreeNode(v, zig, None) if v % 2 else TreeNode(v, None, zig)
print("zig-zag 5000 iterative:", diameter_iter(zig))
```

**Output (my run):**
```
[1, 2, 3, 4, 5] -> 3
[1, 2] -> 1
[1] -> 0
[1, None, 2, 3, 4, 5, None, None, 6, 7] -> 5
[] -> 0
exhaustive ok: 626 shapes with 0..7 nodes
random ok: 300 trees
not through the root: 4 (root has one child, path is below it)
chain n=50: height_slow calls = 2550, n*n = 2500
chain n=100: height_slow calls = 10100, n*n = 10000
chain n=200: height_slow calls = 40200, n*n = 40000
chain 10000 recursive: RecursionError | iterative: 9999
zig-zag 5000 iterative: 4999
```

**Edge cases:**
- Empty tree and single node: 0.
- Two nodes: 1 (edges, not nodes). If the interviewer wants nodes, add 1 for non-empty trees.
- Path not through the root (the run prints one such tree).
- Chain of 10^4 nodes: the recursive version hits the default recursion limit of 1000 and raises `RecursionError`; the iterative post-order is fine.
- Negative or repeated values do not matter, only shape.

**Follow-ups:**
- Diameter in nodes instead of edges? Same code, answer `best + 1` for a non-empty tree.
- Weighted edges or node values (max path sum)? Same shape, return the best downward sum. That is Q17 in this part.
- Avoid recursion? Iterative post-order with a dict of heights keyed by `id(node)`, as in the code.

**Common mistakes:**
- Assuming the path goes through the root.
- Returning the diameter from the recursion instead of the height (the return value and the running best are different things).
- Forgetting `nonlocal`.
- Recomputing heights: O(n^2).
- Counting nodes when the question says edges.

### Q12 ⭐⭐⭐ 🟡 Validate a binary search tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return True if the tree is a valid BST: every node's value is strictly greater than every value in its left subtree and strictly less than every value in its right subtree (so duplicates make it invalid), 0 <= n <= 10^4, values are any integers including the 32-bit minimum and maximum. Give two solutions: pass down (low, high) bounds, and check that an iterative inorder traversal is strictly increasing. Explain why comparing each node only with its parent fails and why sentinels like -2**31 break on boundary values (use None or infinity). Example: root=[2, 1, 3] -> True; root=[5, 1, 4, null, null, 3, 6] -> False; root=[5, 4, 6, null, null, 3, 7] -> False; root=[2, 2, 2] -> False; root=[-2147483648] -> True; root=[] -> True.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Tree recursion with inherited constraints (top-down), or the BST property "inorder is sorted". Same fact, two views.

**Say this first (1 line):** "A node is valid only if it fits the open interval (low, high) set by ALL its ancestors, so I pass the bounds down, using None for 'no bound'. Or I run an inorder walk and check it is strictly increasing."

**Brute force:**
- For every node, scan its whole left subtree (all values must be smaller) and right subtree (all larger).
- Correct, but each node scans its subtree: O(n^2) on a chain. I use it below as the oracle.

**Optimal:**
- Bounds: `ok(node, low, high)`. A None node is fine. Otherwise `low < node.val < high` must hold. Go left with `(low, node.val)` and right with `(node.val, high)`.
- Invariant: every value in the subtree must lie strictly between `low` and `high`. Going left, the parent becomes the new upper bound but the lower bound from further up is kept, so a deep node is checked against every ancestor.
- Inorder: iterative stack walk, keep the previous value, fail if `cur <= prev`. The `<=` is what makes duplicates invalid.
- Why parent-only fails: `[5, 4, 6, null, null, 3, 7]`. Node 6 is a valid right child of 5, and 3 is a valid left child of 6, but 3 sits in the right subtree of 5, so it must be greater than 5.
- Why sentinels like `-2**31` fail: the tree `[-2147483648]` is valid but `val <= low` rejects it. Use None (or `float("-inf")`, which compares with ints fine).

**Complexity:** Time O(n), each node once. Space O(h) for the recursion or the stack: O(log n) balanced, O(n) on a chain.

**Dry run:** `[5, 1, 4, null, null, 3, 6]`. Root 5 with bounds (None, None): ok. Left child 1 with (None, 5): ok. Right child 4 with (5, None): `4 <= 5` so False. Answer False, found at the first right-subtree node, before ever looking at 3 and 6.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- brute force: compare every node with ALL nodes of its two subtrees ----------
def is_bst_brute(root):
    for n in all_nodes(root):
        if any(x.val >= n.val for x in all_nodes(n.left)):
            return False
        if any(x.val <= n.val for x in all_nodes(n.right)):
            return False
    return True

# ---------- optimal 1: pass (low, high) bounds down; None means "no bound" ----------
def is_bst_bounds(root):
    def ok(n, low, high):
        if n is None:
            return True
        if (low is not None and n.val <= low) or (high is not None and n.val >= high):
            return False
        return ok(n.left, low, n.val) and ok(n.right, n.val, high)
    return ok(root, None, None)

# ---------- optimal 2: iterative inorder must be strictly increasing ----------
def is_bst_inorder(root):
    st, cur, prev = [], root, None
    while cur or st:
        while cur:
            st.append(cur); cur = cur.left
        cur = st.pop()
        if prev is not None and cur.val <= prev:      # <= makes duplicates invalid
            return False
        prev, cur = cur.val, cur.right
    return True

# ---------- the classic wrong answers ----------
def is_bst_parent_only(root):                         # compares a node only with its children
    if root is None: return True
    if root.left and root.left.val >= root.val: return False
    if root.right and root.right.val <= root.val: return False
    return is_bst_parent_only(root.left) and is_bst_parent_only(root.right)

def is_bst_sentinel(root, lo=-2**31, hi=2**31 - 1):   # fake "infinity" breaks on the extremes
    if root is None: return True
    if root.val <= lo or root.val >= hi: return False
    return is_bst_sentinel(root.left, lo, root.val) and is_bst_sentinel(root.right, root.val, hi)

examples = [([2, 1, 3], True), ([5, 1, 4, None, None, 3, 6], False),
            ([5, 4, 6, None, None, 3, 7], False), ([2, 2, 2], False),
            ([-2147483648], True), ([], True)]
for arr, want in examples:
    root = build_tree(arr)
    assert is_bst_bounds(root) == is_bst_inorder(root) == is_bst_brute(root) == want
    print(arr, "->", is_bst_bounds(root))

# wrong versions fail exactly where the prompt says
t = build_tree([5, 4, 6, None, None, 3, 7])
print("parent-only on [5,4,6,null,null,3,7]:", is_bst_parent_only(t), "(wrong, 3 sits right of 5)")
print("sentinel on [-2147483648]:", is_bst_sentinel(build_tree([-2147483648])), "(wrong, should be True)")
print("sentinel on [2147483647]:", is_bst_sentinel(build_tree([2147483647])), "(wrong, should be True)")
for arr in ([2147483647], [-2147483648, None, 2147483647], [2147483647, 2147483647]):
    r = build_tree(arr)
    assert is_bst_bounds(r) == is_bst_inorder(r) == is_bst_brute(r)
    print("None bounds on", arr, "->", is_bst_bounds(r))

# exhaustive: all shapes with 0..5 nodes, every labelling with values from {0,1,2}
count = valid = 0
for n in range(6):
    for s in shapes(n):
        for vals in __import__("itertools").product(range(3), repeat=n):
            it = iter(vals)
            def put(sh):
                return None if sh is None else (next(it), put(sh[0]), put(sh[1]))
            root = from_tup(put(s))                    # preorder labelling
            b = is_bst_brute(root)
            assert is_bst_bounds(root) == is_bst_inorder(root) == b
            count += 1; valid += b
print("exhaustive ok:", count, "labelled trees, of which", valid, "are valid BSTs")

# inorder-labelled shapes up to 7 nodes are always BSTs; swapping two labels breaks it
for n in range(8):
    for s in shapes(n):
        root = from_tup(label(s, "in"))
        assert is_bst_bounds(root) and is_bst_inorder(root)
        if n >= 2:
            ns = all_nodes(root)
            for i in range(n):
                for j in range(i + 1, n):
                    ns[i].val, ns[j].val = ns[j].val, ns[i].val
                    assert is_bst_bounds(root) == is_bst_inorder(root) == is_bst_brute(root) == False
                    ns[i].val, ns[j].val = ns[j].val, ns[i].val
print("inorder-labelled shapes 0..7 are BSTs; every swap of two values is caught")

# random trees, wide integer range including the 32-bit extremes
random.seed(12)
pool = [-2**31, -5, 0, 3, 8, 2**31 - 1]
for _ in range(2000):
    arr = [random.choice(pool)]
    for _ in range(random.randint(0, 12)):
        arr.append(None if random.random() < 0.3 else random.choice(pool))
    r = build_tree(arr)
    assert is_bst_bounds(r) == is_bst_inorder(r) == is_bst_brute(r)
print("random ok: 2000 trees")

# deep chain of 5000 ascending values: inorder version is iterative
deep = chain(5000)
print("chain 5000 inorder:", is_bst_inorder(deep), "| bounds recursive:", deep_ok(is_bst_bounds, deep))
```

**Output (my run):**
```
[2, 1, 3] -> True
[5, 1, 4, None, None, 3, 6] -> False
[5, 4, 6, None, None, 3, 7] -> False
[2, 2, 2] -> False
[-2147483648] -> True
[] -> True
parent-only on [5,4,6,null,null,3,7]: True (wrong, 3 sits right of 5)
sentinel on [-2147483648]: False (wrong, should be True)
sentinel on [2147483647]: False (wrong, should be True)
None bounds on [2147483647] -> True
None bounds on [-2147483648, None, 2147483647] -> True
None bounds on [2147483647, 2147483647] -> False
exhaustive ok: 11497 labelled trees, of which 15 are valid BSTs
inorder-labelled shapes 0..7 are BSTs; every swap of two values is caught
random ok: 2000 trees
chain 5000 inorder: True | bounds recursive: RecursionError
```

**Edge cases:**
- Empty tree: True. Single node: True, even `-2**31`.
- Duplicates anywhere: False (strict on both sides), including `[2, 2, 2]` and a duplicate far below.
- Extremes `-2**31` and `2**31 - 1`: use None bounds, not sentinels.
- A chain of 5000 nodes: recursive bounds hits `RecursionError` at the default limit of 1000; use the iterative inorder (or an explicit stack of `(node, low, high)`).

**Follow-ups:**
- Allow duplicates on the left only? Say the rule out loud first, then make the bound inclusive on that side only: the left-going `high` rejects `val > high` instead of `val >= high`, and the right side stays strict.
- Which is better? Same big-O. Inorder is shorter to write iteratively and stops early; bounds also generalises to "each node must lie in a range".
- Why is checking only inorder sortedness enough? A tree is a BST exactly when its inorder sequence is strictly increasing, and the code tests that directly.

**Common mistakes:**
- Comparing each node only with its parent.
- Using `<` where `<=` is needed (accepting duplicates).
- Sentinels `-2**31` and `2**31 - 1`.
- Starting an inorder `prev` at 0 or a sentinel instead of None.

### Q13 ⭐⭐⭐ 🟡 Lowest common ancestor of a binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is an ordinary binary tree with DISTINCT values, 2 <= n <= 10^5 nodes; p and q are two different values that both exist. Return the value of their lowest common ancestor (a node may be its own descendant). Give the recursive post-order solution (return the node if it matches, else combine the two child results), explain why returning early at a match is correct when both nodes exist, and say what changes if either value may be missing (a second pass or counting found nodes). Example: root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], p=5, q=1 -> 3; root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], p=5, q=4 -> 5; root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], p=6, q=4 -> 5; root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], p=7, q=8 -> 3; root=[1, 2], p=1, q=2 -> 1.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Post-order combine on a binary tree (no ordering to exploit, so the answer has to be found by looking at both sides).

**Say this first (1 line):** "Recurse on both children. A call returns its node if it matches p or q, otherwise whatever the children found. The first node where both sides report a hit is the LCA."

**Brute force:**
- Find the root-to-p path and the root-to-q path (store the nodes), then walk both from the root and keep the last node they share.
- O(n) time and O(n) space for the paths. Perfectly fine, but two passes and extra memory. I use it as the oracle.

**Optimal:**
- `go(n)`: if `n` is None or matches p or q, return `n`. Otherwise `l = go(left)`, `r = go(right)`.
- If both `l` and `r` are non-None, p and q are on different sides, so `n` is the LCA. Else return whichever is non-None (or None).
- Why returning early at a match is correct when both values exist: when `go` reaches p, either q is below p (so p is the LCA, and nothing below p needs checking), or q is somewhere else and will be reported by another branch, so a higher node sees two hits. Either way the right node wins.
- If a value may be missing: that argument breaks. With q absent, the early return hands back p's node as if it were an LCA. Fix: visit both children before testing the node and count matches. Return the answer only if the count is 2 (or do a second pass to confirm both exist). The code has `lca_safe`.

**Complexity:** Time O(n), each node once. Space O(h) recursion: O(log n) balanced, O(n) on a chain. The parent-map version is O(n) time and space but iterative.

**Dry run:** `[3,5,1,6,2,0,8,null,null,7,4]`, p=6, q=4. At 3: go(5) and go(1). At 5: go(6) matches, returns 6. go(2): go(7) none, go(4) matches, returns 4, so 2 returns 4. At 5: both sides hit, return 5. At 1: nothing found, None. At 3: left is 5, right is None, return 5. Answer 5.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- brute force: root-to-node paths, longest common prefix ----------
def path_to(root, val):
    st = [(root, [root])]
    while st:
        n, p = st.pop()
        if n.val == val:
            return p
        for c in (n.left, n.right):
            if c: st.append((c, p + [c]))
    return None

def lca_brute(root, p, q):
    a, b = path_to(root, p), path_to(root, q)
    if a is None or b is None:
        return None
    last = None
    for x, y in zip(a, b):
        if x is not y: break
        last = x
    return last

# ---------- optimal: post-order, return the node if it matches, else combine ----------
def lca(root, p, q):
    def go(n):
        if n is None or n.val == p or n.val == q:
            return n                      # early return: see "why" below
        l, r = go(n.left), go(n.right)
        if l and r:
            return n                      # p and q are on different sides
        return l or r
    return go(root)

# ---------- safe version when a value may be missing: count the matches seen ----------
def lca_safe(root, p, q):
    found = 0
    def go(n):
        nonlocal found
        if n is None:
            return None
        l, r = go(n.left), go(n.right)    # visit BOTH sides first, so we never skip a match
        if n.val == p or n.val == q:
            found += 1
            return n
        return n if (l and r) else (l or r)
    ans = go(root)
    return ans if found == 2 else None

# ---------- iterative with a parent map (safe on deep trees) ----------
def lca_parent(root, p, q):
    parent, st, byval = {id(root): None}, [root], {}
    while st:
        n = st.pop(); byval[n.val] = n
        for c in (n.left, n.right):
            if c:
                parent[id(c)] = n; st.append(c)
    a, anc = byval[p], set()
    while a:
        anc.add(id(a)); a = parent[id(a)]
    b = byval[q]
    while id(b) not in anc:
        b = parent[id(b)]
    return b

T = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
examples = [(T, 5, 1, 3), (T, 5, 4, 5), (T, 6, 4, 5), (T, 7, 8, 3), ([1, 2], 1, 2, 1)]
for arr, p, q, want in examples:
    root = build_tree(arr)
    got = lca(root, p, q)
    assert got.val == want and got is lca_brute(root, p, q) is lca_parent(root, p, q) is lca_safe(root, p, q)
    print("p=%d q=%d -> %d" % (p, q, got.val))

# exhaustive: every shape with 2..7 nodes (distinct preorder labels), every ordered pair p != q
pairs = 0
for n in range(2, 8):
    for s in shapes(n):
        root = from_tup(label(s, "pre"))
        for p in range(n):
            for q in range(n):
                if p != q:
                    w = lca_brute(root, p, q)
                    assert lca(root, p, q) is w and lca_safe(root, p, q) is w and lca_parent(root, p, q) is w
                    pairs += 1
print("exhaustive ok:", pairs, "(tree, p, q) cases, all shapes with 2..7 nodes")

# one value missing: the early-return version is fooled, the counting version is not
fooled = safe_none = cases = 0
for n in range(1, 8):
    for s in shapes(n):
        root = from_tup(label(s, "pre"))
        for p in range(n):
            cases += 1
            fooled += lca(root, p, 99) is not None      # returns p's node although 99 is absent
            safe_none += lca_safe(root, p, 99) is None
print("missing q: early-return answered for", fooled, "of", cases, "| counting version returned None for", safe_none, "of", cases)

# random larger trees with distinct values
random.seed(13)
for _ in range(300):
    n = random.randint(2, 60)
    vals = random.sample(range(1000), n)
    arr = [vals[0]]; slots = 2; k = 1
    while k < n:                                   # random level-order fill, some Nones
        if random.random() < 0.3 and slots > 1:
            arr.append(None)
        else:
            arr.append(vals[k]); k += 1; slots += 1
        slots -= 1
    root = build_tree(arr)
    ns = all_nodes(root)
    if len(ns) < 2: continue
    p, q = random.sample([x.val for x in ns], 2)
    assert lca(root, p, q) is lca_brute(root, p, q) is lca_parent(root, p, q)
print("random ok: 300 trees up to 60 nodes")

deep = chain(20000)
r = deep_ok(lca, deep, 19999, 20000)               # both values sit at the bottom
print("chain 20000 recursive:", r if isinstance(r, str) else r.val, "| parent-map:", lca_parent(deep, 19999, 20000).val)
```

**Output (my run):**
```
p=5 q=1 -> 3
p=5 q=4 -> 5
p=6 q=4 -> 5
p=7 q=8 -> 3
p=1 q=2 -> 1
exhaustive ok: 23020 (tree, p, q) cases, all shapes with 2..7 nodes
missing q: early-return answered for 4081 of 4081 | counting version returned None for 4081 of 4081
random ok: 300 trees up to 60 nodes
chain 20000 recursive: RecursionError | parent-map: 19999
```

**Edge cases:**
- p is an ancestor of q: the early return gives p (the examples `p=5, q=4` and `[1, 2]`).
- p and q at the deepest level on a chain of 20000 nodes: recursion raises `RecursionError`; the parent-map version is iterative and fine.
- Missing value: the run shows the early-return version "answers" in every one of the 4081 cases where q is absent, while the counting version returns None each time.
- Values are distinct per the prompt. With duplicate values you would match by node reference, not by value.

**Follow-ups:**
- It is a BST? Use the ordering and go left or right, O(h) with no full traversal. That is Q6 in this part: the LCA is the first node whose value lies between p and q.
- Many LCA queries on one tree? Preprocess with Euler tour plus sparse table or binary lifting; each query becomes O(1) or O(log n).
- Do it without recursion? Build a parent map (as in the code), mark p's ancestors in a set, then climb from q.

**Common mistakes:**
- Comparing `n.val == p` without handling None first.
- Trusting the early-return version when a value can be absent.
- Returning a value instead of a node from the helper, then being unable to tell "found nothing" from "found value 0".
- Treating "a node is its own descendant" wrongly: the LCA of 5 and 4 where 5 is above 4 is 5, not 3.

### Q14 ⭐⭐⭐ 🟡 Right side view. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Imagine standing to the right of the tree: return the values you can see, top to bottom, which is the last node of every level (0 <= n <= 10^4). Give the BFS version (the last node of each level) and the DFS version (visit right before left and record the first node seen at each new depth), and say why the DFS answer is not simply the right spine. Example: root=[1, 2, 3, null, 5, null, 4] -> [1, 3, 4]; root=[1, 2, 3, 4] -> [1, 3, 4]; root=[1, null, 3] -> [1, 3]; root=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Level-order traversal (BFS), or depth-first with a depth counter and "first to reach a depth wins".

**Say this first (1 line):** "The right view is the last node of every level. BFS gives it directly. DFS also works if I go right first and record the first node I meet at each new depth."

**Brute force:**
- Collect every level into a list of lists, then take the last element of each. O(n) time, O(n) extra space for the stored levels. It works, it just stores more than needed.
- My independent check gives every node a heap-style index (root 1, children `2i` and `2i+1`) and keeps the largest index per depth.

**Optimal:**
- BFS: at the start of each round the queue holds exactly one level. Its last element, `q[-1]`, is the visible node. Then pop the `len(q)` nodes of that level and push their children.
- DFS: `go(node, depth)`. If `depth == len(out)`, this is the first node at that depth, and because we visit right before left it is the rightmost one, so append it. Then recurse right, then left.
- Why not just the right spine: the view shows a left-side node whenever the right side is shorter. In `[1, 2, 3, 4]`, node 4 is the only node at depth 2 (3 has no children), so it is visible even though it hangs on the left. The spine gives `[1, 3]`, the view is `[1, 3, 4]`.

**Complexity:** Time O(n) both ways. Space: BFS O(w) (the widest level, up to n/2). DFS O(h) (n on a chain, log n balanced). Pick DFS on a wide shallow tree, BFS on a tall thin one.

**Dry run:** `[1, 2, 3, null, 5, null, 4]`. Level 0 queue `[1]`: last is 1. Level 1 queue `[2, 3]`: last is 3. Level 2 queue `[5, 4]` (children of 2 then 3): last is 4. Answer `[1, 3, 4]`. DFS: depth 0 sees 1, goes right to 3 (depth 1, new, record), goes right to 4 (depth 2, new, record), back up, then 3's left is None, then 2 at depth 1 (already recorded), then 5 at depth 2 (already recorded).

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- BFS: the last node of every level ----------
def right_view_bfs(root):
    out, q = [], deque([root] if root else [])
    while q:
        out.append(q[-1].val)                       # rightmost node of this level
        for _ in range(len(q)):
            n = q.popleft()
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
    return out

# ---------- DFS: visit right before left, record the FIRST node seen at each depth ----------
def right_view_dfs(root):
    out = []
    def go(n, d):
        if n is None:
            return
        if d == len(out):                           # first time we reach this depth
            out.append(n.val)
        go(n.right, d + 1)
        go(n.left, d + 1)
    go(root, 0)
    return out

def right_view_dfs_iter(root):                      # same order with an explicit stack
    out, st = [], ([(root, 0)] if root else [])
    while st:
        n, d = st.pop()
        if d == len(out):
            out.append(n.val)
        if n.left: st.append((n.left, d + 1))       # pushed first, so popped last
        if n.right: st.append((n.right, d + 1))
    return out

# ---------- the wrong idea: just follow right pointers ----------
def right_spine(root):
    out = []
    while root:
        out.append(root.val); root = root.right
    return out

# ---------- independent brute force: heap-style index of every node, max index per depth ----------
def right_view_brute(t):
    best = {}
    def go(t, d, idx):
        if t is None: return
        if d not in best or idx > best[d][0]:
            best[d] = (idx, t[0])
        go(t[1], d + 1, 2 * idx); go(t[2], d + 1, 2 * idx + 1)
    go(t, 0, 1)
    return [best[d][1] for d in sorted(best)]

examples = [([1, 2, 3, None, 5, None, 4], [1, 3, 4]), ([1, 2, 3, 4], [1, 3, 4]),
            ([1, None, 3], [1, 3]), ([], [])]
for arr, want in examples:
    r = build_tree(arr)
    assert right_view_bfs(r) == right_view_dfs(r) == right_view_dfs_iter(r) == want
    print(arr, "->", right_view_bfs(r))
r = build_tree([1, 2, 3, 4])
print("right spine of [1,2,3,4]:", right_spine(r), "but the right view is", right_view_bfs(r))

def r_height(r):                                   # view length must equal the height
    h, lvl = 0, [r] if r else []
    while lvl:
        h += 1; lvl = [c for x in lvl for c in (x.left, x.right) if c]
    return h

total = 0
for n in range(8):
    for s in shapes(n):
        t = label(s, "pre"); r = from_tup(t)
        want = right_view_brute(t)
        assert right_view_bfs(r) == right_view_dfs(r) == right_view_dfs_iter(r) == want
        assert len(want) == (0 if n == 0 else r_height(r))
        total += 1
print("exhaustive ok:", total, "shapes with 0..7 nodes")

random.seed(14)
for _ in range(300):
    arr = [random.randint(0, 99)]
    for _ in range(random.randint(0, 40)):
        arr.append(None if random.random() < 0.4 else random.randint(0, 99))
    r = build_tree(arr)
    assert right_view_bfs(r) == right_view_dfs(r) == right_view_dfs_iter(r)
print("random ok: 300 trees (repeated values allowed)")

deep = chain(10000, "left")                          # left chain: every node is visible
res = deep_ok(right_view_dfs, deep)
print("left chain 10000: BFS view length", len(right_view_bfs(deep)), "| recursive DFS:", res if isinstance(res, str) else len(res),
      "| iterative DFS length", len(right_view_dfs_iter(deep)))
```

**Output (my run):**
```
[1, 2, 3, None, 5, None, 4] -> [1, 3, 4]
[1, 2, 3, 4] -> [1, 3, 4]
[1, None, 3] -> [1, 3]
[] -> []
right spine of [1,2,3,4]: [1, 3] but the right view is [1, 3, 4]
exhaustive ok: 626 shapes with 0..7 nodes
random ok: 300 trees (repeated values allowed)
left chain 10000: BFS view length 10000 | recursive DFS: RecursionError | iterative DFS length 10000
```

**Edge cases:**
- Empty tree: `[]`.
- Left-only chain: every node is visible, so the answer is the whole chain (10^4 nodes: recursive DFS hits `RecursionError` under the default limit; BFS and the explicit-stack DFS are fine).
- Repeated values: no problem, we record nodes by level, not by value.
- A left subtree deeper than the right: its extra levels show through (`[1, 2, 3, 4]`).

**Follow-ups:**
- Left side view? Same code with left first (BFS: `q[0]`).
- Both views, or the full vertical view? That is the vertical order question (Q28).
- Why does DFS need the depth check? Without it you would append every node.

**Common mistakes:**
- Following only `.right` pointers.
- Reading `q[-1]` after popping the level instead of before.
- Forgetting that DFS must go right first.
- Looping `while q` for the level instead of `range(len(q))`, which mixes levels together.

### Q15 ⭐⭐⭐ 🟡 Kth smallest in a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a valid BST with distinct values (1 <= k <= n <= 10^4), return the k-th smallest value. Use an iterative inorder traversal that stops after k pops: O(h + k) time, O(h) space. Then answer the follow-up: the tree is modified often and k-th queries are frequent, so what extra field per node (the size of its subtree) gives O(h) per query, and what does each insert or delete have to maintain? Example: root=[3, 1, 4, null, 2], k=1 -> 1; root=[5, 3, 6, 2, 4, null, null, 1], k=3 -> 3; root=[5, 3, 6, 2, 4, null, null, 1], k=6 -> 6; root=[1], k=1 -> 1.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Inorder traversal of a BST visits values in sorted order, so the k-th smallest is the k-th node visited. Stop early.

**Say this first (1 line):** "Inorder of a BST is sorted, so I walk inorder with an explicit stack and return on the k-th pop. That is O(h + k) time and O(h) space."

**Brute force:** Do a full inorder walk into a list and return `list[k - 1]`. O(n) time and O(n) space. Even simpler and worse: dump all values and sort, O(n log n).

**Optimal:**
- Push the left spine, pop a node (that is the next smallest), count it, then move to its right child and push that child's left spine.
- Return the moment the count reaches k. Nothing after the k-th node is ever touched.
- The stack only ever holds the ancestors of the current node, so at most h nodes. Pushes are at most `k + h - 1`: every popped node was pushed, and fewer than h are left on the stack.
- Follow-up (frequent queries on a changing tree): store `size` (nodes in the subtree) in each node. At node n with `left = size(n.left)`: if `k == left + 1` the answer is n; if `k <= left` go left; else `k -= left + 1` and go right. That is O(h) per query. Every insert or delete must add or subtract 1 on every ancestor on the path (O(h) extra work), and rotations in a balanced tree must recompute the sizes of the two nodes they move.

**Complexity:** Time O(h + k): at most h pushes to reach the first node, then k pops. Space O(h). With sizes: O(h) per query, O(h) per update, O(n) extra space for the size field. In a balanced tree h is O(log n); on a chain it is n.

**Dry run:** `[5, 3, 6, 2, 4, null, null, 1]`, k=3. Push 5, 3, 2, 1 (stack `[5,3,2,1]`). Pop 1, k=2 left. 1 has no right. Pop 2, k=1. 2 has no right child. Pop 3, k=0, return 3. We never touched 4 or 6.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- brute force: full inorder list, index k - 1 ----------
def kth_brute(root, k):
    out, st, cur = [], [], root
    while cur or st:
        while cur:
            st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out[k - 1]

# ---------- optimal: iterative inorder, stop after k pops ----------
STATS = {"pops": 0, "pushes": 0, "max_stack": 0}
def kth_smallest(root, k):
    st, cur = [], root
    while cur or st:
        while cur:
            st.append(cur); STATS["pushes"] += 1
            STATS["max_stack"] = max(STATS["max_stack"], len(st))
            cur = cur.left
        cur = st.pop(); STATS["pops"] += 1
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
    raise ValueError("k larger than n")

# ---------- follow-up: store subtree sizes (dict id -> size here; a real node would carry a field) ----------
def build_sizes(root):
    size = {}
    for n in reversed(all_nodes(root)):             # children come after parents in preorder, so reversed = children first
        size[id(n)] = 1 + (size[id(n.left)] if n.left else 0) + (size[id(n.right)] if n.right else 0)
    return size

def kth_by_size(root, k, size):                     # O(h) per query, no traversal
    n = root
    while n:
        left = size[id(n.left)] if n.left else 0
        if k == left + 1: return n.val
        if k <= left: n = n.left
        else: k -= left + 1; n = n.right
    raise ValueError("k larger than n")

def insert_with_size(root, val, size):              # an insert must bump the size of every ancestor
    nd = TreeNode(val); size[id(nd)] = 1
    if root is None: return nd
    cur = root
    while True:
        size[id(cur)] += 1
        side = "left" if val < cur.val else "right"
        nxt = getattr(cur, side)
        if nxt is None:
            setattr(cur, side, nd); return root
        cur = nxt

def height(root):
    h, lvl = 0, [root] if root else []
    while lvl:
        h += 1; lvl = [c for x in lvl for c in (x.left, x.right) if c]
    return h

examples = [([3, 1, 4, None, 2], 1, 1), ([5, 3, 6, 2, 4, None, None, 1], 3, 3),
            ([5, 3, 6, 2, 4, None, None, 1], 6, 6), ([1], 1, 1)]
for arr, k, want in examples:
    r = build_tree(arr); sz = build_sizes(r)
    assert kth_smallest(r, k) == kth_brute(r, k) == kth_by_size(r, k, sz) == want
    print(arr, "k=%d ->" % k, want)

# exhaustive: every BST shape with 1..7 nodes (inorder labels 0..n-1), every k
cases = 0
for n in range(1, 8):
    for s in shapes(n):
        r = from_tup(label(s, "in")); sz = build_sizes(r); h = height(r)
        for k in range(1, n + 1):
            STATS.update(pops=0, pushes=0, max_stack=0)
            assert kth_smallest(r, k) == kth_by_size(r, k, sz) == kth_brute(r, k) == k - 1
            assert STATS["pops"] == k                           # stops right after the k-th pop
            assert STATS["max_stack"] <= h                      # never more than h nodes on the stack
            assert STATS["pushes"] <= k + h - 1                  # pushes = pops + what is left on the stack (< h)
            cases += 1
print("exhaustive ok:", cases, "(BST, k) cases; pops == k and stack <= h every time")

# random BSTs by inserting random distinct keys; sizes maintained under inserts
random.seed(15)
for _ in range(200):
    keys = random.sample(range(-500, 500), random.randint(1, 80))
    root, sz = None, {}
    for key in keys:
        root = insert_with_size(root, key, sz)
        srt = sorted(keys[:keys.index(key) + 1])
        k = random.randint(1, len(srt))
        assert kth_by_size(root, k, sz) == srt[k - 1] == kth_smallest(root, k)
    assert sz == build_sizes(root)                              # incremental sizes match a fresh rebuild
print("random ok: 200 BSTs, sizes kept correct across inserts")

# deep chain: iterative walk copes where recursion would not
deep = chain(10000)
print("chain 10000, k=10000 ->", kth_smallest(deep, 10000), "| k=1 ->", kth_smallest(deep, 1))
```

**Output (my run):**
```
[3, 1, 4, None, 2] k=1 -> 1
[5, 3, 6, 2, 4, None, None, 1] k=3 -> 3
[5, 3, 6, 2, 4, None, None, 1] k=6 -> 6
[1] k=1 -> 1
exhaustive ok: 4081 (BST, k) cases; pops == k and stack <= h every time
random ok: 200 BSTs, sizes kept correct across inserts
chain 10000, k=10000 -> 10000 | k=1 -> 1
```

**Edge cases:**
- k = 1: the leftmost node. k = n: the rightmost, the walk visits the whole tree.
- One node.
- Chain of 10^4 nodes: the iterative walk is fine (a recursive walk would raise `RecursionError`).
- Duplicates are excluded by the prompt. With duplicates you would count occurrences and need a clear rule.
- k out of range: the code raises `ValueError` instead of returning garbage.

**Follow-ups:**
- Many queries, tree changes often: size field as above, O(h) per query and update.
- Tree never changes, many queries? Store the sorted inorder array once, then each query is O(1).
- k-th largest? Mirror the walk (right first), or ask for the `(n - k + 1)`-th smallest if you know n.

**Common mistakes:**
- A recursive walk that collects everything and then indexes (O(n) when O(h + k) is possible).
- Off-by-one: decrementing k before or after the check.
- Not restoring `cur = cur.right` after a pop, so the walk loops or skips a subtree.
- Forgetting to update the size of every ancestor on insert and delete.

### Q16 ⭐⭐⭐ 🟡 Build a tree from preorder and inorder. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given the preorder and inorder traversals of a binary tree with DISTINCT values (1 <= n <= 3000), rebuild the tree and return it. Use a dict from value to inorder index and a moving preorder pointer for O(n); explain why slicing the lists and calling `list.index` is O(n^2). Explain why the pair identifies the tree uniquely (the root is the first preorder value, which splits the inorder list), and why preorder alone does not (give two different trees with the same preorder). Example: preorder=[3, 9, 20, 15, 7], inorder=[9, 3, 15, 20, 7] -> [3, 9, 20, null, null, 15, 7]; preorder=[-1], inorder=[-1] -> [-1]; preorder=[1, 2], inorder=[2, 1] -> [1, 2]; preorder=[1, 2], inorder=[1, 2] -> [1, null, 2].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Divide and conquer on traversal order. Preorder tells you the root, inorder tells you the sizes of the left and right parts.

**Say this first (1 line):** "The first preorder value is the root. Find it in inorder: everything left of it is the left subtree, everything right is the right subtree. I use a dict for that position and a moving preorder pointer, so it is O(n)."

**Brute force:** Take `pre[0]` as the root, `ino.index(root)` to find the split, and recurse on slices `pre[1:i+1], ino[:i]` and `pre[i+1:], ino[i+1:]`. `index` is O(n) and slicing copies, so each level costs O(n) and a chain costs O(n^2). The run counts the copied elements: 9900, 39800, 159600 for n = 100, 200, 400, which is about n^2.

**Optimal:**
- Build `pos = {value: inorder index}` once. Keep a pointer `p` into `pre`.
- `go(lo, hi)` builds the subtree whose inorder range is `ino[lo:hi]`. If empty, return None. Otherwise the root is `pre[p]` (then `p += 1`), `i = pos[root.val]`, left is `go(lo, i)`, right is `go(i + 1, hi)`.
- Left must be built first. Preorder is root, left part, right part, so the pointer reaches the right subtree's root only after the whole left part is consumed.
- Distinct values are required so that `pos` is well defined.
- Why the pair is unique: the root is forced (first of preorder), its inorder position fixes how many nodes are on each side, and the same argument applies inside each side. By induction there is exactly one tree. I also checked it by running: for every shape up to 7 nodes (625 non-empty shapes) all (preorder, inorder) pairs are different.
- Why preorder alone is not enough: for `[1, 2]` the tree can be 2 as the left child or 2 as the right child. The run shows that all 429 shapes with 7 nodes have the same preorder when labelled in preorder, so the sequence says nothing about the shape.

**Complexity:** Time O(n): one dict build, then O(1) per node. Space O(n) for the dict plus O(h) recursion. Slicing plus `index`: O(n^2) time.

**Dry run:** `pre=[3,9,20,15,7]`, `ino=[9,3,15,20,7]`. Root 3 at inorder index 1: left range `[0,1)`, right range `[2,5)`. Left: root 9, ranges empty both sides. Right: next preorder is 20 at index 3: left range `[2,3)` gives 15, right range `[4,5)` gives 7. Tree `[3, 9, 20, null, null, 15, 7]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- brute force: slice the lists and use list.index (O(n^2)) ----------
def build_slow(pre, ino):
    if not pre:
        return None
    root = TreeNode(pre[0])
    i = ino.index(pre[0])                               # O(n) search
    root.left = build_slow(pre[1:i + 1], ino[:i])       # slicing copies O(n)
    root.right = build_slow(pre[i + 1:], ino[i + 1:])
    return root

# ---------- optimal: dict value -> inorder index, moving preorder pointer ----------
def build(pre, ino):
    pos = {v: i for i, v in enumerate(ino)}
    p = 0
    def go(lo, hi):                                     # build from ino[lo:hi]
        nonlocal p
        if lo >= hi:
            return None
        root = TreeNode(pre[p]); p += 1                 # next preorder value is this subtree's root
        i = pos[root.val]
        root.left = go(lo, i)                           # left must be built first: preorder is root, left, right
        root.right = go(i + 1, hi)
        return root
    return go(0, len(ino))

# ---------- iterative version with a stack (safe on a 3000-node skewed tree) ----------
def build_iter(pre, ino):
    root = TreeNode(pre[0]); stack, j = [root], 0
    for v in pre[1:]:
        node = stack[-1]
        if node.val != ino[j]:                          # inorder has not reached this node yet: v is its left child
            node.left = TreeNode(v); stack.append(node.left)
        else:                                           # unwind to the node that owns v as a right child
            while stack and stack[-1].val == ino[j]:
                node = stack.pop(); j += 1
            node.right = TreeNode(v); stack.append(node.right)
    return root

def pre_of(t): return [] if t is None else [t[0]] + pre_of(t[1]) + pre_of(t[2])
def in_of(t): return [] if t is None else in_of(t[1]) + [t[0]] + in_of(t[2])

examples = [([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),
            ([-1], [-1], [-1]), ([1, 2], [2, 1], [1, 2]), ([1, 2], [1, 2], [1, None, 2])]
for pre, ino, want in examples:
    for f in (build_slow, build, build_iter):
        r = f(pre, ino)
        assert to_arr(r) == want
    print("pre=%s in=%s -> %s" % (pre, ino, to_arr(build(pre, ino))))

# exhaustive: every shape with 1..7 nodes, preorder labels, rebuild from (pre, in)
seen_pairs, total = {}, 0
for n in range(1, 8):
    for s in shapes(n):
        t = label(s, "pre")
        pre, ino = pre_of(t), in_of(t)
        for f in (build_slow, build, build_iter):
            assert tup(f(pre, ino)) == t
        key = (tuple(pre), tuple(ino))
        assert key not in seen_pairs                    # (pre, in) pairs are all different -> identifies the tree
        seen_pairs[key] = t
        total += 1
print("exhaustive ok:", total, "shapes; every (preorder, inorder) pair is distinct, so the pair identifies the tree")

# preorder alone is NOT enough: how many shapes share one preorder?
for n in range(1, 8):
    pres = {tuple(pre_of(label(s, "pre"))) for s in shapes(n)}
    print("n=%d: %d shapes, %d distinct preorder sequence(s)" % (n, len(shapes(n)), len(pres)))
print("two trees, same preorder [1, 2]:", to_arr(build([1, 2], [2, 1])), "and", to_arr(build([1, 2], [1, 2])))

# random relabelling with distinct arbitrary values
random.seed(16)
for _ in range(300):
    n = random.randint(1, 8)
    s = random.choice(shapes(n))
    vals = random.sample(range(-50, 50), n)
    t = label(s, "pre")
    def rel(t): return None if t is None else (vals[t[0]], rel(t[1]), rel(t[2]))
    t = rel(t)
    assert tup(build(pre_of(t), in_of(t))) == t == tup(build_iter(pre_of(t), in_of(t)))
print("random ok: 300 relabelled trees")

# n = 3000 skewed tree: recursion fails under the default limit, the iterative build does not
pre = list(range(1, 3001)); ino = list(range(1, 3001))          # right chain
r = deep_ok(build, pre, ino)
print("right chain 3000 recursive:", r if isinstance(r, str) else "built",
      "| iterative nodes:", len(all_nodes(build_iter(pre, ino))))
ino_rev = pre[::-1]                                              # left chain
print("left chain 3000 iterative nodes:", len(all_nodes(build_iter(pre, ino_rev))))

# work done by slicing: total elements copied on a right chain
copied = 0
def build_count(pre, ino):
    global copied
    if not pre: return None
    root = TreeNode(pre[0]); i = ino.index(pre[0])
    a, b, c, d = pre[1:i + 1], ino[:i], pre[i + 1:], ino[i + 1:]
    copied += len(a) + len(b) + len(c) + len(d)
    root.left = build_count(a, b); root.right = build_count(c, d)
    return root
for n in (100, 200, 400):
    copied = 0
    build_count(list(range(n)), list(range(n)))
    print("slicing copies on a chain of n=%d: %d (about n^2 = %d)" % (n, copied, n * n))
```

**Output (my run):**
```
pre=[3, 9, 20, 15, 7] in=[9, 3, 15, 20, 7] -> [3, 9, 20, None, None, 15, 7]
pre=[-1] in=[-1] -> [-1]
pre=[1, 2] in=[2, 1] -> [1, 2]
pre=[1, 2] in=[1, 2] -> [1, None, 2]
exhaustive ok: 625 shapes; every (preorder, inorder) pair is distinct, so the pair identifies the tree
n=1: 1 shapes, 1 distinct preorder sequence(s)
n=2: 2 shapes, 1 distinct preorder sequence(s)
n=3: 5 shapes, 1 distinct preorder sequence(s)
n=4: 14 shapes, 1 distinct preorder sequence(s)
n=5: 42 shapes, 1 distinct preorder sequence(s)
n=6: 132 shapes, 1 distinct preorder sequence(s)
n=7: 429 shapes, 1 distinct preorder sequence(s)
two trees, same preorder [1, 2]: [1, 2] and [1, None, 2]
random ok: 300 relabelled trees
right chain 3000 recursive: RecursionError | iterative nodes: 3000
left chain 3000 iterative nodes: 3000
slicing copies on a chain of n=100: 9900 (about n^2 = 10000)
slicing copies on a chain of n=200: 39800 (about n^2 = 40000)
slicing copies on a chain of n=400: 159600 (about n^2 = 160000)
```

**Edge cases:**
- One node. A chain going right (`pre == ino`) and a chain going left (`ino` reversed).
- Depth: a skewed tree of 3000 nodes is within the stated limit, but the recursive build needs depth 3000 and raises `RecursionError` at the default limit of 1000. Either raise the limit (`sys.setrecursionlimit`, and be aware the C stack can still overflow for big values) or use the iterative stack version in the code, which handles it.
- Duplicate values would break `pos`; the prompt rules them out.
- Inputs that are not a valid pair (different sets of values) raise `KeyError` or `IndexError`. Say you would validate first if the input is untrusted.

**Follow-ups:**
- Inorder plus postorder? Same idea, the root is the last postorder value and you build the right subtree first (Q29).
- Preorder plus postorder? Not unique in general (e.g. a single child can be left or right); unique only for full binary trees.
- Why not preorder plus level order? Possible but more complex; the inorder split is what gives the sizes.

**Common mistakes:**
- Building the right subtree before the left with a shared preorder pointer.
- Slicing lists and using `index` (O(n^2)).
- Off-by-one in the slice bounds when slicing (the left part of preorder is `pre[1:i+1]` only when `i` counts from the start of the current range).
- Mutating `pre` with `pop(0)` (O(n) each).

### Q17 ⭐⭐⭐ 🔴 Binary tree maximum path sum. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). A path is any sequence of nodes connected by parent-child edges where each node appears at most once; it need not start at the root or end at a leaf and it has at least one node. Values may be negative, 1 <= n <= 3*10^4. Return the largest sum of the values on any path. Each call returns the best DOWNWARD path starting at that node (clamped at 0, meaning 'take nothing from this side') while a running best uses left + node + right; explain why the clamp is right for the returned value but the best must still be at least the largest single node when every value is negative. Example: root=[1, 2, 3] -> 6; root=[-10, 9, 20, null, null, 15, 7] -> 42; root=[-3] -> -3; root=[2, -1] -> 2; root=[-1, -2, -3] -> -1.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Tree DP with "return one thing, record another": the return value is the best path going DOWN from a node (so a parent can extend it), the running best is the best path that BENDS at a node.

**Say this first (1 line):** "At each node I compute the best downward gain from each child, dropping any negative gain. The best path bending here is left + val + right. I return val + the better side, because a parent can only continue one branch."

**Brute force:** Try every pair of nodes as the two ends and sum the values on the unique path between them. In the code: a DFS from each node over the undirected tree. O(n^2) time. Right answer, too slow for n = 3 * 10^4.

**Optimal:**
- `gain(n)`: `l = max(gain(left), 0)`, `r = max(gain(right), 0)`. The `max(..., 0)` means "take nothing from this side".
- `best = max(best, l + n.val + r)`: the path that bends at `n` and uses both sides.
- `return n.val + max(l, r)`: the best path that starts at `n` and goes down one side. Returning `l + n.val + r` would let a parent use both branches of the child, and then the path would fork, which is not a path.
- Why the clamp is right for the returned value: if a branch has negative gain, a path that ends at `n` is better than one that continues into it.
- Why `best` must not start at 0: the path must have at least one node. With all values negative the answer is the largest single node (`[-1, -2, -3]` gives -1, and `best = 0` would wrongly return 0). Start at `float("-inf")`, or at `root.val`.
- Without the clamp the bending sum can include a negative branch. The run shows `[1, -5, 3]`: unclamped code answers 3, the correct answer is 4 (1 + 3).

**Complexity:** Time O(n), one visit per node. Space O(h) recursion (n on a chain; the iterative version keeps a dict of n gains).

**Dry run:** `[-10, 9, 20, null, null, 15, 7]`. Leaves: 9 gives gain 9, best 9. 15 gives 15, 7 gives 7. At 20: `l = 15, r = 7`, bend = 42, best = 42, returns 35. At -10: `l = 9, r = 35`, bend = 34 (less than 42), best stays 42. Answer 42 (path 15-20-7).

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"

import itertools

# ---------- brute force: try every pair of nodes, sum the unique tree path between them ----------
def max_path_brute(root):
    nodes = all_nodes(root)
    adj = {id(n): [] for n in nodes}
    for n in nodes:
        for c in (n.left, n.right):
            if c:
                adj[id(n)].append(c); adj[id(c)].append(n)
    best = None
    for s in nodes:                                    # DFS from every start; every reachable end is a path
        st = [(s, None, s.val)]
        while st:
            n, parent, tot = st.pop()
            best = tot if best is None else max(best, tot)
            for m in adj[id(n)]:
                if m is not parent:
                    st.append((m, n, tot + m.val))
    return best

# ---------- optimal: return best DOWNWARD gain (clamped at 0), track best path bending at the node ----------
def max_path_sum(root):
    best = float("-inf")                               # NOT 0: all-negative trees must give the largest single node
    def gain(n):
        nonlocal best
        if n is None:
            return 0
        l = max(gain(n.left), 0)                       # drop a negative branch
        r = max(gain(n.right), 0)
        best = max(best, l + n.val + r)                # path bends at n and uses both branches
        return n.val + max(l, r)                       # a parent can extend only ONE branch
    gain(root)
    return best

def max_path_iter(root):                               # same, iterative post-order
    g, best, st = {}, float("-inf"), [(root, False)]
    while st:
        n, done = st.pop()
        if not done:
            st.append((n, True))
            for c in (n.left, n.right):
                if c: st.append((c, False))
        else:
            l = max(g[id(n.left)], 0) if n.left else 0
            r = max(g[id(n.right)], 0) if n.right else 0
            best = max(best, l + n.val + r)
            g[id(n)] = n.val + max(l, r)
    return best

def max_path_bad_init(root):                           # the classic bug: best starts at 0
    best = 0
    def gain(n):
        nonlocal best
        if n is None: return 0
        l, r = max(gain(n.left), 0), max(gain(n.right), 0)
        best = max(best, l + n.val + r)
        return n.val + max(l, r)
    gain(root)
    return best

def max_path_no_clamp(root):                           # the other bug: negative branches are not dropped
    best = float("-inf")
    def gain(n):
        nonlocal best
        if n is None: return 0
        l, r = gain(n.left), gain(n.right)
        best = max(best, l + n.val + r)
        return n.val + max(l, r)
    gain(root)
    return best

examples = [([1, 2, 3], 6), ([-10, 9, 20, None, None, 15, 7], 42), ([-3], -3), ([2, -1], 2), ([-1, -2, -3], -1)]
for arr, want in examples:
    r = build_tree(arr)
    assert max_path_sum(r) == max_path_iter(r) == max_path_brute(r) == want
    print(arr, "->", want)
print("bad init (best=0) on [-1,-2,-3]:", max_path_bad_init(build_tree([-1, -2, -3])), "(wrong)")
print("no clamp on [1,-5,3]:", max_path_no_clamp(build_tree([1, -5, 3])), "vs correct", max_path_sum(build_tree([1, -5, 3])),
      "(brute", str(max_path_brute(build_tree([1, -5, 3]))) + ")")

# exhaustive: every shape with 1..5 nodes, every value assignment from {-2..2}
cases = 0
for n in range(1, 6):
    for s in shapes(n):
        for vals in itertools.product(range(-2, 3), repeat=n):
            it = iter(vals)
            def put(sh): return None if sh is None else (next(it), put(sh[0]), put(sh[1]))
            r = from_tup(put(s))
            w = max_path_brute(r)
            assert max_path_sum(r) == max_path_iter(r) == w
            cases += 1
print("exhaustive ok:", cases, "labelled trees (1..5 nodes, values -2..2)")

# 1500 random trees up to 14 nodes, values -20..20 (brute force is all node pairs)
random.seed(17)
for _ in range(1500):
    arr = [random.randint(-20, 20)]
    for _ in range(random.randint(0, 13)):
        arr.append(None if random.random() < 0.25 else random.randint(-20, 20))
    r = build_tree(arr)
    assert max_path_sum(r) == max_path_iter(r) == max_path_brute(r)
print("random ok: 1500 trees")

deep = chain(30000)                                    # all positive chain: whole chain is the path
print("chain 30000 recursive:", deep_ok(max_path_sum, deep), "| iterative:", max_path_iter(deep), "(sum 1..30000 =", 30000 * 30001 // 2, ")")
```

**Output (my run):**
```
[1, 2, 3] -> 6
[-10, 9, 20, None, None, 15, 7] -> 42
[-3] -> -3
[2, -1] -> 2
[-1, -2, -3] -> -1
bad init (best=0) on [-1,-2,-3]: 0 (wrong)
no clamp on [1,-5,3]: 3 vs correct 4 (brute 4)
exhaustive ok: 140680 labelled trees (1..5 nodes, values -2..2)
random ok: 1500 trees
chain 30000 recursive: RecursionError | iterative: 450015000 (sum 1..30000 = 450015000 )
```

**Edge cases:**
- Single negative node: its own value.
- All negative: the largest (closest to zero) single node, never an empty path.
- A zero-valued or negative root that the best path avoids entirely.
- Chain of 30000 nodes: recursion raises `RecursionError`; iterative post-order is fine. Sums are exact because Python ints do not overflow.

**Follow-ups:**
- Return the path itself, not only the sum? Store the best node and which child you used at each node, or keep `(gain, child_choice)`; rebuild after the pass.
- Path must go from root to a leaf? That is a simpler downward-only problem.
- Same shape in other problems? Diameter (Q11) is the same pattern with every value 1 (path sum then counts nodes, so the diameter in edges is that sum minus 1).

**Common mistakes:**
- Initialising `best = 0`.
- Forgetting the clamp, or clamping the `best` computation but not the return value (or vice versa).
- Returning `l + val + r` upward (a forked path).
- Using a plain int `best` inside the helper without `nonlocal`.

### Q18 ⭐⭐⭐ 🔴 Serialize and deserialize a binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Design `serialize(root) -> str` and `deserialize(s) -> root` so that deserialize(serialize(t)) rebuilds a tree equal to t in shape and values, for 0 <= n <= 10^4 and values in [-1000, 1000] (negative values, so choose a delimiter that cannot appear in a number). Use preorder with an explicit null marker for every missing child. State exactly how many tokens the string has for n nodes (it is 2n + 1, including the empty tree, which is one marker) and why the marker makes preorder alone enough, while plain preorder without markers is ambiguous. Deserialize with an iterator or an index, and say what happens to the recursion depth on a skewed tree and how to avoid it. Example: arr=[1, 2, 3, null, null, 4, 5] -> [1, 2, 3, null, null, 4, 5]; arr=[] -> []; arr=[1] -> [1]; arr=[-1, null, -2, -3] -> [-1, null, -2, -3].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Preorder with explicit null markers (a self-delimiting encoding). Recursion on both sides mirrors the tree.

**Say this first (1 line):** "Write preorder, but write a `#` for every missing child, joined with commas. Then reading is deterministic: read a token, if it is `#` return None, otherwise make a node and read its left then its right subtree."

**Brute force:** Store two traversals (preorder and inorder) and rebuild with Q16. That needs distinct values and two strings. Another option: store the level-order array with Nones, which can be huge for a skewed tree (about 2^h slots if you pad every level). The marker format uses exactly 2n + 1 tokens.

**Optimal:**
- `serialize`: preorder, append `str(val)` for a node and `#` for None. `",".join(tokens)`. Commas are safe because a number never contains one; `-` is part of a number and also cannot be confused with `#`.
- `deserialize`: `toks = iter(s.split(","))`, a recursive `go()` that consumes one token per call. `n.left = go()` must run before `n.right = go()`, since the stream is in preorder.
- Token count: n nodes have 2n child slots. n - 1 of them are filled by the other nodes, so the number of markers is `2n - (n - 1) = n + 1`, and the tokens are `n + (n + 1) = 2n + 1`. For the empty tree that gives 1 (just `#`). The run checks this for every tree shape with 0 to 7 nodes.
- Why markers make preorder enough: the stream is self-delimiting. A subtree ends exactly when its left and right parts have both been consumed, and a marker tells you a part is empty. So there is only one way to parse it.
- Plain preorder without markers is ambiguous: `[1, 2]` could be 2 as a left child or as a right child. The run prints both trees with the same plain preorder `[1, 2]`, and the marker strings `1,2,#,#,#` and `1,#,2,#,#`.
- Recursion depth is the tree height. On a skewed tree of 3000 nodes both recursive functions raise `RecursionError` under the default limit of 1000. Avoid it with an explicit stack: serialize with a stack that pops the left child first; deserialize with a stack of `[node, left_filled]` entries (code above). The iterative round trip works on 3000 nodes (6001 tokens).

**Complexity:** Time O(n) both ways (string building with `join`, not repeated `+`). Space O(n) for the string, plus O(h) for the recursion or stack.

**Dry run:** `[1, 2, 3, null, null, 4, 5]`. Preorder with markers: 1, 2, `#`, `#`, 3, 4, `#`, `#`, 5, `#`, `#` which is `1,2,#,#,3,4,#,#,5,#,#`: 11 tokens, and 2 * 5 + 1 = 11. Read: 1, then left: 2 (left `#`, right `#`), then right: 3 (left: 4 with two markers, right: 5 with two markers).

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


NULL = "#"

# ---------- preorder with a null marker for every missing child, comma delimiter ----------
def serialize(root):
    out = []
    def go(n):
        if n is None:
            out.append(NULL); return
        out.append(str(n.val)); go(n.left); go(n.right)
    go(root)
    return ",".join(out)

def deserialize(s):
    toks = iter(s.split(","))
    def go():
        t = next(toks)
        if t == NULL:
            return None
        n = TreeNode(int(t))
        n.left = go()                                   # preorder: left subtree is fully consumed first
        n.right = go()
        return n
    return go()

# ---------- iterative versions (no recursion, safe on a skewed tree) ----------
def serialize_iter(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None:
            out.append(NULL); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)   # left is popped first
    return ",".join(out)

def deserialize_iter(s):
    toks = s.split(",")
    if toks[0] == NULL:
        return None
    root = TreeNode(int(toks[0])); i = 1
    stack = [[root, False]]                             # [node, left child already filled?]
    while stack:
        top = stack[-1]; t = toks[i]; i += 1
        node = None if t == NULL else TreeNode(int(t))
        if not top[1]:
            top[0].left = node; top[1] = True
        else:
            top[0].right = node; stack.pop()
        if node:
            stack.append([node, False])
    assert i == len(toks)                               # every token consumed exactly once
    return root

# ---------- plain preorder (no markers) is ambiguous ----------
def plain_preorder(t): return [] if t is None else [t[0]] + plain_preorder(t[1]) + plain_preorder(t[2])

def same_shape_and_values(a, b):
    sa, sb = [(a, b)], True
    while sa:
        x, y = sa.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        sa.append((x.left, y.left)); sa.append((x.right, y.right))
    return True

examples = [[1, 2, 3, None, None, 4, 5], [], [1], [-1, None, -2, -3]]
for arr in examples:
    r = build_tree(arr)
    s = serialize(r)
    back = deserialize(s)
    assert s == serialize_iter(r)
    assert to_arr(back) == to_arr(deserialize_iter(s)) == arr
    print(arr, "->", repr(s), "->", to_arr(back))

# exhaustive: all shapes with 0..7 nodes, token count is exactly 2n + 1
total = 0
for n in range(8):
    for s in shapes(n):
        r = from_tup(label(s, "pre"))
        text = serialize(r)
        assert len(text.split(",")) == 2 * n + 1, (n, text)
        assert text == serialize_iter(r)
        back, back2 = deserialize(text), deserialize_iter(text)
        assert tup(back) == tup(back2) == tup(r)
        orig = {id(x) for x in all_nodes(r)}
        assert not orig & {id(x) for x in all_nodes(back)}   # a copy, no shared nodes
        total += 1
print("exhaustive ok:", total, "shapes; tokens == 2n + 1 for n = 0..7 (empty tree is one marker)")

# plain preorder collides: count distinct preorder lists vs shapes
for n in range(1, 6):
    pres = {tuple(plain_preorder(label(s, "pre"))) for s in shapes(n)}
    print("n=%d: %d shapes, plain preorder values identify %d of them" % (n, len(shapes(n)), len(pres)))
print("plain preorder of [1,2] as left child and as right child:", plain_preorder((1, (2, None, None), None)), plain_preorder((1, None, (2, None, None))))
print("with markers:", serialize(build_tree([1, 2])), "vs", serialize(build_tree([1, None, 2])))

# negative values, delimiter safe
r = build_tree([-1000, -1, 1000, None, -7])
assert to_arr(deserialize(serialize(r))) == [-1000, -1, 1000, None, -7]
print("negatives ok:", serialize(r))

# random trees, values -1000..1000
random.seed(18)
for _ in range(500):
    arr = [random.randint(-1000, 1000)]
    for _ in range(random.randint(0, 40)):
        arr.append(None if random.random() < 0.35 else random.randint(-1000, 1000))
    r = build_tree(arr)
    s = serialize(r)
    assert s == serialize_iter(r) and to_arr(deserialize(s)) == to_arr(deserialize_iter(s)) == to_arr(r)
    assert len(s.split(",")) == 2 * len(all_nodes(r)) + 1
print("random ok: 500 trees")

# skewed tree with 3000 nodes: recursive versions fail under the default limit, iterative ones work
deep = chain(3000)
text = serialize_iter(deep)
print("skewed 3000: recursive serialize:", "RecursionError" if deep_ok(serialize, deep) == "RecursionError" else "ok",
      "| recursive deserialize:", "RecursionError" if deep_ok(deserialize, text) == "RecursionError" else "ok",
      "| iterative round trip equal:", same_shape_and_values(deep, deserialize_iter(text)), "| tokens:", len(text.split(",")))
```

**Output (my run):**
```
[1, 2, 3, None, None, 4, 5] -> '1,2,#,#,3,4,#,#,5,#,#' -> [1, 2, 3, None, None, 4, 5]
[] -> '#' -> []
[1] -> '1,#,#' -> [1]
[-1, None, -2, -3] -> '-1,#,-2,-3,#,#,#' -> [-1, None, -2, -3]
exhaustive ok: 626 shapes; tokens == 2n + 1 for n = 0..7 (empty tree is one marker)
n=1: 1 shapes, plain preorder values identify 1 of them
n=2: 2 shapes, plain preorder values identify 1 of them
n=3: 5 shapes, plain preorder values identify 1 of them
n=4: 14 shapes, plain preorder values identify 1 of them
n=5: 42 shapes, plain preorder values identify 1 of them
plain preorder of [1,2] as left child and as right child: [1, 2] [1, 2]
with markers: 1,2,#,#,# vs 1,#,2,#,#
negatives ok: -1000,-1,#,-7,#,#,1000,#,#
random ok: 500 trees
skewed 3000: recursive serialize: RecursionError | recursive deserialize: RecursionError | iterative round trip equal: True | tokens: 6001
```

**Edge cases:**
- Empty tree: `"#"`. Single node: `"1,#,#"`.
- Negative values such as `-1` and `-1000`: fine with the comma delimiter and a marker that is not a digit or `-`.
- Skewed trees: use the iterative functions, as above.
- The rebuilt tree must be a fresh copy (no shared nodes); the run verifies this by node identity on every small shape.

**Follow-ups:**
- BFS (level-order) format instead? Same idea with a queue, with a marker for every missing child (Q38).
- Smaller output for a BST? Preorder alone with no markers is enough, because the values determine the shape (Q44).
- Values may contain commas or be strings? Choose an escape or a length prefix, or use a binary or JSON format.

**Common mistakes:**
- A format without markers (ambiguous) or without delimiters (`12` versus `1,2`).
- Building the right child before the left.
- Using `int(token)` on `#`.
- Repeated string `+=` in a loop (quadratic); collect tokens and join.
- Leaving the recursion limit as is and testing only on small trees.

### Q19 ⭐⭐ 🟢 Subtree of another tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given trees `root` (1 <= n <= 2000) and `sub` (1 <= m <= 1000), return True if some node of `root` has a subtree identical to `sub` in shape and values (the whole subtree down to the leaves, so a node with extra descendants does not count). Give the O(n * m) solution built on the same-tree check, and the serialization approach with null markers and delimiters; show why serializing without delimiters and markers is wrong (a tree holding 12 against a tree holding 2). Example: root=[3, 4, 5, 1, 2], sub=[4, 1, 2] -> True; root=[3, 4, 5, 1, 2, null, null, null, null, 0], sub=[4, 1, 2] -> False; root=[1, 1], sub=[1] -> True; root=[12], sub=[2] -> False.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Same-tree check run at every node (O(n * m)), or serialize both trees and use a substring search.

**Say this first (1 line):** "For every node in root I ask 'is the tree below you identical to sub?' with the same-tree check. That is O(n * m). The alternative is serialization with null markers and delimiters, then a substring test."

**Brute force / baseline:**
- Visit each node of `root`; call `is_same(node, sub)`, which compares values and both children, treating None carefully (`a is b` when either is None).
- "Identical" means down to the leaves: a node with extra descendants does not count (the second example).
- Cost: each `is_same` call from one start node touches at most 2m + 1 calls (every call with a non-None sub node is a distinct node of sub, and every call with a None sub node is a child of one of them). So at most `n * (2m + 1)` calls in total: O(n * m). The run checks this bound for every pair of small trees.

**Optimal / alternative:**
- Serialize both trees as preorder with a null marker for every missing child and a delimiter before every token, for example `,3,4,1,#,#,2,#,#,5,#,#`. Then `ser(sub) in ser(root)`.
- Why this is right: the marker string is self-delimiting (it parses to exactly one tree, as in Q18), and every token starts with a comma, so a match must start at a token boundary. It then parses as a whole subtree beginning at that node.
- Why both parts are needed: without delimiters, `12` contains `2` (root `[12]` against sub `[2]`; the run shows the wrong answer). Without markers, `[1, null, 2]` and `[1, 2]` both give `,1,2`, so a root with a right child "contains" the sub with a left child (the run shows it). With markers but no delimiters `12##` still contains `2##`.
- The substring test with Python's `in` is fast in practice. The worst-case guarantee needs KMP or a hash-based search over the token list, giving O(n + m).

**Complexity:** Same-tree approach: time O(n * m) worst case (for example a chain of ones against a chain of ones ending in a 2: the run measures 120198 calls for n = 400, m = 200, bound 160400), space O(h) recursion. Serialization: O(n + m) to build the strings and the substring test's cost, space O(n + m).

**Dry run:** `root=[3, 4, 5, 1, 2]`, `sub=[4, 1, 2]`. At node 3: values differ, no. At node 4: values equal, then 1 vs 1 (both children None on each side: equal), 2 vs 2: True. Second example: the node 4 matches but its child 2 has a child 0 while `sub` has None there, so `a is b` fails: False.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"

import itertools

CALLS = 0
def is_same(a, b):
    global CALLS
    CALLS += 1
    if a is None or b is None:
        return a is b
    return a.val == b.val and is_same(a.left, b.left) and is_same(a.right, b.right)

# ---------- brute force / O(n*m): try is_same at every node of root ----------
def is_subtree(root, sub):
    st = [root]
    while st:
        n = st.pop()
        if is_same(n, sub):
            return True
        for c in (n.left, n.right):
            if c: st.append(c)
    return False

# ---------- serialization: markers AND delimiters, then a substring test ----------
def ser(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None:
            out.append(",#"); continue
        out.append("," + str(n.val)); st.append(n.right); st.append(n.left)
    return "".join(out)                                # every token starts with a comma

def is_subtree_ser(root, sub):
    return ser(sub) in ser(root)

# ---------- the wrong version: no delimiters, no markers ----------
def naive(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n:
            out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return "".join(out)

# ---------- independent brute force on tuples ----------
def tsubs(t):
    if t is None: return []
    return [t] + tsubs(t[1]) + tsubs(t[2])
def subtree_brute(tr, ts):
    return any(x == ts for x in tsubs(tr))

examples = [([3, 4, 5, 1, 2], [4, 1, 2], True),
            ([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2], False),
            ([1, 1], [1], True), ([12], [2], False)]
for ra, sa, want in examples:
    r, s = build_tree(ra), build_tree(sa)
    assert is_subtree(r, s) == is_subtree_ser(r, s) == subtree_brute(tup(r), tup(s)) == want
    print("root=%s sub=%s -> %s" % (ra, sa, want))
print("naive concatenation: root [12] holds", repr(naive(build_tree([12]))), "and sub [2] holds", repr(naive(build_tree([2]))),
      "-> '2' in '12' is", naive(build_tree([2])) in naive(build_tree([12])), "(wrong)")
def ser_no_delim(root):                                # markers but NO delimiters
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None:
            out.append("#"); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return "".join(out)
print("markers but no delimiters:", repr(ser_no_delim(build_tree([12]))), "vs", repr(ser_no_delim(build_tree([2]))),
      "-> substring test says", ser_no_delim(build_tree([2])) in ser_no_delim(build_tree([12])), "(wrong)")
print("with delimiters:", repr(ser(build_tree([12]))), "vs", repr(ser(build_tree([2]))),
      "-> substring test says", ser(build_tree([2])) in ser(build_tree([12])))

def ser_no_marker(root):                               # delimiters but NO null markers
    out, st = [], [root]
    while st:
        n = st.pop()
        if n:
            out.append("," + str(n.val)); st.append(n.right); st.append(n.left)
    return "".join(out)
a_, b_ = build_tree([1, None, 2]), build_tree([1, 2])
print("delimiters but no markers: root [1,null,2] gives", repr(ser_no_marker(a_)), "and sub [1,2] gives", repr(ser_no_marker(b_)),
      "-> substring test says", ser_no_marker(b_) in ser_no_marker(a_), "(wrong, the trees differ)")

# exhaustive: all trees with 1..4 nodes (all shapes, values in {1, 2}) as both root and sub
trees = []
for n in range(1, 5):
    for s in shapes(n):
        for vals in itertools.product((1, 2), repeat=n):
            it = iter(vals)
            def put(sh): return None if sh is None else (next(it), put(sh[0]), put(sh[1]))
            trees.append(put(s))
cases = yes = 0
worst = 0.0
for ta in trees:
    ra = from_tup(ta)
    for tb in trees:
        rb = from_tup(tb)
        CALLS = 0
        a = is_subtree(ra, rb)
        n, m = len(tsubs(ta)), len(tsubs(tb))
        assert CALLS <= n * (2 * m + 1)                # each start node costs at most 2m + 1 calls
        worst = max(worst, CALLS / (n * m))
        b = is_subtree_ser(ra, rb)
        assert a == b == subtree_brute(ta, tb)
        cases += 1; yes += a
print("exhaustive ok:", cases, "(root, sub) pairs,", yes, "are True; is_same calls never exceed n*(2m+1)")

# the naive version really is wrong on small trees
bad = sum(1 for ta in trees for tb in trees
          if (naive(from_tup(tb)) in naive(from_tup(ta))) != subtree_brute(ta, tb))
print("naive string test wrong on", bad, "of", cases, "pairs (plain values concatenated, no markers, no delimiters)")

# random larger trees with a planted subtree
random.seed(19)
for _ in range(300):
    arr = [random.randint(0, 2)]
    for _ in range(random.randint(0, 25)):
        arr.append(None if random.random() < 0.3 else random.randint(0, 2))
    r = build_tree(arr)
    sub = random.choice(all_nodes(r)) if random.random() < 0.5 else build_tree([random.randint(0, 2), random.randint(0, 2)])
    assert is_subtree(r, sub) == is_subtree_ser(r, sub) == subtree_brute(tup(r), tup(sub))
print("random ok: 300 trees")

# worst case for O(n*m): all ones with a different last value
n_, m_ = 400, 200
a = chain(n_); b = chain(m_)
for x in all_nodes(a): x.val = 1
for x in all_nodes(b): x.val = 1
tail = b
while tail.right: tail = tail.right
tail.val = 2                                          # sub ends in a 2, root never has one
CALLS = 0
print("chain n=%d, sub chain m=%d: found =" % (n_, m_), is_subtree(a, b), "| is_same calls =", CALLS, "| n*m =", n_ * m_)
```

**Output (my run):**
```
root=[3, 4, 5, 1, 2] sub=[4, 1, 2] -> True
root=[3, 4, 5, 1, 2, None, None, None, None, 0] sub=[4, 1, 2] -> False
root=[1, 1] sub=[1] -> True
root=[12] sub=[2] -> False
naive concatenation: root [12] holds '12' and sub [2] holds '2' -> '2' in '12' is True (wrong)
markers but no delimiters: '12##' vs '2##' -> substring test says True (wrong)
with delimiters: ',12,#,#' vs ',2,#,#' -> substring test says False
delimiters but no markers: root [1,null,2] gives ',1,2' and sub [1,2] gives ',1,2' -> substring test says True (wrong, the trees differ)
exhaustive ok: 75076 (root, sub) pairs, 982 are True; is_same calls never exceed n*(2m+1)
naive string test wrong on 6178 of 75076 pairs (plain values concatenated, no markers, no delimiters)
random ok: 300 trees
chain n=400, sub chain m=200: found = False | is_same calls = 120198 | n*m = 80000
```

**Edge cases:**
- `sub` equal to the whole root: True. Root a single node: only a single-node sub with the same value matches.
- Repeated values (`[1, 1]` against `[1]`): the second node matches.
- Extra descendants below the match (second example): False.
- `12` versus `2`: delimiters needed.
- Deep chains: recursive `is_same` is limited by the recursion limit; the chain test uses a right chain of 400 nodes, which is safe, and a real 2000-node chain needs the iterative approach (the iterative serializer above has no recursion).

**Follow-ups:**
- Faster than O(n * m)? Serialization plus KMP, or hash every subtree (Merkle-style hash with canonical ids) and compare the hash of `sub` with every node's hash: O(n + m) expected.
- Why not compare only heights or sizes first? It is a good prune: skip `is_same` when the sizes differ.
- Count how many nodes root has with sub as their subtree? Same hashing, count matches.

**Common mistakes:**
- Calling `is_same` only at the root.
- Treating "contains the same values below" as a match (extra descendants must not match).
- Serializing without markers or without delimiters.
- Writing `a == b` on node objects (compares identity, not structure).

### Q20 ⭐⭐ 🟢 Minimum depth. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the number of nodes on the shortest path from the root to a LEAF (a node with no children); an empty tree has depth 0 and 0 <= n <= 10^5. A node with one child is not a leaf, so `1 + min(left, right)` is wrong when one side is empty; explain and fix it. Give the recursive version and the BFS version that stops at the first leaf, and say which does less work on a perfect tree and which on a long chain. Example: root=[3, 9, 20, null, null, 15, 7] -> 2; root=[2, null, 3, null, 4, null, 5, null, 6] -> 5; root=[] -> 0; root=[1, 2] -> 2.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Shortest path to a leaf in a tree: BFS stops at the first leaf; recursion needs a special case for nodes with one child.

**Say this first (1 line):** "A leaf has no children, so a node with one child is not a leaf. If one side is empty I must use the other side, not take `1 + min` of an empty 0. Or I do BFS and return the depth of the first leaf I meet."

**Brute force:** Collect the depth of every leaf and take the minimum: O(n) time, O(h) to O(w) space. This is correct but always touches every node. I use it as the oracle.

**Optimal:**
- Recursive: `None` gives 0. If `left` is None return `1 + depth(right)`. If `right` is None return `1 + depth(left)`. Otherwise `1 + min(depth(left), depth(right))`.
- Why `1 + min(l, r)` alone is wrong: for a node with one child, the empty side returns 0, so the formula says the node is a leaf at depth 1. For `[1, 2]` it answers 1, but the root is not a leaf; the only leaf is 2, at depth 2. The run shows the wrong answers (1 for `[1, 2]`, 1 for the chain with expected 5) and that it fails on 496 of 626 small shapes.
- BFS: process the tree level by level; the first node with no children is the shallowest leaf, so return the current depth immediately. No case analysis on one-child nodes is needed.
- Which does less work: on a perfect tree of height 10 (1023 nodes) the recursion visits all 1023 nodes while BFS stops after popping 512 (the 511 internal nodes plus the first leaf), about half. On a long chain both visit every node (500 and 500). On a tree with a shallow leaf beside a long chain BFS pops 2 nodes and the plain recursion still visits 500.
- Space: BFS holds up to a whole level (about n/2 on the perfect tree) but only 1 node at a time on a chain; recursion holds up to the height (n on a chain).

**Complexity:** Time O(n) worst case for both (recursion always O(n); BFS O(n) worst, often far less because it stops at the first leaf, at most all nodes on levels above the shallowest leaf). Space: recursion O(h); BFS O(w), the widest level.

**Dry run:** `[3, 9, 20, null, null, 15, 7]`. BFS: depth 1, queue `[3]`: 3 has children. Depth 2, queue `[9, 20]`: pop 9, no children, it is a leaf, return 2. Never looks at 15 or 7. Recursive: node 3 has two children, so `1 + min(depth(9), depth(20))` is `1 + min(1, 2) = 2`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- brute force: depth of every leaf, take the smallest ----------
def min_depth_brute(root):
    if root is None:
        return 0
    best, st = None, [(root, 1)]
    while st:
        n, d = st.pop()
        if n.left is None and n.right is None:
            best = d if best is None else min(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

# ---------- the classic bug ----------
def min_depth_wrong(root):
    if root is None:
        return 0
    return 1 + min(min_depth_wrong(root.left), min_depth_wrong(root.right))    # a one-child node is NOT a leaf

# ---------- recursive, fixed ----------
VISITS = 0
def min_depth_rec(root):
    global VISITS
    if root is None:
        return 0
    VISITS += 1
    if root.left is None:
        return 1 + min_depth_rec(root.right)            # only one side exists: must use it
    if root.right is None:
        return 1 + min_depth_rec(root.left)
    return 1 + min(min_depth_rec(root.left), min_depth_rec(root.right))

# ---------- BFS: the first leaf found level by level is the shallowest ----------
POPS = 0
def min_depth_bfs(root):
    global POPS
    if root is None:
        return 0
    q, depth = deque([root]), 1
    while q:
        for _ in range(len(q)):
            n = q.popleft(); POPS += 1
            if n.left is None and n.right is None:
                return depth                            # first leaf = minimum depth
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        depth += 1

examples = [([3, 9, 20, None, None, 15, 7], 2), ([2, None, 3, None, 4, None, 5, None, 6], 5), ([], 0), ([1, 2], 2)]
for arr, want in examples:
    r = build_tree(arr)
    assert min_depth_rec(r) == min_depth_bfs(r) == min_depth_brute(r) == want
    print(arr, "->", want)
print("wrong 1+min on [1,2]:", min_depth_wrong(build_tree([1, 2])), "(correct is 2)")
print("wrong 1+min on the chain example:", min_depth_wrong(build_tree([2, None, 3, None, 4, None, 5, None, 6])), "(correct is 5)")

# exhaustive over every shape with 0..7 nodes
total = wrong = 0
for n in range(8):
    for s in shapes(n):
        r = from_tup(label(s, "pre"))
        w = min_depth_brute(r)
        assert min_depth_rec(r) == min_depth_bfs(r) == w
        wrong += min_depth_wrong(r) != w
        total += 1
print("exhaustive ok:", total, "shapes; the 1+min version is wrong on", wrong, "of them")

random.seed(20)
for _ in range(500):
    arr = [random.randint(0, 9)]
    for _ in range(random.randint(0, 50)):
        arr.append(None if random.random() < 0.4 else random.randint(0, 9))
    r = build_tree(arr)
    assert min_depth_rec(r) == min_depth_bfs(r) == min_depth_brute(r)
print("random ok: 500 trees")

# work on three shapes: perfect tree, long chain, and a tree with a shallow leaf next to a long chain
def perfect(h):
    arr = list(range(1, 2 ** h))
    return build_tree(arr)
def lopsided(n):                                         # root with a leaf on the left, a chain of n - 2 on the right
    return TreeNode(0, TreeNode(1), chain(n - 2))
for name, r in (("perfect h=10 (n=1023)", perfect(10)), ("chain n=500", chain(500)), ("shallow leaf + chain n=500", lopsided(500))):
    VISITS = POPS = 0
    a = min_depth_rec(r); b = min_depth_bfs(r)
    assert a == b == min_depth_brute(r)
    print("%-28s depth=%d  recursive visits=%d  BFS pops=%d" % (name, a, VISITS, POPS))

# long chain of 100000 nodes (the stated maximum): recursion fails, BFS does not
deep = chain(100000)
POPS = 0
print("chain 100000: recursive:", deep_ok(min_depth_rec, deep), "| BFS:", min_depth_bfs(deep), "| BFS pops:", POPS)
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> 2
[2, None, 3, None, 4, None, 5, None, 6] -> 5
[] -> 0
[1, 2] -> 2
wrong 1+min on [1,2]: 1 (correct is 2)
wrong 1+min on the chain example: 1 (correct is 5)
exhaustive ok: 626 shapes; the 1+min version is wrong on 496 of them
random ok: 500 trees
perfect h=10 (n=1023)        depth=10  recursive visits=1023  BFS pops=512
chain n=500                  depth=500  recursive visits=500  BFS pops=500
shallow leaf + chain n=500   depth=2  recursive visits=500  BFS pops=2
chain 100000: recursive: RecursionError | BFS: 100000 | BFS pops: 100000
```

**Edge cases:**
- Empty tree: 0. Single node: 1 (it is a leaf).
- A root with one child (`[1, 2]`): 2, not 1.
- A chain: the depth is n, the case where the one-child rule matters most.
- n up to 10^5: a 100000-node chain makes the recursive version raise `RecursionError` at the default limit of 1000 (the run shows it); BFS handles it. A plain recursion limit of 1000 already fails at about 1000 nodes, so for the stated bound use BFS or an explicit stack.

**Follow-ups:**
- Count edges instead of nodes? Subtract 1 for a non-empty tree.
- Maximum depth? Plain `1 + max(l, r)` works, since an empty side never wins a max (Q2).
- Can recursion stop early too? Yes: DFS with a global `best` that prunes any branch already deeper than `best`, but the worst case is still O(n).

**Common mistakes:**
- `1 + min(left, right)` without the one-child case.
- Treating a node with one child as a leaf.
- Returning the BFS depth after the whole level instead of at the first leaf (still correct, but loses the early exit).
- Off-by-one: starting the depth at 0 and counting edges.

### Q21 ⭐⭐ 🟢 Sorted array and sorted list to a height-balanced BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a sorted array of distinct integers (0 <= n <= 10^4), build a BST whose subtree heights differ by at most 1 at every node, using this rule so the answer is unique: the root of a range is the element at index (lo + hi) // 2 (the lower middle for an even count). Return the tree. Then do the same for a SORTED SINGLY LINKED LIST (nodes `ListNode(val, next)`; the middle of a list is Part 6 Q2) and give two ways: find the middle with slow and fast pointers each time, and simulate inorder so each list node is consumed once in O(n). Both must give the same tree as the array rule. Example: nums=[-10, -3, 0, 5, 9] -> [0, -10, 5, null, -3, null, 9]; nums=[1, 3] -> [1, null, 3]; nums=[1] -> [1]; nums=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Divide and conquer on a sorted range. The middle element is the root, so both subtrees get half the elements and the heights differ by at most 1. For the list, the same tree falls out of an inorder simulation.

**Say this first (1 line):** "Root is the element at (lo + hi) // 2, recurse on both halves; for a list I count n once and build inorder so each list node is consumed exactly once."

**Brute force:** For the list, copy it into an array first (O(n) extra space) and reuse the array builder. Or find the middle with slow and fast pointers at every call. Each call costs the length of its segment, so one level costs about n/2 pointer steps and there are log n levels: O(n log n) time, O(log n) stack, no extra copy.

**Optimal:**
- Array: `go(lo, hi)` makes the node for `nums[(lo + hi) // 2]`, then `go(lo, mid - 1)` and `go(mid + 1, hi)`. O(n) time, O(log n) stack. The depth is about 14 at n = 10^4, so recursion is safe here.
- List, inorder simulation: count n, keep one cursor on the list. `go(lo, hi)` first builds the left subtree (it eats list nodes lo..mid-1), then the cursor sits exactly on list node `mid`, take its value and step the cursor, then build the right subtree. The tree is built bottom-up and the list is read once, in order. O(n) time, O(log n) stack.
- The lower-middle rule is the same `(lo + hi) // 2` in both, so the trees match.
- Why balanced: the two halves differ in size by at most 1, so by induction their heights differ by at most 1.

**Complexity:** Array: T(n) = 2T(n/2) + O(1) = O(n). List with repeated middle search: T(n) = 2T(n/2) + O(n) = O(n log n). List by inorder simulation: O(n). Stack depth O(log n) in all of them.

**Dry run:** `[-10, -3, 0, 5, 9]`. `go(0, 4)`: mid = 2, root 0. Left `go(0, 1)`: mid = 0, node -10, its right is `go(1, 1)` = -3. Right `go(3, 4)`: mid = 3, node 5, its right is `go(4, 4)` = 9. Level order: `[0, -10, 5, null, -3, null, 9]`. For the list, the cursor visits -10, -3, 0, 5, 9 in that order, so -10 is built first, then -3, then the root 0.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

class ListNode:
    __slots__ = ("val", "next")
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def build_list(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v); tail = tail.next
    return dummy.next

def list_vals(head):
    out = []
    while head:
        out.append(head.val); head = head.next
        assert len(out) < 10**6
    return out

# ---------- array: root of [lo, hi] is index (lo + hi) // 2 ----------
def sorted_array_to_bst(nums):
    def go(lo, hi):
        if lo > hi: return None
        mid = (lo + hi) // 2
        return TreeNode(nums[mid], go(lo, mid - 1), go(mid + 1, hi))
    return go(0, len(nums) - 1)

# ---------- list, way 1: slow/fast to find the (lower) middle every time, O(n log n) ----------
STEPS = [0]
def list_to_bst_midpoint(head):
    def go(start, end):                      # half-open segment [start, end); end is a node or None
        if start is end: return None
        slow = fast = start
        while fast.next is not end and fast.next.next is not end:   # stops on the LOWER middle
            slow = slow.next; fast = fast.next.next; STEPS[0] += 1
        return TreeNode(slow.val, go(start, slow), go(slow.next, end))
    return go(head, None)

# ---------- list, way 2: simulate inorder, each list node consumed once, O(n) ----------
def list_to_bst_inorder(head):
    n, p = 0, head
    while p: n += 1; p = p.next
    cur = [head]
    def go(lo, hi):                          # builds indexes lo..hi; the lower middle is (lo + hi) // 2
        if lo > hi: return None
        mid = (lo + hi) // 2
        left = go(lo, mid - 1)               # left subtree consumes list nodes lo..mid-1
        node = TreeNode(cur[0].val)          # now cur is exactly list node mid
        cur[0] = cur[0].next
        node.left = left
        node.right = go(mid + 1, hi)
        return node
    return go(0, n - 1)

# ---------- checks ----------
def is_bst_balanced(root):
    vals = []
    def go(n):                               # returns height; depth is ~log n here so recursion is fine
        if n is None: return 0
        hl = go(n.left); vals.append(n.val); hr = go(n.right)
        assert abs(hl - hr) <= 1, "height-unbalanced"
        return 1 + max(hl, hr)
    go(root)
    assert vals == sorted(vals) and len(set(vals)) == len(vals)
    return vals

for arr, exp in [([-10, -3, 0, 5, 9], [0, -10, 5, None, -3, None, 9]), ([1, 3], [1, None, 3]), ([1], [1]), ([], [])]:
    a = to_arr(sorted_array_to_bst(arr))
    b = to_arr(list_to_bst_midpoint(build_list(arr)))
    c = to_arr(list_to_bst_inorder(build_list(arr)))
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, "->", a)

# exhaustive over every length 0..70 plus random distinct sorted arrays; all three agree and are valid
for n in range(0, 71):
    arr = list(range(n))
    t1 = sorted_array_to_bst(arr)
    assert is_bst_balanced(t1) == arr
    h = build_list(arr)
    t2, t3 = list_to_bst_midpoint(h), list_to_bst_inorder(h)
    assert same_shape(t1, t2) and same_shape(t1, t3)
    assert list_vals(h) == arr                           # input list untouched
random.seed(21)
for _ in range(300):
    arr = sorted(random.sample(range(-500, 500), random.randint(0, 60)))
    t1 = sorted_array_to_bst(arr)
    assert same_shape(t1, list_to_bst_midpoint(build_list(arr))) and same_shape(t1, list_to_bst_inorder(build_list(arr)))
print("cross-check ok: lengths 0..70 and 300 random sorted arrays, three builders give the same tree")

# the work of the 'find the middle every time' version: ~ (n/2) pointer steps per level, log n levels
for n in (1023, 10000):
    STEPS[0] = 0
    list_to_bst_midpoint(build_list(range(n)))
    print("n =", n, "-> slow/fast pointer steps =", STEPS[0], "(sandbox count; the inorder version touches each node once)")
assert sorted_array_to_bst(list(range(10**4))) is not None   # n = 10^4: depth ~14, no recursion problem
```

**Output (my run):**
```
[-10, -3, 0, 5, 9] -> [0, -10, 5, None, -3, None, 9]
[1, 3] -> [1, None, 3]
[1] -> [1]
[] -> []
cross-check ok: lengths 0..70 and 300 random sorted arrays, three builders give the same tree
n = 1023 -> slow/fast pointer steps = 4097 (sandbox count; the inorder version touches each node once)
n = 10000 -> slow/fast pointer steps = 54613 (sandbox count; the inorder version touches each node once)
```

**Edge cases:**
- Empty array or list: return None (checked: the counting loop gives n = 0 and `go(0, -1)` returns None).
- One element: a single node.
- Even length: the LOWER middle is the root, so `[1, 3]` gives root 1 with right child 3. The other choice (upper middle) is a different valid tree, which is why the prompt fixes the rule.
- The list must stay untouched; the inorder version only reads it.

**Follow-ups:**
- Same for a sorted list but you may not count it first? Use a first pass to count (O(n)), or recurse on sizes. Counting is the standard trick.
- Does the slow/fast version find the lower middle? Only with the stop test `fast.next.next is not end`; the textbook `while fast and fast.next` gives the upper middle on even lengths and builds a different (still balanced) tree.
- Is the result complete (every level full except the last)? Not necessarily; the rule only guarantees height balance.

**Common mistakes:**
- Using `lo + hi // 2` (precedence) or the upper middle and getting a different tree from the expected one.
- Cutting the list (`prev.next = None`) in the midpoint version and destroying the input.
- Forgetting that the cursor must advance after the left subtree is built, not before.
- Using `len(nums) // 2` on slices: slicing copies and makes the array version O(n log n).

### Q22 ⭐⭐ 🟢 Range sum of a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is a BST with distinct values (1 <= n <= 2*10^4). Return the sum of all values v with low <= v <= high. Use the BST order to skip whole subtrees (do not visit the left subtree when the node's value is <= low, and the right when it is >= high) and say what that saves compared with summing all n nodes with a full traversal. Write it recursively and iteratively. Example: root=[10, 5, 15, 3, 7, null, 18], low=7, high=15 -> 32; root=[10, 5, 15, 3, 7, 13, 18, 1, null, 6], low=6, high=10 -> 23; root=[10], low=11, high=20 -> 0; root=[10, 5, 15], low=5, high=5 -> 5.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST order lets you discard whole subtrees. A plain traversal ignores that order.

**Say this first (1 line):** "At each node, add it if it is in range, go left only if the node is above low, go right only if it is below high; I visit the in-range nodes plus two boundary paths."

**Brute force:** Traverse all n nodes and add values in range. O(n) time, O(h) stack.

**Optimal:**
- If `node.val <= low`, everything in the left subtree is smaller than `node.val`, so strictly below low: skip it. If `node.val >= high`, skip the right subtree the same way.
- Otherwise visit both sides. A node with `low < val < high` is always inside and both children matter.
- Saving: the visited nodes are the in-range ones (k of them) plus the nodes on the paths that bound the range, at most 2h. So O(k + h) instead of O(n). My exhaustive run (every BST shape up to 7 nodes, every low and high) never exceeded k + 2h.
- The worst case is still O(n): when the range covers everything, k = n.

**Complexity:** Time O(k + h) where k is the count of in-range nodes, worst case O(n). Space O(h) for the recursion or the explicit stack. On a skewed tree h = n.

**Dry run:** Root `[10, 5, 15, 3, 7, null, 18]`, low = 7, high = 15. Visit 10: in range, add 10; 10 > 7 so go left, 10 < 15 so go right. Visit 5: not in range; 5 <= 7 so skip its left; 5 < 15 so go right. Visit 7: add 7; 7 <= 7 so skip left; 7 < 15 go right (None). Visit 15: add 15; 15 > 7 go left (None); 15 >= 15 skip right. Sum = 10 + 7 + 15 = 32. Visited 4 of 6 nodes (3 and 18 were skipped).

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def range_sum_full(root, low, high):
    """Brute force: visit every node."""
    return sum(n.val for n in nodes_of(root) if low <= n.val <= high)

VISITED = [0]
def range_sum_rec(root, low, high):
    """Prune with the BST order. Recursion depth = height (can be 2*10^4 on a skewed tree: see iterative)."""
    if root is None: return 0
    VISITED[0] += 1
    total = root.val if low <= root.val <= high else 0
    if root.val > low:  total += range_sum_rec(root.left, low, high)    # left values < root.val; useful only if root.val > low
    if root.val < high: total += range_sum_rec(root.right, low, high)   # right values > root.val; useful only if root.val < high
    return total

def range_sum_iter(root, low, high):
    total, visited, st = 0, 0, [root] if root else []
    while st:
        n = st.pop(); visited += 1
        if low <= n.val <= high: total += n.val
        if n.val > low and n.left:  st.append(n.left)
        if n.val < high and n.right: st.append(n.right)
    return total, visited

for arr, lo, hi, exp in [([10, 5, 15, 3, 7, None, 18], 7, 15, 32), ([10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10, 23),
                         ([10], 11, 20, 0), ([10, 5, 15], 5, 5, 5)]:
    r = build_tree(arr)
    VISITED[0] = 0
    a, b, c = range_sum_rec(r, lo, hi), range_sum_iter(r, lo, hi)[0], range_sum_full(r, lo, hi)
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, lo, hi, "->", a, "| visited", VISITED[0], "of", len(nodes_of(r)))

# exhaustive: every BST shape up to 7 nodes (values 0..n-1 in inorder), every low <= high in a slightly wider range.
# Also test the visit-count claim: visited <= (nodes inside [low, high]) + 2 * height.
cases = worst_extra = 0
for n in range(1, 8):
    for s in shapes(n):
        r = from_tup(label_inorder(s)); h = height(r)
        for low in range(-1, n + 1):
            for high in range(low, n + 1):
                VISITED[0] = 0
                a = range_sum_rec(r, low, high); b, vis = range_sum_iter(r, low, high)
                assert a == b == range_sum_full(r, low, high) and VISITED[0] == vis
                inside = sum(1 for v in range(n) if low <= v <= high)
                assert vis <= inside + 2 * h, (s, low, high)
                worst_extra = max(worst_extra, vis - inside); cases += 1
print("exhaustive ok:", cases, "(tree, low, high) cases; largest visited-minus-inside =", worst_extra)

# random big-ish BSTs (random insertion order) vs brute force
def insert(root, v):
    if root is None: return TreeNode(v)
    cur = root
    while True:
        if v < cur.val:
            if cur.left is None: cur.left = TreeNode(v); break
            cur = cur.left
        else:
            if cur.right is None: cur.right = TreeNode(v); break
            cur = cur.right
    return root
random.seed(22)
for _ in range(300):
    vals = random.sample(range(-100, 100), random.randint(1, 60)); r = None
    for v in vals: r = insert(r, v)
    lo = random.randint(-110, 110); hi = random.randint(lo, 110)
    assert range_sum_rec(r, lo, hi) == range_sum_iter(r, lo, hi)[0] == range_sum_full(r, lo, hi) == sum(v for v in vals if lo <= v <= hi)
print("random cross-check ok (300 trees)")

# deep skewed tree, n = 2*10^4: recursion fails under the default limit, the iterative one is fine
chain = None
for v in range(20000, 0, -1): chain = TreeNode(v, None, chain)      # right chain 1..20000 (a valid BST)
try:
    range_sum_rec(chain, 5, 20000); print("recursive: no error")
except RecursionError:
    print("recursive on a 20000-node chain: RecursionError (default limit 1000)")
print("iterative on the same chain (sum, visited):", range_sum_iter(chain, 5, 20000))
assert range_sum_iter(chain, 5, 20000)[0] == sum(range(5, 20001))
print("pruned query [5, 10] on the chain visits", range_sum_iter(chain, 5, 10)[1], "nodes (the right spine stops once val >= high)")
```

**Output (my run):**
```
[10, 5, 15, 3, 7, None, 18] 7 15 -> 32 | visited 4 of 6
[10, 5, 15, 3, 7, 13, 18, 1, None, 6] 6 10 -> 23 | visited 4 of 9
[10] 11 20 -> 0 | visited 1 of 1
[10, 5, 15] 5 5 -> 5 | visited 2 of 3
exhaustive ok: 25628 (tree, low, high) cases; largest visited-minus-inside = 7
random cross-check ok (300 trees)
recursive on a 20000-node chain: RecursionError (default limit 1000)
iterative on the same chain (sum, visited): (200009990, 20000)
pruned query [5, 10] on the chain visits 10 nodes (the right spine stops once val >= high)
```

**Edge cases:**
- low == high: the answer is that value if present, and the walk is just the search path.
- Range outside the tree: you still walk one boundary path, and the sum is 0.
- Range covers all values: all n nodes are visited; no saving.
- Skewed tree: the recursion depth is n. At n = 2 * 10^4 the recursive version raised RecursionError in my run with the default limit, so for this size prefer the iterative one.
- Values in the prompt are distinct; with duplicates the "skip left when val <= low" rule would be wrong.

**Follow-ups:**
- Count instead of sum? Same walk, add 1.
- Many queries? Store subtree sizes or sums per node (an order-statistic style augmentation) to answer in O(h).
- Why is `val <= low` safe and not `val < low`? Left values are strictly smaller than `val`, so at `val == low` they are all below low.

**Common mistakes:**
- Testing only `if val < low: go right` and `elif val > high: go left`, and forgetting that an in-range node needs both sides.
- Adding the node's value before checking the range.
- Recursing into both children and filtering later, which is the O(n) brute force in disguise.

### Q23 ⭐⭐ 🟢 Insert into a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a BST with distinct values (0 <= n <= 10^4) and a value `val` that is not already in it, insert `val` as a new LEAF at the position the search for it ends (so the result is unique) and return the root. Write the iterative version in O(h) time and O(1) space, handling the empty tree. Say what happens to the cost when you insert a sorted sequence one by one into an empty tree, and how many nodes that tree has on its longest path. Example: root=[4, 2, 7, 1, 3], val=5 -> [4, 2, 7, 1, 3, 5]; root=[], val=5 -> [5]; root=[40, 20, 60, 10, 30, 50, 70], val=25 -> [40, 20, 60, 10, 30, 50, 70, null, null, 25]; root=[1], val=0 -> [1, 0].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST search path. The new value goes where an unsuccessful search for it would end.

**Say this first (1 line):** "Walk down comparing with each node, left if smaller and right if larger, until the next child is empty; attach the new leaf there and return the original root."

**Brute force:** Flatten to a sorted list, insert, rebuild a tree from the sorted list. O(n) time and space, and it reshapes the tree, so the result is not the leaf insert the question asks for.

**Optimal:**
- Empty tree: the new node is the root.
- Otherwise `cur = root`. If `val < cur.val` and `cur.left` is empty, attach there, else step left. Mirror for the right.
- Only one pointer is written, so every old node keeps its identity and the root object is returned unchanged (checked by node identity in the run: exactly one new node, and it is a leaf).
- Iterative, so O(1) extra space and no recursion limit.

**Complexity:** Time O(h), space O(1). h is about log n for a balanced tree and n for a chain.

**Sorted insertions:** Insert 0, 1, 2, ... one by one. Value k is bigger than everything, so it walks down the whole right chain of k nodes: k node visits. Total 0 + 1 + ... + (n-1) = n(n-1)/2 = O(n^2). The tree is a single right chain with n nodes on its longest path. The run confirmed this: n = 500 gives 124750 visits and a longest path of 500. A shuffled order of 2000 values gave height 23 in my run. Self-balancing trees (AVL, red-black) avoid the chain; Python has no built-in one.

**Dry run:** `[4, 2, 7, 1, 3]`, val = 5. At 4: 5 > 4, go right to 7. At 7: 5 < 7, left is empty, attach. Level order `[4, 2, 7, 1, 3, 5]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def insert_iter(root, val):
    """Iterative leaf insert; O(h) time, O(1) extra space. Returns the root."""
    node = TreeNode(val)
    if root is None: return node
    cur = root
    while True:
        if val < cur.val:
            if cur.left is None: cur.left = node; return root
            cur = cur.left
        else:                       # val > cur.val (values are distinct and val is not in the tree)
            if cur.right is None: cur.right = node; return root
            cur = cur.right

def insert_tuple(t, val):
    """Independent brute force on tuple trees (recursive, rebuilds the path)."""
    if t is None: return (val, None, None)
    if val < t[0]: return (t[0], insert_tuple(t[1], val), t[2])
    return (t[0], t[1], insert_tuple(t[2], val))

for arr, v, exp in [([4, 2, 7, 1, 3], 5, [4, 2, 7, 1, 3, 5]), ([], 5, [5]),
                    ([40, 20, 60, 10, 30, 50, 70], 25, [40, 20, 60, 10, 30, 50, 70, None, None, 25]), ([1], 0, [1, 0])]:
    r = build_tree(arr); old = nodes_of(r); old_ids = {id(n) for n in old}
    out = insert_iter(r, v)
    assert to_arr(out) == exp, (arr, to_arr(out))
    new = [n for n in nodes_of(out) if id(n) not in old_ids]
    assert len(new) == 1 and new[0].val == v and new[0].left is None and new[0].right is None   # exactly one new LEAF
    if r is not None: assert out is r                                                             # same root object
    print(arr, "insert", v, "->", to_arr(out))

# exhaustive: every BST shape up to 6 nodes (values 0, 2, 4, ...), insert every odd gap value and the two ends
cases = 0
for n in range(0, 7):
    for s in shapes(n):
        t = label_inorder(s)
        def scale(x): return None if x is None else (2 * x[0], scale(x[1]), scale(x[2]))
        t = scale(t)
        for v in range(-1, 2 * n, 2):
            r = from_tup(t); old_ids = {id(x) for x in nodes_of(r)}
            out = insert_iter(r, v)
            assert tup(out) == insert_tuple(t, v)
            assert len([x for x in nodes_of(out) if id(x) not in old_ids]) == 1
            if r: assert out is r
            cases += 1
print("exhaustive ok:", cases, "(shape, value) cases")

# sorted insertion: node k (0-based) is placed after visiting k nodes, so total visits = n(n-1)/2 and the tree is one chain
def insert_counting(root, val):
    visits = 0
    node = TreeNode(val)
    if root is None: return node, 0
    cur = root
    while True:
        visits += 1
        if val < cur.val:
            if cur.left is None: cur.left = node; return root, visits
            cur = cur.left
        else:
            if cur.right is None: cur.right = node; return root, visits
            cur = cur.right
for n in (1, 2, 10, 500):
    root, total = None, 0
    for v in range(n):
        root, c = insert_counting(root, v); total += c
    assert total == n * (n - 1) // 2 and height(root) == n
    print("n =", n, "sorted inserts: visits =", total, "= n(n-1)/2, longest path =", height(root), "nodes")

# a shuffled order gives a much shorter tree (sandbox number, one seed)
random.seed(23)
vals = list(range(2000)); random.shuffle(vals); root = None
for v in vals: root = insert_iter(root, v)
print("2000 shuffled inserts: height =", height(root), "(sorted order would give 2000)")
```

**Output (my run):**
```
[4, 2, 7, 1, 3] insert 5 -> [4, 2, 7, 1, 3, 5]
[] insert 5 -> [5]
[40, 20, 60, 10, 30, 50, 70] insert 25 -> [40, 20, 60, 10, 30, 50, 70, None, None, 25]
[1] insert 0 -> [1, 0]
exhaustive ok: 1275 (shape, value) cases
n = 1 sorted inserts: visits = 0 = n(n-1)/2, longest path = 1 nodes
n = 2 sorted inserts: visits = 1 = n(n-1)/2, longest path = 2 nodes
n = 10 sorted inserts: visits = 45 = n(n-1)/2, longest path = 10 nodes
n = 500 sorted inserts: visits = 124750 = n(n-1)/2, longest path = 500 nodes
2000 shuffled inserts: height = 23 (sorted order would give 2000)
```

**Edge cases:**
- Empty tree: return the new node.
- Value smaller than the minimum or larger than the maximum: leaf at the far left or right.
- The value is already present (excluded by the prompt): the code would put it on the right; decide the duplicate rule explicitly in a real interview.
- Skewed tree: O(n) per insert, and the iterative loop has no recursion problem.

**Follow-ups:**
- Recursive version? `if not root: return TreeNode(v)`, then `root.left = insert(root.left, v)`. Same O(h), but O(h) stack, and it rewrites pointers on the whole path.
- How do you keep it balanced? Rotations after the insert (AVL, red-black), or a treap with random priorities.
- Is the leaf-insert result unique? Yes. Any BST insertion that keeps old nodes in place must put the node at the end of the search path, so only one leaf position exists.

**Common mistakes:**
- Returning the new node instead of the root.
- Forgetting the empty tree.
- Walking with `cur = cur.left` without a stop condition and falling off the tree into None.
- Using `<=` and `>` in a way that silently inserts duplicates on one side.

### Q24 ⭐⭐ 🟢 Complexity of traversals: time O(n), space O(h) or O(n). Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Write a function that returns the tuple (visits, max_recursion_depth, max_stack, max_queue) for a tree: visits is the number of nodes visited by a full traversal; max_recursion_depth is the largest number of simultaneously active calls of a recursive inorder that is only ever called on non-null nodes; max_stack is the largest `len(stack)` of the iterative inorder `while stack or cur: while cur: stack.append(cur); cur = cur.left; cur = stack.pop(); visit(cur); cur = cur.right`; max_queue is the largest `len(queue)` of a level-order loop that starts with deque([root]), pops from the left and appends non-null children (measured after each append). Explain from the results why recursion and stack space is O(h) (h = height in nodes) while a queue needs O(w) for the widest level w, and which of the two is O(n) on a skewed tree and which on a perfect tree. Example: root=[1, 2, 3, 4, 5, 6, 7] -> (7, 3, 3, 4); root=[1, 2, null, 3, null, 4] -> (4, 4, 4, 1); root=[1, null, 2, null, 3, null, 4] -> (4, 4, 1, 1); root=[] -> (0, 0, 0, 0).
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Python recursion-limit explainers (techinterview.org depth-of-a-tree page, a OneUptime guide, DataCamp DFS tutorial; snippets only, not opened: default limit 1000, raising it risks a crash, explicit stack preferred)

**Pattern:** Measure space, not just time. Depth-first traversals hold a path (height); breadth-first holds a level (width).

**Say this first (1 line):** "Every traversal visits n nodes, so time is O(n); DFS space is the height h because it holds one root-to-node path, BFS space is the widest level w."

**Brute force:** Nothing to brute force. The measured version below is the instrument: run the three loops and record the peaks, and check them against the claims on every tree shape up to 8 nodes.

**Optimal (what the numbers say):**
- Recursion depth is exactly h in nodes (checked on 2056 shapes). The call for a node stays active until its whole subtree is done, so the active calls are one root-to-node path.
- The explicit inorder stack holds the left spine plus ancestors still waiting for a visit. It is never more than h. It is exactly h on a left chain and just 1 on a right chain, because a right child is not pushed until its parent has been popped.
- The queue holds the unfinished part of one level and the started part of the next. Its peak is at least the widest level w (checked) and at most n.
- Perfect tree with k levels (n = 2^k - 1): h = k, w = 2^(k-1), so DFS needs O(log n) and the queue needs about n/2: O(n).
- Skewed tree: h = n, w = 1, so recursion and a left-leaning stack are O(n) while the queue is O(1).

**Complexity:** Time O(n) for all three (each node is pushed once, popped once). Space: recursion and stack O(h), queue O(w). h ranges from log n to n, w from 1 to about n/2.

**Dry run:** `[1, 2, 3, 4, 5, 6, 7]` (perfect, 3 levels). Recursion: calls 1, 2, 4 are active at once, depth 3. Stack: push 1, 2, 4, size 3; pop 4, push nothing; pop 2, push 5 (size 2); and so on, peak 3. Queue: after popping 1 it holds 2, 3; after popping 2 it holds 3, 4, 5; after popping 3 it holds 4, 5, 6, 7, peak 4. Result `(7, 3, 3, 4)`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def metrics(root):
    """(visits, max_recursion_depth, max_stack, max_queue). Empty tree -> all zeros.
    max_queue counts the initial deque([root]) (length 1) too, so a single node gives 1."""
    if root is None: return (0, 0, 0, 0)
    # recursive inorder, only called on non-null nodes: count simultaneously active calls
    live = peak = visits = 0
    def rec(n):
        nonlocal live, peak, visits
        live += 1; peak = max(peak, live)
        if n.left: rec(n.left)
        visits += 1
        if n.right: rec(n.right)
        live -= 1
    rec(root)
    # iterative inorder, exactly the loop in the prompt
    stack, cur, mx_stack, v2 = [], root, 0, 0
    while stack or cur:
        while cur:
            stack.append(cur); mx_stack = max(mx_stack, len(stack)); cur = cur.left
        cur = stack.pop(); v2 += 1; cur = cur.right
    # level order with a deque
    q, mx_q, v3 = deque([root]), 1, 0
    while q:
        n = q.popleft(); v3 += 1
        for c in (n.left, n.right):
            if c is not None:
                q.append(c); mx_q = max(mx_q, len(q))
    assert visits == v2 == v3
    return (visits, peak, mx_stack, mx_q)

for arr, exp in [([1, 2, 3, 4, 5, 6, 7], (7, 3, 3, 4)), ([1, 2, None, 3, None, 4], (4, 4, 4, 1)),
                 ([1, None, 2, None, 3, None, 4], (4, 4, 1, 1)), ([], (0, 0, 0, 0))]:
    got = metrics(build_tree(arr)); assert got == exp, (arr, got); print(arr, "->", got)

def widest(root):
    best, level = 0, [root] if root else []
    while level:
        best = max(best, len(level)); level = [c for n in level for c in (n.left, n.right) if c]
    return best

# exhaustive over every shape with 0..8 nodes: recursion depth = h exactly, stack <= h, w <= queue <= n
cnt = 0
for n in range(0, 9):
    for s in shapes(n):
        r = from_tup(label_inorder(s)); v, rd, ms, mq = metrics(r); h, w = height(r), widest(r)
        assert v == n and rd == h and ms <= h and w <= mq <= n, (s, v, rd, ms, mq, h, w)
        if n: assert mq >= 1
        cnt += 1
print("exhaustive ok on", cnt, "tree shapes: visits = n, recursion depth = h, stack <= h, widest level <= queue <= n")

# the three shapes the question asks about, at n = 255 / 256 nodes (sandbox numbers)
def perfect(k):   # k levels
    return None if k == 0 else TreeNode(1, perfect(k - 1), perfect(k - 1))
def left_chain(n):
    r = None
    for _ in range(n): r = TreeNode(1, r, None)
    return r
def right_chain(n):
    r = None
    for _ in range(n): r = TreeNode(1, None, r)
    return r
print("perfect, 8 levels, n = 255:", metrics(perfect(8)), "(h = 8, widest level = 128)")
print("left chain, n = 200      :", metrics(left_chain(200)), "(h = 200, w = 1)")
print("right chain, n = 200     :", metrics(right_chain(200)), "(h = 200, w = 1)")
assert metrics(left_chain(200)) == (200, 200, 200, 1) and metrics(right_chain(200))[2:] == (1, 1)
# perfect tree: test the exact queue peak for k = 1..9
for k in range(1, 10):
    got = metrics(perfect(k))
    assert got[1] == got[2] == k and got[3] == max(1, 2 ** (k - 1)), (k, got)
print("perfect trees k = 1..9: queue peak = 2^(k-1) exactly, recursion = stack = k")
# Python limit: recursion of depth 1500 on a left chain fails by default; the explicit-stack loop does not
try:
    metrics(left_chain(1500)); print("no error")
except RecursionError:
    print("recursive inorder on a 1500-node chain: RecursionError")
```

**Output (my run):**
```
[1, 2, 3, 4, 5, 6, 7] -> (7, 3, 3, 4)
[1, 2, None, 3, None, 4] -> (4, 4, 4, 1)
[1, None, 2, None, 3, None, 4] -> (4, 4, 1, 1)
[] -> (0, 0, 0, 0)
exhaustive ok on 2056 tree shapes: visits = n, recursion depth = h, stack <= h, widest level <= queue <= n
perfect, 8 levels, n = 255: (255, 8, 8, 128) (h = 8, widest level = 128)
left chain, n = 200      : (200, 200, 200, 1) (h = 200, w = 1)
right chain, n = 200     : (200, 200, 1, 1) (h = 200, w = 1)
perfect trees k = 1..9: queue peak = 2^(k-1) exactly, recursion = stack = k
recursive inorder on a 1500-node chain: RecursionError
```

**Edge cases:**
- Empty tree: `(0, 0, 0, 0)`.
- Single node: the prompt says to measure the queue "after each append", which would give 0 here (no append happens). My function counts the initial `deque([root])` too, so a single node gives a queue peak of 1. Say which convention you use; it only matters for trees with no appended children.
- Python's default recursion limit is 1000: a 1500-node left chain raised RecursionError in the recursive inorder, while the explicit stack handled it (it only needs memory, not frames). The Part 4 Q25 answer covers this trade-off.
- Morris traversal gets O(1) extra space at the cost of temporarily changing pointers.

**Follow-ups:**
- Which is better on a wide shallow tree? DFS, since the stack is only h. On a deep thin tree BFS is better.
- Can iterative DFS beat O(h)? Morris traversal does O(1) extra by threading, at the cost of modifying the tree while it runs.
- Does the output count of a traversal (the result list) count as space? It is O(n) for storing it; "extra space" excludes it.

**Common mistakes:**
- Saying "recursion is O(1) space". The call stack is O(h).
- Calling the BFS queue O(h). It is O(w).
- Using n for recursion depth on a balanced tree, or log n on an unbalanced one.
- Forgetting that a right chain keeps the inorder stack at size 1.

### Q25 ⭐⭐ 🟡 Zigzag level-order traversal. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the levels top to bottom, but the first level left to right, the second right to left, the third left to right, and so on (0 <= n <= 2000). Do a normal BFS and reverse alternate levels (or fill a deque from alternating ends) rather than reversing the queue, and explain why the queue itself must stay in left-to-right order. Example: root=[3, 9, 20, null, null, 15, 7] -> [[3], [20, 9], [15, 7]]; root=[1, 2, 3, 4, null, null, 5] -> [[1], [3, 2], [4, 5]]; root=[1] -> [[1]]; root=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BFS with a level snapshot (`for _ in range(len(q))`), then a per-level direction flag. Part 4 Q30 has the same queue idiom.

**Say this first (1 line):** "Normal BFS, children always enqueued left then right, and only the order I write each level into the output flips on odd levels."

**Brute force:** Do plain level order, then reverse every odd-numbered level in a second pass. O(n) time and space. It is perfectly good; it just takes two passes over the levels.

**Optimal:**
- Keep `left_to_right` as a flag. For each level pop `len(q)` nodes. If the flag is true, `append` the value to a deque for this level, otherwise `appendleft`. Convert it to a list when the level ends.
- Enqueue `left` then `right` for every node, whatever the direction.
- Why the queue must stay left to right: level d+1 in the queue must be ordered by the parents' order in level d. If you reverse the queue, the parents are processed in reversed order and their children are enqueued in the wrong order. Then the next level, which should be reversed again, comes out wrong. In my run the "reverse the queue" version gives `[[1], [3, 2], [5, 4]]` instead of `[[1], [3, 2], [4, 5]]` on the second example, and it was wrong on 573 of 2056 shapes.
- `appendleft` on a deque is O(1); `list.insert(0, x)` would be O(level width) each.

**Complexity:** Time O(n), space O(w) for the queue plus O(n) for the output.

**Dry run:** `[1, 2, 3, 4, null, null, 5]`. Level 0: pop 1, left to right, `[1]`; enqueue 2, 3. Level 1 (flag false): pop 2, `appendleft` gives `[2]`; enqueue 4; pop 3, `appendleft` gives `[3, 2]`; enqueue 5. Level 2 (flag true): pop 4, 5 giving `[4, 5]`. Result `[[1], [3, 2], [4, 5]]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def zigzag(root):
    """BFS; the queue is ALWAYS filled left to right; only the output of each level is reversed or not."""
    if root is None: return []
    out, q, left_to_right = [], deque([root]), True
    while q:
        level = deque()
        for _ in range(len(q)):                     # snapshot: exactly one level
            n = q.popleft()
            if left_to_right: level.append(n.val)   # fill the output from alternating ends
            else:             level.appendleft(n.val)
            if n.left:  q.append(n.left)            # children always left then right
            if n.right: q.append(n.right)
        out.append(list(level)); left_to_right = not left_to_right
    return out

def zigzag_reverse_levels(root):
    """Alternative: normal level order, then reverse every odd level."""
    out, level = [], [root] if root else []
    while level:
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]
    return [l[::-1] if i % 2 else l for i, l in enumerate(out)]

def zigzag_wrong(root):
    """BUG: reverse the queue itself on odd levels. The children then enter in the wrong order for the next level."""
    if root is None: return []
    out, level, flip = [], [root], False
    while level:
        if flip: level = level[::-1]               # reversing the nodes ...
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]   # ... changes who is enqueued first
        flip = not flip
    return out

def zig_tuple(t):
    """Independent brute force on tuple trees: collect (depth, left-to-right index) then regroup."""
    levels = {}
    def go(t, d):
        if t is None: return
        levels.setdefault(d, []).append(t[0]); go(t[1], d + 1); go(t[2], d + 1)   # preorder keeps left-to-right order per level
    go(t, 0)
    return [levels[d][::-1] if d % 2 else levels[d] for d in sorted(levels)]

for arr, exp in [([3, 9, 20, None, None, 15, 7], [[3], [20, 9], [15, 7]]), ([1, 2, 3, 4, None, None, 5], [[1], [3, 2], [4, 5]]),
                 ([1], [[1]]), ([], [])]:
    r = build_tree(arr); got = zigzag(r)
    assert got == zigzag_reverse_levels(r) == exp, (arr, got)
    print(arr, "->", got)
print("reversing the queue (bug) on [1,2,3,4,None,None,5]:", zigzag_wrong(build_tree([1, 2, 3, 4, None, None, 5])))

# exhaustive: all shapes with 0..8 nodes (values 0..n-1 by inorder, distinct), compare three solutions + brute force
cnt = bad = 0
for n in range(0, 9):
    for s in shapes(n):
        t = label_inorder(s); r = from_tup(t)
        assert zigzag(r) == zigzag_reverse_levels(r) == zig_tuple(t)
        if zigzag_wrong(r) != zigzag(r): bad += 1
        cnt += 1
print("exhaustive ok on", cnt, "shapes; the 'reverse the queue' bug is wrong on", bad, "of them")
random.seed(25)
for _ in range(200):
    n = random.randint(0, 60); arr = [random.choice([None, random.randint(0, 9)]) for _ in range(n)]
    if arr: arr[0] = 1
    r = build_tree(arr); assert zigzag(r) == zigzag_reverse_levels(r)
print("random cross-check ok (200 arrays)")
big = build_tree([1] * 2000)    # a bushy tree with 2000 nodes
assert sum(len(l) for l in zigzag(big)) == 2000
print("n = 2000 bushy tree: levels =", len(zigzag(big)))
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> [[3], [20, 9], [15, 7]]
[1, 2, 3, 4, None, None, 5] -> [[1], [3, 2], [4, 5]]
[1] -> [[1]]
[] -> []
reversing the queue (bug) on [1,2,3,4,None,None,5]: [[1], [3, 2], [5, 4]]
exhaustive ok on 2056 shapes; the 'reverse the queue' bug is wrong on 573 of them
random cross-check ok (200 arrays)
n = 2000 bushy tree: levels = 11
```

**Edge cases:**
- Empty tree: return `[]` (guard before the loop).
- Single node: `[[1]]`.
- Skewed tree: every level has one node, so zigzag equals plain level order.
- Missing children in the middle of a level: handled, since only existing children are enqueued.

**Follow-ups:**
- Do it with two stacks? Possible (left then right into one stack, right then left into the other), but it is harder to read than the flag.
- Right-to-left only? Enqueue right then left, or reverse each level.
- DFS version? Pass the depth, append to `levels[depth]`, and reverse odd levels at the end.

**Common mistakes:**
- Flipping the queue direction instead of the output direction.
- Forgetting the level snapshot and mixing levels.
- Using `list.insert(0, ...)` and quietly making it O(n^2) on a wide level.
- Toggling the flag inside the node loop instead of once per level.

### Q26 ⭐⭐ 🟡 Path sum II: list the root-to-leaf paths. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return every path from the ROOT to a LEAF whose values sum to `target`, as lists of values, ordered by the left-to-right order of their leaves (0 <= n <= 5000, values may be negative). Use backtracking on one shared `path` list (append, recurse, pop) and copy it only when a match is found; explain why storing the list without copying is a bug, and the cost of copying in terms of the number of matches and the path length. Example: root=[5, 4, 8, 11, null, 13, 4, 7, 2, null, null, 5, 1], target=22 -> [[5, 4, 11, 2], [5, 8, 4, 5]]; root=[1, 2, 3], target=5 -> []; root=[1, 2], target=0 -> []; root=[], target=0 -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** DFS with backtracking on one shared path list. Choose, recurse, undo.

**Say this first (1 line):** "One shared `path`: append the node, recurse, pop on the way out; at a real leaf with remaining sum 0 I copy the path into the answer."

**Brute force:** Build every root-to-leaf path as a new list (a new list per node, `path + [val]`), then filter by sum. O(n * h) time and space in the worst case, because each node copies a path of length up to h.

**Optimal:**
- `go(node, rem)`: append `node.val`, subtract it from `rem`. If the node is a leaf (no left and no right) and `rem == 0`, record `path[:]`. Otherwise recurse left then right. Finally `path.pop()`.
- A leaf means both children missing. `[1, 2]` with target 1 is not a match: 1 has one child, so 1 alone is not a root-to-leaf path. The run shows target 3 matches `[[1, 2]]`.
- Left before right gives the left-to-right leaf order the prompt asks for.
- Do not prune on `rem < 0`, because values can be negative.
- Why copying matters: the answer would hold the same list object that keeps being mutated. In my run the buggy version printed `[[], []]` (two references to one list, emptied by the pops) for the first example. `path[:]` snapshots the current contents.
- Cost of copying: k matches of length up to h cost O(k * h) extra, on top of the O(n) walk. The walk itself does O(1) work per node (append and pop), so the total is O(n + k * h).

**Complexity:** Time O(n + k * L) with k matching paths of length L at most h. Space O(h) for the path and the recursion, plus the output.

**Dry run:** Example 1 with target 22. Path 5, 4, 11, 7: leaf 7, sum 27, no. Pop 7, go to 2: path 5, 4, 11, 2 sums to 22, copy it. Backtrack to 5, go right: 8, 13 (26, no), 4, then 5 gives 5 + 8 + 4 + 5 = 22, copy; then 1 gives 18, no. Result `[[5, 4, 11, 2], [5, 8, 4, 5]]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def path_sum_rec(root, target):
    """Backtracking on ONE shared path list. Recursive: depth = height (fails on a 5000-node chain by default)."""
    res, path = [], []
    def go(n, rem):
        if n is None: return
        path.append(n.val); rem -= n.val
        if n.left is None and n.right is None:
            if rem == 0: res.append(path[:])          # COPY here; path keeps changing afterwards
        else:
            go(n.left, rem); go(n.right, rem)
        path.pop()                                    # undo on the way out
    go(root, target)
    return res

def path_sum_iter(root, target):
    """Same idea with an explicit stack of (node, entered?) pairs: no recursion limit."""
    res, path, st, rem = [], [], [(root, False)] if root else [], 0
    while st:
        n, done = st.pop()
        if done:
            path.pop(); rem -= n.val; continue
        path.append(n.val); rem += n.val              # rem is now the running sum from the root
        st.append((n, True))
        if n.left is None and n.right is None:
            if rem == target: res.append(path[:])
        else:
            if n.right: st.append((n.right, False))   # push right first so left is processed first
            if n.left:  st.append((n.left, False))
    return res

def path_sum_buggy(root, target):
    """BUG: appends the shared list itself instead of a copy."""
    res, path = [], []
    def go(n, rem):
        if n is None: return
        path.append(n.val); rem -= n.val
        if n.left is None and n.right is None:
            if rem == 0: res.append(path)             # <- same list object every time
        else:
            go(n.left, rem); go(n.right, rem)
        path.pop()
    go(root, target)
    return res

def leaf_paths(t, pre=()):
    """Independent brute force on tuple trees: every root-to-leaf path, then filter."""
    if t is None: return []
    p = pre + (t[0],)
    if t[1] is None and t[2] is None: return [list(p)]
    return leaf_paths(t[1], p) + leaf_paths(t[2], p)

for arr, tg, exp in [([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22, [[5, 4, 11, 2], [5, 8, 4, 5]]),
                     ([1, 2, 3], 5, []), ([1, 2], 0, []), ([], 0, [])]:
    r = build_tree(arr); a, b = path_sum_rec(r, tg), path_sum_iter(r, tg)
    assert a == b == exp, (arr, a, b)
    print(arr, "target", tg, "->", a)
print("[1, 2] with target 3 ->", path_sum_rec(build_tree([1, 2]), 3), "(1 has one child, so 1 alone is not a leaf path; 1-2 is)")
print("bug (no copy), same first example:", path_sum_buggy(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22))

# exhaustive over all shapes 0..7 with several value labelings (values in -2..3) and every target in range
random.seed(26); cnt = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(4):
            vals = iter(random.randint(-2, 3) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return (v, L, lab(x[1]))
            t = lab(s); r = from_tup(t); allp = leaf_paths(t)
            for tg in range(-8, 12):
                exp = [p for p in allp if sum(p) == tg]
                assert path_sum_rec(r, tg) == path_sum_iter(r, tg) == exp
                cnt += 1
print("exhaustive+random ok:", cnt, "(tree, target) cases; order = left-to-right order of leaves")

# 5000-node chain: recursion fails by default, the explicit stack does not
chain = None
for _ in range(5000): chain = TreeNode(1, chain, None)
try:
    path_sum_rec(chain, 5000); print("recursive: no error")
except RecursionError:
    print("recursive on a 5000-node chain: RecursionError")
res = path_sum_iter(chain, 5000)
assert len(res) == 1 and len(res[0]) == 5000
print("iterative on the same chain: 1 path of length", len(res[0]))
# cost of copying: k matches of length L cost k * L extra. all-zero tree, target 0: every leaf matches
zeros31 = build_tree([0] * 31)       # 16 leaves, path length 5
print("perfect tree 31 nodes all zero, target 0: matches =", len(path_sum_rec(zeros31, 0)), "each of length 5")
```

**Output (my run):**
```
[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1] target 22 -> [[5, 4, 11, 2], [5, 8, 4, 5]]
[1, 2, 3] target 5 -> []
[1, 2] target 0 -> []
[] target 0 -> []
[1, 2] with target 3 -> [[1, 2]] (1 has one child, so 1 alone is not a leaf path; 1-2 is)
bug (no copy), same first example: [[], []]
exhaustive+random ok: 50080 (tree, target) cases; order = left-to-right order of leaves
recursive on a 5000-node chain: RecursionError
iterative on the same chain: 1 path of length 5000
perfect tree 31 nodes all zero, target 0: matches = 16 each of length 5
```

**Edge cases:**
- Empty tree: `[]`, even for target 0 (there is no path).
- Node with one child is not a leaf.
- Negative or zero values: no early pruning; 50080 (tree, target) cases agreed with the brute force.
- n = 5000 as a chain: the recursive version raised RecursionError in my run (default limit 1000); the explicit-stack version returned the one path of length 5000. Use it for the stated limit.

**Follow-ups:**
- Just return True or False (Path Sum I)? Drop the list and return `go(left) or go(right)` at the leaf test.
- Paths that do not start at the root? That is Part 7 Q27 (prefix sums).
- Why not pass `path + [val]` down? It is simpler and cannot alias, at O(h) copying per node: O(n * h) always, not only for matches.

**Common mistakes:**
- `res.append(path)` without a copy.
- Forgetting `path.pop()` on the leaf branch, so the path grows wrong.
- Treating a node with one child as a leaf.
- Pruning when the running sum goes above the target, which is wrong with negatives.

### Q27 ⭐⭐ 🟡 Path sum III: count downward paths with prefix sums. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Count the paths whose values sum to `target`, where a path goes downward from any node to any descendant (it need not start at the root or end at a leaf; a single node counts), values may be negative or zero, 0 <= n <= 1000. Beat the O(n * h) solution that starts a walk at every node with a prefix-sum dictionary: count[prefix] along the current root-to-node path, answer += count[prefix - target], and UNDO the count when you leave the node. The array version of this idea is Part 1 Q13; explain what breaks if you forget the undo. Example: root=[10, 5, -3, 3, 2, null, 11, 3, -2, null, 1], target=8 -> 3; root=[5, 4, 8, 11, null, 13, 4, 7, 2, null, null, 5, 1], target=22 -> 3; root=[1, -1], target=0 -> 1; root=[0, 0, null, 0], target=0 -> 6.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Prefix sums on a tree path, with a hash map that is updated when you enter a node and undone when you leave it. The array version is Part 1 Q13.

**Say this first (1 line):** "Along the current root-to-node path, a downward path ending here sums to target exactly when an earlier prefix equals prefix minus target, so I look that up in a counter and remove my own prefix when I leave."

**Brute force:** Start a downward walk at every node and count walks with sum equal to target. O(n * h) time, O(h) space: O(n^2) on a chain, O(n log n) on a balanced tree.

**Optimal:**
- `prefix` = sum from the root to the current node. `count[p]` = how many nodes on the CURRENT root-to-node path have prefix p (start with `count[0] = 1` for the empty prefix, so a path starting at the root counts).
- At a node: `ans += count[prefix - target]`; then `count[prefix] += 1`; recurse into both children; then `count[prefix] -= 1`.
- Why the undo: `count` must describe only the ancestors of the current node. A path has to go downward, so a node in the left subtree must not be matched against a prefix recorded in the right subtree.
- What breaks without it: stale prefixes from finished branches are counted as if they were ancestors, so you count "paths" that go up and over. In my run, `[1, 1, 1]` with target 0 gave 1 instead of 0, and forgetting the undo was wrong in 4934 of 24414 small cases.
- Values may be negative or zero, so you cannot shrink a window; the counter handles that.

**Complexity:** Time O(n): one visit per node, O(1) average per dictionary operation. Space O(h) for the path, the dictionary (at most h keys live) and the stack.

**Dry run:** `[1, -1]`, target 0. count = {0: 1}. Node 1: prefix 1, look up 1 - 0 = 1: none. count[1] = 1. Node -1: prefix 0, look up 0: count[0] = 1, so ans = 1 (the path 1, -1). Undo both. Answer 1.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def count_paths_brute(root, target):
    """O(n * h): start a downward walk at every node."""
    total = 0
    for start in nodes_of(root):
        st = [(start, start.val)]
        while st:
            n, s = st.pop()
            if s == target: total += 1
            for c in (n.left, n.right):
                if c: st.append((c, s + c.val))
    return total

def count_paths_prefix_rec(root, target, undo=True):
    """O(n): count[prefix] along the CURRENT root-to-node path. Recursion depth = height."""
    count = {0: 1}                                    # the empty prefix
    ans = 0
    def go(n, prefix):
        nonlocal ans
        if n is None: return
        prefix += n.val
        ans += count.get(prefix - target, 0)          # paths ending at n that start below some ancestor
        count[prefix] = count.get(prefix, 0) + 1
        go(n.left, prefix); go(n.right, prefix)
        if undo: count[prefix] -= 1                   # leaving n: the prefix is no longer on the path
    go(root, 0)
    return ans

def count_paths_prefix_iter(root, target):
    """Same, with an explicit stack of (node, prefix_before, entered?) so deep trees are fine."""
    count, ans = {0: 1}, 0
    st = [(root, 0, False)] if root else []
    while st:
        n, before, leaving = st.pop()
        prefix = before + n.val
        if leaving:
            count[prefix] -= 1; continue              # the undo
        ans += count.get(prefix - target, 0)
        count[prefix] = count.get(prefix, 0) + 1
        st.append((n, before, True))
        if n.right: st.append((n.right, prefix, False))
        if n.left:  st.append((n.left, prefix, False))
    return ans

cases = [([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8, 3), ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22, 3),
         ([1, -1], 0, 1), ([0, 0, None, 0], 0, 6)]
for arr, tg, exp in cases:
    r = build_tree(arr)
    a, b, c = count_paths_brute(r, tg), count_paths_prefix_rec(r, tg), count_paths_prefix_iter(r, tg)
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, "target", tg, "->", b)
print("empty tree ->", count_paths_prefix_iter(None, 0))
# find the smallest tree where forgetting the undo gives a wrong answer
found = None
for n in range(1, 6):
    for arr in ([1] * n, [1, 2, 3, 4, 5][:n], [1, 1, 1, 1, 1][:n]):
        r = build_tree(arr)
        for tg in range(0, 8):
            if found is None and count_paths_prefix_rec(r, tg, undo=False) != count_paths_brute(r, tg):
                found = (arr, tg, count_paths_prefix_rec(r, tg, undo=False), count_paths_brute(r, tg))
print("forgetting the undo, first failing case (array, target, buggy, true):", found)
assert found is not None

# exhaustive: all shapes up to 7 nodes, values drawn from {-2..2} (zeros and negatives), all targets -6..6
random.seed(27); cnt = 0; bug_wrong = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(3):
            vals = iter(random.randint(-2, 2) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return TreeNode(v, L, lab(x[1]))
            r = lab(s)
            for tg in range(-6, 7):
                e = count_paths_brute(r, tg)
                assert count_paths_prefix_rec(r, tg) == count_paths_prefix_iter(r, tg) == e
                if count_paths_prefix_rec(r, tg, undo=False) != e: bug_wrong += 1
                cnt += 1
print("exhaustive+random ok:", cnt, "cases; forgetting the undo was wrong in", bug_wrong, "of them")

# n = 1000 chain of ones, target 3: recursion depth 1000 hits the limit, the iterative one is fine
chain = None
for _ in range(1000): chain = TreeNode(1, chain, None)
try:
    count_paths_prefix_rec(chain, 3); print("recursive: no error")
except RecursionError:
    print("recursive on a 1000-node chain: RecursionError")
assert count_paths_prefix_iter(chain, 3) == 998 and count_paths_brute(chain, 3) == 998
print("iterative on the chain, target 3 ->", count_paths_prefix_iter(chain, 3), "(starts 998 down the chain)")
```

**Output (my run):**
```
[10, 5, -3, 3, 2, None, 11, 3, -2, None, 1] target 8 -> 3
[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1] target 22 -> 3
[1, -1] target 0 -> 1
[0, 0, None, 0] target 0 -> 6
empty tree -> 0
forgetting the undo, first failing case (array, target, buggy, true): ([1, 1, 1], 0, 1, 0)
exhaustive+random ok: 24414 cases; forgetting the undo was wrong in 4934 of them
recursive on a 1000-node chain: RecursionError
iterative on the chain, target 3 -> 998 (starts 998 down the chain)
```

**Edge cases:**
- Empty tree: 0.
- A single node equal to target: counts once, through `count[0]`.
- Zeros: `[0, 0, null, 0]` with target 0 gives 6 (every downward path of the 3-chain: 3 singles, 2 pairs, 1 triple).
- Depth: n up to 1000 makes the recursion depth 1000, and in my run the recursive version raised RecursionError on a 1000-node chain. The iterative version (enter/leave entries on a stack) worked and returned 998 for target 3.
- Large sums are fine, Python ints do not overflow.

**Follow-ups:**
- Why `count[0] = 1`? Otherwise paths that begin at the root are missed.
- What if you need the paths themselves? Use Part 7 Q26 style backtracking; the counter only gives a count.
- Why does the dictionary stay small? Undoing removes the prefixes of finished branches, so it holds at most h + 1 distinct keys at once.

**Common mistakes:**
- No undo.
- Missing the initial `{0: 1}`.
- Updating the counter before the lookup, which counts an empty path when target is 0.
- Looking up `prefix + target` instead of `prefix - target`.

### Q28 ⭐⭐ 🟡 Vertical order traversal. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Give the root column 0, a left child the column one less than its parent and a right child one more, and the root row 0 with each child one row below its parent. Return the values grouped by column from the leftmost to the rightmost; inside a column order by row (top first), and when two nodes share both row and column put the smaller value first. Use a BFS or DFS that records (column, row, value) and sort, or a BFS with a per-column bucket if the tie rule is first-come; state the cost of each (n up to 1000). A public candidate report describes a version of this problem where ties follow insertion order, so always ask which tie rule is wanted. Example: root=[3, 9, 20, null, null, 15, 7] -> [[9], [3, 15], [20], [7]]; root=[1, 2, 3, 4, 5, 6, 7] -> [[4], [2], [1, 5, 6], [3], [7]]; root=[3, 1, 4, 0, 2, 2] -> [[0], [1], [3, 2, 2], [4]]; root=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Coordinates on a tree: column (left minus 1, right plus 1) and row (depth). Group by column, order inside a column by row, then by the tie rule.

**Say this first (1 line):** "First ask which tie rule applies for same row and same column; then record (column, row, value) per node, sort, and group by column."

**Brute force:** For every node compute (column, row, value), then for every column scan all nodes and sort the ones in it. O(n * c) with c columns, O(n^2) worst case on a chain.

**Optimal:**
- One BFS (or DFS) collecting `(col, row, val)`. Sort the list: tuple order is column, row, value, which is exactly the rule in the prompt. Group consecutive equal columns.
- DFS works too because the sort puts rows back in order; BFS plus the sort is the same cost.
- Tie rule matters. With "smaller value first" you must sort by value. With "insertion order" (BFS first-come) you can skip the sort: BFS visits rows top to bottom and, within a row, left to right, so appending to a per-column bucket gives the right order, and the columns are the range min..max, O(n) in total. A public candidate report describes the insertion-order version, so ask.
- Example of the difference from my run: `[1, 2, 3, null, 5, 4]` has 5 and 4 in column 0, row 2. The sorted rule gives `[[2], [1, 4, 5], [3]]`, first-come gives `[[2], [1, 5, 4], [3]]`. On shapes up to 7 nodes with values 0 to 2, the two rules differed on 58 of 1878 trees.

**Complexity:** Sorted rule: O(n log n) time (the sort), O(n) space. First-come BFS: O(n) time, O(n) space. n = 1000 is tiny either way.

**Dry run:** `[3, 9, 20, null, null, 15, 7]`. 3 at (0, 0); 9 at (-1, 1); 20 at (1, 1); 15 at (0, 2); 7 at (2, 2). Sorted: (-1,1,9), (0,0,3), (0,2,15), (1,1,20), (2,2,7). Groups: `[[9], [3, 15], [20], [7]]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def vertical_sorted(root):
    """Walk with BFS, record (col, row, val), sort, group by column. O(n log n)."""
    if root is None: return []
    rec, q = [], deque([(root, 0, 0)])
    while q:
        n, col, row = q.popleft(); rec.append((col, row, n.val))
        if n.left:  q.append((n.left, col - 1, row + 1))
        if n.right: q.append((n.right, col + 1, row + 1))
    rec.sort()                                         # column, then row, then value (the tie rule)
    out, last = [], None
    for col, row, v in rec:
        if col != last: out.append([]); last = col
        out[-1].append(v)
    return out

def vertical_first_come(root):
    """BFS with per-column buckets. Ties (same row and column) keep BFS order = left-to-right. O(n)."""
    if root is None: return []
    buckets, q = {}, deque([(root, 0)])
    while q:
        n, col = q.popleft(); buckets.setdefault(col, []).append(n.val)
        if n.left:  q.append((n.left, col - 1))
        if n.right: q.append((n.right, col + 1))
    return [buckets[c] for c in range(min(buckets), max(buckets) + 1)]

def vertical_dfs(root):
    """DFS version (explicit stack): the sort puts rows back in order, so DFS visiting order does not matter."""
    rec, st = [], [(root, 0, 0)] if root else []
    while st:
        n, col, row = st.pop(); rec.append((col, row, n.val))
        if n.right: st.append((n.right, col + 1, row + 1))
        if n.left:  st.append((n.left, col - 1, row + 1))
    rec.sort(); cols = {}
    for c, r, v in rec: cols.setdefault(c, []).append(v)
    return [cols[c] for c in sorted(cols)]

def vertical_tuple(t):
    """Independent brute force on tuple trees: for each column, nodes sorted by (row, value)."""
    nodes = []
    def go(t, c, r):
        if t is None: return
        nodes.append((c, r, t[0])); go(t[1], c - 1, r + 1); go(t[2], c + 1, r + 1)
    go(t, 0, 0)
    return [[v for (cc, r, v) in sorted(x for x in nodes if x[0] == c)] for c in sorted({x[0] for x in nodes})]

for arr, exp in [([3, 9, 20, None, None, 15, 7], [[9], [3, 15], [20], [7]]),
                 ([1, 2, 3, 4, 5, 6, 7], [[4], [2], [1, 5, 6], [3], [7]]),
                 ([3, 1, 4, 0, 2, 2], [[0], [1], [3, 2, 2], [4]]), ([], [])]:
    r = build_tree(arr); a = vertical_sorted(r)
    assert a == vertical_dfs(r) == exp, (arr, a)
    print(arr, "->", a)

# exhaustive over shapes up to 7 nodes with values from {0,1,2} so ties on (col,row) with different values occur
random.seed(28); cnt = diff = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(3):
            vals = iter(random.randint(0, 2) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return (v, L, lab(x[1]))
            t = lab(s); r = from_tup(t)
            assert vertical_sorted(r) == vertical_dfs(r) == vertical_tuple(t)
            f = vertical_first_come(r)
            assert [sorted(c) for c in f] == [sorted(c) for c in vertical_sorted(r)]      # same groups, maybe different order inside a column
            assert [len(c) for c in f] == [len(c) for c in vertical_sorted(r)]
            if f != vertical_sorted(r): diff += 1
            cnt += 1
print("exhaustive+random ok:", cnt, "trees; first-come order differs from the sorted tie rule on", diff, "of them")
# one concrete difference
ex = build_tree([1, 2, 3, None, 5, 4])      # 5 and 4 share column 0 and row 2; 5 is left of 4 in BFS, but 4 < 5
print("tie example [1, 2, 3, None, 5, 4]: sorted rule", vertical_sorted(ex), "| first-come", vertical_first_come(ex))
big = build_tree([random.randint(0, 99) for _ in range(1000)])
assert vertical_sorted(big) == vertical_dfs(big) and sum(map(len, vertical_sorted(big))) == 1000
print("n = 1000 random tree: columns =", len(vertical_sorted(big)))
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> [[9], [3, 15], [20], [7]]
[1, 2, 3, 4, 5, 6, 7] -> [[4], [2], [1, 5, 6], [3], [7]]
[3, 1, 4, 0, 2, 2] -> [[0], [1], [3, 2, 2], [4]]
[] -> []
exhaustive+random ok: 1878 trees; first-come order differs from the sorted tie rule on 58 of them
tie example [1, 2, 3, None, 5, 4]: sorted rule [[2], [1, 4, 5], [3]] | first-come [[2], [1, 5, 4], [3]]
n = 1000 random tree: columns = 18
```

**Edge cases:**
- Empty tree: `[]`.
- Same value twice in one cell, as in `[3, 1, 4, 0, 2, 2]`: both stay, column 0 is `[3, 2, 2]`.
- A node and a deeper node in the same column: row order puts the shallower one first, even when its value is bigger. That is why you cannot just sort by value inside a column.
- Skewed tree: n columns or one column; the DFS here uses an explicit stack, so depth is not a problem.

**Follow-ups:**
- Top view or bottom view? Same coordinates; keep the first (or last) node per column.
- Why not a dict of lists only? You need the column order at the end, so sort the keys or track min and max.
- Can I avoid the sort completely? Only for the first-come rule.

**Common mistakes:**
- Sorting by (column, value) and forgetting the row.
- Using DFS order with no row in the sort key.
- Assuming "left to right" breaks ties the same as "smaller value first".
- Building the column list with `range(min, max)` and dropping the last column.

### Q29 ⭐⭐ 🟡 Build a tree from inorder and postorder. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given the inorder and postorder traversals of a tree with DISTINCT values (1 <= n <= 3000), rebuild and return it. The root is the LAST postorder value; build the RIGHT subtree before the left when you consume postorder from the end, and explain why. Use an index map for O(n). Then show that preorder plus postorder does NOT identify a binary tree uniquely (give two different trees with the same pair; the tests check your pair exhaustively over small shapes) and say which trees it does identify. Example: inorder=[9, 3, 15, 20, 7], postorder=[9, 15, 7, 20, 3] -> [3, 9, 20, null, null, 15, 7]; inorder=[-1], postorder=[-1] -> [-1]; inorder=[2, 1], postorder=[2, 1] -> [1, 2]; inorder=[1, 2], postorder=[2, 1] -> [1, null, 2].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Divide and conquer on traversal orders. Postorder ends with the root; the root's position in inorder splits left from right.

**Say this first (1 line):** "Last postorder value is the root, find it in inorder through a hash map, build the right subtree first because I am reading postorder backward, then the left."

**Brute force:** Slice both lists each time and use `list.index`. Correct, but `index` is O(n) and slicing copies, so O(n^2) time and space on a skewed tree.

**Optimal:**
- Map each value to its inorder index (values are distinct). Keep one cursor at the end of postorder.
- `go(lo, hi)` on an inorder window: take `postorder[cursor]`, decrement the cursor, make the node, find its index k. Then `right = go(k + 1, hi)` and `left = go(lo, k - 1)`.
- Why right first: postorder is left, right, root. Read backward it is root, right, left. After taking the root, the next values from the end belong to the right subtree, so the right subtree has to consume them before the left one does. Swapping the order silently builds a wrong tree.
- Preorder plus postorder does NOT identify a tree. If a node has exactly one child, the child could be left or right and both trees give the same pair. Two-node example from my run: preorder `[0, 1]`, postorder `[1, 0]` fits `[0, null, 1]` and `[0, 1]`. (Preorder plus inorder, and inorder plus postorder, are unique; I checked all shapes up to 8 nodes for the second one.)
- Which trees are identified: exactly the FULL binary trees (every node has 0 or 2 children). In my exhaustive run up to 7 nodes, every unique pair was a full tree and no full tree collided with another tree. A non-full tree has a one-child node, and mirroring that child gives a second tree with the same pair.

**Complexity:** Time O(n) (one dict build, one pass), space O(n) for the map plus O(h) stack.

**Dry run:** inorder `[9, 3, 15, 20, 7]`, postorder `[9, 15, 7, 20, 3]`. Cursor at 3: root 3, index 1. Right window (2..4): next from the end is 20, index 3. Its right window (4..4): 7. Its left window (2..2): 15. Back to 3's left window (0..0): 9. Result `[3, 9, 20, null, null, 15, 7]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def build_slices(inorder, postorder):
    """Brute force: slice the lists and use list.index. O(n^2) time and space on skewed trees."""
    if not postorder: return None
    root = postorder[-1]; k = inorder.index(root)
    return TreeNode(root, build_slices(inorder[:k], postorder[:k]),
                    build_slices(inorder[k + 1:], postorder[k:-1]))

def build_in_post(inorder, postorder):
    """O(n): index map + a cursor walking postorder from the END. Right subtree first. Recursion depth = height."""
    pos = {v: i for i, v in enumerate(inorder)}
    assert len(pos) == len(inorder) == len(postorder), "values must be distinct and lists equal length"
    cur = [len(postorder) - 1]
    def go(lo, hi):                                  # inorder window [lo, hi]
        if lo > hi: return None
        v = postorder[cur[0]]; cur[0] -= 1           # the next unused value from the end is this window's root
        node = TreeNode(v)
        k = pos[v]
        node.right = go(k + 1, hi)                   # postorder is left, right, root: reading backward meets RIGHT first
        node.left = go(lo, k - 1)
        return node
    return go(0, len(inorder) - 1)

def build_in_post_iter(inorder, postorder):
    """Same tree with an explicit stack (safe for a 3000-node chain). One pass over postorder from the end."""
    n = len(postorder)
    if n == 0: return None
    root = TreeNode(postorder[-1]); stack = [root]; j = n - 1      # j walks inorder from the end
    for i in range(n - 2, -1, -1):
        node = TreeNode(postorder[i]); parent = stack[-1]
        if parent.val != inorder[j]:
            parent.right = node                       # the parent's own inorder slot is still ahead: we are in its right subtree
        else:
            while stack and stack[-1].val == inorder[j]:
                parent = stack.pop(); j -= 1          # unwind to the ancestor whose LEFT child this is
            parent.left = node
        stack.append(node)
    return root

def tin(t):   return [] if t is None else tin(t[1]) + [t[0]] + tin(t[2])
def tpost(t): return [] if t is None else tpost(t[1]) + tpost(t[2]) + [t[0]]
def tpre(t):  return [] if t is None else [t[0]] + tpre(t[1]) + tpre(t[2])

for ino, post, exp in [([9, 3, 15, 20, 7], [9, 15, 7, 20, 3], [3, 9, 20, None, None, 15, 7]), ([-1], [-1], [-1]),
                       ([2, 1], [2, 1], [1, 2]), ([1, 2], [2, 1], [1, None, 2])]:
    a, b, c = build_in_post(ino, post), build_in_post_iter(ino, post), build_slices(ino, post)
    assert to_arr(a) == to_arr(b) == to_arr(c) == exp, (ino, to_arr(a), to_arr(b))
    print("inorder", ino, "postorder", post, "->", to_arr(a))

# exhaustive: every shape with 1..8 nodes (values are distinct labels): rebuild from (inorder, postorder) and compare structure
cnt = 0; pairs = {}
for n in range(1, 9):
    for s in shapes(n):
        t = label_inorder(s); ino, post = tin(t), tpost(t)
        for fn in (build_in_post, build_in_post_iter, build_slices):
            assert same_shape(fn(ino, post), from_tup(t))
        pairs.setdefault((tuple(ino), tuple(post)), []).append(t); cnt += 1
assert all(len(v) == 1 for v in pairs.values())      # (inorder, postorder) never collides, so the answer is unique
print("exhaustive ok:", cnt, "shapes up to 8 nodes rebuilt by all three builders; every (inorder, postorder) pair is unique")

# random trees with random distinct values (not just inorder labels)
random.seed(29)
for _ in range(300):
    m = random.randint(1, 7); shape = random.choice(shapes(m))
    it = iter(random.sample(range(-100, 100), m))
    def lab(x):
        if x is None: return None
        L = lab(x[0]); v = next(it); return (v, L, lab(x[1]))
    t = lab(shape)
    assert same_shape(build_in_post(tin(t), tpost(t)), from_tup(t)) and same_shape(build_in_post_iter(tin(t), tpost(t)), from_tup(t))
print("random cross-check ok (300 trees with random distinct values)")

# preorder + postorder is NOT enough. Group every labelled shape by (preorder, postorder) after relabelling by preorder (values 0..n-1)
def label_pre(shape, c):
    if shape is None: return None
    v = c[0]; c[0] += 1; L = label_pre(shape[0], c); return (v, L, label_pre(shape[1], c))
def is_full(t): return t is None or ((t[1] is None) == (t[2] is None) and is_full(t[1]) and is_full(t[2]))
def collisions(n):
    g = {}
    for s in shapes(n):
        t = label_pre(s, [0]); g.setdefault((tuple(tpre(t)), tuple(tpost(t))), []).append(t)
    return g
# the fixed-values version: shapes labelled in PREORDER 0..n-1 give the same preorder list for all shapes, so colliding pairs show up as shared keys
for n in range(1, 8):
    g = collisions(n); multi = [k for k, v in g.items() if len(v) > 1]
    uniq_full = all(is_full(v[0]) for v in g.values() if len(v) == 1)
    nonfull_alone = [v for v in g.values() if len(v) == 1 and not is_full(v[0])]
    full_collide = [v for v in g.values() if len(v) > 1 and any(is_full(t) for t in v)]
    assert uniq_full and not full_collide and not nonfull_alone
    print("n =", n, "shapes =", len(shapes(n)), "pairs shared by >= 2 trees =", len(multi), "| every unique pair is a FULL tree, no full tree collides")
g = collisions(2); k = [k for k, v in g.items() if len(v) > 1][0]
print("n = 2 collision: preorder", list(k[0]), "postorder", list(k[1]), "->", [to_arr(from_tup(t)) for t in g[k]])
a, b = g[k]; assert not same_shape(from_tup(a), from_tup(b))

# deep skew: 3000-node left chain. Recursive fails under the default limit, the explicit-stack builder is fine.
n = 3000
ino = list(range(n)); post = list(range(n))   # inorder = postorder = 0..n-1: every node is the LEFT child of the next one
try:
    build_in_post(ino, post); print("recursive: no error")
except RecursionError:
    print("recursive on a 3000-node left chain: RecursionError")
deep = build_in_post_iter(ino, post)
assert height(deep) == n and deep.val == n - 1
print("iterative on the same input: root", deep.val, "height", height(deep))
```

**Output (my run):**
```
inorder [9, 3, 15, 20, 7] postorder [9, 15, 7, 20, 3] -> [3, 9, 20, None, None, 15, 7]
inorder [-1] postorder [-1] -> [-1]
inorder [2, 1] postorder [2, 1] -> [1, 2]
inorder [1, 2] postorder [2, 1] -> [1, None, 2]
exhaustive ok: 2055 shapes up to 8 nodes rebuilt by all three builders; every (inorder, postorder) pair is unique
random cross-check ok (300 trees with random distinct values)
n = 1 shapes = 1 pairs shared by >= 2 trees = 0 | every unique pair is a FULL tree, no full tree collides
n = 2 shapes = 2 pairs shared by >= 2 trees = 1 | every unique pair is a FULL tree, no full tree collides
n = 3 shapes = 5 pairs shared by >= 2 trees = 1 | every unique pair is a FULL tree, no full tree collides
n = 4 shapes = 14 pairs shared by >= 2 trees = 4 | every unique pair is a FULL tree, no full tree collides
n = 5 shapes = 42 pairs shared by >= 2 trees = 7 | every unique pair is a FULL tree, no full tree collides
n = 6 shapes = 132 pairs shared by >= 2 trees = 21 | every unique pair is a FULL tree, no full tree collides
n = 7 shapes = 429 pairs shared by >= 2 trees = 46 | every unique pair is a FULL tree, no full tree collides
n = 2 collision: preorder [0, 1] postorder [1, 0] -> [[0, None, 1], [0, 1]]
recursive on a 3000-node left chain: RecursionError
iterative on the same input: root 2999 height 3000
```

**Edge cases:**
- n = 1: a single node.
- Values must be distinct, or the index map is ambiguous.
- Skewed input: for n = 3000 as a left chain the recursive version raised RecursionError in my run. The stack-based builder (shown) handles it in one pass.
- Inconsistent lists (not from one tree): the code asserts equal length and distinct values but a full validity check would compare the result's traversals.

**Follow-ups:**
- Preorder plus inorder? Root is the first preorder value; build LEFT first.
- Why is the map needed? Without it each root lookup is O(n).
- Can you build from postorder alone for a BST? Yes, the BST property replaces the inorder list (the root is the last value, and the split is by value).

**Common mistakes:**
- Building left before right and consuming the wrong postorder values.
- Using `index` on slices and getting O(n^2).
- Claiming preorder plus postorder is unique.
- Passing slices of the postorder list instead of a cursor.

### Q30 ⭐⭐ 🟡 BST iterator with O(h) space. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Implement a class over a BST (distinct values, n <= 10^5) with `next()` returning the next smallest value and `hasNext()`. Both must run in amortized O(1) time and the iterator may hold only O(h) nodes in a stack (do not flatten the tree into a list, which costs O(n) space). Push the left spine on construction and after each `next()` push the left spine of the popped node's right child. The example runs a list of operations on the given tree and lists the results. Example: root=[7, 3, 15, null, null, 9, 20], ops=['next', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext'] -> [3, 7, True, 9, True, 15, True, 20, False].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Controlled inorder traversal. An explicit stack holding the left spine is a paused recursion.

**Say this first (1 line):** "The stack holds the path of nodes whose left spine I have gone down; `next` pops one, pushes the left spine of its right child, and each node is pushed and popped once, so it is amortized O(1) with O(h) memory."

**Brute force:** In the constructor do a full inorder into a list, then walk an index. `next` and `hasNext` are O(1), but the constructor is O(n) time and the list takes O(n) space, which breaks the O(h) requirement.

**Optimal:**
- Constructor: push `root`, `root.left`, ... down the left spine.
- `hasNext()`: the stack is not empty.
- `next()`: pop the top (it is the smallest unvisited). Then push the left spine of its right child. Return the popped value.
- Invariant: the stack holds exactly the ancestors that are still unvisited, plus the left spine below them. The top is always the next value in sorted order.
- Space: the stack is a subset of one root-to-node path, so at most h nodes (checked on 2056 BST shapes up to 8 nodes; the peak was never above h, and the number of pushes was always exactly n).

**Complexity:** `next` can push a whole spine, so one call can be O(h). But each node is pushed once and popped once in total, so n calls cost O(n): amortized O(1) per call. Space O(h): about log n when balanced and n for a chain. In the run a balanced tree of 16383 nodes peaked at 14, and a 20000-node left chain held 20000 right after the constructor.

**Dry run:** `[7, 3, 15, null, null, 9, 20]`. Constructor pushes 7, 3. `next`: pop 3, right child None, return 3. `next`: pop 7, push left spine of 15: 15, 9; return 7. `hasNext` True. `next`: pop 9, return 9. `next`: pop 15, push 20; return 15. `next`: pop 20; return 20; the stack is empty, `hasNext` False. Output `[3, 7, True, 9, True, 15, True, 20, False]`.

**Code:**
```python
import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

class BSTIterator:
    """In-order iterator holding only the current left spine: at most h nodes in the stack."""
    def __init__(self, root):
        self.stack = []; self.pushes = 0; self.max_stack = 0
        self._push_left(root)
    def _push_left(self, node):
        while node is not None:
            self.stack.append(node); self.pushes += 1; node = node.left
        self.max_stack = max(self.max_stack, len(self.stack))
    def hasNext(self):
        return bool(self.stack)
    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)          # the only new work: the left spine of the right child
        return node.val

class FlatIterator:
    """Brute force: flatten to a list in the constructor. O(n) space."""
    def __init__(self, root):
        self.vals, st, cur = [], [], root
        while st or cur:
            while cur: st.append(cur); cur = cur.left
            cur = st.pop(); self.vals.append(cur.val); cur = cur.right
        self.i = 0
    def hasNext(self): return self.i < len(self.vals)
    def next(self):
        self.i += 1; return self.vals[self.i - 1]

def run_ops(it, ops):
    return [getattr(it, o)() for o in ops]

ops = ['next', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext']
r = build_tree([7, 3, 15, None, None, 9, 20])
got = run_ops(BSTIterator(r), ops); assert got == run_ops(FlatIterator(r), ops) == [3, 7, True, 9, True, 15, True, 20, False]
print("root [7, 3, 15, null, null, 9, 20] ->", got)
e = BSTIterator(None); assert e.hasNext() is False
print("empty tree: hasNext() ->", e.hasNext())

# exhaustive: every BST shape up to 8 nodes. Drain it; compare with inorder; stack never above h; each node pushed exactly once.
cnt = 0
for n in range(0, 9):
    for s in shapes(n):
        t = label_inorder(s); root = from_tup(t); h = height(root)
        it = BSTIterator(root); out = []
        while it.hasNext(): out.append(it.next())
        assert out == list(range(n)) and it.max_stack <= h and it.pushes == n
        if n: assert it.max_stack >= 1
        assert not it.hasNext()
        cnt += 1
print("exhaustive ok on", cnt, "BST shapes: output = sorted order, max stack <= h, total pushes = n")

# random interleavings of hasNext/next vs the flat version
def insert(root, v):
    if root is None: return TreeNode(v)
    cur = root
    while True:
        if v < cur.val:
            if cur.left is None: cur.left = TreeNode(v); break
            cur = cur.left
        else:
            if cur.right is None: cur.right = TreeNode(v); break
            cur = cur.right
    return root
random.seed(30)
for _ in range(300):
    root = None
    for v in random.sample(range(1000), random.randint(1, 80)): root = insert(root, v)
    a, b = BSTIterator(root), FlatIterator(root); n = len(nodes_of(root))
    for _ in range(n + 3):
        if random.random() < 0.5:
            assert a.hasNext() == b.hasNext()
        elif b.hasNext():
            assert a.next() == b.next()
print("random interleaving cross-check ok (300 trees)")

# space: balanced vs skewed, n = 2^k - 1 vs a left chain (sandbox counts of the stack peak)
def perfect(lo, hi):
    if lo > hi: return None
    m = (lo + hi) // 2; return TreeNode(m, perfect(lo, m - 1), perfect(m + 1, hi))
bal = BSTIterator(perfect(0, 2 ** 14 - 2))             # n = 16383
while bal.hasNext(): bal.next()
chain = None
for v in range(1, 20001): chain = TreeNode(v, chain, None)   # left chain: root 20000, leftmost 1
ch = BSTIterator(chain); first = ch.next()
print("balanced n = 16383: peak stack =", bal.max_stack, "| left chain n = 20000: stack right after the constructor =", ch.max_stack, "| first value", first)
assert bal.max_stack == 14 and ch.max_stack == 20000
```

**Output (my run):**
```
root [7, 3, 15, null, null, 9, 20] -> [3, 7, True, 9, True, 15, True, 20, False]
empty tree: hasNext() -> False
exhaustive ok on 2056 BST shapes: output = sorted order, max stack <= h, total pushes = n
random interleaving cross-check ok (300 trees)
balanced n = 16383: peak stack = 14 | left chain n = 20000: stack right after the constructor = 20000 | first value 1
```

**Edge cases:**
- Empty tree: `hasNext()` is False from the start (calling `next()` would be invalid).
- Calling `next()` when `hasNext()` is False is the caller's error; the prompt guarantees it does not happen.
- Skewed tree: h = n, so the stack is O(n) in the worst case and that is within the O(h) bound. The stack is explicit, so there is no recursion limit even at n = 10^5.
- Do not modify the tree while iterating.

**Follow-ups:**
- Zero extra space? Morris traversal threads the tree and gives O(1) extra space, but `next` is then O(1) amortized only, and it temporarily modifies the tree.
- A `peek`? Return `stack[-1].val`.
- Reverse (descending) iterator? Mirror it: push right spines.

**Common mistakes:**
- Flattening the tree in the constructor (O(n) space).
- Pushing the right child instead of its left spine.
- Pushing the whole tree up front.
- Saying `next` is O(1) worst case. It is amortized, not worst case.

### Q31 ⭐⭐ 🟡 Delete a node from a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a BST with distinct values and a key (0 <= n <= 10^4), delete the node holding the key if it exists and return the root; do nothing if it does not exist. Rules, so the result is unique: a leaf is removed; a node with one child is replaced by that child; a node with two children takes the value of the smallest node in its right subtree (its inorder successor), and that successor node is then deleted from the right subtree. Write it recursively in O(h), explain the three cases, and say why re-linking nodes versus copying the value matters if other code holds references to nodes. Example: root=[5, 3, 6, 2, 4, null, 7], key=3 -> [5, 4, 6, 2, null, null, 7]; root=[5, 3, 6, 2, 4, null, 7], key=0 -> [5, 3, 6, 2, 4, null, 7]; root=[], key=0 -> []; root=[5, 3, 6, 2, 4, null, 7], key=5 -> [6, 3, 7, 2, 4]; root=[1], key=1 -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST search plus a three-case structural edit. The BST rule tells you where the key is; the edit only has to keep "left < node < right".

**Say this first (1 line):** "I walk down by the BST rule, then fix three cases: no left child, no right child, or two children, where I copy the inorder successor up and delete it from the right subtree. O(h)."

**Brute force:** Dump the inorder values, drop the key, rebuild a balanced BST. O(n) time and space, and it throws away the original shape and every node object. Fine as a checker, wrong as an answer.

**Optimal:**
- Search: key smaller goes left, larger goes right, and each recursive call returns the new root of that subtree, so the parent re-attaches it.
- Found, no left child: return `root.right` (covers the leaf, where that is None).
- Found, no right child: return `root.left`.
- Found, two children: the inorder successor is the leftmost node of the right subtree. It is the next value above the key, so it can sit at the key's position and keep the order. Copy its value up, then delete that value from the right subtree. The successor has no left child, so that second delete lands in case 1 or 2 and is cheap.
- Copy versus re-link. Copying changes the value inside a node object: any other code holding a reference to the "deleted" node now sees the successor's value and thinks it is still in the tree, while the object that really left the tree is the successor's. Re-linking moves the successor node into the deleted node's place, so the deleted node object is the one that ends up detached and keeps its own value. Use re-link when node identity matters (caches, parent pointers, other structures pointing at nodes). Both give the same shape.

**Complexity:** Time O(h): one descent to the key, one descent to the successor, at most 2h steps. Space O(h) for the recursion, O(1) for the iterative version. h is about log n when balanced but n for a skewed tree.

**Dry run:** `[5,3,6,2,4,null,7]`, key 5 (root, two children).
- Successor: go right to 6, no left child, so successor is 6.
- Copy 6 into the root. Now delete 6 from the right subtree: that node has no left child, so return its right child 7.
- Result `[6,3,7,2,4]`.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- recursive, copy the successor's VALUE (the rule in the question) ----------
def delete_rec(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete_rec(root.left, key)
    elif key > root.val:
        root.right = delete_rec(root.right, key)
    else:
        if root.left is None: return root.right      # leaf or only a right child
        if root.right is None: return root.left      # only a left child
        s = root.right
        while s.left: s = s.left                     # inorder successor
        root.val = s.val                             # copy the value up
        root.right = delete_rec(root.right, s.val)   # then remove the successor node
    return root

# ---------- recursive, RE-LINK: the successor NODE takes the deleted node's place ----------
def delete_relink(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete_relink(root.left, key)
    elif key > root.val:
        root.right = delete_relink(root.right, key)
    else:
        if root.left is None: return root.right
        if root.right is None: return root.left
        s = root.right
        while s.left: s = s.left
        s.right = delete_relink(root.right, s.val)   # s leaves its old spot; its right child is spliced up
        s.left = root.left
        return s                                     # s replaces root; root is now detached
    return root

# ---------- iterative copy-value version (safe on a 10^4-deep skewed tree) ----------
def delete_iter(root, key):
    parent, cur = None, root
    while cur is not None and cur.val != key:
        parent, cur = cur, (cur.left if key < cur.val else cur.right)
    if cur is None:
        return root
    if cur.left and cur.right:
        sp, s = cur, cur.right
        while s.left: sp, s = s, s.left
        cur.val = s.val
        parent, cur = sp, s                          # now delete s, which has no left child
    child = cur.left or cur.right
    if parent is None:
        return child
    if parent.left is cur: parent.left = child
    else: parent.right = child
    return root

# ---------- independent spec on tuples (val, left, right) ----------
def delete_tuple(t, key):
    if t is None: return None
    v, l, r = t
    if key < v: return (v, delete_tuple(l, key), r)
    if key > v: return (v, l, delete_tuple(r, key))
    if l is None: return r
    if r is None: return l
    s = r
    while s[1] is not None: s = s[1]
    return (s[0], l, delete_tuple(r, s[0]))

def inorder_vals(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

def to_tup(root):
    return None if root is None else (root.val, to_tup(root.left), to_tup(root.right))

def run(fn, arr, key):
    return to_arr(fn(build(arr), key))

# examples
base = [5, 3, 6, 2, 4, None, 7]
for arr, key in [(base, 3), (base, 0), ([], 0), (base, 5), ([1], 1)]:
    got = [run(f, arr, key) for f in (delete_rec, delete_relink, delete_iter)]
    assert got[0] == got[1] == got[2]
    print(f"root={arr}, key={key} -> {got[0]}")

# exhaustive: every BST shape with 0..7 nodes (values 0,2,4,..), every key including absent ones
cases = 0
for n in range(8):
    for sh in shapes(n):
        t = label(sh, "in", step=2)
        vals = [2 * i for i in range(n)]
        for key in range(-1, 2 * n + 1):
            spec = delete_tuple(t, key)
            roots = [from_tup(t) for _ in range(3)]
            before = {id(x): x.val for x in nodes_of(roots[0])}
            outs = [delete_rec(roots[0], key), delete_relink(roots[1], key), delete_iter(roots[2], key)]
            for o in outs:
                assert to_tup(o) == spec
                assert inorder_vals(o) == [v for v in vals if v != key]   # still a BST, key gone
            # identity bookkeeping on the copy-value version: exactly one node object disappears (if the key existed)
            after = {id(x) for x in nodes_of(outs[0])}
            assert len(after) == len(before) - (1 if key in vals else 0) and after <= set(before)
            # re-link version: the node object that HELD the key is the one that disappears
            if key in vals:
                holder = next(i for i, v in before.items() if v == key)
                assert holder not in {id(x) for x in nodes_of(outs[1])}
            cases += 1
print("exhaustive cases ok:", cases)

# what a held reference sees
def demo(fn):
    root = build(base)
    n5, n6 = root, root.right
    new_root = fn(root, 5)
    in_tree = {id(x) for x in nodes_of(new_root)}
    return (f"{fn.__name__}: old root object still in tree={id(n5) in in_tree} (val={n5.val}); "
            f"node 6 object still in tree={id(n6) in in_tree} (val={n6.val}); result={to_arr(new_root)}")
print(demo(delete_rec))
print(demo(delete_relink))

# recursion limit: a 1500-node right chain 0..1499, delete the last node
def chain(n):
    root = None
    for i in range(n - 1, -1, -1):
        root = TreeNode(i, None, root)
    return root
try:
    delete_rec(chain(1500), 1499); res = "recursive ok"
except RecursionError:
    res = "recursive RecursionError"
r = delete_iter(chain(1500), 1499)
print(f"1500-node chain, limit {sys.getrecursionlimit()}: {res}; iterative ok, size now {len(nodes_of(r))}")
```

**Output (my run):**
```
root=[5, 3, 6, 2, 4, None, 7], key=3 -> [5, 4, 6, 2, None, None, 7]
root=[5, 3, 6, 2, 4, None, 7], key=0 -> [5, 3, 6, 2, 4, None, 7]
root=[], key=0 -> []
root=[5, 3, 6, 2, 4, None, 7], key=5 -> [6, 3, 7, 2, 4]
root=[1], key=1 -> []
exhaustive cases ok: 9414
delete_rec: old root object still in tree=True (val=6); node 6 object still in tree=False (val=6); result=[6, 3, 7, 2, 4]
delete_relink: old root object still in tree=False (val=5); node 6 object still in tree=True (val=6); result=[6, 3, 7, 2, 4]
1500-node chain, limit 1000: recursive RecursionError; iterative ok, size now 1499
```

Output prints `None` where the prompt writes `null`.

**Edge cases:**
- Empty tree, or key absent: nothing changes (the exhaustive test uses absent keys below, between and above the values).
- Delete the root when it is a leaf, or when it has one child: the child becomes the new root, so always use the returned root.
- Successor is the direct right child: its right subtree is spliced up with no loop.
- Skewed tree: the stated bound is 10^4 nodes, but the recursive version raises `RecursionError` at the default limit of 1000 on a chain (shown above at 1500). Use the iterative version with a parent pointer.

**Follow-ups:**
- Use the predecessor instead? Symmetric: rightmost node of the left subtree. The shape can differ but the result is still a valid BST.
- Duplicates? You need a rule (count on the node, or always send equal keys right) and the delete must remove only one.
- Keep it balanced? Needs rotations (AVL or red-black), a different problem.

**Common mistakes:**
- Not assigning the recursive result back (`root.left = delete(...)`), so the edit is lost.
- Deleting the successor by its position instead of by value from the right subtree, which breaks when the successor is the direct right child.
- Taking the rightmost node of the left subtree for one case and the leftmost of the right for another in the same code.
- Ignoring recursion depth on a skewed input.

### Q32 ⭐⭐ 🟡 Inorder successor in a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is a BST with distinct values and no parent pointers (1 <= n <= 10^5). Given the value p of a node that exists, return the value of the next larger value in the tree, or None when p is the maximum. Walk down from the root in O(h) time and O(1) space: when you go left, remember the node as the best candidate so far; explain why a node with a right child has the minimum of that subtree as its successor and the other case is the lowest ancestor for which p is in the left subtree. Example: root=[2, 1, 3], p=1 -> 2; root=[5, 3, 6, 2, 4, null, null, 1], p=6 -> null; root=[5, 3, 6, 2, 4, null, null, 1], p=4 -> 5; root=[5, 3, 6, 2, 4, null, null, 1], p=2 -> 3; root=[2], p=2 -> null.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST descent with a "last left turn" candidate. No parent pointers and no stack needed.

**Say this first (1 line):** "I walk from the root. Every time I go left, the current node is bigger than p, so I remember it. The last one remembered is the answer. O(h) time, O(1) space."

**Brute force:** Inorder traversal into a list, find p, take the next entry. O(n) time and space, ignores the BST property.

**Optimal:**
- Two cases for the successor of a node p:
  - p has a right child: the successor is the minimum of that right subtree (go right once, then left as far as possible).
  - Otherwise it is the lowest ancestor whose LEFT subtree contains p, that is, the last ancestor where the path turned left.
- One loop covers both. If `p < cur.val`, `cur` is a candidate larger than p, so save it and go left. Otherwise go right (equal to p also goes right, which skips p itself and finds the minimum of its right subtree, or falls off the end and keeps the last candidate).
- Invariant: `best` is the smallest value seen so far that is greater than p, and the answer is still inside the subtree at `cur` or equals `best`.
- The walk also answers "next larger than a value that is not in the tree", which the two-case version cannot.

**Complexity:** Time O(h), one node per level, so at most the height (checked below for every node of every tree up to 9 nodes). Space O(1). h is log n when balanced and n when skewed.

**Dry run:** tree `[5,3,6,2,4,null,null,1]`, p = 4.
- At 5: 4 < 5, so best = 5, go left to 3.
- At 3: 4 > 3, go right to 4.
- At 4: not less than 4, go right, which is None. Return best = 5.

p = 6: at 5 go right (6 > 5), at 6 go right, None. best never set, so None.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

def inorder_vals(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

# ---------- brute force: sorted values, then the next one ----------
def succ_brute(root, p):
    vals = inorder_vals(root)                 # O(n) time and space
    i = vals.index(p)
    return vals[i + 1] if i + 1 < len(vals) else None

# ---------- optimal: one walk down, remember the last node where we went left ----------
def succ(root, p, steps=None):
    best, cur = None, root
    while cur is not None:
        if steps is not None: steps[0] += 1
        if p < cur.val:
            best = cur.val                    # cur is bigger than p: a candidate, but maybe a smaller one is deeper
            cur = cur.left
        else:                                 # p >= cur.val: the answer, if any, is strictly to the right
            cur = cur.right
    return best

# ---------- same idea, split into the two textbook cases (finds p first) ----------
def succ_cases(root, p):
    anc, cur = None, root
    while cur.val != p:                       # p is guaranteed to exist
        if p < cur.val: anc, cur = cur, cur.left
        else: cur = cur.right
    if cur.right:                             # case 1: minimum of the right subtree
        cur = cur.right
        while cur.left: cur = cur.left
        return cur.val
    return anc.val if anc else None           # case 2: lowest ancestor whose LEFT subtree holds p

# examples
for arr, p in [([2, 1, 3], 1), ([5, 3, 6, 2, 4, None, None, 1], 6), ([5, 3, 6, 2, 4, None, None, 1], 4),
               ([5, 3, 6, 2, 4, None, None, 1], 2), ([2], 2)]:
    t = build(arr)
    a, b, c = succ(t, p), succ_cases(t, p), succ_brute(t, p)
    assert a == b == c
    print(f"root={arr}, p={p} -> {a}")

# exhaustive: all BST shapes 0..9 nodes, every existing p; also check the step count is at most the height
cases, worst_gap = 0, 0
for n in range(1, 10):
    for sh in shapes(n):
        t = from_tup(label(sh, "in"))
        h = height(t)
        for p in range(n):
            steps = [0]
            got = succ(t, p, steps)
            assert got == succ_brute(t, p) == succ_cases(t, p)
            assert got == (p + 1 if p + 1 < n else None)
            assert steps[0] <= h                          # O(h): never more nodes visited than the height
            worst_gap = max(worst_gap, h - steps[0])
            cases += 1
print("exhaustive cases ok:", cases)

# a p that is NOT in the tree still gets the next larger value (useful follow-up), but only the walk version supports it
t = build([5, 3, 6, 2, 4])
print("next larger than 4.5:", succ(t, 4.5), "| than 1:", succ(t, 1), "| than 9:", succ(t, 9))
```

**Output (my run):**
```
root=[2, 1, 3], p=1 -> 2
root=[5, 3, 6, 2, 4, None, None, 1], p=6 -> None
root=[5, 3, 6, 2, 4, None, None, 1], p=4 -> 5
root=[5, 3, 6, 2, 4, None, None, 1], p=2 -> 3
root=[2], p=2 -> None
exhaustive cases ok: 59279
next larger than 4.5: 5 | than 1: 2 | than 9: None
```

Output prints `None` where the prompt writes `null`.

**Edge cases:**
- p is the maximum: no left turn ever happens on its path, so None.
- Single node: None.
- p is the root with no right child: None. With a right child: minimum of the right subtree.
- Using `p <= cur.val` instead of `<` would save p itself as the answer.

**Follow-ups:**
- Predecessor? Mirror it: remember the node when you go right.
- With parent pointers? Right-subtree minimum, else climb until you come up from a left child.
- Repeated calls on the same tree? Still O(h) each, no preprocessing needed.

**Common mistakes:**
- Returning the first ancestor larger than p instead of the lowest (smallest) one, or not updating `best` on each left turn.
- Using `<=`, so p is its own successor.
- Doing an inorder traversal when O(h) is required.
- Forgetting that the answer may not be in p's subtree at all.

### Q33 ⭐⭐ 🟡 Two sum in a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is a BST with distinct values (1 <= n <= 10^4). Return True if two DIFFERENT nodes have values summing to k (a node cannot be used twice). Give the hash-set solution (O(n) time, O(n) space) and the two-pointer solution that runs an ascending BST iterator and a descending one, which needs only O(h) space (cross-reference the iterator idea in the BST iterator question of this part). Example: root=[5, 3, 6, 2, 4, null, 7], k=9 -> True; root=[5, 3, 6, 2, 4, null, 7], k=28 -> False; root=[1], k=2 -> False; root=[2, 1, 3], k=4 -> True.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Two sum, with the BST's sorted order available. Hash set for speed of writing; two pointers over an ascending and a descending iterator for O(h) space.

**Say this first (1 line):** "Hash set is O(n) time and space. If memory matters I run an ascending iterator and a descending iterator and move them like two pointers, O(n) time and O(h) space."

**Brute force:** Check every pair of nodes, O(n^2) time, O(n) space for the node list.

**Optimal:**
- Hash set: walk the tree once; for each node look up `k - val` among the values already seen, then add the node's value. Looking before adding means a node can never pair with itself, so `k = 2 * val` with one such node correctly gives False.
- Two pointers: inorder is sorted, so the smallest comes from an ascending iterator and the largest from a descending one (the same stack idea as the BST iterator question in this part, with left and right swapped for the descending one). If the sum is too small move the low pointer up, if too big move the high pointer down.
- Stop when the pointers meet: use `a < b` on values. Values are distinct, so `a == b` is the same node.
- Each iterator holds only a stack of at most h nodes.

**Complexity:**
- Set: O(n) time, O(n) space.
- Two pointers: each iterator visits each node at most once, so O(n) time total; space O(h) for two stacks, never deeper than the tree height (checked below). That beats the set when the tree is balanced (h about log n).

**Dry run:** `[5,3,6,2,4,null,7]`, k = 9. Ascending starts at 2, descending at 7. Sum 9, found (2 + 7).
k = 28: 2+7=9 too small, ascending to 3, 3+7=10 ... 6+7=13, then a=7, b=7 is not `a < b`, stop. False.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- brute force: all pairs of different nodes ----------
def two_sum_brute(root, k):
    vals = [n.val for n in nodes_of(root)]
    return any(vals[i] + vals[j] == k for i in range(len(vals)) for j in range(i + 1, len(vals)))

# ---------- hash set, O(n) time and space ----------
def two_sum_set(root, k):
    seen, st = set(), ([root] if root else [])
    while st:
        n = st.pop()
        if k - n.val in seen:                 # the partner was seen earlier, so it is a different node
            return True
        seen.add(n.val)
        if n.left: st.append(n.left)
        if n.right: st.append(n.right)
    return False

# ---------- two pointers: ascending and descending iterators, O(h) space ----------
class BSTIter:
    """Yields values in ascending (asc=True) or descending order with a stack of at most h nodes."""
    def __init__(self, root, asc):
        self.asc, self.st, self.peak = asc, [], 0
        self._push(root)
    def _push(self, node):
        while node:
            self.st.append(node)
            node = node.left if self.asc else node.right
        self.peak = max(self.peak, len(self.st))
    def next(self):
        node = self.st.pop()
        self._push(node.right if self.asc else node.left)
        return node.val

def two_sum_iters(root, k, info=None):
    if root is None: return False
    lo, hi = BSTIter(root, True), BSTIter(root, False)
    a, b = lo.next(), hi.next()
    found = False
    while a < b:                              # strict: the two pointers must be different nodes
        s = a + b
        if s == k: found = True; break
        if s < k:
            if not lo.st: break               # a was the last node on its side
            a = lo.next()
        else:
            if not hi.st: break
            b = hi.next()
    if info is not None: info.append(max(lo.peak, hi.peak))
    return found

# examples
base = [5, 3, 6, 2, 4, None, 7]
for arr, k in [(base, 9), (base, 28), ([1], 2), ([2, 1, 3], 4)]:
    t = build(arr)
    a, b, c = two_sum_set(t, k), two_sum_iters(t, k), two_sum_brute(t, k)
    assert a == b == c
    print(f"root={arr}, k={k} -> {a}")

# exhaustive: all BST shapes 0..8 nodes (values 0,3,6,...), every k from -1 to 3n+3
cases, trues = 0, 0
for n in range(1, 9):
    for sh in shapes(n):
        t = from_tup(label(sh, "in", step=3))
        h = height(t)
        for k in range(-1, 3 * n + 4):
            info = []
            a, b, c = two_sum_set(t, k), two_sum_iters(t, k, info), two_sum_brute(t, k)
            assert a == b == c, (n, k)
            assert info[0] <= h                           # stack never deeper than the height
            cases += 1; trues += a
print("exhaustive cases ok:", cases, "(True in", trues, ")")

# the 'same node twice' trap: single node 2, k=4 must be False
assert two_sum_set(build([2]), 4) is False and two_sum_iters(build([2]), 4) is False
# random BSTs with negatives and a bigger size
random.seed(5)
def random_bst(n):
    vals = random.sample(range(-60, 60), n)
    root = None
    for v in vals:
        if root is None: root = TreeNode(v); continue
        cur = root
        while True:
            nxt = "left" if v < cur.val else "right"
            if getattr(cur, nxt) is None: setattr(cur, nxt, TreeNode(v)); break
            cur = getattr(cur, nxt)
    return root
for _ in range(300):
    t = random_bst(random.randint(1, 30)); k = random.randint(-100, 100)
    assert two_sum_set(t, k) == two_sum_iters(t, k) == two_sum_brute(t, k)
print("300 random BSTs with negatives ok")
```

**Output (my run):**
```
root=[5, 3, 6, 2, 4, None, 7], k=9 -> True
root=[5, 3, 6, 2, 4, None, 7], k=28 -> False
root=[1], k=2 -> False
root=[2, 1, 3], k=4 -> True
exhaustive cases ok: 56838 (True in 17565 )
300 random BSTs with negatives ok
```

Output prints `None` where the prompt writes `null`.

**Edge cases:**
- One node: False for every k (including `2 * val`).
- Negative values, zero: nothing in the logic assumes positive values.
- k that needs the same value twice: only counts if two different nodes hold it, which distinct values rule out.
- Skewed tree: the two-pointer stack grows to n, same as the set's space. The O(h) win needs a reasonably balanced tree.

**Follow-ups:**
- Same problem on a plain binary tree? Only the hash set works (no order).
- Three sum in a BST? Fix a node, run two sum on the rest: O(n^2).
- Why not flatten to a list and two-pointer? O(n) space, which is what the iterators avoid.

**Common mistakes:**
- Adding to the set before the lookup, so a node pairs with itself.
- Stopping the pointer loop with `a <= b`.
- Forgetting that the descending iterator goes right first, then left.
- Claiming O(h) space for a skewed tree.

### Q34 ⭐⭐ 🟡 Count the nodes of a complete binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The input is guaranteed to be a COMPLETE binary tree (every level full except possibly the last, whose nodes are as far left as possible), 0 <= n <= 5*10^4. Beat the O(n) traversal: compute the leftmost depth and the rightmost depth from a node; if they are equal the subtree is perfect and has 2^depth - 1 nodes, otherwise recurse into both children. Show that this takes O(log^2 n) time, and that the number of spine steps (executions of `cur = cur.left` or `cur = cur.right` inside the two depth helpers; the recursive calls themselves are not counted) is at most 2h^2 where h = floor(log2(n)) for n >= 1 (for a perfect tree, n = 2^(h+1) - 1, it is exactly 2h; the worst case over all n with that h is n = 2^(h+1) - 2, with exactly h(2h - 1) steps for h >= 2), which the tests check for every n up to 2^11 and, for every h up to 13, at the boundary cases n = 2^h, n = 2^(h+1) - 2 and n = 2^(h+1) - 1. The tests use the builder, so the arrays below are complete trees. Example: root=[1, 2, 3, 4, 5, 6] -> 6; root=[] -> 0; root=[1] -> 1; root=[1, 2, 3, 4, 5, 6, 7] -> 7; root=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] -> 10.
**Asked at:** Count-complete-tree-nodes write-ups (jointaro company-tagged page, doocs, vultr, interviewing.io, a Substack solution post titled with Amazon; snippets only, not opened: compare left and right depths, O(log^2 n)) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Use the structure guarantee. In a complete tree, comparing the leftmost and rightmost depths tells you whether a subtree is perfect, and a perfect subtree is counted by a formula.

**Say this first (1 line):** "I compare the left-spine depth and right-spine depth. Equal means a perfect subtree, so 2^(d+1) - 1 nodes with no more work. Otherwise I recurse on both children. O(log^2 n)."

**Brute force:** Any traversal, O(n) time, O(h) to O(n) space. It ignores the completeness guarantee.

**Optimal:**
- `left_depth(node)` counts steps down the left spine, `right_depth(node)` down the right spine.
- Equal depths in a complete tree means every level down to that depth is full, so the subtree has `2^(d+1) - 1` nodes.
- Unequal: the node is not perfect, so the answer is `1 + count(left) + count(right)`.
- Why only one side keeps recursing: the last level is filled from the left. At any non-perfect node, either the left child is perfect (the last level reaches only into the right subtree) or the right child is perfect (one level shorter) and the left one is not. A perfect child returns after its two spine walks, so only ONE branch goes deeper.

**Complexity:**
- The recursion visits at most h + 1 nodes down one path, and each visit does two spine walks of at most h steps. So O(h * h) = O(log^2 n). The extra cost over the formula is only the walks.
- Space: O(h) recursion = O(log n).
- The question's exact claim holds, and I tested it, not just reasoned it. With steps = executions of `node = node.left` or `node = node.right` in the two helpers, h = floor(log2 n): for every n from 1 to 2^11 the steps are at most 2h^2; a perfect tree (n = 2^(h+1) - 1) costs exactly 2h; and for h = 2..10 the maximum over all n with that h is at n = 2^(h+1) - 2 with exactly h(2h - 1). The boundary cases n = 2^h, 2^(h+1) - 2 and 2^(h+1) - 1 also pass for every h from 1 to 13 (table below). No problem found with the stated bounds.

**Dry run:** `[1,2,3,4,5,6]` (6 nodes).
- Root: left depth 2 (1 -> 2 -> 4), right depth 1 (1 -> 3). Not equal, so 1 + count(2) + count(3).
- Node 2: left depth 1, right depth 1, perfect: 3 nodes.
- Node 3: left depth 1 (3 -> 6), right depth 0, not equal: 1 + count(6) + count(None). Node 6 is a leaf, 1 node.
- Total 1 + 3 + 2 = 6.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- brute force: O(n) BFS count ----------
def count_brute(root):
    return len(nodes_of(root))

# ---------- optimal: perfect subtrees counted by formula; steps = executions of cur = cur.left / cur.right ----------
STEPS = [0]

def left_depth(node):
    d = 0
    while node.left:
        node = node.left; d += 1; STEPS[0] += 1
    return d

def right_depth(node):
    d = 0
    while node.right:
        node = node.right; d += 1; STEPS[0] += 1
    return d

def count_complete(node):
    if node is None:
        return 0
    l, r = left_depth(node), right_depth(node)
    if l == r:
        return (1 << (l + 1)) - 1             # perfect subtree of height l: 2^(l+1) - 1 nodes
    return 1 + count_complete(node.left) + count_complete(node.right)

def run(n):
    STEPS[0] = 0
    root = build(list(range(1, n + 1)))       # level-order 1..n is exactly a complete tree with n nodes
    return count_complete(root), STEPS[0], root

# examples
for arr in ([1, 2, 3, 4, 5, 6], [], [1], [1, 2, 3, 4, 5, 6, 7], list(range(1, 11))):
    root = build(arr)
    assert count_complete(root) == count_brute(root) == len(arr)
    print(f"root={arr} -> {count_complete(root)}")

# every n up to 2^11: count is right, steps <= 2h^2, and the maximum per h is where the question says
max_steps = {}
for n in range(1, 2 ** 11 + 1):
    cnt, steps, root = run(n)
    assert cnt == n
    h = n.bit_length() - 1                    # floor(log2 n)
    assert steps <= 2 * h * h, (n, steps)
    if n == 2 ** (h + 1) - 1:
        assert steps == 2 * h                 # perfect tree: exactly one left and one right spine
    if h < 11 and steps > max_steps.get(h, (-1, 0))[1]:   # h = 11 has only n = 2^11 in range, so no maximum is taken there
        max_steps[h] = (n, steps)
for h in range(2, 11):
    n_star, s = max_steps[h]
    assert n_star == 2 ** (h + 1) - 2 and s == h * (2 * h - 1), (h, n_star, s)
print("all n <= 2^11: count ok, steps <= 2h^2 ok, perfect n gives 2h, worst n = 2^(h+1)-2 gives h(2h-1) for h=2..10")

# boundary cases for every h up to 13
rows = []
for h in range(1, 14):
    for n in (2 ** h, 2 ** (h + 1) - 2, 2 ** (h + 1) - 1):
        cnt, steps, _ = run(n)
        assert cnt == n and steps <= 2 * h * h
        if n == 2 ** (h + 1) - 1: assert steps == 2 * h
        if n == 2 ** (h + 1) - 2 and h >= 2: assert steps == h * (2 * h - 1)
        rows.append((h, n, steps))
print("spine steps by h:  n=2^h   n=2^(h+1)-2   n=2^(h+1)-1   2h^2")
by_h = {}
for h, n, s in rows: by_h.setdefault(h, []).append(s)
for h in (1, 2, 3, 5, 8, 13):
    a, b, c = by_h[h]
    print(f"h={h:<2}              {a:>6} {b:>12} {c:>13} {2*h*h:>6}")

# h = 1 for reference (n = 2 and 3), and an empty tree costs nothing
print("n=2 steps:", run(2)[1], "| n=3 steps:", run(3)[1], "| empty:", count_complete(None))
```

**Output (my run):**
```
root=[1, 2, 3, 4, 5, 6] -> 6
root=[] -> 0
root=[1] -> 1
root=[1, 2, 3, 4, 5, 6, 7] -> 7
root=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] -> 10
all n <= 2^11: count ok, steps <= 2h^2 ok, perfect n gives 2h, worst n = 2^(h+1)-2 gives h(2h-1) for h=2..10
spine steps by h:  n=2^h   n=2^(h+1)-2   n=2^(h+1)-1   2h^2
h=1                    1            1             2      2
h=2                    4            6             4      8
h=3                   11           15             6     18
h=5                   37           45            10     50
h=8                  106          120            16    128
h=13                 301          325            26    338
n=2 steps: 1 | n=3 steps: 2 | empty: 0
```

Output prints `None` where the prompt writes `null`. The builder turns the array `1..n` into the complete tree with n nodes, which is why the tests can use it for every n.

**Edge cases:**
- Empty tree: 0, handled before any depth call.
- One node: both depths 0, so 2^1 - 1 = 1.
- Perfect tree: answered at the root, 2h steps and no recursion.
- n = 2^h (one node on the last level) and n = 2^(h+1) - 2 (one missing node): the extremes for the step count.
- If the input is not complete, the formula is simply wrong. The guarantee is part of the contract.

**Follow-ups:**
- Binary search on the last level (go to the node by bits of its index) is the other O(log^2 n) method.
- Can you do better than log^2 n? Not by this route. The count needs about log n probes, each costing a root-to-leaf walk.
- Compare with a heap: the same completeness is what lets a heap live in an array.

**Common mistakes:**
- Writing `2 ** d - 1` when d counts edges (it should be `2^(d+1) - 1`) or off by one on the depth definition.
- Comparing only the left depth of the two children instead of the left and right spines of the same node.
- Assuming the answer is O(log n); it is O(log^2 n).
- Using it on a tree that is merely balanced, not complete.

### Q35 ⭐⭐ 🟡 Deep skewed trees and the recursion limit. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Build a skewed tree of n nodes (shape 'left': every node has only a left child; shape 'right': only a right child), then compute its depth two ways: with a plain recursive function and with an explicit stack. Return the pair (recursive_result, iterative_result) where recursive_result is the string 'RecursionError' if Python's default limit (1000) stops it. Build the tree iteratively too, since recursive construction fails the same way. Explain what raising the limit with `sys.setrecursionlimit` does and does not fix for 10^5 nodes (the result is version and call-path dependent: some call paths such as `lru_cache` have a separate C-level limit, older interpreters can crash, and memory still grows with depth), what a depth of n costs in memory, and which iterative template (Part 4 Q25; for linked lists Part 6 Q26) you would use. Do not hard-code the exact failing depth: it depends on the interpreter, and the examples use n = 500 and n = 2000, far from it. Example: n=500, shape='left' -> (500, 500); n=2000, shape='right' -> ('RecursionError', 2000); n=1, shape='left' -> (1, 1); n=0, shape='left' -> (0, 0).
**Asked at:** Python recursion-limit explainers (techinterview.org depth-of-a-tree page, a OneUptime guide, DataCamp DFS tutorial; snippets only, not opened: default limit 1000, raising it risks a crash, explicit stack preferred) | Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND)

**Pattern:** Recursion depth equals tree height, and Python's call stack is small. A skewed tree has height n, so use an explicit stack.

**Say this first (1 line):** "A skewed tree makes the recursion n deep, and Python stops at 1000 frames by default, so I use an explicit stack: O(n) time, O(n) space for a chain but no call-stack limit."

**Brute force:** The plain recursive `1 + max(depth(left), depth(right))`. Correct, O(n) time, but O(h) call-stack frames. On a chain of n nodes that is n frames, and it raises `RecursionError` once n is past the interpreter's limit.

**Optimal:**
- Build iteratively too: a loop that wraps the previous root in a new node. A recursive builder fails at the same depth.
- Depth with an explicit stack of `(node, depth_so_far)` pairs: pop, record the max, push the children. No recursion at all.
- Why the explicit stack still costs O(h) memory: the stack holds the pending nodes. On a chain it holds one at a time (the stack never grows), on a balanced tree it holds about h. A level-order BFS holds up to one level, so it is the better choice for a very bushy tree.
- Cost of depth n in memory: each live Python frame needs memory of its own. I measured about 100 bytes or more per frame on this sandbox (10 MB for 10^5 frames, roughly 107 MB for 10^6; sandbox-only, interpreter and version dependent). The node objects themselves cost memory on top.
- Which template: the explicit-stack traversal from Part 4 Q25 for trees; for a long linked list the iterative walk from Part 6 Q26 (a chain is the same shape).

**Complexity:** Both versions are O(n) time. Recursive: O(h) stack, which is O(n) in the worst case and fails at the limit. Iterative: O(h) heap memory for the stack, with no recursion limit to hit.

**On `sys.setrecursionlimit`. The prompt's claim is only partly true.** I ran it. On this Python 3.13.17, raising the limit made plain pure-Python recursion succeed on 10^5 and even 10^6 nodes (rc 0, no crash; see the output). So "the C stack will overflow at 10^5" is NOT correct for pure-Python recursion on 3.13: since 3.12, Python-to-Python calls do not consume the C stack, and the cost is heap memory. It is still a bad habit, for these reasons:
- Older interpreters (3.11 and earlier) use the C stack for Python calls and can segfault when the limit is raised too far.
- Recursion that passes through C code (a `functools.lru_cache` wrapper, `sorted` with a key function, `__eq__`, `repr`, JSON) is held to a separate, fixed C recursion limit. I tried a recursive function wrapped in `lru_cache` with the limit raised to 10^7 and it passed at depth 1000 and raised `RecursionError` at depth 10^5 (both in the output).
- You have to guess a safe number, and an interviewer will ask what happens at depth 10^6.
- Memory still grows with the depth.

So the honest interview line: raising the limit can work on newer CPython for pure-Python code, but depends on version and call path; the explicit stack always works.

**Dry run:** chain `3 -> 2 -> 1` (left skewed, n = 3). Stack `[(3, 1)]`: pop, best = 1, push `(2, 2)`. Pop, best = 2, push `(1, 3)`. Pop, best = 3, no children. Stack empty, answer 3. The recursive version reaches 3 frames deep, and for n = 2000 it needs 2000.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

import subprocess

def skewed(n, shape):
    """Iterative build: no recursion, so building never hits the limit."""
    root = None
    for i in range(n):
        root = TreeNode(i, root, None) if shape == "left" else TreeNode(i, None, root)
    return root

def depth_rec(node):
    return 0 if node is None else 1 + max(depth_rec(node.left), depth_rec(node.right))

def depth_iter(root):
    best, st = 0, ([(root, 1)] if root else [])
    while st:
        node, d = st.pop()
        best = max(best, d)
        if node.left: st.append((node.left, d + 1))
        if node.right: st.append((node.right, d + 1))
    return best

def depth_pair(n, shape):
    root = skewed(n, shape)
    try:
        rec = depth_rec(root)
    except RecursionError:
        rec = "RecursionError"
    return rec, depth_iter(root)

for n, shape in [(500, "left"), (2000, "right"), (1, "left"), (0, "left")]:
    print(f"n={n}, shape={shape!r} -> {depth_pair(n, shape)}")

# cross-check: both shapes, many sizes, recursive and iterative agree wherever recursion survives
limit = sys.getrecursionlimit()
for shape in ("left", "right"):
    for n in list(range(0, 60)) + [300, 500, 900]:
        assert depth_pair(n, shape) == (n, n)
    for n in (1500, 2000, 5000):
        assert depth_pair(n, shape) == ("RecursionError", n)    # far above the default limit
# a mixed zig-zag chain too (the node's one child alternates sides)
z = None
for i in range(1200):
    z = TreeNode(i, z, None) if i % 2 else TreeNode(i, None, z)
assert depth_iter(z) == 1200
print(f"default recursion limit {limit}; recursive fails on 1500+ nodes, iterative never does")

# what does raising the limit really do? Run each probe in a fresh interpreter, so a crash could not hurt this script.
PROBE = """
import sys, resource
sys.setrecursionlimit(10**7)
class N:
    __slots__ = ('left',)
    def __init__(self, left=None): self.left = left
n = int(sys.argv[1])
root = None
for _ in range(n): root = N(root)
def depth(x): return 0 if x is None else 1 + depth(x.left)
before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(depth(root), (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - before) // 1024, "MB extra")
"""
for n in (10**5, 10**6):
    r = subprocess.run([sys.executable, "-I", "-c", PROBE, str(n)], capture_output=True, text=True)
    print(f"limit raised, pure-Python recursion on {n} nodes: rc={r.returncode}", r.stdout.strip() or r.stderr.strip()[-80:])
print("python", sys.version.split()[0])

# recursion that passes through a C wrapper (lru_cache) has its own fixed limit, whatever setrecursionlimit says
PROBE2 = """
import sys, functools
sys.setrecursionlimit(10**7)
@functools.lru_cache(maxsize=None)
def f(n): return 0 if n == 0 else 1 + f(n - 1)
try:
    print(f(int(sys.argv[1])))
except RecursionError:
    print("RecursionError")
"""
for n in (1000, 10**5):
    r = subprocess.run([sys.executable, "-I", "-c", PROBE2, str(n)], capture_output=True, text=True)
    print(f"limit raised to 10^7, lru_cache recursion depth {n}: rc={r.returncode}", r.stdout.strip())
```

**Output (my run):**
```
n=500, shape='left' -> (500, 500)
n=2000, shape='right' -> ('RecursionError', 2000)
n=1, shape='left' -> (1, 1)
n=0, shape='left' -> (0, 0)
default recursion limit 1000; recursive fails on 1500+ nodes, iterative never does
limit raised, pure-Python recursion on 100000 nodes: rc=0 100000 10 MB extra
limit raised, pure-Python recursion on 1000000 nodes: rc=0 1000000 107 MB extra
python 3.13.17
limit raised to 10^7, lru_cache recursion depth 1000: rc=0 1000
limit raised to 10^7, lru_cache recursion depth 100000: rc=0 RecursionError
```

The exact failing depth is not hard-coded: the examples use n = 500 and n = 2000, and the cross-check only asserts failure at 1500 or more.

**Edge cases:**
- n = 0: empty tree, depth 0 both ways.
- n = 1: one frame, no issue.
- Shape right versus left: the recursion fails the same way. A zig-zag chain also has height n.
- A balanced tree of a million nodes has depth about 20, so recursion is fine there. The danger is height, not size.

**Follow-ups:**
- Freeing a huge chain: CPython deallocates nested objects with a guard (the "trashcan"), so dropping the root does not blow the stack. Do not rely on that for your own recursive `__del__`.
- Run the recursion in a thread with a bigger stack (`threading.stack_size`)? Possible, a hack. Use the explicit stack.
- Post-order or inorder without recursion? Same idea with a pointer and a visited flag, see the traversal questions in this part.

**Common mistakes:**
- Building the deep tree recursively, so the test fails before the algorithm runs.
- Catching `RecursionError` and calling that a solution.
- Raising the limit with no memory or version caveat.
- Using `list.pop(0)` as a queue in the BFS alternative (O(n) per pop; use `deque`).

### Q36 ⭐⭐ 🟡 Flatten a binary tree to a linked list. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Rearrange the tree IN PLACE so that every node's `right` points to the next node in preorder and every `left` is None (the same node objects, checked by identity; the structure is the singly linked list of Part 6 with `right` playing `next`; see Part 6 Q17 for the identity conventions). 0 <= n <= 2000. Give the recursive version, the reversed-postorder version with a `prev` pointer, and the O(1)-extra-space version that, for each node with a left child, hangs the right subtree under the rightmost node of the left subtree. The example shows the values along the right chain. Example: root=[1, 2, 5, 3, 4, null, 6] -> [1, 2, 3, 4, 5, 6]; root=[] -> []; root=[0] -> [0]; root=[1, null, 2, 3] -> [1, 2, 3].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Pointer surgery on a tree, using preorder as the target order. The flattened tree is a singly linked list that reuses `right` as `next`.

**Say this first (1 line):** "The target is preorder, so every node's right should point to its preorder successor. I'll do it in place with the same node objects, and the O(1)-space way is: hang the right subtree under the rightmost node of the left subtree, then move the left subtree to the right."

**Brute force:** Collect the nodes in preorder into a list (O(n) space), then link `nodes[i].right = nodes[i+1]` and set every `left = None`. In place and correct, but with O(n) extra space. Building new nodes from the values would be correct on values and wrong on identity.

**Optimal:**
- Recursive, return the tail: flatten the left and right subtrees, each call returning the last node of its flattened chain. If the left chain exists, link its tail to the old right subtree, move the left chain to `right`, set `left = None`. The tail is the right chain's tail if there is one, else the left tail, else the node itself. O(n), because no chain is walked a second time. (A version that walks to the end of the left chain each time would be O(n^2) on a left-skewed tree.)
- Reversed postorder with `prev`: visit right, then left, then the node. At that moment `prev` is the node that comes next in preorder, so set `node.right = prev`, `node.left = None`, `prev = node`. Short, but recursive.
- O(1) extra space (no stack): for each node `cur` with a left child, find the rightmost node `p` of the left subtree. Preorder says the right subtree comes right after that node, so `p.right = cur.right`. Then `cur.right = cur.left`, `cur.left = None`, move to `cur.right`.
- Invariant for the O(1) version: the nodes before `cur` already form a flat chain that ends at `cur`, and the whole rest of the tree hangs below `cur` with its preorder unchanged.

**Complexity:**
- Recursive and reversed-postorder: O(n) time, O(h) recursion space.
- O(1) version: O(n) time in total (each node is passed over as `cur` once, and each left subtree's right spine is walked once), O(1) extra space. For n up to 2000 the recursion in the first two is safe on balanced trees but a left chain 2000 deep exceeds Python's default limit, so prefer the O(1) version for deep inputs.

**Dry run:** `[1,2,5,3,4,null,6]`, O(1) version.
- cur = 1: left is 2. Rightmost of the left subtree (2 -> 4) is 4. `4.right = 5`; `1.right = 2`; `1.left = None`. Now 1 -> 2 (left 3, right 4 -> 5 -> 6).
- cur = 2: left is 3, rightmost is 3. `3.right = 4`; `2.right = 3`; `2.left = None`. Now 1 -> 2 -> 3 -> 4 -> 5 -> 6 (5's right is 6 already).
- The rest have no left child. Chain `[1,2,3,4,5,6]`.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# Each version works in place on the same node objects: right = next in preorder, left = None.

def flatten_rec(root):
    """Recursive: each call flattens its subtree and returns the TAIL, so splicing needs no extra walk (O(n) total)."""
    def go(node):
        if node is None:
            return None
        left_tail = go(node.left)
        right_tail = go(node.right)
        if left_tail:                             # splice the flattened left chain between node and its old right
            left_tail.right = node.right
            node.right, node.left = node.left, None
        return right_tail or left_tail or node
    go(root)
    return root

def flatten_prev(root):
    """Reversed postorder (right, left, node) with a prev pointer: each node links to the one that follows it in preorder."""
    prev = None
    def go(node):
        nonlocal prev
        if node is None: return
        go(node.right)
        go(node.left)
        node.right, node.left = prev, None
        prev = node
    go(root)
    return root

def flatten_o1(root):
    """O(1) extra space (Morris style): hang the right subtree under the rightmost node of the left subtree."""
    cur = root
    while cur:
        if cur.left:
            p = cur.left
            while p.right: p = p.right
            p.right = cur.right
            cur.right, cur.left = cur.left, None
        cur = cur.right
    return root

def preorder_ids(root):
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(id(n))
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def chain(root, cap=10**6):
    """Values along the right chain; every left must be None. The cap stops a cycle."""
    out = []
    while root is not None:
        assert root.left is None, "left pointer left behind"
        out.append(root.val)
        root = root.right
        assert len(out) <= cap, "cycle"
    return out

def brute(root):
    """Not in place: new nodes from the preorder values (fails the identity requirement, kept as a value checker)."""
    vals = [n.val for n in nodes_of(root)]
    head = None
    for v in reversed(vals): head = TreeNode(v, None, head)
    return head

def check(fn, arr):
    root = build(arr)
    ids = preorder_ids(root)
    vals = [n.val for n in nodes_of(root)]
    out = fn(root)
    assert out is root or root is None
    assert chain(out) == vals                                   # values in preorder
    assert [id(n) for n in nodes_of(out)] == ids                # SAME node objects, in preorder order
    return chain(out)

for arr in ([1, 2, 5, 3, 4, None, 6], [], [0], [1, None, 2, 3]):
    res = [check(f, arr) for f in (flatten_rec, flatten_prev, flatten_o1)]
    assert res[0] == res[1] == res[2] == chain(brute(build(arr)))
    print(f"root={arr} -> {res[0]}")

# exhaustive: every tree shape with 0..7 nodes, all three versions, identity checked
cases = 0
for n in range(8):
    for sh in shapes(n):
        arr = to_arr(from_tup(label(sh, "pre")))
        for f in (flatten_rec, flatten_prev, flatten_o1):
            check(f, arr)
        cases += 1
print("exhaustive shapes ok:", cases)

# random bigger trees (n up to 300), identity checked, with the O(1)-space version
random.seed(11)
for _ in range(300):
    n = random.randint(0, 300)
    root = None if n == 0 else TreeNode(0)
    pool = [root] if root else []
    for i in range(1, n):
        par = random.choice(pool)
        side = random.choice(("left", "right"))
        if getattr(par, side) is None:
            c = TreeNode(i); setattr(par, side, c); pool.append(c)
    arr = to_arr(root)
    for f in (flatten_rec, flatten_prev, flatten_o1):
        check(f, arr)
print("300 random trees ok")
```

**Output (my run):**
```
root=[1, 2, 5, 3, 4, None, 6] -> [1, 2, 3, 4, 5, 6]
root=[] -> []
root=[0] -> [0]
root=[1, None, 2, 3] -> [1, 2, 3]
exhaustive shapes ok: 626
300 random trees ok
```

The test checks identity: for every shape up to 7 nodes (626 shapes) and 300 random trees, the node objects along the right chain are exactly the original nodes in preorder order, and every `left` is None. The chain walker has a cap and the node collector has a visited-id guard, so an accidental cycle or aliasing fails loudly instead of looping.

**Edge cases:**
- Empty tree: return None.
- Only left children: the whole left chain slides to the right.
- Only right children: already flat, nothing changes.
- Node with a left child whose rightmost node is deep: the walk to `p` is what the O(1) version pays.
- Forgetting `left = None` leaves a hidden second path, so it is not a list.

**Follow-ups:**
- Flatten to inorder (a sorted doubly-linked list)? Different target, same pointer-surgery family; the BST-to-doubly-linked-list variant is the usual one.
- Why is this not the same as the linked-list questions in Part 6? The structure is the same list, but the work is a tree walk that must preserve every node.
- Verify it? Compare node identity, not only values, as the test above does.

**Common mistakes:**
- Saving `cur.right` after you have overwritten it, losing the right subtree.
- Setting `cur.right = cur.left` before linking the rightmost node, which loses the old right subtree.
- Leaving `left` pointers set.
- Building new nodes, which fails an identity check.

### Q37 ⭐⭐ 🟡 All nodes at distance K. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Values are distinct, 1 <= n <= 500. Given the value `target` of a node and an integer k >= 0, return the sorted list of values of all nodes exactly k EDGES from the target, going up through parents as well as down. A tree has no parent pointers, so first record parent links in a dict (or write the target-first recursion that returns the distance upward), then run a BFS outward with a visited set; BFS on general graphs belongs to Part 9. Explain why the visited set is needed in a tree (the parent link points back). Example: root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], target=5, k=2 -> [1, 4, 7]; root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], target=5, k=0 -> [5]; root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], target=5, k=3 -> [0, 8]; root=[1], target=1, k=3 -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Treat the tree as an undirected graph by adding parent links, then BFS outward from the target for exactly k layers.

**Say this first (1 line):** "A node's neighbours are left, right and parent. The tree has no parent pointers, so I record them in a dict first, then BFS k layers from the target with a visited set. O(n)."

**Brute force:** For every node compute the path from the root, work out its distance to the target (up to the lowest common ancestor, then down), keep those at exactly k. O(n * h). The code uses this as the independent checker: path strings `L`/`R`, distance = `len(a) + len(b) - 2 * common_prefix`.

**Optimal:**
- Pass 1: iterative DFS to fill `parent[node]` (the dict key is the node object, hashed by identity, so equal values in different nodes would not clash; values are distinct here anyway) and to find the target node.
- Pass 2: BFS from the target node. Each layer expands to `left`, `right` and `parent` of every frontier node. After k layers the frontier is the answer; sort the values.
- Why the visited set: the parent link points back to where you came from. Without `seen`, layer 2 from a leaf returns the leaf itself (the output shows target 2, k = 2 on `[1,2,3]` returning `[2, 3]` instead of `[3]`).
- Alternative, target-first recursion with no parent dict: `go(node)` returns the distance from `node` down to the target (or -1). When the target is found, collect nodes k below it. On the way back up, at an ancestor that is d + 1 from the target, either it is the answer (d + 1 == k) or collect nodes k - d - 2 below its OTHER child. O(n) time, O(h) space.
- BFS on general graphs is Part 9. Here the graph is a tree, so there are no cycles other than the back edge to the parent.

**Complexity:** Time O(n): parent pass O(n), BFS touches each node at most once (visited set), sorting the answer is O(m log m) for m results. Space O(n) for the dict and the visited set; the recursive alternative is O(h).

**Dry run:** the big example, target 5, k = 2. Neighbours of 5: 6, 2 and its parent 3. Layer 2: from 6 nothing new (children none, parent 5 is seen); from 2: 7 and 4; from 3: 1 (5 is seen). Frontier `[7, 4, 1]`, sorted `[1, 4, 7]`.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- brute force: path-string distance for every node (independent of the algorithms) ----------
def dist_k_brute(root, target, k):
    out = []
    def walk(node, path):
        if node is None: return
        out.append((node.val, path))
        walk(node.left, path + "L"); walk(node.right, path + "R")
    walk(root, "")
    tpath = next(p for v, p in out if v == target)
    def dist(a, b):
        c = 0
        while c < min(len(a), len(b)) and a[c] == b[c]: c += 1
        return len(a) + len(b) - 2 * c         # up from a to the common ancestor, down to b
    return sorted(v for v, p in out if dist(p, tpath) == k)

# ---------- optimal 1: parent links + BFS outward with a visited set ----------
def dist_k_bfs(root, target, k):
    parent, st, start = {root: None}, [root], None
    while st:                                  # iterative DFS to record parents (dict keys are node identities)
        n = st.pop()
        if n.val == target: start = n
        for c in (n.left, n.right):
            if c: parent[c] = n; st.append(c)
    seen, frontier = {start}, [start]
    for _ in range(k):
        nxt = []
        for n in frontier:
            for m in (n.left, n.right, parent[n]):
                if m is not None and m not in seen:    # without 'seen' the parent link walks straight back
                    seen.add(m); nxt.append(m)
        frontier = nxt
    return sorted(n.val for n in frontier)

# ---------- optimal 2: target-first recursion, returns distance to the target (or -1) ----------
def dist_k_rec(root, target, k):
    out = []
    def down(node, d):                         # collect nodes exactly d below node
        if node is None or d < 0: return
        if d == 0: out.append(node.val); return
        down(node.left, d - 1); down(node.right, d - 1)
    def go(node):                              # distance from node to target if target is inside, else -1
        if node is None: return -1
        if node.val == target:
            down(node, k); return 0
        for near, far in ((node.left, node.right), (node.right, node.left)):
            d = go(near)
            if d >= 0:
                if d + 1 == k: out.append(node.val)
                else: down(far, k - d - 2)     # the other side starts one edge further away
                return d + 1
        return -1
    go(root)
    return sorted(out)

big = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
for arr, t, k in [(big, 5, 2), (big, 5, 0), (big, 5, 3), ([1], 1, 3)]:
    r = build(arr)
    a, b, c = dist_k_bfs(r, t, k), dist_k_rec(r, t, k), dist_k_brute(r, t, k)
    assert a == b == c
    print(f"root={arr}, target={t}, k={k} -> {a}")

# exhaustive: every shape with 1..7 nodes (distinct preorder labels), every target, k = 0..8
cases = 0
for n in range(1, 8):
    for sh in shapes(n):
        r = from_tup(label(sh, "pre"))
        for t in range(n):
            for k in range(0, 9):
                a, b, c = dist_k_bfs(r, t, k), dist_k_rec(r, t, k), dist_k_brute(r, t, k)
                assert a == b == c, (n, t, k)
                cases += 1
print("exhaustive cases ok:", cases)

# the visited set matters: without it, k = 2 from a leaf comes back to the leaf itself
def bfs_no_seen(root, target, k):
    parent, st, start = {root: None}, [root], None
    while st:
        n = st.pop()
        if n.val == target: start = n
        for c in (n.left, n.right):
            if c: parent[c] = n; st.append(c)
    frontier = [start]
    for _ in range(k):
        frontier = [m for n in frontier for m in (n.left, n.right, parent[n]) if m is not None]
    return sorted(n.val for n in frontier)
r = build([1, 2, 3])
print("target 2, k=2: with seen", dist_k_bfs(r, 2, 2), "| without seen", bfs_no_seen(r, 2, 2))
```

**Output (my run):**
```
root=[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target=5, k=2 -> [1, 4, 7]
root=[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target=5, k=0 -> [5]
root=[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target=5, k=3 -> [0, 8]
root=[1], target=1, k=3 -> []
exhaustive cases ok: 36729
target 2, k=2: with seen [3] | without seen [2, 3]
```

Output prints `None` where the prompt writes `null`. The exhaustive test runs every shape with 1 to 7 nodes, every target and k from 0 to 8 (so k larger than the tree, which must give `[]`), against the path-string brute force.

**Edge cases:**
- k = 0: just the target.
- k larger than the tree can reach: empty list.
- Target is the root: no parent; `parent[root]` is None, which the loop skips.
- Target is a leaf: the answer mostly lies up and across.
- Single node with k > 0: `[]`.

**Follow-ups:**
- Time to burn the whole tree from a node? Same BFS, count layers until the frontier is empty.
- Values not distinct? Pass the target node (a reference), not a value; the dict keyed by node already supports that.
- Why a list `frontier` and not a deque? Layers are replaced whole each round, so no `pop(0)` is needed.

**Common mistakes:**
- No visited set, so the BFS walks back to the parent and double counts.
- Treating distance as depth below the target only, missing ancestors.
- Off-by-one when going up in the recursive version (the other child is one extra edge away).
- Returning unsorted values when the question asks for sorted ones.

### Q38 ⭐⭐ 🟡 Serialize and deserialize with BFS. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Use the level-order format: tokens are joined by commas; start with the root; for each non-null node taken from a queue emit its left child then its right child, writing '#' for a missing child and appending non-null children to the queue; stop when the queue is empty; never trim trailing markers. So the empty tree is '#' and a single node 1 is '1,#,#'. Write `serialize` and `deserialize` that round trip, 0 <= n <= 10^4, and say why there are exactly 2n + 1 tokens, and how this differs from the trimmed array form the examples in this book use for input. The example gives the exact serialized string for the tree. Example: root=[1, 2, 3, null, null, 4, 5] -> '1,2,3,#,#,4,5,#,#,#,#'; root=[] -> '#'; root=[1] -> '1,#,#'; root=[1, null, 2] -> '1,#,2,#,#'.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Tree encoding with a queue. Emit the tree level by level, with an explicit marker for every missing child so the shape is recoverable from the string alone.

**Say this first (1 line):** "Level order with '#' for each missing child, never trimmed: the root first, then for each real node its left and right child tokens. Decoding replays the same queue."

**Brute force:** Preorder with '#' markers by recursion. It also round trips (the code uses it as a cross-check on the token count) but it is recursive, so a 10^4-deep chain hits the recursion limit. The BFS format avoids that.

**Optimal:**
- `serialize`: if the tree is empty return `'#'`. Otherwise start the list with the root value and a queue holding the root. Pop a node, append its left token then its right token (`'#'` for None; real children are appended to the queue as well).
- `deserialize`: split on commas, make the root, put it in the queue, then for each popped node read the next two tokens as its left and right. A `'#'` means no child.
- Both sides use the same queue order, which is why they stay in step.
- Why 2n + 1 tokens, never trimmed: each of the n nodes writes exactly two child tokens (2n in all), plus one token for the root. n - 1 of the child slots are filled by the non-root nodes (one each), leaving n + 1 markers: n values + (n + 1) '#' = 2n + 1. For the empty tree that is the single token `'#'`.
- The array form the examples use for INPUT is trimmed: trailing nulls are dropped and the children of a null are not listed. That form is shorter (7 entries versus 11 tokens in the output) and cannot be decoded without the "children of a null are not listed" convention. The serialization here lists every child slot of every real node and also has no ambiguity: no node's tokens are skipped.

**Complexity:** Time O(n), each node enqueued and dequeued once, each token written and parsed once. Space O(n) for the string and the queue (the queue holds at most one level). No recursion, so a 10^4-node chain is fine.

**Dry run:** the tree `1 / (2, 3)`, with 3 having children 4 and 5.
- Start `1`, queue [1]. Pop 1: write `2`, `3`; queue [2, 3].
- Pop 2: write `#`, `#`. Pop 3: write `4`, `5`; queue [4, 5].
- Pop 4: `#`, `#`. Pop 5: `#`, `#`.
- Result `1,2,3,#,#,4,5,#,#,#,#`, which is 11 = 2 * 5 + 1 tokens.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- the required format: level order, '#' for every missing child, nothing trimmed ----------
def serialize(root):
    if root is None:
        return "#"
    out, q = [str(root.val)], deque([root])
    while q:
        n = q.popleft()
        for c in (n.left, n.right):
            if c is None:
                out.append("#")
            else:
                out.append(str(c.val)); q.append(c)
    return ",".join(out)

def deserialize(s):
    tok = s.split(",")
    if tok[0] == "#":
        assert len(tok) == 1
        return None
    root = TreeNode(int(tok[0]))
    q, i = deque([root]), 1
    while q:
        n = q.popleft()
        for side in ("left", "right"):
            if tok[i] != "#":
                c = TreeNode(int(tok[i])); setattr(n, side, c); q.append(c)
            i += 1
    assert i == len(tok), "leftover tokens"
    return root

# ---------- brute force / cross-check format: preorder with '#' (a different, equally valid encoding) ----------
def ser_pre(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None: out.append("#"); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return ",".join(out)

for arr in ([1, 2, 3, None, None, 4, 5], [], [1], [1, None, 2]):
    s = serialize(build(arr))
    assert same(deserialize(s), build(arr))
    print(f"root={arr} -> '{s}'")

# exhaustive: every shape with 0..8 nodes, negative / multi-digit values; round trip + exactly 2n+1 tokens
cases = 0
for n in range(9):
    for sh in shapes(n):
        t = label(sh, "pre", step=-7)               # values 0, -7, -14, ... (negatives and two digits)
        root = from_tup(t)
        s = serialize(root)
        assert len(s.split(",")) == 2 * n + 1        # n values + (n + 1) '#' markers
        assert s.count("#") == n + 1
        assert same(deserialize(s), root)
        assert s == serialize(deserialize(s))        # canonical: serialize(deserialize(s)) == s
        assert ser_pre(root).count("#") == n + 1     # the preorder encoding has the same token count
        cases += 1
print("exhaustive shapes ok:", cases)

# the trimmed array form used by the examples is a different, shorter thing
root = build([1, 2, 3, None, None, 4, 5])
print("trimmed array:", len(to_arr(root)), "entries | full serialization:", len(serialize(root).split(",")), "tokens")

# n = 10^4 skewed tree: BFS and the parser are iterative, so no recursion limit is touched
chain_root = None
for i in range(10**4):
    chain_root = TreeNode(i, chain_root, None)
s = serialize(chain_root)
assert len(s.split(",")) == 2 * 10**4 + 1 and same(deserialize(s), chain_root)
print("10^4-node left chain: round trip ok,", len(s.split(",")), "tokens")

# random trees
random.seed(3)
for _ in range(300):
    n = random.randint(0, 60)
    root = None if n == 0 else TreeNode(random.randint(-99, 99))
    pool = [root] if root else []
    for _ in range(n - 1):
        par = random.choice(pool); side = random.choice(("left", "right"))
        if getattr(par, side) is None:
            c = TreeNode(random.randint(-99, 99)); setattr(par, side, c); pool.append(c)
    assert same(deserialize(serialize(root)), root)
print("300 random trees ok")
```

**Output (my run):**
```
root=[1, 2, 3, None, None, 4, 5] -> '1,2,3,#,#,4,5,#,#,#,#'
root=[] -> '#'
root=[1] -> '1,#,#'
root=[1, None, 2] -> '1,#,2,#,#'
exhaustive shapes ok: 2056
trimmed array: 7 entries | full serialization: 11 tokens
10^4-node left chain: round trip ok, 20001 tokens
300 random trees ok
```

Output prints `None` where the prompt writes `null` (that is the array input, not the string). The exhaustive test covers every shape with 0 to 8 nodes, with negative and two-digit values, and checks the token count equals 2n + 1 and that `serialize(deserialize(s)) == s`.

**Edge cases:**
- Empty tree: `'#'`, one token, handled before anything else.
- Single node: `'1,#,#'`.
- Negative or multi-digit values: split on commas, not characters.
- Strings as values: a comma or '#' in a value would break this format; the question has integers.
- Skewed 10^4-node tree: 20001 tokens, no recursion.

**Follow-ups:**
- Why not preorder? It works and needs only one pass with a global index, but the recursion depth equals the tree height.
- Can you shrink it? Yes: trim trailing markers, or for a BST use only the preorder values (no markers at all, see the "build a BST from preorder" question).
- Is it unique? Yes: a valid string decodes to exactly one tree, and a tree always produces the same string.

**Common mistakes:**
- Putting None children in the queue, so the decoder reads past the end.
- Trimming trailing `#` on one side only.
- Using `str.split` with a space or character by character, breaking multi-digit and negative values.
- Using `list.pop(0)` as the queue instead of `deque.popleft()`.

### Q39 ⭐⭐ 🔴 Recover a BST with two swapped values. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Exactly two nodes of a BST with distinct values (2 <= n <= 1000) had their VALUES swapped by mistake. Restore the BST by swapping the two values back, without changing the shape, and return the root. Find the two nodes from the inorder sequence: the first descent gives the first node (the larger, earlier one) and the last descent gives the second (the smaller, later one); when the swapped values are adjacent in inorder there is only one descent. Do it with O(h) space, and then mention the O(1)-space version with Morris traversal. The pair to swap back is unique, which the tests check exhaustively on all small trees. Example: root=[1, 3, null, null, 2] -> [3, 1, null, null, 2]; root=[3, 1, 4, null, null, 2] -> [2, 1, 4, null, null, 3]; root=[2, 3, 1] -> [2, 1, 3]; root=[1, 2, 3] -> [2, 1, 3].
**Asked at:** Recover-BST write-ups (neetcode, vultr, doocs, a jointaro Amazon-tagged page, hellointerview community, a CodeChef editorial; snippets only, not opened: first and second out-of-order nodes in inorder, O(1) space via Morris) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** The inorder traversal of a BST is strictly increasing. Two swapped values show up as "descents" in that sequence. Find them in one inorder pass, then swap the values back.

**Say this first (1 line):** "I run an inorder walk keeping the previous node. Where prev is bigger than the current node, that is a descent. The first descent gives the first culprit (prev), the last descent gives the second (the current node). Swap their values. If there is only one descent, the swapped pair was adjacent."

**Brute force:** Inorder into a list, sort the values, write them back in inorder. O(n log n) time, O(n) space. It does restore the BST, but it is more work than needed and does not tell you which two nodes were wrong.

**Optimal:**
- Take the sorted inorder `1 2 3 4 5` and swap two entries.
  - Non-adjacent, e.g. positions 1 and 4: `1 5 3 4 2`. Two descents: `5 > 3` and `4 > 2`. The first node is the earlier element of the FIRST descent (5), the second is the later element of the LAST descent (2).
  - Adjacent, e.g. `1 3 2 4 5`: a single descent `3 > 2`. The first node is its earlier element, the second is its later element, the same rule with one descent.
- So: `first` = the earlier node of the first descent, `second` = the later node of the last descent. Always update `second` on every descent and set `first` only once.
- The pair is unique. Swapping any other pair cannot give a sorted inorder (a sorted order of distinct values is unique, and a transposition identifies its pair). The tests check this exhaustively.
- Space: the stack version holds O(h) nodes. Morris traversal gets O(1): before going left from `cur`, find its inorder predecessor `pred` (rightmost node of the left subtree), set `pred.right = cur` as a temporary thread and go left. When the thread is found again, remove it, visit `cur`, go right. Every thread is removed, so the tree ends exactly as it began. Do not exit early, or a thread stays and creates a cycle.

**Complexity:** Time O(n) for the stack and Morris versions (Morris touches each edge a constant number of times, so still O(n)). Space O(h) for the stack version, O(1) extra for Morris. The tree shape never changes, only two values.

**Dry run:** `[3,1,4,null,null,2]` (inorder 1, 3, 2, 4).
- Walk inorder: 1, then 3 (fine), then 2. Prev is 3, current is 2, and 3 > 2 is a descent: first = 3, second = 2.
- Next 4: 2 < 4, no descent. Swap the values of the two nodes: the tree becomes `[2,1,4,null,null,3]`, inorder 1, 2, 3, 4.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

def inorder_nodes(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur); cur = cur.right
    return out

# ---------- brute force: sort the values and write them back in inorder (O(n log n) time, O(n) space) ----------
def recover_brute(root):
    ns = inorder_nodes(root)
    for node, v in zip(ns, sorted(n.val for n in ns)):
        node.val = v
    return root

# ---------- optimal: iterative inorder with a prev pointer, O(h) space; descents = places where prev.val > cur.val ----------
def recover_stack(root, info=None):
    st, cur, prev, first, second, descents = [], root, None, None, None, 0
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop()
        if prev is not None and prev.val > cur.val:
            descents += 1
            if first is None: first = prev       # first descent: the earlier (larger) node is the culprit
            second = cur                         # last descent: the later (smaller) node is the other one
        prev, cur = cur, cur.right
    if info is not None: info.append(descents)
    first.val, second.val = second.val, first.val
    return root

# ---------- O(1) extra space: Morris traversal (temporary threads from each predecessor to its successor) ----------
def recover_morris(root):
    cur, prev, first, second = root, None, None, None
    def visit(node):
        nonlocal prev, first, second
        if prev is not None and prev.val > node.val:
            if first is None: first = prev
            second = node
        prev = node
    while cur:
        if cur.left is None:
            visit(cur); cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur: pred = pred.right
            if pred.right is None:
                pred.right = cur; cur = cur.left            # make the thread, go left
            else:
                pred.right = None; visit(cur); cur = cur.right   # remove the thread, visit, go right
    first.val, second.val = second.val, first.val           # must finish the whole walk so no thread stays
    return root

def run(fn, arr):
    return to_arr(fn(build(arr)))

for arr in ([1, 3, None, None, 2], [3, 1, 4, None, None, 2], [2, 3, 1], [1, 2, 3]):
    a, b, c = run(recover_brute, arr), run(recover_stack, arr), run(recover_morris, arr)
    assert a == b == c
    print(f"root={arr} -> {a}")

def is_bst(root):
    v = [n.val for n in inorder_nodes(root)]
    return all(x < y for x, y in zip(v, v[1:]))

# exhaustive: every BST shape with 2..8 nodes, EVERY pair of nodes whose values were swapped
cases = adjacent = 0
for n in range(2, 9):
    for sh in shapes(n):
        t = label(sh, "in")
        for i in range(n):
            for j in range(i + 1, n):
                orig = from_tup(t)
                ns = inorder_nodes(orig)
                broken = from_tup(t)
                bn = inorder_nodes(broken)
                bn[i].val, bn[j].val = bn[j].val, bn[i].val
                assert not is_bst(broken)
                # uniqueness: swapping values of exactly ONE pair of nodes restores a BST
                fixes = 0
                for a in range(n):
                    for b in range(a + 1, n):
                        bn[a].val, bn[b].val = bn[b].val, bn[a].val
                        fixes += is_bst(broken)
                        bn[a].val, bn[b].val = bn[b].val, bn[a].val
                assert fixes == 1, (n, i, j)
                for fn in (recover_brute, recover_stack, recover_morris):
                    copy = from_tup(t); cn = inorder_nodes(copy); cn[i].val, cn[j].val = cn[j].val, cn[i].val
                    ids = [id(x) for x in nodes_of(copy)]
                    out = fn(copy)
                    assert same(out, orig)                              # values back, shape unchanged
                    assert [id(x) for x in nodes_of(out)] == ids        # same node objects, no thread left behind
                info = []
                cp = from_tup(t); cn = inorder_nodes(cp); cn[i].val, cn[j].val = cn[j].val, cn[i].val
                recover_stack(cp, info)
                assert info[0] == (1 if j == i + 1 else 2)              # adjacent swap: one descent; otherwise two
                adjacent += (j == i + 1)
                cases += 1
print("exhaustive swaps ok:", cases, "(adjacent in inorder:", adjacent, ")")
```

**Output (my run):**
```
root=[1, 3, None, None, 2] -> [3, 1, None, None, 2]
root=[3, 1, 4, None, None, 2] -> [2, 1, 4, None, None, 3]
root=[2, 3, 1] -> [2, 1, 3]
root=[1, 2, 3] -> [2, 1, 3]
exhaustive swaps ok: 51550 (adjacent in inorder: 13466 )
```

Output prints `None` where the prompt writes `null`. The exhaustive test covers every BST shape with 2 to 8 nodes and every pair of nodes whose values were swapped (51550 cases, 13466 of them adjacent in inorder). For each: all three versions restore the original with the same node objects and no thread left behind (checked by node identity and by the cycle guard), the descent count is 1 if adjacent and 2 otherwise, and exactly one swap of two node values makes the tree a BST again. No problem found with the stated claims.

**Edge cases:**
- n = 2: the only case is one adjacent swap with one descent.
- The swapped nodes are parent and child: the descent is adjacent in inorder; the rule still holds.
- The swap involves the root: nothing special; the traversal is order-based.
- Do NOT stop at the first descent: a non-adjacent swap has a second one, and the second node comes from it.
- Morris: every thread must be removed, or later code walking the tree loops forever.

**Follow-ups:**
- More than two swapped values? The two-descent trick no longer works; sort the values back (the brute force).
- Only validate, not fix? Check that inorder is increasing, as in the "validate a BST" question in this part.
- Why compare with the previous node and not with the parent? A violation can be between a node and a distant ancestor. The inorder predecessor is the right neighbour to compare.

**Common mistakes:**
- Taking `second = cur` at the first descent only, or `first` at the last one.
- Comparing a node with its parent instead of the inorder predecessor.
- Relinking nodes when the question only asks you to swap two values back: far more pointer work, no benefit.
- Leaving a Morris thread in place.

### Q40 ⭐ 🟢 N-ary tree basics. A node is `Node(val, children)` with `children` a list. Examples give an N-ary tree as a level-order array: the root, then null, then for each node in queue order the list of its children followed by null (a node with no children contributes just its null; trailing nulls may be omitted), so [1,null,3,2,4,null,5,6] is root 1 with children 3, 2, 4 and node 3 has children 5 and 6. Return the tuple (preorder, postorder, level_order, max_depth) for a tree with 0 <= n <= 10^4 nodes (level_order is a list of lists; depth counts nodes and is 0 for an empty tree). Explain where the binary-tree traversals change (a loop over children replaces left and right; inorder has no single meaning) and give the explicit-stack versions. Example: arr=[1, null, 3, 2, 4, null, 5, 6] -> ([1, 3, 5, 6, 2, 4], [5, 6, 3, 2, 4, 1], [[1], [3, 2, 4], [5, 6]], 3); arr=[] -> ([], [], [], 0); arr=[7] -> ([7], [7], [[7]], 1).
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Same traversals as a binary tree, with a loop over `children` in place of "left then right".

**Say this first (1 line):** "Preorder visits a node then each child; postorder visits each child then the node; level order is a queue; depth is the number of levels. I'll use explicit stacks so a deep tree cannot hit the recursion limit."

**Brute force:** Plain recursion for each traversal. It is correct and O(n) time, but a 10^4-node chain needs 10^4 frames and fails at Python's default limit of 1000 (shown in the output). The code keeps it as the cross-check.

**Optimal:**
- Reading the input: the array is the root, `None`, then for every node in queue order its children followed by `None`. Keep a queue of nodes, and for each popped node take children until the next `None`.
- Where binary-tree logic changes: a loop over `node.children` replaces the two recursive calls. Inorder has no single meaning, because with k children there is no one place "between" the left and right (you could visit after the first child, but that is a convention, not the tree's).
- Preorder, explicit stack: pop a node, record it, push its children in REVERSE so the first child pops next.
- Postorder, explicit stack, the short trick: pop a node, record it, push its children in order. That produces root, then the last child's subtree first, and so on: the reverse of postorder. Reverse the list at the end.
- Level order: a list per level. `cur = [children of every node in cur]` until it is empty. The number of lists is the max depth (counted in nodes), 0 for an empty tree.

**Complexity:** Time O(n): every node is pushed and popped once, and each child is visited once. Space O(n) for the result, plus O(width) for the level list (a bushy tree) or O(h) for the stack. Recursion would add O(h) frames.

**Dry run:** `[1,null,3,2,4,null,5,6]`. Root 1 has children 3, 2, 4; node 3 has children 5, 6.
- Preorder: pop 1, push 4, 2, 3. Pop 3, push 6, 5. Pop 5, 6, then 2, 4. Result `[1, 3, 5, 6, 2, 4]`.
- Postorder: the reversed-preorder pass records 1, 4, 2, 3, 6, 5. Reversed: `[5, 6, 3, 2, 4, 1]`.
- Levels: `[1]`, `[3, 2, 4]`, `[5, 6]`, so depth 3.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

class Node:
    __slots__ = ("val", "children")
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children if children is not None else []

def build_nary(arr):
    """[root, None, children of root..., None, children of next node in queue order..., None, ...]; trailing Nones optional."""
    if not arr:
        return None
    root = Node(arr[0])
    q, i = deque([root]), 2
    while q and i <= len(arr):
        node = q.popleft()
        while i < len(arr) and arr[i] is not None:
            c = Node(arr[i]); node.children.append(c); q.append(c); i += 1
        i += 1                                       # skip the None that ends this node's children
    return root

def encode_nary(root, trim=True):
    if root is None:
        return []
    out, q = [root.val, None], deque([root])
    while q:
        node = q.popleft()
        for c in node.children:
            out.append(c.val); q.append(c)
        out.append(None)
    while trim and out and out[-1] is None:
        out.pop()
    return out

# ---------- brute force: plain recursion ----------
def traversals_rec(root):
    if root is None:
        return ([], [], [], 0)
    pre, post = [], []
    def go(n):
        pre.append(n.val)
        for c in n.children: go(c)
        post.append(n.val)
    go(root)
    levels, cur = [], [root]
    def lv(nodes):
        if not nodes: return
        levels.append([n.val for n in nodes]); lv([c for n in nodes for c in n.children])
    lv(cur)
    return (pre, post, levels, len(levels))

# ---------- optimal: explicit stacks and a level loop, no recursion ----------
def traversals(root):
    if root is None:
        return ([], [], [], 0)
    pre, st = [], [root]
    while st:                                        # preorder: pop, record, push children right to left
        n = st.pop(); pre.append(n.val)
        st.extend(reversed(n.children))
    rev, st = [], [root]                             # postorder: (node, then children left to right) reversed
    while st:
        n = st.pop(); rev.append(n.val)
        st.extend(n.children)
    post = rev[::-1]
    levels, cur = [], [root]
    while cur:                                       # level order: one list per level
        levels.append([n.val for n in cur])
        cur = [c for n in cur for c in n.children]
    return (pre, post, levels, len(levels))

for arr in ([1, None, 3, 2, 4, None, 5, 6], [], [7]):
    root = build_nary(arr)
    res = traversals(root)
    assert res == traversals_rec(root)
    print(f"arr={arr} -> {res}")

# exhaustive: every ordered tree with 1..7 nodes as (val, [children]), preorder-labelled; encode -> decode -> compare
def forests(m):                                      # all ordered lists of trees holding m nodes in total
    if m == 0: return [[]]
    out = []
    for first in range(1, m + 1):
        for t in trees(first):
            for rest in forests(m - first): out.append([t] + rest)
    return out
_tc = {}
def trees(n):                                        # shapes only: a tree is a tuple of child shapes
    if n not in _tc: _tc[n] = [tuple(f) for f in forests(n - 1)]
    return _tc[n]
def realise(shape, counter):
    node = Node(counter[0]); counter[0] += 1
    node.children = [realise(s, counter) for s in shape]
    return node
def same_nary(a, b):
    return a.val == b.val and len(a.children) == len(b.children) and all(same_nary(x, y) for x, y in zip(a.children, b.children))
count = 0
for n in range(1, 8):
    for sh in trees(n):
        root = realise(sh, [0])
        for trim in (True, False):
            back = build_nary(encode_nary(root, trim))
            assert same_nary(back, root)
        assert traversals(root) == traversals_rec(root)
        count += 1
print("exhaustive ordered trees ok:", count)

# random trees up to 200 nodes with arbitrary fan-out, cross-checked against the recursive brute force
random.seed(9)
for _ in range(300):
    n = random.randint(1, 200)
    root = Node(0); pool = [root]
    for i in range(1, n):
        p = random.choice(pool); c = Node(i); p.children.append(c); pool.append(c)
    assert traversals(root) == traversals_rec(root)
    assert same_nary(build_nary(encode_nary(root)), root)
print("300 random N-ary trees ok")

# n = 10^4 chain: iterative is fine, recursion is not (limit 1000)
chain_arr = [1, None]
for v in range(2, 10**4 + 1): chain_arr += [v, None]
root = build_nary(chain_arr)
pre, post, levels, depth = traversals(root)
assert depth == 10**4 and pre == list(range(1, 10**4 + 1)) and post == pre[::-1]
try:
    traversals_rec(root); rec = "recursive ok"
except RecursionError:
    rec = "recursive RecursionError"
print(f"10^4-node chain: iterative depth {depth}; {rec}")
```

**Output (my run):**
```
arr=[1, None, 3, 2, 4, None, 5, 6] -> ([1, 3, 5, 6, 2, 4], [5, 6, 3, 2, 4, 1], [[1], [3, 2, 4], [5, 6]], 3)
arr=[] -> ([], [], [], 0)
arr=[7] -> ([7], [7], [[7]], 1)
exhaustive ordered trees ok: 197
300 random N-ary trees ok
10^4-node chain: iterative depth 10000; recursive RecursionError
```

Output prints `None` where the prompt writes `null`. The exhaustive test covers every ordered tree with 1 to 7 nodes (197 shapes): encode with and without the trailing `None`s, decode, compare, and match the recursive brute force. 300 seeded random trees (up to 200 nodes, any fan-out) are cross-checked too.

**Edge cases:**
- Empty array: empty results and depth 0.
- Single node `[7]`: no trailing `None` is needed to parse it.
- A node with no children contributes just its `None`, so a run of `None, None` means two leaves in a row.
- Chain of 10^4 nodes: iterative works, recursion raises `RecursionError`.
- A star (one root, 10^4 children): the level list is wide but the stack is still fine.

**Follow-ups:**
- Why is the postorder trick right? Pushing children left to right makes the stack visit the last child first, so the recorded order is the mirror of "children then node"; reversing gives the real postorder.
- Can you get postorder with one pass and no reversal? Yes, with `(node, next_child_index)` pairs on the stack, which is the version for a binary tree with a visited flag.
- N-ary with parent pointers or random access to children by index? Only the container changes; the traversals do not.

**Common mistakes:**
- Pushing children in forward order for preorder, which visits the last child first.
- Counting depth in edges when the question says nodes (an empty tree is 0, a single node is 1).
- Parsing the input as if every node had exactly two entries; the `None` separators mark the end of each node's child list.
- Trying to define inorder for N-ary trees.

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

