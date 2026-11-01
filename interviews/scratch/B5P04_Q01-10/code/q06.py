import random


def trunc_div(a, b):
    # truncate toward zero without floats (safe for big ints)
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def eval_rpn(tokens):
    st = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = st.pop()                      # second popped = RIGHT operand
            a = st.pop()                      # first operand pushed = LEFT operand
            if t == "+": st.append(a + b)
            elif t == "-": st.append(a - b)
            elif t == "*": st.append(a * b)
            else: st.append(trunc_div(a, b))
        else:
            st.append(int(t))                 # int() handles '-11'
    return st[0]


# independent reference: build a tree-free recursive evaluator from the END of the list
def eval_ref(tokens):
    pos = [len(tokens) - 1]

    def go():
        t = tokens[pos[0]]
        pos[0] -= 1
        if t in "+-*/" and len(t) == 1:
            right = go()                      # the last operand comes first when reading backwards
            left = go()
            if t == "+": return left + right
            if t == "-": return left - right
            if t == "*": return left * right
            q = abs(left) // abs(right)
            return q if (left < 0) == (right < 0) else -q
        return int(t)
    return go()


examples = [
    (["2", "1", "+", "3", "*"], 9),
    (["4", "13", "5", "/", "+"], 6),
    (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
    (["7", "-2", "/"], -3),
]
for toks, want in examples:
    assert eval_rpn(toks) == eval_ref(toks) == want, toks
    print(toks, "->", eval_rpn(toks))

# the floor-division trap
print("7 // -2 =", 7 // -2, "  int(7 / -2) =", int(7 / -2), "  trunc_div(7, -2) =", trunc_div(7, -2))
print("-7 // 2 =", -7 // 2, "  int(-7 / 2) =", int(-7 / 2), "  trunc_div(-7, 2) =", trunc_div(-7, 2))
assert 7 // -2 == -4 and trunc_div(7, -2) == -3 and trunc_div(-7, 2) == -3

# int(a / b) is also unsafe beyond float precision (prompt promises 32-bit, so it is fine there)
big = 10**17 + 1
print("int(big / 1) =", int(big / 1), " trunc_div(big, 1) =", trunc_div(big, 1))
assert trunc_div(big, 1) == big and int(big / 1) != big

# edge cases
assert eval_rpn(["5"]) == 5                               # single operand
assert eval_rpn(["-11"]) == -11                           # a negative number is NOT an operator
assert eval_rpn(["3", "4", "-"]) == -1                    # operand order for '-'
assert eval_rpn(["1", "2", "/"]) == 0
assert eval_rpn(["-1", "2", "/"]) == 0                    # truncation toward zero, not -1
assert eval_rpn(["0", "3", "-"]) == -3

# seeded randomised cross-check: random expression trees -> RPN, compare with both evaluators
rng = random.Random(13)


def gen(depth):
    if depth == 0 or rng.random() < 0.3:
        return [str(rng.randint(-20, 20))]
    left, right = gen(depth - 1), gen(depth - 1)
    op = rng.choice("+-*/")
    return left + right + [op]


def safe(toks):
    # reject expressions that divide by zero (the prompt excludes them)
    st = []
    for t in toks:
        if t in ("+", "-", "*", "/"):
            b, a = st.pop(), st.pop()
            if t == "/" and b == 0:
                return False
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": trunc_div(a, b) if b else 0}[t])
        else:
            st.append(int(t))
    return True


done = 0
while done < 1500:
    toks = gen(4)
    if not safe(toks):
        continue
    assert eval_rpn(toks) == eval_ref(toks), toks
    done += 1
print("random cross-check passed:", done, "expressions")
