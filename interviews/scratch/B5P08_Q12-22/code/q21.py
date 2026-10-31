import itertools
import random
from functools import cmp_to_key

random.seed(21)

def min_arrows(points):
    arrows = 0
    shot = None                              # x of the last arrow
    for s, e in sorted(points, key=lambda p: p[1]):      # sort by END
        if shot is None or s > shot:         # the arrow at `shot` misses this balloon (touching is a hit)
            arrows += 1
            shot = e                         # new arrow at this balloon's end
    return arrows

def by_start_naive(points):                  # WRONG: sort by start, never shrink the group's end
    arrows = 0
    end = None
    for s, e in sorted(points):
        if end is None or s > end:
            arrows += 1
            end = e
    return arrows

def by_start_shrinking(points):              # correct variant: sort by start AND shrink end to the min
    arrows = 0
    end = None
    for s, e in sorted(points):
        if end is None or s > end:
            arrows += 1
            end = e
        else:
            end = min(end, e)
    return arrows

def brute(points):                           # smallest set of integer x that hits every balloon (small coordinates)
    lo = min(p[0] for p in points)
    hi = max(p[1] for p in points)
    for r in range(1, len(points) + 1):
        for xs in itertools.combinations(range(lo, hi + 1), r):
            if all(any(s <= x <= e for x in xs) for s, e in points):
                return r

for pts, exp in [([[10, 16], [2, 8], [1, 6], [7, 12]], 2), ([[1, 2], [3, 4], [5, 6], [7, 8]], 4),
                 ([[1, 2], [2, 3], [3, 4], [4, 5]], 2),
                 ([[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]], 2)]:
    assert min_arrows(pts) == brute(pts) == exp
    print(pts, '->', min_arrows(pts))

# exhaustive: every multiset of up to 4 balloons with endpoints in 0..4 (15 possible balloons)
pool = [[a, b] for a in range(5) for b in range(a, 5)]
cnt = naive_bad = 0
for k in range(1, 5):
    for combo in itertools.combinations_with_replacement(pool, k):
        pts = [list(x) for x in combo]
        assert min_arrows(pts) == brute(pts), pts
        assert by_start_shrinking(pts) == min_arrows(pts), pts
        naive_bad += by_start_naive(pts) != min_arrows(pts)
        cnt += 1
print('exhaustive ok:', cnt, 'multisets; naive sort-by-start wrong on', naive_bad)

for _ in range(300):
    pts = []
    for _ in range(random.randint(1, 7)):
        a = random.randint(-6, 6)
        pts.append([a, random.randint(a, a + 5)])
    assert min_arrows(pts) == brute(pts)
print('random ok: 300 inputs')

cx = [[1, 10], [2, 3], [4, 5]]
print('naive sort-by-start on', cx, '->', by_start_naive(cx), '(wrong); correct ->', min_arrows(cx), '; brute ->', brute(cx))
assert by_start_naive(cx) == 1 and min_arrows(cx) == 2 == brute(cx)

# overflow trap: emulate a 32-bit signed subtraction comparator
def wrap32(x):
    return (x + 2 ** 31) % 2 ** 32 - 2 ** 31
def cmp32(a, b):
    return wrap32(a[1] - b[1])               # what a C or Java comparator `a[1] - b[1]` would compute
lo_b, hi_b = [-2 ** 31, -2 ** 31], [2 ** 31 - 1, 2 ** 31 - 1]
print('true a-b:', hi_b[1] - lo_b[1], '| 32-bit a-b:', cmp32(hi_b, lo_b), '(negative: says hi < lo, wrong order)')
bad_order = sorted([hi_b, lo_b], key=cmp_to_key(cmp32))
print('order from 32-bit subtraction comparator:', bad_order, '| correct:', sorted([hi_b, lo_b], key=lambda p: p[1]))
assert cmp32(hi_b, lo_b) < 0 and hi_b[1] - lo_b[1] > 0
big = [[-2 ** 31, 2 ** 31 - 1], [-2 ** 31, -2 ** 31], [2 ** 31 - 1, 2 ** 31 - 1]]
assert min_arrows(big) == 2                  # Python ints: no overflow; sort by key, no subtraction

# edge cases
assert min_arrows([[5, 5]]) == 1
assert min_arrows([[1, 1], [1, 1]]) == 1
assert min_arrows([[1, 5], [5, 9]]) == 1     # touching balloons share the arrow at x = 5
assert min_arrows([[i, i] for i in range(10 ** 5)]) == 10 ** 5
assert min_arrows([[0, 10 ** 9]] * 10 ** 5) == 1
print('edge cases ok')
