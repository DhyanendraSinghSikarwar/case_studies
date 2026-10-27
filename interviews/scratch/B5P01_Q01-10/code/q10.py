import heapq
import random
from collections import Counter


def topk_brute(nums, k):
    # sort distinct values by frequency: O(n log n)
    return [v for v, _ in sorted(Counter(nums).items(), key=lambda p: -p[1])[:k]]


def topk_heap(nums, k):
    cnt = Counter(nums)
    h = []  # min-heap of (freq, value), size <= k: the root is the weakest of the current top k
    for v, c in cnt.items():
        if len(h) < k:
            heapq.heappush(h, (c, v))
        elif c > h[0][0]:
            heapq.heapreplace(h, (c, v))
    return [v for _, v in h]


def topk_bucket(nums, k):
    cnt = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]  # index = frequency, 1..n
    for v, c in cnt.items():
        buckets[c].append(v)
    out = []
    for c in range(len(nums), 0, -1):
        for v in buckets[c]:
            out.append(v)
            if len(out) == k:
                return out
    return out


def topk_nlargest(nums, k):
    cnt = Counter(nums)
    return heapq.nlargest(k, cnt, key=cnt.get)


print("heap  :", sorted(topk_heap([1, 1, 1, 2, 2, 3], 2)), "(expected [1, 2])")
print("bucket:", sorted(topk_bucket([1, 1, 1, 2, 2, 3], 2)), "(expected [1, 2])")

random.seed(10)
cases = 0
for _ in range(1000):
    n = random.randint(1, 14)
    a = [random.randint(-4, 4) for _ in range(n)]
    cnt = Counter(a)
    # prompt guarantees a unique answer: frequency of k-th and (k+1)-th must differ
    freqs = sorted(cnt.values(), reverse=True)
    
    k = random.randint(1, len(freqs))
    if k < len(freqs) and freqs[k - 1] == freqs[k]:
        continue
    cases += 1
    exp = sorted(topk_brute(a, k))
    assert sorted(topk_heap(a, k)) == exp == sorted(topk_bucket(a, k)) == sorted(topk_nlargest(a, k)), (a, k)
print("cross-check: %d seeded unique-answer cases agree" % cases)

assert topk_heap([1], 1) == [1] == topk_bucket([1], 1)
assert sorted(topk_bucket([4, 4, 4, 4], 1)) == [4]
assert sorted(topk_heap([-1, -1, 2, 2, 2, 3], 1)) == [2]
assert sorted(topk_bucket([5, 6, 7, 5, 6, 5], 3)) == [5, 6, 7]
# k equal to number of distinct values returns everything, even with ties
assert sorted(topk_heap([1, 2, 3], 3)) == [1, 2, 3] == sorted(topk_bucket([1, 2, 3], 3))
print("edge asserts passed")
