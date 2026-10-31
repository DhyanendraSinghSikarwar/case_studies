import heapq
import random

random.seed(7)

def rooms_heap(intervals):
    h = []                                              # min-heap of end times, one per room in use
    for s, e in sorted(intervals):                      # by start
        if h and h[0] <= s:                             # earliest-ending room is free (half-open: end == start is fine)
            heapq.heapreplace(h, e)                     # reuse it: pop old end, push new end
        else:
            heapq.heappush(h, e)                        # open a new room
    return len(h)                                       # rooms never close, so size = max rooms needed

def rooms_sweep(intervals):
    events = [(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals]
    events.sort()                                       # at equal time, -1 sorts before +1: ends free rooms first
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best

def rooms_sweep_wrong_order(intervals):
    events = [(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals]
    events.sort(key=lambda ev: (ev[0], -ev[1]))         # BUG: starts before ends at equal time
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best

def rooms_brute(intervals):
    # max number of meetings alive at any start time (the max overlap is always attained at some start)
    return max((sum(s <= t < e for s, e in intervals) for t in {s for s, e in intervals}), default=0)

for fn in (rooms_heap, rooms_sweep, rooms_brute):
    assert fn([[0, 30], [5, 10], [15, 20]]) == 2
    assert fn([[7, 10], [2, 4]]) == 1
    assert fn([[1, 5], [5, 8], [8, 9]]) == 1
    assert fn([[1, 10], [2, 3], [3, 4], [4, 5]]) == 2
    assert fn([]) == 0
    assert fn([[1, 3], [1, 3], [1, 3]]) == 3            # identical meetings all clash

for _ in range(4000):
    n = random.randint(0, 8)
    iv = []
    for _ in range(n):
        s = random.randint(0, 10)
        iv.append([s, random.randint(s + 1, 11)])
    want = rooms_brute(iv)
    assert rooms_heap(iv) == rooms_sweep(iv) == want, iv
print('4000 random cases ok')

print('wrong tie order on [[1,5],[5,8]]:', rooms_sweep_wrong_order([[1, 5], [5, 8]]), '(should be 1)')
# the heap holds only ints, so ties never compare anything else; if you stored (end, name) a tie would compare names
h = [(5, 'room-a')]
heapq.heappush(h, (5, 'room-b'))
print('heap with (end, name) tuples breaks the tie by name:', heapq.heappop(h))
# size check on 10^5 meetings (sandbox only, timing is not a proof)
big = []
for _ in range(100000):
    s = random.randint(0, 10**9 - 1)
    big.append([s, random.randint(s + 1, min(10**9, s + 10**6))])
print('10^5 meetings, rooms:', rooms_heap(big), '== sweep:', rooms_sweep(big))
