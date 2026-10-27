import random


def min_rotation_brute(s):
    n = len(s)
    best = min(range(n), key=lambda i: (s[i:] + s[:i], i))
    return s[best:] + s[:best], best


def min_rotation(s):
    n = len(s)
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a, b = s[(i + k) % n], s[(j + k) % n]
        if a == b:
            k += 1
            continue
        if a > b:
            i += k + 1
        else:
            j += k + 1
        if i == j:
            j += 1
        k = 0
    start = min(i, j)
    return s[start:] + s[:start], start


for s, exp in [('bca', ('abc', 2)), ('cba', ('acb', 2)), ('abab', ('abab', 0)), ('aaa', ('aaa', 0))]:
    print(s, min_rotation(s))
    assert min_rotation(s) == exp == min_rotation_brute(s)
assert min_rotation('a') == ('a', 0)
assert min_rotation('ba') == ('ab', 1)
assert min_rotation('abcabc') == ('abcabc', 0)
assert min_rotation('cabcab') == ('abcabc', 1)       # periodic: smallest index among ties
assert min_rotation('zzzy') == ('yzzz', 3)

rng = random.Random(25)
cases = 0
for _ in range(5000):
    s = ''.join(rng.choice('ab' if rng.random() < 0.7 else 'abc') for _ in range(rng.randint(1, 12)))
    assert min_rotation(s) == min_rotation_brute(s), s
    cases += 1
print('random cross-check passed:', cases, 'cases')
big = 'a' * 100000 + 'b'
print(min_rotation(big)[1])                          # linear time on a long adversarial-looking input
