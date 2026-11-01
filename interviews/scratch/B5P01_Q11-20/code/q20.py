import random
from itertools import product

def brute(s, t):
    # isomorphic iff a consistent one-to-one map exists: check via canonical pattern
    def pat(x):
        first = {}
        return [first.setdefault(ch, len(first)) for ch in x]
    return len(s) == len(t) and pat(s) == pat(t)

def optimal(s, t):
    if len(s) != len(t):
        return False
    s2t, t2s = {}, {}
    for a, b in zip(s, t):
        if s2t.setdefault(a, b) != b or t2s.setdefault(b, a) != a:
            return False
    return True

def one_direction_only(s, t):        # the classic wrong answer
    m = {}
    for a, b in zip(s, t):
        if m.setdefault(a, b) != b:
            return False
    return True

def word_pattern(pattern, sentence):
    words = sentence.split()
    if len(pattern) != len(words):
        return False
    p2w, w2p = {}, {}
    for p, w in zip(pattern, words):
        if p2w.setdefault(p, w) != w or w2p.setdefault(w, p) != p:
            return False
    return True

assert optimal('egg', 'add') is True
assert optimal('foo', 'bar') is False
assert optimal('badc', 'baba') is False
assert optimal('paper', 'title') is True
assert optimal('', '') is True
assert optimal('a', 'a') is True
assert optimal('ab', 'aa') is False
assert optimal('ab', 'abc') is False
print("one direction only on ('badc','baba'):", one_direction_only('badc', 'baba'), "(wrong, truth False)")
assert word_pattern('abba', 'dog cat cat dog') is True
assert word_pattern('abba', 'dog cat cat fish') is False
assert word_pattern('abba', 'dog dog dog dog') is False
assert word_pattern('aaaa', 'dog cat cat dog') is False
assert word_pattern('a', 'dog cat') is False

rng = random.Random(20)
for _ in range(1000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 6)))
    t = ''.join(rng.choice('xyz') for _ in range(len(s)))
    assert optimal(s, t) == brute(s, t), (s, t)
# exhaustive on a tiny alphabet and length 4
for s in map(''.join, product('ab', repeat=4)):
    for t in map(''.join, product('xy', repeat=4)):
        assert optimal(s, t) == brute(s, t)
print("1000 random + 256 exhaustive cases agree")
print(optimal('egg', 'add'), optimal('foo', 'bar'), optimal('badc', 'baba'))
