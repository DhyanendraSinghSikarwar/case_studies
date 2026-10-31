import random


def z_brute(s):
    n = len(s)
    z = [0] * n
    for i in range(n):
        k = 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        z[i] = k
    return z


def z_function(s):
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0                                   # s[l:r] == s[0:r-l], r as far right as seen
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])         # copy from the mirror, capped at the window
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1                           # only reaches past r when the copy hit the edge
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def search_z(text, pattern):
    if not pattern:
        raise ValueError('empty pattern')
    m = len(pattern)
    z = z_function(pattern + '\x00' + text)     # sentinel must not occur in either string
    return [i - m - 1 for i in range(m + 1, len(z)) if z[i] == m]


def search_brute(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text[i:i + len(pattern)] == pattern]


print(z_function('aabxaab'))
print(search_z('abababa', 'aba'))
assert z_function('aabxaab') == [7, 1, 0, 0, 3, 1, 0]
assert search_z('abababa', 'aba') == [0, 2, 4]
assert z_function('') == [] and z_function('a') == [1]
assert z_function('aaaa') == [4, 3, 2, 1]
assert z_function('abcd') == [4, 0, 0, 0]
assert search_z('aaaa', 'aa') == [0, 1, 2]
assert search_z('abc', 'abcd') == [] and search_z('', 'a') == []
assert search_z('abc', 'abc') == [0]

rng = random.Random(22)
cases = 0
for _ in range(3000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 14)))
    assert z_function(s) == z_brute(s), s
    text = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 14)))
    pat = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 4)))
    assert search_z(text, pat) == search_brute(text, pat), (text, pat)
    cases += 1
print('random cross-check passed:', cases, 'cases')
big = 'a' * 20000                               # the quadratic-for-brute shape, linear here
assert z_function(big)[1] == 19999
print('20000 a-characters done')
