import heapq, itertools, random

def sift_down(a, i, n, cnt):
    while True:
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < n and a[l] < a[m]: m = l          # child must be STRICTLY smaller
        if r < n and a[r] < a[m]: m = r          # right must be strictly smaller than the current best
        if m == i: return
        a[i], a[m] = a[m], a[i]; cnt[0] += 1; i = m

def sift_up(a, i):
    swaps = 0
    while i > 0 and a[(i - 1) // 2] > a[i]:      # swap while the parent is STRICTLY greater
        a[(i - 1) // 2], a[i] = a[i], a[(i - 1) // 2]; i = (i - 1) // 2; swaps += 1
    return swaps

def build(vals):
    a, c = list(vals), [0]
    for i in range(len(a) // 2 - 1, -1, -1):     # leaves (second half) are already heaps
        sift_down(a, i, len(a), c)
    p, c2 = [], 0
    for v in vals:
        p.append(v); c2 += sift_up(p, len(p) - 1)
    return [a, c[0], p, c2]

def is_heap(a): return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))

assert build([5,3,8,1,9,2]) == [[1,3,2,5,9,8], 4, [1,3,2,5,9,8], 4]
assert build([9,8,7,6,5,4,3,2,1]) == [[1,2,3,6,5,4,7,8,9], 7, [1,2,4,3,7,8,5,9,6], 16]
assert build([1,2,3,4,5,6,7]) == [[1,2,3,4,5,6,7], 0, [1,2,3,4,5,6,7], 0]
assert build([2,2,2]) == [[2,2,2], 0, [2,2,2], 0]
assert build([]) == [[], 0, [], 0]

# exhaustive: every permutation of 1..n, n <= 8
for n in range(1, 9):
    bound = n - bin(n).count("1")
    worst = 0
    for perm in itertools.permutations(range(1, n + 1)):
        a, sw, p, sw2 = build(perm)
        assert is_heap(a) and is_heap(p) and sorted(a) == sorted(p) == list(range(1, n + 1))
        assert sw <= bound
        worst = max(worst, sw)
    assert worst == bound                        # reached, so the bound is tight
    print(f"n={n}: max bottom-up swaps over all {n}! permutations = {worst} = n - popcount(n) = {bound}")

# the heights of an n-node complete tree sum to n - popcount(n)
for n in range(1, 301):
    def height(i):                               # longest path down from node i
        d = 0
        while 2 * i + 1 < n: i = 2 * i + 1; d += 1
        return d
    assert sum(height(i) for i in range(n)) == n - bin(n).count("1")
print("sum of node heights == n - popcount(n) for n = 1..300")

# one-by-one worst case: descending input costs about n log n swaps; bottom-up stays under n
for n in (255, 1023, 4095):
    r = build(range(n, 0, -1))
    print(f"n={n}: descending input, bottom-up swaps {r[1]}, one-by-one swaps {r[3]}")

# heapq.heappush gives the same layout as one-by-one; heapq.heapify may lay out differently
rng = random.Random(28)
push_same = heapify_same = 0
for _ in range(2000):
    v = [rng.randint(0, 50) for _ in range(rng.randint(0, 30))]
    h = []
    for x in v: heapq.heappush(h, x)
    assert h == build(v)[2]
    push_same += 1
    g = list(v); heapq.heapify(g)
    assert is_heap(g)
    heapify_same += g == build(v)[0]
print("heappush layout == one-by-one in", push_same, "of 2000; heapify layout == textbook bottom-up in", heapify_same, "of 2000 (both always valid heaps)")
