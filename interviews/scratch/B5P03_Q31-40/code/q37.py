import random
from collections import Counter
from itertools import product


def min_steps_brute(s, t):
    """Try every string t2 of the same length reachable by changing k positions; pick the
    smallest k with sorted(t2) == sorted(s). Exponential, tiny inputs only."""
    n = len(t)
    best = n
    alphabet = sorted(set(s) | set(t))
    for t2 in product(alphabet, repeat=n):
        if sorted(t2) == sorted(s):
            k = sum(1 for x, y in zip(t, t2) if x != y)
            best = min(best, k)
    return best


def min_steps(s, t):
    diff = Counter(s)
    diff.subtract(Counter(t))                 # diff[c] = count in s minus count in t
    return sum(v for v in diff.values() if v > 0)


cases = [("bab", "aba", 1), ("leetcode", "practice", 5), ("anagram", "mangaar", 0)]
for s, t, want in cases:
    got = min_steps(s, t)
    print(s, t, got)
    assert got == want

assert min_steps("", "") == 0
assert min_steps("a", "a") == 0
assert min_steps("a", "b") == 1
assert min_steps("aaaa", "bbbb") == 4
assert min_steps("abc", "cba") == 0
assert min_steps("a" * 50000, "b" * 50000) == 50000
# symmetry: surplus on one side equals surplus on the other
assert min_steps("leetcode", "practice") == min_steps("practice", "leetcode")

rng = random.Random(37)
for _ in range(400):
    n = rng.randint(0, 5)
    s = "".join(rng.choice("abc") for _ in range(n))
    t = "".join(rng.choice("abc") for _ in range(n))
    assert min_steps(s, t) == min_steps_brute(s, t), (s, t)
    assert min_steps(s, t) == min_steps(t, s)
print("random cross-check passed: 400 cases")
