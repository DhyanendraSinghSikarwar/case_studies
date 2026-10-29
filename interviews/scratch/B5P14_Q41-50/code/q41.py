import random, sys
random.seed(41)

def tarjan_iter(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)                       # keep input order
    idx = [-1] * n; low = [0] * n; on = [False] * n
    comp = [-1] * n; stack = []; counter = 0; nc = 0
    for s in range(n):
        if idx[s] != -1:
            continue
        idx[s] = low[s] = counter; counter += 1
        stack.append(s); on[s] = True
        work = [(s, 0)]                      # (node, next edge position)
        while work:
            u, i = work.pop()
            if i < len(g[u]):
                work.append((u, i + 1))
                v = g[u][i]
                if idx[v] == -1:             # tree edge: "recurse"
                    idx[v] = low[v] = counter; counter += 1
                    stack.append(v); on[v] = True
                    work.append((v, 0))
                elif on[v]:                  # back/cross edge into the open stack
                    low[u] = min(low[u], idx[v])
            else:                            # u is finished
                if low[u] == idx[u]:         # u is the root of a component
                    while True:
                        w = stack.pop(); on[w] = False; comp[w] = nc
                        if w == u:
                            break
                    nc += 1
                if work:                     # "return" to the parent
                    p = work[-1][0]
                    low[p] = min(low[p], low[u])
    cross = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, nc, cross]

def tarjan_rec(n, edges):                    # oracle: textbook recursion, same visiting order
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
    idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n
    st = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; st.append(u); on[u] = True
        for v in g[u]:
            if idx[v] == -1:
                dfs(v); low[u] = min(low[u], low[v])
            elif on[v]:
                low[u] = min(low[u], idx[v])
        if low[u] == idx[u]:
            while True:
                w = st.pop(); on[w] = False; comp[w] = box[1]
                if w == u:
                    break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1:
            dfs(s)
    cross = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, box[1], cross]

# examples from the prompt
assert tarjan_iter(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == [[2, 2, 2, 1, 0], 3, 2]
assert tarjan_iter(3, [[0, 1], [1, 0], [0, 2], [0, 2]]) == [[1, 1, 0], 2, 1]
print('examples ok')

# seeded random cross-check vs the recursive oracle + reverse-topological property
for _ in range(600):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 16))]
    a = tarjan_iter(n, edges)
    assert a == tarjan_rec(n, edges), (n, edges)
    comp = a[0]
    assert all(comp[u] >= comp[v] for u, v in edges)
print('600 random graphs: iterative == recursive oracle, comp[u] >= comp[v] on every edge')

# edge cases
assert tarjan_iter(1, []) == [[0], 1, 0]
assert tarjan_iter(1, [[0, 0]]) == [[0], 1, 0]               # self loop
assert tarjan_iter(3, []) == [[0, 1, 2], 3, 0]               # isolated nodes, completed in order
assert tarjan_iter(3, [[0, 1], [1, 2], [2, 0]]) == [[0, 0, 0], 1, 0]

# why iterative: a path of 1500 nodes breaks the recursive version, 10^5 is fine iteratively
path = lambda N: [[i, i + 1] for i in range(N - 1)]
try:
    tarjan_rec(1500, path(1500)); print('recursive survived?!')
except RecursionError:
    print('recursive version: RecursionError at 1500-node path')
N = 10**5
comp, cnt, cross = tarjan_iter(N, path(N))
assert cnt == N and cross == N - 1 and comp[0] == N - 1 and comp[N - 1] == 0
print('iterative 10^5 path ok: components', cnt, 'condensation edges', cross)
print('first example:', tarjan_iter(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))

# the on-stack test matters: without it a finished component can be glued onto the current one
def tarjan_no_on_stack(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v)
    idx = [-1] * n; low = [0] * n; comp = [-1] * n; st = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; st.append(u)
        for v in g[u]:
            if idx[v] == -1: dfs(v); low[u] = min(low[u], low[v])
            else: low[u] = min(low[u], idx[v])               # BUG: also fires for finished components
        if low[u] == idx[u]:
            while True:
                w = st.pop(); comp[w] = box[1]
                if w == u: break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1: dfs(s)
    return comp
for _ in range(5000):
    n = random.randint(2, 5)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(1, 7))]
    if tarjan_no_on_stack(n, edges) != tarjan_iter(n, edges)[0]:
        print('without the on-stack test:', n, edges, '->', tarjan_no_on_stack(n, edges), 'instead of', tarjan_iter(n, edges)[0]); break
else:
    raise SystemExit('no counterexample found')
