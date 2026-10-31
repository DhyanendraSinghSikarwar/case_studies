import random
from collections import Counter


def inter_brute(a, b):
    return sorted({x for x in a if x in b})  # `in` on a list is O(len(b)) -> O(n*m)


def inter_multi_brute(a, b):
    b = list(b)
    out = []
    for x in a:
        if x in b:
            b.remove(x)  # O(m) each
            out.append(x)
    return sorted(out)


def inter_set(a, b):
    return sorted(set(a) & set(b))


def inter_multi(a, b):
    ca = Counter(a)
    out = []
    for x in b:
        if ca[x] > 0:
            out.append(x)
            ca[x] -= 1
    return sorted(out)


def inter_multi_counter_and(a, b):
    return sorted((Counter(a) & Counter(b)).elements())  # & takes min of counts


print("distinct:", inter_set([1, 2, 2, 1], [2, 2]), "(expected [2])")
print("multiset:", inter_multi([1, 2, 2, 1], [2, 2]), "(expected [2, 2])")

random.seed(7)
for _ in range(1000):
    a = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    b = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    assert inter_set(a, b) == inter_brute(a, b), (a, b)
    m = inter_multi_brute(a, b)
    assert inter_multi(a, b) == m == inter_multi_counter_and(a, b), (a, b)
print("cross-check: 1000 seeded cases agree")

# the asymmetry matters: swapping inputs must give the same multiset
assert inter_multi([1, 1, 1], [1]) == inter_multi([1], [1, 1, 1]) == [1]
assert inter_set([], [1]) == [] and inter_multi([], []) == []
assert inter_set([4, 4], [4]) == [4]
assert inter_multi([4, 9, 5], [9, 4, 9, 8, 4]) == [4, 9]
assert inter_set([1, 2], [3, 4]) == []
print("edge asserts passed")
