import random
from bisect import bisect_left

def brute(values):                       # oracle: for each value count the distinct smaller values, O(n^2)
    ranks = [1 + len({u for u in values if u < v}) for v in values]
    return [ranks, len(set(values))]

def compress(values):
    uniq = sorted(set(values))           # sort the distinct values once
    rank = {v: i + 1 for i, v in enumerate(uniq)}     # 1-based dense rank
    return [[rank[v] for v in values], len(uniq)]

def compress_bisect(values):             # same with bisect_left on the sorted unique list
    uniq = sorted(set(values))
    return [[bisect_left(uniq, v) + 1 for v in values], len(uniq)]

for vals, want in [([40, -5, 40, 7], [[3, 1, 3, 2], 3]), ([], [[], 0]),
                   ([10**18, -10**18, 0], [[3, 1, 2], 3])]:
    assert compress(vals) == compress_bisect(vals) == brute(vals) == want
    print(vals, '->', compress(vals))

random.seed(17)
for case in range(800):
    vals = [random.randint(-6, 6) for _ in range(random.randint(0, 12))]
    assert compress(vals) == compress_bisect(vals) == brute(vals)
print('800 random cases match the O(n^2) oracle')

# competition ranking ("1224") differs: ties share a rank and the next rank skips
def competition(values):
    s = sorted(values); first = {}
    for i, v in enumerate(s): first.setdefault(v, i + 1)
    return [first[v] for v in values]
assert competition([40, 40, 7, 90]) == [2, 2, 1, 4] and compress([40, 40, 7, 90])[0] == [2, 2, 1, 3]
print('dense', compress([40, 40, 7, 90])[0], 'competition', competition([40, 40, 7, 90]))

# edge cases and size
assert compress([5]) == [[1], 1]
assert compress([2, 2, 2]) == [[1, 1, 1], 1]
assert compress([-1, -2, -3]) == [[3, 2, 1], 3]
big = [random.randint(-10**18, 10**18) for _ in range(10**5)]
r, d = compress(big)
assert d == len(set(big)) and min(r) == 1 and max(r) == d       # ranks fill 1..d with no gaps
print('n = 100000: distinct', d, 'ranks span 1..', max(r))
print('edge asserts ok')
