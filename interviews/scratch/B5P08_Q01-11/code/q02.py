import heapq
import random

random.seed(2)

class KthLargest:
    """Min-heap holding the k largest values seen so far; its root is the k-th largest."""
    def __init__(self, k, nums):
        self.k = k
        self.h = list(nums)
        heapq.heapify(self.h)                    # O(n)
        while len(self.h) > k:
            heapq.heappop(self.h)                # keep only the k largest

    def add(self, val):
        if len(self.h) < self.k:
            heapq.heappush(self.h, val)          # heap not full yet
        elif val > self.h[0]:
            heapq.heapreplace(self.h, val)       # pop the root, push val: one sift, O(log k)
        return self.h[0]                         # k-th largest (valid once len == k)

class KthLargestBrute:
    def __init__(self, k, nums):
        self.k, self.a = k, list(nums)
    def add(self, val):
        self.a.append(val)
        return sorted(self.a, reverse=True)[self.k - 1]   # O(n log n) per add

def run(cls, k, nums, adds):
    obj = cls(k, nums)
    return [obj.add(v) for v in adds]

assert run(KthLargest, 3, [4, 5, 8, 2], [3, 5, 10, 9, 4]) == [4, 5, 5, 8, 8]
assert run(KthLargest, 1, [], [-3, -2, -4, 0]) == [-3, -2, -2, 0]
assert run(KthLargest, 2, [0], [-1, 1, -2, -4, 3]) == [-1, 0, 0, 0, 1]

# randomised cross-check, honouring len(nums) + 1 >= k
for _ in range(500):
    n = random.randint(0, 8)
    k = random.randint(1, n + 1)
    nums = [random.randint(-5, 5) for _ in range(n)]
    adds = [random.randint(-5, 5) for _ in range(random.randint(1, 12))]
    assert run(KthLargest, k, nums, adds) == run(KthLargestBrute, k, nums, adds)
print('500 random streams ok')

# heap size never exceeds k, and k == len(nums)+1 is the tightest legal case
obj = KthLargest(4, [1, 2, 3])
assert obj.add(0) == 0 and len(obj.h) == 4       # first add fills the heap
assert obj.add(10) == 1 and len(obj.h) == 4
# duplicates count separately
assert run(KthLargest, 2, [5, 5], [5]) == [5]
# k larger than len(nums)+1 is outside the constraint: the root is then NOT the k-th largest
bad = KthLargest(5, [1])
print('outside the constraint, add(2) returns', bad.add(2), '(only 2 values exist, so no 5th largest)')

# why not a max-heap of everything: finding the k-th needs k pops each time
mx = [-x for x in [4, 5, 8, 2, 3]]
heapq.heapify(mx)
tmp = [heapq.heappop(mx) for _ in range(3)]
print('3rd largest via max-heap of all:', -tmp[-1], '(cost k log n per query, and it destroys the heap)')
print('size-k min-heap root:', run(KthLargest, 3, [4, 5, 8, 2], [3])[0], '(O(log k) per add)')
