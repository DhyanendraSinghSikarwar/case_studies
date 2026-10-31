import random


def tdiv(a, b):
    q = abs(a) // abs(b)                  # Python // floors, so truncate by hand
    return q if (a >= 0) == (b > 0) else -q


def calc_fast(s):
    def apply(stack, op, num):
        if op == "+":
            stack.append(num)
        elif op == "-":
            stack.append(-num)
        elif op == "*":
            stack[-1] *= num
        else:
            stack[-1] = tdiv(stack[-1], num)

    stack, op, num, ctx = [], "+", 0, []
    for ch in s + "+":                    # sentinel flushes the last number
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "(":
            ctx.append((stack, op))       # save the outer context
            stack, op, num = [], "+", 0
        elif ch == ")":
            apply(stack, op, num)
            num = sum(stack)              # value of the bracket becomes the next operand
            stack, op = ctx.pop()
        elif ch != " ":
            apply(stack, op, num)
            op, num = ch, 0
    return sum(stack)


def calc_brute(s):
    # independent recursive-descent parser (fine for the small brute-force sizes)
    t = [c for c in s if c != " "]
    pos = 0

    def expr():
        nonlocal pos
        v = term()
        while pos < len(t) and t[pos] in "+-":
            o = t[pos]; pos += 1
            r = term()
            v = v + r if o == "+" else v - r
        return v

    def term():
        nonlocal pos
        v = atom()
        while pos < len(t) and t[pos] in "*/":
            o = t[pos]; pos += 1
            r = atom()
            v = v * r if o == "*" else tdiv(v, r)
        return v

    def atom():
        nonlocal pos
        if t[pos] == "(":
            pos += 1
            v = expr()
            pos += 1                      # ')'
            return v
        j = pos
        while j < len(t) and t[j].isdigit():
            j += 1
        v = int("".join(t[pos:j]))
        pos = j
        return v

    return expr()


tests = [("1+1", 2), ("6-4/2", 4), ("2*(5+5*2)/3+(6/2+8)", 21),
         ("(2+6*3+5-(3*14/7+2)*5)+3", -12)]
for s, want in tests:
    assert calc_fast(s) == calc_brute(s) == want, s
    print(f"{s!r} -> {calc_fast(s)}")

# edge cases
assert calc_fast("7") == 7 and calc_fast(" 42 ") == 42
assert calc_fast("((7))") == 7
assert calc_fast("(2-5)/2") == -1                 # truncates toward zero (floor would give -2)
assert calc_fast("0-7/2") == -3 and calc_fast("7/2") == 3
assert calc_fast("2*(3+4)*(5-1)") == 56
assert calc_fast("10-(2+3)*2/(1+1)") == 5
assert calc_fast("8/(3-1)/2") == 2                # left-to-right division chain
assert calc_fast("100*(1+(2*(3+(4*5))))") == 4700
assert -7 // 2 == -4 and tdiv(-7, 2) == -3
assert calc_fast("(" * 5000 + "1" + ")" * 5000) == 1   # nesting depth 5000, no recursion used
assert calc_fast("1" + "+1" * 100000) == 100001

# seeded random expressions (skip those with a zero divisor)
rng = random.Random(37)

def gen(depth):
    if depth == 0 or rng.random() < 0.3:
        return str(rng.randint(0, 12))
    a, b = gen(depth - 1), gen(depth - 1)
    o = rng.choice("+-*/")
    e = f"{a}{o}{b}"
    if rng.random() < 0.5:
        e = f"({e})"
    return e

tested = skipped = 0
for _ in range(4000):
    e = gen(rng.randint(1, 4))
    if rng.random() < 0.3:
        e = e.replace("+", " + ")
    try:
        want = calc_brute(e)
    except ZeroDivisionError:
        skipped += 1
        continue
    assert calc_fast(e) == want, e
    tested += 1
print(f"seeded random expressions: {tested} compared, {skipped} skipped (zero divisor)")
