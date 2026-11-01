import random

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class NaiveFixed:                        # brute force: keep every accepted timestamp, count those in the same window
    def __init__(self, clock, limit, window): self.clock = clock; self.limit = limit; self.w = window; self.acc = {}
    def allow(self, user):
        now = self.clock(); k = now // self.w
        n = sum(1 for t in self.acc.get(user, []) if t // self.w == k)
        if n < self.limit:
            self.acc.setdefault(user, []).append(now); return True
        return False

class FixedWindowLimiter:
    def __init__(self, clock, limit, window):
        self.clock = clock; self.limit = limit; self.window = window
        self.state = {}                  # user -> [window index, accepted count]
    def allow(self, user):
        k = self.clock() // self.window
        st = self.state.get(user)
        if st is None or st[0] != k: st = self.state[user] = [k, 0]    # new window: reset
        if st[1] < self.limit:
            st[1] += 1; return True
        return False                     # rejected requests are not counted

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = dict(init=[2, 10], ops=[[8, 'allow', ['u']], [9, 'allow', ['u']], [9, 'allow', ['u']], [10, 'allow', ['u']],
    [11, 'allow', ['u']], [11, 'allow', ['u']], [20, 'allow', ['u']], [20, 'allow', ['v']]])
want = [True, True, False, True, True, False, True, True]
assert run(FixedWindowLimiter, **ex) == want == run(NaiveFixed, **ex)
print('example ->', run(FixedWindowLimiter, **ex))

random.seed(14)
for case in range(600):
    limit = random.randint(1, 3); w = random.randint(1, 6); t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 4)
        ops.append([t, 'allow', [random.choice('uvw')]])
    assert run(FixedWindowLimiter, [limit, w], ops) == run(NaiveFixed, [limit, w], ops)
print('600 random timed sequences match the naive reference')

# the boundary burst: 4 accepted in 4 seconds (t = 8..11) with limit 2 per 10 s
res = run(FixedWindowLimiter, [2, 10], [[t, 'allow', ['u']] for t in (8, 9, 10, 11)])
assert res == [True] * 4
# a sliding window log (accept if < limit accepted in (now-window, now]) would refuse t=10 and t=11
def sliding(limit, window, times):
    acc = []; out = []
    for t in times:
        n = sum(1 for a in acc if a > t - window)
        if n < limit: acc.append(t); out.append(True)
        else: out.append(False)
    return out
assert sliding(2, 10, (8, 9, 10, 11)) == [True, True, False, False]
print('fixed window', res, '| sliding window', sliding(2, 10, (8, 9, 10, 11)))

# edge cases
assert run(FixedWindowLimiter, [1, 5], [[0, 'allow', ['a']], [4, 'allow', ['a']], [5, 'allow', ['a']]]) == [True, False, True]  # t=5 is a new window
assert run(FixedWindowLimiter, [3, 1], [[7, 'allow', ['a']]] * 4) == [True, True, True, False]
assert run(FixedWindowLimiter, [1, 1], [[t, 'allow', ['a']] for t in range(5)]) == [True] * 5     # window 1: every second is new
assert run(FixedWindowLimiter, [1, 10], []) == []
assert run(FixedWindowLimiter, [1, 10], [[0, 'allow', ['a']], [0, 'allow', ['b']], [0, 'allow', ['a']]]) == [True, True, False]  # users independent
print('edge asserts ok')
