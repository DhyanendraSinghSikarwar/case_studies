from itertools import product


def lvp_brute(s):
    best = 0
    for i in range(len(s)):
        bal = 0
        for j in range(i, len(s)):
            bal += 1 if s[j] == "(" else -1
            if bal < 0:
                break
            if bal == 0:
                best = max(best, j - i + 1)
    return best


def lvp_stack(s):
    stack = [-1]
    best = 0
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best


def lvp_two_pass(s):
    best = left = right = 0
    for c in s:
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * right)
        elif right > left:
            left = right = 0
    left = right = 0
    for c in reversed(s):
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * left)
        elif left > right:
            left = right = 0
    return best


def lvp_one_pass_only(s):                            # the bug: left-to-right pass alone
    best = left = right = 0
    for c in s:
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * right)
        elif right > left:
            left = right = 0
    return best


examples = [("(()", 2), (")()())", 4), ("", 0), ("()(())", 6), ("()(()", 2)]
for s, want in examples:
    got = lvp_stack(s)
    assert got == lvp_two_pass(s) == lvp_brute(s) == want, (s, got)
    print(repr(s), "->", got)

print("left-to-right only on '(()' ->", lvp_one_pass_only("(()"), "(wrong); correct:", lvp_two_pass("(()"))
assert lvp_one_pass_only("(()") == 0 and lvp_two_pass("(()") == 2
assert lvp_stack("((((") == 0 and lvp_stack("))))") == 0
assert lvp_stack("()" * 15000) == 30000 and lvp_two_pass("()" * 15000) == 30000
assert lvp_stack("(" * 15000 + ")" * 15000) == 30000
assert lvp_stack("(" * 15000 + ")" * 14999) == 29998

total = 0
for n in range(0, 13):                               # every string up to length 12
    for t in product("()", repeat=n):
        s = "".join(t)
        want = lvp_brute(s)
        assert lvp_stack(s) == want and lvp_two_pass(s) == want, s
        total += 1
print("exhaustive check passed:", total, "strings of length 0 to 12")
