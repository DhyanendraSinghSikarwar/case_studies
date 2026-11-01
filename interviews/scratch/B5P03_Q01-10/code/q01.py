import random


def rev_words_split(s):
    return " ".join(reversed(s.split()))


def rev_words_manual(s):
    # scan from the right; collect each word, no split()
    words = []
    i = len(s) - 1
    while i >= 0:
        while i >= 0 and s[i] == " ":
            i -= 1
        if i < 0:
            break
        j = i
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1:j + 1])
    return " ".join(words)


def rev_words_inplace(chars):
    # chars is a list of single characters; O(1) extra space, mutates and returns it
    def rev(a, b):  # reverse chars[a..b] inclusive
        while a < b:
            chars[a], chars[b] = chars[b], chars[a]
            a += 1
            b -= 1

    n = len(chars)
    rev(0, n - 1)
    i = 0
    while i < n:                      # reverse each word back
        if chars[i] == " ":
            i += 1
            continue
        j = i
        while j + 1 < n and chars[j + 1] != " ":
            j += 1
        rev(i, j)
        i = j + 1
    # squeeze spaces in place: write pointer w, one space between words
    w = 0
    i = 0
    while i < n:
        if chars[i] != " ":
            if w > 0:
                chars[w] = " "
                w += 1
            while i < n and chars[i] != " ":
                chars[w] = chars[i]
                w += 1
                i += 1
        else:
            i += 1
    del chars[w:]
    return chars


examples = [("  the sky  is blue ", "blue is sky the"), ("a", "a"), ("   ", "")]
for s, want in examples:
    a, b = rev_words_split(s), rev_words_manual(s)
    c = "".join(rev_words_inplace(list(s)))
    assert a == b == c == want, (s, a, b, c, want)
    print(repr(s), "->", repr(a))

assert rev_words_manual("") == "" and rev_words_split("") == ""
assert rev_words_manual("x  y") == "y x"
assert rev_words_manual(" ab") == "ab"
assert "".join(rev_words_inplace(list("hello   world  "))) == "world hello"
big = "ab " * 3333 + "z"
assert rev_words_manual(big) == rev_words_split(big)

rng = random.Random(3)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("ab1  ") for _ in range(rng.randint(1, 12)))
    want = rev_words_split(s)
    assert rev_words_manual(s) == want, s
    assert "".join(rev_words_inplace(list(s))) == want, s
    cases += 1
print("random cross-check passed:", cases, "cases")
