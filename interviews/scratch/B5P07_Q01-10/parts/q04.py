# ---------- brute force: build a NEW mirrored tree (correct values, but not in place) ----------
def invert_copy(root):
    if root is None:
        return None
    return TreeNode(root.val, invert_copy(root.right), invert_copy(root.left))

# ---------- optimal 1: recursive, in place ----------
def invert_rec(root):
    if root is None:
        return None
    root.left, root.right = invert_rec(root.right), invert_rec(root.left)   # one swap per node
    return root

# ---------- optimal 2: iterative, in place (stack; a deque gives the same result) ----------
def invert_iter(root):
    st = [root] if root else []
    while st:
        node = st.pop()
        node.left, node.right = node.right, node.left                       # one swap per node
        if node.left: st.append(node.left)
        if node.right: st.append(node.right)
    return root

# ---------- helpers ----------
def all_nodes(root):
    out, st = [], ([root] if root else [])
    while st:
        n = st.pop(); out.append(n)
        for c in (n.left, n.right):
            if c: st.append(c)
    return out
def tmirror(t):
    return None if t is None else (t[0], tmirror(t[2]), tmirror(t[1]))

# ---------- examples ----------
for arr in ([4, 2, 7, 1, 3, 6, 9], [2, 1, 3], [], [1, 2]):
    print(arr, '->', to_level_order(invert_iter(build_tree(arr))), to_level_order(invert_rec(build_tree(arr))))

# ---------- cross-check: every shape up to 7 nodes; identity verified ----------
for t in all_trees(7):
    for fn in (invert_rec, invert_iter):
        root = from_tuple(t)
        before = all_nodes(root)
        ids_before = {id(n) for n in before}
        old_kids = {id(n): (n.left, n.right) for n in before}      # keep references so ids stay valid
        res = fn(root)
        assert res is root                                         # same root object returned
        assert to_tuple(res) == tmirror(t)                         # values/shape mirrored
        after = all_nodes(res)
        assert len(after) == len(before) and {id(n) for n in after} == ids_before   # same node objects
        for n in before:                                           # every node swapped exactly once
            assert (n.left, n.right) == old_kids[id(n)][::-1]
    c = from_tuple(t)
    assert to_tuple(invert_copy(c)) == tmirror(t)
print('all 626 shapes: mirrored, same root, same node objects, each node swapped once')

# the copy version fails the identity test, which is why the prompt checks identity
root = build_tree([1, 2, 3]); ids = {id(n) for n in all_nodes(root)}
new = invert_copy(root)
print('copy reuses nodes:', bool(ids & {id(n) for n in all_nodes(new)}))

# invert twice = original (so a "swap before and after" bug cancels itself out)
root = build_tree([4, 2, 7, 1, 3, 6, 9]); orig = to_level_order(root)
invert_iter(invert_iter(root)); assert to_level_order(root) == orig
def invert_twice_bug(root):
    if root is None: return None
    root.left, root.right = root.right, root.left
    invert_twice_bug(root.left); invert_twice_bug(root.right)
    root.left, root.right = root.right, root.left     # second swap undoes the first
    return root
r = build_tree([2, 1, 3]); invert_twice_bug(r)
print('swapping twice per node leaves', to_level_order(r), '(unchanged)')

random.seed(1)
def random_tuple(n):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, 99), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(300):
    t = random_tuple(random.randint(0, 80))
    r1, r2 = from_tuple(t), from_tuple(t)
    assert to_tuple(invert_rec(r1)) == to_tuple(invert_iter(r2)) == tmirror(t)
print('random ok: 300')

# ---------- edge cases and depth ----------
assert invert_rec(None) is None and invert_iter(None) is None
one = TreeNode(9); assert invert_iter(one) is one and to_level_order(one) == [9]
n = 100_000
root = None
for i in range(n): root = TreeNode(i, root, None)             # left chain of 10^5 nodes
root = invert_iter(root)
depth, cur = 0, root
while cur: depth, cur = depth + 1, cur.right                  # now it is a right chain
assert depth == n
try:
    invert_rec(root)
except RecursionError:
    print('recursive version raises RecursionError on a 10^5 chain')
print('all asserts passed')
