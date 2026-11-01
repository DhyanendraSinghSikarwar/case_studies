import random


def add_builtin(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]


def add_binary(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    out = []
    while i >= 0 or j >= 0 or carry:
        s = carry
        if i >= 0:
            s += a[i] == "1"; i -= 1
        if j >= 0:
            s += b[j] == "1"; j -= 1
        out.append("1" if s & 1 else "0")
        carry = s >> 1
    return "".join(reversed(out)) or "0"


examples = [("11", "1", "100"), ("1010", "1011", "10101"), ("0", "0", "0")]
for a, b, want in examples:
    got = add_binary(a, b)
    assert got == add_builtin(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert add_binary("1" * 10000, "1") == "1" + "0" * 10000 == add_builtin("1" * 10000, "1")  # int(.., 2) has no 4300-digit limit
assert add_binary("0", "1") == "1"
assert add_binary("00000", "0") == "00000"   # leading zeros (outside the contract) are not stripped
assert add_binary("1", "1") == "10"

rng = random.Random(15)
cases = 0
for _ in range(2000):
    a = rng.choice(["0", "1" + "".join(rng.choice("01") for _ in range(rng.randint(0, 39)))])
    b = rng.choice(["0", "1" + "".join(rng.choice("01") for _ in range(rng.randint(0, 39)))])
    assert int(add_binary(a, b), 2) == int(a, 2) + int(b, 2), (a, b)
    assert add_binary(a, b) == add_builtin(a, b), (a, b)
    cases += 1
print("random cross-check passed:", cases, "cases")
