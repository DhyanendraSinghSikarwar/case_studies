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
