import random
from collections import deque

class MovingAverage:                   # optimal: deque + exact integer running total
    def __init__(self, size):
        self.size = size; self.q = deque(); self.total = 0
    def next(self, val):
        self.q.append(val); self.total += val
        if len(self.q) > self.size:
            self.total -= self.q.popleft()      # the value that fell out of the window
        return self.total / len(self.q)         # the only float, formed at the end

class NaiveMA:                         # brute force: keep everything, re-sum the last `size` each call
    def __init__(self, size): self.size = size; self.a = []
    def next(self, val):
        self.a.append(val); w = self.a[-self.size:]
        return sum(w) / len(w)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

ex = [['next',[1]],['next',[10]],['next',[3]],['next',[5]],['next',[-4]]]
want = [1.0, 5.5, 4.666666666666667, 6.0, 1.3333333333333333]
assert run(MovingAverage, [3], ex) == want == run(NaiveMA, [3], ex)
print("example:", run(MovingAverage, [3], ex))

random.seed(14)
for _ in range(500):
    size = random.randint(1, 6)
    ops = [['next', [random.randint(-10**4, 10**4)]] for _ in range(random.randint(0, 40))]
    assert run(MovingAverage, [size], ops) == run(NaiveMA, [size], ops)
print("500 random sequences: deque version == naive version (exact float equality)")

# edge cases
assert run(MovingAverage, [1], [['next',[7]],['next',[-3]]]) == [7.0, -3.0]        # size 1
m = MovingAverage(1000)
for _ in range(5000): r = m.next(10**4)
assert r == 10**4 and m.total == 1000 * 10**4 and len(m.q) == 1000                  # max size, max value
m = MovingAverage(3); assert [m.next(0) for _ in range(4)] == [0.0]*4              # all zeros
m = MovingAverage(2)
assert [m.next(v) for v in (-10**4, -10**4, 10**4)] == [-10000.0, -10000.0, 0.0]   # negatives
# floats would drift: sum of 0.1s vs the exact integer total
f = 0.0
for _ in range(10): f += 0.1
print("float total after ten +0.1:", f, "(integer totals never drift)")
print("edge asserts ok")
