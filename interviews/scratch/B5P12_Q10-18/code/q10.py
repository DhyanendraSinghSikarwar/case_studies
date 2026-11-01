import itertools
import random

random.seed(1210)

def solve_queens(n, trace=None):
    """Backtracking, one queen per row. cols / (r-c) / (r+c) sets give O(1) conflict tests.
    Returns (solutions as strings, number of recursive calls). Columns tried left to right => ascending order."""
    out, placed = [], []
    cs, d1, d2 = set(), set(), set()
    calls = 0
    def go(r):
        nonlocal calls
        calls += 1
        if r == n:
            out.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in placed])
            if trace is not None: trace.append('  ' * r + str(placed) + '  SOLUTION')
            return
        safe = [c for c in range(n) if c not in cs and (r - c) not in d1 and (r + c) not in d2]
        if trace is not None:
            trace.append('  ' * r + str(placed) + '  row %d: safe columns %s%s' % (r, safe, '  DEAD END' if not safe else ''))
        for c in safe:
            cs.add(c); d1.add(r - c); d2.add(r + c); placed.append(c)
            go(r + 1)
            placed.pop(); cs.discard(c); d1.discard(r - c); d2.discard(r + c)
    go(0)
    return out, calls

def unpruned_calls(n):
    """Same row-by-row tree but with NO conflict test: every column is tried in every row. Closed form: 1 + n + n^2 + ... + n^n."""
    return sum(n ** k for k in range(n + 1))

def unpruned_measured(n):
    """Count the calls of the unpruned row-by-row tree by actually running it (n <= 6)."""
    calls = 0
    def go(r):
        nonlocal calls
        calls += 1
        if r == n: return
        for _ in range(n): go(r + 1)
    go(0); return calls

def perm_tree_calls(n):
    """Calls of the 'one queen per row and per column' tree (no diagonal test): 1 + n + n(n-1) + ... + n!."""
    t, f = 0, 1
    for k in range(n + 1):
        t += f; f *= (n - k)
    return t

def brute(n):
    """Oracle: every permutation of columns (one queen per row AND per column), test diagonals pairwise.
    itertools.permutations yields lexicographic order, i.e. ascending column tuples."""
    res = []
    for p in itertools.permutations(range(n)):
        if all(abs(p[i] - p[j]) != j - i for i in range(n) for j in range(i + 1, n)):
            res.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in p])
    return res

# prompt examples
assert solve_queens(4)[0] == [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
assert solve_queens(1)[0] == [['Q']]
assert solve_queens(3)[0] == [] and solve_queens(2)[0] == []
print("3 prompt examples ok")

# decision tree for n = 4
tr = []
sols, calls = solve_queens(4, tr)
print("--- decision tree, n=4 ---")
print("\n".join(tr))
print("calls with pruning:", calls, "| unpruned row-by-row tree:", unpruned_calls(4))
for n in range(1, 7):
    assert unpruned_measured(n) == unpruned_calls(n), n
print("closed form 1+n+...+n^n matches a measured run for n=1..6")

# counts for n = 1..9 and node-visit comparison
print("--- counts and calls ---")
counts = []
for n in range(1, 10):
    s, c = solve_queens(n)
    counts.append(len(s))
    assert s == sorted(s, key=lambda sol: [row.index('Q') for row in sol])   # ascending by queen columns
    print("n=%d solutions=%d calls=%d columns-only=%d unpruned=%d" % (n, len(s), c, perm_tree_calls(n), unpruned_calls(n)))
assert counts == [1, 0, 0, 2, 10, 4, 40, 92, 352]
print("counts n=1..9:", counts)

# seeded random cross-check against the permutation oracle (n = 1..8)
for _ in range(300):
    n = random.randint(1, 8)
    assert solve_queens(n)[0] == brute(n), n
print("300 seeded random sizes (1..8) agree with the permutation oracle")
# edge asserts
assert solve_queens(2) == ([], 3)          # root + two row-0 placements; every row-1 try is attacked
assert all(len(s) == 4 and all(len(row) == 4 for row in s) for s in solve_queens(4)[0])
print("edge asserts ok")
