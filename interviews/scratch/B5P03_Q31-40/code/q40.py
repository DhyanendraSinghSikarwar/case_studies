import random


def lrs_brute(s):
    """Longest length L such that some substring of length L occurs twice (overlap allowed). O(n^2) per
    length set-building, O(n^3) overall via checking every length from the top."""
    n = len(s)
    for L in range(n - 1, 0, -1):
        seen = set()
        for i in range(n - L + 1):
            w = s[i:i + L]
            if w in seen:
                return L
            seen.add(w)
    return 0


MOD = (1 << 61) - 1          # large prime modulus
BASE = 911382323


def has_repeat(s, L, base=BASE, mod=MOD):
    """Does some substring of length L occur at least twice? Rolling hash, verify on hit."""
    n = len(s)
    if L == 0:
        return True
    top = pow(base, L - 1, mod)
    h = 0
    for k in range(L):
        h = (h * base + ord(s[k])) % mod
    seen = {h: [0]}                           # hash -> starts with that hash
    for i in range(1, n - L + 1):
        h = ((h - ord(s[i - 1]) * top) * base + ord(s[i + L - 1])) % mod
        if h in seen:
            for j in seen[h]:                 # verify real substrings: rules out collisions
                if s[j:j + L] == s[i:i + L]:
                    return True
            seen[h].append(i)
        else:
            seen[h] = [i]
    return False


def lrs(s, base=BASE, mod=MOD):
    lo, hi = 0, len(s) - 1                    # answer is in [0, n-1]; monotone predicate
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if has_repeat(s, mid, base, mod):
            lo = mid
        else:
            hi = mid - 1
    return lo


for s in ["banana", "abcd", "aaaaa", "abcabcabc"]:
    print(s, "->", lrs(s))
assert lrs("banana") == 3 and lrs("abcd") == 0 and lrs("aaaaa") == 4 and lrs("abcabcabc") == 6
assert lrs("aa") == 1 and lrs("ab") == 0 and lrs("abab") == 2
assert lrs("a" * 30000) == 29999
assert lrs("abcdefghijklmnopqrstuvwxyz" * 2) == 26
assert lrs("ab" * 5 + "c") == 8

# worst-case collisions: a tiny modulus forces hash hits, and the verification must keep the answer right
bad = lrs("abcabcabcxyz", base=7, mod=5)
print("with modulus 5 (heavy collisions):", bad, "expected", lrs_brute("abcabcabcxyz"))
assert bad == lrs_brute("abcabcabcxyz")


def lrs_no_verify(s, base=7, mod=5):
    """Deliberately WRONG: trusts the hash. Shows why verification matters."""
    def rep(L):
        h = 0
        hs = set()
        for i in range(len(s) - L + 1):
            h = sum(ord(c) * pow(base, L - 1 - k, mod) for k, c in enumerate(s[i:i + L])) % mod
            if h in hs:
                return True
            hs.add(h)
        return False
    lo, hi = 0, len(s) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if rep(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


print("no verification, modulus 5:", lrs_no_verify("abcdefgh"), "true answer", lrs_brute("abcdefgh"))
assert lrs_no_verify("abcdefgh") != lrs_brute("abcdefgh")

rng = random.Random(40)
for _ in range(1500):
    s = "".join(rng.choice("ab" if rng.random() < 0.5 else "abc") for _ in range(rng.randint(2, 16)))
    assert lrs(s) == lrs_brute(s), s
    assert lrs(s, base=7, mod=11) == lrs_brute(s), s       # tiny modulus: verification keeps it exact
print("random cross-check passed: 1500 cases (default and tiny modulus)")
