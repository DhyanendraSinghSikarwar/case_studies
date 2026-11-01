import heapq
import random

random.seed(3701)


def skyline(buildings):
    # event = (x, -height, right). Starts have negative second key; ends have 0.
    # Sorting puts, at equal x: taller starts first (more negative), then all starts before ends.
    events = [(l, -h, r) for l, r, h in buildings] + [(r, 0, 0) for l, r, h in buildings]
    events.sort()
    heap = [(0, float('inf'))]                    # (-height, right end); sentinel = ground, never expires
    res = []
    for x, neg_h, r in events:
        while heap[0][1] <= x:                    # lazy deletion: drop tops whose building has ended
            heapq.heappop(heap)
        if neg_h:                                 # a start event: add the building
            heapq.heappush(heap, (neg_h, r))
        while heap[0][1] <= x:                    # (a start with r <= x cannot occur, but keep the top clean)
            heapq.heappop(heap)
        cur = -heap[0][0]
        if not res or res[-1][1] != cur:          # emit only when the maximum height changes
            res.append([x, cur])
    return res


def brute(buildings):
    """Max covering height at every integer x of the range; key points are the changes."""
    hi = max(r for l, r, h in buildings)
    res, prev = [], 0
    for x in range(0, hi + 1):
        cur = max((h for l, r, h in buildings if l <= x < r), default=0)
        if cur != prev:
            res.append([x, cur])
            prev = cur
    return res


# --- the prompt's examples ---
ex = [([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],
       [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]),
      ([[0, 2, 3], [2, 4, 3]], [[0, 3], [4, 0]]),
      ([[1, 5, 4], [1, 3, 6], [3, 7, 2]], [[1, 6], [3, 4], [5, 2], [7, 0]])]
for b, want in ex:
    got = skyline(b)
    print(got)
    assert got == want == brute(b)

# --- what goes wrong if ends are handled before starts at the same x (touching buildings) ---
def skyline_ends_first(buildings):
    events = sorted([(l, h, r) for l, r, h in buildings] + [(r, -1, 0) for l, r, h in buildings])   # end key -1 < start key h
    heap, res = [(0, float('inf'))], []
    for x, h, r in events:
        if h > 0:
            heapq.heappush(heap, (-h, r))
        while heap[0][1] <= x:
            heapq.heappop(heap)
        cur = -heap[0][0]
        if not res or res[-1][1] != cur:
            res.append([x, cur])
    return res


print('ends-first on touching buildings:', skyline_ends_first([[0, 2, 3], [2, 4, 3]]), '(spurious [2, 0], [2, 3])')
assert skyline_ends_first([[0, 2, 3], [2, 4, 3]]) == [[0, 3], [2, 0], [2, 3], [4, 0]]

# --- random cross-check (sorted by left, equal lefts in random order, gaps and touching included) ---
for _ in range(2000):
    k = random.randint(1, 8)
    bs = []
    for _ in range(k):
        l = random.randint(0, 12)
        bs.append([l, random.randint(l + 1, 15), random.randint(1, 6)])
    bs.sort(key=lambda t: (t[0], random.random()))
    assert skyline(bs) == brute(bs), bs
print('random cases passed: 2000')

# --- edge cases ---
assert skyline([[1, 2, 5]]) == [[1, 5], [2, 0]]                          # single building
assert skyline([[1, 2, 5], [4, 6, 5]]) == [[1, 5], [2, 0], [4, 5], [6, 0]]   # gap: drop to 0, rise again
assert skyline([[0, 10, 1], [2, 4, 5], [3, 5, 5]]) == [[0, 1], [2, 5], [5, 1], [10, 0]]  # equal heights merge
assert skyline([[0, 5, 7], [0, 5, 7]]) == [[0, 7], [5, 0]]               # duplicate buildings
assert skyline([[0, 5, 3], [1, 2, 3]]) == [[0, 3], [5, 0]]               # fully inside, same height: no point
assert skyline([[0, 2 ** 31 - 1, 2 ** 31 - 1]]) == [[0, 2 ** 31 - 1], [2 ** 31 - 1, 0]]   # huge coordinates
many = [[i, i + 2, 1 + i % 7] for i in range(10 ** 4)]
assert len(skyline(many)) > 0                                            # n = 10^4 runs
print('edge asserts passed')
