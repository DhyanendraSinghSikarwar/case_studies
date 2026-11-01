def inorder_nodes(root):
    out, st, cur = [], [], root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur); cur = cur.right
    return out

# ---------- brute force: sort the values and write them back in inorder (O(n log n) time, O(n) space) ----------
def recover_brute(root):
    ns = inorder_nodes(root)
    for node, v in zip(ns, sorted(n.val for n in ns)):
        node.val = v
    return root

# ---------- optimal: iterative inorder with a prev pointer, O(h) space; descents = places where prev.val > cur.val ----------
def recover_stack(root, info=None):
    st, cur, prev, first, second, descents = [], root, None, None, None, 0
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop()
        if prev is not None and prev.val > cur.val:
            descents += 1
            if first is None: first = prev       # first descent: the earlier (larger) node is the culprit
            second = cur                         # last descent: the later (smaller) node is the other one
        prev, cur = cur, cur.right
    if info is not None: info.append(descents)
    first.val, second.val = second.val, first.val
    return root

# ---------- O(1) extra space: Morris traversal (temporary threads from each predecessor to its successor) ----------
def recover_morris(root):
    cur, prev, first, second = root, None, None, None
    def visit(node):
        nonlocal prev, first, second
        if prev is not None and prev.val > node.val:
            if first is None: first = prev
            second = node
        prev = node
    while cur:
        if cur.left is None:
            visit(cur); cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur: pred = pred.right
            if pred.right is None:
                pred.right = cur; cur = cur.left            # make the thread, go left
            else:
                pred.right = None; visit(cur); cur = cur.right   # remove the thread, visit, go right
    first.val, second.val = second.val, first.val           # must finish the whole walk so no thread stays
    return root

def run(fn, arr):
    return to_arr(fn(build(arr)))

for arr in ([1, 3, None, None, 2], [3, 1, 4, None, None, 2], [2, 3, 1], [1, 2, 3]):
    a, b, c = run(recover_brute, arr), run(recover_stack, arr), run(recover_morris, arr)
    assert a == b == c
    print(f"root={arr} -> {a}")

def is_bst(root):
    v = [n.val for n in inorder_nodes(root)]
    return all(x < y for x, y in zip(v, v[1:]))

# exhaustive: every BST shape with 2..8 nodes, EVERY pair of nodes whose values were swapped
cases = adjacent = 0
for n in range(2, 9):
    for sh in shapes(n):
        t = label(sh, "in")
        for i in range(n):
            for j in range(i + 1, n):
                orig = from_tup(t)
                ns = inorder_nodes(orig)
                broken = from_tup(t)
                bn = inorder_nodes(broken)
                bn[i].val, bn[j].val = bn[j].val, bn[i].val
                assert not is_bst(broken)
                # uniqueness: swapping values of exactly ONE pair of nodes restores a BST
                fixes = 0
                for a in range(n):
                    for b in range(a + 1, n):
                        bn[a].val, bn[b].val = bn[b].val, bn[a].val
                        fixes += is_bst(broken)
                        bn[a].val, bn[b].val = bn[b].val, bn[a].val
                assert fixes == 1, (n, i, j)
                for fn in (recover_brute, recover_stack, recover_morris):
                    copy = from_tup(t); cn = inorder_nodes(copy); cn[i].val, cn[j].val = cn[j].val, cn[i].val
                    ids = [id(x) for x in nodes_of(copy)]
                    out = fn(copy)
                    assert same(out, orig)                              # values back, shape unchanged
                    assert [id(x) for x in nodes_of(out)] == ids        # same node objects, no thread left behind
                info = []
                cp = from_tup(t); cn = inorder_nodes(cp); cn[i].val, cn[j].val = cn[j].val, cn[i].val
                recover_stack(cp, info)
                assert info[0] == (1 if j == i + 1 else 2)              # adjacent swap: one descent; otherwise two
                adjacent += (j == i + 1)
                cases += 1
print("exhaustive swaps ok:", cases, "(adjacent in inorder:", adjacent, ")")
