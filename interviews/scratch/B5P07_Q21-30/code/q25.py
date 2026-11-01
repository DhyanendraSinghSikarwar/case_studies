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

def zigzag(root):
    """BFS; the queue is ALWAYS filled left to right; only the output of each level is reversed or not."""
    if root is None: return []
    out, q, left_to_right = [], deque([root]), True
    while q:
        level = deque()
        for _ in range(len(q)):                     # snapshot: exactly one level
            n = q.popleft()
            if left_to_right: level.append(n.val)   # fill the output from alternating ends
            else:             level.appendleft(n.val)
            if n.left:  q.append(n.left)            # children always left then right
            if n.right: q.append(n.right)
        out.append(list(level)); left_to_right = not left_to_right
    return out

def zigzag_reverse_levels(root):
    """Alternative: normal level order, then reverse every odd level."""
    out, level = [], [root] if root else []
    while level:
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]
    return [l[::-1] if i % 2 else l for i, l in enumerate(out)]

def zigzag_wrong(root):
    """BUG: reverse the queue itself on odd levels. The children then enter in the wrong order for the next level."""
    if root is None: return []
    out, level, flip = [], [root], False
    while level:
        if flip: level = level[::-1]               # reversing the nodes ...
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]   # ... changes who is enqueued first
        flip = not flip
    return out

def zig_tuple(t):
    """Independent brute force on tuple trees: collect (depth, left-to-right index) then regroup."""
    levels = {}
    def go(t, d):
        if t is None: return
        levels.setdefault(d, []).append(t[0]); go(t[1], d + 1); go(t[2], d + 1)   # preorder keeps left-to-right order per level
    go(t, 0)
    return [levels[d][::-1] if d % 2 else levels[d] for d in sorted(levels)]

for arr, exp in [([3, 9, 20, None, None, 15, 7], [[3], [20, 9], [15, 7]]), ([1, 2, 3, 4, None, None, 5], [[1], [3, 2], [4, 5]]),
                 ([1], [[1]]), ([], [])]:
    r = build_tree(arr); got = zigzag(r)
    assert got == zigzag_reverse_levels(r) == exp, (arr, got)
    print(arr, "->", got)
print("reversing the queue (bug) on [1,2,3,4,None,None,5]:", zigzag_wrong(build_tree([1, 2, 3, 4, None, None, 5])))

# exhaustive: all shapes with 0..8 nodes (values 0..n-1 by inorder, distinct), compare three solutions + brute force
cnt = bad = 0
for n in range(0, 9):
    for s in shapes(n):
        t = label_inorder(s); r = from_tup(t)
        assert zigzag(r) == zigzag_reverse_levels(r) == zig_tuple(t)
        if zigzag_wrong(r) != zigzag(r): bad += 1
        cnt += 1
print("exhaustive ok on", cnt, "shapes; the 'reverse the queue' bug is wrong on", bad, "of them")
random.seed(25)
for _ in range(200):
    n = random.randint(0, 60); arr = [random.choice([None, random.randint(0, 9)]) for _ in range(n)]
    if arr: arr[0] = 1
    r = build_tree(arr); assert zigzag(r) == zigzag_reverse_levels(r)
print("random cross-check ok (200 arrays)")
big = build_tree([1] * 2000)    # a bushy tree with 2000 nodes
assert sum(len(l) for l in zigzag(big)) == 2000
print("n = 2000 bushy tree: levels =", len(zigzag(big)))
