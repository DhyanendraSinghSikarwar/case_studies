import random
import sys


def depth_sum_rec(x, depth=1):
    total = 0
    for e in x:                                      # plain loop: one frame per level
        total += e * depth if isinstance(e, int) else depth_sum_rec(e, depth + 1)
    return total


def depth_sum_stack(x):
    total = 0
    stack = [(x, 1)]
    while stack:
        lst, d = stack.pop()
        for e in lst:
            if isinstance(e, int):
                total += e * d
            else:
                stack.append((e, d + 1))
    return total


def chain(depth, value):
    x = [value]
    for _ in range(depth - 1):                       # built in a loop: no recursion needed
        x = [x]
    return x


def random_nested(rng, depth_left):
    out = []
    for _ in range(rng.randint(0, 4)):
        if depth_left > 0 and rng.random() < 0.4:
            out.append(random_nested(rng, depth_left - 1))
        else:
            out.append(rng.randint(-5, 9))
    return out


print("sys.getrecursionlimit() =", sys.getrecursionlimit(), "on Python", sys.version.split()[0])
for x, want in [([1, [4, [6]]], 27), ([[1, 1], 2, [1, 1]], 10)]:
    assert depth_sum_rec(x) == depth_sum_stack(x) == want
    print(x, "->", want)

deep = chain(5000, 7)
try:
    depth_sum_rec(deep)
    print("recursive version: no error (unexpected)")
except RecursionError as e:
    print("recursive version on depth 5000: RecursionError:", e)
print("explicit stack on depth 5000:", depth_sum_stack(deep))
assert depth_sum_stack(deep) == 35000

old = sys.getrecursionlimit()
sys.setrecursionlimit(10000)
try:
    print("recursive with the limit raised to 10000:", depth_sum_rec(deep))
finally:
    sys.setrecursionlimit(old)
print("limit restored to", sys.getrecursionlimit())

assert depth_sum_stack([]) == 0 and depth_sum_stack([[]]) == 0 and depth_sum_stack([[], [[]]]) == 0
assert depth_sum_stack([3]) == 3
assert depth_sum_stack([-1, [-1]]) == -3
assert depth_sum_stack(chain(100000, 1)) == 100000   # far beyond any recursion limit

rng = random.Random(25)
for _ in range(1000):
    x = random_nested(rng, 6)
    assert depth_sum_rec(x) == depth_sum_stack(x), x
print("random cross-check passed: 1000 random nested lists, depth up to 7")
