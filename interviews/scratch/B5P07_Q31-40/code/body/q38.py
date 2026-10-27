# ---------- the required format: level order, '#' for every missing child, nothing trimmed ----------
def serialize(root):
    if root is None:
        return "#"
    out, q = [str(root.val)], deque([root])
    while q:
        n = q.popleft()
        for c in (n.left, n.right):
            if c is None:
                out.append("#")
            else:
                out.append(str(c.val)); q.append(c)
    return ",".join(out)

def deserialize(s):
    tok = s.split(",")
    if tok[0] == "#":
        assert len(tok) == 1
        return None
    root = TreeNode(int(tok[0]))
    q, i = deque([root]), 1
    while q:
        n = q.popleft()
        for side in ("left", "right"):
            if tok[i] != "#":
                c = TreeNode(int(tok[i])); setattr(n, side, c); q.append(c)
            i += 1
    assert i == len(tok), "leftover tokens"
    return root

# ---------- brute force / cross-check format: preorder with '#' (a different, equally valid encoding) ----------
def ser_pre(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None: out.append("#"); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return ",".join(out)

for arr in ([1, 2, 3, None, None, 4, 5], [], [1], [1, None, 2]):
    s = serialize(build(arr))
    assert same(deserialize(s), build(arr))
    print(f"root={arr} -> '{s}'")

# exhaustive: every shape with 0..8 nodes, negative / multi-digit values; round trip + exactly 2n+1 tokens
cases = 0
for n in range(9):
    for sh in shapes(n):
        t = label(sh, "pre", step=-7)               # values 0, -7, -14, ... (negatives and two digits)
        root = from_tup(t)
        s = serialize(root)
        assert len(s.split(",")) == 2 * n + 1        # n values + (n + 1) '#' markers
        assert s.count("#") == n + 1
        assert same(deserialize(s), root)
        assert s == serialize(deserialize(s))        # canonical: serialize(deserialize(s)) == s
        assert ser_pre(root).count("#") == n + 1     # the preorder encoding has the same token count
        cases += 1
print("exhaustive shapes ok:", cases)

# the trimmed array form used by the examples is a different, shorter thing
root = build([1, 2, 3, None, None, 4, 5])
print("trimmed array:", len(to_arr(root)), "entries | full serialization:", len(serialize(root).split(",")), "tokens")

# n = 10^4 skewed tree: BFS and the parser are iterative, so no recursion limit is touched
chain_root = None
for i in range(10**4):
    chain_root = TreeNode(i, chain_root, None)
s = serialize(chain_root)
assert len(s.split(",")) == 2 * 10**4 + 1 and same(deserialize(s), chain_root)
print("10^4-node left chain: round trip ok,", len(s.split(",")), "tokens")

# random trees
random.seed(3)
for _ in range(300):
    n = random.randint(0, 60)
    root = None if n == 0 else TreeNode(random.randint(-99, 99))
    pool = [root] if root else []
    for _ in range(n - 1):
        par = random.choice(pool); side = random.choice(("left", "right"))
        if getattr(par, side) is None:
            c = TreeNode(random.randint(-99, 99)); setattr(par, side, c); pool.append(c)
    assert same(deserialize(serialize(root)), root)
print("300 random trees ok")
