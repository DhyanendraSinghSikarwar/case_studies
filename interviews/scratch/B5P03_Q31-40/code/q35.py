import random
import sys
from functools import cache
from itertools import combinations, product


def edit_distance(a, b):
    @cache
    def d(i, j):                       # distance between a[:i] and b[:j]
        if i == 0:
            return j                   # insert j chars
        if j == 0:
            return i                   # delete i chars
        if a[i - 1] == b[j - 1]:
            return d(i - 1, j - 1)     # last chars equal: free
        return 1 + min(d(i - 1, j),        # delete a[i-1]
                       d(i, j - 1),        # insert b[j-1]
                       d(i - 1, j - 1))    # replace
    return d(len(a), len(b))


def lcs(a, b):
    @cache
    def f(i, j):                       # LCS length of a[:i] and b[:j]
        if i == 0 or j == 0:
            return 0
        if a[i - 1] == b[j - 1]:
            return 1 + f(i - 1, j - 1)
        return max(f(i - 1, j), f(i, j - 1))
    return f(len(a), len(b))


def indel_distance(a, b):
    return len(a) + len(b) - 2 * lcs(a, b)


print(edit_distance("horse", "ros"))
print(edit_distance("intention", "execution"))
print(lcs("abcde", "ace"))
print(lcs("abc", "def"))
print(indel_distance("horse", "ros"))
assert edit_distance("horse", "ros") == 3
assert edit_distance("intention", "execution") == 5
assert lcs("abcde", "ace") == 3
assert lcs("abc", "def") == 0
assert indel_distance("horse", "ros") == 4
assert edit_distance("", "") == 0 and edit_distance("", "abc") == 3 and edit_distance("abc", "") == 3
assert lcs("", "abc") == 0 and lcs("aaa", "aa") == 2

# subsequence versus substring
print("lcs('abcde','ace') =", lcs("abcde", "ace"))


def longest_common_substring(a, b):
    return max((k for k in range(min(len(a), len(b)) + 1)
                if any(a[i:i + k] in b for i in range(len(a) - k + 1))), default=0)


print("longest common substring('abcde','ace') =", longest_common_substring("abcde", "ace"))
assert longest_common_substring("abcde", "ace") == 1


# brute-force references on tiny strings
def subsequences(s):
    for k in range(len(s) + 1):
        for idx in combinations(range(len(s)), k):
            yield "".join(s[i] for i in idx)


def lcs_brute(a, b):
    sb = set(subsequences(b))
    return max(len(x) for x in subsequences(a) if x in sb)


def edit_brute(a, b):
    """Breadth-first search over edit operations; independent of the recurrence."""
    letters = sorted(set(a) | set(b))
    frontier, seen, steps = {a}, {a}, 0
    while b not in frontier:
        nxt = set()
        for s in frontier:
            for i in range(len(s)):
                nxt.add(s[:i] + s[i + 1:])
                for c in letters:
                    nxt.add(s[:i] + c + s[i + 1:])
            for i in range(len(s) + 1):
                for c in letters:
                    nxt.add(s[:i] + c + s[i:])
        frontier = nxt - seen
        seen |= nxt
        steps += 1
    return steps


rng = random.Random(35)
for _ in range(300):
    a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
    b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
    assert lcs(a, b) == lcs_brute(a, b), (a, b)
    assert edit_distance(a, b) == edit_brute(a, b), (a, b)
    assert indel_distance(a, b) >= edit_distance(a, b)          # indel-only can only cost more
    assert edit_distance(a, b) == edit_distance(b, a) and lcs(a, b) == lcs(b, a)
print("random cross-check passed: 300 pairs")

# memoised recursion depth: Python's recursion limit
print("recursion limit", sys.getrecursionlimit())
try:
    edit_distance("a" * 2000, "b" * 2000)
except RecursionError:
    print("RecursionError at length 2000 with default limit")
