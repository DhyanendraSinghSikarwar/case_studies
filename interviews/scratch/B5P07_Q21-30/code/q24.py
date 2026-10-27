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

def metrics(root):
    """(visits, max_recursion_depth, max_stack, max_queue). Empty tree -> all zeros.
    max_queue counts the initial deque([root]) (length 1) too, so a single node gives 1."""
    if root is None: return (0, 0, 0, 0)
    # recursive inorder, only called on non-null nodes: count simultaneously active calls
    live = peak = visits = 0
    def rec(n):
        nonlocal live, peak, visits
        live += 1; peak = max(peak, live)
        if n.left: rec(n.left)
        visits += 1
        if n.right: rec(n.right)
        live -= 1
    rec(root)
    # iterative inorder, exactly the loop in the prompt
    stack, cur, mx_stack, v2 = [], root, 0, 0
    while stack or cur:
        while cur:
            stack.append(cur); mx_stack = max(mx_stack, len(stack)); cur = cur.left
        cur = stack.pop(); v2 += 1; cur = cur.right
    # level order with a deque
    q, mx_q, v3 = deque([root]), 1, 0
    while q:
        n = q.popleft(); v3 += 1
        for c in (n.left, n.right):
            if c is not None:
                q.append(c); mx_q = max(mx_q, len(q))
    assert visits == v2 == v3
    return (visits, peak, mx_stack, mx_q)

for arr, exp in [([1, 2, 3, 4, 5, 6, 7], (7, 3, 3, 4)), ([1, 2, None, 3, None, 4], (4, 4, 4, 1)),
                 ([1, None, 2, None, 3, None, 4], (4, 4, 1, 1)), ([], (0, 0, 0, 0))]:
    got = metrics(build_tree(arr)); assert got == exp, (arr, got); print(arr, "->", got)

def widest(root):
    best, level = 0, [root] if root else []
    while level:
        best = max(best, len(level)); level = [c for n in level for c in (n.left, n.right) if c]
    return best

# exhaustive over every shape with 0..8 nodes: recursion depth = h exactly, stack <= h, w <= queue <= n
cnt = 0
for n in range(0, 9):
    for s in shapes(n):
        r = from_tup(label_inorder(s)); v, rd, ms, mq = metrics(r); h, w = height(r), widest(r)
        assert v == n and rd == h and ms <= h and w <= mq <= n, (s, v, rd, ms, mq, h, w)
        if n: assert mq >= 1
        cnt += 1
print("exhaustive ok on", cnt, "tree shapes: visits = n, recursion depth = h, stack <= h, widest level <= queue <= n")

# the three shapes the question asks about, at n = 255 / 256 nodes (sandbox numbers)
def perfect(k):   # k levels
    return None if k == 0 else TreeNode(1, perfect(k - 1), perfect(k - 1))
def left_chain(n):
    r = None
    for _ in range(n): r = TreeNode(1, r, None)
    return r
def right_chain(n):
    r = None
    for _ in range(n): r = TreeNode(1, None, r)
    return r
print("perfect, 8 levels, n = 255:", metrics(perfect(8)), "(h = 8, widest level = 128)")
print("left chain, n = 200      :", metrics(left_chain(200)), "(h = 200, w = 1)")
print("right chain, n = 200     :", metrics(right_chain(200)), "(h = 200, w = 1)")
assert metrics(left_chain(200)) == (200, 200, 200, 1) and metrics(right_chain(200))[2:] == (1, 1)
# perfect tree: test the exact queue peak for k = 1..9
for k in range(1, 10):
    got = metrics(perfect(k))
    assert got[1] == got[2] == k and got[3] == max(1, 2 ** (k - 1)), (k, got)
print("perfect trees k = 1..9: queue peak = 2^(k-1) exactly, recursion = stack = k")
# Python limit: recursion of depth 1500 on a left chain fails by default; the explicit-stack loop does not
try:
    metrics(left_chain(1500)); print("no error")
except RecursionError:
    print("recursive inorder on a 1500-node chain: RecursionError")
