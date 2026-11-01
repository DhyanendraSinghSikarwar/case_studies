import itertools
import random
from collections import deque

random.seed(8)

def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:                 # b before a: edge b -> a
        adj[b].append(a)
        indeg[a] += 1                          # repeated pairs count twice and are subtracted twice: consistent
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    taken = 0
    while q:
        u = q.popleft(); taken += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return taken == num_courses                # leftovers all sit on, or behind, a cycle

def brute(num_courses, prerequisites):
    """Transitive closure (Floyd-Warshall style): feasible iff no course can reach itself."""
    n = num_courses
    r = [[False] * n for _ in range(n)]
    for a, b in prerequisites:
        r[b][a] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]:
                        r[i][j] = True
    return not any(r[i][i] for i in range(n))

def leftover(num_courses, prerequisites):
    """Which courses Kahn cannot take: the cycle plus everything downstream of it."""
    adj = [[] for _ in range(num_courses)]; indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a); indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0); gone = set()
    while q:
        u = q.popleft(); gone.add(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return sorted(set(range(num_courses)) - gone)

assert can_finish(2, [[1, 0]]) is True
assert can_finish(2, [[1, 0], [0, 1]]) is False
assert can_finish(3, [[1, 1]]) is False
assert can_finish(3, []) is True
print('4 prompt examples ok')

for _ in range(1500):
    n = random.randint(1, 6)
    pre = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 8))]
    assert can_finish(n, pre) == brute(n, pre), (n, pre)
print('1500 seeded random inputs (repeats and self loops included): Kahn == transitive closure')

# exhaustive: every set of ordered pairs (self loops included) on 3 courses = 2^9 sets
pairs = [(a, b) for a in range(3) for b in range(3)]
for mask in range(1 << 9):
    pre = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert can_finish(3, pre) == brute(3, pre)
print('exhaustive on 3 courses, all 512 prerequisite sets: ok')

# leftovers: a cycle plus a tail behind it
print('leftover for 0<->1 cycle with 2 after 1 and a free course 3:', leftover(4, [[0, 1], [1, 0], [2, 1]]))
# duplicates do not break the counting
assert can_finish(2, [[1, 0], [1, 0], [1, 0]]) is True
# scale: a chain of 2000 courses, then the same chain closed into a cycle
chain = [[i + 1, i] for i in range(1999)]
assert can_finish(2000, chain) is True and can_finish(2000, chain + [[0, 1999]]) is False
print('chain of 2000 courses: True; closed into a ring: False')
