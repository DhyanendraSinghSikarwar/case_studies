
def range_sum_full(root, low, high):
    """Brute force: visit every node."""
    return sum(n.val for n in nodes_of(root) if low <= n.val <= high)

VISITED = [0]
def range_sum_rec(root, low, high):
    """Prune with the BST order. Recursion depth = height (can be 2*10^4 on a skewed tree: see iterative)."""
    if root is None: return 0
    VISITED[0] += 1
    total = root.val if low <= root.val <= high else 0
    if root.val > low:  total += range_sum_rec(root.left, low, high)    # left values < root.val; useful only if root.val > low
    if root.val < high: total += range_sum_rec(root.right, low, high)   # right values > root.val; useful only if root.val < high
    return total

def range_sum_iter(root, low, high):
    total, visited, st = 0, 0, [root] if root else []
    while st:
        n = st.pop(); visited += 1
        if low <= n.val <= high: total += n.val
        if n.val > low and n.left:  st.append(n.left)
        if n.val < high and n.right: st.append(n.right)
    return total, visited

for arr, lo, hi, exp in [([10, 5, 15, 3, 7, None, 18], 7, 15, 32), ([10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10, 23),
                         ([10], 11, 20, 0), ([10, 5, 15], 5, 5, 5)]:
    r = build_tree(arr)
    VISITED[0] = 0
    a, b, c = range_sum_rec(r, lo, hi), range_sum_iter(r, lo, hi)[0], range_sum_full(r, lo, hi)
    assert a == b == c == exp, (arr, a, b, c)
    print(arr, lo, hi, "->", a, "| visited", VISITED[0], "of", len(nodes_of(r)))

# exhaustive: every BST shape up to 7 nodes (values 0..n-1 in inorder), every low <= high in a slightly wider range.
# Also test the visit-count claim: visited <= (nodes inside [low, high]) + 2 * height.
cases = worst_extra = 0
for n in range(1, 8):
    for s in shapes(n):
        r = from_tup(label_inorder(s)); h = height(r)
        for low in range(-1, n + 1):
            for high in range(low, n + 1):
                VISITED[0] = 0
                a = range_sum_rec(r, low, high); b, vis = range_sum_iter(r, low, high)
                assert a == b == range_sum_full(r, low, high) and VISITED[0] == vis
                inside = sum(1 for v in range(n) if low <= v <= high)
                assert vis <= inside + 2 * h, (s, low, high)
                worst_extra = max(worst_extra, vis - inside); cases += 1
print("exhaustive ok:", cases, "(tree, low, high) cases; largest visited-minus-inside =", worst_extra)

# random big-ish BSTs (random insertion order) vs brute force
def insert(root, v):
    if root is None: return TreeNode(v)
    cur = root
    while True:
        if v < cur.val:
            if cur.left is None: cur.left = TreeNode(v); break
            cur = cur.left
        else:
            if cur.right is None: cur.right = TreeNode(v); break
            cur = cur.right
    return root
random.seed(22)
for _ in range(300):
    vals = random.sample(range(-100, 100), random.randint(1, 60)); r = None
    for v in vals: r = insert(r, v)
    lo = random.randint(-110, 110); hi = random.randint(lo, 110)
    assert range_sum_rec(r, lo, hi) == range_sum_iter(r, lo, hi)[0] == range_sum_full(r, lo, hi) == sum(v for v in vals if lo <= v <= hi)
print("random cross-check ok (300 trees)")

# deep skewed tree, n = 2*10^4: recursion fails under the default limit, the iterative one is fine
chain = None
for v in range(20000, 0, -1): chain = TreeNode(v, None, chain)      # right chain 1..20000 (a valid BST)
try:
    range_sum_rec(chain, 5, 20000); print("recursive: no error")
except RecursionError:
    print("recursive on a 20000-node chain: RecursionError (default limit 1000)")
print("iterative on the same chain (sum, visited):", range_sum_iter(chain, 5, 20000))
assert range_sum_iter(chain, 5, 20000)[0] == sum(range(5, 20001))
print("pruned query [5, 10] on the chain visits", range_sum_iter(chain, 5, 10)[1], "nodes (the right spine stops once val >= high)")
