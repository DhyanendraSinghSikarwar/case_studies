import itertools
import math
import random
from collections import Counter

random.seed(3201)


def solve(n):
    """Run the buggy shuffle on every one of the n^n choice sequences (j in 0..n-1 for each i)."""
    cnt = Counter()
    for js in itertools.product(range(n), repeat=n):
        a = list(range(n))
        for i, j in enumerate(js):
            a[i], a[j] = a[j], a[i]
        cnt[tuple(a)] += 1
    hi, lo = max(cnt.values()), min(cnt.values())
    return [n ** n, len(cnt), lo, hi,
            list(min(p for p, c in cnt.items() if c == hi)),
            list(min(p for p, c in cnt.items() if c == lo))], cnt


def brute(n):
    """Oracle: recursive enumeration of the swap tree."""
    cnt = Counter()

    def rec(a, i):
        if i == n:
            cnt[tuple(a)] += 1
            return
        for j in range(n):
            b = a[:]
            b[i], b[j] = b[j], b[i]
            rec(b, i + 1)
    rec(list(range(n)), 0)
    hi, lo = max(cnt.values()), min(cnt.values())
    return [sum(cnt.values()), len(cnt), lo, hi,
            list(sorted(p for p in cnt if cnt[p] == hi)[0]),
            list(sorted(p for p in cnt if cnt[p] == lo)[0])]


def correct(n):
    """Fisher-Yates: i from n-1 down to 1, j in 0..i. Exactly n! sequences."""
    cnt = Counter()
    for js in itertools.product(*[range(i + 1) for i in range(n - 1, 0, -1)]):
        a = list(range(n))
        for i, j in zip(range(n - 1, 0, -1), js):
            a[i], a[j] = a[j], a[i]
        cnt[tuple(a)] += 1
    return cnt


for n, want in [(1, [1, 1, 1, 1, [0], [0]]), (2, [4, 2, 2, 2, [0, 1], [0, 1]]),
                (3, [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]), (4, [256, 24, 8, 15, [1, 0, 3, 2], [3, 0, 1, 2]])]:
    got, _ = solve(n)
    assert got == want == brute(n), (n, got)
    print("n =", n, "->", got)

# the n = 3 table: all 27 sequences, then the counts per permutation next to the correct shuffle
res3, cnt3 = solve(3)
print("\nn = 3, buggy shuffle (j from the whole range), 27 sequences:")
fy3 = correct(3)
print("perm        buggy count   buggy prob   correct count (6 sequences)")
for p in sorted(cnt3):
    print(f"{str(list(p)):<11} {cnt3[p]:>11}   {cnt3[p]:>2}/27        {fy3[p]:>5}")
print("sum", sum(cnt3.values()), "| correct sum", sum(fy3.values()), "| ideal 27/6 =", 27 / 6)

# bias grows: statistics for n = 1..6 (6^6 = 46656 sequences is the largest enumeration)
print("\n n   n^n   n!  distinct  min  max   max/min")
for n in range(1, 7):
    r, c = solve(n)
    assert r == brute(n)
    assert r[1] == math.factorial(n)                        # every permutation is reachable, just not evenly
    assert (r[2] == r[3]) == (n <= 2)                       # uniform only for n <= 2
    assert sum(c.values()) == n ** n
    fy = correct(n)
    assert len(fy) == math.factorial(n) and set(fy.values()) == {1}   # correct: every permutation exactly once
    print(f"{n:>2} {n ** n:>5} {math.factorial(n):>4} {r[1]:>8} {r[2]:>4} {r[3]:>4}   {r[3] / r[2]:.3f}")

# the divisibility argument, checked for n = 3..200: n^n is never divisible by n!, because n-1 | n! but gcd(n-1, n) = 1
for n in range(3, 201):
    assert math.factorial(n) % (n - 1) == 0 and math.gcd(n - 1, n) == 1 and n - 1 >= 2
    assert (n ** n) % (n - 1) == 1 and (n ** n) % math.factorial(n) != 0
print("n = 3..200: n^n mod (n-1) = 1 and n! does not divide n^n")
print("n = 1, 2: n^n / n! =", 1 / 1, 4 / 2, "(integers, so uniform is possible and happens)")

# seeded sampling is only a sanity picture, the exact table above is the proof
rng = random.Random(7)
s = Counter()
for _ in range(60000):
    a = [0, 1, 2]
    for i in range(3):
        j = rng.randrange(3)
        a[i], a[j] = a[j], a[i]
    s[tuple(a)] += 1
print("60000 seeded samples (picture only):", {tuple(p): s[p] for p in sorted(s)})

# random cross-check of solve against the recursive oracle (n small; all n in 1..5, each repeated seeded)
for _ in range(60):
    n = random.randint(1, 5)
    assert solve(n)[0] == brute(n)
print("60 seeded checks: loop enumeration equals recursive enumeration")
assert solve(1)[0] == [1, 1, 1, 1, [0], [0]]
print("edge asserts ok")
