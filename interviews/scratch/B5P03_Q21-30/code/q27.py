import itertools
import random


def is_pal(x):
    return x == x[::-1]


def shortest_pal_brute(s):
    for L in range(len(s), -1, -1):
        if is_pal(s[:L]):
            return s[L:][::-1] + s
    return s                                   # unreachable: L = 0 always works


def pi_function(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def shortest_pal(s):
    if not s:
        return s
    t = s + '#' + s[::-1]
    L = pi_function(t)[-1]
    return s[L:][::-1] + s


def shortest_pal_exhaustive(s, alphabet):
    # truly exhaustive: try every possible prefix string of growing length
    for k in range(len(s) + 1):
        for pre in itertools.product(alphabet, repeat=k):
            cand = ''.join(pre) + s
            if is_pal(cand):
                return cand


for s, exp in [('aacecaaa', 'aaacecaaa'), ('abcd', 'dcbabcd'), ('', ''), ('aba', 'aba')]:
    print(repr(s), '->', repr(shortest_pal(s)))
    assert shortest_pal(s) == exp == shortest_pal_brute(s)
assert shortest_pal('a') == 'a' and shortest_pal('ab') == 'bab'
assert shortest_pal('aaaa') == 'aaaa'

rng = random.Random(27)
cases = 0
for _ in range(3000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 14)))
    assert shortest_pal(s) == shortest_pal_brute(s), s
    cases += 1
for n in range(0, 7):                          # all strings over {a, b}, against the exhaustive search
    for tup in itertools.product('ab', repeat=n):
        s = ''.join(tup)
        assert shortest_pal(s) == shortest_pal_exhaustive(s, 'ab'), s
        cases += 1
print('random and exhaustive cross-check passed:', cases, 'cases')
big = 'a' * 30000 + 'b'
print(len(shortest_pal(big)))                  # linear time at the stated size limit
