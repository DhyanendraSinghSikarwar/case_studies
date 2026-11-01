import random


class DNode:
    __slots__ = ('val', 'prev', 'next')

    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class DLL:
    """Doubly linked list with two sentinels. Real nodes always sit strictly between them."""

    def __init__(self):
        self.head = DNode()          # sentinel, never removed
        self.tail = DNode()          # sentinel, never removed
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _insert_between(self, v, left, right):
        node = DNode(v, left, right)   # new node's two pointers
        left.next = node               # left neighbour's next
        right.prev = node              # right neighbour's prev
        self.size += 1                 # 4 assignments in total
        return node

    def add_first(self, v):
        return self._insert_between(v, self.head, self.head.next)

    def add_last(self, v):
        return self._insert_between(v, self.tail.prev, self.tail)

    def remove(self, node):
        assert node is not self.head and node is not self.tail, "sentinels are never removed"
        assert node.prev is not None and node.next is not None, "node already removed"
        node.prev.next = node.next     # 2 assignments bypass the node
        node.next.prev = node.prev
        node.prev = node.next = None   # detach so a double remove is caught
        self.size -= 1
        return node.val

    def pop_first(self):
        if self.head.next is self.tail:
            return None
        return self.remove(self.head.next)

    def pop_last(self):
        if self.tail.prev is self.head:
            return None
        return self.remove(self.tail.prev)

    def to_array(self):
        out = []
        n = self.head.next
        while n is not self.tail:
            out.append(n.val)
            n = n.next
            assert len(out) <= self.size, "forward walk is longer than size (broken links)"
        return out

    def to_array_backward(self):
        out = []
        n = self.tail.prev
        while n is not self.head:
            out.append(n.val)
            n = n.prev
            assert len(out) <= self.size, "backward walk is longer than size (broken links)"
        return out

    def check(self):
        fwd, bwd = self.to_array(), self.to_array_backward()
        assert fwd == bwd[::-1] and len(fwd) == self.size
        assert self.head.prev is None and self.tail.next is None
        return fwd


# Brute force model: a plain Python list (insert(0) and pop(0) are O(n); removing a node means a search, O(n)).
# The prompt's walk-through
d = DLL()
d.add_last(1); d.add_last(2); d.add_first(0)
print('after add_last 1, add_last 2, add_first 0:', d.check())
print('pop_last ->', d.pop_last(), d.check())
print('pop_first ->', d.pop_first(), d.check())
print('pop_first ->', d.pop_first(), d.check())
print('pop_first on empty ->', d.pop_first(), '| pop_last on empty ->', d.pop_last(), '| to_array ->', d.to_array())

# remove(node) from the middle, with node handles
d = DLL()
a, b, c = d.add_last('a'), d.add_last('b'), d.add_last('c')
print('remove middle ->', d.remove(b), d.check())
try:
    d.remove(b)
except AssertionError as e:
    print('double remove caught:', e)
try:
    d.remove(d.head)
except AssertionError as e:
    print('sentinel remove caught:', e)

# seeded randomised cross-check against a Python list model; mirror check after EVERY operation
rng = random.Random(29)
ops_done = 0
for trial in range(300):
    d = DLL()
    model = []                       # list of (value, node) in order
    nxt = 0
    for _ in range(rng.randint(1, 40)):
        op = rng.choice(['af', 'al', 'rm', 'pf', 'pl'])
        if op == 'af':
            model.insert(0, (nxt, d.add_first(nxt))); nxt += 1
        elif op == 'al':
            model.append((nxt, d.add_last(nxt))); nxt += 1
        elif op == 'rm' and model:
            i = rng.randrange(len(model))
            v, node = model.pop(i)
            assert d.remove(node) == v
        elif op == 'pf':
            got = d.pop_first()
            assert got == (model.pop(0)[0] if model else None)
        elif op == 'pl':
            got = d.pop_last()
            assert got == (model.pop()[0] if model else None)
        assert d.check() == [v for v, _ in model]
        assert d.head.next is d.tail or d.head.next.prev is d.head
        ops_done += 1
print('300 random op sequences,', ops_done, 'operations, mirror check after each: OK')

# sentinels survive emptying
d = DLL()
for i in range(5):
    d.add_last(i)
while d.pop_first() is not None:
    pass
assert d.head.next is d.tail and d.tail.prev is d.head and d.size == 0
print('sentinels intact after emptying: True')
