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
