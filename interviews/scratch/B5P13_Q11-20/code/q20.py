import math
import random

random.seed(1320)

def pascal(num_rows, row_index):
    tri = []
    for i in range(num_rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = tri[i - 1][j - 1] + tri[i - 1][j]
        tri.append(row)
    row = [1] * (row_index + 1)
    for i in range(1, row_index + 1):
        for j in range(i - 1, 0, -1):          # RIGHT to LEFT: row[j-1] is still last row's value when we use it
            row[j] += row[j - 1]
    return [tri, row]

def brute(num_rows, row_index):
    return [[[math.comb(i, j) for j in range(i + 1)] for i in range(num_rows)],
            [math.comb(row_index, j) for j in range(row_index + 1)]]

examples = [
    (5, 4, [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]),
    (0, 0, [[], [1]]),
    (1, 1, [[[1]], [1, 1]]),
    (3, 10, [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]),
]
for nr, ri, exp in examples:
    got = pascal(nr, ri)
    print(nr, ri, '->', got)
    assert got == exp and brute(nr, ri) == exp

# left-to-right update is wrong: it re-uses a value already overwritten
def wrong_row(n):
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, i):
            row[j] += row[j - 1]
    return row
print('left-to-right row 4:', wrong_row(4), '(correct [1, 4, 6, 4, 1])')
assert wrong_row(4) != [1, 4, 6, 4, 1]

# the multiplicative recurrence C(n,k) = C(n,k-1) * (n-k+1) / k is ALWAYS exact: multiply first, then //
for n in range(0, 200):
    c = 1
    for k in range(1, n + 1):
        assert (c * (n - k + 1)) % k == 0
        c = c * (n - k + 1) // k
        assert c == math.comb(n, k)
print('exact-division recurrence checked for every row n < 200')

# int32 boundary: largest entry of row 33 is below 2^31 - 1, row 34 has an entry above it
mx = lambda n: max(math.comb(n, k) for k in range(n + 1))
print('max entry row 33 =', mx(33), ' row 34 =', mx(34), ' 2^31 - 1 =', 2 ** 31 - 1)
assert mx(33) < 2 ** 31 - 1 < mx(34) and all(mx(n) < 2 ** 31 - 1 for n in range(34))

# row sums are 2^n; symmetry
for n in range(0, 61):
    r = pascal(0, n)[1]
    assert sum(r) == 2 ** n and r == r[::-1]
print('row sums 2^n and symmetry ok for n <= 60')

# seeded random cross-check against math.comb
for _ in range(300):
    nr, ri = random.randint(0, 30), random.randint(0, 200)
    assert pascal(nr, ri) == brute(nr, ri)
print('random cross-check ok: 300 cases')

# edge asserts
assert pascal(0, 0) == [[], [1]] and pascal(2, 0)[1] == [1] and len(pascal(30, 200)[0]) == 30 and len(pascal(30, 200)[1]) == 201
print('edge asserts ok; C(200, 100) has', len(str(math.comb(200, 100))), 'digits')
