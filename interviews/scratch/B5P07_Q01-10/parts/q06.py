# ---------- brute force: root-to-node paths, last common node ----------
def path_to(root, x):
    out, cur = [], root
    while cur is not None:
        out.append(cur)
        if x == cur.val: return out
        cur = cur.left if x < cur.val else cur.right
    raise ValueError('value not in tree')
def lca_brute(root, p, q):
    a, b, last = path_to(root, p), path_to(root, q), None
    for x, y in zip(a, b):
        if x is y: last = x
        else: break
    return last.val

# ---------- optimal: walk down once ----------
def lca_bst(root, p, q, steps=None):
    lo, hi = (p, q) if p < q else (q, p)
    cur, n = root, 0
    while cur is not None:
        n += 1
        if hi < cur.val:            # both are smaller: go left
            cur = cur.left
        elif lo > cur.val:          # both are larger: go right
            cur = cur.right
        else:                       # lo <= cur.val <= hi: the paths split here (or cur is p or q)
            if steps is not None: steps.append(n)
            return cur.val
    raise ValueError('p or q not in tree')

# ---------- examples ----------
big = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
for arr, p, q in ((big, 2, 8), (big, 2, 4), (big, 3, 5), ([2, 1], 2, 1)):
    print(arr, p, q, '->', lca_bst(build_tree(arr), p, q))

# ---------- cross-check: every BST shape up to 7 nodes (distinct values 0..n-1, labelled by inorder), every pair ----------
def label_in(s, c=None):
    c = c if c is not None else [0]
    if s is None: return None
    L = label_in(s[0], c); v = c[0]; c[0] += 1
    return (v, L, label_in(s[1], c))
def height(t): return 0 if t is None else 1 + max(height(t[1]), height(t[2]))
pairs = 0
for n in range(2, 8):
    for s in shapes(n):
        t = label_in(s); root = from_tuple(t); h = height(t)
        for p in range(n):
            for q in range(n):
                if p == q: continue
                st = []
                got = lca_bst(root, p, q, st)
                assert got == lca_brute(root, p, q)
                assert st[0] <= h                        # at most h loop rounds
                pairs += 1
print('BST shapes up to 7 nodes, all ordered pairs checked:', pairs)

# ---------- random BSTs with non-consecutive values (insert in random order) ----------
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
random.seed(2)
for _ in range(300):
    vals = random.sample(range(-50, 50), random.randint(2, 30)); root = None
    for v in vals: root = insert(root, v)
    for _ in range(20):
        p, q = random.sample(vals, 2)
        assert lca_bst(root, p, q) == lca_brute(root, p, q)
print('random BSTs ok: 300')

# ---------- edge cases: ancestor of the other, argument order, skewed chain ----------
r = build_tree(big)
assert lca_bst(r, 8, 2) == lca_bst(r, 2, 8) == 6
assert lca_bst(r, 4, 2) == 2 and lca_bst(r, 0, 5) == 2
n = 100_000
chain = None
for v in range(n - 1, -1, -1): chain = TreeNode(v, None, chain)     # 0 -> 1 -> ... right chain
assert lca_bst(chain, n - 1, n - 2) == n - 2 and lca_bst(chain, 0, n - 1) == 0
print('chain of 10^5 handled iteratively; all asserts passed')
