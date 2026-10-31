import random


def calc_brute(expr):
    # reference: Python eval with floor division replaced by truncation via tokens
    toks, i = [], 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            toks.append(int(expr[i:j])); i = j
        elif c in "+-*/":
            toks.append(c); i += 1
        else:
            i += 1
    # evaluate * and / first, then + and -
    out = [toks[0]]
    k = 1
    while k < len(toks):
        op, v = toks[k], toks[k + 1]
        if op == "*":
            out[-1] *= v
        elif op == "/":
            q = abs(out[-1]) // v
            out[-1] = q if out[-1] >= 0 else -q
        else:
            out += [op, v]
        k += 2
    total = out[0]
    for k in range(1, len(out), 2):
        total = total + out[k + 1] if out[k] == "+" else total - out[k + 1]
    return total


def calc(expr):
    total, last, num, op = 0, 0, 0, "+"
    for ch in expr + "+":   # sentinel flushes the final number
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                total += last; last = num
            elif op == "-":
                total += last; last = -num
            elif op == "*":
                last = last * num
            else:
                q = abs(last) // num
                last = q if last >= 0 else -q   # truncate toward zero
            op, num = ch, 0
    return total + last


examples = [("3+2*2", 7), (" 3/2 ", 1), (" 3+5 / 2 ", 5), ("14-3/2", 13), ("10-20/3", 4)]
for e, want in examples:
    got = calc(e)
    assert got == calc_brute(e) == want, (e, got)
    print(repr(e), "->", got)

assert calc("0") == 0
assert calc("7") == 7
assert calc("1-1+1") == 1
assert calc("2*3*4") == 24
assert calc("1-2*3/4") == 0        # 6/4 truncates to 1, then 1 - 1
assert calc("1-6/4") == 0          # 1 - 1
assert calc("0-5/2") == -2         # last = -5, then -5/2 truncates to -2, not -3
assert calc("100000*100000*100000") == 10 ** 15   # no overflow in Python
assert calc("1+" * 1000 + "1") == 1001

rng = random.Random(13)
cases = 0
for _ in range(3000):
    parts = [str(rng.randint(1, 20))]
    for _ in range(rng.randint(0, 6)):
        parts.append(rng.choice("+-*/"))
        parts.append(str(rng.randint(1, 20)))
    e = "".join(p if rng.random() < 0.8 else " " + p + " " for p in parts)
    assert calc(e) == calc_brute(e), e
    cases += 1
print("random cross-check passed:", cases, "cases")
