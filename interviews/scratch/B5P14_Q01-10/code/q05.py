import random

class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key = key; self.val = val; self.prev = None; self.next = None

class LRUCache:                        # dict + doubly linked list, dummy head (MRU side) and dummy tail (LRU side)
    def __init__(self, capacity):
        self.cap = capacity; self.map = {}
        self.head = Node(); self.tail = Node()
        self.head.next = self.tail; self.tail.prev = self.head
    def _unlink(self, node):
        node.prev.next = node.next          # unlink 1: left neighbour skips node
        node.next.prev = node.prev          # unlink 2: right neighbour skips node
        # node.prev / node.next are stale now; _push_front overwrites both
    def _push_front(self, node):
        node.prev = self.head               # push 1
        node.next = self.head.next          # push 2
        self.head.next.prev = node          # push 3: old first node points back at us
        self.head.next = node               # push 4: head points forward at us
    def get(self, key):
        node = self.map.get(key)
        if node is None: return -1
        self._unlink(node); self._push_front(node)      # even a read mutates the list
        return node.val
    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.val = value; self._unlink(node); self._push_front(node); return
        if len(self.map) == self.cap:
            lru = self.tail.prev            # never the head dummy because cap >= 1
            self._unlink(lru); del self.map[lru.key]    # node stores its key for exactly this delete
        node = Node(key, value); self.map[key] = node; self._push_front(node)
    def order(self):
        out = []; n = self.head.next
        while n is not self.tail: out.append(n.key); n = n.next
        return out
    def size(self): return len(self.map)

class NaiveLRU:                        # brute force: list of [key, value], least recent first, O(n) scans
    def __init__(self, capacity): self.cap = capacity; self.items = []
    def _find(self, key):
        for i, (k, _) in enumerate(self.items):
            if k == key: return i
        return -1
    def get(self, key):
        i = self._find(key)
        if i < 0: return -1
        kv = self.items.pop(i); self.items.append(kv); return kv[1]
    def put(self, key, value):
        i = self._find(key)
        if i >= 0: self.items.pop(i)
        elif len(self.items) == self.cap: self.items.pop(0)
        self.items.append([key, value])
    def order(self): return [k for k, _ in reversed(self.items)]
    def size(self): return len(self.items)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([3], [['put',[1,'a']],['put',[2,'b']],['put',[3,'c']],['order',[]],['get',[1]],['order',[]],['put',[4,'d']],
            ['order',[]],['get',[2]],['size',[]]], [None,None,None,[3,2,1],'a',[1,3,2],None,[4,1,3],-1,3])
e2 = ([1], [['put',[1,1]],['put',[2,2]],['get',[1]],['get',[2]],['order',[]]], [None,None,-1,2,[2]])
for init, ops, want in (e1, e2):
    assert run(LRUCache, init, ops) == want == run(NaiveLRU, init, ops)
print("examples:", run(LRUCache, *e1[:2]), run(LRUCache, *e2[:2]))

def check_links(c):                    # structural invariant: forward and backward walks agree with the dict
    fwd = []; n = c.head.next
    while n is not c.tail: assert n.prev.next is n and n.next.prev is n; fwd.append(n.key); n = n.next
    assert len(fwd) == len(c.map) <= c.cap and set(fwd) == set(c.map)

random.seed(14)
for _ in range(1000):
    cap = random.randint(1, 4)
    ops = [random.choice([['get', [random.randint(0, 5)]], ['put', [random.randint(0, 5), random.randint(0, 99)]],
                          ['order', []], ['size', []]]) for _ in range(random.randint(0, 50))]
    assert run(LRUCache, [cap], ops) == run(NaiveLRU, [cap], ops), (cap, ops)
    c = LRUCache(cap)
    for m, a in ops: getattr(c, m)(*a); check_links(c)
print("1000 random operation sequences: linked list == naive, links consistent after every call")

# edge cases
c = LRUCache(1); c.put(1, 1); c.put(1, 2); assert c.order() == [1] and c.get(1) == 2   # update at capacity: no eviction
c.put(2, 3); assert c.get(1) == -1 and c.order() == [2]
c = LRUCache(2); assert c.get(0) == -1 and c.order() == [] and c.size() == 0           # empty
c.put(1, 1); c.put(2, 2); c.get(1); c.put(3, 3); assert c.order() == [3, 1]            # 2 was least recent
c = LRUCache(3000)
for k in range(10**5): c.put(k, k)
assert c.size() == 3000 and c.order()[0] == 10**5 - 1 and c.order()[-1] == 10**5 - 3000
print("edge asserts ok (capacity 1, empty, 10^5 puts at capacity 3000)")
