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


# ---------- brute force: slice the lists and use list.index (O(n^2)) ----------
def build_slow(pre, ino):
    if not pre:
        return None
    root = TreeNode(pre[0])
    i = ino.index(pre[0])                               # O(n) search
    root.left = build_slow(pre[1:i + 1], ino[:i])       # slicing copies O(n)
    root.right = build_slow(pre[i + 1:], ino[i + 1:])
    return root

# ---------- optimal: dict value -> inorder index, moving preorder pointer ----------
def build(pre, ino):
    pos = {v: i for i, v in enumerate(ino)}
    p = 0
    def go(lo, hi):                                     # build from ino[lo:hi]
        nonlocal p
        if lo >= hi:
            return None
        root = TreeNode(pre[p]); p += 1                 # next preorder value is this subtree's root
        i = pos[root.val]
        root.left = go(lo, i)                           # left must be built first: preorder is root, left, right
        root.right = go(i + 1, hi)
        return root
    return go(0, len(ino))

# ---------- iterative version with a stack (safe on a 3000-node skewed tree) ----------
def build_iter(pre, ino):
    root = TreeNode(pre[0]); stack, j = [root], 0
    for v in pre[1:]:
        node = stack[-1]
        if node.val != ino[j]:                          # inorder has not reached this node yet: v is its left child
            node.left = TreeNode(v); stack.append(node.left)
        else:                                           # unwind to the node that owns v as a right child
            while stack and stack[-1].val == ino[j]:
                node = stack.pop(); j += 1
            node.right = TreeNode(v); stack.append(node.right)
    return root

def pre_of(t): return [] if t is None else [t[0]] + pre_of(t[1]) + pre_of(t[2])
def in_of(t): return [] if t is None else in_of(t[1]) + [t[0]] + in_of(t[2])

examples = [([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),
            ([-1], [-1], [-1]), ([1, 2], [2, 1], [1, 2]), ([1, 2], [1, 2], [1, None, 2])]
for pre, ino, want in examples:
    for f in (build_slow, build, build_iter):
        r = f(pre, ino)
        assert to_arr(r) == want
    print("pre=%s in=%s -> %s" % (pre, ino, to_arr(build(pre, ino))))

# exhaustive: every shape with 1..7 nodes, preorder labels, rebuild from (pre, in)
seen_pairs, total = {}, 0
for n in range(1, 8):
    for s in shapes(n):
        t = label(s, "pre")
        pre, ino = pre_of(t), in_of(t)
        for f in (build_slow, build, build_iter):
            assert tup(f(pre, ino)) == t
        key = (tuple(pre), tuple(ino))
        assert key not in seen_pairs                    # (pre, in) pairs are all different -> identifies the tree
        seen_pairs[key] = t
        total += 1
print("exhaustive ok:", total, "shapes; every (preorder, inorder) pair is distinct, so the pair identifies the tree")

# preorder alone is NOT enough: how many shapes share one preorder?
for n in range(1, 8):
    pres = {tuple(pre_of(label(s, "pre"))) for s in shapes(n)}
    print("n=%d: %d shapes, %d distinct preorder sequence(s)" % (n, len(shapes(n)), len(pres)))
print("two trees, same preorder [1, 2]:", to_arr(build([1, 2], [2, 1])), "and", to_arr(build([1, 2], [1, 2])))

# random relabelling with distinct arbitrary values
random.seed(16)
for _ in range(300):
    n = random.randint(1, 8)
    s = random.choice(shapes(n))
    vals = random.sample(range(-50, 50), n)
    t = label(s, "pre")
    def rel(t): return None if t is None else (vals[t[0]], rel(t[1]), rel(t[2]))
    t = rel(t)
    assert tup(build(pre_of(t), in_of(t))) == t == tup(build_iter(pre_of(t), in_of(t)))
print("random ok: 300 relabelled trees")

# n = 3000 skewed tree: recursion fails under the default limit, the iterative build does not
pre = list(range(1, 3001)); ino = list(range(1, 3001))          # right chain
r = deep_ok(build, pre, ino)
print("right chain 3000 recursive:", r if isinstance(r, str) else "built",
      "| iterative nodes:", len(all_nodes(build_iter(pre, ino))))
ino_rev = pre[::-1]                                              # left chain
print("left chain 3000 iterative nodes:", len(all_nodes(build_iter(pre, ino_rev))))

# work done by slicing: total elements copied on a right chain
copied = 0
def build_count(pre, ino):
    global copied
    if not pre: return None
    root = TreeNode(pre[0]); i = ino.index(pre[0])
    a, b, c, d = pre[1:i + 1], ino[:i], pre[i + 1:], ino[i + 1:]
    copied += len(a) + len(b) + len(c) + len(d)
    root.left = build_count(a, b); root.right = build_count(c, d)
    return root
for n in (100, 200, 400):
    copied = 0
    build_count(list(range(n)), list(range(n)))
    print("slicing copies on a chain of n=%d: %d (about n^2 = %d)" % (n, copied, n * n))
