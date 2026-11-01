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
# ---- optimal: each call returns (depth, answer node). Equal child depths -> this node; else the deeper child's answer.
def deepest_subtree(root):
    def go(n):
        if n is None: return 0, None
        dl, al = go(n.left); dr, ar = go(n.right)
        if dl == dr: return dl + 1, n
        return (dl + 1, al) if dl > dr else (dr + 1, ar)
    return go(root)[1]

# ---- brute force: list every node with its path from the root; find the deepest; keep the nodes that are a
# prefix (ancestor-or-self) of every deepest node; the lowest of them is the longest path.
def brute(root):
    items, st = [], [(root, '')]
    while st:
        n, p = st.pop(); items.append((n, p))
        if n.left: st.append((n.left, p + 'L'))
        if n.right: st.append((n.right, p + 'R'))
    deepest = max(len(p) for _, p in items)
    paths = [p for _, p in items if len(p) == deepest]
    best = max((x for x in items if all(q.startswith(x[1]) for q in paths)), key=lambda x: len(x[1]))
    return best[0]

def all_nodes(root):
    out, st = [], [root]
    while st:
        n = st.pop(); out.append(n); st += [c for c in (n.left, n.right) if c]
    return out

# ---- examples from the question
N = None
ex = [([3, 5, 1, 6, 2, 0, 8, N, N, 7, 4], [2, 7, 4]), ([1], [1]), ([0, 1, 3, N, 2], [2]), ([1, 2, 3], [1, 2, 3])]
for arr, want in ex:
    r = build_tree(arr); ans = deepest_subtree(r)
    assert to_arr(ans) == want and ans is brute(r)
    assert any(ans is n for n in all_nodes(r))             # a real node of the input tree, not a copy
print('examples ok:', [to_arr(deepest_subtree(build_tree(a))) for a, _ in ex])

# ---- exhaustive: every shape with 1..9 nodes, distinct values (so identity is also checked by `is`)
count = 0
for n in range(1, 10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre'))
        a, b = deepest_subtree(r), brute(r)
        assert a is b
        count += 1
print('shapes checked exhaustively (1..9 nodes):', count)

# ---- seeded random trees with holes, n up to 80
random.seed(47)
for _ in range(400):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 80)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    assert deepest_subtree(nodes[0]) is brute(nodes[0])
print('400 random trees ok')

# ---- same idea as 'LCA of the deepest leaves': check against a generic LCA on the deepest leaf set
def lca(root, targets):
    if root is None or root in targets: return root
    l, r = lca(root.left, targets), lca(root.right, targets)
    return root if l and r else (l or r)
for _ in range(200):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 60)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    depth, st, deep = {}, [(nodes[0], 0)], []
    while st:
        n, d = st.pop(); depth[n] = d
        st += [(c, d + 1) for c in (n.left, n.right) if c]
    m = max(depth.values()); deep = {n for n in nodes if depth[n] == m}
    assert lca(nodes[0], deep) is deepest_subtree(nodes[0])
print('LCA of the deepest-leaf set gives the same node on 200 random trees')

# ---- skewed chain of 500 nodes (the allowed maximum): the deepest node is the only leaf
root = TreeNode(0); cur = root
for i in range(1, 500): cur.right = TreeNode(i); cur = cur.right
assert deepest_subtree(root) is cur
print('chain of 500: the answer is the single leaf', cur.val)
