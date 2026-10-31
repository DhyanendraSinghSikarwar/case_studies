import random

BIG = (1 << 61) - 1


def happy_brute(s):
    for L in range(len(s) - 1, 0, -1):
        if s[:L] == s[-L:]:
            return s[:L]
    return ''


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


def happy_pi(s):
    return s[:pi_function(s)[-1]] if s else ''


def z_function(s):
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def happy_z(s):
    z = z_function(s)
    for i in range(1, len(s)):
        if i + z[i] == len(s):                  # smallest i = longest border
            return s[i:]
    return ''


def happy_hash(s, B=911382323, M=BIG):
    n = len(s)
    pre = suf = 0
    power = 1
    hits = []
    for L in range(1, n):                       # prefix hash grows right, suffix hash grows left
        pre = (pre * B + ord(s[L - 1])) % M
        suf = (suf + ord(s[n - L]) * power) % M
        power = power * B % M
        if pre == suf:
            hits.append(L)
    for L in reversed(hits):                    # verify longest first; a collision is skipped
        if s[:L] == s[-L:]:
            return s[:L]
    return ''


for s, exp in [('level', 'l'), ('ababab', 'abab'), ('abc', ''), ('a', '')]:
    r = (happy_pi(s), happy_z(s), happy_hash(s), happy_brute(s))
    print(repr(s), r)
    assert all(x == exp for x in r), (s, r)
assert happy_pi('aaaa') == 'aaa' and happy_pi('abcab') == 'ab'
assert happy_pi('aabaaab') == 'aab'
assert happy_z('') == '' and happy_hash('') == ''

rng = random.Random(26)
cases = 0
for _ in range(4000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 14)))
    b = happy_brute(s)
    assert happy_pi(s) == b and happy_z(s) == b and happy_hash(s) == b, s
    # tiny modulus: many collisions, still right because hits are verified
    assert happy_hash(s, B=3, M=7) == b, s
    cases += 1
print('random cross-check passed (pi, Z, hash, hash with M=7):', cases, 'cases')
