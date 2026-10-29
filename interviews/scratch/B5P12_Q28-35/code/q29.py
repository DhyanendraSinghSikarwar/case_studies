import random

random.seed(2901)
MASK = 0xFFFFFFFF


def add(a, b):
    """a + b with only ^, &, <<. Returns [sum, rounds]. Everything is masked to 32 bits."""
    a &= MASK
    b &= MASK
    rounds = 0
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK   # sum without carry, carries moved one place left
        rounds += 1
    return [a if a <= 0x7FFFFFFF else ~(a ^ MASK), rounds]   # ~(a ^ MASK) == a - 2**32 for bit 31 set


def add_no_mask(a, b, cap=40):
    """The same loop WITHOUT masking: for a = -1, b = 1 it never ends (we stop it after `cap` rounds)."""
    trace = []
    for _ in range(cap):
        if b == 0:
            return a, trace
        a, b = a ^ b, (a & b) << 1
        trace.append((a, b))
    return None, trace


def ripple(a, b):
    """Brute force: a 32-bit ripple-carry adder built from single bits (full adders)."""
    out, carry = 0, 0
    for i in range(32):
        x, y = (a >> i) & 1, (b >> i) & 1
        out |= (x ^ y ^ carry) << i
        carry = (x & y) | (carry & (x ^ y))
    return out - (1 << 32) if out >> 31 else out


# dry run on a = 7, b = 5
a, b, r = 7, 5, 0
while b:
    a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
    r += 1
    print(f"round {r}: a = {a:04b} ({a}), b = {b:04b} ({b})")

for (x, y), want in [((7, 5), [12, 3]), ((-3, 3), [0, 32]), ((10**9, 10**9), [2 * 10**9, 2]),
                     ((-10**9, -10**9), [-2 * 10**9, 2]), ((0, 0), [0, 0])]:
    got = add(x, y)
    assert got == want and got[0] == ripple(x, y) == x + y, (x, y, got)
    print(f"add({x}, {y}) -> {got}")

res, trace = add_no_mask(-1, 1)
print("no mask, a=-1, b=1: result after 40 rounds =", res, "| first states (a, b):", trace[:3], "... last b =", trace[-1][1])

# seeded random cross-check against the ripple-carry adder (sum only) and against +
mx = 0
for _ in range(20000):
    x, y = random.randint(-10**9, 10**9), random.randint(-10**9, 10**9)
    s, rounds = add(x, y)
    assert s == ripple(x, y) == x + y
    mx = max(mx, rounds)
for x in range(-70, 71):
    for y in range(-70, 71):
        assert add(x, y)[0] == ripple(x, y) == x + y
print("20000 random + 141*141 small pairs ok; most rounds seen in the random run:", mx)
assert 2 * 10**9 < 2**31
assert add(10**9, 10**9)[0] == 2 * 10**9 and add(-1, 1) == [0, 32]
print("edge asserts ok")
