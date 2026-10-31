import itertools, random, sys
random.seed(22)

def has_cycle(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))                 # remember the edge index, not just the neighbour
        adj[v].append((u, i))                 # a self loop is stored twice at u, which is fine
    seen = [False] * n
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, -1)]                     # (node, index of the edge we arrived by)
        while stack:
            u, arrived_by = stack.pop()
            for v, i in adj[u]:
                if i == arrived_by:           # do not walk back along the same edge
                    continue
                if seen[v]:                   # reached by a different edge: a cycle
                    return True
                seen[v] = True
                stack.append((v, i))
    return False

def has_cycle_uf(n, edges):                   # second method: an edge joining two already-joined nodes closes a cycle
    p = list(range(n))
    def find(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges:
        a, b = find(u), find(v)
        if a == b:
            return True
        p[a] = b
    return False

def has_cycle_parent_only(n, edges, use_set):   # the tempting version: skip the parent NODE
    adj = [set() if use_set else [] for _ in range(n)]
    for u, v in edges:
        if use_set:
            adj[u].add(v); adj[v].add(u)         # a set (or dict) collapses a repeated edge into one entry
        else:
            adj[u].append(v); adj[v].append(u)
    seen = [False] * n
    for s in range(n):
        if seen[s]: continue
        seen[s] = True; stack = [(s, -1)]
        while stack:
            u, par = stack.pop()
            for v in adj[u]:
                if v == par: continue
                if seen[v]: return True
                seen[v] = True; stack.append((v, u))
    return False

def brute(n, edges):                          # remove each edge in turn: does its end still reach its start?
    for i, (u, v) in enumerate(edges):
        if u == v:
            return True
        adj = [[] for _ in range(n)]
        for j, (a, b) in enumerate(edges):
            if j != i:
                adj[a].append(b); adj[b].append(a)
        seen, st = {u}, [u]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); st.append(y)
        if v in seen:
            return True
    return False

assert has_cycle(4, [[0, 1], [1, 2], [2, 3]]) is False
assert has_cycle(3, [[0, 1], [1, 2], [2, 0]]) is True
assert has_cycle(2, [[0, 1], [1, 0]]) is True
assert has_cycle(2, [[1, 1]]) is True
print("examples ok: False True True True")

# exhaustive over ALL edge lists (order and endpoint direction included): n=3 up to 4 edges, n=4 up to 3 edges
cnt = true_n = 0
for n, maxe in ((1, 3), (2, 4), (3, 4), (4, 3)):
    ordered = [[u, v] for u in range(n) for v in range(n)]
    for k in range(maxe + 1):
        for es in itertools.product(ordered, repeat=k):
            es = [list(e) for e in es]
            r = has_cycle(n, es)
            assert r == brute(n, es) == has_cycle_uf(n, es), (n, es)
            cnt += 1; true_n += r
print("exhaustive: %d edge lists (n<=4, <=4 edges), DFS == brute == union-find; %d contain a cycle" % (cnt, true_n))

# the parent-node idea: how often is it wrong over every edge list with n <= 3 and <= 3 edges?
wrong = {False: 0, True: 0}; first = {False: None, True: None}
for n in (1, 2, 3):
    ordered = [[u, v] for u in range(n) for v in range(n)]
    for k in range(4):
        for es in itertools.product(ordered, repeat=k):
            es = [list(e) for e in es]
            truth = brute(n, es)
            for use_set in (False, True):
                if has_cycle_parent_only(n, es, use_set) != truth:
                    wrong[use_set] += 1
                    if first[use_set] is None or len(es) < len(first[use_set]): first[use_set] = es
print("parent-node skip with LIST adjacency: wrong on", wrong[False], "lists (the parent's own loop still meets the second copy of a repeated edge)")
print("parent-node skip with SET adjacency: wrong on", wrong[True], "lists; smallest failing edges:", first[True])
assert wrong[False] == 0 and wrong[True] > 0

for _ in range(500):
    n = random.randint(1, 8)
    es = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 9))]
    assert has_cycle(n, es) == brute(n, es)
print("500 random multigraphs with self loops ok")

# deep paths: iterative copes with 2e5 nodes; a recursive DFS dies at the default limit
n = 200000
path = [[i, i + 1] for i in range(n - 1)]
assert has_cycle(n, path) is False and has_cycle(n, path + [[n - 1, 0]]) is True
assert has_cycle(n, path + [[7, 7]]) is True and has_cycle(n, path + [[7, 8]]) is True
def rec_cycle(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges): adj[u].append((v, i)); adj[v].append((u, i))
    seen = [False] * n
    def dfs(u, pe):
        seen[u] = True
        for v, i in adj[u]:
            if i == pe: continue
            if seen[v] or dfs(v, i): return True
        return False
    return any(not seen[s] and dfs(s, -1) for s in range(n))
try:
    rec_cycle(5000, path[:4999])
except RecursionError:
    print("recursive DFS on a 5000-node path: RecursionError (limit %d); iterative handled n=200000" % sys.getrecursionlimit())
