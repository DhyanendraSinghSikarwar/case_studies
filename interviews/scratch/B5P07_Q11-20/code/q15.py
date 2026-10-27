import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array with None -> tree. Children of a None are not listed."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def all_nodes(root):
    """Preorder node list; asserts the structure is a tree (no cycle, no shared node)."""
    seen, out, st = set(), [], ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or shared node"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def to_arr(root):
    """Tree -> level-order array with None, trailing Nones trimmed."""
    all_nodes(root)                      # guard first
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def tup(root):                           # structural value (recursive: small trees only)
    return None if root is None else (root.val, tup(root.left), tup(root.right))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

_sh = {0: [None]}
def shapes(n):
    """All binary tree shapes with n nodes as nested (left, right) tuples."""
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode):
    """Give a shape the labels 0..n-1 in 'pre' (preorder) or 'in' (inorder, so a BST) order."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1])
        else:
            L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1])
        return (v, L, R)
    return go(shape)

def chain(n, side="right"):
    """Skewed tree of n nodes built bottom-up (no recursion)."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root) if side == "right" else TreeNode(v, root, None)
    return root

def deep_ok(f, *args):
    """Run f(*args); return its result or the string 'RecursionError'."""
    try:
        return f(*args)
    except RecursionError:
        return "RecursionError"


# ---------- brute force: full inorder list, index k - 1 ----------
def kth_brute(root, k):
    out, st, cur = [], [], root
    while cur or st:
        while cur:
            st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out[k - 1]

# ---------- optimal: iterative inorder, stop after k pops ----------
STATS = {"pops": 0, "pushes": 0, "max_stack": 0}
def kth_smallest(root, k):
    st, cur = [], root
    while cur or st:
        while cur:
            st.append(cur); STATS["pushes"] += 1
            STATS["max_stack"] = max(STATS["max_stack"], len(st))
            cur = cur.left
        cur = st.pop(); STATS["pops"] += 1
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
    raise ValueError("k larger than n")

# ---------- follow-up: store subtree sizes (dict id -> size here; a real node would carry a field) ----------
def build_sizes(root):
    size = {}
    for n in reversed(all_nodes(root)):             # children come after parents in preorder, so reversed = children first
        size[id(n)] = 1 + (size[id(n.left)] if n.left else 0) + (size[id(n.right)] if n.right else 0)
    return size

def kth_by_size(root, k, size):                     # O(h) per query, no traversal
    n = root
    while n:
        left = size[id(n.left)] if n.left else 0
        if k == left + 1: return n.val
        if k <= left: n = n.left
        else: k -= left + 1; n = n.right
    raise ValueError("k larger than n")

def insert_with_size(root, val, size):              # an insert must bump the size of every ancestor
    nd = TreeNode(val); size[id(nd)] = 1
    if root is None: return nd
    cur = root
    while True:
        size[id(cur)] += 1
        side = "left" if val < cur.val else "right"
        nxt = getattr(cur, side)
        if nxt is None:
            setattr(cur, side, nd); return root
        cur = nxt

def height(root):
    h, lvl = 0, [root] if root else []
    while lvl:
        h += 1; lvl = [c for x in lvl for c in (x.left, x.right) if c]
    return h

examples = [([3, 1, 4, None, 2], 1, 1), ([5, 3, 6, 2, 4, None, None, 1], 3, 3),
            ([5, 3, 6, 2, 4, None, None, 1], 6, 6), ([1], 1, 1)]
for arr, k, want in examples:
    r = build_tree(arr); sz = build_sizes(r)
    assert kth_smallest(r, k) == kth_brute(r, k) == kth_by_size(r, k, sz) == want
    print(arr, "k=%d ->" % k, want)

# exhaustive: every BST shape with 1..7 nodes (inorder labels 0..n-1), every k
cases = 0
for n in range(1, 8):
    for s in shapes(n):
        r = from_tup(label(s, "in")); sz = build_sizes(r); h = height(r)
        for k in range(1, n + 1):
            STATS.update(pops=0, pushes=0, max_stack=0)
            assert kth_smallest(r, k) == kth_by_size(r, k, sz) == kth_brute(r, k) == k - 1
            assert STATS["pops"] == k                           # stops right after the k-th pop
            assert STATS["max_stack"] <= h                      # never more than h nodes on the stack
            assert STATS["pushes"] <= k + h - 1                  # pushes = pops + what is left on the stack (< h)
            cases += 1
print("exhaustive ok:", cases, "(BST, k) cases; pops == k and stack <= h every time")

# random BSTs by inserting random distinct keys; sizes maintained under inserts
random.seed(15)
for _ in range(200):
    keys = random.sample(range(-500, 500), random.randint(1, 80))
    root, sz = None, {}
    for key in keys:
        root = insert_with_size(root, key, sz)
        srt = sorted(keys[:keys.index(key) + 1])
        k = random.randint(1, len(srt))
        assert kth_by_size(root, k, sz) == srt[k - 1] == kth_smallest(root, k)
    assert sz == build_sizes(root)                              # incremental sizes match a fresh rebuild
print("random ok: 200 BSTs, sizes kept correct across inserts")

# deep chain: iterative walk copes where recursion would not
deep = chain(10000)
print("chain 10000, k=10000 ->", kth_smallest(deep, 10000), "| k=1 ->", kth_smallest(deep, 1))
