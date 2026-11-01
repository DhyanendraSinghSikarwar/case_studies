import random
from itertools import accumulate

def brute(nums, queries):
    return [sum(nums[l:r + 1]) for l, r in queries]            # O(n) per query

def optimal(nums, queries):
    pre = [0]                                                  # pre[i] = sum of nums[:i]
    for v in nums:
        pre.append(pre[-1] + v)
    return [pre[r + 1] - pre[l] for l, r in queries]           # O(1) per query

def optimal_accumulate(nums, queries):
    pre = list(accumulate(nums, initial=0))                    # same table, idiom form
    return [pre[r + 1] - pre[l] for l, r in queries]

# examples from the prompt
ex = [([3, -1, 4, 1, -5], [[0, 4], [1, 2], [3, 3], [0, 0]], [2, 3, 1, 3]),
      ([7], [[0, 0]], [7]),
      ([-2, -2, -2], [[0, 2], [1, 2]], [-6, -4])]
for nums, qs, want in ex:
    got = optimal(nums, qs)
    assert got == want == brute(nums, qs) == optimal_accumulate(nums, qs)
    print(nums, qs, '->', got)

# seeded random cross-check
random.seed(1)
cases = 0
for _ in range(500):
    n = random.randint(1, 12)
    nums = [random.randint(-9, 9) for _ in range(n)]
    qs = []
    for _ in range(random.randint(0, 8)):
        l = random.randint(0, n - 1)
        qs.append([l, random.randint(l, n - 1)])
    assert optimal(nums, qs) == brute(nums, qs) == optimal_accumulate(nums, qs)
    cases += 1
print('random cross-check ok:', cases, 'cases')

# exhaustive: every (l, r) on a fixed small array
a = [5, -3, 0, 8, -1, 2]
allq = [[l, r] for l in range(len(a)) for r in range(l, len(a))]
assert optimal(a, allq) == brute(a, allq)
print('all', len(allq), 'ranges of a 6-array ok')

# max size: the sum really exceeds a 32-bit int; Python needs nothing special
big = [10**9] * 10**5
total = optimal(big, [[0, len(big) - 1]])[0]
print('max total', total, '> 2**31-1 =', 2**31 - 1, ' fits int64:', total < 2**63)
assert total == 10**14 > 2**31 - 1
# edge: single element, negative-only
assert optimal([-5], [[0, 0]]) == [-5]
assert optimal([1, 2, 3], []) == []
print('edge asserts ok')
