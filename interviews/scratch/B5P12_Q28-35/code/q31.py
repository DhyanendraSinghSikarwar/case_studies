import itertools
import random

random.seed(3101)


def run(c, prune, target, trace=None):
    """Version A (prune=False, c as given) or version B (prune=True, c must be sorted).
    Returns (calls, hits). If trace is a list, appends an indented line per call."""
    calls = hits = 0

    def dfs(start, rem, depth, label):
        nonlocal calls, hits
        calls += 1
        note = "rem<0 stop" if rem < 0 else "HIT" if rem == 0 else ""
        if trace is not None:
            trace.append("  " * depth + f"{label}rem={rem} {note}".rstrip())
        if rem < 0:
            return
        if rem == 0:
            hits += 1
            return
        for j in range(start, len(c)):
            if prune and c[j] > rem:
                break                        # sorted: every later candidate is at least as big
            dfs(j, rem - c[j], depth + 1, f"take {c[j]}: ")

    dfs(0, target, 0, "")
    return calls, hits


def solve(candidates, target):
    a, ha = run(list(candidates), False, target)
    b, hb = run(sorted(candidates), True, target)
    assert ha == hb
    return [a, b, ha]


def brute(candidates, target):
    """Same two rules with an explicit stack (no recursion), children pushed in reverse."""
    def go(c, prune):
        calls = hits = 0
        stack = [(0, target)]
        while stack:
            start, rem = stack.pop()
            calls += 1
            if rem < 0:
                continue
            if rem == 0:
                hits += 1
                continue
            for j in range(len(c) - 1, start - 1, -1):
                if prune and c[j] > rem:
                    continue                 # same as 'break' because c is sorted
                stack.append((j, rem - c[j]))
        return calls, hits
    a, ha = go(list(candidates), False)
    b, hb = go(sorted(candidates), True)
    return [a, b, ha]


# decision trees for candidates=[5, 2, 3], target=8
for name, c, prune in [("A (given order 5,2,3)", [5, 2, 3], False), ("B (sorted 2,3,5, with break)", [2, 3, 5], True)]:
    t = []
    calls, hits = run(c, prune, 8, t)
    print(f"--- {name}: {calls} calls, {hits} hits")
    print("\n".join(t))

for c, t, want in [([5, 2, 3], 8, [19, 13, 3]), ([7], 1, [2, 1, 0]), ([4, 2, 3, 1], 10, [102, 94, 23]), ([1], 5, [6, 6, 1])]:
    got = solve(c, t)
    assert got == want == brute(c, t), (c, t, got)
    print(c, t, "->", got)

big = [3, 5, 7, 11, 13, 17, 19, 20]
print("B saves a lot:", big, 40, "->", solve(big, 40))
print("B saves nothing:", [1], 5, "->", solve([1], 5), "| and", [20, 1], 40, "->", solve([20, 1], 40))

# why B <= A: B's calls are exactly the multisets with sum <= target (empty one = root); each also exists in A
def multisets_le(c, target):
    n = 0
    def go(start, total):
        nonlocal n
        n += 1
        for j in range(start, len(c)):
            if total + c[j] <= target:
                go(j, total + c[j])
    go(0, 0)
    return n

for _ in range(300):
    k = random.randint(1, 5)
    c = random.sample(range(1, 21), k)
    t = random.randint(1, 40)
    a, b, h = solve(c, t)
    assert b == multisets_le(sorted(c), t) and b <= a
    assert [a, b, h] == brute(c, t)
print("300 seeded random cases: B == #multisets with sum <= target, B <= A, hits agree, explicit stack agrees")

# exhaustive: every ordering of every 3-subset of 1..8, targets 1..16
cnt = 0
for cs in itertools.combinations(range(1, 9), 3):
    for perm in itertools.permutations(cs):
        for t in range(1, 17):
            a, ha = run(list(perm), False, t)
            b, hb = run(list(cs), True, t)
            assert b <= a and ha == hb
            cnt += 1
print("exhaustive over", cnt, "(ordering, target) cases: calls_B <= calls_A and hits agree")
assert solve([1], 40) == [41, 41, 1]
print("edge asserts ok (depth 41 for candidate 1, target 40)")
