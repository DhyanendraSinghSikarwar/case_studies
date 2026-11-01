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

# ---------- the required format: level order, '#' for every missing child, nothing trimmed ----------
def serialize(root):
    if root is None:
        return "#"
    out, q = [str(root.val)], deque([root])
    while q:
        n = q.popleft()
        for c in (n.left, n.right):
            if c is None:
                out.append("#")
            else:
                out.append(str(c.val)); q.append(c)
    return ",".join(out)

def deserialize(s):
    tok = s.split(",")
    if tok[0] == "#":
        assert len(tok) == 1
        return None
    root = TreeNode(int(tok[0]))
    q, i = deque([root]), 1
    while q:
        n = q.popleft()
        for side in ("left", "right"):
            if tok[i] != "#":
                c = TreeNode(int(tok[i])); setattr(n, side, c); q.append(c)
            i += 1
    assert i == len(tok), "leftover tokens"
    return root

# ---------- brute force / cross-check format: preorder with '#' (a different, equally valid encoding) ----------
def ser_pre(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None: out.append("#"); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return ",".join(out)

for arr in ([1, 2, 3, None, None, 4, 5], [], [1], [1, None, 2]):
    s = serialize(build(arr))
    assert same(deserialize(s), build(arr))
    print(f"root={arr} -> '{s}'")

# exhaustive: every shape with 0..8 nodes, negative / multi-digit values; round trip + exactly 2n+1 tokens
cases = 0
for n in range(9):
    for sh in shapes(n):
        t = label(sh, "pre", step=-7)               # values 0, -7, -14, ... (negatives and two digits)
        root = from_tup(t)
        s = serialize(root)
        assert len(s.split(",")) == 2 * n + 1        # n values + (n + 1) '#' markers
        assert s.count("#") == n + 1
        assert same(deserialize(s), root)
        assert s == serialize(deserialize(s))        # canonical: serialize(deserialize(s)) == s
        assert ser_pre(root).count("#") == n + 1     # the preorder encoding has the same token count
        cases += 1
print("exhaustive shapes ok:", cases)

# the trimmed array form used by the examples is a different, shorter thing
root = build([1, 2, 3, None, None, 4, 5])
print("trimmed array:", len(to_arr(root)), "entries | full serialization:", len(serialize(root).split(",")), "tokens")

# n = 10^4 skewed tree: BFS and the parser are iterative, so no recursion limit is touched
chain_root = None
for i in range(10**4):
    chain_root = TreeNode(i, chain_root, None)
s = serialize(chain_root)
assert len(s.split(",")) == 2 * 10**4 + 1 and same(deserialize(s), chain_root)
print("10^4-node left chain: round trip ok,", len(s.split(",")), "tokens")

# random trees
random.seed(3)
for _ in range(300):
    n = random.randint(0, 60)
    root = None if n == 0 else TreeNode(random.randint(-99, 99))
    pool = [root] if root else []
    for _ in range(n - 1):
        par = random.choice(pool); side = random.choice(("left", "right"))
        if getattr(par, side) is None:
            c = TreeNode(random.randint(-99, 99)); setattr(par, side, c); pool.append(c)
    assert same(deserialize(serialize(root)), root)
print("300 random trees ok")
