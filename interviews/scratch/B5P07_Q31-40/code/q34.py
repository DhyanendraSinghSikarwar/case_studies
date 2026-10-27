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

# ---------- brute force: O(n) BFS count ----------
def count_brute(root):
    return len(nodes_of(root))

# ---------- optimal: perfect subtrees counted by formula; steps = executions of cur = cur.left / cur.right ----------
STEPS = [0]

def left_depth(node):
    d = 0
    while node.left:
        node = node.left; d += 1; STEPS[0] += 1
    return d

def right_depth(node):
    d = 0
    while node.right:
        node = node.right; d += 1; STEPS[0] += 1
    return d

def count_complete(node):
    if node is None:
        return 0
    l, r = left_depth(node), right_depth(node)
    if l == r:
        return (1 << (l + 1)) - 1             # perfect subtree of height l: 2^(l+1) - 1 nodes
    return 1 + count_complete(node.left) + count_complete(node.right)

def run(n):
    STEPS[0] = 0
    root = build(list(range(1, n + 1)))       # level-order 1..n is exactly a complete tree with n nodes
    return count_complete(root), STEPS[0], root

# examples
for arr in ([1, 2, 3, 4, 5, 6], [], [1], [1, 2, 3, 4, 5, 6, 7], list(range(1, 11))):
    root = build(arr)
    assert count_complete(root) == count_brute(root) == len(arr)
    print(f"root={arr} -> {count_complete(root)}")

# every n up to 2^11: count is right, steps <= 2h^2, and the maximum per h is where the question says
max_steps = {}
for n in range(1, 2 ** 11 + 1):
    cnt, steps, root = run(n)
    assert cnt == n
    h = n.bit_length() - 1                    # floor(log2 n)
    assert steps <= 2 * h * h, (n, steps)
    if n == 2 ** (h + 1) - 1:
        assert steps == 2 * h                 # perfect tree: exactly one left and one right spine
    if h < 11 and steps > max_steps.get(h, (-1, 0))[1]:   # h = 11 has only n = 2^11 in range, so no maximum is taken there
        max_steps[h] = (n, steps)
for h in range(2, 11):
    n_star, s = max_steps[h]
    assert n_star == 2 ** (h + 1) - 2 and s == h * (2 * h - 1), (h, n_star, s)
print("all n <= 2^11: count ok, steps <= 2h^2 ok, perfect n gives 2h, worst n = 2^(h+1)-2 gives h(2h-1) for h=2..10")

# boundary cases for every h up to 13
rows = []
for h in range(1, 14):
    for n in (2 ** h, 2 ** (h + 1) - 2, 2 ** (h + 1) - 1):
        cnt, steps, _ = run(n)
        assert cnt == n and steps <= 2 * h * h
        if n == 2 ** (h + 1) - 1: assert steps == 2 * h
        if n == 2 ** (h + 1) - 2 and h >= 2: assert steps == h * (2 * h - 1)
        rows.append((h, n, steps))
print("spine steps by h:  n=2^h   n=2^(h+1)-2   n=2^(h+1)-1   2h^2")
by_h = {}
for h, n, s in rows: by_h.setdefault(h, []).append(s)
for h in (1, 2, 3, 5, 8, 13):
    a, b, c = by_h[h]
    print(f"h={h:<2}              {a:>6} {b:>12} {c:>13} {2*h*h:>6}")

# h = 1 for reference (n = 2 and 3), and an empty tree costs nothing
print("n=2 steps:", run(2)[1], "| n=3 steps:", run(3)[1], "| empty:", count_complete(None))
