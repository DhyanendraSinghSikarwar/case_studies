
def vertical_sorted(root):
    """Walk with BFS, record (col, row, val), sort, group by column. O(n log n)."""
    if root is None: return []
    rec, q = [], deque([(root, 0, 0)])
    while q:
        n, col, row = q.popleft(); rec.append((col, row, n.val))
        if n.left:  q.append((n.left, col - 1, row + 1))
        if n.right: q.append((n.right, col + 1, row + 1))
    rec.sort()                                         # column, then row, then value (the tie rule)
    out, last = [], None
    for col, row, v in rec:
        if col != last: out.append([]); last = col
        out[-1].append(v)
    return out

def vertical_first_come(root):
    """BFS with per-column buckets. Ties (same row and column) keep BFS order = left-to-right. O(n)."""
    if root is None: return []
    buckets, q = {}, deque([(root, 0)])
    while q:
        n, col = q.popleft(); buckets.setdefault(col, []).append(n.val)
        if n.left:  q.append((n.left, col - 1))
        if n.right: q.append((n.right, col + 1))
    return [buckets[c] for c in range(min(buckets), max(buckets) + 1)]

def vertical_dfs(root):
    """DFS version (explicit stack): the sort puts rows back in order, so DFS visiting order does not matter."""
    rec, st = [], [(root, 0, 0)] if root else []
    while st:
        n, col, row = st.pop(); rec.append((col, row, n.val))
        if n.right: st.append((n.right, col + 1, row + 1))
        if n.left:  st.append((n.left, col - 1, row + 1))
    rec.sort(); cols = {}
    for c, r, v in rec: cols.setdefault(c, []).append(v)
    return [cols[c] for c in sorted(cols)]

def vertical_tuple(t):
    """Independent brute force on tuple trees: for each column, nodes sorted by (row, value)."""
    nodes = []
    def go(t, c, r):
        if t is None: return
        nodes.append((c, r, t[0])); go(t[1], c - 1, r + 1); go(t[2], c + 1, r + 1)
    go(t, 0, 0)
    return [[v for (cc, r, v) in sorted(x for x in nodes if x[0] == c)] for c in sorted({x[0] for x in nodes})]

for arr, exp in [([3, 9, 20, None, None, 15, 7], [[9], [3, 15], [20], [7]]),
                 ([1, 2, 3, 4, 5, 6, 7], [[4], [2], [1, 5, 6], [3], [7]]),
                 ([3, 1, 4, 0, 2, 2], [[0], [1], [3, 2, 2], [4]]), ([], [])]:
    r = build_tree(arr); a = vertical_sorted(r)
    assert a == vertical_dfs(r) == exp, (arr, a)
    print(arr, "->", a)

# exhaustive over shapes up to 7 nodes with values from {0,1,2} so ties on (col,row) with different values occur
random.seed(28); cnt = diff = 0
for n in range(0, 8):
    for s in shapes(n):
        for _ in range(3):
            vals = iter(random.randint(0, 2) for _ in range(n))
            def lab(x):
                if x is None: return None
                L = lab(x[0]); v = next(vals); return (v, L, lab(x[1]))
            t = lab(s); r = from_tup(t)
            assert vertical_sorted(r) == vertical_dfs(r) == vertical_tuple(t)
            f = vertical_first_come(r)
            assert [sorted(c) for c in f] == [sorted(c) for c in vertical_sorted(r)]      # same groups, maybe different order inside a column
            assert [len(c) for c in f] == [len(c) for c in vertical_sorted(r)]
            if f != vertical_sorted(r): diff += 1
            cnt += 1
print("exhaustive+random ok:", cnt, "trees; first-come order differs from the sorted tie rule on", diff, "of them")
# one concrete difference
ex = build_tree([1, 2, 3, None, 5, 4])      # 5 and 4 share column 0 and row 2; 5 is left of 4 in BFS, but 4 < 5
print("tie example [1, 2, 3, None, 5, 4]: sorted rule", vertical_sorted(ex), "| first-come", vertical_first_come(ex))
big = build_tree([random.randint(0, 99) for _ in range(1000)])
assert vertical_sorted(big) == vertical_dfs(big) and sum(map(len, vertical_sorted(big))) == 1000
print("n = 1000 random tree: columns =", len(vertical_sorted(big)))
