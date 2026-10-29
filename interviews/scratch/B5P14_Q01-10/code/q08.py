import random
from fractions import Fraction

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class TokenBucket:                     # optimal: lazy refill, integer arithmetic
    def __init__(self, clock, capacity, rate):
        self.clock = clock; self.cap = capacity; self.rate = rate
        self.tokens = capacity; self.last = clock()          # starts full; clock reads 0 here
    def allow(self, cost=1):
        now = self.clock()
        self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate)   # refill for elapsed time
        self.last = now                                      # updated on EVERY call, accepted or not
        if cost <= self.tokens:
            self.tokens -= cost; return True
        return False                                         # a rejection removes nothing

class NaiveBucket:                     # brute force: simulate one second at a time
    def __init__(self, clock, capacity, rate):
        self.clock = clock; self.cap = capacity; self.rate = rate; self.tokens = capacity; self.last = clock()
    def allow(self, cost=1):
        now = self.clock()
        while self.last < now:
            self.tokens = min(self.cap, self.tokens + self.rate); self.last += 1
        if cost <= self.tokens: self.tokens -= cost; return True
        return False

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = [[0,'allow',[]],[0,'allow',[]],[0,'allow',[]],[0,'allow',[]],[1,'allow',[]],[1,'allow',[]],[10,'allow',[3]],[10,'allow',[1]],[11,'allow',[2]]]
want = [True, True, True, False, True, False, True, False, False]
assert run(TokenBucket, [3, 1], ex) == want == run(NaiveBucket, [3, 1], ex)
print("example:", run(TokenBucket, [3, 1], ex))

random.seed(14)
for _ in range(1500):
    cap = random.randint(1, 6); rate = random.randint(0, 3); t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 5); ops.append([t, 'allow', random.choice([[], [], [random.randint(1, 8)]])])
    assert run(TokenBucket, [cap, rate], ops) == run(NaiveBucket, [cap, rate], ops), (cap, rate, ops)
print("1500 random clocked sequences: lazy-refill bucket == one-second-at-a-time naive")

# edge cases
assert run(TokenBucket, [3, 0], [[0,'allow',[3]],[100,'allow',[]]]) == [True, False]     # rate 0: never refills
assert run(TokenBucket, [5, 1], [[0,'allow',[6]],[50,'allow',[6]]]) == [False, False]    # cost > capacity never succeeds
assert run(TokenBucket, [5, 2], [[0,'allow',[5]],[1,'allow',[3]],[1,'allow',[2]]]) == [True, False, True]  # 2 tokens at t=1: cost 3 fails, cost 2 passes
# rejection still moves `last`: refilling must not be counted twice
assert run(TokenBucket, [2, 1], [[0,'allow',[2]],[1,'allow',[2]],[2,'allow',[2]]]) == [True, False, True]
b = TokenBucket(Clock(), 10**6, 10**6); b.clock.t = 10**9
assert b.allow(10**6) and b.tokens == 0                    # huge elapsed time is capped at capacity
# why floats are fragile: ten 0.1-second ticks do not add up to one second
f = 0.0
for _ in range(10): f += 0.1
print("ten additions of 0.1 equal 1.0?", f == 1.0, "; Fraction version:", sum([Fraction(1, 10)] * 10) == 1)
print("edge asserts ok (rate 0, cost > capacity, rejection updates last, capacity cap, 10^6 values)")
