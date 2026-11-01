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
