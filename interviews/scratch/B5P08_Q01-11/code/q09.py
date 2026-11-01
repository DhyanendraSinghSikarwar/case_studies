import heapq
import random
from collections import Counter

random.seed(9)

def d2(p):
    return p[0] * p[0] + p[1] * p[1]                    # squared distance: exact ints, no sqrt

def k_closest_heap(points, k):
    h = []                                              # max-heap of size k via negated distance
    for i, p in enumerate(points):
        item = (-d2(p), i)                              # index i breaks ties with ints, never compares points
        if len(h) < k:
            heapq.heappush(h, item)
        elif item > h[0]:                               # strictly closer than the farthest kept
            heapq.heapreplace(h, item)
    return [list(points[i]) for _, i in h]              # O(n log k)

def k_closest_nsmallest(points, k):
    return [list(p) for p in heapq.nsmallest(k, points, key=d2)]

def k_closest_quickselect(points, k, rng=random):
    """Iterative three-way quickselect on indices by squared distance. Expected O(n)."""
    idx = list(range(len(points)))
    dist = [d2(p) for p in points]
    lo, hi = 0, len(idx) - 1
    while lo < hi:
        pivot = dist[idx[rng.randint(lo, hi)]]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            v = dist[idx[i]]
            if v < pivot:
                idx[lt], idx[i] = idx[i], idx[lt]; lt += 1; i += 1
            elif v > pivot:
                idx[i], idx[gt] = idx[gt], idx[i]; gt -= 1
            else:
                i += 1
        if k <= lt:
            hi = lt - 1                                 # all k wanted are strictly closer than pivot
        elif k > gt + 1:
            lo = gt + 1                                 # whole < and == blocks are in, keep searching right
        else:
            break                                       # the k-th boundary is inside the == block
    return [list(points[i]) for i in idx[:k]]

def valid(points, k, got):
    """Accept any k input points (as a multiset) whose squared distances are the k smallest."""
    if len(got) != k: return False
    if Counter(map(tuple, got)) - Counter(map(tuple, points)): return False
    return sorted(map(d2, got)) == sorted(map(d2, points))[:k]

fns = (k_closest_heap, k_closest_nsmallest, k_closest_quickselect)
cases = [([[1, 3], [-2, 2]], 1), ([[3, 3], [5, -1], [-2, 4]], 2), ([[1, 1], [-1, -1], [2, 2], [0, 3]], 2),
         ([[0, 0]], 1), ([[2, 2]] * 5, 3), ([[1, 0], [0, 1], [-1, 0], [0, -1]], 2), ([[10000, -10000], [0, 0]], 2)]
for pts, k in cases:
    for fn in fns:
        assert valid(pts, k, fn(pts, k)), (fn.__name__, pts, k)
assert sorted(k_closest_heap([[1, 3], [-2, 2]], 1)) == [[-2, 2]]
assert sorted(k_closest_heap([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]

for _ in range(3000):
    n = random.randint(1, 10)
    pts = [[random.randint(-3, 3), random.randint(-3, 3)] for _ in range(n)]
    k = random.randint(1, n)
    for fn in fns:
        assert valid(pts, k, fn(pts, k)), (fn.__name__, pts, k)
print('3000 random cases ok (validator: multiset of k smallest squared distances)')

# ties at the k-th distance: several answers are valid, so never compare outputs literally
pts = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
print('four points tie at d2=2, k=2 ->', k_closest_heap(pts, 2), 'and', k_closest_quickselect(pts, 2))

# why the index in the heap tuple: tuples of (distance, payload) tie on distance, then compare payloads
class P:
    def __init__(self, x, y): self.x, self.y = x, y
h = [(2, P(1, 1))]
try:
    heapq.heappush(h, (2, P(-1, 1)))
except TypeError as e:
    print('TypeError on tie with unorderable point objects:', e)
big = [[random.randint(-10**4, 10**4), random.randint(-10**4, 10**4)] for _ in range(100000)]
assert valid(big, 1000, k_closest_heap(big, 1000)) and valid(big, 1000, k_closest_quickselect(big, 1000))
print('n = 10^5, k = 1000 ok for heap and quickselect')
