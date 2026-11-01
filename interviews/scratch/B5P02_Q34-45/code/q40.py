import random

def brute(a, b, k):
    return sorted(a + b)[k - 1]

def kth_union(a, b, k):
    i = j = 0
    cur = None
    for _ in range(k):
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            cur = a[i]; i += 1
        else:
            cur = b[j]; j += 1
    return cur

for a, b, k, exp in [([1, 3, 5, 7], [2, 4, 6], 5, 5), ([1, 1, 2], [1, 2, 2], 4, 2)]:
    assert kth_union(a, b, k) == brute(a, b, k) == exp
    print(a, b, "k =", k, "->", kth_union(a, b, k))
assert kth_union([], [4], 1) == 4 and kth_union([4], [], 1) == 4
assert kth_union([1, 2], [3, 4], 4) == 4 and kth_union([5, 6], [1, 2], 3) == 5
assert kth_union([2, 2], [2, 2], 3) == 2 and kth_union([-3, 0], [-5, 1], 2) == -3
random.seed(40)
for _ in range(1500):
    a = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 7)))
    b = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 7)))
    if not a and not b: continue
    k = random.randint(1, len(a) + len(b))
    assert kth_union(a, b, k) == brute(a, b, k), (a, b, k)
print("1500 seeded cases match sorted(a + b)[k-1]; edges pass")
