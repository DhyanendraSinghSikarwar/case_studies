import heapq
import random

random.seed(42)

def rooms_brute(n, meetings):
    """Simulate with a plain array of 'room free at time t' values; scan all rooms per meeting."""
    avail, cnt = [0] * n, [0] * n
    for s, e in sorted(meetings):
        free = [r for r in range(n) if avail[r] <= s]
        if free:
            r = free[0]; avail[r] = e                      # smallest free room number
        else:
            t = min(avail); r = avail.index(t)             # earliest free time, smallest room number among equals
            avail[r] = t + (e - s)                         # keeps its duration
        cnt[r] += 1
    return cnt.index(max(cnt))                             # index() = smallest room number among ties

def rooms_heaps(n, meetings, busy_key=None):
    """free: min-heap of room numbers. busy: min-heap of (free_time, room). Two heaps, one pass over sorted meetings."""
    free = list(range(n)); heapq.heapify(free)
    busy, cnt = [], [0] * n
    for s, e in sorted(meetings):
        while busy and busy[0][0] <= s:                    # <=: a room freed exactly at s is available
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            r = heapq.heappop(free)
            heapq.heappush(busy, (e, r))
        else:
            t, r = heapq.heappop(busy)                     # ties on t resolved by the smaller room number
            heapq.heappush(busy, (t + e - s, r))
        cnt[r] += 1
    return cnt.index(max(cnt))

def rooms_wrong_tiebreak(n, meetings):
    """Bug: busy tuple (free_time, meeting_index, room): on equal free times the earliest-STARTED meeting's room wins, not the smallest room."""
    free = list(range(n)); heapq.heapify(free)
    busy, cnt = [], [0] * n
    for idx, (s, e) in enumerate(sorted(meetings)):
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[2])
        if free:
            r = heapq.heappop(free)
            heapq.heappush(busy, (e, idx, r))
        else:
            t, i, r = heapq.heappop(busy)
            heapq.heappush(busy, (t + e - s, idx, r))
        cnt[r] += 1
    return cnt.index(max(cnt))

# ---- examples
for n, m, want in [(2, [[0, 10], [1, 5], [2, 7], [3, 4]], 0),
                   (3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]], 1),
                   (1, [[0, 1], [5, 6]], 0),
                   (2, [[0, 5], [1, 2], [2, 3]], 1)]:
    assert rooms_heaps(n, m) == rooms_brute(n, m) == want, (n, m)
    print('n =', n, m, '->', rooms_heaps(n, m))

# ---- tie behaviour of heap tuples: (free_time, room) breaks ties by smaller room
h = []
heapq.heappush(h, (10, 2)); heapq.heappush(h, (10, 0)); heapq.heappush(h, (10, 1))
print('busy rooms that free at the same time pop in room order:', [heapq.heappop(h) for _ in range(3)])
try:
    h = []
    heapq.heappush(h, (10, {'room': 2})); heapq.heappush(h, (10, {'room': 0}))
except TypeError as e:
    print('storing a room object instead of its number ->', e)

# ---- random cross-check; meetings with distinct starts (the prompt's guarantee)
def rand_case():
    n = random.randint(1, 4)
    starts = random.sample(range(0, 14), random.randint(1, 8))
    return n, [[s, s + random.randint(1, 6)] for s in starts]
bug_found = None
for _ in range(4000):
    n, m = rand_case()
    random.shuffle(m)
    assert rooms_heaps(n, m) == rooms_brute(n, m), (n, m)
    if bug_found is None and rooms_wrong_tiebreak(n, m) != rooms_brute(n, m):
        bug_found = (n, sorted(m))
print('4000 random cases agree with the brute-force simulation')
print('forgetting the room number as the tie-break (using meeting index) fails, e.g.:', bug_found,
      'wrong =', rooms_wrong_tiebreak(*bug_found), 'right =', rooms_heaps(*bug_found))

# ---- edge asserts
assert rooms_heaps(1, [[0, 1]]) == 0
assert rooms_heaps(3, [[0, 1]]) == 0                      # only one meeting: room 0, ties resolved to the smallest
assert rooms_heaps(2, [[0, 5], [5, 6]]) == 0              # end == next start: room 0 is free again (end is exclusive)
assert rooms_heaps(2, [[0, 5], [1, 3], [3, 4]]) == 1      # room 1 frees at 3 exactly when the third starts
n = 100
LIM = 5 * 10 ** 5
big = [[s0, random.randint(s0 + 1, LIM)] for s0 in random.sample(range(0, LIM), 10 ** 5)]   # distinct starts, start < end <= LIM
assert len(big) == 10 ** 5 and all(0 <= a < b <= LIM for a, b in big)
r = rooms_heaps(n, big)
assert 0 <= r < n
print('n=100, 10^5 meetings: busiest room', r)
