import random
from collections import defaultdict

class NaiveFreqStack:                    # brute force: scan the whole stack on every pop, O(n)
    def __init__(self): self.s = []
    def push(self, x): self.s.append(x)
    def pop(self):
        cnt = {}
        for v in self.s: cnt[v] = cnt.get(v, 0) + 1
        best = max(cnt.values())
        for i in range(len(self.s) - 1, -1, -1):      # topmost occurrence among the most frequent values
            if cnt[self.s[i]] == best: return self.s.pop(i)

class FreqStack:
    def __init__(self):
        self.count = defaultdict(int)    # value -> current count
        self.stacks = defaultdict(list)  # f -> values in the order their count reached f
        self.max_freq = 0
    def push(self, x):
        self.count[x] += 1
        f = self.count[x]
        self.stacks[f].append(x)         # x now sits on stack 1..f (one entry per level)
        if f > self.max_freq: self.max_freq = f
    def pop(self):
        x = self.stacks[self.max_freq].pop()
        self.count[x] -= 1
        if not self.stacks[self.max_freq]: self.max_freq -= 1
        return x

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[], ops=[['push', [5]], ['push', [7]], ['push', [5]], ['push', [7]], ['push', [4]], ['push', [5]],
                        ['pop', []], ['pop', []], ['pop', []], ['pop', []]])
want = [None, None, None, None, None, None, 5, 7, 5, 4]
assert run(FreqStack, **ex) == want == run(NaiveFreqStack, **ex)
print('example ->', run(FreqStack, **ex))

random.seed(13)
for case in range(800):
    ops = []; size = 0
    for _ in range(random.randint(0, 50)):
        if size and random.random() < 0.4: ops.append(['pop', []]); size -= 1
        else: ops.append(['push', [random.randint(0, 4)]]); size += 1
    assert run(FreqStack, [], ops) == run(NaiveFreqStack, [], ops), ops
print('800 random sequences match the naive reference')

# one value on several stacks
f = FreqStack()
for x in [5, 5, 5, 7]: f.push(x)
assert [i for i in (1, 2, 3) if 5 in f.stacks[i]] == [1, 2, 3] and f.stacks[1] == [5, 7]
print('stacks after 5,5,5,7:', {k: v for k, v in sorted(f.stacks.items())})

# edge cases
f = FreqStack(); f.push(9); assert f.pop() == 9 and f.max_freq == 0
f = FreqStack()
for x in [1, 2, 3]: f.push(x)
assert [f.pop(), f.pop(), f.pop()] == [3, 2, 1]               # all frequency 1: plain LIFO
f = FreqStack()
for x in [2, 2, 2]: f.push(x)
assert [f.pop(), f.pop(), f.pop()] == [2, 2, 2]
f = FreqStack()
for x in [1, 1, 2, 2]: f.push(x)
assert f.pop() == 2 and f.pop() == 1 and f.pop() == 2 and f.pop() == 1   # tie at freq 2: 2 was pushed last
assert run(FreqStack, [], []) == []
print('edge asserts ok')
