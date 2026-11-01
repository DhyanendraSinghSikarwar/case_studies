import itertools
import random


def remove_k_brute(num, k):
    # reference: try every way to keep len - k digits, take the smallest NUMBER
    keep = len(num) - k
    if keep == 0:
        return "0"
    best = min(int("".join(c)) for c in itertools.combinations(num, keep))
    return str(best)


def remove_k(num, k):
    stack = []
    for d in num:
        while k and stack and stack[-1] > d:   # a bigger digit before a smaller one: delete it
            stack.pop()
            k -= 1
        stack.append(d)
    if k:
        stack = stack[: len(stack) - k]        # still owe deletions: drop from the end
    return "".join(stack).lstrip("0") or "0"   # no leading zeros, '0' if nothing is left


examples = [(("1432219", 3), "1219"), (("10200", 1), "200"), (("10", 2), "0"), (("9", 1), "0"), (("112", 1), "11")]
for (num, k), want in examples:
    got = remove_k(num, k)
    assert got == remove_k_brute(num, k) == want, (num, k, got)
    print((num, k), "->", repr(got))

assert remove_k("0", 0) == "0"
assert remove_k("123", 0) == "123"                     # k = 0: unchanged
assert remove_k("123", 3) == "0"                       # k = len: nothing left
assert remove_k("12345", 2) == "123"                   # increasing: trim from the end
assert remove_k("54321", 2) == "321"                   # decreasing: pops everything it can
assert remove_k("100", 1) == "0"                       # leading zeros stripped
assert remove_k("1000", 2) == "0"
assert remove_k("10001", 4) == "0"
assert remove_k("22222", 2) == "222"                   # all equal: nothing pops, trim the end
assert remove_k("9" * 100000, 50000) == "9" * 50000    # max size
assert remove_k("1" + "0" * 99999, 1) == "0"

rng = random.Random(20)
cases = 0
for _ in range(3000):
    n = rng.randint(1, 9)
    num = str(rng.randint(1, 9)) + "".join(rng.choice("0123456789" if rng.random() < .5 else "0129") for _ in range(n - 1))
    if rng.random() < 0.05:
        num = "0"
    k = rng.randint(0, len(num))
    assert remove_k(num, k) == remove_k_brute(num, k), (num, k)
    cases += 1
print("random cross-check passed:", cases, "cases")
