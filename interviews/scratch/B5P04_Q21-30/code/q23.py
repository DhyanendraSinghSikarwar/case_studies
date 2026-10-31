import random
from collections import deque


class MonoQueue:
    def __init__(self):
        self.d = deque()

    def push(self, v):
        while self.d and self.d[-1] < v:            # strictly smaller only: keep equals
            self.d.pop()
        self.d.append(v)

    def popLeft(self, v):
        if self.d and self.d[0] == v:
            self.d.popleft()

    def getMax(self):
        if not self.d:
            raise ValueError("getMax on an empty queue")
        return self.d[0]


class BuggyMonoQueue(MonoQueue):                    # the duplicate bug: pops equals too
    def push(self, v):
        while self.d and self.d[-1] <= v:
            self.d.pop()
        self.d.append(v)


class Brute:
    def __init__(self):
        self.a = []

    def push(self, v):
        self.a.append(v)

    def popLeft(self, v):
        assert self.a[0] == v
        self.a.pop(0)

    def getMax(self):
        return max(self.a)


def window_max(stream, k):
    q, out = MonoQueue(), []
    for i, v in enumerate(stream):
        q.push(v)
        if i >= k - 1:
            out.append(q.getMax())
            q.popLeft(stream[i - k + 1])
    return out


def window_max_brute(stream, k):
    return [max(stream[i:i + k]) for i in range(len(stream) - k + 1)]


q = MonoQueue()
log = []
q.push(3); q.push(1); log.append(q.getMax())
q.push(2); q.popLeft(3); log.append(q.getMax())
q.popLeft(1); log.append(q.getMax())
q.push(5); log.append(q.getMax())
print(log)
assert log == [3, 2, 2, 5]

r = MonoQueue()
r.push(2); r.push(2); r.popLeft(2)
print("duplicates:", r.getMax())
assert r.getMax() == 2

b = BuggyMonoQueue()
b.push(2); b.push(2); b.popLeft(2)
print("buggy (pops equals) after the same steps, items left:", len(b.d), "(getMax would fail)")
assert len(b.d) == 0

try:
    MonoQueue().getMax()
except ValueError as e:
    print("empty:", e)

assert window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert window_max([5], 1) == [5]
assert window_max([2, 2, 2, 2], 2) == [2, 2, 2]
assert window_max([4, 3, 2, 1], 4) == [4]

rng = random.Random(23)
ops = 0
for _ in range(400):
    m, ref, live = MonoQueue(), Brute(), []
    for _ in range(40):
        if live and rng.random() < 0.4:
            v = live.pop(0)
            m.popLeft(v)
            ref.popLeft(v)
        else:
            v = rng.randint(0, 4)                   # tiny range: many duplicates
            live.append(v)
            m.push(v)
            ref.push(v)
        if live:
            assert m.getMax() == ref.getMax(), live
        ops += 1
for _ in range(300):
    s = [rng.randint(-5, 5) for _ in range(rng.randint(1, 12))]
    k = rng.randint(1, len(s))
    assert window_max(s, k) == window_max_brute(s, k)
print("random cross-check passed:", ops, "queue ops and 300 window runs")
