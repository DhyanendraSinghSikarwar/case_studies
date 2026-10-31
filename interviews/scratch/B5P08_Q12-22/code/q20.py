import heapq
import itertools
import random
from functools import lru_cache

random.seed(20)

def connect_sticks(sticks):
    heap = list(sticks)
    heapq.heapify(heap)                      # min-heap of lengths
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)              # two shortest
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total

def connect_longest_first(sticks):           # WRONG on purpose: join the two LONGEST
    a = sorted(sticks)
    total = 0
    while len(a) > 1:
        x = a.pop()
        y = a.pop()
        total += x + y
        a.append(x + y)
        a.sort()
    return total

def brute(sticks):                           # try every pair at every step, memoised on the sorted multiset
    @lru_cache(None)
    def f(t):
        if len(t) == 1:
            return 0
        best = 10 ** 18
        for i, j in itertools.combinations(range(len(t)), 2):
            rest = [t[k] for k in range(len(t)) if k not in (i, j)] + [t[i] + t[j]]
            best = min(best, t[i] + t[j] + f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(sticks)))

def weighted_depth(sticks):                  # build the merge tree, then sum leaf weight * leaf depth
    heap = [(w, i) for i, w in enumerate(sticks)]        # (weight, unique id): ties never reach a non-orderable item
    heapq.heapify(heap)
    kids = {}
    nxt = len(sticks)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        kids[nxt] = (a[1], b[1])
        heapq.heappush(heap, (a[0] + b[0], nxt))
        nxt += 1
    total = 0
    stack = [(heap[0][1], 0)]                            # iterative walk from the root
    while stack:
        node, d = stack.pop()
        if node in kids:
            stack.append((kids[node][0], d + 1))
            stack.append((kids[node][1], d + 1))
        else:
            total += sticks[node] * d
    return total

for st, exp in [([2, 4, 3], 14), ([1, 8, 3, 5], 30), ([5], 0), ([1, 1, 1, 1], 8)]:
    assert connect_sticks(st) == brute(st) == weighted_depth(st) == exp
    print(st, '->', connect_sticks(st))

for _ in range(1000):
    st = [random.randint(1, 9) for _ in range(random.randint(1, 6))]
    assert connect_sticks(st) == brute(st) == weighted_depth(st), st
print('random ok: 1000 inputs')

# three-stick counter-example for longest-first
cx = [1, 2, 3]
print('longest first on', cx, '->', connect_longest_first(cx), '; shortest first ->', connect_sticks(cx), '; brute ->', brute(cx))
assert connect_longest_first(cx) == 11 and connect_sticks(cx) == 9 == brute(cx)
worse = sum(connect_longest_first(list(c)) > connect_sticks(list(c)) for c in itertools.product(range(1, 6), repeat=3))
print('triples over 1..5 where longest-first costs more:', worse, 'of 125')

# the heap of tuples: equal weights tie, so the tuple needs a unique tiebreak if the payload is not orderable
try:
    h = []
    heapq.heappush(h, (3, {'name': 'x'}))
    heapq.heappush(h, (3, {'name': 'y'}))
except TypeError as e:
    print('TypeError on tied weights with dict payload:', e)

# edge cases and max size
assert connect_sticks([7]) == 0
assert connect_sticks([1, 1]) == 2
assert connect_sticks([10 ** 4] * 4) == 80000
big = [random.randint(1, 10 ** 4) for _ in range(10 ** 4)]
assert connect_sticks(big) == weighted_depth(big)
print('edge cases ok; cost for n = 10^4 random sticks:', connect_sticks(big))
