import heapq
import random

random.seed(43)

def range_brute(lists):
    """Try every pair (a, b) of values; keep the narrowest valid one, smaller a on a tie."""
    vals = sorted({x for l in lists for x in l})
    best = None
    for a in vals:
        for b in vals:
            if b >= a and all(any(a <= x <= b for x in l) for l in lists):
                if best is None or (b - a, a) < (best[1] - best[0], best[0]):
                    best = [a, b]
    return best

def range_heap(lists):
    """Heap of (value, list index, position): one current element per list. The index is unique per list, so ties never
    compare anything unorderable. hi = max of the current elements, tracked as we push."""
    heap = [(l[0], i, 0) for i, l in enumerate(lists)]
    heapq.heapify(heap)
    hi = max(v for v, _, _ in heap)
    best = [heap[0][0], hi]
    while True:
        lo, i, j = heap[0]
        if hi - lo < best[1] - best[0] or (hi - lo == best[1] - best[0] and lo < best[0]):
            best = [lo, hi]
        if j + 1 == len(lists[i]):            # the list that supplied the minimum is exhausted: no window can cover it any more
            return best
        nxt = lists[i][j + 1]
        heapq.heapreplace(heap, (nxt, i, j + 1))     # pop min and push its successor in one O(log k) step
        hi = max(hi, nxt)

# ---- examples
for lists, want in [([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]], [20, 24]),
                    ([[1, 2, 3], [1, 2, 3], [1, 2, 3]], [1, 1]),
                    ([[1], [5]], [1, 5]),
                    ([[1, 5], [2]], [1, 2])]:
    assert range_heap(lists) == range_brute(lists) == want, (lists, range_heap(lists))
    print(lists, '->', range_heap(lists))

# ---- tie behaviour: equal values from different lists
h = [(5, 2, 0), (5, 0, 3), (5, 1, 1)]
heapq.heapify(h)
print('equal values pop by list index, then position:', [heapq.heappop(h) for _ in range(3)])
try:
    h = []
    heapq.heappush(h, (5, [1, 2])); heapq.heappush(h, (5, [1, 3]))
    print('(value, the list itself) happens to work for lists: a tie compares list CONTENTS, O(len) per tie and not an intended order')
    heapq.heappush(h, (5, {'a': 1}))
except TypeError as e:
    print('but any unorderable payload on a tie fails ->', e)
print('so push (value, list index, position), not (value, the list)')

# ---- random cross-check: duplicates, negatives, equal-width ranges (smaller a must win)
for _ in range(2500):
    k = random.randint(1, 4)
    lists = [sorted(random.randint(-5, 8) for _ in range(random.randint(1, 5))) for _ in range(k)]
    assert range_heap(lists) == range_brute(lists), lists
print('2500 random list sets agree with the all-pairs brute force (width then smaller a)')

# ---- why stopping at the first exhausted list is correct: a window must contain an element of that list; every unused one is
# larger than the heap minimum already tried, so any further window starts higher AND misses the exhausted list's last element.
# a tie example where the later range has the same width: smaller a must be kept
assert range_heap([[1, 5], [2, 6]]) == [1, 2] == range_brute([[1, 5], [2, 6]])
assert range_heap([[1, 3], [2, 4]]) == [1, 2] == range_brute([[1, 3], [2, 4]])
print('tie on width [[1,3],[2,4]] ->', range_heap([[1, 3], [2, 4]]), '(widths 1 at [1,2], [2,3], [3,4]: smallest a wins)')

# ---- edge asserts and size
assert range_heap([[7]]) == [7, 7]
assert range_heap([[-10 ** 5, 10 ** 5]]) == [-10 ** 5, -10 ** 5]            # k = 1: any single element has width 0, smallest a
assert range_heap([[0], [0], [0]]) == [0, 0]
N, K = 10 ** 5, 3500
lists = [[random.randint(-10 ** 5, 10 ** 5)] for _ in range(K)]          # every list non-empty
for _ in range(N - K):
    lists[random.randrange(K)].append(random.randint(-10 ** 5, 10 ** 5))
lists = [sorted(l) for l in lists]
assert sum(map(len, lists)) == N
res = range_heap(lists)
assert res[0] <= res[1] and all(any(res[0] <= x <= res[1] for x in l) for l in lists)
print('k=3500, N=10^5: range', res, 'covers every list')
