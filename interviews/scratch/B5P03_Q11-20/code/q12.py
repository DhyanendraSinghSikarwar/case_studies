import random


def rep_brute(s):
    n = len(s)
    return any(s == s[:k] * (n // k) for k in range(1, n) if n % k == 0)


def rep_double(s):
    return s in (s + s)[1:-1]


def prefix_function(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def rep_kmp(s):
    n = len(s)
    p = n - prefix_function(s)[-1]
    return p < n and n % p == 0


examples = [("abab", True), ("aba", False), ("abcabcabcabc", True), ("a", False)]
for s, want in examples:
    assert rep_brute(s) == rep_double(s) == rep_kmp(s) == want, s
    print(repr(s), "->", rep_kmp(s))

assert prefix_function("abcabc") == [0, 0, 0, 1, 2, 3]
assert rep_kmp("aaaa") and rep_double("aaaa")
assert not rep_kmp("abaab") and not rep_double("abaab")
assert not rep_kmp("abcab")            # period 3 but 5 % 3 != 0
assert rep_kmp("ab" * 5000) and not rep_kmp("a" * 9999 + "b")  # max size

rng = random.Random(12)
cases = 0
for _ in range(3000):
    if rng.random() < 0.5:
        s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 12)))
    else:
        blk = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
        s = blk * rng.randint(1, 4)
    assert rep_brute(s) == rep_double(s) == rep_kmp(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
