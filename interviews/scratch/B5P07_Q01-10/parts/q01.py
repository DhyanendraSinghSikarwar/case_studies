# ---------- brute force: same idea with list.pop(0) (O(n) per pop, so O(n^2) overall) ----------
def build_slow(arr):
    arr = list(arr)
    while arr and arr[-1] is None:
        arr.pop()
    if not arr:
        return None
    root = TreeNode(arr.pop(0)); q = [root]
    while q and arr:
        node = q.pop(0)                      # the O(n) pop
        l = arr.pop(0) if arr else None
        r = arr.pop(0) if arr else None
        if l is not None: node.left = TreeNode(l); q.append(node.left)
        if r is not None: node.right = TreeNode(r); q.append(node.right)
    return root

# ---------- examples ----------
for arr in ([1, 2, 3, None, 4, None, None], [3, 9, 20, None, None, 15, 7], [], [1, None, 2, None, 3]):
    print(arr, '->', to_level_order(build_tree(arr)))

# ---------- == versus to_level_order ----------
a, b = build_tree([1, 2, 3]), build_tree([1, 2, 3])
print('a == b:', a == b, '| same shape and values:', to_level_order(a) == to_level_order(b))
assert not hasattr(a, '__dict__')            # __slots__: no per-node dict
try:
    a.extra = 1
except AttributeError:
    print('slots block new attributes')

# ---------- cross-check: every shape up to 7 nodes, then seeded random trees ----------
count = 0
for t in all_trees(7):
    root = from_tuple(t)
    arr = to_level_order(root)
    assert to_tuple(build_tree(arr)) == t
    assert to_tuple(build_slow(arr)) == t
    assert to_tuple(build_tree(arr + [None, None, None])) == t   # trailing nulls ignored
    assert to_level_order(build_tree(arr)) == arr
    count += 1
print('shapes round-tripped:', count)

random.seed(5)
def random_tuple(n, lo=-9, hi=9):
    if n == 0:
        return None
    l = random.randint(0, n - 1)
    return (random.randint(lo, hi), random_tuple(l), random_tuple(n - 1 - l))
for _ in range(500):
    t = random_tuple(random.randint(0, 40))
    arr = to_level_order(from_tuple(t))
    assert to_tuple(build_tree(arr)) == t == to_tuple(build_slow(arr))
print('random trees ok: 500')

# ---------- edge cases ----------
assert build_tree([]) is None and to_level_order(None) == []
assert build_tree([None]) is None            # a lone null is an empty tree
assert to_level_order(build_tree([7])) == [7]
# a long right chain (n = 10^4) builds without recursion
chain = [1]
for _ in range(9999):
    chain += [None, 1]
assert len(to_level_order(build_tree(chain))) == len(chain)
# cycle guard in the harness
c = TreeNode(1); c.left = c
try:
    to_level_order(c)
except AssertionError as e:
    print('guard fired:', e)
print('all asserts passed')
