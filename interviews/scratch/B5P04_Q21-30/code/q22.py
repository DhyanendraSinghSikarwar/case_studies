import random
from collections import deque


class MyCircularQueue:
    def __init__(self, k):
        self.k = k
        self.buf = [None] * k
        self.head = 0
        self.size = 0

    def enQueue(self, x):
        if self.size == self.k:
            return False
        self.buf[(self.head + self.size) % self.k] = x
        self.size += 1
        return True

    def deQueue(self):
        if self.size == 0:
            return False
        self.buf[self.head] = None                 # drop the reference
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True

    def Front(self):
        return -1 if self.size == 0 else self.buf[self.head]

    def Rear(self):
        return -1 if self.size == 0 else self.buf[(self.head + self.size - 1) % self.k]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k


class ListModel:                                    # brute force: list.pop(0), O(n) dequeue
    def __init__(self, k):
        self.k, self.a = k, []

    def enQueue(self, x):
        if len(self.a) == self.k:
            return False
        self.a.append(x)
        return True

    def deQueue(self):
        if not self.a:
            return False
        self.a.pop(0)
        return True

    def Front(self):
        return self.a[0] if self.a else -1

    def Rear(self):
        return self.a[-1] if self.a else -1

    def isEmpty(self):
        return not self.a

    def isFull(self):
        return len(self.a) == self.k


q = MyCircularQueue(3)
trace = [q.enQueue(1), q.enQueue(2), q.enQueue(3), q.enQueue(4), q.Rear(), q.isFull(),
         q.deQueue(), q.enQueue(4), q.Rear(), q.Front()]
print(trace)
assert trace == [True, True, True, False, 3, True, True, True, 4, 2]

e = MyCircularQueue(2)
assert e.Front() == -1 and e.Rear() == -1 and e.isEmpty() and not e.isFull() and e.deQueue() is False
one = MyCircularQueue(1)
assert one.enQueue(9) and one.isFull() and not one.enQueue(8) and one.Front() == one.Rear() == 9
assert one.deQueue() and one.isEmpty() and one.enQueue(7) and one.Front() == 7
z = MyCircularQueue(2)                              # 0 is a valid value, -1 only means empty
assert z.enQueue(0) and z.Front() == 0 and z.Rear() == 0

rng = random.Random(22)
ops_run = wraps = 0
for _ in range(300):
    k = rng.randint(1, 6)
    a, b, c = MyCircularQueue(k), ListModel(k), deque()
    for _ in range(60):
        op = rng.choice(["enQueue", "enQueue", "deQueue", "Front", "Rear", "isEmpty", "isFull"])
        if op == "enQueue":
            x = rng.randint(0, 9)
            ra, rb = a.enQueue(x), b.enQueue(x)
            if ra:
                c.append(x)
            assert ra == rb
        elif op == "deQueue":
            ra, rb = a.deQueue(), b.deQueue()
            if rb:
                c.popleft()
            assert ra == rb
        else:
            assert getattr(a, op)() == getattr(b, op)()
        assert a.size == len(b.a) == len(c) and (not c or a.Front() == c[0])
        wraps += (a.head + a.size > k)
        ops_run += 1
print("random cross-check passed:", ops_run, "operations; wrapped states seen:", wraps > 0)
