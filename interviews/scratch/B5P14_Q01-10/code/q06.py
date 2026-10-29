import random
from bisect import bisect_right, bisect_left

class TimeMap:                         # optimal: per key two parallel sorted lists
    def __init__(self): self.ts = {}; self.vs = {}
    def set(self, key, value, timestamp):
        self.ts.setdefault(key, []).append(timestamp)     # timestamps arrive strictly increasing per key
        self.vs.setdefault(key, []).append(value)
    def get(self, key, timestamp):
        ts = self.ts.get(key)
        if not ts: return ''
        i = bisect_right(ts, timestamp)                   # first index with ts > timestamp
        return self.vs[key][i - 1] if i else ''           # i - 1 is the last ts <= timestamp

class WrongTimeMap(TimeMap):           # the classic bug, kept only to show it fails
    def get(self, key, timestamp):
        ts = self.ts.get(key)
        if not ts: return ''
        i = bisect_left(ts, timestamp)                    # first index with ts >= timestamp
        return self.vs[key][i - 1] if i else ''

class NaiveTimeMap:                    # brute force: one flat list of rows, scan all of them
    def __init__(self): self.rows = []
    def set(self, key, value, timestamp): self.rows.append((key, value, timestamp))
    def get(self, key, timestamp):
        best = None
        for k, v, t in self.rows:
            if k == key and t <= timestamp and (best is None or t > best[0]): best = (t, v)
        return best[1] if best else ''

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

ex = [['set',['love','high',10]],['get',['love',10]],['get',['love',15]],['set',['love','low',20]],['get',['love',5]],
      ['get',['love',19]],['get',['love',20]],['get',['hate',10]]]
want = [None,'high','high',None,'','high','low','']
assert run(TimeMap, [], ex) == want == run(NaiveTimeMap, [], ex)
print("example:", run(TimeMap, [], ex))
print("bisect_left version on the same example:", run(WrongTimeMap, [], ex))
assert run(WrongTimeMap, [], ex) != want

random.seed(14)
for _ in range(1000):
    last = {}; ops = []
    for _ in range(random.randint(0, 40)):
        k = random.choice('abc')
        if random.random() < .5:
            last[k] = last.get(k, 0) + random.randint(1, 4)
            ops.append(['set', [k, 'v%d' % random.randint(0, 99), last[k]]])
        else: ops.append(['get', [k, random.randint(0, 30)]])
    assert run(TimeMap, [], ops) == run(NaiveTimeMap, [], ops), ops
print("1000 random operation sequences: bisect_right version == naive")

# edge cases
m = TimeMap(); assert m.get('x', 5) == ''                          # unknown key
m.set('x', 'a', 3); assert m.get('x', 2) == '' and m.get('x', 3) == 'a' and m.get('x', 10**7) == 'a'   # before first, exact, far after
m = TimeMap()
for t in range(1, 2 * 10**5 + 1): m.set('k', t, t)
assert m.get('k', 10**7) == 2 * 10**5 and m.get('k', 77777) == 77777 and m.get('k', 0) == ''
print("edge asserts ok (unknown key, before first, exact hit, 2*10^5 sets)")
