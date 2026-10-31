import random
import sys
import unicodedata


def reverse_text_brute(s):
    """Reference: split into clusters (base + following marks) with a list, reverse cluster order."""
    clusters = []
    for ch in s:
        if unicodedata.combining(ch) != 0 and clusters:
            clusters[-1] += ch
        else:
            clusters.append(ch)
    return "".join(reversed(clusters))


def reverse_text(s):
    """One right-to-left scan: collect trailing marks, then emit base + marks."""
    out = []
    i = len(s) - 1
    while i >= 0:
        j = i
        while j > 0 and unicodedata.combining(s[j]) != 0:   # walk left over marks
            j -= 1
        out.append(s[j:i + 1])      # base char (s[j]) followed by its marks
        i = j - 1
    return "".join(out)


s = "café"
print(sys.version.split()[0], "unidata", unicodedata.unidata_version)
print(len(s), ascii(s), "->", ascii(reverse_text(s)))
print("plain slice:", ascii("éx"[::-1]))
print("fixed      :", ascii(reverse_text("éx")))
assert reverse_text("café") == "éfac"
assert "éx"[::-1] == "x́e"
assert reverse_text("éx") == "xé"

# where the approximation still fails
flag = "\U0001F1EE\U0001F1F3"                       # regional indicators I + N = India flag
print("flag len", len(flag), "reversed", ascii(reverse_text("a" + flag)))
fam = "\U0001F468‍\U0001F469‍\U0001F467"  # man ZWJ woman ZWJ girl
print("family len", len(fam), "combining on ZWJ:", unicodedata.combining("‍"))
print("jamo combining:", unicodedata.combining("ᄒ"), unicodedata.combining("ᅡ"))
print("NFC recomposes:", ascii(unicodedata.normalize("NFC", "é")), len(unicodedata.normalize("NFC", "é")))
print("stacked marks:", ascii(reverse_text("á̂b")))

# edge cases
assert reverse_text("") == ""
assert reverse_text("a") == "a"
assert reverse_text("́") == "́"            # lone mark has no base
assert reverse_text("́a") == "á"          # leading orphan mark stays its own cluster
assert reverse_text("abc") == "abc"[::-1]
assert reverse_text("á̂b") == "bá̂"   # stacked marks keep order
assert reverse_text("́̂") == "́̂"       # only marks

rng = random.Random(31)
alphabet = ["a", "b", "e", "x", "́", "̂", "̈", "z"]
for _ in range(3000):
    t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 9)))
    got = reverse_text(t)
    assert got == reverse_text_brute(t), ascii(t)
    assert len(got) == len(t)
    assert sorted(got) == sorted(t)
print("random cross-check passed: 3000 cases")
