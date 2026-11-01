from collections import deque
import random
random.seed(41)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):                      # level-order list, None = missing child
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):                         # level-order with None, trailing None trimmed
    out, q = [], deque([root]) if root else deque()
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out

def tup(root):                            # structure + values as nested tuples (iterative: safe on deep trees)
    memo, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if n is None: continue
        if s == 0: st += [(n, 1), (n.right, 0), (n.left, 0)]
        else: memo[id(n)] = (n.val, memo.get(id(n.left)), memo.get(id(n.right)))
    return memo.get(id(root))

def from_tup(t):                          # recursive: use on small shapes only
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def shapes(n, _c={0: [None]}):            # every binary-tree shape with n nodes, as nested pairs
    if n not in _c:
        _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

def label(shape, mode):                   # 'pre' or 'in' numbering 0..n-1 -> value tuples
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
import itertools

# ---- brute force: insert values one by one (iterative; O(n * height), O(n^2) on a skewed tree)
def build_insert(pre):
    root = None
    for v in pre:
        nd = TreeNode(v)
        if root is None: root = nd; continue
        cur = root
        while True:
            side = 'left' if v < cur.val else 'right'
            nxt = getattr(cur, side)
            if nxt is None: setattr(cur, side, nd); break
            cur = nxt
    return root

# ---- optimal: upper bound + moving index, O(n). Recursive form (depth = tree height).
def build_bound(pre):
    i = 0
    def go(bound):
        nonlocal i
        if i == len(pre) or pre[i] > bound: return None      # next value belongs to an ancestor's right side
        nd = TreeNode(pre[i]); i += 1
        nd.left = go(nd.val)                                  # left subtree: values below nd.val
        nd.right = go(bound)                                  # right subtree: values below the inherited bound
        return nd
    return go(float('inf'))

# ---- same O(n), explicit stack: safe for a 3000-deep skewed input
def build_stack(pre):
    if not pre: return None
    root = TreeNode(pre[0]); st = [root]
    for v in pre[1:]:
        nd = TreeNode(v); last = None
        while st and st[-1].val < v: last = st.pop()          # v is bigger: climb to the parent whose right slot is free
        if last: last.right = nd
        else: st[-1].left = nd
        st.append(nd)
    return root

def preorder(root):
    out, st = [], [root] if root else []
    while st:
        n = st.pop(); out.append(n.val)
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def inorder(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

# ---- examples from the question
N = None
ex = [([8, 5, 1, 7, 10, 12], [8, 5, 10, 1, 7, N, 12]), ([1], [1]), ([3, 1, 2], [3, 1, N, N, 2]), ([1, 2, 3], [1, N, 2, N, 3])]
for pre, want in ex:
    for f in (build_insert, build_bound, build_stack):
        assert to_arr(f(pre)) == want, (f.__name__, pre)
print('examples ok:', [to_arr(build_bound(p)) for p, _ in ex])

# ---- exhaustive: every BST shape up to 8 nodes; the three builders agree and recover the tree
seen, count = set(), 0
for n in range(1, 9):
    for sh in shapes(n):
        t = label(sh, 'in'); pre = preorder(from_tup(t))
        assert tup(build_insert(pre)) == tup(build_bound(pre)) == tup(build_stack(pre)) == t
        assert tuple(pre) not in seen                           # different trees never share a preorder
        seen.add(tuple(pre)); count += 1
print('BST shapes 1..8 nodes: all three builders recover the tree;', count, 'distinct preorders (preorder is injective)')

# ---- exhaustive count: which permutations of 0..n-1 are a valid BST preorder? exactly Catalan(n) of them
for n in range(1, 8):
    ok = 0
    for p in itertools.permutations(range(n)):
        r = build_bound(list(p))
        if preorder(r) == list(p) and inorder(r) == sorted(p): ok += 1   # a real BST whose preorder is p
    assert ok == len(shapes(n)), (n, ok)
print('valid preorders among all permutations of n<=7 = number of shapes (1,2,5,14,42,132,429)')

# ---- precondition: the bound builder does NOT validate its input. [1, 2, 0] is not a BST preorder:
bad = build_bound([1, 2, 0])
print('invalid preorder [1, 2, 0] -> built a tree whose inorder is', inorder(bad), '(not sorted: garbage in, garbage out)')
assert inorder(bad) != sorted(inorder(bad))

# ---- seeded random distinct values, including negatives
random.seed(44)
for _ in range(400):
    vals = random.sample(range(-50, 50), random.randint(1, 12))
    r1 = build_insert(vals); pre = preorder(r1)
    assert tup(build_bound(pre)) == tup(build_stack(pre)) == tup(r1)
print('400 random cases ok')

# ---- inorder is not needed: sorted(pre) is the inorder, so it adds no information
sh = shapes(6)[17]; t = label(sh, 'in'); pre = preorder(from_tup(t))
assert sorted(pre) == list(range(6))
print('inorder of a BST is sorted(pre):', sorted(pre))

# ---- worst case: 3000 ascending values = right-skewed tree of height 3000
pre = list(range(1, 3001))
r = build_stack(pre); assert preorder(r) == pre
try: build_bound(pre); print('recursive built it?')
except RecursionError: print('build_bound on 3000 ascending values: RecursionError (default limit 1000); build_stack is fine')
