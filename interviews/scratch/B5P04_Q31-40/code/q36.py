import random
from collections import deque


class CircularDeque:
    def __init__(self, k):
        self.a = [0] * k
        self.k = k
        self.head = 0                    # index of the front element
        self.size = 0

    def insertFront(self, v):
        if self.size == self.k:
            return False
        self.head = (self.head - 1) % self.k      # Python's % is never negative
        self.a[self.head] = v
        self.size += 1
        return True

    def insertLast(self, v):
        if self.size == self.k:
            return False
        self.a[(self.head + self.size) % self.k] = v
        self.size += 1
        return True

    def deleteFront(self):
        if self.size == 0:
            return False
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True

    def deleteLast(self):
        if self.size == 0:
            return False
        self.size -= 1
        return True

    def getFront(self):
        return -1 if self.size == 0 else self.a[self.head]

    def getRear(self):
        return -1 if self.size == 0 else self.a[(self.head + self.size - 1) % self.k]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k


class RefDeque:
    """Brute force: a Python deque plus a capacity check."""
    def __init__(self, k):
        self.d, self.k = deque(), k

    def insertFront(self, v):
        if len(self.d) == self.k: return False
        self.d.appendleft(v); return True

    def insertLast(self, v):
        if len(self.d) == self.k: return False
        self.d.append(v); return True

    def deleteFront(self):
        if not self.d: return False
        self.d.popleft(); return True

    def deleteLast(self):
        if not self.d: return False
        self.d.pop(); return True

    def getFront(self): return self.d[0] if self.d else -1
    def getRear(self): return self.d[-1] if self.d else -1
    def isEmpty(self): return not self.d
    def isFull(self): return len(self.d) == self.k


c = CircularDeque(3)
trace = [c.insertLast(1), c.insertLast(2), c.insertFront(3), c.insertFront(4),
         c.getRear(), c.isFull(), c.deleteLast(), c.insertFront(4), c.getFront()]
print(trace)
assert trace == [True, True, True, False, 2, True, True, True, 4]
print("(-1) % 3 =", (-1) % 3, "in Python (a C-style % would give -1)")

# edge cases
c1 = CircularDeque(1)
assert c1.getFront() == -1 and c1.getRear() == -1 and not c1.deleteFront() and not c1.deleteLast()
assert c1.insertFront(7) and c1.isFull() and not c1.insertLast(8) and not c1.insertFront(8)
assert c1.getFront() == c1.getRear() == 7 and c1.deleteLast() and c1.isEmpty()
c2 = CircularDeque(3)                    # wrap-around on both ends
for v in (1, 2, 3):
    assert c2.insertFront(v)             # front-to-back: 3 2 1
assert [c2.getFront(), c2.getRear()] == [3, 1]
assert c2.deleteFront() and c2.insertLast(9) and [c2.getFront(), c2.getRear()] == [2, 9]

rng = random.Random(36)
ops = ["insertFront", "insertLast", "deleteFront", "deleteLast", "getFront", "getRear", "isEmpty", "isFull"]
for _ in range(2000):
    k = rng.randint(1, 6)
    a, b = CircularDeque(k), RefDeque(k)
    for _ in range(rng.randint(1, 40)):
        op = rng.choice(ops)
        if op.startswith("insert"):
            v = rng.randint(1, 99)
            assert getattr(a, op)(v) == getattr(b, op)(v), (k, op)
        else:
            assert getattr(a, op)() == getattr(b, op)(), (k, op)
print("2000 seeded random op sequences match the deque-based reference")
