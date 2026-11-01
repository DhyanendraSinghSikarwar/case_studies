import itertools

# ---------- brute force: mirror the whole tree on tuples, compare with the original ----------
def tmirror(t):
    return None if t is None else (t[0], tmirror(t[2]), tmirror(t[1]))
def symmetric_brute(root):
    t = to_tuple(root)
    return t == tmirror(t)

# ---------- optimal 1: recursive two-node comparison ----------
def mirror(a, b):
    if a is None and b is None: return True
    if a is None or b is None: return False
    return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
def is_symmetric(root):
    return root is None or mirror(root.left, root.right)

# ---------- optimal 2: iterative, queue of pairs ----------
def is_symmetric_iter(root):
    if root is None: return True
    q = deque([(root.left, root.right)])
    while q:
        a, b = q.popleft()
        if a is None and b is None: continue
        if a is None or b is None or a.val != b.val: return False
        q.append((a.left, b.right))       # outer pair
        q.append((a.right, b.left))       # inner pair
    return True

# ---------- examples ----------
for arr in ([1, 2, 2, 3, 4, 4, 3], [1, 2, 2, None, 3, None, 3], [1, 2, 2, None, 3, 3], [1, 2, 3], [1]):
    r = build_tree(arr)
    print(arr, '->', is_symmetric(r), is_symmetric_iter(r))

# ---------- cross-check: every shape up to 7 nodes, every labelling with values {0, 1}; then values 0..2 on 5 nodes ----------
def relabel(shape_tree, vals):
    it = iter(vals)
    def go(t):
        if t is None: return None
        v = next(it); L = go(t[1]); return (v, L, go(t[2]))
    return go(shape_tree)
checked = sym_count = 0
for n in range(8):
    for s in shapes(n):
        base = label_pre(s)
        for vals in itertools.product((0, 1), repeat=n):
            t = relabel(base, vals); r = from_tuple(t)
            e = t == tmirror(t)
            assert is_symmetric(r) == is_symmetric_iter(r) == symmetric_brute(r) == e
            checked += 1; sym_count += e
print('labelled trees checked:', checked, '| symmetric among them:', sym_count)
for s in shapes(5):
    for vals in itertools.product((0, 1, 2), repeat=5):
        t = relabel(label_pre(s), vals); assert is_symmetric(from_tuple(t)) == (t == tmirror(t))

# ---------- why comparing inorder values is NOT enough: search for a counter-example ----------
def tin(t): return [] if t is None else tin(t[1]) + [t[0]] + tin(t[2])
found = None
for n in range(1, 6):
    for s in shapes(n):
        for vals in itertools.product((1, 2), repeat=n):
            t = relabel(label_pre(s), vals)
            if t != tmirror(t) and tin(t) == tin(t)[::-1]:
                found = t; break
        if found: break
    if found: break
r = from_tuple(found)
print('palindromic inorder but NOT symmetric:', to_level_order(r), 'inorder', tin(found))
assert not is_symmetric(r) and tin(found) == tin(found)[::-1]
# a bigger one: values 1,2,1 in a left chain also reads 1,2,1 in order
r2 = build_tree([2, 1, None, 2])  # left chain 2 -> 1 -> 2
print('left chain', to_level_order(r2), 'inorder', tin(to_tuple(r2)), 'symmetric:', is_symmetric(r2))

# ---------- random trees built to be symmetric, then perturbed ----------
random.seed(9)
def random_tuple(n, k=3):
    if n == 0: return None
    l = random.randint(0, n - 1)
    return (random.randint(0, k - 1), random_tuple(l, k), random_tuple(n - 1 - l, k))
for _ in range(500):
    half = random_tuple(random.randint(0, 20))
    t = (7, half, tmirror(half)); assert is_symmetric(from_tuple(t)) and is_symmetric_iter(from_tuple(t))
    if half is not None:                      # change one value on the right side
        u = (7, half, (tmirror(half)[0] + 1,) + tmirror(half)[1:]); r = from_tuple(u)
        assert not is_symmetric(r) and not is_symmetric_iter(r)
print('random ok: 500 symmetric, 500 perturbed')

# ---------- edge cases ----------
assert is_symmetric(None) and is_symmetric_iter(None)
assert is_symmetric(TreeNode(1)) and not is_symmetric(build_tree([1, 2]))
assert not is_symmetric(build_tree([1, None, 1]))
print('all asserts passed')
