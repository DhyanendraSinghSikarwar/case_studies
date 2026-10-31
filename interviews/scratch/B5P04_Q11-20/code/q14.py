import random
from collections import deque


# Only queue operations are used on the internal queues:
# append (enqueue to back), popleft (dequeue from front), len (size), truthiness (is-empty)
# and q[0] as the queue's "front" peek. Never indexed elsewhere, never popped from the right.

class StackOneQueue:
    """push is O(n) (rotate), pop/top/empty are O(1)."""

    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):       # move the n older items behind the new one
            self.q.append(self.q.popleft())

    def pop(self):
        return self.q.popleft()

    def top(self):
        return self.q[0]                       # peek at the FRONT: a queue's own front() operation

    def empty(self):
        return not self.q


class StackTwoQueues:
    """push is O(1), pop/top are O(n): drain all but the last item into the spare queue."""

    def __init__(self):
        self.a, self.b = deque(), deque()
        self.last = None

    def push(self, x):
        self.a.append(x)
        self.last = x

    def _shift(self):
        while len(self.a) > 1:
            self.last = self.a.popleft()
            self.b.append(self.last)
        return self.a.popleft()

    def pop(self):
        x = self._shift()
        self.a, self.b = self.b, self.a
        return x

    def top(self):
        return self.last

    def empty(self):
        return not self.a


def run(cls, ops):
    s, out = cls(), []
    for op, *arg in ops:
        if op == "push":
            s.push(arg[0])
            out.append(None)
        else:
            out.append(getattr(s, op)())
    return out


def run_list_stack(ops):
    s, out = [], []
    for op, *arg in ops:
        if op == "push":
            s.append(arg[0])
            out.append(None)
        elif op == "pop":
            out.append(s.pop())
        elif op == "top":
            out.append(s[-1])
        else:
            out.append(not s)
    return out


example = [("push", 1), ("push", 2), ("top",), ("pop",), ("empty",), ("pop",), ("empty",)]
for cls in (StackOneQueue, StackTwoQueues):
    got = run(cls, example)
    assert got == [None, None, 2, 2, False, 1, True], got
    print(cls.__name__, "->", got)

for cls in (StackOneQueue, StackTwoQueues):
    s = cls()
    assert s.empty()
    s.push(7)
    assert s.top() == 7 and not s.empty()
    assert s.pop() == 7 and s.empty()
    for v in [5, 5, 5]:                    # duplicates
        s.push(v)
    assert [s.pop(), s.pop(), s.pop()] == [5, 5, 5] and s.empty()
    for v in range(1000):
        s.push(v)
    assert [s.pop() for _ in range(1000)] == list(range(999, -1, -1))   # max size order

rng = random.Random(14)
cases = 0
for _ in range(1500):
    ops, size = [], 0
    for _ in range(rng.randint(1, 30)):
        r = rng.random()
        if size == 0 or r < 0.5:
            ops.append(("push", rng.randint(-5, 5)))
            size += 1
        elif r < 0.75:
            ops.append(("top",))
        elif r < 0.9:
            ops.append(("pop",))
            size -= 1
        else:
            ops.append(("empty",))
    want = run_list_stack(ops)
    assert run(StackOneQueue, ops) == want, ops
    assert run(StackTwoQueues, ops) == want, ops
    cases += 1
print("random cross-check passed:", cases, "operation sequences")

# operation counting: queue operations used per call, to show where the O(n) sits
class Counted(deque):
    ops = 0

    def append(self, x):
        Counted.ops += 1
        super().append(x)

    def popleft(self):
        Counted.ops += 1
        return super().popleft()


def cost_of_push(n):
    s = StackOneQueue()
    s.q = Counted()
    for v in range(n):
        s.push(v)
    Counted.ops = 0
    s.push(n)
    return Counted.ops

print("queue ops for one push when n items are present (one-queue version):",
      [(n, cost_of_push(n)) for n in (0, 1, 10, 100)])
