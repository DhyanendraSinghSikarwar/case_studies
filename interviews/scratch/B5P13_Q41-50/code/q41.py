import random, itertools
random.seed(41)

# ---- the exact partition from the question (pivot = a[lo], returns the new array and j)
def hoare(nums):
    a = list(nums); p = a[0]; i, j = -1, len(a)
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: return [a, j]
        a[i], a[j] = a[j], a[i]

# ---- the examples
assert hoare([5, 3, 8, 1, 9, 2]) == [[2, 3, 1, 8, 9, 5], 2]
assert hoare([2, 1]) == [[1, 2], 0]
assert hoare([1, 2]) == [[1, 2], 0]
assert hoare([4, 4, 4, 4]) == [[4, 4, 4, 4], 1]
print('examples ok:', hoare([5, 3, 8, 1, 9, 2]), hoare([2, 1]), hoare([1, 2]), hoare([4, 4, 4, 4]))

def guarantees(orig, a, j):
    p = orig[0]
    return (sorted(a) == sorted(orig) and 0 <= j < len(a) - 1
            and all(x <= p for x in a[:j + 1]) and all(x >= p for x in a[j + 1:]))

# ---- exhaustive check: every array of length 2..7 over values 0..3 (and 0..4 for length <= 5)
cnt = 0
for n in range(2, 8):
    for t in itertools.product(range(4 if n > 5 else 5), repeat=n):
        a, j = hoare(t)
        assert guarantees(t, a, j), t
        cnt += 1
print('guarantees hold for', cnt, 'arrays (all arrays of length 2..7 over small value sets)')

# ---- seeded random cross-check against the while-True version (same i/j walk, different loop shape)
def hoare_alt(nums):
    a = list(nums); p = a[0]; i, j = 0, len(a) - 1
    while True:
        while a[i] < p: i += 1
        while a[j] > p: j -= 1
        if i >= j: return [a, j]
        a[i], a[j] = a[j], a[i]
        i += 1; j -= 1
for _ in range(2000):
    t = [random.randint(-5, 5) for _ in range(random.randint(2, 50))]
    assert hoare(t) == hoare_alt(t)
    a, j = hoare(t); assert guarantees(t, a, j)
print('2000 random arrays: both loop shapes agree and the guarantees hold')

# ---- recursion on [lo, j] and [j+1, hi] sorts; j-1 / j+1 (Lomuto style) does not
def part_range(a, lo, hi, pivot_index):
    p = a[pivot_index]; i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: return j
        a[i], a[j] = a[j], a[i]
def qs(a, lo, hi, wrong=False, depth=0):
    if depth > 200: raise RecursionError('no progress')
    if lo >= hi: return
    j = part_range(a, lo, hi, lo)
    if wrong: qs(a, lo, j - 1, True, depth + 1); qs(a, j + 1, hi, True, depth + 1)
    else: qs(a, lo, j, False, depth + 1); qs(a, j + 1, hi, False, depth + 1)
for _ in range(500):
    t = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
    a = list(t); qs(a, 0, len(a) - 1); assert a == sorted(t)
bad = 0
for _ in range(500):
    t = [random.randint(0, 9) for _ in range(random.randint(2, 12))]
    a = list(t); qs(a, 0, len(a) - 1, wrong=True); bad += a != sorted(t)
print('recursing on [lo, j] and [j+1, hi]: 500/500 sorted; on [lo, j-1] and [j+1, hi]:', bad, '/ 500 left unsorted')

# ---- last element as pivot with the same loop: j can be len-1, so [lo, j] is the whole range
a = [1, 2]; j = part_range(a, 0, 1, 1)
print('pivot = last element, [1, 2] -> j =', j, '(= len - 1, so recursing on [0, j] never shrinks)')
try:
    b = [1, 2, 3]
    def qs_last(a, lo, hi, depth=0):
        if depth > 50: raise RecursionError('stuck: same range again and again')
        if lo >= hi: return
        j = part_range(a, lo, hi, hi); qs_last(a, lo, j, depth + 1); qs_last(a, j + 1, hi, depth + 1)
    qs_last(b, 0, 2)
except RecursionError as e: print('last-element pivot quicksort:', e)
# count how often the last-element pivot can return len-1 on small arrays
hits = sum(1 for t in itertools.product(range(3), repeat=4) if (lambda a: part_range(a, 0, 3, 3))(list(t)) == 3)
print('last-element pivot returned j = n-1 for', hits, 'of 81 arrays of length 4 over {0,1,2}')

# ---- equal keys: both pointers stop on equal keys, so j lands in the middle; Lomuto (last pivot) would give n-1
for n in (8, 100):
    a, j = hoare([7] * n); print('all equal, n =', n, '-> j =', j, '(middle); Lomuto with all equal puts the pivot at', n - 1)
swaps = []
for n in (8, 100):
    a = [7] * n; p = a[0]; i, j, s = -1, n, 0
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: break
        a[i], a[j] = a[j], a[i]; s += 1
    swaps.append(s)
print('swaps on all-equal input of size 8 and 100:', swaps, '(useless swaps, but the split is balanced)')

# ---- edge asserts
assert hoare([3, 3]) == [[3, 3], 0]
assert hoare([9, 1]) == [[1, 9], 0]
assert hoare([1, 9, 1]) == [[1, 9, 1], 0]
assert hoare([2, 2, 1]) == [[1, 2, 2], 1]
print('edge asserts ok')
