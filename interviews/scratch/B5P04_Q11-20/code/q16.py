import random


def remove_brute(s, k, rng=None):
    # reference: repeatedly delete a block of k equal adjacent letters.
    # With rng, pick a RANDOM removable block each time (tests order independence);
    # without rng, always take the leftmost block.
    while True:
        spots = [i for i in range(len(s) - k + 1) if s[i:i + k] == s[i] * k]
        if not spots:
            return s
        i = rng.choice(spots) if rng else spots[0]
        s = s[:i] + s[i + k:]


def remove_a(s):
    # part (a): pairs. Stack of letters.
    st = []
    for c in s:
        if st and st[-1] == c:
            st.pop()
        else:
            st.append(c)
    return "".join(st)


def remove_b(s, k):
    # part (b): stack of [letter, run length]; a run that reaches k disappears
    st = []
    for c in s:
        if st and st[-1][0] == c:
            st[-1][1] += 1
            if st[-1][1] == k:
                st.pop()
        else:
            st.append([c, 1])
    return "".join(ch * n for ch, n in st)


examples_a = [("abbaca", "ca"), ("azxxzy", "ay")]
examples_b = [(("deeedbbcccbdaa", 3), "aa"), (("pbbcggttciiippooaais", 2), "ps")]
for s, want in examples_a:
    got = remove_a(s)
    assert got == remove_b(s, 2) == remove_brute(s, 2) == want, (s, got)
    print("(a)", repr(s), "->", repr(got))
for (s, k), want in examples_b:
    got = remove_b(s, k)
    assert got == remove_brute(s, k) == want, (s, k, got)
    print("(b)", (s, k), "->", repr(got))

assert remove_a("") == "" and remove_b("", 3) == ""
assert remove_a("a") == "a" and remove_b("a", 2) == "a"
assert remove_a("aa") == "" and remove_a("aaa") == "a"
assert remove_b("aaaa", 3) == "a"            # a run longer than k leaves a remainder
assert remove_b("aaaaaa", 3) == ""           # two full blocks
assert remove_b("abcd", 2) == "abcd"
assert remove_b("abba", 2) == "" and remove_b("aabbaa", 3) == "aabbaa"
assert remove_b("a" * 100000, 2) == ""       # max size
assert remove_b("ab" * 50000, 2) == "ab" * 50000

rng = random.Random(16)
cases = 0
for _ in range(3000):
    n = rng.randint(0, 14)
    s = "".join(rng.choice("abc") for _ in range(n))
    k = rng.randint(2, 4)
    want = remove_brute(s, k)
    assert remove_b(s, k) == want, (s, k)
    for _ in range(3):                       # any removal order gives the same string
        assert remove_brute(s, k, rng) == want, (s, k)
    if k == 2:
        assert remove_a(s) == want
    cases += 1
print("random cross-check passed:", cases, "cases (3 random removal orders each)")
