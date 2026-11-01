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

# ---------- brute force: build a NEW mirrored tree (correct values, but not in place) ----------
def invert_copy(root):
    if root is None:
        return None
    return TreeNode(root.val, invert_copy(root.right), invert_copy(root.left))

# ---------- optimal 1: recursive, in place ----------
def invert_rec(root):
    if root is None:
        return None
    root.left, root.right = invert_rec(root.right), invert_rec(root.left)   # one swap per node
    return root

# ---------- optimal 2: iterative, in place (stack; a deque gives the same result) ----------
def invert_iter(root):
    st = [root] if root else []
    while st:
        node = st.pop()
        node.left, node.right = node.right, node.left                       # one swap per node
        if node.left: st.append(node.left)
        if node.right: st.append(node.right)
    return root

# ---------- helpers ----------
def all_nodes(root):
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(n)
        for c in (n.left, n.right):
            if c: st.append(c)
    return out
def tmirror(t):
    return None if t is None else (t[0], tmirror(t[2]), tmirror(t[1]))

# ---------- examples ----------
for arr in ([4, 2, 7, 1, 3, 6, 9], [2, 1, 3], [], [1, 2]):
    print(arr, '->', to_level_order(invert_iter(build_tree(arr))), to_level_order(invert_rec(build_tree(arr))))

# ---------- cross-check: every shape up to 7 nodes; identity verified ----------
for t in all_trees(7):
    for fn in (invert_rec, invert_iter):
        root = from_tuple(t)
        before = all_nodes(root)
        ids_before = {id(n) for n in before}
        old_kids = {id(n): (n.left, n.right) for n in before}      # keep references so ids stay valid
        res = fn(root)
        assert res is root                                         # same root object returned
        assert to_tuple(res) == tmirror(t)                         # values/shape mirrored
        after = all_nodes(res)
        assert len(after) == len(before) and {id(n) for n in after} == ids_before   # same node objects
        for n in before:                                           # every node swapped exactly once
            assert (n.left, n.right) == old_kids[id(n)][::-1]
    c = from_tuple(t)
    assert to_tuple(invert_copy(c)) == tmirror(t)
print('all 626 shapes: mirrored, same root, same node objects, each node swapped once')

# the copy version fails the identity test, which is why the prompt checks identity
root = build_tree([1, 2, 3]); ids = {id(n) for n in all_nodes(root)}
new = invert_copy(root)
print('copy reuses nodes:', bool(ids & {id(n) for n in all_nodes(new)}))

# invert twice = original (so a "swap before and after" bug cancels itself out)
root = build_tree([4, 2, 7, 1, 3, 6, 9]); orig = to_level_order(root)
invert_iter(invert_iter(root)); assert to_level_order(root) == orig
def invert_twice_bug(root):
    if root is None: return None
    root.left, root.right = root.right, root.left
    invert_twice_bug(root.left); invert_twice_bug(root.right)
    root.left, root.right = root.right, root.left     # second swap undoes the first
    return root
r = build_tree([2, 1, 3]); invert_twice_bug(r)
print('swapping twice per node leaves', to_level_order(r), '(unchanged)')

random.seed(1)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 99), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(300):
    t = random_tuple(random.randint(0, 80))
    r1, r2 = from_tuple(t), from_tuple(t)
    assert to_tuple(invert_rec(r1)) == to_tuple(invert_iter(r2)) == tmirror(t)
print('random ok: 300')

# ---------- edge cases and depth ----------
assert invert_rec(None) is None and invert_iter(None) is None
one = TreeNode(9); assert invert_iter(one) is one and to_level_order(one) == [9]
n = 100_000
root = None
for i in range(n): root = TreeNode(i, root, None)             # left chain of 10^5 nodes
root = invert_iter(root)
depth, cur = 0, root
while cur: depth, cur = depth + 1, cur.right                  # now it is a right chain
assert depth == n
try:
    invert_rec(root)
except RecursionError:
    print('recursive version raises RecursionError on a 10^5 chain')
print('all asserts passed')
