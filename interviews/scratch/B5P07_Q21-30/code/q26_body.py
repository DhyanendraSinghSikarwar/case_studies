
def path_sum_rec(root, target):
    """Backtracking on ONE shared path list. Recursive: depth = height (fails on a 5000-node chain by default)."""
    res, path = [], []
    def go(n, rem):
        if n is None: return
        path.append(n.val); rem -= n.val
        if n.left is None and n.right is None:
            if rem == 0: res.append(path[:])          # COPY here; path keeps changing afterwards
        else:
            go(n.left, rem); go(n.right, rem)
        path.pop()                                    # undo on the way out
    go(root, target)
    return res

def path_sum_iter(root, target):
    """Same idea with an explicit stack of (node, entered?) pairs: no recursion limit."""
    res, path, st, rem = [], [], [(root, False)] if root else [], 0
    while st:
        n, done = st.pop()
        if done:
            path.pop(); rem -= n.val; continue
        path.append(n.val); rem += n.val              # rem is now the running sum from the root
        st.append((n, True))
        if n.left is None and n.right is None:
            if rem == target: res.append(path[:])
        else:
            if n.right: st.append((n.right, False))   # push right first so left is processed first
            if n.left:  st.append((n.left, False))
    return res

def path_sum_buggy(root, target):
    """BUG: appends the shared list itself instead of a copy."""
    res, path = [], []
    def go(n, rem):
        if n is None: return
        path.append(n.val); rem -= n.val
        if n.left is None and n.right is None:
            if rem == 0: res.append(path)             # <- same list object every time
        else:
            go(n.left, rem); go(n.right, rem)
        path.pop()
    go(root, target)
    return res

def leaf_paths(t, pre=()):
    """Independent brute force on tuple trees: every root-to-leaf path, then filter."""
    if t is None: return []
    p = pre + (t[0],)
    if t[1] is None and t[2] is None: return [list(p)]
    return leaf_paths(t[1], p) + leaf_paths(t[2], p)

for arr, tg, exp in [([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22, [[5, 4, 11, 2], [5, 8, 4, 5]]),
                     ([1, 2, 3], 5, []), ([1, 2], 0, []), ([], 0, [])]:
    r = build_tree(arr); a, b = path_sum_rec(r, tg), path_sum_iter(r, tg)
    assert a == b == exp, (arr, a, b)
    print(arr, "target", tg, "->", a)
print("[1, 2] with target 3 ->", path_sum_rec(build_tree([1, 2]), 3), "(1 has one child, so 1 alone is not a leaf path; 1-2 is)")
print("bug (no copy), same first example:", path_sum_buggy(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22))

# exhaustive over all shapes 0..7 with several value labelings (values in -2..3) and every target in range
random.seed(26); cnt = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(4):
            vals = iter(random.randint(-2, 3) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return (v, L, lab(x[1]))
            t = lab(s); r = from_tup(t); allp = leaf_paths(t)
            for tg in range(-8, 12):
                exp = [p for p in allp if sum(p) == tg]
                assert path_sum_rec(r, tg) == path_sum_iter(r, tg) == exp
                cnt += 1
print("exhaustive+random ok:", cnt, "(tree, target) cases; order = left-to-right order of leaves")

# 5000-node chain: recursion fails by default, the explicit stack does not
chain = None
for _ in range(5000): chain = TreeNode(1, chain, None)
try:
    path_sum_rec(chain, 5000); print("recursive: no error")
except RecursionError:
    print("recursive on a 5000-node chain: RecursionError")
res = path_sum_iter(chain, 5000)
assert len(res) == 1 and len(res[0]) == 5000
print("iterative on the same chain: 1 path of length", len(res[0]))
# cost of copying: k matches of length L cost k * L extra. all-zero tree, target 0: every leaf matches
zeros31 = build_tree([0] * 31)       # 16 leaves, path length 5
print("perfect tree 31 nodes all zero, target 0: matches =", len(path_sum_rec(zeros31, 0)), "each of length 5")
