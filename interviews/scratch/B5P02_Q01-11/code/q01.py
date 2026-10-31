import random


def pal_brute(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]


def pal_two_pointers(s):
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True


examples = [("A man, a plan, a canal: Panama", True), ("race a car", False),
            (" ", True), ("0P", False)]
for s, want in examples:
    got = pal_two_pointers(s)
    assert got == pal_brute(s) == want, (s, got, want)
    print(repr(s), "->", got)

assert pal_two_pointers("") is True
assert pal_two_pointers(".,") is True          # only junk
assert pal_two_pointers("a") is True
assert pal_two_pointers("ab") is False
assert pal_two_pointers("a.") is True
assert pal_two_pointers("Aa") is True          # case ignored
assert pal_two_pointers("0P0") is True         # digits count
assert pal_two_pointers("a" * 200000) is True  # max size, no recursion

rng = random.Random(5)
alphabet = "aAbB1 ,.:"
cases = 0
for _ in range(3000):
    s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 9)))
    assert pal_two_pointers(s) == pal_brute(s), s
    cases += 1
# force palindromes too, so True is well covered
for _ in range(1000):
    half = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
    s = half + rng.choice(["", "x", " "]) + half[::-1].swapcase()
    assert pal_two_pointers(s) == pal_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
