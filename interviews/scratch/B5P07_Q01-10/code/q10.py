import random
from collections import deque

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(arr):
    """Level-order array (None = missing child) -> root. One pass, deque + index."""
    arr = list(arr)
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q, i = deque([root]), 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    """Canonical array; asserts no node is reached twice (cycle or shared node)."""
    if root is None:
        return []
    out, q, seen = [], deque([root]), set()
    while q:
        node = q.popleft()
        if node is None:
            out.append(None); continue
        assert id(node) not in seen, "cycle or shared node"
        seen.add(id(node))
        out.append(node.val); q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

# ---- exhaustive shapes as nested tuples (left, right); labelled by preorder index
_SH = {0: [None]}
def shapes(n):
    if n not in _SH:
        _SH[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _SH[n]
def label_pre(s, c=None):
    """shape -> tuple tree (val, left, right) with values 0..n-1 in preorder."""
    c = c if c is not None else [0]
    if s is None:
        return None
    v = c[0]; c[0] += 1
    L = label_pre(s[0], c)
    return (v, L, label_pre(s[1], c))
def from_tuple(t):
    return None if t is None else TreeNode(t[0], from_tuple(t[1]), from_tuple(t[2]))
def to_tuple(r):
    return None if r is None else (r.val, to_tuple(r.left), to_tuple(r.right))
def all_trees(max_n):
    return [label_pre(s) for n in range(max_n + 1) for s in shapes(n)]

# ---------- brute force on tuples: definition at every node ----------
def th(t): return 0 if t is None else 1 + max(th(t[1]), th(t[2]))
def balanced_def(t):
    return t is None or (abs(th(t[1]) - th(t[2])) <= 1 and balanced_def(t[1]) and balanced_def(t[2]))

# ---------- top-down: recompute the height at every node (counts node visits made by height) ----------
def height(n, c):
    if n is None: return 0
    c[0] += 1
    return 1 + max(height(n.left, c), height(n.right, c))
def balanced_top_down(root, c=None):
    c = c if c is not None else [0]
    if root is None: return True
    return (abs(height(root.left, c) - height(root.right, c)) <= 1
            and balanced_top_down(root.left, c) and balanced_top_down(root.right, c))

# ---------- single pass: return the height, or -1 as "unbalanced" ----------
def check(n, c):
    if n is None: return 0
    c[0] += 1
    lh = check(n.left, c)
    if lh == -1: return -1
    rh = check(n.right, c)
    if rh == -1 or abs(lh - rh) > 1: return -1
    return 1 + max(lh, rh)
def balanced(root, c=None):
    return check(root, c if c is not None else [0]) != -1

# ---------- single pass, iterative (post-order with an explicit stack): safe for a 5000-node chain ----------
def balanced_iter(root):
    if root is None: return True
    h, st = {}, [(root, False)]                 # h maps id(node) -> height of its subtree
    while st:
        n, done = st.pop()
        if not done:
            st.append((n, True))
            if n.right: st.append((n.right, False))
            if n.left: st.append((n.left, False))
        else:
            lh = h[id(n.left)] if n.left else 0
            rh = h[id(n.right)] if n.right else 0
            if abs(lh - rh) > 1: return False
            h[id(n)] = 1 + max(lh, rh)
    return True

# ---------- wrong: only the root's two heights ----------
def root_only(root):
    c = [0]
    return root is None or abs(height(root.left, c) - height(root.right, c)) <= 1

# ---------- examples ----------
for arr in ([3, 9, 20, None, None, 15, 7], [1, 2, 2, 3, 3, None, None, 4, 4], [], [1, 2, None, 3]):
    r = build_tree(arr)
    print(arr, '->', balanced(r), balanced_top_down(r))

# ---------- cross-check: every shape up to 9 nodes (4862 shapes at n = 9) ----------
total = bad_root = 0; worst_top = worst_one = 0
first_counter = None
for n in range(10):
    for s in shapes(n):
        t = label_pre(s); r = from_tuple(t)
        exp = balanced_def(t)
        c1, c2 = [0], [0]
        assert balanced(r, c1) == balanced_top_down(r, c2) == balanced_iter(r) == exp
        assert c1[0] <= n                                    # single pass: at most one visit per node
        worst_one = max(worst_one, c1[0]); worst_top = max(worst_top, c2[0])
        if root_only(r) != exp:
            bad_root += 1
            if first_counter is None: first_counter = to_level_order(r)
        total += 1
print('shapes checked:', total, '| root-only check wrong on', bad_root, '| smallest counter-example', first_counter)
r = build_tree([1, 2, 2, 3, None, None, 3, 4, None, None, 4])
print('tall twin chains: root heights equal ->', root_only(r), '| balanced ->', balanced(r))
assert root_only(r) and not balanced(r)

# ---------- cost: height recomputation (top-down) versus one pass ----------
def perfect(k): return None if k == 0 else TreeNode(0, perfect(k - 1), perfect(k - 1))
for k in (4, 8, 12):
    c1, c2 = [0], [0]; r = perfect(k)
    assert balanced(r, c1) and balanced_top_down(r, c2)
    print('perfect k=%2d n=%5d: single pass %5d visits, top-down %6d visits (about n*log2(n+1) = %d)' % (k, 2**k - 1, c1[0], c2[0], (2**k - 1) * k))

random.seed(12)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 9), random_tuple(l), random_tuple(n - 1 - l))
def near_balanced(n):                  # split sizes almost evenly so that many trees are balanced
    if n == 0: return None
    l = (n - 1) // 2 + random.choice((0, 0, 0, 1, -1)) if n > 2 else random.randint(0, n - 1)
    l = max(0, min(n - 1, l)); return (0, near_balanced(l), near_balanced(n - 1 - l))
yes = 0
for _ in range(600):
    t = random_tuple(random.randint(0, 40)) if _ % 2 else near_balanced(random.randint(0, 60))
    r = from_tuple(t); e = balanced_def(t); yes += e
    assert balanced(r) == balanced_top_down(r) == balanced_iter(r) == e
print('random ok: 600 (balanced among them: %d)' % yes)

# ---------- edge cases ----------
assert balanced(None) and balanced(TreeNode(1))
assert not balanced(build_tree([1, 2, None, 3]))
chain = None
for _ in range(5000): chain = TreeNode(0, chain, None)          # n = 5000, the prompt's maximum
assert not balanced_iter(chain)
try:
    balanced(chain)
except RecursionError:
    print('recursive single pass: RecursionError on a 5000-node chain (default limit 1000); iterative answers False')
assert balanced_iter(build_tree([1, 2, 3, 4, 5, 6, 7]))
print('all asserts passed')
