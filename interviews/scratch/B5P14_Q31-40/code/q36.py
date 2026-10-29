import random
from bisect import bisect_left, bisect_right

random.seed(3601)


def reverse_pairs(nums):
    """Count i < j with nums[i] > 2 * nums[j] using a Fenwick tree over compressed values."""
    if not nums:
        return 0
    vals = sorted(set(nums))                     # coordinate compression (distinct sorted values)
    m = len(vals)
    tree = [0] * (m + 1)                         # 1-indexed BIT of counts

    def add(i):                                  # i is a 1-based rank
        while i <= m:
            tree[i] += 1
            i += i & -i

    def prefix(i):                               # how many stored values have rank <= i
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    ans = 0
    for j, x in enumerate(nums):
        # earlier elements <= 2x: bisect_right gives how many DISTINCT values are <= 2x, i.e. the top rank to count
        # (2x need not be a stored value, so we cannot look up its rank)
        not_greater = prefix(bisect_right(vals, 2 * x))
        ans += j - not_greater                   # earlier elements are j in total; the rest are > 2x
        add(bisect_left(vals, x) + 1)            # insert nums[j] AFTER the query
    return ans


def brute(nums):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > 2 * nums[j])


# --- the prompt's examples ---
ex = [([1, 3, 2, 3, 1], 2), ([2, 4, 3, 5, 1], 3), ([-5, -5], 1), ([], 0)]
for nums, want in ex:
    got = reverse_pairs(nums)
    print(nums, '->', got)
    assert got == want == brute(nums)

# --- random cross-check against the O(n^2) double loop ---
for _ in range(1500):
    n = random.randint(0, 14)
    hi = random.choice([3, 10, 100])
    nums = [random.randint(-hi, hi) for _ in range(n)]
    assert reverse_pairs(nums) == brute(nums), nums
print('random cases passed: 1500')

# --- edge cases ---
assert reverse_pairs([0, 0, 0]) == 0                       # 0 > 0 is false
assert reverse_pairs([1]) == 0
assert reverse_pairs([-1, -1]) == 1                        # -1 > -2: negatives make equal values a pair
assert reverse_pairs([5, 2]) == 1 and reverse_pairs([4, 2]) == 0   # strict: 4 > 4 is false
assert reverse_pairs([2 ** 31, -2 ** 31]) == 1             # 2 * value exceeds 32 bits: fine in Python
assert reverse_pairs([2 ** 31] * 3) == 0
n = 5 * 10 ** 4
assert reverse_pairs(list(range(n))) == 0                  # increasing: no pair
d = reverse_pairs(list(range(n, 0, -1)))                   # decreasing n..1: pair (a, b) needs a > 2b
assert d == sum(n - 2 * b for b in range(1, n // 2 + 1))   # closed form
print('n = 50000 strictly decreasing ->', d)
print('edge asserts passed')
