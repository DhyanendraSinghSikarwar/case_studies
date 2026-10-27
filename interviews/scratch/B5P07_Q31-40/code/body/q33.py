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
