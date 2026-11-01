import bisect
import itertools
import random

random.seed(1313)

def weighted_pick(w, rs):
    """Inclusive prefix sums once, then bisect_right per pick: first index whose prefix sum is > r."""
    pre = list(itertools.accumulate(w))
    total = pre[-1]
    picks = [bisect.bisect_right(pre, r) for r in rs]
    # counts[i] = how many r in 0..total-1 land on i (loop over r only for the check; real pick is O(log n))
    counts = [0] * len(w)
    for r in range(total):
        counts[bisect.bisect_right(pre, r)] += 1
    return [picks, counts]

def brute(w, rs):
    """Linear scan: subtract weights one by one until r falls inside a block."""
    def pick(r):
        for i, x in enumerate(w):
            if r < x:
                return i
            r -= x
    counts = [0] * len(w)
    for r in range(sum(w)):
        counts[pick(r)] += 1
    return [[pick(r) for r in rs], counts]

examples = [
    ([1, 3], [0, 1, 2, 3], [[0, 1, 1, 1], [1, 3]]),
    ([5], [0, 4], [[0, 0], [5]]),
    ([2, 1, 3], [0, 1, 2, 3, 5], [[0, 0, 1, 2, 2], [2, 1, 3]]),
]
for w, rs, exp in examples:
    got = weighted_pick(w, rs)
    print(w, rs, '->', got)
    assert got == exp and brute(w, rs) == exp

# why bisect_left is wrong for r in 0..total-1: boundary values go to the previous index
w = [2, 1, 3]
pre = list(itertools.accumulate(w))
left = [0] * 3
for r in range(sum(w)):
    left[bisect.bisect_left(pre, r)] += 1
print('prefix', pre, 'bisect_left counts', left, '(want', w, ')')
assert left != w and left == [3, 1, 2]

# if r is drawn from 1..total instead, bisect_left is the right one
alt = [0] * 3
for r in range(1, sum(w) + 1):
    alt[bisect.bisect_left(pre, r)] += 1
assert alt == w
print('r in 1..total with bisect_left gives', alt)

# seeded random cross-check against the linear scan
for _ in range(300):
    w = [random.randint(1, 6) for _ in range(random.randint(1, 6))]
    rs = [random.randrange(sum(w)) for _ in range(random.randint(0, 10))]
    assert weighted_pick(w, rs) == brute(w, rs) and weighted_pick(w, rs)[1] == w
print('random cross-check ok: 300 cases (counts == w every time)')

# maximum size: n = 10^4, sum <= 10^6; one prefix build, picks cost O(log n) each
w = [random.randint(1, 100) for _ in range(10 ** 4)]
assert sum(w) <= 10 ** 6
pre = list(itertools.accumulate(w))
assert bisect.bisect_right(pre, 0) == 0 and bisect.bisect_right(pre, sum(w) - 1) == len(w) - 1
print('max size ok: n =', len(w), 'total =', sum(w))

# edge asserts
assert weighted_pick([1], [0]) == [[0], [1]]
assert weighted_pick([1, 1, 1], [0, 1, 2])[0] == [0, 1, 2]
assert weighted_pick([4, 1], [3, 4])[0] == [0, 1]       # r = 3 is the last value of block 0, r = 4 the first of block 1
print('edge asserts ok')
