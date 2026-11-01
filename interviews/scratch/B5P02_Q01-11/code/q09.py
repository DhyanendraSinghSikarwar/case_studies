import random
from collections import Counter


def perm_brute(s1, s2):
    k = len(s1)
    want = sorted(s1)
    return any(sorted(s2[i:i + k]) == want for i in range(len(s2) - k + 1))


def perm_window(s1, s2):
    k = len(s1)
    if k > len(s2):
        return False
    need = [0] * 26
    have = [0] * 26
    for c in s1:
        need[ord(c) - 97] += 1
    matches = 0                         # how many of the 26 letters have have == need

    def bump(idx, delta):
        nonlocal matches
        if have[idx] == need[idx]:
            matches -= 1                # was matching, about to change
        have[idx] += delta
        if have[idx] == need[idx]:
            matches += 1                # matches after the change

    for i in range(26):
        if need[i] == 0:
            matches += 1                # 0 == 0 matches at the start
    for r, c in enumerate(s2):
        bump(ord(c) - 97, 1)
        if r >= k:
            bump(ord(s2[r - k]) - 97, -1)
        if matches == 26:
            return True
    return False


print(perm_window("ab", "eidbaooo"))
print(perm_window("ab", "eidboaoo"))
assert perm_window("ab", "eidbaooo") is True
assert perm_window("ab", "eidboaoo") is False
assert perm_window("a", "a") is True
assert perm_window("ab", "a") is False                 # s1 longer than s2
assert perm_window("abc", "abc") is True               # whole string
assert perm_window("aab", "abab") is True              # repeats: counts matter
assert perm_window("aab", "abba") is False
assert perm_window("z" * 5000, "z" * 10000) is True    # max size

rng = random.Random(17)
cases = 0
for _ in range(3000):
    s1 = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
    s2 = "".join(rng.choice("abc") for _ in range(rng.randint(1, 9)))
    assert perm_window(s1, s2) == perm_brute(s1, s2), (s1, s2)
    cases += 1
print("random cross-check passed:", cases, "cases")
