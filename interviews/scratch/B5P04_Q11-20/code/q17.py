import itertools
import random


def is_valid(t):
    bal = 0
    for c in t:
        if c == "(":
            bal += 1
        elif c == ")":
            bal -= 1
            if bal < 0:
                return False
    return bal == 0


def all_best_brute(s):
    # reference: try deleting r parentheses for r = 0, 1, 2, ...; the first r that works is minimal.
    # Returns the SET of all valid strings reachable with that minimum number of deletions.
    spots = [i for i, c in enumerate(s) if c in "()"]
    for r in range(len(spots) + 1):
        found = set()
        for drop in itertools.combinations(spots, r):
            d = set(drop)
            t = "".join(c for i, c in enumerate(s) if i not in d)
            if is_valid(t):
                found.add(t)
        if found:
            return r, found


def min_remove(s):
    stack = []                 # indices of '(' still waiting for a ')'
    drop = set()
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        elif c == ")":
            if stack:
                stack.pop()    # matched
            else:
                drop.add(i)    # closer with nothing to close: drop it
    drop.update(stack)         # openers never closed: drop them
    return "".join(c for i, c in enumerate(s) if i not in drop)


def min_remove_count(s):
    # count-only variant: no stack, two counters
    open_, extra = 0, 0
    for c in s:
        if c == "(":
            open_ += 1
        elif c == ")":
            if open_:
                open_ -= 1
            else:
                extra += 1
    return open_ + extra


examples = [("lee(t(c)o)de)", "lee(t(c)o)de"), ("a)b(c)d", "ab(c)d"), ("))((", ""), ("(a(b(c)d)", "a(b(c)d)")]
for s, want in examples:
    got = min_remove(s)
    r, best = all_best_brute(s)
    assert got == want and got in best and is_valid(got), (s, got)
    assert len(s) - len(got) == r == min_remove_count(s)
    print(repr(s), "->", repr(got), "| removals:", r, "| valid answers of that size:", sorted(best))

assert min_remove("") == "" and min_remove("abc") == "abc"
assert min_remove("(") == "" and min_remove(")") == ""
assert min_remove("()") == "()" and min_remove(")(") == ""
assert min_remove("((()))") == "((()))"
assert min_remove("(" * 50000 + ")" * 50000) == "(" * 50000 + ")" * 50000
assert min_remove(")" * 50000 + "(" * 50000) == ""

# exhaustive over alphabet 'a()', every string up to length 8
checked, multi = 0, 0
for n in range(0, 9):
    for tup in itertools.product("a()", repeat=n):
        s = "".join(tup)
        got = min_remove(s)
        r, best = all_best_brute(s)
        assert got in best and len(s) - len(got) == r == min_remove_count(s), s
        checked += 1
        multi += len(best) > 1
print("exhaustive check passed:", checked, "strings;", multi, "of them have more than one valid minimal answer")

rng = random.Random(17)
for _ in range(500):
    s = "".join(rng.choice("ab(()") for _ in range(rng.randint(0, 11)))
    r, best = all_best_brute(s)
    assert min_remove(s) in best and is_valid(min_remove(s))
print("random cross-check passed: 500 cases")
