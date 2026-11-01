import random
import re
from functools import cache


def wildcard_brute(s, p):
    """Memoised recursion (the DP idea), used as the reference."""
    @cache
    def m(i, j):
        if j == len(p):
            return i == len(s)
        if p[j] == "*":
            return m(i, j + 1) or (i < len(s) and m(i + 1, j))
        return i < len(s) and (p[j] == "?" or p[j] == s[i]) and m(i + 1, j + 1)
    return m(0, 0)


def wildcard_regex(s, p):
    """Independent reference: translate to a regex ('*' -> '.*', '?' -> '.')."""
    rx = "".join(".*" if c == "*" else "." if c == "?" else re.escape(c) for c in p)
    return re.fullmatch(rx, s, re.DOTALL) is not None


def wildcard(s, p):
    i = j = 0
    star = -1                 # index of the last '*' in p
    mark = 0                  # index in s where that star's current match attempt started
    while i < len(s):
        if j < len(p) and (p[j] == "?" or p[j] == s[i]):
            i += 1
            j += 1
        elif j < len(p) and p[j] == "*":
            star = j          # remember the star, let it match empty for now
            mark = i
            j += 1
        elif star != -1:      # mismatch: backtrack, star absorbs one more char
            mark += 1
            i = mark
            j = star + 1
        else:
            return False
    while j < len(p) and p[j] == "*":   # leftover pattern may only be stars
        j += 1
    return j == len(p)


cases = [("aa", "a", False), ("aa", "*", True), ("cb", "?a", False),
         ("adceb", "*a*b", True), ("acdcb", "a*c?b", False), ("", "*", True)]
for s, p, want in cases:
    got = wildcard(s, p)
    print(repr(s), repr(p), got)
    assert got is want

assert wildcard("", "") is True
assert wildcard("a", "") is False
assert wildcard("", "?") is False
assert wildcard("abc", "***") is True
assert wildcard("abc", "a*c") is True
assert wildcard("abc", "a?c") is True
assert wildcard("mississippi", "m??*ss*?i*pi") is False
assert wildcard("abcabczzzde", "*abc???de*") is True
assert wildcard("a" * 2000, "*" * 1000 + "a" * 1000) is True

# worst case for the backtracking: many near-matches, still O(n*m), here counted
def wildcard_counting(s, p):
    steps = 0
    i = j = 0
    star = -1
    mark = 0
    while i < len(s):
        steps += 1
        if j < len(p) and (p[j] == "?" or p[j] == s[i]):
            i += 1; j += 1
        elif j < len(p) and p[j] == "*":
            star = j; mark = i; j += 1
        elif star != -1:
            mark += 1; i = mark; j = star + 1
        else:
            return False, steps
    while j < len(p) and p[j] == "*":
        j += 1
    return j == len(p), steps


n = 1000
s = "a" * n
p = "*" + "a" * (n // 2) + "b"
print("adversarial n=%d, pattern length %d: result, loop steps" % (n, len(p)), wildcard_counting(s, p))

rng = random.Random(38)
for _ in range(6000):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 7)))
    p = "".join(rng.choice("ab?**") for _ in range(rng.randint(0, 7)))
    r = wildcard(s, p)
    assert r == wildcard_brute(s, p) == wildcard_regex(s, p), (s, p)
print("random cross-check passed: 6000 cases")
