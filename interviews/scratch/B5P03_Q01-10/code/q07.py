import random
import re

INT_MAX, INT_MIN = 2**31 - 1, -2**31


def my_atoi(s):
    i, n = 0, len(s)
    while i < n and s[i] == " ":          # skip leading spaces only (not tabs)
        i += 1
    sign = 1
    if i < n and s[i] in "+-":
        sign = -1 if s[i] == "-" else 1
        i += 1
    limit = 2**31 if sign == -1 else 2**31 - 1
    res = 0
    while i < n and "0" <= s[i] <= "9":   # not str.isdigit(): that accepts other scripts
        res = res * 10 + (ord(s[i]) - 48)
        if res > limit:                   # clamp now; res never exceeds ~2^31 * 10
            return INT_MIN if sign == -1 else INT_MAX
        i += 1
    return sign * res


def atoi_regex(s):                        # oracle only: regex + int() on the matched part
    m = re.match(r" *([+-]?[0-9]+)", s)
    if not m:
        return 0
    return max(INT_MIN, min(INT_MAX, int(m.group(1))))


examples = [("42", 42), ("   -042", -42), ("1337c0d3", 1337), ("words and 987", 0),
            ("-91283472332", -2147483648), ("+-12", 0)]
for s, want in examples:
    assert my_atoi(s) == atoi_regex(s) == want, (s, my_atoi(s), want)
    print(repr(s), "->", my_atoi(s))

assert my_atoi("") == 0 and my_atoi("   ") == 0
assert my_atoi("-") == 0 and my_atoi("+") == 0
assert my_atoi("2147483647") == INT_MAX
assert my_atoi("2147483648") == INT_MAX
assert my_atoi("-2147483648") == INT_MIN
assert my_atoi("-2147483649") == INT_MIN
assert my_atoi("0" * 50 + "12") == 12                  # leading zeros never trigger the clamp
assert my_atoi("9" * 200) == INT_MAX
assert my_atoi("\t1") == 0                            # tab is not a skipped space
assert my_atoi("  +0 12") == 0
assert my_atoi("3.14") == 3
assert my_atoi("٣") == 0                         # Arabic-Indic digit three: not a digit here
assert "٣".isdigit() and int("٣") == 3      # but isdigit()/int() would accept it

rng = random.Random(9)
cases = 0
for _ in range(5000):
    parts = [" " * rng.randint(0, 2), rng.choice(["", "+", "-", "+-", "-+"]),
             "".join(rng.choice("0123456789") for _ in range(rng.randint(0, 12))),
             rng.choice(["", "x", " 5", ".5", "e3"])]
    s = "".join(parts)
    assert my_atoi(s) == atoi_regex(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
