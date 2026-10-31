import random
from collections import Counter


def kdistinct_brute(s, k):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            seen.add(s[j])
            if len(seen) > k:
                break
            best = max(best, j - i + 1)
    return best


def kdistinct_window(s, k):
    if k <= 0:
        return 0
    count = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]
            left += 1
        best = max(best, right - left + 1)
    return best


print("eceba, 2:", kdistinct_window("eceba", 2), "(expected 3)")
print("aa, 1:", kdistinct_window("aa", 1), "(expected 2)")
print("abc, 0:", kdistinct_window("abc", 0), "(expected 0)")

# the stale-key bug: len(count) counts keys with value 0 too
def kdistinct_buggy(s, k):
    count = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


try:
    print("buggy on eceba,2 ->", kdistinct_buggy("eceba", 2))
except IndexError:
    print("buggy on eceba,2 -> IndexError (zero-count keys keep len(count) above k, left runs off the end)")

random.seed(25)
for _ in range(1000):
    n = random.randint(0, 12)
    s = "".join(random.choice("abcd") for _ in range(n))
    k = random.randint(0, 4)
    assert kdistinct_window(s, k) == kdistinct_brute(s, k), (s, k)
print("cross-check: 1000 seeded cases agree")

assert kdistinct_window("", 3) == 0
assert kdistinct_window("a", 1) == 1
assert kdistinct_window("abc", 5) == 3  # k above the alphabet size: whole string
assert kdistinct_window("aaaa", 1) == 4
assert kdistinct_window("abcabc", 3) == 6
big = "".join(random.choice("abcdefgh") for _ in range(50000))
assert kdistinct_window(big, 8) == 50000
assert kdistinct_window(big, 1) >= 1
print("edge asserts passed")
