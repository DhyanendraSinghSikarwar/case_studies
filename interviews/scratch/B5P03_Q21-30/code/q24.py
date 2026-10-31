import random

BIG = (1 << 61) - 1                              # a Mersenne prime
seed_rng = random.Random(24)                     # base chosen at random, but reproducibly


def rabin_karp(text, pattern, M=BIG, B=None, verify=True, stats=None):
    n, m = len(text), len(pattern)
    if m == 0:
        raise ValueError('empty pattern')
    if B is None:
        B = seed_rng.randrange(2, M - 1)
    if m > n:
        return []
    high = pow(B, m - 1, M)
    hp = ht = 0
    for i in range(m):
        hp = (hp * B + ord(pattern[i])) % M
        ht = (ht * B + ord(text[i])) % M
    res = []
    for i in range(n - m + 1):
        if ht == hp:
            if stats is not None:
                stats['hits'] += 1
            if not verify or text[i:i + m] == pattern:
                res.append(i)
        if i + m < n:
            ht = ((ht - ord(text[i]) * high) * B + ord(text[i + m])) % M
    return res


def search_brute(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text[i:i + len(pattern)] == pattern]


print(rabin_karp('abracadabra', 'abra'))
print(rabin_karp('aaaaa', 'aa'))
print(rabin_karp('abcabc', 'cab'))
assert rabin_karp('abracadabra', 'abra') == [0, 7]
assert rabin_karp('aaaaa', 'aa') == [0, 1, 2, 3]
assert rabin_karp('abcabc', 'cab') == [2]
assert rabin_karp('abc', 'abcd') == [] and rabin_karp('', 'a') == []
assert rabin_karp('abc', 'abc') == [0]
assert rabin_karp('abc', 'c') == [2]

# Deliberately tiny modulus: collisions everywhere, still correct because we verify.
rng = random.Random(240)
cases = 0
for _ in range(3000):
    text = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 16)))
    pat = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 4)))
    expected = search_brute(text, pat)
    assert rabin_karp(text, pat, M=7, B=3) == expected, (text, pat)
    assert rabin_karp(text, pat, M=7, B=5) == expected, (text, pat)
    assert rabin_karp(text, pat) == expected, (text, pat)
    cases += 1
print('random cross-check passed (M = 7, M = 7 other base, M = 2^61-1):', cases, 'cases')

# What goes wrong without the verify step: find the first wrong answer (seeded search).
rng = random.Random(241)
for _ in range(10000):
    text = ''.join(rng.choice('abc') for _ in range(rng.randint(3, 8)))
    pat = ''.join(rng.choice('abc') for _ in range(rng.randint(2, 3)))
    if rabin_karp(text, pat, M=7, B=3, verify=False) != search_brute(text, pat):
        print('no-verify wrong example:', text, pat, rabin_karp(text, pat, M=7, B=3, verify=False), search_brute(text, pat))
        break

# Spurious hits: tiny M versus large M on the same random input.
rng = random.Random(242)
text = ''.join(rng.choice('abcd') for _ in range(2000))
pat = 'abcdabcd'
for M in (7, BIG):
    st = {'hits': 0}
    found = rabin_karp(text, pat, M=M, B=3 if M == 7 else None, stats=st)
    print('M =', M, 'matches:', len(found), 'hash hits:', st['hits'])
