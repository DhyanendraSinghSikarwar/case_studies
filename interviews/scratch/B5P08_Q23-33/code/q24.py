import random

def intersect(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if a[i][1] < b[j][1]:          # the one that ends first can never match anything later
            i += 1
        else:
            j += 1
    return out

def brute(a, b):                       # double the coordinates so [0,2] and [3,5] stay apart
    pa, pb = set(), set()
    for s, e in a: pa.update(range(2 * s, 2 * e + 1))
    for s, e in b: pb.update(range(2 * s, 2 * e + 1))
    out, cur = [], None
    for p in sorted(pa & pb):
        if cur and p == cur[1] + 1: cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[x // 2, y // 2] for x, y in out]

def gen(rng):                          # sorted, pairwise disjoint (no shared point) closed intervals
    res, x = [], rng.randint(0, 3)
    for _ in range(rng.randint(0, 6)):
        s = x + rng.randint(0, 3); e = s + rng.randint(0, 4)
        res.append([s, e]); x = e + 1
    return res

assert intersect([[0,2],[5,10],[13,23],[24,25]], [[1,5],[8,12],[15,24],[25,26]]) == [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
assert intersect([[1,3],[5,9]], []) == []
assert intersect([[1,7]], [[3,10]]) == [[3,7]]
assert intersect([[0,2],[3,5]], [[2,3]]) == [[2,2],[3,3]]
assert intersect([], []) == []

rng = random.Random(24)
for _ in range(2000):
    a, b = gen(rng), gen(rng)
    got = intersect(a, b)
    assert got == brute(a, b), (a, b)
    if a and b:
        assert len(got) <= len(a) + len(b) - 1          # output size bound
print("2000 random cases match brute force; output size never above len(a)+len(b)-1")

# a tight case for the size bound: interleaved intervals that all overlap their neighbour
a = [[0, 3], [5, 8]]; b = [[1, 6]]
print("tight example:", intersect(a, b), "len(a)+len(b)-1 =", len(a) + len(b) - 1)
