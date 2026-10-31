import random
import re
import sys


def calc_brute(s):
    # reference only: recursive-descent parser (recursion depth = nesting depth)
    pos = 0

    def expr():
        nonlocal pos
        total, sign = 0, 1
        while pos < len(s) and s[pos] != ")":
            c = s[pos]
            if c == " ":
                pos += 1
            elif c == "+":
                sign = 1
                pos += 1
            elif c == "-":
                sign = -1
                pos += 1
            elif c == "(":
                pos += 1
                total += sign * expr()
                pos += 1  # skip ')'
                sign = 1
            else:
                num = 0
                while pos < len(s) and s[pos].isdigit():
                    num = num * 10 + int(s[pos])
                    pos += 1
                total += sign * num
                sign = 1
        return total

    return expr()


def calc(s):
    result, sign, num = 0, 1, 0
    stack = []  # saved (result, sign) of the enclosing contexts
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "+" or ch == "-":
            result += sign * num
            num = 0
            sign = 1 if ch == "+" else -1
        elif ch == "(":
            stack.append(result)
            stack.append(sign)
            result, sign = 0, 1
        elif ch == ")":
            result += sign * num
            num = 0
            result = result * stack.pop() + stack.pop()  # sign first, then outer result
    return result + sign * num


examples = [("1 + 1", 2), (" 2-1 + 2 ", 3), ("(1+(4+5+2)-3)+(6+8)", 23), ("-(2+3)", -5), ("2-(5-6)", 3)]
for s, want in examples:
    got = calc(s)
    assert got == calc_brute(s) == eval(s) == want, (s, got)  # eval only as a test oracle
    print(repr(s), "->", got)

assert calc("0") == 0
assert calc("(((5)))") == 5
assert calc("-(-(2))") == 2
assert calc("2-(-3)") == 5
assert calc(" ( 0 ) + 4 ") == 4
assert calc("10-(2-(3-(4-5)))") == eval("10-(2-(3-(4-5)))")


def gen(rng, depth):
    parts = []
    if rng.random() < 0.3:
        parts.append("-")  # unary minus only at the start of a group
    for t in range(rng.randint(1, 4)):
        if t:
            parts.append(rng.choice("+-"))
        if depth < 3 and rng.random() < 0.3:
            parts.append("(" + gen(rng, depth + 1) + ")")
        else:
            parts.append(str(rng.randint(0, 120)))
    return "".join(parts)


rng = random.Random(11)
for _ in range(2000):
    e = gen(rng, 0)
    e = re.sub(r"\d+|.", lambda m: m.group() + (" " if rng.random() < 0.3 else ""), e)  # spaces between tokens
    assert calc(e) == calc_brute(e) == eval(e.replace(" ", "")), e
print("random cross-check passed: 2000 cases")

deep = "(" * 100000 + "1" + ")" * 100000 + "+" + "-(" * 50000 + "2" + ")" * 50000
print("stack version, 150000-deep nesting ->", calc(deep))
print("recursion limit on this run:", sys.getrecursionlimit())
try:
    calc_brute(deep)
    print("recursive version: ok")
except RecursionError:
    print("recursive version: RecursionError")
