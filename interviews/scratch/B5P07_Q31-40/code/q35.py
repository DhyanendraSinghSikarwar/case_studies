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

import subprocess

def skewed(n, shape):
    """Iterative build: no recursion, so building never hits the limit."""
    root = None
    for i in range(n):
        root = TreeNode(i, root, None) if shape == "left" else TreeNode(i, None, root)
    return root

def depth_rec(node):
    return 0 if node is None else 1 + max(depth_rec(node.left), depth_rec(node.right))

def depth_iter(root):
    best, st = 0, ([(root, 1)] if root else [])
    while st:
        node, d = st.pop()
        best = max(best, d)
        if node.left: st.append((node.left, d + 1))
        if node.right: st.append((node.right, d + 1))
    return best

def depth_pair(n, shape):
    root = skewed(n, shape)
    try:
        rec = depth_rec(root)
    except RecursionError:
        rec = "RecursionError"
    return rec, depth_iter(root)

for n, shape in [(500, "left"), (2000, "right"), (1, "left"), (0, "left")]:
    print(f"n={n}, shape={shape!r} -> {depth_pair(n, shape)}")

# cross-check: both shapes, many sizes, recursive and iterative agree wherever recursion survives
limit = sys.getrecursionlimit()
for shape in ("left", "right"):
    for n in list(range(0, 60)) + [300, 500, 900]:
        assert depth_pair(n, shape) == (n, n)
    for n in (1500, 2000, 5000):
        assert depth_pair(n, shape) == ("RecursionError", n)    # far above the default limit
# a mixed zig-zag chain too (the node's one child alternates sides)
z = None
for i in range(1200):
    z = TreeNode(i, z, None) if i % 2 else TreeNode(i, None, z)
assert depth_iter(z) == 1200
print(f"default recursion limit {limit}; recursive fails on 1500+ nodes, iterative never does")

# what does raising the limit really do? Run each probe in a fresh interpreter, so a crash could not hurt this script.
PROBE = """
import sys, resource
sys.setrecursionlimit(10**7)
class N:
    __slots__ = ('left',)
    def __init__(self, left=None): self.left = left
n = int(sys.argv[1])
root = None
for _ in range(n): root = N(root)
def depth(x): return 0 if x is None else 1 + depth(x.left)
before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(depth(root), (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - before) // 1024, "MB extra")
"""
for n in (10**5, 10**6):
    r = subprocess.run([sys.executable, "-I", "-c", PROBE, str(n)], capture_output=True, text=True)
    print(f"limit raised, pure-Python recursion on {n} nodes: rc={r.returncode}", r.stdout.strip() or r.stderr.strip()[-80:])
print("python", sys.version.split()[0])

# recursion that passes through a C wrapper (lru_cache) has its own fixed limit, whatever setrecursionlimit says
PROBE2 = """
import sys, functools
sys.setrecursionlimit(10**7)
@functools.lru_cache(maxsize=None)
def f(n): return 0 if n == 0 else 1 + f(n - 1)
try:
    print(f(int(sys.argv[1])))
except RecursionError:
    print("RecursionError")
"""
for n in (1000, 10**5):
    r = subprocess.run([sys.executable, "-I", "-c", PROBE2, str(n)], capture_output=True, text=True)
    print(f"limit raised to 10^7, lru_cache recursion depth {n}: rc={r.returncode}", r.stdout.strip())
