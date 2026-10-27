import heapq
import random

random.seed(10)

def merge_heap(lists):
    h = [(l[0], i, 0) for i, l in enumerate(lists) if l]   # one head per non-empty list: (value, list index, position)
    heapq.heapify(h)
    out, peak = [], len(h)
    while h:
        v, i, j = heapq.heappop(h)
        out.append(v)
        if j + 1 < len(lists[i]):                       # at most one push per pop
            heapq.heappush(h, (lists[i][j + 1], i, j + 1))
        peak = max(peak, len(h))
    assert peak <= len(lists)                           # heap never holds more than k entries
    return out                                          # O(N log k) time, O(k) heap space

def merge_two(a, b):
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if b[j] < a[i]: out.append(b[j]); j += 1        # strict <: ties take from a first, stable
        else: out.append(a[i]); i += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out

def merge_pairwise(lists):
    """Bottom-up divide and conquer, iterative: log2(k) rounds, each touching N items -> O(N log k)."""
    cur = [list(l) for l in lists]
    if not cur: return []
    while len(cur) > 1:
        nxt = [merge_two(cur[i], cur[i + 1]) for i in range(0, len(cur) - 1, 2)]
        if len(cur) % 2: nxt.append(cur[-1])
        cur = nxt
    return cur[0]

def merge_library(lists):
    return list(heapq.merge(*lists))                    # heapq.merge returns an ITERATOR, wrap it in list()

def merge_sort_all(lists):
    return sorted(x for l in lists for x in l)          # O(N log N), the brute force

fns = (merge_heap, merge_pairwise, merge_library, merge_sort_all)
for fn in fns:
    assert fn([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert fn([[], [1], []]) == [1]
    assert fn([]) == []
    assert fn([[2, 2], [2], [1, 2, 3]]) == [1, 2, 2, 2, 2, 3]
    assert fn([[], []]) == []
    assert fn([[-3, -3], [-3]]) == [-3, -3, -3]

for _ in range(2000):
    k = random.randint(0, 6)
    lists = [sorted(random.randint(-5, 5) for _ in range(random.randint(0, 6))) for _ in range(k)]
    want = merge_sort_all(lists)
    for fn in fns:
        assert fn(lists) == want, (fn.__name__, lists)
print('2000 random cases ok')

# max constraints: k = 100 lists, N = 10^4
big = [sorted(random.randint(-10**9, 10**9) for _ in range(100)) for _ in range(100)]
assert merge_heap(big) == merge_sort_all(big) == merge_pairwise(big)
print('k = 100, N = 10^4 ok; heapq.merge type:', type(heapq.merge([1], [2])).__name__)

# tie-breaking: without the list index, a tie on value would compare the NEXT tuple field
it_a, it_b = iter([1]), iter([1])
try:
    heapq.heappush([(1, it_a)], (1, it_b))               # (value, iterator): tie on value, then iterator < iterator
except TypeError as e:
    print('TypeError on tied value with iterator payload:', e)
# with the index the first field that differs is always an int, and equal values come out in list order
h = [(2, 0, 0), (2, 1, 0), (2, 2, 0)]
heapq.heapify(h)
print('equal values pop in list-index order:', [heapq.heappop(h)[1] for _ in range(3)])

# a lazily consumed merge: heapq.merge never builds the full output
gen = heapq.merge([1, 5, 9], [2, 6], [3])
print('first three from the iterator:', [next(gen) for _ in range(3)])
