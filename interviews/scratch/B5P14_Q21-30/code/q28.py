import random

def optimal(n, edges, removals):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:                # iterative, path halving
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    comps = n
    def union(a, b):
        nonlocal comps
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            comps -= 1
    gone = set(removals)
    for i, (u, v) in enumerate(edges):       # edges that are never deleted
        if i not in gone:
            union(u, v)
    out = [comps]
    for idx in reversed(removals):           # add the deleted edges back, last deletion first
        union(*edges[idx])
        out.append(comps)
    out.reverse()
    return out

def count_components(n, edges, banned):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if i not in banned:
            adj[u].append(v); adj[v].append(u)
    seen = [False] * n; c = 0
    for s in range(n):
        if not seen[s]:
            c += 1; seen[s] = True; st = [s]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if not seen[y]:
                        seen[y] = True; st.append(y)
    return c

def brute(n, edges, removals):
    banned = set(); out = [count_components(n, edges, banned)]
    for idx in removals:
        banned.add(idx); out.append(count_components(n, edges, banned))
    return out

assert optimal(4, [[0, 1], [1, 2], [2, 3]], [1, 0]) == [1, 2, 3]
assert optimal(3, [[0, 1], [0, 1], [1, 2]], [0, 1, 2]) == [1, 1, 2, 3]
print('examples:', optimal(4, [[0, 1], [1, 2], [2, 3]], [1, 0]), optimal(3, [[0, 1], [0, 1], [1, 2]], [0, 1, 2]))

# edge cases
assert optimal(1, [], []) == [1]
assert optimal(2, [[0, 0]], [0]) == [2, 2]                 # self loop never merges anything
assert optimal(5, [], []) == [5]
assert optimal(3, [[0, 1], [1, 2]], []) == [1]             # no removals: one number

random.seed(28)
for _ in range(800):
    n = random.randint(1, 8)
    m = random.randint(0, 12)
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(m)]
    k = random.randint(0, m)
    removals = random.sample(range(m), k)
    assert optimal(n, edges, removals) == brute(n, edges, removals), (n, edges, removals)
print('random cross-check ok: 800 cases (parallel edges and self loops included)')

N = 10**5
edges = [[i, i + 1] for i in range(N - 1)] + [[i, i + 2] for i in range(N - 2)]
removals = list(range(len(edges)))
random.shuffle(removals)
res = optimal(N, edges, removals)
assert res[0] == 1 and res[-1] == N and len(res) == len(edges) + 1
assert all(res[i] <= res[i + 1] for i in range(len(res) - 1))   # deletions never reduce the count
print('n = 10^5, 2*10^5 deletions: monotone, starts at 1, ends at', res[-1])
