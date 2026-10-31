import posixpath
import random
import re


def simplify_rewrite(path):
    # reference: rewrite the string until nothing changes (independent of the stack idea)
    s = path if path.endswith("/") else path + "/"
    while True:
        t = s
        t = re.sub(r"/+", "/", t)                        # collapse repeated slashes
        t = t.replace("/./", "/")                        # drop '.'
        t = re.sub(r"^/(\.\./)+", "/", t)                # '..' at the root stays at the root
        t = re.sub(r"/(?!\.\.?/)[^/]+/\.\./", "/", t, count=1)      # name/.. cancels (name is not '.' or '..')
        if t == s:
            break
        s = t
    return s[:-1] if len(s) > 1 else s


def simplify_stack(path):
    stack = []
    for name in path.split("/"):
        if name in ("", "."):
            continue                                     # empty (from '//' or edges) and '.' do nothing
        if name == "..":
            if stack:
                stack.pop()                              # go up one level; at the root do nothing
        else:
            stack.append(name)                           # includes '...' and 'a.b'
    return "/" + "/".join(stack)


examples = [("/home/", "/home"), ("/home//foo/", "/home/foo"), ("/a/./b/../../c/", "/c"),
            ("/../", "/"), ("/.../a/../b/c/../d/./", "/.../b/d")]
for p, want in examples:
    assert simplify_stack(p) == simplify_rewrite(p) == want, (p, simplify_stack(p), simplify_rewrite(p))
    print(repr(p), "->", repr(simplify_stack(p)))

# edge cases
assert simplify_stack("/") == "/"
assert simplify_stack("////") == "/"
assert simplify_stack("/..") == "/" and simplify_stack("/../..") == "/"
assert simplify_stack("/a/..") == "/"                    # back to root, no trailing slash
assert simplify_stack("/...") == "/..."                  # three dots is a name
assert simplify_stack("/a.b/c_d/../e") == "/a.b/e"
assert simplify_stack("/" + "a/" * 1500) == "/" + "/".join(["a"] * 1500)   # about 3000 characters

# a Python-library trap: normpath keeps a leading double slash on POSIX
print("posixpath.normpath('//a') =", posixpath.normpath("//a"), "  but expected '/a':", simplify_stack("//a"))
assert posixpath.normpath("//a") == "//a" and simplify_stack("//a") == "/a"

# seeded randomised cross-check
rng = random.Random(4)
pieces = ["a", "b", "ab", ".", "..", "...", "", ""]
for _ in range(3000):
    path = "/" + "/".join(rng.choice(pieces) for _ in range(rng.randint(0, 8)))
    assert simplify_stack(path) == simplify_rewrite(path), (path, simplify_stack(path), simplify_rewrite(path))
print("random cross-check passed: 3000 paths")
