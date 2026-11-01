
def count_paths_brute(root, target):
    """O(n * h): start a downward walk at every node."""
    total = 0
    for start in nodes_of(root):
        st = [(start, start.val)]
        while st:
            n, s = st.pop()
            if s == target: total += 1
            for c in (n.left, n.right):
                if c: st.append((c, s + c.val))
    return total

def count_paths_prefix_rec(root, target, undo=True):
    """O(n): count[prefix] along the CURRENT root-to-node path. Recursion depth = height."""
    count = {0: 1}                                    # the empty prefix
    ans = 0
    def go(n, prefix):
        nonlocal ans
        if n is None: return
        prefix += n.val
        ans += count.get(prefix - target, 0)          # paths ending at n that start below some ancestor
        count[prefix] = count.get(prefix, 0) + 1
        go(n.left, prefix); go(n.right, prefix)
        if undo: count[prefix] -= 1                   # leaving n: the prefix is no longer on the path
    go(root, 0)
    return ans

def count_paths_prefix_iter(root, target):
    """Same, with an explicit stack of (node, prefix_before, entered?) so deep trees are fine."""
    count, ans = {0: 1}, 0
    st = [(root, 0, False)] if root else []
    while st:
        n, before, leaving = st.pop()
        prefix = before + n.val
        if leaving:
            count[prefix] -= 1; continue              # the undo
        ans += count.get(prefix - target, 0)
        count[prefix] = count.get(prefix, 0) + 1
        st.append((n, before, True))
        if n.right: st.append((n.right, prefix, False))
        if n.left:  st.append((n.left, prefix, False))
    return ans

cases = [([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8, 3), ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22, 3),
         ([1, -1], 0, 1), ([0, 0, None, 0], 0, 6)]
for arr, tg, exp in cases:
    r = build_tree(arr)
    a, b, c = count_paths_brute(r, tg), count_paths_prefix_rec(r, tg), count_paths_prefix_iter(r, tg)
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, "target", tg, "->", b)
print("empty tree ->", count_paths_prefix_iter(None, 0))
# find the smallest tree where forgetting the undo gives a wrong answer
found = None
for n in range(1, 6):
    for arr in ([1] * n, [1, 2, 3, 4, 5][:n], [1, 1, 1, 1, 1][:n]):
        r = build_tree(arr)
        for tg in range(0, 8):
            if found is None and count_paths_prefix_rec(r, tg, undo=False) != count_paths_brute(r, tg):
                found = (arr, tg, count_paths_prefix_rec(r, tg, undo=False), count_paths_brute(r, tg))
print("forgetting the undo, first failing case (array, target, buggy, true):", found)
assert found is not None

# exhaustive: all shapes up to 7 nodes, values drawn from {-2..2} (zeros and negatives), all targets -6..6
random.seed(27); cnt = 0; bug_wrong = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(3):
            vals = iter(random.randint(-2, 2) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return TreeNode(v, L, lab(x[1]))
            r = lab(s)
            for tg in range(-6, 7):
                e = count_paths_brute(r, tg)
                assert count_paths_prefix_rec(r, tg) == count_paths_prefix_iter(r, tg) == e
                if count_paths_prefix_rec(r, tg, undo=False) != e: bug_wrong += 1
                cnt += 1
print("exhaustive+random ok:", cnt, "cases; forgetting the undo was wrong in", bug_wrong, "of them")

# n = 1000 chain of ones, target 3: recursion depth 1000 hits the limit, the iterative one is fine
chain = None
for _ in range(1000): chain = TreeNode(1, chain, None)
try:
    count_paths_prefix_rec(chain, 3); print("recursive: no error")
except RecursionError:
    print("recursive on a 1000-node chain: RecursionError")
assert count_paths_prefix_iter(chain, 3) == 998 and count_paths_brute(chain, 3) == 998
print("iterative on the chain, target 3 ->", count_paths_prefix_iter(chain, 3), "(starts 998 down the chain)")
