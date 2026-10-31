import random, itertools, functools, math
random.seed(43)

# ---- Timsort: count the '<' calls CPython's list.sort makes, by sorting objects that count them
class Cnt:
    n = 0
    __slots__ = ('v',)
    def __init__(self, v): self.v = v
    def __lt__(self, o): Cnt.n += 1; return self.v < o.v
def timsort_cmps(nums):
    Cnt.n = 0; sorted(Cnt(v) for v in nums); return Cnt.n

# ---- plain insertion sort: comparisons a[j-1] > x, element moves
def insertion(nums):
    a = list(nums); cmps = shifts = 0
    for i in range(1, len(a)):
        x = a[i]; j = i
        while j > 0:
            cmps += 1
            if a[j - 1] > x: a[j] = a[j - 1]; shifts += 1; j -= 1
            else: break
        a[j] = x
    assert a == sorted(nums)
    return cmps, shifts

# ---- inversions in O(n log n) by merge counting; (the brute force below is O(n^2))
def inversions(nums):
    a = list(nums)
    def go(lo, hi):
        if hi - lo < 2: return 0
        mid = (lo + hi) // 2; inv = go(lo, mid) + go(mid, hi)
        L, R = a[lo:mid], a[mid:hi]; i = j = 0; k = lo
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: a[k] = L[i]; i += 1
            else: a[k] = R[j]; j += 1; inv += len(L) - i
            k += 1
        a[k:hi] = L[i:] + R[j:]
        return inv
    return go(0, len(a))

# ---- top-down merge sort of Q15: split at n // 2, take from the left on ties (<=), count comparisons
def merge_cmps(nums):
    c = 0
    def sort(x):
        nonlocal c
        if len(x) <= 1: return x
        m = len(x) // 2; L, R = sort(x[:m]), sort(x[m:]); out = []; i = j = 0
        while i < len(L) and j < len(R):
            c += 1
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(list(nums)); return c

def solve(nums):
    ic, sh = insertion(nums)
    return [timsort_cmps(nums), ic, sh, inversions(nums), merge_cmps(nums)]

# ---- examples
ex = {(1, 2, 3, 4, 5): [4, 4, 0, 0, 5], (5, 4, 3, 2, 1): [4, 10, 10, 10, 7], (1, 2, 4, 3, 5, 6): [10, 6, 1, 1, 8],
      (2, 2, 1, 1): [5, 6, 4, 4, 4], (): [0, 0, 0, 0, 0]}
for k, v in ex.items(): assert solve(list(k)) == v, (k, solve(list(k)))
print('examples ok:', [solve(list(k)) for k in ex])

# ---- cross-check: separate counting wrapper (cmp_to_key counts calls of the comparison function) and O(n^2) inversions
def tim_alt(nums):
    c = [0]
    def cmp(x, y): c[0] += 1; return -1 if x < y else (1 if x > y else 0)
    sorted(nums, key=functools.cmp_to_key(cmp)); return c[0]
for _ in range(1500):
    n = random.randint(0, 40); k = random.choice([2, 5, 100])
    t = [random.randint(0, k) for _ in range(n)]
    inv2 = sum(t[i] > t[j] for i in range(n) for j in range(i + 1, n))
    r = solve(t)
    assert r[0] == tim_alt(t) and r[3] == inv2 and r[2] == inv2
print('1500 random lists: Timsort count == cmp_to_key counter, merge-count inversions == O(n^2) count == insertion shifts')

# ---- exhaustive claims for small n (all lists over 0..2, lengths <= 7)
tested = 0
for n in range(0, 8):
    for t in itertools.product(range(3), repeat=n):
        ic, sh = insertion(t); inv = sum(t[i] > t[j] for i in range(n) for j in range(i + 1, n))
        assert sh == inv                                            # each shift removes exactly one inversion
        minima = sum(1 for i in range(1, n) if all(t[p] > t[i] for p in range(i)))   # items that go all the way to the front
        assert ic == inv + (n - 1 if n else 0) - minima             # exact comparison count
        tested += 1
print('shifts == inversions and comparisons == inversions + (n-1) - (strict new prefix minima) for', tested, 'lists')

# ---- Timsort on already sorted / strictly descending lists: n - 1 comparisons (CPython 3.13, observed)
for n in range(1, 300):
    assert timsort_cmps(list(range(n))) == max(n - 1, 0)
    assert timsort_cmps(list(range(n, 0, -1))) == max(n - 1, 0)
print('sorted and strictly descending lists of every length 1..299: exactly n - 1 comparisons')
print('descending with ties [2,2,1,1]:', timsort_cmps([2, 2, 1, 1]), '(not strictly descending, so not one run)')

# ---- n = 300: nearly sorted versus random versus reversed
base = list(range(300))
near = list(base)
for _ in range(5):
    i = random.randrange(299); near[i], near[i + 1] = near[i + 1], near[i]
rnd = random.sample(base, 300)
print('n = 300  (timsort, insertion, shifts, inversions, merge)')
for name, t in (('sorted', base), ('5 adjacent swaps', near), ('reversed', base[::-1]), ('random', rnd)):
    print(f'  {name:17}', solve(t))

# ---- edge asserts
assert solve([7]) == [0, 0, 0, 0, 0]
assert solve([1, 1, 1, 1]) == [3, 3, 0, 0, 4]
assert solve([2, 1]) == [1, 1, 1, 1, 1]
print('edge asserts ok')
