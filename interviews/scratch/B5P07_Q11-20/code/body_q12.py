
# ---------- brute force: compare every node with ALL nodes of its two subtrees ----------
def is_bst_brute(root):
    for n in all_nodes(root):
        if any(x.val >= n.val for x in all_nodes(n.left)):
            return False
        if any(x.val <= n.val for x in all_nodes(n.right)):
            return False
    return True

# ---------- optimal 1: pass (low, high) bounds down; None means "no bound" ----------
def is_bst_bounds(root):
    def ok(n, low, high):
        if n is None:
            return True
        if (low is not None and n.val <= low) or (high is not None and n.val >= high):
            return False
        return ok(n.left, low, n.val) and ok(n.right, n.val, high)
    return ok(root, None, None)

# ---------- optimal 2: iterative inorder must be strictly increasing ----------
def is_bst_inorder(root):
    st, cur, prev = [], root, None
    while cur or st:
        while cur:
            st.append(cur); cur = cur.left
        cur = st.pop()
        if prev is not None and cur.val <= prev:      # <= makes duplicates invalid
            return False
        prev, cur = cur.val, cur.right
    return True

# ---------- the classic wrong answers ----------
def is_bst_parent_only(root):                         # compares a node only with its children
    if root is None: return True
    if root.left and root.left.val >= root.val: return False
    if root.right and root.right.val <= root.val: return False
    return is_bst_parent_only(root.left) and is_bst_parent_only(root.right)

def is_bst_sentinel(root, lo=-2**31, hi=2**31 - 1):   # fake "infinity" breaks on the extremes
    if root is None: return True
    if root.val <= lo or root.val >= hi: return False
    return is_bst_sentinel(root.left, lo, root.val) and is_bst_sentinel(root.right, root.val, hi)

examples = [([2, 1, 3], True), ([5, 1, 4, None, None, 3, 6], False),
            ([5, 4, 6, None, None, 3, 7], False), ([2, 2, 2], False),
            ([-2147483648], True), ([], True)]
for arr, want in examples:
    root = build_tree(arr)
    assert is_bst_bounds(root) == is_bst_inorder(root) == is_bst_brute(root) == want
    print(arr, "->", is_bst_bounds(root))

# wrong versions fail exactly where the prompt says
t = build_tree([5, 4, 6, None, None, 3, 7])
print("parent-only on [5,4,6,null,null,3,7]:", is_bst_parent_only(t), "(wrong, 3 sits right of 5)")
print("sentinel on [-2147483648]:", is_bst_sentinel(build_tree([-2147483648])), "(wrong, should be True)")
print("sentinel on [2147483647]:", is_bst_sentinel(build_tree([2147483647])), "(wrong, should be True)")
for arr in ([2147483647], [-2147483648, None, 2147483647], [2147483647, 2147483647]):
    r = build_tree(arr)
    assert is_bst_bounds(r) == is_bst_inorder(r) == is_bst_brute(r)
    print("None bounds on", arr, "->", is_bst_bounds(r))

# exhaustive: all shapes with 0..5 nodes, every labelling with values from {0,1,2}
count = valid = 0
for n in range(6):
    for s in shapes(n):
        for vals in __import__("itertools").product(range(3), repeat=n):
            it = iter(vals)
            def put(sh):
                return None if sh is None else (next(it), put(sh[0]), put(sh[1]))
            root = from_tup(put(s))                    # preorder labelling
            b = is_bst_brute(root)
            assert is_bst_bounds(root) == is_bst_inorder(root) == b
            count += 1; valid += b
print("exhaustive ok:", count, "labelled trees, of which", valid, "are valid BSTs")

# inorder-labelled shapes up to 7 nodes are always BSTs; swapping two labels breaks it
for n in range(8):
    for s in shapes(n):
        root = from_tup(label(s, "in"))
        assert is_bst_bounds(root) and is_bst_inorder(root)
        if n >= 2:
            ns = all_nodes(root)
            for i in range(n):
                for j in range(i + 1, n):
                    ns[i].val, ns[j].val = ns[j].val, ns[i].val
                    assert is_bst_bounds(root) == is_bst_inorder(root) == is_bst_brute(root) == False
                    ns[i].val, ns[j].val = ns[j].val, ns[i].val
print("inorder-labelled shapes 0..7 are BSTs; every swap of two values is caught")

# random trees, wide integer range including the 32-bit extremes
random.seed(12)
pool = [-2**31, -5, 0, 3, 8, 2**31 - 1]
for _ in range(2000):
    arr = [random.choice(pool)]
    for _ in range(random.randint(0, 12)):
        arr.append(None if random.random() < 0.3 else random.choice(pool))
    r = build_tree(arr)
    assert is_bst_bounds(r) == is_bst_inorder(r) == is_bst_brute(r)
print("random ok: 2000 trees")

# deep chain of 5000 ascending values: inorder version is iterative
deep = chain(5000)
print("chain 5000 inorder:", is_bst_inorder(deep), "| bounds recursive:", deep_ok(is_bst_bounds, deep))
