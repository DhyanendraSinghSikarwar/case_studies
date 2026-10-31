import random
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(arr):
    """Level-order array with None -> tree (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def to_arr(root):
    """Tree -> level-order array with None. Asserts no node is reached twice (aliasing or a cycle)."""
    if root is None:
        return []
    seen, out, q = set(), [], deque([root])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        assert id(nd) not in seen, "aliasing or cycle"
        seen.add(id(nd)); out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def nodes_of(root):
    """All nodes by explicit stack (no recursion limit); asserts no aliasing."""
    out, seen, st = [], set(), [root] if root else []
    while st:
        n = st.pop()
        assert id(n) not in seen, "aliasing or cycle"
        seen.add(id(n)); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out

def same_shape(a, b):
    """Structure and value comparison with an explicit stack."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

def shapes(n, _memo={0: [None]}):
    """All binary-tree shapes with n nodes as (left, right) tuples (None = empty)."""
    if n not in _memo:
        _memo[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _memo[n]

def label_inorder(shape, counter=None):
    """Shape -> tuple tree (val, left, right) with values 0..n-1 in INORDER, so it is a BST."""
    counter = counter if counter is not None else [0]
    if shape is None: return None
    L = label_inorder(shape[0], counter); v = counter[0]; counter[0] += 1
    return (v, L, label_inorder(shape[1], counter))

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def tup(r):
    return None if r is None else (r.val, tup(r.left), tup(r.right))
def height(r):   # in nodes, explicit stack
    best, st = 0, [(r, 1)] if r else []
    while st:
        n, d = st.pop(); best = max(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

def build_slices(inorder, postorder):
    """Brute force: slice the lists and use list.index. O(n^2) time and space on skewed trees."""
    if not postorder: return None
    root = postorder[-1]; k = inorder.index(root)
    return TreeNode(root, build_slices(inorder[:k], postorder[:k]),
                    build_slices(inorder[k + 1:], postorder[k:-1]))

def build_in_post(inorder, postorder):
    """O(n): index map + a cursor walking postorder from the END. Right subtree first. Recursion depth = height."""
    pos = {v: i for i, v in enumerate(inorder)}
    assert len(pos) == len(inorder) == len(postorder), "values must be distinct and lists equal length"
    cur = [len(postorder) - 1]
    def go(lo, hi):                                  # inorder window [lo, hi]
        if lo > hi: return None
        v = postorder[cur[0]]; cur[0] -= 1           # the next unused value from the end is this window's root
        node = TreeNode(v)
        k = pos[v]
        node.right = go(k + 1, hi)                   # postorder is left, right, root: reading backward meets RIGHT first
        node.left = go(lo, k - 1)
        return node
    return go(0, len(inorder) - 1)

def build_in_post_iter(inorder, postorder):
    """Same tree with an explicit stack (safe for a 3000-node chain). One pass over postorder from the end."""
    n = len(postorder)
    if n == 0: return None
    root = TreeNode(postorder[-1]); stack = [root]; j = n - 1      # j walks inorder from the end
    for i in range(n - 2, -1, -1):
        node = TreeNode(postorder[i]); parent = stack[-1]
        if parent.val != inorder[j]:
            parent.right = node                       # the parent's own inorder slot is still ahead: we are in its right subtree
        else:
            while stack and stack[-1].val == inorder[j]:
                parent = stack.pop(); j -= 1          # unwind to the ancestor whose LEFT child this is
            parent.left = node
        stack.append(node)
    return root

def tin(t):   return [] if t is None else tin(t[1]) + [t[0]] + tin(t[2])
def tpost(t): return [] if t is None else tpost(t[1]) + tpost(t[2]) + [t[0]]
def tpre(t):  return [] if t is None else [t[0]] + tpre(t[1]) + tpre(t[2])

for ino, post, exp in [([9, 3, 15, 20, 7], [9, 15, 7, 20, 3], [3, 9, 20, None, None, 15, 7]), ([-1], [-1], [-1]),
                       ([2, 1], [2, 1], [1, 2]), ([1, 2], [2, 1], [1, None, 2])]:
    a, b, c = build_in_post(ino, post), build_in_post_iter(ino, post), build_slices(ino, post)
    assert to_arr(a) == to_arr(b) == to_arr(c) == exp, (ino, to_arr(a), to_arr(b))
    print("inorder", ino, "postorder", post, "->", to_arr(a))

# exhaustive: every shape with 1..8 nodes (values are distinct labels): rebuild from (inorder, postorder) and compare structure
cnt = 0; pairs = {}
for n in range(1, 9):
    for s in shapes(n):
        t = label_inorder(s); ino, post = tin(t), tpost(t)
        for fn in (build_in_post, build_in_post_iter, build_slices):
            assert same_shape(fn(ino, post), from_tup(t))
        pairs.setdefault((tuple(ino), tuple(post)), []).append(t); cnt += 1
assert all(len(v) == 1 for v in pairs.values())      # (inorder, postorder) never collides, so the answer is unique
print("exhaustive ok:", cnt, "shapes up to 8 nodes rebuilt by all three builders; every (inorder, postorder) pair is unique")

# random trees with random distinct values (not just inorder labels)
random.seed(29)
for _ in range(300):
    m = random.randint(1, 7); shape = random.choice(shapes(m))
    it = iter(random.sample(range(-100, 100), m))
    def lab(x):
        if x is None: return None
        L = lab(x[0]); v = next(it); return (v, L, lab(x[1]))
    t = lab(shape)
    assert same_shape(build_in_post(tin(t), tpost(t)), from_tup(t)) and same_shape(build_in_post_iter(tin(t), tpost(t)), from_tup(t))
print("random cross-check ok (300 trees with random distinct values)")

# preorder + postorder is NOT enough. Group every labelled shape by (preorder, postorder) after relabelling by preorder (values 0..n-1)
def label_pre(shape, c):
    if shape is None: return None
    v = c[0]; c[0] += 1; L = label_pre(shape[0], c); return (v, L, label_pre(shape[1], c))
def is_full(t): return t is None or ((t[1] is None) == (t[2] is None) and is_full(t[1]) and is_full(t[2]))
def collisions(n):
    g = {}
    for s in shapes(n):
        t = label_pre(s, [0]); g.setdefault((tuple(tpre(t)), tuple(tpost(t))), []).append(t)
    return g
# the fixed-values version: shapes labelled in PREORDER 0..n-1 give the same preorder list for all shapes, so colliding pairs show up as shared keys
for n in range(1, 8):
    g = collisions(n); multi = [k for k, v in g.items() if len(v) > 1]
    uniq_full = all(is_full(v[0]) for v in g.values() if len(v) == 1)
    nonfull_alone = [v for v in g.values() if len(v) == 1 and not is_full(v[0])]
    full_collide = [v for v in g.values() if len(v) > 1 and any(is_full(t) for t in v)]
    assert uniq_full and not full_collide and not nonfull_alone
    print("n =", n, "shapes =", len(shapes(n)), "pairs shared by >= 2 trees =", len(multi), "| every unique pair is a FULL tree, no full tree collides")
g = collisions(2); k = [k for k, v in g.items() if len(v) > 1][0]
print("n = 2 collision: preorder", list(k[0]), "postorder", list(k[1]), "->", [to_arr(from_tup(t)) for t in g[k]])
a, b = g[k]; assert not same_shape(from_tup(a), from_tup(b))

# deep skew: 3000-node left chain. Recursive fails under the default limit, the explicit-stack builder is fine.
n = 3000
ino = list(range(n)); post = list(range(n))   # inorder = postorder = 0..n-1: every node is the LEFT child of the next one
try:
    build_in_post(ino, post); print("recursive: no error")
except RecursionError:
    print("recursive on a 3000-node left chain: RecursionError")
deep = build_in_post_iter(ino, post)
assert height(deep) == n and deep.val == n - 1
print("iterative on the same input: root", deep.val, "height", height(deep))
