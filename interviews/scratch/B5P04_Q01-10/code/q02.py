import random


class BruteMinStack:
    """Reference: a plain list, getMin scans (O(n))."""
    def __init__(self): self.a = []
    def push(self, x): self.a.append(x)
    def pop(self): self.a.pop()
    def top(self): return self.a[-1]
    def getMin(self): return min(self.a)


class MinStack:
    """Parallel stack: mins[i] is the minimum of a[0..i]. O(1) all, O(n) extra."""
    def __init__(self):
        self.a, self.mins = [], []
    def push(self, x):
        self.a.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))
    def pop(self):
        self.a.pop(); self.mins.pop()
    def top(self): return self.a[-1]
    def getMin(self): return self.mins[-1]


class MinStackSparse:
    """Second stack only grows when x <= current min (the <= matters for duplicates)."""
    def __init__(self):
        self.a, self.mins = [], []
    def push(self, x):
        self.a.append(x)
        if not self.mins or x <= self.mins[-1]:
            self.mins.append(x)
    def pop(self):
        if self.a.pop() == self.mins[-1]:
            self.mins.pop()
    def top(self): return self.a[-1]
    def getMin(self): return self.mins[-1]


class MinStackBuggy(MinStackSparse):
    """Same idea with '<' : duplicates of the minimum are not recorded."""
    def push(self, x):
        self.a.append(x)
        if not self.mins or x < self.mins[-1]:
            self.mins.append(x)


class MinStackDiff:
    """One stack of differences x - min_before_push; one variable for the min."""
    def __init__(self):
        self.d, self.m = [], None
    def push(self, x):
        if not self.d:
            self.d.append(0); self.m = x
        else:
            self.d.append(x - self.m)
            if x < self.m:
                self.m = x                    # negative entry marks "new minimum"
    def pop(self):
        diff = self.d.pop()
        if diff < 0:
            self.m -= diff                    # restore the previous minimum
    def top(self):
        diff = self.d[-1]
        return self.m if diff < 0 else self.m + diff
    def getMin(self): return self.m


IMPLS = [MinStack, MinStackSparse, MinStackDiff]

# prompt example
for cls in IMPLS:
    s = cls()
    s.push(-2); s.push(0); s.push(-3)
    assert s.getMin() == -3
    s.pop()
    assert s.top() == 0 and s.getMin() == -2
    s.push(-2); s.push(-2); s.pop()
    assert s.getMin() == -2
print("prompt example passes for", [c.__name__ for c in IMPLS])

# what breaks without duplicate handling
b = MinStackBuggy()
b.push(2); b.push(2); b.pop()
print("buggy ('<') after push 2, push 2, pop: stack holds", b.a, "but mins =", b.mins)
try:
    b.getMin()
except IndexError:
    print("getMin() raised IndexError although 2 is still in the stack")

# edge cases
for cls in IMPLS:
    s = cls()
    s.push(7)
    assert s.top() == 7 and s.getMin() == 7
    s.pop()
    s.push(5); s.push(5); s.push(5)
    s.pop(); s.pop()
    assert s.getMin() == 5 and s.top() == 5          # all equal
    s.push(-2**31); s.push(2**31 - 1)
    assert s.getMin() == -2**31 and s.top() == 2**31 - 1
    s.pop()
    assert s.top() == -2**31

# seeded randomised cross-check against the brute force
rng = random.Random(42)
checked = 0
for _ in range(500):
    impls = [BruteMinStack()] + [c() for c in IMPLS]
    size = 0
    for _ in range(rng.randint(1, 40)):
        if size and rng.random() < 0.4:
            for s in impls: s.pop()
            size -= 1
        else:
            x = rng.randint(-4, 4)               # small range -> many duplicates
            for s in impls: s.push(x)
            size += 1
        if size:
            ref = impls[0]
            for s in impls[1:]:
                assert s.top() == ref.top() and s.getMin() == ref.getMin()
            checked += 1
print("random cross-check passed:", checked, "state checks")
