VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s):
    total = 0
    for i, ch in enumerate(s):
        v = VAL[ch]
        if i + 1 < len(s) and v < VAL[s[i + 1]]:
            total -= v
        else:
            total += v
    return total


def int_to_roman(n):
    # brute-force oracle: greedy encode, used to test the decoder for every value
    table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
             (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for v, sym in table:
        while n >= v:
            out.append(sym)
            n -= v
    return "".join(out)


def roman_to_int_right_to_left(s):
    # alternative: walk from the right, remember the biggest symbol seen so far
    total = best = 0
    for ch in reversed(s):
        v = VAL[ch]
        if v < best:
            total -= v
        else:
            total += v
            best = v
    return total


examples = [("III", 3), ("LVIII", 58), ("MCMXCIV", 1994), ("IX", 9)]
for s, want in examples:
    assert roman_to_int(s) == roman_to_int_right_to_left(s) == want, (s, want)
    print(s, "->", roman_to_int(s))

assert roman_to_int("I") == 1
assert roman_to_int("MMMCMXCIX") == 3999
assert roman_to_int("IV") == 4 and roman_to_int("VI") == 6
for n in range(1, 4000):                       # exhaustive: every legal value
    r = int_to_roman(n)
    assert roman_to_int(r) == n, (n, r)
    assert roman_to_int_right_to_left(r) == n, (n, r)
print("exhaustive round-trip passed: 3999 values")
