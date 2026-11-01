import random
from bisect import bisect_right

class NaiveSnapshot:                     # brute force: copy the whole array on snap, O(length) per snap
    def __init__(self, length): self.cur = [0] * length; self.snaps = []
    def set(self, index, val): self.cur[index] = val
    def snap(self): self.snaps.append(list(self.cur)); return len(self.snaps) - 1
    def get(self, index, snap_id): return self.snaps[snap_id][index]

class SnapshotArray:
    def __init__(self, length):
        self.ids = [[0] for _ in range(length)]     # per index: snap ids at which it was set (initial 0)
        self.vals = [[0] for _ in range(length)]    # parallel values; initial pair (0, 0)
        self.sid = 0                                # id the NEXT snap() will return = current epoch
    def set(self, index, val):
        ids, vals = self.ids[index], self.vals[index]
        if ids[-1] == self.sid: vals[-1] = val      # same epoch: overwrite, no new pair
        else: ids.append(self.sid); vals.append(val)
    def snap(self):
        self.sid += 1; return self.sid - 1          # O(1): nothing is copied
    def get(self, index, snap_id):
        ids = self.ids[index]
        return self.vals[index][bisect_right(ids, snap_id) - 1]   # last pair with id <= snap_id

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[3], ops=[['set', [0, 5]], ['snap', []], ['set', [0, 6]], ['get', [0, 0]], ['set', [1, 9]], ['set', [1, 8]],
    ['snap', []], ['get', [1, 0]], ['get', [1, 1]], ['get', [0, 1]], ['get', [2, 1]]])
want = [None, 0, None, 5, None, None, 1, 0, 8, 6, 0]
assert run(SnapshotArray, **ex) == want == run(NaiveSnapshot, **ex)
print('example ->', run(SnapshotArray, **ex))

random.seed(18)
for case in range(600):
    n = random.randint(1, 4); ops = []; snaps = 0
    for _ in range(random.randint(0, 40)):
        r = random.random()
        if r < 0.4: ops.append(['set', [random.randrange(n), random.randint(0, 9)]])
        elif r < 0.6: ops.append(['snap', []]); snaps += 1
        elif snaps: ops.append(['get', [random.randrange(n), random.randrange(snaps)]])
    assert run(SnapshotArray, [n], ops) == run(NaiveSnapshot, [n], ops)
print('600 random sequences match the naive reference')

# memory: pairs stored = number of distinct (index, epoch) sets, not length * snaps
s = SnapshotArray(50000)
for i in range(1000): s.set(i % 7, i); s.snap()
pairs = sum(len(x) for x in s.ids)
assert pairs == 50000 + 999                 # 1000 sets, but the very first one overwrote its index's initial (0, 0) pair
print('pairs stored', pairs, 'versus a full copy per snap', 50000 * 1000)

# edge cases
s = SnapshotArray(1); assert s.snap() == 0 and s.get(0, 0) == 0           # snapshot of untouched array
s.set(0, 0); s.set(0, 0); assert s.snap() == 1 and s.get(0, 1) == 0
s.set(0, 4); s.set(0, 5); assert s.get(0, 1) == 0 and s.snap() == 2 and s.get(0, 2) == 5   # double set in one epoch
assert s.get(0, 0) == 0 and len(s.ids[0]) == 3                              # pairs for epochs 0, 1 and 2
print('pairs for index 0:', list(zip(s.ids[0], s.vals[0])))
print('edge asserts ok')
