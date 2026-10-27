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
- Weighted edges or node values (max path sum)? Same shape, return the best downward sum. See Q17.
- Avoid recursion? Iterative post-order with a dict of heights keyed by `id(node)`, as in the code.

**Common mistakes:**
- Assuming the path goes through the root.
- Returning the diameter from the recursion instead of the height (the return value and the running best are different things).
- Forgetting `nonlocal`.
- Recomputing heights: O(n^2).
- Counting nodes when the question says edges.

