import random, itertools, sys, time

random.seed(23)

def matrix_chain(dims):
    """cost[i][j] = fewest scalar multiplications for matrices A_i..A_j; split[i][j] = smallest k achieving it."""
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = None
            for k in range(i, j):                      # left part A_i..A_k, right part A_k+1..A_j
                c = cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if best is None or c < best:           # STRICT <: the first (smallest) k wins ties
                    best = c
                    split[i][j] = k
            cost[i][j] = best

    def paren(i, j):
        if i == j:
            return 'A%d' % i
        k = split[i][j]
        return '(' + paren(i, k) + paren(k + 1, j) + ')'
    return [cost[0][n - 1], paren(0, n - 1)], cost, split

def solve(dims):
    return matrix_chain(dims)[0]

def brute(dims):
    """Enumerate every parenthesisation; choose by cost, then by smallest root split, then (recursively) left tree, then right tree."""
    n = len(dims) - 1
    def trees(i, j):
        if i == j:
            yield (0, (), 'A%d' % i)
            return
        for k in range(i, j):
            for cl, kl, sl in trees(i, k):
                for cr, kr, sr in trees(k + 1, j):
                    yield (cl + cr + dims[i] * dims[k + 1] * dims[j + 1], (k, kl, kr), '(' + sl + sr + ')')
    best = min(trees(0, n - 1), key=lambda t: (t[0], t[1]))
    return [best[0], best[2]]

def count_trees(n):                                     # Catalan(n - 1)
    from math import comb
    return comb(2 * (n - 1), n - 1) // n

# examples
for dims, exp in [([10, 30, 5, 60], [4500, '((A0A1)A2)']), ([40, 20, 30, 10, 30], [26000, '((A0(A1A2))A3)']),
                  ([5, 7], [0, 'A0']), ([1, 2, 3, 4, 5], [38, '(((A0A1)A2)A3)'])]:
    a, b = solve(dims), brute(dims)
    assert a == b == exp, (dims, a, b)
    print('example', dims, '->', a)

# hand table for dims = [10, 30, 5, 60]
dims = [10, 30, 5, 60]
_, cost, split = matrix_chain(dims)
print('dims', dims, '-> matrices A0 10x30, A1 30x5, A2 5x60')
print('cost table (rows i, columns j):')
for row in cost: print('  ', row)
print('split table:')
for row in split: print('  ', row)
print('cost[0][2]: k=0 ->', cost[0][0] + cost[1][2] + 10 * 30 * 60, ' k=1 ->', cost[0][1] + cost[2][2] + 10 * 5 * 60)

# a tie to show the smallest-k rule: all dims equal, every parenthesisation costs the same
print('tie example dims [2,2,2,2] ->', solve([2, 2, 2, 2]), '(all', count_trees(3), 'trees cost 16; smallest root split k=0 wins)')
assert solve([2, 2, 2, 2]) == [16, '(A0(A1A2))']

# seeded cross-check, n <= 6 matrices, small dims so ties are common
cases = 0
for _ in range(400):
    n = random.randint(1, 6)
    dims = [random.randint(1, 4) for _ in range(n + 1)]
    got, want = solve(dims), brute(dims)
    assert got == want, (dims, got, want)
    cases += 1
print('cross-check cases', cases)

# exhaustive: all chains of 4 matrices (5 dims) with dims in 1..3, and all of 3 matrices with dims 1..5
cnt = 0
for dims in itertools.product(range(1, 4), repeat=5):
    assert solve(list(dims)) == brute(list(dims)); cnt += 1
for dims in itertools.product(range(1, 6), repeat=4):
    assert solve(list(dims)) == brute(list(dims)); cnt += 1
print('exhaustive chains checked:', cnt)

# how many random chains had more than one optimal tree (so the tie rule mattered)
def all_optimal(dims):
    n = len(dims) - 1
    def trees(i, j):
        if i == j:
            yield (0, 'A%d' % i); return
        for k in range(i, j):
            for cl, sl in trees(i, k):
                for cr, sr in trees(k + 1, j):
                    yield (cl + cr + dims[i] * dims[k + 1] * dims[j + 1], '(' + sl + sr + ')')
    ts = list(trees(0, n - 1)); m = min(t[0] for t in ts)
    return sum(1 for t in ts if t[0] == m)
multi = 0
random.seed(230)
for _ in range(300):
    n = random.randint(2, 6)
    dims = [random.randint(1, 4) for _ in range(n + 1)]
    multi += all_optimal(dims) > 1
print('of 300 more random chains (n 2..6), several optimal parenthesisations existed in', multi)

# edge cases
assert solve([5, 7]) == [0, 'A0']
assert solve([3, 4, 5]) == [60, '(A0A1)']

# max size: 200 matrices (dims 201 long), recursion depth of paren() is at most n
print('recursion limit', sys.getrecursionlimit())
dims = [random.randint(1, 100) for _ in range(201)]
t0 = time.perf_counter(); res = solve(dims); t1 = time.perf_counter()
print('n=200 matrices: cost', res[0], '| string length', len(res[1]), '(sandbox timing %.1f s)' % (t1 - t0))
# all-ones dims: every tree costs n - 1, the smallest-k rule gives the right-deep tree, nesting depth 199 (below the default limit of 1000)
d2 = [1] * 201
res2 = solve(d2); print('n=200 all-ones dims: cost', res2[0], '| string starts', res2[1][:20])
assert res2[0] == 199 and res2[1].count('(') == 199
