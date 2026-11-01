import random
from collections import OrderedDict


class Node:
    __slots__ = ('key', 'val', 'prev', 'next')

    def __init__(self, key=None, val=None):
        self.key, self.val, self.prev, self.next = key, val, None, None


class LRU:
    """dict key -> node, plus a doubly linked list with sentinels. Most recent right after head."""

    def __init__(self, capacity):
        assert capacity >= 1
        self.cap = capacity
        self.map = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev

    def _push_front(self, n):
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n

    def get(self, key):
        n = self.map.get(key)
        if n is None:
            return -1
        self._unlink(n)              # O(1) because we hold the node and it has prev
        self._push_front(n)          # now the most recently used
        return n.val

    def put(self, key, val):
        n = self.map.get(key)
        if n is not None:            # existing key: update and refresh
            n.val = val
            self._unlink(n)
            self._push_front(n)
            return
        if len(self.map) == self.cap:    # full: evict the least recently used, just before tail
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]        # the node stores its key so we can delete from the dict
        n = Node(key, val)
        self.map[key] = n
        self._push_front(n)

    def keys_recent_first(self):
        out, n = [], self.head.next
        while n is not self.tail:
            out.append(n.key)
            n = n.next
            assert len(out) <= len(self.map), "broken links"
        back, n = [], self.tail.prev
        while n is not self.head:
            back.append(n.key)
            n = n.prev
            assert len(back) <= len(self.map), "broken links"
        assert out == back[::-1] and set(out) == set(self.map)
        return out


class LRUBrute:
    """Brute force: dict plus a list of keys ordered by use. Refreshing a key is a list scan, O(capacity)."""

    def __init__(self, capacity):
        self.cap, self.d, self.order = capacity, {}, []   # order[0] is least recent

    def _touch(self, key):
        self.order.remove(key)           # O(c) search
        self.order.append(key)

    def get(self, key):
        if key not in self.d:
            return -1
        self._touch(key)
        return self.d[key]

    def put(self, key, val):
        if key in self.d:
            self.d[key] = val
            self._touch(key)
            return
        if len(self.d) == self.cap:
            old = self.order.pop(0)
            del self.d[old]
        self.d[key] = val
        self.order.append(key)


class LRUOrdered:
    """Reference: collections.OrderedDict (a hash map plus a doubly linked list inside)."""

    def __init__(self, capacity):
        self.cap, self.od = capacity, OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, val):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = val
        if len(self.od) > self.cap:
            self.od.popitem(last=False)


# prompt example, capacity 2
c = LRU(2)
c.put(1, 1); c.put(2, 2)
print('get(1) ->', c.get(1), '| recent first:', c.keys_recent_first())
c.put(3, 3)
print('put(3,3) evicts 2; get(2) ->', c.get(2), '| recent first:', c.keys_recent_first())
c.put(4, 4)
print('put(4,4) evicts 1; get(1) ->', c.get(1))
print('get(3) ->', c.get(3), '| get(4) ->', c.get(4), '| recent first:', c.keys_recent_first())

# put on an existing key refreshes it and updates the value
c = LRU(2)
c.put(1, 'a'); c.put(2, 'b'); c.put(1, 'A'); c.put(3, 'c')   # 2 is now least recent and is evicted
assert c.get(2) == -1 and c.get(1) == 'A' and c.get(3) == 'c'
# capacity 1
c = LRU(1)
c.put(1, 1); c.put(2, 2)
assert c.get(1) == -1 and c.get(2) == 2
print('refresh-on-put and capacity 1: OK')

# seeded randomised cross-check of all three
rng = random.Random(30)
ops = 0
for _ in range(300):
    cap = rng.randint(1, 5)
    a, b, o = LRU(cap), LRUBrute(cap), LRUOrdered(cap)
    for _ in range(rng.randint(1, 60)):
        k = rng.randint(0, 7)
        if rng.random() < 0.5:
            v = rng.randint(0, 99)
            a.put(k, v); b.put(k, v); o.put(k, v)
        else:
            assert a.get(k) == b.get(k) == o.get(k)
        assert a.keys_recent_first() == b.order[::-1] == list(reversed(o.od))
        assert len(a.map) <= cap
        ops += 1
print('300 random sessions,', ops, 'operations, LRU = brute force = OrderedDict: OK')
