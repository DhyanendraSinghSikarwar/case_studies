import random
from bisect import bisect_left, bisect_right

random.seed(6)

def insert_interval(intervals, new):
    out, i, n = [], 0, len(intervals)
    s, e = new
    while i < n and intervals[i][1] < s:                # phase 1: strictly before new (touching is NOT before)
        out.append(list(intervals[i])); i += 1
    while i < n and intervals[i][0] <= e:               # phase 2: overlaps or touches new
        s = min(s, intervals[i][0]); e = max(e, intervals[i][1]); i += 1
    out.append([s, e])
    while i < n:                                        # phase 3: strictly after
        out.append(list(intervals[i])); i += 1
    return out

def insert_bisect(intervals, new):
    """Binary search finds the window in O(log n), but the slice copies are still O(n)."""
    starts = [x[0] for x in intervals]                  # O(n) to build; a persistent list would avoid it
    ends = [x[1] for x in intervals]
    lo = bisect_left(ends, new[0])                      # first interval whose end >= new start
    hi = bisect_right(starts, new[1])                   # first interval whose start > new end
    s, e = new
    if lo < hi:
        s, e = min(s, intervals[lo][0]), max(e, intervals[hi - 1][1])
    return [list(x) for x in intervals[:lo]] + [[s, e]] + [list(x) for x in intervals[hi:]]

def brute(intervals, new):
    pts = set()
    for s, e in list(intervals) + [new]:
        pts.update(range(2 * s, 2 * e + 1))
    out, cur = [], None
    for p in sorted(pts):
        if cur and p == cur[1] + 1: cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[a // 2, b // 2] for a, b in out]

for fn in (insert_interval, insert_bisect):
    assert fn([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert fn([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert fn([], [5, 7]) == [[5, 7]]
    assert fn([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]
    assert fn([[1, 5]], [5, 6]) == [[1, 6]]
    assert fn([[1, 5]], [0, 0]) == [[0, 0], [1, 5]]           # new before everything
    assert fn([[1, 5], [7, 8]], [0, 20]) == [[0, 20]]         # swallows everything

def random_disjoint(rng):
    out, x = [], rng.randint(0, 2)
    for _ in range(rng.randint(0, 5)):
        s = x; e = s + rng.randint(0, 3)
        out.append([s, e]); x = e + rng.randint(1, 3)         # gap >= 1: disjoint closed intervals do not touch
    return out

for _ in range(3000):
    iv = random_disjoint(random)
    s = random.randint(0, 20); new = [s, random.randint(s, 21)]
    want = brute(iv, new)
    assert insert_interval(iv, new) == want == insert_bisect(iv, new), (iv, new)
print('3000 random cases ok')

# the common bug: using < instead of <= in phase 2 misses a touching interval
def buggy(intervals, new):
    out, i, n = [], 0, len(intervals); s, e = new
    while i < n and intervals[i][1] < s: out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] < e: s = min(s, intervals[i][0]); e = max(e, intervals[i][1]); i += 1
    out.append([s, e]); out += intervals[i:]
    return out
print('buggy (< not <=) on [[6,7]] + [5,6]:', buggy([[6, 7]], [5, 6]), '(should be [[5, 7]])')
