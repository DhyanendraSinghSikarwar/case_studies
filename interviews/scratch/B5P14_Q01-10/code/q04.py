import random, time
from collections import OrderedDict

class LRUCache:                        # optimal: OrderedDict, most recent at the END
    def __init__(self, capacity):
        self.cap = capacity; self.d = OrderedDict()
    def get(self, key):
        if key not in self.d: return -1         # a miss changes nothing
        self.d.move_to_end(key)                 # O(1): a hit makes it most recent
        return self.d[key]
    def put(self, key, value):
        if key in self.d: self.d.move_to_end(key)   # update also refreshes recency
        self.d[key] = value
        if len(self.d) > self.cap:
            self.d.popitem(last=False)          # evict the least recent (front)

class NaiveLRU:                        # brute force: plain dict + a list of keys, O(n) remove
    def __init__(self, capacity): self.cap = capacity; self.val = {}; self.order = []   # oldest first
    def get(self, key):
        if key not in self.val: return -1
        self.order.remove(key); self.order.append(key); return self.val[key]
    def put(self, key, value):
        if key in self.val: self.order.remove(key)
        elif len(self.val) == self.cap:
            old = self.order.pop(0); del self.val[old]
        self.val[key] = value; self.order.append(key)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([2], [['put',[1,1]],['put',[2,2]],['get',[1]],['put',[3,3]],['get',[2]],['put',[4,4]],['get',[1]],['get',[3]],['get',[4]]],
      [None,None,1,None,-1,None,-1,3,4])
e2 = ([1], [['put',[5,10]],['put',[5,20]],['get',[5]],['put',[6,1]],['get',[5]],['get',[6]]], [None,None,20,None,-1,1])
for init, ops, want in (e1, e2):
    assert run(LRUCache, init, ops) == want == run(NaiveLRU, init, ops)
print("examples:", run(LRUCache, *e1[:2]), run(LRUCache, *e2[:2]))

random.seed(14)
for _ in range(1000):
    cap = random.randint(1, 4)
    ops = [random.choice([['get', [random.randint(0, 5)]], ['put', [random.randint(0, 5), random.randint(0, 99)]]])
           for _ in range(random.randint(0, 50))]
    assert run(LRUCache, [cap], ops) == run(NaiveLRU, [cap], ops), (cap, ops)
print("1000 random operation sequences: OrderedDict == naive")

# edge cases
c = LRUCache(1); c.put(1, 1); c.put(1, 2); assert c.get(1) == 2 and len(c.d) == 1   # update at capacity does not evict
c.put(2, 3); assert c.get(1) == -1 and c.get(2) == 3
assert LRUCache(2).get(9) == -1                                                    # empty cache
c = LRUCache(2); c.put(1, 1); c.put(2, 2); c.get(9); c.put(3, 3)                  # failed get must not refresh
assert c.get(1) == -1 and c.get(2) == 2
c = LRUCache(3000)
for k in range(10**5): c.put(k, k)
assert len(c.d) == 3000 and list(c.d)[0] == 10**5 - 3000
print("edge asserts ok (capacity 1, update at capacity, failed get, 10^5 puts at capacity 3000)")

# Claim check: can a PLAIN dict do it? Yes by pop + re-insert, and next(iter(d)) finds the oldest key,
# but after many deletions at the front the dict keeps dead slots and next(iter(d)) scans them.
d = {k: k for k in range(200000)}
for k in range(199990): del d[k]
t = time.perf_counter()
for _ in range(200): next(iter(d))
slow = time.perf_counter() - t
d2 = {k: k for k in range(10)}
t = time.perf_counter()
for _ in range(200): next(iter(d2))
fast = time.perf_counter() - t
print("sandbox timing: dict with a dead front, oldest-key lookup more than 10x slower than fresh dict:", slow > 10 * fast)
