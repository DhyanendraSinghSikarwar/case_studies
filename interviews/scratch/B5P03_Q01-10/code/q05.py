import random


def rotate_brute(s, goal):
    if len(s) != len(goal):
        return False
    return any(s[k:] + s[:k] == goal for k in range(len(s)))


def rotate_check(s, goal):
    return len(s) == len(goal) and goal in s + s


def rotate_check_no_length(s, goal):      # the bug: forgets the length check
    return goal in s + s


examples = [("abcde", "cdeab", True), ("abcde", "abced", False), ("aa", "a", False)]
for s, g, want in examples:
    assert rotate_check(s, g) == rotate_brute(s, g) == want, (s, g)
    print((s, g), "->", want)

print("without the length check, ('aa','a') ->", rotate_check_no_length("aa", "a"), "(wrong)")
assert rotate_check_no_length("aa", "a") is True
assert rotate_check("a", "a") is True
assert rotate_check("ab", "ba") is True
assert rotate_check("abc", "abc") is True          # zero rotation allowed
assert rotate_check("abc", "abca") is False
assert rotate_check("a" * 100, "a" * 100) is True
assert rotate_check("a" * 99 + "b", "b" + "a" * 99) is True
assert rotate_check("abab", "baba") is True

rng = random.Random(5)
cases = trues = 0
for _ in range(5000):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
    if rng.random() < 0.5:
        k = rng.randint(0, len(s))
        g = s[k:] + s[:k]
        if rng.random() < 0.3:
            g = g[:-1] + rng.choice("ab")
    else:
        g = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
    want = rotate_brute(s, g)
    assert rotate_check(s, g) == want, (s, g)
    trues += want
    cases += 1
print("random cross-check passed:", cases, "cases,", trues, "of them True")
