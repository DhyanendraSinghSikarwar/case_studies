import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

class BSTIterator:
    """In-order iterator holding only the current left spine: at most h nodes in the stack."""
    def __init__(self, root):
        self.stack = []; self.pushes = 0; self.max_stack = 0
        self._push_left(root)
    def _push_left(self, node):
        while node is not None:
            self.stack.append(node); self.pushes += 1; node = node.left
        self.max_stack = max(self.max_stack, len(self.stack))
    def hasNext(self):
        return bool(self.stack)
    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)          # the only new work: the left spine of the right child
        return node.val

class FlatIterator:
    """Brute force: flatten to a list in the constructor. O(n) space."""
    def __init__(self, root):
        self.vals, st, cur = [], [], root
        while st or cur:
            while cur: st.append(cur); cur = cur.left
            cur = st.pop(); self.vals.append(cur.val); cur = cur.right
        self.i = 0
    def hasNext(self): return self.i < len(self.vals)
    def next(self):
        self.i += 1; return self.vals[self.i - 1]

def run_ops(it, ops):
    return [getattr(it, o)() for o in ops]

ops = ['next', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext']
r = build_tree([7, 3, 15, None, None, 9, 20])
got = run_ops(BSTIterator(r), ops); assert got == run_ops(FlatIterator(r), ops) == [3, 7, True, 9, True, 15, True, 20, False]
print("root [7, 3, 15, null, null, 9, 20] ->", got)
e = BSTIterator(None); assert e.hasNext() is False
print("empty tree: hasNext() ->", e.hasNext())

# exhaustive: every BST shape up to 8 nodes. Drain it; compare with inorder; stack never above h; each node pushed exactly once.
cnt = 0
for n in range(0, 9):
    for s in shapes(n):
        t = label_inorder(s); root = from_tup(t); h = height(root)
        it = BSTIterator(root); out = []
        while it.hasNext(): out.append(it.next())
        assert out == list(range(n)) and it.max_stack <= h and it.pushes == n
        if n: assert it.max_stack >= 1
        assert not it.hasNext()
        cnt += 1
print("exhaustive ok on", cnt, "BST shapes: output = sorted order, max stack <= h, total pushes = n")

# random interleavings of hasNext/next vs the flat version
def insert(root, v):
    if root is None: return TreeNode(v)
    cur = root
    while True:
        if v < cur.val:
            if cur.left is None: cur.left = TreeNode(v); break
            cur = cur.left
        else:
            if cur.right is None: cur.right = TreeNode(v); break
            cur = cur.right
    return root
random.seed(30)
for _ in range(300):
    root = None
    for v in random.sample(range(1000), random.randint(1, 80)): root = insert(root, v)
    a, b = BSTIterator(root), FlatIterator(root); n = len(nodes_of(root))
    for _ in range(n + 3):
        if random.random() < 0.5:
            assert a.hasNext() == b.hasNext()
        elif b.hasNext():
            assert a.next() == b.next()
print("random interleaving cross-check ok (300 trees)")

# space: balanced vs skewed, n = 2^k - 1 vs a left chain (sandbox counts of the stack peak)
def perfect(lo, hi):
    if lo > hi: return None
    m = (lo + hi) // 2; return TreeNode(m, perfect(lo, m - 1), perfect(m + 1, hi))
bal = BSTIterator(perfect(0, 2 ** 14 - 2))             # n = 16383
while bal.hasNext(): bal.next()
chain = None
for v in range(1, 20001): chain = TreeNode(v, chain, None)   # left chain: root 20000, leftmost 1
ch = BSTIterator(chain); first = ch.next()
print("balanced n = 16383: peak stack =", bal.max_stack, "| left chain n = 20000: stack right after the constructor =", ch.max_stack, "| first value", first)
assert bal.max_stack == 14 and ch.max_stack == 20000
