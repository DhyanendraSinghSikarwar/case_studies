TABLE = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
         (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
DIGITS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(r):
    # independent checker: a smaller symbol before a larger one is subtracted
    total = 0
    for i, ch in enumerate(r):
        v = DIGITS[ch]
        total += -v if i + 1 < len(r) and DIGITS[r[i + 1]] > v else v
    return total


def to_roman_digitwise(n):
    # brute force: build each decimal place from a fixed 10-entry table
    th = ["", "M", "MM", "MMM"]
    hu = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    te = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    on = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return th[n // 1000] + hu[n // 100 % 10] + te[n // 10 % 10] + on[n % 10]


def to_roman(n):
    out = []
    for val, sym in TABLE:
        count, n = divmod(n, val)
        out.append(sym * count)
    return "".join(out)


examples = [(3749, "MMMDCCXLIX"), (58, "LVIII"), (1994, "MCMXCIV"), (4, "IV")]
for n, want in examples:
    got = to_roman(n)
    assert got == to_roman_digitwise(n) == want, (n, got)
    print(n, "->", got)

assert to_roman(1) == "I"
assert to_roman(3999) == "MMMCMXCIX"
assert to_roman(2000) == "MM"
for n in range(1, 4000):          # exhaustive over the whole domain
    r = to_roman(n)
    assert r == to_roman_digitwise(n), n
    assert roman_to_int(r) == n, (n, r)
print("exhaustive check passed: 3999 values (greedy == digit table == round trip)")
print("longest numeral:", max((to_roman(n) for n in range(1, 4000)), key=len))
