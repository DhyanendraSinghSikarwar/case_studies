import itertools
import random
import re

random.seed(3501)


def solve(num, target, zero_rule=True, trace=None):
    """Returns (sorted expressions, calls). calls counts every dfs call. zero_rule=False only exists
    to measure what the leading-zero rule prunes (its answers then include illegal operands)."""
    n = len(num)
    out = []
    calls = 0

    def dfs(i, expr, val, last, depth):
        nonlocal calls
        calls += 1
        if trace is not None:
            trace.append("  " * depth + f"i={i} expr={expr or '-'} val={val} last={last}" + (" HIT" if i == n and val == target else ""))
        if i == n:
            if val == target:
                out.append(expr)
            return
        for j in range(i + 1, n + 1):                 # operand = num[i:j]
            tok = num[i:j]
            if zero_rule and len(tok) > 1 and tok[0] == "0":
                break                                 # '0x...' and every longer operand starting here are illegal
            v = int(tok)
            if i == 0:
                dfs(j, tok, v, v, depth + 1)
            else:
                dfs(j, expr + "+" + tok, val + v, v, depth + 1)
                dfs(j, expr + "-" + tok, val - v, -v, depth + 1)
                dfs(j, expr + "*" + tok, val - last + last * v, last * v, depth + 1)   # undo last term, redo it times v

    dfs(0, "", 0, 0, 0)
    return sorted(out), calls


def brute(num, target):
    out = []
    for ops in itertools.product(["", "+", "-", "*"], repeat=len(num) - 1):
        e = num[0] + "".join(o + d for o, d in zip(ops, num[1:]))
        if any(len(t) > 1 and t[0] == "0" for t in re.split(r"[+\-*]", e)):
            continue
        if eval(e) == target:                         # eval applies the usual precedence
            out.append(e)
    return sorted(out)


# dry run: decision tree for '105', target 5
tr = []
res, calls = solve("105", 5, trace=tr)
print("\n".join(tr))
print("answer", res, "| dfs calls", calls)

for num, tg, want in [("2345", 25, ["2+3+4*5"]), ("105", 5, ["1*0+5", "10-5"]), ("00", 0, ["0*0", "0+0", "0-0"]),
                      ("9", 9, ["9"]), ("9", 0, [])]:
    got = solve(num, tg)[0]
    assert got == want == brute(num, tg), (num, tg, got)
    print(repr(num), tg, "->", got)

# why value - last + last * v works: '1-2*3' -> val after '1-2' is -1, last is -2
assert eval("1-2*3") == -1 - (-2) + (-2) * 3 == -5

# node counts: with the leading-zero rule against without it, against the 4^(n-1) leaves of the unpruned filling space
print("n  digits      4^(n-1)  calls without rule  calls with rule  valid leaves")
for num in ["12345678", "10203040", "00000000", "10000000", "11111111"]:
    n = len(num)
    c_without = solve(num, 0, zero_rule=False)[1]
    c_with = solve(num, 0)[1]
    leaves = sum(1 for _ in itertools.product(["", "+", "-", "*"], repeat=n - 1)
                 if not any(len(t) > 1 and t[0] == "0" for t in re.split(r"[+\-*]", num[0] + "".join(o + d for o, d in zip(_, num[1:])))))
    print(f"{n}  {num}  {4 ** (n - 1):>7}  {c_without:>18}  {c_with:>15}  {leaves:>12}")

# seeded random cross-check against eval over all 4^(n-1) fillings
for _ in range(300):
    n = random.randint(1, 6)
    num = "".join(random.choice("0123456789" if random.random() < 0.5 else "0012") for _ in range(n))
    tg = random.choice([0, random.randint(-30, 100), eval(num[0] + "".join(random.choice("+-*") + d for d in num[1:]))])
    got = solve(num, tg)[0]
    assert got == brute(num, tg) and got == sorted(set(got)), (num, tg)
print("300 seeded random cases: same sorted list as the eval enumeration, no duplicates")
assert solve("0", 0)[0] == ["0"] and solve("05", 5)[0] == ["0+5"] and solve("05", 0)[0] == ["0*5"] and solve("00", 0)[0] == ["0*0", "0+0", "0-0"]
assert solve("12345678", 10**9)[0] == [] and solve("99999999", 99999999)[0] == ["99999999"]
print("edge asserts ok")
