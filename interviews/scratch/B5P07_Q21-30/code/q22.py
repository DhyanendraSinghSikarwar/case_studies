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

def range_sum_full(root, low, high):
    """Brute force: visit every node."""
    return sum(n.val for n in nodes_of(root) if low <= n.val <= high)

VISITED = [0]
def range_sum_rec(root, low, high):
    """Prune with the BST order. Recursion depth = height (can be 2*10^4 on a skewed tree: see iterative)."""
    if root is None: return 0
    VISITED[0] += 1
    total = root.val if low <= root.val <= high else 0
    if root.val > low:  total += range_sum_rec(root.left, low, high)    # left values < root.val; useful only if root.val > low
    if root.val < high: total += range_sum_rec(root.right, low, high)   # right values > root.val; useful only if root.val < high
    return total

def range_sum_iter(root, low, high):
    total, visited, st = 0, 0, [root] if root else []
    while st:
        n = st.pop(); visited += 1
        if low <= n.val <= high: total += n.val
        if n.val > low and n.left:  st.append(n.left)
        if n.val < high and n.right: st.append(n.right)
    return total, visited

for arr, lo, hi, exp in [([10, 5, 15, 3, 7, None, 18], 7, 15, 32), ([10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10, 23),
                         ([10], 11, 20, 0), ([10, 5, 15], 5, 5, 5)]:
    r = build_tree(arr)
    VISITED[0] = 0
    a, b, c = range_sum_rec(r, lo, hi), range_sum_iter(r, lo, hi)[0], range_sum_full(r, lo, hi)
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, lo, hi, "->", a, "| visited", VISITED[0], "of", len(nodes_of(r)))

# exhaustive: every BST shape up to 7 nodes (values 0..n-1 in inorder), every low <= high in a slightly wider range.
# Also test the visit-count claim: visited <= (nodes inside [low, high]) + 2 * height.
cases = worst_extra = 0
for n in range(1, 8):
    for s in shapes(n):
        r = from_tup(label_inorder(s)); h = height(r)
        for low in range(-1, n + 1):
            for high in range(low, n + 1):
                VISITED[0] = 0
                a = range_sum_rec(r, low, high); b, vis = range_sum_iter(r, low, high)
                assert a == b == range_sum_full(r, low, high) and VISITED[0] == vis
                inside = sum(1 for v in range(n) if low <= v <= high)
                assert vis <= inside + 2 * h, (s, low, high)
                worst_extra = max(worst_extra, vis - inside); cases += 1
print("exhaustive ok:", cases, "(tree, low, high) cases; largest visited-minus-inside =", worst_extra)

# random big-ish BSTs (random insertion order) vs brute force
def insert(root, v):
    if root is None: return TreeNode(v)
    cur = root
    while True:
        if v < cur.val:
            if cur.left is None: cur.left = TreeNode(v); break
            cur = cur.left
        else:
            if cur.right is None: cur.right = TreeNode(v); break
            cur = cur.right
    return root
random.seed(22)
for _ in range(300):
    vals = random.sample(range(-100, 100), random.randint(1, 60)); r = None
    for v in vals: r = insert(r, v)
    lo = random.randint(-110, 110); hi = random.randint(lo, 110)
    assert range_sum_rec(r, lo, hi) == range_sum_iter(r, lo, hi)[0] == range_sum_full(r, lo, hi) == sum(v for v in vals if lo <= v <= hi)
print("random cross-check ok (300 trees)")

# deep skewed tree, n = 2*10^4: recursion fails under the default limit, the iterative one is fine
chain = None
for v in range(20000, 0, -1): chain = TreeNode(v, None, chain)      # right chain 1..20000 (a valid BST)
try:
    range_sum_rec(chain, 5, 20000); print("recursive: no error")
except RecursionError:
    print("recursive on a 20000-node chain: RecursionError (default limit 1000)")
print("iterative on the same chain (sum, visited):", range_sum_iter(chain, 5, 20000))
assert range_sum_iter(chain, 5, 20000)[0] == sum(range(5, 20001))
print("pruned query [5, 10] on the chain visits", range_sum_iter(chain, 5, 10)[1], "nodes (the right spine stops once val >= high)")
