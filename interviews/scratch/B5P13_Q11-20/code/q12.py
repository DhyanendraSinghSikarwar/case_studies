import itertools
import math
import random
from fractions import Fraction

random.seed(1312)

def reservoir_one(stream, draws):
    """One pass, one held item plus a counter. i-th item (1-based) replaces the held one iff draw == 0, draw in 0..i-1."""
    held = stream[0]
    for i, x in enumerate(stream[1:], start=2):
        if draws[i - 2] == 0:
            held = x
    return held

def solve(stream, draws):
    n = len(stream)
    held = reservoir_one(stream, draws)
    # exact counts without enumeration: counts after item i; old items survive in (i-1) of i draws
    counts, total = [1], 1
    for i in range(2, n + 1):
        counts = [c * (i - 1) for c in counts] + [total]
        total *= i
    return [held, counts, total]

def brute(stream, draws):
    """Enumerate EVERY draw sequence with itertools.product and count which position is held."""
    n = len(stream)
    cnt, tot = [0] * n, 0
    for ds in itertools.product(*[range(i) for i in range(2, n + 1)]):
        pos = 0
        for i, d in enumerate(ds, start=2):
            if d == 0:
                pos = i - 1
        cnt[pos] += 1
        tot += 1
    pos = 0
    for i, d in enumerate(draws, start=2):
        if d == 0:
            pos = i - 1
    return [stream[pos], cnt, tot]

examples = [
    ([10, 20, 30], [0, 2], [20, [2, 2, 2], 6]),
    ([5], [], [5, [1], 1]),
    ([4, 4, 9, 1], [1, 0, 0], [1, [6, 6, 6, 6], 24]),
]
for s, d, exp in examples:
    got = solve(s, d)
    print(s, d, '->', got)
    assert got == exp and brute(s, d) == exp

# the exact table: every item held in (n-1)! of n! sequences, for every n <= 7 (enumeration, not sampling)
for n in range(1, 8):
    r = brute(list(range(n)), [1] * (n - 1))
    assert r[1] == [math.factorial(n - 1)] * n and r[2] == math.factorial(n), (n, r)
    assert solve(list(range(n)), [1] * (n - 1)) == r
    print('n =', n, 'counts =', r[1], 'of', r[2], '-> probability', Fraction(r[1][0], r[2]))

# the product: (1/i)(1-1/(i+1))...(1-1/n) = 1/n for item i, exactly
for n in range(1, 12):
    for i in range(1, n + 1):
        p = Fraction(1, i)
        for m in range(i + 1, n + 1):
            p *= 1 - Fraction(1, m)
        assert p == Fraction(1, n)
print('product telescopes to 1/n: checked exactly for n <= 11, every i')

# seeded random cross-check (values may repeat; items identified by position)
for _ in range(300):
    n = random.randint(1, 6)
    s = [random.randint(0, 3) for _ in range(n)]
    d = [random.randint(0, i - 1) for i in range(2, n + 1)]
    assert solve(s, d) == brute(s, d)
print('random cross-check ok: 300 cases')

# edge asserts
assert solve([7], []) == [7, [1], 1]
assert solve([1, 2], [0]) == [2, [1, 1], 2] and solve([1, 2], [1]) == [1, [1, 1], 2]
assert reservoir_one(list(range(6)), [1, 1, 1, 1, 1]) == 0      # no draw is 0: the first item stays
assert reservoir_one(list(range(6)), [0, 0, 0, 0, 0]) == 5      # every draw is 0: the last item wins
print('edge asserts ok')
