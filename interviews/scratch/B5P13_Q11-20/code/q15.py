import itertools
import math
import random

random.seed(1315)

def merge_sort(records):
    """Top-down, split at n // 2, one comparison left.key <= right.key per taken item while both halves have items."""
    cmps = 0
    def sort(a):
        nonlocal cmps
        n = len(a)
        if n <= 1:
            return a
        mid = n // 2
        left, right = sort(a[:mid]), sort(a[mid:])
        out, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            cmps += 1
            if left[i][0] <= right[j][0]:          # <= takes the LEFT item on ties: that is stability
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        out.extend(left[i:]); out.extend(right[j:])   # leftovers: no comparisons
        return out
    res = sort([list(r) for r in records])
    return [res, cmps]

def brute(records):
    """Reference: sorted() for the order (stable) and a separate recursive counter over index ranges."""
    recs = [list(r) for r in records]
    def go(lo, hi):
        if hi - lo <= 1:
            return recs[lo:hi], 0
        mid = lo + (hi - lo) // 2
        (L, a), (R, b) = go(lo, mid), go(mid, hi)
        c, out = a + b, []
        while L and R:
            c += 1
            out.append(L.pop(0) if L[0][0] <= R[0][0] else R.pop(0))
        return out + L + R, c
    _, c = go(0, len(recs))
    return [sorted(recs, key=lambda r: r[0]), c]

def bottom_up_cmps(keys):
    """Bottom-up (width 1, 2, 4, ...): no recursion, but a different split, so the count can differ."""
    a = [[k, 0] for k in keys]; width = 1; cmps = 0
    while width < len(a):
        nxt = []
        for lo in range(0, len(a), 2 * width):
            L, R = a[lo:lo + width], a[lo + width:lo + 2 * width]
            i = j = 0
            while i < len(L) and j < len(R):
                cmps += 1
                if L[i][0] <= R[j][0]: nxt.append(L[i]); i += 1
                else: nxt.append(R[j]); j += 1
            nxt.extend(L[i:]); nxt.extend(R[j:])
        a, width = nxt, width * 2
    return cmps

examples = [
    ([[3, 1], [1, 2], [3, 3], [2, 4], [1, 5]], [[[1, 2], [1, 5], [2, 4], [3, 1], [3, 3]], 8]),
    ([], [[], 0]),
    ([[9, 0]], [[[9, 0]], 0]),
    ([[1, 1], [2, 2], [3, 3], [4, 4]], [[[1, 1], [2, 2], [3, 3], [4, 4]], 4]),
]
for rec, exp in examples:
    got = merge_sort(rec)
    print(rec, '->', got)
    assert got == exp and brute(rec) == exp

# worst case n*ceil(log2 n) - 2^ceil(log2 n) + 1, exhaustive over all permutations for n <= 8; by hand n = 5: 5*3 - 8 + 1 = 8
for n in range(1, 9):
    worst = max(merge_sort([[v, 0] for v in p])[1] for p in itertools.permutations(range(n)))
    c = math.ceil(math.log2(n))
    assert worst == n * c - 2 ** c + 1, (n, worst)
    print('n =', n, 'worst comparisons over all', math.factorial(n), 'permutations =', worst, '= formula', n * c - 2 ** c + 1)

# bottom-up can differ from top-down (n = 3 sorted input: top-down splits 1|2, bottom-up merges 2 then 1)
diff = [(p, merge_sort([[v, 0] for v in p])[1], bottom_up_cmps(p))
        for n in range(2, 7) for p in itertools.permutations(range(n)) if merge_sort([[v, 0] for v in p])[1] != bottom_up_cmps(p)]
print('bottom-up differs from top-down for', len(diff), 'permutations with n <= 6; first:', diff[0])
assert diff

# the '<' variant is unstable: equal keys come out reversed
def merge_lt(a, b):
    out = []
    while a and b:
        out.append(a.pop(0) if a[0][0] < b[0][0] else b.pop(0))
    return out + a + b
print('with < the two 5s come out as', [r[1] for r in merge_lt([[5, 'first']], [[5, 'second']])])
assert [r[1] for r in merge_lt([[5, 'first']], [[5, 'second']])] == ['second', 'first']

# seeded random cross-check (order AND count vs the separate counter)
for _ in range(400):
    rec = [[random.randint(0, 4), random.randint(0, 9)] for _ in range(random.randint(0, 30))]
    assert merge_sort(rec) == brute(rec)
print('random cross-check ok: 400 cases')

# maximum size: n = 10^5, comparisons <= n * ceil(log2 n)
rec = [[random.randint(-10 ** 9, 10 ** 9), i] for i in range(10 ** 5)]
out, c = merge_sort(rec)
assert out == sorted(rec, key=lambda r: r[0]) and c <= 10 ** 5 * math.ceil(math.log2(10 ** 5))
print('n = 10^5: ok, comparisons', c, '<= n*ceil(log2 n) =', 10 ** 5 * 17)

# edge asserts
assert merge_sort([[2, 0], [2, 1], [2, 2]]) == [[[2, 0], [2, 1], [2, 2]], 2]   # all equal: input order kept; split 1|2 costs 1 + 1
assert merge_sort([[1, 0], [2, 1]])[1] == 1
print('edge asserts ok')
