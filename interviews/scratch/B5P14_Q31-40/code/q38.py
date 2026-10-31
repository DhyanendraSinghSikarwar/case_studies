import random
from collections import deque

random.seed(3801)


class ZigzagIterator:
    """Round-robin over k lists. Deque of (list, next index) for lists that still have elements."""

    def __init__(self, lists):
        self.q = deque((lst, 0) for lst in lists if lst)       # empty lists never enter

    def next(self):                                            # O(1); caller checked hasNext()
        lst, i = self.q.popleft()
        if i + 1 < len(lst):
            self.q.append((lst, i + 1))                        # back of the line for the next round
        return lst[i]

    def hasNext(self):
        return bool(self.q)


class NaiveZigzag:
    """Reference: precompute the whole order by rounds, then serve it with a cursor."""

    def __init__(self, lists):
        self.out = []
        longest = max((len(l) for l in lists), default=0)
        for r in range(longest):
            for l in lists:
                if r < len(l):
                    self.out.append(l[r])
        self.pos = 0

    def next(self):
        self.pos += 1
        return self.out[self.pos - 1]

    def hasNext(self):
        return self.pos < len(self.out)


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's examples ---
ops = [['next', []], ['next', []], ['next', []], ['next', []], ['hasNext', []], ['next', []], ['next', []], ['hasNext', []]]
r1 = run(ZigzagIterator, [[[1, 2, 3], [4], [5, 6]]], ops)
print('example 1:', r1)
assert r1 == [1, 4, 5, 2, True, 6, 3, False] == run(NaiveZigzag, [[[1, 2, 3], [4], [5, 6]]], ops)
r2 = run(ZigzagIterator, [[[], []]], [['hasNext', []]])
print('example 2:', r2)
assert r2 == [False]

# --- random operation sequences (next only when hasNext is True, as the checker promises) ---
total = 0
for _ in range(1000):
    lists = [[random.randint(0, 9) for _ in range(random.randint(0, 5))] for _ in range(random.randint(0, 5))]
    a, b = ZigzagIterator(lists), NaiveZigzag(lists)
    for _ in range(random.randint(1, 30)):
        if random.random() < 0.4 or not b.hasNext():
            assert a.hasNext() == b.hasNext()
        else:
            assert a.hasNext() and a.next() == b.next()
        total += 1
print('random ops compared:', total)

# --- the input lists are never copied or mutated ---
src = [[1, 2], [3]]
it = ZigzagIterator(src)
while it.hasNext():
    it.next()
assert src == [[1, 2], [3]]

# --- edge cases ---
assert run(ZigzagIterator, [[]], [['hasNext', []]]) == [False]                       # k = 0
assert run(ZigzagIterator, [[[7]]], [['hasNext', []], ['next', []], ['hasNext', []]]) == [True, 7, False]
one = ZigzagIterator([[], [1, 2, 3], []])                                            # one real list: plain order
assert [one.next() for _ in range(3)] == [1, 2, 3] and not one.hasNext()
dup = ZigzagIterator([[1, 1], [1, 1]])
assert [dup.next() for _ in range(4)] == [1, 1, 1, 1]
big = ZigzagIterator([list(range(i, 10 ** 4, 100)) for i in range(100)])             # k = 100, 10^4 elements total
seen = []
while big.hasNext():
    seen.append(big.next())
assert len(seen) == 10 ** 4 and seen[:3] == [0, 1, 2]
print('edge asserts passed')
