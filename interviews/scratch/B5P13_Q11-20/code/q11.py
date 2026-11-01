import itertools
import inspect
import math
import random
from collections import Counter

random.seed(1311)

def shuffle_with(n, choices):
    """Fisher-Yates driven by an explicit list of choices: the k-th choice is used at i = n-1-k, 0 <= j <= i."""
    a = list(range(n))
    for k, i in enumerate(range(n - 1, 0, -1)):
        j = choices[k]
        assert 0 <= j <= i
        a[i], a[j] = a[j], a[i]
    return a

def fisher_yates(n, choices):
    """Optimal: run once for the given choices, then run on EVERY choice sequence and tabulate."""
    counts = Counter(tuple(shuffle_with(n, cs))
                     for cs in itertools.product(*[range(i + 1) for i in range(n - 1, 0, -1)]))
    return [shuffle_with(n, choices), sum(counts.values()), len(counts),
            min(counts.values()), max(counts.values())]

def brute(n, choices):
    """Brute force: recursive walk of the swap tree (a branch for every j at every step)."""
    acc = Counter()
    def rec(a, i):
        if i == 0:
            acc[tuple(a)] += 1
            return
        for j in range(i + 1):
            b = a[:]
            b[i], b[j] = b[j], b[i]
            rec(b, i - 1)
    rec(list(range(n)), n - 1)
    a, i = list(range(n)), n - 1
    for c in choices:
        a[i], a[c] = a[c], a[i]
        i -= 1
    return [a, sum(acc.values()), len(acc), min(acc.values()), max(acc.values())]

examples = [
    (3, [2, 1], [[0, 1, 2], 6, 6, 1, 1]),
    (1, [], [[0], 1, 1, 1, 1]),
    (4, [0, 0, 0], [[1, 2, 3, 0], 24, 24, 1, 1]),
    (5, [4, 3, 2, 1], [[0, 1, 2, 3, 4], 120, 120, 1, 1]),
]
for n, ch, exp in examples:
    got = fisher_yates(n, ch)
    print(n, ch, '->', got)
    assert got == exp and brute(n, ch) == exp

# the exhaustive table for every n <= 5: n! sequences, n! distinct perms, each exactly once
for n in range(1, 6):
    r = fisher_yates(n, [0] * (n - 1))
    assert r[1:] == [math.factorial(n)] * 2 + [1, 1], r
    print('n =', n, 'sequences, distinct, min, max =', r[1:])

# seeded random cross-check against the recursive swap tree
for _ in range(300):
    n = random.randint(1, 5)
    ch = [random.randint(0, i) for i in range(n - 1, 0, -1)]
    assert fisher_yates(n, ch) == brute(n, ch)
print('random cross-check ok: 300 cases')

# the wrong loop (j from 0..n-1) on n = 3: 27 equally likely sequences, 6 permutations, NOT uniform
bad = Counter()
for js in itertools.product(range(3), repeat=3):
    a = [0, 1, 2]
    for i, j in enumerate(js):
        a[i], a[j] = a[j], a[i]
    bad[tuple(a)] += 1
print('naive swap-with-any, n=3:', sorted(bad.items()))
assert sum(bad.values()) == 27 and set(bad.values()) == {4, 5}

# does CPython's random.shuffle run this loop? (read from the installed 3.13 source)
src = inspect.getsource(random.Random.shuffle)
print('loop is reversed(range(1, len(x))):', 'reversed(range(1, len(x)))' in src,
      '| uses randbelow(i + 1):', 'randbelow(i + 1)' in src)
assert 'reversed(range(1, len(x)))' in src and 'randbelow(i + 1)' in src

# edge asserts
assert fisher_yates(1, []) == [[0], 1, 1, 1, 1]
assert fisher_yates(2, [0])[0] == [1, 0] and fisher_yates(2, [1])[0] == [0, 1]
print('edge asserts ok')
