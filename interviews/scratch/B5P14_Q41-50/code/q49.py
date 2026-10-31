import bisect, random
random.seed(49)

class OrderStats:
    def __init__(self, max_value):
        self.n = max_value + 1                # values 0..max_value live at tree positions 1..n
        self.t = [0] * (self.n + 1)
        self.cnt = [0] * self.n               # exact copy counts, so remove can answer True/False
        self.size = 0
        self.top = 1
        while self.top * 2 <= self.n:         # largest power of two <= n
            self.top *= 2

    def _add(self, i, d):
        while i <= self.n:
            self.t[i] += d; i += i & -i

    def insert(self, x):
        self.cnt[x] += 1; self.size += 1; self._add(x + 1, 1)

    def remove(self, x):
        if x < 0 or x >= self.n or self.cnt[x] == 0:
            return False
        self.cnt[x] -= 1; self.size -= 1; self._add(x + 1, -1)
        return True

    def count_le(self, x):
        if x < 0:
            return 0
        i = min(x, self.n - 1) + 1; s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i
        return s

    def kth(self, k):
        if k < 1 or k > self.size:
            return -1
        pos = 0; step = self.top
        while step:                           # binary descent: never overshoot the k-th element
            nxt = pos + step
            if nxt <= self.n and self.t[nxt] < k:
                pos = nxt; k -= self.t[nxt]
            step >>= 1
        return pos                            # position pos+1 holds the answer, i.e. the value pos

class Naive:
    def __init__(self, max_value): self.a = []
    def insert(self, x): bisect.insort(self.a, x)
    def remove(self, x):
        if x in self.a: self.a.remove(x); return True
        return False
    def count_le(self, x): return sum(1 for v in self.a if v <= x)
    def kth(self, k): return self.a[k - 1] if 1 <= k <= len(self.a) else -1

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

ops = [['insert', [5]], ['insert', [3]], ['insert', [5]], ['insert', [9]], ['count_le', [5]], ['kth', [1]], ['kth', [3]], ['kth', [4]],
       ['kth', [5]], ['remove', [5]], ['remove', [7]], ['kth', [3]], ['count_le', [-1]], ['count_le', [10]]]
got = run(OrderStats, [10], ops)
assert got == [None, None, None, None, 3, 3, 5, 9, -1, True, False, 9, 0, 3], got
print('example ->', got)

for _ in range(500):
    mv = random.randint(1, 12)
    ops = []
    for _ in range(random.randint(0, 40)):
        r = random.random()
        if r < .3: ops.append(['insert', [random.randint(0, mv)]])
        elif r < .45: ops.append(['remove', [random.randint(0, mv)]])
        elif r < .7: ops.append(['count_le', [random.randint(-2, mv + 2)]])
        else: ops.append(['kth', [random.randint(-1, 12)]])
    assert run(OrderStats, [mv], ops) == run(Naive, [mv], ops), (mv, ops)
print('500 random operation sequences match the naive reference (max_value 1..12)')

assert run(OrderStats, [1], [['kth', [1]], ['insert', [0]], ['kth', [1]], ['remove', [0]], ['remove', [0]], ['count_le', [5]]]) == [-1, None, 0, True, False, 0]
assert run(OrderStats, [8], [['insert', [8]], ['insert', [0]], ['kth', [2]], ['count_le', [100]]]) == [None, None, 8, 2]   # n = 9, not a power of two
M = 10**6
o = OrderStats(M)
vals = [random.randint(0, M) for _ in range(20000)]
for v in vals: o.insert(v)
s = sorted(vals)
assert all(o.kth(k) == s[k - 1] for k in (1, 2, 777, 10000, 20000)) and o.count_le(M) == 20000
print('max_value = 10^6 with 20000 inserts ok')
