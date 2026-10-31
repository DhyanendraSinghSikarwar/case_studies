import heapq, random

class NaiveStock:                       # brute force: rescan the dict every call
    def __init__(self): self.p = {}
    def update(self, timestamp, price): self.p[timestamp] = price
    def current(self): return self.p[max(self.p)]
    def maximum(self): return max(self.p.values())
    def minimum(self): return min(self.p.values())

class StockPrice:                       # optimal: dict + two heaps with lazy deletion
    def __init__(self):
        self.price = {}                 # timestamp -> latest price
        self.latest = -1                # largest timestamp seen
        self.lo = []                    # (price, ts)
        self.hi = []                    # (-price, ts)
        self.pushed = 0; self.popped = 0   # counters only for the amortised claim
    def update(self, timestamp, price):
        self.price[timestamp] = price
        if timestamp > self.latest: self.latest = timestamp
        heapq.heappush(self.lo, (price, timestamp))
        heapq.heappush(self.hi, (-price, timestamp))
        self.pushed += 2
    def current(self): return self.price[self.latest]
    def maximum(self):
        while self.price[self.hi[0][1]] != -self.hi[0][0]:   # stale: that ts now has another price
            heapq.heappop(self.hi); self.popped += 1
        return -self.hi[0][0]
    def minimum(self):
        while self.price[self.lo[0][1]] != self.lo[0][0]:
            heapq.heappop(self.lo); self.popped += 1
        return self.lo[0][0]

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[], ops=[['update', [1, 10]], ['update', [2, 5]], ['current', []], ['maximum', []], ['update', [1, 3]],
          ['maximum', []], ['update', [4, 2]], ['minimum', []], ['current', []], ['update', [4, 20]], ['maximum', []], ['minimum', []]])
want = [None, None, 5, 10, None, 5, None, 2, 2, None, 20, 3]
assert run(StockPrice, **ex) == want == run(NaiveStock, **ex)
print('example ->', run(StockPrice, **ex))

random.seed(11)
for case in range(500):
    ops = [['update', [random.randint(1, 8), random.randint(1, 6)]]]   # first call must be update
    for _ in range(random.randint(0, 40)):
        if random.random() < 0.5: ops.append(['update', [random.randint(1, 8), random.randint(1, 6)]])
        else: ops.append([random.choice(['current', 'maximum', 'minimum']), []])
    assert run(StockPrice, [], ops) == run(NaiveStock, [], ops), ops
print('500 random sequences match the naive reference')

# amortised claim: every entry is popped at most once, so pops <= pushes
s = StockPrice()
for i in range(20000):
    s.update(random.randint(1, 50), random.randint(1, 10**6))
    if i % 7 == 0: s.maximum(); s.minimum()
assert s.popped <= s.pushed
print('pushed', s.pushed, 'popped', s.popped, '(popped <= pushed)')

# edge cases
s = StockPrice(); s.update(5, 9)
assert (s.current(), s.maximum(), s.minimum()) == (9, 9, 9)
s.update(5, 4); assert (s.current(), s.maximum(), s.minimum()) == (4, 4, 4)   # correction of the only record
s.update(2, 4); assert s.current() == 4 and s.maximum() == 4                  # older timestamp, same price
s.update(5, 4); assert s.minimum() == 4                                        # same value re-sent: duplicate heap entry is fine
s.update(1, 100); assert s.current() == 4 and s.maximum() == 100               # late record does not change current
s.update(1, 1); assert s.maximum() == 4 and s.minimum() == 1
print('edge asserts ok')
