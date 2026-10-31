import itertools
import random

random.seed(103)

def kadane(nums):
    """best_here = best sum of a subarray ENDING exactly at i: max(x, best_here_prev + x). Answer = max over all i."""
    best_here = best = nums[0]
    for x in nums[1:]:
        best_here = max(x, best_here + x)      # extend the previous subarray, or restart at x
        best = max(best, best_here)
    return best

def kadane_table(nums):
    ends, cur = [], 0
    for i, x in enumerate(nums):
        cur = x if i == 0 else max(x, cur + x)
        ends.append(cur)
    return ends

def brute(nums):
    n = len(nums)
    return max(sum(nums[i:j + 1]) for i in range(n) for j in range(i, n))   # O(n^2) subarrays (sum is O(n): O(n^3) overall)

def brute_prefix(nums):
    """True O(n^2): prefix sums."""
    n = len(nums); pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    return max(pre[j] - pre[i] for i in range(n) for j in range(i + 1, n + 1))

for a, want in [([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6), ([-3, -1, -2], -1), ([7], 7), ([5, -9, 6], 6)]:
    assert kadane(a) == brute(a) == brute_prefix(a) == want
print('4 prompt examples ok')

a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print('nums      ', a)
print('ends at i ', kadane_table(a))
print('answer = max over i =', max(kadane_table(a)), ' (last state is', kadane_table(a)[-1], ')')

for _ in range(1000):
    n = random.randint(1, 12)
    a = [random.randint(-10, 10) for _ in range(n)]
    assert kadane(a) == brute(a) == brute_prefix(a) == max(kadane_table(a)), a
print('1000 seeded random lists (len 1..12, values -10..10): Kadane == enumeration')

cnt = 0
for n in range(1, 7):
    for a in itertools.product(range(-3, 3), repeat=n):
        assert kadane(list(a)) == brute(list(a)); cnt += 1
print('exhaustive len 1..6 values -3..2:', cnt, 'lists ok')

# why max over all i: count lists where the last state is NOT the answer
last_wrong = 0; total = 0
for n in range(1, 6):
    for a in itertools.product(range(-3, 4), repeat=n):
        total += 1
        if kadane_table(list(a))[-1] != brute(list(a)):
            last_wrong += 1
print(f'last state != answer on {last_wrong} of {total} lists (len 1..5, values -3..3)')

# all-negative: answer is the largest element, never 0
for _ in range(200):
    a = [random.randint(-9, -1) for _ in range(random.randint(1, 8))]
    assert kadane(a) == max(a) < 0
print('all-negative lists: answer = max element (200 seeded lists)')

big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
print('n = 10^5 ->', kadane(big), end=' ')
pre = 0; mn = 0; best = -10**9
for x in big:
    pre += x; best = max(best, pre - mn); mn = min(mn, pre)
assert best == kadane(big); print('(agrees with the prefix-sum minus smallest earlier prefix method)')
