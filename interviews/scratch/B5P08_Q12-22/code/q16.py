import itertools
import random

random.seed(16)

def erase_overlap(intervals):                          # sort by END, keep when start >= last kept end
    kept = 0
    last_end = None
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if last_end is None or s >= last_end:          # half-open: touching is fine
            kept += 1
            last_end = e
    return len(intervals) - kept

def max_non_overlapping(intervals):                    # activity selection size
    return len(intervals) - erase_overlap(intervals)

def overlap(a, b):                                     # half-open [s, e)
    return a[0] < b[1] and b[0] < a[1]

def brute(intervals):                                  # try every subset (n <= 10)
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        sel = [intervals[i] for i in range(n) if mask >> i & 1]
        if all(not overlap(a, b) for a, b in itertools.combinations(sel, 2)):
            best = max(best, len(sel))
    return n - best

def by_start(intervals):                               # WRONG greedy: sort by start
    kept = 0
    last_end = None
    for s, e in sorted(intervals):
        if last_end is None or s >= last_end:
            kept += 1
            last_end = e
    return len(intervals) - kept

for iv, exp in [([[1, 2], [2, 3], [3, 4], [1, 3]], 1), ([[1, 2], [1, 2], [1, 2]], 2),
                ([[1, 2], [2, 3]], 0), ([[1, 100], [11, 22], [1, 11], [2, 12]], 2)]:
    assert erase_overlap(iv) == brute(iv) == exp
    print(iv, '->', erase_overlap(iv))

# exhaustive: all multisets of up to 4 intervals with endpoints in 0..4 (10 possible intervals)
pool = [[a, b] for a in range(5) for b in range(a + 1, 5)]
cnt = 0
for k in range(1, 5):
    for combo in itertools.combinations_with_replacement(pool, k):
        iv = [list(x) for x in combo]
        assert erase_overlap(iv) == brute(iv), iv
        assert erase_overlap(iv[::-1]) == erase_overlap(iv)          # input order does not matter
        cnt += 1
print('exhaustive ok:', cnt, 'multisets')

for _ in range(500):
    n = random.randint(1, 10)
    iv = []
    for _ in range(n):
        a = random.randint(-8, 8)
        iv.append([a, random.randint(a + 1, a + 6)])
    assert erase_overlap(iv) == brute(iv)
    assert max_non_overlapping(iv) == len(iv) - brute(iv)
print('random ok: 500 inputs')

# counter-example for sort-by-start
cx = [[1, 10], [2, 3], [4, 5]]
print('sort by start on', cx, '->', by_start(cx), '(wrong); by end ->', erase_overlap(cx), '; brute ->', brute(cx))
assert by_start(cx) == 2 and erase_overlap(cx) == 1 == brute(cx)
bad = 0
for combo in itertools.combinations_with_replacement(pool, 3):
    iv = [list(x) for x in combo]
    bad += by_start(iv) != erase_overlap(iv)
print('3-interval multisets where sort-by-start is wrong:', bad)
assert bad > 0

# edge cases and a large input
assert erase_overlap([[0, 1]]) == 0
assert erase_overlap([[-50000, 50000], [-50000, -49999]]) == 1
assert erase_overlap([[1, 2], [2, 3], [3, 4]]) == 0               # touching endpoints do not overlap
assert erase_overlap([[1, 3], [1, 3]]) == 1
big = [[i, i + 2] for i in range(-50000, 49998)]                  # chain of overlaps, n about 10^5
assert erase_overlap(big) == len(big) - ((len(big) + 1) // 2)
print('edge cases ok; big n =', len(big))
