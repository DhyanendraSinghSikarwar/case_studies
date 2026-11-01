import random


def mul_brute(a, b):
    # reference only: uses Python's big int, which the real answer must avoid
    return str(int(a) * int(b))


def mul_school(a, b):
    if a == "0" or b == "0":
        return "0"
    n, m = len(a), len(b)
    res = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        da = ord(a[i]) - 48
        for j in range(m - 1, -1, -1):
            cur = res[i + j + 1] + da * (ord(b[j]) - 48)
            res[i + j + 1] = cur % 10
            res[i + j] += cur // 10
    k = 0
    while k < len(res) - 1 and res[k] == 0:
        k += 1
    return "".join(map(str, res[k:]))


examples = [("2", "3", "6"), ("123", "456", "56088"), ("0", "9999", "0"), ("99", "99", "9801")]
for a, b, want in examples:
    got = mul_school(a, b)
    assert got == mul_brute(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert mul_school("9" * 200, "9" * 200) == mul_brute("9" * 200, "9" * 200)  # max size
assert mul_school("1", "1") == "1"
assert mul_school("10", "10") == "100"
assert mul_school("9999", "0") == "0"
assert mul_school("5", "5") == "25"

rng = random.Random(11)
cases = 0
for _ in range(1500):
    a = str(rng.randint(0, 10 ** rng.randint(1, 12)))
    b = str(rng.randint(0, 10 ** rng.randint(1, 12)))
    assert mul_school(a, b) == mul_brute(a, b), (a, b)
    cases += 1
print("random cross-check passed:", cases, "cases")
