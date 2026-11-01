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
NOT_WATCHED, CAMERA, WATCHED = 0, 1, 2

# ---- optimal greedy, recursive form (clear, fine up to depth ~900 under the default limit)
def cameras_rec(root):
    count = 0
    def go(n):
        nonlocal count
        if n is None: return WATCHED                      # an empty child never needs a camera
        a, b = go(n.left), go(n.right)
        if a == NOT_WATCHED or b == NOT_WATCHED: count += 1; return CAMERA
        if a == CAMERA or b == CAMERA: return WATCHED
        return NOT_WATCHED
    if go(root) == NOT_WATCHED: count += 1                # an unwatched root needs its own camera
    return count

# ---- same rule with an explicit post-order stack (safe for any depth)
def cameras(root):
    if root is None: return 0
    state, count, st = {}, 0, [(root, 0)]
    while st:
        n, s = st.pop()
        if s == 0:
            st.append((n, 1))
            for c in (n.left, n.right):
                if c: st.append((c, 0))
        else:
            a = state.get(id(n.left), WATCHED) if n.left else WATCHED
            b = state.get(id(n.right), WATCHED) if n.right else WATCHED
            if a == NOT_WATCHED or b == NOT_WATCHED: count += 1; state[id(n)] = CAMERA
            elif a == CAMERA or b == CAMERA: state[id(n)] = WATCHED
            else: state[id(n)] = NOT_WATCHED
    if state[id(root)] == NOT_WATCHED: count += 1
    return count

# ---- brute force: smallest subset of nodes that watches everyone (a camera watches itself, its parent, its children)
def watchers(root):
    """for each node (in a list), the set of node indexes whose camera would watch it; plus is_leaf flags"""
    nodes, st = [], [root] if root else []
    while st:
        n = st.pop(); nodes.append(n); st += [c for c in (n.left, n.right) if c]
    idx = {id(n): i for i, n in enumerate(nodes)}
    w = [{i} for i in range(len(nodes))]
    for i, n in enumerate(nodes):
        for c in (n.left, n.right):
            if c: w[i].add(idx[id(c)]); w[idx[id(c)]].add(i)
    leaf = [n.left is None and n.right is None for n in nodes]
    return w, leaf

def optimal_sets(root):
    w, leaf = watchers(root)
    for k in range(len(w) + 1):
        good = [c for c in itertools.combinations(range(len(w)), k) if all(w[i] & set(c) for i in range(len(w)))]
        if good: return k, good, leaf
def brute(root): return optimal_sets(root)[0] if root else 0

# ---- examples from the question
N = None
ex = [([0, 0, N, 0, 0], 1), ([0, 0, N, 0, N, 0, N, N, 0], 2), ([0], 1), ([0, 0, 0], 1), ([], 0)]
for arr, want in ex:
    r = build_tree(arr)
    assert cameras(r) == cameras_rec(r) == brute(r) == want, arr
print('examples ok:', [w for _, w in ex])

# ---- exhaustive: every shape with 0..9 nodes
count, no_leaf = 0, 0
for n in range(10):
    for sh in shapes(n):
        r = from_tup(label(sh, 'pre'))
        g = cameras(r)
        assert g == cameras_rec(r) == brute(r), tup(r)
        if n >= 2:                                        # some optimal placement avoids every leaf (parent watches a superset)
            k, good, leaf = optimal_sets(r)
            assert any(not any(leaf[i] for i in c) for c in good)
            no_leaf += 1
        count += 1
print('shapes checked exhaustively (0..9 nodes):', count)
print('trees with n >= 2 where an optimal placement with no camera on a leaf exists:', no_leaf, '(all of them)')
print('[0,0,0]: a camera on each leaf needs 2, the greedy needs', cameras(build_tree([0, 0, 0])), '(the root watches all three)')

# ---- the root-unwatched case
single = build_tree([0]); chain3 = build_tree([0, 0, N, 0])
print('single node: greedy count =', cameras(single), '(the final root fix adds the camera)')
print('chain of 3: greedy count =', cameras(chain3), '(camera on the middle node)')
assert cameras(single) == 1 and cameras(chain3) == 1

# ---- seeded random trees up to 14 nodes against brute force
random.seed(50)
for _ in range(300):
    nodes = [TreeNode(0)]
    for v in range(1, random.randint(1, 14)):
        p = random.choice(nodes); side = 'left' if random.random() < .5 else 'right'
        if getattr(p, side) is None:
            c = TreeNode(v); setattr(p, side, c); nodes.append(c)
    assert cameras(nodes[0]) == brute(nodes[0])
print('300 random trees (up to 14 nodes) ok')

# ---- depth: a chain of 1000 nodes (the allowed maximum)
root = TreeNode(0); cur = root
for i in range(1, 1000): cur.left = TreeNode(0); cur = cur.left
print('chain of 1000 nodes: iterative =', cameras(root))
assert cameras(root) == 334                           # ceil(n/3)
try: print('recursive =', cameras_rec(root))
except RecursionError: print('recursive version: RecursionError (default limit 1000)')
print('chain sizes 1..12 -> cameras:', [cameras(build_tree([0] + [0, N] * (k - 1))) for k in range(1, 13)], '(= ceil(k/3))')
assert all(cameras(build_tree([0] + [0, N] * (k - 1))) == -(-k // 3) for k in range(1, 40))
