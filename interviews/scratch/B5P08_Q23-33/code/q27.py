import heapq, random
from collections import Counter

def k_pairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []
    h = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapq.heapify(h)
    out = []
    while h and len(out) < k:
        _, i, j = heapq.heappop(h)
        out.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(h, (nums1[i] + nums2[j + 1], i, j + 1))
    return out

def valid(nums1, nums2, k, got):       # checker: right pairs (with multiplicity) and exactly the k smallest sums
    allp = [(x, y) for x in nums1 for y in nums2]
    return (len(got) == k and not (Counter(map(tuple, got)) - Counter(allp))
            and [x + y for x, y in got] == sorted(x + y for x, y in allp)[:k])   # ascending order of sum

def brute(nums1, nums2, k):
    return sorted(([x, y] for x in nums1 for y in nums2), key=lambda p: p[0] + p[1])[:k]

assert valid([1,7,11], [2,4,6], 3, k_pairs([1,7,11], [2,4,6], 3))
assert k_pairs([1,7,11], [2,4,6], 3) == [[1,2],[1,4],[1,6]]
assert k_pairs([1,1,2], [1,2,3], 2) == [[1,1],[1,1]]
assert k_pairs([1,2], [3], 2) == [[1,3],[2,3]]

rng = random.Random(27)
for _ in range(2000):
    a = sorted(rng.randint(-6, 6) for _ in range(rng.randint(1, 6)))
    b = sorted(rng.randint(-6, 6) for _ in range(rng.randint(1, 6)))
    k = rng.randint(1, len(a) * len(b))
    got = k_pairs(a, b, k)
    assert valid(a, b, k, got), (a, b, k, got)
    assert [x + y for x, y in got] == [x + y for x, y in brute(a, b, k)]
print("2000 random cases: valid output, sums equal brute force (pairs may differ on ties)")

# Tie-breaking: (sum, i, j) never ties completely because (i, j) is unique per state,
# so heapq never has to compare anything beyond ints. Pushing (sum, [u, v]) also works (lists compare),
# but pushing (sum, {'u':..}) with dict payloads would raise TypeError on equal sums:
h = []
heapq.heappush(h, (5, {'p': 1}))
try:
    heapq.heappush(h, (5, {'p': 2}))
except TypeError as e:
    print("TypeError on tied sums with dict payload:", e)

# Size: heap never exceeds min(k, len(nums1)) entries -> O(k log min(k, n1)); n = 100000, k = 10000
n = 100000
a = [i * 3 for i in range(n)]; b = [i * 5 - 7 for i in range(n)]
res = k_pairs(a, b, 10000)
assert [x + y for x, y in res] == sorted(x + y for x, y in res)
print("n=100000, k=10000: last sum", sum(res[-1]), "first", res[0])
