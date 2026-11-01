import random
random.seed(44)

class RangeAddSum:
    def __init__(self, nums):
        self.n = len(nums)
        self.sm = [0] * (4 * self.n)          # sm[o]: TRUE sum of node o's range
        self.lz = [0] * (4 * self.n)          # lz[o]: add promised to both children, not yet pushed
        self._build(1, 0, self.n - 1, nums)

    def _build(self, o, lo, hi, a):
        if lo == hi:
            self.sm[o] = a[lo]; return
        mid = (lo + hi) // 2
        self._build(2 * o, lo, mid, a); self._build(2 * o + 1, mid + 1, hi, a)
        self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]

    def _apply(self, o, lo, hi, v):           # v * LENGTH, not v
        self.sm[o] += v * (hi - lo + 1); self.lz[o] += v

    def _push(self, o, lo, hi):
        if self.lz[o]:
            mid = (lo + hi) // 2
            self._apply(2 * o, lo, mid, self.lz[o])
            self._apply(2 * o + 1, mid + 1, hi, self.lz[o])
            self.lz[o] = 0

    def _add(self, o, lo, hi, l, r, v):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self._apply(o, lo, hi, v); return
        self._push(o, lo, hi)                 # push BEFORE recursing
        mid = (lo + hi) // 2
        self._add(2 * o, lo, mid, l, r, v); self._add(2 * o + 1, mid + 1, hi, l, r, v)
        self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]

    def _sum(self, o, lo, hi, l, r):
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.sm[o]
        self._push(o, lo, hi)
        mid = (lo + hi) // 2
        return self._sum(2 * o, lo, mid, l, r) + self._sum(2 * o + 1, mid + 1, hi, l, r)

    def add(self, l, r, v):
        self._add(1, 0, self.n - 1, l, r, v)

    def sum(self, l, r):
        return self._sum(1, 0, self.n - 1, l, r)

class Naive:
    def __init__(self, nums): self.a = list(nums)
    def add(self, l, r, v):
        for i in range(l, r + 1): self.a[i] += v
    def sum(self, l, r): return sum(self.a[l:r + 1])

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ex_ops = [['sum', [0, 4]], ['add', [1, 3, 10]], ['sum', [0, 4]], ['sum', [2, 2]], ['add', [0, 4, -1]], ['sum', [0, 1]], ['sum', [3, 4]]]
got = run(RangeAddSum, [[1, 2, 3, 4, 5]], ex_ops)
assert got == [15, None, 45, 13, None, 11, 17], got
print('example ->', got)

for _ in range(500):
    n = random.randint(1, 9)
    init = [[random.randint(-5, 5) for _ in range(n)]]
    ops = []
    for _ in range(random.randint(0, 30)):
        l = random.randrange(n); r = random.randrange(l, n)
        ops.append(['add', [l, r, random.randint(-9, 9)]] if random.random() < .5 else ['sum', [l, r]])
    assert run(RangeAddSum, init, ops) == run(Naive, init, ops), (init, ops)
print('500 random operation sequences match the naive reference')

assert run(RangeAddSum, [[7]], [['sum', [0, 0]], ['add', [0, 0, -7]], ['sum', [0, 0]]]) == [7, None, 0]   # n = 1
big = 10**9
assert run(RangeAddSum, [[0] * 3], [['add', [0, 2, big]], ['add', [0, 2, big]], ['sum', [0, 2]]])[-1] == 6 * big
# the classic bug: using v instead of v * length
class Bug(RangeAddSum):
    def _apply(self, o, lo, hi, v): self.sm[o] += v; self.lz[o] += v
bad = run(Bug, [[1, 2, 3, 4, 5]], ex_ops)
print('bug (v instead of v*length) gives', bad)
assert bad != got

n = 10**5
obj = RangeAddSum([0] * n)
for i in range(0, n, 50): obj.add(i, n - 1, 1)
assert obj.sum(0, n - 1) == sum(n - i for i in range(0, n, 50))
print('n = 10^5 build + 2000 range adds ok')
