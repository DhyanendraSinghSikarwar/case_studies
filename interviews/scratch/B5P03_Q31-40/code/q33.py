import re
import time


def one_or_more_a_manual(s):
    """Linear manual check for the language a+ (same language as (a+)+)."""
    if not s:
        return False
    for ch in s:
        if ch != "a":
            return False
    return True


print(bool(re.fullmatch(r"(a+)+", "aaaa")))
print(re.fullmatch(r"(a+)+", "aaab"))
assert re.fullmatch(r"(a+)+", "aaaa") is not None
assert re.fullmatch(r"(a+)+", "aaab") is None
assert one_or_more_a_manual("aaaa") is True
assert one_or_more_a_manual("aaab") is False
assert one_or_more_a_manual("") is False
assert one_or_more_a_manual("b") is False
assert one_or_more_a_manual("a") is True

# same language, safe regex: no nested quantifier
for s in ["", "a", "aaaa", "aaab", "b", "ba", "ab"]:
    assert (re.fullmatch(r"a+", s) is not None) == one_or_more_a_manual(s) == (re.fullmatch(r"(a+)+", s) is not None)

# catastrophic backtracking, SANDBOX-ONLY timings (machine and CPython build dependent)
print("n   regex (a+)+ on a*n+'b'   manual")
prev = None
for n in range(14, 23):
    s = "a" * n + "b"
    t0 = time.perf_counter()
    r = re.fullmatch(r"(a+)+", s)
    t1 = time.perf_counter()
    m = one_or_more_a_manual(s)
    t2 = time.perf_counter()
    assert r is None and m is False
    ratio = "" if prev is None else f"x{(t1 - t0) / prev:.1f}"
    print(f"{n:2d}  {t1 - t0:9.4f}s {ratio:>6}   {t2 - t1:.7f}s")
    prev = t1 - t0
