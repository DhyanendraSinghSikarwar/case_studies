import random

random.seed(1204)

def subsets_inc_exc(nums):
    """Include-or-exclude: one yes/no decision per element. Returns (sorted result, number of calls)."""
    out, cur, calls = [], [], [0]
    def go(i):
        calls[0] += 1
        if i == len(nums):
            out.append(cur[:])             # copy: cur keeps changing
            return
        go(i + 1)                           # exclude nums[i]
        cur.append(nums[i])                 # choose
        go(i + 1)                           # explore
        cur.pop()                           # undo
    go(0)
    return sorted(out), calls[0]

def subsets_start_index(nums):
    """Start-index version: every node is an answer, so only 2^n calls."""
    out, cur, calls = [], [], [0]
    def go(start):
        calls[0] += 1
        out.append(cur[:])
        for j in range(start, len(nums)):
            cur.append(nums[j]); go(j + 1); cur.pop()
    go(0)
    return sorted(out), calls[0]

def brute(nums):                           # bitmask loop
    n = len(nums)
    return sorted([nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n))

examples = [([4, 1, 7], [[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]), ([], [[]]), ([5], [[], [5]]), ([3, 1], [[], [1], [3], [3, 1]])]
for nums, want in examples:
    assert subsets_inc_exc(nums)[0] == want == brute(nums) == subsets_start_index(nums)[0]
    print(nums, '->', subsets_inc_exc(nums)[0])

# decision tree for [4, 1] (E = exclude, I = include); leaf = subset
def tree(nums, i=0, cur=(), depth=0):
    pad = '  ' * depth
    if i == len(nums):
        print(f'{pad}leaf {list(cur)}'); return
    print(f'{pad}at {nums[i]}:')
    print(f'{pad} exclude'); tree(nums, i + 1, cur, depth + 1)
    print(f'{pad} include'); tree(nums, i + 1, cur + (nums[i],), depth + 1)
tree([4, 1])

# call counts: 2^(n+1)-1 for include/exclude, 2^n for start-index; there is nothing to prune (every leaf is an answer)
for n in range(0, 11):
    nums = list(range(n))
    assert subsets_inc_exc(nums)[1] == 2 ** (n + 1) - 1
    assert subsets_start_index(nums)[1] == 2 ** n
    assert len(subsets_inc_exc(nums)[0]) == 2 ** n
print('calls for n=10: include/exclude', subsets_inc_exc(list(range(10)))[1], ' start-index', subsets_start_index(list(range(10)))[1])

# seeded cross-check
for _ in range(1500):
    nums = random.sample(range(-9, 10), random.randint(0, 8))
    r = subsets_inc_exc(nums)[0]
    assert r == brute(nums) == subsets_start_index(nums)[0]
    assert len(r) == 2 ** len(nums) and len({tuple(s) for s in r}) == len(r)
print('random cross-check ok: 1500 cases')

# edge: negative and unordered input; n = 10 gives 1024 subsets
assert subsets_inc_exc([-1, 0])[0] == [[], [-1], [-1, 0], [0]]
assert len(subsets_inc_exc(list(range(10)))[0]) == 1024
print('edge asserts ok')
