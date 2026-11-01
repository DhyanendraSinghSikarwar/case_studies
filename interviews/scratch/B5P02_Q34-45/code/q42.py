import random

def is_subseq(t, w):
    it = iter(w)
    return all(c in it for c in t)

def brute(s, t):
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if is_subseq(t, s[i:j]) and (best == "" or j - i < len(best)):
                best = s[i:j]
                break                      # shortest from this i; strict < keeps leftmost on ties
    return best

def min_window_subseq(s, t):
    if not t: return ""
    n, m = len(s), len(t)
    i = 0
    best_start, best_len = -1, n + 1
    while i < n:
        j = 0
        while i < n:                       # forward: complete the match
            if s[i] == t[j]:
                j += 1
                if j == m: break
            i += 1
        if i == n: break                   # could not finish a match
        end = i
        j = m - 1
        while j >= 0:                      # backward: tighten the left edge
            if s[i] == t[j]: j -= 1
            i -= 1
        i += 1
        if end - i + 1 < best_len:
            best_start, best_len = i, end - i + 1
        i += 1                             # restart one past the tightened left edge
    return "" if best_start < 0 else s[best_start:best_start + best_len]

for s, t, exp in [("abcdebdde", "bde", "bcde"), ("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u", "")]:
    assert min_window_subseq(s, t) == brute(s, t) == exp
    print(repr(s), repr(t), "->", repr(min_window_subseq(s, t)))
assert min_window_subseq("", "a") == "" and min_window_subseq("abc", "") == "" and min_window_subseq("a", "a") == "a"
assert min_window_subseq("abc", "abcd") == "" and min_window_subseq("aaab", "ab") == "ab" and min_window_subseq("cnhczmccqouqadqtmjjzl", "mm") == "mccqouqadqtm"
assert min_window_subseq("abab", "ab") == "ab"          # tie: leftmost
random.seed(42)
for _ in range(2000):
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 12)))
    t = "".join(random.choice("abc") for _ in range(random.randint(0, 4)))
    if t == "": continue
    assert min_window_subseq(s, t) == brute(s, t), (s, t)
print("2000 seeded cases match brute force; edges pass")
