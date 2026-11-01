# Runs EVERY example rendered into the Part 7 prompts (qs.py is the single source of truth) against node-based reference solutions,
# and cross-checks each reference against independent brute force on tuple-encoded trees, exhaustively over all tree shapes with
# 0..7 nodes (626 shapes in total for n<=7) plus seeded random cases. Run: python3 -I check_examples.py
import sys, os, random, itertools, heapq
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qs import QS
random.seed(7)

class TreeNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(s, val=0, left=None, right=None): s.val = val; s.left = left; s.right = right
class ListNode:
    __slots__ = ('val', 'next')
    def __init__(s, val=0, next=None): s.val = val; s.next = next

def build_tree(arr):
    arr = list(arr)
    if not arr or arr[0] is None: return None
    root = TreeNode(arr[0]); q = deque([root]); i = 1
    while q and i < len(arr):
        nd = q.popleft()
        if i < len(arr) and arr[i] is not None: nd.left = TreeNode(arr[i]); q.append(nd.left)
        i += 1
        if i < len(arr) and arr[i] is not None: nd.right = TreeNode(arr[i]); q.append(nd.right)
        i += 1
    return root
def to_arr(root):
    if root is None: return []
    out = []; q = deque([root])
    while q:
        nd = q.popleft()
        if nd is None: out.append(None); continue
        out.append(nd.val); q.append(nd.left); q.append(nd.right)
    while out and out[-1] is None: out.pop()
    return out
def tup(root): return None if root is None else (root.val, tup(root.left), tup(root.right))
def from_tup(t): return None if t is None else TreeNode(t[0], from_tup(t[1]), from_tup(t[2]))
def nodes_of(root):
    out = []; st = [root] if root else []
    while st:
        n = st.pop(); out.append(n)
        for c in (n.right, n.left):
            if c: st.append(c)
    return out
def count_nodes(root): return len(nodes_of(root))

# ---- shape enumeration
_sh = {0: [None]}
def shapes(n):
    if n in _sh: return _sh[n]
    out = []
    for l in range(n):
        for L in shapes(l):
            for R in shapes(n - 1 - l): out.append((L, R))
    _sh[n] = out; return out
def label(shape, mode):
    c = [0]
    def go(s):
        if s is None: return None
        if mode == 'pre':
            v = c[0]; c[0] += 1; L = go(s[0]); R = go(s[1]); return (v, L, R)
        L = go(s[0]); v = c[0]; c[0] += 1; R = go(s[1]); return (v, L, R)
    return go(shape)
MAXN = 7
ALL_PRE = [label(s, 'pre') for n in range(MAXN + 1) for s in shapes(n)]
ALL_IN = [label(s, 'in') for n in range(MAXN + 1) for s in shapes(n)]
print('shapes up to', MAXN, '=', len(ALL_PRE))

# ---- tuple helpers (brute force side)
def paths_leaf(t, pre=()):
    if t is None: return []
    p = pre + (t[0],)
    if t[1] is None and t[2] is None: return [p]
    return paths_leaf(t[1], p) + paths_leaf(t[2], p)
def tmirror(t): return None if t is None else (t[0], tmirror(t[2]), tmirror(t[1]))
def tpre(t): return [] if t is None else [t[0]] + tpre(t[1]) + tpre(t[2])
def tin(t): return [] if t is None else tin(t[1]) + [t[0]] + tin(t[2])
def tpost(t): return [] if t is None else tpost(t[1]) + tpost(t[2]) + [t[0]]
def theight(t): return 0 if t is None else 1 + max(theight(t[1]), theight(t[2]))
def tsize(t): return 0 if t is None else 1 + tsize(t[1]) + tsize(t[2])
def graph(t):
    """undirected adjacency over positions (path strings) for brute force"""
    adj = {}; val = {}
    def go(t, pos, par):
        if t is None: return
        val[pos] = t[0]; adj.setdefault(pos, [])
        if par is not None: adj[pos].append(par); adj[par].append(pos)
        go(t[1], pos + 'L', pos); go(t[2], pos + 'R', pos)
    go(t, 'r', None); return adj, val
def bfs_dist(adj, s):
    d = {s: 0}; q = deque([s])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return d
def tpos(t):
    """list of (depth, col, rowindex-heap-id, val, path) for all nodes"""
    out = []
    def go(t, d, c, idx, path):
        if t is None: return
        out.append((d, c, idx, t[0], path)); go(t[1], d + 1, c - 1, 2 * idx, path + 'L'); go(t[2], d + 1, c + 1, 2 * idx + 1, path + 'R')
    go(t, 0, 0, 1, ''); return out

# ---- reference solutions on nodes
def r_max_depth(root):
    if not root: return 0
    return 1 + max(r_max_depth(root.left), r_max_depth(root.right))
def r_same(p, q):
    if p is None or q is None: return p is q
    return p.val == q.val and r_same(p.left, q.left) and r_same(p.right, q.right)
def r_invert(root):
    if root: root.left, root.right = r_invert(root.right), r_invert(root.left)
    return root
def r_sym(root):
    def m(a, b):
        if a is None or b is None: return a is b
        return a.val == b.val and m(a.left, b.right) and m(a.right, b.left)
    return root is None or m(root.left, root.right)
def r_lca_bst(root, p, q):
    cur = root
    while cur:
        if p < cur.val and q < cur.val: cur = cur.left
        elif p > cur.val and q > cur.val: cur = cur.right
        else: return cur.val
def r_path_leaf(root, target):
    if not root: return False
    if not root.left and not root.right: return root.val == target
    return r_path_leaf(root.left, target - root.val) or r_path_leaf(root.right, target - root.val)
def r_pre(root): return [] if not root else [root.val] + r_pre(root.left) + r_pre(root.right)
def it_pre(root):
    out = []; st = [root] if root else []
    while st:
        n = st.pop(); out.append(n.val)
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out
def it_in(root):
    out = []; st = []; cur = root
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); out.append(cur.val); cur = cur.right
    return out
def it_post(root):
    out = []; st = []; cur = root; last = None
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        top = st[-1]
        if top.right and last is not top.right: cur = top.right
        else: out.append(top.val); last = st.pop()
    return out
def it_post2(root):
    out = []; st = [root] if root else []
    while st:
        n = st.pop(); out.append(n.val)
        if n.left: st.append(n.left)
        if n.right: st.append(n.right)
    return out[::-1]
def r_levels(root):
    out = []; q = deque([root] if root else [])
    while q:
        lv = []
        for _ in range(len(q)):
            n = q.popleft(); lv.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        out.append(lv)
    return out
def r_balanced(root):
    def h(n):
        if not n: return 0
        a = h(n.left)
        if a < 0: return -1
        b = h(n.right)
        if b < 0 or abs(a - b) > 1: return -1
        return 1 + max(a, b)
    return h(root) >= 0
def r_diameter(root):
    best = [0]
    def h(n):
        if not n: return 0
        a, b = h(n.left), h(n.right); best[0] = max(best[0], a + b); return 1 + max(a, b)
    h(root); return best[0]
def r_valid_bst(root):
    def go(n, lo, hi):
        if not n: return True
        if (lo is not None and n.val <= lo) or (hi is not None and n.val >= hi): return False
        return go(n.left, lo, n.val) and go(n.right, n.val, hi)
    return go(root, None, None)
def r_lca(root, p, q):
    def go(n):
        if not n or n.val in (p, q): return n
        l, r = go(n.left), go(n.right)
        return n if l and r else (l or r)
    return go(root).val
def r_right_view(root):
    out = []
    def go(n, d):
        if not n: return
        if d == len(out): out.append(n.val)
        go(n.right, d + 1); go(n.left, d + 1)
    go(root, 0); return out
def r_kth(root, k):
    st = []; cur = root
    while True:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop(); k -= 1
        if k == 0: return cur.val
        cur = cur.right
def r_build_pre_in(pre, ino):
    idx = {v: i for i, v in enumerate(ino)}; it = iter(pre)
    def go(lo, hi):
        if lo > hi: return None
        v = next(it); nd = TreeNode(v); m = idx[v]
        nd.left = go(lo, m - 1); nd.right = go(m + 1, hi); return nd
    return go(0, len(ino) - 1)
def r_build_in_post(ino, post):
    idx = {v: i for i, v in enumerate(ino)}; pos = [len(post) - 1]
    def go(lo, hi):
        if lo > hi: return None
        v = post[pos[0]]; pos[0] -= 1; nd = TreeNode(v); m = idx[v]
        nd.right = go(m + 1, hi); nd.left = go(lo, m - 1); return nd
    return go(0, len(ino) - 1)
def r_maxpath(root):
    best = [None]
    def go(n):
        if not n: return 0
        l = max(go(n.left), 0); r = max(go(n.right), 0)
        s = n.val + l + r
        if best[0] is None or s > best[0]: best[0] = s
        return n.val + max(l, r)
    go(root); return best[0]
def ser(root):
    out = []; st = [root]
    while st:
        n = st.pop()
        if n is None: out.append('#')
        else: out.append(str(n.val)); st.append(n.right); st.append(n.left)
    return ','.join(out)
def deser(s):
    toks = s.split(','); i = 0
    root = TreeNode(0); stack = []   # iterative: frames [node, side]
    if toks[0] == '#': return None
    root = TreeNode(int(toks[0])); i = 1; stack = [[root, 0]]
    while stack:
        fr = stack[-1]
        if fr[1] == 2: stack.pop(); continue
        t = toks[i]; i += 1
        child = None if t == '#' else TreeNode(int(t))
        if fr[1] == 0: fr[0].left = child
        else: fr[0].right = child
        fr[1] += 1
        if child: stack.append([child, 0])
    assert i == len(toks)
    return root
def bfs_ser(root):
    out = []; q = deque([root])
    while q:
        n = q.popleft()
        if n is None: out.append('#'); continue
        out.append(str(n.val)); q.append(n.left); q.append(n.right)
    return ','.join(out)
def bfs_deser(s):
    toks = s.split(',')
    if toks[0] == '#': return None
    root = TreeNode(int(toks[0])); q = deque([root]); i = 1
    while q:
        n = q.popleft()
        for side in ('left', 'right'):
            t = toks[i]; i += 1
            if t != '#':
                c = TreeNode(int(t)); setattr(n, side, c); q.append(c)
    assert i == len(toks); return root
def r_is_subtree(root, sub):
    st = [root]
    while st:
        n = st.pop()
        if n is None: continue
        if r_same(n, sub): return True
        st.append(n.left); st.append(n.right)
    return False
def r_min_depth(root):
    if not root: return 0
    q = deque([(root, 1)])
    while q:
        n, d = q.popleft()
        if not n.left and not n.right: return d
        if n.left: q.append((n.left, d + 1))
        if n.right: q.append((n.right, d + 1))
def r_sorted_to_bst(nums, lo=0, hi=None):
    if hi is None: hi = len(nums) - 1
    if lo > hi: return None
    m = (lo + hi) // 2
    return TreeNode(nums[m], r_sorted_to_bst(nums, lo, m - 1), r_sorted_to_bst(nums, m + 1, hi))
def list_to_bst(head):
    n = 0; p = head
    while p: n += 1; p = p.next
    cur = [head]
    # simpler: left size = (cnt-1)//2, right size = cnt-1-left size
    def go2(cnt):
        if cnt <= 0: return None
        ls = (cnt - 1) // 2
        left = go2(ls); nd = TreeNode(cur[0].val); cur[0] = cur[0].next
        nd.left = left; nd.right = go2(cnt - 1 - ls); return nd
    return go2(n)
def list_to_bst_mid(head):
    if head is None: return None
    if head.next is None: return TreeNode(head.val)
    # slow/fast with prev; lower-middle rule: for cnt elements the root index is (cnt-1)//2
    slow = fast = head; prev = None
    while fast and fast.next:
        prev = slow; slow = slow.next; fast = fast.next.next
    # for even cnt, slow is the upper middle; step back to lower middle
    if fast is None:  # even count: slow = index cnt/2 ; lower middle is prev
        mid = prev
        pp = head
        if pp is mid:
            left_head = None
        else:
            while pp.next is not mid: pp = pp.next
            pp.next = None; left_head = head
        right_head = mid.next; mid.next = None
        nd = TreeNode(mid.val)
    else:
        prev.next = None; left_head = head; right_head = slow.next; nd = TreeNode(slow.val)
    nd.left = list_to_bst_mid(left_head); nd.right = list_to_bst_mid(right_head); return nd
def mk_list(a):
    d = ListNode(); t = d
    for v in a: t.next = ListNode(v); t = t.next
    return d.next
def r_range_sum(root, lo, hi):
    if not root: return 0
    if root.val < lo: return r_range_sum(root.right, lo, hi)
    if root.val > hi: return r_range_sum(root.left, lo, hi)
    return root.val + r_range_sum(root.left, lo, hi) + r_range_sum(root.right, lo, hi)
def r_insert(root, val):
    if not root: return TreeNode(val)
    cur = root
    while True:
        if val < cur.val:
            if cur.left is None: cur.left = TreeNode(val); break
            cur = cur.left
        else:
            if cur.right is None: cur.right = TreeNode(val); break
            cur = cur.right
    return root
def cost(root):
    visits = 0; best_rec = [0]
    def go(n, d):
        nonlocal visits
        visits += 1; best_rec[0] = max(best_rec[0], d)
        if n.left: go(n.left, d + 1)
        if n.right: go(n.right, d + 1)
    if root: go(root, 1)
    st = []; cur = root; ms = 0
    while st or cur:
        while cur: st.append(cur); ms = max(ms, len(st)); cur = cur.left
        cur = st.pop(); cur = cur.right
    q = deque([root] if root else []); mq = len(q)
    while q:
        n = q.popleft()
        for c in (n.left, n.right):
            if c: q.append(c); mq = max(mq, len(q))
    return (visits, best_rec[0], ms, mq)
def r_zigzag(root):
    ls = r_levels(root); return [l[::-1] if i % 2 else l for i, l in enumerate(ls)]
def r_path_all(root, target):
    out = []; path = []
    def go(n, rem):
        if not n: return
        path.append(n.val)
        if not n.left and not n.right and rem == n.val: out.append(path[:])
        go(n.left, rem - n.val); go(n.right, rem - n.val); path.pop()
    go(root, target); return out
def r_path_count(root, target):
    cnt = {0: 1}; ans = [0]
    def go(n, pre):
        if not n: return
        pre += n.val; ans[0] += cnt.get(pre - target, 0); cnt[pre] = cnt.get(pre, 0) + 1
        go(n.left, pre); go(n.right, pre); cnt[pre] -= 1
    go(root, 0); return ans[0]
def r_vertical(root):
    rec = []
    q = deque([(root, 0, 0)] if root else [])
    while q:
        n, r, c = q.popleft(); rec.append((c, r, n.val))
        if n.left: q.append((n.left, r + 1, c - 1))
        if n.right: q.append((n.right, r + 1, c + 1))
    rec.sort(); out = []
    for c in sorted({x[0] for x in rec}): out.append([v for cc, r, v in rec if cc == c])
    return out
class BSTIter:
    def __init__(s, root): s.st = []; s.maxst = 0; s._push(root)
    def _push(s, n):
        while n: s.st.append(n); n = n.left
        s.maxst = max(s.maxst, len(s.st))
    def next(s):
        n = s.st.pop(); s._push(n.right); return n.val
    def hasNext(s): return bool(s.st)
def r_delete(root, key):
    if not root: return None
    if key < root.val: root.left = r_delete(root.left, key)
    elif key > root.val: root.right = r_delete(root.right, key)
    else:
        if not root.left: return root.right
        if not root.right: return root.left
        s = root.right
        while s.left: s = s.left
        root.val = s.val; root.right = r_delete(root.right, s.val)
    return root
def r_succ(root, p):
    best = None; cur = root
    while cur:
        if p < cur.val: best = cur.val; cur = cur.left
        else: cur = cur.right
    return best
def r_two_sum(root, k):
    a = it_in(root); i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == k: return True
        if s < k: i += 1
        else: j -= 1
    return False
SPINE = [0]
def r_count_complete(root):
    def lh(n):
        c = 0
        while n.left: n = n.left; c += 1; SPINE[0] += 1
        return c
    def rh(n):
        c = 0
        while n.right: n = n.right; c += 1; SPINE[0] += 1
        return c
    def go(n):
        if not n: return 0
        a, b = lh(n), rh(n)
        if a == b: return 2 ** (a + 1) - 1
        return 1 + go(n.left) + go(n.right)
    return go(root)
def r_deep(n, shape):
    root = None
    for i in range(n):
        root = TreeNode(i, root, None) if shape == 'left' else TreeNode(i, None, root)
    def rec(nd): return 0 if nd is None else 1 + rec(nd.left or nd.right)
    try: a = rec(root)
    except RecursionError: a = 'RecursionError'
    d = 0; st = [(root, 1)] if root else []
    while st:
        nd, k = st.pop(); d = max(d, k)
        if nd.left: st.append((nd.left, k + 1))
        if nd.right: st.append((nd.right, k + 1))
    return (a, d)
def r_flatten(root):
    cur = root
    while cur:
        if cur.left:
            p = cur.left
            while p.right: p = p.right
            p.right = cur.right; cur.right = cur.left; cur.left = None
        cur = cur.right
    return root
def r_dist_k(root, target, k):
    par = {root: None}; st = [root]; tn = None
    while st:
        n = st.pop()
        if n.val == target: tn = n
        for c in (n.left, n.right):
            if c: par[c] = n; st.append(c)
    seen = {tn}; fr = [tn]
    for _ in range(k):
        nf = []
        for n in fr:
            for m in (n.left, n.right, par[n]):
                if m and m not in seen: seen.add(m); nf.append(m)
        fr = nf
    return sorted(n.val for n in fr)
def r_recover(root):
    st = []; cur = root; prev = first = second = None
    while st or cur:
        while cur: st.append(cur); cur = cur.left
        cur = st.pop()
        if prev and prev.val > cur.val:
            if not first: first = prev
            second = cur
        prev = cur; cur = cur.right
    first.val, second.val = second.val, first.val
    return root
def r_nary_parse(arr):
    class Node:
        def __init__(s, v): s.val = v; s.children = []
    if not arr: return None
    root = Node(arr[0]); q = deque([root]); i = 2
    while q and i <= len(arr):
        n = q.popleft()
        while i < len(arr) and arr[i] is not None:
            c = Node(arr[i]); n.children.append(c); q.append(c); i += 1
        i += 1
    return root
def r_nary(arr):
    root = r_nary_parse(arr)
    if not root: return ([], [], [], 0)
    pre = []; post = []
    st = [(root, 0)]
    while st:
        n, i = st.pop()
        if i == 0: pre.append(n.val)
        if i < len(n.children): st.append((n, i + 1)); st.append((n.children[i], 0))
        else: post.append(n.val)
    lv = []; q = [root]
    while q:
        lv.append([n.val for n in q]); q = [c for n in q for c in n.children]
    return (pre, post, lv, len(lv))
def r_trie(words, queries):
    root = {}; nodes = 0
    for w in words:
        cur = root
        for ch in w:
            if ch not in cur: cur[ch] = {'#': 0}; nodes += 1
            cur = cur[ch]; cur['#'] += 1
    res = []
    for q in queries:
        cur = root; ok = True
        for ch in q:
            if ch not in cur: ok = False; break
            cur = cur[ch]
        res.append(cur['#'] if ok else 0)
    return (res, nodes)
def r_classify(nodes):
    objs = [TreeNode(v) for v, l, r in nodes]
    for o, (v, l, r) in zip(objs, nodes):
        o.left = objs[l] if l != -1 else None; o.right = objs[r] if r != -1 else None
    seen = set(); shared = False
    # cycle detection by colouring (iterative)
    state = {}; st = [(objs[0], 0)]
    cap = 10 * len(objs) + 10; steps = 0
    while st:
        steps += 1; assert steps < cap
        n, i = st.pop()
        if i == 0:
            if id(n) in state:
                if state[id(n)] == 1: return 'cycle'
                shared = True; continue
            state[id(n)] = 1
            st.append((n, 1))
            for c in (n.right, n.left):
                if c: st.append((c, 0))
        else: state[id(n)] = 2
    return 'shared' if shared else 'tree'
def r_max_width(root):
    if not root: return 0
    best = 0; lv = [(root, 0)]
    while lv:
        best = max(best, lv[-1][1] - lv[0][1] + 1); base = lv[0][1]; nxt = []
        for n, i in lv:
            i -= base
            if n.left: nxt.append((n.left, 2 * i))
            if n.right: nxt.append((n.right, 2 * i + 1))
        lv = nxt
    return best
def r_bst_pre(pre):
    it = [0]
    def go(bound):
        if it[0] == len(pre) or pre[it[0]] > bound: return None
        nd = TreeNode(pre[it[0]]); it[0] += 1
        nd.left = go(nd.val); nd.right = go(bound); return nd
    return go(float('inf'))
def r_rob(root):
    def go(n):
        if not n: return (0, 0)
        a, b = go(n.left), go(n.right)
        return (n.val + a[1] + b[1], max(a) + max(b))
    return max(go(root))
def r_dll(root):
    prev = [None]; head = [None]
    def go(n):
        if not n: return
        go(n.left)
        if prev[0]: prev[0].right = n; n.left = prev[0]
        else: head[0] = n
        prev[0] = n; go(n.right)
    go(root)
    if head[0]: head[0].left = prev[0]; prev[0].right = head[0]
    return head[0]
def r_deepest(root):
    def go(n):
        if not n: return (0, None)
        a, b = go(n.left), go(n.right)
        if a[0] == b[0]: return (a[0] + 1, n)
        return (max(a[0], b[0]) + 1, a[1] if a[0] > b[0] else b[1])
    return go(root)[1]
def r_morris(root):
    out = []; cur = root; it = 0
    while cur:
        it += 1
        if not cur.left: out.append(cur.val); cur = cur.right
        else:
            p = cur.left
            while p.right and p.right is not cur: p = p.right
            if p.right is None: p.right = cur; cur = cur.left
            else: p.right = None; out.append(cur.val); cur = cur.right
    return out, it
def r_boundary(root):
    if not root: return []
    out = [root.val]
    def leaf(n): return not n.left and not n.right
    left = []; n = root.left
    while n and not leaf(n):
        left.append(n.val); n = n.left or n.right
    leaves = []; st = [root]
    while st:
        n = st.pop()
        if leaf(n) and n is not root: leaves.append(n.val)
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    right = []; n = root.right
    while n and not leaf(n):
        right.append(n.val); n = n.right or n.left
    return out + left + leaves + right[::-1]
def r_cameras(root):
    ans = [0]
    def go(n):   # 0 not watched, 1 camera, 2 watched
        if not n: return 2
        a, b = go(n.left), go(n.right)
        if a == 0 or b == 0: ans[0] += 1; return 1
        return 2 if (a == 1 or b == 1) else 0
    if go(root) == 0: ans[0] += 1
    return ans[0]

# ---- solver wrappers keyed like qs.py: take example kwargs, return comparable result
def B(a): return build_tree(a)
SOLVE = {
 'build_roundtrip': lambda arr: to_arr(build_tree(arr)),
 'max_depth': lambda root: r_max_depth(B(root)),
 'same_tree': lambda p, q: r_same(B(p), B(q)),
 'invert': lambda root: (lambda t: (lambda ids0: (lambda r: (to_arr(r), set(map(id, nodes_of(r))) == ids0)[0])(r_invert(t)))(set(map(id, nodes_of(t)))))(B(root)),
 'symmetric': lambda root: r_sym(B(root)),
 'lca_bst': lambda root, p, q: r_lca_bst(B(root), p, q),
 'path_sum_leaf': lambda root, target: r_path_leaf(B(root), target),
 'traversals3': lambda root: (it_pre(B(root)), it_in(B(root)), it_post(B(root))),
 'level_order': lambda root: r_levels(B(root)),
 'is_balanced': lambda root: r_balanced(B(root)),
 'diameter': lambda root: r_diameter(B(root)),
 'is_valid_bst': lambda root: r_valid_bst(B(root)),
 'lca_tree': lambda root, p, q: r_lca(B(root), p, q),
 'right_view': lambda root: r_right_view(B(root)),
 'kth_smallest_bst': lambda root, k: r_kth(B(root), k),
 'build_pre_in': lambda preorder, inorder: to_arr(r_build_pre_in(preorder, inorder)),
 'max_path_sum': lambda root: r_maxpath(B(root)),
 'serde_preorder': lambda arr: to_arr(deser(ser(B(arr)))),
 'is_subtree': lambda root, sub: r_is_subtree(B(root), B(sub)),
 'min_depth': lambda root: r_min_depth(B(root)),
 'sorted_to_bst': lambda nums: to_arr(r_sorted_to_bst(nums)),
 'range_sum_bst': lambda root, low, high: r_range_sum(B(root), low, high),
 'bst_insert': lambda root, val: to_arr(r_insert(B(root), val)),
 'traversal_cost': lambda root: cost(B(root)),
 'zigzag': lambda root: r_zigzag(B(root)),
 'path_sum_all': lambda root, target: r_path_all(B(root), target),
 'path_sum_count': lambda root, target: r_path_count(B(root), target),
 'vertical_order': lambda root: r_vertical(B(root)),
 'build_in_post': lambda inorder, postorder: to_arr(r_build_in_post(inorder, postorder)),
 'bst_iterator': lambda root, ops: (lambda it: [getattr(it, o)() for o in ops])(BSTIter(B(root))),
 'bst_delete': lambda root, key: to_arr(r_delete(B(root), key)),
 'inorder_successor': lambda root, p: r_succ(B(root), p),
 'two_sum_bst': lambda root, k: r_two_sum(B(root), k),
 'count_complete': lambda root: r_count_complete(B(root)),
 'deep_skew': lambda n, shape: r_deep(n, shape),
 'flatten': lambda root: (lambda r: (lambda out: out)([ (lambda c: c)(0) ] and (lambda r2: [x for x in chain_vals(r2)])(r)))(r_flatten(B(root))),
 'distance_k': lambda root, target, k: r_dist_k(B(root), target, k),
 'bfs_serde': lambda root: bfs_ser(B(root)),
 'recover_bst': lambda root: to_arr(r_recover(B(root))),
 'nary': lambda arr: r_nary(arr),
 'trie_counts': lambda words, queries: r_trie(words, queries),
 'classify': lambda nodes: r_classify(nodes),
 'max_width': lambda root: r_max_width(B(root)),
 'bst_from_preorder': lambda preorder: to_arr(r_bst_pre(preorder)),
 'rob_tree': lambda root: r_rob(B(root)),
 'bst_to_dll': lambda root: (lambda h: [] if h is None else (lambda vals: vals)(dll_vals(h, count_nodes_dll(h))))(r_dll(B(root))),
 'deepest_subtree': lambda root: to_arr(r_deepest(B(root))),
 'morris_inorder': lambda root: r_morris(B(root)),
 'boundary': lambda root: r_boundary(B(root)),
 'min_cameras': lambda root: r_cameras(B(root)),
}
def chain_vals(r):
    out = []
    while r: assert r.left is None; out.append(r.val); r = r.right; assert len(out) < 10**6
    return out
def count_nodes_dll(h):
    n = 1; p = h.right
    while p is not h: n += 1; p = p.right; assert n < 10**6
    return n
def dll_vals(h, n):
    out = []; p = h
    for _ in range(n): out.append(p.val); p = p.right
    assert p is h
    # backward check
    q = h.left; back = []
    for _ in range(n): back.append(q.val); q = q.left
    assert back[::-1] == out
    return out

def render(v): return repr(v).replace('None', 'null')
def example_text(ex):
    parts = []
    for kw, out in ex: parts.append(', '.join(f"{k}={render(v)}" for k, v in kw.items()) + ' -> ' + render(out))
    return '; '.join(parts)

if __name__ == '__main__':
    assert len(QS) == 50 and len({q[2] for q in QS}) == 50, len(QS)
    assert set(SOLVE) == {q[2] for q in QS}, set(SOLVE) ^ {q[2] for q in QS}
    nex = 0
    for s, d, key, text, ex, asked in QS:
        for kw, out in ex:
            got = SOLVE[key](**kw); nex += 1
            assert got == out, (key, kw, got, out)
    print('examples ok:', nex)

    # ===== independent brute-force cross-checks, exhaustive over shapes =====
    # tuple helpers for brute versions
    def brute_depth(t): return max([len(p) for p in paths_leaf(t)], default=0)
    for t in ALL_PRE:
        r = from_tup(t); n = tsize(t)
        assert to_arr(build_tree(to_arr(r))) == to_arr(r) and tup(build_tree(to_arr(r))) == t         # build_roundtrip
        assert r_max_depth(r) == brute_depth(t) == theight(t)
        assert r_same(from_tup(t), from_tup(t)) and (t is None or r is not from_tup(t))
        assert r_sym(r) == (t == tmirror(t) if t is None else (t[1] == tmirror(t[2])))
        inv = r_invert(from_tup(t)); assert tup(inv) == tmirror(t)
        assert (it_pre(r), it_in(r), it_post(r), it_post2(r)) == (tpre(t), tin(t), tpost(t), tpost(t))
        # levels brute from positions
        pos = tpos(t); lv = {}
        for d, c, idx, v, path in pos: lv.setdefault(d, []).append((path.replace('L', '0').replace('R', '1'), v))
        exp = [[v for p, v in sorted(lv[d])] for d in sorted(lv)]
        assert r_levels(r) == exp, (t, r_levels(r), exp)
        assert r_zigzag(r) == [l[::-1] if i % 2 else l for i, l in enumerate(exp)]
        assert r_right_view(r) == [l[-1] for l in exp]
        # balanced brute: heights at every node
        def allbal(t):
            if t is None: return True
            return abs(theight(t[1]) - theight(t[2])) <= 1 and allbal(t[1]) and allbal(t[2])
        assert r_balanced(r) == allbal(t)
        # diameter brute: max graph distance
        adj, val = graph(t)
        dm = max([max(bfs_dist(adj, s).values()) for s in adj], default=0)
        assert r_diameter(r) == dm, (t, r_diameter(r), dm)
        # min depth brute
        assert r_min_depth(r) == min([len(p) for p in paths_leaf(t)], default=0)
        # path sums: all leaf paths and all downward paths brute
        for target in range(-1, 12):
            lp = paths_leaf(t)
            assert r_path_leaf(r, target) == any(sum(p) == target for p in lp)
            assert r_path_all(r, target) == [list(p) for p in lp if sum(p) == target]
            # downward count brute: every node as start, walk all downward
            cnt = [0]
            def sub(t):
                if t is None: return
                def walk(u, s):
                    if u is None: return
                    s += u[0]; cnt[0] += (s == target); walk(u[1], s); walk(u[2], s)
                walk(t, 0); sub(t[1]); sub(t[2])
            sub(t); assert r_path_count(r, target) == cnt[0]
        # vertical order brute
        vo = {}
        for d, c, idx, v, path in pos: vo.setdefault(c, []).append((d, v))
        assert r_vertical(r) == [[v for d, v in sorted(vo[c])] for c in sorted(vo)]
        # max path sum brute over node pairs (values can be negative here)
        # width brute
        best = 0
        for d in {p[0] for p in pos}:
            ids = [p[2] for p in pos if p[0] == d]; best = max(best, max(ids) - min(ids) + 1)
        assert r_max_width(r) == best
        # nodes brute for cameras / rob: subsets
        # serde
        assert tup(deser(ser(r))) == t and tup(bfs_deser(bfs_ser(r))) == t
        toks = ser(r).split(',') if True else None
        assert len(toks) == 2 * n + 1 and len(bfs_ser(r).split(',')) == 2 * n + 1       # 2n+1 incl. empty tree
        # subtree brute: every node's tuple equals sub tuple
        def subs(t):
            if t is None: return []
            return [t] + subs(t[1]) + subs(t[2])
        allsubs = subs(t)
        for u in ALL_PRE[:60]:
            if u is not None: assert r_is_subtree(r, from_tup(u)) == (u in allsubs)
        # boundary: independent definition by labelled flags
        if t is not None:
            nodes = pos
            # left boundary path
            def left_path(t):
                out = []; u = t[1]
                while u is not None and (u[1] or u[2]): out.append(u[0]); u = u[1] if u[1] is not None else u[2]
                return out
            def right_path(t):
                out = []; u = t[2]
                while u is not None and (u[1] or u[2]): out.append(u[0]); u = u[2] if u[2] is not None else u[1]
                return out
            leaves = [p[-1] for p in paths_leaf(t)]
            if n == 1: leaves = []
            assert r_boundary(r) == [t[0]] + left_path(t) + leaves + right_path(t)[::-1]
        # deepest subtree brute: deepest nodes, smallest subtree containing all = LCA found via path prefixes
        if t is not None:
            dd = [p for p in pos if p[0] == max(q[0] for q in pos)]
            paths = [p[4] for p in dd]
            import os as _os
            pref = _os.path.commonprefix(paths)
            u = t
            for ch in pref: u = u[1] if ch == 'L' else u[2]
            assert tup(r_deepest(r)) == u
        # morris
        ids0 = [id(x) for x in nodes_of(r)]; snap = [(id(x.left), id(x.right)) for x in nodes_of(r)]
        vals, it = r_morris(r)
        assert vals == tin(t) and it == n + sum(1 for x in subs(t) if x[1] is not None)
        assert [(id(x.left), id(x.right)) for x in nodes_of(r)] == snap
        # cameras brute: smallest subset covering
        if n <= 7:
            nds = nodes_of(from_tup(t)); par = {}
            for x in nds:
                for c in (x.left, x.right):
                    if c: par[id(c)] = x
            best = None
            for k in range(0, n + 1):
                for sub_ in itertools.combinations(range(n), k):
                    cov = set()
                    for i in sub_:
                        x = nds[i]; cov.add(id(x))
                        if id(x) in par: cov.add(id(par[id(x)]))
                        for c in (x.left, x.right):
                            if c: cov.add(id(c))
                    if len(cov) == n: best = k; break
                if best is not None: break
            assert r_cameras(from_tup(t)) == best, (t, r_cameras(from_tup(t)), best)
        # complete? depth stuff
    print('shape-exhaustive group 1 ok')

    # random-value trees: max path sum, rob, lca_tree, distance_k, cost, deepest, kth etc.
    def rand_tree(n, lo=-9, hi=9):
        sh = random.choice(shapes(n)); t = label(sh, 'pre')
        # relabel with distinct random ints for LCA tests / random for sums
        return t
    def relabel(t, vals):
        it = iter(vals)
        def go(u):
            if u is None: return None
            v = next(it); return (v, go(u[1]), go(u[2]))
        return go(t)
    for _ in range(1500):
        n = random.randint(1, 7); t = relabel(label(random.choice(shapes(n)), 'pre'), [random.randint(-6, 9) for _ in range(n)])
        r = from_tup(t); adj, val = graph(t)
        # max path sum brute: path between any two positions (including same)
        best = None
        for a in adj:
            d = bfs_dist(adj, a)
            # path nodes sum: reconstruct by BFS parents
            for b in adj:
                # find path a->b
                prev = {a: None}; q = deque([a])
                while q:
                    x = q.popleft()
                    for y in adj[x]:
                        if y not in prev: prev[y] = x; q.append(y)
                s = 0; x = b
                while x is not None: s += val[x]; x = prev[x]
                best = s if best is None or s > best else best
        assert r_maxpath(r) == best, (t, r_maxpath(r), best)
    print('random group ok')
    # rob with non-negative values (as specified) vs brute
    for _ in range(600):
        n = random.randint(0, 7); t = relabel(label(random.choice(shapes(n)), 'pre'), [random.randint(0, 9) for _ in range(n)])
        adj, val = graph(t); ks = list(val); bestr = 0
        for mask in range(1 << len(ks)):
            ch = {ks[i] for i in range(len(ks)) if mask >> i & 1}
            if any(k[:-1] in ch for k in ch if len(k) > 1): continue
            bestr = max(bestr, sum(val[k] for k in ch))
        assert r_rob(from_tup(t)) == bestr
    # LCA / distance_k with distinct labels (pre labels are distinct)
    for t in ALL_PRE:
        n = tsize(t)
        if n < 2: continue
        r = from_tup(t); adj, val = graph(t); inv = {v: k for k, v in val.items()}
        for p in range(n):
            for q in range(n):
                if p == q: continue
                pp, qq = inv[p], inv[q]
                import os as _os
                c = _os.path.commonprefix([pp, qq]); u = t
                for ch in c[1:]: u = u[1] if ch == 'L' else u[2]
                assert r_lca(from_tup(t), p, q) == u[0]
        for p in range(n):
            d = bfs_dist(adj, inv[p])
            for k in range(0, 5):
                assert r_dist_k(from_tup(t), p, k) == sorted(val[x] for x, dd in d.items() if dd == k)
    print('lca / distance_k exhaustive ok')

    # build pre+in / in+post: round trip, injectivity, and pre+post NOT unique
    seen_pi = {}; seen_ip = {}; seen_pp = {}
    for t in ALL_PRE:
        r = from_tup(t)
        assert tup(r_build_pre_in(tpre(t), tin(t))) == t
        assert tup(r_build_in_post(tin(t), tpost(t))) == t
    # injectivity over SHAPES with distinct labels: use shapes labelled by preorder; for same-size trees with the same preorder labels
    for n in range(0, MAXN + 1):
        pi = {}; ip = {}; pp = {}
        for sh in shapes(n):
            t = label(sh, 'pre')
            for dct, key in ((pi, (tuple(tpre(t)), tuple(tin(t)))), (ip, (tuple(tin(t)), tuple(tpost(t)))), (pp, (tuple(tpre(t)), tuple(tpost(t))))):
                dct.setdefault(key, []).append(t)
        assert all(len(v) == 1 for v in pi.values()) and all(len(v) == 1 for v in ip.values())
        amb = sum(1 for v in pp.values() if len(v) > 1)
        if n >= 2: assert amb > 0
        def full(t): return t is None or ((t[1] is None) == (t[2] is None) and full(t[1]) and full(t[2]))
        assert all(len(v) == 1 for v in pp.values() if full(v[0]))   # pre+post identifies full binary trees (0 or 2 children everywhere)
        assert all(not full(v[0]) for v in pp.values() if len(v) > 1)
        if n == 2: assert amb == 1
    print('pre+in and in+post unique, pre+post ambiguous for n>=2 (n=2: exactly one ambiguous pair) ok')
    # preorder alone ambiguous (two different trees same preorder)
    assert tpre((1, (2, None, None), None)) == tpre((1, None, (2, None, None)))

    # ----- BST group: inorder labels with gaps (value = 2*index+1) so absent values exist
    def gap(t):
        if t is None: return None
        return (2 * t[0] + 1, gap(t[1]), gap(t[2]))
    for t0 in ALL_IN:
        t = gap(t0); r = from_tup(t); n = tsize(t); vals = tin(t)
        assert r_valid_bst(r) is True
        assert vals == sorted(vals)
        # kth
        for k in range(1, n + 1): assert r_kth(from_tup(t), k) == vals[k - 1]
        # lca_bst vs lca_tree brute
        for p in vals:
            for q in vals:
                if p != q: assert r_lca_bst(r, p, q) == r_lca(r, p, q)
        # range sum
        for lo in range(0, 2 * n + 3):
            for hi in range(lo, 2 * n + 3):
                assert r_range_sum(r, lo, hi) == sum(v for v in vals if lo <= v <= hi)
        # insert (every value including absent ones)
        for v in range(0, 2 * n + 2):
            if v in vals: continue
            got = r_insert(from_tup(t), v); assert tin(tup(got)) == sorted(vals + [v]) if False else tin(tup(got)) == sorted(vals + [v])
            # leaf insertion: node count +1 and new node is a leaf at the end of search path
            nd = got
            while nd.val != v: nd = nd.left if v < nd.val else nd.right
            assert nd.left is None and nd.right is None
        # delete: all keys including absent
        for k in range(0, 2 * n + 2):
            got = r_delete(from_tup(t), k); assert r_valid_bst(got) and tin(tup(got)) == [v for v in vals if v != k]
        # successor
        for i, v in enumerate(vals): assert r_succ(r, v) == (vals[i + 1] if i + 1 < n else None)
        # two sum
        for k in range(0, 4 * n + 3):
            assert r_two_sum(r, k) == any(a + b == k for a, b in itertools.combinations(vals, 2))
        # iterator + O(h) stack bound
        it = BSTIter(from_tup(t)); got = []
        while it.hasNext(): got.append(it.next())
        assert got == vals and it.maxst <= theight(t)
        # bst from preorder
        assert tup(r_bst_pre(tpre(t))) == t
        # dll
        if n:
            h = r_dll(from_tup(t)); assert dll_vals(h, n) == vals
        # sorted -> BST under the middle rule, balanced; list versions same tree
        # recover: every pair swap, uniqueness of the fixing pair
        if n >= 2:
            for i, j in itertools.combinations(range(n), 2):
                # swap values vals[i], vals[j]
                def swp(u):
                    if u is None: return None
                    v = u[0]; v = vals[j] if v == vals[i] else vals[i] if v == vals[j] else v
                    return (v, swp(u[1]), swp(u[2]))
                bad = swp(t)
                fixed = r_recover(from_tup(bad)); assert tup(fixed) == t
                # number of value pairs whose swap makes a BST
                cnt = 0
                bv = tin(bad)
                for a, b in itertools.combinations(bv, 2):
                    def swp2(u):
                        if u is None: return None
                        v = u[0]; v = b if v == a else a if v == b else v
                        return (v, swp2(u[1]), swp2(u[2]))
                    if r_valid_bst(from_tup(swp2(bad))): cnt += 1
                assert cnt == 1, (t, i, j, cnt)
    print('BST groups exhaustive ok (all BST shapes n<=7)')
    # invalid BSTs: validate vs brute (all-pairs ancestor condition) over labelled shapes with random values
    for _ in range(3000):
        n = random.randint(0, 7); t = relabel(label(random.choice(shapes(n)), 'pre'), [random.randint(0, 5) for _ in range(n)])
        def ok(u, anc):
            if u is None: return True
            for (a, side) in anc:
                if side == 'L' and not u[0] < a: return False
                if side == 'R' and not u[0] > a: return False
            return ok(u[1], anc + [(u[0], 'L')]) and ok(u[2], anc + [(u[0], 'R')])
        assert r_valid_bst(from_tup(t)) == ok(t, [])
    # extreme values
    assert r_valid_bst(build_tree([-2**31])) and r_valid_bst(build_tree([2**31 - 1, -2**31]))
    print('validate BST brute ok')

    # sorted array / list -> BST under (lo+hi)//2 rule
    def isbal(u):
        if u is None: return True
        return abs(theight(u[1]) - theight(u[2])) <= 1 and isbal(u[1]) and isbal(u[2])
    for n in range(0, 60):
        a = list(range(n)); t1 = tup(r_sorted_to_bst(a))
        assert isbal(t1) and tin(t1) == a
        t2 = tup(list_to_bst(mk_list(a))); t3 = tup(list_to_bst_mid(mk_list(a)))
        assert t1 == t2 == t3, (n, t1, t2, t3)
    print('sorted array/list to BST (3 versions same tree, balanced) ok n<60')

    # complete tree: count + spine step bound for all n up to 2^15
    worst = {}
    for n in range(0, 2 ** 11 + 1):
        t = build_tree(list(range(1, n + 1))) if n < 4000 else None
        if t is None:
            # build a complete tree of n nodes quickly via index arithmetic
            nodes = [None] + [TreeNode(i) for i in range(1, n + 1)]
            for i in range(1, n + 1):
                if 2 * i <= n: nodes[i].left = nodes[2 * i]
                if 2 * i + 1 <= n: nodes[i].right = nodes[2 * i + 1]
            t = nodes[1] if n else None
        SPINE[0] = 0
        assert r_count_complete(t) == n
        if n >= 1:
            h = n.bit_length() - 1
            assert SPINE[0] <= 2 * h * h, (n, h, SPINE[0])
            if n == 2 ** (h + 1) - 1: assert SPINE[0] == 2 * h
            if n == 2 ** (h + 1) - 2 and h >= 2: assert SPINE[0] == h * (2 * h - 1)
            worst[h] = max(worst.get(h, 0), SPINE[0])
        if n > 600 and n % 7 != 0 and n not in (2 ** 15,):
            pass
    print('count_complete ok to 2^11; max spine steps by h:', worst)
    # (the loop above is O(n) per n for building; kept small enough) -- boundary cases explicit
    for h in range(0, 14):
        for n in (2 ** h, 2 ** (h + 1) - 2, 2 ** (h + 1) - 1):
            if n < 1: continue
            nodes = [None] + [TreeNode(i) for i in range(1, n + 1)]
            for i in range(1, n + 1):
                if 2 * i <= n: nodes[i].left = nodes[2 * i]
                if 2 * i + 1 <= n: nodes[i].right = nodes[2 * i + 1]
            SPINE[0] = 0; assert r_count_complete(nodes[1]) == n and SPINE[0] <= 2 * h * h
            if n == 2 ** (h + 1) - 1: assert SPINE[0] == 2 * h
            if n == 2 ** (h + 1) - 2 and h >= 2: assert SPINE[0] == h * (2 * h - 1)

    # level order queue on perfect trees = 2^(k-1)
    for k in range(1, 9):
        n = 2 ** k - 1; t = build_tree(list(range(1, n + 1))); assert cost(t)[3] == 2 ** (k - 1) and cost(t)[1] == k and cost(t)[2] == k
    print('perfect-tree queue max = 2^(k-1) ok')
    # skewed costs
    for n in range(1, 40):
        l = build_tree(sum(([i, None] for i in range(n)), [])[:-1]); r = build_tree(sum(([i, None] for i in range(n)), [])[:-1])
    for n in range(1, 30):
        left = None; right = None
        for i in range(n): left = TreeNode(i, left, None); right = TreeNode(i, None, right)
        assert cost(left) == (n, n, n, 1) and cost(right) == (n, n, 1, 1)
    print('skewed cost formulas ok')

    # deep skew behaviour
    assert r_deep(500, 'left') == (500, 500) and r_deep(2000, 'right') == ('RecursionError', 2000) and r_deep(100000, 'left')[1] == 100000
    print('deep skew ok; recursion limit', sys.getrecursionlimit())

    # random distinct-label checks for max_path_sum covered; random for flatten / trie / nary / classify / morris restore
    for t in ALL_PRE:
        r = from_tup(t); ids0 = sorted(id(x) for x in nodes_of(r)); fr = r_flatten(r)
        assert chain_vals(fr) == tpre(t) and sorted(id(x) for x in nodes_of(fr)) == ids0
    for _ in range(500):
        words = [''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 6))]
        qs_ = [''.join(random.choice('abc') for _ in range(random.randint(1, 3))) for _ in range(5)]
        c, nd = r_trie(words, qs_)
        assert c == [sum(w.startswith(q) for w in words) for q in qs_] and nd == len({w[:i] for w in words for i in range(1, len(w) + 1)})
    def nary_ser(tree):   # tree = (val, [children])
        out = [tree[0], None]; q = deque([tree])
        while q:
            n = q.popleft()
            for c in n[1]: out.append(c[0]); q.append(c)
            out.append(None)
        while out and out[-1] is None: out.pop()
        return out
    def rand_nary(d):
        return (random.randint(1, 99), [rand_nary(d - 1) for _ in range(random.randint(0, 3))] if d > 0 else [])
    def n_pre(t): return [t[0]] + [x for c in t[1] for x in n_pre(c)]
    def n_post(t): return [x for c in t[1] for x in n_post(c)] + [t[0]]
    def n_depth(t): return 1 + max([n_depth(c) for c in t[1]], default=0)
    for _ in range(400):
        t = rand_nary(random.randint(0, 3)); a = nary_ser(t); res = r_nary(a)
        assert res[0] == n_pre(t) and res[1] == n_post(t) and res[3] == n_depth(t) and sum(map(len, res[2])) == len(n_pre(t)), (t, a, res)
    # classify vs brute (enumerate all root paths)
    for _ in range(3000):
        m = random.randint(1, 5); nodes = [[i, random.choice([-1] + list(range(m))), random.choice([-1] + list(range(m)))] for i in range(m)]
        # brute: DFS with explicit path, counting arrivals; limit depth
        arrivals = {}; cyc = False
        def walk(i, path):
            global_cyc = False
            arrivals[i] = arrivals.get(i, 0) + 1
            if i in path: return True
            if arrivals[i] > 1: return False
            for c in nodes[i][1:]:
                if c != -1 and walk(c, path | {i}): return True
            return False
        cyc = walk(0, frozenset())
        # brute 'shared' by counting incoming edges from reachable nodes (cycle case handled first)
        if cyc: exp = 'cycle'
        else:
            reach = set(); st = [0]
            while st:
                x = st.pop()
                if x in reach: continue
                reach.add(x); st += [c for c in nodes[x][1:] if c != -1]
            incoming = sum(1 for x in reach for c in nodes[x][1:] if c != -1)
            exp = 'tree' if incoming == len(reach) - 1 else 'shared'
        assert r_classify(nodes) == exp, (nodes, r_classify(nodes), exp)
    print('flatten / trie / nary / classify brute ok')
    # max_width on deep skew (index normalisation keeps ints small)
    deep = None
    for i in range(3000): deep = TreeNode(i, None, deep)
    assert r_max_width(deep) == 1
    # serde on a deep skewed tree with an iterative deser
    deep2 = None
    for i in range(3000): deep2 = TreeNode(i, deep2, None)
    assert ser(deser(ser(deep2))) == ser(deep2)
    print('ALL OK')
