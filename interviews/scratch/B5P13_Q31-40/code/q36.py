import random

random.seed(3601)


def solve(cases):
    out = []
    for c in cases:
        try:
            plain = sorted(c)
        except TypeError:
            plain = "TypeError"
        try:
            none_last = sorted(c, key=lambda v: (v is None, v))
        except TypeError:
            none_last = "TypeError"
        out.append([plain, none_last])
    return out


def ins_sort(c, key=None):
    """Oracle: insertion sort that uses ONLY the < operator (like list.sort does)."""
    k = key or (lambda v: v)
    a = []
    for v in c:
        j = len(a)
        while j > 0 and k(v) < k(a[j - 1]):
            j -= 1
        a.insert(j, v)
    return a


def brute(cases):
    out = []
    for c in cases:
        row = []
        for key in (None, lambda v: (v is None, v)):
            try:
                row.append(ins_sort(c, key))
            except TypeError:
                row.append("TypeError")
        out.append(row)
    return out


cases = [[3, 1, 2], [1, "a"], [None, 3, 1], [None], [(1, "a"), (2, None)], [(1, "a"), (1, None)], [True, 2, 1.5], [None, None]]
want = [[[1, 2, 3], [1, 2, 3]], ["TypeError", "TypeError"], ["TypeError", [1, 3, None]], [[None], [None]],
        [[(1, "a"), (2, None)], [(1, "a"), (2, None)]], ["TypeError", "TypeError"], [[True, 1.5, 2], [True, 1.5, 2]],
        ["TypeError", [None, None]]]
got = solve(cases)
assert got == want == brute(cases)
for c, g in zip(cases, got):
    print(f"{str(c):<28} plain={g[0]!s:<22} none_last={g[1]}")

# the exact messages (3.13 wording is what you see here)
for expr in ("1 < 'a'", "None < 1", "None < None", "(1, 'a') < (1, None)", "(1, 'a') < (2, None)", "[1, 'a'] < [1, 2]"):
    try:
        print(f"{expr:<22} ->", eval(expr))
    except TypeError as e:
        print(f"{expr:<22} -> TypeError: {e}")
print("1 == 1.0 == True:", 1 == 1.0 == True, "| True < 1.5:", True < 1.5, "| 2 > True:", 2 > True)

# tuple/list comparison uses == to find the first differing position, then < only there
class Loud:
    def __init__(self, n): self.n = n
    def __eq__(self, o): print(f"   == {self.n},{o.n}"); return self.n == o.n
    def __lt__(self, o): print(f"   <  {self.n},{o.n}"); return self.n < o.n
print("(Loud(1), Loud(5)) < (Loud(1), Loud(9)):")
print("  result", (Loud(1), Loud(5)) < (Loud(1), Loud(9)))

# 0 or 1 items never compare anything
class Boom:
    def __lt__(self, o): raise AssertionError("compared")
assert sorted([]) == [] and sorted([Boom()]) and True
print("sorted([]) and sorted([Boom()]) made no comparison")

# claim: any list with a str and a number (2+ items) raises in plain sort, whatever the order; None with a number too
rng = random.Random(36)
pool = [1, 2, 1.5, True, "a", "b", None]
for _ in range(3000):
    lst = [rng.choice(pool) for _ in range(rng.randint(0, 6))]
    has_str = any(isinstance(v, str) for v in lst)
    has_num = any(isinstance(v, (int, float)) for v in lst)
    has_none = any(v is None for v in lst)
    kinds = has_str + has_num + has_none
    try:
        sorted(lst)
        raised = False
    except TypeError:
        raised = True
    if kinds >= 2:
        assert raised, lst           # a total order must connect the groups, so some cross-type '<' happens
    assert (len(lst) >= 2 and has_none and len([v for v in lst if v is None]) == len(lst)) <= raised
print("3000 seeded mixed lists: two kinds among {str, number, None} always raises; an all-None list of 2+ raises")

# the none-last key
assert sorted([3, None, 1, None, 2], key=lambda v: (v is None, v)) == [1, 2, 3, None, None]
assert (False, 1) < (True, None)       # decided by the first slot, so None is never compared with a number

# seeded random cross-check of solve against the insertion-sort oracle
def pick(rng):
    k = rng.randint(0, 3)
    if k == 0: return [rng.choice([None, 1, 2, 3, 1.5, True]) for _ in range(rng.randint(0, 6))]
    if k == 1: return [rng.choice("abc") for _ in range(rng.randint(0, 6))]
    if k == 2: return [rng.choice([(1, "a"), (1, None), (2, None), (1, 2), (2, "b")]) for _ in range(rng.randint(0, 5))]
    return [rng.choice(pool + [(1, "a"), [1, 2]]) for _ in range(rng.randint(0, 5))]
rng = random.Random(3602)
diff = 0
for _ in range(2000):
    cs = [pick(rng) for _ in range(rng.randint(1, 20))]
    s, b = solve(cs), brute(cs)
    for x, y in zip(s, b):
        if x != y:
            diff += 1
print("2000 seeded batches compared with the insertion-sort oracle, differing rows:", diff)
assert diff == 0

# edge cases
assert solve([[]]) == [[[], []]] and solve([[None, None, None]]) == [["TypeError", [None, None, None]]]
assert solve([[(1, None), (1, None)]]) == [[[(1, None), (1, None)], [(1, None), (1, None)]]]   # equal tuples: == only
print("edge asserts ok")
