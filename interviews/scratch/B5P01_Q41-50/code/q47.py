import random
from collections import Counter, defaultdict

class BruteMultiset:                               # list only: remove is O(n)
    def __init__(self, seed=0): self.a, self.rng = [], random.Random(seed)
    def insert(self, x): self.a.append(x); return self.a.count(x) == 1
    def remove(self, x):
        if x not in self.a: return False
        self.a.remove(x); return True
    def getRandom(self): return self.rng.choice(self.a)

class RandomizedCollection:                        # average O(1) for all three operations
    def __init__(self, seed=0):
        self.a = []                                # values, dense, so random index is uniform over elements
        self.pos = defaultdict(set)                # value -> set of indices where it sits in self.a
        self.rng = random.Random(seed)
    def insert(self, x):
        new = not self.pos[x]
        self.pos[x].add(len(self.a)); self.a.append(x)
        return new
    def remove(self, x):
        if not self.pos.get(x): return False
        i = self.pos[x].pop()                      # any slot holding x
        last = len(self.a) - 1
        if i != last:
            y = self.a[last]
            self.pos[y].add(i)                     # add the new slot FIRST ...
            self.pos[y].discard(last)              # ... then drop the old one (works when y == x too)
            self.a[i] = y
        self.a.pop()
        if not self.pos[x]: del self.pos[x]
        return True
    def getRandom(self): return self.rng.choice(self.a)

# prompt example
rc = RandomizedCollection(seed=47)
print("insert 1:", rc.insert(1), "| insert 1:", rc.insert(1), "| insert 2:", rc.insert(2))
print("remove 1:", rc.remove(1), "| remaining list:", sorted(rc.a))
draws = Counter(rc.getRandom() for _ in range(10_000))
print("getRandom over 10,000 draws:", dict(sorted(draws.items())), "(expect about 5000 / 5000)")

# the "last slot" trap: remove a value whose only/last copy is at the end, and a value equal to the last
t = RandomizedCollection()
for v in (5, 7, 7): t.insert(v)
assert t.remove(7) and sorted(t.a) == [5, 7] and t.pos[7] == {t.a.index(7)} and t.pos[5] == {0}
assert t.remove(7) and t.a == [5] and 7 not in t.pos
assert not t.remove(7)

# seeded randomized cross-check against Counter model, with invariant checks
rng = random.Random(471)
for trial in range(300):
    rc, model = RandomizedCollection(trial), Counter()
    for _ in range(60):
        x = rng.randint(0, 4)
        if rng.random() < 0.55:
            assert rc.insert(x) == (model[x] == 0); model[x] += 1
        else:
            assert rc.remove(x) == (model[x] > 0)
            if model[x] > 0: model[x] -= 1
        assert Counter(rc.a) == +model                                   # same multiset
        for v, s in rc.pos.items():
            assert s and all(rc.a[i] == v for i in s) and len(s) == model[v]   # index sets exact
        assert sum(len(s) for s in rc.pos.values()) == len(rc.a)
        if rc.a: assert rc.getRandom() in model and model[rc.getRandom()] > 0
print("300 seeded trials x 60 ops: multiset, index sets and return values all consistent")

# edge cases
e = RandomizedCollection()
assert e.remove(3) is False
assert e.insert(3) is True and e.insert(3) is False
assert e.remove(3) and e.remove(3) and not e.remove(3) and e.a == []
try: e.getRandom(); raise SystemExit("should fail")
except IndexError: print("getRandom on empty raises IndexError (the problem guarantees non-empty)")
print("edge asserts passed")
