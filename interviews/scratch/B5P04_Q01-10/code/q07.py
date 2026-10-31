import random


def daily_brute(temps):
    n = len(temps)
    res = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temps[j] > temps[i]:
                res[i] = j - i
                break
    return res


def daily_stack(temps):
    n = len(temps)
    res = [0] * n
    stack = []                                 # indices; temps[stack] is non-increasing bottom to top
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:  # strictly warmer: today answers these days
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res                                 # indices left on the stack keep 0


def daily_jump(temps):
    # right-to-left with jump pointers: follow answers instead of a stack
    n = len(temps)
    res = [0] * n
    for i in range(n - 2, -1, -1):
        j = i + 1
        while j < n and temps[j] <= temps[i]:
            if res[j] == 0:                    # j has no warmer day, so neither does i
                j = n
                break
            j += res[j]                        # jump straight to j's next warmer day
        if j < n:
            res[i] = j - i
    return res


examples = [([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
            ([30, 40, 50, 60], [1, 1, 1, 0]),
            ([30, 60, 90], [1, 1, 0])]
for temps, want in examples:
    assert daily_brute(temps) == daily_stack(temps) == daily_jump(temps) == want, temps
    print(temps, "->", daily_stack(temps))

# edge cases
assert daily_stack([50]) == [0]
assert daily_stack([50, 50, 50]) == [0, 0, 0]          # equal is NOT warmer
assert daily_stack([90, 80, 70]) == [0, 0, 0]          # strictly decreasing
assert daily_stack([-5, -3, -4, 0]) == [1, 2, 1, 0]    # negatives
n = 100_000
assert daily_stack(list(range(n))) == [1] * (n - 1) + [0]      # max size, all pushes and pops
assert daily_jump(list(range(n, 0, -1))) == [0] * n            # max size, nothing resolves

# seeded randomised cross-check (small range => many ties)
rng = random.Random(99)
for _ in range(1500):
    temps = [rng.randint(-3, 6) for _ in range(rng.randint(1, 14))]
    want = daily_brute(temps)
    assert daily_stack(temps) == want, temps
    assert daily_jump(temps) == want, temps
print("random cross-check passed: 1500 cases")
