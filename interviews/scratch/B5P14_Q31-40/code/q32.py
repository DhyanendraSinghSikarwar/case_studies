import heapq
import random
from collections import OrderedDict, defaultdict

random.seed(3201)


class LFUCache:
    """O(1) average get/put. freq -> OrderedDict (oldest use first), plus a min_freq pointer."""

    def __init__(self, capacity):
        self.cap = capacity
        self.val = {}                               # key -> value
        self.freq = {}                              # key -> use count
        self.buckets = defaultdict(OrderedDict)     # count -> keys in recency order (LRU first)
        self.min_freq = 0

    def _touch(self, key):                          # one more use: move key from bucket f to f + 1
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:                  # the only way min_freq can move up
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None             # newest end of the new bucket

    def get(self, key):
        if key not in self.val:
            return -1
        self._touch(key)
        return self.val[key]

    def put(self, key, value):
        if self.cap == 0:
            return None
        if key in self.val:                         # existing key: replace, one use, refresh recency
            self.val[key] = value
            self._touch(key)
            return None
        if len(self.val) == self.cap:               # new key at capacity: evict (lowest count, then LRU)
            victim, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.val[victim]
            del self.freq[victim]
        self.val[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1                           # a new key always has the smallest count
        return None


class NaiveLFU:
    """Reference: every key keeps [value, uses, last-use stamp]; evict by scanning for min (uses, stamp)."""

    def __init__(self, capacity):
        self.cap, self.d, self.clock = capacity, {}, 0

    def get(self, key):
        if key not in self.d:
            return -1
        self.clock += 1
        e = self.d[key]
        e[1] += 1
        e[2] = self.clock
        return e[0]

    def put(self, key, value):
        if self.cap == 0:
            return None
        self.clock += 1
        if key in self.d:
            e = self.d[key]
            e[0], e[1], e[2] = value, e[1] + 1, self.clock
            return None
        if len(self.d) == self.cap:
            victim = min(self.d, key=lambda k: (self.d[k][1], self.d[k][2]))
            del self.d[victim]
        self.d[key] = [value, 1, self.clock]
        return None


class HeapLFU:
    """The O(log n) alternative: lazy heap of (uses, stamp, key). Shown only to count the cost."""

    def __init__(self, capacity):
        self.cap, self.d, self.h, self.clock = capacity, {}, [], 0   # d: key -> [value, uses, stamp]

    def _push(self, key):
        self.clock += 1
        e = self.d[key]
        e[2] = self.clock
        heapq.heappush(self.h, (e[1], e[2], key))   # O(log n) on EVERY get/put

    def get(self, key):
        if key not in self.d:
            return -1
        self.d[key][1] += 1
        self._push(key)
        return self.d[key][0]

    def put(self, key, value):
        if self.cap == 0:
            return None
        if key in self.d:
            self.d[key][0] = value
            self.d[key][1] += 1
            self._push(key)
            return None
        if len(self.d) == self.cap:
            while True:                             # skip stale entries
                u, s, k = heapq.heappop(self.h)
                if k in self.d and self.d[k][1] == u and self.d[k][2] == s:
                    del self.d[k]
                    break
        self.d[key] = [value, 1, 0]
        self._push(key)
        return None


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's examples ---
ops1 = [['put', [1, 1]], ['put', [2, 2]], ['get', [1]], ['put', [3, 3]], ['get', [2]],
        ['get', [3]], ['put', [4, 4]], ['get', [1]], ['get', [3]], ['get', [4]]]
r1 = run(LFUCache, [2], ops1)
print('example 1:', r1)
assert r1 == [None, None, 1, None, -1, 3, None, -1, 3, 4]
r2 = run(LFUCache, [0], [['put', [0, 0]], ['get', [0]]])
print('example 2:', r2)
assert r2 == [None, -1]

# --- random operation-sequence oracle (small key space forces many evictions and ties) ---
total = 0
for _ in range(800):
    cap = random.randint(0, 4)
    ops = []
    for _ in range(random.randint(1, 40)):
        k = random.randint(0, 5)
        ops.append(['get', [k]] if random.random() < 0.4 else ['put', [k, random.randint(0, 99)]])
    a, b, c = run(LFUCache, [cap], ops), run(NaiveLFU, [cap], ops), run(HeapLFU, [cap], ops)
    assert a == b == c, (cap, ops)
    total += len(ops)
print('random ops compared (3 implementations):', total)

# --- min_freq invariant: after every op it equals the true minimum count ---
for _ in range(300):
    c = LFUCache(3)
    for _ in range(40):
        k = random.randint(0, 6)
        c.get(k) if random.random() < 0.5 else c.put(k, 0)
        if c.freq:
            assert c.min_freq == min(c.freq.values())
            assert all(c.buckets[f] for f in c.buckets)   # no empty buckets are kept
print('min_freq invariant held')

# --- tie rule demo: equal counts -> evict the least recently used (gets count as use) ---
c = LFUCache(2)
c.put(1, 'a'); c.put(2, 'b')          # both count 1; key 1 is older
c.put(3, 'c')                         # evicts 1 (tie -> LRU)
print('after put 3, get 1 ->', c.get(1), '| get 2 ->', c.get(2))   # 2 now has count 2
c.put(4, 'd')                         # 3 has count 1, 2 has count 2 -> evict 3
print('after put 4, get 3 ->', c.get(3), '| get 2 ->', c.get(2), '| get 4 ->', c.get(4))

# --- edge cases ---
z = LFUCache(0); assert z.put(1, 1) is None and z.get(1) == -1
o = LFUCache(1); o.put(1, 1); o.put(1, 5); assert o.get(1) == 5      # update at capacity: no eviction
o.put(2, 2); assert o.get(1) == -1 and o.get(2) == 2                 # new key evicts the only key
h = LFUCache(2); h.put(1, 1); h.put(2, 2)
for _ in range(5): h.get(1)
h.put(3, 3); assert h.get(2) == -1 and h.get(1) == 1                 # hot key survives (count 6 vs 1)
big = LFUCache(10 ** 4)
for i in range(2 * 10 ** 4): big.put(i, i)
assert len(big.val) == 10 ** 4 and big.get(0) == -1 and big.get(2 * 10 ** 4 - 1) == 2 * 10 ** 4 - 1
print('edge asserts passed')
