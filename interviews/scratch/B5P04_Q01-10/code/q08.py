import random
import re
import sys


def decode_brute(s):
    # repeatedly expand an innermost k[letters] block until none is left
    pat = re.compile(r"(\d+)\[([a-z]*)\]")
    while True:
        new = pat.sub(lambda m: m.group(2) * int(m.group(1)), s)
        if new == s:
            return s
        s = new


def decode_stack(s):
    stack = []                       # saved (text so far, repeat count) pairs
    cur, k = [], 0                   # text of the current level, number being read
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)     # counts can have several digits
        elif ch == "[":
            stack.append((cur, k))   # save the outer level
            cur, k = [], 0
        elif ch == "]":
            outer, times = stack.pop()
            outer.append("".join(cur) * times)
            cur = outer              # restore the outer level
        else:
            cur.append(ch)
    return "".join(cur)


def decode_rec(s):
    i = 0

    def parse():                     # parse until ']' or the end
        nonlocal i
        out, k = [], 0
        while i < len(s):
            ch = s[i]
            if ch.isdigit():
                k = k * 10 + int(ch); i += 1
            elif ch == "[":
                i += 1
                out.append(parse() * k)   # recursion: one frame per nesting level
                k = 0
            elif ch == "]":
                i += 1
                return "".join(out)
            else:
                out.append(ch); i += 1
        return "".join(out)
    return parse()


examples = [("3[a]2[bc]", "aaabcbc"), ("3[a2[c]]", "accaccacc"),
            ("2[abc]3[cd]ef", "abcabccdcdcdef"), ("ab10[c]", "abcccccccccc")]
for s, want in examples:
    assert decode_brute(s) == decode_stack(s) == decode_rec(s) == want, s
    print(repr(s), "->", repr(decode_stack(s)))

# edge cases
assert decode_stack("abc") == "abc"                    # no brackets
assert decode_stack("1[a]") == "a"
assert decode_stack("300[a]") == "a" * 300             # multi-digit count
assert decode_stack("2[2[2[a]]]") == "a" * 8           # deep multiplication
assert decode_stack("3[]") == ""                       # empty body (outside the prompt's grammar, harmless)
assert decode_stack("2[a]b2[c]") == "aabcc"

# recursion limit: nesting depth 5000, answer is just 'a'
deep = "1[" * 5000 + "a" + "]" * 5000
print("default recursion limit:", sys.getrecursionlimit())
assert decode_stack(deep) == "a"
try:
    decode_rec(deep)
    print("recursive version: OK")
except RecursionError:
    print("recursive version at depth 5000: RecursionError; stack version returned", repr(decode_stack(deep)))

# seeded randomised cross-check on generated valid encodings
rng = random.Random(21)


def gen(depth):
    parts = []
    for _ in range(rng.randint(1, 3)):
        if depth > 0 and rng.random() < 0.5:
            parts.append(str(rng.randint(1, 12)) + "[" + gen(depth - 1) + "]")
        else:
            parts.append("".join(rng.choice("abc") for _ in range(rng.randint(1, 3))))
    return "".join(parts)


n = 0
while n < 1000:
    s = gen(3)
    want = decode_brute(s)
    assert decode_stack(s) == want and decode_rec(s) == want, s
    n += 1
print("random cross-check passed:", n, "encoded strings")
