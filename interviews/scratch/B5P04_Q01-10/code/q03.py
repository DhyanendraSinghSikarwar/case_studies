import random
from collections import deque


class BruteQueue:
    """Move everything to the second stack and back on every pop: O(n) each time."""
    def __init__(self): self.s1, self.s2 = [], []
    def push(self, x): self.s1.append(x)
    def _flip(self, src, dst):
        while src: dst.append(src.pop())
    def pop(self):
        self._flip(self.s1, self.s2)
        v = self.s2.pop()
        self._flip(self.s2, self.s1)
        return v
    def peek(self):
        self._flip(self.s1, self.s2)
        v = self.s2[-1]
        self._flip(self.s2, self.s1)
        return v
    def empty(self): return not self.s1


class MyQueue:
    """Input stack + output stack; refill output only when it is empty."""
    def __init__(self):
        self.inp, self.out = [], []
        self.moves = 0                          # instrumentation for the amortised proof
    def push(self, x): self.inp.append(x)
    def _fill(self):
        if not self.out:                        # the key condition
            while self.inp:
                self.out.append(self.inp.pop())
                self.moves += 1
    def pop(self):
        self._fill()
        return self.out.pop()
    def peek(self):
        self._fill()
        return self.out[-1]
    def empty(self): return not self.inp and not self.out


# prompt example
q = MyQueue()
q.push(1); q.push(2)
assert q.peek() == 1
assert q.pop() == 1
assert q.empty() is False
assert q.pop() == 2
assert q.empty() is True
print("prompt example passes")

# a single pop can be O(n) ...
q = MyQueue()
for i in range(1000): q.push(i)
q.pop()
print("first pop after 1000 pushes moved", q.moves, "elements")
# ... but total moves over a whole run never exceed the number of pushes
for i in range(999): q.pop()
print("after draining: total moves =", q.moves, "(pushes = 1000)")
assert q.moves == 1000

# interleaved push/pop: moves <= pushes always
rng = random.Random(3)
q, pushes = MyQueue(), 0
for _ in range(20000):
    if rng.random() < 0.55 or q.empty():
        q.push(pushes); pushes += 1
    else:
        q.pop()
    assert q.moves <= pushes
print("interleaved run: moves", q.moves, "<= pushes", pushes)

# edge cases
q = MyQueue()
assert q.empty()
q.push(9); assert q.peek() == 9 and q.pop() == 9 and q.empty()
q.push(1); q.push(2); q.pop(); q.push(3)       # push while output is non-empty
assert q.pop() == 2 and q.pop() == 3 and q.empty()
q.push(5); q.push(5)                            # duplicates
assert q.pop() == 5 and q.pop() == 5

# seeded randomised cross-check: MyQueue and BruteQueue vs collections.deque
rng = random.Random(7)
ops = 0
for _ in range(400):
    a, b, ref = MyQueue(), BruteQueue(), deque()
    for _ in range(rng.randint(1, 60)):
        r = rng.random()
        if r < 0.5 or not ref:
            x = rng.randint(-5, 5)
            a.push(x); b.push(x); ref.append(x)
        elif r < 0.7:
            assert a.peek() == b.peek() == ref[0]
        else:
            assert a.pop() == b.pop() == ref.popleft()
        assert a.empty() == b.empty() == (not ref)
        ops += 1
print("random cross-check passed:", ops, "operations")
