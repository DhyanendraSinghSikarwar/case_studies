import random
from collections import Counter

def brute(s, t):
    need = Counter(t)
    best = ''
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            if not (Counter(s[i:j]) & need) == need:
                continue
            if best == '' or j - i < len(best):
                best = s[i:j]
            break              # first j for this i is the shortest from i
    return best

def optimal(s, t):
    if not t or len(t) > len(s):
        return ''
    need = Counter(t)
    missing = len(t)               # characters still missing, counted with multiplicity
    left = 0
    best_len, best_start = len(s) + 1, 0
    for right, ch in enumerate(s):
        if need[ch] > 0:           # a still-needed copy arrives
            missing -= 1
        need[ch] -= 1              # may go negative: surplus copy
        while missing == 0:        # window valid: shrink
            if right - left + 1 < best_len:      # strict < keeps the leftmost tie
                best_len, best_start = right - left + 1, left
            need[s[left]] += 1
            if need[s[left]] > 0:  # we gave up a needed copy
                missing += 1
            left += 1
    return '' if best_len > len(s) else s[best_start:best_start + best_len]

assert optimal('ADOBECODEBANC', 'ABC') == 'BANC'
assert optimal('a', 'aa') == ''
assert optimal('a', 'a') == 'a'
assert optimal('', 'a') == ''
assert optimal('abc', '') == ''
assert optimal('aa', 'aa') == 'aa'
assert optimal('abcabc', 'cba') == 'abc'      # leftmost among ties
assert optimal('xyz', 'q') == ''
assert optimal('aabdec', 'abc') == 'abdec'
assert optimal('bba', 'ab') == 'ba'

rng = random.Random(15)
for _ in range(1000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 12)))
    t = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 4)))
    assert optimal(s, t) == brute(s, t), (s, t)
print("1000 random cases agree with brute force")
print(repr(optimal('ADOBECODEBANC', 'ABC')), repr(optimal('a', 'aa')), repr(optimal('a', 'a')))
big = 'ab' * 50000
print("n = 100000:", len(optimal(big, 'ba' * 2)))
