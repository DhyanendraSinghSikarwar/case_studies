import random
from collections import Counter


def replace_brute(s, k):
    best = 0
    for i in range(len(s)):
        cnt = Counter()
        for j in range(i, len(s)):
            cnt[s[j]] += 1
            if (j - i + 1) - max(cnt.values()) <= k:
                best = max(best, j - i + 1)
    return best


def replace_window(s, k):
    cnt = [0] * 26
    left = max_f = 0
    for r, c in enumerate(s):
        i = ord(c) - 65
        cnt[i] += 1
        max_f = max(max_f, cnt[i])          # stale: never lowered on shrink
        if (r - left + 1) - max_f > k:      # window invalid: slide by one (do not grow)
            cnt[ord(s[left]) - 65] -= 1
            left += 1
    return len(s) - left                    # window never shrinks in size once it grew


def replace_window_exact(s, k):
    # same idea but recomputes the real max each step (O(26 n)), to compare with the stale version
    cnt = [0] * 26
    left = best = 0
    for r, c in enumerate(s):
        cnt[ord(c) - 65] += 1
        while (r - left + 1) - max(cnt) > k:
            cnt[ord(s[left]) - 65] -= 1
            left += 1
        best = max(best, r - left + 1)
    return best


print(replace_window("AABABBA", 1))
print(replace_window("ABAB", 2))
assert replace_window("AABABBA", 1) == 4
assert replace_window("ABAB", 2) == 4
assert replace_window("A", 0) == 1
assert replace_window("ABC", 0) == 1                # k = 0: longest run
assert replace_window("AAAA", 0) == 4
assert replace_window("ABCD", 10) == 4              # k >= len: whole string
assert replace_window("AAAB" * 25000, 1) == replace_window_exact("AAAB" * 25000, 1)

rng = random.Random(12)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 11)))
    k = rng.randint(0, 4)
    want = replace_brute(s, k)
    assert replace_window(s, k) == want, (s, k)
    assert replace_window_exact(s, k) == want, (s, k)
    cases += 1
print("random cross-check passed:", cases, "cases")
