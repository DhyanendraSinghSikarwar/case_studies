import random
import sys

random.seed(1316)

def quicksort_iter(nums):
    """Lomuto, last element as pivot, explicit stack. depth = most nested partition calls of the recursive version."""
    a = list(nums); cmps = 0; depth = 0
    stack = [(0, len(a) - 1, 1)] if len(a) > 1 else []
    while stack:
        lo, hi, d = stack.pop()
        depth = max(depth, d)
        p, i = a[hi], lo
        for j in range(lo, hi):
            cmps += 1                              # the ONE comparison per item
            if a[j] < p:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]                  # pivot to its final place i
        if i + 1 < hi: stack.append((i + 1, hi, d + 1))   # skip ranges with fewer than 2 items
        if lo < i - 1: stack.append((lo, i - 1, d + 1))
    return [a, cmps, depth]

def brute(nums):
    """Recursive Lomuto (only safe for small inputs)."""
    a = list(nums); cmps = 0; depth = 0
    def rec(lo, hi, d):
        nonlocal cmps, depth
        if lo >= hi: return
        depth = max(depth, d)
        p, i = a[hi], lo
        for j in range(lo, hi):
            cmps += 1
            if a[j] < p:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        rec(lo, i - 1, d + 1); rec(i + 1, hi, d + 1)
    rec(0, len(a) - 1, 1)
    return [a, cmps, depth]

examples = [
    ([3, 1, 2], [[1, 2, 3], 2, 1]),
    ([1, 2, 3, 4], [[1, 2, 3, 4], 6, 3]),
    ([5, 5, 5], [[5, 5, 5], 3, 2]),
    ([4, 2, 7, 1, 9, 3], [[1, 2, 3, 4, 7, 9], 8, 2]),
]
for nums, exp in examples:
    got = quicksort_iter(nums)
    print(nums, '->', got)
    assert got == exp and brute(nums) == exp

# sorted and all-equal input: n(n-1)/2 comparisons, depth n-1
for n in range(1, 40):
    for arr in (list(range(n)), [5] * n):
        r = quicksort_iter(arr)
        assert r[1] == n * (n - 1) // 2 and (r[2] == n - 1 if n > 1 else r[2] == 0)
print('sorted / all-equal: comparisons n(n-1)/2 and depth n-1 verified for n < 40')

# n = 3000: iterative copes, the recursive version hits the default limit (1000)
big = quicksort_iter(list(range(3000)))
assert big[0] == list(range(3000)) and big[1] == 3000 * 2999 // 2 and big[2] == 2999
print('n = 3000 sorted: comparisons', big[1], 'depth', big[2], '| recursion limit', sys.getrecursionlimit())
try:
    brute(list(range(1500)))
    print('recursive n=1500: no error')
except RecursionError:
    print('recursive version, n = 1500: RecursionError')

# random input, n = 3000
rnd = [random.randint(-10 ** 9, 10 ** 9) for _ in range(3000)]
r = quicksort_iter(rnd)
assert r[0] == sorted(rnd)
print('random n = 3000: comparisons', r[1], 'depth', r[2], '(n(n-1)/2 would be', 3000 * 2999 // 2, ')')

# not stable: tag the items and run the same Lomuto on the keys; find an input where equal keys swap order
def lomuto_tagged(items):
    a = list(items)
    def rec(lo, hi):
        if lo >= hi: return
        p, i = a[hi][0], lo
        for j in range(lo, hi):
            if a[j][0] < p:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        rec(lo, i - 1); rec(i + 1, hi)
    rec(0, len(a) - 1)
    return a
import itertools
ex = next([(k, 'abc'[i]) for i, k in enumerate(p)] for p in itertools.product([1, 2], repeat=3)
          if [t for k, t in lomuto_tagged([(k, 'abc'[i]) for i, k in enumerate(p)]) if k == 2]
          != [t for k, t in [(k, 'abc'[i]) for i, k in enumerate(p)] if k == 2])
print('unstable example:', ex, '->', lomuto_tagged(ex))

# seeded random cross-check vs recursive Lomuto and sorted()
for _ in range(400):
    nums = [random.randint(-5, 5) for _ in range(random.randint(1, 40))]
    r = quicksort_iter(nums)
    assert r == brute(nums) and r[0] == sorted(nums)
print('random cross-check ok: 400 cases')

# edge asserts
assert quicksort_iter([7]) == [[7], 0, 0]
assert quicksort_iter([2, 1]) == [[1, 2], 1, 1]
print('edge asserts ok')
