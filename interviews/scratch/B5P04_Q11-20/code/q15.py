import itertools


def build_brute(s):
    # reference: apply the keystrokes to a text, '#' deletes the last char if there is one
    out = ""
    for c in s:
        out = out[:-1] if c == "#" else out + c
    return out


def same_brute(s, t):
    return build_brute(s) == build_brute(t)


def build_stack(s):
    st = []
    for c in s:
        if c != "#":
            st.append(c)
        elif st:                 # '#' on an empty text does nothing
            st.pop()
    return st


def same_stack(s, t):
    return build_stack(s) == build_stack(t)


def next_valid(s, i):
    """Index of the next surviving character at or left of i (or -1), skipping deleted ones."""
    skip = 0
    while i >= 0:
        if s[i] == "#":
            skip += 1
        elif skip:
            skip -= 1            # this character is deleted by a pending '#'
        else:
            return i
        i -= 1
    return -1


def same_two_pointer(s, t):
    i, j = len(s) - 1, len(t) - 1
    while True:
        i, j = next_valid(s, i), next_valid(t, j)
        if i < 0 and j < 0:
            return True          # both exhausted together
        if i < 0 or j < 0 or s[i] != t[j]:
            return False
        i -= 1
        j -= 1


examples = [(("ab#c", "ad#c"), True), (("ab##", "c#d#"), True), (("a#c", "b"), False), (("a##c", "#a#c"), True)]
for (s, t), want in examples:
    got = same_stack(s, t)
    assert got == same_two_pointer(s, t) == same_brute(s, t) == want, (s, t)
    print((s, t), "->", got)

assert same_stack("", "") and same_two_pointer("", "")
assert same_stack("#", "") and same_two_pointer("#", "")          # '#' on empty text
assert same_stack("###", "") and same_two_pointer("###", "")
assert not same_stack("a", "") and not same_two_pointer("a", "")
assert same_stack("a#", "#") and same_two_pointer("a#", "#")
assert not same_stack("ab", "a") and not same_two_pointer("ab", "a")
assert same_stack("a" * 200, "a" * 200) and same_two_pointer("a" * 200, "a" * 200)
assert same_two_pointer("a" * 100 + "#" * 100, "")

# exhaustive over alphabet 'ab#', every string up to length 5 (364 strings, all pairs)
strings = [""]
for n in range(1, 6):
    strings += ["".join(p) for p in itertools.product("ab#", repeat=n)]
pairs = 0
for s in strings:
    for t in strings:
        want = same_brute(s, t)
        assert same_stack(s, t) == want and same_two_pointer(s, t) == want, (s, t)
        pairs += 1
print("exhaustive cross-check passed:", len(strings), "strings,", pairs, "pairs")
