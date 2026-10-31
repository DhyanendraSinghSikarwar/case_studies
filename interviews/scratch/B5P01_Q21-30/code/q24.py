import random


def encode_naive(strs):
    return ",".join(strs)


def decode_naive(s):
    return s.split(",")


def encode(strs):
    """length + '#' + payload, concatenated."""
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode(s):
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)           # first '#' after i ends the length field
        length = int(s[i:j])          # digits only, so the first '#' is ours
        out.append(s[j + 1:j + 1 + length])   # take exactly `length` chars
        i = j + 1 + length            # jump over the payload unread
    return out


ex = ["we", "say", ":", "yes"]
enc = encode(ex)
print("encoded:", repr(enc))
print("decoded:", decode(enc))
assert decode(enc) == ex

# why a separator is unsafe
bad = ["a,b", "c"]
print("naive round trip of", bad, "->", decode_naive(encode_naive(bad)))
assert decode_naive(encode_naive(bad)) != bad
print("naive round trip of [] ->", decode_naive(encode_naive([])), "(wrong: one empty string)")
assert decode_naive(encode_naive([])) != []

# --- edge cases
for case in ([], [""], ["", ""], ["#"], ["3#abc"], ["12", "3"], ["0#"],
             ["a" * 1000], ["héllo", "日本語", "😀"], ["1#1#1"], ["\n", " "]):
    assert decode(encode(case)) == case, case
assert encode([]) == "" and encode([""]) == "0#"
print("edge cases OK")

# --- seeded randomised check (adversarial alphabet: digits, '#', ',', letters)
rng = random.Random(24)
alpha = "#0123456789,ab "
for _ in range(2000):
    strs = ["".join(rng.choice(alpha) for _ in range(rng.randint(0, 6)))
            for _ in range(rng.randint(0, 6))]
    assert decode(encode(strs)) == strs
print("2000 random round trips OK")
