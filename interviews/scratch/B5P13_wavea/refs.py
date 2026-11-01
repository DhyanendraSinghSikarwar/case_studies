# Reference solutions (S) and independent oracles (B) for Book 5 Part 13 (prefix sums, matrices, math, randomised algorithms, sorting internals).
import itertools, functools, sys, math, random, collections, bisect, copy
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
sys.setrecursionlimit(1000)
S = {}; B = {}
def reg(d, name):
    def deco(f): d[name] = f; return f
    return deco
MOD = 10**9 + 7

# ============ prefix sums and difference arrays
@reg(S, 'range_sum_1d')
def _(nums, queries):
    pre = [0]
    for v in nums: pre.append(pre[-1] + v)
    return [pre[r + 1] - pre[l] for l, r in queries]
@reg(B, 'range_sum_1d')
def _(nums, queries): return [sum(nums[l:r + 1]) for l, r in queries]

@reg(S, 'range_add')
def _(n, updates):
    d = [0] * (n + 1)
    for l, r, v in updates: d[l] += v; d[r + 1] -= v
    out = []; run = 0
    for i in range(n): run += d[i]; out.append(run)
    return out
@reg(B, 'range_add')
def _(n, updates):
    a = [0] * n
    for l, r, v in updates:
        for i in range(l, r + 1): a[i] += v
    return a

@reg(S, 'range_sum_2d')
def _(matrix, queries):
    m, n = len(matrix), len(matrix[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n): P[i + 1][j + 1] = matrix[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    return [P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1] for r1, c1, r2, c2 in queries]
@reg(B, 'range_sum_2d')
def _(matrix, queries): return [sum(matrix[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1)) for r1, c1, r2, c2 in queries]

@reg(S, 'pivot_index')
def _(nums):
    run = list(itertools.accumulate(nums)); total = run[-1]; piv = -1
    for i in range(len(nums)):
        left = run[i] - nums[i]
        if left == total - run[i]: piv = i; break
    return [piv, run]
@reg(B, 'pivot_index')
def _(nums):
    run = []; s = 0
    for v in nums: s += v; run.append(s)
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1:]): return [i, run]
    return [-1, run]

@reg(S, 'car_pooling')
def _(capacity, trips):
    d = [0] * 1002
    for p, a, b in trips: d[a] += p; d[b] -= p
    load = 0; peak = 0; first = 0
    for x in range(1001):
        load += d[x]
        if load > peak: peak = load; first = x
    return [peak <= capacity, peak, first]
@reg(B, 'car_pooling')
def _(capacity, trips):
    loads = [sum(p for p, a, b in trips if a <= x < b) for x in range(1001)]
    peak = max(loads); first = loads.index(peak)
    return [all(l <= capacity for l in loads), peak, first]

@reg(S, 'matrix_block_sum')
def _(mat, k):
    m, n = len(mat), len(mat[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n): P[i + 1][j + 1] = mat[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            r1, c1, r2, c2 = max(0, i - k), max(0, j - k), min(m - 1, i + k), min(n - 1, j + k)
            row.append(P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1])
        out.append(row)
    return out
@reg(B, 'matrix_block_sum')
def _(mat, k):
    m, n = len(mat), len(mat[0])
    return [[sum(mat[r][c] for r in range(m) for c in range(n) if abs(r - i) <= k and abs(c - j) <= k) for j in range(n)] for i in range(m)]

@reg(S, 'range_sum_2d_mutable')
def _(matrix, ops):
    rows = [list(itertools.accumulate(r, initial=0)) for r in matrix]; mat = [list(r) for r in matrix]; out = []
    for op in ops:
        if op[0] == 'update':
            _, r, c, v = op; mat[r][c] = v; rows[r] = list(itertools.accumulate(mat[r], initial=0)); out.append(None)
        else:
            _, r1, c1, r2, c2 = op; out.append(sum(rows[r][c2 + 1] - rows[r][c1] for r in range(r1, r2 + 1)))
    return out
@reg(B, 'range_sum_2d_mutable')
def _(matrix, ops):
    mat = [list(r) for r in matrix]; out = []
    for op in ops:
        if op[0] == 'update': mat[op[1]][op[2]] = op[3]; out.append(None)
        else: out.append(sum(mat[i][j] for i in range(op[1], op[3] + 1) for j in range(op[2], op[4] + 1)))
    return out

@reg(S, 'increment_submatrices')
def _(n, queries):
    d = [[0] * (n + 1) for _ in range(n + 1)]
    for r1, c1, r2, c2 in queries:
        d[r1][c1] += 1; d[r1][c2 + 1] -= 1; d[r2 + 1][c1] -= 1; d[r2 + 1][c2 + 1] += 1
    for i in range(n + 1):
        for j in range(1, n + 1): d[i][j] += d[i][j - 1]
    for j in range(n + 1):
        for i in range(1, n + 1): d[i][j] += d[i - 1][j]
    return [row[:n] for row in d[:n]]
@reg(B, 'increment_submatrices')
def _(n, queries):
    a = [[0] * n for _ in range(n)]
    for r1, c1, r2, c2 in queries:
        for i in range(r1, r2 + 1):
            for j in range(c1, c2 + 1): a[i][j] += 1
    return a

# ============ merge sort machinery (top-down, split at len // 2, take left when left.key <= right.key)
def msort(recs, cnt):
    n = len(recs)
    if n <= 1: return list(recs)
    mid = n // 2; L = msort(recs[:mid], cnt); R = msort(recs[mid:], cnt)
    out = []; i = j = 0
    while i < len(L) and j < len(R):
        cnt[0] += 1
        if L[i][0] <= R[j][0]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    out.extend(L[i:]); out.extend(R[j:]); return out
@reg(S, 'merge_sort')
def _(records):
    cnt = [0]; out = msort([list(r) for r in records], cnt); return [out, cnt[0]]
@reg(B, 'merge_sort')
def _(records):
    # bottom-up index merge with the same split points reproduced by recursion on index ranges
    recs = [list(r) for r in records]
    def go(lo, hi):
        if hi - lo <= 1: return recs[lo:hi], 0
        mid = lo + (hi - lo) // 2
        (L, a), (R, b) = go(lo, mid), go(mid, hi); c = a + b; out = []
        while L and R:
            c += 1
            out.append(L.pop(0) if L[0][0] <= R[0][0] else R.pop(0))
        return out + L + R, c
    s, c = go(0, len(recs)); assert s == sorted(recs, key=lambda r: r[0]); return [s, c]

@reg(S, 'count_inversions')
def _(nums):
    a = list(nums); buf = [0] * len(a)
    def sort(lo, hi):
        if hi - lo <= 1: return 0
        mid = (lo + hi) // 2; inv = sort(lo, mid) + sort(mid, hi); i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if a[i] <= a[j]: buf[k] = a[i]; i += 1
            else: buf[k] = a[j]; j += 1; inv += mid - i
            k += 1
        while i < mid: buf[k] = a[i]; i += 1; k += 1
        while j < hi: buf[k] = a[j]; j += 1; k += 1
        a[lo:hi] = buf[lo:hi]; return inv
    return sort(0, len(a))
@reg(B, 'count_inversions')
def _(nums): return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > nums[j])

@reg(S, 'count_range_sum')
def _(nums, lo, hi):
    pre = [0] + list(itertools.accumulate(nums)); cnt = 0
    def sort(a):
        nonlocal cnt
        if len(a) <= 1: return a
        mid = len(a) // 2; L = sort(a[:mid]); R = sort(a[mid:]); x = y = 0
        for v in L:
            while x < len(R) and R[x] - v < lo: x += 1
            while y < len(R) and R[y] - v <= hi: y += 1
            cnt += y - x
        return sorted_merge(L, R)
    def sorted_merge(L, R):
        out = []; i = j = 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(pre); return cnt
@reg(B, 'count_range_sum')
def _(nums, lo, hi):
    c = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if lo <= s <= hi: c += 1
    return c

# ============ matrices
@reg(S, 'rotate_image')
def _(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n): matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix: row.reverse()
    return matrix
@reg(B, 'rotate_image')
def _(matrix): return [list(r) for r in zip(*matrix[::-1])]

@reg(S, 'spiral_matrix')
def _(matrix):
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1; out = []
    while top <= bottom and left <= right:
        for j in range(left, right + 1): out.append(matrix[top][j])
        for i in range(top + 1, bottom + 1): out.append(matrix[i][right])
        if top < bottom and left < right:
            for j in range(right - 1, left - 1, -1): out.append(matrix[bottom][j])
            for i in range(bottom - 1, top, -1): out.append(matrix[i][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out
@reg(B, 'spiral_matrix')
def _(matrix):
    m, n = len(matrix), len(matrix[0]); seen = set(); i = j = 0; di, dj = 0, 1; out = []
    for _ in range(m * n):
        out.append(matrix[i][j]); seen.add((i, j))
        ni, nj = i + di, j + dj
        if not (0 <= ni < m and 0 <= nj < n and (ni, nj) not in seen): di, dj = dj, -di; ni, nj = i + di, j + dj
        i, j = ni, nj
    return out

@reg(S, 'set_matrix_zeroes')
def _(matrix):
    m, n = len(matrix), len(matrix[0])
    row0 = any(matrix[0][j] == 0 for j in range(n)); col0 = any(matrix[i][0] == 0 for i in range(m))
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0: matrix[i][0] = 0; matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0: matrix[i][j] = 0
    if row0:
        for j in range(n): matrix[0][j] = 0
    if col0:
        for i in range(m): matrix[i][0] = 0
    return matrix
def naive_markers(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0: matrix[i][0] = 0; matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0: matrix[i][j] = 0
    if matrix[0][0] == 0:
        for j in range(n): matrix[0][j] = 0
        for i in range(m): matrix[i][0] = 0
    return matrix
@reg(B, 'set_matrix_zeroes')
def _(matrix):
    rs = {i for i, r in enumerate(matrix) if 0 in r}; cs = {j for r in matrix for j, v in enumerate(r) if v == 0}
    return [[0 if i in rs or j in cs else v for j, v in enumerate(r)] for i, r in enumerate(matrix)]

@reg(S, 'game_of_life')
def _(board, generations):
    m, n = len(board), len(board[0])
    for _ in range(generations):
        for i in range(m):
            for j in range(n):
                live = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n: live += board[i + di][j + dj] & 1
                if live == 3 or (board[i][j] & 1 and live == 2): board[i][j] |= 2
        for i in range(m):
            for j in range(n): board[i][j] >>= 1
    return board
@reg(B, 'game_of_life')
def _(board, generations):
    cells = {(i, j) for i, r in enumerate(board) for j, v in enumerate(r) if v}; m, n = len(board), len(board[0])
    for _ in range(generations):
        cnt = collections.Counter((i + di, j + dj) for i, j in cells for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di or dj))
        cells = {p for p, c in cnt.items() if 0 <= p[0] < m and 0 <= p[1] < n and (c == 3 or (c == 2 and p in cells))}
    return [[1 if (i, j) in cells else 0 for j in range(n)] for i in range(m)]

@reg(S, 'diagonal_traverse')
def _(mat):
    m, n = len(mat), len(mat[0]); i = j = 0; up = True; out = []
    for _ in range(m * n):
        out.append(mat[i][j])
        if up:
            if j == n - 1: i += 1; up = False
            elif i == 0: j += 1; up = False
            else: i -= 1; j += 1
        else:
            if i == m - 1: j += 1; up = True
            elif j == 0: i += 1; up = True
            else: i += 1; j -= 1
    return out
@reg(B, 'diagonal_traverse')
def _(mat):
    m, n = len(mat), len(mat[0]); out = []
    for s in range(m + n - 1):
        diag = [mat[i][s - i] for i in range(m) if 0 <= s - i < n]  # top row first = going down-left order
        out.extend(diag[::-1] if s % 2 == 0 else diag)
    return out

@reg(S, 'matrix_layer_rotation')
def _(matrix, r):
    m, n = len(matrix), len(matrix[0])
    for l in range(min(m, n) // 2):
        t, b, lf, rt = l, m - 1 - l, l, n - 1 - l
        pos = [(t, j) for j in range(lf, rt + 1)] + [(i, rt) for i in range(t + 1, b + 1)] + [(b, j) for j in range(rt - 1, lf - 1, -1)] + [(i, lf) for i in range(b - 1, t, -1)]
        L = len(pos); vals = [matrix[i][j] for i, j in pos]; s = r % L
        for idx, (i, j) in enumerate(pos): matrix[i][j] = vals[(idx + s) % L]
    return matrix
@reg(B, 'matrix_layer_rotation')
def _(matrix, r):
    m, n = len(matrix), len(matrix[0]); out = [list(row) for row in matrix]
    for l in range(min(m, n) // 2):
        t, b, lf, rt = l, m - 1 - l, l, n - 1 - l
        cells = [(t, j) for j in range(lf, rt + 1)] + [(i, rt) for i in range(t + 1, b + 1)] + [(b, j) for j in range(rt - 1, lf - 1, -1)] + [(i, lf) for i in range(b - 1, t, -1)]
        dq = collections.deque(out[i][j] for i, j in cells); dq.rotate(-(r % len(cells)))
        for (i, j), v in zip(cells, dq): out[i][j] = v
    return out

# ============ math
def euclid(a, b):
    steps = 0
    while b: a, b = b, a % b; steps += 1
    return a, steps
@reg(S, 'gcd_lcm')
def _(a, b, nums):
    g, steps = euclid(a, b); l = a // g * b; ga = 0; la = 1
    for v in nums:
        ga = euclid(ga, v)[0]; la = la // euclid(la, v)[0] * v
    return [g, l, steps, ga, la]
@reg(B, 'gcd_lcm')
def _(a, b, nums):
    def rsteps(x, y): return 0 if y == 0 else 1 + rsteps(y, x % y)
    return [math.gcd(a, b), math.lcm(a, b), rsteps(a, b), math.gcd(*nums), math.lcm(*nums)]

def vfact(n, p):
    c = 0
    while n: n //= p; c += n
    return c
def factor_small(b):
    f = {}; d = 2
    while d * d <= b:
        while b % d == 0: f[d] = f.get(d, 0) + 1; b //= d
        d += 1
    if b > 1: f[b] = f.get(b, 0) + 1
    return f
@reg(S, 'trailing_zeroes')
def _(n, base):
    return [min(vfact(n, p) // e for p, e in factor_small(10).items()), min(vfact(n, p) // e for p, e in factor_small(base).items())]
@reg(B, 'trailing_zeroes')
def _(n, base):
    f = math.factorial(n)
    def tz(x, b):
        c = 0
        while x % b == 0: x //= b; c += 1
        return c
    return [tz(f, 10), tz(f, base)]

@reg(S, 'count_primes')
def _(n):
    if n < 3: return [0, 0]
    sv = bytearray([1]) * n; sv[0] = sv[1] = 0; marks = 0; p = 2
    while p * p < n:
        if sv[p]:
            cnt = len(range(p * p, n, p)); marks += cnt; sv[p * p::p] = bytes(cnt)
        p += 1
    return [sum(sv), marks]
@reg(B, 'count_primes')
def _(n):
    isp = lambda x: x >= 2 and all(x % d for d in range(2, math.isqrt(x) + 1))
    return [sum(1 for x in range(n) if isp(x)), sum(len(range(p * p, n, p)) for p in range(2, n) if p * p < n and isp(p))]

@reg(S, 'pow_fast')
def _(x, n):
    e = abs(n); res = 1; base = x; mult = 0
    while e:
        if e & 1: res *= base; mult += 1
        e >>= 1
        if e: base *= base; mult += 1
    f = Fraction(1, res) if n < 0 else Fraction(res)
    return [f.numerator, f.denominator, mult]
@reg(B, 'pow_fast')
def _(x, n):
    f = Fraction(x) ** n; e = abs(n)
    return [f.numerator, f.denominator, bin(e).count('1') + e.bit_length() - 1 if e else 0]

def to_int32(v): return ((v + 2**31) % 2**32) - 2**31
@reg(S, 'reverse_int32')
def _(x):
    sign = -1 if x < 0 else 1; v = abs(x); r = 0
    while v: r = r * 10 + v % 10; v //= 10
    r *= sign
    return [r if -2**31 <= r <= 2**31 - 1 else 0, to_int32(r)]
@reg(B, 'reverse_int32')
def _(x):
    import ctypes
    s = str(x); r = int('-' + s[:0:-1]) if x < 0 else int(s[::-1])
    return [r if ctypes.c_int32(r).value == r else 0, ctypes.c_int32(r).value]

@reg(S, 'happy_number')
def _(n):
    f = lambda v: sum(int(c) ** 2 for c in str(v))
    slow, fast = n, f(n)
    while fast != 1 and slow != fast: slow = f(slow); fast = f(f(fast))
    # cycle length: from a point inside the cycle
    x = fast; c = 1; y = f(x)
    while y != x: y = f(y); c += 1
    steps = -1
    if fast == 1 or n == 1:
        steps = 0; v = n
        while v != 1: v = f(v); steps += 1
    return [steps >= 0, steps, c]
@reg(B, 'happy_number')
def _(n):
    seen = {}; v = n; i = 0
    while v not in seen:
        seen[v] = i; i += 1
        v = sum(int(c) ** 2 for c in str(v))
    cyc = i - seen[v]
    return [v == 1 or (1 in seen), seen.get(1, -1), cyc]

def col_num(t):
    r = 0
    for ch in t: r = r * 26 + ord(ch) - 64
    return r
def col_title(n):
    out = []
    while n: n, r = divmod(n - 1, 26); out.append(chr(65 + r))
    return ''.join(reversed(out))
@reg(S, 'excel_column')
def _(title, number): return [col_num(title), col_title(number)]
@reg(B, 'excel_column')
def _(title, number):
    num = sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(title)))
    k = number - 1; L = 1
    while k >= 26 ** L: k -= 26 ** L; L += 1
    digs = []
    for _ in range(L): k, r = divmod(k, 26); digs.append(chr(65 + r))
    return [num, ''.join(reversed(digs))]

@reg(S, 'pascal_triangle')
def _(num_rows, row_index):
    tri = []
    for i in range(num_rows):
        row = [1] * (i + 1)
        for j in range(1, i): row[j] = tri[i - 1][j - 1] + tri[i - 1][j]
        tri.append(row)
    row = [1] * (row_index + 1)
    for i in range(1, row_index + 1):
        for j in range(i - 1, 0, -1): row[j] += row[j - 1]
    return [tri, row]
@reg(B, 'pascal_triangle')
def _(num_rows, row_index): return [[[math.comb(i, j) for j in range(i + 1)] for i in range(num_rows)], [math.comb(row_index, j) for j in range(row_index + 1)]]

@reg(S, 'round_half_even')
def _(values):
    out = []
    for s in values:
        f = float(s); d = Decimal(s)
        out.append([round(f), int(d.to_integral_value(ROUND_HALF_UP)), repr(round(f, 2)), str(d.quantize(Decimal('0.01'), ROUND_HALF_EVEN))])
    return out
@reg(B, 'round_half_even')
def _(values):
    out = []
    for s in values:
        q = Fraction(s); f = float(s); ex = Fraction(f)
        def he(x):
            fl = math.floor(x); d = x - fl
            return fl if d < Fraction(1, 2) else fl + 1 if d > Fraction(1, 2) else (fl if fl % 2 == 0 else fl + 1)
        hu = (1 if q >= 0 else -1) * math.floor(abs(q) + Fraction(1, 2))
        r2 = float(he(ex * 100) / Fraction(100))
        h2 = he(q * 100); sign = '-' if h2 < 0 else ''; a = abs(h2)
        out.append([he(ex), hu, repr(r2), f"{sign}{a // 100}.{a % 100:02d}"])
    return out

@reg(S, 'fraction_decimal')
def _(numerator, denominator):
    if numerator == 0: return '0'
    sign = '-' if (numerator < 0) != (denominator < 0) else ''
    n, d = abs(numerator), abs(denominator); ip, rem = divmod(n, d)
    if rem == 0: return sign + str(ip)
    digits = []; seen = {}
    while rem and rem not in seen:
        seen[rem] = len(digits); rem *= 10; digits.append(str(rem // d)); rem %= d
    if rem == 0: return sign + str(ip) + '.' + ''.join(digits)
    k = seen[rem]; return sign + str(ip) + '.' + ''.join(digits[:k]) + '(' + ''.join(digits[k:]) + ')'
@reg(B, 'fraction_decimal')
def _(numerator, denominator):
    if numerator == 0: return '0'
    fr = Fraction(abs(numerator), abs(denominator)); sign = '-' if (numerator < 0) != (denominator < 0) else ''
    ip = fr.numerator // fr.denominator; rem = fr.numerator % fr.denominator; d = fr.denominator
    if rem == 0: return sign + str(ip)
    a = b = 0; rest = d
    while rest % 2 == 0: rest //= 2; a += 1
    while rest % 5 == 0: rest //= 5; b += 1
    pre = max(a, b); period = 0
    if rest > 1:
        period = 1; x = 10 % rest
        while x != 1: x = x * 10 % rest; period += 1
    total = pre + period; old = sys.get_int_max_str_digits(); sys.set_int_max_str_digits(0)
    try: D = str(rem * 10**total // d).zfill(total)
    finally: sys.set_int_max_str_digits(old)
    return sign + str(ip) + '.' + D[:pre] + ('(' + D[pre:] + ')' if period else '')

@reg(S, 'prime_factors')
def _(nums):
    out = []
    for n in nums:
        m = n; d = 2; steps = 0; f = []
        while d * d <= m:
            steps += 1
            if m % d == 0:
                e = 0
                while m % d == 0: m //= d; e += 1
                f.append([d, e])
            d += 1
        if m > 1: f.append([m, 1])
        div = 1
        for p, e in f: div *= e + 1
        out.append([f, div, steps])
    return out
@reg(B, 'prime_factors')
def _(nums):
    out = []
    for n in nums:
        f = []; m = n; d = 2; steps = 0
        while True:
            if d * d > m: break
            steps += 1
            if m % d == 0:
                e = 0
                while m % d == 0: m //= d; e += 1
                f.append([d, e])
            d += 1
        if m > 1: f.append([m, 1])
        prod = 1
        for p, e in f: prod *= p ** e
        assert prod == n
        divs = 1
        for p, e in f: divs *= e + 1
        if n <= 20000: assert divs == sum(1 for k in range(1, n + 1) if n % k == 0)
        out.append([f, divs, steps])
    return out

@reg(S, 'modular_inverse')
def _(a, m, queries):
    try: inv = pow(a, -1, m)
    except ValueError: inv = None
    mx = max([q[0] for q in queries], default=0); fact = [1] * (mx + 1)
    for i in range(1, mx + 1): fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (mx + 1); inv_fact[mx] = pow(fact[mx], -1, MOD)
    for i in range(mx, 0, -1): inv_fact[i - 1] = inv_fact[i] * i % MOD
    return [inv, [fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD for n, r in queries]]
@reg(B, 'modular_inverse')
def _(a, m, queries):
    inv = next((x for x in range(m) if a * x % m == 1), None)
    return [inv, [math.comb(n, r) % MOD for n, r in queries]]

@reg(S, 'float_pitfalls')
def _(prices, target):
    fl = [float(p) for p in prices]; s = 0.0
    for v in fl: s += v
    ex = sum(Fraction(Decimal(p)) for p in prices)
    return [repr(s), str(ex), s == float(target), math.isclose(s, float(target)), repr(math.fsum(fl))]
@reg(B, 'float_pitfalls')
def _(prices, target):
    s = 0.0
    for p in prices: s = s + float(p)
    tot = Fraction(0)
    for p in prices:
        sign = -1 if p.startswith('-') else 1; q = p.lstrip('-'); w, _, fr = q.partition('.')
        tot += sign * Fraction(int(w + fr), 10 ** len(fr))
    exact = sum(Fraction(float(p)) for p in prices)
    fs = float(exact)   # math.fsum is the correctly rounded exact sum of the doubles
    return [repr(s), str(tot), s == float(target), abs(s - float(target)) <= 1e-9 * max(abs(s), abs(float(target))), repr(fs)]

@reg(S, 'bigint_fib')
def _(n):
    def fd(k):
        if k == 0: return 0, 1
        a, b = fd(k // 2); c = a * (2 * b - a); d = a * a + b * b
        return (d, c + d) if k & 1 else (c, d)
    f = fd(n)[0]; old = sys.get_int_max_str_digits(); sys.set_int_max_str_digits(0)
    try: s = str(f)
    finally: sys.set_int_max_str_digits(old)
    return [f % MOD, len(s), s[:5]]
@reg(B, 'bigint_fib')
def _(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    chunks = []; x = a
    while x: x, r = divmod(x, 10**500); chunks.append(r)
    s = str(chunks[-1]) + ''.join(str(c).zfill(500) for c in reversed(chunks[:-1])) if chunks else '0'
    return [a % MOD, len(s), s[:5]]

# ============ randomised algorithms (exhaustive over all random-choice sequences)
def fy_apply(n, choices):
    a = list(range(n))
    for k, i in enumerate(range(n - 1, 0, -1)): j = choices[k]; a[i], a[j] = a[j], a[i]
    return a
@reg(S, 'fisher_yates')
def _(n, choices):
    cnt = collections.Counter(tuple(fy_apply(n, c)) for c in itertools.product(*[range(i + 1) for i in range(n - 1, 0, -1)]))
    return [fy_apply(n, choices), sum(cnt.values()), len(cnt), min(cnt.values()), max(cnt.values())]
@reg(B, 'fisher_yates')
def _(n, choices):
    def rec(a, i, cs, acc):  # acc: Counter of final perms
        if i == 0: acc[tuple(a)] += 1; return
        for j in range(i + 1):
            b = list(a); b[i], b[j] = b[j], b[i]; rec(b, i - 1, cs, acc)
    acc = collections.Counter(); rec(list(range(n)), n - 1, None, acc)
    a = list(range(n)); i = n - 1
    for c in choices: a[i], a[c] = a[c], a[i]; i -= 1
    return [a, sum(acc.values()), len(acc), min(acc.values()), max(acc.values())]

@reg(S, 'biased_shuffle')
def _(n):
    cnt = collections.Counter()
    for js in itertools.product(range(n), repeat=n):
        a = list(range(n))
        for i, j in enumerate(js): a[i], a[j] = a[j], a[i]
        cnt[tuple(a)] += 1
    hi, lo = max(cnt.values()), min(cnt.values())
    return [n ** n, len(cnt), lo, hi, list(min(p for p, c in cnt.items() if c == hi)), list(min(p for p, c in cnt.items() if c == lo))]
@reg(B, 'biased_shuffle')
def _(n):
    cnt = collections.Counter()
    def rec(a, i):
        if i == n: cnt[tuple(a)] += 1; return
        for j in range(n):
            b = a[:]; b[i], b[j] = b[j], b[i]; rec(b, i + 1)
    rec(list(range(n)), 0)
    hi, lo = max(cnt.values()), min(cnt.values())
    return [sum(cnt.values()), len(cnt), lo, hi, list(sorted(p for p in cnt if cnt[p] == hi)[0]), list(sorted(p for p in cnt if cnt[p] == lo)[0])]

@reg(S, 'reservoir_k1')
def _(stream, draws):
    held = stream[0]
    for x, d in zip(stream[1:], draws):
        if d == 0: held = x
    n = len(stream); counts = [1]; total = 1
    # DP over items: counts[t] = sequences in which position t is held after the current item
    for i in range(2, n + 1):
        counts = [c * (i - 1) for c in counts] + [total]; total *= i
    return [held, counts, total]
@reg(B, 'reservoir_k1')
def _(stream, draws):
    n = len(stream); cnt = [0] * n; tot = 0
    for ds in itertools.product(*[range(i) for i in range(2, n + 1)]):
        pos = 0
        for i, d in enumerate(ds, 1):
            if d == 0: pos = i
        cnt[pos] += 1; tot += 1
    pos = 0
    for i, d in enumerate(draws, 1):
        if d == 0: pos = i
    return [stream[pos], cnt, tot]

@reg(S, 'reservoir_k')
def _(stream, k, draws):
    n = len(stream); res = list(stream[:k])
    for i, d in zip(range(k + 1, n + 1), draws):
        if d < k: res[d] = stream[i - 1]
    cnt = [0] * n; subs = collections.Counter(); tot = 0
    for ds in itertools.product(*[range(i) for i in range(k + 1, n + 1)]):
        r = list(range(k))
        for i, d in zip(range(k + 1, n + 1), ds):
            if d < k: r[d] = i - 1
        tot += 1; subs[frozenset(r)] += 1
        for p in r: cnt[p] += 1
    return [res, cnt, tot, len(subs), min(subs.values()), max(subs.values())]
@reg(B, 'reservoir_k')
def _(stream, k, draws):
    n = len(stream); res = list(stream[:k])
    for idx, d in enumerate(draws):
        if d < k: res[d] = stream[k + idx]
    def rec(i, r, acc):
        if i > n: acc.append(tuple(r)); return
        for d in range(i):
            r2 = list(r)
            if d < k: r2[d] = i - 1
            rec(i + 1, r2, acc)
    acc = []; rec(k + 1, list(range(k)), acc)
    cnt = [sum(p in r for r in acc) for p in range(n)]; subs = collections.Counter(frozenset(r) for r in acc)
    return [res, cnt, len(acc), len(subs), min(subs.values()), max(subs.values())]

@reg(S, 'weighted_pick')
def _(w, rs):
    pre = list(itertools.accumulate(w)); total = pre[-1]
    cnt = [0] * len(w)
    for r in range(total): cnt[bisect.bisect_right(pre, r)] += 1
    return [[bisect.bisect_right(pre, r) for r in rs], cnt]
@reg(B, 'weighted_pick')
def _(w, rs):
    def pick(r):
        for i, x in enumerate(w):
            if r < x: return i
            r -= x
    total = sum(w); cnt = [0] * len(w)
    for r in range(total): cnt[pick(r)] += 1
    return [[pick(r) for r in rs], cnt]

@reg(S, 'rejection_sampling')
def _(m, t, stream):
    lim = (m * m // t) * t; out = []; used = 0
    for k in range(0, len(stream) - 1, 2):
        x = m * (stream[k] - 1) + (stream[k + 1] - 1); used += 2
        if x < lim: out.append(x % t + 1)
    cnt = [0] * t
    for a in range(1, m + 1):
        for b in range(1, m + 1):
            x = m * (a - 1) + (b - 1)
            if x < lim: cnt[x % t] += 1
    return [out, used, cnt, str(Fraction(2 * m * m, lim))]
@reg(B, 'rejection_sampling')
def _(m, t, stream):
    pairs = list(zip(stream[0::2], stream[1::2])); out = []
    for a, b in pairs:
        x = (a - 1) * m + b - 1
        if x < t * (m * m // t): out.append(x % t + 1)
    cnt = collections.Counter(((a - 1) * m + b - 1) % t for a in range(1, m + 1) for b in range(1, m + 1) if (a - 1) * m + b - 1 < t * (m * m // t))
    q = Fraction(t * (m * m // t), m * m)
    return [out, 2 * len(pairs), [cnt[i] for i in range(t)], str(2 / q)]

@reg(S, 'pick_index_target')
def _(nums, target, draws):
    occ = [i for i, v in enumerate(nums) if v == target]; held = occ[0]
    for j, i in enumerate(occ):
        if draws[j] == 0: held = i
    c = len(occ); counts = [1]; total = 1
    for j in range(2, c + 1): counts = [x * (j - 1) for x in counts] + [total]; total *= j
    return [held, counts, total]
@reg(B, 'pick_index_target')
def _(nums, target, draws):
    occ = [i for i, v in enumerate(nums) if v == target]; c = len(occ); cnt = [0] * c; tot = 0
    for ds in itertools.product(*[range(j + 1) for j in range(c)]):
        last = max(j for j, d in enumerate(ds) if d == 0); cnt[last] += 1; tot += 1
    last = max(j for j, d in enumerate(draws) if d == 0)
    return [occ[last], cnt, tot]

# ============ sorting internals
def lomuto_sort(a, want_depth=True):
    a = list(a); cmps = 0; depth = 0; stack = [(0, len(a) - 1, 1)] if len(a) > 1 else []
    while stack:
        lo, hi, d = stack.pop(); depth = max(depth, d); p = a[hi]; i = lo
        for j in range(lo, hi):
            cmps += 1
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        if i + 1 < hi: stack.append((i + 1, hi, d + 1))
        if lo < i - 1: stack.append((lo, i - 1, d + 1))
    return a, cmps, depth
@reg(S, 'quicksort_iter')
def _(nums):
    a, c, d = lomuto_sort(nums); return [a, c, d]
@reg(B, 'quicksort_iter')
def _(nums):
    a = list(nums); cmps = 0; depth = 0
    def rec(lo, hi, d):
        nonlocal cmps, depth
        if lo >= hi: return
        depth = max(depth, d); p = a[hi]; i = lo
        for j in range(lo, hi):
            cmps += 1
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]; rec(lo, i - 1, d + 1); rec(i + 1, hi, d + 1)
    rec(0, len(a) - 1, 1); return [a, cmps, depth]

def three_way_sort(a):
    a = list(a); cmps = 0; stack = [(0, len(a) - 1)] if len(a) > 1 else []
    while stack:
        lo, hi = stack.pop(); p = a[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            cmps += 1
            if a[i] < p: a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > p: a[i], a[gt] = a[gt], a[i]; gt -= 1
            else: i += 1
        if lt - 1 > lo: stack.append((lo, lt - 1))
        if gt + 1 < hi: stack.append((gt + 1, hi))
    return a, cmps
@reg(S, 'three_way')
def _(nums):
    s, c3 = three_way_sort(nums); _, cl, _ = lomuto_sort(nums); return [s, cl, c3]
@reg(B, 'three_way')
def _(nums):
    cmps = [0, 0]; a = list(nums)
    def rec3(lo, hi):
        if lo >= hi: return
        p = a[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            cmps[1] += 1
            if a[i] < p: a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > p: a[i], a[gt] = a[gt], a[i]; gt -= 1
            else: i += 1
        rec3(lo, lt - 1); rec3(gt + 1, hi)
    rec3(0, len(a) - 1)
    b = list(nums)
    def recl(lo, hi):
        if lo >= hi: return
        p = b[hi]; i = lo
        for j in range(lo, hi):
            cmps[0] += 1
            if b[j] < p: b[i], b[j] = b[j], b[i]; i += 1
        b[i], b[hi] = b[hi], b[i]; recl(lo, i - 1); recl(i + 1, hi)
    recl(0, len(b) - 1); return [a, cmps[0], cmps[1]]

def hoare(a):
    a = list(a); lo, hi = 0, len(a) - 1; pivot = a[lo]; i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot: i += 1
        j -= 1
        while a[j] > pivot: j -= 1
        if i >= j: return a, j
        a[i], a[j] = a[j], a[i]
@reg(S, 'hoare_partition')
def _(nums): a, j = hoare(nums); return [a, j]
@reg(B, 'hoare_partition')
def _(nums):
    a = list(nums); pivot = a[0]; i = -1; j = len(a)
    while True:
        while True:
            i += 1
            if not a[i] < pivot: break
        while True:
            j -= 1
            if not a[j] > pivot: break
        if i >= j: return [a, j]
        a[i], a[j] = a[j], a[i]

@reg(S, 'heap_sort')
def _(records):
    a = [list(r) for r in records]; n = len(a); cmps = 0
    def sift(root, size):
        nonlocal cmps
        while 2 * root + 1 < size:
            ch = 2 * root + 1
            if ch + 1 < size:
                cmps += 1
                if a[ch + 1][0] > a[ch][0]: ch += 1
            cmps += 1
            if a[root][0] < a[ch][0]: a[root], a[ch] = a[ch], a[root]; root = ch
            else: break
    for s in range(n // 2 - 1, -1, -1): sift(s, n)
    for end in range(n - 1, 0, -1): a[0], a[end] = a[end], a[0]; sift(0, end)
    return [a, cmps]
@reg(B, 'heap_sort')
def _(records):
    a = [list(r) for r in records]; n = len(a); cmps = [0]
    def sift(root, size):
        ch = 2 * root + 1
        if ch >= size: return
        if ch + 1 < size:
            cmps[0] += 1
            if a[ch + 1][0] > a[ch][0]: ch += 1
        cmps[0] += 1
        if a[root][0] < a[ch][0]: a[root], a[ch] = a[ch], a[root]; sift(ch, size)
    for s in reversed(range(n // 2)): sift(s, n)
    for end in reversed(range(1, n)): a[0], a[end] = a[end], a[0]; sift(0, end)
    assert [r[0] for r in a] == sorted(r[0] for r in records)
    return [a, cmps[0]]

@reg(S, 'counting_sort')
def _(records):
    a = [list(r) for r in records]; mx = max(r[0] for r in a); passes = 0; exp = 1
    while True:
        passes += 1; cnt = [0] * 10
        for r in a: cnt[r[0] // exp % 10] += 1
        for d in range(1, 10): cnt[d] += cnt[d - 1]
        out = [None] * len(a)
        for r in reversed(a): cnt[r[0] // exp % 10] -= 1; out[cnt[r[0] // exp % 10]] = r
        a = out; exp *= 10
        if exp > mx: break
    return [a, passes]
@reg(B, 'counting_sort')
def _(records): return [sorted([list(r) for r in records], key=lambda r: r[0]), len(str(max(r[0] for r in records)))]

@reg(S, 'largest_number')
def _(nums):
    ss = sorted(map(str, nums), key=functools.cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
    r = ''.join(ss); return '0' if r[0] == '0' else r
@reg(B, 'largest_number')
def _(nums):
    best = max(''.join(map(str, p)) for p in itertools.permutations(nums)); return '0' if best[0] == '0' else best

@reg(S, 'stability_sort')
def _(records):
    A = [r[0] for r in sorted(records, key=lambda r: (r[1], -r[2]))]
    s = sorted(records, key=lambda r: r[2], reverse=True); Bn = [r[0] for r in sorted(s, key=lambda r: r[1])]
    C = [r[0] for r in sorted(records, key=lambda r: r[1], reverse=True)]
    D = [r[0] for r in sorted(records, key=lambda r: r[1])[::-1]]
    return [A, Bn, C, D]
@reg(B, 'stability_sort')
def _(records):
    idx = list(range(len(records)))
    A = [records[i][0] for i in sorted(idx, key=lambda i: (records[i][1], -records[i][2], i))]
    C = [records[i][0] for i in sorted(idx, key=lambda i: (records[i][1], -i), reverse=True)]
    # C: dept descending, ties in original order: sort by (dept, -index) descending
    D = [records[i][0] for i in sorted(idx, key=lambda i: (records[i][1], i), reverse=True)]
    return [A, A, C, D]

@reg(S, 'sort_mixed_types')
def _(cases):
    out = []
    for c in cases:
        try: p = sorted(c)
        except TypeError: p = 'TypeError'
        try: k = sorted(c, key=lambda v: (v is None, v))
        except TypeError: k = 'TypeError'
        out.append([p, k])
    return out
def _ins(c, key=None):
    a = []
    for v in c:
        kv = key(v) if key else v; j = len(a)
        while j > 0 and kv < (key(a[j - 1]) if key else a[j - 1]): j -= 1
        a.insert(j, v)
    return a
@reg(B, 'sort_mixed_types')
def _(cases):
    out = []
    for c in cases:
        try: p = _ins(c)
        except TypeError: p = 'TypeError'
        try: k = _ins(c, key=lambda v: (v is None, v))
        except TypeError: k = 'TypeError'
        out.append([p, k])
    return out

class Cnt:
    n = 0
    def __init__(self, v): self.v = v
    def __lt__(self, o): Cnt.n += 1; return self.v < o.v
@reg(S, 'adaptive_counts')
def _(nums):
    Cnt.n = 0; sorted([Cnt(v) for v in nums]); tim = Cnt.n
    a = list(nums); cmp = shifts = 0
    for i in range(1, len(a)):
        x = a[i]; j = i
        while j > 0:
            cmp += 1
            if a[j - 1] > x: a[j] = a[j - 1]; shifts += 1; j -= 1
            else: break
        a[j] = x
    mc = [0]; msort([[v, 0] for v in nums], mc)
    inv = sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > nums[j])
    return [tim, cmp, shifts, inv, mc[0]]
@reg(B, 'adaptive_counts')
def _(nums):
    class K:
        c = 0
        def __init__(s, v): s.v = v
        def __lt__(s, o): K.c += 1; return s.v < o.v
    l = [K(v) for v in nums]; l.sort(); tim = K.c
    a = list(nums); cmp = 0; shifts = 0
    for i in range(1, len(a)):
        j = i
        while True:
            if j == 0: break
            cmp += 1
            if not a[j - 1] > a[j]: break
            a[j - 1], a[j] = a[j], a[j - 1]; shifts += 1; j -= 1
    def mcount(x):
        if len(x) <= 1: return 0
        m = len(x) // 2; L, R = sorted(x[:m]), sorted(x[m:]); i = j = c = 0
        while i < len(L) and j < len(R):
            c += 1
            if L[i] <= R[j]: i += 1
            else: j += 1
        return c + mcount(x[:m]) + mcount(x[m:])
    inv = sum(nums[i] > nums[j] for i, j in itertools.combinations(range(len(nums)), 2))
    return [tim, cmp, shifts, inv, mcount(list(nums))]

def minrun(n):
    r = 0
    while n >= 64: r |= n & 1; n >>= 1
    return n + r
@reg(S, 'timsort_minrun')
def _(nums):
    n = len(nums); mr = minrun(n); runs = []; lo = 0
    while lo < n:
        i = lo + 1
        if i < n:
            if nums[i] < nums[lo]:
                while i < n and nums[i] < nums[i - 1]: i += 1
            else:
                while i < n and nums[i] >= nums[i - 1]: i += 1
        rl = max(i - lo, min(mr, n - lo)); runs.append(rl); lo += rl
    return [mr, runs]
@reg(B, 'timsort_minrun')
def _(nums):
    n = len(nums)
    r = 0; k = n
    while k >= 64: r |= k & 1; k >>= 1
    m = k + r
    def natural(lo):
        if lo == n - 1: return 1
        desc = nums[lo + 1] < nums[lo]; e = lo + 1
        while e < n and ((nums[e] < nums[e - 1]) if desc else (nums[e] >= nums[e - 1])): e += 1
        return e - lo
    runs = []; lo = 0
    while lo < n:
        rl = natural(lo)
        if rl < m: rl = min(m, n - lo)
        runs.append(rl); lo += rl
    return [m, runs]

def bin_ins_cmps(perm):
    a = []; c = 0
    for x in perm:
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2; c += 1
            if x < a[mid]: hi = mid
            else: lo = mid + 1
        a.insert(lo, x)
    return c
def optimal_cmps(n):
    perms = list(itertools.permutations(range(n))); pos = [[p.index(v) for v in range(n)] for p in perms]
    pairs = list(itertools.combinations(range(n), 2))
    @functools.lru_cache(None)
    def can(S, L):
        if len(S) == 1: return True
        if L == 0 or len(S) > 2 ** L: return False
        for i, j in pairs:
            a = frozenset(k for k in S if pos[k][i] < pos[k][j]); b = S - a
            if a and b and can(a, L - 1) and can(b, L - 1): return True
        return False
    L = 0; full = frozenset(range(len(perms)))
    while not can(full, L): L += 1
    return L
@reg(S, 'lower_bound')
def _(n):
    perms = list(itertools.permutations(range(n)))
    mw = max(msort([[v, 0] for v in p], c := [0]) and c[0] for p in perms)
    return [(math.factorial(n) - 1).bit_length(), mw, max(bin_ins_cmps(p) for p in perms), optimal_cmps(n)]
@reg(B, 'lower_bound')
def _(n):
    W = {0: 0, 1: 0}
    for k in range(2, n + 1): W[k] = W[k // 2] + W[k - k // 2] + k - 1
    return [math.ceil(math.log2(math.factorial(n))) if n > 1 else 0, W[n], sum((i).bit_length() for i in range(1, n)), [0, 0, 1, 3, 5, 7][n]]

@reg(S, 'maximum_gap')
def _(nums):
    n = len(nums)
    if n < 2: return 0
    lo, hi = min(nums), max(nums)
    if lo == hi: return 0
    size = max(1, (hi - lo) // (n - 1)); nb = (hi - lo) // size + 1; mins = [None] * nb; maxs = [None] * nb
    for v in nums:
        b = (v - lo) // size
        mins[b] = v if mins[b] is None else min(mins[b], v); maxs[b] = v if maxs[b] is None else max(maxs[b], v)
    best = 0; prev = None
    for b in range(nb):
        if mins[b] is None: continue
        if prev is not None: best = max(best, mins[b] - prev)
        prev = maxs[b]
    return best
@reg(B, 'maximum_gap')
def _(nums):
    s = sorted(nums); return max((y - x for x, y in zip(s, s[1:])), default=0)
