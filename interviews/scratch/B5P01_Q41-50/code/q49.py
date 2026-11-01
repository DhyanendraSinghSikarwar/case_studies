from math import gcd
from collections import Counter
import random

def brute(pts):                                    # O(n^3): for each pair, count points with zero cross product
    n = len(pts)
    if n <= 2: return n
    best = 2
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = pts[i], pts[j]
            c = sum((x2 - x1) * (y - y1) == (y2 - y1) * (x - x1) for x, y in pts)
            best = max(best, c)
    return best

def direction(dx, dy):                             # reduced, sign-normalised slope as an integer pair
    g = gcd(dx, dy)                                # gcd >= 0, and > 0 for distinct points
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
    return (dx, dy)                                # vertical line is (0, 1); horizontal is (1, 0)

def optimal(pts):                                  # O(n^2) time, O(n) space (distinct points)
    n = len(pts)
    if n <= 2: return n
    best = 1
    for i, (x0, y0) in enumerate(pts):
        c = Counter(direction(x - x0, y - y0) for j, (x, y) in enumerate(pts) if j != i)
        best = max(best, 1 + max(c.values()))      # anchor + the most common direction
    return best

for p, want in [([[1, 1], [2, 2], [3, 3]], 3),
                ([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]], 4)]:
    assert brute(p) == optimal(p) == want
print("examples:", optimal([[1, 1], [2, 2], [3, 3]]), optimal([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))

# why not floats: slopes (n-1)/n and n/(n+1) differ by about 1e-18, far below double precision
n = 10**9
fp = [[0, 0], [n, n - 1], [n + 1, n]]
print("not collinear: exact max =", brute(fp), "| optimal =", optimal(fp),
      "| float slopes equal:", (n - 1) / n == n / (n + 1))

rng = random.Random(49)
for _ in range(500):
    n = rng.randint(0, 10)
    s = set()
    while len(s) < n: s.add((rng.randint(-4, 4), rng.randint(-4, 4)))
    pts = [list(t) for t in s]
    assert brute(pts) == optimal(pts), pts
print("500 seeded cross-checks passed")

assert optimal([]) == 0 and optimal([[1, 1]]) == 1 and optimal([[1, 1], [2, 5]]) == 2
assert optimal([[3, 0], [3, 1], [3, 2], [4, 4]]) == 3              # vertical line
assert optimal([[0, 5], [1, 5], [2, 5], [-7, 5]]) == 4             # horizontal line, negative x
assert optimal([[0, 0], [1, 1], [-1, -1], [2, 2]]) == 4            # opposite directions share a normalised key
assert optimal([[0, 0], [1, 2], [2, 1], [3, 3]]) == 2              # two parallel-ish pairs, no triple
assert direction(-2, -4) == direction(2, 4) == (1, 2) and direction(0, -5) == (0, 1)
print("edge asserts passed")
