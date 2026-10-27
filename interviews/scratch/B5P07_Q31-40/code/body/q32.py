def inorder_vals(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out

# ---------- brute force: sorted values, then the next one ----------
def succ_brute(root, p):
    vals = inorder_vals(root)                 # O(n) time and space
    i = vals.index(p)
    return vals[i + 1] if i + 1 < len(vals) else None

# ---------- optimal: one walk down, remember the last node where we went left ----------
def succ(root, p, steps=None):
    best, cur = None, root
    while cur is not None:
        if steps is not None: steps[0] += 1
        if p < cur.val:
            best = cur.val                    # cur is bigger than p: a candidate, but maybe a smaller one is deeper
            cur = cur.left
        else:                                 # p >= cur.val: the answer, if any, is strictly to the right
            cur = cur.right
    return best

# ---------- same idea, split into the two textbook cases (finds p first) ----------
def succ_cases(root, p):
    anc, cur = None, root
    while cur.val != p:                       # p is guaranteed to exist
        if p < cur.val: anc, cur = cur, cur.left
        else: cur = cur.right
    if cur.right:                             # case 1: minimum of the right subtree
        cur = cur.right
        while cur.left: cur = cur.left
        return cur.val
    return anc.val if anc else None           # case 2: lowest ancestor whose LEFT subtree holds p

# examples
for arr, p in [([2, 1, 3], 1), ([5, 3, 6, 2, 4, None, None, 1], 6), ([5, 3, 6, 2, 4, None, None, 1], 4),
               ([5, 3, 6, 2, 4, None, None, 1], 2), ([2], 2)]:
    t = build(arr)
    a, b, c = succ(t, p), succ_cases(t, p), succ_brute(t, p)
    assert a == b == c
    print(f"root={arr}, p={p} -> {a}")

# exhaustive: all BST shapes 0..9 nodes, every existing p; also check the step count is at most the height
cases, worst_gap = 0, 0
for n in range(1, 10):
    for sh in shapes(n):
        t = from_tup(label(sh, "in"))
        h = height(t)
        for p in range(n):
            steps = [0]
            got = succ(t, p, steps)
            assert got == succ_brute(t, p) == succ_cases(t, p)
            assert got == (p + 1 if p + 1 < n else None)
            assert steps[0] <= h                          # O(h): never more nodes visited than the height
            worst_gap = max(worst_gap, h - steps[0])
            cases += 1
print("exhaustive cases ok:", cases)

# a p that is NOT in the tree still gets the next larger value (useful follow-up), but only the walk version supports it
t = build([5, 3, 6, 2, 4])
print("next larger than 4.5:", succ(t, 4.5), "| than 1:", succ(t, 1), "| than 9:", succ(t, 9))
