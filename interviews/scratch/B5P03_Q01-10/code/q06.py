import io
import sys
import time


def join_plus(words):
    out = ""
    for i, w in enumerate(words):
        if i:
            out += ", "
        out += w
    return out


def join_list(words):
    return ", ".join(words)


def join_stringio(words):
    buf = io.StringIO()
    for i, w in enumerate(words):
        if i:
            buf.write(", ")
        buf.write(w)
    return buf.getvalue()


def join_prepend(words):                 # out = w + out : never gets the in-place trick
    out = ""
    for w in reversed(words):
        out = w + (", " + out if out else "")
    return out


def join_plus_aliased(words):            # a second reference to the string defeats the trick
    out = ""
    for i, w in enumerate(words):
        if i:
            out += ", "
        out += w
        keep = out                       # second reference to the same str object
    return out


for words, want in [(["ab", "cd", "e"], "ab, cd, e"), ([], ""), (["x"], "x")]:
    for f in (join_plus, join_list, join_stringio, join_prepend, join_plus_aliased):
        assert f(words) == want, (f.__name__, words)
    print(words, "->", repr(want))

assert join_list(["", ""]) == ", "
assert join_plus(["", "a"]) == ", a"

print("python", sys.version.split()[0], sys.implementation.name)
print("sandbox-only timings (seconds), not proof of big-O:")
print("%8s %10s %10s %10s %10s %12s" % ("n", "+=", "join", "StringIO", "w+out", "+= aliased"))
for n in (10000, 20000, 40000, 80000):
    words = ["word%d" % i for i in range(n)]
    row = []
    for f in (join_plus, join_list, join_stringio, join_prepend, join_plus_aliased):
        t = time.perf_counter()
        r = f(words)
        row.append(time.perf_counter() - t)
        assert r == ", ".join(words)
    print("%8d %10.4f %10.4f %10.4f %10.4f %12.4f" % (n, *row))
