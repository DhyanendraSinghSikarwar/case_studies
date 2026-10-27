import heapq
import random

random.seed(18)

def last_stone(stones):
    heap = [-s for s in stones]              # heapq is a min-heap: store negatives to get a max-heap
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)             # heaviest
        b = -heapq.heappop(heap)             # second heaviest, a >= b
        if a != b:
            heapq.heappush(heap, -(a - b))   # the remainder goes back
    return -heap[0] if heap else 0

def last_stone_sorted(stones):               # oracle: re-sort after each smash, O(n^2 log n)
    a = sorted(stones)
    while len(a) > 1:
        x = a.pop()
        y = a.pop()
        if x != y:
            a.append(x - y)
            a.sort()
    return a[0] if a else 0

for st, exp in [([2, 7, 4, 1, 8, 1], 1), ([1], 1), ([3, 3], 0), ([10, 4, 2, 10], 2)]:
    assert last_stone(st) == last_stone_sorted(st) == exp
    print(st, '->', last_stone(st))

for _ in range(2000):
    st = [random.randint(1, 20) for _ in range(random.randint(1, 12))]
    assert last_stone(st) == last_stone_sorted(st), st
print('random ok: 2000 inputs')

# negation trap: popping the heap without negating gives the LIGHTEST stones
h = [2, 7, 4, 1, 8, 1]
heapq.heapify(h)
print('raw min-heap pops first:', heapq.heappop(h), heapq.heappop(h), '(the two lightest, not heaviest)')

# a different, ordered-tuple view: ties between equal weights never raise, because ints are comparable
tie = [(-5, 'a'), (-5, 'b')]
heapq.heapify(tie)
print('tuple tie on weight breaks by label:', heapq.heappop(tie))

# edge cases
assert last_stone([5]) == 5
assert last_stone([1000] * 30) == 0                # 30 equal stones cancel in pairs
assert last_stone([1000] * 29) == 1000
assert last_stone([1, 1, 1]) == 1
assert last_stone([1000, 1]) == 999
assert last_stone([1, 2, 3]) == 0
print('edge cases ok')
