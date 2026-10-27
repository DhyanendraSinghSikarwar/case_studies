import itertools

CALLS = 0
def is_same(a, b):
    global CALLS
    CALLS += 1
    if a is None or b is None:
        return a is b
    return a.val == b.val and is_same(a.left, b.left) and is_same(a.right, b.right)

# ---------- brute force / O(n*m): try is_same at every node of root ----------
def is_subtree(root, sub):
    st = [root]
    while st:
        n = st.pop()
        if is_same(n, sub):
            return True
        for c in (n.left, n.right):
            if c: st.append(c)
    return False

# ---------- serialization: markers AND delimiters, then a substring test ----------
def ser(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None:
            out.append(",#"); continue
        out.append("," + str(n.val)); st.append(n.right); st.append(n.left)
    return "".join(out)                                # every token starts with a comma

def is_subtree_ser(root, sub):
    return ser(sub) in ser(root)

# ---------- the wrong version: no delimiters, no markers ----------
def naive(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        if n:
            out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return "".join(out)

# ---------- independent brute force on tuples ----------
def tsubs(t):
    if t is None: return []
    return [t] + tsubs(t[1]) + tsubs(t[2])
def subtree_brute(tr, ts):
    return any(x == ts for x in tsubs(tr))

examples = [([3, 4, 5, 1, 2], [4, 1, 2], True),
            ([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2], False),
            ([1, 1], [1], True), ([12], [2], False)]
for ra, sa, want in examples:
    r, s = build_tree(ra), build_tree(sa)
    assert is_subtree(r, s) == is_subtree_ser(r, s) == subtree_brute(tup(r), tup(s)) == want
    print("root=%s sub=%s -> %s" % (ra, sa, want))
print("naive concatenation: root [12] holds", repr(naive(build_tree([12]))), "and sub [2] holds", repr(naive(build_tree([2]))),
      "-> '2' in '12' is", naive(build_tree([2])) in naive(build_tree([12])), "(wrong)")
def ser_no_delim(root):                                # markers but NO delimiters
    out, st = [], [root]
    while st:
        n = st.pop()
        if n is None:
            out.append("#"); continue
        out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return "".join(out)
print("markers but no delimiters:", repr(ser_no_delim(build_tree([12]))), "vs", repr(ser_no_delim(build_tree([2]))),
      "-> substring test says", ser_no_delim(build_tree([2])) in ser_no_delim(build_tree([12])), "(wrong)")
print("with delimiters:", repr(ser(build_tree([12]))), "vs", repr(ser(build_tree([2]))),
      "-> substring test says", ser(build_tree([2])) in ser(build_tree([12])))

# exhaustive: all trees with 1..4 nodes (all shapes, values in {1, 2}) as both root and sub
trees = []
for n in range(1, 5):
    for s in shapes(n):
        for vals in itertools.product((1, 2), repeat=n):
            it = iter(vals)
            def put(sh): return None if sh is None else (next(it), put(sh[0]), put(sh[1]))
            trees.append(put(s))
cases = yes = 0
worst = 0.0
for ta in trees:
    ra = from_tup(ta)
    for tb in trees:
        rb = from_tup(tb)
        CALLS = 0
        a = is_subtree(ra, rb)
        n, m = len(tsubs(ta)), len(tsubs(tb))
        assert CALLS <= n * (2 * m + 1)                # each start node costs at most 2m + 1 calls
        worst = max(worst, CALLS / (n * m))
        b = is_subtree_ser(ra, rb)
        assert a == b == subtree_brute(ta, tb)
        cases += 1; yes += a
print("exhaustive ok:", cases, "(root, sub) pairs,", yes, "are True; is_same calls never exceed n*(2m+1)")

# the naive version really is wrong on small trees
bad = sum(1 for ta in trees for tb in trees
          if (naive(from_tup(tb)) in naive(from_tup(ta))) != subtree_brute(ta, tb))
print("naive string test wrong on", bad, "of", cases, "pairs (plain values concatenated, no markers, no delimiters)")

# random larger trees with a planted subtree
random.seed(19)
for _ in range(300):
    arr = [random.randint(0, 2)]
    for _ in range(random.randint(0, 25)):
        arr.append(None if random.random() < 0.3 else random.randint(0, 2))
    r = build_tree(arr)
    sub = random.choice(all_nodes(r)) if random.random() < 0.5 else build_tree([random.randint(0, 2), random.randint(0, 2)])
    assert is_subtree(r, sub) == is_subtree_ser(r, sub) == subtree_brute(tup(r), tup(sub))
print("random ok: 300 trees")

# worst case for O(n*m): all ones with a different last value
n_, m_ = 400, 200
a = chain(n_); b = chain(m_)
for x in all_nodes(a): x.val = 1
for x in all_nodes(b): x.val = 1
tail = b
while tail.right: tail = tail.right
tail.val = 2                                          # sub ends in a 2, root never has one
CALLS = 0
print("chain n=%d, sub chain m=%d: found =" % (n_, m_), is_subtree(a, b), "| is_same calls =", CALLS, "| n*m =", n_ * m_)
