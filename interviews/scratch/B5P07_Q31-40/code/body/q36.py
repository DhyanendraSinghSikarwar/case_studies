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
