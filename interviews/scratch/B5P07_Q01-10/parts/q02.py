# ---------- brute force on tuples (independent of the node code) ----------
def height_tuple(t):
    return 0 if t is None else 1 + max(height_tuple(t[1]), height_tuple(t[2]))

# ---------- 1. recursive: height = 1 + max(children); tracks its own call depth ----------
def depth_rec(root, stats=None, d=1):
    if root is None:
        return 0
    if stats is not None:
        stats['rec'] = max(stats['rec'], d)          # deepest call stack of real nodes
    return 1 + max(depth_rec(root.left, stats, d + 1), depth_rec(root.right, stats, d + 1))

# ---------- 2. BFS: count levels with a size snapshot ----------
def depth_bfs(root, stats=None):
    if root is None:
        return 0
    q, levels = deque([root]), 0
    while q:
        levels += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        if stats is not None:
            stats['q'] = max(stats['q'], len(q))
    return levels

# ---------- 3. iterative DFS: stack of (node, depth) ----------
def depth_dfs(root, stats=None):
    best, st = 0, ([(root, 1)] if root else [])
    while st:
        node, d = st.pop()
        best = max(best, d)
        if node.left: st.append((node.left, d + 1))
        if node.right: st.append((node.right, d + 1))
        if stats is not None:
            stats['st'] = max(stats['st'], len(st))
    return best

def width_tuple(t):                                   # widest level, independent brute force
    lv, w = [t] if t else [], 0
    while lv:
        w = max(w, len(lv))
        lv = [c for x in lv for c in (x[1], x[2]) if c is not None]
    return w

# ---------- examples ----------
for arr in ([3, 9, 20, None, None, 15, 7], [1, None, 2], [], [5]):
    r = build_tree(arr)
    print(arr, '->', depth_rec(r), depth_bfs(r), depth_dfs(r))

# ---------- cross-check: all shapes up to 7 nodes; measure the space claims ----------
worst_st_gap = 0
for t in all_trees(7):
    r, h = from_tuple(t), height_tuple(t)
    s = {'rec': 0, 'q': 0, 'st': 0}
    assert depth_rec(r, s) == depth_bfs(r, s) == depth_dfs(r, s) == h
    assert s['rec'] == h                              # recursion depth = height
    assert s['q'] <= width_tuple(t)                   # BFS queue never exceeds the widest level (children of a level)
    assert s['st'] <= h                               # DFS stack never exceeds h entries
print('shapes ok: 626; rec depth == h; BFS queue <= widest level; DFS stack <= h')

random.seed(11)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (0, random_tuple(l), random_tuple(n - 1 - l))
for _ in range(400):
    t = random_tuple(random.randint(0, 60)); r = from_tuple(t)
    assert depth_rec(r) == depth_bfs(r) == depth_dfs(r) == height_tuple(t)
print('random ok: 400')

# ---------- shapes that make the space O(n) ----------
def perfect(k):                                       # k levels, n = 2^k - 1
    return None if k == 0 else TreeNode(0, perfect(k - 1), perfect(k - 1))
for k in (1, 4, 10):
    s = {'rec': 0, 'q': 0, 'st': 0}; r = perfect(k)
    depth_bfs(r, s); depth_dfs(r, s); depth_rec(r, s)
    print('perfect k=%d n=%d: BFS queue peak %d, DFS stack peak %d, recursion depth %d' % (k, 2**k - 1, s['q'], s['st'], s['rec']))
def skewed(n):                                        # right chain, built without recursion
    root = None
    for _ in range(n): root = TreeNode(0, None, root)
    return root
n = 100_000
r = skewed(n); s = {'rec': 0, 'q': 0, 'st': 0}
assert depth_bfs(r, s) == depth_dfs(r, s) == n
print('skewed n=%d: BFS queue peak %d, DFS stack peak %d' % (n, s['q'], s['st']))
try:
    depth_rec(r)
except RecursionError:
    print('skewed n=%d: recursive version raises RecursionError (default limit)' % n)

# ---------- edge cases ----------
assert depth_rec(None) == depth_bfs(None) == depth_dfs(None) == 0
assert depth_rec(TreeNode(5)) == 1
print('all asserts passed')
