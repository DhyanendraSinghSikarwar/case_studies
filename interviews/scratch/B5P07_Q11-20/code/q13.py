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
