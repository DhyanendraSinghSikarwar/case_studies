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
