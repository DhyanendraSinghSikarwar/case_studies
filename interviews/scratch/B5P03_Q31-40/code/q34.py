import random


def one_edit_brute(s, t):
    """Reference: try every single edit of s and compare with t (O(n^2))."""
    letters = set(s) | set(t) | {"z"}
    for i in range(len(s)):
        if s[:i] + s[i + 1:] == t:                         # delete
            return True
        for c in letters:
            if c != s[i] and s[:i] + c + s[i + 1:] == t:   # replace
                return True
    for i in range(len(s) + 1):
        for c in letters:
            if s[:i] + c + s[i:] == t:                     # insert
                return True
    return False


def same_from(s, i, t, j):
    """True if s[i:] == t[j:], compared by index so no slice copy (keeps O(1) extra space)."""
    if len(s) - i != len(t) - j:
        return False
    while i < len(s):
        if s[i] != t[j]:
            return False
        i += 1
        j += 1
    return True


def one_edit(s, t):
    if len(s) > len(t):                  # make s the shorter one
        s, t = t, s
    ls, lt = len(s), len(t)
    if lt - ls > 1:
        return False
    for i in range(ls):
        if s[i] != t[i]:
            if ls == lt:
                return same_from(s, i + 1, t, i + 1)   # replace: remainders equal
            return same_from(s, i, t, i + 1)       # insert into s: skip t[i]
    return lt - ls == 1                             # no mismatch: need exactly one extra char


cases = [("ab", "acb", True), ("cab", "ad", False), ("1203", "1213", True),
         ("", "", False), ("a", "", True), ("ab", "ab", False)]
for s, t, want in cases:
    got = one_edit(s, t)
    print(repr(s), repr(t), got)
    assert got is want and one_edit_brute(s, t) is want

assert one_edit("", "a") is True
assert one_edit("a", "b") is True                  # replace single char
assert one_edit("ab", "ba") is False               # two replacements
assert one_edit("abc", "ab") is True               # delete last
assert one_edit("abc", "bc") is True               # delete first
assert one_edit("abc", "abcd") is True             # insert at end
assert one_edit("abc", "abcde") is False           # length gap 2
assert one_edit("aab", "ab") is True               # duplicates
assert one_edit("a" * 10000, "a" * 9999 + "b") is True

rng = random.Random(34)
for _ in range(5000):
    n = rng.randint(0, 6)
    s = "".join(rng.choice("abc") for _ in range(n))
    t = "".join(rng.choice("abc") for _ in range(max(0, n + rng.randint(-2, 2))))
    assert one_edit(s, t) == one_edit_brute(s, t), (s, t)
    assert one_edit(s, t) == one_edit(t, s)
print("random cross-check passed: 5000 cases")
