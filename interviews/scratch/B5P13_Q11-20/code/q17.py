import random

random.seed(1317)

def count_inversions(nums):
    """Merge sort; when the right item is taken, it beats every item still waiting on the left."""
    a = list(nums)
    buf = [0] * len(a)
    def sort(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        inv = sort(lo, mid) + sort(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if a[i] <= a[j]:                 # tie: take LEFT, equal values are not inversions
                buf[k] = a[i]; i += 1
            else:
                buf[k] = a[j]; j += 1
                inv += mid - i               # everything left in the left half is > a[j]
            k += 1
        while i < mid: buf[k] = a[i]; i += 1; k += 1
        while j < hi: buf[k] = a[j]; j += 1; k += 1
        a[lo:hi] = buf[lo:hi]
        return inv
    return sort(0, len(a))

def brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] > nums[j])

def insertion_shifts(nums):
    a = list(nums); shifts = 0
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0 and a[j] > x:          # strict >: equal items are not shifted
            a[j + 1] = a[j]; j -= 1; shifts += 1
        a[j + 1] = x
    return shifts

examples = [([2, 4, 1, 3, 5], 3), ([5, 4, 3, 2, 1], 10), ([1, 1, 1], 0), ([], 0), ([3, 1, 2, 3, 1], 5)]
for nums, exp in examples:
    got = count_inversions(nums)
    print(nums, '->', got)
    assert got == exp and brute(nums) == exp

# the '<' tie rule would count equal pairs as inversions
def wrong_tie(nums):
    n = len(nums); return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] >= nums[j])
print('counting ties too, [1, 1, 1] would give', wrong_tie([1, 1, 1]))

# max n(n-1)/2 for strictly decreasing input
for n in range(0, 12):
    assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2
print('strictly decreasing input gives n(n-1)/2 for n <= 11')

# inversions == insertion-sort shifts; cross-check against the double loop
for _ in range(400):
    nums = [random.randint(-6, 6) for _ in range(random.randint(0, 25))]
    c = count_inversions(nums)
    assert c == brute(nums) == insertion_shifts(nums)
print('random cross-check ok: 400 cases (merge count == double loop == insertion shifts)')

# maximum size: n = 10^5 (decreasing = worst case, random, all equal)
n = 10 ** 5
assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2
r = [random.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
print('n = 10^5 random:', count_inversions(r), '(about n(n-1)/4 =', n * (n - 1) // 4, ')')
assert count_inversions([7] * n) == 0

# edge asserts
assert count_inversions([1]) == 0 and count_inversions([2, 1]) == 1 and count_inversions([1, 2]) == 0
print('edge asserts ok')
