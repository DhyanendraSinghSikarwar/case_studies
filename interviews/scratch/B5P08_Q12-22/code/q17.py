import bisect
import heapq
import random

random.seed(17)

def running_median(adds):
    lo = []                                  # max-heap of the smaller half, stored negated
    hi = []                                  # min-heap of the larger half
    out = []
    for x in adds:
        heapq.heappush(lo, -x)               # 1. push into lo
        heapq.heappush(hi, -heapq.heappop(lo))   # 2. move lo's max to hi so every lo <= every hi
        if len(hi) > len(lo):                # 3. rebalance: lo may have at most one extra
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) > len(hi):
            out.append(float(-lo[0]))        # odd count: the top of lo
        else:
            out.append((-lo[0] + hi[0]) / 2) # even count: mean of the two tops
    return out

def median_insort(adds):                     # sorted list + bisect.insort: O(n) per insert (memmove)
    a = []
    out = []
    for x in adds:
        bisect.insort(a, x)
        m = len(a)
        out.append(float(a[m // 2]) if m % 2 else (a[m // 2 - 1] + a[m // 2]) / 2)
    return out

def median_brute(adds):                      # re-sort the whole prefix each time, O(n^2 log n)
    out = []
    for i in range(1, len(adds) + 1):
        s = sorted(adds[:i])
        m = len(s)
        out.append(float(s[m // 2]) if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2)
    return out

for adds, exp in [([1, 2, 3], [1.0, 1.5, 2.0]), ([5, 15, 1, 3], [5.0, 10.0, 5.0, 4.0]),
                  ([-1, -2, -3, -4, -5], [-1.0, -1.5, -2.0, -2.5, -3.0]),
                  ([2, 2, 2, 2], [2.0, 2.0, 2.0, 2.0]), ([7], [7.0])]:
    assert running_median(adds) == median_insort(adds) == median_brute(adds) == exp
    print(adds, '->', running_median(adds))

for _ in range(1000):
    adds = [random.randint(-9, 9) for _ in range(random.randint(1, 25))]
    assert running_median(adds) == median_brute(adds), adds
print('random ok: 1000 small streams (many duplicates)')

for _ in range(20):
    adds = [random.randint(-10 ** 6, 10 ** 6) for _ in range(random.randint(100, 400))]
    assert running_median(adds) == median_insort(adds) == median_brute(adds)
print('random ok: 20 streams of 100-400 values in [-10^6, 10^6]')

# invariant check after every step: len(lo) == len(hi) or len(lo) == len(hi) + 1, and max(lo) <= min(hi)
lo, hi = [], []
for x in [random.randint(-50, 50) for _ in range(2000)]:
    heapq.heappush(lo, -x)
    heapq.heappush(hi, -heapq.heappop(lo))
    if len(hi) > len(lo):
        heapq.heappush(lo, -heapq.heappop(hi))
    assert len(lo) in (len(hi), len(hi) + 1)
    assert not hi or -lo[0] <= hi[0]
print('invariant holds for 2000 steps')

# edge cases: sorted, reverse sorted, all equal, extremes, mean of two extremes
assert running_median([1, 2]) == [1.0, 1.5]
assert running_median([-10 ** 6, 10 ** 6]) == [-1000000.0, 0.0]
assert running_median([10 ** 6, 10 ** 6 - 1]) == [1000000.0, 999999.5]
n = 20000
up = list(range(n))
assert running_median(up) == median_insort(up)
assert running_median(up[::-1]) == median_insort(up[::-1])
assert running_median([3] * n) == [3.0] * n
big = [random.randint(-10 ** 6, 10 ** 6) for _ in range(10 ** 5)]       # max size, iterative
res = running_median(big)
assert len(res) == 10 ** 5 and res[-1] == median_insort(big)[-1]
print('edge cases ok; n = 10^5 done')
