import heapq
import random

random.seed(41)

def median_brute(nums, k):
    out = []
    for i in range(len(nums) - k + 1):
        w = sorted(nums[i:i + k])
        out.append(float(w[k // 2]) if k % 2 else (w[k // 2 - 1] + w[k // 2]) / 2)
    return out

def median_two_heaps(nums, k):
    """lo = max-heap (negated) of the smaller half, hi = min-heap of the larger half. Entries are (value, index):
    the index makes ties orderable and identifies the exact element to delete lazily."""
    lo, hi = [], []
    side = {}                 # index -> 'lo' or 'hi' for elements currently in the window
    dead = set()              # indices that left the window but may still sit inside a heap
    lsz = hsz = 0             # LIVE sizes (heap lengths include dead entries)
    out = []

    def prune(h):             # discard dead entries from the top so h[0] is a live element
        while h and h[0][1] in dead:
            dead.discard(h[0][1])
            heapq.heappop(h)

    for i, x in enumerate(nums):
        prune(lo)
        if lo and x <= -lo[0][0]:
            heapq.heappush(lo, (-x, i)); side[i] = 'lo'; lsz += 1
        else:
            heapq.heappush(hi, (x, i)); side[i] = 'hi'; hsz += 1
        if i >= k:                                   # element i-k leaves: mark only, fix the live count
            j = i - k
            dead.add(j)
            if side.pop(j) == 'lo': lsz -= 1
            else: hsz -= 1
        while lsz > (lsz + hsz + 1) // 2:            # lo may hold at most one more than hi
            prune(lo); v, j = heapq.heappop(lo); heapq.heappush(hi, (-v, j)); side[j] = 'hi'; lsz -= 1; hsz += 1
        while lsz < (lsz + hsz + 1) // 2:
            prune(hi); v, j = heapq.heappop(hi); heapq.heappush(lo, (-v, j)); side[j] = 'lo'; hsz -= 1; lsz += 1
        prune(lo); prune(hi)
        if i >= k - 1:
            out.append(float(-lo[0][0]) if k % 2 else (-lo[0][0] + hi[0][0]) / 2)
    return out

# ---- examples
for nums, k, want in [([1, 3, -1, -3, 5, 3, 6, 7], 3, [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]),
                      ([1, 2, 3, 4, 2, 3, 1, 4, 2], 3, [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]),
                      ([1, 4, 2, 3], 4, [2.5]), ([5, 5, 5], 2, [5.0, 5.0])]:
    got = median_two_heaps(nums, k)
    assert got == median_brute(nums, k) == want, (nums, k, got)
    print(nums, k, '->', got)

# ---- tie behaviour: equal values in the heap, tuple (value, index) keeps them orderable
h = []
heapq.heappush(h, (5, 0)); heapq.heappush(h, (5, 1))
print('equal values pop by index:', heapq.heappop(h), heapq.heappop(h))
try:
    h2 = [(5, [1])]
    heapq.heappush(h2, (5, {'i': 2}))
except TypeError as e:
    print('payload without a unique int:', e)

# ---- random cross-check: heavy duplicates, odd and even k, k == 1, k == n
for _ in range(3000):
    n = random.randint(1, 14)
    nums = [random.randint(-3, 3) for _ in range(n)]
    k = random.randint(1, n)
    assert median_two_heaps(nums, k) == median_brute(nums, k), (nums, k)
print('3000 random lists agree with sort-each-window')

# ---- extremes and size
assert median_two_heaps([7], 1) == [7.0]
assert median_two_heaps([10 ** 9, 10 ** 9], 2) == [1e9]
assert median_two_heaps([-10 ** 9, 10 ** 9], 2) == [0.0]
assert median_two_heaps([1, 2, 3, 4], 1) == [1.0, 2.0, 3.0, 4.0]
nums = [random.randint(-10 ** 9, 10 ** 9) for _ in range(10 ** 5)]
for k in (1, 2, 3, 100, 1001):
    got = median_two_heaps(nums[:3000], k)
    assert got == median_brute(nums[:3000], k), k
assert len(median_two_heaps(nums, 1000)) == 10 ** 5 - 999
asc = list(range(10 ** 5))
assert median_two_heaps(asc, 5000)[:2] == [2499.5, 2500.5]
print('size 10^5 ok (ascending input, window 5000: first medians', median_two_heaps(asc, 5000)[:2], ')')
