import random
random.seed(46)

def count_smaller(nums):
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}      # compress to 1..k
    t = [0] * (len(ranks) + 1)
    def add(i):
        while i < len(t):
            t[i] += 1; i += i & -i
    def pre(i):
        s = 0
        while i > 0:
            s += t[i]; i -= i & -i
        return s
    res = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):        # right to left: the tree holds exactly nums[i+1:]
        res[i] = pre(ranks[nums[i]] - 1)          # strictly smaller ranks only
        add(ranks[nums[i]])
    return res

def brute(nums):
    return [sum(1 for j in range(i + 1, len(nums)) if nums[j] < nums[i]) for i in range(len(nums))]

assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
assert count_smaller([2, 2, 2]) == [0, 0, 0]
assert count_smaller([]) == []
print('examples ok')

for _ in range(600):
    nums = [random.randint(-4, 4) for _ in range(random.randint(0, 12))]
    assert count_smaller(nums) == brute(nums), nums
print('600 random arrays match the O(n^2) double loop')

assert count_smaller([7]) == [0]
assert count_smaller([3, 2, 1]) == [2, 1, 0]                 # descending
assert count_smaller([1, 2, 3]) == [0, 0, 0]                 # ascending
assert count_smaller([-10**9, 10**9, -10**9]) == [0, 1, 0]   # extremes, duplicates
# direction matters: scanning left to right and using the same query counts elements to the LEFT instead
def left_count(nums):
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}; t = [0] * (len(ranks) + 1); out = []
    for v in nums:
        i = ranks[v] - 1; s = 0
        while i > 0: s += t[i]; i -= i & -i
        out.append(s); i = ranks[v]
        while i < len(t): t[i] += 1; i += i & -i
    return out
print('left-to-right scan gives', left_count([5, 2, 6, 1]), 'not', count_smaller([5, 2, 6, 1]))
assert left_count([5, 2, 6, 1]) != [2, 1, 1, 0]
nums = [random.randint(-10**9, 10**9) for _ in range(10**5)]
r = count_smaller(nums); assert len(r) == 10**5 and all(0 <= x < 10**5 for x in r)
print('n = 10^5 ok')
print('first example:', count_smaller([5, 2, 6, 1]))
