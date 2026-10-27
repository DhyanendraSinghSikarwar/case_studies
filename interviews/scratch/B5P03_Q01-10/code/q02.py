import random


def lcp_brute(strs):
    # try every length k from the length of strs[0] downwards
    for k in range(len(strs[0]), -1, -1):
        p = strs[0][:k]
        if all(t.startswith(p) for t in strs):
            return p


def lcp_vertical(strs):
    first = strs[0]
    for i in range(len(first)):
        for t in strs[1:]:
            if i == len(t) or t[i] != first[i]:
                return first[:i]
    return first


def lcp_horizontal(strs):
    prefix = strs[0]
    for t in strs[1:]:
        while not t.startswith(prefix):
            prefix = prefix[:-1]
    return prefix


def lcp_minmax(strs):
    lo, hi = min(strs), max(strs)      # lexicographic order
    i = 0
    while i < len(lo) and i < len(hi) and lo[i] == hi[i]:
        i += 1
    return lo[:i]


examples = [(["flower", "flow", "flight"], "fl"), (["dog", "racecar", "car"], ""),
            (["a"], "a"), (["", "b"], "")]
for strs, want in examples:
    r = [lcp_brute(strs), lcp_vertical(strs), lcp_horizontal(strs), lcp_minmax(strs)]
    assert all(x == want for x in r), (strs, r, want)
    print(strs, "->", repr(want))

assert lcp_vertical(["abc", "abc", "abc"]) == "abc"
assert lcp_vertical(["ab", "abc"]) == "ab"          # one string is a prefix of another
assert lcp_minmax(["abc", "ab", "abd"]) == "ab"
assert lcp_horizontal(["", ""]) == ""
assert lcp_minmax(["x" * 200] * 200) == "x" * 200

rng = random.Random(11)
cases = 0
for _ in range(3000):
    k = rng.randint(1, 5)
    strs = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 6))) for _ in range(k)]
    want = lcp_brute(strs)
    assert lcp_vertical(strs) == want, strs
    assert lcp_horizontal(strs) == want, strs
    assert lcp_minmax(strs) == want, strs
    cases += 1
print("random cross-check passed:", cases, "cases")
