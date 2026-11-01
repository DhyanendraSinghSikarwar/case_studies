import random


def lps_brute(s):
    best = ""
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            t = s[i:j]
            if len(t) > len(best) and t == t[::-1]:      # strict > keeps the leftmost
                best = t
    return best


def lps_expand(s):
    start, best = 0, 1

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - l - 1                          # start, length

    for c in range(len(s)):
        for l, r in ((c, c), (c, c + 1)):                # odd centre, even centre
            st, ln = expand(l, r)
            if ln > best:                                # strict: ties keep the leftmost
                start, best = st, ln
    return s[start:start + best]


examples = [("babad", "bab"), ("cbbd", "bb"), ("a", "a"), ("abacdfgdcaba", "aba")]
for s, want in examples:
    assert lps_expand(s) == lps_brute(s) == want, (s, lps_expand(s), want)
    print(repr(s), "->", repr(want))

assert lps_expand("ab") == "a"
assert lps_expand("aa") == "aa"
assert lps_expand("aaaa") == "aaaa"
assert lps_expand("abcd") == "a"
assert lps_expand("racecar") == "racecar"
assert lps_expand("xabbay") == "abba"
assert lps_expand("z" * 1000) == "z" * 1000
s = "ab" * 500
assert lps_expand(s) == "ab" * 499 + "a"             # len 999, starts at 0

rng = random.Random(21)
cases = 0
for _ in range(4000):
    s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 12)))
    assert lps_expand(s) == lps_brute(s), s
    cases += 1
for _ in range(2000):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 14)))
    assert lps_expand(s) == lps_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
