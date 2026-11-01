import random

random.seed(36)

def quickselect_rounds(nums, k):
    """k-th largest by first-element pivot and three-way partition. Returns [value, rounds]."""
    seg = list(nums)
    rounds = 0
    while True:
        p = seg[0]
        rounds += 1
        gt = [x for x in seg if x > p]
        eq = [x for x in seg if x == p]
        lt = [x for x in seg if x < p]
        if k <= len(gt):
            seg = gt
        elif k <= len(gt) + len(eq):
            return [p, rounds]
        else:
            k -= len(gt) + len(eq)
            seg = lt

def kth_brute(nums, k):
    return sorted(nums, reverse=True)[k - 1]

def two_way_rounds(nums, k, equals_go_small):
    """Two-way partition with the first element as pivot: only 'big' and 'small' lists, so equal keys cannot be
    finished off together. Equals go to the small side (or the big side). Returns [value, rounds]."""
    seg, rounds = list(nums), 0
    while True:
        p, rest = seg[0], seg[1:]
        rounds += 1
        if equals_go_small:
            big = [x for x in rest if x > p]; small = [x for x in rest if x <= p]
        else:
            big = [x for x in rest if x >= p]; small = [x for x in rest if x < p]
        if k == len(big) + 1:
            return [p, rounds]
        if k <= len(big):
            seg = big
        else:
            k -= len(big) + 1; seg = small

def quickselect_random(nums, k, rng):
    """Same scheme with a random pivot; returns [value, rounds]."""
    seg = list(nums)
    rounds = 0
    while True:
        p = seg[rng.randrange(len(seg))]
        rounds += 1
        gt = [x for x in seg if x > p]
        eq = [x for x in seg if x == p]
        lt = [x for x in seg if x < p]
        if k <= len(gt):
            seg = gt
        elif k <= len(gt) + len(eq):
            return [p, rounds]
        else:
            k -= len(gt) + len(eq)
            seg = lt

# ---- examples
for nums, k, want in [([3, 2, 1, 5, 6, 4], 2, [5, 2]), ([5, 5, 5, 5], 3, [5, 1]),
                      ([1, 2, 3, 4, 5], 1, [5, 5]), ([9], 1, [9, 1])]:
    got = quickselect_rounds(nums, k)
    assert got == want, (nums, k, got, want)
    print(nums, k, '->', got)

# ---- seeded cross-check against sorting (heavy duplicates)
for _ in range(2000):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 12))]
    k = random.randint(1, len(nums))
    v, r = quickselect_rounds(nums, k)
    assert v == kth_brute(nums, k) and 1 <= r <= len(nums), (nums, k)
    assert quickselect_random(nums, k, random.Random(1))[0] == v
print('2000 random lists agree with sorted()')

# ---- the claims
for n in (1, 5, 50, 500, 5000):
    assert quickselect_rounds([7] * n, max(1, n // 2)) == [7, 1]          # all equal: 1 round, any n
n = 3000
for k in (1, n // 2, n):
    assert quickselect_rounds([7] * n, k)[1] == 1
print('all-equal n=3000: three-way rounds for k=1, n/2, n:', [quickselect_rounds([7] * n, k)[1] for k in (1, n // 2, n)])
print('two-way (equals to small side) rounds for k=1, n/2, n:', [two_way_rounds([7] * n, k, True)[1] for k in (1, n // 2, n)])
print('two-way (equals to big side) rounds for k=1, n/2, n:  ', [two_way_rounds([7] * n, k, False)[1] for k in (1, n // 2, n)])
for _ in range(500):   # two-way version is still correct, just not duplicate-proof
    nums = [random.randint(0, 4) for _ in range(random.randint(1, 10))]; k = random.randint(1, len(nums))
    assert two_way_rounds(nums, k, True)[0] == two_way_rounds(nums, k, False)[0] == kth_brute(nums, k)
print('all-equal input: three-way always 1 round for any n and k')
for n in (1, 5, 50, 500, 2000):
    assert quickselect_rounds(list(range(1, n + 1)), 1) == [n, n]         # ascending, k=1: n rounds
print('ascending, k=1: rounds == n for n = 1..2000')

n = 2000
asc = list(range(1, n + 1))
rng = random.Random(7)
rounds_random = [quickselect_random(asc, 1, rng)[1] for _ in range(200)]
print('n=2000 ascending, k=1: first-element pivot rounds =', quickselect_rounds(asc, 1)[1],
      '| random pivot rounds avg =', round(sum(rounds_random) / 200, 1), 'max =', max(rounds_random))

# n = 10^5 random data: first-element pivot is fine on random input
data = [random.randint(0, 10 ** 9) for _ in range(10 ** 5)]
v, r = quickselect_rounds(data, 10 ** 5 // 2)
assert v == kth_brute(data, 10 ** 5 // 2)
print('n=1e5 random values, median: rounds =', r, '(round count only; no timing claim)')
