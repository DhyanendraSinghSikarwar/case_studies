import itertools, random, math

random.seed(20)

def combinations(n, k, prune=True):
    """All k-subsets of 1..n ascending. Returns (result, calls). prune=True stops the loop at n-(k-len(path))+1."""
    out = []; path = []; calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        if len(path) == k:
            out.append(path[:]); return
        hi = n - (k - len(path)) + 1 if prune else n      # last value that still leaves room for the rest
        for v in range(start, hi + 1):
            path.append(v); go(v + 1); path.pop()
    go(1)
    return out, calls

def solve(n, k): return combinations(n, k)[0]
def brute(n, k): return sorted(map(list, itertools.combinations(range(1, n + 1), k)))

for n, k, exp in [(5, 3, [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]),
                  (3, 3, [[1, 2, 3]]), (4, 1, [[1], [2], [3], [4]]), (1, 1, [[1]])]:
    got = solve(n, k)
    assert got == exp == brute(n, k)
    print('example', (n, k), '->', got)

# decision tree for n=4, k=2 with pruning (X = value cut by the bound)
def tree(n, k):
    path = []
    def go(start, d):
        if len(path) == k: print('  ' * d + '-> leaf', path); return
        hi = n - (k - len(path)) + 1
        for v in range(start, hi + 1):
            path.append(v); print('  ' * d + f'pick {v} -> {path}'); go(v + 1, d + 1); path.pop()
        if hi < n: print('  ' * d + f'(loop stops at {hi}; values {hi + 1}..{n} cannot leave room for {k - len(path)} number(s))')
    go(1, 0)
print('decision tree n=4, k=2 (pruned):'); tree(4, 2)

# node counts: pruned vs unpruned
print('calls (nodes visited), pruned vs unpruned:')
for n, k in [(5, 3), (6, 4), (10, 8), (12, 10), (20, 19), (20, 10)]:
    r1, c1 = combinations(n, k, True); r0, c0 = combinations(n, k, False)
    assert r1 == r0 and len(r1) == math.comb(n, k)
    print(f'  n={n:2d} k={k:2d}: results={len(r1):6d}  pruned={c1:7d}  unpruned={c0:7d}  dead nodes removed={c0 - c1}')

# claim: pruned search has no dead nodes: every call is on a path to a result, calls = sum over depth of C(n, depth)-ish. Check exact formula
# number of calls at depth d = number of valid prefixes of length d = C(n-k+d, d) ... verify by counting
for n in range(1, 9):
    for k in range(1, n + 1):
        r1, c1 = combinations(n, k, True)
        assert c1 == sum(math.comb(n - k + d, d) for d in range(k + 1)), (n, k)
print('pruned calls == sum_d C(n-k+d, d) for all 1 <= k <= n <= 8')
# and unpruned never fewer than pruned
for n in range(1, 11):
    for k in range(1, n + 1):
        assert combinations(n, k, True)[1] <= combinations(n, k, False)[1]
print('pruned calls <= unpruned calls for all 1 <= k <= n <= 10')

# size claim
big = solve(20, 10)
assert len(big) == 184756 == math.comb(20, 10) and big[0] == list(range(1, 11)) and big[-1] == list(range(11, 21))
print('C(20, 10) =', len(big), ' first', big[0], ' last', big[-1])
assert max(math.comb(20, k) for k in range(1, 21)) == 184756

# seeded random cross-check vs itertools.combinations
for _ in range(300):
    n = random.randint(1, 9); k = random.randint(1, n)
    assert solve(n, k) == brute(n, k) == sorted(solve(n, k))
print('300 seeded random cases agree; also exhaustive over 1 <= k <= n <= 10')
for n in range(1, 11):
    for k in range(1, n + 1): assert solve(n, k) == brute(n, k)
assert solve(1, 1) == [[1]] and solve(4, 4) == [[1, 2, 3, 4]]
print('edge asserts passed; depth is k <= 20, recursion limit 1000 is no problem')
