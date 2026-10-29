import random
from collections import OrderedDict

random.seed(4001)


class Bucket:
    """All keys that currently hold the same count; keys in order of arrival (oldest first)."""
    __slots__ = ('cnt', 'keys', 'prev', 'next')

    def __init__(self, cnt):
        self.cnt, self.keys, self.prev, self.next = cnt, OrderedDict(), None, None


class AllOne:
    def __init__(self):
        self.head, self.tail = Bucket(0), Bucket(0)          # dummies: head side = small counts
        self.head.next, self.tail.prev = self.tail, self.head
        self.where = {}                                      # key -> its bucket

    def _insert_after(self, node, cnt):
        b = Bucket(cnt)
        b.prev, b.next = node, node.next
        node.next.prev = b
        node.next = b
        return b

    def _drop_if_empty(self, b):
        if not b.keys:                                       # unlink an empty bucket: O(1)
            b.prev.next, b.next.prev = b.next, b.prev

    def inc(self, key):
        b = self.where.get(key)
        if b is None:                                        # new key: count 1
            nb = self.head.next if self.head.next.cnt == 1 else self._insert_after(self.head, 1)
        else:
            nb = b.next if (b.next is not self.tail and b.next.cnt == b.cnt + 1) else self._insert_after(b, b.cnt + 1)
            del b.keys[key]
            self._drop_if_empty(b)
        nb.keys[key] = None                                  # joins the END of the new bucket
        self.where[key] = nb

    def dec(self, key):
        b = self.where.get(key)
        if b is None:                                        # unknown key: nothing happens
            return
        del b.keys[key]
        if b.cnt == 1:
            del self.where[key]                              # count 0: the key disappears
        else:
            pb = b.prev if (b.prev is not self.head and b.prev.cnt == b.cnt - 1) else self._insert_after(b.prev, b.cnt - 1)
            pb.keys[key] = None
            self.where[key] = pb
        self._drop_if_empty(b)

    def getMaxKey(self):
        return next(iter(self.tail.prev.keys)) if self.where else ''      # oldest key in the top bucket

    def getMinKey(self):
        return next(iter(self.head.next.keys)) if self.where else ''


class NaiveAllOne:
    """Counts + a last-change stamp per key; getters scan every key."""

    def __init__(self):
        self.c, self.stamp, self.t = {}, {}, 0

    def inc(self, key):
        self.t += 1
        self.c[key] = self.c.get(key, 0) + 1
        self.stamp[key] = self.t

    def dec(self, key):
        if key not in self.c:
            return
        self.t += 1
        self.c[key] -= 1
        self.stamp[key] = self.t
        if self.c[key] == 0:
            del self.c[key], self.stamp[key]

    def getMaxKey(self):
        if not self.c:
            return ''
        m = max(self.c.values())
        return min((self.stamp[k], k) for k in self.c if self.c[k] == m)[1]     # earliest change wins

    def getMinKey(self):
        if not self.c:
            return ''
        m = min(self.c.values())
        return min((self.stamp[k], k) for k in self.c if self.c[k] == m)[1]


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's example ---
ops = [['inc', ['a']], ['inc', ['b']], ['inc', ['b']], ['getMaxKey', []], ['getMinKey', []], ['inc', ['a']],
       ['inc', ['c']], ['getMaxKey', []], ['getMinKey', []], ['dec', ['b']], ['dec', ['b']], ['getMaxKey', []],
       ['dec', ['z']], ['getMinKey', []]]
r = run(AllOne, [], ops)
print('example:', r)
assert r == [None, None, None, 'b', 'a', None, None, 'b', 'c', None, None, 'a', None, 'c'] == run(NaiveAllOne, [], ops)

# --- random operation-sequence oracle ---
keys = ['a', 'b', 'c', 'd', 'e']
total = 0
for _ in range(1500):
    ops = []
    for _ in range(random.randint(1, 40)):
        x = random.random()
        ops.append(['inc', [random.choice(keys)]] if x < 0.45 else ['dec', [random.choice(keys)]] if x < 0.75
                   else [random.choice(['getMaxKey', 'getMinKey']), []])
    assert run(AllOne, [], ops) == run(NaiveAllOne, [], ops), ops
    total += len(ops)
print('random ops compared:', total)

# --- structural invariant: bucket counts strictly increase and no bucket is empty ---
a = AllOne()
for _ in range(3000):
    k = random.choice(keys)
    a.inc(k) if random.random() < 0.55 else a.dec(k)
    n, last, seen = a.head.next, 0, 0
    while n is not a.tail:
        assert n.cnt > last and n.keys
        last = n.cnt
        seen += len(n.keys)
        n = n.next
    assert seen == len(a.where)
print('bucket list invariant held')

# --- the tie rule in action: who is "oldest at this count" ---
t = AllOne()
for k in ['x', 'y', 'z']:
    t.inc(k)                                     # all count 1, x arrived first
print('min key with x, y, z at 1:', t.getMinKey())
t.inc('x'); t.dec('x')                           # x goes 1 -> 2 -> 1: it rejoins the END of bucket 1
print('after x goes 1->2->1, min key:', t.getMinKey(), '(y has held count 1 the longest)')
assert t.getMinKey() == 'y'

# --- edge cases ---
e = AllOne()
assert e.getMaxKey() == '' and e.getMinKey() == ''                     # empty
e.dec('nope'); assert e.getMaxKey() == ''                              # dec of unknown key
e.inc('k'); assert e.getMaxKey() == e.getMinKey() == 'k'               # one key is both max and min
e.dec('k'); assert e.getMaxKey() == '' and not e.where                 # count 0 removes it
e.inc('k'); e.inc('k'); e.inc('k'); e.dec('k'); assert e.getMaxKey() == 'k'
for k in 'pq':
    e.inc(k)
assert e.getMinKey() == 'p' and e.getMaxKey() == 'k'
big = AllOne()
for i in range(10 ** 4):
    big.inc('key%d' % i)
for i in range(10 ** 4):
    big.inc('key%d' % i)
assert big.getMaxKey() == 'key0' and big.getMinKey() == 'key0'         # all at 2, key0 reached 2 first
print('edge asserts passed')
