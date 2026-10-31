import itertools, random
random.seed(17)

def provinces_dfs(m):                       # iterative DFS with an explicit stack
    n = len(m)
    seen = [False] * n
    count = 0
    for s in range(n):
        if seen[s]:
            continue
        count += 1
        seen[s] = True
        stack = [s]
        while stack:
            u = stack.pop()
            row = m[u]
            for v in range(n):
                if row[v] and not seen[v]:
                    seen[v] = True
                    stack.append(v)
    return count

def provinces_uf(m):
    n = len(m)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    count = n
    for i in range(n):
        for j in range(i + 1, n):           # symmetric: only the upper triangle is needed
            if m[i][j]:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    count -= 1
    return count

def brute(m):                               # transitive closure (Warshall), then count distinct rows' minimum members
    n = len(m)
    r = [[bool(x) for x in row] for row in m]
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]:
                        r[i][j] = True
    return sum(1 for i in range(n) if not any(r[i][j] for j in range(i)))   # i is the smallest member of its group

cases = [([[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2), ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3), ([[1]], 1)]
for m, exp in cases:
    assert provinces_dfs(m) == provinces_uf(m) == brute(m) == exp
print("examples ok: 2 3 1")

cnt = 0
for n in range(1, 6):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                m[i][j] = m[j][i] = 1
        a = provinces_dfs(m)
        assert a == provinces_uf(m) == brute(m)
        cnt += 1
print("exhaustive: all %d symmetric matrices with n <= 5 agree (DFS, union-find, Warshall closure)" % cnt)

for _ in range(200):
    n = random.randint(1, 30); p = random.random() * 0.15
    m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                m[i][j] = m[j][i] = 1
    assert provinces_dfs(m) == provinces_uf(m) == brute(m)
print("200 random n <= 30 matrices agree")

n = 200
ident = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
full = [[1] * n for _ in range(n)]
chain = [[1 if abs(i - j) <= 1 else 0 for j in range(n)] for i in range(n)]
print("n=200: identity ->", provinces_dfs(ident), "| all ones ->", provinces_uf(full), "| chain ->", provinces_dfs(chain))
assert (provinces_dfs(ident), provinces_dfs(full), provinces_uf(chain)) == (200, 1, 1)
