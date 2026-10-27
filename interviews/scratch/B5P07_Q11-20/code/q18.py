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


NULL = "#"

# ---------- preorder with a null marker for every missing child, comma delimiter ----------
def serialize(root):
    out = []
    def go(n):
        if n is None:
            out.append(NULL); return
        out.append(str(n.val)); go(n.left); go(n.right)
    go(root)
    return ",".join(out)

def deserialize(s):
    toks = iter(s.split(","))
    def go():
        t = next(toks)
        if t == NULL:
            return None
        n = TreeNode(int(t))
        n.left = go()                                   # preorder: left subtree is fully consumed first
        n.right = go()
        return n
    return go()

# ---------- iterative versions (no recursion, safe on a skewed tree) ----------
def serialize_iter(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None:
            out.append(NULL); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)   # left is popped first
    return ",".join(out)

def deserialize_iter(s):
    toks = s.split(",")
    if toks[0] == NULL:
        return None
    root = TreeNode(int(toks[0])); i = 1
    stack = [[root, False]]                             # [node, left child already filled?]
    while stack:
        top = stack[-1]; t = toks[i]; i += 1
        node = None if t == NULL else TreeNode(int(t))
        if not top[1]:
            top[0].left = node; top[1] = True
        else:
            top[0].right = node; stack.pop()
        if node:
            stack.append([node, False])
    assert i == len(toks)                               # every token consumed exactly once
    return root

# ---------- plain preorder (no markers) is ambiguous ----------
def plain_preorder(t): return [] if t is None else [t[0]] + plain_preorder(t[1]) + plain_preorder(t[2])

def same_shape_and_values(a, b):
    sa, sb = [(a, b)], True
    while sa:
        x, y = sa.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        sa.append((x.left, y.left)); sa.append((x.right, y.right))
    return True

examples = [[1, 2, 3, None, None, 4, 5], [], [1], [-1, None, -2, -3]]
for arr in examples:
    r = build_tree(arr)
    s = serialize(r)
    back = deserialize(s)
    assert s == serialize_iter(r)
    assert to_arr(back) == to_arr(deserialize_iter(s)) == arr
    print(arr, "->", repr(s), "->", to_arr(back))

# exhaustive: all shapes with 0..7 nodes, token count is exactly 2n + 1
total = 0
for n in range(8):
    for s in shapes(n):
        r = from_tup(label(s, "pre"))
        text = serialize(r)
        assert len(text.split(",")) == 2 * n + 1, (n, text)
        assert text == serialize_iter(r)
        back, back2 = deserialize(text), deserialize_iter(text)
        assert tup(back) == tup(back2) == tup(r)
        orig = {id(x) for x in all_nodes(r)}
        assert not orig & {id(x) for x in all_nodes(back)}   # a copy, no shared nodes
        total += 1
print("exhaustive ok:", total, "shapes; tokens == 2n + 1 for n = 0..7 (empty tree is one marker)")

# plain preorder collides: count distinct preorder lists vs shapes
for n in range(1, 6):
    pres = {tuple(plain_preorder(label(s, "pre"))) for s in shapes(n)}
    print("n=%d: %d shapes, plain preorder values identify %d of them" % (n, len(shapes(n)), len(pres)))
print("plain preorder of [1,2] as left child and as right child:", plain_preorder((1, (2, None, None), None)), plain_preorder((1, None, (2, None, None))))
print("with markers:", serialize(build_tree([1, 2])), "vs", serialize(build_tree([1, None, 2])))

# negative values, delimiter safe
r = build_tree([-1000, -1, 1000, None, -7])
assert to_arr(deserialize(serialize(r))) == [-1000, -1, 1000, None, -7]
print("negatives ok:", serialize(r))

# random trees, values -1000..1000
random.seed(18)
for _ in range(500):
    arr = [random.randint(-1000, 1000)]
    for _ in range(random.randint(0, 40)):
        arr.append(None if random.random() < 0.35 else random.randint(-1000, 1000))
    r = build_tree(arr)
    s = serialize(r)
    assert s == serialize_iter(r) and to_arr(deserialize(s)) == to_arr(deserialize_iter(s)) == to_arr(r)
    assert len(s.split(",")) == 2 * len(all_nodes(r)) + 1
print("random ok: 500 trees")

# skewed tree with 3000 nodes: recursive versions fail under the default limit, iterative ones work
deep = chain(3000)
text = serialize_iter(deep)
print("skewed 3000: recursive serialize:", "RecursionError" if deep_ok(serialize, deep) == "RecursionError" else "ok",
      "| recursive deserialize:", "RecursionError" if deep_ok(deserialize, text) == "RecursionError" else "ok",
      "| iterative round trip equal:", same_shape_and_values(deep, deserialize_iter(text)), "| tokens:", len(text.split(",")))
