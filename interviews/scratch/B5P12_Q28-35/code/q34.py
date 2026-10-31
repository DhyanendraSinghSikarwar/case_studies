import random

MAX_LEVEL = 16


class Node:
    __slots__ = ("key", "next")

    def __init__(self, key, level):
        self.key = key
        self.next = [None] * level          # next[i] = successor on level i (0 = bottom, holds every key)


class SkipList:
    """Ordered set of ints. A new node gets level 1, plus one more level per fair coin flip, up to 16."""

    def __init__(self, seed=0, level_fn=None):
        self.rng = random.Random(seed)
        self.level_fn = level_fn             # test hook: force levels (e.g. always 1 = plain linked list)
        self.head = Node(None, MAX_LEVEL)    # sentinel with all 16 levels
        self.steps = 0                       # nodes stepped onto while searching (for the O(log n) vs O(n) demo)

    def _random_level(self):
        if self.level_fn:
            return self.level_fn()
        lvl = 1
        while lvl < MAX_LEVEL and self.rng.random() < 0.5:
            lvl += 1
        return lvl

    def _path(self, x):
        """Start on the top level, move right while the next key is < x, then drop one level. Returns the
        last node before x on every level."""
        update = [None] * MAX_LEVEL
        cur = self.head
        for i in range(MAX_LEVEL - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].key < x:
                cur = cur.next[i]
                self.steps += 1
            update[i] = cur
        return update

    def contains(self, x):
        nxt = self._path(x)[0].next[0]
        return nxt is not None and nxt.key == x

    def insert(self, x):
        update = self._path(x)
        nxt = update[0].next[0]
        if nxt is not None and nxt.key == x:
            return False
        node = Node(x, self._random_level())
        for i in range(len(node.next)):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node
        return True

    def remove(self, x):
        update = self._path(x)
        node = update[0].next[0]
        if node is None or node.key != x:
            return False
        for i in range(len(node.next)):
            update[i].next[i] = node.next[i]
        return True

    def levels(self):
        """Keys on each level, bottom first, for printing."""
        out = []
        for i in range(MAX_LEVEL):
            row, cur = [], self.head.next[i]
            while cur is not None:
                row.append(cur.key)
                cur = cur.next[i]
            if not row:
                break
            out.append(row)
        return out


def run(ops, seed=0, level_fn=None):
    sl = SkipList(seed, level_fn)
    return [getattr(sl, name)(x) for name, x in ops], sl


def brute(ops):
    s, out = set(), []
    for name, x in ops:
        if name == "insert":
            out.append(x not in s)
            s.add(x)
        elif name == "contains":
            out.append(x in s)
        else:
            out.append(x in s)
            s.discard(x)
    return out


# dry run, first example, with the tower shape after every op
ex = [["insert", 3], ["insert", 1], ["contains", 3], ["remove", 3], ["contains", 3], ["insert", 1]]
sl = SkipList(seed=7)
for name, x in ex:
    r = getattr(sl, name)(x)
    print(f"{name:8} {x}: {r!s:5} levels (bottom first): {sl.levels()}")

for ops, want in [(ex, [True, True, True, True, False, False]), ([["remove", 5]], [False]),
                  ([["insert", -2], ["insert", -2], ["remove", -2], ["remove", -2]], [True, False, True, False])]:
    got, _ = run(ops)
    assert got == want == brute(ops), (ops, got)
    print(ops, "->", got)

# results never depend on the coin flips: seeds 0..5 and forced levels (all 1, all 16) agree with a set
random.seed(3401)
for _ in range(300):
    ops = [[random.choice(["insert", "contains", "remove"]), random.randint(-12, 12)] for _ in range(random.randint(1, 60))]
    want = brute(ops)
    for seed in range(6):
        assert run(ops, seed)[0] == want
    assert run(ops, level_fn=lambda: 1)[0] == want and run(ops, level_fn=lambda: 16)[0] == want
    lv = run(ops)[1].levels()
    assert not lv or lv[0] == sorted(set(lv[0])), "bottom level is sorted, no repeats"
print("300 seeded random op lists: same results for 6 seeds and for forced level 1 and 16, equal to a set")

# speed depends on the levels: 2000 inserts in increasing order, then 2000 lookups
keys = list(range(2000))
for name, fn in [("random levels", None), ("all level 1 (a sorted linked list)", lambda: 1)]:
    sl = SkipList(seed=1, level_fn=fn)
    for k in keys:
        sl.insert(k)
    sl.steps = 0
    for k in keys:
        sl.contains(k)
    print(f"{name}: average nodes stepped onto per lookup = {sl.steps / len(keys):.1f}")

# edge asserts
sl = SkipList()
assert sl.insert(0) and not sl.insert(0) and sl.contains(0) and sl.remove(0) and not sl.remove(0) and not sl.contains(0)
assert all(sl.insert(x) for x in (10**6, -10**6, 0)) and sl.levels()[0] == [-10**6, 0, 10**6]
print("edge asserts ok")
