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

# ---- optimal: each subtree returns (best if its root is taken, best if its root is not taken)
def rob(root):
    def go(n):
        if n is None: return (0, 0)
        a, b = go(n.left), go(n.right)
        return (n.val + a[1] + b[1], max(a) + max(b))
    return max(go(root))

# ---- same thing with an explicit post-order stack: safe for n = 10^4 skewed
def rob_iter(root):
    if root is None: return 0
    res, st = {}, [(root, 0)]
    while st:
        n, s = st.pop()
        if s == 0: st += [(n, 1)] + [(c, 0) for c in (n.left, n.right) if c]
        else:
            a, b = res.pop(id(n.left), (0, 0)), res.pop(id(n.right), (0, 0))
            res[id(n)] = (n.val + a[1] + b[1], max(a) + max(b))
    return max(res[id(root)])

# ---- brute force: try every subset of nodes with no parent-child pair
def brute(root):
    nodes, par = [], {}
    st = [root] if root else []
    while st:
        n = st.pop(); nodes.append(n)
        for c in (n.left, n.right):
            if c: par[id(c)] = n; st.append(c)
    best = 0
    for mask in range(1 << len(nodes)):
        chosen = {id(nodes[i]) for i in range(len(nodes)) if mask >> i & 1}
        if any(par.get(i) is not None and id(par[i]) in chosen for i in chosen): continue
        best = max(best, sum(nodes[i].val for i in range(len(nodes)) if mask >> i & 1))
    return best

# ---- the tempting but wrong greedy: take the better of "all even levels" and "all odd levels"
def level_parity(root):
    if root is None: return 0
    sums, level = [0, 0], [root]; d = 0
    while level:
        sums[d % 2] += sum(n.val for n in level); level = [c for n in level for c in (n.left, n.right) if c]; d += 1
    return max(sums)

def naive_run(root):                                  # the real recursion, counting its calls
    calls = [0]
    def go(n):
        calls[0] += 1
        if n is None: return 0
        take = n.val
        for c in (n.left, n.right):
            if c: take += go(c.left) + go(c.right)
        return max(take, go(n.left) + go(n.right))
    return go(root), calls[0]

# ---- examples from the question
N = None
ex = [([3, 2, 3, N, 3, N, 1], 7), ([3, 4, 5, 1, 3, N, 1], 9), ([], 0), ([2, 1, 3, N, 4], 7)]
for arr, want in ex:
    r = build_tree(arr)
    assert rob(r) == rob_iter(r) == brute(r) == want, arr
print('examples ok:', [w for _, w in ex])

# ---- exhaustive over every shape up to 7 nodes, with seeded random non-negative values
random.seed(45)
count = fails = 0
for n in range(8):
    for sh in shapes(n):
        for _ in range(3):
            def addv(s): return None if s is None else (random.randint(0, 9), addv(s[0]), addv(s[1]))
            r = from_tup(addv(sh))
            b = brute(r)
            assert rob(r) == rob_iter(r) == b
            if level_parity(r) != b: fails += 1
            count += 1
print('trees checked:', count, '| the level-parity greedy was wrong on', fails, 'of them')
assert level_parity(build_tree([2, 1, 3, N, 4])) == 6 and rob(build_tree([2, 1, 3, N, 4])) == 7
print('counter-example [2,1,3,null,4]: parity greedy =', level_parity(build_tree([2, 1, 3, N, 4])), ', true answer = 7 (take 3 and 4)')

# ---- zero values and single node
assert rob(build_tree([0, 0, 0])) == 0 and rob(build_tree([5])) == 5

def perfect(h): return from_tup(label_perfect(h))
def label_perfect(h): return None if h < 0 else (1, label_perfect(h - 1), label_perfect(h - 1))
for h in range(0, 8):
    v, calls = naive_run(perfect(h)); assert v == rob(perfect(h))
print('naive calls, perfect tree heights 0..7 (None children counted):', [naive_run(perfect(h))[1] for h in range(8)])
# ---- cost: pair version visits each node once; the naive 'grandchildren' recursion without memo blows up
print('nodes in those trees:', [2 ** (h + 1) - 1 for h in range(8)], '(the pair version makes one call per node plus one per missing child)')

# ---- deep input: skewed chain of 10^4 nodes
root = TreeNode(1); cur = root
for i in range(2, 10001):
    cur.left = TreeNode(1); cur = cur.left
print('chain of 10000 nodes, all values 1: iterative answer =', rob_iter(root))
assert rob_iter(root) == 5000
try: rob(root); print('recursive version survived')
except RecursionError: print('recursive version: RecursionError at depth 10000 (default limit 1000)')
