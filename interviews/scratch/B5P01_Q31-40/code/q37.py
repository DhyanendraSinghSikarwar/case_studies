import sys

# 1. Insertion order and the reinsert example from the prompt
d = {1: 'a', 2: 'b'}
del d[1]
d[1] = 'a'
print("1) after delete + reinsert of 1:", list(d))
assert list(d) == [2, 1]
d2 = {1: 'a', 2: 'b'}
d2[1] = 'z'                                   # updating an existing key keeps its slot
print("   update in place keeps position:", list(d2))
assert list(d2) == [1, 2]
print("   popitem is LIFO:", {1: 'a', 2: 'b', 3: 'c'}.popitem())

# 2. Resize behaviour: getsizeof jumps in steps; growth is geometric, so inserts are amortised O(1)
d, last, jumps = {}, sys.getsizeof({}), []
for i in range(200):
    d[i] = i
    s = sys.getsizeof(d)
    if s != last:
        jumps.append((len(d), s))
        last = s
print("2) (len when the table grew, getsizeof bytes):", jumps)
assert len(jumps) < 12                         # ~10 resizes for 200 keys, not 200
assert jumps[-1][0] < 200

# 3. Hashable and consistent with equality
for bad in ([1], {1}, {'a': 1}):
    try:
        {bad: 1}
    except TypeError as e:
        print("3) unhashable key:", type(bad).__name__, "->", e)
print("   1, 1.0 and True are one key:", {1: 'x', 1.0: 'y', True: 'z'})
assert {1: 'x', 1.0: 'y', True: 'z'} == {1: 'z'}


class OnlyEq:
    def __eq__(self, other):
        return True
print("   defining __eq__ alone sets __hash__ to", OnlyEq.__hash__)
assert OnlyEq.__hash__ is None


class Bad:                                     # hash NOT consistent with equality
    def __init__(self, v): self.v = v
    def __eq__(self, o): return self.v == o.v
    def __hash__(self): return id(self)
s = {Bad(1)}
print("   equal objects, different hashes -> Bad(1) in {Bad(1)}:", Bad(1) in s)
assert Bad(1) not in s


class Mut:                                     # mutating a key changes its hash: lost entry
    def __init__(self, v): self.v = v
    def __eq__(self, o): return self.v == o.v
    def __hash__(self): return hash(self.v)
m = Mut(1)
dm = {m: 'x'}
m.v = 2
print("   after mutating the key, lookup by the same object:", m in dm, "| len still", len(dm))
assert m not in dm and len(dm) == 1

# 4. Mutating size while iterating
d = {1: 'a', 2: 'b', 3: 'c'}
try:
    for k in d:
        d[k + 10] = 'new'
except RuntimeError as e:
    print("4) add during iteration ->", e)
d = {1: 'a', 2: 'b', 3: 'c'}
try:
    for k in d:
        del d[k]
except RuntimeError as e:
    print("   delete during iteration ->", e)
d = {1: 'a', 2: 'b', 3: 'c'}
for k in d:
    d[k] = d[k].upper()                        # changing a value does not change size: allowed
print("   updating values while iterating is fine:", d)
d = {k: v for k, v in d.items() if k != 2}      # safe pattern: build a new dict
for k in list(d):                               # or iterate over a snapshot
    if k == 1:
        del d[k]
print("   safe patterns leave:", d)
assert d == {3: 'C'}

# 5. Sets use the same hash-table idea but keep no insertion order and no values
print("5) list({3, 1, 2}) =", list({3, 1, 2}), "(slot order of the small-int hashes, not insertion order; never rely on set order)")
print("   the growth points above are 6, 11, 22, 43, 86, 171: each is one past 2/3 of a power-of-two table (5/8, 10/16, 21/32, 42/64, 85/128, 170/256)")
