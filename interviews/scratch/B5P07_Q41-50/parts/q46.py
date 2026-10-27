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
# ---- optimal: inorder walk remembering the previous node; relink left=prev, right=next; close the circle at the end.
# Iterative inorder (explicit stack) so a 10^4-deep skewed tree is safe.
def to_dll(root):
    head = prev = None
    st, cur = [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); nxt = cur.right                  # read the old right child BEFORE overwriting it
        if prev is None: head = cur
        else: prev.right = cur; cur.left = prev
        prev = cur; cur = nxt
    if head: head.left = prev; prev.right = head          # make it circular
    return head

# ---- the recursive version (shown for comparison; depth = tree height)
def to_dll_rec(root):
    prev = head = None
    def go(n):
        nonlocal prev, head
        if n is None: return
        go(n.left)
        if prev is None: head = n
        else: prev.right = n; n.left = prev
        prev = n
        go(n.right)
    go(root)
    if head: head.left = prev; prev.right = head
    return head

# ---- brute force: collect nodes in sorted order, then relink them
def brute(root):
    nodes, st = [], [root] if root else []
    while st:
        n = st.pop(); nodes.append(n)
        for c in (n.left, n.right):
            if c: st.append(c)
    nodes.sort(key=lambda n: n.val)                       # distinct values, so the order is the sorted order
    for i, n in enumerate(nodes):
        n.left, n.right = nodes[i - 1], nodes[(i + 1) % len(nodes)]
    return nodes[0] if nodes else None

def walk(head, n): 
    out, cur = [], head
    for _ in range(n): out.append(cur.val); cur = cur.right
    return out, cur

def verify(head, ids_before, n):
    """identity checks: same node objects, right walk sorted and circular, left walk is the reverse"""
    if n == 0: assert head is None; return
    vals, back = walk(head, n)
    assert back is head                                   # n steps along right returns to the head (circular)
    assert vals == sorted(vals) and len(set(vals)) == n
    seen, cur = [], head
    for _ in range(n): seen.append(id(cur)); cur = cur.right
    assert set(seen) == ids_before and len(seen) == n     # exactly the original node objects, none lost, none new
    cur, back_vals = head, []
    for _ in range(n): cur = cur.left; back_vals.append(cur.val)
    assert back_vals == vals[::-1]                        # left walk from head visits the largest first
    assert head.left.val == vals[-1] and head.left.right is head

def ids_of(root):
    out, st = set(), [root] if root else []
    while st:
        n = st.pop(); out.add(id(n)); st += [c for c in (n.left, n.right) if c]
    return out

# ---- examples from the question
N = None
for arr, want in [([4, 2, 5, 1, 3], [1, 2, 3, 4, 5]), ([], []), ([7], [7]), ([2, N, 3], [2, 3])]:
    r = build_tree(arr); ids = ids_of(r); h = to_dll(r)
    verify(h, ids, len(ids))
    assert (walk(h, len(ids))[0] if h else []) == want
print('examples ok')
one = build_tree([7]); h = to_dll(one); assert h is one and h.left is h and h.right is h
print('single node points at itself on both sides: head.left is head and head.right is head')

# ---- exhaustive over every BST shape up to 8 nodes; three algorithms, node identity checked
count = 0
for n in range(9):
    for sh in shapes(n):
        t = label(sh, 'in')
        for fn in (to_dll, to_dll_rec, brute):
            r = from_tup(t); ids = ids_of(r); verify(fn(r), ids, n)
        count += 1
print('BST shapes checked (0..8 nodes), three methods each, identity verified:', count)

# ---- seeded random BSTs with negatives
random.seed(46)
for _ in range(300):
    vals = random.sample(range(-100, 100), random.randint(1, 30))
    root = None
    for v in vals:
        nd = TreeNode(v)
        if root is None: root = nd; continue
        cur = root
        while True:
            side = 'left' if v < cur.val else 'right'
            if getattr(cur, side) is None: setattr(cur, side, nd); break
            cur = getattr(cur, side)
    ids = ids_of(root); verify(to_dll(root), ids, len(vals))
print('300 random BSTs ok')

# ---- deep skewed input: 10^4 nodes, left chain (values descending down the chain)
root = TreeNode(10000); cur = root
for v in range(9999, 0, -1): cur.left = TreeNode(v); cur = cur.left
ids = ids_of(root)
deep = TreeNode(10000); cur = deep
for v in range(9999, 0, -1): cur.left = TreeNode(v); cur = cur.left
try: to_dll_rec(deep); print('recursive version survived')
except RecursionError: print('recursive version on a 10000-deep chain: RecursionError (default limit 1000)')
h = to_dll(root); verify(h, ids, 10000)
print('iterative version on the same chain: head =', h.val, ', head.left =', h.left.val, ', n steps along right returns to head')
