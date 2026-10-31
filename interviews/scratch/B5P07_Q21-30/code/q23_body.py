
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
