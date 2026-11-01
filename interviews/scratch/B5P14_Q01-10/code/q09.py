import random

class NestedIterator:                  # optimal: stack of Python iterators, eager advance
    def __init__(self, nested):
        self.stack = [iter(nested)]; self.ready = None   # ready: None or a 1-tuple holding the next int
        self._advance()
    def _advance(self):
        self.ready = None
        while self.stack:
            try: x = next(self.stack[-1])
            except StopIteration:
                self.stack.pop(); continue               # this list is exhausted: go back to its parent
            if isinstance(x, int):
                self.ready = (x,); return                # found the next integer
            self.stack.append(iter(x))                   # a sub-list: descend into it
    def next(self):
        v = self.ready[0]; self._advance(); return v     # advance NOW so hasNext is always right
    def hasNext(self): return self.ready is not None

class NaiveNested:                     # brute force: recursive flatten up front (fails on depth 5000)
    def __init__(self, nested):
        self.flat = []
        def go(x):
            for y in x:
                if isinstance(y, int): self.flat.append(y)
                else: go(y)
        go(nested); self.i = 0
    def next(self): self.i += 1; return self.flat[self.i - 1]
    def hasNext(self): return self.i < len(self.flat)

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([[[1,1],2,[1,1]]], [['hasNext',[]],['next',[]],['next',[]],['next',[]],['hasNext',[]],['next',[]],['next',[]],['hasNext',[]]],
      [True,1,1,2,True,1,1,False])
e2 = ([[[],[[]],3,[[],[]]]], [['hasNext',[]],['next',[]],['hasNext',[]]], [True,3,False])
for init, ops, want in (e1, e2):
    assert run(NestedIterator, init, ops) == want == run(NaiveNested, init, ops)
print("examples:", run(NestedIterator, *e1[:2]), run(NestedIterator, *e2[:2]))

random.seed(14)
def mk(d): return [random.randint(-5, 9) if d == 0 or random.random() < .6 else mk(d - 1) for _ in range(random.randint(0, 4))]
def count(x): return sum(1 if isinstance(y, int) else count(y) for y in x)
for _ in range(1500):
    nested = mk(4); left = count(nested); ops = [['hasNext', []]]
    for _ in range(random.randint(0, 14)):
        if left and random.random() < .6: ops.append(['next', []]); left -= 1    # never next() when empty
        else: ops.append(['hasNext', []])
    assert run(NestedIterator, [nested], ops) == run(NaiveNested, [nested], ops), (nested, ops)
print("1500 random nested lists with random hasNext/next sequences: iterator == naive")

# edge cases
assert run(NestedIterator, [[]], [['hasNext', []]]) == [False]                    # empty list
assert run(NestedIterator, [[[], [[]], [[], []]]], [['hasNext', []]]) == [False]  # only empty lists
assert run(NestedIterator, [[[[[7]]]]], [['hasNext',[]],['next',[]],['hasNext',[]]]) == [True, 7, False]
it = NestedIterator([0, [], -3]); assert [it.next(), it.hasNext(), it.next(), it.hasNext()] == [0, True, -3, False]  # 0 is a value
deep = 7
for _ in range(5000): deep = [deep]                      # nesting depth 5000
it = NestedIterator(deep); assert it.hasNext() and it.next() == 7 and not it.hasNext()
try: NaiveNested(deep); recursive_ok = True
except RecursionError: recursive_ok = False
print("depth 5000: iterator ok; recursive flatten survived?", recursive_ok)
big = [[i, [i + 1]] for i in range(0, 2 * 10**5, 2)]
it = NestedIterator(big); out = []
while it.hasNext(): out.append(it.next())
assert out == list(range(2 * 10**5))
print("edge asserts ok (empty, only-empty lists, value 0, depth 5000, 2*10^5 ints)")
