import random
from bisect import bisect_left
from collections import Counter

def brute(a, b):
    ca, cb = Counter(a), Counter(b)
    out = []
    for v in sorted(ca):
        out += [v] * min(ca[v], cb.get(v, 0))
    return out

def optimal(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:                  # equal: take it once, advance both (this keeps min count)
            out.append(a[i])
            i += 1
            j += 1
    return out

def by_search(small, big):
    # when small is far shorter: for each value binary search in big, resuming after the last hit
    out, lo = [], 0
    for x in small:
        k = bisect_left(big, x, lo)
        if k < len(big) and big[k] == x:
            out.append(x)
            lo = k + 1
        else:
            lo = k
    return out

assert optimal([1, 2, 2, 3, 4], [2, 2, 2, 4, 5]) == [2, 2, 4]
assert optimal([1, 3], [2, 4]) == []
assert optimal([], [1, 2]) == []
assert optimal([1, 2], []) == []
assert optimal([2, 2], [2, 2]) == [2, 2]
assert optimal([5], [5]) == [5]
assert optimal([1, 1, 1], [1]) == [1]
assert optimal([-3, -3, 0, 7], [-3, 0, 0, 9]) == [-3, 0]
assert optimal([1, 2, 3], [4, 5, 6]) == []

rng = random.Random(19)
for _ in range(1000):
    a = sorted(rng.randint(-4, 5) for _ in range(rng.randint(0, 10)))
    b = sorted(rng.randint(-4, 5) for _ in range(rng.randint(0, 10)))
    assert optimal(a, b) == brute(a, b), (a, b)
    assert by_search(a, b) == brute(a, b), (a, b)
print("1000 random cases: two pointers and binary-search variant agree with the Counter reference")
print(optimal([1, 2, 2, 3, 4], [2, 2, 2, 4, 5]), optimal([1, 3], [2, 4]))
