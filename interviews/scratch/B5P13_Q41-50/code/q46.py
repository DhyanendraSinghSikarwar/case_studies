import itertools, math, functools, random
random.seed(46)

# ---- one comparison counter shared by the sorters below
def merge_sort_cmps(perm):                    # top-down merge sort of Q15: split at n // 2, `<=` on ties
    c = 0
    def sort(x):
        nonlocal c
        if len(x) <= 1: return x
        m = len(x) // 2; L, R = sort(x[:m]), sort(x[m:]); out = []; i = j = 0
        while i < len(L) and j < len(R):
            c += 1
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(list(perm)); return c

def binary_insertion_cmps(perm):              # exactly the probe rule of the question
    a = []; c = 0
    for x in perm:
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2; c += 1
            if x < a[mid]: hi = mid
            else: lo = mid + 1
        a.insert(lo, x)
    assert a == sorted(perm)
    return c

# ---- optimal: exhaustive search over decision trees.
# State = the set of permutations (as indices) still consistent with the answers so far.
# can(S, L): can some comparison strategy of depth <= L identify the permutation inside S?
def optimal(n):
    perms = list(itertools.permutations(range(n)))
    pos = [[p.index(v) for v in range(n)] for p in perms]          # pos[k][v] = place of value v in permutation k
    pairs = list(itertools.combinations(range(n), 2))
    @functools.lru_cache(None)
    def can(S, L):
        if len(S) == 1: return True
        if L == 0 or len(S) > 2 ** L: return False                  # a tree of depth L has at most 2^L leaves
        for i, j in pairs:
            yes = frozenset(k for k in S if pos[k][i] < pos[k][j]); no = S - yes
            if yes and no and can(yes, L - 1) and can(no, L - 1): return True
        return False
    L = 0; full = frozenset(range(len(perms)))
    while not can(full, L): L += 1
    return L

def solve(n):
    perms = list(itertools.permutations(range(n)))
    return [math.ceil(math.log2(math.factorial(n))), max(merge_sort_cmps(p) for p in perms),
            max(binary_insertion_cmps(p) for p in perms), optimal(n)]

# ---- examples
assert solve(3) == [3, 3, 3, 3] and solve(4) == [5, 5, 5, 5] and solve(5) == [7, 8, 8, 7]
print('examples ok')

# ---- the computed table
print(' n  n!   info_bound  merge_worst  insertion_worst  optimal')
table = {}
for n in range(1, 6):
    table[n] = solve(n)
    print(f'{n:2} {math.factorial(n):4} {table[n][0]:10} {table[n][1]:12} {table[n][2]:16} {table[n][3]:8}')
assert [table[n][0] for n in range(1, 6)] == [0, 1, 3, 5, 7] and [table[n][3] for n in range(1, 6)] == [0, 1, 3, 5, 7]

# ---- cross-check 1: closed-form worst cases
W = {0: 0, 1: 0}
for n in range(2, 13): W[n] = W[n // 2] + W[n - n // 2] + n - 1                 # merge sort worst-case recurrence
for n in range(1, 6):
    assert table[n][1] == W[n]
    assert table[n][2] == sum(i.bit_length() for i in range(1, n))              # inserting into a prefix of i items needs ceil(log2(i+1)) = i.bit_length() probes
    assert table[n][3] >= table[n][0]                                           # nobody beats the information bound
print('closed forms agree: merge worst W(n) = W(n//2) + W(n - n//2) + n - 1, binary insertion worst = sum of bit_length(i), i < n')

# ---- cross-check 2: a real algorithm that reaches the optimum for n = 5 (Ford-Johnson merge insertion, editor-implemented)
def ford_johnson(perm):
    c = 0
    def less(x, y):
        nonlocal c; c += 1; return x < y
    def fj(items):
        n = len(items)
        if n <= 1: return list(items)
        big, small = [], {}
        for i in range(0, n - 1, 2):
            x, y = items[i], items[i + 1]
            if less(x, y): x, y = y, x               # x is the larger of the pair
            big.append(x); small[x] = y
        rest = items[-1] if n % 2 else None
        chain = fj(big)                              # sort the larger elements recursively
        main = [small[chain[0]]] + chain             # b1 < a1 < a2 ...
        pend = [small[a] for a in chain[1:]] + ([rest] if rest is not None else [])   # b2, b3, ...
        bound = {small[a]: a for a in chain[1:]}      # b_j must be inserted below its partner a_j
        done, t_prev, k = 0, 1, 1
        # Jacobsthal numbers 1, 3, 5, 11, 21 ... give the insertion order: b_t, b_{t-1}, ..., b_{t_prev + 1}
        jac = [1, 3, 5, 11, 21, 43]
        order = []; prev = 1
        for t in jac[1:]:
            t = min(t, len(pend) + 1)
            order += list(range(t, prev, -1))
            prev = t
            if t >= len(pend) + 1: break
        for j in order:                              # j is 2-based: pend[j - 2] is b_j
            b = pend[j - 2]
            hi = main.index(bound[b]) if b in bound else len(main)
            lo = 0
            while lo < hi:
                mid = (lo + hi) // 2
                if less(b, main[mid]): hi = mid
                else: lo = mid + 1
            main.insert(lo, b)
        return main
    out = fj(list(perm)); assert out == sorted(perm), (perm, out)
    return c
fj_worst = {n: max(ford_johnson(p) for p in itertools.permutations(range(n))) for n in range(1, 8)}
print('Ford-Johnson merge insertion, worst case over all permutations, n = 1..7:', [fj_worst[n] for n in range(1, 8)])
assert [fj_worst[n] for n in range(1, 6)] == [0, 1, 3, 5, 7]
print('so seven comparisons really do sort 5 items (matches the exhaustive optimum 7), while merge sort and binary insertion need 8')

# ---- information bound for larger n (formula only; no search is claimed beyond n = 5)
print('n: info_bound / merge_worst (closed forms) :', {n: (math.ceil(math.log2(math.factorial(n))), W[n]) for n in (6, 8, 10, 12)})

# ---- edge asserts
assert solve(1) == [0, 0, 0, 0] and solve(2) == [1, 1, 1, 1]
assert math.factorial(5) == 120 and 2 ** 6 < 120 <= 2 ** 7
print('edge asserts ok')
