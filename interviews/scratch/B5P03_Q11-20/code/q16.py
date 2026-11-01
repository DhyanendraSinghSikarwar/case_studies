import random
from collections import Counter
from itertools import permutations


def lp_brute(s):
    # try every ordering of every sub-multiset (tiny inputs only)
    best = 0
    n = len(s)
    for mask in range(1 << n):
        sub = [s[i] for i in range(n) if mask >> i & 1]
        if len(sub) <= best:
            continue
        if any(p == p[::-1] for p in set(permutations(sub))):
            best = len(sub)
    return best


def lp_count(s):
    pairs = 0
    odd = False
    for c in Counter(s).values():
        pairs += c // 2 * 2
        odd = odd or c % 2 == 1
    return pairs + (1 if odd else 0)


examples = [("abccccdd", 7), ("a", 1), ("Aa", 1), ("aaabbb", 5)]
for s, want in examples:
    got = lp_count(s)
    assert got == lp_brute(s) == want, (s, got)
    print(repr(s), "->", got)

assert lp_count("") == 0
assert lp_count("ab") == 1
assert lp_count("aaaa") == 4
assert lp_count("aA" * 1000) == 2000              # case-sensitive: 1000 a and 1000 A, all paired
assert lp_count("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") == 1  # 52 singletons
assert lp_count("a" * 2000) == 2000

rng = random.Random(16)
cases = 0
for _ in range(400):
    s = "".join(rng.choice("abcA") for _ in range(rng.randint(0, 8)))
    assert lp_count(s) == lp_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
