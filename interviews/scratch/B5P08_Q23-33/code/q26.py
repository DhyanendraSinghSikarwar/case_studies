import heapq, random

def furthest(heights, bricks, ladders):
    h = []                                       # min-heap of the climbs a ladder currently covers
    for i in range(len(heights) - 1):
        d = heights[i + 1] - heights[i]
        if d > 0:
            heapq.heappush(h, d)
            if len(h) > ladders:                 # too many ladder climbs: pay bricks for the smallest
                bricks -= heapq.heappop(h)
                if bricks < 0:
                    return i
    return len(heights) - 1

def brute(heights, bricks, ladders):             # try every brick/ladder choice (depth <= n, small n only)
    best = 0
    def go(i, b, l):
        nonlocal best
        best = max(best, i)
        if i == len(heights) - 1: return
        d = heights[i + 1] - heights[i]
        if d <= 0: go(i + 1, b, l); return
        if b >= d: go(i + 1, b - d, l)
        if l > 0: go(i + 1, b, l - 1)
    go(0, bricks, ladders)
    return best

assert furthest([4,2,7,6,9,14,12], 5, 1) == 4
assert furthest([4,12,2,7,3,18,20,3,19], 10, 2) == 7
assert furthest([14,3,19,3], 17, 0) == 3
assert furthest([1,2], 0, 0) == 0

rng = random.Random(26)
for _ in range(2000):
    n = rng.randint(2, 9)
    hs = [rng.randint(1, 9) for _ in range(n)]
    b, l = rng.randint(0, 15), rng.randint(0, n)
    assert furthest(hs, b, l) == brute(hs, b, l), (hs, b, l)
print("2000 random cases match brute force")

# edge cases: ladders >= number of climbs -> always reach the end, bricks 0 is fine
assert furthest([1, 5, 2, 9, 3], 0, 2) == 4
assert furthest([5, 4, 3, 2, 1], 0, 0) == 4       # only descents: free
# Why not 'bricks first, ladder when out'? Greedy by order wastes a ladder on a small climb.
def bricks_first(hs, bricks, ladders):
    for i in range(len(hs) - 1):
        d = hs[i + 1] - hs[i]
        if d <= 0: continue
        if bricks >= d: bricks -= d
        elif ladders: ladders -= 1
        else: return i
    return len(hs) - 1
case = ([1, 3, 4, 5], 2, 1)
print("bricks-first on", case, "->", bricks_first(*case), "vs heap greedy", furthest(*case))

# heap holds plain ints, so ties are harmless. Size is at most ladders + 1 at all times.
n = 100000
hs = [(i * 7919) % 1000003 + 1 for i in range(n)]
print("n=100000:", furthest(hs, 10**9, 50), "(iterative, heap size <= 51)")
