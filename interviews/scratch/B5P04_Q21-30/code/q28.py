import random
from itertools import product


def max_rect_brute(matrix):
    r = len(matrix)
    if r == 0:
        return 0
    c = len(matrix[0])
    pre = [[0] * (c + 1) for _ in range(r + 1)]
    for i in range(r):
        for j in range(c):
            pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] - pre[i][j] + (matrix[i][j] == "1")
    best = 0
    for i1 in range(r):
        for i2 in range(i1, r):
            for j1 in range(c):
                for j2 in range(j1, c):
                    area = (i2 - i1 + 1) * (j2 - j1 + 1)
                    ones = pre[i2 + 1][j2 + 1] - pre[i1][j2 + 1] - pre[i2 + 1][j1] + pre[i1][j1]
                    if ones == area:
                        best = max(best, area)
    return best


def largest_in_histogram(h):
    stack = []                                       # indices, heights strictly increasing
    best = 0
    for i in range(len(h) + 1):
        cur = h[i] if i < len(h) else 0              # sentinel flushes the stack
        while stack and h[stack[-1]] >= cur:
            height = h[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best


def max_rect(matrix):
    if not matrix:
        return 0
    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for j, ch in enumerate(row):
            heights[j] = heights[j] + 1 if ch == "1" else 0
        best = max(best, largest_in_histogram(heights))
    return best


examples = [(["10100", "10111", "11111", "10010"], 6), (["0"], 0), (["1"], 1), (["11", "11"], 4)]
for m, want in examples:
    got = max_rect(m)
    assert got == max_rect_brute(m) == want, (m, got)
    print(m, "->", got)

assert max_rect([]) == 0
assert max_rect(["1" * 200] * 200) == 40000
assert max_rect(["0" * 200] * 200) == 0
assert max_rect(["10" * 100] * 200) == 200
assert max_rect(["1111", "0000", "1111"]) == 4
assert largest_in_histogram([2, 1, 5, 6, 2, 3]) == 10

total = 0
for t in product("01", repeat=12):                   # every 3 x 4 matrix
    m = ["".join(t[0:4]), "".join(t[4:8]), "".join(t[8:12])]
    assert max_rect(m) == max_rect_brute(m), m
    total += 1
rng = random.Random(28)
for _ in range(500):
    r, c = rng.randint(1, 6), rng.randint(1, 6)
    m = ["".join(rng.choice("0111") for _ in range(c)) for _ in range(r)]
    assert max_rect(m) == max_rect_brute(m), m
    total += 1
print("cross-check passed:", total, "matrices (all 4096 of size 3x4, plus 500 random up to 6x6)")
