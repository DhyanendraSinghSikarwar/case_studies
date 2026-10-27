import random
import sys
from bisect import bisect_left, bisect_right, insort_left, insort_right

assert sys.version_info >= (3, 10), "key= needs Python 3.10+"
print("python", sys.version_info.major, sys.version_info.minor)

age = lambda t: t[1]
people = [('ann', 22), ('bob', 30), ('cy', 30), ('di', 41)]

# (a) count people younger than 30: x is a plain age, key is applied to the LIST ELEMENTS only
a = bisect_left(people, 30, key=age)
print("(a)", a)
assert a == 1 == sum(1 for p in people if p[1] < 30)

# (b) insert ('zed', 30) after the existing age-30 entries: insort applies key to x too, but inserts x itself
b = list(people)
insort_right(b, ('zed', 30), key=age)
print("(b)", b)
assert b == [('ann', 22), ('bob', 30), ('cy', 30), ('zed', 30), ('di', 41)]

# (c) binary search on the answer: smallest v in 0..99 with v*v >= 50
c = bisect_left(range(100), 50, key=lambda v: v * v)
print("(c)", c)
assert c == 8 == next(v for v in range(100) if v * v >= 50)

# where key is NOT applied: passing a whole tuple as x to bisect_left compares 30 (key of element) with a tuple
try:
    bisect_left(people, ('zed', 30), key=age)
except TypeError as e:
    print("bisect_left with a tuple x ->", type(e).__name__)
# insort_left, by contrast, applies key to x as well, so the tuple is fine and goes BEFORE the age-30 entries
d = list(people)
insort_left(d, ('zed', 30), key=age)
print("insort_left puts it first among age 30:", d)
assert d[1] == ('zed', 30)
# bisect_right on a plain age behaves like upper bound
assert bisect_right(people, 30, key=age) == 3 and bisect_right(people, 5, key=age) == 0 and bisect_right(people, 99, key=age) == 4

# pre-3.10 workaround: a parallel list of keys that is kept in step with the data
keys = [p[1] for p in people]
assert bisect_left(keys, 30) == a
pk, pd = list(keys), list(people)
i = bisect_right(pk, 30)
pk.insert(i, 30)
pd.insert(i, ('zed', 30))
assert pd == b, "parallel-list workaround gives the same list"
print("parallel-key workaround matches:", pd == b)

# seeded randomised cross-check against linear scans
rng = random.Random(28)
for _ in range(2000):
    lst = sorted(((rng.choice('abcdef'), rng.randint(15, 45)) for _ in range(rng.randint(0, 12))), key=age)
    x = rng.randint(10, 50)
    assert bisect_left(lst, x, key=age) == sum(1 for p in lst if p[1] < x)
    assert bisect_right(lst, x, key=age) == sum(1 for p in lst if p[1] <= x)
    new = ('n', x)
    r1 = list(lst); insort_right(r1, new, key=age)
    assert [p[1] for p in r1] == sorted(p[1] for p in lst + [new])
    assert r1[bisect_right(lst, x, key=age)] == new          # landed after all equal ages
print("random check passed: 2000 cases")

# edge cases
assert bisect_left([], 5, key=age) == 0
assert bisect_left(range(100), 0, key=lambda v: v * v) == 0 and bisect_left(range(100), 10 ** 9, key=lambda v: v * v) == 100
print("edge asserts passed")
