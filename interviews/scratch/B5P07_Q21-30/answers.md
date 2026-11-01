### Q21 ⭐⭐ 🟢 Sorted array and sorted list to a height-balanced BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a sorted array of distinct integers (0 <= n <= 10^4), build a BST whose subtree heights differ by at most 1 at every node, using this rule so the answer is unique: the root of a range is the element at index (lo + hi) // 2 (the lower middle for an even count). Return the tree. Then do the same for a SORTED SINGLY LINKED LIST (nodes `ListNode(val, next)`; the middle of a list is Part 6 Q2) and give two ways: find the middle with slow and fast pointers each time, and simulate inorder so each list node is consumed once in O(n). Both must give the same tree as the array rule. Example: nums=[-10, -3, 0, 5, 9] -> [0, -10, 5, null, -3, null, 9]; nums=[1, 3] -> [1, null, 3]; nums=[1] -> [1]; nums=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Divide and conquer on a sorted range. The middle element is the root, so both subtrees get half the elements and the heights differ by at most 1. For the list, the same tree falls out of an inorder simulation.

**Say this first (1 line):** "Root is the element at (lo + hi) // 2, recurse on both halves; for a list I count n once and build inorder so each list node is consumed exactly once."

**Brute force:** For the list, copy it into an array first (O(n) extra space) and reuse the array builder. Or find the middle with slow and fast pointers at every call. Each call costs the length of its segment, so one level costs about n/2 pointer steps and there are log n levels: O(n log n) time, O(log n) stack, no extra copy.

**Optimal:**
- Array: `go(lo, hi)` makes the node for `nums[(lo + hi) // 2]`, then `go(lo, mid - 1)` and `go(mid + 1, hi)`. O(n) time, O(log n) stack. The depth is about 14 at n = 10^4, so recursion is safe here.
- List, inorder simulation: count n, keep one cursor on the list. `go(lo, hi)` first builds the left subtree (it eats list nodes lo..mid-1), then the cursor sits exactly on list node `mid`, take its value and step the cursor, then build the right subtree. The tree is built bottom-up and the list is read once, in order. O(n) time, O(log n) stack.
- The lower-middle rule is the same `(lo + hi) // 2` in both, so the trees match.
- Why balanced: the two halves differ in size by at most 1, so by induction their heights differ by at most 1.

**Complexity:** Array: T(n) = 2T(n/2) + O(1) = O(n). List with repeated middle search: T(n) = 2T(n/2) + O(n) = O(n log n). List by inorder simulation: O(n). Stack depth O(log n) in all of them.

**Dry run:** `[-10, -3, 0, 5, 9]`. `go(0, 4)`: mid = 2, root 0. Left `go(0, 1)`: mid = 0, node -10, its right is `go(1, 1)` = -3. Right `go(3, 4)`: mid = 3, node 5, its right is `go(4, 4)` = 9. Level order: `[0, -10, 5, null, -3, null, 9]`. For the list, the cursor visits -10, -3, 0, 5, 9 in that order, so -10 is built first, then -3, then the root 0.

**Code:**
```python
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
```

**Output (my run):**
```
[-10, -3, 0, 5, 9] -> [0, -10, 5, None, -3, None, 9]
[1, 3] -> [1, None, 3]
[1] -> [1]
[] -> []
cross-check ok: lengths 0..70 and 300 random sorted arrays, three builders give the same tree
n = 1023 -> slow/fast pointer steps = 4097 (sandbox count; the inorder version touches each node once)
n = 10000 -> slow/fast pointer steps = 54613 (sandbox count; the inorder version touches each node once)
```

**Edge cases:**
- Empty array or list: return None (checked: the counting loop gives n = 0 and `go(0, -1)` returns None).
- One element: a single node.
- Even length: the LOWER middle is the root, so `[1, 3]` gives root 1 with right child 3. The other choice (upper middle) is a different valid tree, which is why the prompt fixes the rule.
- The list must stay untouched; the inorder version only reads it.

**Follow-ups:**
- Same for a sorted list but you may not count it first? Use a first pass to count (O(n)), or recurse on sizes. Counting is the standard trick.
- Does the slow/fast version find the lower middle? Only with the stop test `fast.next.next is not end`; the textbook `while fast and fast.next` gives the upper middle on even lengths and builds a different (still balanced) tree.
- Is the result complete (every level full except the last)? Not necessarily; the rule only guarantees height balance.

**Common mistakes:**
- Using `lo + hi // 2` (precedence) or the upper middle and getting a different tree from the expected one.
- Cutting the list (`prev.next = None`) in the midpoint version and destroying the input.
- Forgetting that the cursor must advance after the left subtree is built, not before.
- Using `len(nums) // 2` on slices: slicing copies and makes the array version O(n log n).

### Q22 ⭐⭐ 🟢 Range sum of a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is a BST with distinct values (1 <= n <= 2*10^4). Return the sum of all values v with low <= v <= high. Use the BST order to skip whole subtrees (do not visit the left subtree when the node's value is <= low, and the right when it is >= high) and say what that saves compared with summing all n nodes with a full traversal. Write it recursively and iteratively. Example: root=[10, 5, 15, 3, 7, null, 18], low=7, high=15 -> 32; root=[10, 5, 15, 3, 7, 13, 18, 1, null, 6], low=6, high=10 -> 23; root=[10], low=11, high=20 -> 0; root=[10, 5, 15], low=5, high=5 -> 5.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST order lets you discard whole subtrees. A plain traversal ignores that order.

**Say this first (1 line):** "At each node, add it if it is in range, go left only if the node is above low, go right only if it is below high; I visit the in-range nodes plus two boundary paths."

**Brute force:** Traverse all n nodes and add values in range. O(n) time, O(h) stack.

**Optimal:**
- If `node.val <= low`, everything in the left subtree is smaller than `node.val`, so strictly below low: skip it. If `node.val >= high`, skip the right subtree the same way.
- Otherwise visit both sides. A node with `low < val < high` is always inside and both children matter.
- Saving: the visited nodes are the in-range ones (k of them) plus the nodes on the paths that bound the range, at most 2h. So O(k + h) instead of O(n). My exhaustive run (every BST shape up to 7 nodes, every low and high) never exceeded k + 2h.
- The worst case is still O(n): when the range covers everything, k = n.

**Complexity:** Time O(k + h) where k is the count of in-range nodes, worst case O(n). Space O(h) for the recursion or the explicit stack. On a skewed tree h = n.

**Dry run:** Root `[10, 5, 15, 3, 7, null, 18]`, low = 7, high = 15. Visit 10: in range, add 10; 10 > 7 so go left, 10 < 15 so go right. Visit 5: not in range; 5 <= 7 so skip its left; 5 < 15 so go right. Visit 7: add 7; 7 <= 7 so skip left; 7 < 15 go right (None). Visit 15: add 15; 15 > 7 go left (None); 15 >= 15 skip right. Sum = 10 + 7 + 15 = 32. Visited 4 of 6 nodes (3 and 18 were skipped).

**Code:**
```python
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
```

**Output (my run):**
```
[10, 5, 15, 3, 7, None, 18] 7 15 -> 32 | visited 4 of 6
[10, 5, 15, 3, 7, 13, 18, 1, None, 6] 6 10 -> 23 | visited 4 of 9
[10] 11 20 -> 0 | visited 1 of 1
[10, 5, 15] 5 5 -> 5 | visited 2 of 3
exhaustive ok: 25628 (tree, low, high) cases; largest visited-minus-inside = 7
random cross-check ok (300 trees)
recursive on a 20000-node chain: RecursionError (default limit 1000)
iterative on the same chain (sum, visited): (200009990, 20000)
pruned query [5, 10] on the chain visits 10 nodes (the right spine stops once val >= high)
```

**Edge cases:**
- low == high: the answer is that value if present, and the walk is just the search path.
- Range outside the tree: you still walk one boundary path, and the sum is 0.
- Range covers all values: all n nodes are visited; no saving.
- Skewed tree: the recursion depth is n. At n = 2 * 10^4 the recursive version raised RecursionError in my run with the default limit, so for this size prefer the iterative one.
- Values in the prompt are distinct; with duplicates the "skip left when val <= low" rule would be wrong.

**Follow-ups:**
- Count instead of sum? Same walk, add 1.
- Many queries? Store subtree sizes or sums per node (an order-statistic style augmentation) to answer in O(h).
- Why is `val <= low` safe and not `val < low`? Left values are strictly smaller than `val`, so at `val == low` they are all below low.

**Common mistakes:**
- Testing only `if val < low: go right` and `elif val > high: go left`, and forgetting that an in-range node needs both sides.
- Adding the node's value before checking the range.
- Recursing into both children and filtering later, which is the O(n) brute force in disguise.

### Q23 ⭐⭐ 🟢 Insert into a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a BST with distinct values (0 <= n <= 10^4) and a value `val` that is not already in it, insert `val` as a new LEAF at the position the search for it ends (so the result is unique) and return the root. Write the iterative version in O(h) time and O(1) space, handling the empty tree. Say what happens to the cost when you insert a sorted sequence one by one into an empty tree, and how many nodes that tree has on its longest path. Example: root=[4, 2, 7, 1, 3], val=5 -> [4, 2, 7, 1, 3, 5]; root=[], val=5 -> [5]; root=[40, 20, 60, 10, 30, 50, 70], val=25 -> [40, 20, 60, 10, 30, 50, 70, null, null, 25]; root=[1], val=0 -> [1, 0].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST search path. The new value goes where an unsuccessful search for it would end.

**Say this first (1 line):** "Walk down comparing with each node, left if smaller and right if larger, until the next child is empty; attach the new leaf there and return the original root."

**Brute force:** Flatten to a sorted list, insert, rebuild a tree from the sorted list. O(n) time and space, and it reshapes the tree, so the result is not the leaf insert the question asks for.

**Optimal:**
- Empty tree: the new node is the root.
- Otherwise `cur = root`. If `val < cur.val` and `cur.left` is empty, attach there, else step left. Mirror for the right.
- Only one pointer is written, so every old node keeps its identity and the root object is returned unchanged (checked by node identity in the run: exactly one new node, and it is a leaf).
- Iterative, so O(1) extra space and no recursion limit.

**Complexity:** Time O(h), space O(1). h is about log n for a balanced tree and n for a chain.

**Sorted insertions:** Insert 0, 1, 2, ... one by one. Value k is bigger than everything, so it walks down the whole right chain of k nodes: k node visits. Total 0 + 1 + ... + (n-1) = n(n-1)/2 = O(n^2). The tree is a single right chain with n nodes on its longest path. The run confirmed this: n = 500 gives 124750 visits and a longest path of 500. A shuffled order of 2000 values gave height 23 in my run. Self-balancing trees (AVL, red-black) avoid the chain; Python has no built-in one.

**Dry run:** `[4, 2, 7, 1, 3]`, val = 5. At 4: 5 > 4, go right to 7. At 7: 5 < 7, left is empty, attach. Level order `[4, 2, 7, 1, 3, 5]`.

**Code:**
```python
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

def insert_iter(root, val):
    """Iterative leaf insert; O(h) time, O(1) extra space. Returns the root."""
    node = TreeNode(val)
    if root is None: return node
    cur = root
    while True:
        if val < cur.val:
            if cur.left is None: cur.left = node; return root
            cur = cur.left
        else:                       # val > cur.val (values are distinct and val is not in the tree)
            if cur.right is None: cur.right = node; return root
            cur = cur.right

def insert_tuple(t, val):
    """Independent brute force on tuple trees (recursive, rebuilds the path)."""
    if t is None: return (val, None, None)
    if val < t[0]: return (t[0], insert_tuple(t[1], val), t[2])
    return (t[0], t[1], insert_tuple(t[2], val))

for arr, v, exp in [([4, 2, 7, 1, 3], 5, [4, 2, 7, 1, 3, 5]), ([], 5, [5]),
                    ([40, 20, 60, 10, 30, 50, 70], 25, [40, 20, 60, 10, 30, 50, 70, None, None, 25]), ([1], 0, [1, 0])]:
    r = build_tree(arr); old = nodes_of(r); old_ids = {id(n) for n in old}
    out = insert_iter(r, v)
    assert to_arr(out) == exp, (arr, to_arr(out))
    new = [n for n in nodes_of(out) if id(n) not in old_ids]
    assert len(new) == 1 and new[0].val == v and new[0].left is None and new[0].right is None   # exactly one new LEAF
    if r is not None: assert out is r                                                             # same root object
    print(arr, "insert", v, "->", to_arr(out))

# exhaustive: every BST shape up to 6 nodes (values 0, 2, 4, ...), insert every odd gap value and the two ends
cases = 0
for n in range(0, 7):
    for s in shapes(n):
        t = label_inorder(s)
        def scale(x): return None if x is None else (2 * x[0], scale(x[1]), scale(x[2]))
        t = scale(t)
        for v in range(-1, 2 * n, 2):
            r = from_tup(t); old_ids = {id(x) for x in nodes_of(r)}
            out = insert_iter(r, v)
            assert tup(out) == insert_tuple(t, v)
            assert len([x for x in nodes_of(out) if id(x) not in old_ids]) == 1
            if r: assert out is r
            cases += 1
print("exhaustive ok:", cases, "(shape, value) cases")

# sorted insertion: node k (0-based) is placed after visiting k nodes, so total visits = n(n-1)/2 and the tree is one chain
def insert_counting(root, val):
    visits = 0
    node = TreeNode(val)
    if root is None: return node, 0
    cur = root
    while True:
        visits += 1
        if val < cur.val:
            if cur.left is None: cur.left = node; return root, visits
            cur = cur.left
        else:
            if cur.right is None: cur.right = node; return root, visits
            cur = cur.right
for n in (1, 2, 10, 500):
    root, total = None, 0
    for v in range(n):
        root, c = insert_counting(root, v); total += c
    assert total == n * (n - 1) // 2 and height(root) == n
    print("n =", n, "sorted inserts: visits =", total, "= n(n-1)/2, longest path =", height(root), "nodes")

# a shuffled order gives a much shorter tree (sandbox number, one seed)
random.seed(23)
vals = list(range(2000)); random.shuffle(vals); root = None
for v in vals: root = insert_iter(root, v)
print("2000 shuffled inserts: height =", height(root), "(sorted order would give 2000)")
```

**Output (my run):**
```
[4, 2, 7, 1, 3] insert 5 -> [4, 2, 7, 1, 3, 5]
[] insert 5 -> [5]
[40, 20, 60, 10, 30, 50, 70] insert 25 -> [40, 20, 60, 10, 30, 50, 70, None, None, 25]
[1] insert 0 -> [1, 0]
exhaustive ok: 1275 (shape, value) cases
n = 1 sorted inserts: visits = 0 = n(n-1)/2, longest path = 1 nodes
n = 2 sorted inserts: visits = 1 = n(n-1)/2, longest path = 2 nodes
n = 10 sorted inserts: visits = 45 = n(n-1)/2, longest path = 10 nodes
n = 500 sorted inserts: visits = 124750 = n(n-1)/2, longest path = 500 nodes
2000 shuffled inserts: height = 23 (sorted order would give 2000)
```

**Edge cases:**
- Empty tree: return the new node.
- Value smaller than the minimum or larger than the maximum: leaf at the far left or right.
- The value is already present (excluded by the prompt): the code would put it on the right; decide the duplicate rule explicitly in a real interview.
- Skewed tree: O(n) per insert, and the iterative loop has no recursion problem.

**Follow-ups:**
- Recursive version? `if not root: return TreeNode(v)`, then `root.left = insert(root.left, v)`. Same O(h), but O(h) stack, and it rewrites pointers on the whole path.
- How do you keep it balanced? Rotations after the insert (AVL, red-black), or a treap with random priorities.
- Is the leaf-insert result unique? Yes. Any BST insertion that keeps old nodes in place must put the node at the end of the search path, so only one leaf position exists.

**Common mistakes:**
- Returning the new node instead of the root.
- Forgetting the empty tree.
- Walking with `cur = cur.left` without a stop condition and falling off the tree into None.
- Using `<=` and `>` in a way that silently inserts duplicates on one side.

### Q24 ⭐⭐ 🟢 Complexity of traversals: time O(n), space O(h) or O(n). Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Write a function that returns the tuple (visits, max_recursion_depth, max_stack, max_queue) for a tree: visits is the number of nodes visited by a full traversal; max_recursion_depth is the largest number of simultaneously active calls of a recursive inorder that is only ever called on non-null nodes; max_stack is the largest `len(stack)` of the iterative inorder `while stack or cur: while cur: stack.append(cur); cur = cur.left; cur = stack.pop(); visit(cur); cur = cur.right`; max_queue is the largest `len(queue)` of a level-order loop that starts with deque([root]), pops from the left and appends non-null children (measured after each append). Explain from the results why recursion and stack space is O(h) (h = height in nodes) while a queue needs O(w) for the widest level w, and which of the two is O(n) on a skewed tree and which on a perfect tree. Example: root=[1, 2, 3, 4, 5, 6, 7] -> (7, 3, 3, 4); root=[1, 2, null, 3, null, 4] -> (4, 4, 4, 1); root=[1, null, 2, null, 3, null, 4] -> (4, 4, 1, 1); root=[] -> (0, 0, 0, 0).
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Python recursion-limit explainers (techinterview.org depth-of-a-tree page, a OneUptime guide, DataCamp DFS tutorial; snippets only, not opened: default limit 1000, raising it risks a crash, explicit stack preferred)

**Pattern:** Measure space, not just time. Depth-first traversals hold a path (height); breadth-first holds a level (width).

**Say this first (1 line):** "Every traversal visits n nodes, so time is O(n); DFS space is the height h because it holds one root-to-node path, BFS space is the widest level w."

**Brute force:** Nothing to brute force. The measured version below is the instrument: run the three loops and record the peaks, and check them against the claims on every tree shape up to 8 nodes.

**Optimal (what the numbers say):**
- Recursion depth is exactly h in nodes (checked on 2056 shapes). The call for a node stays active until its whole subtree is done, so the active calls are one root-to-node path.
- The explicit inorder stack holds the left spine plus ancestors still waiting for a visit. It is never more than h. It is exactly h on a left chain and just 1 on a right chain, because a right child is not pushed until its parent has been popped.
- The queue holds the unfinished part of one level and the started part of the next. Its peak is at least the widest level w (checked) and at most n.
- Perfect tree with k levels (n = 2^k - 1): h = k, w = 2^(k-1), so DFS needs O(log n) and the queue needs about n/2: O(n).
- Skewed tree: h = n, w = 1, so recursion and a left-leaning stack are O(n) while the queue is O(1).

**Complexity:** Time O(n) for all three (each node is pushed once, popped once). Space: recursion and stack O(h), queue O(w). h ranges from log n to n, w from 1 to about n/2.

**Dry run:** `[1, 2, 3, 4, 5, 6, 7]` (perfect, 3 levels). Recursion: calls 1, 2, 4 are active at once, depth 3. Stack: push 1, 2, 4, size 3; pop 4, push nothing; pop 2, push 5 (size 2); and so on, peak 3. Queue: after popping 1 it holds 2, 3; after popping 2 it holds 3, 4, 5; after popping 3 it holds 4, 5, 6, 7, peak 4. Result `(7, 3, 3, 4)`.

**Code:**
```python
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

def metrics(root):
    """(visits, max_recursion_depth, max_stack, max_queue). Empty tree -> all zeros.
    max_queue counts the initial deque([root]) (length 1) too, so a single node gives 1."""
    if root is None: return (0, 0, 0, 0)
    # recursive inorder, only called on non-null nodes: count simultaneously active calls
    live = peak = visits = 0
    def rec(n):
        nonlocal live, peak, visits
        live += 1; peak = max(peak, live)
        if n.left: rec(n.left)
        visits += 1
        if n.right: rec(n.right)
        live -= 1
    rec(root)
    # iterative inorder, exactly the loop in the prompt
    stack, cur, mx_stack, v2 = [], root, 0, 0
    while stack or cur:
        while cur:
            stack.append(cur); mx_stack = max(mx_stack, len(stack)); cur = cur.left
        cur = stack.pop(); v2 += 1; cur = cur.right
    # level order with a deque
    q, mx_q, v3 = deque([root]), 1, 0
    while q:
        n = q.popleft(); v3 += 1
        for c in (n.left, n.right):
            if c is not None:
                q.append(c); mx_q = max(mx_q, len(q))
    assert visits == v2 == v3
    return (visits, peak, mx_stack, mx_q)

for arr, exp in [([1, 2, 3, 4, 5, 6, 7], (7, 3, 3, 4)), ([1, 2, None, 3, None, 4], (4, 4, 4, 1)),
                 ([1, None, 2, None, 3, None, 4], (4, 4, 1, 1)), ([], (0, 0, 0, 0))]:
    got = metrics(build_tree(arr)); assert got == exp, (arr, got); print(arr, "->", got)

def widest(root):
    best, level = 0, [root] if root else []
    while level:
        best = max(best, len(level)); level = [c for n in level for c in (n.left, n.right) if c]
    return best

# exhaustive over every shape with 0..8 nodes: recursion depth = h exactly, stack <= h, w <= queue <= n
cnt = 0
for n in range(0, 9):
    for s in shapes(n):
        r = from_tup(label_inorder(s)); v, rd, ms, mq = metrics(r); h, w = height(r), widest(r)
        assert v == n and rd == h and ms <= h and w <= mq <= n, (s, v, rd, ms, mq, h, w)
        if n: assert mq >= 1
        cnt += 1
print("exhaustive ok on", cnt, "tree shapes: visits = n, recursion depth = h, stack <= h, widest level <= queue <= n")

# the three shapes the question asks about, at n = 255 / 256 nodes (sandbox numbers)
def perfect(k):   # k levels
    return None if k == 0 else TreeNode(1, perfect(k - 1), perfect(k - 1))
def left_chain(n):
    r = None
    for _ in range(n): r = TreeNode(1, r, None)
    return r
def right_chain(n):
    r = None
    for _ in range(n): r = TreeNode(1, None, r)
    return r
print("perfect, 8 levels, n = 255:", metrics(perfect(8)), "(h = 8, widest level = 128)")
print("left chain, n = 200      :", metrics(left_chain(200)), "(h = 200, w = 1)")
print("right chain, n = 200     :", metrics(right_chain(200)), "(h = 200, w = 1)")
assert metrics(left_chain(200)) == (200, 200, 200, 1) and metrics(right_chain(200))[2:] == (1, 1)
# perfect tree: test the exact queue peak for k = 1..9
for k in range(1, 10):
    got = metrics(perfect(k))
    assert got[1] == got[2] == k and got[3] == max(1, 2 ** (k - 1)), (k, got)
print("perfect trees k = 1..9: queue peak = 2^(k-1) exactly, recursion = stack = k")
# Python limit: recursion of depth 1500 on a left chain fails by default; the explicit-stack loop does not
try:
    metrics(left_chain(1500)); print("no error")
except RecursionError:
    print("recursive inorder on a 1500-node chain: RecursionError")
```

**Output (my run):**
```
[1, 2, 3, 4, 5, 6, 7] -> (7, 3, 3, 4)
[1, 2, None, 3, None, 4] -> (4, 4, 4, 1)
[1, None, 2, None, 3, None, 4] -> (4, 4, 1, 1)
[] -> (0, 0, 0, 0)
exhaustive ok on 2056 tree shapes: visits = n, recursion depth = h, stack <= h, widest level <= queue <= n
perfect, 8 levels, n = 255: (255, 8, 8, 128) (h = 8, widest level = 128)
left chain, n = 200      : (200, 200, 200, 1) (h = 200, w = 1)
right chain, n = 200     : (200, 200, 1, 1) (h = 200, w = 1)
perfect trees k = 1..9: queue peak = 2^(k-1) exactly, recursion = stack = k
recursive inorder on a 1500-node chain: RecursionError
```

**Edge cases:**
- Empty tree: `(0, 0, 0, 0)`.
- Single node: the prompt says to measure the queue "after each append", which would give 0 here (no append happens). My function counts the initial `deque([root])` too, so a single node gives a queue peak of 1. Say which convention you use; it only matters for trees with no appended children.
- Python's default recursion limit is 1000: a 1500-node left chain raised RecursionError in the recursive inorder, while the explicit stack handled it (it only needs memory, not frames). The Part 4 Q25 answer covers this trade-off.
- Morris traversal gets O(1) extra space at the cost of temporarily changing pointers.

**Follow-ups:**
- Which is better on a wide shallow tree? DFS, since the stack is only h. On a deep thin tree BFS is better.
- Can iterative DFS beat O(h)? Morris traversal does O(1) extra by threading, at the cost of modifying the tree while it runs.
- Does the output count of a traversal (the result list) count as space? It is O(n) for storing it; "extra space" excludes it.

**Common mistakes:**
- Saying "recursion is O(1) space". The call stack is O(h).
- Calling the BFS queue O(h). It is O(w).
- Using n for recursion depth on a balanced tree, or log n on an unbalanced one.
- Forgetting that a right chain keeps the inorder stack at size 1.

### Q25 ⭐⭐ 🟡 Zigzag level-order traversal. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return the levels top to bottom, but the first level left to right, the second right to left, the third left to right, and so on (0 <= n <= 2000). Do a normal BFS and reverse alternate levels (or fill a deque from alternating ends) rather than reversing the queue, and explain why the queue itself must stay in left-to-right order. Example: root=[3, 9, 20, null, null, 15, 7] -> [[3], [20, 9], [15, 7]]; root=[1, 2, 3, 4, null, null, 5] -> [[1], [3, 2], [4, 5]]; root=[1] -> [[1]]; root=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BFS with a level snapshot (`for _ in range(len(q))`), then a per-level direction flag. Part 4 Q30 has the same queue idiom.

**Say this first (1 line):** "Normal BFS, children always enqueued left then right, and only the order I write each level into the output flips on odd levels."

**Brute force:** Do plain level order, then reverse every odd-numbered level in a second pass. O(n) time and space. It is perfectly good; it just takes two passes over the levels.

**Optimal:**
- Keep `left_to_right` as a flag. For each level pop `len(q)` nodes. If the flag is true, `append` the value to a deque for this level, otherwise `appendleft`. Convert it to a list when the level ends.
- Enqueue `left` then `right` for every node, whatever the direction.
- Why the queue must stay left to right: level d+1 in the queue must be ordered by the parents' order in level d. If you reverse the queue, the parents are processed in reversed order and their children are enqueued in the wrong order. Then the next level, which should be reversed again, comes out wrong. In my run the "reverse the queue" version gives `[[1], [3, 2], [5, 4]]` instead of `[[1], [3, 2], [4, 5]]` on the second example, and it was wrong on 573 of 2056 shapes.
- `appendleft` on a deque is O(1); `list.insert(0, x)` would be O(level width) each.

**Complexity:** Time O(n), space O(w) for the queue plus O(n) for the output.

**Dry run:** `[1, 2, 3, 4, null, null, 5]`. Level 0: pop 1, left to right, `[1]`; enqueue 2, 3. Level 1 (flag false): pop 2, `appendleft` gives `[2]`; enqueue 4; pop 3, `appendleft` gives `[3, 2]`; enqueue 5. Level 2 (flag true): pop 4, 5 giving `[4, 5]`. Result `[[1], [3, 2], [4, 5]]`.

**Code:**
```python
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
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> [[3], [20, 9], [15, 7]]
[1, 2, 3, 4, None, None, 5] -> [[1], [3, 2], [4, 5]]
[1] -> [[1]]
[] -> []
reversing the queue (bug) on [1,2,3,4,None,None,5]: [[1], [3, 2], [5, 4]]
exhaustive ok on 2056 shapes; the 'reverse the queue' bug is wrong on 573 of them
random cross-check ok (200 arrays)
n = 2000 bushy tree: levels = 11
```

**Edge cases:**
- Empty tree: return `[]` (guard before the loop).
- Single node: `[[1]]`.
- Skewed tree: every level has one node, so zigzag equals plain level order.
- Missing children in the middle of a level: handled, since only existing children are enqueued.

**Follow-ups:**
- Do it with two stacks? Possible (left then right into one stack, right then left into the other), but it is harder to read than the flag.
- Right-to-left only? Enqueue right then left, or reverse each level.
- DFS version? Pass the depth, append to `levels[depth]`, and reverse odd levels at the end.

**Common mistakes:**
- Flipping the queue direction instead of the output direction.
- Forgetting the level snapshot and mixing levels.
- Using `list.insert(0, ...)` and quietly making it O(n^2) on a wide level.
- Toggling the flag inside the node loop instead of once per level.

### Q26 ⭐⭐ 🟡 Path sum II: list the root-to-leaf paths. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Return every path from the ROOT to a LEAF whose values sum to `target`, as lists of values, ordered by the left-to-right order of their leaves (0 <= n <= 5000, values may be negative). Use backtracking on one shared `path` list (append, recurse, pop) and copy it only when a match is found; explain why storing the list without copying is a bug, and the cost of copying in terms of the number of matches and the path length. Example: root=[5, 4, 8, 11, null, 13, 4, 7, 2, null, null, 5, 1], target=22 -> [[5, 4, 11, 2], [5, 8, 4, 5]]; root=[1, 2, 3], target=5 -> []; root=[1, 2], target=0 -> []; root=[], target=0 -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** DFS with backtracking on one shared path list. Choose, recurse, undo.

**Say this first (1 line):** "One shared `path`: append the node, recurse, pop on the way out; at a real leaf with remaining sum 0 I copy the path into the answer."

**Brute force:** Build every root-to-leaf path as a new list (a new list per node, `path + [val]`), then filter by sum. O(n * h) time and space in the worst case, because each node copies a path of length up to h.

**Optimal:**
- `go(node, rem)`: append `node.val`, subtract it from `rem`. If the node is a leaf (no left and no right) and `rem == 0`, record `path[:]`. Otherwise recurse left then right. Finally `path.pop()`.
- A leaf means both children missing. `[1, 2]` with target 1 is not a match: 1 has one child, so 1 alone is not a root-to-leaf path. The run shows target 3 matches `[[1, 2]]`.
- Left before right gives the left-to-right leaf order the prompt asks for.
- Do not prune on `rem < 0`, because values can be negative.
- Why copying matters: the answer would hold the same list object that keeps being mutated. In my run the buggy version printed `[[], []]` (two references to one list, emptied by the pops) for the first example. `path[:]` snapshots the current contents.
- Cost of copying: k matches of length up to h cost O(k * h) extra, on top of the O(n) walk. The walk itself does O(1) work per node (append and pop), so the total is O(n + k * h).

**Complexity:** Time O(n + k * L) with k matching paths of length L at most h. Space O(h) for the path and the recursion, plus the output.

**Dry run:** Example 1 with target 22. Path 5, 4, 11, 7: leaf 7, sum 27, no. Pop 7, go to 2: path 5, 4, 11, 2 sums to 22, copy it. Backtrack to 5, go right: 8, 13 (26, no), 4, then 5 gives 5 + 8 + 4 + 5 = 22, copy; then 1 gives 18, no. Result `[[5, 4, 11, 2], [5, 8, 4, 5]]`.

**Code:**
```python
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

def path_sum_rec(root, target):
    """Backtracking on ONE shared path list. Recursive: depth = height (fails on a 5000-node chain by default)."""
    res, path = [], []
    def go(n, rem):
        if n is None: return
        path.append(n.val); rem -= n.val
        if n.left is None and n.right is None:
            if rem == 0: res.append(path[:])          # COPY here; path keeps changing afterwards
        else:
            go(n.left, rem); go(n.right, rem)
        path.pop()                                    # undo on the way out
    go(root, target)
    return res

def path_sum_iter(root, target):
    """Same idea with an explicit stack of (node, entered?) pairs: no recursion limit."""
    res, path, st, rem = [], [], [(root, False)] if root else [], 0
    while st:
        n, done = st.pop()
        if done:
            path.pop(); rem -= n.val; continue
        path.append(n.val); rem += n.val              # rem is now the running sum from the root
        st.append((n, True))
        if n.left is None and n.right is None:
            if rem == target: res.append(path[:])
        else:
            if n.right: st.append((n.right, False))   # push right first so left is processed first
            if n.left:  st.append((n.left, False))
    return res

def path_sum_buggy(root, target):
    """BUG: appends the shared list itself instead of a copy."""
    res, path = [], []
    def go(n, rem):
        if n is None: return
        path.append(n.val); rem -= n.val
        if n.left is None and n.right is None:
            if rem == 0: res.append(path)             # <- same list object every time
        else:
            go(n.left, rem); go(n.right, rem)
        path.pop()
    go(root, target)
    return res

def leaf_paths(t, pre=()):
    """Independent brute force on tuple trees: every root-to-leaf path, then filter."""
    if t is None: return []
    p = pre + (t[0],)
    if t[1] is None and t[2] is None: return [list(p)]
    return leaf_paths(t[1], p) + leaf_paths(t[2], p)

for arr, tg, exp in [([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22, [[5, 4, 11, 2], [5, 8, 4, 5]]),
                     ([1, 2, 3], 5, []), ([1, 2], 0, []), ([], 0, [])]:
    r = build_tree(arr); a, b = path_sum_rec(r, tg), path_sum_iter(r, tg)
    assert a == b == exp, (arr, a, b)
    print(arr, "target", tg, "->", a)
print("[1, 2] with target 3 ->", path_sum_rec(build_tree([1, 2]), 3), "(1 has one child, so 1 alone is not a leaf path; 1-2 is)")
print("bug (no copy), same first example:", path_sum_buggy(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22))

# exhaustive over all shapes 0..7 with several value labelings (values in -2..3) and every target in range
random.seed(26); cnt = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(4):
            vals = iter(random.randint(-2, 3) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return (v, L, lab(x[1]))
            t = lab(s); r = from_tup(t); allp = leaf_paths(t)
            for tg in range(-8, 12):
                exp = [p for p in allp if sum(p) == tg]
                assert path_sum_rec(r, tg) == path_sum_iter(r, tg) == exp
                cnt += 1
print("exhaustive+random ok:", cnt, "(tree, target) cases; order = left-to-right order of leaves")

# 5000-node chain: recursion fails by default, the explicit stack does not
chain = None
for _ in range(5000): chain = TreeNode(1, chain, None)
try:
    path_sum_rec(chain, 5000); print("recursive: no error")
except RecursionError:
    print("recursive on a 5000-node chain: RecursionError")
res = path_sum_iter(chain, 5000)
assert len(res) == 1 and len(res[0]) == 5000
print("iterative on the same chain: 1 path of length", len(res[0]))
# cost of copying: k matches of length L cost k * L extra. all-zero tree, target 0: every leaf matches
zeros31 = build_tree([0] * 31)       # 16 leaves, path length 5
print("perfect tree 31 nodes all zero, target 0: matches =", len(path_sum_rec(zeros31, 0)), "each of length 5")
```

**Output (my run):**
```
[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1] target 22 -> [[5, 4, 11, 2], [5, 8, 4, 5]]
[1, 2, 3] target 5 -> []
[1, 2] target 0 -> []
[] target 0 -> []
[1, 2] with target 3 -> [[1, 2]] (1 has one child, so 1 alone is not a leaf path; 1-2 is)
bug (no copy), same first example: [[], []]
exhaustive+random ok: 50080 (tree, target) cases; order = left-to-right order of leaves
recursive on a 5000-node chain: RecursionError
iterative on the same chain: 1 path of length 5000
perfect tree 31 nodes all zero, target 0: matches = 16 each of length 5
```

**Edge cases:**
- Empty tree: `[]`, even for target 0 (there is no path).
- Node with one child is not a leaf.
- Negative or zero values: no early pruning; 50080 (tree, target) cases agreed with the brute force.
- n = 5000 as a chain: the recursive version raised RecursionError in my run (default limit 1000); the explicit-stack version returned the one path of length 5000. Use it for the stated limit.

**Follow-ups:**
- Just return True or False (Path Sum I)? Drop the list and return `go(left) or go(right)` at the leaf test.
- Paths that do not start at the root? That is Part 7 Q27 (prefix sums).
- Why not pass `path + [val]` down? It is simpler and cannot alias, at O(h) copying per node: O(n * h) always, not only for matches.

**Common mistakes:**
- `res.append(path)` without a copy.
- Forgetting `path.pop()` on the leaf branch, so the path grows wrong.
- Treating a node with one child as a leaf.
- Pruning when the running sum goes above the target, which is wrong with negatives.

### Q27 ⭐⭐ 🟡 Path sum III: count downward paths with prefix sums. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Count the paths whose values sum to `target`, where a path goes downward from any node to any descendant (it need not start at the root or end at a leaf; a single node counts), values may be negative or zero, 0 <= n <= 1000. Beat the O(n * h) solution that starts a walk at every node with a prefix-sum dictionary: count[prefix] along the current root-to-node path, answer += count[prefix - target], and UNDO the count when you leave the node. The array version of this idea is Part 1 Q13; explain what breaks if you forget the undo. Example: root=[10, 5, -3, 3, 2, null, 11, 3, -2, null, 1], target=8 -> 3; root=[5, 4, 8, 11, null, 13, 4, 7, 2, null, null, 5, 1], target=22 -> 3; root=[1, -1], target=0 -> 1; root=[0, 0, null, 0], target=0 -> 6.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Prefix sums on a tree path, with a hash map that is updated when you enter a node and undone when you leave it. The array version is Part 1 Q13.

**Say this first (1 line):** "Along the current root-to-node path, a downward path ending here sums to target exactly when an earlier prefix equals prefix minus target, so I look that up in a counter and remove my own prefix when I leave."

**Brute force:** Start a downward walk at every node and count walks with sum equal to target. O(n * h) time, O(h) space: O(n^2) on a chain, O(n log n) on a balanced tree.

**Optimal:**
- `prefix` = sum from the root to the current node. `count[p]` = how many nodes on the CURRENT root-to-node path have prefix p (start with `count[0] = 1` for the empty prefix, so a path starting at the root counts).
- At a node: `ans += count[prefix - target]`; then `count[prefix] += 1`; recurse into both children; then `count[prefix] -= 1`.
- Why the undo: `count` must describe only the ancestors of the current node. A path has to go downward, so a node in the left subtree must not be matched against a prefix recorded in the right subtree.
- What breaks without it: stale prefixes from finished branches are counted as if they were ancestors, so you count "paths" that go up and over. In my run, `[1, 1, 1]` with target 0 gave 1 instead of 0, and forgetting the undo was wrong in 4934 of 24414 small cases.
- Values may be negative or zero, so you cannot shrink a window; the counter handles that.

**Complexity:** Time O(n): one visit per node, O(1) average per dictionary operation. Space O(h) for the path, the dictionary (at most h keys live) and the stack.

**Dry run:** `[1, -1]`, target 0. count = {0: 1}. Node 1: prefix 1, look up 1 - 0 = 1: none. count[1] = 1. Node -1: prefix 0, look up 0: count[0] = 1, so ans = 1 (the path 1, -1). Undo both. Answer 1.

**Code:**
```python
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

def count_paths_brute(root, target):
    """O(n * h): start a downward walk at every node."""
    total = 0
    for start in nodes_of(root):
        st = [(start, start.val)]
        while st:
            n, s = st.pop()
            if s == target: total += 1
            for c in (n.left, n.right):
                if c: st.append((c, s + c.val))
    return total

def count_paths_prefix_rec(root, target, undo=True):
    """O(n): count[prefix] along the CURRENT root-to-node path. Recursion depth = height."""
    count = {0: 1}                                    # the empty prefix
    ans = 0
    def go(n, prefix):
        nonlocal ans
        if n is None: return
        prefix += n.val
        ans += count.get(prefix - target, 0)          # paths ending at n that start below some ancestor
        count[prefix] = count.get(prefix, 0) + 1
        go(n.left, prefix); go(n.right, prefix)
        if undo: count[prefix] -= 1                   # leaving n: the prefix is no longer on the path
    go(root, 0)
    return ans

def count_paths_prefix_iter(root, target):
    """Same, with an explicit stack of (node, prefix_before, entered?) so deep trees are fine."""
    count, ans = {0: 1}, 0
    st = [(root, 0, False)] if root else []
    while st:
        n, before, leaving = st.pop()
        prefix = before + n.val
        if leaving:
            count[prefix] -= 1; continue              # the undo
        ans += count.get(prefix - target, 0)
        count[prefix] = count.get(prefix, 0) + 1
        st.append((n, before, True))
        if n.right: st.append((n.right, prefix, False))
        if n.left:  st.append((n.left, prefix, False))
    return ans

cases = [([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8, 3), ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22, 3),
         ([1, -1], 0, 1), ([0, 0, None, 0], 0, 6)]
for arr, tg, exp in cases:
    r = build_tree(arr)
    a, b, c = count_paths_brute(r, tg), count_paths_prefix_rec(r, tg), count_paths_prefix_iter(r, tg)
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, "target", tg, "->", b)
print("empty tree ->", count_paths_prefix_iter(None, 0))
# find the smallest tree where forgetting the undo gives a wrong answer
found = None
for n in range(1, 6):
    for arr in ([1] * n, [1, 2, 3, 4, 5][:n], [1, 1, 1, 1, 1][:n]):
        r = build_tree(arr)
        for tg in range(0, 8):
            if found is None and count_paths_prefix_rec(r, tg, undo=False) != count_paths_brute(r, tg):
                found = (arr, tg, count_paths_prefix_rec(r, tg, undo=False), count_paths_brute(r, tg))
print("forgetting the undo, first failing case (array, target, buggy, true):", found)
assert found is not None

# exhaustive: all shapes up to 7 nodes, values drawn from {-2..2} (zeros and negatives), all targets -6..6
random.seed(27); cnt = 0; bug_wrong = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(3):
            vals = iter(random.randint(-2, 2) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return TreeNode(v, L, lab(x[1]))
            r = lab(s)
            for tg in range(-6, 7):
                e = count_paths_brute(r, tg)
                assert count_paths_prefix_rec(r, tg) == count_paths_prefix_iter(r, tg) == e
                if count_paths_prefix_rec(r, tg, undo=False) != e: bug_wrong += 1
                cnt += 1
print("exhaustive+random ok:", cnt, "cases; forgetting the undo was wrong in", bug_wrong, "of them")

# n = 1000 chain of ones, target 3: recursion depth 1000 hits the limit, the iterative one is fine
chain = None
for _ in range(1000): chain = TreeNode(1, chain, None)
try:
    count_paths_prefix_rec(chain, 3); print("recursive: no error")
except RecursionError:
    print("recursive on a 1000-node chain: RecursionError")
assert count_paths_prefix_iter(chain, 3) == 998 and count_paths_brute(chain, 3) == 998
print("iterative on the chain, target 3 ->", count_paths_prefix_iter(chain, 3), "(starts 998 down the chain)")
```

**Output (my run):**
```
[10, 5, -3, 3, 2, None, 11, 3, -2, None, 1] target 8 -> 3
[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1] target 22 -> 3
[1, -1] target 0 -> 1
[0, 0, None, 0] target 0 -> 6
empty tree -> 0
forgetting the undo, first failing case (array, target, buggy, true): ([1, 1, 1], 0, 1, 0)
exhaustive+random ok: 24414 cases; forgetting the undo was wrong in 4934 of them
recursive on a 1000-node chain: RecursionError
iterative on the chain, target 3 -> 998 (starts 998 down the chain)
```

**Edge cases:**
- Empty tree: 0.
- A single node equal to target: counts once, through `count[0]`.
- Zeros: `[0, 0, null, 0]` with target 0 gives 6 (every downward path of the 3-chain: 3 singles, 2 pairs, 1 triple).
- Depth: n up to 1000 makes the recursion depth 1000, and in my run the recursive version raised RecursionError on a 1000-node chain. The iterative version (enter/leave entries on a stack) worked and returned 998 for target 3.
- Large sums are fine, Python ints do not overflow.

**Follow-ups:**
- Why `count[0] = 1`? Otherwise paths that begin at the root are missed.
- What if you need the paths themselves? Use Part 7 Q26 style backtracking; the counter only gives a count.
- Why does the dictionary stay small? Undoing removes the prefixes of finished branches, so it holds at most h + 1 distinct keys at once.

**Common mistakes:**
- No undo.
- Missing the initial `{0: 1}`.
- Updating the counter before the lookup, which counts an empty path when target is 0.
- Looking up `prefix + target` instead of `prefix - target`.

### Q28 ⭐⭐ 🟡 Vertical order traversal. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Give the root column 0, a left child the column one less than its parent and a right child one more, and the root row 0 with each child one row below its parent. Return the values grouped by column from the leftmost to the rightmost; inside a column order by row (top first), and when two nodes share both row and column put the smaller value first. Use a BFS or DFS that records (column, row, value) and sort, or a BFS with a per-column bucket if the tie rule is first-come; state the cost of each (n up to 1000). A public candidate report describes a version of this problem where ties follow insertion order, so always ask which tie rule is wanted. Example: root=[3, 9, 20, null, null, 15, 7] -> [[9], [3, 15], [20], [7]]; root=[1, 2, 3, 4, 5, 6, 7] -> [[4], [2], [1, 5, 6], [3], [7]]; root=[3, 1, 4, 0, 2, 2] -> [[0], [1], [3, 2, 2], [4]]; root=[] -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Coordinates on a tree: column (left minus 1, right plus 1) and row (depth). Group by column, order inside a column by row, then by the tie rule.

**Say this first (1 line):** "First ask which tie rule applies for same row and same column; then record (column, row, value) per node, sort, and group by column."

**Brute force:** For every node compute (column, row, value), then for every column scan all nodes and sort the ones in it. O(n * c) with c columns, O(n^2) worst case on a chain.

**Optimal:**
- One BFS (or DFS) collecting `(col, row, val)`. Sort the list: tuple order is column, row, value, which is exactly the rule in the prompt. Group consecutive equal columns.
- DFS works too because the sort puts rows back in order; BFS plus the sort is the same cost.
- Tie rule matters. With "smaller value first" you must sort by value. With "insertion order" (BFS first-come) you can skip the sort: BFS visits rows top to bottom and, within a row, left to right, so appending to a per-column bucket gives the right order, and the columns are the range min..max, O(n) in total. A public candidate report describes the insertion-order version, so ask.
- Example of the difference from my run: `[1, 2, 3, null, 5, 4]` has 5 and 4 in column 0, row 2. The sorted rule gives `[[2], [1, 4, 5], [3]]`, first-come gives `[[2], [1, 5, 4], [3]]`. On shapes up to 7 nodes with values 0 to 2, the two rules differed on 58 of 1878 trees.

**Complexity:** Sorted rule: O(n log n) time (the sort), O(n) space. First-come BFS: O(n) time, O(n) space. n = 1000 is tiny either way.

**Dry run:** `[3, 9, 20, null, null, 15, 7]`. 3 at (0, 0); 9 at (-1, 1); 20 at (1, 1); 15 at (0, 2); 7 at (2, 2). Sorted: (-1,1,9), (0,0,3), (0,2,15), (1,1,20), (2,2,7). Groups: `[[9], [3, 15], [20], [7]]`.

**Code:**
```python
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

def vertical_sorted(root):
    """Walk with BFS, record (col, row, val), sort, group by column. O(n log n)."""
    if root is None: return []
    rec, q = [], deque([(root, 0, 0)])
    while q:
        n, col, row = q.popleft(); rec.append((col, row, n.val))
        if n.left:  q.append((n.left, col - 1, row + 1))
        if n.right: q.append((n.right, col + 1, row + 1))
    rec.sort()                                         # column, then row, then value (the tie rule)
    out, last = [], None
    for col, row, v in rec:
        if col != last: out.append([]); last = col
        out[-1].append(v)
    return out

def vertical_first_come(root):
    """BFS with per-column buckets. Ties (same row and column) keep BFS order = left-to-right. O(n)."""
    if root is None: return []
    buckets, q = {}, deque([(root, 0)])
    while q:
        n, col = q.popleft(); buckets.setdefault(col, []).append(n.val)
        if n.left:  q.append((n.left, col - 1))
        if n.right: q.append((n.right, col + 1))
    return [buckets[c] for c in range(min(buckets), max(buckets) + 1)]

def vertical_dfs(root):
    """DFS version (explicit stack): the sort puts rows back in order, so DFS visiting order does not matter."""
    rec, st = [], [(root, 0, 0)] if root else []
    while st:
        n, col, row = st.pop(); rec.append((col, row, n.val))
        if n.right: st.append((n.right, col + 1, row + 1))
        if n.left:  st.append((n.left, col - 1, row + 1))
    rec.sort(); cols = {}
    for c, r, v in rec: cols.setdefault(c, []).append(v)
    return [cols[c] for c in sorted(cols)]

def vertical_tuple(t):
    """Independent brute force on tuple trees: for each column, nodes sorted by (row, value)."""
    nodes = []
    def go(t, c, r):
        if t is None: return
        nodes.append((c, r, t[0])); go(t[1], c - 1, r + 1); go(t[2], c + 1, r + 1)
    go(t, 0, 0)
    return [[v for (cc, r, v) in sorted(x for x in nodes if x[0] == c)] for c in sorted({x[0] for x in nodes})]

for arr, exp in [([3, 9, 20, None, None, 15, 7], [[9], [3, 15], [20], [7]]),
                 ([1, 2, 3, 4, 5, 6, 7], [[4], [2], [1, 5, 6], [3], [7]]),
                 ([3, 1, 4, 0, 2, 2], [[0], [1], [3, 2, 2], [4]]), ([], [])]:
    r = build_tree(arr); a = vertical_sorted(r)
    assert a == vertical_dfs(r) == exp, (arr, a)
    print(arr, "->", a)

# exhaustive over shapes up to 7 nodes with values from {0,1,2} so ties on (col,row) with different values occur
random.seed(28); cnt = diff = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(3):
            vals = iter(random.randint(0, 2) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return (v, L, lab(x[1]))
            t = lab(s); r = from_tup(t)
            assert vertical_sorted(r) == vertical_dfs(r) == vertical_tuple(t)
            f = vertical_first_come(r)
            assert [sorted(c) for c in f] == [sorted(c) for c in vertical_sorted(r)]      # same groups, maybe different order inside a column
            assert [len(c) for c in f] == [len(c) for c in vertical_sorted(r)]
            if f != vertical_sorted(r): diff += 1
            cnt += 1
print("exhaustive+random ok:", cnt, "trees; first-come order differs from the sorted tie rule on", diff, "of them")
# one concrete difference
ex = build_tree([1, 2, 3, None, 5, 4])      # 5 and 4 share column 0 and row 2; 5 is left of 4 in BFS, but 4 < 5
print("tie example [1, 2, 3, None, 5, 4]: sorted rule", vertical_sorted(ex), "| first-come", vertical_first_come(ex))
big = build_tree([random.randint(0, 99) for _ in range(1000)])
assert vertical_sorted(big) == vertical_dfs(big) and sum(map(len, vertical_sorted(big))) == 1000
print("n = 1000 random tree: columns =", len(vertical_sorted(big)))
```

**Output (my run):**
```
[3, 9, 20, None, None, 15, 7] -> [[9], [3, 15], [20], [7]]
[1, 2, 3, 4, 5, 6, 7] -> [[4], [2], [1, 5, 6], [3], [7]]
[3, 1, 4, 0, 2, 2] -> [[0], [1], [3, 2, 2], [4]]
[] -> []
exhaustive+random ok: 1878 trees; first-come order differs from the sorted tie rule on 58 of them
tie example [1, 2, 3, None, 5, 4]: sorted rule [[2], [1, 4, 5], [3]] | first-come [[2], [1, 5, 4], [3]]
n = 1000 random tree: columns = 18
```

**Edge cases:**
- Empty tree: `[]`.
- Same value twice in one cell, as in `[3, 1, 4, 0, 2, 2]`: both stay, column 0 is `[3, 2, 2]`.
- A node and a deeper node in the same column: row order puts the shallower one first, even when its value is bigger. That is why you cannot just sort by value inside a column.
- Skewed tree: n columns or one column; the DFS here uses an explicit stack, so depth is not a problem.

**Follow-ups:**
- Top view or bottom view? Same coordinates; keep the first (or last) node per column.
- Why not a dict of lists only? You need the column order at the end, so sort the keys or track min and max.
- Can I avoid the sort completely? Only for the first-come rule.

**Common mistakes:**
- Sorting by (column, value) and forgetting the row.
- Using DFS order with no row in the sort key.
- Assuming "left to right" breaks ties the same as "smaller value first".
- Building the column list with `range(min, max)` and dropping the last column.

### Q29 ⭐⭐ 🟡 Build a tree from inorder and postorder. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given the inorder and postorder traversals of a tree with DISTINCT values (1 <= n <= 3000), rebuild and return it. The root is the LAST postorder value; build the RIGHT subtree before the left when you consume postorder from the end, and explain why. Use an index map for O(n). Then show that preorder plus postorder does NOT identify a binary tree uniquely (give two different trees with the same pair; the tests check your pair exhaustively over small shapes) and say which trees it does identify. Example: inorder=[9, 3, 15, 20, 7], postorder=[9, 15, 7, 20, 3] -> [3, 9, 20, null, null, 15, 7]; inorder=[-1], postorder=[-1] -> [-1]; inorder=[2, 1], postorder=[2, 1] -> [1, 2]; inorder=[1, 2], postorder=[2, 1] -> [1, null, 2].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Divide and conquer on traversal orders. Postorder ends with the root; the root's position in inorder splits left from right.

**Say this first (1 line):** "Last postorder value is the root, find it in inorder through a hash map, build the right subtree first because I am reading postorder backward, then the left."

**Brute force:** Slice both lists each time and use `list.index`. Correct, but `index` is O(n) and slicing copies, so O(n^2) time and space on a skewed tree.

**Optimal:**
- Map each value to its inorder index (values are distinct). Keep one cursor at the end of postorder.
- `go(lo, hi)` on an inorder window: take `postorder[cursor]`, decrement the cursor, make the node, find its index k. Then `right = go(k + 1, hi)` and `left = go(lo, k - 1)`.
- Why right first: postorder is left, right, root. Read backward it is root, right, left. After taking the root, the next values from the end belong to the right subtree, so the right subtree has to consume them before the left one does. Swapping the order silently builds a wrong tree.
- Preorder plus postorder does NOT identify a tree. If a node has exactly one child, the child could be left or right and both trees give the same pair. Two-node example from my run: preorder `[0, 1]`, postorder `[1, 0]` fits `[0, null, 1]` and `[0, 1]`. (Preorder plus inorder, and inorder plus postorder, are unique; I checked all shapes up to 8 nodes for the second one.)
- Which trees are identified: exactly the FULL binary trees (every node has 0 or 2 children). In my exhaustive run up to 7 nodes, every unique pair was a full tree and no full tree collided with another tree. A non-full tree has a one-child node, and mirroring that child gives a second tree with the same pair.

**Complexity:** Time O(n) (one dict build, one pass), space O(n) for the map plus O(h) stack.

**Dry run:** inorder `[9, 3, 15, 20, 7]`, postorder `[9, 15, 7, 20, 3]`. Cursor at 3: root 3, index 1. Right window (2..4): next from the end is 20, index 3. Its right window (4..4): 7. Its left window (2..2): 15. Back to 3's left window (0..0): 9. Result `[3, 9, 20, null, null, 15, 7]`.

**Code:**
```python
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

def build_slices(inorder, postorder):
    """Brute force: slice the lists and use list.index. O(n^2) time and space on skewed trees."""
    if not postorder: return None
    root = postorder[-1]; k = inorder.index(root)
    return TreeNode(root, build_slices(inorder[:k], postorder[:k]),
                    build_slices(inorder[k + 1:], postorder[k:-1]))

def build_in_post(inorder, postorder):
    """O(n): index map + a cursor walking postorder from the END. Right subtree first. Recursion depth = height."""
    pos = {v: i for i, v in enumerate(inorder)}
    assert len(pos) == len(inorder) == len(postorder), "values must be distinct and lists equal length"
    cur = [len(postorder) - 1]
    def go(lo, hi):                                  # inorder window [lo, hi]
        if lo > hi: return None
        v = postorder[cur[0]]; cur[0] -= 1           # the next unused value from the end is this window's root
        node = TreeNode(v)
        k = pos[v]
        node.right = go(k + 1, hi)                   # postorder is left, right, root: reading backward meets RIGHT first
        node.left = go(lo, k - 1)
        return node
    return go(0, len(inorder) - 1)

def build_in_post_iter(inorder, postorder):
    """Same tree with an explicit stack (safe for a 3000-node chain). One pass over postorder from the end."""
    n = len(postorder)
    if n == 0: return None
    root = TreeNode(postorder[-1]); stack = [root]; j = n - 1      # j walks inorder from the end
    for i in range(n - 2, -1, -1):
        node = TreeNode(postorder[i]); parent = stack[-1]
        if parent.val != inorder[j]:
            parent.right = node                       # the parent's own inorder slot is still ahead: we are in its right subtree
        else:
            while stack and stack[-1].val == inorder[j]:
                parent = stack.pop(); j -= 1          # unwind to the ancestor whose LEFT child this is
            parent.left = node
        stack.append(node)
    return root

def tin(t):   return [] if t is None else tin(t[1]) + [t[0]] + tin(t[2])
def tpost(t): return [] if t is None else tpost(t[1]) + tpost(t[2]) + [t[0]]
def tpre(t):  return [] if t is None else [t[0]] + tpre(t[1]) + tpre(t[2])

for ino, post, exp in [([9, 3, 15, 20, 7], [9, 15, 7, 20, 3], [3, 9, 20, None, None, 15, 7]), ([-1], [-1], [-1]),
                       ([2, 1], [2, 1], [1, 2]), ([1, 2], [2, 1], [1, None, 2])]:
    a, b, c = build_in_post(ino, post), build_in_post_iter(ino, post), build_slices(ino, post)
    assert to_arr(a) == to_arr(b) == to_arr(c) == exp, (ino, to_arr(a), to_arr(b))
    print("inorder", ino, "postorder", post, "->", to_arr(a))

# exhaustive: every shape with 1..8 nodes (values are distinct labels): rebuild from (inorder, postorder) and compare structure
cnt = 0; pairs = {}
for n in range(1, 9):
    for s in shapes(n):
        t = label_inorder(s); ino, post = tin(t), tpost(t)
        for fn in (build_in_post, build_in_post_iter, build_slices):
            assert same_shape(fn(ino, post), from_tup(t))
        pairs.setdefault((tuple(ino), tuple(post)), []).append(t); cnt += 1
assert all(len(v) == 1 for v in pairs.values())      # (inorder, postorder) never collides, so the answer is unique
print("exhaustive ok:", cnt, "shapes up to 8 nodes rebuilt by all three builders; every (inorder, postorder) pair is unique")

# random trees with random distinct values (not just inorder labels)
random.seed(29)
for _ in range(300):
    m = random.randint(1, 7); shape = random.choice(shapes(m))
    it = iter(random.sample(range(-100, 100), m))
    def lab(x):
        if x is None: return None
        L = lab(x[0]); v = next(it); return (v, L, lab(x[1]))
    t = lab(shape)
    assert same_shape(build_in_post(tin(t), tpost(t)), from_tup(t)) and same_shape(build_in_post_iter(tin(t), tpost(t)), from_tup(t))
print("random cross-check ok (300 trees with random distinct values)")

# preorder + postorder is NOT enough. Group every labelled shape by (preorder, postorder) after relabelling by preorder (values 0..n-1)
def label_pre(shape, c):
    if shape is None: return None
    v = c[0]; c[0] += 1; L = label_pre(shape[0], c); return (v, L, label_pre(shape[1], c))
def is_full(t): return t is None or ((t[1] is None) == (t[2] is None) and is_full(t[1]) and is_full(t[2]))
def collisions(n):
    g = {}
    for s in shapes(n):
        t = label_pre(s, [0]); g.setdefault((tuple(tpre(t)), tuple(tpost(t))), []).append(t)
    return g
# the fixed-values version: shapes labelled in PREORDER 0..n-1 give the same preorder list for all shapes, so colliding pairs show up as shared keys
for n in range(1, 8):
    g = collisions(n); multi = [k for k, v in g.items() if len(v) > 1]
    uniq_full = all(is_full(v[0]) for v in g.values() if len(v) == 1)
    nonfull_alone = [v for v in g.values() if len(v) == 1 and not is_full(v[0])]
    full_collide = [v for v in g.values() if len(v) > 1 and any(is_full(t) for t in v)]
    assert uniq_full and not full_collide and not nonfull_alone
    print("n =", n, "shapes =", len(shapes(n)), "pairs shared by >= 2 trees =", len(multi), "| every unique pair is a FULL tree, no full tree collides")
g = collisions(2); k = [k for k, v in g.items() if len(v) > 1][0]
print("n = 2 collision: preorder", list(k[0]), "postorder", list(k[1]), "->", [to_arr(from_tup(t)) for t in g[k]])
a, b = g[k]; assert not same_shape(from_tup(a), from_tup(b))

# deep skew: 3000-node left chain. Recursive fails under the default limit, the explicit-stack builder is fine.
n = 3000
ino = list(range(n)); post = list(range(n))   # inorder = postorder = 0..n-1: every node is the LEFT child of the next one
try:
    build_in_post(ino, post); print("recursive: no error")
except RecursionError:
    print("recursive on a 3000-node left chain: RecursionError")
deep = build_in_post_iter(ino, post)
assert height(deep) == n and deep.val == n - 1
print("iterative on the same input: root", deep.val, "height", height(deep))
```

**Output (my run):**
```
inorder [9, 3, 15, 20, 7] postorder [9, 15, 7, 20, 3] -> [3, 9, 20, None, None, 15, 7]
inorder [-1] postorder [-1] -> [-1]
inorder [2, 1] postorder [2, 1] -> [1, 2]
inorder [1, 2] postorder [2, 1] -> [1, None, 2]
exhaustive ok: 2055 shapes up to 8 nodes rebuilt by all three builders; every (inorder, postorder) pair is unique
random cross-check ok (300 trees with random distinct values)
n = 1 shapes = 1 pairs shared by >= 2 trees = 0 | every unique pair is a FULL tree, no full tree collides
n = 2 shapes = 2 pairs shared by >= 2 trees = 1 | every unique pair is a FULL tree, no full tree collides
n = 3 shapes = 5 pairs shared by >= 2 trees = 1 | every unique pair is a FULL tree, no full tree collides
n = 4 shapes = 14 pairs shared by >= 2 trees = 4 | every unique pair is a FULL tree, no full tree collides
n = 5 shapes = 42 pairs shared by >= 2 trees = 7 | every unique pair is a FULL tree, no full tree collides
n = 6 shapes = 132 pairs shared by >= 2 trees = 21 | every unique pair is a FULL tree, no full tree collides
n = 7 shapes = 429 pairs shared by >= 2 trees = 46 | every unique pair is a FULL tree, no full tree collides
n = 2 collision: preorder [0, 1] postorder [1, 0] -> [[0, None, 1], [0, 1]]
recursive on a 3000-node left chain: RecursionError
iterative on the same input: root 2999 height 3000
```

**Edge cases:**
- n = 1: a single node.
- Values must be distinct, or the index map is ambiguous.
- Skewed input: for n = 3000 as a left chain the recursive version raised RecursionError in my run. The stack-based builder (shown) handles it in one pass.
- Inconsistent lists (not from one tree): the code asserts equal length and distinct values but a full validity check would compare the result's traversals.

**Follow-ups:**
- Preorder plus inorder? Root is the first preorder value; build LEFT first.
- Why is the map needed? Without it each root lookup is O(n).
- Can you build from postorder alone for a BST? Yes, the BST property replaces the inorder list (the root is the last value, and the split is by value).

**Common mistakes:**
- Building left before right and consuming the wrong postorder values.
- Using `index` on slices and getting O(n^2).
- Claiming preorder plus postorder is unique.
- Passing slices of the postorder list instead of a cursor.

### Q30 ⭐⭐ 🟡 BST iterator with O(h) space. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Implement a class over a BST (distinct values, n <= 10^5) with `next()` returning the next smallest value and `hasNext()`. Both must run in amortized O(1) time and the iterator may hold only O(h) nodes in a stack (do not flatten the tree into a list, which costs O(n) space). Push the left spine on construction and after each `next()` push the left spine of the popped node's right child. The example runs a list of operations on the given tree and lists the results. Example: root=[7, 3, 15, null, null, 9, 20], ops=['next', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext'] -> [3, 7, True, 9, True, 15, True, 20, False].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Controlled inorder traversal. An explicit stack holding the left spine is a paused recursion.

**Say this first (1 line):** "The stack holds the path of nodes whose left spine I have gone down; `next` pops one, pushes the left spine of its right child, and each node is pushed and popped once, so it is amortized O(1) with O(h) memory."

**Brute force:** In the constructor do a full inorder into a list, then walk an index. `next` and `hasNext` are O(1), but the constructor is O(n) time and the list takes O(n) space, which breaks the O(h) requirement.

**Optimal:**
- Constructor: push `root`, `root.left`, ... down the left spine.
- `hasNext()`: the stack is not empty.
- `next()`: pop the top (it is the smallest unvisited). Then push the left spine of its right child. Return the popped value.
- Invariant: the stack holds exactly the ancestors that are still unvisited, plus the left spine below them. The top is always the next value in sorted order.
- Space: the stack is a subset of one root-to-node path, so at most h nodes (checked on 2056 BST shapes up to 8 nodes; the peak was never above h, and the number of pushes was always exactly n).

**Complexity:** `next` can push a whole spine, so one call can be O(h). But each node is pushed once and popped once in total, so n calls cost O(n): amortized O(1) per call. Space O(h): about log n when balanced and n for a chain. In the run a balanced tree of 16383 nodes peaked at 14, and a 20000-node left chain held 20000 right after the constructor.

**Dry run:** `[7, 3, 15, null, null, 9, 20]`. Constructor pushes 7, 3. `next`: pop 3, right child None, return 3. `next`: pop 7, push left spine of 15: 15, 9; return 7. `hasNext` True. `next`: pop 9, return 9. `next`: pop 15, push 20; return 15. `next`: pop 20; return 20; the stack is empty, `hasNext` False. Output `[3, 7, True, 9, True, 15, True, 20, False]`.

**Code:**
```python
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

class BSTIterator:
    """In-order iterator holding only the current left spine: at most h nodes in the stack."""
    def __init__(self, root):
        self.stack = []; self.pushes = 0; self.max_stack = 0
        self._push_left(root)
    def _push_left(self, node):
        while node is not None:
            self.stack.append(node); self.pushes += 1; node = node.left
        self.max_stack = max(self.max_stack, len(self.stack))
    def hasNext(self):
        return bool(self.stack)
    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)          # the only new work: the left spine of the right child
        return node.val

class FlatIterator:
    """Brute force: flatten to a list in the constructor. O(n) space."""
    def __init__(self, root):
        self.vals, st, cur = [], [], root
        while st or cur:
            while cur: st.append(cur); cur = cur.left
            cur = st.pop(); self.vals.append(cur.val); cur = cur.right
        self.i = 0
    def hasNext(self): return self.i < len(self.vals)
    def next(self):
        self.i += 1; return self.vals[self.i - 1]

def run_ops(it, ops):
    return [getattr(it, o)() for o in ops]

ops = ['next', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext', 'next', 'hasNext']
r = build_tree([7, 3, 15, None, None, 9, 20])
got = run_ops(BSTIterator(r), ops); assert got == run_ops(FlatIterator(r), ops) == [3, 7, True, 9, True, 15, True, 20, False]
print("root [7, 3, 15, null, null, 9, 20] ->", got)
e = BSTIterator(None); assert e.hasNext() is False
print("empty tree: hasNext() ->", e.hasNext())

# exhaustive: every BST shape up to 8 nodes. Drain it; compare with inorder; stack never above h; each node pushed exactly once.
cnt = 0
for n in range(0, 9):
    for s in shapes(n):
        t = label_inorder(s); root = from_tup(t); h = height(root)
        it = BSTIterator(root); out = []
        while it.hasNext(): out.append(it.next())
        assert out == list(range(n)) and it.max_stack <= h and it.pushes == n
        if n: assert it.max_stack >= 1
        assert not it.hasNext()
        cnt += 1
print("exhaustive ok on", cnt, "BST shapes: output = sorted order, max stack <= h, total pushes = n")

# random interleavings of hasNext/next vs the flat version
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
random.seed(30)
for _ in range(300):
    root = None
    for v in random.sample(range(1000), random.randint(1, 80)): root = insert(root, v)
    a, b = BSTIterator(root), FlatIterator(root); n = len(nodes_of(root))
    for _ in range(n + 3):
        if random.random() < 0.5:
            assert a.hasNext() == b.hasNext()
        elif b.hasNext():
            assert a.next() == b.next()
print("random interleaving cross-check ok (300 trees)")

# space: balanced vs skewed, n = 2^k - 1 vs a left chain (sandbox counts of the stack peak)
def perfect(lo, hi):
    if lo > hi: return None
    m = (lo + hi) // 2; return TreeNode(m, perfect(lo, m - 1), perfect(m + 1, hi))
bal = BSTIterator(perfect(0, 2 ** 14 - 2))             # n = 16383
while bal.hasNext(): bal.next()
chain = None
for v in range(1, 20001): chain = TreeNode(v, chain, None)   # left chain: root 20000, leftmost 1
ch = BSTIterator(chain); first = ch.next()
print("balanced n = 16383: peak stack =", bal.max_stack, "| left chain n = 20000: stack right after the constructor =", ch.max_stack, "| first value", first)
assert bal.max_stack == 14 and ch.max_stack == 20000
```

**Output (my run):**
```
root [7, 3, 15, null, null, 9, 20] -> [3, 7, True, 9, True, 15, True, 20, False]
empty tree: hasNext() -> False
exhaustive ok on 2056 BST shapes: output = sorted order, max stack <= h, total pushes = n
random interleaving cross-check ok (300 trees)
balanced n = 16383: peak stack = 14 | left chain n = 20000: stack right after the constructor = 20000 | first value 1
```

**Edge cases:**
- Empty tree: `hasNext()` is False from the start (calling `next()` would be invalid).
- Calling `next()` when `hasNext()` is False is the caller's error; the prompt guarantees it does not happen.
- Skewed tree: h = n, so the stack is O(n) in the worst case and that is within the O(h) bound. The stack is explicit, so there is no recursion limit even at n = 10^5.
- Do not modify the tree while iterating.

**Follow-ups:**
- Zero extra space? Morris traversal threads the tree and gives O(1) extra space, but `next` is then O(1) amortized only, and it temporarily modifies the tree.
- A `peek`? Return `stack[-1].val`.
- Reverse (descending) iterator? Mirror it: push right spines.

**Common mistakes:**
- Flattening the tree in the constructor (O(n) space).
- Pushing the right child instead of its left spine.
- Pushing the whole tree up front.
- Saying `next` is O(1) worst case. It is amortized, not worst case.
