import random
random.seed(42)

def articulation(n, edges):
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:                            # self loops never matter
            g[u].append((v, i)); g[v].append((u, i))
    disc = [-1] * n; low = [0] * n; t = 0; arts = set()
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = t; t += 1; kids = 0
        st = [(s, -1, 0)]                     # (node, edge id used to arrive, next adjacency position)
        while st:
            u, pe, i = st.pop()
            if i < len(g[u]):
                st.append((u, pe, i + 1))
                v, e = g[u][i]
                if e == pe:                   # skip the arrival edge by id (parallel edges still count)
                    continue
                if disc[v] == -1:
                    disc[v] = low[v] = t; t += 1
                    st.append((v, e, 0))
                else:
                    low[u] = min(low[u], disc[v])
            elif st:                          # u finished; its parent entry is on top
                p = st[-1][0]
                low[p] = min(low[p], low[u])
                if p == s:
                    kids += 1
                elif low[u] >= disc[p]:       # >= : the back edge may land ON p
                    arts.add(p)
        if kids >= 2:
            arts.add(s)
    return sorted(arts)

def comps(n, edges, skip=-1):
    p = list(range(n))
    def f(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges:
        if u != skip and v != skip:
            p[f(u)] = f(v)
    return len({f(x) for x in range(n) if x != skip})

def oracle(n, edges):                         # delete each node and recount components
    base = comps(n, edges)
    out = []
    for v in range(n):
        isolated = not any((u == v) != (w == v) for u, w in edges)   # no edge to another node
        expected = base - 1 if isolated else base                     # removing it explains this much
        if comps(n, edges, v) > expected:
            out.append(v)
    return out

assert articulation(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == [1, 3]
assert articulation(3, [[0, 1], [1, 2], [2, 0]]) == []
assert articulation(4, [[0, 1], [0, 2], [0, 3]]) == [0]
print('examples ok')

for _ in range(800):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 12))]
    assert articulation(n, edges) == oracle(n, edges), (n, edges)
print('800 random graphs match the delete-each-node oracle')

assert articulation(1, []) == [] and articulation(2, [[0, 1]]) == []     # lone node, single edge
assert articulation(2, [[0, 1], [0, 1]]) == []                           # parallel edges
assert articulation(3, [[0, 1], [1, 2]]) == [1]                          # path
assert articulation(4, [[0, 0], [1, 2], [2, 3]]) == [2]                  # disconnected + self loop
assert articulation(4, [[0, 1], [1, 2], [2, 3], [3, 0]]) == []           # cycle

# '>' instead of '>=' is wrong for vertices: a cycle hanging off p has low[child] == disc[p]
def art_gt(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges: g[u].append(v); g[v].append(u)
    disc = [-1] * n; low = [0] * n; res = set(); t = [0]
    def dfs(u, p, root):
        disc[u] = low[u] = t[0]; t[0] += 1; kids = 0
        for v in g[u]:
            if v == p: continue
            if disc[v] == -1:
                kids += 1; dfs(v, u, False); low[u] = min(low[u], low[v])
                if not root and low[v] > disc[u]: res.add(u)
            else: low[u] = min(low[u], disc[v])
        if root and kids >= 2: res.add(u)
    for s in range(n):
        if disc[s] == -1: dfs(s, -1, True)
    return sorted(res)
bowtie = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]]               # two triangles sharing node 2
print('bowtie: >= gives', articulation(5, bowtie), ' > gives', art_gt(5, bowtie))
assert articulation(5, bowtie) == [2] and art_gt(5, bowtie) == []

N = 10**5
assert articulation(N, [[i, i + 1] for i in range(N - 1)]) == list(range(1, N - 1))
print('10^5 path iterative ok')
print('first example:', articulation(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]))
