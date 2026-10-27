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
