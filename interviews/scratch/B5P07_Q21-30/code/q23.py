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

def insert_iter(root, val):
    """Iterative leaf insert; O(h) time, O(1) extra space. Returns the root."""
    node = TreeNode(val)
    if root is None: return node
    cur = root
    while True:
        if val < cur.val:
            if cur.left is None: cur.left = node; return root
            cur = cur.left
        else:                       # val > cur.val (values are distinct and val is not in the tree)
            if cur.right is None: cur.right = node; return root
            cur = cur.right

def insert_tuple(t, val):
    """Independent brute force on tuple trees (recursive, rebuilds the path)."""
    if t is None: return (val, None, None)
    if val < t[0]: return (t[0], insert_tuple(t[1], val), t[2])
    return (t[0], t[1], insert_tuple(t[2], val))

for arr, v, exp in [([4, 2, 7, 1, 3], 5, [4, 2, 7, 1, 3, 5]), ([], 5, [5]),
                    ([40, 20, 60, 10, 30, 50, 70], 25, [40, 20, 60, 10, 30, 50, 70, None, None, 25]), ([1], 0, [1, 0])]:
    r = build_tree(arr); old = nodes_of(r); old_ids = {id(n) for n in old}
    out = insert_iter(r, v)
    assert to_arr(out) == exp, (arr, to_arr(out))
    new = [n for n in nodes_of(out) if id(n) not in old_ids]
    assert len(new) == 1 and new[0].val == v and new[0].left is None and new[0].right is None   # exactly one new LEAF
    if r is not None: assert out is r                                                             # same root object
    print(arr, "insert", v, "->", to_arr(out))

# exhaustive: every BST shape up to 6 nodes (values 0, 2, 4, ...), insert every odd gap value and the two ends
cases = 0
for n in range(0, 7):
    for s in shapes(n):
        t = label_inorder(s)
        def scale(x): return None if x is None else (2 * x[0], scale(x[1]), scale(x[2]))
        t = scale(t)
        for v in range(-1, 2 * n, 2):
            r = from_tup(t); old_ids = {id(x) for x in nodes_of(r)}
            out = insert_iter(r, v)
            assert tup(out) == insert_tuple(t, v)
            assert len([x for x in nodes_of(out) if id(x) not in old_ids]) == 1
            if r: assert out is r
            cases += 1
print("exhaustive ok:", cases, "(shape, value) cases")

# sorted insertion: node k (0-based) is placed after visiting k nodes, so total visits = n(n-1)/2 and the tree is one chain
def insert_counting(root, val):
    visits = 0
    node = TreeNode(val)
    if root is None: return node, 0
    cur = root
    while True:
        visits += 1
        if val < cur.val:
            if cur.left is None: cur.left = node; return root, visits
            cur = cur.left
        else:
            if cur.right is None: cur.right = node; return root, visits
            cur = cur.right
for n in (1, 2, 10, 500):
    root, total = None, 0
    for v in range(n):
        root, c = insert_counting(root, v); total += c
    assert total == n * (n - 1) // 2 and height(root) == n
    print("n =", n, "sorted inserts: visits =", total, "= n(n-1)/2, longest path =", height(root), "nodes")

# a shuffled order gives a much shorter tree (sandbox number, one seed)
random.seed(23)
vals = list(range(2000)); random.shuffle(vals); root = None
for v in vals: root = insert_iter(root, v)
print("2000 shuffled inserts: height =", height(root), "(sorted order would give 2000)")
