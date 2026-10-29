import heapq, random
from collections import OrderedDict

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

class NaiveTTL:                          # brute force: list of [key, value, expiry], least recent first, O(n) per call
    def __init__(self, clock, capacity): self.clock = clock; self.cap = capacity; self.items = []
    def _live(self):
        now = self.clock(); self.items = [e for e in self.items if e[2] > now]
    def put(self, key, value, ttl):
        self._live(); now = self.clock()
        for i, e in enumerate(self.items):
            if e[0] == key: del self.items[i]; break
        else:
            if len(self.items) >= self.cap: self.items.pop(0)     # least recently used LIVE key
        self.items.append([key, value, now + ttl])
    def get(self, key):
        self._live()
        for i, e in enumerate(self.items):
            if e[0] == key: self.items.append(self.items.pop(i)); return e[1]
        return -1
    def size(self): self._live(); return len(self.items)

class TTLCache:
    def __init__(self, clock, capacity):
        self.clock = clock; self.cap = capacity
        self.od = OrderedDict()          # key -> (value, version); order = recency, LRU first
        self.heap = []                   # (expiry, key, version); stale versions skipped lazily
        self.version = 0
    def _purge(self):
        now = self.clock()
        while self.heap and self.heap[0][0] <= now:          # expiry <= now means already gone
            _, key, ver = heapq.heappop(self.heap)
            if key in self.od and self.od[key][1] == ver: del self.od[key]
    def put(self, key, value, ttl):
        self._purge()                                         # 1. drop every expired entry first
        now = self.clock()
        if key in self.od: del self.od[key]                   # 2. replace: new value, new life, most recent
        elif len(self.od) >= self.cap: self.od.popitem(last=False)   # 3. evict LRU live key
        self.version += 1
        self.od[key] = (value, self.version)
        heapq.heappush(self.heap, (now + ttl, key, self.version))
    def get(self, key):
        self._purge()
        if key not in self.od: return -1
        self.od.move_to_end(key)                              # refresh recency, not life
        return self.od[key][0]
    def size(self): self._purge(); return len(self.od)

class NoPurgeBug(TTLCache):              # deliberately wrong: evicts by recency without purging first
    def put(self, key, value, ttl):
        now = self.clock()
        if key in self.od: del self.od[key]
        elif len(self.od) >= self.cap: self.od.popitem(last=False)
        self.version += 1; self.od[key] = (value, self.version)
        heapq.heappush(self.heap, (now + ttl, key, self.version))

def run(cls, init, ops):
    clk = Clock(); o = cls(clk, *init); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(o, m)(*a))
    return out

ex = dict(init=[2], ops=[[0, 'put', ['a', 1, 10]], [1, 'put', ['b', 2, 3]], [2, 'get', ['a']], [3, 'put', ['c', 3, 10]],
    [3, 'get', ['b']], [4, 'size', []], [10, 'get', ['a']], [10, 'size', []], [11, 'put', ['c', 9, 5]], [15, 'get', ['c']], [16, 'get', ['c']]])
want = [None, None, 1, None, -1, 2, -1, 1, None, 9, -1]
assert run(TTLCache, **ex) == want == run(NaiveTTL, **ex)
print('example ->', run(TTLCache, **ex))

random.seed(12)
for case in range(600):
    cap = random.randint(1, 4); t = 0; ops = []
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 3)
        r = random.random()
        if r < 0.45: ops.append([t, 'put', [random.choice('abcde'), random.randint(0, 99), random.randint(1, 6)]])
        elif r < 0.9: ops.append([t, 'get', [random.choice('abcde')]])
        else: ops.append([t, 'size', []])
    assert run(TTLCache, [cap], ops) == run(NaiveTTL, [cap], ops), (cap, ops)
print('600 random timed sequences match the naive reference')

# why purge first: capacity 2, a expires at 5, b lives long. At t=5 put c.
seq = [[0, 'put', ['a', 1, 5]], [1, 'put', ['b', 2, 100]], [2, 'get', ['a']], [5, 'put', ['c', 3, 100]], [5, 'get', ['b']]]
good = run(TTLCache, [2], seq); bad = run(NoPurgeBug, [2], seq)
assert good[-1] == 2 and bad[-1] == -1
print('with purge b ->', good[-1], '| without purge b ->', bad[-1], '(a is dead but b, live, gets evicted)')

# boundary and get-does-not-extend-life
seq = [[0, 'put', ['k', 7, 4]], [3, 'get', ['k']], [3, 'size', []], [4, 'get', ['k']], [4, 'size', []]]
assert run(TTLCache, [1], seq) == [None, 7, 1, -1, 0]
seq = [[0, 'put', ['k', 7, 4]], [3, 'put', ['k', 8, 4]], [6, 'get', ['k']], [7, 'get', ['k']]]   # re-put restarts the life
assert run(TTLCache, [1], seq) == [None, None, 8, -1]
seq = [[0, 'put', ['a', 1, 9]], [0, 'put', ['b', 2, 9]], [0, 'get', ['a']], [0, 'put', ['c', 3, 9]], [0, 'get', ['b']], [0, 'get', ['a']]]
assert run(TTLCache, [2], seq) == [None, None, 1, None, -1, 1]       # capacity 2: get(a) saved a, b was LRU
assert run(TTLCache, [1], []) == []
print('edge asserts ok')
