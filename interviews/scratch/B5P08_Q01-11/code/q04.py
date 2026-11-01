import heapq
import random

random.seed(4)

def kth_sort(nums, k):
    return sorted(nums, reverse=True)[k - 1]            # O(n log n), O(n) copy

def kth_heap(nums, k):
    h = []                                              # min-heap of the k largest so far
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)                     # O(log k)
    return h[0]                                         # O(n log k) time, O(k) space

def kth_quickselect(nums, k, rng=random):
    """Iterative three-way quickselect on a COPY. Expected O(n), worst O(n^2)."""
    a = list(nums)
    target = k - 1                                      # index in descending order
    lo, hi = 0, len(a) - 1
    while True:
        pivot = a[rng.randint(lo, hi)]                  # random pivot defeats sorted inputs
        # Dutch flag, descending: [lo..lt) > pivot, [lt..i) == pivot, (gt..hi] < pivot
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if a[i] > pivot:
                a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] < pivot:
                a[i], a[gt] = a[gt], a[i]; gt -= 1
            else:
                i += 1
        if target < lt:
            hi = lt - 1
        elif target > gt:
            lo = gt + 1
        else:
            return pivot                                # target falls in the == block

def kth_nlargest(nums, k):
    return heapq.nlargest(k, nums)[-1]                  # same size-k heap idea, in C

for fn in (kth_sort, kth_heap, kth_quickselect, kth_nlargest):
    assert fn([3, 2, 1, 5, 6, 4], 2) == 5
    assert fn([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert fn([7], 1) == 7
    assert fn([2, 2, 2], 3) == 2
    assert fn([3, 2, 2, 1], 2) == 2 and fn([3, 2, 2, 1], 3) == 2   # duplicates count
    assert fn([-5, -1, -3], 3) == -5

# randomised cross-check including heavy duplicates
for _ in range(1500):
    n = random.randint(1, 12)
    hi = random.choice([2, 5, 50])
    nums = [random.randint(-hi, hi) for _ in range(n)]
    k = random.randint(1, n)
    want = kth_sort(nums, k)
    snapshot = list(nums)
    assert kth_heap(nums, k) == want == kth_quickselect(nums, k) == kth_nlargest(nums, k)
    assert nums == snapshot                              # none of them modifies the input
print('1500 random cases ok (input never modified)')

# large: all equal and already sorted inputs (quickselect with a bad fixed pivot would be O(n^2))
big = [7] * 100000
assert kth_quickselect(big, 50000) == 7
srt = list(range(100000))
assert kth_quickselect(srt, 1) == 99999 and kth_quickselect(srt, 100000) == 0
assert kth_heap(srt, 10) == 99990
print('n = 10^5 all-equal and sorted inputs ok')

# comparison counts: how many elements does the heap actually replace?
rnd = random.sample(range(10**6), 10**5)
h, repl = [], 0
for x in rnd:
    if len(h) < 10: heapq.heappush(h, x)
    elif x > h[0]: heapq.heapreplace(h, x); repl += 1
print('random order, k=10: heap replacements =', repl, 'of', len(rnd), '(sorted ascending input would replace every one)')
