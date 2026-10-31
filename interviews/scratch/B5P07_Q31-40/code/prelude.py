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
