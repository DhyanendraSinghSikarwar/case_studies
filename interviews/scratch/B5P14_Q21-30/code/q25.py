import random

def optimal(nums):
    """Fenwick tree over compressed ranks. Returns [total, before_greater]."""
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}   # coordinate compression to 1..m
    m = len(ranks)
    tree = [0] * (m + 1)
    before = []
    for j, v in enumerate(nums):
        r = ranks[v]
        cnt, i = 0, r
        while i > 0:                                       # prefix_count(r): earlier elements with rank <= r
            cnt += tree[i]; i -= i & -i
        before.append(j - cnt)                             # earlier elements strictly greater
        i = r
        while i <= m:                                      # insert rank r
            tree[i] += 1; i += i & -i
    return [sum(before), before]

def brute(nums):
    before = [sum(1 for i in range(j) if nums[i] > nums[j]) for j in range(len(nums))]
    return [sum(before), before]

def at_most_variant(nums):
    """Pairs i < j with nums[i] >= nums[j] ('at most' side of the comparison): use prefix_count(rank - 1)."""
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(ranks); tree = [0] * (m + 1); total = 0
    for j, v in enumerate(nums):
        r = ranks[v]; cnt, i = 0, r - 1                    # strictly smaller earlier elements
        while i > 0: cnt += tree[i]; i -= i & -i
        total += j - cnt                                   # earlier elements >= v
        i = r
        while i <= m: tree[i] += 1; i += i & -i
    return total

assert optimal([3, 1, 2, 3, 1]) == [5, [0, 1, 1, 0, 3]]
assert optimal([]) == [0, []]
assert optimal([2, 2, 2]) == [0, [0, 0, 0]]
print('examples:', optimal([3, 1, 2, 3, 1]), optimal([]), optimal([2, 2, 2]))

# dry run of the Fenwick loops on the first example ranks: values 1,2,3 -> ranks 1,2,3
print('ranks:', {v: i + 1 for i, v in enumerate(sorted(set([3, 1, 2, 3, 1])))})

# edge cases
assert optimal([5]) == [0, [0]]
assert optimal([3, 2, 1]) == [3, [0, 1, 2]]                # strictly decreasing: n(n-1)/2
assert optimal([-10**9, 10**9, -10**9]) == [1, [0, 0, 1]]
n = 1000
assert optimal(list(range(n, 0, -1)))[0] == n * (n - 1) // 2

random.seed(25)
for _ in range(800):
    n = random.randint(0, 25)
    nums = [random.randint(-6, 6) for _ in range(n)]
    assert optimal(nums) == brute(nums), nums
    assert at_most_variant(nums) == sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] >= nums[j])
print('random cross-check ok: 800 arrays (duplicates heavy), strict and >= variants')

big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
total = optimal(big)[0]
print('n = 10^5 random: total inversions =', total, '(expected about n^2/4 =', 10**10 // 4, ')')
