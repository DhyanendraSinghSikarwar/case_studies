import random

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class NaiveLogger:                       # brute force: remember every print time
    def __init__(self, clock): self.clock = clock; self.times = {}
    def shouldPrint(self, message):
        now = self.clock(); ts = self.times.setdefault(message, [])
        if not ts or now - ts[-1] >= 10: ts.append(now); return True
        return False

class Logger:
    def __init__(self, clock): self.clock = clock; self.last = {}     # message -> time it was last PRINTED
    def shouldPrint(self, message):
        now = self.clock(); p = self.last.get(message)
        if p is None or now - p >= 10:   # exactly 10 later is allowed
            self.last[message] = now; return True
        return False                     # refused: do NOT touch the stored time

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = dict(init=[], ops=[[1, 'shouldPrint', ['foo']], [2, 'shouldPrint', ['bar']], [3, 'shouldPrint', ['foo']], [8, 'shouldPrint', ['bar']],
    [10, 'shouldPrint', ['foo']], [11, 'shouldPrint', ['foo']], [12, 'shouldPrint', ['bar']], [21, 'shouldPrint', ['foo']]])
want = [True, True, False, False, False, True, True, True]
assert run(Logger, **ex) == want == run(NaiveLogger, **ex)
print('example ->', run(Logger, **ex))

random.seed(16)
for case in range(600):
    t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.choice([0, 1, 3, 9, 10, 11])      # boundary-biased gaps around 10
        ops.append([t, 'shouldPrint', [random.choice('ab')]])
    assert run(Logger, [], ops) == run(NaiveLogger, [], ops)
print('600 random timed sequences match the naive reference')

# steady stream every 3 seconds prints at 0, 12, 24 ...
ops = [[t, 'shouldPrint', ['m']] for t in range(0, 40, 3)]
printed = [t for (t, _, _), ok in zip(ops, run(Logger, [], ops)) if ok]
assert printed[:3] == [0, 12, 24]
print('stream every 3 s prints at', printed)

# if a refusal wrongly refreshed the time, the message would never print again
class RefreshBug(Logger):
    def shouldPrint(self, message):
        now = self.clock(); p = self.last.get(message)
        ok = p is None or now - p >= 10
        self.last[message] = now
        return ok
bad = [t for (t, _, _), ok in zip(ops, run(RefreshBug, [], ops)) if ok]
assert bad == [0]
print('buggy refresh-on-refuse prints at', bad)

# same boundary family as the hit counter of Q1: an item of age exactly 10 (here) or 300 (there) is already expired, so the new print is allowed at age >= 10
assert run(Logger, [], [[0, 'shouldPrint', ['x']], [9, 'shouldPrint', ['x']], [10, 'shouldPrint', ['x']]]) == [True, False, True]
assert run(Logger, [], [[5, 'shouldPrint', ['x']], [5, 'shouldPrint', ['x']]]) == [True, False]      # same second
assert run(Logger, [], []) == []
assert run(Logger, [], [[0, 'shouldPrint', ['']]]) == [True]                                            # empty message is a message
print('edge asserts ok')
