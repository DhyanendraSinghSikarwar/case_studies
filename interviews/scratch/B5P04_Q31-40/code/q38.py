import heapq
import random


class MaxStackTwo:
    """Two stacks: O(1) push/pop/top/peekMax, O(n) popMax."""
    def __init__(self):
        self.s, self.m = [], []

    def push(self, x):
        self.s.append(x)
        self.m.append(x if not self.m else max(x, self.m[-1]))

    def pop(self):
        self.m.pop()
        return self.s.pop()

    def top(self):
        return self.s[-1]

    def peekMax(self):
        return self.m[-1]

    def popMax(self):
        mx, buf = self.m[-1], []
        while self.s[-1] != mx:           # dig down to the topmost max
            buf.append(self.pop())
        self.pop()
        for x in reversed(buf):           # put the others back in order
            self.push(x)
        return mx


class MaxStackHeap:
    """Heap with lazy deletion: O(log n) amortised for every operation."""
    def __init__(self):
        self.stack, self.heap, self.val = [], [], {}
        self.dead, self.uid = set(), 0

    def push(self, x):
        self.uid += 1
        self.val[self.uid] = x
        self.stack.append(self.uid)
        heapq.heappush(self.heap, (-x, -self.uid))   # newest id wins ties = topmost

    def _clean_stack(self):
        while self.stack[-1] in self.dead:
            self.stack.pop()

    def _clean_heap(self):
        while -self.heap[0][1] in self.dead:
            heapq.heappop(self.heap)

    def pop(self):
        self._clean_stack()
        i = self.stack.pop()
        self.dead.add(i)
        return self.val[i]

    def top(self):
        self._clean_stack()
        return self.val[self.stack[-1]]

    def peekMax(self):
        self._clean_heap()
        return -self.heap[0][0]

    def popMax(self):
        self._clean_heap()
        x, i = heapq.heappop(self.heap)
        self.dead.add(-i)
        return -x


class MaxStackBrute:
    def __init__(self):
        self.a = []

    def push(self, x): self.a.append(x)
    def pop(self): return self.a.pop()
    def top(self): return self.a[-1]
    def peekMax(self): return max(self.a)

    def popMax(self):
        m = max(self.a)
        for i in range(len(self.a) - 1, -1, -1):     # topmost occurrence
            if self.a[i] == m:
                return self.a.pop(i)


def drive(cls, ops):
    o, out = cls(), []
    for name, *arg in ops:
        out.append(getattr(o, name)(*arg))
    return out


ex = [("push", 5), ("push", 1), ("push", 5), ("top",), ("popMax",), ("top",),
      ("peekMax",), ("pop",), ("top",)]
want = [None, None, None, 5, 5, 1, 5, 1, 5]
for cls in (MaxStackTwo, MaxStackHeap, MaxStackBrute):
    assert drive(cls, ex) == want, cls.__name__
print("example ->", drive(MaxStackHeap, ex))

# edge cases: duplicates of the max are removed topmost first, order of the rest kept
dup = [("push", 2), ("push", 7), ("push", 3), ("push", 7), ("popMax",), ("top",),
       ("popMax",), ("top",), ("pop",), ("top",)]
for cls in (MaxStackTwo, MaxStackHeap, MaxStackBrute):
    assert drive(cls, dup) == [None] * 4 + [7, 3, 7, 3, 3, 2], cls.__name__
one = [("push", -4), ("peekMax",), ("popMax",)]
for cls in (MaxStackTwo, MaxStackHeap, MaxStackBrute):
    assert drive(cls, one) == [None, -4, -4]

rng = random.Random(38)
for _ in range(3000):
    ops, size = [], 0
    for _ in range(rng.randint(1, 40)):
        r = rng.random()
        if size == 0 or r < 0.4:
            ops.append(("push", rng.randint(-4, 4))); size += 1
        else:
            name = rng.choice(["pop", "top", "peekMax", "popMax"])
            ops.append((name,))
            if name in ("pop", "popMax"):
                size -= 1
    r0 = drive(MaxStackBrute, ops)
    assert drive(MaxStackTwo, ops) == r0 and drive(MaxStackHeap, ops) == r0, ops
print("3000 seeded random op lists: two-stack == heap+lazy delete == brute force")
