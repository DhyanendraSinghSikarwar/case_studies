import random, sys
random.seed(13)

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.size = [1] * n
        self.sets = n
    def find(self, x):                 # iterative: find the root, then compress the path
        r = x
        while self.p[r] != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra                # smaller tree under the larger
        self.size[ra] += self.size[rb]
        self.sets -= 1
        return True

def solve(n, ops):
    d = DSU(n)
    res = []
    for kind, a, b in ops:
        res.append(d.union(a, b) if kind == 'union' else d.find(a) == d.find(b))
    return [res, d.sets, max(d.size[d.find(i)] for i in range(n))]

def brute(n, ops):                     # relabel the whole array on every merge, O(n) per union
    lab = list(range(n)); res = []
    for kind, a, b in ops:
        if kind == 'union':
            if lab[a] == lab[b]:
                res.append(False)
            else:
                old = lab[b]
                lab = [lab[a] if x == old else x for x in lab]
                res.append(True)
        else:
            res.append(lab[a] == lab[b])
    counts = {}
    for x in lab: counts[x] = counts.get(x, 0) + 1
    return [res, len(counts), max(counts.values())]

assert solve(5, [['union', 0, 1], ['union', 1, 2], ['connected', 0, 2], ['union', 0, 2], ['connected', 3, 4]]) == [[True, True, True, False, False], 3, 3]
assert solve(1, [['union', 0, 0], ['connected', 0, 0]]) == [[False, True], 1, 1]
assert solve(3, []) == [[], 3, 1]
print("examples ok")

for _ in range(500):
    n = random.randint(1, 9)
    ops = [[random.choice(['union', 'connected']), random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 14))]
    assert solve(n, ops) == brute(n, ops), (n, ops)
print("500 random cases match the relabel brute force")

# the recursion-limit failure: a plain recursive find on the chain that unions build without size
def find_recursive(p, x):
    return x if p[x] == x else find_recursive(p, p[x])
n = 10**5
chain = list(range(n))
for i in range(n - 1):                 # union(i, i+1) always linking root(i) under root(i+1), no size rule
    chain[i] = i + 1
try:
    find_recursive(chain, 0)
except RecursionError:
    print("recursive find on a 1e5 chain: RecursionError (limit %d)" % sys.getrecursionlimit())

# the same chain through the iterative DSU with union by size: tiny depth, no error
big = solve(n, [['union', i, i + 1] for i in range(n - 1)] + [['connected', 0, n - 1]])
assert big[0][-1] is True and big[1] == 1 and big[2] == n
print("iterative DSU, 1e5 chained unions: sets=%d largest=%d" % (big[1], big[2]))

# union by size alone (NO compression): tree height stays <= log2(n)
def height_by_size_only(n, pairs):
    p = list(range(n)); sz = [1] * n
    def root(x):
        while p[x] != x: x = p[x]
        return x
    for a, b in pairs:
        ra, rb = root(a), root(b)
        if ra != rb:
            if sz[ra] < sz[rb]: ra, rb = rb, ra
            p[rb] = ra; sz[ra] += sz[rb]
    worst = 0
    for x in range(n):
        d = 0
        while p[x] != x: x = p[x]; d += 1
        worst = max(worst, d)
    return worst
worst = 0
for _ in range(400):
    n2 = random.randint(1, 64)
    h = height_by_size_only(n2, [(random.randrange(n2), random.randrange(n2)) for _ in range(random.randint(0, 150))])
    assert 2 ** h <= n2, (n2, h)       # a node at depth h implies a set of size >= 2^h
    worst = max(worst, h)
print("by-size only: 400 random runs, max depth seen %d, always 2^depth <= n" % worst)

# compression alone: the first find on the chain is O(n), but it flattens the whole path
p = list(range(1000))
for i in range(999): p[i] = i + 1
d = DSU(1000); d.p = p
d.find(0)
assert all(d.p[i] == 999 for i in range(1000))
print("compression only: one find on a 1000-chain walks 999 links and flattens every node to the root")
