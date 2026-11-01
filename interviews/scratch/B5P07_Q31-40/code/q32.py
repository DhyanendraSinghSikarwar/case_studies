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

def inorder_vals(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

# ---------- brute force: sorted values, then the next one ----------
def succ_brute(root, p):
    vals = inorder_vals(root)                 # O(n) time and space
    i = vals.index(p)
    return vals[i + 1] if i + 1 < len(vals) else None

# ---------- optimal: one walk down, remember the last node where we went left ----------
def succ(root, p, steps=None):
    best, cur = None, root
    while cur is not None:
        if steps is not None: steps[0] += 1
        if p < cur.val:
            best = cur.val                    # cur is bigger than p: a candidate, but maybe a smaller one is deeper
            cur = cur.left
        else:                                 # p >= cur.val: the answer, if any, is strictly to the right
            cur = cur.right
    return best

# ---------- same idea, split into the two textbook cases (finds p first) ----------
def succ_cases(root, p):
    anc, cur = None, root
    while cur.val != p:                       # p is guaranteed to exist
        if p < cur.val: anc, cur = cur, cur.left
        else: cur = cur.right
    if cur.right:                             # case 1: minimum of the right subtree
        cur = cur.right
        while cur.left: cur = cur.left
        return cur.val
    return anc.val if anc else None           # case 2: lowest ancestor whose LEFT subtree holds p

# examples
for arr, p in [([2, 1, 3], 1), ([5, 3, 6, 2, 4, None, None, 1], 6), ([5, 3, 6, 2, 4, None, None, 1], 4),
               ([5, 3, 6, 2, 4, None, None, 1], 2), ([2], 2)]:
    t = build(arr)
    a, b, c = succ(t, p), succ_cases(t, p), succ_brute(t, p)
    assert a == b == c
    print(f"root={arr}, p={p} -> {a}")

# exhaustive: all BST shapes 0..9 nodes, every existing p; also check the step count is at most the height
cases, worst_gap = 0, 0
for n in range(1, 10):
    for sh in shapes(n):
        t = from_tup(label(sh, "in"))
        h = height(t)
        for p in range(n):
            steps = [0]
            got = succ(t, p, steps)
            assert got == succ_brute(t, p) == succ_cases(t, p)
            assert got == (p + 1 if p + 1 < n else None)
            assert steps[0] <= h                          # O(h): never more nodes visited than the height
            worst_gap = max(worst_gap, h - steps[0])
            cases += 1
print("exhaustive cases ok:", cases)

# a p that is NOT in the tree still gets the next larger value (useful follow-up), but only the walk version supports it
t = build([5, 3, 6, 2, 4])
print("next larger than 4.5:", succ(t, 4.5), "| than 1:", succ(t, 1), "| than 9:", succ(t, 9))
