import random
from bisect import bisect_left, bisect_right
from collections import defaultdict

class RangeFreqQuery:
    def __init__(self, arr):
        self.pos = defaultdict(list)
        for i, v in enumerate(arr):                  # positions are appended in increasing order, so each list is sorted
            self.pos[v].append(i)

    def query(self, left, right, value):             # O(log k), k = occurrences of value
        p = self.pos.get(value)                      # .get: do not create an entry for an unseen value
        if not p:
            return 0
        return bisect_right(p, right) - bisect_left(p, left)

class Naive:
    def __init__(self, arr): self.a = list(arr)
    def query(self, left, right, value): return self.a[left:right + 1].count(value)

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

arr = [12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]
ops = [['query', [1, 2, 4]], ['query', [0, 11, 33]], ['query', [3, 3, 56]], ['query', [0, 11, 99]], ['query', [4, 8, 22]]]
assert run(RangeFreqQuery, [arr], ops) == [1, 2, 1, 0, 2]
print('example:', run(RangeFreqQuery, [arr], ops))

# bounds: both ends inclusive
q = RangeFreqQuery([5, 5, 5, 5])
assert q.query(0, 3, 5) == 4 and q.query(1, 2, 5) == 2 and q.query(2, 2, 5) == 1 and q.query(0, 0, 6) == 0
assert len(q.pos) == 1                                # querying an unseen value did not add a key
assert RangeFreqQuery([1]).query(0, 0, 1) == 1

random.seed(30)
n_ops = 0
for _ in range(500):
    n = random.randint(1, 20)
    arr = [random.randint(1, 5) for _ in range(n)]
    ops = []
    for _ in range(30):
        l = random.randrange(n); r = random.randint(l, n - 1)
        ops.append(['query', [l, r, random.randint(1, 7)]])      # 6 and 7 never occur
    assert run(RangeFreqQuery, [arr], ops) == run(Naive, [arr], ops), (arr, ops)
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 arrays,', n_ops, 'queries')

# memory claim: a prefix-count table per value needs (n + 1) * distinct cells
n, distinct = 10**5, 10**4
print('prefix table cells for n = 10^5 and 10^4 distinct values:', (n + 1) * distinct, 'vs positions lists:', n)
big = [random.randint(1, 10**4) for _ in range(10**5)]
f = RangeFreqQuery(big)
assert sum(len(v) for v in f.pos.values()) == 10**5
for _ in range(2000):
    l = random.randrange(10**5); r = random.randint(l, 10**5 - 1); v = random.randint(1, 10**4)
    assert f.query(l, r, v) == big[l:r + 1].count(v)
print('n = 10^5, 2000 random queries ok')
