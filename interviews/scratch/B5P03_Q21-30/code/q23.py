import random


def pi_function(s, stats=None):
    n = len(s)
    pi = [0] * n
    k = 0
    for i in range(1, n):
        while k and s[i] != s[k]:
            k = pi[k - 1]                      # fall back to the next shorter border
            if stats is not None:
                stats['fallbacks'] += 1
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def pi_brute(s):
    n = len(s)
    out = []
    for i in range(n):
        sub = s[:i + 1]
        best = 0
        for L in range(1, len(sub)):           # proper: L < len(sub)
            if sub[:L] == sub[-L:]:
                best = L
        out.append(best)
    return out


def kmp_search(text, pattern):
    if not pattern:
        raise ValueError('empty pattern')
    m = len(pattern)
    pi = pi_function(pattern)
    res, k = [], 0
    for i, c in enumerate(text):               # i only moves forward
        while k and c != pattern[k]:
            k = pi[k - 1]
        if c == pattern[k]:
            k += 1
        if k == m:
            res.append(i - m + 1)
            k = pi[k - 1]                      # allow overlapping matches
    return res


def search_brute(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text[i:i + len(pattern)] == pattern]


print(pi_function('abacaba'))
print(pi_function('aabaaab'))
print(kmp_search('aaaa', 'aa'))
assert pi_function('abacaba') == [0, 0, 1, 0, 1, 2, 3]
assert pi_function('aabaaab') == [0, 1, 0, 1, 2, 2, 3]
assert kmp_search('aaaa', 'aa') == [0, 1, 2]
assert pi_function('') == [] and pi_function('a') == [0]
assert pi_function('aaaa') == [0, 1, 2, 3]
assert kmp_search('abc', 'abcd') == [] and kmp_search('', 'a') == []
assert kmp_search('abababa', 'aba') == [0, 2, 4]

rng = random.Random(23)
cases = 0
for _ in range(3000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 14)))
    assert pi_function(s) == pi_brute(s), s
    text = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 16)))
    pat = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 5)))
    assert kmp_search(text, pat) == search_brute(text, pat), (text, pat)
    cases += 1
print('random cross-check passed:', cases, 'cases')

# The amortised bound, checked: total fallback steps never exceed n.
worst = 0
for _ in range(2000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 40)))
    st = {'fallbacks': 0}
    pi_function(s, st)
    assert st['fallbacks'] <= len(s)
    worst = max(worst, st['fallbacks'] / len(s))
print('max fallbacks / n over random strings:', round(worst, 3))
