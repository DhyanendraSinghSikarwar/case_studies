
# ---------- brute force: depth of every leaf, take the smallest ----------
def min_depth_brute(root):
    if root is None:
        return 0
    best, st = None, [(root, 1)]
    while st:
        n, d = st.pop()
        if n.left is None and n.right is None:
            best = d if best is None else min(best, d)
        for c in (n.left, n.right):
            if c: st.append((c, d + 1))
    return best

# ---------- the classic bug ----------
def min_depth_wrong(root):
    if root is None:
        return 0
    return 1 + min(min_depth_wrong(root.left), min_depth_wrong(root.right))    # a one-child node is NOT a leaf

# ---------- recursive, fixed ----------
VISITS = 0
def min_depth_rec(root):
    global VISITS
    if root is None:
        return 0
    VISITS += 1
    if root.left is None:
        return 1 + min_depth_rec(root.right)            # only one side exists: must use it
    if root.right is None:
        return 1 + min_depth_rec(root.left)
    return 1 + min(min_depth_rec(root.left), min_depth_rec(root.right))

# ---------- BFS: the first leaf found level by level is the shallowest ----------
POPS = 0
def min_depth_bfs(root):
    global POPS
    if root is None:
        return 0
    q, depth = deque([root]), 1
    while q:
        for _ in range(len(q)):
            n = q.popleft(); POPS += 1
            if n.left is None and n.right is None:
                return depth                            # first leaf = minimum depth
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        depth += 1

examples = [([3, 9, 20, None, None, 15, 7], 2), ([2, None, 3, None, 4, None, 5, None, 6], 5), ([], 0), ([1, 2], 2)]
for arr, want in examples:
    r = build_tree(arr)
    assert min_depth_rec(r) == min_depth_bfs(r) == min_depth_brute(r) == want
    print(arr, "->", want)
print("wrong 1+min on [1,2]:", min_depth_wrong(build_tree([1, 2])), "(correct is 2)")
print("wrong 1+min on the chain example:", min_depth_wrong(build_tree([2, None, 3, None, 4, None, 5, None, 6])), "(correct is 5)")

# exhaustive over every shape with 0..7 nodes
total = wrong = 0
for n in range(8):
    for s in shapes(n):
        r = from_tup(label(s, "pre"))
        w = min_depth_brute(r)
        assert min_depth_rec(r) == min_depth_bfs(r) == w
        wrong += min_depth_wrong(r) != w
        total += 1
print("exhaustive ok:", total, "shapes; the 1+min version is wrong on", wrong, "of them")

random.seed(20)
for _ in range(500):
    arr = [random.randint(0, 9)]
    for _ in range(random.randint(0, 50)):
        arr.append(None if random.random() < 0.4 else random.randint(0, 9))
    r = build_tree(arr)
    assert min_depth_rec(r) == min_depth_bfs(r) == min_depth_brute(r)
print("random ok: 500 trees")

# work on three shapes: perfect tree, long chain, and a tree with a shallow leaf next to a long chain
def perfect(h):
    arr = list(range(1, 2 ** h))
    return build_tree(arr)
def lopsided(n):                                         # root with a leaf on the left, a chain of n - 2 on the right
    return TreeNode(0, TreeNode(1), chain(n - 2))
for name, r in (("perfect h=10 (n=1023)", perfect(10)), ("chain n=500", chain(500)), ("shallow leaf + chain n=500", lopsided(500))):
    VISITS = POPS = 0
    a = min_depth_rec(r); b = min_depth_bfs(r)
    assert a == b == min_depth_brute(r)
    print("%-28s depth=%d  recursive visits=%d  BFS pops=%d" % (name, a, VISITS, POPS))

# long chain of 100000 nodes (the stated maximum): recursion fails, BFS does not
deep = chain(100000)
POPS = 0
print("chain 100000: recursive:", deep_ok(min_depth_rec, deep), "| BFS:", min_depth_bfs(deep), "| BFS pops:", POPS)
