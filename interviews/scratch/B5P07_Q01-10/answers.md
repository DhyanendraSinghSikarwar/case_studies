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
