# ---------- brute force: pair each node with its depth by DFS, then group ----------
def levels_brute(t):
    groups = {}
    def go(x, d):
        if x is None: return
        groups.setdefault(d, []).append(x[0])        # left subtree is visited first, so left-to-right order
        go(x[1], d + 1); go(x[2], d + 1)
    go(t, 0)
    return [groups[d] for d in sorted(groups)]

# ---------- optimal: BFS with a deque and a level-size snapshot ----------
def level_order(root, peak=None):
    if root is None:
        return []
    out, q = [], deque([root])
    if peak is not None: peak[0] = 1                 # the root alone is already in the queue
    while q:
        level = []
        for _ in range(len(q)):                      # snapshot: only this level's nodes
            node = q.popleft()                       # O(1); list.pop(0) would be O(n)
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
            if peak is not None: peak[0] = max(peak[0], len(q))
        out.append(level)
    return out

# ---------- examples ----------
for arr in ([3, 9, 20, None, None, 15, 7], [1], [], [1, 2, None, 3]):
    print(arr, '->', level_order(build_tree(arr)))

# ---------- cross-check: all shapes up to 7 nodes, then random trees ----------
for t in all_trees(7):
    r = from_tuple(t)
    assert level_order(r) == levels_brute(t)
    flat = [v for lv in level_order(r) for v in lv]
    assert flat == [x for x in to_level_order(r) if x is not None]      # same order as the canonical array
print('626 shapes ok')
random.seed(8)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 99), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(400):
    t = random_tuple(random.randint(0, 100))
    assert level_order(from_tuple(t)) == levels_brute(t)
print('random ok: 400')

# ---------- maximum queue length on a perfect tree, n = 2^k - 1 ----------
def perfect(k):
    return None if k == 0 else TreeNode(0, perfect(k - 1), perfect(k - 1))
for k in range(1, 11):
    pk = [0]; level_order(perfect(k), pk)
    assert pk[0] == 2 ** (k - 1)
    print('k=%2d n=%4d peak queue %4d  (2^(k-1) = %d, about n/2)' % (k, 2**k - 1, pk[0], 2 ** (k - 1)))

# ---------- edge cases ----------
assert level_order(None) == [] and level_order(TreeNode(7)) == [[7]]
chain = None
for i in range(2000): chain = TreeNode(i, chain, None)
lv = level_order(chain); assert len(lv) == 2000 and all(len(x) == 1 for x in lv)
print('2000-node chain: 2000 levels of one node; all asserts passed')
