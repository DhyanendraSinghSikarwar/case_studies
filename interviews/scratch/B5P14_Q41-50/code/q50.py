import random
random.seed(50)

def calendar_k(bookings):
    xs = sorted({x for s, e in bookings for x in (s, e)})
    pos = {x: i for i, x in enumerate(xs)}
    m = len(xs) - 1                           # elementary cells [xs[k], xs[k+1])
    mx = [0] * (4 * m); lz = [0] * (4 * m)    # mx[o] = best overlap inside o, INCLUDING o's own lz

    def add(o, lo, hi, l, r):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            mx[o] += 1; lz[o] += 1; return
        mid = (lo + hi) // 2
        add(2 * o, lo, mid, l, r); add(2 * o + 1, mid + 1, hi, l, r)
        mx[o] = max(mx[2 * o], mx[2 * o + 1]) + lz[o]     # no push-down: the tag stays here

    out = []
    for s, e in bookings:
        add(1, 0, m - 1, pos[s], pos[e] - 1)  # cells from s up to (not including) e
        out.append(mx[1])
    return out

def oracle(bookings):                         # recompute from scratch after every booking
    out = []
    for k in range(1, len(bookings) + 1):
        pts = sorted({x for s, e in bookings[:k] for x in (s, e)})
        out.append(max(sum(1 for s, e in bookings[:k] if s <= x < e) for x in pts))
    return out

assert calendar_k([[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]) == [1, 1, 2, 3, 3, 3]
assert calendar_k([[0, 5], [5, 10], [0, 10]]) == [1, 1, 2]
print('examples ok')

for _ in range(600):
    n = random.randint(1, 10)
    bk = []
    for _ in range(n):
        s = random.randint(0, 14); bk.append([s, random.randint(s + 1, 15)])
    assert calendar_k(bk) == oracle(bk), bk
print('600 random booking lists match the recompute-from-scratch oracle')

assert calendar_k([[0, 1]]) == [1]
assert calendar_k([[3, 7]] * 4) == [1, 2, 3, 4]                       # identical bookings
assert calendar_k([[0, 5], [5, 10], [10, 15]]) == [1, 1, 1]           # touching never overlaps
assert calendar_k([[0, 10**9], [0, 1], [10**9 - 1, 10**9]]) == [1, 2, 2]
bk = [[random.randint(0, 5 * 10**8), 0] for _ in range(400)]
for b in bk: b[1] = b[0] + random.randint(1, 5 * 10**8)
res = calendar_k(bk)
assert res == oracle(bk) and res == sorted(res)
print('400 bookings with endpoints up to 10^9 ok; answers never decrease, final max', res[-1])
print('first example:', calendar_k([[10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]))
