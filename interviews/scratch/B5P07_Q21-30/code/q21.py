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

class ListNode:
    __slots__ = ("val", "next")
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def build_list(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v); tail = tail.next
    return dummy.next

def list_vals(head):
    out = []
    while head:
        out.append(head.val); head = head.next
        assert len(out) < 10**6
    return out

# ---------- array: root of [lo, hi] is index (lo + hi) // 2 ----------
def sorted_array_to_bst(nums):
    def go(lo, hi):
        if lo > hi: return None
        mid = (lo + hi) // 2
        return TreeNode(nums[mid], go(lo, mid - 1), go(mid + 1, hi))
    return go(0, len(nums) - 1)

# ---------- list, way 1: slow/fast to find the (lower) middle every time, O(n log n) ----------
STEPS = [0]
def list_to_bst_midpoint(head):
    def go(start, end):                      # half-open segment [start, end); end is a node or None
        if start is end: return None
        slow = fast = start
        while fast.next is not end and fast.next.next is not end:   # stops on the LOWER middle
            slow = slow.next; fast = fast.next.next; STEPS[0] += 1
        return TreeNode(slow.val, go(start, slow), go(slow.next, end))
    return go(head, None)

# ---------- list, way 2: simulate inorder, each list node consumed once, O(n) ----------
def list_to_bst_inorder(head):
    n, p = 0, head
    while p: n += 1; p = p.next
    cur = [head]
    def go(lo, hi):                          # builds indexes lo..hi; the lower middle is (lo + hi) // 2
        if lo > hi: return None
        mid = (lo + hi) // 2
        left = go(lo, mid - 1)               # left subtree consumes list nodes lo..mid-1
        node = TreeNode(cur[0].val)          # now cur is exactly list node mid
        cur[0] = cur[0].next
        node.left = left
        node.right = go(mid + 1, hi)
        return node
    return go(0, n - 1)

# ---------- checks ----------
def is_bst_balanced(root):
    vals = []
    def go(n):                               # returns height; depth is ~log n here so recursion is fine
        if n is None: return 0
        hl = go(n.left); vals.append(n.val); hr = go(n.right)
        assert abs(hl - hr) <= 1, "height-unbalanced"
        return 1 + max(hl, hr)
    go(root)
    assert vals == sorted(vals) and len(set(vals)) == len(vals)
    return vals

for arr, exp in [([-10, -3, 0, 5, 9], [0, -10, 5, None, -3, None, 9]), ([1, 3], [1, None, 3]), ([1], [1]), ([], [])]:
    a = to_arr(sorted_array_to_bst(arr))
    b = to_arr(list_to_bst_midpoint(build_list(arr)))
    c = to_arr(list_to_bst_inorder(build_list(arr)))
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, "->", a)

# exhaustive over every length 0..70 plus random distinct sorted arrays; all three agree and are valid
for n in range(0, 71):
    arr = list(range(n))
    t1 = sorted_array_to_bst(arr)
    assert is_bst_balanced(t1) == arr
    h = build_list(arr)
    t2, t3 = list_to_bst_midpoint(h), list_to_bst_inorder(h)
    assert same_shape(t1, t2) and same_shape(t1, t3)
    assert list_vals(h) == arr                           # input list untouched
random.seed(21)
for _ in range(300):
    arr = sorted(random.sample(range(-500, 500), random.randint(0, 60)))
    t1 = sorted_array_to_bst(arr)
    assert same_shape(t1, list_to_bst_midpoint(build_list(arr))) and same_shape(t1, list_to_bst_inorder(build_list(arr)))
print("cross-check ok: lengths 0..70 and 300 random sorted arrays, three builders give the same tree")

# the work of the 'find the middle every time' version: ~ (n/2) pointer steps per level, log n levels
for n in (1023, 10000):
    STEPS[0] = 0
    list_to_bst_midpoint(build_list(range(n)))
    print("n =", n, "-> slow/fast pointer steps =", STEPS[0], "(sandbox count; the inorder version touches each node once)")
assert sorted_array_to_bst(list(range(10**4))) is not None   # n = 10^4: depth ~14, no recursion problem
