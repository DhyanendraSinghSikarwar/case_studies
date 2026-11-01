import random

random.seed(1218)

def subsets_dup(nums, stats=None):
    """Sort, then loop from `start`; skip a value equal to its left neighbour at the SAME level (i > start)."""
    a = sorted(nums)
    out, cur = [], []
    calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        out.append(cur[:])                      # every node of this tree is one answer
        for i in range(start, len(a)):
            if i > start and a[i] == a[i - 1]:
                continue                        # same value already tried as the next element at this level
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    if stats is not None: stats.append(calls)
    assert out == sorted(out)                   # the DFS preorder is already the required order (prefix before extension, siblings ascending)
    return out

def subsets_no_skip(nums):
    """Same tree without the skip: 2^n calls, then dedupe at the end. Shows the waste."""
    a = sorted(nums)
    out, cur = [], []
    calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        out.append(tuple(cur))
        for i in range(start, len(a)):
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    return sorted(map(list, set(out))), calls

def subsets_wrong_skip(nums):
    """WRONG on purpose: i > 0 instead of i > start."""
    a = sorted(nums)
    out, cur = [], []
    def go(start):
        out.append(cur[:])
        for i in range(start, len(a)):
            if i > 0 and a[i] == a[i - 1]:
                continue
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    return sorted(out)

def brute(nums):
    n = len(nums)
    return sorted(map(list, {tuple(sorted(nums[i] for i in range(n) if m >> i & 1)) for m in range(1 << n)}))

for nums, want in [([3, 1, 3], [[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]), ([], [[]]),
                   ([2, 2, 2], [[], [2], [2, 2], [2, 2, 2]]),
                   ([1, 2, 2, 1], [[], [1], [1, 1], [1, 1, 2], [1, 1, 2, 2], [1, 2], [1, 2, 2], [2], [2, 2]])]:
    assert subsets_dup(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# decision tree on [1, 2, 2]
print("--- decision tree for [1, 2, 2] (a node = a call = one answer) ---")
a = [1, 2, 2]
def show(start, cur, depth):
    print("  " * depth + str(cur))
    for i in range(start, len(a)):
        if i > start and a[i] == a[i - 1]:
            print("  " * (depth + 1) + "skip index %d (value %d equals its left neighbour at this level)" % (i, a[i]))
            continue
        show(i + 1, cur + [a[i]], depth + 1)
show(0, [], 0)

# the wrong skip
print("--- i > 0 instead of i > start ---")
good, bad = subsets_dup([1, 2, 2]), subsets_wrong_skip([1, 2, 2])
print("correct:", good)
print("i > 0  :", bad, "| lost:", [s for s in good if s not in bad])
wrong_cases = 0
for _ in range(300):
    nums = [random.randint(1, 3) for _ in range(random.randint(0, 6))]
    if subsets_wrong_skip(nums) != brute(nums): wrong_cases += 1
print("i > 0 wrong on", wrong_cases, "of 300 seeded random inputs")
assert wrong_cases > 0

# node counts
print("--- calls (nodes) ---")
for nums in ([1, 2, 2], [1, 2, 2, 1], [2, 2, 2, 2, 2, 2], [1, 1, 2, 2, 3, 3, 4, 4], list(range(8))):
    st = []
    res = subsets_dup(nums, st)
    _, plain = subsets_no_skip(nums)
    print("%-26s distinct=%3d calls with skip=%3d calls without skip=%3d" % (nums, len(res), st[0], plain))
    assert st[0] == len(res)

# seeded random cross-check
for _ in range(300):
    nums = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    assert subsets_dup(nums) == brute(nums) == subsets_no_skip(nums)[0], nums
print("300 seeded random inputs agree with the bitmask-set oracle")
# the count of distinct subsets is the product of (multiplicity + 1)
import collections, math
for _ in range(200):
    nums = [random.randint(1, 4) for _ in range(random.randint(0, 9))]
    assert len(subsets_dup(nums)) == math.prod(c + 1 for c in collections.Counter(nums).values())
print("200 seeded random inputs: number of distinct subsets = product of (multiplicity + 1)")
# edge asserts
assert subsets_dup([]) == [[]]
assert subsets_dup([5]) == [[], [5]]
assert len(subsets_dup(list(range(10)))) == 1024
assert len(subsets_dup([7] * 10)) == 11
x = [3, 1, 3]; subsets_dup(x); assert x == [3, 1, 3]       # input not mutated (we sort a copy)
print("edge asserts ok")
