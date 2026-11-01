import random


def largest_brute(h):
    # try every pair of edges (i, j): width * lowest bar between them. O(n^2)
    best = 0
    for i in range(len(h)):
        low = h[i]
        for j in range(i, len(h)):
            low = min(low, h[j])
            best = max(best, low * (j - i + 1))
    return best


def largest_stack(heights):
    hs = heights + [0]          # sentinel bar of height 0 flushes the stack at the end
    stack = []                  # indices, heights strictly increasing from bottom to top
    best = 0
    for i, cur in enumerate(hs):
        while stack and hs[stack[-1]] >= cur:
            height = hs[stack.pop()]
            left = stack[-1] if stack else -1       # new top = nearest smaller bar on the left
            best = max(best, height * (i - left - 1))  # right edge is i (exclusive)
        stack.append(i)
    return best


examples = [([2, 1, 5, 6, 2, 3], 10), ([2, 4], 4), ([1, 1, 1, 1], 4), ([0], 0), ([6, 2, 5, 4, 5, 1, 6], 12)]
for h, want in examples:
    got = largest_stack(h)
    assert got == largest_brute(h) == want, (h, got)
    print(h, "->", got)

assert largest_stack([]) == 0
assert largest_stack([7]) == 7
assert largest_stack([0, 0, 0]) == 0
assert largest_stack([5, 5, 5, 5, 5]) == 25          # all equal: ties popped, still right
assert largest_stack([1, 2, 3, 4, 5]) == 9           # increasing: flushed by the sentinel
assert largest_stack([5, 4, 3, 2, 1]) == 9           # decreasing: pops on every step
assert largest_stack([2, 0, 2]) == 2                 # a zero splits the histogram
big = [10 ** 9] * 100000
assert largest_stack(big) == 10 ** 9 * 100000        # max size, no overflow in Python

rng = random.Random(12)
cases = 0
for _ in range(3000):
    n = rng.randint(0, 12)
    h = [rng.randint(0, rng.choice([2, 5, 9])) for _ in range(n)]
    assert largest_stack(h) == largest_brute(h), h
    cases += 1
print("random cross-check passed:", cases, "cases")
