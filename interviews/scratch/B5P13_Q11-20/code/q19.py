import itertools
import random
import string

random.seed(1319)

def title_to_number(title):
    r = 0
    for ch in title:
        r = r * 26 + (ord(ch) - 64)         # A=1 .. Z=26: digits 1..26, no zero digit
    return r

def number_to_title(n):
    out = []
    while n:
        n, d = divmod(n - 1, 26)            # shift to 0..25 first, then peel a letter
        out.append(chr(65 + d))
    return ''.join(reversed(out))

def solve(title, number):
    return [title_to_number(title), number_to_title(number)]

# brute force: an explicit table of ALL titles up to length 4, in order (shorter first, then alphabetical)
TABLE = [''.join(p) for L in range(1, 5) for p in itertools.product(string.ascii_uppercase, repeat=L)]
INDEX = {t: i + 1 for i, t in enumerate(TABLE)}
assert len(TABLE) == 26 + 26 ** 2 + 26 ** 3 + 26 ** 4

def brute(title, number):
    # for the 7-letter maximum the table is too small, so fall back to digit-by-digit counting
    if len(title) <= 4 and number <= len(TABLE):
        return [INDEX[title], TABLE[number - 1]]
    k, L = number - 1, 1
    while k >= 26 ** L:
        k -= 26 ** L; L += 1
    digs = []
    for _ in range(L):
        k, r = divmod(k, 26); digs.append(chr(65 + r))
    return [sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(title))), ''.join(reversed(digs))]

examples = [('AB', 28, [28, 'AB']), ('A', 1, [1, 'A']), ('ZY', 701, [701, 'ZY']),
            ('FXSHRXW', 2147483647, [2147483647, 'FXSHRXW'])]
for t, n, exp in examples:
    got = solve(t, n)
    print(t, n, '->', got)
    assert got == exp and brute(t, n) == exp

# why n - 1: plain base 26 breaks on the multiples of 26
def naive(n):
    out = []
    while n:
        n, d = divmod(n, 26); out.append(chr(64 + d))     # d == 0 gives '@'
    return ''.join(reversed(out))
print('naive divmod(n, 26): 26 ->', repr(naive(26)), ', 52 ->', repr(naive(52)), '| with n-1:', number_to_title(26), number_to_title(52))
assert naive(26) == '@' + '' or '@' in naive(26)

# round trip over the WHOLE table (475254 titles) and against the table in both directions
for i, t in enumerate(TABLE, start=1):
    assert title_to_number(t) == i and number_to_title(i) == t
print('round trip ok for all', len(TABLE), 'titles up to length 4')

# seeded random cross-check
for _ in range(500):
    L = random.randint(1, 4)
    t = ''.join(random.choice(string.ascii_uppercase) for _ in range(L))
    n = random.randint(1, len(TABLE))
    assert solve(t, n) == brute(t, n)
print('random cross-check ok: 500 cases')

# limits: 2^31 - 1 is 7 letters, and 8 letters would overflow int32 (Python has no overflow; the bound is the prompt's)
assert number_to_title(2 ** 31 - 1) == 'FXSHRXW' and len(number_to_title(2 ** 31 - 1)) == 7
assert title_to_number('FXSHRXX') > 2 ** 31 - 1
print('length of title(2^31-1) =', len(number_to_title(2 ** 31 - 1)), '; next title FXSHRXX =', title_to_number('FXSHRXX'))

# edge asserts
assert number_to_title(26) == 'Z' and number_to_title(27) == 'AA' and number_to_title(52) == 'AZ' and number_to_title(53) == 'BA'
assert title_to_number('Z') == 26 and title_to_number('AA') == 27 and title_to_number('ZZ') == 702 and number_to_title(702) == 'ZZ'
print('edge asserts ok')
