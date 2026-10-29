import random

def brute(n, edges):                     # oracle: Floyd-Warshall reachability, u ~ v iff each reaches the other
    reach = [[i == j for j in range(n)] for i in range(n)]
    for u, v in edges: reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]: reach[i][j] = True
    seen = [False] * n; out = []
    for i in range(n):
        if not seen[i]:
            comp = [j for j in range(n) if reach[i][j] and reach[j][i]]
            for j in comp: seen[j] = True
            out.append(comp)
    return out

def kosaraju(n, edges):
    g = [[] for _ in range(n)]; rg = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v); rg[v].append(u)
    # pass 1: iterative DFS on g, record nodes in order of FINISH
    seen = [False] * n; order = []
    for s in range(n):
        if seen[s]: continue
        seen[s] = True
        stack = [(s, 0)]                        # (node, index of next neighbour to try)
        while stack:
            u, i = stack.pop()
            if i < len(g[u]):
                stack.append((u, i + 1))        # come back to u for its next neighbour
                v = g[u][i]
                if not seen[v]:
                    seen[v] = True; stack.append((v, 0))
            else:
                order.append(u)                 # all neighbours done: u finishes now
    # pass 2: iterative DFS on the reversed graph in decreasing finish order; each tree = one SCC
    comp_of = [-1] * n; comps = []
    for s in reversed(order):
        if comp_of[s] != -1: continue
        comp_of[s] = len(comps); members = [s]; stack = [s]
        while stack:
            u = stack.pop()
            for v in rg[u]:
                if comp_of[v] == -1:
                    comp_of[v] = len(comps); members.append(v); stack.append(v)
        comps.append(sorted(members))
    return sorted(comps, key=lambda c: c[0])

cases = [(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]], [[0, 1, 2], [3], [4]]),
         (3, [[0, 0]], [[0], [1], [2]]),
         (4, [[0, 1], [1, 0], [2, 3], [3, 2], [1, 2]], [[0, 1], [2, 3]])]
for n, e, want in cases:
    assert kosaraju(n, e) == brute(n, e) == want
    print(n, e, '->', kosaraju(n, e))

random.seed(20)
for case in range(600):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 14))]   # repeats and self loops allowed
    assert kosaraju(n, edges) == brute(n, edges), (n, edges)
print('600 random graphs match the Floyd-Warshall oracle')

# deep graphs: a path of 10^5 nodes would blow the recursion limit, the explicit stack does not
N = 10**5
path = [[i, i + 1] for i in range(N - 1)]
res = kosaraju(N, path); assert len(res) == N and res[0] == [0] and res[-1] == [N - 1]
cyc = path + [[N - 1, 0]]
res = kosaraju(N, cyc); assert res == [list(range(N))]
print('path of', N, '->', len(kosaraju(N, path)), 'components; same path closed into one cycle ->', len(res), 'component')

# edge cases
assert kosaraju(1, []) == [[0]]
assert kosaraju(2, []) == [[0], [1]]
assert kosaraju(3, [[0, 1], [0, 1], [1, 0]]) == [[0, 1], [2]]          # repeated edges
assert kosaraju(3, [[2, 1], [1, 0]]) == [[0], [1], [2]]                 # DAG: every node alone
assert kosaraju(4, [[3, 2], [2, 1], [1, 0], [0, 3]]) == [[0, 1, 2, 3]] # unsorted labels in one cycle
print('edge asserts ok')
