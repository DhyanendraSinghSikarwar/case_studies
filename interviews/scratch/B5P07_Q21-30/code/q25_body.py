
def zigzag(root):
    """BFS; the queue is ALWAYS filled left to right; only the output of each level is reversed or not."""
    if root is None: return []
    out, q, left_to_right = [], deque([root]), True
    while q:
        level = deque()
        for _ in range(len(q)):                     # snapshot: exactly one level
            n = q.popleft()
            if left_to_right: level.append(n.val)   # fill the output from alternating ends
            else:             level.appendleft(n.val)
            if n.left:  q.append(n.left)            # children always left then right
            if n.right: q.append(n.right)
        out.append(list(level)); left_to_right = not left_to_right
    return out

def zigzag_reverse_levels(root):
    """Alternative: normal level order, then reverse every odd level."""
    out, level = [], [root] if root else []
    while level:
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]
    return [l[::-1] if i % 2 else l for i, l in enumerate(out)]

def zigzag_wrong(root):
    """BUG: reverse the queue itself on odd levels. The children then enter in the wrong order for the next level."""
    if root is None: return []
    out, level, flip = [], [root], False
    while level:
        if flip: level = level[::-1]               # reversing the nodes ...
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]   # ... changes who is enqueued first
        flip = not flip
    return out

def zig_tuple(t):
    """Independent brute force on tuple trees: collect (depth, left-to-right index) then regroup."""
    levels = {}
    def go(t, d):
        if t is None: return
        levels.setdefault(d, []).append(t[0]); go(t[1], d + 1); go(t[2], d + 1)   # preorder keeps left-to-right order per level
    go(t, 0)
    return [levels[d][::-1] if d % 2 else levels[d] for d in sorted(levels)]

for arr, exp in [([3, 9, 20, None, None, 15, 7], [[3], [20, 9], [15, 7]]), ([1, 2, 3, 4, None, None, 5], [[1], [3, 2], [4, 5]]),
                 ([1], [[1]]), ([], [])]:
    r = build_tree(arr); got = zigzag(r)
    assert got == zigzag_reverse_levels(r) == exp, (arr, got)
    print(arr, "->", got)
print("reversing the queue (bug) on [1,2,3,4,None,None,5]:", zigzag_wrong(build_tree([1, 2, 3, 4, None, None, 5])))

# exhaustive: all shapes with 0..8 nodes (values 0..n-1 by inorder, distinct), compare three solutions + brute force
cnt = bad = 0
for n in range(0, 9):
    for s in shapes(n):
        t = label_inorder(s); r = from_tup(t)
        assert zigzag(r) == zigzag_reverse_levels(r) == zig_tuple(t)
        if zigzag_wrong(r) != zigzag(r): bad += 1
        cnt += 1
print("exhaustive ok on", cnt, "shapes; the 'reverse the queue' bug is wrong on", bad, "of them")
random.seed(25)
for _ in range(200):
    n = random.randint(0, 60); arr = [random.choice([None, random.randint(0, 9)]) for _ in range(n)]
    if arr: arr[0] = 1
    r = build_tree(arr); assert zigzag(r) == zigzag_reverse_levels(r)
print("random cross-check ok (200 arrays)")
big = build_tree([1] * 2000)    # a bushy tree with 2000 nodes
assert sum(len(l) for l in zigzag(big)) == 2000
print("n = 2000 bushy tree: levels =", len(zigzag(big)))
