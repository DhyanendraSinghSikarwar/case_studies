import random

VOWELS = set("aeiouAEIOU")


def rv_brute(s):
    v = [c for c in s if c in VOWELS][::-1]
    it = iter(v)
    return "".join(next(it) if c in VOWELS else c for c in s)


def rv_two_pointers(s):
    a = list(s)
    i, j = 0, len(a) - 1
    while i < j:
        while i < j and a[i] not in VOWELS:
            i += 1
        while i < j and a[j] not in VOWELS:
            j -= 1
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1
    return "".join(a)


examples = [("IceCreAm", "AceCreIm"), ("leetcode", "leotcede"), ("xyz", "xyz")]
for s, want in examples:
    got = rv_two_pointers(s)
    assert got == rv_brute(s) == want, (s, got)
    print(repr(s), "->", repr(got))

assert rv_two_pointers("") == ""
assert rv_two_pointers("a") == "a"
assert rv_two_pointers("aeiou") == "uoiea"
assert rv_two_pointers("AbcdE") == "EbcdA"
assert rv_two_pointers("y") == "y"                       # y is not a vowel here
assert rv_two_pointers("bcd" * 100000) == "bcd" * 100000  # max size, no vowels
big = "ab" * 150000
assert rv_two_pointers(big) == big                        # all vowels equal 'a'

rng = random.Random(17)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("aeiouAEIOUbcxyz ! ") for _ in range(rng.randint(0, 12)))
    assert rv_two_pointers(s) == rv_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
