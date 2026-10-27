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

# ---------- brute force: serialise both with the canonical level-order array and compare ----------
def same_brute(p, q):
    return to_level_order(p) == to_level_order(q)

# ---------- optimal: walk both trees together; counts calls so the bound can be tested ----------
def same_tree(p, q, calls=None):
    if calls is not None:
        calls[0] += 1
    if p is None and q is None:          # both empty: same
        return True
    if p is None or q is None:           # exactly one empty: different (checked BEFORE .val)
        return False
    return (p.val == q.val
            and same_tree(p.left, q.left, calls)
            and same_tree(p.right, q.right, calls))

# ---------- examples ----------
cases = [([1, 2, 3], [1, 2, 3]), ([1, 2], [1, None, 2]), ([1, 2, 1], [1, 1, 2]), ([], []), ([], [1])]
for a, b in cases:
    p, q = build_tree(a), build_tree(b)
    print(a, b, '->', same_tree(p, q), '| p == q:', p == q)

# ---------- == is identity; the function ignores identity ----------
p, q = build_tree([1, 2, 3]), build_tree([1, 2, 3])
assert p != q and same_tree(p, q) and same_tree(p, p)
assert p is not q and p.left is not q.left        # different objects, same content

# ---------- cross-check: every pair of shapes up to 4 nodes with all-equal values (worst case for work),
# and every pair of preorder-labelled trees (values differ by position) ----------
def sized(t, v):
    """same shape, every value set to v"""
    return None if t is None else (v, sized(t[1], v), sized(t[2], v))
def size(t):
    return 0 if t is None else 1 + size(t[1]) + size(t[2])
pairs = 0
trees = all_trees(4)
for t1 in trees:
    for t2 in trees:
        for a, b in ((t1, t2), (sized(t1, 0), sized(t2, 0))):
            p, q, c = from_tuple(a), from_tuple(b), [0]
            got = same_tree(p, q, c)
            assert got == (a == b) == same_brute(p, q)
            m = min(size(a), size(b))
            assert c[0] <= 2 * m + 1                 # at most 1 + 2 * min(m, n) calls
            pairs += 1
print('pairs checked:', pairs, '| calls never exceed 2*min(m,n)+1')

# the bound is tight for equal trees: n nodes -> n real comparisons + n + 1 empty-pair calls
c = [0]; same_tree(build_tree(list(range(1, 8))), build_tree(list(range(1, 8))), c)
print('equal 7-node trees: calls =', c[0], '(2n + 1 = 15)')

random.seed(3)
for _ in range(500):
    n = random.randint(0, 12)
    arr = [random.randint(0, 1) for _ in range(n)]
    arr2 = list(arr)
    if arr2 and random.random() < 0.5:
        arr2[random.randrange(len(arr2))] = random.randint(0, 1)
    p, q = build_tree(arr), build_tree(arr2)
    assert same_tree(p, q) == same_brute(p, q) == (to_tuple(p) == to_tuple(q))
print('random ok: 500')

# ---------- edge cases ----------
assert same_tree(None, None) and not same_tree(None, TreeNode(0)) and not same_tree(TreeNode(0), None)
assert same_tree(TreeNode(0), TreeNode(0)) and not same_tree(TreeNode(0), TreeNode(1))
try:
    (lambda a, b: a.val == b.val)(None, TreeNode(1))
except AttributeError:
    print('reading .val before the None check would raise AttributeError')
print('all asserts passed')
