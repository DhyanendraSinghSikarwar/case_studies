import heapq, random

def max_events(events):
    ev = sorted(events)                # by start day
    h, i, day, cnt, n = [], 0, 0, 0, len(ev)
    while i < n or h:
        if not h:
            day = max(day, ev[i][0])   # nothing open: jump to the next start
        while i < n and ev[i][0] <= day:
            heapq.heappush(h, ev[i][1]); i += 1
        while h and h[0] < day:        # expired
            heapq.heappop(h)
        if h:
            heapq.heappop(h); cnt += 1; day += 1   # attend the soonest-ending event
    return cnt

def brute(events):                     # maximum bipartite matching events -> days (Kuhn), small inputs only
    match = {}
    def try_(i, seen):
        for d in range(events[i][0], events[i][1] + 1):
            if d in seen: continue
            seen.add(d)
            if d not in match or try_(match[d], seen):
                match[d] = i; return True
        return False
    return sum(try_(i, set()) for i in range(len(events)))

assert max_events([[1,2],[2,3],[3,4]]) == 3
assert max_events([[1,2],[2,3],[3,4],[1,2]]) == 4
assert max_events([[1,1],[1,1],[1,1]]) == 1
assert max_events([[1,4],[4,4],[2,2],[3,4],[1,1]]) == 4

rng = random.Random(25)
for _ in range(1500):
    n = rng.randint(1, 8)
    ev = []
    for _ in range(n):
        s = rng.randint(1, 7); ev.append([s, rng.randint(s, 8)])
    assert max_events(ev) == brute(ev), ev
print("1500 random cases match matching brute force")

# wrong rule: each day attend the open event with the LATEST end (to show why soonest-end matters)
def latest_end_first(events):
    ev = sorted(events); h, i, day, cnt = [], 0, 0, 0
    while i < len(ev) or h:
        if not h: day = max(day, ev[i][0])
        while i < len(ev) and ev[i][0] <= day: heapq.heappush(h, -ev[i][1]); i += 1
        while h and -h[0] < day: heapq.heappop(h)
        if h: heapq.heappop(h); cnt += 1; day += 1
    return cnt
bad = [[1, 1], [1, 2]]
print("latest-end-first on", bad, ":", latest_end_first(bad), "vs soonest-end", max_events(bad))

# heap of plain ints: tied ends are fine (equal ints compare). The heap holds end days only.
h = []
for e in [4, 4, 2, 4]: heapq.heappush(h, e)
print("ties in a heap of ints are fine:", [heapq.heappop(h) for _ in range(4)])

# scale: n = 100000, sort + one push and one pop per event -> O(n log n); loop is iterative
rng = random.Random(1)
big = []
for _ in range(100000):
    s = rng.randint(1, 100000); big.append([s, min(100000, s + rng.randint(0, 50))])
print("n=100000 random events ->", max_events(big), "attended (<= 100000 days)")
