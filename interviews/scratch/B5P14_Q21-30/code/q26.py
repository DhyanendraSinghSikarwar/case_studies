import random

class UndergroundSystem:
    def __init__(self):
        self.open = {}                      # id -> (station, t_in)
        self.done = {}                      # (start, end) -> [total, count]

    def checkIn(self, id, station, t):      # O(1)
        assert id not in self.open, 'one open trip per id'
        self.open[id] = (station, t)

    def checkOut(self, id, station, t):     # O(1)
        if id not in self.open:             # my rule: reject loudly, never invent a trip
            raise ValueError('check-out without check-in: %r' % (id,))
        start, t_in = self.open.pop(id)
        rec = self.done.setdefault((start, station), [0, 0])
        rec[0] += t - t_in
        rec[1] += 1

    def getAverageTime(self, start, end):   # O(1)
        total, count = self.done[(start, end)]
        return total / count

class Naive:
    """Keeps every trip and every duration, rescans lists on each query."""
    def __init__(self): self.open = []; self.trips = []
    def checkIn(self, id, station, t): self.open.append((id, station, t))
    def checkOut(self, id, station, t):
        for k, (i, s, ti) in enumerate(self.open):
            if i == id:
                del self.open[k]; self.trips.append((s, station, t - ti)); return
    def getAverageTime(self, start, end):
        d = [x for s, e, x in self.trips if s == start and e == end]
        return sum(d) / len(d)

def run(cls, ops):
    obj = cls()
    return [getattr(obj, m)(*a) for m, a in ops]

ex = [['checkIn', [45, 'A', 3]], ['checkIn', [32, 'A', 8]], ['checkOut', [45, 'B', 15]], ['checkOut', [32, 'B', 22]],
      ['getAverageTime', ['A', 'B']], ['checkIn', [10, 'B', 24]], ['checkOut', [10, 'A', 40]],
      ['getAverageTime', ['B', 'A']], ['checkIn', [45, 'A', 30]], ['checkOut', [45, 'B', 36]],
      ['getAverageTime', ['A', 'B']]]
want = [None, None, None, None, 13.0, None, None, 16.0, None, None, 10.666666666666666]
assert run(UndergroundSystem, ex) == want
print('example:', run(UndergroundSystem, ex))

# direction matters; check-out without check-in is rejected
u = UndergroundSystem()
u.checkIn(1, 'X', 0); u.checkOut(1, 'Y', 5)
assert u.getAverageTime('X', 'Y') == 5.0
try:
    u.getAverageTime('Y', 'X'); raise SystemExit('should raise')
except KeyError:
    print('Y -> X has no completed trip: KeyError (the checker never asks)')
try:
    u.checkOut(99, 'Y', 7); raise SystemExit('should raise')
except ValueError as e:
    print('rejected:', e)
u.checkIn(1, 'X', 10); u.checkOut(1, 'X', 10)             # zero-length trip, same start and end is allowed
assert u.getAverageTime('X', 'X') == 0.0

# operation-sequence oracle: random valid call sequences
random.seed(26)
stations = ['A', 'B', 'C']
n_ops = 0
for _ in range(500):
    ops, open_ids, finished, t = [], {}, set(), 0
    for _ in range(random.randint(1, 40)):
        t += random.randint(0, 5)
        r = random.random()
        free = [i for i in range(6) if i not in open_ids]
        if r < 0.4 and free:
            i = random.choice(free); s = random.choice(stations); open_ids[i] = s
            ops.append(['checkIn', [i, s, t]])
        elif r < 0.75 and open_ids:
            i = random.choice(list(open_ids)); s = random.choice(stations)
            finished.add((open_ids.pop(i), s)); ops.append(['checkOut', [i, s, t]])
        elif finished:
            a, b = random.choice(sorted(finished)); ops.append(['getAverageTime', [a, b]])
    assert run(UndergroundSystem, ops) == run(Naive, ops), ops
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 sequences,', n_ops, 'operations')
