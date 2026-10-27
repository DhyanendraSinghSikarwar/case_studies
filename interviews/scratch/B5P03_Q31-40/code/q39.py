import random


def brute_longest(s):
    """Leftmost longest palindromic substring, expand-around-centre, O(n^2)."""
    best = ""
    for c in range(2 * len(s) - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        cand = s[l + 1:r]
        if len(cand) > len(best):          # strict '>' keeps the leftmost on ties
            best = cand
    return best


def brute_count(s):
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1)
               if s[i:j] == s[i:j][::-1])


def manacher(s):
    """Returns (leftmost longest palindrome, count of palindromic substrings, radii)."""
    if not s:
        return "", 0, []
    t = "#" + "#".join(s) + "#"          # every palindrome in t has odd length
    n = len(t)
    rad = [0] * n                         # rad[i] = palindrome radius at centre i in t
    centre = right = 0                    # rightmost palindrome found: centre, and its right edge
    for i in range(n):
        if i < right:
            rad[i] = min(right - i, rad[2 * centre - i])   # start from the mirror's radius
        # expand only when we may have reached or passed the right edge
        while (i - rad[i] - 1 >= 0 and i + rad[i] + 1 < n
               and t[i - rad[i] - 1] == t[i + rad[i] + 1]):
            rad[i] += 1
        if i + rad[i] > right:            # new rightmost palindrome
            centre, right = i, i + rad[i]
    # radius in t equals palindrome length in s
    best_len, best_c = max((r, -i) for i, r in enumerate(rad))   # ties: smallest i => leftmost
    best_c = -best_c
    start = (best_c - best_len) // 2
    count = sum((r + 1) // 2 for r in rad)   # palindromes centred at i: ceil(r / 2)
    return s[start:start + best_len], count, rad


for s in ["babad", "abacdfgdcaba"]:
    print(s, "->", manacher(s)[0])
print("count 'aaa' ->", manacher("aaa")[1])
print("radii of 'aba' in '#a#b#a#':", manacher("aba")[2])
assert manacher("babad")[0] == "bab"
assert manacher("abacdfgdcaba")[0] == "aba"
assert manacher("aaa")[1] == 6
assert manacher("") == ("", 0, [])
assert manacher("a")[:2] == ("a", 1)
assert manacher("ab")[:2] == ("a", 2)          # leftmost on ties
assert manacher("abba")[:2] == ("abba", 6)
assert manacher("cbbd")[0] == "bb"
assert manacher("a" * 1000)[1] == 1000 * 1001 // 2
assert manacher("abc" * 100)[0] == "a"

rng = random.Random(39)
for _ in range(4000):
    s = "".join(rng.choice("ab" if rng.random() < 0.6 else "abc") for _ in range(rng.randint(0, 14)))
    got, cnt, _ = manacher(s)
    assert got == brute_longest(s), (s, got, brute_longest(s))
    assert cnt == brute_count(s), s
print("random cross-check passed: 4000 cases")


# amortisation evidence: count inner while-loop expansions (successful extra matches)
def expansions(s):
    t = "#" + "#".join(s) + "#"
    n = len(t)
    rad = [0] * n
    centre = right = 0
    work = 0
    for i in range(n):
        if i < right:
            rad[i] = min(right - i, rad[2 * centre - i])
        while (i - rad[i] - 1 >= 0 and i + rad[i] + 1 < n
               and t[i - rad[i] - 1] == t[i + rad[i] + 1]):
            rad[i] += 1
            work += 1
        if i + rad[i] > right:
            centre, right = i, i + rad[i]
    return work, n


for name, s in [("a*1000", "a" * 1000), ("ab*500", "ab" * 500), ("random", "".join(rng.choice("ab") for _ in range(1000)))]:
    w, n = expansions(s)
    print(f"{name}: len(t)={n}, successful expansions={w}, bound 'right edge moves only forward' => <= {n}")
    assert w <= n
