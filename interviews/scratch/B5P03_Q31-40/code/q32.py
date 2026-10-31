import random


def valid_utf8_reference(data):
    """Reference: Python's own decoder (stricter: also rejects overlong, surrogates, > U+10FFFF)."""
    try:
        bytes(data).decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def valid_utf8_structural(data):
    """Structure only, the version the prompt asks for."""
    owed = 0                                  # continuation bytes still expected
    for b in data:
        if owed == 0:
            if b >> 7 == 0b0:                 # 0xxxxxxx
                continue
            elif b >> 5 == 0b110:             # 110xxxxx
                owed = 1
            elif b >> 4 == 0b1110:            # 1110xxxx
                owed = 2
            elif b >> 3 == 0b11110:           # 11110xxx
                owed = 3
            else:                             # 10xxxxxx stray continuation, or 11111xxx
                return False
        else:
            if b >> 6 != 0b10:                # must be 10xxxxxx
                return False
            owed -= 1
    return owed == 0                          # sequence must not be cut off


print(valid_utf8_structural([197, 130, 1]))
print(valid_utf8_structural([235, 140, 4]))
print(valid_utf8_structural([255]))
print(valid_utf8_structural([]))
assert valid_utf8_structural([197, 130, 1]) is True
assert valid_utf8_structural([235, 140, 4]) is False
assert valid_utf8_structural([255]) is False
assert valid_utf8_structural([]) is True
assert valid_utf8_structural([0x80]) is False           # lone continuation
assert valid_utf8_structural([0xC2]) is False           # truncated at end
assert valid_utf8_structural([0xF0, 0x9F, 0x98, 0x80]) is True   # U+1F600
assert valid_utf8_structural([0xF0, 0x9F, 0x98]) is False
assert valid_utf8_structural(list("héllo €".encode("utf-8"))) is True
assert valid_utf8_structural([0xC2, 0xC2]) is False     # lead followed by lead

# what the structural check accepts but the real decoder rejects (the checks we skip)
for name, bs in [("overlong '/' C0 AF", [0xC0, 0xAF]),
                 ("surrogate U+D800 ED A0 80", [0xED, 0xA0, 0x80]),
                 ("above U+10FFFF F4 90 80 80", [0xF4, 0x90, 0x80, 0x80]),
                 ("F8 88 80 80 80 (5-byte lead)", [0xF8, 0x88, 0x80, 0x80, 0x80])]:
    print(f"{name}: structural={valid_utf8_structural(bs)} python={valid_utf8_reference(bs)}")

# random cross-check against the real decoder. The pool avoids C0/C1, E0, ED and F4-FF
# leads, but F0 followed by 80..8F is still an overlong form, so a few disagreements
# are expected and each one is checked to be exactly that kind.
rng = random.Random(32)
pool = [0x41, 0x7F, 0x80, 0xBF, 0xC2, 0xDF, 0xE1, 0xEC, 0xEE, 0xF0, 0xF1, 0xA9, 0x9F, 0x90]
agree = 0
for _ in range(20000):
    data = [rng.choice(pool) for _ in range(rng.randint(0, 6))]
    s = valid_utf8_structural(data)
    r = valid_utf8_reference(data)
    if s != r:
        # the only allowed disagreement: an F0 lead with a too-small second byte (overlong)
        assert s and not r, data
        assert 0xF0 in data, data
    agree += (s == r)
print("random cross-check passed, exact agreement on", agree, "of 20000")
# real encoder output always passes both
for _ in range(2000):
    txt = "".join(chr(rng.choice([0x41, 0xE9, 0x20AC, 0x1F600, 0x4E2D])) for _ in range(rng.randint(0, 8)))
    bs = list(txt.encode("utf-8"))
    assert valid_utf8_structural(bs) and valid_utf8_reference(bs)
print("encoder round-trip passed: 2000 cases")
