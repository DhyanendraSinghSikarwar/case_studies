import random

random.seed(5)

def merge(intervals):
    out = []
    for s, e in sorted(intervals):                      # by start, then end
        if out and s <= out[-1][1]:                     # closed: touching (s == last end) merges
            out[-1][1] = max(out[-1][1], e)             # max, so a contained interval cannot shrink it
        else:
            out.append([s, e])                          # fresh list: caller's input is untouched
    return out

def merge_buggy(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = e                              # BUG: overwrites with e even when e is smaller
        else:
            out.append([s, e])
    return out

def merge_brute(intervals):
    """Mark every covered point on a doubled grid (so the gap between 4 and 5 is visible), then read runs."""
    pts = set()
    for s, e in intervals:
        pts.update(range(2 * s, 2 * e + 1))
    out, cur = [], None
    for p in sorted(pts):
        if cur and p == cur[1] + 1:
            cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[a // 2, b // 2] for a, b in out]

assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge([[1, 4], [4, 5]]) == [[1, 5]]
assert merge([[1, 4], [0, 4]]) == [[0, 4]]
assert merge([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]
assert merge([[3, 3]]) == [[3, 3]]
assert merge([[1, 4], [5, 6]]) == [[1, 4], [5, 6]]   # integers 4 and 5 are different points: NOT merged

for _ in range(3000):
    n = random.randint(1, 7)
    iv = []
    for _ in range(n):
        s = random.randint(0, 12)
        iv.append([s, random.randint(s, 12)])
    snap = [list(x) for x in iv]
    assert merge(iv) == merge_brute(iv), iv
    assert iv == snap                                   # input untouched
print('3000 random cases ok')

print('buggy on [[1,10],[2,3],[4,5]]:', merge_buggy([[1, 10], [2, 3], [4, 5]]), '(shrunk the end, wrong)')
# sort key note: sorted() on lists compares start then end; duplicates and ties are fine
print('merge of 3 equal points:', merge([[2, 2], [2, 2], [2, 2]]))
# a sorted() on tuples of mixed types would raise TypeError; ints only here
try:
    sorted([[1, 'a'], [1, 2]])
except TypeError as e:
    print('TypeError on tied start with mixed ends:', e)
