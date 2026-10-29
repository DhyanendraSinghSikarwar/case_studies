import random
from collections import deque

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class SlidingWindowLimiter:            # optimal: per-user deque of ACCEPTED timestamps
    def __init__(self, clock, limit, window):
        self.clock = clock; self.limit = limit; self.window = window; self.log = {}
    def allow(self, user):
        now = self.clock()
        q = self.log.setdefault(user, deque())
        while q and q[0] <= now - self.window:      # window is (now - window, now]: age == window is expired
            q.popleft()
        if len(q) < self.limit:
            q.append(now); return True              # only accepted requests are recorded
        return False

class NaiveLimiter:                    # brute force: one flat list of accepted (user, t), rescanned
    def __init__(self, clock, limit, window): self.clock = clock; self.limit = limit; self.window = window; self.acc = []
    def allow(self, user):
        now = self.clock()
        n = sum(1 for u, t in self.acc if u == user and now - self.window < t <= now)
        if n < self.limit: self.acc.append((user, now)); return True
        return False

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = [[0,'allow',['u']],[5,'allow',['u']],[9,'allow',['u']],[10,'allow',['u']],[10,'allow',['v']],[15,'allow',['u']],[16,'allow',['u']]]
want = [True, True, False, True, True, True, False]
assert run(SlidingWindowLimiter, [2, 10], ex) == want == run(NaiveLimiter, [2, 10], ex)
print("example:", run(SlidingWindowLimiter, [2, 10], ex))

random.seed(14)
for _ in range(1500):
    limit = random.randint(1, 4); window = random.randint(1, 8); t = 0; ops = []
    for _ in range(random.randint(0, 50)):
        t += random.randint(0, 4); ops.append([t, 'allow', [random.choice('uvw')]])
    assert run(SlidingWindowLimiter, [limit, window], ops) == run(NaiveLimiter, [limit, window], ops), (limit, window, ops)
print("1500 random clocked sequences: deque limiter == naive")

# boundary and edge cases
def seq(limit, window, times, user='u'): return run(SlidingWindowLimiter, [limit, window], [[t, 'allow', [user]] for t in times])
assert seq(2, 10, [0, 5, 9, 10]) == [True, True, False, True]       # age exactly 10 has expired
assert seq(1, 3, [0, 2, 3]) == [True, False, True]                  # window 3: t=3 sees (0,3], t=0 is out
assert seq(2, 5, [7, 7, 7, 7]) == [True, True, False, False]        # same second
assert seq(1, 5, [0, 1, 2, 3, 4, 5]) == [True, False, False, False, False, True]   # rejected calls are NOT recorded
assert run(SlidingWindowLimiter, [1, 1], []) == []                  # no calls
q = SlidingWindowLimiter(Clock(), 100, 3600)
for i in range(10**5): q.clock.t = i // 10; q.allow('u')
assert len(q.log['u']) <= 100                                       # memory O(limit)
print("edge asserts ok (boundary at age == window, same second, rejected not recorded, memory <= limit)")
