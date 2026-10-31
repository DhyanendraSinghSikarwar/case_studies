import itertools
import re

PATTERN = re.compile(r'[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?')


def is_number_regex(s):
    return PATTERN.fullmatch(s) is not None


def is_digit(c):
    return '0' <= c <= '9'                      # not c.isdigit(): that accepts Unicode digits


def is_number(s):
    n, i = len(s), 0
    if i < n and s[i] in '+-':
        i += 1
    a = 0
    while i < n and is_digit(s[i]):
        i += 1
        a += 1
    b = 0
    if i < n and s[i] == '.':
        i += 1
        while i < n and is_digit(s[i]):
            i += 1
            b += 1
    if a + b == 0:
        return False
    if i < n and s[i] in 'eE':
        i += 1
        if i < n and s[i] in '+-':
            i += 1
        c = 0
        while i < n and is_digit(s[i]):
            i += 1
            c += 1
        if c == 0:
            return False
    return i == n


yes = ['2', '0089', '-0.1', '+3.14', '4.', '-.9', '2e10', '3e+7', '53.5e93']
no = ['abc', '1a', '1e', 'e3', '99e2.5', '--6', '-+3', '95a54e53', '.', '+.']
for s in yes:
    assert is_number(s), s
for s in no:
    assert not is_number(s), s
print('yes ->', [is_number(s) for s in yes])
print('no  ->', [is_number(s) for s in no])
assert not is_number('') and not is_number('+') and not is_number('e') and not is_number('.e1')
assert is_number('0') and is_number('.5e-3') and is_number('5.e3') and is_number('-0')
assert not is_number(' 1') and not is_number('1 ') and not is_number('1e5e5')

# Exhaustive cross-check: every string up to length 7 over this alphabet, against the regex.
count = valid = 0
for n in range(0, 8):
    for tup in itertools.product('+-.eE1', repeat=n):
        s = ''.join(tup)
        r = is_number(s)
        assert r == is_number_regex(s), s
        count += 1
        valid += r
print('exhaustive cross-check passed:', count, 'strings,', valid, 'valid')

# The Unicode trap: isdigit and a bare \d accept more than ASCII digits.
print('\u0663'.isdigit(), '\u00b2'.isdigit(), bool(re.fullmatch(r'\d+', '\u0663')), is_number('\u0663'))
print(float('1_0'), float(' 1e3 '), float('inf'))
