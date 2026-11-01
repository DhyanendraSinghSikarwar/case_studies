import random


def anagram_starts_brute(s, p):
    k = len(p)
    want = sorted(p)
    return [i for i in range(len(s) - k + 1) if sorted(s[i:i + k]) == want]


def anagram_starts_arrays(s, p):
    # compare two 26-length lists each step: O(26 * n)
    k = len(p)
    if k > len(s):
        return []
    need, have = [0] * 26, [0] * 26
    for c in p:
        need[ord(c) - 97] += 1
    out = []
    for r, c in enumerate(s):
        have[ord(c) - 97] += 1
        if r >= k:
            have[ord(s[r - k]) - 97] -= 1
        if r >= k - 1 and have == need:
            out.append(r - k + 1)
    return out


def anagram_starts(s, p):
    # O(1) per step: 'diff' = number of letters whose counts differ
    k = len(p)
    if k > len(s):
        return []
    cnt = [0] * 26                      # cnt[x] = window count - needed count
    for c in p:
        cnt[ord(c) - 97] -= 1
    diff = sum(1 for v in cnt if v != 0)
    out = []

    def bump(idx, delta):
        nonlocal diff
        if cnt[idx] == 0:
            diff += 1                   # was equal, about to differ
        cnt[idx] += delta
        if cnt[idx] == 0:
            diff -= 1                   # became equal

    for r, c in enumerate(s):
        bump(ord(c) - 97, 1)
        if r >= k:
            bump(ord(s[r - k]) - 97, -1)
        if r >= k - 1 and diff == 0:
            out.append(r - k + 1)
    return out


print(anagram_starts("cbaebabacd", "abc"))
print(anagram_starts("abab", "ab"))
assert anagram_starts("cbaebabacd", "abc") == [0, 6]
assert anagram_starts("abab", "ab") == [0, 1, 2]
assert anagram_starts("a", "ab") == []                 # p longer than s
assert anagram_starts("aaaa", "aa") == [0, 1, 2]       # overlapping matches
assert anagram_starts("abc", "abc") == [0]
assert anagram_starts("abc", "d") == []
assert anagram_starts("a" * 30000, "a" * 30000) == [0]
assert anagram_starts_arrays("abab", "ab") == [0, 1, 2]

rng = random.Random(4)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 10)))
    p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
    want = anagram_starts_brute(s, p)
    assert anagram_starts(s, p) == want and anagram_starts_arrays(s, p) == want, (s, p)
    cases += 1
print("random cross-check passed:", cases, "cases")
