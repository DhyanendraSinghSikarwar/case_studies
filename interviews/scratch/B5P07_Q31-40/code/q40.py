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

class Node:
    __slots__ = ("val", "children")
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children if children is not None else []

def build_nary(arr):
    """[root, None, children of root..., None, children of next node in queue order..., None, ...]; trailing Nones optional."""
    if not arr:
        return None
    root = Node(arr[0])
    q, i = deque([root]), 2
    while q and i <= len(arr):
        node = q.popleft()
        while i < len(arr) and arr[i] is not None:
            c = Node(arr[i]); node.children.append(c); q.append(c); i += 1
        i += 1                                       # skip the None that ends this node's children
    return root

def encode_nary(root, trim=True):
    if root is None:
        return []
    out, q = [root.val, None], deque([root])
    while q:
        node = q.popleft()
        for c in node.children:
            out.append(c.val); q.append(c)
        out.append(None)
    while trim and out and out[-1] is None:
        out.pop()
    return out

# ---------- brute force: plain recursion ----------
def traversals_rec(root):
    if root is None:
        return ([], [], [], 0)
    pre, post = [], []
    def go(n):
        pre.append(n.val)
        for c in n.children: go(c)
        post.append(n.val)
    go(root)
    levels, cur = [], [root]
    def lv(nodes):
        if not nodes: return
        levels.append([n.val for n in nodes]); lv([c for n in nodes for c in n.children])
    lv(cur)
    return (pre, post, levels, len(levels))

# ---------- optimal: explicit stacks and a level loop, no recursion ----------
def traversals(root):
    if root is None:
        return ([], [], [], 0)
    pre, st = [], [root]
    while st:                                        # preorder: pop, record, push children right to left
        n = st.pop(); pre.append(n.val)
        st.extend(reversed(n.children))
    rev, st = [], [root]                             # postorder: (node, then children left to right) reversed
    while st:
        n = st.pop(); rev.append(n.val)
        st.extend(n.children)
    post = rev[::-1]
    levels, cur = [], [root]
    while cur:                                       # level order: one list per level
        levels.append([n.val for n in cur])
        cur = [c for n in cur for c in n.children]
    return (pre, post, levels, len(levels))

for arr in ([1, None, 3, 2, 4, None, 5, 6], [], [7]):
    root = build_nary(arr)
    res = traversals(root)
    assert res == traversals_rec(root)
    print(f"arr={arr} -> {res}")

# exhaustive: every ordered tree with 1..7 nodes as (val, [children]), preorder-labelled; encode -> decode -> compare
def forests(m):                                      # all ordered lists of trees holding m nodes in total
    if m == 0: return [[]]
    out = []
    for first in range(1, m + 1):
        for t in trees(first):
            for rest in forests(m - first): out.append([t] + rest)
    return out
_tc = {}
def trees(n):                                        # shapes only: a tree is a tuple of child shapes
    if n not in _tc: _tc[n] = [tuple(f) for f in forests(n - 1)]
    return _tc[n]
def realise(shape, counter):
    node = Node(counter[0]); counter[0] += 1
    node.children = [realise(s, counter) for s in shape]
    return node
def same_nary(a, b):
    return a.val == b.val and len(a.children) == len(b.children) and all(same_nary(x, y) for x, y in zip(a.children, b.children))
count = 0
for n in range(1, 8):
    for sh in trees(n):
        root = realise(sh, [0])
        for trim in (True, False):
            back = build_nary(encode_nary(root, trim))
            assert same_nary(back, root)
        assert traversals(root) == traversals_rec(root)
        count += 1
print("exhaustive ordered trees ok:", count)

# random trees up to 200 nodes with arbitrary fan-out, cross-checked against the recursive brute force
random.seed(9)
for _ in range(300):
    n = random.randint(1, 200)
    root = Node(0); pool = [root]
    for i in range(1, n):
        p = random.choice(pool); c = Node(i); p.children.append(c); pool.append(c)
    assert traversals(root) == traversals_rec(root)
    assert same_nary(build_nary(encode_nary(root)), root)
print("300 random N-ary trees ok")

# n = 10^4 chain: iterative is fine, recursion is not (limit 1000)
chain_arr = [1, None]
for v in range(2, 10**4 + 1): chain_arr += [v, None]
root = build_nary(chain_arr)
pre, post, levels, depth = traversals(root)
assert depth == 10**4 and pre == list(range(1, 10**4 + 1)) and post == pre[::-1]
try:
    traversals_rec(root); rec = "recursive ok"
except RecursionError:
    rec = "recursive RecursionError"
print(f"10^4-node chain: iterative depth {depth}; {rec}")
