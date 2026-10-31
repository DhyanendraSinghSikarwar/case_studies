import random
from bisect import bisect_left
from collections import defaultdict

def brute(s, t):
    # try every way: recursive match
    def go(i, j):
        if i == len(s):
            return True
        if j == len(t):
            return False
        return (s[i] == t[j] and go(i + 1, j + 1)) or go(i, j + 1)
    return go(0, 0)

def optimal(s, t):
    i = 0
    for ch in t:
        if i < len(s) and s[i] == ch:
            i += 1
    return i == len(s)

class Index:
    """Follow-up: many queries against one t. Precompute positions per letter."""
    def __init__(self, t):
        self.pos = defaultdict(list)
        for i, ch in enumerate(t):
            self.pos[ch].append(i)

    def is_subsequence(self, s):
        prev = -1                      # index in t of the last matched character
        for ch in s:
            lst = self.pos.get(ch)
            if not lst:
                return False
            k = bisect_left(lst, prev + 1)     # first occurrence strictly after prev
            if k == len(lst):
                return False
            prev = lst[k]
        return True

assert optimal('ace', 'abcde') is True
assert optimal('aec', 'abcde') is False
assert optimal('', 'x') is True
assert optimal('', '') is True
assert optimal('a', '') is False
assert optimal('abc', 'abc') is True
assert optimal('abcd', 'abc') is False      # s longer than t
assert optimal('aa', 'a') is False          # each char of t used once
assert optimal('aa', 'aba') is True

rng = random.Random(17)
for _ in range(1000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 5)))
    t = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
    want = brute(s, t)
    assert optimal(s, t) == want, (s, t)
    assert Index(t).is_subsequence(s) == want, (s, t)
print("1000 random cases: two pointers, binary-search index and brute force agree")
idx = Index('abcde')
print(optimal('ace', 'abcde'), optimal('aec', 'abcde'), optimal('', 'x'))
print([idx.is_subsequence(q) for q in ('ace', 'aec', '', 'z')])
