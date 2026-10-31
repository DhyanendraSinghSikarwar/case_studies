import random

def build(nums):
    """table[j][i] = best (value, index) of block [i, i + 2^j). Tuples compare value first, then index: leftmost wins ties."""
    n = len(nums)
    table = [[(v, i) for i, v in enumerate(nums)]]
    j = 1
    while (1 << j) <= n:
        prev, half = table[-1], 1 << (j - 1)
        table.append([min(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)])
        j += 1
    return table

def optimal(nums, queries):
    table = build(nums)
    entries = sum(len(row) for row in table)
    answers = []
    for l, r in queries:
        k = (r - l + 1).bit_length() - 1                  # floor(log2(length)), no float log
        v, i = min(table[k][l], table[k][r - (1 << k) + 1])   # two overlapping blocks
        answers.append([v, i])
    return [answers, entries]

def brute(nums, queries):
    answers = []
    for l, r in queries:
        seg = nums[l:r + 1]
        m = min(seg)
        answers.append([m, l + seg.index(m)])             # list.index returns the leftmost
    n = len(nums)
    entries = sum(n - (1 << j) + 1 for j in range(n.bit_length()) if (1 << j) <= n)
    return [answers, entries]

assert optimal([5, 2, 4, 2, 7], [[0, 4], [2, 4], [0, 0]]) == [[[2, 1], [2, 3], [5, 0]], 11]
assert optimal([3], [[0, 0]]) == [[[3, 0]], 1]
print('examples:', optimal([5, 2, 4, 2, 7], [[0, 4], [2, 4], [0, 0]]), optimal([3], [[0, 0]]))

# the overlap is harmless for min (idempotent) but breaks a sum
nums = [1, 2, 3, 4, 5]
l, r = 0, 4; k = 2                                        # blocks [0,4) and [1,5) overlap on 1..3
wrong = sum(nums[0:4]) + sum(nums[1:5])
print('overlapping blocks: sum would be', wrong, 'instead of', sum(nums))
assert wrong != sum(nums)

# entries count: n log n growth; for n = 10^5
n = 10**5
cells = sum(n - (1 << j) + 1 for j in range(n.bit_length()) if (1 << j) <= n)
print('n = 10^5 table cells:', cells, '(about n * log2 n =', round(n * 16.6), ')')

random.seed(24)
for _ in range(600):
    n = random.randint(1, 40)
    nums = [random.randint(-5, 5) for _ in range(n)]      # small range = many ties
    qs = []
    for _ in range(30):
        l = random.randrange(n); qs.append([l, random.randint(l, n - 1)])
    assert optimal(nums, qs) == brute(nums, qs), (nums, qs)
print('random cross-check ok: 600 arrays x 30 queries, many duplicate minima')

# all equal: the leftmost index must be l itself
assert optimal([7] * 9, [[3, 8], [0, 8]])[0] == [[7, 3], [7, 0]]
big = [random.randint(0, 10**9) for _ in range(10**5)]
qs = [[l, random.randint(l, 10**5 - 1)] for l in (random.randrange(10**5) for _ in range(1000))]
assert optimal(big, qs) == brute(big, qs)
print('n = 10^5, 1000 random queries ok')
