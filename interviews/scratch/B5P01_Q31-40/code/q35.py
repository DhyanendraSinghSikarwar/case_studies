import random
from collections import Counter


class RandomizedSet:
    """list holds the elements densely; dict maps value -> index in that list."""

    def __init__(self, rng=None):
        self.items = []
        self.pos = {}
        self.rng = rng or random

    def insert(self, x):
        if x in self.pos:
            return False
        self.pos[x] = len(self.items)
        self.items.append(x)
        return True

    def remove(self, x):
        if x not in self.pos:
            return False
        i = self.pos[x]
        last = self.items[-1]
        self.items[i] = last          # move last element into the hole
        self.pos[last] = i            # update ITS index first ...
        self.items.pop()
        del self.pos[x]               # ... then delete x (order matters when x is last)
        return True

    def get_random(self):
        return self.items[self.rng.randrange(len(self.items))]


class BruteSet:
    """Reference with O(n) operations."""

    def __init__(self):
        self.items = []

    def insert(self, x):
        if x in self.items:
            return False
        self.items.append(x)
        return True

    def remove(self, x):
        if x not in self.items:
            return False
        self.items.remove(x)
        return True


# Prompt example
s = RandomizedSet(random.Random(35))
print(s.insert(1), s.insert(2), s.remove(1), "getRandom x5 ->", [s.get_random() for _ in range(5)])
assert all(s.get_random() == 2 for _ in range(50))

# Removing the LAST element (the classic bug if you delete before re-pointing)
s = RandomizedSet(random.Random(1))
for v in (10, 20, 30):
    s.insert(v)
assert s.remove(30) and s.items == [10, 20] and s.pos == {10: 0, 20: 1}
assert s.remove(10) and s.items == [20] and s.pos == {20: 0}
assert s.remove(20) and s.items == [] and s.pos == {}
assert not s.remove(20) and not s.remove(99)
assert s.insert(20) and not s.insert(20)
print("last-element removal and re-insert OK")

# Buggy variant: pop the list and delete the key BEFORE re-pointing the moved element
class Buggy(RandomizedSet):
    def remove(self, x):
        if x not in self.pos:
            return False
        i = self.pos.pop(x)
        last = self.items.pop()
        if i < len(self.items):
            self.items[i] = last
        self.pos[last] = i          # when x was last, this re-adds x with a stale index
        return True
b = Buggy()
b.insert(1); b.insert(2)
b.remove(2)
print("buggy remove-last leaves pos =", b.pos, "items =", b.items, "(ghost key 2)")
assert 2 in b.pos and b.items == [1]

# Seeded randomised cross-check of membership semantics against the O(n) reference
rng = random.Random(350)
for trial in range(300):
    fast, ref = RandomizedSet(random.Random(trial)), BruteSet()
    for _ in range(60):
        op = rng.choice(["i", "i", "r", "g"])
        x = rng.randint(0, 9)
        if op == "i":
            assert fast.insert(x) == ref.insert(x)
        elif op == "r":
            assert fast.remove(x) == ref.remove(x)
        elif ref.items:
            assert fast.get_random() in ref.items
        assert sorted(fast.items) == sorted(ref.items)
        assert all(fast.items[i] == v for v, i in fast.pos.items())
        assert len(fast.pos) == len(fast.items)
print("cross-check passed: 300 random op sequences (18,000 ops)")

# Uniformity check (seeded): 4 elements, 40,000 draws, each should be near 10,000
s = RandomizedSet(random.Random(7))
for v in (5, 6, 7, 8):
    s.insert(v)
s.remove(6); s.insert(9)
c = Counter(s.get_random() for _ in range(30000))
print("draw counts over {5,7,8,9}:", dict(sorted(c.items())))
assert set(c) == {5, 7, 8, 9} and all(abs(v - 7500) < 400 for v in c.values())
