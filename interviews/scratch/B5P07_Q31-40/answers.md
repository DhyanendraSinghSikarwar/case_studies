### Q31 ⭐⭐ 🟡 Delete a node from a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Given a BST with distinct values and a key (0 <= n <= 10^4), delete the node holding the key if it exists and return the root; do nothing if it does not exist. Rules, so the result is unique: a leaf is removed; a node with one child is replaced by that child; a node with two children takes the value of the smallest node in its right subtree (its inorder successor), and that successor node is then deleted from the right subtree. Write it recursively in O(h), explain the three cases, and say why re-linking nodes versus copying the value matters if other code holds references to nodes. Example: root=[5, 3, 6, 2, 4, null, 7], key=3 -> [5, 4, 6, 2, null, null, 7]; root=[5, 3, 6, 2, 4, null, 7], key=0 -> [5, 3, 6, 2, 4, null, 7]; root=[], key=0 -> []; root=[5, 3, 6, 2, 4, null, 7], key=5 -> [6, 3, 7, 2, 4]; root=[1], key=1 -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST search plus a three-case structural edit. The BST rule tells you where the key is; the edit only has to keep "left < node < right".

**Say this first (1 line):** "I walk down by the BST rule, then fix three cases: no left child, no right child, or two children, where I copy the inorder successor up and delete it from the right subtree. O(h)."

**Brute force:** Dump the inorder values, drop the key, rebuild a balanced BST. O(n) time and space, and it throws away the original shape and every node object. Fine as a checker, wrong as an answer.

**Optimal:**
- Search: key smaller goes left, larger goes right, and each recursive call returns the new root of that subtree, so the parent re-attaches it.
- Found, no left child: return `root.right` (covers the leaf, where that is None).
- Found, no right child: return `root.left`.
- Found, two children: the inorder successor is the leftmost node of the right subtree. It is the next value above the key, so it can sit at the key's position and keep the order. Copy its value up, then delete that value from the right subtree. The successor has no left child, so that second delete lands in case 1 or 2 and is cheap.
- Copy versus re-link. Copying changes the value inside a node object: any other code holding a reference to the "deleted" node now sees the successor's value and thinks it is still in the tree, while the object that really left the tree is the successor's. Re-linking moves the successor node into the deleted node's place, so the deleted node object is the one that ends up detached and keeps its own value. Use re-link when node identity matters (caches, parent pointers, other structures pointing at nodes). Both give the same shape.

**Complexity:** Time O(h): one descent to the key, one descent to the successor, at most 2h steps. Space O(h) for the recursion, O(1) for the iterative version. h is about log n when balanced but n for a skewed tree.

**Dry run:** `[5,3,6,2,4,null,7]`, key 5 (root, two children).
- Successor: go right to 6, no left child, so successor is 6.
- Copy 6 into the root. Now delete 6 from the right subtree: that node has no left child, so return its right child 7.
- Result `[6,3,7,2,4]`.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- recursive, copy the successor's VALUE (the rule in the question) ----------
def delete_rec(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete_rec(root.left, key)
    elif key > root.val:
        root.right = delete_rec(root.right, key)
    else:
        if root.left is None: return root.right      # leaf or only a right child
        if root.right is None: return root.left      # only a left child
        s = root.right
        while s.left: s = s.left                     # inorder successor
        root.val = s.val                             # copy the value up
        root.right = delete_rec(root.right, s.val)   # then remove the successor node
    return root

# ---------- recursive, RE-LINK: the successor NODE takes the deleted node's place ----------
def delete_relink(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete_relink(root.left, key)
    elif key > root.val:
        root.right = delete_relink(root.right, key)
    else:
        if root.left is None: return root.right
        if root.right is None: return root.left
        s = root.right
        while s.left: s = s.left
        s.right = delete_relink(root.right, s.val)   # s leaves its old spot; its right child is spliced up
        s.left = root.left
        return s                                     # s replaces root; root is now detached
    return root

# ---------- iterative copy-value version (safe on a 10^4-deep skewed tree) ----------
def delete_iter(root, key):
    parent, cur = None, root
    while cur is not None and cur.val != key:
        parent, cur = cur, (cur.left if key < cur.val else cur.right)
    if cur is None:
        return root
    if cur.left and cur.right:
        sp, s = cur, cur.right
        while s.left: sp, s = s, s.left
        cur.val = s.val
        parent, cur = sp, s                          # now delete s, which has no left child
    child = cur.left or cur.right
    if parent is None:
        return child
    if parent.left is cur: parent.left = child
    else: parent.right = child
    return root

# ---------- independent spec on tuples (val, left, right) ----------
def delete_tuple(t, key):
    if t is None: return None
    v, l, r = t
    if key < v: return (v, delete_tuple(l, key), r)
    if key > v: return (v, l, delete_tuple(r, key))
    if l is None: return r
    if r is None: return l
    s = r
    while s[1] is not None: s = s[1]
    return (s[0], l, delete_tuple(r, s[0]))

def inorder_vals(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

def to_tup(root):
    return None if root is None else (root.val, to_tup(root.left), to_tup(root.right))

def run(fn, arr, key):
    return to_arr(fn(build(arr), key))

# examples
base = [5, 3, 6, 2, 4, None, 7]
for arr, key in [(base, 3), (base, 0), ([], 0), (base, 5), ([1], 1)]:
    got = [run(f, arr, key) for f in (delete_rec, delete_relink, delete_iter)]
    assert got[0] == got[1] == got[2]
    print(f"root={arr}, key={key} -> {got[0]}")

# exhaustive: every BST shape with 0..7 nodes (values 0,2,4,..), every key including absent ones
cases = 0
for n in range(8):
    for sh in shapes(n):
        t = label(sh, "in", step=2)
        vals = [2 * i for i in range(n)]
        for key in range(-1, 2 * n + 1):
            spec = delete_tuple(t, key)
            roots = [from_tup(t) for _ in range(3)]
            before = {id(x): x.val for x in nodes_of(roots[0])}
            outs = [delete_rec(roots[0], key), delete_relink(roots[1], key), delete_iter(roots[2], key)]
            for o in outs:
                assert to_tup(o) == spec
                assert inorder_vals(o) == [v for v in vals if v != key]   # still a BST, key gone
            # identity bookkeeping on the copy-value version: exactly one node object disappears (if the key existed)
            after = {id(x) for x in nodes_of(outs[0])}
            assert len(after) == len(before) - (1 if key in vals else 0) and after <= set(before)
            # re-link version: the node object that HELD the key is the one that disappears
            if key in vals:
                holder = next(i for i, v in before.items() if v == key)
                assert holder not in {id(x) for x in nodes_of(outs[1])}
            cases += 1
print("exhaustive cases ok:", cases)

# what a held reference sees
def demo(fn):
    root = build(base)
    n5, n6 = root, root.right
    new_root = fn(root, 5)
    in_tree = {id(x) for x in nodes_of(new_root)}
    return (f"{fn.__name__}: old root object still in tree={id(n5) in in_tree} (val={n5.val}); "
            f"node 6 object still in tree={id(n6) in in_tree} (val={n6.val}); result={to_arr(new_root)}")
print(demo(delete_rec))
print(demo(delete_relink))

# recursion limit: a 1500-node right chain 0..1499, delete the last node
def chain(n):
    root = None
    for i in range(n - 1, -1, -1):
        root = TreeNode(i, None, root)
    return root
try:
    delete_rec(chain(1500), 1499); res = "recursive ok"
except RecursionError:
    res = "recursive RecursionError"
r = delete_iter(chain(1500), 1499)
print(f"1500-node chain, limit {sys.getrecursionlimit()}: {res}; iterative ok, size now {len(nodes_of(r))}")
```

**Output (my run):**
```
root=[5, 3, 6, 2, 4, None, 7], key=3 -> [5, 4, 6, 2, None, None, 7]
root=[5, 3, 6, 2, 4, None, 7], key=0 -> [5, 3, 6, 2, 4, None, 7]
root=[], key=0 -> []
root=[5, 3, 6, 2, 4, None, 7], key=5 -> [6, 3, 7, 2, 4]
root=[1], key=1 -> []
exhaustive cases ok: 9414
delete_rec: old root object still in tree=True (val=6); node 6 object still in tree=False (val=6); result=[6, 3, 7, 2, 4]
delete_relink: old root object still in tree=False (val=5); node 6 object still in tree=True (val=6); result=[6, 3, 7, 2, 4]
1500-node chain, limit 1000: recursive RecursionError; iterative ok, size now 1499
```

Output prints `None` where the prompt writes `null`.

**Edge cases:**
- Empty tree, or key absent: nothing changes (the exhaustive test uses absent keys below, between and above the values).
- Delete the root when it is a leaf, or when it has one child: the child becomes the new root, so always use the returned root.
- Successor is the direct right child: its right subtree is spliced up with no loop.
- Skewed tree: the stated bound is 10^4 nodes, but the recursive version raises `RecursionError` at the default limit of 1000 on a chain (shown above at 1500). Use the iterative version with a parent pointer.

**Follow-ups:**
- Use the predecessor instead? Symmetric: rightmost node of the left subtree. The shape can differ but the result is still a valid BST.
- Duplicates? You need a rule (count on the node, or always send equal keys right) and the delete must remove only one.
- Keep it balanced? Needs rotations (AVL or red-black), a different problem.

**Common mistakes:**
- Not assigning the recursive result back (`root.left = delete(...)`), so the edit is lost.
- Deleting the successor by its position instead of by value from the right subtree, which breaks when the successor is the direct right child.
- Taking the rightmost node of the left subtree for one case and the leftmost of the right for another in the same code.
- Ignoring recursion depth on a skewed input.

### Q32 ⭐⭐ 🟡 Inorder successor in a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is a BST with distinct values and no parent pointers (1 <= n <= 10^5). Given the value p of a node that exists, return the value of the next larger value in the tree, or None when p is the maximum. Walk down from the root in O(h) time and O(1) space: when you go left, remember the node as the best candidate so far; explain why a node with a right child has the minimum of that subtree as its successor and the other case is the lowest ancestor for which p is in the left subtree. Example: root=[2, 1, 3], p=1 -> 2; root=[5, 3, 6, 2, 4, null, null, 1], p=6 -> null; root=[5, 3, 6, 2, 4, null, null, 1], p=4 -> 5; root=[5, 3, 6, 2, 4, null, null, 1], p=2 -> 3; root=[2], p=2 -> null.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** BST descent with a "last left turn" candidate. No parent pointers and no stack needed.

**Say this first (1 line):** "I walk from the root. Every time I go left, the current node is bigger than p, so I remember it. The last one remembered is the answer. O(h) time, O(1) space."

**Brute force:** Inorder traversal into a list, find p, take the next entry. O(n) time and space, ignores the BST property.

**Optimal:**
- Two cases for the successor of a node p:
  - p has a right child: the successor is the minimum of that right subtree (go right once, then left as far as possible).
  - Otherwise it is the lowest ancestor whose LEFT subtree contains p, that is, the last ancestor where the path turned left.
- One loop covers both. If `p < cur.val`, `cur` is a candidate larger than p, so save it and go left. Otherwise go right (equal to p also goes right, which skips p itself and finds the minimum of its right subtree, or falls off the end and keeps the last candidate).
- Invariant: `best` is the smallest value seen so far that is greater than p, and the answer is still inside the subtree at `cur` or equals `best`.
- The walk also answers "next larger than a value that is not in the tree", which the two-case version cannot.

**Complexity:** Time O(h), one node per level, so at most the height (checked below for every node of every tree up to 9 nodes). Space O(1). h is log n when balanced and n when skewed.

**Dry run:** tree `[5,3,6,2,4,null,null,1]`, p = 4.
- At 5: 4 < 5, so best = 5, go left to 3.
- At 3: 4 > 3, go right to 4.
- At 4: not less than 4, go right, which is None. Return best = 5.

p = 6: at 5 go right (6 > 5), at 6 go right, None. best never set, so None.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

def inorder_vals(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

# ---------- brute force: sorted values, then the next one ----------
def succ_brute(root, p):
    vals = inorder_vals(root)                 # O(n) time and space
    i = vals.index(p)
    return vals[i + 1] if i + 1 < len(vals) else None

# ---------- optimal: one walk down, remember the last node where we went left ----------
def succ(root, p, steps=None):
    best, cur = None, root
    while cur is not None:
        if steps is not None: steps[0] += 1
        if p < cur.val:
            best = cur.val                    # cur is bigger than p: a candidate, but maybe a smaller one is deeper
            cur = cur.left
        else:                                 # p >= cur.val: the answer, if any, is strictly to the right
            cur = cur.right
    return best

# ---------- same idea, split into the two textbook cases (finds p first) ----------
def succ_cases(root, p):
    anc, cur = None, root
    while cur.val != p:                       # p is guaranteed to exist
        if p < cur.val: anc, cur = cur, cur.left
        else: cur = cur.right
    if cur.right:                             # case 1: minimum of the right subtree
        cur = cur.right
        while cur.left: cur = cur.left
        return cur.val
    return anc.val if anc else None           # case 2: lowest ancestor whose LEFT subtree holds p

# examples
for arr, p in [([2, 1, 3], 1), ([5, 3, 6, 2, 4, None, None, 1], 6), ([5, 3, 6, 2, 4, None, None, 1], 4),
               ([5, 3, 6, 2, 4, None, None, 1], 2), ([2], 2)]:
    t = build(arr)
    a, b, c = succ(t, p), succ_cases(t, p), succ_brute(t, p)
    assert a == b == c
    print(f"root={arr}, p={p} -> {a}")

# exhaustive: all BST shapes 0..9 nodes, every existing p; also check the step count is at most the height
cases, worst_gap = 0, 0
for n in range(1, 10):
    for sh in shapes(n):
        t = from_tup(label(sh, "in"))
        h = height(t)
        for p in range(n):
            steps = [0]
            got = succ(t, p, steps)
            assert got == succ_brute(t, p) == succ_cases(t, p)
            assert got == (p + 1 if p + 1 < n else None)
            assert steps[0] <= h                          # O(h): never more nodes visited than the height
            worst_gap = max(worst_gap, h - steps[0])
            cases += 1
print("exhaustive cases ok:", cases)

# a p that is NOT in the tree still gets the next larger value (useful follow-up), but only the walk version supports it
t = build([5, 3, 6, 2, 4])
print("next larger than 4.5:", succ(t, 4.5), "| than 1:", succ(t, 1), "| than 9:", succ(t, 9))
```

**Output (my run):**
```
root=[2, 1, 3], p=1 -> 2
root=[5, 3, 6, 2, 4, None, None, 1], p=6 -> None
root=[5, 3, 6, 2, 4, None, None, 1], p=4 -> 5
root=[5, 3, 6, 2, 4, None, None, 1], p=2 -> 3
root=[2], p=2 -> None
exhaustive cases ok: 59279
next larger than 4.5: 5 | than 1: 2 | than 9: None
```

Output prints `None` where the prompt writes `null`.

**Edge cases:**
- p is the maximum: no left turn ever happens on its path, so None.
- Single node: None.
- p is the root with no right child: None. With a right child: minimum of the right subtree.
- Using `p <= cur.val` instead of `<` would save p itself as the answer.

**Follow-ups:**
- Predecessor? Mirror it: remember the node when you go right.
- With parent pointers? Right-subtree minimum, else climb until you come up from a left child.
- Repeated calls on the same tree? Still O(h) each, no preprocessing needed.

**Common mistakes:**
- Returning the first ancestor larger than p instead of the lowest (smallest) one, or not updating `best` on each left turn.
- Using `<=`, so p is its own successor.
- Doing an inorder traversal when O(h) is required.
- Forgetting that the answer may not be in p's subtree at all.

### Q33 ⭐⭐ 🟡 Two sum in a BST. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The tree is a BST with distinct values (1 <= n <= 10^4). Return True if two DIFFERENT nodes have values summing to k (a node cannot be used twice). Give the hash-set solution (O(n) time, O(n) space) and the two-pointer solution that runs an ascending BST iterator and a descending one, which needs only O(h) space (cross-reference the iterator idea in the BST iterator question of this part). Example: root=[5, 3, 6, 2, 4, null, 7], k=9 -> True; root=[5, 3, 6, 2, 4, null, 7], k=28 -> False; root=[1], k=2 -> False; root=[2, 1, 3], k=4 -> True.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Two sum, with the BST's sorted order available. Hash set for speed of writing; two pointers over an ascending and a descending iterator for O(h) space.

**Say this first (1 line):** "Hash set is O(n) time and space. If memory matters I run an ascending iterator and a descending iterator and move them like two pointers, O(n) time and O(h) space."

**Brute force:** Check every pair of nodes, O(n^2) time, O(n) space for the node list.

**Optimal:**
- Hash set: walk the tree once; for each node look up `k - val` among the values already seen, then add the node's value. Looking before adding means a node can never pair with itself, so `k = 2 * val` with one such node correctly gives False.
- Two pointers: inorder is sorted, so the smallest comes from an ascending iterator and the largest from a descending one (the same stack idea as the BST iterator question in this part, with left and right swapped for the descending one). If the sum is too small move the low pointer up, if too big move the high pointer down.
- Stop when the pointers meet: use `a < b` on values. Values are distinct, so `a == b` is the same node.
- Each iterator holds only a stack of at most h nodes.

**Complexity:**
- Set: O(n) time, O(n) space.
- Two pointers: each iterator visits each node at most once, so O(n) time total; space O(h) for two stacks, never deeper than the tree height (checked below). That beats the set when the tree is balanced (h about log n).

**Dry run:** `[5,3,6,2,4,null,7]`, k = 9. Ascending starts at 2, descending at 7. Sum 9, found (2 + 7).
k = 28: 2+7=9 too small, ascending to 3, 3+7=10 ... 6+7=13, then a=7, b=7 is not `a < b`, stop. False.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- brute force: all pairs of different nodes ----------
def two_sum_brute(root, k):
    vals = [n.val for n in nodes_of(root)]
    return any(vals[i] + vals[j] == k for i in range(len(vals)) for j in range(i + 1, len(vals)))

# ---------- hash set, O(n) time and space ----------
def two_sum_set(root, k):
    seen, st = set(), ([root] if root else [])
    while st:
        n = st.pop()
        if k - n.val in seen:                 # the partner was seen earlier, so it is a different node
            return True
        seen.add(n.val)
        if n.left: st.append(n.left)
        if n.right: st.append(n.right)
    return False

# ---------- two pointers: ascending and descending iterators, O(h) space ----------
class BSTIter:
    """Yields values in ascending (asc=True) or descending order with a stack of at most h nodes."""
    def __init__(self, root, asc):
        self.asc, self.st, self.peak = asc, [], 0
        self._push(root)
    def _push(self, node):
        while node:
            self.st.append(node)
            node = node.left if self.asc else node.right
        self.peak = max(self.peak, len(self.st))
    def next(self):
        node = self.st.pop()
        self._push(node.right if self.asc else node.left)
        return node.val

def two_sum_iters(root, k, info=None):
    if root is None: return False
    lo, hi = BSTIter(root, True), BSTIter(root, False)
    a, b = lo.next(), hi.next()
    found = False
    while a < b:                              # strict: the two pointers must be different nodes
        s = a + b
        if s == k: found = True; break
        if s < k:
            if not lo.st: break               # a was the last node on its side
            a = lo.next()
        else:
            if not hi.st: break
            b = hi.next()
    if info is not None: info.append(max(lo.peak, hi.peak))
    return found

# examples
base = [5, 3, 6, 2, 4, None, 7]
for arr, k in [(base, 9), (base, 28), ([1], 2), ([2, 1, 3], 4)]:
    t = build(arr)
    a, b, c = two_sum_set(t, k), two_sum_iters(t, k), two_sum_brute(t, k)
    assert a == b == c
    print(f"root={arr}, k={k} -> {a}")

# exhaustive: all BST shapes 0..8 nodes (values 0,3,6,...), every k from -1 to 3n+3
cases, trues = 0, 0
for n in range(1, 9):
    for sh in shapes(n):
        t = from_tup(label(sh, "in", step=3))
        h = height(t)
        for k in range(-1, 3 * n + 4):
            info = []
            a, b, c = two_sum_set(t, k), two_sum_iters(t, k, info), two_sum_brute(t, k)
            assert a == b == c, (n, k)
            assert info[0] <= h                           # stack never deeper than the height
            cases += 1; trues += a
print("exhaustive cases ok:", cases, "(True in", trues, ")")

# the 'same node twice' trap: single node 2, k=4 must be False
assert two_sum_set(build([2]), 4) is False and two_sum_iters(build([2]), 4) is False
# random BSTs with negatives and a bigger size
random.seed(5)
def random_bst(n):
    vals = random.sample(range(-60, 60), n)
    root = None
    for v in vals:
        if root is None: root = TreeNode(v); continue
        cur = root
        while True:
            nxt = "left" if v < cur.val else "right"
            if getattr(cur, nxt) is None: setattr(cur, nxt, TreeNode(v)); break
            cur = getattr(cur, nxt)
    return root
for _ in range(300):
    t = random_bst(random.randint(1, 30)); k = random.randint(-100, 100)
    assert two_sum_set(t, k) == two_sum_iters(t, k) == two_sum_brute(t, k)
print("300 random BSTs with negatives ok")
```

**Output (my run):**
```
root=[5, 3, 6, 2, 4, None, 7], k=9 -> True
root=[5, 3, 6, 2, 4, None, 7], k=28 -> False
root=[1], k=2 -> False
root=[2, 1, 3], k=4 -> True
exhaustive cases ok: 56838 (True in 17565 )
300 random BSTs with negatives ok
```

Output prints `None` where the prompt writes `null`.

**Edge cases:**
- One node: False for every k (including `2 * val`).
- Negative values, zero: nothing in the logic assumes positive values.
- k that needs the same value twice: only counts if two different nodes hold it, which distinct values rule out.
- Skewed tree: the two-pointer stack grows to n, same as the set's space. The O(h) win needs a reasonably balanced tree.

**Follow-ups:**
- Same problem on a plain binary tree? Only the hash set works (no order).
- Three sum in a BST? Fix a node, run two sum on the rest: O(n^2).
- Why not flatten to a list and two-pointer? O(n) space, which is what the iterators avoid.

**Common mistakes:**
- Adding to the set before the lookup, so a node pairs with itself.
- Stopping the pointer loop with `a <= b`.
- Forgetting that the descending iterator goes right first, then left.
- Claiming O(h) space for a skewed tree.

### Q34 ⭐⭐ 🟡 Count the nodes of a complete binary tree. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). The input is guaranteed to be a COMPLETE binary tree (every level full except possibly the last, whose nodes are as far left as possible), 0 <= n <= 5*10^4. Beat the O(n) traversal: compute the leftmost depth and the rightmost depth from a node; if they are equal the subtree is perfect and has 2^depth - 1 nodes, otherwise recurse into both children. Show that this takes O(log^2 n) time, and that the number of spine steps (executions of `cur = cur.left` or `cur = cur.right` inside the two depth helpers; the recursive calls themselves are not counted) is at most 2h^2 where h = floor(log2(n)) for n >= 1 (for a perfect tree, n = 2^(h+1) - 1, it is exactly 2h; the worst case over all n with that h is n = 2^(h+1) - 2, with exactly h(2h - 1) steps for h >= 2), which the tests check for every n up to 2^11 and, for every h up to 13, at the boundary cases n = 2^h, n = 2^(h+1) - 2 and n = 2^(h+1) - 1. The tests use the builder, so the arrays below are complete trees. Example: root=[1, 2, 3, 4, 5, 6] -> 6; root=[] -> 0; root=[1] -> 1; root=[1, 2, 3, 4, 5, 6, 7] -> 7; root=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] -> 10.
**Asked at:** Count-complete-tree-nodes write-ups (jointaro company-tagged page, doocs, vultr, interviewing.io, a Substack solution post titled with Amazon; snippets only, not opened: compare left and right depths, O(log^2 n)) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Use the structure guarantee. In a complete tree, comparing the leftmost and rightmost depths tells you whether a subtree is perfect, and a perfect subtree is counted by a formula.

**Say this first (1 line):** "I compare the left-spine depth and right-spine depth. Equal means a perfect subtree, so 2^(d+1) - 1 nodes with no more work. Otherwise I recurse on both children. O(log^2 n)."

**Brute force:** Any traversal, O(n) time, O(h) to O(n) space. It ignores the completeness guarantee.

**Optimal:**
- `left_depth(node)` counts steps down the left spine, `right_depth(node)` down the right spine.
- Equal depths in a complete tree means every level down to that depth is full, so the subtree has `2^(d+1) - 1` nodes.
- Unequal: the node is not perfect, so the answer is `1 + count(left) + count(right)`.
- Why only one side keeps recursing: the last level is filled from the left. At any non-perfect node, either the left child is perfect (the last level reaches only into the right subtree) or the right child is perfect (one level shorter) and the left one is not. A perfect child returns after its two spine walks, so only ONE branch goes deeper.

**Complexity:**
- The recursion visits at most h + 1 nodes down one path, and each visit does two spine walks of at most h steps. So O(h * h) = O(log^2 n). The extra cost over the formula is only the walks.
- Space: O(h) recursion = O(log n).
- The question's exact claim holds, and I tested it, not just reasoned it. With steps = executions of `node = node.left` or `node = node.right` in the two helpers, h = floor(log2 n): for every n from 1 to 2^11 the steps are at most 2h^2; a perfect tree (n = 2^(h+1) - 1) costs exactly 2h; and for h = 2..10 the maximum over all n with that h is at n = 2^(h+1) - 2 with exactly h(2h - 1). The boundary cases n = 2^h, 2^(h+1) - 2 and 2^(h+1) - 1 also pass for every h from 1 to 13 (table below). No problem found with the stated bounds.

**Dry run:** `[1,2,3,4,5,6]` (6 nodes).
- Root: left depth 2 (1 -> 2 -> 4), right depth 1 (1 -> 3). Not equal, so 1 + count(2) + count(3).
- Node 2: left depth 1, right depth 1, perfect: 3 nodes.
- Node 3: left depth 1 (3 -> 6), right depth 0, not equal: 1 + count(6) + count(None). Node 6 is a leaf, 1 node.
- Total 1 + 3 + 2 = 6.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- brute force: O(n) BFS count ----------
def count_brute(root):
    return len(nodes_of(root))

# ---------- optimal: perfect subtrees counted by formula; steps = executions of cur = cur.left / cur.right ----------
STEPS = [0]

def left_depth(node):
    d = 0
    while node.left:
        node = node.left; d += 1; STEPS[0] += 1
    return d

def right_depth(node):
    d = 0
    while node.right:
        node = node.right; d += 1; STEPS[0] += 1
    return d

def count_complete(node):
    if node is None:
        return 0
    l, r = left_depth(node), right_depth(node)
    if l == r:
        return (1 << (l + 1)) - 1             # perfect subtree of height l: 2^(l+1) - 1 nodes
    return 1 + count_complete(node.left) + count_complete(node.right)

def run(n):
    STEPS[0] = 0
    root = build(list(range(1, n + 1)))       # level-order 1..n is exactly a complete tree with n nodes
    return count_complete(root), STEPS[0], root

# examples
for arr in ([1, 2, 3, 4, 5, 6], [], [1], [1, 2, 3, 4, 5, 6, 7], list(range(1, 11))):
    root = build(arr)
    assert count_complete(root) == count_brute(root) == len(arr)
    print(f"root={arr} -> {count_complete(root)}")

# every n up to 2^11: count is right, steps <= 2h^2, and the maximum per h is where the question says
max_steps = {}
for n in range(1, 2 ** 11 + 1):
    cnt, steps, root = run(n)
    assert cnt == n
    h = n.bit_length() - 1                    # floor(log2 n)
    assert steps <= 2 * h * h, (n, steps)
    if n == 2 ** (h + 1) - 1:
        assert steps == 2 * h                 # perfect tree: exactly one left and one right spine
    if h < 11 and steps > max_steps.get(h, (-1, 0))[1]:   # h = 11 has only n = 2^11 in range, so no maximum is taken there
        max_steps[h] = (n, steps)
for h in range(2, 11):
    n_star, s = max_steps[h]
    assert n_star == 2 ** (h + 1) - 2 and s == h * (2 * h - 1), (h, n_star, s)
print("all n <= 2^11: count ok, steps <= 2h^2 ok, perfect n gives 2h, worst n = 2^(h+1)-2 gives h(2h-1) for h=2..10")

# boundary cases for every h up to 13
rows = []
for h in range(1, 14):
    for n in (2 ** h, 2 ** (h + 1) - 2, 2 ** (h + 1) - 1):
        cnt, steps, _ = run(n)
        assert cnt == n and steps <= 2 * h * h
        if n == 2 ** (h + 1) - 1: assert steps == 2 * h
        if n == 2 ** (h + 1) - 2 and h >= 2: assert steps == h * (2 * h - 1)
        rows.append((h, n, steps))
print("spine steps by h:  n=2^h   n=2^(h+1)-2   n=2^(h+1)-1   2h^2")
by_h = {}
for h, n, s in rows: by_h.setdefault(h, []).append(s)
for h in (1, 2, 3, 5, 8, 13):
    a, b, c = by_h[h]
    print(f"h={h:<2}              {a:>6} {b:>12} {c:>13} {2*h*h:>6}")

# h = 1 for reference (n = 2 and 3), and an empty tree costs nothing
print("n=2 steps:", run(2)[1], "| n=3 steps:", run(3)[1], "| empty:", count_complete(None))
```

**Output (my run):**
```
root=[1, 2, 3, 4, 5, 6] -> 6
root=[] -> 0
root=[1] -> 1
root=[1, 2, 3, 4, 5, 6, 7] -> 7
root=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] -> 10
all n <= 2^11: count ok, steps <= 2h^2 ok, perfect n gives 2h, worst n = 2^(h+1)-2 gives h(2h-1) for h=2..10
spine steps by h:  n=2^h   n=2^(h+1)-2   n=2^(h+1)-1   2h^2
h=1                    1            1             2      2
h=2                    4            6             4      8
h=3                   11           15             6     18
h=5                   37           45            10     50
h=8                  106          120            16    128
h=13                 301          325            26    338
n=2 steps: 1 | n=3 steps: 2 | empty: 0
```

Output prints `None` where the prompt writes `null`. The builder turns the array `1..n` into the complete tree with n nodes, which is why the tests can use it for every n.

**Edge cases:**
- Empty tree: 0, handled before any depth call.
- One node: both depths 0, so 2^1 - 1 = 1.
- Perfect tree: answered at the root, 2h steps and no recursion.
- n = 2^h (one node on the last level) and n = 2^(h+1) - 2 (one missing node): the extremes for the step count.
- If the input is not complete, the formula is simply wrong. The guarantee is part of the contract.

**Follow-ups:**
- Binary search on the last level (go to the node by bits of its index) is the other O(log^2 n) method.
- Can you do better than log^2 n? Not by this route. The count needs about log n probes, each costing a root-to-leaf walk.
- Compare with a heap: the same completeness is what lets a heap live in an array.

**Common mistakes:**
- Writing `2 ** d - 1` when d counts edges (it should be `2^(d+1) - 1`) or off by one on the depth definition.
- Comparing only the left depth of the two children instead of the left and right spines of the same node.
- Assuming the answer is O(log n); it is O(log^2 n).
- Using it on a tree that is merely balanced, not complete.

### Q35 ⭐⭐ 🟡 Deep skewed trees and the recursion limit. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Build a skewed tree of n nodes (shape 'left': every node has only a left child; shape 'right': only a right child), then compute its depth two ways: with a plain recursive function and with an explicit stack. Return the pair (recursive_result, iterative_result) where recursive_result is the string 'RecursionError' if Python's default limit (1000) stops it. Build the tree iteratively too, since recursive construction fails the same way. Explain why raising the limit with `sys.setrecursionlimit` is not a fix for 10^5 nodes (the C stack can overflow), what a depth of n costs in memory, and which iterative template (Part 4 Q25; for linked lists Part 6 Q26) you would use. Do not hard-code the exact failing depth: it depends on the interpreter, and the examples use n = 500 and n = 2000, far from it. Example: n=500, shape='left' -> (500, 500); n=2000, shape='right' -> ('RecursionError', 2000); n=1, shape='left' -> (1, 1); n=0, shape='left' -> (0, 0).
**Asked at:** Python recursion-limit explainers (techinterview.org depth-of-a-tree page, a OneUptime guide, DataCamp DFS tutorial; snippets only, not opened: default limit 1000, raising it risks a crash, explicit stack preferred) | Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND)

**Pattern:** Recursion depth equals tree height, and Python's call stack is small. A skewed tree has height n, so use an explicit stack.

**Say this first (1 line):** "A skewed tree makes the recursion n deep, and Python stops at 1000 frames by default, so I use an explicit stack: O(n) time, O(n) space for a chain but no call-stack limit."

**Brute force:** The plain recursive `1 + max(depth(left), depth(right))`. Correct, O(n) time, but O(h) call-stack frames. On a chain of n nodes that is n frames, and it raises `RecursionError` once n is past the interpreter's limit.

**Optimal:**
- Build iteratively too: a loop that wraps the previous root in a new node. A recursive builder fails at the same depth.
- Depth with an explicit stack of `(node, depth_so_far)` pairs: pop, record the max, push the children. No recursion at all.
- Why the explicit stack still costs O(h) memory: the stack holds the pending nodes. On a chain it holds one at a time (the stack never grows), on a balanced tree it holds about h. A level-order BFS holds up to one level, so it is the better choice for a very bushy tree.
- Cost of depth n in memory: each live Python frame needs memory of its own. I measured about 100 bytes or more per frame on this sandbox (10 MB for 10^5 frames, roughly 107 MB for 10^6; sandbox-only, interpreter and version dependent). The node objects themselves cost memory on top.
- Which template: the explicit-stack traversal from Part 4 Q25 for trees; for a long linked list the iterative walk from Part 6 Q26 (a chain is the same shape).

**Complexity:** Both versions are O(n) time. Recursive: O(h) stack, which is O(n) in the worst case and fails at the limit. Iterative: O(h) heap memory for the stack, with no recursion limit to hit.

**On `sys.setrecursionlimit`. The prompt's claim is only partly true.** I ran it. On this Python 3.13.17, raising the limit made plain pure-Python recursion succeed on 10^5 and even 10^6 nodes (rc 0, no crash; see the output). So "the C stack will overflow at 10^5" is NOT correct for pure-Python recursion on 3.13: since 3.12, Python-to-Python calls do not consume the C stack, and the cost is heap memory. It is still a bad habit, for these reasons:
- Older interpreters (3.11 and earlier) use the C stack for Python calls and can segfault when the limit is raised too far.
- Recursion that passes through C code (a `functools.lru_cache` wrapper, `sorted` with a key function, `__eq__`, `repr`, JSON) is held to a separate, fixed C recursion limit. I tried a recursive function wrapped in `lru_cache` with the limit raised to 10^7 and it passed at depth 1000 and raised `RecursionError` at depth 10^5 (both in the output).
- You have to guess a safe number, and an interviewer will ask what happens at depth 10^6.
- Memory still grows with the depth.

So the honest interview line: raising the limit can work on newer CPython for pure-Python code, but depends on version and call path; the explicit stack always works.

**Dry run:** chain `3 -> 2 -> 1` (left skewed, n = 3). Stack `[(3, 1)]`: pop, best = 1, push `(2, 2)`. Pop, best = 2, push `(1, 3)`. Pop, best = 3, no children. Stack empty, answer 3. The recursive version reaches 3 frames deep, and for n = 2000 it needs 2000.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

import subprocess

def skewed(n, shape):
    """Iterative build: no recursion, so building never hits the limit."""
    root = None
    for i in range(n):
        root = TreeNode(i, root, None) if shape == "left" else TreeNode(i, None, root)
    return root

def depth_rec(node):
    return 0 if node is None else 1 + max(depth_rec(node.left), depth_rec(node.right))

def depth_iter(root):
    best, st = 0, ([(root, 1)] if root else [])
    while st:
        node, d = st.pop()
        best = max(best, d)
        if node.left: st.append((node.left, d + 1))
        if node.right: st.append((node.right, d + 1))
    return best

def depth_pair(n, shape):
    root = skewed(n, shape)
    try:
        rec = depth_rec(root)
    except RecursionError:
        rec = "RecursionError"
    return rec, depth_iter(root)

for n, shape in [(500, "left"), (2000, "right"), (1, "left"), (0, "left")]:
    print(f"n={n}, shape={shape!r} -> {depth_pair(n, shape)}")

# cross-check: both shapes, many sizes, recursive and iterative agree wherever recursion survives
limit = sys.getrecursionlimit()
for shape in ("left", "right"):
    for n in list(range(0, 60)) + [300, 500, 900]:
        assert depth_pair(n, shape) == (n, n)
    for n in (1500, 2000, 5000):
        assert depth_pair(n, shape) == ("RecursionError", n)    # far above the default limit
# a mixed zig-zag chain too (the node's one child alternates sides)
z = None
for i in range(1200):
    z = TreeNode(i, z, None) if i % 2 else TreeNode(i, None, z)
assert depth_iter(z) == 1200
print(f"default recursion limit {limit}; recursive fails on 1500+ nodes, iterative never does")

# what does raising the limit really do? Run each probe in a fresh interpreter, so a crash could not hurt this script.
PROBE = """
import sys, resource
sys.setrecursionlimit(10**7)
class N:
    __slots__ = ('left',)
    def __init__(self, left=None): self.left = left
n = int(sys.argv[1])
root = None
for _ in range(n): root = N(root)
def depth(x): return 0 if x is None else 1 + depth(x.left)
before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(depth(root), (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - before) // 1024, "MB extra")
"""
for n in (10**5, 10**6):
    r = subprocess.run([sys.executable, "-I", "-c", PROBE, str(n)], capture_output=True, text=True)
    print(f"limit raised, pure-Python recursion on {n} nodes: rc={r.returncode}", r.stdout.strip() or r.stderr.strip()[-80:])
print("python", sys.version.split()[0])

# recursion that passes through a C wrapper (lru_cache) has its own fixed limit, whatever setrecursionlimit says
PROBE2 = """
import sys, functools
sys.setrecursionlimit(10**7)
@functools.lru_cache(maxsize=None)
def f(n): return 0 if n == 0 else 1 + f(n - 1)
try:
    print(f(int(sys.argv[1])))
except RecursionError:
    print("RecursionError")
"""
for n in (1000, 10**5):
    r = subprocess.run([sys.executable, "-I", "-c", PROBE2, str(n)], capture_output=True, text=True)
    print(f"limit raised to 10^7, lru_cache recursion depth {n}: rc={r.returncode}", r.stdout.strip())
```

**Output (my run):**
```
n=500, shape='left' -> (500, 500)
n=2000, shape='right' -> ('RecursionError', 2000)
n=1, shape='left' -> (1, 1)
n=0, shape='left' -> (0, 0)
default recursion limit 1000; recursive fails on 1500+ nodes, iterative never does
limit raised, pure-Python recursion on 100000 nodes: rc=0 100000 10 MB extra
limit raised, pure-Python recursion on 1000000 nodes: rc=0 1000000 107 MB extra
python 3.13.17
limit raised to 10^7, lru_cache recursion depth 1000: rc=0 1000
limit raised to 10^7, lru_cache recursion depth 100000: rc=0 RecursionError
```

The exact failing depth is not hard-coded: the examples use n = 500 and n = 2000, and the cross-check only asserts failure at 1500 or more.

**Edge cases:**
- n = 0: empty tree, depth 0 both ways.
- n = 1: one frame, no issue.
- Shape right versus left: the recursion fails the same way. A zig-zag chain also has height n.
- A balanced tree of a million nodes has depth about 20, so recursion is fine there. The danger is height, not size.

**Follow-ups:**
- Freeing a huge chain: CPython deallocates nested objects with a guard (the "trashcan"), so dropping the root does not blow the stack. Do not rely on that for your own recursive `__del__`.
- Run the recursion in a thread with a bigger stack (`threading.stack_size`)? Possible, a hack. Use the explicit stack.
- Post-order or inorder without recursion? Same idea with a pointer and a visited flag, see the traversal questions in this part.

**Common mistakes:**
- Building the deep tree recursively, so the test fails before the algorithm runs.
- Catching `RecursionError` and calling that a solution.
- Raising the limit with no memory or version caveat.
- Using `list.pop(0)` as a queue in the BFS alternative (O(n) per pop; use `deque`).

### Q36 ⭐⭐ 🟡 Flatten a binary tree to a linked list. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Rearrange the tree IN PLACE so that every node's `right` points to the next node in preorder and every `left` is None (the same node objects, checked by identity; the structure is the singly linked list of Part 6 with `right` playing `next`; see Part 6 Q17 for the identity conventions). 0 <= n <= 2000. Give the recursive version, the reversed-postorder version with a `prev` pointer, and the O(1)-extra-space version that, for each node with a left child, hangs the right subtree under the rightmost node of the left subtree. The example shows the values along the right chain. Example: root=[1, 2, 5, 3, 4, null, 6] -> [1, 2, 3, 4, 5, 6]; root=[] -> []; root=[0] -> [0]; root=[1, null, 2, 3] -> [1, 2, 3].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Pointer surgery on a tree, using preorder as the target order. The flattened tree is a singly linked list that reuses `right` as `next`.

**Say this first (1 line):** "The target is preorder, so every node's right should point to its preorder successor. I'll do it in place with the same node objects, and the O(1)-space way is: hang the right subtree under the rightmost node of the left subtree, then move the left subtree to the right."

**Brute force:** Collect the nodes in preorder into a list (O(n) space), then link `nodes[i].right = nodes[i+1]` and set every `left = None`. In place and correct, but with O(n) extra space. Building new nodes from the values would be correct on values and wrong on identity.

**Optimal:**
- Recursive, return the tail: flatten the left and right subtrees, each call returning the last node of its flattened chain. If the left chain exists, link its tail to the old right subtree, move the left chain to `right`, set `left = None`. The tail is the right chain's tail if there is one, else the left tail, else the node itself. O(n), because no chain is walked a second time. (A version that walks to the end of the left chain each time would be O(n^2) on a left-skewed tree.)
- Reversed postorder with `prev`: visit right, then left, then the node. At that moment `prev` is the node that comes next in preorder, so set `node.right = prev`, `node.left = None`, `prev = node`. Short, but recursive.
- O(1) extra space (no stack): for each node `cur` with a left child, find the rightmost node `p` of the left subtree. Preorder says the right subtree comes right after that node, so `p.right = cur.right`. Then `cur.right = cur.left`, `cur.left = None`, move to `cur.right`.
- Invariant for the O(1) version: the nodes before `cur` already form a flat chain that ends at `cur`, and the whole rest of the tree hangs below `cur` with its preorder unchanged.

**Complexity:**
- Recursive and reversed-postorder: O(n) time, O(h) recursion space.
- O(1) version: O(n) time in total (each node is passed over as `cur` once, and each left subtree's right spine is walked once), O(1) extra space. For n up to 2000 the recursion in the first two is safe on balanced trees but a left chain 2000 deep exceeds Python's default limit, so prefer the O(1) version for deep inputs.

**Dry run:** `[1,2,5,3,4,null,6]`, O(1) version.
- cur = 1: left is 2. Rightmost of the left subtree (2 -> 4) is 4. `4.right = 5`; `1.right = 2`; `1.left = None`. Now 1 -> 2 (left 3, right 4 -> 5 -> 6).
- cur = 2: left is 3, rightmost is 3. `3.right = 4`; `2.right = 3`; `2.left = None`. Now 1 -> 2 -> 3 -> 4 -> 5 -> 6 (5's right is 6 already).
- The rest have no left child. Chain `[1,2,3,4,5,6]`.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# Each version works in place on the same node objects: right = next in preorder, left = None.

def flatten_rec(root):
    """Recursive: each call flattens its subtree and returns the TAIL, so splicing needs no extra walk (O(n) total)."""
    def go(node):
        if node is None:
            return None
        left_tail = go(node.left)
        right_tail = go(node.right)
        if left_tail:                             # splice the flattened left chain between node and its old right
            left_tail.right = node.right
            node.right, node.left = node.left, None
        return right_tail or left_tail or node
    go(root)
    return root

def flatten_prev(root):
    """Reversed postorder (right, left, node) with a prev pointer: each node links to the one that follows it in preorder."""
    prev = None
    def go(node):
        nonlocal prev
        if node is None: return
        go(node.right)
        go(node.left)
        node.right, node.left = prev, None
        prev = node
    go(root)
    return root

def flatten_o1(root):
    """O(1) extra space (Morris style): hang the right subtree under the rightmost node of the left subtree."""
    cur = root
    while cur:
        if cur.left:
            p = cur.left
            while p.right: p = p.right
            p.right = cur.right
            cur.right, cur.left = cur.left, None
        cur = cur.right
    return root

def preorder_ids(root):
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(id(n))
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def chain(root, cap=10**6):
    """Values along the right chain; every left must be None. The cap stops a cycle."""
    out = []
    while root is not None:
        assert root.left is None, "left pointer left behind"
        out.append(root.val)
        root = root.right
        assert len(out) <= cap, "cycle"
    return out

def brute(root):
    """Not in place: new nodes from the preorder values (fails the identity requirement, kept as a value checker)."""
    vals = [n.val for n in nodes_of(root)]
    head = None
    for v in reversed(vals): head = TreeNode(v, None, head)
    return head

def check(fn, arr):
    root = build(arr)
    ids = preorder_ids(root)
    vals = [n.val for n in nodes_of(root)]
    out = fn(root)
    assert out is root or root is None
    assert chain(out) == vals                                   # values in preorder
    assert [id(n) for n in nodes_of(out)] == ids                # SAME node objects, in preorder order
    return chain(out)

for arr in ([1, 2, 5, 3, 4, None, 6], [], [0], [1, None, 2, 3]):
    res = [check(f, arr) for f in (flatten_rec, flatten_prev, flatten_o1)]
    assert res[0] == res[1] == res[2] == chain(brute(build(arr)))
    print(f"root={arr} -> {res[0]}")

# exhaustive: every tree shape with 0..7 nodes, all three versions, identity checked
cases = 0
for n in range(8):
    for sh in shapes(n):
        arr = to_arr(from_tup(label(sh, "pre")))
        for f in (flatten_rec, flatten_prev, flatten_o1):
            check(f, arr)
        cases += 1
print("exhaustive shapes ok:", cases)

# random bigger trees (n up to 300), identity checked, with the O(1)-space version
random.seed(11)
for _ in range(300):
    n = random.randint(0, 300)
    root = None if n == 0 else TreeNode(0)
    pool = [root] if root else []
    for i in range(1, n):
        par = random.choice(pool)
        side = random.choice(("left", "right"))
        if getattr(par, side) is None:
            c = TreeNode(i); setattr(par, side, c); pool.append(c)
    arr = to_arr(root)
    for f in (flatten_rec, flatten_prev, flatten_o1):
        check(f, arr)
print("300 random trees ok")
```

**Output (my run):**
```
root=[1, 2, 5, 3, 4, None, 6] -> [1, 2, 3, 4, 5, 6]
root=[] -> []
root=[0] -> [0]
root=[1, None, 2, 3] -> [1, 2, 3]
exhaustive shapes ok: 626
300 random trees ok
```

The test checks identity: for every shape up to 7 nodes (626 shapes) and 300 random trees, the node objects along the right chain are exactly the original nodes in preorder order, and every `left` is None. The chain walker has a cap and the node collector has a visited-id guard, so an accidental cycle or aliasing fails loudly instead of looping.

**Edge cases:**
- Empty tree: return None.
- Only left children: the whole left chain slides to the right.
- Only right children: already flat, nothing changes.
- Node with a left child whose rightmost node is deep: the walk to `p` is what the O(1) version pays.
- Forgetting `left = None` leaves a hidden second path, so it is not a list.

**Follow-ups:**
- Flatten to inorder (a sorted doubly-linked list)? Different target, same pointer-surgery family; the BST-to-doubly-linked-list variant is the usual one.
- Why is this not the same as the linked-list questions in Part 6? The structure is the same list, but the work is a tree walk that must preserve every node.
- Verify it? Compare node identity, not only values, as the test above does.

**Common mistakes:**
- Saving `cur.right` after you have overwritten it, losing the right subtree.
- Setting `cur.right = cur.left` before linking the rightmost node, which loses the old right subtree.
- Leaving `left` pointers set.
- Building new nodes, which fails an identity check.

### Q37 ⭐⭐ 🟡 All nodes at distance K. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Values are distinct, 1 <= n <= 500. Given the value `target` of a node and an integer k >= 0, return the sorted list of values of all nodes exactly k EDGES from the target, going up through parents as well as down. A tree has no parent pointers, so first record parent links in a dict (or write the target-first recursion that returns the distance upward), then run a BFS outward with a visited set; BFS on general graphs belongs to Part 9. Explain why the visited set is needed in a tree (the parent link points back). Example: root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], target=5, k=2 -> [1, 4, 7]; root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], target=5, k=0 -> [5]; root=[3, 5, 1, 6, 2, 0, 8, null, null, 7, 4], target=5, k=3 -> [0, 8]; root=[1], target=1, k=3 -> [].
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Treat the tree as an undirected graph by adding parent links, then BFS outward from the target for exactly k layers.

**Say this first (1 line):** "A node's neighbours are left, right and parent. The tree has no parent pointers, so I record them in a dict first, then BFS k layers from the target with a visited set. O(n)."

**Brute force:** For every node compute the path from the root, work out its distance to the target (up to the lowest common ancestor, then down), keep those at exactly k. O(n * h). The code uses this as the independent checker: path strings `L`/`R`, distance = `len(a) + len(b) - 2 * common_prefix`.

**Optimal:**
- Pass 1: iterative DFS to fill `parent[node]` (the dict key is the node object, hashed by identity, so equal values in different nodes would not clash; values are distinct here anyway) and to find the target node.
- Pass 2: BFS from the target node. Each layer expands to `left`, `right` and `parent` of every frontier node. After k layers the frontier is the answer; sort the values.
- Why the visited set: the parent link points back to where you came from. Without `seen`, layer 2 from a leaf returns the leaf itself (the output shows target 2, k = 2 on `[1,2,3]` returning `[2, 3]` instead of `[3]`).
- Alternative, target-first recursion with no parent dict: `go(node)` returns the distance from `node` down to the target (or -1). When the target is found, collect nodes k below it. On the way back up, at an ancestor that is d + 1 from the target, either it is the answer (d + 1 == k) or collect nodes k - d - 2 below its OTHER child. O(n) time, O(h) space.
- BFS on general graphs is Part 9. Here the graph is a tree, so there are no cycles other than the back edge to the parent.

**Complexity:** Time O(n): parent pass O(n), BFS touches each node at most once (visited set), sorting the answer is O(m log m) for m results. Space O(n) for the dict and the visited set; the recursive alternative is O(h).

**Dry run:** the big example, target 5, k = 2. Neighbours of 5: 6, 2 and its parent 3. Layer 2: from 6 nothing new (children none, parent 5 is seen); from 2: 7 and 4; from 3: 1 (5 is seen). Frontier `[7, 4, 1]`, sorted `[1, 4, 7]`.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- brute force: path-string distance for every node (independent of the algorithms) ----------
def dist_k_brute(root, target, k):
    out = []
    def walk(node, path):
        if node is None: return
        out.append((node.val, path))
        walk(node.left, path + "L"); walk(node.right, path + "R")
    walk(root, "")
    tpath = next(p for v, p in out if v == target)
    def dist(a, b):
        c = 0
        while c < min(len(a), len(b)) and a[c] == b[c]: c += 1
        return len(a) + len(b) - 2 * c         # up from a to the common ancestor, down to b
    return sorted(v for v, p in out if dist(p, tpath) == k)

# ---------- optimal 1: parent links + BFS outward with a visited set ----------
def dist_k_bfs(root, target, k):
    parent, st, start = {root: None}, [root], None
    while st:                                  # iterative DFS to record parents (dict keys are node identities)
        n = st.pop()
        if n.val == target: start = n
        for c in (n.left, n.right):
            if c: parent[c] = n; st.append(c)
    seen, frontier = {start}, [start]
    for _ in range(k):
        nxt = []
        for n in frontier:
            for m in (n.left, n.right, parent[n]):
                if m is not None and m not in seen:    # without 'seen' the parent link walks straight back
                    seen.add(m); nxt.append(m)
        frontier = nxt
    return sorted(n.val for n in frontier)

# ---------- optimal 2: target-first recursion, returns distance to the target (or -1) ----------
def dist_k_rec(root, target, k):
    out = []
    def down(node, d):                         # collect nodes exactly d below node
        if node is None or d < 0: return
        if d == 0: out.append(node.val); return
        down(node.left, d - 1); down(node.right, d - 1)
    def go(node):                              # distance from node to target if target is inside, else -1
        if node is None: return -1
        if node.val == target:
            down(node, k); return 0
        for near, far in ((node.left, node.right), (node.right, node.left)):
            d = go(near)
            if d >= 0:
                if d + 1 == k: out.append(node.val)
                else: down(far, k - d - 2)     # the other side starts one edge further away
                return d + 1
        return -1
    go(root)
    return sorted(out)

big = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
for arr, t, k in [(big, 5, 2), (big, 5, 0), (big, 5, 3), ([1], 1, 3)]:
    r = build(arr)
    a, b, c = dist_k_bfs(r, t, k), dist_k_rec(r, t, k), dist_k_brute(r, t, k)
    assert a == b == c
    print(f"root={arr}, target={t}, k={k} -> {a}")

# exhaustive: every shape with 1..7 nodes (distinct preorder labels), every target, k = 0..8
cases = 0
for n in range(1, 8):
    for sh in shapes(n):
        r = from_tup(label(sh, "pre"))
        for t in range(n):
            for k in range(0, 9):
                a, b, c = dist_k_bfs(r, t, k), dist_k_rec(r, t, k), dist_k_brute(r, t, k)
                assert a == b == c, (n, t, k)
                cases += 1
print("exhaustive cases ok:", cases)

# the visited set matters: without it, k = 2 from a leaf comes back to the leaf itself
def bfs_no_seen(root, target, k):
    parent, st, start = {root: None}, [root], None
    while st:
        n = st.pop()
        if n.val == target: start = n
        for c in (n.left, n.right):
            if c: parent[c] = n; st.append(c)
    frontier = [start]
    for _ in range(k):
        frontier = [m for n in frontier for m in (n.left, n.right, parent[n]) if m is not None]
    return sorted(n.val for n in frontier)
r = build([1, 2, 3])
print("target 2, k=2: with seen", dist_k_bfs(r, 2, 2), "| without seen", bfs_no_seen(r, 2, 2))
```

**Output (my run):**
```
root=[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target=5, k=2 -> [1, 4, 7]
root=[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target=5, k=0 -> [5]
root=[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target=5, k=3 -> [0, 8]
root=[1], target=1, k=3 -> []
exhaustive cases ok: 36729
target 2, k=2: with seen [3] | without seen [2, 3]
```

Output prints `None` where the prompt writes `null`. The exhaustive test runs every shape with 1 to 7 nodes, every target and k from 0 to 8 (so k larger than the tree, which must give `[]`), against the path-string brute force.

**Edge cases:**
- k = 0: just the target.
- k larger than the tree can reach: empty list.
- Target is the root: no parent; `parent[root]` is None, which the loop skips.
- Target is a leaf: the answer mostly lies up and across.
- Single node with k > 0: `[]`.

**Follow-ups:**
- Time to burn the whole tree from a node? Same BFS, count layers until the frontier is empty.
- Values not distinct? Pass the target node (a reference), not a value; the dict keyed by node already supports that.
- Why a list `frontier` and not a deque? Layers are replaced whole each round, so no `pop(0)` is needed.

**Common mistakes:**
- No visited set, so the BFS walks back to the parent and double counts.
- Treating distance as depth below the target only, missing ancestors.
- Off-by-one when going up in the recursive version (the other child is one extra edge away).
- Returning unsorted values when the question asks for sorted ones.

### Q38 ⭐⭐ 🟡 Serialize and deserialize with BFS. Nodes are `TreeNode(val, left, right)`; examples write a tree as a level-order array with null for a missing child (the children of a null are not listed). Use the level-order format: tokens are joined by commas; start with the root; for each non-null node taken from a queue emit its left child then its right child, writing '#' for a missing child and appending non-null children to the queue; stop when the queue is empty; never trim trailing markers. So the empty tree is '#' and a single node 1 is '1,#,#'. Write `serialize` and `deserialize` that round trip, 0 <= n <= 10^4, and say why there are exactly 2n + 1 tokens, and how this differs from the trimmed array form the examples in this book use for input. The example gives the exact serialized string for the tree. Example: root=[1, 2, 3, null, null, 4, 5] -> '1,2,3,#,#,4,5,#,#,#,#'; root=[] -> '#'; root=[1] -> '1,#,#'; root=[1, null, 2] -> '1,#,2,#,#'.
**Asked at:** Tree interview-pattern guides on techinterview.org (binary-tree patterns, traversal patterns, advanced tree patterns, depth of a binary tree; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND) | Candidate-reported rounds (Naukri Code360: a Flipkart November 2021 online coding round with a vertical order traversal question, an Amazon March 2022 SDE-2 online round with LCA of a binary tree; a Glassdoor Flipkart September-October 2025 report of LCA in a coding round; a LeetCode discuss Facebook intern report listing serialize/deserialize, LCA and smallest subtree with the deepest nodes; snippets only, not opened; self-reported, unverified) | Blind 75 / NeetCode 150 pattern lists and their GitHub copies (search snippets only, not opened; the snippets confirm a Trees category and Validate BST in Blind 75, the rest of the tree list is editor knowledge)

**Pattern:** Tree encoding with a queue. Emit the tree level by level, with an explicit marker for every missing child so the shape is recoverable from the string alone.

**Say this first (1 line):** "Level order with '#' for each missing child, never trimmed: the root first, then for each real node its left and right child tokens. Decoding replays the same queue."

**Brute force:** Preorder with '#' markers by recursion. It also round trips (the code uses it as a cross-check on the token count) but it is recursive, so a 10^4-deep chain hits the recursion limit. The BFS format avoids that.

**Optimal:**
- `serialize`: if the tree is empty return `'#'`. Otherwise start the list with the root value and a queue holding the root. Pop a node, append its left token then its right token (`'#'` for None; real children are appended to the queue as well).
- `deserialize`: split on commas, make the root, put it in the queue, then for each popped node read the next two tokens as its left and right. A `'#'` means no child.
- Both sides use the same queue order, which is why they stay in step.
- Why 2n + 1 tokens, never trimmed: each of the n nodes writes exactly two child tokens (2n in all), plus one token for the root. n - 1 of the child slots are filled by the non-root nodes (one each), leaving n + 1 markers: n values + (n + 1) '#' = 2n + 1. For the empty tree that is the single token `'#'`.
- The array form the examples use for INPUT is trimmed: trailing nulls are dropped and the children of a null are not listed. That form is shorter (7 entries versus 11 tokens in the output) and cannot be decoded without the "children of a null are not listed" convention. The serialization here lists every child slot of every real node and also has no ambiguity: no node's tokens are skipped.

**Complexity:** Time O(n), each node enqueued and dequeued once, each token written and parsed once. Space O(n) for the string and the queue (the queue holds at most one level). No recursion, so a 10^4-node chain is fine.

**Dry run:** the tree `1 / (2, 3)`, with 3 having children 4 and 5.
- Start `1`, queue [1]. Pop 1: write `2`, `3`; queue [2, 3].
- Pop 2: write `#`, `#`. Pop 3: write `4`, `5`; queue [4, 5].
- Pop 4: `#`, `#`. Pop 5: `#`, `#`.
- Result `1,2,3,#,#,4,5,#,#,#,#`, which is 11 = 2 * 5 + 1 tokens.

**Code:**
```python
import random
import sys
from collections import deque

class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(arr):
    """Level-order array with None for a missing child (children of a None are not listed)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None:
            nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root

def nodes_of(root, cap=10**6):
    """Every node, iterative preorder. A visited-id guard turns a cycle or a shared node into an AssertionError."""
    out, seen, st = [], set(), ([root] if root else [])
    while st:
        n = st.pop()
        assert id(n) not in seen, "cycle or aliasing"
        seen.add(id(n)); out.append(n)
        assert len(out) <= cap, "runaway tree"
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out

def to_arr(root):
    """Trimmed level-order array (the input format used by the examples)."""
    nodes_of(root)
    out, q = [], deque([root] if root else [])
    while q:
        nd = q.popleft()
        if nd is None:
            out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None:
        out.pop()
    return out

def same(a, b):
    """Structure and values equal, iterative (no recursion limit)."""
    st = [(a, b)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st.append((x.left, y.left)); st.append((x.right, y.right))
    return True

# ---- exhaustive shapes: a shape is None or (left_shape, right_shape)
_sh = {0: [None]}
def shapes(n):
    if n not in _sh:
        _sh[n] = [(L, R) for l in range(n) for L in shapes(l) for R in shapes(n - 1 - l)]
    return _sh[n]

def label(shape, mode, step=1):
    """mode 'in': inorder labels 0, step, 2*step... (so the tree is a BST); 'pre': preorder labels."""
    c = [0]
    def go(s):
        if s is None: return None
        if mode == "pre":
            v = c[0]; c[0] += step; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += step; R = go(s[1]); return (v, L, R)
    return go(shape)

def from_tup(t):
    return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))

def height(root):
    h, level = 0, ([root] if root else [])
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h

# ---------- the required format: level order, '#' for every missing child, nothing trimmed ----------
def serialize(root):
    if root is None:
        return "#"
    out, q = [str(root.val)], deque([root])
    while q:
        n = q.popleft()
        for c in (n.left, n.right):
            if c is None:
                out.append("#")
            else:
                out.append(str(c.val)); q.append(c)
    return ",".join(out)

def deserialize(s):
    tok = s.split(",")
    if tok[0] == "#":
        assert len(tok) == 1
        return None
    root = TreeNode(int(tok[0]))
    q, i = deque([root]), 1
    while q:
        n = q.popleft()
        for side in ("left", "right"):
            if tok[i] != "#":
                c = TreeNode(int(tok[i])); setattr(n, side, c); q.append(c)
            i += 1
    assert i == len(tok), "leftover tokens"
    return root

# ---------- brute force / cross-check format: preorder with '#' (a different, equally valid encoding) ----------
def ser_pre(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None: out.append("#"); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return ",".join(out)

for arr in ([1, 2, 3, None, None, 4, 5], [], [1], [1, None, 2]):
    s = serialize(build(arr))
    assert same(deserialize(s), build(arr))
    print(f"root={arr} -> '{s}'")

# exhaustive: every shape with 0..8 nodes, negative / multi-digit values; round trip + exactly 2n+1 tokens
cases = 0
for n in range(9):
    for sh in shapes(n):
        t = label(sh, "pre", step=-7)               # values 0, -7, -14, ... (negatives and two digits)
        root = from_tup(t)
        s = serialize(root)
        assert len(s.split(",")) == 2 * n + 1        # n values + (n + 1) '#' markers
        assert s.count("#") == n + 1
        assert same(deserialize(s), root)
        assert s == serialize(deserialize(s))        # canonical: serialize(deserialize(s)) == s
        assert ser_pre(root).count("#") == n + 1     # the preorder encoding has the same token count
        cases += 1
print("exhaustive shapes ok:", cases)

# the trimmed array form used by the examples is a different, shorter thing
root = build([1, 2, 3, None, None, 4, 5])
print("trimmed array:", len(to_arr(root)), "entries | full serialization:", len(serialize(root).split(",")), "tokens")

# n = 10^4 skewed tree: BFS and the parser are iterative, so no recursion limit is touched
chain_root = None
for i in range(10**4):
    chain_root = TreeNode(i, chain_root, None)
s = serialize(chain_root)
assert len(s.split(",")) == 2 * 10**4 + 1 and same(deserialize(s), chain_root)
print("10^4-node left chain: round trip ok,", len(s.split(",")), "tokens")

# random trees
random.seed(3)
for _ in range(300):
    n = random.randint(0, 60)
    root = None if n == 0 else TreeNode(random.randint(-99, 99))
    pool = [root] if root else []
    for _ in range(n - 1):
        par = random.choice(pool); side = random.choice(("left", "right"))
        if getattr(par, side) is None:
            c = TreeNode(random.randint(-99, 99)); setattr(par, side, c); pool.append(c)
    assert same(deserialize(serialize(root)), root)
print("300 random trees ok")
```

**Output (my run):**
```
root=[1, 2, 3, None, None, 4, 5] -> '1,2,3,#,#,4,5,#,#,#,#'
root=[] -> '#'
root=[1] -> '1,#,#'
root=[1, None, 2] -> '1,#,2,#,#'
exhaustive shapes ok: 2056
trimmed array: 7 entries | full serialization: 11 tokens
10^4-node left chain: round trip ok, 20001 tokens
300 random trees ok
```

Output prints `None` where the prompt writes `null` (that is the array input, not the string). The exhaustive test covers every shape with 0 to 8 nodes, with negative and two-digit values, and checks the token count equals 2n + 1 and that `serialize(deserialize(s)) == s`.

**Edge cases:**
- Empty tree: `'#'`, one token, handled before anything else.
- Single node: `'1,#,#'`.
- Negative or multi-digit values: split on commas, not characters.
- Strings as values: a comma or '#' in a value would break this format; the question has integers.
- Skewed 10^4-node tree: 20001 tokens, no recursion.

**Follow-ups:**
- Why not preorder? It works and needs only one pass with a global index, but the recursion depth equals the tree height.
- Can you shrink it? Yes: trim trailing markers, or for a BST use only the preorder values (no markers at all, see the "build a BST from preorder" question).
- Is it unique? Yes: a valid string decodes to exactly one tree, and a tree always produces the same string.

**Common mistakes:**
- Putting None children in the queue, so the decoder reads past the end.
- Trimming trailing `#` on one side only.
- Using `str.split` with a space or character by character, breaking multi-digit and negative values.
- Using `list.pop(0)` as the queue instead of `deque.popleft()`.
