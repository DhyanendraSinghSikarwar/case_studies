import random
from collections import Counter

def brute(s, words):
    if not words: return []
    L, m = len(words[0]), len(words)
    need = Counter(words)
    out = []
    for i in range(len(s) - L * m + 1):
        chunks = [s[i + t * L: i + (t + 1) * L] for t in range(m)]
        if Counter(chunks) == need:
            out.append(i)
    return out

def find_concat(s, words):
    if not words or not s: return []
    L, m, n = len(words[0]), len(words), len(s)
    need = Counter(words)
    out = []
    for off in range(L):                       # L independent word-aligned scans
        have = Counter()
        left, matched = off, 0                 # matched = number of words inside the window
        for right in range(off, n - L + 1, L):
            w = s[right:right + L]
            if w not in need:                  # a foreign word breaks every window across it
                have.clear(); matched = 0; left = right + L
                continue
            have[w] += 1; matched += 1
            while have[w] > need[w]:           # too many copies of w: drop from the left
                have[s[left:left + L]] -= 1
                matched -= 1; left += L
            if matched == m:
                out.append(left)
                have[s[left:left + L]] -= 1    # slide one word so the scan continues
                matched -= 1; left += L
    return sorted(out)

for s, ws, exp in [("barfoothefoobarman", ["foo", "bar"], [0, 9]),
                   ("wordgoodgoodgoodbestword", ["word", "good", "best", "word"], []),
                   ("barfoofoobarthefoobarman", ["bar", "foo", "the"], [6, 9, 12])]:
    assert find_concat(s, ws) == brute(s, ws) == exp
    print(repr(s), ws, "->", find_concat(s, ws))
assert find_concat("", ["a"]) == [] and find_concat("aaa", []) == [] and find_concat("a", ["ab"]) == []
assert find_concat("aaaa", ["a", "a"]) == [0, 1, 2] and find_concat("abab", ["ab", "ab"]) == [0] and find_concat("abbaab", ["ab", "ba"]) == [0, 2]
assert find_concat("lingmindraboofooowingdingbarrwingmonkeypoundcake", ["fooo", "barr", "wing", "ding", "wing"]) == [13]
random.seed(41)
for _ in range(1500):
    L = random.randint(1, 3)
    pool = ["".join(random.choice("ab") for _ in range(L)) for _ in range(3)]
    words = [random.choice(pool) for _ in range(random.randint(1, 4))]
    s = "".join(random.choice(pool) for _ in range(random.randint(0, 9)))
    if random.random() < 0.3 and s:
        i = random.randrange(len(s)); s = s[:i] + random.choice("abc") + s[i + 1:]
    assert find_concat(s, words) == brute(s, words), (s, words)
print("1500 seeded cases match brute force; edges pass")
