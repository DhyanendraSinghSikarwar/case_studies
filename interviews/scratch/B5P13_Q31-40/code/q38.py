import math
import random

random.seed(3801)


def solve(records):
    """In-place heap sort on a copy; every key comparison in sift is counted."""
    a = [list(r) for r in records]
    n = len(a)
    cmps = 0

    def sift(root, size):
        nonlocal cmps
        while 2 * root + 1 < size:
            ch = 2 * root + 1
            if ch + 1 < size:
                cmps += 1
                if a[ch + 1][0] > a[ch][0]:      # pick the larger child
                    ch += 1
            cmps += 1
            if a[root][0] < a[ch][0]:            # child bigger than the root: swap and keep sinking
                a[root], a[ch] = a[ch], a[root]
                root = ch
            else:
                break

    for s in range(n // 2 - 1, -1, -1):          # build the max-heap
        sift(s, n)
    for end in range(n - 1, 0, -1):              # move the max to the end, shrink the heap
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    return [a, cmps]


def brute(records):
    """Oracle: recursive sift with its own counter."""
    a = [list(r) for r in records]
    n = len(a)
    c = [0]

    def sift(root, size):
        ch = 2 * root + 1
        if ch >= size:
            return
        if ch + 1 < size:
            c[0] += 1
            if a[ch + 1][0] > a[ch][0]:
                ch += 1
        c[0] += 1
        if a[root][0] < a[ch][0]:
            a[root], a[ch] = a[ch], a[root]
            sift(ch, size)
    for s in reversed(range(n // 2)):
        sift(s, n)
    for end in reversed(range(1, n)):
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    assert [r[0] for r in a] == sorted(r[0] for r in records)
    return [a, c[0]]


# dry run on [[5,1],[4,2],[3,3],[2,4],[1,5]] with the array printed after each step (keys only)
a = [[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]]
n = len(a)
print("keys at start         :", [r[0] for r in a], "(already a max-heap)")
tr = []
cm = 0
def sift_t(root, size):
    global cm
    while 2 * root + 1 < size:
        ch = 2 * root + 1
        if ch + 1 < size:
            cm += 1
            if a[ch + 1][0] > a[ch][0]:
                ch += 1
        cm += 1
        if a[root][0] < a[ch][0]:
            a[root], a[ch] = a[ch], a[root]
            root = ch
        else:
            break
for s in range(n // 2 - 1, -1, -1):
    sift_t(s, n)
print("after build           :", [r[0] for r in a], "comparisons so far", cm)
for end in range(n - 1, 0, -1):
    a[0], a[end] = a[end], a[0]
    sift_t(0, end)
    print(f"after end={end} sift     :", [r[0] for r in a], "comparisons so far", cm)

for rc, want in [([[3, 1], [1, 2], [2, 3]], [[[1, 2], [2, 3], [3, 1]], 3]),
                 ([[0, 0], [0, 1]], [[[0, 1], [0, 0]], 1]),
                 ([[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]], [[[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]], 10]),
                 ([], [[], 0])]:
    assert solve(rc) == want == brute(rc), rc
print("all four examples match, including the recursive oracle")

# not stable: the smallest failing input from this algorithm
print("unstable:", solve([[0, 0], [0, 1]])[0], "(tags 0,1 became 1,0)")
print("unstable 3 items:", solve([[1, "a"], [1, "b"], [1, "c"]])[0])

# bound: sift makes at most 2 comparisons per level, so comparisons <= 2 * (n/2 + n) * floor(log2 n); compare with n log2 n
print("\n     n   random   sorted  reversed  all equal   2n*log2(n)")
for n in (10, 100, 1000, 5000):
    rows = []
    for kind in ("random", "sorted", "reversed", "equal"):
        ks = {"random": [random.randint(0, 10 ** 6) for _ in range(n)], "sorted": list(range(n)),
              "reversed": list(range(n, 0, -1)), "equal": [7] * n}[kind]
        cm_ = solve([[k, i] for i, k in enumerate(ks)])[1]
        assert cm_ <= 2 * (n // 2 + n) * max(1, int(math.log2(n)))
        rows.append(cm_)
    print(f"{n:>6} {rows[0]:>8} {rows[1]:>8} {rows[2]:>9} {rows[3]:>10} {2 * n * math.log2(n):>12.0f}")

# seeded random cross-check against sorted() on the keys and the recursive sift counter
for _ in range(500):
    n = random.randint(0, 40)
    rc = [[random.randint(-5, 5), i] for i in range(n)]
    got = solve(rc)
    assert got == brute(rc) and [r[0] for r in got[0]] == sorted(r[0] for r in rc)
    assert sorted(map(tuple, got[0])) == sorted(map(tuple, rc))          # same records, nothing lost
print("500 seeded random cases: sorted keys, same records, same comparison count as the recursive sift")

# edge cases
assert solve([]) == [[], 0] and solve([[4, 4]]) == [[[4, 4]], 0] and solve([[2, 0], [1, 1]])[1] == 1
assert solve([[1, 0], [2, 1]])[0] == [[1, 0], [2, 1]]
print("edge asserts ok")
