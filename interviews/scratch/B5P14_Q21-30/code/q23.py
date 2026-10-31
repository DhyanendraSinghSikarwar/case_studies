import random

class MinSegTree:
    """Bottom-up segment tree for range minimum with point assignment. tree[1] is the root, leaves at n..2n-1."""
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1):                 # O(n) build
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, v):                                # set nums[i] = v, O(log n)
        i += self.n
        self.tree[i] = v
        while i > 1:
            i >>= 1
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, l, r):                                 # min of nums[l..r] inclusive, O(log n)
        res = float('inf')
        l += self.n
        r += self.n + 1                                    # half-open [l, r)
        while l < r:
            if l & 1:                                      # l is a right child: take it, move right
                res = min(res, self.tree[l]); l += 1
            if r & 1:                                      # r is a right child: its left sibling r-1 is inside
                r -= 1; res = min(res, self.tree[r])
            l >>= 1; r >>= 1
        return res

class Naive:
    def __init__(self, nums): self.a = list(nums)
    def update(self, i, v): self.a[i] = v
    def query(self, l, r): return min(self.a[l:r + 1])

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ex1 = ([[5, 3, 8, 1, 9, 2]], [['query', [0, 5]], ['query', [2, 4]], ['update', [3, 10]], ['query', [0, 5]],
       ['query', [2, 4]], ['update', [0, 0]], ['query', [0, 1]]])
ex2 = ([[4]], [['query', [0, 0]], ['update', [0, -2]], ['query', [0, 0]]])
assert run(MinSegTree, *ex1) == [1, 1, None, 2, 8, None, 0]
assert run(MinSegTree, *ex2) == [4, None, -2]
print('example 1:', run(MinSegTree, *ex1))
print('example 2:', run(MinSegTree, *ex2))

# exhaustive check of every (l, r) for every length 1..20 (non powers of two included)
random.seed(23)
for n in range(1, 21):
    a = [random.randint(-9, 9) for _ in range(n)]
    t = MinSegTree(a)
    for l in range(n):
        for r in range(l, n):
            assert t.query(l, r) == min(a[l:r + 1]), (n, l, r)
print('exhaustive all (l, r), n = 1..20 ok (includes n = 3, 5, 6, 7 ... not powers of two)')

# the same bottom-up code with a different commutative, associative op (sum) also works for any n
class SumSeg(MinSegTree):
    def __init__(self, nums):
        self.n = len(nums); self.tree = [0] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1): self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    def update(self, i, v):
        i += self.n; self.tree[i] = v
        while i > 1: i >>= 1; self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    def query(self, l, r):
        res = 0; l += self.n; r += self.n + 1
        while l < r:
            if l & 1: res += self.tree[l]; l += 1
            if r & 1: r -= 1; res += self.tree[r]
            l >>= 1; r >>= 1
        return res
a = [random.randint(-9, 9) for _ in range(13)]
s = SumSeg(a)
assert all(s.query(l, r) == sum(a[l:r + 1]) for l in range(13) for r in range(l, 13))
print('same loop with + instead of min ok for n = 13')

# why a Fenwick tree cannot do min with raises: a 'prefix min' BIT only ever keeps the smaller value
class BadMinBIT:
    def __init__(self, n): self.t = [float('inf')] * (n + 1); self.n = n
    def set(self, i, v):                                   # i is 1-based
        while i <= self.n: self.t[i] = min(self.t[i], v); i += i & -i
    def prefix_min(self, i):
        res = float('inf')
        while i > 0: res = min(res, self.t[i]); i -= i & -i
        return res
b = BadMinBIT(4)
for i, v in enumerate([5, 3, 8, 1], 1): b.set(i, v)
b.set(4, 10)                                              # raise the 1 to 10: the stored 1 cannot be undone
print('BIT prefix_min after raising 1 -> 10:', b.prefix_min(4), '(true answer 3)')
assert b.prefix_min(4) == 1 != 3

# operation-sequence oracle against the naive version
cases = ops_total = 0
for _ in range(400):
    n = random.randint(1, 12)
    init = [[random.randint(-20, 20) for _ in range(n)]]
    ops = []
    for _ in range(random.randint(1, 40)):
        if random.random() < 0.4:
            ops.append(['update', [random.randrange(n), random.randint(-30, 30)]])
        else:
            l = random.randrange(n); r = random.randint(l, n - 1)
            ops.append(['query', [l, r]])
    assert run(MinSegTree, init, ops) == run(Naive, init, ops), (init, ops)
    cases += 1; ops_total += len(ops)
print('operation-sequence oracle ok:', cases, 'sequences,', ops_total, 'operations')
