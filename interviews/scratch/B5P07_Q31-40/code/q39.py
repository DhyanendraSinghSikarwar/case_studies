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

def inorder_nodes(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur); cur = cur.right
    return out

# ---------- brute force: sort the values and write them back in inorder (O(n log n) time, O(n) space) ----------
def recover_brute(root):
    ns = inorder_nodes(root)
    for node, v in zip(ns, sorted(n.val for n in ns)):
        node.val = v
    return root

# ---------- optimal: iterative inorder with a prev pointer, O(h) space; descents = places where prev.val > cur.val ----------
def recover_stack(root, info=None):
    st, cur, prev, first, second, descents = [], root, None, None, None, 0
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop()
        if prev is not None and prev.val > cur.val:
            descents += 1
            if first is None: first = prev       # first descent: the earlier (larger) node is the culprit
            second = cur                         # last descent: the later (smaller) node is the other one
        prev, cur = cur, cur.right
    if info is not None: info.append(descents)
    first.val, second.val = second.val, first.val
    return root

# ---------- O(1) extra space: Morris traversal (temporary threads from each predecessor to its successor) ----------
def recover_morris(root):
    cur, prev, first, second = root, None, None, None
    def visit(node):
        nonlocal prev, first, second
        if prev is not None and prev.val > node.val:
            if first is None: first = prev
            second = node
        prev = node
    while cur:
        if cur.left is None:
            visit(cur); cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur: pred = pred.right
            if pred.right is None:
                pred.right = cur; cur = cur.left            # make the thread, go left
            else:
                pred.right = None; visit(cur); cur = cur.right   # remove the thread, visit, go right
    first.val, second.val = second.val, first.val           # must finish the whole walk so no thread stays
    return root

def run(fn, arr):
    return to_arr(fn(build(arr)))

for arr in ([1, 3, None, None, 2], [3, 1, 4, None, None, 2], [2, 3, 1], [1, 2, 3]):
    a, b, c = run(recover_brute, arr), run(recover_stack, arr), run(recover_morris, arr)
    assert a == b == c
    print(f"root={arr} -> {a}")

def is_bst(root):
    v = [n.val for n in inorder_nodes(root)]
    return all(x < y for x, y in zip(v, v[1:]))

# exhaustive: every BST shape with 2..8 nodes, EVERY pair of nodes whose values were swapped
cases = adjacent = 0
for n in range(2, 9):
    for sh in shapes(n):
        t = label(sh, "in")
        for i in range(n):
            for j in range(i + 1, n):
                orig = from_tup(t)
                ns = inorder_nodes(orig)
                broken = from_tup(t)
                bn = inorder_nodes(broken)
                bn[i].val, bn[j].val = bn[j].val, bn[i].val
                assert not is_bst(broken)
                # uniqueness: swapping values of exactly ONE pair of nodes restores a BST
                fixes = 0
                for a in range(n):
                    for b in range(a + 1, n):
                        bn[a].val, bn[b].val = bn[b].val, bn[a].val
                        fixes += is_bst(broken)
                        bn[a].val, bn[b].val = bn[b].val, bn[a].val
                assert fixes == 1, (n, i, j)
                for fn in (recover_brute, recover_stack, recover_morris):
                    copy = from_tup(t); cn = inorder_nodes(copy); cn[i].val, cn[j].val = cn[j].val, cn[i].val
                    ids = [id(x) for x in nodes_of(copy)]
                    out = fn(copy)
                    assert same(out, orig)                              # values back, shape unchanged
                    assert [id(x) for x in nodes_of(out)] == ids        # same node objects, no thread left behind
                info = []
                cp = from_tup(t); cn = inorder_nodes(cp); cn[i].val, cn[j].val = cn[j].val, cn[i].val
                recover_stack(cp, info)
                assert info[0] == (1 if j == i + 1 else 2)              # adjacent swap: one descent; otherwise two
                adjacent += (j == i + 1)
                cases += 1
print("exhaustive swaps ok:", cases, "(adjacent in inorder:", adjacent, ")")
