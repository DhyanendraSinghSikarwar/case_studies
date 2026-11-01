from collections import Counter
import random, math

def brute(pts):                                    # O(n^3): ordered (i, j, k), j != k, i distinct from both
    n, cnt = len(pts), 0
    d2 = lambda a, b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and i != k and j != k and d2(pts[i], pts[j]) == d2(pts[i], pts[k]):
                    cnt += 1
    return cnt

def optimal(pts):                                  # O(n^2) time, O(n) space
    total = 0
    for (x0, y0) in pts:                           # anchor i
        c = Counter((x - x0) ** 2 + (y - y0) ** 2 for (x, y) in pts)   # squared integer distances
        for m in c.values():
            total += m * (m - 1)                   # ordered pairs (j, k) among m points at that distance
    return total
# note: the anchor itself lands at distance 0 with count 1 (points are distinct) and adds 1*0 = 0.

assert brute([[0, 0], [1, 0], [2, 0]]) == optimal([[0, 0], [1, 0], [2, 0]]) == 2
assert optimal([[1, 1]]) == 0
print("examples:", optimal([[0, 0], [1, 0], [2, 0]]), optimal([[1, 1]]))

# float danger: sqrt distances of large integer points can differ in exact value yet compare equal as floats
a, b = 10**8, 10**8 + 1
print("squared ints differ:", a * a + 1 != b * b, "| math.sqrt(a*a+1) == math.sqrt(a*a):", math.sqrt(a * a + 1) == math.sqrt(a * a))

rng = random.Random(45)
for _ in range(400):
    n = rng.randint(0, 9)
    s = set()
    while len(s) < n: s.add((rng.randint(-3, 3), rng.randint(-3, 3)))     # distinct points
    pts = [list(p) for p in s]
    assert brute(pts) == optimal(pts), pts
print("400 seeded cross-checks passed")

assert optimal([]) == 0
assert optimal([[0, 0], [1, 1]]) == 0
square = [[0, 0], [0, 1], [1, 1], [1, 0]]
assert optimal(square) == brute(square) == 8       # each corner: two neighbours at d=1 -> 2 ordered; plus diagonals none
print("square (4 corners):", optimal(square))
neg = [[-1, 0], [0, 0], [1, 0]]
assert optimal(neg) == 2
grid = [[x, y] for x in range(30) for y in range(30)]
print("30x30 grid (900 points):", optimal(grid))
