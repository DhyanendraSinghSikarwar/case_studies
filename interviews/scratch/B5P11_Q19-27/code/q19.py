import random, sys
from functools import lru_cache

random.seed(19)

def min_cuts(s):
    """Palindrome table by expanding around every centre, then cuts[r] over l with pal[l][r]."""
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):          # odd and even centres
            while l >= 0 and r < n and s[l] == s[r]:
                pal[l][r] = True
                l -= 1
                r += 1
    cuts = [0] * n                                    # cuts[r] = min cuts for s[0..r]
    for r in range(n):
        if pal[0][r]:
            cuts[r] = 0
        else:
            cuts[r] = min(cuts[l - 1] + 1 for l in range(1, r + 1) if pal[l][r])
    return cuts[-1]

def min_cuts_light(s):
    """O(n) extra space: no table. cuts[] is relaxed forward from every palindrome found while expanding."""
    n = len(s)
    cuts = list(range(-1, n))                         # cuts[k] = best cuts for the prefix of length k (cuts[0] = -1 sentinel)
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):
            while l >= 0 and r < n and s[l] == s[r]:
                # s[l..r] is a palindrome: the prefix of length r+1 can end with this piece
                if cuts[l] + 1 < cuts[r + 1]:
                    cuts[r + 1] = cuts[l] + 1
                l -= 1
                r += 1
    return cuts[n]

def brute(s):
    """Plain recursion over all cut positions: f(i) = fewest cuts for s[i:]."""
    def f(i):
        if i == len(s):
            return -1                                  # no piece left: the cut after the last piece is not made
        return min(1 + f(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return f(0)

# examples
for s, exp in [('aab', 1), ('a', 0), ('ab', 1), ('aaaa', 0), ('abcbm', 2)]:
    a, b, c = min_cuts(s), min_cuts_light(s), brute(s)
    assert a == b == c == exp, (s, a, b, c)
    print('example', repr(s), '->', a)

# hand table for 'aab'
s = 'aab'; n = len(s)
pal = [[s[l:r + 1] == s[l:r + 1][::-1] if l <= r else None for r in range(n)] for l in range(n)]
print('pal table for aab (rows l, cols r; None below diagonal):')
for l in range(n):
    print('  l=%d' % l, [('T' if v else 'F') if v is not None else '.' for v in pal[l]])
cuts = []
for r in range(n):
    if pal[0][r]:
        cuts.append(0); print('  r=%d pal[0][%d] is True -> cuts=0' % (r, r))
    else:
        cands = [(l, cuts[l - 1] + 1) for l in range(1, r + 1) if pal[l][r]]
        cuts.append(min(v for _, v in cands)); print('  r=%d candidates (l, cuts[l-1]+1) %s -> cuts=%d' % (r, cands, cuts[-1]))
print('cuts =', cuts)

# seeded cross-check: len <= 10, small alphabets so palindromes occur
cases = 0; hist = {}
for _ in range(600):
    alpha = random.choice(['ab', 'abc', 'a', 'abcd'])
    s = ''.join(random.choice(alpha) for _ in range(random.randint(1, 10)))
    exp = brute(s)
    assert min_cuts(s) == min_cuts_light(s) == exp, s
    cases += 1; hist[exp] = hist.get(exp, 0) + 1
print('cross-check cases', cases, '| answer histogram', dict(sorted(hist.items())))
# exhaustive over all binary strings up to length 10
cnt = 0
for L in range(1, 11):
    for bits in range(1 << L):
        s = format(bits, '0%db' % L)
        assert min_cuts(s) == min_cuts_light(s) == brute(s); cnt += 1
print('exhaustive binary strings len 1..10:', cnt)

# edge cases
assert min_cuts('a' * 2000) == 0
assert min_cuts('ab' * 50) == 1 == min_cuts_light('ab' * 50)   # 'a' + 'bab...ab' (the rest is a palindrome)
assert min_cuts('abcdefghij' * 5) == 49     # no palindrome longer than 1: every letter is its own piece
assert min_cuts_light('abcdefghij' * 5) == 49
assert min_cuts('a') == 0 == min_cuts_light('a')
print('edge asserts passed')

# memory of the table at n = 2000
n = 2000
tbl = [[False] * n for _ in range(n)]
outer = sys.getsizeof(tbl); rows = sum(sys.getsizeof(r) for r in tbl)
print('list-of-lists 2000x2000: rows', rows, 'bytes + outer', outer, '= about %.1f MB' % ((rows + outer) / 1e6))
tb = [bytearray(n) for _ in range(n)]
print('list of bytearrays 2000x2000: about %.1f MB' % ((sum(sys.getsizeof(r) for r in tb) + sys.getsizeof(tb)) / 1e6))
tri = [bytearray(n - l) for l in range(n)]
print('upper triangle only (l <= r): about %.1f MB' % (sum(sys.getsizeof(r) for r in tri) / 1e6))
import time
t0 = time.perf_counter(); r1 = min_cuts('ab' * 1000); t1 = time.perf_counter(); r2 = min_cuts_light('ab' * 1000); t2 = time.perf_counter()
print('n=2000 "ab"*1000 (sandbox timing): table version', r1, round(t1 - t0, 2), 's; light version', r2, round(t2 - t1, 2), 's')
import random as _r
_r.seed(5); w = ''.join(_r.choice('ab') for _ in range(2000))
t0 = time.perf_counter(); r1 = min_cuts(w); t1 = time.perf_counter(); r2 = min_cuts_light(w); t2 = time.perf_counter()
assert r1 == r2
print('n=2000 random binary (sandbox timing):', r1, round(t1 - t0, 2), 's;', round(t2 - t1, 2), 's')

# recursion: a memoised f(i) on a string with no palindrome longer than 1 nests n deep (observed on this Python, default limit)
def memo_cuts(s):
    @lru_cache(maxsize=None)
    def f(i):
        if i == len(s):
            return -1
        return min(1 + f(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return f(0)
print('recursion limit', sys.getrecursionlimit())
for n in (300, 2000):
    w = ('abc' * n)[:n]
    try:
        print('memoised recursion, n =', n, '->', memo_cuts(w), '(bottom-up gives', min_cuts_light(w), ')')
    except RecursionError:
        print('memoised recursion, n =', n, '-> RecursionError (bottom-up gives', min_cuts_light(w), ')')
