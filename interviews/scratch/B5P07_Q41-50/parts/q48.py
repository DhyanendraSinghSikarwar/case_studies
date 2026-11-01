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
def morris(root, visit=None, stats=None):
    """Inorder with O(1) extra space. Returns (values, loop iterations). stats['walk'] counts predecessor steps."""
    out, cur, it = [], root, 0
    while cur:
        it += 1
        if cur.left is None:
            out.append(cur.val)
            if visit: visit(cur)
            cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur:   # rightmost of the left subtree, or the thread
                pred = pred.right
                if stats is not None: stats['walk'] += 1
            if pred.right is None:
                pred.right = cur; cur = cur.left                      # first arrival: thread, go left
            else:
                pred.right = None                                     # second arrival: remove the thread
                out.append(cur.val)
                if visit: visit(cur)
                cur = cur.right
    return out, it

def inorder_stack(root):                                              # reference
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

def snapshot(root):                                                   # identity picture of the tree: (node, left, right)
    out, st = [], [root] if root else []
    while st:
        n = st.pop(); out.append((id(n), id(n.left), id(n.right))); st += [c for c in (n.left, n.right) if c]
    return sorted(out)

def count_left(root):
    return sum(1 for n in all_nodes(root) if n.left)
def all_nodes(root):
    out, st = [], [root] if root else []
    while st:
        n = st.pop(); out.append(n); st += [c for c in (n.left, n.right) if c]
    return out

# ---- examples from the question
N = None
ex = [([1, N, 2, 3], ([1, 3, 2], 4)), ([4, 2, 6, 1, 3, 5, 7], ([1, 2, 3, 4, 5, 6, 7], 10)), ([], ([], 0)), ([1, 2, N, 3], ([3, 2, 1], 5))]
for arr, want in ex:
    r = build_tree(arr); before = snapshot(r)
    assert morris(r) == want, arr
    assert snapshot(r) == before and to_arr(r) == arr            # restored: same objects, same pointers, same values
print('examples ok:', [morris(build_tree(a)) for a, _ in ex])

# ---- exhaustive: every shape 0..9 nodes: values, loop count n + L, restoration by identity, walk bound
count = 0
for n in range(10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre')); before = snapshot(r)
        st = {'walk': 0}
        vals, it = morris(r, stats=st)
        assert vals == inorder_stack(r)
        assert it == n + count_left(r)                            # each node with a left child is reached twice
        assert snapshot(r) == before                              # every pointer back where it was
        assert st['walk'] <= 2 * n                                # total predecessor steps never above 2n
        count += 1
print('shapes checked (0..9 nodes):', count, '- loop count = n + L, tree restored by identity, predecessor steps <= 2n')

# ---- tightness of the 2n bound? largest ratio seen
best = 0
for n in range(1, 10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre')); st = {'walk': 0}; morris(r, stats=st); best = max(best, st['walk'] / n)
print('largest (predecessor steps) / n over all shapes up to 9 nodes: %.3f' % best)

# ---- seeded random trees: same checks
random.seed(48)
for _ in range(300):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 150)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    r = nodes[0]; before = snapshot(r)
    vals, it = morris(r)
    assert vals == inorder_stack(r) and it == len(nodes) + count_left(r) and snapshot(r) == before
print('300 random trees ok')

# ---- unsafe if interrupted: a visit() that raises leaves threads behind (compare pointers on the saved node list,
# because a normal traversal of a threaded tree would loop forever)
r = build_tree([4, 2, 6, 1, 3, 5, 7]); nodes = all_nodes(r); before = [(id(n.left), id(n.right)) for n in nodes]
def boom(n):
    if n.val == 3: raise RuntimeError('stop midway')
try: morris(r, visit=boom)
except RuntimeError: pass
after = [(id(n.left), id(n.right)) for n in nodes]
print('after an exception at value 3, pointers restored?', after == before)
assert after != before
was_none = [b[1] == id(None) for b in before]
leftover = [(n.val, n.right.val) for n, w in zip(nodes, was_none) if w and n.right is not None]
print('nodes that had no right child but now point to one (value, target) - the thread left behind:', leftover)
assert leftover

# ---- deep skewed trees: fine, no recursion at all
chain = TreeNode(0); cur = chain
for i in range(1, 20000): cur.left = TreeNode(i); cur = cur.left
vals, it = morris(chain)
print('left chain of 20000 nodes: first values', vals[:3], ', loop iterations =', it, '(n + L = 20000 + 19999)')
assert it == 39999 and vals == list(range(19999, -1, -1))
