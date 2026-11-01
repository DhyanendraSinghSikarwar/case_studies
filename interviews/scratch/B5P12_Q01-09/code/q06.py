import itertools
import math
import random

random.seed(1206)

def permutations_used(nums):
    """used-array version. Returns (sorted result, calls)."""
    n = len(nums); out, cur, used, calls = [], [], [False] * n, [0]
    def go():
        calls[0] += 1
        if len(cur) == n:
            out.append(cur[:]); return
        for i in range(n):
            if used[i]:
                continue                    # pruning rule: an element can be placed once
            used[i] = True; cur.append(nums[i])     # choose
            go()                                    # explore
            cur.pop(); used[i] = False              # undo
    go()
    return sorted(out), calls[0]

def permutations_swap(nums):
    """Swap-in-place variant: no used array; the prefix nums[:k] is fixed. Output order is NOT sorted, so we sort."""
    a, out, calls = list(nums), [], [0]
    def go(k):
        calls[0] += 1
        if k == len(a):
            out.append(a[:]); return
        for i in range(k, len(a)):
            a[k], a[i] = a[i], a[k]
            go(k + 1)
            a[k], a[i] = a[i], a[k]
    go(0)
    return sorted(out), calls[0]

def unpruned(nums):
    """No used check: try every element at every position, filter at the leaves. Counts calls only (n <= 6 here)."""
    n = len(nums); calls = [0]; good = [0]
    def go(seq):
        calls[0] += 1
        if len(seq) == n:
            good[0] += len(set(seq)) == n; return
        for i in range(n):
            go(seq + (i,))
    go(())
    return calls[0], good[0]

def brute(nums):
    return sorted(map(list, itertools.permutations(nums)))

examples = [([3, 1, 2], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), ([], [[]]), ([9], [[9]]), ([2, 1], [[1, 2], [2, 1]])]
for nums, want in examples:
    assert permutations_used(nums)[0] == want == brute(nums) == permutations_swap(nums)[0]
    print(nums, '->', permutations_used(nums)[0])

# decision tree for [3, 1, 2] (used-array order = input order; the final list is then sorted)
lines = []
def tree(nums, cur=(), depth=0):
    if len(cur) == len(nums):
        lines.append('  ' * depth + 'leaf ' + str(list(cur))); return
    for v in nums:
        if v in cur:
            lines.append('  ' * depth + f'skip {v} (used)'); continue
        lines.append('  ' * depth + f'place {v}')
        tree(nums, cur + (v,), depth + 1)
tree([3, 1, 2])
print('\n'.join(lines[:13])); print('  ...', len(lines), 'lines in all')

# node counts: used array = sum n!/(n-k)!, unpruned = sum n^k
for n in range(0, 7):
    calls = permutations_used(list(range(n)))[1]
    assert calls == sum(math.factorial(n) // math.factorial(n - k) for k in range(n + 1))
    un, good = unpruned(list(range(n))) if n else (1, 1)
    assert good == math.factorial(n) and un == sum(n ** k for k in range(n + 1))
    print(f'n={n} used-array calls={calls:6} unpruned calls={un:6} results={good}')

# seeded cross-check
for _ in range(1000):
    nums = random.sample(range(-9, 10), random.randint(0, 6))
    r = permutations_used(nums)[0]
    assert r == brute(nums) == permutations_swap(nums)[0]
print('random cross-check ok: 1000 cases')

# edge: n = 8 gives 40320 permutations, sorted, all distinct; sorted(nums) first, reversed last
r = permutations_used([5, 3, 8, 1, 9, 2, 7, 4])[0]
assert len(r) == 40320 and r[0] == sorted(r[0]) and r[-1] == sorted(r[0], reverse=True)
assert permutations_used([])[0] == [[]] and permutations_used([-1, 0])[0] == [[-1, 0], [0, -1]]
print('edge asserts ok')
