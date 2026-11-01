
# ---------- brute force: root-to-node paths, longest common prefix ----------
def path_to(root, val):
    st = [(root, [root])]
    while st:
        n, p = st.pop()
        if n.val == val:
            return p
        for c in (n.left, n.right):
            if c: st.append((c, p + [c]))
    return None

def lca_brute(root, p, q):
    a, b = path_to(root, p), path_to(root, q)
    if a is None or b is None:
        return None
    last = None
    for x, y in zip(a, b):
        if x is not y: break
        last = x
    return last

# ---------- optimal: post-order, return the node if it matches, else combine ----------
def lca(root, p, q):
    def go(n):
        if n is None or n.val == p or n.val == q:
            return n                      # early return: see "why" below
        l, r = go(n.left), go(n.right)
        if l and r:
            return n                      # p and q are on different sides
        return l or r
    return go(root)

# ---------- safe version when a value may be missing: count the matches seen ----------
def lca_safe(root, p, q):
    found = 0
    def go(n):
        nonlocal found
        if n is None:
            return None
        l, r = go(n.left), go(n.right)    # visit BOTH sides first, so we never skip a match
        if n.val == p or n.val == q:
            found += 1
            return n
        return n if (l and r) else (l or r)
    ans = go(root)
    return ans if found == 2 else None

# ---------- iterative with a parent map (safe on deep trees) ----------
def lca_parent(root, p, q):
    parent, st, byval = {id(root): None}, [root], {}
    while st:
        n = st.pop(); byval[n.val] = n
        for c in (n.left, n.right):
            if c:
                parent[id(c)] = n; st.append(c)
    a, anc = byval[p], set()
    while a:
        anc.add(id(a)); a = parent[id(a)]
    b = byval[q]
    while id(b) not in anc:
        b = parent[id(b)]
    return b

T = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
examples = [(T, 5, 1, 3), (T, 5, 4, 5), (T, 6, 4, 5), (T, 7, 8, 3), ([1, 2], 1, 2, 1)]
for arr, p, q, want in examples:
    root = build_tree(arr)
    got = lca(root, p, q)
    assert got.val == want and got is lca_brute(root, p, q) is lca_parent(root, p, q) is lca_safe(root, p, q)
    print("p=%d q=%d -> %d" % (p, q, got.val))

# exhaustive: every shape with 2..7 nodes (distinct preorder labels), every ordered pair p != q
pairs = 0
for n in range(2, 8):
    for s in shapes(n):
        root = from_tup(label(s, "pre"))
        for p in range(n):
            for q in range(n):
                if p != q:
                    w = lca_brute(root, p, q)
                    assert lca(root, p, q) is w and lca_safe(root, p, q) is w and lca_parent(root, p, q) is w
                    pairs += 1
print("exhaustive ok:", pairs, "(tree, p, q) cases, all shapes with 2..7 nodes")

# one value missing: the early-return version is fooled, the counting version is not
fooled = safe_none = cases = 0
for n in range(1, 8):
    for s in shapes(n):
        root = from_tup(label(s, "pre"))
        for p in range(n):
            cases += 1
            fooled += lca(root, p, 99) is not None      # returns p's node although 99 is absent
            safe_none += lca_safe(root, p, 99) is None
print("missing q: early-return answered for", fooled, "of", cases, "| counting version returned None for", safe_none, "of", cases)

# random larger trees with distinct values
random.seed(13)
for _ in range(300):
    n = random.randint(2, 60)
    vals = random.sample(range(1000), n)
    arr = [vals[0]]; slots = 2; k = 1
    while k < n:                                   # random level-order fill, some Nones
        if random.random() < 0.3 and slots > 1:
            arr.append(None)
        else:
            arr.append(vals[k]); k += 1; slots += 1
        slots -= 1
    root = build_tree(arr)
    ns = all_nodes(root)
    if len(ns) < 2: continue
    p, q = random.sample([x.val for x in ns], 2)
    assert lca(root, p, q) is lca_brute(root, p, q) is lca_parent(root, p, q)
print("random ok: 300 trees up to 60 nodes")

deep = chain(20000)
r = deep_ok(lca, deep, 19999, 20000)               # both values sit at the bottom
print("chain 20000 recursive:", r if isinstance(r, str) else r.val, "| parent-map:", lca_parent(deep, 19999, 20000).val)
