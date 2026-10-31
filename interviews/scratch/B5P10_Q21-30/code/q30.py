import random, itertools, sys
from functools import cache

random.seed(30)
INF = float('inf')

def last_stone_ii(stones):
    """Split into two groups with sums a <= b: last stone = b - a = total - 2a. Maximise a <= total // 2 by subset sums."""
    total = sum(stones); half = total // 2
    can = [True] + [False] * half               # can[s]: some subset sums to s
    for x in stones:
        for s in range(half, x - 1, -1):         # downward: each stone used at most once
            if can[s - x]: can[s] = True
    a = max(s for s in range(half + 1) if can[s])
    return total - 2 * a

def bitset(stones):
    total = sum(stones); bits = 1
    for x in stones: bits |= bits << x
    h = total // 2
    while not bits >> h & 1: h -= 1
    return total - 2 * h

def memo_subset(stones):
    total = sum(stones); half = total // 2; n = len(stones)
    @cache
    def best(i, cap):                            # largest subset sum <= cap using stones[i:]
        if i == n: return 0
        r = best(i + 1, cap)
        if stones[i] <= cap: r = max(r, stones[i] + best(i + 1, cap - stones[i]))
        return r
    return total - 2 * best(0, half)

def signs(stones):
    n = len(stones); best = INF
    for mask in range(1 << n):
        s = sum(x if mask >> i & 1 else -x for i, x in enumerate(stones))
        best = min(best, abs(s))
    return best

def smashes(stones):
    """Every sequence of smashes (choose any two stones each time)."""
    @cache
    def f(state):
        if len(state) <= 1: return state[0] if state else 0
        best = INF
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                rest = list(state[:i] + state[i + 1:j] + state[j + 1:])
                d = state[j] - state[i]
                if d: rest.append(d)
                best = min(best, f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(stones)))

for st, exp in [([2, 7, 4, 1, 8, 1], 1), ([31, 26, 33, 21, 40], 5), ([5], 5), ([3, 3], 0), ([1, 2, 5], 2)]:
    assert last_stone_ii(st) == bitset(st) == memo_subset(st) == signs(st) == smashes(st) == exp, st
    print('example', st, '->', exp)

st = [2, 7, 4, 1, 8, 1]; total = sum(st); half = total // 2
can = [True] + [False] * half
print('total', total, 'half', half, '; reachable subset sums 0..', half, 'after each stone:')
for x in st:
    for s in range(half, x - 1, -1):
        if can[s - x]: can[s] = True
    print(f'  after {x}:', [s for s in range(half + 1) if can[s]])
a = max(s for s in range(half + 1) if can[s])
print('best group sum a =', a, '-> last stone =', total, '-', 2 * a, '=', total - 2 * a)

n_cases = 0
for _ in range(500):
    n = random.randint(1, 7); st = [random.randint(1, 12) for _ in range(n)]
    want = smashes(st)
    assert last_stone_ii(st) == bitset(st) == memo_subset(st) == want == signs(st), st
    n_cases += 1
print('cross-check cases (len <= 7)', n_cases, ': subset-sum DP == bitset == memo == every smash order == all sign assignments')
for _ in range(200):
    st = [random.randint(1, 30) for _ in range(random.randint(1, 14))]
    assert last_stone_ii(st) == signs(st) == bitset(st)
print('200 more (len <= 14) against all sign assignments')

big = [random.randint(1, 100) for _ in range(30)]
print('n = 30, values <= 100 ->', last_stone_ii(big), '(total', sum(big), ')')
print('limit', sys.getrecursionlimit(), '- memo recursion depth is len(stones) <= 30, far below it')
assert last_stone_ii([100] * 30) == 0 and last_stone_ii([1]) == 1 and last_stone_ii([1, 100]) == 99
print('edge asserts passed')
