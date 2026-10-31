import random, itertools, sys
random.seed(42)

# ---- optimal: both quicksorts iterative (explicit stack of ranges), with comparison counters
def lomuto_iter(nums):
    a = list(nums); cmps = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi: continue
        p = a[hi]; i = lo
        for j in range(lo, hi):
            cmps += 1                                  # one test a[j] < p
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]                      # pivot to its final index i
        stack.append((lo, i - 1)); stack.append((i + 1, hi))
    return a, cmps

def three_way_iter(nums):
    a = list(nums); cmps = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if hi - lo < 1: continue                       # fewer than 2 items
        p = a[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            cmps += 1                                  # ONE comparison, three outcomes (<, >, ==)
            if a[i] < p: a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > p: a[i], a[gt] = a[gt], a[i]; gt -= 1
            else: i += 1
        stack.append((lo, lt - 1)); stack.append((gt + 1, hi))   # the block [lt..gt] == p is never touched again
    return a, cmps

def solve(nums):
    s, cl = lomuto_iter(nums); s3, c3 = three_way_iter(nums)
    assert s == s3
    return [s, cl, c3]

# ---- recursive versions, written separately, as the cross-check
def rec_versions(nums):
    c = [0, 0]; a = list(nums); b = list(nums)
    def rl(lo, hi):
        if lo >= hi: return
        p = a[hi]; i = lo
        for j in range(lo, hi):
            c[0] += 1
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]; rl(lo, i - 1); rl(i + 1, hi)
    def r3(lo, hi):
        if hi - lo < 1: return
        p = b[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            c[1] += 1
            if b[i] < p: b[lt], b[i] = b[i], b[lt]; lt += 1; i += 1
            elif b[i] > p: b[i], b[gt] = b[gt], b[i]; gt -= 1
            else: i += 1
        r3(lo, lt - 1); r3(gt + 1, hi)
    rl(0, len(a) - 1); r3(0, len(b) - 1)
    assert a == b == sorted(nums)
    return [a, c[0], c[1]]

# ---- examples
assert solve([2, 2, 2, 2]) == [[2, 2, 2, 2], 6, 4]
assert solve([3, 1, 2, 3, 1]) == [[1, 1, 2, 3, 3], 8, 8]
assert solve([1, 2, 3, 4, 5]) == [[1, 2, 3, 4, 5], 10, 14]
print('examples ok:', solve([2, 2, 2, 2]), solve([3, 1, 2, 3, 1]), solve([1, 2, 3, 4, 5]))

# ---- seeded random cross-check (small value ranges give many repeats)
for _ in range(3000):
    n = random.randint(1, 30); k = random.choice([1, 2, 3, 5, 50])
    t = [random.randint(0, k) for _ in range(n)]
    assert solve(t) == rec_versions(t) and solve(t)[0] == sorted(t)
print('3000 random inputs: iterative == recursive (sorted list and both counters)')

# ---- exact claims, checked
for n in (1, 2, 3, 10, 57, 2000):
    s, cl, c3 = solve([7] * n)
    assert cl == n * (n - 1) // 2 and c3 == (n if n >= 2 else 0)
print('all equal, n = 2000: Lomuto', solve([7] * 2000)[1], '= n(n-1)/2 ; three-way', solve([7] * 2000)[2], '= n')
# sorted input is bad for Lomuto (last element = maximum) and fine-ish for three-way only by luck of the pivot rule
print('sorted 1..2000: Lomuto', solve(list(range(2000)))[1], ' three-way', solve(list(range(2000)))[2])
d = [random.randint(0, 9) for _ in range(2000)]
print('2000 random items from 10 distinct values: Lomuto', solve(d)[1], ' three-way', solve(d)[2])

# ---- why iterative: the recursive Lomuto on all-equal input of size n is about n frames deep
try:
    rec_versions([7] * 1500)
except RecursionError:
    print('recursive version on 1500 equal items: RecursionError (limit', sys.getrecursionlimit(), ')')
print('iterative version on 2000 equal items worked (no recursion at all)')

# ---- edge asserts
assert solve([]) == [[], 0, 0]
assert solve([5]) == [[5], 0, 0]
assert solve([2, 1]) == [[1, 2], 1, 2]
assert solve([1, 1, 1, 2, 2, 2]) [0] == [1, 1, 1, 2, 2, 2]
assert solve([-3, -3, 0, -3])[0] == [-3, -3, -3, 0]
print('edge asserts ok')
