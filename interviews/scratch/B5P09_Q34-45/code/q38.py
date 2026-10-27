import itertools
import random

random.seed(38)

def build_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:                     # input order, both directions
        adj[u].append(v)
        adj[v].append(u)
    return adj

def dfs_mark_on_pop(adj, start):
    """A: push everything, skip stale entries on pop. Exactly the recursive preorder."""
    seen, stack, order, peak = set(), [start], [], 1
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        for v in reversed(adj[u]):         # reversed, so the FIRST neighbour is popped first
            stack.append(v)
        peak = max(peak, len(stack))
    return order, peak

def dfs_mark_on_push(adj, start):
    """B: mark when pushed. Each node enters the stack at most once, but the order is not preorder."""
    seen, stack, order, peak = {start}, [start], [], 1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
        peak = max(peak, len(stack))
    return order, peak

def dfs_recursive(adj, start):
    """Brute force / reference preorder (fine on small inputs only)."""
    seen, order = set(), []
    def go(u):
        seen.add(u)
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                go(v)
    go(start)
    return order

def solve(n, edges, start):
    adj = build_adj(n, edges)
    return [dfs_mark_on_pop(adj, start)[0], dfs_mark_on_push(adj, start)[0]]

# ---- examples from the prompt
assert solve(4, [[0, 1], [0, 2], [1, 3], [2, 3]], 0) == [[0, 1, 3, 2], [0, 2, 3, 1]]
assert solve(4, [[0, 1], [1, 2], [2, 3]], 0) == [[0, 1, 2, 3], [0, 1, 2, 3]]
assert solve(3, [[0, 1], [0, 2], [1, 2]], 0) == [[0, 1, 2], [0, 2, 1]]
print('examples ok')

# ---- why B differs: expanding 0 marks 1, 2, 3 as seen at once. In a real DFS the walk 0 -> 1 -> 3 reaches 3 as
#      a child of 1; B pops 3 first and 1 is already marked, so 1 can never be explored from inside 3's branch.
E = [[0, 1], [0, 2], [0, 3], [3, 1]]
adj = build_adj(4, E)
print('A (true preorder):', dfs_mark_on_pop(adj, 0)[0], ' B:', dfs_mark_on_push(adj, 0)[0], ' recursive:', dfs_recursive(adj, 0))

# ---- exhaustive over EVERY simple graph on <= 5 nodes (input order and reversed order), every start
total = diff = b_bigger = 0
for n in range(1, 6):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for m in range(len(pairs) + 1):
        for es in itertools.combinations(pairs, m):
            for edges in (list(es), list(reversed(es))):
                adj = build_adj(n, edges)
                for s in range(n):
                    oa, pa = dfs_mark_on_pop(adj, s)
                    ob, pb = dfs_mark_on_push(adj, s)
                    assert oa == dfs_recursive(adj, s)            # A is exactly the recursive preorder
                    assert sorted(oa) == sorted(ob)               # B visits the same set
                    total += 1
                    diff += oa != ob
                    b_bigger += pb > pa
print('exhaustive:', total, 'cases; A == recursive preorder always; same node set always;')
print('  B order differs from A on', diff, 'cases; B peak stack larger than A on', b_bigger)
assert b_bigger == 0 and diff > 0

# ---- seeded random cross-check on larger graphs
N = 400
dif = 0
for _ in range(N):
    n = random.randint(2, 12)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    edges = [list(e) for e in random.sample(pairs, random.randint(0, len(pairs)))]
    s = random.randrange(n)
    adj = build_adj(n, edges)
    a, b = solve(n, edges, s)
    assert a == dfs_recursive(adj, s) and sorted(a) == sorted(b)
    dif += a != b
print('random check on', N, 'seeded graphs ok; B differs from preorder on', dif)

# ---- stack size: complete graph. A stacks every neighbour entry (about n^2 / 2), B at most n
n = 300
K = [[i, j] for i in range(n) for j in range(i + 1, n)]
adj = build_adj(n, K)
print('K300 peak stack: A =', dfs_mark_on_pop(adj, 0)[1], ' B =', dfs_mark_on_push(adj, 0)[1], ' (n =', n, ')')
assert dfs_mark_on_push(adj, 0)[1] <= n and dfs_mark_on_pop(adj, 0)[1] > n

# ---- deep path: both iterative versions are fine, the recursive one hits the recursion limit
n = 100000
path = [[i, i + 1] for i in range(n - 1)]
adj = build_adj(n, path)
assert dfs_mark_on_pop(adj, 0)[0] == list(range(n)) and dfs_mark_on_push(adj, 0)[0] == list(range(n))
try:
    dfs_recursive(adj, 0)
except RecursionError:
    print('recursive DFS on a 100000-node path: RecursionError (default limit 1000)')

# ---- edge cases
assert solve(1, [], 0) == [[0], [0]]
assert solve(5, [[0, 1]], 3) == [[3], [3]]            # start in its own component: only that node
assert solve(2, [[0, 1]], 1) == [[1, 0], [1, 0]]
print('edge cases ok')
