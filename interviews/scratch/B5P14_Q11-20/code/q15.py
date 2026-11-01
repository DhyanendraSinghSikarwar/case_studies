import random

class NaivePeeking:                      # brute force: copies everything into a list (not allowed by the prompt, fine as an oracle)
    def __init__(self, it): self.a = list(it); self.i = 0
    def peek(self): return self.a[self.i]
    def next(self): self.i += 1; return self.a[self.i - 1]
    def hasNext(self): return self.i < len(self.a)

_DONE = object()

class PeekingIterator:
    def __init__(self, it):
        self.it = it
        self.buf = next(it, _DONE)       # buffer is filled eagerly, one element ahead
    def peek(self): return self.buf
    def next(self):
        v = self.buf
        self.buf = next(self.it, _DONE)  # refill right after consuming
        return v
    def hasNext(self): return self.buf is not _DONE

def run(cls, init, ops):
    o = cls(iter(init[0]))
    return [getattr(o, m)(*a) for m, a in ops]

e1 = dict(init=[[1, 2, 3]], ops=[['next', []], ['peek', []], ['next', []], ['next', []], ['hasNext', []]])
e2 = dict(init=[[7]], ops=[['peek', []], ['peek', []], ['hasNext', []], ['next', []], ['hasNext', []]])
assert run(PeekingIterator, **e1) == [1, 2, 2, 3, False] == run(NaivePeeking, **e1)
assert run(PeekingIterator, **e2) == [7, 7, True, 7, False] == run(NaivePeeking, **e2)
print('examples ->', run(PeekingIterator, **e1), run(PeekingIterator, **e2))

random.seed(15)
for case in range(600):
    data = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    ops = []; left = len(data)
    for _ in range(random.randint(0, 20)):
        r = random.random()
        if left and r < 0.35: ops.append(['next', []]); left -= 1
        elif left and r < 0.7: ops.append(['peek', []])
        else: ops.append(['hasNext', []])
    assert run(PeekingIterator, [data], ops) == run(NaivePeeking, [data], ops)
print('600 random sequences match the naive reference')

# it works on a one-shot generator and never reads more than one element ahead
pulled = []
def gen():
    for i in range(5): pulled.append(i); yield i
p = PeekingIterator(gen())
assert pulled == [0]                     # constructor pulled exactly one element
p.peek(); p.peek(); assert pulled == [0]  # peeking never advances
p.next(); assert pulled == [0, 1]
print('elements pulled so far:', pulled)

# edge cases: None and falsy values are legitimate elements (sentinel is a private object)
p = PeekingIterator(iter([None, 0, '']))
assert p.hasNext() and p.next() is None and p.next() == 0 and p.next() == '' and not p.hasNext()
p = PeekingIterator(iter([]))
assert not p.hasNext()
p = PeekingIterator(iter([4])); assert p.next() == 4 and not p.hasNext()
print('edge asserts ok')
