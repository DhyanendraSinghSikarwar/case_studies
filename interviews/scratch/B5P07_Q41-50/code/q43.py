import random
random.seed(43)

def max_width(root):
    if root is None: return 0
    best, level = 0, [(root, 0)]
    while level:
        base = level[0][1]
        best = max(best, level[-1][1] - base + 1)       # leftmost to rightmost, gaps included
        nxt = []
        for node, i in level:
            i -= base                                   # re-base BEFORE doubling: indexes stay small
            if node.left: nxt.append((node.left, 2 * i))
            if node.right: nxt.append((node.right, 2 * i + 1))
        level = nxt
    return best

def max_width_no_rebase(root):                          # same idea, raw heap indexes (kept to show the cost)
    if root is None: return 0, 0
    best, big, level = 0, 0, [(root, 1)]
    while level:
        best = max(best, level[-1][1] - level[0][1] + 1)
        big = max(big, level[-1][1].bit_length())
        level = [(c, 2 * i + k) for n, i in level for k, c in ((0, n.left), (1, n.right)) if c]
    return best, big

def max_count(root):                                    # the easier, different question: most nodes on one level
    if root is None: return 0
    best, level = 0, [root]
    while level:
        best = max(best, len(level)); level = [c for n in level for c in (n.left, n.right) if c]
    return best

# ---- brute force on nested tuples: absolute heap positions, grouped by depth
def brute(t):
    pos = {}
    def go(t, d, idx):
        if t is None: return
        pos.setdefault(d, []).append(idx); go(t[1], d + 1, 2 * idx); go(t[2], d + 1, 2 * idx + 1)
    go(t, 0, 1)
    return max((max(v) - min(v) + 1 for v in pos.values()), default=0)

# ---- helpers
class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
def build_tree(arr):
    from collections import deque
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root
def from_tup(t): return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def shapes(n, _c={0: [None]}):
    if n not in _c: _c[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _c[n]

# ---- examples from the question
N = None
cases = [([1, 3, 2, 5, 3, N, 9], 4), ([1, 3, 2, 5], 2), ([1, 3, N, 5, 3], 2), ([1, 2, 3, 4, N, N, 5], 4), ([1], 1), ([], 0)]
for arr, want in cases:
    assert max_width(build_tree(arr)) == want, arr
print('examples ok:', [w for _, w in cases])

# ---- exhaustive over every shape with 0..8 nodes
count = 0
for n in range(9):
    for sh in shapes(n):
        def addv(s):
            return None if s is None else (0, addv(s[0]), addv(s[1]))
        tv = addv(sh); r = from_tup(tv)
        assert max_width(r) == brute(tv) == max_width_no_rebase(r)[0], tv
        count += 1
print('shapes checked exhaustively (0..8 nodes):', count)

# ---- seeded random trees up to 60 nodes, level-order arrays with holes
for _ in range(300):
    n = random.randint(1, 60); root = TreeNode(0); nodes = [root]
    for v in range(1, n):
        p = random.choice(nodes)
        side = random.random() < .5
        if getattr(p, 'left' if side else 'right') is None:
            c = TreeNode(v); setattr(p, 'left' if side else 'right', c); nodes.append(c)
    def tupr(x): return None if x is None else (x.val, tupr(x.left), tupr(x.right))
    assert max_width(root) == brute(tupr(root))
print('300 random trees ok')

# ---- width is NOT the same as the largest level
wide = build_tree([1, 2, 3, 4, N, N, 5])
print('[1,2,3,4,null,null,5]: width =', max_width(wide), ' largest level count =', max_count(wide))
assert (max_width(wide), max_count(wide)) == (4, 2)

# ---- deep skewed trees: a zig-zag chain of 3000 nodes (left, right, left, ...)
root = TreeNode(0); cur = root
for i in range(1, 3000):
    nxt = TreeNode(i)
    if i % 2: cur.left = nxt
    else: cur.right = nxt
    cur = nxt
w, bits = max_width_no_rebase(root)
print('zig-zag chain, 3000 nodes: width =', max_width(root), '; without re-basing the biggest index has', bits, 'bits')
assert max_width(root) == 1 and bits == 3000   # raw heap index doubles at every level
# right-only chain: raw index grows like 2^depth, re-based index stays at 0 or 1
chain = TreeNode(0); cur = chain
for i in range(1, 3000):
    cur.right = TreeNode(i); cur = cur.right
print('right chain, 3000 nodes: width =', max_width(chain), '; raw-index bits =', max_width_no_rebase(chain)[1])
assert max_width(chain) == 1
