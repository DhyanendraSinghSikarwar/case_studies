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
