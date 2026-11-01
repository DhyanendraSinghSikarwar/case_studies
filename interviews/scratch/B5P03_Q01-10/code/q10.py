import random
from itertools import groupby


def compress_brute(chars):
    out = []
    for ch, grp in groupby(chars):
        k = len(list(grp))
        out.append(ch)
        if k > 1:
            out.extend(str(k))
    return out


def compress_inplace(chars):
    n = len(chars)
    write = read = 0
    while read < n:
        ch = chars[read]
        start = read
        while read < n and chars[read] == ch:      # read pointer jumps to the end of the run
            read += 1
        chars[write] = ch
        write += 1
        if read - start > 1:
            for d in str(read - start):            # digits of the run length, as characters
                chars[write] = d
                write += 1
        assert write <= read                       # the invariant, checked at run time
    return write


def run(chars):
    c = list(chars)
    k = compress_inplace(c)
    return k, c[:k]


examples = [(list("aabbccc"), 6, list("a2b2c3")), (["a"], 1, ["a"]),
            (list("a" + "b" * 12), 4, list("ab12"))]
for chars, wk, wp in examples:
    k, pre = run(chars)
    assert (k, pre) == (wk, wp) == (len(compress_brute(chars)), compress_brute(chars)), (chars, k, pre)
    print("k =", k, "prefix", pre)

assert run([]) == (0, [])
assert run(list("abc")) == (3, list("abc"))            # all runs of length 1: no digits
assert run(list("a" * 9)) == (2, list("a9"))
assert run(list("a" * 10)) == (3, list("a10"))
assert run(list("a" * 100)) == (4, list("a100"))
assert run(list("a" * 2000)) == (5, list("a2000"))
assert run(list("aab")) == (3, list("a2b"))
assert run(list("abba")) == (4, list("ab2a"))          # non-adjacent same letters stay separate

rng = random.Random(8)
cases = 0
for _ in range(4000):
    chars = []
    for _ in range(rng.randint(0, 6)):
        chars += [rng.choice("abc")] * rng.choice([1, 1, 2, 3, 9, 10, 11, 25])
    k, pre = run(chars)
    assert pre == compress_brute(chars) and k == len(pre), chars
    cases += 1
print("random cross-check passed:", cases, "cases")
