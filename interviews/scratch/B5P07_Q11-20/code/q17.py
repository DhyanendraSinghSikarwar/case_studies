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
