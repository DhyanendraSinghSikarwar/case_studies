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

def vertical_sorted(root):
    """Walk with BFS, record (col, row, val), sort, group by column. O(n log n)."""
    if root is None: return []
    rec, q = [], deque([(root, 0, 0)])
    while q:
        n, col, row = q.popleft(); rec.append((col, row, n.val))
        if n.left:  q.append((n.left, col - 1, row + 1))
        if n.right: q.append((n.right, col + 1, row + 1))
    rec.sort()                                         # column, then row, then value (the tie rule)
    out, last = [], None
    for col, row, v in rec:
        if col != last: out.append([]); last = col
        out[-1].append(v)
    return out

def vertical_first_come(root):
    """BFS with per-column buckets. Ties (same row and column) keep BFS order = left-to-right. O(n)."""
    if root is None: return []
    buckets, q = {}, deque([(root, 0)])
    while q:
        n, col = q.popleft(); buckets.setdefault(col, []).append(n.val)
        if n.left:  q.append((n.left, col - 1))
        if n.right: q.append((n.right, col + 1))
    return [buckets[c] for c in range(min(buckets), max(buckets) + 1)]

def vertical_dfs(root):
    """DFS version (explicit stack): the sort puts rows back in order, so DFS visiting order does not matter."""
    rec, st = [], [(root, 0, 0)] if root else []
    while st:
        n, col, row = st.pop(); rec.append((col, row, n.val))
        if n.right: st.append((n.right, col + 1, row + 1))
        if n.left:  st.append((n.left, col - 1, row + 1))
    rec.sort(); cols = {}
    for c, r, v in rec: cols.setdefault(c, []).append(v)
    return [cols[c] for c in sorted(cols)]

def vertical_tuple(t):
    """Independent brute force on tuple trees: for each column, nodes sorted by (row, value)."""
    nodes = []
    def go(t, c, r):
        if t is None: return
        nodes.append((c, r, t[0])); go(t[1], c - 1, r + 1); go(t[2], c + 1, r + 1)
    go(t, 0, 0)
    return [[v for (cc, r, v) in sorted(x for x in nodes if x[0] == c)] for c in sorted({x[0] for x in nodes})]

for arr, exp in [([3, 9, 20, None, None, 15, 7], [[9], [3, 15], [20], [7]]),
                 ([1, 2, 3, 4, 5, 6, 7], [[4], [2], [1, 5, 6], [3], [7]]),
                 ([3, 1, 4, 0, 2, 2], [[0], [1], [3, 2, 2], [4]]), ([], [])]:
    r = build_tree(arr); a = vertical_sorted(r)
    assert a == vertical_dfs(r) == exp, (arr, a)
    print(arr, "->", a)

# exhaustive over shapes up to 7 nodes with values from {0,1,2} so ties on (col,row) with different values occur
random.seed(28); cnt = diff = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(3):
            vals = iter(random.randint(0, 2) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return (v, L, lab(x[1]))
            t = lab(s); r = from_tup(t)
            assert vertical_sorted(r) == vertical_dfs(r) == vertical_tuple(t)
            f = vertical_first_come(r)
            assert [sorted(c) for c in f] == [sorted(c) for c in vertical_sorted(r)]      # same groups, maybe different order inside a column
            assert [len(c) for c in f] == [len(c) for c in vertical_sorted(r)]
            if f != vertical_sorted(r): diff += 1
            cnt += 1
print("exhaustive+random ok:", cnt, "trees; first-come order differs from the sorted tie rule on", diff, "of them")
# one concrete difference
ex = build_tree([1, 2, 3, None, 5, 4])      # 5 and 4 share column 0 and row 2; 5 is left of 4 in BFS, but 4 < 5
print("tie example [1, 2, 3, None, 5, 4]: sorted rule", vertical_sorted(ex), "| first-come", vertical_first_come(ex))
big = build_tree([random.randint(0, 99) for _ in range(1000)])
assert vertical_sorted(big) == vertical_dfs(big) and sum(map(len, vertical_sorted(big))) == 1000
print("n = 1000 random tree: columns =", len(vertical_sorted(big)))
