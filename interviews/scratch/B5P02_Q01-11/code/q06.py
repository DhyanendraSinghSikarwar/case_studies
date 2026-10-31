import random


def longest_brute(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best


def longest_last_seen(s):
    last = {}              # char -> index of its latest occurrence
    left = best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= left:   # the >= left test stops the left edge going backwards
            left = last[c] + 1
        last[c] = r
        best = max(best, r - left + 1)
    return best


def longest_set(s):
    seen = set()
    left = best = 0
    for r, c in enumerate(s):
        while c in seen:               # shrink until c is free
            seen.remove(s[left])
            left += 1
        seen.add(c)
        best = max(best, r - left + 1)
    return best


for s, want in [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), ("abba", 2)]:
    a, b = longest_last_seen(s), longest_set(s)
    assert a == b == longest_brute(s) == want, (s, a, b, want)
    print(repr(s), "->", a)

assert longest_last_seen("a") == 1
assert longest_last_seen("abcdef") == 6            # all distinct
assert longest_last_seen("tmmzuxt") == 5           # old 't' is left of the window: do not move left back
assert longest_last_seen("dvdf") == 3
assert longest_last_seen("ab" * 25000) == 2        # max size
assert longest_set("ab" * 25000) == 2
assert longest_last_seen("a b a") == 3

rng = random.Random(14)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 12)))
    want = longest_brute(s)
    assert longest_last_seen(s) == want and longest_set(s) == want, s
    cases += 1
print("random cross-check passed:", cases, "cases")
