import random
import sys
from collections import deque

random.seed(4)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    img = [row[:] for row in image]          # do not mutate the input
    if old == color:
        return img                           # the guard (see below)
    m, n = len(img), len(img[0])
    img[sr][sc] = color                      # recolouring on push doubles as the visited mark
    stack = [(sr, sc)]
    while stack:
        x, y = stack.pop()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and img[a][b] == old:
                img[a][b] = color
                stack.append((a, b))
    return img

def brute(image, sr, sc, color):
    """Recursive DFS with an explicit visited set; only safe while the region is < ~1000 cells deep."""
    m, n = len(image), len(image[0]); old = image[sr][sc]; seen = set()
    def go(x, y):
        seen.add((x, y))
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and image[a][b] == old and (a, b) not in seen:
                go(a, b)
    go(sr, sc)
    return [[color if (i, j) in seen else image[i][j] for j in range(n)] for i in range(m)]

def unguarded(image, sr, sc, color, cap):
    """No visited set and no old == color guard. When old == color nothing ever changes, so cells re-enter forever."""
    img = [row[:] for row in image]; old = img[sr][sc]; m, n = len(img), len(img[0])
    stack = [(sr, sc)]; pops = 0
    while stack:
        pops += 1
        if pops > cap:
            return 'still running after %d pops' % cap
        x, y = stack.pop(); img[x][y] = color
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and img[a][b] == old:
                stack.append((a, b))
    return img

assert flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
assert flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == [[0, 0, 0], [0, 0, 0]]
assert flood_fill([[5]], 0, 0, 9) == [[9]]
print('3 prompt examples ok')

src = [[1, 0], [0, 1]]
flood_fill(src, 0, 0, 7); assert src == [[1, 0], [0, 1]]        # input untouched

for _ in range(1000):
    m, n = random.randint(1, 5), random.randint(1, 5)
    img = [[random.randint(0, 2) for _ in range(n)] for _ in range(m)]
    sr, sc, col = random.randrange(m), random.randrange(n), random.randint(0, 3)
    want = brute(img, sr, sc, col) if img[sr][sc] != col else img
    assert flood_fill(img, sr, sc, col) == want, (img, sr, sc, col)
print('1000 seeded random grids: iterative == recursive-with-visited')

# the guard: same colour, no visited set
print('unguarded, color == old:', unguarded([[0, 0], [0, 0]], 0, 0, 0, 10000))
print('unguarded, color != old:', unguarded([[0, 0], [0, 0]], 0, 0, 5, 10000))

# scale: 300 x 300 all the same colour = one region of 90000 cells
big = [[1] * 300 for _ in range(300)]
out = flood_fill(big, 0, 0, 2)
assert all(v == 2 for row in out for v in row) and all(v == 1 for row in big for v in row)
print('300x300 single region recoloured iteratively, 90000 cells')

# a serpentine corridor forces a DFS path 45000+ deep: recursion cannot cope
snake = [[0] * 300 for _ in range(300)]
for i in range(1, 300, 2):
    for j in range(300):
        snake[i][j] = 1                       # walls on odd rows ...
    snake[i][299 if (i // 2) % 2 == 0 else 0] = 0   # ... with one gap alternating sides
out = flood_fill(snake, 0, 0, 9)
assert sum(v == 9 for row in out for v in row) == sum(v == 0 for row in snake for v in row)
try:
    brute(snake, 0, 0, 9)
except RecursionError:
    print('recursive DFS on the snake: RecursionError at limit', sys.getrecursionlimit())
print('iterative handled the snake of', sum(v == 9 for row in out for v in row), 'cells')
