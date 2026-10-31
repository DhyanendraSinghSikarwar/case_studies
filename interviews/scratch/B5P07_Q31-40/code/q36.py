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

# Each version works in place on the same node objects: right = next in preorder, left = None.

def flatten_rec(root):
    """Recursive: each call flattens its subtree and returns the TAIL, so splicing needs no extra walk (O(n) total)."""
    def go(node):
        if node is None:
            return None
        left_tail = go(node.left)
        right_tail = go(node.right)
        if left_tail:                             # splice the flattened left chain between node and its old right
            left_tail.right = node.right
            node.right, node.left = node.left, None
        return right_tail or left_tail or node
    go(root)
    return root

def flatten_prev(root):
    """Reversed postorder (right, left, node) with a prev pointer: each node links to the one that follows it in preorder."""
    prev = None
    def go(node):
        nonlocal prev
        if node is None: return
        go(node.right)
        go(node.left)
        node.right, node.left = prev, None
        prev = node
    go(root)
    return root

def flatten_o1(root):
    """O(1) extra space (Morris style): hang the right subtree under the rightmost node of the left subtree."""
    cur = root
    while cur:
        if cur.left:
            p = cur.left
            while p.right: p = p.right
            p.right = cur.right
            cur.right, cur.left = cur.left, None
        cur = cur.right
    return root

def preorder_ids(root):
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(id(n))
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def chain(root, cap=10**6):
    """Values along the right chain; every left must be None. The cap stops a cycle."""
    out = []
    while root is not None:
        assert root.left is None, "left pointer left behind"
        out.append(root.val)
        root = root.right
        assert len(out) <= cap, "cycle"
    return out

def brute(root):
    """Not in place: new nodes from the preorder values (fails the identity requirement, kept as a value checker)."""
    vals = [n.val for n in nodes_of(root)]
    head = None
    for v in reversed(vals): head = TreeNode(v, None, head)
    return head

def check(fn, arr):
    root = build(arr)
    ids = preorder_ids(root)
    vals = [n.val for n in nodes_of(root)]
    out = fn(root)
    assert out is root or root is None
    assert chain(out) == vals                                   # values in preorder
    assert [id(n) for n in nodes_of(out)] == ids                # SAME node objects, in preorder order
    return chain(out)

for arr in ([1, 2, 5, 3, 4, None, 6], [], [0], [1, None, 2, 3]):
    res = [check(f, arr) for f in (flatten_rec, flatten_prev, flatten_o1)]
    assert res[0] == res[1] == res[2] == chain(brute(build(arr)))
    print(f"root={arr} -> {res[0]}")

# exhaustive: every tree shape with 0..7 nodes, all three versions, identity checked
cases = 0
for n in range(8):
    for sh in shapes(n):
        arr = to_arr(from_tup(label(sh, "pre")))
        for f in (flatten_rec, flatten_prev, flatten_o1):
            check(f, arr)
        cases += 1
print("exhaustive shapes ok:", cases)

# random bigger trees (n up to 300), identity checked, with the O(1)-space version
random.seed(11)
for _ in range(300):
    n = random.randint(0, 300)
    root = None if n == 0 else TreeNode(0)
    pool = [root] if root else []
    for i in range(1, n):
        par = random.choice(pool)
        side = random.choice(("left", "right"))
        if getattr(par, side) is None:
            c = TreeNode(i); setattr(par, side, c); pool.append(c)
    arr = to_arr(root)
    for f in (flatten_rec, flatten_prev, flatten_o1):
        check(f, arr)
print("300 random trees ok")
