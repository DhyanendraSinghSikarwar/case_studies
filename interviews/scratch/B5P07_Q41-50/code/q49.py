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
def is_leaf(n): return n.left is None and n.right is None

# ---- optimal: three iterative pieces, no recursion
def boundary(root):
    if root is None: return []
    out = [root.val]
    n = root.left                                     # left boundary, top-down, leaf excluded
    while n and not is_leaf(n):
        out.append(n.val); n = n.left or n.right
    st = [root]                                       # leaves, left to right (root excluded, so a lone root is not repeated)
    while st:
        n = st.pop()
        if is_leaf(n) and n is not root: out.append(n.val)
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    right, n = [], root.right                         # right boundary, collected top-down, leaf excluded
    while n and not is_leaf(n):
        right.append(n.val); n = n.right or n.left
    return out + right[::-1]                          # ... then reversed to go bottom-up

# ---- brute force: one recursive DFS with two flags; left-boundary nodes on entry, leaves in order, right-boundary on exit
def brute(root):
    if root is None: return []
    res = [root.val]
    def go(n, onl, onr):
        if n is None: return
        leaf = n.left is None and n.right is None
        if onl and not leaf: res.append(n.val)
        if leaf: res.append(n.val)
        # a left-boundary node passes the flag to its left child, or to its right child when the left is missing
        go(n.left, onl, onr and n.right is None)
        go(n.right, onl and n.left is None, onr)
        if onr and not leaf: res.append(n.val)
    # the root is already in res; its left/right children start the two boundaries
    go(root.left, True, False)
    go(root.right, False, True)
    return res

# ---- examples from the question
N = None
ex = [([1, N, 2, 3, 4], [1, 3, 4, 2]),
      ([1, 2, 3, 4, 5, 6, N, N, N, 7, 8, 9, 10], [1, 2, 4, 7, 8, 9, 10, 6, 3]),
      ([1], [1]), ([1, 2], [1, 2]), ([], [])]
for arr, want in ex:
    r = build_tree(arr)
    assert boundary(r) == want == brute(r), arr
print('examples ok:', [w for _, w in ex])

# ---- exhaustive: every shape with 0..9 nodes (distinct values), plus a no-duplicates check
count = 0
for n in range(10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre'))
        a, b = boundary(r), brute(r)
        assert a == b, (tup(r), a, b)
        assert len(a) == len(set(a)) and set(a) <= set(range(n))     # no value repeated, only real nodes
        count += 1
print('shapes checked exhaustively (0..9 nodes):', count)

# ---- seeded random trees
random.seed(49)
for _ in range(400):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 100)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    a = boundary(nodes[0]); assert a == brute(nodes[0]) and len(a) == len(set(a))
print('400 random trees ok')

# ---- skewed input of 10^4 nodes: iterative code survives, the recursive brute force does not
chain = TreeNode(0); cur = chain
for i in range(1, 10000): cur.left = TreeNode(i); cur = cur.left
b = boundary(chain)
print('left chain of 10000: boundary length =', len(b), ', first 3 =', b[:3], ', last =', b[-1])
assert b == list(range(10000))
rchain = TreeNode(0); cur = rchain
for i in range(1, 10000): cur.right = TreeNode(i); cur = cur.right
b = boundary(rchain)
print('right chain of 10000: boundary length =', len(b), ', first 3 =', b[:3], ', last =', b[-1])
assert b == [0, 9999] + list(range(9998, 0, -1))
try: brute(chain); print('recursive survived')
except RecursionError: print('recursive brute force on the 10000-deep chain: RecursionError (default limit 1000)')
