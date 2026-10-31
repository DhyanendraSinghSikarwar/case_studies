# Reference solutions (S) and independent oracles (B) for Book 5 Part 14 (design problems, advanced graphs, segment/Fenwick trees, mock sets).
# Design questions: kwargs are init (constructor args after the optional clock) and ops ([method, [args]] or, for clocked designs, [time, method, [args]]).
import sys, heapq, bisect, itertools, collections, math, copy
from collections import OrderedDict, deque, defaultdict
sys.setrecursionlimit(1000)
S = {}; B = {}
DES = {}   # key -> (S class, B class, clocked, ctor adapter)

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

def run_design(cls, clocked, adapter, init, ops):
    init = copy.deepcopy(init)
    args = adapter(init) if adapter else init
    if clocked:
        clk = Clock(); obj = cls(clk, *args); out = []
        last = 0
        for t, m, a in ops:
            assert t >= last, 'time must not go backwards'; last = t
            clk.t = t; out.append(getattr(obj, m)(*copy.deepcopy(a)))
        return out
    obj = cls(*args)
    return [getattr(obj, m)(*copy.deepcopy(a)) for m, a in ops]

def design(key, Sc, Bc, clocked=False, adapter=None):
    DES[key] = (Sc, Bc, clocked, adapter)
    S[key] = lambda init, ops, _k=key: run_design(DES[_k][0], clocked, adapter, init, ops)
    B[key] = lambda init, ops, _k=key: run_design(DES[_k][1], clocked, adapter, init, ops)

def reg(d, name):
    def deco(f): d[name] = f; return f
    return deco

# ============================================================ LRU
class LRU_OD:
    def __init__(self, capacity): self.cap = capacity; self.d = OrderedDict()
    def get(self, key):
        if key not in self.d: return -1
        self.d.move_to_end(key); return self.d[key]
    def put(self, key, value):
        if key in self.d: self.d.move_to_end(key)
        self.d[key] = value
        if len(self.d) > self.cap: self.d.popitem(last=False)
    def order(self): return list(reversed(self.d))
    def size(self): return len(self.d)
class LRU_N:
    def __init__(self, capacity): self.cap = capacity; self.d = {}; self.o = []   # o: least recent first
    def get(self, key):
        if key not in self.d: return -1
        self.o.remove(key); self.o.append(key); return self.d[key]
    def put(self, key, value):
        if key in self.d: self.o.remove(key)
        elif len(self.d) == self.cap:
            old = self.o.pop(0); del self.d[old]
        self.d[key] = value; self.o.append(key)
    def order(self): return self.o[::-1]
    def size(self): return len(self.d)
class Node:
    __slots__ = ('key', 'val', 'prev', 'next')
    def __init__(self, key=0, val=0): self.key = key; self.val = val; self.prev = self.next = None
class LRU_DLL:
    def __init__(self, capacity):
        self.cap = capacity; self.map = {}
        self.head = Node(); self.tail = Node(); self.head.next = self.tail; self.tail.prev = self.head   # head side = most recent
    def _unlink(self, n): n.prev.next = n.next; n.next.prev = n.prev
    def _push_front(self, n):
        n.next = self.head.next; n.prev = self.head; self.head.next.prev = n; self.head.next = n
    def get(self, key):
        n = self.map.get(key)
        if n is None: return -1
        self._unlink(n); self._push_front(n); return n.val
    def put(self, key, value):
        n = self.map.get(key)
        if n is not None:
            n.val = value; self._unlink(n); self._push_front(n); return
        if len(self.map) == self.cap:
            lru = self.tail.prev; self._unlink(lru); del self.map[lru.key]
        n = Node(key, value); self.map[key] = n; self._push_front(n)
    def order(self):
        out = []; n = self.head.next
        while n is not self.tail: out.append(n.key); n = n.next
        return out
    def size(self): return len(self.map)
design('lru_ordereddict', LRU_OD, LRU_N)
design('lru_dll', LRU_DLL, LRU_N)

# ============================================================ LFU
class LFU_S:
    def __init__(self, capacity):
        self.cap = capacity; self.kv = {}; self.freq = {}; self.groups = defaultdict(OrderedDict); self.minf = 0
    def _touch(self, key):
        f = self.freq[key]; del self.groups[f][key]
        if not self.groups[f]:
            del self.groups[f]
            if self.minf == f: self.minf = f + 1
        self.freq[key] = f + 1; self.groups[f + 1][key] = None
    def get(self, key):
        if key not in self.kv: return -1
        self._touch(key); return self.kv[key]
    def put(self, key, value):
        if self.cap == 0: return
        if key in self.kv: self.kv[key] = value; self._touch(key); return
        if len(self.kv) == self.cap:
            old, _ = self.groups[self.minf].popitem(last=False)
            if not self.groups[self.minf]: del self.groups[self.minf]
            del self.kv[old]; del self.freq[old]
        self.kv[key] = value; self.freq[key] = 1; self.groups[1][key] = None; self.minf = 1
class LFU_N:
    def __init__(self, capacity): self.cap = capacity; self.d = {}; self.clock = 0   # key -> [val, freq, stamp]
    def get(self, key):
        if key not in self.d: return -1
        self.clock += 1; e = self.d[key]; e[1] += 1; e[2] = self.clock; return e[0]
    def put(self, key, value):
        if self.cap == 0: return
        self.clock += 1
        if key in self.d: e = self.d[key]; e[0] = value; e[1] += 1; e[2] = self.clock; return
        if len(self.d) == self.cap:
            victim = min(self.d, key=lambda k: (self.d[k][1], self.d[k][2])); del self.d[victim]
        self.d[key] = [value, 1, self.clock]
design('lfu', LFU_S, LFU_N)

# ============================================================ time-based KV, snapshot array
class TimeMap_S:
    def __init__(self): self.d = {}
    def set(self, key, value, timestamp):
        t, v = self.d.setdefault(key, ([], [])); t.append(timestamp); v.append(value)
    def get(self, key, timestamp):
        if key not in self.d: return ''
        t, v = self.d[key]; i = bisect.bisect_right(t, timestamp)
        return v[i - 1] if i else ''
class TimeMap_N:
    def __init__(self): self.rows = []
    def set(self, key, value, timestamp): self.rows.append((key, value, timestamp))
    def get(self, key, timestamp):
        best = None
        for k, v, t in self.rows:
            if k == key and t <= timestamp and (best is None or t >= best[0]): best = (t, v)
        return best[1] if best else ''
design('time_kv', TimeMap_S, TimeMap_N)

class Snap_S:
    def __init__(self, length): self.h = [[(0, 0)] for _ in range(length)]; self.sid = 0
    def set(self, index, val):
        row = self.h[index]
        if row[-1][0] == self.sid: row[-1] = (self.sid, val)
        else: row.append((self.sid, val))
    def snap(self): self.sid += 1; return self.sid - 1
    def get(self, index, snap_id):
        row = self.h[index]; i = bisect.bisect_right(row, (snap_id, float('inf'))) - 1
        return row[i][1]
class Snap_N:
    def __init__(self, length): self.cur = [0] * length; self.snaps = []
    def set(self, index, val): self.cur[index] = val
    def snap(self): self.snaps.append(list(self.cur)); return len(self.snaps) - 1
    def get(self, index, snap_id): return self.snaps[snap_id][index]
design('snapshot', Snap_S, Snap_N)

# ============================================================ rate limiters and counters (clocked)
class Sliding_S:
    def __init__(self, clock, limit, window): self.c = clock; self.limit = limit; self.w = window; self.d = {}
    def allow(self, user):
        now = self.c(); q = self.d.setdefault(user, deque())
        while q and q[0] <= now - self.w: q.popleft()
        if len(q) < self.limit: q.append(now); return True
        return False
class Sliding_N:
    def __init__(self, clock, limit, window): self.c = clock; self.limit = limit; self.w = window; self.acc = []
    def allow(self, user):
        now = self.c()
        n = sum(1 for u, t in self.acc if u == user and now - self.w < t <= now)
        if n < self.limit: self.acc.append((user, now)); return True
        return False
design('sliding_log', Sliding_S, Sliding_N, True)

class Fixed_S:
    def __init__(self, clock, limit, window): self.c = clock; self.limit = limit; self.w = window; self.d = {}
    def allow(self, user):
        w = self.c() // self.w; st = self.d.get(user)
        if st is None or st[0] != w: st = [w, 0]; self.d[user] = st
        if st[1] < self.limit: st[1] += 1; return True
        return False
class Fixed_N:
    def __init__(self, clock, limit, window): self.c = clock; self.limit = limit; self.w = window; self.acc = []
    def allow(self, user):
        now = self.c()
        n = sum(1 for u, t in self.acc if u == user and t // self.w == now // self.w)
        if n < self.limit: self.acc.append((user, now)); return True
        return False
design('fixed_window', Fixed_S, Fixed_N, True)

class Bucket_S:
    def __init__(self, clock, capacity, rate):
        self.c = clock; self.cap = capacity; self.rate = rate; self.tokens = capacity; self.last = clock()
    def allow(self, cost=1):
        now = self.c(); self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate); self.last = now
        if cost <= self.tokens: self.tokens -= cost; return True
        return False
class Bucket_N:
    def __init__(self, clock, capacity, rate):
        self.c = clock; self.cap = capacity; self.rate = rate; self.tokens = capacity; self.last = clock()
    def allow(self, cost=1):
        now = self.c()
        while self.last < now:    # one whole second at a time
            self.tokens = min(self.cap, self.tokens + self.rate); self.last += 1
        if cost <= self.tokens: self.tokens -= cost; return True
        return False
design('token_bucket', Bucket_S, Bucket_N, True)

class Hit_S:
    def __init__(self, clock): self.c = clock; self.q = deque(); self.total = 0
    def hit(self):
        now = self.c()
        if self.q and self.q[-1][0] == now: self.q[-1][1] += 1
        else: self.q.append([now, 1])
        self.total += 1
    def getHits(self):
        now = self.c()
        while self.q and self.q[0][0] <= now - 300: self.total -= self.q.popleft()[1]
        return self.total
class Hit_N:
    def __init__(self, clock): self.c = clock; self.ts = []
    def hit(self): self.ts.append(self.c())
    def getHits(self): now = self.c(); return sum(1 for t in self.ts if now - 300 < t <= now)
design('hit_counter', Hit_S, Hit_N, True)

class Logger_S:
    def __init__(self, clock): self.c = clock; self.last = {}
    def shouldPrint(self, message):
        now = self.c()
        if message not in self.last or now - self.last[message] >= 10: self.last[message] = now; return True
        return False
class Logger_N:
    def __init__(self, clock): self.c = clock; self.printed = []
    def shouldPrint(self, message):
        now = self.c()
        if any(m == message and now - t < 10 for t, m in self.printed): return False
        self.printed.append((now, message)); return True
design('logger', Logger_S, Logger_N, True)

# ============================================================ iterators
class Nested_S:
    def __init__(self, nested): self.st = [iter(nested)]; self.nxt = None; self._adv()
    def _adv(self):
        self.nxt = None
        while self.st:
            try: x = next(self.st[-1])
            except StopIteration: self.st.pop(); continue
            if isinstance(x, int): self.nxt = (x,); return
            self.st.append(iter(x))
    def next(self): v = self.nxt[0]; self._adv(); return v
    def hasNext(self): return self.nxt is not None
class Nested_N:
    def __init__(self, nested):
        self.flat = []
        def go(x):
            for y in x:
                if isinstance(y, int): self.flat.append(y)
                else: go(y)
        go(nested); self.i = 0
    def next(self): self.i += 1; return self.flat[self.i - 1]
    def hasNext(self): return self.i < len(self.flat)
design('flatten_iter', Nested_S, Nested_N)

class Peek_S:
    def __init__(self, it): self.it = it; self.buf = []; self._fill()
    def _fill(self):
        try: self.buf = [next(self.it)]
        except StopIteration: self.buf = []
    def peek(self): return self.buf[0]
    def next(self): v = self.buf[0]; self._fill(); return v
    def hasNext(self): return bool(self.buf)
class Peek_N:
    def __init__(self, it): self.a = list(it); self.i = 0
    def peek(self): return self.a[self.i]
    def next(self): self.i += 1; return self.a[self.i - 1]
    def hasNext(self): return self.i < len(self.a)
design('peeking', Peek_S, Peek_N, False, lambda init: [iter(init[0])])

class Zig_S:
    def __init__(self, lists): self.q = deque((l, 0) for l in lists if l)
    def next(self):
        l, i = self.q.popleft(); v = l[i]
        if i + 1 < len(l): self.q.append((l, i + 1))
        return v
    def hasNext(self): return bool(self.q)
class Zig_N:
    def __init__(self, lists):
        self.a = [l[r] for r in range(max((len(l) for l in lists), default=0)) for l in lists if r < len(l)]; self.i = 0
    def next(self): self.i += 1; return self.a[self.i - 1]
    def hasNext(self): return self.i < len(self.a)
design('zigzag', Zig_S, Zig_N)

# ============================================================ Twitter, all-O(1)
class Tw_S:
    def __init__(self, feed_size): self.n = feed_size; self.cnt = 0; self.tw = defaultdict(list); self.fol = defaultdict(set)
    def postTweet(self, user, tweet_id): self.cnt += 1; self.tw[user].append((self.cnt, tweet_id))
    def follow(self, a, b):
        if a != b: self.fol[a].add(b)
    def unfollow(self, a, b): self.fol[a].discard(b)
    def getNewsFeed(self, user):
        srcs = [reversed(self.tw[u]) for u in self.fol[user] | {user} if self.tw[u]]
        return [t for _, t in itertools.islice(heapq.merge(*srcs, key=lambda x: -x[0]), self.n)]
class Tw_N:
    def __init__(self, feed_size): self.n = feed_size; self.posts = []; self.edges = set()
    def postTweet(self, user, tweet_id): self.posts.append((user, tweet_id))
    def follow(self, a, b):
        if a != b: self.edges.add((a, b))
    def unfollow(self, a, b): self.edges.discard((a, b))
    def getNewsFeed(self, user):
        vis = [t for u, t in reversed(self.posts) if u == user or (user, u) in self.edges]
        return vis[:self.n]
design('twitter', Tw_S, Tw_N)

class Bk:
    __slots__ = ('cnt', 'keys', 'prev', 'next')
    def __init__(self, cnt): self.cnt = cnt; self.keys = OrderedDict(); self.prev = self.next = None
class AllOne_S:
    def __init__(self):
        self.head = Bk(0); self.tail = Bk(0); self.head.next = self.tail; self.tail.prev = self.head; self.where = {}
    def _after(self, node, cnt):
        b = Bk(cnt); b.prev = node; b.next = node.next; node.next.prev = b; node.next = b; return b
    def _drop(self, b):
        if not b.keys: b.prev.next = b.next; b.next.prev = b.prev
    def inc(self, key):
        b = self.where.get(key)
        if b is None:
            nb = self.head.next if self.head.next.cnt == 1 else self._after(self.head, 1)
        else:
            nb = b.next if b.next is not self.tail and b.next.cnt == b.cnt + 1 else self._after(b, b.cnt + 1)
            del b.keys[key]; self._drop(b)
        nb.keys[key] = None; self.where[key] = nb
    def dec(self, key):
        b = self.where.get(key)
        if b is None: return
        del b.keys[key]
        if b.cnt == 1: del self.where[key]
        else:
            pb = b.prev if b.prev is not self.head and b.prev.cnt == b.cnt - 1 else self._after(b.prev, b.cnt - 1)
            pb.keys[key] = None; self.where[key] = pb
        self._drop(b)
    def getMaxKey(self): return next(iter(self.tail.prev.keys)) if self.where else ''
    def getMinKey(self): return next(iter(self.head.next.keys)) if self.where else ''
class AllOne_N:
    def __init__(self): self.c = {}; self.st = {}; self.t = 0
    def inc(self, key): self.t += 1; self.c[key] = self.c.get(key, 0) + 1; self.st[key] = self.t
    def dec(self, key):
        if key not in self.c: return
        self.t += 1; self.c[key] -= 1; self.st[key] = self.t
        if self.c[key] == 0: del self.c[key]; del self.st[key]
    def getMaxKey(self):
        if not self.c: return ''
        m = max(self.c.values()); return min((self.st[k], k) for k in self.c if self.c[k] == m)[1]
    def getMinKey(self):
        if not self.c: return ''
        m = min(self.c.values()); return min((self.st[k], k) for k in self.c if self.c[k] == m)[1]
design('all_o1', AllOne_S, AllOne_N)

# ============================================================ Fenwick, segment trees, sparse table
class BIT_S:
    def __init__(self, nums):
        self.n = len(nums); self.a = list(nums); self.t = [0] * (self.n + 1)
        for i, v in enumerate(nums, 1):          # O(n) build
            self.t[i] += v; j = i + (i & -i)
            if j <= self.n: self.t[j] += self.t[i]
    def update(self, i, val):
        d = val - self.a[i]; self.a[i] = val; i += 1
        while i <= self.n: self.t[i] += d; i += i & -i
    def _pre(self, i):
        s = 0
        while i > 0: s += self.t[i]; i -= i & -i
        return s
    def sumRange(self, l, r): return self._pre(r + 1) - self._pre(l)
class Arr_N:
    def __init__(self, nums): self.a = list(nums)
    def update(self, i, val): self.a[i] = val
    def sumRange(self, l, r): return sum(self.a[l:r + 1])
design('bit_point_range', BIT_S, Arr_N)

class MinSeg_S:
    def __init__(self, nums):
        self.n = len(nums); self.t = [0] * self.n + list(nums)
        for i in range(self.n - 1, 0, -1): self.t[i] = min(self.t[2 * i], self.t[2 * i + 1])
    def update(self, i, v):
        i += self.n; self.t[i] = v
        while i > 1: i >>= 1; self.t[i] = min(self.t[2 * i], self.t[2 * i + 1])
    def query(self, l, r):
        res = float('inf'); l += self.n; r += self.n + 1
        while l < r:
            if l & 1: res = min(res, self.t[l]); l += 1
            if r & 1: r -= 1; res = min(res, self.t[r])
            l >>= 1; r >>= 1
        return res
class ArrMin_N:
    def __init__(self, nums): self.a = list(nums)
    def update(self, i, v): self.a[i] = v
    def query(self, l, r): return min(self.a[l:r + 1])
design('segtree_min', MinSeg_S, ArrMin_N)

class Lazy_S:
    def __init__(self, nums):
        self.n = len(nums); self.sm = [0] * (4 * self.n); self.lz = [0] * (4 * self.n); self._build(1, 0, self.n - 1, nums)
    def _build(self, o, l, r, a):
        if l == r: self.sm[o] = a[l]; return
        m = (l + r) // 2; self._build(2 * o, l, m, a); self._build(2 * o + 1, m + 1, r, a); self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]
    def _apply(self, o, l, r, v): self.sm[o] += v * (r - l + 1); self.lz[o] += v
    def _push(self, o, l, r):
        if self.lz[o]:
            m = (l + r) // 2; self._apply(2 * o, l, m, self.lz[o]); self._apply(2 * o + 1, m + 1, r, self.lz[o]); self.lz[o] = 0
    def _add(self, o, l, r, ql, qr, v):
        if qr < l or r < ql: return
        if ql <= l and r <= qr: self._apply(o, l, r, v); return
        self._push(o, l, r); m = (l + r) // 2
        self._add(2 * o, l, m, ql, qr, v); self._add(2 * o + 1, m + 1, r, ql, qr, v); self.sm[o] = self.sm[2 * o] + self.sm[2 * o + 1]
    def _sum(self, o, l, r, ql, qr):
        if qr < l or r < ql: return 0
        if ql <= l and r <= qr: return self.sm[o]
        self._push(o, l, r); m = (l + r) // 2
        return self._sum(2 * o, l, m, ql, qr) + self._sum(2 * o + 1, m + 1, r, ql, qr)
    def add(self, l, r, v): self._add(1, 0, self.n - 1, l, r, v)
    def sum(self, l, r): return self._sum(1, 0, self.n - 1, l, r)
class LazyArr_N:
    def __init__(self, nums): self.a = list(nums)
    def add(self, l, r, v):
        for i in range(l, r + 1): self.a[i] += v
    def sum(self, l, r): return sum(self.a[l:r + 1])
design('lazy_range', Lazy_S, LazyArr_N)

class BIT2_S:
    def __init__(self, matrix):
        self.m = len(matrix); self.n = len(matrix[0]); self.a = [[0] * self.n for _ in range(self.m)]
        self.t = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        for i in range(self.m):
            for j in range(self.n): self.update(i, j, matrix[i][j])
    def update(self, r, c, v):
        d = v - self.a[r][c]; self.a[r][c] = v; i = r + 1
        while i <= self.m:
            j = c + 1
            while j <= self.n: self.t[i][j] += d; j += j & -j
            i += i & -i
    def _pre(self, r, c):
        s = 0; i = r
        while i > 0:
            j = c
            while j > 0: s += self.t[i][j]; j -= j & -j
            i -= i & -i
        return s
    def sumRegion(self, r1, c1, r2, c2): return self._pre(r2 + 1, c2 + 1) - self._pre(r1, c2 + 1) - self._pre(r2 + 1, c1) + self._pre(r1, c1)
class Mat_N:
    def __init__(self, matrix): self.a = [list(r) for r in matrix]
    def update(self, r, c, v): self.a[r][c] = v
    def sumRegion(self, r1, c1, r2, c2): return sum(self.a[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
design('bit_2d', BIT2_S, Mat_N)

@reg(S, 'sparse_table')
def _(nums, queries):
    n = len(nums); T = [[(v, i) for i, v in enumerate(nums)]]; j = 1; entries = n
    while (1 << j) <= n:
        p = T[-1]; h = 1 << (j - 1)
        T.append([min(p[i], p[i + h]) for i in range(n - (1 << j) + 1)]); entries += len(T[-1]); j += 1
    out = []
    for l, r in queries:
        k = (r - l + 1).bit_length() - 1
        v, i = min(T[k][l], T[k][r - (1 << k) + 1]); out.append([v, i])
    return [out, entries]
@reg(B, 'sparse_table')
def _(nums, queries):
    n = len(nums); entries = sum(n - (1 << j) + 1 for j in range(n.bit_length()) if (1 << j) <= n)
    out = []
    for l, r in queries:
        m = min(nums[l:r + 1]); out.append([m, nums.index(m, l, r + 1)])
    return [out, entries]

@reg(S, 'coord_compress')
def _(values):
    uniq = sorted(set(values)); rank = {v: i + 1 for i, v in enumerate(uniq)}
    return [[rank[v] for v in values], len(uniq)]
@reg(B, 'coord_compress')
def _(values):
    out = []
    for v in values: out.append(1 + len({w for w in values if w < v}))
    return [out, len(set(values))]

def _bit_add(t, i, d):
    while i < len(t): t[i] += d; i += i & -i
def _bit_pre(t, i):
    s = 0
    while i > 0: s += t[i]; i -= i & -i
    return s

@reg(S, 'inversions_bit')
def _(nums):
    uniq = sorted(set(nums)); rk = {v: i + 1 for i, v in enumerate(uniq)}; t = [0] * (len(uniq) + 1); res = []
    for i, v in enumerate(nums):
        res.append(i - _bit_pre(t, rk[v])); _bit_add(t, rk[v], 1)
    return [sum(res), res]
@reg(B, 'inversions_bit')
def _(nums):
    res = [sum(1 for j in range(i) if nums[j] > nums[i]) for i in range(len(nums))]
    return [sum(res), res]

@reg(S, 'count_smaller')
def _(nums):
    uniq = sorted(set(nums)); rk = {v: i + 1 for i, v in enumerate(uniq)}; t = [0] * (len(uniq) + 1); res = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        res[i] = _bit_pre(t, rk[nums[i]] - 1); _bit_add(t, rk[nums[i]], 1)
    return res
@reg(B, 'count_smaller')
def _(nums): return [sum(1 for j in range(i + 1, len(nums)) if nums[j] < nums[i]) for i in range(len(nums))]

# ============================================================ graphs
def _adj(n, edges, directed=True):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        if not directed: g[v].append(u)
    return g

@reg(S, 'scc_kosaraju')
def _(n, edges):
    g = _adj(n, edges); rg = _adj(n, [(v, u) for u, v in edges]); seen = [False] * n; order = []
    for s in range(n):
        if seen[s]: continue
        seen[s] = True; st = [(s, 0)]
        while st:
            u, i = st.pop()
            if i < len(g[u]):
                st.append((u, i + 1)); v = g[u][i]
                if not seen[v]: seen[v] = True; st.append((v, 0))
            else: order.append(u)
    comp = [-1] * n; comps = []
    for s in reversed(order):
        if comp[s] != -1: continue
        comp[s] = len(comps); cur = [s]; st = [s]
        while st:
            u = st.pop()
            for v in rg[u]:
                if comp[v] == -1: comp[v] = len(comps); cur.append(v); st.append(v)
        comps.append(sorted(cur))
    return sorted(comps)
@reg(B, 'scc_kosaraju')
def _(n, edges):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for u, v in edges: reach[u][v] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]: reach[i][j] = True
    comps = {tuple(v for v in range(n) if reach[u][v] and reach[v][u]) for u in range(n)}
    return sorted(list(c) for c in comps)

@reg(S, 'scc_tarjan')
def _(n, edges):
    g = _adj(n, edges); idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n; stack = []; cnt = 0; nc = 0
    for s in range(n):
        if idx[s] != -1: continue
        idx[s] = low[s] = cnt; cnt += 1; stack.append(s); on[s] = True; work = [(s, 0)]
        while work:
            u, i = work.pop()
            if i < len(g[u]):
                work.append((u, i + 1)); v = g[u][i]
                if idx[v] == -1:
                    idx[v] = low[v] = cnt; cnt += 1; stack.append(v); on[v] = True; work.append((v, 0))
                elif on[v]: low[u] = min(low[u], idx[v])
            else:
                if low[u] == idx[u]:
                    while True:
                        w = stack.pop(); on[w] = False; comp[w] = nc
                        if w == u: break
                    nc += 1
                if work: p = work[-1][0]; low[p] = min(low[p], low[u])
    cond = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, nc, cond]
@reg(B, 'scc_tarjan')
def _(n, edges):
    g = _adj(n, edges); idx = [-1] * n; low = [0] * n; on = [False] * n; comp = [-1] * n; stack = []; box = [0, 0]
    def dfs(u):
        idx[u] = low[u] = box[0]; box[0] += 1; stack.append(u); on[u] = True
        for v in g[u]:
            if idx[v] == -1: dfs(v); low[u] = min(low[u], low[v])
            elif on[v]: low[u] = min(low[u], idx[v])
        if low[u] == idx[u]:
            while True:
                w = stack.pop(); on[w] = False; comp[w] = box[1]
                if w == u: break
            box[1] += 1
    for s in range(n):
        if idx[s] == -1: dfs(s)
    cond = len({(comp[u], comp[v]) for u, v in edges if comp[u] != comp[v]})
    return [comp, box[1], cond]

def _components(n, edges, skip_edge=-1, skip_node=-1):
    p = list(range(n))
    def f(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for i, (u, v) in enumerate(edges):
        if i == skip_edge or u == skip_node or v == skip_node: continue
        p[f(u)] = f(v)
    return len({f(x) for x in range(n) if x != skip_node})

def _lowlink(n, edges):
    g = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v: g[u].append((v, i)); g[v].append((u, i))
    disc = [-1] * n; low = [0] * n; t = 0; bridges = set(); arts = set()
    for s in range(n):
        if disc[s] != -1: continue
        disc[s] = low[s] = t; t += 1; kids = 0; st = [(s, -1, 0)]
        while st:
            u, pe, i = st.pop()
            if i < len(g[u]):
                st.append((u, pe, i + 1)); v, e = g[u][i]
                if e == pe: continue
                if disc[v] == -1:
                    disc[v] = low[v] = t; t += 1; st.append((v, e, 0))
                else: low[u] = min(low[u], disc[v])
            else:
                if st:
                    p = st[-1][0]; low[p] = min(low[p], low[u])
                    if low[u] > disc[p]: bridges.add((min(u, p), max(u, p)))
                    if p == s: kids += 1
                    elif low[u] >= disc[p]: arts.add(p)
        if kids >= 2: arts.add(s)
    return sorted(list(b) for b in bridges), sorted(arts)

@reg(S, 'bridges')
def _(n, edges): return _lowlink(n, edges)[0]
@reg(B, 'bridges')
def _(n, edges):
    base = _components(n, edges); out = set()
    for i, (u, v) in enumerate(edges):
        if u != v and _components(n, edges, skip_edge=i) > base: out.add((min(u, v), max(u, v)))
    return sorted(list(b) for b in out)
@reg(S, 'articulation')
def _(n, edges): return _lowlink(n, edges)[1]
@reg(B, 'articulation')
def _(n, edges):
    base = _components(n, edges); out = []
    for v in range(n):
        alone = all(a == b == v or v not in (a, b) for a, b in edges)   # v has no edge to another node
        if _components(n, edges, skip_node=v) > base - (1 if alone else 0): out.append(v)
    return out

@reg(S, 'itinerary')
def _(tickets):
    g = defaultdict(list)
    for a, b in tickets: g[a].append(b)
    for a in g: g[a].sort(reverse=True)
    out = []; st = ['JFK']
    while st:
        while g[st[-1]]: st.append(g[st[-1]].pop())
        out.append(st.pop())
    return out[::-1]
@reg(B, 'itinerary')
def _(tickets):
    m = len(tickets); used = [False] * m
    def dfs(path):
        if len(path) == m + 1: return list(path)
        for dest in sorted({t[1] for i, t in enumerate(tickets) if not used[i] and t[0] == path[-1]}):
            i = next(i for i, t in enumerate(tickets) if not used[i] and t == [path[-1], dest]); used[i] = True; path.append(dest)
            r = dfs(path)
            path.pop(); used[i] = False
            if r: return r
        return None
    return dfs(['JFK'])

@reg(S, 'topo_lex')
def _(n, edges):
    g = _adj(n, edges); indeg = [0] * n
    for u, v in edges: indeg[v] += 1
    h = [v for v in range(n) if indeg[v] == 0]; heapq.heapify(h); out = []
    while h:
        u = heapq.heappop(h); out.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(h, v)
    return out if len(out) == n else []
@reg(B, 'topo_lex')
def _(n, edges):
    for p in itertools.permutations(range(n)):
        pos = {v: i for i, v in enumerate(p)}
        if all(pos[u] < pos[v] for u, v in edges): return list(p)
    return []

@reg(S, 'parallel_time')
def _(n, relations, time):
    g = [[] for _ in range(n + 1)]; indeg = [0] * (n + 1)
    for a, b in relations: g[a].append(b); indeg[b] += 1
    fin = [0] * (n + 1); q = deque(v for v in range(1, n + 1) if indeg[v] == 0); start = [0] * (n + 1); seen = 0
    while q:
        u = q.popleft(); seen += 1; fin[u] = start[u] + time[u - 1]
        for v in g[u]:
            start[v] = max(start[v], fin[u]); indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return [max(fin[1:]), fin[1:]] if seen == n else [-1, []]
@reg(B, 'parallel_time')
def _(n, relations, time):
    pre = defaultdict(list)
    for a, b in relations: pre[b].append(a)
    memo = {}; state = {}
    class Cyc(Exception): pass
    def f(v):
        if v in memo: return memo[v]
        if state.get(v) == 1: raise Cyc
        state[v] = 1; r = time[v - 1] + max((f(p) for p in pre[v]), default=0); state[v] = 2; memo[v] = r; return r
    try: fin = [f(v) for v in range(1, n + 1)]
    except Cyc: return [-1, []]
    return [max(fin), fin]

@reg(S, 'sp_coupon')
def _(n, edges):
    g = [[] for _ in range(n)]
    for u, v, w in edges: g[u].append((v, w))
    INF = float('inf'); dist = [[INF, INF] for _ in range(n)]; dist[0][0] = 0; h = [(0, 0, 0)]
    while h:
        d, u, k = heapq.heappop(h)
        if d > dist[u][k]: continue
        for v, w in g[u]:
            for nk, c in ((k, w), (1, w // 2) if k == 0 else (None, 0)):
                if nk is None: continue
                if d + c < dist[v][nk]: dist[v][nk] = d + c; heapq.heappush(h, (d + c, v, nk))
    r = min(dist[n - 1]); return -1 if r == INF else r
@reg(B, 'sp_coupon')
def _(n, edges):
    best = [float('inf')]
    def dfs(u, seen, cost, save):
        if u == n - 1: best[0] = min(best[0], cost - save); return
        for a, b, w in edges:
            if a == u and b not in seen:
                seen.add(b); dfs(b, seen, cost + w, max(save, w - w // 2)); seen.discard(b)
    dfs(0, {0}, 0, 0)
    return -1 if best[0] == float('inf') else best[0]

@reg(S, 'bipartite_matching')
def _(L, R, edges):
    g = [[] for _ in range(L)]
    for u, v in edges: g[u].append(v)
    mr = [-1] * R
    def try_(u, seen):
        for v in g[u]:
            if v in seen: continue
            seen.add(v)
            if mr[v] == -1 or try_(mr[v], seen): mr[v] = u; return True
        return False
    size = sum(1 for u in range(L) if try_(u, set()))
    return [size, size == L]
@reg(B, 'bipartite_matching')
def _(L, R, edges):
    g = [set() for _ in range(L)]
    for u, v in edges: g[u].add(v)
    @__import__('functools').lru_cache(None)
    def f(i, mask):
        if i == L: return 0
        best = f(i + 1, mask)
        for v in g[i]:
            if not mask >> v & 1: best = max(best, 1 + f(i + 1, mask | 1 << v))
        return best
    s = f(0, 0); return [s, s == L]

# ============================================================ set questions
class MovAvg_S:
    def __init__(self, size): self.size = size; self.q = deque(); self.t = 0
    def next(self, val):
        self.q.append(val); self.t += val
        if len(self.q) > self.size: self.t -= self.q.popleft()
        return self.t / len(self.q)
class MovAvg_N:
    def __init__(self, size): self.size = size; self.a = []
    def next(self, val): self.a.append(val); w = self.a[-self.size:]; return sum(w) / len(w)
design('moving_avg', MovAvg_S, MovAvg_N)

class Metro_S:
    def __init__(self): self.open = {}; self.stat = {}
    def checkIn(self, id, station, t): self.open[id] = (station, t)
    def checkOut(self, id, station, t):
        s, t0 = self.open.pop(id); a = self.stat.setdefault((s, station), [0, 0]); a[0] += t - t0; a[1] += 1
    def getAverageTime(self, start, end): a = self.stat[(start, end)]; return a[0] / a[1]
class Metro_N:
    def __init__(self): self.open = {}; self.trips = []
    def checkIn(self, id, station, t): self.open[id] = (station, t)
    def checkOut(self, id, station, t): s, t0 = self.open.pop(id); self.trips.append((s, station, t - t0))
    def getAverageTime(self, start, end):
        d = [x for a, b, x in self.trips if a == start and b == end]; return sum(d) / len(d)
design('underground', Metro_S, Metro_N)

class Board_S:
    def __init__(self): self.s = {}
    def addScore(self, player, score): self.s[player] = self.s.get(player, 0) + score
    def top(self, K): return sum(heapq.nlargest(K, self.s.values()))
    def reset(self, player): self.s.pop(player, None)
class Board_N:
    def __init__(self): self.rows = []
    def addScore(self, player, score): self.rows.append((player, score))
    def reset(self, player): self.rows = [(p, s) for p, s in self.rows if p != player]
    def top(self, K):
        tot = {}
        for p, s in self.rows: tot[p] = tot.get(p, 0) + s
        return sum(sorted(tot.values(), reverse=True)[:K])
design('leaderboard', Board_S, Board_N)

class TTL_S:
    def __init__(self, clock, capacity): self.c = clock; self.cap = capacity; self.od = OrderedDict(); self.h = []; self.ver = {}; self.n = 0
    def _purge(self):
        now = self.c()
        while self.h and self.h[0][0] <= now:
            e, k, v = heapq.heappop(self.h)
            if k in self.od and self.ver[k] == v: del self.od[k]
    def put(self, key, value, ttl):
        self._purge(); now = self.c()
        if key in self.od: del self.od[key]
        elif len(self.od) >= self.cap: self.od.popitem(last=False)
        self.n += 1; self.ver[key] = self.n; self.od[key] = value; heapq.heappush(self.h, (now + ttl, key, self.n))
    def get(self, key):
        self._purge()
        if key not in self.od: return -1
        self.od.move_to_end(key); return self.od[key]
    def size(self): self._purge(); return len(self.od)
class TTL_N:
    def __init__(self, clock, capacity): self.c = clock; self.cap = capacity; self.items = []   # [key, value, expiry], least recent first
    def _live(self): now = self.c(); self.items = [e for e in self.items if e[2] > now]
    def put(self, key, value, ttl):
        self._live(); now = self.c()
        self.items = [e for e in self.items if e[0] != key] if any(e[0] == key for e in self.items) else (self.items[1:] if len(self.items) >= self.cap else self.items)
        self.items.append([key, value, now + ttl])
    def get(self, key):
        self._live()
        for i, e in enumerate(self.items):
            if e[0] == key: self.items.append(self.items.pop(i)); return e[1]
        return -1
    def size(self): self._live(); return len(self.items)
design('lru_ttl', TTL_S, TTL_N, True)

class Sched_S:
    def __init__(self, clock): self.c = clock; self.h = []; self.pending = {}; self.seq = 0
    def submit(self, job_id, delay, priority):
        self.seq += 1; self.pending[job_id] = self.seq; heapq.heappush(self.h, (self.c() + delay, priority, self.seq, job_id))
    def cancel(self, job_id): return self.pending.pop(job_id, None) is not None
    def poll(self, limit):
        now = self.c(); out = []
        while self.h and len(out) < limit and self.h[0][0] <= now:
            r, p, s, j = heapq.heappop(self.h)
            if self.pending.get(j) == s: out.append(j); del self.pending[j]
        return out
class Sched_N:
    def __init__(self, clock): self.c = clock; self.jobs = []; self.seq = 0   # (ready, prio, seq, id)
    def submit(self, job_id, delay, priority): self.seq += 1; self.jobs.append((self.c() + delay, priority, self.seq, job_id))
    def cancel(self, job_id):
        n = len(self.jobs); self.jobs = [j for j in self.jobs if j[3] != job_id]; return len(self.jobs) < n
    def poll(self, limit):
        now = self.c(); ready = sorted(j for j in self.jobs if j[0] <= now)[:limit]
        for j in ready: self.jobs.remove(j)
        return [j[3] for j in ready]
design('scheduler', Sched_S, Sched_N, True)

@reg(S, 'valid_tree')
def _(n, edges):
    if len(edges) != n - 1: return False
    p = list(range(n))
    def f(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    for u, v in edges:
        a, b = f(u), f(v)
        if a == b: return False
        p[a] = b
    return True
@reg(B, 'valid_tree')
def _(n, edges):
    g = _adj(n, edges, False); seen = {0}; q = [0]
    for u in q:
        for v in g[u]:
            if v not in seen: seen.add(v); q.append(v)
    connected = len(seen) == n
    # acyclic: a connected graph with a cycle has more than n - 1 edges (parallel edges and self loops count)
    return connected and len(edges) == n - 1

@reg(S, 'reverse_delete')
def _(n, edges, removals):
    rem = set(removals); p = list(range(n)); comps = [n]
    def f(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    def union(u, v):
        a, b = f(u), f(v)
        if a == b: return 0
        p[a] = b; return 1
    c = n
    for i, (u, v) in enumerate(edges):
        if i not in rem: c -= union(u, v)
    res = [c]
    for i in reversed(removals): c -= union(*edges[i]); res.append(c)
    return res[::-1]
@reg(B, 'reverse_delete')
def _(n, edges, removals):
    out = [_components(n, edges)]; gone = set()
    for i in removals:
        gone.add(i); out.append(_components(n, [e for j, e in enumerate(edges) if j not in gone]))
    return out

@reg(S, 'connect_cities')
def _(n, edges, built):
    p = list(range(n))
    def f(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    comps = n
    for u, v in built:
        a, b = f(u), f(v)
        if a != b: p[a] = b; comps -= 1
    cost = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = f(u), f(v)
        if a != b: p[a] = b; comps -= 1; cost += w
    return cost if comps == 1 else -1
@reg(B, 'connect_cities')
def _(n, edges, built):
    best = None
    for mask in range(1 << len(edges)):
        chosen = [edges[i] for i in range(len(edges)) if mask >> i & 1]
        if _components(n, [(u, v) for u, v in built] + [(u, v) for u, v, w in chosen]) == 1:
            c = sum(w for u, v, w in chosen)
            if best is None or c < best: best = c
    return -1 if best is None else best

@reg(S, 'min_sources')
def _(n, edges):
    comps = S['scc_kosaraju'](n=n, edges=edges); cid = {}
    for i, c in enumerate(comps):
        for v in c: cid[v] = i
    has_in = {cid[v] for u, v in edges if cid[u] != cid[v]}
    return sorted(c[0] for i, c in enumerate(comps) if i not in has_in)
@reg(B, 'min_sources')
def _(n, edges):
    g = _adj(n, edges)
    def reach(src):
        seen = set(src); q = list(src)
        for u in q:
            for v in g[u]:
                if v not in seen: seen.add(v); q.append(v)
        return len(seen) == n
    for k in range(1, n + 1):
        for combo in itertools.combinations(range(n), k):
            if reach(combo): return list(combo)

def _is_rooted_tree(n, edges):
    indeg = [0] * (n + 1); g = [[] for _ in range(n + 1)]
    for u, v in edges: indeg[v] += 1; g[u].append(v)
    roots = [v for v in range(1, n + 1) if indeg[v] == 0]
    if len(roots) != 1 or any(indeg[v] > 1 for v in range(1, n + 1)): return False
    seen = {roots[0]}; q = [roots[0]]
    for u in q:
        for v in g[u]:
            if v not in seen: seen.add(v); q.append(v)
    return len(seen) == n
@reg(S, 'redundant_II')
def _(edges):
    n = len(edges); parent = [0] * (n + 1); c1 = c2 = None
    for u, v in edges:
        if parent[v]: c1 = [parent[v], v]; c2 = [u, v]
        else: parent[v] = u
    p = list(range(n + 1))
    def f(x):
        while p[x] != x: p[x] = p[p[x]]; x = p[x]
        return x
    cyc = None
    for u, v in edges:
        if c2 and [u, v] == c2: continue
        a, b = f(u), f(v)
        if a == b: cyc = [u, v]; break
        p[b] = a
    if not c2: return cyc
    return c1 if cyc else c2
@reg(B, 'redundant_II')
def _(edges):
    n = len(edges)
    for i in range(n - 1, -1, -1):
        if _is_rooted_tree(n, edges[:i] + edges[i + 1:]): return list(edges[i])

class RF_S:
    def __init__(self, arr):
        self.pos = defaultdict(list)
        for i, v in enumerate(arr): self.pos[v].append(i)
    def query(self, left, right, value):
        p = self.pos.get(value, []); return bisect.bisect_right(p, right) - bisect.bisect_left(p, left)
class RF_N:
    def __init__(self, arr): self.a = list(arr)
    def query(self, left, right, value): return self.a[left:right + 1].count(value)
design('range_freq', RF_S, RF_N)

class OS_S:
    def __init__(self, max_value):
        self.n = max_value + 1; self.t = [0] * (self.n + 1); self.cnt = [0] * self.n; self.size = 0
        self.top = 1
        while self.top * 2 <= self.n: self.top *= 2
    def insert(self, x): self.cnt[x] += 1; self.size += 1; _bit_add(self.t, x + 1, 1)
    def remove(self, x):
        if self.cnt[x] == 0: return False
        self.cnt[x] -= 1; self.size -= 1; _bit_add(self.t, x + 1, -1); return True
    def count_le(self, x): return _bit_pre(self.t, min(x, self.n - 1) + 1) if x >= 0 else 0
    def kth(self, k):
        if k < 1 or k > self.size: return -1
        pos = 0; step = self.top
        while step:
            nxt = pos + step
            if nxt <= self.n and self.t[nxt] < k: pos = nxt; k -= self.t[nxt]
            step >>= 1
        return pos   # 1-based index pos+1 holds the value pos
class OS_N:
    def __init__(self, max_value): self.a = []
    def insert(self, x): bisect.insort(self.a, x)
    def remove(self, x):
        if x in self.a: self.a.remove(x); return True
        return False
    def count_le(self, x): return sum(1 for v in self.a if v <= x)
    def kth(self, k): return self.a[k - 1] if 1 <= k <= len(self.a) else -1
design('dyn_multiset', OS_S, OS_N)

@reg(S, 'reverse_pairs')
def _(nums):
    uniq = sorted(set(nums)); t = [0] * (len(uniq) + 1); res = 0
    for j, x in enumerate(nums):
        res += j - _bit_pre(t, bisect.bisect_right(uniq, 2 * x)); _bit_add(t, bisect.bisect_left(uniq, x) + 1, 1)
    return res
@reg(B, 'reverse_pairs')
def _(nums): return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > 2 * nums[j])

@reg(S, 'calendar_k')
def _(bookings):
    xs = sorted({x for s, e in bookings for x in (s, e)}); idx = {x: i for i, x in enumerate(xs)}; m = len(xs) - 1   # elementary cells [xs[i], xs[i+1])
    mx = [0] * (4 * m); lz = [0] * (4 * m)
    def add(o, l, r, ql, qr):
        if qr < l or r < ql: return
        if ql <= l and r <= qr: mx[o] += 1; lz[o] += 1; return
        mid = (l + r) // 2; add(2 * o, l, mid, ql, qr); add(2 * o + 1, mid + 1, r, ql, qr); mx[o] = max(mx[2 * o], mx[2 * o + 1]) + lz[o]
    out = []
    for s, e in bookings: add(1, 0, m - 1, idx[s], idx[e] - 1); out.append(mx[1])
    return out
@reg(B, 'calendar_k')
def _(bookings):
    out = []
    for k in range(1, len(bookings) + 1):
        pts = sorted({x for s, e in bookings[:k] for x in (s, e)})
        out.append(max(sum(1 for s, e in bookings[:k] if s <= x < e) for x in pts))
    return out

class Stock_S:
    def __init__(self): self.p = {}; self.last = 0; self.mn = []; self.mx = []
    def update(self, timestamp, price):
        self.p[timestamp] = price; self.last = max(self.last, timestamp)
        heapq.heappush(self.mn, (price, timestamp)); heapq.heappush(self.mx, (-price, timestamp))
    def current(self): return self.p[self.last]
    def maximum(self):
        while self.p[self.mx[0][1]] != -self.mx[0][0]: heapq.heappop(self.mx)
        return -self.mx[0][0]
    def minimum(self):
        while self.p[self.mn[0][1]] != self.mn[0][0]: heapq.heappop(self.mn)
        return self.mn[0][0]
class Stock_N:
    def __init__(self): self.p = {}
    def update(self, timestamp, price): self.p[timestamp] = price
    def current(self): return self.p[max(self.p)]
    def maximum(self): return max(self.p.values())
    def minimum(self): return min(self.p.values())
design('stock_price', Stock_S, Stock_N)

class Vote_S:
    def __init__(self, persons, times):
        self.times = times; cnt = defaultdict(int); lead = -1; self.lead = []
        for p in persons:
            cnt[p] += 1
            if lead == -1 or cnt[p] >= cnt[lead]: lead = p
            self.lead.append(lead)
    def q(self, t): return self.lead[bisect.bisect_right(self.times, t) - 1]
class Vote_N:
    def __init__(self, persons, times): self.p = persons; self.t = times
    def q(self, t):
        cnt = defaultdict(int); last = {}
        for i, (p, tt) in enumerate(zip(self.p, self.t)):
            if tt > t: break
            cnt[p] += 1; last[p] = i
        m = max(cnt.values()); return max((last[p], p) for p in cnt if cnt[p] == m)[1]
design('top_voted', Vote_S, Vote_N)

class FS_S:
    def __init__(self): self.f = defaultdict(int); self.g = defaultdict(list); self.m = 0
    def push(self, x):
        self.f[x] += 1; self.m = max(self.m, self.f[x]); self.g[self.f[x]].append(x)
    def pop(self):
        x = self.g[self.m].pop(); self.f[x] -= 1
        if not self.g[self.m]: self.m -= 1
        return x
class FS_N:
    def __init__(self): self.a = []
    def push(self, x): self.a.append(x)
    def pop(self):
        m = max(self.a.count(v) for v in set(self.a))
        for i in range(len(self.a) - 1, -1, -1):
            if self.a.count(self.a[i]) == m: return self.a.pop(i)
design('freq_stack', FS_S, FS_N)

@reg(S, 'skyline')
def _(buildings):
    ev = sorted([(l, -h, r) for l, r, h in buildings] + [(r, 0, 0) for l, r, h in buildings]); h = [(0, float('inf'))]; res = []
    for x, nh, r in ev:
        while h[0][1] <= x: heapq.heappop(h)
        if nh: heapq.heappush(h, (nh, r))
        while h[0][1] <= x: heapq.heappop(h)
        cur = -h[0][0]
        if not res or res[-1][1] != cur: res.append([x, cur])
    return res
@reg(B, 'skyline')
def _(buildings):
    hi = max(r for l, r, h in buildings); res = []; prev = 0
    for x in range(0, hi + 1):
        cur = max((h for l, r, h in buildings if l <= x < r), default=0)
        if cur != prev: res.append([x, cur]); prev = cur
    return res
