import random
import time


def str_str(h, nd):
    if nd == "":
        return 0
    n, m = len(h), len(nd)
    for i in range(n - m + 1):
        j = 0
        while j < m and h[i + j] == nd[j]:
            j += 1
        if j == m:
            return i
    return -1


def str_str_counted(h, nd):
    # same loop, but counts character comparisons so we can see the O(n*m) blow-up
    n, m, cmp_ = len(h), len(nd), 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            cmp_ += 1
            if h[i + j] != nd[j]:
                break
            j += 1
        if j == m:
            return i, cmp_
    return -1, cmp_


examples = [("sadbutsad", "sad", 0), ("leetcode", "leeto", -1),
            ("mississippi", "issip", 4), ("abc", "", 0)]
for h, nd, want in examples:
    assert str_str(h, nd) == h.find(nd) == want, (h, nd)
    print((h, nd), "->", want)

assert str_str("a", "a") == 0
assert str_str("a", "b") == -1
assert str_str("abc", "abcd") == -1        # needle longer than haystack
assert str_str("aaa", "aaaa") == -1
assert str_str("", "") == 0 and str_str("", "a") == -1
assert str_str("abcabd", "abd") == 3

# adversarial input: every window matches almost to the end, then fails on the last char
n, m = 10000, 5001
h, nd = "a" * n, "a" * (m - 1) + "b"
res, comps = str_str_counted(h, nd)
print("adversarial: result", res, "| comparisons", comps, "| (n-m+1)*m =", (n - m + 1) * m)
assert res == -1 and comps == (n - m + 1) * m

t = time.perf_counter(); r1 = h.find(nd); t_find = time.perf_counter() - t
t = time.perf_counter(); r2 = str_str(h, nd); t_naive = time.perf_counter() - t
assert r1 == r2 == -1
print("sandbox-only timing: str.find %.5f s, naive Python loop %.2f s" % (t_find, t_naive))

rng = random.Random(7)
cases = 0
for _ in range(5000):
    h = "".join(rng.choice("ab") for _ in range(rng.randint(0, 10)))
    nd = "".join(rng.choice("ab") for _ in range(rng.randint(0, 4)))
    assert str_str(h, nd) == h.find(nd), (h, nd)
    cases += 1
print("random cross-check passed:", cases, "cases")
