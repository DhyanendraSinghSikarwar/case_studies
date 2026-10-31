import itertools, random, math, collections

random.seed(19)

def perms_dup(nums, rule='left_unused'):
    """Distinct permutations. rule 'left_unused': skip a[i] if a[i]==a[i-1] and NOT used[i-1] (correct, tight).
    rule 'left_used': skip if a[i]==a[i-1] and used[i-1] (also correct, but prunes late). Returns (result, calls)."""
    a = sorted(nums); n = len(a); used = [False] * n; cur = []; out = []; calls = 0
    def go():
        nonlocal calls
        calls += 1
        if len(cur) == n:
            out.append(cur[:]); return
        for i in range(n):
            if used[i]: continue
            if i and a[i] == a[i - 1]:
                if rule == 'left_unused' and not used[i - 1]: continue
                if rule == 'left_used' and used[i - 1]: continue
            used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go()
    return out, calls

def no_skip(nums):
    """Plain permutations with a used array and no duplicate rule: n! leaves, many repeated. Returns (list, calls)."""
    a = sorted(nums); n = len(a); used = [False] * n; cur = []; out = []; calls = 0
    def go():
        nonlocal calls
        calls += 1
        if len(cur) == n: out.append(cur[:]); return
        for i in range(n):
            if not used[i]:
                used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go(); return out, calls

def permutations_dup(nums):
    return perms_dup(nums)[0]          # already in ascending order because the input is sorted and we try indices in order

def brute(nums):
    return sorted(map(list, set(itertools.permutations(nums))))

def multinomial(nums):
    c = collections.Counter(nums); r = math.factorial(len(nums))
    for v in c.values(): r //= math.factorial(v)
    return r

# examples
for nums, exp in [([2, 1, 2], [[1, 2, 2], [2, 1, 2], [2, 2, 1]]), ([5], [[5]]), ([], [[]]),
                  ([3, 3, 1, 1], [[1, 1, 3, 3], [1, 3, 1, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 1, 3, 1], [3, 3, 1, 1]])]:
    got = permutations_dup(nums)
    assert got == exp == brute(nums), nums
    print('example', nums, '->', got)

# decision tree of [1, 1, 2] under the correct rule (indent = depth; X = skipped by the rule)
def show_tree(nums):
    a = sorted(nums); n = len(a); used = [False] * n; cur = []
    def go(d):
        if len(cur) == n:
            print('  ' * d + '-> leaf', cur); return
        for i in range(n):
            if used[i]: continue
            if i and a[i] == a[i - 1] and not used[i - 1]:
                print('  ' * d + f'skip index {i} (value {a[i]}): twin at {i-1} not used'); continue
            used[i] = True; cur.append(a[i]); print('  ' * d + f'pick index {i} -> {cur}'); go(d + 1); cur.pop(); used[i] = False
    go(0)
print('decision tree for [2, 1, 2] (sorted: [1, 2, 2]):')
show_tree([2, 1, 2])

# node counts: no rule vs correct rule vs the other rule, on [1, 1, 2, 2]
for nums in ([1, 2, 2], [1, 1, 2, 2], [1, 1, 1, 2, 2, 3]):
    r0, c0 = no_skip(nums); r1, c1 = perms_dup(nums, 'left_unused'); r2, c2 = perms_dup(nums, 'left_used')
    assert sorted(r1) == brute(nums) and sorted(r2) == brute(nums)
    print(f'{nums}: results={len(r1)} (multinomial {multinomial(nums)}); calls no-rule={c0} (leaves {len(r0)}), left-unused rule={c1}, left-used rule={c2}')

# claim 1: count = multinomial; both rules correct and left-unused never more calls (all multisets of 5 values from {1,2,3}, plus length 0..4)
worse = 0; total = 0
for L in range(0, 7):
    for nums in itertools.product([1, 2, 3], repeat=L):
        if L > 5 and sum(nums) % 7: continue       # thin the length-6 family to keep it quick
        total += 1
        r1, c1 = perms_dup(list(nums), 'left_unused'); r2, c2 = perms_dup(list(nums), 'left_used')
        assert len(r1) == multinomial(nums) and r1 == sorted(r1) and len(set(map(tuple, r1))) == len(r1)
        assert sorted(r2) == r1
        assert c1 <= c2
        worse += c1 < c2
print('inputs checked', total, '| count == multinomial and both rules right on all; left-unused fewer calls on', worse)

# claim 2: equal values keep their ORIGINAL relative order (tag the twins and look at the generated order)
a = [(1, 'a'), (1, 'b'), (2, 'c')]
tagged = []
used = [False] * 3; cur = []
def go():
    if len(cur) == 3: tagged.append([t[1] for t in cur]); return
    for i in range(3):
        if used[i]: continue
        if i and a[i][0] == a[i - 1][0] and not used[i - 1]: continue
        used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
go()
print('tagged twins 1a, 1b, 2c; each leaf lists tags in order:', tagged)
assert all(t.index('a') < t.index('b') for t in tagged)

# seeded random cross-check against set(itertools.permutations)
for _ in range(400):
    n = random.randint(0, 7); nums = [random.randint(0, 3) for _ in range(n)]
    assert permutations_dup(nums) == brute(nums), nums
print('400 seeded random cases agree')

# edge asserts
assert permutations_dup([]) == [[]] and permutations_dup([7, 7, 7]) == [[7, 7, 7]]
assert permutations_dup([-1, 0, -1]) == [[-1, -1, 0], [-1, 0, -1], [0, -1, -1]]
assert len(permutations_dup([1, 2, 3, 4, 5, 6, 7, 8])) == 40320 and len(permutations_dup([1] * 8)) == 1
print('edge asserts passed; 8 distinct values ->', len(permutations_dup(list(range(8)))), 'results; recursion depth <= 8')
