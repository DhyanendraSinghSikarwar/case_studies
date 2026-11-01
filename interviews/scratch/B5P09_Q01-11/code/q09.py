import itertools
import random
from collections import deque

random.seed(9)

def course_order(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a); indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)   # ascending seed
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []

def feasible_brute(n, pre):
    """Try every permutation (n <= 6)."""
    for p in itertools.permutations(range(n)):
        pos = {c: i for i, c in enumerate(p)}
        if all(pos[b] < pos[a] for a, b in pre):
            return True
    return False

def count_orders(n, pre):
    cnt = 0
    for p in itertools.permutations(range(n)):
        pos = {c: i for i, c in enumerate(p)}
        if all(pos[b] < pos[a] for a, b in pre):
            cnt += 1
    return cnt

def valid(n, pre, got):
    """Checker: [] only if a cycle exists, otherwise a permutation with b before a for every pair."""
    if not feasible_brute(n, pre):
        return got == []
    if sorted(got) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[b] < pos[a] for a, b in pre)

def kahn_always_one_ready(n, pre):
    """Unique-order test: at every step exactly one node has indegree 0."""
    adj = [[] for _ in range(n)]; indeg = [0] * n
    for a, b in pre:
        adj[b].append(a); indeg[a] += 1
    ready = [i for i in range(n) if indeg[i] == 0]; done = 0
    while ready:
        if len(ready) != 1:
            return False
        u = ready.pop(); done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: ready.append(v)
    return done == n

assert course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
assert course_order(2, [[0, 1], [1, 0]]) == []
assert course_order(1, []) == [0]
print('3 prompt examples ok')

for _ in range(1500):
    n = random.randint(1, 6)
    pre = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 7))]
    assert valid(n, pre, course_order(n, pre)), (n, pre)
print('1500 seeded random inputs: output accepted by the validator (permutation, every b before a, [] only on cycles)')

# the uniqueness claim: a topological order is unique  <=>  Kahn never has two ready nodes at once
# <=>  consecutive nodes of the order are joined by prerequisite edges. Exhaustive on n <= 4, all pair sets without loops.
checked = 0
for n in (1, 2, 3, 4):
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    for mask in range(1 << len(pairs)):
        pre = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        cnt = count_orders(n, pre)
        one = kahn_always_one_ready(n, pre)
        assert (cnt == 1) == one, (n, pre, cnt)
        if cnt == 1:
            o = course_order(n, pre)
            es = {(b, a) for a, b in pre}
            assert all((o[i], o[i + 1]) in es for i in range(n - 1)), (n, pre)   # Hamiltonian path in the DAG
        checked += 1
print('uniqueness claim verified exhaustively on', checked, 'prerequisite sets for n = 1..4: unique iff one node is ready at every step')

# example of a non-unique case and the count of valid orders
print('orders for 4 courses with [[1,0],[2,0],[3,1],[3,2]]:', count_orders(4, [[1, 0], [2, 0], [3, 1], [3, 2]]), '(0,1,2,3 and 0,2,1,3)')
print('FIFO Kahn gives', course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]), '; another valid answer is [0, 2, 1, 3]')
chain = [[i + 1, i] for i in range(1999)]
assert course_order(2000, chain) == list(range(2000)) and course_order(2000, chain + [[0, 1999]]) == []
print('chain of 2000: unique order; same chain closed into a ring: []')
