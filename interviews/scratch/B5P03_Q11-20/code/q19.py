import random


def zig_brute(s, rows):
    # reference: compute each character's row from the cycle position
    if rows == 1 or rows >= len(s):
        return s
    cycle = 2 * (rows - 1)
    buckets = [[] for _ in range(rows)]
    for i, c in enumerate(s):
        k = i % cycle
        buckets[k if k < rows else cycle - k].append(c)
    return "".join("".join(b) for b in buckets)


def zig_flag(s, rows):
    if rows == 1:
        return s
    bufs = [[] for _ in range(min(rows, len(s)))]
    r, step = 0, 1
    for c in s:
        bufs[r].append(c)
        if r == 0:
            step = 1
        elif r == len(bufs) - 1:
            step = -1
        r += step
    return "".join("".join(b) for b in bufs)


examples = [("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"), ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"), ("AB", 1, "AB")]
for s, k, want in examples:
    got = zig_flag(s, k)
    assert got == zig_brute(s, k) == want, (s, k, got)
    print((s, k), "->", got)

assert zig_flag("A", 5) == "A"            # more rows than characters
assert zig_flag("AB", 5) == "AB"
assert zig_flag("ABC", 2) == "ACB"
assert zig_flag("", 3) == ""
assert zig_flag("ABCD", 4) == "ABCD"
assert zig_flag("x" * 1000, 1) == "x" * 1000

rng = random.Random(19)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("abcdefgh") for _ in range(rng.randint(0, 20)))
    k = rng.randint(1, 8)
    assert zig_flag(s, k) == zig_brute(s, k), (s, k)
    assert sorted(zig_flag(s, k)) == sorted(s)
    cases += 1
print("random cross-check passed:", cases, "cases")
