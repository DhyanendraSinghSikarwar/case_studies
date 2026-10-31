import random


def add_brute(a, b):
    return str(int(a) + int(b))


def add_strings(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    out = []
    while i >= 0 or j >= 0 or carry:
        s = carry
        if i >= 0:
            s += ord(a[i]) - 48; i -= 1
        if j >= 0:
            s += ord(b[j]) - 48; j -= 1
        out.append(chr(48 + s % 10))
        carry = s // 10
    return "".join(reversed(out))


examples = [("11", "123", "134"), ("456", "77", "533"), ("0", "0", "0"), ("999", "1", "1000")]
for a, b, want in examples:
    got = add_strings(a, b)
    assert got == add_brute(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert add_strings("9" * 10000, "1") == "1" + "0" * 10000      # max size, long carry chain
big = add_strings("9" * 10000, "9" * 10000)
assert big == "1" + "9" * 9999 + "8"
try:
    add_brute("9" * 10000, "9" * 10000)
except ValueError as e:
    print("int() on 10000 digits:", str(e)[:44])   # default limit is 4300 digits in Python 3.13
assert add_strings("1", "9") == "10"
assert add_strings("0", "5") == "5"

rng = random.Random(14)
cases = 0
for _ in range(2000):
    a = str(rng.randint(0, 10 ** rng.randint(1, 30)))
    b = str(rng.randint(0, 10 ** rng.randint(1, 30)))
    assert add_strings(a, b) == add_brute(a, b), (a, b)
    cases += 1
print("random cross-check passed:", cases, "cases")
