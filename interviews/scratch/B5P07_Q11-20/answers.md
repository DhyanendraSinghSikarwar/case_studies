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
- Allow duplicates on the left only? Change one comparison: left bound becomes `<=` allowed (`val > high` fails instead of `>=`). Say the rule out loud first.
- Which is better? Same big-O. Inorder is shorter to write iteratively and stops early; bounds also generalises to "each node must lie in a range".
- Why is checking only inorder sortedness enough? A tree is a BST exactly when its inorder sequence is strictly increasing, and the code tests that directly.

**Common mistakes:**
- Comparing each node only with its parent.
- Using `<` where `<=` is needed (accepting duplicates).
- Sentinels `-2**31` and `2**31 - 1`.
- Keeping a single global `prev` in a recursive inorder but forgetting it must be initialised to None, not 0 or `-inf` with `<`.

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

