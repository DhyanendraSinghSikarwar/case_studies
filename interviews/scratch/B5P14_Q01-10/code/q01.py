import random
from collections import deque

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class HitCounter:                      # optimal: deque of [second, count] + running total
    def __init__(self, clock):
        self.clock = clock; self.q = deque(); self.total = 0
    def _expire(self, now):
        while self.q and self.q[0][0] <= now - 300:   # exactly 300 old is expired
            self.total -= self.q.popleft()[1]
    def hit(self):
        now = self.clock(); self._expire(now)         # expire here too, so hit-only traffic stays bounded
        if self.q and self.q[-1][0] == now: self.q[-1][1] += 1
        else: self.q.append([now, 1])
        self.total += 1
    def getHits(self):
        self._expire(self.clock())
        return self.total

class RingHitCounter:                  # variant: 300 buckets keyed by second % 300, stale check by stamp
    def __init__(self, clock):
        self.clock = clock; self.stamp = [None] * 300; self.cnt = [0] * 300
    def hit(self):
        now = self.clock(); i = now % 300
        if self.stamp[i] != now: self.stamp[i] = now; self.cnt[i] = 0   # stale bucket: reuse it
        self.cnt[i] += 1
    def getHits(self):
        now = self.clock()
        return sum(c for s, c in zip(self.stamp, self.cnt) if s is not None and now - 300 < s <= now)

class NaiveHits:                       # brute force: keep every timestamp, rescan
    def __init__(self, clock): self.clock = clock; self.ts = []
    def hit(self): self.ts.append(self.clock())
    def getHits(self):
        now = self.clock()
        return sum(1 for t in self.ts if now - 300 < t <= now)

def run(cls, ops):
    clk = Clock(); obj = cls(clk); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(obj, m)(*a))
    return out

ex = [[1,'hit',[]],[2,'hit',[]],[3,'hit',[]],[4,'getHits',[]],[300,'getHits',[]],[301,'getHits',[]],
      [301,'hit',[]],[302,'getHits',[]],[310,'getHits',[]]]
want = [None, None, None, 3, 3, 2, None, 2, 1]
for cls in (HitCounter, RingHitCounter, NaiveHits):
    assert run(cls, ex) == want, cls.__name__
print("example ok for all three classes:", run(HitCounter, ex))

random.seed(14)
for case in range(600):
    t = 0; ops = []
    step = random.choice([2, 20, 150])          # small steps: dense; large steps: expiry at 300
    for _ in range(random.randint(0, 60)):
        t += random.randint(0, step)
        ops.append([t, random.choice(['hit', 'hit', 'getHits']), []])
    a = run(HitCounter, ops); assert a == run(NaiveHits, ops) == run(RingHitCounter, ops), ops
print("600 random operation sequences: deque == ring == naive")

# edge cases
assert run(HitCounter, [[5, 'getHits', []]]) == [0]                       # nothing yet
assert run(HitCounter, [[0, 'hit', []], [299, 'getHits', []], [300, 'getHits', []]]) == [None, 1, 0]
assert run(HitCounter, [[7,'hit',[]],[7,'hit',[]],[7,'hit',[]],[7,'getHits',[]]]) == [None]*3 + [3]
clk = Clock(); h = HitCounter(clk); clk.t = 9
for _ in range(10**6): h.hit()                                            # a million hits in one second
assert h.getHits() == 10**6 and len(h.q) == 1
clk.t = 9 + 1000
for s in range(9 + 1000, 9 + 1000 + 5000): clk.t = s; h.hit()       # hits only, never getHits
assert len(h.q) <= 300 and h.total <= 300
print("1,000,000 hits in one second -> 1 deque entry; after 5000 hit-only seconds the deque holds", len(h.q), "entries")
