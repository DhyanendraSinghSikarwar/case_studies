from collections import Counter, defaultdict
import random

def brute(nums, t):                      # O(n^2) reference: count index pairs i<j
    return sum(nums[i] + nums[j] == t for i in range(len(nums)) for j in range(i + 1, len(nums)))

def partition_of(x, t, parts):           # x and t-x MUST land in the same partition
    return min(x, t - x) % parts

def partitioned(nums, t, parts=3):
    buckets = defaultdict(list)          # stand-in for `parts` files on disk
    for x in nums: buckets[partition_of(x, t, parts)].append(x)
    total, pairs = 0, []
    for pid in sorted(buckets):          # each bucket fits in memory on its own
        c = Counter(buckets[pid])
        for x in sorted(c):
            y = t - x
            if x < y and y in c:
                total += c[x] * c[y]; pairs.append((x, y))
            elif x == y:
                total += c[x] * (c[x] - 1) // 2
                if c[x] > 1: pairs.append((x, y))
    return total, pairs, {p: sorted(v) for p, v in sorted(buckets.items())}

def sorted_two_pointer(nums, t):         # what external sort + one streaming pass gives you
    a = sorted(nums); i, j, total = 0, len(a) - 1, 0
    while i < j:
        s = a[i] + a[j]
        if s < t: i += 1
        elif s > t: j -= 1
        else:
            if a[i] == a[j]: total += (j - i + 1) * (j - i) // 2; break
            li, lj = a[i], a[j]; ci = cj = 0
            while a[i] == li: i += 1; ci += 1
            while a[j] == lj: j -= 1; cj += 1
            total += ci * cj
    return total

def bounded_stream(nums, t, cap):        # streaming with eviction: APPROXIMATE (can miss pairs)
    seen, order, found = set(), [], 0
    for x in nums:
        if t - x in seen: found += 1
        seen.add(x); order.append(x)
        if len(order) > cap: seen.discard(order.pop(0))   # pop(0) is O(n); use deque in real code
    return found

nums = [3, 17, 8, 12, 5, 15, 10, 10, 1, 19, 7, 13]
t = 20
total, pairs, buckets = partitioned(nums, t, 3)
print("buckets:", buckets)
print("pairs (value form):", pairs, "-> index pairs:", total)
print("brute:", brute(nums, t), "| sorted two-pointer:", sorted_two_pointer(nums, t))
print("bounded stream cap=12:", bounded_stream(nums, t, 12), "cap=2:", bounded_stream(nums, t, 2), "(exact is", brute(nums, t), ")")

far = [1, 5, 6, 7, 19]                   # partners 1 and 19 are four positions apart
print("far-apart pair: exact", brute(far, t), "| cap=2 stream finds", bounded_stream(far, t, 2), "| cap=5 finds", bounded_stream(far, t, 5))

rng = random.Random(43)
for _ in range(500):
    n = rng.randint(0, 14)
    a = [rng.randint(-6, 14) for _ in range(n)]; tt = rng.randint(-4, 12)
    parts = rng.randint(1, 5)
    assert partitioned(a, tt, parts)[0] == brute(a, tt) == sorted_two_pointer(a, tt), (a, tt, parts)
print("500 seeded cross-checks passed (partitioned == brute == sorted two-pointer)")

assert partitioned([], 5)[0] == 0
assert partitioned([5], 10)[0] == 0                 # single element cannot pair with itself
assert partitioned([5, 5], 10)[0] == 1
assert partitioned([5, 5, 5], 10)[0] == 3
assert partitioned([-3, 23], 20)[0] == 1            # negatives: Python % keeps bucket id non-negative
print("edge asserts passed")
