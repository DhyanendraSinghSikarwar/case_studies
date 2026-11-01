import itertools, random

random.seed(21)

def comb_sum2(candidates, target, skip=True, brk=True):
    """Each input element at most once; each distinct combination once. Returns (result, calls)."""
    c = sorted(candidates); out = []; cur = []; calls = 0; iters = 0
    def go(start, rem):
        nonlocal calls, iters
        calls += 1
        if rem == 0:
            out.append(cur[:]); return
        for j in range(start, len(c)):
            iters += 1
            if c[j] > rem:
                if brk: break
                continue
            if skip and j > start and c[j] == c[j - 1]: continue     # same value already tried at this level
            cur.append(c[j]); go(j + 1, rem - c[j]); cur.pop()
    go(0, target)
    comb_sum2.iters = iters
    return out, calls

def solve(candidates, target): return sorted(comb_sum2(candidates, target)[0])

def brute(candidates, target):
    n = len(candidates); res = set()
    for mask in range(1, 1 << n):
        sub = tuple(sorted(candidates[i] for i in range(n) if mask >> i & 1))
        if sum(sub) == target: res.add(sub)
    return sorted(map(list, res))

for cand, t, exp in [([3, 1, 1, 2, 4, 2], 6, [[1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 4]]),
                     ([2, 2, 2], 4, [[2, 2]]), ([5, 6], 3, []), ([4], 4, [[4]])]:
    got = solve(cand, t)
    assert got == exp == brute(cand, t)
    print('example', cand, t, '->', got)

def tree(cand, target):
    c = sorted(cand); cur = []
    def go(start, rem, d):
        if rem == 0: print('  ' * d + '-> hit', cur); return
        for j in range(start, len(c)):
            if c[j] > rem: print('  ' * d + f'break: c[{j}]={c[j]} > remaining {rem}'); break
            if j > start and c[j] == c[j - 1]: print('  ' * d + f'skip c[{j}]={c[j]} (same as left neighbour at this level)'); continue
            cur.append(c[j]); print('  ' * d + f'take c[{j}]={c[j]} -> {cur}, remaining {rem - c[j]}'); go(j + 1, rem - c[j], d + 1); cur.pop()
    go(0, target, 0)
print('decision tree, sorted candidates [1, 1, 2, 2, 3, 4], target 6:'); tree([3, 1, 1, 2, 4, 2], 6)

# node counts: all four combinations of the two prunings on the first example and a larger one
def compare(cand, t):
    row = {}
    for skip in (False, True):
        for brk in (False, True):
            r, calls = comb_sum2(cand, t, skip, brk); row[(skip, brk)] = (calls, comb_sum2.iters)
            assert len(set(map(tuple, r))) == len(solve(cand, t)) and sorted(set(map(tuple, r))) == sorted(map(tuple, solve(cand, t)))
    return row
for cand, t in [([3, 1, 1, 2, 4, 2], 6), ([1] * 7 + [2] * 7, 14), ([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5], 20)]:
    row = compare(cand, t)
    print(f'{len(cand)} candidates, target {t}, answers {len(solve(cand, t))}: (calls, loop steps): neither={row[(False, False)]}, break only={row[(False, True)]}, skip only={row[(True, False)]}, both={row[(True, True)]}')

# without the skip rule duplicates appear:
r, _ = comb_sum2([2, 2, 2], 4, skip=False)
print('no skip rule on [2, 2, 2], target 4:', r, '(three copies of [2, 2])')
# with j > 0 instead of j > start the valid [1, 1, 2] is lost for [1, 1, 2], target 4
def wrong_skip(candidates, target):
    c = sorted(candidates); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            if j > 0 and c[j] == c[j - 1]: continue            # WRONG: compares with the global left neighbour
            cur.append(c[j]); go(j + 1, rem - c[j]); cur.pop()
    go(0, target); return out
print('wrong test j > 0 on [1, 1, 2], target 4 ->', wrong_skip([1, 1, 2], 4), ' correct ->', solve([1, 1, 2], 4))
assert wrong_skip([1, 1, 2], 4) == [] and solve([1, 1, 2], 4) == [[1, 1, 2]]

# Q8 difference: recursing with j reuses an element
def reuse(candidates, target):
    c = sorted(set(candidates)); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            cur.append(c[j]); go(j, rem - c[j]); cur.pop()
    go(0, target); return out
print('Q8 style (reuse, recurse with j) on [3, 1, 2, 4], target 6:', reuse([3, 1, 2, 4], 6))
print('once-each (this question) on [3, 1, 2, 4], target 6:', solve([3, 1, 2, 4], 6))

# properties and seeded random cross-check vs bitmask
for _ in range(400):
    n = random.randint(1, 10); cand = [random.randint(1, 6) for _ in range(n)]; t = random.randint(1, 20)
    got = solve(cand, t)
    assert got == brute(cand, t), (cand, t)
    assert got == sorted(got) and len({tuple(x) for x in got}) == len(got)
    assert all(x == sorted(x) and sum(x) == t for x in got)
print('400 seeded random cases agree (sorted, no duplicates, each sums to target)')

# edge and max size asserts
assert solve([4], 4) == [[4]] and solve([5, 6], 3) == [] and solve([1], 2) == []
big = solve([1] * 14, 14); assert big == [[1] * 14]
print('14 ones, target 14 ->', len(big), 'combination; depth up to 14, well under the recursion limit of 1000')
print('edge asserts passed')
