import random
from itertools import zip_longest


def cmp_brute(a, b):
    x = [int(p) for p in a.split(".")]
    y = [int(p) for p in b.split(".")]
    for p, q in zip_longest(x, y, fillvalue=0):
        if p != q:
            return -1 if p < q else 1
    return 0


def next_rev(s, i):
    # read one revision starting at i; return (value, index after the dot)
    n, v = len(s), 0
    while i < n and s[i] != ".":
        v = v * 10 + (ord(s[i]) - 48)
        i += 1
    return v, i + 1


def cmp_version(a, b):
    i = j = 0
    while i < len(a) or j < len(b):
        x, i = next_rev(a, i) if i < len(a) else (0, i)
        y, j = next_rev(b, j) if j < len(b) else (0, j)
        if x != y:
            return -1 if x < y else 1
    return 0


examples = [("1.2", "1.10", -1), ("1.01", "1.001", 0), ("1.0", "1.0.0.0", 0), ("0.1", "1.1", -1), ("2.0.1", "2", 1)]
for a, b, want in examples:
    got = cmp_version(a, b)
    assert got == cmp_brute(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert "1.2" > "1.10"                         # the string-compare pitfall: wrongly says 1.2 is larger
assert cmp_version("1.2", "1.10") == -1
assert cmp_version("0", "0.0.0") == 0
assert cmp_version("1.0.1", "1") == 1
assert cmp_version("7", "7.0") == 0
assert cmp_version("001", "1") == 0
assert cmp_version("1." + "0." * 200 + "1", "1") == 1   # long, nonzero tail decides
assert cmp_version("9" * 100, "9" * 99) == 1             # big revisions are fine in Python

rng = random.Random(20)
cases = 0
for _ in range(4000):
    def gen():
        return ".".join(("0" * rng.randint(0, 2)) + str(rng.randint(0, 12)) for _ in range(rng.randint(1, 5)))
    a, b = gen(), gen()
    assert cmp_version(a, b) == cmp_brute(a, b), (a, b)
    assert cmp_version(a, b) == -cmp_version(b, a)
    cases += 1
print("random cross-check passed:", cases, "cases")
