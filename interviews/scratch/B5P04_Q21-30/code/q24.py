import random
from itertools import combinations


def smallest_brute(s):
    letters = set(s)
    best = None
    n = len(s)
    for r in range(len(letters), len(letters) + 1):
        for idx in combinations(range(n), r):
            cand = "".join(s[i] for i in idx)
            if set(cand) == letters:
                if best is None or cand < best:
                    best = cand
    return best if best is not None else ""


def smallest_stack(s):
    last = {c: i for i, c in enumerate(s)}
    stack, on = [], set()
    for i, c in enumerate(s):
        if c in on:
            continue
        while stack and stack[-1] > c and last[stack[-1]] > i:
            on.discard(stack.pop())
        stack.append(c)
        on.add(c)
    return "".join(stack)


def smallest_no_last_check(s):                       # the bug: always pop bigger tops
    stack, on = [], set()
    for c in s:
        if c in on:
            continue
        while stack and stack[-1] > c:
            on.discard(stack.pop())
        stack.append(c)
        on.add(c)
    return "".join(stack)


examples = [("bcabc", "abc"), ("cbacdcbc", "acdb"), ("abacb", "abc"), ("a", "a")]
for s, want in examples:
    got = smallest_stack(s)
    assert got == smallest_brute(s) == want, (s, got)
    print(repr(s), "->", repr(got))

print("without the last-index check, 'cba' ->", smallest_no_last_check("cba"), "(wrong, c and b are lost)", "| correct:", smallest_stack("cba"))
assert smallest_no_last_check("cba") == "a" and smallest_stack("cba") == "cba"
assert smallest_stack("") == ""
assert smallest_stack("aaaa") == "a"
assert smallest_stack("abcd") == "abcd"
assert smallest_stack("dcba") == "dcba"
assert smallest_stack("ecbacba") == "eacb"
assert len(smallest_stack("zyx" * 1000)) == 3

rng = random.Random(24)
for _ in range(600):
    s = "".join(rng.choice("abcd") for _ in range(rng.randint(1, 10)))
    assert smallest_stack(s) == smallest_brute(s), s
print("random cross-check passed: 600 strings over 'abcd', length up to 10")
