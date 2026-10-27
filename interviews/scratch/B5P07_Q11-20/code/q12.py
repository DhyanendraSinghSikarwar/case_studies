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


# ---------- brute force: compare every node with ALL nodes of its two subtrees ----------
def is_bst_brute(root):
    for n in all_nodes(root):
        if any(x.val >= n.val for x in all_nodes(n.left)):
            return False
        if any(x.val <= n.val for x in all_nodes(n.right)):
            return False
    return True

# ---------- optimal 1: pass (low, high) bounds down; None means "no bound" ----------
def is_bst_bounds(root):
    def ok(n, low, high):
        if n is None:
            return True
        if (low is not None and n.val <= low) or (high is not None and n.val >= high):
            return False
        return ok(n.left, low, n.val) and ok(n.right, n.val, high)
    return ok(root, None, None)

# ---------- optimal 2: iterative inorder must be strictly increasing ----------
def is_bst_inorder(root):
    st, cur, prev = [], root, None
    while cur or st:
        while cur:
            st.append(cur); cur = cur.left
        cur = st.pop()
        if prev is not None and cur.val <= prev:      # <= makes duplicates invalid
            return False
        prev, cur = cur.val, cur.right
    return True

# ---------- the classic wrong answers ----------
def is_bst_parent_only(root):                         # compares a node only with its children
    if root is None: return True
    if root.left and root.left.val >= root.val: return False
    if root.right and root.right.val <= root.val: return False
    return is_bst_parent_only(root.left) and is_bst_parent_only(root.right)

def is_bst_sentinel(root, lo=-2**31, hi=2**31 - 1):   # fake "infinity" breaks on the extremes
    if root is None: return True
    if root.val <= lo or root.val >= hi: return False
    return is_bst_sentinel(root.left, lo, root.val) and is_bst_sentinel(root.right, root.val, hi)

examples = [([2, 1, 3], True), ([5, 1, 4, None, None, 3, 6], False),
            ([5, 4, 6, None, None, 3, 7], False), ([2, 2, 2], False),
            ([-2147483648], True), ([], True)]
for arr, want in examples:
    root = build_tree(arr)
    assert is_bst_bounds(root) == is_bst_inorder(root) == is_bst_brute(root) == want
    print(arr, "->", is_bst_bounds(root))

# wrong versions fail exactly where the prompt says
t = build_tree([5, 4, 6, None, None, 3, 7])
print("parent-only on [5,4,6,null,null,3,7]:", is_bst_parent_only(t), "(wrong, 3 sits right of 5)")
print("sentinel on [-2147483648]:", is_bst_sentinel(build_tree([-2147483648])), "(wrong, should be True)")
print("sentinel on [2147483647]:", is_bst_sentinel(build_tree([2147483647])), "(wrong, should be True)")
for arr in ([2147483647], [-2147483648, None, 2147483647], [2147483647, 2147483647]):
    r = build_tree(arr)
    assert is_bst_bounds(r) == is_bst_inorder(r) == is_bst_brute(r)
    print("None bounds on", arr, "->", is_bst_bounds(r))

# exhaustive: all shapes with 0..5 nodes, every labelling with values from {0,1,2}
count = valid = 0
for n in range(6):
    for s in shapes(n):
        for vals in __import__("itertools").product(range(3), repeat=n):
            it = iter(vals)
            def put(sh):
                return None if sh is None else (next(it), put(sh[0]), put(sh[1]))
            root = from_tup(put(s))                    # preorder labelling
            b = is_bst_brute(root)
            assert is_bst_bounds(root) == is_bst_inorder(root) == b
            count += 1; valid += b
print("exhaustive ok:", count, "labelled trees, of which", valid, "are valid BSTs")

# inorder-labelled shapes up to 7 nodes are always BSTs; swapping two labels breaks it
for n in range(8):
    for s in shapes(n):
        root = from_tup(label(s, "in"))
        assert is_bst_bounds(root) and is_bst_inorder(root)
        if n >= 2:
            ns = all_nodes(root)
            for i in range(n):
                for j in range(i + 1, n):
                    ns[i].val, ns[j].val = ns[j].val, ns[i].val
                    assert is_bst_bounds(root) == is_bst_inorder(root) == is_bst_brute(root) == False
                    ns[i].val, ns[j].val = ns[j].val, ns[i].val
print("inorder-labelled shapes 0..7 are BSTs; every swap of two values is caught")

# random trees, wide integer range including the 32-bit extremes
random.seed(12)
pool = [-2**31, -5, 0, 3, 8, 2**31 - 1]
for _ in range(2000):
    arr = [random.choice(pool)]
    for _ in range(random.randint(0, 12)):
        arr.append(None if random.random() < 0.3 else random.choice(pool))
    r = build_tree(arr)
    assert is_bst_bounds(r) == is_bst_inorder(r) == is_bst_brute(r)
print("random ok: 2000 trees")

# deep chain of 5000 ascending values: inorder version is iterative
deep = chain(5000)
print("chain 5000 inorder:", is_bst_inorder(deep), "| bounds recursive:", deep_ok(is_bst_bounds, deep))
