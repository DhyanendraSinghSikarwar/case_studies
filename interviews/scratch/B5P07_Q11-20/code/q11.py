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
