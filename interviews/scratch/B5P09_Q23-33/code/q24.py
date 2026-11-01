import itertools
import random

random.seed(24)

def min_semesters(n, relations):
    """Kahn's algorithm one level (= one semester) at a time."""
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        adj[a].append(b)
        indeg[b] += 1
    cur = [i for i in range(1, n + 1) if indeg[i] == 0]
    semesters = done = 0
    while cur:
        semesters += 1
        done += len(cur)
        nxt = []
        for u in cur:
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        cur = nxt
    return semesters if done == n else -1

def min_semesters_brute(n, relations):
    """Longest chain (in courses) by n rounds of relaxation; a cycle never settles, so any still-improving edge means -1."""
    d = [1] * (n + 1)
    for _ in range(n):
        for a, b in relations:
            if d[a] + 1 > d[b]:
                d[b] = d[a] + 1
    if any(d[a] + 1 > d[b] for a, b in relations):
        return -1
    return max(d[1:])

for n, rel, want in [(3, [[1, 3], [2, 3]], 2), (3, [[1, 2], [2, 3], [3, 1]], -1),
                     (4, [[1, 2], [2, 3], [3, 4]], 4), (2, [], 1)]:
    got = min_semesters(n, rel)
    assert got == want == min_semesters_brute(n, rel), (n, rel, got, want)
    print(n, rel, '->', got)

# ---- exhaustive: EVERY relation set on n <= 3 including self loops (2^9 sets for n=3), and every set without self loops on n = 4 (2^12)
cnt = 0
for n, loops in [(1, True), (2, True), (3, True), (4, False)]:
    pairs = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if loops or a != b]
    for mask in range(1 << len(pairs)):
        rel = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        assert min_semesters(n, rel) == min_semesters_brute(n, rel), (n, rel)
        cnt += 1
print('exhaustive check on', cnt, 'relation sets (all graphs on n<=3 with self loops, n=4 without): longest chain == Kahn levels')

# ---- seeded random larger cases, with duplicate relations allowed
for _ in range(500):
    n = random.randint(1, 9)
    rel = [[random.randint(1, n), random.randint(1, n)] for _ in range(random.randint(0, 12))]
    assert min_semesters(n, rel) == min_semesters_brute(n, rel), (n, rel)
print('500 seeded random cases agree')

# ---- the answer is a longest path: a DAG that is a single chain has n semesters, a star has 2
n = 5000
chain = [[i, i + 1] for i in range(1, n)]
assert min_semesters(n, chain) == n
assert min_semesters(n, [[1, i] for i in range(2, n + 1)]) == 2
assert min_semesters(n, []) == 1
assert min_semesters(n, chain + [[n, 1]]) == -1                    # one back edge makes a cycle
assert min_semesters(1, [[1, 1]]) == -1                            # self loop
print('n=5000 chain ->', min_semesters(n, chain), 'semesters; star ->', 2, '; no relations ->', 1)

# ---- a partial cycle: courses before the cycle finish, but done < n exposes the cycle
assert min_semesters(4, [[1, 2], [2, 3], [3, 2]]) == -1
print('cycle hidden behind a valid prefix is still caught by done < n')
