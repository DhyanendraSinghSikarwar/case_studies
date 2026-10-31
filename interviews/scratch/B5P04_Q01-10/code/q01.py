import itertools
import random

PAIR = {")": "(", "]": "[", "}": "{"}


def valid_brute(s):
    # keep deleting adjacent matched pairs; valid iff nothing is left
    prev = None
    while prev != s:
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""


def valid_stack(s):
    stack = []
    for ch in s:
        if ch in PAIR:                       # a closer
            if not stack or stack[-1] != PAIR[ch]:
                return False                 # failure mode 1: empty stack or wrong partner
            stack.pop()
        else:
            stack.append(ch)                 # an opener
    return not stack                         # failure mode 2: openers left over


def valid_counter(s):
    # the tempting but wrong version: one counter for all three types
    c = 0
    for ch in s:
        c += 1 if ch in "([{" else -1
        if c < 0:
            return False
    return c == 0


examples = [("()[]{}", True), ("(]", False), ("([{}])", True),
            ("((", False), ("]", False), ("([)]", False)]
for s, want in examples:
    assert valid_brute(s) == valid_stack(s) == want, s
    print(repr(s), "->", valid_stack(s))

# why a counter is not enough
print("counter says '([)]' is", valid_counter("([)]"), "but stack says", valid_stack("([)]"))
assert valid_counter("([)]") is True and valid_stack("([)]") is False

# edge cases
assert valid_stack("") is True               # not in the prompt's range, but the natural base case
assert valid_stack("(" * 5000 + ")" * 5000)   # deep nesting is fine: explicit stack, no recursion
assert not valid_stack("(" * 5000 + ")" * 4999)
assert not valid_stack("}{")                 # counter-style balance but wrong order
assert not valid_stack(")(")

# exhaustive check: every string over the 6 characters up to length 7
total = 0
for n in range(0, 8):
    for tup in itertools.product("()[]{}", repeat=n):
        s = "".join(tup)
        assert valid_stack(s) == valid_brute(s), s
        total += 1
print("exhaustive check passed:", total, "strings (length 0..7)")

# seeded random longer strings, biased towards valid ones by building from pairs
rng = random.Random(5)
valid_seen = 0
for _ in range(2000):
    parts = []
    for _ in range(rng.randint(1, 8)):
        o, c = rng.choice(["()", "[]", "{}"])
        parts.append((o, c))
    s = "".join(o for o, _ in parts) + "".join(c for _, c in reversed(parts))
    if rng.random() < 0.5:                   # corrupt half of them
        i = rng.randrange(len(s))
        s = s[:i] + rng.choice("()[]{}") + s[i + 1:]
    assert valid_stack(s) == valid_brute(s), s
    valid_seen += valid_stack(s)
print("random check passed: 2000 cases,", valid_seen, "valid")
