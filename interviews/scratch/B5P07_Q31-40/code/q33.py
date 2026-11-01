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

# ---------- brute force: all pairs of different nodes ----------
def two_sum_brute(root, k):
    vals = [n.val for n in nodes_of(root)]
    return any(vals[i] + vals[j] == k for i in range(len(vals)) for j in range(i + 1, len(vals)))

# ---------- hash set, O(n) time and space ----------
def two_sum_set(root, k):
    seen, st = set(), ([root] if root else [])
    while st:
        n = st.pop()
        if k - n.val in seen:                 # the partner was seen earlier, so it is a different node
            return True
        seen.add(n.val)
        if n.left: st.append(n.left)
        if n.right: st.append(n.right)
    return False

# ---------- two pointers: ascending and descending iterators, O(h) space ----------
class BSTIter:
    """Yields values in ascending (asc=True) or descending order with a stack of at most h nodes."""
    def __init__(self, root, asc):
        self.asc, self.st, self.peak = asc, [], 0
        self._push(root)
    def _push(self, node):
        while node:
            self.st.append(node)
            node = node.left if self.asc else node.right
        self.peak = max(self.peak, len(self.st))
    def next(self):
        node = self.st.pop()
        self._push(node.right if self.asc else node.left)
        return node.val

def two_sum_iters(root, k, info=None):
    if root is None: return False
    lo, hi = BSTIter(root, True), BSTIter(root, False)
    a, b = lo.next(), hi.next()
    found = False
    while a < b:                              # strict: the two pointers must be different nodes
        s = a + b
        if s == k: found = True; break
        if s < k:
            if not lo.st: break               # a was the last node on its side
            a = lo.next()
        else:
            if not hi.st: break
            b = hi.next()
    if info is not None: info.append(max(lo.peak, hi.peak))
    return found

# examples
base = [5, 3, 6, 2, 4, None, 7]
for arr, k in [(base, 9), (base, 28), ([1], 2), ([2, 1, 3], 4)]:
    t = build(arr)
    a, b, c = two_sum_set(t, k), two_sum_iters(t, k), two_sum_brute(t, k)
    assert a == b == c
    print(f"root={arr}, k={k} -> {a}")

# exhaustive: all BST shapes 0..8 nodes (values 0,3,6,...), every k from -1 to 3n+3
cases, trues = 0, 0
for n in range(1, 9):
    for sh in shapes(n):
        t = from_tup(label(sh, "in", step=3))
        h = height(t)
        for k in range(-1, 3 * n + 4):
            info = []
            a, b, c = two_sum_set(t, k), two_sum_iters(t, k, info), two_sum_brute(t, k)
            assert a == b == c, (n, k)
            assert info[0] <= h                           # stack never deeper than the height
            cases += 1; trues += a
print("exhaustive cases ok:", cases, "(True in", trues, ")")

# the 'same node twice' trap: single node 2, k=4 must be False
assert two_sum_set(build([2]), 4) is False and two_sum_iters(build([2]), 4) is False
# random BSTs with negatives and a bigger size
random.seed(5)
def random_bst(n):
    vals = random.sample(range(-60, 60), n)
    root = None
    for v in vals:
        if root is None: root = TreeNode(v); continue
        cur = root
        while True:
            nxt = "left" if v < cur.val else "right"
            if getattr(cur, nxt) is None: setattr(cur, nxt, TreeNode(v)); break
            cur = getattr(cur, nxt)
    return root
for _ in range(300):
    t = random_bst(random.randint(1, 30)); k = random.randint(-100, 100)
    assert two_sum_set(t, k) == two_sum_iters(t, k) == two_sum_brute(t, k)
print("300 random BSTs with negatives ok")
