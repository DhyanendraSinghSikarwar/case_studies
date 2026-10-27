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
