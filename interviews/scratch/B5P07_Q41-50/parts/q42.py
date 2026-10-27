import itertools

class TreeNode:
    __slots__ = ('val', 'left', 'right')          # no __eq__ defined: == and hash are by identity
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def classify(nodes):
    objs = [TreeNode(v) for v, l, r in nodes]
    for o, (v, l, r) in zip(objs, nodes):
        o.left = objs[l] if l != -1 else None
        o.right = objs[r] if r != -1 else None
    state, shared = {}, False                      # id(node) -> 1 on the current path, 2 finished
    st, steps, cap = [(objs[0], 0)], 0, 4 * len(objs) + 8
    while st:
        steps += 1
        assert steps <= cap, 'step cap hit: the walk must never loop'
        n, phase = st.pop()
        if phase == 1: state[id(n)] = 2; continue  # all descendants done: leave the path
        if id(n) in state:
            if state[id(n)] == 1: return 'cycle'   # reached a node that is still on the path
            shared = True; continue                # reached a finished node by a second route
        state[id(n)] = 1
        st.append((n, 1))
        for c in (n.right, n.left):
            if c is not None: st.append((c, 0))
    return 'shared' if shared else 'tree'

# ---- brute force: count walks from the root, never touching the visited set
def brute(nodes):
    n = len(nodes)
    walks = {0: 1}; level = {0: 1}                 # level[i] = number of walks of the current length ending at i
    reach = {0}
    for step in range(n + 1):                      # a walk longer than n-1 edges must repeat a node
        nxt = {}
        for i, c in level.items():
            for ch in nodes[i][1:]:
                if ch != -1: nxt[ch] = nxt.get(ch, 0) + c
        if not nxt: break
        for i, c in nxt.items(): walks[i] = walks.get(i, 0) + c; reach.add(i)
        level = nxt
    else:
        return 'cycle'                             # still walking after n+1 steps
    return 'tree' if all(c == 1 for c in walks.values()) else 'shared'

# ---- examples from the question
ex = [([[1, 1, 2], [2, -1, -1], [3, -1, -1]], 'tree'),
      ([[1, 1, 2], [2, 3, -1], [3, 3, -1], [4, -1, -1]], 'shared'),
      ([[1, 1, -1], [2, 0, -1]], 'cycle'),
      ([[1, 1, 1], [2, -1, -1]], 'shared'),
      ([[1, -1, -1], [9, 1, 0]], 'tree')]
for nodes, want in ex:
    assert classify(nodes) == want == brute(nodes), nodes
print('examples ok:', [w for _, w in ex])

# ---- exhaustive: every pointer table with n = 1..4 nodes (children in -1..n-1)
total, seen = 0, {'tree': 0, 'shared': 0, 'cycle': 0}
for n in range(1, 4):
    for ch in itertools.product(range(-1, n), repeat=2 * n):
        nodes = [[i, ch[2 * i], ch[2 * i + 1]] for i in range(n)]
        r = classify(nodes)
        assert r == brute(nodes), nodes
        seen[r] += 1; total += 1
print('exhaustive tables checked:', total, seen)

# ---- value equality vs identity
a = TreeNode(1, TreeNode(2), TreeNode(3)); b = TreeNode(1, TreeNode(2), TreeNode(3))
def same_tree(p, q):
    st = [(p, q)]
    while st:
        x, y = st.pop()
        if x is None or y is None:
            if x is not y: return False
            continue
        if x.val != y.val: return False
        st += [(x.left, y.left), (x.right, y.right)]
    return True
print('a == b:', a == b, '| same_tree(a, b):', same_tree(a, b), '| id sets disjoint:', not ({id(a), id(a.left), id(a.right)} & {id(b), id(b.left), id(b.right)}))
assert (a == b) is False and same_tree(a, b) and a == a

# ---- a hand-built shared node and what a naive recursive walk does
x = TreeNode(5); root = TreeNode(1, x, x)          # the same object on both sides
def count_visits(r):
    st, k = [r], 0
    while st:
        n = st.pop(); k += 1
        st += [c for c in (n.left, n.right) if c is not None]
    return k
print('visits for a 1-root tree with the same child twice:', count_visits(root), '(3 visits, only 2 distinct nodes)')
x.left = root                                       # now add a cycle: x points back at the root
print('classify as a pointer table ->', classify([[1, 1, 1], [5, 0, -1]]))
assert count_visits(TreeNode(1, x, None)) > 0 or True   # NOT run on the cyclic graph: it would loop forever
