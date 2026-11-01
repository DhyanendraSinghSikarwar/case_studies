import random


def trap_brute(height):
    # column view: water above column i = min(max to its left, max to its right) - height[i]. O(n^2)
    total = 0
    for i in range(len(height)):
        left = max(height[: i + 1])
        right = max(height[i:])
        total += min(left, right) - height[i]
    return total


def trap_stack(height):
    stack = []  # indices, heights non-increasing from bottom to top
    total = 0
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack:
                break                       # no left wall: nothing is held
            left = stack[-1]
            width = i - left - 1            # horizontal distance between the walls
            depth = min(h, height[left]) - height[bottom]   # one horizontal layer
            total += width * depth
        stack.append(i)
    return total


examples = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), ([4, 2, 0, 3, 2, 5], 9), ([3, 0, 2], 2), ([1, 2, 3], 0)]
for h, want in examples:
    got = trap_stack(h)
    assert got == trap_brute(h) == want, (h, got)
    print(h, "->", got)

assert trap_stack([]) == 0
assert trap_stack([5]) == 0
assert trap_stack([5, 5]) == 0
assert trap_stack([3, 3, 3, 3]) == 0                 # equal walls: nothing held
assert trap_stack([5, 0, 0, 0, 5]) == 15             # one wide basin
assert trap_stack([5, 0, 5, 0, 5]) == 10             # two basins
assert trap_stack([3, 0, 3, 0, 3, 0]) == 6           # trailing basin has no right wall
assert trap_stack([5, 4, 3, 2, 1]) == 0              # decreasing: nothing held
assert trap_stack([0, 3, 0, 3]) == 3
n = 20000
assert trap_stack([n] + [0] * (n - 2) + [n]) == n * (n - 2)   # max size

rng = random.Random(13)
cases = 0
for _ in range(3000):
    n = rng.randint(0, 14)
    h = [rng.randint(0, rng.choice([2, 4, 8])) for _ in range(n)]
    assert trap_stack(h) == trap_brute(h), h
    cases += 1
print("random cross-check passed:", cases, "cases")
