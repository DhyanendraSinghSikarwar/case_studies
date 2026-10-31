import heapq
import random

random.seed(1)

def layouts(vals):
    pushed = []
    for v in vals:
        heapq.heappush(pushed, v)            # O(log n) each: append, then sift up
    heapified = list(vals)
    heapq.heapify(heapified)                 # O(n) total, in place on the copy
    h = list(pushed)
    pops = [heapq.heappop(h) for _ in range(min(3, len(h)))]   # O(log n) each
    neg = []
    for v in vals:
        heapq.heappush(neg, -v)              # max-heap trick: store negatives
    top = [-heapq.heappop(neg) for _ in range(min(3, len(neg)))]
    return [pushed, heapified, pops, top]

def is_heap(a):
    # parent of i is (i-1)//2, children of i are 2i+1 and 2i+2
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))

def brute(vals):
    """Independent check: only properties, since the layout itself is CPython's."""
    pushed, heapified, pops, top = layouts(vals)
    assert is_heap(pushed) and is_heap(heapified)
    assert sorted(pushed) == sorted(vals) == sorted(heapified)
    assert pops == sorted(vals)[:3]
    assert top == sorted(vals, reverse=True)[:3]
    return True

# the four examples from the prompt (layouts are exactly CPython 3.13's)
assert layouts([5, 3, 8, 1, 9, 2]) == [[1, 3, 2, 5, 9, 8], [1, 3, 2, 5, 9, 8], [1, 2, 3], [9, 8, 5]]
assert layouts([4, 4, 1]) == [[1, 4, 4], [1, 4, 4], [1, 4, 4], [4, 4, 1]]
assert layouts([]) == [[], [], [], []]
assert layouts([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [[1, 2, 4, 3, 7, 8, 5, 9, 6], [1, 2, 3, 6, 5, 4, 7, 8, 9], [1, 2, 3], [9, 8, 7]]

# push-built and heapify-built layouts differ on the last example: both are valid heaps
a = layouts([9, 8, 7, 6, 5, 4, 3, 2, 1])
print('push layout    ', a[0])
print('heapify layout ', a[1])
print('same heap, different lists:', a[0] != a[1], '| both valid:', is_heap(a[0]) and is_heap(a[1]))

# the list is NOT sorted: only parent <= child holds
h = [1, 3, 2, 5, 9, 8]
print('h[0] is the min:', h[0], '| sorted?', h == sorted(h), '| 3 comes before 2 in the list')

# randomised cross-check, 600 seeded lists of size 0..50
for _ in range(600):
    vals = [random.randint(-20, 20) for _ in range(random.randint(0, 50))]
    brute(vals)
print('600 random lists ok')

# ties: tuples compare element by element, so a tie falls through to the next field
h = []
heapq.heappush(h, (1, 'b'))
heapq.heappush(h, (1, 'a'))
print('tie on priority broken by the 2nd field:', heapq.heappop(h))
h = []
heapq.heappush(h, (1, {'x': 1}))
try:
    heapq.heappush(h, (1, {'y': 2}))         # tie on 1, then dict < dict
except TypeError as e:
    print('TypeError on tie with unorderable payload:', e)

# max-heap trick edge: negation works for ints, not for strings
try:
    heapq.heappush([], -'abc')
except TypeError as e:
    print('cannot negate a str:', e)
print('done')
